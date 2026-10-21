"""Prueba de datos_amenazas.js (seccion A1-A4 del artefacto TimesFM).

Verifica que el generador escribe las claves esperadas, que cada cifra coincide con su CSV
de origen y que las afirmaciones fijas de los titulos de la seccion siguen siendo ciertas.
"""

import collections
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from experiments.amenazas import artifact_amenazas as aa

REPO = Path(__file__).resolve().parents[1]
RES = REPO / aa.RES
HTML = REPO / "reports/timesfm_benchmark/artifact/index.html"
CLAVES = {"meta", "informacion", "porMetodo", "brechas", "victorias", "escalera", "escaleraBrechas",
          "a4PorAnio", "a4PorPeriodo", "a4Delta", "a3", "porZona", "costo"}


@pytest.fixture(scope="module")
def datos(tmp_path_factory, monkeypatch_module):
    out = tmp_path_factory.mktemp("am") / "datos_amenazas.js"
    aa.build(out, RES)
    text = out.read_text(encoding="utf-8")
    assert text.startswith("window.AMENAZAS = ") and text.rstrip().endswith(";")
    return json.loads(text[len("window.AMENAZAS = "):].rstrip().rstrip(";"))


@pytest.fixture(scope="module")
def monkeypatch_module():
    mp = pytest.MonkeyPatch()
    mp.chdir(REPO)
    yield mp
    mp.undo()


def test_claves(datos):
    assert set(datos) == CLAVES
    assert datos["meta"]["bloques"]["ll4"]["prueba"] == [2013, 2016]
    assert datos["meta"]["bloques"]["ll4b"]["prueba"] == [2009, 2012]
    assert {r["metodo"] for r in datos["informacion"]} == {
        "timesfm_anom", "llr_simple", "llr_rezagos_sel", "tuned", "tuned_sin_td"}


@pytest.mark.parametrize("clave", sorted(aa.FUENTES))
def test_cifras_iguales_al_csv(datos, clave):
    esperado = aa.leer(clave, RES)
    obtenido = pd.DataFrame(datos[clave])
    assert len(obtenido) == len(esperado) > 0
    assert list(obtenido.columns) == list(esperado.columns)
    for c in esperado.columns:
        a, b = esperado[c], obtenido[c]
        if pd.api.types.is_numeric_dtype(a):
            np.testing.assert_allclose(b.astype("f8").to_numpy(), a.astype("f8").to_numpy(),
                                       rtol=0, atol=0, equal_nan=True, err_msg=f"{clave}.{c}")
        else:
            assert (a.astype(str).where(a.notna(), None).tolist()
                    == b.astype(str).where(b.notna(), None).tolist()), f"{clave}.{c}"


def _m(d, s, a, m, p="total"):
    return next(r for r in d["porMetodo"] if r["split"] == s and r["ambito"] == a
                and r["metodo"] == m and str(r["periodo"]) == p)


def _b(d, s, a, x, y, e="mes_anio"):
    return next(r for r in d["brechas"] if r["split"] == s and r["ambito"] == a
                and r["metodo_a"] == x and r["metodo_b"] == y and r["esquema"] == e)


def test_titulos_fijos_siguen_siendo_ciertos(datos):
    cinco = ["llr_simple", "llr_rezagos_sel", "tuned_sin_td", "tuned", "timesfm_anom"]
    for s in ("ll4", "ll4b"):
        for a in ("panel", "peru"):
            rm = {m: _m(datos, s, a, m)["rmse"] for m in cinco}
            assert min(rm, key=rm.get) == "timesfm_anom"
            # A2: sin rezagos de Td, tuned mejora y sigue con mayor RMSE que TimesFM.
            assert rm["timesfm_anom"] < rm["tuned_sin_td"] < rm["tuned"]
            r = _b(datos, s, a, "timesfm_anom", "llr_rezagos_sel")
            assert abs(r["brecha"]) < 0.05
            # Encabezado: frente a tuned, IC sin cero en los dos esquemas.
            for e in ("espacial_2g", "mes_anio"):
                assert _b(datos, s, a, "timesfm_anom", "tuned", e)["ic_hi"] < 0
        # Robustez: con Td y Tmin crudas tambien supera a tuned en 2009-2012.
    for a in ("panel", "peru"):
        assert _m(datos, "ll4b", a, "timesfm_td")["rmse"] < _m(datos, "ll4b", a, "tuned")["rmse"]
    r = _b(datos, "ll4", "panel", "timesfm_anom", "llr_rezagos_sel")
    assert r["ic_lo"] <= 0 <= r["ic_hi"]
    # Escalera: TimesFM por delante de los dos LLR en todo inicio, IC mes-anio sin cero.
    for s in ("ll4", "ll4b"):
        for i in datos["meta"]["escaleraInicios"]:
            for m in ("llr_simple", "llr_rezagos"):
                g = next(x for x in datos["escaleraBrechas"] if x["split"] == s and x["esquema"] == "mes_anio"
                         and x["metodo_a"] == f"timesfm@{i}" and x["metodo_b"] == f"{m}@{i}")
                assert g["ic_hi"] < 0
    # A3: con la Tmin de otro anio, peor que la climatologia.
    clim = next(x for x in datos["a3"] if x["corrida"] == "pred_clim")["rmse"]
    anios = [x for x in datos["a3"] if x["modo"] == "year"]
    assert anios and all(x["rmse"] > clim for x in anios)


def test_parse_a3():
    texto = """celdas 3 filas 30
pred_clim              rmse 1.2840  skill +0.000  bias -0.166
real_anom              rmse 0.8389  skill +0.347  bias +0.065
shuf_anom_year_s2      rmse 1.5509  skill -0.208  bias -0.156
shuf_anom_cell_s0      rmse 1.2656  skill +0.014  bias +0.079
"""
    f = aa.parse_a3(texto)
    assert list(f.corrida) == ["pred_clim", "real_anom", "shuf_anom_year_s2", "shuf_anom_cell_s0"]
    assert f.celdas.unique().tolist() == [3] and f.filas.unique().tolist() == [30]
    r = f.set_index("corrida")
    assert r.loc["shuf_anom_year_s2", "semilla"] == 2 and r.loc["shuf_anom_year_s2", "modo"] == "year"
    assert r.loc["real_anom", "tmin"] == "real" and r.loc["shuf_anom_cell_s0", "modo"] == "cell"
    assert r.loc["shuf_anom_year_s2", "rmse"] == pytest.approx(1.5509)


def test_a3_csv_coincide_con_su_salida():
    f = pd.read_csv(RES / "a3_control_tmin_barajada.csv")
    assert {"pred_clim", "real_anom", "shuf_anom_year_s0", "shuf_anom_year_s1", "shuf_anom_year_s2",
            "shuf_anom_cell_s0"} <= set(f.corrida)


def test_html_carga_los_dos_archivos_y_no_repite_ids():
    s = HTML.read_text(encoding="utf-8")
    assert s.index('<script src="datos.js">') < s.index('<script src="datos_amenazas.js">')
    ids = re.findall(r'\bid="([^"]+)"', s)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    assert not dup, dup
    assert 'href="#amenazas"' in s and 'id="amenazas"' in s


def test_paper_orden_y_fuentes(datos):
    s = HTML.read_text(encoding="utf-8")
    assert 'href="#paper"' in s
    assert s.index('<section id="paper">') < s.index('<section id="amenazas">')
    assert '<script src="paper.js"></script>' in s
    assert 'am-t-regla' not in s
    assert 'lectura("soloB")' not in s
    # El tiempo de versiones iniciales no se reasigna al control seleccionado.
    assert not any(r["metodo"] in {"llr_rezagos_sel", "llr_simple_sel"} for r in datos["costo"])
    # Cada celda necesaria para las tablas anuales y por zona tiene rivales pareados.
    methods = {"clim", "tuned", "llr_simple", "llr_rezagos_sel", "timesfm_anom"}
    by_key = collections.defaultdict(set)
    for r in datos["porMetodo"]:
        by_key[(r["split"], r["ambito"], str(r["periodo"]))].add(r["metodo"])
    assert by_key and all(methods <= m for m in by_key.values())
    zones = collections.defaultdict(set)
    for r in datos["porZona"]:
        zones[(r["split"], r["ambito"], r["zone_id"])].add(r["metodo"])
    assert zones and all(methods <= m for m in zones.values())


def test_datos_publicados_coinciden_con_generador(datos):
    text = (REPO / aa.OUT).read_text(encoding="utf-8")
    assert json.loads(text.removeprefix("window.AMENAZAS = ").strip().removesuffix(";")) == datos


SECCIONES = ["resultado", "horizonte", "soporte", "sesgo-mensual", "alcance", "escala", "divergencia",
             "campo", "paper", "amenazas", "limites", "protocolo"]
# Lo que salio de la seccion A1-A4: A4, victorias por zona, matrices duplicadas y la regla E/C+A.
RETIRADAS = ["am-a4", "am-fig-zonas", "am-fig-rmse", "am-fig-brechas", "am-t-regla", "am-conclusion"]
FUERA_DE_NARRATIVA = ["T1", "transferencia", "El Niño", "ERA5", "ISD", "TCN", "ganador universal", "E/C+A",
                      "Amenazas A1–A4", "recibe más información"]


def _seccion(s, sid):
    return re.search(rf'<section id="{sid}">.*?</section>', s, re.S).group(0)


def test_html_conserva_el_benchmark_y_reemplaza_a1_a4():
    s = HTML.read_text(encoding="utf-8")
    assert re.findall(r'<section id="([^"]+)"', s) == SECCIONES
    nav = re.search(r'<nav class="story-nav".*?</nav>', s, re.S).group(0)
    assert 'href="#paper">Paper<' in nav and 'href="#amenazas">Controles<' in nav
    for x in RETIRADAS:
        assert f'id="{x}"' not in s, x


def test_paper_y_controles_sin_temas_fuera_de_la_narrativa():
    s = HTML.read_text(encoding="utf-8")
    textos = {"paper": _seccion(s, "paper"), "amenazas": _seccion(s, "amenazas"),
              "paper.js": HTML.with_name("paper.js").read_text(encoding="utf-8")}
    for nombre, t in textos.items():
        for palabra in FUERA_DE_NARRATIVA:
            assert palabra not in t, (nombre, palabra)


def test_cribado_seis_de_nueve_superan_a_tuned():
    t = pd.read_csv(REPO / "reports/timesfm_benchmark/cribado_limpio/leaderboard.csv")
    tuned = t.loc[t.method == "tuned", "rmse"].item()
    v = t[t.method.str.startswith("timesfm:")]
    assert len(v) == 9
    assert set(v.loc[v.rmse >= tuned, "method"]) == {"timesfm:tmin_td_short", "timesfm:uni_anom_full",
                                                      "timesfm:uni_td_full"}


def _dur(s):
    """Mismo formato que dur() de paper.js."""
    if s >= 72 * 3600:
        return f"{s / 86400:.1f} días"
    if s >= 3600:
        h = int(s // 3600)
        return f"{h} h {round((s - h * 3600) / 60)} min"
    if s >= 60:
        mi = int(s // 60)
        return f"{mi} min {round(s - mi * 60)} s"
    return f"{round(s)} s"


CHROME = shutil.which("google-chrome") or shutil.which("chromium")


@pytest.mark.skipif(CHROME is None, reason="sin Chrome")
def test_pagina_se_dibuja_sin_errores_y_con_costos_del_csv():
    r = subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--virtual-time-budget=15000",
         "--enable-logging=stderr", "--v=0", "--dump-dom", HTML.as_uri()],
        capture_output=True, text=True, timeout=120,
    )
    assert "Uncaught" not in r.stderr, r.stderr[-2000:]
    dom = r.stdout
    for svg in ("am-fig-anio", "am-fig-a2", "am-fig-escalera", "am-fig-a3"):
        assert re.search(rf'<svg id="{svg}"[^>]*>.*?<(circle|line|path|rect)', dom, re.S), svg
    assert re.search(r'id="paper-robustez-titulo">6 de las 9 configuraciones', dom)
    assert re.search(r'<svg id="fig-ranking"[^>]*>.*?<circle', dom, re.S)    # el benchmark original sigue
    tabla = re.search(r'<table id="paper-costos"[^>]*>(.*?)</table>', dom, re.S).group(1)
    filas = [[re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<td[^>]*>(.*?)</td>", f, re.S)]
             for f in re.findall(r"<tr[^>]*>(.*?)</tr>", tabla, re.S)[1:]]
    assert len(filas) == 6
    c = pd.read_csv(RES / "costo.csv")
    seg = lambda m, b, e: c[(c.metodo == m) & (c.bloque == b) & (c.etapa == e)].segundos_pared.item()
    tuned_ll4b = seg("tuned", "ll4b", "seleccion de recetas (solo anios de entrenamiento)") + \
        seg("tuned", "ll4b", "ajuste + prediccion (backtest)")
    assert filas[0][1] == "Palacios (tuned)" and filas[0][-1] == _dur(tuned_ll4b)
    assert filas[1][1] == "TimesFM" and filas[1][-1] == _dur(
        seg("timesfm_anom", "ll4b", "prediccion (sin ajuste ni seleccion)"))
    prod = seg("tuned", "produccion 1981-2016", "seleccion de recetas (grid completo)") + \
        seg("tuned", "produccion 1981-2016", "ajuste (grid completo)") + \
        seg("tuned", "real 2017-2020", "prediccion (grid completo)")
    assert filas[4][-1] == _dur(prod)
    assert filas[5][-1] == _dur(seg("timesfm_anom", "real 2017-2020", "prediccion producto completo"))
