"""evaluate.score_split no debe pisar el n puntual con el n probabilistico (tdew-214.14.1)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.timesfm import evaluate as ev
from experiments.timesfm.probabilistic import COLUMNS


def test_point_n_survives_rows_with_missing_quantiles(tmp_path):
    dates = pd.date_range("2013-01-01", periods=10)
    ref = pd.DataFrame({"ID": 1, "zone_id": 3, "FECHA": dates, "TD_obs": np.linspace(10, 12, 10),
                        "pred_tuned": 11.0, "pred_clim": 10.5, "pred_tmin": 9.0, "pred_ols": 10.0})
    (tmp_path / "bt" / "ll4").mkdir(parents=True)
    ref.to_parquet(tmp_path / "bt" / "ll4" / "predictions.parquet")
    pred = pd.DataFrame({"ID": 1, "FECHA": dates, "pred": 11.2})
    for k, name in enumerate(COLUMNS):
        pred[name] = 10.0 + 0.2 * k
    pred.loc[0, "q10"] = np.nan  # una fila sin el cubo completo de deciles
    (tmp_path / "preds").mkdir()
    pred.to_parquet(tmp_path / "preds" / "ll4__tmin_anom_full.parquet")

    board, _ = ev.score_split(tmp_path / "preds", "ll4", backtest_root=tmp_path / "bt")
    row = board.set_index("method").loc["timesfm:tmin_anom_full"]
    assert row["n"] == 10
    assert row["n_prob"] == 9
