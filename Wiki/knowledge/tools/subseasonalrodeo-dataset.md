---
type: Tool
title: SubseasonalRodeo (dataset)
description: Dataset abierto que combina temperatura/precipitación CPC, SST/hielo marino, índices climáticos (MEI, MJO), reanálisis NCEP y pronósticos NMME para pronóstico subestacional del occidente de EE.UU.
resource: https://arxiv.org/abs/1809.07394
tags: [dataset, climate, forecasting]
timestamp: 2026-09-11T15:57:37Z
status: draft
contributed_by: [claude]
sources: ["[[sources/subseasonal-forecasting-western-us-ml]]"]
---

# SubseasonalRodeo (dataset)

Compilación de datos publicada junto con `[[sources/subseasonal-forecasting-western-us-ml]]`
para entrenar y evaluar modelos de pronóstico subestacional (2-6 semanas) de temperatura y
precipitación.

## Contenido

- Temperatura y precipitación: CPC (NOAA)
- Anomalías de temperatura superficial del mar (SST) y hielo marino: NOAA OISSTv2
- Índices climáticos: MEI (ENSO), MJO
- Reanálisis atmosférico: NCEP
- Pronósticos dinámicos: NMME, CFSv2

## Cobertura

Región oeste de EE.UU., 25°N-50°N, 125°W-93°W, resolución espacial 1°×1°.

## Uso

Sirvió como base de entrenamiento/evaluación para `[[methods/multitask-regression-ensemble-subseasonal]]`
y para la competencia "Subseasonal Rodeo" 2017-2018 referenciada en
`[[findings/subseasonal-forecasting-skill-gains]]`.
