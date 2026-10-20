"""`--train-start` de los LLR (tdew-03g, escalera de contexto): recorta el entrenamiento
por la izquierda y no cambia nada cuando se deja en su valor por defecto."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.llr_simple import llr, llr_lags
from experiments.timesfm.panel import TRAIN_START


def _synthetic(n_cells: int = 3, seed: int = 0):
    """TD y TMIN 1981-2016 con ciclo anual, relacion lineal y ruido; mismo formato que load_arrays."""
    dates = pd.date_range(f"{TRAIN_START}-01-01", f"{llr.LAST_YEAR}-12-31")
    rng = np.random.default_rng(seed)
    doy = dates.dayofyear.to_numpy()
    season = 3.0 * np.sin(2 * np.pi * doy / 366.0)
    tm = (8.0 + season + rng.normal(0, 1.5, (n_cells, len(dates)))).astype("f4")
    td = (2.0 + 0.8 * tm + rng.normal(0, 0.7, (n_cells, len(dates)))).astype("f4")
    return np.arange(10, 10 + n_cells, dtype=np.int64), dates, td, tm


@pytest.fixture
def data(monkeypatch):
    state = {"arrays": _synthetic()}
    monkeypatch.setattr(llr, "load_arrays", lambda ids, root=None: state["arrays"])
    return state


def _shuffle_td_years_before(arrays, year_cut: int):
    """Copia con la Td de los anios anteriores a ``year_cut`` permutada entre esos anios
    (bisiesto con bisiesto) y la Tmin intacta: la climatologia por dia del anio de Td y de
    Tmin no cambia, pero la relacion dia a dia Td-Tmin anterior a ``year_cut`` se rompe."""
    ids, dates, td, tm = arrays
    year = dates.year.to_numpy()
    early = sorted(set(year[year < year_cut].tolist()))
    leap = [y for y in early if y % 4 == 0]
    plain = [y for y in early if y % 4]
    mapping = {**dict(zip(plain, plain[1:] + plain[:1])), **dict(zip(leap, leap[1:] + leap[:1]))}
    td2 = td.copy()
    for src, dst in mapping.items():
        td2[:, year == dst] = td[:, year == src]
    return ids, dates, td2, tm


RUNNERS = {
    "llr_simple": (lambda split, **kw: llr.run_split(split, [10, 11, 12], **kw), "pred_llr_simple"),
    "llr_tmin_lags": (lambda split, **kw: llr_lags.run_split(split, [10, 11, 12], chunk=2, **kw),
                      "pred_llr_tmin_lags"),
}


@pytest.mark.parametrize("method", sorted(RUNNERS))
def test_default_train_start_is_1981(data, method):
    run, col = RUNNERS[method]
    default, info_d = run("ll4b")
    explicit, info_e = run("ll4b", train_start=1981)
    pd.testing.assert_frame_equal(default, explicit)
    assert info_d["train_start"] == 1981 and info_d["h_best"] == info_e["h_best"]


@pytest.mark.parametrize("method", sorted(RUNNERS))
def test_train_start_trims_the_fit_but_not_the_climatology(data, method):
    """Con train_start=1991 la climatologia sigue siendo 1981-2008 (igual que el defecto) y
    los coeficientes no ven la relacion Td-Tmin anterior a 1991: romperla no mueve la
    prediccion. Con el defecto si la mueve."""
    run, col = RUNNERS[method]
    base_cut, info = run("ll4b", train_start=1991)
    base_def, _ = run("ll4b")
    np.testing.assert_allclose(base_cut["pred_clim"], base_def["pred_clim"], rtol=0, atol=1e-12)
    data["arrays"] = _shuffle_td_years_before(data["arrays"], 1991)
    cut, _ = run("ll4b", train_start=1991)
    dflt, _ = run("ll4b")
    np.testing.assert_allclose(cut["pred_clim"], base_cut["pred_clim"], rtol=0, atol=1e-9)
    np.testing.assert_allclose(cut[col].to_numpy(), base_cut[col].to_numpy(), rtol=0, atol=1e-8)
    assert np.abs(dflt[col].to_numpy() - base_def[col].to_numpy()).max() > 0.05
    assert info["train_start"] == 1991 and info["train_end"] == 2008


def test_train_start_keeps_the_1981_climatology(data):
    """La prediccion climatologica es la media por dia del anio de 1981..train_end aunque
    los coeficientes empiecen en 1996."""
    ids, dates, td, _ = data["arrays"]
    frame, _ = llr.run_split("ll4b", [10, 11, 12], train_start=1996)
    year, doy = dates.year.to_numpy(), dates.dayofyear.to_numpy()
    d = pd.Timestamp("2009-03-01").dayofyear
    got = frame[(frame.ID == 10) & (frame.FECHA == pd.Timestamp("2009-03-01"))].pred_clim.iloc[0]
    expected = td[0].astype("f8")[(year <= 2008) & (doy == d)].mean()
    assert got == pytest.approx(expected, abs=1e-9)


def test_train_start_fit_matches_a_manual_fit_on_the_kept_years(data):
    """LLR simple: coeficientes con [train_start, train_end], climatologia con [1981, train_end]."""
    ids, dates, td, tm = data["arrays"]
    frame, info = llr.run_split("ll4b", [10, 11, 12], train_start=1996)
    year, doy = dates.year.to_numpy(), dates.dayofyear.to_numpy()
    td64, tm64 = td.astype("f8"), tm.astype("f8")
    clim = year <= 2008
    c_td, c_tm = llr.climatology(td64, doy, clim), llr.climatology(tm64, doy, clim)
    a, b = llr.fit(td64, tm64, doy, clim & (year >= 1996), info["h_best"], c_td, c_tm)
    hold = np.flatnonzero((year >= 2009) & (year <= 2012))
    pred, _ = llr.predict(a, b, td64, tm64, doy, hold, c_td, c_tm)
    np.testing.assert_allclose(frame.pred_llr_simple.to_numpy(), pred.ravel(), rtol=0, atol=1e-10)


def test_train_start_must_leave_inner_years_for_validation():
    with pytest.raises(ValueError):
        llr.check_train_start("ll4b", 2005)  # 2005-2008 son los cuatro de validacion
    with pytest.raises(ValueError):
        llr.check_train_start("ll4", 1980)
    llr.check_train_start("ll4b", 2004)


def test_output_stem_keeps_the_default_name():
    assert llr.output_stem("ll4b", "llr_simple", None) == "ll4b__llr_simple"
    assert llr.output_stem("ll4", "llr_tmin_lags", 1996) == "ll4__llr_tmin_lags__train1996"
