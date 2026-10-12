# Entorno comun de los scripts del benchmark TimesFM. Se carga con `source`.
#
# TDEW_RES           almacen de produccion de Palacios (results_tuning), solo lectura.
# TDEW_TIMESFM_WORK  predicciones e intermedios de TimesFM (~180 GB con el producto 2017-2020).
# TDEW_RECONSTRUCTION_WORK  directorio del protocolo de reconstruccion (TCN, panel departamental).
#
# Los valores por defecto son los de la estacion de trabajo donde se corrio el benchmark.
# experiments/timesfm/paths.py lee las mismas variables.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO"
export TDEW_RES="${TDEW_RES:-/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning}"
export TDEW_TIMESFM_WORK="${TDEW_TIMESFM_WORK:-/home/cvelasquez/tdew_timesfm}"
export TDEW_RECONSTRUCTION_WORK="${TDEW_RECONSTRUCTION_WORK:-/home/cvelasquez/tdew_reconstruction}"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
RES="$TDEW_RES"
WORK="$TDEW_TIMESFM_WORK"
RECON="$TDEW_RECONSTRUCTION_WORK"
OUT=reports/timesfm_benchmark
PANELS="$OUT/panels"
ADD=docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml
PY="uv run python"
BEST=tmin_anom_full   # variante ganadora del cribado (ver 02_cribado.sh)
mkdir -p "$WORK"
