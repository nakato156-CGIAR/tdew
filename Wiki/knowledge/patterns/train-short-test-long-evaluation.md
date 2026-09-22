---
type: Pattern
title: Entrenar con ventanas cortas y evaluar con ventanas largas
description: Tratar la longitud de contexto de entrenamiento y la de inferencia como hiperparámetros independientes, y medir explícitamente la degradación al aumentar la segunda.
resource: https://arxiv.org/abs/2108.12409
tags: [sequence-models, length-extrapolation, evaluation-protocol, context-length, positional-encoding]
timestamp: 2026-09-22T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/alibi-attention-linear-biases]]"]
---

# Entrenar corto, evaluar largo

## El patrón

En modelos de secuencia, la longitud de las subsecuencias de entrenamiento (`L`) y la de las
subsecuencias de inferencia (`Lvalid`) se tratan casi siempre como el mismo número, porque el
coste de atención crece cuadráticamente con `L` y porque nada obliga a separarlas. El patrón
consiste en desacoplarlas: entrenar con la `L` más corta que permita aprender la señal, y medir
por separado qué ocurre al evaluar con `Lvalid > L`. Press, Smith y Lewis
(`[[sources/alibi-attention-linear-biases]]`) llaman *extrapolación* a la capacidad de seguir
rindiendo bien cuando `Lvalid` crece por encima de `L`, y muestran que esa capacidad no es una
propiedad de la arquitectura sino del método posicional: sobre el mismo modelo base, cambiar solo
el encoding de posición mueve el punto de degradación de 20 tokens extra a más de 12.000
(ver `[[findings/alibi-length-extrapolation-results]]`).

Antes de los transformers, los modelos de lenguaje recurrentes se entrenaban con secuencias cortas
asumiendo que generalizarían a contextos más largos; los propios autores del transformer
especularon que este "podría extrapolar", sin verificarlo. Medirlo es lo que convierte la
suposición en un dato.

## Por qué importa

El ahorro es concreto y de dos tipos. En tiempo: un modelo entrenado con L = 512 es 1.84 veces
más rápido de entrenar que uno con L = 3072 sobre el mismo corpus. En memoria: las matrices de
atención son el término que decide si el modelo cabe en una GPU dada, y el modelo con L = 3072 del
experimento de WikiText-103 requería más de 16 GB mientras que el de L = 512 no. Si el modelo
extrapola, ese ahorro no cuesta calidad.

La contrapartida es que un método posicional que no extrapola falla de forma abrupta, no gradual:
un modelo sinusoidal de 1.3B parámetros entrenado con L = 512 pasa de 9.71 de perplejidad a 37.05
al evaluarlo con 1024 tokens y a 105.42 con 2048. No hay una zona de degradación suave que avise.

## Cómo medirlo sin engañarse

Una curva de métrica frente a `Lvalid` con evaluación no solapada mezcla dos efectos: cuánto
aprovecha el modelo el contexto adicional, y cuánto se reduce la *early token curse* — el hecho de
que las predicciones al inicio de cada subsecuencia arrancan sin el contexto que quedó en la
anterior, y que subsecuencias más largas diluyen esa fracción. El paper separa ambos efectos
reevaluando con ventana deslizante de stride 1, que da contexto máximo a cada predicción: en ese
régimen la mejora desaparece y la curva de ALiBi queda plana, revelando que la ganancia medida era
del segundo tipo. Cualquier evaluación de este patrón debería incluir ese control antes de
concluir que el modelo aprendió a usar más historia.

## Alcance

El resultado está demostrado sobre modelos de lenguaje causales con atención, y el mecanismo que
lo habilita (o lo impide) es el encoding posicional. En arquitecturas sin encoding posicional
explícito la pregunta cambia de forma: un TCN dilatado tiene un campo receptivo fijado por su
profundidad y sus dilataciones, de modo que alargar la ventana de entrada no le da más contexto
efectivo aunque tampoco lo rompa. La parte transferible es el protocolo — declarar `L` y `Lvalid`
por separado y reportar la curva — más que la conclusión numérica.
