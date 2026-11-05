"""Conteos independientes para identificar la misma celda a través de los años."""

import pandas as pd

from experiments.timesfm.artifact_kl_celdas import annual_counts


def test_counts_preserve_cells_years_and_half_open_interval():
    frame = pd.DataFrame({
        "ID": [10, 10, 10, 10, 20], "year": [2013, 2013, 2014, 2014, 2013],
        "obs": [20.0, 24.0, 23.9, 22.0, 21.0],
        "timesfm": [19.9, 23.0, 24.0, 24.1, 22.0],
        "llr": [20.0, 24.0, 23.0, 22.0, 25.0],
    })
    got = annual_counts(frame).set_index(["ID", "year"])
    assert got.loc[(10, 2013)].to_dict() == {"n": 2, "obs": 1, "timesfm": 1, "llr": 1}
    assert got.loc[(10, 2014)].to_dict() == {"n": 2, "obs": 2, "timesfm": 0, "llr": 2}
    assert got.loc[(20, 2013)].to_dict() == {"n": 1, "obs": 1, "timesfm": 1, "llr": 0}
    assert (20, 2014) not in got.index
    assert got.n.sum() == len(frame)
