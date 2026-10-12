# tdew-x46 — Baselines (Semana 1, Día 4)

Este directorio contiene el "primer leaderboard" pedido por el bead
`tdew-x46` (mitad baseline; la TCN se planifica/entrega aparte).

- `leaderboard.csv` — métricas por sitio/método/split.
- `skill_vs_climatology.png` — gráfico de barras, skill vs. climatología por
  sitio (test), generado por `experiments/baselines/plot_leaderboard.py`.
- **[`TRACEABILITY.md`](TRACEABILITY.md)** — de dónde sale cada número, bajo
  qué protocolo, y cómo reproducirlo exactamente. Leer esto antes de citar
  cualquier cifra de `leaderboard.csv`.

## Cómo se generó

```bash
uv run python -m pipeline.zenml_pipeline              # bronze -> ... -> baseline_dataset (+ qc)
uv run python -m experiments.baselines.zenml_pipeline  # entrena/evalúa los 5 métodos, escribe leaderboard.csv
```

(equivalente sin ZenML, para debugging puntual:
`uv run python -m pipeline.baseline_features` y
`uv run python -m experiments.baselines.train_baselines`.)

Todo corre bajo `docs/protocol/week1_manifest.yaml` (train 2002-2012 /
validation 2013-2014 / test 2015-2016, target `Td(t+1)` desde `X_{<=t}`, sin
inputs de `t+1` en adelante) y queda registrado en MLflow
(`sqlite:///mlflow.db`, experiment `tdew-week1`, runs `week1-baseline*`).

## Los 5 métodos

1. **`climatology`** — `TD_clim` del día objetivo. Sin ajuste.
2. **`persistence`** — persistencia de la anomalía de ayer
   (`TD_anom(t) + TD_clim(t+1)`). Sin ajuste.
3. **`dept_ols`** — regresión univariada `TD_anom(t+1) ~ TMIN_anom(t)`, una
   por departamento.
4. **`dept_mlr`** — el baseline no-deep que pide el bead: regresión
   multivariada (lags de TD/TMIN + estáticos + estacionalidad), una por
   departamento.
5. **`generalist_mlr`** — un único modelo sobre los 4 departamentos, con
   interacción región-natural (Costa/Sierra/Selva) × lags y ponderación
   inversa al tamaño de cada sitio (para que Loreto no domine el ajuste).
   Agregado a este scope siguiendo la investigación sobre cómo
   GraphCast/Pangu-Weather/MetNet-3/AIFS resuelven la generalización espacial
   (un modelo único con features de posición, no un modelo por celda) —
   contenido de esa investigación generado con asistencia de IA; validar la
   decisión con el equipo antes de asumirla como definitiva para la fase deep.

`leaderboard.csv`: columnas `site, method, split, n, rmse, mae, bias, r,
skill_vs_clim`, con `site="ALL"` como fila pooled. `skill_vs_clim` compara
contra `climatology` dentro del mismo `(site, split)`.

## Siguientes pasos (fuera de este scope)

- Leave-one-site-out San Martín→Loreto (extrapolación intra-Selva) — barato,
  no implementado aún.
- Comparar si `generalist_mlr` iguala a `dept_mlr`: si sí, es la señal de
  entrenar TCN/GRU/Transformer como un único modelo multi-sitio.
- Planificación e implementación de la TCN (bead `tdew-x46` sigue abierto).
