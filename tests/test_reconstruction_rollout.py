from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.reconstruction.rollout import direct_rollout, recursive_rollout


def test_direct_rollout_never_exposes_observed_td():
    hidden = pd.DataFrame({"ID": [1, 1], "date": pd.date_range("2013-01-01", periods=2), "x": [2.0, 3.0], "TD": [5.0, 99.0], "TD_anom": [1.0, 50.0]})

    def predict(frame):
        assert "TD" not in frame and "TD_anom" not in frame
        return frame["x"].to_numpy()

    np.testing.assert_array_equal(direct_rollout(hidden, predict), [2.0, 3.0])


def test_recursive_rollout_is_invariant_to_hidden_observations():
    history = pd.DataFrame({"ID": 1, "date": pd.date_range("2012-12-02", periods=30), "TD_anom": np.arange(30.0)})
    hidden = pd.DataFrame({"ID": [1, 1, 1], "date": pd.date_range("2013-01-01", periods=3), "TD": [100.0, 200.0, 300.0], "TD_anom": [90.0, 190.0, 290.0], "x": [1.0, 1.0, 1.0]})

    def predict(frame):
        return frame["TD_anom_lag1"].to_numpy(dtype=float) + 1.0

    expected = recursive_rollout(history, hidden, predict)
    modified = hidden.assign(TD=-999.0, TD_anom=-999.0)
    actual = recursive_rollout(history, modified, predict)
    np.testing.assert_array_equal(actual, expected)
    np.testing.assert_array_equal(actual, [30.0, 31.0, 32.0])

