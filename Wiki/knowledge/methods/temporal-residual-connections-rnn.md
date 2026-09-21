---
type: Method
title: Conexiones residuales en la dimensión temporal de redes recurrentes
description: Aplicar skip connections a lo largo del tiempo (no solo entre capas) en RNNs, analizadas desde Reservoir Computing: capacidad de memoria, estabilidad e isometría dinámica aproximada.
resource: https://doi.org/10.1016/j.neucom.2024.127966
tags: [recurrent-neural-networks, residual-connections, reservoir-computing, memory-capacity, time-series]
timestamp: 2026-09-21T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/residual-echo-state-networks]]"]
---

# Conexiones residuales temporales en RNNs (Ceni y Gallicchio, Neurocomputing 2024)

Las conexiones residuales son estándar en arquitecturas feedforward profundas; Ceni y
Gallicchio las estudian en la dimensión temporal de redes recurrentes, es decir, como una
ruta de identidad que atraviesa pasos de tiempo en vez de capas. El análisis se plantea desde
Reservoir Computing y teoría de sistemas dinámicos, sobre cuatro propiedades: capacidad de
memoria, procesamiento de información a largo plazo, estabilidad y capacidad de cómputo no
lineal.

Los dos resultados que los autores destacan son que las conexiones residuales temporales
habilitan el procesamiento a largo plazo de series de tiempo, y que usar skip connections
ortogonales lleva a la red al borde de la estabilidad, en un régimen de isometría dinámica
aproximada. Los experimentos cubren tareas de memoria, de pronóstico y de clasificación.

## Alcance y límites para este proyecto

Lo que se puede sostener con esta fuente es el principio general: una ruta de identidad
explícita a lo largo del tiempo facilita el aprendizaje y la retención en modelos de
secuencia, y su ausencia obliga al modelo a reconstruir esa identidad con capas aprendidas.
Lo que **no** se puede sostener es una receta concreta para un TCN convolucional como el de
tdew: los reservorios ortogonales no entrenados de una Echo State Network son un mecanismo
distinto, y la captura de esta fuente se hizo sin acceso al PDF
(ver `[[sources/residual-echo-state-networks]]`).
