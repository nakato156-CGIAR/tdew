"""Prediction schema, metrics, paired tests and final approval gate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

from tdew_estimation.metrics import regression_metrics

PREDICTION_COLUMNS = (
    "ID", "department", "date", "year_horizon", "TD_obs", "TD_clim",
    "TD_pred", "model", "seed", "fold",
)


def validate_prediction_frame(frame: pd.DataFrame) -> None:
    missing = sorted(set(PREDICTION_COLUMNS) - set(frame))
    if missing:
        raise ValueError(f"Prediction artifact is missing columns: {missing}")
    if frame.duplicated(["ID", "date", "model", "seed", "fold"]).any():
        raise ValueError("Prediction artifact has duplicate model observations")
    if not frame["year_horizon"].between(1, 4).all():
        raise ValueError("year_horizon must be in 1..4")


def evaluate_predictions(frame: pd.DataFrame) -> pd.DataFrame:
    validate_prediction_frame(frame)
    groupings: list[tuple[str, list[str]]] = [
        ("pooled", ["model", "seed", "fold"]),
        ("department", ["model", "seed", "fold", "department"]),
        ("month", ["model", "seed", "fold", "month"]),
        ("horizon_year", ["model", "seed", "fold", "year_horizon"]),
        ("department_horizon_year", ["model", "seed", "fold", "department", "year_horizon"]),
    ]
    work = frame.copy()
    work["date"] = pd.to_datetime(work["date"])
    work["month"] = work["date"].dt.month
    rows: list[dict[str, object]] = []
    for level, columns in groupings:
        for keys, group in work.groupby(columns, sort=True, dropna=False):
            keys = keys if isinstance(keys, tuple) else (keys,)
            row = dict(zip(columns, keys))
            metrics = regression_metrics(group["TD_pred"], group["TD_obs"])
            clim = regression_metrics(group["TD_clim"], group["TD_obs"])
            metrics["skill_vs_climatology"] = (
                1.0 - metrics["rmse"] / clim["rmse"] if clim["rmse"] and np.isfinite(clim["rmse"]) else np.nan
            )
            metrics["outside_qc_fraction"] = float((~group["TD_pred"].between(-25.0, 30.0)).mean())
            rows.append({"level": level, **row, **metrics})
    return pd.DataFrame(rows)


def macro_department_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    subset = metrics[metrics["level"] == "department"]
    values = ["rmse", "mae", "bias", "r", "skill_vs_climatology", "outside_qc_fraction"]
    return subset.groupby(["model", "seed", "fold"], as_index=False)[values].mean().assign(level="department_macro")


def cumulative_error_curve(frame: pd.DataFrame) -> pd.DataFrame:
    validate_prediction_frame(frame)
    work = frame.copy()
    work["date"] = pd.to_datetime(work["date"])
    work["sq_error"] = (work["TD_pred"] - work["TD_obs"]) ** 2
    daily = work.groupby(["model", "seed", "fold", "date"], as_index=False)["sq_error"].agg(["sum", "count"]).reset_index()
    daily = daily.sort_values(["model", "seed", "fold", "date"])
    grouped = daily.groupby(["model", "seed", "fold"], sort=False)
    daily["cumulative_rmse"] = np.sqrt(grouped["sum"].cumsum() / grouped["count"].cumsum())
    return daily[["model", "seed", "fold", "date", "cumulative_rmse"]]


@dataclass(frozen=True)
class PairedTestResult:
    rmse_difference: float
    ci_lower: float
    ci_upper: float
    sign_flip_pvalue: float
    winning_cell_fraction: float


def paired_cell_tests(
    candidate: pd.DataFrame,
    tuned: pd.DataFrame,
    *,
    n_bootstrap: int = 1000,
    n_permutations: int = 5000,
    seed: int = 0,
) -> PairedTestResult:
    keys = ["ID", "date"]
    joined = candidate[keys + ["TD_obs", "TD_pred"]].merge(
        tuned[keys + ["TD_pred"]], on=keys, suffixes=("_candidate", "_tuned"), validate="one_to_one"
    )
    if len(joined) != len(candidate) or len(joined) != len(tuned):
        raise ValueError("Candidate and tuned predictions do not cover identical cells/dates")
    obs = joined["TD_obs"].to_numpy(dtype=float)
    cand_sq = (joined["TD_pred_candidate"].to_numpy(dtype=float) - obs) ** 2
    tuned_sq = (joined["TD_pred_tuned"].to_numpy(dtype=float) - obs) ** 2
    point = float(np.sqrt(cand_sq.mean()) - np.sqrt(tuned_sq.mean()))
    per_cell = pd.DataFrame({"ID": joined["ID"], "cand_sq": cand_sq, "tuned_sq": tuned_sq}).groupby("ID").agg(
        cand_sq=("cand_sq", "mean"), tuned_sq=("tuned_sq", "mean")
    )
    if len(per_cell) < 2:
        raise ValueError("Paired cell tests require at least two cells")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(per_cell), size=(n_bootstrap, len(per_cell)))
    cand_values = per_cell["cand_sq"].to_numpy()
    tuned_values = per_cell["tuned_sq"].to_numpy()
    boot = np.sqrt(cand_values[indices].mean(axis=1)) - np.sqrt(tuned_values[indices].mean(axis=1))
    lower, upper = np.quantile(boot, [0.025, 0.975])

    delta = cand_values - tuned_values
    observed = abs(float(delta.mean()))
    exceed = 0
    remaining = n_permutations
    while remaining:
        chunk = min(remaining, 1000)
        signs = rng.choice((-1.0, 1.0), size=(chunk, len(delta)))
        exceed += int((np.abs((signs * delta).mean(axis=1)) >= observed).sum())
        remaining -= chunk
    pvalue = (exceed + 1.0) / (n_permutations + 1.0)
    return PairedTestResult(point, float(lower), float(upper), float(pvalue), float((delta < 0).mean()))


@dataclass(frozen=True)
class ApprovalResult:
    approved: bool
    failures: tuple[str, ...]
    paired: PairedTestResult


def approval_gate(
    candidate: pd.DataFrame,
    tuned: pd.DataFrame,
    *,
    required_departments: Sequence[str] = ("Lima", "Cusco", "Loreto", "San Martin"),
    required_seeds: Sequence[int] = (0, 1, 2),
    n_bootstrap: int = 1000,
    n_permutations: int = 5000,
    seed: int = 0,
) -> ApprovalResult:
    validate_prediction_frame(candidate)
    validate_prediction_frame(tuned)
    failures: list[str] = []
    if set(candidate["fold"].astype(str).unique()) != {"ll4"} or set(tuned["fold"].astype(str).unique()) != {"ll4"}:
        failures.append("approval may only be evaluated on ll4")
    if set(candidate["seed"].unique()) != set(required_seeds):
        failures.append("candidate does not contain exactly seeds 0, 1 and 2")
    candidate_mean = _ensemble_mean(candidate)
    tuned_mean = _ensemble_mean(tuned)
    paired = paired_cell_tests(
        candidate_mean, tuned_mean, n_bootstrap=n_bootstrap, n_permutations=n_permutations, seed=seed
    )
    if paired.ci_upper >= 0:
        failures.append("paired bootstrap RMSE-difference upper CI is not below zero")

    for department in required_departments:
        c = candidate_mean[candidate_mean["department"] == department]
        t = tuned_mean[tuned_mean["department"] == department]
        if c.empty or t.empty:
            failures.append(f"missing department: {department}")
            continue
        cm = regression_metrics(c["TD_pred"], c["TD_obs"])
        tm = regression_metrics(t["TD_pred"], t["TD_obs"])
        if cm["rmse"] >= tm["rmse"]:
            failures.append(f"RMSE does not improve tuned in {department}")
        if abs(cm["bias"]) > max(0.10, abs(tm["bias"])):
            failures.append(f"absolute bias exceeds threshold in {department}")
        for year in (1, 2, 3, 4):
            cy = c[c["year_horizon"] == year]
            if cy.empty:
                failures.append(f"missing horizon year {year} in {department}")
                continue
            model_rmse = regression_metrics(cy["TD_pred"], cy["TD_obs"])["rmse"]
            clim_rmse = regression_metrics(cy["TD_clim"], cy["TD_obs"])["rmse"]
            skill = 1.0 - model_rmse / clim_rmse if clim_rmse else np.nan
            if not np.isfinite(skill) or skill <= 0:
                failures.append(f"non-positive climatology skill in {department}, horizon year {year}")
    return ApprovalResult(not failures, tuple(failures), paired)


def prediction_columns_from_manifest(manifest: Mapping[str, object]) -> dict[str, str]:
    columns = manifest.get("prediction_columns")
    if not isinstance(columns, Mapping) or not columns:
        raise ValueError("Manifest must define a non-empty prediction_columns mapping")
    return {str(name): str(column) for name, column in columns.items()}


def registered_predictions_to_long(frame: pd.DataFrame, manifest: Mapping[str, object]) -> pd.DataFrame:
    """Convert manifest-registered wide prediction columns to canonical long form."""
    registered = prediction_columns_from_manifest(manifest)
    metadata = manifest.get("metadata_columns", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("metadata_columns must be a mapping")
    names = {
        "ID": str(metadata.get("ID", "ID")),
        "department": str(metadata.get("department", "department")),
        "date": str(metadata.get("date", "date")),
        "year_horizon": str(metadata.get("year_horizon", "year_horizon")),
        "TD_obs": str(metadata.get("TD_obs", "TD_obs")),
        "TD_clim": str(metadata.get("TD_clim", "TD_clim")),
        "seed": str(metadata.get("seed", "seed")),
        "fold": str(metadata.get("fold", "fold")),
    }
    missing = sorted((set(names.values()) | set(registered.values())) - set(frame))
    if missing:
        raise ValueError(f"Registered prediction source is missing columns: {missing}")
    pieces = []
    for model, prediction_column in registered.items():
        piece = frame[list(names.values()) + [prediction_column]].rename(
            columns={source: target for target, source in names.items()} | {prediction_column: "TD_pred"}
        )
        piece["model"] = model
        pieces.append(piece[list(PREDICTION_COLUMNS)])
    result = pd.concat(pieces, ignore_index=True)
    validate_prediction_frame(result)
    return result


def _ensemble_mean(frame: pd.DataFrame) -> pd.DataFrame:
    keys = ["ID", "department", "date", "year_horizon", "TD_obs", "TD_clim", "fold"]
    return frame.groupby(keys, as_index=False, dropna=False)["TD_pred"].mean()
