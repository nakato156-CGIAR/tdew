---
type: Method
title: TCN con atención + XAI para pronóstico de punto de rocío
description: Temporal Convolutional Network con mecanismo de atención, combinado con técnicas de IA explicable para selección de features e interpretabilidad, aplicado a pronóstico de dew point.
resource: https://doi.org/10.1109/ACCESS.2025.3490969
tags: [tcn, attention, explainable-ai, xai, dew-point, deep-learning]
timestamp: 2026-09-14T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/xai-tcn-dew-point-forecasting-bangladesh]]"]
---

# TCN con atención + XAI para pronóstico de punto de rocío

Método propuesto por Huerta et al. — **nombres de autores no confirmados, ver nota de
acceso en** `[[sources/xai-tcn-dew-point-forecasting-bangladesh]]` — para pronosticar
temperatura de punto de rocío (dew point) usando una red Temporal Convolutional Network
(TCN) potenciada con un mecanismo de atención, y técnicas de IA explicable (XAI) aplicadas
tanto para selección de features como para interpretar las predicciones del modelo.

## Componentes del método (según lo disponible en esta captura)

1. **Backbone TCN**: red convolucional temporal (arquitectura exacta — número de capas,
   dilataciones, tamaño de kernel — no confirmada en esta captura).
2. **Mecanismo de atención**: añadido sobre el TCN para mejorar el modelado de
   dependencias temporales (tipo de atención no confirmado).
3. **XAI para selección de features**: técnica(s) de IA explicable usada(s) para decidir
   qué variables de entrada incluir en el modelo (técnica específica no confirmada; posible
   uso de SHAP según búsquedas relacionadas, pero no verificado directamente).
4. **XAI para interpretabilidad de predicciones**: las mismas o similares técnicas se usan
   post-hoc para explicar qué factores influyen en cada predicción de punto de rocío.

## Datos de entrenamiento/evaluación

- 35 estaciones meteorológicas de Bangladesh.
- Serie temporal de ~4 décadas (desde 1980).

## Limitaciones de esta entrada

Esta entrada está en `status: draft` porque la fuente no pudo leerse completa (bloqueo de
IEEE Xplore, ver `[[sources/xai-tcn-dew-point-forecasting-bangladesh]]`). Faltan: variables
de entrada exactas, arquitectura detallada, técnica XAI exacta, y split de
entrenamiento/validación/test. No promover a `reviewed` sin antes validar contra el PDF
original (DOI 10.1109/ACCESS.2025.3490969).

## Relevancia para tdew

Patrón potencialmente transferible al pipeline de tdew: combinar un modelo de secuencias
(TCN) con atención y XAI para pronóstico de variables meteorológicas derivadas (como
evapotranspiración o punto de rocío), ganando tanto desempeño como interpretabilidad de
qué variables de entrada dominan la predicción.
