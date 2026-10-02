# PLAN_3: producto TimesFM 2017–2020 sobre las 2.178.827 celdas con Td (E9)

Versión final. Fecha: 2026-10-02. Bead padre: `tdew-214` (se propone una subtarea nueva, hermana de las de PLAN_1 y PLAN_2).

## Experimentos que cubre este plan

Los códigos E# son nuestros (E1–E16, numerados para esta comparación). No son los del paper de Palacios (`reports/paper/paper.qmd`).

| # | Experimento (en el paper) | Qué mide |
|---|---|---|
| E9 | Producto 2017–2020 (`fig-map`, `fig-timeseries`, QC del relleno) | Predicción diaria de Td del hueco real 2017-01-01 a 2020-12-31 sobre 2.178.827 celdas (3.183.266.247 valores). Media nacional (paper: 19,39 °C), medias anuales (19,36 / 19,30 / 19,41 / 19,51 °C), rango (−13,29 a 41,16 °C) y ausencia de deriva bajo autorregresión sostenida de 1.461 días |

Este plan depende de PLAN_1 (E2–E4) y de PLAN_2 (E5, E8) en lo documental. La inferencia en sí no consume sus salidas (ver sección 3). Habilita el PLAN_4: E10 (costura 2016/2017), E11 (cola cálida, Td > 35 °C) y E12 (cota Td ≤ Tmin + k).

## 0. Decisiones tomadas

1. **Cobertura.** Panel completo de 2.178.827 celdas, que son los IDs del producto de Palacios (`$RES/tuning/predictions_2017_2020`). Mismo horizonte, 2017-01-01 a 2020-12-31 (1.461 días). No se submuestrea y no se usan pesos. Antes de la corrida larga se hace un smoke test de 2 buckets, que no es entregable.
2. **Variante.** Solo `tmin_anom_full`: objetivo anomalía de Td, covariable futura anomalía de Tmin, contexto completo. Es la ganadora del benchmark.
3. **Split nuevo `real`.** Contexto 1981-01-01 a 2016-12-31 (13.149 días, más largo que el de `ll4`, 11.688). Horizonte 2017–2020 en una sola pasada, sin reentrenar ni re-emitir.
4. **Tmin 2017–2020.** Se lee de `$RES/future_tmin_by_bucket/id_bucket=XXXX/future_tmin_{2017..2020}.parquet` (solo lectura). Es el mismo insumo del relleno de Palacios, ya regridado.
5. **Formato de salida.** Una carpeta por bucket con `pred.parquet`, con `ID` int32, `day` int16 (días desde 2017-01-01, 0 a 1460), `pred` y los nueve deciles `q10`…`q90` en float32 (46 B por fila sin comprimir), con compresión zstd. Destino: `/home/cvelasquez/tdew_timesfm/preds_real/`. No se escribe bajo `$RES`.
6. **Reanudable.** La unidad de trabajo es un bucket. Cada bucket termina con un archivo sentinela `.done` y se escribe de forma atómica. Reanudar es relanzar el mismo comando.
7. **Contrato con PLAN_4.** Este plan deja el producto completo, validado y con manifiesto de buckets. PLAN_4 solo lee y no vuelve a inferir.
8. **Vigilancia.** Corrida en `tmux` bajo el protocolo escalonado de la memoria `background-training-watcher-protocol` (1 h, 5 h, 8–12 h), más vigilancia continua del log.
9. **Licencia.** Los pesos de TimesFM 3.0 no permiten uso comercial ni productivo (`limitaciones.md`, sección 9). El producto es un entregable de investigación y no un producto operativo. Esto queda en el addendum, el README y la proveniencia.

## 1. Objetivo

Producir el equivalente, con TimesFM 3.0 zero-shot, del producto de relleno 2017–2020 de Palacios. Con él se puede comparar ambos productos celda a celda y día a día (E9). Además se dejan guardados el valor central y los nueve deciles para que el PLAN_4 (E10, E11, E12) no requiera ninguna re-corrida.

No hay verdad observada de Td para 2017–2020. Por eso el análisis es de acuerdo entre productos (sesgo, RMSE y correlación TimesFM − Palacios), no de error. En ningún texto se usa la palabra «error» para esas métricas.

## 2. Alcance

Entra en este punto:

- Código del split `real` en `panel.py` y su lectura de Tmin futura. No cambia el comportamiento de `ll1/ll2/ll4`.
- Corrida por buckets `experiments/timesfm/real.py` con sentinela, reanudación, verificación de espacio y proveniencia.
- Smoke test de 2 buckets.
- Corrida completa (~5,6 días estimados) en `tmux` con watcher.
- Verificación de integridad del producto (filas, celdas, dtypes, NaN, rango).
- Análisis de acuerdo TimesFM−Palacios: `experiments/timesfm/real_compare.py`.
- Figuras de apoyo (serie nacional, mapa de diferencia) y control de reproducción de las cifras de Palacios.
- Tests, proveniencia, addendum de manifiesto y documentación.

## 3. Dependencias

- **PLAN_1 y PLAN_2.** No son prerrequisito técnico de la inferencia. Esta lee solo `bucketed_training_data`, `future_tmin_by_bucket` y el producto de Palacios. La corrida larga puede lanzarse en cuanto el smoke test pase, incluso antes de cerrar PLAN_1 y PLAN_2.
- **Sí dependen de ellos.** El README, `TRACEABILITY.md` y el addendum se redactan después de que PLAN_1 haya creado `docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`. Este plan reutiliza de PLAN_1 la constante `MANIFEST_REF_LIMPIO` de `evaluate.py` y las convenciones de sufijo `_limpio`. No se redefinen aquí.
- **Habilita PLAN_4.** Debe estar completo el producto (`preds_real/`) y su manifiesto de buckets.
- **GPU.** La GPU es única (RTX A2000 12 GB, 2 GB ocupados por otros procesos). Mientras corra la inferencia no se lanzan otras cargas sobre ella.

## 4. Pre-condiciones verificadas

Verificadas con lecturas reales, sin escribir archivos ni bajo `$RES`.

| Hecho | Evidencia |
|---|---|
| Tmin futura ya está regridada y por bucket. | `$RES/future_tmin_by_bucket/` tiene 8.192 buckets, 6,3 GB. Cada uno contiene `future_tmin_{2017..2020}.parquet` con `ID` int64, `FECHA` timestamp[us], `TMIN` float32. El bucket 0 tiene 125.925 filas en 2017 (345 celdas × 365 días). |
| Cada bucket cubre la grilla completa (2.818.404 IDs), no solo las celdas con Td. | 2.818.404 / 8.192 ≈ 344 celdas por bucket, frente a ≈ 266 con Td. |
| El producto de Palacios existe y tiene el esquema esperado. | `$RES/tuning/predictions_2017_2020/id_bucket=*/pred.parquet`: 8.192 buckets, 31 GB, columnas `FECHA` timestamp[ns], `ID` int64, `TD_predicted` float64. El bucket 0 tiene 385.704 filas (264 celdas × 1.461 días). |
| Las celdas de Palacios son las que tienen Td. | 3.183.266.247 / 1.461 = 2.178.827 celdas, igual que la cobertura Td v1.1. |
| `panel.py` solo conoce los splits `ll1/ll2/ll4`. | `SPLITS` define `ll1: (2015,(2016,2016))`, `ll2: (2014,(2015,2016))`, `ll4: (2012,(2013,2016))`. `run.py` restringe `--split` a esas tres opciones. |
| `build_panel` exige `TD` y `TMIN` completos en el hold-out. | Lee `train_YYYY.parquet` del bucket para `context_start_year…holdout_end` y descarta celdas con NaN en contexto u hold-out. Para el hold-out 2017–2020 `bucketed_training_data` no tiene datos. |
| La covariable futura debe medir contexto + horizonte. | `build_inputs` lanza `ValueError` si el ancho no es 13.149 + 1.461 = 14.610. |
| La climatología se calcula solo con años de contexto. | En `build_panel` sale de `ctx.groupby(["ID","doy"])`, replicando `backtest.train_only_climatology`. Para `real` usa 1981–2016. `doy` 366 queda cubierto por los años bisiestos del contexto. |
| El esquema actual de salida pesa 53 B por fila. | `preds_cribado/ll4__tmin_anom_full.parquet`: 84,3 MB para 1.092 celdas × 1.461 días (1.595.412 filas) con zstd. |
| Tiempo medido. | 5,09 celdas/s con TF32 en RTX A2000 (cuello: longitud del contexto, ~proporcional). 2.178.827 / 5,09 ≈ 4,95 días con contexto ll4. Con el contexto de `real` (×1,125) ≈ 5,6 días. Un bucket de ≈ 266 celdas toma ≈ 52 s (cálculo, no medición). |
| Rendimiento no escala con más procesos. | Tres procesos rindieron 4,59 celdas/s agregadas contra 5,39 con uno. El límite es la potencia (70 W). |
| Espacio. | `/`: 320 GB libres (65 % usado). `/home/cvelasquez/tdew_timesfm` ocupa 28 GB. `/media/ppalacios/Data1`: 872 GB libres, pero no se escribe bajo `$RES`. |
| Tamaño estimado del producto. | 3,183e9 filas × 46 B ≈ 146 GB sin comprimir. Con el 53 B del esquema anterior serían 168 GB. Deja `/` entre 81 % y 83 % ocupado. La compresión de float32 aleatorio es baja; se mide en el smoke test. |
| No hay otras cargas de GPU ni entrenamientos activos. | `nvidia-smi`: 1.993 MiB en uso, 0 % de utilización. Corre un `tmux` del usuario (pid 392396) y servidores ajenos que no usan GPU. |

Pendiente de verificar en el smoke test (no medido todavía): (a) tamaño máximo de bucket con Td (para fijar `cells_per_batch`), (b) que `train_1981…2016.parquet` existen en cada bucket, (c) la proporción de compresión real, (d) cuántas celdas con Td tienen contexto completo y Tmin futura completa (se espera que sean todas).

## 5. Principio de no sobrescritura

- No se escribe bajo `$RES`. `future_tmin_by_bucket`, `bucketed_training_data`, `predictions_2017_2020` y `zone_table.parquet` se leen solamente.
- No se modifica nada en `reports/paper/scripts/` (`qc_fill.py`, `make_paper_figs.py`). Los controles de QC se reimplementan en el script nuevo.
- `docs/protocol/timesfm_manifest.yaml` y el addendum de PLAN_1 no se modifican. Se crea un addendum nuevo, aparte.
- `preds_nacional/`, `preds_cribado/`, `preds_departamental/` y `preds_escala/` no se tocan. El producto nuevo va a `preds_real/`.
- Los resultados publicados nuevos llevan sufijo `_limpio` y van a `reports/timesfm_benchmark/real_limpio/`. Ninguno usa el run con fuga (`$RES/tuning/backtest`).
- `reports/metric_provenance.jsonl` es de solo adición.
- Un bucket con `.done` no se reescribe. Para rehacerlo hay que borrar ese bucket a mano.

## 6. Diseño

### 6.1 Split `real` (`panel.py`)

- Añadir `"real": (2016, (2017, 2020))` a `SPLITS`. `SplitSpec` ya calcula `context_length` = 13.149 y `horizon` = 1.461.
- Añadir a `build_panel` el parámetro `future_root: Path | None = None`. Para el split `real`:
  - El hold-out no se lee de `bucketed_training_data`. `TMIN` de 2017–2020 se lee de `future_root/id_bucket=XXXX/future_tmin_{year}.parquet`, filtrado a los IDs pedidos.
  - `td_hold` se devuelve como NaN con forma `(N, 1461)` (no existe verdad). El campo sigue siendo el mismo, para no cambiar `PanelBatch`.
  - El filtro de completitud exige contexto completo (`TD` y `TMIN`, 13.149 días) y `TMIN` futura completa (1.461 días). No exige `TD` en el hold-out.
  - `tmin_clim` y `td_clim` se calculan con el contexto, como hoy.
- `run.py` solo cambia en `choices` de `--split` y en una opción `--future-root`, para que `python -m experiments.timesfm.run --split real` siga siendo posible con una sola variante. La corrida larga no usa ese camino, sino `real.py`.
- Los splits `ll1/ll2/ll4` se comportan igual (los tests existentes `test_timesfm_panel.py` y `test_timesfm_inputs.py` lo comprueban).

### 6.2 Corrida por buckets (`experiments/timesfm/real.py`)

Funciones:

- `list_cells(palacios_root) -> dict[int, np.ndarray]`. Lee solo la columna `ID` de cada `pred.parquet` de Palacios y agrupa por bucket (`ID % 8192`). Escribe `ids_real_2178827.csv` y `bucket_plan.csv` (bucket, celdas) en `preds_real/`. Falla si el total no es 2.178.827.
- `bucket_done(out_dir, bucket) -> bool`. Verdadero si existe `.done` y su JSON coincide con el `ids_hash` y la versión del código actual.
- `run_bucket(model, spec, bucket, ids, *, historical_root, future_root, out_dir, batch_size, cells_per_batch) -> dict`. Arma el panel con `build_panel`, llama a `build_inputs`, `predict_panel` y `to_physical` (de `run.py`), construye la tabla con `ID` int32, `day` int16, `pred` y `q10…q90`, y la escribe de forma atómica (ver 6.3). Devuelve el resumen del bucket.
- `run_real(...)`. Recorre los buckets en orden ascendente (el bucket es `ID % 8192`, por lo que cada uno mezcla ubicaciones de todo el país y cualquier prefijo es una muestra geográficamente dispersa). Salta los que tienen `.done`. Antes de cada bucket verifica el espacio libre (6.4). Carga el modelo una sola vez.
- Lectura anticipada: un hilo (o pool de 2–4) prepara el panel del bucket siguiente mientras la GPU procesa el actual. `iter_panel_batches` no sirve aquí porque mezcla celdas de varios buckets y no permite sentinela por bucket.
- `verify_outputs(out_dir, palacios_root) -> pd.DataFrame`. Revisa los 8.192 buckets (ver 10).
- `main(argv)`. Opciones: `--ids-from-palacios`, `--out-dir`, `--historical-root`, `--future-root`, `--palacios-root`, `--buckets` (rango o lista, para el smoke test), `--batch-size`, `--cells-per-batch`, `--min-free-gb` (por defecto 60), `--no-tf32`, `--bead-id`, `--verify-only`.

### 6.3 Escritura atómica y sentinela

- Se escribe `id_bucket=XXXX/pred.parquet.tmp` y, al terminar sin error, se renombra a `pred.parquet`. Luego se escribe `id_bucket=XXXX/.done` (JSON) y se hace `fsync`.
- El `.done` contiene: bucket, celdas pedidas, celdas escritas, celdas omitidas (con IDs y motivo), filas, bytes, sha256 del Parquet, segundos, celdas/s, `git_commit`, `ids_hash`, fecha, TF32 y versión de `timesfm`.
- Al arrancar se borran los `pred.parquet.tmp` huérfanos (corrida interrumpida). Un bucket sin `.done` se rehace completo.
- Esquema fijo: `ID` int32, `day` int16, `pred` float32, `q10…q90` float32, zstd. Filas ordenadas por `(ID, day)`. `FECHA` se reconstruye como `2017-01-01 + day`.
- `preds_real/MANIFEST.csv` (una fila por bucket) se regenera al final desde los `.done`. Es el contrato de lectura para PLAN_4.

### 6.4 Disco

- Antes de cada bucket se verifica `shutil.disk_usage` sobre `preds_real/`. Si queda menos de `--min-free-gb` (60 GB), la corrida termina con código distinto de 0 y un mensaje claro. Los `.done` conservan el progreso.
- El watcher avisa con menos de 100 GB libres.
- Si se cruza el umbral:
  1. Se pausa y no se borra nada sin avisar.
  2. Se revisa qué ocupa `/home/cvelasquez/tdew_timesfm` (28 GB de corridas anteriores, regenerables, pero la decisión es del usuario).
  3. Opciones: liberar espacio con aprobación; o mover buckets ya completos a `/media/ppalacios/Data1` en un directorio propio fuera de `$RES`, con autorización de Palacios y dejando un enlace simbólico; o reducir el coste con float16 en deciles (decisión de formato nueva, requiere aprobación porque cambia el contrato con PLAN_4).
  4. Se relanza el mismo comando.

### 6.5 Rendimiento

- TF32 activado (`enable_tf32`), como en el benchmark. `make_positive=False` (igual que todo el benchmark).
- Un solo proceso en GPU. `--shard` no se usa.
- `cells_per_batch` ≥ tamaño máximo de bucket (se fija en el smoke test), de modo que cada bucket sea un solo lote y no haya restos pequeños e ineficientes.
- Si la GPU lanza OOM, `predict_panel` ya reintenta con menos `per_core_batch_size`.

## 7. Pasos

**Paso 1. Código del split.**
- Editar `experiments/timesfm/panel.py`: `SPLITS["real"]`, parámetro `future_root`, ramas de lectura y filtro descritas en 6.1.
- Editar `experiments/timesfm/run.py`: `choices` y `--future-root`.
- Correr `uv run pytest tests/test_timesfm_panel.py tests/test_timesfm_inputs.py` (sin regresiones en `ll*`).

**Paso 2. `real.py`.**
- Crear `experiments/timesfm/real.py` con las funciones de 6.2. Importar de `run.py` `load_model`, `predict_panel`, `build_inputs`, `to_physical`, `enable_tf32`, `QUANTILE_COLUMNS` y `variant`. No duplicar.
- Incluir `build_real_provenance(...)`, análogo a `build_provenance` de `run.py` (ver 11).

**Paso 3. Tests (sin GPU).** Escribir `tests/test_timesfm_real.py` (ver 11) y correrlo.

**Paso 4. Lista de celdas.**
```bash
uv run python -m experiments.timesfm.real --palacios-root $RES/tuning/predictions_2017_2020 \
  --out-dir /home/cvelasquez/tdew_timesfm/preds_real --ids-from-palacios --plan-only
```
Resultado esperado: 2.178.827 celdas y 8.192 buckets en `bucket_plan.csv`.

**Paso 5. Smoke test (2 buckets, no entregable).**
```bash
uv run python -m experiments.timesfm.real --buckets 0,1 \
  --out-dir /home/cvelasquez/tdew_timesfm/preds_real_smoke ...
```
- Va a un directorio aparte para no mezclar. Comprobar: celdas escritas = celdas pedidas, sin NaN ni infinitos, columnas y dtypes, tamaño real por fila (compresión), celdas/s, tiempo por bucket.
- Fijar `cells_per_batch` y confirmar la estimación de 5,6 días.
- Relanzar el mismo comando y comprobar que salta ambos buckets (reanudación).
- Interrumpir un tercer bucket a mitad (Ctrl-C) y comprobar que no queda `.done` ni `pred.parquet` parcial.
- Comparación rápida contra Palacios (`real_compare.py --buckets 0,1`): la media de la diferencia debe ser coherente con el orden de magnitud del benchmark (centrada cerca de cero, RMSE del orden de 1 °C). Si difiere mucho, se revisa antes de lanzar la corrida larga.
- Se borra `preds_real_smoke/` al terminar si no se necesita.

**Paso 6. Corrida completa en `tmux`.** Crear `/home/cvelasquez/tdew_timesfm/run_real.sh`, que contiene el comando de `real.py` con `tee` a `logs_real.log`. Lanzarlo así:
```bash
tmux new-session -d -s timesfm_real '/home/cvelasquez/tdew_timesfm/run_real.sh'
```
Reanudar tras una interrupción es relanzar la misma orden. El watcher (sección 13) se activa de inmediato.

**Paso 7. Verificación del producto.** Al terminar:
```bash
uv run python -m experiments.timesfm.real --verify-only \
  --out-dir /home/cvelasquez/tdew_timesfm/preds_real --palacios-root $RES/tuning/predictions_2017_2020
```
Produce `verify_real.csv` y el `MANIFEST.csv` final. Debe cumplir los criterios de la sección 10.

**Paso 8. Análisis de acuerdo.** Escribir `experiments/timesfm/real_compare.py` y correrlo (sección 9). Sale en `reports/timesfm_benchmark/real_limpio/`.

**Paso 9. Figuras.** Serie nacional diaria de ambos productos, serie de la diferencia, y mapa de la diferencia media por celda (siguiendo el patrón de `fig-timeseries` y `fig-map` de `make_paper_figs.py`, leído sin modificarlo). Salen en `reports/timesfm_benchmark/real_limpio/figs/` con sufijo `_limpio`.

**Paso 10. Addendum, README, TRACEABILITY y limitaciones** (sección 12).

**Paso 11. Registrar y cerrar.** Registros de proveniencia, `bd` y reporte de tareas (Notion según `CLAUDE.md`).

## 8. Artefactos de salida y rutas

| Artefacto | Ruta |
|---|---|
| Producto (8.192 buckets) | `/home/cvelasquez/tdew_timesfm/preds_real/id_bucket=XXXX/pred.parquet` |
| Sentinelas por bucket | `/home/cvelasquez/tdew_timesfm/preds_real/id_bucket=XXXX/.done` |
| Lista de celdas y plan de buckets | `preds_real/ids_real_2178827.csv`, `preds_real/bucket_plan.csv` |
| Manifiesto de buckets (contrato con PLAN_4) | `preds_real/MANIFEST.csv` |
| Verificación de integridad | `preds_real/verify_real.csv` |
| Log de la corrida | `/home/cvelasquez/tdew_timesfm/logs_real.log` |
| Acuerdo TimesFM−Palacios (CSV) | `reports/timesfm_benchmark/real_limpio/agreement_*.csv` |
| Figuras | `reports/timesfm_benchmark/real_limpio/figs/*_limpio.png` |
| Resumen de la corrida | `reports/timesfm_benchmark/real_limpio/run_summary_limpio.csv` |
| Addendum de manifiesto | `docs/protocol/timesfm_manifest_addendum_real_2017_2020.yaml` |
| Tests | `tests/test_timesfm_real.py`, `tests/test_timesfm_real_provenance.py` |

El producto de 146–168 GB queda fuera de git. En el repositorio solo entran los CSV pequeños, las figuras, el código y el addendum.

## 9. Análisis de acuerdo TimesFM−Palacios (sin verdad observada)

`real_compare.py` procesa bucket por bucket: lee TimesFM y Palacios, une por `(ID, day)` (Palacios: `day = FECHA − 2017-01-01`) y acumula en flujo, en el patrón de `escala.py` con `MetricsAccum`. No carga el producto entero en memoria (3,18e9 filas). Todas las diferencias son TimesFM − Palacios.

- **Cifras de producto**, por separado para cada producto:
  - Número de valores, celdas y NaN.
  - Media nacional.
  - Medias anuales 2017–2020.
  - Mínimo y máximo (rango).
- **Control de reproducción** de las cifras de Palacios: 3.183.266.247 valores; media 19,39 °C; medias anuales 19,36 / 19,30 / 19,41 / 19,51 °C; rango −13,29 a 41,16 °C. Si no coinciden, se informa y se investiga antes de interpretar el resto.
- **Acuerdo global y por corte**: sesgo medio, RMSE, MAE y r entre ambos productos, para el total y por año, mes, zona SENAMHI (`zone_table.parquet`), tier de soporte (`support_distance.parquet`) y departamento.
- **Deriva por día de horizonte**: sesgo y RMSE de la diferencia en cada uno de los 1.461 días. Pendiente de la diferencia nacional diaria frente al día de horizonte (regresión lineal con intervalo) y diferencia entre la media del primer y del último año. Es la prueba de «sin deriva bajo autorregresión sostenida».
- **Deriva de cada producto por separado**: serie nacional diaria de la anomalía respecto de la climatología 1981–2016; tendencia de cada una.
- **Mapa de acuerdo**: sesgo medio y RMSE por celda (2,18 M filas pequeñas), con su figura.
- **Coherencia con Tmin (insumo de E12, solo descriptivo)**: media de `Td − Tmin` de cada producto y fracción de valores con `Td > Tmin`. El análisis de la cota Td ≤ Tmin + k es del PLAN_4.
- **QC**: replica los chequeos de `qc_fill.py` (conteo de filas, NaN, infinitos, rango, media) leyéndolo sin modificarlo.
- **Lo que no se hace**: no se calculan «errores» ni skill contra observaciones 2017–2020, que no existen. No se interpreta el sesgo como sesgo del método.

## 10. Criterios de aceptación

1. Los 8.192 buckets tienen `.done` y `pred.parquet`, y `MANIFEST.csv` lista 8.192 filas.
2. Total de celdas escritas = 2.178.827 y total de filas = 3.183.266.247. Si hay celdas omitidas, el `.done` las lista con su motivo, y el informe las explica. El objetivo es cero.
3. Esquema exacto: `ID` int32, `day` int16 (0 a 1460, 1.461 valores por celda), `pred` y `q10…q90` float32. Sin NaN ni infinitos.
4. Cuantiles monótonos (`q10 ≤ … ≤ q90`) en el 100 % de las filas, o una fracción de violaciones documentada y explicada.
5. Mismos IDs que Palacios, uno a uno (diferencia simétrica vacía).
6. Control de reproducción de las cifras de Palacios dentro de la tolerancia de redondeo del paper.
7. Cifras de TimesFM reportadas con la misma estructura (media nacional, medias anuales, rango).
8. Pendiente de deriva reportada con intervalo y sin tendencia significativa, o documentada si la hay.
9. Disco libre en `/` ≥ 60 GB al terminar.
10. Smoke test pasado antes de lanzar la corrida larga; reanudación probada.
11. Tests nuevos en verde y suite existente sin regresiones.

## 11. Tests y proveniencia

`tests/test_timesfm_real.py` (sin GPU; el modelo se sustituye por una función de predicción falsa):

- `SplitSpec("real")`: `context_length` = 13.149, `horizon` = 1.461, fechas límite.
- `build_panel` con raíces sintéticas en `tmp_path` para `historical_root` y `future_root`: el hold-out sale de `future_root`, `td_hold` es NaN, y el ancho de la covariable es 14.610. Una celda con `TMIN` futura incompleta se omite y queda registrada.
- Los splits `ll1/ll2/ll4` siguen leyendo el hold-out de `bucketed_training_data` (regresión).
- Conversión `day` ↔ `FECHA` (ida y vuelta, año bisiesto 2020 con `doy` 366).
- Esquema y dtypes de la salida, orden de filas y monotonía de cuantiles.
- Reanudación: salta buckets con `.done`; rehace los que tienen `.tmp` huérfano; se niega a continuar si el `ids_hash` no coincide.
- Umbral de disco: con `--min-free-gb` mayor que lo libre, termina con código no cero y sin dejar archivos parciales.
- Escritura atómica: un fallo a mitad no deja `pred.parquet` ni `.done`.

`tests/test_timesfm_real_provenance.py` (patrón de `test_timesfm_evaluate_provenance.py`):

- El registro incluye `split_id` `real_2017_2020`, `panel_id` `real_2178827_td`, `panel_cell_count` 2.178.827, `test_period` (2017-01-01, 2020-12-31), `trained=False`, `autoregressive=True`, `manifest_ref` al addendum nuevo, variante `tmin_anom_full` y el directorio de salida.
- `notes` registra: sin verdad observada, uso no comercial de los pesos (licencia), TF32 activado, `make_positive=False`, versión de `timesfm` y raíz de Tmin futura.

Proveniencia: un registro `MetricProvenance` por corrida completa (no por bucket), escrito al final con `tdew_estimation.provenance` en `reports/metric_provenance.jsonl` (solo adición). Cada `.done` guarda su propio resumen por bucket. El CSV de acuerdo lleva su `.provenance.json` al lado, como el resto del benchmark.

`docs/protocol/timesfm_manifest_addendum_real_2017_2020.yaml` (archivo nuevo, no modifica los existentes):
- Define el split `real` (contexto 1981–2016, horizonte 2017–2020, una sola pasada).
- Define el panel (2.178.827 celdas del producto de Palacios).
- Declara que no hay verdad observada y que las métricas son de acuerdo entre productos.
- Registra la restricción de licencia no comercial.
- Referencia el manifiesto original y el addendum de PLAN_1.

## 12. Documentación

- `reports/timesfm_benchmark/README.md`: sección nueva «Producto 2017–2020» con las cifras de E9 (TimesFM y Palacios), la tabla de acuerdo y la nota de licencia. Las cifras de ambos productos se reportan con la misma estructura.
- `reports/timesfm_benchmark/TRACEABILITY.md`: filas para el producto, el manifiesto de buckets, `real.py` y `real_compare.py`.
- `reports/timesfm_benchmark/limitaciones.md`: añadir (a) ausencia de verdad observada en 2017–2020, (b) licencia no comercial: el producto no es un despliegue operativo, (c) coste de 5,6 días de GPU frente a 20 minutos del método de Palacios (`b3_fill.log`).
- `experiments/timesfm/README.md`: describir el split `real`, el formato de salida y cómo reanudar.
- Para PLAN_4, una sección «Contrato de lectura» que describe `preds_real/`: columnas, tipos, deciles, reconstrucción de `FECHA` y uso de `MANIFEST.csv`.

## 13. Plan de vigilancia (watcher)

Protocolo de la memoria `background-training-watcher-protocol`: no basta con lanzar y esperar.

**Antes de pasar a la vigilancia pasiva** (justo después del lanzamiento):
1. Revisar el árbol de procesos: sin zombis ni procesos en estado D, y los hilos de lectura anticipada siguen siendo hijos del proceso vivo.
2. Confirmar la GPU activa (`nvidia-smi`, utilización alta) y que el bucket 0 produjo su `.done`.
3. Revisar MLflow (`mlflow.db`) por runs en `RUNNING` cuyo proceso ya murió y marcarlos como terminados. Esta corrida no abre MLflow; la revisión es por si quedó algo de corridas anteriores.
4. Anotar la tasa inicial de celdas/s (esperada ≈ 4,5–5,1) y el espacio libre inicial.

**Cadencia escalonada.** Primera revisión a la hora. Si todo está sano (proceso vivo, GPU activa, sin errores nuevos en el log, sin zombis), la siguiente se espacia a 5 horas. Si también está sana, se espacia a 8–12 horas (≈ 10–14 revisiones en total para ~134 h).

**Vigilancia continua** (en paralelo, ciclo corto, p. ej. cada 10 min): busca en `logs_real.log` `Traceback`, `OOM`/`out of memory`, `Killed` y salida inesperada de la sesión `tmux`. También comprueba:
- Que aparezcan `.done` nuevos (sin avance en 15 min se trata como cuelgue).
- Que la tasa no caiga por debajo de 3,5 celdas/s sostenida durante 30 min (sospecha de recorte térmico).
- Que el espacio libre en `/` supere 100 GB (aviso) y 60 GB (el script se detiene solo).

**Respuesta ante fallos.** Revisar la causa en el log, resolverla y relanzar el mismo comando. Los buckets completos se saltan. Si el fallo es de datos de un bucket concreto, se registra, se aísla y se informa al usuario.

## 14. Riesgos

- **Duración y fallos.** ~5,6 días de GPU continua. Mitigación: sentinela por bucket, escritura atómica y reanudación; watcher escalonado. Un corte de luz o reinicio cuesta como máximo un bucket (≈ 1 min).
- **Disco.** El producto ocupa ~146–168 GB, que dejan `/` en 81–83 %. Umbral de parada a 60 GB libres y aviso a 100 GB; protocolo de la sección 6.4 si se cruza. Nada se escribe bajo `$RES`. Mover a `Data1` requiere autorización de Palacios.
- **Compresión menor a la esperada.** Los float32 se comprimen poco. Se mide en el smoke test y se ajusta la estimación antes de lanzar.
- **Rendimiento.** La estimación (5,6 días) extrapola 5,09 celdas/s al contexto más largo. El recorte por potencia (70 W) y la temperatura (83 °C sostenidos) pueden bajar la tasa. Otros procesos en la GPU (2 GB ocupados) o la contención de disco al leer 36 archivos por bucket también influyen. La lectura anticipada reduce el último riesgo.
- **Celdas omitidas.** Si alguna celda con Td no tiene contexto o Tmin futura completos, se omite. Se registra y se informa. Hay que reportar cuántas y por qué antes de declarar paridad 1:1.
- **Sin verdad observada.** Cualquier lectura de «mejor» o «peor» entre productos sería injustificada. Las tablas solo muestran acuerdo.
- **Licencia no comercial.** Los pesos de TimesFM 3.0 prohíben uso comercial o productivo. El producto es solo de investigación, y así se declara en el addendum, el README y la proveniencia. No hay despliegue operativo.
- **Divergencia de la estimación de Palacios.** Si el control de reproducción de las cifras de Palacios falla, el problema está en la lectura o en un cambio posterior de su producto. Se investiga antes de interpretar.
- **Regresión en `panel.py`.** Mitigado con tests existentes y de regresión sobre `ll*`.
- **GPU compartida.** Si otro usuario lanza trabajo en la GPU durante la corrida, la tasa baja o hay OOM. El watcher lo detecta y `predict_panel` reintenta con lote menor.

## 15. Qué no entra

- E10 (costura 2016/2017), E11 (cola cálida > 35 °C) y E12 (cota Td ≤ Tmin + k): son del PLAN_4. Este plan solo guarda lo que necesitan.
- Cualquier cálculo de error, skill o RMSE frente a observaciones 2017–2020.
- Otras variantes de TimesFM, fine-tuning o reentrenamiento.
- Reducción de coste (más hardware, clúster), submuestreo o formatos con pérdida.
- Despliegue operativo o uso comercial.
- Re-correr o modificar el producto de Palacios, o escribir bajo `$RES`.
- Modificar `reports/paper/scripts/` o archivos con fuga.

### Archivos críticos para la implementación
- `experiments/timesfm/panel.py`
- `experiments/timesfm/run.py`
- `experiments/timesfm/real.py` (nuevo)
- `experiments/timesfm/real_compare.py` (nuevo)
- `tests/test_timesfm_real.py` (nuevo)
