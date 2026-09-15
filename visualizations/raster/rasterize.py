"""
visualizations.rasterize

Reshape a (ID, value) table into a 2D raster matching the national PISCO
grid. ``ID`` is a row-major index over ``(latitude, longitude)`` (see
``pipeline/silver.py::_grid_index``) with **latitude descending** (north to
south) — the same convention as a north-up image — so a plain reshape lines
up directly with ``imshow``'s default ``origin="upper"``, no flips needed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def to_grid(df: pd.DataFrame, value_col: str, n_lat: int, n_lon: int, all_ids: np.ndarray) -> np.ndarray:
    """``df`` has (at least) ``ID`` and ``value_col``. Cells missing from
    ``df`` (e.g. a variable not covering every land cell) come back as NaN.
    ``all_ids`` must be the full, ID-sorted id array of the grid (length
    ``n_lat * n_lon``)."""
    values = pd.Series(np.nan, index=all_ids, dtype="float32")
    values.loc[df["ID"].to_numpy()] = df[value_col].to_numpy(dtype="float32")
    return values.to_numpy().reshape(n_lat, n_lon)
