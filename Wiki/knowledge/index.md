---
type: Source
title: Índice de knowledge/
description: Catálogo de todos los conceptos de la wiki, actualizado por /ingest, /reconcile y /update.
status: stable
---

# Índice

## Methods
- [[methods/multitask-regression-ensemble-subseasonal]] — Ensemble MultiLLR + AutoKNN para pronóstico subestacional. `reviewed`
- [[methods/stgcn-graph-conv-forecasting]] — STGCN: convolución de grafos + convolución temporal con compuertas para pronóstico de tráfico. `reviewed`
- [[methods/precipitation-temporal-disaggregation]] — Desagregación temporal de precipitación diaria a horaria (satélite + AWS + quantile mapping). `reviewed`
- [[methods/interpolate-first-calculate-later-eto]] — Estrategia IC + interpolación climatológicamente asistida para ETo grillada (FAO Penman-Monteith). `reviewed`
- [[methods/attention-tcn-explainable-forecasting]] — TCN con atención + XAI para pronóstico de punto de rocío. `draft`
- [[methods/resnet-direct-continuous-weather-forecasting]] — Resnet de 19 bloques residuales con preentrenamiento sobre salidas de modelo climático (WeatherBench). `draft`
- [[methods/htc-bilstm-attention-multitarget]] — HTC-LSTM-Attn: Conv1D jerárquicas + BiLSTM + atención, con hold-out espacial. `draft`
- [[methods/temporal-residual-connections-rnn]] — Conexiones residuales en la dimensión temporal de redes recurrentes. `draft`

## Tools
- [[tools/subseasonalrodeo-dataset]] — Dataset SubseasonalRodeo. `reviewed`
- [[tools/weathernext-3]] — Modelo global de pronóstico horario de Google DeepMind. `reviewed`
- [[tools/piscop-h-dataset]] — PISCOp_h, dataset grillado de precipitación horaria para Perú. `reviewed`
- [[tools/piscoeo-pm-dataset]] — PISCOeo_pm, dataset grillado de evapotranspiración de referencia (FAO Penman-Monteith) para Perú. `reviewed`

## Patterns
- [[patterns/persistence-climatology-reference-baselines]] — Persistencia y climatología como referencias obligatorias en pronóstico meteorológico. `draft`

## Findings
- [[findings/subseasonal-forecasting-skill-gains]] — Ganancias de skill vs. CFSv2. `reviewed`
- [[findings/weathernext-hourly-forecasting]] — Pronóstico horario y generalización espacial de WeatherNext 3. `reviewed`
- [[findings/stgcn-vs-baselines-traffic]] — STGCN supera baselines de tráfico con menos parámetros y entrenamiento más rápido. `reviewed`
- [[findings/piscop-h-validation-results]] — Validación técnica de PISCOp_h: buen desempeño en centro/sur andino, peor en el norte. `reviewed`
- [[findings/piscoeo-pm-vs-global-products]] — PISCOeo_pm supera a CRU_TS, TerraClimate y ERA5-Land en validación independiente de ETo. `reviewed`
- [[findings/xai-tcn-dew-point-performance]] — Métricas (test/validation loss, MAE, RMSE, R²) y baselines del TCN+atención para punto de rocío en Bangladesh. `draft`
- [[findings/resnet-weatherbench-vs-ifs-baselines]] — La Resnet preentrenada con CMIP alcanza el nivel de IFS T63 en WeatherBench. `draft`
- [[findings/htc-lstm-attn-bangladesh-metrics]] — HTC-LSTM-Attn: métricas en test temporal y hold-out espacial (Bangladesh). `draft`

## Decisions

## Sources
- [[sources/subseasonal-forecasting-western-us-ml]] — Improving Subseasonal Forecasting in the Western U.S. with Machine Learning (arXiv:1809.07394). `reviewed`
- [[sources/deepmind-weathernext]] — WeatherNext 3 (Google DeepMind). `reviewed`
- [[sources/stgcn-traffic-forecasting]] — Spatio-Temporal Graph Convolutional Networks (IJCAI-18). `reviewed`
- [[sources/piscop-h-hourly-precipitation-peru]] — PISCOp_h: High-Resolution Gridded Hourly Precipitation Dataset for Peru (Data in Brief, 2022). `reviewed`
- [[sources/piscoeo-pm-reference-evapotranspiration-peru]] — PISCOeo_pm: reference evapotranspiration gridded database based on FAO Penman-Monteith in Peru (Scientific Data, 2022). `reviewed`
- [[sources/xai-tcn-dew-point-forecasting-bangladesh]] — Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks (IEEE Access, 2025). `draft`
- [[sources/resnet-weatherbench-pretrained-climate]] — Data-driven medium-range weather prediction with a Resnet pretrained on climate simulations (Rasp y Thuerey, JAMES 2020). `draft`
- [[sources/htc-lstm-attn-multitarget-weather-bangladesh]] — Redefining multi-target weather forecasting with HTC-LSTM-Attn (Kabir y Chakma, PLOS ONE 2026). `draft`
- [[sources/residual-echo-state-networks]] — Residual Echo State Networks (Ceni y Gallicchio, Neurocomputing 2024). `draft`
