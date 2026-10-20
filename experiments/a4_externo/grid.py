"""Grilla PISCO 0,01° y lectura de celdas por bucket.

ID = fila * 1422 + columna, con la fila 0 en 1,22°N y la columna 0 en 81,40°W
(centros de celda; se verifica contra ``zone_table.parquet`` en ``check_mapping``).
El bucket de un ID es ``ID % 8192``.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

NCOL, NROW = 1422, 1982
LON0, LAT0, STEP = -81.40, 1.22, 0.01
NUM_BUCKETS = 8192


def lonlat_to_id(lon, lat) -> np.ndarray:
    """ID de la celda cuyo centro es el mas cercano; -1 fuera de la grilla."""
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)
    col = np.rint((lon - LON0) / STEP).astype(int)
    row = np.rint((LAT0 - lat) / STEP).astype(int)
    ok = (col >= 0) & (col < NCOL) & (row >= 0) & (row < NROW)
    return np.where(ok, row * NCOL + col, -1)


def id_to_lonlat(ids) -> tuple[np.ndarray, np.ndarray]:
    ids = np.asarray(ids, dtype=np.int64)
    return LON0 + (ids % NCOL) * STEP, LAT0 - (ids // NCOL) * STEP


def check_mapping(zone_table: Path, sample: int = 200_000) -> float:
    """Maxima discrepancia (grados) entre el mapeo y ``zone_table`` en una muestra."""
    zt = pd.read_parquet(zone_table, columns=["ID", "lon", "lat"])
    zt = zt.sample(min(sample, len(zt)), random_state=0)
    lon, lat = id_to_lonlat(zt["ID"].to_numpy())
    return float(max(np.abs(lon - zt["lon"]).max(), np.abs(lat - zt["lat"]).max()))


def bucket_dir(root: Path, bucket: int) -> Path:
    return Path(root) / f"id_bucket={bucket:04d}"


def read_cells(root: Path, file_names: Iterable[str], ids: Iterable[int], columns: list[str],
               *, workers: int = 16) -> pd.DataFrame:
    """Filas de ``ids`` en ``root/id_bucket=XXXX/<file_name>`` para cada nombre de archivo.

    Solo lectura; archivos inexistentes se omiten.
    """
    ids = np.unique(np.asarray(list(ids), dtype=np.int64))
    by_bucket: dict[int, list[int]] = {}
    for i in ids:
        by_bucket.setdefault(int(i % NUM_BUCKETS), []).append(int(i))
    names = list(file_names)

    def one(item):
        bucket, cell_ids = item
        out = []
        for name in names:
            path = bucket_dir(root, bucket) / name
            if not path.exists():
                continue
            table = pq.read_table(path, columns=columns, filters=[("ID", "in", cell_ids)])
            out.append(table.to_pandas())
        return pd.concat(out, ignore_index=True) if out else None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        parts = [p for p in pool.map(one, by_bucket.items()) if p is not None]
    if not parts:
        return pd.DataFrame(columns=columns)
    frame = pd.concat(parts, ignore_index=True)
    if "id_bucket" in frame:
        frame = frame.drop(columns="id_bucket")
    return frame
