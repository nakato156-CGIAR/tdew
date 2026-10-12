"""Cola calida de TimesFM y de Palacios en 2017-2020 (E9; analogo a ``sec-results-tail`` del paper).

El paper caracteriza en Palacios una cola de valores de Td fisicamente implausibles
(por encima de 35 C): casi todos fuera del dominio con estaciones, en la clase
Thornthwaite ``A (r) A'`` (el llano amazonico) y concentrados en noviembre. Este modulo
mide lo mismo en los **dos** productos sobre el mismo campo, para ver si TimesFM
reproduce esa cola.

No hay verdad observada de Td en 2017-2020: lo que se compara es la **coincidencia
entre dos productos**, no el error de ninguno. Que un valor supere 35 C es un criterio
fisico (el record mundial de punto de rocio ronda 35 C), no una comparacion con la
observacion.

Procesa bucket por bucket y acumula conteos y un histograma fino (sin cargar los
3.18e9 valores), con el mismo patron que ``real_compare``.
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd

from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.bucket_layout import bucket_dir_name

from . import paths
from .real import (
    DEFAULT_OUT_DIR,
    DEFAULT_PALACIOS_ROOT,
    EXPECTED_CELLS,
    HORIZON_DAYS,
    HORIZON_START,
    MANIFEST_REF_REAL,
    MLFLOW_EXPERIMENT,
    PRED_NAME,
    VARIANT_KEY,
    date_to_day,
)
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE, _read_product
from .variants import variant

logger = logging.getLogger("timesfm.real_tail")

PRODUCTS = ("timesfm", "palacios")
SUFFIX = "_limpio"
DEFAULT_OUT = Path("reports/timesfm_benchmark/real_limpio")
DEFAULT_AGG = paths.WORK / "agg_real"

THRESHOLDS = (35.0, 38.0)  # umbral primario del paper y uno mas alto
PRIMARY = THRESHOLDS[0]
TIERS = ("within", "near", "marginal", "extrapolated", "unsupported", "desconocido")
TIER_INDEX = {name: k for k, name in enumerate(TIERS)}
SELVA_ZONE = 0  # zona 0 = "A (r) A'" (perhumedo, megatermal): el llano amazonico
YEARS = (2017, 2018, 2019, 2020)

DATES = pd.date_range(HORIZON_START, periods=HORIZON_DAYS, freq="D")
YEAR = DATES.year.to_numpy()
MONTH = DATES.month.to_numpy()

# Histograma fino de Td: bin 0 = por debajo de HIST_LO; bins 1..N = [HIST_LO + (k-1)*STEP, ...);
# bin N+1 = por encima de HIST_HI. Sirve para la curva de supervivencia de la cola.
HIST_LO, HIST_HI, HIST_STEP = 10.0, 46.0, 0.05
N_BINS = int(round((HIST_HI - HIST_LO) / HIST_STEP))
SURVIVAL_GRID = tuple(float(x) for x in np.arange(25.0, 42.0 + 1e-9, 0.5))
N_GROUPS = len(TIERS) * 2  # (nivel de soporte) x (selva si/no)


def _tier_index(tiers: np.ndarray) -> np.ndarray:
    return pd.Series(tiers).map(TIER_INDEX).fillna(TIER_INDEX["desconocido"]).to_numpy(np.int64)


def _hist_index(values: np.ndarray) -> np.ndarray:
    k = np.floor((values - HIST_LO) / HIST_STEP).astype(np.int64) + 1
    return np.clip(k, 0, N_BINS + 1)


class _Counts:
    """Conteos de un producto."""

    def __init__(self) -> None:
        self.n = 0
        self.nan = 0
        self.max = -np.inf
        self.above = {thr: 0 for thr in THRESHOLDS}
        self.tier_values = np.zeros(len(TIERS))
        self.tier_cells = np.zeros(len(TIERS))
        self.tier_above = {thr: np.zeros(len(TIERS)) for thr in THRESHOLDS}
        self.sel_values = np.zeros(2)
        self.sel_cells = np.zeros(2)
        self.sel_above = {thr: np.zeros(2) for thr in THRESHOLDS}
        self.sel_month_values = np.zeros(2 * 13)
        self.sel_month_above = np.zeros(2 * 13)
        self.year_values = np.zeros(len(YEARS))
        self.year_above = np.zeros(len(YEARS))
        self.hist = np.zeros((N_GROUPS, N_BINS + 2))
        self.cells_any: list[pd.DataFrame] = []

    def add(self, ids: np.ndarray, day: np.ndarray, values: np.ndarray, meta: Mapping[str, pd.Series]) -> None:
        v = np.asarray(values, dtype=np.float64)
        ids, day = np.asarray(ids, dtype=np.int64), np.asarray(day, dtype=np.int64)
        self.nan += int((~np.isfinite(v)).sum())
        keep = np.isfinite(v)
        ids, day, v = ids[keep], day[keep], v[keep]
        if v.size == 0:
            return
        self.n += v.size
        self.max = max(self.max, float(v.max()))
        tier = _tier_index(meta["tier"].reindex(ids).fillna("desconocido").to_numpy())
        sel = (meta["zone"].reindex(ids).fillna(-1).to_numpy() == SELVA_ZONE).astype(np.int64)
        month, year = MONTH[day], YEAR[day] - YEARS[0]

        self.tier_values += np.bincount(tier, minlength=len(TIERS))
        self.sel_values += np.bincount(sel, minlength=2)
        self.sel_month_values += np.bincount(sel * 13 + month, minlength=26)
        self.year_values += np.bincount(year, minlength=len(YEARS))
        grp = tier * 2 + sel
        self.hist += np.bincount(grp * (N_BINS + 2) + _hist_index(v),
                                 minlength=N_GROUPS * (N_BINS + 2)).reshape(N_GROUPS, N_BINS + 2)

        uniq = np.unique(ids)
        u_tier = _tier_index(meta["tier"].reindex(uniq).fillna("desconocido").to_numpy())
        u_sel = (meta["zone"].reindex(uniq).fillna(-1).to_numpy() == SELVA_ZONE).astype(np.int64)
        self.tier_cells += np.bincount(u_tier, minlength=len(TIERS))
        self.sel_cells += np.bincount(u_sel, minlength=2)

        for thr in THRESHOLDS:
            m = v > thr
            self.above[thr] += int(m.sum())
            self.tier_above[thr] += np.bincount(tier[m], minlength=len(TIERS))
            self.sel_above[thr] += np.bincount(sel[m], minlength=2)
            if thr == PRIMARY:
                self.sel_month_above += np.bincount(sel[m] * 13 + month[m], minlength=26)
                self.year_above += np.bincount(year[m], minlength=len(YEARS))


class TailAccumulator:
    def __init__(self) -> None:
        self.product = {name: _Counts() for name in PRODUCTS}
        # Solape entre productos sobre las mismas celdas y dias: [ambos, solo TimesFM, solo Palacios, filas]
        self.joint = np.zeros((2, 4))
        self.cell_frames: list[pd.DataFrame] = []
        self.buckets = 0

    def add_bucket(self, bucket: int, tfm: pd.DataFrame, pal: pd.DataFrame, *, meta: Mapping[str, pd.Series]) -> None:
        t = pd.DataFrame({"ID": tfm["ID"].to_numpy(np.int64), "day": tfm["day"].to_numpy(np.int64),
                          "p": tfm["pred"].to_numpy(np.float64)})
        o = pd.DataFrame({"ID": pal["ID"].to_numpy(np.int64), "day": date_to_day(pal["FECHA"]).astype(np.int64),
                          "o": pal["TD_predicted"].to_numpy(np.float64)})
        self.product["timesfm"].add(t["ID"].to_numpy(), t["day"].to_numpy(), t["p"].to_numpy(), meta)
        self.product["palacios"].add(o["ID"].to_numpy(), o["day"].to_numpy(), o["o"].to_numpy(), meta)
        self.buckets += 1

        j = t.merge(o, on=["ID", "day"], how="inner")
        j = j[np.isfinite(j["p"]) & np.isfinite(j["o"])]
        if not j.empty:
            sel = (meta["zone"].reindex(j["ID"].to_numpy()).fillna(-1).to_numpy() == SELVA_ZONE).astype(np.int64)
            a, b = (j["p"].to_numpy() > PRIMARY), (j["o"].to_numpy() > PRIMARY)
            for k, mask in enumerate((a & b, a & ~b, ~a & b, np.ones_like(a))):
                self.joint[:, k] += np.bincount(sel[mask], minlength=2)

        # Celdas con algun valor sobre el umbral en cualquiera de los dos productos.
        hit = np.union1d(t.loc[t["p"] > PRIMARY, "ID"].to_numpy(), o.loc[o["o"] > PRIMARY, "ID"].to_numpy())
        if hit.size:
            parts = []
            for name, frame, col in (("timesfm", t, "p"), ("palacios", o, "o")):
                sub = frame[frame["ID"].isin(hit)]
                g = sub.groupby("ID")[col]
                parts.append(pd.DataFrame({
                    f"n_above_{name}": g.apply(lambda s: int((s > PRIMARY).sum())),
                    f"max_{name}": g.max()}))
            self.cell_frames.append(pd.concat(parts, axis=1).fillna({"n_above_timesfm": 0, "n_above_palacios": 0})
                                    .rename_axis("ID").reset_index())

    # ----------------------------------------------------------------- tablas
    def summary(self) -> pd.DataFrame:
        rows = []
        for name, c in self.product.items():
            cells_hit = self._cells_hit(name)
            row = {"product": name, "n": c.n, "nan": c.nan, "max": c.max, "cells": int(c.tier_cells.sum()),
                   "cells_with_exceedance": int(cells_hit["ID"].nunique()) if len(cells_hit) else 0}
            for thr in THRESHOLDS:
                row[f"above_{thr:g}"] = c.above[thr]
                row[f"pct_above_{thr:g}"] = 100.0 * c.above[thr] / c.n if c.n else float("nan")
            rows.append(row)
        return pd.DataFrame(rows)

    def _cells_hit(self, name: str) -> pd.DataFrame:
        if not self.cell_frames:
            return pd.DataFrame({"ID": np.array([], dtype=np.int64)})
        frame = pd.concat(self.cell_frames, ignore_index=True)
        return frame.loc[frame[f"n_above_{name}"] > 0, ["ID"]]

    def by_tier(self, meta_tier: pd.Series) -> pd.DataFrame:
        rows = []
        total_cells = {name: c.tier_cells.sum() for name, c in self.product.items()}
        for name, c in self.product.items():
            hit = self._cells_hit(name)
            hit_tier = _tier_index(meta_tier.reindex(hit["ID"].to_numpy()).fillna("desconocido").to_numpy()) \
                if len(hit) else np.array([], dtype=np.int64)
            affected = np.bincount(hit_tier, minlength=len(TIERS))
            for k, tier in enumerate(TIERS):
                if c.tier_cells[k] == 0 and c.tier_values[k] == 0:
                    continue
                rows.append({"product": name, "tier": tier, "cells": int(c.tier_cells[k]),
                             "pct_field": 100.0 * c.tier_cells[k] / total_cells[name],
                             "cells_affected": int(affected[k]), "values": int(c.tier_values[k]),
                             "above_35": int(c.tier_above[PRIMARY][k]),
                             "pct_above_35": 100.0 * c.tier_above[PRIMARY][k] / c.tier_values[k]
                             if c.tier_values[k] else float("nan"),
                             "above_38": int(c.tier_above[THRESHOLDS[1]][k])})
        return pd.DataFrame(rows)

    def by_zone_class(self, meta_zone: pd.Series) -> pd.DataFrame:
        rows = []
        for name, c in self.product.items():
            hit = self._cells_hit(name)
            hit_sel = (meta_zone.reindex(hit["ID"].to_numpy()).fillna(-1).to_numpy() == SELVA_ZONE).astype(np.int64) \
                if len(hit) else np.array([], dtype=np.int64)
            affected = np.bincount(hit_sel, minlength=2)
            total_above = c.sel_above[PRIMARY].sum()
            for k, label in ((1, "selva_A(r)A'"), (0, "resto")):
                rows.append({"product": name, "zone_class": label, "cells": int(c.sel_cells[k]),
                             "cells_affected": int(affected[k]), "values": int(c.sel_values[k]),
                             "above_35": int(c.sel_above[PRIMARY][k]),
                             "pct_above_35": 100.0 * c.sel_above[PRIMARY][k] / c.sel_values[k]
                             if c.sel_values[k] else float("nan"),
                             "share_of_all_exceedances": 100.0 * c.sel_above[PRIMARY][k] / total_above
                             if total_above else float("nan"),
                             "above_38": int(c.sel_above[THRESHOLDS[1]][k])})
        return pd.DataFrame(rows)

    def by_month(self) -> pd.DataFrame:
        rows = []
        for name, c in self.product.items():
            for label, ks in (("selva_A(r)A'", (1,)), ("resto", (0,)), ("todo", (0, 1))):
                for month in range(1, 13):
                    values = sum(c.sel_month_values[k * 13 + month] for k in ks)
                    above = sum(c.sel_month_above[k * 13 + month] for k in ks)
                    rows.append({"product": name, "zone_class": label, "month": month, "values": int(values),
                                 "above_35": int(above),
                                 "pct_above_35": 100.0 * above / values if values else float("nan")})
        return pd.DataFrame(rows)

    def by_year(self) -> pd.DataFrame:
        rows = []
        for name, c in self.product.items():
            for k, year in enumerate(YEARS):
                rows.append({"product": name, "year": year, "values": int(c.year_values[k]),
                             "above_35": int(c.year_above[k]),
                             "pct_above_35": 100.0 * c.year_above[k] / c.year_values[k]
                             if c.year_values[k] else float("nan")})
        return pd.DataFrame(rows)

    def joint_table(self) -> pd.DataFrame:
        rows = []
        for label, ks in (("todo", (0, 1)), ("selva_A(r)A'", (1,)), ("resto", (0,))):
            both, only_t, only_p, n = (float(sum(self.joint[k, i] for k in ks)) for i in range(4))
            above_t, above_p = both + only_t, both + only_p
            rows.append({"zone_class": label, "rows": int(n), "both_above_35": int(both),
                         "only_timesfm": int(only_t), "only_palacios": int(only_p),
                         "timesfm_above_given_palacios_above": both / above_p if above_p else float("nan"),
                         "palacios_above_given_timesfm_above": both / above_t if above_t else float("nan")})
        return pd.DataFrame(rows)

    def survival(self) -> pd.DataFrame:
        """P(Td >= x), con x redondeado al bin de 0.05 C, por producto y grupo de celdas."""
        # Grupo de histograma = nivel de soporte * 2 + (1 si la celda es de la selva).
        groups_of = {
            "todo": list(range(N_GROUPS)),
            "selva_A(r)A'": [k * 2 + 1 for k in range(len(TIERS))],
            "resto": [k * 2 for k in range(len(TIERS))],
            "selva_con_apoyo": [TIER_INDEX["within"] * 2 + 1],
            "selva_sin_apoyo": [TIER_INDEX["unsupported"] * 2 + 1],
        }

        rows = []
        for name, c in self.product.items():
            for label, groups in groups_of.items():
                h = c.hist[groups].sum(axis=0)
                total = h.sum()
                for x in SURVIVAL_GRID:
                    k = int(np.floor((x - HIST_LO) / HIST_STEP)) + 1
                    n_ge = float(h[k:].sum())
                    rows.append({"product": name, "group": label, "x": x, "n_ge": int(n_ge),
                                 "frac_ge": n_ge / total if total else float("nan"), "n_group": int(total)})
        return pd.DataFrame(rows)

    def per_cell(self) -> pd.DataFrame:
        if not self.cell_frames:
            return pd.DataFrame(columns=["ID", "n_above_timesfm", "max_timesfm", "n_above_palacios", "max_palacios"])
        frame = pd.concat(self.cell_frames, ignore_index=True).sort_values("ID")
        return frame[["ID", "n_above_timesfm", "max_timesfm", "n_above_palacios", "max_palacios"]]


def write_outputs(acc: TailAccumulator, out_dir: Path, agg_dir: Path, *, meta: Mapping[str, pd.Series]) -> list[Path]:
    out_dir, agg_dir = Path(out_dir), Path(agg_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    agg_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def save(frame: pd.DataFrame, directory: Path, name: str) -> None:
        path = directory / f"{name}{SUFFIX}.csv"
        frame.to_csv(path, index=False)
        written.append(path)

    save(acc.summary(), out_dir, "tail_summary")
    save(acc.by_tier(meta["tier"]), out_dir, "tail_by_tier")
    save(acc.by_zone_class(meta["zone"]), out_dir, "tail_by_zone_class")
    save(acc.by_month(), out_dir, "tail_by_month")
    save(acc.by_year(), out_dir, "tail_by_year")
    save(acc.joint_table(), out_dir, "tail_joint")
    save(acc.survival(), out_dir, "tail_survival")
    save(acc.per_cell(), agg_dir, "tail_by_cell")
    return written


def build_tail_provenance(*, n_cells: int, outputs: Sequence[Path], bead_id: str,
                          tfm_root: Path, palacios_root: Path) -> prov.MetricProvenance:
    spec = variant(VARIANT_KEY)
    return prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id=bead_id, manifest_ref=MANIFEST_REF_REAL, model_family=spec.family,
        model_id=spec.checkpoint, variant_label=spec.key, trained=False, training_period=None,
        validation_period=None, test_period=("2017-01-01", "2020-12-31"), split_id="real_2017_2020",
        autoregressive=False, target_type=spec.target_type, climatology_used=spec.climatology_used,
        climatology_role=spec.climatology_role, inputs=tuple(spec.inputs),
        panel_id=f"real_{n_cells}_td", panel_cell_count=int(n_cells), panel_file=None,
        output_files=tuple(str(p) for p in outputs),
        notes=(f"Cola calida (Td > 35 C) de TimesFM y de Palacios, analogo a sec-results-tail del paper. "
               f"Sin verdad observada: es coincidencia entre productos y un criterio fisico, no error. "
               f"TimesFM leido de {tfm_root}, Palacios de {palacios_root}. Pesos de TimesFM de uso no comercial."),
    )


# ---------------------------------------------------------------------- CLI

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tfm-root", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--palacios-root", type=Path, default=DEFAULT_PALACIOS_ROOT)
    parser.add_argument("--zone-table", type=Path, default=DEFAULT_ZONE)
    parser.add_argument("--support-distance", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--agg-dir", type=Path, default=DEFAULT_AGG)
    parser.add_argument("--buckets", default=None, help="'0,1' o '0-3'; por defecto, todos los de --tfm-root")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--mlflow", action="store_true")
    parser.add_argument("--mlflow-uri", default=et.DEFAULT_TRACKING_URI)
    parser.add_argument("--mlflow-experiment", default=MLFLOW_EXPERIMENT)
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--bead-id", default="tdew-214.13")
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    parser.add_argument("--repo-root", type=Path, default=prov.REPO_ROOT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    from .real import parse_buckets, refuse_under_res

    for target in (args.out_dir, args.agg_dir, args.registry_path):
        refuse_under_res(target)

    if args.buckets:
        buckets = parse_buckets(args.buckets)
    else:
        buckets = sorted(int(p.name.split("=")[1]) for p in args.tfm_root.glob("id_bucket=*")
                         if (p / PRED_NAME).exists())
    meta = {"zone": pd.read_parquet(args.zone_table, columns=["ID", "zone_id"]).set_index("ID")["zone_id"],
            "tier": pd.read_parquet(args.support_distance, columns=["ID", "tier"]).set_index("ID")["tier"]}

    def load(bucket: int) -> tuple[pd.DataFrame, pd.DataFrame]:
        tfm = _read_product(args.tfm_root / bucket_dir_name(bucket) / PRED_NAME, ["ID", "day", "pred"])
        pal = _read_product(args.palacios_root / bucket_dir_name(bucket) / PRED_NAME,
                            ["ID", "FECHA", "TD_predicted"])
        return tfm, pal

    acc = TailAccumulator()
    window = max(1, args.workers) * 2
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        for start in range(0, len(buckets), window):
            chunk = buckets[start : start + window]
            for bucket, (tfm, pal) in zip(chunk, pool.map(load, chunk)):
                acc.add_bucket(bucket, tfm, pal, meta=meta)
            logger.info("%d/%d buckets", min(start + window, len(buckets)), len(buckets))

    written = write_outputs(acc, args.out_dir, args.agg_dir, meta=meta)
    n_cells = int(acc.product["palacios"].tier_cells.sum())
    record = build_tail_provenance(n_cells=n_cells, outputs=written, bead_id=args.bead_id,
                                   tfm_root=args.tfm_root, palacios_root=args.palacios_root)
    if args.mlflow:
        import mlflow

        summary = acc.summary().set_index("product")
        metrics = {f"{name}_{col}": float(summary.loc[name, col]) for name in PRODUCTS
                   for col in ("n", "max", "cells_with_exceedance", "above_35", "pct_above_35")}
        metrics["buckets"] = float(len(buckets))
        with et.start_run(
            args.run_name or f"timesfm-real-tail-{len(buckets)}buckets",
            params={"split": "real", "variant": VARIANT_KEY, "bead_id": args.bead_id,
                    "panel_id": record.panel_id, "full_panel": len(buckets) == 8192 and n_cells == EXPECTED_CELLS,
                    "tfm_root": str(args.tfm_root)},
            tracking_uri=args.mlflow_uri, experiment_name=args.mlflow_experiment,
        ) as run:
            mlflow.log_metrics({k: v for k, v in metrics.items() if np.isfinite(v)})
            record = dataclasses.replace(record, mlflow_run_id=run.info.run_id)
    prov.record_metric_provenance(record, registry_path=args.registry_path, repo_root=args.repo_root)
    print(acc.summary().to_string(index=False))
    print(acc.by_zone_class(meta["zone"]).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
