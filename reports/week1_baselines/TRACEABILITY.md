# Trazabilidad — tdew-x46 baselines (Semana 1, Día 4)

Este documento responde: **de dónde salieron** `leaderboard.csv` y
`skill_vs_climatology.png`, **bajo qué protocolo/reglas** se calcularon, **qué
mide y qué hipótesis prueba cada uno de los 5 métodos**, **por qué no se
reusó tal cual el modelo de producción de Piero Palacios**, y **cómo
reproducir estos números exactamente**.

## 1. Protocolo (reglas congeladas, no negociables sin nuevo acuerdo)

Fuente única: [`docs/protocol/week1_manifest.yaml`](../../docs/protocol/week1_manifest.yaml)
(congelado 2026-09-15, bead `tdew-cra`).

- **Sitios**: 4 departamentos completos — Lima (Costa), Cusco (Sierra),
  Loreto/Iquitos (Selva), San Martín/Tarapoto (Selva) — seleccionados por
  polígono departamental real, no bounding box.
- **Periodo y splits** (estrictamente temporales, sin mezcla):
  train 2002–2012, validation 2013–2014, test 2015–2016.
- **Target**: `X_{<=t} -> Td(t+1)`. **Leakage constraint**: ninguna feature
  puede provenir de `t+1` o después — esto es lo que hace que el diseño de
  features de este baseline **difiera** del modelo de producción
  (`tdew_estimation/anomaly_train.py`, `docs/MODEL_INPUTS.md`), que sí usa
  TMIN del mismo día que el target.
- **Climatología**: `TD_clim`/`TMIN_clim` es el promedio por (celda, día del
  año) calculado SOLO con años de train (2002–2012, `pipeline/gold.py`),
  luego aplicado igual a train/validation/test. `TD_anom = TD - TD_clim` es
  lo que consumen los 5 baselines.
- **Normalización (z-score)**: capa aparte (`pipeline/normalize.py`), media/
  desviación estándar también calculadas solo con train, aplicadas a
  TMIN/TMAX/TD/sus anomalías/DEM/TDI/X/Y/LST_DAY/LST_NIGHT como columnas
  `{col}_norm`. Existe en `Data/gold/model_features_norm` pero **ninguno de
  los 5 baselines la usa** — las regresiones trabajan en unidades originales
  (anomalía cruda), no en z-score.

Decisiones específicas de esta implementación (acordadas con el usuario en
esta sesión, no están en el manifest):
- Timing de features **estricto por manifest** (no se replicó el diseño del
  modelo de producción que usa TMIN del mismo día).
- Escalera de **5 métodos** (persistence, climatology, dept_ols, dept_mlr,
  generalist_mlr) — el 5to (`generalist_mlr`) se agregó a pedido explícito
  del usuario, siguiendo una investigación (agente Opus, resumen abajo) sobre
  cómo GraphCast/Pangu-Weather/MetNet-3/AIFS resuelven la generalización
  espacial.

## 2. Linaje de datos (de dónde sale cada número)

```
Data/bronze (rasters PISCO, symlink a disco compartido)
  -> pipeline/silver.py       -> Data/silver/{tmin,tmax,td,static_covariates,lst_normals,department_grid_ids}
  -> pipeline/gold.py          -> Data/gold/model_input        (climatología train-only, TMIN/TMAX/TD + anomalías)
  -> pipeline/features.py      -> Data/gold/model_features     (+ split train/val/test, sin/cos DOY)
  -> pipeline/normalize.py     -> Data/gold/model_features_norm (+ z-score, stats train-only)
  -> pipeline/sequences.py     -> Data/gold/sequence_index/L=31 (elegibilidad: >=30 días contiguos + t+1 en mismo run/split)
  -> pipeline/baseline_features.py -> Data/gold/baseline_dataset (lags leak-safe + targets, reusa sequence_index/L=31)
  -> experiments/baselines/train_baselines.py -> reports/week1_baselines/leaderboard.csv
  -> experiments/baselines/plot_leaderboard.py -> reports/week1_baselines/skill_vs_climatology.png
```

Cada paso es una stage de `dvc.yaml` (`bronze, silver, gold, features,
normalize, sequences, qc, baseline_dataset`) y también un step de ZenML
(`pipeline/zenml_pipeline.py::medallion_pipeline`,
`experiments/baselines/zenml_pipeline.py::baselines_pipeline`) — correr por
ZenML es la forma soportada de reproducir esto (ver `CLAUDE.md`/pedido
explícito del usuario: "todos los pipelines" pasan por ZenML).

## 3. Los 5 métodos: qué miden, qué hipótesis prueban, fórmula y métricas

Convención de tiempo usada en toda esta sección: **`t`** = "hoy", el último
día con dato real observado. **`t+1`** = "mañana", el día que se predice
(el target). Todas las features de todos los métodos usan datos de fecha
`<= t` — nunca de `t+1` (regla `leakage_constraint` del manifest,
sección 1).

Los 5 métodos **miden exactamente lo mismo** en el sentido de evaluación:
predicen `Td(t+1)` y se puntúan con el mismo examen — mismas celdas, mismas
fechas de `validation`/`test`, y el mismo set de 5 métricas para los 5:

- `n` — cantidad de pares (predicción, observación) válidos usados.
- `rmse = sqrt(mean((pred − obs)²))` — error cuadrático medio, penaliza más
  los errores grandes.
- `mae = mean(|pred − obs|)` — error absoluto medio, más robusto a outliers
  que `rmse`.
- `bias = mean(pred − obs)` — error promedio con signo: `bias > 0` = el
  método sobreestima en promedio, `bias < 0` = subestima.
- `r` — correlación de Pearson entre predicción y observación.
- `skill_vs_clim = 1 − rmse_método / rmse_climatología` — cuánto mejora
  sobre el piso mínimo (ver la pregunta anterior en esta conversación para el
  detalle completo de esta métrica).

Lo que **sí** es distinto entre los 5 es la **hipótesis** que cada uno pone a
prueba sobre qué explica `Td(t+1)`, y por lo tanto su fórmula/proceso de
ajuste:

### 3.1 `climatology`
- **Qué mide**: si alcanza con saber la época del año (nada del clima
  reciente) para predecir mañana.
- **Hipótesis**: "solo importa la época del año".
- **Fórmula**: `pred = TD_clim(celda, día-del-año de t+1)` — el promedio
  histórico (2002–2012, train-only) de TD para esa celda en esa fecha del
  calendario.
- **Proceso de ajuste**: ninguno. Es un valor ya calculado en
  `pipeline/gold.py` (columna `TD_clim`), no se re-estima aquí.
- **Rol en la tabla**: es la referencia — su `skill_vs_clim` es `0.0` por
  definición en las 5 filas (se compara contra sí misma).

### 3.2 `persistence`
- **Qué mide**: si alcanza con la inercia día-a-día (sin mirar geografía,
  estación ni ninguna otra variable) para predecir mañana.
- **Hipótesis**: "mañana ≈ hoy" (la desviación de hoy respecto a su propio
  promedio histórico se mantiene mañana).
- **Fórmula**: `pred = TD_anom(t) + TD_clim(t+1)`, donde
  `TD_anom(t) = TD(t) − TD_clim(t)` es cuánto se desvió TD hoy de su
  climatología.
- **Proceso de ajuste**: ninguno, es una regla fija (no hay parámetros que
  estimar de los datos).

### 3.3 `dept_ols`
- **Qué mide**: si la temperatura mínima de hoy, sola, ya explica la
  anomalía de TD de mañana.
- **Hipótesis**: "solo importa `TMIN` de hoy".
- **Fórmula**: `TD_anom(t+1) ~ a + b · TMIN_anom(t)` — una regresión lineal
  simple (1 variable + intercepto), **una por departamento** (4 modelos:
  Lima, Cusco, Loreto/Iquitos, San Martín/Tarapoto).
- **Proceso de ajuste**: `tdew_estimation.metrics.OLSAccum` — acumula
  sufficient statistics (`Σx, Σy, Σx², Σxy, n`) leyendo el dataset por
  bloques (`id_bucket`) y resuelve `a, b` en forma cerrada al final, sin
  necesitar cargar el departamento completo en memoria. Solo con filas de
  `split=train`.

### 3.4 `dept_mlr`
- **Qué mide**: si la historia reciente de TD/TMIN, más la geografía y la
  estación del año, explican mejor la anomalía de mañana que una sola
  variable. Este es el "baseline no-deep" que pide el bead `tdew-x46`.
- **Hipótesis**: "importa la historia reciente + geografía + estación, todo
  junto, por sitio".
- **Fórmula**:
  ```
  TD_anom(t+1) ~ const
               + TMIN_anom(t) + TMIN_anom(t-1)
               + TD_anom(t) + TD_anom(t-1) + TD_anom(t-2) + TD_anom(t-6) + TD_anom(t-29)
               + sin(doy(t+1)) + cos(doy(t+1))
               + DEM + TDI + X + Y
               + LST_DAY(mes de t+1) + LST_NIGHT(mes de t+1)
  ```
  (15 variables + intercepto), **una regresión por departamento** — no por
  celda individual, esa sería la granularidad del modelo de producción de
  Piero Palacios (ver sección 4).
- **Proceso de ajuste**: `tdew_estimation.metrics.NormalEquationsAccum` —
  el mismo truco de acumulación por bloques que `dept_ols`, pero
  multivariado: acumula `X'X` (16×16) y `X'y` por `id_bucket` y resuelve
  `beta = (X'X + ridge·I)⁻¹ X'y` al final (`ridge=1e-6`, solo para
  estabilidad numérica frente a la colinealidad entre lags — matemáticamente
  equivalente a `statsmodels.OLS(...).fit()` sobre el dataset completo,
  verificado en `tests/test_metrics.py`). Solo con filas de `split=train`.

### 3.5 `generalist_mlr`
- **Qué mide**: si la dinámica que aprende `dept_mlr` por separado en cada
  departamento se puede compartir en un solo modelo para los 4 sitios sin
  perder poder predictivo — la pregunta de fondo detrás de "¿generalista o
  por sitio?" (ver sección 6, investigación citada).
- **Hipótesis**: "lo mismo que `dept_mlr`, pero la dinámica se puede
  compartir entre sitios" (con una corrección por región natural).
- **Fórmula**: igual que `dept_mlr`, más:
  ```
  + region_Sierra + region_Selva                          (Costa = referencia)
  + region_Sierra × (cada uno de los 7 lags de TD/TMIN)
  + region_Selva  × (cada uno de los 7 lags de TD/TMIN)
  ```
  (31 variables + intercepto en total), **un solo ajuste usando las filas de
  train de los 4 departamentos juntas**. Las interacciones región×lag dejan
  que la "memoria" de TD pese distinto en Selva que en Sierra, sin necesitar
  4 modelos separados.
- **Proceso de ajuste**: mismo `NormalEquationsAccum`, pero cada fila se
  pondera por `peso(sitio) = 1 / n_filas_train(sitio)` antes de acumular —
  sin este peso, Loreto/Iquitos (~1.2 mil millones de filas de train) le
  ganaría el ajuste 10.5x a Lima (~116 millones) simplemente por volumen, no
  porque su dinámica sea "más correcta".

## 4. Resumen (tabla)

| # | método | mide / hipótesis | fórmula (resumen) | ¿se ajusta? | granularidad |
|---|---|---|---|---|---|
| 1 | `climatology` | solo importa la época del año | `TD_clim(t+1)` | no | — |
| 2 | `persistence` | solo importa la inercia (mañana ≈ hoy) | `TD_anom(t) + TD_clim(t+1)` | no | — |
| 3 | `dept_ols` | solo importa `TMIN` de hoy | `a + b·TMIN_anom(t)` | sí (OLS) | 1 modelo/departamento |
| 4 | `dept_mlr` | historia + geografía + estación, por sitio | 15 variables (lags+estáticos+doy) | sí (ridge normal-eqs) | 1 modelo/departamento |
| 5 | `generalist_mlr` | igual que #4, compartido entre sitios | 31 variables (+ región × lags), ponderado | sí (ridge normal-eqs, WLS) | 1 modelo para los 4 sitios |

Las 5 filas se puntúan con las mismas `n, rmse, mae, bias, r, skill_vs_clim`
por `(sitio, split)` — el examen es idéntico, lo que cambia es qué hipótesis
sobre la física/estadística del problema encierra cada fórmula.

## 5. Comparación completa: qué hizo Palacios vs. qué hicimos en esta sesión

Esta sección enumera **todas** las diferencias entre el trabajo previo de
Piero Palacios (`tdew_estimation/`, `HPC_code_tunning/`, `docs/MODEL_INPUTS.md`,
`docs/evaluation_methodology.md`) y los 5 baselines de `tdew-x46` — no solo
la regla de fuga de `t+1`, que es apenas una de ocho diferencias.

### 5.0 Tabla maestra (todas las dimensiones)

| Dimensión | Piero Palacios (`tdew_estimation/`, `HPC_code_tunning/`) | Esta sesión (`tdew-x46`) |
|---|---|---|
| **Objetivo/tarea** | Producción: rellenar el hueco real de TD 2017–2020 (no hay TD real en ese rango) | Investigación: primer leaderboard de baselines para comparar contra TCN/GRU/Transformer de la Semana 1 |
| **Alcance espacial** | Grid nacional completo (~2.8M celdas), particionado en 41 zonas climáticas SENAMHI | 4 departamentos completos (436,523 celdas): Lima, Cusco, Loreto/Iquitos, San Martín/Tarapoto |
| **Alcance temporal (train)** | 1981–2016 (o hasta el año de corte del holdout) | 2002–2012 (fijo, `period.splits.train` del manifest) |
| **Splits de evaluación** | `ll1`/`ll2`/`ll4`: holdouts de 1, 2 y 4 años sobre el mismo régimen de gap-fill | 1 solo split fijo: train 2002–2012 / validation 2013–2014 / test 2015–2016, sin mezcla |
| **Variable objetivo** | `TD` (dewpoint) absoluto, para el hueco real 2017–2020 | `Td(t+1)`: un paso adelante, dentro de un rango donde SÍ existe TD real (2002–2016) |
| **Timing de features** | Permite `TMIN` del **mismo día** que el target (dato real conocido incluso en el hueco) | Prohíbe cualquier input `>= t+1` (`leakage_constraint` del manifest) — ni siquiera TMIN del mismo día |
| **Mecanismo de predicción** | **Autoregresivo/recursivo**: dentro del hueco, los lags de `TD_anom` se alimentan con la predicción del propio modelo del día anterior (`tdew_estimation/forecast.py`), porque no hay TD real que usar | **No autoregresivo**: todos los lags son TD/TMIN reales observados (2002–2016 tiene TD real completo), nunca la propia predicción del modelo |
| **Técnica de modelo (`tuned`/producción)** | Regresión ponderada **local por kernel** (WLS, kernel Tricube o Gaussiano, medio-ancho `h` en días) sobre una **ventana circular de día-del-año**, ajustada **por separado en cada celda** — cientos de miles de regresiones locales por celda | Una regresión **global** (sin ventana de kernel) por departamento (`dept_ols`/`dept_mlr`) o una sola para los 4 sitios (`generalist_mlr`), con `sin/cos(doy)` como feature explícito para capturar la estacionalidad en vez de ventanear por DOY |
| **Selección de hiperparámetros/features** | Sí: `HPC_code_tunning/select_backtest.py` re-selecciona, por (zona × doy), qué subconjunto de lags usar de un pool de candidatos (`TuningConfig`, `candidate_pool`, `h_grid`) — solo con años de train | No: el set de features de `dept_mlr`/`generalist_mlr` es fijo, decidido de antemano (sección 3); `ridge=1e-6` es un valor fijo de estabilidad numérica, no buscado |
| **Cómputo a escala** | Dask distribuido (`dask.distributed`, multi-worker/multi-nodo SLURM) + un kernel WLS por lotes en GPU (`cupy`, ver `D3 batched-WLS kernel`) | Un solo proceso, acumulación streaming por `id_bucket` en NumPy puro (`tdew_estimation.metrics.NormalEquationsAccum`/`MetricsAccum`), sin Dask ni GPU |
| **Normalización** | Anomalía `TD_anom = TD − TD_clim` por (celda, doy); sin capa adicional de z-score | Igual noción de anomalía (reusada de `pipeline/gold.py`), más una capa de z-score train-only (`pipeline/normalize.py`) que existe en el dataset pero que estos 5 baselines **no usan** (una regresión lineal no la necesita; sí la usarán probablemente TCN/GRU/Transformer) |
| **Partición espacial usada como feature/agrupador** | Zona climática SENAMHI (metadato meteorológico fijo, 41 zonas) | Departamento administrativo (metadato político, 4 unidades) — el propio manifest (`sites.senamhi_41_zones_compatibility`) deja **pendiente y sin asumir** que ambos esquemas sean equivalentes |
| **Escalera de métodos evaluados** | 4 métodos: `climatology`, `td_eq_tmin`, `zone_ols`, `tuned` (detalle en 5.1) | 5 métodos: `climatology`, `persistence`, `dept_ols`, `dept_mlr`, `generalist_mlr` (detalle en sección 3) — solo el nombre `climatology` se repite, y ni ese se calcula igual |
| **Métricas** | `n, rmse, mae, bias, r, skill_vs_clim` + inferencia estadística (bootstrap de bloques por celda, Cohen's d, test de permutación — `effect_sizes.py`) | Mismas fórmulas de `n, rmse, mae, bias, r, skill_vs_clim` (reimplementadas, sección 3) — **sin** la capa de inferencia estadística de `effect_sizes.py` (no se hizo en esta sesión) |
| **Registro/tracking** | Salidas a CSV/parquet planos (`metrics.csv`, `predictions.parquet`, `effect_sizes.csv`), sin MLflow | MLflow (`sqlite:///mlflow.db`, experiment `tdew-week1`) + DVC + ZenML (sección 6) |

### 5.1 Por qué estas diferencias no son solo "un cambio de datos de entrada"

De las filas de la tabla, tres son genuinamente cambios de **metodología**
(no de qué columnas entran a la fórmula), y vale la pena remarcarlas:

1. **Mecanismo del modelo**: kernel-local por (celda, ventana-DOY) vs.
   regresión global por departamento/generalista con estacionalidad
   explícita. No es "el mismo modelo con menos columnas" — es una técnica de
   ajuste distinta (regresión local no-paramétrica en el espacio de DOY vs.
   regresión lineal global con una feature cíclica).
2. **Mecanismo de predicción**: autoregresivo/recursivo (alimentado con sus
   propias predicciones cuando no hay TD real) vs. no-autoregresivo (todos
   los lags son siempre datos reales, porque el rango 2002–2016 nunca tiene
   huecos de TD). Esto no es una diferencia de columnas, es una diferencia de
   cómo se genera la predicción día a día.
3. **Régimen de evaluación**: holdouts multi-año (`ll1/ll2/ll4`, simulando el
   gap real) vs. un único split fijo de un paso adelante. Son dos preguntas
   de investigación distintas, no la misma pregunta con distintos datos.

La regla de `t+1` (no usar `TMIN` del mismo día) sí es, en cambio, una
diferencia puramente de **qué dato entra** — la única de las ocho filas de la
tabla que es solamente eso.

### 5.2 La escalera de Palacios NO son los mismos 5 métodos

Malentendido frecuente (surgió en esta sesión, se aclara explícitamente): la
diferencia con Palacios **no es únicamente** "los mismos 4-5 métodos, solo
que sin `t+1` en la entrada". Su escalera (`HPC_code_tunning/backtest.py`,
`docs/evaluation_methodology.md` sección 5) tiene 4 métodos, y solo uno
coincide en nombre con los nuestros — con fórmula distinta:

| Palacios (`backtest.py`) | fórmula | ¿corresponde a alguno de nuestros 5? |
|---|---|---|
| `climatology` | promedio histórico por (celda, doy), **recalculado por cada ventana de holdout** (`ll1`/`ll2`/`ll4`) | mismo nombre, pero climatología calculada distinto (nuestro `climatology` usa fijo train 2002–2012 del manifest) |
| `td_eq_tmin` | `pred = TMIN` (directo, sin anomalía, sin ajuste) | **no existe en nuestra lista** — no equivale a `persistence` (que persiste la *anomalía de TD de ayer*, no TMIN de hoy) |
| `zone_ols` | `Td ~ a + b·TMIN` (TMIN del **mismo día** que el target), una por **zona climática SENAMHI** (41 zonas) | se parece en espíritu a `dept_ols`, pero usa TMIN del mismo día (prohibido acá) y zona SENAMHI, no departamento |
| `tuned` (el modelo de producción) | WLS por **celda individual × ventana de día-del-año** | **no existe en nuestra lista** — sería un 6to baseline hiperlocal; se descartó por costo de cómputo (ver 5.0, fila "Cómputo a escala") y queda fuera de alcance de esta sesión, no implementado |

Y al revés: `persistence`, `dept_mlr` y `generalist_mlr` **no tienen
equivalente** en la escalera de Palacios — son fórmulas nuevas de esta
sesión, no una versión "recortada" de las suyas. Lo único reusado tal cual de
su trabajo son las fórmulas de las métricas (`rmse/mae/bias/r/skill_vs_clim`)
y la idea general de tener una escalera de dificultad creciente — no los
métodos en sí.

**Por qué no se reusó el código de Palacios tal cual**: no resuelve la
pregunta que necesita responder esta semana ("¿qué tanto mejora un modelo
secuencial (TCN/GRU/Transformer) sobre un baseline liviano, bajo el *mismo*
régimen de datos/splits/features que esos modelos van a usar?"). Reusarlo
sin cambios habría comparado peras con manzanas: su régimen resuelve un
problema real distinto (rellenar 2017–2020) con reglas de fuga distintas
(TMIN del mismo día sí permitido) y a una granularidad (por celda) que los
modelos deep de esta semana no van a replicar. Lo que sí se reusó
explícitamente: la idea de "escalera de baselines" y las fórmulas exactas de
`rmse/mae/bias/r/skill_vs_clim` de `HPC_code_tunning/backtest.py` (sección 3
de este documento), reimplementadas en `tdew_estimation/metrics.py` para el
nuevo régimen — así los números quedan en el mismo lenguaje/formato que el
resto del proyecto, aunque no sean numéricamente comparables entre sí (son
exámenes distintos).

## 6. Cómo reproducir exactamente estos números

```bash
uv run python -m pipeline.zenml_pipeline               # hasta baseline_dataset (+ qc)
uv run python -m experiments.baselines.zenml_pipeline   # leaderboard.csv
uv run python -m experiments.baselines.plot_leaderboard # skill_vs_climatology.png
```

Escala real de este run: 436,523 celdas (4 departamentos), ~305M
filas de test (pooled) y ~305M de validation — `Data/gold/baseline_dataset`
son 64 shards (`id_bucket=0..63`) por ~47GB en total; por eso todo el código
de `pipeline/baseline_features.py` y `experiments/baselines/train_baselines.py`
está streameado por bucket (nunca carga un departamento completo en memoria
— ver `tdew_estimation.metrics.NormalEquationsAccum`/`MetricsAccum`).

## 7. Dónde quedó registrado cada run

- **MLflow** (`sqlite:///mlflow.db`, experiment `tdew-week1`): un run
  `week1-baseline` por `(site, method)` con tags `git_commit`, `seed=0`,
  `dataset_version=Data/gold/baseline_dataset`, `site`, y métricas
  `{split}_{n,rmse,mae,bias,r,skill_vs_clim}`; más un run
  `week1-baseline-leaderboard` con `leaderboard.csv` como artifact.
  Inspeccionar con `mlflow ui --backend-store-uri sqlite:///mlflow.db`.
- **Beads**: notas de progreso, resultado final y coordinación en
  `bd show tdew-x46`.
- **Git**: el run que generó los archivos de este directorio se ejecutó
  contra el estado del working tree que este mismo commit fija (el tag
  `git_commit` en MLflow apunta al commit *padre*, ya que el run corrió
  antes de este commit; si se necesita que el tag coincida exactamente,
  re-ejecutar `experiments.baselines.zenml_pipeline` después de este commit).

## 8. Investigación externa citada (transparencia sobre uso de IA)

La decisión de agregar `generalist_mlr` (y la interacción región-natural ×
lags) se apoya en un resumen de investigación generado por un agente de IA
(Claude, modelo Opus) sobre cómo GraphCast/Pangu-Weather/MetNet-3/AIFS
resuelven la generalización espacial en modelos de clima a gran escala.
**Ese contenido fue generado con asistencia de IA y no ha sido validado por
un experto humano del equipo** — se cita aquí por transparencia y se
recomienda su revisión antes de asumirlo como base definitiva para el
diseño de la TCN/GRU/Transformer de esta semana. Fuentes primarias citadas
por el agente: GraphCast (DeepMind), MetNet-3 (Google Research), Pangu-
Weather (Huawei, GMD 2024), AIFS/stretched-grid (ECMWF, arXiv:2409.02891),
Montero-Manso & Hyndman (arXiv:2008.00444), Rasp & Lerch (MWR 2018).
