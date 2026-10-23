"""Pruebas de experiments/paper_nuevo/analisis_descriptivo.py con datos sinteticos."""

from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.paper_nuevo import analisis_descriptivo as ad


def _frame(n_cells=4, n_days=400, seed=0):
    rng = np.random.default_rng(seed)
    ids = np.repeat(np.arange(n_cells), n_days)
    clim = np.tile(15 + 3 * np.sin(np.arange(n_days) / 58.0), n_cells)
    obs = clim + rng.normal(0, 1.5, len(ids))
    df = pd.DataFrame({"ID": ids, "TD_obs": obs, "clim": clim, "perfecto": obs.copy(),
                       "ruido": obs + rng.normal(0, 1.0, len(ids))})
    return df


def test_skill_perfecto_y_clim():
    df = _frame()
    t = ad.skill_table(df, ["perfecto", "clim", "ruido"]).set_index("metodo")
    assert t.loc["perfecto", "skill_mse"] == 1.0
    assert abs(t.loc["perfecto", "razon_varianza"] - 1.0) < 1e-12
    assert abs(t.loc["perfecto", "corr_anomalia"] - 1.0) < 1e-12
    assert t.loc["clim", "skill_mse"] == 0.0
    assert t.loc["clim", "razon_varianza"] == 0.0
    assert t.loc["ruido", "skill_mse"] < 1.0
    assert t.loc["ruido", "razon_varianza"] > 1.0  # el ruido anade varianza


def test_cobertura_cuantiles_calibrados():
    rng = np.random.default_rng(1)
    n = 200_000
    mu = rng.normal(20, 3, n)
    obs = mu + rng.normal(0, 1, n)
    from scipy.stats import norm
    q = mu[:, None] + norm.ppf(ad.probabilistic.LEVELS)[None, :]
    row = ad.calibration_row(obs, q)
    assert abs(row["cobertura_80"] - 0.8) < 0.005
    fr = [row[f"pit_frac_{i}"] for i in range(10)]
    assert abs(sum(fr) - 1) < 1e-12
    assert max(abs(f - 0.1) for f in fr) < 0.01


def test_pit_cuentas_y_desborde():
    q = np.tile(np.arange(1.0, 10.0), (3, 1))
    c = ad.pit_counts(np.array([0.0, 5.5, 100.0]), q)
    assert c[0] == 1 and c[5] == 1 and c[9] == 1 and c.sum() == 3


def test_clasificacion_oni_umbrales():
    assert ad.classify_oni(0.5) == "el_nino"
    assert ad.classify_oni(0.49) == "neutral"
    assert ad.classify_oni(-0.5) == "la_nina"
    assert ad.classify_oni(-0.49) == "neutral"
    assert ad.classify_oni(np.nan) == "sin_dato"


def test_oni_mes_central(tmp_path):
    p = tmp_path / "oni.txt"
    p.write_text(" SEAS  YR   TOTAL   ANOM\n  DJF 2010  26.0   1.5\n  JFM 2010  26.0  -0.6\n  NDJ 2010  26.0   0.0\n")
    t = ad.oni_monthly(p).set_index(["year", "month"])
    assert t.loc[(2010, 1), "clase"] == "el_nino"
    assert t.loc[(2010, 2), "clase"] == "la_nina"
    assert t.loc[(2010, 12), "clase"] == "neutral"


def test_umbrales_extremos_por_celda():
    rng = np.random.default_rng(2)
    ids = np.repeat([0, 1], 1000)
    x = np.r_[rng.normal(0, 1, 1000), rng.normal(0, 10, 1000)]
    lo, hi = ad.cell_thresholds(ids, x)
    for c in (0, 1):
        s = pd.Series(x[ids == c])
        assert np.allclose(lo[ids == c], s.quantile(0.05)) and np.allclose(hi[ids == c], s.quantile(0.95))
        assert abs((x[ids == c] >= hi[ids == c]).mean() - 0.05) < 0.002
    assert hi[0] < hi[1500]


def test_tabla_extremos_clases():
    df = _frame()
    ao = df.TD_obs - df.clim
    lo, hi = ad.cell_thresholds(df.ID.to_numpy(), ao.to_numpy())
    t = ad.extremes_table(df, ["perfecto", "ruido"], lo, hi)
    assert (t[t.metodo == "perfecto"].rmse == 0).all()
    n = t[t.metodo == "ruido"].set_index("clase").n
    assert abs(n["superior_5"] / len(df) - 0.05) < 0.01 and abs(n["inferior_5"] / len(df) - 0.05) < 0.01


def test_estratos_y_zona_dominante():
    df = _frame()
    df["year"] = 2010
    df["month"] = np.tile(np.arange(400) % 12 + 1, 4)
    df["timesfm_anom"] = df["perfecto"]
    df["zone_id"] = np.where(df.ID < 3, 0, 1)
    df["zone_label"] = np.where(df.ID < 3, "A", "B")
    lab = np.where(df.ID < 2, "x", "y")
    g = ad.grouped_rmse(df, ["timesfm_anom", "ruido"], lab, tipo="t")
    r = g[g.metodo == "ruido"]
    assert (r.brecha_tfm_menos_metodo < 0).all() and set(r.celdas) == {2}
    z = ad.dominant_zone_table(df, ["timesfm_anom", "ruido"])
    assert (z.zona_dominante == "A").all() and abs(z.frac_celdas.iloc[0] - 0.75) < 1e-12
