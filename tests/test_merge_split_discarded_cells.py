"""merge_split debe informar las celdas de TimesFM que la referencia no tiene.

Con la referencia limpia (17.027 celdas) y las predicciones de TimesFM (17.041),
14 celdas de TimesFM se descartan en la union interna. ``cells_lost`` solo mira el
lado de la referencia y daria 0 sin mencionarlas.
"""
from __future__ import annotations

import pandas as pd

from experiments.timesfm.merge_predictions import merge_split

DATES = pd.date_range("2020-01-01", periods=3)


def _frame(ids, value_col):
    rows = [(i, d, 1.0) for i in ids for d in DATES]
    return pd.DataFrame(rows, columns=["ID", "FECHA", value_col])


def _setup(tmp_path, reference_ids, timesfm_ids):
    root = tmp_path / "ref"
    (root / "ll4").mkdir(parents=True)
    reference = _frame(reference_ids, "pred_tuned")
    reference["zone_id"] = 0
    reference.to_parquet(root / "ll4" / "predictions.parquet", index=False)
    variant = tmp_path / "ll4__v.parquet"
    _frame(timesfm_ids, "pred").to_parquet(variant, index=False)
    return root, variant


def test_reports_timesfm_cells_missing_from_reference(tmp_path):
    root, variant = _setup(tmp_path, ["a", "b"], ["a", "b", "x", "y", "z"])
    stats = merge_split("ll4", variant, backtest_root=root, out_root=tmp_path / "out")
    assert stats["cells_timesfm"] == 5
    assert stats["cells_timesfm_dropped"] == 3
    assert stats["cells_lost"] == 0
    assert stats["cells_merged"] == 2


def test_reports_reference_cells_missing_from_timesfm(tmp_path):
    root, variant = _setup(tmp_path, ["a", "b", "c"], ["a", "b"])
    stats = merge_split("ll4", variant, backtest_root=root, out_root=tmp_path / "out")
    assert stats["cells_lost"] == 1
    assert stats["cells_timesfm_dropped"] == 0
