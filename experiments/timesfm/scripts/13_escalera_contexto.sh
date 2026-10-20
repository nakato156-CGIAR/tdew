#!/usr/bin/env bash
# A1 (tdew-03g): escalera de anio de inicio del contexto para tmin_anom_full, panel de cribado.
# Separa longitud del contexto y regimen PISCO (antes de 2000 sin LST de MODIS). La climatologia
# de las anomalias queda FIJA en 1981-train_end (--clim-start-year 1981) para todos los inicios:
# solo cambia la longitud del contexto. Control (solo ll4b): inicio 2002 con climatologia
# 2002-2008, que es el comportamiento de tmin_anom_med, para medir cuanto de la brecha med-full
# es climatologia. fp32 estricto, mismas opciones que 02_cribado.sh. Lanzar dentro de tmux;
# usa la GPU (~5 min por corrida). Evaluacion: python -m experiments.amenazas.escalera_contexto.
source "$(dirname "$0")/env.sh"
run() {  # split inicio_contexto inicio_climatologia
  echo "--- tmin_anom_full $1 ctx$2 clim$3 $(date +%T) ---"
  $PY -m experiments.timesfm.run --variants tmin_anom_full --split "$1" --no-tf32 \
    --context-start-year "$2" --clim-start-year "$3" \
    --ids-file "$PANELS/cribado_estratificado.csv" --out-dir "$WORK/preds_cribado_escalera" \
    --batch-size 16 --cells-per-batch 256 --bead-id tdew-03g
}
for SPLIT in ${SPLITS:-ll4b ll4}; do
  for START in ${STARTS:-1981 1986 1991 1996 2002}; do
    run "$SPLIT" "$START" 1981
  done
  if [ "$SPLIT" = ll4b ]; then run ll4b 2002 2002; fi
done
