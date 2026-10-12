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
