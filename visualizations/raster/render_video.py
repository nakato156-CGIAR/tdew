"""
visualizations.render_video

Build an mp4 that sweeps through every day of a (variable, year) found in
``Data/silver``, one frame per day, on a fixed color scale so the video
reads correctly frame-to-frame. Cached to disk under ``Data/gold/renders``
(a deterministic render of silver data counts as a gold-layer product here)
— re-running with the same (var, year) is a no-op unless ``overwrite=True``.

Uses ``imageio-ffmpeg`` as the mp4 backend so this doesn't depend on a
system ffmpeg install (relevant on Windows).
"""

from __future__ import annotations

from pathlib import Path

import imageio
import numpy as np

from visualizations.raster.data_access import DEFAULT_SILVER_DIR, iter_year_days, year_value_range
from visualizations.raster.plotting import draw_raster

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RENDERS_DIR = REPO_ROOT / "Data" / "gold" / "renders"
FPS = 12


def _frame_to_rgb(raster: np.ndarray, date, vmin: float, vmax: float, var: str) -> np.ndarray:
    fig = draw_raster(raster, f"{var.upper()} — {date.date()}", var.upper(), vmin=vmin, vmax=vmax)
    fig.canvas.draw()
    return np.asarray(fig.canvas.buffer_rgba())[:, :, :3]


def render_path(var: str, year: int, renders_dir: Path = DEFAULT_RENDERS_DIR) -> Path:
    return renders_dir / f"{var}_{year}.mp4"


def build_year_video(
    var: str,
    year: int,
    *,
    silver_dir: Path = DEFAULT_SILVER_DIR,
    renders_dir: Path = DEFAULT_RENDERS_DIR,
    overwrite: bool = False,
) -> Path:
    out_path = render_path(var, year, renders_dir)
    if out_path.exists() and not overwrite:
        return out_path

    vmin, vmax = year_value_range(var, year, silver_dir)
    renders_dir.mkdir(parents=True, exist_ok=True)

    with imageio.get_writer(out_path, fps=FPS, codec="libx264", macro_block_size=None) as writer:
        for date, raster in iter_year_days(var, year, silver_dir):
            writer.append_data(_frame_to_rgb(raster, date, vmin, vmax, var))

    return out_path
