"""Step-based TCN training with intra-epoch validation and exact checkpoints."""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Iterator

import mlflow
import numpy as np
import torch

from experiments.tcn import checkpoint as ckpt
from tdew_estimation.metrics import MetricsAccum

from .tcn import closed_rollout, rollout_loss


def _infinite(loader: Iterable[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    while True:
        emitted = False
        for batch in loader:
            emitted = True
            yield batch
        if not emitted:
            raise ValueError("Training loader produced no batches")


def _device_batch(batch: dict[str, Any], device: torch.device) -> dict[str, Any]:
    return {key: value.to(device) if torch.is_tensor(value) else value for key, value in batch.items()}


def _predict(model: torch.nn.Module, batch: dict[str, Any], mode: str) -> torch.Tensor:
    if mode == "direct":
        return model(batch["dynamic"].float(), batch["static"].float(), batch["region"], batch["target_cond"].float())
    if mode == "recursive":
        return closed_rollout(
            model,
            batch["dynamic_windows"].float(),
            batch["static"].float(),
            batch["region"],
            batch["target_cond"].float(),
            batch["initial_td_history"].float(),
        )
    raise ValueError("mode must be direct or recursive")


@torch.no_grad()
def evaluate_loader(
    model: torch.nn.Module,
    loader: Iterable[dict[str, Any]],
    device: torch.device,
    *,
    mode: str,
) -> dict[str, dict[str, float]]:
    model.eval()
    accumulators: dict[str, MetricsAccum] = defaultdict(MetricsAccum)
    for raw_batch in loader:
        batch = _device_batch(raw_batch, device)
        prediction = _predict(model, batch, mode)
        target = batch["label"]
        departments = raw_batch["department"]
        pred_np = prediction.detach().cpu().numpy()
        target_np = target.detach().cpu().numpy()
        if pred_np.ndim == 2:
            pred_np = pred_np.reshape(len(pred_np), -1)
            target_np = target_np.reshape(len(target_np), -1)
        accumulators["ALL"].add(pred_np.ravel(), target_np.ravel())
        for index, department in enumerate(departments):
            accumulators[str(department)].add(np.asarray(pred_np[index]).ravel(), np.asarray(target_np[index]).ravel())
    return {department: accumulator.finalize() for department, accumulator in accumulators.items()}


def train_steps(
    model: torch.nn.Module,
    train_loader: Iterable[dict[str, Any]],
    validation_loader: Iterable[dict[str, Any]],
    *,
    optimizer: torch.optim.Optimizer,
    checkpoint_dir: Path,
    config: dict[str, Any],
    mode: str,
    device: torch.device,
    max_steps: int = 20_000,
    eval_every: int = 1_000,
    patience: int = 5,
    min_delta: float = 0.002,
    objective: str = "mse",
    resume: str = "auto",
    training_eval_loader: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Train until max_steps or five validations without 0.002 C improvement."""
    checkpoint_dir = Path(checkpoint_dir)
    start_step = 0
    best_rmse = math.inf
    evaluations_without_improvement = 0
    resume_path = ckpt.resolve_resume_path(resume, checkpoint_dir)
    if resume_path is not None:
        payload = ckpt.load_checkpoint(resume_path)
        ckpt.restore_into(payload, model=model, optimizer=optimizer)
        start_step = int(payload["global_step"])
        best_rmse = -float(payload["best_val_skill"])
        evaluations_without_improvement = int(payload.get("config", {}).get("evaluations_without_improvement", 0))
        if start_step >= max_steps:
            raise ValueError(
                f"{resume_path} is already at step {start_step}, which is not below max_steps={max_steps}; "
                "resuming would train nothing and score the earlier run's weights"
            )

    model.to(device)
    iterator = _infinite(train_loader)
    # Deterministic samplers restart at batch zero. Advancing to the recorded
    # position makes the first resumed update consume the same next batch.
    for _ in range(start_step):
        next(iterator)
    history = []
    for step in range(start_step + 1, max_steps + 1):
        model.train()
        batch = _device_batch(next(iterator), device)
        optimizer.zero_grad(set_to_none=True)
        prediction = _predict(model, batch, mode)
        loss = rollout_loss(prediction, batch["label"].float(), objective=objective)
        loss.backward()
        optimizer.step()
        if mlflow.active_run() is not None:
            mlflow.log_metric("train_loss", float(loss.item()), step=step)

        if step % eval_every != 0 and step != max_steps:
            continue
        metrics = evaluate_loader(model, validation_loader, device, mode=mode)
        train_metrics = (
            evaluate_loader(model, training_eval_loader, device, mode=mode)
            if training_eval_loader is not None
            else {}
        )
        rmse = float(metrics["ALL"]["rmse"])
        improved = rmse <= best_rmse - min_delta
        if improved:
            best_rmse = rmse
            evaluations_without_improvement = 0
        else:
            evaluations_without_improvement += 1
        history.append({"step": step, "validation_metrics": metrics, "training_metrics": train_metrics})
        if mlflow.active_run() is not None:
            for split, split_metrics in (("val", metrics), ("train", train_metrics)):
                for department, values in split_metrics.items():
                    for name, value in values.items():
                        if np.isfinite(value):
                            mlflow.log_metric(f"{split}_{department}_{name}", float(value), step=step)
        payload_config = {
            **config,
            "mode": mode,
            "objective": objective,
            "evaluations_without_improvement": evaluations_without_improvement,
        }
        for path in (checkpoint_dir / f"eval_{step:06d}.pt", checkpoint_dir / "last.pt"):
            ckpt.save_checkpoint(
                path, model=model, optimizer=optimizer, scheduler=None, epoch=0,
                global_step=step, best_val_skill=-best_rmse, config=payload_config,
            )
        if improved:
            ckpt.save_checkpoint(
                checkpoint_dir / "best.pt", model=model, optimizer=optimizer,
                scheduler=None, epoch=0, global_step=step,
                best_val_skill=-best_rmse, config=payload_config,
            )
        if evaluations_without_improvement >= patience:
            break
    return {"best_rmse": best_rmse, "history": history, "last_step": history[-1]["step"] if history else start_step}


def train_fixed_steps(
    model: torch.nn.Module,
    train_loader: Iterable[dict[str, Any]],
    *,
    optimizer: torch.optim.Optimizer,
    checkpoint_dir: Path,
    config: dict[str, Any],
    mode: str,
    device: torch.device,
    max_steps: int,
    checkpoint_every: int = 1000,
    objective: str = "mse",
    resume: str = "auto",
) -> Path:
    """Refit a frozen configuration without reading the hidden block."""
    checkpoint_dir = Path(checkpoint_dir)
    start_step = 0
    resume_path = ckpt.resolve_resume_path(resume, checkpoint_dir)
    if resume_path is not None:
        payload = ckpt.load_checkpoint(resume_path)
        ckpt.restore_into(payload, model=model, optimizer=optimizer)
        start_step = int(payload["global_step"])
    model.to(device)
    iterator = _infinite(train_loader)
    for _ in range(start_step):
        next(iterator)
    for step in range(start_step + 1, max_steps + 1):
        model.train()
        batch = _device_batch(next(iterator), device)
        optimizer.zero_grad(set_to_none=True)
        prediction = _predict(model, batch, mode)
        loss = rollout_loss(prediction, batch["label"].float(), objective=objective)
        loss.backward()
        optimizer.step()
        if mlflow.active_run() is not None:
            mlflow.log_metric("train_loss", float(loss.item()), step=step)
        if step % checkpoint_every == 0 or step == max_steps:
            ckpt.save_checkpoint(
                checkpoint_dir / "last.pt", model=model, optimizer=optimizer,
                scheduler=None, epoch=0, global_step=step,
                best_val_skill=float("nan"),
                config={**config, "mode": mode, "objective": objective, "fixed_refit": True},
            )
    final = checkpoint_dir / "final.pt"
    ckpt.save_checkpoint(
        final, model=model, optimizer=optimizer, scheduler=None, epoch=0,
        global_step=max_steps, best_val_skill=float("nan"),
        config={**config, "mode": mode, "objective": objective, "fixed_refit": True},
    )
    return final
