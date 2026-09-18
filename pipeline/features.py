#!/usr/bin/env python3
"""
pipeline.features

Derived-features layer, consumed by ``pipeline.normalize``/``pipeline.sequences``.
Reads ``Data/gold/model_input`` (already TMAX-complete and leak-free-climatology,
see ``pipeline.gold``) and, per ``id_bucket``:

- Restricts rows to the frozen modeling range 2002-01-01..2016-12-31
  (``docs/protocol/week1_manifest.yaml`` ``period.full_range`` — TD does not
  exist outside this range, so it is not part of the modeling dataset).
- Assigns a ``split`` column (``train``/``validation``/``test``) from the
  calendar year of ``date``, per the frozen, non-overlapping
  ``period.splits``.
- Adds the von Mises / circular day-of-year encoding: ``sin_doy``/``cos_doy``
  = sin/cos(2*pi*doy/366). No separate lag columns are added here — see the
  ``lag_features`` note in the manifest (sequence models get Td/Tmin/Tmax
  history from the sequence window itself, built downstream by
  ``pipeline.sequences``).

Output
------
``Data/gold/model_features/id_bucket=XXXX/part.parquet`` — same columns as
``Data/gold/model_input`` plus ``split``, ``sin_doy``, ``cos_doy``, restricted
to 2002-2016.

Usage
-----
python -m pipeline.features
python -m pipeline.features --gold-dir Data/gold
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"

# Frozen period + splits (docs/protocol/week1_manifest.yaml, period).
FULL_RANGE_START = pd.Timestamp("2002-01-01")
FULL_RANGE_END = pd.Timestamp("2016-12-31")
SPLIT_YEAR_RANGES = {
    "train": (2002, 2012),
    "validation": (2013, 2014),
    "test": (2015, 2016),
}
DOY_PERIOD = 366  # calendar day-of-year wraps at 366 (leap years included)


def assign_split(dates: pd.Series) -> pd.Series:
    years = pd.DatetimeIndex(dates).year
    split = pd.Series(pd.NA, index=dates.index, dtype="object")
    for name, (start, end) in SPLIT_YEAR_RANGES.items():
        split = split.mask((years >= start) & (years <= end), name)
    return split


def add_doy_encoding(df: pd.DataFrame) -> pd.DataFrame:
    theta = 2 * np.pi * df["doy"].to_numpy() / DOY_PERIOD
    df["sin_doy"] = np.sin(theta)
    df["cos_doy"] = np.cos(theta)
    return df


def build_bucket_features(table: pd.DataFrame) -> pd.DataFrame:
    in_range = (table["date"] >= FULL_RANGE_START) & (table["date"] <= FULL_RANGE_END)
    table = table.loc[in_range].copy()
    table["split"] = assign_split(table["date"])
    table = add_doy_encoding(table)
    return table.sort_values(["ID", "date"]).reset_index(drop=True)


def run(gold_dir: Path, *, overwrite: bool = False) -> Path:
    model_input_dir = gold_dir / "model_input"
    if not model_input_dir.exists():
        raise FileNotFoundError(f"{model_input_dir} not found — run pipeline.gold first")

    out_dir = gold_dir / "model_features"
    if overwrite and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    bucket_ids = discover_bucket_ids(model_input_dir)
    for bucket_id in bucket_ids:
        out_path = out_dir / f"id_bucket={bucket_id}" / "part.parquet"
        if out_path.exists() and not overwrite:
            continue
        table = pd.read_parquet(model_input_dir / f"id_bucket={bucket_id}" / "part.parquet")
        features = build_bucket_features(table)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        features.to_parquet(out_path, index=False)
    print(f"[features] wrote {out_dir.relative_to(gold_dir.parent)} ({len(bucket_ids)} buckets)")
    return out_dir


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Derived-features layer: split label + sin/cos(DOY).")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.gold_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
