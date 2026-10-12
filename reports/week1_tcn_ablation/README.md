# Ablación correctiva del TCN+atención (bead `tdew-x46.1`)

Experimento corto para decidir si tres cambios propuestos tras el diagnóstico del run
`week1-tcn-attention` (L=31, seed=0) corrigen el déficit del modelo frente a los baselines.
Resultado resumido: **dos de los tres cambios no tuvieron efecto medible, el tercero fue
perjudicial, y el único que cambió el cuadro fue el que no era una hipótesis sobre el modelo
sino sobre cómo se mide.**

## Qué se comparó

Cuatro variantes, todas con el mismo seed, el mismo orden de datos, el mismo presupuesto de
8,000 pasos (batch 1024) y la misma submuestra de validación:

| variante | cambia |
|---|---|
| `current` | nada — reproduce la configuración con la que corrió el entrenamiento largo |
| `residual` | la cabeza predice el residuo sobre `TD_anom_norm(t)` y arranca en cero |
| `residual+film` | además, FiLM como `(1+gamma)*h + beta` con generador inicializado en cero |
| `residual+film+uniform` | además, pesos de sitio uniformes en lugar de `1/n_train_rows(site)` |

La submuestra de validación son 40,000 ventanas por sitio (160,000 en total), fija y
compartida por las cuatro variantes, tomada del split `validation` del mismo
`Data/gold/model_features_norm`. El RMSE agrupado repondera el MSE de cada sitio por su
número de filas en la validación real, porque la submuestra está balanceada 1:1:1:1 y la
validación real es ~70% Loreto.

Sobre esas mismas ventanas, climatología da 1.2925 y persistencia 0.9200 de RMSE agrupado
(la validación completa da 1.3093 y 0.9305, así que la submuestra es ligeramente más fácil,
en un factor de 0.989).

## Trayectoria (RMSE agrupado, °C)

| paso | `current` | `residual` | `residual+film` | `+uniform` |
|---|---|---|---|---|
| 0 | 1.3138 | 0.9200 | 0.9200 | 0.9200 |
| 1000 | **0.8593** | **0.8542** | **0.8588** | 0.9165 |
| 2000 | 0.8685 | 0.8698 | 0.8802 | 0.9242 |
| 3000 | 0.8770 | 0.8807 | 0.8895 | 0.9409 |
| 4000 | 0.8760 | 0.8934 | 0.9045 | 0.9397 |
| 5000 | 0.8820 | 0.8950 | 0.9008 | 0.9273 |
| 6000 | 0.8837 | 0.9049 | 0.9040 | **0.9145** |
| 7000 | 0.8930 | 0.9109 | 0.9160 | 0.9216 |
| 8000 | 0.8950 | 0.9150 | 0.9041 | 0.9169 |

Las tres variantes con cabeza residual arrancan exactamente en persistencia (0.9200), que es
lo que la inicialización en cero garantiza por construcción.

## Qué se concluye

**El cambio que importa es el ciclo de medición, no la arquitectura.** Las tres primeras
variantes tocan su mínimo en el paso 1000 con 0.8593, 0.8542 y 0.8588: una dispersión de
0.005 entre configuraciones supuestamente muy distintas, frente a una distancia de 0.066
hasta persistencia. En el mejor punto, `current` ya supera a persistencia en los cuatro
sitios sobre las mismas ventanas (lima 0.6132 vs 0.6454, cusco 0.6427 vs 0.6929, iquitos
0.9512 vs 1.0189, tarapoto 0.4912 vs 0.5210). Corregido por el factor 0.989 de dificultad de
la submuestra, 0.854 equivale a ~0.864 en la validación completa, es decir la paridad con
`generalist_mlr` (0.8632), no una mejora sobre él.

**La cabeza residual y la reparametrización de FiLM no aportan nada medible aquí.** La
diferencia entre `current`, `residual` y `residual+film` en su mejor punto cabe dentro de
0.005. La hipótesis de que el modelo quedaba por debajo de persistencia porque le faltaba una
ruta de identidad hacia el último lag, y porque FiLM con `gamma` cerca de cero atenuaba el
encoder temporal, **no se sostiene** con esta evidencia. La cabeza residual sí garantiza un
piso: el modelo sin entrenar es persistencia exacta en vez de 1.3138. Eso tiene valor como
propiedad de robustez, no como fuente de precisión.

**Los pesos de sitio uniformes empeoran el resultado**, y en la dirección contraria a la
prevista. La hipótesis era que `weight = 1/n_train_rows(site)`, aplicado encima de un sampler
que ya entrega batches 25/25/25/25 por round-robin, dejaba a Loreto en 4.2% del gradiente
siendo ~70% de la validación agrupada, y que igualar los pesos lo corregiría. Lo medido es lo
opuesto: con pesos uniformes el mejor punto empeora de 0.859 a 0.915, y **Loreto es el sitio
que más se degrada** (1.0161 contra 0.9512 de `current`), pese a pasar de 4.2% a 25% del
gradiente. El mecanismo propuesto queda refutado; por qué la ponderación desigual ayuda no se
explica con estas mediciones.

**El hallazgo robusto es la degradación monótona.** Las cuatro variantes empeoran de forma
sostenida después de su mínimo, y lo hacen con configuraciones de pérdida y de arquitectura
distintas. Eso reproduce, en 8,000 pasos, lo mismo que el entrenamiento largo mostró a lo
largo de cinco épocas (val_rmse 0.9598 → 1.0003). El déficit del run largo no es falta de
capacidad ni de entrenamiento: es que el punto en que se lo evaluó está muy pasado del óptimo.
Con validación cada 11.6 h no había forma de verlo.

## Límites de este experimento

Un solo seed, una sola submuestra de validación y evaluación cada 1,000 pasos, así que el
óptimo real podría estar antes del paso 1000 y las diferencias de 0.005 entre las tres
primeras variantes no son distinguibles del ruido de seed. El entrenamiento usa 4 de los 64
`id_bucket`, de modo que las 8.2M ventanas por variante caen enteras dentro de la fase
balanceada del round-robin. Nada de esto está replicado con seeds independientes.

## Seguimiento pendiente

Queda sin explicar por qué el modelo se degrada de forma monótona pasado el paso ~1000, y esa
es ahora la pregunta que manda. Una hipótesis compatible con los datos, **no verificada**: la
climatología y las estadísticas de normalización se estiman sobre 2002-2012, y la validación
2013-2014 tiene mayor varianza de anomalía (RMSE de climatología 1.3093 contra una desviación
estándar de `TD_anom` de 1.1116 en train), así que un encogimiento óptimo para el periodo de
entrenamiento queda mal calibrado para el de validación, y cuanto más se optimiza sobre train
peor se ajusta ese encogimiento. Verificarlo requiere medir el encogimiento efectivo del
modelo a lo largo del entrenamiento y contrastarlo con el óptimo de cada periodo.

## Reproducir

```bash
uv run python -m experiments.tcn.ablation_x46_1 --steps 8000 --eval-every 1000 --val-per-site 40000
```

Salidas: `ablation_history.csv` (una fila por variante y paso de evaluación),
`ablation_summary.csv` (punto final de cada variante más las filas de referencia del
leaderboard) y un run de MLflow por variante, `x46.1-ablation-<variante>`.
