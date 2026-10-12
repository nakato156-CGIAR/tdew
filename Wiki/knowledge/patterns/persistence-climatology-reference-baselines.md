---
type: Pattern
title: Persistencia y climatología como referencias obligatorias en pronóstico meteorológico
description: Reportar el error de "repetir el valor de ayer" y el de "usar la climatología del día" junto a cualquier modelo aprendido, porque sin ellas las métricas absolutas no acotan el aporte del modelo.
resource: https://arxiv.org/abs/2008.08626
tags: [benchmark, baselines, persistence, climatology, evaluation-protocol, weather-forecasting]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/resnet-weatherbench-pretrained-climate]]", "[[sources/htc-lstm-attn-multitarget-weather-bangladesh]]", "[[sources/xai-tcn-dew-point-forecasting-bangladesh]]"]
---

# Persistencia y climatología como referencias obligatorias

## El patrón

En pronóstico meteorológico, dos predictores sin parámetros acotan por abajo cualquier
resultado: la **persistencia** (el valor, o la anomalía, del paso anterior) y la
**climatología** (el valor medio histórico de ese día del año en ese punto). Ambos se
reportan junto al modelo aprendido, y el skill se expresa como reducción relativa de error
frente a uno de ellos.

WeatherBench los incorpora al benchmark: la tabla de resultados de
`[[sources/resnet-weatherbench-pretrained-climate]]` encabeza con Persistence, Climatology y
Weekly climatology antes de cualquier modelo físico o aprendido
(`[[findings/resnet-weatherbench-vs-ifs-baselines]]`), y el ACC se define por construcción
respecto a la climatología.

## Por qué importa cuál de las dos

No hay una referencia trivial universalmente más fuerte. En la misma tabla, persistencia
supera ampliamente a climatología en Z500, T850 y T2M a 3 días, mientras que en precipitación
ocurre lo contrario (climatología 2.36 mm frente a persistencia 3.23 mm). La referencia
adecuada depende de la autocorrelación de la variable y del horizonte.

## Contraejemplos observados

Dos de las fuentes ingeridas sobre pronóstico meteorológico con deep learning no reportan
ninguna referencia trivial y comparan solo contra otros modelos aprendidos:

- `[[sources/htc-lstm-attn-multitarget-weather-bangladesh]]` compara contra once modelos
  (LSTM, GRU, Conv1D, CNN-LSTM, ANN, DTR, CatBoost, Autoformer, FEDformer, TimesNet,
  Pyraformer) y reporta R² = 0.8527 en temperatura máxima **mensual**. Sobre series mensuales
  con ciclo anual marcado, la climatología por mes explica de por sí la mayor parte de la
  varianza, así que ese R² no separa el aporte del modelo del ciclo estacional.
- `[[sources/xai-tcn-dew-point-forecasting-bangladesh]]` compara contra LSTM, CNN, BiLSTM,
  LSTM-CNN y GRU, y reporta RMSE = 0.044 y MAE = 0.032 sobre punto de rocío en escala
  normalizada, sin persistencia ni climatología y sin explicitar la escala física.

En ambos casos las cifras no son comparables con las de un proyecto que sí reporta skill
relativo, y no permiten decidir si el modelo aporta algo sobre copiar el día anterior.

## Consecuencia para tdew

El leaderboard de baselines del proyecto (`reports/week1_baselines/leaderboard.csv`) ya sigue
este patrón: climatología, persistencia, dept_ols, dept_mlr y generalist_mlr se reportan por
sitio y agrupados, con `skill_vs_clim` explícito. Ese diseño es lo que permitió detectar, en
septiembre de 2026, que el TCN con atención entrenado sobre `Data/gold/model_features_norm`
quedaba por debajo de la persistencia en los cuatro departamentos del protocolo — un
diagnóstico imposible de alcanzar con el estilo de reporte de las dos fuentes anteriores.
