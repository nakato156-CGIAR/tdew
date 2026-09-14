#!/bin/bash
# Leak-free validation, exactly as HPC_code_tunning/README.md Step 2 prescribes:
# recipes selected on TRAIN YEARS ONLY (not just coefficients), extended h-grid,
# for all three lead times so the lead-time curve is on the same footing.
set -e
WT=/home/ppalacios/Documents/tdew_estimation/tdew_estimation/.claude/worktrees/tdew-gap-fill-resume-7391e5
PY=/home/ppalacios/Documents/tdew_estimation/.venv/bin/python
RES=/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning
ROOT=$RES/tuning/backtest_clean
cd "$WT"; export PYTHONPATH="$WT"
mkdir -p "$ROOT"

echo "=== CLEAN BACKTEST START $(date) ==="
for SPLIT in ll1 ll2 ll4; do
  echo "--- [$SPLIT] 1/2 select recipes on TRAIN YEARS ONLY $(date +%T) ---"
  $PY -u -m HPC_code_tunning.select_backtest --base "$RES" --split "$SPLIT" \
      --n-buckets 16 --per-zone-n 200 --h-grid 7,11,15,21,31,45 \
      --out-root "$ROOT" --seed 0

  echo "--- [$SPLIT] 2/2 backtest with that train-only recipe $(date +%T) ---"
  $PY -u -m HPC_code_tunning.backtest --base "$RES" --splits "$SPLIT" \
      --n-buckets 64 --h-grid 7,11,15,21,31,45 \
      --manifest "$ROOT/manifest_trainonly_${SPLIT}.parquet" \
      --out-root "$ROOT" --seed 0
  echo "--- [$SPLIT] DONE $(date +%T) ---"
done

echo "--- effect sizes over all splits $(date +%T) ---"
$PY -u -m HPC_code_tunning.effect_sizes --backtest-root "$ROOT" \
    --splits ll1,ll2,ll4 --n-boot 1000 --n-perm 5000 --seed 0
echo "=== CLEAN BACKTEST DONE $(date) ==="
