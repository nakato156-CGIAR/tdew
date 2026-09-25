"""Barrido de coste: celdas/s y VRAM pico en funcion de contexto, horizonte y lote.

El coste de TimesFM crece con el cuadrado de ``(contexto + horizonte)/32``, que es
el numero de tokens que entra a la atencion, y el paquete no trae ni estimacion
previa de memoria ni retroceso automatico ante OOM
(`timesfm3/torch/timesfm3_forecaster.py:119-134`). Medirlo es parte del resultado:
decide el tamano de las fases siguientes y sostiene la afirmacion sobre lo que
costaria una pasada nacional.
"""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from .panel import DEFAULT_HISTORICAL_ROOT, PanelBatch, iter_panel_batches, split_spec

logger = logging.getLogger("timesfm.throughput")

CONTEXTS = (731, 4018, 11688)
HORIZONS = (366, 731, 1461)
BATCHES = (1, 2, 4, 8, 16)


def _trim(panel: PanelBatch, context: int, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    """Contexto recortado por la izquierda y covariable de ancho contexto+horizonte."""
    td = panel.td_ctx[:, -context:]
    tmin = np.concatenate([panel.tmin_ctx[:, -context:], panel.tmin_hold[:, :horizon]], axis=1)
    return td, tmin


def sweep(
    panel: PanelBatch,
    *,
    contexts: Sequence[int] = CONTEXTS,
    horizons: Sequence[int] = HORIZONS,
    batches: Sequence[int] = BATCHES,
    with_covariates: bool = True,
    device: str = "cuda",
) -> pd.DataFrame:
    import torch
    from timesfm3 import TimesFM3Forecaster

    model = TimesFM3Forecaster.from_pretrained("google/timesfm-3.0-pytorch", device=device)
    rows: list[dict[str, object]] = []
    for context in contexts:
        for horizon in horizons:
            td, tmin = _trim(panel, context, horizon)
            contexts_list = [np.ascontiguousarray(r, dtype=np.float32) for r in td]
            cov_list = (
                [np.ascontiguousarray(r[None, :], dtype=np.float32) for r in tmin]
                if with_covariates
                else None
            )
            tokens = (context + int(np.ceil(horizon / 64) * 64)) / 32
            for batch in batches:
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats()
                model.config.per_core_batch_size = batch
                started = time.time()
                try:
                    list(
                        model.predict_batch(
                            contexts=contexts_list,
                            horizon=horizon,
                            past_future_covariates=cov_list,
                            return_quantiles=True,
                            make_positive=False,
                        )
                    )
                    elapsed = time.time() - started
                    peak = torch.cuda.max_memory_allocated() / 2**30
                    status = "ok"
                except torch.cuda.OutOfMemoryError:
                    torch.cuda.empty_cache()
                    elapsed, peak, status = float("nan"), float("nan"), "oom"
                rows.append(
                    {
                        "context": context,
                        "horizon": horizon,
                        "batch": batch,
                        "covariates": int(bool(with_covariates)),
                        "cells": panel.n_cells,
                        "tokens": tokens,
                        "seconds": elapsed,
                        "cells_per_second": panel.n_cells / elapsed if elapsed == elapsed else float("nan"),
                        "peak_vram_gb": peak,
                        "status": status,
                    }
                )
                logger.info(
                    "ctx=%d hor=%d batch=%d -> %s %.2f celdas/s, %.2f GB",
                    context,
                    horizon,
                    batch,
                    status,
                    rows[-1]["cells_per_second"] if status == "ok" else float("nan"),
                    peak,
                )
                if status == "oom":
                    break  # lotes mayores tampoco entran
    del model
    torch.cuda.empty_cache()
    return pd.DataFrame(rows)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids-file", type=Path, required=True)
    parser.add_argument("--cells", type=int, default=32)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--no-covariates", action="store_true")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = pd.read_csv(args.ids_file)["ID"].tolist()[: args.cells]
    spec = split_spec("ll4", context_start_year=1981)
    panel = next(
        iter_panel_batches(
            ids, spec, historical_root=args.historical_root, max_cells_per_batch=args.cells
        )
    )
    logger.info("panel de %d celdas, contexto %d d", panel.n_cells, panel.td_ctx.shape[1])

    frame = sweep(panel, with_covariates=not args.no_covariates, device=args.device)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(frame.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
