"""Calcula TODA cifra que cita el paper nuevo desde los CSV de resultados.

Salidas:
- ``reports/paper_nuevo/_variables.yml``: variables de Quarto (``{{< var rmse.ll4b.panel.timesfm >}}``).
- ``reports/paper_nuevo/cifras/cifras.csv``: clave, valor_num, valor_texto, fuente, filtro, nota.
- ``reports/paper_nuevo/cifras/CLAVES.md``: lista legible de claves para quien redacta.

Convencion de signo: brecha = RMSE(A) - RMSE(B); negativa favorece a A (TimesFM).
Lo que no existe en las fuentes se registra como "n. d." con una nota; nunca se inventa.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from experiments.paper_nuevo import fuentes as F
from experiments.paper_nuevo import formato as fm
from experiments.paper_nuevo.datos import AMBITO_TXT, AMBITOS, SPLITS, Datos, cargar

log = logging.getLogger(__name__)

ALIAS = {"timesfm_anom": "timesfm", "timesfm_anom_med": "timesfm_med"}
NOMBRE = {
    "clim": "climatología", "tuned": "tuned", "tuned_sin_td": "tuned sin rezagos de Td",
    "llr_simple": "LLR simple", "llr_rezagos": "LLR con rezagos", "llr_simple_sel": "LLR simple seleccionado",
    "llr_rezagos_sel": "LLR con rezagos seleccionado", "timesfm_anom": "TimesFM",
    "timesfm_td": "TimesFM en Td cruda", "timesfm_anom_med": "TimesFM con contexto desde 2002",
}


def alias(m: str) -> str:
    return ALIAS.get(m, m)


def par(a: str, b: str) -> str:
    return f"{alias(a)}_vs_{alias(b)}"


def lista_es(items: list[str]) -> str:
    items = [str(i) for i in items]
    if not items:
        return "ninguno"
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " y " + items[-1]


BLOQUE_TXT = {"ll4b": "2009–2012", "ll4": "2013–2016"}


def _en(s: str, a: str) -> str:
    """«2009–2012 en Perú» / «2013–2016 en el dominio completo» (lectura en prosa de un caso bloque × ámbito)."""
    return f"{BLOQUE_TXT.get(s, s)} en " + ("Perú" if a == "peru" else "el dominio completo")


def si_no(x: bool) -> str:
    return "sí" if x else "no"


@dataclass
class Registro:
    filas: dict[str, dict] = field(default_factory=dict)
    verificaciones: list[tuple[str, bool]] = field(default_factory=list)

    def add(self, clave: str, valor: float | None, texto: str, archivo: str, filtro: str,
            desc: str, nota: str = "") -> str:
        if clave in self.filas:
            raise KeyError(f"clave duplicada: {clave}")
        self.filas[clave] = dict(clave=clave, valor_num=None if valor is None else float(valor),
                                 valor_texto=texto, fuente_archivo=archivo, fuente_filtro=filtro,
                                 nota=nota, descripcion=desc)
        return texto

    def nd(self, clave: str, archivo: str, filtro: str, desc: str, nota: str) -> None:
        self.add(clave, None, fm.ND, archivo, filtro, desc, nota)

    def verificar(self, desc: str, ok: bool) -> None:
        self.verificaciones.append((desc, bool(ok)))
        if not ok:
            log.warning("verificacion fallida: %s", desc)

    def texto(self, clave: str) -> str:
        return self.filas[clave]["valor_texto"]

    def num(self, clave: str) -> float | None:
        return self.filas[clave]["valor_num"]


def _src(*paths: Path) -> str:
    return "; ".join(F.rel(p) for p in paths)


# ---------------------------------------------------------------------------------------
def _conteos(R: Registro, d: Datos) -> None:
    A = F.rel(F.A1_POR_METODO)
    m = d.metodo
    tot = m[(m.periodo == "total") & (m.metodo == "clim")].set_index(["split", "ambito"])
    for s in SPLITS:
        for a in AMBITOS:
            r = tot.loc[(s, a)]
            R.add(f"filas.{s}.{a}", r.n, fm.ent(r.n), A, f"split={s}; ambito={a}; metodo=clim; periodo=total; col=n",
                  f"Filas celda × día puntuadas en `{s}`, {AMBITO_TXT[a]}")
            R.add(f"celdas.{s}.{a}", r.celdas, fm.ent(r.celdas), A,
                  f"split={s}; ambito={a}; metodo=clim; periodo=total; col=celdas", f"Celdas puntuadas en `{s}`, {AMBITO_TXT[a]}")
    celdas = int(tot.loc[("ll4b", "panel")].celdas)
    peru = int(tot.loc[("ll4b", "peru")].celdas)
    R.verificar("celdas del panel iguales en ll4 y ll4b y = filas de nacional_17027.csv",
                celdas == int(tot.loc[("ll4", "panel")].celdas) == len(d.panel))
    R.add("panel.celdas", celdas, fm.ent(celdas), A, "ambito=panel; col=celdas", "Celdas puntuadas del dominio completo (panel)")
    R.add("panel.celdas_peru", peru, fm.ent(peru), A, "ambito=peru; col=celdas", "Celdas del panel dentro del contorno de Perú")
    R.add("panel.celdas_fuera", celdas - peru, fm.ent(celdas - peru), A, "panel.celdas - panel.celdas_peru",
          "Celdas del panel fuera de Perú")
    R.add("panel.pct_fuera", 100 * (celdas - peru) / celdas, fm.num(100 * (celdas - peru) / celdas, 1), A,
          "100 × (panel - peru) / panel", "Porcentaje del panel fuera de Perú (sin símbolo %)")
    R.add("panel.dias_por_celda", tot.loc[("ll4b", "panel")].n / celdas, fm.ent(tot.loc[("ll4b", "panel")].n / celdas), A,
          "n / celdas, ll4b panel", "Días evaluados por celda en cada bloque")
    # Zonas
    zp = d.panel.zone_id.nunique()
    R.add("panel.zonas_panel", zp, fm.ent(zp), F.rel(F.PANEL_NACIONAL), "nunique(zone_id)", "Unidades cartográficas con celdas en el panel")
    zz = d.zona.groupby(["split", "ambito"]).zone_id.nunique()
    R.verificar("zonas del panel: panel CSV = a1_por_zona", int(zz.loc[("ll4b", "panel")]) == zp)
    zpe = int(zz.loc[("ll4b", "peru")])
    R.add("panel.zonas_peru", zpe, fm.ent(zpe), F.rel(F.A1_POR_ZONA), "ambito=peru; nunique(zone_id)", "Unidades cartográficas con celdas dentro de Perú")
    z_panel = set(d.zona[d.zona.ambito == "panel"].zone_label)
    z_peru = set(d.zona[d.zona.ambito == "peru"].zone_label)
    R.add("panel.zonas_sin_peru", len(z_panel - z_peru), fm.ent(len(z_panel - z_peru)), F.rel(F.A1_POR_ZONA),
          "zonas del panel sin celdas en peru", "Zonas del panel sin celdas dentro de Perú",
          nota="etiquetas: " + lista_es(sorted(z_panel - z_peru)))
    zt = d.zone_table_labels
    zf = F.rel(F.zone_table_path()) if F.zone_table_path() else "$RES/zone_table.parquet"
    if zt is None:
        for k in ("unidades_total", "tipos_climaticos", "unidades_extra"):
            R.nd(f"panel.{k}", zf, "zone_table.parquet", "Conteo de unidades cartográficas SENAMHI",
                 "zone_table.parquet ($RES) no disponible en esta máquina")
    else:
        extra = [z for z in zt if z.startswith("Lago") or z == "Loma"]
        R.add("panel.unidades_total", len(zt), fm.ent(len(zt)), zf, "nunique(zone_label)", "Unidades cartográficas SENAMHI (zone_table)")
        R.add("panel.unidades_extra", len(extra), fm.ent(len(extra)), zf, "zone_label que empieza con 'Lago' o es 'Loma'",
              "Unidades adicionales (lagos y lomas costeras)", nota="etiquetas: " + lista_es(extra))
        R.add("panel.tipos_climaticos", len(zt) - len(extra), fm.ent(len(zt) - len(extra)), zf,
              "unidades_total - unidades_extra", "Tipos climáticos (incluye 'Glaciar')")
    # Bloques
    esc = d.escalera
    for s in SPLITS:
        anios = sorted(int(p) for p in m[(m.split == s)].periodo.unique() if p != "total")
        fe = F.rel(F.A1_POR_METODO)
        R.add(f"bloques.{s}.anio_ini", anios[0], str(anios[0]), fe, f"split={s}; min(periodo)", f"Primer año de prueba de `{s}`")
        R.add(f"bloques.{s}.anio_fin", anios[-1], str(anios[-1]), fe, f"split={s}; max(periodo)", f"Último año de prueba de `{s}`")
        R.add(f"bloques.{s}.n_anios", len(anios), str(len(anios)), fe, f"split={s}; nunique(periodo != total)", f"Años de prueba de `{s}`")
        e1 = esc[(esc.split == s) & (esc.metodo == "timesfm") & (esc.inicio == 1981)].iloc[0]
        fe2 = F.rel(F.A1_ESCALERA)
        R.add(f"bloques.{s}.contexto_ini", int(e1.inicio), str(int(e1.inicio)), fe2, f"split={s}; metodo=timesfm; inicio=1981", f"Primer año de contexto de `{s}`")
        R.add(f"bloques.{s}.contexto_fin", int(e1.clim_fin), str(int(e1.clim_fin)), fe2, f"split={s}; clim_fin", f"Último año de contexto de `{s}`")
        R.add(f"bloques.{s}.anios_contexto", int(e1.anios_historial), str(int(e1.anios_historial)), fe2, f"split={s}; anios_historial",
              f"Años de contexto de la referencia de TimesFM en `{s}`")
        R.verificar(f"{s}: contexto_fin + 1 = primer año de prueba", int(e1.clim_fin) + 1 == anios[0])
    todos = sorted({int(p) for p in m.periodo.unique() if p != "total"})
    R.add("bloques.n_anios_total", len(todos), str(len(todos)), A, "nunique(periodo != total), ambos splits", "Años evaluados en total")
    R.add("bloques.anio_min", todos[0], str(todos[0]), A, "min(periodo)", "Primer año evaluado")
    R.add("bloques.anio_max", todos[-1], str(todos[-1]), A, "max(periodo)", "Último año evaluado")
    # Bootstrap
    pb = F.rel(F.A1_BRECHAS_PROV)
    R.add("bootstrap.replicas", d.replicas, fm.ent(d.replicas), pb, "notes: 'bootstrap N replicas'", "Réplicas del bootstrap pareado")
    R.add("bootstrap.semilla", d.semilla, str(d.semilla), pb, "notes: 'semilla'", "Semilla del bootstrap")
    R.add("bootstrap.bloque_grados", d.bloque_grados, fm.num(d.bloque_grados, 0), pb, "notes: 'bloques espaciales de G grados'",
          "Lado (°) de los bloques espaciales")
    b = d.brechas
    for esq, nom in (("espacial_2g", "espacial"), ("mes_anio", "mes_anio")):
        for a in AMBITOS:
            nb = b[(b.esquema == esq) & (b.ambito == a)].bloques.unique()
            R.verificar(f"número de bloques único en {esq}/{a}", len(nb) == 1)
            R.add(f"bootstrap.bloques.{nom}.{a}", nb[0], fm.ent(nb[0]), F.rel(F.A1_BRECHAS), f"esquema={esq}; ambito={a}; col=bloques",
                  f"Bloques del esquema {nom} en {AMBITO_TXT[a]}")


def _metricas(R: Registro, d: Datos) -> None:
    A = F.rel(F.A1_POR_METODO)
    m = d.metodo
    for r in m.itertuples(index=False):
        k = f"{r.split}.{r.ambito}.{alias(r.metodo)}"
        flt = f"split={r.split}; ambito={r.ambito}; metodo={r.metodo}; periodo={r.periodo}"
        nom = NOMBRE.get(r.metodo, r.metodo)
        ctx = f"{nom}, `{r.split}`, {AMBITO_TXT[r.ambito]}"
        if r.periodo == "total":
            R.add(f"rmse.{k}", r.rmse, fm.num(r.rmse), A, flt + "; col=rmse", f"RMSE (°C), {ctx}")
            R.add(f"rmse4.{k}", r.rmse, fm.num(r.rmse, 4), A, flt + "; col=rmse", f"RMSE (°C) con 4 decimales, {ctx}")
            R.add(f"mae.{k}", r.mae, fm.num(r.mae), A, flt + "; col=mae", f"MAE (°C), {ctx}")
            R.add(f"sesgo.{k}", r.sesgo, fm.num(r.sesgo, 3, True), A, flt + "; col=sesgo", f"Sesgo (°C), {ctx}")
            R.add(f"rmse_macro.{k}", r.rmse_macro_zona, fm.num(r.rmse_macro_zona), A, flt + "; col=rmse_macro_zona",
                  f"RMSE macro por zona (°C), {ctx}")
        else:
            R.add(f"rmse_anual.{k}.a{r.periodo}", r.rmse, fm.num(r.rmse), A, flt + "; col=rmse", f"RMSE (°C) del año {r.periodo}, {ctx}")
            R.add(f"sesgo_anual.{k}.a{r.periodo}", r.sesgo, fm.num(r.sesgo, 3, True), A, flt + "; col=sesgo",
                  f"Sesgo (°C) del año {r.periodo}, {ctx}")
    # Conteo de casos de mayor sesgo absoluto de TimesFM frente a tuned
    t = m[m.periodo == "total"].set_index(["split", "ambito", "metodo"])
    casos, mayor = [], []
    for s in SPLITS:
        for a in AMBITOS:
            sf, st = t.loc[(s, a, "timesfm_anom")].sesgo, t.loc[(s, a, "tuned")].sesgo
            ok = abs(sf) > abs(st)
            casos.append((s, a))
            if ok:
                mayor.append(_en(s, a))
            R.add(f"sesgo_conteo.{s}.{a}.timesfm_mayor_abs", int(ok), si_no(ok), A,
                  f"|sesgo timesfm_anom| > |sesgo tuned|; split={s}; ambito={a}", f"¿El sesgo de TimesFM es mayor en magnitud que el de `tuned`? ({s}, {AMBITO_TXT[a]})")
    R.add("sesgo_conteo.n_mayor", len(mayor), str(len(mayor)), A, "suma de los 4 casos", "Casos (de 4) en que |sesgo TimesFM| > |sesgo tuned|")
    R.add("sesgo_conteo.n_casos", len(casos), str(len(casos)), A, "split × ambito", "Casos comparados (bloque × ámbito)")
    R.add("sesgo_conteo.casos_mayor", len(mayor), lista_es(mayor), A, "casos con |sesgo TimesFM| > |sesgo tuned|", "Lista de casos con mayor sesgo absoluto de TimesFM")
    menor = [_en(s, a) for s, a in casos if _en(s, a) not in mayor]
    R.add("sesgo_conteo.casos_menor", len(menor), lista_es(menor), A, "complemento", "Casos con |sesgo TimesFM| <= |sesgo tuned|")
    # TimesFM menor RMSE que todos los demas en cada bloque x ambito
    nmin = 0
    for s in SPLITS:
        for a in AMBITOS:
            sub = t.loc[(s, a)].rmse
            nmin += int(sub.idxmin() == "timesfm_anom")
    R.add("rmse_min.n_casos_timesfm_menor", nmin, str(nmin), A, "idxmin(rmse) == timesfm_anom, 4 casos",
          "Casos (de 4) en que TimesFM `tmin_anom_full` tiene el menor RMSE entre todos los métodos")
    # 2013 / inversion y brechas anuales
    _anual(R, d)


def _anual(R: Registro, d: Datos) -> None:
    A = F.rel(F.A1_POR_METODO)
    m = d.metodo.set_index(["split", "ambito", "metodo", "periodo"])
    pares = [("timesfm_anom", "tuned"), ("timesfm_anom", "llr_rezagos_sel"), ("timesfm_anom", "tuned_sin_td")]
    for s in SPLITS:
        anios = sorted(int(p) for p in d.metodo[d.metodo.split == s].periodo.unique() if p != "total")
        for a in AMBITOS:
            for (x, y) in pares + ([("timesfm_td", "tuned")] if s == "ll4b" else []):
                g = {}
                for yr in anios:
                    g[yr] = m.loc[(s, a, x, str(yr))].rmse - m.loc[(s, a, y, str(yr))].rmse
                    R.add(f"brecha_anual.{s}.{a}.{par(x, y)}.a{yr}", g[yr], fm.num(g[yr], 3, True), A,
                          f"RMSE({x}) - RMSE({y}); split={s}; ambito={a}; periodo={yr}",
                          f"Brecha anual RMSE({NOMBRE[x]}) − RMSE({NOMBRE[y]}), {yr}, `{s}`, {AMBITO_TXT[a]} (descriptiva, sin IC)")
                if (x, y) not in pares[:2]:
                    continue
                tot = m.loc[(s, a, x, "total")].rmse - m.loc[(s, a, y, "total")].rmse
                pos = [yr for yr in anios if g[yr] > 0]
                mejor = [yr for yr in anios if g[yr] < tot]
                k = f"anual_resumen.{s}.{a}.{par(x, y)}"
                flt = f"split={s}; ambito={a}; {x} - {y} por año"
                R.add(f"{k}.n_negativas", sum(v < 0 for v in g.values()), str(sum(v < 0 for v in g.values())), A, flt, "Años con brecha negativa (favorece a TimesFM)")
                R.add(f"{k}.n_anios", len(anios), str(len(anios)), A, flt, "Años comparados")
                R.add(f"{k}.todas_negativas", int(not pos), si_no(not pos), A, flt, "¿Todas las brechas anuales son negativas?")
                R.add(f"{k}.anios_positivos", len(pos), lista_es(pos), A, flt, "Años con brecha positiva (TimesFM peor)")
                R.add(f"{k}.anios_mayor_ventaja", len(mejor), lista_es(mejor), A,
                      flt + "; años con brecha más negativa que la brecha agregada del bloque",
                      "Años en que la ventaja de TimesFM supera la brecha agregada del bloque")
                yb = min(g, key=g.get)
                R.add(f"{k}.anio_mejor", yb, str(yb), A, flt, "Año con la brecha más negativa")
                R.add(f"{k}.brecha_mejor", g[yb], fm.num(g[yb], 3, True), A, flt, "Brecha del año con la brecha más negativa")
    # Inversion de 2013
    n_pos = 0
    for s in SPLITS:
        for a in AMBITOS:
            for yr in sorted(int(p) for p in d.metodo[d.metodo.split == s].periodo.unique() if p != "total"):
                n_pos += int(m.loc[(s, a, "timesfm_anom", str(yr))].rmse > m.loc[(s, a, "tuned", str(yr))].rmse)
    R.add("inversion.n_casos_vs_tuned", n_pos, str(n_pos), A, "TimesFM peor que tuned, por split × ámbito × año (16 casos)",
          "Casos (bloque × ámbito × año) en que TimesFM tiene mayor RMSE que `tuned`")
    for key, who, yr in (("2013", "ll4", "2013"),):
        R.add("inversion.anio", int(yr), yr, A, "año con brecha > 0 en ll4 panel", "Año en que se invierte el orden frente a `tuned` (dominio completo)")
        R.add("inversion.gap_tuned", m.loc[(who, "panel", "timesfm_anom", yr)].rmse - m.loc[(who, "panel", "tuned", yr)].rmse,
              fm.num(m.loc[(who, "panel", "timesfm_anom", yr)].rmse - m.loc[(who, "panel", "tuned", yr)].rmse, 3, True), A,
              f"{who} panel {yr}", "Brecha TimesFM − `tuned` en 2013, dominio completo")
        R.add("inversion.gap_llr_rezagos_sel", m.loc[(who, "panel", "timesfm_anom", yr)].rmse - m.loc[(who, "panel", "llr_rezagos_sel", yr)].rmse,
              fm.num(m.loc[(who, "panel", "timesfm_anom", yr)].rmse - m.loc[(who, "panel", "llr_rezagos_sel", yr)].rmse, 3, True), A,
              f"{who} panel {yr}", "Brecha TimesFM − `llr_rezagos_sel` en 2013, dominio completo")
        R.add("inversion.sesgo_timesfm", m.loc[(who, "panel", "timesfm_anom", yr)].sesgo, fm.num(m.loc[(who, "panel", "timesfm_anom", yr)].sesgo, 3, True), A,
              f"{who} panel {yr}", "Sesgo de TimesFM en 2013, dominio completo")
        R.add("inversion.sesgo_tuned", m.loc[(who, "panel", "tuned", yr)].sesgo, fm.num(m.loc[(who, "panel", "tuned", yr)].sesgo, 3, True), A,
              f"{who} panel {yr}", "Sesgo de `tuned` en 2013, dominio completo")
        R.add("inversion.solo_panel", int(m.loc[(who, "peru", "timesfm_anom", yr)].rmse < m.loc[(who, "peru", "tuned", yr)].rmse),
              si_no(m.loc[(who, "peru", "timesfm_anom", yr)].rmse < m.loc[(who, "peru", "tuned", yr)].rmse), A, f"{who} peru {yr}",
              "¿En Perú TimesFM sigue por debajo de `tuned` en 2013?")


def _brechas(R: Registro, d: Datos) -> None:
    B = F.rel(F.A1_BRECHAS)
    for (s, a, x, y), g in d.brechas.groupby(["split", "ambito", "metodo_a", "metodo_b"], sort=False):
        e = g.set_index("esquema")
        R.verificar(f"brecha puntual idéntica entre esquemas: {s} {a} {x} {y}", abs(e.brecha.iloc[0] - e.brecha.iloc[1]) < 1e-9)
        v = float(e.brecha.iloc[0])
        k = f"brecha.{s}.{a}.{par(x, y)}"
        flt = f"split={s}; ambito={a}; metodo_a={x}; metodo_b={y}"
        ctx = f"RMSE({NOMBRE.get(x, x)}) − RMSE({NOMBRE.get(y, y)}), `{s}`, {AMBITO_TXT[a]}"
        R.add(f"{k}.v", v, fm.num(v, 3, True), B, flt + "; col=brecha", f"Brecha (°C) {ctx}")
        R.add(f"{k}.abs", abs(v), fm.num(abs(v), 3), B, flt + "; col=brecha", f"Magnitud de la brecha (°C) {ctx}")
        for esq, p in (("espacial_2g", "esp"), ("mes_anio", "ma")):
            lo, hi = float(e.ic_lo[esq]), float(e.ic_hi[esq])
            R.add(f"{k}.{p}_lo", lo, fm.num(lo, 3, True), B, flt + f"; esquema={esq}; col=ic_lo", f"Límite inferior IC 95 % {esq}, {ctx}")
            R.add(f"{k}.{p}_hi", hi, fm.num(hi, 3, True), B, flt + f"; esquema={esq}; col=ic_hi", f"Límite superior IC 95 % {esq}, {ctx}")
            R.add(f"{k}.{p}_ic", None, fm.ic(lo, hi), B, flt + f"; esquema={esq}", f"IC 95 % {esq} como texto, {ctx}")
            excl = not (lo <= 0 <= hi)
            R.add(f"{k}.{p}_excluye_cero", int(excl), si_no(excl), B, flt + f"; esquema={esq}", f"¿El IC {esq} excluye cero? {ctx}")
            R.add(f"{k}.{p}_bloques_a_gana", int(e.bloques_a_gana[esq]), fm.ent(e.bloques_a_gana[esq]), B, flt + f"; esquema={esq}; col=bloques_a_gana",
                  f"Bloques (de {int(e.bloques[esq])}) en que A gana, {esq}, {ctx}")
        both = (not (e.ic_lo['espacial_2g'] <= 0 <= e.ic_hi['espacial_2g'])) and (not (e.ic_lo['mes_anio'] <= 0 <= e.ic_hi['mes_anio']))
        R.add(f"{k}.ambos_excluyen_cero", int(both), si_no(both), B, flt, f"¿Los dos IC excluyen cero? {ctx}")
    # Conteos: en cuantos de los 4 casos (bloque x ambito) ambos IC excluyen cero
    for rival in ("tuned", "llr_rezagos_sel", "tuned_sin_td", "llr_simple", "llr_simple_sel", "llr_rezagos"):
        n, casos, nuevo = 0, [], []
        for s in SPLITS:
            for a in AMBITOS:
                k = f"brecha.{s}.{a}.{par('timesfm_anom', rival)}.ambos_excluyen_cero"
                if k in R.filas:
                    ok = R.num(k) == 1
                    n += int(ok)
                    (casos if ok else nuevo).append(_en(s, a))
        k = f"brecha_conteo.timesfm_vs_{rival}"
        R.add(f"{k}.n_excluyen", n, str(n), B, f"timesfm_anom vs {rival}: casos con ambos IC sin cero", f"Casos (de 4) en que los dos IC excluyen cero, TimesFM vs {NOMBRE[rival]}")
        R.add(f"{k}.excluyen", n, lista_es(casos), B, "idem", "Casos con ambos IC sin cero")
        R.add(f"{k}.incluyen", len(nuevo), lista_es(nuevo), B, "idem", "Casos en que algún IC incluye cero")
    # LLR sin zonas con IC espacial / mes-año que excluyen cero en ll4, dominio completo (suplemento, LLR no seleccionados y seleccionados)
    llr_rivales = ("llr_simple", "llr_rezagos", "llr_simple_sel", "llr_rezagos_sel")
    esp_ok = [r for r in llr_rivales if R.num(f"brecha.ll4.panel.{par('timesfm_anom', r)}.esp_excluye_cero") == 1]
    ma_ok = [r for r in llr_rivales if R.num(f"brecha.ll4.panel.{par('timesfm_anom', r)}.ma_excluye_cero") == 1]
    R.add("brecha_conteo.llr_ll4_panel.esp_excluyen", len(esp_ok), lista_es([NOMBRE[r] for r in esp_ok]), B, "ll4; panel; esquema=espacial_2g; IC sin cero",
          "LLR sin zonas frente a los que el IC espacial excluye cero (`ll4`, dominio completo)")
    R.add("brecha_conteo.llr_ll4_panel.n_ma_excluyen", len(ma_ok), str(len(ma_ok)), B, "ll4; panel; esquema=mes_anio; IC sin cero",
          "Número de LLR sin zonas (de 4) frente a los que el IC mes-año excluye cero (`ll4`, dominio completo)")
    R.add("brecha_conteo.llr_ll4_panel.n_esp_excluyen", len(esp_ok), str(len(esp_ok)), B, "ll4; panel; esquema=espacial_2g; IC sin cero",
          "Número de LLR sin zonas (de 4) frente a los que el IC espacial excluye cero (`ll4`, dominio completo)")
    # Brechas inexistentes
    for a in AMBITOS:
        for rival in ("llr_rezagos_sel", "tuned"):
            R.nd(f"brecha.ll4b.{a}.timesfm_td_vs_{rival}.ic", B, f"metodo_a=timesfm_td; metodo_b={rival}; ambito={a}",
                 f"IC de TimesFM en Td cruda frente a `{rival}` ({AMBITO_TXT[a]})", "no se calculó IC; solo diferencia puntual de RMSE")
        pt = float(d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "timesfm_td")].rmse.iloc[0]
                   - d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "llr_rezagos_sel")].rmse.iloc[0])
        R.add(f"puntual.ll4b.{a}.timesfm_td_vs_llr_rezagos_sel", pt, fm.num(pt, 3, True), F.rel(F.A1_POR_METODO),
              f"RMSE(timesfm_td) - RMSE(llr_rezagos_sel); ll4b; {a}", "Diferencia puntual (sin IC) Td cruda − `llr_rezagos_sel`")
        pt2 = float(d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "timesfm_td")].rmse.iloc[0]
                    - d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "tuned")].rmse.iloc[0])
        R.add(f"puntual.ll4b.{a}.timesfm_td_vs_tuned", pt2, fm.num(pt2, 3, True), F.rel(F.A1_POR_METODO),
              f"RMSE(timesfm_td) - RMSE(tuned); ll4b; {a}", "Diferencia puntual (sin IC) Td cruda − `tuned`",
              nota="a1_brechas.csv no tiene IC para esta pareja")
        pt3 = float(d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "timesfm_anom")].rmse.iloc[0]
                    - d.metodo[(d.metodo.split == "ll4b") & (d.metodo.ambito == a) & (d.metodo.periodo == "total") & (d.metodo.metodo == "timesfm_td")].rmse.iloc[0])
        R.add(f"puntual.ll4b.{a}.timesfm_vs_timesfm_td", pt3, fm.num(pt3, 3, True), F.rel(F.A1_POR_METODO),
              f"RMSE(timesfm_anom) - RMSE(timesfm_td); ll4b; {a}", "Diferencia puntual (sin IC) TimesFM `tmin_anom_full` − Td cruda (signo opuesto al de `puntual.*.timesfm_td_vs_*`)",
              nota="a1_brechas.csv no tiene IC para esta pareja")
        R.nd(f"brecha.ll4.{a}.timesfm_td_vs_tuned.ic", F.rel(F.A1_BRECHAS), "split=ll4; metodo_a=timesfm_td",
             "`timesfm_td` en `ll4`", "timesfm_td solo se evaluó en ll4b")
    # n.d. por anio y por zona
    R.nd("brecha_anual.ic", B, "brecha por año", "IC de las brechas anuales", "las brechas anuales son descriptivas, sin IC")
    R.nd("brecha_zona.ic", B, "brecha por zona", "IC de las brechas por zona", "las brechas por zona son descriptivas, sin IC")


def _zonas(R: Registro, d: Datos) -> None:
    Z = F.rel(F.A1_POR_ZONA)
    z = d.zona
    piv = z.pivot_table(index=["split", "ambito", "zone_id", "zone_label", "celdas"], columns="metodo", values="rmse").reset_index()
    for s in SPLITS:
        for a in AMBITOS:
            sub = piv[(piv.split == s) & (piv.ambito == a)]
            R.add(f"zonas.{s}.{a}.n_zonas", len(sub), fm.ent(len(sub)), Z, f"split={s}; ambito={a}; nunique(zone_id)", f"Zonas con celdas en `{s}`, {AMBITO_TXT[a]}")
            for rival in ("tuned", "llr_rezagos_sel", "tuned_sin_td"):
                gap = sub["timesfm_anom"] - sub[rival]
                k = f"zonas.{s}.{a}.vs_{alias(rival)}"
                flt = f"split={s}; ambito={a}; RMSE por zona timesfm_anom - {rival}"
                ctx = f"brecha por zona TimesFM − {NOMBRE[rival]}, `{s}`, {AMBITO_TXT[a]}"
                R.add(f"{k}.n_negativas", int((gap < 0).sum()), fm.ent((gap < 0).sum()), Z, flt, f"Zonas con {ctx} negativa")
                R.add(f"{k}.n_positivas", int((gap > 0).sum()), fm.ent((gap > 0).sum()), Z, flt, f"Zonas con {ctx} positiva")
                R.add(f"{k}.mas_negativa", gap.min(), fm.num(gap.min(), 3, True), Z, flt, f"Valor más negativo de la {ctx}")
                R.add(f"{k}.menos_negativa", gap.max(), fm.num(gap.max(), 3, True), Z, flt, f"Valor más alto (más cercano a cero o positivo) de la {ctx}")
                R.add(f"{k}.mas_negativa_2d", gap.min(), fm.num(gap.min(), 2, True), Z, flt, f"Valor más negativo (2 decimales) de la {ctx}")
                R.add(f"{k}.menos_negativa_2d", gap.max(), fm.num(gap.max(), 2, True), Z, flt, f"Valor más alto (2 decimales) de la {ctx}")
                w = sub.loc[gap.idxmax()]
                R.add(f"{k}.peor_zona", None, str(w.zone_label), Z, flt, f"Etiqueta de la zona con peor desempeño relativo de TimesFM, {ctx}")
                R.add(f"{k}.peor_zona_id", int(w.zone_id), str(int(w.zone_id)), Z, flt, "Identificador de esa zona")
                R.add(f"{k}.peor_zona_gap", gap.max(), fm.num(gap.max(), 3, True), Z, flt, "Brecha de esa zona")
                R.add(f"{k}.peor_zona_celdas", int(w.celdas), fm.ent(w.celdas), Z, flt, "Celdas de esa zona")
                b = sub.loc[gap.idxmin()]
                R.add(f"{k}.mejor_zona", None, str(b.zone_label), Z, flt, f"Etiqueta de la zona con mayor ventaja de TimesFM, {ctx}")
                R.add(f"{k}.mejor_zona_gap", gap.min(), fm.num(gap.min(), 3, True), Z, flt, "Brecha de esa zona")
                R.add(f"{k}.mejor_zona_celdas", int(b.celdas), fm.ent(b.celdas), Z, flt, "Celdas de esa zona")
    # victorias (conteo de zonas ganadas) y verificacion cruzada contra RMSE por zona
    V = F.rel(F.A1_VICTORIAS)
    for r in d.victorias.itertuples(index=False):
        k = f"victorias.{r.split}.{r.ambito}.{par(r.metodo_a, r.metodo_b)}"
        R.add(k, r.zonas_a_gana, fm.ent(r.zonas_a_gana), V, f"split={r.split}; ambito={r.ambito}; metodo_a={r.metodo_a}; metodo_b={r.metodo_b}",
              f"Zonas (de {r.zonas}) en que {NOMBRE.get(r.metodo_a, r.metodo_a)} tiene menor RMSE que {NOMBRE.get(r.metodo_b, r.metodo_b)}, `{r.split}`, {AMBITO_TXT[r.ambito]}")
        sub = piv[(piv.split == r.split) & (piv.ambito == r.ambito)]
        if r.metodo_a in sub and r.metodo_b in sub:
            # El RMSE por zona de la fuente tiene 5 decimales: un empate redondeado puede ser victoria.
            lo, hi = int((sub[r.metodo_a] < sub[r.metodo_b]).sum()), int((sub[r.metodo_a] <= sub[r.metodo_b]).sum())
            R.verificar(f"victorias recomputadas {k}", lo <= r.zonas_a_gana <= hi)


def _cribado(R: Registro, d: Datos) -> None:
    L = F.rel(F.LEADERBOARD)
    lb = d.leaderboard
    lb = lb[lb.split == "ll4"].copy()
    tun = lb[lb.method == "tuned"].iloc[0]
    clim = lb[lb.method == "climatology"].iloc[0]
    var = lb[lb.method.str.startswith("timesfm:")].copy()
    var["slug"] = var.method.str.split(":", n=1).str[1]
    R.add("cribado.n_celdas", tun.cells, fm.ent(tun.cells), L, "split=ll4; method=tuned; col=cells", "Celdas puntuadas del cribado limpio (en común con `tuned`)")
    R.add("cribado.n_filas", tun.n, fm.ent(tun.n), L, "split=ll4; method=tuned; col=n", "Filas del cribado limpio")
    R.add("cribado.n_variantes", len(var), str(len(var)), L, "method empieza con 'timesfm:'", "Variantes de TimesFM del cribado")
    menor = var[var.rmse < tun.rmse]
    R.add("cribado.n_menor_tuned", len(menor), str(len(menor)), L, "rmse variante < rmse tuned", "Variantes con RMSE menor que `tuned`")
    R.add("cribado.n_mayor_tuned", len(var) - len(menor), str(len(var) - len(menor)), L, "rmse variante >= rmse tuned", "Variantes con RMSE mayor que `tuned`")
    R.add("cribado.pierden", len(var) - len(menor), lista_es(list(var[var.rmse >= tun.rmse].slug)), L, "rmse variante >= tuned", "Variantes que pierden frente a `tuned`")
    for nom, row in (("tuned", tun), ("clim", clim)):
        R.add(f"cribado.{nom}.rmse", row.rmse, fm.num(row.rmse), L, f"split=ll4; method={row.method}", f"RMSE (°C) de {nom} en el cribado")
        R.add(f"cribado.{nom}.mae", row.mae, fm.num(row.mae), L, f"split=ll4; method={row.method}", f"MAE (°C) de {nom} en el cribado")
        R.add(f"cribado.{nom}.sesgo", row.bias, fm.num(row.bias, 3, True), L, f"split=ll4; method={row.method}", f"Sesgo (°C) de {nom} en el cribado")
    for r in var.itertuples(index=False):
        k = f"cribado.v.{r.slug}"
        flt = f"split=ll4; method={r.method}"
        R.add(f"{k}.rmse", r.rmse, fm.num(r.rmse), L, flt, f"RMSE (°C) de la variante {r.slug}")
        R.add(f"{k}.mae", r.mae, fm.num(r.mae), L, flt, f"MAE (°C) de la variante {r.slug}")
        R.add(f"{k}.sesgo", r.bias, fm.num(r.bias, 3, True), L, flt, f"Sesgo (°C) de la variante {r.slug}")
        R.add(f"{k}.delta_tuned", r.rmse - tun.rmse, fm.num(r.rmse - tun.rmse, 3, True), L, flt + "; rmse - rmse(tuned)", f"RMSE de {r.slug} menos RMSE de `tuned` (puntual, sin IC)")
        R.add(f"{k}.menor_tuned", int(r.rmse < tun.rmse), si_no(r.rmse < tun.rmse), L, flt, f"¿{r.slug} tiene RMSE menor que `tuned`?")
        R.add(f"{k}.skill", r.skill_vs_clim, fm.num(r.skill_vs_clim, 3, True), L, flt + "; col=skill_vs_clim", f"Habilidad frente a climatología de {r.slug}")
    a = var.set_index("slug")
    dif = abs(a.loc["tmin_td_full"].rmse - a.loc["tmin_td_znorm"].rmse)
    R.add("cribado.dif_td_full_znorm", dif, fm.sci(dif), L, "|rmse(tmin_td_full) - rmse(tmin_td_znorm)|", "Diferencia de RMSE (°C) entre `tmin_td_full` y `tmin_td_znorm`",
          nota="la igualdad de predicciones no se comprobó")
    c = d.costo
    cr = c[c.etapa.str.startswith("seleccion de variante")].iloc[0]
    R.add("cribado.n_celdas_predichas", cr.celdas, fm.ent(cr.celdas), F.rel(F.COSTO_CSV), "etapa=seleccion de variante (cribado); col=celdas",
          "Celdas predichas en el cribado (más que las puntuadas en común con `tuned`)")
    R.add("cribado.mejor_variante", None, a.rmse.idxmin(), L, "min(rmse) entre variantes", "Variante de TimesFM con menor RMSE en el cribado")


def _escalera(R: Registro, d: Datos) -> None:
    E = F.rel(F.A1_ESCALERA)
    e = d.escalera[d.escalera.periodo == "total"]
    for r in e.itertuples(index=False):
        k = f"escalera.{r.split}.{r.metodo}.i{r.inicio}"
        flt = f"split={r.split}; metodo={r.metodo}; inicio={r.inicio}; periodo=total"
        ctx = f"{r.metodo}, inicio {r.inicio}, `{r.split}` (panel de cribado, 1.092 celdas)"
        R.add(f"{k}.rmse", r.rmse, fm.num(r.rmse), E, flt, f"RMSE (°C) {ctx}")
        R.add(f"{k}.delta", r.delta_rmse_vs_1981, fm.num(r.delta_rmse_vs_1981, 3, True), E, flt + "; col=delta_rmse_vs_1981", f"Cambio de RMSE (°C) frente a inicio 1981, {ctx}")
        R.add(f"{k}.anios", r.anios_historial, str(int(r.anios_historial)), E, flt + "; col=anios_historial", f"Años de historial, {ctx}")
    EB = F.rel(F.A1_ESCALERA_BRECHAS)
    for r in d.esc_brechas.itertuples(index=False):
        k = f"escalera_brecha.{r.split}.{r.esquema}.{r.metodo_a.replace('@', '_')}_vs_{r.metodo_b.replace('@', '_')}"
        flt = f"split={r.split}; esquema={r.esquema}; metodo_a={r.metodo_a}; metodo_b={r.metodo_b}"
        ctx = f"{r.metodo_a} − {r.metodo_b}, `{r.split}`, {r.esquema}"
        R.add(f"{k}.v", r.brecha, fm.num(r.brecha, 3, True), EB, flt, f"Brecha RMSE (°C) {ctx}")
        R.add(f"{k}.lo", r.ic_lo, fm.num(r.ic_lo, 3, True), EB, flt, f"IC inferior {ctx}")
        R.add(f"{k}.hi", r.ic_hi, fm.num(r.ic_hi, 3, True), EB, flt, f"IC superior {ctx}")
        R.add(f"{k}.ic", None, fm.ic(r.ic_lo, r.ic_hi), EB, flt, f"IC 95 % {ctx}")
    # Tamano del efecto de recortar solo contexto frente a recortar tambien la climatologia
    for s in SPLITS:
        ee = e.set_index(["split", "metodo", "inicio"])
        dlt = ee.loc[(s, "timesfm_clim_propia", 2002)].rmse - ee.loc[(s, "timesfm", 2002)].rmse
        R.add(f"escalera.{s}.costo_recortar_clim", dlt, fm.num(dlt, 3, True), E, f"split={s}; rmse(timesfm_clim_propia@2002) - rmse(timesfm@2002)",
              f"Costo (°C) de recortar además la climatología desde 2002, `{s}`")


def _a3(R: Registro, d: Datos) -> None:
    A = F.rel(F.A3_BARAJADA)
    for r in d.a3.itertuples(index=False):
        flt = f"corrida={r.corrida}"
        R.add(f"a3.{r.corrida}.rmse", r.rmse, fm.num(r.rmse, 3), A, flt, f"RMSE (°C), corrida A3 {r.corrida} (`ll4`, panel de cribado; 3 decimales, como en el resto del paper)")
        R.add(f"a3.{r.corrida}.skill", r.skill, fm.num(r.skill, 3, True), A, flt, f"Habilidad frente a climatología, {r.corrida}")
        R.add(f"a3.{r.corrida}.sesgo", r.sesgo, fm.num(r.sesgo, 3, True), A, flt, f"Sesgo (°C), {r.corrida}")
    yr = d.a3[d.a3.modo == "year"]
    R.add("a3.barajado_anio.rmse_min", yr.rmse.min(), fm.num(yr.rmse.min(), 3), A, "modo=year", "RMSE mínimo entre las corridas con Tmin barajada entre años")
    R.add("a3.barajado_anio.rmse_max", yr.rmse.max(), fm.num(yr.rmse.max(), 3), A, "modo=year", "RMSE máximo entre las corridas con Tmin barajada entre años")
    R.add("a3.barajado_anio.n_semillas", yr.semilla.nunique(), str(yr.semilla.nunique()), A, "modo=year; nunique(semilla)", "Semillas del barajado entre años")
    R.add("a3.barajado_anio.n_corridas", len(yr), str(len(yr)), A, "modo=year", "Corridas con barajado entre años")
    clim = float(d.a3[d.a3.corrida == "pred_clim"].rmse.iloc[0])
    R.add("a3.barajado_anio.todas_peor_que_clim", int((yr.rmse > clim).all()), si_no((yr.rmse > clim).all()), A, "rmse(modo=year) > rmse(pred_clim)",
          "¿Todas las corridas con barajado entre años quedan peor que la climatología?")
    R.add("a3.n_celdas", d.a3.celdas.iloc[0], fm.ent(d.a3.celdas.iloc[0]), A, "col=celdas", "Celdas del panel de A3")
    R.add("a3.n_filas", d.a3.filas.iloc[0], fm.ent(d.a3.filas.iloc[0]), A, "col=filas", "Filas del panel de A3")
    R.nd("a3.ll4b.rmse", A, "split=ll4b", "A3 en `ll4b`", "A3 solo se corrió en ll4")


_GRADOS = ("CAPITAN FAP", "CORONEL FAP", "CAP FAP", "GEN FAP", "TENIENTE", "CAPITAN", "CORONEL", "CAP")


def _nombre_estacion(n: str) -> str:
    """Nombre ISD sin grado militar ni "INTL", en minusculas con inicial mayuscula (solo para rotular)."""
    n = str(n).strip()
    for g_ in _GRADOS:
        if n.startswith(g_ + " "):
            n = n[len(g_) + 1:]
            break
    if n.endswith(" INTL"):
        n = n[:-5]
    return n.title().replace(" De ", " de ").replace(" A ", " A. ")


def _a4(R: Registro, d: Datos) -> None:
    P = F.rel(F.A4_POR_PERIODO)
    for r in d.a4_periodo.itertuples(index=False):
        per = r.periodo.replace("-", "_")
        k = f"a4.{r.kind}.{r.fuente}_{per}"
        flt = f"muestra=productos; kind={r.kind}; fuente={r.fuente}; periodo={r.periodo}"
        ctx = f"{r.kind} {r.fuente} {r.periodo}"
        R.add(f"{k}.n_dias", r.n_dias, fm.ent(r.n_dias), P, flt, f"Días-estación, {ctx}")
        R.add(f"{k}.n_estaciones", r.n_estaciones, fm.ent(r.n_estaciones), P, flt, f"Estaciones, {ctx}")
        R.add(f"{k}.rmse", r.rmse, fm.num(r.rmse, 2), P, flt, f"RMSE (°C), {ctx} (2 decimales)")
        R.add(f"{k}.sesgo", r.sesgo, fm.num(r.sesgo, 2, True), P, flt, f"Sesgo (°C), {ctx} (2 decimales)")
        R.add(f"{k}.mae", r.mae, fm.num(r.mae, 2), P, flt, f"MAE (°C), {ctx} (2 decimales)")
    BT = F.rel(F.A4_DELTA_BOOT)
    for r in d.a4_boot.itertuples(index=False):
        k = f"a4.delta_rmse.{r.kind}.{alias(r.a)}_vs_{alias(r.b)}"
        flt = f"muestra=productos; kind={r.kind}; a={r.a}; b={r.b}; periodo={r.periodo}"
        R.add(f"{k}.v", r.delta_rmse, fm.num(r.delta_rmse, 3, True), BT, flt, f"ΔRMSE (°C) {r.a} − {r.b}, {r.kind}, {r.periodo}")
        R.add(f"{k}.ic", None, fm.ic(r.ic95_lo, r.ic95_hi), BT, flt, "IC 95 % del ΔRMSE")
        R.add(f"{k}.excluye_cero", int(not (r.ic95_lo <= 0 <= r.ic95_hi)), si_no(not (r.ic95_lo <= 0 <= r.ic95_hi)), BT, flt, "¿El IC excluye cero?")
        R.add(f"{k}.n_estaciones", r.n_estaciones, fm.ent(r.n_estaciones), BT, flt, "Estaciones del bootstrap")
        R.add(f"{k}.n_dias", r.n_dias, fm.ent(r.n_dias), BT, flt, "Días-estación del bootstrap")
    # Estaciones con mayor sesgo de PISCO Td 2009-2016
    se = d.a4_estacion[(d.a4_estacion.kind == "td") & (d.a4_estacion.fuente == "pisco") & (d.a4_estacion.periodo == "2009-2016")]
    names = d.a4_estaciones.set_index("station")["STATION NAME"]
    elev = d.a4_estaciones.set_index("station")["ELEV(M)"]
    se = se.assign(nombre=se.station.astype(str).map(names)).sort_values("sesgo", ascending=False)
    for i, r in enumerate(se.head(3).itertuples(index=False), 1):
        R.add(f"a4.td.pisco_2009_2016.estacion_sesgo{i}", r.sesgo, fm.num(r.sesgo, 2, True), F.rel(F.A4_POR_ESTACION),
              f"muestra=productos; kind=td; fuente=pisco; periodo=2009-2016; sesgo #{i}", f"Sesgo de la estación con el {i}.º mayor sesgo de PISCO Td", nota=f"estación: {r.nombre}")
    # Conteos de |sesgo| > 2 °C y nombre de las tres estaciones con mayor sesgo de PISCO
    for i, r in enumerate(se.head(3).itertuples(index=False), 1):
        R.add(f"a4.td.pisco_2009_2016.estacion_sesgo{i}_nombre", None, _nombre_estacion(r.nombre), F.rel(F.A4_ESTACIONES),
              f"station={r.station}; col=STATION NAME", f"Nombre de la estación con el {i}.º mayor sesgo de PISCO Td")
        R.add(f"a4.td.pisco_2009_2016.estacion_sesgo{i}_elev", float(elev[str(r.station)]), fm.ent(elev[str(r.station)]), F.rel(F.A4_ESTACIONES),
              f"station={r.station}; col=ELEV(M)", f"Elevación (m) de la estación con el {i}.º mayor sesgo de PISCO Td")
    for fuente, per in (("pisco", "2009-2016"), ("palacios", "2017-2020"), ("timesfm", "2017-2020")):
        x = d.a4_estacion[(d.a4_estacion.kind == "td") & (d.a4_estacion.fuente == fuente) & (d.a4_estacion.periodo == per)]
        n = int((x.sesgo.abs() > 2).sum())
        k = f"a4.td.{fuente}_{per.replace('-', '_')}"
        flt = f"muestra=productos; kind=td; fuente={fuente}; periodo={per}; |sesgo| > 2"
        R.add(f"{k}.n_sesgo_gt2", n, fm.ent(n), F.rel(F.A4_POR_ESTACION), flt, f"Estaciones con |sesgo| > 2 °C, Td {fuente} {per}")
        R.add(f"{k}.n_estaciones_tabla", len(x), fm.ent(len(x)), F.rel(F.A4_POR_ESTACION), flt.split("; |")[0], f"Estaciones evaluadas, Td {fuente} {per}")
    R.nd("a4.independencia_estaciones", F.rel(F.A4_ESTACIONES), "estaciones ISD vs estaciones de PISCO Td v1.1",
         "Independencia de las estaciones ISD frente a PISCO", "no hay lista pública para comprobarlo (sintesis_amenazas.md §6)")


# --- Costo ------------------------------------------------------------------------------
COSTO_IDS = [
    ("timesfm_ll4b_inferencia", "timesfm_anom", "ll4b", "prediccion"),
    ("timesfm_td_ll4b_inferencia", "timesfm_td", "ll4b", "prediccion"),
    ("timesfm_ll4_inferencia", "timesfm_anom", "ll4", "prediccion (sin"),
    ("timesfm_cribado", "timesfm (9 variantes)", "ll4", "seleccion de variante"),
    ("timesfm_ll4_escala", "timesfm_anom", "ll4", "prediccion pasada"),
    ("timesfm_producto_inferencia", "timesfm_anom", "real 2017-2020", "prediccion producto"),
    ("tuned_ll4b_seleccion", "tuned", "ll4b", "seleccion"),
    ("tuned_ll4b_ajuste", "tuned", "ll4b", "ajuste"),
    ("tuned_ll4_seleccion", "tuned", "ll4", "seleccion"),
    ("tuned_ll4_ajuste", "tuned", "ll4", "ajuste"),
    ("tuned_prod_seleccion", "tuned", "produccion 1981-2016", "seleccion"),
    ("tuned_prod_ajuste", "tuned", "produccion 1981-2016", "ajuste"),
    ("tuned_producto_prediccion", "tuned", "real 2017-2020", "prediccion"),
    ("llr_simple_ll4b_carga", "llr_simple", "ll4b", "carga"),
    ("llr_simple_ll4b_seleccion_h", "llr_simple", "ll4b", "seleccion"),
    ("llr_simple_ll4b_ajuste", "llr_simple", "ll4b", "ajuste"),
    ("llr_simple_ll4b_total", "llr_simple", "ll4b", "total"),
    ("llr_rezagos_ll4b_carga", "llr_rezagos", "ll4b", "carga"),
    ("llr_rezagos_ll4b_seleccion_h", "llr_rezagos", "ll4b", "seleccion"),
    ("llr_rezagos_ll4b_ajuste", "llr_rezagos", "ll4b", "ajuste"),
    ("llr_rezagos_ll4b_total", "llr_rezagos", "ll4b", "total"),
]


def costo_filas(d: Datos) -> dict[str, pd.Series]:
    out = {}
    for cid, met, blq, etapa in COSTO_IDS:
        c = d.costo
        sel = c[(c.metodo == met) & (c.bloque == blq) & c.etapa.str.startswith(etapa)]
        if len(sel) != 1:
            raise ValueError(f"fila de costo ambigua o ausente: {cid} -> {len(sel)}")
        out[cid] = sel.iloc[0]
    if len({r.name for r in out.values()}) != len(d.costo):
        raise ValueError("COSTO_IDS no cubre todas las filas de costo.csv exactamente una vez")
    return out


def _costo(R: Registro, d: Datos) -> None:
    C = F.rel(F.COSTO_CSV)
    rows = costo_filas(d)
    for cid, r in rows.items():
        flt = f"metodo={r.metodo}; bloque={r.bloque}; etapa={r.etapa}"
        k = f"costo.{cid}"
        R.add(f"{k}.seg", r.segundos_pared, fm.num(r.segundos_pared, 1 if r.segundos_pared % 1 else 0), C, flt + "; col=segundos_pared", f"Segundos de pared, {r.metodo} {r.bloque} {r.etapa}")
        R.add(f"{k}.tiempo", r.segundos_pared, fm.dur(r.segundos_pared), C, flt + "; col=segundos_pared", f"Tiempo de pared legible, {r.metodo} {r.bloque} {r.etapa}")
        R.add(f"{k}.celdas", r.celdas, fm.ent(r.celdas), C, flt + "; col=celdas", "Celdas procesadas")
        R.add(f"{k}.hardware", None, str(r.hardware), C, flt + "; col=hardware", "Hardware declarado")
        if pd.notna(r.celdas_por_s):
            R.add(f"{k}.celdas_por_s", r.celdas_por_s, fm.num(r.celdas_por_s, 2), C, flt + "; col=celdas_por_s", "Celdas por segundo")
            R.verificar(f"celdas/s recomputadas {cid}", abs(r.celdas / r.segundos_pared - r.celdas_por_s) < 0.01 or cid.endswith("escala"))
    s = {cid: float(r.segundos_pared) for cid, r in rows.items()}

    def der(clave, valor, texto, filtro, desc, nota=""):
        R.add(clave, valor, texto, C, filtro, desc, nota)

    def tiempo(clave, valor, filtro, desc):
        der(f"{clave}.seg", valor, fm.num(valor, 1 if round(valor, 6) % 1 else 0), filtro, desc + " (s)")
        der(f"{clave}.tiempo", valor, fm.dur(valor), filtro, desc + " (legible)")

    tun = s["tuned_ll4b_seleccion"] + s["tuned_ll4b_ajuste"]
    inf = s["timesfm_ll4b_inferencia"]
    cri = s["timesfm_cribado"]
    tiempo("costo.ll4b.tuned_total", tun, "tuned_ll4b_seleccion + tuned_ll4b_ajuste", "Total `tuned` en `ll4b` (selección + ajuste y predicción)")
    tiempo("costo.ll4b.timesfm_inferencia", inf, "timesfm_ll4b_inferencia", "Inferencia de TimesFM en `ll4b`")
    tiempo("costo.ll4b.timesfm_seleccion", cri, "timesfm_cribado (suma de las 9 variantes, hecho en ll4)", "Selección única de configuración de TimesFM")
    tiempo("costo.ll4b.timesfm_total", inf + cri, "inferencia ll4b + cribado (una sola vez)", "Total TimesFM en `ll4b` incluyendo la selección una vez")
    der("costo.ll4b.ratio_total", (inf + cri) / tun, fm.num((inf + cri) / tun, 2), "(inferencia + cribado) / tuned_total", "Cociente total TimesFM / total `tuned` en `ll4b`")
    der("costo.ll4b.ratio_total_r", (inf + cri) / tun, fm.num((inf + cri) / tun, 0), "(inferencia + cribado) / tuned_total, 0 decimales", "Cociente total TimesFM / total `tuned` en `ll4b`, entero")
    der("costo.ll4b.ratio_inferencia_tuned_total", inf / tun, fm.num(inf / tun, 2), "inferencia / tuned_total", "Cociente inferencia TimesFM / total `tuned`")
    der("costo.ll4b.ratio_inferencia_ajuste", inf / s["tuned_ll4b_ajuste"], fm.num(inf / s["tuned_ll4b_ajuste"], 1), "inferencia / tuned_ll4b_ajuste",
        "Cociente inferencia TimesFM / ajuste y predicción de `tuned`")
    der("costo.ll4b.ratio_inferencia_ajuste_r", inf / s["tuned_ll4b_ajuste"], fm.num(inf / s["tuned_ll4b_ajuste"], 0), "inferencia / tuned_ll4b_ajuste, 0 decimales",
        "Cociente inferencia TimesFM / ajuste y predicción de `tuned`, entero")
    der("costo.ll4b.celdas_timesfm_extra", rows["timesfm_ll4b_inferencia"].celdas - 17027, fm.ent(rows["timesfm_ll4b_inferencia"].celdas - 17027), "celdas TimesFM - 17.027 puntuadas",
        "Celdas que TimesFM predice de más (panel 17.041)")
    tl = s["tuned_ll4_seleccion"] + s["tuned_ll4_ajuste"]
    tiempo("costo.ll4.tuned_total", tl, "tuned_ll4_seleccion + tuned_ll4_ajuste", "Total `tuned` limpio de Palacios en `ll4`")
    # Escala de producto
    tsel = s["tuned_prod_seleccion"] + s["tuned_prod_ajuste"]
    tiempo("costo.producto.tuned_entrenamiento", tsel, "tuned_prod_seleccion + tuned_prod_ajuste", "Selección y ajuste de `tuned` (1981–2016)")
    der("costo.producto.tuned_entrenamiento.horas", tsel / 3600, fm.horas(tsel), "segundos / 3600", "Horas de selección y ajuste de `tuned` a escala de producto")
    der("costo.producto.tuned_entrenamiento.horas_enteras", tsel / 3600, fm.num(tsel / 3600, 0), "segundos / 3600 redondeado", "Horas redondeadas (\"unas N h\")")
    tp = s["tuned_producto_prediccion"]
    tf = s["timesfm_producto_inferencia"]
    tiempo("costo.producto.tuned_prediccion", tp, "tuned_producto_prediccion", "Predicción 2017–2020 de `tuned`")
    tiempo("costo.producto.timesfm_inferencia", tf, "timesfm_producto_inferencia", "Inferencia 2017–2020 de TimesFM")
    der("costo.producto.timesfm_inferencia.dias", tf / 86400, fm.dias(tf), "segundos / 86400", "Días de inferencia de TimesFM a escala de producto")
    der("costo.producto.timesfm_inferencia.dias_aprox", tf / 86400, "≈" + fm.dias(tf) + " días", "segundos / 86400", "Días de inferencia, con símbolo ≈")
    der("costo.producto.ratio_inferencia", tf / tp, fm.num(tf / tp, 0), "timesfm_inferencia / tuned_prediccion", "Cociente de inferencia TimesFM / `tuned` a escala de producto",
        nota="costo.md dice «unas 370 veces»; el cociente exacto es " + fm.num(tf / tp, 1))
    der("costo.producto.ratio_inferencia_1d", tf / tp, fm.num(tf / tp, 1), "timesfm_inferencia / tuned_prediccion", "Cociente con un decimal")
    tiempo("costo.producto.tuned_total_con_prediccion", tsel + tp, "entrenamiento + predicción de `tuned`", "`tuned` a escala de producto, entrenamiento y predicción 2017–2020")
    der("costo.producto.celdas_por_s_timesfm", rows["timesfm_producto_inferencia"].celdas_por_s, fm.num(rows["timesfm_producto_inferencia"].celdas_por_s, 2),
        "col=celdas_por_s", "Celdas por segundo de TimesFM a escala de producto")
    der("costo.producto.celdas", rows["timesfm_producto_inferencia"].celdas, fm.ent(rows["timesfm_producto_inferencia"].celdas), "col=celdas", "Celdas del producto 2017–2020")
    # LLR
    for nom in ("llr_simple", "llr_rezagos"):
        partes = s[f"{nom}_ll4b_carga"] + s[f"{nom}_ll4b_seleccion_h"] + s[f"{nom}_ll4b_ajuste"]
        R.verificar(f"{nom}: suma de etapas ≈ total", abs(partes - s[f"{nom}_ll4b_total"]) < 1.0)
    # No medidos
    if d.r3_costo is None:
        R.nd("costo.llr_simple_sel.tiempo", C, "llr_simple_sel", "Tiempo de `llr_simple_sel`", "no medido")
        R.nd("costo.llr_rezagos_sel.tiempo", C, "llr_rezagos_sel", "Tiempo de `llr_rezagos_sel`", "no medido; los tiempos de costo.csv son de la versión sin selección conjunta")
    R.nd("costo.tuned_sin_td.tiempo", C, "tuned_sin_td", "Tiempo de `tuned` sin rezagos de Td", "no figura en la tabla de costo")
    R.nd("costo.horas_humanas", C, "-", "Horas-persona de diseño", "no medidas")
    R.nd("costo.preentrenamiento_timesfm", C, "-", "Costo de preentrenamiento de TimesFM", "no cronometrado")
    R.nd("costo.preprocesamiento_compartido", C, "-", "Preprocesamiento compartido (regrillado, climatologías)", "sin cronometraje independiente completo")
    R.nd("costo.host_palacios", C, "tuned ll4 y producción", "Host de las corridas de Palacios", "el log no registra el host")
    R.add("costo.hardware.estacion", None, d.estacion_trabajo, F.rel(F.COSTO_MD), "párrafo inicial de costo.md", "Estación de trabajo (CPU, RAM, GPU)")


# Parametros de TimesFM 3.0 en millones. Constante documentada, no derivada de codigo: valor de la API de
# Hugging Face para `google/timesfm-3.0-pytorch` (ver reports/paper_nuevo/bib_verificacion.md).
TIMESFM_PARAMETROS_MILLONES = 330


def _desglose_percentiles() -> tuple[float, float]:
    """Percentiles del IC bootstrap leidos del codigo que genero a1_brechas.csv (experiments/amenazas/desglose.py)."""
    txt = (F.REPO / "experiments" / "amenazas" / "desglose.py").read_text()
    m = re.search(r"np\.percentile\(rep,\s*\[([\d.]+),\s*([\d.]+)\]\)", txt)
    if m is None:
        raise ValueError("no se encontro np.percentile(rep, [lo, hi]) en desglose.py")
    return float(m.group(1)), float(m.group(2))


def _diseno(R: Registro, d: Datos) -> None:
    """Cifras de diseno derivadas del codigo (configuracion de variantes, pool, grillas) y de a1_*.csv."""
    from HPC_code_tunning.feature_spec import DEFAULT_CANDIDATE_POOL
    from experiments.llr_simple import llr, llr_lags
    from experiments.timesfm.variants import VARIANTS

    A, B = F.rel(F.A1_POR_METODO), F.rel(F.A1_BRECHAS)
    # a. Cuanto de la brecha TimesFM - tuned cierra quitar los rezagos de Td de `tuned`.
    t = d.metodo[d.metodo.periodo == "total"].set_index(["split", "ambito", "metodo"]).rmse
    for s in SPLITS:
        for a in AMBITOS:
            mejora = float(t[(s, a, "tuned")] - t[(s, a, "tuned_sin_td")])
            kb = f"brecha.{s}.{a}.tuned_vs_tuned_sin_td.v"
            R.verificar(f"mejora sin Td coincide con a1_brechas: {s} {a}", abs(mejora - R.num(kb)) < 5e-5)
            gap = abs(R.num(f"brecha.{s}.{a}.timesfm_vs_tuned.v"))
            flt = f"split={s}; ambito={a}; periodo=total; col=rmse"
            ctx = f"`{s}`, {AMBITO_TXT[a]}"
            R.add(f"a2.{s}.{a}.mejora_sin_td", mejora, fm.num(mejora), A, flt + "; rmse(tuned) - rmse(tuned_sin_td)",
                  f"Reduccion de RMSE (°C) de `tuned` al quitar los rezagos de Td, {ctx}")
            R.add(f"a2.{s}.{a}.brecha_timesfm_tuned", gap, fm.num(gap), A, flt + "; |rmse(timesfm_anom) - rmse(tuned)|",
                  f"Magnitud de la brecha TimesFM − `tuned` (°C), {ctx}")
            R.add(f"a2.{s}.{a}.fraccion_cerrada_pct", 100 * mejora / gap, fm.num(100 * mejora / gap, 0), A,
                  flt + "; 100 * mejora_sin_td / brecha_timesfm_tuned",
                  f"Porcentaje (sin %) de la brecha TimesFM − `tuned` que cubre quitar los rezagos de Td, {ctx}")
            sin = float(t[(s, a, "tuned_sin_td")] - t[(s, a, "timesfm_anom")])
            R.add(f"a2.{s}.{a}.brecha_timesfm_sin_td", sin, fm.num(sin), A, flt + "; rmse(tuned_sin_td) - rmse(timesfm_anom)",
                  f"Magnitud de la brecha restante de TimesFM frente a `tuned` sin rezagos de Td (°C), {ctx}")
    # b. Longitud de contexto de cada variante de TimesFM (anios hasta el fin del contexto de cada bloque).
    V = F.rel(F.REPO / "experiments" / "timesfm" / "variants.py")
    for v in VARIANTS:
        R.add(f"variantes.{v.key}.contexto_ini", v.context_start_year, str(v.context_start_year), V, f"Variant.key={v.key}",
              f"Primer año de contexto de la variante {v.key}")
        for s in SPLITS:
            n = int(R.num(f"bloques.{s}.contexto_fin")) - v.context_start_year + 1
            R.add(f"variantes.{v.key}.contexto_anios.{s}", n, str(n), V + "; " + B, f"Variant.key={v.key}; bloques.{s}.contexto_fin - inicio + 1",
                  f"Años de contexto de la variante {v.key} en `{s}`")
    R.add("variantes.n_total", len(VARIANTS), str(len(VARIANTS)), V, "len(VARIANTS)", "Variantes definidas en el código (incluye las que no entraron al cribado)")
    # b2. Conteos de diseno que la prosa citaba a mano.
    L = F.rel(F.LEADERBOARD)
    slugs = {m.split(":", 1)[1] for m in d.leaderboard[d.leaderboard.split == "ll4"].method if m.startswith("timesfm:")}
    en_cribado = [v for v in VARIANTS if v.key in slugs]
    inicios = sorted({v.context_start_year for v in en_cribado})
    R.add("variantes.inicios_cribado", len(inicios), lista_es([str(x) for x in inicios]), V + "; " + L,
          "context_start_year distintos de las variantes del cribado", "Años de inicio del contexto probados en el cribado")
    n_uni = sum(1 for v in en_cribado if not v.covariates)
    R.add("variantes.n_univariadas", n_uni, str(n_uni), V + "; " + L,
          "variantes del cribado sin covariables", "Variantes del cribado sin Tmin (univariadas)")
    llrs = sorted({alias(m) for m in d.metodo.metodo.unique() if m.startswith("llr_")})
    R.add("diseno.llr.n_variantes", len(llrs), str(len(llrs)), A, "metodos que empiezan con llr_ en a1_por_metodo.csv",
          "Variantes de LLR sin zonas evaluadas", nota=lista_es(llrs))
    peor = []
    for s in SPLITS:
        for y in range(int(R.num(f"bloques.{s}.anio_ini")), int(R.num(f"bloques.{s}.anio_fin")) + 1):
            if R.num(f"rmse_anual.{s}.panel.tuned_sin_td.a{y}") > R.num(f"rmse_anual.{s}.panel.tuned.a{y}"):
                peor.append(str(y))
    R.add("a2.anios_sin_td_peor", len(peor), lista_es(peor), A, "años con rmse_anual(tuned_sin_td) > rmse_anual(tuned), dominio completo",
          "Años (dominio completo) en que `tuned` sin rezagos de Td tiene mayor RMSE que `tuned`")
    # c. Diseno de los metodos, desde el codigo que los define.
    FS = F.rel(F.REPO / "HPC_code_tunning" / "feature_spec.py")
    LL = F.rel(F.REPO / "experiments" / "llr_simple" / "llr.py")
    pool = list(DEFAULT_CANDIDATE_POOL)
    td = sorted(int(x.rsplit("lag", 1)[1]) for x in pool if x.startswith("TD_anom_lag"))
    tm = sorted(int(x.rsplit("lag", 1)[1]) for x in pool if x.startswith("TMIN_anom_lag"))
    R.add("diseno.tuned.pool_terminos", len(pool), str(len(pool)), FS, "len(DEFAULT_CANDIDATE_POOL)", "Términos candidatos del pool de `tuned` (incluye la constante)")
    R.add("diseno.tuned.pool_rezagos_td", len(td), str(len(td)), FS, "TD_anom_lag*", "Rezagos de Td en el pool de `tuned`")
    R.add("diseno.tuned.pool_rezagos_tmin", len(tm), str(len(tm)), FS, "TMIN_anom_lag*", "Rezagos de Tmin en el pool de `tuned`")
    R.add("diseno.tuned.pool_sin_td", len(pool) - len(td), str(len(pool) - len(td)), FS, "pool sin TD_anom_lag*", "Términos del pool de `tuned_sin_td`")
    R.add("diseno.tuned.rezagos_td", len(td), lista_es([str(x) for x in td]), FS, "TD_anom_lag*", "Lista de rezagos de Td del pool")
    R.add("diseno.tuned.rezagos_tmin", len(tm), lista_es([str(x) for x in tm]), FS, "TMIN_anom_lag*", "Lista de rezagos de Tmin del pool")
    R.nd("diseno.tuned.h_min", FS, "-", "Menor semiancho `h` de la grilla de `tuned` (usada en el artículo)",
         "la grilla 7-45 solo está documentada en costo.md; el valor por defecto del código es otro (HPC_code_tunning, h_grid=7,11,15,21)")
    R.nd("diseno.tuned.h_max", FS, "-", "Mayor semiancho `h` de la grilla de `tuned` (usada en el artículo)", "ver diseno.tuned.h_min")
    hs, hg, st = llr.H_GRID_SEL, llr.H_GRID, llr.TRAIN_START_GRID
    R.add("diseno.llr.h_n", len(hg), str(len(hg)), LL, "H_GRID", "Valores de `h` de los LLR sin selección conjunta")
    R.add("diseno.llr.h_min", min(hg), str(min(hg)), LL, "H_GRID", "Menor `h` de los LLR sin selección conjunta")
    R.add("diseno.llr.h_max", max(hg), str(max(hg)), LL, "H_GRID", "Mayor `h` de los LLR sin selección conjunta")
    R.add("diseno.llr_sel.h_n", len(hs), str(len(hs)), LL, "H_GRID_SEL", "Valores de `h` de los LLR seleccionados")
    R.add("diseno.llr_sel.h_min", min(hs), str(min(hs)), LL, "H_GRID_SEL", "Menor `h` de los LLR seleccionados")
    R.add("diseno.llr_sel.h_max", max(hs), str(max(hs)), LL, "H_GRID_SEL", "Mayor `h` de los LLR seleccionados")
    R.add("diseno.llr_sel.inicios_n", len(st), str(len(st)), LL, "TRAIN_START_GRID", "Años de inicio candidatos de los LLR seleccionados")
    R.add("diseno.llr_sel.inicio_min", min(st), str(min(st)), LL, "TRAIN_START_GRID", "Primer año de inicio candidato")
    R.add("diseno.llr_sel.inicio_max", max(st), str(max(st)), LL, "TRAIN_START_GRID", "Último año de inicio candidato")
    R.add("diseno.llr_sel.combinaciones", len(hs) * len(st), str(len(hs) * len(st)), LL, "len(H_GRID_SEL) * len(TRAIN_START_GRID)", "Combinaciones (h, inicio) evaluadas por los LLR seleccionados")
    R.add("diseno.llr.validacion_anios", llr.VALIDATION_YEARS, str(llr.VALIDATION_YEARS), LL, "VALIDATION_YEARS", "Últimos años de entrenamiento usados como validación interna de los LLR")
    R.add("diseno.llr.rezagos_tmin", len(llr_lags.DEFAULT_LAGS), lista_es([str(x) for x in llr_lags.DEFAULT_LAGS]),
          F.rel(F.REPO / "experiments" / "llr_simple" / "llr_lags.py"), "DEFAULT_LAGS", "Rezagos de Tmin del LLR con rezagos")
    R.add("timesfm.parametros_millones", TIMESFM_PARAMETROS_MILLONES, str(TIMESFM_PARAMETROS_MILLONES), "reports/paper_nuevo/bib_verificacion.md",
          "constante en cifras.py", "Parámetros de TimesFM 3.0 (millones)", nota="constante documentada (API de Hugging Face), no derivada de código")
    # d. Nivel de los IC bootstrap.
    lo, hi = _desglose_percentiles()
    R.add("bootstrap.nivel", hi - lo, fm.num(hi - lo, 0), "experiments/amenazas/desglose.py", f"np.percentile(rep, [{lo}, {hi}])",
          "Nivel (%) de los IC bootstrap, sin símbolo %")
    R.add("bootstrap.percentil_inf", lo, fm.num(lo, 1), "experiments/amenazas/desglose.py", f"np.percentile(rep, [{lo}, {hi}])",
          "Percentil inferior (%) del IC bootstrap")
    R.add("bootstrap.percentil_sup", hi, fm.num(hi, 1), "experiments/amenazas/desglose.py", f"np.percentile(rep, [{lo}, {hi}])",
          "Percentil superior (%) del IC bootstrap")


# ---------------------------------------------------------------------------------------
# R1 (inferencia adicional) y R2 (descriptivo): tdew-4w2 / tdew-ddx.
RIV = ("tuned", "tuned_sin_td", "llr_rezagos_sel", "llr_simple_sel")
ESQ_R1 = {"espacial_2g": "esp", "espaciotemporal_2g_anio": "esa", "temporal_trim_anio": "ta"}
ESQ_TXT = {"espacial_2g": "bloques espaciales de 2°", "espaciotemporal_2g_anio": "bloques de 2° × año",
           "temporal_trim_anio": "bloques trimestre-año"}
HORIZ_MESES = (1, 12, 24, 36, 48)
BANDAS = {"0-500": "b0_500", "500-1500": "b500_1500", "1500-2500": "b1500_2500", "2500-3500": "b2500_3500",
          ">3500": "b3500_mas", "fuera_peru": "fuera_peru", "peru": "peru"}
BANDA_TXT = {"0-500": "0–500 m", "500-1500": "500–1.500 m", "1500-2500": "1.500–2.500 m", "2500-3500": "2.500–3.500 m",
             ">3500": "más de 3.500 m", "fuera_peru": "fuera de Perú", "peru": "dentro de Perú"}
ENSO_TXT = {"el_nino": "El Niño", "la_nina": "La Niña", "neutral": "neutral"}
CLASE_EXT = {"inferior_5": "inf5", "superior_5": "sup5", "resto": "resto"}
CLASE_EXT_TXT = {"inferior_5": "5 % inferior de la anomalía observada", "superior_5": "5 % superior de la anomalía observada",
                 "resto": "90 % central"}


def fp(p: float) -> str:
    """p-valor en espanol: tres decimales, o «< 0,001»."""
    return f"<{fm.NBSP}0,001" if p < 0.001 else fm.num(p, 3)


def _una(df: pd.DataFrame, **kw) -> pd.Series:
    sel = df
    for k, v in kw.items():
        sel = sel[sel[k] == v]
    if len(sel) != 1:
        raise ValueError(f"se esperaba una fila para {kw}, hay {len(sel)}")
    return sel.iloc[0]


def _r1(R: Registro, d: Datos) -> None:
    H, BT, DM = F.rel(F.R1_HORIZONTE), F.rel(F.R1_BOOT), F.rel(F.R1_DM)
    # --- Horizonte: brecha por mes desde el inicio del bloque (1..48) y por año del bloque (1..4)
    h = d.r1_horizonte
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIV:
                k = f"horizonte.{s}.{a}.{r}"
                flt = f"split={s}; ambito={a}; metodo_b={r}"
                ctx = f"TimesFM − {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}"
                sub = h[(h.split == s) & (h.ambito == a) & (h.metodo_b == r)]
                an = sub[sub.unidad == "anio"].set_index("horizonte").sort_index()
                me = sub[sub.unidad == "mes"].set_index("horizonte").sort_index()
                R.verificar(f"horizonte {s}/{a}/{r}: 4 años y 48 meses", len(an) == 4 and len(me) == 48)
                for y, x in an.iterrows():
                    R.add(f"{k}.anio{y}.v", x.brecha, fm.num(x.brecha, 3, True), H, flt + f"; unidad=anio; horizonte={y}; col=brecha",
                          f"Brecha (°C) en el año {y} del bloque, {ctx}")
                    R.add(f"{k}.anio{y}.ic", None, fm.ic(x.ic_lo, x.ic_hi), H, flt + f"; unidad=anio; horizonte={y}",
                          f"IC 95 % (bloques espaciales de 2°) de la brecha en el año {y} del bloque, {ctx}")
                    excl = not (x.ic_lo <= 0 <= x.ic_hi)
                    R.add(f"{k}.anio{y}.excluye_cero", int(excl), si_no(excl), H, flt + f"; unidad=anio; horizonte={y}",
                          f"¿El IC del año {y} del bloque excluye cero? {ctx}")
                    R.add(f"{k}.anio{y}.n", x.n, fm.ent(x.n), H, flt + f"; unidad=anio; horizonte={y}; col=n", f"Filas celda × día del año {y} del bloque")
                pos = [int(y) for y, x in an.iterrows() if x.brecha > 0]
                R.add(f"{k}.anios_positivos", len(pos), lista_es(pos), H, flt + "; unidad=anio; brecha > 0",
                      f"Años del bloque con brecha positiva (TimesFM peor), {ctx}")
                R.add(f"{k}.anio1_positivo", int(1 in pos), si_no(1 in pos), H, flt + "; unidad=anio; horizonte=1",
                      f"¿La brecha del primer año del bloque es positiva (TimesFM peor)? {ctx}")
                for m in HORIZ_MESES:
                    x = me.loc[m]
                    R.add(f"{k}.mes{m}.v", x.brecha, fm.num(x.brecha, 3, True), H, flt + f"; unidad=mes; horizonte={m}; col=brecha",
                          f"Brecha (°C) en el mes {m} desde el inicio del bloque, {ctx}")
                    R.add(f"{k}.mes{m}.ic", None, fm.ic(x.ic_lo, x.ic_hi), H, flt + f"; unidad=mes; horizonte={m}",
                          f"IC 95 % (bloques espaciales de 2°) de la brecha del mes {m}, {ctx}")
                neg = int((me.brecha < 0).sum())
                excl_neg = int((me.ic_hi < 0).sum())
                excl_pos = int((me.ic_lo > 0).sum())
                R.add(f"{k}.meses_neg", neg, fm.ent(neg), H, flt + "; unidad=mes; brecha < 0", f"Meses (de 48) con brecha negativa, {ctx}")
                R.add(f"{k}.meses_ic_neg", excl_neg, fm.ent(excl_neg), H, flt + "; unidad=mes; ic_hi < 0",
                      f"Meses (de 48) con IC 95 % enteramente por debajo de cero, {ctx}")
                R.add(f"{k}.meses_ic_pos", excl_pos, fm.ent(excl_pos), H, flt + "; unidad=mes; ic_lo > 0",
                      f"Meses (de 48) con IC 95 % enteramente por encima de cero, {ctx}")
                R.add(f"{k}.meses_ic_incluye", 48 - excl_neg - excl_pos, fm.ent(48 - excl_neg - excl_pos), H, flt + "; unidad=mes; IC con cero",
                      f"Meses (de 48) con IC 95 % que incluye cero, {ctx}")
                mmin, mmax = int(me.brecha.idxmin()), int(me.brecha.idxmax())
                R.add(f"{k}.mes_mayor_ventaja", mmin, str(mmin), H, flt + "; unidad=mes; argmin(brecha)", f"Mes con la brecha más negativa, {ctx}")
                R.add(f"{k}.brecha_mayor_ventaja", me.brecha[mmin], fm.num(me.brecha[mmin], 3, True), H, flt + "; unidad=mes; min(brecha)",
                      f"Brecha del mes con la brecha más negativa, {ctx}")
                R.add(f"{k}.mes_menor_ventaja", mmax, str(mmax), H, flt + "; unidad=mes; argmax(brecha)", f"Mes con la brecha menos negativa (o más positiva), {ctx}")
                R.add(f"{k}.brecha_menor_ventaja", me.brecha[mmax], fm.num(me.brecha[mmax], 3, True), H, flt + "; unidad=mes; max(brecha)",
                      f"Brecha del mes con la brecha menos negativa, {ctx}")
                m1 = float(me.brecha.iloc[:12].mean())
                m4 = float(me.brecha.iloc[-12:].mean())
                R.add(f"{k}.media_mes1_12", m1, fm.num(m1, 3, True), H, flt + "; unidad=mes; media simple de los meses 1–12",
                      f"Media simple de las brechas mensuales de los meses 1–12 (descriptiva), {ctx}")
                R.add(f"{k}.media_mes37_48", m4, fm.num(m4, 3, True), H, flt + "; unidad=mes; media simple de los meses 37–48",
                      f"Media simple de las brechas mensuales de los meses 37–48 (descriptiva), {ctx}")
    # --- Bootstrap alternativo: espacial 2° (control), 2° × año y trimestre-año
    b = d.r1_boot
    puntual = d.brechas.query("esquema == 'espacial_2g'").set_index(["split", "ambito", "metodo_a", "metodo_b"]).brecha
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIV:
                k0 = f"robustez.{s}.{a}.{r}"
                ctx = f"TimesFM − {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}"
                v = None
                for esq, p in ESQ_R1.items():
                    x = _una(b, split=s, ambito=a, metodo_b=r, esquema=esq)
                    flt = f"split={s}; ambito={a}; metodo_b={r}; esquema={esq}"
                    if v is None:
                        v = float(x.brecha)
                        R.verificar(f"brecha puntual de r1_bootstrap = a1_brechas: {s} {a} {r}", abs(v - puntual[(s, a, "timesfm_anom", r)]) < 1e-5)
                        R.add(f"{k0}.v", v, fm.num(v, 3, True), BT, flt + "; col=brecha", f"Brecha puntual (°C), {ctx}")
                    else:
                        R.verificar(f"brecha puntual idéntica entre esquemas r1: {s} {a} {r} {esq}", abs(v - float(x.brecha)) < 1e-9)
                    n = ESQ_TXT[esq]
                    R.add(f"{k0}.{p}_lo", x.ic_lo, fm.num(x.ic_lo, 3, True), BT, flt + "; col=ic_lo", f"Límite inferior IC 95 % ({n}), {ctx}")
                    R.add(f"{k0}.{p}_hi", x.ic_hi, fm.num(x.ic_hi, 3, True), BT, flt + "; col=ic_hi", f"Límite superior IC 95 % ({n}), {ctx}")
                    R.add(f"{k0}.{p}_ic", None, fm.ic(x.ic_lo, x.ic_hi), BT, flt, f"IC 95 % ({n}) como texto, {ctx}")
                    ex = not (x.ic_lo <= 0 <= x.ic_hi)
                    R.add(f"{k0}.{p}_excluye_cero", int(ex), si_no(ex), BT, flt, f"¿El IC ({n}) excluye cero? {ctx}")
                    R.add(f"{k0}.{p}_bloques", x.bloques, fm.ent(x.bloques), BT, flt + "; col=bloques", f"Bloques del esquema ({n}), {ctx}")
                    R.add(f"{k0}.{p}_bloques_a_gana", x.bloques_a_gana, fm.ent(x.bloques_a_gana), BT, flt + "; col=bloques_a_gana",
                          f"Bloques en que TimesFM gana ({n}), {ctx}")
    # Conteos «de N comparaciones, M excluyen cero» por esquema, bloque y ámbito
    for esq, p in ESQ_R1.items():
        tot = [(s, a, r) for s in SPLITS for a in AMBITOS for r in RIV]
        ok = [t for t in tot if R.num(f"robustez.{t[0]}.{t[1]}.{t[2]}.{p}_excluye_cero") == 1]
        flt = f"esquema={esq}; IC sin cero"
        R.add(f"robustez_conteo.{p}.n_comparaciones", len(tot), str(len(tot)), BT, flt, f"Comparaciones (bloque × ámbito × rival) bajo {ESQ_TXT[esq]}")
        R.add(f"robustez_conteo.{p}.n_excluyen", len(ok), str(len(ok)), BT, flt, f"Comparaciones cuyo IC excluye cero bajo {ESQ_TXT[esq]}")
        R.add(f"robustez_conteo.{p}.texto", len(ok), f"{len(ok)} de {len(tot)}", BT, flt, f"«M de N» comparaciones con IC sin cero bajo {ESQ_TXT[esq]}")
        for s in SPLITS:
            for a in AMBITOS:
                sub = [t for t in tot if t[0] == s and t[1] == a]
                okk = [t for t in sub if t in ok]
                inc = [NOMBRE[t[2]] for t in sub if t not in ok]
                k = f"robustez_conteo.{p}.{s}.{a}"
                R.add(f"{k}.n_comparaciones", len(sub), str(len(sub)), BT, flt + f"; split={s}; ambito={a}", f"Rivales comparados en {_en(s, a)}")
                R.add(f"{k}.n_excluyen", len(okk), str(len(okk)), BT, flt + f"; split={s}; ambito={a}",
                      f"Rivales cuyo IC ({ESQ_TXT[esq]}) excluye cero en {_en(s, a)}")
                R.add(f"{k}.texto", len(okk), f"{len(okk)} de {len(sub)}", BT, flt + f"; split={s}; ambito={a}",
                      f"«M de N» rivales con IC sin cero ({ESQ_TXT[esq]}) en {_en(s, a)}")
                R.add(f"{k}.incluyen", len(inc), lista_es(inc), BT, flt + f"; split={s}; ambito={a}",
                      f"Rivales cuyo IC ({ESQ_TXT[esq]}) incluye cero en {_en(s, a)}")
    # --- Diebold-Mariano
    dm = d.r1_dm
    fam = sorted(dm.familia.unique())
    R.verificar("DM: familia única de 16", fam == [16])
    R.add("dm.familia", int(fam[0]), str(int(fam[0])), DM, "col=familia", "Pruebas por regla de rezago en la familia de Holm (bloque × ámbito × rival)")
    R.add("dm.rezago_corto", 7, "7", DM, "regla_rezago=nw_auto; col=rezago", "Rezago Newey-West automático, floor(4 (T/100)^(2/9)) con T = 1.461")
    R.add("dm.rezago_largo", 30, "30", DM, "regla_rezago=nw_30; col=rezago", "Rezago Newey-West largo")
    R.verificar("DM: reglas de rezago = {7, 30}", sorted(dm.rezago.unique()) == [7, 30])
    for x in dm.itertuples(index=False):
        k = f"dm.{x.split}.{x.ambito}.{x.metodo_b}.lag{x.rezago}"
        flt = f"split={x.split}; ambito={x.ambito}; metodo_b={x.metodo_b}; rezago={x.rezago}"
        ctx = f"TimesFM − {NOMBRE[x.metodo_b]}, `{x.split}`, {AMBITO_TXT[x.ambito]}, rezago {x.rezago}"
        R.add(f"{k}.T", x.T, fm.ent(x.T), DM, flt + "; col=T", f"Días de la serie diaria de diferencial de pérdida, {ctx}")
        R.add(f"{k}.perdida_media", x.perdida_media, fm.num(x.perdida_media, 3, True), DM, flt + "; col=perdida_media",
              f"Diferencial medio diario de error cuadrático medio por celda (°C²), {ctx}")
        R.add(f"{k}.dm", x.dm, fm.num(x.dm, 2, True), DM, flt + "; col=dm", f"Estadístico DM, {ctx}")
        R.add(f"{k}.dm_hln", x.dm_hln, fm.num(x.dm_hln, 2, True), DM, flt + "; col=dm_hln", f"Estadístico DM con corrección HLN, {ctx}")
        R.add(f"{k}.p_normal", x.p_normal, fp(x.p_normal), DM, flt + "; col=p_normal", f"p bilateral con normal, {ctx}")
        R.add(f"{k}.p_hln", x.p_hln, fp(x.p_hln), DM, flt + "; col=p_hln", f"p bilateral HLN (t de T−1 gl), sin ajuste, {ctx}")
        R.add(f"{k}.p_holm", x.p_holm, fp(x.p_holm), DM, flt + "; col=p_holm", f"p HLN ajustado por Holm sobre la familia de 16, {ctx}")
        R.add(f"{k}.p_holm_sci", x.p_holm, fm.sci(x.p_holm, 2), DM, flt + "; col=p_holm", f"p ajustado por Holm en notación científica, {ctx}")
        R.add(f"{k}.sig05", int(x.p_holm < 0.05), si_no(x.p_holm < 0.05), DM, flt + "; p_holm < 0,05", f"¿p de Holm menor que 0,05? {ctx}")
    for lag in (7, 30):
        sub = dm[dm.rezago == lag]
        ok = sub[sub.p_holm < 0.05]
        k = f"dm_conteo.lag{lag}"
        flt = f"rezago={lag}; p_holm < 0,05"
        R.add(f"{k}.n", len(sub), str(len(sub)), DM, flt, f"Pruebas DM con rezago {lag}")
        R.add(f"{k}.n_holm05", len(ok), str(len(ok)), DM, flt, f"Pruebas DM con rezago {lag} y p de Holm menor que 0,05")
        R.add(f"{k}.texto", len(ok), f"{len(ok)} de {len(sub)}", DM, flt, f"«M de N» pruebas DM con p de Holm menor que 0,05 (rezago {lag})")
        for s in SPLITS:
            for a in AMBITOS:
                ss = sub[(sub.split == s) & (sub.ambito == a)]
                ko = ss[ss.p_holm >= 0.05]
                kk = f"{k}.{s}.{a}"
                R.add(f"{kk}.n_holm05", int((ss.p_holm < 0.05).sum()), str(int((ss.p_holm < 0.05).sum())), DM, flt + f"; split={s}; ambito={a}",
                      f"Rivales con p de Holm menor que 0,05 en {_en(s, a)}, rezago {lag}")
                R.add(f"{kk}.no_signif", len(ko), lista_es([NOMBRE[m] for m in ko.metodo_b]), DM, flt + f"; split={s}; ambito={a}",
                      f"Rivales sin significancia (p de Holm ≥ 0,05) en {_en(s, a)}, rezago {lag}")


def _r2(R: Registro, d: Datos) -> None:
    SK, EX, CA, AL, ZD, EN = (F.rel(p) for p in (F.R2_SKILL, F.R2_EXTREMOS, F.R2_CALIBRACION, F.R2_ALTITUD, F.R2_ZONA_DOM, F.R2_ENSO))
    # --- Habilidad, razón de varianzas y correlación de anomalías
    sk = d.r2_skill.set_index(["split", "ambito", "metodo"])
    for (s, a, m), x in sk.iterrows():
        k = f"skill.{s}.{a}.{alias(m)}"
        flt = f"split={s}; ambito={a}; metodo={m}"
        ctx = f"{NOMBRE[m]}, `{s}`, {AMBITO_TXT[a]}"
        R.add(f"{k}.skill", x.skill_mse, fm.num(x.skill_mse, 3), SK, flt + "; col=skill_mse", f"Habilidad 1 − MSE/MSE(climatología), {ctx}")
        R.add(f"{k}.razon_varianza", x.razon_varianza, fm.num(x.razon_varianza, 3), SK, flt + "; col=razon_varianza",
              f"Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), {ctx}")
        R.add(f"{k}.razon_desv", x.razon_desv, fm.num(x.razon_desv, 3), SK, flt + "; col=razon_desv", f"Razón de desviaciones estándar de las anomalías, {ctx}")
        R.add(f"{k}.skill_celda_media", x.skill_celda_media, fm.num(x.skill_celda_media, 3), SK, flt + "; col=skill_celda_media", f"Media entre celdas de la habilidad por celda, {ctx}")
        R.add(f"{k}.skill_celda_mediana", x.skill_celda_mediana, fm.num(x.skill_celda_mediana, 3), SK, flt + "; col=skill_celda_mediana",
              f"Mediana entre celdas de la habilidad por celda, {ctx}")
        if x.corr_anomalia == x.corr_anomalia:
            R.add(f"{k}.corr", x.corr_anomalia, fm.num(x.corr_anomalia, 3), SK, flt + "; col=corr_anomalia", f"Correlación de las anomalías predicha y observada, {ctx}")
        else:
            R.verificar(f"corr indefinida solo para la climatología: {s} {a} {m}", m == "clim")  # anomalía predicha nula
    for s in SPLITS:
        for a in AMBITOS:
            x = sk.loc[(s, a, "clim")]
            t = sk.loc[(s, a, "timesfm_anom")]
            R.add(f"skill.{s}.{a}.mse_clim", x.mse_clim, fm.num(x.mse_clim, 3), SK, f"split={s}; ambito={a}; col=mse_clim", f"MSE de la climatología (°C²), `{s}`, {AMBITO_TXT[a]}")
            R.add(f"skill.{s}.{a}.mse_timesfm", t.mse, fm.num(t.mse, 3), SK, f"split={s}; ambito={a}; col=mse", f"MSE de TimesFM (°C²), `{s}`, {AMBITO_TXT[a]}")
            for r in RIV:
                k = f"skill_dif.{s}.{a}.timesfm_vs_{r}"
                q = sk.loc[(s, a, r)]
                flt = f"split={s}; ambito={a}; timesfm_anom − {r}"
                R.add(f"{k}.skill", t.skill_mse - q.skill_mse, fm.num(t.skill_mse - q.skill_mse, 3, True), SK, flt, f"Habilidad de TimesFM − habilidad de {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}")
                R.add(f"{k}.razon_varianza", t.razon_varianza - q.razon_varianza, fm.num(t.razon_varianza - q.razon_varianza, 3, True), SK, flt,
                      f"Razón de varianzas de TimesFM − la de {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}")
                R.add(f"{k}.corr", t.corr_anomalia - q.corr_anomalia, fm.num(t.corr_anomalia - q.corr_anomalia, 3, True), SK, flt,
                      f"Correlación de anomalías de TimesFM − la de {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}")
            cinco = ["timesfm_anom", *RIV]
            mejor_rv = max(cinco, key=lambda m: sk.loc[(s, a, m)].razon_varianza)
            mejor_c = max(cinco, key=lambda m: sk.loc[(s, a, m)].corr_anomalia)
            R.add(f"skill_max.{s}.{a}.razon_varianza", None, NOMBRE[mejor_rv], SK, f"split={s}; ambito={a}; argmax(razon_varianza) entre 5 métodos",
                  f"Método con mayor razón de varianzas, `{s}`, {AMBITO_TXT[a]}")
            R.add(f"skill_max.{s}.{a}.corr", None, NOMBRE[mejor_c], SK, f"split={s}; ambito={a}; argmax(corr_anomalia) entre 5 métodos",
                  f"Método con mayor correlación de anomalías, `{s}`, {AMBITO_TXT[a]}")
    # --- Extremos
    ex = d.r2_extremos.set_index(["split", "ambito", "clase", "metodo"])
    for (s, a, c, m), x in ex.iterrows():
        k = f"extremos.{s}.{a}.{CLASE_EXT[c]}.{alias(m)}"
        flt = f"split={s}; ambito={a}; clase={c}; metodo={m}"
        ctx = f"{NOMBRE[m]}, {CLASE_EXT_TXT[c]}, `{s}`, {AMBITO_TXT[a]}"
        R.add(f"{k}.rmse", x.rmse, fm.num(x.rmse, 3), EX, flt + "; col=rmse", f"RMSE (°C), {ctx}")
        R.add(f"{k}.sesgo", x.sesgo, fm.num(x.sesgo, 3, True), EX, flt + "; col=sesgo", f"Sesgo (°C), {ctx}")
        if m == "timesfm_anom":
            R.add(f"extremos.{s}.{a}.{CLASE_EXT[c]}.n", x.n, fm.ent(x.n), EX, flt + "; col=n", f"Filas celda × día, {CLASE_EXT_TXT[c]}, `{s}`, {AMBITO_TXT[a]}")
    for s in SPLITS:
        for a in AMBITOS:
            for c in CLASE_EXT:
                for r in RIV:
                    g = ex.loc[(s, a, c, "timesfm_anom")].rmse - ex.loc[(s, a, c, r)].rmse
                    R.add(f"extremos.{s}.{a}.{CLASE_EXT[c]}.brecha.{r}", g, fm.num(g, 3, True), EX, f"split={s}; ambito={a}; clase={c}; rmse(timesfm_anom) − rmse({r})",
                          f"Brecha (°C) TimesFM − {NOMBRE[r]}, {CLASE_EXT_TXT[c]}, `{s}`, {AMBITO_TXT[a]}")
            n_ext = int(ex.loc[(s, a, "inferior_5", "timesfm_anom")].n + ex.loc[(s, a, "superior_5", "timesfm_anom")].n)
            n_tot = n_ext + int(ex.loc[(s, a, "resto", "timesfm_anom")].n)
            R.add(f"extremos.{s}.{a}.pct_extremos", 100 * n_ext / n_tot, fm.num(100 * n_ext / n_tot, 1), EX, f"split={s}; ambito={a}; (n inf5 + n sup5) / n total",
                  f"Porcentaje de filas en las dos colas (sin símbolo %), `{s}`, {AMBITO_TXT[a]}")
            for r in RIV:
                ok = all(ex.loc[(s, a, c, "timesfm_anom")].rmse < ex.loc[(s, a, c, r)].rmse for c in ("inferior_5", "superior_5"))
                R.add(f"extremos.{s}.{a}.colas_favorecen.{r}", int(ok), si_no(ok), EX, f"split={s}; ambito={a}; rmse timesfm < rmse {r} en inf5 y sup5",
                      f"¿TimesFM tiene menor RMSE que {NOMBRE[r]} en las dos colas? `{s}`, {AMBITO_TXT[a]}")
    # --- Calibración de los cuantiles de TimesFM (intervalo 80 % = q10–q90)
    R.add("calib.nominal", 80, "80", CA, "intervalo q10–q90 de TimesFM", "Cobertura nominal (%) del intervalo q10–q90")
    R.add("calib.cola_nominal", 10, "10", CA, "fracción esperada bajo q10 y sobre q90", "Fracción nominal (%) de cada cola (bajo q10, sobre q90)")
    for x in d.r2_calibracion.itertuples(index=False):
        per = "total" if str(x.periodo) == "total" else f"a{x.periodo}"
        k = f"calib.{x.split}.{x.ambito}.{per}"
        flt = f"split={x.split}; ambito={x.ambito}; periodo={x.periodo}"
        ctx = f"`{x.split}`, {AMBITO_TXT[x.ambito]}, {'total' if per == 'total' else 'año ' + str(x.periodo)}"
        R.add(f"{k}.n", x.n, fm.ent(x.n), CA, flt + "; col=n", f"Filas celda × día, {ctx}")
        R.add(f"{k}.cobertura", 100 * x.cobertura_80, fm.num(100 * x.cobertura_80, 1), CA, flt + "; 100 × cobertura_80", f"Cobertura empírica del intervalo 80 % (%, sin símbolo), {ctx}")
        R.add(f"{k}.anchura", x.anchura_80, fm.num(x.anchura_80, 2), CA, flt + "; col=anchura_80", f"Anchura media del intervalo 80 % (°C), {ctx}")
        R.add(f"{k}.crps", x.crps_aprox, fm.num(x.crps_aprox, 3), CA, flt + "; col=crps_aprox", f"CRPS aproximado por cuadratura de pinball (°C), {ctx}")
        R.add(f"{k}.pinball", x.pinball_medio, fm.num(x.pinball_medio, 3), CA, flt + "; col=pinball_medio", f"Pinball medio de los nueve cuantiles (°C), {ctx}")
        R.add(f"{k}.frac_bajo_q10", 100 * x.frac_bajo_q10, fm.num(100 * x.frac_bajo_q10, 1), CA, flt + "; 100 × frac_bajo_q10", f"Observaciones bajo q10 (%, sin símbolo), {ctx}")
        R.add(f"{k}.frac_sobre_q90", 100 * x.frac_sobre_q90, fm.num(100 * x.frac_sobre_q90, 1), CA, flt + "; 100 × frac_sobre_q90", f"Observaciones sobre q90 (%, sin símbolo), {ctx}")
        if per == "total":
            for j in range(10):
                v = getattr(x, f"pit_frac_{j}")
                R.add(f"{k}.pit{j}", 100 * v, fm.num(100 * v, 1), CA, flt + f"; 100 × pit_frac_{j}",
                      f"Observaciones en el decil {j + 1} de la predicción (%, sin símbolo; 10 % nominal), {ctx}")
    # --- Altitud
    ali = d.r2_altitud.set_index(["split", "ambito", "estrato", "metodo"])
    for (s, a, e, m), x in ali.iterrows():
        if m == "clim":
            continue
        k = f"altitud.{s}.{a}.{BANDAS[e]}"
        flt = f"split={s}; ambito={a}; estrato={e}; metodo={m}"
        ctx = f"{NOMBRE[m]}, {BANDA_TXT[e]}, `{s}`, {AMBITO_TXT[a]}"
        R.add(f"{k}.rmse.{alias(m)}", x.rmse, fm.num(x.rmse, 3), AL, flt + "; col=rmse", f"RMSE (°C), {ctx}")
        R.add(f"{k}.sesgo.{alias(m)}", x.sesgo, fm.num(x.sesgo, 3, True), AL, flt + "; col=sesgo", f"Sesgo (°C), {ctx}")
        if m == "timesfm_anom":
            R.add(f"{k}.celdas", x.celdas, fm.ent(x.celdas), AL, flt + "; col=celdas", f"Celdas, {BANDA_TXT[e]}, `{s}`, {AMBITO_TXT[a]}")
            R.add(f"{k}.n", x.n, fm.ent(x.n), AL, flt + "; col=n", f"Filas celda × día, {BANDA_TXT[e]}, `{s}`, {AMBITO_TXT[a]}")
        else:
            R.add(f"{k}.brecha.{m}", x.brecha_tfm_menos_metodo, fm.num(x.brecha_tfm_menos_metodo, 3, True), AL, flt + "; col=brecha_tfm_menos_metodo",
                  f"Brecha (°C) TimesFM − {NOMBRE[m]}, {BANDA_TXT[e]}, `{s}`, {AMBITO_TXT[a]}")
    bandas5 = [e for e in BANDAS if e not in ("fuera_peru", "peru")]
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIV:
                g = {e: float(ali.loc[(s, a, e, r)].brecha_tfm_menos_metodo) for e in bandas5}
                emin, emax = min(g, key=g.get), max(g, key=g.get)
                k = f"altitud.{s}.{a}.vs_{r}"
                flt = f"split={s}; ambito={a}; brecha por banda de altitud vs {r}"
                ctx = f"frente a {NOMBRE[r]}, `{s}`, {AMBITO_TXT[a]}"
                R.add(f"{k}.banda_max_ventaja", None, BANDA_TXT[emin], AL, flt, f"Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) {ctx}")
                R.add(f"{k}.brecha_max_ventaja", g[emin], fm.num(g[emin], 3, True), AL, flt, f"Brecha en la banda de mayor ventaja {ctx}")
                R.add(f"{k}.banda_min_ventaja", None, BANDA_TXT[emax], AL, flt, f"Banda con la brecha menos negativa (menor ventaja) {ctx}")
                R.add(f"{k}.brecha_min_ventaja", g[emax], fm.num(g[emax], 3, True), AL, flt, f"Brecha en la banda de menor ventaja {ctx}")
                npos = sum(v > 0 for v in g.values())
                R.add(f"{k}.n_bandas_positivas", npos, str(npos), AL, flt, f"Bandas (de 5) con brecha positiva (TimesFM peor) {ctx}")
                R.add(f"{k}.n_bandas_negativas", len(g) - npos, str(len(g) - npos), AL, flt + "; brecha ≤ 0", f"Bandas (de 5) con brecha no positiva {ctx}")
            R.verificar(f"altitud {s}/{a}: las 5 bandas suman las celdas del ámbito",
                        sum(int(ali.loc[(s, a, e, "timesfm_anom")].celdas) for e in bandas5) == int(R.num(f"celdas.{s}.{a}")))
    # --- Peso de la zona dominante
    zd = d.r2_zona_dom.set_index(["split", "ambito", "metodo"])
    for s in SPLITS:
        for a in AMBITOS:
            x = zd.loc[(s, a, "timesfm_anom")]
            k = f"zdom.{s}.{a}"
            flt = f"split={s}; ambito={a}"
            ctx = f"`{s}`, {AMBITO_TXT[a]}"
            R.add(f"{k}.etiqueta", None, str(x.zona_dominante), ZD, flt + "; col=zona_dominante", f"Zona SENAMHI con más celdas, {ctx}")
            R.add(f"{k}.celdas_zona", x.celdas_zona, fm.ent(x.celdas_zona), ZD, flt + "; col=celdas_zona", f"Celdas de la zona dominante, {ctx}")
            R.add(f"{k}.celdas_ambito", x.celdas_ambito, fm.ent(x.celdas_ambito), ZD, flt + "; col=celdas_ambito", f"Celdas del ámbito, {ctx}")
            R.add(f"{k}.pct_celdas", 100 * x.frac_celdas, fm.num(100 * x.frac_celdas, 1), ZD, flt + "; 100 × frac_celdas", f"Porcentaje de celdas en la zona dominante (sin símbolo %), {ctx}")
            R.add(f"{k}.pct_filas", 100 * x.frac_filas, fm.num(100 * x.frac_filas, 1), ZD, flt + "; 100 × frac_filas", f"Porcentaje de filas celda × día en la zona dominante (sin símbolo %), {ctx}")
            for m in ("timesfm_anom", *RIV, "clim"):
                y = zd.loc[(s, a, m)]
                kk = f"{k}.{alias(m)}"
                R.add(f"{kk}.rmse_total", y.rmse_total, fm.num(y.rmse_total, 3), ZD, flt + f"; metodo={m}; col=rmse_total", f"RMSE total (°C), {NOMBRE[m]}, {ctx}")
                R.add(f"{kk}.rmse_zona", y.rmse_zona, fm.num(y.rmse_zona, 3), ZD, flt + f"; metodo={m}; col=rmse_zona", f"RMSE dentro de la zona dominante (°C), {NOMBRE[m]}, {ctx}")
                R.add(f"{kk}.rmse_sin_zona", y.rmse_sin_zona, fm.num(y.rmse_sin_zona, 3), ZD, flt + f"; metodo={m}; col=rmse_sin_zona", f"RMSE sin la zona dominante (°C), {NOMBRE[m]}, {ctx}")
                R.add(f"{kk}.pct_sse_zona", 100 * y.frac_sse_zona, fm.num(100 * y.frac_sse_zona, 1), ZD, flt + f"; metodo={m}; 100 × frac_sse_zona",
                      f"Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), {NOMBRE[m]}, {ctx}")
            for r in RIV:
                y = zd.loc[(s, a, r)]
                kk = f"{k}.brecha.{r}"
                R.add(f"{kk}.total", y.brecha_total, fm.num(y.brecha_total, 3, True), ZD, flt + f"; metodo={r}; col=brecha_total", f"Brecha total (°C) TimesFM − {NOMBRE[r]}, {ctx}")
                R.add(f"{kk}.zona", y.brecha_zona, fm.num(y.brecha_zona, 3, True), ZD, flt + f"; metodo={r}; col=brecha_zona", f"Brecha (°C) TimesFM − {NOMBRE[r]} dentro de la zona dominante, {ctx}")
                R.add(f"{kk}.sin_zona", y.brecha_sin_zona, fm.num(y.brecha_sin_zona, 3, True), ZD, flt + f"; metodo={r}; col=brecha_sin_zona",
                      f"Brecha (°C) TimesFM − {NOMBRE[r]} sin la zona dominante, {ctx}")
                R.add(f"{kk}.sin_zona_favorece", int(y.brecha_sin_zona < 0), si_no(y.brecha_sin_zona < 0), ZD, flt + f"; metodo={r}; brecha_sin_zona < 0",
                      f"¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a {NOMBRE[r]}? {ctx}")
            n_f = sum(zd.loc[(s, a, r)].brecha_sin_zona < 0 for r in RIV)
            R.add(f"{k}.n_rivales_sin_zona_favorece", int(n_f), str(int(n_f)), ZD, flt + "; brecha_sin_zona < 0", f"Rivales (de 4) frente a los que TimesFM sigue ganando sin la zona dominante, {ctx}")
    # --- ENSO
    en = d.r2_enso.set_index(["split", "ambito", "estrato", "metodo"])
    for s in SPLITS:
        for a in AMBITOS:
            tot_m = 0
            for c in ENSO_TXT:
                x = en.loc[(s, a, c, "timesfm_anom")]
                k = f"enso.{s}.{a}.{c}"
                flt = f"split={s}; ambito={a}; estrato={c}"
                ctx = f"{ENSO_TXT[c]}, `{s}`, {AMBITO_TXT[a]}"
                tot_m += int(x.meses)
                R.add(f"{k}.meses", x.meses, fm.ent(x.meses), EN, flt + "; col=meses", f"Meses de la clase ONI, {ctx}")
                R.add(f"{k}.n", x.n, fm.ent(x.n), EN, flt + "; col=n", f"Filas celda × día de la clase, {ctx}")
                R.add(f"{k}.celdas", x.celdas, fm.ent(x.celdas), EN, flt + "; col=celdas", f"Celdas con filas en la clase, {ctx}")
                for m in ("timesfm_anom", *RIV, "clim"):
                    y = en.loc[(s, a, c, m)]
                    R.add(f"{k}.rmse.{alias(m)}", y.rmse, fm.num(y.rmse, 3), EN, flt + f"; metodo={m}; col=rmse", f"RMSE (°C), {NOMBRE[m]}, {ctx}")
                    R.add(f"{k}.sesgo.{alias(m)}", y.sesgo, fm.num(y.sesgo, 3, True), EN, flt + f"; metodo={m}; col=sesgo", f"Sesgo (°C), {NOMBRE[m]}, {ctx}")
                for r in RIV:
                    y = en.loc[(s, a, c, r)]
                    R.add(f"{k}.brecha.{r}", y.brecha_tfm_menos_metodo, fm.num(y.brecha_tfm_menos_metodo, 3, True), EN, flt + f"; metodo={r}; col=brecha_tfm_menos_metodo",
                          f"Brecha (°C) TimesFM − {NOMBRE[r]}, {ctx}")
            R.verificar(f"ENSO {s}/{a}: los meses de las tres clases suman los 48 del bloque", tot_m == 48)
            R.add(f"enso.{s}.{a}.meses_total", tot_m, str(tot_m), EN, f"split={s}; ambito={a}; suma de meses de las tres clases", f"Meses del bloque clasificados por ONI, `{s}`, {AMBITO_TXT[a]}")
            for r in RIV:
                n_neg = sum(en.loc[(s, a, c, r)].brecha_tfm_menos_metodo < 0 for c in ENSO_TXT)
                R.add(f"enso.{s}.{a}.n_clases_favorece.{r}", int(n_neg), str(int(n_neg)), EN, f"split={s}; ambito={a}; brecha < 0 en la clase vs {r}",
                      f"Clases ENSO (de 3) en que la brecha frente a {NOMBRE[r]} es negativa, `{s}`, {AMBITO_TXT[a]}")
    R.add("enso.umbral_oni", 0.5, "0,5", EN, "proveniencia: ONI ≥ 0,5 El Niño; ≤ −0,5 La Niña", "Umbral del ONI (°C) para clasificar los meses")


# Constantes de preentrenamiento y de decodificacion de TimesFM 3.0: valores de reports/paper_nuevo/notas_preentrenamiento.md,
# sin derivacion desde datos. Cada una cita la seccion de las notas (§1.4 = GiftEvalPretrain, §3.3-3.4 = decodificacion).
def _preentrenamiento(R: Registro, d: Datos) -> None:
    N = F.rel(F.NOTAS_PRE)
    notas = F.NOTAS_PRE.read_text(encoding="utf-8")
    for frag in ("`era5_1989` a `era5_2018`", "2,8125°", "64 × 128", "245.760 series, 45 variables", "2.146.959.000 puntos",
                 "`cmip6_1850` a `cmip6_2010`", "1.351.680 series, 53 variables", "8.192 ejemplos", "71 univariate and 17 multivariate",
                 "4.5 million time series and 230 billion", "152 carpetas", "`_MAX_CONTEXT_LENGTH`", "15.360 puntos",
                 "`ceil((1461 − 32)/32) = 45`", "1.472 (46 parches", "extract_len = min(2·32, 64) = 64", "parche de entrada 32 y de salida 64",
                 "máximo de 32 variates", "seven domains"):
        R.verificar(f"notas_preentrenamiento.md contiene «{frag}»", frag in notas)

    def c(clave, valor, texto, filtro, desc):
        R.add(clave, valor, texto, N, filtro, desc)

    c("preentrenamiento.reanalisis_anio_ini", 1989, "1989", "§1.4: carpetas `era5_1989` a `era5_2018`", "Primer año de ERA5 en GiftEvalPretrain")
    c("preentrenamiento.reanalisis_anio_fin", 2018, "2018", "§1.4: carpetas `era5_1989` a `era5_2018`", "Último año de ERA5 en GiftEvalPretrain")
    c("preentrenamiento.reanalisis_anios", 30, "30", "§1.4: «un directorio por año, 30 años»", "Años (directorios) de ERA5 en GiftEvalPretrain")
    c("preentrenamiento.reanalisis_grilla_grados", 2.8125, "2,8125", "§1.4: «2,8125° resolution … 64 × 128 grid»", "Resolución de la grilla de ERA5 y CMIP6 en LOTSA (°)")
    c("preentrenamiento.reanalisis_grilla", None, "64 × 128", "§1.4", "Dimensiones de la grilla (latitud × longitud)")
    c("preentrenamiento.reanalisis_celdas_por_anio", 8192, "8.192", "§1.4: «8.192 ejemplos de 45 canales» en `era5_2000`", "Series por año en ERA5 (64 × 128 celdas)")
    c("preentrenamiento.reanalisis_series", 245760, "245.760", "§1.4: tabla 14 de GIFT-Eval, ERA5", "Series de ERA5 en GIFT-Eval/LOTSA")
    c("preentrenamiento.reanalisis_variables", 45, "45", "§1.4: tabla 14 de GIFT-Eval, ERA5", "Variables (canales) de ERA5")
    c("preentrenamiento.reanalisis_puntos", 2146959000, "2.146.959.000", "§1.4: tabla 14 de GIFT-Eval, ERA5", "Puntos de tiempo de ERA5")
    c("preentrenamiento.reanalisis_frecuencia", None, "horaria", "§1.4: tabla 14 de GIFT-Eval, ERA5", "Frecuencia de ERA5 en GiftEvalPretrain")
    c("preentrenamiento.cmip6_anio_ini", 1850, "1850", "§1.4: carpetas `cmip6_1850` a `cmip6_2010`", "Primer año de CMIP6 en GiftEvalPretrain")
    c("preentrenamiento.cmip6_anio_fin", 2010, "2010", "§1.4: carpetas `cmip6_1850` a `cmip6_2010`", "Último año de CMIP6 en GiftEvalPretrain")
    c("preentrenamiento.cmip6_paso_anios", 5, "5", "§1.4: «cada 5 años»", "Paso (años) entre carpetas de CMIP6")
    c("preentrenamiento.cmip6_series", 1351680, "1.351.680", "§1.4: tabla 14 de GIFT-Eval, CMIP6", "Series de CMIP6")
    c("preentrenamiento.cmip6_variables", 53, "53", "§1.4: tabla 14 de GIFT-Eval, CMIP6", "Variables de CMIP6")
    c("preentrenamiento.gifteval_univariadas", 71, "71", "§1.4: ficha de GiftEvalPretrain", "Conjuntos univariados de GiftEvalPretrain")
    c("preentrenamiento.gifteval_multivariadas", 17, "17", "§1.4: ficha de GiftEvalPretrain", "Conjuntos multivariados de GiftEvalPretrain")
    c("preentrenamiento.gifteval_carpetas", 152, "152", "§1.4: listado del repositorio en el Hub", "Carpetas de GiftEvalPretrain en el Hub")
    c("preentrenamiento.gifteval_series_millones", 4.5, "4,5", "§1.4: «4.5 million time series»", "Series de GiftEvalPretrain (millones)")
    c("preentrenamiento.gifteval_puntos_miles_de_millones", 230, "230", "§1.4: «230 billion data points»", "Puntos de GiftEvalPretrain (miles de millones)")
    c("preentrenamiento.gifteval_dominios", 7, "7", "§1.4: «seven domains»", "Dominios de GiftEvalPretrain")
    c("preentrenamiento.parche_entrada", 32, "32", "§3.4: «parche de entrada 32 y de salida 64»", "Largo del parche de entrada (días)")
    c("preentrenamiento.parche_salida", 64, "64", "§3.4: «parche de entrada 32 y de salida 64»", "Largo del parche de salida (días)")
    c("preentrenamiento.solapamiento", 32, "32", "§3.4: «solapamiento 32»", "Solapamiento entre parches de salida (días)")
    t_dias = d.r1_dm["T"].unique()
    R.verificar("horizonte de 1.461 días = T de r1_diebold_mariano.csv", len(t_dias) == 1 and int(t_dias[0]) == 1461)
    c("preentrenamiento.horizonte_dias", 1461, fm.ent(1461), "§3.4 (1.461 días); verificado contra la columna T de r1_diebold_mariano.csv", "Horizonte decodificado (días)")
    n_parches = -(-(1461 - 32) // 32)
    R.verificar("n de parches = ceil((1461 − 32)/32) = 45", n_parches == 45)
    c("preentrenamiento.n_parches", n_parches, str(n_parches), "§3.4: ceil((1461 − 32)/32) = 45", "Parches de pronóstico que cubren el horizonte de 1.461 días")
    c("preentrenamiento.horizonte_relleno", 1472, fm.ent(1472), "§3.4: «se rellena a 1.472 (46 parches de horizonte)»", "Horizonte rellenado (días)")
    c("preentrenamiento.n_parches_horizonte", 46, "46", "§3.4: «46 parches de horizonte»", "Parches de horizonte tras el relleno")
    c("preentrenamiento.contexto_max", 15360, fm.ent(15360), "§3.4: `_MAX_CONTEXT_LENGTH` = 15.360 puntos", "Contexto máximo del código (días)")
    c("preentrenamiento.max_variates", 32, "32", "§3.3: «máximo de 32 variates»", "Máximo de series (variates) por pasada")


R3_ETAPAS = (("carga", "carga"), ("seleccion", "seleccion"), ("ajuste", "ajuste final"), ("total", "total"))


def r3_filas(d: Datos) -> dict[tuple[str, str, str], pd.Series]:
    """(método, bloque, etapa corta) -> fila de r3_costo_llr_sel.csv; exige exactamente una por clave."""
    out = {}
    for met in ("llr_simple_sel", "llr_rezagos_sel"):
        for blq in ("ll4b", "ll4"):
            for corta, pref in R3_ETAPAS:
                c = d.r3_costo
                sel = c[(c.metodo == met) & (c.bloque == blq) & c.etapa.str.startswith(pref)]
                if len(sel) != 1:
                    raise ValueError(f"fila r3 ambigua o ausente: {met} {blq} {corta} -> {len(sel)}")
                out[(met, blq, corta)] = sel.iloc[0]
    if len(out) != len(d.r3_costo):
        raise ValueError("r3_costo_llr_sel.csv tiene filas fuera de método x bloque x etapa")
    return out


def _r3(R: Registro, d: Datos) -> None:
    """Costo medido de los LLR seleccionados (r3_costo_llr_sel.csv). Opcional: sin el archivo quedan las claves n. d."""
    if d.r3_costo is None:
        return  # las claves `costo.llr_*_sel.tiempo` ya salen como n. d. desde _costo
    C = F.rel(F.R3_COSTO)
    rows = r3_filas(d)
    rc = costo_filas(d)
    tun = float(rc["tuned_ll4b_seleccion"].segundos_pared + rc["tuned_ll4b_ajuste"].segundos_pared)
    tfm = float(rc["timesfm_ll4b_inferencia"].segundos_pared + rc["timesfm_cribado"].segundos_pared)
    for met in ("llr_simple_sel", "llr_rezagos_sel"):
        for blq in ("ll4b", "ll4"):
            for corta, _ in R3_ETAPAS:
                r = rows[(met, blq, corta)]
                seg = float(r.segundos_pared)
                k = f"costo.{met}.{blq}.{corta}"
                flt = f"metodo={met}; bloque={blq}; etapa={r.etapa}"
                R.add(f"{k}.seg", seg, fm.num(seg, 1 if round(seg, 6) % 1 else 0), C, flt + "; col=segundos_pared", f"Segundos de pared, {met} {blq} {corta}")
                R.add(f"{k}.tiempo", seg, fm.dur(seg), C, flt + "; col=segundos_pared", f"Tiempo de pared legible, {met} {blq} {corta}")
                R.add(f"{k}.celdas", r.celdas, fm.ent(r.celdas), C, flt + "; col=celdas", "Celdas procesadas")
                cps = r.celdas / seg
                R.add(f"{k}.celdas_por_s", cps, fm.num(cps, 2), C, flt + "; col=celdas/segundos_pared", "Celdas por segundo")
                R.add(f"{k}.reproduce", r.reproduce_max_abs_diff, fm.num(r.reproduce_max_abs_diff, 1) if r.reproduce_max_abs_diff == 0 else fm.num(r.reproduce_max_abs_diff, 6),
                      C, flt + "; col=reproduce_max_abs_diff", "Diferencia absoluta máxima al reproducir la predicción de la selección")
            parts = sum(rows[(met, blq, e)].segundos_pared for e in ("carga", "seleccion", "ajuste"))
            R.verificar(f"{met} {blq}: suma de etapas ≈ total", abs(parts - rows[(met, blq, "total")].segundos_pared) < 1.0)
        hw = str(rows[(met, "ll4b", "total")].hardware)
        gpu = str(rows[(met, "ll4b", "total")].gpu)
        R.add(f"costo.{met}.hardware", None, hw, C, f"metodo={met}; col=hardware", "Hardware de la corrida")
        R.add(f"costo.{met}.gpu", None, "sin GPU" if gpu == "no" else gpu, C, f"metodo={met}; col=gpu", "Uso de GPU en la corrida")
        mx = max(float(rows[(met, b, e)].reproduce_max_abs_diff) for b in ("ll4b", "ll4") for e, _ in R3_ETAPAS)
        R.add(f"costo.{met}.reproduce_max", mx, fm.num(mx, 1) if mx == 0 else fm.num(mx, 6), C, f"metodo={met}; max(col=reproduce_max_abs_diff)", "Diferencia absoluta máxima de reproducción (todas las filas)")
        R.add(f"costo.{met}.reproduce_texto", mx,
              "reproduce la predicción con diferencia absoluta máxima de " + (fm.num(mx, 1) if mx == 0 else fm.num(mx, 6)),
              C, f"metodo={met}; max(col=reproduce_max_abs_diff)", "Texto de la verificación de reproducción")
        t = float(rows[(met, "ll4b", "total")].segundos_pared)
        R.add(f"costo.{met}.tiempo", t, fm.dur(t), C, f"metodo={met}; bloque=ll4b; etapa=total; col=segundos_pared", f"Tiempo total de `{met}` en `ll4b`")
        R.add(f"costo.{met}.seg", t, fm.num(t, 1 if round(t, 6) % 1 else 0), C, f"metodo={met}; bloque=ll4b; etapa=total; col=segundos_pared", f"Segundos totales de `{met}` en `ll4b`")
        R.add(f"costo.{met}.ratio_timesfm", tfm / t, fm.num(tfm / t, 2), C + "; " + F.rel(F.COSTO_CSV),
              "(timesfm_ll4b_inferencia + timesfm_cribado) / llr total ll4b", f"Cociente total TimesFM / `{met}` en `ll4b`")
        R.add(f"costo.{met}.ratio_tuned", tun / t, fm.num(tun / t, 2), C + "; " + F.rel(F.COSTO_CSV),
              "(tuned_ll4b_seleccion + tuned_ll4b_ajuste) / llr total ll4b", f"Cociente total `tuned` / `{met}` en `ll4b`")
        R.add(f"costo.{met}.ratio_timesfm_r", tfm / t, fm.num(tfm / t, 0), C + "; " + F.rel(F.COSTO_CSV),
              "(timesfm_ll4b_inferencia + timesfm_cribado) / llr total ll4b, 0 decimales", f"Cociente total TimesFM / `{met}` en `ll4b`, entero")
        R.add(f"costo.{met}.ratio_tuned_r", tun / t, fm.num(tun / t, 0), C + "; " + F.rel(F.COSTO_CSV),
              "(tuned_ll4b_seleccion + tuned_ll4b_ajuste) / llr total ll4b, 0 decimales", f"Cociente total `tuned` / `{met}` en `ll4b`, entero")


def construir(d: Datos | None = None) -> Registro:
    d = d or cargar()
    R = Registro()
    _conteos(R, d)
    _metricas(R, d)
    _brechas(R, d)
    _zonas(R, d)
    _cribado(R, d)
    _escalera(R, d)
    _a3(R, d)
    _a4(R, d)
    _costo(R, d)
    _diseno(R, d)
    _r1(R, d)
    _r2(R, d)
    _preentrenamiento(R, d)
    _r3(R, d)
    R.nd("tuned.ll4.referencia_limpia_palacios", F.rel(F.A1_POR_METODO), "-",
         "Cifra limpia de referencia de Palacios para `tuned` en `ll4`",
         "no está en las fuentes numéricas permitidas; solo se informa el RMSE de a1_por_metodo.csv (rmse4.ll4.panel.tuned)")
    return R


# --- Salidas ----------------------------------------------------------------------------
def a_arbol(R: Registro) -> dict:
    arbol: dict = {}
    for clave, fila in R.filas.items():
        partes = clave.split(".")
        nodo = arbol
        for p in partes[:-1]:
            nodo = nodo.setdefault(p, {})
            if not isinstance(nodo, dict):
                raise KeyError(f"conflicto hoja/rama en {clave}")
        if partes[-1] in nodo:
            raise KeyError(f"conflicto hoja/rama en {clave}")
        nodo[partes[-1]] = fila["valor_texto"]
    return arbol


class _Dumper(yaml.SafeDumper):
    """Todos los textos entre comillas dobles, para que ningun valor se lea como numero."""


_Dumper.add_representer(str, lambda dp, v: dp.represent_scalar("tag:yaml.org,2002:str", v, style='"'))


def yml_texto(R: Registro) -> str:
    cab = "# Generado por experiments/paper_nuevo/cifras.py. No editar a mano.\n"
    return cab + yaml.dump(a_arbol(R), Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=10**6, default_flow_style=False)


def csv_texto(R: Registro) -> str:
    import io

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["key", "valor_num", "valor_texto", "fuente_archivo", "fuente_filtro", "nota"])
    for f in R.filas.values():
        num = "" if f["valor_num"] is None else repr(f["valor_num"])
        w.writerow([f["clave"], num, f["valor_texto"], f["fuente_archivo"], f["fuente_filtro"], f["nota"]])
    return buf.getvalue()


def claves_md(R: Registro) -> str:
    out = ["# Claves de cifras del paper nuevo", "",
           "Generado por `experiments/paper_nuevo/cifras.py`; no se edita a mano. En Quarto se usa `{{< var clave >}}`.",
           "Brecha = RMSE(A) − RMSE(B) en °C; negativa favorece a A. `n. d.` indica que la cifra no existe en las fuentes.", "",
           f"Total de claves: {len(R.filas)}.", ""]
    grupos: dict[str, list[dict]] = {}
    for f in R.filas.values():
        grupos.setdefault(f["clave"].split(".")[0], []).append(f)
    for g, filas in grupos.items():
        out += [f"## {g}", "", "| clave | valor | significado |", "|---|---|---|"]
        for f in filas:
            nota = f" ({f['nota']})" if f["nota"] else ""
            val = f["valor_texto"].replace("|", "\\|")
            out.append(f"| `{f['clave']}` | {val} | {f['descripcion'].replace('|', '/')}{nota} |")
        out.append("")
    return "\n".join(out)


def sha256(*textos: str) -> str:
    h = hashlib.sha256()
    for t in textos:
        h.update(t.encode("utf-8"))
    return h.hexdigest()


def registrar_proveniencia(salidas: list[str], variante: str, notas: str, entradas: list[str]) -> None:
    """Sidecar + fila en el registro, solo si el contenido cambio (idempotente)."""
    from tdew_estimation import provenance as prov

    h = hashlib.sha256()
    for s in salidas:
        h.update((F.REPO / s).read_bytes())
    marca = f"sha256={h.hexdigest()[:16]}"
    for row in prov.load_registry():
        if row.get("variant_label") == variante and marca in (row.get("notes") or "") and set(salidas) <= set(row.get("output_files", [])):
            return
    rec = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(), bead_id="tdew-tpu",
        manifest_ref="docs/protocol/timesfm_manifest.yaml", model_family="comparison", model_id="multi",
        variant_label=variante, trained=True, training_period=("1981-01-01", "2012-12-31"), validation_period=None,
        test_period=("2009-01-01", "2016-12-31"), split_id="ll4,ll4b", autoregressive=True, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference", inputs=tuple(sorted(entradas)),
        panel_id="nacional_17027", panel_cell_count=17027, panel_file=F.rel(F.PANEL_NACIONAL),
        output_files=tuple(salidas), seeds=(0,), notes=f"{notas} {marca}")
    prov.record_metric_provenance(rec)


def escribir(salida: Path | None = None) -> Registro:
    R = construir()
    malas = [d for d, ok in R.verificaciones if not ok]
    if malas:
        raise AssertionError("verificaciones fallidas: " + "; ".join(malas))
    yml, csvt, md = yml_texto(R), csv_texto(R), claves_md(R)
    F.CIFRAS_DIR.mkdir(parents=True, exist_ok=True)
    F.VARIABLES_YML.write_text(yml, encoding="utf-8")
    F.CIFRAS_CSV.write_text(csvt, encoding="utf-8")
    F.CLAVES_MD.write_text(md, encoding="utf-8")
    entradas = sorted({a for f in R.filas.values() for a in f["fuente_archivo"].split("; ") if a.startswith("reports/")})
    registrar_proveniencia(
        [F.rel(F.CIFRAS_CSV)], "paper_nuevo_cifras",
        "Cifras del paper nuevo calculadas por experiments/paper_nuevo/cifras.py desde los CSV de resultados; "
        "ver fuente_archivo y fuente_filtro por clave.", entradas)
    log.info("%d claves; %d n. d.", len(R.filas), sum(f["valor_texto"] == fm.ND for f in R.filas.values()))
    return R


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    escribir()
