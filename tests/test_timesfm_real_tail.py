"""Cola calida (Td > 35 C) de TimesFM y de Palacios sobre datos sinteticos (E9)."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm import real_tail as rt

DAYS = 1461
DATES = pd.date_range("2017-01-01", periods=DAYS)
NOV_2017 = 304  # 2017-11-01
IDS = [3, 8192 + 3, 2 * 8192 + 3]  # bucket 3
SELVA_SIN_APOYO, SELVA_CON_APOYO, RESTO_SIN_APOYO = IDS


def _meta():
    return {"zone": pd.Series([0, 0, 5], index=pd.Index(IDS)),
            "tier": pd.Series(["unsupported", "within", "unsupported"], index=pd.Index(IDS))}


def _tfm(planted=True):
    rows = []
    for i in IDS:
        v = np.full(DAYS, 25.0)
        if planted and i == SELVA_SIN_APOYO:
            v[NOV_2017:NOV_2017 + 6] = 36.0
            v[NOV_2017 + 1] = 39.0
        rows.append(pd.DataFrame({"ID": np.int32(i), "day": np.arange(DAYS, dtype=np.int16),
                                  "pred": v.astype(np.float32)}))
    return pd.concat(rows, ignore_index=True)


def _pal(planted=True):
    rows = []
    for i in IDS:
        v = np.full(DAYS, 25.0)
        if planted and i == SELVA_SIN_APOYO:
            v[NOV_2017:NOV_2017 + 3] = 36.0
            v[NOV_2017 + 2] = 38.5
        rows.append(pd.DataFrame({"FECHA": DATES, "ID": np.int64(i), "TD_predicted": v}))
    return pd.concat(rows, ignore_index=True)


@pytest.fixture()
def acc():
    a = rt.TailAccumulator()
    a.add_bucket(3, _tfm(), _pal(), meta=_meta())
    return a


def test_planted_days_fall_in_november_2017():
    assert DATES[NOV_2017].month == 11 and DATES[NOV_2017].year == 2017
    assert DATES[NOV_2017 - 1].month == 10


def test_summary_counts_values_above_each_threshold(acc):
    s = acc.summary().set_index("product")
    assert s.loc["timesfm", "above_35"] == 6 and s.loc["timesfm", "above_38"] == 1
    assert s.loc["palacios", "above_35"] == 3 and s.loc["palacios", "above_38"] == 1
    assert s.loc["timesfm", "max"] == pytest.approx(39.0) and s.loc["palacios", "max"] == pytest.approx(38.5)
    assert s.loc["timesfm", "n"] == 3 * DAYS
    assert s.loc["timesfm", "cells_with_exceedance"] == 1 and s.loc["timesfm", "cells"] == 3
    assert s.loc["timesfm", "pct_above_35"] == pytest.approx(100 * 6 / (3 * DAYS))


def test_threshold_is_strictly_above():
    a = rt.TailAccumulator()
    tfm = _tfm(planted=False)
    tfm.loc[tfm["ID"] == SELVA_SIN_APOYO, "pred"] = np.float32(35.0)
    a.add_bucket(3, tfm, _pal(planted=False), meta=_meta())
    assert a.summary().set_index("product").loc["timesfm", "above_35"] == 0


def test_by_tier_counts_cells_and_affected_cells(acc):
    t = acc.by_tier(_meta()["tier"]).set_index(["product", "tier"])
    assert t.loc[("timesfm", "unsupported"), "cells"] == 2
    assert t.loc[("timesfm", "unsupported"), "cells_affected"] == 1
    assert t.loc[("timesfm", "unsupported"), "above_35"] == 6
    assert t.loc[("timesfm", "within"), "cells_affected"] == 0
    assert t.loc[("timesfm", "within"), "above_35"] == 0
    assert t.loc[("timesfm", "unsupported"), "pct_field"] == pytest.approx(100 * 2 / 3)
    assert t.loc[("palacios", "unsupported"), "above_35"] == 3


def test_by_zone_class_separates_the_selva(acc):
    z = acc.by_zone_class(_meta()["zone"]).set_index(["product", "zone_class"])
    assert z.loc[("timesfm", "selva_A(r)A'"), "above_35"] == 6
    assert z.loc[("timesfm", "resto"), "above_35"] == 0
    assert z.loc[("timesfm", "selva_A(r)A'"), "share_of_all_exceedances"] == pytest.approx(100.0)
    assert z.loc[("timesfm", "selva_A(r)A'"), "cells"] == 2 and z.loc[("timesfm", "resto"), "cells"] == 1


def test_by_month_and_year_use_the_calendar_of_the_date(acc):
    m = acc.by_month().query("product == 'timesfm' and zone_class == \"selva_A(r)A'\"").set_index("month")
    assert m.loc[11, "above_35"] == 6 and m["above_35"].sum() == 6
    assert m.loc[11, "pct_above_35"] > m.loc[10, "pct_above_35"] == 0
    y = acc.by_year().query("product == 'timesfm'").set_index("year")
    assert y.loc[2017, "above_35"] == 6 and y.loc[2018, "above_35"] == 0
    assert y["values"].sum() == 3 * DAYS


def test_joint_table_overlaps_products_on_the_same_cell_days(acc):
    j = acc.joint_table().set_index("zone_class")
    assert j.loc["todo", "both_above_35"] == 3
    assert j.loc["todo", "only_timesfm"] == 3 and j.loc["todo", "only_palacios"] == 0
    assert j.loc["todo", "timesfm_above_given_palacios_above"] == pytest.approx(1.0)
    assert j.loc["todo", "palacios_above_given_timesfm_above"] == pytest.approx(0.5)
    assert j.loc["todo", "rows"] == 3 * DAYS
    assert j.loc["resto", "both_above_35"] == 0


def test_survival_curve_is_monotone_and_matches_the_planted_tail(acc):
    s = acc.survival()
    g = s.query("product == 'timesfm' and group == 'selva_sin_apoyo'").sort_values("x")
    assert g["n_group"].iloc[0] == DAYS
    assert (np.diff(g["frac_ge"].to_numpy()) <= 1e-12).all()
    at = g.set_index("x")
    assert at.loc[35.0, "n_ge"] == 6 and at.loc[39.0, "n_ge"] == 1 and at.loc[39.5, "n_ge"] == 0
    assert s.query("product == 'timesfm' and group == 'selva_con_apoyo' and x == 35.0")["n_ge"].iloc[0] == 0
    assert s.query("product == 'palacios' and group == 'todo' and x == 25.0")["n_ge"].iloc[0] == 3 * DAYS


def test_per_cell_lists_cells_with_any_exceedance_in_either_product(acc):
    c = acc.per_cell()
    assert list(c["ID"]) == [SELVA_SIN_APOYO]
    row = c.iloc[0]
    assert row["n_above_timesfm"] == 6 and row["n_above_palacios"] == 3
    assert row["max_timesfm"] == pytest.approx(39.0) and row["max_palacios"] == pytest.approx(38.5)


def test_a_cell_exceeding_only_in_palacios_is_still_listed():
    a = rt.TailAccumulator()
    a.add_bucket(3, _tfm(planted=False), _pal(), meta=_meta())
    c = a.per_cell().iloc[0]
    assert c["n_above_timesfm"] == 0 and c["n_above_palacios"] == 3
    assert c["max_timesfm"] == pytest.approx(25.0)


def test_streaming_over_two_buckets_equals_one_pass():
    two = rt.TailAccumulator()
    ids_b = [5, 8192 + 5]
    meta_b = {"zone": pd.Series([5, 5], index=pd.Index(ids_b)), "tier": pd.Series(["near", "near"], index=pd.Index(ids_b))}
    tfm_b = pd.DataFrame({"ID": np.repeat(np.int32(ids_b), DAYS), "day": np.tile(np.arange(DAYS, dtype=np.int16), 2),
                          "pred": np.float32(20.0)})
    pal_b = pd.DataFrame({"FECHA": np.tile(DATES, 2), "ID": np.repeat(np.int64(ids_b), DAYS), "TD_predicted": 20.0})
    two.add_bucket(3, _tfm(), _pal(), meta=_meta())
    two.add_bucket(5, tfm_b, pal_b, meta=meta_b)
    s = two.summary().set_index("product")
    assert s.loc["timesfm", "above_35"] == 6 and s.loc["timesfm", "n"] == 5 * DAYS and s.loc["timesfm", "cells"] == 5
    assert two.joint_table().set_index("zone_class").loc["todo", "rows"] == 5 * DAYS


def test_nan_is_counted_not_hidden_and_not_scored():
    a = rt.TailAccumulator()
    tfm = _tfm(planted=False)
    tfm.loc[:9, "pred"] = np.nan
    a.add_bucket(3, tfm, _pal(planted=False), meta=_meta())
    s = a.summary().set_index("product")
    assert s.loc["timesfm", "nan"] == 10 and s.loc["timesfm", "n"] == 3 * DAYS - 10


def test_cells_missing_from_the_metadata_are_unknown_tier_and_not_selva():
    a = rt.TailAccumulator()
    ids = [3]
    tfm = pd.DataFrame({"ID": np.int32(3), "day": np.arange(DAYS, dtype=np.int16), "pred": np.float32(40.0)})
    pal = pd.DataFrame({"FECHA": DATES, "ID": np.int64(3), "TD_predicted": 40.0})
    meta = {"zone": pd.Series(dtype=float), "tier": pd.Series(dtype=object)}
    a.add_bucket(3, tfm, pal, meta=meta)
    t = a.by_tier(meta["tier"]).set_index(["product", "tier"])
    assert t.loc[("timesfm", "desconocido"), "above_35"] == DAYS
    z = a.by_zone_class(meta["zone"]).set_index(["product", "zone_class"])
    assert z.loc[("timesfm", "resto"), "above_35"] == DAYS and z.loc[("timesfm", "selva_A(r)A'"), "above_35"] == 0


def test_write_outputs_use_limpio_suffix_and_the_cell_table_goes_to_agg(tmp_path, acc):
    written = rt.write_outputs(acc, tmp_path / "out", tmp_path / "agg", meta=_meta())
    names = {p.name for p in written}
    assert {"tail_summary_limpio.csv", "tail_by_tier_limpio.csv", "tail_by_zone_class_limpio.csv",
            "tail_by_month_limpio.csv", "tail_by_year_limpio.csv", "tail_joint_limpio.csv",
            "tail_survival_limpio.csv", "tail_by_cell_limpio.csv"} == names
    assert all(p.name.endswith("_limpio.csv") for p in written)
    assert (tmp_path / "agg" / "tail_by_cell_limpio.csv").exists()
    assert not (tmp_path / "out" / "tail_by_cell_limpio.csv").exists()


def test_main_runs_over_synthetic_buckets_and_records_provenance(tmp_path):
    tfm_root, pal_root = tmp_path / "preds_real", tmp_path / "palacios"
    d = tfm_root / "id_bucket=0003"
    d.mkdir(parents=True)
    _tfm().to_parquet(d / "pred.parquet", index=False)
    d = pal_root / "id_bucket=0003"
    d.mkdir(parents=True)
    _pal().to_parquet(d / "pred.parquet", index=False)
    meta = _meta()
    pd.DataFrame({"ID": IDS, "zone_id": meta["zone"].to_numpy(), "zone_label": "z", "lon": 0.0, "lat": 0.0}
                 ).to_parquet(tmp_path / "zone.parquet")
    pd.DataFrame({"ID": IDS, "lon": 0.0, "lat": 0.0, "dist_km": 1.0, "tier": meta["tier"].to_numpy()}
                 ).to_parquet(tmp_path / "support.parquet")
    registry, out = tmp_path / "registry.jsonl", tmp_path / "out"
    code = rt.main([
        "--tfm-root", str(tfm_root), "--palacios-root", str(pal_root), "--zone-table", str(tmp_path / "zone.parquet"),
        "--support-distance", str(tmp_path / "support.parquet"), "--out-dir", str(out),
        "--agg-dir", str(tmp_path / "agg"), "--buckets", "3", "--registry-path", str(registry),
        "--repo-root", str(tmp_path), "--mlflow", "--mlflow-uri", f"sqlite:///{tmp_path / 'm.db'}",
    ])
    assert code == 0
    assert (out / "tail_summary_limpio.csv").exists()
    rows = [json.loads(x) for x in registry.read_text().splitlines()]
    assert rows and rows[-1]["mlflow_run_id"] and rows[-1]["split_id"] == "real_2017_2020"
    assert rows[-1]["panel_cell_count"] == len(IDS)
    assert "sin verdad observada" in rows[-1]["notes"].lower()
    assert (out / "tail_summary_limpio.csv.provenance.json").exists()


def test_refuses_to_write_under_the_read_only_results_root(tmp_path):
    with pytest.raises(Exception):
        rt.main(["--out-dir", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/x",
                 "--agg-dir", str(tmp_path), "--registry-path", str(tmp_path / "r.jsonl"), "--buckets", "3"])
