# HANDOFF_PLAN_3: producto TimesFM 2017–2020 (E9)

Fecha: 2026-10-02. Bead: `tdew-214.13` (hijo de `tdew-214`). Rama: `tdew-214-real-2017-2020`, creada desde `tdew-u8m-paper-timesfm-narrative`. Plan de origen: `PLAN_3.md`. Sin push.

## Estado

| etapa | resultado |
|---|---|
| Implementación (split `real`, `real.py`, `real_compare.py`, MLflow, proveniencia) | hecha con tests primero |
| Smoke test de los buckets 0 y 1 | pasado (ver abajo) |
| Revisión independiente (Opus, esfuerzo alto) | pendiente |
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

## Pendiente

1. Revisión independiente y, si aprueba, merge.
2. Visto bueno del usuario y corrida larga (`tmux`, watcher escalonado).
3. Tras la corrida: `--verify-only`, `real_compare.py` completo, figuras, README del benchmark, `TRACEABILITY.md`, `limitaciones.md`.
