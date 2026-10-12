"""Proveniencia de los cinco metodos de reports/week1_baselines/leaderboard.csv.

Todos menos climatology predicen TD_anom_target y suman TD_clim_target
(ver predict_all_methods); climatology ES TD_clim_target directamente."""

from __future__ import annotations

from experiments.baselines.train_baselines import (
    DEPT_FEATURES,
    GENERALIST_FEATURES,
    METHOD_PROVENANCE,
    TEST_PERIOD,
    TRAIN_PERIOD,
    VALIDATION_PERIOD,
    build_method_provenance,
)


def test_method_provenance_has_all_five_methods():
    assert set(METHOD_PROVENANCE) == {
        "climatology", "persistence", "dept_ols", "dept_mlr", "generalist_mlr",
    }


def test_only_climatology_is_raw_target_the_rest_are_anomaly():
    assert METHOD_PROVENANCE["climatology"]["target_type"] == "td_raw"
    for method in ("persistence", "dept_ols", "dept_mlr", "generalist_mlr"):
        assert METHOD_PROVENANCE[method]["target_type"] == "td_anomaly"
        assert METHOD_PROVENANCE[method]["climatology_used"] is True


def test_only_persistence_and_climatology_are_untrained():
    assert METHOD_PROVENANCE["climatology"]["trained"] is True  # train-only clim stats
    assert METHOD_PROVENANCE["persistence"]["trained"] is False
    for method in ("dept_ols", "dept_mlr", "generalist_mlr"):
        assert METHOD_PROVENANCE[method]["trained"] is True


def test_no_method_is_autoregressive():
    """Cada fila es un pronostico a un paso (X_{<=t} -> Td(t+1)) evaluado con
    entradas observadas, no una recursion que realimente su propia prediccion."""
    for meta in METHOD_PROVENANCE.values():
        assert meta["autoregressive"] is False


def test_dept_mlr_inputs_match_the_actual_design_matrix_columns():
    assert METHOD_PROVENANCE["dept_mlr"]["inputs"] == tuple(DEPT_FEATURES)


def test_generalist_mlr_inputs_match_the_actual_design_matrix_columns():
    assert METHOD_PROVENANCE["generalist_mlr"]["inputs"] == tuple(GENERALIST_FEATURES)


def test_build_method_provenance_for_a_single_site():
    record = build_method_provenance(
        "lima", "dept_mlr", cells=29079, bead_id="tdew-x46",
        output_files=("reports/week1_baselines/leaderboard.csv",),
    )
    assert record.variant_label == "dept_mlr@lima"
    assert record.training_period == TRAIN_PERIOD
    assert record.validation_period == VALIDATION_PERIOD
    assert record.test_period == TEST_PERIOD
    assert record.panel_id == "lima"
    assert record.panel_cell_count == 29079
    assert record.panel_file == "Data/silver/department_grid_ids/lima.csv"


def test_build_method_provenance_for_pooled_all_has_no_panel_file():
    record = build_method_provenance(
        "ALL", "climatology", cells=436519, bead_id="tdew-x46",
        output_files=("reports/week1_baselines/leaderboard.csv",),
    )
    assert record.panel_id == "ALL"
    assert record.panel_file is None
    assert record.training_period == TRAIN_PERIOD


def test_build_method_provenance_untrained_persistence_has_no_training_period():
    record = build_method_provenance(
        "cusco", "persistence", cells=60041, bead_id="tdew-x46",
        output_files=("reports/week1_baselines/leaderboard.csv",),
    )
    assert record.trained is False
    assert record.training_period is None
