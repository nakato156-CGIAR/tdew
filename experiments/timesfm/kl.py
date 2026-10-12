"""Divergencia KL entre el Td observado y el Td de Palacios y de TimesFM (backtest limpio 2013-2016).

Se compara la distribucion marginal de Td: histograma de las observaciones frente al de
cada metodo, sobre los mismos pares (celda, dia). KL(obs || metodo) mide cuanta
informacion se pierde al describir la distribucion observada con la del metodo.
Es una medida de la forma de la distribucion, no del acierto dia a dia: un metodo con
la distribucion correcta pero los dias en desorden tendria KL cercana a 0.

Se reportan KL(obs || metodo), KL(metodo || obs) y la divergencia de Jensen-Shannon,
en nats, con suavizado aditivo de Jeffreys (0,5 por bin) igual para los tres histogramas.
Los valores fuera de rango caen en los bins extremos y se cuentan aparte.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from tdew_estimation import provenance as prov

from . import paths
from .real import refuse_under_res
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE
from .variants import variant

logger = logging.getLogger(__name__)

DEFAULT_PALACIOS = paths.RES / "tuning/backtest_clean/ll4/predictions.parquet"
DEFAULT_TFM = paths.WORK / "preds_nacional/ll4__tmin_anom_full.parquet"
DEFAULT_OUT = Path("reports/timesfm_benchmark/kl_limpio")
SUFFIX = "_limpio"
LO, HI = -20.0, 50.0
BIN_FINE, BIN_COARSE = 0.1, 0.5
ALPHA = 0.5
METHODS = ("palacios", "timesfm")
MANIFEST_REF = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"
SELVA_ZONE_ID = 0
MONTHS = tuple(range(1, 13))


def _edges(width: float) -> np.ndarray:
    return np.round(np.arange(LO, HI + width / 2, width), 6)


def _hist(values: np.ndarray, width: float) -> tuple[np.ndarray, int]:
    """Cuentas por bin; lo que cae fuera de [LO, HI] va al bin extremo y se devuelve su numero."""
    edges = _edges(width)
    out = int(((values < LO) | (values >= HI)).sum())
    clipped = np.clip(values, LO, np.nextafter(HI, LO))
    return np.bincount(np.floor((clipped - LO) / width).astype(np.int64), minlength=len(edges) - 1), out


def divergences(obs_counts: np.ndarray, method_counts: np.ndarray, alpha: float = ALPHA) -> dict:
    p = obs_counts + alpha
    q = method_counts + alpha
    p, q = p / p.sum(), q / q.sum()
    m = 0.5 * (p + q)
    kl_pq = float(np.sum(p * np.log(p / q)))
    kl_qp = float(np.sum(q * np.log(q / p)))
    jsd = float(0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m)))
    return {"kl_obs_method": kl_pq, "kl_method_obs": kl_qp, "jsd": jsd}


def load_pairs(palacios: Path, tfm: Path) -> pd.DataFrame:
    pal = pq.ParquetFile(palacios).read(columns=["ID", "FECHA", "TD_obs", "pred_tuned"]).to_pandas()
    tf = pq.ParquetFile(tfm).read(columns=["ID", "FECHA", "pred"]).to_pandas()
    frame = pal.merge(tf, on=["ID", "FECHA"], how="inner", validate="one_to_one")
    logger.info("pares de Palacios %d, de TimesFM %d, comunes %d (descartados de TimesFM: %d)",
                len(pal), len(tf), len(frame), len(tf) - len(frame))
    frame = frame.rename(columns={"pred_tuned": "palacios", "pred": "timesfm", "TD_obs": "obs"})
    return frame.dropna(subset=["obs", "palacios", "timesfm"]).reset_index(drop=True)


def group_masks(frame: pd.DataFrame, tier: pd.Series, zone: pd.Series) -> dict[str, np.ndarray]:
    tiers = frame["ID"].map(tier).fillna("desconocido").to_numpy()
    selva = (frame["ID"].map(zone).to_numpy() == SELVA_ZONE_ID)
    month = frame["FECHA"].dt.month.to_numpy()
    masks: dict[str, np.ndarray] = {"todo|todo": np.ones(len(frame), dtype=bool)}
    for name in ("within", "near", "marginal", "extrapolated", "unsupported"):
        masks[f"tier|{name}"] = tiers == name
    masks["zona|selva A (r) A'"] = selva
    masks["zona|resto"] = ~selva
    for mth in MONTHS:
        masks[f"mes|{mth:02d}"] = month == mth
    return masks


def compute(frame: pd.DataFrame, tier: pd.Series, zone: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (tabla de divergencias por grupo y metodo, histogramas gruesos del grupo 'todo')."""
    rows = []
    for key, mask in group_masks(frame, tier, zone).items():
        kind, name = key.split("|", 1)
        n = int(mask.sum())
        if n == 0:
            continue
        for width, label in ((BIN_FINE, "0.1"), (BIN_COARSE, "0.5")):
            obs_counts, _ = _hist(frame["obs"].to_numpy()[mask], width)
            for method in METHODS:
                counts, out = _hist(frame[method].to_numpy()[mask], width)
                rows.append({"group_kind": kind, "group": name, "method": method, "bin_width": label,
                             "n": n, "n_out_of_range": out, **divergences(obs_counts, counts)})
    table = pd.DataFrame(rows)

    edges = _edges(BIN_COARSE)
    hist = {"bin_lo": edges[:-1], "bin_hi": edges[1:]}
    for col in ("obs", *METHODS):
        counts, _ = _hist(frame[col].to_numpy(), BIN_COARSE)
        hist[col] = counts
    hist = pd.DataFrame(hist)
    hist = hist[(hist[["obs", *METHODS]].sum(axis=1) > 0)].reset_index(drop=True)
    return table, hist


def build_provenance(*, n_cells: int, outputs: Sequence[Path], bead_id: str, palacios: Path, tfm: Path) -> prov.MetricProvenance:
    spec = variant("tmin_anom_full")
    return prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id=bead_id, manifest_ref=MANIFEST_REF, model_family=spec.family, model_id=spec.checkpoint,
        variant_label=spec.key, trained=False, training_period=None, validation_period=None,
        test_period=("2013-01-01", "2016-12-31"), split_id="ll4", autoregressive=False,
        target_type=spec.target_type, climatology_used=spec.climatology_used,
        climatology_role=spec.climatology_role, inputs=tuple(spec.inputs),
        panel_id=f"nacional_{n_cells}_limpio", panel_cell_count=int(n_cells), panel_file=str(tfm),
        output_files=tuple(str(p) for p in outputs),
        notes=(f"KL(obs || metodo) entre la distribucion de Td observado y la de Palacios (tuned) y TimesFM, "
               f"backtest limpio 2013-2016. Mide la forma de la distribucion, no el acierto dia a dia. "
               f"Palacios leido de {palacios}, TimesFM de {tfm}. Suavizado de Jeffreys 0,5 por bin, "
               f"bins de 0,1 y 0,5 C en [{LO}, {HI}). Pesos de TimesFM de uso no comercial."),
    )


def write_outputs(table: pd.DataFrame, hist: pd.DataFrame, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, frame in (("kl_by_group", table), ("kl_hist", hist)):
        path = out_dir / f"{name}{SUFFIX}.csv"
        frame.to_csv(path, index=False)
        written.append(path)
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--palacios", type=Path, default=DEFAULT_PALACIOS)
    parser.add_argument("--timesfm", type=Path, default=DEFAULT_TFM)
    parser.add_argument("--zone-table", type=Path, default=DEFAULT_ZONE)
    parser.add_argument("--support-distance", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--bead-id", default="tdew-214.13")
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    parser.add_argument("--repo-root", type=Path, default=prov.REPO_ROOT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    for target in (args.out_dir, args.registry_path):
        refuse_under_res(target)

    frame = load_pairs(args.palacios, args.timesfm)
    logger.info("%d pares, %d celdas", len(frame), frame["ID"].nunique())
    tier = pd.read_parquet(args.support_distance, columns=["ID", "tier"]).set_index("ID")["tier"]
    zone = pd.read_parquet(args.zone_table, columns=["ID", "zone_id"]).set_index("ID")["zone_id"]
    table, hist = compute(frame, tier, zone)
    written = write_outputs(table, hist, args.out_dir)
    record = build_provenance(n_cells=int(frame["ID"].nunique()), outputs=written, bead_id=args.bead_id,
                              palacios=args.palacios, tfm=args.timesfm)
    prov.record_metric_provenance(record, registry_path=args.registry_path, repo_root=args.repo_root)
    view = table[(table.bin_width == "0.1") & (table.group_kind.isin(["todo", "tier", "zona"]))]
    print(view.round(5).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
