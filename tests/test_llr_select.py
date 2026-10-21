"""Seleccion conjunta de h y train_start de los LLR (tdew-03g): validacion interna sin mirar
el bloque oculto, igual a un ajuste manual y sin cambiar el camino por defecto."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from experiments.llr_simple import llr, llr_lags
from experiments.timesfm.panel import TRAIN_START

IDS = [10, 11, 12]
H_SMALL = (7, 31, 90, 180)


def _synthetic(n_cells: int = 3, seed: int = 0, break_year: int | None = None):
    """TD y TMIN 1981-2016 con ciclo anual y relacion lineal; con ``break_year`` la pendiente
    Td-Tmin antes de ese anio es otra (0,1 en vez de 0,8)."""
    dates = pd.date_range(f"{TRAIN_START}-01-01", f"{llr.LAST_YEAR}-12-31")
    rng = np.random.default_rng(seed)
    doy = dates.dayofyear.to_numpy()
    season = 3.0 * np.sin(2 * np.pi * doy / 366.0)
    tm = 8.0 + season + rng.normal(0, 1.5, (n_cells, len(dates)))
    slope = np.full(len(dates), 0.8)
    if break_year is not None:
        slope[dates.year.to_numpy() < break_year] = 0.1
    td = 2.0 + 0.8 * season + slope * (tm - 8.0 - season) + rng.normal(0, 0.5, (n_cells, len(dates)))
    return np.arange(10, 10 + n_cells, dtype=np.int64), dates, td.astype("f4"), tm.astype("f4")


@pytest.fixture
def data(monkeypatch):
    state = {"arrays": _synthetic()}
    monkeypatch.setattr(llr, "load_arrays", lambda ids, root=None: state["arrays"])
    return state


RUNNERS = {
    "llr_simple": (lambda split, **kw: llr.run_split_select(split, IDS, **kw), "pred_llr_simple_sel"),
    "llr_tmin_lags": (lambda split, **kw: llr_lags.run_split_select(split, IDS, chunk=2, **kw),
                      "pred_llr_tmin_lags_sel"),
}


def _table(info):
    return pd.DataFrame(info["selection"]["validation_rmse"])


def _perturb_after(arrays, year_cut: int, which: str, seed: int = 5):
    ids, dates, td, tm = arrays
    late = dates.year.to_numpy() > year_cut
    rng = np.random.default_rng(seed)
    td2, tm2 = td.copy(), tm.copy()
    if which == "td":
        td2[:, late] = rng.normal(50, 20, td2[:, late].shape)
    else:
        tm2[:, late] = rng.normal(-30, 20, tm2[:, late].shape)
    return ids, dates, td2, tm2


@pytest.mark.parametrize("method", sorted(RUNNERS))
def test_selection_does_not_look_at_the_heldout_block(data, method):
    """Cambiar Td o Tmin de 2009 en adelante (ll4b: entrenamiento hasta 2008) no mueve la tabla de
    validacion ni lo elegido; cambiar la Td tampoco mueve la prediccion del bloque oculto."""
    run, col = RUNNERS[method]
    base, info = run("ll4b", h_grid=H_SMALL)
    original = data["arrays"]
    data["arrays"] = _perturb_after(original, 2008, "td")
    td_frame, td_info = run("ll4b", h_grid=H_SMALL)
    pd.testing.assert_frame_equal(_table(td_info), _table(info), rtol=0, atol=0)
    assert (td_info["train_start"], td_info["h_best"]) == (info["train_start"], info["h_best"])
    np.testing.assert_array_equal(td_frame[col].to_numpy(), base[col].to_numpy())
    np.testing.assert_array_equal(td_frame.pred_clim.to_numpy(), base.pred_clim.to_numpy())
    assert np.abs(td_frame.TD_obs.to_numpy() - base.TD_obs.to_numpy()).max() > 1.0
    data["arrays"] = _perturb_after(original, 2008, "tm")
    _, tm_info = run("ll4b", h_grid=H_SMALL)
    pd.testing.assert_frame_equal(_table(tm_info), _table(info), rtol=0, atol=0)


@pytest.mark.parametrize("method", sorted(RUNNERS))
def test_selection_finds_a_planted_break(data, method):
    """Si la relacion Td-Tmin cambia en 1991, la validacion elige empezar en 1991 o despues."""
    data["arrays"] = _synthetic(break_year=1991)
    run, _ = RUNNERS[method]
    _, info = run("ll4b", h_grid=H_SMALL)
    assert info["train_start"] >= 1991
    t = _table(info)
    assert len(t) == len(H_SMALL) * len(llr.TRAIN_START_GRID)
    assert t.rmse.min() == pytest.approx(t[(t.train_start == info["train_start"]) & (t.h == info["h_best"])].rmse.iloc[0])
    sel = info["selection"]
    assert sel["validation_years"] == [2005, 2008] and sel["final_fit_years"] == [info["train_start"], 2008]
    assert sel["validation_climatology_years"] == [1981, 2004] and sel["final_climatology_years"] == [1981, 2008]


def test_circulant_window_equals_roll():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(4, 366))
    for h in (7, 60, 180):
        ks = np.arange(-h, h + 1)
        w = (1 - (np.abs(ks) / (h + 1)) ** 3) ** 3
        roll = sum(wt * np.roll(x, -k, axis=1) for k, wt in zip(ks, w))
        np.testing.assert_allclose(llr.window_sum(x, llr.circulant_window(h)), roll, rtol=0, atol=1e-10)
    with pytest.raises(ValueError):
        llr.circulant_window(183)


def _masks(dates, train_end, start):
    year, doy = dates.year.to_numpy(), dates.dayofyear.to_numpy()
    return year, doy, year <= train_end - 4, (year >= start) & (year <= train_end - 4), \
        np.flatnonzero((year > train_end - 4) & (year <= train_end))


def test_llr_simple_selection_matches_a_manual_fit(data):
    """La validacion de (1991, 31) y el ajuste final coinciden con `fit` (np.roll) a mano."""
    frame, info = llr.run_split_select("ll4b", IDS, h_grid=H_SMALL)
    ids, dates, td, tm = data["arrays"]
    td64, tm64 = td.astype("f8"), tm.astype("f8")
    year, doy, clim_m, fit_m, valid = _masks(dates, 2008, 1991)
    c_td, c_tm = llr.climatology(td64, doy, clim_m), llr.climatology(tm64, doy, clim_m)
    p, o = llr.predict(*llr.fit(td64, tm64, doy, fit_m, 31, c_td, c_tm), td64, tm64, doy, valid, c_td, c_tm)
    t = _table(info)
    got = t[(t.train_start == 1991) & (t.h == 31)].rmse.iloc[0]
    assert got == pytest.approx(float(np.sqrt(np.nanmean((p - o) ** 2))), abs=1e-10)
    s, h = info["train_start"], info["h_best"]
    clim = year <= 2008
    c_td, c_tm = llr.climatology(td64, doy, clim), llr.climatology(tm64, doy, clim)
    hold = np.flatnonzero((year >= 2009) & (year <= 2012))
    pred, _ = llr.predict(*llr.fit(td64, tm64, doy, clim & (year >= s), h, c_td, c_tm),
                          td64, tm64, doy, hold, c_td, c_tm)
    np.testing.assert_allclose(frame.pred_llr_simple_sel.to_numpy(), pred.ravel(), rtol=0, atol=1e-9)


def test_llr_lags_selection_matches_a_manual_fit(data):
    frame, info = llr_lags.run_split_select("ll4b", IDS, chunk=2, h_grid=H_SMALL)
    ids, dates, td, tm = data["arrays"]
    td64, tm64 = td.astype("f8"), tm.astype("f8")
    year, doy, clim_m, fit_m, valid = _masks(dates, 2008, 1996)
    c_td, c_tm = llr.climatology(td64, doy, clim_m), llr.climatology(tm64, doy, clim_m)
    feat = llr_lags.lag_features(llr.drop_before(tm64 - c_tm[:, doy], year, 1996), llr_lags.DEFAULT_LAGS)
    beta = llr_lags.solve(llr_lags.doy_sums(feat, td64 - c_td[:, doy], doy, fit_m), 90)
    p = llr_lags.predict(beta, feat, c_td, doy, valid)
    t = _table(info)
    got = t[(t.train_start == 1996) & (t.h == 90)].rmse.iloc[0]
    assert got == pytest.approx(float(np.sqrt(np.nansum((p - td64[:, valid]) ** 2) / np.isfinite(td64[:, valid]).sum())),
                                abs=1e-10)
    s, h = info["train_start"], info["h_best"]
    clim = year <= 2008
    c_td, c_tm = llr.climatology(td64, doy, clim), llr.climatology(tm64, doy, clim)
    feat = llr_lags.lag_features(llr.drop_before(tm64 - c_tm[:, doy], year, s), llr_lags.DEFAULT_LAGS)
    beta = llr_lags.solve(llr_lags.doy_sums(feat, td64 - c_td[:, doy], doy, clim & (year >= s)), h)
    hold = np.flatnonzero((year >= 2009) & (year <= 2012))
    pred = llr_lags.predict(beta, feat, c_td, doy, hold)
    np.testing.assert_allclose(frame.pred_llr_tmin_lags_sel.to_numpy(), pred.ravel(), rtol=0, atol=1e-9)


def test_llr_lags_selection_workers_give_the_same_result(data):
    one, info1 = llr_lags.run_split_select("ll4b", IDS, chunk=1, h_grid=(15, 120), workers=1)
    two, info2 = llr_lags.run_split_select("ll4b", IDS, chunk=1, h_grid=(15, 120), workers=2)
    pd.testing.assert_frame_equal(one, two)
    assert info1 == info2


@pytest.mark.parametrize("module,method", [(llr, "llr_simple"), (llr_lags, "llr_tmin_lags")])
def test_cli_keeps_the_default_and_writes_sel_apart(data, tmp_path, module, method):
    ids_file = tmp_path / "ids.csv"
    pd.DataFrame({"ID": IDS}).to_csv(ids_file, index=False)
    common = ["--split", "ll4b", "--ids-file", str(ids_file), "--out-dir", str(tmp_path)]
    module.main(common)
    default = pd.read_parquet(tmp_path / f"ll4b__{method}.parquet")
    assert f"pred_{method}" in default and json.loads((tmp_path / f"ll4b__{method}.json").read_text())["train_start"] == 1981
    module.main(common + ["--select-train-start", "--h-grid", "7,60,180"])
    sel = pd.read_parquet(tmp_path / f"ll4b__{method}_sel.parquet")
    info = json.loads((tmp_path / f"ll4b__{method}_sel.json").read_text())
    assert f"pred_{method}_sel" in sel and f"pred_{method}" not in sel
    assert info["selection"]["h_grid"] == [7, 60, 180]
    assert info["selection"]["train_start_grid"] == list(llr.TRAIN_START_GRID)
    pd.testing.assert_frame_equal(pd.read_parquet(tmp_path / f"ll4b__{method}.parquet"), default)
    with pytest.raises(SystemExit):
        module.main(common + ["--select-train-start", "--train-start", "1991"])


def test_grids_are_validated():
    with pytest.raises(ValueError):
        llr.check_grids("ll4b", (7,), (1981, 2005))
    with pytest.raises(ValueError):
        llr.check_grids("ll4b", (200,), (1981,))
    assert llr.check_grids("ll4", (60, 7, 7), (1996, 1981)) == ((7, 60), (1981, 1996))
