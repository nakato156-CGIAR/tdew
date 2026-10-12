"""Command-line evaluator for manifest-registered prediction columns."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd
import yaml

from tdew_estimation import provenance as prov

from .evaluation import (
    approval_gate,
    cumulative_error_curve,
    evaluate_predictions,
    macro_department_metrics,
    registered_predictions_to_long,
)
from .protocol import protocol_spec

logger = logging.getLogger("reconstruction.evaluate")

MANIFEST_REF = "docs/protocol/reconstruction_manifest.yaml@2026-09-21"
# El metodo de Palacios (ver HPC_code_tunning/backtest.py::RIVAL_PROVENANCE) es
# autorregresivo. Los modelos que produce cli.py::run_baseline se nombran
# f"{model}_{feature_set}_{mode}" (mas "_calibrated" opcional), asi que ese
# sufijo SI dice si son autorregresivos. Pero este archivo lee `model` desde el
# manifiesto (registered_predictions_to_long usa la clave que el manifiesto le
# puso a cada columna, p. ej. "ridge_full" en
# docs/protocol/reconstruction_predictions.example.yaml), que puede ser un
# alias arbitrario sin relacion con esa convencion -- adivinar por el alias
# seria silenciosamente incorrecto. Por eso _is_autoregressive nunca adivina
# para un nombre que no reconoce: exige --autoregressive-overrides.
_KNOWN_AUTOREGRESSIVE = {"tuned"}


class UnknownAutoregressiveStatus(ValueError):
    pass


def _is_autoregressive(model: str, overrides: dict[str, bool]) -> bool:
    if model in overrides:
        return overrides[model]
    if model in _KNOWN_AUTOREGRESSIVE:
        return True
    stem = model.removesuffix("_calibrated")
    if stem.endswith("_direct"):
        return False
    if stem.endswith("_recursive") or stem.endswith("_ar"):
        return True
    raise UnknownAutoregressiveStatus(
        f"no se puede inferir si el modelo {model!r} es autorregresivo: no esta "
        "en _KNOWN_AUTOREGRESSIVE ni sigue la convencion _direct/_recursive de "
        "cli.py. Registralo con --autoregressive-overrides "
        f'\'{{"{model}": true_o_false}}\''
    )


def build_model_fold_provenance(
    model: str, fold: str, *, cells: int, bead_id: str, output_files: tuple[str, ...],
    autoregressive_overrides: dict[str, bool] | None = None,
    seed: int | None = None,
    panel_id: str | None = None,
) -> prov.MetricProvenance:
    """Una fila de metrics.parquet identifica (model, fold[, seed]); este archivo
    agrega predicciones ya generadas por experiments.reconstruction.cli, asi
    que no conoce el feature_set completo de cada modelo -- ese detalle vive
    en el sidecar JSON de la corrida de cli.py que lo produjo (ver ``notes``).

    ``seed`` distingue multiples corridas del mismo modelo en el mismo fold
    (p. ej. varias semillas de una TCN); se omite cuando solo hay una. ``panel_id``
    por defecto es ``fold`` (el uso original, un solo panel por reconstruccion),
    pero un agregador como experiments.timesfm.departamental.py que reusa este
    formato puede darle un nombre mas descriptivo."""
    spec = protocol_spec(fold)
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=MANIFEST_REF,
        model_family="reconstruction",
        model_id=model,
        variant_label=f"{model}_seed{seed}" if seed is not None else model,
        trained=True,
        training_period=(spec.train_start.date().isoformat(), spec.train_end.date().isoformat()),
        validation_period=None,
        test_period=(spec.hidden_start.date().isoformat(), spec.hidden_end.date().isoformat()),
        split_id=fold,
        autoregressive=_is_autoregressive(model, autoregressive_overrides or {}),
        target_type="td_anomaly",
        climatology_used=True,
        climatology_role="target_anomaly_base",
        inputs=(),
        panel_id=panel_id if panel_id is not None else fold,
        panel_cell_count=cells,
        panel_file=None,
        seeds=(seed,) if seed is not None else (),
        output_files=output_files,
        notes=(
            "feature_set completo en el sidecar <prediccion>.json de la corrida "
            "de experiments.reconstruction.cli que genero este modelo"
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluacion de reconstrucciones de Td")
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--candidate", type=str)
    parser.add_argument("--tuned", type=str, default="tuned")
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--permutations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--bead-id", default="tdew-x46.3",
                         help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    parser.add_argument(
        "--autoregressive-overrides", type=str, default=None,
        help='JSON {"model_alias": true_o_false} para nombres de modelo del manifiesto que '
             "_is_autoregressive no puede clasificar por convencion de nombre",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    autoregressive_overrides = (
        json.loads(args.autoregressive_overrides) if args.autoregressive_overrides else {}
    )
    manifest = yaml.safe_load(args.manifest.read_text())
    wide = pd.read_parquet(args.predictions)
    predictions = registered_predictions_to_long(wide, manifest)
    metrics = evaluate_predictions(predictions)
    macro = macro_department_metrics(metrics)
    curve = cumulative_error_curve(predictions)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = args.output_dir / "metrics.parquet"
    predictions.to_parquet(args.output_dir / "predictions.parquet", index=False)
    metrics.to_parquet(metrics_path, index=False)
    macro.to_parquet(args.output_dir / "metrics_department_macro.parquet", index=False)
    curve.to_parquet(args.output_dir / "cumulative_error.parquet", index=False)

    for (model, fold, seed), group in predictions.groupby(["model", "fold", "seed"]):
        try:
            record = build_model_fold_provenance(
                str(model), str(fold), cells=int(group["ID"].nunique()),
                bead_id=args.bead_id, output_files=(str(metrics_path),),
                autoregressive_overrides=autoregressive_overrides, seed=int(seed),
            )
        except UnknownAutoregressiveStatus as exc:
            logger.warning("[%s/%s/seed%s] se omite la proveniencia: %s", model, fold, seed, exc)
            continue
        prov.record_metric_provenance(record)

    if args.candidate:
        result = approval_gate(
            predictions[predictions["model"] == args.candidate],
            predictions[predictions["model"] == args.tuned],
            n_bootstrap=args.bootstrap,
            n_permutations=args.permutations,
            seed=args.seed,
        )
        payload = {
            "approved": result.approved,
            "failures": list(result.failures),
            "paired": result.paired.__dict__,
        }
        (args.output_dir / "approval.json").write_text(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
