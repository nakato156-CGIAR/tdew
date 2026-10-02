# HANDOFF_PLAN_2: tiers de soporte (E5) y sesgo mensual (E8) de TimesFM

Fecha: 2026-10-02. Bead: `tdew-0bt` (hijo lógico de `tdew-214`). Branch: `tdew-214-tier-mes`, creada desde `tdew-u8m-paper-timesfm-narrative` (`0b53245`). Plan de origen: `PLAN_2.md`. Sin push; `main` no se toca.

## Estado

| etapa | resultado |
|---|---|
| Implementación y primera ejecución (`66cc5e5`, `5b0c3a2`) | Revisión independiente 1 (Opus, esfuerzo alto): `RECHAZADO`, 2 bloqueantes y 6 menores |
| Correcciones, MLflow y segunda ejecución (`a70645e`, `aa7207b`) | Todos los hallazgos atendidos |
| Revisión independiente 2 (Opus, contexto limpio, mutaciones y contraste desde parquet) | `RECHAZADO`, 1 bloqueante de cobertura de tests y 8 menores; ninguna cifra errónea |
| Correcciones de la revisión 2 con TDD y tercera ejecución (`4895735` y el commit de artefactos) | Todos los hallazgos atendidos; rojo → verde y mutantes muertos (ver abajo) |
| Merge | Hecho a `tdew-u8m-paper-timesfm-narrative` por instrucción expresa del usuario (`/goal`), sin una tercera revisión independiente |

No se lanzó una tercera revisión de subagente: el usuario pidió corregir con TDD y hacer el merge. En su lugar se repitieron las diez mutaciones que sobrevivían o eran sensibles (todas mueren), se repitió el contraste independiente desde los parquet y se corrió la suite completa. Conviene que una persona del equipo valide las cifras y los textos.

## Hallazgos de la revisión 1

| # | hallazgo | corrección | verificación |
|---|---|---|---|
| 1 | README citaba «0,15 a 0,51 °C» de dispersión; el mínimo real es 0,136 | README: «0,14 a 0,51 °C»; corregido también en `PLAN_2.md` §4 y §11 | `tests/test_timesfm_by_tier_month_docs.py` |
| 2 | test de float64 no fallaba sin el casteo | caso donde restar y promediar en float32 pierde `obs` (pred ≈ 2²⁵, obs < 1), con precondición explícita | mutación sin float64 en `_error_frame` y en `score`: falla |
| 3 | rama mensual del control sin verificar mes | diciembre, magnitud del máximo y mes del máximo (enero) | mutación `loc[12]`→`loc[1]`: falla el caso positivo |
| 4 | NaN pasaba el control; `main()` sin tests | `_off()` trata NaN como fallo; tests de `main()`; `--registry-path` | mutación `abs(diff) > tol`: fallan los tres casos |
| 5 | cribado sin comprobaciones de panel | `panel_check` con `EXPECTED_NATIONAL_CELLS` y `EXPECTED_CRIBADO_CELLS` | ver revisión 2 |
| 6 | `output_files` y sidecars imprecisos | `provenance_targets` (solo los CSV de cada split y método; TimesFM/`ll4` al final) | tests de `provenance_targets` |
| 7 y 8 | formato del `.md` y figura opcional sin mencionar | documentados en el README | — |

## Hallazgos de la revisión 2 y su corrección (TDD)

Los tests nuevos se escribieron primero y se confirmó que los cinco que detectan un defecto presente fallaban antes de tocar código (alertas con NaN, nota de `backtest_root`, rango de dispersión por método del README, nota de float32, comando del cribado sin `--mlflow`). Los demás pasaban sobre el código correcto y protegen contra mutaciones.

| # | hallazgo | corrección | test que ahora lo protege |
|---|---|---|---|
| Bloqueante | ningún test comprobaba que `main()` llame a `panel_check` (M7, M12, M13) | cuatro tests de `main` (cribado con su panel y sin control nacional; cribado que falla y no escribe; nacional con panel esperado; nacional que falla solo por el total) y un test de `panel_check` donde solo cambia el total | `test_main_cribado_*`, `test_main_national_*`, `test_panel_check_total_is_checked_independently_of_the_listed_tiers` |
| Menor 1 | mes de `FECHA − 1 día` sobrevivía | tests con fechas en el primer y último día del mes, para mensual y mes × tier | `test_month_is_the_calendar_month_of_fecha_on_month_edges` |
| Menor 2 | afirmaciones del README sin test | un test por afirmación: rango cálido, dispersión por método, brechas de `within` y `unsupported` | `test_warm_bias_range_*`, `test_per_method_dispersion_*`, `test_tier_gap_endpoints_*` |
| Menor 3 | nota de float32 vaga | el README cita la magnitud medida: hasta 1,7·10⁻⁸ °C en TimesFM y 8·10⁻⁹ °C en `tuned` | `test_float32_note_states_the_measured_magnitude` |
| Menor 4 | comando del cribado sin `--mlflow` | agregado a TRACEABILITY | `test_traceability_cribado_command_includes_mlflow` |
| Menor 5 | nota nacional con `backtest_root` no leído | la nota nacional dice `merged_root=...`; la del cribado conserva `backtest_root` | `test_national_notes_*`, `test_cribado_notes_*` |
| Menor 6 | alertas de TimesFM ignoraban NaN | `timesfm_alerts` usa `_off()` | `test_timesfm_alerts_flag_nan_*` |
| Menor 7 | filas de la primera corrida con `output_files` imprecisos | sin cambio: el jsonl es de solo adición | — |
| Menor 8 | estilo | negritas reducidas en este archivo; el README raíz sigue en inglés, como el resto de ese archivo | — |

Error propio encontrado al escribir los tests: el README citaba «TimesFM de 0,15 a 0,34» y el máximo real es 0,3348, que redondea a 0,33. Se corrigió a 0,33.

Mutantes comprobados tras la corrección (todos hacen fallar al menos un test): mes de `FECHA − 1 día`, `main` sin `panel_check`, cribado con el reparto nacional, cribado con el total nacional, total sin comprobar en `panel_check`, alertas que ignoran NaN, tres cifras del README alteradas y la nota nacional con `backtest_root`.

## MLflow

`by_tier_month.py --mlflow` (apagado por defecto) registra una corrida de evaluación por split en el experimento `tdew-timesfm-benchmark` de `mlflow.db`, ignorada por git. TimesFM no entrena: son evaluaciones. Métricas: `<método>_<tier>_<métrica>`, `<método>_{rmse,bias,skill}_all` (ponderadas por `n`), `<método>_bias_mNN` y, en `ll4`, `<método>_cell_bias_std_mNN`. El `run_id` queda en `mlflow_run_id` de la proveniencia.

Corridas vigentes (tercera ejecución, commit `4895735`): `6d94bab9…` (`nacional_17027_limpio`, `ll1`), `5e7267d2…` (`ll2`), `de7dd675…` (`ll4`) y `4c2c366b…` (`cribado_1092_limpio`, `ll4`). Las corridas de las ejecuciones anteriores siguen en el servidor (`f9200a84…`, `b5494815…`, `477aa973…`, `7669ac26…`, de la segunda) y no se borran. Servidor: `uv run mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000`.

## Ejecución y artefactos vigentes

Los dos comandos de `PLAN_2.md` §7 se ejecutaron tres veces. Los siete CSV (más `tiers_texto_limpio.{csv,md}`) son idénticos byte a byte en las tres. `reports/metric_provenance.jsonl` es de solo adición: la primera ejecución dejó 20 filas (commit `66cc5e5`), la segunda otras 20 (`a70645e`, con `mlflow_run_id`) y la tercera otras 20 (`4895735`, con notas corregidas). Las vigentes son las de la tercera; las anteriores se conservan sin cambios y quedan reemplazadas.

Tabla comparativa contra Palacios (`ll4`, 17.027 celdas, run limpio):

| tier | celdas | RMSE TimesFM | RMSE `tuned` | ΔRMSE | sesgo TimesFM | sesgo `tuned` | skill TimesFM | skill `tuned` |
|---|---|---|---|---|---|---|---|---|
| within | 8.306 | 0,867 | 0,946 | 0,079 | +0,050 | +0,010 | 0,314 | 0,251 |
| near | 1.779 | 1,061 | 1,139 | 0,078 | +0,068 | −0,079 | 0,275 | 0,222 |
| marginal | 1.433 | 1,198 | 1,276 | 0,078 | +0,143 | −0,044 | 0,242 | 0,193 |
| extrapolated | 2.563 | 1,298 | 1,374 | 0,077 | +0,149 | −0,070 | 0,228 | 0,183 |
| unsupported | 2.946 | 1,652 | 1,724 | 0,072 | +0,223 | −0,089 | 0,188 | 0,153 |
| todos | 17.027 | 1,1536 | 1,2279 | 0,0743 | +0,104 | −0,033 | 0,2485 | 0,2001 |

Sesgo mensual `ll4` (TimesFM / `tuned`, °C): enero −0,325 / −0,402; diciembre +0,089 / +0,017; TimesFM de +0,11 a +0,26 entre marzo y septiembre; solo enero y octubre tienen menor |sesgo| en TimesFM. Tablas completas en `reports/timesfm_benchmark/README.md` (secciones «Soporte observacional» y «Sesgo mensual») y en los CSV de `nacional_limpio/` y `cribado_limpio/`.

## Contraste con datos y reproducción reales

Script independiente (no importa `by_tier_month`; agrega con `np.bincount` desde los parquet), ejecutado sobre la tercera ejecución con 0 fallas:

- Recálculo total: 75 filas de tiers, 180 mensuales y 900 mes × tier nacionales, y 25, 60 y 300 del cribado, con diferencia máxima 5·10⁻¹³ (`n` y `cells` exactos).
- Reproducción del paper: una copia de `validation_by_support.py` sobre `backtest_clean` da exactamente `validation_by_support.csv`; `tuned` de `tiers_limpio.csv` coincide con él y con `tbl-tiers` de `paper.qmd` a tres decimales.
- Consistencia con PLAN_1: el RMSE y el sesgo globales ponderados por `n` igualan `nacional_limpio/metrics_all.csv` (≤ 4·10⁻¹⁶) y las cifras del HANDOFF_PLAN_1; `n` es igual a los pares del run limpio (6.231.882 / 12.446.737 / 24.876.447); los cinco métodos del cribado igualan `cribado_limpio/leaderboard.csv`.
- Determinismo: el CLI hacia directorios y registro temporales reproduce los CSV byte a byte (comprobado por la revisión 2 y por el autor).
- MLflow: `rmse_all` de las corridas nacionales vigentes iguala `metrics_all.csv` (9 comparaciones) y el de la corrida del cribado iguala el leaderboard (0,8389 TimesFM, 0,9326 `tuned`).
- El jsonl anterior es prefijo exacto del nuevo.

## Pendientes y advertencias

1. Cerrar el bead `tdew-0bt` y marcar la fila de Notion (`Bead ID = tdew-0bt`: `Completed`, `Progress = 1`), si no se hizo ya al cerrar la sesión.
2. La figura mensual opcional del paso 5 no se generó.
3. `PAPER_PLAN.md` y `paper.qmd` no se tocaron (el archivo es de Palacios). Texto propuesto, en inglés: «2026-10-02 — TimesFM vs `tuned` by observational-support tier and by month (bead `tdew-0bt`, `PLAN_2.md`). ll4: TimesFM RMSE below `tuned` in all five tiers (0.867 vs 0.946 within; 1.652 vs 1.724 unsupported); `tuned` reproduces `tbl-tiers` exactly. Monthly bias: December `tuned` +0.017, max |bias| 0.402 (January); TimesFM max |bias| 0.325 (January), warm +0.11 to +0.26 °C in March–September. Outputs under `reports/timesfm_benchmark/nacional_limpio/`.»
4. Los sidecars `.provenance.json` guardan solo el último registro (limitación de `record_metric_provenance`); el registro completo está en el jsonl.
5. El script de contraste vive en el scratchpad de la sesión; si se quiere conservar, conviene moverlo a un directorio versionado.
6. Ninguna comparación del cribado debe leerse como estimador del campo: es una muestra estratificada con 842 de 1.092 celdas `within`.

## Uso de IA

Implementación, ejecución, contraste de cifras y revisiones hechas con asistencia de Claude Code; las dos revisiones independientes las hicieron subagentes de IA sin contexto del autor. Conviene que un experto del tema valide las cifras y los textos, conforme a la política de uso de IA del CIP.
