---
type: Method
title: "Interpolar primero, calcular después (IC) + interpolación climatológicamente asistida para ETo"
description: Estrategia para estimar evapotranspiración de referencia (FAO Penman-Monteith) grillada cuando faltan subvariables meteorológicas en estaciones, interpolando cada subvariable espacialmente antes de aplicar la fórmula.
resource: https://doi.org/10.1038/s41597-022-01373-8
tags: [evapotranspiration, spatial-interpolation, gap-filling, homogenization, fao-penman-monteith, regression-kriging]
timestamp: 2026-09-14T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: ["[[sources/piscoeo-pm-reference-evapotranspiration-peru]]"]
---

# Interpolar primero, calcular después (IC) para ETo grillada

Estrategia usada por `[[tools/piscoeo-pm-dataset]]` para producir evapotranspiración de
referencia (ETo) grillada de alta resolución cuando no todas las subvariables requeridas por
FAO Penman-Monteith (FPM) están disponibles en cada estación meteorológica.

## Problema

FPM requiere temperatura máx/mín, radiación solar (vía horas de sol), presión de vapor real
(vía punto de rocío), y velocidad del viento — rara vez todas disponibles en una misma
estación. Dos alternativas comunes son problemáticas:

- **"Less demanding methods"** (p.ej. Hargreaves-Samani, solo con temperatura): la
  variabilidad y tendencias del ETo estimado dependen únicamente de temperatura, ignorando el
  resto de las subvariables.
- **Estimar subvariables faltantes con relaciones empíricas** (recomendaciones del documento
  FPM o entre variables): usa relaciones estacionarias derivadas empíricamente, que pueden
  dejar de ser válidas bajo cambio climático.

## Estrategia IC (interpolating first, calculating later)

En vez de estimar subvariables faltantes a partir de otras variables, se usan estaciones
**vecinas de la misma variable** para completar/interpolar espacio-temporalmente cada
subvariable por separado, y solo al final se aplica la fórmula FPM sobre los campos grillados
resultantes. Dos pasos:

1. Estimar cada subvariable faltante mediante interpolación espacial (usando información de
   la misma variable en estaciones cercanas).
2. Calcular FPM a partir de los campos grillados completos de todas las subvariables.

Hay evidencia (citada en el paper, de estudios en España, EE.UU., Reino Unido y otras
regiones) de que este enfoque produce mejores resultados que estimar subvariables faltantes
vía relaciones empíricas entre variables.

## Pipeline aplicado a cada subvariable (antes de interpolar)

1. **Control de calidad** (5 etapas): errores de codificación, rango físico, rango climático
   (outliers vía IQR), comparación con estaciones vecinas (percentile rank), inspección
   visual.
2. **Relleno de vacíos (gap-filling)**: usando estaciones vecinas con datos estandarizados
   (climatología diaria), con condiciones mínimas de años en común y correlación; búsqueda
   iterativa a distancias crecientes; uso de "estaciones virtuales" derivadas de ERA5-Land
   (corregidas por quantile mapping) cuando no hay suficientes estaciones reales cercanas.
3. **Homogenización**: standard normal homogeneity test (SNHT), en versión relativa (pairwise
   homogenization algorithm) cuando hay suficientes estaciones vecinas correlacionadas, o
   absoluta si no; aplicada a escala mensual y luego interpolada a escala diaria.

## Interpolación espacial: climatologically aided interpolation (CAI)

Divide la interpolación en 3 pasos para reducir costo computacional y preservar variabilidad
a escala nacional:

1. Interpolación espacial de **valores normales** (climatología, p.ej. 1981–2010) vía
   regression-kriging, usando covariables espaciales satelitales (LST, cobertura de nubes,
   elevación, longitud/latitud, índice de disección topográfica).
2. Interpolación espacial de **anomalías** respecto a los normales (mismas covariables + el
   índice de disección topográfica).
3. **Agregación** de normales + anomalías para obtener el valor real grillado.

Este mismo patrón (normales + anomalías + agregación) se usa también para el downscaling
espacial de temperatura (Tmax/Tmin), vía geographically weighted regression en vez de
regression-kriging.

## Aplicabilidad

Documentado para el caso peruano en terreno topográficamente complejo con red de estaciones
escasa y desigualmente distribuida, pero la estrategia (IC + CAI + normales/anomalías) es
generalizable a otras regiones con datos meteorológicos limitados para calcular ETo grillada
de alta resolución.
