"""
tdew_estimation.experiment_tracking

Thin, shared MLflow wrapper so every training/evaluation script in this
project (baselines today; TCN/GRU/Transformer later) tags its runs the same
way, instead of every script calling ``mlflow`` directly with ad-hoc tags.

Backend: local SQLite (``mlflow.db`` at the repo root), per
``docs/experiment_infrastructure.md`` (MLflow 3.x deprecates the plain
``./mlruns`` file store).

Usage
-----
    from tdew_estimation import experiment_tracking as et
    import mlflow

    with et.start_run(
        "week1-baseline",
        seed=0,
        dataset_version="Data/gold/baseline_dataset",
        site="lima",
        params={"method": "dept_mlr"},
    ) as run:
        mlflow.log_metric("val_rmse", rmse)
"""

from __future__ import annotations

import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

import mlflow

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKING_URI = f"sqlite:///{REPO_ROOT / 'mlflow.db'}"


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


@contextmanager
def start_run(
    name: str,
    *,
    seed: Optional[int] = None,
    dataset_version: Optional[str] = None,
    site: Optional[str] = None,
    context_length: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None,
    tracking_uri: str = DEFAULT_TRACKING_URI,
    experiment_name: str = "tdew-week1",
) -> Iterator[Any]:
    """Open an MLflow run named ``name`` under ``experiment_name``, auto-tagging
    ``git_commit``/``seed``/``dataset_version``/``site``/``context_length`` and
    logging ``params`` as MLflow params. Yields the active ``mlflow.ActiveRun``;
    the caller logs metrics/artifacts as usual inside the ``with`` block."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=name) as run:
        tags = {"git_commit": _git_commit()}
        if seed is not None:
            tags["seed"] = str(seed)
        if dataset_version is not None:
            tags["dataset_version"] = str(dataset_version)
        if site is not None:
            tags["site"] = str(site)
        if context_length is not None:
            tags["context_length"] = str(context_length)
        mlflow.set_tags(tags)
        if params:
            mlflow.log_params(params)
        yield run
