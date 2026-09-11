---
type: Source
title: WeatherNext 3 (Google DeepMind)
description: Página de producto de Google DeepMind sobre WeatherNext 3, modelo de IA para pronóstico meteorológico global horario.
resource: https://deepmind.google/science/weathernext/
tags: [weather-forecasting, deep-learning, google-deepmind, ai-for-science]
timestamp: 2026-09-11T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: []
---

# WeatherNext 3 — Google DeepMind

Fuente: página de producto/anuncio de Google DeepMind (no es un paper académico ni
tiene autoría individual listada). Describe **WeatherNext 3**, un modelo de IA para
pronóstico meteorológico global que genera predicciones cada hora del día procesando
imágenes satelitales directamente, en vez de depender solo de predicción numérica del
clima (NWP) tradicional.

Puntos clave:

- Primer modelo global del clima con pronósticos horarios (no solo actualizaciones
  periódicas).
- Predice temperatura y humedad en estaciones a 5km de resolución, viento y otras
  variables de superficie a 10km.
- Generaliza a ubicaciones no vistas en entrenamiento.
- Disponible vía BigQuery, Earth Engine, Google Maps Platform, Google Cloud Storage,
  y la plataforma experimental "Weather Lab"; integrado en Search, Maps y Gemini.
- Caso de uso: apoyo al National Hurricane Center durante el huracán Melissa.

No incluye metodología detallada ni benchmarks cuantitativos contra otros sistemas
(p.ej. HRES) — para eso se necesitaría ingerir el paper técnico o la documentación de
desarrolladores por separado.

Ver captura completa en [[../../raw/urls/deepmind-weathernext]].
