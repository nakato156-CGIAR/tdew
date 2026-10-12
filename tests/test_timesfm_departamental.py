"""Ensamblado de la mesa departamental: formato canónico y control de paridad."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.departamental import (
    CANONICAL_COLUMNS,
    assemble,
    climatology_to_long,
    timesfm_to_long,
    tuned_to_long,
)


@pytest.fixture
def reference_long():
    """Salida del pipeline de reconstrucción, que ya viene en formato largo."""
    dates = pd.date_range("2013-01-01", periods=4, freq="D")
    ids = [11, 22]
    rows = []
    for index, location in enumerate(ids):
        for offset, date in enumerate(dates):
            rows.append(
                {
                    "ID": location,
                    "department": "Cusco" if index == 0 else "Lima",
                    "date": date,
                    "year_horizon": 1,
                    "TD_obs": 10.0 + offset + index,
                    "TD_clim": 9.0 + offset + index,
                    "TD_pred": 9.5 + offset + index,
                    "model": "tcn_direct",
                    "seed": 0,
                    "fold": "ll4",
                }
            )
    return pd.DataFrame(rows)


def _write_timesfm(tmp_path, reference_long, shift=0.25):
    frame = reference_long[["ID", "date"]].copy()
    frame["FECHA"] = frame["date"]
    frame = frame.drop(columns=["date"])
    frame["pred"] = reference_long["TD_obs"].to_numpy() + shift
    path = tmp_path / "timesfm.parquet"
    frame.to_parquet(path, index=False)
    return path


def _write_backtest(tmp_path, reference_long, *, clim_offset=0.0, obs_offset=0.0):
    frame = pd.DataFrame(
        {
            "ID": reference_long["ID"],
            "FECHA": reference_long["date"],
            "TD_obs": reference_long["TD_obs"] + obs_offset,
            "pred_clim": reference_long["TD_clim"] + clim_offset,
            "pred_tuned": reference_long["TD_obs"] - 0.5,
        }
    )
    path = tmp_path / "backtest.parquet"
    frame.to_parquet(path, index=False)
    return path


def test_timesfm_conversion_keeps_the_canonical_columns(tmp_path, reference_long):
    path = _write_timesfm(tmp_path, reference_long)
    out = timesfm_to_long(path, reference_long)
    assert list(out.columns) == list(CANONICAL_COLUMNS)
    assert out["model"].unique().tolist() == ["timesfm"]
    assert len(out) == len(reference_long)
    np.testing.assert_allclose(out["TD_pred"], reference_long["TD_obs"] + 0.25)


def test_climatology_becomes_an_explicit_competitor(reference_long):
    out = climatology_to_long(reference_long)
    assert list(out.columns) == list(CANONICAL_COLUMNS)
    np.testing.assert_allclose(out["TD_pred"], reference_long["TD_clim"])
    assert out["model"].unique().tolist() == ["climatology"]


def test_tuned_conversion_resolves_the_duplicated_observation_column(tmp_path, reference_long):
    """Ambas fuentes traen TD_obs, así que la unión genera sufijos.

    Si esa resolución estuviera mal, la tabla saldría con una columna TD_obs
    ausente o con el valor equivocado y la comparación entera quedaría torcida.
    """
    path = _write_backtest(tmp_path, reference_long)
    out = tuned_to_long(path, reference_long)
    assert list(out.columns) == list(CANONICAL_COLUMNS)
    np.testing.assert_allclose(out["TD_obs"], reference_long["TD_obs"])
    np.testing.assert_allclose(out["TD_pred"], reference_long["TD_obs"] - 0.5)


def test_parity_check_stops_a_mismatched_climatology(tmp_path, reference_long):
    path = _write_backtest(tmp_path, reference_long, clim_offset=0.5)
    with pytest.raises(ValueError, match="no coinciden"):
        tuned_to_long(path, reference_long)


def test_parity_check_stops_a_mismatched_observation(tmp_path, reference_long):
    path = _write_backtest(tmp_path, reference_long, obs_offset=0.5)
    with pytest.raises(ValueError, match="no coinciden"):
        tuned_to_long(path, reference_long)


def test_parity_check_tolerates_floating_point_noise(tmp_path, reference_long):
    path = _write_backtest(tmp_path, reference_long, clim_offset=1e-6)
    out = tuned_to_long(path, reference_long)
    assert len(out) == len(reference_long)


def test_assemble_stacks_every_competitor_once(tmp_path, reference_long):
    reconstruction = tmp_path / "tcn.parquet"
    reference_long.to_parquet(reconstruction, index=False)
    out = assemble(
        [reconstruction],
        timesfm_parquet=_write_timesfm(tmp_path, reference_long),
        backtest_predictions=_write_backtest(tmp_path, reference_long),
    )
    assert set(out["model"]) == {"tcn_direct", "climatology", "timesfm", "tuned"}
    counts = out.groupby("model").size()
    assert counts.nunique() == 1, "cada competidor debe cubrir las mismas filas"


def test_assemble_requires_a_reconstruction_output():
    with pytest.raises(ValueError, match="al menos una salida"):
        assemble([])
