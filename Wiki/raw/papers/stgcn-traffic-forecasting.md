# Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting

- **Venue/año**: IJCAI-18 (Proceedings of the Twenty-Seventh International Joint Conference on
  Artificial Intelligence), pp. 3634-3640, 2018.
- **URL**: https://www.ijcai.org/proceedings/2018/0505.pdf
- **Autores**: Bing Yu, Haoteng Yin, Zhanxing Zhu (Peking University / Center for Data Science /
  Beijing Institute of Big Data Research).
- **Fecha de captura**: 2026-09-11

## Abstract

El pronóstico de tráfico preciso y a tiempo es crucial para el control y la guía del
tráfico urbano. Debido a la alta no linealidad y complejidad del flujo de tráfico, los
métodos tradicionales no satisfacen los requisitos de predicción a mediano-largo plazo y
suelen ignorar las dependencias espaciales y temporales. Los autores proponen Spatio-Temporal
Graph Convolutional Networks (STGCN), un framework de deep learning que formula el problema
sobre grafos y construye el modelo con estructuras completamente convolucionales (sin
unidades recurrentes), logrando entrenamiento más rápido con menos parámetros. STGCN captura
correlaciones espacio-temporales de forma efectiva y supera consistentemente a baselines
state-of-the-art en datasets reales de tráfico.

## Metodología (extracto)

- **Formulación del problema**: la red de tráfico se modela como un grafo (dirigido o no)
  G = (V, E, W), donde cada observación v_t en el tiempo t es una señal de grafo definida
  sobre n estaciones/sensores, en vez de tratar la red como grids o segmentos independientes.
- **Convolución en grafos (graph CNN)**: usa el operador de convolución espectral de grafos
  Θ ⋆G x = U Θ(Λ) Uᵀ x, con dos estrategias de aproximación para reducir el costo de O(n²):
  - **Chebyshev polynomials approximation** (Defferrard et al. 2016): localiza el filtro y
    reduce el costo a O(K|E|).
  - **1st-order approximation** (Kipf & Welling 2016): formulación lineal por capas, apilando
    capas de convolución de grafo localizadas de orden 1, más eficiente para grafos grandes.
- **Convolución temporal con compuertas (gated CNN)**: en vez de RNN/LSTM, aplica convolución
  causal 1-D de ancho K_t seguida de Gated Linear Units (GLU) para capturar dinámicas
  temporales, permitiendo entrenamiento paralelo (inspirado en Gehring et al. 2017, seq2seq
  convolucional).
- **ST-Conv block**: bloque "sandwich" con dos capas de convolución temporal con compuertas y
  una capa de convolución espacial de grafo en medio; incluye conexiones residuales,
  estrategia de bottleneck (compresión/expansión de canales) y layer normalization. El modelo
  apila dos ST-Conv blocks más una capa de salida totalmente conectada.
- **Función de pérdida**: L2 entre la predicción v̂ y el valor real v_{t+1}, optimizada con
  RMSprop (50 épocas, batch size 50, learning rate inicial 1e-3 con decay 0.7 cada 5 épocas).

## Datasets

- **BJER4**: 12 rutas del anillo este No.4 de Beijing, detectores de doble lazo, agregado
  cada 5 min, jul-ago 2014 (excluyendo fines de semana).
- **PeMSD7(M) / PeMSD7(L)**: California PeMS (Caltrans Performance Measurement System),
  Distrito 7, 228 y 1,026 estaciones respectivamente, mayo-jun 2012, agregado cada 5 min.
- Todos los experimentos usan M=12 pasos históricos (60 min) para predecir H=3/6/9 pasos
  (15/30/45 min).

## Resultados (extracto)

- STGCN (variantes Cheb y 1st-order) supera con significancia estadística (two-tailed T-test,
  α=0.01, P<0.01) a HA, LSVR, ARIMA, FNN, FC-LSTM y GCGRU en MAE, MAPE y RMSE, en las tres
  ventanas de predicción (15/30/45 min) en BJER4 y PeMSD7(M/L).
- En PeMSD7(M), STGCN entrena en 272s vs. 3,824s de GCGRU (~14x más rápido); en PeMSD7(L),
  GCGRU necesita reducir el batch size a la mitad por límite de memoria GPU y aun así STGCN
  usa menos de un décimo del tiempo de entrenamiento de GCGRU.
- STGCN usa ~4.54×10^5 parámetros: ~2/3 de los de GCGRU y ahorra >95% de parámetros respecto
  a FC-LSTM.
- La variante 1st-order es ~20% más rápida que Cheb en el dataset más grande, con desempeño
  comparable.

## Nota de captura

Captura basada en la extracción de texto (pdftotext) del PDF oficial de IJCAI
(https://www.ijcai.org/proceedings/2018/0505.pdf). La extracción de fórmulas matemáticas
pierde algunos símbolos (subíndices, superíndices) por limitaciones del extractor de texto;
las tablas de resultados (Tablas 1-3 del paper) también sufrieron pérdida parcial de
alineación de columnas. Contenido generado con asistencia de IA (Claude) — validar cifras y
fórmulas exactas contra el PDF original antes de citarlas en trabajo downstream.
