# Redefining multi-target weather forecasting with a novel deep learning model: Hierarchical temporal convolutional long short-term memory with attention (HTC-LSTM-Attn) in Bangladesh

- **Venue/año**: PLOS ONE, publicado el 23 de marzo de 2026.
- **URL**: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0342431
- **DOI**: https://doi.org/10.1371/journal.pone.0342431
- **Autores**: Md Anamul Kabir (Department of Electronics & Communication Engineering,
  Khulna University, Bangladesh; Dhaka Power Distribution Company Ltd), Chatak Chakma
  (Department of Electronics & Communication Engineering, Khulna University, Bangladesh).
- **Licencia**: Creative Commons Attribution (open access).
- **Fecha de captura**: 2026-09-21

## Abstract (verbatim)

"Bangladesh, being a country that relies on agriculture, has its agricultural sector
contributing around 20% to the Gross Domestic Product (GDP) and providing employment
opportunities for nearly 60% of the population. The study proposes a novel multi-step
forecasting deep-learning framework designed to forecast the maximum temperature and
humidity of 24 cities, called Hierarchical Temporal Convolutional Long Short-Term Memory
with attention (HTC-LSTM-Attn). The model contains hierarchical temporal convolutions (HTC)
for extracting multi-scale patterns, bidirectional LSTMs for sequential dependencies, and an
attention mechanism for learning to weigh time steps differently, while parameters are
optimized with Keras tuner. Using data from Bangladesh Agricultural Research Council (BARC)
from 1961 to 2022 and rigorous preprocessing with seasonal features and lagged statistics,
the model obtains temperature results for with a Mean Absolute Error (MAE) of 0.8178 °C,
Root Mean Squared Error (RMSE) of 0.9718 °C, R-squared (R²) of 0.8527, and Mean Absolute
Percentage Error (MAPE) of 2.8823% and humidity with MAE of 2.4693%, RMSE of 3.2442%, R² of
0.7228, and MAPE of 3.1757% values on a strict temporal test set (19 stations, 2016-2022).
On a spatial hold-out test set (5 unseen stations, 2016-2022) performance remains robust,
temperature with MAE of 0.9587 °C, RMSE of 1.1898 °C, R² of 0.8342, and MAPE of 3.1534% and
humidity with MAE of 2.4796%, RMSE of 3.2119%, R² of 0.6561, and MAPE of 3.2045%
consistently surpassing performance measures of models Gated Recurrent Unit (GRU), Long
Short-Term Memory (LSTM), Convolutional Neural Network (CNN), Decision Tree Regression
(DTR), Convolutional Neural Network - Long Short-Term Memory (CNN-LSTM) and latest
transformer-based architectures (Autoformer, FEDformer, TimesNet, and Pyraformer). These
results have shown robust spatial performance with the respective improvements needed in
agricultural planning and disaster management in Bangladesh, in its vulnerable climate
context."

## Arquitectura (extracto)

- **Hierarchical Temporal Convolutions (HTC)**: tres capas Conv1D en paralelo con kernels 1,
  3 y 5 (96, 64 y 96 filtros respectivamente), seguidas de batch normalization, ReLU y
  concatenación en un espacio de 256 canales.
- **BiLSTM**: 96 unidades por dirección.
- **Atención**: scores ponderados por softmax sobre los pasos de tiempo.
- Hiperparámetros optimizados con Keras tuner.

## Datos y protocolo

- Fuente: Bangladesh Agricultural Research Council (BARC), 1961-2022, **datos mensuales**
  (62 años).
- 24 estaciones válidas, tras excluir 11 estaciones "planas" sin variación suficiente.
- Variables: temperatura máxima, humedad, lluvia, velocidad de viento, nubosidad, horas de
  sol, más features estacionales y rezagadas construidas.
- Split: entrenamiento 1961-2012 (19 estaciones), validación 2013-2015 (mismas 19), test
  temporal 2016-2022 (mismas 19), y **test espacial** 2016-2022 sobre 5 estaciones nunca
  vistas (Bogra, Dinajpur, Srimangal, Madaripur, Feni).

## Baselines comparados

Deep learning: LSTM, GRU, Conv1D, CNN-LSTM, ANN. ML clásico: Decision Tree Regression,
CatBoost. Transformers: Autoformer, FEDformer, TimesNet, Pyraformer.

**No se reporta un baseline de persistencia ni de climatología.**

## Métricas reportadas

| Variable | Conjunto | MAE | RMSE | R² | MAPE |
|---|---|---|---|---|---|
| Temperatura máx. | test temporal (19 est.) | 0.8178 °C | 0.9718 °C | 0.8527 | 2.8823% |
| Temperatura máx. | test espacial (5 est. no vistas) | 0.9587 °C | 1.1898 °C | 0.8342 | 3.1534% |
| Humedad | test temporal | 2.4693% | 3.2442% | 0.7228 | 3.1757% |
| Humedad | test espacial | 2.4796% | 3.2119% | 0.6561 | 3.2045% |

Ablación: quitar la atención degrada el MAE de temperatura en 3.7% (test temporal) y 5.4%
(test espacial).
