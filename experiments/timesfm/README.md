# experiments/timesfm

Esta carpeta contiene el código que ejecuta el benchmark de TimesFM 3.0
(Google, 330M de parámetros) en modo zero-shot para reconstruir la
temperatura de rocío diaria (Td), y lo compara contra el método `tuned` de
Palacios y contra la TCN del proyecto. No se entrena ningún modelo aquí: la
inferencia usa el checkpoint público `google/timesfm-3.0-pytorch`. Los
resultados (CSV, figuras y la página HTML interactiva) se publican en
`reports/timesfm_benchmark/`, y el protocolo del experimento está en
`docs/protocol/timesfm_manifest.yaml`.

El benchmark opera en cuatro niveles de medición: cribado (1106 celdas,
compara las 9 variantes entre sí), backtest nacional (17 027 celdas del
run limpio de Palacios, comparación pareada contra la cifra publicada en el paper),
departamental (2048 celdas, el único nivel en el que se compara también
contra la TCN) y escala (436 519 celdas, para medir coste y estabilidad al
volumen real de datos).

## Archivos

- `variants.py`: define las 9 variantes de TimesFM evaluadas, como
  dataclasses `Variant` (objetivo Td o anomalía, covariables usadas, año de
  inicio del contexto, banderas de autorregresión, promediado simétrico y
  normalización z). No tiene interfaz de línea de comandos.
- `panel.py`: construye los paneles de contexto y horizonte a partir de
  `$RES/bucketed_training_data/...`, con la misma fuente que
  `HPC_code_tunning/backtest.py`, cuidando que ningún dato del bloque oculto
  entre al contexto salvo Tmin como exógena. Define los splits `ll1`, `ll2` y
  `ll4` (`SPLITS`, `SplitSpec`, `PanelBatch`, `iter_panel_batches`).
- `run.py`: script principal de inferencia. Corre cada variante de TimesFM en
  modo zero-shot sobre un panel y escribe un parquet en formato largo
  `(ID, FECHA)` con la mediana y los 9 deciles de la predicción, junto con su
  registro de proveniencia.
- `probabilistic.py`: funciones para calcular métricas probabilísticas sobre
  los 9 deciles predichos (pinball loss, aproximación de CRPS, cobertura de
  intervalo). No tiene interfaz de línea de comandos.
- `by_tier_month.py`: desempeño por tier de soporte observacional (E5) y sesgo
  mensual (E8) de TimesFM y los rivales de Palacios, solo cómputo sobre las
  predicciones existentes. Escribe los CSV `*_limpio` de `nacional_limpio/` y
  `cribado_limpio/`, con control de reproducción contra el paper y `--mlflow`
  opcional; `artifact_data.py` los incorpora a la página interactiva.
- `evaluate.py`: puntúa las variantes de TimesFM junto con los métodos de
  Palacios (climatología, `td_eq_tmin`, `zone_ols`, `tuned`), leyendo
  `predictions.parquet` del backtest y restringiendo la comparación a las
  celdas donde TimesFM también produjo predicción. Genera los
  `leaderboard.csv`. La raíz de referencia por defecto es el run limpio
  (`CLEAN_BACKTEST_ROOT`, `$RES/tuning/backtest_clean`); el run con fuga
  (`LEAKY_BACKTEST_ROOT`) solo se usa pasando `--backtest-root`. Con
  `--growth-curve` escribe además la curva de RMSE acumulado. Omite las variantes
  retiradas del protocolo (`RETIRED_VARIANTS`).
- `publish.py`: copia un CSV intermedio al repositorio y clona sus filas de
  `reports/metric_provenance.jsonl` apuntando al destino (idempotente).
- `merge_predictions.py`: copia `predictions.parquet` del backtest (por defecto
  el run limpio, la misma constante que `evaluate.py`) agregando
  la columna `pred_timesfm`, sin modificar el original, para que
  `HPC_code_tunning/effect_sizes.py` la use a través de `METHOD_COLS`.
- `departamental.py`: convierte las predicciones de TimesFM y de Palacios al
  formato largo canónico del pipeline de reconstrucción
  (`experiments/reconstruction/cli.py`) para compararlas con la TCN en el
  panel departamental.
- `escala.py`: puntúa la prueba de escala (436 519 celdas por 1461 días, unas
  638 millones de filas) de forma incremental, sin cargar todo en memoria,
  agregando por sitio y con reponderación comparable a
  `reports/week1_baselines/leaderboard.csv`.
- `throughput.py`: mide el coste de la inferencia (celdas por segundo, VRAM
  pico) variando longitud de contexto, horizonte y tamaño de lote. Escribe
  `coste_throughput.csv`.
- `plots.py`: funciones de graficación compartidas (paleta Okabe-Ito, salida
  en PNG estático porque la estación de trabajo se usa por SSH sin
  navegador): curvas de error, comparación entre variantes, calibración y
  coste.
- `make_figures.py`: genera todas las figuras del reporte para las que ya
  existan los datos de entrada, y omite en silencio las que aún no se pueden
  producir. Usa las funciones de `plots.py`.
- `artifact_data.py`: construye el JSON embebido en la página HTML
  interactiva de `reports/timesfm_benchmark/artifact/`, incluyendo el mapa
  nacional comprimido con zlib. No recalcula métricas: las toma de los CSV ya
  publicados.

- `departamental_pareado.py`: prueba pareada por celda de TimesFM contra cada rival
  del panel departamental (las tres semillas de la TCN, `tuned` y la climatología),
  con las funciones de `HPC_code_tunning/effect_sizes.py`. Escribe
  `departamental/pareado.csv`.
- `paths.py`: raíces de datos. `TDEW_RES`, `TDEW_TIMESFM_WORK` y
  `TDEW_RECONSTRUCTION_WORK` las sobrescriben; los valores por defecto son las rutas de
  la estación de trabajo donde se corrió el benchmark.
- `scripts/`: un script por etapa (`00_panels.sh` a `07_reporte.sh`, con `env.sh`
  común) con las órdenes que se ejecutaron, y `make_panels.py`, que reconstruye los
  seis paneles de celdas desde sus fuentes y comprueba que son idénticos a los usados.
  Los pasos completos de reproducción están en la sección «Reproducibility» del
  `README.md` de la raíz.

## Orden de ejecución

`variants.py` y `panel.py` fijan la configuración y los datos de entrada.
`run.py` corre la inferencia y produce el parquet de predicciones.
`merge_predictions.py`, `departamental.py` y `escala.py` adaptan esas
predicciones a cada nivel de comparación. `evaluate.py` calcula las métricas
y los leaderboards. `make_figures.py` y `plots.py` generan las figuras, y
`artifact_data.py` arma la página interactiva final a partir de los CSV ya
publicados.

## Producto 2017-2020 (split `real`, E9)

`panel.py` define el split `real`: contexto 1981-2016 (13.149 días) y horizonte
2017-01-01 a 2020-12-31 (1.461 días). La Tmin futura sale de
`future_tmin_by_bucket` (argumento `future_root`), `td_hold` queda en NaN porque
no hay Td observada, y una celda se omite si le falta contexto o Tmin futura.
Los splits `ll1/ll2/ll4` no cambian.

- `real.py`: corrida por buckets (`ID % 8192`) de la variante `tmin_anom_full`
  sobre las 2.178.827 celdas del producto de Palacios. Cada bucket se escribe de
  forma atómica (`pred.parquet.tmp` → `pred.parquet`) y termina con `.done`
  (JSON con filas, bytes, sha256, celdas omitidas, `ids_hash`, `code_version`).
  Reanudar es relanzar el mismo comando; un `.done` con otro `ids_hash` o
  `code_version` aborta con `ResumeMismatch`. `--plan-only` lista celdas,
  `--verify-only` revisa el producto y regenera `MANIFEST.csv`. Con `--mlflow`
  registra una corrida en `tdew-timesfm-benchmark`. Cada corrida deja un registro
  en `reports/metric_provenance.jsonl`. Un lote por bucket (≤ 271 celdas), sin
  `--cells-per-batch`.
- `real_compare.py`: acuerdo TimesFM − Palacios, en flujo por bucket. Sin verdad
  observada: sesgo, RMSE, MAE y r **entre productos**, nunca «error». Salidas
  `*_limpio.csv` con su `.provenance.json`.

Formato de salida (`preds_real/id_bucket=XXXX/pred.parquet`): `ID` int32, `day`
int16 (días desde 2017-01-01, 0 a 1460), `pred` y `q10`…`q90` float32, zstd,
ordenado por `(ID, day)`. `FECHA = 2017-01-01 + day`. Leer con
`pq.ParquetFile(ruta).read()`: `pq.read_table(ruta)` infiere la partición hive
del directorio y agrega una columna `id_bucket` que no está en el archivo.

Medido en el smoke test (buckets 0 y 1, RTX A2000): 4,3 celdas/s con
`--batch-size 32` (3,4 con 4 y 4,1 con 16; la salida es idéntica bit a bit), pico
de 7,4 GB de VRAM y 49,6 B por fila con zstd (los float32 casi no comprimen).
Extrapolado: ≈ 5,9 días y ≈ 158 GB para el producto completo.
