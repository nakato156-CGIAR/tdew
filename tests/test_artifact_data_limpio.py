"""El artefacto interactivo lee las salidas *_limpio y no conserva cifras con fuga
(PLAN_1 §Paso 7)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd
import pytest

from experiments.timesfm import artifact_data

REAL = Path(__file__).resolve().parents[1] / "reports/timesfm_benchmark"


def _report(tmp_path):
    report = tmp_path / "report"
    for sub in ("nacional_limpio", "cribado_limpio", "nacional", "cribado", "departamental", "escala"):
        (report / sub).mkdir(parents=True)
    for rel in ("nacional_limpio/metrics_by_zone.csv", "nacional_limpio/metrics_all.csv",
                "nacional_limpio/effect_sizes_all.csv", "cribado_limpio/leaderboard.csv",
                "departamental/metrics.csv", "coste_throughput.csv", "escala/leaderboard.csv",
                "curva_error_nacional_limpio.csv"):
        shutil.copy(REAL / rel, report / rel)
    # versiones con fuga: deben ignorarse (contenido sentinela inconfundible)
    (report / "nacional/metrics_by_zone.csv").write_text(
        "split,zone_id,method,cells,rmse,skill_vs_clim\nll4,99,timesfm:x,1,9.0,9.0\n")
    (report / "curva_error_nacional.csv").write_text(
        "split,method,dia,rmse_acumulado\nll4,tuned,1,99.0\n")
    return report


def test_zone_metrics_reads_the_clean_directory(tmp_path):
    zones = artifact_data.zone_metrics(_report(tmp_path))
    assert "99" not in zones
    assert len(zones) == 33


def test_error_curve_reads_the_clean_csv(tmp_path):
    curve = artifact_data.error_curve(_report(tmp_path))
    assert max(curve["tuned"]["rmse"]) < 5, "leyo la curva con fuga sentinela (99.0)"
    assert set(curve) == {"climatology", "td_eq_tmin", "zone_ols", "tuned", "timesfm"}


def test_tables_read_clean_nacional_efectos_and_cribado(tmp_path):
    tables = artifact_data.tables(_report(tmp_path))
    assert {r["n_cells"] for r in tables["efectos"]} == {17027}
    assert {r["cells"] for r in tables["cribado"]} == {1092}
    tuned = [r for r in tables["nacional"] if r["split"] == "ll4" and r["method"] == "tuned"]
    assert tuned[0]["rmse"] == pytest.approx(1.2279, abs=5e-5)


def test_parity_passes_on_the_published_clean_outputs_and_detects_tampering():
    payload = {"tablas": artifact_data.tables(REAL)}
    artifact_data.check_parity(payload, REAL)
    for row in payload["tablas"]["nacional"]:
        if row["split"] == "ll4" and row["method"] == "tuned":
            row["rmse"] = 1.2194            # cifra con fuga
    with pytest.raises(ValueError):
        artifact_data.check_parity(payload, REAL)


def test_html_keeps_no_leaky_figures_as_current_values():
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    for stale in ("1.219", "17 041", "24 896 901", "38/41", "0.066 °C"):
        assert stale not in html, stale


def test_html_tolerates_zones_without_measurements():
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    assert "zonasMedidas" in html and "no tiene celdas en el muestreo" in html


def test_html_static_counts_match_datos_js():
    import json

    data = (REAL / "artifact/datos.js").read_text(encoding="utf-8")
    meta = json.loads(data[len("window.DATOS = "):].rstrip().rstrip(";"))["meta"]
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    total = meta["muestreoDentro"] + meta["muestreoFuera"]
    assert total == 17027
    assert f"{total // 1000} {total % 1000:03d} celdas" in html
    assert f"{meta['muestreoFuera'] // 1000} {meta['muestreoFuera'] % 1000:03d} están fuera" in html
    assert f"{100 * meta['muestreoFuera'] / total:.1f} %" in html


def test_html_warns_next_to_departamental_and_escala_that_tuned_is_not_clean():
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    note = "no es comparable con las cifras limpias"
    assert html.count(note) == 2
    dept = html.index("TimesFM obtiene el menor RMSE en los cuatro.")
    escala = html.index("su corrida sobre toda la rejilla fue eliminada por memoria.")
    assert note in html[dept:dept + 600]
    assert note in html[escala:escala + 600]


def test_html_has_no_38_zonas_even_across_line_breaks():
    import re

    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    assert not re.search(r"\b38\s+zonas", html)
    assert not re.search(r"\b38/41", html)


def test_horizon_narrative_matches_the_clean_error_curve():
    """El texto de la seccion de horizonte cita los dias de cruce de la curva limpia."""
    curve = pd.read_csv(REAL / "curva_error_nacional_limpio.csv")
    wide = curve.pivot(index="dia", columns="method", values="rmse_acumulado")
    gap = wide["timesfm"] - wide["tuned"]          # > 0: Palacios va por delante
    ahead = gap[gap > 0].index
    first, last = int(ahead.min()), int(ahead.max())
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    assert f"hasta el día {first - 1}" in html and f"el día {last}" in html
    assert f"{gap.max():.2f} °C" in html
    assert f"el día {int(gap.idxmax())}" in html
    assert gap.loc[:first - 1].max() < 0 and gap.loc[last + 1:].max() < 0
    assert "En los primeros días Palacios tiene la ventaja" not in html


def test_html_skill_and_bias_and_license_figures_match_clean_data():
    html = (REAL / "artifact/index.html").read_text(encoding="utf-8")
    ma = pd.read_csv(REAL / "nacional_limpio/metrics_all.csv").set_index(["split", "method"])
    assert f"{ma.loc[('ll4', 'timesfm'), 'bias']:+.3f}".replace("-", "−") in html or \
        f"+{ma.loc[('ll4', 'timesfm'), 'bias']:.3f}" in html
    assert "+0.105" not in html
    assert "seis veces el semiancho" not in html
    assert "1 106 celdas" in html           # la cifra de TimesFM 2.5 declara su panel de origen
