#!/usr/bin/env bash
# E9: producto 2017-2020 sobre las 2.178.827 celdas del producto de Palacios (8.192 buckets).
# Inferencia: unos 6 dias en la RTX A2000 (4,3-5,0 celdas/s), 147 GB. Reanudable: relanzar la
# misma orden retoma desde el ultimo bucket con .done.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.real \
  --out-dir "$WORK/preds_real" --palacios-root "$RES/tuning/predictions_2017_2020" \
  --ids-from-palacios --batch-size 32 --min-free-gb 60 --bead-id tdew-214.13
$PY -m experiments.timesfm.real --verify-only --out-dir "$WORK/preds_real" \
  --palacios-root "$RES/tuning/predictions_2017_2020" --ids-from-palacios

# Acuerdo entre productos (no hay Td observada): unas 1,5 h. Cola calida Td > 35 C: unos 15 min.
$PY -m experiments.timesfm.real_compare --tfm-root "$WORK/preds_real" \
  --palacios-root "$RES/tuning/predictions_2017_2020" --with-climatology --bead-id tdew-214.13
$PY -m experiments.timesfm.real_tail --tfm-root "$WORK/preds_real" \
  --palacios-root "$RES/tuning/predictions_2017_2020" --bead-id tdew-214.13
