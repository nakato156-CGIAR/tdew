"""Prueba pareada por celda de TimesFM contra cada rival del panel departamental.

Lee ``departamental/predicciones_largo.parquet`` (las seis series que puntua
``departamental.py``: TimesFM, la TCN con semillas 0, 1 y 2, ``tuned`` y la
climatologia, sobre las mismas 2.048 celdas y 1.461 dias) y, para cada rival, calcula
con las mismas funciones que ``HPC_code_tunning/effect_sizes.py``:

- ``delta_rmse = RMSE_timesfm - RMSE_rival`` agrupado sobre celdas-dia (negativo
  favorece a TimesFM), con IC 95 % por bootstrap de celdas (``n_boot`` remuestreos);
- la fraccion de celdas donde TimesFM tiene menor RMSE propio;
- d de Cohen pareado y p de permutacion por cambio de signo sobre el ΔRMSE por celda;
- el RMSE mediano por celda de cada metodo.

El ``tuned`` de este panel usa recetas seleccionadas con 1981-2016 (con fuga).

Uso::

    uv run python -m experiments.timesfm.departamental_pareado \\
        --out reports/timesfm_benchmark/departamental/pareado.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from HPC_code_tunning.effect_sizes import (
    block_bootstrap_delta,
    cohens_d_paired,
    per_location_delta_rmse,
    sign_flip_permutation,
)
from tdew_estimation import provenance as prov

from .evaluate import build_row_provenance

DEFAULT_LONG = Path("reports/timesfm_benchmark/departamental/predicciones_largo.parquet")
DEFAULT_OUT = Path("reports/timesfm_benchmark/departamental/pareado.csv")
FOCAL = ("timesfm", 0)
VARIANT_KEY = "tmin_anom_full"


def per_cell_stats(long: pd.DataFrame) -> pd.DataFrame:
    """``se_<serie>``/``n_<serie>`` por celda, una columna por (modelo, semilla)."""
    err = long["TD_pred"].to_numpy(float) - long["TD_obs"].to_numpy(float)
    work = pd.DataFrame({"ID": long["ID"].to_numpy(), "series": long["model"] + "_s" + long["seed"].astype(str),
                         "se": err ** 2, "n": np.isfinite(err).astype(int)})
    work = work[np.isfinite(work["se"])]
    grouped = work.groupby(["ID", "series"])[["se", "n"]].sum().unstack("series")
    grouped.columns = [f"{stat}_{series}" for stat, series in grouped.columns]
    return grouped.reset_index()


def paired_table(long: pd.DataFrame, *, n_boot: int, n_perm: int, seed: int) -> pd.DataFrame:
    per_id = per_cell_stats(long)
    focal = f"{FOCAL[0]}_s{FOCAL[1]}"
    rivals = sorted({f"{m}_s{s}" for m, s in long[["model", "seed"]].drop_duplicates().itertuples(index=False)}
                    - {focal})
    rows = []
    for rival in rivals:
        boot = block_bootstrap_delta(per_id, focal, rival, n_boot, seed)
        delta_cell = per_location_delta_rmse(per_id, focal, rival)  # positivo = TimesFM mejor
        cell_rmse = lambda s: np.sqrt(per_id[f"se_{s}"] / per_id[f"n_{s}"])  # noqa: E731
        model, rival_seed = rival.rsplit("_s", 1)
        rows.append({
            "rival": model, "rival_seed": int(rival_seed), "cells": len(per_id),
            "rmse_timesfm": boot["rmse"], "rmse_rival": boot["rmse_baseline"],
            # Signo del README: TimesFM menos rival; negativo favorece a TimesFM.
            "delta_rmse": -boot["delta_rmse"], "delta_lo": -boot["delta_hi"], "delta_hi": -boot["delta_lo"],
            "frac_cells_timesfm_wins": float(np.mean(delta_cell > 0)),
            "cohen_d_paired": cohens_d_paired(delta_cell),
            "p_perm": sign_flip_permutation(delta_cell, n_perm, seed),
            "median_cell_rmse_timesfm": float(np.median(cell_rmse(focal))),
            "median_cell_rmse_rival": float(np.median(cell_rmse(rival))),
            "n_boot": n_boot, "n_perm": n_perm, "seed": seed,
        })
    return pd.DataFrame(rows)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--long", type=Path, default=DEFAULT_LONG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--n-boot", type=int, default=1000)
    parser.add_argument("--n-perm", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--bead-id", default="tdew-214.14.4")
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    args = parser.parse_args(argv)

    long = pd.read_parquet(args.long, columns=["ID", "TD_obs", "TD_pred", "model", "seed"])
    table = paired_table(long, n_boot=args.n_boot, n_perm=args.n_perm, seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out, index=False)
    print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    prov.record_metric_provenance(
        build_row_provenance(
            f"timesfm:{VARIANT_KEY}", split="ll4", cells=int(table["cells"].iloc[0]), bead_id=args.bead_id,
            panel_id="departamental_2048", panel_file=None, output_files=(str(args.out),),
            notes=(f"Prueba pareada por celda contra cada rival de {args.long}; bootstrap de celdas "
                   f"n_boot={args.n_boot}, permutacion por cambio de signo n_perm={args.n_perm}, seed={args.seed}. "
                   "tuned con seleccion de recetas con fuga (1981-2016)."),
        ),
        registry_path=args.registry_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
