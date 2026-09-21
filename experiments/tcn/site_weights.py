#!/usr/bin/env python3
"""
experiments.tcn.site_weights

Per-site sample weights for the multi-site TCN training loss
(``tdew_estimation.models.losses.weighted_huber_loss``), inheriting
``generalist_mlr``'s criterion (``experiments/baselines/train_baselines.py``):
``weight = 1 / n_train_rows(site)``, so Loreto/Iquitos does not dominate the
shared fit by row-count volume alone.

Counted from ``Data/gold/sequence_index/L=31`` (train split,
``n_eligible_targets`` summed per site) -- cheap (only sequence_index
metadata, never touches ``model_features_norm``) and exact (it is the same
eligibility count the L=31 DataLoader will actually iterate over).

Design decision (see the tcn-attention design plan, bead tdew-x46): these
weights are computed ONCE from L=31 and reused unchanged for the L=14 and
L=60 training runs too, instead of recomputing them per L. Recomputing per L
would make the tdew-bs4 L-ablation confound "different L" with "slightly
different site weighting" (L=60 loses a few more warm-up days per cell than
L=14); freezing the weights keeps the loss function identical across the
three L runs, so L is the only thing that varies.

Usage
-----
uv run python -m experiments.tcn.site_weights
uv run python -m experiments.tcn.site_weights --out experiments/tcn/site_weights.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import pandas as pd

from pipeline.qc import SITES, load_site_ids
from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"
DEFAULT_OUT = Path(__file__).resolve().parent / "site_weights.json"
WEIGHT_SEQUENCE_LENGTH = 31  # frozen reference L for the weight computation, see module docstring

# docs/protocol/week1_manifest.yaml sites.departments[].region_natural
REGION_NATURAL: Dict[str, str] = {
    "lima": "Costa",
    "cusco": "Sierra",
    "iquitos_loreto": "Selva",
    "tarapoto_san_martin": "Selva",
}
REGION_INDEX: Dict[str, int] = {"Costa": 0, "Sierra": 1, "Selva": 2}


def count_train_rows_per_site(
    gold_dir: Path, silver_dir: Path, *, length: int = WEIGHT_SEQUENCE_LENGTH, max_buckets: int | None = None
) -> Dict[str, int]:
    seq_dir = gold_dir / "sequence_index" / f"L={length}"
    if not seq_dir.exists():
        raise FileNotFoundError(f"{seq_dir} not found -- run pipeline.sequences first")

    site_ids = {site: load_site_ids(silver_dir, site) for site in SITES}
    bucket_ids = discover_bucket_ids(seq_dir)
    if max_buckets is not None:
        bucket_ids = bucket_ids[:max_buckets]

    counts = {site: 0 for site in SITES}
    for bucket_id in bucket_ids:
        path = seq_dir / f"id_bucket={bucket_id}" / "part.parquet"
        if not path.exists():
            continue
        df = pd.read_parquet(path, columns=["ID", "split", "n_eligible_targets"])
        df = df[df["split"] == "train"]
        if df.empty:
            continue
        for site, ids in site_ids.items():
            site_df = df[df["ID"].isin(ids)]
            counts[site] += int(site_df["n_eligible_targets"].sum())
    return counts


def compute_site_weights(train_counts: Dict[str, int]) -> Dict[str, float]:
    return {site: (1.0 / n if n else 0.0) for site, n in train_counts.items()}


def run(
    gold_dir: Path = DEFAULT_GOLD_DIR,
    silver_dir: Path = DEFAULT_SILVER_DIR,
    out: Path = DEFAULT_OUT,
    *,
    max_buckets: int | None = None,
) -> Path:
    train_counts = count_train_rows_per_site(gold_dir, silver_dir, max_buckets=max_buckets)
    weights = compute_site_weights(train_counts)
    payload = {
        "reference_context_length": WEIGHT_SEQUENCE_LENGTH,
        "train_n_eligible_targets": train_counts,
        "weight": weights,
        "region_natural": REGION_NATURAL,
        "region_index": REGION_INDEX,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(f"[site_weights] wrote {out} (train rows: {train_counts})")
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Per-site sample weights for multi-site TCN training.")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--max-buckets", type=int, default=None, help="Smoke-test hook: only scan the first N buckets.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.gold_dir, args.silver_dir, args.out, max_buckets=args.max_buckets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
