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
    # --- correctives under test in bead tdew-x46.1 (both default to the
    # behaviour the week1-tcn-attention run was trained with, so an existing
    # checkpoint still loads: neither flag adds, removes or renames a
    # parameter) ---
    # Predict the residual over persistence instead of the level: the head's
    # output is added to TD_anom_norm(t), and the head's last layer is
    # zero-initialised, so an untrained model IS persistence exactly.
    #
    # What it buys, per the tdew-x46.1 ablation
    # (reports/week1_tcn_ablation/): a floor, not accuracy. At init the pooled
    # validation RMSE is 0.9200 (persistence) instead of 1.3138, but at the
    # best point of an 8,000-step run the difference against the plain head is
    # 0.8542 vs 0.8593 -- inside the spread. The hypothesis that the model
    # underperformed because it lacked this identity path was NOT confirmed.
    residual_persistence: bool = False
    # Index of TD_anom_norm inside the dynamic feature axis
    # (experiments.tcn.dataset.DYNAMIC_COLS).
    persistence_feature_index: int = 2
    # FiLM as (1+gamma)*h + beta with a zero-initialised generator, i.e.
    # starting at the identity -- see FiLMGenerator. Also measured in the
    # tdew-x46.1 ablation and also without a measurable effect on accuracy
    # (0.8588 against 0.8542 without it, at the same best point).
    film_identity: bool = False

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
        self.film = FiLMGenerator(
            c.d_model, c.n_static_features, c.region_embed_dim, c.film_hidden, identity_init=c.film_identity
        )
        head_in = c.d_model + c.n_target_cond_features
        self.head = nn.Sequential(
            nn.Linear(head_in, c.head_hidden),
            nn.GELU(),
            nn.Dropout(c.dropout),
            nn.Linear(c.head_hidden, 1),
        )
        if c.residual_persistence:
            # Zero-init the last head layer so the correction starts at exactly
            # 0 and the model's initial prediction is persistence. The trunk
            # receives no gradient on the very first step (dout/dhidden == W ==
            # 0), but the layer's own weights do, so it becomes non-zero
            # immediately -- the same zero-init-the-residual-branch trick as in
            # He et al.'s ResNet recipe.
            nn.init.zeros_(self.head[-1].weight)
            nn.init.zeros_(self.head[-1].bias)

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
        pooled = FiLMGenerator.apply(pooled, gamma, beta, identity=self.config.film_identity)

        combined = torch.cat([pooled, target_cond], dim=-1)  # [B, d_model + n_target_cond_features]
        pred_norm = self.head(combined).squeeze(-1)  # [B]
        if self.config.residual_persistence:
            pred_norm = pred_norm + dynamic[:, -1, self.config.persistence_feature_index]
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
