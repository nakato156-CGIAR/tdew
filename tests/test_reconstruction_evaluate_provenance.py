"""Proveniencia por (model, fold) en experiments/reconstruction/evaluate.py.

A diferencia de cli.py, este archivo agrega predicciones ya generadas por otras
corridas y no conoce su feature_set -- solo el protocolo (por fold) y si el
modelo es autorregresivo, deducible de su nombre."""

from __future__ import annotations

import pytest

from experiments.reconstruction.evaluate import (
    UnknownAutoregressiveStatus,
    build_model_fold_provenance,
)
from experiments.reconstruction.protocol import protocol_spec


def test_tuned_is_autoregressive():
    record = build_model_fold_provenance(
        "tuned", "ll4", cells=8192, bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.autoregressive is True


def test_recursive_suffixed_model_is_autoregressive():
    record = build_model_fold_provenance(
        "ridge_exogenous_full_ar_recursive", "dev_a", cells=512,
        bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.autoregressive is True


def test_direct_model_is_not_autoregressive():
    record = build_model_fold_provenance(
        "ridge_exogenous_full_direct", "dev_a", cells=512,
        bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.autoregressive is False


def test_dates_come_from_the_protocol_spec_for_the_given_fold():
    spec = protocol_spec("dev_b")
    record = build_model_fold_provenance(
        "histgb_exogenous_full_direct", "dev_b", cells=512,
        bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.training_period == (
        spec.train_start.date().isoformat(), spec.train_end.date().isoformat(),
    )
    assert record.test_period == (
        spec.hidden_start.date().isoformat(), spec.hidden_end.date().isoformat(),
    )
    assert record.split_id == "dev_b"


def test_target_is_anomaly_and_uses_climatology():
    record = build_model_fold_provenance(
        "tuned", "ll4", cells=8192, bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True


def test_notes_flag_that_feature_set_is_not_known_here():
    record = build_model_fold_provenance(
        "tuned", "ll4", cells=8192, bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.inputs == ()
    assert record.notes is not None and "cli" in record.notes


def test_manifest_alias_with_no_direct_recursive_suffix_is_not_guessed():
    """ridge_full/histgb_full are the kind of manifest-chosen aliases in
    docs/protocol/reconstruction_predictions.example.yaml that don't preserve
    cli.py's naming convention -- classifying them must fail loudly, not
    silently default to non-autoregressive."""
    with pytest.raises(UnknownAutoregressiveStatus):
        build_model_fold_provenance(
            "ridge_full", "ll4", cells=8192, bead_id="tdew-x46.3",
            output_files=("metrics.parquet",),
        )


def test_manifest_alias_is_classifiable_via_explicit_override():
    record = build_model_fold_provenance(
        "ridge_full", "ll4", cells=8192, bead_id="tdew-x46.3",
        output_files=("metrics.parquet",),
        autoregressive_overrides={"ridge_full": True},
    )
    assert record.autoregressive is True


def test_seed_is_appended_to_variant_label_when_given():
    with_seed = build_model_fold_provenance(
        "tcn_direct", "ll4", cells=8192, bead_id="tdew-214",
        output_files=("metrics.parquet",), seed=2,
    )
    without_seed = build_model_fold_provenance(
        "tcn_direct", "ll4", cells=8192, bead_id="tdew-214",
        output_files=("metrics.parquet",),
    )
    assert with_seed.variant_label == "tcn_direct_seed2"
    assert with_seed.seeds == (2,)
    assert without_seed.variant_label == "tcn_direct"
    assert without_seed.seeds == ()


def test_panel_id_defaults_to_fold_but_can_be_overridden():
    default_panel = build_model_fold_provenance(
        "tuned", "ll4", cells=8192, bead_id="tdew-214", output_files=("metrics.parquet",),
    )
    custom_panel = build_model_fold_provenance(
        "tuned", "ll4", cells=8192, bead_id="tdew-214", output_files=("metrics.parquet",),
        panel_id="departamental",
    )
    assert default_panel.panel_id == "ll4"
    assert custom_panel.panel_id == "departamental"


def test_calibrated_recursive_model_still_classifies_as_autoregressive():
    """cli.py appends "_calibrated" after the mode suffix for shrinkage-
    corrected predictions; the _calibrated suffix must not hide "_recursive"."""
    record = build_model_fold_provenance(
        "ridge_exogenous_full_ar_recursive_calibrated", "dev_a", cells=512,
        bead_id="tdew-x46.3", output_files=("metrics.parquet",),
    )
    assert record.autoregressive is True
