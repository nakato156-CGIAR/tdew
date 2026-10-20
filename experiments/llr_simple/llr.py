"""LLR simple (tdew-03g): regresion local de la anomalia de Td sobre la de Tmin del mismo dia.

Rival oficial sin diseno por zona: nucleo tricubico circular sobre el dia del anio,
una sola ventana ``h`` para todas las celdas, sin rezagos de Td ni recursion
autorregresiva. Es una reimplementacion independiente, no el pipeline de Palacios
(`HPC_code_tunning`); necesita su revision antes de citarla como equivalente.

Protocolo por split: climatologia y coeficientes con los anios de entrenamiento
(1981..``train_end_year``); ``h`` se elige con los ultimos cuatro anios de
entrenamiento como validacion (coeficientes ajustados con los anteriores) y despues
se reajusta con todo el entrenamiento. La Td del bloque oculto no entra en nada.
"""

from __future__ import annotations

import argparse
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from experiments.timesfm.panel import DEFAULT_HISTORICAL_ROOT, NUM_BUCKETS, SPLITS, TRAIN_START

logger = logging.getLogger("llr_simple")

H_GRID = (7, 11, 15, 21, 31, 45, 60)
LAST_YEAR = 2016
VALIDATION_YEARS = 4


def load_arrays(ids: Sequence[int], root: Path = DEFAULT_HISTORICAL_ROOT):
    """TD y TMIN diarias 1981-2016 como matrices (celdas, dias), float32, NaN si falta."""
    ids = np.asarray(sorted({int(i) for i in ids}), dtype=np.int64)
    dates = pd.date_range(f"{TRAIN_START}-01-01", f"{LAST_YEAR}-12-31")
    cell = {int(i): k for k, i in enumerate(ids)}
    td = np.full((len(ids), len(dates)), np.nan, "f4")
    tm = np.full_like(td, np.nan)
    by_bucket: dict[int, list[int]] = {}
    for i in ids:
        by_bucket.setdefault(int(i) % NUM_BUCKETS, []).append(int(i))

    def read(bucket: int) -> pd.DataFrame:
        frames = []
        for year in range(TRAIN_START, LAST_YEAR + 1):
            path = root / f"id_bucket={bucket:04d}" / f"train_{year}.parquet"
            frame = pd.read_parquet(path, columns=["ID", "FECHA", "TD", "TMIN"])
            frames.append(frame[frame.ID.isin(by_bucket[bucket])])
        return pd.concat(frames)

    with ThreadPoolExecutor(16) as pool:
        for frame in pool.map(read, sorted(by_bucket)):
            rows = frame.ID.map(cell).to_numpy()
            cols = (pd.to_datetime(frame.FECHA) - dates[0]).dt.days.to_numpy()
            td[rows, cols] = frame.TD.to_numpy()
            tm[rows, cols] = frame.TMIN.to_numpy()
    return ids, dates, td, tm


def climatology(x: np.ndarray, doy: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Media por celda y dia del anio con los dias de ``mask``; columnas 1..366."""
    out = np.zeros((x.shape[0], 367))
    for d in range(1, 367):
        out[:, d] = x[:, mask & (doy == d)].mean(axis=1)
    return out


def fit(td, tm, doy, train, h, clim_td, clim_tm):
    """Coeficientes (a, b) por celda y dia del anio, en anomalias, ventana tricubica circular."""
    xa = tm - clim_tm[:, doy]
    ya = td - clim_td[:, doy]
    keys = ("n", "x", "y", "xx", "xy")
    sums = {k: np.zeros((td.shape[0], 366)) for k in keys}
    for d in range(1, 367):
        m = train & (doy == d)
        x, y = xa[:, m], ya[:, m]
        sums["n"][:, d - 1] = m.sum()
        sums["x"][:, d - 1] = x.sum(1)
        sums["y"][:, d - 1] = y.sum(1)
        sums["xx"][:, d - 1] = (x * x).sum(1)
        sums["xy"][:, d - 1] = (x * y).sum(1)
    ks = np.arange(-h, h + 1)
    w = (1 - (np.abs(ks) / (h + 1)) ** 3) ** 3
    acc = {k: sum(wt * np.roll(sums[k], -kk, axis=1) for kk, wt in zip(ks, w)) for k in keys}
    n, x, y, xx, xy = (acc[k] for k in keys)
    b = (n * xy - x * y) / (n * xx - x * x + 1e-9)
    a = (y - b * x) / n
    return a, b


def predict(a, b, td, tm, doy, cols, clim_td, clim_tm):
    d = doy[cols]
    return clim_td[:, d] + a[:, d - 1] + b[:, d - 1] * (tm[:, cols] - clim_tm[:, d]), td[:, cols]


def run_split(split: str, ids: Sequence[int], root: Path = DEFAULT_HISTORICAL_ROOT):
    train_end, (y0, y1) = SPLITS[split]
    ids, dates, td, tm = load_arrays(ids, root)
    doy, year = dates.dayofyear.to_numpy(), dates.year.to_numpy()
    td64, tm64 = td.astype("f8"), tm.astype("f8")

    inner = year <= train_end - VALIDATION_YEARS
    valid = (year > train_end - VALIDATION_YEARS) & (year <= train_end)
    c_td, c_tm = climatology(td64, doy, inner), climatology(tm64, doy, inner)
    scores = {}
    for h in H_GRID:
        a, b = fit(td64, tm64, doy, inner, h, c_td, c_tm)
        p, o = predict(a, b, td64, tm64, doy, np.flatnonzero(valid), c_td, c_tm)
        scores[h] = float(np.sqrt(np.nanmean((p - o) ** 2)))
        logger.info("validacion h=%d rmse=%.4f", h, scores[h])
    h_best = min(scores, key=scores.get)

    train = year <= train_end
    c_td, c_tm = climatology(td64, doy, train), climatology(tm64, doy, train)
    a, b = fit(td64, tm64, doy, train, h_best, c_td, c_tm)
    hold = np.flatnonzero((year >= y0) & (year <= y1))
    pred, obs = predict(a, b, td64, tm64, doy, hold, c_td, c_tm)
    frame = pd.DataFrame(
        {
            "ID": np.repeat(ids, hold.size),
            "FECHA": np.tile(dates[hold].to_numpy(), ids.size),
            "TD_obs": obs.ravel(),
            "pred_llr_simple": pred.ravel(),
            "pred_clim": c_td[:, doy[hold]].ravel(),
        }
    )
    return frame, {"split": split, "h_best": h_best, "validation_rmse": scores}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", required=True, choices=[s for s in SPLITS if s != "real"])
    parser.add_argument("--ids-file", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = pd.read_csv(args.ids_file).ID.unique()
    frame, info = run_split(args.split, ids, args.historical_root)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(args.out_dir / f"{args.split}__llr_simple.parquet", index=False)
    (args.out_dir / f"{args.split}__llr_simple.json").write_text(
        json.dumps({**info, "ids_file": str(args.ids_file), "n_cells": int(len(ids))}, indent=2)
    )
    rmse = float(np.sqrt(np.nanmean((frame.pred_llr_simple - frame.TD_obs) ** 2)))
    clim = float(np.sqrt(np.nanmean((frame.pred_clim - frame.TD_obs) ** 2)))
    logger.info("%s: h=%d rmse llr=%.4f clim=%.4f", args.split, info["h_best"], rmse, clim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
