# Costo comparable de TimesFM, `tuned` y los LLR propios

Bead `tdew-03g`. Datos en `costo.csv`. Todas las cifras salen de logs y archivos de
tiempos de corridas reales; no se estimó ninguna salvo donde se indica. Estación de
trabajo: Intel Core i9-14900K (32 hilos), 125 GB de RAM, NVIDIA RTX A2000 12 GB
limitada a 70 W (`reports/timesfm_benchmark/limitaciones.md` §8).

## Bloque `ll4b` (prueba 2009-2012), misma máquina

| método | etapa | celdas | tiempo de pared | GPU |
|---|---|---|---|---|
| TimesFM `tmin_anom_full` | predicción (sin ajuste ni selección) | 17.041 | 73 min 10 s (3,88 celdas/s) | sí |
| TimesFM `tmin_td_full` | predicción | 17.041 | 73 min 1 s (3,89 celdas/s) | sí |
| `tuned` | selección de recetas con años de entrenamiento | 5.506 (16 buckets) | 52 min 38 s | sí (CuPy) |
| `tuned` | ajuste + predicción | 17.027 (64 buckets) | 5 min 50 s | sí (CuPy) |
| LLR simple | carga + selección de `h` + ajuste y predicción | 17.027 | 2 min 8 s (17 s + 1 min 32 s + 19 s) | no |
| LLR con rezagos de Tmin | carga + selección de `h` + ajuste y predicción | 17.027 | 8 min 28 s (14 s + 6 min 43 s + 1 min 31 s) | no |

TimesFM y `tuned` corrieron uno detrás del otro (TimesFM terminó a las 14:05:02 y
`tuned` empezó a las 14:05:04 del 20 de octubre), de modo que no compartieron la GPU.
Durante la selección de `tuned`, entre 14:24 y 14:41, corrió en CPU el LLR con rezagos
de `ll4`. Los tiempos del LLR se midieron con `/usr/bin/time` en una re-corrida de
`ll4b` el mismo día (`costo_llr_ll4b_time.log`), que reprodujo los RMSE originales
(1,0984 y 1,0891); en paralelo, otro agente ejecutaba la selección de `tuned` sin
rezagos de Td, con carga media de unos 3 núcleos. El LLR usó en promedio 1,2 y 1,0
núcleos: está limitado por un solo hilo, no por los 32 disponibles. En el LLR el
ajuste final y la predicción ocurren en la misma pasada y no se separan.

TimesFM predice 14 celdas más que las 17.027 que se puntúan (panel de 17.041). El
comando de la corrida `ll4b` no quedó registrado; TF32 está activo por defecto en
`experiments/timesfm/run.py`. Su ritmo, 3,9 celdas/s con 10.227 días de contexto, es
menor que los 5,09 celdas/s de la pasada de escala con TF32; no se determinó la causa.

## Otras corridas de referencia

| método | corrida | etapa | celdas | tiempo |
|---|---|---|---|---|
| TimesFM | `ll4` | predicción | 17.041 | 85 min 55 s (3,31 celdas/s; no consta TF32) |
| TimesFM | `ll4`, cribado | selección entre 9 variantes | 1.106 × 9 | 49 min 8 s (suma de las 9) |
| TimesFM | escala `ll4` | predicción | 436.519 | 23 h 48 min (5,09 celdas/s, TF32) |
| TimesFM | producto 2017-2020 | predicción | 2.178.827 | 438.074 s ≈ 5,1 días (4,97 celdas/s) |
| `tuned` | `ll4` limpio (Palacios, 14-09-2026) | selección + ajuste y predicción | 5.506 / 17.027 | 53 min 14 s + 6 min 42 s |
| `tuned` | producción 1981-2016 | selección de recetas | 2.818.404 | 32 h 41 min |
| `tuned` | producción 1981-2016 | ajuste | 2.818.404 | 6 h 45 min |
| `tuned` | producto 2017-2020 | predicción, 14 procesos | 2.178.827 | 19 min 40 s |

Las corridas de Palacios (`$RES/tuning/*.log`) no registran el host. Se lanzaron
desde `/home/ppalacios`, que existe en esta estación, y `b0_run.sh` declara «local
single-GPU», pero no queda probado que usaran la misma tarjeta.

## Lectura

En `ll4b`, con las etapas que cada método necesita para producir un pronóstico sin
ver el bloque oculto, TimesFM tardó unos 73 min por variante en GPU, `tuned` 58 min
en GPU y los LLR 2 y 8 min en un núcleo de CPU. La comparación justa para TimesFM
debe sumar además la selección de variante (49 min sobre 1.106 celdas en `ll4`), que
se hizo una sola vez y sobre el bloque de evaluación. A escala de producto, la
predicción de TimesFM (≈5,1 días) es unas 370 veces más lenta que la de `tuned` (20
min), pero `tuned` necesita antes 39 h de selección y ajuste que TimesFM no tiene.

## Insumos de diseño que requiere cada método

Columna cualitativa basada en el código; no se estiman horas-persona.

| método | insumos y decisiones previas |
|---|---|
| climatología | media por celda y día del año en los años de entrenamiento |
| LLR simple (`experiments/llr_simple/llr.py`) | climatología de Td y Tmin por celda; núcleo tricúbico circular en el día del año; un único `h` global elegido en una grilla de 7 valores (7-60) con los últimos 4 años de entrenamiento; sin zonas ni rezagos |
| LLR con rezagos (`llr_lags.py`) | lo mismo más rezagos fijos de la anomalía de Tmin (1, 2, 7 y 30 días) y una cresta de 1e-6 |
| `tuned` (`HPC_code_tunning/`) | shapefile de zonas climáticas SENAMHI (`clasif_clima_peru.zip` → `zone_table.parquet`, 41 zonas); pool de 11 términos candidatos (constante, Tmin del día, rezagos de Tmin 1, 2, 7 y 30, rezagos de Td 1, 2, 3, 7 y 30); búsqueda de receta y `h` (grilla 7-45) por zona × día del año con muestreo de celdas por zona; pronóstico autorregresivo con sus propios rezagos de Td; implementación en GPU con CuPy |
| TimesFM 3.0 (`experiments/timesfm/`) | checkpoint preentrenado `google/timesfm-3.0-pytorch` (330M parámetros, licencia no comercial); climatología para construir la anomalía; Tmin futura como covariable; elección entre 9 configuraciones de entrada, objetivo y contexto; GPU en la práctica (TF32, lote 16-32) |
