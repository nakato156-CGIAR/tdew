"""Proveniencia de los CSV de E5/E8: un registro por (split, metodo), con el
addendum de manifiesto limpio y el panel nacional limpio."""

from __future__ import annotations

import json

import pytest

from experiments.timesfm.by_tier_month import (
    METHOD_COLS,
    provenance_targets,
    build_provenance,
    method_provenance_name,
)
from experiments.timesfm.evaluate import MANIFEST_REF_LIMPIO

OUT = ("reports/timesfm_benchmark/nacional_limpio/tiers_limpio.csv",)


def _build(method, split="ll4"):
    return build_provenance(
        method, split=split, cells=17027, bead_id="tdew-0bt",
        panel_id="nacional_17027_limpio",
        panel_file="reports/timesfm_benchmark/panels/nacional_17027.csv",
        output_files=OUT, notes="test",
    )


def test_method_provenance_names_cover_every_method():
    names = {method_provenance_name(m) for m in METHOD_COLS}
    assert names == {"timesfm:tmin_anom_full", "tuned", "climatology", "td_eq_tmin", "zone_ols"}


def test_timesfm_record_structure():
    r = _build("timesfm")
    assert r.model_family == "timesfm-3.0"
    assert r.variant_label == "tmin_anom_full"
    assert r.trained is False
    assert r.test_period == ("2013-01-01", "2016-12-31")
    assert r.panel_id == "nacional_17027_limpio"
    assert r.panel_cell_count == 17027
    assert r.manifest_ref == MANIFEST_REF_LIMPIO
    assert r.output_files == OUT


@pytest.mark.parametrize("method", ["tuned", "climatology", "tmin", "zone_ols"])
def test_rival_records_use_clean_manifest(method):
    r = _build(method, split="ll1")
    assert r.manifest_ref == MANIFEST_REF_LIMPIO
    assert r.test_period == ("2016-01-01", "2016-12-31")
    json.dumps(r.to_json_dict())  # serializable


def test_tuned_is_trained_on_clean_period():
    r = _build("tuned")
    assert r.trained is True
    assert r.training_period == ("1981-01-01", "2012-12-31")


_FILES = {
    "tiers": "d/tiers_limpio.csv",
    "mensual": "d/sesgo_mensual_limpio.csv",
    "mes_tier": "d/sesgo_mes_tier_limpio.csv",
    "texto": "d/tiers_texto_limpio.csv",
}


def test_texto_csv_only_in_ll4_and_reduced_methods():
    targets = provenance_targets(["ll1", "ll2", "ll4"], _FILES)
    assert len(targets) == 3 * len(METHOD_COLS)
    for split, method, files in targets:
        in_texto = _FILES["texto"] in files
        assert in_texto == (split == "ll4" and method in {"timesfm", "tuned", "climatology"})
        assert {_FILES["tiers"], _FILES["mensual"], _FILES["mes_tier"]} <= set(files)


def test_timesfm_ll4_is_written_last_so_sidecars_describe_it():
    targets = provenance_targets(["ll1", "ll2", "ll4"], _FILES)
    assert (targets[-1][0], targets[-1][1]) == ("ll4", "timesfm")
    assert len({(s, m) for s, m, _ in targets}) == len(targets)


def test_cribado_has_no_texto_file():
    files = {k: v for k, v in _FILES.items() if k != "texto"}
    targets = provenance_targets(["ll4"], files)
    assert all(_FILES["texto"] not in f for _, _, f in targets)
