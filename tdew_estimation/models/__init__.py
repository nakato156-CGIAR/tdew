"""tdew_estimation.models

Shared deep-sequence-model architectures for the Semana 1 deep-learning
ladder (bead tdew-x46 TCN today; tdew-2s6 GRU / tdew-efi Transformer later
reuse the building blocks in ``tcn_blocks``/``attention_pool``/
``conditioning``/``losses`` where useful). See the tcn-attention design plan
(bead tdew-x46, plan file ``adaptive-leaping-summit.md``) for the full
architecture rationale.
"""

from tdew_estimation.models.tcn_attention import (
    TCNAttentionConfig,
    TCNAttentionModel,
    invert_to_physical,
)
from tdew_estimation.models.tcn_blocks import receptive_field, validate_receptive_field

__all__ = [
    "TCNAttentionConfig",
    "TCNAttentionModel",
    "invert_to_physical",
    "receptive_field",
    "validate_receptive_field",
]
