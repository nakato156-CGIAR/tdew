"""Unit tests for tdew_estimation.models.tcn_blocks.

Verifies the receptive-field formula against hand computation, that the
configuration used by TCNAttentionModel covers all three frozen context
lengths L in {14, 31, 60} (docs/protocol/week1_manifest.yaml), that
validate_receptive_field raises for an undersized config, and that
TCNEncoder is truly causal (output at position t never depends on input at
positions > t) -- the leak-safety property bead tdew-x46 explicitly asks to
verify.
"""

from __future__ import annotations

import pytest
import torch

from tdew_estimation.models.tcn_blocks import TCNEncoder, receptive_field, validate_receptive_field

FROZEN_LENGTHS = (14, 31, 60)  # docs/protocol/week1_manifest.yaml context_lengths_L


@pytest.mark.parametrize(
    "kernel_size,n_blocks,dilation_base,expected",
    [
        (3, 1, 2, 5),
        (3, 2, 2, 13),
        (3, 3, 2, 29),
        (3, 4, 2, 61),
        (3, 5, 2, 125),
        (5, 2, 2, 25),  # RF = 1 + 2*4*(2^2-1) = 1+8*3=25
        (3, 3, 1, 13),  # dilation_base=1 (no growth): RF = 1 + 2*2*3 = 13
    ],
)
def test_receptive_field_matches_hand_computation(kernel_size, n_blocks, dilation_base, expected):
    assert receptive_field(kernel_size, n_blocks, dilation_base) == expected


def test_default_tcn_attention_config_covers_all_frozen_lengths():
    # kernel_size=3, n_blocks=4, dilation_base=2 -> RF=61 (TCNAttentionConfig defaults).
    rf = receptive_field(kernel_size=3, n_blocks=4, dilation_base=2)
    assert rf == 61
    for length in FROZEN_LENGTHS:
        assert rf >= length, f"RF={rf} does not cover L={length}"


def test_validate_receptive_field_raises_when_undersized():
    # n_blocks=3 -> RF=29, does not cover L=60.
    with pytest.raises(ValueError, match="receptive_field"):
        validate_receptive_field(context_length=60, kernel_size=3, n_blocks=3, dilation_base=2)
    # But does cover L=14.
    assert validate_receptive_field(context_length=14, kernel_size=3, n_blocks=3, dilation_base=2) == 29


def test_tcn_encoder_output_shape():
    torch.manual_seed(0)
    d_model, n_blocks, T, B = 16, 4, 31, 5
    encoder = TCNEncoder(d_model, n_blocks)
    x = torch.randn(B, T, d_model)
    y = encoder(x)
    assert y.shape == (B, T, d_model)


def test_tcn_encoder_is_causal():
    """Perturbing the input strictly after position t must not change the
    output at position t (docs/protocol/week1_manifest.yaml
    leakage_constraint, applied at the layer level)."""
    torch.manual_seed(0)
    d_model, n_blocks, T, B = 8, 3, 20, 4
    encoder = TCNEncoder(d_model, n_blocks)
    encoder.eval()  # disable dropout so the comparison is exact

    x = torch.randn(B, T, d_model)
    cutoff = 10  # positions 0..cutoff must be unaffected by changes to cutoff+1..T-1

    x_perturbed = x.clone()
    x_perturbed[:, cutoff + 1 :, :] = torch.randn(B, T - cutoff - 1, d_model)

    with torch.no_grad():
        y_original = encoder(x)
        y_perturbed = encoder(x_perturbed)

    assert torch.allclose(y_original[:, : cutoff + 1, :], y_perturbed[:, : cutoff + 1, :], atol=1e-6)
    # Sanity: the perturbation actually changes something at/after the cutoff+1 position,
    # otherwise the test would pass vacuously.
    assert not torch.allclose(y_original[:, cutoff + 1 :, :], y_perturbed[:, cutoff + 1 :, :])
