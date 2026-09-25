"""Figuras del benchmark de TimesFM.

PNG estatico y no HTML interactivo porque esta estacion de trabajo se usa por SSH
sin navegador, la misma razon que da `experiments/baselines/plot_leaderboard.py:12`.

Paleta Okabe-Ito, un tono fijo por metodo y jamas reciclado: si un metodo
desaparece de una figura, los demas conservan su color. El orden esta elegido para
que ningun par contiguo baje del umbral de separacion en vision con deficiencia de
color (peor par contiguo, deuteranopia: dE 9,6). Como los tonos claros no alcanzan
3:1 contra el fondo, cada barra lleva su valor escrito y cada figura tiene su CSV
al lado: el color nunca es el unico portador del dato.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# Orden fijo de asignacion, validado con el verificador de paletas.
METHOD_COLORS = {
    "climatology": "#E69F00",
    "tuned": "#0072B2",
    "timesfm": "#009E73",
    "tcn": "#D55E00",
    "zone_ols": "#56B4E9",
    "td_eq_tmin": "#CC79A7",
}
INK = "#2b2b2b"
MUTED = "#6b6b6b"
GRID = "#dcdcdc"

METHOD_LABELS = {
    "climatology": "climatología",
    "tuned": "Palacios (tuned)",
    "zone_ols": "zone_ols",
    "td_eq_tmin": "Td = Tmin",
    "tcn": "TCN directa",
    "timesfm": "TimesFM",
}


def _spread_labels(ax, entries: list[tuple[float, str, str]], x: float) -> None:
    """Escribe etiquetas al final de varias lineas separandolas si se pisan.

    Sin esto, dos metodos con valores parecidos escriben uno encima del otro y la
    cifra se vuelve ilegible, que es justo el caso interesante.
    """
    bottom, top = ax.get_ylim()
    gap = (top - bottom) * 0.045
    entries = sorted(entries, key=lambda item: item[0])
    placed: list[float] = []
    for value, text, color in entries:
        y = value
        if placed and y - placed[-1] < gap:
            y = placed[-1] + gap
        placed.append(y)
        ax.text(x, y, text, fontsize=8.5, color=color, va="center", ha="left")


def color_for(method: str) -> str:
    if method.startswith("timesfm"):
        return METHOD_COLORS["timesfm"]
    return METHOD_COLORS.get(method, MUTED)


def label_for(method: str) -> str:
    if method.startswith("timesfm:"):
        return method.split(":", 1)[1]
    return METHOD_LABELS.get(method, method)


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(INK)


def variant_ladder(leaderboard: pd.DataFrame, out_path: Path, *, split: str = "ll4") -> Path:
    """Escalera de RMSE: las variantes de TimesFM junto a los rivales.

    Barras horizontales porque las etiquetas de metodo son largas y el trabajo de
    la figura es comparar magnitudes entre identidades. La climatologia es la
    linea de referencia: por debajo, el metodo aporta; por encima, no.
    """
    frame = leaderboard[leaderboard["split"] == split].sort_values("rmse", ascending=False)
    clim = float(frame.loc[frame["method"] == "climatology", "rmse"].iloc[0])

    height = max(3.2, 0.32 * len(frame) + 1.6)
    fig, ax = plt.subplots(figsize=(8.2, height))
    positions = np.arange(len(frame))
    colors = [color_for(m) for m in frame["method"]]
    ax.barh(positions, frame["rmse"], color=colors, height=0.68)
    ax.set_yticks(positions)
    ax.set_yticklabels([label_for(m) for m in frame["method"]], fontsize=9)

    for y, value in zip(positions, frame["rmse"]):
        ax.text(value + clim * 0.012, y, f"{value:.3f}", va="center", ha="left",
                fontsize=8.5, color=INK)

    ax.axvline(clim, color=METHOD_COLORS["climatology"], lw=2, zorder=3)
    ax.text(clim, len(frame) - 0.3, f" climatología {clim:.3f}", fontsize=8.5,
            color=MUTED, va="top", ha="left")

    ax.set_xlabel("RMSE (°C) — menor es mejor")
    ax.set_title(f"Reconstrucción de Td en el bloque oculto {split} — {int(frame['cells'].iloc[0])} celdas")
    ax.set_xlim(0, float(frame["rmse"].max()) * 1.12)
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def throughput_curve(frame: pd.DataFrame, out_path: Path) -> Path:
    """Celdas por segundo segun la longitud del contexto, una linea por horizonte."""
    best = (
        frame[frame["status"] == "ok"]
        .groupby(["context", "horizon"], as_index=False)["cells_per_second"]
        .max()
    )
    fig, ax = plt.subplots(figsize=(7, 4.2))
    palette = ["#0072B2", "#009E73", "#D55E00"]
    for index, (horizon, group) in enumerate(best.groupby("horizon")):
        group = group.sort_values("context")
        color = palette[index % len(palette)]
        ax.plot(group["context"], group["cells_per_second"], "o-", color=color, lw=2,
                markersize=6, label=f"horizonte {horizon} d")
        # Se etiqueta el extremo izquierdo, donde las lineas estan separadas; a la
        # derecha convergen y tres etiquetas se pisarian. El valor de ese extremo va
        # en el texto del informe y en el CSV.
        first = group.iloc[0]
        ax.text(first["context"] * 0.93, first["cells_per_second"],
                f"{first['cells_per_second']:.1f}", fontsize=8.5, color=color,
                va="center", ha="right")

    ax.set_xscale("log")
    ax.set_xticks(sorted(best["context"].unique()))
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlim(best["context"].min() * 0.62, best["context"].max() * 1.35)
    ax.set_ylim(0, float(best["cells_per_second"].max()) * 1.12)
    ax.set_xlabel("longitud del contexto (días)")
    ax.set_ylabel("celdas por segundo")
    ax.set_title("Costo de TimesFM 3 en la RTX A2000\nel contexto manda; el tamaño de lote satura en 8–16")
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9, labelcolor=MUTED)
    _style(ax)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def pinball_by_decile(leaderboard: pd.DataFrame, out_path: Path, *, split: str = "ll4",
                      top: int = 4) -> Path:
    """Perdida pinball por decil de las mejores variantes.

    Solo TimesFM aparece: los rivales no entregan distribucion, asi que esta
    figura describe al modelo, no lo compara.
    """
    frame = leaderboard[
        (leaderboard["split"] == split) & leaderboard["method"].str.startswith("timesfm:")
    ].nsmallest(top, "rmse")
    levels = np.arange(10, 100, 10)
    columns = [f"pinball_q{q:02d}" for q in levels]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    palette = ["#009E73", "#0072B2", "#D55E00", "#CC79A7"]
    for index, (_, row) in enumerate(frame.iterrows()):
        color = palette[index % len(palette)]
        ax.plot(levels / 100, [row[c] for c in columns], "o-", color=color, lw=2,
                markersize=6, label=label_for(row["method"]))
    ax.set_xlabel("nivel del cuantil")
    ax.set_ylabel("pérdida pinball (°C)")
    ax.set_title("Calibración por decil\nno hay q05 ni q95: el intervalo más ancho posible es el 80 %")
    ax.set_xticks(levels / 100)
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9, labelcolor=MUTED)
    _style(ax)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def accuracy_vs_cost(
    leaderboard: pd.DataFrame,
    runtime: pd.DataFrame,
    out_path: Path,
    *,
    split: str = "ll4",
    national_cells: int = 2_818_404,
) -> Path:
    """Precision contra costo: RMSE frente a horas de GPU por pasada nacional.

    Es la figura que decide si el modelo es utilizable a escala. Una variante que
    gana 0,01 °C a cambio de cuadruplicar el tiempo de computo no sirve para
    rellenar 2,8 millones de celdas.
    """
    board = leaderboard[
        (leaderboard["split"] == split) & leaderboard["method"].str.startswith("timesfm:")
    ].copy()
    board["variant"] = board["method"].str.split(":", n=1).str[1]
    merged = board.merge(runtime[["variant", "cells_per_second"]], on="variant", how="inner")
    merged["horas_nacional"] = national_cells / merged["cells_per_second"] / 3600.0

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.set_xscale("log")
    low, high = float(merged["horas_nacional"].min()), float(merged["horas_nacional"].max())
    ax.set_xlim(low * 0.55, high * 1.9)
    ax.scatter(merged["horas_nacional"], merged["rmse"], s=70,
               color=METHOD_COLORS["timesfm"], zorder=3)
    for _, row in merged.iterrows():
        ax.annotate(row["variant"], (row["horas_nacional"], row["rmse"]),
                    textcoords="offset points", xytext=(9, 3), fontsize=8.5, color=INK)

    # Las lineas de referencia se rotulan a la izquierda para no chocar con los
    # nombres de las variantes, que salen hacia la derecha de cada punto.
    for name in ("climatology", "tuned"):
        values = leaderboard.loc[
            (leaderboard["split"] == split) & (leaderboard["method"] == name), "rmse"
        ]
        if values.empty:
            continue
        value = float(values.iloc[0])
        ax.axhline(value, color=METHOD_COLORS[name], lw=2, ls="--")
        ax.text(ax.get_xlim()[0] * 1.06, value, f"{label_for(name)} {value:.3f}",
                fontsize=8.5, color=METHOD_COLORS[name], va="bottom", ha="left")

    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    # Varias variantes cuestan casi lo mismo; sin depurar, sus marcas se escriben
    # una encima de otra y ninguna se lee.
    ticks: list[float] = []
    for value in sorted(merged["horas_nacional"].round(0).unique()):
        if not ticks or value / ticks[-1] > 1.09:
            ticks.append(float(value))
    ax.set_xticks(ticks)
    ax.set_xlabel("horas de GPU para una pasada de las 2,8 M celdas del grid nacional")
    ax.set_ylabel("RMSE (°C)")
    ax.set_title("Precisión contra costo de las variantes de TimesFM")
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def error_growth(
    curves: pd.DataFrame, out_path: Path, *, split: str = "ll4"
) -> Path:
    """RMSE acumulado dia a dia del bloque oculto, una linea por metodo.

    Responde la pregunta que una sola cifra esconde: si el modelo se degrada con
    la distancia al ultimo dato observado o si su error es plano.
    """
    fig, ax = plt.subplots(figsize=(8, 4.6))
    # Se ordenan las series por su valor final para que la leyenda siga el mismo
    # orden vertical que las lineas.
    order = (
        curves.sort_values("dia").groupby("method").tail(1).sort_values("rmse_acumulado", ascending=False)
    )
    ends: list[tuple[float, str, str]] = []
    for method in order["method"]:
        group = curves[curves["method"] == method].sort_values("dia")
        ax.plot(group["dia"], group["rmse_acumulado"], color=color_for(method), lw=2,
                label=label_for(method))
        last = group.iloc[-1]
        ends.append((float(last["rmse_acumulado"]), f"{last['rmse_acumulado']:.3f}", color_for(method)))
    last_day = float(curves["dia"].max())
    ax.set_xlim(0, last_day * 1.12)
    # Se deja aire arriba para que la leyenda no se pise con la etiqueta de la
    # serie mas alta.
    ax.set_ylim(top=float(curves["rmse_acumulado"].max()) * 1.18)
    _spread_labels(ax, ends, last_day * 1.02)
    ax.set_xlabel("días transcurridos desde el último Td observado")
    ax.set_ylabel("RMSE acumulado (°C)")
    ax.set_title(f"Crecimiento del error dentro del bloque oculto — {split}")
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9, labelcolor=MUTED)
    _style(ax)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path
