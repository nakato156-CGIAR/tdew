"""Proveniencia de una corrida de experiments/tcn/train.py (Week1 TCN con
atencion): reutiliza PROVENANCE_COMMON de experiments/tcn/dataset.py, la misma
fuente que la auditoria de ablacion, para no mantener una copia aparte."""

from __future__ import annotations

from experiments.tcn.dataset import PROVENANCE_COMMON
from experiments.tcn.train import TOTAL_CELLS, TRAIN_PERIOD, VALIDATION_PERIOD, build_provenance


def test_build_provenance_reuses_dataset_provenance_common():
    record = build_provenance(
        context_length=31, seed=0, run_name="week1-tcn-attention",
        mlflow_run_id="abc123", bead_id="tdew-x46",
        output_files=("checkpoints/best.pt", "checkpoints/last.pt"),
    )
    assert record.autoregressive == PROVENANCE_COMMON["autoregressive"]
    assert record.target_type == PROVENANCE_COMMON["target_type"]
    assert record.climatology_used == PROVENANCE_COMMON["climatology_used"]
    assert record.climatology_role == PROVENANCE_COMMON["climatology_role"]
    assert record.inputs == PROVENANCE_COMMON["inputs"]
    assert record.manifest_ref == PROVENANCE_COMMON["manifest_ref"]


def test_build_provenance_identifies_context_length_and_seed_in_variant_label():
    record = build_provenance(
        context_length=60, seed=2, run_name="week1-tcn-attention",
        mlflow_run_id=None, bead_id="tdew-x46",
        output_files=("checkpoints/best.pt",),
    )
    assert record.variant_label == "L60_seed2"
    assert record.seeds == (2,)
    assert record.mlflow_run_id is None


def test_build_provenance_only_covers_train_and_validation_not_test():
    record = build_provenance(
        context_length=14, seed=0, run_name="week1-tcn-attention",
        mlflow_run_id="abc", bead_id="tdew-x46", output_files=("x.pt",),
    )
    assert record.trained is True
    assert record.training_period == TRAIN_PERIOD
    assert record.validation_period == VALIDATION_PERIOD
    assert record.test_period is None
    assert record.split_id == "validation"


def test_build_provenance_panel_is_the_pooled_four_departments():
    record = build_provenance(
        context_length=31, seed=0, run_name="week1-tcn-attention",
        mlflow_run_id=None, bead_id="tdew-x46", output_files=("x.pt",),
    )
    assert record.panel_id == "ALL"
    assert record.panel_cell_count == TOTAL_CELLS
    assert record.panel_cell_count == 29079 + 60041 + 305564 + 41835
