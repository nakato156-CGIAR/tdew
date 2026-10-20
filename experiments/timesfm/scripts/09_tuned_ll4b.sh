#!/usr/bin/env bash
# A1 (tdew-03g): `tuned` de Palacios en el bloque 2009-2012 (split ll4b), con seleccion de recetas
# solo con 1981-2008. Mismos parametros que reports/paper/scripts/backtest_clean_run.sh.
# Escribe en $WORK (nunca en $RES). Usa la GPU: no correrlo a la vez que TimesFM.
source "$(dirname "$0")/env.sh"
H=7,11,15,21,31,45
ROOT="$WORK/tuning_ll4b"
mkdir -p "$ROOT"
echo "--- [ll4b] 1/2 seleccion solo con anios de entrenamiento $(date +%T) ---"
$PY -u -m HPC_code_tunning.select_backtest --base "$RES" --split ll4b \
  --n-buckets 16 --per-zone-n 200 --h-grid "$H" --out-root "$ROOT" --seed 0
echo "--- [ll4b] 2/2 backtest con esa receta $(date +%T) ---"
$PY -u -m HPC_code_tunning.backtest --base "$RES" --splits ll4b \
  --n-buckets 64 --h-grid "$H" --manifest "$ROOT/manifest_trainonly_ll4b.parquet" \
  --out-root "$ROOT" --seed 0
echo "--- [ll4b] DONE $(date +%T) ---"
