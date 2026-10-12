"""Resolucion del nombre de metodo para proveniencia en HPC_code_tunning/
effect_sizes.py: cada fila de effect_sizes.csv es una comparacion
focal-vs-baseline, asi que la proveniencia se registra para el metodo focal."""

from __future__ import annotations

from HPC_code_tunning.effect_sizes import build_row_provenance, focal_provenance_method_name


def test_non_timesfm_focal_passes_through_unchanged():
    for focal in ("climatology", "td_eq_tmin", "zone_ols", "tuned"):
        assert focal_provenance_method_name(focal, None) == focal
        assert focal_provenance_method_name(focal, "tmin_anom_full") == focal


def test_timesfm_focal_without_variant_is_unresolvable():
    assert focal_provenance_method_name("timesfm", None) is None


def test_timesfm_focal_with_variant_is_qualified():
    assert focal_provenance_method_name("timesfm", "tmin_anom_full") == "timesfm:tmin_anom_full"


def test_resolved_timesfm_method_is_reachable_through_build_row_provenance():
    method = focal_provenance_method_name("timesfm", "tmin_anom_full")
    record = build_row_provenance(
        method, split="ll4", cells=17041, bead_id="tdew-214",
        panel_id="backtest", panel_file=None, output_files=("effect_sizes.csv",),
    )
    assert record.variant_label == "tmin_anom_full"


def test_tuned_focal_is_reachable_and_uses_anomaly_target():
    method = focal_provenance_method_name("tuned", None)
    record = build_row_provenance(
        method, split="ll1", cells=17041, bead_id="tdew-214",
        panel_id="backtest", panel_file=None, output_files=("effect_sizes.csv",),
    )
    assert record.target_type == "td_anomaly"
    assert record.climatology_used is True
