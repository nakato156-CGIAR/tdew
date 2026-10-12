"""publish_csv copia un CSV intermedio al repo y le da su propio registro de
proveniencia (PLAN_1 §Pasos 4-5): cada CSV publicado debe tener filas que lo citen."""
from __future__ import annotations

import pytest

from experiments.timesfm.evaluate import build_row_provenance
from experiments.timesfm.publish import publish_csv
from tdew_estimation import provenance as prov


def _record_for(src, registry, repo_root, *, method="tuned", panel_id="nacional_17027_limpio"):
    prov.record_metric_provenance(
        build_row_provenance(
            method, split="ll4", cells=17027, bead_id="tdew-214.12", panel_id=panel_id,
            panel_file="panels/x.csv", output_files=(str(src),), notes="n",
            manifest_ref="addendum",
        ),
        registry_path=registry, repo_root=repo_root,
    )


def test_publish_copies_file_and_clones_each_matching_record(tmp_path):
    src = tmp_path / "work" / "metrics_all.csv"
    src.parent.mkdir()
    src.write_text("a,b\n1,2\n")
    dst = tmp_path / "repo" / "nacional_limpio" / "metrics_all.csv"
    registry = tmp_path / "registry.jsonl"
    _record_for(src, registry, tmp_path)
    _record_for(src, registry, tmp_path, method="timesfm:tmin_anom_full")
    before = len(prov.load_registry(registry))

    n = publish_csv(src, dst, registry_path=registry, repo_root=tmp_path)

    assert n == 2
    assert dst.read_text() == src.read_text()
    rows = prov.load_registry(registry)
    assert len(rows) == before + 2
    new = rows[before:]
    assert all(r["output_files"] == ["repo/nacional_limpio/metrics_all.csv"] for r in new)
    assert {r["panel_id"] for r in new} == {"nacional_17027_limpio"}
    assert all(r["manifest_ref"] == "addendum" and r["notes"].startswith("n; ") for r in new)
    old_ids = {r["run_id"] for r in rows[:before]}
    assert not old_ids & {r["run_id"] for r in new}, "cada clon lleva un run_id nuevo"
    assert (dst.parent / "metrics_all.csv.provenance.json").exists()


def test_publish_does_not_modify_existing_registry_rows(tmp_path):
    src = tmp_path / "m.csv"
    src.write_text("x\n")
    registry = tmp_path / "registry.jsonl"
    _record_for(src, registry, tmp_path)
    original = registry.read_text()
    publish_csv(src, tmp_path / "out" / "m.csv", registry_path=registry, repo_root=tmp_path)
    assert registry.read_text().startswith(original)


def test_publish_refuses_a_file_without_provenance(tmp_path):
    src = tmp_path / "orphan.csv"
    src.write_text("x\n")
    with pytest.raises(ValueError, match="sin registros de proveniencia"):
        publish_csv(src, tmp_path / "out.csv", registry_path=tmp_path / "r.jsonl",
                    repo_root=tmp_path)
    assert not (tmp_path / "out.csv").exists(), "no se publica nada sin proveniencia"


def test_publish_is_idempotent_for_the_same_destination(tmp_path):
    src = tmp_path / "work" / "m.csv"
    src.parent.mkdir()
    src.write_text("x\n")
    dst = tmp_path / "repo" / "m.csv"
    registry = tmp_path / "registry.jsonl"
    _record_for(src, registry, tmp_path)
    assert publish_csv(src, dst, registry_path=registry, repo_root=tmp_path) == 1
    assert publish_csv(src, dst, registry_path=registry, repo_root=tmp_path) == 0
    assert len(prov.load_registry(registry)) == 2


def test_publish_records_repo_relative_path_and_origin_link(tmp_path):
    src = tmp_path / "work" / "m.csv"
    src.parent.mkdir()
    src.write_text("x\n")
    dst = tmp_path / "repo" / "sub" / "m.csv"
    registry = tmp_path / "registry.jsonl"
    _record_for(src, registry, tmp_path)
    origin_run = prov.load_registry(registry)[0]["run_id"]
    publish_csv(src, dst, registry_path=registry, repo_root=tmp_path / "repo")
    clone = prov.load_registry(registry)[-1]
    assert clone["output_files"] == ["sub/m.csv"]
    assert f"source_run_id={origin_run}" in clone["notes"]
    assert f"published_from={src}" in clone["notes"]
    assert clone["notes"].startswith("n")


def test_published_from_is_recorded_as_an_absolute_path_even_for_relative_src(
        tmp_path, monkeypatch):
    work = tmp_path / "work"
    work.mkdir()
    (work / "m.csv").write_text("x\n")
    registry = tmp_path / "registry.jsonl"
    _record_for(work / "m.csv", registry, tmp_path)
    monkeypatch.chdir(work)
    publish_csv(__import__("pathlib").Path("m.csv"), tmp_path / "o" / "m.csv",
                registry_path=registry, repo_root=tmp_path)
    assert f"published_from={work / 'm.csv'}" in prov.load_registry(registry)[-1]["notes"]


def test_publish_finds_rows_recorded_with_another_checkouts_absolute_path(tmp_path):
    src = tmp_path / "repo" / "reports" / "m.csv"
    src.parent.mkdir(parents=True)
    src.write_text("x\n")
    registry = tmp_path / "registry.jsonl"
    record = build_row_provenance(
        "tuned", split="ll4", cells=1, bead_id="b", panel_id="p", panel_file="f",
        output_files=("/other/checkout/reports/m.csv",), manifest_ref="addendum",
    )
    registry.write_text(__import__("json").dumps(record.to_json_dict()) + "\n")
    n = publish_csv(src, tmp_path / "repo" / "reports" / "copy.csv",
                    registry_path=registry, repo_root=tmp_path / "repo")
    assert n == 1
