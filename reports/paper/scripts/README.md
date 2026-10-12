# Figure and diagnostic scripts

Reproduce the numbers and figures in `paper.qmd`. Run with the project venv from the repo root
(`PYTHONPATH=$PWD .venv/bin/python reports/paper/scripts/<script>`). All read from
`$RES = /media/ppalacios/Data1/henry_simcast_peru_full/results_tuning` (paths are set at the top of
each script) and are read-only with respect to the data products.

| script | produces |
|---|---|
| `qc_fill.py` | national QC of the filled product: ranges, NaN count, annual means, outlier fractions |
| `make_paper_figs.py` | F1 (seam time series), F2 (mean-Td map), F4 (warm-tail panel) |
| `make_seam_fig.py` | F3 (seam artefact test on full-year windows + natural-variability control); caches per-cell window means to `$RES/tuning/seam_windows_cache.parquet` so replots are fast |
| `make_f5_month_of_year.py` | F5 (warm tail by month of year) from `warm_tail_monthly.json`; no data scan needed |
| `warm_tail_diagnostics.py` | warm-tail diagnostics: per-year and per-month >35 C incidence, Td-vs-Tmin bound violation, effect of capping, run-length clustering; dumps `warm_tail_monthly.json` used to build F5 |
| `november_diagnostics.py` | why the warm tail is a November phenomenon: per-month skill, selected bandwidth by zone and month; output kept in `november_diagnostics_output.txt` |
| `make_f_selection.py` | F0 (selected models: h distribution, h by zone and day of year, predictor retention, skill uplift) |
| `fao56_corrected_baseline.py` | Table: corrected FAO-56 baselines (Allen's -2 C, arid-only and global, best single offset) scored per Thornthwaite moisture class. Reads `$BACKTEST_ROOT` (default `$RES/tuning/backtest_clean`, the leak-free run the paper reports) |
| `excess_bound_eval.py` | Table: the family `Td <= Tmin + k` on the *production* fill -- share of field altered, mean shift, share of >35 C exceedances removed |
| `backtest_clean_run.sh` | the leak-free validation run itself, as executed: `select_backtest` (train-only) then `backtest` then `effect_sizes` for ll1/ll2/ll4 into `$RES/tuning/backtest_clean/`. Every accuracy number in the paper comes from this run |

Selection never sees the withheld years: `backtest_clean_run.sh` selects predictors and bandwidth on
the training years alone. The older `$RES/tuning/backtest/` run, in which selection saw 1981–2016, is
retained only as the leaky arm of the selection-optimism comparison reported in the paper.

These were reconstructed into the repository on 2026-09-07 after the originals were lost from
`/tmp` in a reboot — which is why they now live under version control.

## Map figures

`geo_overlay.py` draws Peru's national and departmental boundaries (GADM 4.1 level 1, in
`../geo/`) over the four figures with a geographic axis: F2, F3, F4 and S4. The outline
carries an argument rather than decorating the figure. The released field covers about twice
the area of Peru, and accuracy degrades with distance from the Peruvian station network the
source product is built on, so the border shows the reader where the errors come from: the
`unsupported` tier, at RMSE 1.724 °C against 0.946 °C inside, and every one of the 132,920
cells carrying a value above 35 °C, lie beyond it.

GADM's extent agrees with the SENAMHI classification shapefile to three decimal places,
which is a useful cross-check of both.
