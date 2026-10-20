#!/usr/bin/env bash
# Robustez de A3 (tdew-077): el control negativo de 08_control_tmin_barajada.sh con otras dos
# formas de barajar la Tmin del horizonte, solo para la variante titular tmin_anom_full.
#   cell  semilla 0: Tmin de otra celda del panel (rompe el vinculo espacial, conserva el anio).
#   year  semillas 1 y 2: otros dos sorteos del barajado entre anios (08 usa la semilla 0).
# Panel de cribado, ll4, fp32 estricto. Lanzar dentro de tmux (ver CLAUDE.md); usa la GPU.
source "$(dirname "$0")/env.sh"
for SPEC in cell:0 year:1 year:2; do
  MODE="${SPEC%%:*}"; SEED="${SPEC##*:}"
  echo "--- barajado $MODE semilla $SEED $(date +%T) ---"
  $PY -m experiments.timesfm.run --variants tmin_anom_full --split ll4 --no-tf32 \
    --tmin-shuffle "$MODE" --shuffle-seed "$SEED" --ids-file "$PANELS/cribado_estratificado.csv" \
    --out-dir "$WORK/preds_cribado_shuffle_${MODE}_s${SEED}" --batch-size 16 --cells-per-batch 256 \
    --bead-id tdew-077
done
$PY -m experiments.timesfm.control_tmin_barajada_eval
