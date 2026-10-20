#!/usr/bin/env bash
# A1 (tdew-03g): control de regimen MODIS. tmin_anom_med = tmin_anom_full con contexto desde 2002
# (antes de 2000 PISCO no usa LST de MODIS). Panel nacional, ll4b y ll4, fp32 estricto.
# Lanzar dentro de tmux (ver CLAUDE.md); usa la GPU. Comparacion: comparar_bloque.py <split>.
source "$(dirname "$0")/env.sh"
for SPLIT in ${SPLITS:-ll4b ll4}; do
  echo "--- tmin_anom_med $SPLIT $(date +%T) ---"
  $PY -m experiments.timesfm.run --variants tmin_anom_med --split "$SPLIT" --no-tf32 \
    --ids-file "$PANELS/nacional_17041.csv" --out-dir "$WORK/preds_nacional_med" \
    --batch-size 16 --cells-per-batch 512 --bead-id tdew-03g
done
