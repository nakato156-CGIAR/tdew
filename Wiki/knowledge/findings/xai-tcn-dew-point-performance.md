---
type: Finding
title: Desempeño del TCN con atención para pronóstico de punto de rocío (Bangladesh)
description: Test loss 0.002, validation loss 0.00212, MAE 0.032, RMSE 0.044 y R² 0.938 para el TCN+atención+XAI sobre punto de rocío en 35 estaciones de Bangladesh, en escala no declarada y sin baseline de persistencia.
resource: https://doi.org/10.1109/ACCESS.2025.3490969
tags: [dew-point, tcn, attention, bangladesh, metrics]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/xai-tcn-dew-point-forecasting-bangladesh]]", "[[raw/papers/xai-tcn-dew-point-forecasting-bangladesh-abstract-indexed]]"]
---

# Desempeño de TCN+atención+XAI en pronóstico de dew point (Bangladesh)

Resultados reportados para `[[methods/attention-tcn-explainable-forecasting]]` sobre datos
de 35 estaciones meteorológicas de Bangladesh (~4 décadas desde 1980).

## Métricas reportadas (abstract indexado, no verificadas contra el PDF)

- **Test loss**: 0.002
- **Validation loss**: 0.00212
- **Mean Absolute Error (MAE)**: 0.032
- **Root Mean Squared Error (RMSE)**: 0.044
- **R² y R² ajustado**: 0.938

## Baselines comparados

LSTM, CNN, BiLSTM, híbrido LSTM_CNN y GRU. Los autores afirman mayor precisión que todos
ellos y consistencia al aplicar el modelo a datos de otras estaciones.

## Limitaciones

- **La escala de las métricas sigue sin declararse.** Un RMSE de 0.044 sobre punto de rocío
  en °C sería implausible; la lectura compatible con un test loss de 0.002 es que la serie
  está normalizada antes de calcular la pérdida, pero ni el abstract ni los snippets lo
  dicen. Mientras eso no se verifique, estas cifras **no son comparables** con el RMSE en °C
  del leaderboard de tdew.
- No hay persistencia ni climatología entre los baselines, así que las métricas no acotan el
  aporte sobre una referencia trivial. Ver
  `[[patterns/persistence-climatology-reference-baselines]]`.
- No se confirma el split exacto de entrenamiento/validación/test, el horizonte de pronóstico
  ni las variables de entrada.
- Esta entrada sigue en `status: draft`; no promover a `reviewed` sin validar las cifras
  contra el PDF original (DOI 10.1109/ACCESS.2025.3490969) — ver notas de acceso en
  `[[sources/xai-tcn-dew-point-forecasting-bangladesh]]`.
