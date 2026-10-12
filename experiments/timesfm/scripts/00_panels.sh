#!/usr/bin/env bash
# Paneles de celdas. Reconstruye los seis paneles y comprueba que coinciden con los usados.
# Los cuatro de $WORK y $RECON se copian alli si faltan; los de reports/ ya estan versionados.
source "$(dirname "$0")/env.sh"
$PY -m experiments.timesfm.scripts.make_panels --out-dir "$WORK/panels_rebuilt" --check
mkdir -p "$RECON/panels"
[ -f "$WORK/panel_436k.csv" ] || cp -f "$WORK/panels_rebuilt/panel_436k.csv" "$WORK/"
[ -f "$WORK/panel_escala_submuestra.csv" ] || cp -f "$WORK/panels_rebuilt/panel_escala_submuestra.csv" "$WORK/"
[ -f "$RECON/panels/ll4_reducido_512.csv" ] || cp -f "$WORK/panels_rebuilt/ll4_reducido_512.csv" "$RECON/panels/"
