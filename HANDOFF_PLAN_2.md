# HANDOFF_PLAN_2: tiers de soporte (E5) y sesgo mensual (E8) de TimesFM

Fecha: 2026-10-02. Bead: `tdew-0bt` (hijo lógico de `tdew-214`). Branch: `tdew-214-tier-mes`, creada desde `tdew-u8m-paper-timesfm-narrative` (`0b53245`). Plan de origen: `PLAN_2.md`. Sin push; `main` no se toca.

## Estado

| etapa | resultado |
|---|---|
| Implementación y primera ejecución (`66cc5e5`, `5b0c3a2`) | Revisión independiente 1 (Opus, esfuerzo alto): `RECHAZADO` por 2 bloqueantes y 6 menores |
| Correcciones, MLflow y re-ejecución completa (`a70645e` y el commit de artefactos) | Todos los hallazgos atendidos; suite completa 441 passed |
| Revisión independiente 2 (Opus, contexto limpio, con mutaciones y contraste desde parquet) | `RECHAZADO` por 1 bloqueante de tests (ninguna cifra errónea) y 8 menores; ver «Revisión 2» |

Si una revisión posterior da `APROBADO`: `git switch tdew-u8m-paper-timesfm-narrative && git merge --no-ff tdew-214-tier-mes`, `bd close tdew-0bt` y actualizar la fila de Notion con `Bead ID = tdew-0bt` (`Completed`, `Progress = 1`). Si no, la branch queda con las observaciones.

## Hallazgos de la revisión 1 y cómo se atendieron

| # | hallazgo | corrección | verificación |
|---|---|---|---|
| 1 (bloqueante) | README citaba «0,15 a 0,51 °C» de dispersión entre celdas; el mínimo real es 0,136 | README: «0,14 a 0,51 °C» (TimesFM 0,15–0,34; `tuned` 0,14–0,51); mismo rango corregido en `PLAN_2.md` §4 y §11 (origen del error) | `tests/test_timesfm_by_tier_month_docs.py` compara las tablas y el rango del README contra los CSV |
| 2 (bloqueante) | `test_float32_inputs_are_aggregated_in_float64` no fallaba al quitar el casteo | Caso nuevo donde restar y promediar en float32 pierde `obs` (pred ≈ 2²⁵, obs < 1) con una precondición explícita de que float32 difiere de float64 en más de 0,1 | Mutación a mano: sin float64 en `_error_frame` y sin float64 en `score`, el test falla en ambos casos |
| 3 | rama mensual del control sin verificar mes | `reproduction_check` exige diciembre, magnitud del máximo y que el máximo caiga en enero; caso positivo con `monthly` | Mutación `loc[12]`→`loc[1]`: falla el caso positivo |
| 4 | NaN pasaba el control; `main()` sin tests | `_off()` trata NaN como fallo; tests de `main()` (corrida feliz, control fallido devuelve 1 y no escribe, control invocado antes de escribir); `--registry-path` | Mutación `abs(diff) > tol`: fallan los tres casos de NaN |
| 5 | modo cribado sin las comprobaciones del plan | `panel_check` con `EXPECTED_NATIONAL_CELLS` (17.027 por split y reparto) y `EXPECTED_CRIBADO_CELLS` (1.092; 842/79/59/65/47) | Tests de total, de reparto con total correcto y de constantes |
| 6 | `output_files` y sidecars imprecisos | `provenance_targets`: cada registro lista solo los CSV de su split y método; TimesFM/`ll4` se escribe al final | Tests de `provenance_targets`; sidecar de `tiers_limpio.csv` = `tmin_anom_full`, ll4 |
| 7 | `.md` en formato numérico inglés | Se mantiene (es el formato de `tbl-tiers`) y se documenta en el README | — |
| 8 | figura opcional sin mencionar | README indica que no se generó y remite a `ll4_bias_by_month.png` | — |

Mutaciones adicionales comprobadas por el autor: mes tomado de otra columna y `ddof=1` en la dispersión hacen fallar tests existentes. La revisión 2 precisó que un desfase de un día en el mes (`FECHA − 1 día`) sobrevive a los tests (menor 1 de la revisión 2).

## Cambio añadido a petición del usuario: MLflow

`by_tier_month.py --mlflow` registra una corrida de evaluación por split en el experimento `tdew-timesfm-benchmark` de `mlflow.db` (ignorada por git). TimesFM no entrena, de modo que son evaluaciones, no entrenamientos; el README raíz ya no dice «no MLflow» sin matiz. Métricas: `<método>_<tier>_<métrica>` (rmse, mae, bias, r, skill), `<método>_{rmse,bias,skill}_all` (ponderadas por `n`), `<método>_bias_mNN` y, en `ll4`, `<método>_cell_bias_std_mNN`. El `run_id` queda en `mlflow_run_id` de cada registro de proveniencia.

| run | panel | split |
|---|---|---|
| `f9200a84…` | `nacional_17027_limpio` | `ll1` |
| `b5494815…` | `nacional_17027_limpio` | `ll2` |
| `477aa973…` | `nacional_17027_limpio` | `ll4` |
| `7669ac26…` | `cribado_1092_limpio` | `ll4` |

Ver con `uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000`.

## Re-ejecución y artefactos vigentes

Se ejecutaron de nuevo los dos comandos de `PLAN_2.md` §7 con `--mlflow` desde el commit `a70645e`. Los siete CSV (más `tiers_texto_limpio.{csv,md}`) resultaron **idénticos byte a byte** a los de la primera ejecución. `reports/metric_provenance.jsonl` es de solo adición: las 20 filas de la primera ejecución (commit `66cc5e5`, `generated_at` 16:07 UTC, p. ej. `run_id` `b7a2ab15…`) quedan reemplazadas por las 20 nuevas (commit `a70645e`, 16:34 UTC, con `mlflow_run_id`); las anteriores se conservan sin cambios.

Tabla comparativa contra Palacios (`ll4`, 17.027 celdas, run limpio):

| tier | celdas | RMSE TimesFM | RMSE `tuned` | ΔRMSE | sesgo TimesFM | sesgo `tuned` | skill TimesFM | skill `tuned` |
|---|---|---|---|---|---|---|---|---|
| within | 8.306 | 0,867 | 0,946 | 0,079 | +0,050 | +0,010 | 0,314 | 0,251 |
| near | 1.779 | 1,061 | 1,139 | 0,078 | +0,068 | −0,079 | 0,275 | 0,222 |
| marginal | 1.433 | 1,198 | 1,276 | 0,078 | +0,143 | −0,044 | 0,242 | 0,193 |
| extrapolated | 2.563 | 1,298 | 1,374 | 0,077 | +0,149 | −0,070 | 0,228 | 0,183 |
| unsupported | 2.946 | 1,652 | 1,724 | 0,072 | +0,223 | −0,089 | 0,188 | 0,153 |
| todos | 17.027 | 1,1536 | 1,2279 | 0,0743 | +0,104 | −0,033 | 0,2485 | 0,2001 |

Sesgo mensual `ll4` (TimesFM / `tuned`, °C): enero −0,325 / −0,402; diciembre +0,089 / +0,017; TimesFM de +0,11 a +0,26 entre marzo y septiembre; solo enero y octubre tienen menor |sesgo| en TimesFM. Tablas completas en `reports/timesfm_benchmark/README.md` (secciones «Soporte observacional» y «Sesgo mensual») y en los CSV de `nacional_limpio/`.

## Contraste de cifras con datos y reproducción reales

Script independiente (no importa `by_tier_month`; agrega con `np.bincount` desde los parquet), ejecutado el 2 de octubre de 2026 con 0 fallas:

- **A, recálculo total:** las 75 filas de tiers, 180 mensuales y 900 mes × tier nacionales, y las 25, 60 y 300 del cribado, coinciden con los CSV con diferencia máxima 5·10⁻¹³ (`n`, `cells` exactos).
- **B, reproducción del paper:** una copia de `validation_by_support.py` ejecutada sobre `backtest_clean` da exactamente `validation_by_support.csv` (diferencia 0 en todas las columnas); `tuned` de `tiers_limpio.csv` coincide con él (≤ 4·10⁻¹⁶) y con `tbl-tiers` de `paper.qmd` a tres decimales (diferencia 0 en celdas, RMSE, MAE, sesgo, r, climatología y skill).
- **C, consistencia con PLAN_1:** el RMSE global ponderado por `n` reconstruido desde los tiers iguala `nacional_limpio/metrics_all.csv` (diferencia 4·10⁻¹⁶), coincide con las cifras del HANDOFF_PLAN_1 (TimesFM 1,1736/1,1533/1,1536; `tuned` 1,2538/1,2765/1,2279; climatología 1,6803/1,6667/1,5352) y `n` = pares del run limpio (6.231.882 / 12.446.737 / 24.876.447). Los cinco métodos del cribado igualan `cribado_limpio/leaderboard.csv`.
- **D, float32 vs float64:** diferencia máxima en el sesgo mensual de TimesFM 8·10⁻¹¹, por debajo del umbral de reporte.
- **E, texto:** cada número de las tablas del README sale de los CSV (test automático); «menor RMSE en los cinco tiers» (también en el cribado), brechas de 0,0795 a 0,0715, «solo enero y octubre», mínimo y máximo de la dispersión y diciembre de `tuned` (+0,0175; el paper cita +0,02) verificados con código.
- **F, determinismo:** el CLI ejecutado hacia directorios y registro temporales reproduce los CSV byte a byte.
- **MLflow:** `rmse_all` de las corridas nacionales iguala `metrics_all.csv` (9 comparaciones) y los `run_id` de proveniencia existen en el servidor.

## Pendientes y advertencias

1. Corregir el bloqueante y los menores de la revisión 2, volver a revisar y, si es `APROBADO`, merge, cierre del bead y fila de Notion.
2. La figura mensual opcional del paso 5 sigue sin generarse.
3. `PAPER_PLAN.md` y `paper.qmd` no se tocaron (el archivo es de Palacios). Texto propuesto si Palacios quiere anotarlo, en inglés: «2026-10-02 — TimesFM vs `tuned` by observational-support tier and by month (bead `tdew-0bt`, `PLAN_2.md`). ll4: TimesFM RMSE below `tuned` in all five tiers (0.867 vs 0.946 within; 1.652 vs 1.724 unsupported); `tuned` reproduces `tbl-tiers` exactly. Monthly bias: December `tuned` +0.017, max |bias| 0.402 (January); TimesFM max |bias| 0.325 (January), warm +0.11 to +0.26 °C in March–September. Outputs under `reports/timesfm_benchmark/nacional_limpio/`.»
4. Los sidecars `.provenance.json` guardan solo el último registro (limitación de `record_metric_provenance`); el registro completo está en el jsonl.
5. El script de contraste vive en el scratchpad de la sesión; si se quiere conservar, conviene moverlo a un directorio versionado.

## Revisión 2

Veredicto: `RECHAZADO`. Todas las cifras publicadas se reproducen desde los parquet; el bloqueante es de cobertura de tests.

Verificado sin hallazgo por el revisor: recálculo independiente de las tablas nacionales (75, 180 y 900 filas) y del cribado (25, 60 y 300) con diferencia máxima 1·10⁻¹⁴; copia de `validation_by_support.py` idéntica byte a byte al CSV del paper; RMSE y sesgo globales iguales a `metrics_all.csv` y al leaderboard del cribado (≤ 4,4·10⁻¹⁶); CLI hacia directorios temporales idéntico byte a byte; métricas de MLflow iguales a los CSV (≤ 8,9·10⁻¹⁶); proveniencia vigente coherente; criterios de aceptación §8 cumplidos; 146 passed en los cuatro archivos de test y 441 en la suite completa.

### Bloqueante

1. **Ningún test comprueba que `main()` llame a `panel_check`** (`by_tier_month.py:556-561`, `tests/test_timesfm_by_tier_month.py:474-493`). Sobreviven: quitar la llamada (M7), aplicar al cribado el reparto nacional (M12) y no comprobar el total de celdas (M13). `test_main_returns_1_and_writes_nothing_when_control_fails` devuelve 1 porque `reproduction_check` también falla con datos sintéticos, y `main` no tiene tests en modo cribado (`--preds-dir`). Sin la llamada, el cribado queda sin comprobación de panel y los totales de `ll1` y `ll2` también. Corrección sugerida: un test de `main` en modo cribado sin anular `panel_check`, o un espía que confirme que se llama con `EXPECTED_CRIBADO_CELLS`.

### Menores

1. El mes tomado de `FECHA − 1 día` sobrevive a los tests (los datos sintéticos caen siempre el día 15). Con datos reales el control de `main` sí lo detecta (diciembre de `tuned` pasaría a −0,0056).
2. Sin test: «sesgo cálido de 0,11 a 0,26», los subrangos «TimesFM de 0,15 a 0,34 y `tuned` de 0,14 a 0,51» y «baja a 0,072» (hoy correctos).
3. README del benchmark: «los promedios en float32 difieren en el último decimal»; la diferencia medida en el sesgo mensual de TimesFM es de 1,7·10⁻⁸ a 2,6·10⁻⁸. La justificación es vaga.
4. TRACEABILITY: el comando del cribado no lleva `--mlflow`, pero los registros vigentes del cribado tienen `mlflow_run_id` (`7669ac26…`).
5. `by_tier_month.py:603-608`: en modo nacional `notes` registra `backtest_root=...`, que no se lee (las columnas de referencia salen del merge, idénticas al run limpio comprobado).
6. `timesfm_alerts` (`by_tier_month.py:392`, `397`) usa `abs(diff) > tol`: un NaN no genera alerta.
7. Las 20 filas de la primera corrida conservan `output_files` imprecisos; inevitable en un archivo de solo adición y documentado.
8. Estilo: el README raíz está en inglés (coherente con ese archivo); este HANDOFF usa negrita en varios sitios y conviene reducirla según `ESTILO_REDACCION.md`.

### Mutaciones que sobreviven

M3a (mes de `FECHA − 1 día`), M7, M12, M13 y M11b/c/d (afirmaciones del README). El resto de las 20 mutaciones probadas (float64 en `_error_frame` y en `score`, mes de otra columna, `ddof=1`, `loc[12]`, NaN, control después de escribir, `mlflow_run_id`, orden de `provenance_targets`, ponderación por `n`, filtro de panel, filtro de no finitos) hace fallar al menos un test.

Desviaciones de §10 aceptadas por el revisor: `PAPER_PLAN.md` sin tocar (archivo de Palacios), figura mensual omitida y `--mlflow` apagado por defecto.

## Uso de IA

Implementación, ejecución, contraste de cifras y revisiones hechas con asistencia de Claude Code; las revisiones las hacen subagentes de IA sin contexto del autor. Conviene que un experto del tema valide las cifras y los textos, conforme a la política de uso de IA del CIP.
