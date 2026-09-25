"""Une TimesFM y el metodo de Palacios a la tabla del panel departamental.

El pipeline de reconstruccion (`experiments/reconstruction/cli.py`) ya escribe el
formato largo canonico que `evaluation.py` sabe puntuar: una fila por
`(ID, fecha, modelo, semilla, fold)` con `TD_obs`, `TD_clim` y `TD_pred`. Aqui se
traen los otros dos competidores a ese mismo formato.

`TD_obs` y `TD_clim` se toman de la salida de reconstruccion y no se recalculan.
Es deliberado: si cada competidor trajera su propia verdad y su propia
climatologia, una diferencia de metodo quedaria mezclada con una diferencia de
contabilidad. La paridad entre ambas fuentes se comprueba antes de unir.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from tdew_estimation import provenance as prov

from .evaluate import DEFAULT_BACKTEST_ROOT

logger = logging.getLogger("timesfm.departamental")

# "climatology" y "timesfm" (bare, sin variante) aparecen aqui porque este
# archivo los inserta el mismo con ese nombre (climatology_to_long,
# timesfm_to_long); ninguno de los dos sigue la convencion _direct/_recursive
# de cli.py ni esta en evaluate._KNOWN_AUTOREGRESSIVE, asi que sin este
# override evaluate.build_model_fold_provenance los rechazaria (correctamente:
# no puede adivinarlos por el nombre). Ambos son de una sola pasada, no
# autorregresivos.
_LOCAL_AUTOREGRESSIVE_OVERRIDES = {"climatology": False, "timesfm": False}

CANONICAL_COLUMNS = (
    "ID", "department", "date", "year_horizon", "TD_obs", "TD_clim",
    "TD_pred", "model", "seed", "fold",
)
CLIMATOLOGY_TOLERANCE = 1e-4  # misma tolerancia que la paridad de Tmin del protocolo


def _skeleton(reference_long: pd.DataFrame) -> pd.DataFrame:
    """Metadatos comunes: una fila por `(ID, fecha)`, sin prediccion ni modelo."""
    keys = ["ID", "department", "date", "year_horizon", "TD_obs", "TD_clim", "fold"]
    return reference_long[keys].drop_duplicates(subset=["ID", "date"]).reset_index(drop=True)


def timesfm_to_long(
    predictions_parquet: Path,
    reference_long: pd.DataFrame,
    *,
    model: str = "timesfm",
    seed: int = 0,
) -> pd.DataFrame:
    """Convierte la salida de `experiments.timesfm.run` al formato canonico."""
    frame = pd.read_parquet(predictions_parquet, columns=["ID", "FECHA", "pred"])
    frame = frame.rename(columns={"FECHA": "date", "pred": "TD_pred"})
    frame["date"] = pd.to_datetime(frame["date"])

    skeleton = _skeleton(reference_long)
    skeleton["date"] = pd.to_datetime(skeleton["date"])
    merged = skeleton.merge(frame, on=["ID", "date"], how="inner", validate="one_to_one")
    if len(merged) != len(skeleton):
        logger.warning(
            "TimesFM cubre %d de %d filas del panel; la tabla queda sobre la interseccion",
            len(merged), len(skeleton),
        )
    merged["model"] = model
    merged["seed"] = int(seed)
    return merged[list(CANONICAL_COLUMNS)]


def tuned_to_long(
    backtest_predictions: Path,
    reference_long: pd.DataFrame,
    *,
    model: str = "tuned",
    seed: int = 0,
    check_climatology: bool = True,
) -> pd.DataFrame:
    """Trae `pred_tuned` del backtest de Palacios al formato canonico.

    Con ``check_climatology`` se compara la climatologia de ambas fuentes antes de
    unir. Si difieren mas que la tolerancia, la comparacion no es sobre el mismo
    terreno y conviene detenerse en lugar de publicar la tabla.
    """
    frame = pd.read_parquet(backtest_predictions, columns=["ID", "FECHA", "TD_obs", "pred_clim", "pred_tuned"])
    frame = frame.rename(columns={"FECHA": "date"})
    frame["date"] = pd.to_datetime(frame["date"])

    skeleton = _skeleton(reference_long)
    skeleton["date"] = pd.to_datetime(skeleton["date"])
    merged = skeleton.merge(frame, on=["ID", "date"], how="inner", validate="one_to_one")
    if merged.empty:
        raise ValueError("el backtest de Palacios no cubre ninguna celda del panel departamental")

    if check_climatology:
        gap_clim = np.abs(merged["TD_clim"].to_numpy(float) - merged["pred_clim"].to_numpy(float))
        gap_obs = np.abs(merged["TD_obs_x"].to_numpy(float) - merged["TD_obs_y"].to_numpy(float))
        worst_clim, worst_obs = float(np.nanmax(gap_clim)), float(np.nanmax(gap_obs))
        logger.info("paridad con el backtest: climatologia %.2e, Td observado %.2e", worst_clim, worst_obs)
        if worst_clim > CLIMATOLOGY_TOLERANCE or worst_obs > CLIMATOLOGY_TOLERANCE:
            raise ValueError(
                f"las dos fuentes no coinciden (climatologia {worst_clim:.2e}, "
                f"Td observado {worst_obs:.2e}); la comparacion no seria sobre el mismo terreno"
            )

    merged = merged.rename(columns={"TD_obs_x": "TD_obs", "pred_tuned": "TD_pred"})
    merged["model"] = model
    merged["seed"] = int(seed)
    return merged[list(CANONICAL_COLUMNS)]


def climatology_to_long(reference_long: pd.DataFrame, *, seed: int = 0) -> pd.DataFrame:
    """La climatologia como competidor explicito, para que aparezca en la escalera."""
    skeleton = _skeleton(reference_long)
    skeleton["TD_pred"] = skeleton["TD_clim"]
    skeleton["model"] = "climatology"
    skeleton["seed"] = int(seed)
    return skeleton[list(CANONICAL_COLUMNS)]


def assemble(
    reconstruction_parquets: Sequence[Path],
    *,
    timesfm_parquet: Path | None = None,
    backtest_predictions: Path | None = None,
    include_climatology: bool = True,
) -> pd.DataFrame:
    """Junta todos los competidores en una sola tabla larga."""
    pieces = [pd.read_parquet(path) for path in reconstruction_parquets]
    if not pieces:
        raise ValueError("hace falta al menos una salida del pipeline de reconstruccion")
    reference = pieces[0]
    for frame in pieces:
        frame["date"] = pd.to_datetime(frame["date"])

    if include_climatology:
        pieces.append(climatology_to_long(reference))
    if timesfm_parquet is not None:
        pieces.append(timesfm_to_long(timesfm_parquet, reference))
    if backtest_predictions is not None:
        pieces.append(tuned_to_long(backtest_predictions, reference))

    out = pd.concat(pieces, ignore_index=True)
    out["date"] = pd.to_datetime(out["date"])
    return out


def main(argv: Sequence[str] | None = None) -> int:
    from experiments.reconstruction.evaluate import (
        UnknownAutoregressiveStatus,
        build_model_fold_provenance,
    )
    from experiments.reconstruction.evaluation import (
        cumulative_error_curve,
        evaluate_predictions,
        macro_department_metrics,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reconstruction", type=Path, nargs="+", required=True,
                        help="parquets del pipeline de reconstruccion (TCN, ridge, histgb)")
    parser.add_argument("--timesfm", type=Path, default=None)
    parser.add_argument("--backtest-predictions", type=Path,
                        default=DEFAULT_BACKTEST_ROOT / "ll4" / "predictions.parquet")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--bead-id", default="tdew-214",
                        help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    long = assemble(
        args.reconstruction,
        timesfm_parquet=args.timesfm,
        backtest_predictions=args.backtest_predictions,
    )
    predictions_path = args.out_dir / "predicciones_largo.parquet"
    long.to_parquet(predictions_path, index=False)

    metrics = evaluate_predictions(long)
    metrics_path = args.out_dir / "metrics.csv"
    metrics_macro_path = args.out_dir / "metrics_macro.csv"
    curve_path = args.out_dir / "curva_acumulada.csv"
    metrics.to_csv(metrics_path, index=False)
    macro_department_metrics(metrics).to_csv(metrics_macro_path, index=False)
    cumulative_error_curve(long).to_csv(curve_path, index=False)

    pooled = metrics[metrics["level"] == "pooled"].sort_values("rmse")
    print(pooled[["model", "seed", "n", "rmse", "mae", "bias", "r", "skill_vs_climatology"]]
          .to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    output_files = (str(metrics_path), str(metrics_macro_path), str(curve_path), str(predictions_path))
    for (model, fold, seed), group in long.groupby(["model", "fold", "seed"]):
        try:
            record = build_model_fold_provenance(
                str(model), str(fold), cells=int(group["ID"].nunique()),
                bead_id=args.bead_id, output_files=output_files,
                autoregressive_overrides=_LOCAL_AUTOREGRESSIVE_OVERRIDES,
                seed=int(seed), panel_id="departamental",
            )
        except UnknownAutoregressiveStatus as exc:
            logger.warning("[%s/%s/seed%s] se omite la proveniencia: %s", model, fold, seed, exc)
            continue
        prov.record_metric_provenance(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
