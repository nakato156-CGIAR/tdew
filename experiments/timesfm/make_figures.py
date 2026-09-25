"""Genera de una vez todas las figuras del informe que ya tengan datos.

Cada figura se salta en silencio si le falta su insumo, de modo que el comando se
puede correr en cualquier momento del benchmark y produce lo que haya.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import pandas as pd

from . import plots

logger = logging.getLogger("timesfm.figuras")

REPORT = Path("reports/timesfm_benchmark")


def build(report: Path = REPORT, *, runtime_csv: Path | None = None) -> list[Path]:
    figs = report / "figs"
    made: list[Path] = []

    coste = report / "coste_throughput.csv"
    if coste.exists():
        made.append(plots.throughput_curve(pd.read_csv(coste), figs / "coste_throughput.png"))

    leaderboard = report / "cribado" / "leaderboard.csv"
    if leaderboard.exists():
        board = pd.read_csv(leaderboard)
        made.append(plots.variant_ladder(board, figs / "escalera_cribado.png"))
        if {f"pinball_q{q:02d}" for q in range(10, 100, 10)} <= set(board.columns):
            made.append(plots.pinball_by_decile(board, figs / "calibracion_cribado.png"))
        if runtime_csv and Path(runtime_csv).exists():
            made.append(
                plots.accuracy_vs_cost(board, pd.read_csv(runtime_csv), figs / "precision_costo.png")
            )

    curva = report / "curva_error_cribado.csv"
    if curva.exists():
        made.append(plots.error_growth(pd.read_csv(curva), figs / "crecimiento_error_cribado.png"))

    nacional = report / "nacional" / "leaderboard.csv"
    if nacional.exists():
        made.append(plots.variant_ladder(pd.read_csv(nacional), figs / "escalera_nacional.png"))

    curva_nacional = report / "curva_error_nacional.csv"
    if curva_nacional.exists():
        made.append(
            plots.error_growth(pd.read_csv(curva_nacional), figs / "crecimiento_error_nacional.png")
        )

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
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    made = build(args.report, runtime_csv=args.runtime_csv)
    print(f"{len(made)} figuras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
