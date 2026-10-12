---
type: Method
title: "ALiBi: sesgo lineal por distancia sobre los scores de atención"
description: Sustituir los embeddings posicionales por un sesgo estático no aprendido, proporcional a la distancia query-key, con una pendiente fija por cabeza de atención.
resource: https://arxiv.org/abs/2108.12409
tags: [transformers, attention, positional-encoding, alibi, recency-bias, length-extrapolation]
timestamp: 2026-09-22T00:00:00Z
status: draft
contributed_by: [claude]
sources: ["[[sources/alibi-attention-linear-biases]]"]
---

# ALiBi (Attention with Linear Biases)

## Formulación

En un transformer estándar la atención de la consulta `i` sobre las primeras `i` claves se
calcula como `softmax(q_i K^T)`. ALiBi elimina todo embedding posicional de la red y añade, tras
el producto punto y antes del softmax, un sesgo estático no aprendido:

```
softmax(q_i K^T + m · [−(i−1), ..., −2, −1, 0])
```

El vector de sesgos penaliza linealmente la distancia entre la consulta y cada clave: la clave en
la misma posición recibe 0, la inmediatamente anterior `−m`, la de dos pasos atrás `−2m`, y así.
El sesgo **no** se multiplica por el factor de escala `√d_k`.

## Pendientes por cabeza

`m` es un escalar fijado antes del entrenamiento, distinto en cada cabeza, de modo que las
cabezas decaen a ritmos distintos y el modelo conserva tanto cabezas muy locales como cabezas casi
sin penalización. Con 8 cabezas los autores usan la secuencia geométrica 1/2¹, 1/2², …, 1/2⁸. Con
16 cabezas se interpolan esas pendientes promediando geométricamente cada par consecutivo, lo que
da la secuencia que empieza en 1/√2 con razón 1/√2. En general, para `n` cabezas, la secuencia
geométrica que empieza en `2^(−8/n)` y usa ese mismo valor como razón.

Las pendientes no se retunean por dataset ni por tamaño de modelo: el mismo conjunto desarrollado
en WikiText-103 se transfirió sin cambios al corpus de libros y al modelo de 1.3B parámetros. Los
autores probaron hacerlas entrenables y la extrapolación empeoró (además de frenar el
entrenamiento un 3%). De una exploración manual de unos diez conjuntos concluyen que lo que
importa es que las pendientes caigan en el rango (0, 1) con densidad creciente cerca de 0, y que
el método es poco sensible a la elección exacta — muestrear de una exponencial funcionó en algunos
casos, con alta varianza.

## Implementación y coste

El sesgo se suma a la matriz de máscara, que en un LM causal ya se suma al producto query-key
antes del softmax. No se añade ninguna operación ni parámetro, así que no hay penalización de
runtime. El único coste es de memoria: la máscara pasa de `L×L` a `n×L×L`, con `n` el número de
cabezas, porque cada cabeza usa su propia pendiente — hasta 100 MB extra en los experimentos del
paper, frente a los gigabytes que se ahorran al poder entrenar con secuencias más cortas.

Como método relativo, ALiBi inyecta posición en cada capa, sobre claves y consultas pero no sobre
los valores, igual que el sesgo de T5 y que rotary. Los autores hipotetizan que mantener la
información posicional fuera de los valores favorece la extrapolación, sin demostrarlo.

## Relación con los métodos que reemplaza

Comparado en igualdad de condiciones sobre el mismo modelo base (ver
`[[findings/alibi-length-extrapolation-results]]`): los embeddings aprendidos no pueden representar
posiciones mayores que `L` y no extrapolan en absoluto; el sinusoidal extrapola unas decenas de
tokens; rotary, un par de centenares, más lento; el sesgo de T5 llega más lejos pero entrena al
menos el doble de lento, de modo que entrenar corto y extrapolar no ahorra tiempo frente a
entrenar directo con la longitud objetivo. ALiBi es el único de los cuatro que combina
extrapolación con coste de runtime nulo.

Una variante cercana, el Distance Aware Transformer (Wu et al., 2021), **multiplica** los scores
por un sesgo función de la distancia en vez de sumarlo; los autores reportan que en sus propios
experimentos, no incluidos en el paper, multiplicar degradó el rendimiento.

## Aplicabilidad al TCN de tdew

La capa de pooling por atención del proyecto (`tdew_estimation/models/attention_pool.py`) usa un
`nn.MultiheadAttention` bidireccional sobre las `T` posiciones de la ventana codificadas por el
TCN, más una consulta aprendida estilo CLS, y no incorpora ningún encoding posicional: el orden
llega solo a través de las convoluciones dilatadas del encoder. Añadir un sesgo tipo ALiBi es
directo — es una suma sobre la matriz de atención — y daría un sesgo de recencia explícito y
parametrizado por cabeza.

Dos salvedades antes de trasladarlo: el paper valida ALiBi en LMs causales autorregresivos, no en
atención bidireccional de pooling sobre una ventana fija, y el vector de sesgos tal como está
escrito asume causalidad (distancias solo hacia atrás). Y las pendientes 1/2¹…1/2⁸ están
calibradas para contextos de cientos a miles de tokens; con ventanas de 14 a 60 pasos diarios
(`docs/protocol/week1_manifest.yaml`) una pendiente de 1/2 penaliza la posición más lejana con
−30 en logits, lo que deja la atención efectivamente truncada. Cualquier traslado exige recalibrar
la escala de `m` a la longitud de ventana real.
