#!/usr/bin/env python3
"""
experiments.tcn.zenml_pipeline

ZenML wrapper around ``experiments.tcn.train`` (bead tdew-x46, "TCN con
attention"), so the TCN training run is tracked/reproducible the same way
as the medallion ETL and the baseline ladder, per project convention: all
pipelines go through ZenML, not raw script invocation (see
``experiments/baselines/zenml_pipeline.py`` for the same pattern).

Usage
-----
uv run python -m experiments.tcn.zenml_pipeline --context-length 31
uv run python -m experiments.tcn.zenml_pipeline --context-length 31 --max-epochs 1 --max-buckets 2  # smoke test
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from zenml import pipeline, step

from experiments.tcn import checkpoint as ckpt
from experiments.tcn import train as train_tcn

DEFAULT_GOLD_DIR = str(train_tcn.DEFAULT_GOLD_DIR)
DEFAULT_SILVER_DIR = str(train_tcn.DEFAULT_SILVER_DIR)
DEFAULT_SITE_WEIGHTS = str(train_tcn.DEFAULT_SITE_WEIGHTS)
DEFAULT_NORM_STATS = str(train_tcn.DEFAULT_NORM_STATS)
DEFAULT_CHECKPOINT_ROOT = str(ckpt.DEFAULT_CHECKPOINT_ROOT)


@step
def train_tcn_step(
    context_length: int = 31,
    gold_dir: str = DEFAULT_GOLD_DIR,
    silver_dir: str = DEFAULT_SILVER_DIR,
    site_weights_path: str = DEFAULT_SITE_WEIGHTS,
    norm_stats_path: str = DEFAULT_NORM_STATS,
    checkpoint_root: str = DEFAULT_CHECKPOINT_ROOT,
    run_name: str = "week1-tcn-attention",
    resume: str = "auto",
    max_epochs: int = 30,
    batch_size: int = 1024,
    max_buckets: Optional[int] = None,
) -> str:
    result = train_tcn.run(
        gold_dir=Path(gold_dir),
        silver_dir=Path(silver_dir),
        context_length=context_length,
        site_weights_path=Path(site_weights_path),
        norm_stats_path=Path(norm_stats_path),
        checkpoint_root=Path(checkpoint_root),
        run_name=run_name,
        resume=resume,
        max_epochs=max_epochs,
        batch_size=batch_size,
        max_buckets=max_buckets,
    )
    return result["checkpoint_dir"]


@pipeline
def tcn_pipeline(
    context_length: int = 31,
    gold_dir: str = DEFAULT_GOLD_DIR,
    silver_dir: str = DEFAULT_SILVER_DIR,
    site_weights_path: str = DEFAULT_SITE_WEIGHTS,
    norm_stats_path: str = DEFAULT_NORM_STATS,
    checkpoint_root: str = DEFAULT_CHECKPOINT_ROOT,
    run_name: str = "week1-tcn-attention",
    resume: str = "auto",
    max_epochs: int = 30,
    batch_size: int = 1024,
    max_buckets: Optional[int] = None,
) -> None:
    train_tcn_step(
        context_length=context_length,
        gold_dir=gold_dir,
        silver_dir=silver_dir,
        site_weights_path=site_weights_path,
        norm_stats_path=norm_stats_path,
        checkpoint_root=checkpoint_root,
        run_name=run_name,
        resume=resume,
        max_epochs=max_epochs,
        batch_size=batch_size,
        max_buckets=max_buckets,
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ZenML pipeline for TCN+attention training (bead tdew-x46).")
    p.add_argument("--context-length", type=int, default=31, choices=[14, 31, 60])
    p.add_argument("--gold-dir", type=str, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=str, default=DEFAULT_SILVER_DIR)
    p.add_argument("--site-weights", type=str, default=DEFAULT_SITE_WEIGHTS)
    p.add_argument("--norm-stats", type=str, default=DEFAULT_NORM_STATS)
    p.add_argument("--checkpoint-root", type=str, default=DEFAULT_CHECKPOINT_ROOT)
    p.add_argument("--run-name", type=str, default="week1-tcn-attention")
    p.add_argument("--resume", type=str, default="auto")
    p.add_argument("--max-epochs", type=int, default=30)
    p.add_argument("--batch-size", type=int, default=1024)
    p.add_argument("--max-buckets", type=int, default=None)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    tcn_pipeline(
        context_length=args.context_length,
        gold_dir=args.gold_dir,
        silver_dir=args.silver_dir,
        site_weights_path=args.site_weights,
        norm_stats_path=args.norm_stats,
        checkpoint_root=args.checkpoint_root,
        run_name=args.run_name,
        resume=args.resume,
        max_epochs=args.max_epochs,
        batch_size=args.batch_size,
        max_buckets=args.max_buckets,
    )
