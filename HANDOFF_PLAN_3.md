# HANDOFF_PLAN_3: producto TimesFM 2017–2020 (E9)

Fecha: 2026-10-02. Bead: `tdew-214.13` (hijo de `tdew-214`). Rama: `tdew-214-real-2017-2020`, creada desde `tdew-u8m-paper-timesfm-narrative`. Plan de origen: `PLAN_3.md`. Sin push.

## Estado

| etapa | resultado |
|---|---|
| Implementación (split `real`, `real.py`, `real_compare.py`, MLflow, proveniencia) | hecha con tests primero |
| Smoke test de los buckets 0 y 1 | pasado (ver abajo) |
| Revisión independiente (Opus, contexto limpio, mutaciones y contraste con datos reales) | `APROBADO`, 0 bloqueantes, 10 menores y 4 dudas; ver abajo |
| Correcciones de la revisión (TDD) | M-1 a M-6, M-8 y M-10 hechas; suite completa 561 en verde; bucket 0 reproduce el sha256 del smoke |
| Corrida completa (8.192 buckets) | **no lanzada**; requiere aviso previo y visto bueno del usuario |

## Desviaciones respecto de PLAN_3

- `--cells-per-batch` no existe: un bucket (≤ 271 celdas) es un solo panel y `predict_panel` lo parte en lotes de `--batch-size`.
- `--batch-size` por defecto 32 (PLAN_3 no fijaba el valor; `run.py` usa 4). Medido: 4 → 3,4; 16 → 4,1; 32 → 4,4 celdas/s, con salida idéntica bit a bit.
- MLflow en `real.py` y `real_compare.py` (`--mlflow`); PLAN_3 decía que esta corrida no abría MLflow.
- Estimación nueva de la corrida completa: ≈ 5,9 días (PLAN_3: 5,6) y ≈ 158 GB (PLAN_3: 146–168).
- `tests/test_metric_provenance.py`: se registran los CSV del smoke y `real_limpio` se excluye del criterio de PLAN_1 sobre paneles nacional/cribado.

## Smoke test (buckets 0 y 1, 528 celdas)

| medida | valor |
|---|---|
| celdas escritas / omitidas | 528 / 0 |
| filas | 771.408 |
| violaciones de monotonía de cuantiles | 0 |
| tasa | 4,36 celdas/s (batch 32) |
| bytes por fila | 49,58 |
| acuerdo TimesFM − Palacios | sesgo +0,053 °C, RMSE 0,462 °C, MAE 0,319 °C, r 0,9986 |
| NaN / infinitos | 0 / 0 |

Reanudación probada (relanzar salta los buckets con `.done`). Interrupción con `SIGINT` en la predicción del bucket 2: sin `pred.parquet`, `.tmp` ni `.done`; la misma orden lo completó. La interrupción durante la escritura se cubre con un test unitario.

Corridas MLflow (`tdew-timesfm-benchmark`): `fba171b1…` (smoke con batch 4, exploratorio), `bceb411e…` (smoke con batch 32) y `8d2ef220…` (comparación). Los registros de proveniencia de las tres están en `reports/metric_provenance.jsonl` (solo adición). Los CSV de la comparación están en `reports/timesfm_benchmark/real_limpio/smoke_b0_1/`.

## Revisión independiente

Antes de corregir, el revisor recalculó desde los parquet reales el panel, la conversión a °C (con GPU, diferencia 0,0) y las cifras de acuerdo, y todo coincidió. Hallazgos y estado:

| # | hallazgo | estado |
|---|---|---|
| M-1 | el prefetch cargaba cada bucket 4 veces (`setdefault` evalúa `submit`) | corregido; `test_prefetch_loads_each_bucket_exactly_once` |
| M-2 | sin defensa contra un panel de otro bucket | corregido en `run_bucket`; tests con 2 y 4 buckets |
| M-3 | `--verify-only` caía ante un parquet corrupto y dejaba un `verify_real.csv` viejo; sin sha256 | corregido: se informa por bucket, se compara sha256 y se borra el CSV previo |
| M-4 | la nota decía «TF32 activado» con `--no-tf32` | corregido |
| M-5 | `run.py --split real` registraba una proveniencia incorrecta | ese camino ahora se rechaza; el producto se corre con `real.py` |
| M-6 | un subconjunto o `--verify-only` reescribía `bucket_plan.csv` | corregido: el plan solo se escribe con `--plan-only` o en la corrida completa |
| M-8 | nada impedía escribir bajo `$RES` | `refuse_under_res` en `real.py` y `real_compare.py` (`$RES` es escribible por este usuario) |
| M-10 | mutaciones sobrevivientes (deciles sin climatología, orden, bytes, `bucket_done` sin parquet) | tests nuevos; quedan sin cubrir M8 (HAC), M17 (tolerancia 0,05) y RMSE por celda |
| M-7 | un bucket con fallo de datos detiene la corrida y no hay `--exclude-buckets` | pendiente, no bloquea |
| M-9 | falta `run_summary_limpio.csv`, figuras y mapa; corte por departamento solo cubre los 4 sitios; `real_compare` toma buckets por `pred.parquet` y no por `.done` | pendiente (pasos 8 a 10 de PLAN_3) |
| D-1 | el retardo HAC (30 días) cambia el error estándar de la pendiente entre 0,014 y 0,025 °C/año; la diferencia tiene ciclo estacional | pendiente: informar sensibilidad al retardo en el análisis final |
| D-2 | `CODE_VERSION` es manual y el `.done` no compara `tf32`, raíces ni `git_commit` | pendiente |
| D-3 | `pred` es idéntico a `q50` (≈ 12,7 GB redundantes) | sin cambio: el formato está fijado en PLAN_3 |

Incidente del revisor: creó y borró de inmediato un archivo vacío bajo `$RES` (queda solo el cambio de mtime del directorio).

## Pendiente

1. Revisión independiente y, si aprueba, merge.
2. Visto bueno del usuario y corrida larga (`tmux`, watcher escalonado).
3. Tras la corrida: `--verify-only`, `real_compare.py` completo, figuras, README del benchmark, `TRACEABILITY.md`, `limitaciones.md`.
