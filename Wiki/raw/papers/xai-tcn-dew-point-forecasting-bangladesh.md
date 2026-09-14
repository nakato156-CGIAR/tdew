---
captured_at: 2026-09-14T00:00:00Z
url: https://ieeexplore.ieee.org/document/10947683/
title: Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks
---

# Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks

- **Venue/año**: IEEE Access, 2025.
- **DOI**: 10.1109/ACCESS.2025.3490969
- **arnumber**: 10947683
- **URL original solicitada**: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10947683
  (enlace de descarga de PDF; redirige/equivale a https://ieeexplore.ieee.org/document/10947683/)
- **Autores**: no disponibles en esta captura (ver Nota de acceso).
- **Fecha de captura**: 2026-09-14

## Nota de acceso

WebFetch sobre la URL `stamp.jsp` devolvió HTTP 418 ("I'm a Teapot" — bloqueo anti-bot de
IEEE Xplore). WebFetch sobre la página del documento
(`ieeexplore.ieee.org/document/10947683/`) devolvió contenido vacío (la página requiere
JavaScript para renderizar el abstract/metadatos; IEEE Xplore no es accesible a scrapers
simples). El contenido de esta captura se reconstruyó exclusivamente vía WebSearch
(snippets de resultados de búsqueda que citan el abstract), sin acceso al PDF ni al HTML
completo del artículo. **No se pudo confirmar la lista de autores.** Validar todos los
datos (autores, cifras exactas, metodología detallada) contra el PDF original (DOI
10.1109/ACCESS.2025.3490969) antes de citar en trabajo downstream.

## Abstract (reconstruido vía WebSearch)

El estudio desarrolla un modelo de Temporal Convolutional Networks (TCN) con mecanismo de
atención para predecir la temperatura de punto de rocío (dew point), potenciado con
técnicas de IA explicable (XAI) para apoyar la selección de features y ofrecer insights
interpretables sobre los factores que influyen en las predicciones. La predicción de punto
de rocío se describe como un indicador clave para cambio climático, relevante para
adaptación climática, agricultura, planificación energética, pronóstico del tiempo y salud
pública. La investigación analiza datos de temperatura de punto de rocío de 35 estaciones
meteorológicas en Bangladesh, buscando patrones y tendencias a lo largo de cuatro décadas
desde 1980.

## Resultados reportados (vía WebSearch, sin verificar contra el paper completo)

- Test loss: 0.002
- Validation loss: 0.00212
- Mean Absolute Error (MAE): 0.032
- Root Mean Squared Error (RMSE): mencionado como métrica reportada, valor exacto no
  confirmado en los snippets disponibles.

## Elementos no confirmados en esta captura

- Arquitectura exacta del TCN con atención (número de capas, dilataciones, tipo de
  mecanismo de atención).
- Técnica(s) XAI específica(s) usada(s) (p.ej. SHAP, LIME, attention weights) — búsquedas
  adicionales sugieren posible uso de SHAP, pero no está confirmado directamente en el
  abstract de esta fuente.
- Lista de autores y afiliación institucional.
- Variables/features de entrada usadas para la predicción de punto de rocío.
- Período de test/validación específico dentro del rango de datos (1980–presente).

## Búsquedas realizadas para esta captura

1. `ieeexplore arnumber=10947683` — identificó el título del paper.
2. `"Explainable AI-Driven Dew Point Forecasting..." authors abstract` — resumen del
   abstract y métricas.
3. `... IEEE Access DOI 2025` — identificó DOI 10.1109/ACCESS.2025.3490969.
4. `"dew point" "temporal convolutional network" attention SHAP explainable Bangladesh 35
   stations feature selection` — sin nueva información confirmada más allá de lo anterior.
