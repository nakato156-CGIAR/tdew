# experiments/tcn

Esta carpeta contiene la implementación y el entrenamiento de `TCNAttentionModel`
(bead `tdew-x46`), una red TCN con atención que predice la anomalía de
temperatura de rocío del día siguiente, `Td(t+1)`. La entrada combina ventanas
de 14, 31 o 60 días de variables dinámicas (Tmin, Tmax, Td histórico, día del
año), covariables estáticas del sitio (DEM, TDI, coordenadas X/Y) y
condicionantes del día objetivo (LST diurno y nocturno, día del año). El
entrenamiento usa datos de los cuatro sitios del proyecto en conjunto (Lima
como costa, Cusco como sierra, Loreto y San Martín como selva), se ejecuta a
través de ZenML y registra métricas en MLflow.

## Archivos principales

- `train.py`: bucle de entrenamiento y validación. Usa AdamW, pérdida Huber
  ponderada por sitio y autocast en bf16; guarda checkpoints por época además
  de `best.pt`/`last.pt`, calcula RMSE, MAE, bias y skill contra climatología,
  y registra la proveniencia de cada corrida.
- `dataset.py`: define `TdewWindowDataset`, un `IterableDataset` que genera
  ventanas sobre la marcha desde `Data/gold/model_features_norm` usando
  `sequence_index` para determinar qué ventanas son elegibles. Distribuye los
  sitios en round-robin dentro de cada bucket para que ningún batch quede
  dominado por un solo sitio (en particular Loreto o San Martín frente a Lima
  o Cusco), y aplica un buffer de shuffle en el split de entrenamiento.
- `checkpoint.py`: guarda, carga y reanuda checkpoints, incluyendo el estado
  del optimizador, el scheduler y el generador de números aleatorios, para que
  una corrida reanudada sea reproducible bit a bit.
- `site_weights.py`: calcula el peso de cada sitio como `1 / n_filas_train`,
  el mismo criterio usado en `generalist_mlr`. Los pesos se fijan una vez con
  longitud de contexto L=31 y se reutilizan para L=14 y L=60. Escribe
  `site_weights.json`.
- `ablation_x46_1.py`: ablación correctiva (bead `tdew-x46.1`) que compara
  cuatro variantes del modelo (residual de persistencia, FiLM inicializado
  como identidad, ciclo por pasos fijo, pesos por sitio uniformes) bajo el
  mismo presupuesto de pasos. Escribe resultados en
  `reports/week1_tcn_ablation/`.
- `zenml_pipeline.py`: envuelve `train.run()` en un `@step`/`@pipeline` de
  ZenML, siguiendo la convención del proyecto de ejecutar el entrenamiento a
  través de ZenML en lugar de invocar el script directamente.

## `checkpoints/`

Una subcarpeta por combinación de run, longitud de contexto y semilla, por
ejemplo `week1-tcn-attention_L31_seed0/`, con los archivos
`epoch_0000.pt` … `epoch_0004.pt`, `best.pt` y `last.pt`. Al momento de
escribir este README solo hay 5 épocas entrenadas de las 30 planeadas para
esa corrida.

## `site_weights.json`

Peso por sitio derivado de `site_weights.py`: guarda la longitud de contexto
de referencia (31), el conteo `train_n_eligible_targets` de cada sitio y el
peso resultante `1 / n`. Loreto, al ser el sitio con más filas elegibles,
recibe el peso más bajo.

## `audit_x46/`

Auditoría del run entrenado `week1-tcn-attention_L31_seed0`, orientada a
explicar por qué el modelo memoriza en vez de generalizar, en particular en
Loreto. `common.py` reúne utilidades compartidas por los scripts: muestreo
reproducible de ventanas reales, carga del modelo entrenado y cálculo de
métricas. Los scripts están numerados en el orden en que se fueron
ejecutando durante la investigación:

- `01_mlflow_dump.py`: vuelca en texto plano los parámetros, métricas y tags
  de todos los runs registrados en `mlflow.db`.
- `02_checkpoints.py`: inspecciona los checkpoints reales (época, paso
  global, mejor skill de validación, estadísticas de los pesos, escala de
  gamma/beta de las capas FiLM).
- `03_build_sample.py`: construye y guarda en caché submuestras fijas de
  datos (`sample_validation.npz`, `sample_train.npz`,
  `sample_train_big.npz`) que reutilizan el resto de los scripts.
- `04_compare_predictors.py`: compara el modelo entrenado contra
  climatología, persistencia, medias móviles y una regresión OLS sobre las
  mismas entradas.
- `05_batches.py`: mide la composición real de los batches que produce el
  `DataLoader` — la fracción de gradiente que aporta cada sitio, el tamaño de
  muestra efectivo y la presencia de NaN — a lo largo de un bucket completo.
- `06_sensitivity.py`: mide la sensibilidad de la predicción a cada bloque o
  canal de entrada mediante ablaciones a cero, y a los componentes internos
  de FiLM y atención.
- `07_loss_vs_metric.py`: compara la función objetivo que se optimiza
  (Huber ponderada) contra la métrica de evaluación (RMSE agrupado).
- `08_probes.py`: entrena sondas lineales sobre las representaciones
  internas del modelo (entrada cruda, salida de la TCN, vector agregado,
  salida de FiLM) para ubicar en qué capa se pierde información relevante.
- `09_economy.py`: estima la economía de cómputo del entrenamiento — pasos
  por época, tiempo por época, muestras por parámetro — a partir de los
  checkpoints y de MLflow.
- `10_ablation.py`: réplica en CPU, a escala reducida, de cinco variantes
  arquitectónicas o de ponderación bajo condiciones idénticas (mismos
  batches, misma semilla, mismo número de pasos).
- `11_data_checks.py`: verifica fuga temporal, simetría en la comparación
  con los baselines, y rangos o NaN en los tensores de entrada.
- `12_loss_numerics.py`: investiga por qué el `train_loss` registrado en
  MLflow no coincide con la pérdida recalculada, y el efecto de usar bf16 en
  vez de float32.
- `13_train_val_gap.py`: compara el RMSE del modelo, de la persistencia y de
  la climatología entre train, validation y test sobre las mismas celdas,
  para cuantificar la brecha de generalización.
- `14_overfit_mechanism.py`: evalúa si el condicionante del día objetivo
  (LST) filtra información del propio objetivo, o si la relación observada
  es lineal y reproducible con una regresión OLS.
- `15_loreto_zoom.py`: inspecciona series y errores por celda en Loreto
  (autocorrelación, ventanas duplicadas, error por rango de valores).
- `16_loreto_structure.py`: mide la redundancia espacial entre celdas de
  Loreto y el RMSE año por año.
- `17_memorization_test.py`: agrega ruido gaussiano creciente a la ventana
  de entrada para probar si el modelo memoriza en vez de generalizar.
- `18_effective_n.py`: estima el número efectivo de observaciones
  independientes por sitio a partir del espectro de correlación espacial
  (participation ratio).
- `19_gradient_share.py`: mide la fracción real del gradiente de una época
  que recibe cada sitio, dado el orden real de emisión round-robin.
- `20_ablation_gpu.py`: versión ampliada en GPU de `10_ablation.py`, con
  2.55 millones de ventanas y 20 000 pasos.
- `21_early_stop.py`: compara la frecuencia de evaluación real usada en
  producción (aproximadamente 1.7 millones de pasos por época) contra el
  punto en que el óptimo de validación aparece en el experimento controlado.

`audit_x46/out/` guarda las cachés de muestras (`sample_train.npz`,
`sample_validation.npz`, `sample_train_big.npz`, este último de
aproximadamente 1.9 GB) y los CSV de resultados de cada script de auditoría
(`ablation.csv`, `ablation_gpu.csv`, `batches.csv`, `compare_predictors.csv`,
`gradient_share.csv`, `memorization.csv`, `probes.csv`,
`sensitivity_best.pt.csv`, `sensitivity_last.pt.csv`,
`train_val_gap.csv`). Cada uno tiene su archivo de proveniencia
correspondiente en `reports/week1_tcn_audit/`.
