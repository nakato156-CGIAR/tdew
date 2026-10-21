"""LLR con rezagos de Tmin (tdew-03g, A2): mismo esqueleto que `llr.py` con mas predictores.

Regresores por celda y dia del anio: constante, anomalia de Tmin del dia y sus
rezagos (por defecto 1, 2, 7 y 30 dias). Sin rezagos de Td: no hay recursion, porque
la Tmin es exogena y existe en todo el bloque oculto. Es el LLR con una informacion
cercana a la que recibe TimesFM (Tmin de dias anteriores), sin su historial de Td.
Misma ventana tricubica circular y mismo protocolo de ``h`` que `llr.py`, incluido
``--train-start``: recorta los anios de ajuste y de eleccion de ``h``, no la
climatologia, y los rezagos no toman la anomalia de Tmin de dias anteriores a
``train_start``.

Seleccion conjunta de ``h`` y ``train_start`` (``--select-train-start``, ``--h-grid``): igual
que en `llr.py` (ver su docstring), salida ``<split>__llr_tmin_lags_sel`` con columna
``pred_llr_tmin_lags_sel``. Los bloques de celdas se reparten entre procesos
(``--workers``); la eleccion usa el error agregado de todos los bloques.
"""

from __future__ import annotations

import argparse
import json
import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from experiments.timesfm.panel import DEFAULT_HISTORICAL_ROOT, SPLITS, TRAIN_START

from . import llr as _llr
from .llr import (H_GRID, H_GRID_SEL, TRAIN_START_GRID, VALIDATION_YEARS, add_selection_args, best_cell,
                  check_grids, check_train_start, circulant_window, climatology, drop_before, output_stem,
                  selection_grids, selection_info, window_sum)

logger = logging.getLogger("llr_lags")

DEFAULT_LAGS = (1, 2, 7, 30)
RIDGE = 1e-6


def lag_features(xa: np.ndarray, lags: Sequence[int]) -> np.ndarray:
    """(celdas, dias, 1 + 1 + len(lags)): constante, anomalia de Tmin y sus rezagos; NaN al inicio."""
    n, t = xa.shape
    out = np.full((n, t, 2 + len(lags)), np.nan)
    out[:, :, 0] = 1.0
    out[:, :, 1] = xa
    for j, k in enumerate(lags):
        out[:, k:, 2 + j] = xa[:, :-k]
    return out


def doy_sums(feat: np.ndarray, ya: np.ndarray, doy: np.ndarray, train: np.ndarray):
    """Sumas X'X y X'y por celda y dia del anio con los dias de entrenamiento validos."""
    n, _, k = feat.shape
    xtx = np.zeros((n, 366, k, k))
    xty = np.zeros((n, 366, k))
    cnt = np.zeros((n, 366))
    for d in range(1, 367):
        cols = np.flatnonzero(train & (doy == d))
        f, y = feat[:, cols, :], ya[:, cols]
        ok = np.isfinite(f).all(axis=2) & np.isfinite(y)
        f = np.where(ok[:, :, None], f, 0.0)
        y = np.where(ok, y, 0.0)
        xtx[:, d - 1] = np.einsum("ctk,ctl->ckl", f, f)
        xty[:, d - 1] = np.einsum("ctk,ct->ck", f, y)
        cnt[:, d - 1] = ok.sum(axis=1)
    return xtx, xty, cnt


def solve(sums, h: int) -> np.ndarray:
    """Coeficientes (celdas, 366, k) con la ventana tricubica circular de semiancho ``h``."""
    xtx, xty, _ = sums
    ks = np.arange(-h, h + 1)
    w = (1 - (np.abs(ks) / (h + 1)) ** 3) ** 3
    a = sum(wt * np.roll(xtx, -kk, axis=1) for kk, wt in zip(ks, w))
    b = sum(wt * np.roll(xty, -kk, axis=1) for kk, wt in zip(ks, w))
    a = a + RIDGE * np.eye(a.shape[-1])
    return np.linalg.solve(a, b[..., None])[..., 0]


def solve_window(sums, win: np.ndarray) -> np.ndarray:
    """Como ``solve`` pero con la ventana circulante de ``circulant_window``."""
    xtx, xty, _ = sums
    a = window_sum(xtx, win) + RIDGE * np.eye(xtx.shape[-1])
    return np.linalg.solve(a, window_sum(xty, win)[..., None])[..., 0]


def predict(beta, feat, clim_td, doy, cols) -> np.ndarray:
    d = doy[cols]
    return clim_td[:, d] + np.einsum("ctk,ctk->ct", beta[:, d - 1, :], feat[:, cols, :])


def run_split(split: str, ids: Sequence[int], lags: Sequence[int] = DEFAULT_LAGS,
              root: Path = DEFAULT_HISTORICAL_ROOT, chunk: int = 1000,
              train_start: int = TRAIN_START):
    check_train_start(split, train_start)
    train_end, (y0, y1) = SPLITS[split]
    ids, dates, td, tm = _llr.load_arrays(ids, root)
    doy, year = dates.dayofyear.to_numpy(), dates.year.to_numpy()
    inner_clim = year <= train_end - VALIDATION_YEARS
    inner = (year >= train_start) & inner_clim
    valid = np.flatnonzero((year > train_end - VALIDATION_YEARS) & (year <= train_end))
    train_clim = year <= train_end
    train = (year >= train_start) & train_clim
    hold = np.flatnonzero((year >= y0) & (year <= y1))
    sq = {h: 0.0 for h in H_GRID}
    cnt = 0
    pieces, obs_p, clim_p = [], [], []
    chosen = None
    # Dos pasadas por bloque de celdas: la primera acumula el error de validacion por ``h``;
    # como ``h`` debe ser comun a todas las celdas, se guardan las sumas y se resuelve despues.
    blocks = [slice(s, min(s + chunk, len(ids))) for s in range(0, len(ids), chunk)]
    for pass_no in (1, 2):
        for b in blocks:
            td64, tm64 = td[b].astype("f8"), tm[b].astype("f8")
            if pass_no == 1:
                c_td, c_tm = climatology(td64, doy, inner_clim), climatology(tm64, doy, inner_clim)
                feat = lag_features(drop_before(tm64 - c_tm[:, doy], year, train_start), lags)
                sums = doy_sums(feat, td64 - c_td[:, doy], doy, inner)
                for h in H_GRID:
                    p = predict(solve(sums, h), feat, c_td, doy, valid)
                    e = (p - td64[:, valid]) ** 2
                    sq[h] += float(np.nansum(e))
                cnt += int(np.isfinite(td64[:, valid]).sum())
                logger.info("validacion: bloque %s listo", b)
            else:
                c_td, c_tm = climatology(td64, doy, train_clim), climatology(tm64, doy, train_clim)
                feat = lag_features(drop_before(tm64 - c_tm[:, doy], year, train_start), lags)
                beta = solve(doy_sums(feat, td64 - c_td[:, doy], doy, train), chosen)
                pieces.append(predict(beta, feat, c_td, doy, hold))
                obs_p.append(td64[:, hold])
                clim_p.append(c_td[:, doy[hold]])
                logger.info("ajuste final: bloque %s listo", b)
        if pass_no == 1:
            scores = {h: float(np.sqrt(sq[h] / cnt)) for h in H_GRID}
            chosen = min(scores, key=scores.get)
            logger.info("validacion rmse por h: %s -> h=%d", scores, chosen)
    pred, obs, clim = (np.concatenate(x) for x in (pieces, obs_p, clim_p))
    frame = pd.DataFrame(
        {
            "ID": np.repeat(ids, hold.size),
            "FECHA": np.tile(dates[hold].to_numpy(), ids.size),
            "TD_obs": obs.ravel(),
            "pred_llr_tmin_lags": pred.ravel(),
            "pred_clim": clim.ravel(),
        }
    )
    return frame, {"split": split, "train_start": int(train_start), "train_end": int(train_end),
                   "h_best": chosen, "lags": list(lags), "validation_rmse": scores}


# Estado del proceso padre que heredan los hijos por ``fork`` (sin copiar las matrices).
_SEL: dict = {}


def _sel_validate(b: slice) -> tuple[dict, int]:
    """Suma de errores cuadraticos de validacion por (train_start, h) en un bloque de celdas."""
    g = _SEL
    doy, year, td64, tm64 = g["doy"], g["year"], g["td"][b].astype("f8"), g["tm"][b].astype("f8")
    inner_clim = year <= g["train_end"] - VALIDATION_YEARS
    valid = g["valid"]
    c_td, c_tm = climatology(td64, doy, inner_clim), climatology(tm64, doy, inner_clim)
    xa, ya = tm64 - c_tm[:, doy], td64 - c_td[:, doy]
    sq = {}
    for s in g["starts"]:
        feat = lag_features(drop_before(xa, year, s), g["lags"])
        sums = doy_sums(feat, ya, doy, (year >= s) & inner_clim)
        for h in g["hs"]:
            p = predict(solve_window(sums, g["wins"][h]), feat, c_td, doy, valid)
            sq[(s, h)] = float(np.nansum((p - td64[:, valid]) ** 2))
        del feat, sums
    logger.info("validacion: bloque %s listo", b)
    return sq, int(np.isfinite(td64[:, valid]).sum())


def _sel_final(b: slice) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    g = _SEL
    doy, year, td64, tm64 = g["doy"], g["year"], g["td"][b].astype("f8"), g["tm"][b].astype("f8")
    train_clim = year <= g["train_end"]
    s, h = g["best"]
    c_td, c_tm = climatology(td64, doy, train_clim), climatology(tm64, doy, train_clim)
    feat = lag_features(drop_before(tm64 - c_tm[:, doy], year, s), g["lags"])
    beta = solve_window(doy_sums(feat, td64 - c_td[:, doy], doy, (year >= s) & train_clim), g["wins"][h])
    hold = g["hold"]
    logger.info("ajuste final: bloque %s listo", b)
    return predict(beta, feat, c_td, doy, hold), td64[:, hold], c_td[:, doy[hold]]


def _map(fn, blocks, workers: int):
    if workers <= 1:
        return [fn(b) for b in blocks]
    from threadpoolctl import threadpool_limits

    with threadpool_limits(1), ProcessPoolExecutor(workers, mp_context=mp.get_context("fork")) as pool:
        return list(pool.map(fn, blocks))


def run_split_select(split: str, ids: Sequence[int], lags: Sequence[int] = DEFAULT_LAGS,
                     root: Path = DEFAULT_HISTORICAL_ROOT, chunk: int = 1000,
                     h_grid: Sequence[int] = H_GRID_SEL, starts: Sequence[int] = TRAIN_START_GRID,
                     workers: int = 1):
    """LLR con rezagos de Tmin con ``h`` y ``train_start`` elegidos juntos por validacion interna."""
    hs, ss = check_grids(split, h_grid, starts)
    train_end, (y0, y1) = SPLITS[split]
    ids, dates, td, tm = _llr.load_arrays(ids, root)
    doy, year = dates.dayofyear.to_numpy(), dates.year.to_numpy()
    _SEL.clear()
    _SEL.update(doy=doy, year=year, td=td, tm=tm, train_end=train_end, lags=tuple(lags), hs=hs, starts=ss,
                wins={h: circulant_window(h) for h in hs},
                valid=np.flatnonzero((year > train_end - VALIDATION_YEARS) & (year <= train_end)),
                hold=np.flatnonzero((year >= y0) & (year <= y1)))
    blocks = [slice(s, min(s + chunk, len(ids))) for s in range(0, len(ids), chunk)]
    try:
        parts = _map(_sel_validate, blocks, workers)
        cnt = sum(c for _, c in parts)
        table = [{"train_start": s, "h": h, "rmse": float(np.sqrt(sum(p[(s, h)] for p, _ in parts) / cnt))}
                 for s in ss for h in hs]
        best = best_cell(table)
        logger.info("validacion rmse: %s -> train_start=%d h=%d", table, best["train_start"], best["h"])
        _SEL["best"] = (best["train_start"], best["h"])
        out = _map(_sel_final, blocks, workers)
    finally:
        hold = _SEL["hold"]
        _SEL.clear()
    pred, obs, clim = (np.concatenate([o[i] for o in out]) for i in range(3))
    frame = pd.DataFrame(
        {
            "ID": np.repeat(ids, hold.size),
            "FECHA": np.tile(dates[hold].to_numpy(), ids.size),
            "TD_obs": obs.ravel(),
            "pred_llr_tmin_lags_sel": pred.ravel(),
            "pred_clim": clim.ravel(),
        }
    )
    return frame, {**selection_info(split, table, best, hs, ss), "lags": list(lags)}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", required=True, choices=[s for s in SPLITS if s != "real"])
    parser.add_argument("--ids-file", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--lags", default=",".join(map(str, DEFAULT_LAGS)))
    parser.add_argument("--chunk", type=int, default=1000)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--train-start", type=int, default=None,
                        help=f"primer anio de entrenamiento (por defecto {TRAIN_START}); la salida lleva "
                             "__train<anio> en el nombre")
    add_selection_args(parser)
    parser.add_argument("--workers", type=int, default=1,
                        help="procesos para los bloques de celdas (solo con la seleccion conjunta)")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = pd.read_csv(args.ids_file).ID.unique()
    lags = tuple(int(v) for v in args.lags.split(",") if v)
    sel = selection_grids(args)
    if sel is not None:
        frame, info = run_split_select(args.split, ids, lags, args.historical_root, args.chunk, *sel,
                                       workers=args.workers)
        method = "llr_tmin_lags_sel"
        stem = f"{args.split}__{method}"
    else:
        start = TRAIN_START if args.train_start is None else args.train_start
        frame, info = run_split(args.split, ids, lags, args.historical_root, args.chunk, train_start=start)
        method = "llr_tmin_lags"
        stem = output_stem(args.split, method, args.train_start)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(args.out_dir / f"{stem}.parquet", index=False)
    (args.out_dir / f"{stem}.json").write_text(
        json.dumps({**info, "ids_file": str(args.ids_file), "n_cells": int(len(ids))}, indent=2)
    )
    rmse = float(np.sqrt(np.nanmean((frame[f"pred_{method}"] - frame.TD_obs) ** 2)))
    logger.info("%s: train_start=%d h=%d rmse %s=%.4f", args.split, info["train_start"], info["h_best"],
                method, rmse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
