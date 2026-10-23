"""Figuras del paper nuevo (TimesFM `timesfm_anom` frente a `tuned` y controles).

Todos los valores graficados salen de CSV mediante codigo; nada se escribe a mano.
Convencion de signo: brecha = RMSE(A) - RMSE(B), con A = TimesFM. Negativo favorece a TimesFM.

Uso (desde la raiz del repositorio):
    uv run python -m experiments.paper_nuevo.figuras [directorio_salida]

Salida: PNG (300 dpi), PDF y SVG por figura en reports/paper_nuevo/figuras/.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import estilo  # noqa: E402
from .estilo import COLOR, COLOR_AMBITO, COLOR_ZONA, ETIQUETA, FOCO, GRID, INK, MUTED  # noqa: E402

GRID_V = GRID

REPO = Path(__file__).resolve().parents[2]
RESULTADOS = REPO / "reports/paper_nuevo/resultados"
BRECHAS = RESULTADOS / "a1_brechas.csv"
POR_METODO = RESULTADOS / "a1_por_metodo.csv"
POR_ZONA = RESULTADOS / "a1_por_zona.csv"
ESCALERA = RESULTADOS / "a1_escalera_contexto.csv"
A3 = RESULTADOS / "a3_control_tmin_barajada.csv"
PANEL = REPO / "reports/timesfm_benchmark/panels/nacional_17027.csv"
GEOJSON = REPO / "reports/timesfm_benchmark/geo/peru_departamental_simple.geojson"
SALIDA = REPO / "reports/paper_nuevo/figuras"

TIMESFM = "timesfm_anom"
RIVALES = ["tuned", "llr_rezagos_sel"]
SPLITS = ["ll4b", "ll4"]          # ll4b (2009-2012) va primero
AMBITOS = ["panel", "peru"]
ESQUEMAS = ["espacial_2g", "mes_anio"]
ANIOS = [str(a) for a in range(2009, 2017)]


# --------------------------------------------------------------------------- utilidades
def _guardar(fig, nombre: str, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rutas = []
    for ext in ("png", "pdf", "svg"):
        ruta = out_dir / f"{nombre}.{ext}"
        fig.savefig(ruta)
        rutas.append(ruta)
    plt.close(fig)
    return rutas


def _exigir(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def _es(x: float, dec: int = 2) -> str:
    return f"{x:.{dec}f}".replace("-", "−").replace(".", ",")


def _letra(s: str) -> str:
    """Clase principal de la zona: A..E, o el nombre completo (Lago Titicaca, Loma)."""
    return s[0] if s[0] in "ABCDE" and len(s) > 1 and s[1] == " " else s


# Copiado de reports/paper/scripts/geo_overlay.py (`add_peru_outline`, Palacios) sin
# modificar ese archivo. Cambios: lee el GeoJSON departamental simplificado del
# benchmark en lugar de GADM nivel 1 (no hace falta geopandas).
def add_peru_outline(ax, admin1: bool = True, national_lw: float = 0.9,
                     admin1_lw: float = 0.3, colour: str = "0.25",
                     alpha: float = 0.85) -> bool:
    """Dibuja limites departamentales y nacional sobre un eje lon/lat, sin tocar sus limites."""
    from shapely.geometry import shape
    from shapely.ops import unary_union
    if not GEOJSON.exists():
        return False
    geo = json.loads(GEOJSON.read_text())
    depts = [shape(f["geometry"]) for f in geo["features"]]
    national = unary_union(depts).boundary
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    if admin1:
        for geom in depts:
            for part in (geom.geoms if hasattr(geom, "geoms") else [geom]):
                x, y = part.exterior.xy
                ax.plot(x, y, lw=admin1_lw, color=colour, alpha=alpha * 0.55,
                        zorder=5, solid_capstyle="round")
    for part in (national.geoms if hasattr(national, "geoms") else [national]):
        x, y = part.xy
        ax.plot(x, y, lw=national_lw, color=colour, alpha=alpha, zorder=6,
                solid_capstyle="round")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return True


# --------------------------------------------------------------------------- carga
def _cargar_brechas() -> pd.DataFrame:
    d = pd.read_csv(BRECHAS)
    d = d[(d.metodo_a == TIMESFM) & d.metodo_b.isin(RIVALES)]
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIVALES:
                for e in ESQUEMAS:
                    n = len(d[(d.split == s) & (d.ambito == a) & (d.metodo_b == r) & (d.esquema == e)])
                    _exigir(n == 1, f"a1_brechas: falta o se duplica {s}/{a}/{r}/{e} (n={n})")
    return d


def _cargar_por_metodo() -> pd.DataFrame:
    m = pd.read_csv(POR_METODO)
    for met in (TIMESFM, *RIVALES, "clim"):
        _exigir(met in set(m.metodo), f"a1_por_metodo: falta el metodo {met}")
    _exigir(set(SPLITS) <= set(m.split) and set(AMBITOS) <= set(m.ambito), "a1_por_metodo: split/ambito")
    return m


# --------------------------------------------------------------------------- Fig. 1
GRIS_PERU = "#8f8f8f"      # celdas dentro de Perú (resto de zonas)
GRIS_FUERA = "#d6d6d6"     # celdas fuera de Perú (resto de zonas)


def _depto_lineas(ax, color: str, lw: float) -> None:
    """Limites departamentales (lineas finas) y contorno nacional (linea oscura), sin tocar los limites del eje."""
    from shapely.geometry import shape
    from shapely.ops import unary_union
    geo = json.loads(GEOJSON.read_text())
    depts = [shape(f["geometry"]) for f in geo["features"]]
    for geom in depts:
        for part in (geom.geoms if hasattr(geom, "geoms") else [geom]):
            x, y = part.exterior.xy
            ax.plot(x, y, lw=lw, color=color, zorder=4, solid_capstyle="round")
    nac = unary_union(depts).boundary
    for part in (nac.geoms if hasattr(nac, "geoms") else [nac]):
        x, y = part.xy
        ax.plot(x, y, lw=0.8, color=INK, zorder=6, solid_capstyle="round")


def fig1_panel(out_dir: Path) -> list[Path]:
    """Mensaje unico: Perú es solo la mitad del dominio de evaluacion y la otra mitad es sobre todo una zona.

    Mapa en gris (Perú oscuro, fuera claro) con la zona mas numerosa resaltada; barras de longitud sobre
    base comun con el reparto de celdas. Todo numero anotado se calcula aqui.
    """
    from experiments.timesfm.artifact_data import N_LON, LAT_MAX, LON_MIN, STEP, peru_mask
    from experiments.timesfm.paths import RES

    p = pd.read_csv(PANEL)
    _exigir(len(p) == 17027 and p.ID.is_unique, "panel: se esperaban 17027 IDs unicos")
    mascara = peru_mask(REPO / "reports/timesfm_benchmark")
    ids = p.ID.to_numpy()
    lat = LAT_MAX - (ids // N_LON) * STEP
    lon = LON_MIN + (ids % N_LON) * STEP
    dentro = mascara[ids]
    n_in, n_out = int(dentro.sum()), int((~dentro).sum())
    _exigir(n_in == 8272 and n_out == 8755, f"panel: Perú/fuera = {n_in}/{n_out}, se esperaba 8272/8755")

    zt = pd.read_parquet(RES / "zone_table.parquet", columns=["ID", "zone_label"]).set_index("ID")
    zona = zt.zone_label.reindex(p.ID).to_numpy()
    _exigir(not pd.isna(zona).any(), "panel: celdas sin zona en zone_table")
    cuenta = pd.Series(zona).value_counts()
    foco = cuenta.index[0]                      # zona con mas celdas del dominio
    es_foco = zona == foco
    n_foco = int(es_foco.sum())
    foco_in, foco_out = int((es_foco & dentro).sum()), int((es_foco & ~dentro).sum())
    pct_foco_fuera = 100 * foco_out / n_out
    nombre = foco.replace("'", "′")
    c_foco = COLOR_ZONA["A"]                     # violeta: fuera de la paleta de metodos

    estilo.aplicar()
    lat_med = float(np.mean(lat))
    xlim = (LON_MIN - 0.2, LON_MIN + N_LON * STEP + 0.2)
    ylim = (LAT_MAX - 1982 * STEP - 0.2, LAT_MAX + 0.2)
    asp = 1 / np.cos(np.radians(lat_med))        # proporcion cartografica: 1 grado de lon mide cos(lat) de uno de lat
    alto_map = 10.4
    ancho_map = alto_map * (xlim[1] - xlim[0]) / ((ylim[1] - ylim[0]) * asp)
    fig = plt.figure(figsize=(estilo.ANCHO_COMPLETO, alto_map * estilo.CM))
    W = estilo.ANCHO_COMPLETO / estilo.CM
    m = fig.add_axes([0.0, 0.0, ancho_map / W, 1.0])
    s = 2.4
    for sel, col, z in ((~dentro & ~es_foco, GRIS_FUERA, 2), (dentro & ~es_foco, GRIS_PERU, 2), (es_foco, c_foco, 3)):
        m.scatter(lon[sel], lat[sel], s=s, c=col, lw=0, rasterized=True, zorder=z)
    m.set_xlim(*xlim); m.set_ylim(*ylim)
    m.set_aspect(asp)
    _depto_lineas(m, "white", 0.35)
    m.set_xlim(*xlim); m.set_ylim(*ylim)
    m.axis("off")
    # Rotulos directos sobre el oceano (esquina inferior izquierda, sin celdas).
    x0, y0 = xlim[0] + 0.3, ylim[0] + 3.4
    m.text(x0, y0 + 1.1, "Perú", color=INK, fontsize=9, fontweight="bold", va="bottom")
    m.text(x0, y0, f"Zona {nombre}", color=c_foco, fontsize=8, fontweight="bold", va="top")
    # Escala de 500 km (1 grado de latitud = 111,2 km), abajo a la derecha del oceano.
    grados = 500 / (111.195 * np.cos(np.radians(lat_med)))
    xs, ys = xlim[0] + 0.3, ylim[0] + 0.6
    m.plot([xs, xs + grados], [ys, ys], color=INK, lw=1.0, solid_capstyle="butt", zorder=7)
    m.text(xs + grados / 2, ys + 0.25, "500 km", ha="center", va="bottom", fontsize=6.8, color=MUTED)

    # Barras: celdas por ambito; la zona focal parte de la base comun (comparable en longitud).
    x_lab = ancho_map + 2.7                      # cm: espacio para los rotulos de fila
    b = fig.add_axes([x_lab / W, 0.20, (W - x_lab - 0.1) / W, 0.40])
    filas = [("Perú", n_in, foco_in, GRIS_PERU, "white"), ("Fuera de Perú", n_out, foco_out, GRIS_FUERA, INK)]
    for k, (lab, tot, nf, gc, tc) in enumerate(filas):
        y = 1 - k
        b.barh(y, nf, height=0.52, color=c_foco, lw=0, zorder=3)
        b.barh(y, tot - nf, left=nf, height=0.52, color=gc, lw=0, zorder=3)
        b.text(-300, y, lab, ha="right", va="center", fontsize=8.5, fontweight="bold", color=INK)
        b.text(tot + 200, y, _es_miles(tot), ha="left", va="center", fontsize=8.5, color=INK)
        b.text(nf / 2, y, _es_miles(nf), ha="center", va="center", fontsize=7.6, color="white", fontweight="bold", zorder=4)
        b.text(nf + (tot - nf) / 2, y, "otras zonas", ha="center", va="center", fontsize=7.2, color=tc, zorder=4)
    b.text(foco_in / 2, 1.38, f"Zona {nombre}", ha="center", va="bottom", fontsize=7.4, color=c_foco, fontweight="bold")
    b.set_xlim(0, 10800); b.set_ylim(-0.5, 1.5)
    b.set_yticks([]); b.set_xticks([0, 4000, 8000])
    b.set_xticklabels(["0", "4.000", "8.000"])
    estilo.cuadricula(b, "x")
    for sp in ("left", "bottom"):
        b.spines[sp].set_visible(False)
    b.tick_params(axis="x", length=0)
    b.set_xlabel("Celdas del dominio de evaluación", fontsize=7.6, color=MUTED, loc="left")
    # Titular de lectura: el porcentaje se calcula, no se escribe.
    fig.text((ancho_map + 0.4) / W, 0.94,
             f"{_es_miles(n_out)} de {_es_miles(n_in + n_out)} celdas\nestán fuera de Perú;\n"
             f"{_es(pct_foco_fuera, 0)} % de ellas son de la\nzona {nombre}.",
             ha="left", va="top", fontsize=8.8, fontweight="bold", color=INK, linespacing=1.3)
    return _guardar(fig, "fig1_panel", out_dir)


def _es_miles(n: int) -> str:
    return f"{n:,}".replace(",", ".")


# --------------------------------------------------------------------------- Fig. 2
def fig2_brechas(out_dir: Path) -> list[Path]:
    d = _cargar_brechas()
    estilo.aplicar()
    fig, axs = plt.subplots(2, 2, figsize=(estilo.ANCHO_COMPLETO, 9.0 * estilo.CM), sharex=True, sharey=True)
    off = {"espacial_2g": -0.17, "mes_anio": 0.17}
    base = {"tuned": 1.0, "llr_rezagos_sel": 0.0}   # tuned arriba
    for i, sp in enumerate(SPLITS):
        for j, am in enumerate(AMBITOS):
            ax = axs[i, j]
            estilo.cuadricula(ax, "x")
            ax.axvline(0, color=INK, lw=0.8, zorder=2)
            for r in RIVALES:
                for e in ESQUEMAS:
                    f = d[(d.split == sp) & (d.ambito == am) & (d.metodo_b == r) & (d.esquema == e)].iloc[0]
                    y = base[r] + off[e]
                    hueco = e == "mes_anio"
                    ax.plot([f.ic_lo, f.ic_hi], [y, y], color=COLOR[r], lw=2.0 if not hueco else 1.2,
                            solid_capstyle="butt", zorder=3)
                    ax.plot([f.brecha], [y], "o", ms=3.8, mfc="white" if hueco else COLOR[r],
                            mec=COLOR[r], mew=1.2, zorder=4)
                    # valor de la brecha sobre el punto, solo para el esquema espacial
                    if not hueco:
                        # brechas casi nulas: el rotulo va a la derecha del punto para no cruzar la linea del cero
                        cerca0 = abs(f.brecha) < 0.012
                        ax.text(f.brecha + (0.004 if cerca0 else 0), y - 0.2, _es(f.brecha, 3),
                                ha="left" if cerca0 else "center", va="top",
                                fontsize=6.8, color=INK,
                                bbox=None if cerca0 else dict(fc="white", ec="none", pad=0.6), zorder=6)
            ax.set_ylim(-0.65, 1.55)
            ax.set_yticks([base[r] for r in RIVALES])
            ax.set_yticklabels(["tuned" if r == "tuned" else "LLR con\nrezagos (sel.)" for r in RIVALES])
            if i == 0:
                ax.set_title(estilo.ETIQUETA_AMBITO[am], fontsize=8, fontweight="bold")
            if j == 0:
                ax.text(-0.42, 0.5, f"Bloque {estilo.ETIQUETA_SPLIT[sp]}", transform=ax.transAxes,
                        rotation=90, va="center", ha="center", fontsize=8, fontweight="bold")
            ax.spines["left"].set_visible(False)
            ax.tick_params(axis="y", length=0)
    axs[0, 0].set_xlim(-0.15, 0.03)
    for ax in axs[1]:
        ax.set_xlabel(estilo.XLABEL_BRECHA)
    for ax in axs.flat:
        estilo.coma(ax, "x")
    # leyenda directa de los dos esquemas de IC, en el primer panel
    fig.tight_layout(h_pad=0.8, w_pad=0.8)
    h1, = axs[0, 0].plot([], [], color=MUTED, lw=2.0, marker="o", mfc=MUTED)
    h2, = axs[0, 0].plot([], [], color=MUTED, lw=1.2, marker="o", mfc="white")
    fig.legend([h1, h2], ["IC 95 %, bloques espaciales (2 grados)", "IC 95 %, bloques mes-año"],
               loc="lower center", ncol=2, bbox_to_anchor=(0.55, -0.045), fontsize=7.2, handlelength=1.8)
    return _guardar(fig, "fig2_brechas", out_dir)


# --------------------------------------------------------------------------- Fig. 3
def _brecha_anual(m: pd.DataFrame, ambito: str, rival: str) -> pd.DataFrame:
    filas = []
    for anio in ANIOS:
        sp = "ll4b" if int(anio) <= 2012 else "ll4"
        x = m[(m.split == sp) & (m.ambito == ambito) & (m.periodo == anio)].set_index("metodo").rmse
        _exigir(TIMESFM in x.index and rival in x.index, f"a1_por_metodo: falta {sp}/{ambito}/{anio}")
        filas.append((int(anio), float(x[TIMESFM] - x[rival])))
    return pd.DataFrame(filas, columns=["anio", "brecha"])


def fig3_anual(out_dir: Path) -> list[Path]:
    m = _cargar_por_metodo()
    estilo.aplicar()
    fig, axs = plt.subplots(1, 2, figsize=(estilo.ANCHO_COMPLETO, 6.6 * estilo.CM), sharey=True)
    etiqueta = {"tuned": "vs. tuned", "llr_rezagos_sel": "vs. LLR (sel.)"}
    datos = {(am, r): _brecha_anual(m, am, r) for am in AMBITOS for r in RIVALES}
    todos = np.concatenate([g.brecha.to_numpy() for g in datos.values()])
    for ax, am in zip(axs, AMBITOS):
        estilo.cuadricula(ax, "y")
        ax.axhline(0, color=INK, lw=0.8, zorder=2)
        ax.axvline(2012.5, color=MUTED, lw=0.8, ls=(0, (3, 3)), zorder=1)
        for r in RIVALES:
            g = datos[(am, r)]
            # Un segmento por bloque: 2012 -> 2013 cambia de selecciones y de contexto, no se une con linea.
            for blq in (g.anio <= 2012, g.anio >= 2013):
                ax.plot(g.anio[blq], g.brecha[blq], color=COLOR[r], marker="o", ms=3.6, mec="white", mew=0.6, zorder=3)
            ultimo = g.iloc[-1]
            ax.annotate(etiqueta[r], (ultimo.anio, ultimo.brecha), xytext=(5, 0), textcoords="offset points",
                        va="center", fontsize=7.2, color=COLOR[r], fontweight="bold", annotation_clip=False)
        ax.set_xticks(range(2009, 2017))
        ax.set_xlim(2008.6, 2018.3)
        ax.spines["bottom"].set_bounds(2008.6, 2016.4)
        ax.set_title(estilo.ETIQUETA_AMBITO[am], fontsize=8, fontweight="bold")
        ax.set_xlabel("Año")
    axs[0].set_ylim(todos.min() - 0.02, todos.max() + 0.045)
    for ax in axs:
        ax.text(2010.5, 1.0, "bloque 2009–2012", transform=ax.get_xaxis_transform(), ha="center",
                va="top", fontsize=7, color=MUTED)
        ax.text(2014.5, 1.0, "bloque 2013–2016", transform=ax.get_xaxis_transform(), ha="center",
                va="top", fontsize=7, color=MUTED)
        ax.text(2008.8, todos.max() + 0.02, "↑ TimesFM peor", fontsize=6.8, color=MUTED, va="center")
        ax.text(2008.8, todos.min() - 0.01, "↓ TimesFM mejor", fontsize=6.8, color=MUTED, va="center")
    axs[0].set_ylabel("Brecha de RMSE: TimesFM − rival (°C)\n(negativo = favorece a TimesFM)")
    estilo.coma(axs[0], "y")
    fig.tight_layout(w_pad=1.0)
    return _guardar(fig, "fig3_anual", out_dir)


# --------------------------------------------------------------------------- Fig. 4
def fig4_zonas(out_dir: Path) -> list[Path]:
    z = pd.read_csv(POR_ZONA)
    z = z[z.ambito == "panel"]
    for met in (TIMESFM, *RIVALES):
        _exigir(met in set(z.metodo), f"a1_por_zona: falta {met}")
    r = z.pivot_table(index=["split", "zone_id", "zone_label", "celdas"], columns="metodo", values="rmse").reset_index()
    for rv in RIVALES:
        r[f"b_{rv}"] = r[TIMESFM] - r[rv]
    _exigir(r.groupby("split").zone_id.nunique().eq(33).all(), "a1_por_zona: se esperaban 33 zonas por bloque")
    ref = r[r.split == "ll4"].sort_values("b_tuned", ascending=False)   # arriba: brecha menos negativa
    orden = list(ref.zone_id)
    y = {zid: k for k, zid in enumerate(orden)}
    celdas = ref.set_index("zone_id").celdas
    etiqueta = ref.set_index("zone_id").zone_label

    def _lab(t: str) -> str:
        return t.replace("'", "′").replace(" , ", ", ").replace(" . ", ".")

    estilo.aplicar()
    fig, axs = plt.subplots(1, 2, figsize=(estilo.ANCHO_COMPLETO, 14.2 * estilo.CM), sharey=True, sharex=True)
    nmax = celdas.max()

    def tam(n):
        return 7 + 40 * np.sqrt(n / nmax)

    for ax, sp in zip(axs, SPLITS):
        estilo.cuadricula(ax, "x")
        ax.axvline(0, color=INK, lw=0.8, zorder=2)
        s_ = r[r.split == sp]
        # Cada zona: un hilo gris entre sus dos rivales; puntos grandes al fondo y chicos encima.
        ax.hlines([y[i] for i in s_.zone_id], s_[["b_tuned", "b_llr_rezagos_sel"]].min(axis=1),
                  s_[["b_tuned", "b_llr_rezagos_sel"]].max(axis=1), color="#bdbdbd", lw=0.7, zorder=1)
        pts = [(row.celdas, y[row.zone_id], getattr(row, f"b_{rv}"), rv) for row in s_.itertuples() for rv in RIVALES]
        for k, (n, yy, xx, rv) in enumerate(sorted(pts, key=lambda p: -p[0])):
            ax.scatter([xx], [yy], s=tam(n), color=COLOR[rv], lw=0.4, edgecolor="white", zorder=3 + k * 1e-3)
        ax.set_title(f"Bloque {estilo.ETIQUETA_SPLIT[sp]}", fontsize=8, fontweight="bold")
        ax.set_xlabel("Brecha de RMSE: TimesFM − rival (°C)\n(negativo = favorece a TimesFM)")
        ax.set_ylim(len(orden) - 0.4, -0.7)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    estilo.coma(axs[0], "x")
    estilo.coma(axs[1], "x")
    axs[0].set_yticks(range(len(orden)))
    axs[0].set_yticklabels([f"{_lab(etiqueta[i])}  ({int(celdas[i]):,})".replace(",", ".") for i in orden], fontsize=6.6)
    axs[0].text(-0.01, 1.0, "zona SENAMHI (n.º de celdas)", transform=axs[0].transAxes, ha="right",
                va="bottom", fontsize=6.8, color=MUTED)
    from matplotlib.lines import Line2D
    hm = [Line2D([], [], marker="o", ls="", color=COLOR[rv], mec="white", ms=5.5, label=estilo.ETIQUETA_CORTA[rv]) for rv in RIVALES]
    hs = [Line2D([], [], marker="o", ls="", color="#9a9a9a", mec="white", ms=np.sqrt(tam(n)), label=f"{n:,}".replace(",", "."))
          for n in (10, 100, 1000)]
    fig.tight_layout(w_pad=0.6, rect=(0, 0.075, 1, 1))
    fig.legend(hm, [h.get_label() for h in hm], loc="lower left", bbox_to_anchor=(0.0, 0.035), ncol=2, fontsize=7,
               handletextpad=0.1, columnspacing=1.2, title="Rival", title_fontsize=7, alignment="left", frameon=False)
    fig.legend(hs, [h.get_label() for h in hs], loc="lower center", bbox_to_anchor=(0.62, 0.035), ncol=3, fontsize=7,
               handletextpad=0.1, columnspacing=1.2, title="Celdas de la zona (tamaño del punto)", title_fontsize=7,
               alignment="left", frameon=False)
    fig.text(0.0, 0.0, "Código de zona (clasificación climática SENAMHI): letra = índice de humedad; paréntesis = régimen "
             "estacional de lluvias; A′–D′ = eficiencia térmica.\nZonas ordenadas en ambos paneles por la brecha frente a "
             "tuned en 2013–2016; el hilo gris une los dos rivales de cada zona.",
             fontsize=6.4, color=MUTED, ha="left", va="bottom")
    return _guardar(fig, "fig4_zonas", out_dir)


# --------------------------------------------------------------------------- suplemento
def sfig_escalera(out_dir: Path) -> list[Path]:
    e = pd.read_csv(ESCALERA)
    e = e[e.periodo == "total"]
    # LLR con rezagos y LLR simple (rezagos fijos, sin seleccion) usan colores propios: el ocre pleno
    # queda reservado a `llr_rezagos_sel`, que es otro metodo.
    mets = {"timesfm": ("TimesFM", FOCO), "llr_rezagos": ("LLR con rezagos (no sel.)", COLOR["llr_rezagos"]),
            "llr_simple": ("LLR simple", COLOR["llr_simple"])}
    for k in mets:
        _exigir(k in set(e.metodo), f"escalera: falta {k}")
    estilo.aplicar()
    fig, axs = plt.subplots(1, 2, figsize=(estilo.ANCHO_COMPLETO, 6.0 * estilo.CM), sharey=True)
    for ax, sp in zip(axs, SPLITS):
        estilo.cuadricula(ax, "y")
        for k, (lab, c) in mets.items():
            g = e[(e.split == sp) & (e.metodo == k)].sort_values("inicio")
            _exigir(len(g) == 5, f"escalera: {sp}/{k} sin 5 inicios")
            ax.plot(g.inicio, g.rmse, marker="o", ms=3.8, color=c, ls="-" if k != "llr_simple" else "--", mec="white", mew=0.5)
            if sp == SPLITS[-1]:
                ax.annotate(lab, (g.inicio.iloc[-1], g.rmse.iloc[-1]), xytext=(5, 0),
                            textcoords="offset points", va="center", fontsize=7.2, color=c, fontweight="bold")
        t = e[(e.split == sp) & (e.metodo == "tuned")].rmse.iloc[0]
        ax.axhline(t, color=COLOR["tuned"], lw=1.0, ls=":")
        ax.text(1981, t + 0.003, "tuned (referencia)", fontsize=7, color=COLOR["tuned"], va="bottom")
        ax.set_xticks([1981, 1986, 1991, 1996, 2002])
        ax.set_xlim(1980, 2002 + (7 if sp == SPLITS[-1] else 1))
        ax.set_title(f"Bloque {estilo.ETIQUETA_SPLIT[sp]} (1.092 celdas)", fontsize=8, fontweight="bold")
        ax.set_xlabel("Año de inicio del historial")
    axs[0].set_ylabel("RMSE total (°C)")
    estilo.coma(axs[0], "y")
    fig.tight_layout(w_pad=1.0)
    return _guardar(fig, "sfig_escalera_contexto", out_dir)


def sfig_a3(out_dir: Path) -> list[Path]:
    a = pd.read_csv(A3)
    filas = [("pred_clim", "Climatología", COLOR["clim"]),
             ("pred_tuned", "tuned", COLOR["tuned"]),
             ("real_td", "TimesFM, Td\n(Tmin real)", FOCO),
             ("real_anom", "TimesFM, anomalía\n(Tmin real)", FOCO)]
    barajadas = a[a.tmin == "barajada"].copy()
    _exigir(len(barajadas) == 5 and set(filas_k for filas_k, *_ in filas) <= set(a.corrida), "a3: corridas inesperadas")
    estilo.aplicar()
    fig, ax = plt.subplots(figsize=(estilo.ANCHO_COMPLETO, 7.4 * estilo.CM))
    estilo.cuadricula(ax, "x")
    ref_clim = float(a[a.corrida == "pred_clim"].rmse.iloc[0])
    y = 0
    rot, pos = [], []
    for corrida, lab, c in filas:
        v = float(a[a.corrida == corrida].rmse.iloc[0])
        ax.plot([v], [y], "o", color=c, ms=5.5, zorder=3)
        ax.text(v + 0.012, y, _es(v, 3), va="center", fontsize=7)
        rot.append(lab); pos.append(y); y += 1
    y += 0.4
    nombres = {("cell", "anom"): "Tmin barajada entre celdas\n(TimesFM, anomalía)",
               ("year", "td"): "Tmin barajada entre años\n(TimesFM, Td)",
               ("year", "anom"): "Tmin barajada entre años\n(TimesFM, anomalía; 3 semillas)"}
    grupos = [("cell", "anom"), ("year", "td"), ("year", "anom")]
    for (tipo, var) in grupos:
        g = barajadas[(barajadas.variante == var) & barajadas.corrida.str.contains(f"_{tipo}_")]
        _exigir(len(g) >= 1, f"a3: sin corridas {tipo}/{var}")
        # desplazamiento vertical minimo para que las semillas de valor casi igual no se tapen
        dy = np.linspace(-0.13, 0.13, len(g)) if len(g) > 1 else np.zeros(1)
        ax.scatter(g.rmse.sort_values(), y + dy, edgecolor=FOCO, facecolor="white", lw=1.2, s=26, zorder=3)
        izq = abs(g.rmse.max() - ref_clim) < 0.03
        ax.text(g.rmse.min() - 0.012 if izq else g.rmse.max() + 0.012, y,
                ", ".join(_es(v, 3) for v in sorted(g.rmse)), va="center", fontsize=7,
                ha="right" if izq else "left")
        rot.append(nombres[(tipo, var)]); pos.append(y); y += 1
    ax.set_yticks(pos); ax.set_yticklabels(rot, fontsize=7)
    ax.set_ylim(y - 0.4, -0.7)
    ax.set_xlim(0.75, 1.75)
    estilo.coma(ax, "x", 1)
    ax.set_xlabel("RMSE total (°C; el eje empieza en 0,75), 1.092 celdas, 1.595.412 pares celda-día")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.axvline(float(a[a.corrida == "pred_clim"].rmse.iloc[0]), color=COLOR["clim"], lw=0.8, ls=":")
    from matplotlib.lines import Line2D
    hl = [Line2D([], [], marker="o", ls="", mfc=FOCO, mec=FOCO, ms=5, label="Corrida de referencia (Tmin del bloque)"),
          Line2D([], [], marker="o", ls="", mfc="white", mec=FOCO, mew=1.2, ms=5, label="Tmin barajada (un círculo por semilla)")]
    ax.legend(handles=hl, loc="center right", bbox_to_anchor=(1.0, 0.42), fontsize=7, handletextpad=0.2)
    fig.tight_layout()
    return _guardar(fig, "sfig_a3_tmin_barajada", out_dir)


# --------------------------------------------------------------------------- Fig. 5
HORIZONTE = RESULTADOS / "r1_brecha_horizonte.csv"
RIVALES_H = ["tuned", "tuned_sin_td", "llr_rezagos_sel", "llr_simple_sel"]
# Trazo discontinuo para las variantes sin rezagos de Td / simples: se separan de `tuned` y `llr_rezagos_sel` aunque el color se parezca.
ESTILO_H = {"tuned": "-", "tuned_sin_td": (0, (4, 2)), "llr_rezagos_sel": "-", "llr_simple_sel": (0, (4, 2))}


def _cargar_horizonte() -> pd.DataFrame:
    d = pd.read_csv(HORIZONTE)
    d = d[(d.unidad == "mes") & (d.metodo_a == TIMESFM) & d.metodo_b.isin(RIVALES_H)]
    for s in SPLITS:
        for a in AMBITOS:
            for r in RIVALES_H:
                h = d[(d.split == s) & (d.ambito == a) & (d.metodo_b == r)].horizonte.tolist()
                _exigir(sorted(h) == list(range(1, 49)), f"r1_brecha_horizonte: meses 1..48 incompletos en {s}/{a}/{r}")
    return d


def fig5_horizonte(out_dir: Path) -> list[Path]:
    d = _cargar_horizonte()
    estilo.aplicar()
    fig, axs = plt.subplots(2, 2, figsize=(estilo.ANCHO_COMPLETO, 10.2 * estilo.CM), sharex=True, sharey=True)
    lo, hi = d.ic_lo.min(), d.ic_hi.max()
    for i, s in enumerate(SPLITS):
        for j, a in enumerate(AMBITOS):
            ax = axs[i, j]
            estilo.cuadricula(ax, "y")
            for x in (12.5, 24.5, 36.5):
                ax.axvline(x, color=GRID_V, lw=0.6, zorder=1)
            ax.axhline(0, color=INK, lw=0.8, zorder=2)
            for r in RIVALES_H:
                g = d[(d.split == s) & (d.ambito == a) & (d.metodo_b == r)].sort_values("horizonte")
                ax.fill_between(g.horizonte, g.ic_lo, g.ic_hi, color=COLOR[r], alpha=0.10, lw=0, zorder=2)
                ax.plot(g.horizonte, g.brecha, color=COLOR[r], ls=ESTILO_H[r], lw=1.15, zorder=3)
            ax.set_xlim(1, 48)
            ax.set_xticks([1, 6, 12, 18, 24, 30, 36, 42, 48])
            ax.set_title(f"{estilo.ETIQUETA_SPLIT[s]}, {estilo.ETIQUETA_AMBITO[a]}", fontsize=7.6, fontweight="bold", pad=13)
            for k in range(4):
                ax.text(6.5 + 12 * k, 1.0, f"año {k + 1}", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=6.4, color=MUTED)
            if i == 1:
                ax.set_xlabel("Mes desde el inicio del bloque")
            if j == 0:
                estilo.coma(ax, "y")
    fig.supylabel("Brecha de RMSE: TimesFM − rival (°C)", fontsize=8, x=0.005)
    pad = 0.01
    axs[0, 0].set_ylim(lo - pad, hi + pad)
    for ax in axs.ravel():
        ax.text(0.99, 0.02, "↓ TimesFM mejor", transform=ax.transAxes, ha="right", va="bottom", fontsize=6.6, color=MUTED)
        ax.text(0.99, 0.98, "↑ TimesFM peor", transform=ax.transAxes, ha="right", va="top", fontsize=6.6, color=MUTED)
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color=COLOR[r], ls=ESTILO_H[r], lw=1.4, label=estilo.ETIQUETA[r]) for r in RIVALES_H]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.01), fontsize=7.4, handlelength=2.6)
    fig.tight_layout(rect=(0, 0.05, 1, 1), h_pad=1.2, w_pad=1.0)
    return _guardar(fig, "fig5_horizonte", out_dir)


# --------------------------------------------------------------------------- Fig. 6
BOOT = RESULTADOS / "r1_bootstrap_espaciotemporal.csv"
# Tres esquemas de bootstrap, de arriba abajo en cada rival: grosor decreciente.
ESQ_ROB = [("espacial_2g", "Bloques espaciales de 2°", 2.6), ("espaciotemporal_2g_anio", "Bloques 2° × año", 1.7),
           ("temporal_trim_anio", "Bloques trimestre-año", 0.9)]


def _cargar_robustez() -> pd.DataFrame:
    b = pd.read_csv(BOOT)
    b = b[(b.metodo_a == TIMESFM) & b.metodo_b.isin(RIVALES_H)]
    a1 = pd.read_csv(BRECHAS).query("esquema == 'espacial_2g' and metodo_a == @TIMESFM").set_index(["split", "ambito", "metodo_b"]).brecha
    for sp in SPLITS:
        for am in AMBITOS:
            for r in RIVALES_H:
                for e, _, _ in ESQ_ROB:
                    n = len(b[(b.split == sp) & (b.ambito == am) & (b.metodo_b == r) & (b.esquema == e)])
                    _exigir(n == 1, f"r1_bootstrap: falta o se duplica {sp}/{am}/{r}/{e} (n={n})")
                x = b[(b.split == sp) & (b.ambito == am) & (b.metodo_b == r)].brecha
                _exigir(x.max() - x.min() < 1e-9, f"r1_bootstrap: brecha puntual distinta entre esquemas en {sp}/{am}/{r}")
                if (sp, am, r) in a1.index:   # a1_brechas solo trae tuned y llr_rezagos_sel (control cruzado)
                    _exigir(abs(x.iloc[0] - a1[(sp, am, r)]) < 1e-4, f"brecha puntual r1 != a1_brechas en {sp}/{am}/{r}")
    return b


def fig6_robustez(out_dir: Path) -> list[Path]:
    from matplotlib.lines import Line2D
    b = _cargar_robustez()
    estilo.aplicar()
    fig, axs = plt.subplots(2, 2, figsize=(estilo.ANCHO_COMPLETO, 11.0 * estilo.CM), sharex=True, sharey=True)
    off = {"espacial_2g": 0.24, "espaciotemporal_2g_anio": 0.0, "temporal_trim_anio": -0.24}
    n_r = len(RIVALES_H)
    lo, hi = b.ic_lo.min(), b.ic_hi.max()
    for i, sp in enumerate(SPLITS):
        for j, am in enumerate(AMBITOS):
            ax = axs[i, j]
            estilo.cuadricula(ax, "x")
            ax.axvline(0, color=INK, lw=0.8, zorder=2)
            for k, r in enumerate(RIVALES_H):
                yb = n_r - 1 - k   # tuned arriba
                for e, _, lw in ESQ_ROB:
                    f = b[(b.split == sp) & (b.ambito == am) & (b.metodo_b == r) & (b.esquema == e)].iloc[0]
                    y = yb + off[e]
                    ax.plot([f.ic_lo, f.ic_hi], [y, y], color=COLOR[r], lw=lw, solid_capstyle="butt", zorder=3)
                    ax.plot([f.brecha], [y], "o", ms=2.6, mfc="white", mec=INK, mew=0.7, zorder=4)
            ax.set_ylim(-0.6, n_r - 0.4)
            ax.set_yticks(range(n_r))
            ax.set_yticklabels([estilo.ETIQUETA[r] for r in reversed(RIVALES_H)])
            ax.spines["left"].set_visible(False)
            ax.tick_params(axis="y", length=0)
            ax.set_title(f"{estilo.ETIQUETA_SPLIT[sp]}, {estilo.ETIQUETA_AMBITO[am]}", fontsize=7.6, fontweight="bold")
            estilo.coma(ax, "x", 2)
            if i == 1:
                ax.set_xlabel(estilo.XLABEL_BRECHA)
    pad = 0.005
    axs[0, 0].set_xlim(lo - pad, max(hi, 0) + pad)
    for ax in axs.flat:
        ax.text(0.02, 0.02, "← favorece a TimesFM", transform=ax.transAxes, ha="left", va="bottom", fontsize=6.4, color=MUTED)
    fig.tight_layout(rect=(0, 0.07, 1, 1), h_pad=1.0, w_pad=0.8)
    hs = [Line2D([0], [0], color=MUTED, lw=lw, solid_capstyle="butt", label=t) for _, t, lw in ESQ_ROB]
    hs.append(Line2D([0], [0], marker="o", ls="", ms=3.2, mfc="white", mec=INK, mew=0.7, label="Brecha puntual"))
    fig.legend(handles=hs, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.005), fontsize=7.0, handlelength=2.2, columnspacing=1.2)
    return _guardar(fig, "fig6_robustez", out_dir)


# --------------------------------------------------------------------------- orquestacion
def generar_todas(out_dir: str | Path = SALIDA) -> list[Path]:
    out_dir = Path(out_dir)
    rutas: list[Path] = []
    for f in (fig1_panel, fig2_brechas, fig3_anual, fig4_zonas, fig5_horizonte, fig6_robustez, sfig_escalera, sfig_a3):
        rutas += f(out_dir)
    return rutas


if __name__ == "__main__":
    for r in generar_todas(sys.argv[1] if len(sys.argv) > 1 else SALIDA):
        print(r)
