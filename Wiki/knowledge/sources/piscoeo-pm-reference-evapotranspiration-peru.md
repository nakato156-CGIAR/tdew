---
type: Source
title: "PISCOeo_pm, a reference evapotranspiration gridded database based on FAO Penman-Monteith in Peru"
description: Paper de Huerta et al. (SENAMHI, Scientific Data 2022) que documenta PISCOeo_pm, un dataset grillado de evapotranspiración de referencia (FAO Penman-Monteith) para Perú (1981–2016, ~1 km).
resource: https://doi.org/10.1038/s41597-022-01373-8
tags: [evapotranspiration, hydrology, peru, gridded-dataset, senamhi, netcdf, fao-penman-monteith]
timestamp: 2026-09-14T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: []
---

# PISCOeo_pm (Scientific Data, 2022)

Ver captura completa en `[[raw/papers/piscoeo-pm-reference-evapotranspiration-peru]]`.

## Resumen

Huerta, Bonnesoeur, Cuadros-Adriazola, Gutierrez, Ochoa-Tocachi, Román-Dañobeytia y
Lavado-Casimiro (SENAMHI/CONDESAN/iMHEA/Imperial College London) documentan PISCOeo_pm, un
dataset grillado de evapotranspiración de referencia (ETo) para Perú (~1 km / 0.01°,
1981–2016), calculado con la fórmula FAO Penman-Monteith a partir de subvariables
meteorológicas grilladas (Tmax, Tmin, duración de sol, punto de rocío, velocidad del viento)
procesadas vía control de calidad, relleno de vacíos, homogenización e interpolación espacial
climatológicamente asistida ("interpolating first, calculating later"). En validación
independiente, PISCOeo_pm supera en precisión a CRU_TS, TerraClimate y ERA5-Land a escalas
diaria, mensual y normal mensual.

**Nota de dominio**: paper de ciencia de datos climáticos/hidrológicos (no de LLMs), pero
directamente relevante para tdew: es el único dataset grillado de alta resolución de
evapotranspiración de referencia para Perú, insumo potencial clave para el pipeline de tdew.

## Nota de acceso

PDF provisto directamente por el usuario (`s41597-022-01373-8.pdf`), leído sin necesidad de
WebFetch. Artículo Open Access (CC BY 4.0).

## Conceptos derivados

- `[[tools/piscoeo-pm-dataset]]` — el dataset grillado en sí (NetCDF, 0.01°, diario/normal,
  1981–2016).
- `[[methods/interpolate-first-calculate-later-eto]]` — la estrategia IC (interpolar primero,
  calcular después) + interpolación climatológicamente asistida para estimar ETo cuando
  faltan subvariables.
- `[[findings/piscoeo-pm-vs-global-products]]` — resultados de validación independiente y
  comparación con CRU_TS, TerraClimate y ERA5-Land.
