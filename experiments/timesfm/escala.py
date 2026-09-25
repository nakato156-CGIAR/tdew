"""Puntuacion de la prueba de escala: 436.519 celdas, por sitio y reponderada.

A este volumen la tabla no cabe en memoria: 436.519 celdas por 1.461 dias son
637,8 millones de filas por metodo. Se puntua en flujo con
``tdew_estimation.metrics.MetricsAccum``, que acumula nueve sumas por grupo y
reconstruye n, RMSE, MAE, sesgo y r al cerrar, de modo que el resultado no depende
de donde caigan los cortes entre bloques.

El agregado ``ALL`` va reponderado por el numero real de celdas de cada
departamento, siguiendo el patron de
``experiments/tcn/audit_x46/04_compare_predictors.py:27,72-79``, para que sea
comparable con las filas ``site="ALL"`` de
``reports/week1_baselines/leaderboard.csv``, que estan dominadas por Loreto.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterator, Sequence

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from tdew_estimation import provenance as prov
from tdew_estimation.metrics import MetricsAccum

from .evaluate import build_row_provenance

logger = logging.getLogger("timesfm.escala")

SITES = ("lima", "cusco", "iquitos_loreto", "tarapoto_san_martin")
DEFAULT_SILVER = Path("Data/silver/department_grid_ids")
RIVALS = {"climatology": "pred_clim", "tuned": "pred_tuned"}


def site_of(ids: np.ndarray, membership: dict[str, set[int]]) -> np.ndarray:
    """Etiqueta cada celda con su departamento."""
    out = np.empty(ids.shape, dtype=object)
    out[:] = "otro"
    for site, members in membership.items():
        out[np.isin(ids, list(members))] = site
    return out


def load_membership(silver: Path = DEFAULT_SILVER) -> tuple[dict[str, set[int]], dict[str, int]]:
    membership, counts = {}, {}
    for site in SITES:
        ids = pd.read_csv(silver / f"{site}.csv")["ID"].astype(int)
        membership[site] = set(ids)
        counts[site] = int(ids.nunique())
    return membership, counts


def _iter_chunks(path: Path, columns: Sequence[str], batch_rows: int) -> Iterator[pd.DataFrame]:
    parquet = pq.ParquetFile(path)
    for batch in parquet.iter_batches(batch_size=batch_rows, columns=list(columns)):
        yield batch.to_pandas()


def _index_timesfm(path: Path, keep: set[int] | None, batch_rows: int) -> pd.Series:
    """Indexa la salida de TimesFM por ``(ID, FECHA)``, quedandose solo con ``keep``.

    La pasada de escala son 637,8 millones de filas y el rival solo cubre una
    submuestra de celdas. Como la union posterior es interna, descartar en la
    lectura las celdas que el rival no tiene da exactamente el mismo resultado y
    evita construir un indice de 637 millones de entradas, que es la forma que
    tuvieron los agotamientos de memoria de esta campana.
    """
    keep_array = np.fromiter(sorted(keep), dtype=np.int64) if keep is not None else None
    pieces = []
    for chunk in _iter_chunks(path, ["ID", "FECHA", "pred"], batch_rows):
        if keep_array is not None:
            chunk = chunk[np.isin(chunk["ID"].to_numpy(), keep_array)]
            if chunk.empty:
                continue
        pieces.append(chunk)
    frame = (
        pd.concat(pieces, ignore_index=True)
        if pieces
        else pd.DataFrame(columns=["ID", "FECHA", "pred"])
    )
    frame["FECHA"] = pd.to_datetime(frame["FECHA"])
    return frame.set_index(["ID", "FECHA"])["pred"]


def score(
    timesfm_parquet: Path,
    backtest_predictions: Path,
    *,
    silver: Path = DEFAULT_SILVER,
    batch_rows: int = 2_000_000,
    ids: set[int] | None = None,
) -> pd.DataFrame:
    """Puntua TimesFM y los rivales sobre las celdas que ambos cubren.

    La union es por ``(ID, FECHA)`` bloque a bloque: se indexa primero la salida de
    TimesFM por celda para poder cruzarla sin materializar las dos tablas.
    """
    membership, counts = load_membership(silver)

    logger.info("indexando la salida de TimesFM")
    timesfm = _index_timesfm(timesfm_parquet, ids, batch_rows)
    logger.info("%d filas de TimesFM, %d celdas", len(timesfm), timesfm.index.get_level_values(0).nunique())

    methods = {**RIVALS, "timesfm": None}
    accums: dict[tuple[str, str], MetricsAccum] = {}
    seen_cells: dict[str, set[int]] = {site: set() for site in (*SITES, "otro")}

    columns = ["ID", "FECHA", "TD_obs", *RIVALS.values()]
    for chunk in _iter_chunks(backtest_predictions, columns, batch_rows):
        chunk["FECHA"] = pd.to_datetime(chunk["FECHA"])
        joined = chunk.join(timesfm, on=["ID", "FECHA"], how="inner")
        if joined.empty:
            continue
        joined = joined.rename(columns={"pred": "pred_timesfm"})
        sites = site_of(joined["ID"].to_numpy(), membership)
        observed = joined["TD_obs"].to_numpy(dtype=float)
        for site in np.unique(sites):
            mask = sites == site
            seen_cells[site].update(joined.loc[mask, "ID"].unique().tolist())
            for method in methods:
                column = RIVALS.get(method, "pred_timesfm")
                key = (str(site), method)
                accums.setdefault(key, MetricsAccum())
                accums[key].add(joined.loc[mask, column].to_numpy(dtype=float), observed[mask])

    rows = []
    for (site, method), accum in accums.items():
        rows.append({"site": site, "method": method, "cells": len(seen_cells[site]), **accum.finalize()})
    frame = pd.DataFrame(rows)
    total = sum(counts.values())
    for method in methods:
        part = frame[(frame["method"] == method) & (frame["site"].isin(SITES))]
        if len(part) != len(SITES):
            logger.warning("%s no cubre los cuatro departamentos; se omite el agregado", method)
            continue
        per_site = dict(zip(part["site"], part["rmse"]))
        mse = sum(counts[s] / total * per_site[s] ** 2 for s in SITES)
        mae = sum(counts[s] / total * v for s, v in zip(part["site"], part["mae"]))
        bias = sum(counts[s] / total * v for s, v in zip(part["site"], part["bias"]))
        rows.append(
            {
                "site": "ALL_reponderado",
                "method": method,
                "cells": total,
                "n": int(part["n"].sum()),
                "rmse": float(np.sqrt(mse)),
                "mae": float(mae),
                "bias": float(bias),
                "r": np.nan,
                "skill_vs_clim": np.nan,
            }
        )
    frame = pd.DataFrame(rows)
    # El skill se calcula al final, sobre la tabla ya completa: si se calcula antes
    # de anadir las filas agregadas, reconstruir el marco lo descarta.
    # Siempre dentro del mismo sitio, nunca entre sitios.
    clim = frame[frame["method"] == "climatology"].set_index("site")["rmse"]
    frame["skill_vs_clim"] = [
        1.0 - value / clim[site] if site in clim.index and clim[site] else np.nan
        for site, value in zip(frame["site"], frame["rmse"])
    ]
    return frame.sort_values(["site", "rmse"]).reset_index(drop=True)


def _provenance_method_name(row_method: str, variant_key: str) -> str:
    """``score()`` reporta el nombre bare 'timesfm' (via ``methods = {**RIVALS,
    'timesfm': None}``); la proveniencia necesita la variante real, la misma
    forma 'timesfm:<key>' que usa experiments.timesfm.evaluate."""
    return f"timesfm:{variant_key}" if row_method == "timesfm" else row_method


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timesfm", type=Path, required=True)
    parser.add_argument("--backtest-predictions", type=Path, required=True)
    parser.add_argument("--silver", type=Path, default=DEFAULT_SILVER)
    parser.add_argument("--batch-rows", type=int, default=2_000_000)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--ids-csv",
        type=Path,
        default=None,
        help="celdas a conservar de la salida de TimesFM; la union es interna, "
        "asi que filtrar por las celdas del rival no cambia el resultado",
    )
    parser.add_argument("--split", default="ll4",
                        help="split anotado en tdew_estimation.provenance (esta pasada es de un solo split)")
    parser.add_argument("--timesfm-variant", default="tmin_anom_full",
                        help="variante de TimesFM detras de la columna pred_timesfm, para la proveniencia")
    parser.add_argument("--bead-id", default="tdew-214",
                        help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ids = None
    if args.ids_csv is not None:
        ids = set(pd.read_csv(args.ids_csv)["ID"].astype(int).tolist())
        logger.info("se conservan %d celdas de la salida de TimesFM", len(ids))
    frame = score(
        args.timesfm,
        args.backtest_predictions,
        silver=args.silver,
        batch_rows=args.batch_rows,
        ids=ids,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(frame.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    for _, row in frame.iterrows():
        method = _provenance_method_name(row["method"], args.timesfm_variant)
        prov.record_metric_provenance(
            build_row_provenance(
                method, split=args.split, cells=int(row["cells"]), bead_id=args.bead_id,
                panel_id=str(row["site"]), panel_file=None, output_files=(str(args.out),),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
