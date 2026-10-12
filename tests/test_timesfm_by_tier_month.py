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


def _float32_trap(n=1000, seed=3):
    """Datos donde restar y promediar en float32 pierde el valor de ``obs``:
    pred ~ 2**25 (separacion 2 entre float32) y obs < 1, de modo que
    ``pred - obs`` en float32 redondea de vuelta a ``pred``."""
    rng = np.random.default_rng(seed)
    obs = rng.uniform(0.1, 0.9, n).astype("float32")
    pred = (2**25 + 2 * rng.integers(0, 50, n)).astype("float32")
    return obs, pred


def test_float32_trap_premise_float32_arithmetic_is_wrong():
    # Precondicion: sin casteo, el resultado difiere de float64 por > 0,1.
    obs, pred = _float32_trap()
    err32 = float((pred - obs).mean())
    err64 = float((pred.astype("float64") - obs.astype("float64")).mean())
    assert abs(err32 - err64) > 0.1


def test_aggregates_use_float64_even_when_inputs_are_float32():
    obs, pred = _float32_trap()
    n = len(obs)
    df = pd.DataFrame({
        "ID": np.arange(n) % 4,
        "FECHA": pd.Timestamp("2016-03-01"),
        "TD_obs": obs, "tier": "within",
        **{c: pred for c in PRED_COLS},
    })
    expected = float((pred.astype("float64") - obs.astype("float64")).mean())
    got_month = monthly_bias(df, "ll4", dispersion=False).query("method == 'tuned'")
    assert got_month["bias_pooled"].iloc[0] == pytest.approx(expected, abs=1e-6)
    got_tier = tier_table(df, "ll4").query("method == 'tuned'")
    assert got_tier["bias"].iloc[0] == pytest.approx(expected, abs=1e-6)
    got_tier_month = monthly_bias_by_tier(df, "ll4").query("method == 'tuned'")
    assert got_tier_month["bias"].iloc[0] == pytest.approx(expected, abs=1e-6)
    direct = score(pred, obs)  # score recibe float32 y debe castear
    assert direct["bias"] == pytest.approx(expected, abs=1e-6)


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


def _monthly_tuned(overrides=None) -> pd.DataFrame:
    """Sesgo mensual de tuned ll4 con enero -0,402 y diciembre +0,017."""
    bias = {m: 0.05 for m in range(1, 13)}
    bias.update({1: -0.402, 12: 0.017, 6: -0.137})
    bias.update(overrides or {})
    return pd.DataFrame({
        "split": "ll4", "method": "tuned", "month": list(bias),
        "bias_pooled": list(bias.values()),
    })


def _ok_inputs(tmp_path):
    df = _panel(n_cells=10)
    t = tier_table(df, "ll4")
    cells = t[t["method"] == "tuned"].set_index("tier")["cells"].to_dict()
    return t, cells, _paper_csv(tmp_path, df)


def test_reproduction_check_positive_case_with_monthly(tmp_path):
    t, cells, csv = _ok_inputs(tmp_path)
    reproduction_check(t, paper_csv=csv, expected_cells=cells, monthly=_monthly_tuned())


def test_reproduction_check_uses_december_not_another_month(tmp_path):
    t, cells, csv = _ok_inputs(tmp_path)
    with pytest.raises(ReproductionError, match="diciembre"):
        reproduction_check(t, paper_csv=csv, expected_cells=cells,
                           monthly=_monthly_tuned({12: 0.2}))


def test_reproduction_check_peak_must_be_in_january(tmp_path):
    t, cells, csv = _ok_inputs(tmp_path)
    moved = _monthly_tuned({1: -0.1, 3: -0.402})
    with pytest.raises(ReproductionError, match="enero"):
        reproduction_check(t, paper_csv=csv, expected_cells=cells, monthly=moved)


def test_reproduction_check_peak_magnitude(tmp_path):
    t, cells, csv = _ok_inputs(tmp_path)
    with pytest.raises(ReproductionError, match="maximo"):
        reproduction_check(t, paper_csv=csv, expected_cells=cells,
                           monthly=_monthly_tuned({1: -0.5}))


@pytest.mark.parametrize("what", ["rmse", "december", "peak_month"])
def test_reproduction_check_nan_is_never_ok(tmp_path, what):
    t, cells, csv = _ok_inputs(tmp_path)
    monthly = _monthly_tuned()
    if what == "rmse":
        t = t.copy()
        t.loc[(t["method"] == "tuned") & (t["tier"] == "within"), "rmse"] = np.nan
    elif what == "december":
        monthly.loc[monthly["month"] == 12, "bias_pooled"] = np.nan
    else:
        monthly.loc[monthly["month"] == 1, "bias_pooled"] = np.nan
    with pytest.raises(ReproductionError):
        reproduction_check(t, paper_csv=csv, expected_cells=cells, monthly=monthly)


def _tiers_with_cells(by_tier: dict, splits=("ll4",)) -> pd.DataFrame:
    rows = [{"split": s, "tier": t, "method": "tuned", "cells": c}
            for s in splits for t, c in by_tier.items()]
    return pd.DataFrame(rows)


def test_panel_check_passes_for_expected_panel():
    by_tier = {"within": 3, "near": 2}
    btm.panel_check(_tiers_with_cells(by_tier, ("ll1", "ll2", "ll4")),
                    expected_total=5, expected_by_tier=by_tier)


def test_panel_check_fails_on_wrong_total_in_any_split():
    by_tier = {"within": 3, "near": 2}
    t = pd.concat([_tiers_with_cells(by_tier, ("ll1",)),
                   _tiers_with_cells({"within": 3, "near": 1}, ("ll2",))])
    with pytest.raises(ReproductionError, match="ll2"):
        btm.panel_check(t, expected_total=5, expected_by_tier=by_tier)


def test_panel_check_fails_on_wrong_tier_split_even_if_total_matches():
    t = _tiers_with_cells({"within": 2, "near": 3})
    with pytest.raises(ReproductionError, match="within"):
        btm.panel_check(t, expected_total=5, expected_by_tier={"within": 3, "near": 2})


def test_expected_panel_constants_match_the_paper():
    assert btm.EXPECTED_NATIONAL_CELLS == 17027 == sum(btm.EXPECTED_CELLS.values())
    assert btm.EXPECTED_CRIBADO_CELLS == {
        "within": 842, "near": 79, "marginal": 59, "extrapolated": 65, "unsupported": 47}
    assert sum(btm.EXPECTED_CRIBADO_CELLS.values()) == 1092


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


# ------------------------------------------------------------------- main

def _write_inputs(tmp_path, n_cells=10):
    merged = tmp_path / "merged" / "ll4"
    merged.mkdir(parents=True)
    df = _panel(n_cells=n_cells)
    df.drop(columns="tier").to_parquet(merged / "predictions.parquet", index=False)
    support = pd.DataFrame({"ID": range(n_cells), "tier": df.groupby("ID")["tier"].first().to_numpy()})
    support_path = tmp_path / "support.parquet"
    support.to_parquet(support_path)
    paper = _paper_csv(tmp_path, df)
    return df, support_path, paper


def _argv(tmp_path, support, paper, out="out"):
    return [
        "--merged-root", str(tmp_path / "merged"), "--splits", "ll4",
        "--support-distance", str(support), "--paper-csv", str(paper),
        "--out-dir", str(tmp_path / out), "--panel-id", "sintetico",
        "--registry-path", str(tmp_path / "registry.jsonl"),
    ]


def test_main_happy_path_writes_outputs_and_provenance(tmp_path, monkeypatch):
    import json
    _, support, paper = _write_inputs(tmp_path)
    monkeypatch.setattr(btm, "panel_check", lambda *a, **k: None)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    assert btm.main(_argv(tmp_path, support, paper)) == 0
    out = tmp_path / "out"
    for name in ("tiers_limpio.csv", "sesgo_mensual_limpio.csv", "sesgo_mes_tier_limpio.csv",
                 "tiers_texto_limpio.csv", "tiers_texto_limpio.md"):
        assert (out / name).exists(), name
    lines = (tmp_path / "registry.jsonl").read_text().strip().splitlines()
    assert len(lines) == len(METHOD_COLS)  # 1 split x 5 metodos
    sidecar = json.loads((out / "tiers_limpio.csv.provenance.json").read_text())
    assert sidecar["variant_label"] == "tmin_anom_full"  # el ultimo escritor es TimesFM


def test_main_returns_1_and_writes_nothing_when_control_fails(tmp_path):
    # Con datos sinteticos el panel real (17.027 celdas) no coincide: el control debe abortar.
    _, support, paper = _write_inputs(tmp_path)
    assert btm.main(_argv(tmp_path, support, paper)) == 1
    out = tmp_path / "out"
    assert not list(out.glob("*.csv")) if out.exists() else True
    assert not (tmp_path / "registry.jsonl").exists()


def test_main_calls_reproduction_check_before_writing(tmp_path, monkeypatch):
    _, support, paper = _write_inputs(tmp_path)
    monkeypatch.setattr(btm, "panel_check", lambda *a, **k: None)

    def boom(*a, **k):
        raise ReproductionError("fallo simulado")

    monkeypatch.setattr(btm, "reproduction_check", boom)
    assert btm.main(_argv(tmp_path, support, paper)) == 1
    out = tmp_path / "out"
    assert not list(out.glob("*.csv")) if out.exists() else True


# ----------------------------------------------------------------- MLflow

def _mlflow_inputs(n_cells=10):
    df = _panel(n_cells=n_cells)
    tiers = tier_table(df, "ll4")
    monthly = monthly_bias(df, "ll4", dispersion=True)
    return df, tiers, monthly


def test_log_mlflow_one_run_per_split_with_tier_and_month_metrics(tmp_path):
    from mlflow.tracking import MlflowClient

    _, tiers, monthly = _mlflow_inputs()
    uri = f"sqlite:///{tmp_path / 'mlflow.db'}"
    run_ids = btm.log_mlflow(
        tiers, monthly, splits=["ll4"], panel_id="nacional_17027_limpio", bead_id="tdew-0bt",
        tracking_uri=uri, experiment_name="test-timesfm",
    )
    assert set(run_ids) == {"ll4"}
    run = MlflowClient(tracking_uri=uri).get_run(run_ids["ll4"])
    row = tiers[(tiers["tier"] == "within") & (tiers["method"] == "timesfm")].iloc[0]
    assert run.data.metrics["timesfm_within_rmse"] == pytest.approx(row["rmse"])
    assert run.data.metrics["timesfm_within_skill"] == pytest.approx(row["skill"])
    assert "tuned_unsupported_rmse" in run.data.metrics or "tuned_extrapolated_rmse" in run.data.metrics
    dec = monthly[(monthly["method"] == "tuned") & (monthly["month"] == 12)].iloc[0]
    assert run.data.metrics["tuned_bias_m12"] == pytest.approx(dec["bias_pooled"])
    assert run.data.metrics["tuned_cell_bias_std_m12"] == pytest.approx(dec["cell_bias_std"])
    assert run.data.tags["dataset_version"] == "nacional_17027_limpio"
    assert run.data.params["split"] == "ll4"
    assert run.data.params["bead_id"] == "tdew-0bt"


def test_log_mlflow_overall_rmse_is_n_weighted_over_tiers(tmp_path):
    from mlflow.tracking import MlflowClient

    df, tiers, monthly = _mlflow_inputs()
    uri = f"sqlite:///{tmp_path / 'mlflow.db'}"
    run_ids = btm.log_mlflow(tiers, monthly, splits=["ll4"], panel_id="p", bead_id="b",
                             tracking_uri=uri, experiment_name="test-timesfm")
    run = MlflowClient(tracking_uri=uri).get_run(run_ids["ll4"])
    for method, col in METHOD_COLS.items():
        pooled = score(df[col].to_numpy(), df["TD_obs"].to_numpy())
        assert run.data.metrics[f"{method}_rmse_all"] == pytest.approx(pooled["rmse"])
        assert run.data.metrics[f"{method}_bias_all"] == pytest.approx(pooled["bias"])


def test_main_mlflow_flag_records_run_id_in_provenance(tmp_path, monkeypatch):
    import json
    from mlflow.tracking import MlflowClient

    _, support, paper = _write_inputs(tmp_path)
    monkeypatch.setattr(btm, "panel_check", lambda *a, **k: None)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    uri = f"sqlite:///{tmp_path / 'mlflow.db'}"
    argv = _argv(tmp_path, support, paper) + ["--mlflow", "--mlflow-uri", uri,
                                              "--mlflow-experiment", "test-timesfm"]
    assert btm.main(argv) == 0
    records = [json.loads(l) for l in (tmp_path / "registry.jsonl").read_text().splitlines()]
    run_ids = {r["mlflow_run_id"] for r in records}
    assert len(run_ids) == 1 and None not in run_ids  # 1 split -> 1 run
    run = MlflowClient(tracking_uri=uri).get_run(run_ids.pop())
    assert run.data.metrics["timesfm_rmse_all"] > 0


def test_main_without_mlflow_flag_leaves_run_id_empty(tmp_path, monkeypatch):
    import json

    _, support, paper = _write_inputs(tmp_path)
    monkeypatch.setattr(btm, "panel_check", lambda *a, **k: None)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    assert btm.main(_argv(tmp_path, support, paper)) == 0
    records = [json.loads(l) for l in (tmp_path / "registry.jsonl").read_text().splitlines()]
    assert all(r["mlflow_run_id"] is None for r in records)


# ------------------------------------- revision 2: panel_check dentro de main

def _expected(monkeypatch, *, cribado=None, cells=None, national=None):
    if cribado is not None:
        monkeypatch.setattr(btm, "EXPECTED_CRIBADO_CELLS", cribado)
    if cells is not None:
        monkeypatch.setattr(btm, "EXPECTED_CELLS", cells)
    if national is not None:
        monkeypatch.setattr(btm, "EXPECTED_NATIONAL_CELLS", national)


def _boom(*a, **k):
    raise AssertionError("no debe llamarse en este modo")


def _cribado_inputs(tmp_path, n_cells=10):
    df = _panel(n_cells=n_cells)
    backtest = tmp_path / "backtest" / "ll4"
    backtest.mkdir(parents=True)
    df.drop(columns=["tier", "pred_timesfm"]).to_parquet(backtest / "predictions.parquet", index=False)
    preds = tmp_path / "preds"
    preds.mkdir()
    tf = df[["ID", "FECHA"]].copy()
    tf["pred"] = df["pred_timesfm"].astype("float32")
    tf.to_parquet(preds / "ll4__tmin_anom_full.parquet", index=False)
    panel = tmp_path / "panel.csv"
    pd.DataFrame({"ID": range(n_cells)}).to_csv(panel, index=False)
    support = tmp_path / "support.parquet"
    pd.DataFrame({"ID": range(n_cells), "tier": df.groupby("ID")["tier"].first().to_numpy()}).to_parquet(support)
    return [
        "--preds-dir", str(preds), "--backtest-root", str(tmp_path / "backtest"),
        "--panel-file", str(panel), "--splits", "ll4", "--support-distance", str(support),
        "--out-dir", str(tmp_path / "out"), "--panel-id", "cribado_sintetico",
        "--registry-path", str(tmp_path / "registry.jsonl"),
    ]


def test_main_cribado_uses_cribado_panel_and_never_the_national_control(tmp_path, monkeypatch):
    _expected(monkeypatch, cribado={t: 2 for t in TIERS}, cells={t: 99 for t in TIERS}, national=999)
    monkeypatch.setattr(btm, "reproduction_check", _boom)
    assert btm.main(_cribado_inputs(tmp_path)) == 0
    assert (tmp_path / "out" / "tiers_cribado_limpio.csv").exists()
    assert not (tmp_path / "out" / "tiers_texto_limpio.csv").exists()


def test_main_cribado_fails_and_writes_nothing_when_panel_differs(tmp_path, monkeypatch):
    _expected(monkeypatch, cribado={**{t: 2 for t in TIERS}, "within": 3})
    monkeypatch.setattr(btm, "reproduction_check", _boom)
    assert btm.main(_cribado_inputs(tmp_path)) == 1
    out = tmp_path / "out"
    assert not list(out.glob("*.csv")) if out.exists() else True
    assert not (tmp_path / "registry.jsonl").exists()


def test_main_national_passes_with_expected_panel(tmp_path, monkeypatch):
    _, support, paper = _write_inputs(tmp_path)
    _expected(monkeypatch, cells={t: 2 for t in TIERS}, national=10)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    assert btm.main(_argv(tmp_path, support, paper)) == 0


def test_main_national_fails_when_only_the_total_differs(tmp_path, monkeypatch):
    _, support, paper = _write_inputs(tmp_path)
    _expected(monkeypatch, cells={t: 2 for t in TIERS}, national=11)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    assert btm.main(_argv(tmp_path, support, paper)) == 1
    assert not (tmp_path / "registry.jsonl").exists()


def test_panel_check_total_is_checked_independently_of_the_listed_tiers():
    # los tiers listados coinciden; un tier extra no listado cambia solo el total
    t = _tiers_with_cells({"within": 3, "near": 2, "marginal": 1})
    with pytest.raises(ReproductionError, match="6 celdas != 5"):
        btm.panel_check(t, expected_total=5, expected_by_tier={"within": 3, "near": 2})


# ----------------------------------------- revision 2: mes con fechas de borde

@pytest.mark.parametrize("edge", ["start", "end"])
def test_month_is_the_calendar_month_of_fecha_on_month_edges(edge):
    df = _panel(n_cells=6)
    period = df["FECHA"].dt.to_period("M")
    df["FECHA"] = (period.dt.to_timestamp() if edge == "start"
                   else period.dt.to_timestamp(how="end").dt.normalize())
    m = monthly_bias(df, "ll4", dispersion=False).query("method == 'tuned'").set_index("month")["bias_pooled"]
    ref = (df["pred_tuned"] - df["TD_obs"]).groupby(df["FECHA"].dt.month).mean()
    np.testing.assert_allclose(m.sort_index().to_numpy(), ref.sort_index().to_numpy())
    mt = monthly_bias_by_tier(df, "ll4").query("method == 'tuned' and tier == 'within'").set_index("month")["bias"]
    sub = df[df["tier"] == "within"]
    ref_t = (sub["pred_tuned"] - sub["TD_obs"]).groupby(sub["FECHA"].dt.month).mean()
    np.testing.assert_allclose(mt.sort_index().to_numpy(), ref_t.sort_index().to_numpy())


# ------------------------------------ revision 2: alertas y notas de proveniencia

def test_timesfm_alerts_flag_nan_instead_of_ignoring_it():
    t = pd.DataFrame([{"split": "ll4", "tier": "within", "method": "timesfm", "rmse": np.nan}])
    assert any("within" in a for a in btm.timesfm_alerts(t))
    ok = pd.DataFrame([{"split": "ll4", "tier": "within", "method": "timesfm",
                        "rmse": btm.EXPECTED_TIMESFM_RMSE["within"]}])
    assert btm.timesfm_alerts(ok) == []
    m = pd.DataFrame([{"split": "ll4", "method": "timesfm", "month": 1, "bias_pooled": np.nan}])
    assert any("mes 1" in a for a in btm.timesfm_alerts(ok, m))


def _notes(tmp_path):
    import json
    return {json.loads(l)["notes"] for l in (tmp_path / "registry.jsonl").read_text().splitlines()}


def test_national_notes_name_the_merge_not_an_unread_backtest_root(tmp_path, monkeypatch):
    _, support, paper = _write_inputs(tmp_path)
    monkeypatch.setattr(btm, "panel_check", lambda *a, **k: None)
    monkeypatch.setattr(btm, "reproduction_check", lambda *a, **k: None)
    assert btm.main(_argv(tmp_path, support, paper)) == 0
    (note,) = {n.split("cells=")[0] for n in _notes(tmp_path)}
    assert "merged_root=" in note and "backtest_root=" not in note


def test_cribado_notes_name_the_backtest_root(tmp_path, monkeypatch):
    _expected(monkeypatch, cribado={t: 2 for t in TIERS})
    assert btm.main(_cribado_inputs(tmp_path)) == 0
    assert all("backtest_root=" in n for n in _notes(tmp_path))
