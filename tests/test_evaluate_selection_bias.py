"""Con una sola variante el sesgo de seleccion no existe (no hubo seleccion):
no se escribe sesgo_seleccion_<split>.csv (PLAN_1 §Paso 3)."""
from __future__ import annotations

import numpy as np
import pytest
import pandas as pd

from experiments.timesfm import evaluate
from tdew_estimation import provenance as prov

DATES = pd.date_range("2020-01-01", periods=5)


def _setup(tmp_path, variants):
    rng = np.random.default_rng(1)
    root = tmp_path / "ref"
    (root / "ll4").mkdir(parents=True)
    rows = []
    for i in range(4):
        for d in DATES:
            obs = rng.normal()
            rows.append((i, i % 2, d, obs, obs + .3, obs + 1, obs + 2, obs + 2))
    ref = pd.DataFrame(rows, columns=["ID", "zone_id", "FECHA", "TD_obs", "pred_tuned",
                                      "pred_clim", "pred_tmin", "pred_ols"])
    ref.to_parquet(root / "ll4" / "predictions.parquet", index=False)
    preds = tmp_path / "preds"
    preds.mkdir()
    for key in variants:
        p = ref[["ID", "FECHA"]].copy()
        p["pred"] = ref["TD_obs"] + rng.normal(0, .2, len(ref))
        for q in range(1, 10):
            p[f"q{q * 10}"] = p["pred"] + (q - 5) * 0.1
        p.to_parquet(preds / f"ll4__{key}.parquet", index=False)
    return root, preds


def _run(tmp_path, monkeypatch, variants):
    root, preds = _setup(tmp_path, variants)
    monkeypatch.setattr(prov, "record_metric_provenance", lambda *a, **k: None)
    out = tmp_path / "out"
    evaluate.main(["--predictions-dir", str(preds), "--splits", "ll4",
                   "--backtest-root", str(root), "--out-dir", str(out)])
    return out


def test_single_variant_writes_no_selection_bias_file(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, ["tmin_anom_full"])
    assert (out / "leaderboard.csv").exists()
    assert not list(out.glob("sesgo_seleccion_*.csv"))


def test_several_variants_still_write_selection_bias_file(tmp_path, monkeypatch):
    out = _run(tmp_path, monkeypatch, ["tmin_anom_full", "uni_anom_full"])
    assert (out / "sesgo_seleccion_ll4.csv").exists()


def test_retired_variant_parquet_is_skipped_with_a_warning(tmp_path, caplog):
    root, preds = _setup(tmp_path, ["tmin_anom_full", "uni_anom_full", "tmin_td_25"])
    with caplog.at_level("WARNING", logger="timesfm.evaluate"):
        board, _ = evaluate.score_split(preds, "ll4", backtest_root=root)
    methods = set(board["method"])
    assert "timesfm:tmin_td_25" not in methods
    assert {"timesfm:tmin_anom_full", "timesfm:uni_anom_full"} <= methods
    assert any("tmin_td_25" in r.message and "retirada" in r.message for r in caplog.records)


def test_retired_variants_constant_matches_the_variant_registry():
    from experiments.timesfm.variants import variant

    for key in evaluate.RETIRED_VARIANTS:
        with pytest.raises(KeyError):
            variant(key)


def test_unknown_variant_parquet_is_skipped_before_anything_is_written(tmp_path, caplog):
    root, preds = _setup(tmp_path, ["tmin_anom_full"])
    pd.read_parquet(preds / "ll4__tmin_anom_full.parquet").to_parquet(
        preds / "ll4__foo_removed.parquet", index=False)
    with caplog.at_level("WARNING", logger="timesfm.evaluate"):
        board, _ = evaluate.score_split(preds, "ll4", backtest_root=root)
    assert "timesfm:foo_removed" not in set(board["method"])
    assert any("foo_removed" in r.message for r in caplog.records)


def test_by_zone_emits_each_rival_once_per_zone_not_once_per_variant(tmp_path):
    root, preds = _setup(tmp_path, ["tmin_anom_full", "uni_anom_full"])
    _, zones = evaluate.score_split(preds, "ll4", backtest_root=root, by_zone=True)
    counts = zones.groupby(["split", "zone_id", "method"]).size()
    assert (counts == 1).all(), counts[counts > 1]
    assert {"tuned", "climatology", "timesfm:tmin_anom_full", "timesfm:uni_anom_full"} <= set(
        zones["method"])


def test_notes_option_is_appended_to_every_provenance_note(tmp_path, monkeypatch):
    root, preds = _setup(tmp_path, ["tmin_anom_full"])
    records = []
    monkeypatch.setattr(prov, "record_metric_provenance", records.append)
    evaluate.main(["--predictions-dir", str(preds), "--splits", "ll4", "--backtest-root", str(root),
                   "--out-dir", str(tmp_path / "o"), "--notes", "interseccion con backtest_clean"])
    assert records and all("interseccion con backtest_clean" in r.notes for r in records)
