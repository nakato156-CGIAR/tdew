"""Garantias de no-fuga y de alineacion del panel de TimesFM (bead tdew-214)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.timesfm.panel import (
    build_panel,
    iter_panel_batches,
    merge_panels,
    split_spec,
)


@pytest.fixture
def historical_root(tmp_path):
    """Escribe un arbol `id_bucket=XXXX/train_YYYY.parquet` sintetico y verificable.

    El Td del bloque oculto se hace deliberadamente enorme (1000 + dia) para que
    cualquier fuga hacia el contexto sea imposible de pasar por alto.
    """
    root = tmp_path / "bucketed"
    ids = [8192 * 3 + 7, 8192 * 5 + 7, 7]  # tres celdas, todas del bucket 7
    dates = pd.date_range("1981-01-01", "2016-12-31", freq="D")
    for year in range(1981, 2017):
        mask = dates.year == year
        block = dates[mask]
        frames = []
        for offset, location in enumerate(ids):
            hidden = block.year >= 2013
            td = np.where(hidden, 1000.0 + block.dayofyear, offset + np.sin(block.dayofyear / 58.0))
            frames.append(
                pd.DataFrame(
                    {
                        "ID": location,
                        "FECHA": block,
                        "TD": td.astype("float32"),
                        "TMIN": (offset + block.dayofyear / 100.0).astype("float32"),
                        "doy": block.dayofyear.astype("int16"),
                    }
                )
            )
        directory = root / "id_bucket=0007"
        directory.mkdir(parents=True, exist_ok=True)
        pd.concat(frames, ignore_index=True).to_parquet(directory / f"train_{year}.parquet")
    return root, ids


def test_context_stops_before_the_hidden_block(historical_root):
    root, ids = historical_root
    panel = build_panel(ids, split_spec("ll4"), historical_root=root)
    assert panel is not None
    assert panel.ctx_dates[-1] == pd.Timestamp("2012-12-31")
    assert panel.hold_dates[0] == pd.Timestamp("2013-01-01")
    assert panel.td_ctx.shape[1] == 11688
    assert panel.td_hold.shape[1] == 1461
    # El bloque oculto vale >= 1000; el contexto jamas debe contener esos valores.
    assert panel.td_ctx.max() < 100.0
    assert panel.td_hold.min() >= 1000.0


def test_climatology_uses_only_training_years(historical_root):
    root, ids = historical_root
    panel = build_panel(ids, split_spec("ll4"), historical_root=root)
    # Si la climatologia hubiese visto 2013-2016 estaria contaminada por los 1000+.
    assert np.nanmax(panel.td_clim) < 100.0
    # Y debe coincidir con la media directa sobre los anios de train.
    reference = panel.td_ctx[:, panel.ctx_doy == 100].mean(axis=1)
    np.testing.assert_allclose(panel.td_clim[:, 100], reference, rtol=1e-5)


def test_short_context_trims_from_the_left_only(historical_root):
    root, ids = historical_root
    full = build_panel(ids, split_spec("ll4"), historical_root=root)
    short = build_panel(ids, split_spec("ll4", context_start_year=2011), historical_root=root)
    assert short.ctx_dates[-1] == full.ctx_dates[-1]
    assert short.td_ctx.shape[1] == 731
    np.testing.assert_allclose(short.td_ctx, full.td_ctx[:, -731:])


def test_anomaly_is_value_minus_train_only_climatology(historical_root):
    root, ids = historical_root
    panel = build_panel(ids, split_spec("ll4"), historical_root=root)
    anomaly = panel.anomaly("TD", block="context")
    np.testing.assert_allclose(
        anomaly, panel.td_ctx - panel.td_clim[:, panel.ctx_doy], rtol=1e-5
    )


def test_batches_accumulate_across_buckets_without_losing_cells(historical_root):
    root, ids = historical_root
    batches = list(
        iter_panel_batches(ids, split_spec("ll4"), historical_root=root, max_cells_per_batch=2)
    )
    assert sum(b.n_cells for b in batches) == len(ids)
    assert sorted(np.concatenate([b.ids for b in batches])) == sorted(ids)
    assert max(b.n_cells for b in batches) <= 2


def test_merge_preserves_row_order_and_calendar(historical_root):
    root, ids = historical_root
    batches = list(
        iter_panel_batches(ids, split_spec("ll4"), historical_root=root, max_cells_per_batch=1)
    )
    merged = merge_panels(batches)
    assert merged.n_cells == len(ids)
    assert list(merged.ctx_dates) == list(batches[0].ctx_dates)
    for index, batch in enumerate(batches):
        np.testing.assert_allclose(merged.td_ctx[index], batch.td_ctx[0])


def test_unknown_split_is_rejected():
    with pytest.raises(KeyError):
        split_spec("ll3")


def test_context_start_after_train_end_is_rejected():
    with pytest.raises(ValueError):
        split_spec("ll4", context_start_year=2013)


@pytest.fixture
def many_buckets(tmp_path):
    """Un arbol con seis buckets, una celda cada uno, para probar la pereza."""
    root = tmp_path / "bucketed"
    # Identificadores distintos modulo 8192, para que cada uno caiga en su propio
    # bucket y la prueba mida lo que dice medir.
    ids = [0, 1, 2, 3, 4, 5]
    dates = pd.date_range("1981-01-01", "2016-12-31", freq="D")
    for location in ids:
        directory = root / f"id_bucket={location % 8192:04d}"
        directory.mkdir(parents=True, exist_ok=True)
        for year in range(1981, 2017):
            block = dates[dates.year == year]
            pd.DataFrame(
                {
                    "ID": location,
                    "FECHA": block,
                    "TD": np.full(len(block), 1.0, dtype="float32"),
                    "TMIN": np.full(len(block), 2.0, dtype="float32"),
                    "doy": block.dayofyear.astype("int16"),
                }
            ).to_parquet(directory / f"train_{year}.parquet")
    return root, ids


def test_first_batch_does_not_require_reading_every_bucket(monkeypatch, many_buckets):
    """La lectura anticipada tiene que estar acotada, no abarcar todo el panel.

    `ThreadPoolExecutor.map` encola todas las tareas de golpe y retiene sus
    resultados, de modo que la huella en memoria crecia con el numero total de
    buckets y no con el tamano del lote. En una corrida real sobre 436.519 celdas
    repartidas en 8.192 buckets eso llego a 53 GB. El invariante que lo impide es
    que consumir el primer lote no obligue a leer todos los buckets.
    """
    root, ids = many_buckets
    from experiments.timesfm import panel as panel_module

    leidos: list[int] = []
    original = panel_module.build_panel

    def registrando(chunk, spec, *, historical_root, bucket=None):
        leidos.append(int(bucket))
        return original(chunk, spec, historical_root=historical_root, bucket=bucket)

    monkeypatch.setattr(panel_module, "build_panel", registrando)
    generador = panel_module.iter_panel_batches(
        ids, split_spec("ll4"), historical_root=root,
        max_cells_per_batch=1, read_workers=1,
    )
    primero = next(generador)
    assert primero.n_cells == 1
    # Ventana de dos buckets con read_workers=1: el primer lote no puede haber
    # exigido leer los seis.
    assert len(set(leidos)) <= 2, f"se leyeron {sorted(set(leidos))} antes del primer lote"

    restantes = list(generador)
    assert primero.n_cells + sum(b.n_cells for b in restantes) == len(ids)
    assert len(set(leidos)) == len(ids)


@pytest.fixture
def trending_root(tmp_path):
    """Como `historical_root` pero con Td y Tmin que suben 0,1 por anio: la climatologia
    depende de que anios se promedian."""
    root = tmp_path / "trend"
    ids = [8192 * 2 + 3, 3]
    directory = root / "id_bucket=0003"
    directory.mkdir(parents=True)
    for year in range(1981, 2017):
        block = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
        frames = [
            pd.DataFrame({
                "ID": location, "FECHA": block,
                "TD": (k + 0.1 * (year - 1981) + np.sin(block.dayofyear / 58.0)).astype("float32"),
                "TMIN": (5 + k + 0.1 * (year - 1981) + block.dayofyear / 100.0).astype("float32"),
                "doy": block.dayofyear.astype("int16"),
            })
            for k, location in enumerate(ids)
        ]
        pd.concat(frames, ignore_index=True).to_parquet(directory / f"train_{year}.parquet")
    return root, ids


def test_clim_start_year_defaults_to_the_context_start(trending_root):
    """Sin `clim_start_year` el panel es el de siempre: climatologia con los anios del contexto."""
    root, ids = trending_root
    a = build_panel(ids, split_spec("ll4b", context_start_year=2002), historical_root=root)
    b = build_panel(ids, split_spec("ll4b", context_start_year=2002, clim_start_year=2002), historical_root=root)
    np.testing.assert_array_equal(a.td_clim, b.td_clim)
    np.testing.assert_array_equal(a.td_ctx, b.td_ctx)
    # Fila 0 = ID 3 (desplazamiento 1). Media 2002..2008 en el doy 100: 1 + 0,1 * 24 + seno.
    assert a.ids[0] == 3
    np.testing.assert_allclose(a.td_clim[0, 100], 1 + 2.4 + np.sin(100 / 58.0), atol=1e-5)


def test_clim_start_year_decouples_climatology_from_context(trending_root):
    """Contexto 2002-2008 con climatologia 1981-2008: el contexto no cambia, la climatologia
    es la del contexto largo, y el bloque oculto sigue fuera de ambas."""
    root, ids = trending_root
    full = build_panel(ids, split_spec("ll4b"), historical_root=root)
    short_fixed = build_panel(ids, split_spec("ll4b", context_start_year=2002, clim_start_year=1981),
                              historical_root=root)
    short_own = build_panel(ids, split_spec("ll4b", context_start_year=2002), historical_root=root)
    assert short_fixed.ctx_dates[0] == pd.Timestamp("2002-01-01")
    np.testing.assert_array_equal(short_fixed.td_ctx, short_own.td_ctx)
    np.testing.assert_array_equal(short_fixed.td_clim, full.td_clim)
    np.testing.assert_array_equal(short_fixed.tmin_clim, full.tmin_clim)
    assert not np.allclose(short_own.td_clim[:, 1:], full.td_clim[:, 1:])
    np.testing.assert_array_equal(short_fixed.td_hold, full.td_hold)


def test_clim_start_year_outside_training_is_rejected():
    with pytest.raises(ValueError):
        split_spec("ll4b", clim_start_year=2009)
    with pytest.raises(ValueError):
        split_spec("ll4b", clim_start_year=1980)
