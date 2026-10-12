#!/usr/bin/env bash
# Fase 4: prueba de escala. TimesFM sobre las 436.519 celdas de los cuatro departamentos
# (23 h 48 min a 5,09 celdas/s en la RTX A2000, 26,9 GB) y puntuacion sobre la submuestra de
# 61.113 celdas que alcanzo el rival tuned ($RES/tuning/backtest_escala_sub, recetas con fuga).
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.run --variants "$BEST" --split ll4 --ids-file "$WORK/panel_436k.csv" \
  --out-dir "$WORK/preds_escala" --batch-size 16 --cells-per-batch 512
$PY -m experiments.timesfm.escala \
  --timesfm "$WORK/preds_escala/ll4__${BEST}.parquet" \
  --backtest-predictions "$RES/tuning/backtest_escala_sub/ll4/predictions.parquet" \
  --ids-csv "$WORK/panel_escala_submuestra.csv" --out "$OUT/escala/leaderboard.csv" \
  --bead-id tdew-214.5
