"""Pruebas de experiments.timesfm.kl: divergencias, histogramas y seleccion de grupos."""
import numpy as np
import pandas as pd

from experiments.timesfm import kl


def test_identical_histograms_have_zero_divergence():
    counts = np.array([5, 10, 0, 3])
    out = kl.divergences(counts, counts)
    assert out["kl_obs_method"] == 0 and out["kl_method_obs"] == 0 and out["jsd"] == 0


def test_divergence_is_positive_and_asymmetric():
    a, b = np.array([50, 5, 1, 0]), np.array([5, 20, 20, 10])
    out = kl.divergences(a, b)
    assert out["kl_obs_method"] > 0 and out["jsd"] > 0
    assert out["kl_obs_method"] != out["kl_method_obs"]


def test_jsd_is_bounded_by_ln2():
    out = kl.divergences(np.array([1000, 0, 0]), np.array([0, 0, 1000]))
    assert 0 < out["jsd"] <= np.log(2)


def test_hist_counts_everything_and_reports_out_of_range():
    values = np.array([-25.0, -20.0, 0.0, 49.95, 50.0, 60.0])
    counts, out = kl._hist(values, 0.5)
    assert counts.sum() == len(values)
    assert out == 3  # -25, 50.0 y 60; -20 queda dentro
    assert counts[0] == 2  # -25 se pliega al primer bin junto con -20


def test_group_masks_split_tier_and_zone():
    frame = pd.DataFrame({"ID": [1, 1, 2, 3], "FECHA": pd.to_datetime(["2013-01-01", "2013-02-01", "2013-01-05", "2013-03-01"])})
    tier = pd.Series({1: "within", 2: "near", 3: "unsupported"})
    zone = pd.Series({1: 5, 2: 0, 3: 0})
    masks = kl.group_masks(frame, tier, zone)
    assert masks["tier|within"].sum() == 2 and masks["zona|selva A (r) A'"].sum() == 2
    assert masks["zona|resto"].sum() == 2 and masks["mes|01"].sum() == 2


def test_compute_prefers_the_closer_method():
    rng = np.random.default_rng(0)
    obs = rng.normal(20, 5, 20000)
    frame = pd.DataFrame({"ID": 1, "FECHA": pd.Timestamp("2013-01-01"), "obs": obs,
                          "palacios": obs + rng.normal(3, 1, obs.size), "timesfm": obs + rng.normal(0, 1, obs.size)})
    table, hist = kl.compute(frame, pd.Series({1: "within"}), pd.Series({1: 0}))
    t = table[(table.group == "todo") & (table.bin_width == "0.1")].set_index("method")
    assert t.loc["timesfm", "kl_obs_method"] < t.loc["palacios", "kl_obs_method"]
    assert hist[["obs", "palacios", "timesfm"]].sum().tolist() == [20000] * 3
