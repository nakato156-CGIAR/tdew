#!/usr/bin/env bash
# A1 (tdew-03g): la misma escalera de inicio que 13_escalera_contexto.sh para los dos LLR, sobre
# las celdas del cribado. Climatologia FIJA con 1981-train_end; coeficientes y eleccion de h con
# [inicio, train_end] (h se valida con los ultimos 4 anios; rezagos sin Tmin previa al inicio).
# Solo CPU; puede correr junto al job de GPU.
source "$(dirname "$0")/env.sh"
for SPLIT in ${SPLITS:-ll4b ll4}; do
  for START in ${STARTS:-1981 1986 1991 1996 2002}; do
    echo "--- LLR $SPLIT train$START $(date +%T) ---"
    $PY -m experiments.llr_simple.llr --split "$SPLIT" --train-start "$START" \
      --ids-file "$PANELS/cribado_estratificado.csv" --out-dir "$WORK/llr_escalera"
    $PY -m experiments.llr_simple.llr_lags --split "$SPLIT" --train-start "$START" \
      --ids-file "$PANELS/cribado_estratificado.csv" --out-dir "$WORK/llr_escalera"
  done
done
