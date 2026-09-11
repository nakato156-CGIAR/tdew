# Improving Subseasonal Forecasting in the Western U.S. with Machine Learning

- **arXiv id**: 1809.07394
- **URL**: https://arxiv.org/abs/1809.07394 (PDF: https://arxiv.org/pdf/1809.07394)
- **Autores**: Jessica Hwang, Paulo Orenstein, Judah Cohen, Karl Pfeiffer, Lester Mackey
- **Venue/fecha**: arXiv preprint. v1: 19 sept 2018; última revisión v3: 22 mayo 2019.
- **Fecha de captura**: 2026-09-11
- **Categorías**: Estadística Aplicada, Aprendizaje Automático, Computadoras y Sociedad

## Abstract

Los autores describen un enfoque de aprendizaje automático para predecir temperatura y
precipitación en el occidente de EE.UU. con dos a seis semanas de anticipación
("subseasonal forecasting"). El sistema es un ensemble de dos modelos de regresión que
integran mediciones meteorológicas diversas y pronósticos dinámicos operativos. Reportan
mejoras significativas de skill frente al sistema operativo CFSv2 (debiased), del orden de
40-50% para temperatura y 129-169% para precipitación, en el período histórico 2011-2018.

## Metodología (extracto)

El ensemble combina dos modelos de regresión no lineal:

1. **MultiLLR (Multitask Local Linear Regression con selección de features)**: integra
   mediciones meteorológicas diversas y usa un "procedimiento backward stepwise
   personalizado" adaptado a la métrica objetivo de skill de coseno. Features: presión
   atmosférica, temperatura, anomalías SST/hielo marino, índice MEI (ENSO), oscilación
   Madden-Julian (MJO), humedad relativa, altura geopotencial, pronósticos dinámicos NMME.

2. **AutoKNN (Multitask Autoregressive k-Nearest-Neighbors)**: usa únicamente datos
   históricos de la variable objetivo (temperatura o precipitación), con "características
   de vecino más próximo adaptadas al skill": rezagos de 29/43 días, 58/86 días y 1 año
   previo, más los 20 vecinos históricos más similares por skill medio.

El ensemble final normaliza las anomalías predichas (norma L2) de ambos modelos y calcula
un promedio ponderado de las anomalías normalizadas.

### Dataset: SubseasonalRodeo

Compilación de datos abierta que combina: temperatura y precipitación CPC (NOAA),
anomalías SST/hielo marino (NOAA OISSTv2), índices climáticos (MEI, MJO), reanálisis NCEP,
y pronósticos dinámicos NMME/CFSv2. Cobertura: región oeste de EE.UU., 25°N-50°N,
125°W-93°W, resolución 1°×1°.

## Resultados (extracto)

**Período de concurso (2017-2018, 26 pronósticos bisemanales, "Subseasonal Rodeo")**:
- Temperatura semanas 3-4: skill 0.345 (vs. CFSv2 debiased: 0.159)
- Precipitación semanas 3-4: skill 0.236 (vs. 0.071)
- El ensemble superó al competidor ganador del Rodeo en las cuatro tareas evaluadas.

**Período histórico (2011-2018)**:
- Mejora sobre CFSv2 debiased: 40-50% en temperatura, 129-169% en precipitación.
- Ensemble combinado con CFSv2: skill 0.357 (temperatura semanas 3-4), 0.186
  (precipitación semanas 5-6).

## Nota de captura

Captura basada en la página de abstract de arXiv (https://arxiv.org/abs/1809.07394) y en
la versión HTML de ar5iv (https://ar5iv.labs.arxiv.org/abs/1809.07394), ya que el PDF
directo no pudo procesarse como texto legible por la herramienta de fetch usada. Contenido
generado con asistencia de IA (Claude) — validar cifras contra el paper original antes de
citarlas en trabajo downstream.
