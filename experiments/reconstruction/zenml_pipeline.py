"""ZenML orchestration for bucket preparation, reconstruction and evaluation.

Importing this module does not execute a pipeline.  Commands are documented in
``HANDOFF.md`` for a later session after source paths and storage are checked.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from zenml import pipeline, step

from . import cli as reconstruction_cli
from .bucketed import (
    build_canonical_buckets,
    materialize_silver_buckets,
    read_panel_ids,
    select_panel,
)
from .evaluation import cumulative_error_curve, evaluate_predictions, macro_department_metrics


@step
def panel_step(silver_dir: str, protocol: str, panel_path: str, seed: int = 0) -> str:
    panel = select_panel(Path(silver_dir), protocol, seed=seed)
    target = Path(panel_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(target, index=False)
    return str(target)


@step
def rebucket_silver_step(
    silver_dir: str,
    silver_bucket_root: str,
    panel_path: str,
    num_buckets: int,
    months_per_part: int = 12,
    overwrite: bool = False,
) -> str:
    result = materialize_silver_buckets(
        Path(silver_dir), Path(silver_bucket_root), num_buckets=num_buckets,
        selected_ids=read_panel_ids(Path(panel_path)), overwrite=overwrite,
        months_per_part=months_per_part,
    )
    return str(result)


@step
def canonical_audit_step(
    historical_root: str,
    silver_bucket_root: str,
    silver_dir: str,
    canonical_root: str,
    panel_path: str,
    overwrite: bool = False,
    max_buckets: int | None = None,
) -> str:
    result = build_canonical_buckets(
        Path(historical_root), Path(silver_bucket_root), Path(silver_dir),
        Path(canonical_root), overwrite=overwrite, max_buckets=max_buckets,
        selected_ids=read_panel_ids(Path(panel_path)),
    )
    return str(result)


@step(enable_cache=False)
def reconstruction_step(
    canonical_root: str,
    panel_path: str,
    output_path: str,
    protocol: str,
    mode: str,
    model: str,
    feature_set: str,
    seed: int,
    max_steps: int,
    eval_every: int,
    checkpoint: str | None,
    context_length: int,
    batch_size: int,
    num_workers: int,
    learning_rate: float,
    objective: str,
    feature_cache: str | None,
    device: str | None,
    unlock_ll4: bool,
) -> str:
    argv = [
        "--input", canonical_root, "--panel-ids", panel_path,
        "--output", output_path, "--protocol", protocol, "--mode", mode,
        "--model", model, "--feature-set", feature_set, "--seed", str(seed),
        "--max-steps", str(max_steps), "--eval-every", str(eval_every),
        "--context-length", str(context_length), "--batch-size", str(batch_size),
        "--num-workers", str(num_workers), "--learning-rate", str(learning_rate),
        "--objective", objective,
    ]
    if feature_cache:
        argv.extend(["--feature-cache", feature_cache])
    if checkpoint:
        argv.extend(["--checkpoint", checkpoint])
    if device:
        argv.extend(["--device", device])
    if unlock_ll4:
        argv.append("--unlock-ll4")
    reconstruction_cli.main(argv)
    return output_path


@step
def evaluation_step(predictions_path: str, output_dir: str) -> str:
    predictions = pd.read_parquet(predictions_path)
    metrics = evaluate_predictions(predictions)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    metrics.to_parquet(target / "metrics.parquet", index=False)
    macro_department_metrics(metrics).to_parquet(target / "metrics_department_macro.parquet", index=False)
    cumulative_error_curve(predictions).to_parquet(target / "cumulative_error.parquet", index=False)
    return str(target)


@pipeline
def reconstruction_pipeline(
    historical_root: str,
    silver_dir: str,
    work_root: str,
    output_path: str,
    protocol: str = "dev_a",
    mode: str = "direct",
    model: str = "tcn",
    feature_set: str = "exogenous_full",
    seed: int = 0,
    num_buckets: int = 8192,
    months_per_part: int = 12,
    max_buckets: int | None = None,
    max_steps: int = 20_000,
    eval_every: int = 1_000,
    checkpoint: str | None = None,
    context_length: int = 7,
    batch_size: int = 1024,
    num_workers: int = 0,
    learning_rate: float = 3e-4,
    objective: str = "mse",
    feature_cache: str | None = None,
    device: str | None = None,
    unlock_ll4: bool = False,
    overwrite: bool = False,
) -> None:
    root = Path(work_root)
    panel = panel_step(
        silver_dir=silver_dir,
        protocol=protocol,
        panel_path=str(root / "panels" / f"{protocol}_seed{seed}.csv"),
        seed=seed,
    )
    silver_buckets = rebucket_silver_step(
        silver_dir=silver_dir,
        silver_bucket_root=str(root / "silver_bucketed"),
        panel_path=panel,
        num_buckets=num_buckets,
        months_per_part=months_per_part,
        overwrite=overwrite,
    )
    canonical = canonical_audit_step(
        historical_root=historical_root,
        silver_bucket_root=silver_buckets,
        silver_dir=silver_dir,
        canonical_root=str(root / "canonical"),
        panel_path=panel,
        overwrite=overwrite,
        max_buckets=max_buckets,
    )
    predictions = reconstruction_step(
        canonical_root=canonical,
        panel_path=panel,
        output_path=output_path,
        protocol=protocol,
        mode=mode,
        model=model,
        feature_set=feature_set,
        seed=seed,
        max_steps=max_steps,
        eval_every=eval_every,
        checkpoint=checkpoint,
        context_length=context_length,
        batch_size=batch_size,
        num_workers=num_workers,
        learning_rate=learning_rate,
        objective=objective,
        feature_cache=feature_cache or str(root / "features"),
        device=device,
        unlock_ll4=unlock_ll4,
    )
    evaluation_step(predictions_path=predictions, output_dir=str(Path(output_path).parent / "evaluation"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ZenML para reconstruccion continua de Td")
    parser.add_argument("--historical-root", required=True)
    parser.add_argument("--silver-dir", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--protocol", choices=["dev_a", "dev_b", "ll4", "production"], default="dev_a")
    parser.add_argument("--mode", choices=["direct", "recursive"], default="direct")
    parser.add_argument("--model", choices=["ridge", "histgb", "tcn"], default="tcn")
    parser.add_argument("--feature-set", default="exogenous_full")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--num-buckets", type=int, default=8192)
    parser.add_argument("--months-per-part", type=int, default=12)
    parser.add_argument("--max-buckets", type=int)
    parser.add_argument("--max-steps", type=int, default=20_000)
    parser.add_argument("--eval-every", type=int, default=1_000)
    parser.add_argument("--checkpoint")
    parser.add_argument("--context-length", type=int, default=7, choices=[3, 7, 14, 31, 60])
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--feature-cache")
    parser.add_argument("--objective", choices=["mse", "huber"], default="mse")
    parser.add_argument("--device", choices=["cpu", "cuda"])
    parser.add_argument("--unlock-ll4", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    reconstruction_pipeline(
        historical_root=args.historical_root, silver_dir=args.silver_dir,
        work_root=args.work_root, output_path=args.output,
        months_per_part=args.months_per_part,
        protocol=args.protocol, mode=args.mode, model=args.model,
        feature_set=args.feature_set, seed=args.seed, num_buckets=args.num_buckets,
        max_buckets=args.max_buckets, max_steps=args.max_steps,
        eval_every=args.eval_every, checkpoint=args.checkpoint,
        context_length=args.context_length, batch_size=args.batch_size,
        num_workers=args.num_workers, learning_rate=args.learning_rate,
        objective=args.objective, device=args.device, feature_cache=args.feature_cache,
        unlock_ll4=args.unlock_ll4, overwrite=args.overwrite,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
