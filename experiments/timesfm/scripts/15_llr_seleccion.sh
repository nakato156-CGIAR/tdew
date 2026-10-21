#!/usr/bin/env bash
# tdew-03g: rival LLR mas fuerte. LLR simple y LLR con rezagos de Tmin con h y anio de inicio del
# ajuste elegidos juntos por validacion interna (ultimos 4 anios de entrenamiento; h en
# 7..180, train_start en 1981, 1986, 1991, 1996; climatologia 1981-train_end), panel nacional.
# Solo CPU. Salida $WORK/llr_simple/<split>__llr_simple_sel.* y __llr_tmin_lags_sel.*
# Evaluacion: python -m experiments.amenazas.desglose.
source "$(dirname "$0")/env.sh"
for SPLIT in ${SPLITS:-ll4b ll4}; do
  echo "--- LLR simple sel $SPLIT $(date +%T) ---"
  $PY -m experiments.llr_simple.llr --split "$SPLIT" --select-train-start \
    --ids-file "$PANELS/nacional_17027.csv" --out-dir "$WORK/llr_simple"
  echo "--- LLR rezagos sel $SPLIT $(date +%T) ---"
  $PY -m experiments.llr_simple.llr_lags --split "$SPLIT" --select-train-start \
    --workers "${WORKERS:-12}" --chunk "${CHUNK:-1000}" \
    --ids-file "$PANELS/nacional_17027.csv" --out-dir "$WORK/llr_simple"
done
echo "--- fin $(date +%T) ---"
