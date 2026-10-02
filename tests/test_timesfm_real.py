"""Producto TimesFM 2017-2020 por buckets: sentinela, atomicidad, reanudacion (tdew-214.13).

El modelo se sustituye por una funcion de prediccion falsa: no hay GPU.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import pytest

from experiments.timesfm import real
from experiments.timesfm.panel import NUM_BUCKETS
from experiments.timesfm.variants import variant

from test_timesfm_real_panel import _write_future, _write_historical

BUCKET = 7
IDS = [BUCKET, 8192 * 3 + BUCKET, 8192 * 5 + BUCKET]
Q = 9


def fake_predict(model, panel, spec, *, batch_size, min_batch_size=1):
    """Anomalia = 0.1 * indice de celda; deciles crecientes. Devuelve (point, quantiles, batch)."""
    n, h = panel.n_cells, panel.td_hold.shape[1]
    base = (np.arange(n, dtype=np.float32)[:, None] * 0.1) * np.ones((n, h), dtype=np.float32)
    quant = base[:, :, None] + np.linspace(-1, 1, Q, dtype=np.float32)[None, None, :]
    return base, quant, batch_size


@pytest.fixture
def world(tmp_path):
    historical, future = tmp_path / "bucketed", tmp_path / "future"
    _write_historical(historical, IDS)
    _write_future(future, IDS)
    out = tmp_path / "preds_real"
    return historical, future, out


def _run(world, **kwargs):
    historical, future, out = world
    cells = kwargs.pop("cells", {BUCKET: np.array(sorted(IDS), dtype=np.int64)})
    return real.run_real(
        cells, out_dir=out, historical_root=historical, future_root=future,
        model=None, predict=fake_predict, min_free_gb=0, **kwargs,
    )


# ------------------------------------------------------------------ formato

def test_output_schema_order_and_dtypes(world):
    _run(world)
    table = pq.ParquetFile(world[2] / f"id_bucket={BUCKET:04d}" / "pred.parquet").read()
    assert table.schema.names == ["ID", "day", "pred"] + [f"q{i}0" for i in range(1, 10)]
    types = {f.name: str(f.type) for f in table.schema}
    assert types["ID"] == "int32" and types["day"] == "int16"
    # pyarrow imprime float32 como "float"
    assert all(types[c] == "float" for c in table.schema.names[2:])
    frame = table.to_pandas()
    assert len(frame) == 3 * 1461
    assert frame["day"].min() == 0 and frame["day"].max() == 1460
    assert frame.sort_values(["ID", "day"]).index.equals(frame.index)
    assert frame.groupby("ID")["day"].nunique().eq(1461).all()
    assert not frame.isna().any().any()
    q = frame[[f"q{i}0" for i in range(1, 10)]].to_numpy()
    assert (np.diff(q, axis=1) >= 0).all()


def test_prediction_is_anomaly_plus_train_climatology(world):
    historical, future, out = world
    _run(world)
    frame = pq.ParquetFile(out / f"id_bucket={BUCKET:04d}" / "pred.parquet").read().to_pandas()
    # Celda de menor ID = indice 0 => anomalia 0 => pred = climatologia de Td del doy.
    cell = frame[frame["ID"] == min(IDS)].sort_values("day")
    doy = pd.date_range("2017-01-01", periods=1461).dayofyear.to_numpy()
    expected = np.sin(doy / 58.0)  # offset 0 en el fixture
    # El fixture es la climatologia exacta: sin(doy/58) es identico cada anio.
    np.testing.assert_allclose(cell["pred"].to_numpy(), expected, atol=1e-5)


def test_day_to_date_roundtrip_including_leap_year():
    days = np.arange(1461, dtype=np.int16)
    dates = real.day_to_date(days)
    assert dates[0] == pd.Timestamp("2017-01-01")
    assert dates[-1] == pd.Timestamp("2020-12-31")
    assert pd.Timestamp("2020-02-29") in set(dates)
    np.testing.assert_array_equal(real.date_to_day(dates), days)
    assert dates[-1].dayofyear == 366


# ------------------------------------------------------------------ .done y manifiesto

def test_done_sentinel_contents(world):
    _run(world)
    done = json.loads((world[2] / f"id_bucket={BUCKET:04d}" / ".done").read_text())
    assert done["bucket"] == BUCKET
    assert done["cells_requested"] == 3 and done["cells_written"] == 3
    assert done["cells_omitted"] == []
    assert done["rows"] == 3 * 1461
    assert done["bytes"] == (world[2] / f"id_bucket={BUCKET:04d}" / "pred.parquet").stat().st_size
    assert len(done["sha256"]) == 64
    for key in ("ids_hash", "git_commit", "seconds", "cells_per_second", "code_version",
                "tf32", "timesfm_version", "generated_at", "quantile_violation_rows"):
        assert key in done


def test_omitted_cells_are_listed_with_reason(tmp_path):
    historical, future = tmp_path / "bucketed", tmp_path / "future"
    _write_historical(historical, IDS)
    _write_future(future, IDS[:2])  # la tercera no tiene Tmin futura
    out = tmp_path / "preds_real"
    real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                  historical_root=historical, future_root=future, model=None,
                  predict=fake_predict, min_free_gb=0)
    done = json.loads((out / f"id_bucket={BUCKET:04d}" / ".done").read_text())
    assert done["cells_written"] == 2 and done["cells_requested"] == 3
    assert [o["id"] for o in done["cells_omitted"]] == [max(IDS)]
    assert done["cells_omitted"][0]["reason"]


def test_manifest_has_one_row_per_done_bucket(world):
    _run(world)
    manifest = real.write_manifest(world[2])
    assert list(manifest["bucket"]) == [BUCKET]
    assert manifest.loc[0, "rows"] == 3 * 1461
    assert (world[2] / "MANIFEST.csv").exists()


# ------------------------------------------------------------------ reanudacion

def test_resume_skips_done_buckets(world):
    _run(world)
    calls = []

    def counting(model, panel, spec, **kw):
        calls.append(panel.n_cells)
        return fake_predict(model, panel, spec, **kw)

    historical, future, out = world
    summary = real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                            historical_root=historical, future_root=future, model=None,
                            predict=counting, min_free_gb=0)
    assert calls == []
    assert summary["buckets_skipped"] == 1 and summary["buckets_run"] == 0


def test_orphan_tmp_is_removed_and_bucket_redone(world):
    historical, future, out = world
    directory = out / f"id_bucket={BUCKET:04d}"
    directory.mkdir(parents=True)
    (directory / "pred.parquet.tmp").write_bytes(b"basura")
    _run(world)
    assert not (directory / "pred.parquet.tmp").exists()
    assert (directory / ".done").exists()


def test_bucket_without_done_is_redone_even_if_parquet_exists(world):
    _run(world)
    directory = world[2] / f"id_bucket={BUCKET:04d}"
    (directory / ".done").unlink()
    summary = _run(world)
    assert summary["buckets_run"] == 1 and (directory / ".done").exists()


def test_resume_refuses_when_ids_hash_differs(world):
    _run(world)
    other = {BUCKET: np.array(sorted(IDS)[:2], dtype=np.int64)}
    with pytest.raises(real.ResumeMismatch, match="ids_hash"):
        _run(world, cells=other)


def test_resume_refuses_when_code_version_differs(world):
    _run(world)
    path = world[2] / f"id_bucket={BUCKET:04d}" / ".done"
    done = json.loads(path.read_text())
    done["code_version"] = "otra"
    path.write_text(json.dumps(done))
    with pytest.raises(real.ResumeMismatch, match="code_version"):
        _run(world)


# ------------------------------------------------------------------ atomicidad y disco

def test_failure_in_prediction_leaves_no_parquet_nor_done(world):
    def boom(*a, **k):
        raise RuntimeError("fallo")

    historical, future, out = world
    with pytest.raises(RuntimeError):
        real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                      historical_root=historical, future_root=future, model=None,
                      predict=boom, min_free_gb=0)
    directory = out / f"id_bucket={BUCKET:04d}"
    assert not (directory / "pred.parquet").exists()
    assert not (directory / ".done").exists()


def test_failure_while_writing_leaves_no_partial_files(world, monkeypatch):
    def half_write(table, where, **kw):
        Path(where).write_bytes(b"PAR1 truncado")
        raise OSError("disco lleno")

    monkeypatch.setattr(real.pq, "write_table", half_write)
    historical, future, out = world
    with pytest.raises(OSError):
        real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                      historical_root=historical, future_root=future, model=None,
                      predict=fake_predict, min_free_gb=0)
    directory = out / f"id_bucket={BUCKET:04d}"
    assert not (directory / "pred.parquet").exists()
    assert not (directory / "pred.parquet.tmp").exists()
    assert not (directory / ".done").exists()


def test_non_finite_prediction_is_never_marked_done(world):
    def nan_predict(model, panel, spec, **kw):
        point, quant, b = fake_predict(model, panel, spec, **kw)
        point[0, 5] = np.nan
        return point, quant, b

    historical, future, out = world
    with pytest.raises(ValueError, match="no finit"):
        real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                      historical_root=historical, future_root=future, model=None,
                      predict=nan_predict, min_free_gb=0)
    assert not (out / f"id_bucket={BUCKET:04d}" / ".done").exists()


def test_disk_threshold_stops_without_partial_files(world):
    historical, future, out = world
    with pytest.raises(real.DiskSpaceError):
        real.run_real({BUCKET: np.array(sorted(IDS), dtype=np.int64)}, out_dir=out,
                      historical_root=historical, future_root=future, model=None,
                      predict=fake_predict, min_free_gb=10**9)
    assert not list(out.glob("id_bucket=*/*"))


def test_main_returns_nonzero_on_disk_threshold(world, monkeypatch, tmp_path):
    monkeypatch.setattr(real, "load_model", lambda *a, **k: None)
    monkeypatch.setattr(real, "enable_tf32", lambda: None)
    palacios = tmp_path / "palacios"
    d = palacios / f"id_bucket={BUCKET:04d}"
    d.mkdir(parents=True)
    pd.DataFrame({"ID": np.repeat(IDS, 2).astype("int64"),
                  "FECHA": pd.Timestamp("2017-01-01"), "TD_predicted": 1.0}).to_parquet(d / "pred.parquet")
    historical, future, out = world
    code = real.main([
        "--palacios-root", str(palacios), "--out-dir", str(out), "--historical-root", str(historical),
        "--future-root", str(future), "--buckets", str(BUCKET), "--min-free-gb", str(10**9),
        "--registry-path", str(tmp_path / "reg.jsonl"),
    ])
    assert code != 0


# ------------------------------------------------------------------ celdas y verificacion

def test_list_cells_groups_by_bucket_and_checks_directory(tmp_path):
    palacios = tmp_path / "palacios"
    for bucket, ids in ((7, IDS), (9, [9, 8192 + 9])):
        d = palacios / f"id_bucket={bucket:04d}"
        d.mkdir(parents=True)
        pd.DataFrame({"ID": np.repeat(ids, 3).astype("int64"),
                      "FECHA": pd.Timestamp("2017-01-01"), "TD_predicted": 1.0}).to_parquet(d / "pred.parquet")
    cells = real.list_cells(palacios)
    assert sorted(cells) == [7, 9]
    assert list(cells[7]) == sorted(IDS) and list(cells[9]) == [9, 8192 + 9]
    only = real.list_cells(palacios, buckets=[9])
    assert sorted(only) == [9]
    # Un ID en un directorio equivocado es un error, no un dato.
    bad = palacios / "id_bucket=0011"
    bad.mkdir()
    pd.DataFrame({"ID": [12], "FECHA": pd.Timestamp("2017-01-01"), "TD_predicted": 1.0}).to_parquet(bad / "pred.parquet")
    with pytest.raises(ValueError, match="bucket"):
        real.list_cells(palacios)


def test_verify_outputs_passes_clean_product_and_detects_corruption(world):
    _run(world)
    cells = {BUCKET: np.array(sorted(IDS), dtype=np.int64)}
    report = real.verify_outputs(world[2], cells)
    assert report["ok"].all()
    # Corrupcion: falta un dia de una celda.
    path = world[2] / f"id_bucket={BUCKET:04d}" / "pred.parquet"
    frame = pq.ParquetFile(path).read().to_pandas()
    frame = frame.drop(frame.index[10])
    frame.to_parquet(path, index=False)
    report = real.verify_outputs(world[2], cells)
    assert not report["ok"].all()


def test_verify_detects_missing_bucket_and_id_mismatch(world):
    _run(world)
    cells = {BUCKET: np.array(sorted(IDS), dtype=np.int64), 9: np.array([9], dtype=np.int64)}
    report = real.verify_outputs(world[2], cells)
    assert not report.set_index("bucket").loc[9, "ok"]
    cells2 = {BUCKET: np.array(sorted(IDS)[:2], dtype=np.int64)}
    assert not real.verify_outputs(world[2], cells2)["ok"].all()


def test_ids_hash_depends_on_ids_only_and_not_on_order():
    a = real.ids_hash(np.array([3, 1, 2]))
    assert a == real.ids_hash(np.array([1, 2, 3]))
    assert a != real.ids_hash(np.array([1, 2, 4]))


def test_total_cell_check_rejects_wrong_total():
    with pytest.raises(ValueError, match="2178827"):
        real.check_total({0: np.arange(10)})
    assert NUM_BUCKETS == 8192
    assert variant("tmin_anom_full").target == "TD_anom"
