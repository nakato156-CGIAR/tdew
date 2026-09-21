---
type: Source
title: "Residual Echo State Networks: Residual recurrent neural networks with stable dynamics and fast learning"
description: Paper de Ceni y Gallicchio (Neurocomputing, 2024) sobre el sesgo arquitectónico de las conexiones residuales aplicadas a la dimensión temporal de redes recurrentes.
resource: https://doi.org/10.1016/j.neucom.2024.127966
tags: [recurrent-neural-networks, residual-connections, reservoir-computing, echo-state-networks, time-series, memory-capacity]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# Residual Echo State Networks (Neurocomputing, 2024)

Ver captura completa en `[[raw/papers/residual-echo-state-networks]]`.

## Resumen

Ceni y Gallicchio estudian las conexiones residuales aplicadas a la dimensión temporal de
redes recurrentes, desde el marco de Reservoir Computing y teoría de sistemas dinámicos,
atendiendo a capacidad de memoria, procesamiento de información a largo plazo, estabilidad y
capacidad de cómputo no lineal. Reportan que las skip connections ortogonales llevan a la
red al borde de la estabilidad en un régimen de isometría dinámica aproximada, y que el
beneficio de las conexiones residuales temporales aparece en tareas de memoria, pronóstico y
clasificación.

**Nota de dominio**: se ingiere como respaldo del principio general de que una ruta de
identidad a través del tiempo facilita el aprendizaje en modelos de secuencia, no como
receta transferible: el proyecto tdew usa un TCN convolucional, no una red de reservorio, y
el diseño concreto de sus reservorios ortogonales no se traslada directamente.

## Nota de acceso

Artículo tras paywall. Captura reconstruida desde abstract y highlights indexados más la
ficha de metadatos, sin leer el PDF. No se verificaron datasets, configuración experimental
ni magnitudes de mejora. No promover a `reviewed` sin acceso al texto completo.

## Conceptos derivados

- `[[methods/temporal-residual-connections-rnn]]` — conexiones residuales en la dimensión
  temporal de RNNs.
