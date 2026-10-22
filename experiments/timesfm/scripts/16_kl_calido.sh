#!/usr/bin/env bash
# tdew-214.19: divergencia calida de Td (masa de menos en 20-24 C, de mas en 24,5-27 C), backtest
# limpio 2013-2016. Corta delta = P_pred(B) - P_obs(B), su share del deficit nacional, la
# contribucion a la KL y el sesgo condicional por zona SENAMHI, banda DEM, departamento, tier,
# anio, mes, anio-mes y zona x anio, para TimesFM, LLR (pred_tuned) y clim. Solo CPU, ~2 min.
# Salida reports/timesfm_benchmark/kl_calido/ (CSV + .provenance.json + figs/).
# Se lanza en tmux; el log queda en $WORK/kl_calido.log con EXIT= al final:
#   tmux new-session -d -s tdew-214.19-kl-calido 'bash experiments/timesfm/scripts/16_kl_calido.sh'
source "$(dirname "$0")/env.sh"
LOG="$WORK/kl_calido.log"
set +e
{
  echo "--- kl_calido $(date +%T) ---"
  $PY -m experiments.timesfm.kl_calido --n-boot "${N_BOOT:-200}" "$@"
} 2>&1 | tee "$LOG"
STATUS=${PIPESTATUS[0]}
echo "EXIT=$STATUS" >> "$LOG"
echo "--- fin $(date +%T) EXIT=$STATUS ---"
exit "$STATUS"
