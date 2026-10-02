# PLAN_2: tabla por tier de soporte observacional (E5) y tabla mensual de sesgo (E8) de TimesFM frente a Palacios

Versión final. Fecha: 2026-10-02. Bead padre: `tdew-214` (se propone una subtarea nueva, hermana de la de PLAN_1).

## Experimentos que cubre este plan

Los códigos E# son los de la lista de experimentos del paper de Palacios (`reports/paper/paper.qmd`), numerados E1–E16 para esta comparación.

| # | Experimento (en el paper) | Qué mide |
|---|---|---|
| E5 | Tiers de soporte observacional (`tbl-tiers`) | RMSE, MAE, sesgo, r y skill según la distancia de cada celda al dominio SENAMHI (within, near, marginal, extrapolated, unsupported) |
| E8 | Sesgo estacional por mes | Sesgo medio de cada mes del año (el paper cita diciembre: +1,45 → +0,02 °C con selección por zona×doy) |

Este plan depende de PLAN_1, que cubre E2 (escalera de RMSE), E3 (tamaños de efecto) y E4 (curva de lead time).

## 0. Decisiones tomadas

1. **Splits de E5.** Se puntúan `ll1`, `ll2` y `ll4`. La tabla del texto del paper muestra solo `ll4`, como `tbl-tiers`.
2. **Métodos.** El CSV completo incluye TimesFM, `tuned`, climatología, Td=Tmin y `zone_ols`. La versión reducida para el texto lleva TimesFM, `tuned` y climatología.
3. **Sesgo mensual (E8).**
   - Se agrega de forma pooled por mes calendario de `FECHA` (misma convención que `effect_sizes._plots` y que el +0,017 de diciembre citado en el paper).
   - En `ll4` se añade la dispersión entre celdas: desviación y percentiles 5 y 95 del sesgo por celda×mes.
   - `ll1` y `ll2` entran como filas adicionales del CSV largo, solo con el valor pooled.
4. **Sesgo mes × tier.** Se calcula, en un CSV aparte.
5. **Código.**
   - Script nuevo `experiments/timesfm/by_tier_month.py`, con CLI, proveniencia (`panel_id` `nacional_17027_limpio`) y tests. Lee el merge intermedio de PLAN_1.
   - El panel de cribado se procesa en la misma herramienta como verificación, en CSV aparte (`panel_id` `cribado_1092_limpio`).
   - No se toca `reports/paper/scripts/`. El script nuevo importa de él solo si hace falta, y nunca lo modifica.

## 1. Objetivo

Completar la comparación entre TimesFM 3.0 zero-shot y el método `tuned` de Palacios con dos análisis que el paper ya reporta para `tuned`: el desempeño por tier de soporte observacional (E5, `tbl-tiers`) y el sesgo estacional por mes (E8). Son solo cómputo sobre predicciones existentes. No se corre inferencia nueva y no se escribe bajo `$RES`.

## 2. Alcance

Entra en este punto:

- E5: RMSE, MAE, sesgo, r, RMSE de climatología y skill por tier, para TimesFM y `tuned`. También RMSE de Td=Tmin y `zone_ols`, en `ll1`, `ll2` y `ll4`.
- E8: sesgo medio mensual de TimesFM y de `tuned` (y de los demás métodos, ver paso 4), con dispersión entre celdas en `ll4`.
- Sesgo mes × tier en `ll4` (y en `ll1`, `ll2` si el costo es nulo, ver paso 4).
- Verificación sobre el panel de cribado limpio (1.092 celdas).
- Control de reproducción contra las cifras del paper para `tuned`.
- Una tabla reducida en formato listo para el texto.
- Una figura mensual `_limpio` (opcional, ver paso 7).
- Proveniencia, tests, addendum de manifiesto y documentación.

## 3. Dependencia de PLAN_1

PLAN_1 quedó completado el 2026-10-02 (bead `tdew-214.12`, commits `31f6ed8` y `6247e83`). Ya existen en disco:

- `/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/{ll1,ll2,ll4}/predictions.parquet` (columna `pred_timesfm`).
- `reports/timesfm_benchmark/panels/nacional_17027.csv` y `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`.

Este plan reutiliza de PLAN_1 la constante `CLEAN_BACKTEST_ROOT`, la constante `MANIFEST_REF_LIMPIO` y el addendum de manifiesto. No se redefinen aquí.

Para el cribado, el script lee las predicciones de TimesFM de `/home/cvelasquez/tdew_timesfm/preds_cribado/` (variante `tmin_anom_full`, split `ll4`). Las une con el run limpio por `(ID, FECHA)`, en memoria, restringidas a `panels/cribado_estratificado.csv`.

## 4. Pre-condiciones verificadas

Verificadas con lecturas reales en memoria, sin escribir archivos ni bajo `$RES`. TimesFM se obtuvo uniendo `preds_nacional/ll4__tmin_anom_full.parquet` con `backtest_clean/ll4/predictions.parquet` por `(ID, FECHA)`, `validate="one_to_one"`, que es equivalente al merge de PLAN_1.

| Hecho | Evidencia |
|---|---|
| `support_distance.parquet` cubre el 100 % de las celdas del run limpio. | La unión por `ID` conserva las 17.027 celdas. |
| Las celdas por tier coinciden con el paper. | within 8.306, near 1.779, marginal 1.433, extrapolated 2.563, unsupported 2.946 (suma 17.027). |
| El RMSE de `tuned` ll4 por tier reproduce `tbl-tiers` y `validation_by_support.csv`. | within 0,946, near 1,139, marginal 1,276, extrapolated 1,374, unsupported 1,724. |
| RMSE de TimesFM ll4 por tier (valores esperados). | within 0,867, near 1,061, marginal 1,198, extrapolated 1,298, unsupported 1,652. |
| El sesgo mensual de `tuned` ll4 limpio reproduce la cita del paper. | Diciembre +0,017; máximo \|sesgo\| 0,402 (enero, −0,402). |
| Sesgo mensual de TimesFM ll4 (valores esperados). | Enero −0,325, febrero +0,061, marzo +0,248, abril +0,263, mayo +0,112, junio +0,151, julio +0,210, agosto +0,255, septiembre +0,193, octubre −0,098, noviembre +0,100, diciembre +0,089. |
| Convención de mes del código existente. | `effect_sizes._plots` usa `pd.to_datetime(FECHA).dt.month` y `mean(pred − obs)` pooled sobre todas las celdas-día del focal, por split. No existe CSV. |
| La dispersión entre celdas del sesgo mensual es relevante. | Desviación del sesgo por celda×mes de 0,14 a 0,51 °C (enero `tuned` 0,51; TimesFM 0,33). El pooled oculta variación espacial. |
| El panel de cribado limpio es una muestra estratificada. | De las 1.092 celdas: within 842, near 79, marginal 59, extrapolated 65, unsupported 47. |
| Las predicciones de TimesFM son float32. | Los promedios en float32 difieren del float64 en el último decimal. |
| `validation_by_support.py` no es reutilizable tal cual. | Está fijo a `tuned`, `clima`, `Td=Tmin`, `zone_ols`, lee `$BACKTEST_ROOT` y escribe su CSV junto al script. La lógica de `score()` y de unión con `tier` sí es reutilizable. |
| Los tiers del paper vienen de `make_support_distance.py`. | Distancia al dominio SENAMHI: dentro, 0–50, 50–100, 100–200, más de 200 km. |

## 5. Principio de no sobrescritura

- No se escribe bajo `$RES`. `support_distance.parquet` y `backtest_clean/` se leen solamente.
- No se modifica nada en `reports/paper/scripts/` (`validation_by_support.py`, su CSV, `make_support_distance.py`).
- Las salidas publicadas van a `reports/timesfm_benchmark/nacional_limpio/` y `reports/timesfm_benchmark/cribado_limpio/`, con sufijo `_limpio` en los nombres de archivo. Los directorios `nacional/` y `cribado/` y sus CSV no se tocan.
- `reports/metric_provenance.jsonl` es de solo adición: se agregan registros nuevos y los existentes permanecen.
- No se calcula nada con el run con fuga (`$RES/tuning/backtest`).

## 6. Diseño del script

Archivo nuevo: `experiments/timesfm/by_tier_month.py`. Convenciones del paquete: `from __future__ import annotations`, `main(argv) -> int`, argparse y proveniencia con `tdew_estimation.provenance` (`record_metric_provenance`), como `evaluate.py`.

Funciones:

- `load_panel(split, *, backtest_root, merged_root=None, preds_dir=None, panel_file=None) -> pd.DataFrame`. Lee `predictions.parquet` del run limpio (`CLEAN_BACKTEST_ROOT`) con columnas `ID, FECHA, TD_obs, pred_tuned, pred_clim, pred_tmin, pred_ols`.
  - Modo nacional: lee `pred_timesfm` del merge intermedio (`--merged-root`).
  - Modo cribado: une `pred` (renombrada a `pred_timesfm`) de `--preds-dir` por `(ID, FECHA)` con `validate="one_to_one"` y filtra por `--panel-file`.
  - Convierte todas las columnas de predicción a `float64` al leerlas.
  - Informa el número de celdas y el de pares `(ID, FECHA)` descartados por unión.
- `attach_tier(df, support_path) -> pd.DataFrame`. Une con `support_distance.parquet` (columnas `ID`, `tier`) y falla si queda alguna celda sin tier.
- `score(pred, obs) -> dict`. Mismas métricas que `validation_by_support.score`: RMSE, MAE, sesgo, r, sobre pares finitos. Se reimplementa en el script (no se importa de `reports/`, que no es paquete) con una prueba de equivalencia numérica contra el CSV del paper para `tuned`.
- `tier_table(df, split) -> pd.DataFrame`. Una fila por `(split, tier, method)`, con las columnas `cells`, `n`, `rmse`, `mae`, `bias`, `r`, `clim_rmse` y `skill = 1 − rmse/clim_rmse`. Los métodos son `timesfm`, `tuned`, `climatology`, `tmin`, `zone_ols`. La climatología es referencia, con skill 0 por construcción.
- `monthly_bias(df, split, *, dispersion) -> pd.DataFrame`. Formato largo, una fila por `(split, method, month)`:
  - `bias_pooled = mean(pred − obs)` agrupado por `to_datetime(FECHA).dt.month`.
  - Con `dispersion=True` (solo `ll4`) añade `cell_bias_std`, `cell_bias_p05` y `cell_bias_p95`, calculados sobre el sesgo medio por `(ID, month)`.
  - `n` es el número de pares y `cells` el número de celdas.
- `monthly_bias_by_tier(df, split) -> pd.DataFrame`. Una fila por `(split, tier, method, month)`, con `bias`, `n` y `cells`.
- `reduced_table(tiers_ll4) -> pd.DataFrame`. Una fila por tier con TimesFM, `tuned` y climatología (RMSE, MAE, sesgo, r, skill), en el formato de columnas de `tbl-tiers`. Se emite también como tabla markdown con tres decimales.
- `main(argv)`. Opciones: `--merged-root`, `--preds-dir`, `--panel-file`, `--splits` (por defecto `ll1,ll2,ll4`), `--backtest-root` (por defecto `CLEAN_BACKTEST_ROOT`), `--support-distance` (por defecto `$RES/tuning/support_distance.parquet`), `--out-dir`, `--panel-id`, `--bead-id`, `--suffix` (por defecto `_limpio`). Registra en `notes` la raíz de backtest usada y la conversión a float64.

Decisiones de diseño:

- La agregación mensual es pooled sobre todas las celdas-día del mes. El promedio por celda, o por año y mes, queda fuera de alcance.
- El mes es el de `FECHA`, no el de la fecha de emisión. Ninguna de las dos tablas depende de la emisión.
- El percentil se calcula con `numpy.percentile` sobre las celdas con al menos un día en el mes. En `ll4` toda celda tiene 4 años de cada mes, por lo que la cobertura es completa.
- `unsupported` y los demás tiers se ordenan con la constante `TIERS` del script, igual que en el paper.

## 7. Pasos

**Paso 1. Script y utilidades (código).**
- Crear `experiments/timesfm/by_tier_month.py` con las funciones de la sección 6.
- Importar `CLEAN_BACKTEST_ROOT` y `MANIFEST_REF_LIMPIO` de `evaluate.py` (introducidos por PLAN_1). No mantener copia propia.
- Incluir `build_provenance(...)` que reutilice `build_row_provenance` de `evaluate.py` para TimesFM y `RIVAL_PROVENANCE` para los rivales, con `manifest_ref = "docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml"`.

**Paso 2. Ejecución nacional.**
```
uv run python -m experiments.timesfm.by_tier_month \
  --merged-root $WORK/backtest_clean_timesfm --splits ll1,ll2,ll4 \
  --backtest-root $RES/tuning/backtest_clean \
  --out-dir reports/timesfm_benchmark/nacional_limpio \
  --panel-id nacional_17027_limpio \
  --panel-file reports/timesfm_benchmark/panels/nacional_17027.csv
```
Salidas:
- `nacional_limpio/tiers_limpio.csv`: tabla completa de E5 (todos los métodos y splits).
- `nacional_limpio/tiers_texto_limpio.csv`: tabla reducida de `ll4` (TimesFM, `tuned`, climatología). Se emite también en markdown en `nacional_limpio/tiers_texto_limpio.md`, para pegar en el texto.
- `nacional_limpio/sesgo_mensual_limpio.csv`: formato largo. Incluye `ll1`, `ll2` y `ll4`, con columnas de dispersión llenas solo en `ll4`.
- `nacional_limpio/sesgo_mes_tier_limpio.csv`: sesgo mes × tier × método para los tres splits.

**Paso 3. Control de reproducción (parte del script y de los tests).**
Se ejecuta antes de escribir los CSV y aborta con error si falla:
- Celdas por tier: 8.306 / 1.779 / 1.433 / 2.563 / 2.946, tolerancia exacta.
- RMSE de `tuned` ll4 por tier contra `reports/paper/scripts/validation_by_support.csv`, tolerancia 1e-6. Este CSV se lee, no se modifica.
- Sesgo mensual de `tuned` ll4: diciembre +0,017 y máximo \|sesgo\| 0,402 en enero, tolerancia 5e-4.
- RMSE de TimesFM por tier y sesgo por mes de TimesFM contra los valores esperados de la sección 4 (tolerancia 5e-4), solo como alerta, para detectar un merge defectuoso.
Si el control falla en una prueba de CI, el test es el que lo detecta (paso 8). En ejecución real el script lo informa con `ERROR` y sale con código distinto de cero.

**Paso 4. Cribado (verificación).**
```
uv run python -m experiments.timesfm.by_tier_month \
  --preds-dir $WORK/preds_cribado --splits ll4 \
  --backtest-root $RES/tuning/backtest_clean \
  --out-dir reports/timesfm_benchmark/cribado_limpio \
  --panel-id cribado_1092_limpio \
  --panel-file reports/timesfm_benchmark/panels/cribado_estratificado.csv
```
- Escribe `cribado_limpio/tiers_cribado_limpio.csv` y `cribado_limpio/sesgo_mensual_cribado_limpio.csv` (y `sesgo_mes_tier_cribado_limpio.csv` si el costo es nulo; son 1.092 celdas).
- Comprobaciones: 1.092 celdas comunes; reparto 842 / 79 / 59 / 65 / 47. La muestra es estratificada, por lo que los números por tier se leen como verificación cualitativa del orden TimesFM < `tuned` en RMSE, no como estimador del campo.
- Este CSV no entra en la tabla del texto.

**Paso 5. Figura mensual `_limpio` (opcional, solo si el costo es menor).**
- Agregar en `plots.py` una función `monthly_bias_plot(table, out_path)` y llamarla desde `make_figures.py`. Barras agrupadas mensuales para TimesFM y `tuned` en `ll4`, con la banda p05–p95 entre celdas como barra de error.
- Salida: `reports/timesfm_benchmark/figs/nacional_sesgo_mensual_limpio.png`. Las figuras existentes no se tocan.
- Si se omite, `effect_sizes.bias_by_month.png` (focal TimesFM) de la copia de PLAN_1 cubre el pooled de TimesFM. El plan no depende de esta figura.

**Paso 6. Proveniencia.**
- Un registro por CSV publicado, con `record_metric_provenance`, agregado a `reports/metric_provenance.jsonl`.
- `panel_id`: `nacional_17027_limpio` o `cribado_1092_limpio`. `panel_file`: los CSV de `panels/`. `manifest_ref`: `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`. Se registran los splits, la variante `tmin_anom_full` y el `output_files` con la ruta del CSV.
- Los registros de los rivales (`tuned`, climatología, Td=Tmin, `zone_ols`) usan `RIVAL_PROVENANCE` como en `evaluate.py`.
- El addendum del manifiesto de PLAN_1 recibe una línea nueva en su sección `sin_cambio` o `analisis_adicionales`: «E5 y E8 solo cómputo sobre predicciones existentes». No hay manifiesto nuevo.

**Paso 7. Tests.**
Detalle en la sección 9.

**Paso 8. Documentación.**
Detalle en la sección 10.

## 8. Criterios de aceptación

1. Los cuatro CSV nacionales y los dos o tres del cribado existen en `_limpio`, con proveniencia registrada.
2. Control de reproducción verde: celdas por tier exactas; RMSE de `tuned` ll4 por tier igual al del paper (diferencia máxima 1e-6); diciembre +0,017 y máximo \|sesgo\| 0,402 (enero).
3. Cada celda nacional tiene un tier (cero IDs sin tier). La suma de `cells` por tier es 17.027 en cada split.
4. La tabla reducida usa los mismos tiers y el mismo orden que `tbl-tiers`. El `tuned` de ese archivo coincide, a tres decimales, con la tabla del paper.
5. Los valores de TimesFM coinciden con los esperados de la sección 4 dentro de 5e-4. Cualquier diferencia mayor se documenta como hallazgo, no se corrige en silencio.
6. Los agregados se calculan en float64 y la nota correspondiente figura en README y TRACEABILITY.
7. `git status` no muestra cambios en `reports/paper/scripts/`, `nacional/`, `cribado/` ni en sus CSV. No se creó ningún archivo bajo `$RES`.
8. `uv run pytest` pasa completo, incluidos los tests nuevos y `test_metric_provenance.py`.

## 9. Cambios a tests y proveniencia

- `tests/test_metric_provenance.py`
  - Agregar a `TRACKED_METRIC_FILES` los CSV nuevos: `nacional_limpio/tiers_limpio.csv`, `tiers_texto_limpio.csv`, `sesgo_mensual_limpio.csv`, `sesgo_mes_tier_limpio.csv`, `cribado_limpio/tiers_cribado_limpio.csv`, `sesgo_mensual_cribado_limpio.csv` (y `sesgo_mes_tier_cribado_limpio.csv` si se genera).
  - Si el test de exclusión exige que todo CSV de `reports/` esté rastreado o excluido, el `.md` de la tabla reducida y la figura no cuentan (no son CSV). Verificar con la lógica del test (línea ~154) y, si hace falta, ampliar `EXCLUDED_FILES`.
- `tests/test_timesfm_by_tier_month.py` (nuevo):
  - `score` coincide con una implementación de referencia en datos sintéticos; filtra pares no finitos.
  - Con datos sintéticos, `tier_table` entrega las columnas y el orden `TIERS`, y `skill = 1 − rmse/clim_rmse`.
  - El mes se toma de `FECHA` y no de otra columna (caso con FECHA en dos años).
  - `monthly_bias` pooled coincide con `groupby(month).mean()` y la dispersión se llena solo en `ll4`.
  - `attach_tier` falla si hay un `ID` sin tier.
  - Conversión a float64: un caso en que el promedio en float32 difiere del de float64.
  - El control de reproducción se lanza (excepción) cuando se altera el conteo de celdas.
  - Prueba de integración opcional marcada para saltarse si no existe `$RES` (con datos reales: celdas por tier y RMSE de `tuned` ll4 contra `validation_by_support.csv`).
- `tests/test_timesfm_by_tier_month_provenance.py` (nuevo): estructura del registro (modelo, `trained`, periodos, `panel_id` `nacional_17027_limpio`, `manifest_ref` del addendum), análogo a `test_timesfm_evaluate_provenance.py`.

## 10. Documentación a actualizar

- `reports/timesfm_benchmark/README.md`
  - Nueva subsección «Soporte observacional» con la tabla reducida de `ll4` (TimesFM, `tuned`, climatología) y los tamaños de ventaja por tier. Se enlaza el CSV completo.
  - Nueva subsección «Sesgo mensual» con una tabla de 12 meses para TimesFM y `tuned` en `ll4`, y la lectura de los hallazgos: sesgo cálido de TimesFM de 0,1 a 0,26 °C en marzo–septiembre, máximo \|sesgo\| 0,325 en enero, frente a diciembre +0,017 y máximo 0,402 (enero) de `tuned`.
  - Dispersión entre celdas y sesgo mes × tier: referencia al CSV.
  - Nota del cribado: 842 de las 1.092 celdas son within, muestra estratificada, verificación cualitativa.
  - Nota técnica: las predicciones de TimesFM están en float32 y todos los agregados se calculan en float64.
- `reports/timesfm_benchmark/TRACEABILITY.md`: nuevas filas para cada CSV (script, comando, `panel_id`, fuentes de entrada: merge intermedio, `support_distance.parquet`, run limpio), la nota float32→float64, la convención de mes (por `FECHA`, pooled) y la referencia al addendum.
- `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`: una línea de análisis adicionales (paso 6). El manifiesto original no cambia.
- `PAPER_PLAN.md`: entrada fechada que registra E5 y E8 como hechos para TimesFM, con la ruta de los CSV. No se modifica `paper.qmd`; la inclusión en el texto es una decisión posterior.

## 11. Riesgos

- **Orden de ejecución.** El merge de PLAN_1 aún no existe. Si PLAN_1 cambia el nombre de la columna o la ruta, el script falla de forma explícita (comprobación de columnas al inicio).
- **Predicciones float32.** Sin casteo, los promedios difieren en el último decimal. Mitigado con la conversión a float64 y un test.
- **Cribado no representativo.** Una lectura apresurada de los números por tier del cribado puede llevar a conclusiones erróneas. Mitigado con la nota en README y exclusión de la tabla del texto.
- **Sesgo mensual sensible a la agregación.** Pooled y por celda dan lecturas distintas (dispersión de 0,14 a 0,51 °C). Se publican ambas en `ll4` y se documenta cuál reproduce el paper.
- **Atribución del +0,02 de diciembre.** El paper lo atribuye a la selección por zona×doy del run limpio. El control confirma +0,017 en `backtest_clean`. No se extrapola a otros runs.
- **Comparación entre tiers distintos.** TimesFM y `tuned` se puntúan sobre las mismas 17.027 celdas, por lo que la diferencia es pareada. No se interpretan los CSV del cribado frente a los nacionales.
- **Convención de tier.** Los tiers se heredan de `support_distance.parquet` (distancia al dominio SENAMHI) sin recalcular. Si el archivo cambia, el control de celdas por tier falla.

## 12. Qué no entra

- Inferencia nueva de TimesFM y re-corridas de Palacios.
- Modificar `paper.qmd`, `reports/paper/scripts/` o sus CSV.
- Agregación mensual por celda con pesos o por año y mes (más allá de la dispersión definida).
- Pruebas de significancia o bootstrap por tier o por mes (los tamaños de efecto globales son de PLAN_1).
- Tiers o distancias distintas de las del paper.
- Tablas departamental y de escala (siguen con `tuned` con selección con fuga, ver PLAN_1).
- El cribado como evidencia principal: solo verificación.
- Reescritura de registros de proveniencia existentes.

---

### Archivos críticos para la implementación
- `experiments/timesfm/by_tier_month.py` (nuevo)
- `experiments/timesfm/evaluate.py`
- `tests/test_metric_provenance.py`
- `reports/paper/scripts/validation_by_support.py` (solo lectura, referencia)
- `reports/timesfm_benchmark/TRACEABILITY.md`
