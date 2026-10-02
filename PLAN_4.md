# PLAN_4: comparación de TimesFM y Palacios en la costura 2016/2017, la cola cálida y la cota Td ≤ Tmin + k (E10, E11, E12)

Versión final. Fecha: 2026-10-02. Bead padre: `tdew-214` (se propone una subtarea nueva, hermana de las de PLAN_1, PLAN_2 y PLAN_3).

## Experimentos que cubre este plan

Los códigos E# son nuestros (E1–E16, numerados para esta comparación). No son los del paper de Palacios (`reports/paper/paper.qmd`).

| # | Experimento (en el paper) | Qué mide |
|---|---|---|
| E10 | Continuidad en la costura 2016/2017 (`tbl-seam`, `fig-seam` = F3, `fig-timeseries`, sec-results-seam) | Diferencia de la media anual de Td entre ventanas de cuatro años de igual longitud (se cancela la estacionalidad) sobre 2.178.827 celdas. Control observado 2013–16 − 2009–12 frente a reconstruido 2017–20 − observado 2013–16, para TimesFM y para Palacios. Serie nacional mensual observada 2010–2016 empalmada con ambos productos |
| E11 | Cola cálida Td > 35 °C (sec-results-tail, `tbl-support`, `tbl-inherited`, F4, F5) | Fracción de valores > 35 °C, máximo, celdas afectadas, exceedance por tier de soporte, concentración por mes y en la clase `A (r) A'`, rachas, lo «heredado» del producto fuente en 2013–2016 (ll4) y solapamiento de las excedencias de ambos productos. Para TimesFM, además, la fracción de cuantiles > 35 °C y la anchura q90−q10 por mes y tier |
| E12 | Cota Td ≤ Tmin + k (`tbl-bound`, sec-limitations) | Fracción de valores alterados por la cota, desplazamiento medio y parte de los valores > 35 °C que la cota retira, para k = 0, 5, 6, 8, 10, 12. Línea de referencia del observado histórico. Para TimesFM, violación por q10, q50 y q90 y un agregado por celda para mapas |

Este plan depende de PLAN_3 (producto TimesFM 2017–2020 en `/home/cvelasquez/tdew_timesfm/preds_real/`, con `MANIFEST.csv`): sin ese producto completo y verificado no se ejecuta el paso central. Es coherente con PLAN_1 (run limpio, sufijo `_limpio`, addendum de manifiesto, la referencia ll4 de 17.027 celdas) y con PLAN_2 (tiers de soporte y zonas: `support_distance.parquet` y `zone_table.parquet`, que aquí se leen y no se recalculan). Se reutilizan de PLAN_1 la constante `MANIFEST_REF_LIMPIO` y las convenciones de sufijo, y de PLAN_3 el contrato de lectura de `preds_real/`.

## 0. Decisiones tomadas

1. **Lado a lado.** Cada análisis se presenta para ambos productos. Además se calcula, en el mismo paso, una tabla de solapamiento de las excedencias > 35 °C (celdas y celda-días donde ambos productos superan el umbral).
2. **Un solo paso por bucket.** Un único recorrido de los 8.192 buckets alimenta E10, E11, E12, la serie nacional, el solapamiento y los descriptivos de deciles. No se vuelve a leer ningún producto por análisis.
3. **Origen de las cifras de Palacios.** Se usan las cifras publicadas en el paper cuando son las que se necesitan (`tbl-seam`, `tbl-support`, `tbl-inherited`, `tbl-bound`, texto de sec-results-tail). Solo se calcula lo que el paper no trae: la línea de observado histórico Td > Tmin + k, el solapamiento, todo lo de TimesFM, los cortes nuevos y los insumos de las figuras que superponen ambos productos (el paper solo publica los PNG). Cada cifra del informe lleva su origen («paper» o «calculada») en `TRACEABILITY.md`.
4. **Código de Palacios sin cambios.** Se verificó (sección 3) que ningún script de `reports/paper/scripts/` cambió desde la última revisión del paper (2026-09-18) y que sus datos son anteriores. Por eso no se vuelven a ejecutar sus scripts. Se conservan tres controles baratos: control de costura vía caché, «heredado» vía ll4 y cordura de recuentos del producto de Palacios.
5. **Scripts de Palacios solo lectura.** Se reimplementan las definiciones (ventanas, umbral 35, familia de k, tiers, bins) en código nuevo bajo `experiments/timesfm/`. No se edita nada en `reports/paper/scripts/`. De allí solo se importa `geo_overlay.add_peru_outline` para dibujar el contorno.
6. **Serie nacional completa.** El mismo paso lee `train_2010…2016` (~22 GB) y se replica `fig-timeseries` completa.
7. **Deciles.** Se reportan descriptivos (violación de la cota por q10, q50 y q90, fracción de cuantiles > 35 °C, anchura q90−q10 por mes y tier) más una comprobación de calibración en ll4 (cobertura nominal frente a empírica por tier). Son marginales por paso de horizonte, no trayectorias, y no verificables en 2017–2020. Esa salvedad va en cada tabla y figura que los use.
8. **Cota.** Se evalúa como en el paper y se guarda un agregado por celda (no el producto completo) con los recuentos de violaciones por k y por cuantil, para mapas. No se produce ni se publica un producto acotado.
9. **Definición de la cota.** La misma que la de Palacios: valor alterado si `v > Tmin_mismo_día + k`; desplazamiento `max(v − (Tmin + k), 0)`; k ∈ {0, 5, 6, 8, 10, 12} (los de `tbl-bound`; el script de Palacios añade 4 y 15, que aquí no se usan). Las comparaciones se hacen en float64 (los float32 de TimesFM y de Tmin se convierten antes de comparar) para que el redondeo no cambie los recuentos.
10. **Sufijo `_limpio` y no escribir bajo `$RES`.** Todo resultado publicado lleva sufijo `_limpio` y va a `reports/timesfm_benchmark/real_limpio/`. Los agregados grandes van a `/home/cvelasquez/tdew_timesfm/agg_real/` (fuera de git). Ningún archivo con fuga (`$RES/tuning/backtest`) se usa.
11. **Sin «error».** No hay verdad observada de Td en 2017–2020. En ningún texto se llama «error» a una diferencia entre productos ni a una violación de cota.

## 1. Objetivo

Aplicar a TimesFM 3.0 zero-shot los tres análisis de calidad del producto del paper (continuidad en la costura, cola cálida y cota física sobre Td − Tmin) y compararlos con los de Palacios, usando el producto de PLAN_3 y los datos observados 1981–2016. Con los deciles de TimesFM se añaden descriptivos de incertidumbre que el método de Palacios no tiene, con sus límites de interpretación explícitos.

## 2. Alcance

Entra en este punto:

- Código del paso único (`experiments/timesfm/real_paso.py`), del informe (`real_informe.py`), de figuras (`real_figs.py`) y de la calibración y el «heredado» en ll4 (`real_ll4.py`).
- Controles de reproducción (costura vía caché, «heredado» vía ll4, cordura de recuentos del producto de Palacios).
- Tablas CSV, figuras `_limpio` (F3, F4, F5, `fig-timeseries`, mapa de media y mapas de cota), proveniencia, addendum, tests y documentación.

No entra: ver sección 15.

## 3. Pre-condiciones verificadas

Verificadas con lecturas reales, sin escribir archivos ni bajo `$RES`.

**3.1 Hechos técnicos**

| Hecho | Evidencia |
|---|---|
| Palacios y Tmin se unen por `(ID, day)`. | `predictions_2017_2020/id_bucket=*/pred.parquet` tiene `FECHA` (ns), `ID` int64 y `TD_predicted` float64, ordenado por `(ID, FECHA)`, un solo row group. Se comprobó en los buckets 4321 y 8000 (264 y 267 celdas × 1.461 días). `day = (FECHA − 2017-01-01).days`. |
| La Tmin futura no tiene huecos en celdas con Td. | `future_tmin_by_bucket/id_bucket=XXXX/future_tmin_{2017..2020}.parquet`: 344 celdas por bucket × 1.461 días (502.584 filas). Los NaN (116.880 y 112.497 en los dos buckets) son exactamente las celdas sin Td × 1.461 días. Cero NaN en celdas con Td. |
| Cálculo por bucket barato. | Pivote de Tmin por `searchsorted`, deciles simulados (9 × 264 × 1.461) y recuentos por k: ≈ 0,3 s por bucket frente a ≈ 0,1 s de lectura con caché caliente. |
| Caché de costura reutilizable. | `$RES/tuning/seam_windows_cache.parquet`: 2.178.827 filas, `ID` int64, `w1` float32 (observado 2009–12), `w2` float32 (observado 2013–16), `w3` float64 (Palacios 2017–20). Reproduce el control: media +0,1008, sd 0,1246, p1 −0,183, p99 +0,416; y la fila de Palacios: −0,0407, sd 0,1757, p1 −0,363, p99 +0,540. |
| Tiers disponibles. | `$RES/tuning/support_distance.parquet`: 2.178.827 filas (`ID`, `lon`, `lat`, `dist_km`, `tier`). Within 1.066.118; near 228.643; marginal 179.581; extrapolated 328.136; unsupported 376.349. |
| Clase Thornthwaite. | `$RES/zone_table.parquet`: 2.818.404 IDs, `zone_id`, `zone_label` (41 etiquetas, sin nulos). La clase `A (r) A'` tiene 909.274 celdas en todos los tiers (276.029 within). |
| Observado v1.1 2013–2016 por celda. | `bucketed_training_data/id_bucket=XXXX/train_YYYY.parquet` (`ID`, `FECHA`, `TD`, `TMIN`, `doy`), 1981–2016; 112 GB. |
| Referencia ll4 existente. | `$RES/tuning/backtest_clean/ll4/predictions.parquet`: 24.876.447 filas = 17.027 celdas × 1.461 (`TD_obs`, `pred_tuned`, `Tmin_hold`, `FECHA` 2013–2016). |
| TimesFM ya cubre esas celdas con deciles. | `/home/cvelasquez/tdew_timesfm/preds_nacional/ll4__tmin_anom_full.parquet`: 24.896.901 filas (`ID`, `FECHA`, `pred`, `q10…q90` float32), 17.041 celdas, de las que 17.027 coinciden con las de Palacios. El «heredado» y la calibración de TimesFM salen de allí, sin inferir nada. |
| «Heredado» de Palacios reproducible. | Con la referencia ll4: dentro, observado máx 38,34 °C y 0,0046 % > 35, reconstruido máx 34,10 °C y 0 %; fuera, observado máx 46,47 °C (en el tier unsupported). Las dos tasas de «fuera» (0,6724 % y 0,2147 %) se comprueban en el paso 5. |
| Línea observada de la cota (nueva). | En la misma muestra ll4 (`TD_obs` frente a `Tmin_hold`), fracción con `Td > Tmin + k` para k = 0, 5, 6, 8, 10, 12: observado 78,79 / 14,57 / 9,19 / 3,33 / 0,99 / 0,23 %; Palacios 79,61 / 13,26 / 7,75 / 2,33 / 0,58 / 0,09 %. Son una muestra de 17.027 celdas, no las 2.178.827. Sirven de referencia, no sustituyen a `tbl-bound`. |
| Recursos. | 32 núcleos, 125 GB de RAM (99 GB disponibles). `/` tiene 320 GB libres. Lectura del paso: TimesFM ≈ 146 GB, Palacios 31 GB, Tmin 6,3 GB, `train_2010…2016` ≈ 22 GB; total ≈ 205 GB. |
| Entorno. | `pyarrow`, `pandas`, `numpy` están en el venv del proyecto (`uv run`), no en el Python del sistema. |

**3.2 El código y los datos de Palacios no cambiaron**

Verificación hecha antes de este plan, sin volver a ejecutar sus scripts:

| Comprobación | Resultado |
|---|---|
| Commits posteriores a 2026-09-18 (última revisión de `paper.qmd`) en `reports/paper/scripts/` | Ninguno. |
| Cambios posteriores a la creación de `make_seam_fig.py` y `make_paper_figs.py` | Solo el trazado del contorno de Perú (cosmético). |
| `git status reports/paper` | Limpio. |
| Fecha de los datos | `predictions_2017_2020` 2026-07-22; `seam_windows_cache.parquet` 2026-08-26; `backtest_clean` 2026-09-14; `support_distance.parquet` 2026-09-15. Todos anteriores a la revisión final. |

Para dejarlo trazable, `real_informe.py` guarda en `fuentes_limpio.json` el `sha256` de los cinco scripts de Palacios usados como referencia (`make_seam_fig.py`, `warm_tail_diagnostics.py`, `excess_bound_eval.py`, `make_support_distance.py`, `november_diagnostics.py`), de `paper.qmd` y la fecha de modificación de los cuatro datos citados. Una comprobación posterior puede detectar un cambio.

**3.3 Origen de cada cifra (paper o calculada)**

| Cifra | Producto | Origen |
|---|---|---|
| `tbl-seam`: control +0,101 / sd 0,125 / −0,18…+0,42 / 0,0 %; Palacios −0,041 / sd 0,176 / −0,36…+0,54 / 0,0 % | Palacios | Paper. Control barato: recálculo desde el caché (arriba) |
| Misma estructura para TimesFM (media, sd, p1–p99, % de \|Δ\| > 1 °C) | TimesFM | Calculada |
| Diferencia TimesFM − Palacios de la media 2017–20 por celda y por tier | Ambos | Calculada |
| 0,1326 % > 35 °C, máx 41,16 °C, 132.920 celdas, todas fuera del dominio | Palacios | Paper. Cordura: recuentos del producto de Palacios que el paso ya produce |
| `tbl-support` (exceedance por tier) | Palacios | Paper |
| Misma estructura para TimesFM, con `pred`, y q50 y q90 como columnas adicionales | TimesFM | Calculada |
| Noviembre 1,556 % frente a octubre 0,027 %, incidencia anual 0,2015 / 0,1696 / 0,0293 / 0,1299 %, 40,6 % de días aislados, racha media 3,42 d, picos en días 313/331/313/331 | Palacios | Paper |
| Mismas medidas para TimesFM (con `pred`; las rachas solo con `pred`) | TimesFM | Calculada |
| `tbl-inherited` | Palacios | Paper. Control barato: recálculo con ll4 |
| `tbl-inherited` | TimesFM | Calculada con ll4 (`preds_nacional`) |
| `tbl-bound` (k = 0, 5, 6, 8, 10, 12) | Palacios | Paper |
| Misma estructura para TimesFM (`pred`, q10, q50, q90) | TimesFM | Calculada |
| Línea observada de la cota | Observado | Calculada (ll4, 17.027 celdas) |
| Solapamiento de excedencias > 35 °C | Ambos | Calculada |
| Serie nacional mensual de Palacios, mapa de media y mapa de excedencias de Palacios | Palacios | Calculada: el paper solo publica los PNG y la superposición de ambos productos necesita los datos. No se reportan como cifras nuevas de Palacios en tablas |
| Calibración de deciles por tier (ll4) | TimesFM | Calculada |
| Chequeo de cordura de Palacios: celdas (2.178.827), filas (3.183.266.247), `w3_pal` frente a la columna `w3` del caché, celdas con alguna excedencia (132.920) | Palacios | Calculada como subproducto del paso; se compara con el paper y el caché; no entra a las tablas |

Regla en caso de discrepancia: si algún recálculo de control no coincide con el paper (más allá del redondeo), se detiene la interpretación y se investiga. No se corrige la cifra del paper.

## 4. Dependencias

- **PLAN_3 (bloqueante).** `preds_real/` completo, `MANIFEST.csv` con 8.192 filas, `verify_real.csv` sin hallazgos y 2.178.827 celdas. El paso central lo exige al inicio.
- **PLAN_1 y PLAN_2 (documentales).** La constante `MANIFEST_REF_LIMPIO` y las convenciones `_limpio` salen de PLAN_1. Los tiers y las zonas ya existen en `$RES` y no dependen de su ejecución. El addendum de PLAN_1 (`docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`) y el de PLAN_3 deben existir antes de redactar el addendum de este plan, que los referencia.
- **Sin GPU.** Este plan es de CPU y disco. Puede correr incluso durante la inferencia de PLAN_3 sobre los buckets ya terminados solo para pruebas (nunca la corrida final).

## 5. Principio de no sobrescritura

- Nada se escribe bajo `$RES`. Se leen `predictions_2017_2020`, `future_tmin_by_bucket`, `bucketed_training_data`, `seam_windows_cache.parquet`, `support_distance.parquet`, `zone_table.parquet` y `backtest_clean/ll4/predictions.parquet`.
- No se modifica nada en `reports/paper/scripts/`, ni `paper.qmd`, ni los archivos con fuga (`$RES/tuning/backtest`).
- No se modifica `preds_real/` (producto de PLAN_3, solo lectura) ni `docs/protocol/timesfm_manifest.yaml` ni los addendums de PLAN_1 y PLAN_3. Se crea un addendum nuevo, aparte.
- `preds_nacional/`, `preds_cribado/`, `preds_departamental/` y `preds_escala/` no se tocan.
- `reports/metric_provenance.jsonl` es de solo adición.
- Los resultados publicados nuevos llevan sufijo `_limpio`.

## 6. Diseño: un solo paso por bucket

### 6.1 Entradas por bucket

Para cada `id_bucket=XXXX` (los 8.192 del `MANIFEST.csv` de PLAN_3):

1. TimesFM: `preds_real/id_bucket=XXXX/pred.parquet` (`ID`, `day`, `pred`, `q10…q90`).
2. Palacios: `predictions_2017_2020/id_bucket=XXXX/pred.parquet` (`ID`, `FECHA`, `TD_predicted`). Se calcula `day` y se comprueba la unión.
3. Tmin: `future_tmin_by_bucket/id_bucket=XXXX/future_tmin_{2017..2020}.parquet`, restringida a los IDs del bucket con Td.
4. Observado: `bucketed_training_data/id_bucket=XXXX/train_{2010..2016}.parquet`, columnas `ID`, `FECHA`, `TD`.

Tablas de búsqueda globales (se cargan una vez por proceso con el `initializer` del pool): `tier_code` (int8, indexado por `ID`, de `support_distance.parquet`; 255 si falta) y `clase_Ar_A` (bool, de `zone_table.parquet`, `zone_label.strip() == "A (r) A'"`). Ocupan ≈ 3 MB cada una porque `ID` máximo es 2.818.403.

### 6.2 Unión y validaciones por bucket

- Se ordena por `(ID, day)` si hace falta y se exige que el conjunto de IDs de TimesFM y de Palacios sea idéntico. Si lo es y ambos están ordenados, se trabaja con matrices `(n_celdas, 1461)` obtenidas por `reshape`. Si no, se usa la clave `ID * 2048 + day` con `searchsorted`.
- Tmin se pivota a `(n_celdas, 1461)` con `searchsorted` sobre los IDs (patrón medido en las pre-condiciones).
- Conteos de cordura por bucket: celdas, filas, NaN e infinitos de TimesFM y de Palacios, IDs sin pareja, filas con cuantiles que se cruzan (`q_i > q_{i+1}`).
- Observado 2010–2016: media por celda y mes (84 meses), solo celdas del bucket con Td.
- Derivados constantes de las 1.461 columnas: `ym` (0…47), año (0…3), mes del año (0…11) y día del año.

### 6.3 Acumuladores

Cada bucket devuelve un diccionario de arreglos pequeños y un DataFrame por celda (≈ 266 filas). El padre los suma. Productos: `pal`, `pred`, `q10`, `q50`, `q90` (q20…q80 no se usan en E10–E12). Tiers: 5 (`within`, `near`, `marginal`, `extrapolated`, `unsupported`).

| Acumulador | Forma | Alimenta |
|---|---|---|
| **Por celda** (`agg_celdas`): `w3_tfm`, `w3_pal` (media 2017–20), `max_pred`, `max_q90`, `max_pal`, `ancho_medio` (q90−q10), `n_valid`, `n_gt35_{pal,pred,q10,q50,q90}`, `n_both35` (pred y pal a la vez), `v{k}_{pal,pred,q10,q50,q90}` para los 6 valores de k | 2.178.827 filas, ≈ 50 columnas (float32/int16/int32), ≈ 0,5 GB | E10 (tbl-seam, F3, mapas), E11 (celdas afectadas, F4), E12 (mapas), solapamiento, cordura |
| **Mensual por tier y clase** (`m_tier_clase`): `n`, `suma`, `n_gt35` por producto; `ancho_suma`, `ancho_n` para q90−q10 | (5 productos, 5 tiers, 2 clases, 48 meses, 3) | E11 (tbl-support por tier, F5, noviembre, clase `A (r) A'`), fig-timeseries, anchura por mes y tier |
| **Histograma de valores** por producto y tier | (5, 5, 130 bins de 0,5 °C entre −20 y 45 + 2 desbordes) | F4 (panel A) |
| **Histograma de exceso** `Td − Tmin` por producto y tier | (5, 5, 80 bins de 0,5 °C entre −20 y 20 + 2 desbordes) | E12 (descriptivo de la distribución) |
| **Violaciones de cota** por producto, k, tier y mes: `n_alt` (`v > Tmin + k`), `suma_desp` (`max(v − Tmin − k, 0)`), `n_warm_retirado` (`v > 35` y `v > Tmin + k`) | (5, 6, 5, 48, 3) | E12 (tbl-bound), cobertura por q10/q50/q90 |
| **Rachas** > 35 °C (codificación por longitud dentro de cada ID, como `warm_tail_diagnostics.py`) para `pal` y `pred` | (2, 1462) | E11 (rachas) |
| **Día del año** de las excedencias | (2, 4, 366) | E11 (picos por año) |
| **Solapamiento celda-día** `pred > 35` frente a `pal > 35` | (5 tiers, 2, 2) | Tabla de solapamiento |
| **Observado mensual** 2010–2016: `suma`, `n` | (5 tiers, 84, 2) | fig-timeseries |
| **Extremos** (mín y máx) por producto y tier | (5, 5, 2) | E11 (máximos), E10 (rango) |
| **Chequeos** | escalares | Cordura (celdas, filas, NaN, IDs sin pareja, cruces de cuantiles) |

Los deciles q20…q80 no entran a ningún acumulador: solo se leen del Parquet las columnas `ID`, `day`, `pred`, `q10`, `q50`, `q90` de TimesFM, lo que reduce la lectura efectiva.

### 6.4 Paralelismo, memoria y reanudación

- `ProcessPoolExecutor` con 12 procesos y `chunksize=16`, como en los scripts de Palacios. El padre acumula los resultados a medida que llegan.
- Memoria por proceso: un bucket de TimesFM ocupa ≈ 16 MB (390 mil filas × 10 columnas × 4 B), más ≈ 3 MB de Palacios y las matrices temporales de 266 × 1.461 en float64 por producto; pico estimado < 1 GB por proceso. El padre: ≈ 0,5 GB de arreglos por celda más los acumuladores (< 100 MB). Total < 20 GB.
- El resultado final del paso se escribe de forma atómica (`.tmp` más renombrado) en `/home/cvelasquez/tdew_timesfm/agg_real/acumuladores_limpio.npz` y `agg_celdas_limpio.parquet`. Todo el informe se genera después desde esos archivos, sin releer los productos.
- El paso completo es corto (sección 12). No se implementa sentinela por bucket. Si se interrumpe, se relanza. Cada bucket es determinista, por lo que el resultado no depende del orden.

### 6.5 Definiciones y cuidados con los deciles

- Exceedance de un cuantil: `q_p > 35`. Es un indicador de cola de la distribución predictiva marginal en ese día, no una probabilidad de exceder 35 °C.
- Violación de la cota por cuantil: `q_p > Tmin + k`. La monotonía `q10 ≤ q50 ≤ q90` implica violaciones ordenadas; se reporta la fracción de filas con cuantiles cruzados.
- Las rachas y la autocorrelación solo se calculan con `pred` y con el producto de Palacios. Los cuantiles son marginales por paso y no forman trayectorias.
- Anchura: `q90 − q10` (intervalo central de 80 %, el más ancho que dan los deciles; no hay intervalos de 90 % o 95 %).

## 7. Pasos

**Paso 0. Verificación previa (no escribe nada).**
```bash
git -C /home/cvelasquez/Code/tdew status --short reports/paper
git -C /home/cvelasquez/Code/tdew log --since=2026-09-18 --oneline -- reports/paper/scripts
ls /home/cvelasquez/tdew_timesfm/preds_real/MANIFEST.csv
```
Se espera árbol limpio, sin commits posteriores y `MANIFEST.csv` con 8.192 filas.

**Paso 1. Módulo del paso (`experiments/timesfm/real_paso.py`, nuevo).** Funciones:
- `cargar_lookups(support_path, zone_path) -> (tier_code, clase_Ar_A)`.
- `unir_bucket(tfm_df, pal_df, tmin_df) -> (matrices, chequeos)`: ordenación, comprobación de IDs idénticos, pivote de Tmin, cálculo de `day`.
- `acumular_bucket(matrices, observado, lookups) -> dict`: todos los acumuladores de 6.3 para un bucket.
- `sumar(acc, parcial)`: suma de acumuladores, asociativa y conmutativa.
- `run(args) -> int`: pool, suma, escritura atómica, resumen.
- `main(argv)`. Opciones: `--tfm-root`, `--palacios-root`, `--tmin-root`, `--train-root`, `--support`, `--zone-table`, `--out-dir` (por defecto `/home/cvelasquez/tdew_timesfm/agg_real`), `--workers` (12), `--buckets` (rango o lista, para pruebas), `--ks`, `--bead-id`.

**Paso 2. Tests sin datos reales** (sección 11): `tests/test_timesfm_real_paso.py`. Se corren con `uv run pytest tests/test_timesfm_real_paso.py`.

**Paso 3. Prueba en 2 buckets** (no entregable; datos de prueba de PLAN_3 si `preds_real/` aún no está completo).
```bash
uv run python -m experiments.timesfm.real_paso --buckets 0,1 \
  --out-dir /home/cvelasquez/tdew_timesfm/agg_real_smoke
```
Se comprueba contra una implementación independiente en memoria (pandas) sobre esos dos buckets: recuentos por k, solapamiento, medias de ventana, rachas. Se mide el tiempo por bucket y se extrapola a 8.192 antes de la corrida completa.

**Paso 4. Paso completo.** Solo si PLAN_3 está terminado y verificado.
```bash
uv run python -m experiments.timesfm.real_paso --workers 12 \
  --out-dir /home/cvelasquez/tdew_timesfm/agg_real 2>&1 | tee /home/cvelasquez/tdew_timesfm/logs_paso_real.log
```
Se corre en `tmux` por prudencia. Al terminar: 8.192 buckets procesados, 2.178.827 celdas, 3.183.266.247 filas por producto.

**Paso 5. Controles de reproducción (baratos).** Dentro de `real_informe.py` y `real_ll4.py`:
- Cordura del producto de Palacios: 2.178.827 celdas; 3.183.266.247 filas; `w3_pal` del paso igual a la columna `w3` del caché (diferencia máxima < 1e-5 °C); 132.920 celdas con alguna excedencia y 0,1326 % de valores > 35 °C (paper). Solo se reportan como chequeo.
- Control de costura: A = `w2 − w1` del caché frente a +0,101 / 0,125 / −0,18…+0,42 / 0,0 %; B de Palacios = `w3 − w2` frente a −0,041 / 0,176 / −0,36…+0,54 / 0,0 %.
- «Heredado» de Palacios con ll4 frente a `tbl-inherited` (máximo y % dentro y fuera).
- Opcional y barato: recalcular `w1` y `w2` desde `train_2009…2016` en 64 buckets (≈ 3 GB leídos) y compararlos con el caché.

**Paso 6. Informe (`experiments/timesfm/real_informe.py`, nuevo).** Lee solo los acumuladores y construye los CSV de la sección 9. Escribe `fuentes_limpio.json` (hashes de scripts de Palacios y fechas de datos, sección 3.2) y la tabla de origen de cada cifra.

**Paso 7. ll4: heredado y calibración (`experiments/timesfm/real_ll4.py`, nuevo).** Lee `backtest_clean/ll4/predictions.parquet` y `preds_nacional/ll4__tmin_anom_full.parquet` (≈ 1,2 GB en memoria), une por `(ID, FECHA)` sobre las 17.027 celdas comunes y calcula:
- «Heredado» de TimesFM y de Palacios: máximo y fracción > 35 °C, observado y reconstruido, dentro (`tier == within`) y fuera.
- Línea observada de la cota (k = 0, 5, 6, 8, 10, 12), con `Tmin_hold`, para observado, Palacios y TimesFM (`pred`).
- Calibración de deciles: fracción de observaciones `≤ q_p` para p = 0,1…0,9 y cobertura del intervalo central de 80 %, por tier y global; fracción de filas con cuantiles cruzados.
Todo se reporta como muestra de 17.027 celdas (2013–2016), no como las 2.178.827.

**Paso 8. Figuras (`experiments/timesfm/real_figs.py`, nuevo).** Sección 9. Importa `add_peru_outline` desde `reports/paper/scripts/geo_overlay.py` con `sys.path` (sin modificarlo) y toma `lon`/`lat` de `support_distance.parquet`.

**Paso 9. Proveniencia, addendum, documentación y tests de proveniencia** (secciones 11 y 13).

**Paso 10. Registrar y cerrar.** Registros de proveniencia, `bd` y reporte de tareas (Notion según `CLAUDE.md`).

## 8. Análisis por experimento

### E10. Continuidad en la costura

- Ventanas: `w1` observado 2009–12, `w2` observado 2013–16 (del caché de Palacios, solo lectura), `w3_tfm` y `w3_pal` (2017–20, del paso). Control A = `w2 − w1`; costuras B_pal = `w3_pal − w2` y B_tfm = `w3_tfm − w2`. Se añade la diferencia directa D = `w3_tfm − w3_pal`.
- Para cada fila: media, desviación estándar, p1 y p99 y fracción de celdas con |Δ| > 1 °C, sobre 2.178.827 celdas. Corte adicional por tier.
- Serie nacional mensual (`fig-timeseries`): observado 2010-01…2016-12 (84 meses), y 2017-01…2020-12 para Palacios y TimesFM. En TimesFM se añade la media nacional de q10 y de q90 como banda, rotulada «media nacional de los deciles» (no es el decil de la media nacional).
- Lectura permitida: si B_tfm es comparable a A en media y dispersión, no hay discontinuidad de nivel anual en la costura. No se concluye que una serie sea mejor que otra.

### E11. Cola cálida

- Por producto: fracción de valores > 35 °C, máximo, celdas afectadas, y todo ello por tier de soporte (misma estructura que `tbl-support`), con TimesFM para `pred`, y q50 y q90 como columnas adicionales.
- Estacionalidad: porcentaje > 35 °C por mes del año y por año (F5), noviembre frente a octubre, incidencia anual, picos por día del año.
- Clase `A (r) A'`: mismas fracciones restringidas a la clase, por tier.
- Rachas con `pred` (y con Palacios, como control de la codificación): fracción de días aislados y racha media.
- «Heredado» (ll4): paso 7.
- Anchura q90−q10 por mes y por tier (en particular noviembre en la clase `A (r) A'`) y fracción de q90 > 35 °C.
- Solapamiento (por tier): celda-días con ambos > 35 °C, solo Palacios, solo TimesFM; índice de Jaccard; celdas con alguna excedencia en ambos, solo en uno y en ninguno.
- Lectura permitida: dónde y cuándo cada producto supera el umbral y cuánto coinciden. No se atribuye causa a la cola de TimesFM con el mecanismo de ancho de ventana de Palacios (no aplica a un modelo zero-shot).

### E12. Cota Td ≤ Tmin + k

- Para k = 0, 5, 6, 8, 10, 12 y cada producto: fracción de valores alterados, desplazamiento medio sobre todos los valores y fracción de los valores > 35 °C que la cota retira (misma definición que `excess_bound_eval.py`).
- TimesFM, adicionalmente: violación por q10, q50 y q90 (la fracción de celda-días con el cuantil por encima de `Tmin + k`) y el mismo corte por tier y por mes.
- Línea observada (ll4): paso 7.
- Agregado por celda (`agg_celdas_limpio.parquet`) con los recuentos `v{k}_*` para mapas. No se produce un producto acotado.
- Lectura permitida: la cota no es una restricción física estricta (el observado la rebasa en una fracción comparable), por lo que una violación de k pequeño no equivale a un valor no físico; la comparación útil es con la línea observada.

## 9. Artefactos de salida y rutas

| Artefacto | Ruta |
|---|---|
| Acumuladores y agregado por celda (fuera de git) | `/home/cvelasquez/tdew_timesfm/agg_real/acumuladores_limpio.npz`, `agg_celdas_limpio.parquet` |
| Log del paso | `/home/cvelasquez/tdew_timesfm/logs_paso_real.log` |
| E10, tabla de costura (paper + TimesFM + diferencia) | `reports/timesfm_benchmark/real_limpio/e10_costura_limpio.csv`, `e10_costura_por_tier_limpio.csv` |
| E10, serie nacional mensual | `reports/timesfm_benchmark/real_limpio/e10_serie_nacional_limpio.csv` |
| E11, soporte por tier | `reports/timesfm_benchmark/real_limpio/e11_soporte_tier_limpio.csv` |
| E11, mes, año, clase y rachas | `e11_mensual_limpio.csv`, `e11_clase_ArA_limpio.csv`, `e11_rachas_limpio.csv`, `e11_picos_limpio.csv` |
| E11, heredado y solapamiento | `e11_heredado_ll4_limpio.csv`, `e11_solapamiento_limpio.csv` |
| E11, anchura de deciles | `e11_anchura_q90_q10_limpio.csv` |
| E12, cota | `e12_cota_limpio.csv` (por producto y k), `e12_cota_cuantiles_limpio.csv`, `e12_linea_observada_ll4_limpio.csv` |
| Calibración de deciles (ll4) | `e12_calibracion_ll4_limpio.csv` |
| Figuras | `reports/timesfm_benchmark/real_limpio/figs/F3_costura_limpio.png`, `F4_cola_calida_limpio.png`, `F5_mes_del_ano_limpio.png`, `fig_timeseries_limpio.png`, `F2_mapa_media_limpio.png`, `E12_mapa_violaciones_k8_limpio.png`, `E12_calibracion_ll4_limpio.png` |
| Fuentes y hashes | `reports/timesfm_benchmark/real_limpio/fuentes_limpio.json` |
| Origen de cada cifra (paper o calculada) | `reports/timesfm_benchmark/TRACEABILITY.md` (sección nueva) |
| Addendum de manifiesto | `docs/protocol/timesfm_manifest_addendum_real_analisis_2017_2020.yaml` |
| Tests | `tests/test_timesfm_real_paso.py`, `tests/test_timesfm_real_paso_provenance.py` |

Contenido de las figuras (sufijo `_limpio`; se siguen los diseños del paper, que se leen y no se modifican):

- **F3_costura_limpio.** Paneles A (control observado), B Palacios, B TimesFM y distribuciones superpuestas, con el mismo límite de color. Mapas en `lon`/`lat` con el contorno de Perú.
- **F4_cola_calida_limpio.** Histograma de valores (escala log, ambos productos), mapa de celdas con máximo > 35 °C para cada producto y fracción mensual > 35 °C.
- **F5_mes_del_ano_limpio.** Fracción > 35 °C por mes del año, conjunta y por año, para ambos productos (y q90 de TimesFM como serie adicional).
- **fig_timeseries_limpio.** Media nacional mensual: observado 2010–2016 empalmado con Palacios y TimesFM, con banda de medias nacionales de q10 y q90.
- **F2_mapa_media_limpio.** Mapas de media 2017–2020 de ambos productos y de su diferencia.
- **E12_mapa_violaciones_k8_limpio.** Fracción por celda de días con `Td > Tmin + 8` para `pred` y q90 de TimesFM (y Palacios para referencia).
- **E12_calibracion_ll4_limpio.** Cobertura nominal frente a empírica por tier.

El producto de agregados por celda queda fuera de git (≈ 0,5 GB). En el repositorio solo entran los CSV pequeños, las figuras, el código, `fuentes_limpio.json` y el addendum.

## 10. Criterios de aceptación

1. El paso procesa los 8.192 buckets, con 2.178.827 celdas y 3.183.266.247 filas por producto, y cero IDs sin pareja entre TimesFM, Palacios y Tmin.
2. Cero NaN e infinitos en `pred` y los cuantiles de TimesFM dentro de las celdas del paso; la fracción de filas con cuantiles cruzados está reportada.
3. Cordura de Palacios: `w3_pal` coincide con el caché (diferencia máxima < 1e-5 °C); 132.920 celdas con alguna excedencia; 0,1326 % de valores > 35 °C, dentro de redondeo del paper.
4. Control de costura: A = +0,101 / 0,125 / −0,18…+0,42 / 0,0 % y B de Palacios = −0,041 / 0,176 / −0,36…+0,54 / 0,0 %, dentro de redondeo del paper.
5. «Heredado» de Palacios (ll4) dentro de redondeo de `tbl-inherited`. Si no coincide, se documenta y no se avanza a interpretar.
6. Las tablas de E10, E11 y E12 de TimesFM tienen la misma estructura que las del paper (filas, columnas y unidades), con el origen («paper» o «calculada») anotado en `TRACEABILITY.md`.
7. Para k = 0, 5, 6, 8, 10, 12, la fracción alterada de TimesFM es consistente entre `e12_cota_limpio.csv` y la suma de las violaciones por tier y mes.
8. Solapamiento: n11 + n10 + n01 + n00 = filas totales por tier, y n10 + n11 y n01 + n11 coinciden con los recuentos por producto.
9. Calibración en ll4 reportada por tier y global, con la salvedad de que es una muestra de 17.027 celdas.
10. Todos los CSV y figuras llevan sufijo `_limpio`, proveniencia y rutas relativas al repositorio; ninguno depende del run con fuga.
11. Nada escrito bajo `$RES`; `git status reports/paper` limpio.
12. Tests nuevos en verde y suite existente sin regresiones (`uv run pytest`).

## 11. Tests y proveniencia

`tests/test_timesfm_real_paso.py` (sin datos reales, con buckets sintéticos en `tmp_path`):

- `unir_bucket`: ordenación, rechazo de IDs distintos, pivote de Tmin con huecos, conversión `FECHA` ↔ `day` incluido el año bisiesto 2020.
- Recuentos de violaciones (`v > Tmin + k`), desplazamiento y `n_warm_retirado` frente a una implementación de fuerza bruta en pandas.
- Rachas > 35 °C frente a una implementación ingenua (longitudes dentro de cada ID, sin cruzar IDs).
- Solapamiento: las cuatro celdas de la tabla suman el total; simetría al intercambiar productos.
- `sumar` es asociativa y conmutativa (permutación de buckets da el mismo resultado).
- Tiers y clase `A (r) A'` asignados correctamente; IDs ausentes de `tier_code` se rechazan.
- Cuantiles cruzados contados correctamente.
- Histogramas: suma igual a n, bordes inclusivos/exclusivos y desbordes.
- Ventanas de costura: media por celda igual a la de pandas.

`tests/test_timesfm_real_paso_provenance.py` (patrón de `test_timesfm_evaluate_provenance.py`):

- Cada registro lleva `split_id` `real_2017_2020`, `panel_id` `real_2178827_td` (paso) o `nacional_17027_limpio` (ll4), `manifest_ref` al addendum nuevo, `test_period` (2017-01-01, 2020-12-31) para el paso y (2013-01-01, 2016-12-31) para ll4, `trained=False`.
- `notes` registra: sin verdad observada en 2017–2020, deciles marginales por paso, origen paper o calculada, hashes de `fuentes_limpio.json`.

`tests/test_metric_provenance.py`: agregar a `TRACKED_METRIC_FILES` los CSV `e10_*`, `e11_*`, `e12_*` de `real_limpio/` (cada uno con su `.provenance.json` al lado). `fuentes_limpio.json` no es una métrica y no se agrega.

Proveniencia: un registro por tabla publicada (no por bucket), escrito con `tdew_estimation.provenance` en `reports/metric_provenance.jsonl` (solo adición). Las rutas absolutas de `output_files` dependen de dónde se corra el comando; las salidas publicadas se generan con `--out-dir` bajo el repositorio para que `test_metric_provenance` las encuentre.

`docs/protocol/timesfm_manifest_addendum_real_analisis_2017_2020.yaml` (archivo nuevo): `addendum_de` el manifiesto original, el addendum de PLAN_1 y el de PLAN_3; define los análisis E10–E12, la definición de la cota (k y Tmin del mismo día), los tiers (`support_distance.parquet` de 2026-09-15), la regla paper-o-calculada y la salvedad de los deciles.

## 12. Estimación de tiempo y memoria

| Concepto | Estimación | Base |
|---|---|---|
| Lectura | ≈ 205 GB (TimesFM ≈ 146 GB leyendo solo `ID`, `day`, `pred`, `q10`, `q50`, `q90` es menos; Palacios 31 GB; Tmin 6,3 GB; observado ≈ 22 GB) | Tamaños de PLAN_3 y `du` de `bucketed_training_data` (112 GB × 7/36) |
| Cálculo | ≈ 3–4 s por bucket con los acumuladores completos, ≈ 3–4 h-núcleo en total; con 12 procesos ≈ 5–15 min | Medición con deciles simulados: 0,3 s por bucket; se multiplica por ≈ 10 para los acumuladores adicionales |
| Tiempo total | 20–60 min (acotado por lectura de disco en frío, no medido) | La caché de página (88 GB) acelera relecturas, no la primera pasada |
| Memoria | < 1 GB por proceso, < 20 GB en total | Un bucket ≈ 16 MB de TimesFM; agregado por celda ≈ 0,5 GB |
| Disco escrito | < 1 GB (acumuladores y agregado por celda) | |
| `real_ll4.py` | 1–3 min, ≈ 4 GB de RAM | 24,9 M filas × 2 tablas |
| Figuras e informe | < 5 min | Leen acumuladores |

La estimación del tiempo se fija con el paso 3 (dos buckets) antes de la corrida completa.

## 13. Documentación

- `reports/timesfm_benchmark/README.md`: sección «Costura, cola cálida y cota» con las tablas de E10–E12 lado a lado y las salvedades de la sección 14.
- `reports/timesfm_benchmark/TRACEABILITY.md`: filas para cada tabla y figura, con el origen de cada cifra (paper o calculada), citando el addendum y `fuentes_limpio.json`.
- `reports/timesfm_benchmark/limitaciones.md`: añadir (a) no hay verdad observada en 2017–2020, (b) los deciles son marginales por paso y no verificables allí, (c) TimesFM no conoce restricciones físicas.
- `experiments/timesfm/README.md`: descripción del paso único, sus acumuladores y cómo reproducirlo.

## 14. Riesgos

- **Dependencia de PLAN_3.** Hasta que el producto esté completo no se puede ejecutar el paso. Mitigación: tests con buckets sintéticos y prueba con los buckets ya terminados.
- **Lectura en frío.** 205 GB en 20–60 min depende del disco; se mide en la prueba de dos buckets. Cálculo no es el cuello de botella.
- **Cuantiles que se cruzan.** Un modelo sin restricciones puede producir `q_i > q_{i+1}`. Se reporta la fracción y no se reordena silenciosamente.
- **Sobreinterpretación de los deciles.** Son marginales por paso de horizonte: no sirven para rachas ni para probabilidades conjuntas. La calibración en ll4 (2013–2016, 17.027 celdas) no garantiza calibración en 2017–2020. Cada tabla de deciles lleva esa salvedad.
- **Cifras de Palacios heredadas del paper.** Si algún dato fuente cambió después del 2026-09-18, las cifras citadas se desviarían. Los hashes y fechas de `fuentes_limpio.json` y los tres controles baratos lo detectarían.
- **Muestra ll4 frente a panel completo.** La línea observada de la cota y el «heredado» salen de 17.027 celdas (8.306 within, 2.946 unsupported, etc.), que sobrerrepresentan el dominio frente a los 2,18 millones. Se rotula así y no se compara punto a punto con `tbl-bound`.
- **Comparaciones de umbral en float32.** Se evita convirtiendo a float64 antes de comparar.
- **Espacio.** El paso escribe < 1 GB; `/` tiene 320 GB libres, pero PLAN_3 puede dejarlo en 81–83 %. Se verifica antes de escribir.
- **Rutas relativas de Palacios.** `warm_tail_diagnostics.py` escribe en `.asta/theories/` con ruta relativa; por eso no se ejecuta ni se importa.

## 15. Qué no entra y qué no puede concluirse

No entra:

- Reejecutar los scripts de Palacios, modificar `reports/paper/scripts/` o escribir bajo `$RES`.
- Una nueva inferencia de TimesFM (este plan solo lee `preds_real/`) ni inferencia ll4 de las 2.178.827 celdas.
- Producir o publicar un producto acotado.
- Otras variantes de TimesFM, fine-tuning o ajuste (clipping, recalibración).
- Los análisis de noviembre del paper que dependen del interior del método de Palacios (`november_diagnostics.py`: LOYOCV, ancho de ventana, R² en muestra): no tienen equivalente en un modelo zero-shot.

No puede concluirse, porque no hay verdad observada de Td en 2017–2020:

- Que un producto tenga más o menos «error» que otro, ni que un valor > 35 °C o que viole la cota sea un error. Solo se puede decir cuánto se parecen y dónde discrepan.
- Que la cola cálida de TimesFM esté causada por falta de soporte observacional, por analogía con el resultado de Palacios. Solo se muestra su distribución por tier y su solapamiento.
- Que la anchura q90−q10 por mes o por tier mida incertidumbre real en 2017–2020. Solo se reporta su distribución y su calibración medida en 2013–2016.
- Que el cumplimiento de la cota demuestre exactitud: el observado también rebasa Td ≤ Tmin + k.
- Que la continuidad en la costura (E10) implique exactitud: solo descarta una discontinuidad de nivel anual del tamaño de la variabilidad natural.

### Archivos críticos para la implementación
- `experiments/timesfm/real_paso.py` (nuevo)
- `experiments/timesfm/real_informe.py` (nuevo)
- `experiments/timesfm/real_ll4.py` (nuevo)
- `experiments/timesfm/real_figs.py` (nuevo)
- `tests/test_timesfm_real_paso.py` (nuevo)
