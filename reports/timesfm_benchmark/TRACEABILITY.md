# Trazabilidad del benchmark de TimesFM

De dónde sale cada número de este directorio, bajo qué protocolo y cómo se
reproduce. Leer esto antes de citar cualquier cifra de `leaderboard.csv`.

## 1. Protocolo

Fuente única: [`docs/protocol/timesfm_manifest.yaml`](../../docs/protocol/timesfm_manifest.yaml),
congelado el 2026-09-22, bead `tdew-214`.

Addendum del 2026-10-02 (bead `tdew-214.12`):
[`docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`](../../docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml).
El manifiesto original no se modificó. La adenda fija como referencia del rival
`tuned` el run limpio `$RES/tuning/backtest_clean` (selección de recetas solo con
años de entrenamiento, `h` en {7, 11, 15, 21, 31, 45}), con 17.027 celdas, y declara
que las tablas departamental y de escala conservan un `tuned` con selección con
fuga. Los registros de proveniencia calculados contra la referencia limpia citan la
adenda en `manifest_ref`; los anteriores conservan
`docs/protocol/timesfm_manifest.yaml@2026-09-22`.

Los splits no se inventaron para este trabajo: son los mismos que define
`HPC_code_tunning/backtest.py:61-66` y bajo los que Palacios reporta sus cifras.

| split | entrena | predice (oculto) | días |
|---|---|---|---|
| `ll1` | 1981–2015 | 2016 | 366 |
| `ll2` | 1981–2014 | 2015–2016 | 731 |
| `ll4` | 1981–2012 | 2013–2016 | 1.461 |

Reglas que gobiernan la comparación:

- El contexto de TimesFM termina el 31 de diciembre del último año de
  entrenamiento. Ningún valor de Td del bloque oculto entra al contexto ni a la
  climatología.
- La climatología se recalcula con solo los años de entrenamiento de cada split,
  replicando `backtest.train_only_climatology` (`backtest.py:72-79`).
- Tmin del bloque oculto sí se entrega como covariable. Es exógeno, existe en todo
  el rango y es exactamente la información que consume el método de Palacios, que
  también lo usa. Igualar la entrada hace que la comparación mida el modelo.
- `make_positive=False` en todas las corridas.
- Todos los métodos se puntúan sobre la intersección exacta de celdas y días.

### Decisión de diseño que el lector debe conocer

Las variantes (diez al inicio, nueve tras la enmienda del 2026-09-25) se evaluaron
directamente sobre el mismo bloque que después se reporta, por decisión explícita
del usuario. No se usó un fold de desarrollo previo. En consecuencia, la cifra de la
variante ganadora incluye la ventaja de haber probado varias configuraciones contra
el mismo examen. Esa ventaja se mide y se publica junto al resultado
(`cribado_limpio/sesgo_seleccion_ll4.csv`, vigente, y `cribado/sesgo_seleccion_ll4.csv`,
con fuga, más la sección correspondiente del `README.md`), en lugar de
quedar como advertencia sin cuantificar. Palacios hizo la comprobación análoga
sobre su propia reselección de recetas y obtuvo 0,0088 de skill
(`PAPER_PLAN.md:275`).

## 2. Linaje de los datos

```
/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/
├── bucketed_training_data/id_bucket=XXXX/train_YYYY.parquet   (1981-2016, ID/FECHA/TD/TMIN/doy)
│     └── experiments/timesfm/panel.py::build_panel
│           ├── contexto TD 1981..train_end        → contextos de TimesFM
│           ├── climatología por (ID, doy)          → control de paridad y anomalías
│           └── TMIN contexto+horizonte             → covariable futura
│                 └── experiments/timesfm/run.py    → <split>__<variante>.parquet
│                       (ID, FECHA, pred, q10..q90)
├── tuning/backtest_clean/<split>/predictions.parquet        (referencia vigente, 17.027 celdas)
│     (ID, zone_id, FECHA, TD_obs, pred_tuned, pred_clim, pred_tmin, pred_ols)
│     └── experiments/timesfm/evaluate.py           → nacional_limpio/, cribado_limpio/
│     └── experiments/timesfm/merge_predictions.py  → $WORK/backtest_clean_timesfm/<split>/predictions.parquet
│           └── HPC_code_tunning/effect_sizes.py    → effect_sizes_all.csv, figuras
│                 └── experiments/timesfm/publish.py → nacional_limpio/ (copia con proveniencia propia)
├── tuning/backtest/<split>/predictions.parquet              (run con fuga, 17.041 celdas, solo referencia)
│     └── nacional/, cribado/, curva_error_*.csv sin sufijo
└── zone_table.parquet  (2.818.404 IDs → zone_id SENAMHI)
      └── panels/*.csv
```

Los archivos originales bajo `tuning/backtest/` y `tuning/backtest_clean/` no se
modifican. La columna `pred_timesfm` se añade en una copia bajo otra raíz
(`$WORK/backtest_clean_timesfm`).

## 3. Los paneles de celdas

| panel | celdas | archivo | cómo se eligió |
|---|---|---|---|
| cribado | 1.106 | `panels/cribado_estratificado.csv` | hasta 40 celdas por zona SENAMHI sobre las del backtest de Palacios, `numpy.random.default_rng(20260922)` |
| backtest (limpio) | 17.027 | `panels/nacional_17027.csv` | las celdas del run limpio de Palacios (`ID`, `zone_id` de `backtest_clean/ll4`); subconjunto del panel de 17.041 |
| cribado (limpio) | 1.092 | `panels/cribado_estratificado.csv` (1.106 IDs) | intersección del cribado con el run limpio; las 14 celdas restantes se descartan en la unión interna |
| backtest (con fuga) | 17.041 | `panels/nacional_17041.csv` | las celdas del backtest con fuga, sin filtrar; solo referencia |
| departamental | 2.048 | `$WORK/panels/ll4_seed0.csv` | panel `ll4` del protocolo de reconstrucción, 512 por departamento (no los 2.048/departamento del manifiesto: verificado contra `predicciones_largo.parquet` y contra el artefacto, sección "Panel departamental") |
| escala | 436.519 | `Data/silver/department_grid_ids/*.csv` | las cuatro listas completas |
| escala, submuestra puntuada | 61.113 | `$TFM/panel_escala_submuestra.csv` | 14 % de cada departamento, proporcional, que es lo que el método de Palacios alcanzó a cubrir |

El muestreo de 64 buckets de Palacios toca 38 de las 41 zonas SENAMHI en el run con
fuga y 33 en el run limpio. El panel de cribado limpio cubre las 33.

El `tuned` de las tablas departamental y de escala viene de
`HPC_code_tunning.backtest` ejecutado sin `--manifest` (`run_cola_final.sh` y
`run_tuned_escala.sh`), es decir, con `$RES/tuning/manifest.parquet`, cuya selección
de recetas vio los años 1981–2016. **Esas dos tablas no son comparables con las
cifras limpias.** La re-corrida con selección limpia queda
para un punto posterior.

El panel llamado aquí `backtest` no es una muestra del Perú: el marco de muestreo
sortea buckets sobre la caja envolvente del producto PISCO, de modo que 8.755 de
sus 17.027 celdas —el 51,4 %— caen en Brasil, Bolivia, Ecuador o Colombia
(8.272 dentro del Perú). Verificado con `shapely.contains_xy` sobre los contornos
departamentales; las 14 celdas ajenas al run limpio estaban todas dentro del Perú.
Bead `tdew-214.8`.

## 4. Los rivales y qué mide cada uno

| método | columna | qué hipótesis prueba |
|---|---|---|
| `climatology` | `pred_clim` | el piso: ¿aporta algo más que la media histórica del día del año? |
| `td_eq_tmin` | `pred_tmin` | ¿basta con usar Tmin sin transformar? |
| `zone_ols` | `pred_ols` | ¿basta una recta por zona climática? |
| `tuned` | `pred_tuned` | el método del paper: regresión local ponderada por `(ID, doy)`, kernel tricube, receta por zona × día del año, pronóstico autorregresivo |
| `timesfm:<variante>` | `pred` / `pred_timesfm` | un modelo de fundación sin entrenar, con la misma información de entrada |
| `tcn` | — | la TCN de reconstrucción continua, solo en el panel departamental |

`zone_ols` se ajusta con estadísticos suficientes acumulados sobre las celdas de
la corrida. Si el backtest se restringe con `--ids-csv`, esa línea base se reajusta
solo con las celdas restringidas y deja de ser comparable con la corrida nacional;
climatología y `tuned` son por celda y no se ven afectados.

## 5. Controles ejecutados antes de comparar nada

| control | qué verifica | resultado |
|---|---|---|
| reproducción de la cifra publicada (limpia) | RMSE de `tuned` y `climatology` en `ll4` de `nacional_limpio/metrics_all.csv` contra `backtest_clean/metrics_all.csv` | 1,2279 y 1,5352, n = 24.876.447, diferencia absoluta 0 en los tres splits |
| cobertura de la fusión (limpia) | celdas de la referencia y de TimesFM en la unión interna | 17.027 de 17.027; 14 celdas de TimesFM fuera de la referencia |
| reproducción de la cifra con fuga | RMSE de `tuned` y `climatology` en `ll4` desde `tuning/backtest` | 1,219433 y 1,535218, contra 1,219 y 1,535 de `PAPER_PLAN.md:263-268` |
| paridad de climatología | `TD_clim` del panel contra `pred_clim` de Palacios, mismas `(ID, FECHA)` | `max\|diff\| = 0,0` |
| paridad de Tmin y Td observado | `tmin_hold` y `td_hold` contra `Tmin_hold` y `TD_obs` | `max\|diff\| = 0,0` en ambos |
| no-fuga | último día del contexto y primero del bloque oculto; NaN | 2012-12-31 / 2013-01-01; cero NaN |
| horizonte no alterado | días devueltos por celda y ancho de la covariable | 1.461 exactos, de 2013-01-01 a 2016-12-31 |
| recorte de negativos desactivado | predicciones negativas en celdas de Cusco | 11.524 de 99.348 (11,6 %), mínimo −6,83 °C |
| cruce de cuantiles | monotonía de los nueve deciles | 0 cruces |
| regresión de `effect_sizes.py` | que la parametrización del método focal no cambie los números previos | idénticos a `effect_sizes_all.csv` original |
| pruebas unitarias | panel sin fuga, armado de entradas y métricas probabilísticas | 26 pruebas, todas pasan |

### Defecto encontrado y corregido durante la ejecución

En las variantes cuyo objetivo es la anomalía de Td, la predicción puntual se
devolvía a grados sumando la climatología, pero los nueve cuantiles se escribían
sin esa corrección. El resultado era que `TD_obs`, en grados, se comparaba contra
cuantiles en anomalía: el CRPS aproximado de `tmin_anom_full` salía 10,04 y su
cobertura del intervalo 80 % salía 0,085, cuando la de las variantes sobre Td crudo
salía 0,83. Las métricas puntuales —RMSE, MAE, sesgo, r— nunca estuvieron
afectadas, porque usan la columna `pred`, que sí llevaba la corrección.

Se corrigió en `experiments/timesfm/run.py::to_physical`, que ahora acepta tanto la
matriz puntual como el cubo de cuantiles, y se añadió la prueba
`test_to_physical_also_converts_the_quantile_cube`. Las dos variantes sobre
anomalía se volvieron a correr con el código corregido antes de elegir ninguna
ganadora.

## 6. Cómo reproducirlo

### Referencia limpia (vigente)

```bash
RES=/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning
WORK=/home/cvelasquez/tdew_timesfm
ADD=docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml
OUT=reports/timesfm_benchmark

# Todos los comandos se ejecutan desde la raíz del repositorio.
# Panel: IDs y zonas de backtest_clean/ll4 (17.027 celdas)
RES=$RES OUT=$OUT uv run python - <<'PY'
import os
import pandas as pd
d = pd.read_parquet(os.environ["RES"] + "/tuning/backtest_clean/ll4/predictions.parquet",
                    columns=["ID", "zone_id"])
d.drop_duplicates().sort_values("ID").to_csv(
    os.environ["OUT"] + "/panels/nacional_17027.csv", index=False)
PY

# Fusión con TimesFM (intermedio en $WORK; no se escribe bajo $RES)
uv run python -m experiments.timesfm.merge_predictions \
  --predictions-dir $WORK/preds_nacional --variant tmin_anom_full --splits ll1,ll2,ll4 \
  --backtest-root $RES/tuning/backtest_clean --out-root $WORK/backtest_clean_timesfm \
  --panel-id nacional_17027_limpio --bead-id tdew-214.12

# Escalera por bloque, desglose por zona y curva de error acumulado
uv run python -m experiments.timesfm.evaluate \
  --predictions-dir $WORK/preds_nacional --splits ll1,ll2,ll4 --by-zone \
  --backtest-root $RES/tuning/backtest_clean --out-dir $OUT/nacional_limpio \
  --panel-id nacional_17027_limpio --panel-file $OUT/panels/nacional_17027.csv \
  --bead-id tdew-214.12 --growth-curve ll4 --growth-variant tmin_anom_full \
  --growth-curve-out $OUT/curva_error_nacional_limpio.csv

# Tamaños de efecto y curva de horizonte
uv run python -m HPC_code_tunning.effect_sizes \
  --backtest-root $WORK/backtest_clean_timesfm --splits ll1,ll2,ll4 \
  --focal timesfm --lead-time-methods timesfm,tuned --timesfm-variant tmin_anom_full \
  --n-boot 1000 --n-perm 5000 --seed 0 --panel-id nacional_17027_limpio \
  --panel-file $OUT/panels/nacional_17027.csv --manifest-ref $ADD --bead-id tdew-214.12 \
  --notes "backtest_root deriva de tuning/backtest_clean (merge con TimesFM tmin_anom_full)"

# Publicación con proveniencia propia (copia los CSV y clona sus filas del registro)
uv run python -m experiments.timesfm.publish \
  --src $WORK/backtest_clean_timesfm/metrics_all.csv $WORK/backtest_clean_timesfm/effect_sizes_all.csv \
  --dst-dir $OUT/nacional_limpio
cp -f $WORK/backtest_clean_timesfm/lead_time_curve.png $OUT/nacional_limpio/
for s in ll1 ll2 ll4; do for f in $WORK/backtest_clean_timesfm/$s/*.png; do
  cp -f "$f" "$OUT/nacional_limpio/${s}_$(basename "$f")"; done; done

# Cribado limpio (1.092 celdas comunes) y figuras con sufijo
uv run python -m experiments.timesfm.evaluate \
  --predictions-dir $WORK/preds_cribado --splits ll4 --by-zone \
  --backtest-root $RES/tuning/backtest_clean --out-dir $OUT/cribado_limpio \
  --panel-id cribado_1092_limpio --panel-file $OUT/panels/cribado_estratificado.csv \
  --bead-id tdew-214.12 --growth-curve ll4 --growth-variant tmin_anom_full \
  --growth-curve-out $OUT/curva_error_cribado_limpio.csv \
  --notes "panel_file son las 1106 celdas del cribado; se puntuan las 1092 comunes con backtest_clean (14 descartadas)"
uv run python -m experiments.timesfm.make_figures --suffix _limpio

# Página interactiva (el worktree puede no tener Data/; --silver del checkout que sí la tenga)
uv run python - <<'PY'
from pathlib import Path
from experiments.timesfm import artifact_data
artifact_data.build(Path("reports/timesfm_benchmark/artifact/datos.js"), silver=Path("Data/silver"))
PY
```

El recuento de celdas dentro y fuera del Perú (8.272 y 8.755 sobre las 17.027) sale de
`artifact_data.build_layers` (`shapely.contains_xy` contra los contornos
departamentales) y queda en `meta.muestreoDentro`/`muestreoFuera` de `datos.js`.

`sesgo_seleccion_*.csv` no se genera para el panel nacional: con una sola variante no
hubo selección y la dispersión sería cero por construcción. El cribado limpio sí lo
genera (nueve variantes). La variante retirada `tmin_td_25` se omite en la
puntuación aunque su parquet siga en `$WORK/preds_cribado`.

Las filas de `reports/metric_provenance.jsonl` de estas corridas guardan la ruta
de los CSV publicados relativa al repositorio y la de los intermedios (`$WORK`)
absoluta. `git_commit` registra el `HEAD` en el momento de la corrida: si el código
tenía cambios sin confirmar, ese commit no reproduce la fila por sí solo.

### Referencia con fuga (histórica)

Estos comandos reproducen las cifras con fuga y por eso fijan `--backtest-root` al
run anterior:

```bash
# Entorno (TimesFM entra por el extra 'timesfm' del proyecto)
uv sync --extra timesfm --extra deep

# Fase 0 — costo
uv run python -m experiments.timesfm.throughput \
  --ids-file reports/timesfm_benchmark/panels/nacional_17041.csv \
  --cells 32 --out reports/timesfm_benchmark/coste_throughput.csv

# Fase 1 — las diez variantes sobre el panel de cribado
uv run python -m experiments.timesfm.run --variants all --split ll4 \
  --ids-file reports/timesfm_benchmark/panels/cribado_estratificado.csv \
  --out-dir "$WORK/preds_cribado" --batch-size 16 --cells-per-batch 256
uv run python -m experiments.timesfm.evaluate \
  --predictions-dir "$WORK/preds_cribado" --splits ll4 \
  --backtest-root "$RES/tuning/backtest" \
  --out-dir reports/timesfm_benchmark/cribado --by-zone

# Fase 2 — la ganadora sobre las 17.041 celdas, tres splits
uv run python -m experiments.timesfm.run --variants "$BEST" --split ll4 \
  --ids-file reports/timesfm_benchmark/panels/nacional_17041.csv \
  --out-dir "$WORK/preds_nacional" --batch-size 16 --cells-per-batch 512
uv run python -m experiments.timesfm.merge_predictions \
  --predictions-dir "$WORK/preds_nacional" --variant "$BEST" \
  --splits ll1,ll2,ll4 --backtest-root "$RES/tuning/backtest" \
  --out-root "$RES/tuning/backtest_timesfm"
uv run python -m HPC_code_tunning.effect_sizes \
  --backtest-root "$RES/tuning/backtest_timesfm" --splits ll1,ll2,ll4 \
  --focal timesfm --lead-time-methods timesfm,tuned

# Fase 4 — el método de Palacios sobre las celdas departamentales
uv run python -m HPC_code_tunning.backtest --base "$RES" --splits ll4 \
  --n-buckets 8192 --ids-csv Data/silver/department_grid_ids/*.csv \
  --out-root "$RES/tuning/backtest_depts"
```

`$RES` es `/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning` y
`$WORK` es `/home/cvelasquez/tdew_timesfm`.

## 7. Dónde queda registrada cada corrida

- Beads: `tdew-214` y sus subtareas por fase, `tdew-214.8` sobre el marco de muestreo y
  `tdew-214.12` sobre la re-puntuación contra el run limpio (`PLAN_1.md`).
- Notion: fila `Benchmark TimesFM vs. metodo Palacios y TCN` en el Gantt Chart del
  Timeline Planner, con `Bead ID = tdew-214`.
- MLflow: experimento `tdew-timesfm`.
- Tiempos de cada corrida: `runtime_<split>.csv` en el directorio de predicciones.
- Pasada de escala: `$TFM/logs_escala.log` y `$TFM/preds_escala/runtime_ll4.csv`;
  436.519 celdas en 85.686 s (23 h 48 min) a 5,094 celdas/s, lote efectivo 16.
  Puntuada con `python -m experiments.timesfm.escala --ids-csv
  $TFM/panel_escala_submuestra.csv`, que restringe la salida de TimesFM a las
  celdas del rival; como la unión es interna, el resultado es idéntico a puntuar
  sin filtrar y evita construir un índice de 637,8 millones de entradas.

## 8. Cambios hechos a código existente

Dos archivos del pipeline de Palacios se tocaron, de forma que los resultados
previos siguen reproduciéndose:

- `HPC_code_tunning/effect_sizes.py`: `METHOD_COLS` incorpora `timesfm`; los
  métodos cuya columna falta en un archivo se omiten, de modo que los
  `predictions.parquet` originales de cuatro métodos siguen funcionando. El método
  focal, antes fijo en `tuned`, ahora es un parámetro (`--focal`), y la curva de
  horizonte admite varias series (`--lead-time-methods`). Las columnas
  `rmse_tuned` y `frac_cells_tuned_wins` se conservan como alias de las nuevas
  `rmse_focal` y `frac_cells_focal_wins`. Verificado: los tres valores de `ll4`
  salen idénticos a los del `effect_sizes_all.csv` publicado.
- `HPC_code_tunning/backtest.py`: opción `--ids-csv` que restringe la corrida a una
  lista explícita de celdas filtrando `id_to_zone`, del que ya dependía todo el
  recorrido. Ninguna otra línea cambia y las diez pruebas del módulo siguen
  pasando.

## 9. Nota sobre uso de IA

La implementación, la ejecución y el análisis de este benchmark se hicieron con
asistencia de Claude Code (Claude Opus 5). Todas las cifras provienen de
ejecuciones reales sobre los datos del proyecto y los controles de la sección 5
son reproducibles. Las decisiones de protocolo —qué variantes probar, sobre qué
bloque evaluarlas y qué rivales incluir— las tomó el usuario. Conviene validar las
conclusiones con el equipo antes de tomarlas como definitivas, conforme a la
política de uso de IA del CIP.
