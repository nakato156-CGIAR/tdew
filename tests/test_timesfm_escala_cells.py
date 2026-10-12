"""escala.score: ``cells`` del agregado son las celdas puntuadas; los pesos van en ``weight_cells``."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.timesfm import escala


def test_aggregate_reports_scored_cells_and_keeps_weights_apart(tmp_path):
    silver = tmp_path / "ids"
    silver.mkdir()
    # Cuatro departamentos de 10 celdas; solo se puntuan 2 por departamento.
    members = {site: list(range(100 * k, 100 * k + 10)) for k, site in enumerate(escala.SITES)}
    for site, ids in members.items():
        pd.DataFrame({"ID": ids}).to_csv(silver / f"{site}.csv", index=False)
    scored = [i for ids in members.values() for i in ids[:2]]
    dates = pd.date_range("2013-01-01", periods=5)
    rows = pd.DataFrame([(i, d) for i in scored for d in dates], columns=["ID", "FECHA"])
    rng = np.random.default_rng(0)
    rows["TD_obs"] = 20 + rng.normal(size=len(rows))
    rows["pred_clim"] = 20.0
    rows["pred_tuned"] = rows["TD_obs"] + 0.5
    rows.to_parquet(tmp_path / "bt.parquet")
    tfm = rows[["ID", "FECHA"]].assign(pred=rows["TD_obs"] + 0.2)
    tfm.to_parquet(tmp_path / "tfm.parquet")

    frame = escala.score(tmp_path / "tfm.parquet", tmp_path / "bt.parquet", silver=silver)
    agg = frame[frame["site"] == "ALL_reponderado"].set_index("method")
    assert (agg["cells"] == len(scored)).all()
    assert (agg["weight_cells"] == 40).all()
    per_site = frame[frame["site"].isin(escala.SITES)]
    assert (per_site["cells"] == 2).all() and (per_site["weight_cells"] == 10).all()
