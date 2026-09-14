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
- [[methods/interpolate-first-calculate-later-eto]] — Estrategia IC + interpolación climatológicamente asistida para ETo grillada (FAO Penman-Monteith). `draft`

## Tools
- [[tools/subseasonalrodeo-dataset]] — Dataset SubseasonalRodeo. `reviewed`
- [[tools/weathernext-3]] — Modelo global de pronóstico horario de Google DeepMind. `reviewed`
- [[tools/piscop-h-dataset]] — PISCOp_h, dataset grillado de precipitación horaria para Perú. `reviewed`
- [[tools/piscoeo-pm-dataset]] — PISCOeo_pm, dataset grillado de evapotranspiración de referencia (FAO Penman-Monteith) para Perú. `draft`

## Patterns

## Findings
- [[findings/subseasonal-forecasting-skill-gains]] — Ganancias de skill vs. CFSv2. `reviewed`
- [[findings/weathernext-hourly-forecasting]] — Pronóstico horario y generalización espacial de WeatherNext 3. `reviewed`
- [[findings/stgcn-vs-baselines-traffic]] — STGCN supera baselines de tráfico con menos parámetros y entrenamiento más rápido. `reviewed`
- [[findings/piscop-h-validation-results]] — Validación técnica de PISCOp_h: buen desempeño en centro/sur andino, peor en el norte. `reviewed`
- [[findings/piscoeo-pm-vs-global-products]] — PISCOeo_pm supera a CRU_TS, TerraClimate y ERA5-Land en validación independiente de ETo. `draft`

## Decisions

## Sources
- [[sources/subseasonal-forecasting-western-us-ml]] — Improving Subseasonal Forecasting in the Western U.S. with Machine Learning (arXiv:1809.07394). `reviewed`
- [[sources/deepmind-weathernext]] — WeatherNext 3 (Google DeepMind). `reviewed`
- [[sources/stgcn-traffic-forecasting]] — Spatio-Temporal Graph Convolutional Networks (IJCAI-18). `reviewed`
- [[sources/piscop-h-hourly-precipitation-peru]] — PISCOp_h: High-Resolution Gridded Hourly Precipitation Dataset for Peru (Data in Brief, 2022). `reviewed`
- [[sources/piscoeo-pm-reference-evapotranspiration-peru]] — PISCOeo_pm: reference evapotranspiration gridded database based on FAO Penman-Monteith in Peru (Scientific Data, 2022). `draft`
