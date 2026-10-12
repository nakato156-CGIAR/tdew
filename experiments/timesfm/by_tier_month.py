"""Desempeno por tier de soporte observacional (E5) y sesgo mensual (E8) de
TimesFM junto a los rivales de Palacios.

Solo computo sobre predicciones existentes: no corre inferencia y no escribe
bajo ``$RES``. Lee el merge intermedio de ``merge_predictions`` (columna
``pred_timesfm``) o, para el panel de cribado, une las predicciones de TimesFM
con el run limpio por ``(ID, FECHA)``. Los tiers vienen de
``support_distance.parquet`` (distancia al dominio SENAMHI), sin recalcular.

Convenciones: el mes es el de ``FECHA`` y el sesgo mensual es el promedio pooled
de ``pred - obs`` sobre todas las celdas-dia del mes. Las predicciones llegan en
float32; todo agregado se calcula en float64.
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
from pathlib import Path
from typing import Mapping, Sequence

import mlflow
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov

from . import paths
from .evaluate import CLEAN_BACKTEST_ROOT, MANIFEST_REF_LIMPIO, build_row_provenance

logger = logging.getLogger("timesfm.by_tier_month")

TIERS = ["within", "near", "marginal", "extrapolated", "unsupported"]
# metodo (nombre en los CSV) -> columna de predicciones
METHOD_COLS = {
    "timesfm": "pred_timesfm",
    "tuned": "pred_tuned",
    "climatology": "pred_clim",
    "tmin": "pred_tmin",
    "zone_ols": "pred_ols",
}
# nombre de metodo para la proveniencia (el de evaluate.RIVALS o timesfm:<variante>)
DEFAULT_VARIANT = "tmin_anom_full"
_PROVENANCE_NAMES = {
    "timesfm": f"timesfm:{DEFAULT_VARIANT}",
    "tuned": "tuned",
    "climatology": "climatology",
    "tmin": "td_eq_tmin",
    "zone_ols": "zone_ols",
}
REFERENCE_COLS = ["TD_obs", "pred_tuned", "pred_clim", "pred_tmin", "pred_ols"]
SKILL_REFERENCE = "climatology"

_RES = paths.RES
DEFAULT_SUPPORT = _RES / "tuning" / "support_distance.parquet"
DEFAULT_PAPER_CSV = Path(__file__).resolve().parents[2] / "reports/paper/scripts/validation_by_support.csv"

# Cifras del paper para el run limpio (control de reproduccion).
EXPECTED_CELLS = {
    "within": 8306, "near": 1779, "marginal": 1433, "extrapolated": 2563, "unsupported": 2946,
}
EXPECTED_DEC_BIAS = 0.017
EXPECTED_MAX_ABS_BIAS = 0.402
# Valores esperados de TimesFM (solo alerta, detectan un merge defectuoso).
EXPECTED_TIMESFM_RMSE = {
    "within": 0.867, "near": 1.061, "marginal": 1.198, "extrapolated": 1.298, "unsupported": 1.652,
}
EXPECTED_TIMESFM_BIAS = {
    1: -0.325, 2: 0.061, 3: 0.248, 4: 0.263, 5: 0.112, 6: 0.151,
    7: 0.210, 8: 0.255, 9: 0.193, 10: -0.098, 11: 0.100, 12: 0.089,
}
EXPECTED_NATIONAL_CELLS = 17027
# Reparto del panel de cribado limpio (1.092 celdas comunes con el run limpio).
EXPECTED_CRIBADO_CELLS = {
    "within": 842, "near": 79, "marginal": 59, "extrapolated": 65, "unsupported": 47,
}
EXPECTED_PEAK_MONTH = 1  # el maximo |sesgo| de tuned cae en enero
RMSE_TOL = 1e-6
BIAS_TOL = 5e-4
ALERT_TOL = 5e-4


class ReproductionError(RuntimeError):
    """El control de reproduccion contra las cifras del paper fallo."""


def method_provenance_name(method: str) -> str:
    return _PROVENANCE_NAMES[method]


# ------------------------------------------------------------------ carga

def _read_columns(path: Path, columns: Sequence[str]) -> pd.DataFrame:
    available = set(pq.read_schema(path).names)
    missing = [c for c in columns if c not in available]
    if missing:
        raise ValueError(f"{path}: faltan las columnas {missing}")
    return pd.read_parquet(path, columns=list(columns))


def _to_float64(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].astype("float64")
    return df


def _panel_ids(panel_file: Path) -> set[int]:
    return set(pd.read_csv(panel_file, usecols=["ID"])["ID"].astype("int64"))


def load_panel(
    split: str,
    *,
    backtest_root: Path = CLEAN_BACKTEST_ROOT,
    merged_root: Path | None = None,
    preds_dir: Path | None = None,
    panel_file: Path | None = None,
    variant: str = DEFAULT_VARIANT,
) -> pd.DataFrame:
    """Predicciones de todos los metodos para un split, en float64.

    Modo nacional (``merged_root``): ``pred_timesfm`` sale del merge intermedio.
    Modo cribado (``preds_dir``): se une ``pred`` de TimesFM al run limpio por
    ``(ID, FECHA)`` y se restringe a ``panel_file``.
    """
    base = ["ID", "FECHA"]
    pred_cols = REFERENCE_COLS
    if merged_root is not None:
        df = _read_columns(Path(merged_root) / split / "predictions.parquet",
                           base + pred_cols + ["pred_timesfm"])
    elif preds_dir is not None:
        ref = _read_columns(Path(backtest_root) / split / "predictions.parquet", base + pred_cols)
        tf = _read_columns(Path(preds_dir) / f"{split}__{variant}.parquet", base + ["pred"])
        tf = tf.rename(columns={"pred": "pred_timesfm"})
        ref["FECHA"] = pd.to_datetime(ref["FECHA"])
        tf["FECHA"] = pd.to_datetime(tf["FECHA"])
        cells_timesfm = tf["ID"].nunique()
        df = ref.merge(tf, on=base, how="inner", validate="one_to_one")
        logger.info("[%s] celdas TimesFM=%d, comunes con el run limpio=%d, pares descartados=%d",
                    split, cells_timesfm, df["ID"].nunique(), len(tf) - len(df))
    else:
        raise ValueError("load_panel requiere merged_root o preds_dir")
    df["FECHA"] = pd.to_datetime(df["FECHA"])
    if panel_file is not None:
        df = df[df["ID"].isin(_panel_ids(Path(panel_file)))].reset_index(drop=True)
    _to_float64(df, REFERENCE_COLS + ["pred_timesfm"])
    logger.info("[%s] %d celdas, %d pares (ID, FECHA)", split, df["ID"].nunique(), len(df))
    return df


def attach_tier(df: pd.DataFrame, support_path: Path) -> pd.DataFrame:
    support = pd.read_parquet(support_path, columns=["ID", "tier"])
    out = df.merge(support, on="ID", how="left", validate="many_to_one")
    missing = out.loc[out["tier"].isna(), "ID"].unique()
    if len(missing):
        raise ValueError(f"{len(missing)} celdas sin tier en {support_path} (p. ej. {missing[:5].tolist()})")
    unknown = set(out["tier"]) - set(TIERS)
    if unknown:
        raise ValueError(f"tiers desconocidos: {sorted(unknown)}")
    return out


# --------------------------------------------------------------- metricas

def score(pred: np.ndarray, obs: np.ndarray) -> dict:
    """RMSE, MAE, sesgo y r sobre los pares finitos (misma definicion que
    ``reports/paper/scripts/validation_by_support.score``, mas ``n``)."""
    pred = np.asarray(pred, dtype="float64")
    obs = np.asarray(obs, dtype="float64")
    e = pred - obs
    ok = np.isfinite(e) & np.isfinite(obs)
    e, p, o = e[ok], pred[ok], obs[ok]
    return {
        "n": int(ok.sum()),
        "rmse": float(np.sqrt((e ** 2).mean())),
        "mae": float(np.abs(e).mean()),
        "bias": float(e.mean()),
        "r": float(np.corrcoef(p, o)[0, 1]),
    }


def tier_table(df: pd.DataFrame, split: str) -> pd.DataFrame:
    """Una fila por (split, tier, metodo) con RMSE, MAE, sesgo, r y skill
    frente a climatologia (``1 - rmse / clim_rmse``)."""
    rows = []
    for tier in TIERS:
        sub = df[df["tier"] == tier]
        if sub.empty:
            continue
        obs = sub["TD_obs"].to_numpy(dtype="float64")
        scores = {m: score(sub[col].to_numpy(), obs) for m, col in METHOD_COLS.items()}
        ns = {s["n"] for s in scores.values()}
        if len(ns) > 1:
            logger.warning("[%s/%s] n distinto entre metodos: %s", split, tier, sorted(ns))
        clim_rmse = scores[SKILL_REFERENCE]["rmse"]
        cells = int(sub["ID"].nunique())
        for method, s in scores.items():
            rows.append({
                "split": split, "tier": tier, "method": method, "cells": cells, **s,
                "clim_rmse": clim_rmse, "skill": 1 - s["rmse"] / clim_rmse,
            })
    return pd.DataFrame(rows)


def _error_frame(df: pd.DataFrame) -> pd.DataFrame:
    obs = df["TD_obs"].to_numpy(dtype="float64")
    out = pd.DataFrame({"ID": df["ID"].to_numpy(), "month": df["FECHA"].dt.month.to_numpy()})
    if "tier" in df:
        out["tier"] = df["tier"].to_numpy()
    for method, col in METHOD_COLS.items():
        e = df[col].to_numpy(dtype="float64") - obs
        e[~np.isfinite(obs)] = np.nan
        out[method] = e
    return out


def monthly_bias(df: pd.DataFrame, split: str, *, dispersion: bool) -> pd.DataFrame:
    """Sesgo pooled por mes calendario de ``FECHA``, un renglon por
    (split, metodo, mes). Con ``dispersion`` anade la desviacion y los
    percentiles 5 y 95 del sesgo medio por (celda, mes)."""
    err = _error_frame(df)
    rows = []
    for method in METHOD_COLS:
        valid = err[["ID", "month", method]].dropna()
        pooled = valid.groupby("month")[method].agg(["mean", "size"])
        cells = valid.groupby("month")["ID"].nunique()
        if dispersion:
            per_cell = valid.groupby(["month", "ID"])[method].mean()
        for month, row in pooled.iterrows():
            rec = {
                "split": split, "method": method, "month": int(month),
                "bias_pooled": float(row["mean"]), "n": int(row["size"]),
                "cells": int(cells.loc[month]),
                "cell_bias_std": np.nan, "cell_bias_p05": np.nan, "cell_bias_p95": np.nan,
            }
            if dispersion:
                v = per_cell.loc[month].to_numpy(dtype="float64")
                rec["cell_bias_std"] = float(np.std(v))
                rec["cell_bias_p05"] = float(np.percentile(v, 5))
                rec["cell_bias_p95"] = float(np.percentile(v, 95))
            rows.append(rec)
    return pd.DataFrame(rows)


def monthly_bias_by_tier(df: pd.DataFrame, split: str) -> pd.DataFrame:
    """Sesgo pooled por (tier, metodo, mes)."""
    err = _error_frame(df)
    rows = []
    for tier in TIERS:
        sub = err[err["tier"] == tier]
        if sub.empty:
            continue
        for method in METHOD_COLS:
            valid = sub[["ID", "month", method]].dropna()
            agg = valid.groupby("month")[method].agg(["mean", "size"])
            cells = valid.groupby("month")["ID"].nunique()
            for month, row in agg.iterrows():
                rows.append({
                    "split": split, "tier": tier, "method": method, "month": int(month),
                    "bias": float(row["mean"]), "n": int(row["size"]),
                    "cells": int(cells.loc[month]),
                })
    return pd.DataFrame(rows)


# ----------------------------------------------------------- tabla reducida

REDUCED_METHODS = ("timesfm", "tuned", "climatology")
_REDUCED_METRICS = ("rmse", "mae", "bias", "r", "skill")


def reduced_table(tiers: pd.DataFrame) -> pd.DataFrame:
    """Una fila por tier con TimesFM, tuned y climatologia, en el orden de
    columnas de ``tbl-tiers`` (RMSE, MAE, sesgo, r, skill por metodo)."""
    rows = []
    for tier in TIERS:
        sub = tiers[tiers["tier"] == tier]
        if sub.empty:
            continue
        rec = {"tier": tier, "cells": int(sub["cells"].iloc[0])}
        for method in REDUCED_METHODS:
            row = sub[sub["method"] == method].iloc[0]
            for metric in _REDUCED_METRICS:
                rec[f"{method}_{metric}"] = float(row[metric])
        rows.append(rec)
    return pd.DataFrame(rows)


def reduced_markdown(reduced: pd.DataFrame) -> str:
    names = {"timesfm": "TimesFM", "tuned": "tuned", "climatology": "Climatología"}
    labels = {"rmse": "RMSE", "mae": "MAE", "bias": "Sesgo", "r": "r", "skill": "Skill"}
    header = ["Tier", "Celdas"] + [f"{names[m]} {labels[k]}" for m in REDUCED_METHODS for k in _REDUCED_METRICS]
    lines = ["| " + " | ".join(header) + " |",
             "|:---|---:|" + "---:|" * (len(header) - 2)]
    for _, r in reduced.iterrows():
        cells = [r["tier"], f"{int(r['cells']):,}"]
        for m in REDUCED_METHODS:
            for k in _REDUCED_METRICS:
                value = r[f"{m}_{k}"]
                cells.append(f"{value:+.3f}" if k == "bias" else f"{value:.3f}")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


# --------------------------------------------------- control de reproduccion

def _off(value: float, expected: float, tol: float) -> bool:
    """True si ``value`` no esta a ``tol`` de ``expected``; un NaN siempre falla."""
    return not (abs(value - expected) <= tol)


def reproduction_check(
    tiers: pd.DataFrame,
    *,
    paper_csv: Path = DEFAULT_PAPER_CSV,
    expected_cells: Mapping[str, int] = EXPECTED_CELLS,
    monthly: pd.DataFrame | None = None,
    expected_dec_bias: float = EXPECTED_DEC_BIAS,
    expected_max_abs_bias: float = EXPECTED_MAX_ABS_BIAS,
    expected_peak_month: int = EXPECTED_PEAK_MONTH,
) -> None:
    """Compara el ``tuned`` ll4 con las cifras del paper. Lanza
    ``ReproductionError`` si no coincide: celdas por tier (exacto), RMSE por
    tier contra ``validation_by_support.csv`` (1e-6) y, si se da ``monthly``,
    el sesgo de diciembre, el maximo |sesgo| y el mes en que ocurre (5e-4).
    Un valor NaN nunca pasa el control."""
    problems: list[str] = []
    tuned = tiers[(tiers["split"] == "ll4") & (tiers["method"] == "tuned")].set_index("tier")
    for tier, expected in expected_cells.items():
        got = int(tuned["cells"].get(tier, -1))
        if got != expected:
            problems.append(f"celdas {tier}: {got} != {expected}")
    paper = pd.read_csv(paper_csv)
    paper = paper[paper["split"] == "ll4"].set_index("tier")
    for tier in tuned.index:
        ours = float(tuned.loc[tier, "rmse"])
        theirs = float(paper.loc[tier, "tuned_rmse"])
        if _off(ours, theirs, RMSE_TOL):
            problems.append(f"RMSE tuned {tier}: {ours:.8f} vs {theirs:.8f} (tol {RMSE_TOL:.0e})")
    if monthly is not None:
        m = monthly[(monthly["split"] == "ll4") & (monthly["method"] == "tuned")].set_index("month")
        dec = float(m.loc[12, "bias_pooled"])
        if _off(dec, expected_dec_bias, BIAS_TOL):
            problems.append(f"sesgo diciembre tuned: {dec:+.4f} != {expected_dec_bias:+.3f}")
        absolute = m["bias_pooled"].abs()
        if absolute.isna().any():
            problems.append("sesgo mensual tuned con NaN")
        else:
            peak_month = int(absolute.idxmax())
            if peak_month != expected_peak_month:
                problems.append(
                    f"el maximo |sesgo| de tuned cae en el mes {peak_month}, no en enero "
                    f"(mes {expected_peak_month})")
            peak = float(absolute.max())
            if _off(peak, expected_max_abs_bias, BIAS_TOL):
                problems.append(f"sesgo maximo |tuned|: {peak:.4f} != {expected_max_abs_bias:.3f}")
    if problems:
        raise ReproductionError("; ".join(problems))


def panel_check(
    tiers: pd.DataFrame,
    *,
    expected_total: int,
    expected_by_tier: Mapping[str, int],
) -> None:
    """Cada split puntua exactamente el panel esperado: total de celdas y
    reparto por tier. Lanza ``ReproductionError`` si no coincide."""
    problems: list[str] = []
    tuned = tiers[tiers["method"] == "tuned"]
    for split, group in tuned.groupby("split"):
        by_tier = group.set_index("tier")["cells"]
        total = int(by_tier.sum())
        if total != expected_total:
            problems.append(f"{split}: {total} celdas != {expected_total}")
        for tier, expected in expected_by_tier.items():
            got = int(by_tier.get(tier, 0))
            if got != expected:
                problems.append(f"{split} {tier}: {got} celdas != {expected}")
    if problems:
        raise ReproductionError("; ".join(problems))


def timesfm_alerts(tiers: pd.DataFrame, monthly: pd.DataFrame | None = None) -> list[str]:
    """Diferencias de TimesFM ll4 frente a los valores esperados (> 5e-4).
    Son una alerta para detectar un merge defectuoso, no un error."""
    alerts = []
    t = tiers[(tiers["split"] == "ll4") & (tiers["method"] == "timesfm")].set_index("tier")
    for tier, expected in EXPECTED_TIMESFM_RMSE.items():
        if tier in t.index and _off(float(t.loc[tier, "rmse"]), expected, ALERT_TOL):
            alerts.append(f"RMSE timesfm {tier}: {float(t.loc[tier, 'rmse']):.4f} vs {expected:.3f}")
    if monthly is not None:
        m = monthly[(monthly["split"] == "ll4") & (monthly["method"] == "timesfm")].set_index("month")
        for month, expected in EXPECTED_TIMESFM_BIAS.items():
            if month in m.index and _off(float(m.loc[month, "bias_pooled"]), expected, ALERT_TOL):
                alerts.append(f"sesgo timesfm mes {month}: {float(m.loc[month, 'bias_pooled']):+.4f} vs {expected:+.3f}")
    return alerts


# -------------------------------------------------------------- proveniencia

def build_provenance(
    method: str,
    *,
    split: str,
    cells: int,
    bead_id: str,
    panel_id: str,
    panel_file: str,
    output_files: tuple[str, ...],
    notes: str | None = None,
) -> prov.MetricProvenance:
    return build_row_provenance(
        method_provenance_name(method),
        split=split,
        cells=cells,
        bead_id=bead_id,
        panel_id=panel_id,
        panel_file=panel_file,
        output_files=output_files,
        notes=notes,
        manifest_ref=MANIFEST_REF_LIMPIO,
    )


def provenance_targets(
    splits: Sequence[str], files: Mapping[str, str],
) -> list[tuple[str, str, tuple[str, ...]]]:
    """(split, metodo, output_files) de cada registro. Cada registro lista solo
    los CSV que contienen ese split y metodo: ``files["texto"]`` (tabla reducida)
    solo para ll4 y TimesFM, tuned y climatologia. TimesFM/ll4 va al final: los
    sidecars guardan el ultimo registro y asi describen el metodo principal."""
    core = tuple(files[k] for k in ("tiers", "mensual", "mes_tier"))
    targets = []
    for split in splits:
        for method in METHOD_COLS:
            extra = ()
            if "texto" in files and split == "ll4" and method in REDUCED_METHODS:
                extra = (files["texto"],)
            targets.append((split, method, core + extra))
    targets.sort(key=lambda t: (t[0], t[1]) == ("ll4", "timesfm"))
    return targets


# ------------------------------------------------------------------ MLflow

MLFLOW_EXPERIMENT = "tdew-timesfm-benchmark"
_TIER_METRICS = ("rmse", "mae", "bias", "r", "skill")


def _overall(tiers: pd.DataFrame, method: str) -> dict[str, float]:
    """RMSE, sesgo y skill sobre todos los tiers, ponderando por ``n``."""
    sub = tiers[tiers["method"] == method]
    n = sub["n"].to_numpy(dtype="float64")
    rmse = float(np.sqrt((n * sub["rmse"].to_numpy() ** 2).sum() / n.sum()))
    bias = float((n * sub["bias"].to_numpy()).sum() / n.sum())
    clim = tiers[tiers["method"] == SKILL_REFERENCE]
    nc = clim["n"].to_numpy(dtype="float64")
    clim_rmse = float(np.sqrt((nc * clim["rmse"].to_numpy() ** 2).sum() / nc.sum()))
    return {"rmse_all": rmse, "bias_all": bias, "skill_all": 1 - rmse / clim_rmse}


def log_mlflow(
    tiers: pd.DataFrame,
    monthly: pd.DataFrame,
    *,
    splits: Sequence[str],
    panel_id: str,
    bead_id: str,
    tracking_uri: str = et.DEFAULT_TRACKING_URI,
    experiment_name: str = MLFLOW_EXPERIMENT,
) -> dict[str, str]:
    """Una corrida de evaluacion de MLflow por split, con las metricas de E5 y
    E8 de todos los metodos. Devuelve ``{split: run_id}``. TimesFM no se entrena:
    la corrida registra una evaluacion, no un entrenamiento."""
    run_ids: dict[str, str] = {}
    for split in splits:
        metrics: dict[str, float] = {}
        t = tiers[tiers["split"] == split]
        for method in METHOD_COLS:
            for _, row in t[t["method"] == method].iterrows():
                for metric in _TIER_METRICS:
                    metrics[f"{method}_{row['tier']}_{metric}"] = float(row[metric])
            metrics.update({f"{method}_{k}": v for k, v in _overall(t, method).items()})
        m = monthly[monthly["split"] == split]
        for _, row in m.iterrows():
            metrics[f"{row['method']}_bias_m{int(row['month']):02d}"] = float(row["bias_pooled"])
            if pd.notna(row["cell_bias_std"]):
                metrics[f"{row['method']}_cell_bias_std_m{int(row['month']):02d}"] = float(row["cell_bias_std"])
        with et.start_run(
            f"timesfm-tier-month-{split}",
            dataset_version=panel_id,
            params={
                "split": split, "panel_id": panel_id, "bead_id": bead_id,
                "variant": DEFAULT_VARIANT, "methods": ",".join(METHOD_COLS),
                "trained": False, "aggregation": "pooled, float64, mes por FECHA",
            },
            tracking_uri=tracking_uri,
            experiment_name=experiment_name,
        ) as run:
            mlflow.log_metrics(metrics)
            run_ids[split] = run.info.run_id
    return run_ids


# ---------------------------------------------------------------------- CLI

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--merged-root", type=Path, default=None,
                        help="merge intermedio con pred_timesfm (modo nacional)")
    parser.add_argument("--preds-dir", type=Path, default=None,
                        help="parquet de TimesFM <split>__<variante>.parquet (modo cribado)")
    parser.add_argument("--variant", default=DEFAULT_VARIANT)
    parser.add_argument("--panel-file", type=Path, default=None)
    parser.add_argument("--splits", default="ll1,ll2,ll4")
    parser.add_argument("--backtest-root", type=Path, default=CLEAN_BACKTEST_ROOT)
    parser.add_argument("--support-distance", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--paper-csv", type=Path, default=DEFAULT_PAPER_CSV)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--panel-id", required=True)
    parser.add_argument("--bead-id", default="tdew-0bt")
    parser.add_argument("--suffix", default="_limpio")
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    parser.add_argument("--mlflow", action="store_true",
                        help="registra una corrida de evaluacion de MLflow por split")
    parser.add_argument("--mlflow-uri", default=et.DEFAULT_TRACKING_URI)
    parser.add_argument("--mlflow-experiment", default=MLFLOW_EXPERIMENT)
    args = parser.parse_args(argv)
    if (args.merged_root is None) == (args.preds_dir is None):
        parser.error("indicar exactamente uno de --merged-root o --preds-dir")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    nacional = args.merged_root is not None
    stem = "" if nacional else "_cribado"
    args.out_dir = args.out_dir.resolve()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]

    tiers, monthly, by_tier, cells_by_split = [], [], [], {}
    for split in splits:
        df = load_panel(split, backtest_root=args.backtest_root, merged_root=args.merged_root,
                        preds_dir=args.preds_dir, panel_file=args.panel_file, variant=args.variant)
        df = attach_tier(df, args.support_distance)
        cells_by_split[split] = int(df["ID"].nunique())
        tiers.append(tier_table(df, split))
        monthly.append(monthly_bias(df, split, dispersion=(split == "ll4")))
        by_tier.append(monthly_bias_by_tier(df, split))
        del df
    tiers_df = pd.concat(tiers, ignore_index=True)
    monthly_df = pd.concat(monthly, ignore_index=True)
    by_tier_df = pd.concat(by_tier, ignore_index=True)

    try:
        panel_check(
            tiers_df,
            expected_total=EXPECTED_NATIONAL_CELLS if nacional else sum(EXPECTED_CRIBADO_CELLS.values()),
            expected_by_tier=EXPECTED_CELLS if nacional else EXPECTED_CRIBADO_CELLS,
        )
        if nacional and "ll4" in splits:
            reproduction_check(
                tiers_df, paper_csv=args.paper_csv, expected_cells=EXPECTED_CELLS,
                monthly=monthly_df, expected_dec_bias=EXPECTED_DEC_BIAS,
                expected_max_abs_bias=EXPECTED_MAX_ABS_BIAS,
                expected_peak_month=EXPECTED_PEAK_MONTH,
            )
    except ReproductionError as exc:
        logger.error("ERROR control de reproduccion: %s", exc)
        return 1
    logger.info("control de reproduccion: OK")
    if nacional and "ll4" in splits:
        for alert in timesfm_alerts(tiers_df, monthly_df):
            logger.warning("ALERTA %s", alert)

    sfx = args.suffix
    outputs = {
        "tiers": args.out_dir / f"tiers{stem}{sfx}.csv",
        "mensual": args.out_dir / f"sesgo_mensual{stem}{sfx}.csv",
        "mes_tier": args.out_dir / f"sesgo_mes_tier{stem}{sfx}.csv",
    }
    tiers_df.to_csv(outputs["tiers"], index=False)
    monthly_df.to_csv(outputs["mensual"], index=False)
    by_tier_df.to_csv(outputs["mes_tier"], index=False)
    if nacional and "ll4" in splits:
        reduced = reduced_table(tiers_df[tiers_df["split"] == "ll4"])
        outputs["texto"] = args.out_dir / f"tiers_texto{sfx}.csv"
        reduced.to_csv(outputs["texto"], index=False)
        (args.out_dir / f"tiers_texto{sfx}.md").write_text(reduced_markdown(reduced), encoding="utf-8")
        print(reduced_markdown(reduced))

    panel_file = str(args.panel_file) if args.panel_file else str(args.merged_root or args.preds_dir)
    files = {k: str(v) for k, v in outputs.items()}
    if nacional:
        source = (f"merged_root={Path(args.merged_root).resolve()} (columnas de referencia "
                  "del run limpio incluidas en el merge)")
    else:
        source = f"backtest_root={Path(args.backtest_root).resolve()}"
    run_ids: dict[str, str] = {}
    if args.mlflow:
        run_ids = log_mlflow(
            tiers_df, monthly_df, splits=splits, panel_id=args.panel_id, bead_id=args.bead_id,
            tracking_uri=args.mlflow_uri, experiment_name=args.mlflow_experiment,
        )
        logger.info("MLflow: %s", run_ids)
    for split, method, output_files in provenance_targets(splits, files):
        notes = (
            f"{source}; selección solo con años de "
            f"entrenamiento; cells={cells_by_split[split]}; predicciones float32 "
            "agregadas en float64; mes por FECHA, sesgo pooled; E5/E8 solo cómputo "
            "sobre predicciones existentes"
        )
        record = build_provenance(
            method, split=split, cells=cells_by_split[split], bead_id=args.bead_id,
            panel_id=args.panel_id, panel_file=panel_file, output_files=output_files,
            notes=notes,
        )
        if split in run_ids:
            record = dataclasses.replace(record, mlflow_run_id=run_ids[split])
        prov.record_metric_provenance(record, registry_path=args.registry_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
