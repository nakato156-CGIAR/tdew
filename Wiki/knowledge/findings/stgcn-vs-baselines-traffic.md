---
type: Finding
title: STGCN supera a baselines de tráfico con menos parámetros y entrenamiento más rápido
description: En BJER4 y PeMSD7(M/L), STGCN supera con significancia estadística a HA, LSVR, ARIMA, FNN, FC-LSTM y GCGRU en MAE/MAPE/RMSE (15/30/45 min), entrenando ~14x más rápido y con ~2/3 de los parámetros de GCGRU.
resource: https://www.ijcai.org/proceedings/2018/0505.pdf
tags: [benchmark, traffic-forecasting, graph-neural-networks, training-efficiency]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/stgcn-traffic-forecasting]]"]
---

# STGCN supera a baselines de tráfico con menos parámetros y entrenamiento más rápido

Resultados experimentales de Yu, Yin y Zhu (IJCAI-18, ver
`[[sources/stgcn-traffic-forecasting]]`) para el modelo `[[methods/stgcn-graph-conv-forecasting]]`.

## Precisión

- En los datasets BJER4, PeMSD7(M) y PeMSD7(L), ambas variantes de STGCN (Chebyshev y
  1st-order) superan con significancia estadística (two-tailed T-test, α=0.01, P<0.01) a
  los baselines Historical Average (HA), Linear SVR (LSVR), ARIMA, Feed-Forward NN (FNN),
  FC-LSTM y Graph Convolutional GRU (GCGRU), en MAE, MAPE y RMSE, para horizontes de
  predicción de 15, 30 y 45 minutos.
- ARIMA es consistentemente el peor método por su incapacidad de manejar datos
  espacio-temporales complejos. Los métodos de deep learning en general superan a los
  métodos estadísticos/ML clásicos.
- La ventaja de STGCN es mayor en PeMSD7 que en BJER4, atribuida a que la red de sensores de
  PeMS es más compleja y estructurada, permitiendo que el modelo aproveche mejor la
  topología espacial.

## Eficiencia de entrenamiento

- En PeMSD7(M), STGCN entrena en 272s vs. 3,824s de GCGRU (~14x más rápido).
- En PeMSD7(L) (1,026 estaciones), GCGRU debe reducir el batch size a la mitad por
  limitaciones de memoria GPU; aun así, STGCN usa menos de un décimo del tiempo de
  entrenamiento de GCGRU (1,926-1,554s de STGCN vs. 19,512s de GCGRU).
- STGCN usa ~4.54×10^5 parámetros: ~2/3 de los de GCGRU, y ahorra >95% de parámetros
  frente a FC-LSTM.
- La variante 1st-order approximation es ~20% más rápida que Chebyshev en el dataset más
  grande (PeMSD7(L)), con desempeño comparable.

## Comportamiento cualitativo

- En picos de hora punta (morning/evening rush), STGCN sigue la tendencia real más
  fielmente que otros métodos y detecta el fin del pico más temprano, atribuido a que no
  depende excesivamente del promedio histórico (a diferencia de la mayoría de redes
  recurrentes).
