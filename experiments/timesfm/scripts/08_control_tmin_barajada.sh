#!/usr/bin/env bash
# A3 (tdew-077): control negativo con la Tmin del horizonte barajada entre anios, panel de cribado, ll4.
# Lanzar dentro de tmux (ver CLAUDE.md). Fp32 estricto, como 02_cribado.sh.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.run --variants tmin_td_full,tmin_anom_full --split ll4 --no-tf32 \
  --tmin-shuffle year --shuffle-seed 0 --ids-file "$PANELS/cribado_estratificado.csv" \
  --out-dir "$WORK/preds_cribado_shuffle_year" --batch-size 16 --cells-per-batch 256 --bead-id tdew-077
# Escalera real frente a barajada sobre las 1.092 celdas comunes con el run limpio de Palacios.
$PY -m experiments.timesfm.control_tmin_barajada_eval
