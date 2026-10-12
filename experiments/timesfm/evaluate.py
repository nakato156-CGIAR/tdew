"""Puntuacion de las variantes de TimesFM junto a los rivales de Palacios.

Todos los metodos se puntuan sobre exactamente las mismas celdas y los mismos
dias: los rivales se leen del ``predictions.parquet`` que produjo
``HPC_code_tunning/backtest.py`` y se restringen a las celdas que TimesFM
alcanzo, de modo que ninguna diferencia venga de la muestra.

Las metricas puntuales son las mismas que reporta el backtest
(`tdew_estimation.metrics.regression_metrics`): n, RMSE, MAE, sesgo y r, mas
skill frente a climatologia. Las probabilisticas solo aplican a TimesFM, que es
el unico metodo que entrega distribucion.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from HPC_code_tunning.backtest import RIVAL_PROVENANCE, build_rival_provenance
from tdew_estimation import provenance as prov
from tdew_estimation.metrics import regression_metrics

from . import paths
from .panel import SPLITS
from .probabilistic import COLUMNS as QUANTILE_COLUMNS
from .probabilistic import probabilistic_metrics
from .variants import BY_KEY as KNOWN_VARIANTS
from .variants import variant as get_variant

logger = logging.getLogger("timesfm.evaluate")

RIVALS = {
    "climatology": "pred_clim",
    "td_eq_tmin": "pred_tmin",
    "zone_ols": "pred_ols",
    "tuned": "pred_tuned",
}
_RES_TUNING = paths.RES / "tuning"
# Run con fuga: la seleccion de recetas vio los anos 1981-2016. Se conserva solo
# como referencia historica; no es el default.
LEAKY_BACKTEST_ROOT = _RES_TUNING / "backtest"
# Run limpio: seleccion solo con anos de entrenamiento. Es la referencia del paper.
CLEAN_BACKTEST_ROOT = _RES_TUNING / "backtest_clean"
DEFAULT_BACKTEST_ROOT = CLEAN_BACKTEST_ROOT

MANIFEST_REF = "docs/protocol/timesfm_manifest.yaml@2026-09-22"
# Variantes retiradas del protocolo (enmienda del manifiesto, 2026-09-25). Sus parquet
# pueden seguir en disco; no se puntuan ni se registran.
RETIRED_VARIANTS = frozenset({"tmin_td_25"})
# Addendum fechado que fija la referencia limpia (PLAN_1 §Paso 8).
MANIFEST_REF_LIMPIO = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"


def manifest_ref_for(backtest_root: Path) -> str:
    """El documento que gobierna una corrida segun su raiz de referencia: el
    addendum para la raiz limpia, el manifiesto original para cualquier otra."""
    if Path(backtest_root).resolve() == CLEAN_BACKTEST_ROOT.resolve():
        return MANIFEST_REF_LIMPIO
    return MANIFEST_REF


def backtest_notes(backtest_root: Path, *, cells: int, extra: str | None = None) -> str:
    """Texto de ``MetricProvenance.notes``: la raiz de referencia usada, como
    selecciono sus recetas y sobre cuantas celdas se puntuo. La descripcion de la
    seleccion depende de la raiz: no se afirma "limpia" para una raiz que no lo es."""
    root = Path(backtest_root).resolve()
    if root == CLEAN_BACKTEST_ROOT.resolve():
        selection = "selección solo con años de entrenamiento, h {7,11,15,21,31,45}"
    elif root == LEAKY_BACKTEST_ROOT.resolve():
        selection = "selección con fuga (vio los años 1981-2016)"
    else:
        selection = "selección no declarada"
    note = f"backtest_root={root}; {selection}; cells={cells}"
    return f"{note}; {extra}" if extra else note


def build_row_provenance(
    method: str,
    *,
    split: str,
    cells: int,
    bead_id: str,
    panel_id: str,
    panel_file: str,
    output_files: tuple[str, ...],
    notes: str | None = None,
    manifest_ref: str = MANIFEST_REF,
) -> prov.MetricProvenance:
    """El registro de proveniencia de una fila de ``leaderboard.csv`` (un metodo,
    un split). ``method`` es ``"timesfm:<key>"`` para las variantes de este
    proyecto, o uno de los cuatro nombres de ``RIVALS`` para los metodos de
    Palacios (``RIVAL_PROVENANCE``/``build_rival_provenance`` viven en
    ``HPC_code_tunning.backtest``, el origen real de esas cuatro predicciones,
    para que este archivo no mantenga su propia copia que pueda desviarse)."""
    if method.startswith("timesfm:"):
        key = method.split(":", 1)[1]
        spec = get_variant(key)
        train_end_year, holdout_years = SPLITS[split]
        test_period = (f"{holdout_years[0]}-01-01", f"{holdout_years[1]}-12-31")
        return prov.MetricProvenance(
            run_id=prov.new_run_id(),
            generated_at=prov.now_iso(),
            git_commit=prov.git_commit(),
            bead_id=bead_id,
            manifest_ref=manifest_ref,
            model_family=spec.family,
            model_id=spec.checkpoint,
            variant_label=key,
            trained=False,
            training_period=None,
            validation_period=None,
            test_period=test_period,
            split_id=split,
            autoregressive=spec.autoregressive,
            target_type=spec.target_type,
            climatology_used=spec.climatology_used,
            climatology_role=spec.climatology_role,
            inputs=tuple(spec.inputs),
            panel_id=panel_id,
            panel_cell_count=cells,
            panel_file=panel_file,
            output_files=output_files,
            notes=notes,
        )

    return build_rival_provenance(
        method,
        split=split,
        cells=cells,
        bead_id=bead_id,
        manifest_ref=manifest_ref,
        panel_id=panel_id,
        panel_file=panel_file,
        output_files=output_files,
        notes=notes,
    )


def load_reference(split: str, *, backtest_root: Path = DEFAULT_BACKTEST_ROOT) -> pd.DataFrame:
    path = backtest_root / split / "predictions.parquet"
    frame = pd.read_parquet(path, columns=["ID", "zone_id", "FECHA", "TD_obs", *RIVALS.values()])
    frame["FECHA"] = pd.to_datetime(frame["FECHA"])
    return frame


def score_split(
    predictions_dir: Path,
    split: str,
    *,
    backtest_root: Path = DEFAULT_BACKTEST_ROOT,
    by_zone: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (leaderboard, metricas por zona) para un split."""
    files = sorted(predictions_dir.glob(f"{split}__*.parquet"))
    if not files:
        raise FileNotFoundError(f"sin predicciones de TimesFM para {split} en {predictions_dir}")

    reference = load_reference(split, backtest_root=backtest_root)
    rows: list[dict[str, object]] = []
    zone_rows: list[dict[str, object]] = []
    rivals_done = False
    zone_rivals_done = False

    for path in files:
        key = path.stem.split("__", 1)[1]
        if key in RETIRED_VARIANTS:
            logger.warning("[%s] variante retirada del protocolo, se omite: %s", key, path.name)
            continue
        if key not in KNOWN_VARIANTS:
            logger.warning("[%s] variante desconocida para el registro, se omite: %s", key, path.name)
            continue
        pred = pd.read_parquet(path)
        pred["FECHA"] = pd.to_datetime(pred["FECHA"])
        merged = pred.merge(reference, on=["ID", "FECHA"], how="inner", validate="one_to_one")
        if merged.empty:
            logger.warning("[%s] sin interseccion con el backtest", key)
            continue
        cells = merged["ID"].nunique()

        clim = regression_metrics(merged["pred_clim"], merged["TD_obs"])["rmse"]
        point = regression_metrics(merged["pred"], merged["TD_obs"])
        row = {
            "split": split,
            "method": f"timesfm:{key}",
            "cells": cells,
            **point,
            "skill_vs_clim": 1.0 - point["rmse"] / clim if clim else np.nan,
        }
        prob = probabilistic_metrics(merged)
        # El `n` de las metricas probabilisticas cuenta filas con los nueve deciles finitos;
        # no debe pisar el `n` de las metricas puntuales.
        prob["n_prob"] = prob.pop("n")
        row.update(prob)
        rows.append(row)

        if not rivals_done:
            for name, column in RIVALS.items():
                metrics = regression_metrics(merged[column], merged["TD_obs"])
                rows.append(
                    {
                        "split": split,
                        "method": name,
                        "cells": cells,
                        **metrics,
                        "skill_vs_clim": 1.0 - metrics["rmse"] / clim if clim else np.nan,
                    }
                )
            rivals_done = True

        if by_zone:
            for zone, group in merged.groupby("zone_id"):
                zone_clim = regression_metrics(group["pred_clim"], group["TD_obs"])["rmse"]
                columns = [("timesfm:" + key, "pred")]
                if not zone_rivals_done:
                    columns.extend(RIVALS.items())
                for name, column in columns:
                    metrics = regression_metrics(group[column], group["TD_obs"])
                    zone_rows.append(
                        {
                            "split": split,
                            "zone_id": int(zone),
                            "method": name,
                            "cells": group["ID"].nunique(),
                            **metrics,
                            "skill_vs_clim": 1.0 - metrics["rmse"] / zone_clim if zone_clim else np.nan,
                        }
                    )
            zone_rivals_done = True

    leaderboard = pd.DataFrame(rows).sort_values("rmse").reset_index(drop=True)
    zones = pd.DataFrame(zone_rows)
    return leaderboard, zones


def error_growth_curves(
    predictions_dir: Path,
    split: str,
    *,
    variant: str,
    backtest_root: Path = DEFAULT_BACKTEST_ROOT,
) -> pd.DataFrame:
    """RMSE acumulado dia a dia dentro del bloque oculto, por metodo.

    Una sola cifra de RMSE esconde si el error crece con la distancia al ultimo
    dato observado. El metodo de Palacios es autorregresivo dentro del bloque y
    deberia degradarse; TimesFM predice todo el horizonte de una vez y no
    realimenta, asi que su curva deberia ser plana salvo por la estacionalidad.
    """
    reference = load_reference(split, backtest_root=backtest_root)
    pred = pd.read_parquet(predictions_dir / f"{split}__{variant}.parquet", columns=["ID", "FECHA", "pred"])
    pred["FECHA"] = pd.to_datetime(pred["FECHA"])
    merged = reference.merge(pred, on=["ID", "FECHA"], how="inner", validate="one_to_one")
    merged = merged.rename(columns={"pred": "pred_timesfm"})
    cells = int(merged["ID"].nunique())

    origin = merged["FECHA"].min()
    merged["dia"] = (merged["FECHA"] - origin).dt.days + 1

    rows = []
    columns = {**RIVALS, "timesfm": "pred_timesfm"}
    for name, column in columns.items():
        error = (merged[column].to_numpy(dtype=float) - merged["TD_obs"].to_numpy(dtype=float)) ** 2
        # Igual que regression_metrics: los valores no finitos no cuentan ni en la suma ni en n.
        finite = np.isfinite(error)
        daily = pd.DataFrame({"dia": merged["dia"].to_numpy()[finite], "se": error[finite]})
        daily = daily.groupby("dia", as_index=False).agg(se=("se", "sum"), n=("se", "size"))
        daily = daily.sort_values("dia")
        cumulative = np.sqrt(daily["se"].cumsum() / daily["n"].cumsum())
        rows.append(pd.DataFrame({"split": split, "method": name, "dia": daily["dia"],
                                  "rmse_acumulado": cumulative}))
    curve = pd.concat(rows, ignore_index=True)
    curve.attrs["cells"] = cells
    return curve


def selection_bias(leaderboard: pd.DataFrame) -> dict[str, float]:
    """Cuanto de la ventaja de la mejor variante puede ser fruto de haber probado varias.

    Se reporta la dispersion entre variantes y la distancia de la mejor a la
    mediana. Es el analogo directo de la comprobacion que hizo Palacios sobre su
    propia reseleccion (PAPER_PLAN.md:275), y la unica forma honesta de citar una
    ganadora elegida sobre el mismo bloque que se reporta.
    """
    variants = leaderboard[leaderboard["method"].str.startswith("timesfm:")].sort_values("rmse")
    if variants.empty:
        return {}
    rmse = variants["rmse"].to_numpy(dtype=float)
    skill = variants["skill_vs_clim"].to_numpy(dtype=float)
    out = {
        "n_variantes": int(rmse.size),
        "rmse_mejor": float(rmse[0]),
        "rmse_mediana": float(np.nanmedian(rmse)),
        "rmse_peor": float(np.nanmax(rmse)),
        "dispersion_rmse": float(np.nanmedian(rmse) - rmse[0]),
        "skill_mejor": float(np.nanmax(skill)),
        "skill_mediana": float(np.nanmedian(skill)),
        "dispersion_skill": float(np.nanmax(skill) - np.nanmedian(skill)),
    }
    if rmse.size > 1:
        # La brecha con la segunda es la medida que importa para el sesgo de
        # seleccion: la dispersion total mezcla variantes de diseno distinto
        # (con y sin covariable, contextos de 2 y de 32 anios) y refleja esas
        # decisiones, no el ruido de haber elegido entre configuraciones
        # equivalentes. Si la brecha con la segunda es del orden de la
        # incertidumbre del propio RMSE, la ganadora es intercambiable.
        out["rmse_segunda"] = float(rmse[1])
        out["brecha_primera_segunda"] = float(rmse[1] - rmse[0])
        out["segunda_variante"] = str(variants["method"].iloc[1]).split(":", 1)[1]
    return out


def _write_growth_curve(args: argparse.Namespace, panel_id: str, panel_file: str | None) -> None:
    curve = error_growth_curves(
        args.predictions_dir, args.growth_curve,
        variant=args.growth_variant, backtest_root=args.backtest_root,
    )
    args.growth_curve_out.parent.mkdir(parents=True, exist_ok=True)
    curve.to_csv(args.growth_curve_out, index=False)
    logger.info("escrito %s", args.growth_curve_out)
    cells = int(curve.attrs["cells"])
    for method in (*RIVALS, f"timesfm:{args.growth_variant}"):
        prov.record_metric_provenance(
            build_row_provenance(
                method, split=args.growth_curve, cells=cells, bead_id=args.bead_id,
                panel_id=panel_id, panel_file=panel_file,
                output_files=(str(args.growth_curve_out),),
                notes=backtest_notes(
                    args.backtest_root, cells=cells,
                    extra="; ".join(filter(None, ["curva de error acumulado", args.notes])),
                ),
                manifest_ref=args.manifest_ref or manifest_ref_for(args.backtest_root),
            )
        )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions-dir", type=Path, required=True)
    parser.add_argument("--splits", default="ll4")
    parser.add_argument("--backtest-root", type=Path, default=DEFAULT_BACKTEST_ROOT)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--by-zone", action="store_true")
    parser.add_argument("--growth-curve", default=None, metavar="SPLIT",
                        help="ademas escribe el RMSE acumulado dia a dia de ese split "
                             "(requiere --growth-variant y --growth-curve-out)")
    parser.add_argument("--growth-variant", default=None,
                        help="variante de TimesFM cuya curva se calcula")
    parser.add_argument("--growth-curve-out", type=Path, default=None,
                        help="CSV de salida de la curva de error acumulado")
    parser.add_argument("--notes", default=None,
                        help="texto libre que se agrega a las notas de proveniencia, p. ej. "
                             "la relacion entre --panel-file y las celdas puntuadas")
    parser.add_argument("--manifest-ref", default=None,
                        help="documento que gobierna la corrida; por defecto, el addendum si "
                             "--backtest-root es la raiz limpia y el manifiesto original si no")
    parser.add_argument("--bead-id", default="tdew-214",
                        help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    parser.add_argument("--panel-id", default=None,
                        help="nombre del panel de celdas puntuado; por defecto, el nombre de --predictions-dir")
    parser.add_argument("--panel-file", default=None,
                        help="CSV del panel de celdas puntuado, si se conoce")
    args = parser.parse_args(argv)
    if args.growth_curve and not (args.growth_variant and args.growth_curve_out):
        parser.error("--growth-curve requiere --growth-variant y --growth-curve-out")
    # Rutas absolutas: el registro y los sidecars no deben depender del directorio de trabajo.
    args.out_dir = args.out_dir.resolve()
    if args.growth_curve_out:
        args.growth_curve_out = args.growth_curve_out.resolve()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    boards, zones = [], []
    sesgo_paths: dict[str, Path] = {}
    for split in [s.strip() for s in args.splits.split(",") if s.strip()]:
        board, zone = score_split(
            args.predictions_dir, split, backtest_root=args.backtest_root, by_zone=args.by_zone
        )
        boards.append(board)
        if not zone.empty:
            zones.append(zone)
        print(f"\n=== {split} ===")
        columns = ["method", "cells", "n", "rmse", "mae", "bias", "r", "skill_vs_clim"]
        print(board[columns].to_string(index=False, float_format=lambda v: f"{v:.4f}"))
        bias = selection_bias(board)
        # Con una sola variante no hubo seleccion: la dispersion seria 0 por construccion.
        if bias and bias["n_variantes"] > 1:
            shown = {
                key: (round(value, 4) if isinstance(value, (int, float)) else value)
                for key, value in bias.items()
            }
            print("\nsesgo de seleccion:", shown)
            sesgo_paths[split] = args.out_dir / f"sesgo_seleccion_{split}.csv"
            pd.DataFrame([{"split": split, **bias}]).to_csv(sesgo_paths[split], index=False)

    combined = pd.concat(boards, ignore_index=True)
    leaderboard_path = args.out_dir / "leaderboard.csv"
    combined.to_csv(leaderboard_path, index=False)
    metrics_by_zone_path = None
    if zones:
        metrics_by_zone_path = args.out_dir / "metrics_by_zone.csv"
        pd.concat(zones, ignore_index=True).to_csv(metrics_by_zone_path, index=False)

    panel_id = args.panel_id or args.predictions_dir.name
    panel_file = args.panel_file or str(args.predictions_dir)
    for _, row in combined[["split", "method", "cells"]].iterrows():
        # leaderboard.csv siempre; metrics_by_zone.csv y sesgo_seleccion_<split>.csv
        # solo si esta corrida los produjo (desglose de la MISMA comparacion, no
        # una fuente nueva -- por eso comparten el registro en vez de uno aparte).
        output_files = [str(leaderboard_path)]
        if metrics_by_zone_path is not None:
            output_files.append(str(metrics_by_zone_path))
        if row["split"] in sesgo_paths:
            output_files.append(str(sesgo_paths[row["split"]]))
        prov.record_metric_provenance(
            build_row_provenance(
                row["method"],
                split=row["split"],
                cells=int(row["cells"]),
                bead_id=args.bead_id,
                panel_id=panel_id,
                panel_file=panel_file,
                output_files=tuple(output_files),
                notes=backtest_notes(args.backtest_root, cells=int(row["cells"]), extra=args.notes),
                manifest_ref=args.manifest_ref or manifest_ref_for(args.backtest_root),
            )
        )
    if args.growth_curve:
        _write_growth_curve(args, panel_id, panel_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
