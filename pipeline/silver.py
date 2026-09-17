#!/usr/bin/env python3
"""
pipeline.silver

Silver layer: conform the raw ``.nc`` rasters landed in bronze into tidy,
ID-indexed parquet tables. All inputs sit on the same full-Peru PISCOt grid
(lat x lon), so every table shares one ``ID`` space: row-major over
``(latitude, longitude)``, written once as ``grid_index.parquet``.

Two bronze layouts are supported for the daily rasters, both keyed by the same
``{var}_daily_...`` naming:
- flat, one ``.nc`` per year (PISCOt v1.2 tmin/tmax): ``{var}_daily_{year}.nc``
  directly under ``bronze_dir``.
- one subfolder per year, one ``.nc`` per month (PISCO v1.1 td, delivered as
  ``{var}_daily_{year}.zip`` and landed here already-extracted):
  ``{var}_daily_{year}/{var}_daily_{year}_{month:02d}.nc``.
Both feed the same ``extract_daily_var`` (it groups by the actual time
coordinate values found in the file, so it doesn't care whether a single
``.nc`` spans a year or a month).

Outputs under ``Data/silver``
------------------------------
- ``grid_index.parquet``            ID, latitude, longitude
- ``static_covariates.parquet``     ID, DEM, TDI, X, Y
- ``lst_normals.parquet``           ID, month (1-12), LST_DAY, LST_NIGHT
- ``{var}/{var}_daily_{year}_{month:02d}.parquet``  ID, date, doy, value (one
  per var/year/month; var in {tmin, tmax, td, ...} — whatever daily rasters
  exist under either bronze layout above)

Department filtering
---------------------
``extract_daily_var`` (tmin/tmax/td) is the expensive part of this pipeline —
full 2.8M-cell national grid x thousands of days. ``grid_index``/
``static_covariates``/``lst_normals`` stay full-country always (cheap: one
meshgrid + a handful of small covariate reads) since
``Data/silver/department_grid_ids/*.csv`` (see ``docs/CITY_GRID_IDS.md``) is
itself a spatial join against ``grid_index.parquet`` and so cannot exist
before a first run produces it.

Typical two-pass flow to scope a run to specific departments:
1. ``python -m pipeline.silver --skip-daily`` — writes grid_index.parquet
   (and static/LST) without touching tmin/tmax/td.
2. Generate ``Data/silver/department_grid_ids/{dept}.csv`` (snippet in
   ``docs/CITY_GRID_IDS.md``).
3. ``python -m pipeline.silver --departments lima,cusco,...`` — full run,
   with the tmin/tmax/td loops filtered to the union of those department IDs.

Usage
-----
python -m pipeline.silver
python -m pipeline.silver --bronze-dir Data/bronze --silver-dir Data/silver --overwrite
python -m pipeline.silver --skip-daily
python -m pipeline.silver --departments lima,cusco,iquitos_loreto,tarapoto_san_martin
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRONZE_DIR = REPO_ROOT / "Data" / "bronze"
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"

DAILY_VAR_RE = re.compile(r"^(?P<var>[a-zA-Z0-9]+)_daily_(?P<year>\d{4})\.nc$")
MONTHLY_DIR_RE = re.compile(r"^(?P<var>[a-zA-Z0-9]+)_daily_(?P<year>\d{4})$")


def _grid_index(lat: np.ndarray, lon: np.ndarray) -> pd.DataFrame:
    """Row-major (lat outer, lon inner) ID grid — matches how every 2D/3D
    raster here is reshaped to a flat cell axis."""
    LAT, LON = np.meshgrid(lat, lon, indexing="ij")
    return pd.DataFrame(
        {
            "ID": np.arange(LAT.size, dtype=np.int64),
            "latitude": LAT.reshape(-1),
            "longitude": LON.reshape(-1),
        }
    )


def build_grid_index(any_static_nc: Path) -> pd.DataFrame:
    with xr.open_dataset(any_static_nc) as ds:
        return _grid_index(ds["latitude"].values, ds["longitude"].values)


def extract_static_covariates(
    covariate_files: dict[str, Path], grid: pd.DataFrame
) -> pd.DataFrame:
    """``covariate_files`` maps output column name -> path to a 2D (lat, lon)
    ``.nc`` file (e.g. ``{"DEM": .../DEM.nc, "TDI": .../TDI.nc}``)."""
    out = grid[["ID"]].copy()
    for col, path in covariate_files.items():
        with xr.open_dataset(path) as ds:
            data_var = next(v for v in ds.data_vars if v != "crs")
            arr = ds[data_var].transpose("latitude", "longitude").values
        out[col] = arr.reshape(-1).astype(np.float32)
    return out


def extract_lst_normals(lst_day: Path, lst_night: Path, grid: pd.DataFrame) -> pd.DataFrame:
    """Monthly-normal land-surface temperature, long form: one row per
    ``(ID, month)``."""
    frames = []
    for col, path in (("LST_DAY", lst_day), ("LST_NIGHT", lst_night)):
        with xr.open_dataset(path) as ds:
            data_var = next(v for v in ds.data_vars if v != "crs")
            da = ds[data_var].transpose("z", "latitude", "longitude")
            n_months = da.sizes["z"]
            vals = da.values.reshape(n_months, -1).astype(np.float32)
        frames.append(
            pd.DataFrame(
                {
                    "ID": np.tile(grid["ID"].to_numpy(), n_months),
                    "month": np.repeat(np.arange(1, n_months + 1), len(grid)),
                    col: vals.reshape(-1),
                }
            )
        )
    return frames[0].merge(frames[1], on=["ID", "month"])


def load_department_ids(silver_dir: Path, departments: list[str]) -> np.ndarray:
    """Union of grid ``ID``s across ``Data/silver/department_grid_ids/{dept}.csv``
    files (see ``docs/CITY_GRID_IDS.md`` for how those are generated)."""
    dept_dir = silver_dir / "department_grid_ids"
    ids = []
    for name in departments:
        path = dept_dir / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"Department grid-id file not found: {path}. Generate it first with the "
                "spatial-join snippet in docs/CITY_GRID_IDS.md (requires grid_index.parquet, "
                "e.g. from `python -m pipeline.silver --skip-daily`)."
            )
        ids.append(pd.read_csv(path)["ID"].to_numpy())
    return np.unique(np.concatenate(ids))


def extract_daily_var(
    nc_path: Path,
    var: str,
    grid: pd.DataFrame,
    out_dir: Path,
    *,
    overwrite: bool,
    select_ids: np.ndarray | None = None,
) -> list[Path]:
    """One ``{var}_daily_{year}_{month:02d}.parquet`` per calendar month found in
    ``nc_path``. This is a full-country grid (~2.8M cells): chunking by month
    (rather than materializing a whole year at once) keeps peak memory bounded,
    matching the convention used by ``HPC_code/nc_to_point_parquet.py``.

    ``select_ids``, when given, restricts the *output* to those grid IDs (e.g.
    a department's cells) — the raster is still read at full national extent
    per month chunk (its on-disk layout doesn't allow a cheaper spatial read),
    but the rows written to parquet only cover the selected cells, which is
    where the real cost (row count, disk, downstream gold processing) lives.
    """
    written: list[Path] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    ids_full = grid["ID"].to_numpy()
    n_cells_full = len(ids_full)
    if select_ids is not None:
        mask = np.isin(ids_full, select_ids)
        ids = ids_full[mask]
    else:
        mask = None
        ids = ids_full
    n_cells = len(ids)
    with xr.open_dataset(nc_path) as ds:
        da = ds[var].transpose("time", "latitude", "longitude")
        times = pd.DatetimeIndex(da["time"].values)
        months = pd.DataFrame({"pos": np.arange(len(times)), "y": times.year, "m": times.month})
        for (year, month), group in months.groupby(["y", "m"], sort=True):
            out_path = out_dir / f"{var}_daily_{year}_{month:02d}.parquet"
            if out_path.exists() and not overwrite:
                print(f"[silver] {out_path.relative_to(out_dir.parent)} exists, skip")
                written.append(out_path)
                continue
            pos = group["pos"].to_numpy()
            vals = da.isel(time=pos).values.reshape(len(pos), n_cells_full)
            if mask is not None:
                vals = vals[:, mask]
            dates = times[pos]
            df = pd.DataFrame(
                {
                    "ID": np.tile(ids, len(pos)),
                    "date": np.repeat(dates.values, n_cells),
                    "doy": np.repeat(dates.dayofyear.to_numpy(), n_cells),
                    "value": vals.reshape(-1).astype(np.float32),
                }
            )
            df.to_parquet(out_path, index=False)
            print(f"[silver] wrote {out_path.relative_to(out_dir.parent)} ({len(df)} rows)")
            written.append(out_path)
    return written


def run(
    bronze_dir: Path,
    silver_dir: Path,
    *,
    overwrite: bool = False,
    departments: list[str] | None = None,
    skip_daily: bool = False,
) -> None:
    if not bronze_dir.exists():
        raise FileNotFoundError(f"Bronze dir not found: {bronze_dir}")
    silver_dir.mkdir(parents=True, exist_ok=True)

    cov_dir = bronze_dir / "spatial_covariables"
    static_files = {
        name: cov_dir / f"{name}.nc"
        for name in ("DEM", "TDI", "X", "Y")
        if (cov_dir / f"{name}.nc").exists()
    }
    if not static_files:
        raise FileNotFoundError(f"No spatial covariate .nc files found under {cov_dir}")

    grid_index_path = silver_dir / "grid_index.parquet"
    grid = build_grid_index(next(iter(static_files.values())))
    if overwrite or not grid_index_path.exists():
        grid.to_parquet(grid_index_path, index=False)
        print(f"[silver] wrote grid_index.parquet ({len(grid)} cells)")

    static_path = silver_dir / "static_covariates.parquet"
    if overwrite or not static_path.exists():
        static_df = extract_static_covariates(static_files, grid)
        static_df.to_parquet(static_path, index=False)
        print(f"[silver] wrote static_covariates.parquet ({len(static_df)} rows)")
    else:
        print("[silver] static_covariates.parquet exists, skip")

    lst_day, lst_night = cov_dir / "LST_DAY.nc", cov_dir / "LST_NIGHT.nc"
    lst_path = silver_dir / "lst_normals.parquet"
    if lst_day.exists() and lst_night.exists():
        if overwrite or not lst_path.exists():
            lst_df = extract_lst_normals(lst_day, lst_night, grid)
            lst_df.to_parquet(lst_path, index=False)
            print(f"[silver] wrote lst_normals.parquet ({len(lst_df)} rows)")
        else:
            print("[silver] lst_normals.parquet exists, skip")
    else:
        print("[silver] LST_DAY.nc/LST_NIGHT.nc not found, skipping LST normals")

    if skip_daily:
        print("[silver] --skip-daily: not touching tmin/tmax/td")
        return

    select_ids = None
    if departments:
        select_ids = load_department_ids(silver_dir, departments)
        print(f"[silver] department filter ({', '.join(departments)}): {len(select_ids)} cells")

    for nc_path in sorted(bronze_dir.glob("*_daily_*.nc")):
        m = DAILY_VAR_RE.match(nc_path.name)
        if not m:
            continue
        var = m.group("var")
        extract_daily_var(nc_path, var, grid, silver_dir / var, overwrite=overwrite, select_ids=select_ids)

    for sub in sorted(bronze_dir.iterdir()):
        if not sub.is_dir():
            continue
        m = MONTHLY_DIR_RE.match(sub.name)
        if not m:
            continue
        var = m.group("var")
        for nc_path in sorted(sub.glob(f"{var}_daily_*.nc")):
            extract_daily_var(nc_path, var, grid, silver_dir / var, overwrite=overwrite, select_ids=select_ids)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Silver layer: conform raw .nc rasters into tidy per-ID parquet tables.")
    p.add_argument("--bronze-dir", type=Path, default=DEFAULT_BRONZE_DIR)
    p.add_argument("--silver-dir", type=Path, default=DEFAULT_SILVER_DIR)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument(
        "--departments",
        type=str,
        default=None,
        help=(
            "Comma-separated department slugs (matching "
            "Data/silver/department_grid_ids/{slug}.csv) to filter the tmin/tmax/td "
            "extraction to. Default: no filter (full country, current behavior)."
        ),
    )
    p.add_argument(
        "--skip-daily",
        action="store_true",
        help="Skip the tmin/tmax/td extraction loops; only write grid_index/static/lst.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    departments = [d.strip() for d in args.departments.split(",") if d.strip()] if args.departments else None
    run(
        args.bronze_dir,
        args.silver_dir,
        overwrite=args.overwrite,
        departments=departments,
        skip_daily=args.skip_daily,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
