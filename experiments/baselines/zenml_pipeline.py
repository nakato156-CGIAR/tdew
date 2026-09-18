#!/usr/bin/env python3
"""
experiments.baselines.zenml_pipeline

ZenML wrapper around ``experiments.baselines.train_baselines`` (the tdew-x46
baseline ladder), so the baseline run is tracked/reproducible the same way as
the medallion ETL (``pipeline.zenml_pipeline``), per project convention: all
pipelines go through ZenML, not raw script invocation.

Usage
-----
uv run python -m experiments.baselines.zenml_pipeline
uv run python -m experiments.baselines.zenml_pipeline --max-buckets 2  # smoke test
"""

from __future__ import annotations

import argparse
from pathlib import Path

from zenml import pipeline, step

from experiments.baselines import train_baselines

DEFAULT_GOLD_DIR = str(train_baselines.DEFAULT_GOLD_DIR)
DEFAULT_SILVER_DIR = str(train_baselines.DEFAULT_SILVER_DIR)
DEFAULT_OUT = str(train_baselines.DEFAULT_OUT)


@step
def train_baselines_step(
    gold_dir: str = DEFAULT_GOLD_DIR,
    silver_dir: str = DEFAULT_SILVER_DIR,
    out_path: str = DEFAULT_OUT,
    max_buckets: int | None = None,
) -> str:
    train_baselines.run(
        gold_dir=Path(gold_dir),
        silver_dir=Path(silver_dir),
        out_path=Path(out_path),
        max_buckets=max_buckets,
    )
    return out_path


@pipeline
def baselines_pipeline(
    gold_dir: str = DEFAULT_GOLD_DIR,
    silver_dir: str = DEFAULT_SILVER_DIR,
    out_path: str = DEFAULT_OUT,
    max_buckets: int | None = None,
) -> None:
    train_baselines_step(gold_dir=gold_dir, silver_dir=silver_dir, out_path=out_path, max_buckets=max_buckets)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ZenML pipeline for the tdew-x46 baseline ladder.")
    p.add_argument("--gold-dir", type=str, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=str, default=DEFAULT_SILVER_DIR)
    p.add_argument("--out", type=str, default=DEFAULT_OUT)
    p.add_argument("--max-buckets", type=int, default=None)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    baselines_pipeline(gold_dir=args.gold_dir, silver_dir=args.silver_dir, out_path=args.out, max_buckets=args.max_buckets)
