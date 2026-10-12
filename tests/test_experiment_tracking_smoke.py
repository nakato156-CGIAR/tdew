"""Smoke test for tdew_estimation.experiment_tracking.

Not a real experiment: just verifies a run opens, gets tagged, and closes
cleanly against a temporary SQLite store. Safe to delete once a real
training script (baselines, TCN, ...) has exercised this path end-to-end.
"""

from __future__ import annotations

import mlflow

from tdew_estimation import experiment_tracking as et


def test_start_run_tags_and_closes(tmp_path):
    tracking_uri = f"sqlite:///{tmp_path / 'mlflow_test.db'}"

    with et.start_run(
        "smoke-test",
        seed=0,
        dataset_version="unit-test",
        site="lima",
        context_length=31,
        params={"method": "climatology"},
        tracking_uri=tracking_uri,
        experiment_name="tdew-week1-smoke",
    ) as run:
        run_id = run.info.run_id
        mlflow.log_metric("dummy_metric", 1.0)

    assert mlflow.active_run() is None

    client = mlflow.tracking.MlflowClient(tracking_uri=tracking_uri)
    finished = client.get_run(run_id)
    assert finished.info.status == "FINISHED"
    assert finished.data.tags["site"] == "lima"
    assert finished.data.tags["context_length"] == "31"
    assert finished.data.tags["seed"] == "0"
    assert "git_commit" in finished.data.tags
    assert finished.data.params["method"] == "climatology"
    assert finished.data.metrics["dummy_metric"] == 1.0
