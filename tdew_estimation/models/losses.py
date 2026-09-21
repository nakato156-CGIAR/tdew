"""
tdew_estimation.models.losses

Site-weighted Huber loss for TD_anom_norm(t+1) regression.

Huber (SmoothL1) instead of plain MSE: Selva (Loreto/San Martin, ~79% of the
436,519 protocol cells) has more convective/humidity extremes, and Sierra
(Cusco) has thermal-inversion/frost events -- both produce heavier tails in
TD_anom than a Costa-only distribution would. Under MSE those tails would
dominate the batch gradient (error enters squared); Huber caps that
influence to linear beyond ``delta`` while staying quadratic (and smoothly
differentiable) for ordinary residuals. ``delta=1.0`` is not arbitrary here:
TD_anom_norm is a z-score by construction (mean~=0, std=1,
``Data/gold/normalization_stats.json``), so delta=1.0 is literally "one
standard deviation of anomaly" as the quadratic/linear cutover.

Per-sample weighting inherits generalist_mlr's criterion
(``experiments/baselines/train_baselines.py``): ``weight = 1 /
n_train_rows(site)``, so Loreto/Iquitos (~1.2B train rows) cannot dominate
the shared multi-site fit over Lima (~116M rows) by sheer volume.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def weighted_huber_loss(
    pred: torch.Tensor,
    target: torch.Tensor,
    weight: torch.Tensor,
    delta: float = 1.0,
) -> torch.Tensor:
    """pred, target, weight: 1-D tensors of the same length (one value per
    sample in the batch). Returns the scalar
    ``sum(weight * huber(pred, target)) / sum(weight)``."""
    per_sample = F.huber_loss(pred, target, delta=delta, reduction="none")
    weight = weight.to(per_sample.dtype)
    denom = weight.sum().clamp_min(1e-12)
    return (per_sample * weight).sum() / denom
