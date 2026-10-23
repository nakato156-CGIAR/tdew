"""Cifras y tablas del paper nuevo: recomputo independiente desde los CSV fuente y determinismo."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache

import pandas as pd
import pytest
import yaml

from experiments.paper_nuevo import cifras as ci
from experiments.paper_nuevo import formato as fm
from experiments.paper_nuevo import fuentes as F
from experiments.paper_nuevo import tablas as tb


@lru_cache(maxsize=1)
def _R():
    return ci.construir()


def _es(x: float, nd: int = 3) -> str:
    """Formato espanol independiente de formato.py (Decimal, mitad hacia arriba)."""
    d = Decimal(repr(float(x))).copy_abs().quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return str(d).replace(".", ",")


def _min_seg(seg: float) -> str:
    s = int(Decimal(repr(float(seg))).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return f"{s // 60} min {s % 60} s"


def test_rmse_ll4b_panel_timesfm():
    m = pd.read_csv(F.A1_POR_METODO)
    x = m[(m.split == "ll4b") & (m.ambito == "panel") & (m.metodo == "timesfm_anom") & (m.periodo == "total")].rmse.iloc[0]
    assert _R().texto("rmse.ll4b.panel.timesfm") == "1,046" == _es(x)


def test_rmse_todas_las_celdas_totales():
    m = pd.read_csv(F.A1_POR_METODO)
    for r in m[m.periodo == "total"].itertuples(index=False):
        assert _R().texto(f"rmse.{r.split}.{r.ambito}.{ci.alias(r.metodo)}") == _es(r.rmse)


def test_sesgo_tiene_signo_tipografico():
    assert _R().texto("sesgo.ll4.panel.tuned") == "−0,033"
    assert _R().texto("sesgo.ll4.panel.timesfm") == "+0,104"


def test_brecha_y_ic():
    b = pd.read_csv(F.A1_BRECHAS)
    r = b[(b.split == "ll4") & (b.ambito == "panel") & (b.metodo_a == "timesfm_anom") & (b.metodo_b == "tuned")].set_index("esquema")
    R = _R()
    assert R.texto("brecha.ll4.panel.timesfm_vs_tuned.v") == "−" + _es(abs(r.brecha.iloc[0]))
    assert R.texto("brecha.ll4.panel.timesfm_vs_tuned.ma_ic") == f"[−{_es(abs(r.ic_lo['mes_anio']))}; −{_es(abs(r.ic_hi['mes_anio']))}]"
    assert R.texto("brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ambos_excluyen_cero") == "no"


def test_conteos_de_panel():
    R = _R()
    panel = pd.read_csv(F.PANEL_NACIONAL)
    assert R.texto("panel.celdas") == "17.027" and len(panel) == 17027
    assert R.texto("panel.celdas_peru") == "8.272"
    assert R.texto("panel.celdas_fuera") == "8.755"
    assert R.texto("panel.zonas_panel") == str(panel.zone_id.nunique()) == "33"
    assert R.texto("panel.zonas_peru") == "32"
    assert R.texto("bootstrap.replicas") == "2.000"


def test_costo_total_timesfm_ll4b():
    c = pd.read_csv(F.COSTO_CSV)
    inf = c[(c.metodo == "timesfm_anom") & (c.bloque == "ll4b")].segundos_pared.iloc[0]
    cri = c[c.metodo == "timesfm (9 variantes)"].segundos_pared.iloc[0]
    tun = c[(c.metodo == "tuned") & (c.bloque == "ll4b")].segundos_pared.sum()
    assert _min_seg(inf + cri) == "122 min 18 s" == _R().texto("costo.ll4b.timesfm_total.tiempo")
    assert _min_seg(tun) == "58 min 28 s" == _R().texto("costo.ll4b.tuned_total.tiempo")
    assert _R().texto("costo.ll4b.ratio_total") == _es((inf + cri) / tun, 2) == "2,09"
    assert _R().texto("costo.producto.timesfm_inferencia.dias_aprox").startswith("≈5,1")


def test_cribado_seis_de_nueve():
    lb = pd.read_csv(F.LEADERBOARD)
    lb = lb[lb.split == "ll4"]
    tun = lb[lb.method == "tuned"].rmse.iloc[0]
    var = lb[lb.method.str.startswith("timesfm:")]
    assert len(var) == 9 and int((var.rmse < tun).sum()) == 6
    R = _R()
    assert R.texto("cribado.n_variantes") == "9" and R.texto("cribado.n_menor_tuned") == "6"
    assert R.texto("cribado.dif_td_full_znorm") == "1,12 × 10^−8^"


def test_sesgo_mayor_en_tres_de_cuatro():
    m = pd.read_csv(F.A1_POR_METODO)
    m = m[m.periodo == "total"].set_index(["split", "ambito", "metodo"])
    n = sum(abs(m.loc[(s, a, "timesfm_anom")].sesgo) > abs(m.loc[(s, a, "tuned")].sesgo) for s in ("ll4", "ll4b") for a in ("panel", "peru"))
    assert n == 3 == int(_R().num("sesgo_conteo.n_mayor"))


def test_2013_inversion():
    R = _R()
    assert R.texto("brecha_anual.ll4.panel.timesfm_vs_tuned.a2013").startswith("+")
    assert R.texto("inversion.n_casos_vs_tuned") == "1"
    assert R.texto("anual_resumen.ll4.peru.timesfm_vs_tuned.todas_negativas") == "sí"


def test_a4_conteos_sin_era5():
    R = _R()
    assert R.texto("a4.td.pisco_2009_2016.n_dias") == "31.326" and R.texto("a4.td.pisco_2009_2016.n_estaciones") == "13"
    assert R.texto("a4.anom.pisco_2009_2016.n_dias") == "30.751" and R.texto("a4.anom.pisco_2009_2016.n_estaciones") == "12"
    assert not any("era5" in k for k in R.filas)


def test_no_disponibles_son_nd_y_sin_numero():
    nd = [f for f in _R().filas.values() if f["valor_texto"] == fm.ND]
    assert nd and all(f["valor_num"] is None and f["nota"] for f in nd)
    claves = {f["clave"] for f in nd}
    for k in ("a3.ll4b.rmse", "brecha_anual.ic", "brecha_zona.ic", "brecha.ll4b.panel.timesfm_td_vs_llr_rezagos_sel.ic"):
        assert k in claves


def test_verificaciones_internas_y_etiquetas():
    assert all(ok for _, ok in _R().verificaciones)
    assert not any("Ã" in f["valor_texto"] for f in _R().filas.values())


def test_formato():
    assert fm.num(1.04625) == "1,046" and fm.num(0.0055) == "0,006"
    assert fm.num(-0.0004, 3, True) == "−0,0004" and fm.num(0.0, 3) == "0,000" and fm.num(0.054, 3, True) == "+0,054"
    assert fm.ent(17027) == "17.027" and fm.ent(24876447) == "24.876.447" and fm.ent(33) == "33"
    assert fm.dur(4389.8) == "73 min 10 s" and fm.dur(141991) == "39 h 27 min" and fm.dur(438074) == "≈5,1 días"


def test_determinismo_mismos_bytes():
    a, b = ci.construir(), ci.construir()
    assert ci.yml_texto(a) == ci.yml_texto(b)
    assert ci.csv_texto(a) == ci.csv_texto(b)
    assert ci.claves_md(a) == ci.claves_md(b)
    ta, tb_ = tb.construir(a), tb.construir(b)
    assert all(ta[k].md() == tb_[k].md() and ta[k].csv() == tb_[k].csv() for k in tb.TABLE_IDS)


def test_yaml_ida_y_vuelta():
    R = _R()
    arbol = yaml.safe_load(ci.yml_texto(R))

    def hojas(n, pre=""):
        for k, v in n.items():
            yield from hojas(v, f"{pre}{k}.") if isinstance(v, dict) else [(f"{pre}{k}", v)]

    got = dict(hojas(arbol))
    assert got == {k: f["valor_texto"] for k, f in R.filas.items()}


def test_salidas_en_disco_estan_al_dia():
    R = _R()
    assert F.VARIABLES_YML.read_text(encoding="utf-8") == ci.yml_texto(R)
    assert F.CIFRAS_CSV.read_text(encoding="utf-8") == ci.csv_texto(R)
    assert F.CLAVES_MD.read_text(encoding="utf-8") == ci.claves_md(R)
    for tid, t in tb.construir(R).items():
        assert (F.TABLAS_DIR / f"{tid}.md").read_text(encoding="utf-8") == t.md(), tid
        assert (F.TABLAS_DIR / f"{tid}.csv").read_text(encoding="utf-8") == t.csv(), tid


def test_tablas_forma_y_consistencia():
    t = tb.construir(_R())
    assert set(t) == set(tb.TABLE_IDS)
    for tid, x in t.items():
        assert all(len(f) == len(x.columnas) for f in x.filas), tid
        lineas = x.md().strip().splitlines()
        assert len(lineas) == len(x.filas) + 2 and lineas[1].startswith("|:---") or lineas[1].startswith("|---")
    assert len(t["tab3"].filas) == 16 and len(t["tab4"].filas) == 11
    fila = next(f for f in t["tab3"].filas if f[0][1] == "2009–2012" and f[1][1] == "dominio completo" and "TimesFM" in f[2][1])
    assert fila[3][1] == "1,046"
    assert next(f for f in t["tab6"].filas if f[2][1] == "Total incluyendo la selección una vez")[3][1] == "122 min 18 s"


def test_a2_mejora_sin_td_y_fraccion_cerrada():
    m = pd.read_csv(F.A1_POR_METODO)
    m = m[m.periodo == "total"].set_index(["split", "ambito", "metodo"]).rmse
    R = _R()
    for s in ("ll4", "ll4b"):
        for a in ("panel", "peru"):
            mejora = m[(s, a, "tuned")] - m[(s, a, "tuned_sin_td")]
            gap = abs(m[(s, a, "timesfm_anom")] - m[(s, a, "tuned")])
            assert R.texto(f"a2.{s}.{a}.mejora_sin_td") == _es(mejora)
            assert R.texto(f"a2.{s}.{a}.brecha_timesfm_tuned") == _es(gap)
            assert R.texto(f"a2.{s}.{a}.fraccion_cerrada_pct") == _es(100 * mejora / gap, 0)
    # Cifras que cita la narrativa (paper_narrative.md §1 y §3.7).
    assert (R.texto("a2.ll4.panel.mejora_sin_td"), R.texto("a2.ll4.panel.brecha_timesfm_tuned")) == ("0,054", "0,074")
    assert (R.texto("a2.ll4b.panel.mejora_sin_td"), R.texto("a2.ll4b.panel.brecha_timesfm_tuned")) == ("0,014", "0,076")


def test_variantes_longitud_de_contexto():
    from experiments.timesfm.variants import VARIANTS

    R = _R()
    assert R.texto("variantes.tmin_td_short.contexto_anios.ll4") == "2"  # 2011-2012
    assert R.texto("variantes.tmin_anom_med.contexto_anios.ll4") == "11" and R.texto("variantes.tmin_anom_med.contexto_anios.ll4b") == "7"
    assert R.texto("variantes.tmin_anom_full.contexto_anios.ll4") == R.texto("bloques.ll4.anios_contexto") == "32"
    assert R.texto("variantes.tmin_anom_full.contexto_anios.ll4b") == R.texto("bloques.ll4b.anios_contexto") == "28"
    assert R.texto("variantes.n_total") == str(len(VARIANTS))
    for v in VARIANTS:
        assert R.texto(f"variantes.{v.key}.contexto_ini") == str(v.context_start_year)


def test_diseno_desde_codigo():
    from HPC_code_tunning.feature_spec import DEFAULT_CANDIDATE_POOL
    from experiments.llr_simple import llr

    R = _R()
    assert R.texto("diseno.tuned.pool_terminos") == str(len(DEFAULT_CANDIDATE_POOL)) == "11"
    assert R.texto("diseno.tuned.pool_sin_td") == "6"
    assert R.texto("diseno.tuned.rezagos_td") == "1, 2, 3, 7 y 30" and R.texto("diseno.tuned.rezagos_tmin") == "1, 2, 7 y 30"
    assert R.texto("diseno.llr_sel.h_max") == str(max(llr.H_GRID_SEL)) == "180"
    assert R.texto("diseno.llr_sel.combinaciones") == str(len(llr.H_GRID_SEL) * len(llr.TRAIN_START_GRID)) == "40"
    assert R.texto("diseno.llr.h_max") == "60" and R.texto("diseno.llr.h_n") == "7"
    assert R.texto("diseno.llr.validacion_anios") == "4"
    assert R.texto("timesfm.parametros_millones") == "330"
    # La grilla de `h` de `tuned` usada en el articulo no esta en el codigo por defecto: debe ser n. d.
    assert R.texto("diseno.tuned.h_min") == fm.ND and R.texto("diseno.tuned.h_max") == fm.ND


def test_bootstrap_nivel_95():
    R = _R()
    assert R.texto("bootstrap.nivel") == "95"
    assert (R.texto("bootstrap.percentil_inf"), R.texto("bootstrap.percentil_sup")) == ("2,5", "97,5")


def test_sesgo_conteo_casos_se_leen_en_prosa():
    R = _R()
    assert R.texto("sesgo_conteo.casos_mayor") == "2009–2012 en Perú, 2013–2016 en el dominio completo y 2013–2016 en Perú"
    assert R.texto("sesgo_conteo.casos_menor") == "2009–2012 en el dominio completo"


def test_claves_de_diseno_y_signos_nuevas():
    R = _R()
    assert R.texto("variantes.inicios_cribado") == "1981, 2002 y 2011"
    assert R.texto("variantes.n_univariadas") == "2"
    assert R.texto("diseno.llr.n_variantes") == "4"
    assert R.texto("a2.anios_sin_td_peor") == "2009 y 2013"
    assert R.texto("brecha_conteo.llr_ll4_panel.n_esp_excluyen") == "2"
    assert R.texto("brecha_conteo.llr_ll4_panel.n_ma_excluyen") == "0"
    m = pd.read_csv(F.A1_POR_METODO)
    t = m[(m.split == "ll4b") & (m.ambito == "panel") & (m.periodo == "total")].set_index("metodo").rmse
    assert R.texto("puntual.ll4b.panel.timesfm_vs_timesfm_td") == "−" + _es(abs(t["timesfm_anom"] - t["timesfm_td"]))


# --- R1 / R2 (tdew-ddx): claves de robustez, horizonte, DM y descriptivos, recomputadas desde los CSV ---------
def _s(x: float, nd: int = 3, signo: bool = True) -> str:
    t = _es(abs(x), nd)
    return ("−" if x < 0 else "+" if signo else "") + t


def test_robustez_ic_por_esquema_y_conteos():
    b = pd.read_csv(F.R1_BOOT)
    r = b[(b.split == "ll4") & (b.ambito == "panel") & (b.metodo_b == "llr_rezagos_sel")].set_index("esquema")
    R = _R()
    assert R.texto("robustez.ll4.panel.llr_rezagos_sel.ta_ic") == f"[{_s(r.ic_lo['temporal_trim_anio'])}; {_s(r.ic_hi['temporal_trim_anio'])}]"
    assert R.texto("robustez.ll4.panel.llr_rezagos_sel.esa_ic") == f"[{_s(r.ic_lo['espaciotemporal_2g_anio'])}; {_s(r.ic_hi['espaciotemporal_2g_anio'])}]"
    assert R.texto("robustez.ll4.panel.llr_rezagos_sel.v") == _s(r.brecha.iloc[0])
    for esq, p in (("espacial_2g", "esp"), ("espaciotemporal_2g_anio", "esa"), ("temporal_trim_anio", "ta")):
        sub = b[b.esquema == esq]
        n = int(((sub.ic_lo > 0) | (sub.ic_hi < 0)).sum())
        assert len(sub) == 16 and R.texto(f"robustez_conteo.{p}.texto") == f"{n} de 16"
        assert R.texto(f"robustez_conteo.{p}.n_excluyen") == str(n)
    # Frente a `tuned` todo IC excluye cero; el único caso espacial con cero es ll4/panel frente a llr_rezagos_sel.
    assert R.texto("robustez_conteo.esp.ll4.panel.incluyen") == "LLR con rezagos seleccionado"


def test_dm_holm_y_formato_de_p():
    dm = pd.read_csv(F.R1_DM)
    R = _R()
    x = dm[(dm.split == "ll4") & (dm.ambito == "panel") & (dm.metodo_b == "tuned") & (dm.rezago == 7)].iloc[0]
    assert R.texto("dm.ll4.panel.tuned.lag7.p_holm") == _es(x.p_holm) == "0,005"
    assert R.texto("dm.ll4.panel.tuned.lag7.dm") == _s(x.dm, 2)
    y = dm[(dm.split == "ll4b") & (dm.ambito == "peru") & (dm.metodo_b == "tuned") & (dm.rezago == 30)].iloc[0]
    assert y.p_holm < 0.001 and R.texto("dm.ll4b.peru.tuned.lag30.p_holm") == "<\u00a00,001"
    assert R.texto("dm.ll4b.peru.tuned.lag30.p_holm_sci") == fm.sci(y.p_holm, 2)
    for lag in (7, 30):
        sub = dm[dm.rezago == lag]
        assert R.texto(f"dm_conteo.lag{lag}.texto") == f"{int((sub.p_holm < 0.05).sum())} de {len(sub)}"
    assert R.texto("dm.familia") == "16"


def test_horizonte_anios_y_meses():
    h = pd.read_csv(F.R1_HORIZONTE)
    R = _R()
    a1 = h[(h.split == "ll4") & (h.ambito == "panel") & (h.metodo_b == "tuned") & (h.unidad == "anio") & (h.horizonte == 1)].iloc[0]
    assert R.texto("horizonte.ll4.panel.tuned.anio1.v") == _s(a1.brecha) == "+0,055"
    assert R.texto("horizonte.ll4.panel.tuned.anio1.ic") == f"[{_s(a1.ic_lo)}; {_s(a1.ic_hi)}]"
    m = h[(h.split == "ll4b") & (h.ambito == "peru") & (h.metodo_b == "llr_simple_sel") & (h.unidad == "mes")].sort_values("horizonte")
    assert R.texto("horizonte.ll4b.peru.llr_simple_sel.meses_neg") == str(int((m.brecha < 0).sum()))
    assert R.texto("horizonte.ll4b.peru.llr_simple_sel.meses_ic_neg") == str(int((m.ic_hi < 0).sum()))
    assert R.texto("horizonte.ll4b.peru.llr_simple_sel.mes_mayor_ventaja") == str(int(m.loc[m.brecha.idxmin(), "horizonte"]))
    # Solo el primer año de ll4/panel tiene brecha anual positiva, frente a los cuatro rivales.
    for r in ci.RIV:
        assert R.texto(f"horizonte.ll4.panel.{r}.anios_positivos") == "1"
        assert R.texto(f"horizonte.ll4.peru.{r}.anios_positivos") == "ninguno"


def test_descriptivos_r2():
    R = _R()
    sk = pd.read_csv(F.R2_SKILL).set_index(["split", "ambito", "metodo"])
    assert R.texto("skill.ll4.panel.timesfm.razon_varianza") == _es(sk.loc[("ll4", "panel", "timesfm_anom")].razon_varianza)
    assert R.texto("skill.ll4b.peru.tuned.corr") == _es(sk.loc[("ll4b", "peru", "tuned")].corr_anomalia)
    ex = pd.read_csv(F.R2_EXTREMOS).set_index(["split", "ambito", "clase", "metodo"])
    g = ex.loc[("ll4", "panel", "superior_5", "timesfm_anom")].rmse - ex.loc[("ll4", "panel", "superior_5", "tuned")].rmse
    assert R.texto("extremos.ll4.panel.sup5.brecha.tuned") == _s(g)
    assert R.texto("extremos.ll4.panel.sup5.tuned.sesgo") == _s(ex.loc[("ll4", "panel", "superior_5", "tuned")].sesgo)
    ca = pd.read_csv(F.R2_CALIBRACION)
    t = ca[(ca.split == "ll4") & (ca.ambito == "panel") & (ca.periodo == "total")].iloc[0]
    assert R.texto("calib.ll4.panel.total.cobertura") == _es(100 * t.cobertura_80, 1)
    assert R.texto("calib.ll4.panel.total.crps") == _es(t.crps_aprox)
    al = pd.read_csv(F.R2_ALTITUD)
    b = al[(al.split == "ll4") & (al.ambito == "panel") & (al.estrato_tipo == "altitud") & (al.metodo == "tuned")]
    assert R.texto("altitud.ll4.panel.vs_tuned.brecha_max_ventaja") == _s(b.brecha_tfm_menos_metodo.min())
    assert R.texto("altitud.ll4.panel.vs_tuned.banda_max_ventaja") == ci.BANDA_TXT[b.loc[b.brecha_tfm_menos_metodo.idxmin(), "estrato"]]
    zd = pd.read_csv(F.R2_ZONA_DOM)
    z = zd[(zd.split == "ll4") & (zd.ambito == "panel") & (zd.metodo == "llr_rezagos_sel")].iloc[0]
    assert R.texto("zdom.ll4.panel.brecha.llr_rezagos_sel.sin_zona") == _s(z.brecha_sin_zona)
    assert R.texto("zdom.ll4.panel.pct_celdas") == _es(100 * z.frac_celdas, 1)
    en = pd.read_csv(F.R2_ENSO)
    for s in ("ll4", "ll4b"):
        for a in ("panel", "peru"):
            meses = en[(en.split == s) & (en.ambito == a) & (en.metodo == "timesfm_anom")].set_index("estrato").meses
            assert meses.sum() == 48 and R.texto(f"enso.{s}.{a}.la_nina.meses") == str(int(meses["la_nina"]))


def test_preentrenamiento_constantes():
    R = _R()
    notas = F.NOTAS_PRE.read_text(encoding="utf-8")
    assert R.texto("preentrenamiento.reanalisis_anio_ini") == "1989" and R.texto("preentrenamiento.reanalisis_anio_fin") == "2018"
    assert R.texto("preentrenamiento.reanalisis_grilla_grados") == "2,8125" and "2,8125°" in notas
    assert R.texto("preentrenamiento.n_parches") == "45" and R.texto("preentrenamiento.parche_salida") == "64"
    assert R.texto("preentrenamiento.contexto_max") == "15.360" and "15.360 puntos" in notas


def test_r3_ausente_se_trata_como_nd():
    R = _R()
    if not F.R3_COSTO.exists():
        assert R.texto("costo.llr_simple_sel.tiempo") == fm.ND and R.texto("costo.llr_rezagos_sel.tiempo") == fm.ND


@pytest.mark.skipif(not F.R3_COSTO.exists(), reason="r3_costo_llr_sel.csv no existe")
def test_r3_costo_llr_sel_recomputo():
    R = _R()
    c = pd.read_csv(F.R3_COSTO)
    base = pd.read_csv(F.COSTO_CSV)
    g = lambda m, b, pref: float(c[(c.metodo == m) & (c.bloque == b) & c.etapa.str.startswith(pref)].segundos_pared.iloc[0])
    b_ = lambda m, e: float(base[(base.metodo == m) & (base.bloque == "ll4b") & base.etapa.str.startswith(e)].segundos_pared.iloc[0])
    tun = b_("tuned", "seleccion") + b_("tuned", "ajuste")
    tfm = b_("timesfm_anom", "prediccion") + float(base[base.metodo.str.startswith("timesfm (9")].segundos_pared.iloc[0])
    for m in ("llr_simple_sel", "llr_rezagos_sel"):
        t = g(m, "ll4b", "total")
        assert R.texto(f"costo.{m}.tiempo") == _min_seg(t)
        assert R.texto(f"costo.{m}.ratio_tuned") == _es(tun / t, 2)
        assert R.texto(f"costo.{m}.ratio_timesfm") == _es(tfm / t, 2)
        for b in ("ll4b", "ll4"):
            for corta, pref in (("carga", "carga"), ("seleccion", "seleccion"), ("ajuste", "ajuste"), ("total", "total")):
                assert R.num(f"costo.{m}.{b}.{corta}.seg") == g(m, b, pref)
            assert abs(g(m, b, "carga") + g(m, b, "seleccion") + g(m, b, "ajuste") - g(m, b, "total")) < 1.0
            assert R.texto(f"costo.{m}.{b}.total.celdas_por_s") == _es(17027 / g(m, b, "total"), 2)
        assert "14900K" in R.texto(f"costo.{m}.hardware") and R.texto(f"costo.{m}.gpu") == "sin GPU"
        assert R.texto(f"costo.{m}.reproduce_texto").endswith("de 0,0")
    assert R.texto("costo.llr_simple_sel.tiempo") == "1 min 42 s"
    t = tb.construir(R)
    assert len(t["s7"].filas) == len(c) + len(pd.read_csv(F.COSTO_CSV))


def test_tablas_nuevas_forma():
    t = tb.construir(_R())
    assert len(t["tab7_robustez"].filas) == 16 and len(t["s9_skill"].filas) == 20 and len(t["s10_extremos"].filas) == 60
    assert len(t["s11_calibracion"].filas) == 20 and len(t["s12_altitud"].filas) == 20
    assert len(t["s13_enso"].filas) == 12 and len(t["s14_zona_dominante"].filas) == 16
    f = next(x for x in t["tab7_robustez"].filas if x[0][1] == "2013–2016" and x[1][1] == "dominio completo" and "rezagos seleccionado" in x[2][1])
    assert f[5][1] == _R().texto("robustez.ll4.panel.llr_rezagos_sel.esa_ic") and f[7][1] == _R().texto("dm.ll4.panel.llr_rezagos_sel.lag7.p_holm")
