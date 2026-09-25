"""Copia el predictions.parquet del backtest anadiendo la columna de TimesFM.

Los archivos originales bajo ``$RES/tuning/backtest/`` no se tocan: son la fuente
de las cifras publicadas y deben seguir reproduciendolas. Aqui se escribe una
copia bajo otra raiz con ``pred_timesfm`` anadida, que es lo que consume
``HPC_code_tunning.effect_sizes`` una vez que ``timesfm`` figura en
``METHOD_COLS``.

La union es interna por ``(ID, FECHA)``: si TimesFM no cubriera alguna celda, esa
celda desaparece para **todos** los metodos, de modo que la comparacion sigue
siendo pareada. El conteo de celdas antes y despues se imprime justamente para que
esa perdida no pase inadvertida — ``effect_sizes`` la propagaria en silencio a
todas las comparaciones por su union interna (`effect_sizes.py:148`).
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import pandas as pd

from tdew_estimation import provenance as prov

from .evaluate import build_row_provenance

logger = logging.getLogger("timesfm.merge")

DEFAULT_BACKTEST_ROOT = Path(
    "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/tuning/backtest"
)


def merge_split(
    split: str,
    variant_parquet: Path,
    *,
    backtest_root: Path = DEFAULT_BACKTEST_ROOT,
    out_root: Path,
) -> dict[str, int]:
    source = backtest_root / split / "predictions.parquet"
    reference = pd.read_parquet(source)
    reference["FECHA"] = pd.to_datetime(reference["FECHA"])
    cells_before = reference["ID"].nunique()

    timesfm = pd.read_parquet(variant_parquet, columns=["ID", "FECHA", "pred"])
    timesfm["FECHA"] = pd.to_datetime(timesfm["FECHA"])
    timesfm = timesfm.rename(columns={"pred": "pred_timesfm"})

    merged = reference.merge(timesfm, on=["ID", "FECHA"], how="inner", validate="one_to_one")
    cells_after = merged["ID"].nunique()

    target_dir = out_root / split
    target_dir.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(target_dir / "predictions.parquet", index=False)

    stats = {
        "rows_reference": len(reference),
        "rows_merged": len(merged),
        "cells_reference": int(cells_before),
        "cells_merged": int(cells_after),
        "cells_lost": int(cells_before - cells_after),
    }
    logger.info("[%s] %s", split, stats)
    if stats["cells_lost"]:
        logger.warning(
            "[%s] se perdieron %d celdas; todas las comparaciones quedan sobre %d celdas",
            split, stats["cells_lost"], cells_after,
        )
    return stats


def score_split(split: str, *, out_root: Path) -> pd.DataFrame:
    """Recalcula metrics.csv sobre el archivo fusionado, con TimesFM incluido."""
    from HPC_code_tunning.effect_sizes import METHOD_COLS, present_methods

    from tdew_estimation.metrics import regression_metrics

    frame = pd.read_parquet(out_root / split / "predictions.parquet").dropna(subset=["TD_obs"])
    methods = present_methods(frame)
    cells = int(frame["ID"].nunique())
    clim = regression_metrics(frame[METHOD_COLS["climatology"]], frame["TD_obs"])["rmse"]
    rows = []
    for name, column in methods.items():
        metrics = regression_metrics(frame[column], frame["TD_obs"])
        rows.append(
            {
                "split": split,
                "method": name,
                "cells": cells,
                **metrics,
                "skill_vs_clim": 1.0 - metrics["rmse"] / clim if clim else float("nan"),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(out_root / split / "metrics.csv", index=False)
    return out


def _provenance_method_name(row_method: str, variant_key: str) -> str:
    """``score_split`` reports the bare method name from METHOD_COLS (``"timesfm"``
    among them); provenance needs the actual variant key, the same
    ``"timesfm:<key>"`` form ``experiments.timesfm.evaluate`` uses."""
    return f"timesfm:{variant_key}" if row_method == "timesfm" else row_method


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-dir", type=Path, required=True,
                        help="directorio con los parquet de TimesFM, <split>__<variante>.parquet")
    parser.add_argument("--variant", required=True, help="clave de la variante a fusionar")
    parser.add_argument("--splits", default="ll1,ll2,ll4")
    parser.add_argument("--backtest-root", type=Path, default=DEFAULT_BACKTEST_ROOT)
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--bead-id", default="tdew-214",
                        help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    parser.add_argument("--panel-id", default=None,
                        help="nombre del panel de celdas fusionado; por defecto, el nombre de --predictions-dir")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    panel_id = args.panel_id or args.predictions_dir.name
    boards = []
    for split in [s.strip() for s in args.splits.split(",") if s.strip()]:
        variant_parquet = args.predictions_dir / f"{split}__{args.variant}.parquet"
        if not variant_parquet.exists():
            logger.warning("falta %s, se omite el split", variant_parquet)
            continue
        merge_split(split, variant_parquet, backtest_root=args.backtest_root, out_root=args.out_root)
        board = score_split(split, out_root=args.out_root)
        print(f"\n=== {split} ===")
        print(board.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
        boards.append(board)

        metrics_path = str(args.out_root / split / "metrics.csv")
        for _, row in board[["method", "cells"]].iterrows():
            method = _provenance_method_name(row["method"], args.variant)
            prov.record_metric_provenance(
                build_row_provenance(
                    method,
                    split=split,
                    cells=int(row["cells"]),
                    bead_id=args.bead_id,
                    panel_id=panel_id,
                    panel_file=str(args.predictions_dir),
                    output_files=(metrics_path,),
                )
            )
    if boards:
        combined = pd.concat(boards, ignore_index=True)
        combined.to_csv(args.out_root / "metrics_all.csv", index=False)
        logger.info("escrito %s", args.out_root / "metrics_all.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
