"""Las notas de proveniencia dicen contra que referencia se puntuo (PLAN_1 §8)."""
from __future__ import annotations

import pandas as pd
import pytest

from experiments.timesfm import departamental, evaluate, merge_predictions
from experiments.timesfm.evaluate import (
    build_row_provenance,
    CLEAN_BACKTEST_ROOT,
    LEAKY_BACKTEST_ROOT,
    backtest_notes,
)
from tdew_estimation import provenance as prov


ADDENDUM = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"


def test_manifest_ref_for_clean_root_is_the_addendum_and_leaky_is_original():
    assert evaluate.MANIFEST_REF_LIMPIO == ADDENDUM
    assert evaluate.manifest_ref_for(CLEAN_BACKTEST_ROOT) == ADDENDUM
    assert evaluate.manifest_ref_for(LEAKY_BACKTEST_ROOT) == evaluate.MANIFEST_REF


def test_build_row_provenance_accepts_manifest_ref_for_both_method_kinds():
    for method in ("timesfm:tmin_anom_full", "tuned"):
        record = build_row_provenance(
            method, split="ll4", cells=1, bead_id="b", panel_id="p", panel_file="f",
            output_files=("o",), manifest_ref=ADDENDUM,
        )
        assert record.manifest_ref == ADDENDUM


def test_default_manifest_ref_is_unchanged_for_old_callers():
    record = build_row_provenance(
        "tuned", split="ll4", cells=1, bead_id="b", panel_id="p", panel_file="f",
        output_files=("o",),
    )
    assert record.manifest_ref == evaluate.MANIFEST_REF


def test_notes_extra_is_appended():
    note = backtest_notes(CLEAN_BACKTEST_ROOT, cells=5, extra="cells_lost=0")
    assert note.endswith("cells_lost=0")


def test_clean_root_notes_describe_train_only_selection_and_cells():
    note = backtest_notes(CLEAN_BACKTEST_ROOT, cells=17027)
    assert f"backtest_root={CLEAN_BACKTEST_ROOT}" in note
    assert "selección solo con años de entrenamiento" in note
    assert "h {7,11,15,21,31,45}" in note
    assert "17027" in note


def test_leaky_root_notes_never_claim_train_only_selection():
    note = backtest_notes(LEAKY_BACKTEST_ROOT, cells=17041)
    assert "con fuga" in note
    assert "solo con años de entrenamiento" not in note


def test_unknown_root_states_selection_is_unknown_and_resolves_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    note = backtest_notes(__import__("pathlib").Path("rel/root"), cells=3)
    assert f"backtest_root={tmp_path / 'rel' / 'root'}" in note
    assert "selección no declarada" in note


def test_departamental_requires_backtest_predictions(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        departamental.main(["--reconstruction", str(tmp_path / "x.parquet"),
                            "--out-dir", str(tmp_path)])
    assert exc.value.code == 2
    assert "--backtest-predictions" in capsys.readouterr().err


def test_merge_main_records_notes_with_cells(tmp_path, monkeypatch):
    dates = pd.date_range("2020-01-01", periods=3)
    root = tmp_path / "ref"
    (root / "ll4").mkdir(parents=True)
    ref = pd.DataFrame(
        [(i, d, 1.0, 1.0, 1.0, 1.0, 1.0, 0) for i in ("a", "b") for d in dates],
        columns=["ID", "FECHA", "TD_obs", "pred_tuned", "pred_clim", "pred_tmin",
                 "pred_ols", "zone_id"],
    )
    ref.to_parquet(root / "ll4" / "predictions.parquet", index=False)
    preds = tmp_path / "preds"
    preds.mkdir()
    pd.DataFrame([(i, d, 1.0) for i in ("a", "b", "x") for d in dates],
                 columns=["ID", "FECHA", "pred"]).to_parquet(
        preds / "ll4__tmin_anom_full.parquet", index=False)
    records = []
    monkeypatch.setattr(prov, "record_metric_provenance", records.append)
    merge_predictions.main([
        "--predictions-dir", str(preds), "--variant", "tmin_anom_full",
        "--splits", "ll4", "--backtest-root", str(root), "--out-root", str(tmp_path / "out"),
        "--manifest-ref", ADDENDUM,
    ])
    assert records, "debe registrar proveniencia"
    for rec in records:
        assert f"backtest_root={root}" in rec.notes
        assert "cells=2" in rec.notes
        assert any(f.endswith("metrics_all.csv") for f in rec.output_files)
        assert any(f.endswith("ll4/metrics.csv") for f in rec.output_files)
        assert "cells_lost=0" in rec.notes
        assert "cells_timesfm_dropped=1" in rec.notes
        assert rec.manifest_ref == ADDENDUM
