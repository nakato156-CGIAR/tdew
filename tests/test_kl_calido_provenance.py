"""Proveniencia de kl_calido: un registro que documenta todos los CSV y deja un sidecar por archivo."""
from __future__ import annotations

import json
from pathlib import Path

from experiments.timesfm import kl_calido
from tdew_estimation import provenance as prov


def _build(outputs, limit_ids=None):
    return kl_calido.build_provenance(n_cells=17027, outputs=outputs, bead_id="tdew-214.19",
                                      palacios=Path("pal.parquet"), tfm=Path("tfm.parquet"),
                                      n_boot=200, seed=0, limit_ids=limit_ids)


def test_record_structure():
    outs = [Path(f"reports/timesfm_benchmark/kl_calido/{c}.csv") for c in kl_calido.CUTS]
    r = _build(outs)
    assert r.bead_id == "tdew-214.19"
    assert r.model_family == "timesfm-3.0" and r.variant_label == "tmin_anom_full"
    assert r.test_period == ("2013-01-01", "2016-12-31") and r.split_id == "ll4"
    assert r.panel_id == "nacional_17027_limpio" and r.panel_cell_count == 17027
    assert r.output_files == tuple(str(p) for p in outs)
    assert r.seeds == (0,)
    assert "pred_clim" in r.notes and "200 replicas" in r.notes and "Muestra" not in r.notes
    json.dumps(r.to_json_dict())


def test_sample_runs_are_flagged():
    assert "Muestra de 50 celdas" in _build([Path("x.csv")], limit_ids=50).notes


def test_sidecars_written_for_every_output(tmp_path):
    outs = []
    for name in (*kl_calido.CUTS, "hist_nacional"):
        p = tmp_path / f"{name}.csv"
        p.write_text("a\n1\n")
        outs.append(p)
    registry = tmp_path / "registry.jsonl"
    prov.record_metric_provenance(_build(outs), registry_path=registry, repo_root=tmp_path)
    for p in outs:
        side = json.loads(p.with_name(p.name + ".provenance.json").read_text())
        assert side["bead_id"] == "tdew-214.19" and str(p) in side["output_files"]
    assert len(prov.load_registry(registry)) == 1
