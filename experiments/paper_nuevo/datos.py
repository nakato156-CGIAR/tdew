"""Lectura de las fuentes numericas del paper nuevo en un solo objeto, sin transformar cifras."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache

import pandas as pd

from experiments.paper_nuevo import fuentes as F

SPLITS = ("ll4b", "ll4")  # orden de presentacion: ll4b primero
AMBITOS = ("panel", "peru")
AMBITO_TXT = {"panel": "dominio completo", "peru": "Perú"}


def limpiar_etiqueta(s: str) -> str:
    """Corrige etiquetas de zona con mojibake (utf-8 leido como latin-1)."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def _tabla_md(texto: str, encabezado: str) -> pd.DataFrame:
    """Primera tabla pipe que sigue al encabezado `encabezado` de un .md."""
    lineas = texto.splitlines()
    i = next(k for k, ln in enumerate(lineas) if ln.startswith(encabezado))
    filas = []
    for ln in lineas[i + 1:]:
        if ln.startswith("|"):
            filas.append([c.strip() for c in ln.strip().strip("|").split("|")])
        elif filas:
            break
    cab, filas = filas[0], [f for f in filas[2:]]
    return pd.DataFrame(filas, columns=cab)


@dataclass
class Datos:
    metodo: pd.DataFrame
    brechas: pd.DataFrame
    zona: pd.DataFrame
    victorias: pd.DataFrame
    escalera: pd.DataFrame
    esc_brechas: pd.DataFrame
    a3: pd.DataFrame
    a4_periodo: pd.DataFrame
    a4_boot: pd.DataFrame
    a4_estacion: pd.DataFrame
    a4_estaciones: pd.DataFrame
    costo: pd.DataFrame
    insumos: pd.DataFrame
    estacion_trabajo: str
    leaderboard: pd.DataFrame
    panel: pd.DataFrame
    replicas: int
    semilla: int
    bloque_grados: float
    zone_table_labels: list[str] | None
    r1_horizonte: pd.DataFrame
    r1_boot: pd.DataFrame
    r1_dm: pd.DataFrame
    r2_skill: pd.DataFrame
    r2_extremos: pd.DataFrame
    r2_calibracion: pd.DataFrame
    r2_altitud: pd.DataFrame
    r2_zona_dom: pd.DataFrame
    r2_enso: pd.DataFrame
    r3_costo: pd.DataFrame | None  # None si r3_costo_llr_sel.csv no existe todavia


@lru_cache(maxsize=1)
def cargar() -> Datos:
    zona = pd.read_csv(F.A1_POR_ZONA)
    zona["zone_label"] = zona["zone_label"].map(limpiar_etiqueta)
    notas = json.loads(F.A1_BRECHAS_PROV.read_text())["notes"]
    mm = re.search(r"bootstrap (\d+) replicas semilla (\d+), bloques\s+espaciales de ([\d.]+) grados", notas)
    if mm is None:
        raise ValueError("no se pudo leer replicas/semilla/bloques de la proveniencia de a1_brechas.csv")
    md = F.COSTO_MD.read_text()
    hw = re.search(r"Estación de\s+trabajo:\s*(.*?)\s*\(`reports", " ".join(md.split()))
    zt = F.zone_table_path()
    labels = None
    if zt is not None:
        labels = sorted(limpiar_etiqueta(s) for s in pd.read_parquet(zt, columns=["zone_label"])["zone_label"].unique())
    a4p = pd.read_csv(F.A4_POR_PERIODO)
    return Datos(
        metodo=pd.read_csv(F.A1_POR_METODO),
        brechas=pd.read_csv(F.A1_BRECHAS),
        zona=zona,
        victorias=pd.read_csv(F.A1_VICTORIAS),
        escalera=pd.read_csv(F.A1_ESCALERA),
        esc_brechas=pd.read_csv(F.A1_ESCALERA_BRECHAS),
        a3=pd.read_csv(F.A3_BARAJADA),
        # A4 base: solo la muestra `productos` (sin filas de ERA5).
        a4_periodo=a4p[a4p["muestra"] == "productos"].copy(),
        a4_boot=pd.read_csv(F.A4_DELTA_BOOT).query("muestra == 'productos'").copy(),
        a4_estacion=pd.read_csv(F.A4_POR_ESTACION).query("muestra == 'productos'").copy(),
        a4_estaciones=pd.read_csv(F.A4_ESTACIONES, dtype={"station": str}),
        costo=pd.read_csv(F.COSTO_CSV),
        insumos=_tabla_md(md, "## Insumos de diseño"),
        estacion_trabajo=hw.group(1) if hw else "",
        leaderboard=pd.read_csv(F.LEADERBOARD),
        panel=pd.read_csv(F.PANEL_NACIONAL),
        replicas=int(mm.group(1)), semilla=int(mm.group(2)), bloque_grados=float(mm.group(3)),
        zone_table_labels=labels,
        r1_horizonte=pd.read_csv(F.R1_HORIZONTE), r1_boot=pd.read_csv(F.R1_BOOT), r1_dm=pd.read_csv(F.R1_DM),
        r2_skill=pd.read_csv(F.R2_SKILL), r2_extremos=pd.read_csv(F.R2_EXTREMOS),
        r2_calibracion=pd.read_csv(F.R2_CALIBRACION), r2_altitud=pd.read_csv(F.R2_ALTITUD),
        r2_zona_dom=pd.read_csv(F.R2_ZONA_DOM).assign(zona_dominante=lambda x: x.zona_dominante.map(limpiar_etiqueta)),
        r2_enso=pd.read_csv(F.R2_ENSO),
        r3_costo=pd.read_csv(F.R3_COSTO) if F.R3_COSTO.exists() else None,
    )
