# Revisión simulada estilo Nature: consolidado

Tres revisiones independientes, generadas con IA (Claude Sonnet) sobre el borrador del 2026-10-23 (`paper.pdf`, 18 pp.; `suplemento.pdf`, 11 pp.). Los informes completos están en `revisor1_estadistica.md`, `revisor2_clima_datos.md` y `revisor3_ml_reproducibilidad.md`. Deben validarse con Palacios y SENAMHI antes de actuar sobre ellos.

Los tres recomiendan **revisión mayor** y proponen una revista especializada en lugar de la familia Nature. Los tres coinciden en que las cifras están bien trazadas: los revisores 1 y 3 las contrastaron con los CSV y las predicciones, y no hallaron discrepancias.

## Objeciones compartidas (dos o tres revisores)

| # | Objeción | Revisores | Tipo de respuesta |
|---|---|---|---|
| 1 | La ventaja frente a `tuned` se debe en gran parte a su recursión sobre Td. Frente a rivales sin recursión (`tuned_sin_td`, `llr_rezagos_sel`) la brecha es de 0,003 a 0,03 °C. El encuadre "TimesFM frente a Palacios" sobredimensiona el hallazgo. | R1, R3 | Reencuadre + análisis de la brecha por horizonte dentro del bloque (barato, con predicciones existentes) |
| 2 | La configuración de TimesFM se seleccionó sobre el bloque 2013–2016, y los rivales LLR se añadieron después de ver resultados. Además, hay muchas comparaciones sin corrección por multiplicidad. | R1, R3 | Declarar el análisis confirmatorio (bloque 2009–2012) frente al exploratorio; cribado con validación anterior a ambos bloques (costoso: GPU) |
| 3 | La relevancia práctica no está demostrada. Las brechas son mucho menores que el sesgo de PISCO frente a estaciones (+1,4 °C), y no hay margen de equivalencia ni propagación a ET0. | R1, R2 | Reencuadre + propagación a ET0 (moderado) |
| 4 | Faltan métricas de skill frente a climatología, extremos (cola de anomalías), razón de varianzas y calibración de cuantiles. | R1, R2 | Barato con predicciones existentes |
| 5 | Solo hay dos bloques con contextos solapados, así que "4 de 4 casos" no son réplicas. | R1 (R2 lo menciona) | Más bloques con origen móvil (costoso: GPU + `tuned`) |
| 6 | Faltan la sección de disponibilidad de código y datos, la licencia de PISCO y los marcadores pendientes ([[FALTA]], [[CITA]]). | R2, R3 | Redacción + datos externos |

## Objeciones de un solo revisor

- **R1 (bootstrap):** ningún esquema cubre la dependencia espacio-temporal. Con bloques solo temporales, los IC son entre 3 y 6 veces más anchos, y en 2013–2016 se pierde la distinción frente a `tuned_sin_td` y `llr_rezagos_sel`. Se pide un bootstrap espacio-temporal o Diebold-Mariano con HAC. Es barato.
- **R2 (circularidad):** el "observado" es PISCO interpolado. Se pide estratificar el error por distancia a estación, llevar ISD al cuerpo, usar Perú como análisis primario y desglosar el error por región y altitud. La zona A(r)A' (42 % del dominio) pesa en el agregado.
- **R2 (ENSO):** se pide estratificar los años 2013 y 2015–2016 por fase ENSO. Hay tensión con la regla del proyecto de no explicar por El Niño. Estratificar es descriptivo y no causal, así que es compatible si se redacta como tal.
- **R3 (preentrenamiento):** falta discutir si TimesFM vio PISCO o series peruanas en su corpus. Hay que documentar el corpus o añadir una prueba libre de sospecha.
- **R3 (baselines):** faltan gradient boosting global, Chronos-2/Moirai y el TCN del repositorio. También falta explicar cómo entra la covariable en TimesFM y cómo decodifica 1.461 días.
- **R3 (costo):** el costo sale de una sola corrida no controlada, y el de los LLR seleccionados no se midió.

## Clasificación por costo

- **Solo texto:** objeciones 1, 2, 3 y 6 (reencuadre); preentrenamiento; disponibilidad de código y datos; mecanismo de la covariable.
- **Análisis nuevos baratos (predicciones existentes, CPU):** brecha por horizonte; bootstrap espacio-temporal o DM-HAC; skill, extremos y razón de varianzas; Perú primario y desglose por región y altitud; estratificación ENSO descriptiva; distancia a estación; medir el costo de los LLR seleccionados.
- **Experimentos costosos (GPU o días de cómputo):** más bloques con origen móvil; cribado sin fuga; Chronos-2, Moirai y gradient boosting; propagación a ET0 con producto completo.
