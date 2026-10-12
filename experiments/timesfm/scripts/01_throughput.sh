#!/usr/bin/env bash
# Fase 0: coste de la inferencia (celdas/s y VRAM pico) por contexto, horizonte y lote.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.throughput \
  --ids-file "$PANELS/nacional_17041.csv" --cells 32 --out "$OUT/coste_throughput.csv"
