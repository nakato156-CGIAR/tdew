#!/usr/bin/env python3
"""
pipeline.sequences

Sequence-eligibility index, consumed by the training data loaders built in
later beads (tdew-x46 TCN, tdew-2s6 GRU, tdew-efi Transformer). Reads
``Data/gold/model_features_norm`` (``pipeline.normalize`` output, one row per
(ID, date), already split-labeled and gap-free per the underlying daily
rasters) and, per ``id_bucket``, finds every maximal contiguous run of daily
rows sharing the same ``ID`` AND the same ``split`` — a run breaks on a
calendar gap (missing day), an ID change, or a ``split`` change (e.g.
2012-12-31 -> 2013-01-01 is calendar-contiguous but train -> validation).

For a context length ``L``, predicting ``Td(t+1)`` from
``X_{t-L+1:t}`` (docs/protocol/week1_manifest.yaml ``target.definition``), a
target day ``t`` inside a run of length ``N`` is eligible iff there are at
least ``L`` days at or before ``t`` in the run (``local_index(t) >= L-1``) AND
``t`` is not the run's last day (so ``t+1`` — the label — is itself inside the
same run/split). That gives, per run: ``n_eligible = max(0, N - L)``.

Sequences are deliberately NOT materialized as expanded L-length arrays here —
for L=60 that would multiply the already-multi-billion-row dataset ~60x. This
index (run boundaries + eligible-target-date range) is enough for a
DataLoader to slice ``model_features_norm`` on the fly per (ID, target_date),
while still proving — and letting anyone audit — that no window or label ever
crosses a train/validation/test boundary.

Output
------
``Data/gold/sequence_index/L={14,31,60}/id_bucket=XXXX/part.parquet``:
    ID, split, run_start_date, run_end_date, n_days,
    n_eligible_targets, first_eligible_target_date, last_eligible_target_date

Usage
-----
python -m pipeline.sequences
python -m pipeline.sequences --gold-dir Data/gold --lengths 14,31,60
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"

# Frozen context lengths (docs/protocol/week1_manifest.yaml, amended 2026-09-17
# from {14, 30, 60} to {14, 31, 60} — see the manifest's `amendments` entry).
DEFAULT_LENGTHS = (14, 31, 60)


def find_runs(df: pd.DataFrame) -> pd.DataFrame:
    """``df`` must be sorted by (ID, date). Returns one row per maximal
    contiguous (same ID, same split, no calendar gap) run."""
    prev_id = df["ID"].shift(1)
    prev_date = df["date"].shift(1)
    prev_split = df["split"].shift(1)

    same_id = df["ID"] == prev_id
    contiguous_day = (df["date"] - prev_date).dt.days == 1
    same_split = df["split"] == prev_split
    continues_run = same_id & contiguous_day.fillna(False) & same_split

    run_id = (~continues_run).cumsum()
    runs = df.groupby(run_id, sort=False).agg(
        ID=("ID", "first"),
        split=("split", "first"),
        run_start_date=("date", "min"),
        run_end_date=("date", "max"),
        n_days=("date", "size"),
    )
    return runs.reset_index(drop=True)


def eligibility_for_length(runs: pd.DataFrame, length: int) -> pd.DataFrame:
    out = runs.copy()
    out["n_eligible_targets"] = (out["n_days"] - length).clip(lower=0)
    has_eligible = out["n_eligible_targets"] > 0
    out["first_eligible_target_date"] = pd.NaT
    out["last_eligible_target_date"] = pd.NaT
    out.loc[has_eligible, "first_eligible_target_date"] = out.loc[has_eligible, "run_start_date"] + pd.to_timedelta(
        length - 1, unit="D"
    )
    out.loc[has_eligible, "last_eligible_target_date"] = out.loc[has_eligible, "run_end_date"] - pd.to_timedelta(
        1, unit="D"
    )
    return out[
        [
            "ID",
            "split",
            "run_start_date",
            "run_end_date",
            "n_days",
            "n_eligible_targets",
            "first_eligible_target_date",
            "last_eligible_target_date",
        ]
    ]


def run(gold_dir: Path, *, lengths: tuple[int, ...] = DEFAULT_LENGTHS, overwrite: bool = False) -> Path:
    features_dir = gold_dir / "model_features_norm"
    if not features_dir.exists():
        raise FileNotFoundError(f"{features_dir} not found — run pipeline.normalize first")

    bucket_ids = discover_bucket_ids(features_dir)
    out_root = gold_dir / "sequence_index"

    for length in lengths:
        out_dir = out_root / f"L={length}"
        if overwrite and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    for bucket_id in bucket_ids:
        df = pd.read_parquet(
            features_dir / f"id_bucket={bucket_id}" / "part.parquet", columns=["ID", "date", "split"]
        ).sort_values(["ID", "date"])
        runs = find_runs(df)
        for length in lengths:
            out_path = out_root / f"L={length}" / f"id_bucket={bucket_id}" / "part.parquet"
            if out_path.exists() and not overwrite:
                continue
            table = eligibility_for_length(runs, length)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            table.to_parquet(out_path, index=False)

    print(f"[sequences] wrote {out_root.relative_to(gold_dir.parent)} for L in {lengths} ({len(bucket_ids)} buckets)")
    return out_root


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sequence-eligibility index for context lengths L.")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument(
        "--lengths",
        type=str,
        default=",".join(str(length) for length in DEFAULT_LENGTHS),
        help="Comma-separated context lengths L.",
    )
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    lengths = tuple(int(x.strip()) for x in args.lengths.split(",") if x.strip())
    run(args.gold_dir, lengths=lengths, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
