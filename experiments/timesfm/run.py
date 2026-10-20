"""Inferencia zero-shot de TimesFM sobre un panel, variante a variante.

Escribe un parquet largo por `(ID, FECHA)` con la prediccion mediana y los nueve
deciles, para que la evaluacion puntual y la probabilistica salgan de la misma
corrida. No entrena nada: el unico estado es el checkpoint descargado.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from tdew_estimation import provenance as prov

from .panel import (
    DEFAULT_HISTORICAL_ROOT,
    SPLITS,
    TMIN_SHUFFLE_MODES,
    PanelBatch,
    iter_panel_batches,
    shuffle_tmin,
    split_spec,
)
from .variants import CHECKPOINT_REVISION, Variant, parse_keys, variant

logger = logging.getLogger("timesfm.run")

QUANTILE_LEVELS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
QUANTILE_COLUMNS = tuple(f"q{int(round(q * 100)):02d}" for q in QUANTILE_LEVELS)

MANIFEST_REF = "docs/protocol/timesfm_manifest.yaml@2026-09-22"


def build_provenance(
    spec: Variant,
    *,
    split: str,
    panel_spec,
    ids_file: Path,
    cells: Sequence[int],
    target: Path,
    bead_id: str = "tdew-214",
    tmin_shuffle: str | None = None,
    shuffle_seed: int = 0,
    context_start_year: int | None = None,
    clim_start_year: int | None = None,
) -> prov.MetricProvenance:
    """El registro de proveniencia de una corrida (una variante, un split, un
    panel de celdas). Separado de ``run_variant`` para poder probarlo sin GPU
    ni modelo cargado.

    ``context_start_year`` y ``clim_start_year`` son las sobrescrituras de
    ``--context-start-year`` y ``--clim-start-year``: si alguna no es ``None`` queda en
    ``notes`` el contexto efectivo y los anios de la climatologia de las anomalias
    (``panel_spec.climatology_start_year`` a ``train_end``).
    """
    context_note = (
        f"; CONTEXTO desde {panel_spec.context_start_year} (--context-start-year={context_start_year};"
        f" la variante dice {spec.context_start_year}), {panel_spec.context_length} dias hasta"
        f" {panel_spec.context_end.date().isoformat()}; CLIMATOLOGIA de las anomalias con"
        f" {panel_spec.climatology_start_year}-{panel_spec.train_end_year}"
        f" (--clim-start-year={clim_start_year})"
        if context_start_year is not None or clim_start_year is not None
        else ""
    )
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=MANIFEST_REF,
        model_family=spec.family,
        model_id=spec.checkpoint,
        variant_label=spec.key,
        trained=False,
        training_period=None,
        validation_period=None,
        test_period=(
            panel_spec.holdout_start.date().isoformat(),
            panel_spec.holdout_end.date().isoformat(),
        ),
        split_id=split,
        autoregressive=spec.autoregressive,
        target_type=spec.target_type,
        climatology_used=spec.climatology_used,
        climatology_role=spec.climatology_role,
        inputs=tuple(spec.inputs),
        panel_id=ids_file.stem,
        panel_cell_count=len(cells),
        panel_file=str(ids_file),
        output_files=(str(target),),
        notes=f"checkpoint {spec.checkpoint}@{CHECKPOINT_REVISION}"
        + (
            f"; CONTROL NEGATIVO: Tmin del horizonte barajada (modo {tmin_shuffle}, semilla {shuffle_seed})"
            if tmin_shuffle
            else ""
        )
        + context_note,
    )


# ---------------------------------------------------------------------------------------
# Armado de entradas
# ---------------------------------------------------------------------------------------
def _doy_channels(doy: np.ndarray) -> np.ndarray:
    """Seno y coseno del dia del anio, periodo 366 (igual que pipeline/features.py:55)."""
    radians = 2.0 * np.pi * doy.astype(np.float32) / 366.0
    return np.stack([np.sin(radians), np.cos(radians)]).astype(np.float32)


def build_inputs(panel: PanelBatch, spec: Variant) -> tuple[list[np.ndarray], list[np.ndarray] | None]:
    """Contextos y covariables para un lote, ya en el formato que pide el modelo.

    La covariable futura debe medir exactamente ``contexto + horizonte``: su ancho
    es lo que define el horizonte dentro del modelo, sin validacion alguna
    (`timesfm3/torch/model.py:395-396`).
    """
    if spec.target == "TD":
        context = panel.td_ctx
    elif spec.target == "TD_anom":
        context = panel.anomaly("TD", block="context")
    else:
        raise ValueError(f"objetivo desconocido: {spec.target!r}")

    contexts = [np.ascontiguousarray(row, dtype=np.float32) for row in context]
    if not spec.covariates:
        return contexts, None

    channels: list[np.ndarray] = []
    for name in spec.covariates:
        if name == "TMIN":
            channels.append(np.concatenate([panel.tmin_ctx, panel.tmin_hold], axis=1))
        elif name == "TMIN_anom":
            channels.append(
                np.concatenate(
                    [panel.anomaly("TMIN", block="context"), panel.anomaly("TMIN", block="holdout")],
                    axis=1,
                )
            )
        elif name == "DOY":
            full_doy = np.concatenate([panel.ctx_doy, panel.hold_doy])
            shared = _doy_channels(full_doy)  # (2, C+H)
            channels.append(np.broadcast_to(shared[0], (panel.n_cells, shared.shape[1])))
            channels.append(np.broadcast_to(shared[1], (panel.n_cells, shared.shape[1])))
        else:
            raise ValueError(f"covariable desconocida: {name!r}")

    expected = panel.td_ctx.shape[1] + panel.td_hold.shape[1]
    covariates = []
    for cell in range(panel.n_cells):
        stacked = np.stack([np.asarray(ch[cell], dtype=np.float32) for ch in channels])
        if stacked.shape[1] != expected:
            raise ValueError(
                f"la covariable mide {stacked.shape[1]} y deberia medir {expected} "
                "(contexto + horizonte); un ancho distinto cambia el horizonte en silencio"
            )
        covariates.append(np.ascontiguousarray(stacked))
    return contexts, covariates


def to_physical(raw: np.ndarray, panel: PanelBatch, spec: Variant) -> np.ndarray:
    """Devuelve la prediccion en grados, deshaciendo la anomalia si hace falta.

    Acepta tanto la prediccion puntual, de forma ``(celdas, horizonte)``, como los
    cuantiles, de forma ``(celdas, horizonte, niveles)``. Ambos deben pasar por
    aqui: si solo se corrige el punto, las metricas probabilisticas de las
    variantes sobre anomalia quedan comparando grados contra anomalias.
    """
    if spec.target == "TD":
        return raw
    offset = panel.clim_for("TD", block="holdout")
    if raw.ndim == 3:
        offset = offset[:, :, None]
    return raw + offset


# ---------------------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------------------
def enable_tf32() -> None:
    """Activa TF32 en las multiplicaciones de matrices.

    PyTorch trae `float32_matmul_precision='highest'` por defecto, que desactiva
    los nucleos TF32 de Ampere. Medido en la RTX A2000 sobre 48 celdas con
    contexto 11.688 y horizonte 1.461: 1,44x mas rapido. La diferencia en la
    prediccion tiene un maximo de 0,0034 degC y un RMSE de 0,00043 degC entre
    ambas precisiones, lo que mueve el RMSE agregado del orden de 1e-7 degC,
    siete ordenes por debajo del efecto que este benchmark mide. La convolucion
    ya usaba TF32 (`cudnn.allow_tf32` viene en True); lo que faltaba era matmul.
    """
    import torch

    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.set_float32_matmul_precision("high")


def load_model(
    spec: Variant,
    *,
    device: str = "cuda",
    batch_size: int = 4,
):
    """Carga el modelo de la variante."""
    from timesfm3 import TimesFM3Forecaster

    model = TimesFM3Forecaster.from_pretrained(spec.checkpoint, device=device, revision=CHECKPOINT_REVISION)
    model.config.per_core_batch_size = int(batch_size)
    return model


def _predict_chunk(
    model,
    contexts: Sequence[np.ndarray],
    covariates: Sequence[np.ndarray] | None,
    horizon: int,
    spec: Variant,
) -> tuple[np.ndarray, np.ndarray]:
    outputs = list(
        model.predict_batch(
            contexts=list(contexts),
            horizon=horizon,
            past_future_covariates=list(covariates) if covariates is not None else None,
            return_quantiles=True,
            use_symmetric_averaging=spec.symmetric_averaging,
            make_positive=False,  # Cusco tiene Td negativo; el recorte por defecto lo destruiria
            sort_quantiles=True,
            use_znorm=spec.znorm,
            padding_mode="none",
        )
    )
    point = np.stack([np.asarray(o.forecast, dtype=np.float32).ravel()[:horizon] for o in outputs])
    quantiles = np.stack(
        [np.asarray(o.quantiles, dtype=np.float32).reshape(-1, len(QUANTILE_LEVELS))[:horizon] for o in outputs]
    )
    return point, quantiles


def predict_panel(
    model,
    panel: PanelBatch,
    spec: Variant,
    *,
    batch_size: int,
    min_batch_size: int = 1,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Predice un lote completo, reduciendo el batch ante OOM.

    El paquete no captura OOM ni reduce el batch por su cuenta
    (`timesfm3_forecaster.py:119-134` solo limpia cache), asi que el retroceso se
    hace aqui. Devuelve tambien el batch efectivo que sobrevivio.
    """
    import torch

    contexts, covariates = build_inputs(panel, spec)
    horizon = panel.td_hold.shape[1]
    size = int(batch_size)
    while True:
        try:
            points, quantiles = [], []
            for start in range(0, len(contexts), size):
                stop = start + size
                model.config.per_core_batch_size = size
                point, quant = _predict_chunk(
                    model,
                    contexts[start:stop],
                    covariates[start:stop] if covariates is not None else None,
                    horizon,
                    spec,
                )
                points.append(point)
                quantiles.append(quant)
            return np.concatenate(points), np.concatenate(quantiles), size
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if size <= min_batch_size:
                raise
            size = max(min_batch_size, size // 2)
            logger.warning("OOM: se reintenta con per_core_batch_size=%d", size)


# ---------------------------------------------------------------------------------------
# Escritura
# ---------------------------------------------------------------------------------------
_SCHEMA = pa.schema(
    [("ID", pa.int64()), ("FECHA", pa.timestamp("ns")), ("pred", pa.float32())]
    + [(name, pa.float32()) for name in QUANTILE_COLUMNS]
)


def _table(panel: PanelBatch, point: np.ndarray, quantiles: np.ndarray) -> pa.Table:
    n, horizon = point.shape
    columns = {
        "ID": np.repeat(panel.ids, horizon),
        "FECHA": np.tile(panel.hold_dates.to_numpy(), n),
        "pred": point.ravel(),
    }
    for index, name in enumerate(QUANTILE_COLUMNS):
        columns[name] = quantiles[:, :, index].ravel()
    return pa.Table.from_pydict(columns, schema=_SCHEMA)


def output_name(
    split: str,
    key: str,
    *,
    shard: tuple[int, int] | None = None,
    context_start_year: int | None = None,
    clim_start_year: int | None = None,
) -> str:
    """Nombre del parquet: ``<split>__<key>[__ctx<anio>][__clim<anio>][__shard<i>de<n>].parquet``."""
    ctx = f"__ctx{int(context_start_year)}" if context_start_year is not None else ""
    ctx += f"__clim{int(clim_start_year)}" if clim_start_year is not None else ""
    suffix = f"__shard{shard[0]}de{shard[1]}" if shard else ""
    return f"{split}__{key}{ctx}{suffix}.parquet"


def run_variant(
    keys: Iterable[str],
    *,
    split: str,
    ids: Sequence[int],
    ids_file: Path,
    out_dir: Path,
    historical_root: Path = DEFAULT_HISTORICAL_ROOT,
    batch_size: int = 4,
    cells_per_batch: int = 256,
    device: str = "cuda",
    tf32: bool = True,
    shard: tuple[int, int] | None = None,
    bead_id: str = "tdew-214",
    future_root: Path | None = None,
    tmin_shuffle: str | None = None,
    shuffle_seed: int = 0,
    context_start_year: int | None = None,
    clim_start_year: int | None = None,
) -> pd.DataFrame:
    """Corre una o varias variantes sobre el mismo conjunto de celdas.

    ``shard = (i, n)`` toma una de ``n`` porciones disjuntas de las celdas, para
    repartir una pasada grande entre varios procesos sobre la misma GPU. Medido:
    dos procesos concurrentes rinden ~1,7x lo de uno solo, porque un proceso con
    lotes pequenos no llena los 26 multiprocesadores de la tarjeta.

    ``context_start_year`` sobrescribe el anio de inicio del contexto de cada
    variante (escalera de contexto, tdew-03g) y anade ``__ctx<anio>`` al nombre del
    parquet para no pisar la salida de la variante con su contexto propio.
    ``clim_start_year`` fija el primer anio de la climatologia de las anomalias con
    independencia del contexto (``__clim<anio>`` en el nombre); por defecto coincide
    con el inicio del contexto, como en las corridas anteriores.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    if device == "cuda" and tf32:
        enable_tf32()
    # El reparto es por resto del identificador, no por bloques contiguos: los IDs
    # son densos en orden row-major, asi que un corte contiguo daria a cada proceso
    # una franja geografica distinta y sus tiempos serian dispares.
    cells = sorted({int(v) for v in ids})
    label = ""
    if shard is not None:
        index, total = shard
        cells = [c for c in cells if c % total == index]
        label = f" [porcion {index + 1} de {total}]"
        if not cells:
            raise ValueError(f"la porcion {index}/{total} quedo vacia")

    rows = []
    for key in keys:
        spec = variant(key)
        start_year = spec.context_start_year if context_start_year is None else int(context_start_year)
        panel_spec = split_spec(split, context_start_year=start_year, clim_start_year=clim_start_year)
        target = out_dir / output_name(
            split, key, shard=shard, context_start_year=context_start_year, clim_start_year=clim_start_year
        )
        logger.info(
            "[%s]%s %s | contexto %d d, horizonte %d d, %d celdas",
            key,
            label,
            spec.describe(),
            panel_spec.context_length,
            panel_spec.horizon,
            len(cells),
        )
        model = load_model(spec, device=device, batch_size=batch_size)
        writer = pq.ParquetWriter(target, _SCHEMA, compression="zstd")
        seen, effective, started = 0, batch_size, time.time()
        try:
            for panel in iter_panel_batches(
                cells,
                panel_spec,
                historical_root=historical_root,
                max_cells_per_batch=cells_per_batch,
                future_root=future_root,
            ):
                if tmin_shuffle:
                    panel = shuffle_tmin(panel, tmin_shuffle, shuffle_seed)
                point, quantiles, effective = predict_panel(
                    model, panel, spec, batch_size=effective
                )
                writer.write_table(
                    _table(
                        panel,
                        to_physical(point, panel, spec),
                        to_physical(quantiles, panel, spec),
                    )
                )
                seen += panel.n_cells
                logger.info(
                    "[%s] %d celdas, %.2f celdas/s", key, seen, seen / max(time.time() - started, 1e-9)
                )
        finally:
            writer.close()
            del model
            import torch

            torch.cuda.empty_cache()
        elapsed = time.time() - started
        rows.append(
            {
                "variant": key,
                "split": split,
                "shard": f"{shard[0]}/{shard[1]}" if shard else "",
                "cells": seen,
                "context_start_year": panel_spec.context_start_year,
                "clim_start_year": panel_spec.climatology_start_year,
                "context_days": panel_spec.context_length,
                "horizon_days": panel_spec.horizon,
                "seconds": elapsed,
                "cells_per_second": seen / elapsed if elapsed else np.nan,
                "effective_batch": effective,
                "output": str(target),
            }
        )
        prov.record_metric_provenance(
            build_provenance(
                spec,
                split=split,
                panel_spec=panel_spec,
                ids_file=ids_file,
                cells=cells,
                target=target,
                bead_id=bead_id,
                tmin_shuffle=tmin_shuffle,
                shuffle_seed=shuffle_seed,
                context_start_year=context_start_year,
                clim_start_year=clim_start_year,
            )
        )
        logger.info("[%s] listo en %.1f s -> %s", key, elapsed, target)
    return pd.DataFrame(rows)


def read_ids(path: Path) -> list[int]:
    frame = pd.read_csv(path)
    column = "ID" if "ID" in frame.columns else frame.columns[0]
    return [int(v) for v in frame[column].unique()]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variants", default="all", help="'all' o lista separada por comas")
    parser.add_argument("--split", default="ll4", choices=tuple(SPLITS))
    parser.add_argument("--ids-file", type=Path, required=True, help="CSV con columna ID")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--future-root", type=Path, default=None,
                        help="future_tmin_by_bucket; obligatorio con --split real")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--cells-per-batch", type=int, default=256)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--limit", type=int, default=0, help="recorta las celdas, para pruebas")
    parser.add_argument("--shard", default=None, metavar="i/n",
                        help="corre solo la porcion i de n; reparte una pasada entre procesos")
    parser.add_argument("--no-tf32", action="store_true",
                        help="desactiva TF32 (mas lento, numerica identica a FP32)")
    parser.add_argument("--tmin-shuffle", choices=TMIN_SHUFFLE_MODES, default=None,
                        help="control negativo: baraja la Tmin del horizonte (no la Td)")
    parser.add_argument("--shuffle-seed", type=int, default=0)
    parser.add_argument("--context-start-year", type=int, default=None,
                        help="sobrescribe el anio de inicio del contexto de la variante; la salida"
                             " lleva __ctx<anio> en el nombre (escalera de contexto, tdew-03g)")
    parser.add_argument("--clim-start-year", type=int, default=None,
                        help="primer anio de la climatologia de las anomalias (hasta train_end); por"
                             " defecto el inicio del contexto. La salida lleva __clim<anio>")
    parser.add_argument("--bead-id", default="tdew-214",
                        help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    args = parser.parse_args(argv)

    if args.split == "real":
        # Este camino registraria una proveniencia incorrecta (split_id, manifest_ref,
        # autoregressive); el producto 2017-2020 se corre con experiments.timesfm.real.
        parser.error("--split real se corre con `python -m experiments.timesfm.real`")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = read_ids(args.ids_file)
    if args.limit:
        ids = ids[: args.limit]

    shard = None
    suffix = ""
    if args.shard:
        index, total = (int(v) for v in args.shard.split("/"))
        if not 0 <= index < total:
            raise SystemExit(f"shard invalido: {args.shard}")
        shard = (index, total)
        suffix = f"_shard{index}de{total}"

    summary = run_variant(
        parse_keys(args.variants),
        split=args.split,
        ids=ids,
        ids_file=args.ids_file,
        out_dir=args.out_dir,
        historical_root=args.historical_root,
        batch_size=args.batch_size,
        cells_per_batch=args.cells_per_batch,
        device=args.device,
        tf32=not args.no_tf32,
        shard=shard,
        bead_id=args.bead_id,
        future_root=args.future_root,
        tmin_shuffle=args.tmin_shuffle,
        shuffle_seed=args.shuffle_seed,
        context_start_year=args.context_start_year,
        clim_start_year=args.clim_start_year,
    )
    ctx = f"_ctx{args.context_start_year}" if args.context_start_year is not None else ""
    ctx += f"_clim{args.clim_start_year}" if args.clim_start_year is not None else ""
    path = args.out_dir / f"runtime_{args.split}{ctx}{suffix}.csv"
    if path.exists():
        summary = pd.concat([pd.read_csv(path), summary], ignore_index=True)
    summary.to_csv(path, index=False)
    print(summary.to_string(index=False))
    print(json.dumps({"runtime_csv": str(path)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
