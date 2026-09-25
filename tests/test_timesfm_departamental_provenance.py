"""departamental.py junta modelos con nombres 'bare' (climatology, timesfm)
que experiments.reconstruction.evaluate._is_autoregressive no puede
clasificar por su nombre -- _LOCAL_AUTOREGRESSIVE_OVERRIDES debe resolverlos
explicitamente, no dejar que caigan en la excepcion."""

from __future__ import annotations

from experiments.reconstruction.evaluate import (
    UnknownAutoregressiveStatus,
    build_model_fold_provenance,
)
from experiments.timesfm.departamental import _LOCAL_AUTOREGRESSIVE_OVERRIDES

import pytest


def test_local_overrides_cover_climatology_and_bare_timesfm():
    assert _LOCAL_AUTOREGRESSIVE_OVERRIDES == {"climatology": False, "timesfm": False}


def test_climatology_and_timesfm_are_classifiable_with_the_override():
    for model in ("climatology", "timesfm"):
        record = build_model_fold_provenance(
            model, "ll4", cells=8192, bead_id="tdew-214",
            output_files=("metrics.csv",),
            autoregressive_overrides=_LOCAL_AUTOREGRESSIVE_OVERRIDES,
        )
        assert record.autoregressive is False


def test_climatology_and_timesfm_are_unclassifiable_without_the_override():
    """Confirma que el override realmente hace falta -- sin el, evaluate.py
    los rechazaria (correctamente, no puede adivinarlos por el nombre)."""
    for model in ("climatology", "timesfm"):
        with pytest.raises(UnknownAutoregressiveStatus):
            build_model_fold_provenance(
                model, "ll4", cells=8192, bead_id="tdew-214", output_files=("metrics.csv",),
            )


def test_tuned_and_direct_suffixed_models_do_not_need_the_override():
    for model in ("tuned", "tcn_direct"):
        record = build_model_fold_provenance(
            model, "ll4", cells=8192, bead_id="tdew-214", output_files=("metrics.csv",),
            autoregressive_overrides=_LOCAL_AUTOREGRESSIVE_OVERRIDES,
        )
        assert record.autoregressive == (model == "tuned")
