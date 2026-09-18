# Trazabilidad — tdew-x46 baselines (Semana 1, Día 4)

Este documento responde: **de dónde salieron** `leaderboard.csv` y
`skill_vs_climatology.png`, **bajo qué protocolo/reglas** se calcularon, y
**cómo reproducirlos exactamente**.

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
- **Normalización/climatología**: estadísticos calculados SOLO con años de
  train (2002–2012), nunca con validation/test.

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

## 3. Cómo se calculó cada método (fórmulas exactas)

Ver docstrings de `experiments/baselines/train_baselines.py` para el detalle
completo. Resumen:

| método | fórmula | ajuste |
|---|---|---|
| `climatology` | `TD_clim(ID, doy(t+1))` | ninguno |
| `persistence` | `TD_anom(t) + TD_clim(t+1)` | ninguno |
| `dept_ols` | `TD_anom(t+1) ~ a + b·TMIN_anom(t)`, 1 por departamento | `tdew_estimation.metrics.OLSAccum` (closed-form) |
| `dept_mlr` | `TD_anom(t+1) ~` lags TD/TMIN + estáticos + estacionalidad, 1 por departamento | `tdew_estimation.metrics.NormalEquationsAccum` (ridge=1e-6) |
| `generalist_mlr` | igual que `dept_mlr` + dummies región natural × lags, pesos ∝ 1/n_train_filas(sitio) | ídem, un solo modelo para los 4 sitios |

Métricas (`n, rmse, mae, bias, r, skill_vs_clim`): mismas fórmulas que
`HPC_code_tunning/backtest.py::_metrics/_score_all` (documentado en
`docs/evaluation_methodology.md`), reimplementadas en
`tdew_estimation/metrics.py` para no acoplarse a ese régimen (que es un
problema distinto: gap-fill multi-año autoregresivo, no `Td(t+1)`
single-step).

## 4. Cómo reproducir exactamente estos números

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

## 5. Dónde quedó registrado cada run

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

## 6. Investigación externa citada (transparencia sobre uso de IA)

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
