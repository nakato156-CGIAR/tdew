"""LLR simple (tdew-03g): regresion local de la anomalia de Td sobre la de Tmin del mismo dia.

Rival oficial sin diseno por zona: nucleo tricubico circular sobre el dia del anio,
una sola ventana ``h`` para todas las celdas, sin rezagos de Td ni recursion
autorregresiva. Es una reimplementacion independiente, no el pipeline de Palacios
(`HPC_code_tunning`); necesita su revision antes de citarla como equivalente.

Protocolo por split: climatologia y coeficientes con los anios de entrenamiento
(1981..``train_end_year``); ``h`` se elige con los ultimos cuatro anios de
entrenamiento como validacion (coeficientes ajustados con los anteriores) y despues
se reajusta con todo el entrenamiento. La Td del bloque oculto no entra en nada.

``train_start`` (``--train-start``, escalera de contexto de tdew-03g) recorta por la
izquierda solo los anios con que se ajustan los coeficientes y se elige ``h``, igual que
``--context-start-year`` recorta el contexto de TimesFM. La climatologia (de Td y de
Tmin) sigue con 1981..``train_end`` (y 1981..``train_end``-4 en la validacion), simetrico
con la escalera de TimesFM, que fija la climatologia con ``--clim-start-year 1981``. En
``llr_lags`` los rezagos tampoco toman la anomalia de Tmin de dias anteriores a
``train_start``.

Seleccion conjunta (``--select-train-start`` y/o ``--h-grid``, opcional): ``h`` en
``H_GRID_SEL`` (o la grilla dada) y el anio de inicio del ajuste en ``TRAIN_START_GRID``
se eligen juntos con la misma validacion interna (coeficientes con
[train_start, train_end-4], climatologia 1981..train_end-4, error en los cuatro ultimos
anios de entrenamiento) y despues se reajusta con [train_start elegido, train_end] y la
climatologia 1981..train_end. El bloque oculto no entra en la eleccion. La salida va a
``<split>__llr_simple_sel`` (columna ``pred_llr_simple_sel``) con la tabla de validacion
en el JSON; sin esas opciones el comportamiento es el de siempre. En este camino la suma
ponderada por dia del anio se hace con una matriz circulante (``circulant_window``), que
da lo mismo que ``np.roll`` salvo redondeo y es mucho mas rapida para ``h`` grandes.
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
H_GRID_SEL = (7, 11, 15, 21, 31, 45, 60, 90, 120, 180)
TRAIN_START_GRID = (1981, 1986, 1991, 1996)
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


def doy_moments(td, tm, doy, train, clim_td, clim_tm):
    """Sumas n, x, y, xx, xy de las anomalias por celda y dia del anio (columnas 0..365)."""
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
    return sums


def _ab(n, x, y, xx, xy):
    b = (n * xy - x * y) / (n * xx - x * x + 1e-9)
    a = (y - b * x) / n
    return a, b


def fit(td, tm, doy, train, h, clim_td, clim_tm):
    """Coeficientes (a, b) por celda y dia del anio, en anomalias, ventana tricubica circular."""
    sums = doy_moments(td, tm, doy, train, clim_td, clim_tm)
    keys = ("n", "x", "y", "xx", "xy")
    ks = np.arange(-h, h + 1)
    w = (1 - (np.abs(ks) / (h + 1)) ** 3) ** 3
    acc = {k: sum(wt * np.roll(sums[k], -kk, axis=1) for kk, wt in zip(ks, w)) for k in keys}
    return _ab(*(acc[k] for k in keys))


def circulant_window(h: int) -> np.ndarray:
    """Matriz (366, 366) con W[d, d+k mod 366] = peso tricubico de k, |k| <= h.

    ``W @ x`` a lo largo del dia del anio es la misma suma que ``sum_k w_k roll(x, -k)``.
    Exige 2h+1 <= 366 para que la ventana no se solape consigo misma.
    """
    h = int(h)
    if not 1 <= h <= 182:
        raise ValueError(f"h={h} fuera de [1, 182]")
    ks = np.arange(-h, h + 1)
    w = (1 - (np.abs(ks) / (h + 1)) ** 3) ** 3
    out = np.zeros((366, 366))
    d = np.arange(366)
    for k, wt in zip(ks, w):
        out[d, (d + k) % 366] = wt
    return out


def window_sum(x: np.ndarray, win: np.ndarray) -> np.ndarray:
    """Suma ponderada circular sobre el eje 1 (dia del anio) de ``x`` (celdas, 366, ...)."""
    shape = x.shape
    return np.matmul(win, x.reshape(shape[0], 366, -1)).reshape(shape)


def fit_window(sums: dict, win: np.ndarray):
    """(a, b) desde ``doy_moments`` con la ventana circulante ``win``."""
    return _ab(*(window_sum(sums[k], win) for k in ("n", "x", "y", "xx", "xy")))


def predict(a, b, td, tm, doy, cols, clim_td, clim_tm):
    d = doy[cols]
    return clim_td[:, d] + a[:, d - 1] + b[:, d - 1] * (tm[:, cols] - clim_tm[:, d]), td[:, cols]


def check_train_start(split: str, train_start: int) -> None:
    """La validacion de ``h`` necesita al menos un anio interno antes de los cuatro de validacion."""
    train_end = SPLITS[split][0]
    if not TRAIN_START <= train_start <= train_end - VALIDATION_YEARS:
        raise ValueError(
            f"train_start={train_start} fuera de [{TRAIN_START}, {train_end - VALIDATION_YEARS}] "
            f"para el split {split}"
        )


def drop_before(x: np.ndarray, year: np.ndarray, train_start: int) -> np.ndarray:
    """Copia de ``x`` (una anomalia ya formada) con NaN en los dias anteriores a ``train_start``."""
    if train_start <= TRAIN_START:
        return x
    out = x.copy()
    out[:, year < train_start] = np.nan
    return out


def check_grids(split: str, h_grid: Sequence[int], starts: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Valida y ordena las grillas de la seleccion conjunta."""
    hs = tuple(sorted({int(h) for h in h_grid}))
    ss = tuple(sorted({int(s) for s in starts}))
    if not hs or not ss:
        raise ValueError("grillas vacias")
    for h in hs:
        circulant_window(h)
    for s in ss:
        check_train_start(split, s)
    return hs, ss


def best_cell(table: list[dict]) -> dict:
    """Fila de menor RMSE de validacion; en empate, la primera (inicio y h menores)."""
    return min(table, key=lambda r: r["rmse"])


def selection_info(split: str, table: list[dict], best: dict, hs, ss) -> dict:
    train_end = SPLITS[split][0]
    return {
        "split": split, "train_start": int(best["train_start"]), "train_end": int(train_end),
        "h_best": int(best["h"]),
        "selection": {
            "criterio": "RMSE de validacion agregado sobre todas las celdas, h y train_start comunes",
            "h_grid": list(hs), "train_start_grid": list(ss),
            "validation_years": [train_end - VALIDATION_YEARS + 1, train_end],
            "validation_fit_years": "train_start..%d" % (train_end - VALIDATION_YEARS),
            "validation_climatology_years": [TRAIN_START, train_end - VALIDATION_YEARS],
            "final_fit_years": [int(best["train_start"]), int(train_end)],
            "final_climatology_years": [TRAIN_START, int(train_end)],
            "validation_rmse": table,
        },
    }


def run_split_select(split: str, ids: Sequence[int], root: Path = DEFAULT_HISTORICAL_ROOT,
                     h_grid: Sequence[int] = H_GRID_SEL, starts: Sequence[int] = TRAIN_START_GRID):
    """LLR simple con ``h`` y ``train_start`` elegidos juntos por validacion interna."""
    hs, ss = check_grids(split, h_grid, starts)
    train_end, (y0, y1) = SPLITS[split]
    ids, dates, td, tm = load_arrays(ids, root)
    doy, year = dates.dayofyear.to_numpy(), dates.year.to_numpy()
    td64, tm64 = td.astype("f8"), tm.astype("f8")
    del td, tm
    inner_clim = year <= train_end - VALIDATION_YEARS
    valid = np.flatnonzero((year > train_end - VALIDATION_YEARS) & (year <= train_end))
    c_td, c_tm = climatology(td64, doy, inner_clim), climatology(tm64, doy, inner_clim)
    wins = {h: circulant_window(h) for h in hs}
    table = []
    for s in ss:
        sums = doy_moments(td64, tm64, doy, (year >= s) & inner_clim, c_td, c_tm)
        for h in hs:
            p, o = predict(*fit_window(sums, wins[h]), td64, tm64, doy, valid, c_td, c_tm)
            table.append({"train_start": s, "h": h, "rmse": float(np.sqrt(np.nanmean((p - o) ** 2)))})
            logger.info("validacion train_start=%d h=%d rmse=%.4f", s, h, table[-1]["rmse"])
    best = best_cell(table)
    train_clim = year <= train_end
    c_td, c_tm = climatology(td64, doy, train_clim), climatology(tm64, doy, train_clim)
    sums = doy_moments(td64, tm64, doy, (year >= best["train_start"]) & train_clim, c_td, c_tm)
    a, b = fit_window(sums, wins[best["h"]])
    hold = np.flatnonzero((year >= y0) & (year <= y1))
    pred, obs = predict(a, b, td64, tm64, doy, hold, c_td, c_tm)
    frame = pd.DataFrame(
        {
            "ID": np.repeat(ids, hold.size),
            "FECHA": np.tile(dates[hold].to_numpy(), ids.size),
            "TD_obs": obs.ravel(),
            "pred_llr_simple_sel": pred.ravel(),
            "pred_clim": c_td[:, doy[hold]].ravel(),
        }
    )
    return frame, selection_info(split, table, best, hs, ss)


def parse_grid(text: str | None) -> tuple[int, ...] | None:
    return None if text is None else tuple(int(v) for v in text.split(",") if v.strip())


def output_stem(split: str, method: str, train_start: int | None) -> str:
    """``<split>__<metodo>`` y, si se recorta el entrenamiento, ``__train<anio>``."""
    return f"{split}__{method}" + (f"__train{train_start}" if train_start is not None else "")


def run_split(split: str, ids: Sequence[int], root: Path = DEFAULT_HISTORICAL_ROOT,
              train_start: int = TRAIN_START):
    check_train_start(split, train_start)
    train_end, (y0, y1) = SPLITS[split]
    ids, dates, td, tm = load_arrays(ids, root)
    doy, year = dates.dayofyear.to_numpy(), dates.year.to_numpy()
    td64, tm64 = td.astype("f8"), tm.astype("f8")

    # Climatologia con todos los anios desde 1981; coeficientes desde ``train_start``.
    inner_clim = year <= train_end - VALIDATION_YEARS
    inner = (year >= train_start) & inner_clim
    valid = (year > train_end - VALIDATION_YEARS) & (year <= train_end)
    c_td, c_tm = climatology(td64, doy, inner_clim), climatology(tm64, doy, inner_clim)
    scores = {}
    for h in H_GRID:
        a, b = fit(td64, tm64, doy, inner, h, c_td, c_tm)
        p, o = predict(a, b, td64, tm64, doy, np.flatnonzero(valid), c_td, c_tm)
        scores[h] = float(np.sqrt(np.nanmean((p - o) ** 2)))
        logger.info("validacion h=%d rmse=%.4f", h, scores[h])
    h_best = min(scores, key=scores.get)

    train_clim = year <= train_end
    train = (year >= train_start) & train_clim
    c_td, c_tm = climatology(td64, doy, train_clim), climatology(tm64, doy, train_clim)
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
    return frame, {"split": split, "train_start": int(train_start), "train_end": int(train_end),
                   "h_best": h_best, "validation_rmse": scores}


def add_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--select-train-start", nargs="?", const=",".join(map(str, TRAIN_START_GRID)),
                        default=None, metavar="ANIOS",
                        help="elige train_start (grilla, por defecto %s) junto con h por validacion "
                             "interna; salida <split>__<metodo>_sel" % ",".join(map(str, TRAIN_START_GRID)))
    parser.add_argument("--h-grid", default=None,
                        help="grilla de h para la seleccion conjunta (por defecto %s); activa la "
                             "salida _sel" % ",".join(map(str, H_GRID_SEL)))


def selection_grids(args) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """(h_grid, starts) si se pidio la seleccion conjunta; None para el camino de siempre."""
    if args.select_train_start is None and args.h_grid is None:
        return None
    if args.select_train_start is not None and args.train_start is not None:
        raise SystemExit("--train-start y --select-train-start son incompatibles")
    starts = parse_grid(args.select_train_start) or (
        (TRAIN_START if args.train_start is None else args.train_start),)
    return parse_grid(args.h_grid) or H_GRID_SEL, starts


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", required=True, choices=[s for s in SPLITS if s != "real"])
    parser.add_argument("--ids-file", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--train-start", type=int, default=None,
                        help=f"primer anio de entrenamiento (por defecto {TRAIN_START}); la salida lleva "
                             "__train<anio> en el nombre")
    add_selection_args(parser)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = pd.read_csv(args.ids_file).ID.unique()
    sel = selection_grids(args)
    if sel is not None:
        frame, info = run_split_select(args.split, ids, args.historical_root, *sel)
        method = "llr_simple_sel"
        stem = f"{args.split}__{method}"
    else:
        start = TRAIN_START if args.train_start is None else args.train_start
        frame, info = run_split(args.split, ids, args.historical_root, train_start=start)
        method = "llr_simple"
        stem = output_stem(args.split, method, args.train_start)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(args.out_dir / f"{stem}.parquet", index=False)
    (args.out_dir / f"{stem}.json").write_text(
        json.dumps({**info, "ids_file": str(args.ids_file), "n_cells": int(len(ids))}, indent=2)
    )
    rmse = float(np.sqrt(np.nanmean((frame[f"pred_{method}"] - frame.TD_obs) ** 2)))
    clim = float(np.sqrt(np.nanmean((frame.pred_clim - frame.TD_obs) ** 2)))
    logger.info("%s: h=%d rmse llr=%.4f clim=%.4f", args.split, info["h_best"], rmse, clim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
