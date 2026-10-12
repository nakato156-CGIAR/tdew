"""Prueba pareada departamental (tdew-214.14.4): signo, fraccion de celdas y una fila por rival."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import departamental_pareado as dp


def _long():
    rng = np.random.default_rng(0)
    ids, days = np.arange(20), 30
    obs = 20 + rng.normal(size=(len(ids), days))
    rows = []
    for model, seed, noise in (("timesfm", 0, 0.5), ("tcn_direct", 0, 0.8), ("tcn_direct", 1, 0.6),
                               ("climatology", 0, 1.5)):
        pred = obs + rng.normal(scale=noise, size=obs.shape)
        rows.append(pd.DataFrame({"ID": np.repeat(ids, days), "TD_obs": obs.ravel(),
                                  "TD_pred": pred.ravel(), "model": model, "seed": seed}))
    return pd.concat(rows, ignore_index=True)


def test_one_row_per_rival_with_timesfm_minus_rival_sign():
    long = _long()
    table = dp.paired_table(long, n_boot=50, n_perm=50, seed=0).set_index(["rival", "rival_seed"])
    assert set(table.index) == {("tcn_direct", 0), ("tcn_direct", 1), ("climatology", 0)}
    err = long.assign(se=(long.TD_pred - long.TD_obs) ** 2).groupby(["model", "seed"])["se"].mean() ** 0.5
    row = table.loc[("tcn_direct", 0)]
    assert row["rmse_timesfm"] == pytest.approx(err[("timesfm", 0)])
    assert row["delta_rmse"] == pytest.approx(err[("timesfm", 0)] - err[("tcn_direct", 0)])
    assert row["delta_rmse"] < 0 and row["delta_lo"] <= row["delta_rmse"] <= row["delta_hi"]
    assert 0.0 <= row["frac_cells_timesfm_wins"] <= 1.0
    assert (table["cells"] == 20).all()
