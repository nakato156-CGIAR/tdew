"""Pruebas de experiments.timesfm.kl_calido: deficit calido por grupo, shares y bootstrap de bloques."""
import numpy as np
import pandas as pd

from experiments.amenazas.desglose import block_keys
from experiments.timesfm import kl, kl_calido


def _synthetic(n_per_cell=400, seed=0):
    """Celdas 1-2 en la zona 10 (deficit en B: el metodo manda Td de 22 C a 25,5 C);
    celdas 3-4 en la zona 20 (prediccion = obs). Dos anios y dos meses."""
    rng = np.random.default_rng(seed)
    rows = []
    for cid, zone in ((1, 10), (2, 10), (3, 20), (4, 20)):
        obs = rng.uniform(15, 28, n_per_cell).astype(np.float32)
        pred = obs.astype("f8").copy()
        if zone == 10:
            in_b = (obs >= 20) & (obs < 24)
            pred[in_b] = 25.5
        rows.append(pd.DataFrame({
            "ID": cid, "zone_id": zone, "obs": obs,
            "timesfm": pred.astype(np.float32), "llr": pred, "clim": obs.copy(),
            "year": np.where(np.arange(n_per_cell) % 2 == 0, 2013, 2014).astype(np.int16),
            "month": np.where(np.arange(n_per_cell) % 4 < 2, 1, 7).astype(np.int8)}))
    frame = pd.concat(rows, ignore_index=True)
    cells = pd.DataFrame({"ID": [1, 2, 3, 4], "zone_label": ["Z10", "Z10", "Z20", "Z20"],
                          "lon": [-75.5, -73.5, -71.5, -69.5], "lat": [-10.0, -10.0, -14.0, -14.0],
                          "tier": ["within", "near", "within", "near"],
                          "dem_band": ["0-500", "0-500", ">3500", ">3500"],
                          "depto": ["LORETO", "LORETO", "PUNO", "PUNO"]})
    cells["block_2g"] = block_keys(cells, "espacial_2g")
    return frame, cells


def test_bin_index_matches_kl_hist():
    v = np.array([-25.0, -20.0, 0.0, 19.99, 20.0, 23.99, 24.0, 49.95, 50.0, 60.0], dtype=np.float32)
    counts, _ = kl._hist(v, kl.BIN_COARSE)
    nb = len(counts)
    assert np.array_equal(np.bincount(kl_calido._bin_index(v), minlength=nb), counts)
    lo = kl._edges(kl.BIN_COARSE)[kl_calido.b_bins()]
    assert lo.min() == 20.0 and lo.max() == 23.5 and len(lo) == 8


def test_one_zone_carries_all_the_deficit():
    frame, cells = _synthetic()
    tables = kl_calido.compute(frame, cells, n_boot=50)
    z = tables["zona"].set_index(["zone_id", "model"])
    assert np.isclose(z.loc[(10, "timesfm"), "share_B"], 1.0)
    assert np.isclose(z.loc[(20, "timesfm"), "share_B"], 0.0)
    assert z.loc[(10, "timesfm"), "delta_B"] < 0 and z.loc[(10, "timesfm"), "delta_Bp"] > 0
    assert z.loc[(10, "llr"), "bias_obs_B"] > 0          # pred - obs > 0 cuando obs en B
    assert z.loc[(10, "llr"), "bias_pred_Bp"] < 0        # obs - pred < 0 cuando pred en B'
    assert z.loc[(10, "timesfm"), "kl_B"] > 0
    assert np.isclose(z.loc[(20, "llr"), "delta_B"], 0.0) and np.isclose(z.loc[(20, "llr"), "kl_total"], 0.0)
    # clim = obs: sin deficit; share indefinido (denominador nacional 0)
    assert np.isclose(z.loc[(10, "clim"), "delta_B"], 0.0)
    # n_obs_B y n coherentes con los datos
    obs10 = frame.obs[frame.zone_id == 10]
    assert z.loc[(10, "timesfm"), "n_obs_B"] == int(((obs10 >= 20) & (obs10 < 24)).sum())
    assert z.loc[(10, "timesfm"), "n"] == len(obs10) and z.loc[(10, "timesfm"), "n_cells"] == 2


def test_shares_of_every_partition_sum_to_one():
    frame, cells = _synthetic()
    tables = kl_calido.compute(frame, cells, n_boot=20)
    for cut in ("zona", "dem", "depto", "tier", "anio", "mes", "anio_mes"):
        for m in ("timesfm", "llr"):
            t = tables[cut][tables[cut].model == m]
            assert np.isclose(t.share_B.sum(), 1.0), cut
            assert np.isclose(t.share_Bp.sum(), 1.0), cut
    # el departamento con el deficit es LORETO; la zona elegida para zona x anio es la 10
    d = tables["depto"].set_index(["depto", "model"])
    assert np.isclose(d.loc[("LORETO", "timesfm"), "share_B"], 1.0)
    za = tables["zona_anio"]
    assert set(za.zone_id) == {10} and set(za.model) == {"timesfm", "llr", "clim"}
    assert np.isclose(za[za.model == "timesfm"].share_B.sum(), 1.0)


def test_national_hist_matches_kl():
    frame, _ = _synthetic()
    h = kl_calido.national_hist(frame)
    assert h[["obs", "timesfm", "llr", "clim"]].sum().tolist() == [len(frame)] * 4
    ref, _ = kl._hist(frame.obs.to_numpy(), kl.BIN_COARSE)
    assert np.array_equal(h.obs.to_numpy(), ref[ref > 0])


def test_bootstrap_on_block_aggregates():
    rng = np.random.default_rng(1)
    k = 30
    n = rng.integers(500, 1500, k).astype("f8")
    obs_in = np.floor(n * 0.3)
    pred_in = {"a": np.floor(n * 0.2), "b": obs_in.copy()}
    ci = kl_calido.bootstrap_delta(n, obs_in, pred_in, n_boot=300, seed=0)
    point = (pred_in["a"].sum() - obs_in.sum()) / n.sum()
    assert ci["a"][0] <= point <= ci["a"][1] and ci["a"][1] < 0
    assert ci["b"] == (0.0, 0.0)
    # un solo bloque: sin IC
    assert all(np.isnan(x) for x in kl_calido.bootstrap_delta(n[:1], obs_in[:1], {"a": pred_in["a"][:1]})["a"])
    w = kl_calido.block_weights(k, 10)
    assert w.shape == (10, k) and np.all(w.sum(axis=1) == k)


def test_zone_and_year_tables_have_block_ci():
    frame, cells = _synthetic()
    tables = kl_calido.compute(frame, cells, n_boot=50)
    for cut in ("zona", "anio"):
        t = tables[cut]
        for scheme in ("espacial_2g", "mes_anio"):
            assert {f"delta_B_lo_{scheme}", f"delta_B_hi_{scheme}", f"bloques_{scheme}"} <= set(t.columns)
        r = t[t.model == "timesfm"]
        ok = r.delta_B_lo_mes_anio.notna()
        assert ok.any()
        assert (r.delta_B_lo_mes_anio[ok] <= r.delta_B[ok] + 1e-12).all()
        assert (r.delta_B[ok] <= r.delta_B_hi_mes_anio[ok] + 1e-12).all()
