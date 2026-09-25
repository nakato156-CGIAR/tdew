"""Common execution interface for continuous Td reconstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import mlflow

from tdew_estimation import experiment_tracking as et
from tdew_estimation import provenance as prov
from tdew_estimation.metrics import regression_metrics

from .baselines import apply_shrinkage, fit_baseline, fit_shrinkage_alpha
from .bucketed import load_canonical_input
from .data import AR_LAGS, add_td_targets, build_exogenous_features
from .protocol import Protocol, horizon_year, protocol_spec, require_protocol_access
from .rollout import direct_rollout, recursive_rollout
from .tcn_runner import run_tcn

MANIFEST_REF = "docs/protocol/reconstruction_manifest.yaml@2026-09-21"


def build_provenance(
    *,
    protocol: str,
    mode: str,
    model: str,
    variant_label: str,
    feature_set: str,
    seed: int,
    cells: int,
    bead_id: str,
    mlflow_run_id: str | None,
    panel_id: str,
    panel_file: str | None,
    output_files: tuple[str, ...],
    trained: bool = True,
) -> prov.MetricProvenance:
    """Cada corrida de run_baseline/run_tcn ajusta un modelo (ridge/histgb/tcn)
    y lo evalua sobre el bloque oculto de un protocolo congelado -- las fechas
    de entrenamiento y del bloque oculto vienen de la misma ProtocolSpec que
    tests/test_reconstruction_manifest_parity.py verifica contra el YAML.

    ``trained`` es False en la rama ``inference_only`` de
    ``tcn_runner.run_tcn`` (mismo protocolo que un checkpoint congelado: solo
    restaura pesos y predice, sin entrenar ni un paso -- ver
    ``predictions.attrs["trained"]``)."""
    spec = protocol_spec(protocol)
    return prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id=bead_id,
        manifest_ref=MANIFEST_REF,
        model_family="reconstruction",
        model_id=model,
        variant_label=variant_label,
        trained=trained,
        training_period=(
            (spec.train_start.date().isoformat(), spec.train_end.date().isoformat())
            if trained else None
        ),
        validation_period=None,
        test_period=(spec.hidden_start.date().isoformat(), spec.hidden_end.date().isoformat()),
        split_id=protocol,
        autoregressive=mode == "recursive",
        target_type="td_anomaly",
        climatology_used=True,
        climatology_role="target_anomaly_base",
        inputs=(feature_set,),
        panel_id=panel_id,
        panel_cell_count=cells,
        panel_file=panel_file,
        seeds=(seed,),
        mlflow_run_id=mlflow_run_id,
        output_files=output_files,
    )


def add_observed_ar_lags(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.sort_values(["ID", "date"]).copy()
    grouped = out.groupby("ID", sort=False)["TD_anom"]
    for lag in AR_LAGS:
        out[f"TD_anom_lag{lag}"] = grouped.shift(lag)
    return out


def run_baseline(
    canonical: pd.DataFrame,
    *,
    protocol: Protocol | str,
    mode: str,
    model: str,
    feature_set: str,
    seed: int,
    params: dict[str, Any] | None = None,
    unlock_ll4: bool = False,
) -> pd.DataFrame:
    spec = require_protocol_access(protocol, unlock_ll4=unlock_ll4)
    features = build_exogenous_features(canonical, spec)
    train, hidden = add_td_targets(features, spec)
    if mode == "recursive":
        train = add_observed_ar_lags(train)
        effective_feature_set = feature_set if feature_set.endswith("_ar") else f"{feature_set}_ar"
    elif mode == "direct":
        effective_feature_set = feature_set.removesuffix("_ar")
    else:
        raise ValueError("mode must be direct or recursive")
    fitted = fit_baseline(
        train, model=model, feature_set=effective_feature_set, params=params, seed=seed
    )
    if mode == "direct":
        anomaly = direct_rollout(hidden, fitted.predict_anomaly)
    else:
        anomaly = recursive_rollout(train, hidden, fitted.predict_anomaly)
    prediction = anomaly + hidden["TD_clim"].to_numpy(dtype=float)
    result = pd.DataFrame(
        {
            "ID": hidden["ID"].to_numpy(),
            "department": hidden["department"].to_numpy(),
            "date": hidden["date"].to_numpy(),
            "year_horizon": horizon_year(hidden["date"], spec).to_numpy(),
            "TD_obs": hidden["TD"].to_numpy(dtype=float),
            "TD_clim": hidden["TD_clim"].to_numpy(dtype=float),
            "TD_pred": prediction,
            "model": f"{model}_{effective_feature_set}_{mode}",
            "seed": seed,
            "fold": spec.name.value,
        }
    )
    return result


def select_hyperparameters(
    canonical: pd.DataFrame,
    *,
    model: str,
    mode: str,
    feature_set: str,
    seed: int,
) -> tuple[dict[str, Any], pd.DataFrame]:
    from .baselines import parameter_grid

    rows = []
    candidates: list[tuple[float, str, dict[str, float] | None]] = []
    for params in parameter_grid(model):
        fold_rmse = []
        fold_predictions = []
        for fold in (Protocol.DEV_A, Protocol.DEV_B):
            predictions = run_baseline(
                canonical, protocol=fold, mode=mode, model=model,
                feature_set=feature_set, seed=seed, params=params,
            )
            score = regression_metrics(predictions["TD_pred"], predictions["TD_obs"])["rmse"]
            rows.append({"params": json.dumps(params, sort_keys=True), "fold": fold.value, "rmse": score})
            fold_rmse.append(score)
            fold_predictions.append(predictions)
        params_json = json.dumps(params, sort_keys=True)
        raw_mean = float(np.mean(fold_rmse))
        rows.append({"params": params_json, "fold": "mean", "variant": "raw", "rmse": raw_mean})
        candidates.append((raw_mean, params_json, None))
        combined = pd.concat(fold_predictions, ignore_index=True)
        alphas = fit_shrinkage_alpha(combined)
        calibrated_scores = []
        for predictions in fold_predictions:
            calibrated = apply_shrinkage(predictions, alphas)
            calibrated_scores.append(regression_metrics(calibrated, predictions["TD_obs"])["rmse"])
        calibrated_mean = float(np.mean(calibrated_scores))
        rows.append(
            {
                "params": params_json,
                "fold": "mean",
                "variant": "calibrated",
                "rmse": calibrated_mean,
                "alphas": json.dumps(alphas, sort_keys=True),
            }
        )
        candidates.append((calibrated_mean, params_json, alphas))
    table = pd.DataFrame(rows)
    _, best_payload, best_alphas = min(candidates, key=lambda item: (item[0], item[1], item[2] is not None))
    table.attrs["best_alphas"] = best_alphas
    return json.loads(best_payload), table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reconstruccion continua de Td 2017-2020")
    parser.add_argument("--input", type=Path, required=True, help="Parquet canonico o raiz bucketed")
    parser.add_argument("--panel-ids", type=Path, help="CSV con columna ID para limitar celdas")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", choices=[p.value for p in Protocol], required=True)
    parser.add_argument("--mode", choices=["direct", "recursive"], required=True)
    parser.add_argument("--model", choices=["ridge", "histgb", "tcn"], required=True)
    parser.add_argument("--feature-set", default="exogenous_full")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-steps", type=int, default=20_000)
    parser.add_argument("--eval-every", type=int, default=1_000)
    parser.add_argument("--patience", type=int, default=5, help="Evaluaciones sin mejora antes de detener")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--context-length", type=int, default=7, choices=[3, 7, 14, 31, 60])
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--objective", choices=["mse", "huber"], default="mse")
    parser.add_argument("--device", choices=["cpu", "cuda"])
    parser.add_argument("--feature-cache", type=Path, help="Directorio donde cachear la tabla de features por protocolo y panel")
    parser.add_argument("--params-json", type=str)
    parser.add_argument("--tune", action="store_true", help="Seleccionar parametros con dev_a y dev_b")
    parser.add_argument("--unlock-ll4", action="store_true")
    parser.add_argument("--bead-id", default="tdew-x46.3",
                         help="bead que gobierna esta corrida, para tdew_estimation.provenance")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    panel_ids = pd.read_csv(args.panel_ids)["ID"] if args.panel_ids else None
    canonical = load_canonical_input(args.input, ids=panel_ids)
    params = json.loads(args.params_json) if args.params_json else None
    if args.tune and args.model == "tcn":
        raise ValueError("TCN screening is one run per protocol/context; --tune applies only to ridge/histgb")
    if args.tune:
        params, tuning = select_hyperparameters(
            canonical, model=args.model, mode=args.mode, feature_set=args.feature_set, seed=args.seed
        )
        tuning_path = args.output.with_name(f"{args.output.stem}_tuning.csv")
        tuning_path.parent.mkdir(parents=True, exist_ok=True)
        tuning.to_csv(tuning_path, index=False)
        best_alphas = tuning.attrs.get("best_alphas")
    else:
        best_alphas = None
    dataset_hash = _sha256(args.input)
    with et.start_run(
        "td-reconstruction",
        seed=args.seed,
        dataset_version=dataset_hash,
        site="ALL",
        params={
            "protocol": args.protocol,
            "mode": args.mode,
            "model": args.model,
            "feature_set": args.feature_set,
            "max_steps": args.max_steps,
            "eval_every": args.eval_every,
            "context_length": args.context_length,
            "batch_size": args.batch_size,
            "objective": args.objective,
            "model_params": json.dumps(params or {}, sort_keys=True),
        },
        experiment_name="tdew-reconstruction",
    ) as active_run:
        if args.model == "tcn":
            predictions = run_tcn(
                canonical,
                protocol=args.protocol,
                mode=args.mode,
                feature_set=args.feature_set,
                seed=args.seed,
                output_path=args.output,
                checkpoint=args.checkpoint,
                context_length=args.context_length,
                max_steps=args.max_steps,
                eval_every=args.eval_every,
                patience=args.patience,
                batch_size=args.batch_size,
                num_workers=args.num_workers,
                learning_rate=args.learning_rate,
                objective=args.objective,
                unlock_ll4=args.unlock_ll4,
                device=args.device,
                feature_cache=_feature_cache_path(args, dataset_hash, panel_ids),
            )
        else:
            predictions = run_baseline(
                canonical, protocol=args.protocol, mode=args.mode, model=args.model,
                feature_set=args.feature_set, seed=args.seed, params=params,
                unlock_ll4=args.unlock_ll4,
            )
            if best_alphas is not None:
                predictions["TD_pred"] = apply_shrinkage(predictions, best_alphas)
                predictions["model"] = predictions["model"] + "_calibrated"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        predictions.to_parquet(args.output, index=False)
        metadata = {
            "protocol": args.protocol, "mode": predictions.attrs.get("mode", args.mode), "model": args.model,
            "feature_set": predictions.attrs.get("feature_set", args.feature_set), "seed": args.seed, "params": params or {},
            "calibration_alpha": best_alphas, "rows": len(predictions),
            "checkpoint": predictions.attrs.get("checkpoint"),
            "device": predictions.attrs.get("device", args.device),
        }
        args.output.with_suffix(".json").write_text(json.dumps(metadata, indent=2, sort_keys=True))
        finite = predictions["TD_obs"].notna()
        if finite.any():
            score = regression_metrics(predictions.loc[finite, "TD_pred"], predictions.loc[finite, "TD_obs"])
            for name, value in score.items():
                if np.isfinite(value):
                    mlflow.log_metric(name, float(value))
            for department, group in predictions.loc[finite].groupby("department"):
                department_score = regression_metrics(group["TD_pred"], group["TD_obs"])
                for name, value in department_score.items():
                    if np.isfinite(value):
                        mlflow.log_metric(f"{department}_{name}", float(value))
        mlflow.set_tag("dataset_sha256", dataset_hash)
        mlflow.log_artifact(str(args.output))
        mlflow.log_artifact(str(args.output.with_suffix(".json")))
        checkpoint_artifact = predictions.attrs.get("checkpoint")
        if checkpoint_artifact and Path(checkpoint_artifact).is_file():
            mlflow.log_artifact(str(checkpoint_artifact), artifact_path="checkpoints")
        if args.input.is_dir() and (args.input / "manifest.json").exists():
            mlflow.log_artifact(str(args.input / "manifest.json"), artifact_path="dataset")

        panel_id = args.panel_ids.stem if args.panel_ids else "unrestricted"
        panel_file = str(args.panel_ids) if args.panel_ids else None
        prov.record_metric_provenance(
            build_provenance(
                protocol=args.protocol,
                mode=predictions.attrs.get("mode", args.mode),
                model=args.model,
                variant_label=str(predictions["model"].iloc[0]),
                feature_set=metadata["feature_set"],
                seed=args.seed,
                cells=int(predictions["ID"].nunique()),
                bead_id=args.bead_id,
                mlflow_run_id=active_run.info.run_id,
                panel_id=panel_id,
                panel_file=panel_file,
                trained=bool(predictions.attrs.get("trained", True)),
                output_files=(str(args.output), str(args.output.with_suffix(".json"))),
            )
        )
    return 0


def _feature_cache_path(args: argparse.Namespace, dataset_hash: str, panel_ids: pd.Series | None) -> Path | None:
    """Name the cache after everything the featured table depends on."""
    if args.feature_cache is None:
        return None
    digest = hashlib.sha256()
    digest.update(dataset_hash.encode())
    if panel_ids is not None:
        digest.update(",".join(str(int(value)) for value in sorted(panel_ids.unique())).encode())
    return Path(args.feature_cache) / f"{args.protocol}_{digest.hexdigest()[:16]}.parquet"


def _sha256(path: Path) -> str:
    if path.is_dir():
        manifest = path / "manifest.json"
        if manifest.exists():
            path = manifest
        else:
            digest = hashlib.sha256()
            for item in sorted(path.rglob("*.parquet")):
                stat = item.stat()
                digest.update(f"{item.relative_to(path)}:{stat.st_size}:{stat.st_mtime_ns}\n".encode())
            return digest.hexdigest()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
