#!/usr/bin/env bash
# Fase 1: las nueve variantes zero-shot sobre las 1.106 celdas de cribado, split ll4.
# Inferencia medida en una RTX A2000 12 GB (lote 16): 49 min para las nueve variantes
# (de 1,6 a 18,5 celdas/s segun contexto y covariables). La ganadora es la de menor RMSE.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.run --variants all --split ll4 \
  --ids-file "$PANELS/cribado_estratificado.csv" \
  --out-dir "$WORK/preds_cribado" --batch-size 16 --cells-per-batch 256

# Puntuacion contra el run limpio de Palacios (1.092 celdas comunes) y curva de error acumulado.
$PY -m experiments.timesfm.evaluate \
  --predictions-dir "$WORK/preds_cribado" --splits ll4 --by-zone \
  --backtest-root "$RES/tuning/backtest_clean" --out-dir "$OUT/cribado_limpio" \
  --panel-id cribado_1092_limpio --panel-file "$PANELS/cribado_estratificado.csv" \
  --bead-id tdew-214.12 --growth-curve ll4 --growth-variant "$BEST" \
  --growth-curve-out "$OUT/curva_error_cribado_limpio.csv" \
  --notes "panel_file son las 1106 celdas del cribado; se puntuan las 1092 comunes con backtest_clean (14 descartadas)"
$PY -m experiments.timesfm.by_tier_month \
  --preds-dir "$WORK/preds_cribado" --splits ll4 \
  --backtest-root "$RES/tuning/backtest_clean" --out-dir "$OUT/cribado_limpio" \
  --panel-id cribado_1092_limpio --panel-file "$PANELS/cribado_estratificado.csv"

# Referencia historica con fuga (selection de recetas de Palacios con 1981-2016).
$PY -m experiments.timesfm.evaluate \
  --predictions-dir "$WORK/preds_cribado" --splits ll4 --by-zone \
  --backtest-root "$RES/tuning/backtest" --out-dir "$OUT/cribado"
