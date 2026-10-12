"""Unit tests for tdew_estimation.metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from tdew_estimation.metrics import MetricsAccum, NormalEquationsAccum, OLSAccum, regression_metrics, score_methods


def test_regression_metrics_known_values():
    obs = np.array([10.0, 12.0, 8.0, 9.0])
    pred = np.array([11.0, 12.0, 6.0, 9.0])  # errors: 1, 0, -2, 0
    m = regression_metrics(pred, obs)
    assert m["n"] == 4
    assert np.isclose(m["bias"], (1 + 0 - 2 + 0) / 4)
    assert np.isclose(m["mae"], (1 + 0 + 2 + 0) / 4)
    assert np.isclose(m["rmse"], np.sqrt((1 + 0 + 4 + 0) / 4))


def test_metrics_accum_matches_regression_metrics_across_chunks():
    rng = np.random.default_rng(0)
    obs = rng.normal(20, 3, size=1000)
    pred = obs + rng.normal(0, 1, size=1000)

    expected = regression_metrics(pred, obs)

    acc = MetricsAccum()
    for p_chunk, o_chunk in zip(np.array_split(pred, 7), np.array_split(obs, 7)):
        acc.add(p_chunk, o_chunk)
    got = acc.finalize()

    for k in ("n", "rmse", "mae", "bias", "r"):
        assert np.isclose(got[k], expected[k]), (k, got[k], expected[k])


def test_score_methods_skill_vs_clim_and_grouping():
    df = pd.DataFrame(
        {
            "site": ["a", "a", "b", "b"],
            "obs": [10.0, 10.0, 20.0, 20.0],
            "clim": [10.0, 10.0, 20.0, 20.0],  # perfect climatology -> rmse 0
            "model": [11.0, 9.0, 21.0, 19.0],  # rmse 1 -> worse than climatology
        }
    )
    out = score_methods(
        df, obs_col="obs", method_cols={"climatology": "clim", "model": "model"}, clim_col="clim", group_cols=["site"]
    )
    pooled_model = out[(out["site"] == "ALL") & (out["method"] == "model")].iloc[0]
    assert np.isclose(pooled_model["rmse"], 1.0)
    # clim_rmse is exactly 0 here (perfect climatology) -> skill_vs_clim is
    # undefined (nan), per score_methods' guard against dividing by zero.
    assert np.isnan(pooled_model["skill_vs_clim"])
    site_a = out[(out["site"] == "a") & (out["method"] == "climatology")].iloc[0]
    assert np.isclose(site_a["rmse"], 0.0)


def test_ols_accum_matches_closed_form_ols():
    rng = np.random.default_rng(1)
    x = rng.normal(size=500)
    y = 2.0 + 3.0 * x + rng.normal(scale=0.01, size=500)

    acc = OLSAccum()
    for xc, yc in zip(np.array_split(x, 5), np.array_split(y, 5)):
        acc.add(xc, yc)
    a, b = acc.fit()

    expected = sm.OLS(y, sm.add_constant(x)).fit().params
    assert np.isclose(a, expected[0], atol=1e-6)
    assert np.isclose(b, expected[1], atol=1e-6)


def test_normal_equations_accum_matches_statsmodels_wls():
    rng = np.random.default_rng(2)
    n = 400
    X_raw = rng.normal(size=(n, 3))
    beta_true = np.array([1.0, 2.0, -1.0, 0.5])
    X = np.column_stack([np.ones(n), X_raw])
    y = X @ beta_true + rng.normal(scale=0.01, size=n)
    w = rng.uniform(0.5, 1.5, size=n)

    acc = NormalEquationsAccum(["const", "x1", "x2", "x3"])
    for lo, hi in [(0, 100), (100, 250), (250, 400)]:
        acc.add(X[lo:hi], y[lo:hi], w[lo:hi])
    got = acc.fit(ridge=0.0)

    expected = sm.WLS(y, X, weights=w).fit().params
    for i, name in enumerate(["const", "x1", "x2", "x3"]):
        assert np.isclose(got[name], expected[i], atol=1e-4), (name, got[name], expected[i])
