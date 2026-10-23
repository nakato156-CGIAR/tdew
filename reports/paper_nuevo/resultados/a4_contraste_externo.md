# A4. Contraste externo limitado de Td 2017–2020 con estaciones ISD

Bead `tdew-ra6`. Código: `experiments/a4_externo/` (ver su `README.md`). Tablas: `a4_*.csv` en esta carpeta; las que terminan en `_h4b2` son la variante de sensibilidad del criterio diario. Fecha de cálculo: 2026-10-20, rama `tdew-214-real-2017-2020`, commit base `4a10f16` (sin commit propio).

> Revisión de coherencia (2026-10-21). Se informan únicamente productos frente a estaciones y TimesFM frente a Palacios sobre los mismos días. Las filas históricas de ERA5 y ERA5-Land permanecen en los CSV, pero se excluyen de las tablas y de la interpretación de este documento. No se usan como escala. El acuerdo entre productos no equivale a exactitud.

## Por qué se realiza el contraste

En 2017–2020 no hay Td observado de PISCO. Las evaluaciones retrospectivas miden la reproducción del Td grillado; este contraste compara con observaciones de estación en puntos. La independencia de esas estaciones respecto de las usadas en PISCO no está verificada. El artículo previo describe covariables espaciales compartidas entre Td y Tmin; el detalle de MODIS y la referencia Huerta 2023 requieren comprobación bibliográfica antes de trasladarse al artículo. No se usa ese detalle como explicación causal.

## Datos y criterios

**Estaciones.** NOAA NCEI ISD global-hourly (espejo público en AWS, `noaa-global-hourly-pds`), todas las estaciones con `CTRY=PE` en `isd-history.csv` con registro hasta 2009 o después: 37 estaciones, 378 de 444 archivos anuales 2009-2020 disponibles (el resto devuelve 404). Control de calidad por observación: se descarta `+9999`, se aceptan solo los códigos de calidad 0, 1, 4, 5 y 9, se descarta Td fuera de [-40, 35] °C y Td > T + 0,5 °C. Las observaciones de una misma hora (SYNOP y METAR) se resumen con la mediana.

**Td diaria.** Día local UTC-5. Un día es válido con al menos 4 horas válidas y al menos una en cada bloque local de 6 h (00-06, 06-12, 12-18, 18-24); la Td diaria es la media de las cuatro medias de bloque. Este criterio deja fuera a los aeropuertos que no reportan de noche (Juliaca, Talara, Tarapoto, Chachapoyas, Huaraz, Ilo y otros). Con un criterio de al menos 2 bloques (`_h4b2`) entran hasta 26 estaciones según período y métrica, y puede haber mayor representación de las horas de luz; se usa solo como sensibilidad.

**Muestra principal.** Estaciones con al menos 180 días comunes a las fuentes de la muestra en el periodo: 13 para Td absoluta en 2009–2016 y 12 para sus anomalías; 12 para ambas métricas en 2017–2020. Andahuaylas solo tiene datos útiles hasta 2016 y no entra en la muestra de anomalías del agregado. En 2020 hay menos días-estación válidos; los conteos se separan por métrica en los CSV. Los registros revisados muestran menor cobertura nocturna desde marzo de 2020.

**Celda.** Cada estación se asigna a la celda PISCO 0,01° de centro más cercano: `ID = fila·1422 + columna`, fila 0 en 1,22°N, columna 0 en 81,40°W (verificado contra `zone_table.parquet`, discrepancia máxima 1e-14°). La elevación de la celda se aproxima con el DEM de 90 m de Open-Meteo en su centro.

**Fuentes comparadas.** `pisco`: TD de `bucketed_training_data` (PISCO v1.1), 2009–2016. `palacios`: `tuning/predictions_2017_2020`. `timesfm`: `preds_real` (`tmin_anom_full`). Se usan los pares estación–fuente ya calculados.

**Anomalías.** Cada serie menos su climatología armónica (media y tres armónicos anuales), ajustada en 2009–2016. La estación usa la suya; `pisco`, `palacios` y `timesfm` usan la climatología de PISCO en la celda. La transformación descuenta diferencias climatológicas fijas entre estación y celda. En 2009–2016 se evalúa con climatología dentro de muestra y en 2017–2020 fuera de muestra; el cambio de error entre períodos no se atribuye a una causa aislada.

Errores como fuente − estación. Intervalos de 95 % por bootstrap de estaciones (2.000 réplicas) para la diferencia de RMSE agrupado sobre los mismos días.

## Estaciones usadas

| USAF | Estación (ICAO) | Lat, lon | Elev. (m) | Est. − celda (m) | Td PISCO 09-16 sesgo / RMSE | Td `palacios` 17-20 | Td `timesfm` 17-20 | Anom. RMSE PISCO 09-16 | `palacios` | `timesfm` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 843770 | Iquitos, Secada Vignetta (SPQT) | -3,785, -73,309 | 93 | -4 | +1,91 / 2,34 | +1,74 / 1,93 | +1,94 / 2,09 | 1,31 | 0,80 | 0,73 |
| 844010 | Piura, Concha Iberico (SPUR) | -5,206, -80,616 | 35 | +2 | +0,68 / 0,98 | +0,97 / 1,35 | +1,10 / 1,46 | 0,70 | 0,99 | 1,05 |
| 844520 | Chiclayo, Quiñones (SPHI) | -6,787, -79,828 | 30 | +3 | +0,55 / 0,72 | +0,51 / 0,97 | +0,90 / 1,21 | 0,43 | 0,82 | 0,87 |
| 844720 | Cajamarca, Revoredo (SPJR) | -7,139, -78,489 | 2676 | -4 | -1,40 / 2,06 | -0,26 / 1,52 | -0,10 / 1,33 | 1,45 | 1,89 | 1,88 |
| 845010 | Trujillo, Martínez de Pinillos (SPRU) | -8,081, -79,109 | 32 | +6 | +2,11 / 2,25 | +1,51 / 1,68 | +1,58 / 1,74 | 0,68 | 0,92 | 0,86 |
| 845150 | Pucallpa, Abensur (SPCL) | -8,378, -74,574 | 156 | -2 | -1,36 / 2,20 | -1,15 / 2,08 | -1,09 / 2,00 | 1,22 | 1,16 | 1,11 |
| 846280 | Lima-Callao, Jorge Chávez (SPJC) | -12,022, -77,114 | 34 | +13 | +1,14 / 1,29 | +1,23 / 1,38 | +1,21 / 1,35 | 0,60 | 0,63 | 0,59 |
| 846730 | Ayacucho, Mendívil (SPHO) | -13,155, -74,204 | 2718 | -5 | -1,61 / 2,45 | -0,17 / 3,05 | -0,20 / 3,00 | 1,66 | 3,41 | 3,32 |
| 846860 | Cusco, Velasco Astete (SPZO) | -13,536, -71,939 | 3310 | +22 | +3,97 / 4,50 | +4,10 / 4,68 | +4,19 / 4,67 | 1,72 | 1,89 | 1,74 |
| 846880 | Andahuaylas (SPHY) | -13,706, -73,350 | 3444 | -107 | +4,24 / 4,49 | — | — | — | — | — |
| 846910 | Pisco (SPSO) | -13,745, -76,220 | 12 | +5 | +1,01 / 1,25 | +1,40 / 1,63 | +1,42 / 1,62 | 0,70 | 0,87 | 0,83 |
| 847520 | Arequipa, Rodríguez Ballón (SPQU) | -16,341, -71,583 | 2562 | +29 | +5,91 / 7,39 | +4,95 / 6,86 | +5,03 / 6,86 | 2,89 | 3,19 | 3,15 |
| 847820 | Tacna, Ciriani (SPTN) | -18,053, -70,276 | 469 | +26 | +1,59 / 1,86 | +1,53 / 1,91 | +1,64 / 1,97 | 0,74 | 0,89 | 0,79 |

Valores en °C. La diferencia de elevación estación − celda está entre -5 y +29 m salvo en Andahuaylas (-107 m). La lista completa, con conteos de registros y las estaciones excluidas, está en `a4_estaciones.csv` y `a4_estaciones_excluidas.csv`.

## Resultados agregados

Muestra de productos (`a4_por_periodo.csv`, `muestra = productos`; los valores de productos coinciden con las filas históricas de muestra común). Se mantienen exactamente las fechas y estaciones de los resultados existentes.

| Fuente | Período | Métrica | Días-estación | Estaciones | Sesgo (°C) | RMSE (°C) | r |
|---|---|---|---|---|---|---|---|
| pisco | 2009-2016 | Td | 31.326 | 13 | +1,42 | 3,06 | 0,946 |
| pisco | 2009-2016 | Anomalía | 30.751 | 12 | +0,02 | 1,33 | 0,625 |
| palacios | 2017-2020 | Td | 14.666 | 12 | +1,38 | 2,88 | 0,949 |
| palacios | 2017-2020 | Anomalía | 14.666 | 12 | +0,18 | 1,68 | 0,502 |
| timesfm | 2017-2020 | Td | 14.666 | 12 | +1,48 | 2,89 | 0,951 |
| timesfm | 2017-2020 | Anomalía | 14.666 | 12 | +0,29 | 1,63 | 0,556 |

Diferencias de RMSE agrupado con IC 95 % por estaciones (`a4_delta_rmse_bootstrap.csv`):

| Comparación | Periodo | Td | Anomalía |
|---|---|---|---|
| `timesfm` − `palacios` | 2017-2020 | +0,010 [-0,025; +0,057] | -0,046 [-0,073; -0,019] |

### Por año

RMSE de anomalía frente a estación (`a4_por_anio.csv`). La última columna cuenta días-estación de la métrica de anomalías, no necesariamente los de Td absoluta:

| Año | PISCO | `palacios` | `timesfm` | Días-estación (anomalías) |
|---|---|---|---|---|
| 2009 | 1,36 |  |  | 3.412 |
| 2010 | 1,38 |  |  | 3.572 |
| 2011 | 1,26 |  |  | 3.586 |
| 2012 | 1,34 |  |  | 4.333 |
| 2013 | 1,50 |  |  | 3.953 |
| 2014 | 1,00 |  |  | 3.239 |
| 2015 | 1,29 |  |  | 4.319 |
| 2016 | 1,40 |  |  | 4.337 |
| 2017 |  | 1,46 | 1,42 | 4.343 |
| 2018 |  | 1,54 | 1,49 | 4.312 |
| 2019 |  | 2,11 | 2,05 | 4.364 |
| 2020 |  | 1,18 | 1,19 | 1.647 |

Sesgo de Td (fuente − estación) por año: PISCO entre +0,71 (2014) y +1,93 (2009); `palacios` +1,01, +1,30, +1,75, +1,56 y `timesfm` +1,10, +1,42, +1,84, +1,65 en 2017-2020. El RMSE de Td de los dos productos va de 1,89 a 3,16 según el año.

### Desacuerdo entre productos

| Año | RMSE TimesFM − Palacios en celdas de estación | RMSE en panel nacional (`real_limpio`) | Sesgo TimesFM − Palacios en estaciones |
|---|---|---|---|
| 2017 | 0,30 | 0,46 | +0,08 |
| 2018 | 0,34 | 0,43 | +0,08 |
| 2019 | 0,32 | 0,50 | +0,08 |
| 2020 | 0,33 | 0,47 | +0,06 |

Fuente: `a4_desacuerdo_oni.csv`; se seleccionan únicamente las columnas de productos, sin usar índices climáticos para interpretar sus diferencias. Estas cifras miden acuerdo entre reconstrucciones, no error frente a observaciones nacionales de Td, que no están disponibles en ese período.

## Lectura

En 2009–2016 PISCO tiene sesgo +1,42 °C y RMSE 3,06 °C frente a las 13 estaciones. Los productos 2017–2020 muestran sesgos +1,38 y +1,48 °C y patrones locales compatibles con los desfases de PISCO: en Arequipa, +4,95 y +5,03 °C; en Cusco, +4,10 y +4,19 °C. Esto no identifica por sí solo el origen del sesgo. El RMSE absoluto y el de anomalías describen aspectos distintos; se informan ambos.

En Td, TimesFM − Palacios tiene una diferencia de RMSE de +0,010 °C, IC [−0,025; +0,057]. No se distinguió el signo de la diferencia y no se estableció equivalencia. En anomalías la diferencia es −0,046 °C, IC [−0,073; −0,019], sobre 12 estaciones. El remuestreo refleja variación entre las estaciones disponibles, no representatividad nacional ni incertidumbre espacial y temporal completa.

En Ayacucho el sesgo de anomalía de 2019 es aproximadamente +4,3 °C para ambos productos. El patrón es compatible con un cambio de estación o procesamiento, pero no se comprobaron metadatos que permitan atribuirlo a esa causa. Al dejar fuera Ayacucho, el RMSE de anomalía 2017–2020 baja a 1,44 °C para Palacios y 1,40 °C para TimesFM; el de PISCO en 2009–2016 queda en 1,31 °C. Al dejar fuera Arequipa, los valores son 1,47, 1,42 y 1,08 °C, respectivamente (`a4_dejar_una_estacion_fuera.csv`). No se excluyó ninguna de esas estaciones de las tablas principales.

Con el criterio diario de al menos dos bloques de 6 h (`a4_por_periodo_h4b2.csv`), hay 23 estaciones para anomalías en ambos períodos; para Td absoluta hay 23 en 2009–2016 y 26 en 2017–2020. El RMSE de anomalía es 1,45 °C para PISCO, 1,98 °C para Palacios y 1,94 °C para TimesFM. La brecha TimesFM − Palacios es −0,045 °C [−0,073; −0,009] en anomalías y −0,001 °C [−0,031; +0,036] en Td. Cambian simultáneamente las estaciones y el criterio de media diaria; no se aisló el efecto de cada cambio.

El backtest contra PISCO y este contraste miden cosas distintas: reproducir Td grillada frente a aproximar observaciones atmosféricas en puntos. Los resultados de este contraste no convierten el error nacional frente a PISCO en una estimación del error atmosférico nacional.

## Chequeo de la Tmin regridada 2017-2020

Panel nacional (17.027 celdas), `future_tmin_by_bucket` (2017-2020) frente a TMIN de `bucketed_training_data` (2013-2016). Las dos son PISCOt v1.2 en la grilla de 2,8 M celdas; no hay años solapados, así que no hay correlación día a día posible.

- Distribución global (`a4_tmin_global.csv`): media 17,31 frente a 17,28 °C, desviación 8,01 frente a 7,95; p05 -0,60 frente a -0,38, p50 21,06 frente a 21,02, p95 23,94 frente a 23,92.
- Por mes (`a4_tmin_por_mes.csv`): las medias difieren entre -0,25 (enero) y +0,29 °C (setiembre); las diferencias de percentiles no pasan de 0,7 °C (p95 de enero, 24,41 frente a 23,75).
- Medias por celda y mes (`a4_tmin_celda_mes.csv`): r = 0,9991 entre periodos; r = 0,978 del ciclo anual por celda (sin la media de la celda); diferencia media -0,026 °C, desviación 0,34, p05/p95 ±0,56; 1,3 % de los pares celda-mes difieren en más de 1 °C.
- Costura dic/ene (`a4_tmin_costura.csv`): el salto medio ene-2017 − dic-2016 es -0,002 °C (otros años, de -0,33 a +1,02). Su dispersión entre celdas es mayor (desviación 1,33 frente a 0,66-0,90 en los demás años). No se identificó su causa; no se atribuye a ENSO ni a una diferencia de regrillado.
- Textura espacial (`a4_tmin_rugosidad.csv`, diferencia de Tmin media anual entre celdas vecinas de una fila, 16.730 pares): desviación de 0,40-0,45 °C en todos los años de 2013 a 2020, sin cambio en 2017. La textura medida no identifica un cambio de regrillado; tampoco permite descartarlo por sí sola.

Los resúmenes consultados no muestran un desplazamiento global grande de nivel o distribución en la Tmin al pasar a 2017–2020; no constituyen una prueba de equivalencia de distribuciones; la mayor dispersión del salto de enero de 2017 queda como punto abierto.

## Limitaciones

- **Independencia frente a PISCO.** Se usan aeropuertos CORPAC/FAP y el artículo previo describe 182 estaciones SENAMHI para PISCO Td v1.1. No se verificó la correspondencia entre esas redes. Los desfases locales no demuestran independencia. En 2017–2020 no hay solapamiento temporal del objetivo con PISCO Td, pero puede persistir dependencia espacial respecto de estaciones usadas para construir el producto de entrenamiento; no se afirma validación plenamente independiente.
- **Insumos compartidos.** El contraste en puntos no elimina posibles dependencias del producto de entrenamiento. La descripción bibliográfica específica de LST compartida queda por comprobar, sin atribución causal.
- **Muestra pequeña y sesgada.** 12-13 estaciones, todas en aeropuertos: 6 en la costa (Piura, Chiclayo, Trujillo, Lima, Pisco, Tacna), 5 en los Andes (Cajamarca, Ayacucho, Cusco, Arequipa y Andahuaylas, esta solo en 2009-2016) y 2 en la Amazonía (Iquitos, Pucallpa). Ninguna está en el altiplano con el criterio principal. Los intervalos por bootstrap de estaciones son anchos.
- **Punto frente a celda.** Una estación de aeropuerto representa un punto; la celda PISCO es de ≈1 km y el Td grillado es suavizado. Parte del error de todas las fuentes es representatividad.
- **Calidad de estación.** Se aplicó solo control de calidad básico. Ayacucho 2019-2020 tiene un salto aparente que afecta a todas las fuentes; no se corrigió ni se excluyó en las tablas principales (se informa el efecto de dejarlo fuera). En 2020 la cobertura nocturna cae desde marzo.
- **Climatología de anomalías.** Ajustada en 2009-2016 con 8 años o menos según la estación; en 2009-2016 el contraste de anomalías está dentro de la muestra.

## Archivos

- Código: `experiments/a4_externo/{__init__,isd,download,grid,openmeteo,compare,tmin_check}.py`, `README.md`; prueba `tests/test_a4_isd.py`.
- Tablas: `a4_estaciones.csv`, `a4_estaciones_excluidas.csv`, `a4_dias_por_estacion_anio.csv`, `a4_por_periodo.csv`, `a4_por_anio.csv`, `a4_por_estacion.csv`, `a4_por_estacion_anio_anom.csv`, `a4_resumen_entre_estaciones.csv`, `a4_todas_las_parejas_por_periodo.csv`, `a4_delta_rmse_bootstrap.csv`, `a4_dejar_una_estacion_fuera.csv`, `a4_desacuerdo_oni.csv`, `a4_indices_2009_2020.csv`, `a4_tmin_*.csv`, `a4_config.json`; las mismas con sufijo `_h4b2` para la sensibilidad.
- Datos descargados (fuera del repositorio): `/home/cvelasquez/tdew_timesfm/a4/` (`isd_raw/`, `isd_meta/`, `indices/`, `openmeteo_raw/`, pares estación-fuente en `pares_estacion_fuente*.parquet`).

Este análisis se preparó con asistencia de IA generativa (Claude; revisión documental con Codex) y debe revisarse con Palacios y SENAMHI antes de usarse en el paper.
