"""Prueba de datos_amenazas.js (seccion A1-A4 del artefacto TimesFM).

Verifica que el generador escribe las claves esperadas, que cada cifra coincide con su CSV
de origen y que las afirmaciones fijas de los titulos de la seccion siguen siendo ciertas.
"""

import collections
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from experiments.amenazas import artifact_amenazas as aa

REPO = Path(__file__).resolve().parents[1]
RES = REPO / aa.RES
HTML = REPO / "reports/timesfm_benchmark/artifact/index.html"
CLAVES = {"meta", "informacion", "porMetodo", "brechas", "victorias", "escalera", "escaleraBrechas",
          "a4PorAnio", "a4PorPeriodo", "a4Delta", "a3"}


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
            assert rm["tuned_sin_td"] < rm["tuned"]
            r = _b(datos, s, a, "timesfm_anom", "llr_rezagos_sel")
            assert abs(r["brecha"]) < 0.05
            e = _b(datos, s, a, "tuned_sin_td", "llr_simple")
            assert e["ic_lo"] <= 0 <= e["ic_hi"]
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
    # A4: los productos heredan el sesgo humedo de PISCO en Td cruda.
    td = {(x["fuente"], x["periodo"]): x for x in datos["a4PorPeriodo"] if x["kind"] == "td"}
    pisco = td[("pisco", "2009-2016")]["sesgo"]
    for f in ("palacios", "timesfm"):
        assert td[(f, "2017-2020")]["sesgo"] > 1 and abs(td[(f, "2017-2020")]["sesgo"] - pisco) < 0.15


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
