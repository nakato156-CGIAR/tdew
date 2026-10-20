# A1: desglose de la comparación TimesFM frente a LLR y `tuned`

Bead `tdew-03g`. Script: `experiments/amenazas/desglose.py`
(`uv run python -m experiments.amenazas.desglose`). Salidas en esta carpeta:
`a1_por_metodo.csv`, `a1_por_zona.csv`, `a1_victorias_zona.csv` y `a1_brechas.csv`, cada
una con su `.provenance.json`. Las tablas entre los marcadores se regeneran en cada
corrida; el texto fuera de ellos se escribe a mano y debe revisarse si cambian.

## Qué se midió

Bloques `ll4` (contexto hasta 2012, prueba 2013-2016) y `ll4b` (contexto hasta 2008,
prueba 2009-2012), sobre las 17.027 celdas de
`reports/timesfm_benchmark/panels/nacional_17027.csv` y las mismas 24.876.447 filas
(celda × día) para todos los métodos. Métodos: climatología (`clim`), método de
Palacios con recetas por zona seleccionadas solo con años de entrenamiento (`tuned`),
LLR simple sobre la anomalía de Tmin (`llr_simple`), LLR con Tmin y rezagos
(`llr_rezagos`), TimesFM 3.0 zero-shot con objetivo Td (`timesfm_td`, solo `ll4b`) y con
objetivo anomalía (`timesfm_anom`). `tuned` sin rezagos de Td y TimesFM con mediana
entran solos cuando existan sus parquet.

Ámbito «Perú»: las 8.272 celdas del panel que caen dentro del país según
`experiments.timesfm.artifact_data.peru_mask`, es decir `shapely.contains_xy` sobre la
unión de los contornos de `reports/timesfm_benchmark/geo/peru_departamental_simple.geojson`
evaluada en el centro de cada celda de la rejilla de 0,01°. Es la misma máscara que
dio 8.272 dentro y 8.755 fuera (bead `tdew-214.8`); la prueba
`tests/test_amenazas_desglose.py` comprueba ese conteo. Dentro del Perú quedan 32 de
las 33 zonas del panel: «Lago Titicaca» no tiene celdas dentro.

El RMSE macro por zona es el promedio simple de los RMSE de cada zona SENAMHI; da a
cada zona el mismo peso, de modo que zonas con 1 o 3 celdas (dos casos en el ámbito
Perú) pesan igual que la que tiene 2.147. Los intervalos son percentiles 2,5 y 97,5
de 2.000 réplicas (semilla 0) de un bootstrap que remuestrea bloques completos con
sus sumas de error cuadrático: bloques espaciales de 2° × 2° de lon/lat (74 en el
panel, 45 en el Perú) o bloques mes-año (48). Las réplicas son las mismas para todas
las parejas, de modo que la comparación es pareada. El bloque espacial no recoge la
dependencia temporal y el mes-año no recoge la espacial; ninguno cubre ambas, y el
más ancho de los dos es la lectura prudente.

<!-- tablas:inicio -->
### RMSE y sesgo por método, bloque `ll4` (°C)

| método | ámbito | RMSE | sesgo | RMSE macro por zona | 2013 | 2014 | 2015 | 2016 |
|---|---|---|---|---|---|---|---|---|
| clim | panel (17.027) | 1,535 | −0,363 | 1,249 | 1,393 | 1,391 | 1,648 | 1,684 |
| tuned | panel (17.027) | 1,228 | −0,033 | 0,901 | 1,149 | 1,186 | 1,245 | 1,324 |
| llr_simple | panel (17.027) | 1,175 | −0,010 | 0,874 | 1,143 | 1,152 | 1,172 | 1,231 |
| llr_rezagos | panel (17.027) | 1,161 | +0,025 | 0,861 | 1,137 | 1,148 | 1,142 | 1,215 |
| timesfm_anom | panel (17.027) | 1,154 | +0,104 | 0,802 | 1,205 | 1,127 | 1,080 | 1,199 |
| clim | Perú (8.272) | 1,262 | −0,301 | 1,226 | 1,123 | 1,147 | 1,372 | 1,381 |
| tuned | Perú (8.272) | 0,944 | +0,010 | 0,884 | 0,883 | 0,932 | 0,973 | 0,985 |
| llr_simple | Perú (8.272) | 0,912 | +0,009 | 0,861 | 0,870 | 0,905 | 0,921 | 0,950 |
| llr_rezagos | Perú (8.272) | 0,897 | +0,059 | 0,847 | 0,868 | 0,901 | 0,890 | 0,929 |
| timesfm_anom | Perú (8.272) | 0,865 | +0,050 | 0,787 | 0,858 | 0,861 | 0,836 | 0,903 |

### RMSE y sesgo por método, bloque `ll4b` (°C)

| método | ámbito | RMSE | sesgo | RMSE macro por zona | 2009 | 2010 | 2011 | 2012 |
|---|---|---|---|---|---|---|---|---|
| clim | panel (17.027) | 1,362 | −0,300 | 1,115 | 1,241 | 1,426 | 1,409 | 1,363 |
| tuned | panel (17.027) | 1,122 | −0,156 | 0,825 | 1,035 | 1,127 | 1,117 | 1,202 |
| tuned_sin_td | panel (17.027) | 1,108 | −0,124 | 0,808 | 1,050 | 1,103 | 1,091 | 1,184 |
| llr_simple | panel (17.027) | 1,098 | −0,140 | 0,798 | 1,027 | 1,095 | 1,096 | 1,171 |
| llr_rezagos | panel (17.027) | 1,089 | −0,117 | 0,793 | 1,032 | 1,089 | 1,076 | 1,156 |
| timesfm_td | panel (17.027) | 1,106 | +0,035 | 0,769 | 1,185 | 1,081 | 1,062 | 1,092 |
| timesfm_anom | panel (17.027) | 1,046 | −0,108 | 0,745 | 1,026 | 1,021 | 1,034 | 1,102 |
| clim | Perú (8.272) | 1,087 | −0,203 | 1,083 | 1,013 | 1,137 | 1,089 | 1,106 |
| tuned | Perú (8.272) | 0,861 | −0,060 | 0,808 | 0,796 | 0,852 | 0,841 | 0,947 |
| tuned_sin_td | Perú (8.272) | 0,856 | −0,034 | 0,792 | 0,813 | 0,847 | 0,830 | 0,929 |
| llr_simple | Perú (8.272) | 0,849 | −0,056 | 0,782 | 0,796 | 0,843 | 0,835 | 0,916 |
| llr_rezagos | Perú (8.272) | 0,844 | −0,028 | 0,778 | 0,801 | 0,835 | 0,821 | 0,912 |
| timesfm_td | Perú (8.272) | 0,840 | −0,003 | 0,750 | 0,867 | 0,819 | 0,813 | 0,859 |
| timesfm_anom | Perú (8.272) | 0,804 | −0,085 | 0,729 | 0,774 | 0,776 | 0,789 | 0,874 |

### Brechas pareadas RMSE(A) − RMSE(B) con IC 95 % (°C; negativo favorece a A)

| bloque | ámbito | A − B | brecha | IC bloques espaciales 2° | IC bloques mes-año |
|---|---|---|---|---|---|
| ll4 | panel (17.027) | timesfm_anom − llr_rezagos | −0,007 | [−0,017; +0,001] | [−0,038; +0,023] |
| ll4 | panel (17.027) | timesfm_anom − llr_simple | −0,021 | [−0,031; −0,012] | [−0,053; +0,010] |
| ll4 | panel (17.027) | timesfm_anom − tuned | −0,074 | [−0,080; −0,069] | [−0,140; −0,015] |
| ll4 | panel (17.027) | tuned − llr_simple | +0,053 | [+0,044; +0,062] | [+0,017; +0,097] |
| ll4 | panel (17.027) | tuned − llr_rezagos | +0,067 | [+0,058; +0,075] | [+0,029; +0,114] |
| ll4 | Perú (8.272) | timesfm_anom − llr_rezagos | −0,032 | [−0,044; −0,021] | [−0,047; −0,018] |
| ll4 | Perú (8.272) | timesfm_anom − llr_simple | −0,047 | [−0,058; −0,036] | [−0,063; −0,031] |
| ll4 | Perú (8.272) | timesfm_anom − tuned | −0,079 | [−0,087; −0,071] | [−0,109; −0,052] |
| ll4 | Perú (8.272) | tuned − llr_simple | +0,032 | [+0,021; +0,043] | [+0,016; +0,050] |
| ll4 | Perú (8.272) | tuned − llr_rezagos | +0,047 | [+0,036; +0,058] | [+0,026; +0,071] |
| ll4b | panel (17.027) | timesfm_anom − llr_rezagos | −0,043 | [−0,047; −0,039] | [−0,062; −0,026] |
| ll4b | panel (17.027) | timesfm_anom − llr_simple | −0,052 | [−0,057; −0,048] | [−0,073; −0,033] |
| ll4b | panel (17.027) | timesfm_anom − tuned | −0,076 | [−0,084; −0,068] | [−0,102; −0,050] |
| ll4b | panel (17.027) | tuned − llr_simple | +0,024 | [+0,020; +0,027] | [+0,009; +0,039] |
| ll4b | panel (17.027) | tuned − llr_rezagos | +0,033 | [+0,028; +0,037] | [+0,019; +0,046] |
| ll4b | panel (17.027) | timesfm_td − llr_simple | +0,007 | [−0,001; +0,015] | [−0,042; +0,059] |
| ll4b | panel (17.027) | tuned_sin_td − tuned | −0,014 | [−0,017; −0,011] | [−0,027; +0,000] |
| ll4b | panel (17.027) | tuned_sin_td − llr_simple | +0,010 | [+0,007; +0,012] | [−0,003; +0,022] |
| ll4b | panel (17.027) | timesfm_anom − tuned_sin_td | −0,062 | [−0,068; −0,056] | [−0,084; −0,043] |
| ll4b | Perú (8.272) | timesfm_anom − llr_rezagos | −0,039 | [−0,046; −0,033] | [−0,050; −0,029] |
| ll4b | Perú (8.272) | timesfm_anom − llr_simple | −0,044 | [−0,050; −0,039] | [−0,057; −0,033] |
| ll4b | Perú (8.272) | timesfm_anom − tuned | −0,056 | [−0,065; −0,049] | [−0,073; −0,040] |
| ll4b | Perú (8.272) | tuned − llr_simple | +0,012 | [+0,008; +0,016] | [+0,002; +0,024] |
| ll4b | Perú (8.272) | tuned − llr_rezagos | +0,017 | [+0,014; +0,021] | [+0,007; +0,027] |
| ll4b | Perú (8.272) | timesfm_td − llr_simple | −0,009 | [−0,020; +0,002] | [−0,037; +0,019] |
| ll4b | Perú (8.272) | tuned_sin_td − tuned | −0,005 | [−0,008; −0,001] | [−0,014; +0,005] |
| ll4b | Perú (8.272) | tuned_sin_td − llr_simple | +0,007 | [+0,003; +0,011] | [−0,000; +0,015] |
| ll4b | Perú (8.272) | timesfm_anom − tuned_sin_td | −0,052 | [−0,058; −0,045] | [−0,064; −0,040] |

### Zonas en que el método de la fila gana al de la columna, `ll4`, panel (17.027) (33 zonas)

| A \ B | clim | tuned | llr_simple | llr_rezagos | timesfm_anom |
|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 |
| tuned | 33 | — | 4 | 0 | 0 |
| llr_simple | 33 | 29 | — | 5 | 1 |
| llr_rezagos | 33 | 33 | 28 | — | 1 |
| timesfm_anom | 33 | 33 | 32 | 32 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4`, Perú (8.272) (32 zonas)

| A \ B | clim | tuned | llr_simple | llr_rezagos | timesfm_anom |
|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 |
| tuned | 32 | — | 6 | 0 | 0 |
| llr_simple | 32 | 26 | — | 4 | 0 |
| llr_rezagos | 32 | 32 | 28 | — | 0 |
| timesfm_anom | 32 | 32 | 32 | 32 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4b`, panel (17.027) (33 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | timesfm_td | timesfm_anom |
|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 33 | — | 3 | 5 | 1 | 3 | 0 |
| tuned_sin_td | 33 | 30 | — | 12 | 1 | 5 | 0 |
| llr_simple | 33 | 28 | 21 | — | 12 | 4 | 0 |
| llr_rezagos | 33 | 32 | 32 | 21 | — | 6 | 0 |
| timesfm_td | 33 | 30 | 28 | 29 | 27 | — | 3 |
| timesfm_anom | 33 | 33 | 33 | 33 | 33 | 30 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4b`, Perú (8.272) (32 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | timesfm_td | timesfm_anom |
|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 32 | — | 5 | 6 | 1 | 3 | 0 |
| tuned_sin_td | 32 | 27 | — | 12 | 1 | 3 | 0 |
| llr_simple | 32 | 26 | 20 | — | 10 | 4 | 0 |
| llr_rezagos | 32 | 31 | 31 | 22 | — | 6 | 0 |
| timesfm_td | 32 | 29 | 29 | 28 | 26 | — | 3 |
| timesfm_anom | 32 | 32 | 32 | 32 | 32 | 29 | — |

<!-- tablas:fin -->

## Lectura

TimesFM con objetivo anomalía tiene el RMSE agregado más bajo en los dos bloques y en
los dos ámbitos. Frente al rival propio más fuerte, el LLR con rezagos, la brecha es
de −0,007 °C en `ll4` sobre el panel, con intervalos que incluyen el cero en ambos
esquemas; en `ll4b` es de −0,043 °C y ningún intervalo incluye el cero. Restringida al
Perú, la brecha en `ll4` crece a −0,032 °C [−0,047; −0,018] con bloques mes-año, de
modo que la brecha pequeña de `ll4` en el panel proviene de las celdas fuera del país,
donde el LLR con rezagos queda por delante.

El año 2013 explica esa diferencia. En el panel, TimesFM es el peor de los cuatro
métodos de regresión ese año (1,205 contra 1,137 del LLR con rezagos), mientras que
dentro del Perú es el mejor (0,858 contra 0,868). Con un solo bloque por período no
se puede separar si esto es propio de 2013 o de la región fuera del Perú; queda como
observación.

Las clasificaciones por zona son más estables que las agregadas: `timesfm_anom` gana
al LLR con rezagos en 32 de 33 zonas en `ll4` y en todas en `ll4b`, y la diferencia
en RMSE macro por zona es mayor que la agregada (0,802 contra 0,861 en `ll4`, −0,059
frente a −0,007). Es consistente con una ventaja de TimesFM mayor en las zonas con
pocas celdas que en las que dominan el promedio por celdas.

`tuned` queda detrás de los dos LLR propios en todos los cortes: frente al LLR simple
la brecha es de +0,053 °C en `ll4` y +0,024 °C en `ll4b` sobre el panel, con intervalos
que excluyen el cero, y el LLR simple gana en 29 y 28 de 33 zonas. Dentro del Perú la
brecha se reduce a +0,032 y +0,012 °C. El sesgo de TimesFM cambia de signo entre bloques
(+0,104 en `ll4`, −0,108 en `ll4b` sobre el panel); el del LLR simple es negativo en
ambos (−0,010 y −0,140).

`tuned` sin rezagos de Td (`tuned_sin_td`) solo está disponible para `ll4b` en esta
corrida. Quitarle los rezagos de Td baja su RMSE de 1,122 a 1,108 °C en el panel
(−0,014; el intervalo mes-año llega a cero) y lo deja a +0,010 °C del LLR simple; en
el Perú la mejora es de −0,005. TimesFM sigue por delante en −0,062 °C. Falta `ll4`
para saber si el efecto se repite.

Dos salvedades. La variante `tmin_anom_full` de TimesFM se eligió entre nueve sobre
el bloque `ll4` (bead `tdew-214.11.8`); `ll4b` no participó en esa elección, por lo que
es la medición menos expuesta a ese sesgo de selección y es la que da la ventaja más
clara. Y el LLR propio es una reimplementación independiente que no ha revisado
Palacios.
