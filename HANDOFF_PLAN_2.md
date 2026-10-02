# HANDOFF_PLAN_2: tiers de soporte (E5) y sesgo mensual (E8) de TimesFM

Fecha: 2026-10-02. Bead: `tdew-0bt` (abierto). Branch: `tdew-214-tier-mes`, creada desde `tdew-u8m-paper-timesfm-narrative` (`0b53245`). Plan de origen: `PLAN_2.md`. Commits: `66cc5e5` (código y tests) y `5b0c3a2` (CSV `_limpio`, proveniencia y documentación). Sin merge y sin push.

## Estado

Implementación completa salvo la figura mensual opcional (paso 5 del plan, omitida; el plan no depende de ella). El control de reproducción pasó y la suite completa da 414 passed. La revisión independiente de un subagente Opus (esfuerzo alto, sin contexto de la implementación) terminó con `VEREDICTO: RECHAZADO` por dos hallazgos bloqueantes. Por instrucción del usuario, la branch se deja sin corregir ni mezclar hasta una revisión posterior. `PAPER_PLAN.md` no se tocó.

## Hallazgos bloqueantes

1. **Rango de dispersión erróneo en el README.** En «Sesgo mensual», el texto dice «La dispersión entre celdas (0,15 a 0,51 °C)». El mínimo real entre TimesFM y `tuned` en `ll4` es 0,136 (`tuned`, abril), que la propia tabla muestra. Por método: TimesFM de 0,150 a 0,335 y `tuned` de 0,136 a 0,505. La cifra se copió de PLAN_2 §4 sin contrastarla. Corrección: «0,14 a 0,51 °C» (y, si procede, corregir el mismo rango en PLAN_2 §4 y §11).
2. **Test de float64 vacuo.** `tests/test_timesfm_by_tier_month.py:164-177` (`test_float32_inputs_are_aggregated_in_float64`) usa un valor constante float32(0,1) con `obs = 0`; con ese caso el promedio en float32 es igual al de float64. Quitar el `dtype="float64"` de `_error_frame` no hace fallar el test (mutación comprobada). La aserción sobre `dtype` es tautológica. Corrección: un caso donde el promedio en float32 sí difiera del de float64 (por ejemplo, muchos valores heterogéneos con `obs` distinta de cero) que falle sin el casteo.

## Hallazgos menores

3. `reproduction_check`, rama mensual (`by_tier_month.py` ~325-332): ningún test verifica que se use diciembre ni que el máximo |sesgo| caiga en enero, y no hay un caso positivo con `monthly`. Cambiar `m.loc[12]` por `m.loc[1]` no rompe ningún test.
4. `abs(nan - x) > tol` es `False`: un RMSE o sesgo `tuned` NaN pasaría el control como OK. `main()` no tiene tests; por lectura, el control corre antes de escribir los CSV y devuelve 1 si falla.
5. El modo cribado no verifica 1.092 celdas ni el reparto 842/79/59/65/47 (paso 4 del plan); en `ll1` y `ll2` tampoco se verifica la suma de 17.027. Los datos sí cumplen.
6. Cada `.provenance.json` guarda solo el último registro escrito (`zone_ols`, `ll4`), comportamiento ya presente en PLAN_1. Los registros de `ll1`/`ll2` y de `tmin`/`zone_ols` listan `tiers_texto_limpio.csv` en `output_files` aunque ese archivo solo contiene `ll4` con TimesFM, `tuned` y climatología. El plan pedía un registro por CSV; se implementó uno por (split, método).
7. `tiers_texto_limpio.md` usa punto decimal y miles en inglés (como `tbl-tiers`) con encabezados en español.
8. El README no menciona que la figura mensual opcional se omitió.

## Verificado sin hallazgos

Recálculo independiente desde los parquet (sin importar `by_tier_month`): todas las filas de los CSV nacionales coinciden con diferencia menor que 1e-9 en `ll1`, `ll2` y `ll4`, incluidos `n`, `cells`, desviación con `ddof=0` y percentiles. RMSE `ll4` de TimesFM por tier: 0,8669 / 1,0614 / 1,1983 / 1,2976 / 1,6522; de `tuned`: 0,9464 / 1,1388 / 1,2762 / 1,3742 / 1,7237 (coincide con `validation_by_support.csv` y `tbl-tiers`). Sesgo mensual `ll4`: TimesFM enero −0,325 y diciembre +0,089; `tuned` enero −0,402 y diciembre +0,017. Uniones sin duplicados ni pérdida de filas, 0 celdas sin tier. Sin cambios en `reports/paper/`, `PAPER_PLAN.md`, `nacional/` ni `cribado/`; el jsonl solo ganó 20 líneas. Criterios de aceptación §8: los ocho cumplidos (el 6 en el código, sin protección de test por el hallazgo 2).

## Pasos para cerrar

1. Corregir los hallazgos 1 y 2 y, de preferencia, 3 a 5; re-ejecutar `uv run pytest`.
2. Volver a lanzar la revisión independiente.
3. Si el veredicto es `APROBADO`: `git switch tdew-u8m-paper-timesfm-narrative && git merge --no-ff tdew-214-tier-mes`, `bd close tdew-0bt` y actualizar la fila de Notion con `Bead ID = tdew-0bt` (`Completed`, `Progress = 1`).

## Uso de IA

Implementación y revisión hechas con asistencia de Claude Code; la revisión la hizo un subagente de IA sin contexto del autor. Conviene que un experto del tema valide las cifras y los textos, conforme a la política de uso de IA del CIP.
