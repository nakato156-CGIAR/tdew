"""Shared matplotlib rendering for a single raster frame, used by the
Streamlit app (visualizations.raster.app) and the video builder
(visualizations.raster.render_video)."""

from __future__ import annotations

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def draw_raster(raster: np.ndarray, title: str, label: str, *, vmin: float | None = None, vmax: float | None = None) -> Figure:
    fig = Figure(figsize=(6, 8))
    FigureCanvasAgg(fig)
    ax = fig.subplots()
    im = ax.imshow(raster, cmap="viridis", vmin=vmin, vmax=vmax)
    ax.set_title(title)
    ax.axis("off")
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02, label=label)
    fig.tight_layout()
    return fig
