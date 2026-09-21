# Auditoría independiente del run `week1-tcn-attention` (tdew-x46)

Auditoría ejecutada el 2026-09-21 por un agente separado, en un worktree aislado en el
commit `6102f29` con `Data/`, `mlflow.db` y los checkpoints montados por symlink. El agente
no recibió ninguna conclusión previa, ni acceso al historial de git, a `Wiki/` ni al gestor de
issues, y la única regla sobre las cifras fue que todas salieran de código propio. El objetivo
era doble: explicar el déficit del modelo y comprobar si un diagnóstico hecho antes por otra
vía era replicable.

Scripts en `experiments/tcn/audit_x46/` (19 scripts numerados), salidas en este directorio.
Las submuestras materializadas (`sample_train.npz`, `sample_validation.npz`, 30 MB) no se
versionan; `03_build_sample.py` las regenera con semilla fija.

## Lo que la auditoría estableció primero: la comparación es legítima

Antes de comparar nada se verificó que ambos pipelines puntúan lo mismo (`11_data_checks.py`).
Los conteos de objetivos elegibles recalculados desde `Data/gold/sequence_index/L=31` coinciden
exactamente con la columna `n` del leaderboard (validation ALL = 305,126,781). El RMSE de
climatología implícito en las métricas del run profundo (`val_rmse / (1 − val_skill_vs_clim)`)
reproduce el del leaderboard con una diferencia relativa de −1.6·10⁻¹¹. Y sobre 558,400 pares
de fechas consecutivas de la misma celda, `max |label(d−1) − dynamic[−1](d)| = 0.0`, con el
control sobre `dynamic[−2]` dando 7.31: la ventana termina en `t` y no incluye `t+1`.

## El hallazgo central: memorización habilitada por redundancia espacial

Evaluando el modelo sobre las **mismas celdas** en los tres splits (`13_train_val_gap.py`):

| sitio | RMSE modelo train | RMSE persistencia train | RMSE modelo validation | razón v/t modelo | razón v/t persistencia |
|---|---|---|---|---|---|
| lima | 0.5686 | 0.5893 | 0.6976 | 1.23 | 1.14 |
| cusco | 0.5673 | 0.6439 | 0.7510 | 1.32 | 1.14 |
| tarapoto_san_martin | 0.3438 | 0.5271 | 0.6422 | 1.87 | 1.13 |
| **iquitos_loreto** | **0.1466** | 0.9151 | **1.1059** | **7.54** | 1.12 |

En Loreto el modelo es 6.2 veces mejor que la persistencia sobre el periodo de entrenamiento y
un 8% peor sobre el de validación. El salto ocurre exactamente en la frontera del split:
desglosado por año (`16_loreto_structure.py`), el RMSE del modelo es 0.132–0.158 en cada uno de
los once años de train y 1.054–1.142 en los cuatro siguientes, mientras los estadísticos libres
de modelo no muestran discontinuidad alguna (persistencia 0.818–0.953 contra 0.959–1.027;
autocorrelación de lag 1 entre 0.62 y 0.80 en train contra 0.73–0.76 después, con más variación
*dentro* de train que entre splits).

El mecanismo propuesto, y la medición que lo sostiene (`18_effective_n.py`): el espectro de la
matriz de correlación entre celdas sobre los 5,479 días completos da, para Loreto, correlación
mediana entre celdas de 0.9262, 89.9% de la varianza en el primer componente, 3 componentes
para el 99% y un rango efectivo (participation ratio) de **1.23**.

| sitio | corr. mediana entre celdas | var. 1er componente | comp. para 99% | rango efectivo |
|---|---|---|---|---|
| iquitos_loreto | 0.9262 | 0.8988 | 3 | 1.23 |
| tarapoto_san_martin | 0.8100 | 0.7736 | 7 | 1.62 |
| lima | 0.6923 | 0.6453 | 15 | 2.14 |
| cusco | 0.5389 | 0.5245 | 15 | 2.87 |

Ese orden coincide exactamente con el orden del sobreajuste en muestra (razón
modelo/persistencia sobre train: Loreto 0.154, Tarapoto 0.644, Lima 0.957, Cusco 0.964). Las
305,564 celdas de Loreto son, en grados de libertad, cercanas a una sola serie regional: las
1.22·10⁹ ventanas nominales corresponden a un número de observaciones independientes del orden
de 10⁴. Un modelo de 157,177 parámetros ajusta esa secuencia de once años y no generaliza a las
siguientes.

Tres explicaciones alternativas quedaron descartadas por medición: no hay fuga por
`target_cond` (anular `LST(t+1)` en train mueve el RMSE de Loreto de 0.1466 a 0.1404); la
relación no es lineal-y-presente-en-los-datos (un OLS con las mismas entradas ajustado solo
sobre train de Loreto da 0.8187 **en muestra**); y no es una tabla de consulta frágil (ruido
N(0, 0.05) en los tres canales de anomalía degrada el RMSE de train un 2.8%).

La atribución del mecanismo es inferencia, no medición directa. Lo medido es la discontinuidad
en la frontera del split, la ausencia de cambio en los estadísticos libres de modelo, y el
rango efectivo.

## El reparto real del gradiente, medido sobre la época completa

`05_batches.py` consumió 120 batches reales del `DataLoader` y encontró composición
254.7/256.4/257.5/255.4 por sitio, con reparto del gradiente Lima 43.8%, Tarapoto 30.6%,
Cusco 21.4%, Loreto 4.2%. Pero eso vale solo al **principio** de cada bucket.
`19_gradient_share.py` reconstruyó el flujo completo bucket por bucket y añadió el hecho
decisivo: en un batch homogéneo en sitio, la pérdida `Σw·h / Σw` **cancela el peso por
completo**. La fase equilibrada cubre 26.6% de las muestras de un bucket y la cola de Loreto el
56.1%, así que el reparto por época es:

| sitio | share real por época | si todo batch fuera equilibrado | intención declarada 1/n | frecuencia natural |
|---|---|---|---|---|
| lima | 0.117 | 0.440 | 0.25 | 0.067 |
| cusco | 0.160 | 0.213 | 0.25 | 0.138 |
| iquitos_loreto | **0.594** | 0.042 | 0.25 | 0.700 |
| tarapoto_san_martin | 0.129 | 0.306 | 0.25 | 0.096 |

El cálculo estima 1,699,611 batches por época contra los 1,699,186 pasos reales del checkpoint
(0.025% de error), lo que valida el modelo del flujo. La ponderación por sitio no hace lo que
declara: Loreto recibe 59.4% del gradiente, no el 25% previsto — y eso es precisamente el sitio
con rango efectivo 1.23.

Dato adicional: cada batch de 1024 muestras proviene de solo 8–28 celdas distintas, porque el
búfer de mezcla de 20,000 abarca ~5 celdas por sitio (cada celda aporta 3,987 fechas de train).

## Economía del entrenamiento

`09_economy.py`, leyendo `global_step` de los checkpoints y `epoch_seconds` de `mlflow.db`:
1,699,186 pasos por época (99.975% de las 1,740,401,253 ventanas elegibles: cada época es una
pasada completa), 11.60 h por época, 40.7 pasos/s. Hasta la época 4: 8,495,929 pasos y 8.70·10⁹
ventanas, 55,351 muestras por parámetro. Treinta épocas al ritmo medido son 14.5 días.

`best.pt` guarda `epoch = 0` y ese `best_val_skill = 0.26696` no cambió en ningún checkpoint
posterior. El óptimo se alcanzó al cerrar la primera época y las 46.4 h siguientes lo
degradaron (0.2670 → 0.2612 → 0.2550 → 0.2624 → 0.2360).

## Qué aprendió el modelo, y dónde se pierde la información

Sobre 60,000 ventanas (`06_sensitivity.py`): `corr(label, pred) = 0.684` mientras
`corr(label, TD_anom_norm(t)) = 0.759` — el modelo correlaciona menos con el objetivo que uno
de sus propios canales de entrada. La atención concentra 0.788–0.815 de su masa en `t` y ≤0.020
en cada uno de los 30 rezagos restantes (uniforme sería 0.031). **Poner a cero todo salvo los
últimos 3 días de la ventana mejora el RMSE en 0.055 °C** (0.7835 → 0.7284). Anular
`target_cond` entero cuesta 0.003 °C, y la correlación del objetivo con `LST(t+1)` está entre
0.002 y 0.032 en todos los sitios y splits: la condicionalización del día objetivo es
prácticamente inerte. FiLM: `|gamma|` medio 0.15, `‖pooled‖` 5.11 y `‖gamma·pooled‖` 0.72, o sea
el resumen de la ventana entra a la cabeza atenuado ~7 veces.

Sondas lineales ajustadas sobre 80,000 ventanas de train y evaluadas sobre 120,000 de
validation (`08_probes.py`), RMSE ALL reponderado:

| sonda | n_feat | RMSE |
|---|---|---|
| P0 entradas crudas | 166 | 0.8534 |
| P1 salida del TCN aplanada | 1,995 | 0.9121 |
| P2 tras el pooling por atención | 75 | 0.9104 |
| P3 entrada exacta de la cabeza, FiLM aplicado | 69 | 0.9440 |
| predicción real del modelo | — | 0.9916 |
| P4 sin la ventana | 11 | 1.2952 |
| persistencia | — | 0.9269 |

El codificador cuesta 0.059 °C respecto a las entradas crudas, el pooling no añade pérdida,
FiLM cuesta 0.034 °C y la cabeza real queda 0.048 °C por debajo de una lectura lineal de su
propia entrada. P1 tiene 1,995 regresores sobre 80,000 muestras, así que su valor podría estar
sesgado, pero se evalúa fuera de muestra y el sesgo iría en dirección optimista.

## Un OLS con las mismas entradas supera al TCN y al leaderboard

Sobre la misma submuestra de 559,200 ventanas de validation y reponderando por celdas reales
(`04_compare_predictors.py`), un ajuste por mínimos cuadrados de 166 regresores sobre
exactamente los tensores que recibe el TCN, ajustado en buckets disjuntos:

| predictor | lima | cusco | loreto | tarapoto | ALL reponderado |
|---|---|---|---|---|---|
| climatología | 1.0280 | 1.0394 | 1.4108 | 0.8834 | 1.2989 |
| persistencia | 0.6418 | 0.7574 | 1.0083 | 0.5513 | 0.9204 |
| TCN `best.pt` | 0.6592 | 0.7581 | 1.0435 | 0.5761 | 0.9498 |
| TCN época 4 | 0.6656 | 0.7730 | 1.0912 | 0.5951 | 0.9895 |
| **OLS mismas entradas** | 0.6175 | 0.7042 | 0.9251 | 0.5233 | **0.8479** |
| OLS solo rezagos de TD | 0.6122 | 0.7023 | 0.9353 | 0.5257 | 0.8554 |

La submuestra reproduce el número oficial con 1% de error (0.9498 contra 0.9598), lo que la
valida como sustituto. El OLS supera al TCN por 0.102 °C y también a `generalist_mlr` (0.8632):
la información está en las entradas del modelo profundo.

## Ablación de arquitectura, evaluada sobre celdas no vistas

`10_ablation.py`: cinco variantes, mismos batches, semilla y optimizador, 1,500 pasos de batch
512 sobre 128 celdas, evaluadas sobre 60,000 ventanas de validation de **buckets disjuntos**
(celdas y años no vistos):

| variante | ALL reponderado | loreto |
|---|---|---|
| A arquitectura actual | 0.8587 | 0.9368 |
| B FiLM en identidad | 0.8713 | 0.9517 |
| C residual de persistencia | 0.8565 | 0.9331 |
| D B+C | 0.8533 | 0.9307 |
| E actual con pesos uniformes | 0.8717 | 0.9531 |

Las cinco quedan entre 0.853 y 0.872, al nivel del OLS y muy por encima del run real (0.950),
con diferencias entre ellas del orden del ruido de una sola semilla. La misma arquitectura,
entrenada 1,500 pasos sobre 128 celdas, generaliza a celdas y años no vistos mejor que esa
misma arquitectura entrenada 8,500,000 pasos sobre 436,519 celdas. Medición adicional en el
paso 0: `‖grad input_proj‖ / ‖grad head.0‖` = 0.082 con la FiLM actual y 0.163 con FiLM en
identidad, o sea la modulación multiplicativa sí reduce a la mitad el gradiente que llega al
codificador — sin que eso se traduzca en precisión.

## Objetivo optimizado contra métrica de selección

`07_loss_vs_metric.py` sobre 120,000 residuos: el 13.71% supera δ=1, y concentra el 65.17% del
error cuadrático pero solo el 60.08% de la masa de la pérdida de Huber. La distorsión existe y
va en el sentido esperado, pero es modesta y no explica por sí sola la diferencia con los
baselines. La selección de `best.pt` por `val_skill_vs_clim` es correcta: dentro de un run es
monótona en `val_rmse` porque `clim_rmse` es constante.

Se sospechó que el cómputo en bfloat16 distorsionaba la pérdida, dado que los pesos por sitio
son del orden de 10⁻⁹. `12_loss_numerics.py` comparó float32 contra bfloat16 sobre 60 batches
reales: razón media 1.000117 y norma del gradiente 1.640·10⁻² contra 1.648·10⁻². La precisión
no es el problema.

## Lo que se verificó y estaba bien

La aritmética de normalización e inversión a °C es consistente entre baselines y modelo
profundo. No hay fuga de `t+1` por la ventana dinámica. El campo receptivo (61) cubre L=31. El
`state_dict` de los checkpoints carga sin claves faltantes ni sobrantes.

Dos desviaciones menores del protocolo, ambas medidas como inmateriales: `target_cond` incluye
`LST_DAY` y `LST_NIGHT` del día `t+1`, lo que contradice literalmente el `leakage_constraint`
del manifiesto — los baselines hacen lo mismo con `LST_*_target`, así que la comparación no se
desequilibra, y su correlación con el objetivo es ≤0.032. Y, por la convención de elegibilidad,
la ventana del primer objetivo de validation (2013-01-31) empieza el 2012-12-31, un día dentro
del periodo de train: es entrada pasada, no viola causalidad.

## Veredicto

**Datos**: sanos en integridad, pero su tamaño nominal es engañoso. El desequilibrio 70/14/10/7
entre sitios se combina con redundancia espacial extrema en el sitio mayoritario, y la
metodología actual no reconoce eso en ningún punto.

**Metodología**: causa dominante. El óptimo de validación ocurre en la época 0 y las cuatro
siguientes lo degradan; el mecanismo de ponderación por sitio queda anulado en el 56% de los
batches; cada batch procede de 8–28 celdas; y no hay parada temprana ni validación intra-época.

**Modelo**: contribuye, pero es la causa menor. La cadena de sondas cuantifica su coste en unos
0.10 °C, repartido entre codificador (0.059), FiLM (0.034) y cabeza (0.048), y la atención
colapsa en el último paso. Pero la misma arquitectura alcanza 0.853 en 1,500 pasos, así que no
es lo que impide llegar al nivel de los baselines.

## Correcciones que se derivan, ninguna verificada

1. Validar dentro de la época, no al final. Una evaluación cada ~20,000 pasos sobre un
   subconjunto fijo costaría minutos.
2. Submuestrear Loreto en función de su rango efectivo (1.23 contra 2.87 de Cusco) en lugar de
   ponderar la pérdida, o mantener el round-robin hasta el final del bucket reciclando los
   sitios agotados, de modo que el peso por sitio deje de cancelarse.
3. Aumentar la diversidad de celdas por batch: hoy son 8–28 por paso.
4. Añadir la conexión residual de persistencia, la única variante arquitectónica que mejoró de
   forma consistente.
5. Revisar la ablación de L (`tdew-bs4`) con esta evidencia: truncar la ventana a 3 días mejora
   el modelo entrenado en 0.055 °C.
6. Registrar métricas por sitio y no solo el agregado. La brecha de 7.54× en Loreto es invisible
   en el `val_rmse` agrupado y fue lo que más información aportó.
