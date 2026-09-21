"""Unit tests for tdew_estimation.models.attention_pool.QueryPoolingAttention.

Checks the pooled output shape and, critically, that every timestep in the
window actually influences the pooled representation (a non-zero gradient
reaches each input position) -- a dead/ignored lag would silently defeat
the point of adding attention over last-timestep pooling.
"""

from __future__ import annotations

import torch

from tdew_estimation.models.attention_pool import QueryPoolingAttention


def test_output_shape():
    torch.manual_seed(0)
    d_model, n_heads, T, B = 32, 4, 31, 6
    pool = QueryPoolingAttention(d_model, n_heads)
    x = torch.randn(B, T, d_model)
    out = pool(x)
    assert out.shape == (B, d_model)


def test_attention_weights_shape_and_recorded():
    torch.manual_seed(0)
    d_model, n_heads, T, B = 16, 2, 14, 3
    pool = QueryPoolingAttention(d_model, n_heads)
    x = torch.randn(B, T, d_model)
    pool(x)
    assert pool.last_attn_weights is not None
    assert pool.last_attn_weights.shape == (B, T + 1)  # query + T window tokens


def test_gradient_reaches_every_timestep():
    torch.manual_seed(0)
    d_model, n_heads, T, B = 16, 4, 20, 4
    pool = QueryPoolingAttention(d_model, n_heads, dropout=0.0)
    pool.eval()  # dropout off so no timestep is randomly zeroed out of the graph

    x = torch.randn(B, T, d_model, requires_grad=True)
    out = pool(x)
    out.sum().backward()

    assert x.grad is not None
    per_timestep_grad_norm = x.grad.norm(dim=(0, 2))  # [T]
    assert torch.all(per_timestep_grad_norm > 0), "some timestep received zero gradient (dead position)"
