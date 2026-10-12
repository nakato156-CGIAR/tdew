"""Proveniencia y MLflow del producto TimesFM 2017-2020 (tdew-214.13)."""

from __future__ import annotations

import json

import numpy as np
import pytest

from experiments.timesfm import real
from tdew_estimation import provenance as prov


def _record(tmp_path, n=2178827):
    return real.build_real_provenance(
        n_cells=n, ids_file=tmp_path / "ids_real_2178827.csv", out_dir=tmp_path / "preds_real",
        future_root=tmp_path / "future", bead_id="tdew-214.13",
    )


def test_record_declares_real_split_without_observed_truth(tmp_path):
    rec = _record(tmp_path)
    assert rec.split_id == "real_2017_2020"
    assert rec.panel_id == "real_2178827_td"
    assert rec.panel_cell_count == 2178827
    assert rec.test_period == ("2017-01-01", "2020-12-31")
    assert rec.trained is False and rec.training_period is None
    # TimesFM decodifica el horizonte de una pasada (timesfm3 model.decode), igual que en ll1-ll4.
    assert rec.autoregressive is False
    assert rec.variant_label == "tmin_anom_full"
    assert rec.manifest_ref == real.MANIFEST_REF_REAL
    assert rec.manifest_ref.endswith("timesfm_manifest_addendum_real_2017_2020.yaml")
    assert str(tmp_path / "preds_real") in rec.output_files
    assert rec.bead_id == "tdew-214.13"


def test_notes_record_license_tf32_positive_and_no_truth(tmp_path):
    notes = _record(tmp_path).notes
    for fragment in ("sin verdad observada", "no comercial", "TF32", "make_positive=False",
                     "timesfm", "future_tmin"):
        assert fragment in notes, fragment


def test_panel_id_follows_the_cells_actually_requested(tmp_path):
    rec = _record(tmp_path, n=531)
    assert rec.panel_id == "real_531_td" and rec.panel_cell_count == 531


def test_record_is_appended_to_registry(tmp_path):
    registry = tmp_path / "registry.jsonl"
    rec = _record(tmp_path)
    prov.record_metric_provenance(rec, registry_path=registry, repo_root=tmp_path)
    prov.record_metric_provenance(_record(tmp_path, n=5), registry_path=registry, repo_root=tmp_path)
    rows = [json.loads(x) for x in registry.read_text().splitlines()]
    assert len(rows) == 2 and rows[0]["panel_cell_count"] == 2178827


def test_mlflow_run_logs_throughput_and_size_metrics(tmp_path):
    import mlflow

    uri = f"sqlite:///{tmp_path / 'mlflow.db'}"
    summary = {
        "buckets_total": 2, "cells_written": 531, "cells_omitted": 0, "rows": 775791,
        "bytes": 35_000_000, "seconds": 120.0, "cells_per_second": 4.4,
        "quantile_violation_rows": 0, "bytes_per_row": 45.1,
    }
    run_id = real.log_mlflow(summary, tracking_uri=uri, experiment_name="test-real",
                             run_name="smoke", params={"split": "real", "bead_id": "tdew-214.13"})
    run = mlflow.tracking.MlflowClient(uri).get_run(run_id)
    assert run.data.metrics["cells_written"] == 531
    assert run.data.metrics["bytes_per_row"] == pytest.approx(45.1)
    assert run.data.params["split"] == "real"
    assert run.info.status == "FINISHED"


def test_notes_follow_the_tf32_setting(tmp_path):
    on = real.build_real_provenance(n_cells=5, ids_file=tmp_path / "i.csv", out_dir=tmp_path / "o",
                                    future_root=tmp_path / "f", tf32=True).notes
    off = real.build_real_provenance(n_cells=5, ids_file=tmp_path / "i.csv", out_dir=tmp_path / "o",
                                     future_root=tmp_path / "f", tf32=False).notes
    assert "TF32 activado" in on and "TF32 desactivado" in off and "TF32 activado" not in off
