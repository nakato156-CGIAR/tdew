"""Prueba de datos_kl_calido.js (subseccion "Divergencia calida" del artefacto TimesFM).

Verifica las claves, que cada cifra coincide con su CSV de origen y que las afirmaciones
fijas del texto de la subseccion siguen siendo ciertas en los CSV.
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from experiments.timesfm import artifact_kl_calido as ak

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / ak.SRC
HTML = REPO / "reports/timesfm_benchmark/artifact/index.html"
pytestmark = pytest.mark.skipif(not (SRC / "zona.csv").exists(), reason="faltan los CSV de kl_calido")


@pytest.fixture(scope="module")
def datos(tmp_path_factory):
    out = tmp_path_factory.mktemp("klc") / "datos_kl_calido.js"
    ak.build(out, SRC)
    text = out.read_text(encoding="utf-8")
    assert text.startswith("window.D_KLC = ")
    return json.loads(text[len("window.D_KLC = "):].rstrip().rstrip(";"))


def test_claves(datos):
    assert set(datos) == {"meta", "nacional", "zona", "anio", "anioMes", "depto", "dem"}
    assert datos["meta"]["B"] == [20.0, 24.0] and datos["meta"]["celdas"] == 17027


@pytest.mark.parametrize("nombre", sorted(ak.CORTES))
def test_cifras_iguales_al_csv(datos, nombre):
    clave = ak.CORTES[nombre][0]
    esperado = ak.leer(nombre, SRC)
    obtenido = pd.DataFrame(datos[clave])
    assert len(obtenido) == len(esperado) > 0
    for c in esperado.columns:
        if pd.api.types.is_float_dtype(esperado[c]):
            assert (esperado[c] - obtenido[c]).abs().max() < 1e-4, c
        else:
            assert list(esperado[c]) == list(obtenido[c]), c


def test_afirmaciones_del_texto():
    z = pd.read_csv(SRC / "zona.csv").set_index(["zone_id", "model"])
    for m in ("timesfm", "llr"):
        assert z.loc[(0, m), "share_B"] > 1
        assert z.loc[(11, m), "delta_B"] > 0
        assert -0.36 < z.loc[(11, m), "share_B"] < -0.24          # "entre un cuarto y un tercio"
    d = pd.read_csv(SRC / "depto.csv").set_index(["depto", "model"])
    for dep in ("UCAYALI", "MADRE DE DIOS"):                       # cambian de signo entre metodos
        assert d.loc[(dep, "timesfm"), "delta_B"] * d.loc[(dep, "llr"), "delta_B"] < 0
    za = pd.read_csv(SRC / "zona_anio.csv")
    za = za[za.zone_id == 0].set_index(["anio", "model"])
    for m in ("timesfm", "llr"):                                   # 2013 el mas fuerte en la zona 0
        assert za.xs(m, level="model").delta_B.idxmin() == 2013
    assert za.loc[(2013, "clim"), "delta_B"] < 0 and za.loc[(2014, "clim"), "delta_B"] < 0


def test_pagina_carga_el_archivo():
    s = HTML.read_text(encoding="utf-8")
    assert s.index('<script src="datos.js">') < s.index('<script src="datos_kl_calido.js">')
    assert 'id="kl-calido"' in s and 'href="#kl-calido"' in s
