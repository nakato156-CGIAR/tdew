---
type: Finding
title: Desempeño del TCN con atención para pronóstico de punto de rocío (Bangladesh)
description: Métricas de test/validation loss y MAE reportadas para el modelo TCN+atención+XAI sobre datos de punto de rocío de 35 estaciones de Bangladesh.
resource: https://doi.org/10.1109/ACCESS.2025.3490969
tags: [dew-point, tcn, attention, bangladesh, metrics]
timestamp: 2026-09-14T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/xai-tcn-dew-point-forecasting-bangladesh]]"]
---

# Desempeño de TCN+atención+XAI en pronóstico de dew point (Bangladesh)

Resultados reportados para `[[methods/attention-tcn-explainable-forecasting]]` sobre datos
de 35 estaciones meteorológicas de Bangladesh (~4 décadas desde 1980).

## Métricas reportadas (vía WebSearch, no verificadas contra el paper completo)

- **Test loss**: 0.002
- **Validation loss**: 0.00212
- **Mean Absolute Error (MAE)**: 0.032
- **Root Mean Squared Error (RMSE)**: métrica mencionada como reportada, valor exacto no
  disponible en esta captura.

## Limitaciones

- No se confirma la unidad/escala de las métricas (p.ej. si dew point está normalizado
  antes de calcular el loss, lo cual afectaría directamente la magnitud de MAE/RMSE).
- No hay comparación contra baselines (LSTM, ARIMA, etc.) disponible en esta captura.
- No se confirma el split exacto de entrenamiento/validación/test.
- Esta entrada está en `status: draft`; no promover a `reviewed` sin validar las cifras
  contra el PDF original (DOI 10.1109/ACCESS.2025.3490969) — ver nota de acceso en
  `[[sources/xai-tcn-dew-point-forecasting-bangladesh]]`.
