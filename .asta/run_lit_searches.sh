#!/bin/bash
cd /home/ppalacios/Documents/tdew_estimation/tdew_estimation/.claude/worktrees/tdew-gap-fill-resume-7391e5
B=.asta/literature/threads

run() {  # $1=slug  $2=query
  local d="$B/2026-07-22-$1"
  mkdir -p "$d"
  asta literature interactive "$2" --thread-dir "$d" -o "$1.json" --timeout 850 \
      > "$d/run.log" 2>&1
  echo "done: $1 (exit $?)"
}

run tdew-from-tmin "Validity and bias of estimating dew point temperature from daily minimum temperature, the FAO-56 assumption that dewpoint temperature approximately equals daily minimum temperature, documented errors of this assumption in arid, semi-arid and high-elevation mountain regions, and proposed corrections such as aridity-dependent offsets, for estimating vapour pressure, dew point or relative humidity from air temperature." &

run gridded-gapfill-validation "Temporal gap filling, extension and reconstruction of gridded daily meteorological and climate datasets: statistical and machine learning methods, and how such temporal extensions are validated using forward temporal hold-out versus spatial cross-validation, and which baselines are standard such as daily climatology and persistence." &

run dewpoint-limits-amazon "Physical upper limits on dew point temperature and near surface humidity in the humid tropics, wet bulb temperature limits, late dry season Amazon humidity and drought and land atmosphere coupling, and unphysical or oversaturated humidity values produced by statistical humidity estimation models in tropical lowlands." &

run local-regression-selection "Local linear regression on climate anomalies with region specific and season specific selection of predictors and smoothing bandwidth, multitask feature selection for subseasonal climate forecasting such as MultiLLR, and error growth in autoregressive multi step prediction of climate variables." &

wait
echo "ALL SEARCHES COMPLETE"
