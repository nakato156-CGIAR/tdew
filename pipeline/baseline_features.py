#!/usr/bin/env python3
"""
pipeline.baseline_features

Leak-safe, lagged feature table for the tdew-x46 non-deep baselines
(persistence, climatology, dept_ols, dept_mlr, generalist_mlr — see
``docs/protocol/week1_manifest.yaml`` and the tdew-x46 plan). Reads
``Data/gold/model_features_norm`` (one row per (ID, date), already
split-labeled) and, per ``id_bucket``:

- Reuses ``Data/gold/sequence_index/L=31`` (``pipeline.sequences``) to decide
  which target dates ``t+1`` are eligible: at least 30 contiguous days of
  history ending at ``t`` AND ``t+1`` inside the same (ID, split) run. This
  is exactly the run/gap/split-boundary logic ``pipeline.sequences.find_runs``
  already solved for the L=31 sequential-model window (30-day lookback is the
  same magnitude as our max lag, 30) — reusing it here avoids re-deriving
  "no window/label may cross a train/validation/test boundary" a second time.
- For each row at date ``t`` (the last observed day, predicting ``Td(t+1)``),
  builds ONLY backward-looking features (``leakage_constraint`` in the
  manifest: no input may come from ``t+1`` or later): ``TD_anom_lag{1,2,3,7,
  30}`` = ``TD_anom`` at ``t, t-1, t-2, t-6, t-29`` respectively, and
  ``TMIN_anom_lag{0,1}`` = ``TMIN_anom`` at ``t, t-1``. This differs from the
  production model (``tdew_estimation/anomaly_train.py``, ``MODEL_INPUTS.md``)
  which uses TMIN of the *same day as the target* — that design does not
  satisfy this protocol's stricter leakage rule, so it is not replicated here.
- Carries the target-day (``t+1``) climatology/seasonal/static covariates
  (``TD_clim_target``, ``sin_doy_target``, ``cos_doy_target``,
  ``LST_DAY_target``, ``LST_NIGHT_target``) plus the ID-level static
  covariates (``DEM``, ``TDI``, ``X``, ``Y``, unchanged by date) needed by
  ``dept_mlr``/``generalist_mlr``.
- Emits the regression targets in both anomaly and raw units:
  ``TD_anom_target`` (what the regressions predict) and ``TD_target`` (what
  metrics are scored against).

Output
------
``Data/gold/baseline_dataset/id_bucket=XXXX/part.parquet`` — one row per
eligible (ID, date=t): ID, date, split, all lag/target/static columns above.

Usage
-----
python -m pipeline.baseline_features
python -m pipeline.baseline_features --gold-dir Data/gold
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"
SEQUENCE_LENGTH = 31  # covers lag30 exactly (X_{t-L+1:t}, L=31 -> reaches t-30... t)

# (output_column, shift_from_t) — TD_anom at t-shift, named by its distance
# (in days) from the *target* t+1 (e.g. lag1 = TD_anom(t), one day before t+1).
TD_ANOM_LAGS = [("TD_anom_lag1", 0), ("TD_anom_lag2", 1), ("TD_anom_lag3", 2), ("TD_anom_lag7", 6), ("TD_anom_lag30", 29)]
TMIN_ANOM_LAGS = [("TMIN_anom_lag0", 0), ("TMIN_anom_lag1", 1)]

STATIC_COLS = ["DEM", "TDI", "X", "Y"]
TARGET_DAY_COLS = ["TD_clim", "sin_doy", "cos_doy", "LST_DAY", "LST_NIGHT"]
TARGET_DAY_RENAME = {
    "TD_clim": "TD_clim_target",
    "sin_doy": "sin_doy_target",
    "cos_doy": "cos_doy_target",
    "LST_DAY": "LST_DAY_target",
    "LST_NIGHT": "LST_NIGHT_target",
}


def _bucket_path(root: Path, bucket_id: int) -> Path:
    return root / f"id_bucket={bucket_id}" / "part.parquet"


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """``df`` must be sorted by (ID, date). Adds backward-looking lag columns
    and the t+1 target columns, all via per-ID shifts (no cross-ID leakage)."""
    g = df.groupby("ID", sort=False)

    for col, shift in TD_ANOM_LAGS:
        df[col] = g["TD_anom"].shift(shift) if shift else df["TD_anom"]
    for col, shift in TMIN_ANOM_LAGS:
        df[col] = g["TMIN_anom"].shift(shift) if shift else df["TMIN_anom"]

    df["TD_anom_target"] = g["TD_anom"].shift(-1)
    df["TD_target"] = g["TD"].shift(-1)
    for col in TARGET_DAY_COLS:
        if col in df.columns:
            df[TARGET_DAY_RENAME[col]] = g[col].shift(-1)

    return df


def eligible_mask(df: pd.DataFrame, seq_index: pd.DataFrame) -> pd.Series:
    """Boolean mask over ``df`` rows (date ``t``) whose target ``t+1`` falls
    inside an L=31-eligible window of ``seq_index`` (same ID, same run).

    Each ID has only a handful of runs (typically one per split, ~3), so
    merging on ``ID`` explodes each row ~3x at most — kept fully vectorized
    (no per-row Python-object set) so this stays cheap even for a
    multi-million-row bucket."""
    elig = seq_index.loc[
        seq_index["n_eligible_targets"] > 0,
        ["ID", "first_eligible_target_date", "last_eligible_target_date"],
    ]
    if elig.empty:
        return pd.Series(False, index=df.index)

    probe = pd.DataFrame({"ID": df["ID"].to_numpy(), "target_date": (df["date"] + pd.Timedelta(days=1)).to_numpy()})
    probe = probe.reset_index()  # keep the original df row position as a plain column

    merged = probe.merge(elig, on="ID", how="inner")
    hit = (merged["target_date"] >= merged["first_eligible_target_date"]) & (
        merged["target_date"] <= merged["last_eligible_target_date"]
    )

    mask = pd.Series(False, index=df.index)
    mask.iloc[merged.loc[hit, "index"].unique()] = True
    return mask


def build_bucket_baseline_features(features_df: pd.DataFrame, seq_index: pd.DataFrame) -> pd.DataFrame:
    df = features_df.sort_values(["ID", "date"]).reset_index(drop=True)
    df = add_lag_features(df)
    mask = eligible_mask(df, seq_index)
    df = df.loc[mask].reset_index(drop=True)

    keep = (
        ["ID", "date", "split"]
        + [c for c, _ in TD_ANOM_LAGS]
        + [c for c, _ in TMIN_ANOM_LAGS]
        + ["TD_anom_target", "TD_target"]
        + [v for k, v in TARGET_DAY_RENAME.items() if v in df.columns]
        + [c for c in STATIC_COLS if c in df.columns]
    )
    return df[keep]


def run(gold_dir: Path, *, overwrite: bool = False) -> Path:
    features_dir = gold_dir / "model_features_norm"
    seq_dir = gold_dir / "sequence_index" / f"L={SEQUENCE_LENGTH}"
    if not features_dir.exists():
        raise FileNotFoundError(f"{features_dir} not found — run pipeline.normalize first")
    if not seq_dir.exists():
        raise FileNotFoundError(f"{seq_dir} not found — run pipeline.sequences first")

    out_dir = gold_dir / "baseline_dataset"
    if overwrite and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    bucket_ids = discover_bucket_ids(features_dir)
    for bucket_id in bucket_ids:
        out_path = _bucket_path(out_dir, bucket_id)
        if out_path.exists() and not overwrite:
            continue
        features_df = pd.read_parquet(_bucket_path(features_dir, bucket_id))
        seq_path = _bucket_path(seq_dir, bucket_id)
        seq_index = pd.read_parquet(seq_path) if seq_path.exists() else pd.DataFrame(
            columns=["ID", "n_eligible_targets", "first_eligible_target_date", "last_eligible_target_date"]
        )
        table = build_bucket_baseline_features(features_df, seq_index)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        table.to_parquet(out_path, index=False)
    print(f"[baseline_features] wrote {out_dir.relative_to(gold_dir.parent)} ({len(bucket_ids)} buckets)")
    return out_dir


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Leak-safe lagged feature table for the tdew-x46 non-deep baselines.")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.gold_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
