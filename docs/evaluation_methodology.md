# Metodología de evaluación (régimen de backtest de `HPC_code_tunning`)

> Objetivo de este documento: describir **el régimen exacto** bajo el cual se evalúan el
> modelo de producción y los baselines en este proyecto, para que un modelo nuevo pueda
> evaluarse bajo el **mismo protocolo** y sus métricas sean directamente comparables con
> las que produce (o vuelva a producir) `HPC_code_tunning/backtest.py` +
> `effect_sizes.py`.
>
> Fuente: `HPC_code_tunning/backtest.py`, `effect_sizes.py`, `selection.py`, `README.md`
> (secciones "Two runs, two year-windows" y "Step 2 — validate the method first").

## 1. Regla de oro: cuándo se separan años y cuándo no

Hay **dos trabajos distintos** que usan el mismo pipeline (zonas → seleccionar receta →
entrenar coeficientes → pronóstico autoregresivo), pero con ventanas de años opuestas:

- **Job 1 — VALIDAR** (esto es lo que produce los números de baseline/comparación):
  se **oculta deliberadamente** un bloque de años recientes, se selecciona y entrena
  **solo** con los años anteriores, se predice el bloque oculto de forma autoregresiva, y
  se califica contra el TD real que se escondió.
- **Job 2 — PRODUCIR** (el entregable real 2017–2020): usa **todos** los años etiquetados
  (1981–2016) porque no hay nada que ocultar (2017-2020 no tiene TD real).

**Un modelo nuevo que quiera ser comparable debe replicar el régimen de Job 1**, no el de
Job 2. Nunca debe entrenar (ni seleccionar hiperparámetros/recetas) usando años que estén
dentro de la ventana que luego va a predecir.

## 2. Splits temporales (holdouts)

Definidos en `backtest.py::SPLITS`. El entrenamiento **siempre** empieza en 1981:

| split | train hasta | holdout (predicho) | horizonte |
|---|---|---|---|
| `ll1` | 2015 | 2016 | 1 año |
| `ll2` | 2014 | 2015–2016 | 2 años |
| `ll4` | 2012 | 2013–2016 | 4 años (el "headline") |

`ll4` es la comparación principal (simula el gap real de 4 años 2017–2020). `ll1`/`ll2`
sirven para construir la **curva de degradación por horizonte** (skill vs. longitud del
holdout).

## 3. Qué NO debe ver el entrenamiento (anti-leakage)

- **Climatología train-only.** La climatología (`TD_clim`, `TMIN_clim` por `(ID, doy)`) se
  recalcula usando **solo los años de train** de cada split — nunca se usa la climatología
  "global" 1981–2016 para evaluar un split que oculta años. (`train_only_climatology` en
  `backtest.py`).
- **La receta/selección de features también debe ser train-only**, no solo el ajuste de
  coeficientes. Si el modelo elige hiperparámetros o features mirando datos posteriores al
  corte de train, el resultado es optimista (peeking). En este pipeline eso lo hace
  `select_backtest.py` (reselecciona la receta usando solo 1981–2012 para `ll4`).
- **Predicción estrictamente autoregresiva, sin observación real dentro del bloque
  oculto.** Durante el holdout no se usa ningún `TD` observado: los lags de `TD_anom`
  dentro del bloque se alimentan con las **predicciones propias del modelo del día
  anterior**, exactamente como ocurrirá en el gap real 2017–2020 (`forecast_bucket_zoned`,
  vía `_bucket_split` en `backtest.py`). Los lags de `TMIN_anom` sí usan Tmin observado real,
  porque Tmin existe en todo el rango.

## 4. Muestra espacial usada para el backtest

No se corre sobre el grid completo (2.8M celdas) por costo — se usa un subconjunto de
**buckets completos**: `id_bucket = ID % 8192`, y como los IDs son densos en orden
row-major, cada bucket es por sí solo una **rejilla nacional representativa** que toca las
41 zonas climáticas SENAMHI. Por eso leer un puñado de buckets completos (`--n-buckets`,
default 64 en `backtest.py`, 16 en la re-selección de `select_backtest.py`) es una muestra
barata y representativa, en vez de escanear las 8192 shards. Selección aleatoria
determinística vía `numpy.random.default_rng(seed)` (`choose_buckets`).

## 5. Los 4 métodos evaluados (la "escalera" de baselines)

Todos se puntúan sobre el **mismo** holdout, mismas celdas, mismos días:

1. **`climatology`** — media histórica por `(ID, doy)` sobre los años de train (sin ajuste
   a Tmin, el "gap-filler" ingenuo de hoy).
2. **`td_eq_tmin`** — `Td = Tmin`, sin transformar.
3. **`zone_ols`** — regresión lineal simple `Td ~ a + b·Tmin`, un intercepto/pendiente por
   **zona climática** (no por celda), ajustada con estadísticos suficientes acumulados
   (`n, Σx, Σy, Σx², Σxy`) sobre los años de train, resuelta en forma cerrada
   (`_OLSAccum.fit()`).
4. **`tuned`** (el modelo de producción/tuneado) — regresión local ponderada (WLS,
   ventana Tricube por día-del-año) sobre anomalías, con receta de features reajustada
   (refit) usando solo los años de train del split.

## 6. Métricas y su fórmula exacta

### 6.1 Métricas puntuales por método (`backtest.py::_metrics` / `_score_all`)

Para cada método, sobre todas las filas `(ID, día)` del holdout con observación finita:

- `n` — conteo de pares válidos.
- `rmse = sqrt(mean((pred - obs)^2))`
- `mae = mean(|pred - obs|)`
- `bias = mean(pred - obs)`
- `r` — correlación de Pearson `pred` vs `obs`.
- `skill_vs_clim = 1 - RMSE_método / RMSE_climatología` (positivo = mejor que climatología).

Se escriben a `metrics.csv` por split y `metrics_all.csv` combinado.

### 6.2 Inferencia estadística (`effect_sizes.py`)

Sobre `predictions.parquet` (una fila por `ID × día` con la observación y cada predicción):

- **Estadísticos suficientes por ubicación**: suma de error cuadrático (`se`) y conteo
  (`n`) por `ID`, por método (`_per_id_se`). RMSE pooled = `sqrt(Σse / Σn)`.
- **ΔRMSE con IC 95% por block-bootstrap de ubicación (ID).** Se remuestrea con reemplazo
  el conjunto de IDs (no días individuales) — así se respeta la autocorrelación temporal
  dentro de cada celda (su serie completa se mueve junta). `n_boot=1000` por defecto,
  percentiles 2.5/97.5 (`block_bootstrap_delta`).
- **Skill con el mismo bootstrap**: `skill = 1 - RMSE_tuned/RMSE_baseline`, para cada uno
  de los 3 baselines (`climatology`, `td_eq_tmin`, `zone_ols`).
- **Fracción de celdas donde el modelo gana** (`frac_cells_tuned_wins`): sobre el ΔRMSE
  **por-ubicación pareado** (`per_location_delta_rmse`, RMSE por ID, no pooled).
- **Cohen's d pareado**: `mean(Δ) / sd(Δ)` sobre las diferencias por-ubicación
  (`cohens_d_paired`).
- **Test de permutación por sign-flip** (`sign_flip_permutation`): bajo H0 (el modelo no es
  mejor que el baseline), el signo de la mejora en cada ubicación es igual de probable
  +/−; se generan `n_perm=5000` reordenamientos aleatorios de signo y se calcula el
  p-valor de una cola de que la mejora media observada no sea casualidad.

Salida: `effect_sizes.csv` por split, `effect_sizes_all.csv` combinado, más gráficos
(`rmse_ladder.png`, `delta_rmse_hist.png`, `bias_by_month.png`, `lead_time_curve.png`).

## 7. Checklist para que un modelo nuevo sea comparable

Para que las métricas de un modelo propio se puedan poner en la misma tabla/gráfico que
`climatology`, `td_eq_tmin`, `zone_ols` y `tuned`:

1. Usar los **mismos splits** (`ll1`, `ll2`, `ll4` — mismos años de train/holdout).
2. Entrenar (y seleccionar cualquier hiperparámetro) **solo con años ≤ train_end** del
   split; nunca tocar el bloque oculto durante fit/selección.
3. Recalcular la climatología (si el modelo la usa) **solo con años de train** del split,
   no con 1981–2016 completo.
4. Predecir el holdout de forma **autoregresiva y honesta**: si el modelo usa algún lag de
   TD, ese lag debe alimentarse con la predicción del propio modelo dentro del bloque
   oculto — nunca con el TD real oculto.
5. Producir un `predictions.parquet` (o equivalente) con una fila por `(ID, FECHA)` que
   incluya `TD_obs` y la predicción del modelo nuevo — idealmente en el mismo formato que
   `backtest.py` (columnas `ID, zone_id, FECHA, doy, TD_obs, <pred_col>`), para poder
   reusar `effect_sizes.py` sin modificarlo (basta añadir una entrada a `METHOD_COLS`).
6. Evaluar sobre la **misma muestra de buckets** (o, idealmente, sobre el grid completo si
   el costo lo permite) para que la comparación no esté sesgada por muestras distintas.
7. Reportar las mismas métricas: RMSE/MAE/bias/r/skill_vs_clim por método, más ΔRMSE con
   bootstrap CI, fracción de celdas donde gana, Cohen's d y el p-valor de permutación
   frente a cada baseline.

## 8. Nota sobre reproducibilidad de los números actuales

A la fecha de este documento, el repositorio **no contiene** un `metrics_all.csv` /
`effect_sizes_all.csv` ya generado (no hay carpeta de resultados de backtest bajo
control de versiones) — el código describe el *método*, pero los números concretos solo
existen si se vuelve a correr:

```bash
python -m HPC_code_tunning.select_backtest --base "$RES" --split ll4 ...
python -m HPC_code_tunning.backtest --base "$RES" --splits ll1,ll2,ll4 ...
python -m HPC_code_tunning.effect_sizes --backtest-root "$RES/tuning/backtest" --splits ll1,ll2,ll4
```

(ver `HPC_code_tunning/README.md`, sección "Step 2 — validate the method first", para los
flags completos). Cuando vuelvas a ejecutar el backtest, los resultados quedarán en
`$RES/tuning/backtest/<split>/{metrics.csv,predictions.parquet,effect_sizes.csv}`.
