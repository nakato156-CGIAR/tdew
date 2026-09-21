---
type: Method
title: Resnet convolucional con preentrenamiento climático para pronóstico de medio plazo
description: Red totalmente convolucional de 19 bloques residuales entrenada en modo direct o continuous sobre WeatherBench, preentrenada con 150 años de salida CMIP y ajustada sobre reanálisis ERA.
resource: https://arxiv.org/abs/2008.08626
tags: [resnet, residual-connections, weather-forecasting, transfer-learning, weatherbench, convolutional-networks]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/resnet-weatherbench-pretrained-climate]]"]
---

# Resnet con preentrenamiento climático (Rasp y Thuerey, JAMES 2020)

## Arquitectura

Red totalmente convolucional con 19 bloques residuales. Cada bloque son dos bloques
convolucionales `[conv 2D -> LeakyReLU -> BatchNorm -> Dropout]`, tras los cuales la entrada
del bloque se suma a la señal. Las convoluciones internas tienen 128 canales y kernel 3; la
primera capa usa kernel 7 para ampliar el campo de visión. Las convoluciones son periódicas
en longitud y usan zero padding en latitud, respetando la geometría del globo. LeakyReLU con
α = 0.3, weight decay 1e-5, dropout 0.1 (omitido en el modelo preentrenado).

## Las tres estrategias de pronóstico

Los autores distinguen explícitamente tres formas de construir un pronóstico data-driven, y
entrenan las dos primeras:

- **Direct**: un modelo entrenado por cada horizonte deseado (aquí 6 h, 1 d, 3 d, 5 d).
- **Continuous**: el horizonte entra como canal adicional (campo 32×64 con las horas
  divididas entre 100) y un solo modelo cubre todos los horizontes; durante el entrenamiento
  se sortea un horizonte entre 6 y 120 h por muestra.
- **Iterative**: modelo de paso corto aplicado repetidamente sobre su propia salida
  (la estrategia de Weyn et al., 2020, no usada aquí).

## Preentrenamiento

El modelo se entrena primero con 150 años de salida de modelo climático (CMIP) y luego se
ajusta sobre ERA (1979-2015, validación en 2016) con learning rate inicial reducido de 5e-5
a 5e-7. La justificación es regularización, no falta de datos: el sobreajuste empeora con el
horizonte porque la atmósfera se vuelve más caótica y un modelo entrenado con MSE debe
estimar la media de una distribución cada vez más ancha, lo que requiere más datos. Los
modelos entrenados solo con CMIP, sin ver reanálisis, obtienen scores de test sobre ERA
apenas peores o iguales que los entrenados solo con ERA.

## Detalles de preprocesamiento que los autores marcan como determinantes

- La log-transformación de la precipitación `ln(ε + PR) − ln(ε)` con ε = 0.001, sin restar la
  media, es calificada de decisiva para evitar que la red prediga simplemente ceros.
- Z500/T850/T2M y precipitación se predicen con redes separadas; una sola red para las cuatro
  variables "llevó a malas predicciones para todas".
- La pérdida es MSE ponderado por latitud (peso ∝ cos φ), para que el área de cada celda
  pese proporcionalmente.

Resultados en `[[findings/resnet-weatherbench-vs-ifs-baselines]]`.
