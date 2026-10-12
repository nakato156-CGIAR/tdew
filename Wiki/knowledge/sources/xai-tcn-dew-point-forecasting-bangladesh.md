---
type: Source
title: "Explainable AI-Driven Dew Point Forecasting With Attention-Based Temporal Convolutional Networks"
description: Paper (IEEE Access, 2025) que propone un TCN con atención y técnicas XAI para pronosticar la temperatura de punto de rocío en 35 estaciones de Bangladesh.
resource: https://doi.org/10.1109/ACCESS.2025.3490969
tags: [dew-point, deep-learning, tcn, attention, explainable-ai, xai, bangladesh, weather-forecasting]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# Explainable AI-Driven Dew Point Forecasting With Attention-Based TCN (IEEE Access, 2025)

Ver captura completa en `[[raw/papers/xai-tcn-dew-point-forecasting-bangladesh]]`.

## Resumen

Paper publicado en IEEE Access (2025, DOI 10.1109/ACCESS.2025.3490969) que propone un
modelo de Temporal Convolutional Networks (TCN) con mecanismo de atención para pronosticar
la temperatura de punto de rocío (dew point), complementado con técnicas de IA explicable
(XAI) para selección de features e interpretabilidad. Usa datos de 35 estaciones
meteorológicas de Bangladesh a lo largo de ~4 décadas (desde 1980). Reporta test loss de
0.002, validation loss de 0.00212 y MAE de 0.032.

**Nota de dominio**: directamente relevante para tdew — pronóstico de punto de rocío es una
variable meteorológica derivada afín a los productos ya ingeridos (PISCOp_h, PISCOeo_pm) y
el paper aporta un enfoque de modelado (TCN + atención + XAI) potencialmente aplicable al
pipeline del proyecto.

## Verificación parcial (2026-09-21)

Una segunda captura por una ruta distinta —el registro indexado de Consensus, ver
`[[raw/papers/xai-tcn-dew-point-forecasting-bangladesh-abstract-indexed]]`— aportó el abstract
completo y cerró parte de los huecos de la primera: primer autor **Md. Abdullah et al.**,
**RMSE = 0.044**, **R² y R² ajustado = 0.938**, y los baselines comparados (**LSTM, CNN,
BiLSTM, LSTM_CNN híbrido y GRU**). El paper acumulaba 11 citas a esa fecha.

Sigue sin resolverse lo que más condiciona el uso de estas cifras: la escala en que se
calculan MAE y RMSE. Un RMSE de 0.044 sobre punto de rocío en °C sería implausible, y la
lectura compatible con un test loss de 0.002 es que la serie está normalizada, pero el
abstract no lo declara. Tampoco hay persistencia ni climatología entre los baselines, así que
las cifras no acotan el aporte sobre una referencia trivial — ver
`[[patterns/persistence-climatology-reference-baselines]]`. El PDF de IEEE Xplore sigue sin
leerse.

## Nota de acceso — IMPORTANTE

IEEE Xplore bloqueó el acceso directo (HTTP 418 en la URL de descarga de PDF; página del
documento sin contenido renderizable vía WebFetch, requiere JavaScript). Esta captura se
reconstruyó **solo a partir de snippets de WebSearch**, sin leer el PDF ni el HTML completo
del artículo. No se pudo confirmar: lista de autores, arquitectura exacta del modelo,
técnica(s) XAI específica(s) usada(s), ni las variables de entrada. **Validar contra el PDF
original (DOI 10.1109/ACCESS.2025.3490969) antes de usar estos datos en trabajo downstream
o de promover estos conceptos a `reviewed`.**

## Conceptos derivados

- `[[methods/attention-tcn-explainable-forecasting]]` — el método de TCN + atención + XAI
  para pronóstico de series temporales meteorológicas.
- `[[findings/xai-tcn-dew-point-performance]]` — métricas de desempeño reportadas (test
  loss, validation loss, MAE, RMSE, R²) y baselines comparados.
- `[[patterns/persistence-climatology-reference-baselines]]` — esta fuente es uno de los
  contraejemplos del patrón: compara solo contra modelos aprendidos.
