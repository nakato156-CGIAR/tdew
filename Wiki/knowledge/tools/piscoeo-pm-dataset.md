---
type: Tool
title: PISCOeo_pm
description: Dataset grillado de evapotranspiración de referencia (FAO Penman-Monteith) para Perú (0.01°, 1981–2016, NetCDF) desarrollado por SENAMHI.
resource: https://doi.org/10.6084/m9.figshare.19686738.v1
tags: [evapotranspiration, gridded-dataset, peru, netcdf, senamhi, fao-penman-monteith]
timestamp: 2026-09-14T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/piscoeo-pm-reference-evapotranspiration-peru]]"]
---

# PISCOeo_pm

Dataset grillado de evapotranspiración de referencia (ETo) para todo el territorio
continental peruano, desarrollado por SENAMHI (Huerta et al., 2022). Calculado con la fórmula
FAO Penman-Monteith (FPM) a partir de subvariables meteorológicas grilladas. Distribuido en
formato NetCDF.

## Características

- **Resolución espacial**: ~1 km (0.01°), todo el territorio continental de Perú.
- **Resolución temporal**: diaria y normal (climatología mensual).
- **Período**: 1981–2016.
- **Insumos**: temperatura máxima/mínima (de `[[tools/piscop-h-dataset|familia PISCO]]`,
  concretamente PISCOt, vía downscaling espacial), duración de horas de sol, temperatura de
  punto de rocío, y velocidad del viento — procesados vía control de calidad, relleno de
  vacíos, homogenización e interpolación espacial (ver
  `[[methods/interpolate-first-calculate-later-eto]]`).
- **Repositorios de datos**: Figshare, https://doi.org/10.6084/m9.figshare.c.5633182.v3 y
  https://doi.org/10.6084/m9.figshare.19686738.v1.
- **Código**: https://github.com/adrHuerta/PISCOeo_pm (R 3.6.3 + Python 3.8.5), licencia GNU
  GPL v3.

## Datos adicionales incluidos

Además de ETo, el dataset publica las subvariables grilladas intermedias (Tmax, Tmin,
duración de sol, punto de rocío, velocidad del viento) en valores diarios y normales —
útiles para otras aplicaciones, aunque su validación técnica no fue el foco del paper.

## Desempeño y limitaciones

Ver `[[findings/piscoeo-pm-vs-global-products]]` para el detalle de la validación
independiente y comparación con productos globales (CRU_TS, TerraClimate, ERA5-Land). En
resumen: mejor precisión que los tres productos globales en escalas diaria/mensual, con menor
desempeño en la costa (Pacific Coast) y a escala anual (acumulación de sesgos). No incluye
corrección por respuesta estomática a CO2 creciente — posible sesgo en años recientes. Los
grids sobre cuerpos de agua deben considerarse vacíos/enmascarados.

## Relevancia para tdew

Único dataset grillado de alta resolución de evapotranspiración de referencia para Perú;
insumo potencial directo para el pipeline de tdew (estimación de variables meteorológicas
derivadas / balance hídrico). Comparte linaje metodológico y de autoría con
`[[tools/piscop-h-dataset]]` (mismo grupo SENAMHI, misma familia de productos PISCO). No se
ha verificado en esta captura si tdew ya usa PISCOeo_pm o PISCOt como insumo — pendiente de
contrastar con `MODEL_INPUTS.md`/`pipeline/` del repo si aplica.
