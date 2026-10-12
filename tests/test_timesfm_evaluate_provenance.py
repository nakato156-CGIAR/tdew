"""Proveniencia de cada fila de leaderboard.csv: una variante de TimesFM o uno
de los cuatro rivales de Palacios de docs/protocol/timesfm_manifest.yaml."""

from __future__ import annotations

import pytest

from experiments.timesfm.evaluate import RIVAL_PROVENANCE, RIVALS, build_row_provenance
from experiments.timesfm.variants import VARIANTS


def test_rival_provenance_covers_exactly_the_four_rivals():
    assert set(RIVAL_PROVENANCE) == set(RIVALS)


def test_build_row_provenance_for_a_timesfm_variant():
    record = build_row_provenance(
        "timesfm:tmin_anom_full",
        split="ll4",
        cells=1106,
        bead_id="tdew-214",
        panel_id="preds_cribado",
        panel_file="/home/cvelasquez/tdew_timesfm/preds_cribado",
        output_files=("reports/timesfm_benchmark/cribado/leaderboard.csv",),
    )
    assert record.model_family == "timesfm-3.0"
    assert record.variant_label == "tmin_anom_full"
    assert record.trained is False
    assert record.training_period is None
    assert record.test_period == ("2013-01-01", "2016-12-31")
    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True
    assert record.panel_cell_count == 1106


def test_build_row_provenance_for_climatology_rival():
    record = build_row_provenance(
        "climatology", split="ll4", cells=17041, bead_id="tdew-214",
        panel_id="nacional_17041", panel_file="panels/nacional_17041.csv",
        output_files=("reports/timesfm_benchmark/nacional/leaderboard.csv",),
    )
    assert record.model_family == "statistical_baseline"
    assert record.trained is True
    assert record.training_period == ("1981-01-01", "2012-12-31")
    assert record.autoregressive is False
    assert record.climatology_used is True
    assert record.climatology_role == "is_the_method"


def test_build_row_provenance_for_tuned_rival_is_autoregressive_and_trained():
    record = build_row_provenance(
        "tuned", split="ll1", cells=17041, bead_id="tdew-214",
        panel_id="nacional_17041", panel_file="panels/nacional_17041.csv",
        output_files=("reports/timesfm_benchmark/nacional/leaderboard.csv",),
    )
    assert record.trained is True
    assert record.training_period == ("1981-01-01", "2015-12-31")
    assert record.test_period == ("2016-01-01", "2016-12-31")
    assert record.autoregressive is True
    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True


def test_build_row_provenance_for_td_eq_tmin_is_untrained_and_not_autoregressive():
    record = build_row_provenance(
        "td_eq_tmin", split="ll2", cells=1106, bead_id="tdew-214",
        panel_id="cribado_estratificado", panel_file="panels/cribado_estratificado.csv",
        output_files=("reports/timesfm_benchmark/cribado/leaderboard.csv",),
    )
    assert record.trained is False
    assert record.training_period is None
    assert record.autoregressive is False
    assert record.climatology_used is False


def test_build_row_provenance_for_zone_ols_is_trained_and_not_autoregressive():
    record = build_row_provenance(
        "zone_ols", split="ll4", cells=17041, bead_id="tdew-214",
        panel_id="nacional_17041", panel_file="panels/nacional_17041.csv",
        output_files=("reports/timesfm_benchmark/nacional/leaderboard.csv",),
    )
    assert record.trained is True
    assert record.autoregressive is False
    assert record.climatology_used is False


def test_build_row_provenance_rejects_unknown_method():
    with pytest.raises(KeyError):
        build_row_provenance(
            "unknown_method", split="ll4", cells=1, bead_id="tdew-214",
            panel_id="x", panel_file="x.csv", output_files=("x.csv",),
        )


def test_every_variant_reachable_through_timesfm_prefixed_method_name():
    for spec in VARIANTS:
        record = build_row_provenance(
            f"timesfm:{spec.key}", split="ll4", cells=1, bead_id="tdew-214",
            panel_id="x", panel_file="x.csv", output_files=("x.csv",),
        )
        assert record.variant_label == spec.key
