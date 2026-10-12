"""Proveniencia de una corrida de experiments/reconstruction/cli.py: las fechas
de entrenamiento/bloque oculto vienen de la misma ProtocolSpec que
tests/test_reconstruction_manifest_parity.py ya verifica contra el YAML."""

from __future__ import annotations

from experiments.reconstruction.cli import MANIFEST_REF, build_provenance
from experiments.reconstruction.protocol import protocol_spec


def test_build_provenance_direct_mode_is_not_autoregressive():
    record = build_provenance(
        protocol="dev_a", mode="direct", model="ridge",
        variant_label="ridge_exogenous_full_direct", feature_set="exogenous_full",
        seed=0, cells=2048, bead_id="tdew-x46.3", mlflow_run_id="abc123",
        panel_id="dev_a_panel", panel_file="panels/dev_a.csv",
        output_files=("out.parquet", "out.json"),
    )
    assert record.autoregressive is False
    assert record.manifest_ref == MANIFEST_REF


def test_build_provenance_recursive_mode_is_autoregressive():
    record = build_provenance(
        protocol="dev_a", mode="recursive", model="ridge",
        variant_label="ridge_exogenous_full_ar_recursive", feature_set="exogenous_full_ar",
        seed=0, cells=2048, bead_id="tdew-x46.3", mlflow_run_id=None,
        panel_id="dev_a_panel", panel_file=None, output_files=("out.parquet",),
    )
    assert record.autoregressive is True


def test_build_provenance_dates_match_protocol_spec():
    spec = protocol_spec("ll4")
    record = build_provenance(
        protocol="ll4", mode="direct", model="tcn",
        variant_label="tcn_exogenous_full_direct", feature_set="exogenous_full",
        seed=0, cells=8192, bead_id="tdew-x46.3", mlflow_run_id=None,
        panel_id="ll4_panel", panel_file=None, output_files=("out.parquet",),
    )
    assert record.training_period == (
        spec.train_start.date().isoformat(), spec.train_end.date().isoformat(),
    )
    assert record.test_period == (
        spec.hidden_start.date().isoformat(), spec.hidden_end.date().isoformat(),
    )
    assert record.split_id == "ll4"
    assert record.validation_period is None


def test_build_provenance_predicts_anomaly_and_uses_climatology():
    record = build_provenance(
        protocol="dev_b", mode="direct", model="histgb",
        variant_label="histgb_exogenous_full_direct", feature_set="exogenous_full",
        seed=1, cells=512, bead_id="tdew-x46.3", mlflow_run_id=None,
        panel_id="dev_b_panel", panel_file=None, output_files=("out.parquet",),
    )
    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True
    assert record.climatology_role == "target_anomaly_base"
    assert record.trained is True


def test_build_provenance_inference_only_tcn_is_not_trained():
    """tcn_runner.run_tcn's inference_only branch (frozen checkpoint, same
    protocol, no train_steps call) must not claim trained=True."""
    record = build_provenance(
        protocol="ll4", mode="direct", model="tcn",
        variant_label="tcn_exogenous_full_direct", feature_set="exogenous_full",
        seed=0, cells=8192, bead_id="tdew-x46.3", mlflow_run_id=None,
        panel_id="ll4_panel", panel_file=None, output_files=("out.parquet",),
        trained=False,
    )
    assert record.trained is False
    assert record.training_period is None
    # El bloque oculto si se evalua, entrenado o no.
    assert record.test_period is not None


def test_build_provenance_seed_and_model_identity():
    record = build_provenance(
        protocol="dev_a", mode="direct", model="ridge",
        variant_label="ridge_exogenous_full_direct_calibrated", feature_set="exogenous_full",
        seed=7, cells=512, bead_id="tdew-x46.3", mlflow_run_id="run-1",
        panel_id="dev_a_panel", panel_file=None, output_files=("out.parquet",),
    )
    assert record.model_id == "ridge"
    assert record.variant_label == "ridge_exogenous_full_direct_calibrated"
    assert record.seeds == (7,)
    assert record.mlflow_run_id == "run-1"
