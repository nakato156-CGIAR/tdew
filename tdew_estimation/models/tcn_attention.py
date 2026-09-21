"""
tdew_estimation.models.tcn_attention

``TCNAttentionModel``: causal dilated TCN backbone + single attention-pool
layer + FiLM site conditioning + target-day conditioning + regression head,
predicting ``TD_anom_norm(t+1)``. This is the "TCN con attention" variant of
bead tdew-x46 (a "sin attention" variant is planned for a later session --
see the bead's notes and the tcn-attention design plan,
``adaptive-leaping-summit.md``, for the full architecture rationale).

Input contract (one window per sample, ``X_{t-L+1:t} -> Td(t+1)``,
``docs/protocol/week1_manifest.yaml``):

- ``dynamic``     [B, T, 5]  TMIN_anom_norm, TMAX_anom_norm, TD_anom_norm,
                              sin_doy, cos_doy for t-L+1..t.
- ``static``      [B, 4]     DEM_norm, TDI_norm, X_norm, Y_norm (constant
                              per cell).
- ``region``      [B]        0=Costa, 1=Sierra, 2=Selva.
- ``target_cond`` [B, 4]     sin_doy(t+1), cos_doy(t+1), LST_DAY_norm(t+1),
                              LST_NIGHT_norm(t+1) -- known ahead of time,
                              never a leakage source (same role as
                              dept_mlr/generalist_mlr's target-day
                              seasonal/LST regressors).

Output: ``pred_norm`` [B], predicted ``TD_anom_norm(t+1)``. Use
``invert_to_physical`` to turn that into degrees C for scoring against
``reports/week1_baselines/leaderboard.csv`` with
``tdew_estimation.metrics`` unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
from torch import nn

from tdew_estimation.models.attention_pool import QueryPoolingAttention
from tdew_estimation.models.conditioning import FiLMGenerator
from tdew_estimation.models.tcn_blocks import TCNEncoder, receptive_field


@dataclass(frozen=True)
class TCNAttentionConfig:
    n_dynamic_features: int = 5  # TMIN_anom_norm, TMAX_anom_norm, TD_anom_norm, sin_doy, cos_doy
    n_static_features: int = 4  # DEM_norm, TDI_norm, X_norm, Y_norm
    n_target_cond_features: int = 4  # sin_doy(t+1), cos_doy(t+1), LST_DAY_norm(t+1), LST_NIGHT_norm(t+1)
    d_model: int = 64
    n_tcn_blocks: int = 4
    kernel_size: int = 3
    dilation_base: int = 2
    n_attention_heads: int = 4
    region_embed_dim: int = 8
    film_hidden: int = 32
    head_hidden: int = 32
    dropout: float = 0.1

    def receptive_field(self) -> int:
        return receptive_field(self.kernel_size, self.n_tcn_blocks, self.dilation_base)


class TCNAttentionModel(nn.Module):
    def __init__(self, config: Optional[TCNAttentionConfig] = None):
        super().__init__()
        self.config = config or TCNAttentionConfig()
        c = self.config

        self.input_proj = nn.Linear(c.n_dynamic_features, c.d_model)
        self.tcn = TCNEncoder(
            c.d_model, c.n_tcn_blocks, kernel_size=c.kernel_size, dilation_base=c.dilation_base, dropout=c.dropout
        )
        self.attention_pool = QueryPoolingAttention(c.d_model, c.n_attention_heads, dropout=c.dropout)
        self.film = FiLMGenerator(c.d_model, c.n_static_features, c.region_embed_dim, c.film_hidden)
        head_in = c.d_model + c.n_target_cond_features
        self.head = nn.Sequential(
            nn.Linear(head_in, c.head_hidden),
            nn.GELU(),
            nn.Dropout(c.dropout),
            nn.Linear(c.head_hidden, 1),
        )

    @property
    def receptive_field(self) -> int:
        return self.tcn.receptive_field

    def num_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def forward(
        self,
        dynamic: torch.Tensor,
        static: torch.Tensor,
        region: torch.Tensor,
        target_cond: torch.Tensor,
    ) -> torch.Tensor:
        h = self.input_proj(dynamic)  # [B, T, d_model]
        h = self.tcn(h)  # [B, T, d_model]
        pooled = self.attention_pool(h)  # [B, d_model]

        gamma, beta = self.film(static, region)
        pooled = FiLMGenerator.apply(pooled, gamma, beta)

        combined = torch.cat([pooled, target_cond], dim=-1)  # [B, d_model + n_target_cond_features]
        pred_norm = self.head(combined).squeeze(-1)  # [B]
        return pred_norm


def invert_to_physical(
    pred_norm: torch.Tensor,
    td_anom_mean: float,
    td_anom_std: float,
    td_clim_target: torch.Tensor,
) -> torch.Tensor:
    """Invert TD_anom_norm(t+1) predictions to TD(t+1) in degrees C:
    ``TD_pred = pred_norm * std + mean + TD_clim(t+1)`` -- the same
    ``pred + clim`` pattern ``train_baselines.py::predict_from_coefs`` uses,
    so ``tdew_estimation.metrics`` scores TCN and baseline predictions on
    identical footing."""
    td_anom_pred = pred_norm * td_anom_std + td_anom_mean
    return td_anom_pred + td_clim_target
