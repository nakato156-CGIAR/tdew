"""PROVENANCE_COMMON in experiments/tcn/ablation_x46_1.py must keep matching
the frozen feature list in docs/protocol/week1_manifest.yaml -- same parity
guard pattern as tests/test_reconstruction_manifest_parity.py."""

from __future__ import annotations

from pathlib import Path

import yaml

from experiments.tcn.ablation_x46_1 import PROVENANCE_COMMON, VARIANTS, build_provenance
from experiments.tcn.train import TOTAL_CELLS, TRAIN_PERIOD, VALIDATION_PERIOD

MANIFEST_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "protocol" / "week1_manifest.yaml"
)


def test_provenance_common_inputs_match_week1_manifest():
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert list(PROVENANCE_COMMON["inputs"]) == manifest["features"]["inputs"]


def test_provenance_common_is_not_autoregressive():
    assert PROVENANCE_COMMON["autoregressive"] is False


def test_provenance_common_target_type_matches_the_actual_label_column():
    """LABEL_COL/DYNAMIC_COLS en dataset.py son anomalias climatologicas
    normalizadas, no Td cruda -- PROVENANCE_COMMON debe reflejar eso aunque el
    contrato del manifiesto hable de Td(t+1) en grados, porque invert_to_physical
    solo suma la climatologia de vuelta al reportar, no al entrenar/predecir."""
    from experiments.tcn.dataset import DYNAMIC_COLS, LABEL_COL

    assert LABEL_COL.endswith("_anom_norm")
    assert all(col.endswith("_anom_norm") or col in ("sin_doy", "cos_doy") for col in DYNAMIC_COLS)
    assert PROVENANCE_COMMON["target_type"] == "td_anomaly"
    assert PROVENANCE_COMMON["climatology_used"] is True
    assert PROVENANCE_COMMON["climatology_role"] is not None


def test_all_four_ablation_variants_are_declared():
    assert set(VARIANTS) == {"current", "residual", "residual+film", "residual+film+uniform"}


def test_build_provenance_reuses_train_py_constants_for_the_pooled_panel():
    """La ablacion evalua sobre la misma submuestra validacion pooled que
    experiments.tcn.train -- no debe redeclarar TOTAL_CELLS/TRAIN_PERIOD por
    su cuenta."""
    record = build_provenance(
        variant="residual+film", context_length=31, seed=0, bead_id="tdew-x46.1",
        mlflow_run_id="run-1", output_files=("ablation_summary.csv", "ablation_history.csv"),
    )
    assert record.panel_cell_count == TOTAL_CELLS
    assert record.training_period == TRAIN_PERIOD
    assert record.validation_period == VALIDATION_PERIOD
    assert record.variant_label == "residual+film_L31_seed0"
    assert record.mlflow_run_id == "run-1"
    assert record.autoregressive == PROVENANCE_COMMON["autoregressive"]
    assert record.target_type == PROVENANCE_COMMON["target_type"]
