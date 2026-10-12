"""accuracy_vs_cost: un punto por variante aunque runtime tenga corridas repetidas."""
from __future__ import annotations

import pandas as pd

from experiments.timesfm import plots


def test_cost_frame_has_one_row_per_variant_with_the_latest_runtime():
    board = pd.DataFrame({
        "split": "ll4",
        "method": ["timesfm:a", "timesfm:b", "tuned"],
        "rmse": [0.8, 0.9, 0.95],
    })
    runtime = pd.DataFrame({
        "variant": ["a", "a", "b", "retired"],
        "cells_per_second": [3.33, 3.21, 5.0, 9.9],
    })
    frame = plots.cost_frame(board, runtime, split="ll4", national_cells=3600)
    assert sorted(frame["variant"]) == ["a", "b"]
    row_a = frame[frame["variant"] == "a"].iloc[0]
    assert row_a["cells_per_second"] == 3.21           # la ultima corrida
    assert abs(row_a["horas_nacional"] - 3600 / 3.21 / 3600) < 1e-12
