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

from tdew_estimation.provenance import load_registry, resolve_recorded_path

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
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/leaderboard.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/metrics_by_zone.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/metrics_all.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/effect_sizes_all.csv",
    REPORTS_ROOT / "timesfm_benchmark/curva_error_nacional_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/tiers_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/tiers_texto_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/sesgo_mensual_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/sesgo_mes_tier_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/leaderboard.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/metrics_by_zone.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/sesgo_seleccion_ll4.csv",
    REPORTS_ROOT / "timesfm_benchmark/curva_error_cribado_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/tiers_cribado_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/sesgo_mensual_cribado_limpio.csv",
    REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/sesgo_mes_tier_cribado_limpio.csv",
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
        "version con fuga, generada antes de que existiera `evaluate --growth-curve`; "
        "se conserva sin cambios (PLAN_1 §4). La version limpia si esta instrumentada",
    REPORTS_ROOT / "timesfm_benchmark/curva_error_nacional.csv":
        "version con fuga, generada antes de que existiera `evaluate --growth-curve`; "
        "se conserva sin cambios (PLAN_1 §4). La version limpia si esta instrumentada",
    REPORTS_ROOT / "timesfm_benchmark/panels/cribado_estratificado.csv":
        "panel de celdas (lista de IDs), no una metrica -- se referencia como panel_file en otros registros",
    REPORTS_ROOT / "timesfm_benchmark/panels/nacional_17041.csv":
        "panel de celdas (lista de IDs), no una metrica -- se referencia como panel_file en otros registros",
    REPORTS_ROOT / "timesfm_benchmark/panels/nacional_17027.csv":
        "panel de celdas (lista de IDs), no una metrica -- se referencia como panel_file en otros registros",
    REPORTS_ROOT / "paper/scripts/validation_by_support.csv":
        "reports/paper/scripts/validation_by_support.py lee desde una ruta externa "
        "(RES/BACKTEST_ROOT fuera del repo) y no pasa por tdew_estimation.provenance -- "
        "salida ad hoc del backtest para el paper, no un run instrumentado",
    REPORTS_ROOT / "paper/scripts/zone_table_supplement.csv":
        "conteo de celdas por zona de clasificacion climatica (analogo a un panel de "
        "celdas), no una metrica de precision de pronostico",
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
        if any(resolve_recorded_path(f, repo_root=REPO_ROOT) == target
               for f in row.get("output_files", []))
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


def test_clean_panel_cell_counts_match_the_panel_file():
    """Los registros del panel limpio declaran tantas celdas como IDs tiene
    panels/nacional_17027.csv (17.027), no un numero copiado del plan."""
    import pandas as pd

    panel = pd.read_csv(REPORTS_ROOT / "timesfm_benchmark/panels/nacional_17027.csv")
    assert panel["ID"].is_unique and len(panel) == 17027
    rows = [r for r in _registry_rows() if r.get("panel_id") == "nacional_17027_limpio"]
    assert rows, "no hay registros con panel_id nacional_17027_limpio"
    for row in rows:
        assert row["panel_cell_count"] == len(panel), row["run_id"]
        assert row["manifest_ref"] == "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"


def test_clean_effect_sizes_cover_the_whole_clean_panel():
    """PLAN_1 criterio 5: 12 filas (3 splits x 4 baselines) sobre las 17.027 celdas,
    y el p minimo alcanzable con 5.000 permutaciones es 1/5001."""
    import pandas as pd

    es = pd.read_csv(REPORTS_ROOT / "timesfm_benchmark/nacional_limpio/effect_sizes_all.csv")
    assert len(es) == 12
    assert set(es["n_cells"]) == {17027}
    assert set(es["split"]) == {"ll1", "ll2", "ll4"}
    assert es["perm_p_value"].min() == pytest.approx(1 / 5001, rel=1e-3)


def test_clean_effect_sizes_reconstruct_from_metrics_all():
    """PLAN_1 criterio 6: delta_rmse_C(timesfm_vs_climatology) = RMSE(clima) - RMSE(TimesFM)
    con las cifras de metrics_all.csv, y timesfm_vs_tuned en ll4 es ~ +0,074."""
    import pandas as pd

    base = REPORTS_ROOT / "timesfm_benchmark/nacional_limpio"
    es, ma = pd.read_csv(base / "effect_sizes_all.csv"), pd.read_csv(base / "metrics_all.csv")
    for split in ("ll1", "ll2", "ll4"):
        rmse = ma[ma["split"] == split].set_index("method")["rmse"]
        row = es[(es["split"] == split) & (es["comparison"] == "timesfm_vs_climatology")].iloc[0]
        assert row["delta_rmse_C"] == pytest.approx(
            rmse["climatology"] - rmse["timesfm"], abs=1e-6)
    tuned = es[(es["split"] == "ll4") & (es["comparison"] == "timesfm_vs_tuned")].iloc[0]
    assert tuned["delta_rmse_C"] == pytest.approx(0.074, abs=5e-4)


def test_every_row_documenting_the_clean_outputs_carries_the_clean_panel_id():
    """PLAN_1 criterio 12: ninguna fila que documente un archivo *_limpio puede llevar
    otro panel_id ni el manifiesto original."""
    base = REPORTS_ROOT / "timesfm_benchmark"
    clean_files = [p for p in TRACKED_METRIC_FILES if "limpio" in str(p.relative_to(REPORTS_ROOT))]
    assert clean_files
    for path in clean_files:
        rows = _rows_documenting(path)
        assert rows, path
        for row in rows:
            expected = ("cribado_1092_limpio" if "cribado" in path.name or "cribado_limpio" in str(path)
                        else "nacional_17027_limpio")
            assert row["panel_id"] == expected, (path.name, row["panel_id"])
            assert row["manifest_ref"] == "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"


def test_clean_screening_covers_the_1092_common_cells():
    """PLAN_1 criterio 7: el cribado limpio puntua las 1.092 celdas comunes al
    panel de cribado (1.106) y al run limpio; las 14 restantes se descartan."""
    import pandas as pd

    base = REPORTS_ROOT / "timesfm_benchmark"
    board = pd.read_csv(base / "cribado_limpio/leaderboard.csv")
    assert set(board["cells"]) == {1092}
    assert set(board["split"]) == {"ll4"}
    screening = set(pd.read_csv(base / "panels/cribado_estratificado.csv")["ID"])
    clean = set(pd.read_csv(base / "panels/nacional_17027.csv")["ID"])
    assert len(screening & clean) == 1092
    variants = board[board["method"].str.startswith("timesfm:")]
    assert len(variants) == 9, "nueve variantes tras la enmienda del 2026-09-25"
    by_zone = pd.read_csv(base / "cribado_limpio/metrics_by_zone.csv")
    assert by_zone["zone_id"].nunique() == 33
    for method in ("tuned", "climatology", "timesfm:tmin_anom_full"):
        assert by_zone[by_zone["method"] == method]["cells"].sum() == 1092, method
    assert not by_zone.duplicated(["split", "zone_id", "method"]).any()


def test_clean_screening_provenance_counts_match_the_leaderboard():
    import pandas as pd

    path = REPORTS_ROOT / "timesfm_benchmark/cribado_limpio/leaderboard.csv"
    rows = _rows_documenting(path)
    assert rows
    assert {r["panel_cell_count"] for r in rows} == {1092}
    assert {r["panel_id"] for r in rows} == {"cribado_1092_limpio"}
    assert len(rows) == len(pd.read_csv(path))
