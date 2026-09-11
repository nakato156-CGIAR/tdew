---
type: Finding
title: Pronóstico horario y generalización espacial de WeatherNext 3
description: WeatherNext 3 reporta pronósticos globales cada hora y buena generalización a ubicaciones no vistas en entrenamiento, sin cifras cuantitativas publicadas en la fuente.
resource: https://deepmind.google/science/weathernext/
tags: [weather-forecasting, deep-learning, benchmarks]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/deepmind-weathernext]]"]
---

# Pronóstico horario y generalización espacial de WeatherNext 3

Según la página de producto de Google DeepMind, [[tools/weathernext-3]] logra:

1. Ser "el primer modelo global del clima que genera pronósticos cada hora del día",
   a diferencia de los ciclos de actualización periódicos de los sistemas NWP
   tradicionales.
2. Predecir temperatura y humedad en estaciones a 5km de resolución, y viento y otras
   variables de superficie a 10km.
3. Mantener pronósticos precisos "incluso en ubicaciones que el modelo no vio durante
   el entrenamiento" (generalización espacial).

**Advertencia:** la fuente no publica métricas cuantitativas de error/skill ni
comparación directa contra HRES u otros sistemas de referencia — estas afirmaciones son
las que reporta la propia página de producto, sin benchmark verificable adjunto. No
citar como validación independiente sin cruzar contra el paper técnico o la
documentación de desarrolladores.
