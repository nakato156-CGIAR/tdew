# A4. Contraste externo de Td 2017-2020 con estaciones ISD y ERA5

Bead `tdew-ra6`. Código: `experiments/a4_externo/` (ver su `README.md`). Tablas: `a4_*.csv` en esta carpeta; las que terminan en `_h4b2` son la variante de sensibilidad del criterio diario. Fecha de cálculo: 2026-10-20, rama `tdew-214-real-2017-2020`, commit base `4a10f16` (sin commit propio).

> **Nota del 2026-10-21.** ERA5 y ERA5-Land no se usan como comparación con los productos. Son otros productos, con otra grilla (0,25° y 0,1° frente a 0,01° de PISCO) y otros insumos; cambiar de dataset queda reservado para la prueba de transferencia (T1). Sus filas y la lectura 2 se conservan solo como registro de lo calculado y no se citan en el paper. Las comparaciones válidas de esta sección son productos frente a estaciones y TimesFM frente a Palacios sobre las mismas estaciones y días.

## Por qué hace falta una referencia externa

En 2017-2020 no hay Td observado de PISCO. Los dos productos de Td (Palacios `tuned` y TimesFM `tmin_anom_full`) se validaron hasta ahora contra el Td grillado de PISCO v1.1 en bloques ocultos de 1981-2016. Según Huerta et al. (2022, tabla 1; 2023), el Td de PISCOeo_pm se interpola con LST_mean de MODIS y la Tmin de PISCOt (el predictor) con LST_night de MODIS. Los dos campos comparten insumos, así que un buen puntaje frente al Td grillado no prueba exactitud frente al Td atmosférico. Este contraste usa observaciones de estación que no pasan por la grilla.

## Datos y criterios

**Estaciones.** NOAA NCEI ISD global-hourly (espejo público en AWS, `noaa-global-hourly-pds`), todas las estaciones con `CTRY=PE` en `isd-history.csv` con registro hasta 2009 o después: 37 estaciones, 378 de 444 archivos anuales 2009-2020 disponibles (el resto devuelve 404). Control de calidad por observación: se descarta `+9999`, se aceptan solo los códigos de calidad 0, 1, 4, 5 y 9, se descarta Td fuera de [-40, 35] °C y Td > T + 0,5 °C. Las observaciones de una misma hora (SYNOP y METAR) se resumen con la mediana.

**Td diaria.** Día local UTC-5. Un día es válido con al menos 4 horas válidas y al menos una en cada bloque local de 6 h (00-06, 06-12, 12-18, 18-24); la Td diaria es la media de las cuatro medias de bloque. Este criterio deja fuera a los aeropuertos que no reportan de noche (Juliaca, Talara, Tarapoto, Chachapoyas, Huaraz, Ilo y otros). Con un criterio de al menos 2 bloques (`_h4b2`) entran 26 estaciones, pero la media diaria queda sesgada hacia las horas de luz; se usa solo como sensibilidad.

**Muestra principal.** Estaciones con al menos 180 días comunes a todas las fuentes en el periodo: 13 en 2009-2016 y 12 en 2017-2020 (Andahuaylas solo tiene datos útiles hasta 2016). En 2020 hay muchos menos días válidos (1.647 frente a ≈4.300 en otros años) porque, desde marzo de 2020, varios aeropuertos dejaron de reportar de noche.

**Celda.** Cada estación se asigna a la celda PISCO 0,01° de centro más cercano: `ID = fila·1422 + columna`, fila 0 en 1,22°N, columna 0 en 81,40°W (verificado contra `zone_table.parquet`, discrepancia máxima 1e-14°). La elevación de la celda se aproxima con el DEM de 90 m de Open-Meteo en su centro.

**Fuentes comparadas.** `pisco`: TD de `bucketed_training_data` (PISCO v1.1), 2009-2016. `palacios`: `tuning/predictions_2017_2020`. `timesfm`: `preds_real` (`tmin_anom_full`). `era5` (0,25°) y `era5_land` (0,1°): Td media diaria local en la coordenada de la estación, obtenida de la API histórica de Open-Meteo sin credenciales, con la corrección por elevación desactivada (`elevation=nan`). Para ERA5-Land, en Trujillo y Pisco la celda más cercana es oceánica y no tiene dato; se usó el punto desplazado 0,1° al este (`era5_land_desplazamiento_este` en `a4_estaciones.csv`).

**Anomalías.** Cada serie menos su climatología armónica (media y tres armónicos anuales) ajustada en 2009-2016. La estación usa la suya; `pisco`, `palacios` y `timesfm` usan la de PISCO en la celda, porque los productos continúan a PISCO; ERA5 y ERA5-Land usan la propia. Así la anomalía no depende del desfase fijo entre estación y celda. En 2009-2016 la climatología está ajustada dentro de la muestra y en 2017-2020 no, para todas las fuentes por igual; ERA5 sirve de control de ese efecto.

Errores como fuente − estación. Intervalos de 95 % por bootstrap de estaciones (2.000 réplicas) para la diferencia de RMSE agrupado sobre los mismos días.

## Estaciones usadas

| USAF | Estación (ICAO) | Lat, lon | Elev. (m) | Est. − celda (m) | Td PISCO 09-16 sesgo / RMSE | Td `palacios` 17-20 | Td `timesfm` 17-20 | Anom. RMSE PISCO 09-16 | `palacios` | `timesfm` | ERA5-Land 17-20 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 843770 | Iquitos, Secada Vignetta (SPQT) | -3,785, -73,309 | 93 | -4 | +1,91 / 2,34 | +1,74 / 1,93 | +1,94 / 2,09 | 1,31 | 0,80 | 0,73 | 0,50 |
| 844010 | Piura, Concha Iberico (SPUR) | -5,206, -80,616 | 35 | +2 | +0,68 / 0,98 | +0,97 / 1,35 | +1,10 / 1,46 | 0,70 | 0,99 | 1,05 | 1,03 |
| 844520 | Chiclayo, Quiñones (SPHI) | -6,787, -79,828 | 30 | +3 | +0,55 / 0,72 | +0,51 / 0,97 | +0,90 / 1,21 | 0,43 | 0,82 | 0,87 | 0,80 |
| 844720 | Cajamarca, Revoredo (SPJR) | -7,139, -78,489 | 2676 | -4 | -1,40 / 2,06 | -0,26 / 1,52 | -0,10 / 1,33 | 1,45 | 1,89 | 1,88 | 1,65 |
| 845010 | Trujillo, Martínez de Pinillos (SPRU) | -8,081, -79,109 | 32 | +6 | +2,11 / 2,25 | +1,51 / 1,68 | +1,58 / 1,74 | 0,68 | 0,92 | 0,86 | 1,03 |
| 845150 | Pucallpa, Abensur (SPCL) | -8,378, -74,574 | 156 | -2 | -1,36 / 2,20 | -1,15 / 2,08 | -1,09 / 2,00 | 1,22 | 1,16 | 1,11 | 0,66 |
| 846280 | Lima-Callao, Jorge Chávez (SPJC) | -12,022, -77,114 | 34 | +13 | +1,14 / 1,29 | +1,23 / 1,38 | +1,21 / 1,35 | 0,60 | 0,63 | 0,59 | 0,76 |
| 846730 | Ayacucho, Mendívil (SPHO) | -13,155, -74,204 | 2718 | -5 | -1,61 / 2,45 | -0,17 / 3,05 | -0,20 / 3,00 | 1,66 | 3,41 | 3,32 | 3,31 |
| 846860 | Cusco, Velasco Astete (SPZO) | -13,536, -71,939 | 3310 | +22 | +3,97 / 4,50 | +4,10 / 4,68 | +4,19 / 4,67 | 1,72 | 1,89 | 1,74 | 1,68 |
| 846880 | Andahuaylas (SPHY) | -13,706, -73,350 | 3444 | -107 | +4,24 / 4,49 | — | — | — | — | — | — |
| 846910 | Pisco (SPSO) | -13,745, -76,220 | 12 | +5 | +1,01 / 1,25 | +1,40 / 1,63 | +1,42 / 1,62 | 0,70 | 0,87 | 0,83 | 0,85 |
| 847520 | Arequipa, Rodríguez Ballón (SPQU) | -16,341, -71,583 | 2562 | +29 | +5,91 / 7,39 | +4,95 / 6,86 | +5,03 / 6,86 | 2,89 | 3,19 | 3,15 | 2,57 |
| 847820 | Tacna, Ciriani (SPTN) | -18,053, -70,276 | 469 | +26 | +1,59 / 1,86 | +1,53 / 1,91 | +1,64 / 1,97 | 0,74 | 0,89 | 0,79 | 0,96 |

Valores en °C. La diferencia de elevación estación − celda está entre -5 y +29 m salvo en Andahuaylas (-107 m). La lista completa, con conteos de registros y las estaciones excluidas, está en `a4_estaciones.csv` y `a4_estaciones_excluidas.csv`.

## Resultados agregados

Muestra común con reanálisis (`a4_por_periodo.csv`, `muestra = con_reanalisis`; coincide con la muestra solo de productos porque todas las estaciones tienen ERA5-Land).

| Fuente | Periodo | n días | n est. | Td sesgo | Td RMSE | Td r | Anom. sesgo | Anom. RMSE | Anom. r |
|---|---|---|---|---|---|---|---|---|---|
| PISCO v1.1 | 2009-2016 | 31.326 | 13 | +1,42 | 3,06 | 0,946 | +0,02 | 1,33 | 0,625 |
| ERA5 | 2009-2016 | 31.326 | 13 | -0,39 | 1,91 | 0,973 | +0,03 | 1,28 | 0,696 |
| ERA5-Land | 2009-2016 | 31.326 | 13 | +0,06 | 1,85 | 0,973 | +0,02 | 1,21 | 0,705 |
| `palacios` | 2017-2020 | 14.666 | 12 | +1,38 | 2,88 | 0,949 | +0,18 | 1,68 | 0,502 |
| `timesfm` | 2017-2020 | 14.666 | 12 | +1,48 | 2,89 | 0,951 | +0,29 | 1,63 | 0,556 |
| ERA5 | 2017-2020 | 14.666 | 12 | -0,50 | 1,94 | 0,973 | +0,11 | 1,57 | 0,615 |
| ERA5-Land | 2017-2020 | 14.666 | 12 | +0,14 | 1,65 | 0,977 | +0,24 | 1,51 | 0,628 |

Diferencias de RMSE agrupado con IC 95 % por estaciones (`a4_delta_rmse_bootstrap.csv`):

| Comparación | Periodo | Td | Anomalía |
|---|---|---|---|
| `timesfm` − `palacios` | 2017-2020 | +0,010 [-0,025; +0,057] | -0,046 [-0,073; -0,019] |
| ERA5-Land − `palacios` | 2017-2020 | -1,22 [-1,99; -0,37] | -0,17 [-0,32; -0,04] |
| ERA5-Land − `timesfm` | 2017-2020 | -1,23 [-2,00; -0,37] | -0,12 [-0,28; +0,01] |
| ERA5-Land − PISCO | 2009-2016 | -1,21 [-1,90; -0,29] | -0,12 [-0,29; -0,02] |

### Por año

RMSE de anomalía frente a estación (`a4_por_anio.csv`):

| Año | PISCO | `palacios` | `timesfm` | ERA5 | ERA5-Land | n días |
|---|---|---|---|---|---|---|
| 2009 | 1,36 | | | 1,29 | 1,25 | 3.412 |
| 2010 | 1,38 | | | 1,48 | 1,36 | 3.572 |
| 2011 | 1,26 | | | 1,21 | 1,16 | 3.586 |
| 2012 | 1,34 | | | 1,32 | 1,24 | 4.333 |
| 2013 | 1,50 | | | 1,31 | 1,21 | 3.953 |
| 2014 | 1,00 | | | 0,86 | 0,90 | 3.239 |
| 2015 | 1,29 | | | 1,28 | 1,19 | 4.319 |
| 2016 | 1,40 | | | 1,31 | 1,29 | 4.337 |
| 2017 | | 1,46 | 1,42 | 1,39 | 1,33 | 4.343 |
| 2018 | | 1,54 | 1,49 | 1,42 | 1,32 | 4.312 |
| 2019 | | 2,11 | 2,05 | 1,97 | 1,92 | 4.364 |
| 2020 | | 1,18 | 1,19 | 1,15 | 1,15 | 1.647 |

Sesgo de Td (fuente − estación) por año: PISCO entre +0,71 (2014) y +1,93 (2009); `palacios` +1,01, +1,30, +1,75, +1,56 y `timesfm` +1,10, +1,42, +1,84, +1,65 en 2017-2020. El RMSE de Td de los dos productos va de 1,89 a 3,16 según el año.

### Desacuerdo entre productos y ENSO

| Año | RMSE `timesfm` − `palacios` en celdas de estación | Ídem, nacional (`real_limpio`) | Sesgo `timesfm` − `palacios` (estaciones) | ONI medio (mín; máx) | Niño 1+2 medio (máx) |
|---|---|---|---|---|---|
| 2017 | 0,30 | 0,46 | +0,08 | -0,06 (-0,76; 0,35) | 0,03 (1,83) |
| 2018 | 0,34 | 0,43 | +0,08 | 0,14 (-0,71; 1,05) | -0,22 (0,84) |
| 2019 | 0,32 | 0,50 | +0,08 | 0,65 (0,20; 0,99) | 0,00 (0,80) |
| 2020 | 0,33 | 0,47 | +0,06 | -0,21 (-1,11; 0,71) | -0,42 (0,44) |

ONI de NOAA CPC (`oni.ascii.txt`, media de las 12 estaciones trimestrales del año) y Niño 1+2 de `sstoi.indices` (anomalía mensual). En 2017-2020 el ONI no pasa de ±1,1 y no hay un evento El Niño fuerte como el de 2015-2016; el Niño costero de 2017 aparece solo en Niño 1+2 (máximo 1,83). Con cuatro años, el desacuerdo entre productos (0,30-0,34 en las celdas de estación, 0,43-0,50 nacional) no muestra relación con los índices; no se puede sacar una conclusión sobre ENSO con esta muestra.

## Lectura

1. **El Td de PISCO se aparta mucho de las estaciones en valor absoluto, y los dos productos heredan ese desfase.** En 2009-2016 PISCO tiene sesgo +1,42 °C y RMSE 3,06 °C frente a las 13 estaciones; en Arequipa el sesgo es +5,9 °C, en Cusco +4,0 °C y en Andahuaylas +4,2 °C, con diferencias de elevación estación-celda de 22 a 29 m en los dos primeros. ERA5-Land tiene sesgo +0,06 °C y RMSE 1,85 °C en los mismos días. Los productos 2017-2020 repiten el patrón por estación (Arequipa +4,95 y +5,03; Cusco +4,10 y +4,19), como cabe esperar de modelos entrenados para reproducir PISCO. El RMSE de Td no sirve para comparar los productos con PISCO porque lo domina el desfase de unas pocas estaciones.

2. **En anomalías, los productos quedan frente a ERA5-Land en una proporción parecida a la de PISCO en 2009-2016.** RMSE de anomalía: PISCO 1,33 frente a ERA5-Land 1,21 en 2009-2016 (cociente 1,10); `palacios` 1,68 y `timesfm` 1,63 frente a ERA5-Land 1,51 en 2017-2020 (cocientes 1,11 y 1,08). El aumento de error de un periodo al otro (+0,30 °C en ERA5-Land, +0,29 en ERA5) aparece también en el reanálisis, así que se explica sobre todo por la climatología fuera de muestra y por cambios en las estaciones, no por los productos. La correlación de anomalías baja más en los productos (0,50-0,56 frente a 0,625 de PISCO) que en ERA5-Land (0,705 a 0,628).

3. **TimesFM y `tuned` no se distinguen en Td y TimesFM queda algo mejor en anomalías.** En Td la diferencia es +0,010 °C con IC [-0,025; +0,057]. En anomalías TimesFM tiene 0,046 °C menos de RMSE (IC [-0,073; -0,019]), en la misma dirección que el backtest contra PISCO (ΔRMSE pareado +0,074 a favor de TimesFM). La muestra es de 12 estaciones, así que el intervalo refleja sobre todo la variación entre esas estaciones.

4. **Un salto en la estación de Ayacucho domina el año 2019.** En Ayacucho (SPHO) el sesgo de anomalía de 2019 es +4,3 °C para `palacios`, `timesfm`, ERA5 y ERA5-Land a la vez (+2,3 a +2,7 en 2020), lo que apunta a un cambio en la estación (instrumento o procesamiento) y no a los productos. Si se deja fuera Ayacucho (`a4_dejar_una_estacion_fuera.csv`), el RMSE de anomalía 2017-2020 baja a 1,44 (`palacios`), 1,40 (`timesfm`) y 1,25 (ERA5-Land), y el de PISCO 2009-2016 a 1,31 (ERA5-Land 1,18). Sin Arequipa, que es la estación con más ruido, baja a 1,47 / 1,42 / 1,38 y 1,08 (PISCO). El cociente frente a ERA5-Land queda entre 1,06 y 1,17 para PISCO y entre 1,03 y 1,15 para los productos en todas las exclusiones de una estación.

5. **Sensibilidad al criterio diario.** Con al menos 2 bloques de 6 h (`a4_por_periodo_h4b2.csv`, 23-26 estaciones, incluye aeropuertos sin datos nocturnos) el RMSE de anomalía queda en 1,45 (PISCO 2009-2016), 1,98 (`palacios`), 1,94 (`timesfm`) y 1,69 (ERA5-Land 2017-2020); TimesFM − `palacios` en anomalías es -0,045 [-0,073; -0,009] y en Td -0,001 [-0,031; +0,036]. El orden de las fuentes no cambia; el cociente frente a ERA5-Land sube a 1,15-1,18 para los productos (PISCO en 2009-2016: 1,09). Con este criterio cambian a la vez el conjunto de estaciones y la definición de la media diaria, así que la diferencia no se atribuye a una causa concreta.

6. **La validación contra el Td grillado no mide lo mismo que este contraste.** En el backtest contra PISCO el RMSE de los productos es ≈1,15-1,23 °C en Td; frente a estaciones de aeropuerto, el RMSE de PISCO mismo es 3,06 °C en Td y 1,33 °C en anomalías. La primera cifra describe cuánto reproducen los productos el Td grillado, no cuánto se acercan al Td atmosférico.

## Chequeo de la Tmin regridada 2017-2020

Panel nacional (17.027 celdas), `future_tmin_by_bucket` (2017-2020) frente a TMIN de `bucketed_training_data` (2013-2016). Las dos son PISCOt v1.2 en la grilla de 2,8 M celdas; no hay años solapados, así que no hay correlación día a día posible.

- Distribución global (`a4_tmin_global.csv`): media 17,31 frente a 17,28 °C, desviación 8,01 frente a 7,95; p05 -0,60 frente a -0,38, p50 21,06 frente a 21,02, p95 23,94 frente a 23,92.
- Por mes (`a4_tmin_por_mes.csv`): las medias difieren entre -0,25 (enero) y +0,29 °C (setiembre); las diferencias de percentiles no pasan de 0,7 °C (p95 de enero, 24,41 frente a 23,75).
- Medias por celda y mes (`a4_tmin_celda_mes.csv`): r = 0,9991 entre periodos; r = 0,978 del ciclo anual por celda (sin la media de la celda); diferencia media -0,026 °C, desviación 0,34, p05/p95 ±0,56; 1,3 % de los pares celda-mes difieren en más de 1 °C.
- Costura dic/ene (`a4_tmin_costura.csv`): el salto medio ene-2017 − dic-2016 es -0,002 °C (otros años, de -0,33 a +1,02). Su dispersión entre celdas es mayor (desviación 1,33 frente a 0,66-0,90 en los demás años). Puede deberse a una diferencia celda a celda entre las dos corridas de regrid o al clima de enero de 2017 (inicio del Niño costero); con estos datos no se pueden separar.
- Textura espacial (`a4_tmin_rugosidad.csv`, diferencia de Tmin media anual entre celdas vecinas de una fila, 16.730 pares): desviación de 0,40-0,45 °C en todos los años de 2013 a 2020, sin cambio en 2017. No hay señal de un método de regrid distinto.

No se encontró un cambio de nivel ni de distribución en la Tmin de entrada al pasar a 2017-2020; la mayor dispersión del salto de enero de 2017 queda como punto abierto.

## ERA5 y ERA5-Land

Se hizo el contraste en puntos (coordenada de cada estación) con ERA5 a 0,25° y ERA5-Land a 0,1°, vía la API pública de Open-Meteo, sin credenciales (datos CC BY 4.0; ERA5 bajo la licencia de Copernicus; uso no comercial). No se hizo un contraste grillado de los productos contra ERA5 en todo el Perú. Para eso haría falta una de estas opciones: una clave del Copernicus Climate Data Store (`~/.cdsapirc`) para descargar `reanalysis-era5-land` con recorte al Perú, una cuenta de servicio de Google Earth Engine (`ECMWF/ERA5_LAND/DAILY_AGGR`), o leer el bucket público `s3://nsf-ncar-era5` sin credenciales, lo que exige instalar `s3fs`/`h5netcdf` y leer por rangos archivos mensuales globales horarios (decenas de GB si se descargan enteros).

ERA5 no es una referencia independiente de estas estaciones: su análisis de superficie asimila T y humedad a 2 m de estaciones SYNOP, que incluyen estos aeropuertos, y ERA5-Land se fuerza con ERA5. Su mejor puntaje es en parte consecuencia de esa asimilación; se usa aquí como escala de lo que logra un producto que sí ve estas estaciones, no como verdad.

## Limitaciones

- **Independencia frente a PISCO.** Las 13 estaciones son aeropuertos (CORPAC/FAP). PISCO Td v1.1 usa 182 estaciones de SENAMHI, y no hay una lista pública que permita comprobar si alguna coincide con estas o está en el mismo sitio. Los desfases grandes de PISCO en Arequipa, Cusco y Andahuaylas sugieren que esas estaciones de aeropuerto no se usaron tal cual, pero no lo prueban. Si alguna estación entró en PISCO, el error de PISCO en 2009-2016 está subestimado en ella; el de los productos en 2017-2020 no, porque en ese periodo no hay Td de PISCO.
- **Insumos compartidos.** Este contraste mide error frente a Td atmosférico en puntos, pero no elimina la dependencia Tmin-Td por LST de MODIS: el error compartido sigue presente en el entrenamiento de los dos productos.
- **Muestra pequeña y sesgada.** 12-13 estaciones, todas en aeropuertos: 6 en la costa (Piura, Chiclayo, Trujillo, Lima, Pisco, Tacna), 5 en los Andes (Cajamarca, Ayacucho, Cusco, Arequipa y Andahuaylas, esta solo en 2009-2016) y 2 en la Amazonía (Iquitos, Pucallpa). Ninguna está en el altiplano con el criterio principal. Los intervalos por bootstrap de estaciones son anchos.
- **Punto frente a celda.** Una estación de aeropuerto representa un punto; la celda PISCO es de ≈1 km y el Td grillado es suavizado. Parte del error de todas las fuentes es representatividad.
- **Calidad de estación.** Se aplicó solo control de calidad básico. Ayacucho 2019-2020 tiene un salto aparente que afecta a todas las fuentes; no se corrigió ni se excluyó en las tablas principales (se informa el efecto de dejarlo fuera). En 2020 la cobertura nocturna cae desde marzo.
- **Climatología de anomalías.** Ajustada en 2009-2016 con 8 años o menos según la estación; en 2009-2016 el contraste de anomalías está dentro de la muestra.

## Archivos

- Código: `experiments/a4_externo/{__init__,isd,download,grid,openmeteo,compare,tmin_check}.py`, `README.md`; prueba `tests/test_a4_isd.py`.
- Tablas: `a4_estaciones.csv`, `a4_estaciones_excluidas.csv`, `a4_dias_por_estacion_anio.csv`, `a4_por_periodo.csv`, `a4_por_anio.csv`, `a4_por_estacion.csv`, `a4_por_estacion_anio_anom.csv`, `a4_resumen_entre_estaciones.csv`, `a4_todas_las_parejas_por_periodo.csv`, `a4_delta_rmse_bootstrap.csv`, `a4_dejar_una_estacion_fuera.csv`, `a4_desacuerdo_oni.csv`, `a4_indices_2009_2020.csv`, `a4_tmin_*.csv`, `a4_config.json`; las mismas con sufijo `_h4b2` para la sensibilidad.
- Datos descargados (fuera del repositorio): `/home/cvelasquez/tdew_timesfm/a4/` (`isd_raw/`, `isd_meta/`, `indices/`, `openmeteo_raw/`, pares estación-fuente en `pares_estacion_fuente*.parquet`).

Este análisis se preparó con asistencia de IA generativa (Claude) y debe revisarse con Palacios y SENAMHI antes de usarse en el paper.
