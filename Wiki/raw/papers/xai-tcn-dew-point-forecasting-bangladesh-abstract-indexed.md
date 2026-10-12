# Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks — abstract indexado

Segunda captura de la misma fuente que
`raw/papers/xai-tcn-dew-point-forecasting-bangladesh.md`, hecha por una ruta distinta. La
primera captura (2026-09-14) se reconstruyó solo con snippets de WebSearch porque IEEE Xplore
devolvió HTTP 418; quedó sin autores, sin RMSE y sin baselines. `raw/` es inmutable, así que
esta captura se crea con slug propio en vez de editar aquella.

- **Venue/año**: IEEE Access, 2025.
- **DOI**: https://doi.org/10.1109/ACCESS.2025.3490969
- **Autores (según el registro indexado)**: Md. Abdullah et al.
- **Citas al momento de la captura**: 11.
- **Ruta de captura**: registro indexado de Consensus (agregador sobre Semantic Scholar,
  PubMed, Scopus y arXiv), consultado el 2026-09-21. **Sigue sin leerse el PDF de IEEE
  Xplore.**
- **Fecha de captura**: 2026-09-21

## Abstract (verbatim, según el registro indexado)

"Climate change poses global challenges, including rising temperatures and extreme weather,
severely affecting regions such as Bangladesh. Predictions of dew point temperature, a key
indicator for climate change, are vital for climate adaptation, agriculture, energy planning,
weather forecasting, and public health. This research analyzed dew point temperature data
from 35 weather stations across Bangladesh to find patterns and trends over four decades
since 1980. This study developed an attention-based Temporal Convolutional Networks (TCN)
model for predicting dew point temperature. The model was enhanced with Explainable AI (XAI)
techniques to facilitate feature selection and provide interpretable insights into the
factors influencing the predictions. In order to assess the performance of the proposed model
this work utilized different performance measures and achieved test loss of 0.002, validation
loss of 0.00212, Mean Absolute Error (MAE) of 0.032, and Root Mean Squared Error (RMSE) of
0.044, R² and adjusted R² values of 0.938, demonstrating higher prediction accuracy compared
to other models such as Long Short-Term Memory (LSTM), Convolutional Neural Network (CNN),
Bi-directional Long Short-Term Memory (BiLSTM), LSTM_CNN hybrid, and Gated Recurrent Unit
(GRU). Consistent performance across datasets from other weather stations confirmed the
robustness of the suggested model."

## Qué resuelve y qué sigue abierto respecto a la primera captura

Resuelto: primer autor, RMSE (0.044), R² y R² ajustado (0.938), y la lista de baselines
comparados (LSTM, CNN, BiLSTM, LSTM_CNN, GRU).

Sigue abierto: la lista completa de autores, la arquitectura exacta del TCN (profundidad,
dilataciones, dónde entra la atención), qué técnica XAI concreta se usó, las variables de
entrada, el horizonte de pronóstico, el split train/validation/test, y —lo más relevante para
comparar— **la escala en que se calculan MAE y RMSE**. Un RMSE de 0.044 sobre punto de rocío
en °C sería implausible; la lectura consistente con un test loss de 0.002 es que la serie está
normalizada antes de calcular la pérdida, pero el abstract no lo dice. Tampoco hay
persistencia ni climatología entre los baselines.
