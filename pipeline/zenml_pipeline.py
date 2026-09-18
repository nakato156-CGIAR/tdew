#!/usr/bin/env python3
"""
pipeline.zenml_pipeline

ZenML wrapper around the existing bronze -> silver -> gold medallion scripts
(pipeline/{bronze,silver,gold}.py). Thin orchestration only: each step calls
the module's existing ``run()`` function and passes along on-disk directory
paths as plain strings — the rasters/parquet tables themselves are not
rematerialized through ZenML's artifact store, they stay exactly where the
scripts already put them under ``Data/``.

It also wraps the tdew-ztn.3 derived-dataset scripts
(pipeline/{features,normalize,sequences,qc}.py): features/normalize/sequences
chain off gold's output, while qc runs as its own branch straight off silver
(it reads the raw daily tables directly, not the gold/features join).

Usage
-----
uv run python -m pipeline.zenml_pipeline
"""

from __future__ import annotations

from pathlib import Path

from zenml import pipeline, step

from pipeline import baseline_features, bronze, features, gold, normalize, qc, sequences, silver

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRONZE_DIR = str(REPO_ROOT / "Data" / "bronze")
DEFAULT_SILVER_DIR = str(REPO_ROOT / "Data" / "silver")
DEFAULT_GOLD_DIR = str(REPO_ROOT / "Data" / "gold")
DEFAULT_DEPARTMENTS = "lima,cusco,iquitos_loreto,tarapoto_san_martin"
DEFAULT_LENGTHS = ",".join(str(x) for x in sequences.DEFAULT_LENGTHS)
DEFAULT_QC_OUT = str(qc.DEFAULT_OUT)


@step
def bronze_step(bronze_dir: str, overwrite: bool = False) -> str:
    bronze.run(Path(bronze_dir), overwrite=overwrite)
    return bronze_dir


@step
def silver_step(
    bronze_dir: str,
    silver_dir: str,
    departments: str | None = DEFAULT_DEPARTMENTS,
    overwrite: bool = False,
) -> str:
    depts = [d.strip() for d in departments.split(",") if d.strip()] if departments else None
    silver.run(Path(bronze_dir), Path(silver_dir), overwrite=overwrite, departments=depts)
    return silver_dir


@step
def gold_step(
    silver_dir: str,
    gold_dir: str,
    num_buckets: int = gold.DEFAULT_NUM_BUCKETS,
    overwrite: bool = False,
) -> str:
    gold.run(Path(silver_dir), Path(gold_dir), num_buckets=num_buckets, overwrite=overwrite)
    return gold_dir


@step
def features_step(gold_dir: str, overwrite: bool = False) -> str:
    # features.run/normalize.run/sequences.run all take the shared top-level
    # gold_dir (e.g. "Data/gold") and resolve their own subdirectory under it
    # (model_input, model_features, model_features_norm) — this step, like
    # gold_step, returns that same shared gold_dir string (not the nested
    # output path) so it can be chained straight into normalize_step/
    # sequences_step without anyone needing to know the internal layout.
    features.run(Path(gold_dir), overwrite=overwrite)
    return gold_dir


@step
def normalize_step(gold_dir: str, overwrite: bool = False) -> str:
    normalize.run(Path(gold_dir), overwrite=overwrite)
    return gold_dir


@step
def sequences_step(gold_dir: str, lengths: str = DEFAULT_LENGTHS, overwrite: bool = False) -> str:
    parsed_lengths = tuple(int(x.strip()) for x in lengths.split(",") if x.strip())
    sequences.run(Path(gold_dir), lengths=parsed_lengths, overwrite=overwrite)
    return gold_dir


@step
def qc_step(silver_dir: str, out_path: str = DEFAULT_QC_OUT) -> str:
    out = qc.run(Path(silver_dir), Path(out_path))
    return str(out)


@step
def baseline_features_step(gold_dir: str, overwrite: bool = False) -> str:
    # tdew-x46 baselines: leak-safe lagged feature table, reuses
    # sequence_index/L=31 (already built by sequences_step) for eligibility.
    baseline_features.run(Path(gold_dir), overwrite=overwrite)
    return gold_dir


@pipeline
def medallion_pipeline(
    bronze_dir: str = DEFAULT_BRONZE_DIR,
    silver_dir: str = DEFAULT_SILVER_DIR,
    gold_dir: str = DEFAULT_GOLD_DIR,
    departments: str | None = DEFAULT_DEPARTMENTS,
    num_buckets: int = gold.DEFAULT_NUM_BUCKETS,
    lengths: str = DEFAULT_LENGTHS,
    qc_out: str = DEFAULT_QC_OUT,
    overwrite: bool = False,
) -> None:
    bronze_out = bronze_step(bronze_dir=bronze_dir, overwrite=overwrite)
    silver_out = silver_step(
        bronze_dir=bronze_out,
        silver_dir=silver_dir,
        departments=departments,
        overwrite=overwrite,
    )
    gold_out = gold_step(silver_dir=silver_out, gold_dir=gold_dir, num_buckets=num_buckets, overwrite=overwrite)
    features_out = features_step(gold_dir=gold_out, overwrite=overwrite)
    normalize_out = normalize_step(gold_dir=features_out, overwrite=overwrite)
    sequences_out = sequences_step(gold_dir=normalize_out, lengths=lengths, overwrite=overwrite)
    baseline_features_step(gold_dir=sequences_out, overwrite=overwrite)
    qc_step(silver_dir=silver_out, out_path=qc_out)


if __name__ == "__main__":
    medallion_pipeline()
