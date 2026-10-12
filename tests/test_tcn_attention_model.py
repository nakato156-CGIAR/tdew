"""Unit tests for tdew_estimation.models.tcn_attention.TCNAttentionModel.

Pure-mechanics smoke tests on synthetic tensors -- no real Data/gold is
touched here (see the tcn-attention design plan, bead tdew-x46: this
session is architecture + code + mechanics tests only, no training against
real data yet).
"""

from __future__ import annotations

import pytest
import torch

from tdew_estimation.models.tcn_attention import TCNAttentionConfig, TCNAttentionModel, invert_to_physical

FROZEN_LENGTHS = (14, 31, 60)  # docs/protocol/week1_manifest.yaml context_lengths_L


def _synthetic_batch(config: TCNAttentionConfig, batch_size: int, context_length: int):
    torch.manual_seed(0)
    dynamic = torch.randn(batch_size, context_length, config.n_dynamic_features)
    static = torch.randn(batch_size, config.n_static_features)
    # Make sure all three natural regions (Costa=0, Sierra=1, Selva=2) appear
    # at least once, so the region embedding gets a gradient from every row.
    region = torch.arange(batch_size) % 3
    target_cond = torch.randn(batch_size, config.n_target_cond_features)
    return dynamic, static, region, target_cond


def test_forward_shape_for_every_frozen_context_length():
    config = TCNAttentionConfig()  # defaults: d_model=64, n_tcn_blocks=4 -> RF=61, covers all 3 lengths
    model = TCNAttentionModel(config)
    for L in FROZEN_LENGTHS:
        dynamic, static, region, target_cond = _synthetic_batch(config, batch_size=6, context_length=L)
        pred = model(dynamic, static, region, target_cond)
        assert pred.shape == (6,)
        assert torch.isfinite(pred).all()


def test_receptive_field_covers_frozen_lengths():
    config = TCNAttentionConfig()
    assert config.receptive_field() == 61
    for L in FROZEN_LENGTHS:
        assert config.receptive_field() >= L


def test_parameter_count_is_compact():
    model = TCNAttentionModel()
    n_params = model.num_parameters()
    # Design estimate (tcn-attention plan): ~157K. Guard against accidental
    # architecture bloat while leaving room for minor tweaks.
    assert 50_000 < n_params < 500_000, f"unexpected parameter count: {n_params}"


def test_gradients_are_finite_and_flow_to_every_submodule():
    config = TCNAttentionConfig(d_model=16, n_tcn_blocks=3, n_attention_heads=2)  # RF=29, covers L=14 only
    model = TCNAttentionModel(config)
    dynamic, static, region, target_cond = _synthetic_batch(config, batch_size=8, context_length=14)

    pred = model(dynamic, static, region, target_cond)
    target = torch.randn_like(pred)
    loss = torch.nn.functional.mse_loss(pred, target)
    loss.backward()

    for name, param in model.named_parameters():
        assert param.grad is not None, f"{name} received no gradient"
        assert torch.isfinite(param.grad).all(), f"{name} has non-finite gradient"


def test_invert_to_physical_matches_pred_plus_clim_pattern():
    pred_norm = torch.tensor([0.0, 1.0, -2.0])
    mean, std = 0.1, 2.0
    td_clim = torch.tensor([20.0, 20.0, 20.0])
    out = invert_to_physical(pred_norm, mean, std, td_clim)
    expected = pred_norm * std + mean + td_clim
    assert torch.allclose(out, expected)


def test_config_defaults_are_frozen_and_hashable():
    # TCNAttentionConfig is a frozen dataclass so it is safe to reuse/log as
    # an MLflow param dict and to construct model instances repeatably.
    config = TCNAttentionConfig()
    with pytest.raises(Exception):
        config.d_model = 128  # type: ignore[misc]
