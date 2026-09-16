# Phase A — Temporal forward backtest (refit-only, variant a)

> **Status:** DONE 2026-07-16. **Owner:** Piero Palacios (CIP). **Assistant:** Claude Code.
> This is the paper's core validation evidence. Numbers below **need SME sign-off** (CIP policy);
> AI-assisted analysis is disclosed. See `PAPER_PLAN.md` §5/§12.

## What this tests

Does the per-SENAMHI-zone × doy **tuned** Td model beat the incumbent gap-fill baselines when
forecasting **held-out future years autoregressively** — i.e. under the exact conditions of the
real 2017–2020 gap (no observed Td inside the held-out block; the model's own predicted Td feeds
its next-day lags)?

- **Design.** Train on early years, forecast the held-out recent years, score vs observed v1.1 Td.
  Leave-last-N: **ll1** (1981–2015 → 2016), **ll2** (1981–2014 → 2015–16),
  **ll4** (1981–2012 → 2013–16, the headline — mimics the 4-year gap).
- **Honesty.** Climatology recomputed on **train years only** (no holdout leakage into the
  baseline or the model's anomaly anchor). Forecast fully autoregressive. Coefficients **refit on
  train years** (variant a).
- **Sample.** 64 whole buckets = **17,041 cells** scattered nationwide across **all 41 zones**
  (`id_bucket = ID % 8192` is a regular grid lattice, so each bucket samples the whole country).
- **Baselines (identical holdout).** climatology → Td=Tmin (FAO-56) → zone OLS Td~Tmin → tuned.

## Result — tuned wins decisively at every lead time

RMSE (°C), pooled over all held-out cell-days:

| split | climatology | Td=Tmin | zone OLS | **tuned** | tuned skill vs clim |
|---|---|---|---|---|---|
| ll1 (→2016)    | 1.680 | 3.621 | 2.379 | **1.262** | **0.249** |
| ll2 (→2015–16) | 1.667 | 3.676 | 2.370 | **1.274** | **0.235** |
| ll4 (→2013–16) | 1.535 | 3.551 | 2.329 | **1.219** | **0.206** |

Tuned model: **bias ≈ −0.05 °C**, **r ≈ 0.990** across splits.

### Effect sizes (paired per-cell; location-block bootstrap 95% CI; sign-flip permutation null, 5000)

**ll4 (headline):**

| tuned vs | ΔRMSE °C [95% CI] | skill [95% CI] | cells tuned wins | Cohen's d | perm p |
|---|---|---|---|---|---|
| climatology | +0.316 [0.314, 0.317] | 0.206 [0.204, 0.207] | 99.99% | 2.98 | 2e-4 |
| Td = Tmin   | +2.332 [2.308, 2.354] | 0.657 [0.655, 0.658] | 99.98% | 1.37 | 2e-4 |
| zone OLS    | +1.110 [1.091, 1.126] | 0.476 [0.472, 0.480] | 99.80% | 1.06 | 2e-4 |

ll1/ll2 are stronger still (e.g. ll1 vs climatology: Cohen's d = 4.2, wins 100.0% of cells). Full
tables: `$RES/tuning/backtest/effect_sizes_all.csv`, `metrics_all.csv`.

### Interpretation

- The tuned model reduces Td RMSE **~20% below climatology** (the gap-fill incumbent) even after 4
  years of pure autoregression, and is far ahead of Td=Tmin and a zone linear fit. Improvement is
  near-universal across cells (≈100%), with large effect sizes and a negligible permutation p-value.
- **Skill decays with lead** (0.249 → 0.235 → 0.206) — the expected error growth; the model does not
  collapse over a 4-year autoregressive horizon.
- This clears the plan's gate: **tuning is worth the full-grid re-select + re-train (Phase B0).**
- **December warm bias corrected.** The fixed-5 model had a **+1.45 °C** December warm bias
  (`accuracy_v11_v12.md`); in this backtest the tuned model's December bias is **+0.01 °C** (all months
  within ±0.44 °C, January the largest). The per-zone×doy seasonal recipe removes the seasonal bias.

### Caveats (state in the paper)

1. **Variant (a) selection optimism.** Coefficients are refit on train years, but the *recipe*
   (feature set + h per zone×doy) comes from the existing 1981–2016 manifest, which saw the holdout.
   **A5** (variant b: re-select on train years only) bounds this residual optimism.
   **A5 RESULT (2026-07-17): selection bias = 0.009 skill (~+0.013 °C RMSE, ~4% of the uplift) — negligible.**
   Honestly re-selected ll4 skill vs climatology = 0.197 (vs 0.206 refit-only); tuned still wins 99.99% of
   cells (Cohen's d 2.86, p≈2e-4). See `$RES/tuning/backtest_reselect/`.
2. **Old h-grid.** Recipes use `{7,11,15,21}`; the final config extends to `{7,11,15,21,31,45}` (§9).
   B0 re-runs selection with the extended grid before the production fill.
3. **Shared covariates.** Gridded Td and Tmin both derive from LST+DEM (PISCOeo_pm), so they share
   structure; station-level validation is out of scope (§4).

## Reproduce

```bash
cd /home/ppalacios/Documents/tdew_estimation
export PY=$PWD/.venv/bin/python
export RES=/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning
PYTHONPATH=$PWD $PY -m HPC_code_tunning.backtest --base "$RES" \
  --n-buckets 64 --splits ll1,ll2,ll4 --seed 0 --out-root "$RES/tuning/backtest"
PYTHONPATH=$PWD $PY -m HPC_code_tunning.effect_sizes \
  --backtest-root "$RES/tuning/backtest" --splits ll1,ll2,ll4 --n-boot 1000 --n-perm 5000
```

Plots per split: `rmse_ladder.png`, `delta_rmse_hist.png`, `bias_by_month.png`;
lead-time curve: `$RES/tuning/backtest/lead_time_curve.png`.
