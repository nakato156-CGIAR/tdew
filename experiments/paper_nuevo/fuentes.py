"""Rutas de todas las entradas y salidas del paper nuevo, relativas a la raiz del repo."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PAPER = REPO / "reports" / "paper_nuevo"
RESULTADOS = PAPER / "resultados"
BENCH = REPO / "reports" / "timesfm_benchmark"

# --- Entradas (fuentes de verdad numericas) -------------------------------------------
A1_POR_METODO = RESULTADOS / "a1_por_metodo.csv"
A1_BRECHAS = RESULTADOS / "a1_brechas.csv"
A1_POR_ZONA = RESULTADOS / "a1_por_zona.csv"
A1_VICTORIAS = RESULTADOS / "a1_victorias_zona.csv"
A1_ESCALERA = RESULTADOS / "a1_escalera_contexto.csv"
A1_ESCALERA_BRECHAS = RESULTADOS / "a1_escalera_contexto_brechas.csv"
A3_BARAJADA = RESULTADOS / "a3_control_tmin_barajada.csv"
# A4: solo la version base (no `_h4b2`) y sin filas de ERA5.
A4_POR_PERIODO = RESULTADOS / "a4_por_periodo.csv"
A4_DELTA_BOOT = RESULTADOS / "a4_delta_rmse_bootstrap.csv"
A4_POR_ESTACION = RESULTADOS / "a4_por_estacion.csv"
A4_ESTACIONES = RESULTADOS / "a4_estaciones.csv"
COSTO_CSV = RESULTADOS / "costo.csv"
COSTO_MD = RESULTADOS / "costo.md"
LEADERBOARD = BENCH / "cribado_limpio" / "leaderboard.csv"
PANEL_NACIONAL = BENCH / "panels" / "nacional_17027.csv"
# R1 (inferencia) y R2 (descriptivo): analisis_inferencia.py y analisis_descriptivo.py.
R1_HORIZONTE = RESULTADOS / "r1_brecha_horizonte.csv"
R1_BOOT = RESULTADOS / "r1_bootstrap_espaciotemporal.csv"
R1_DM = RESULTADOS / "r1_diebold_mariano.csv"
R2_SKILL = RESULTADOS / "r2_skill.csv"
R2_EXTREMOS = RESULTADOS / "r2_extremos.csv"
R2_CALIBRACION = RESULTADOS / "r2_calibracion.csv"
R2_ALTITUD = RESULTADOS / "r2_estratos_altitud.csv"
R2_ZONA_DOM = RESULTADOS / "r2_sin_zona_dominante.csv"
R2_ENSO = RESULTADOS / "r2_enso.csv"
# R3 (costo de los LLR seleccionados): puede no existir todavia; cifras.py lo trata como opcional.
R3_COSTO = RESULTADOS / "r3_costo_llr_sel.csv"
# Notas de preentrenamiento: fuente de las constantes de `preentrenamiento.*`.
NOTAS_PRE = PAPER / "notas_preentrenamiento.md"
# Sidecar de proveniencia de a1_brechas.csv: de aqui salen replicas, semilla y bloques.
A1_BRECHAS_PROV = RESULTADOS / "a1_brechas.csv.provenance.json"

# --- Salidas ----------------------------------------------------------------------------
VARIABLES_YML = PAPER / "_variables.yml"
CIFRAS_DIR = PAPER / "cifras"
CIFRAS_CSV = CIFRAS_DIR / "cifras.csv"
CLAVES_MD = CIFRAS_DIR / "CLAVES.md"
TABLAS_DIR = PAPER / "tablas"


def rel(path: Path) -> str:
    """Ruta relativa al repo, con barras, para registrar en CSV y proveniencia."""
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def zone_table_path() -> Path | None:
    """`zone_table.parquet` bajo $RES (almacen de Palacios); None si no esta disponible."""
    from experiments.timesfm.paths import RES

    p = RES / "zone_table.parquet"
    return p if p.exists() else None
