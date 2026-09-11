---
type: Finding
title: Validación técnica de PISCOp_h — desempeño regional y estacional
description: PISCOp_h tiene buen desempeño en el centro/sur andino peruano y peor desempeño (subestimación de frecuencia, sobreestimación de intensidad) en el norte, especialmente en invierno.
resource: https://doi.org/10.1016/j.dib.2022.108570
tags: [precipitation, validation, peru, bias]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/piscop-h-hourly-precipitation-peru]]"]
---

# Validación técnica de PISCOp_h

Resultados de la validación de `[[tools/piscop-h-dataset]]` (generado con
`[[methods/precipitation-temporal-disaggregation]]`) reportados por Huerta et al. (2022).

## Métricas usadas

- **Frequency ratio (Fr)**: razón entre la frecuencia de horas húmedas (≥0.1 mm) del
  producto grillado y la observada en estaciones.
- **Intensity ratio (Ir)**: razón entre las tasas medias de precipitación durante períodos
  húmedos, grillado vs. observado.
- **Standardized Mean Absolute Difference (MAD)**: mide la coherencia temporal (alineación
  del ciclo horario) entre el producto grillado y las observaciones.

## Resultados

- **Andes central y sur de Perú**: buen desempeño — Fr e Ir dentro de ±25% durante el
  verano austral.
- **Norte de Perú**: el producto subestima la frecuencia de horas húmedas y sobreestima la
  intensidad, particularmente marcado en invierno.
- **Coherencia temporal (MAD)**: valores menores a 0.25 en la mayor parte del territorio
  peruano, indicando buena alineación del ciclo horario en general.
- **Efecto de la corrección de sesgo diurno**: PISCOp_h (con corrección vía quantile
  mapping) mejora sobre PISCOp_h_non-DBC (sin corrección), confirmando el valor de la etapa
  de corrección de sesgo en el método de desagregación.

## Limitaciones

El desempeño regional desigual (mejor en el sur/centro andino, peor en el norte) sugiere
que la calidad de la corrección de sesgo depende de la densidad/calidad de la red de
estaciones automáticas usada como referencia en cada región — no se reportan aquí cifras de
densidad de estaciones por región para confirmar esta hipótesis; validar contra el paper
completo si se requiere precisión.
