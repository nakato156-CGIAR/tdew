"""
experiments.tcn.checkpoint

Save/load/resume for TCN training. See the tcn-attention design plan (bead
tdew-x46) for the rationale: no ``GradScaler`` state (bf16 autocast needs
none, unlike fp16), and RNG state is saved so resuming reproduces the same
training trajectory bit-for-bit from the point of interruption.

Layout: ``experiments/tcn/checkpoints/{run_name}_L{L}_seed{seed}/``, holding
``epoch_NNNN.pt`` (one per epoch), ``last.pt`` (always overwritten, used by
``--resume auto``) and ``best.pt`` (best ``val_skill_vs_clim`` seen so far).
``L``/``seed`` are part of the directory name because each ``L`` is a
distinct training run for the tdew-bs4 ablation, not a checkpoint shared
across L's.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHECKPOINT_ROOT = Path(__file__).resolve().parent / "checkpoints"


def checkpoint_dir(run_name: str, context_length: int, seed: int, root: Path = DEFAULT_CHECKPOINT_ROOT) -> Path:
    return root / f"{run_name}_L{context_length}_seed{seed}"


def capture_rng_state() -> Dict[str, Any]:
    state = {
        "torch": torch.get_rng_state(),
        "numpy": np.random.get_state(),
        "python": random.getstate(),
    }
    if torch.cuda.is_available():
        state["torch_cuda"] = torch.cuda.get_rng_state_all()
    return state


def restore_rng_state(state: Dict[str, Any]) -> None:
    torch.set_rng_state(state["torch"])
    np.random.set_state(state["numpy"])
    random.setstate(state["python"])
    if torch.cuda.is_available() and "torch_cuda" in state:
        torch.cuda.set_rng_state_all(state["torch_cuda"])


def save_checkpoint(
    path: Path,
    *,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: Optional[Any],
    epoch: int,
    global_step: int,
    best_val_skill: float,
    config: Dict[str, Any],
    mlflow_run_id: Optional[str] = None,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict() if scheduler is not None else None,
        "epoch": epoch,
        "global_step": global_step,
        "best_val_skill": best_val_skill,
        "rng_state": capture_rng_state(),
        "config": config,
        "mlflow_run_id": mlflow_run_id,
    }
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    torch.save(payload, tmp_path)
    tmp_path.replace(path)


def load_checkpoint(path: Path, *, map_location: str = "cpu") -> Dict[str, Any]:
    """Always maps tensors to CPU by default (not just the model/optimizer
    state, but also the CPU-only RNG state tensor torch.get_rng_state()
    always produces): torch.load's map_location applies indiscriminately to
    every tensor in the pickle, and remapping the RNG state to CUDA breaks
    torch.set_rng_state (it requires a CPU ByteTensor). model.load_state_dict
    / optimizer.load_state_dict both copy CPU state into GPU
    parameters/state correctly on their own, so there is no need to place
    this checkpoint on CUDA up front."""
    return torch.load(Path(path), map_location=map_location, weights_only=False)


def restore_into(
    checkpoint: Dict[str, Any],
    *,
    model: torch.nn.Module,
    optimizer: Optional[torch.optim.Optimizer] = None,
    scheduler: Optional[Any] = None,
    restore_rng: bool = True,
) -> None:
    model.load_state_dict(checkpoint["model_state_dict"])
    if optimizer is not None and checkpoint.get("optimizer_state_dict") is not None:
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    if scheduler is not None and checkpoint.get("scheduler_state_dict") is not None:
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
    if restore_rng and checkpoint.get("rng_state") is not None:
        restore_rng_state(checkpoint["rng_state"])


def resolve_resume_path(resume: str, ckpt_dir: Path) -> Optional[Path]:
    """``resume`` is 'auto' (use last.pt if present, else start fresh),
    'none' (never resume), or an explicit path to a checkpoint file."""
    if resume == "none":
        return None
    if resume == "auto":
        last_path = ckpt_dir / "last.pt"
        return last_path if last_path.exists() else None
    explicit = Path(resume)
    if not explicit.exists():
        raise FileNotFoundError(f"--resume path not found: {explicit}")
    return explicit
