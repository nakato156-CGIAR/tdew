"""LLR con rezagos de Tmin: usa el rezago cuando importa y no mira la Td del bloque oculto."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.llr_simple.llr import climatology
from experiments.llr_simple.llr_lags import doy_sums, lag_features, predict, solve


def _series(seed=0, years=10, cells=2):
    dates = pd.date_range("2001-01-01", periods=365 * years)
    doy = dates.dayofyear.to_numpy()
    rng = np.random.default_rng(seed)
    tm = 10 + 4 * np.sin(2 * np.pi * doy / 365) + rng.normal(size=(cells, doy.size))
    xa = tm - 10 - 4 * np.sin(2 * np.pi * doy / 365)
    lag1 = np.concatenate([np.zeros((cells, 1)), xa[:, :-1]], axis=1)
    td = 5 + 0.3 * xa + 0.6 * lag1  # la Td depende del rezago de Tmin
    return doy, td, tm


def _fit_predict(lags):
    doy, td, tm = _series()
    train = np.arange(doy.size) < 365 * 8
    c_td, c_tm = climatology(td, doy, train), climatology(tm, doy, train)
    feat = lag_features(tm - c_tm[:, doy], lags)
    beta = solve(doy_sums(feat, td - c_td[:, doy], doy, train), 15)
    hold = np.flatnonzero(~train)
    return predict(beta, feat, c_td, doy, hold), td[:, hold]


def test_lag_feature_is_the_shifted_anomaly():
    xa = np.arange(10.0).reshape(1, 10)
    f = lag_features(xa, (2,))
    assert np.isnan(f[0, :2, 2]).all()
    np.testing.assert_array_equal(f[0, 2:, 2], xa[0, :-2])


def test_lag_model_beats_same_day_model_when_truth_has_a_lag():
    p_lag, o = _fit_predict((1,))
    p_day, _ = _fit_predict(())
    assert np.sqrt(np.mean((p_lag - o) ** 2)) < 0.5 * np.sqrt(np.mean((p_day - o) ** 2))


def test_prediction_ignores_td_of_the_hold_block():
    doy, td, tm = _series()
    train = np.arange(doy.size) < 365 * 8
    c_td, c_tm = climatology(td, doy, train), climatology(tm, doy, train)
    feat = lag_features(tm - c_tm[:, doy], (1, 7))
    beta = solve(doy_sums(feat, td - c_td[:, doy], doy, train), 15)
    hold = np.flatnonzero(~train)
    td2 = td.copy()
    td2[:, hold] += 50
    c_td2 = climatology(td2, doy, train)
    np.testing.assert_array_equal(
        predict(beta, feat, c_td, doy, hold), predict(beta, feat, c_td2, doy, hold)
    )
