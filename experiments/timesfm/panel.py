"""Construccion de paneles de contexto/horizonte para TimesFM, leak-safe.

El panel se arma desde el mismo origen que usa el backtest de Palacios
(``$RES/bucketed_training_data/id_bucket=XXXX/train_YYYY.parquet``, columnas
``ID, FECHA, TD, TMIN, doy``, 1981-2016), de modo que TimesFM ve exactamente la
informacion que ve ``HPC_code_tunning/backtest.py`` y ni un dato mas.

Regla de no-fuga: el contexto termina el 31 de diciembre de ``train_end_year`` y
la climatologia se calcula solo con esos anios, igual que
``backtest.train_only_climatology``. Nada del bloque oculto entra en el contexto
ni en la climatologia; lo unico del bloque oculto que se entrega al modelo es
TMIN, que es exogeno y existe en todo el rango (es la misma variable que el
metodo de Palacios usa como covariable).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import numpy as np
import pandas as pd

from tdew_estimation.bucket_layout import bucket_dir

from . import paths

# Mismos splits que HPC_code_tunning/backtest.py:61-66 — (train_end_year, (y0, y1)).
SPLITS: dict[str, tuple[int, tuple[int, int]]] = {
    "ll1": (2015, (2016, 2016)),
    "ll2": (2014, (2015, 2016)),
    "ll4": (2012, (2013, 2016)),
    # Hueco real de Palacios: no hay Td observada en el horizonte. La Tmin futura
    # sale de `future_tmin_by_bucket`, no de `bucketed_training_data`.
    "real": (2016, (2017, 2020)),
}
FUTURE_SPLITS = frozenset({"real"})
TRAIN_START = 1981
NUM_BUCKETS = 8192
REQUIRED_COLUMNS = ("ID", "FECHA", "TD", "TMIN", "doy")

DEFAULT_HISTORICAL_ROOT = paths.RES / "bucketed_training_data"


@dataclass(frozen=True)
class SplitSpec:
    """Ventana temporal de un split, en anios completos."""

    name: str
    train_end_year: int
    holdout_years: tuple[int, int]
    context_start_year: int = TRAIN_START

    @property
    def context_end(self) -> pd.Timestamp:
        return pd.Timestamp(f"{self.train_end_year}-12-31")

    @property
    def context_start(self) -> pd.Timestamp:
        return pd.Timestamp(f"{self.context_start_year}-01-01")

    @property
    def holdout_start(self) -> pd.Timestamp:
        return pd.Timestamp(f"{self.holdout_years[0]}-01-01")

    @property
    def holdout_end(self) -> pd.Timestamp:
        return pd.Timestamp(f"{self.holdout_years[1]}-12-31")

    @property
    def horizon(self) -> int:
        return int((self.holdout_end - self.holdout_start).days) + 1

    @property
    def context_length(self) -> int:
        return int((self.context_end - self.context_start).days) + 1


def split_spec(name: str, *, context_start_year: int = TRAIN_START) -> SplitSpec:
    """Devuelve la ventana de un split, opcionalmente con contexto recortado.

    ``context_start_year`` permite las variantes de contexto corto sin tocar el
    bloque oculto: recorta por la izquierda, nunca por la derecha.
    """
    if name not in SPLITS:
        raise KeyError(f"split desconocido: {name!r}; hay {sorted(SPLITS)}")
    train_end, holdout = SPLITS[name]
    if context_start_year > train_end:
        raise ValueError(
            f"context_start_year={context_start_year} deja el contexto vacio "
            f"para el split {name} (train_end={train_end})"
        )
    return SplitSpec(name, train_end, holdout, context_start_year)


@dataclass
class PanelBatch:
    """Un lote de celdas ya alineado en el calendario diario del split.

    Todas las matrices comparten el mismo eje temporal: las columnas de contexto
    van de ``context_start`` a ``context_end`` y las de horizonte de
    ``holdout_start`` a ``holdout_end``, sin huecos.
    """

    spec: SplitSpec
    ids: np.ndarray  # (N,) int64
    td_ctx: np.ndarray  # (N, C) float32
    tmin_ctx: np.ndarray  # (N, C) float32
    td_hold: np.ndarray  # (N, H) float32 — la verdad, jamas se entrega al modelo
    tmin_hold: np.ndarray  # (N, H) float32 — exogeno, si se entrega
    td_clim: np.ndarray  # (N, 367) float32, indexado por doy (1..366)
    tmin_clim: np.ndarray  # (N, 367) float32
    ctx_doy: np.ndarray  # (C,) int16
    hold_doy: np.ndarray  # (H,) int16
    ctx_dates: pd.DatetimeIndex
    hold_dates: pd.DatetimeIndex

    @property
    def n_cells(self) -> int:
        return int(self.ids.size)

    def clim_for(self, which: str, *, block: str) -> np.ndarray:
        """Climatologia expandida al eje diario del bloque pedido."""
        table = self.td_clim if which == "TD" else self.tmin_clim
        doy = self.ctx_doy if block == "context" else self.hold_doy
        return table[:, doy]

    def anomaly(self, which: str, *, block: str) -> np.ndarray:
        values = {
            ("TD", "context"): self.td_ctx,
            ("TD", "holdout"): self.td_hold,
            ("TMIN", "context"): self.tmin_ctx,
            ("TMIN", "holdout"): self.tmin_hold,
        }[(which, block)]
        return values - self.clim_for(which, block=block)


def _buckets_for(ids: Sequence[int]) -> dict[int, np.ndarray]:
    """Agrupa los IDs por bucket ``ID % 8192``."""
    arr = np.asarray(sorted(set(int(i) for i in ids)), dtype=np.int64)
    if arr.size == 0:
        raise ValueError("la lista de IDs esta vacia")
    buckets = arr % NUM_BUCKETS
    order = np.argsort(buckets, kind="stable")
    arr, buckets = arr[order], buckets[order]
    edges = np.flatnonzero(np.diff(buckets)) + 1
    return {
        int(chunk[0] % NUM_BUCKETS): chunk
        for chunk in np.split(arr, edges)
        if chunk.size
    }


def _read_bucket(root: Path, bucket: int, years: range) -> pd.DataFrame:
    """Lee un bucket restringido a los anios pedidos."""
    directory = bucket_dir(root, bucket)
    frames = []
    for year in years:
        path = directory / f"train_{year}.parquet"
        if path.exists():
            frames.append(pd.read_parquet(path, columns=list(REQUIRED_COLUMNS)))
    if not frames:
        raise FileNotFoundError(f"sin parquets para el bucket {bucket} en {directory}")
    return pd.concat(frames, ignore_index=True)


def _read_future_bucket(root: Path, bucket: int, years: range) -> pd.DataFrame:
    """Lee la Tmin futura regridada de un bucket (``future_tmin_{year}.parquet``)."""
    directory = bucket_dir(root, bucket)
    frames = []
    for year in years:
        path = directory / f"future_tmin_{year}.parquet"
        if path.exists():
            frames.append(pd.read_parquet(path, columns=["ID", "FECHA", "TMIN"]))
    if not frames:
        raise FileNotFoundError(f"sin future_tmin para el bucket {bucket} en {directory}")
    return pd.concat(frames, ignore_index=True)


def _pivot(frame: pd.DataFrame, column: str, ids: np.ndarray, dates: pd.DatetimeIndex) -> np.ndarray:
    wide = (
        frame.pivot(index="ID", columns="FECHA", values=column)
        .reindex(index=ids, columns=dates)
        .to_numpy(dtype=np.float32)
    )
    return wide


def build_panel(
    ids: Sequence[int],
    spec: SplitSpec,
    *,
    historical_root: Path | str = DEFAULT_HISTORICAL_ROOT,
    bucket: int | None = None,
    future_root: Path | str | None = None,
) -> PanelBatch | None:
    """Arma el panel de un conjunto de IDs que comparten bucket.

    Devuelve ``None`` si ninguna celda sobrevive el filtro de completitud.

    En los splits de ``FUTURE_SPLITS`` (``real``) el hold-out no existe en
    ``historical_root``: ``TMIN`` se lee de ``future_root``, ``td_hold`` queda en NaN
    (no hay verdad) y el filtro exige contexto completo y Tmin futura completa.
    """
    future = spec.name in FUTURE_SPLITS
    if future and future_root is None:
        raise ValueError(f"el split {spec.name!r} necesita future_root (Tmin 2017-2020)")
    root = Path(historical_root)
    wanted = np.asarray(sorted(set(int(i) for i in ids)), dtype=np.int64)
    if bucket is None:
        buckets = np.unique(wanted % NUM_BUCKETS)
        if buckets.size != 1:
            raise ValueError("build_panel espera IDs de un solo bucket; usa iter_panel_batches")
        bucket = int(buckets[0])

    years = range(spec.context_start_year, (spec.train_end_year if future else spec.holdout_years[1]) + 1)
    frame = _read_bucket(root, bucket, years)
    frame = frame[frame["ID"].isin(wanted)]
    if frame.empty:
        return None

    frame["FECHA"] = pd.to_datetime(frame["FECHA"])
    if future:
        fut = _read_future_bucket(Path(future_root), bucket, range(spec.holdout_years[0], spec.holdout_years[1] + 1))
        fut = fut[fut["ID"].isin(wanted)].copy()
        fut["FECHA"] = pd.to_datetime(fut["FECHA"])
        fut["TD"] = np.float32(np.nan)
        fut["doy"] = fut["FECHA"].dt.dayofyear.astype("int16")

    ctx_dates = pd.date_range(spec.context_start, spec.context_end, freq="D")
    hold_dates = pd.date_range(spec.holdout_start, spec.holdout_end, freq="D")

    ctx = frame[frame["FECHA"] <= spec.context_end]
    if future:
        hold = fut[(fut["FECHA"] >= spec.holdout_start) & (fut["FECHA"] <= spec.holdout_end)]
    else:
        hold = frame[(frame["FECHA"] >= spec.holdout_start) & (frame["FECHA"] <= spec.holdout_end)]

    # Celdas utiles: sin un solo NaN ni en contexto ni en el bloque oculto. En este
    # dataset la ausencia es por celda entera (mar y borde), nunca huecos parciales,
    # pero el filtro no lo asume.
    usable = set(wanted.tolist())
    # En `real` no hay Td futura: del hold-out solo se exige Tmin.
    checks = ((ctx, ["TD", "TMIN"]), (hold, ["TMIN"] if future else ["TD", "TMIN"]))
    for part, cols in checks:
        bad = part.loc[part[cols].isna().any(axis=1), "ID"].unique()
        usable -= set(int(v) for v in bad)
    counts = ctx.groupby("ID").size()
    usable &= {int(i) for i in counts.index[counts == len(ctx_dates)]}
    counts_h = hold.groupby("ID").size()
    usable &= {int(i) for i in counts_h.index[counts_h == len(hold_dates)]}
    if not usable:
        return None

    kept = np.asarray(sorted(usable), dtype=np.int64)
    ctx = ctx[ctx["ID"].isin(usable)]
    hold = hold[hold["ID"].isin(usable)]

    # Climatologia solo con anios de train, replicando backtest.train_only_climatology.
    clim = (
        ctx.groupby(["ID", "doy"], sort=False)
        .agg(TD_clim=("TD", "mean"), TMIN_clim=("TMIN", "mean"))
        .reset_index()
    )
    td_clim = np.full((kept.size, 367), np.nan, dtype=np.float32)
    tmin_clim = np.full((kept.size, 367), np.nan, dtype=np.float32)
    row_of = {int(v): i for i, v in enumerate(kept)}
    rows = np.fromiter((row_of[int(v)] for v in clim["ID"]), dtype=np.int64, count=len(clim))
    cols = clim["doy"].to_numpy(dtype=np.int64)
    td_clim[rows, cols] = clim["TD_clim"].to_numpy(dtype=np.float32)
    tmin_clim[rows, cols] = clim["TMIN_clim"].to_numpy(dtype=np.float32)

    return PanelBatch(
        spec=spec,
        ids=kept,
        td_ctx=_pivot(ctx, "TD", kept, ctx_dates),
        tmin_ctx=_pivot(ctx, "TMIN", kept, ctx_dates),
        td_hold=(
            np.full((kept.size, len(hold_dates)), np.nan, dtype=np.float32)
            if future
            else _pivot(hold, "TD", kept, hold_dates)
        ),
        tmin_hold=_pivot(hold, "TMIN", kept, hold_dates),
        td_clim=td_clim,
        tmin_clim=tmin_clim,
        ctx_doy=ctx_dates.dayofyear.to_numpy(dtype=np.int16),
        hold_doy=hold_dates.dayofyear.to_numpy(dtype=np.int16),
        ctx_dates=ctx_dates,
        hold_dates=hold_dates,
    )


def merge_panels(batches: Sequence[PanelBatch]) -> PanelBatch:
    """Une lotes que comparten split y calendario.

    Los paneles de buckets distintos tienen exactamente el mismo eje temporal, asi
    que unirlos es concatenar por celdas. Hace falta porque una muestra
    estratificada reparte una celda por bucket y, sin unir, la GPU recibiria las
    series de una en una.
    """
    if not batches:
        raise ValueError("no hay lotes que unir")
    head = batches[0]
    if len(batches) == 1:
        return head
    for other in batches[1:]:
        if other.spec != head.spec:
            raise ValueError("no se pueden unir lotes de splits distintos")
    return PanelBatch(
        spec=head.spec,
        ids=np.concatenate([b.ids for b in batches]),
        td_ctx=np.concatenate([b.td_ctx for b in batches]),
        tmin_ctx=np.concatenate([b.tmin_ctx for b in batches]),
        td_hold=np.concatenate([b.td_hold for b in batches]),
        tmin_hold=np.concatenate([b.tmin_hold for b in batches]),
        td_clim=np.concatenate([b.td_clim for b in batches]),
        tmin_clim=np.concatenate([b.tmin_clim for b in batches]),
        ctx_doy=head.ctx_doy,
        hold_doy=head.hold_doy,
        ctx_dates=head.ctx_dates,
        hold_dates=head.hold_dates,
    )


def iter_panel_batches(
    ids: Iterable[int],
    spec: SplitSpec,
    *,
    historical_root: Path | str = DEFAULT_HISTORICAL_ROOT,
    max_cells_per_batch: int = 256,
    read_workers: int = 8,
    future_root: Path | str | None = None,
) -> Iterator[PanelBatch]:
    """Emite lotes de hasta ``max_cells_per_batch`` celdas, cruzando buckets.

    Los buckets se leen en paralelo (la lectura de parquet suelta el GIL) y las
    celdas se acumulan hasta llenar el lote, de modo que el tamano del lote no
    dependa de cuantas celdas caigan en cada bucket.

    La lectura anticipada esta acotada a ``read_workers * 2`` buckets. Sin ese
    limite la huella en memoria crece con el numero total de buckets y no con el
    tamano del lote: ``ThreadPoolExecutor.map`` encola todas las tareas de golpe y
    retiene sus resultados. Con las 17.041 celdas del panel nacional eso eran
    1,6 GB y pasaba inadvertido; con las 436.519 celdas de los cuatro
    departamentos, repartidas entre los 8.192 buckets, llego a 53 GB.
    """
    grouped = _buckets_for(list(ids))
    root = Path(historical_root)
    workers = max(1, read_workers)
    prefetch = workers * 2
    pending: list[PanelBatch] = []
    held = 0

    def load(bucket: int) -> list[PanelBatch]:
        members = grouped[bucket]
        out = []
        for start in range(0, members.size, max_cells_per_batch):
            chunk = members[start : start + max_cells_per_batch]
            extra = {} if future_root is None else {"future_root": future_root}
            panel = build_panel(chunk, spec, historical_root=root, bucket=bucket, **extra)
            if panel is not None:
                out.append(panel)
        return out

    buckets = sorted(grouped)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for window_start in range(0, len(buckets), prefetch):
            window = buckets[window_start : window_start + prefetch]
            for produced in pool.map(load, window):
                for panel in produced:
                    pending.append(panel)
                    held += panel.n_cells
                    while held >= max_cells_per_batch:
                        merged = merge_panels(pending)
                        yield _slice_panel(merged, 0, max_cells_per_batch)
                        remainder = _slice_panel(merged, max_cells_per_batch, merged.n_cells)
                        pending = [remainder] if remainder.n_cells else []
                        held = remainder.n_cells if remainder.n_cells else 0
    if pending:
        merged = merge_panels(pending)
        if merged.n_cells:
            yield merged


def _slice_panel(panel: PanelBatch, start: int, stop: int) -> PanelBatch:
    return PanelBatch(
        spec=panel.spec,
        ids=panel.ids[start:stop],
        td_ctx=panel.td_ctx[start:stop],
        tmin_ctx=panel.tmin_ctx[start:stop],
        td_hold=panel.td_hold[start:stop],
        tmin_hold=panel.tmin_hold[start:stop],
        td_clim=panel.td_clim[start:stop],
        tmin_clim=panel.tmin_clim[start:stop],
        ctx_doy=panel.ctx_doy,
        hold_doy=panel.hold_doy,
        ctx_dates=panel.ctx_dates,
        hold_dates=panel.hold_dates,
    )
