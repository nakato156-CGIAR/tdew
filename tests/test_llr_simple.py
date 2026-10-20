"""LLR simple: recupera una relacion lineal conocida y respeta el calendario circular."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.llr_simple.llr import climatology, fit, predict


def _synthetic(slope=0.7, years=8, cells=3, noise=0.0, seed=0):
    dates = pd.date_range("2001-01-01", periods=365 * years)
    doy = dates.dayofyear.to_numpy()
    rng = np.random.default_rng(seed)
    tm = 10 + 5 * np.sin(2 * np.pi * doy / 365) + rng.normal(size=(cells, doy.size))
    td = 5 + slope * (tm - 10) + noise * rng.normal(size=tm.shape)
    return doy, td, tm


def test_recovers_known_slope_without_noise():
    doy, td, tm = _synthetic(slope=0.7)
    train = np.ones(doy.size, bool)
    c_td, c_tm = climatology(td, doy, train), climatology(tm, doy, train)
    _, b = fit(td, tm, doy, train, 15, c_td, c_tm)
    assert np.allclose(b[:, 10:355], 0.7, atol=0.1)


def test_prediction_is_exact_without_noise():
    doy, td, tm = _synthetic(slope=0.7)
    train = np.ones(doy.size, bool)
    c_td, c_tm = climatology(td, doy, train), climatology(tm, doy, train)
    a, b = fit(td, tm, doy, train, 15, c_td, c_tm)
    pred, obs = predict(a, b, td, tm, doy, np.arange(doy.size), c_td, c_tm)
    assert np.sqrt(np.mean((pred - obs) ** 2)) < 0.3


def test_prediction_ignores_td_of_the_prediction_block():
    doy, td, tm = _synthetic(slope=0.7, noise=0.5)
    train = np.arange(doy.size) < 365 * 6
    c_td, c_tm = climatology(td, doy, train), climatology(tm, doy, train)
    a, b = fit(td, tm, doy, train, 21, c_td, c_tm)
    hold = np.flatnonzero(~train)
    p1, _ = predict(a, b, td, tm, doy, hold, c_td, c_tm)
    td2 = td.copy()
    td2[:, hold] += 100.0
    p2, _ = predict(a, b, td2, tm, doy, hold, c_td, c_tm)
    np.testing.assert_array_equal(p1, p2)
