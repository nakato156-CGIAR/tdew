"""Pruebas sinteticas de experiments/paper_nuevo/analisis_inferencia.py (tdew-4w2)."""

import numpy as np
import pandas as pd
import pytest

from experiments.paper_nuevo import analisis_inferencia as ai


def _df():
    dates = pd.date_range("2009-01-01", "2012-12-31")
    d = pd.DataFrame({"FECHA": np.tile(dates, 2), "ID": np.repeat([1, 2], len(dates)),
                      "lon": np.repeat([-75.5, -71.2], len(dates)), "lat": -12.1})
    d["year"] = d.FECHA.dt.year.astype(np.int16)
    d["month"] = d.FECHA.dt.month.astype(np.int8)
    return d


def test_dm_iid_zero_mean_not_significant():
    rng = np.random.default_rng(1)
    pvals = [ai.diebold_mariano(rng.normal(size=1461), ai.nw_lag(1461))["p_hln"] for _ in range(40)]
    assert np.mean(np.array(pvals) < 0.05) < 0.2
    assert ai.diebold_mariano(rng.normal(size=1461), 7)["p_hln"] > 0.001


def test_dm_detects_shift_and_ar_autocorrelation():
    rng = np.random.default_rng(2)
    assert ai.diebold_mariano(rng.normal(0.5, 1, 1461), 7)["p_hln"] < 1e-6
    e = np.zeros(1461)
    for i in range(1, 1461):
        e[i] = 0.9 * e[i - 1] + rng.normal()
    # con autocorrelacion el HAC da una varianza mayor que la iid
    assert ai.nw_variance(e, 30) > 3 * e.var()


def test_nw_lag_rule():
    assert ai.nw_lag(1461) == 7
    assert ai.nw_lag(100) == 4
    assert ai.nw_lag(1461) < ai.LONG_LAG


def test_holm():
    adj = ai.holm([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06])
    assert (adj >= np.array([0.01, 0.04, 0.03])).all() and (adj <= 1).all()


def test_block_keys_new_schemes():
    d = _df()
    st = ai.block_keys(d, "espaciotemporal_2g_anio")
    assert len(np.unique(st)) == 2 * 4
    tq = ai.block_keys(d, "temporal_trim_anio")
    assert len(np.unique(tq)) == 16
    assert np.array_equal(ai.block_keys(d, "espacial_2g"), ai.dg.block_keys(d, "espacial_2g"))
    with pytest.raises(ValueError):
        ai.block_keys(d, "otro")


def test_horizon_index():
    d = _df()
    month, year = ai.horizon_index(d)
    assert month.min() == 1 and month.max() == 48 and year.min() == 1 and year.max() == 4
    assert month[(d.year == 2010) & (d.month == 3)].max() == 15


def test_horizon_gaps_sign_and_levels():
    d = _df()
    rng = np.random.default_rng(0)
    n = len(d)
    se = pd.DataFrame({"timesfm_anom": rng.normal(size=n) ** 2 * 0.5, "tuned": rng.normal(size=n) ** 2})
    out = ai.horizon_gaps(d, se, [("timesfm_anom", "tuned")], n_boot=50)
    assert set(out.unidad) == {"mes", "anio"}
    assert (out[out.unidad == "mes"].horizonte.nunique(), out[out.unidad == "anio"].horizonte.nunique()) == (48, 4)
    assert (out.brecha < 0).all()
