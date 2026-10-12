#!/usr/bin/env bash
# Figuras estaticas y pagina interactiva. Ninguno recalcula metricas: leen los CSV publicados.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.make_figures --suffix _limpio --runtime-csv "$WORK/preds_cribado/runtime_ll4.csv"
$PY -m experiments.timesfm.artifact_data --out "$OUT/artifact/datos.js"
