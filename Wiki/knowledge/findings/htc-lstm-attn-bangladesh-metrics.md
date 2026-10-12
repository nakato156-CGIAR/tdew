---
type: Finding
title: HTC-LSTM-Attn — métricas en test temporal y hold-out espacial en Bangladesh
description: RMSE de 0.9718 °C (test temporal, 19 estaciones) y 1.1898 °C (5 estaciones no vistas) para temperatura máxima mensual, sin baseline de persistencia ni de climatología.
resource: https://doi.org/10.1371/journal.pone.0342431
tags: [benchmark, weather-forecasting, bangladesh, spatial-holdout, attention, ablation]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/htc-lstm-attn-multitarget-weather-bangladesh]]"]
---

# Métricas de HTC-LSTM-Attn (Kabir y Chakma, PLOS ONE 2026)

Resultados de `[[methods/htc-bilstm-attention-multitarget]]` sobre datos **mensuales** de
la Bangladesh Agricultural Research Council (1961-2022).

| Variable | Conjunto | MAE | RMSE | R² | MAPE |
|---|---|---|---|---|---|
| Temperatura máx. | test temporal, 2016-2022, 19 estaciones vistas | 0.8178 °C | 0.9718 °C | 0.8527 | 2.8823% |
| Temperatura máx. | test espacial, 2016-2022, 5 estaciones no vistas | 0.9587 °C | 1.1898 °C | 0.8342 | 3.1534% |
| Humedad | test temporal | 2.4693% | 3.2442% | 0.7228 | 3.1757% |
| Humedad | test espacial | 2.4796% | 3.2119% | 0.6561 | 3.2045% |

La degradación de RMSE de temperatura entre ambos conjuntos es de 22% (0.9718 a 1.1898 °C),
y la de R² de humedad, de 0.7228 a 0.6561. Es la magnitud que cuesta extrapolar a una
estación nunca vista en este dataset y con este modelo.

Ablación de la atención: el MAE de temperatura empeora 3.7% en el test temporal y 5.4% en el
espacial al quitarla.

Baselines comparados: LSTM, GRU, Conv1D, CNN-LSTM, ANN, Decision Tree Regression, CatBoost,
Autoformer, FEDformer, TimesNet y Pyraformer. **Ninguna referencia trivial** (persistencia,
climatología) aparece en la comparación, de modo que las cifras no acotan cuánto del R² de
0.85 en temperatura mensual proviene del ciclo anual. Ver
`[[patterns/persistence-climatology-reference-baselines]]`.
