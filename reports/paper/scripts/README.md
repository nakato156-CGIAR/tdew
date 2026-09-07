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

These were reconstructed into the repository on 2026-09-07 after the originals were lost from
`/tmp` in a reboot — which is why they now live under version control.
