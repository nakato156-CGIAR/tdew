"""LLR con rezagos de Tmin (tdew-03g, A2): mismo esqueleto que `llr.py` con mas predictores.

Regresores por celda y dia del anio: constante, anomalia de Tmin del dia y sus
rezagos (por defecto 1, 2, 7 y 30 dias). Sin rezagos de Td: no hay recursion, porque
la Tmin es exogena y existe en todo el bloque oculto. Es el LLR con una informacion
cercana a la que recibe TimesFM (Tmin de dias anteriores), sin su historial de Td.
Misma ventana tricubica circular y mismo protocolo de ``h`` que `llr.py`, incluido
``--train-start``: recorta los anios de ajuste y de eleccion de ``h``, no la
climatologia, y los rezagos no toman la anomalia de Tmin de dias anteriores a
``train_start``.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from experiments.timesfm.panel import DEFAULT_HISTORICAL_ROOT, SPLITS, TRAIN_START

from . import llr as _llr
from .llr import H_GRID, VALIDATION_YEARS, check_train_start, climatology, drop_before, output_stem

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
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = pd.read_csv(args.ids_file).ID.unique()
    lags = tuple(int(v) for v in args.lags.split(",") if v)
    start = TRAIN_START if args.train_start is None else args.train_start
    frame, info = run_split(args.split, ids, lags, args.historical_root, args.chunk, train_start=start)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stem = output_stem(args.split, "llr_tmin_lags", args.train_start)
    frame.to_parquet(args.out_dir / f"{stem}.parquet", index=False)
    (args.out_dir / f"{stem}.json").write_text(
        json.dumps({**info, "ids_file": str(args.ids_file), "n_cells": int(len(ids))}, indent=2)
    )
    rmse = float(np.sqrt(np.nanmean((frame.pred_llr_tmin_lags - frame.TD_obs) ** 2)))
    logger.info("%s: h=%d rmse llr_tmin_lags=%.4f", args.split, info["h_best"], rmse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
