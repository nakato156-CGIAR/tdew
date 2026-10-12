"""Acuerdo entre el producto TimesFM y el de Palacios en 2017-2020 (E9, PLAN_3 sec. 9).

No hay verdad observada de Td en 2017-2020, asi que ninguna metrica de este modulo
es un error: son sesgo, RMSE, MAE y r **entre dos productos**, con la diferencia
siempre ``TimesFM - Palacios``. El sesgo no se interpreta como sesgo del metodo.

Procesa bucket por bucket y acumula sumas (sin cargar los 3.18e9 valores), con el
patron de ``escala.py`` y ``tdew_estimation.metrics.MetricsAccum``.
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
import pyarrow.parquet as pq

from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.bucket_layout import bucket_dir_name
from tdew_estimation.metrics import MetricsAccum

from . import paths
from .panel import DEFAULT_HISTORICAL_ROOT, build_panel, split_spec
from .real import (
    DEFAULT_FUTURE_ROOT,
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
from .variants import variant

logger = logging.getLogger("timesfm.real_compare")

DATES = pd.date_range(HORIZON_START, periods=HORIZON_DAYS, freq="D")
YEAR = DATES.year.to_numpy()
MONTH = DATES.month.to_numpy()
DOY = DATES.dayofyear.to_numpy()
YEARS = (2017, 2018, 2019, 2020)
DIMENSIONS = ("year", "month", "zone", "tier", "site")
PRODUCTS = ("timesfm", "palacios")
SUFFIX = "_limpio"
DEFAULT_OUT = Path("reports/timesfm_benchmark/real_limpio")
DEFAULT_AGG = paths.WORK / "agg_real"
_RES = paths.RES
DEFAULT_ZONE = _RES / "zone_table.parquet"
DEFAULT_SUPPORT = _RES / "tuning" / "support_distance.parquet"
DEFAULT_SILVER = Path("Data/silver/department_grid_ids")

# Cifras del producto de Palacios publicadas en el paper (reports/paper/paper.qmd). Las medias
# anuales del paper son el promedio sin ponderar de las 12 medias mensuales nacionales
# (reports/paper/scripts/qc_fill.py:82-85), no la media de todas las celdas-dia del año.
PALACIOS_PAPER = {
    "n": 3_183_266_247, "mean": 19.39,
    "mean_2017": 19.36, "mean_2018": 19.30, "mean_2019": 19.41, "mean_2020": 19.51,
    "min": -13.29, "max": 41.16,
}
PAPER_ROUNDING = 0.005  # el paper redondea a 2 decimales


def paper_convention_figures(figures: pd.DataFrame, product: str) -> dict[str, float]:
    """Cifras de ``product`` con la definicion del paper: ``mean_<año>`` = media de medias mensuales."""
    row = figures.set_index("product").loc[product].to_dict()
    out = {k: row[k] for k in PALACIOS_PAPER}
    for year in YEARS:
        out[f"mean_{year}"] = row[f"mean_{year}_monthly"]
    return out


def reproduction_control(observed: Mapping[str, float], *, full_panel: bool) -> pd.DataFrame:
    """Compara las cifras de Palacios recalculadas con las del paper.

    ``observed["mean_<año>"]`` debe seguir la convencion del paper (media de las
    medias mensuales); ``paper_convention_figures`` la arma desde ``product_figures``.
    Con un subconjunto de buckets el control no aplica: ``ok`` es NaN.
    """
    rows = []
    for key, expected in PALACIOS_PAPER.items():
        got = float(observed[key])
        if not full_panel:
            ok = np.nan
        elif key == "n":
            ok = bool(int(got) == expected)
        else:
            ok = bool(abs(got - expected) <= PAPER_ROUNDING + 1e-9)
        rows.append({"quantity": key, "paper": expected, "observed": got,
                     "diff": got - expected, "ok": ok})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------- acumulador

_SUM_FIELDS = ("n", "sum_err", "sum_err2", "sum_abserr", "sum_p", "sum_o", "sum_p2", "sum_o2", "sum_po")


def _finalize(sums: np.ndarray) -> dict[str, float]:
    acc = MetricsAccum()
    for name, value in zip(_SUM_FIELDS, sums):
        setattr(acc, name, int(value) if name == "n" else float(value))
    return acc.finalize()


def _sums(frame: pd.DataFrame) -> pd.DataFrame:
    """Suma por clave de las nueve sumas de MetricsAccum. ``frame`` trae k, p, o."""
    d = frame["p"] - frame["o"]
    work = pd.DataFrame({
        "k": frame["k"], "n": 1.0, "sum_err": d, "sum_err2": d * d, "sum_abserr": d.abs(),
        "sum_p": frame["p"], "sum_o": frame["o"], "sum_p2": frame["p"] ** 2,
        "sum_o2": frame["o"] ** 2, "sum_po": frame["p"] * frame["o"],
    })
    return work.groupby("k", sort=False)[list(_SUM_FIELDS)].sum()


class _Product:
    """Cifras de un producto sobre todas sus filas (no solo las que se unen)."""

    def __init__(self) -> None:
        self.n = 0
        self.nan = 0
        self.inf = 0
        self.total = 0.0
        self.min = np.inf
        self.max = -np.inf
        self.year_n = np.zeros(len(YEARS))
        self.year_sum = np.zeros(len(YEARS))
        self.month_n = np.zeros((len(YEARS), 12))
        self.month_sum = np.zeros((len(YEARS), 12))
        self.cells = 0
        self.rows_only = 0

    def add(self, ids: np.ndarray, day: np.ndarray, values: np.ndarray) -> None:
        v = np.asarray(values, dtype=np.float64)
        self.nan += int(np.isnan(v).sum())
        self.inf += int(np.isinf(v).sum())
        finite = np.isfinite(v)
        f = v[finite]
        if f.size:
            self.n += f.size
            self.total += float(f.sum())
            self.min = min(self.min, float(f.min()))
            self.max = max(self.max, float(f.max()))
            day_f = np.asarray(day)[finite].astype(np.int64)
            years = YEAR[day_f]
            for k, year in enumerate(YEARS):
                m = years == year
                self.year_n[k] += int(m.sum())
                self.year_sum[k] += float(f[m].sum())
            slot = (years - YEARS[0]) * 12 + (MONTH[day_f] - 1)
            self.month_n += np.bincount(slot, minlength=len(YEARS) * 12).reshape(len(YEARS), 12)
            self.month_sum += np.bincount(slot, weights=f, minlength=len(YEARS) * 12).reshape(len(YEARS), 12)
        self.cells += int(np.unique(ids).size)


class Accumulator:
    def __init__(self) -> None:
        self.product = {name: _Product() for name in PRODUCTS}
        self.groups: dict[str, dict] = {"all": {}, **{dim: {} for dim in DIMENSIONS}}
        z = lambda: np.zeros(HORIZON_DAYS)  # noqa: E731
        self.day_n, self.day_p, self.day_o, self.day_d, self.day_d2 = z(), z(), z(), z(), z()
        self.cell_frames: list[pd.DataFrame] = []
        self.tmin = {name: np.zeros(3) for name in PRODUCTS}  # n, sum(td - tmin), count(td > tmin)
        self.clim_sum = np.zeros(367)
        self.clim_cells = 0
        self.buckets = 0

    # ------------------------------------------------------------------ entrada
    def add_bucket(
        self,
        bucket: int,
        tfm: pd.DataFrame,
        pal: pd.DataFrame,
        *,
        meta: Mapping[str, pd.Series],
        tmin: pd.DataFrame | None = None,
        clim: tuple[np.ndarray, np.ndarray] | None = None,
    ) -> None:
        t = pd.DataFrame({"ID": tfm["ID"].to_numpy(np.int64), "day": tfm["day"].to_numpy(np.int64),
                          "p": tfm["pred"].to_numpy(np.float64)})
        o = pd.DataFrame({"ID": pal["ID"].to_numpy(np.int64), "day": date_to_day(pal["FECHA"]).astype(np.int64),
                          "o": pal["TD_predicted"].to_numpy(np.float64)})
        self.product["timesfm"].add(t["ID"].to_numpy(), t["day"].to_numpy(), t["p"].to_numpy())
        self.product["palacios"].add(o["ID"].to_numpy(), o["day"].to_numpy(), o["o"].to_numpy())

        merged = t.merge(o, on=["ID", "day"], how="outer", indicator=True)
        self.product["timesfm"].rows_only += int((merged["_merge"] == "left_only").sum())
        self.product["palacios"].rows_only += int((merged["_merge"] == "right_only").sum())
        j = merged[merged["_merge"] == "both"]
        j = j[np.isfinite(j["p"]) & np.isfinite(j["o"])]
        self.buckets += 1
        if j.empty:
            return
        ids, day = j["ID"].to_numpy(), j["day"].to_numpy()
        p, ob = j["p"].to_numpy(), j["o"].to_numpy()
        d = p - ob

        def keys(dim: str) -> np.ndarray:
            if dim == "year":
                return YEAR[day]
            if dim == "month":
                return MONTH[day]
            missing = {"zone": -1, "tier": "desconocido", "site": "otro"}[dim]
            return meta[dim].reindex(ids).fillna(missing).to_numpy()

        base = pd.DataFrame({"p": p, "o": ob})
        for dim in ("all", *DIMENSIONS):
            base["k"] = 0 if dim == "all" else keys(dim)
            for key, row in _sums(base).iterrows():
                store = self.groups[dim]
                store[key] = store.get(key, 0.0) + row.to_numpy()
        base = base.drop(columns="k")

        self.day_n += np.bincount(day, minlength=HORIZON_DAYS)
        self.day_p += np.bincount(day, weights=p, minlength=HORIZON_DAYS)
        self.day_o += np.bincount(day, weights=ob, minlength=HORIZON_DAYS)
        self.day_d += np.bincount(day, weights=d, minlength=HORIZON_DAYS)
        self.day_d2 += np.bincount(day, weights=d * d, minlength=HORIZON_DAYS)

        cell = pd.DataFrame({"ID": ids, "n": 1.0, "d": d, "d2": d * d, "p": p, "o": ob})
        grouped = cell.groupby("ID", sort=True).sum()
        self.cell_frames.append(pd.DataFrame({
            "ID": grouped.index.to_numpy(np.int64), "n": grouped["n"].to_numpy(np.int64),
            "bias": (grouped["d"] / grouped["n"]).to_numpy(),
            "rmse": np.sqrt(grouped["d2"] / grouped["n"]).to_numpy(),
            "mean_timesfm": (grouped["p"] / grouped["n"]).to_numpy(),
            "mean_palacios": (grouped["o"] / grouped["n"]).to_numpy(),
        }))

        if tmin is not None:
            tm = tmin[["ID", "day", "TMIN"]].copy()
            tm["ID"], tm["day"] = tm["ID"].astype(np.int64), tm["day"].astype(np.int64)
            for name, frame, col in (("timesfm", t, "p"), ("palacios", o, "o")):
                x = frame.merge(tm, on=["ID", "day"], how="inner")
                x = x[np.isfinite(x[col])]
                diff = x[col].to_numpy() - x["TMIN"].to_numpy(np.float64)
                self.tmin[name] += np.array([diff.size, diff.sum(), float((diff > 0).sum())])

        if clim is not None:
            clim_ids, table = clim
            if set(np.asarray(clim_ids).tolist()) != set(np.unique(ids).tolist()):
                raise ValueError(f"bucket {bucket}: la climatologia no cubre las mismas celdas que el producto")
            self.clim_sum += np.asarray(table, dtype=np.float64).sum(axis=0)
            self.clim_cells += len(clim_ids)

    # ------------------------------------------------------------------ salidas
    def agreement_overall(self) -> dict[str, float]:
        return _finalize(self.groups["all"].get(0, np.zeros(len(_SUM_FIELDS))))

    def agreement_by(self, dim: str) -> pd.DataFrame:
        rows = [{"key": key, **_finalize(sums)} for key, sums in self.groups[dim].items()]
        frame = pd.DataFrame(rows, columns=["key", "n", "rmse", "mae", "bias", "r"])
        return frame.sort_values("key").reset_index(drop=True)

    def product_figures(self) -> pd.DataFrame:
        rows = []
        for name, p in self.product.items():
            row = {
                "product": name, "n": p.n, "cells": p.cells, "nan": p.nan, "inf": p.inf,
                "mean": p.total / p.n if p.n else np.nan,
                "min": p.min if p.n else np.nan, "max": p.max if p.n else np.nan,
                "rows_only_in_this_product": p.rows_only,
            }
            for k, year in enumerate(YEARS):
                row[f"mean_{year}"] = p.year_sum[k] / p.year_n[k] if p.year_n[k] else np.nan
            for k, year in enumerate(YEARS):
                # Convencion del paper: promedio sin ponderar de las 12 medias mensuales.
                with np.errstate(invalid="ignore", divide="ignore"):
                    monthly = p.month_sum[k] / p.month_n[k]
                row[f"mean_{year}_monthly"] = float(monthly.mean()) if (p.month_n[k] > 0).all() else np.nan
            rows.append(row)
        return pd.DataFrame(rows)

    def horizon_table(self) -> pd.DataFrame:
        n = np.where(self.day_n > 0, self.day_n, np.nan)
        return pd.DataFrame({
            "day": np.arange(HORIZON_DAYS), "date": DATES, "n": self.day_n.astype(np.int64),
            "bias": self.day_d / n, "rmse": np.sqrt(self.day_d2 / n),
            "mean_timesfm": self.day_p / n, "mean_palacios": self.day_o / n,
        })

    def horizon_drift(self) -> dict[str, float]:
        """Pendiente de la diferencia nacional diaria frente al dia de horizonte."""
        table = self.horizon_table()
        return trend(table["bias"].to_numpy(), per_year=365.25) | _first_last_year(table["bias"].to_numpy())

    def anomaly_series(self) -> pd.DataFrame:
        if self.clim_cells == 0:
            raise ValueError("no se acumulo climatologia (usa --with-climatology)")
        table = self.horizon_table()
        clim = self.clim_sum[DOY] / self.clim_cells
        if not np.isfinite(clim).all():
            raise ValueError("la climatologia tiene NaN en algun dia de año")
        table["doy"] = DOY
        table["clim_mean"] = clim
        table["anom_timesfm"] = table["mean_timesfm"] - clim
        table["anom_palacios"] = table["mean_palacios"] - clim
        return table

    def drift_by_product(self) -> pd.DataFrame:
        series = self.anomaly_series()
        rows = [{"series": f"anomalia_{name}", **trend(series[f"anom_{name}"].to_numpy(), per_year=365.25),
                 **_first_last_year(series[f"anom_{name}"].to_numpy())} for name in PRODUCTS]
        return pd.DataFrame(rows)

    def tmin_coherence(self) -> pd.DataFrame:
        rows = []
        for name, (n, total, above) in self.tmin.items():
            rows.append({"product": name, "n": int(n),
                         "mean_td_minus_tmin": total / n if n else np.nan,
                         "frac_td_gt_tmin": above / n if n else np.nan})
        return pd.DataFrame(rows)

    def per_cell(self) -> pd.DataFrame:
        if not self.cell_frames:
            return pd.DataFrame(columns=["ID", "n", "bias", "rmse", "mean_timesfm", "mean_palacios"])
        return pd.concat(self.cell_frames, ignore_index=True).sort_values("ID").reset_index(drop=True)


# ---------------------------------------------------------------------- tendencia

def trend(series: np.ndarray, *, per_year: float = 365.25, lag: int = 30) -> dict[str, float]:
    """Pendiente OLS por dia (y por año) con error estandar de Newey-West.

    La serie diaria esta muy autocorrelacionada: el error estandar clasico
    subestima la incertidumbre, por eso el intervalo usa el HAC (nucleo de
    Bartlett, ``lag`` dias). Se informa tambien el clasico para comparar.
    """
    y = np.asarray(series, dtype=np.float64)
    ok = np.isfinite(y)
    y, x = y[ok], np.arange(len(series), dtype=np.float64)[ok]
    n = y.size
    if n < 3:
        return {"slope_per_year": np.nan, "se_hac_per_year": np.nan, "se_ols_per_year": np.nan,
                "ci_low": np.nan, "ci_high": np.nan, "significant": False, "n_days": n}
    X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    xtx_inv = np.linalg.inv(X.T @ X)
    se_ols = np.sqrt(resid @ resid / (n - 2) * xtx_inv[1, 1])
    u = X * resid[:, None]
    s = u.T @ u
    for k in range(1, min(lag, n - 1) + 1):
        w = 1.0 - k / (lag + 1.0)
        gamma = u[k:].T @ u[:-k]
        s += w * (gamma + gamma.T)
    se_hac = np.sqrt((xtx_inv @ s @ xtx_inv)[1, 1])
    slope = beta[1] * per_year
    half = 1.96 * se_hac * per_year
    return {"slope_per_year": float(slope), "se_hac_per_year": float(se_hac * per_year),
            "se_ols_per_year": float(se_ols * per_year), "ci_low": float(slope - half),
            "ci_high": float(slope + half), "significant": bool(slope - half > 0 or slope + half < 0),
            "n_days": int(n)}


def _first_last_year(series: np.ndarray) -> dict[str, float]:
    s = np.asarray(series, dtype=np.float64)
    first, last = np.nanmean(s[YEAR == 2017]), np.nanmean(s[YEAR == 2020])
    return {"mean_first_year": float(first), "mean_last_year": float(last),
            "last_minus_first_year": float(last - first)}


# ---------------------------------------------------------------------- salida a disco

def write_outputs(acc: Accumulator, out_dir: Path, agg_dir: Path, *, full_panel: bool,
                  with_climatology: bool = False) -> list[Path]:
    out_dir, agg_dir = Path(out_dir), Path(agg_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    agg_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def save(frame: pd.DataFrame, directory: Path, name: str) -> None:
        path = directory / f"{name}{SUFFIX}.csv"
        frame.to_csv(path, index=False)
        written.append(path)

    figures = acc.product_figures()
    save(figures, out_dir, "product_figures")
    save(reproduction_control(paper_convention_figures(figures, "palacios"), full_panel=full_panel),
         out_dir, "reproduction_palacios")
    save(pd.DataFrame([acc.agreement_overall()]), out_dir, "agreement_overall")
    for dim in DIMENSIONS:
        save(acc.agreement_by(dim).rename(columns={"key": dim}), out_dir, f"agreement_by_{dim}")
    save(acc.horizon_table(), out_dir, "agreement_by_horizon_day")
    drift = pd.DataFrame([{"series": "diferencia_timesfm_menos_palacios", **acc.horizon_drift()}])
    if with_climatology:
        drift = pd.concat([drift, acc.drift_by_product()], ignore_index=True)
        save(acc.anomaly_series(), out_dir, "anomaly_series")
    save(drift, out_dir, "drift")
    save(acc.tmin_coherence(), out_dir, "tmin_coherence")
    save(acc.per_cell(), agg_dir, "agreement_by_cell")
    return written


def build_compare_provenance(*, n_cells: int, outputs: Sequence[Path], ids_file: Path | None,
                             bead_id: str, tfm_root: Path, palacios_root: Path) -> prov.MetricProvenance:
    spec = variant(VARIANT_KEY)
    return prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id=bead_id, manifest_ref=MANIFEST_REF_REAL, model_family=spec.family,
        model_id=spec.checkpoint, variant_label=spec.key, trained=False, training_period=None,
        validation_period=None, test_period=("2017-01-01", "2020-12-31"), split_id="real_2017_2020",
        autoregressive=False, target_type=spec.target_type, climatology_used=spec.climatology_used,
        climatology_role=spec.climatology_role, inputs=tuple(spec.inputs),
        panel_id=f"real_{n_cells}_td", panel_cell_count=int(n_cells),
        panel_file=str(ids_file) if ids_file else None,
        output_files=tuple(str(p) for p in outputs),
        notes=(f"Acuerdo TimesFM - Palacios (diferencia = TimesFM - Palacios), sin verdad observada: "
               f"sesgo, RMSE, MAE y r entre productos, no error. TimesFM leido de {tfm_root}, "
               f"Palacios de {palacios_root}. Pesos de TimesFM de uso no comercial."),
    )


# ---------------------------------------------------------------------- CLI

def _read_product(path: Path, columns: Sequence[str]) -> pd.DataFrame:
    # ParquetFile: read_table agregaria `id_bucket` por inferencia hive del directorio.
    return pq.ParquetFile(path).read(columns=list(columns)).to_pandas()


def _read_tmin(future_root: Path, bucket: int) -> pd.DataFrame:
    frames = []
    for year in YEARS:
        path = Path(future_root) / bucket_dir_name(bucket) / f"future_tmin_{year}.parquet"
        if path.exists():
            frames.append(pd.read_parquet(path, columns=["ID", "FECHA", "TMIN"]))
    frame = pd.concat(frames, ignore_index=True)
    frame["day"] = date_to_day(pd.to_datetime(frame["FECHA"]))
    return frame[["ID", "day", "TMIN"]]


def _site_series(silver: Path) -> pd.Series:
    sites = {"lima": "lima", "cusco": "cusco", "iquitos_loreto": "iquitos_loreto",
             "tarapoto_san_martin": "tarapoto_san_martin"}
    parts = []
    for name in sites:
        path = Path(silver) / f"{name}.csv"
        if path.exists():
            ids = pd.read_csv(path)["ID"].astype(np.int64).unique()
            parts.append(pd.Series(name, index=pd.Index(ids)))
    if not parts:
        logger.warning("sin tablas de departamento en %s: todo queda como 'otro'", silver)
        return pd.Series(dtype=object)
    return pd.concat(parts)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tfm-root", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--palacios-root", type=Path, default=DEFAULT_PALACIOS_ROOT)
    parser.add_argument("--future-root", type=Path, default=DEFAULT_FUTURE_ROOT)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--zone-table", type=Path, default=DEFAULT_ZONE)
    parser.add_argument("--support-distance", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--silver", type=Path, default=DEFAULT_SILVER)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--agg-dir", type=Path, default=DEFAULT_AGG)
    parser.add_argument("--buckets", default=None, help="'0,1' o '0-3'; por defecto, todos los de --tfm-root")
    parser.add_argument("--with-climatology", action="store_true",
                        help="lee 1981-2016 de cada bucket para la deriva de la anomalia de cada producto")
    parser.add_argument("--historical-workers", type=int, default=4)
    parser.add_argument("--no-tmin", action="store_true", help="omite la coherencia con Tmin")
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
    zone = pd.read_parquet(args.zone_table, columns=["ID", "zone_id"]).set_index("ID")["zone_id"]
    tier = pd.read_parquet(args.support_distance, columns=["ID", "tier"]).set_index("ID")["tier"]
    site = _site_series(args.silver)
    spec = variant(VARIANT_KEY)
    panel_spec = split_spec("real", context_start_year=spec.context_start_year)

    def load(bucket: int) -> dict:
        tfm = _read_product(args.tfm_root / bucket_dir_name(bucket) / PRED_NAME, ["ID", "day", "pred"])
        pal = _read_product(args.palacios_root / bucket_dir_name(bucket) / PRED_NAME,
                            ["ID", "FECHA", "TD_predicted"])
        out = {"tfm": tfm, "pal": pal, "tmin": None, "clim": None}
        if not args.no_tmin:
            out["tmin"] = _read_tmin(args.future_root, bucket)
        if args.with_climatology:
            panel = build_panel(np.unique(tfm["ID"].to_numpy(np.int64)), panel_spec,
                                historical_root=args.historical_root, bucket=bucket,
                                future_root=args.future_root)
            if panel is not None:
                out["clim"] = (panel.ids, panel.td_clim)
        return out

    acc = Accumulator()
    window = max(1, args.historical_workers) * 2
    with ThreadPoolExecutor(max_workers=max(1, args.historical_workers)) as pool:
        for start in range(0, len(buckets), window):
            chunk = buckets[start : start + window]
            for bucket, data in zip(chunk, pool.map(load, chunk)):
                meta = {"zone": zone, "tier": tier, "site": site}
                acc.add_bucket(bucket, data["tfm"], data["pal"], meta=meta,
                               tmin=data["tmin"], clim=data["clim"])
            logger.info("%d/%d buckets", min(start + window, len(buckets)), len(buckets))

    cells = acc.product["palacios"].cells
    full = len(buckets) == 8192 and cells == EXPECTED_CELLS
    written = write_outputs(acc, args.out_dir, args.agg_dir, full_panel=full,
                            with_climatology=args.with_climatology)
    record = build_compare_provenance(
        n_cells=acc.product["timesfm"].cells, outputs=written, ids_file=None, bead_id=args.bead_id,
        tfm_root=args.tfm_root, palacios_root=args.palacios_root,
    )
    if args.mlflow:
        import mlflow

        overall = acc.agreement_overall()
        figures = acc.product_figures().set_index("product")
        metrics = {f"agreement_{k}": v for k, v in overall.items()}
        for name in PRODUCTS:
            for col in ("n", "cells", "mean", "min", "max", "nan", "inf", "mean_2017", "mean_2018",
                        "mean_2019", "mean_2020", "rows_only_in_this_product"):
                metrics[f"{name}_{col}"] = float(figures.loc[name, col])
        drift = acc.horizon_drift()
        metrics.update({f"drift_{k}": float(v) for k, v in drift.items() if k != "significant"})
        metrics["drift_significant"] = float(drift["significant"])
        metrics["buckets"] = float(len(buckets))
        with et.start_run(
            args.run_name or f"timesfm-real-compare-{len(buckets)}buckets",
            params={"split": "real", "variant": VARIANT_KEY, "bead_id": args.bead_id,
                    "panel_id": record.panel_id, "trained": False, "full_panel": full,
                    "with_climatology": args.with_climatology, "tfm_root": str(args.tfm_root)},
            tracking_uri=args.mlflow_uri, experiment_name=args.mlflow_experiment,
        ) as run:
            mlflow.log_metrics({k: v for k, v in metrics.items() if np.isfinite(v)})
            record = dataclasses.replace(record, mlflow_run_id=run.info.run_id)
    prov.record_metric_provenance(record, registry_path=args.registry_path, repo_root=args.repo_root)
    print(acc.product_figures().to_string(index=False))
    print(pd.DataFrame([acc.agreement_overall()]).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
