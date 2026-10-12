#!/usr/bin/env bash
# Fase 3: panel departamental de 2.048 celdas (512 por departamento), split ll4, con la TCN.
# Las predicciones de la TCN (semillas 0-2) y de Palacios sobre este panel son entradas externas:
#   $RECON/predictions/ll4_tcn_direct_seed{0,1,2}.parquet   (experiments/reconstruction, ver su README)
#   $RES/tuning/backtest_panel_dept/ll4/predictions.parquet  (HPC_code_tunning.backtest --ids-csv, recetas con fuga)
source "$(dirname "$0")/env.sh"
PANEL="$RECON/panels/ll4_reducido_512.csv"   # inferencia: 11 min en la RTX A2000
$PY -m experiments.timesfm.run --variants "$BEST" --split ll4 --ids-file "$PANEL" \
  --out-dir "$WORK/preds_departamental" --batch-size 16 --cells-per-batch 512
$PY -m experiments.timesfm.departamental \
  --reconstruction "$RECON"/predictions/ll4_tcn_direct_seed{0,1,2}.parquet \
  --timesfm "$WORK/preds_departamental/ll4__${BEST}.parquet" \
  --backtest-predictions "$RES/tuning/backtest_panel_dept/ll4/predictions.parquet" \
  --out-dir "$OUT/departamental"
