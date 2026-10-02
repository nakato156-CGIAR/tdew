"""Split `real` de TimesFM: contexto 1981-2016, horizonte 2017-2020 con Tmin futura (tdew-214.13)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.panel import build_panel, split_spec

BUCKET = 7
IDS = [8192 * 3 + BUCKET, 8192 * 5 + BUCKET, BUCKET]


def _write_historical(root, ids):
    dates = pd.date_range("1981-01-01", "2016-12-31", freq="D")
    directory = root / f"id_bucket={BUCKET:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    for year in range(1981, 2017):
        block = dates[dates.year == year]
        frames = [
            pd.DataFrame(
                {
                    "ID": location,
                    "FECHA": block,
                    "TD": (offset + np.sin(block.dayofyear / 58.0)).astype("float32"),
                    "TMIN": (offset + block.dayofyear / 100.0).astype("float32"),
                    "doy": block.dayofyear.astype("int16"),
                }
            )
            for offset, location in enumerate(ids)
        ]
        pd.concat(frames, ignore_index=True).to_parquet(directory / f"train_{year}.parquet")


def _write_future(root, ids, *, drop_last_day_of=None):
    directory = root / f"id_bucket={BUCKET:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    for year in range(2017, 2021):
        block = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
        frames = []
        for offset, location in enumerate(ids):
            dates = block
            if drop_last_day_of == location and year == 2020:
                dates = block[:-1]
            frames.append(
                pd.DataFrame(
                    {
                        "ID": np.int64(location),
                        "FECHA": dates.astype("datetime64[us]"),
                        # marca inequívoca: 500 + offset*10 + año-2017, constante en el año
                        "TMIN": np.float32(500 + offset * 10 + (year - 2017)),
                    }
                )
            )
        pd.concat(frames, ignore_index=True).to_parquet(directory / f"future_tmin_{year}.parquet")


@pytest.fixture
def roots(tmp_path):
    historical, future = tmp_path / "bucketed", tmp_path / "future"
    _write_historical(historical, IDS)
    _write_future(future, IDS)
    return historical, future


def test_real_split_dates_and_lengths():
    spec = split_spec("real")
    assert spec.context_start == pd.Timestamp("1981-01-01")
    assert spec.context_end == pd.Timestamp("2016-12-31")
    assert spec.holdout_start == pd.Timestamp("2017-01-01")
    assert spec.holdout_end == pd.Timestamp("2020-12-31")
    assert spec.context_length == 13149
    assert spec.horizon == 1461


def test_real_panel_reads_holdout_tmin_from_future_root(roots):
    historical, future = roots
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert panel is not None
    assert panel.td_ctx.shape == (3, 13149)
    assert panel.tmin_ctx.shape == (3, 13149)
    assert panel.tmin_hold.shape == (3, 1461)
    assert panel.td_hold.shape == (3, 1461)
    assert panel.hold_dates[0] == pd.Timestamp("2017-01-01")
    assert panel.hold_dates[-1] == pd.Timestamp("2020-12-31")
    # Cada celda recibe su propia marca por año (alineación por ID y fecha).
    for row, location in enumerate(panel.ids):
        offset = IDS.index(int(location))
        for year in range(2017, 2021):
            mask = panel.hold_dates.year == year
            assert np.all(panel.tmin_hold[row, mask] == 500 + offset * 10 + (year - 2017))


def test_real_panel_has_no_observed_td_in_holdout(roots):
    historical, future = roots
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert np.isnan(panel.td_hold).all()


def test_real_panel_context_and_climatology_are_train_only(roots):
    historical, future = roots
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert panel.ctx_dates[-1] == pd.Timestamp("2016-12-31")
    # Ninguna Tmin 2017+ (marca >= 500) puede entrar al contexto ni a la climatología.
    assert panel.tmin_ctx.max() < 100
    assert np.nanmax(panel.tmin_clim) < 100
    # doy 366 queda cubierto por los años bisiestos del contexto.
    assert not np.isnan(panel.td_clim[:, 366]).any()
    assert not np.isnan(panel.tmin_clim[:, 366]).any()


def test_real_panel_leap_year_doy_axis(roots):
    historical, future = roots
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert panel.hold_doy[-1] == 366  # 2020-12-31
    assert (panel.hold_dates == pd.Timestamp("2020-02-29")).sum() == 1


def test_real_panel_drops_cell_with_incomplete_future_tmin(tmp_path):
    historical, future = tmp_path / "bucketed", tmp_path / "future"
    _write_historical(historical, IDS)
    _write_future(future, IDS, drop_last_day_of=IDS[1])
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert panel is not None
    assert IDS[1] not in set(panel.ids.tolist())
    assert panel.n_cells == 2


def test_real_panel_requires_future_root(roots):
    historical, _ = roots
    with pytest.raises(ValueError, match="future_root"):
        build_panel(IDS, split_spec("real"), historical_root=historical)


def test_real_panel_cell_without_future_file_is_dropped(tmp_path):
    historical, future = tmp_path / "bucketed", tmp_path / "future"
    _write_historical(historical, IDS)
    _write_future(future, IDS[:2])  # la tercera celda no aparece en el futuro
    panel = build_panel(IDS, split_spec("real"), historical_root=historical, future_root=future)
    assert set(panel.ids.tolist()) == set(IDS[:2])


def test_ll_splits_still_read_holdout_from_historical(tmp_path):
    """Regresión: ll4 sigue leyendo el hold-out de `bucketed_training_data`."""
    historical = tmp_path / "bucketed"
    _write_historical(historical, IDS)
    panel = build_panel(IDS, split_spec("ll4"), historical_root=historical)
    assert panel is not None
    assert not np.isnan(panel.td_hold).any()
    assert panel.td_hold.shape == (3, 1461)
