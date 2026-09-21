---
type: Source
title: "Data-driven medium-range weather prediction with a Resnet pretrained on climate simulations: A new model for WeatherBench"
description: Paper de Rasp y Thuerey (JAMES, 2020) que entrena una Resnet de 19 bloques residuales sobre WeatherBench, preentrenada con salidas de modelo climático y ajustada sobre reanálisis.
resource: https://arxiv.org/abs/2008.08626
tags: [weather-forecasting, deep-learning, resnet, residual-connections, weatherbench, benchmark, persistence-baseline, transfer-learning]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# Resnet preentrenada con simulaciones climáticas para WeatherBench (JAMES, 2020)

Ver captura completa en `[[raw/papers/resnet-weatherbench-pretrained-climate]]`.

## Resumen

Rasp y Thuerey entrenan una red convolucional residual (19 bloques residuales, 128 canales,
kernel 3, convoluciones periódicas en longitud) para predecir geopotencial en 500 hPa,
temperatura en 850 hPa, temperatura a 2 m y precipitación a resolución 5.625° con horizontes
de hasta 5 días, sobre el benchmark WeatherBench. La contribución metodológica central es el
preentrenamiento con 150 años de salida de modelo climático (CMIP) antes del fine-tuning
sobre reanálisis ERA (1979-2015), justificado como regularización: el sobreajuste empeora
con el horizonte de pronóstico porque la atmósfera se vuelve más caótica y un modelo
entrenado con MSE debe estimar la media de una distribución cada vez más ancha. El modelo
preentrenado alcanza RMSE de 268/523 m²s⁻² en Z500 y 1.65/2.52 K en T850 a 3/5 días,
comparable al modelo físico IFS T63 y muy por encima de las submisiones previas a
WeatherBench.

**Nota de dominio**: relevante para tdew en dos frentes. Primero, la tabla de resultados
encabeza con persistencia, climatología y climatología semanal como referencias triviales
obligatorias, el mismo criterio que usa el leaderboard de baselines del proyecto
(`reports/week1_baselines/leaderboard.csv`). Segundo, la arquitectura es enteramente
residual: la entrada de cada bloque se suma a su salida, y los autores reportan que los
experimentos con cambios de dimensionalidad rindieron peor que la Resnet simple.

## Precisión sobre el uso del término "residual"

El trabajo usa bloques residuales **dentro de la red** (He et al., 2015). No predice el
incremento respecto a un estado previo ni corrige una referencia climatológica: los modelos
`direct` y `continuous` predicen los campos completos y la climatología aparece solo como
baseline y como referencia para el cálculo de ACC.

## Conceptos derivados

- `[[methods/resnet-direct-continuous-weather-forecasting]]` — la arquitectura y las tres
  estrategias de construcción de pronóstico (direct / continuous / iterative) más el
  preentrenamiento con CMIP.
- `[[findings/resnet-weatherbench-vs-ifs-baselines]]` — la tabla de RMSE frente a
  persistencia, climatología, IFS y submisiones previas.
- `[[patterns/persistence-climatology-reference-baselines]]` — el uso de persistencia y
  climatología como referencias obligatorias.
