# Arquitectura medallón de `pipeline/`

Este documento describe qué hace cada capa del medallón (bronze, silver, gold), qué recibe y qué produce, cómo se guardan los datos y qué significa cada columna. Los números de filas, archivos y tamaños se midieron sobre los datos en disco el 12 de octubre de 2026. Las reglas de partición temporal vienen de `docs/protocol/week1_manifest.yaml`.

El medallón alimenta los experimentos de aprendizaje profundo y los baselines (`experiments/`). No es el almacén que usa el modelo de producción de `tdew_estimation/` ni los experimentos de TimesFM, que leen otro conjunto de buckets (ver la última sección).

## Resumen

| Capa | Módulo | Entrada | Salida | Tamaño en disco |
|---|---|---|---|---|
| bronze | `pipeline.bronze` | Archivos NetCDF originales de PISCO | `Data/bronze/_inventory.csv` (los NetCDF quedan intactos) | 133 GB |
| silver | `pipeline.silver` | NetCDF de bronze | Tablas parquet por celda (`ID`) | 82 GB |
| gold | `pipeline.gold` | Tablas de silver | `Data/gold/model_input`: una fila por celda y día | 365 GB (incluye todas las tablas derivadas) |
| gold | `pipeline.features` | `model_input` | `model_features`: años 2002–2016, etiqueta `split`, codificación de `doy` | |
| gold | `pipeline.normalize` | `model_features` | `model_features_norm` y `normalization_stats.json` | |
| gold | `pipeline.sequences` | `model_features_norm` | `sequence_index/L={14,31,60}` | |
| gold | `pipeline.baseline_features` | `model_features_norm` y `sequence_index/L=31` | `baseline_dataset` | |
| qc | `pipeline.qc` | Tablas diarias de silver | `Data/qc/qc_table.csv` | |

Las etapas están declaradas en `dvc.yaml` y también envueltas en `pipeline/zenml_pipeline.py`, que solo llama a la función `run()` de cada módulo y pasa rutas de directorio, sin copiar datos al almacén de artefactos de ZenML.

## Cómo se guarda la información

`Data/bronze`, `Data/silver` y `Data/gold` son enlaces simbólicos a `/media/ppalacios/Data1/henry_simcast_peru/tdew_medallion/{bronze,silver,gold}`, un disco compartido cuyo dueño es otro usuario. DVC no puede gestionar rutas dentro de un directorio enlazado, por lo que todas las salidas en `dvc.yaml` llevan `cache: false` y `persist: true`: DVC registra hashes para detectar etapas desactualizadas, pero no copia ni sube los datos. `Data/qc` es un directorio normal del repositorio.

Todo el contenido tabular es parquet. Las tablas diarias de gold se particionan al estilo Hive por `id_bucket = ID % 64`, con carpetas sin ceros a la izquierda (`id_bucket=0`, `id_bucket=63`) y un archivo `part.parquet` por bucket. Cada bucket contiene todas las fechas de unas 6 800 celdas, así que las operaciones por celda (climatología, rezagos, rachas) se resuelven leyendo un bucket a la vez. Los 64 buckets son el valor por defecto de `--num-buckets` y es el que existe en disco.

Todas las etapas son incrementales: omiten archivos que ya existen salvo que se pase `--overwrite`.

## Rejilla e identificador de celda

Todos los rasters comparten la rejilla de PISCO: 1 982 latitudes por 1 422 longitudes a 0,01°, es decir 2 818 404 celdas. `ID` es el índice de la celda en orden fila-mayor (latitud como eje externo, longitud como eje interno), entero de 64 bits. Es la llave de unión de todas las tablas.

Las tablas diarias de silver y gold no cubren todo el país. Se filtran a 436 519 celdas de cuatro sitios, definidos por departamento completo (el centro de la celda cae dentro del polígono departamental):

| Sitio | Archivo de IDs en `Data/silver/department_grid_ids/` | Celdas |
|---|---|---|
| Lima | `lima.csv` | 29 079 |
| Cusco | `cusco.csv` | 60 041 |
| Loreto (Iquitos) | `iquitos_loreto.csv` | 305 564 |
| San Martín (Tarapoto) | `tarapoto_san_martin.csv` | 41 835 |

Cada CSV tiene las columnas `ID`, `latitude` y `longitude`. Se generan con una unión espacial contra `peru_departamental_simple.geojson` (fuente comunitaria, no oficial; ver `docs/CITY_GRID_IDS.md`). Las celdas cercanas al borde departamental podrían estar mal clasificadas por pocos kilómetros.

## Bronze

**Entrada.** Los archivos NetCDF originales, que en esta máquina ya llegaron extraídos (los `.nc` de tmin y tmax enlazan a `_raw/v1_2`).

| Contenido | Ruta bajo `Data/bronze/` | Cobertura |
|---|---|---|
| Tmin diaria | `tmin_daily_{año}.nc` | 1981–2020, un archivo por año |
| Tmax diaria | `tmax_daily_{año}.nc` | 1981–2020, un archivo por año |
| Td diaria | `td_daily_{año}/td_daily_{año}_{mes}.nc` | 2002–2016, un archivo por mes |
| Covariables estáticas | `spatial_covariables/{DEM,TDI,X,Y}.nc` | Rasters 2D (latitud, longitud) |
| Normales mensuales de temperatura de superficie | `spatial_covariables/{LST_DAY,LST_NIGHT}.nc` | 12 meses (dimensión `z`) |

**Transformaciones.** Ninguna sobre los datos. El módulo descomprime cualquier `.zip` que encuentre en una carpeta hermana con el nombre del archivo y escribe un inventario.

**Salida.** `Data/bronze/_inventory.csv`, con una fila por archivo y las columnas `relative_path`, `suffix`, `size_bytes` y `modified`.

## Silver

**Entrada.** Los NetCDF de bronze y `Data/silver/department_grid_ids/*.csv`.

**Transformaciones.**
- La rejilla se aplana a filas, con el eje de tiempo como bloque externo.
- Cada raster diario se lee mes a mes y se escribe un parquet por variable, año y mes, para acotar la memoria.
- Las tablas diarias se filtran a los 436 519 `ID` de los cuatro sitios (`--departments`). El raster se lee completo en cada mes, y solo las filas escritas se restringen. `grid_index`, `static_covariates` y `lst_normals` cubren siempre el país completo.
- Los valores se convierten a `float32` y se agrega `doy` (día del año) calculado desde la fecha.
- No se convierten unidades ni se rellenan vacíos. La tabla de QC cuenta filas por celda y día, no valores nulos. Sobre valores nulos, en el bucket 0 de `model_features` no hay nulos ni NaN (comprobación puntual, no un control del pipeline).

**Salida.**

| Archivo | Filas | Columnas |
|---|---|---|
| `grid_index.parquet` | 2 818 404 | `ID`, `latitude`, `longitude` |
| `static_covariates.parquet` | 2 818 404 | `ID`, `DEM`, `TDI`, `X`, `Y` |
| `lst_normals.parquet` | 33 820 848 (2 818 404 × 12 meses) | `ID`, `month`, `LST_DAY`, `LST_NIGHT` |
| `tmin/tmin_daily_{año}_{mes}.parquet` | 480 archivos, 1981–2020 | `ID`, `date`, `doy`, `value` |
| `tmax/tmax_daily_{año}_{mes}.parquet` | 480 archivos, 1981–2020 | `ID`, `date`, `doy`, `value` |
| `td/td_daily_{año}_{mes}.parquet` | 180 archivos, 2002–2016 | `ID`, `date`, `doy`, `value` |

Un mes de 31 días tiene 13 532 089 filas, que equivalen a 436 519 celdas por 31 días.

## Control de calidad (`pipeline.qc`)

Se ejecuta directamente sobre las tablas diarias de silver, restringido a 2002-01-01 a 2016-12-31 (5 479 días). Por cada combinación de sitio y variable calcula los pares celda–día esperados y observados, los duplicados y los días calendario sin ninguna fila. Agrega una fila `alignment(tmin,tmax,td)` por sitio con los días cubiertos por alguna serie pero no por las tres.

Columnas de `Data/qc/qc_table.csv`: `site`, `variable`, `n_cells`, `expected_days`, `expected_pairs`, `observed_pairs`, `missing_pairs`, `missing_pct`, `total_rows`, `duplicate_rows`, `distinct_days_present`, `missing_calendar_days`.

En la ejecución actual, los cuatro sitios y las tres variables tienen 0 pares faltantes, 0 duplicados y 5 479 días presentes. Las tres series están alineadas en todos los días.

## Gold

### `model_input` (`pipeline.gold`)

**Entrada.** Las tablas diarias, `static_covariates` y `lst_normals` de silver.

**Transformaciones.**
1. Cada tabla de silver se reparte por `id_bucket` en `Data/gold/_bucketed/{tmin,tmax,td,static,lst}`.
2. Dentro de cada bucket, para cada variable (`TMIN`, `TMAX`, `TD`) se calcula la climatología `{var}_clim` como la media por (`ID`, `doy`) usando únicamente los años 2002–2012, el periodo de entrenamiento congelado en el manifiesto. Ese valor se aplica por unión a todas las filas de la variable, incluidas las de validación y prueba, de modo que ningún año posterior entra en la línea base. `TMIN_clim` y `TMAX_clim` quedan definidas para 1981–2020. `TD_clim` solo existe en 2002–2016, porque la tabla de Td no tiene otras fechas.
3. La anomalía es `{var}_anom = {var} − {var}_clim`.
4. Las tres variables se unen por (`ID`, `date`, `doy`), tomando `TMIN` como tabla base (unión por la izquierda). Se agregan `month`, las covariables estáticas por `ID` y las normales de LST por (`ID`, `month`).
5. Cada bucket se ordena por (`ID`, `date`).

La climatología no se suaviza. El día 366 se promedia solo con 2004, 2008 y 2012, los únicos años bisiestos del periodo de entrenamiento.

**Salida.** `Data/gold/model_input/id_bucket=N/part.parquet`: 6 377 542 590 filas, que equivalen a 436 519 celdas por los 14 610 días de 1981-01-01 a 2020-12-31. `TD`, `TD_clim` y `TD_anom` son nulos en el 62,5 % de las filas, que son los días fuera de 2002–2016 donde no existe Td.

### `model_features` (`pipeline.features`)

**Entrada.** `model_input`.

**Transformaciones.**
- Se conservan solo las fechas entre 2002-01-01 y 2016-12-31, el único rango donde existen las tres variables.
- Se asigna `split` por año calendario: `train` 2002–2012, `validation` 2013–2014, `test` 2015–2016.
- Se agrega la codificación circular del día del año, `sin_doy = sin(2π·doy/366)` y `cos_doy = cos(2π·doy/366)`. No se agregan columnas de rezago: los modelos secuenciales obtienen la historia de la propia ventana.

**Salida.** `Data/gold/model_features/id_bucket=N/part.parquet`: 2 391 687 601 filas (436 519 × 5 479). Tiene las mismas columnas que `model_input` más `split`, `sin_doy` y `cos_doy`.

### `model_features_norm` (`pipeline.normalize`)

**Entrada.** `model_features`.

**Transformaciones.**
- En una primera pasada por buckets se acumulan suma y suma de cuadrados de las filas con `split == "train"` para obtener media y desviación estándar de cada columna continua. Cada columna usa 1 753 933 342 filas de entrenamiento (436 519 celdas × 4 018 días).
- Las estadísticas se guardan en `Data/gold/normalization_stats.json` (`mean`, `std`, `n_train_rows` por columna).
- En una segunda pasada se agrega `{col}_norm = (col − mean) / std` a todas las filas, de cualquier `split`. Si `std` es 0, la columna normalizada vale 0.
- `sin_doy`, `cos_doy`, `doy` y `month` no se normalizan.

**Salida.** `Data/gold/model_features_norm/id_bucket=N/part.parquet`: las columnas de `model_features` más 12 columnas `_norm`: `TMIN`, `TMAX`, `TD`, `TMIN_anom`, `TMAX_anom`, `TD_anom`, `DEM`, `TDI`, `X`, `Y`, `LST_DAY` y `LST_NIGHT`, cada una con el sufijo `_norm`.

Estadísticas de entrenamiento guardadas:

| Columna | Media | Desviación estándar |
|---|---|---|
| `TMIN` | 18,47 | 6,77 |
| `TMAX` | 28,63 | 5,27 |
| `TD` | 20,50 | 7,19 |
| `TMIN_anom` | ≈ 0 | 0,96 |
| `TMAX_anom` | ≈ 0 | 1,56 |
| `TD_anom` | ≈ 0 | 1,11 |
| `DEM` | 799,72 | 1 274,55 |
| `TDI` | 2,32 | 1,06 |
| `X` | −74,48 | 1,94 |
| `Y` | −6,16 | 3,76 |
| `LST_DAY` | 26,57 | 4,37 |
| `LST_NIGHT` | 18,48 | 6,90 |

### `sequence_index` (`pipeline.sequences`)

**Entrada.** `ID`, `date` y `split` de `model_features_norm`.

**Transformaciones.** Por cada `ID` se buscan las rachas máximas de días consecutivos con el mismo `split`. Una racha se corta por un hueco en el calendario, un cambio de `ID` o un cambio de `split`; por ejemplo, 2012-12-31 y 2013-01-01 son días contiguos pero pasan de `train` a `validation`. Para una longitud de contexto `L`, el modelo predice `Td(t+1)` desde la ventana `X_{t−L+1:t}`. Un día objetivo `t` es elegible si tiene al menos `L` días hasta `t` dentro de la racha y no es el último día de la racha, de modo que `t+1` queda dentro del mismo `split`. Cada racha de `N` días aporta `max(0, N − L)` objetivos elegibles.

Las ventanas no se materializan. Para `L = 60` multiplicarían por 60 una tabla de miles de millones de filas. El índice delimita las rachas y el cargador de datos corta `model_features_norm` al vuelo.

**Salida.** `Data/gold/sequence_index/L={14,31,60}/id_bucket=N/part.parquet`. Con `L = 31` hay 1 309 557 filas, tres rachas por celda (una por `split`).

| Columna | Significado |
|---|---|
| `ID` | Celda |
| `split` | `train`, `validation` o `test` |
| `run_start_date`, `run_end_date` | Primer y último día de la racha |
| `n_days` | Largo de la racha |
| `n_eligible_targets` | Cantidad de días objetivo elegibles (`max(0, n_days − L)`) |
| `first_eligible_target_date` | `run_start_date + (L − 1)` días |
| `last_eligible_target_date` | `run_end_date − 1` día |

La longitud `L = 31` reemplazó a 30 en el manifiesto el 17 de septiembre de 2026: con 30, la ventana llega hasta `t−29` y no alcanza el rezago de 30 días del baseline no secuencial.

### `baseline_dataset` (`pipeline.baseline_features`)

**Entrada.** `model_features_norm` y `sequence_index/L=31`.

**Transformaciones.** Por cada `ID`, con desplazamientos hacia atrás únicamente para las entradas y hacia adelante para el objetivo:
- Rezagos de anomalía de Td: `TD_anom_lag1`, `lag2`, `lag3`, `lag7` y `lag30` toman `TD_anom` en `t`, `t−1`, `t−2`, `t−6` y `t−29`. El número del nombre es la distancia en días al objetivo `t+1`.
- Rezagos de anomalía de Tmin: `TMIN_anom_lag0` y `TMIN_anom_lag1` toman `TMIN_anom` en `t` y `t−1`.
- Objetivos: `TD_anom_target` y `TD_target` son `TD_anom` y `TD` en `t+1`.
- Valores del día objetivo: `TD_clim_target`, `sin_doy_target`, `cos_doy_target`, `LST_DAY_target` y `LST_NIGHT_target` corresponden a `t+1`.
- Se conservan solo las filas cuyo `t+1` cae dentro de un rango elegible de `sequence_index/L=31`.

Ninguna entrada proviene de `t+1` o posterior. Esto difiere del modelo de producción, que usa la Tmin del mismo día del objetivo, algo que la regla de fuga del manifiesto no admite.

**Salida.** `Data/gold/baseline_dataset/id_bucket=N/part.parquet`: 2 351 091 334 filas. Son 93 filas menos por celda que `model_features`: los primeros 30 días de cada `split` no tienen contexto suficiente y el último día de cada `split` no tiene objetivo, es decir 31 días en cada uno de los 3 `split`. Columnas: `ID`, `date` (el día `t`), `split`, las siete columnas de rezago, los dos objetivos, los cinco valores del día objetivo y `DEM`, `TDI`, `X`, `Y`.

## Diccionario de columnas

Las unidades de Td, Tmin, Tmax y LST son °C según el rango de los valores. Los NetCDF no declaran unidades.

| Columna | Significado | Aparece en |
|---|---|---|
| `ID` | Índice de celda en la rejilla de 1 982 × 1 422, orden fila-mayor | todas |
| `latitude`, `longitude` | Coordenadas del centro de la celda, en grados (WGS84) | `grid_index`, CSV de departamentos |
| `date` | Día calendario | tablas diarias |
| `doy` | Día del año, de 1 a 366 | tablas diarias |
| `month` | Mes, de 1 a 12 | `lst_normals`, gold |
| `value` | Valor diario de la variable de la carpeta (`tmin`, `tmax` o `td`) | tablas diarias de silver |
| `TMIN`, `TMAX` | Temperatura mínima y máxima diaria (PISCOt v1.2) | gold |
| `TD` | Temperatura de punto de rocío diaria (PISCO v1.1), solo 2002–2016 | gold |
| `TMIN_clim`, `TMAX_clim`, `TD_clim` | Media por celda y día del año sobre 2002–2012 | gold |
| `TMIN_anom`, `TMAX_anom`, `TD_anom` | Valor menos su climatología | gold |
| `DEM` | Elevación en metros (GMTED2010, 1 km). Rango de la rejilla: 0 a 6 478 | `static_covariates`, gold |
| `TDI` | Índice de disección topográfica, adimensional, de 0 a 5. La definición exacta del producto original no está documentada en el repositorio | `static_covariates`, gold |
| `X`, `Y` | Longitud y latitud de la celda, en grados, como covariable numérica | `static_covariates`, gold |
| `LST_DAY`, `LST_NIGHT` | Normal mensual de temperatura de superficie terrestre, diurna y nocturna. Se une por `ID` y `month`, de modo que es igual para todos los años | `lst_normals`, gold |
| `split` | `train` (2002–2012), `validation` (2013–2014) o `test` (2015–2016) | desde `model_features` |
| `sin_doy`, `cos_doy` | Codificación circular del día del año con periodo 366 | desde `model_features` |
| `{col}_norm` | Valor estandarizado con la media y la desviación de entrenamiento | `model_features_norm` |

## Ejecución

```bash
uv run python -m pipeline.bronze
uv run python -m pipeline.silver --departments lima,cusco,iquitos_loreto,tarapoto_san_martin
uv run python -m pipeline.gold
uv run python -m pipeline.features
uv run python -m pipeline.normalize
uv run python -m pipeline.sequences
uv run python -m pipeline.baseline_features
uv run python -m pipeline.qc
uv run python -m pipeline.zenml_pipeline   # todas las etapas con ZenML
```

El filtro por departamentos de silver requiere que existan los CSV de `Data/silver/department_grid_ids/`, que a su vez salen de `grid_index.parquet`. En una máquina nueva se corre primero `pipeline.silver --skip-daily`, se generan los CSV con el fragmento de `docs/CITY_GRID_IDS.md` y luego se corre la etapa completa. Los datos de `Data/` no se editan a mano: si cambia una etapa, se vuelve a correr su etapa de DVC.

## Diferencias con el almacén de producción

El modelo de producción y los experimentos de TimesFM leen otro conjunto de datos, en `/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/`:

| | Medallón (`Data/`) | Producción (`results_tuning/`) |
|---|---|---|
| Celdas | 436 519 en tablas diarias (4 sitios) | 2 818 404 por archivo, de las cuales 2 178 827 tienen datos (las otras 639 577 tienen `TD` y `TMIN` nulos) |
| Buckets | 64 (`id_bucket=N`, sin ceros) | 8 192 (`id_bucket=NNNN`, 4 dígitos) |
| Historia de Td | 2002–2016 (bronze no trae Td anterior) | Un archivo por año, 1981–2016 (`train_{año}.parquet`), con `ID`, `FECHA`, `TD`, `TMIN`, `doy`. En 2002–2016 los valores de `TD` y `TMIN` coinciden con los del medallón |
| Climatología | Media 2002–2012 por celda y día del año | Media 1981–2016 por celda y día del año (verificado en una celda, `climatology_by_bucket/`) |

Esta tabla resume lo observado en los esquemas y en una celda de muestra. No se leyó el código de `tdew_estimation` para la climatología. Las celdas sin datos de producción también tienen `DEM` y `TDI` nulos en `static_covariates`; las 436 519 de los cuatro sitios no tienen nulos.
