---
type: Tool
title: PISCOp_h
description: Dataset grillado de precipitación horaria para Perú (0.1°, 2015–2020, NetCDF) desarrollado por SENAMHI vía desagregación temporal de PISCOp diario.
resource: https://doi.org/10.6084/m9.figshare.c.5743166
tags: [precipitation, gridded-dataset, peru, netcdf, senamhi]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/piscop-h-hourly-precipitation-peru]]"]
---

# PISCOp_h

Dataset grillado de precipitación horaria para todo el territorio peruano, desarrollado por
SENAMHI (Huerta, Lavado-Casimiro, Felipe-Obando, 2022). Distribuido en formato NetCDF con
convenciones CF.

## Características

- **Resolución espacial**: 0.1° × 0.1° (extensión: 0.95°N–18.75°S, 81.25°W–68.05°W).
- **Resolución temporal**: horaria.
- **Período**: 2015–2020.
- **Derivado de**: PISCOp v2.1 (dataset diario grillado, combinación de estaciones +
  satélite), desagregado a resolución horaria vía `[[methods/precipitation-temporal-disaggregation]]`.
- **Repositorio de datos**: Figshare, https://doi.org/10.6084/m9.figshare.c.5743166.
- **Código del flujo de desagregación**: https://github.com/adrHuerta/PISCOp_tdisaggregation
  (no explorado en detalle en esta captura).

## Variantes/productos intermedios generados en el proceso

- **SAT**: promedio lineal de tres satélites (IMERG-Early, PERSIANN-CCS, GSMaP_NRT), sin
  corrección.
- **SATc**: SAT con corrección de sesgo del ciclo diurno (quantile mapping vs. AWS).
- **PISCOp_h_non-DBC**: PISCOp diario desagregado usando SAT (sin corrección de sesgo).
- **PISCOp_h**: producto final, desagregado usando SATc (con corrección de sesgo diurno).

## Desempeño y limitaciones

Ver `[[findings/piscop-h-validation-results]]` para el detalle de la validación técnica
(frequency ratio, intensity ratio, MAD) por región. En resumen: buen desempeño en centro y
sur de los Andes, subestimación de frecuencia y sobreestimación de intensidad en el norte,
en particular durante invierno.

## Relevancia para tdew

Insumo potencial de precipitación horaria de alta resolución para Perú; el formato NetCDF
con convenciones CF facilita su combinación con otras variables (temperatura,
evapotranspiración) usadas en el pipeline de tdew. No se ha verificado en esta captura si el
proyecto tdew ya usa PISCOp o PISCOp_h como insumo — pendiente de contrastar con
`MODEL_INPUTS.md`/`pipeline/` del repo si aplica.
