---
type: Method
title: Ensemble MultiLLR + AutoKNN para pronóstico subestacional
description: Ensemble de regresión local lineal multitarea (MultiLLR) y autoregresión k-NN multitarea (AutoKNN), combinadas por promedio ponderado de anomalías normalizadas.
resource: https://arxiv.org/abs/1809.07394
tags: [regression, ensemble, k-nn, feature-selection, forecasting]
timestamp: 2026-09-11T15:57:37Z
status: draft
contributed_by: [claude]
sources: ["[[sources/subseasonal-forecasting-western-us-ml]]"]
---

# Ensemble MultiLLR + AutoKNN para pronóstico subestacional

Técnica de dos componentes usada por Hwang et al. para predecir temperatura y
precipitación 2-6 semanas a futuro (ver `[[sources/subseasonal-forecasting-western-us-ml]]`).

## Componentes

1. **MultiLLR** (Multitask Local Linear Regression): integra features meteorológicas
   heterogéneas (presión, temperatura, anomalías SST/hielo marino, índice MEI/ENSO,
   oscilación Madden-Julian, humedad relativa, altura geopotencial, pronósticos NMME) y
   selecciona features con un procedimiento backward stepwise adaptado a una métrica de
   skill de coseno.
2. **AutoKNN** (Multitask Autoregressive k-Nearest-Neighbors): usa solo el historial de la
   propia variable objetivo — rezagos de 29/43 días, 58/86 días y 1 año — más los 20
   vecinos históricos más similares por skill medio.

## Combinación

Cada modelo produce anomalías predichas que se normalizan en norma L2; el ensemble final
es un promedio ponderado de esas anomalías normalizadas. Este esquema permite combinar un
modelo que usa contexto meteorológico amplio (MultiLLR) con uno puramente autoregresivo
(AutoKNN) sin que uno domine por escala.

## Resultado asociado

Ver `[[findings/subseasonal-forecasting-skill-gains]]` para las métricas de skill
reportadas.
