"""TCN variants and differentiable closed-loop training primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import torch
from torch import nn

from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel

from .data import AR_LAGS


@dataclass(frozen=True)
class ReconstructionTCNConfig:
    n_dynamic_features: int
    n_static_features: int
    n_target_features: int
    autoregressive: bool = False
    d_model: int = 64
    n_tcn_blocks: int = 4
    kernel_size: int = 3
    dilation_base: int = 2
    n_attention_heads: int = 4
    dropout: float = 0.1


def build_tcn(config: ReconstructionTCNConfig) -> TCNAttentionModel:
    n_target = config.n_target_features + (len(AR_LAGS) if config.autoregressive else 0)
    base = TCNAttentionConfig(
        n_dynamic_features=config.n_dynamic_features,
        n_static_features=config.n_static_features,
        n_target_cond_features=n_target,
        d_model=config.d_model,
        n_tcn_blocks=config.n_tcn_blocks,
        kernel_size=config.kernel_size,
        dilation_base=config.dilation_base,
        n_attention_heads=config.n_attention_heads,
        dropout=config.dropout,
        residual_persistence=False,
    )
    return TCNAttentionModel(base)


def closed_rollout(
    model: nn.Module,
    dynamic_windows: torch.Tensor,
    static: torch.Tensor,
    region: torch.Tensor,
    target_cond: torch.Tensor,
    initial_td_history: torch.Tensor,
    *,
    lags: Sequence[int] = AR_LAGS,
) -> torch.Tensor:
    """Differentiably predict H consecutive days using predicted TD feedback.

    Shapes are dynamic_windows [B,H,L,F], static [B,S], region [B],
    target_cond [B,H,C], initial_td_history [B,max(lags)]. Returned shape is
    [B,H]. No observed target tensor is accepted, making teacher forcing
    inside the rollout impossible by construction.
    """
    if dynamic_windows.ndim != 4 or target_cond.ndim != 3 or initial_td_history.ndim != 2:
        raise ValueError("Invalid tensor ranks for closed rollout")
    if initial_td_history.shape[1] < max(lags):
        raise ValueError(f"initial_td_history needs at least {max(lags)} values")
    horizon = dynamic_windows.shape[1]
    if target_cond.shape[1] != horizon:
        raise ValueError("dynamic_windows and target_cond horizons differ")
    history = initial_td_history
    outputs = []
    for step in range(horizon):
        lag_values = torch.stack([history[:, -lag] for lag in lags], dim=1)
        conditioning = torch.cat([target_cond[:, step], lag_values], dim=1)
        prediction = model(dynamic_windows[:, step], static, region, conditioning)
        outputs.append(prediction)
        history = torch.cat([history, prediction[:, None]], dim=1)
    return torch.stack(outputs, dim=1)


def rollout_loss(predictions: torch.Tensor, targets: torch.Tensor, *, objective: str = "mse") -> torch.Tensor:
    if predictions.shape != targets.shape:
        raise ValueError("Predictions and targets must have identical shapes")
    if objective == "mse":
        return torch.mean((predictions - targets) ** 2)
    if objective == "huber":
        return torch.nn.functional.huber_loss(predictions, targets, delta=1.0)
    raise ValueError("objective must be 'mse' or 'huber'")


def allowed_context_lengths(short_screen_results: dict[int, tuple[float, float]]) -> tuple[int, ...]:
    """Enforce the gate for screening L=31/60 after L=7 vs L=14.

    Values are the two internal-fold RMSEs. L=31 and L=60 are permitted only
    when L=14 strictly improves L=7 in both folds.
    """
    base = (3, 7, 14)
    if 7 not in short_screen_results or 14 not in short_screen_results:
        return base
    seven, fourteen = short_screen_results[7], short_screen_results[14]
    if len(seven) != 2 or len(fourteen) != 2:
        raise ValueError("Each context length must contain exactly two fold RMSEs")
    return base + (31, 60) if all(a < b for a, b in zip(fourteen, seven)) else base
