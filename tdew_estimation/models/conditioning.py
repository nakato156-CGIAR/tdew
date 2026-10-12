"""
tdew_estimation.models.conditioning

Site conditioning (FiLM: feature-wise linear modulation) from per-cell
static covariates (DEM/TDI/X/Y) plus a natural-region embedding
(Costa/Sierra/Selva), applied once to the attention-pooled window summary.

Why FiLM, applied once (not per TCN block, not a plain concat): the site is
constant across the whole window (DEM/TDI/X/Y/region never change between
t-L+1 and t), so there is no reason to re-modulate every TCN block with it
-- that would multiply the FiLM MLP's cost fourfold for no benefit. FiLM at
the single point where the window collapses to one vector is the deep,
non-linear analogue of generalist_mlr's explicit
``region_natural x lag_feature`` interaction terms
(``experiments/baselines/train_baselines.py``): it lets the site *modulate*
the learned window representation instead of only adding to it.
"""

from __future__ import annotations

import torch
from torch import nn

# docs/protocol/week1_manifest.yaml sites.departments[].region_natural
# (0=Costa, 1=Sierra, 2=Selva) -- same encoding the training dataset/CLI use.
N_REGIONS = 3


class FiLMGenerator(nn.Module):
    def __init__(
        self,
        d_model: int,
        n_static: int = 4,
        region_embed_dim: int = 8,
        hidden: int = 32,
        identity_init: bool = False,
    ):
        super().__init__()
        self.d_model = d_model
        self.region_embedding = nn.Embedding(N_REGIONS, region_embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(n_static + region_embed_dim, hidden),
            nn.GELU(),
            nn.Linear(hidden, 2 * d_model),
        )
        if identity_init:
            # Pairs with apply(..., identity=True): zeroing the last layer makes
            # gamma=beta=0, so the modulation starts as (1+0)*h+0 == h, instead
            # of annihilating h. On the trained week1-tcn-attention checkpoint
            # the plain gamma*h+beta form left |gamma| averaging 0.120 after
            # 8.5M steps; switching to this parameterisation did not improve
            # validation RMSE in the tdew-x46.1 ablation
            # (reports/week1_tcn_ablation/), so the attenuation is a real
            # measurement but not a demonstrated cause of the deficit.
            nn.init.zeros_(self.mlp[-1].weight)
            nn.init.zeros_(self.mlp[-1].bias)

    def forward(self, static: torch.Tensor, region: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """static: [B, n_static] float; region: [B] long in [0, N_REGIONS).
        Returns (gamma, beta), each [B, d_model]."""
        region_emb = self.region_embedding(region)
        gamma_beta = self.mlp(torch.cat([static, region_emb], dim=-1))
        gamma, beta = gamma_beta.split(self.d_model, dim=-1)
        return gamma, beta

    @staticmethod
    def apply(h: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, identity: bool = False) -> torch.Tensor:
        """``identity=True`` uses the ``(1+gamma)*h + beta`` parameterisation
        (Perez et al. 2018's usual implementation form), so that gamma=0 leaves
        ``h`` untouched instead of annihilating it."""
        if identity:
            return (1.0 + gamma) * h + beta
        return gamma * h + beta
