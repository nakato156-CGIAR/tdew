# tdew_estimation

This repository contains the code used to estimate daily dewpoint temperature (`td`) needed to run Simcast workflows when `td` is not directly available.

PRAM pseudocode and Big-O complexity are documented in:
- `reports/pram/tdew_estimation_pram.qmd` (Quarto source, Typst format)
- `docs/pram/tdew_estimation_pram.pdf` (rendered PDF)

The core approach implemented here is an **anomaly-based local linear regression model** (“anomaly model”) that:
- builds a **daily climatology** for each grid cell (`ID`) and day-of-year (`doy`)
- models deviations from climatology (`TD_anom`) as a function of temperature anomalies and lagged anomalies
- produces **per-(ID, doy)** regression coefficients that can later be used for forecasting / filling `td`

Inspiration / related work:
- **Improving Subseasonal Forecasting in the Western U.S. with Machine Learning**  
  Jessica Hwang, Paulo Orenstein, Judah Cohen, Karl Pfeiffer, Lester Mackey  
  arXiv:1809.07394 — https://arxiv.org/abs/1809.07394  
  DOI: https://doi.org/10.48550/arXiv.1809.07394  
  We used this as inspiration for the weighted local linear regression framing and feature engineering ideas in our anomaly model.

> The first section, [Reproducibility (TimesFM benchmark)](#reproducibility-timesfm-benchmark), gives every step needed to reproduce the zero-shot TimesFM benchmark: environment, data, transformations, commands and outputs. The rest of this README describes the production anomaly model, what it produces, and how to run its pipeline end-to-end (including Dask). A section near the end explains how to detect and repair missing/incomplete DOYs.

---

## Reproducibility (TimesFM benchmark)

This section lists everything needed to reproduce the zero-shot TimesFM 3.0 benchmark
from its inputs: environment, data, transformations, commands, outputs and the checks
that tie each published number to a file. The detailed results, in Spanish, are in
[`reports/timesfm_benchmark/README.md`](reports/timesfm_benchmark/README.md). The
line-by-line provenance of every number is in
[`reports/timesfm_benchmark/TRACEABILITY.md`](reports/timesfm_benchmark/TRACEABILITY.md).

### What the benchmark measures

TimesFM 3.0 (Google, 330M parameters, checkpoint `google/timesfm-3.0-pytorch`) is used
without training or fine-tuning. For each grid cell it receives the daily dewpoint
history (`Td`) and the daily minimum temperature (`Tmin`) of the period to fill. It then
predicts the missing years of `Td`. It is scored against these rivals, always on the same
cells and days:

| method | column | what it is |
|---|---|---|
| climatology | `pred_clim` | per-cell, per-day-of-year mean of `Td` over the training years only |
| Td = Tmin | `pred_tmin` | `Tmin` used as-is |
| `zone_ols` | `pred_ols` | one `Td ~ a + b·Tmin` line per SENAMHI climate zone |
| `tuned` | `pred_tuned` | Palacios' method: per-(cell, day-of-year) local linear regression on anomalies with a tricube kernel and recipes selected per zone × day of year, forecast autoregressively (`HPC_code_tunning/`) |
| TCN | — | the project's continuous-reconstruction TCN (`experiments/reconstruction/`), departmental panel only |

The rivals are **frozen external inputs**. This repository contains their code, but
re-running them is not part of reproducing the TimesFM results:
- Palacios' backtest is `reports/paper/scripts/backtest_clean_run.sh` → `HPC_code_tunning.backtest`.
- The TCN is `experiments/reconstruction/cli.py`.

Their predictions are consumed read-only and identified by sha256 (see *Data availability*).

### Environment

| item | value used |
|---|---|
| OS / GPU | Linux, one NVIDIA RTX A2000 12 GB (driver 580.126.09); every inference figure below was measured on it |
| Python | 3.13 (`pyproject.toml` requires ≥ 3.11) |
| dependencies | `uv sync --extra timesfm --extra deep` (resolved by `uv.lock`: timesfm 3.0.2, torch 2.14.0 (the CUDA 13.0 wheel, `2.14.0+cu130`), numpy 2.3.5, pandas 2.3.3, pyarrow 24.0.0) |
| checkpoint | `google/timesfm-3.0-pytorch`, Hugging Face revision `43046b85ec22d584a13f8098c2ed39c889e129c2`, pinned in `experiments/timesfm/variants.py` (`CHECKPOINT_REVISION`) |
| numerics | screening and national runs: strict fp32 (`run.py --no-tf32`); departmental, scale and 2017–2020 runs: fp32 with TF32 matrix multiplications (the default). Re-running with the same setting reproduces the published predictions bit for bit (checked on 2026-10-12 on 32 cells of the screening, national, departmental and scale panels and on bucket 0 of the 2017–2020 product, whose file sha256 matches), and a different batch size gives the same output. Switching TF32 changes single values by up to 0.007 °C and RMSE by less than 10⁻⁴ °C. Inference is deterministic (no sampling, dropout 0) |
| licence | the TimesFM 3.0 weights are under `timesfm-non-commercial-license-v1.0`: research use only |

Every command runs from the repository root through `uv run`. Data roots are read from
three environment variables (`experiments/timesfm/paths.py`). Their defaults are the paths
of the workstation where the benchmark ran:

```bash
export TDEW_RES=/path/to/results_tuning              # production bucket store, read-only
export TDEW_TIMESFM_WORK=/path/to/tdew_timesfm       # TimesFM predictions and intermediates (~180 GB)
export TDEW_RECONSTRUCTION_WORK=/path/to/tdew_reconstruction   # TCN predictions and departmental panel
```

### Data availability

- **Source data.** The source data are the SENAMHI PISCO gridded products at 0.01°: daily `Td` from PISCO v1.1 (1981–2016) and daily `Tmin` from PISCOt v1.2 (1981–2020).
- **Derived inputs.** These are not in the repository because of their size, and are available from the authors on request:
  - the bucketed store `$TDEW_RES`, about 180 GB;
  - Palacios' backtest predictions;
  - the TCN predictions;
  - the TimesFM predictions.
- **Checksums.** [`reports/timesfm_benchmark/INPUTS.sha256`](reports/timesfm_benchmark/INPUTS.sha256) lists the sha256 of every frozen input the scoring reads. For the per-bucket trees it lists bucket `0000` only.

To verify a local copy:

```bash
grep -v '^#' reports/timesfm_benchmark/INPUTS.sha256 | envsubst | sha256sum -c
```

### Data flow

```
PISCO monthly point parquet (Td v1.1, Tmin v1.2)            [external]
  │  HPC_code/prep_inputs.py → tdew_estimation.bucketed_data   (inner join on ID, FECHA; ID % 8192)
  ▼
$TDEW_RES/bucketed_training_data/id_bucket=NNNN/train_YYYY.parquet   (1981–2016)
$TDEW_RES/future_tmin_by_bucket/id_bucket=NNNN/future_tmin_YYYY.parquet (2017–2020)
  │  experiments/timesfm/panel.py   context = Td up to Dec 31 of the last training year,
  │                                  covariate = Tmin over context + horizon, train-only climatology
  ▼
experiments/timesfm/run.py / real.py   TimesFM 3.0, one forward pass per cell, median + 9 deciles
  ▼
$TDEW_TIMESFM_WORK/preds_*/<split>__<variant>.parquet   (ID, FECHA, pred, q10..q90)
  │  evaluate.py, merge_predictions.py + HPC_code_tunning/effect_sizes.py, by_tier_month.py,
  │  kl.py, departamental.py, departamental_pareado.py, escala.py, real_compare.py, real_tail.py
  │  (joined with Palacios' $TDEW_RES/tuning/backtest_clean/<split>/predictions.parquet)
  ▼
reports/timesfm_benchmark/**/*.csv  + one provenance row each in reports/metric_provenance.jsonl
  │  make_figures.py, artifact_data.py
  ▼
reports/timesfm_benchmark/figs/*.png, reports/timesfm_benchmark/artifact/{index.html,datos.js}
```

### Inputs and their columns

The grid is the PISCO grid: 1,982 latitudes × 1,422 longitudes at 0.01°, i.e.
2,818,404 cells. `ID` is the row-major cell index (latitude outer, longitude inner), an
int64 shared by every table. Of those cells, 2,178,827 have `Td` and `Tmin`. The other
639,577 have no values and are dropped when a panel is built.

| input | columns | used for |
|---|---|---|
| `bucketed_training_data/…/train_YYYY.parquet` | `ID`, `FECHA` (date), `TD` (°C, float32), `TMIN` (°C, float32), `doy` (1–366, int16) | TimesFM context and covariate; train-only climatology |
| `future_tmin_by_bucket/…/future_tmin_YYYY.parquet` | `ID`, `FECHA`, `TMIN` | `Tmin` covariate for 2017–2020 |
| `tuning/backtest_clean/<split>/predictions.parquet` | `ID`, `zone_id`, `FECHA`, `doy`, `TD_obs`, `pred_tuned`, `pred_clim`, `Tmin_hold`, `pred_tmin`, `pred_ols` | observed `Td` and the four Palacios rivals (17,027 cells) |
| `tuning/predictions_2017_2020/…/pred.parquet` | `FECHA`, `ID`, `TD_predicted` | Palacios' 2017–2020 product, for the agreement analysis |
| `tuning/support_distance.parquet` | `ID`, `lon`, `lat`, `dist_km`, `tier` | observational-support tiers (`within`, `near`, `marginal`, `extrapolated`, `unsupported`) |
| `zone_table.parquet` | `ID`, `zone_id`, `zone_label`, `lon`, `lat` | SENAMHI Thornthwaite climate zone of each cell (41 zones) |
| `Data/silver/department_grid_ids/*.csv` | `ID`, `latitude`, `longitude` | cells of Lima, Cusco, Loreto and San Martín (436,519); see [`docs/MEDALLION.md`](docs/MEDALLION.md) |

### What a bucket is

A bucket is the set of cells with the same `ID % 8192`. It is stored as a Hive-style
folder `id_bucket=0000` … `id_bucket=8191` (`tdew_estimation/bucket_layout.py`).

- **Contents.** 2,818,404 = 344 × 8,192 + 356, so buckets 0–355 hold 345 cells and the rest hold 344. About 266 of those cells carry data.
  - One bucket-year file holds every cell of the bucket for every day of the year: 125,925 rows for bucket 0 in a 365-day year, 126,270 in a leap year.
  - Each file is about 400 KB.
  - `bucketed_training_data` has 8,192 × 36 = 294,912 files (119.5 GB).
- **Why buckets.**
  - The `Td`–`Tmin` join over 2.8 million cells and 36 years is the expensive step. Bucketing pays it once.
  - It also leaves the full series of every cell in one place. A context window or a climatology can then be built one bucket at a time with bounded memory.
- **Why modulo.** IDs are row-major and 8,192 is wider than a grid row (1,422). Consecutive cells of a bucket are therefore about 5.8 latitude rows apart, and every bucket is a lattice spanning the whole domain.
  - Palacios' backtest samples 64 buckets with `numpy.random.default_rng(0)`. That gives a sample spread over the whole country, and also over the whole PISCO bounding box: 51.4 % of those cells lie outside Peru.
- **Bucket count.** The code default of `build_bucketed_training_dataset` is 1,024. The store was built with 8,192, which `experiments/timesfm/panel.py` (`NUM_BUCKETS`) assumes.

The full description of the store, including the production climatology that the
validation does **not** use, is in [`docs/MEDALLION.md`](docs/MEDALLION.md), section
*Almacén de producción*.

### Splits and leakage rules

The splits are those of `HPC_code_tunning/backtest.py`, under which Palacios' paper
reports its numbers:

| split | context / training | held-out block | days |
|---|---|---|---|
| `ll1` | 1981–2015 | 2016 | 366 |
| `ll2` | 1981–2014 | 2015–2016 | 731 |
| `ll4` | 1981–2012 | 2013–2016 | 1,461 |
| `real` | 1981–2016 | 2017–2020 (no observed `Td`) | 1,461 |

**Context cut-off.** The context ends on December 31 of the last training year. No
held-out `Td` reaches the model, the climatology or the normalisation.

**Climatology.** The climatology is the per-(`ID`, `doy`) mean over the context years
only. It is computed in `panel.py`, identically to `backtest.train_only_climatology`;
day 366 is averaged over the leap years only.

**`Tmin` in the held-out block.** `Tmin` of the held-out block is given as a covariate
aligned to the same day. It is exogenous, it exists over the whole range, and it is the
same information Palacios' method consumes.

**Dropped cells.** A cell with any missing `Td` or `Tmin` value in the context, or any
missing `Tmin` in the horizon, is dropped whole. It is never interpolated.

**Common panel.** Every method is scored on the exact intersection of cells and days.

### Cell panels

`uv run python -m experiments.timesfm.scripts.make_panels --out-dir <dir> --check`
rebuilds the six panels from their sources and checks they equal the files the runs
used. All six matched on 2026-10-12.

| panel | cells | rule | role |
|---|---|---|---|
| `nacional_17041.csv` | 17,041 | cells of Palacios' 64-bucket backtest (`tuning/backtest/ll4`) | TimesFM inference panel for ll1/ll2/ll4 |
| `nacional_17027.csv` | 17,027 | cells of Palacios' clean backtest (`tuning/backtest_clean/ll4`); the other 14 are not in it | **national headline** |
| `cribado_estratificado.csv` | 1,106 (1,092 scored) | up to 40 cells per SENAMHI zone from `nacional_17041`, `default_rng(20260922)` | screening of the nine variants |
| `ll4_reducido_512.csv` | 2,048 | 512 per department, `select_panel(Data/silver, "dev_a", seed=0)` (stratified by longitude, latitude and elevation) | departmental table with the TCN |
| `panel_436k.csv` | 436,519 | all cells of the four departments | scale run (inference cost) |
| `panel_escala_submuestra.csv` | 61,113 | 14 % of each department, `default_rng(20260922)` | scale scoring: the cells the `tuned` rival reached |

### The nine variants and the transformation applied

Each variant is a frozen dataclass in `experiments/timesfm/variants.py`:

| variant | target | covariates | context start |
|---|---|---|---|
| `uni_td_full` | `Td` | — | 1981 |
| `uni_anom_full` | `Td` anomaly | — | 1981 |
| `tmin_td_full` | `Td` | `Tmin` | 1981 |
| **`tmin_anom_full`** | `Td` anomaly | `Tmin` anomaly | 1981 |
| `tmin_doy_td_full` | `Td` | `Tmin`, sin/cos of day of year (period 366) | 1981 |
| `tmin_td_med` | `Td` | `Tmin` | 2002 |
| `tmin_td_short` | `Td` | `Tmin` | 2011 |
| `tmin_td_symavg` | `Td` | `Tmin` | 1981, symmetric averaging |
| `tmin_td_znorm` | `Td` | `Tmin` | 1981, external z-score |

For one cell and one split, `run.py` does the following:
1. It takes the target series over the context. For anomaly variants this is `Td − Td_clim(doy)`.
2. It takes the covariate over context plus horizon, with exactly `C + H` values. Its width sets the forecast horizon.
3. It calls `TimesFM3Forecaster.predict_batch(..., make_positive=False, sort_quantiles=True)`. The model decodes the full horizon in a **single pass**, not autoregressively.
4. It keeps the median (`pred`) and the nine deciles (`q10`…`q90`).
5. For anomaly variants it adds `Td_clim(doy)` back to the median and to every decile (`run.py::to_physical`).

The output is one long parquet per split and variant, with columns `ID`, `FECHA`, `pred`
and `q10`…`q90`. The 2017–2020 product (`real.py`) is written per bucket with columns
`ID` int32, `day` int16 (days since 2017-01-01), `pred` and `q10`…`q90`, plus a `.done`
record per bucket.

The winning variant `tmin_anom_full` was chosen by the lowest screening RMSE on `ll4`.
It is the only variant run at the national, departmental, scale and 2017–2020 levels.

### Metrics

The definitions are in `tdew_estimation/metrics.py`, `experiments/timesfm/probabilistic.py`
and `HPC_code_tunning/effect_sizes.py`.

- **Point metrics.** RMSE, MAE, bias (`pred − obs`, so positive means warm) and Pearson
  `r` are pooled over all cell-days, not averaged per cell.
- **Skill.** Skill is `1 − RMSE/RMSE_clim`, with the train-only climatology. This
  RMSE-based form is the convention of Palacios' paper and is lower than the MSE-based
  `1 − MSE/MSE_clim`.
- **Effect sizes.**
  - ΔRMSE is pooled. Its 95 % CI comes from a bootstrap that resamples cells (1,000 resamples, seed 0).
  - The win fraction counts cells where the method's own RMSE is lower.
  - Cohen's *d* is the paired d_z on the per-cell ΔRMSE.
  - The one-sided sign-flip permutation test uses 5,000 permutations. Its floor is p = 0.0002.
- **Probabilistic metrics.**
  - Approximate CRPS = (2/9) · Σ pinball over the nine deciles. It ignores the mass beyond q10 and q90, so it is biased low.
  - 80 % coverage is the share of observations inside [q10, q90].
- **KL divergence.** Fixed histograms over [−20, 50) °C with 0.1 and 0.5 °C bins and Jeffreys smoothing, in nats.

### Step-by-step

The stage scripts are in [`experiments/timesfm/scripts/`](experiments/timesfm/scripts/).
Each one sources `env.sh`, which reads the three variables above. Inference times were
measured on the RTX A2000.

| step | script | does | time | writes |
|---|---|---|---|---|
| 0 | `00_panels.sh` | rebuild and check the six panels | minutes | `$TDEW_TIMESFM_WORK/panels_rebuilt/` |
| 1 | `01_throughput.sh` | inference cost per context × horizon × batch (45 combinations, 32 cells) | not recorded | `coste_throughput.csv` |
| 2 | `02_cribado.sh` | nine variants on 1,106 cells, `ll4` (`--no-tf32`); score on 1,092 | 49 min | `$WORK/preds_cribado/`, `cribado_limpio/` |
| 3 | `03_nacional.sh` | winner on 17,041 cells, ll1/ll2/ll4 (`--no-tf32`); merge, ladder, effect sizes, tiers, monthly bias, KL | 4 h | `$WORK/preds_nacional/`, `nacional_limpio/`, `kl_limpio/`, `curva_error_nacional_limpio.csv` |
| 4 | `04_departamental.sh` | winner on the 2,048-cell departmental panel; table with the TCN and `tuned` | 11 min | `departamental/` |
| — | `uv run python -m experiments.timesfm.departamental_pareado` | per-cell paired test against each departmental rival | minutes | `departamental/pareado.csv` |
| 5 | `05_escala.sh` | winner on 436,519 cells; score on 61,113 | 23 h 48 min | `$WORK/preds_escala/`, `escala/leaderboard.csv` |
| 6 | `06_real.sh` | 2017–2020 product on 2,178,827 cells; agreement with Palacios; warm tail | ~5 days + ~2 h | `$WORK/preds_real/`, `real_limpio/` |
| 7 | `07_reporte.sh` | figures and interactive page (no metric is recomputed) | minutes | `figs/`, `artifact/datos.js` |

Step 3 alone reproduces the headline, about 4 h of GPU time. To check that scoring
reproduces from the published predictions without the GPU, run only the scoring
commands of `02_cribado.sh` and `03_nacional.sh` against the existing `preds_*`
directories.

### Where each headline number comes from

All values are in °C over the held-out block, pooled over cell-days.

| claim | value | file |
|---|---|---|
| national `ll4` RMSE: TimesFM / `tuned` / climatology (17,027 cells, 24,876,447 pairs) | 1.1536 / 1.2279 / 1.5352 | `nacional_limpio/leaderboard.csv` |
| national `ll1`, `ll2` RMSE: TimesFM vs `tuned` | 1.1736 vs 1.2538; 1.1533 vs 1.2765 | same |
| `ll4` ΔRMSE `tuned` − TimesFM, CI, cells won, *d* | 0.0743 [0.074, 0.075], 99.2 %, 2.07 | `nacional_limpio/effect_sizes_all.csv` |
| screening winner RMSE and gap to runner-up (1,092 cells) | 0.8389; 0.023 | `cribado_limpio/leaderboard.csv`, `cribado_limpio/sesgo_seleccion_ll4.csv` |
| departmental RMSE: TimesFM / TCN seeds 0–2 / `tuned` (2,048 cells) | 0.7996 / 0.8484, 0.8429, 0.8325 / 0.8669 | `departamental/metrics.csv` |
| departmental ΔRMSE TimesFM − TCN, by seed | −0.049, −0.043, −0.033 | `departamental/pareado.csv` |
| scale RMSE, re-weighted: TimesFM / `tuned` / climatology (61,113 cells) | 0.9983 / 1.0681 / 1.3911 | `escala/leaderboard.csv` |
| 2017–2020 agreement TimesFM − Palacios: RMSE, bias, *r* (3,183,266,247 values) | 0.465, +0.053, 0.9986 | `real_limpio/agreement_overall_limpio.csv` |
| reproduction of Palacios' published 2017–2020 figures | 8 of 8 | `real_limpio/reproduction_palacios_limpio.csv` |

Every CSV under `reports/timesfm_benchmark/` has a row in
`reports/metric_provenance.jsonl` with the model, split, panel, inputs, manifest and git
commit. `tests/test_metric_provenance.py` fails if a CSV appears without one. The protocol
is frozen in `docs/protocol/timesfm_manifest.yaml`, with three addenda: the clean
reference, the 2017–2020 product, and the 2026-10-12 errata and pins.

### Checks that can be run

```bash
uv run pytest tests/test_timesfm_*.py tests/test_metric_provenance.py tests/test_artifact*.py -q   # synthetic data, no GPU
uv run python -m experiments.timesfm.scripts.make_panels --out-dir /tmp/panels --check            # panels
uv run python -m experiments.timesfm.real --verify-only --ids-from-palacios                        # 2017–2020 product, per-bucket sha256
```

The scoring scripts also check themselves at run time:
- `by_tier_month.py` aborts if `tuned` does not reproduce the paper's per-tier RMSE and monthly bias.
- `real_compare.py` writes the reproduction control.
- `artifact_data.py` aborts if any number on the page departs from its CSV.

### Caveats a reader should know

- **Selection on the test block.** The nine variants were compared on `ll4` 2013–2016, the same block later reported. The 1,092 screening cells are a subset of the 17,027 national cells. The national figure of the winner therefore carries some selection optimism. The gap to the runner-up (0.023 °C) is about a third of the advantage over `tuned` (0.074 °C).
- **The "national" panel is not a sample of Peru.** It is a sample of the PISCO bounding box: 51.4 % of its cells are in Brazil, Bolivia, Ecuador or Colombia.
- **Leaky `tuned` in two tables.** The departmental and scale tables use a `tuned` whose recipes were selected with 1981–2016. They are not comparable with the clean national figures.
- **The TCN seed matters.** In the departmental table the advantage of TimesFM over the TCN depends on the seed: 0.033–0.049 °C, with 86.7–96.2 % of cells won.
- **Bootstrap intervals.** The CIs resample cells as if they were independent. Spatial autocorrelation makes them too narrow.
- **2017–2020 warm tail.** TimesFM reproduces Palacios' implausible `Td` > 35 °C values in the Amazon lowlands, and makes them more frequent: 0.171 % of values against 0.133 %.
- **Commit hash per bucket.** The git commit recorded per bucket of the 2017–2020 product is read when the bucket closes and does not detect uncommitted changes. Four commits appear. None of them changes the inference code.

Generative AI (Claude Code) was used to implement, run and document this benchmark. The
protocol decisions were made by the authors, and the conclusions should be validated by
domain experts.

---

## Deep learning experiments and where their metrics live

Besides the production model described in this README, the repository compares
deep learning variants and a zero-shot foundation model against the anomaly
method. Their metrics don't live in a single place, so it's worth knowing where
to look for each one.

### MLflow: runs with real training

Runs with actual training — week 1 baselines, ablations, and the TCN — are
logged with MLflow against `sqlite:///mlflow.db`. Start the server with:

```bash
uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000
```

In MLflow 3.x, opening an experiment lands the UI on the Overview/Traces tab by
default, which is meant for LLM traces. This project doesn't generate traces,
so that tab shows up empty without indicating any problem. Runs with metrics
are in the Runs tab, reached by appending `/runs` to the URL (for example
`http://<host>:5000/#/experiments/1/runs`):

| experiment | runs | metrics |
|---|---|---|
| `tdew-week1` (id 1) | per-site baselines (`week1-baseline`); TCN ablations (`x46.1-ablation-*`); attention TCN (`week1-tcn-attention`) | `test_rmse`/`validation_rmse`/`test_mae`/`test_skill_vs_clim` for baselines; `val_rmse_pooled` and `val_rmse_<site>` for the ablations; `val_rmse`, `val_mae`, `val_bias`, `val_r`, `val_skill_vs_clim`, `train_loss` for the attention TCN |
| `tdew-reconstruction` (id 2) | continuous Td reconstruction (`td-reconstruction`), with the TCN and ridge/histgb baselines | aggregated `rmse`, `mae`, `bias`, `r`, plus per-department breakdowns (`Cusco_rmse`, `Lima_rmse`, `Loreto_rmse`, `San Martin_rmse`) |

Within `tdew-reconstruction`, the runs that matter for comparing against
TimesFM are the ones with `model=tcn`, protocol `ll4`, `feature_set=exogenous_full`,
and seed 0: they're the source of the "direct TCN" row in the departmental
panel described below.

### TimesFM: zero-shot, MLflow only for evaluations

The nine TimesFM variants don't train, so they produce no training runs. The only
MLflow runs are opt-in evaluations (`--mlflow` in `by_tier_month.py`, `real.py`,
`real_compare.py`, `real_tail.py`; experiment `tdew-timesfm-benchmark`). The metrics
live in [`reports/timesfm_benchmark/`](reports/timesfm_benchmark/) and the steps to
reproduce them are in [Reproducibility (TimesFM benchmark)](#reproducibility-timesfm-benchmark)
above. The current figures are scored against Palacios' clean backtest
(`backtest_clean`, 17,027 national cells, 1,092 screening cells). The folders without the
`_limpio` suffix keep the earlier scoring against the run whose recipe selection saw
1981–2016 (17,041 and 1,106 cells).

---

## Quickstart (bash: full pipeline)

You have two ways to run the pipeline:

- **Recommended**: run the one-shot helper script:
  - `Local/run_pipeline.sh`
- **Manual**: call the Python modules directly if you want to inspect or customize each phase

### Environment (recommended)
```bash
# from the repo root; uv.lock pins every dependency
uv sync                                   # production pipeline
uv sync --extra timesfm --extra deep      # adds TimesFM and torch for the benchmark
```

Run every module through `uv run python ...`. The examples below use `python -c` for
brevity; prefix them with `uv run`.

### Option A (recommended): run the helper script

The helper script runs:
1) compute climatology
2) build a **bucketed merged training dataset** (`TD`, `TMIN`, `doy`) on disk
3) shard climatology by the same ID buckets
4) train anomaly coefficients **by bucket** with Dask
5) DOY completeness check
6) rerun only failed DOYs into a patch dataset
7) patch + re-check

```bash
bash Local/run_pipeline.sh \
  --base "/path/to/base" \
  --results "/path/to/results" \
  --grid "/path/to/grid.dbf" \
  --n-workers 8 \
  --threads 4 \
  --mem 16GB \
  --batch-size 64 \
  --num-buckets 1024
```

The production store that the TimesFM benchmark and Palacios' backtest read was built with 8,192 buckets by `HPC_code/prep_inputs.py`, not with the 1,024 of this example (see *What a bucket is* above).

Outputs written under `--results`:
- `daily_climatology.parquet`
- `bucketed_training_data/`
- `climatology_by_bucket/`
- `llr_coeffs_anomaly_dataset/`
- `anomaly_failures/`
- `llr_coeffs_anomaly_patch_dataset/` (only if failures exist)
- `anomaly_patch_failures/` (only if failures exist)

Useful flags:
```bash
# print resolved settings, don’t run heavy steps
DRY_RUN=1 bash Local/run_pipeline.sh --base "$BASE" --results "$RESULTS" --grid "$GRID"

# if you already prepared the bucketed inputs and only want model fitting
bash Local/run_pipeline.sh --base "$BASE" --results "$RESULTS" --grid "$GRID" --skip-climatology --skip-prepare --skip-patch

# rebuild bucketed training shards and overwrite coefficient outputs
bash Local/run_pipeline.sh --base "$BASE" --results "$RESULTS" --grid "$GRID" --overwrite-prepared --overwrite-clim-buckets --overwrite-train-output
```

### Option B (manual): run each step

These examples show the full workflow:
1) compute climatology
2) build a bucketed TD/TMIN training dataset
3) shard climatology by the same buckets
4) train coefficients by bucket with Dask
5) check which DOYs are incomplete
6) rerun only those DOYs (Dask) into a patch dataset
7) patch the coefficient dataset and re-check

There is no installed console script; you run Python modules/scripts directly.

#### 0) Define paths once (bash variables)
```bash
BASE="/path/to/base"                 # contains td/Outputs, tmin_v11/Outputs (PISCOt v1.1) and tmin_v12/Outputs (v1.2)
RESULTS="/path/to/results"           # where you will write outputs
GRID="/path/to/grid.dbf"             # grid file defining IDs (dbf/shp/gpkg/geojson/csv/parquet)

CLIM="${RESULTS}/daily_climatology.parquet"
PREPARED="${RESULTS}/bucketed_training_data"
CLIM_BUCKETS="${RESULTS}/climatology_by_bucket"
COEFFS="${RESULTS}/llr_coeffs_anomaly_dataset"
FAILURES="${RESULTS}/anomaly_failures"
PATCH="${RESULTS}/llr_coeffs_anomaly_patch_dataset"
PATCH_FAILURES="${RESULTS}/anomaly_patch_failures"
```

#### 1) Compute daily climatology (TD_clim and TMIN_clim)
This step reads monthly TD/TMIN parquet inputs for the training years and writes a single climatology parquet.

```bash
python -c '
from pathlib import Path
from tdew_estimation.climatology import calculate_and_save_climatology_chunked

calculate_and_save_climatology_chunked(
    year_range=(1981, 2016),
    base_path=Path("'"${BASE}"'"),
    output_file=Path("'"${CLIM}"'"),
    td_var="td",
    tmin_var="tmin_v12",
    outputs_subdir="Outputs",
    engine="pyarrow",
    cleanup=True,
)
print("Wrote:", "'"${CLIM}"'")
'
```

Expected output:
- `daily_climatology.parquet` with columns: `ID`, `doy`, `TD_clim`, `TMIN_clim`

#### 2) Build bucketed training shards and bucketed climatology
This step pays the expensive TD/TMIN merge once, writes merged monthly shards partitioned by `id_bucket`, and writes matching climatology shards.

```bash
python -c '
from pathlib import Path
from tdew_estimation.bucketed_data import (
    build_bucketed_training_dataset,
    shard_climatology_by_bucket,
)

build_bucketed_training_dataset(
    year_range=(1981, 2016),
    base_path=Path("'"${BASE}"'"),
    output_dir=Path("'"${PREPARED}"'"),
    td_var="td",
    tmin_var="tmin_v12",
    outputs_subdir="Outputs",
    num_buckets=1024,
    overwrite=False,
)

shard_climatology_by_bucket(
    climatology_path=Path("'"${CLIM}"'"),
    output_dir=Path("'"${CLIM_BUCKETS}"'"),
    num_buckets=1024,
    overwrite=False,
)
print("Prepared:", "'"${PREPARED}"'")
print("Climatology shards:", "'"${CLIM_BUCKETS}"'")
'
```

Expected outputs:
- yearly merged bucket shards under `bucketed_training_data/id_bucket=*/train_YYYY.parquet`
- one climatology parquet per bucket under `climatology_by_bucket/id_bucket=*/climatology.parquet`

#### 3) Train anomaly coefficients by bucket with Dask
This runs one Dask task per bucket, writes one coefficient parquet per bucket, and writes structured failure logs per bucket.

```bash
python -c '
from pathlib import Path
from tdew_estimation.anomaly_train import AnomalyTrainingConfig
from tdew_estimation.anomaly_dask import DaskAnomalyConfig, run_bucketed_anomaly_training_dask

cfg = AnomalyTrainingConfig(
    base_path=Path("'"${BASE}"'"),
    td_var="td",
    tmin_var="tmin_v12",
    train_year_range=(1981, 2016),
    h=11,
    kernel="Tricube",
    min_samples=15,
)

dc = DaskAnomalyConfig(
    n_workers=8,
    threads_per_worker=4,
    memory_limit="16GB",
    batch_size=64,
)

summaries = run_bucketed_anomaly_training_dask(
    prepared_training_root=Path("'"${PREPARED}"'"),
    bucketed_climatology_root=Path("'"${CLIM_BUCKETS}"'"),
    coeffs_output_root=Path("'"${COEFFS}"'"),
    failure_output_root=Path("'"${FAILURES}"'"),
    config=cfg,
    dask_config=dc,
    overwrite=False,
)
print("Buckets processed:", len(summaries))
'
```

Expected outputs:
- coefficient dataset under `llr_coeffs_anomaly_dataset/id_bucket=*/coeffs.parquet`
- failure logs under `anomaly_failures/id_bucket=*/failures.parquet`

#### 4) Check which DOYs are incomplete (failures)
This checks, for each DOY, how many distinct IDs exist in the coefficient dataset and compares that to the expected ID count from the grid file.

```bash
python -c '
from pathlib import Path
from tdew_estimation.grid import expected_count_from_grid
from tdew_estimation.checks import detect_incomplete_anomaly_doys

expected = expected_count_from_grid(Path("'"${GRID}"'"), id_column="ID")
report = detect_incomplete_anomaly_doys(
    Path("'"${COEFFS}"'"),
    expected_count=expected,
    id_col="ID",
    doy_col="doy",
    strict_inequality=True,
    include_missing=True,
    verbose=True,
)
print("DOYS_TO_FIX =", report.incomplete_doys)
'
```

If `DOYS_TO_FIX` is empty, you’re done.

#### 5) Retrain only the failed DOYs with Dask (create a patch dataset)
This reruns training restricted to `DOYS_TO_FIX` for all buckets and writes a patch coefficient dataset.

```bash
python -c '
from pathlib import Path
from tdew_estimation.grid import expected_count_from_grid
from tdew_estimation.checks import detect_incomplete_anomaly_doys
from tdew_estimation.anomaly_train import AnomalyTrainingConfig
from tdew_estimation.anomaly_dask import rerun_failed_doys_with_bucketed_dask, DaskAnomalyConfig

grid = Path("'"${GRID}"'")
coeffs = Path("'"${COEFFS}"'")
patch = Path("'"${PATCH}"'")

expected = expected_count_from_grid(grid, id_column="ID")
report = detect_incomplete_anomaly_doys(coeffs, expected_count=expected, verbose=False)
doys_to_fix = report.incomplete_doys
print("DOYS_TO_FIX =", doys_to_fix)

cfg = AnomalyTrainingConfig(
    base_path=Path("'"${BASE}"'"),
    td_var="td",
    tmin_var="tmin_v12",
    train_year_range=(1981, 2016),
    h=11,
    kernel="Tricube",
    min_samples=15,
)

dc = DaskAnomalyConfig(n_workers=8, threads_per_worker=4, memory_limit="16GB", batch_size=64)

if doys_to_fix:
    rerun_failed_doys_with_bucketed_dask(
        prepared_training_root=Path("'"${PREPARED}"'"),
        bucketed_climatology_root=Path("'"${CLIM_BUCKETS}"'"),
        patch_output_root=patch,
        failure_output_root=Path("'"${PATCH_FAILURES}"'"),
        failed_doys=doys_to_fix,
        config=cfg,
        dask_config=dc,
    )
    print("Wrote patch dataset:", patch)
else:
    print("No DOYs to fix; skipping patch creation.")
'
```

#### 6) Patch the coefficient dataset and re-check completeness
This replaces the failed DOY rows in the base coefficient dataset with the rerun results from the patch dataset.

```bash
python -c '
from pathlib import Path
from tdew_estimation.grid import expected_count_from_grid
from tdew_estimation.checks import detect_incomplete_anomaly_doys
from tdew_estimation.patch_coeffs import patch_anomaly_coeffs_inplace

grid = Path("'"${GRID}"'")
coeffs = Path("'"${COEFFS}"'")
patch = Path("'"${PATCH}"'")

expected = expected_count_from_grid(grid, id_column="ID")
report = detect_incomplete_anomaly_doys(coeffs, expected_count=expected, verbose=False)
doys_to_fix = report.incomplete_doys

if not doys_to_fix:
    print("No DOYs to patch; coefficients already complete.")
else:
    summary = patch_anomaly_coeffs_inplace(
        base_coeffs_path=coeffs,
        patch_coeffs_path=patch,
        doys_to_patch=doys_to_fix,
        id_col="ID",
        doy_col="doy",
    )
    print("Patch summary:", summary)

    report2 = detect_incomplete_anomaly_doys(coeffs, expected_count=expected, verbose=True)
    print("OK:", report2.ok)
'
```

---

## Running Dask across multiple computers (design guide; not implemented here)

The current code starts a *local* Dask cluster inside `run_bucketed_anomaly_training_dask(...)` by calling `Client(n_workers=..., threads_per_worker=..., ...)`.

To run across multiple machines, you keep the **training logic unchanged** and only change **how the Dask `Client` is created**:
- start a scheduler + workers outside Python (on multiple computers)
- connect the driver script to the remote scheduler address

### High-level architecture

You will run:
- 1 machine as the **scheduler** (coordinates tasks)
- N machines as **workers** (execute bucket training tasks)
- 1 machine as the **driver** (your script that submits tasks; can be the scheduler machine, but doesn’t have to be)

### Network and security prerequisites (typical)

Before you try multi-host Dask, confirm with your IT/security team:

1) **Network reachability**
   - Workers must be able to reach the scheduler host (by DNS name or fixed IP).
   - The driver must be able to reach the scheduler as well.

2) **Firewall / ports (concrete examples)**
   - Dask distributed requires TCP connectivity between scheduler, workers, and your driver.
   - Common/default ports you’ll see in practice:
     - **Scheduler port**: `8786/tcp` (clients + workers connect here)
     - **Dashboard port**: `8787/tcp` (optional web UI)
     - **Worker ports**: can be **dynamic/ephemeral** by default unless you pin them
   - In many organizations, inbound ports are blocked by default. The minimum you typically need is:
     - Allow **workers → scheduler** to reach `SCHEDULER_HOST:8786/tcp`
     - Allow **driver → scheduler** to reach `SCHEDULER_HOST:8786/tcp`
     - (Optional) Allow **your browser → scheduler** to reach `SCHEDULER_HOST:8787/tcp` for the dashboard
   - If security policy requires a fixed port range for workers, plan to pin worker ports to a known range (example: `9000–9100/tcp`) and open that range as needed.

3) **VPN / routing**
   - If the machines are on different networks/subnets, you may need:
     - VPN access, or
     - a routed network path between subnets, or
     - a bastion/jump host strategy.
   - Make sure the scheduler host is reachable from all worker nodes over the VPN.
   - In many orgs, you’ll need explicit permission to run compute traffic over the VPN.

4) **Authentication / authorization**
   - In secured environments, running a scheduler that accepts arbitrary task submissions may require:
     - running inside a trusted network segment,
     - access controls at the network layer, and/or
     - TLS and authenticated connections (recommended if crossing trust boundaries).
   - If your org requires it, use Dask’s TLS support and distribute certs/keys securely (do not commit secrets).

5) **Data access**
   - All workers must be able to read the same training parquet inputs (TD/TMIN), bucketed training shards, and coefficient / patch datasets.
   - Common patterns:
     - **Shared filesystem** (NFS/SMB/Lustre): simplest; paths must be valid on every machine.
     - **Object storage** (S3/GCS/Azure): requires adapting I/O paths and credentials; not implemented here.
   - Avoid “local-only” paths that exist only on the driver machine.

### Operational requirements

- **Consistent environment**: all nodes should run the same Python version and package versions (including `dask[distributed]`, `pandas`, parquet engine).
- **Resource sizing**:
  - Workers should have enough RAM to load one bucket shard of merged TD/TMIN rows and the matching climatology shard.
  - Tune number of workers and threads based on CPU/RAM and parquet I/O throughput.
- **Logging / observability**:
  - For a cluster, plan where logs go (local logs, central logging, etc.).
  - Consider monitoring task failures and re-running subsets (your DOY patch workflow helps).

### What exact code you must add/change (where and what)

#### File: `tdew_estimation/anomaly_dask.py`
In `run_bucketed_anomaly_training_dask(...)`, change the function signature to accept a remote scheduler address:

1) Add this parameter to `run_bucketed_anomaly_training_dask(...)`:
- `scheduler_address: Optional[str] = None`

2) Replace the current “Start Dask client (local cluster via distributed defaults)” block with a conditional:

- If `scheduler_address` is provided:
  - connect to the existing multi-host scheduler:
    - `client = Client(scheduler_address, timeout=...)`
  - example values (match your scheduler host/port):
    - `scheduler_address="tcp://SCHEDULER_HOST:8786"`
    - `scheduler_address="tls://SCHEDULER_HOST:8786"` (if you enable TLS)
- Else (existing behavior):
  - start a local cluster as today:
    - `client = Client(n_workers=..., threads_per_worker=..., memory_limit=..., timeout=...)`

That’s the only code change required to support multi-computer execution.

#### File: `tdew_estimation/anomaly_dask.py`
In `rerun_failed_doys_with_bucketed_dask(...)`, forward the scheduler address:
- Add `scheduler_address: Optional[str] = None` to the signature
- Pass it through when calling `run_bucketed_anomaly_training_dask(...)`

#### What you must start outside Python (operational, not implemented here)
- Start scheduler on a reachable host. Typical/default:
  - scheduler listens on `8786/tcp`
  - dashboard on `8787/tcp` (optional)
- Start workers on each machine and point them to:
  - `tcp://SCHEDULER_HOST:8786`
- Ensure your network/firewall rules allow at least:
  - driver → `SCHEDULER_HOST:8786/tcp`
  - workers → `SCHEDULER_HOST:8786/tcp`
  - (optional) your browser → `SCHEDULER_HOST:8787/tcp`

### Minimal usage pattern (conceptual)

This repository does not ship cluster bootstrap scripts. Conceptually, you would:
1) Start a scheduler on a reachable host (e.g., the machine with IP/DNS `SCHEDULER_HOST`).
2) Start workers on each worker machine, pointing them at the scheduler address.
3) Run your driver script (the Python `-c` blocks in this README) but connect to the scheduler by passing:
   - `scheduler_address="tcp://SCHEDULER_HOST:8786"` (example)

The `run_bucketed_anomaly_training_dask(...)` function is designed so that the only refactor is the `Client(...)` creation; the bucketed anomaly training logic remains the same.

---

## Conceptual overview (what the anomaly model does)

### Inputs (time series)
For each grid cell `ID` and date `FECHA`, the pipeline expects daily parquet inputs for:
- `td`  (dewpoint) stored as `Value` → renamed to `TD`
- `tmin_v12` (minimum temperature, PISCOt v1.2; or `tmin_v11` for v1.1) stored as `Value` → renamed to `TMIN`

Required columns in the parquet inputs:
- `ID` (grid cell / location identifier)
- `FECHA` (date)
- `Value` (numeric value)

Typical monthly file convention used by the original pipeline:
- `{base_path}/td/Outputs/td_daily_YYYY_MM.parquet`
- `{base_path}/tmin_v12/Outputs/tmin_v12_daily_YYYY_MM.parquet`
  - also supports `{variable}_daily_YYYY_MM.parquet`

### Step 1 — Daily climatology per (ID, doy)
For each `ID` and each day-of-year `doy ∈ [1..366]`, compute:
- `TD_clim(ID, doy)` = mean daily TD across training years on that DOY
- `TMIN_clim(ID, doy)` = mean daily TMIN across training years on that DOY

The climatology is stored as:
- `daily_climatology.parquet` with columns: `ID`, `doy`, `TD_clim`, `TMIN_clim`

### Step 2 — Convert to anomalies
For each observation:
- `TD_anom = TD - TD_clim(ID, doy)`
- `TMIN_anom = TMIN - TMIN_clim(ID, doy)`

Create lag features (time-lagged anomalies):
- `TD_anom_lag1 = TD_anom(t-1)`
- `TD_anom_lag2 = TD_anom(t-2)`
- `TMIN_anom_lag1 = TMIN_anom(t-1)`

### Step 3 — Local linear regression per DOY (per grid cell)
For each grid cell `ID` and each target DOY `doy_target`, fit a weighted regression in a DOY neighborhood:

Model form (per `ID`, `doy_target`):
- `TD_anom ≈ const_anom
            + TMIN_anom * TMIN_anom_coeff
            + TD_anom_lag1 * TD_anom_lag1
            + TD_anom_lag2 * TD_anom_lag2
            + TMIN_anom_lag1 * TMIN_anom_lag1`

Neighborhood selection:
- training samples are taken from a circular DOY window around `doy_target` of half-width `h`
- circular distance is used: `dist = min(|doy - doy_target|, 366 - |doy - doy_target|)`

Weights:
- default: **Tricube kernel**, matching the notebook implementation:
  - `w = (1 - |dist/h|^3)^3` for `dist ≤ h`, else 0
- optionally: Gaussian kernel

Fitting:
- weighted least squares (WLS)

Output coefficients (per `ID`, `doy`):
- `const_anom`
- `TMIN_anom_coeff`
- `TD_anom_lag1`
- `TD_anom_lag2`
- `TMIN_anom_lag1`
- plus diagnostics such as `r_squared_anom` (when available)

These coefficients are stored in:
- `llr_coeffs_anomaly_dataset/id_bucket=*/coeffs.parquet`

---

## Running at scale (Dask-oriented execution)

The original implementation was designed to run for *many* IDs and *all* DOYs, which is expensive. The practical approach is:

1. **Precompute climatology once** for the training period.
2. Build a **bucketed merged training dataset** once from monthly TD/TMIN inputs.
3. Shard climatology by the same ID buckets.
4. Run anomaly training in parallel across buckets.

Typical pattern:
- Use a Dask scheduler (`dask.distributed.Client`)
- Submit one task per bucket
- Each task reads one bucket shard, fits all IDs in that bucket, and writes `coeffs.parquet`
- Store structured worker failures alongside the coefficient dataset

Why Dask helps:
- parallelizes across spatial buckets
- isolates failures (a single ID failure should not kill the full run)
- supports batching to control scheduler pressure

Key knobs you typically tune:
- number of workers / threads per worker
- number of ID buckets
- bucket submit batch size (to manage scheduler overhead)
- neighborhood half-width `h`
- minimum samples per DOY regression

> This repository uses **Dask-only orchestration** for bucket-based training runs. The core regression math remains in `tdew_estimation.anomaly_train`, while bucket preparation and orchestration live in `tdew_estimation.bucketed_data` and `tdew_estimation.anomaly_dask`.

---

## Outputs / artifacts (what you should expect on disk)

Within your `results_dir` you typically have:

### 1) Climatology
- `daily_climatology.parquet`
  - columns: `ID`, `doy`, `TD_clim`, `TMIN_clim`

### 2) Anomaly coefficients
- `llr_coeffs_anomaly_dataset/`
  - one parquet file per bucket: `id_bucket=*/coeffs.parquet`
  - key columns: `ID`, `doy`
  - coefficient columns: `const_anom`, `TMIN_anom_coeff`, `TD_anom_lag1`, `TD_anom_lag2`, `TMIN_anom_lag1`
  - diagnostics: e.g., `r_squared_anom`

### 3) Prepared training shards
- `bucketed_training_data/id_bucket=*/train_YYYY.parquet`
  - merged yearly TD/TMIN training rows partitioned by `id_bucket`

### 4) Climatology shards
- `climatology_by_bucket/id_bucket=*/climatology.parquet`
  - one climatology parquet per bucket

### 5) Failure logs
- `anomaly_failures/id_bucket=*/failures.parquet`
  - structured bucket / ID / DOY failures recorded during training

---

## Code organization (extracted modules)

The extracted, path-agnostic modules live under `tdew_estimation/`:

- `grid.py`
  - loads grid IDs from a grid file (DBF/SHP/GPKG/GeoJSON/CSV/Parquet)
  - computes `EXPECTED_COUNT` (number of unique IDs)

- `checks.py`
  - detects incomplete DOYs in a coefficient parquet file or a bucketed coefficient dataset using “Option A”
  - produces a copy-paste-friendly `DOYS_TO_FIX` list

- `anomaly_train.py`
  - core anomaly coefficient training logic
  - supports fitting from already prepared TD/TMIN frames and restricting to a subset of DOYs

- `patch_coeffs.py`
  - patches a single coefficient parquet or a bucketed coefficient dataset by replacing only the DOYs being repaired

- `anomaly_dask.py`
  - Dask-based orchestration for anomaly training at scale
  - runs one task per bucket and writes bucket-local coefficient outputs
  - records structured failure logs
  - includes a helper to rerun only failed/incomplete DOYs into a patch dataset

- `bucketed_data.py`
  - builds the bucketed merged TD/TMIN training dataset
  - shards climatology by the same bucket layout

- `main.py`
  - a lightweight CLI/example entrypoint wiring: detect → retrain DOYs (bucketed Dask) → patch → re-check

---

## Small but practical: repairing failed / incomplete DOYs

Large distributed runs can occasionally produce partial results for some DOYs. The repository supports a lightweight repair strategy:

**Definition (Option A, as used in your workflow):**
For each `doy`, count distinct IDs present in the coefficient table.
If `actual_count != EXPECTED_COUNT`, then that DOY is incomplete and should be retrained.

Repair workflow:
1. Compute `EXPECTED_COUNT` from the grid file.
2. Detect `DOYS_TO_FIX` from `llr_coeffs_anomaly_dataset/`.
3. Retrain anomaly coefficients **only** for those DOYs into a bucketed patch dataset.
4. Patch the base coefficient dataset by replacing those DOYs.
5. Re-check completeness.

This keeps the repair step small and avoids re-running the full 366-DOY training.

---

## Notes / future improvements (not implemented here yet)

- Remote-scheduler support for multi-host Dask runs
- Direct NumPy weighted least-squares to reduce `statsmodels` overhead
- Forecast refactor to use the same bucketed data layout as training
- A dedicated CLI entrypoint (thin layer over the extracted modules)
- Rolling-origin, time-blocked cross-validation on a representative subset of IDs for tuning `h`, kernels, and version-shift corrections
- Testing whether a single global `h` is sufficient or whether broad macro-regions in Peru should use different `h` values, adopting regional bandwidths only if validation shows a clear gain
