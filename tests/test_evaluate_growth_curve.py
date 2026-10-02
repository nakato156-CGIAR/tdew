"""``evaluate --growth-curve`` expone error_growth_curves como CLI, con
proveniencia (PLAN_1 §Paso 5): sin CLI, su CSV quedaba excluido del control."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import evaluate
from tdew_estimation import provenance as prov

DATES = pd.date_range("2020-01-01", periods=6)


def _setup(tmp_path):
    rng = np.random.default_rng(2)
    root = tmp_path / "ref"
    (root / "ll4").mkdir(parents=True)
    rows = []
    for i in range(3):
        for d in DATES:
            obs = rng.normal()
            rows.append((i, 0, d, obs, obs + .3, obs + 1, obs + 2, obs + 2))
    ref = pd.DataFrame(rows, columns=["ID", "zone_id", "FECHA", "TD_obs", "pred_tuned",
                                      "pred_clim", "pred_tmin", "pred_ols"])
    ref.to_parquet(root / "ll4" / "predictions.parquet", index=False)
    preds = tmp_path / "preds"
    preds.mkdir()
    p = ref[["ID", "FECHA"]].copy()
    p["pred"] = ref["TD_obs"] + .1
    for q in range(1, 10):
        p[f"q{q * 10}"] = p["pred"] + (q - 5) * 0.1
    # una celda extra de TimesFM que la referencia no tiene
    extra = p[p["ID"] == 0].assign(ID=99)
    pd.concat([p, extra]).to_parquet(preds / "ll4__tmin_anom_full.parquet", index=False)
    return root, preds


def test_error_growth_curves_reports_cell_count(tmp_path):
    root, preds = _setup(tmp_path)
    curve = evaluate.error_growth_curves(preds, "ll4", variant="tmin_anom_full",
                                         backtest_root=root)
    assert curve.attrs["cells"] == 3
    assert set(curve["method"]) == {"climatology", "td_eq_tmin", "zone_ols", "tuned", "timesfm"}
    assert curve["dia"].max() == len(DATES)


def test_cli_writes_curve_and_records_one_provenance_row_per_method(tmp_path, monkeypatch):
    root, preds = _setup(tmp_path)
    records = []
    monkeypatch.setattr(prov, "record_metric_provenance", records.append)
    out = tmp_path / "curva.csv"
    evaluate.main([
        "--predictions-dir", str(preds), "--backtest-root", str(root),
        "--out-dir", str(tmp_path / "o"), "--splits", "ll4",
        "--growth-curve", "ll4", "--growth-variant", "tmin_anom_full",
        "--growth-curve-out", str(out), "--manifest-ref", "addendum",
        "--panel-id", "p_limpio",
    ])
    curve = pd.read_csv(out)
    assert list(curve.columns) == ["split", "method", "dia", "rmse_acumulado"]
    growth = [r for r in records if str(out) in r.output_files]
    assert {r.variant_label for r in growth} == {
        "climatology", "td_eq_tmin", "zone_ols", "tuned", "tmin_anom_full"}
    assert all(r.panel_id == "p_limpio" and r.panel_cell_count == 3 for r in growth)
    assert all(r.manifest_ref == "addendum" for r in growth)
    assert all(r.split_id == "ll4" for r in growth)


def test_growth_curve_requires_variant_and_output(tmp_path):
    root, preds = _setup(tmp_path)
    with pytest.raises(SystemExit) as exc:
        evaluate.main(["--predictions-dir", str(preds), "--backtest-root", str(root),
                       "--out-dir", str(tmp_path / "o"), "--growth-curve", "ll4"])
    assert exc.value.code == 2


def _tiny(tmp_path, *, nan_in_tuned=False):
    """Dos celdas, dos dias, errores conocidos a mano (todos los metodos = obs + e)."""
    root = tmp_path / "ref"
    (root / "ll4").mkdir(parents=True)
    d = pd.date_range("2020-01-01", periods=2)
    rows = []
    for cid in (0, 1):
        for k, date in enumerate(d):
            e = 1.0 if k == 0 else 3.0     # dia 1: error 1 ; dia 2: error 3
            rows.append((cid, 0, date, 0.0, e, e, e, e))
    ref = pd.DataFrame(rows, columns=["ID", "zone_id", "FECHA", "TD_obs", "pred_tuned",
                                      "pred_clim", "pred_tmin", "pred_ols"])
    if nan_in_tuned:
        ref.loc[(ref.ID == 0) & (ref.FECHA == d[0]), "pred_tuned"] = np.nan
    ref.to_parquet(root / "ll4" / "predictions.parquet", index=False)
    preds = tmp_path / "preds"
    preds.mkdir()
    p = ref[["ID", "FECHA"]].copy()
    p["pred"] = ref["pred_clim"]
    p.to_parquet(preds / "ll4__v.parquet", index=False)
    return root, preds


def test_cumulative_rmse_has_hand_computed_values(tmp_path):
    root, preds = _tiny(tmp_path)
    curve = evaluate.error_growth_curves(preds, "ll4", variant="v", backtest_root=root)
    clim = curve[curve["method"] == "climatology"].set_index("dia")["rmse_acumulado"]
    assert clim[1] == pytest.approx(1.0)
    # dia 1 aporta 2 celdas con se=1, dia 2 aporta 2 con se=9 -> sqrt((2+18)/4)
    assert clim[2] == pytest.approx(np.sqrt(5.0))


def test_nan_predictions_do_not_bias_the_cumulative_rmse(tmp_path):
    root, preds = _tiny(tmp_path, nan_in_tuned=True)
    curve = evaluate.error_growth_curves(preds, "ll4", variant="v", backtest_root=root)
    tuned = curve[curve["method"] == "tuned"].set_index("dia")["rmse_acumulado"]
    assert tuned[1] == pytest.approx(1.0)       # solo cuenta la celda finita
    assert tuned[2] == pytest.approx(np.sqrt((1 + 18) / 3))


def test_cli_records_absolute_output_paths_independent_of_cwd(tmp_path, monkeypatch):
    root, preds = _setup(tmp_path)
    records = []
    monkeypatch.setattr(prov, "record_metric_provenance", records.append)
    monkeypatch.chdir(tmp_path)
    evaluate.main([
        "--predictions-dir", str(preds), "--backtest-root", str(root),
        "--out-dir", "rel_out", "--splits", "ll4", "--growth-curve", "ll4",
        "--growth-variant", "tmin_anom_full", "--growth-curve-out", "rel/curva.csv",
    ])
    assert records
    for rec in records:
        assert all(__import__("pathlib").Path(f).is_absolute() for f in rec.output_files)
