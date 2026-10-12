"""PLAN_1 criterio 11: las cifras del run con fuga no quedan como cifra vigente en
la documentacion del benchmark. Un parrafo que las cite debe decir que son con fuga."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = (
    ROOT / "reports/timesfm_benchmark/README.md",
    ROOT / "reports/timesfm_benchmark/TRACEABILITY.md",
    ROOT / "reports/timesfm_benchmark/limitaciones.md",
    ROOT / "experiments/timesfm/README.md",
)
STALE = (r"1,219\b", r"1,2194", r"24\.896\.901", r"\b38\s+zonas", r"0,0658", r"1\.219\b",
         r"0,0883", r"1,2619", r"16\.908", r"0,8432", r"0,2057")


@pytest.mark.parametrize("path", DOCS, ids=lambda p: p.name)
def test_leaky_figures_only_appear_in_paragraphs_that_say_they_are_leaky(path):
    paragraphs = re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))
    offenders = [
        p.strip().splitlines()[0][:90]
        for p in paragraphs
        if any(re.search(token, p) for token in STALE) and "fuga" not in p
    ]
    assert not offenders, offenders


def test_readme_leads_with_the_clean_reference_and_keeps_the_leaky_one_labeled():
    text = (ROOT / "reports/timesfm_benchmark/README.md").read_text(encoding="utf-8")
    assert "17.027 celdas" in text and "1,2279" in text
    assert "#### Referencia: run con fuga" in text
    assert text.count("usa la selección de recetas con fuga") == 2     # departamental y escala


def test_traceability_cites_the_addendum_in_section_1():
    text = (ROOT / "reports/timesfm_benchmark/TRACEABILITY.md").read_text(encoding="utf-8")
    section_1 = text.split("## 2.")[0]
    assert "timesfm_manifest_addendum_2026-10-02.yaml" in section_1
