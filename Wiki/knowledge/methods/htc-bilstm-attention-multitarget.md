---
type: Method
title: HTC-LSTM-Attn — convoluciones temporales jerárquicas + BiLSTM + atención
description: Arquitectura multi-objetivo que concatena tres Conv1D de kernels 1/3/5, un BiLSTM bidireccional y una capa de atención softmax sobre los pasos de tiempo, con hiperparámetros ajustados por Keras tuner.
resource: https://doi.org/10.1371/journal.pone.0342431
tags: [tcn, bilstm, attention, multi-target, weather-forecasting, keras-tuner]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/htc-lstm-attn-multitarget-weather-bangladesh]]"]
---

# HTC-LSTM-Attn (Kabir y Chakma, PLOS ONE 2026)

## Bloque de convoluciones temporales jerárquicas (HTC)

Tres Conv1D en paralelo sobre la misma ventana de entrada, con kernels 1, 3 y 5 y 96, 64 y 96
filtros respectivamente, cada una seguida de batch normalization y ReLU, concatenadas en un
espacio de 256 canales. La jerarquía es por ancho de kernel en paralelo, no por dilatación
apilada como en el TCN de Bai et al.: captura escalas distintas en una sola capa en vez de
ampliar el campo receptivo en profundidad.

## Recurrencia y atención

La secuencia de 256 canales pasa por un LSTM bidireccional de 96 unidades por dirección, y
sobre las salidas por paso de tiempo se aplica una atención con scores normalizados por
softmax. La ablación reportada por los autores atribuye a esa atención una mejora de 3.7% en
el MAE de temperatura del test temporal y 5.4% en el del test espacial.

## Protocolo de evaluación

El aporte metodológico más transferible es el doble hold-out: además del corte temporal
habitual (entrenamiento 1961-2012, validación 2013-2015, test 2016-2022 sobre las mismas 19
estaciones), reservan 5 estaciones que el modelo nunca vio y las evalúan en el mismo periodo
de test. La caída de RMSE de temperatura de 0.9718 °C a 1.1898 °C entre ambos conjuntos
cuantifica cuánto del desempeño depende de haber visto esa estación durante el
entrenamiento.

Métricas completas en `[[findings/htc-lstm-attn-bangladesh-metrics]]`.
