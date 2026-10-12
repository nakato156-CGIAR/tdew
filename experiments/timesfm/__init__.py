"""Benchmark de TimesFM 3 contra el metodo de Palacios y la TCN (bead tdew-214)."""

from .panel import SPLITS, PanelBatch, SplitSpec, iter_panel_batches, split_spec

__all__ = ["SPLITS", "PanelBatch", "SplitSpec", "iter_panel_batches", "split_spec"]
