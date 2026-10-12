# PLAN_1: re-puntuación de TimesFM contra el run limpio (`backtest_clean`)

Versión final. Fecha: 2026-10-02. Bead padre: `tdew-214` (se propone una subtarea nueva para este punto).

## Experimentos que cubre este plan

Los códigos E# son los de la lista de experimentos del paper de Palacios (`reports/paper/paper.qmd`), numerados E1–E16 para esta comparación.

| # | Experimento (en el paper) | Qué mide |
|---|---|---|
| E2 | Escalera de RMSE vs. climatología, Td=Tmin y zone OLS (`tbl-ladder`, `fig-ladder`) | RMSE en los bloques ll1, ll2 y ll4 (se oculta 1, 2 y 4 años), con skill vs. climatología |
| E3 | Tamaños de efecto (`tbl-effects`) | ΔRMSE pareado por celda, intervalo por bootstrap de ubicación, % de celdas ganadas, d de Cohen y p de permutación |
| E4 | Curva de lead time (`fig-leadtime`) | Skill vs. horizonte de 1, 2 y 4 años (cuánto decae el acierto al alargar el hueco) |

## 0. Decisiones tomadas

1. **Ubicación de los resultados.** Los resultados limpios van a directorios y archivos nuevos con sufijo `_limpio` (`nacional_limpio/`, `cribado_limpio/`, `curva_error_nacional_limpio.csv`). Los resultados con fuga quedan donde están, anotados. No se reescriben rutas ni registros de proveniencia.
2. **README del benchmark.** Se reportan solo las cifras del run limpio. Una subsección breve de referencia conserva las cifras con fuga y explica la razón del cambio.
3. **Departamental y escala.** El `tuned` de ambas tablas usa selección con fuga. Se anota de forma visible en el README y en `TRACEABILITY.md` que no son comparables con las cifras limpias. La re-corrida de Palacios sobre esas celdas queda para un punto posterior.
4. **Cribado.** Se re-puntúa contra el run limpio y se publica en `cribado_limpio/` (1.092 celdas). El paso es obligatorio.
5. **Manifiesto del protocolo.** `docs/protocol/timesfm_manifest.yaml` no se modifica. Un addendum fechado, en archivo aparte, registra la nueva referencia (17.027 celdas, 33 zonas).

## 1. Objetivo

Reemplazar, como referencia de comparación, el run de Palacios con fuga (`$RES/tuning/backtest`) por el run limpio que usa el paper (`$RES/tuning/backtest_clean`). El cambio se aplica a la escalera de RMSE (E2), a los tamaños de efecto (E3) y a la curva de horizonte (E4).

No se re-corre inferencia de TimesFM. Se reutilizan las predicciones de la variante `tmin_anom_full` en `/home/cvelasquez/tdew_timesfm/preds_nacional/{ll1,ll2,ll4}__tmin_anom_full.parquet` y las del cribado en `/home/cvelasquez/tdew_timesfm/preds_cribado/`. Los resultados con fuga se conservan sin modificar, como referencia.

## 2. Alcance

Entra en este punto:

- E2: escalera de RMSE para `ll1`, `ll2` y `ll4`, con `leaderboard.csv`, `metrics_all.csv` y `metrics_by_zone.csv` sobre las celdas del run limpio.
- E3: tamaños de efecto de TimesFM contra climatología, Td=Tmin, `zone_ols` y `tuned`. Se usa bootstrap por ubicación (1.000 remuestreos) y permutación por cambio de signo (5.000), con semilla 0, igual que `backtest_clean_run.sh`.
- E4: curva de horizonte entre bloques (`lead_time_curve.png`) y curva de error acumulado día a día en `ll4`.
- Re-puntuación del cribado (1.106 celdas de origen, 1.092 en el run limpio).
- Corrección de los valores por defecto del código que apuntan al run con fuga.
- Anotación de los artefactos publicados que no se regeneran (departamental, escala).
- Addendum del manifiesto, proveniencia y tests.

## 3. Pre-condiciones verificadas

Verificadas con lecturas reales, sin escribir en `$RES`:

| Hecho | Evidencia |
|---|---|
| El run limpio tiene 17.027 celdas por split. Las predicciones de TimesFM tienen 17.041. | `backtest_clean/ll1/predictions.parquet`: 17.027 IDs, 6.231.882 filas. `preds_nacional/ll1__tmin_anom_full.parquet`: 17.041 IDs, 6.237.006 filas. |
| El run limpio es subconjunto estricto de las celdas de TimesFM. | `set(limpio) - set(timesfm) = 0`. |
| La unión por `(ID, FECHA)` es uno a uno y deja 17.027 celdas. | `merge(..., validate="one_to_one")` pasó. |
| Climatología y Td observado son idénticos entre el run limpio y el run con fuga. | `max\|diff\| = 0,0` en ambas columnas. |
| No hay NaN en `TD_obs` ni en `pred_tuned` del run limpio. | Conteo = 0. |
| Las cifras de `tuned` y climatología sobre la unión coinciden con las del paper. | `ll4`: `tuned` 1,22793 y clima 1,53517, ambos con n=24.876.447, igual que `backtest_clean/metrics_all.csv`. |
| Las 14 celdas extra del run con fuga están todas en el panel de cribado. | Del cribado (1.106), 1.092 están en el run limpio. |
| El `tuned` departamental y el de escala usan selección con fuga. | `run_cola_final.sh` y `run_tuned_escala.sh` llaman a `HPC_code_tunning.backtest` sin `--manifest`. Eso usa `$RES/tuning/manifest.parquet` (`backtest.py:449,472`) con `--h-grid` por defecto `7,11,15,21`. |
| Hay espacio en disco. | 320 GB libres. |

Valores esperados tras la re-puntuación, calculados en memoria con `tmin_anom_full`:

| bloque | TimesFM | tuned | clima | ΔRMSE vs. tuned (con fuga → limpio) |
|---|---|---|---|---|
| `ll1` | 1,1736 | 1,2538 | 1,6803 | 0,0883 → ≈0,080 |
| `ll2` | 1,1533 | 1,2765 | 1,6667 | 0,1209 → ≈0,123 |
| `ll4` | 1,1536 | 1,2279 | 1,5352 | 0,0658 → ≈0,074 |

La ventaja de TimesFM sobre `tuned` crece en `ll2` y `ll4`. En `ll1` baja, porque la rejilla ampliada de `h` mejora a `tuned` en ese bloque.

## 4. Principio de no sobrescritura

- No se escribe nada bajo `$RES`. Los archivos de ppalacios quedan intactos, incluidos `backtest_timesfm/` y `backtest_clean/`.
- Las salidas intermedias van a `$WORK/backtest_clean_timesfm/{ll1,ll2,ll4}/` (con `$WORK=/home/cvelasquez/tdew_timesfm`).
- Las salidas publicadas van a `reports/timesfm_benchmark/` con sufijo `_limpio`. Los directorios `nacional/` y `cribado/` y los CSV `curva_error_cribado.csv` y `curva_error_nacional.csv` no se tocan ni se renombran.
- `reports/metric_provenance.jsonl` es de solo adición y guarda rutas absolutas en `output_files`. Se agregan registros nuevos con `panel_id` propio. Los registros con fuga permanecen.
- `git diff` sobre las rutas con fuga debe quedar vacío, salvo las notas de referencia del paso 9 en README y TRACEABILITY.

## 5. Pasos

**Paso 1. Constantes de raíz de backtest (código).**
- En `experiments/timesfm/evaluate.py` se definen `LEAKY_BACKTEST_ROOT` (la ruta actual) y `CLEAN_BACKTEST_ROOT` (`.../tuning/backtest_clean`). `DEFAULT_BACKTEST_ROOT` pasa a ser la limpia.
- `experiments/timesfm/merge_predictions.py:31` importa la constante de `evaluate`, sin mantener copia propia.
- `experiments/timesfm/departamental.py:26,170` importa `DEFAULT_BACKTEST_ROOT`. El `tuned` departamental sale de `backtest_panel_dept`, no del backtest nacional. Para que el default nuevo no se aplique en silencio a datos que no corresponden, `--backtest-predictions` pasa a ser obligatorio y la ayuda del argumento advierte que el `tuned` departamental usa selección con fuga.
- `experiments/timesfm/artifact_data.py:113`: la capa de muestreo lee `tuning/backtest/ll4/predictions.parquet`. Se redirige a la raíz limpia (ver paso 7).
- Cada CLI registra en `notes` la raíz de backtest usada.

**Paso 2. Fusión con el run limpio.**
```
uv run python -m experiments.timesfm.merge_predictions \
  --predictions-dir $WORK/preds_nacional --variant tmin_anom_full \
  --splits ll1,ll2,ll4 \
  --backtest-root $RES/tuning/backtest_clean \
  --out-root $WORK/backtest_clean_timesfm \
  --panel-id nacional_17027_limpio
```
- `merge_split` informa también las celdas de TimesFM descartadas por no estar en la referencia (esperado: 14). Hoy `cells_lost` se calcula solo del lado de la referencia y daría 0 sin mencionarlas.
- Los tres splits van en una sola invocación para que `metrics_all.csv` salga concatenado. El problema de sobrescritura por split, registrado en PAPER_PLAN, no se repite.

**Paso 3. E2: escalera y desglose por zona.**
```
uv run python -m experiments.timesfm.evaluate \
  --predictions-dir $WORK/preds_nacional --splits ll1,ll2,ll4 --by-zone \
  --backtest-root $RES/tuning/backtest_clean \
  --out-dir reports/timesfm_benchmark/nacional_limpio \
  --panel-id nacional_17027_limpio \
  --panel-file reports/timesfm_benchmark/panels/nacional_17027.csv
```
- `panels/nacional_17027.csv` (columnas `ID`, `zone_id`) se genera desde `backtest_clean/ll4/predictions.parquet` y entra en `EXCLUDED_FILES` como los otros paneles.
- `sesgo_seleccion_*` no se recalcula para el panel nacional, que tiene una sola variante. Se documenta la omisión.

**Paso 4. E3: tamaños de efecto.**
```
uv run python -m HPC_code_tunning.effect_sizes \
  --backtest-root $WORK/backtest_clean_timesfm --splits ll1,ll2,ll4 \
  --focal timesfm --lead-time-methods timesfm,tuned \
  --timesfm-variant tmin_anom_full --n-boot 1000 --n-perm 5000 --seed 0 \
  --panel-id nacional_17027_limpio \
  --panel-file reports/timesfm_benchmark/panels/nacional_17027.csv
```
- `effect_sizes.py` no necesita cambios de lógica. Escribe `effect_sizes_all.csv`, `lead_time_curve.png` y los PNG por split dentro de `--backtest-root`. Esos archivos se copian a `reports/timesfm_benchmark/nacional_limpio/`.
- El registro de proveniencia de `effect_sizes` apunta a `$WORK/.../effect_sizes.csv`. Para que cada CSV publicado tenga su propio registro, tras la copia se agrega un registro con `output_files` apuntando a `nacional_limpio/effect_sizes_all.csv` (mismo mecanismo que `merge_predictions` usa para `metrics_all.csv`).

**Paso 5. E4: curva de horizonte.**
- La curva entre bloques sale del paso 4 (`lead_time_curve.png`, con `timesfm` y `tuned`) a partir de `metrics_all.csv`.
- `error_growth_curves` (`evaluate.py:187`) no tiene CLI y por eso sus CSV están en `EXCLUDED_FILES`. Se añade a `evaluate.main` la opción `--growth-curve <split>`, que llama a esa función con la raíz limpia y escribe `curva_error_nacional_limpio.csv` con proveniencia. El CSV nuevo entra en `TRACKED_METRIC_FILES`.
- Las figuras `nacional_curva_horizonte.png` y `crecimiento_error_nacional.png` se regeneran como versiones `_limpio` con `plots.py` y `make_figures.py`, que reciben la ruta de entrada y el sufijo de salida como parámetros.

**Paso 6. Cribado (obligatorio).**
```
uv run python -m experiments.timesfm.evaluate \
  --predictions-dir $WORK/preds_cribado --splits ll4 --by-zone \
  --backtest-root $RES/tuning/backtest_clean \
  --out-dir reports/timesfm_benchmark/cribado_limpio \
  --panel-id cribado_1092_limpio \
  --panel-file reports/timesfm_benchmark/panels/cribado_estratificado.csv
```
- Los rivales y las nueve variantes se puntúan sobre las 1.092 celdas comunes (la unión interna descarta las 14 que no están en el run limpio).
- `sesgo_seleccion_ll4.csv` se recalcula sobre las 1.092 celdas. Es una verificación, no una reselección: la variante ganadora `tmin_anom_full` ya está fijada. Si el orden de las dos primeras cambia, se documenta en el README y no se modifica la elección.
- Se regeneran `escalera_cribado_limpio.png`, `calibracion_cribado_limpio.png` y la curva `curva_error_cribado_limpio.csv` (con `--growth-curve` sobre las predicciones del cribado).
- Las zonas cubiertas por el cribado limpio se cuentan desde `metrics_by_zone.csv` y se informan sin suponer 33.

**Paso 7. Artefacto interactivo y mapa.**
- `experiments/timesfm/artifact_data.py::check_parity` (línea ~259) tiene valores esperados codificados (`1.1536`, `1.2194`, `1.5352`, `1.1533`, `1.1737`). Se actualizan a los valores del paso 3 (el de `tuned` en `ll4` pasa a 1,2279) y la lectura se redirige a `nacional_limpio/`. `zone_metrics`, `error_curve` y `tables` leen las rutas `_limpio`.
- Se recalcula el porcentaje de celdas fuera del Perú sobre las 17.027 celdas, con `shapely.contains_xy` contra los contornos departamentales. El 51,4 % (8.755 de 17.041) vale solo para el panel con fuga. El resultado se registra en el bead `tdew-214.8`.
- El número de zonas cubiertas baja de 38 a 33 de 41 (PAPER_PLAN, entrada del 14 de septiembre). El artefacto debe tolerar las zonas ausentes en el desglose por zona.
- Se regenera `artifact/datos.js` con `artifact_data.build` y se busca en `artifact/index.html` cualquier cifra escrita a mano (1,219 / 1,154 / 17.041 / 38 zonas).

**Paso 8. Addendum del manifiesto.**
- `docs/protocol/timesfm_manifest.yaml` (congelado el 2026-09-22) no se modifica.
- Se crea `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`. Contenido:
  - `addendum_de`: `docs/protocol/timesfm_manifest.yaml@2026-09-22`.
  - `fecha`: 2026-10-02. `bead_id`: el bead nuevo de este punto, bajo `tdew-214`.
  - `motivo`: la referencia del manifiesto original (`$RES/tuning/backtest`) usa selección de recetas con los años 1981–2016. El paper reporta el run limpio (selección solo con años de entrenamiento, `h` en {7, 11, 15, 21, 31, 45}), por lo que la comparación debe hacerse contra ese.
  - `rival_tuned`: nueva fuente `$RES/tuning/backtest_clean/{ll1,ll2,ll4}/predictions.parquet`. Climatología, Td observado y splits no cambian.
  - `panel_nacional`: 17.027 celdas (subconjunto del panel original de 17.041) y 33 zonas SENAMHI de 41 (la sección `nacional` del manifiesto original dice 38). Fuente de la cifra: `PAPER_PLAN.md`, entrada del 2026-09-14. Panel de cribado: 1.092 celdas en `cribado_limpio/`.
  - `sin_cambio`: variantes de TimesFM, contexto, covariable Tmin, `make_positive=False`, predicciones de TimesFM.
  - `no_comparable`: las tablas departamental y de escala conservan `tuned` con selección con fuga y no deben compararse con las cifras limpias.
- Los registros de proveniencia nuevos usan `manifest_ref = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"`. Los antiguos conservan `...timesfm_manifest.yaml@2026-09-22`. `MANIFEST_REF` en `evaluate.py` se vuelve parámetro o se agrega una constante `MANIFEST_REF_LIMPIO`.
- `TRACEABILITY.md` cita el addendum desde su sección 1.

**Paso 9. Documentación del benchmark.**
- `README.md`, sección "Resultados" (líneas ~150–235): se reemplazan las tablas por las del run limpio (escalera, efectos, horizonte). La frase "reproducen 1,219 y 1,535" pasa a "1,228 y 1,535". El agregado pasa de 17.041 a 17.027 celdas y de 24.896.901 a 24.876.447 pares. Se actualizan la tabla de "Los cuatro niveles", la de cribado (1.092 celdas) y la nota sobre las celdas fuera del Perú.
- Subsección breve "Referencia: run con fuga": las cifras anteriores (1,2194 para `tuned` en `ll4`, 0,0658 de ΔRMSE, 17.041 celdas), la razón del cambio (la selección vio 1981–2016) y la ruta de los archivos conservados (`nacional/`, `cribado/`, `curva_error_*.csv`).
- Nota visible, en el README y en `TRACEABILITY.md`, junto a las tablas departamental y de escala: el `tuned` de esas tablas usa el manifiesto de recetas con fuga y `h` de {7, 11, 15, 21}; no son comparables con las cifras limpias; la re-corrida con selección limpia queda para un punto posterior.
- `TRACEABILITY.md`: §3 (paneles, con el panel limpio y el cribado limpio), §5 (control de reproducción: 1,2279 y 1,5352 contra `backtest_clean/metrics_all.csv`), §6 (comandos) y §2 (linaje, con el origen `tuning/backtest_clean/`). El control "17.041 de 17.041" se reemplaza por "17.027 de 17.027; 14 celdas de TimesFM fuera de la referencia".
- `limitaciones.md`: líneas que citan las 17.041 celdas. Se agrega la limitación de 33 zonas de 41.
- `experiments/timesfm/README.md` (líneas ~13, 27, 39, 42): ruta por defecto y nombre de la raíz fusionada.
- Los README y los `.md` de proveniencia no se editan para reescribir cifras antiguas fuera de la subsección de referencia.

**Paso 10. Beads y registro.**
- Crear una subtarea bajo `tdew-214` para este punto. Si corresponde fila en el Gantt de Notion, se asocia con `Bead ID`.
- Actualizar `tdew-214.8` con el conteo nuevo de celdas fuera del Perú.
- Agregar a PAPER_PLAN.md una entrada fechada que enlace este plan.
- No se hacen commits ni push (perfil conservador de `CLAUDE.md`).

## 6. Artefactos de salida

| Ruta | Contenido |
|---|---|
| `$WORK/backtest_clean_timesfm/{ll1,ll2,ll4}/predictions.parquet`, `metrics.csv`, `metrics_all.csv` | referencia limpia con `pred_timesfm` (intermedio, fuera del repo) |
| `reports/timesfm_benchmark/nacional_limpio/leaderboard.csv`, `metrics_by_zone.csv` | E2 |
| `reports/timesfm_benchmark/nacional_limpio/metrics_all.csv`, `effect_sizes_all.csv` | E2, E3 |
| `reports/timesfm_benchmark/nacional_limpio/lead_time_curve.png` y PNG por split | E4 y E2 |
| `reports/timesfm_benchmark/curva_error_nacional_limpio.csv` | E4, curva diaria |
| `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv`, `metrics_by_zone.csv`, `sesgo_seleccion_ll4.csv` | cribado |
| `reports/timesfm_benchmark/curva_error_cribado_limpio.csv` | curva diaria del cribado |
| `reports/timesfm_benchmark/panels/nacional_17027.csv` | panel limpio |
| `reports/timesfm_benchmark/figs/*_limpio.png` | figuras regeneradas |
| `reports/timesfm_benchmark/artifact/datos.js` (y `index.html` si hay cifras fijas) | página interactiva |
| `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml` | addendum del protocolo |

Se conservan sin cambios: `nacional/`, `cribado/`, `curva_error_nacional.csv`, `curva_error_cribado.csv`, sus sidecars `.provenance.json`, `departamental/`, `escala/` y `docs/protocol/timesfm_manifest.yaml`.

## 7. Criterios de verificación y aceptación

1. En `ll4`, las filas `tuned` y `climatology` de `nacional_limpio/metrics_all.csv` coinciden con `backtest_clean/metrics_all.csv` (n=24.876.447; RMSE 1,2279 y 1,5352), con diferencia absoluta menor que 1e-9.
2. Igual para `ll1` (n=6.231.882) y `ll2` (n=12.446.737).
3. `cells = 17.027` en todas las filas y splits de `nacional_limpio/`. El registro de la fusión informa 14 celdas de TimesFM descartadas y 0 de la referencia.
4. TimesFM `ll4` ≈ 1,1536, `ll2` ≈ 1,1533 y `ll1` ≈ 1,1736 (tolerancia 5e-4).
5. `effect_sizes_all.csv` tiene `n_cells = 17027` en las 12 filas (3 splits × 4 baselines), con 1.000 remuestreos, 5.000 permutaciones y semilla 0. El `p` mínimo alcanzable es 0,0002.
6. Control de regresión de `effect_sizes.py`: el `delta_rmse_C` de la comparación `timesfm_vs_climatology` se puede reconstruir como RMSE(clima) − RMSE(TimesFM) con las cifras de `metrics_all.csv`. La comparación `timesfm_vs_tuned` en `ll4` es ≈ +0,074.
7. `cribado_limpio/leaderboard.csv` tiene `cells = 1092` en todas las filas.
8. `git diff --stat` no muestra cambios en `nacional/`, `cribado/`, `departamental/`, `escala/`, `curva_error_*.csv` existentes ni en `docs/protocol/timesfm_manifest.yaml`. Los cambios en README y TRACEABILITY se limitan a lo descrito en el paso 9.
9. `uv run pytest tests/ -q` pasa, incluidos los tests de proveniencia modificados.
10. `check_parity` de `artifact_data` pasa con los valores nuevos.
11. Ninguna cifra "1,219", "1,154", "17.041", "24.896.901" ni "38 zonas" queda como cifra vigente en README, TRACEABILITY, limitaciones ni artefacto (búsqueda con `grep`). Solo aparecen en la subsección de referencia con fuga y en las notas de no comparabilidad.
12. Los dos registros de proveniencia de una misma fila de `nacional_limpio/` llevan `panel_id = nacional_17027_limpio` y `manifest_ref` del addendum.

## 8. Cambios a tests y proveniencia

- `build_row_provenance` (`evaluate.py`) y `build_rival_provenance` (`HPC_code_tunning/backtest.py:124`) no tienen parámetro `notes`. Se añade `notes: Optional[str]` y se transmite a `MetricProvenance(notes=...)`, campo que ya existe (`provenance.py:113`). El texto indica la raíz de backtest, "selección solo con años de entrenamiento, h {7,11,15,21,31,45}" y el número de celdas.
- `panel_id` nuevos: `nacional_17027_limpio` y `cribado_1092_limpio`.
- `tests/test_metric_provenance.py`:
  - Agregar a `TRACKED_METRIC_FILES` los CSV de `nacional_limpio/`, los de `cribado_limpio/` y `curva_error_nacional_limpio.csv`.
  - Agregar a `EXCLUDED_FILES`, con la razón, `panels/nacional_17027.csv` y `curva_error_cribado_limpio.csv` si no se instrumenta.
  - Test nuevo, análogo a `test_departamental_panel_cell_counts_match_the_actual_predictions_parquet`: el `panel_cell_count` de cada registro limpio es igual al número de IDs de `nacional_17027.csv` (17.027), y para el cribado, a 1.092.
- `tests/test_merge_predictions_provenance.py`: caso para `CLEAN_BACKTEST_ROOT`.
- Test nuevo sin datos externos: `evaluate.DEFAULT_BACKTEST_ROOT` termina en `backtest_clean`, y `merge_predictions` usa la misma constante.
- Test nuevo: `merge_split` informa el conteo de celdas de TimesFM descartadas (con un parquet sintético donde TimesFM tiene celdas extra).
- `tests/test_timesfm_departamental.py`: ajustar la llamada si `--backtest-predictions` pasa a ser obligatorio.
- `tests/test_effect_sizes_provenance.py`: sin cambios de lógica.
- `reports/metric_provenance.jsonl` no se edita; solo se agregan filas.

## 9. Riesgos

- Mezcla de cifras con fuga y limpias en README o TRACEABILITY si la edición queda a medias. Mitigación: criterio 11.
- Las rutas absolutas de `output_files` dependen de dónde se corra el comando. Las salidas publicadas se generan con `--out-dir` bajo el repo para que `test_metric_provenance` las encuentre.
- El panel limpio cubre 33 de 41 zonas. `metrics_by_zone.csv`, el mapa y las tablas por zona tienen menos zonas que antes; el artefacto debe tolerarlo.
- `departamental` y `escala` seguirán con `tuned` de selección con fuga. El README mostrará cifras limpias (nacional) junto a cifras no limpias (departamental, escala). La nota del paso 9 debe quedar junto a cada tabla.
- El agregado del panel sigue sin ser un promedio del Perú. La proporción fuera del territorio debe recalcularse (paso 7).
- El orden de las variantes del cribado puede cambiar al pasar de 1.106 a 1.092 celdas. Si la brecha con la segunda es del orden del IC, se documenta; no se reelige la variante.
- El addendum es un archivo nuevo: nada lo exige hoy. Se cita desde `TRACEABILITY.md` y desde los registros de proveniencia para que no quede huérfano.
- `effect_sizes.py` importa `experiments.timesfm.evaluate`. Los cambios del paso 1 no deben crear importaciones circulares con `merge_predictions`.

## 10. Qué no entra

- Re-correr inferencia de TimesFM.
- Re-correr a Palacios (`select_backtest`, `backtest`) sobre el panel departamental o el de escala con selección limpia.
- Escribir o modificar archivos bajo `$RES`.
- Modificar `docs/protocol/timesfm_manifest.yaml`.
- Reselección de variante de TimesFM o cambios de protocolo.
- Fases 6 a 15 del roadmap `tdew-214.11` (soporte observacional, cola larga, mapa, empalme, etc.).
- Edición de `reports/paper/paper.qmd`, que no cita a TimesFM. Su incorporación es el bead `tdew-u8m`.
- Commits o push.

---

### Archivos críticos para la implementación
- `experiments/timesfm/evaluate.py`
- `experiments/timesfm/merge_predictions.py`
- `HPC_code_tunning/effect_sizes.py`
- `tests/test_metric_provenance.py`
- `experiments/timesfm/artifact_data.py`
