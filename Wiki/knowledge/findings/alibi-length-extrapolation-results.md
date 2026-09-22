---
type: Finding
title: Extrapolación de longitud de ALiBi frente a los métodos posicionales existentes
description: Cifras de perplejidad, memoria y tiempo en WikiText-103 y CC100+RoBERTa, y el análisis del propio paper que atribuye la ganancia a la reducción de la early token curse y no al uso de contexto más largo.
resource: https://arxiv.org/abs/2108.12409
tags: [alibi, length-extrapolation, perplexity, wikitext-103, benchmark, positional-encoding, early-token-curse]
timestamp: 2026-09-22T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/alibi-attention-linear-biases]]"]
---

# Resultados de extrapolación de ALiBi (ICLR 2022)

## Hasta dónde extrapola cada método posicional

Todas estas mediciones salen del mismo modelo base (Baevski & Auli, 2018) entrenado sobre
WikiText-103, cambiando únicamente el método posicional, con `k = Lvalid − L` tokens extra en
validación:

| Método | Mejora hasta (L = 512) | Mejora hasta (L = 1024) | Coste |
|---|---|---|---|
| Aprendido | no extrapola | no extrapola | no puede codificar posiciones > L |
| Sinusoidal | k ≈ 20, plano hasta k ≈ 50 | k ≈ 50 | referencia |
| Rotary | k ≈ 200 | k ≈ 100 | entrenamiento e inferencia más lentos |
| T5 bias | k ≈ 600 | k ≈ 800 | ≥ 2× más lento de entrenar |
| ALiBi | hasta ≥ 12k tokens | hasta ≈ 3L | sin coste de runtime |

El dato que invalida al T5 bias como alternativa práctica es de velocidad, no de calidad: el
modelo sinusoidal con L = 1024 corre a 28.5k palabras/segundo y el T5 bias con L = 512 a 14.4k
WPS, así que entrenar corto y extrapolar con T5 bias no ahorra tiempo frente a entrenar
directamente con la longitud objetivo.

## WikiText-103

Sin extrapolar, ALiBi supera al sinusoidal para cada `L`: con L = 3072 y Lvalid = 3072, 17.60 de
perplejidad frente a 18.67 ± 0.24 del sinusoidal. Extrapolando, el modelo ALiBi entrenado con
L = 512 pasa de 19.73 (Lvalid = 512) a 18.40 (Lvalid = 3072), por debajo del sinusoidal entrenado
con L = 3072, con un margen que los autores reportan como estadísticamente significativo. Ese
modelo es 1.84 veces más rápido de entrenar y cabe en una GPU mucho menor, mientras que el
sinusoidal con L = 3072 necesita más de 16 GB para las matrices de atención.

## CC100+RoBERTa, 1.3B parámetros

Corpus de 461 GB, modelos de 25 capas, 16 cabezas, dimensión 2048, entrenados una época (50k
updates) en 128 GPUs V100. Con el mismo presupuesto de tiempo, ALiBi con L = 1024 obtiene 8.92 de
perplejidad en Lvalid = 2048 frente a 9.01 del sinusoidal entrenado con L = 2048, usando 3.1 GB
menos de memoria (26.2 vs 29.3 GB); alcanza un valor dado de perplejidad, en promedio, 11% más
rápido. En el par más corto, ALiBi con L = 512 queda a 0.06 del sinusoidal con L = 1024 (9.30 vs
9.24) con 1.6 GB menos de memoria.

El contraste más fuerte está en la tabla con todos los modelos igualados a 50k updates, donde se
ve el colapso del sinusoidal al pedirle un token más que `L`:

| Modelo | PPL @512 | PPL @1024 | PPL @2048 |
|---|---|---|---|
| Sinusoidal, L=512 | 9.71 | 37.05 | 105.42 |
| ALiBi, L=512 | 9.79 | 9.30 | 9.54 |
| Sinusoidal, L=1024 | — | 9.15 | 48.85 |
| ALiBi, L=1024 | — | 9.16 | 8.92 |
| Sinusoidal, L=2048 | — | — | 8.83 |
| ALiBi, L=2048 | — | — | 8.84 |

A esta escala, sin extrapolar, ALiBi rinde igual que el sinusoidal (diferencias de 0.01 a 0.08),
no mejor. La ventaja de calidad que ALiBi muestra en WikiText-103 sin extrapolar desaparece con
más datos y más cómputo; los autores sugieren que su sesgo inductivo aporta sobre todo en
modelado de lenguaje de bajos recursos.

El rendimiento al extrapolar no es monótono: alcanza su mejor punto alrededor de `2L` y después
se degrada suavemente. El modelo con L = 512 toca su mínimo (9.3) en Lvalid = 1012 y el de
L = 1024 (8.9) en Lvalid = 2024. La explicación que ofrecen es de composición: con subsecuencias
de longitud 2L, la mitad de las que consume el modelo son tan largas como las de entrenamiento; a
partir de 2L+1 esa fracción cae por debajo de la mitad.

## Acotación del propio paper: la ganancia es por la early token curse

El apéndice B reevalúa WikiText-103 con ventana deslizante de stride 1, que da a cada predicción
el máximo contexto disponible. En ese régimen la perplejidad de los modelos ALiBi **no mejora** al
aumentar `Lvalid`: se mantiene plana. Los autores interpretan que la mejora observada con
evaluación no solapada viene de reducir la *early token curse* — al partir el conjunto de
evaluación en subsecuencias, las predicciones tempranas de cada una pierden el contexto que quedó
en la subsecuencia anterior, y subsecuencias más largas reducen la fracción de predicciones
afectadas (del 10% al 5% al pasar de Lvalid = 1000 a 2000 contando las que tienen ≤ 100 tokens de
contexto) — y no de que el modelo explote contextos más largos que los vistos en entrenamiento.
Lo enuncian de forma directa: "when Lvalid > L, ALiBi might not be using contexts longer than the
ones it was trained on". El sesgo de T5 se comporta igual bajo ventana deslizante.

La consecuencia práctica es que ALiBi debe leerse como una garantía de **no degradación** ante
entradas más largas, no como un mecanismo que amplíe el horizonte efectivo del modelo. La
perplejidad del sinusoidal explota incluso con ventana deslizante, así que la diferencia entre los
métodos sigue siendo real; lo que no se sostiene es la lectura de que el modelo aprendió a usar
más contexto.
