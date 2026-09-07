# TDEW Gap-Fill — Scientific Plan & Progress Tracker

> **Purpose of this file.** Single source of truth for the effort to turn the per-zone×doy
> dew-point (Td) tuning pipeline into a **defensible scientific result for a paper**.
> A fresh Claude session should read this top-to-bottom, then continue from the first
> unchecked task in §7. Update the checkboxes and the "Progress log" (§12) as work lands.
>
> **Last updated:** 2026-07-16 · **Owner:** Piero Palacios (CIP) · **Assistant:** Claude Code

---

## 1. Scientific goal (what we are actually doing)

**Gap-fill the PISCO gridded daily dew-point temperature (Td) product forward in time.**

- PISCO **v1.1** provides both **Tmin and Td** for **1981–2016**.
- PISCO **v1.2** provides **Tmin for 1981–2020** but **no Td after 2016**.
- We learn the **Tmin → Td** mapping on the 1981–2016 overlap (Td from v1.1, Tmin from **v1.2**),
  then **predict Td for 2017–2020** at every grid cell using the continued v1.2 Tmin.

The model is per-(ID, doy) **weighted local linear regression on climate anomalies** (tricube DOY-window
kernel, half-window `h`), with per-**SENAMHI-zone × doy** feature/`h` selection (MultiLLR-style,
arXiv:1809.07394; LOYOCV cosine-skill objective). This is **NOT** a "predict at new locations" method —
it predicts **new years at the same grid cells**. That distinction drives the validation design (§5).

**Paper framing.** "A method to extend the PISCO gridded dew-point record (2017–2020) from the
continued minimum-temperature record, with per-climate-zone seasonal model selection." A perfectly
publishable outcome includes a *negative/neutral* result (per-zone×doy tuning does not beat a strong
climatology/Td≈Tmin baseline) **iff** the baselines and the temporal validation are rigorous.

---

## 2. Data inventory (verified 2026-07-16)

| item | path | coverage | notes |
|---|---|---|---|
| **Full national grid root** | `/media/ppalacios/Data1/henry_simcast_peru_full` (`$FULL`) | 2,818,404 IDs | dense 0..N-1 |
| Target Td (v1.1) | `$FULL/td/Outputs/td_daily_YYYY_MM.parquet` | 1981–2016 | the label |
| Grid coords | `$FULL/td/Outputs/grid_index.parquet` | — | ID→lon/lat |
| **v1.2 Tmin (gap-fill input)** | `/media/ppalacios/Data1/henry_simcast_peru/tmin_v12/Outputs` | **1981–2020** | 480 files incl. all of 2017–2020 |
| v1.1 Tmin | `/media/ppalacios/Data1/henry_simcast_peru/tmin_v11/Outputs` | 1981–2016 | 432 files; comparison only |
| Tuning results root | `$FULL/results_tuning` (`$RES`) | — | see §3 |
| Zone shapefile (zip) | `/home/ppalacios/Downloads/clasif_clima_peru.zip` | 41 zones | SENAMHI Thornthwaite; 15,700 polygon parts |

**Version-consistency decision (locked):** train and predict both use **v1.2 Tmin** (`--tmin-var tmin_v12`).
`reports/results/compare_v11_v12.md` shows the Tmin sensitivity differs by version (coeff mean 0.45 vs 0.37)
and switching versions injects ~0.3 °C bias, so a single Tmin source on both sides is required. State this
in the paper.

---

## 3. Method & pipeline status — what is already DONE

Full-grid pipeline has been run end-to-end on 1981–2016 (v1.2 Tmin → v1.1 Td). Artifacts under `$RES`:

- [x] **Prep** — `daily_climatology.parquet` (1.03 B rows), `bucketed_training_data/` (8192 buckets × 36 yr),
      `climatology_by_bucket/` (8192). OOM fixes committed (`86936a3` on `feat/hpc-code-tunning`).
- [x] **Zone table** — `$RES/zone_table.parquet` (2,818,404 rows, 41 zones, `unassigned=0`).
      (`zones.py` `sjoin_nearest` reprojects to EPSG:32718 — CRS-warning fix; verify it's committed.)
- [x] **Select** — `$RES/tuning/manifest.parquet` = **15,006 recipes** (41 zones × 366 doy):
      `[zone_id, zone_label, doy, h, feature_list, n_features, skill, skill_baseline, skill_uplift]`.
      Overview plot: `$RES/tuning/manifest_overview.png`.
      ⚠️ Used the **old h-grid `{7,11,15,21}`**. We are now extending it (§9) → this manifest and the coeffs
      below are **stale for the final config** and must be re-selected with the extended grid before the
      production fill (Phase B0, §7).
- [x] **Train** — `$RES/tuning/zoned_coeffs/id_bucket=XXXX/coeffs.parquet` (8192 buckets, **8.14 B** rows,
      74 GB). Schema `[ID, zone_id, doy, feature_name, coeff, r_squared_anom, h]`, no NaNs.
      (Same staleness caveat — trained from the old-h-grid manifest.)

**Manifest findings (need SME validation):** `h=21` chosen 56 % (window saturates at the max grid value →
consider extending the h-grid); selection prunes little (`n_features=11` kept 71 % → the fixed-5 baseline is
*under*-featured); **mean skill uplift only +0.013 (median +0.007), and 22.5 % of zone-days are equal or
worse** than the fixed-5/h=11 baseline. Existing fixed-model accuracy vs observed Td (from
`reports/results/accuracy_v11_v12.md`): **RMSE ≈ 1.13 °C**, strong **December warm bias +1.45 °C**.

> ⚠️ These skill numbers are **selection-optimistic** (LOYOCV was the objective the recipes were chosen to
> maximize) and **in-sample in time** (all 36 years used). They are NOT the paper's headline. §5 fixes this.

---

## 4. What makes it paper-grade (gaps to close)

1. **Ground truth — RESOLVED.** Target = the **gridded v1.1 Td** (that is the product being extended;
   validating against it is correct, not a compromise). Caveat to state: gridded Td and gridded Tmin both use
   **LST + DEM** covariates (regression-kriging; Td does *not* use Tmin directly — PISCOeo_pm paper,
   DOI 10.1038/s41597-022-01373-8), so they share some structure. Station-level validation is out of scope.
2. **Incumbent baselines — TODO.** Must beat **climatology** (the gap-fill incumbent), **Td = Tmin**
   (FAO-56 / Allen 1998), and a **zone OLS `Td~Tmin`**, not just the internal fixed-5/h=11 ablation.
3. **Validation is TEMPORAL, not spatial — TODO.** Forward backtest (train early years → predict held-out
   recent years), run **autoregressively** (see §5). Spatial blocking is a *secondary* robustness check only.
4. **Effect sizes over p-values — TODO.** ΔRMSE °C + block-bootstrap CIs, skill-vs-climatology, per-location
   distribution, Cohen's d as companion, and a **permutation/null test** (shuffle years, re-select) to show the
   +0.013 uplift is/ isn't distinguishable from selection noise.

---

## 5. Validation design (the paper's core evidence)

**Primary: forward temporal backtest, autoregressive.**

- **Holdout to mimic the real 4-year gap (CONFIRMED):** train on **1981–2012**, predict **2013–2016**
  (leave-last-4), score vs observed v1.1 Td. Also run leave-last-1 and leave-last-2 to show error growth
  with lead time.
- **Autoregressive requirement (critical).** The model uses `TD_anom_lag1/lag2` as predictors. In 2017–2020
  there is **no observed Td**, so those lags must come from the model's **own previous-day prediction**
  (sequential recursion — this is the P6 `forecast.py` gap, §6). The backtest **must also run autoregressively**
  (no observed-Td lags inside the held-out block) or it flatters the model vs what production can do.
- **Selection honesty.** For the winner's-curse fix in the *time* dimension, selection must not see the
  held-out years. Two variants to run and compare:
  - (a) **Refit-only** (fast): keep the existing manifest, refit coefficients on train-years, predict holdout.
  - (b) **Full re-select** (slower, honest): re-run `--stage select` on train-years only, then train+predict.
  Report both; the gap between them *is* the selection-bias estimate.
- **Cost control.** Do the backtest on a **stratified ID sample** (reuse cached `zone_table.parquet`;
  consider `--per-zone-n 500`), not the full 2.8 M grid. Full grid is only for the deliverable (§6).

**Baselines (all scored on the identical holdout):** climatology → Td=Tmin → zone OLS `Td~Tmin` →
fixed-5/h=11 → tuned.

**Metrics & effect sizes:** RMSE, MAE, bias, Pearson r (report these as primary, not cosine skill);
**skill score vs climatology** and vs Td=Tmin; **ΔRMSE °C with block-bootstrap CIs** (resample years/spatial
blocks to respect autocorrelation); **distribution of per-location improvements** + **fraction of cells where
tuned wins**; **Cohen's d** on paired per-location error diffs; **permutation/null test**.

**Secondary (robustness): spatial block CV** — partition Peru into contiguous tiles with a buffer dead-zone;
block *within* zone (recipes are zone-specific). Only needed to support the bootstrap CIs / show spatial
stability; not the primary holdout.

---

## 6. Deliverable — production gap-fill (2017–2020)

- [x] **P6: generalize the forecast to the tuned recipes.** DONE 2026-07-16 —
      `HPC_code_tunning/forecast_zoned.py` consumes the long/tidy `zoned_coeffs/` (variable per-zone×doy
      feature sets, TD lags to 30 d) + `climatology_by_bucket/` and runs the **autoregressive** recursion
      (predicted Td feeds next-day lags). Single-ID reference core + vectorised-across-IDs/loop-over-days
      bucket path (14× faster), kept in sync by `tests/test_forecast_zoned.py` (parity Δ<1e-9, independent
      hand-recursion, autoregressive-feed). No manifest needed at forecast time — the coeffs already encode
      each cell's retained features. Verified on real bucket-0 data (parity Δ=2.5e-14; day-1 math Δ=0).
- [x] **Prep 2017–2020 v1.2 Tmin inputs — this is a REGRID, not a copy.** DONE 2026-07-22 (§12): extracted to
      the full 2.8M grid (`nc_to_point_parquet --var tmin_v12 --no-peru-potato --year-range 2017,2020`, grid_index
      md5-identical to td) → `shard_future_tmin_by_bucket` into `$RES/future_tmin_by_bucket/` (8192×4). Seam
      Jan2017−Dec2016 = +0.028 °C (no grid mismatch). ⚠️ The raw v1.2 Tmin at
      `/media/ppalacios/Data1/henry_simcast_peru/tmin_v12/Outputs` is on a **302,449-ID grid** (max ID
      302448); the full product/coeffs use the **2,818,404-ID** grid. Feeding the raw file directly to the
      forecast mismatches the ID space (verified: produced a spurious −8.7 °C 2016→2017 seam jump; with the
      correctly-regridded full-grid Tmin the seam is −0.06 °C). The **regridded** full-grid v1.2 Tmin lives at
      `$FULL/tmin_v12/Outputs` but only covers **1981–2016** (432 files). B2 must run the same regrid/prep
      that built those, extended to 2017–2020, then bucketise into `future_tmin_root/id_bucket=XXXX/`
      (`[ID, FECHA, TMIN]`). Find the regrid step in `$FULL/extract_tmin.log` / the prep pipeline.
- [x] **Run the full-grid fill** for 2017–2020 using the coeffs trained on all 1981–2016 → the extended Td
      product. DONE 2026-07-22 — `HPC_code_tunning/fill_zoned.py` (new parallel CLI over
      `forecast_bucket_zoned_from_disk`), 8192 buckets / **3.18 B rows**, ~20 min at 14 workers.
      Saved under `$RES/tuning/predictions_2017_2020/id_bucket=*/pred.parquet`.
- [x] Sanity/QC the filled product (ranges, seasonal cycle continuity across the 2016→2017 seam, maps).
      DONE 2026-07-22 — 0 NaN; mean 19.39 °C; annual means 19.30–19.51 (no drift); seam Dec2016 obs 20.23 →
      Jan2017 pred 19.89 (continuous); no cold outliers. ⚠️ **Warm tail: max 41.2 °C, >35 °C = 0.13%
      (4.2 M cells), >32 °C = 1.0% — physically implausible dew points; needs an SME decision (document vs
      clip vs investigate offending zones/doys).** Maps not yet rendered.

---

## 7. Task checklist (work from the first unchecked item)

**Phase A — Validation harness (start here; no full re-run needed)**
- [x] A1. Build the **baseline ladder** module (climatology, Td=Tmin, zone OLS). DONE — in `backtest.py`
       (train-only climatology, streamed per-zone OLS sufficient stats).
- [x] A2. Build the **forward-backtest harness**: train-years vs holdout split, **autoregressive** holdout
       prediction on a sample. DONE — `HPC_code_tunning/backtest.py` (refit coeffs via GPU `train_bucket_zoned`
       → `forecast_zoned`; bucket-subset sample = nationwide lattice, all 41 zones; train-only clim per split).
- [x] A3. Build the **effect-size + bootstrap + null-test** reporting module. DONE —
       `HPC_code_tunning/effect_sizes.py` (ΔRMSE + location-block bootstrap CIs, per-cell win rate, Cohen's d,
       sign-flip permutation null, plots + lead-time curve).
- [x] A4. Run backtest **variant (a) refit-only** for tuned + all baselines. DONE 2026-07-16 — 64 buckets
       (17,041 cells, all zones). Results: `$RES/tuning/backtest/{ll1,ll2,ll4}/` + `reports/results/phase_a_backtest.md`.
       **Tuned decisively beats climatology / Td=Tmin / zone OLS** (see §12). ✅ clears the gate for B0.
- [x] A5. Run backtest **variant (b) full re-select** on train-years; compare to (a) → selection-bias estimate.
       DONE 2026-07-17 — `HPC_code_tunning/select_backtest.py` (train-only frames + train-only clim, no leak;
       16 buckets, per_zone_n=200). **ll4 skill: (a) 0.2057 → (b) 0.1969; selection bias = 0.0088 skill
       (~+0.013 °C RMSE, ~4% of uplift) — negligible.** Tuned still wins 99.99% of cells, d 2.86, p≈2e-4.
       Results: `$RES/tuning/backtest_reselect/`. **Method confirmed robust → B0 justified.**

**Phase B — Production deliverable**
- [x] B0. **Re-select + re-train the full grid with the extended h-grid** `{7,11,15,21,31,45}` (§9), replacing
       the stale manifest/coeffs (§3). DONE 2026-07-22 05:03 (see §12): manifest.parquet=15,006 recipes,
       zoned_coeffs=8192 buckets / 8.13 B rows, 0 NaN. h=45 modal (43.1%), uplift vs fixed-5 mean +0.0153
       (16.8% ≤0). **These are now the production manifest+coeffs for the 2017–2020 fill.** ~39.5 h total.
- [x] B1. Implement **P6 autoregressive forecast** for tuned recipes (§6). DONE 2026-07-16 —
       `HPC_code_tunning/forecast_zoned.py` + `tests/test_forecast_zoned.py` (3 passing). *(unblocks A2)*
- [x] B2. Prep 2017–2020 v1.2 Tmin future inputs — **REGRID** raw 302k-ID Tmin → full 2.8M grid (see §6).
       DONE 2026-07-22: `$RES/future_tmin_by_bucket/` (8192 buckets × 4 yr, `[ID,FECHA,TMIN]`), seam +0.028 °C.
- [x] B3. Full-grid fill 2017–2020; QC. DONE 2026-07-22 — `fill_zoned.py` parallel CLI; 8192 buckets/3.18 B
       rows; QC passed (seam continuous, no drift) with a warm-tail caveat (>35 °C 0.13%, max 41.2 °C → SME).

**Phase C — Write-up**
- [x] C1. Draft Quarto/Typst paper: method, data, temporal validation, effect sizes, filled product.
       **FIRST DRAFT DONE 2026-07-22** — `reports/paper/paper.qmd` (+ `references.bib`, `figures/`).
       Renders clean with Quarto 1.9.36 (all 7 figure refs, 3 citations, all cross-refs resolve).
       Open items marked inline **[SME]** / **[TODO]**: warm-tail disposition, seam regional pattern,
       station-level validation, bib author lists to verify, gitignored `reports/results/`, DOI deposit.
- [ ] C2. **AI-use disclosure** + **SME sign-off** (CIP org policy).

---

## 8. Environment & reproduction

- **Working dir:** `/home/ppalacios/Documents/tdew_estimation`
- **Code branch:** the `HPC_code_tunning/` source is on **`main`** (also `feat/hpc-code-tunning`). Confirm with
  `ls HPC_code_tunning/*.py`; if empty, `git checkout main` (or `feat/hpc-code-tunning`).
- **Python:** `.venv/bin/python` (set `export PY=$PWD/.venv/bin/python`).
- **GPU:** single RTX A2000 12 GB; `cupy` works. Selection/training are GPU (`cupy`).
- **Runs must be detached** so they survive the session: `setsid nohup $PY -m ... > log 2>&1 < /dev/null &`
  (plain `nohup` inside the Claude session gets killed on session exit — use `setsid`). Outputs go to the
  **persistent** `$RES`, never `/tmp`.
- **Standard env block:**
  ```bash
  cd /home/ppalacios/Documents/tdew_estimation
  export PY=$PWD/.venv/bin/python
  export FULL=/media/ppalacios/Data1/henry_simcast_peru_full
  export RES=$FULL/results_tuning
  export ZIP=/home/ppalacios/Downloads/clasif_clima_peru.zip
  export TMIN12=/media/ppalacios/Data1/henry_simcast_peru/tmin_v12/Outputs
  ```
- **Reference commands (already-run full pipeline, for reuse with different `--train-years`):**
  ```bash
  # select (per-zone×doy feature/h search); ~25 h on full sample, reuses zone_table if present
  $PY -m HPC_code_tunning.run_tuning_hpc --base "$RES" \
    --coords "$FULL/td/Outputs/grid_index.parquet" --zones-zip "$ZIP" \
    --tmin-var tmin_v12 --train-years "1981 2016" \
    --per-zone-n 2000 --id-chunk 96 --h-grid 7,11,15,21,31,45 --granularity doy --stage select
  #   ^ extended h-grid (§9). The already-run manifest used the old {7,11,15,21}; re-run to adopt.
  #   For the Phase-A backtest re-select, also pass --train-years "1981 2012".
  # train (fit coeffs on full grid); ~6 h, ~2.67 s/bucket, output tuning/zoned_coeffs/
  $PY -m HPC_code_tunning.run_tuning_hpc --base "$RES" \
    --coords "$FULL/td/Outputs/grid_index.parquet" --zones-zip "$ZIP" \
    --tmin-var tmin_v12 --train-years "1981 2016" \
    --id-chunk 96 --granularity doy --stage train
  ```
  Progress signal for train (no per-bucket logging): `find $RES/tuning/zoned_coeffs -name coeffs.parquet | wc -l` (/8192).

---

## 9. Decisions locked
- Target = gridded v1.1 Td (product being extended). Station-level validation out of scope.
- Tmin source = **v1.2 throughout** (train + predict).
- Validation = **temporal forward backtest, autoregressive**; spatial CV is secondary.
- Effect sizes (ΔRMSE °C, skill scores, bootstrap CIs, null test) lead; Cohen's d as companion.
- Gap to fill = **2017–2020** (4 years).
- **Backtest holdout = leave-last-4 (train 1981–2012, predict 2013–2016)** [confirmed 2026-07-16], plus
  leave-last-1 and -2 for the lead-time curve.
- **h-grid extended to `{7,11,15,21,31,45}`** [confirmed 2026-07-16] — the old run saturated at 21, so give
  selection room to find the plateau. NOTE the trade-off: a very wide DOY window pools nearly the whole year
  and loses seasonal specificity, so if selection keeps picking the max that is itself a finding (it wants
  annual pooling). Top values `31,45` are a starting choice — adjustable if 45 is still the modal pick.

## 10. Open questions / inputs needed from the user
- Where should the paper draft + figures live (`reports/paper/`?).

## 11. Org policy (CIP) — must hold throughout
Validate AI-generated content with SMEs; no confidential/personal data; no unpublished third-party IP;
be mindful of bias; **disclose AI use** in the paper.

## 12. Progress log
- 2026-07-16 — Plan created. Prep/select/train DONE on 1981–2016 (§3). Data for 2017–2020 fill located (§2).
  Next action: **Phase A / B1** (build P6 autoregressive forecast, then the validation harness).
- 2026-07-16 — Confirmed decisions: backtest holdout = leave-last-4 (2013–2016); h-grid extended to
  `{7,11,15,21,31,45}`. Existing manifest/coeffs flagged stale (old h-grid) → Phase B0 re-run before the fill.
- 2026-07-16 — **B1/P6 DONE.** `HPC_code_tunning/forecast_zoned.py`: generalized autoregressive Td forecast
  over the long/tidy zoned coeffs (arbitrary per-zone×doy feature sets, TD lags to 30 d). Reference +
  vectorised paths, 3 passing tests. Verified on real bucket-0 (parity Δ=2.5e-14, day-1 math Δ=0). Pseudo-
  forecast of 2016 on correct full-grid Tmin (60 cells, full AR year): RMSE 1.535 / MAE 1.11 / r 0.944,
  **beats climatology (2.082)** — optimistic (coeffs saw 2016); honest number awaits the leave-last-4 backtest.
  **Key finding for B2:** raw v1.2 Tmin is a 302k-ID grid, product is 2.8M-ID → B2 is a REGRID (see §6);
  regridded full-grid v1.2 Tmin exists only for 1981–2016 at `$FULL/tmin_v12/Outputs`. A2 does NOT depend on
  B2 (backtest Tmin for 2013–2016 is already in the prepared shards). Methodological choice for A2: train-only
  climatology (1981–2012) to avoid holdout leakage.
- 2026-07-16 — **Phase A A1–A4 DONE.** `backtest.py` + `effect_sizes.py`; refit-only autoregressive backtest,
  64-bucket nationwide sample (17,041 cells, all 41 zones), train-only climatology. Headline effect sizes
  (paired, location-block bootstrap 95% CI; sign-flip perm null 5000):

  | split (train→predict) | RMSE tuned | RMSE clim | ΔRMSE vs clim [CI] | skill | cells win | Cohen d | p |
  |---|---|---|---|---|---|---|---|
  | ll1 (1981–2015→2016) | 1.262 | 1.680 | +0.418 [0.417,0.420] | 0.249 | 100.0% | 4.20 | 2e-4 |
  | ll2 (1981–2014→2015–16) | 1.274 | 1.667 | +0.392 [0.391,0.394] | 0.235 | 99.98% | 3.08 | 2e-4 |
  | **ll4 (1981–2012→2013–16)** | **1.219** | **1.535** | **+0.316 [0.314,0.317]** | **0.206** | **99.99%** | **2.98** | **2e-4** |

  Tuned also beats Td=Tmin (ΔRMSE ~+2.3 °C) and zone OLS (~+1.1 °C) at every lead. Skill decays with lead
  (0.249→0.235→0.206) = expected error growth. bias ≈ −0.05 °C, r ≈ 0.990. **Result is decisive → tuning is
  worth the full run (B0 gate cleared).** Caveat: variant (a) — recipe *selection* used the 1981–2016 manifest
  (saw holdout); A5 (re-select on train-years) will bound that residual optimism. Report:
  `reports/results/phase_a_backtest.md`.
- 2026-07-17 — **A5 DONE (selection-bias check).** Honest train-only re-select (`select_backtest.py`): ll4
  tuned skill vs clim (a) 0.2057 → (b) 0.1969 → **selection bias 0.0088 (~+0.013 °C, ~4% of uplift) —
  negligible.** Tuning improvement over climatology is real & robust. **Phase A fully complete (A1–A5).**
  NOT run: B0 (full re-select+train with extended h-grid, ~31 h), B2 (regrid 2017–2020 Tmin), B3 (fill) —
  all await user go-ahead. Note: Phase A used the OLD h-grid {7,11,15,21}; B0 adds {31,45} (untested here).
- 2026-07-17 — **h-grid sensitivity check (sample, ll4).** Re-select train-only with extended
  {7,11,15,21,31,45} vs {7,11,15,21}: modal h moves 21 (51%) → 45 (**39%**, i.e. below the >40% "still
  saturating" line; 31 used 12%). Honest tuned-vs-clim skill: {7,11,15,21}=0.1969 → extended=**0.2001**
  (+0.003, ~1.6% rel; mean LOYOCV skill 0.780→0.782, uplift-vs-fixed5 0.019→0.022). **Verdict: adopt the
  extended grid for B0 (small positive, not saturating); h-grid is second-order — the tuning carries the
  result. Weak case to probe h=61 (diminishing returns + seasonal-specificity loss).** Results:
  `$RES/tuning/backtest_hgrid_ext/`.
- 2026-07-17 — **B0 LAUNCHED** (user-approved, extended h-grid). `bash tmp/b0_run.sh` detached (PID 1216017),
  `--stage select` (per_zone_n=2000, h-grid {7,11,15,21,31,45}) then `--stage train --overwrite` on 1981–2016
  v1.2 Tmin → replaces the production manifest + `zoned_coeffs/`. Old manifest backed up:
  `$RES/tuning/manifest_oldhgrid_backup.parquet`. Log: `$RES/tuning/b0_run.log`. ~37 h select + ~6 h train
  (6 h-values ≈ 1.5× the old 4-value ~25 h). GPU healthy at launch (100% util, 10.3/12.3 GB). Progress:
  select-done = manifest.parquet mtime updates + log "SELECT done"; train has no per-bucket log (watch coeffs
  mtimes). **After B0: B2 (regrid 2017–2020 Tmin, see §6) → B3 (full-grid fill) → Phase C.**
- 2026-07-17 20:23 — **B0 DIED (OOM-kill), ~12% into select.** `systemd-oomd` SIGKILL'd the whole
  `user@1000.service` slice (gnome-shell + a B0 python worker) at **PSI memory pressure 77% > 50% limit** —
  NOT a code bug, NOT a reboot (box up 10 d), NOT GPU. Root cause: parquet-heavy select churned page cache +
  the tiny 2 GiB swap (near-full) -> reclaim thrash -> oomd's aggressive user-slice 50% PSI limit fired.
  Only zones 0–4 of 41 logged; select writes the manifest only at the end, so **no durable output**:
  `manifest.parquet` still the old {7,11,15,21} (Jul 14), coeffs still stale -> full restart needed.
  Dead log preserved: `$RES/tuning/b0_run_died_20260717.log`.
- 2026-07-20 — **B0 RELAUNCHED (oomd-safe).** Now a memory-capped **transient user service** (no root; outputs
  stay user-owned): `systemd-run --user --unit=b0 --collect -p MemoryHigh=56G -p MemoryMax=72G
  -p MemorySwapMax=0 -p ManagedOOMMemoryPressure=auto bash b0_run.sh` (same script: select then
  train --overwrite, extended h-grid, 1981–2016 v1.2). `MemorySwapMax=0` + caps stop B0 from driving the slice
  PSI to the oomd cutoff; `sudo loginctl enable-linger ppalacios` decouples it from the graphical session
  (survives logout/session-death); claude-desktop added to `~/.config/autostart` (auto-reopen). Started
  10:05:43, active, 66,534 IDs sampled. Monitor: `journalctl --user -u b0` / `tail -f $RES/tuning/b0_run.log`
  / `systemctl --user status b0`. **Runtime revised up: select alone ~53 h (zones 0–4 ran ~1.3 h each) + ~6 h
  train ≈ ~2.5 days.** After B0: B2 -> B3 -> Phase C.
- 2026-07-20 12:27 — **B0 DIED AGAIN (oomd), 1 zone done.** The memory-capped user service did NOT survive:
  `systemd-oomd` killed `b0.service` at slice PSI 76.93% > 50% — trigger is the PARENT `user@1000.service`
  aggregate PSI (job + whole desktop), not the job's RAM (~110 GiB free). `MemoryHigh=56G` BACKFIRED: reclaim at
  the cap IS pressure -> spiked PSI -> made b0 the kill target. **Per-job caps cannot fix an oomd PSI kill.**
  Dead log: `$RES/tuning/b0_run_died2_20260720_1227.log`. See [[oomd-safe-long-runs]] (corrected).
- 2026-07-20 13:37 — **B0 RELAUNCHED with the REAL fix.** `sudo systemctl set-property user@1000.service
  ManagedOOMMemoryPressure=auto` (disables the user-slice PSI-kill rule; kernel OOM killer remains as
  true-exhaustion backstop). Relaunched: `systemd-run --user --unit=b0 --collect -p MemoryMax=100G
  -p MemorySwapMax=0 bash b0_run.sh` — hard ceiling + no swap, **NO MemoryHigh** (removed; it caused the
  reclaim-storm). Active/running from zone 0. This is the durable config for B0 and later B3.
- 2026-07-22 05:03 — **B0 DONE** (ran clean under the oomd fix, ~39.5 h, no kill). SELECT: all 41 zones →
  `manifest.parquet` (15,006 recipes, 22:18 Jul 21). TRAIN: `zoned_coeffs/` 8192 buckets / 8,127,391,537 tidy
  rows (05:03 Jul 22). **Sanity check PASSED:** 41 zones × doy 1–366; h-dist uses all 6 values, **h=45 modal
  43.1%** (7:14/11:9/15:9/21:11/31:13); n_features=11 kept 70.7% (light pruning, const always kept); feature
  retention 91–98%; uplift vs fixed-5 mean **+0.0153** / median +0.0084 / **16.8% ≤0** (better than old
  manifest's 22.5%); coeffs 8192/8192, schema `[ID,zone_id,doy,feature_name,coeff,r_squared_anom,h]`, **0 NaN**,
  all 6 h present. Old manifest still backed up at `manifest_oldhgrid_backup.parquet`. **manifest.parquet +
  zoned_coeffs/ are now the PRODUCTION artifacts for the 2017–2020 fill.** Next (user-gated): B2 (regrid
  2017–2020 v1.2 Tmin to the 2.8M grid, §6) → B3 (full-grid fill) → QC → Phase C.
- 2026-07-22 — **B2 DONE (future-Tmin regrid + bucketize).** No new code needed — used existing tools.
  B2.1 `nc_to_point_parquet.py --var tmin_v12 --nc-dir …/_raw/tmin_v12 --base $FULL --no-peru-potato
  --year-range 2017,2020` (detached `b2extract.service`, ~14 min) → 48 monthly files into `$FULL/tmin_v12/Outputs`
  on the **full 2,818,404-cell grid** (grid_index md5-identical to td → IDs align with B0 coeffs; raw .nc covers
  1981–2020). B2.2 `shard_future_tmin_by_bucket(prediction_years=(2017,2020), base=$FULL,
  out=$RES/future_tmin_by_bucket, future_tmin_var=tmin_v12, num_buckets=8192)` (detached `b2bucket.service`, ~1 h)
  → 8192 buckets × 4 yr = 32,768 files `[ID,FECHA,TMIN]`. **Verified:** horizon 2017–2020, TMIN −17.7…29.7 °C,
  NaN=ocean cells; **seam Jan2017−Dec2016 mean Δ +0.028 °C / median −0.10 / |Δ|>5°C 0.00% → NO grid mismatch.**
  All B3 inputs now present: coeffs (B0), climatology_by_bucket, bucketed_training_data (2016 seed),
  future_tmin_by_bucket (B2). **Next (user-gated): B3 — build the fill CLI around
  `forecast_zoned.run_bucketed_zoned_forecast` (history_end_year=2016, prediction_years=(2017,2020)).**
- 2026-07-22 — **B3 DONE (full-grid fill + QC).** Built `HPC_code_tunning/fill_zoned.py` — a parallel CLI that
  fans `forecast_bucket_zoned_from_disk` across buckets with a ProcessPoolExecutor (numerical recursion reused
  untouched; parallelism only at the independent per-bucket boundary). Feed-forward fast path for TD-lag-free
  zones NOT implemented (deferred — bucket-level parallelism already made it ~20 min). Smoke (8 buckets) →
  full run (8192 buckets, 14 workers, ~20 min, `b3fill.service`, oomd-safe): **3,183,266,247 predicted rows**,
  0 errors → `$RES/tuning/predictions_2017_2020/id_bucket=*/pred.parquet` (`[FECHA,ID,TD_predicted]`).
  **QC (national scan, all 3.18 B rows):** 0 NaN; min −13.29 / mean 19.39 / max 41.16 °C; annual means
  19.36/19.30/19.41/19.51 (no drift); seam Dec2016 obs 20.23 → Jan2017 pred 19.89 (continuous, seasonal cycle
  flows across); no cold outliers (<−15 °C = 0%). ⚠️ **WARM TAIL: >30 °C 3.18%, >32 °C 1.02%, >35 °C 0.13%
  (4.2 M cells), max 41.16 °C — physically implausible dew points (records ~35 °C). Needs SME decision:
  document as caveat / clip to a physical ceiling / investigate offending zones×doy recipes.** Maps not yet
  rendered. `fill_zoned.py` is UNCOMMITTED on branch claude/tdew-gap-fill-resume-7391e5. **Next: Phase C
  (paper draft in reports/paper/) + the warm-tail decision + AI-use disclosure & SME sign-off (CIP).**
- 2026-07-22 — **Paper figures started → `reports/paper/figures/`.** Reused existing Phase-A/select plots
  (S1 manifest_overview, S2 rmse_ladder/lead_time/delta_rmse/bias). Generated 4 new from the product
  (`scratchpad/make_paper_figs.py`, parallel scan): F1 national monthly-mean Td 2010–2020 obs→pred (seam
  **seamless** — matching amplitude/phase, no level shift), F2 mean-Td map 2017–2020 (Amazon ~25 °C, Andes
  spine, coast — geographically correct), F3 seam-diff map (SUPERSEDED — see correction below), F4 warm-tail
  panel.
  **Warm-tail DIAGNOSED: the >35 °C cells (n≈133k with ≥1 such day) cluster entirely in the NE Amazon lowlands
  (Loreto) and spike only in the late dry season (~Aug–Oct) each year — a localized, physically interpretable
  regional behavior, not random noise.** → SME decision is narrowly scoped (regional caveat / targeted clip).
- 2026-07-22 — **CORRECTION + rigorous seam test (F3 replaced).** The original F3 (Jan2017 pred − Dec2016 obs)
  compared **two different months**, so it was dominated by the real Dec→Jan seasonal cycle — a WEAK artifact
  test, and the earlier "≈0 everywhere" note here was overstated. Renamed to
  `S3_seasonal_change_dec_to_jan.png` (still a valid picture of seasonal change). New
  **`F3_seam_artifact_test.png`** uses equal-length FULL-YEAR windows (seasonality cancels) plus a
  natural-variability control: **A = obs2013–16 − obs2009–12** (both observed, no model) vs
  **B = pred2017–20 − obs2013–16** (the seam), same colour scale, + overlaid distributions.
  **Result (2,178,827 cells, annual-mean Td): A mean +0.101 sd 0.125; B mean −0.041 sd 0.176; NEITHER has a
  single cell |Δ|>1 °C.** B's spread is only ~1.4× A's and B's mean is closer to zero → **the filled years
  differ from the observed record no more than the observed record differs from itself ⇒ no seam artifact.**
  B is spatially smooth/coherent (no blockiness or speckle). ⚠️ For the paper, state honestly: B's spatial
  *pattern* (warm S-Andes, cool N-Amazon) is a coherent regional signal that this figure alone cannot separate
  from regional model bias (no observed Td after 2016) — **bound it with the Phase-A backtest** (bias ≈ −0.05 °C,
  RMSE 1.22). The faint circular features appear in panel A (observed-only) too → they are PISCO
  regression-kriging station artifacts, NOT introduced by our fill. Cache: `tuning/seam_windows_cache.parquet`.
- 2026-07-22 — **PHASE C STARTED: first full paper draft.** `reports/paper/paper.qmd` (Quarto, ~20 KB) +
  `references.bib` + `figures/` (9 PNGs). Sections: abstract, intro, data, methods (anomaly formulation,
  per-zone×doy selection, training, AR forecast, implementation), validation design, results
  (selection / temporal validation / product / seam), limitations, data-&-code availability, **AI-use
  disclosure**, **SME sign-off table**. All numbers read directly from recorded run outputs
  (`metrics_all.csv`, `effect_sizes_all.csv`, QC + seam logs) — none from memory. Renders clean
  (`quarto render`, v1.9.36): 7 figure refs, 3 citations, all cross-refs resolve; self-contained HTML
  (figures embedded) at `reports/paper/paper.html`. **Open items flagged inline [SME]/[TODO]:** warm-tail
  disposition; seam regional pattern vs regional bias; no station-level validation; **references.bib author
  lists drafted from recollection → MUST verify**; `reports/results/` is gitignored (.gitignore:64) so the
  Phase-A writeup is untracked; figure scripts still in scratchpad; product/code DOI deposit.
  **Still uncommitted on this branch: `fill_zoned.py`, `reports/paper/`.**
