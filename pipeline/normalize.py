#!/usr/bin/env python3
"""
pipeline.normalize

Normalization layer, consumed by ``pipeline.sequences`` and, eventually, model
training (tdew-x46/tdew-2s6/tdew-efi). Reads ``Data/gold/model_features``
(``pipeline.features`` output, already split-labeled) and:

1. Computes per-column mean/std using ONLY ``split == "train"`` rows, streamed
   bucket-by-bucket (two passes: accumulate sum/sumsq for the mean/variance,
   then apply) so the full ~2.4B-row 2002-2016 table never has to fit in
   memory at once — same bucketed-processing pattern as ``pipeline.gold``.
2. Saves those stats to ``Data/gold/normalization_stats.json`` (small, git-
   trackable — NOT a DVC/plain-on-disk-symlink output).
3. Applies z-score (``(x - mean) / std``) to every row (train/validation/test
   alike) using the train-only stats, adding ``{col}_norm`` columns. This is
   what satisfies the manifest's ``normalization_rule``: the *statistics* come
   from training only, but they are then applied everywhere.

``sin_doy``/``cos_doy`` are already in [-1, 1] and are not normalized.

Output
------
``Data/gold/normalization_stats.json``
``Data/gold/model_features_norm/id_bucket=XXXX/part.parquet``

Usage
-----
python -m pipeline.normalize
python -m pipeline.normalize --gold-dir Data/gold
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"

# Candidate continuous columns to normalize — intersected with whatever
# pipeline.gold/pipeline.features actually produced (TMAX/TD are optional).
CONTINUOUS_CANDIDATES = [
    "TMIN", "TMAX", "TD",
    "TMIN_anom", "TMAX_anom", "TD_anom",
    "DEM", "TDI", "X", "Y", "LST_DAY", "LST_NIGHT",
]


def _bucket_path(features_dir: Path, bucket_id: int) -> Path:
    return features_dir / f"id_bucket={bucket_id}" / "part.parquet"


def compute_train_stats(features_dir: Path, bucket_ids: list[int]) -> dict[str, dict[str, float]]:
    columns: list[str] | None = None
    sums: dict[str, float] = {}
    sumsqs: dict[str, float] = {}
    counts: dict[str, int] = {}

    for bucket_id in bucket_ids:
        df = pd.read_parquet(_bucket_path(features_dir, bucket_id))
        if columns is None:
            columns = [c for c in CONTINUOUS_CANDIDATES if c in df.columns]
            sums = {c: 0.0 for c in columns}
            sumsqs = {c: 0.0 for c in columns}
            counts = {c: 0 for c in columns}
        train = df.loc[df["split"] == "train"]
        for c in columns:
            vals = train[c].dropna().to_numpy(dtype=np.float64)
            counts[c] += vals.size
            sums[c] += vals.sum()
            sumsqs[c] += np.square(vals).sum()

    stats: dict[str, dict[str, float]] = {}
    for c in columns or []:
        n = counts[c]
        if n == 0:
            raise ValueError(f"No training rows found for column {c!r} — cannot compute normalization stats")
        mean = sums[c] / n
        variance = max(sumsqs[c] / n - mean**2, 0.0)
        std = float(np.sqrt(variance))
        stats[c] = {"mean": mean, "std": std, "n_train_rows": n}
    return stats


def apply_normalization(df: pd.DataFrame, stats: dict[str, dict[str, float]]) -> pd.DataFrame:
    for col, s in stats.items():
        if col not in df.columns:
            continue
        std = s["std"]
        if std == 0:
            df[f"{col}_norm"] = 0.0
        else:
            df[f"{col}_norm"] = (df[col] - s["mean"]) / std
    return df


def run(gold_dir: Path, *, overwrite: bool = False) -> Path:
    features_dir = gold_dir / "model_features"
    if not features_dir.exists():
        raise FileNotFoundError(f"{features_dir} not found — run pipeline.features first")

    bucket_ids = discover_bucket_ids(features_dir)

    stats_path = gold_dir / "normalization_stats.json"
    if overwrite or not stats_path.exists():
        stats = compute_train_stats(features_dir, bucket_ids)
        stats_path.write_text(json.dumps(stats, indent=2, sort_keys=True))
        print(f"[normalize] wrote {stats_path.relative_to(gold_dir.parent)} ({len(stats)} columns)")
    else:
        stats = json.loads(stats_path.read_text())
        print(f"[normalize] {stats_path.relative_to(gold_dir.parent)} exists, reusing")

    out_dir = gold_dir / "model_features_norm"
    if overwrite and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for bucket_id in bucket_ids:
        out_path = out_dir / f"id_bucket={bucket_id}" / "part.parquet"
        if out_path.exists() and not overwrite:
            continue
        df = pd.read_parquet(_bucket_path(features_dir, bucket_id))
        df = apply_normalization(df, stats)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out_path, index=False)
    print(f"[normalize] wrote {out_dir.relative_to(gold_dir.parent)} ({len(bucket_ids)} buckets)")
    return out_dir


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Train-only normalization stats + z-score application.")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.gold_dir, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
