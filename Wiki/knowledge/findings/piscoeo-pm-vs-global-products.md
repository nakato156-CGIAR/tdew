---
type: Finding
title: PISCOeo_pm supera a CRU_TS, TerraClimate y ERA5-Land en validación independiente de ETo en Perú
description: Validación independiente (train/test, 39 estaciones) muestra que PISCOeo_pm tiene mejor precisión (dr, bias, MAE) que tres productos globales de evapotranspiración de referencia, salvo a escala anual.
resource: https://doi.org/10.1038/s41597-022-01373-8
tags: [evapotranspiration, validation, benchmark, peru, cru_ts, terraclimate, era5-land]
timestamp: 2026-09-14T00:00:00Z
status: reviewed
contributed_by: [claude]
sources: ["[[sources/piscoeo-pm-reference-evapotranspiration-peru]]"]
---

# PISCOeo_pm vs. productos globales de ETo (CRU_TS, TerraClimate, ERA5-Land)

## Metodología de validación

Train/test split: 39 estaciones meteorológicas con todas las subvariables disponibles
("ETo_conventional") apartadas como test; el resto usado para reconstruir el producto
("PISCOeo_pm_for_cv", peor escenario que el producto final por tener menos estaciones).
Métricas: bias, MAE (error absoluto medio), y dr (índice de acuerdo refinado; dr>0.5 indica
poder predictivo mayor al promedio observado).

## Resultados (mediana de métricas, Tabla 4 del paper)

| Producto | Escala | bias (mm) | MAE (mm) | dr |
|---|---|---|---|---|
| PISCOeo_pm_for_cv | diaria | 0.08 | 0.52 | **0.67** |
| ERA5-Land | diaria | −0.22 | 0.69 | 0.55 |
| PISCOeo_pm_for_cv | mensual | 2.39 | 11.7 | **0.66** |
| ERA5-Land | mensual | −6.7 | 16.18 | 0.54 |
| CRU_TS | mensual | −14.3 | 16.18 | 0.37 |
| TerraClimate | mensual | −16.51 | 16.75 | 0.35 |
| PISCOeo_pm_for_cv | anual | 28.67 | 80.46 | −0.06 |
| ERA5-Land | anual | −80.42 | 162.13 | −0.45 |
| TerraClimate | anual | −198.18 | 198.18 | −0.51 |
| CRU_TS | anual | −171.55 | 182.75 | −0.53 |

- PISCOeo_pm_for_cv tiene el mejor desempeño (dr>0.5) en todas las escalas de agregación
  excepto la anual, donde **ningún** producto supera dr=0.5 (acumulación de sesgos diarios).
- Orden jerárquico de mejor a peor desempeño (validación independiente): PISCOeo_pm_for_cv >
  ERA5-Land > TerraClimate > CRU_TS.
- Espacialmente, el desempeño es más débil en estaciones de la costa (Pacific Coast) que en
  los Andes.

## Comparación regional con productos globales (PISCOeo_pm completo)

Por región climática (Pacific Coast/PC, High Amazon/HA, Low Amazon/LA, Western Andes/WA,
Eastern Andes/EA), a escala diaria y mensual (1981–2016):

- Los tres productos globales **subestiman sistemáticamente** ETo respecto a PISCOeo_pm en
  todas las regiones, con las mayores diferencias en PC y WA (zonas áridas/semiáridas).
- ERA5-Land es el producto más cercano a PISCOeo_pm en magnitud y patrón espacial en general
  (PC, HA, LA, EA); CRU_TS sigue mejor la señal estacional mensual en HA y EA.
- A escala anual, los tres productos globales muestran dr negativo en todas las regiones
  (alta disimilitud).
- Las diferencias tienden a aumentar de este (Amazonía, húmedo) a oeste (Pacífico, árido),
  consistente con literatura previa a escala global (Singer et al. 2021).
- Análisis de tendencias (Sen's slope, 1981–2016): PISCOeo_pm muestra tendencias positivas
  significativas en todas las regiones salvo PC. ERA5-Land es el producto que mejor preserva
  magnitud y dirección de esas tendencias (salvo en LA, donde CRU_TS se acerca más);
  TerraClimate difiere en dirección de tendencia en casi todas las regiones — el paper nota
  que TerraClimate no fue diseñado para este tipo de análisis de tendencias.

## Posibles causas de discrepancia (discutidas por los autores)

- Baja resolución espacial de CRU_TS (0.5°) no representa bien el terreno complejo de Perú.
- Sesgos en la estimación de radiación solar en TerraClimate y ERA5-Land — la literatura
  citada indica que los errores de radiación solar tienen el mayor impacto relativo en los
  errores de ETo (más que viento o humedad).
- PISCOeo_pm aplica un proceso de homogenización previo a la interpolación, poco común en
  productos globales, lo que podría explicar su mejor preservación de tendencias.

## Incertidumbre de PISCOeo_pm

Estimada vía propagación de errores (finite differences) de la fórmula FPM, a escala de
grilla y diaria: mayor incertidumbre en la costa (hasta 2.75 mm/día) y, en menor medida, en
la Amazonía (1.5–2.25 mm/día); menor en el norte/centro de los Andes (0–1 mm/día). Esta
incertidumbre solo cubre la fórmula FPM en sí — no incluye errores de las etapas previas
(control de calidad, gap-filling, homogenización, interpolación, downscaling).

## Limitación declarada

La validación técnica se enfocó en ETo; las subvariables individuales (Sd, Td, Ws) no fueron
validadas de forma independiente más allá del gap-filling (ver
`[[methods/interpolate-first-calculate-later-eto]]`). Tampoco se corrigió por el efecto de la
respuesta estomática a concentraciones crecientes de CO2 (asunción de resistencia superficial
mínima fija en FPM), lo que podría introducir sesgo en los años más recientes del dataset.
