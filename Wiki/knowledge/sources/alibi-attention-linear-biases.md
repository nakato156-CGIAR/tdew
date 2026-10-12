---
type: Source
title: "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation"
description: Paper de Press, Smith y Lewis (ICLR 2022) que introduce ALiBi, un sesgo lineal no aprendido sobre los scores de atención que sustituye a los embeddings posicionales y permite entrenar con secuencias cortas e inferir con secuencias largas.
resource: https://arxiv.org/abs/2108.12409
tags: [transformers, attention, positional-encoding, length-extrapolation, alibi, recency-bias, sequence-models, language-modeling]
timestamp: 2026-09-22T00:00:00Z
status: draft
contributed_by: [claude]
sources: []
---

# ALiBi: atención con sesgos lineales (ICLR 2022)

Ver captura completa en `[[raw/papers/alibi-attention-linear-biases]]`.

## Resumen

Press, Smith y Lewis parten de una pregunta concreta: por qué un transformer entrenado con
subsecuencias de longitud `L` se degrada al evaluarlo con subsecuencias de longitud
`Lvalid > L`. Manteniendo fijo el resto del modelo (Baevski & Auli, 2018, sobre WikiText-103) y
cambiando solo el método posicional, muestran que la causa está en ese método: el sinusoidal deja
de mejorar a los ~20-50 tokens extra y después colapsa, rotary aguanta 100-200 tokens y el sesgo
relativo de T5 llega a 600-800 pero entrena al menos el doble de lento, lo que anula la ventaja
de entrenar corto.

La propuesta, ALiBi, elimina los embeddings posicionales y suma al producto query-key un sesgo
estático no aprendido proporcional a la distancia entre la consulta y la clave,
`softmax(q_i K^T + m · [−(i−1), ..., −1, 0])`, con una pendiente `m` fija por cabeza tomada de una
secuencia geométrica (1/2¹ … 1/2⁸ para 8 cabezas). Se implementa sumando los sesgos a la máscara
causal, que ya se suma antes del softmax, así que no añade operaciones ni parámetros; el único
coste es que la máscara pasa de `L×L` a `n×L×L`.

Los resultados cubren dos escalas. En WikiText-103, el modelo con L = 512 pasa de 19.73 de
perplejidad en Lvalid = 512 a 18.40 en Lvalid = 3072, superando al modelo sinusoidal entrenado
directamente con L = 3072 pese a ser 1.84 veces más rápido de entrenar. Con 1.3B de parámetros
sobre 461 GB (CC100+RoBERTa), el modelo ALiBi con L = 1024 obtiene 8.92 de perplejidad en
Lvalid = 2048 frente a 9.01 del sinusoidal entrenado con L = 2048, usando 3.1 GB menos de memoria;
el sinusoidal con L = 1024 evaluado en 2048 se va a 48.85.

El propio apéndice B acota el alcance del resultado: al reevaluar con ventana deslizante de
stride 1, que da contexto máximo a cada predicción, la perplejidad de ALiBi se mantiene plana en
vez de mejorar con `Lvalid`. Los autores concluyen que la ganancia observada viene de reducir la
*early token curse* (menos predicciones con poco contexto por subsecuencia) y no de que el modelo
aproveche contextos más largos que los vistos en entrenamiento.

**Nota de dominio**: relevante para tdew porque la capa de atención del TCN
(`tdew_estimation/models/attention_pool.py`) es un `nn.MultiheadAttention` sobre la ventana
codificada por el TCN **sin ningún encoding posicional propio** — toda la noción de orden llega
implícita desde las convoluciones dilatadas. ALiBi es la variante más barata de inyectar un sesgo
de recencia explícito en esa capa. El diagnóstico del paper sobre embeddings posicionales
aprendidos también aplica como advertencia si alguna vez se añade uno: dejarían de funcionar al
cambiar la longitud de contexto, y el proyecto entrena con L ∈ {14, 31, 60} días
(`docs/protocol/week1_manifest.yaml`).

## Conceptos derivados

- `[[methods/alibi-linear-attention-bias]]` — la formulación del sesgo, las pendientes por cabeza
  y los detalles de implementación.
- `[[findings/alibi-length-extrapolation-results]]` — las cifras de extrapolación en WikiText-103
  y CC100+RoBERTa, y la acotación del apéndice B.
- `[[patterns/train-short-test-long-evaluation]]` — evaluar con longitudes de entrada mayores que
  las de entrenamiento como protocolo, y la fragilidad de los métodos posicionales frente a eso.
