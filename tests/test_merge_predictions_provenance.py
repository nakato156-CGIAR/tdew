"""Mapeo de nombres de metodo de score_split() al vocabulario de proveniencia
(build_row_provenance espera "timesfm:<variante>", no el "timesfm" bare que
present_methods()/METHOD_COLS usan)."""

from __future__ import annotations

from experiments.timesfm.evaluate import build_row_provenance
from experiments.timesfm.merge_predictions import _provenance_method_name


def test_bare_timesfm_becomes_variant_qualified():
    assert _provenance_method_name("timesfm", "tmin_anom_full") == "timesfm:tmin_anom_full"


def test_rival_method_names_pass_through_unchanged():
    for method in ("climatology", "td_eq_tmin", "zone_ols", "tuned"):
        assert _provenance_method_name(method, "tmin_anom_full") == method


def test_mapped_name_is_reachable_through_build_row_provenance():
    method = _provenance_method_name("timesfm", "tmin_anom_full")
    record = build_row_provenance(
        method, split="ll4", cells=17041, bead_id="tdew-214",
        panel_id="nacional_17041", panel_file="x.csv", output_files=("x.csv",),
    )
    assert record.variant_label == "tmin_anom_full"
