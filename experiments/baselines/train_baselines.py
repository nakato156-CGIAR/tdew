#!/usr/bin/env python3
"""
experiments.baselines.train_baselines

tdew-x46 baseline "leaderboard": climatology, persistence, dept_ols, dept_mlr,
generalist_mlr — fit and scored under the frozen Week-1 protocol
(``docs/protocol/week1_manifest.yaml``: train 2002-2012 / validation 2013-2014
/ test 2015-2016, target ``Td(t+1)`` from ``X_{<=t}``, no input from ``t+1``
or later). See the tdew-x46 plan for the full design rationale.

Reads ``Data/gold/baseline_dataset`` (``pipeline.baseline_features``), which
is already leak-safe and eligibility-filtered. Everything here is bucket-
streamed (never concatenates a whole department into one DataFrame) because
the 4 protocol departments together are ~436k cells x ~13 years (~62GB in
``model_features_norm`` alone) — the same "accumulate across id_bucket shards"
philosophy as ``pipeline.gold``/``pipeline.normalize``/
``tdew_estimation.climatology``.

Methods
-------
- ``climatology``  — pred = TD_clim_target. No fit.
- ``persistence``  — pred = TD_anom_lag1 + TD_clim_target (persistence of
  *yesterday's anomaly*, not of the raw value or the climatology). No fit.
- ``dept_ols``     — one univariate OLS per department: TD_anom_target ~ a +
  b * TMIN_anom_lag0 (analogous to the existing ``zone_ols`` baseline in
  ``HPC_code_tunning/backtest.py``, but per protocol department instead of
  SENAMHI zone, and using TMIN lagged to ``t`` per this protocol's leakage
  rule instead of same-day TMIN).
- ``dept_mlr``     — the bead's required non-deep baseline: one multivariate
  (ridge-regularized normal equations) regression per department over the
  full lag + static feature set.
- ``generalist_mlr`` — a single model fit across all 4 departments at once,
  with natural-region (Costa/Sierra/Selva) dummies interacted with every lag
  feature (so persistence/autocorrelation dynamics can differ by region —
  the cheap linear analogue of a learned "topographical embedding", per the
  research summarized in the tdew-x46 plan), and per-row weights inversely
  proportional to each site's train-row count so Loreto (~305k cells) cannot
  dominate the fit over Lima (~29k cells) 7:1.

Output
------
``reports/week1_baselines/leaderboard.csv`` — rows per (site, method, split)
plus a pooled ``site="ALL"`` row per (method, split). Every (site, method) is
also logged as an MLflow run (see ``tdew_estimation.experiment_tracking``).

Usage
-----
uv run python -m experiments.baselines.train_baselines
uv run python -m experiments.baselines.train_baselines --max-buckets 2  # smoke test
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import mlflow
import numpy as np
import pandas as pd

from pipeline.qc import SITES, load_site_ids
from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.bucket_layout import discover_bucket_ids
from tdew_estimation.metrics import MetricsAccum, NormalEquationsAccum, OLSAccum

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"
DEFAULT_OUT = REPO_ROOT / "reports" / "week1_baselines" / "leaderboard.csv"
BASELINE_DATASET_VERSION = "Data/gold/baseline_dataset"

# docs/protocol/week1_manifest.yaml, frozen_on 2026-09-15: period.splits + target.
MANIFEST_REF = "docs/protocol/week1_manifest.yaml@2026-09-15"
TRAIN_PERIOD = ("2002-01-01", "2012-12-31")
VALIDATION_PERIOD = ("2013-01-01", "2014-12-31")
TEST_PERIOD = ("2015-01-01", "2016-12-31")

# docs/protocol/week1_manifest.yaml sites.departments[].region_natural
REGION_NATURAL: Dict[str, str] = {
    "lima": "Costa",
    "cusco": "Sierra",
    "iquitos_loreto": "Selva",
    "tarapoto_san_martin": "Selva",
}

LAG_FEATURES = [
    "TMIN_anom_lag0",
    "TMIN_anom_lag1",
    "TD_anom_lag1",
    "TD_anom_lag2",
    "TD_anom_lag3",
    "TD_anom_lag7",
    "TD_anom_lag30",
]
STATIC_FEATURES = ["sin_doy_target", "cos_doy_target", "DEM", "TDI", "X", "Y", "LST_DAY_target", "LST_NIGHT_target"]
DEPT_FEATURES = ["const"] + LAG_FEATURES + STATIC_FEATURES
GENERALIST_FEATURES = (
    DEPT_FEATURES
    + ["region_Sierra", "region_Selva"]
    + [f"{c}_x_Sierra" for c in LAG_FEATURES]
    + [f"{c}_x_Selva" for c in LAG_FEATURES]
)
REQUIRED_COLS = LAG_FEATURES + STATIC_FEATURES + ["TD_anom_target", "TD_target", "TD_clim_target"]

# Every method here predicts TD_anom_target and adds TD_clim_target back
# (see predict_all_methods), except climatology, which IS TD_clim_target.
METHOD_PROVENANCE: Dict[str, Dict[str, object]] = {
    "climatology": dict(
        trained=True, autoregressive=False, target_type="td_raw",
        climatology_used=True, climatology_role="is_the_method", inputs=("ID", "doy"),
    ),
    "persistence": dict(
        trained=False, autoregressive=False, target_type="td_anomaly",
        climatology_used=True, climatology_role="target_anomaly_base",
        inputs=("TD_anom_lag1",),
    ),
    "dept_ols": dict(
        trained=True, autoregressive=False, target_type="td_anomaly",
        climatology_used=True, climatology_role="target_anomaly_base",
        inputs=("const", "TMIN_anom_lag0"),
    ),
    "dept_mlr": dict(
        trained=True, autoregressive=False, target_type="td_anomaly",
        climatology_used=True, climatology_role="target_anomaly_base",
        inputs=tuple(DEPT_FEATURES),
    ),
    "generalist_mlr": dict(
        trained=True, autoregressive=False, target_type="td_anomaly",
        climatology_used=True, climatology_role="target_anomaly_base",
        inputs=tuple(GENERALIST_FEATURES),
    ),
}


def build_method_provenance(
    site: str, method: str, *, cells: int, bead_id: str, output_files: Tuple[str, ...],
) -> prov.MetricProvenance:
    """One record per (site, method): both validation and test rows for that
    pair share the same fitted coefficients, so they share one provenance
    record rather than duplicating it per split."""
    meta = METHOD_PROVENANCE[method]
    panel_file = None if site == "ALL" else f"Data/silver/department_grid_ids/{site}.csv"
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=MANIFEST_REF,
        model_family="week1_baseline",
        model_id=method,
        variant_label=f"{method}@{site}",
        trained=meta["trained"],
        training_period=TRAIN_PERIOD if meta["trained"] else None,
        validation_period=VALIDATION_PERIOD,
        test_period=TEST_PERIOD,
        split_id="validation+test",
        autoregressive=meta["autoregressive"],
        target_type=meta["target_type"],
        climatology_used=meta["climatology_used"],
        climatology_role=meta["climatology_role"],
        inputs=meta["inputs"],
        panel_id=site,
        panel_cell_count=cells,
        panel_file=panel_file,
        output_files=output_files,
    )


def _bucket_path(root: Path, bucket_id: int) -> Path:
    return root / f"id_bucket={bucket_id}" / "part.parquet"


def iter_site_buckets(
    baseline_dir: Path, site_ids: pd.Index, *, max_buckets: Optional[int] = None
) -> Iterator[pd.DataFrame]:
    """Yield each id_bucket's rows restricted to ``site_ids`` and to rows with
    every required feature/target column finite (dropna once, upfront)."""
    bucket_ids = discover_bucket_ids(baseline_dir)
    if max_buckets is not None:
        bucket_ids = bucket_ids[:max_buckets]
    for bucket_id in bucket_ids:
        path = _bucket_path(baseline_dir, bucket_id)
        if not path.exists():
            continue
        df = pd.read_parquet(path)
        df = df[df["ID"].isin(site_ids)]
        if df.empty:
            continue
        df = df.dropna(subset=[c for c in REQUIRED_COLS if c in df.columns])
        if not df.empty:
            yield df


def dept_design_matrix(df: pd.DataFrame) -> np.ndarray:
    cols = [np.ones(len(df))] + [df[c].to_numpy(dtype=float) for c in LAG_FEATURES + STATIC_FEATURES]
    return np.column_stack(cols)


def generalist_design_matrix(df: pd.DataFrame, region: str) -> np.ndarray:
    n = len(df)
    is_sierra = 1.0 if region == "Sierra" else 0.0
    is_selva = 1.0 if region == "Selva" else 0.0
    base_vals = {c: df[c].to_numpy(dtype=float) for c in LAG_FEATURES + STATIC_FEATURES}
    cols = [np.ones(n)]
    cols += [base_vals[c] for c in LAG_FEATURES + STATIC_FEATURES]
    cols += [np.full(n, is_sierra), np.full(n, is_selva)]
    cols += [base_vals[c] * is_sierra for c in LAG_FEATURES]
    cols += [base_vals[c] * is_selva for c in LAG_FEATURES]
    return np.column_stack(cols)


def predict_from_coefs(X: np.ndarray, coefs: Dict[str, float], feature_names: List[str]) -> np.ndarray:
    beta = np.array([coefs[name] for name in feature_names])
    return X @ beta


def count_train_rows(baseline_dir: Path, site_ids: pd.Index, *, max_buckets: Optional[int]) -> int:
    n = 0
    for df in iter_site_buckets(baseline_dir, site_ids, max_buckets=max_buckets):
        n += int((df["split"] == "train").sum())
    return n


def fit_dept_methods(
    baseline_dir: Path, site_ids: pd.Index, *, max_buckets: Optional[int]
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """One streaming pass over a site's train rows: fits dept_ols + dept_mlr."""
    ols = OLSAccum()
    mlr = NormalEquationsAccum(DEPT_FEATURES)
    for df in iter_site_buckets(baseline_dir, site_ids, max_buckets=max_buckets):
        train = df[df["split"] == "train"]
        if train.empty:
            continue
        ols.add(train["TMIN_anom_lag0"].to_numpy(dtype=float), train["TD_anom_target"].to_numpy(dtype=float))
        mlr.add(dept_design_matrix(train), train["TD_anom_target"].to_numpy(dtype=float))
    a, b = ols.fit()
    return {"const": a, "TMIN_anom_lag0": b}, mlr.fit()


def fit_generalist(
    baseline_dir: Path, site_ids_by_site: Dict[str, pd.Index], site_weights: Dict[str, float], *, max_buckets: Optional[int]
) -> Dict[str, float]:
    acc = NormalEquationsAccum(GENERALIST_FEATURES)
    for site, site_ids in site_ids_by_site.items():
        region = REGION_NATURAL[site]
        w_site = site_weights[site]
        for df in iter_site_buckets(baseline_dir, site_ids, max_buckets=max_buckets):
            train = df[df["split"] == "train"]
            if train.empty:
                continue
            X = generalist_design_matrix(train, region)
            y = train["TD_anom_target"].to_numpy(dtype=float)
            w = np.full(len(train), w_site)
            acc.add(X, y, w)
    return acc.fit()


def predict_all_methods(
    df: pd.DataFrame,
    *,
    region: str,
    ols_coefs: Dict[str, float],
    mlr_coefs: Dict[str, float],
    generalist_coefs: Dict[str, float],
) -> Dict[str, np.ndarray]:
    clim = df["TD_clim_target"].to_numpy(dtype=float)
    ols_X = np.column_stack([np.ones(len(df)), df["TMIN_anom_lag0"].to_numpy(dtype=float)])
    return {
        "climatology": clim,
        "persistence": df["TD_anom_lag1"].to_numpy(dtype=float) + clim,
        "dept_ols": predict_from_coefs(ols_X, ols_coefs, ["const", "TMIN_anom_lag0"]) + clim,
        "dept_mlr": predict_from_coefs(dept_design_matrix(df), mlr_coefs, DEPT_FEATURES) + clim,
        "generalist_mlr": predict_from_coefs(generalist_design_matrix(df, region), generalist_coefs, GENERALIST_FEATURES)
        + clim,
    }


def score_site(
    baseline_dir: Path,
    site: str,
    site_ids: pd.Index,
    *,
    ols_coefs: Dict[str, float],
    mlr_coefs: Dict[str, float],
    generalist_coefs: Dict[str, float],
    pooled: Dict[Tuple[str, str], MetricsAccum],
    max_buckets: Optional[int],
) -> pd.DataFrame:
    region = REGION_NATURAL[site]
    methods = ["climatology", "persistence", "dept_ols", "dept_mlr", "generalist_mlr"]
    accs: Dict[Tuple[str, str], MetricsAccum] = {(split, m): MetricsAccum() for split in ("validation", "test") for m in methods}

    for df in iter_site_buckets(baseline_dir, site_ids, max_buckets=max_buckets):
        for split in ("validation", "test"):
            sdf = df[df["split"] == split]
            if sdf.empty:
                continue
            obs = sdf["TD_target"].to_numpy(dtype=float)
            preds = predict_all_methods(
                sdf, region=region, ols_coefs=ols_coefs, mlr_coefs=mlr_coefs, generalist_coefs=generalist_coefs
            )
            for method, pred in preds.items():
                accs[(split, method)].add(pred, obs)
                pooled[(split, method)].add(pred, obs)

    clim_rmse = {split: accs[(split, "climatology")].finalize()["rmse"] for split in ("validation", "test")}
    rows = []
    for (split, method), acc in accs.items():
        m = acc.finalize()
        m["skill_vs_clim"] = (1.0 - m["rmse"] / clim_rmse[split]) if clim_rmse[split] else np.nan
        m["site"] = site
        m["method"] = method
        m["split"] = split
        rows.append(m)
    return pd.DataFrame(rows)


def pooled_rows(pooled: Dict[Tuple[str, str], MetricsAccum]) -> pd.DataFrame:
    clim_rmse = {split: pooled[(split, "climatology")].finalize()["rmse"] for split in ("validation", "test")}
    rows = []
    for (split, method), acc in pooled.items():
        m = acc.finalize()
        m["skill_vs_clim"] = (1.0 - m["rmse"] / clim_rmse[split]) if clim_rmse[split] else np.nan
        m["site"] = "ALL"
        m["method"] = method
        m["split"] = split
        rows.append(m)
    return pd.DataFrame(rows)


def log_mlflow_run(site: str, method: str, metrics_df: pd.DataFrame) -> None:
    sub = metrics_df[(metrics_df["site"] == site) & (metrics_df["method"] == method)]
    with et.start_run(
        "week1-baseline",
        seed=0,
        dataset_version=BASELINE_DATASET_VERSION,
        site=site,
        params={"method": method},
    ):
        for _, row in sub.iterrows():
            prefix = row["split"]
            for k in ("n", "rmse", "mae", "bias", "r", "skill_vs_clim"):
                if pd.notna(row[k]):
                    mlflow.log_metric(f"{prefix}_{k}", float(row[k]))


def run(
    *, gold_dir: Path, silver_dir: Path, out_path: Path, max_buckets: Optional[int],
    bead_id: str = "tdew-x46",
) -> pd.DataFrame:
    baseline_dir = gold_dir / "baseline_dataset"
    if not baseline_dir.exists():
        raise FileNotFoundError(f"{baseline_dir} not found — run pipeline.baseline_features first")

    site_ids_by_site = {site: load_site_ids(silver_dir, site) for site in SITES}

    print("[train_baselines] counting train rows per site (for generalist_mlr weights)...")
    train_counts = {
        site: count_train_rows(baseline_dir, ids, max_buckets=max_buckets) for site, ids in site_ids_by_site.items()
    }
    print(f"[train_baselines] train rows per site: {train_counts}")
    site_weights = {site: (1.0 / n if n else 0.0) for site, n in train_counts.items()}

    print("[train_baselines] fitting dept_ols/dept_mlr per site...")
    dept_coefs = {
        site: fit_dept_methods(baseline_dir, ids, max_buckets=max_buckets) for site, ids in site_ids_by_site.items()
    }

    print("[train_baselines] fitting generalist_mlr across all sites...")
    generalist_coefs = fit_generalist(baseline_dir, site_ids_by_site, site_weights, max_buckets=max_buckets)

    pooled: Dict[Tuple[str, str], MetricsAccum] = {
        (split, m): MetricsAccum()
        for split in ("validation", "test")
        for m in ("climatology", "persistence", "dept_ols", "dept_mlr", "generalist_mlr")
    }

    print("[train_baselines] scoring validation/test per site...")
    per_site_frames = []
    for site, site_ids in site_ids_by_site.items():
        ols_coefs, mlr_coefs = dept_coefs[site]
        frame = score_site(
            baseline_dir,
            site,
            site_ids,
            ols_coefs=ols_coefs,
            mlr_coefs=mlr_coefs,
            generalist_coefs=generalist_coefs,
            pooled=pooled,
            max_buckets=max_buckets,
        )
        per_site_frames.append(frame)

    leaderboard = pd.concat(per_site_frames + [pooled_rows(pooled)], ignore_index=True)
    cols = ["site", "method", "split", "n", "rmse", "mae", "bias", "r", "skill_vs_clim"]
    leaderboard = leaderboard[cols].sort_values(["site", "method", "split"]).reset_index(drop=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    leaderboard.to_csv(out_path, index=False)
    print(f"[train_baselines] wrote {out_path} ({len(leaderboard)} rows)")

    print("[train_baselines] logging MLflow runs...")
    for site in list(SITES) + ["ALL"]:
        for method in ("climatology", "persistence", "dept_ols", "dept_mlr", "generalist_mlr"):
            if ((leaderboard["site"] == site) & (leaderboard["method"] == method)).any():
                log_mlflow_run(site, method, leaderboard)

    with et.start_run("week1-baseline-leaderboard", seed=0, dataset_version=BASELINE_DATASET_VERSION):
        mlflow.log_artifact(str(out_path))

    print("[train_baselines] recording metric provenance...")
    cells_by_site = {site: len(ids) for site, ids in site_ids_by_site.items()}
    cells_by_site["ALL"] = sum(cells_by_site.values())
    for site in list(SITES) + ["ALL"]:
        for method in METHOD_PROVENANCE:
            if not ((leaderboard["site"] == site) & (leaderboard["method"] == method)).any():
                continue
            prov.record_metric_provenance(
                build_method_provenance(
                    site, method, cells=cells_by_site[site], bead_id=bead_id,
                    output_files=(str(out_path),),
                )
            )

    return leaderboard


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="tdew-x46 non-deep baseline ladder (5 methods).")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument(
        "--max-buckets",
        type=int,
        default=None,
        help="Limit to the first N id_buckets (smoke-testing only; omit for a real run).",
    )
    p.add_argument("--bead-id", default="tdew-x46",
                    help="bead governing this run, for tdew_estimation.provenance")
    return p


def main(argv: List[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(
        gold_dir=args.gold_dir, silver_dir=args.silver_dir, out_path=args.out,
        max_buckets=args.max_buckets, bead_id=args.bead_id,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
