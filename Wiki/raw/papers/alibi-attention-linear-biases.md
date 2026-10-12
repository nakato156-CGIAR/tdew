# Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation

- **Venue/año**: ICLR 2022 (conference paper). Preprint: arXiv:2108.12409
  (v1 27-08-2021, v2 22-04-2022 — la versión capturada aquí es la v2, la que sirve el PDF).
- **URL**: https://arxiv.org/abs/2108.12409 — PDF capturado: https://arxiv.org/pdf/2108.12409
- **DOI (preprint)**: https://doi.org/10.48550/arXiv.2108.12409
- **Autores**: Ofir Press (Univ. of Washington / Facebook AI Research), Noah A. Smith
  (Univ. of Washington / Allen Institute for AI), Mike Lewis (Facebook AI Research).
- **Código**: https://github.com/ofirpress/attention_with_linear_biases
- **Fecha de captura**: 2026-09-22
- **Método de captura**: descarga directa del PDF desde arXiv y extracción con `pdftotext -layout`.
  Texto completo disponible, incluidos apéndices A y B.

## Abstract (verbatim, v2)

"Since the introduction of the transformer model by Vaswani et al. (2017), a fundamental
question has yet to be answered: how does a model achieve extrapolation at inference time for
sequences that are longer than it saw during training? We first show that extrapolation can be
enabled by simply changing the position representation method, though we find that current
methods do not allow for efficient extrapolation. We therefore introduce a simpler and more
efficient position method, Attention with Linear Biases (ALiBi). ALiBi does not add positional
embeddings to word embeddings; instead, it biases query-key attention scores with a penalty that
is proportional to their distance. We show that this method trains a 1.3 billion parameter model
on input sequences of length 1024 that extrapolates to input sequences of length 2048, achieving
the same perplexity as a sinusoidal position embedding model trained on inputs of length 2048 but
training 11% faster and using 11% less memory. ALiBi's inductive bias towards recency also leads
it to outperform multiple strong position methods on the WikiText-103 benchmark."

## Definición de extrapolación (§1)

"We define extrapolation as a model's ability to continue performing well as the number of input
tokens during validation increases beyond the number of tokens on which the model was trained."

Notación usada en todo el paper: `L` es la longitud de las subsecuencias de entrenamiento y
`Lvalid` la longitud de las subsecuencias en validación/inferencia.

## Diagnóstico de los métodos posicionales existentes (§2)

Todos los experimentos de esta sección modifican un único modelo base (Baevski & Auli, 2018)
entrenado sobre WikiText-103, cambiando solo el método posicional:

- **Sinusoidal** (Vaswani et al., 2017): vectores constantes no aprendidos sumados a los
  embeddings de token en la entrada de la primera capa. Entrenado con L = 512, la perplejidad
  mejora hasta k = 20 tokens extra, se mantiene plana entre k = 20 y k = 50, y después se
  degrada. Con L = 1024 mejora hasta Lvalid = L + 50 y luego cae.
- **Rotary** (Su et al., 2021, popularizado por GPT-J): multiplica claves y consultas de cada
  capa de atención por embeddings sinusoidales; inyecta posición en todas las capas y no en los
  valores. Mejora: el modelo con L = 512 (L = 1024) sigue mejorando hasta k = 200 (k = 100)
  tokens extra, a costa de entrenamiento e inferencia más lentos.
- **T5 bias** (Raffel et al., 2020): método relativo que suma un sesgo aprendido y compartido a
  cada score query-key en función de la distancia, con distancias grandes compartiendo el mismo
  sesgo. Es el mejor de los baselines — mejora hasta k = 600 (k = 800) tokens extra para
  L = 512 (L = 1024) — pero el entrenamiento es al menos dos veces más lento que el sinusoidal.
  Los autores señalan que esa lentitud anula la ventaja: el modelo sinusoidal con L = 1024 corre
  a 28.5k palabras/segundo mientras que el T5 bias con L = 512 corre a 14.4k WPS, así que
  entrenar corto y extrapolar no ahorra tiempo.
- El método de embeddings posicionales **aprendidos** no tiene forma de codificar posiciones
  mayores que L, por lo que no puede extrapolar en absoluto (nota al pie 4).

## El método ALiBi (§3)

Sin embeddings posicionales en ningún punto de la red. La única modificación ocurre después del
producto punto query-key, donde se suma un sesgo estático y **no aprendido**:

```
softmax(q_i K^T + m · [−(i−1), ..., −2, −1, 0])
```

- `m` es una pendiente fija por cabeza, definida antes del entrenamiento.
- Para modelos de 8 cabezas las pendientes son la secuencia geométrica
  1/2¹, 1/2², ..., 1/2⁸. Para 16 cabezas se interpolan promediando geométricamente cada par
  consecutivo, dando la secuencia que empieza en 1/√2 con razón 1/√2. En general, para n
  cabezas, la secuencia geométrica que empieza en 2^(−8/n) y usa ese mismo valor como razón.
- Los autores reportan que ese conjunto de pendientes funciona en dominios de texto y tamaños de
  modelo distintos sin retuneo, igual que los hiperparámetros del método sinusoidal se fijaron
  una vez y se reutilizaron. Hacer las pendientes entrenables **no** dio buena extrapolación (y
  frenó el entrenamiento un 3%). La exploración manual (~diez conjuntos de pendientes) indicó que
  las que funcionan están en el rango (0, 1) con densidad creciente cerca de 0, y que el método
  es robusto a esa elección: incluso muestrear de una distribución exponencial funcionó en
  algunos casos, aunque con alta varianza.
- ALiBi tiene un **sesgo inductivo hacia la recencia**: penaliza los scores entre pares
  query-key distantes, y las distintas cabezas aumentan su penalización a ritmos distintos según
  la magnitud de la pendiente.
- Como método relativo, añade información de posición en cada capa a claves y consultas pero no
  a los valores, igual que el T5 bias y rotary. Los autores hipotetizan que esas propiedades
  favorecen la extrapolación.
- **Implementación**: se modifica la matriz de máscara sumándole los sesgos lineales (la máscara
  causal ya se suma al producto query-key antes del softmax), de modo que no se añade ninguna
  operación y no hay penalización de runtime. El coste es de memoria: la máscara pasa de L×L a
  n×L×L (n = número de cabezas), hasta 100 MB extra en sus experimentos. El sesgo de ALiBi no se
  multiplica por el factor de escala √d_k.

## Resultados en WikiText-103 (§4.1)

- Sin extrapolar, para cada L los modelos ALiBi superan a los sinusoidales. Con L = 3072, el
  modelo de Baevski & Auli obtiene 18.67 ± 0.24 (desv. est.) de perplejidad y el modelo ALiBi
  17.60, ambos evaluados con Lvalid = 3072.
- El modelo ALiBi entrenado con L = 512 obtiene 19.73 de perplejidad evaluando con
  Lvalid = 512, y **18.40** al extrapolar a Lvalid = 3072 — superando al modelo sinusoidal
  entrenado con L = 3072 por un margen estadísticamente significativo. Ese modelo es 1.84 veces
  más rápido de entrenar y cabe en una GPU con mucha menos memoria (el sinusoidal con L = 3072
  requiere más de 16 GB).
- Comparado con los baselines: el T5 bias mejora perplejidad hasta Lvalid ≈ 2L; ALiBi sigue
  mejorando hasta al menos ≈ 3L, y el modelo con L = 512 mejora incluso con Lvalid por encima de
  12k tokens.
- Con evaluación de ventana deslizante, el modelo ALiBi con L = 3072 supera a Transformer-XL,
  Sandwich y Shortformer; queda a la par de staged training y por debajo de Routing Transformer y
  kNN-LM (métodos que los autores consideran ortogonales al suyo).
- Los hiperparámetros (las pendientes) se transfieren sin modificación al dominio de libros
  (Toronto Book Corpus, apéndice A.3).

## Resultados en CC100+RoBERTa, 1.3B parámetros (§4.2)

Corpus de 461 GB (161 GB del corpus de entrenamiento de RoBERTa + 300 GB de la parte en inglés de
CC-100); validación de 649K tokens. Modelos de 25 capas, 16 cabezas, dimensión 2048, dimensión
oculta del feedforward 8192, 1.3B parámetros, entrenados una época = 50k updates sobre 128 GPUs
V100.

Table 11 (cada par corre el mismo tiempo de entrenamiento):

| Modelo | Memoria | Updates | Horas | PPL (Lvalid=1024) | PPL (Lvalid=2048) |
|---|---|---|---|---|---|
| Sinusoidal, L=1024 | 26.2 GB | 46.7k | 5.5k | 9.24 | — |
| ALiBi, L=512 | 24.6 GB | 50.0k | 5.5k | 9.30 | — |
| Sinusoidal, L=2048 | 29.3 GB | 44.2k | 5.9k | — | 9.01 |
| ALiBi, L=1024 | 26.2 GB | 50.0k | 5.9k | — | **8.92** |

Table 12 (todos con 50k updates), que muestra el colapso del método sinusoidal al extrapolar:

| Modelo | Memoria | Horas | PPL@512 | PPL@1024 | PPL@2048 |
|---|---|---|---|---|---|
| Sinusoidal, L=512 | 24.6 GB | 5.5k | 9.71 | 37.05 | 105.42 |
| ALiBi, L=512 | 24.6 GB | 5.5k | 9.79 | 9.30 | 9.54 |
| Sinusoidal, L=1024 | 26.2 GB | 5.9k | — | 9.15 | 48.85 |
| ALiBi, L=1024 | 26.2 GB | 5.9k | — | 9.16 | 8.92 |
| Sinusoidal, L=2048 | 29.3 GB | 6.7k | — | — | 8.83 |
| ALiBi, L=2048 | 29.4 GB | 6.7k | — | — | 8.84 |

- El modelo ALiBi con L = 1024 mantiene ventaja sobre el sinusoidal con L = 2048 durante todo el
  entrenamiento y alcanza un valor dado de perplejidad, en promedio (cinco puntos equiespaciados
  del entrenamiento), 11% más rápido, usando 3.1 GB menos de memoria.
- En este régimen grande, ALiBi rinde *similar* al sinusoidal cuando no extrapola (9.79 vs 9.71
  con L = 512; 9.16 vs 9.15 con L = 1024; 8.84 vs 8.83 con L = 2048), a diferencia de los
  datasets pequeños donde lo superaba. Los autores sugieren que el sesgo inductivo de ALiBi
  aporta beneficios adicionales en modelado de lenguaje de bajos recursos.
- El pico de rendimiento al extrapolar está alrededor de 2L: el modelo con L = 512 (9.79 en
  Lvalid = 512) alcanza su mejor score, 9.3, en Lvalid = 1012; el de L = 1024 (9.16) alcanza 8.9
  en Lvalid = 2024. Explicación propuesta por los autores: con subsecuencias de longitud 2L, la
  mitad de las subsecuencias consumidas son tan largas como las vistas en entrenamiento; a partir
  de 2L+1, menos de la mitad de las predicciones ocurren sobre longitudes vistas.
- El modelo sinusoidal no extrapola en absoluto en este escenario: se degrada en cuanto se añade
  un token más que L.

## Análisis: la extrapolación reduce la "early token curse" (apéndice B)

- **Early token curse** (Press et al., 2021): al partir el conjunto de evaluación en
  subsecuencias, las predicciones tempranas de cada subsecuencia no acceden a los tokens de
  contexto que quedaron al final de la subsecuencia anterior, lo que degrada la perplejidad. El
  workaround es evaluar con ventana deslizante, que es mucho más lento.
- Dos explicaciones posibles de la mejora al aumentar Lvalid: (1) el modelo aprovecha contextos
  más largos; (2) simplemente sufre menos la early token curse (con Lvalid = 1000, el 10% de las
  predicciones tienen ≤ 100 tokens de contexto; con Lvalid = 2000, solo el 5%).
- Al reevaluar WikiText-103 con ventana deslizante de stride S = 1 (contexto máximo para cada
  predicción), la perplejidad de los modelos ALiBi **se mantiene plana** al aumentar Lvalid en
  vez de mejorar, mientras que la del sinusoidal explota igual que antes. Los autores concluyen
  que la explicación correcta es la (2), y lo dicen explícitamente: "our analysis reveals that
  when Lvalid > L, ALiBi might not be using contexts longer than the ones it was trained on".
  El comportamiento del T5 bias con ventana deslizante es equivalente.

## Trabajo relacionado señalado por los autores (§5)

- Wennberg & Henter (2021), en paralelo: sesgo de atención en función de la distancia pero con
  función de base radial y parámetros entrenables; solo clasificación de texto, sin extrapolación.
- Distance Aware Transformer (Wu et al., 2021): **multiplica** los scores por un sesgo función de
  la distancia, con un parámetro aprendido por cabeza. En los experimentos de ALiBi (no
  presentados en el paper), multiplicar en vez de sumar degradó el rendimiento.
- Transformer-XL (Dai et al., 2019) atiende a más tokens en inferencia vía caché, pero solo
  reporta con salida limitada a L y su método posicional es muy lento. Longformer (Beltagy et
  al., 2020) necesita entrenar parcialmente sobre secuencias largas; ALiBi no requiere ningún
  entrenamiento adicional sobre secuencias largas.
