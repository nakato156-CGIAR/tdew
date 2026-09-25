"""Mapeo de nombres de metodo para proveniencia en experiments/timesfm/escala.py
(la pasada de escala nacional, 436.519 celdas)."""

from __future__ import annotations

from experiments.timesfm.escala import _provenance_method_name
from experiments.timesfm.evaluate import build_row_provenance


def test_bare_timesfm_becomes_variant_qualified():
    assert _provenance_method_name("timesfm", "tmin_anom_full") == "timesfm:tmin_anom_full"


def test_rival_names_pass_through_unchanged():
    for method in ("climatology", "tuned"):
        assert _provenance_method_name(method, "tmin_anom_full") == method


def test_mapped_name_is_reachable_through_build_row_provenance():
    method = _provenance_method_name("timesfm", "tmin_anom_full")
    record = build_row_provenance(
        method, split="ll4", cells=436519, bead_id="tdew-214",
        panel_id="ALL_reponderado", panel_file=None, output_files=("escala/leaderboard.csv",),
    )
    assert record.variant_label == "tmin_anom_full"
    assert record.panel_cell_count == 436519
