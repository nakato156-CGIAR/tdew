---
type: Tool
title: WeatherNext 3
description: Modelo de IA de Google DeepMind para pronóstico meteorológico global, con predicciones cada hora del día a partir de imágenes satelitales.
resource: https://deepmind.google/science/weathernext/
tags: [weather-forecasting, deep-learning, google-deepmind, satellite-data]
timestamp: 2026-09-11T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: ["[[sources/deepmind-weathernext]]"]
---

# WeatherNext 3

Modelo de ensamble de Google DeepMind que procesa imágenes satelitales crudas
directamente para producir pronósticos meteorológicos globales, en vez de depender
solo de predicción numérica del clima (NWP) tradicional.

## Características

- Genera pronósticos **cada hora del día** (no en ciclos periódicos como los sistemas
  NWP tradicionales).
- Resolución espacial: temperatura y humedad en estaciones a 5km, viento y otras
  variables de superficie a 10km.
- Generaliza a ubicaciones no vistas durante el entrenamiento.

## Acceso

- Vía BigQuery, Earth Engine, Google Maps Platform, Google Cloud Storage.
- Documentación de desarrolladores: developers.google.com/weathernext/guides/models
- Plataforma experimental: "Weather Lab".
- Integrado en Google Search, Maps y Gemini.

## Relación con [[tools/subseasonalrodeo-dataset]]

Ambos abordan pronóstico meteorológico con ML, pero en horizontes distintos:
SubseasonalRodeo se enfoca en pronóstico subestacional (semanas a meses) con modelos
clásicos de regresión/ensamble sobre EE.UU. occidental, mientras que WeatherNext 3 es
un modelo global de deep learning orientado a pronóstico de corto plazo (horario).
No hay contradicción entre ambos — cubren problemas y escalas distintas.

## Limitaciones de esta entrada

La fuente es material de producto, sin metodología detallada ni benchmarks
cuantitativos publicados en la misma página (p.ej. contra HRES). Validar cifras de
precisión contra el paper técnico o la documentación de desarrolladores antes de
citarlas en trabajo serio.
