"""Tablas del paper nuevo: Tab1-Tab7 (cuerpo) y S1-S7, S9-S14 (suplemento; S8 es texto, sin tabla generada).

Cada tabla sale en ``reports/paper_nuevo/tablas/<id>.md`` (tabla pipe sin leyenda; la leyenda va
en el .qmd) y ``<id>.csv`` (los valores numericos detras, con ``.provenance.json``). Todas las
cifras se toman de las claves de ``cifras.py`` para que tabla y texto no puedan diferir.
"""

from __future__ import annotations

import csv
import io
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from experiments.paper_nuevo import cifras as ci
from experiments.paper_nuevo import fuentes as F
from experiments.paper_nuevo import formato as fm
from experiments.paper_nuevo.cifras import Registro, alias, par
from experiments.paper_nuevo.datos import AMBITO_TXT, AMBITOS, SPLITS, Datos, cargar

log = logging.getLogger(__name__)

Cell = tuple  # (valor_num | None, texto)

TABLE_IDS = (
    "tab1", "tab1_insumos", "tab2", "tab3", "tab4", "tab5", "tab6", "tab6_resumen",
    "s1", "s1_anual", "s1_victorias", "s2", "s3", "s3_brechas", "s4", "s4_delta", "s5", "s6", "s7",
    "tab7_robustez", "tab8_isd_estaciones", "s9_skill", "s10_extremos", "s11_calibracion", "s12_altitud", "s13_enso", "s14_zona_dominante",
)
M_TXT = ci.NOMBRE
# Rotulo de bloque en las tablas: anos de prueba, no el codigo interno (`ll4b`, `ll4`), que solo se define en Tab2.
BLQ = {"ll4b": "2009–2012", "ll4": "2013–2016"}


# --- Texto de tablas sin rutas, scripts ni identificadores de codigo ------------------------
_OBS_SUST = [
    (r"\s*\(\$WORK/[^)]*\)", ""),
    (r"\s*\(\$RES/[^)]*\)", ""),
    (r"con /usr/bin/time \(incluye arranque de uv\)", "(incluye el arranque del entorno)"),
    (r"incluye arranque de uv", "incluye el arranque del entorno"),
    (r"sin arranque de uv", "sin el arranque del entorno"),
    (r"per_zone_n=(\d[\d.]*)", r"\1 celdas por zona"),
    (r"train_start", "año de inicio"),
    (r"\s*\(numpy\)", ""),
    (r"incluye parquet de", "incluye la escritura de"),
    (r"sin tmin_td_25 ni repeticiones", "sin una variante adicional ni repeticiones"),
    (r"sobre el mismo bloque ll4\b", "sobre el mismo bloque 2013–2016"),
    (r"otro agente usaba CPU y GPU en paralelo", "otro proceso usaba CPU y GPU en paralelo"),
]
_HW_SUST = [(r"\(b0_run\.sh: local single-GPU\)", "(una GPU local)")]
_METODO_TXT = {
    "timesfm_anom": "TimesFM", "timesfm_td": "TimesFM en Td cruda", "timesfm (9 variantes)": "TimesFM (todas las variantes del cribado)",
    "tuned": "tuned", "llr_simple": "LLR simple", "llr_rezagos": "LLR con rezagos",
    "llr_simple_sel": "LLR simple seleccionado", "llr_rezagos_sel": "LLR con rezagos seleccionado",
}
_BLOQUE_TXT = {"ll4b": "2009–2012", "ll4": "2013–2016", "real 2017-2020": "producto 2017–2020", "produccion 1981-2016": "producción 1981–2016"}


def _sust(texto: str, reglas) -> str:
    for pat, rep in reglas:
        texto = re.sub(pat, rep, texto)
    return texto


def _obs(r) -> str:
    return "" if r.observaciones != r.observaciones else _sust(str(r.observaciones), _OBS_SUST)


def T(texto: str) -> Cell:
    return (None, texto)


def N(x: float, nd: int = 3, signo: bool = False) -> Cell:
    return (float(x), fm.num(x, nd, signo))


@dataclass
class Tabla:
    id: str
    columnas: list[str]
    filas: list[list[Cell]] = field(default_factory=list)
    fuentes: str = ""
    # Tablas con identificadores largos (rutas, nombres de corrida): se permite cortar linea tras "_" y "/".
    # Se anade U+200B, invisible, para que Typst no desborde la celda. No altera el CSV.
    romper_ids: bool = False

    def _celda(self, texto: str) -> str:
        texto = texto.replace("|", "\\|").replace("$", "\\$")  # "$" suelto se leeria como matematica
        return re.sub(r"([_/@])(?=\w)", "\\1\u200b", texto) if self.romper_ids else texto

    def md(self) -> str:
        num_col = [all(f[i][0] is not None or f[i][1] in (fm.ND, "—") for f in self.filas) for i in range(len(self.columnas))]
        # Anchos relativos: Pandoc los toma de la longitud de los guiones del separador cuando alguna fila
        # supera el ancho de linea. Proporcionales al texto mas largo de cada columna, acotados.
        def ancho(i):
            cel = max(len(self._celda(f[i][1]).replace("\u200b", "")) for f in self.filas)
            palabra = max(len(w) for w in self.columnas[i].replace("`", "").split())
            # el texto largo se parte en varias lineas (tope 28); una palabra o cifra no se parte (se reserva su ancho)
            if num_col[i] or cel <= 12:
                return round(max(cel, palabra) * 1.7) + 4   # numericas y textos cortos: no se parten, ancho completo
            return max(8, round(max(min(cel, 24) * 0.9, palabra * 1.35)) + 3)
        sep = [("-" * ancho(i) + ":") if n else (":" + "-" * ancho(i)) for i, n in enumerate(num_col)]
        lin = ["| " + " | ".join(self.columnas) + " |",
               "|" + "|".join(sep) + "|"]
        for f in self.filas:
            lin.append("| " + " | ".join(self._celda(c[1]) for c in f) + " |")
        return "\n".join(lin) + "\n"

    def csv(self) -> str:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(self.columnas)
        for f in self.filas:
            w.writerow([repr(c[0]) if c[0] is not None else c[1] for c in f])
        return buf.getvalue()


def g(R: Registro, clave: str) -> Cell:
    """Celda desde una clave de cifras; 'n. d.' si no existe en las fuentes."""
    if clave not in R.filas:
        return (None, fm.ND)
    f = R.filas[clave]
    return (f["valor_num"], f["valor_texto"])


def _blq_amb(s: str, a: str) -> list[Cell]:
    return [T(BLQ[s]), T(AMBITO_TXT[a])]


# ---------------------------------------------------------------------------------------
# Tab1: textos cualitativos. No contienen cifras; las cifras se anaden desde `cifras`.
# Origen: costo.md ("Insumos de diseno") y paper_narrative.md §3.3 (lineas 53-57);
# licencia de pesos: ORIENTACION_PAPER.md:37 y paper_narrative.md:55.
def tab1(R: Registro, d: Datos) -> Tabla:
    insumos = d.insumos.set_index(d.insumos.columns[0])[d.insumos.columns[1]]
    lic_timesfm = fm.ND
    for k, v in insumos.items():
        if "TimesFM" in k and "licencia no comercial" in v:
            lic_timesfm = "No comercial (checkpoint preentrenado)"
    nvar = R.texto("cribado.n_variantes")
    costo = ci.costo_filas(d)

    def hw(cid):
        r = costo[cid]
        return f"{r.hardware}; GPU: {str(r.gpu).replace('si', 'sí', 1) if str(r.gpu).startswith('si') else r.gpu}"

    filas = [
        ["Climatología", "No", "Ninguna", "Media por celda y día del año", "Td de los años de entrenamiento", fm.ND, "No aplica"],
        ["LLR simple y con rezagos de Tmin", "No", "Un semiancho h global en una grilla corta", "Coeficientes por celda",
         "Climatología de Td y Tmin; anomalía de Tmin del bloque (con rezagos en la segunda variante)", hw("llr_simple_ll4b_total"), "No aplica"],
        ["LLR seleccionados", "No", "Semiancho h y año de inicio, por validación interna",
         "Coeficientes por celda", "Igual que el LLR correspondiente", fm.ND + " (tiempo no medido)", "No aplica"],
        ["tuned", "Sí: unidades cartográficas SENAMHI", "Receta y h por zona × día del año (validación dejando un año fuera)",
         "Coeficientes por celda; despliegue autorregresivo con rezagos de Td", "Td y Tmin históricos, rezagos de Td y de Tmin; zona de la celda",
         hw("tuned_ll4b_seleccion"), "No aplica"],
        ["TimesFM", "No", f"Elección de una configuración entre {nvar} (cribado único, en 2013–2016)",
         "Ninguno: pesos preentrenados sin modificar", "Historial local de Td y Tmin, climatologías y Tmin observada del bloque",
         hw("timesfm_ll4b_inferencia"), lic_timesfm],
    ]
    t = Tabla("tab1", ["Método", "Zonas SENAMHI", "Búsqueda previa", "Ajuste de pesos o coeficientes", "Datos por celda", "Hardware", "Licencia de pesos"],
              fuentes="costo.md (Insumos de diseño), costo.csv (hardware, gpu), paper_narrative.md §3.3")
    t.filas = [[T(x) for x in f] for f in filas]
    return t


def tab1_insumos(R: Registro, d: Datos) -> Tabla:
    """Insumos y decisiones previas por método, en prosa breve y sin rutas ni nombres de archivos."""
    x = lambda k: R.texto(k)  # noqa: E731
    t = Tabla("tab1_insumos", ["Método", "Insumos y decisiones previas"], fuentes="costo.md, sección «Insumos de diseño» (reescrito sin rutas); cifras de cifras.py")
    filas = [
        ("Climatología", "Media por celda y día del año en los años de entrenamiento."),
        ("LLR simple", f"Climatología de Td y Tmin por celda; núcleo tricúbico circular en el día del año; un único semiancho global elegido en una grilla de {x('diseno.llr.h_n')} valores ({x('diseno.llr.h_min')} a {x('diseno.llr.h_max')}) con los últimos {x('diseno.llr.validacion_anios')} años de entrenamiento; sin zonas ni rezagos."),
        ("LLR con rezagos", f"Lo mismo, más rezagos fijos de la anomalía de Tmin ({x('diseno.llr.rezagos_tmin')} días) y una regularización de cresta mínima."),
        ("LLR seleccionados", f"Misma familia de regresión local, con búsqueda conjunta de {x('diseno.llr_sel.h_n')} semianchos ({x('diseno.llr_sel.h_min')} a {x('diseno.llr_sel.h_max')}) y {x('diseno.llr_sel.inicios_n')} años de inicio ({x('diseno.llr_sel.inicio_min')} a {x('diseno.llr_sel.inicio_max')}) por validación interna; ajuste por celda; sin zonas; costo no medido."),
        ("tuned", f"Zonas climáticas de SENAMHI ({x('panel.unidades_total')} unidades cartográficas: {x('panel.tipos_climaticos')} tipos climáticos y {x('panel.unidades_extra')} unidades adicionales); pool de {x('diseno.tuned.pool_terminos')} términos candidatos (constante, Tmin del día, rezagos de Tmin de {x('diseno.tuned.rezagos_tmin')} días y rezagos de Td de {x('diseno.tuned.rezagos_td')} días); búsqueda de receta y semiancho por zona y día del año con muestreo de celdas por zona; reconstrucción autorregresiva con sus propios rezagos de Td; implementación en GPU."),
        ("TimesFM 3.0", f"Checkpoint preentrenado (unos {x('timesfm.parametros_millones')} millones de parámetros, licencia no comercial); climatología para construir la anomalía; Tmin observada del bloque como covariable; elección entre {x('cribado.n_variantes')} configuraciones de entrada, objetivo y contexto; GPU en la práctica."),
    ]
    t.filas = [[T(a), T(b)] for a, b in filas]
    return t


def tab2(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab2", ["Prueba", "Contexto", "Años de contexto", "Celdas (dominio completo / Perú)", "Filas (dominio completo / Perú)", "Código de tuned", "Selección de configuración que vio el bloque"],
              fuentes="a1_por_metodo.csv, a1_escalera_contexto.csv, costo.csv, paper_narrative.md §3.4")
    nv = R.texto("cribado.n_variantes")
    sel = {
        "ll4b": "No participó en el cribado de TimesFM; recetas de tuned y selección de los LLR solo con años de entrenamiento",
        "ll4": f"Cribado de {nv} variantes de TimesFM realizado sobre este bloque; recetas de tuned y selección de los LLR solo con años de entrenamiento",
    }
    cod = {"ll4b": "Código del repositorio (no el entorno de Palacios)", "ll4": "Código del repositorio; reproduce la cifra de la corrida limpia de Palacios"}
    for s in SPLITS:
        t.filas.append([
            T(f"{R.texto(f'bloques.{s}.anio_ini')}–{R.texto(f'bloques.{s}.anio_fin')}"),
            T(f"{R.texto(f'bloques.{s}.contexto_ini')}–{R.texto(f'bloques.{s}.contexto_fin')}"),
            g(R, f"bloques.{s}.anios_contexto"),
            T(f"{R.texto(f'celdas.{s}.panel')} / {R.texto(f'celdas.{s}.peru')}"),
            T(f"{R.texto(f'filas.{s}.panel')} / {R.texto(f'filas.{s}.peru')}"),
            T(cod[s]), T(sel[s])])
    return t


def tab3(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab3", ["Bloque", "Ámbito", "Método", "RMSE (°C)", "MAE (°C)", "Sesgo (°C)"], fuentes="a1_por_metodo.csv, periodo = total")
    for s in SPLITS:
        for a in AMBITOS:
            for m in ("clim", "tuned", "llr_rezagos_sel", "timesfm_anom"):
                k = f"{s}.{a}.{alias(m)}"
                t.filas.append(_blq_amb(s, a) + [T(M_TXT[m]), g(R, f"rmse.{k}"), g(R, f"mae.{k}"), g(R, f"sesgo.{k}")])
    return t


VAR_TXT = {
    "tmin_anom_full": "Referencia: anomalía de Td con anomalía de Tmin, contexto desde 1981",
    "tmin_doy_td_full": "Td con Tmin y día del año, contexto desde 1981",
    "tmin_td_symavg": "Td con Tmin, inferencia con promediado simétrico",
    "tmin_td_znorm": "Td con Tmin, con z-score externo",
    "tmin_td_full": "Td con Tmin, contexto desde 1981",
    "tmin_td_med": "Td con Tmin, contexto desde 2002",
    "tmin_td_short": "Td con Tmin, contexto desde 2011",
    "uni_anom_full": "Anomalía de Td sin covariables",
    "uni_td_full": "Td sin covariables",
}


def tab4(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab4", ["Variante", "RMSE (°C)", "MAE (°C)", "Sesgo (°C)", "RMSE − RMSE de tuned (°C)", "¿RMSE menor que tuned?"],
              fuentes="reports/timesfm_benchmark/cribado_limpio/leaderboard.csv (split ll4)")
    t.filas.append([T("tuned (referencia)"), g(R, "cribado.tuned.rmse"), g(R, "cribado.tuned.mae"), g(R, "cribado.tuned.sesgo"), T("—"), T("—")])
    t.filas.append([T("climatología"), g(R, "cribado.clim.rmse"), g(R, "cribado.clim.mae"), g(R, "cribado.clim.sesgo"), T("—"), T("—")])
    lb = d.leaderboard
    for m in lb[(lb.split == "ll4") & lb.method.str.startswith("timesfm:")].method:
        s = m.split(":", 1)[1]
        k = f"cribado.v.{s}"
        t.filas.append([T(VAR_TXT.get(s, s)), g(R, f"{k}.rmse"), g(R, f"{k}.mae"), g(R, f"{k}.sesgo"), g(R, f"{k}.delta_tuned"), g(R, f"{k}.menor_tuned")])
    return t


def _fila_brecha(R: Registro, s: str, a: str, x: str, y: str) -> list[Cell]:
    k = f"brecha.{s}.{a}.{par(x, y)}"
    return [g(R, f"{k}.v"), g(R, f"{k}.esp_ic"), g(R, f"{k}.ma_ic")]


def tab5(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab5", ["Bloque", "Ámbito", "Método", "RMSE (°C)", "Brecha TimesFM − método (°C)", "IC 95 % espacial 2°", "IC 95 % mes-año"],
              fuentes="a1_por_metodo.csv, a1_brechas.csv")
    for s in SPLITS:
        for a in AMBITOS:
            for m in ("tuned", "tuned_sin_td", "llr_rezagos_sel", "timesfm_td", "timesfm_anom"):
                rm = g(R, f"rmse.{s}.{a}.{alias(m)}")
                if m == "timesfm_anom":
                    fila = [T("—"), T("—"), T("—")]
                elif f"brecha.{s}.{a}.{par('timesfm_anom', m)}.v" in R.filas:
                    fila = _fila_brecha(R, s, a, "timesfm_anom", m)
                elif m == "timesfm_td" and f"rmse.{s}.{a}.timesfm_td" in R.filas:
                    dif = R.num(f"rmse.{s}.{a}.timesfm") - R.num(f"rmse.{s}.{a}.timesfm_td")
                    fila = [N(dif, 3, True), T(fm.ND), T(fm.ND)]
                else:
                    fila = [T(fm.ND), T(fm.ND), T(fm.ND)]
                t.filas.append(_blq_amb(s, a) + [T(M_TXT[m]), rm] + fila)
    return t


def tab6(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab6", ["Escala", "Método", "Etapa", "Tiempo de pared", "Segundos", "Hardware"], fuentes="costo.csv, costo.md")
    rows = ci.costo_filas(d)

    def fila(esc, met, etapa, cid):
        r = rows[cid]
        t.filas.append([T(esc), T(met), T(etapa), g(R, f"costo.{cid}.tiempo"), g(R, f"costo.{cid}.seg"), T(_sust(str(r.hardware), _HW_SUST))])

    def total(esc, met, etapa, base):
        t.filas.append([T(esc), T(met), T(etapa), g(R, f"{base}.tiempo"), g(R, f"{base}.seg"), T("—")])

    blq = "2009–2012, estación con GPU"
    blq_llr = "2009–2012, otra máquina, sin GPU"
    fila(blq, "tuned", "Selección de recetas (solo años de entrenamiento)", "tuned_ll4b_seleccion")
    fila(blq, "tuned", "Ajuste y predicción", "tuned_ll4b_ajuste")
    total(blq, "tuned", "Total", "costo.ll4b.tuned_total")
    fila(blq, "TimesFM", "Inferencia (sin ajuste de pesos)", "timesfm_ll4b_inferencia")
    fila(blq, "TimesFM", "Selección única de configuración (hecha en 2013–2016, suma de las variantes)", "timesfm_cribado")
    total(blq, "TimesFM", "Total incluyendo la selección una vez", "costo.ll4b.timesfm_total")
    t.filas.append([T(blq), T("TimesFM / tuned"), T("Cociente de totales"), g(R, "costo.ll4b.ratio_total_r"), (None, "—"), T("—")])
    if d.r3_costo is not None:
        r3 = ci.r3_filas(d)
        for met, nom in (("llr_simple_sel", "LLR simple seleccionado"), ("llr_rezagos_sel", "LLR con rezagos seleccionado")):
            for corta, etapa in (("carga", "Carga de datos"), ("seleccion", "Selección conjunta de h y año de inicio (40 combinaciones)"), ("ajuste", "Ajuste final, predicción y escritura"), ("total", "Total")):
                r = r3[(met, "ll4b", corta)]
                t.filas.append([T(blq_llr), T(nom), T(etapa), g(R, f"costo.{met}.ll4b.{corta}.tiempo"), g(R, f"costo.{met}.ll4b.{corta}.seg"), T(_sust(str(r.hardware), _HW_SUST))])
            t.filas.append([T(blq_llr), T(f"TimesFM / {nom}"), T("Cociente de totales"), g(R, f"costo.{met}.ratio_timesfm_r"), (None, "—"), T("—")])
            t.filas.append([T(blq_llr), T(f"tuned / {nom}"), T("Cociente de totales"), g(R, f"costo.{met}.ratio_tuned_r"), (None, "—"), T("—")])
    prod = "Producto 2017–2020 (corridas no controladas)"
    fila(prod, "tuned", "Selección de recetas, producción 1981–2016", "tuned_prod_seleccion")
    fila(prod, "tuned", "Ajuste, producción 1981–2016", "tuned_prod_ajuste")
    total(prod, "tuned", "Selección y ajuste", "costo.producto.tuned_entrenamiento")
    fila(prod, "tuned", "Predicción 2017–2020", "tuned_producto_prediccion")
    fila(prod, "TimesFM", "Inferencia 2017–2020", "timesfm_producto_inferencia")
    t.filas.append([T(prod), T("TimesFM / tuned"), T("Cociente de inferencia"), g(R, "costo.producto.ratio_inferencia"), (None, "—"), T("—")])
    return t


def tab6_resumen(R: Registro, d: Datos) -> Tabla:
    """Versión corta de `tab6` para el cuerpo: bloque 2009–2012, por método; el detalle completo va en S7."""
    t = Tabla("tab6_resumen", ["Método", "Selección de configuración", "Ajuste o inferencia", "Total", "Hardware"], fuentes="costo.csv, costo.md, r3_costo_llr_sel.csv")
    gpu = "RTX A2000 12 GB"
    t.filas.append([T("tuned"), g(R, "costo.tuned_ll4b_seleccion.tiempo"), g(R, "costo.tuned_ll4b_ajuste.tiempo"), g(R, "costo.ll4b.tuned_total.tiempo"), T(gpu + " + CPU")])
    t.filas.append([T("TimesFM"), g(R, "costo.timesfm_cribado.tiempo"), g(R, "costo.timesfm_ll4b_inferencia.tiempo"), g(R, "costo.ll4b.timesfm_total.tiempo"), T(gpu)])
    if d.r3_costo is not None:
        cpu = "Intel Core i9-14900K, sin GPU"
        for met, nom in (("llr_simple_sel", "LLR simple seleccionado"), ("llr_rezagos_sel", "LLR con rezagos seleccionado")):
            t.filas.append([T(nom), g(R, f"costo.{met}.ll4b.seleccion.tiempo"), g(R, f"costo.{met}.ll4b.ajuste.tiempo"), g(R, f"costo.{met}.ll4b.total.tiempo"), T(cpu)])
    sin = (None, "—")
    t.filas.append([T("TimesFM / tuned (cociente de totales)"), sin, sin, g(R, "costo.ll4b.ratio_total_r"), T("—")])
    if d.r3_costo is not None:
        for met, nom in (("llr_simple_sel", "LLR simple seleccionado"), ("llr_rezagos_sel", "LLR con rezagos seleccionado")):
            t.filas.append([T(f"TimesFM / {nom} (cociente de totales)"), sin, sin, g(R, f"costo.{met}.ratio_timesfm_r"), T("—")])
    return t


# --- Suplemento -------------------------------------------------------------------------
def s1(R: Registro, d: Datos) -> Tabla:
    """Formato largo (una fila por bloque, ámbito y comparación): 8 columnas en lugar de 13."""
    t = Tabla("s1", ["Bloque", "Ámbito", "Comparación A − B", "RMSE de A", "RMSE de B", "Brecha (°C)", "IC espacial", "IC mes-año"],
              fuentes="a1_por_metodo.csv, a1_brechas.csv")
    comps = (("tuned", "tuned_sin_td", "tuned − tuned sin rezagos de Td"),
             ("tuned_sin_td", "llr_simple", "tuned sin rezagos de Td − LLR simple"),
             ("timesfm_anom", "tuned_sin_td", "TimesFM − tuned sin rezagos de Td"))
    for s in SPLITS:
        for a in AMBITOS:
            for x, y, rot in comps:
                t.filas.append(_blq_amb(s, a) + [T(rot), g(R, f"rmse.{s}.{a}.{alias(x)}"), g(R, f"rmse.{s}.{a}.{alias(y)}")]
                               + _fila_brecha(R, s, a, x, y))
    return t


def s1_anual(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s1_anual", ["Bloque", "Ámbito", "Año", "RMSE tuned", "RMSE tuned sin rezagos de Td", "tuned − tuned sin rezagos de Td (descriptiva)"], fuentes="a1_por_metodo.csv")
    for s in SPLITS:
        anios = [R.num(f"bloques.{s}.anio_ini") + i for i in range(int(R.num(f"bloques.{s}.n_anios")))]
        for a in AMBITOS:
            for y in anios:
                y = int(y)
                x1, x2 = R.num(f"rmse_anual.{s}.{a}.tuned.a{y}"), R.num(f"rmse_anual.{s}.{a}.tuned_sin_td.a{y}")
                t.filas.append(_blq_amb(s, a) + [T(str(y)), g(R, f"rmse_anual.{s}.{a}.tuned.a{y}"), g(R, f"rmse_anual.{s}.{a}.tuned_sin_td.a{y}"), N(x1 - x2, 3, True)])
    return t


def s1_victorias(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s1_victorias", ["Bloque", "Ámbito", "Zonas", "tuned sin rezagos de Td gana a tuned", "tuned sin rezagos de Td gana a LLR simple", "LLR simple gana a tuned sin rezagos de Td"], fuentes="a1_victorias_zona.csv")
    for s in SPLITS:
        for a in AMBITOS:
            n = R.texto(f"zonas.{s}.{a}.n_zonas")
            t.filas.append(_blq_amb(s, a) + [g(R, f"zonas.{s}.{a}.n_zonas")] + [
                (R.num(k), f"{R.texto(k)} de {n}") for k in (f"victorias.{s}.{a}.tuned_sin_td_vs_tuned", f"victorias.{s}.{a}.tuned_sin_td_vs_llr_simple", f"victorias.{s}.{a}.llr_simple_vs_tuned_sin_td")])
    return t


def s2(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s2", ["Método", "Objetivo", "Tmin", "Modo de barajado", "Semilla", "RMSE (°C)", "Habilidad vs climatología", "Sesgo (°C)"], fuentes="a3_control_tmin_barajada.csv (solo 2013–2016; el control no existe en 2009–2012)")
    met = {"clim": "climatología", "tuned": "tuned", "timesfm": "TimesFM"}
    obj = {"td": "Td cruda", "anom": "anomalía"}
    tmin = {"real": "observada", "barajada": "barajada"}
    modo = {"cell": "entre celdas", "year": "entre años"}

    def tx(dic, v):
        return T("—" if (isinstance(v, float) and v != v) else dic.get(str(v), str(v)))
    for r in d.a3.itertuples(index=False):
        sem = (float(r.semilla), str(int(r.semilla))) if r.semilla == r.semilla else (None, "—")
        t.filas.append([tx(met, r.metodo), tx(obj, r.variante), tx(tmin, r.tmin), tx(modo, r.modo), sem,
                        g(R, f"a3.{r.corrida}.rmse"), g(R, f"a3.{r.corrida}.skill"), g(R, f"a3.{r.corrida}.sesgo")])
    return t


ESC_TXT = {"clim": "climatología", "tuned": "tuned", "llr_simple": "LLR simple", "llr_rezagos": "LLR con rezagos", "timesfm": "TimesFM",
           "timesfm_clim_propia": "TimesFM con contexto y climatología desde 2002"}


def _esc_txt(m: str) -> str:
    """'timesfm@1991' -> 'TimesFM, inicio 1991'."""
    base, _, ini = m.partition("@")
    return f"{ESC_TXT.get(base, base)}, inicio {ini}" if ini else ESC_TXT.get(base, base)


def s3(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s3", ["Bloque", "Método", "Inicio del contexto", "Años de historial", "RMSE (°C)", "Cambio frente a inicio 1981 (°C)"], fuentes="a1_escalera_contexto.csv (panel de cribado, periodo = total)")
    e = d.escalera[d.escalera.periodo == "total"]
    for s in SPLITS:
        for r in e[e.split == s].sort_values(["metodo", "inicio"], key=lambda c: c.map({"clim": 0, "tuned": 1, "llr_simple": 2, "llr_rezagos": 3, "timesfm": 4, "timesfm_clim_propia": 5}) if c.name == "metodo" else c).itertuples(index=False):
            k = f"escalera.{s}.{r.metodo}.i{r.inicio}"
            t.filas.append([T(BLQ[s]), T(ESC_TXT.get(r.metodo, r.metodo)), T(str(r.inicio)), g(R, f"{k}.anios"), g(R, f"{k}.rmse"), g(R, f"{k}.delta")])
    return t


def s3_brechas(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s3_brechas", ["Bloque", "A", "B", "Brecha A − B (°C)", "IC espacial 2°", "IC mes-año"], fuentes="a1_escalera_contexto_brechas.csv")
    eb = d.esc_brechas
    for (s, a, b), _ in eb.groupby(["split", "metodo_a", "metodo_b"], sort=False):
        base = lambda q: f"escalera_brecha.{s}.{q}.{a.replace('@', '_')}_vs_{b.replace('@', '_')}"
        t.filas.append([T(BLQ[s]), T(_esc_txt(a)), T(_esc_txt(b)), g(R, base("mes_anio") + ".v"), g(R, base("espacial_2g") + ".ic"), g(R, base("mes_anio") + ".ic")])
    return t


def s4(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s4", ["Magnitud", "Fuente", "Período", "Estaciones", "Días-estación", "Sesgo (°C)", "RMSE (°C)", "MAE (°C)"], fuentes="a4_por_periodo.csv (muestra = productos; sin ERA5)")
    for r in d.a4_periodo.itertuples(index=False):
        k = f"a4.{r.kind}.{r.fuente}_{r.periodo.replace('-', '_')}"
        t.filas.append([T("Td" if r.kind == "td" else "anomalía de Td"), T(r.fuente), T(r.periodo), g(R, f"{k}.n_estaciones"), g(R, f"{k}.n_dias"),
                        g(R, f"{k}.sesgo"), g(R, f"{k}.rmse"), g(R, f"{k}.mae")])
    return t


def s4_delta(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s4_delta", ["Magnitud", "A − B", "Período", "ΔRMSE (°C)", "IC 95 %", "¿Excluye cero?", "Estaciones", "Días-estación"], fuentes="a4_delta_rmse_bootstrap.csv (muestra = productos)")
    for r in d.a4_boot.itertuples(index=False):
        k = f"a4.delta_rmse.{r.kind}.{alias(r.a)}_vs_{alias(r.b)}"
        t.filas.append([T("Td" if r.kind == "td" else "anomalía de Td"), T(f"{r.a} − {r.b}"), T(r.periodo), g(R, f"{k}.v"), g(R, f"{k}.ic"), g(R, f"{k}.excluye_cero"),
                        g(R, f"{k}.n_estaciones"), g(R, f"{k}.n_dias")])
    return t


def s5(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s5", ["Bloque", "Ámbito", "Método", "RMSE (°C)", "Brecha TimesFM − método (°C)", "IC espacial 2°", "IC mes-año"], fuentes="a1_por_metodo.csv, a1_brechas.csv")
    for s in SPLITS:
        for a in AMBITOS:
            for m in ("llr_simple", "llr_rezagos", "llr_simple_sel", "llr_rezagos_sel"):
                t.filas.append(_blq_amb(s, a) + [T(M_TXT[m]), g(R, f"rmse.{s}.{a}.{m}")] + _fila_brecha(R, s, a, "timesfm_anom", m))
    return t


def s6(R: Registro, d: Datos) -> Tabla:
    rivales = ("tuned", "tuned_sin_td", "llr_simple", "llr_rezagos", "llr_simple_sel", "llr_rezagos_sel")
    t = Tabla("s6", ["Bloque", "Ámbito", "Zonas"] + [f"TimesFM gana a {M_TXT[r]}" for r in rivales]
              + ["Brecha por zona vs tuned: más negativa", "Brecha por zona vs tuned: menos negativa"],
              fuentes="a1_victorias_zona.csv, a1_por_zona.csv (la magnitud acompaña siempre al conteo)")
    for s in SPLITS:
        for a in AMBITOS:
            n = R.texto(f"zonas.{s}.{a}.n_zonas")
            fila = _blq_amb(s, a) + [g(R, f"zonas.{s}.{a}.n_zonas")]
            for r in rivales:
                k = f"victorias.{s}.{a}.{par('timesfm_anom', r)}"
                fila.append((R.num(k), f"{R.texto(k)} de {n}"))
            fila += [g(R, f"zonas.{s}.{a}.vs_tuned.mas_negativa"), g(R, f"zonas.{s}.{a}.vs_tuned.menos_negativa")]
            t.filas.append(fila)
    return t


def s7(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s7", ["Método", "Bloque", "Etapa", "Celdas", "Segundos", "Tiempo", "Hardware", "Observaciones"], fuentes="costo.csv (todas las filas)", romper_ids=True)
    for cid, r in ci.costo_filas(d).items():
        t.filas.append([T(_METODO_TXT.get(str(r.metodo), str(r.metodo))), T(_BLOQUE_TXT.get(str(r.bloque), str(r.bloque))), T(str(r.etapa)),
                        g(R, f"costo.{cid}.celdas"), g(R, f"costo.{cid}.seg"), g(R, f"costo.{cid}.tiempo"), T(_sust(str(r.hardware), _HW_SUST)), T(_obs(r))])
    if d.r3_costo is not None:
        for (met, blq, corta), r in ci.r3_filas(d).items():
            k = f"costo.{met}.{blq}.{corta}"
            t.filas.append([T(_METODO_TXT.get(met, met)), T(_BLOQUE_TXT.get(blq, blq)), T(str(r.etapa)), g(R, f"{k}.celdas"), g(R, f"{k}.seg"), g(R, f"{k}.tiempo"),
                            T(_sust(str(r.hardware), _HW_SUST)), T(_obs(r))])
    return t


# --- Robustez de la inferencia (R1) y analisis descriptivos (R2) ---------------------------
RIV = ci.RIV
EXT_ROT = {"inferior_5": "5 % inferior", "superior_5": "5 % superior", "resto": "90 % central"}


def tab7_robustez(R: Registro, d: Datos) -> Tabla:
    t = Tabla("tab7_robustez", ["Bloque", "Ámbito", "Rival", "Brecha (°C)", "IC espacial 2°", "IC 2° × año", "IC trimestre-año",
                                "p de Holm, rezago 7", "p de Holm, rezago 30"],
              fuentes="r1_bootstrap_espaciotemporal.csv, r1_diebold_mariano.csv")
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIV:
                k = f"robustez.{s}.{a}.{r}"
                t.filas.append(_blq_amb(s, a) + [T(M_TXT[r]), g(R, f"{k}.v"), g(R, f"{k}.esp_ic"), g(R, f"{k}.esa_ic"), g(R, f"{k}.ta_ic"),
                                                  g(R, f"dm.{s}.{a}.{r}.lag7.p_holm"), g(R, f"dm.{s}.{a}.{r}.lag30.p_holm")])
    return t


def tab8_isd_estaciones(R: Registro, d: Datos) -> Tabla:
    """Sesgo y RMSE por estacion ISD en Td absoluta: PISCO (2009-2016) frente a tuned y TimesFM (2017-2020)."""
    t = Tabla("tab8_isd_estaciones",
              ["Estación (elevación, m)", "Días PISCO / 2017–2020",
               "Sesgo PISCO", "RMSE PISCO", "Sesgo tuned", "RMSE tuned", "Sesgo TimesFM", "RMSE TimesFM"],
              fuentes="a4_por_estacion.csv (muestra=productos, kind=td), a4_estaciones.csv")
    e = d.a4_estacion
    e = e[e.kind == "td"]
    src = {"pisco": "2009-2016", "palacios": "2017-2020", "timesfm": "2017-2020"}
    por = {f: e[(e.fuente == f) & (e.periodo == p)].set_index(e[(e.fuente == f) & (e.periodo == p)].station.astype(str)) for f, p in src.items()}
    est = d.a4_estaciones.set_index("station")
    orden = sorted(por["pisco"].index, key=lambda k: float(est.loc[k, "ELEV(M)"]))
    for k in orden:
        nom = f"{ci._nombre_estacion(est.loc[k, 'STATION NAME'])} ({fm.ent(est.loc[k, 'ELEV(M)'])})"
        n0 = fm.ent(por["pisco"].loc[k, "n_dias"])
        n1 = fm.ent(por["palacios"].loc[k, "n_dias"]) if k in por["palacios"].index else "—"
        fila = [T(nom), T(f"{n0} / {n1}")]
        for f in ("pisco", "palacios", "timesfm"):
            if k in por[f].index:
                fila += [N(por[f].loc[k, "sesgo"], 2, True), N(por[f].loc[k, "rmse"], 2)]
            else:
                fila += [T("—"), T("—")]
        t.filas.append(fila)
    return t


def s9_skill(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s9_skill", ["Bloque", "Ámbito", "Método", "Habilidad frente a climatología", "Razón de varianzas", "Correlación de anomalías"],
              fuentes="r2_skill.csv (la climatología tiene habilidad 0 por construcción y se omite)")
    for s in SPLITS:
        for a in AMBITOS:
            for m in ("timesfm_anom", *RIV):
                k = f"skill.{s}.{a}.{alias(m)}"
                t.filas.append(_blq_amb(s, a) + [T(M_TXT[m]), g(R, f"{k}.skill"), g(R, f"{k}.razon_varianza"), g(R, f"{k}.corr")])
    return t


def s10_extremos(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s10_extremos", ["Bloque", "Ámbito", "Clase", "Método", "RMSE (°C)", "Sesgo (°C)", "Brecha TimesFM − método (°C)"],
              fuentes="r2_extremos.csv (clases por celda: 5 % inferior y superior de la anomalía observada)")
    for s in SPLITS:
        for a in AMBITOS:
            for c in ci.CLASE_EXT:
                for m in ("timesfm_anom", *RIV):
                    k = f"extremos.{s}.{a}.{ci.CLASE_EXT[c]}"
                    brecha = (T("—") if m == "timesfm_anom" else g(R, f"{k}.brecha.{m}"))
                    t.filas.append(_blq_amb(s, a) + [T(EXT_ROT[c]), T(M_TXT[m]), g(R, f"{k}.{alias(m)}.rmse"), g(R, f"{k}.{alias(m)}.sesgo"), brecha])
    return t


def s11_calibracion(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s11_calibracion", ["Bloque", "Ámbito", "Periodo", "Filas", "Cobertura del intervalo 80 % (%)", "Anchura media (°C)", "CRPS aproximado (°C)",
                                  "Bajo q10 (%)", "Sobre q90 (%)"], fuentes="r2_calibracion.csv (solo TimesFM; nominal: 80 % de cobertura y 10 % por cola)")
    for s in SPLITS:
        for a in AMBITOS:
            pers = ["total"] + [f"a{y}" for y in range(int(R.num(f"bloques.{s}.anio_ini")), int(R.num(f"bloques.{s}.anio_fin")) + 1)]
            for p in pers:
                k = f"calib.{s}.{a}.{p}"
                t.filas.append(_blq_amb(s, a) + [T("Total" if p == "total" else p[1:]), g(R, f"{k}.n"), g(R, f"{k}.cobertura"), g(R, f"{k}.anchura"),
                                                  g(R, f"{k}.crps"), g(R, f"{k}.frac_bajo_q10"), g(R, f"{k}.frac_sobre_q90")])
    return t


def s12_altitud(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s12_altitud", ["Bloque", "Ámbito", "Banda de altitud", "Celdas", "RMSE de TimesFM (°C)"] + [f"Brecha frente a {M_TXT[r]} (°C)" for r in RIV],
              fuentes="r2_estratos_altitud.csv (DEM; las cinco bandas suman las celdas del ámbito)")
    for s in SPLITS:
        for a in AMBITOS:
            for e in ("0-500", "500-1500", "1500-2500", "2500-3500", ">3500"):
                k = f"altitud.{s}.{a}.{ci.BANDAS[e]}"
                t.filas.append(_blq_amb(s, a) + [T(ci.BANDA_TXT[e]), g(R, f"{k}.celdas"), g(R, f"{k}.rmse.timesfm")] + [g(R, f"{k}.brecha.{r}") for r in RIV])
    return t


def s13_enso(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s13_enso", ["Bloque", "Ámbito", "Clase ENSO", "Meses", "RMSE de TimesFM (°C)", "Sesgo de TimesFM (°C)"] + [f"Brecha frente a {M_TXT[r]} (°C)" for r in RIV],
              fuentes="r2_enso.csv (ONI ≥ 0,5 El Niño; ≤ −0,5 La Niña; trimestre móvil en su mes central)")
    for s in SPLITS:
        for a in AMBITOS:
            for c in ci.ENSO_TXT:
                k = f"enso.{s}.{a}.{c}"
                t.filas.append(_blq_amb(s, a) + [T(ci.ENSO_TXT[c]), g(R, f"{k}.meses"), g(R, f"{k}.rmse.timesfm"), g(R, f"{k}.sesgo.timesfm")]
                               + [g(R, f"{k}.brecha.{r}") for r in RIV])
    return t


def s14_zona_dominante(R: Registro, d: Datos) -> Tabla:
    t = Tabla("s14_zona_dominante", ["Bloque", "Ámbito", "Zona dominante", "Celdas de la zona (%)", "Rival", "Brecha total (°C)", "Brecha dentro de la zona (°C)", "Brecha sin la zona (°C)"],
              fuentes="r2_sin_zona_dominante.csv (zona con más celdas del ámbito)")
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIV:
                k = f"zdom.{s}.{a}"
                t.filas.append(_blq_amb(s, a) + [g(R, f"{k}.etiqueta"), g(R, f"{k}.pct_celdas"), T(M_TXT[r]),
                                                  g(R, f"{k}.brecha.{r}.total"), g(R, f"{k}.brecha.{r}.zona"), g(R, f"{k}.brecha.{r}.sin_zona")])
    return t


CONSTRUCTORES = {f.__name__: f for f in (tab1, tab1_insumos, tab2, tab3, tab4, tab5, tab6, tab6_resumen, s1, s1_anual, s1_victorias, s2, s3, s3_brechas, s4, s4_delta, s5, s6, s7,
                                              tab7_robustez, tab8_isd_estaciones, s9_skill, s10_extremos, s11_calibracion, s12_altitud, s13_enso, s14_zona_dominante)}


def construir(R: Registro | None = None, d: Datos | None = None) -> dict[str, Tabla]:
    d = d or cargar()
    R = R or ci.construir(d)
    out = {tid: CONSTRUCTORES[tid](R, d) for tid in TABLE_IDS}
    for tid, t in out.items():
        assert t.id == tid and t.filas, tid
    return out


def escribir(destino: Path | None = None) -> dict[str, Tabla]:
    destino = destino or F.TABLAS_DIR
    tablas = construir()
    destino.mkdir(parents=True, exist_ok=True)
    for tid, t in tablas.items():
        (destino / f"{tid}.md").write_text(t.md(), encoding="utf-8")
        (destino / f"{tid}.csv").write_text(t.csv(), encoding="utf-8")
    if destino == F.TABLAS_DIR:
        salidas = [F.rel(destino / f"{tid}.csv") for tid in TABLE_IDS]
        ci.registrar_proveniencia(
            salidas, "paper_nuevo_tablas",
            "Tablas Tab1-Tab7 y S1-S7, S9-S14 del paper nuevo generadas por experiments/paper_nuevo/tablas.py desde las claves de cifras.py.",
            sorted({a for f in ci.construir().filas.values() for a in f["fuente_archivo"].split("; ") if a.startswith("reports/")}))
    log.info("%d tablas en %s", len(tablas), destino)
    return tablas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    escribir()
