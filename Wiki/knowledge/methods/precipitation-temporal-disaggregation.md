---
type: Method
title: Desagregación temporal de precipitación diaria a horaria (satélite + AWS + quantile mapping)
description: Técnica para convertir un dataset diario grillado de precipitación en un producto horario, usando patrones satelitales corregidos por sesgo con estaciones automáticas.
resource: https://doi.org/10.1016/j.dib.2022.108570
tags: [precipitation, temporal-disaggregation, quantile-mapping, bias-correction, idw]
timestamp: 2026-09-11T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/piscop-h-hourly-precipitation-peru]]"]
---

# Desagregación temporal de precipitación (PISCOp → PISCOp_h)

Método usado por Huerta et al. (2022, SENAMHI) para generar un producto horario de
precipitación (PISCOp_h) a partir de un dataset diario grillado (PISCOp), preservando los
totales diarios pero repartiéndolos en fracciones horarias informadas por patrones
satelitales corregidos.

## Procedimiento (4 etapas)

1. **Promedio satelital (SAT)**: promediar linealmente tres productos satelitales de
   precipitación (IMERG-Early, PERSIANN-CCS, GSMaP_NRT) para obtener una estimación horaria
   de referencia del ciclo diurno.
2. **Interpolación espacial de estaciones (AWS → grilla)**: interpolar espacialmente las
   observaciones de estaciones meteorológicas automáticas usando Inverse Distance Weighting
   (IDW).
3. **Corrección de sesgo del ciclo diurno (quantile mapping)**: corregir el sesgo de SAT
   usando algoritmos de quantile mapping contra las observaciones interpoladas de AWS,
   produciendo SATc (satelital corregido).
4. **Desagregación**: repartir el total diario del dataset grillado de referencia (PISCOp)
   en fracciones horarias, usando la distribución horaria relativa de SATc — la fórmula de
   desagregación garantiza que la suma de las fracciones horarias reconstruya exactamente el
   total diario original.

## Insumos requeridos

- Dataset diario grillado de referencia (en este caso PISCOp v2.1).
- Al menos un producto satelital de precipitación con resolución sub-diaria (idealmente
  varios, para promediar y reducir ruido).
- Red de estaciones automáticas (AWS) con observaciones horarias, para la corrección de
  sesgo y para la validación.

## Productos intermedios/salida

- SAT (satelital promedio sin corregir), SATc (satelital corregido), PISCOp_h_non-DBC
  (desagregado sin corrección de sesgo), PISCOp_h (producto final, con corrección de sesgo).
  Ver `[[tools/piscop-h-dataset]]`.

## Validación y limitaciones conocidas

Ver `[[findings/piscop-h-validation-results]]`. El método depende de la densidad y
representatividad de la red de AWS usada para la corrección de sesgo; en regiones con menor
cobertura de estaciones (norte de Perú) el desempeño es notablemente peor
(subestimación de frecuencia, sobreestimación de intensidad, especialmente en invierno).

## Aplicabilidad general

Aunque aplicado aquí a precipitación en Perú, el patrón (dataset diario confiable +
satélite de alta frecuencia + red de estaciones para corrección de sesgo por quantile
mapping + desagregación preservando el total diario) es transferible a otras variables
meteorológicas con la misma estructura de datos (p.ej. evapotranspiración, radiación),
siempre que exista un producto diario de referencia y una fuente sub-diaria correlacionada
que se pueda corregir por sesgo.
