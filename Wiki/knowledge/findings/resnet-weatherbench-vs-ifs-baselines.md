---
type: Finding
title: La Resnet preentrenada con CMIP alcanza el nivel de IFS T63 en WeatherBench
description: RMSE de 268/523 m²s⁻² (Z500) y 1.65/2.52 K (T850) a 3/5 días, frente a 936/1033 y 4.23/4.56 de persistencia y 268/463 y 1.85/2.52 del modelo físico IFS T63.
resource: https://arxiv.org/abs/2008.08626
tags: [benchmark, weatherbench, resnet, persistence-baseline, climatology-baseline, transfer-learning]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/resnet-weatherbench-pretrained-climate]]"]
---

# Resnet preentrenada frente a baselines triviales y físicos en WeatherBench

Resultados de `[[methods/resnet-direct-continuous-weather-forecasting]]`, RMSE ponderado por
latitud a 3 y 5 días, todo evaluado a 5.625°.

| Modelo | Z500 [m²s⁻²] | T850 [K] | T2M [K] | PR [mm] |
|---|---|---|---|---|
| Persistence | 936 / 1033 | 4.23 / 4.56 | 3.00 / 3.27 | 3.23 / 3.24 |
| Climatology | 1075 | 5.51 | 6.07 | 2.36 |
| Weekly climatology | 816 | 3.50 | 3.19 | 2.32 |
| IFS T42 | 489 / 743 | 3.09 / 3.83 | 3.21 / 3.69 | |
| IFS T63 | 268 / 463 | 1.85 / 2.52 | 2.04 / 2.44 | |
| Operational IFS | 154 / 334 | 1.36 / 2.03 | 1.35 / 1.77 | 2.36 / 2.59 |
| Weyn et al. (2020) | 373 / 611 | 1.98 / 2.87 | | |
| Direct (ERA only) | 314 / 561 | 1.79 / 2.82 | 1.53 / 2.32 | 2.03 / 2.35 |
| Direct (CMIP only) | 323 / 561 | 2.09 / 2.82 | 1.90 / 2.32 | 2.30 / 2.39 |
| Direct (pretrained) | 268 / 523 | 1.65 / 2.52 | 1.42 / 2.03 | 2.16 / 2.30 |
| Continuous (ERA only) | 331 / 545 | 1.87 / 2.57 | 1.60 / 2.06 | 2.22 / 2.32 |
| Continuous (CMIP only) | 330 / 548 | 2.12 / 2.75 | 2.24 / 2.59 | 2.29 / 2.38 |
| Continuous (pretrained) | 284 / 499 | 1.72 / 2.41 | 1.48 / 1.92 | 2.23 / 2.33 |

## Lecturas

- El preentrenamiento con CMIP mejora Z500, T850 y T2M de forma creciente con el horizonte
  (Direct pasa de 314/561 a 268/523 en Z500), y los autores lo atribuyen a que el sobreajuste
  crece con el horizonte por la naturaleza caótica de la atmósfera.
- Para precipitación el preentrenamiento no ayuda, y los autores advierten que RMSE y ACC son
  métricas subóptimas para esa variable.
- El margen entre persistencia y climatología depende de la variable y el horizonte:
  persistencia gana en Z500, T850 y T2M, mientras que en precipitación la climatología
  (2.36) supera a persistencia (3.23). La referencia trivial "correcta" no es la misma para
  todas las variables.
- En ACC (tabla A1 del apéndice) la climatología queda en 0 por construcción y persistencia
  en 0.62/0.53 (Z500) y 0.69/0.65 (T850).
