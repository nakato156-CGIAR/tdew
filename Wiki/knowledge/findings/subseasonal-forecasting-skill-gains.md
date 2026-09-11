---
type: Finding
title: Ganancias de skill del ensemble MultiLLR+AutoKNN vs. CFSv2
description: El ensemble de Hwang et al. mejora 40-50% (temperatura) y 129-169% (precipitación) sobre CFSv2 debiased en 2011-2018, y supera al ganador del Subseasonal Rodeo 2017-2018.
resource: https://arxiv.org/abs/1809.07394
tags: [benchmark, forecasting, evaluation]
timestamp: 2026-09-11T15:57:37Z
status: draft
contributed_by: [claude]
sources: ["[[sources/subseasonal-forecasting-western-us-ml]]"]
---

# Ganancias de skill del ensemble MultiLLR+AutoKNN vs. CFSv2

Resultados empíricos reportados para `[[methods/multitask-regression-ensemble-subseasonal]]`
entrenado sobre `[[tools/subseasonalrodeo-dataset]]`.

## Período de concurso (2017-2018, 26 pronósticos bisemanales, "Subseasonal Rodeo")

| Tarea | Skill del ensemble | Skill CFSv2 (debiased) |
|---|---|---|
| Temperatura semanas 3-4 | 0.345 | 0.159 |
| Precipitación semanas 3-4 | 0.236 | 0.071 |

El ensemble superó al competidor ganador del Rodeo en las cuatro tareas evaluadas
(temperatura y precipitación, semanas 3-4 y 5-6).

## Período histórico (2011-2018)

- Mejora sobre CFSv2 debiased: 40-50% en temperatura, 129-169% en precipitación.
- Ensemble combinado con CFSv2: skill 0.357 (temperatura semanas 3-4), 0.186
  (precipitación semanas 5-6).

## Advertencia

Cifras extraídas vía asistencia de IA a partir del abstract/HTML del paper (el PDF no pudo
procesarse directamente). Validar contra el texto original antes de citar en trabajo
downstream.
