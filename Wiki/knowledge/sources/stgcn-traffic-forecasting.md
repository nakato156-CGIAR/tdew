---
type: Source
title: "Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting"
description: Paper de Yu, Yin y Zhu (IJCAI-18) que propone STGCN, un framework puramente convolucional (graph conv + gated temporal conv) para pronóstico de tráfico.
resource: https://www.ijcai.org/proceedings/2018/0505.pdf
tags: [deep-learning, graph-neural-networks, traffic-forecasting, time-series, convolutional-networks]
timestamp: 2026-09-11T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: []
---

# Spatio-Temporal Graph Convolutional Networks (STGCN)

Ver captura completa en `[[raw/papers/stgcn-traffic-forecasting]]`.

## Resumen

Yu, Yin y Zhu (IJCAI-18, pp. 3634-3640) proponen STGCN, un framework de deep learning para
pronóstico de tráfico a mediano-largo plazo que modela la red vial como un grafo y combina
capas de convolución de grafo (spectral graph convolution, con aproximación de Chebyshev o
de primer orden) con capas de convolución temporal con compuertas (gated CNN, sin RNN/LSTM),
apiladas en bloques "ST-Conv" con conexiones residuales y bottleneck. Evaluado en dos
datasets reales de tráfico (BJER4 en Beijing, PeMSD7 en California), STGCN supera con
significancia estadística a baselines clásicos (HA, LSVR, ARIMA) y de deep learning
(FNN, FC-LSTM, GCGRU) en MAE/MAPE/RMSE para horizontes de 15/30/45 min, con ~14x menos
tiempo de entrenamiento y ~2/3 de los parámetros frente a GCGRU (el baseline basado en
grafo + RNN más cercano).

**Nota de dominio**: paper de deep learning aplicado a pronóstico de series temporales
espacio-temporales (tráfico vial), no de LLMs. Se ingiere a pedido explícito del usuario;
es relevante para tdew por la técnica de modelado espacio-temporal con GNN + convoluciones
temporales, potencialmente transferible a pronóstico climático/subestacional sobre datos
con estructura de grafo o grid.

## Conceptos derivados

- `[[methods/stgcn-graph-conv-forecasting]]` — la arquitectura STGCN (ST-Conv blocks, graph
  conv espectral + gated temporal conv).
- `[[findings/stgcn-vs-baselines-traffic]]` — resultados comparativos de precisión y
  eficiencia de entrenamiento frente a baselines.
