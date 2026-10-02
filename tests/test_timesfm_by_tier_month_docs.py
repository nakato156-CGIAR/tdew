"""Las cifras que el README cita de E5 y E8 deben coincidir con los CSV
publicados: una cifra copiada a mano que se desvie hace fallar esta prueba."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "reports" / "timesfm_benchmark"
README = BENCH / "README.md"
TIERS_CSV = BENCH / "nacional_limpio" / "tiers_limpio.csv"
MONTHLY_CSV = BENCH / "nacional_limpio" / "sesgo_mensual_limpio.csv"
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
          "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _num(cell: str) -> float:
    cell = cell.strip().replace("−", "-").replace("+", "")
    if "," in cell:
        return float(cell.replace(",", "."))
    return float(cell.replace(".", ""))


def _section(name: str) -> str:
    text = README.read_text(encoding="utf-8")
    start = text.index(f"### {name}")
    nxt = text.find("\n### ", start + 1)
    return text[start: nxt if nxt != -1 else None]


def _rows(section: str, first_cells: list[str]) -> dict[str, list[float]]:
    out = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] in first_cells:
            out[cells[0]] = [_num(c) for c in cells[1:]]
    return out


@pytest.fixture(scope="module")
def tiers():
    return pd.read_csv(TIERS_CSV).query("split == 'll4'")


@pytest.fixture(scope="module")
def monthly():
    return pd.read_csv(MONTHLY_CSV).query("split == 'll4'")


def test_tier_table_in_readme_matches_csv(tiers):
    rows = _rows(_section("Soporte observacional"),
                 ["within", "near", "marginal", "extrapolated", "unsupported"])
    assert len(rows) == 5
    for tier, vals in rows.items():
        t = tiers[tiers["tier"] == tier].set_index("method")
        expected = [
            t.loc["timesfm", "cells"],
            t.loc["timesfm", "rmse"], t.loc["tuned", "rmse"], t.loc["climatology", "rmse"],
            t.loc["timesfm", "bias"], t.loc["tuned", "bias"],
            t.loc["timesfm", "skill"], t.loc["tuned", "skill"],
        ]
        assert vals == pytest.approx(expected, abs=5.1e-4), tier


def test_readme_tier_claims_hold(tiers):
    wide = tiers.pivot(index="tier", columns="method", values="rmse")
    assert (wide["timesfm"] < wide["tuned"]).all()  # «menor RMSE en los cinco tiers»
    gap = (wide["tuned"] - wide["timesfm"])
    assert round(gap["within"], 3) == 0.079 and round(gap["unsupported"], 3) == 0.072


def test_monthly_table_in_readme_matches_csv(monthly):
    rows = _rows(_section("Sesgo mensual"), MONTHS)
    assert len(rows) == 12
    for i, name in enumerate(MONTHS, start=1):
        m = monthly[monthly["month"] == i].set_index("method")
        expected = [m.loc["timesfm", "bias_pooled"], m.loc["tuned", "bias_pooled"],
                    m.loc["timesfm", "cell_bias_std"], m.loc["tuned", "cell_bias_std"]]
        assert rows[name] == pytest.approx(expected, abs=5.1e-4), name


def test_cited_dispersion_range_matches_csv(monthly):
    std = monthly[monthly["method"].isin(["timesfm", "tuned"])]["cell_bias_std"]
    text = _section("Sesgo mensual")
    cited = re.search(r"\(([\d,]+) a ([\d,]+) °C", text)
    assert cited, "el README debe citar el rango de la dispersion entre celdas"
    assert _num(cited.group(1)) == pytest.approx(std.min(), abs=5e-3)
    assert _num(cited.group(2)) == pytest.approx(std.max(), abs=5e-3)


def test_readme_monthly_claims_hold(monthly):
    b = monthly.pivot(index="month", columns="method", values="bias_pooled")
    smaller = [m for m in b.index if abs(b.loc[m, "timesfm"]) < abs(b.loc[m, "tuned"])]
    assert smaller == [1, 10]  # «solo en enero y octubre»
    assert round(b.loc[12, "tuned"], 3) == 0.017
    assert b["tuned"].abs().idxmax() == 1 and round(b["tuned"].abs().max(), 3) == 0.402
    assert round(b["timesfm"].abs().max(), 3) == 0.325
