"""
tdew_estimation.models.attention_pool

Single "compact" self-attention layer that pools a TCN-encoded window
``[B, T, d_model]`` into one summary vector ``[B, d_model]``, via a learned
query token (CLS-style) prepended to the sequence and refined by one
``nn.MultiheadAttention`` + FFN block (pre-LayerNorm residual).

Why a learned query instead of last-timestep or mean pooling: the whole
point of adding attention is letting the model re-weight which lags matter
most for Td(t+1) (the deep analogue of dept_mlr/generalist_mlr's per-lag
regression coefficients) -- taking only the TCN's last hidden state would
discard that; mean-pooling would weight every lag equally, which the
baselines already showed is wrong (their coefficients differ by lag).

No leakage from bidirectional attention: every position fed into this layer
comes from the TCN encoder over ``X_{t-L+1:t}``, which is always <= t by
construction of the training-data window (``pipeline/sequences.py``
eligibility, ``docs/protocol/week1_manifest.yaml`` leakage_constraint).
Bidirectional attention *inside* that window never sees t+1.
"""

from __future__ import annotations

import torch
from torch import nn


class QueryPoolingAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, ffn_mult: int = 4, dropout: float = 0.1):
        super().__init__()
        self.query = nn.Parameter(torch.zeros(1, 1, d_model))
        nn.init.normal_(self.query, std=0.02)
        self.attn = nn.MultiheadAttention(d_model, n_heads, dropout=dropout, batch_first=True)
        self.norm_attn = nn.LayerNorm(d_model)
        self.norm_ffn = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, ffn_mult * d_model),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ffn_mult * d_model, d_model),
        )
        self.dropout = nn.Dropout(dropout)
        # Populated on forward(); [B, T+1] attention the pooled query paid to
        # itself + every window position -- kept for tdew-bs4 error analysis
        # (which lags the model actually leans on), not used in training.
        self.last_attn_weights: torch.Tensor | None = None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, d_model]
        batch_size = x.shape[0]
        query = self.query.expand(batch_size, -1, -1)  # [B, 1, d_model]
        tokens = torch.cat([query, x], dim=1)  # [B, T+1, d_model]

        normed = self.norm_attn(tokens)
        attn_out, attn_weights = self.attn(normed, normed, normed, need_weights=True, average_attn_weights=True)
        tokens = tokens + self.dropout(attn_out)

        pooled = tokens[:, 0, :]  # [B, d_model] -- the query's slot
        pooled = pooled + self.dropout(self.ffn(self.norm_ffn(pooled)))

        self.last_attn_weights = attn_weights[:, 0, :].detach()  # [B, T+1]
        return pooled
