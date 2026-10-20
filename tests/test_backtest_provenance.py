"""Provenance for the four-method ladder HPC_code_tunning/backtest.py produces
(climatology, td_eq_tmin, zone_ols, tuned) -- the same dict/helper that
experiments/timesfm/evaluate.py imports for its rival rows, so a change here
must not silently break that import."""

from __future__ import annotations

import pytest

from HPC_code_tunning.backtest import RIVAL_PROVENANCE, SPLITS, build_rival_provenance


def test_rival_provenance_has_exactly_the_four_ladder_methods():
    assert set(RIVAL_PROVENANCE) == {"climatology", "td_eq_tmin", "zone_ols", "tuned"}


def test_only_tuned_is_autoregressive():
    assert RIVAL_PROVENANCE["tuned"]["autoregressive"] is True
    for method in ("climatology", "td_eq_tmin", "zone_ols"):
        assert RIVAL_PROVENANCE[method]["autoregressive"] is False


def test_tuned_predicts_in_anomaly_space():
    """feature_spec.py fixes TARGET_COL='TD_anom' and forecast_zoned.py
    reconstructs the physical value only at the end (`acc + td_clim[d]`) --
    'tuned' leans on climatology exactly like a TimesFM TD_anom variant does,
    so it must be coded the same way, not as target_type='td_raw'."""
    from HPC_code_tunning.feature_spec import TARGET_COL

    assert TARGET_COL == "TD_anom"
    assert RIVAL_PROVENANCE["tuned"]["target_type"] == "td_anomaly"
    assert RIVAL_PROVENANCE["tuned"]["climatology_used"] is True
    assert RIVAL_PROVENANCE["tuned"]["climatology_role"] == "target_anomaly_base"


def test_td_eq_tmin_is_the_only_untrained_method():
    assert RIVAL_PROVENANCE["td_eq_tmin"]["trained"] is False
    for method in ("climatology", "zone_ols", "tuned"):
        assert RIVAL_PROVENANCE[method]["trained"] is True


def test_build_rival_provenance_derives_training_period_from_splits():
    record = build_rival_provenance(
        "zone_ols", split="ll1", cells=8192, bead_id="tdew-214",
        manifest_ref="PAPER_PLAN.md#5,9", panel_id="buckets_n64_seed0",
        panel_file=None, output_files=("predictions.parquet", "metrics.csv"),
    )
    train_end_year, holdout_years = SPLITS["ll1"]
    assert record.training_period == ("1981-01-01", f"{train_end_year}-12-31")
    assert record.test_period == (f"{holdout_years[0]}-01-01", f"{holdout_years[1]}-12-31")
    assert record.panel_file is None


def test_build_rival_provenance_untrained_method_has_no_training_period():
    record = build_rival_provenance(
        "td_eq_tmin", split="ll4", cells=17041, bead_id="tdew-214",
        manifest_ref="docs/protocol/timesfm_manifest.yaml@2026-09-22",
        panel_id="nacional_17041", panel_file="panels/nacional_17041.csv",
        output_files=("predictions.parquet",),
    )
    assert record.trained is False
    assert record.training_period is None


def test_build_rival_provenance_rejects_unknown_method():
    with pytest.raises(KeyError):
        build_rival_provenance(
            "not_a_method", split="ll4", cells=1, bead_id="tdew-214",
            manifest_ref="x", panel_id="x", panel_file=None, output_files=("x",),
        )


# --- tdew-f6a: inputs/autoregressive of `tuned` follow the manifest really used ---------

from HPC_code_tunning.backtest import manifest_feature_names, tuned_inputs_from_features  # noqa: E402
from HPC_code_tunning.feature_spec import DEFAULT_CANDIDATE_POOL  # noqa: E402

_SIN_TD = ("const", "TMIN_anom", "TMIN_anom_lag1", "TMIN_anom_lag2", "TMIN_anom_lag7", "TMIN_anom_lag30")


def _tuned(**kw):
    return build_rival_provenance(
        "tuned", split="ll4b", cells=10, bead_id="tdew-f6a", manifest_ref="x",
        panel_id="buckets_n64_seed0", panel_file=None, output_files=("predictions.parquet",), **kw,
    )


def test_default_pool_reproduces_the_static_tuned_record():
    inputs, autoregressive = tuned_inputs_from_features(DEFAULT_CANDIDATE_POOL)
    assert inputs == RIVAL_PROVENANCE["tuned"]["inputs"]
    assert autoregressive is RIVAL_PROVENANCE["tuned"]["autoregressive"]


def test_without_tuned_features_the_record_is_unchanged():
    record = _tuned()
    assert record.inputs == ("TMIN_anom", "TD_anom_lag")
    assert record.autoregressive is True


def test_pool_without_td_lags_is_not_autoregressive():
    record = _tuned(tuned_features=_SIN_TD)
    assert record.inputs == ("TMIN_anom",)
    assert record.autoregressive is False
    # the shared dict must not be mutated by the override
    assert RIVAL_PROVENANCE["tuned"]["inputs"] == ("TMIN_anom", "TD_anom_lag")
    assert RIVAL_PROVENANCE["tuned"]["autoregressive"] is True


def test_manifest_feature_names_is_the_union_of_feature_lists():
    import pandas as pd

    manifest = pd.DataFrame({
        "feature_list": ["const,TMIN_anom,TMIN_anom_lag1", "const,TMIN_anom,TMIN_anom_lag30"],
    })
    names = manifest_feature_names(manifest)
    assert names == ("TMIN_anom", "TMIN_anom_lag1", "TMIN_anom_lag30", "const")
    assert tuned_inputs_from_features(names) == (("TMIN_anom",), False)


def test_other_methods_ignore_tuned_features():
    record = build_rival_provenance(
        "zone_ols", split="ll4", cells=1, bead_id="x", manifest_ref="x", panel_id="x",
        panel_file=None, output_files=("x",), tuned_features=_SIN_TD,
    )
    assert record.inputs == ("TMIN",)
    assert record.autoregressive is False
