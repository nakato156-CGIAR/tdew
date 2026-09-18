#!/usr/bin/env python3
"""
pipeline.gold

Gold layer: join the silver tables into the master per-(ID, date) feature
table — daily TMIN/TD values, their per-ID/day-of-year climatology and
anomaly, and the static (DEM, TDI, X, Y) + monthly-normal (LST_DAY,
LST_NIGHT) covariates from ``docs/MODEL_INPUTS.md``.

This is national-grid-resolution daily data (~2.8M cells x up to 366 days per
year): a plain ``groupby(["ID", "doy"])`` over the whole thing needs a key
space as large as one full year of data, which OOMs on a laptop (this is the
same wall ``tdew_estimation.bucketed_data`` already hit and solved for the
existing TD/TMIN pipeline — see the comment on ``shard_climatology_by_bucket``).
The fix here is the same one: reshuffle every table by ``id_bucket = ID %
NUM_BUCKETS`` first (``tdew_estimation.bucket_layout``), then compute
climatology/anomaly and join covariates one small bucket at a time.

Lagged anomalies (``TMIN_anom_lag1``, ``TD_anom_lag1/2``, ...) and the actual
LLR anomaly-regression training/forecasting are intentionally NOT done here —
that per-ID time-ordering step is already implemented, at this same scale, by
the bucketed pipeline in ``tdew_estimation`` (see ``Local/run_pipeline.sh`` /
``main.py``). This script only produces the clean join those steps consume.

TD (dewpoint) and TMAX are optional: if no ``silver/td/`` or ``silver/tmax/``
tables exist yet, their derived columns are simply omitted.

Climatology (``{var}_clim``) is computed ONLY from rows whose ``date`` falls
in the frozen training period (2002-2012, ``docs/protocol/week1_manifest.yaml``
/ ``period.splits``) — never from validation/test years — per the manifest's
``normalization_rule``. Rows outside 2002-2016 (e.g. TMIN/TMAX 1981-2001 and
2017-2020) get a climatology value too (same train-year-only per-doy mean) but
have no ``split`` label; downstream ``pipeline.features`` restricts to
2002-2016 and assigns train/validation/test.

Output
------
``Data/gold/model_input/id_bucket=XXXX/part.parquet`` — one row per (ID, date):
    ID, date, doy, month, TMIN, TMIN_clim, TMIN_anom,
    [TMAX, TMAX_clim, TMAX_anom,] [TD, TD_clim, TD_anom,]
    DEM, TDI, X, Y, LST_DAY, LST_NIGHT

Usage
-----
python -m pipeline.gold
python -m pipeline.gold --silver-dir Data/silver --gold-dir Data/gold --num-buckets 1024
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

from tdew_estimation.bucket_layout import discover_bucket_ids

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"
DEFAULT_GOLD_DIR = REPO_ROOT / "Data" / "gold"
DEFAULT_NUM_BUCKETS = 64

# Frozen training period (docs/protocol/week1_manifest.yaml, period.splits.train)
# — climatology is computed ONLY from these years, never from validation/test,
# per the manifest's normalization_rule.
TRAIN_YEAR_START = 2002
TRAIN_YEAR_END = 2012


def _bucket_path(root: Path, bucket_id: int) -> Path:
    """Matches the unpadded hive-style folder pandas/pyarrow write for
    ``partition_cols=["id_bucket"]`` (``tdew_estimation.bucket_layout.bucket_dir``
    zero-pads, so it does not point at these folders)."""
    return root / f"id_bucket={bucket_id}"


def _add_bucket_col(df: pd.DataFrame, num_buckets: int) -> pd.DataFrame:
    df["id_bucket"] = (df["ID"] % num_buckets).astype("int32")
    return df


def reshuffle_by_bucket(df: pd.DataFrame, out_root: Path, num_buckets: int) -> None:
    """Append ``df`` into ``out_root/id_bucket=XXXX/*.parquet``. Safe to call once
    per source file/chunk — each call writes new part files, never overwrites."""
    out_root.mkdir(parents=True, exist_ok=True)
    _add_bucket_col(df, num_buckets)
    df.to_parquet(out_root, partition_cols=["id_bucket"], index=False)


def reshuffle_daily_var(var_dir: Path, out_root: Path, num_buckets: int, *, overwrite: bool) -> bool:
    """Reshuffle every ``{var}_daily_*.parquet`` under ``var_dir`` into
    ``out_root`` by ID bucket. Returns False if ``var_dir`` has no files."""
    files = sorted(var_dir.glob("*_daily_*.parquet")) if var_dir.exists() else []
    if not files:
        return False
    if out_root.exists():
        if not overwrite:
            print(f"[gold] {out_root.name} already bucketed, skip")
            return True
        shutil.rmtree(out_root)
    for f in files:
        reshuffle_by_bucket(pd.read_parquet(f), out_root, num_buckets)
        print(f"[gold] bucketed {f.name}")
    return True


def reshuffle_lookup(path: Path, out_root: Path, num_buckets: int, *, overwrite: bool) -> bool:
    """Reshuffle a single small ID-keyed lookup table (static covariates, LST
    normals) into ``out_root`` by ID bucket."""
    if not path.exists():
        return False
    if out_root.exists():
        if not overwrite:
            print(f"[gold] {out_root.name} already bucketed, skip")
            return True
        shutil.rmtree(out_root)
    reshuffle_by_bucket(pd.read_parquet(path), out_root, num_buckets)
    print(f"[gold] bucketed {path.name}")
    return True


def add_climatology(df: pd.DataFrame, var: str) -> pd.DataFrame:
    """``{var}_clim`` is the per-(ID, doy) mean computed ONLY over
    ``TRAIN_YEAR_START..TRAIN_YEAR_END`` rows, then applied (left-merge) to
    every row of ``df`` — train, validation, test, and any year outside the
    2002-2016 modeling range. This is what keeps validation/test years out of
    the climatology/anomaly baseline (manifest ``normalization_rule``)."""
    df = df.rename(columns={"value": var})
    train_years = pd.DatetimeIndex(df["date"]).year
    train_mask = (train_years >= TRAIN_YEAR_START) & (train_years <= TRAIN_YEAR_END)
    clim = (
        df.loc[train_mask]
        .groupby(["ID", "doy"], as_index=False)[var]
        .mean()
        .rename(columns={var: f"{var}_clim"})
    )
    df = df.merge(clim, on=["ID", "doy"], how="left")
    df[f"{var}_anom"] = df[var] - df[f"{var}_clim"]
    return df


def build_bucket_table(
    bucket_id: int,
    *,
    tmin_root: Path,
    tmax_root: Path | None,
    td_root: Path | None,
    static_root: Path | None,
    lst_root: Path | None,
) -> pd.DataFrame:
    tmin = pd.read_parquet(_bucket_path(tmin_root, bucket_id)).drop(columns=["id_bucket"], errors="ignore")
    table = add_climatology(tmin, "TMIN")

    if tmax_root is not None:
        tmax_path = _bucket_path(tmax_root, bucket_id)
        if tmax_path.exists():
            tmax = pd.read_parquet(tmax_path).drop(columns=["id_bucket"], errors="ignore")
            tmax = add_climatology(tmax, "TMAX")
            table = table.merge(tmax, on=["ID", "date", "doy"], how="left")

    if td_root is not None:
        td_path = _bucket_path(td_root, bucket_id)
        if td_path.exists():
            td = pd.read_parquet(td_path).drop(columns=["id_bucket"], errors="ignore")
            td = add_climatology(td, "TD")
            table = table.merge(td, on=["ID", "date", "doy"], how="left")

    table["month"] = pd.DatetimeIndex(table["date"]).month

    if static_root is not None:
        static_path = _bucket_path(static_root, bucket_id)
        if static_path.exists():
            static = pd.read_parquet(static_path).drop(columns=["id_bucket"], errors="ignore")
            table = table.merge(static, on="ID", how="left")

    if lst_root is not None:
        lst_path = _bucket_path(lst_root, bucket_id)
        if lst_path.exists():
            lst = pd.read_parquet(lst_path).drop(columns=["id_bucket"], errors="ignore")
            table = table.merge(lst, on=["ID", "month"], how="left")

    return table.sort_values(["ID", "date"]).reset_index(drop=True)


def run(silver_dir: Path, gold_dir: Path, *, num_buckets: int = DEFAULT_NUM_BUCKETS, overwrite: bool = False) -> Path:
    if not silver_dir.exists():
        raise FileNotFoundError(f"Silver dir not found: {silver_dir}")
    gold_dir.mkdir(parents=True, exist_ok=True)
    bucketed_dir = gold_dir / "_bucketed"

    tmin_root = bucketed_dir / "tmin"
    if not reshuffle_daily_var(silver_dir / "tmin", tmin_root, num_buckets, overwrite=overwrite):
        raise FileNotFoundError(f"No tmin daily tables under {silver_dir}/tmin")

    tmax_root = bucketed_dir / "tmax"
    have_tmax = reshuffle_daily_var(silver_dir / "tmax", tmax_root, num_buckets, overwrite=overwrite)
    if not have_tmax:
        print("[gold] no silver/tmax tables found, omitting TMAX-derived columns")
        tmax_root = None

    td_root = bucketed_dir / "td"
    have_td = reshuffle_daily_var(silver_dir / "td", td_root, num_buckets, overwrite=overwrite)
    if not have_td:
        print("[gold] no silver/td tables found, omitting TD-derived columns")
        td_root = None

    static_root = bucketed_dir / "static"
    have_static = reshuffle_lookup(silver_dir / "static_covariates.parquet", static_root, num_buckets, overwrite=overwrite)
    if not have_static:
        print("[gold] no static_covariates.parquet found, skipping DEM/TDI/X/Y")
        static_root = None

    lst_root = bucketed_dir / "lst"
    have_lst = reshuffle_lookup(silver_dir / "lst_normals.parquet", lst_root, num_buckets, overwrite=overwrite)
    if not have_lst:
        print("[gold] no lst_normals.parquet found, skipping LST_DAY/LST_NIGHT")
        lst_root = None

    out_dir = gold_dir / "model_input"
    if overwrite and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    bucket_ids = discover_bucket_ids(tmin_root)
    for bucket_id in bucket_ids:
        out_path = out_dir / f"id_bucket={bucket_id}" / "part.parquet"
        if out_path.exists() and not overwrite:
            continue
        table = build_bucket_table(
            bucket_id,
            tmin_root=tmin_root,
            tmax_root=tmax_root,
            td_root=td_root,
            static_root=static_root,
            lst_root=lst_root,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        table.to_parquet(out_path, index=False)
    print(f"[gold] wrote {out_dir.relative_to(gold_dir.parent)} ({len(bucket_ids)} buckets)")
    return out_dir


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Gold layer: build the model-ready feature table.")
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    p.add_argument("--num-buckets", type=int, default=DEFAULT_NUM_BUCKETS)
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run(args.silver_dir, args.gold_dir, num_buckets=args.num_buckets, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
