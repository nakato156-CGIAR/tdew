"""Unit tests for the two architecture correctives added in bead tdew-x46.1:
``residual_persistence`` (the head predicts the residual over TD_anom_norm(t))
and ``film_identity`` (FiLM as ``(1+gamma)*h + beta``, zero-initialised).

Both default to off, reproducing the behaviour the ``week1-tcn-attention`` run
was trained with; the last test pins that they stay checkpoint-compatible.
"""

from __future__ import annotations

import torch

from tdew_estimation.models.conditioning import FiLMGenerator
from tdew_estimation.models.tcn_attention import TCNAttentionConfig, TCNAttentionModel

PERSISTENCE_IDX = 2  # TD_anom_norm in experiments.tcn.dataset.DYNAMIC_COLS


def _synthetic_batch(config: TCNAttentionConfig, batch_size: int = 8, context_length: int = 31):
    torch.manual_seed(0)
    return (
        torch.randn(batch_size, context_length, config.n_dynamic_features),
        torch.randn(batch_size, config.n_static_features),
        torch.arange(batch_size) % 3,
        torch.randn(batch_size, config.n_target_cond_features),
    )


def test_defaults_are_unchanged():
    config = TCNAttentionConfig()
    assert config.residual_persistence is False
    assert config.film_identity is False
    assert config.persistence_feature_index == PERSISTENCE_IDX


def test_residual_head_starts_exactly_at_persistence():
    config = TCNAttentionConfig(residual_persistence=True, persistence_feature_index=PERSISTENCE_IDX)
    model = TCNAttentionModel(config).eval()
    dynamic, static, region, target_cond = _synthetic_batch(config)
    with torch.no_grad():
        pred = model(dynamic, static, region, target_cond)
    torch.testing.assert_close(pred, dynamic[:, -1, PERSISTENCE_IDX])


def test_residual_head_moves_away_from_persistence_after_one_step():
    """The zero-initialised last layer gives the trunk no gradient on step 0,
    but its own weights do get one -- so the correction must be non-zero from
    the first optimizer step, otherwise the model is frozen at persistence."""
    config = TCNAttentionConfig(residual_persistence=True)
    model = TCNAttentionModel(config)
    dynamic, static, region, target_cond = _synthetic_batch(config)
    target = torch.randn(dynamic.shape[0])
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    loss = torch.nn.functional.mse_loss(model(dynamic, static, region, target_cond), target)
    loss.backward()
    optimizer.step()
    model.eval()
    with torch.no_grad():
        pred = model(dynamic, static, region, target_cond)
    assert not torch.allclose(pred, dynamic[:, -1, PERSISTENCE_IDX])


def test_film_identity_init_leaves_the_pooled_vector_untouched():
    film = FiLMGenerator(d_model=16, identity_init=True)
    static = torch.randn(5, 4)
    region = torch.arange(5) % 3
    gamma, beta = film(static, region)
    assert torch.count_nonzero(gamma) == 0 and torch.count_nonzero(beta) == 0
    h = torch.randn(5, 16)
    torch.testing.assert_close(FiLMGenerator.apply(h, gamma, beta, identity=True), h)
    # The original parameterisation annihilates it instead. That attenuation is
    # real on the trained run (|gamma| averaged 0.120 after 8.5M steps), but the
    # tdew-x46.1 ablation found no accuracy gain from removing it -- this test
    # pins the mechanics, not a claimed cause.
    torch.testing.assert_close(FiLMGenerator.apply(h, gamma, beta), torch.zeros_like(h))


def test_correctives_keep_the_state_dict_compatible():
    """Neither flag may add, drop or resize a parameter: an existing
    week1-tcn-attention checkpoint has to keep loading into the fixed model."""
    plain = TCNAttentionModel(TCNAttentionConfig()).state_dict()
    fixed = TCNAttentionModel(TCNAttentionConfig(residual_persistence=True, film_identity=True))
    assert {k: v.shape for k, v in plain.items()} == {k: v.shape for k, v in fixed.state_dict().items()}
    fixed.load_state_dict(plain)
