"""Estilo compartido de las figuras del paper nuevo (TimesFM frente a `tuned`).

Decisiones, con su fuente (presentations/guias, sesiones MIT GTL-AI 4 y 5):
- Un solo color de enfoque (TimesFM) y rivales en tonos apagados: el color guia la
  atencion preatentiva, no decora.
- Sin titulos dentro de la imagen (el mensaje va en el pie de figura de Quarto), sin
  bordes superior y derecho, rejilla solo donde se leen valores, etiquetas directas.
- Multiples pequenos en lugar de ejes duales; una sola escala por eje.
- Paleta Okabe-Ito (segura para daltonismo); el orden de asignacion es fijo.
"""

from __future__ import annotations

import matplotlib as mpl

CM = 1 / 2.54
ANCHO_COMPLETO = 16.0 * CM   # ancho de texto en A4: 16 cm (6,3 in)
ANCHO_MEDIO = 7.8 * CM

# Color por metodo. TimesFM es el foco (verde Okabe-Ito saturado). Los rivales usan
# tonos Okabe-Ito atenuados pero distinguibles entre si y con luminosidad distinta.
COLOR = {
    "timesfm_anom": "#009E73",
    "tuned": "#3F74AE",            # azul atenuado (Okabe-Ito 0072B2); validado con validate_palette
    "llr_rezagos_sel": "#B8821A",  # ocre atenuado (Okabe-Ito E69F00)
    "clim": "#8C8C8C",
    # Variantes de LLR distintas de `llr_rezagos_sel`: ocre claro (rezagos fijos) y marron
    # (simple), para que el ocre pleno signifique solo `llr_rezagos_sel`.
    "llr_rezagos": "#D9B666",
    "llr_simple": "#7A5A28",
    # Rivales que solo aparecen en la Fig. 5 (brecha por horizonte): `tuned_sin_td` en azul claro
    # (misma familia que `tuned`, otra luminosidad) y `llr_simple_sel` en terracota, fuera de los
    # tonos azul, ocre, marron y verde de los demas metodos.
    "tuned_sin_td": "#7DB4E2",
    "llr_simple_sel": "#B5533C",
}
# Color de zona SENAMHI (mapa y leyenda de la Fig. 1b). Es otra variable que el metodo:
# paleta fuera de verde, azul y ocre de los metodos y del gris de la climatologia.
COLOR_ZONA = {
    "A": "#7B3F9E",
    "B": "#D1495B",
    "C": "#17A2B8",
    "D": "#5B6985",
    "E": "#E58AB4",
    "Lago Titicaca": "#111111",
    "Loma": "#B9A7E0",
}
COLOR_AMBITO = {"peru": "#3a3a3a", "fuera": "#c9c9c9"}
ETIQUETA = {
    "timesfm_anom": "TimesFM",
    "tuned": "tuned (Palacios)",
    "llr_rezagos_sel": "LLR con rezagos (sel.)",
    "clim": "Climatología",
    "tuned_sin_td": "tuned sin Td",
    "llr_simple_sel": "LLR simple (sel.)",
}
ETIQUETA_CORTA = {
    "tuned": "vs. tuned",
    "llr_rezagos_sel": "vs. LLR con rezagos (sel.)",
}
ETIQUETA_AMBITO = {"panel": "Dominio completo (17.027 celdas)", "peru": "Perú (8.272 celdas)"}
ETIQUETA_SPLIT = {"ll4b": "2009–2012", "ll4": "2013–2016"}

INK = "#222222"
MUTED = "#6b6b6b"
GRID = "#dedede"
FOCO = COLOR["timesfm_anom"]

# Texto de eje comun a las figuras de brecha.
XLABEL_BRECHA = "Brecha de RMSE: TimesFM − rival (°C)\n(negativo = favorece a TimesFM)"


def aplicar() -> None:
    mpl.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8.5,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5,
        "legend.frameon": False,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "axes.grid": False,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.3,
        "lines.markersize": 4.5,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


def cuadricula(ax, eje: str = "x") -> None:
    """Rejilla fina solo en el eje donde se leen valores."""
    ax.grid(True, axis=eje, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def formato_es(x: float, dec: int = 2) -> str:
    """Numero con coma decimal y signo menos tipografico."""
    return f"{x:+.{dec}f}".replace("-", "−").replace(".", ",")


def coma(ax, eje: str = "y", dec: int = 2) -> None:
    """Separador decimal con coma en las marcas del eje."""
    from matplotlib.ticker import FuncFormatter
    f = FuncFormatter(lambda v, _: f"{v:.{dec}f}".replace("-", "−").replace(".", ","))
    (ax.yaxis if eje == "y" else ax.xaxis).set_major_formatter(f)
