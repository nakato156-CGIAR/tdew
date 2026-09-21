"""Unit tests for tdew_estimation.models.losses.weighted_huber_loss."""

from __future__ import annotations

import math

import torch

from tdew_estimation.models.losses import weighted_huber_loss


def _manual_huber(e: float, delta: float) -> float:
    if abs(e) <= delta:
        return 0.5 * e * e
    return delta * (abs(e) - 0.5 * delta)


def test_matches_manual_formula_uniform_weights():
    pred = torch.tensor([0.0, 2.0, -3.0, 0.5])
    target = torch.tensor([0.0, 0.0, 0.0, 0.0])
    weight = torch.ones_like(pred)
    delta = 1.0

    got = weighted_huber_loss(pred, target, weight, delta=delta).item()
    manual = sum(_manual_huber(p - t, delta) for p, t in zip(pred.tolist(), target.tolist())) / len(pred)
    assert math.isclose(got, manual, rel_tol=1e-6)


def test_weighting_matches_manual_weighted_average():
    pred = torch.tensor([0.0, 5.0])
    target = torch.tensor([0.0, 0.0])
    weight = torch.tensor([1.0, 3.0])
    delta = 1.0

    got = weighted_huber_loss(pred, target, weight, delta=delta).item()
    h0 = _manual_huber(0.0, delta)
    h1 = _manual_huber(5.0, delta)
    manual = (1.0 * h0 + 3.0 * h1) / (1.0 + 3.0)
    assert math.isclose(got, manual, rel_tol=1e-6)


def test_boundary_at_delta_is_continuous():
    delta = 1.0
    pred = torch.tensor([delta - 1e-4, delta + 1e-4])
    target = torch.tensor([0.0, 0.0])
    weight = torch.ones_like(pred)
    # Just below/above delta, the loss should be close to 0.5*delta^2, with no jump.
    per_sample_loss = torch.nn.functional.huber_loss(pred, target, delta=delta, reduction="none")
    assert torch.allclose(per_sample_loss, torch.full_like(per_sample_loss, 0.5 * delta**2), atol=1e-3)


def test_zero_weight_row_does_not_error():
    pred = torch.tensor([0.0, 10.0])
    target = torch.tensor([0.0, 0.0])
    weight = torch.tensor([1.0, 0.0])
    loss = weighted_huber_loss(pred, target, weight, delta=1.0)
    assert torch.isfinite(loss)
    assert math.isclose(loss.item(), 0.0, abs_tol=1e-6)  # only the zero-error, zero-weight-excluded row counts
