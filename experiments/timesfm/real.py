"""Producto TimesFM 2017-2020 sobre las celdas con Td, por buckets (E9, PLAN_3).

Una pasada zero-shot de ``tmin_anom_full``: contexto 1981-2016, horizonte 2017-01-01 a
2020-12-31 con la Tmin futura regridada de ``future_tmin_by_bucket``. No hay verdad
observada en 2017-2020: lo que se produce es una prediccion, no un resultado medido.

La unidad de trabajo es un bucket (``ID % 8192``). Cada uno se escribe de forma
atomica (``pred.parquet.tmp`` -> ``pred.parquet``) y termina con un sentinela
``.done`` (JSON). Reanudar es relanzar el mismo comando. Nada se escribe bajo
``$RES``.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import logging
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from importlib import metadata
from pathlib import Path
from typing import Callable, Mapping, Sequence

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.bucket_layout import bucket_dir_name

from . import paths
from .panel import (
    DEFAULT_HISTORICAL_ROOT,
    NUM_BUCKETS,
    PanelBatch,
    build_panel,
    split_spec,
)
from .run import QUANTILE_COLUMNS, build_inputs, enable_tf32, load_model, predict_panel, to_physical
from .variants import CHECKPOINT_REVISION, Variant, variant

logger = logging.getLogger("timesfm.real")

VARIANT_KEY = "tmin_anom_full"
SPLIT = "real"
EXPECTED_CELLS = 2_178_827
HORIZON_START = pd.Timestamp("2017-01-01")
HORIZON_DAYS = 1461
# Cambiar esto invalida los .done existentes: el formato o la semantica cambiaron.
CODE_VERSION = "real-v1"
MANIFEST_REF_REAL = "docs/protocol/timesfm_manifest_addendum_real_2017_2020.yaml"
MLFLOW_EXPERIMENT = "tdew-timesfm-benchmark"
DEFAULT_PALACIOS_ROOT = paths.RES / "tuning/predictions_2017_2020"
DEFAULT_FUTURE_ROOT = paths.RES / "future_tmin_by_bucket"
DEFAULT_OUT_DIR = paths.WORK / "preds_real"

RES_ROOT = paths.RES

DONE_NAME = ".done"
PRED_NAME = "pred.parquet"
TMP_SUFFIX = ".tmp"

_SCHEMA = pa.schema(
    [("ID", pa.int32()), ("day", pa.int16()), ("pred", pa.float32())]
    + [(name, pa.float32()) for name in QUANTILE_COLUMNS]
)


def refuse_under_res(path: Path | str) -> None:
    """PLAN_3 sec. 5: nada se escribe bajo ``$RES``."""
    resolved = Path(path).expanduser().resolve()
    if resolved == RES_ROOT or RES_ROOT in resolved.parents:
        raise ValueError(f"{resolved} esta bajo $RES ({RES_ROOT}); no se escribe ahi")


class ResumeMismatch(RuntimeError):
    """Un ``.done`` existente no corresponde a las celdas o al codigo actuales."""


class DiskSpaceError(RuntimeError):
    """Queda menos espacio libre que el umbral configurado."""


# ---------------------------------------------------------------------- calendario

def day_to_date(days: np.ndarray) -> pd.DatetimeIndex:
    """``day`` (dias desde 2017-01-01) -> fecha."""
    return HORIZON_START + pd.to_timedelta(np.asarray(days, dtype=np.int64), unit="D")


def date_to_day(dates) -> np.ndarray:
    """Fecha -> ``day`` int16 (0 a 1460)."""
    delta = pd.DatetimeIndex(dates) - HORIZON_START
    return np.asarray(delta.days, dtype=np.int16)


# ---------------------------------------------------------------------- celdas

def ids_hash(ids: Sequence[int] | np.ndarray) -> str:
    """Huella de un conjunto de IDs; no depende del orden."""
    arr = np.unique(np.asarray(ids, dtype=np.int64))
    return hashlib.sha256(arr.tobytes()).hexdigest()


def _read_palacios_bucket(root: Path, bucket: int) -> np.ndarray:
    path = root / bucket_dir_name(bucket) / PRED_NAME
    ids = np.unique(pq.read_table(path, columns=["ID"]).column("ID").to_numpy())
    wrong = ids[ids % NUM_BUCKETS != bucket]
    if wrong.size:
        raise ValueError(
            f"{path}: {wrong.size} IDs no pertenecen al bucket {bucket} (p. ej. {int(wrong[0])})"
        )
    return ids.astype(np.int64)


def list_cells(
    palacios_root: Path | str,
    buckets: Sequence[int] | None = None,
    *,
    workers: int = 8,
) -> dict[int, np.ndarray]:
    """IDs del producto de Palacios, por bucket. Solo lee la columna ``ID``."""
    root = Path(palacios_root)
    if buckets is None:
        names = sorted(p.name for p in root.glob("id_bucket=*") if (p / PRED_NAME).exists())
        buckets = [int(n.split("=")[1]) for n in names]
    buckets = sorted(int(b) for b in buckets)
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        arrays = list(pool.map(lambda b: _read_palacios_bucket(root, b), buckets))
    return {b: a for b, a in zip(buckets, arrays) if a.size}


def check_total(cells: Mapping[int, np.ndarray]) -> None:
    total = sum(int(a.size) for a in cells.values())
    if total != EXPECTED_CELLS:
        raise ValueError(f"el producto de Palacios tiene {total} celdas y se esperaban {EXPECTED_CELLS}")


# ---------------------------------------------------------------------- E/S atomica

def _fsync_path(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 22), b""):
            digest.update(block)
    return digest.hexdigest()


def _bucket_path(out_dir: Path, bucket: int) -> Path:
    return out_dir / bucket_dir_name(bucket)


def _read_done(out_dir: Path, bucket: int) -> dict | None:
    path = _bucket_path(out_dir, bucket) / DONE_NAME
    if not path.exists():
        return None
    return json.loads(path.read_text())


def bucket_done(out_dir: Path, bucket: int, *, ids_hash_value: str) -> bool:
    """Verdadero si el bucket ya termino con las mismas celdas y el mismo codigo.

    Un ``.done`` que no coincide NO se descarta en silencio: reescribirlo
    mezclaria productos distintos bajo el mismo directorio.
    """
    done = _read_done(out_dir, bucket)
    if done is None:
        return False
    if done.get("ids_hash") != ids_hash_value:
        raise ResumeMismatch(f"bucket {bucket}: ids_hash distinto del que figura en el .done")
    if done.get("code_version") != CODE_VERSION:
        raise ResumeMismatch(
            f"bucket {bucket}: code_version {done.get('code_version')!r} != {CODE_VERSION!r}"
        )
    return (_bucket_path(out_dir, bucket) / PRED_NAME).exists()


def clean_orphans(out_dir: Path) -> list[Path]:
    """Borra los ``*.tmp`` que dejo una corrida interrumpida."""
    removed = []
    for path in out_dir.glob("id_bucket=*/*"):
        if path.name.endswith(TMP_SUFFIX):
            path.unlink()
            removed.append(path)
    return removed


def check_disk(out_dir: Path, min_free_gb: float) -> float:
    free = shutil.disk_usage(out_dir).free / 1e9
    if free < min_free_gb:
        raise DiskSpaceError(
            f"quedan {free:.1f} GB libres en {out_dir} y el umbral es {min_free_gb} GB; "
            "los .done conservan el progreso, libera espacio y relanza el mismo comando"
        )
    return free


# ---------------------------------------------------------------------- un bucket

def _build_table(panel: PanelBatch, point: np.ndarray, quantiles: np.ndarray) -> pa.Table:
    n, horizon = point.shape
    columns = {
        "ID": np.repeat(panel.ids.astype(np.int32), horizon),
        "day": np.tile(date_to_day(panel.hold_dates), n),
        "pred": point.astype(np.float32).ravel(),
    }
    for index, name in enumerate(QUANTILE_COLUMNS):
        columns[name] = quantiles[:, :, index].astype(np.float32).ravel()
    return pa.Table.from_pydict(columns, schema=_SCHEMA)


def _timesfm_version() -> str:
    try:
        return metadata.version("timesfm")
    except metadata.PackageNotFoundError:
        return "desconocida"


def _omitted(requested: np.ndarray, kept: np.ndarray) -> list[dict]:
    missing = sorted(set(int(i) for i in requested) - set(int(i) for i in kept))
    reason = "contexto 1981-2016 o Tmin futura 2017-2020 incompletos o ausentes"
    return [{"id": i, "reason": reason} for i in missing]


def run_bucket(
    model,
    spec: Variant,
    bucket: int,
    ids: np.ndarray,
    *,
    historical_root: Path,
    future_root: Path,
    out_dir: Path,
    batch_size: int = 4,
    predict: Callable = predict_panel,
    panel: PanelBatch | None | str = "build",
    tf32: bool = True,
) -> dict:
    """Predice un bucket y lo escribe de forma atomica. Devuelve el resumen del ``.done``."""
    started = time.time()
    panel_spec = split_spec(SPLIT, context_start_year=spec.context_start_year)
    if isinstance(panel, str):
        panel = build_panel(ids, panel_spec, historical_root=historical_root,
                            bucket=bucket, future_root=future_root)
    directory = _bucket_path(out_dir, bucket)
    directory.mkdir(parents=True, exist_ok=True)
    final, tmp = directory / PRED_NAME, directory / (PRED_NAME + TMP_SUFFIX)
    done_path = directory / DONE_NAME
    done_tmp = directory / (DONE_NAME + TMP_SUFFIX)

    if panel is not None:
        stray = [int(i) for i in panel.ids if int(i) % NUM_BUCKETS != bucket or int(i) not in set(ids.tolist())]
        if stray:
            raise ValueError(f"bucket {bucket}: el panel trae celdas ajenas al bucket (p. ej. {stray[0]})")
    if panel is None:
        table = _SCHEMA.empty_table()
        kept = np.array([], dtype=np.int64)
        effective, violations = batch_size, 0
    else:
        point, quantiles, effective = predict(model, panel, spec, batch_size=batch_size)
        point, quantiles = to_physical(point, panel, spec), to_physical(quantiles, panel, spec)
        if not (np.isfinite(point).all() and np.isfinite(quantiles).all()):
            raise ValueError(f"bucket {bucket}: la prediccion tiene valores no finitos")
        violations = int((np.diff(quantiles, axis=2) < 0).any(axis=2).sum())
        table = _build_table(panel, point, quantiles)
        kept = panel.ids

    try:
        pq.write_table(table, tmp, compression="zstd")
        _fsync_path(tmp)
        os.replace(tmp, final)
        _fsync_dir(directory)
    finally:
        if tmp.exists():
            tmp.unlink()

    seconds = time.time() - started
    written = int(kept.size)
    done = {
        "bucket": int(bucket),
        "cells_requested": int(len(ids)),
        "cells_written": written,
        "cells_omitted": _omitted(ids, kept),
        "rows": int(table.num_rows),
        "bytes": final.stat().st_size,
        "sha256": _sha256(final),
        "seconds": seconds,
        "cells_per_second": written / seconds if seconds > 0 else float("nan"),
        "effective_batch": int(effective),
        "quantile_violation_rows": violations,
        "git_commit": prov.git_commit(),
        "ids_hash": ids_hash(ids),
        "code_version": CODE_VERSION,
        "generated_at": prov.now_iso(),
        "tf32": bool(tf32),
        "timesfm_version": _timesfm_version(),
    }
    try:
        done_tmp.write_text(json.dumps(done, indent=1, sort_keys=True))
        _fsync_path(done_tmp)
        os.replace(done_tmp, done_path)
        _fsync_dir(directory)
    finally:
        if done_tmp.exists():
            done_tmp.unlink()
    return done


# ---------------------------------------------------------------------- toda la corrida

def run_real(
    cells: Mapping[int, np.ndarray],
    *,
    out_dir: Path,
    historical_root: Path = DEFAULT_HISTORICAL_ROOT,
    future_root: Path = DEFAULT_FUTURE_ROOT,
    model=None,
    predict: Callable = predict_panel,
    batch_size: int = 4,
    min_free_gb: float = 60.0,
    prefetch_workers: int = 2,
    tf32: bool = True,
) -> dict:
    """Recorre los buckets en orden ascendente, saltando los que ya tienen ``.done``."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    clean_orphans(out_dir)
    spec = variant(VARIANT_KEY)
    panel_spec = split_spec(SPLIT, context_start_year=spec.context_start_year)

    buckets = sorted(cells)
    pending = [b for b in buckets if not bucket_done(out_dir, b, ids_hash_value=ids_hash(cells[b]))]
    skipped = len(buckets) - len(pending)
    logger.info("%d buckets, %d ya terminados, %d por hacer", len(buckets), skipped, len(pending))

    def load(bucket: int):
        return build_panel(cells[bucket], panel_spec, historical_root=historical_root,
                           bucket=bucket, future_root=future_root)

    ran, written, started = 0, 0, time.time()
    ahead = max(1, prefetch_workers) * 2
    with ThreadPoolExecutor(max_workers=max(1, prefetch_workers)) as pool:
        futures: dict[int, object] = {}

        def fill(upto: int) -> None:
            for b in pending[upto : upto + ahead]:
                if b not in futures:
                    futures[b] = pool.submit(load, b)

        try:
            for index, bucket in enumerate(pending):
                fill(index)
                free = check_disk(out_dir, min_free_gb)
                panel = futures.pop(bucket).result()
                done = run_bucket(
                    model, spec, bucket, cells[bucket], historical_root=historical_root,
                    future_root=future_root, out_dir=out_dir, batch_size=batch_size,
                    predict=predict, panel=panel, tf32=tf32,
                )
                ran += 1
                written += done["cells_written"]
                logger.info(
                    "bucket %04d: %d celdas, %.1f s, %.2f celdas/s | acumulado %.2f celdas/s | libre %.0f GB",
                    bucket, done["cells_written"], done["seconds"], done["cells_per_second"],
                    written / max(time.time() - started, 1e-9), free,
                )
        finally:
            for fut in futures.values():
                fut.cancel()
    elapsed = time.time() - started
    return {
        "buckets_total": len(buckets), "buckets_run": ran, "buckets_skipped": skipped,
        "cells_written": written, "seconds": elapsed,
        "cells_per_second": written / elapsed if elapsed > 0 else float("nan"),
    }


# ---------------------------------------------------------------------- manifiesto y verificacion

_MANIFEST_COLUMNS = (
    "bucket", "cells_requested", "cells_written", "n_omitted", "rows", "bytes", "sha256",
    "seconds", "cells_per_second", "quantile_violation_rows", "ids_hash", "code_version",
    "git_commit", "generated_at",
)


def _done_files(out_dir: Path) -> list[dict]:
    rows = []
    for path in sorted(Path(out_dir).glob(f"id_bucket=*/{DONE_NAME}")):
        rows.append(json.loads(path.read_text()))
    return rows


def write_manifest(out_dir: Path) -> pd.DataFrame:
    """``MANIFEST.csv``: una fila por bucket terminado, regenerada desde los ``.done``."""
    rows = []
    for done in _done_files(out_dir):
        done = dict(done)
        done["n_omitted"] = len(done.get("cells_omitted", []))
        rows.append({k: done.get(k) for k in _MANIFEST_COLUMNS})
    manifest = pd.DataFrame(rows, columns=list(_MANIFEST_COLUMNS)).sort_values("bucket").reset_index(drop=True)
    manifest.to_csv(Path(out_dir) / "MANIFEST.csv", index=False)
    return manifest


def run_totals(out_dir: Path) -> dict:
    """Totales de todos los ``.done`` (no solo de esta invocacion)."""
    done = _done_files(out_dir)
    rows = sum(d["rows"] for d in done)
    size = sum(d["bytes"] for d in done)
    seconds = sum(d["seconds"] for d in done)
    cells = sum(d["cells_written"] for d in done)
    return {
        "buckets_total": len(done),
        "cells_written": cells,
        "cells_omitted": sum(len(d["cells_omitted"]) for d in done),
        "rows": rows,
        "bytes": size,
        "bytes_per_row": size / rows if rows else float("nan"),
        "seconds": seconds,
        "cells_per_second": cells / seconds if seconds > 0 else float("nan"),
        "quantile_violation_rows": sum(d["quantile_violation_rows"] for d in done),
    }


def _verify_bucket(out_dir: Path, bucket: int, ids: np.ndarray) -> dict:
    row = {"bucket": bucket, "ok": False, "problem": ""}
    directory = _bucket_path(out_dir, bucket)
    done = _read_done(out_dir, bucket)
    path = directory / PRED_NAME
    if done is None or not path.exists():
        row["problem"] = "falta .done o pred.parquet"
        return row
    # ParquetFile y no read_table: este ultimo infiere la particion hive del nombre
    # del directorio y agrega una columna `id_bucket` que no esta en el archivo.
    table = pq.ParquetFile(path).read()
    if table.schema != _SCHEMA:
        row["problem"] = f"esquema distinto: {table.schema}"
        return row
    frame = table.to_pandas()
    got = np.unique(frame["ID"].to_numpy())
    expected = np.unique(np.asarray(ids, dtype=np.int64))
    omitted = {o["id"] for o in done["cells_omitted"]}
    if set(got.tolist()) != set(expected.tolist()) - omitted:
        row["problem"] = "los IDs no coinciden con los de Palacios (descontando omitidas)"
        return row
    per_cell = frame.groupby("ID")["day"].agg(["count", "min", "max", "nunique"])
    if not ((per_cell["count"] == HORIZON_DAYS) & (per_cell["nunique"] == HORIZON_DAYS)
            & (per_cell["min"] == 0) & (per_cell["max"] == HORIZON_DAYS - 1)).all():
        row["problem"] = "alguna celda no tiene 1.461 dias distintos de 0 a 1460"
        return row
    values = frame[["pred", *QUANTILE_COLUMNS]].to_numpy()
    if not np.isfinite(values).all():
        row["problem"] = "NaN o infinitos"
        return row
    if len(frame) != done["rows"]:
        row["problem"] = "filas distintas de las del .done"
        return row
    if path.stat().st_size != done["bytes"]:
        row["problem"] = "tamano distinto del .done"
        return row
    if _sha256(path) != done["sha256"]:
        row["problem"] = "sha256 distinto del .done"
        return row
    sorted_ok = frame[["ID", "day"]].equals(frame[["ID", "day"]].sort_values(["ID", "day"]).reset_index(drop=True))
    row.update(
        ok=bool(sorted_ok), problem="" if sorted_ok else "filas sin ordenar por (ID, day)",
        cells=int(len(got)), rows=int(len(frame)),
        quantile_violation_rows=int((np.diff(frame[list(QUANTILE_COLUMNS)].to_numpy(), axis=1) < 0).any(axis=1).sum()),
        omitted=len(omitted),
    )
    return row


def verify_outputs(out_dir: Path, cells: Mapping[int, np.ndarray]) -> pd.DataFrame:
    """Revisa cada bucket contra las celdas de Palacios. ``ok`` es por bucket.

    Un archivo ilegible no aborta la revision: queda como ``ok=False`` con el motivo.
    """
    out_dir = Path(out_dir)
    rows = []
    for b in sorted(cells):
        try:
            rows.append(_verify_bucket(out_dir, b, cells[b]))
        except Exception as exc:  # noqa: BLE001 - se informa, no se oculta
            rows.append({"bucket": b, "ok": False, "problem": f"{type(exc).__name__}: {exc}"})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------- proveniencia y MLflow

def build_real_provenance(
    *,
    n_cells: int,
    ids_file: Path,
    out_dir: Path,
    future_root: Path,
    bead_id: str = "tdew-214.13",
    seeds: Sequence[int] = (),
    tf32: bool = True,
) -> prov.MetricProvenance:
    """Un registro por corrida (no por bucket)."""
    spec = variant(VARIANT_KEY)
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=MANIFEST_REF_REAL,
        model_family=spec.family,
        model_id=spec.checkpoint,
        variant_label=spec.key,
        trained=False,
        training_period=None,
        validation_period=None,
        test_period=("2017-01-01", "2020-12-31"),
        split_id="real_2017_2020",
        autoregressive=False,  # decodificacion de una pasada, sin recursion sobre Td predicho
        target_type=spec.target_type,
        climatology_used=spec.climatology_used,
        climatology_role=spec.climatology_role,
        inputs=tuple(spec.inputs),
        panel_id=f"real_{n_cells}_td",
        panel_cell_count=int(n_cells),
        panel_file=str(ids_file),
        output_files=(str(out_dir),),
        seeds=tuple(seeds),
        notes=(
            "Producto 2017-2020 sin verdad observada: las metricas posteriores son de acuerdo "
            "entre productos, no de error. Pesos de TimesFM 3.0 de uso no comercial: entregable "
            f"de investigacion, no operativo. TF32 {'activado' if tf32 else 'desactivado'}, make_positive=False, "
            f"timesfm {_timesfm_version()}, Tmin futura leida de {future_root} (future_tmin_by_bucket), "
            f"contexto 1981-2016, un bucket por unidad de trabajo, code_version={CODE_VERSION}, "
            f"checkpoint {spec.checkpoint}@{CHECKPOINT_REVISION}."
        ),
    )


def log_mlflow(
    summary: Mapping[str, float],
    *,
    tracking_uri: str = et.DEFAULT_TRACKING_URI,
    experiment_name: str = MLFLOW_EXPERIMENT,
    run_name: str,
    params: Mapping[str, object] | None = None,
) -> str:
    """Una corrida de MLflow (evaluacion, no entrenamiento) con las metricas numericas."""
    import mlflow

    metrics = {k: float(v) for k, v in summary.items() if isinstance(v, (int, float, np.integer, np.floating))
               and np.isfinite(v)}
    with et.start_run(
        run_name, params=dict(params or {}), tracking_uri=tracking_uri, experiment_name=experiment_name,
    ) as run:
        mlflow.log_metrics(metrics)
        return run.info.run_id


# ---------------------------------------------------------------------- CLI

def parse_buckets(text: str) -> list[int]:
    """'0,1' o '0-3' o mezcla: '0-2,9'."""
    out: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = (int(v) for v in part.split("-"))
            out.extend(range(lo, hi + 1))
        else:
            out.append(int(part))
    bad = [b for b in out if not 0 <= b < NUM_BUCKETS]
    if bad:
        raise ValueError(f"buckets fuera de rango: {bad}")
    return sorted(set(out))


def _write_plan(out_dir: Path, cells: Mapping[int, np.ndarray]) -> tuple[Path, Path]:
    total = sum(int(a.size) for a in cells.values())
    ids_path = out_dir / f"ids_real_{total}.csv"
    ids = np.sort(np.concatenate([cells[b] for b in sorted(cells)]))
    pd.DataFrame({"ID": ids}).to_csv(ids_path, index=False)
    plan_path = out_dir / "bucket_plan.csv"
    pd.DataFrame({"bucket": sorted(cells), "cells": [int(cells[b].size) for b in sorted(cells)]}).to_csv(
        plan_path, index=False
    )
    return ids_path, plan_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--palacios-root", type=Path, default=DEFAULT_PALACIOS_ROOT)
    parser.add_argument("--ids-from-palacios", action="store_true",
                        help="las celdas siempre salen del producto de Palacios; opcion por compatibilidad con PLAN_3")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--historical-root", type=Path, default=DEFAULT_HISTORICAL_ROOT)
    parser.add_argument("--future-root", type=Path, default=DEFAULT_FUTURE_ROOT)
    parser.add_argument("--buckets", default=None, help="'0,1' o '0-3'; por defecto, todos (smoke test: pocos)")
    parser.add_argument("--batch-size", type=int, default=32,
                        help="medido: 4 -> 3,4; 16 -> 4,1; 32 -> 4,4 celdas/s, salida identica bit a bit")
    parser.add_argument("--min-free-gb", type=float, default=60.0)
    parser.add_argument("--prefetch-workers", type=int, default=2)
    parser.add_argument("--no-tf32", action="store_true")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--bead-id", default="tdew-214.13")
    parser.add_argument("--plan-only", action="store_true", help="solo lista celdas y buckets")
    parser.add_argument("--verify-only", action="store_true", help="solo verifica un producto terminado")
    parser.add_argument("--mlflow", action="store_true")
    parser.add_argument("--mlflow-uri", default=et.DEFAULT_TRACKING_URI)
    parser.add_argument("--mlflow-experiment", default=MLFLOW_EXPERIMENT)
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    out_dir: Path = args.out_dir
    refuse_under_res(out_dir)
    refuse_under_res(args.registry_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    subset = parse_buckets(args.buckets) if args.buckets else None

    cells = list_cells(args.palacios_root, subset)
    total = sum(int(a.size) for a in cells.values())
    if subset is None:
        check_total(cells)
    logger.info("%d celdas en %d buckets", total, len(cells))
    # El plan describe el producto completo: ni un subconjunto ni --verify-only lo reescriben.
    ids_path = out_dir / f"ids_real_{total}.csv"
    if args.plan_only or (subset is None and not args.verify_only):
        ids_path, _ = _write_plan(out_dir, cells)
    if args.plan_only:
        print(json.dumps({"cells": total, "buckets": len(cells), "ids_file": str(ids_path)}))
        return 0

    if args.verify_only:
        (out_dir / "verify_real.csv").unlink(missing_ok=True)
        report = verify_outputs(out_dir, cells)
        report.to_csv(out_dir / "verify_real.csv", index=False)
        manifest = write_manifest(out_dir)
        bad = int((~report["ok"]).sum())
        print(json.dumps({"buckets": len(report), "buckets_fallidos": bad, "manifest_rows": len(manifest)}))
        return 0 if bad == 0 else 2

    tf32 = not args.no_tf32
    if args.device == "cuda" and tf32:
        enable_tf32()
    spec = variant(VARIANT_KEY)
    model = load_model(spec, device=args.device, batch_size=args.batch_size)
    try:
        summary = run_real(
            cells, out_dir=out_dir, historical_root=args.historical_root, future_root=args.future_root,
            model=model, batch_size=args.batch_size, min_free_gb=args.min_free_gb,
            prefetch_workers=args.prefetch_workers, tf32=tf32,
        )
    except DiskSpaceError as exc:
        logger.error("%s", exc)
        return 3

    manifest = write_manifest(out_dir)
    totals = run_totals(out_dir)
    logger.info("manifiesto: %d buckets; totales %s", len(manifest), totals)
    record = build_real_provenance(
        n_cells=total, ids_file=ids_path, out_dir=out_dir, future_root=args.future_root,
        bead_id=args.bead_id, tf32=tf32,
    )
    if args.mlflow:
        run_id = log_mlflow(
            {**totals, **{f"run_{k}": v for k, v in summary.items()}},
            tracking_uri=args.mlflow_uri, experiment_name=args.mlflow_experiment,
            run_name=args.run_name or f"timesfm-real-{len(cells)}buckets",
            params={"split": SPLIT, "variant": VARIANT_KEY, "panel_id": record.panel_id,
                    "bead_id": args.bead_id, "trained": False, "code_version": CODE_VERSION,
                    "tf32": tf32, "batch_size": args.batch_size, "out_dir": str(out_dir)},
        )
        record = dataclasses.replace(record, mlflow_run_id=run_id)
    prov.record_metric_provenance(record, registry_path=args.registry_path)
    print(json.dumps({"summary": summary, "totals": totals, "mlflow_run_id": record.mlflow_run_id}, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
