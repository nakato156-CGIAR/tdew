#!/usr/bin/env python3
"""
experiments.tcn.train

Training loop for ``TCNAttentionModel`` (bead tdew-x46, "TCN con attention"
variant -- see the tcn-attention design plan, ``adaptive-leaping-summit.md``,
for the full architecture/loss/dataloader/checkpoint rationale).

Scope note (2026-09-18): this module is complete and runnable, but this
session's task is architecture + code + mechanics tests only -- nobody has
run ``run()`` against real ``Data/gold`` yet. That is deliberately deferred
to a later session (see the bead's notes).

Validation metrics are pooled across all 4 protocol departments (the
dataset already combines them into one multi-site training set, per the
generalist_mlr finding -- ``reports/week1_baselines/TRACEABILITY.md``), in
the same n/rmse/mae/bias/r/skill_vs_clim format as
``reports/week1_baselines/leaderboard.csv``'s ``site="ALL"`` rows, computed
via the same ``tdew_estimation.metrics.MetricsAccum`` the baselines use. A
per-site breakdown (mirroring the full leaderboard) is left for the
follow-up session that actually trains against real data.

Usage
-----
uv run python -m experiments.tcn.train --context-length 31 --max-epochs 1 --max-buckets 2  # smoke test
uv run python -m experiments.tcn.train --context-length 31 --max-epochs 30
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import mlflow
import numpy as np
import torch
from torch.utils.data import DataLoader

from experiments.tcn import checkpoint as ckpt
from experiments.tcn.dataset import DEFAULT_GOLD_DIR, DEFAULT_SILVER_DIR, TdewWindowDataset, load_site_weights
from pipeline.qc import SITES
from tdew_estimation import experiment_tracking as et
from tdew_estimation.metrics import MetricsAccum
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel, invert_to_physical, validate_receptive_field

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SITE_WEIGHTS = Path(__file__).resolve().parent / "site_weights.json"
DEFAULT_NORM_STATS = DEFAULT_GOLD_DIR / "normalization_stats.json"
DATASET_VERSION = "Data/gold/model_features_norm"


def load_td_anom_stats(path: Path) -> tuple[float, float]:
    stats = json.loads(Path(path).read_text())["TD_anom"]
    return float(stats["mean"]), float(stats["std"])


def build_dataloader(
    *,
    gold_dir: Path,
    silver_dir: Path,
    context_length: int,
    split: str,
    site_weights: Dict[str, float],
    batch_size: int,
    num_workers: int,
    seed: int,
    max_buckets: Optional[int],
    shuffle_buffer_size: int = 20_000,
) -> tuple[TdewWindowDataset, DataLoader]:
    dataset = TdewWindowDataset(
        gold_dir,
        silver_dir,
        context_length=context_length,
        split=split,
        site_weights=site_weights,
        sites=SITES,
        shuffle_buffer_size=shuffle_buffer_size,
        seed=seed,
        max_buckets=max_buckets,
    )
    loader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, pin_memory=torch.cuda.is_available())
    return dataset, loader


def configure_gpu() -> None:
    if not torch.cuda.is_available():
        return
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True  # safe: every run uses one fixed context_length (T never varies)


def _to_device(batch: Dict[str, torch.Tensor], device: torch.device) -> Dict[str, torch.Tensor]:
    return {k: v.to(device, non_blocking=True) for k, v in batch.items()}


def train_one_epoch(
    model: TCNAttentionModel,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    *,
    delta: float,
    use_amp: bool,
) -> tuple[float, int]:
    from tdew_estimation.models.losses import weighted_huber_loss

    model.train()
    total_loss = 0.0
    total_weight = 0.0
    steps = 0
    for batch in loader:
        batch = _to_device(batch, device)
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=use_amp):
            pred_norm = model(
                batch["dynamic"].float(), batch["static"].float(), batch["region"], batch["target_cond"].float()
            )
            loss = weighted_huber_loss(pred_norm, batch["label"].float(), batch["weight"].float(), delta=delta)
        loss.backward()
        optimizer.step()

        batch_weight = float(batch["weight"].sum().item())
        total_loss += float(loss.item()) * batch_weight
        total_weight += batch_weight
        steps += 1
    mean_loss = total_loss / total_weight if total_weight > 0 else float("nan")
    return mean_loss, steps


@torch.no_grad()
def evaluate(
    model: TCNAttentionModel,
    loader: DataLoader,
    device: torch.device,
    *,
    td_anom_mean: float,
    td_anom_std: float,
) -> Dict[str, float]:
    model.eval()
    model_accum = MetricsAccum()
    clim_accum = MetricsAccum()
    for batch in loader:
        batch = _to_device(batch, device)
        pred_norm = model(
            batch["dynamic"].float(), batch["static"].float(), batch["region"], batch["target_cond"].float()
        )
        td_clim = batch["td_clim_target"].float()
        td_pred = invert_to_physical(pred_norm, td_anom_mean, td_anom_std, td_clim)
        td_obs = invert_to_physical(batch["label"].float(), td_anom_mean, td_anom_std, td_clim)

        model_accum.add(td_pred.detach().cpu().numpy(), td_obs.detach().cpu().numpy())
        clim_accum.add(td_clim.detach().cpu().numpy(), td_obs.detach().cpu().numpy())

    model_metrics = model_accum.finalize()
    clim_metrics = clim_accum.finalize()
    clim_rmse = clim_metrics["rmse"]
    model_metrics["skill_vs_clim"] = (
        1.0 - model_metrics["rmse"] / clim_rmse if clim_rmse and np.isfinite(clim_rmse) else float("nan")
    )
    return model_metrics


def run(
    *,
    gold_dir: Path = DEFAULT_GOLD_DIR,
    silver_dir: Path = DEFAULT_SILVER_DIR,
    context_length: int = 31,
    d_model: int = 64,
    n_tcn_blocks: int = 4,
    kernel_size: int = 3,
    dilation_base: int = 2,
    n_attention_heads: int = 4,
    dropout: float = 0.1,
    huber_delta: float = 1.0,
    batch_size: int = 1024,
    num_workers: int = 4,
    lr: float = 3e-4,
    max_epochs: int = 30,
    seed: int = 0,
    site_weights_path: Path = DEFAULT_SITE_WEIGHTS,
    norm_stats_path: Path = DEFAULT_NORM_STATS,
    checkpoint_root: Path = ckpt.DEFAULT_CHECKPOINT_ROOT,
    run_name: str = "week1-tcn-attention",
    resume: str = "auto",
    overwrite: bool = False,
    max_buckets: Optional[int] = None,
    device: Optional[str] = None,
) -> Dict[str, Any]:
    validate_receptive_field(context_length, kernel_size, n_tcn_blocks, dilation_base)
    configure_gpu()

    torch.manual_seed(seed)
    np.random.seed(seed)
    resolved_device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))

    site_weights = load_site_weights(site_weights_path)
    td_anom_mean, td_anom_std = load_td_anom_stats(norm_stats_path)

    config = TCNAttentionConfig(
        d_model=d_model,
        n_tcn_blocks=n_tcn_blocks,
        kernel_size=kernel_size,
        dilation_base=dilation_base,
        n_attention_heads=n_attention_heads,
        dropout=dropout,
    )
    model = TCNAttentionModel(config).to(resolved_device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max_epochs)

    ckpt_dir = ckpt.checkpoint_dir(run_name, context_length, seed, checkpoint_root)
    start_epoch = 0
    global_step = 0
    best_val_skill = float("-inf")
    mlflow_run_id: Optional[str] = None

    resume_path = ckpt.resolve_resume_path(resume, ckpt_dir)
    if resume_path is None and resume == "none" and ckpt_dir.exists() and not overwrite:
        raise FileExistsError(f"{ckpt_dir} already has checkpoints; pass --overwrite or --resume auto")
    if resume_path is not None:
        loaded = ckpt.load_checkpoint(resume_path)  # always CPU-mapped, see checkpoint.load_checkpoint docstring
        ckpt.restore_into(loaded, model=model, optimizer=optimizer, scheduler=scheduler)
        start_epoch = int(loaded["epoch"]) + 1
        global_step = int(loaded["global_step"])
        best_val_skill = float(loaded["best_val_skill"])
        mlflow_run_id = loaded.get("mlflow_run_id")

    train_ds, train_loader = build_dataloader(
        gold_dir=gold_dir,
        silver_dir=silver_dir,
        context_length=context_length,
        split="train",
        site_weights=site_weights,
        batch_size=batch_size,
        num_workers=num_workers,
        seed=seed,
        max_buckets=max_buckets,
    )
    _, val_loader = build_dataloader(
        gold_dir=gold_dir,
        silver_dir=silver_dir,
        context_length=context_length,
        split="validation",
        site_weights=site_weights,
        batch_size=batch_size,
        num_workers=num_workers,
        seed=seed,
        max_buckets=max_buckets,
        shuffle_buffer_size=0,
    )

    run_params = {
        "context_length": context_length,
        "d_model": d_model,
        "n_tcn_blocks": n_tcn_blocks,
        "kernel_size": kernel_size,
        "dilation_base": dilation_base,
        "receptive_field": config.receptive_field(),
        "n_attention_heads": n_attention_heads,
        "dropout": dropout,
        "huber_delta": huber_delta,
        "batch_size": batch_size,
        "lr": lr,
        "max_epochs": max_epochs,
        "n_parameters": model.num_parameters(),
        "variant": "tcn_attention",
    }

    history: list[Dict[str, float]] = []
    with et.start_run(
        run_name,
        seed=seed,
        dataset_version=DATASET_VERSION,
        site="ALL",
        context_length=context_length,
        params=run_params,
    ) as active_run:
        if mlflow_run_id is None:
            mlflow_run_id = active_run.info.run_id
        elif mlflow_run_id != active_run.info.run_id:
            mlflow.set_tag("resumed_from_run_id", mlflow_run_id)

        for epoch in range(start_epoch, max_epochs):
            train_ds.set_epoch(epoch)
            t0 = time.time()
            train_loss, steps = train_one_epoch(
                model, train_loader, optimizer, resolved_device, delta=huber_delta, use_amp=resolved_device.type == "cuda"
            )
            scheduler.step()
            global_step += steps

            val_metrics = evaluate(model, val_loader, resolved_device, td_anom_mean=td_anom_mean, td_anom_std=td_anom_std)
            elapsed = time.time() - t0

            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("val_rmse", val_metrics["rmse"], step=epoch)
            mlflow.log_metric("val_mae", val_metrics["mae"], step=epoch)
            mlflow.log_metric("val_bias", val_metrics["bias"], step=epoch)
            mlflow.log_metric("val_r", val_metrics["r"], step=epoch)
            mlflow.log_metric("val_skill_vs_clim", val_metrics["skill_vs_clim"], step=epoch)
            mlflow.log_metric("epoch_seconds", elapsed, step=epoch)
            if torch.cuda.is_available():
                mlflow.log_metric("gpu_max_memory_mb", torch.cuda.max_memory_allocated() / 1e6, step=epoch)

            history.append({"epoch": epoch, "train_loss": train_loss, **val_metrics})

            config_payload = {**run_params, "seed": seed, "site_weights_path": str(site_weights_path)}
            is_best = val_metrics["skill_vs_clim"] > best_val_skill and np.isfinite(val_metrics["skill_vs_clim"])
            if is_best:
                best_val_skill = val_metrics["skill_vs_clim"]

            ckpt.save_checkpoint(
                ckpt_dir / f"epoch_{epoch:04d}.pt",
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                epoch=epoch,
                global_step=global_step,
                best_val_skill=best_val_skill,
                config=config_payload,
                mlflow_run_id=mlflow_run_id,
            )
            ckpt.save_checkpoint(
                ckpt_dir / "last.pt",
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                epoch=epoch,
                global_step=global_step,
                best_val_skill=best_val_skill,
                config=config_payload,
                mlflow_run_id=mlflow_run_id,
            )
            if is_best:
                ckpt.save_checkpoint(
                    ckpt_dir / "best.pt",
                    model=model,
                    optimizer=optimizer,
                    scheduler=scheduler,
                    epoch=epoch,
                    global_step=global_step,
                    best_val_skill=best_val_skill,
                    config=config_payload,
                    mlflow_run_id=mlflow_run_id,
                )
            mlflow.log_artifact(str(ckpt_dir / "last.pt"))

    return {"history": history, "checkpoint_dir": str(ckpt_dir), "best_val_skill": best_val_skill}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Train TCNAttentionModel for Td(t+1) (bead tdew-x46).")
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--context-length", type=int, default=31, choices=[14, 31, 60])
    p.add_argument("--d-model", type=int, default=64)
    p.add_argument("--n-tcn-blocks", type=int, default=4)
    p.add_argument("--kernel-size", type=int, default=3)
    p.add_argument("--dilation-base", type=int, default=2)
    p.add_argument("--n-attention-heads", type=int, default=4)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--huber-delta", type=float, default=1.0)
    p.add_argument("--batch-size", type=int, default=1024)
    p.add_argument("--num-workers", type=int, default=4)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--max-epochs", type=int, default=30)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--site-weights", type=Path, default=DEFAULT_SITE_WEIGHTS)
    p.add_argument("--norm-stats", type=Path, default=DEFAULT_NORM_STATS)
    p.add_argument("--checkpoint-root", type=Path, default=ckpt.DEFAULT_CHECKPOINT_ROOT)
    p.add_argument("--run-name", type=str, default="week1-tcn-attention")
    p.add_argument("--resume", type=str, default="auto", help="auto|none|<path to .pt>")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--max-buckets", type=int, default=None, help="Smoke-test hook: only use the first N id_buckets.")
    p.add_argument("--device", type=str, default=None, help="cuda|cpu (default: cuda if available)")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run(
        gold_dir=args.gold_dir,
        silver_dir=args.silver_dir,
        context_length=args.context_length,
        d_model=args.d_model,
        n_tcn_blocks=args.n_tcn_blocks,
        kernel_size=args.kernel_size,
        dilation_base=args.dilation_base,
        n_attention_heads=args.n_attention_heads,
        dropout=args.dropout,
        huber_delta=args.huber_delta,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        lr=args.lr,
        max_epochs=args.max_epochs,
        seed=args.seed,
        site_weights_path=args.site_weights,
        norm_stats_path=args.norm_stats,
        checkpoint_root=args.checkpoint_root,
        run_name=args.run_name,
        resume=args.resume,
        overwrite=args.overwrite,
        max_buckets=args.max_buckets,
        device=args.device,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
