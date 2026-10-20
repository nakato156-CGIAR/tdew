"""Pruebas minimas del desglose A1 (tdew-03g) con datos sinteticos."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from experiments.amenazas import desglose as d


def _synthetic(n_cells=40, n_days=60, seed=1):
    rng = np.random.default_rng(seed)
    ids = np.repeat(np.arange(n_cells), n_days)
    fecha = np.tile(pd.date_range("2009-01-01", periods=n_days), n_cells)
    obs = rng.normal(10, 3, ids.size)
    df = pd.DataFrame({
        "ID": ids, "FECHA": fecha, "TD_obs": obs,
        "a": obs + rng.normal(0, 1.0, ids.size),
        "b": obs + rng.normal(0, 1.5, ids.size),
        "zone_id": ids % 4, "zone_label": (ids % 4).astype(str),
        "lon": -80 + (ids % 8) * 1.3, "lat": -15 + (ids // 8) * 1.1,
    })
    df["c"] = df["a"]
    df["year"] = df.FECHA.dt.year
    df["month"] = df.FECHA.dt.month
    return df


def test_identical_methods_give_zero_gap():
    df = _synthetic()
    se = d.squared_errors(df, ["a", "c"])
    for scheme in ("espacial_2g", "mes_anio"):
        g = se.groupby(d.block_keys(df, scheme))
        out = d.block_bootstrap(g.size().to_numpy("f8"),
                                {m: g[m].sum().to_numpy("f8") for m in ("a", "c")},
                                [("a", "c")], n_boot=200)
        row = out.iloc[0]
        assert row.brecha == 0.0 and row.ic_lo == 0.0 and row.ic_hi == 0.0


def test_gap_sign_and_point_estimate():
    df = _synthetic()
    se = d.squared_errors(df, ["a", "b"])
    g = se.groupby(d.block_keys(df, "espacial_2g"))
    out = d.block_bootstrap(g.size().to_numpy("f8"),
                            {m: g[m].sum().to_numpy("f8") for m in ("a", "b")},
                            [("a", "b")], n_boot=300).iloc[0]
    expected = np.sqrt(se.a.mean()) - np.sqrt(se.b.mean())
    assert out.brecha == pytest.approx(expected)
    assert out.brecha < 0 and out.ic_lo <= out.brecha <= out.ic_hi and out.ic_hi < 0


def test_bootstrap_is_reproducible():
    n = np.array([5.0, 7.0, 3.0, 9.0])
    sums = {"x": np.array([4.0, 9.0, 2.0, 8.0]), "y": np.array([5.0, 6.0, 4.0, 7.0])}
    a = d.block_bootstrap(n, sums, [("x", "y")], n_boot=100)
    b = d.block_bootstrap(n, sums, [("x", "y")], n_boot=100)
    pd.testing.assert_frame_equal(a, b)


def test_zone_tables():
    df = _synthetic()
    methods = ["a", "b"]
    zl = d.per_zone(df, d.squared_errors(df, methods), methods)
    assert zl.zone_id.nunique() == 4 and len(zl) == 8
    wins = d.zone_wins(zl, methods)
    row = wins[(wins.metodo_a == "a") & (wins.metodo_b == "b")].iloc[0]
    assert row.zonas == 4 and row.zonas_a_gana == 4


def test_per_method_by_year():
    df = _synthetic(n_days=400)
    pm = d.per_method(df, ["a"])
    assert set(pm.periodo) == {"total", "2009", "2010"}
    tot = pm[pm.periodo == "total"].iloc[0]
    assert tot.n == len(df)


PANEL = Path("reports/timesfm_benchmark/panels/nacional_17027.csv")
GEO = Path("reports/timesfm_benchmark/geo/peru_departamental_simple.geojson")


@pytest.mark.skipif(not (PANEL.exists() and GEO.exists()), reason="sin panel o geojson")
def test_peru_mask_matches_published_count():
    ids = pd.read_csv(PANEL)["ID"].to_numpy()
    inside = d.peru_cells(ids)
    assert len(ids) == 17027
    assert int(inside.sum()) == d.N_PERU == 8272
    assert int((~inside).sum()) == 8755
