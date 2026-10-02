# Benchmark de TimesFM contra el método de Palacios y la TCN

Comparación de TimesFM 3 zero-shot con los dos modelos que este proyecto ya tiene
medidos para reconstruir el punto de rocío diario, bajo el mismo protocolo, las
mismas celdas, los mismos días y las mismas métricas.

> **Estado: medición cerrada** el 23 de septiembre de 2026. Los cuatro niveles
> —cribado, backtest, departamental y escala— están ejecutados y verificados.
> Antes de citar cualquier número, leer [`TRACEABILITY.md`](TRACEABILITY.md), que
> dice de dónde sale cada uno. Los resultados también están en una página
> interactiva: [`artifact/index.html`](artifact/index.html).
>
> **Actualización del 2 de octubre de 2026.** Las cifras del nivel backtest y del
> cribado se recalcularon contra el run limpio de Palacios (`backtest_clean`, 17.027
> celdas), cuya selección de recetas usa solo los años de entrenamiento. Las cifras
> anteriores, calculadas contra un run cuya selección vio los años 1981–2016, se
> conservan en las rutas sin sufijo y se resumen en la subsección «Referencia: run
> con fuga». Las tablas departamental y de escala no se recalcularon: su `tuned`
> sigue usando selección con fuga y no es comparable con las cifras limpias. El
> cambio queda registrado en
> [`docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml`](../../docs/protocol/timesfm_manifest_addendum_2026-10-02.yaml).

## Qué se compara

TimesFM es un modelo de fundación para series de tiempo entrenado por Google. Aquí
no se entrena ni se ajusta: se le entrega el historial de Td de cada celda, la
temperatura mínima del período que hay que rellenar, y se le piden los años
faltantes. La pregunta es si un modelo general de 330 millones de parámetros, sin
ver un solo dato de este problema durante su entrenamiento, alcanza a un método
diseñado específicamente para él.

Los rivales, todos puntuados sobre las mismas celdas y los mismos días:

| método | qué es |
|---|---|
| climatología | la media histórica de cada día del año en cada celda, calculada solo con los años de entrenamiento. Es el piso: lo que se hace hoy para rellenar huecos. |
| Td = Tmin | usar la temperatura mínima sin transformar. |
| `zone_ols` | una recta `Td ~ a + b·Tmin` por zona climática SENAMHI. |
| **`tuned`** | **el método que Palacios propone en el paper.** Regresión local ponderada por celda y día del año sobre anomalías, con kernel tricube y selección de receta por zona × día del año. Predice el bloque oculto de forma autorregresiva. |
| **TimesFM** | el modelo de fundación, sin entrenar, con la misma información de entrada. |
| **TCN directa** | la red convolucional de reconstrucción continua del proyecto, congelada en `exogenous_full`, L=7, 250 pasos. Solo en el panel departamental. |

La covariable que recibe TimesFM es Tmin y solo Tmin, porque es exactamente la
información que consume el método de Palacios. Igualar la entrada hace que la
comparación mida el modelo y no el acceso a datos.

## Bajo qué protocolo

Los bloques de años no se inventaron aquí: son los mismos que define
`HPC_code_tunning/backtest.py` y bajo los que Palacios reporta sus cifras.

| bloque | entrena | predice (oculto) | días |
|---|---|---|---|
| `ll1` | 1981–2015 | 2016 | 366 |
| `ll2` | 1981–2014 | 2015–2016 | 731 |
| `ll4` | 1981–2012 | 2013–2016 | 1.461 |

`ll4` es el que imita el hueco real de cuatro años que hay que rellenar
(2017–2020) y el que reporta el paper: RMSE 1,228 °C del método de Palacios contra
1,535 °C de la climatología, sobre 17.027 celdas.

Ningún valor de Td del bloque oculto llega al modelo, ni directamente ni a través
de la climatología. Tmin sí, porque es exógeno, existe en todo el rango y el método
de Palacios también lo usa.

## Las nueve variantes

TimesFM no se entrena, pero sí hay que decidir qué se le pide: qué serie predecir,
qué covariables recibe, cuánto pasado ve y qué interruptores de inferencia se
activan. Se probaron nueve configuraciones independientes entre sí.

| variante | objetivo | covariables | contexto | particularidad |
|---|---|---|---|---|
| `uni_td_full` | Td | — | 1981–2012 | cuánta señal temporal queda a 1.461 días |
| `uni_anom_full` | anomalía de Td | — | 1981–2012 | el objetivo sin ciclo estacional |
| `tmin_td_full` | Td | Tmin | 1981–2012 | la comparación directa contra Palacios |
| `tmin_anom_full` | anomalía de Td | anomalía de Tmin | 1981–2012 | todo expresado en anomalías |
| `tmin_doy_td_full` | Td | Tmin + seno/coseno del día del año | 1981–2012 | el modelo no tiene indicador de frecuencia; aquí se le da el calendario a mano |
| `tmin_td_med` | Td | Tmin | 2002–2012 | contexto de 11 años |
| `tmin_td_short` | Td | Tmin | 2011–2012 | contexto de 2 años |
| `tmin_td_symavg` | Td | Tmin | 1981–2012 | promediado simétrico, que duplica el cómputo |
| `tmin_td_znorm` | Td | Tmin | 1981–2012 | z-score externo además de la normalización interna |

Los pesos de TimesFM 3.0 se distribuyen bajo `timesfm-non-commercial-license-v1.0`,
que restringe el despliegue en producción y la generación de ingresos. El alcance de
este benchmark es investigación, sin despliegue operativo, condición bajo la cual la
licencia permite el uso de los pesos.

### Cómo leer la cifra de la variante ganadora

Las nueve variantes se evaluaron sobre el mismo bloque que después se reporta, por
decisión explícita del usuario, sin un fold de desarrollo previo. Eso significa que
la cifra de la ganadora incluye la ventaja de haber probado nueve configuraciones
contra el mismo examen. La magnitud de esa ventaja se mide y se publica junto al
resultado, en lugar de quedar como advertencia sin cuantificar. Palacios hizo la
comprobación equivalente sobre su propia reselección de recetas y obtuvo 0,0088 de
skill (`PAPER_PLAN.md:275`).

Se reportan dos cifras distintas, porque miden cosas distintas:

- **Dispersión entre variantes** (mejor contra mediana). Mezcla decisiones de
  diseño genuinas —con covariable y sin ella, contextos de 2 y de 32 años— con el
  ruido de la selección, así que sobreestima el sesgo.
- **Brecha con la segunda** (mejor contra runner-up). Es la que responde si la
  ganadora es intercambiable. Si esa brecha cae dentro de la incertidumbre del
  propio RMSE, dado por el intervalo bootstrap por celda, la elección entre las dos
  primeras es arbitraria y así debe decirse.

## Los cuatro niveles de medición

| nivel | celdas | para qué |
|---|---|---|
| cribado | 1.092 puntuadas, de 1.106 estratificadas por zona SENAMHI | comparar las nueve variantes entre sí |
| backtest | 17.027, las del run limpio de Palacios (TimesFM predijo 17.041; 14 quedan fuera de la referencia) | la comparación pareada contra la cifra publicada |
| departamental | 8.192, el panel `ll4` del protocolo de reconstrucción | la única mesa donde la TCN es comparable |
| escala | 436.519, los cuatro departamentos completos | costo y estabilidad a volumen real |

## Costo medido

En la RTX A2000 de 12 GB, 45 combinaciones de contexto × horizonte × tamaño de
lote, con covariable y cuantiles activados
([`coste_throughput.csv`](coste_throughput.csv),
[figura](figs/coste_throughput.png)):

| contexto (días) | horizonte 366 d | horizonte 731 d | horizonte 1.461 d |
|---|---|---|---|
| 731 | 40,8 celdas/s | 32,4 | 21,1 |
| 4.018 | 10,5 | 9,9 | 9,2 |
| 11.688 | 3,9 | 3,4 | 3,2 |

Lo que gobierna el costo es la longitud del contexto, no el tamaño del lote: pasar
de lote 8 a lote 16 mejora menos del 5 % en todas las combinaciones. No hubo un solo
desbordamiento de memoria y el pico fue de 2,39 GB sobre 12 disponibles, de modo que
el cuello no es la memoria.

Sobre ese barrido se probaron tres aceleraciones y solo una funcionó. **Activar
TF32 da 1,44×**, porque PyTorch trae `float32_matmul_precision='highest'` y con eso
los núcleos TF32 de Ampere quedan apagados para la multiplicación de matrices, que
es donde el modelo pasa casi todo su tiempo; el precio numérico es un RMSE de
0,00043 °C entre ambas precisiones, siete órdenes por debajo del efecto medido.
Subir el lote no sirve. Repartir el trabajo entre procesos concurrentes empeora
las cosas: tres procesos dieron 4,59 celdas/s agregadas contra 5,39 de uno solo con
la tarjeta para sí, un 15 % menos. La tarjeta
está limitada por potencia —`SW Power Cap` activo, 70 W que es además el máximo del
firmware, reloj sostenido en 1.627 de 2.100 MHz— así que repartir el trabajo no
crea vatios nuevos. El detalle está en [`limitaciones.md`](limitaciones.md).

Con TF32 activo, el ritmo medido a volumen real es de 5,09 celdas/s: unos 56 minutos
para las 17.041 celdas del backtest, 23 h 48 min para las 436.519 de los
cuatro departamentos —cronometradas, no estimadas— y unos 6,4 días para los
2,8 millones del grid nacional. El método de Palacios cubre el grid completo en
20 minutos.

Un supuesto del sondeo exploratorio del 21 de septiembre resultó equivocado: no
existe un tope de horizonte de 1.000 días. Ese límite viene de la ficha del modelo,
no del paquete; en el código el horizonte solo se redondea al múltiplo de 64
superior. Los 1.461 días del bloque 2013–2016 salen en una sola pasada, sin partir
ni realimentar.

## Resultados

### Comparación contra la cifra publicada

Sobre las 17.027 celdas del run limpio de Palacios y los 24.876.447 pares
observación–predicción del bloque 2013–2016, que es la muestra de la que sale la
cifra del paper ([`nacional_limpio/leaderboard.csv`](nacional_limpio/leaderboard.csv),
[figura](figs/escalera_nacional_limpio.png)):

> **Este agregado no es un promedio del Perú.** El marco de muestreo del backtest
> sortea buckets sobre la caja envolvente del producto PISCO, no sobre el territorio
> peruano, de modo que **8.755 de esas 17.027 celdas —el 51,4 %— caen en Brasil,
> Bolivia, Ecuador o Colombia**. Se verificó celda a celda con `shapely.contains_xy`
> sobre los contornos departamentales (8.272 dentro del Perú). Las 14 celdas que el
> run limpio no tiene estaban todas dentro del Perú, por lo que el porcentaje no
> cambia respecto del panel de 17.041 celdas. No es un artefacto introducido aquí ni
> invalida ninguna comparación, porque todos los métodos se puntúan sobre las mismas
> celdas y los mismos días y las cifras del paper salen de esa misma muestra, pero
> obliga a no llamar «nacional» a este nivel sin más. La zona «Lago Titicaca» aporta
> 256 celdas muestreadas y ninguna dentro del Perú. Queda anotado como bead
> `tdew-214.8`. El panel limpio cubre 33 de las 41 zonas SENAMHI.

| método | RMSE °C | MAE | sesgo | r | skill vs. clim |
|---|---|---|---|---|---|
| **TimesFM** (`tmin_anom_full`) | **1,1536** | 0,8298 | +0,1044 | 0,9913 | **0,2485** |
| Palacios (`tuned`) | 1,2279 | 0,8810 | −0,0327 | 0,9902 | 0,2001 |
| climatología | 1,5352 | 1,1363 | −0,3627 | 0,9855 | 0 |
| `zone_ols` | 2,3285 | 1,7422 | +0,0853 | 0,9640 | −0,5167 |
| Td = Tmin | 3,5505 | 2,7347 | −2,1255 | 0,9461 | −1,3128 |

Las filas de `tuned` y climatología reproducen 1,228 y 1,535 de
`backtest_clean/metrics_all.csv` con diferencia absoluta cero (n = 24.876.447 en
`ll4`), La
fusión no perdió celdas de la referencia: 17.027 de 17.027. Se descartaron 14 celdas
de TimesFM que la referencia no tiene.

Inferencia pareada con bootstrap de ubicación (1.000 remuestreos de celdas) y test
de permutación por cambio de signo (5.000, semilla 0)
([`effect_sizes_all.csv`](nacional_limpio/effect_sizes_all.csv)):

| comparación | ΔRMSE °C | IC 95 % | skill | celdas ganadas | d de Cohen | p |
|---|---|---|---|---|---|---|
| TimesFM vs. Palacios | +0,0743 | [0,074, 0,075] | 0,0605 | 99,24 % | 2,07 | 0,0002 |
| TimesFM vs. climatología | +0,3815 | [0,380, 0,383] | 0,2485 | 100 % | 2,97 | 0,0002 |
| TimesFM vs. `zone_ols` | +1,1748 | [1,156, 1,192] | 0,5045 | 100 % | 1,14 | 0,0002 |
| TimesFM vs. Td = Tmin | +2,3969 | [2,374, 2,419] | 0,6751 | 100 % | 1,42 | 0,0002 |

TimesFM gana en 16.897 de las 17.027 celdas. El valor de `p` es el mínimo
alcanzable con 5.000 permutaciones. El ΔRMSE y su intervalo son diferencias de RMSE
agregado; el `p`, la d de Cohen y el porcentaje de celdas ganadas se calculan sobre
los ΔRMSE por celda. Los intervalos tratan las celdas como independientes y no
descuentan la autocorrelación espacial, de modo que probablemente son optimistas.
Para referencia, la ventaja de `tuned` sobre climatología es ΔRMSE +0,3072 con skill
0,2001; la de TimesFM sobre climatología es mayor.

#### Cómo se comporta cada método al alargar el horizonte

Los tres bloques, sobre las mismas 17.027 celdas
([figura](figs/nacional_curva_horizonte_limpio.png)):

| bloque | horizonte | TimesFM | Palacios | climatología | skill TimesFM | skill Palacios |
|---|---|---|---|---|---|---|
| `ll1` | 366 d | 1,1736 | 1,2538 | 1,6803 | 0,3015 | 0,2538 |
| `ll2` | 731 d | 1,1533 | 1,2765 | 1,6667 | 0,3080 | 0,2341 |
| `ll4` | 1.461 d | 1,1536 | 1,2279 | 1,5352 | 0,2485 | 0,2001 |

El skill del método de Palacios decae al alargar el bloque —0,254, 0,234, 0,200— y
el propio paper lo describe como crecimiento esperado del error. El de TimesFM no
sigue esa pendiente: se sostiene entre 0,30 y 0,31 en uno y dos años y solo cae en
el bloque de cuatro. En términos operativos, TimesFM a cuatro años alcanza un skill
cercano al del método de Palacios a uno (0,249 frente a 0,254).

La ventaja no es igual de sólida en los tres bloques, y la cifra agregada lo esconde:

| bloque | ΔRMSE vs. Palacios | IC 95 % | celdas ganadas | d de Cohen |
|---|---|---|---|---|
| `ll1` | +0,0802 | [0,079, 0,082] | 77,8 % | 0,74 |
| `ll2` | +0,1231 | [0,122, 0,124] | 98,9 % | 1,91 |
| `ll4` | +0,0743 | [0,074, 0,075] | 99,2 % | 2,07 |

A un año de horizonte TimesFM gana en tres de cada cuatro celdas, no en 99 de cada
100, y la d de Cohen baja de 2,07 a 0,74, a un tercio. Es consistente con el mecanismo: a un
año la predicción autorregresiva de Palacios todavía no ha acumulado deriva. Frente
a la referencia con fuga, la ventaja en `ll1` baja de 0,0883 a 0,0802; en `ll2` y
`ll4` sube. Entre ambos runs cambiaron a la vez los años de selección y la rejilla
de `h` (el run limpio usa {7, 11, 15, 21, 31, 45}), y no se separó el efecto de cada
uno.

Dos matices más. El primero es el sesgo: TimesFM queda en +0,104 °C y `tuned` en
−0,033 °C, de modo que gana en error cuadrático y pierde en centrado. El segundo es
el mecanismo, visible en la curva de error acumulado
([figura](figs/crecimiento_error_nacional_limpio.png)): TimesFM va por delante
hasta el día 164; entre el día 165 y el día 717 `tuned` tiene la ventaja, con algunos cruces breves
entre los días 698 y 717, y de hasta 0,11 °C de RMSE acumulado el día 219; desde el
día 718 TimesFM vuelve a liderar. Al
cierre del bloque el acumulado es 1,154 contra 1,228.

#### Referencia: run con fuga

Las cifras publicadas antes del 2 de octubre de 2026 se calcularon contra
`$RES/tuning/backtest`, un run cuya selección de recetas vio los años 1981–2016,
incluido el bloque que luego se evalúa. Sobre ese run con fuga, con 17.041 celdas y
24.896.901 pares en `ll4`, el RMSE de `tuned` era 1,2194 (frente a 1,2279 limpio) y
el ΔRMSE de TimesFM contra `tuned`, 0,0658 (frente a 0,0743). Los archivos de esa
medición se conservan sin cambios en `nacional/`, `cribado/`,
`curva_error_nacional.csv`, `curva_error_cribado.csv` y `figs/` sin sufijo. Esas
rutas no deben citarse como resultado vigente.

### Soporte observacional

Las 17.027 celdas se reparten en cinco tiers según su distancia al dominio SENAMHI
(`support_distance.parquet`, los mismos del paper): dentro, 0–50, 50–100, 100–200 y más
de 200 km. TimesFM y `tuned` se puntúan sobre las mismas celdas y días en `ll4`
([CSV completo](nacional_limpio/tiers_limpio.csv), con `ll1`, `ll2`, climatología,
Td = Tmin y OLS por zona):

| tier | celdas | RMSE TimesFM | RMSE `tuned` | RMSE climatología | sesgo TimesFM | sesgo `tuned` | skill TimesFM | skill `tuned` |
|---|---|---|---|---|---|---|---|---|
| within | 8.306 | 0,867 | 0,946 | 1,264 | +0,050 | +0,010 | 0,314 | 0,251 |
| near | 1.779 | 1,061 | 1,139 | 1,464 | +0,068 | −0,079 | 0,275 | 0,222 |
| marginal | 1.433 | 1,198 | 1,276 | 1,582 | +0,143 | −0,044 | 0,242 | 0,193 |
| extrapolated | 2.563 | 1,298 | 1,374 | 1,682 | +0,149 | −0,070 | 0,228 | 0,183 |
| unsupported | 2.946 | 1,652 | 1,724 | 2,036 | +0,223 | −0,089 | 0,188 | 0,153 |

El RMSE de `tuned` coincide con `tbl-tiers` del paper a tres decimales. TimesFM
tiene menor RMSE que `tuned` en los cinco tiers, con una diferencia de 0,079 en
`within` que baja a 0,072 en `unsupported`. Ambos métodos empeoran hacia afuera del
dominio y el orden de los tiers es el mismo para los dos. El sesgo de TimesFM crece
con la distancia (de +0,050 a +0,223 °C) y el de `tuned` se mantiene entre −0,09 y
+0,01 °C. La tabla reducida para el texto está en
[`tiers_texto_limpio.md`](nacional_limpio/tiers_texto_limpio.md).

El cribado limpio repite el cálculo sobre 1.092 celdas
([CSV](cribado_limpio/tiers_cribado_limpio.csv)). Esa muestra es estratificada por
zona y 842 de las 1.092 celdas son `within` (79 `near`, 59 `marginal`, 65
`extrapolated`, 47 `unsupported`), de modo que sus cifras por tier no estiman el
campo completo. Se usan solo como verificación: TimesFM queda por debajo de `tuned`
en RMSE en los cinco tiers, el mismo orden del panel nacional.

### Sesgo mensual

Sesgo medio (`pred − obs`, °C) por mes calendario de `FECHA`, agregado sobre todas
las celdas-día del mes en `ll4`. La columna de dispersión es la desviación estándar
entre celdas del sesgo medio por celda y mes
([CSV](nacional_limpio/sesgo_mensual_limpio.csv), con `ll1` y `ll2` en valor pooled):

| mes | TimesFM | `tuned` | desv. entre celdas TimesFM | desv. entre celdas `tuned` |
|---|---|---|---|---|
| enero | −0,325 | −0,402 | 0,335 | 0,505 |
| febrero | +0,061 | +0,005 | 0,175 | 0,153 |
| marzo | +0,248 | +0,146 | 0,267 | 0,157 |
| abril | +0,263 | +0,146 | 0,218 | 0,136 |
| mayo | +0,112 | −0,034 | 0,186 | 0,210 |
| junio | +0,151 | −0,137 | 0,233 | 0,223 |
| julio | +0,210 | −0,051 | 0,255 | 0,218 |
| agosto | +0,255 | +0,030 | 0,277 | 0,191 |
| septiembre | +0,193 | −0,029 | 0,291 | 0,237 |
| octubre | −0,098 | −0,145 | 0,198 | 0,208 |
| noviembre | +0,100 | +0,070 | 0,150 | 0,234 |
| diciembre | +0,089 | +0,017 | 0,153 | 0,206 |

El diciembre de `tuned` (+0,017) reproduce el +0,02 que cita el paper para la
selección por zona × día del año, y su máximo |sesgo| es 0,402 en enero. TimesFM
tiene un sesgo cálido de 0,11 a 0,26 °C entre marzo y septiembre (+0,06 en
febrero) y un máximo |sesgo| de 0,325 en enero. Solo en enero y octubre su sesgo
absoluto es menor que el de `tuned`. La dispersión entre celdas (0,14 a 0,51 °C; TimesFM de 0,15 a 0,33 y `tuned`
de 0,14 a 0,51) es del mismo orden que el sesgo pooled, así que el promedio nacional oculta
variación espacial. El sesgo por mes × tier de los cinco métodos está en
[`sesgo_mes_tier_limpio.csv`](nacional_limpio/sesgo_mes_tier_limpio.csv).

`tiers_texto_limpio.md` usa el formato numérico en inglés de `tbl-tiers` del paper
(punto decimal, coma de miles), porque está pensado para pegarse en ese texto. La
figura mensual opcional del plan (barras de sesgo con banda p05–p95) no se generó;
el pooled de TimesFM sigue disponible en `nacional_limpio/ll4_bias_by_month.png`.

Las predicciones de TimesFM están almacenadas en float32; todos los agregados de
estas dos secciones se calculan en float64. Promediar en float32 cambiaría el sesgo
mensual de TimesFM en hasta 1,7·10⁻⁸ °C (8·10⁻⁹ °C en `tuned`), sin efecto en las
cifras publicadas, y el cálculo en float64 evita depender de ello.

### Cribado de las nueve variantes

Sobre las 1.092 celdas que el panel de cribado (1.106 celdas estratificadas por zona)
comparte con el run limpio ([`cribado_limpio/leaderboard.csv`](cribado_limpio/leaderboard.csv),
[figura](figs/escalera_cribado_limpio.png)). La variante `tmin_td_25` se retiró del
protocolo el 25 de septiembre y no se puntúa. Las columnas de velocidad vienen de la
medición de costo sobre las 1.106 celdas originales, que no depende de la referencia:

| variante | RMSE | skill | celdas/s | pasada nacional |
|---|---|---|---|---|
| `tmin_anom_full` | **0,8389** | 0,3467 | 3,3 | 9,8 días |
| `tmin_doy_td_full` | 0,8621 | 0,3286 | 1,9 | 17,2 días |
| `tmin_td_symavg` | 0,8640 | 0,3271 | 1,6 | 20,2 días |
| `tmin_td_znorm` | 0,8718 | 0,3210 | 3,2 | 10,2 días |
| `tmin_td_full` | 0,8718 | 0,3210 | 3,4 | 9,7 días |
| `tmin_td_med` | 0,8794 | 0,3151 | 7,8 | 4,2 días |
| *Palacios (`tuned`)* | *0,9326* | *0,2736* | — | — |
| `tmin_td_short` | 0,9476 | 0,2620 | 18,5 | 1,8 días |
| `uni_anom_full` | 1,2780 | 0,0047 | 5,1 | 6,5 días |
| *climatología* | *1,2840* | *0* | — | — |
| `uni_td_full` | 1,3124 | −0,0221 | 5,1 | 6,5 días |

El orden de las dos primeras variantes no cambia respecto del cribado con fuga
(`tmin_anom_full` seguida de `tmin_doy_td_full`), de modo que la elección de la
variante ganadora se mantiene. El cribado limpio cubre 33 zonas.

Cuatro cosas quedan medidas.

**La covariable Tmin no es un refinamiento, es la condición de entrada.** Sin ella
ninguna cantidad de contexto alcanza a la climatología: 1,3124 sobre Td crudo y
1,2780 sobre anomalías, contra 1,2840 de la media histórica. Un modelo de 330
millones de parámetros entrenado con más de un billón de puntos llega, a 1.461 días
de horizonte, a la misma conclusión que la media por día del año.

**Quitarle la estacionalidad al problema sale gratis y ayuda más que explicársela.**
Expresar objetivo y covariable en anomalías gana 0,033 °C sobre la versión en Td
crudo; entregarle el día del año como seno y coseno gana 0,010 °C y casi duplica el
costo. Ambas atacan lo mismo, que el modelo no tiene noción de calendario, y la
primera lo hace mejor y sin cómputo adicional.

**El contexto tiene un umbral, no una pendiente suave.** Con 2 años de historia
TimesFM queda por debajo del método de Palacios (0,9476 contra 0,9326); con 11 años
lo supera (0,8794); con 32 años gana 0,008 °C más. El cruce está entre 2 y 11 años,
y a partir de 11 los rendimientos se agotan.

**El promediado simétrico y el z-score externo no compensan.** El primero gana
0,0078 °C duplicando el cómputo. El segundo no cambia nada: ambas variantes dan el
mismo RMSE (0,8718) y, en la comparación hecha sobre las 1.615.866 predicciones del
cribado original de 1.106 celdas, la diferencia máxima es 4·10⁻⁵ °C, ruido de punto
flotante. Es coherente con la equivarianza afín
que declara el paquete, pero la documentación no advierte que la bandera sea inocua.

Sobre el sesgo de haber elegido la mejor de nueve sobre el mismo bloque: la
dispersión entre variantes es de 0,033 °C y la brecha con la segunda, de 0,023 °C
([`cribado_limpio/sesgo_seleccion_ll4.csv`](cribado_limpio/sesgo_seleccion_ll4.csv)).
El cribado no tiene intervalo bootstrap, por lo que esa brecha no se compara con la
incertidumbre del RMSE; la elección entre las dos primeras debe leerse con esa
reserva.

### Calibración probabilística

Solo aplica a TimesFM: climatología, `tuned` y la TCN son deterministas. Sobre las
1.092 celdas del cribado limpio, con los nueve deciles
([figura](figs/calibracion_cribado_limpio.png)):

| variante | CRPS aprox. | cobertura del 80 % | anchura °C |
|---|---|---|---|
| `tmin_anom_full` | 0,4788 | 0,818 | 2,02 |
| `tmin_doy_td_full` | 0,4919 | 0,821 | 2,10 |
| `tmin_td_full` | 0,4984 | 0,832 | 2,18 |
| `uni_td_full` | 0,7675 | 0,777 | 3,02 |

La variante ganadora cubre el 81,8 % de las observaciones en un intervalo nominal
del 80 %, con cero cruces de cuantiles. Las variantes sin covariable tienen
intervalos un 50 % más anchos, lo que es consistente con que el modelo reconoce su
propia incertidumbre cuando no tiene información que explotar. El intervalo del
80 % es el más ancho que se puede formar, porque no hay q05 ni q95.

### Panel departamental, con la TCN

> El `tuned` de este panel usa la selección de recetas con fuga (manifiesto de recetas
> con los años 1981–2016), no la del run limpio. Estas cifras no son comparables con
> las del nivel backtest limpio. La re-corrida con selección limpia queda para un
> punto posterior.

Sobre 2.048 celdas de los cuatro departamentos y los 1.461 días del bloque oculto
2013–2016, con semilla 0 de la TCN. Falta añadir el método de Palacios sobre estas
mismas celdas, que está en cola, y las semillas 1 y 2.

| método | RMSE °C | MAE | sesgo | r | skill vs. clim | fuera de rango QC |
|---|---|---|---|---|---|---|
| **TimesFM** | **0,7996** | 0,5919 | +0,0704 | 0,9953 | **0,3010** | 0,12 % |
| TCN directa | 0,8484 | 0,6267 | +0,0474 | 0,9948 | 0,2584 | 0,08 % |
| climatología | 1,1440 | 0,8638 | −0,2587 | 0,9910 | 0 | 0,03 % |

Por departamento, RMSE en °C:

| departamento | TimesFM | TCN | climatología |
|---|---|---|---|
| Cusco | 0,6807 | 0,7369 | 0,9909 |
| Lima | 0,7104 | 0,7743 | 1,0643 |
| Loreto | 1,0909 | 1,1333 | 1,5089 |
| San Martín | 0,6320 | 0,6724 | 0,9183 |

El macro por departamento, que da el mismo peso a los cuatro en lugar de dejar que
Loreto domine, mantiene el orden: 0,7785 para TimesFM contra 0,8292 de la TCN.

Prueba pareada por celda (1.000 remuestreos, 5.000 permutaciones): ΔRMSE
−0,0488 °C con intervalo [−0,0505, −0,0470] a favor de TimesFM, que gana en el
**96,2 %** de las 2.048 celdas, con p de permutación 0,0002. El RMSE mediano por
celda es 0,714 contra 0,763. La fracción de celdas ganadas se verificó por un
segundo camino, calculando el error cuadrático medio por celda y contando
directamente.

Un contraste que conviene registrar: TimesFM produce algo más de predicciones fuera
del rango de control de calidad de PISCO, −25 a 30 °C, que la TCN —0,12 % contra
0,08 %—, y ambas más que la climatología. Es poco, pero va en la dirección
esperable de un modelo que no conoce las restricciones físicas del problema.

Dos precisiones sobre la composición de esta mesa, ambas por límites de memoria de
la máquina y no por decisión de diseño.

Dos precisiones sobre la composición de esta mesa, ambas por límites de memoria de
la máquina y no por decisión de diseño.

El panel es de **512 celdas por departamento**, no las 2.048 que fija el protocolo
de reconstrucción. Es un subconjunto estricto del panel `ll4` y coincide con el
conjunto de celdas que usaron los folds de desarrollo. La comparación sigue siendo
válida porque todos los competidores se puntúan sobre las mismas celdas, pero el
panel del protocolo queda sin ejercitar a su tamaño nominal.

**Ridge e HistGradientBoosting quedan fuera de esta tabla.** Las dos agotaron los
125 GB de RAM de la máquina y el núcleo las eliminó sin que escribieran salida.
La causa no es el tamaño del panel —reducirlo a la cuarta parte bajó el consumo de
99,9 GB a 94— sino que `run_baseline` (`experiments/reconstruction/cli.py:34-57`)
no pasa por la caché de features y materializa la matriz de diseño densa de
scikit-learn sobre los 23,9 millones de filas de entrenamiento por unas 59 columnas
en float64, con varias copias dentro del `ColumnTransformer`. La TCN no está
afectada porque entrena por minilotes, que es también la razón por la que los folds
de desarrollo no detectaron el problema: se corrieron con `--model tcn`. Queda
registrado en el bead `tdew-x46.3.6`.

### Prueba de escala

> El `tuned` de esta prueba usa la selección de recetas con fuga (manifiesto de recetas
> con los años 1981–2016), no la del run limpio. Estas cifras no son comparables con
> las del nivel backtest limpio. La re-corrida con selección limpia queda para un
> punto posterior.

TimesFM predijo los 1.461 días de las **436.519 celdas** de Lima, Cusco, Loreto y
San Martín, sin hueco, entre el 22 y el 23 de septiembre de 2026. La pasada tardó
23 h 48 min a 5,09 celdas/s sostenidas y escribió 26,9 GB
([`escala/leaderboard.csv`](escala/leaderboard.csv)).

La puntuación se hace sobre la **submuestra proporcional de 61.113 celdas** que el
método de Palacios alcanzó —el 14 % de cada departamento, de modo que Loreto sigue
dominando el agregado igual que en el grid completo—, porque la unión con el rival
es interna y restringir a esas celdas da exactamente el mismo resultado que
puntuarlas por separado. Son 89.286.093 pares observación–predicción, tres veces y
media más que la comparación contra la cifra publicada.

**Agregado de los cuatro departamentos**, reponderado por el número real de celdas
de cada uno:

| método | RMSE °C | MAE | sesgo | skill vs. clim |
|---|---|---|---|---|
| **TimesFM** | **0,9983** | 0,7414 | +0,104 | **0,2824** |
| Palacios (`tuned`) | 1,0681 | 0,7881 | −0,031 | 0,2322 |
| climatología | 1,3911 | 1,0426 | −0,391 | 0 |

**Por departamento**, sobre las mismas celdas y los mismos días:

| departamento | celdas | TimesFM | Palacios | climatología | skill TimesFM |
|---|---|---|---|---|---|
| Cusco | 8.406 | **0,6623** | 0,7281 | 1,0296 | 0,3568 |
| Lima | 4.071 | **0,7118** | 0,7722 | 1,0765 | 0,3388 |
| Loreto | 42.779 | **1,1111** | 1,1823 | 1,5259 | 0,2718 |
| San Martín | 5.857 | **0,6322** | 0,7203 | 0,9268 | 0,3179 |

La ventaja se sostiene al pasar de las 2.048 celdas del panel departamental a la
cobertura completa, y en los cuatro departamentos sin excepción. El sesgo sigue la
misma dirección que en el resto del trabajo: TimesFM gana en error cuadrático
(+0,104 °C de sesgo) y pierde en centrado frente al método de Palacios (−0,031 °C).

Las dos líneas base débiles quedan, sobre esa misma submuestra, en `zone_ols`
1,7805 y Td = Tmin 2,9526. `zone_ols` no es comparable con el de la corrida
nacional: al restringir por celdas esa línea base se reajusta solo con las celdas
restringidas, como advierte el propio parche `--ids-csv`. Climatología y `tuned` son
por celda y no se ven afectados.

#### Por qué la submuestra y no las 436.519 celdas

La corrida del método de Palacios sobre el grid departamental completo **no
terminó**: el núcleo la eliminó con `rc=137` en el bucket 8.190 de 8.192, tras
3 h 14 min y unos 100 GB de memoria, sin escribir salida. La causa está en
`backtest.py`: `run_backtest` acumula un marco por bucket y `_finalize_split` los
concatena, de modo que los 637,8 millones de filas ocupan unos 50 GB en la lista y
otros 50 al concatenar, con las dos copias vivas a la vez; encima se aplican dos
`.map(lambda)` de Python sobre esas 637 millones de filas. El backtest publicado
corre sobre 24,9 millones de filas y nunca lo expuso.

Queda registrado como bead `tdew-x46.8` con prioridad alta, porque el protocolo
`production` son 2.818.404 celdas, 6,5 veces más que lo que ya falló, y el llenado
de producción existente sí escala porque escribe bucket a bucket.

#### Costo medido a volumen real

Ya no es una extrapolación del banco de pruebas: la pasada se cronometró entera.
TimesFM procesó las 436.519 celdas a **5,09 celdas/s** sostenidas con TF32 y
contexto completo, es decir **23 h 48 min**. El banco había anticipado 4,6 celdas/s
y unas 26 horas, de modo que la extrapolación se quedó un 11 % corta. Al mismo
ritmo medido, el grid nacional de 2.818.404 celdas costaría **6,4 días**.

El método de Palacios cubrió sus 61.113 celdas en 70 minutos y el grid nacional
completo en 20 minutos según el registro de producción del proyecto. La diferencia
de costo entre ambos enfoques es de dos a tres órdenes de magnitud.

## Limitaciones de TimesFM

Doce limitaciones, cada una anclada a una línea del paquete instalado o a una
medición hecha aquí: [`limitaciones.md`](limitaciones.md). Las que más pesan para
este proyecto:

- No hay indicador de frecuencia ni conciencia de calendario. La estacionalidad
  anual solo entra por la longitud del contexto o por covariables construidas a
  mano.
- Los cuantiles llegan hasta el decil, de modo que el intervalo de predicción más
  ancho que se puede formar es del 80 %. No se puede reportar cobertura al 90 % ni
  al 95 %.
- Varios comportamientos cambian el resultado sin producir error: el ancho de la
  covariable futura redefine el horizonte, un contexto demasiado largo se recorta
  por la izquierda, los huecos se interpolan linealmente sin señal de dato faltante
  y el recorte de negativos está activado por defecto en el evaluador.
- Los pesos de la versión 3.0 no permiten uso comercial ni productivo. Este
  benchmark queda dentro de lo permitido porque su alcance es investigación, sin
  despliegue operativo; un uso futuro en producción requeriría revisar esta
  licencia de nuevo.

## Contenido del directorio

| archivo | qué contiene |
|---|---|
| `TRACEABILITY.md` | de dónde sale cada número y cómo reproducirlo |
| `limitaciones.md` | las doce limitaciones con su evidencia en el código |
| `coste_throughput.csv` | el barrido de costo, 45 combinaciones |
| `nacional_limpio/` | métricas, tamaños de efecto y desglose por zona sobre las 17.027 celdas del run limpio |
| `cribado_limpio/` | las nueve variantes y los rivales sobre las 1.092 celdas comunes del cribado y el run limpio |
| `nacional_limpio/tiers_*.csv`, `sesgo_mensual_limpio.csv`, `sesgo_mes_tier_limpio.csv` | desempeño por tier de soporte y sesgo mensual (`by_tier_month.py`) |
| `cribado_limpio/*_cribado_limpio.csv` | los mismos cálculos sobre las 1.092 celdas del cribado, solo como verificación |
| `nacional/`, `cribado/` | la medición con fuga (17.041 y 1.106 celdas), conservada como referencia |
| `departamental/` | la mesa con la TCN: cinco niveles de agregación y tests pareados |
| `escala/leaderboard.csv` | los cuatro departamentos completos, por sitio y reponderado |
| `panels/` | las listas de celdas de cada nivel |
| `geo/` | los contornos departamentales y su procedencia |
| `artifact/` | la página interactiva y sus datos embebidos |
| `figs/` | las figuras |

## Nota sobre uso de IA

La implementación, la ejecución y el análisis se hicieron con asistencia de Claude
Code. Las cifras provienen de ejecuciones reales sobre los datos del proyecto y los
controles previos son reproducibles. Las decisiones de protocolo las tomó el
usuario. Conviene validar las conclusiones con el equipo antes de tomarlas como
definitivas, conforme a la política de uso de IA del CIP.
