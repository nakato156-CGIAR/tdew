"""E5 y E8 en el artefacto interactivo: los datos salen de los CSV *_limpio de
PLAN_2, la paridad los protege y la pagina los muestra con las mismas cifras."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import pytest

from experiments.timesfm import artifact_data

REAL = Path(__file__).resolve().parents[1] / "reports/timesfm_benchmark"
HTML = REAL / "artifact/index.html"
DATOS = REAL / "artifact/datos.js"
TIERS = ["within", "near", "marginal", "extrapolated", "unsupported"]


def _datos() -> dict:
    text = DATOS.read_text(encoding="utf-8")
    return json.loads(text[len("window.DATOS = "):].rstrip().rstrip(";"))


# ----------------------------------------------------------- datos (builder)

def test_tables_carry_every_tier_and_monthly_row_from_the_clean_csvs():
    t = artifact_data.tables(REAL)
    tiers = pd.read_csv(REAL / "nacional_limpio/tiers_limpio.csv")
    monthly = pd.read_csv(REAL / "nacional_limpio/sesgo_mensual_limpio.csv")
    assert len(t["soporte"]) == len(tiers) == 75
    assert len(t["sesgoMensual"]) == len(monthly) == 180
    for row in t["soporte"]:
        src = tiers[(tiers.split == row["split"]) & (tiers.tier == row["tier"])
                    & (tiers.method == row["method"])].iloc[0]
        for k in ("cells", "n", "rmse", "mae", "bias", "r", "skill"):
            assert row[k] == pytest.approx(src[k], abs=6e-5), (row["tier"], row["method"], k)
    for row in t["sesgoMensual"]:
        src = monthly[(monthly.split == row["split"]) & (monthly.method == row["method"])
                      & (monthly.month == row["month"])].iloc[0]
        assert row["bias_pooled"] == pytest.approx(src["bias_pooled"], abs=6e-5)
        if row["split"] == "ll4":
            assert row["cell_bias_std"] == pytest.approx(src["cell_bias_std"], abs=6e-5)
        else:
            assert row["cell_bias_std"] is None  # sin dispersion fuera de ll4: null, no NaN


def test_serialized_payload_is_strict_json_for_the_new_tables():
    t = artifact_data.tables(REAL)
    json.dumps({"soporte": t["soporte"], "sesgoMensual": t["sesgoMensual"]}, allow_nan=False)


def test_tier_and_month_tables_come_from_nacional_limpio_only(tmp_path):
    report = tmp_path / "report"
    shutil.copytree(REAL, report, ignore=shutil.ignore_patterns("artifact", "figs", "geo"))
    (report / "nacional_limpio/tiers_limpio.csv").write_text(
        "split,tier,method,cells,n,rmse,mae,bias,r,clim_rmse,skill\nll4,within,timesfm,1,1,9.0,9.0,9.0,0.5,9.0,0.0\n")
    t = artifact_data.tables(report)
    assert len(t["soporte"]) == 1 and t["soporte"][0]["rmse"] == 9.0


# -------------------------------------------------------------------- paridad

def _payload():
    return {"tablas": artifact_data.tables(REAL)}


def _row(payload, key, **match):
    return next(r for r in payload["tablas"][key] if all(r[k] == v for k, v in match.items()))


def test_parity_accepts_the_published_tier_and_month_tables():
    artifact_data.check_parity(_payload(), REAL)


@pytest.mark.parametrize("tamper", [
    lambda p: _row(p, "soporte", split="ll4", tier="within", method="tuned").update(rmse=0.95),
    lambda p: _row(p, "soporte", split="ll4", tier="unsupported", method="timesfm").update(rmse=1.60),
    lambda p: _row(p, "soporte", split="ll4", tier="near", method="timesfm").update(cells=1778),
    lambda p: _row(p, "sesgoMensual", split="ll4", method="tuned", month=12).update(bias_pooled=0.2),
    lambda p: _row(p, "sesgoMensual", split="ll4", method="timesfm", month=1).update(bias_pooled=-0.2),
    lambda p: p["tablas"]["soporte"].pop(),
    lambda p: p["tablas"]["sesgoMensual"].pop(),
])
def test_parity_detects_tampering_of_tier_and_month_tables(tamper):
    payload = _payload()
    tamper(payload)
    with pytest.raises(ValueError):
        artifact_data.check_parity(payload, REAL)


def test_parity_fails_when_the_new_tables_are_missing():
    payload = _payload()
    del payload["tablas"]["soporte"]
    with pytest.raises((ValueError, KeyError)):
        artifact_data.check_parity(payload, REAL)


# ----------------------------------------------------------------------- HTML

def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def test_html_has_the_two_new_sections_and_nav_links():
    html = _html()
    for sid in ("soporte", "sesgo-mensual"):
        assert f'<section id="{sid}">' in html, sid
        assert f'href="#{sid}"' in html, sid
    assert html.index('id="horizonte"') < html.index('id="soporte"') < html.index('id="sesgo-mensual"') < html.index('id="alcance"')


def test_section_numbers_are_consecutive_and_unique():
    nums = re.findall(r'section-index">(\d\d) · ', _html())
    assert nums == [f"{i:02d}" for i in range(1, len(nums) + 1)]
    # se sumaron campo 2017-2020 y divergencia KL (tdew-214.13) y amenazas A1-A4 (tdew-03g)
    assert len(nums) == 11


def _exact_tier_gaps() -> dict[str, float]:
    t = pd.read_csv(REAL / "nacional_limpio/tiers_limpio.csv").query("split == 'll4'")
    w = t.pivot(index="tier", columns="method", values="rmse")
    return (w["tuned"] - w["timesfm"]).to_dict()


def test_static_figures_in_the_new_sections_match_the_csvs():
    """Las cifras escritas a mano en el texto salen del CSV exacto, no de valores ya
    redondeados: la brecha de within es 0.07947, que se escribe 0.079."""
    html = _html()
    gaps = _exact_tier_gaps()
    m = pd.read_csv(REAL / "nacional_limpio/sesgo_mensual_limpio.csv").query("split == 'll4'")
    bias = {(r.method, r.month): r.bias_pooled for r in m.itertuples()}
    section = html[html.index('<section id="soporte">'): html.index('<section id="alcance">')]
    for value in (f"{gaps['within']:.3f}", f"{gaps['unsupported']:.3f}",
                  f"{abs(bias[('tuned', 12)]):.3f}", f"{abs(bias[('tuned', 1)]):.3f}",
                  f"{abs(bias[('timesfm', 1)]):.3f}"):
        assert value in section, value
    assert "17 027" in section


def test_datos_js_keeps_enough_precision_for_derived_differences():
    """El navegador resta RMSE ya volcados: con 4 decimales 0.9464 − 0.8669 daria 0.0795
    y se mostraria 0.080 en vez de 0.079."""
    d = _datos()["tablas"]["soporte"]
    rows = {(r["tier"], r["method"]): r["rmse"] for r in d if r["split"] == "ll4"}
    for tier, exact in _exact_tier_gaps().items():
        assert abs((rows[(tier, "tuned")] - rows[(tier, "timesfm")]) - exact) < 5e-6, tier


def test_new_sections_do_not_use_leaky_or_stale_numbers():
    section = _html()
    for stale in ("0.066", "17 041", "1.219"):
        assert stale not in section[section.index('<section id="soporte">'): section.index('<section id="alcance">')]


# ----------------------------------------------------- render real en Chrome

CHROME = shutil.which("google-chrome") or shutil.which("chromium")


@pytest.mark.skipif(CHROME is None, reason="sin Chrome")
def test_page_renders_tables_and_charts_in_a_real_browser():
    out = subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--virtual-time-budget=15000",
         "--dump-dom", HTML.as_uri()],
        capture_output=True, text=True, timeout=120,
    ).stdout
    tier_rows = re.search(r'<table id="t-soporte">(.*?)</table>', out, re.S)
    assert tier_rows and len(re.findall(r"<tr", tier_rows.group(1))) == 1 + 5  # cabecera + 5 tiers
    month_rows = re.search(r'<table id="t-sesgo-mensual">(.*?)</table>', out, re.S)
    assert month_rows and len(re.findall(r"<tr", month_rows.group(1))) == 1 + 12
    fig = re.search(r'<svg id="fig-sesgo-mensual"[^>]*>(.*?)</svg>', out, re.S)
    assert fig and len(re.findall(r"<rect", fig.group(1))) >= 24  # 12 meses x 2 metodos
    # la tabla que dibuja el navegador muestra el mismo DeltaRMSE que el CSV exacto
    gaps = _exact_tier_gaps()
    shown = {}
    for tier in TIERS:
        row = re.search(rf"<tr><td>{tier}</td>(.*?)</tr>", tier_rows.group(1), re.S)
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row.group(1))
        shown[tier] = cells[3]  # tras Celdas, RMSE TimesFM y RMSE Palacios: DeltaRMSE
    assert shown == {t: f"{gaps[t]:.3f}" for t in TIERS}
    soporte = re.search(r'<svg id="fig-soporte"[^>]*>(.*?)</svg>', out, re.S)
    assert soporte and len(re.findall(r"<circle", soporte.group(1))) >= 10


@pytest.mark.skipif(CHROME is None, reason="sin Chrome")
def test_every_table_cell_in_the_browser_matches_the_csvs():
    out = subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--virtual-time-budget=15000",
         "--dump-dom", HTML.as_uri()],
        capture_output=True, text=True, timeout=120,
    ).stdout

    def body_rows(table_id):
        table = re.search(rf'<table id="{table_id}">(.*?)</table>', out, re.S).group(1)
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S)[1:]
        return [[re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
                for r in rows]

    def signed(v):
        return ("+" if v >= 0 else "-") + f"{abs(v):.3f}"

    def miles(n):
        return f"{int(n):,}".replace(",", " ")

    t = pd.read_csv(REAL / "nacional_limpio/tiers_limpio.csv").query("split == 'll4'")
    by = {(r.tier, r.method): r for r in t.itertuples()}
    expected = []
    for tier in TIERS:
        a, b = by[(tier, "timesfm")], by[(tier, "tuned")]
        expected.append([tier, miles(a.cells), f"{a.rmse:.3f}", f"{b.rmse:.3f}", f"{b.rmse - a.rmse:.3f}",
                         signed(a.bias), signed(b.bias), f"{a.skill:.3f}", f"{b.skill:.3f}"])
    assert body_rows("t-soporte") == expected

    m = pd.read_csv(REAL / "nacional_limpio/sesgo_mensual_limpio.csv").query("split == 'll4'")
    mb = {(r.method, r.month): r for r in m.itertuples()}
    names = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    expected = [[names[k - 1], signed(mb[("timesfm", k)].bias_pooled), signed(mb[("tuned", k)].bias_pooled),
                 f"{mb[('timesfm', k)].cell_bias_std:.3f}", f"{mb[('tuned', k)].cell_bias_std:.3f}"]
                for k in range(1, 13)]
    assert body_rows("t-sesgo-mensual") == expected
