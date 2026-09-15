"""
visualizations.data_access

Read-only accessors the Streamlit app uses to pull rasters straight out of
``Data/silver`` — this is a "silver view": no new gold table is materialized
for viz. ``doy`` is already a column on every silver daily row, and a given
(var, doy) touches at most one row per cell per year, so both the single-day
map and the multi-year climatology mean are cheap enough to compute on
demand with row-group-pruned parquet reads (a full ~450MB monthly file
prunes down to ~1s per query — see ``load_day``/``load_climatology_day``),
cached per-request with ``st.cache_data``.

An earlier version of this precomputed climatology as a batch gold table
(bucketed by ID, like ``pipeline.gold``'s ``model_input``). That table turned
out to be roughly as large as a full year of raw daily data (2.8M cells x
366 days) and the ID-bucketed reshuffle needed to build it without OOMing
took hours on a laptop for even a single variable/year — no better than
just reading silver directly per query. Dropped in favor of the on-demand
approach here.
"""

from __future__ import annotations

import re
import warnings
from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.dataset as pads
import streamlit as st

from visualizations.raster.rasterize import to_grid

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SILVER_DIR = REPO_ROOT / "Data" / "silver"

DAILY_FILE_RE = re.compile(r"^(?P<var>[a-zA-Z0-9]+)_daily_(?P<year>\d{4})_(?P<month>\d{2})\.parquet$")


def list_variables(silver_dir: Path = DEFAULT_SILVER_DIR) -> list[str]:
    """Every ``{var}`` with at least one ``{var}_daily_*.parquet`` under
    ``Data/silver/{var}/``."""
    if not silver_dir.exists():
        return []
    variables = []
    for sub in sorted(silver_dir.iterdir()):
        if sub.is_dir() and any(sub.glob(f"{sub.name}_daily_*.parquet")):
            variables.append(sub.name)
    return variables


def list_years(var: str, silver_dir: Path = DEFAULT_SILVER_DIR) -> list[int]:
    years = set()
    for f in (silver_dir / var).glob(f"{var}_daily_*.parquet"):
        m = DAILY_FILE_RE.match(f.name)
        if m:
            years.add(int(m.group("year")))
    return sorted(years)


@st.cache_data(show_spinner=False)
def load_grid(silver_dir: Path = DEFAULT_SILVER_DIR) -> tuple[pd.DataFrame, int, int, np.ndarray]:
    """(grid_index, n_lat, n_lon, all_ids). ``all_ids`` is ID-sorted, i.e.
    ready to align with a ``reshape(n_lat, n_lon)`` in row-major order."""
    grid = pd.read_parquet(silver_dir / "grid_index.parquet").sort_values("ID")
    n_lat = grid["latitude"].nunique()
    n_lon = grid["longitude"].nunique()
    return grid, n_lat, n_lon, grid["ID"].to_numpy()


def _month_path(var: str, year: int, month: int, silver_dir: Path) -> Path:
    return silver_dir / var / f"{var}_daily_{year}_{month:02d}.parquet"


def load_day(var: str, date: pd.Timestamp, silver_dir: Path = DEFAULT_SILVER_DIR) -> np.ndarray | None:
    """Raster for a single day, or ``None`` if that month's silver table
    doesn't exist. Filters at the parquet-dataset level (row-group pruning
    on ``date``) instead of loading the whole ~450MB monthly file, so this
    stays fast enough for an interactive date slider."""
    path = _month_path(var, date.year, date.month, silver_dir)
    if not path.exists():
        return None
    _, n_lat, n_lon, all_ids = load_grid(silver_dir)
    table = pads.dataset(path).to_table(columns=["ID", "value"], filter=(pads.field("date") == date))
    day_df = table.to_pandas()
    return to_grid(day_df, "value", n_lat, n_lon, all_ids)


def iter_year_days(var: str, year: int, silver_dir: Path = DEFAULT_SILVER_DIR) -> Iterator[tuple[pd.Timestamp, np.ndarray]]:
    """Yield ``(date, raster)`` for every day of ``year`` found in silver, one
    calendar month at a time so a full year is never held in memory at once."""
    _, n_lat, n_lon, all_ids = load_grid(silver_dir)
    for month in range(1, 13):
        path = _month_path(var, year, month, silver_dir)
        if not path.exists():
            continue
        df = pd.read_parquet(path, columns=["ID", "date", "value"])
        for date, day_df in df.groupby("date", sort=True):
            yield pd.Timestamp(date), to_grid(day_df, "value", n_lat, n_lon, all_ids)


def year_value_range(var: str, year: int, silver_dir: Path = DEFAULT_SILVER_DIR) -> tuple[float, float]:
    """Cheap global (min, max) over every month of ``year``, for a fixed
    color scale across video frames."""
    lo, hi = np.inf, -np.inf
    for month in range(1, 13):
        path = _month_path(var, year, month, silver_dir)
        if not path.exists():
            continue
        col = pd.read_parquet(path, columns=["value"])["value"]
        lo = min(lo, float(col.min()))
        hi = max(hi, float(col.max()))
    return lo, hi


def _date_for_doy(year: int, doy: int) -> pd.Timestamp:
    return pd.Timestamp(year=year, month=1, day=1) + pd.Timedelta(days=doy - 1)


@st.cache_data(show_spinner=False)
def load_climatology_day(var: str, doy: int, silver_dir: Path = DEFAULT_SILVER_DIR) -> np.ndarray | None:
    """Mean raster for a given day-of-year, averaged across every year found
    in silver for ``var``. One row-group-pruned read per year (no
    precomputed gold table — see module docstring)."""
    years = list_years(var, silver_dir)
    if not years:
        return None
    _, n_lat, n_lon, all_ids = load_grid(silver_dir)
    rasters = []
    for year in years:
        date = _date_for_doy(year, doy)
        if date.year != year:  # doy 366 in a non-leap year
            continue
        path = _month_path(var, year, date.month, silver_dir)
        if not path.exists():
            continue
        table = pads.dataset(path).to_table(columns=["ID", "value"], filter=(pads.field("doy") == doy))
        rasters.append(to_grid(table.to_pandas(), "value", n_lat, n_lon, all_ids))
    if not rasters:
        return None
    with warnings.catch_warnings():
        # every cell outside the PISCO land mask is NaN in every year — an
        # expected all-NaN slice, not something to warn about.
        warnings.filterwarnings("ignore", message="Mean of empty slice")
        return np.nanmean(np.stack(rasters), axis=0)
