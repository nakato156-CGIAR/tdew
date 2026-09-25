"""Falla si un archivo de métricas publicado bajo reports/ no tiene un
registro de proveniencia en reports/metric_provenance.jsonl, o si ese
registro tiene algún campo requerido vacío.

Alcance: solo los archivos que produce un script ya instrumentado con
tdew_estimation.provenance (ver bead tdew-z39). Todo lo demás bajo reports/
está en EXCLUDED_FILES con la razón documentada -- no es "confiamos en que
está bien", es "todavía no lo instrumentamos" o "no es una métrica".
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tdew_estimation.provenance import load_registry

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_ROOT = REPO_ROOT / "reports"
REGISTRY_PATH = REPORTS_ROOT / "metric_provenance.jsonl"

# reports/results/ son benchmarks de escalamiento HPC (tiempo/GPU), no
# métricas de pronóstico de Td -- fuera de alcance por decisión del plan
# original (docs de este bead), no por omisión.
EXCLUDED_DIRS = (REPORTS_ROOT / "results",)

# Archivos de metricas/leaderboard que un lector citaria, uno por script
# instrumentado. Se mantiene explicito (no glob) para que un archivo nuevo
# bajo reports/ que NADIE registro en este set tambien sea detectado por
# test_every_csv_or_parquet_under_reports_is_accounted_for de abajo.
TRACKED_METRIC_FILES = (
    REPORTS_ROOT / "week1_baselines/leaderboard.csv",
    REPORTS_ROOT / "week1_tcn_ablation/ablation_summary.csv",
    REPORTS_ROOT / "week1_tcn_ablation/ablation_history.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado/leaderboard.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado/metrics_by_zone.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado/sesgo_seleccion_ll4.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional/leaderboard.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional/metrics_by_zone.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional/sesgo_seleccion_ll4.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional/metrics_all.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional/effect_sizes_all.csv",
    REPORTS_ROOT / "timesfm_benchmark/departamental/metrics.csv",
    REPORTS_ROOT / "timesfm_benchmark/departamental/metrics_macro.csv",
    REPORTS_ROOT / "timesfm_benchmark/departamental/curva_acumulada.csv",
    REPORTS_ROOT / "timesfm_benchmark/departamental/predicciones_largo.parquet",
    REPORTS_ROOT / "timesfm_benchmark/escala/leaderboard.csv",
    REPORTS_ROOT / "week1_tcn_audit/ablation.csv",
    REPORTS_ROOT / "week1_tcn_audit/ablation_gpu.csv",
    REPORTS_ROOT / "week1_tcn_audit/batches.csv",
    REPORTS_ROOT / "week1_tcn_audit/compare_predictors.csv",
    REPORTS_ROOT / "week1_tcn_audit/gradient_share.csv",
    REPORTS_ROOT / "week1_tcn_audit/memorization.csv",
    REPORTS_ROOT / "week1_tcn_audit/probes.csv",
    REPORTS_ROOT / "week1_tcn_audit/sensitivity_best.pt.csv",
    REPORTS_ROOT / "week1_tcn_audit/sensitivity_last.pt.csv",
    REPORTS_ROOT / "week1_tcn_audit/train_val_gap.csv",
)

# CSV/parquet bajo reports/ que existen hoy pero cuyo script de origen no
# está instrumentado todavía (bead de seguimiento tdew-z39.7), o que no son
# una métrica de precisión en sí (paneles, listas de IDs, benchmarks de
# velocidad/VRAM). Cada entrada dice por qué -- nunca "no lo revisamos".
EXCLUDED_FILES = {
    REPORTS_ROOT / "timesfm_benchmark/coste_throughput.csv":
        "experiments.timesfm.throughput mide celdas/s y VRAM, no precision -- "
        "autoregressive/target_type/climatology_used no aplican a un benchmark de hardware",
    REPORTS_ROOT / "timesfm_benchmark/curva_error_cribado.csv":
        "error_growth_curves() existe en evaluate.py pero ningun main() la invoca; "
        "se genera fuera de cualquier CLI instrumentado",
    REPORTS_ROOT / "timesfm_benchmark/curva_error_nacional.csv":
        "error_growth_curves() existe en evaluate.py pero ningun main() la invoca; "
        "se genera fuera de cualquier CLI instrumentado",
    REPORTS_ROOT / "timesfm_benchmark/panels/cribado_estratificado.csv":
        "panel de celdas (lista de IDs), no una metrica -- se referencia como panel_file en otros registros",
    REPORTS_ROOT / "timesfm_benchmark/panels/nacional_17041.csv":
        "panel de celdas (lista de IDs), no una metrica -- se referencia como panel_file en otros registros",
}

REQUIRED_FIELDS = (
    "run_id", "generated_at", "git_commit", "bead_id", "manifest_ref",
    "model_family", "model_id", "variant_label",
    "target_type", "panel_id", "panel_cell_count", "output_files",
)


def _discover_reports_files() -> list[Path]:
    found = []
    for pattern in ("*.csv", "*.parquet"):
        for path in REPORTS_ROOT.rglob(pattern):
            if any(excluded in path.resolve().parents for excluded in EXCLUDED_DIRS):
                continue
            found.append(path.resolve())
    return sorted(set(found))


def _registry_rows() -> list[dict]:
    return load_registry(REGISTRY_PATH)


def _rows_documenting(path: Path) -> list[dict]:
    target = path.resolve()
    return [
        row for row in _registry_rows()
        if any(Path(f).resolve() == target for f in row.get("output_files", []))
    ]


@pytest.mark.parametrize(
    "path", TRACKED_METRIC_FILES, ids=lambda p: str(p.relative_to(REPORTS_ROOT)),
)
def test_tracked_metric_file_has_at_least_one_provenance_record(path):
    assert path.exists(), f"{path} no existe -- actualiza TRACKED_METRIC_FILES"
    rows = _rows_documenting(path)
    assert rows, f"{path.relative_to(REPO_ROOT)} no tiene fila en {REGISTRY_PATH.name}"


@pytest.mark.parametrize(
    "path", TRACKED_METRIC_FILES, ids=lambda p: str(p.relative_to(REPORTS_ROOT)),
)
def test_tracked_metric_file_records_have_every_required_field(path):
    rows = _rows_documenting(path)
    for row in rows:
        for field in REQUIRED_FIELDS:
            assert row.get(field) not in (None, "", []), (
                f"{path.relative_to(REPO_ROOT)}: fila {row.get('run_id')} sin {field!r}"
            )
        # trained=False exige training_period=None; trained=True lo exige
        # presente -- ambos casos son "correcto", nunca están mal etiquetados.
        if row["trained"]:
            assert row.get("training_period"), (
                f"{path.relative_to(REPO_ROOT)}: fila {row.get('run_id')} trained=True sin training_period"
            )
        else:
            assert row.get("training_period") is None
        # El registro debe documentar sobre QUE periodo se evaluo -- no todos
        # los scripts tienen un "test" separado de "validation" (p. ej. una
        # corrida de entrenamiento que solo valida nunca toca el test set).
        assert row.get("validation_period") or row.get("test_period"), (
            f"{path.relative_to(REPO_ROOT)}: fila {row.get('run_id')} sin validation_period ni test_period"
        )


def test_every_csv_or_parquet_under_reports_is_accounted_for():
    """Ningun archivo nuevo bajo reports/ puede colarse sin trazabilidad ni
    exclusion documentada: o esta en TRACKED_METRIC_FILES (y tiene proveniencia)
    o esta en EXCLUDED_FILES (con una razon), nunca en ningun otro estado."""
    tracked = {p.resolve() for p in TRACKED_METRIC_FILES}
    excluded = {p.resolve() for p in EXCLUDED_FILES}
    unaccounted = [p for p in _discover_reports_files() if p not in tracked and p not in excluded]
    assert not unaccounted, (
        "archivos bajo reports/ sin proveniencia ni exclusion documentada:\n"
        + "\n".join(str(p.relative_to(REPO_ROOT)) for p in unaccounted)
    )


def test_departamental_panel_cell_counts_match_the_actual_predictions_parquet():
    """panel_cell_count no puede ser un numero copiado de un documento: tiene
    que coincidir con las celdas que el propio archivo que describe realmente
    tiene. Una auditoria encontro exactamente este error (8192 copiado de
    TRACEABILITY.md contra 2048 reales en predicciones_largo.parquet) antes de
    que este test existiera; ahora lo detecta."""
    import pandas as pd

    parquet_path = REPORTS_ROOT / "timesfm_benchmark/departamental/predicciones_largo.parquet"
    long = pd.read_parquet(parquet_path, columns=["ID", "model", "seed", "fold"])
    actual_cells = long.groupby(["model", "seed", "fold"])["ID"].nunique()

    for row in _rows_documenting(parquet_path):
        seed = row["seeds"][0] if row["seeds"] else None
        key = (row["model_id"], seed, row["split_id"])
        assert key in actual_cells.index, (
            f"proveniencia para {key} no corresponde a ningun (model, seed, fold) real "
            f"en {parquet_path.relative_to(REPO_ROOT)}"
        )
        assert row["panel_cell_count"] == int(actual_cells[key]), (
            f"{key}: panel_cell_count={row['panel_cell_count']} pero el parquet tiene "
            f"{int(actual_cells[key])} celdas reales"
        )
