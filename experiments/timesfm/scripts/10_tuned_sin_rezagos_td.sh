#!/usr/bin/env bash
# A2 (tdew-f6a): `tuned` de Palacios SIN rezagos de Td, en ll4b y ll4. Mismo patron que
# 09_tuned_ll4b.sh (seleccion solo con anios de entrenamiento + backtest con esa receta), pero
# el pool de candidatos excluye TD_anom_lag*: solo const, TMIN_anom y sus rezagos. Asi la
# entrada de `tuned` es equiparable a la de TimesFM tmin_anom_full sin Td observado del bloque
# (la recursion autorregresiva en Td desaparece porque ninguna receta tiene rezagos de Td).
# El mismo --candidates se pasa al backtest para que la matriz de entrenamiento no exija
# rezagos de Td finitos (feature_spec.build_feature_frame filtra por todas las columnas del pool).
# Escribe en $WORK (nunca en $RES). Usa la GPU: no correrlo a la vez que TimesFM.
source "$(dirname "$0")/env.sh"
H=7,11,15,21,31,45
CAND=const,TMIN_anom,TMIN_anom_lag1,TMIN_anom_lag2,TMIN_anom_lag7,TMIN_anom_lag30
for SPLIT in ${SPLITS:-ll4b ll4}; do
  ROOT="$WORK/tuning_sin_td_${SPLIT}"
  mkdir -p "$ROOT"
  echo "--- [$SPLIT] 1/2 seleccion sin rezagos de Td, solo anios de entrenamiento $(date +%T) ---"
  $PY -u -m HPC_code_tunning.select_backtest --base "$RES" --split "$SPLIT" \
    --n-buckets 16 --per-zone-n 200 --h-grid "$H" --candidates "$CAND" \
    --out-root "$ROOT" --seed 0
  echo "--- [$SPLIT] 2/2 backtest con esa receta $(date +%T) ---"
  $PY -u -m HPC_code_tunning.backtest --base "$RES" --splits "$SPLIT" \
    --n-buckets 64 --h-grid "$H" --candidates "$CAND" \
    --manifest "$ROOT/manifest_trainonly_${SPLIT}.parquet" \
    --out-root "$ROOT" --seed 0 --bead-id tdew-f6a
  echo "--- [$SPLIT] DONE $(date +%T) ---"
done
