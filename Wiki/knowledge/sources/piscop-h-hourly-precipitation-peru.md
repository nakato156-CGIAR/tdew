---
type: Source
title: "PISCOp_h: High-Resolution Gridded Hourly Precipitation Dataset for Peru"
description: Paper de Huerta, Lavado-Casimiro y Felipe-Obando (SENAMHI, Data in Brief 2022) que documenta PISCOp_h, un dataset grillado horario de precipitación para Perú (2015–2020) obtenido por desagregación temporal.
resource: https://doi.org/10.1016/j.dib.2022.108570
tags: [precipitation, hydrology, peru, gridded-dataset, temporal-disaggregation, senamhi, netcdf]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# PISCOp_h (Data in Brief, 2022)

Ver captura completa en `[[raw/papers/piscop-h-hourly-precipitation-peru]]`.

## Resumen

Huerta, Lavado-Casimiro y Felipe-Obando (SENAMHI) documentan PISCOp_h, un dataset grillado
de precipitación horaria para Perú (0.1° de resolución espacial, 2015–2020), construido
mediante desagregación temporal del dataset diario PISCOp usando 309 estaciones
meteorológicas automáticas y tres productos satelitales (IMERG-Early, PERSIANN-CCS,
GSMaP_NRT). La validación técnica (frequency ratio, intensity ratio, MAD) muestra buen
desempeño en el centro y sur de los Andes peruanos, con subestimación de frecuencia y
sobreestimación de intensidad en el norte, especialmente en invierno.

**Nota de dominio**: paper de ciencia de datos climáticos/hidrológicos (no de LLMs), pero
directamente relevante para tdew: es un dataset de precipitación horaria de alta resolución
para Perú que puede servir como insumo o variable auxiliar para estimación de
evapotranspiración/variables meteorológicas derivadas.

## Nota de acceso

La URL provista por el usuario era un enlace firmado de ScienceDirect (S3, `X-Amz-Expires=300`)
no reutilizable; el acceso directo a ScienceDirect devolvió HTTP 403. El contenido se
reconstruyó vía WebSearch + WebFetch del espejo open-access en PMC
(PMC9486058), dado que *Data in Brief* es de acceso abierto. Validar cifras exactas contra
el PDF/HTML original antes de citarlas en trabajo downstream.

## Conceptos derivados

- `[[tools/piscop-h-dataset]]` — el dataset grillado en sí (NetCDF, 0.1°, horario, 2015–2020).
- `[[methods/precipitation-temporal-disaggregation]]` — la técnica de desagregación temporal
  (satélite + AWS + quantile mapping) usada para pasar de PISCOp diario a PISCOp_h horario.
- `[[findings/piscop-h-validation-results]]` — resultados de validación técnica (Fr, Ir, MAD)
  por región y estación del año.
