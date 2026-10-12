---
type: Method
title: STGCN — Spatio-Temporal Graph Convolutional Networks
description: Arquitectura puramente convolucional (sin RNN/LSTM) que combina convolución espectral de grafos con convolución temporal con compuertas (GLU) en bloques ST-Conv apilados, para pronóstico de series temporales sobre datos con estructura de grafo.
resource: https://www.ijcai.org/proceedings/2018/0505.pdf
tags: [graph-neural-networks, convolutional-networks, time-series, spatio-temporal, traffic-forecasting]
timestamp: 2026-09-11T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: ["[[sources/stgcn-traffic-forecasting]]"]
---

# STGCN — Spatio-Temporal Graph Convolutional Networks

Framework propuesto por Yu, Yin y Zhu (IJCAI-18, ver `[[sources/stgcn-traffic-forecasting]]`)
para pronóstico de series temporales definidas sobre un grafo (p. ej. una red de tráfico),
sin usar unidades recurrentes.

## Idea central

Modelar la red (de tráfico, o cualquier dominio con estructura de grafo) como un grafo
G = (V, E, W) en cada paso de tiempo, en vez de tratarla como grids o segmentos
independientes, y procesar la dimensión espacial con convolución de grafos y la dimensión
temporal con convolución causal 1-D — todo el modelo es convolucional, sin RNN/LSTM.

## Componentes

1. **Convolución espectral de grafos**: operador Θ ⋆G x = U Θ(Λ) Uᵀ x sobre la base de
   Fourier del grafo (autovectores del Laplaciano normalizado). Dos aproximaciones para
   evitar el costo O(n²):
   - **Chebyshev polynomials** (K-localizada, orden K-1): reduce el costo a O(K|E|).
   - **1st-order approximation** (Kipf & Welling): apila capas de convolución de grafo
     localizadas de orden 1; más económica y eficiente para grafos grandes, aunque menos
     expresiva que la aproximación de Chebyshev completa.
2. **Convolución temporal con compuertas (gated CNN)**: convolución causal 1-D de ancho K_t
   por nodo, seguida de Gated Linear Units (GLU: salida = P ⊙ σ(Q)) como no-linealidad,
   permitiendo entrenamiento completamente paralelo sobre el eje temporal (a diferencia de
   RNN/LSTM, que requieren iteración secuencial).
3. **ST-Conv block**: estructura "sandwich" — convolución temporal con compuertas →
   convolución espacial de grafo → convolución temporal con compuertas — con conexiones
   residuales, estrategia de bottleneck (compresión/expansión de canales, p. ej. 64→16→64) y
   layer normalization para evitar overfitting. El modelo completo apila dos ST-Conv blocks
   más una capa de salida convolucional/fully-connected.
4. **Entrenamiento**: pérdida L2 entre predicción y valor real, optimizador RMSprop.

## Por qué importa

Frente a enfoques previos que combinaban CNN (espacial) + RNN/LSTM (temporal), STGCN
elimina por completo la recurrencia, lo que evita la acumulación de error por pasos y el
costo computacional de entrenar RNNs, habilitando entrenamiento paralelo y modelos con
muchos menos parámetros sin sacrificar precisión (ver
`[[findings/stgcn-vs-baselines-traffic]]`).

## Relevancia potencial para tdew

Técnica de modelado espacio-temporal con estructura de grafo (o grid) + convoluciones
temporales, potencialmente transferible a series de tiempo climáticas/agroclimáticas con
estructura espacial (estaciones, celdas de grid) donde hoy se usan RNN/LSTM o modelos
puramente estadísticos.
