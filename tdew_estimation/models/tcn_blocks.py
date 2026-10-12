"""
tdew_estimation.models.tcn_blocks

Causal dilated residual TCN backbone (Bai et al. 2018, WaveNet-residual
style), shared building block for the Semana 1 deep-learning ladder (bead
tdew-x46: TCN+attention today).

Frozen context lengths this must cover: L in {14, 31, 60}
(``docs/protocol/week1_manifest.yaml``, amended 2026-09-17 from {14,30,60}
in bead tdew-ztn.3). The tcn-attention design plan (bead tdew-x46) fixes the
TCN depth (n_blocks) so its receptive field covers the LARGEST L with one
architecture reused across all three L runs -- this isolates the L ablation
(bead tdew-bs4, "select best L by validation") from model capacity, instead
of giving each L a differently-sized model.
"""

from __future__ import annotations

import torch
from torch import nn


def receptive_field(kernel_size: int, n_blocks: int, dilation_base: int = 2) -> int:
    """Receptive field of a stack of ``n_blocks`` residual TCN blocks, each
    with 2 causal convolutions of kernel ``kernel_size`` at the same
    dilation ``dilation_base ** i`` (i = 0..n_blocks-1)::

        RF = 1 + 2*(kernel_size-1) * sum_{i=0}^{n_blocks-1} dilation_base**i
           = 1 + 2*(kernel_size-1) * (dilation_base**n_blocks - 1) / (dilation_base - 1)

    With the design's defaults (kernel_size=3, dilation_base=2, n_blocks=4):
    RF=61, which covers L=60 (the largest frozen context length) with margin.
    """
    if kernel_size < 1 or n_blocks < 1 or dilation_base < 1:
        raise ValueError("kernel_size, n_blocks, dilation_base must all be >= 1")
    if dilation_base == 1:
        dilation_sum = n_blocks
    else:
        dilation_sum = (dilation_base**n_blocks - 1) // (dilation_base - 1)
    return 1 + 2 * (kernel_size - 1) * dilation_sum


def validate_receptive_field(context_length: int, kernel_size: int, n_blocks: int, dilation_base: int = 2) -> int:
    """Raise if the TCN configured by (kernel_size, n_blocks, dilation_base)
    cannot see the full ``context_length``-day window; otherwise return the
    receptive field. This is the explicit check bead tdew-x46 requires
    ("verificar que el receptive field cubra cada L")."""
    rf = receptive_field(kernel_size, n_blocks, dilation_base)
    if rf < context_length:
        raise ValueError(
            f"receptive_field={rf} < context_length={context_length} "
            f"(kernel_size={kernel_size}, n_blocks={n_blocks}, dilation_base={dilation_base}); "
            "increase n_blocks (or kernel_size) to cover the full window."
        )
    return rf


class CausalConv1d(nn.Module):
    """1D convolution, left-padded so ``output[..., t]`` depends only on
    ``input[..., <=t]`` -- never on future positions."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, dilation: int):
        super().__init__()
        self.left_pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, dilation=dilation, padding=0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, T]
        x = nn.functional.pad(x, (self.left_pad, 0))
        return self.conv(x)


class TemporalBlock(nn.Module):
    """One residual TCN block: two (pre-LayerNorm -> causal conv -> GELU ->
    dropout) stages at the same dilation, identity residual connection. All
    blocks operate in ``d_model`` channels in and out (the input projection
    upstream already maps raw features to ``d_model``), so no 1x1 projection
    is needed on the residual path."""

    def __init__(self, d_model: int, kernel_size: int, dilation: int, dropout: float = 0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.conv1 = CausalConv1d(d_model, d_model, kernel_size, dilation)
        self.norm2 = nn.LayerNorm(d_model)
        self.conv2 = CausalConv1d(d_model, d_model, kernel_size, dilation)
        self.act = nn.GELU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, d_model]
        residual = x
        h = self.norm1(x).transpose(1, 2)  # [B, d_model, T]
        h = self.dropout(self.act(self.conv1(h)))
        h = h.transpose(1, 2)  # [B, T, d_model]
        h = self.norm2(h).transpose(1, 2)
        h = self.dropout(self.act(self.conv2(h)))
        h = h.transpose(1, 2)
        return residual + h


class TCNEncoder(nn.Module):
    """Stack of ``n_blocks`` ``TemporalBlock``s with dilation
    ``dilation_base ** i`` for block ``i``. Input/output shape ``[B, T,
    d_model]`` throughout (channel-last, matches the rest of this package's
    tensors)."""

    def __init__(
        self,
        d_model: int,
        n_blocks: int,
        kernel_size: int = 3,
        dilation_base: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.blocks = nn.ModuleList(
            [TemporalBlock(d_model, kernel_size, dilation_base**i, dropout=dropout) for i in range(n_blocks)]
        )
        self.receptive_field = receptive_field(kernel_size, n_blocks, dilation_base)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for block in self.blocks:
            x = block(x)
        return x
