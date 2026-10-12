"""Tests for tdew_estimation.provenance: the MetricProvenance schema and the
shared record_metric_provenance/load_registry helpers."""

from __future__ import annotations

import json

import pytest

from tdew_estimation import provenance as prov


def _base_kwargs(**overrides) -> dict:
    kwargs = dict(
        run_id="run-1",
        generated_at="2026-09-24T00:00:00+00:00",
        git_commit="deadbeef",
        bead_id="tdew-z39",
        manifest_ref="docs/protocol/timesfm_manifest.yaml@2026-09-22",
        model_family="foundation_model",
        model_id="timesfm:3.0",
        variant_label="tmin_td_full",
        trained=False,
        training_period=None,
        validation_period=None,
        test_period=("2013-01-01", "2016-12-31"),
        split_id="ll4",
        autoregressive=False,
        target_type="td_anomaly",
        climatology_used=True,
        climatology_role="input_covariate",
        inputs=("Tmin_anom",),
        panel_id="nacional_17041",
        panel_cell_count=17041,
        panel_file="reports/timesfm_benchmark/panels/nacional_17041.csv",
        output_files=("reports/timesfm_benchmark/nacional/metrics.csv",),
    )
    kwargs.update(overrides)
    return kwargs


def test_valid_record_constructs():
    record = prov.MetricProvenance(**_base_kwargs())
    assert record.model_id == "timesfm:3.0"
    assert record.seeds == ()
    assert record.mlflow_run_id is None


def test_rejects_unknown_target_type():
    with pytest.raises(ValueError, match="target_type"):
        prov.MetricProvenance(**_base_kwargs(target_type="td_kelvin"))


def test_rejects_training_period_when_not_trained():
    with pytest.raises(ValueError, match="training_period"):
        prov.MetricProvenance(
            **_base_kwargs(trained=False, training_period=("1981-01-01", "2012-12-31"))
        )


def test_rejects_climatology_role_when_climatology_unused():
    with pytest.raises(ValueError, match="climatology_role"):
        prov.MetricProvenance(
            **_base_kwargs(climatology_used=False, climatology_role="input_covariate")
        )


def test_rejects_negative_panel_cell_count():
    with pytest.raises(ValueError, match="panel_cell_count"):
        prov.MetricProvenance(**_base_kwargs(panel_cell_count=-1))


def test_rejects_empty_output_files():
    with pytest.raises(ValueError, match="output_files"):
        prov.MetricProvenance(**_base_kwargs(output_files=()))


def test_record_metric_provenance_appends_registry_and_writes_sidecar(tmp_path):
    output_file = "reports/example/metrics.csv"
    (tmp_path / "reports/example").mkdir(parents=True)
    (tmp_path / output_file).write_text("method,rmse\nclimatology,1.53\n")

    registry_path = tmp_path / "reports" / "metric_provenance.jsonl"
    record = prov.MetricProvenance(**_base_kwargs(output_files=(output_file,)))

    prov.record_metric_provenance(record, registry_path=registry_path, repo_root=tmp_path)

    rows = prov.load_registry(registry_path)
    assert len(rows) == 1
    assert rows[0]["run_id"] == "run-1"
    assert rows[0]["output_files"] == [output_file]

    sidecar_path = tmp_path / "reports/example/metrics.csv.provenance.json"
    sidecar = json.loads(sidecar_path.read_text())
    assert sidecar["model_id"] == "timesfm:3.0"


def test_record_metric_provenance_appends_multiple_runs(tmp_path):
    output_file = "reports/example/metrics.csv"
    (tmp_path / "reports/example").mkdir(parents=True)
    registry_path = tmp_path / "reports" / "metric_provenance.jsonl"

    first = prov.MetricProvenance(**_base_kwargs(run_id="run-1", output_files=(output_file,)))
    second = prov.MetricProvenance(**_base_kwargs(run_id="run-2", output_files=(output_file,)))
    prov.record_metric_provenance(first, registry_path=registry_path, repo_root=tmp_path)
    prov.record_metric_provenance(second, registry_path=registry_path, repo_root=tmp_path)

    rows = prov.load_registry(registry_path)
    assert [row["run_id"] for row in rows] == ["run-1", "run-2"]


def test_load_registry_missing_file_returns_empty_list(tmp_path):
    assert prov.load_registry(tmp_path / "does_not_exist.jsonl") == []


def test_new_run_id_and_now_iso_are_distinct():
    assert prov.new_run_id() != prov.new_run_id()
    assert "T" in prov.now_iso()


def test_git_commit_matches_experiment_tracking():
    from tdew_estimation import experiment_tracking as et

    assert prov.git_commit() == et._git_commit()
