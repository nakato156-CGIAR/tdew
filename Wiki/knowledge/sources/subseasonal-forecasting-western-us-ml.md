---
type: Source
title: "Improving Subseasonal Forecasting in the Western U.S. with Machine Learning"
description: Paper de Hwang et al. (arXiv 1809.07394) sobre un ensemble de regresión (MultiLLR + AutoKNN) para pronóstico subestacional de temperatura y precipitación.
resource: https://arxiv.org/abs/1809.07394
tags: [machine-learning, forecasting, ensemble, regression, climate]
timestamp: 2026-09-11T15:57:37Z
status: draft
contributed_by: [claude]
sources: []
---

# Improving Subseasonal Forecasting in the Western U.S. with Machine Learning

Ver captura completa en `[[raw/papers/subseasonal-forecasting-western-us-ml]]`.

## Resumen

Hwang, Orenstein, Cohen, Pfeiffer y Mackey (arXiv:1809.07394) proponen un ensemble de dos
modelos de regresión no lineal — MultiLLR y AutoKNN — para predecir temperatura y
precipitación en el occidente de EE.UU. con 2 a 6 semanas de anticipación. El ensemble
mejora sustancialmente sobre el sistema operativo CFSv2 (debiased): 40-50% en temperatura
y 129-169% en precipitación durante 2011-2018, y superó al ganador del "Subseasonal
Rodeo" 2017-2018 en las cuatro tareas evaluadas. También publican el dataset abierto
SubseasonalRodeo.

**Nota de dominio**: este paper trata de machine learning clásico aplicado a pronóstico
meteorológico, no de LLMs. Se ingiere a pedido explícito del usuario aunque está fuera del
foco declarado de esta wiki (ver CLAUDE.md).

## Conceptos derivados

- `[[methods/multitask-regression-ensemble-subseasonal]]` — la técnica de ensemble MultiLLR + AutoKNN.
- `[[tools/subseasonalrodeo-dataset]]` — el dataset abierto compilado por los autores.
- `[[findings/subseasonal-forecasting-skill-gains]]` — las mejoras de skill reportadas vs. CFSv2.
