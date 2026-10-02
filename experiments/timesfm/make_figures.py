"""Genera de una vez todas las figuras del informe que ya tengan datos.

Cada figura se salta en silencio si le falta su insumo, de modo que el comando se
puede correr en cualquier momento del benchmark y produce lo que haya.
"""

from __future__ import annotations

import argparse
import logging
import shutil
from pathlib import Path
from typing import Sequence

import pandas as pd

from . import plots

logger = logging.getLogger("timesfm.figuras")

REPORT = Path("reports/timesfm_benchmark")


# figura publicada -> (archivo copiado por effect_sizes dentro de nacional<sufijo>/)
_EFFECT_FIGURES = {
    "nacional_curva_horizonte": "lead_time_curve.png",
    "nacional_bias_by_month": "ll4_bias_by_month.png",
    "nacional_delta_rmse_hist": "ll4_delta_rmse_hist.png",
    "nacional_rmse_ladder": "ll4_rmse_ladder.png",
    "nacional_ll1_rmse_ladder": "ll1_rmse_ladder.png",
    "nacional_ll2_rmse_ladder": "ll2_rmse_ladder.png",
}


def build(report: Path = REPORT, *, runtime_csv: Path | None = None, suffix: str = "") -> list[Path]:
    """Con ``suffix`` (p. ej. ``"_limpio"``) lee de ``nacional<suffix>/``,
    ``cribado<suffix>/`` y ``curva_error_*<suffix>.csv`` y escribe figuras con el mismo
    sufijo, sin tocar las figuras sin sufijo. La curva de costo no depende de la
    referencia de backtest y solo se regenera sin sufijo."""
    figs = report / "figs"
    made: list[Path] = []

    coste = report / "coste_throughput.csv"
    if coste.exists() and not suffix:
        made.append(plots.throughput_curve(pd.read_csv(coste), figs / "coste_throughput.png"))

    leaderboard = report / f"cribado{suffix}" / "leaderboard.csv"
    if leaderboard.exists():
        board = pd.read_csv(leaderboard)
        made.append(plots.variant_ladder(board, figs / f"escalera_cribado{suffix}.png"))
        if {f"pinball_q{q:02d}" for q in range(10, 100, 10)} <= set(board.columns):
            made.append(plots.pinball_by_decile(board, figs / f"calibracion_cribado{suffix}.png"))
        if runtime_csv and Path(runtime_csv).exists():
            made.append(
                plots.accuracy_vs_cost(
                    board, pd.read_csv(runtime_csv), figs / f"precision_costo{suffix}.png"
                )
            )

    curva = report / f"curva_error_cribado{suffix}.csv"
    if curva.exists():
        made.append(
            plots.error_growth(pd.read_csv(curva), figs / f"crecimiento_error_cribado{suffix}.png")
        )

    nacional = report / f"nacional{suffix}" / "leaderboard.csv"
    if nacional.exists():
        made.append(
            plots.variant_ladder(pd.read_csv(nacional), figs / f"escalera_nacional{suffix}.png")
        )

    curva_nacional = report / f"curva_error_nacional{suffix}.csv"
    if curva_nacional.exists():
        made.append(
            plots.error_growth(
                pd.read_csv(curva_nacional), figs / f"crecimiento_error_nacional{suffix}.png"
            )
        )

    if suffix:
        for target, source in _EFFECT_FIGURES.items():
            origin = report / f"nacional{suffix}" / source
            if origin.exists():
                destination = figs / f"{target}{suffix}.png"
                shutil.copyfile(origin, destination)
                made.append(destination)

    for path in made:
        logger.info("escrita %s", path)
    return made


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument(
        "--runtime-csv",
        type=Path,
        default=Path("/home/cvelasquez/tdew_timesfm/preds_cribado/runtime_ll4.csv"),
    )
    parser.add_argument("--suffix", default="",
                        help='sufijo de las entradas y salidas, p. ej. "_limpio"')
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    made = build(args.report, runtime_csv=args.runtime_csv, suffix=args.suffix)
    print(f"{len(made)} figuras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
