"""E5 (desempeno por tier de soporte) y E8 (sesgo mensual) de TimesFM frente a
Palacios: funciones puras de ``experiments.timesfm.by_tier_month``."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import by_tier_month as btm
from experiments.timesfm.by_tier_month import (
    METHOD_COLS,
    TIERS,
    ReproductionError,
    attach_tier,
    load_panel,
    monthly_bias,
    monthly_bias_by_tier,
    reduced_table,
    reproduction_check,
    score,
    tier_table,
)

PRED_COLS = list(METHOD_COLS.values())


def _panel(n_cells=10, years=(2015, 2016), seed=0, tiers=None) -> pd.DataFrame:
    """Panel sintetico: n_cells celdas, un dia por mes por ano, con tier asignado."""
    rng = np.random.default_rng(seed)
    dates = pd.to_datetime(
        [f"{y}-{m:02d}-15" for y in years for m in range(1, 13)]
    )
    ids = np.repeat(np.arange(n_cells), len(dates))
    df = pd.DataFrame({"ID": ids, "FECHA": np.tile(dates, n_cells)})
    df["TD_obs"] = rng.normal(10, 3, len(df))
    for i, col in enumerate(PRED_COLS):
        df[col] = df["TD_obs"] + rng.normal(0.1 * i, 1 + 0.2 * i, len(df))
    tiers = tiers or [TIERS[i % len(TIERS)] for i in range(n_cells)]
    df["tier"] = df["ID"].map(dict(enumerate(tiers)))
    return df


# ---------------------------------------------------------------- score

def test_score_matches_reference_implementation():
    rng = np.random.default_rng(1)
    obs = rng.normal(size=500)
    pred = obs + rng.normal(0.2, 0.5, 500)
    s = score(pred, obs)
    err = pred - obs
    assert s["rmse"] == pytest.approx(np.sqrt(np.mean(err**2)))
    assert s["mae"] == pytest.approx(np.mean(np.abs(err)))
    assert s["bias"] == pytest.approx(np.mean(err))
    assert s["r"] == pytest.approx(np.corrcoef(pred, obs)[0, 1])


def test_score_drops_non_finite_pairs():
    obs = np.array([1.0, 2.0, 3.0, 4.0, np.nan])
    pred = np.array([1.5, 2.5, np.inf, 4.5, 5.0])
    s = score(pred, obs)
    assert s["n"] == 3
    assert s["bias"] == pytest.approx(0.5)


# ---------------------------------------------------------------- tiers

def test_attach_tier_merges_and_keeps_all_rows(tmp_path):
    df = _panel(n_cells=5).drop(columns="tier")
    support = pd.DataFrame({"ID": range(5), "tier": TIERS, "dist_km": range(5)})
    path = tmp_path / "support.parquet"
    support.to_parquet(path)
    out = attach_tier(df, path)
    assert len(out) == len(df)
    assert set(out["tier"]) == set(TIERS)


def test_attach_tier_fails_when_a_cell_has_no_tier(tmp_path):
    df = _panel(n_cells=5).drop(columns="tier")
    support = pd.DataFrame({"ID": range(4), "tier": TIERS[:4]})  # falta el ID 4
    path = tmp_path / "support.parquet"
    support.to_parquet(path)
    with pytest.raises(ValueError, match="sin tier"):
        attach_tier(df, path)


def test_tier_table_columns_order_and_skill():
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    assert list(t.columns[:4]) == ["split", "tier", "method", "cells"]
    for col in ("n", "rmse", "mae", "bias", "r", "clim_rmse", "skill"):
        assert col in t.columns
    assert set(t["method"]) == set(METHOD_COLS)
    # orden de tiers = TIERS
    order = list(dict.fromkeys(t["tier"]))
    assert order == [x for x in TIERS if x in order]
    np.testing.assert_allclose(t["skill"], 1 - t["rmse"] / t["clim_rmse"])
    clim = t[t["method"] == "climatology"]
    np.testing.assert_allclose(clim["skill"], 0.0, atol=1e-12)


def test_tier_table_cells_sum_to_total_cells():
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    per_method = t[t["method"] == "tuned"]
    assert per_method["cells"].sum() == df["ID"].nunique()


# ------------------------------------------------------------- mensual

def test_monthly_bias_pooled_matches_groupby():
    df = _panel(n_cells=6)
    m = monthly_bias(df, "ll4", dispersion=False)
    ref = (
        (df["pred_tuned"] - df["TD_obs"])
        .groupby(df["FECHA"].dt.month)
        .mean()
    )
    got = m[m["method"] == "tuned"].set_index("month")["bias_pooled"]
    np.testing.assert_allclose(got.sort_index().to_numpy(), ref.sort_index().to_numpy())
    assert {"split", "method", "month", "bias_pooled", "n", "cells"} <= set(m.columns)


def test_month_comes_from_fecha_not_from_another_column():
    df = _panel(n_cells=3, years=(2015, 2016))
    df["mes_emision"] = 1  # distractor: no debe usarse
    df["FECHA"] = df["FECHA"] + pd.Timedelta(days=0)
    m = monthly_bias(df, "ll4", dispersion=False)
    assert sorted(m["month"].unique()) == list(range(1, 13))
    # cada mes agrupa los dias de los dos anos
    n_per_month = m[m["method"] == "tuned"]["n"].unique()
    assert list(n_per_month) == [3 * 2]


def test_dispersion_only_filled_when_requested():
    df = _panel(n_cells=8)
    without = monthly_bias(df, "ll1", dispersion=False)
    assert without[["cell_bias_std", "cell_bias_p05", "cell_bias_p95"]].isna().all().all()
    with_ = monthly_bias(df, "ll4", dispersion=True)
    assert with_[["cell_bias_std", "cell_bias_p05", "cell_bias_p95"]].notna().all().all()
    row = with_[(with_["method"] == "tuned") & (with_["month"] == 3)].iloc[0]
    cell_month = (
        (df["pred_tuned"] - df["TD_obs"])[df["FECHA"].dt.month == 3]
        .groupby(df["ID"]).mean()
    )
    assert row["cell_bias_std"] == pytest.approx(np.std(cell_month.to_numpy()))
    assert row["cell_bias_p05"] == pytest.approx(np.percentile(cell_month, 5))
    assert row["cell_bias_p95"] == pytest.approx(np.percentile(cell_month, 95))


def test_monthly_bias_by_tier_shape_and_values():
    df = _panel(n_cells=10)
    m = monthly_bias_by_tier(df, "ll4")
    assert {"split", "tier", "method", "month", "bias", "n", "cells"} <= set(m.columns)
    assert len(m) == len(set(df["tier"])) * len(METHOD_COLS) * 12
    one = m[(m["tier"] == "within") & (m["method"] == "timesfm") & (m["month"] == 7)].iloc[0]
    sub = df[(df["tier"] == "within") & (df["FECHA"].dt.month == 7)]
    assert one["bias"] == pytest.approx((sub["pred_timesfm"] - sub["TD_obs"]).mean())


def test_float32_inputs_are_aggregated_in_float64():
    n = 2_000_000
    obs = np.zeros(n, dtype="float32")
    pred = np.full(n, 0.1, dtype="float32")
    df = pd.DataFrame({
        "ID": np.zeros(n, dtype="int64"),
        "FECHA": pd.Timestamp("2016-03-01"),
        "TD_obs": obs, "tier": "within",
        **{c: pred for c in PRED_COLS},
    })
    exact = float(np.float32(0.1))  # el valor real almacenado, en float64
    got = monthly_bias(df, "ll4", dispersion=False).query("method == 'tuned'")["bias_pooled"].iloc[0]
    assert got == pytest.approx(exact, abs=1e-15)
    assert monthly_bias(df, "ll4", dispersion=False)["bias_pooled"].dtype == np.float64


# ------------------------------------------------------------- reducida

def test_reduced_table_uses_tbl_tiers_layout():
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    r = reduced_table(t)
    assert list(r["tier"]) == [x for x in TIERS if x in set(df["tier"])]
    for m in ("timesfm", "tuned", "climatology"):
        assert f"{m}_rmse" in r.columns
    assert {"cells", "timesfm_skill", "tuned_skill", "tuned_bias"} <= set(r.columns)
    md = btm.reduced_markdown(r)
    assert md.startswith("|")
    assert "0.000" not in md.split("\n")[0]


# ------------------------------------------------- control reproduccion

def _paper_csv(tmp_path, df) -> Path:
    t = tier_table(df, "ll4")
    tuned = t[t["method"] == "tuned"].set_index("tier")
    out = pd.DataFrame({
        "split": "ll4", "tier": tuned.index, "cells": tuned["cells"].to_numpy(),
        "tuned_rmse": tuned["rmse"].to_numpy(),
    })
    path = tmp_path / "paper.csv"
    out.to_csv(path, index=False)
    return path


def test_reproduction_check_passes_on_consistent_data(tmp_path):
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    cells = t[t["method"] == "tuned"].set_index("tier")["cells"].to_dict()
    reproduction_check(
        t, paper_csv=_paper_csv(tmp_path, df), expected_cells=cells,
    )


def test_reproduction_check_raises_when_cell_count_changes(tmp_path):
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    cells = t[t["method"] == "tuned"].set_index("tier")["cells"].to_dict()
    cells["within"] += 1
    with pytest.raises(ReproductionError, match="celdas"):
        reproduction_check(t, paper_csv=_paper_csv(tmp_path, df), expected_cells=cells)


def test_reproduction_check_raises_when_tuned_rmse_differs(tmp_path):
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    cells = t[t["method"] == "tuned"].set_index("tier")["cells"].to_dict()
    csv = _paper_csv(tmp_path, df)
    paper = pd.read_csv(csv)
    paper.loc[0, "tuned_rmse"] += 1e-3
    paper.to_csv(csv, index=False)
    with pytest.raises(ReproductionError, match="RMSE"):
        reproduction_check(t, paper_csv=csv, expected_cells=cells)


def test_reproduction_check_raises_on_monthly_bias_mismatch(tmp_path):
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    cells = t[t["method"] == "tuned"].set_index("tier")["cells"].to_dict()
    m = monthly_bias(df, "ll4", dispersion=False)
    with pytest.raises(ReproductionError, match="sesgo"):
        reproduction_check(
            t, monthly=m, paper_csv=_paper_csv(tmp_path, df), expected_cells=cells,
            expected_dec_bias=0.017, expected_max_abs_bias=0.402,
        )


# ------------------------------------------------------------ load_panel

def test_load_panel_national_reads_merge_and_casts_float64(tmp_path):
    merged = tmp_path / "merged" / "ll4"
    merged.mkdir(parents=True)
    df = _panel(n_cells=4).drop(columns="tier")
    df[PRED_COLS + ["TD_obs"]] = df[PRED_COLS + ["TD_obs"]].astype("float32")
    df.to_parquet(merged / "predictions.parquet", index=False)
    out = load_panel("ll4", merged_root=tmp_path / "merged")
    assert all(out[c].dtype == np.float64 for c in PRED_COLS + ["TD_obs"])
    assert out["ID"].nunique() == 4


def test_load_panel_national_fails_when_a_column_is_missing(tmp_path):
    merged = tmp_path / "merged" / "ll4"
    merged.mkdir(parents=True)
    _panel(n_cells=2).drop(columns=["tier", "pred_timesfm"]).to_parquet(
        merged / "predictions.parquet", index=False
    )
    with pytest.raises(ValueError, match="pred_timesfm"):
        load_panel("ll4", merged_root=tmp_path / "merged")


def test_load_panel_cribado_joins_filters_and_reports(tmp_path, caplog):
    backtest = tmp_path / "backtest" / "ll4"
    backtest.mkdir(parents=True)
    base = _panel(n_cells=6).drop(columns=["tier", "pred_timesfm"])
    base.to_parquet(backtest / "predictions.parquet", index=False)
    preds_dir = tmp_path / "preds"
    preds_dir.mkdir()
    tf = base[["ID", "FECHA"]].copy()
    tf["pred"] = 1.0
    tf = tf[tf["ID"] != 5]  # una celda sin TimesFM
    tf.to_parquet(preds_dir / "ll4__tmin_anom_full.parquet", index=False)
    panel = tmp_path / "panel.csv"
    pd.DataFrame({"ID": [0, 1, 2, 5]}).to_csv(panel, index=False)
    out = load_panel(
        "ll4", backtest_root=tmp_path / "backtest", preds_dir=preds_dir,
        panel_file=panel, variant="tmin_anom_full",
    )
    assert sorted(out["ID"].unique()) == [0, 1, 2]
    assert (out["pred_timesfm"] == 1.0).all()
    assert out["pred_timesfm"].dtype == np.float64


# ---------------------------------------------------- integracion (datos)

RES = Path(os.environ.get(
    "RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"))
SUPPORT = RES / "tuning" / "support_distance.parquet"
CLEAN_LL4 = RES / "tuning" / "backtest_clean" / "ll4" / "predictions.parquet"
PAPER_CSV = Path(__file__).resolve().parents[1] / "reports/paper/scripts/validation_by_support.csv"


@pytest.mark.skipif(not (SUPPORT.exists() and CLEAN_LL4.exists()), reason="sin $RES")
def test_real_data_tuned_ll4_reproduces_paper_by_tier():
    cols = ["ID", "FECHA", "TD_obs", "pred_tuned", "pred_clim", "pred_tmin", "pred_ols"]
    df = pd.read_parquet(CLEAN_LL4, columns=cols)
    for c in cols[2:]:
        df[c] = df[c].astype("float64")
    df["pred_timesfm"] = df["pred_tuned"]  # no se evalua TimesFM aqui
    df = attach_tier(df, SUPPORT)
    t = tier_table(df, "ll4")
    got = t[t["method"] == "tuned"].set_index("tier")
    paper = pd.read_csv(PAPER_CSV).query("split == 'll4'").set_index("tier")
    for tier in TIERS:
        assert got.loc[tier, "cells"] == paper.loc[tier, "cells"]
        assert got.loc[tier, "rmse"] == pytest.approx(paper.loc[tier, "tuned_rmse"], abs=1e-6)
