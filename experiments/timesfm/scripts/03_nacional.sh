#!/usr/bin/env bash
# Fase 2: la ganadora sobre el panel nacional en ll1, ll2 y ll4, contra el run limpio de Palacios.
# Inferencia medida en la RTX A2000: 1 h 04 min (ll1), 1 h 30 min (ll2) y 1 h 26 min (ll4) sobre 17.041 celdas.
source "$(dirname "$0")/env.sh"
for SPLIT in ll4 ll2 ll1; do
  $PY -m experiments.timesfm.run --variants "$BEST" --split "$SPLIT" \
    --ids-file "$PANELS/nacional_17041.csv" \
    --out-dir "$WORK/preds_nacional" --batch-size 16 --cells-per-batch 512
done

# Fusion con las predicciones de Palacios (copia en $WORK; $RES no se escribe).
$PY -m experiments.timesfm.merge_predictions \
  --predictions-dir "$WORK/preds_nacional" --variant "$BEST" --splits ll1,ll2,ll4 \
  --backtest-root "$RES/tuning/backtest_clean" --out-root "$WORK/backtest_clean_timesfm" \
  --panel-id nacional_17027_limpio --bead-id tdew-214.12

# Escalera de metodos por split, desglose por zona y curva de error acumulado.
$PY -m experiments.timesfm.evaluate \
  --predictions-dir "$WORK/preds_nacional" --splits ll1,ll2,ll4 --by-zone \
  --backtest-root "$RES/tuning/backtest_clean" --out-dir "$OUT/nacional_limpio" \
  --panel-id nacional_17027_limpio --panel-file "$PANELS/nacional_17027.csv" \
  --bead-id tdew-214.12 --growth-curve ll4 --growth-variant "$BEST" \
  --growth-curve-out "$OUT/curva_error_nacional_limpio.csv"

# Tamanos de efecto (bootstrap por celda, permutacion por cambio de signo) y curva de horizonte.
$PY -m HPC_code_tunning.effect_sizes \
  --backtest-root "$WORK/backtest_clean_timesfm" --splits ll1,ll2,ll4 \
  --focal timesfm --lead-time-methods timesfm,tuned --timesfm-variant "$BEST" \
  --n-boot 1000 --n-perm 5000 --seed 0 --panel-id nacional_17027_limpio \
  --panel-file "$PANELS/nacional_17027.csv" --manifest-ref "$ADD" --bead-id tdew-214.12 \
  --notes "backtest_root deriva de tuning/backtest_clean (merge con TimesFM $BEST)"
$PY -m experiments.timesfm.publish \
  --src "$WORK/backtest_clean_timesfm/metrics_all.csv" "$WORK/backtest_clean_timesfm/effect_sizes_all.csv" \
  --dst-dir "$OUT/nacional_limpio"
cp -f "$WORK/backtest_clean_timesfm/lead_time_curve.png" "$OUT/nacional_limpio/"
for s in ll1 ll2 ll4; do for f in "$WORK/backtest_clean_timesfm/$s"/*.png; do
  cp -f "$f" "$OUT/nacional_limpio/${s}_$(basename "$f")"; done; done

# Soporte observacional (tiers) y sesgo mensual; aborta si tuned no reproduce el paper.
$PY -m experiments.timesfm.by_tier_month \
  --merged-root "$WORK/backtest_clean_timesfm" --splits ll1,ll2,ll4 \
  --backtest-root "$RES/tuning/backtest_clean" --out-dir "$OUT/nacional_limpio" \
  --panel-id nacional_17027_limpio --panel-file "$PANELS/nacional_17027.csv"

# Divergencia KL de la distribucion de Td (ll4).
$PY -m experiments.timesfm.kl \
  --palacios "$RES/tuning/backtest_clean/ll4/predictions.parquet" \
  --timesfm "$WORK/preds_nacional/ll4__${BEST}.parquet" --out-dir "$OUT/kl_limpio"
