---
type: Source
title: "Redefining multi-target weather forecasting with a novel deep learning model: HTC-LSTM-Attn in Bangladesh"
description: Paper de Kabir y Chakma (PLOS ONE, 2026) que combina convoluciones temporales jerárquicas, BiLSTM y atención para pronosticar temperatura máxima y humedad mensuales en 24 estaciones de Bangladesh, con hold-out espacial.
resource: https://doi.org/10.1371/journal.pone.0342431
tags: [weather-forecasting, deep-learning, tcn, bilstm, attention, bangladesh, spatial-holdout, benchmark]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# HTC-LSTM-Attn: pronóstico multi-objetivo de temperatura y humedad (PLOS ONE, 2026)

Ver captura completa en `[[raw/papers/htc-lstm-attn-multitarget-weather-bangladesh]]`.

## Resumen

Kabir y Chakma proponen HTC-LSTM-Attn, que apila tres Conv1D paralelas con kernels 1, 3 y 5
(96/64/96 filtros, concatenadas en 256 canales), un BiLSTM de 96 unidades por dirección y una
capa de atención softmax sobre los pasos de tiempo. Lo entrenan sobre datos **mensuales** de
la Bangladesh Agricultural Research Council (1961-2022) para temperatura máxima y humedad en
24 estaciones. El protocolo separa un test temporal (2016-2022, 19 estaciones vistas) y un
test espacial (2016-2022, 5 estaciones nunca vistas), y reporta RMSE de 0.9718 °C y 1.1898 °C
en temperatura sobre cada uno.

**Nota de dominio**: el interés para tdew es el protocolo, no la arquitectura. El hold-out
espacial sobre estaciones no vistas es la prueba que separa un modelo que generaliza a
celdas nuevas de uno que memoriza la serie de cada punto, y el proyecto todavía no tiene un
equivalente (sus splits son puramente temporales, 2002-2012 / 2013-2014 / 2015-2016).

## Limitación relevante

El paper compara contra 11 modelos aprendidos (LSTM, GRU, Conv1D, CNN-LSTM, ANN, DTR,
CatBoost, Autoformer, FEDformer, TimesNet, Pyraformer) pero **no contra persistencia ni
climatología**. Sobre series mensuales con ciclo anual fuerte, una climatología por mes ya
explica la mayor parte de la varianza, así que un R² de 0.85 no acota cuánto aporta el modelo
sobre esa referencia. Ver `[[patterns/persistence-climatology-reference-baselines]]`.

## Conceptos derivados

- `[[methods/htc-bilstm-attention-multitarget]]` — la arquitectura HTC + BiLSTM + atención.
- `[[findings/htc-lstm-attn-bangladesh-metrics]]` — las métricas reportadas en los dos
  conjuntos de test y la ablación de la atención.
