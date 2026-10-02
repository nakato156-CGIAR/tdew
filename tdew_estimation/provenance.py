"""
tdew_estimation.provenance

Single schema for "where does this published number come from": which
model/variant produced it, when, whether it was trained (and on what
period), whether it is autoregressive, whether the target is raw Td or an
anomaly, whether climatology is used, which inputs it consumes, and which
cell panel the metric is reported over.

Every script that writes a final metrics/leaderboard/predictions file under
``reports/`` should build one ``MetricProvenance`` record for that output and
call ``record_metric_provenance`` right after writing it. Records accumulate
in ``reports/metric_provenance.jsonl`` (one JSON object per line, append-only,
git-tracked) and are mirrored as a ``<output>.provenance.json`` sidecar next
to each file they document.

Usage
-----
    from tdew_estimation import provenance as prov

    record = prov.MetricProvenance(
        run_id=prov.new_run_id(),
        generated_at=prov.now_iso(),
        git_commit=prov.git_commit(),
        bead_id="tdew-214",
        manifest_ref="docs/protocol/timesfm_manifest.yaml@2026-09-22",
        model_family="foundation_model",
        model_id="timesfm:3.0",
        variant_label="tmin_td_full",
        trained=False,
        training_period=None,
        validation_period=None,
        test_period=("2013-01-01", "2016-12-31"),
        split_id="ll4",
        autoregressive=False,
        target_type="td_anomaly",
        climatology_used=True,
        climatology_role="input_covariate",
        inputs=("Tmin_anom",),
        panel_id="nacional_17041",
        panel_cell_count=17041,
        panel_file="reports/timesfm_benchmark/panels/nacional_17041.csv",
        seeds=(),
        mlflow_run_id=None,
        dataset_hash=None,
        output_files=("reports/timesfm_benchmark/nacional/metrics.csv",),
    )
    prov.record_metric_provenance(record)
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from tdew_estimation.experiment_tracking import REPO_ROOT, _git_commit

REPORTS_ROOT = REPO_ROOT / "reports"
DEFAULT_REGISTRY_PATH = REPORTS_ROOT / "metric_provenance.jsonl"

VALID_TARGET_TYPES = ("td_raw", "td_anomaly")


def new_run_id() -> str:
    return uuid.uuid4().hex


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def git_commit() -> str:
    return _git_commit()


@dataclass(frozen=True)
class MetricProvenance:
    run_id: str
    generated_at: str
    git_commit: str
    bead_id: str
    manifest_ref: str

    model_family: str
    model_id: str
    variant_label: str

    trained: bool
    training_period: Optional[Tuple[str, str]]
    validation_period: Optional[Tuple[str, str]]
    test_period: Optional[Tuple[str, str]]
    split_id: Optional[str]

    autoregressive: bool
    target_type: str
    climatology_used: bool
    climatology_role: Optional[str]
    inputs: Tuple[str, ...]

    panel_id: str
    panel_cell_count: int
    panel_file: Optional[str]

    output_files: Tuple[str, ...]

    seeds: Tuple[int, ...] = field(default_factory=tuple)
    mlflow_run_id: Optional[str] = None
    dataset_hash: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.target_type not in VALID_TARGET_TYPES:
            raise ValueError(
                f"target_type must be one of {VALID_TARGET_TYPES}, got {self.target_type!r}"
            )
        if not self.trained and self.training_period is not None:
            raise ValueError("training_period must be None when trained=False")
        if not self.climatology_used and self.climatology_role is not None:
            raise ValueError("climatology_role must be None when climatology_used=False")
        if self.panel_cell_count < 0:
            raise ValueError("panel_cell_count must be >= 0")
        if not self.output_files:
            raise ValueError("output_files must list at least one file this record documents")

    def to_json_dict(self) -> dict:
        return asdict(self)


def resolve_recorded_path(recorded: str, *, repo_root: Path = REPO_ROOT) -> Path:
    """Ruta de un ``output_file`` del registro, resuelta bajo el repo actual.

    Las rutas relativas se anclan en ``repo_root``. Una ruta absoluta que apunta a otro
    checkout o worktree (``.../reports/...``) se reancla bajo ``repo_root`` desde alguno
    de sus componentes ``reports``, pero solo si el archivo reanclado existe: asi una
    ruta externa al repo (p. ej. ``$WORK``) o un directorio de usuario llamado
    ``reports`` nunca se redirigen a un archivo equivocado.
    """
    path = Path(recorded)
    root = Path(repo_root).resolve()
    if not path.is_absolute():
        return (root / path).resolve()
    resolved = path.resolve()
    try:
        parts = resolved.relative_to(root).parts
    except ValueError:
        parts = resolved.parts
    for index, part in enumerate(parts):
        if part == "reports":
            candidate = (root / Path(*parts[index:])).resolve()
            if candidate == resolved or candidate.exists():
                return candidate
    return resolved


def record_metric_provenance(
    record: MetricProvenance,
    *,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    repo_root: Path = REPO_ROOT,
) -> None:
    """Append ``record`` to the JSONL registry and write a sidecar JSON next
    to each of its ``output_files``."""
    payload = record.to_json_dict()

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, sort_keys=True))
        fh.write("\n")

    for output_file in record.output_files:
        output_path = repo_root / output_file
        sidecar_path = output_path.with_name(output_path.name + ".provenance.json")
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        sidecar_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def load_registry(registry_path: Path = DEFAULT_REGISTRY_PATH) -> list[dict]:
    """Read every record from the JSONL registry, oldest first."""
    if not registry_path.exists():
        return []
    with registry_path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]
