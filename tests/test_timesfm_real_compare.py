"""Acuerdo TimesFM - Palacios en flujo por bucket (tdew-214.13). Sin GPU, con datos sinteticos."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import real_compare as rc

DAYS = 1461
DATES = pd.date_range("2017-01-01", periods=DAYS)
IDS_A = [3, 8192 + 3, 2 * 8192 + 3]  # bucket 3
IDS_B = [5, 8192 + 5]  # bucket 5


def _tfm(ids, offset=0.0, bump=None):
    rows = []
    for k, i in enumerate(ids):
        base = 20.0 + k + 2.0 * np.sin(np.arange(DAYS) / 58.0) + offset
        if bump is not None:
            base = base + bump
        rows.append(pd.DataFrame({"ID": np.int32(i), "day": np.arange(DAYS, dtype=np.int16),
                                  "pred": base.astype(np.float32)}))
    return pd.concat(rows, ignore_index=True)


def _pal(ids, offset=0.0):
    rows = []
    for k, i in enumerate(ids):
        base = 20.0 + k + 2.0 * np.sin(np.arange(DAYS) / 58.0) + offset
        rows.append(pd.DataFrame({"FECHA": DATES, "ID": np.int64(i), "TD_predicted": base}))
    return pd.concat(rows, ignore_index=True)


def _tmin(ids, value=15.0):
    return pd.concat([pd.DataFrame({"ID": np.int64(i), "day": np.arange(DAYS, dtype=np.int16),
                                    "TMIN": np.float64(value)}) for i in ids], ignore_index=True)


def _meta(ids):
    return {"zone": pd.Series(7, index=pd.Index(ids)), "tier": pd.Series("within", index=pd.Index(ids)),
            "site": pd.Series("lima", index=pd.Index(ids))}


def test_agreement_is_timesfm_minus_palacios_with_the_right_sign():
    acc = rc.Accumulator()
    acc.add_bucket(3, _tfm(IDS_A, offset=0.5), _pal(IDS_A), meta=_meta(IDS_A))
    overall = acc.agreement_overall()
    assert overall["bias"] == pytest.approx(0.5, abs=1e-5)  # TimesFM mas calido => positivo
    assert overall["rmse"] == pytest.approx(0.5, abs=1e-5)
    assert overall["n"] == len(IDS_A) * DAYS
    assert overall["r"] == pytest.approx(1.0, abs=1e-6)


def test_streaming_matches_a_single_pass_regardless_of_bucket_split():
    rng = np.random.default_rng(0)
    noise_a, noise_b = rng.normal(0, 1, len(IDS_A) * DAYS), rng.normal(0, 1, len(IDS_B) * DAYS)
    a, b = _tfm(IDS_A), _tfm(IDS_B)
    a["pred"] += noise_a.astype(np.float32)
    b["pred"] += noise_b.astype(np.float32)
    acc = rc.Accumulator()
    acc.add_bucket(3, a, _pal(IDS_A), meta=_meta(IDS_A))
    acc.add_bucket(5, b, _pal(IDS_B), meta=_meta(IDS_B))
    d = np.concatenate([a["pred"].to_numpy(np.float64) - _pal(IDS_A)["TD_predicted"].to_numpy(),
                        b["pred"].to_numpy(np.float64) - _pal(IDS_B)["TD_predicted"].to_numpy()])
    res = acc.agreement_overall()
    assert res["bias"] == pytest.approx(d.mean(), abs=1e-9)
    assert res["rmse"] == pytest.approx(np.sqrt((d**2).mean()), abs=1e-9)
    assert res["mae"] == pytest.approx(np.abs(d).mean(), abs=1e-9)


def test_cut_by_year_month_zone_tier_and_site():
    acc = rc.Accumulator()
    tfm = _tfm(IDS_A)
    tfm.loc[tfm["day"] < 365, "pred"] += 1.0  # solo 2017
    acc.add_bucket(3, tfm, _pal(IDS_A), meta=_meta(IDS_A))
    by_year = acc.agreement_by("year").set_index("key")
    assert by_year.loc[2017, "bias"] == pytest.approx(1.0, abs=1e-5)
    assert by_year.loc[2018, "bias"] == pytest.approx(0.0, abs=1e-5)
    by_month = acc.agreement_by("month").set_index("key")
    assert by_month.loc[1, "bias"] == pytest.approx(0.25, abs=1e-5)  # 1 de 4 años afectados
    assert by_month.loc[2, "bias"] == pytest.approx(28 / (28 * 3 + 29), abs=1e-5)
    assert by_month.loc[2, "n"] == len(IDS_A) * (28 * 3 + 29)  # 2017,2018,2019 y 2020 bisiesto
    for dim, key in (("zone", 7), ("tier", "within"), ("site", "lima")):
        table = acc.agreement_by(dim).set_index("key")
        assert table.loc[key, "n"] == len(IDS_A) * DAYS


def test_month_is_the_calendar_month_of_the_date_not_of_the_day_index():
    acc = rc.Accumulator()
    tfm = _tfm(IDS_A)
    jan31 = tfm["day"] == 30  # 2017-01-31
    feb01 = tfm["day"] == 31  # 2017-02-01
    tfm.loc[jan31, "pred"] += 10.0
    acc.add_bucket(3, tfm, _pal(IDS_A), meta=_meta(IDS_A))
    m = acc.agreement_by("month").set_index("key")
    # Un unico dia de enero (por celda y anio) lleva el desfase; febrero queda limpio.
    assert m.loc[1, "bias"] > 0 and m.loc[2, "bias"] == pytest.approx(0.0, abs=1e-5)
    assert feb01.sum() == len(IDS_A)


def test_unmatched_rows_are_counted_not_hidden():
    acc = rc.Accumulator()
    tfm = _tfm(IDS_A)
    tfm = tfm[~((tfm["ID"] == IDS_A[0]) & (tfm["day"] == 10))]  # falta una fila en TimesFM
    pal = _pal(IDS_A + [IDS_A[0] + 3 * 8192])  # una celda extra solo en Palacios
    acc.add_bucket(3, tfm, pal, meta=_meta(IDS_A + [IDS_A[0] + 3 * 8192]))
    prod = acc.product_figures().set_index("product")
    assert prod.loc["palacios", "rows_only_in_this_product"] == DAYS + 1
    assert prod.loc["timesfm", "rows_only_in_this_product"] == 0
    assert acc.agreement_overall()["n"] == len(IDS_A) * DAYS - 1


def test_product_figures_mean_annual_range_and_nan():
    acc = rc.Accumulator()
    tfm = _tfm(IDS_A)
    tfm.loc[5, "pred"] = np.nan
    acc.add_bucket(3, tfm, _pal(IDS_A), meta=_meta(IDS_A))
    p = acc.product_figures().set_index("product")
    pal = _pal(IDS_A)["TD_predicted"]
    assert p.loc["palacios", "mean"] == pytest.approx(pal.mean())
    assert p.loc["palacios", "min"] == pytest.approx(pal.min())
    assert p.loc["palacios", "max"] == pytest.approx(pal.max())
    assert p.loc["timesfm", "nan"] == 1
    assert p.loc["palacios", "n"] == len(pal)
    pal_df = _pal(IDS_A)
    pal_2020 = pal_df[pal_df["FECHA"].dt.year == 2020]["TD_predicted"].mean()
    assert p.loc["palacios", "mean_2020"] == pytest.approx(pal_2020)
    assert p.loc["palacios", "cells"] == len(IDS_A)


def test_reproduction_control_flags_mismatch_and_passes_match():
    table = rc.reproduction_control(
        {"n": rc.PALACIOS_PAPER["n"], "mean": 19.39, "mean_2017": 19.36, "mean_2018": 19.30,
         "mean_2019": 19.41, "mean_2020": 19.51, "min": -13.29, "max": 41.16}, full_panel=True)
    assert table["ok"].all()
    bad = rc.reproduction_control(
        {"n": rc.PALACIOS_PAPER["n"], "mean": 19.45, "mean_2017": 19.36, "mean_2018": 19.30,
         "mean_2019": 19.41, "mean_2020": 19.51, "min": -13.29, "max": 41.16}, full_panel=True)
    assert not bad.set_index("quantity").loc["mean", "ok"]
    assert bad.set_index("quantity").loc["n", "ok"]
    partial = rc.reproduction_control({"n": 10, "mean": 1.0, "mean_2017": 1.0, "mean_2018": 1.0,
                                       "mean_2019": 1.0, "mean_2020": 1.0, "min": 0.0, "max": 1.0},
                                      full_panel=False)
    assert partial["ok"].isna().all()  # no aplica a un subconjunto


def test_horizon_drift_detects_a_planted_trend_with_hac_interval():
    acc = rc.Accumulator()
    trend = np.arange(DAYS) * (1.0 / DAYS)  # 1 degC por 1461 dias
    pieces = []
    for k, i in enumerate(IDS_A):
        pieces.append(pd.DataFrame({"ID": np.int32(i), "day": np.arange(DAYS, dtype=np.int16),
                                    "pred": (20.0 + k + trend).astype(np.float32)}))
    acc.add_bucket(3, pd.concat(pieces, ignore_index=True), _pal_flat(IDS_A), meta=_meta(IDS_A))
    drift = acc.horizon_drift()
    assert drift["slope_per_year"] == pytest.approx(365.25 / DAYS, rel=1e-3)
    assert drift["ci_low"] <= drift["slope_per_year"] <= drift["ci_high"]
    assert drift["significant"] is True or bool(drift["significant"])
    assert drift["last_minus_first_year"] == pytest.approx(3 * 365 / DAYS, rel=0.05)


def _pal_flat(ids):
    return pd.concat([pd.DataFrame({"FECHA": DATES, "ID": np.int64(i), "TD_predicted": 20.0 + k})
                      for k, i in enumerate(ids)], ignore_index=True)


def test_horizon_drift_is_not_significant_without_trend():
    acc = rc.Accumulator()
    rng = np.random.default_rng(1)
    tfm = _tfm(IDS_A)
    tfm["pred"] += rng.normal(0, 0.05, len(tfm)).astype(np.float32)
    acc.add_bucket(3, tfm, _pal(IDS_A), meta=_meta(IDS_A))
    assert not bool(acc.horizon_drift()["significant"])


def test_tmin_coherence_per_product():
    acc = rc.Accumulator()
    acc.add_bucket(3, _tfm(IDS_A), _pal(IDS_A), meta=_meta(IDS_A), tmin=_tmin(IDS_A, 15.0))
    t = acc.tmin_coherence().set_index("product")
    pal = _pal(IDS_A)["TD_predicted"].to_numpy()
    assert t.loc["palacios", "mean_td_minus_tmin"] == pytest.approx((pal - 15.0).mean())
    assert t.loc["palacios", "frac_td_gt_tmin"] == pytest.approx((pal > 15.0).mean())
    assert t.loc["timesfm", "n"] == len(IDS_A) * DAYS


def test_per_cell_table_has_one_row_per_cell_with_bias_and_rmse():
    acc = rc.Accumulator()
    acc.add_bucket(3, _tfm(IDS_A, offset=0.25), _pal(IDS_A), meta=_meta(IDS_A))
    cells = acc.per_cell()
    assert sorted(cells["ID"]) == sorted(IDS_A)
    assert cells["bias"].to_numpy() == pytest.approx(0.25, abs=1e-5)
    assert cells["n"].eq(DAYS).all()


def test_climatology_anomaly_series_subtracts_doy_mean(tmp_path):
    acc = rc.Accumulator()
    clim = np.full((len(IDS_A), 367), 18.0, dtype=np.float32)
    acc.add_bucket(3, _tfm(IDS_A), _pal(IDS_A), meta=_meta(IDS_A), clim=(np.array(IDS_A), clim))
    series = acc.anomaly_series()
    assert len(series) == DAYS
    # media diaria del producto menos 18
    expected = _pal(IDS_A).groupby("FECHA")["TD_predicted"].mean() - 18.0
    np.testing.assert_allclose(series["anom_palacios"].to_numpy(), expected.to_numpy(), atol=1e-9)


def test_write_outputs_use_limpio_suffix_and_sidecars(tmp_path):
    acc = rc.Accumulator()
    acc.add_bucket(3, _tfm(IDS_A), _pal(IDS_A), meta=_meta(IDS_A))
    written = rc.write_outputs(acc, tmp_path / "out", tmp_path / "agg", full_panel=False)
    names = {p.name for p in written}
    assert "agreement_overall_limpio.csv" in names
    assert "product_figures_limpio.csv" in names
    assert "reproduction_palacios_limpio.csv" in names
    assert all(p.name.endswith("_limpio.csv") for p in written)
    assert (tmp_path / "agg" / "agreement_by_cell_limpio.csv").exists()


def test_main_runs_over_synthetic_buckets_and_records_provenance(tmp_path, monkeypatch):
    # Producto TimesFM y de Palacios sinteticos, y un MLflow temporal.
    tfm_root, pal_root = tmp_path / "preds_real", tmp_path / "palacios"
    for bucket, ids in ((3, IDS_A), (5, IDS_B)):
        for root, frame in ((tfm_root, _tfm(ids)), (pal_root, _pal(ids))):
            d = root / f"id_bucket={bucket:04d}"
            d.mkdir(parents=True)
            frame.to_parquet(d / "pred.parquet", index=False)
    zone = pd.DataFrame({"ID": IDS_A + IDS_B, "zone_id": 1, "zone_label": "z", "lon": 0.0, "lat": 0.0})
    zone.to_parquet(tmp_path / "zone.parquet")
    sup = pd.DataFrame({"ID": IDS_A + IDS_B, "lon": 0.0, "lat": 0.0, "dist_km": 1.0, "tier": "within"})
    sup.to_parquet(tmp_path / "support.parquet")
    registry = tmp_path / "registry.jsonl"
    out = tmp_path / "out"
    code = rc.main([
        "--tfm-root", str(tfm_root), "--palacios-root", str(pal_root), "--zone-table", str(tmp_path / "zone.parquet"),
        "--support-distance", str(tmp_path / "support.parquet"), "--silver", str(tmp_path / "nosilver"),
        "--out-dir", str(out), "--agg-dir", str(tmp_path / "agg"), "--buckets", "3,5",
        "--registry-path", str(registry), "--repo-root", str(tmp_path),
        "--mlflow", "--mlflow-uri", f"sqlite:///{tmp_path / 'm.db'}",
    ])
    assert code == 0
    assert (out / "agreement_overall_limpio.csv").exists()
    rows = [json.loads(x) for x in registry.read_text().splitlines()]
    assert rows and rows[-1]["mlflow_run_id"] and rows[-1]["split_id"] == "real_2017_2020"
    assert rows[-1]["panel_cell_count"] == len(IDS_A) + len(IDS_B)
    assert "sin verdad observada" in rows[-1]["notes"]
    assert (out / "agreement_overall_limpio.csv.provenance.json").exists()


def test_annual_means_follow_the_paper_convention_mean_of_monthly_means():
    # Enero de 2017 vale 10, el resto del año 20: la media de medias mensuales pesa enero 1/12,
    # la media de celdas-dia lo pesa 31/365. El paper usa la primera (qc_fill.py).
    acc = rc.Accumulator()
    pal = _pal(IDS_A)
    jan17 = (pal["FECHA"].dt.year == 2017) & (pal["FECHA"].dt.month == 1)
    pal["TD_predicted"] = np.where(jan17, 10.0, 20.0)
    tfm = _tfm(IDS_A)
    acc.add_bucket(3, tfm, pal, meta=_meta(IDS_A))
    fig = acc.product_figures()
    p = fig.set_index("product").loc["palacios"]
    assert p["mean_2017_monthly"] == pytest.approx((10.0 + 11 * 20.0) / 12)
    assert p["mean_2017"] == pytest.approx((31 * 10.0 + 334 * 20.0) / 365)
    obs = rc.paper_convention_figures(fig, "palacios")
    assert obs["mean_2017"] == pytest.approx(p["mean_2017_monthly"])
    assert obs["mean_2018"] == pytest.approx(20.0)


def test_compare_and_tail_provenance_are_not_autoregressive(tmp_path):
    from experiments.timesfm import real_tail as rt

    kw = dict(n_cells=3, outputs=[tmp_path / "a.csv"], bead_id="tdew-214.14",
              tfm_root=tmp_path, palacios_root=tmp_path)
    assert rc.build_compare_provenance(ids_file=None, **kw).autoregressive is False
    assert rt.build_tail_provenance(**kw).autoregressive is False
