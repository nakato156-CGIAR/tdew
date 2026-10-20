"""Control negativo de Tmin barajada (tdew-077): solo cambia la covariable del horizonte."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.panel import PanelBatch, shuffle_tmin, split_spec
from experiments.timesfm.run import build_provenance
from experiments.timesfm.variants import variant


@pytest.fixture
def panel():
    spec = split_spec("ll4b", context_start_year=2000)
    cells = 4
    ctx_dates = pd.date_range(spec.context_start, spec.context_end, freq="D")
    hold_dates = pd.date_range(spec.holdout_start, spec.holdout_end, freq="D")
    rng = np.random.default_rng(1)
    clim = rng.normal(size=(cells, 367)).astype("float32")
    return PanelBatch(
        spec=spec,
        ids=np.arange(cells, dtype=np.int64),
        td_ctx=rng.normal(size=(cells, len(ctx_dates))).astype("float32"),
        tmin_ctx=rng.normal(size=(cells, len(ctx_dates))).astype("float32"),
        td_hold=rng.normal(size=(cells, len(hold_dates))).astype("float32"),
        tmin_hold=rng.normal(size=(cells, len(hold_dates))).astype("float32"),
        td_clim=rng.normal(size=(cells, 367)).astype("float32"),
        tmin_clim=clim,
        ctx_doy=ctx_dates.dayofyear.to_numpy(dtype=np.int16),
        hold_doy=hold_dates.dayofyear.to_numpy(dtype=np.int16),
        ctx_dates=ctx_dates,
        hold_dates=hold_dates,
    )


def test_ll4b_split_is_2009_2012_trained_to_2008():
    spec = split_spec("ll4b")
    assert spec.train_end_year == 2008 and spec.holdout_years == (2009, 2012)


@pytest.mark.parametrize("mode", ["year", "cell"])
def test_shuffle_leaves_truth_and_context_untouched(panel, mode):
    out = shuffle_tmin(panel, mode, seed=3)
    np.testing.assert_array_equal(out.td_hold, panel.td_hold)
    np.testing.assert_array_equal(out.td_ctx, panel.td_ctx)
    np.testing.assert_array_equal(out.tmin_ctx, panel.tmin_ctx)
    assert out.tmin_hold.shape == panel.tmin_hold.shape
    assert not np.allclose(out.tmin_hold, panel.tmin_hold)


@pytest.mark.parametrize("mode", ["year", "cell"])
def test_shuffle_is_deterministic(panel, mode):
    a = shuffle_tmin(panel, mode, seed=3).tmin_hold
    b = shuffle_tmin(panel, mode, seed=3).tmin_hold
    np.testing.assert_array_equal(a, b)


def test_year_mode_is_a_donor_year_of_the_same_cell_and_doy(panel):
    out = shuffle_tmin(panel, "year", seed=0)
    # Cada valor barajado es la Tmin real de algun dia del contexto con el mismo doy.
    ctx = pd.Series(range(len(panel.ctx_doy)), index=panel.ctx_doy)
    for j in (0, 100, 365):
        doy = int(panel.hold_doy[j])
        candidates = panel.tmin_ctx[:, ctx[doy].to_numpy()]
        for cell in range(panel.n_cells):
            assert np.isclose(out.tmin_hold[cell, j], candidates[cell], atol=1e-4).any()


def test_year_mode_handles_leap_day_without_donor(panel):
    # 2012 es bisiesto: el doy 366 existe en el horizonte; el donante puede no serlo.
    out = shuffle_tmin(panel, "year", seed=5)
    assert np.isfinite(out.tmin_hold).all()


def test_unknown_mode_raises(panel):
    with pytest.raises(ValueError):
        shuffle_tmin(panel, "bogus")


def test_provenance_flags_the_negative_control(tmp_path):
    from pathlib import Path

    record = build_provenance(
        variant("tmin_td_full"),
        split="ll4",
        panel_spec=split_spec("ll4"),
        ids_file=Path("panel.csv"),
        cells=[1, 2],
        target=tmp_path / "x.parquet",
        tmin_shuffle="year",
        shuffle_seed=0,
    )
    assert "CONTROL NEGATIVO" in record.notes
