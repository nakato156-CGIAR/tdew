"""Metricas probabilisticas de TimesFM contra valores calculados a mano."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.probabilistic import (
    COLUMNS,
    LEVELS,
    crps_from_quantiles,
    interval_coverage,
    pinball,
    probabilistic_metrics,
)


def test_pinball_matches_the_definition_by_hand():
    # Un solo caso: observado 2, todos los cuantiles en 0. El error es +2, asi que
    # la perdida de cada nivel tau es tau * 2.
    observed = np.array([2.0])
    quantiles = np.zeros((1, LEVELS.size))
    np.testing.assert_allclose(pinball(observed, quantiles), LEVELS * 2.0)

    # Observado 0 y cuantiles en 2: el error es -2 y la perdida es (1 - tau) * 2.
    np.testing.assert_allclose(
        pinball(np.array([0.0]), np.full((1, LEVELS.size), 2.0)), (1.0 - LEVELS) * 2.0
    )


def test_pinball_is_zero_for_a_perfect_degenerate_forecast():
    observed = np.array([3.5, -1.0])
    quantiles = np.repeat(observed[:, None], LEVELS.size, axis=1)
    np.testing.assert_allclose(pinball(observed, quantiles), np.zeros(LEVELS.size), atol=1e-12)


def test_crps_is_twice_the_mean_pinball():
    rng = np.random.default_rng(0)
    observed = rng.normal(size=64)
    quantiles = np.sort(rng.normal(size=(64, LEVELS.size)), axis=1)
    expected = 2.0 * pinball(observed, quantiles).mean()
    assert crps_from_quantiles(observed, quantiles) == pytest.approx(expected)


def test_crps_of_a_perfect_forecast_is_zero():
    observed = np.array([1.0, 2.0, 3.0])
    quantiles = np.repeat(observed[:, None], LEVELS.size, axis=1)
    assert crps_from_quantiles(observed, quantiles) == pytest.approx(0.0, abs=1e-12)


def test_coverage_counts_only_what_falls_inside():
    observed = np.array([0.0, 5.0, -5.0, 1.0])
    lower = np.full(4, -1.0)
    upper = np.full(4, 2.0)
    result = interval_coverage(observed, lower, upper)
    assert result["cobertura_80"] == pytest.approx(0.5)
    assert result["anchura_80"] == pytest.approx(3.0)
    assert result["n"] == 4


def test_coverage_ignores_non_finite_rows():
    observed = np.array([0.0, np.nan])
    result = interval_coverage(observed, np.array([-1.0, -1.0]), np.array([1.0, 1.0]))
    assert result["n"] == 1
    assert result["cobertura_80"] == pytest.approx(1.0)


def test_wrong_number_of_levels_is_rejected():
    with pytest.raises(ValueError):
        pinball(np.array([0.0]), np.zeros((1, 3)))


def test_summary_reports_every_level_and_detects_no_crossing():
    rng = np.random.default_rng(1)
    observed = rng.normal(size=32)
    quantiles = np.sort(rng.normal(size=(32, LEVELS.size)), axis=1)
    frame = pd.DataFrame(quantiles, columns=list(COLUMNS))
    frame["TD_obs"] = observed
    out = probabilistic_metrics(frame)
    assert {f"pinball_{name}" for name in COLUMNS} <= set(out)
    assert out["fraccion_cruces"] == pytest.approx(0.0)
    assert 0.0 <= out["cobertura_80"] <= 1.0


def test_summary_requires_the_nine_deciles():
    frame = pd.DataFrame({"TD_obs": [1.0], "q10": [0.0]})
    with pytest.raises(ValueError, match="faltan columnas"):
        probabilistic_metrics(frame)
