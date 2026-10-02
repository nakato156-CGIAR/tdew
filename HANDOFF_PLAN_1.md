# HANDOFF_PLAN_1: re-puntuación de TimesFM contra `backtest_clean`

Fecha: 2026-10-02. Bead: `tdew-214.12` (hijo de `tdew-214`). Branch: `tdew-214-timesfm-limpio`, creada desde `tdew-u8m-paper-timesfm-narrative` (`82d4798`). Worktree: `.claude/worktrees/tdew-214-timesfm-limpio`. Plan de origen: `PLAN_1.md`. No se hicieron commits ni push.

## Estado

Pasos 1 a 9 de `PLAN_1.md` ejecutados. Cada hito tuvo revisión independiente de un subagente Opus y sus hallazgos se corrigieron. El Paso 10 se cumplió en lo que corresponde (bead creado y notas en `tdew-214.8`); el ítem «agregar entrada a `PAPER_PLAN.md`» se omitió por decisión del usuario, porque ese archivo es de Palacios.

## Cifras vigentes (run limpio, 17.027 celdas)

| bloque | TimesFM | `tuned` | climatología | ΔRMSE vs. `tuned` |
|---|---|---|---|---|
| `ll1` | 1,1736 | 1,2538 | 1,6803 | +0,0802 |
| `ll2` | 1,1533 | 1,2765 | 1,6667 | +0,1231 |
| `ll4` | 1,1536 | 1,2279 | 1,5352 | +0,0743 |

Las filas de `tuned` y climatología coinciden con `backtest_clean/metrics_all.csv` con diferencia absoluta cero. 8.755 de las 17.027 celdas (51,4 %) caen fuera del Perú; las 14 celdas que el run limpio no tiene estaban todas dentro. El panel limpio cubre 33 de 41 zonas. El cribado limpio (1.092 celdas, nueve variantes) mantiene el orden de las dos primeras variantes.

## Qué se cambió

- Código: `evaluate.py` (constantes `LEAKY_`/`CLEAN_BACKTEST_ROOT`, `backtest_notes`, `manifest_ref_for`, `--growth-curve`, `--notes`, `--manifest-ref`, omisión de variantes retiradas, sin `sesgo_seleccion` con una sola variante, rivales por zona una sola vez); `merge_predictions.py` (estadísticas de celdas descartadas); `effect_sizes.py` (`--manifest-ref`, `--notes`, n_boot/n_perm/seed en notas); `publish.py` nuevo; `make_figures.py` (`--suffix`); `plots.py` (`cost_frame`); `artifact_data.py` (rutas `_limpio`, paridad); `tdew_estimation/provenance.py` (`resolve_recorded_path`); `departamental.py` (`--backtest-predictions` obligatorio).
- Datos y reportes nuevos: `reports/timesfm_benchmark/{nacional_limpio,cribado_limpio,curva_error_*_limpio.csv,panels/nacional_17027.csv,figs/*_limpio.png}`, `artifact/{index.html,datos.js}` actualizados, `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`.
- Documentos: `README.md`, `TRACEABILITY.md` (§6 con los comandos limpios y los históricos), `limitaciones.md` (limitación 12) y `experiments/timesfm/README.md`.
- Intactos: `nacional/`, `cribado/`, `departamental/`, `escala/`, `curva_error_{nacional,cribado}.csv`, figuras sin sufijo, `timesfm_manifest.yaml`, `PAPER_PLAN.md` y todo `$RES`.

## Pendientes y advertencias

1. **Commit sin hacer.** Las filas nuevas de `reports/metric_provenance.jsonl` registran `git_commit=82d4798` (el `HEAD` de partida), pero el código que las generó no estaba confirmado. Tras confirmar los cambios conviene regenerar el panel nacional y el cribado con los comandos de `TRACEABILITY.md` §6, partiendo del registro de `HEAD` (`git checkout reports/metric_provenance.jsonl`) para no duplicar filas.
2. **Rutas del registro.** Las filas de `evaluate`/`merge`/`effect_sizes` guardan rutas absolutas del worktree y las de `publish` guardan rutas relativas al repo. `resolve_recorded_path` las reancla bajo `reports/` al fusionar, de modo que `tests/test_metric_provenance.py` debería pasar en el checkout principal.
3. **Dos tests fallan en este worktree** (`predicciones_largo.parquet` departamental): ese parquet no está trackeado en git y solo existe en el checkout principal. No se relaciona con estos cambios.
4. **`datos.js` se regeneró** con `artifact_data.build(..., silver=<Data/silver del checkout principal>)`, porque el worktree no tiene `Data/` (DVC).
5. **Departamental y escala** conservan un `tuned` con selección con fuga (manifiesto de recetas con los años 1981–2016). Quedan marcadas como no comparables en el README, en `TRACEABILITY.md`, en `limitaciones.md` y en la página interactiva. La re-corrida de Palacios con selección limpia queda para un punto posterior.
6. **Limitaciones estadísticas ya anotadas:** los intervalos bootstrap tratan las celdas como independientes; el ΔRMSE es diferencia de RMSE agregado mientras que `p`, d de Cohen y celdas ganadas usan los ΔRMSE por celda.
7. **`PAPER_PLAN.md` no se tocó.** Si Palacios quiere anotar el cambio, texto propuesto (en inglés, como el resto de su bitácora):

   > 2026-10-02 — TimesFM benchmark re-scored against the clean run (bead `tdew-214.12`, plan `PLAN_1.md`). The TimesFM-vs-Palacios comparison moved from `$RES/tuning/backtest` (recipe selection saw 1981–2016) to `$RES/tuning/backtest_clean` (17,027 cells, 33 of 41 zones). No TimesFM inference was re-run. ll4: TimesFM 1.1536, `tuned` 1.2279, climatology 1.5352; ΔRMSE vs `tuned` +0.0743 (was +0.0658). Outputs under `reports/timesfm_benchmark/*_limpio/`. Departamental and scale tables still use the leaky `tuned` and are flagged as not comparable. Addendum: `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`.

## Uso de IA

Implementación, ejecución y revisiones hechas con asistencia de Claude Code. Las revisiones por hito las hicieron subagentes de IA sin contexto del autor; conviene que un experto del tema valide las cifras y los textos, conforme a la política de uso de IA del CIP.
