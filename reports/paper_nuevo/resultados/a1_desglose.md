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
objetivo anomalía (`timesfm_anom`, variante `tmin_anom_full`, contexto desde 1981).
Desde esta corrida entran también `tuned` sin rezagos de Td (`tuned_sin_td`: mismo
protocolo que `tuned`, pero con el pool de candidatos reducido a `const`, `TMIN_anom` y
sus rezagos; script `experiments/timesfm/scripts/10_tuned_sin_rezagos_td.sh`, bead
`tdew-f6a`) y TimesFM con objetivo anomalía y contexto desde 2002 (`timesfm_anom_med`,
variante `tmin_anom_med`: 11 años de contexto en `ll4` y 7 en `ll4b`, solo el período
en que PISCO usa LST de MODIS). Por último, `llr_simple_sel` y `llr_rezagos_sel` son
los dos LLR con el semiancho `h` y el año de inicio del ajuste elegidos juntos por
validación interna: `h` en (7, 11, 15, 21, 31, 45, 60, 90, 120, 180) y el inicio en
(1981, 1986, 1991, 1996), con coeficientes ajustados en [inicio, train_end − 4],
climatología 1981 a train_end − 4 y error medido en los cuatro últimos años de
entrenamiento; después se reajustan con [inicio elegido, train_end] y la climatología
1981 a train_end (`--select-train-start`, `experiments/timesfm/scripts/15_llr_seleccion.sh`).
El bloque de prueba no entra en la elección. En los cuatro casos se eligió el inicio 1991;
`h` salió 60 (`llr_simple_sel`) y 45 (`llr_rezagos_sel`) en `ll4b`, y 90 en los dos en
`ll4`, ninguno en el borde de la grilla. Con la grilla anterior y el inicio fijo en 1981,
los LLR del panel habían elegido `h` = 31 en `ll4b` y 60 en `ll4`.

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
| tuned_sin_td | panel (17.027) | 1,174 | +0,014 | 0,875 | 1,154 | 1,151 | 1,166 | 1,224 |
| llr_simple | panel (17.027) | 1,175 | −0,010 | 0,874 | 1,143 | 1,152 | 1,172 | 1,231 |
| llr_rezagos | panel (17.027) | 1,161 | +0,025 | 0,861 | 1,137 | 1,148 | 1,142 | 1,215 |
| llr_simple_sel | panel (17.027) | 1,172 | −0,002 | 0,856 | 1,159 | 1,147 | 1,156 | 1,224 |
| llr_rezagos_sel | panel (17.027) | 1,157 | +0,036 | 0,840 | 1,145 | 1,149 | 1,130 | 1,202 |
| timesfm_anom | panel (17.027) | 1,154 | +0,104 | 0,802 | 1,205 | 1,127 | 1,080 | 1,199 |
| timesfm_anom_med | panel (17.027) | 1,201 | +0,201 | 0,828 | 1,281 | 1,188 | 1,115 | 1,214 |
| clim | Perú (8.272) | 1,262 | −0,301 | 1,226 | 1,123 | 1,147 | 1,372 | 1,381 |
| tuned | Perú (8.272) | 0,944 | +0,010 | 0,884 | 0,883 | 0,932 | 0,973 | 0,985 |
| tuned_sin_td | Perú (8.272) | 0,908 | +0,047 | 0,861 | 0,879 | 0,905 | 0,910 | 0,937 |
| llr_simple | Perú (8.272) | 0,912 | +0,009 | 0,861 | 0,870 | 0,905 | 0,921 | 0,950 |
| llr_rezagos | Perú (8.272) | 0,897 | +0,059 | 0,847 | 0,868 | 0,901 | 0,890 | 0,929 |
| llr_simple_sel | Perú (8.272) | 0,906 | −0,014 | 0,844 | 0,876 | 0,896 | 0,910 | 0,940 |
| llr_rezagos_sel | Perú (8.272) | 0,891 | +0,034 | 0,828 | 0,869 | 0,895 | 0,882 | 0,915 |
| timesfm_anom | Perú (8.272) | 0,865 | +0,050 | 0,787 | 0,858 | 0,861 | 0,836 | 0,903 |
| timesfm_anom_med | Perú (8.272) | 0,903 | +0,098 | 0,811 | 0,929 | 0,897 | 0,865 | 0,918 |

### RMSE y sesgo por método, bloque `ll4b` (°C)

| método | ámbito | RMSE | sesgo | RMSE macro por zona | 2009 | 2010 | 2011 | 2012 |
|---|---|---|---|---|---|---|---|---|
| clim | panel (17.027) | 1,362 | −0,300 | 1,115 | 1,241 | 1,426 | 1,409 | 1,363 |
| tuned | panel (17.027) | 1,122 | −0,156 | 0,825 | 1,035 | 1,127 | 1,117 | 1,202 |
| tuned_sin_td | panel (17.027) | 1,108 | −0,124 | 0,808 | 1,050 | 1,103 | 1,091 | 1,184 |
| llr_simple | panel (17.027) | 1,098 | −0,140 | 0,798 | 1,027 | 1,095 | 1,096 | 1,171 |
| llr_rezagos | panel (17.027) | 1,089 | −0,117 | 0,793 | 1,032 | 1,089 | 1,076 | 1,156 |
| llr_simple_sel | panel (17.027) | 1,083 | −0,138 | 0,778 | 1,033 | 1,073 | 1,080 | 1,143 |
| llr_rezagos_sel | panel (17.027) | 1,074 | −0,117 | 0,770 | 1,034 | 1,066 | 1,061 | 1,133 |
| timesfm_td | panel (17.027) | 1,106 | +0,035 | 0,769 | 1,185 | 1,081 | 1,062 | 1,092 |
| timesfm_anom | panel (17.027) | 1,046 | −0,108 | 0,745 | 1,026 | 1,021 | 1,034 | 1,102 |
| timesfm_anom_med | panel (17.027) | 1,108 | +0,089 | 0,789 | 1,195 | 1,075 | 1,050 | 1,108 |
| clim | Perú (8.272) | 1,087 | −0,203 | 1,083 | 1,013 | 1,137 | 1,089 | 1,106 |
| tuned | Perú (8.272) | 0,861 | −0,060 | 0,808 | 0,796 | 0,852 | 0,841 | 0,947 |
| tuned_sin_td | Perú (8.272) | 0,856 | −0,034 | 0,792 | 0,813 | 0,847 | 0,830 | 0,929 |
| llr_simple | Perú (8.272) | 0,849 | −0,056 | 0,782 | 0,796 | 0,843 | 0,835 | 0,916 |
| llr_rezagos | Perú (8.272) | 0,844 | −0,028 | 0,778 | 0,801 | 0,835 | 0,821 | 0,912 |
| llr_simple_sel | Perú (8.272) | 0,834 | −0,083 | 0,763 | 0,790 | 0,821 | 0,826 | 0,895 |
| llr_rezagos_sel | Perú (8.272) | 0,830 | −0,062 | 0,756 | 0,792 | 0,811 | 0,815 | 0,897 |
| timesfm_td | Perú (8.272) | 0,840 | −0,003 | 0,750 | 0,867 | 0,819 | 0,813 | 0,859 |
| timesfm_anom | Perú (8.272) | 0,804 | −0,085 | 0,729 | 0,774 | 0,776 | 0,789 | 0,874 |
| timesfm_anom_med | Perú (8.272) | 0,849 | −0,004 | 0,774 | 0,874 | 0,822 | 0,818 | 0,879 |

### Brechas pareadas RMSE(A) − RMSE(B) con IC 95 % (°C; negativo favorece a A)

| bloque | ámbito | A − B | brecha | IC bloques espaciales 2° | IC bloques mes-año |
|---|---|---|---|---|---|
| ll4 | panel (17.027) | timesfm_anom − llr_rezagos | −0,007 | [−0,017; +0,001] | [−0,038; +0,023] |
| ll4 | panel (17.027) | timesfm_anom − llr_simple | −0,021 | [−0,031; −0,012] | [−0,053; +0,010] |
| ll4 | panel (17.027) | timesfm_anom − tuned | −0,074 | [−0,080; −0,069] | [−0,140; −0,015] |
| ll4 | panel (17.027) | tuned − llr_simple | +0,053 | [+0,044; +0,062] | [+0,017; +0,097] |
| ll4 | panel (17.027) | tuned − llr_rezagos | +0,067 | [+0,058; +0,075] | [+0,029; +0,114] |
| ll4 | panel (17.027) | tuned − tuned_sin_td | +0,054 | [+0,046; +0,061] | [+0,019; +0,096] |
| ll4 | panel (17.027) | tuned_sin_td − llr_simple | −0,001 | [−0,003; +0,002] | [−0,012; +0,011] |
| ll4 | panel (17.027) | timesfm_anom − tuned_sin_td | −0,021 | [−0,029; −0,013] | [−0,056; +0,015] |
| ll4 | panel (17.027) | timesfm_anom_med − timesfm_anom | +0,047 | [+0,041; +0,053] | [+0,027; +0,068] |
| ll4 | panel (17.027) | timesfm_anom_med − llr_rezagos | +0,040 | [+0,025; +0,053] | [−0,005; +0,083] |
| ll4 | panel (17.027) | timesfm_anom − llr_rezagos_sel | −0,003 | [−0,011; +0,004] | [−0,029; +0,021] |
| ll4 | panel (17.027) | timesfm_anom − llr_simple_sel | −0,018 | [−0,027; −0,010] | [−0,045; +0,007] |
| ll4 | panel (17.027) | llr_rezagos_sel − llr_rezagos | −0,004 | [−0,008; −0,002] | [−0,013; +0,004] |
| ll4 | panel (17.027) | llr_simple_sel − llr_simple | −0,003 | [−0,006; −0,001] | [−0,010; +0,005] |
| ll4 | Perú (8.272) | timesfm_anom − llr_rezagos | −0,032 | [−0,044; −0,021] | [−0,047; −0,018] |
| ll4 | Perú (8.272) | timesfm_anom − llr_simple | −0,047 | [−0,058; −0,036] | [−0,063; −0,031] |
| ll4 | Perú (8.272) | timesfm_anom − tuned | −0,079 | [−0,087; −0,071] | [−0,109; −0,052] |
| ll4 | Perú (8.272) | tuned − llr_simple | +0,032 | [+0,021; +0,043] | [+0,016; +0,050] |
| ll4 | Perú (8.272) | tuned − llr_rezagos | +0,047 | [+0,036; +0,058] | [+0,026; +0,071] |
| ll4 | Perú (8.272) | tuned − tuned_sin_td | +0,036 | [+0,027; +0,046] | [+0,019; +0,057] |
| ll4 | Perú (8.272) | tuned_sin_td − llr_simple | −0,004 | [−0,008; −0,001] | [−0,011; +0,003] |
| ll4 | Perú (8.272) | timesfm_anom − tuned_sin_td | −0,043 | [−0,054; −0,033] | [−0,060; −0,027] |
| ll4 | Perú (8.272) | timesfm_anom_med − timesfm_anom | +0,037 | [+0,030; +0,045] | [+0,025; +0,050] |
| ll4 | Perú (8.272) | timesfm_anom_med − llr_rezagos | +0,005 | [−0,013; +0,023] | [−0,016; +0,026] |
| ll4 | Perú (8.272) | timesfm_anom − llr_rezagos_sel | −0,026 | [−0,033; −0,018] | [−0,038; −0,014] |
| ll4 | Perú (8.272) | timesfm_anom − llr_simple_sel | −0,041 | [−0,049; −0,033] | [−0,054; −0,029] |
| ll4 | Perú (8.272) | llr_rezagos_sel − llr_rezagos | −0,007 | [−0,013; −0,001] | [−0,011; −0,002] |
| ll4 | Perú (8.272) | llr_simple_sel − llr_simple | −0,006 | [−0,011; −0,002] | [−0,011; −0,000] |
| ll4b | panel (17.027) | timesfm_anom − llr_rezagos | −0,043 | [−0,047; −0,039] | [−0,062; −0,026] |
| ll4b | panel (17.027) | timesfm_anom − llr_simple | −0,052 | [−0,057; −0,048] | [−0,073; −0,033] |
| ll4b | panel (17.027) | timesfm_anom − tuned | −0,076 | [−0,084; −0,068] | [−0,102; −0,050] |
| ll4b | panel (17.027) | tuned − llr_simple | +0,024 | [+0,020; +0,027] | [+0,009; +0,039] |
| ll4b | panel (17.027) | tuned − llr_rezagos | +0,033 | [+0,028; +0,037] | [+0,019; +0,046] |
| ll4b | panel (17.027) | timesfm_td − llr_simple | +0,007 | [−0,001; +0,015] | [−0,042; +0,059] |
| ll4b | panel (17.027) | tuned − tuned_sin_td | +0,014 | [+0,011; +0,017] | [−0,000; +0,027] |
| ll4b | panel (17.027) | tuned_sin_td − llr_simple | +0,010 | [+0,007; +0,012] | [−0,003; +0,022] |
| ll4b | panel (17.027) | timesfm_anom − tuned_sin_td | −0,062 | [−0,068; −0,056] | [−0,084; −0,043] |
| ll4b | panel (17.027) | timesfm_anom_med − timesfm_anom | +0,062 | [+0,053; +0,071] | [+0,024; +0,100] |
| ll4b | panel (17.027) | timesfm_anom_med − llr_rezagos | +0,019 | [+0,011; +0,026] | [−0,032; +0,067] |
| ll4b | panel (17.027) | timesfm_anom − llr_rezagos_sel | −0,028 | [−0,031; −0,026] | [−0,044; −0,013] |
| ll4b | panel (17.027) | timesfm_anom − llr_simple_sel | −0,037 | [−0,041; −0,033] | [−0,052; −0,023] |
| ll4b | panel (17.027) | llr_rezagos_sel − llr_rezagos | −0,015 | [−0,017; −0,012] | [−0,026; −0,004] |
| ll4b | panel (17.027) | llr_simple_sel − llr_simple | −0,015 | [−0,017; −0,013] | [−0,026; −0,005] |
| ll4b | Perú (8.272) | timesfm_anom − llr_rezagos | −0,039 | [−0,046; −0,033] | [−0,050; −0,029] |
| ll4b | Perú (8.272) | timesfm_anom − llr_simple | −0,044 | [−0,050; −0,039] | [−0,057; −0,033] |
| ll4b | Perú (8.272) | timesfm_anom − tuned | −0,056 | [−0,065; −0,049] | [−0,073; −0,040] |
| ll4b | Perú (8.272) | tuned − llr_simple | +0,012 | [+0,008; +0,016] | [+0,002; +0,024] |
| ll4b | Perú (8.272) | tuned − llr_rezagos | +0,017 | [+0,014; +0,021] | [+0,007; +0,027] |
| ll4b | Perú (8.272) | timesfm_td − llr_simple | −0,009 | [−0,020; +0,002] | [−0,037; +0,019] |
| ll4b | Perú (8.272) | tuned − tuned_sin_td | +0,005 | [+0,001; +0,008] | [−0,005; +0,014] |
| ll4b | Perú (8.272) | tuned_sin_td − llr_simple | +0,007 | [+0,003; +0,011] | [−0,000; +0,015] |
| ll4b | Perú (8.272) | timesfm_anom − tuned_sin_td | −0,052 | [−0,058; −0,045] | [−0,064; −0,040] |
| ll4b | Perú (8.272) | timesfm_anom_med − timesfm_anom | +0,044 | [+0,037; +0,052] | [+0,024; +0,064] |
| ll4b | Perú (8.272) | timesfm_anom_med − llr_rezagos | +0,005 | [−0,004; +0,013] | [−0,021; +0,029] |
| ll4b | Perú (8.272) | timesfm_anom − llr_rezagos_sel | −0,025 | [−0,028; −0,023] | [−0,034; −0,016] |
| ll4b | Perú (8.272) | timesfm_anom − llr_simple_sel | −0,030 | [−0,033; −0,026] | [−0,039; −0,021] |
| ll4b | Perú (8.272) | llr_rezagos_sel − llr_rezagos | −0,014 | [−0,019; −0,010] | [−0,022; −0,006] |
| ll4b | Perú (8.272) | llr_simple_sel − llr_simple | −0,015 | [−0,018; −0,011] | [−0,022; −0,008] |

### Zonas en que el método de la fila gana al de la columna, `ll4`, panel (17.027) (33 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | llr_simple_sel | llr_rezagos_sel | timesfm_anom | timesfm_anom_med |
|---|---|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 33 | — | 1 | 4 | 0 | 2 | 0 | 0 | 0 |
| tuned_sin_td | 33 | 32 | — | 17 | 0 | 13 | 0 | 0 | 3 |
| llr_simple | 33 | 29 | 16 | — | 5 | 4 | 0 | 1 | 2 |
| llr_rezagos | 33 | 33 | 33 | 28 | — | 17 | 6 | 1 | 7 |
| llr_simple_sel | 33 | 31 | 20 | 29 | 16 | — | 4 | 0 | 3 |
| llr_rezagos_sel | 33 | 33 | 33 | 33 | 27 | 29 | — | 1 | 10 |
| timesfm_anom | 33 | 33 | 33 | 32 | 32 | 33 | 32 | — | 32 |
| timesfm_anom_med | 33 | 33 | 30 | 31 | 26 | 30 | 23 | 1 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4`, Perú (8.272) (32 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | llr_simple_sel | llr_rezagos_sel | timesfm_anom | timesfm_anom_med |
|---|---|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 32 | — | 2 | 6 | 0 | 4 | 0 | 0 | 0 |
| tuned_sin_td | 32 | 30 | — | 17 | 0 | 14 | 0 | 0 | 3 |
| llr_simple | 32 | 26 | 15 | — | 4 | 5 | 0 | 0 | 1 |
| llr_rezagos | 32 | 32 | 32 | 28 | — | 17 | 6 | 0 | 5 |
| llr_simple_sel | 32 | 28 | 18 | 27 | 15 | — | 4 | 0 | 2 |
| llr_rezagos_sel | 32 | 32 | 32 | 32 | 26 | 28 | — | 0 | 9 |
| timesfm_anom | 32 | 32 | 32 | 32 | 32 | 32 | 32 | — | 30 |
| timesfm_anom_med | 32 | 32 | 29 | 31 | 27 | 30 | 23 | 2 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4b`, panel (17.027) (33 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | llr_simple_sel | llr_rezagos_sel | timesfm_td | timesfm_anom | timesfm_anom_med |
|---|---|---|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 33 | — | 3 | 5 | 1 | 1 | 0 | 3 | 0 | 7 |
| tuned_sin_td | 33 | 30 | — | 12 | 1 | 3 | 0 | 5 | 0 | 11 |
| llr_simple | 33 | 28 | 21 | — | 12 | 2 | 0 | 4 | 0 | 14 |
| llr_rezagos | 33 | 32 | 32 | 21 | — | 14 | 2 | 6 | 0 | 17 |
| llr_simple_sel | 33 | 32 | 30 | 31 | 19 | — | 5 | 12 | 0 | 23 |
| llr_rezagos_sel | 33 | 33 | 33 | 33 | 31 | 28 | — | 13 | 0 | 27 |
| timesfm_td | 33 | 30 | 28 | 29 | 27 | 21 | 20 | — | 3 | 27 |
| timesfm_anom | 33 | 33 | 33 | 33 | 33 | 33 | 33 | 30 | — | 32 |
| timesfm_anom_med | 33 | 26 | 22 | 19 | 16 | 10 | 6 | 6 | 1 | — |

### Zonas en que el método de la fila gana al de la columna, `ll4b`, Perú (8.272) (32 zonas)

| A \ B | clim | tuned | tuned_sin_td | llr_simple | llr_rezagos | llr_simple_sel | llr_rezagos_sel | timesfm_td | timesfm_anom | timesfm_anom_med |
|---|---|---|---|---|---|---|---|---|---|---|
| clim | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tuned | 32 | — | 5 | 6 | 1 | 1 | 0 | 3 | 0 | 10 |
| tuned_sin_td | 32 | 27 | — | 12 | 1 | 3 | 0 | 3 | 0 | 12 |
| llr_simple | 32 | 26 | 20 | — | 10 | 1 | 0 | 4 | 0 | 14 |
| llr_rezagos | 32 | 31 | 31 | 22 | — | 13 | 2 | 6 | 0 | 18 |
| llr_simple_sel | 32 | 31 | 29 | 31 | 19 | — | 6 | 9 | 0 | 24 |
| llr_rezagos_sel | 32 | 32 | 32 | 32 | 30 | 26 | — | 10 | 0 | 25 |
| timesfm_td | 32 | 29 | 29 | 28 | 26 | 23 | 22 | — | 3 | 26 |
| timesfm_anom | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 29 | — | 32 |
| timesfm_anom_med | 32 | 22 | 20 | 18 | 14 | 8 | 7 | 6 | 0 | — |

<!-- tablas:fin -->

## Lectura

Las cifras del panel coinciden con `experiments/llr_simple/resultados_ll4_ll4b.txt`
(RMSE, sesgo, RMSE por año y brechas puntuales). Los intervalos de ese archivo vienen de
otro sorteo de bloques mes-año y difieren en la tercera cifra decimal.

TimesFM con objetivo anomalía (`timesfm_anom`) tiene el RMSE agregado más bajo en los
dos bloques y en los dos ámbitos. Frente al LLR con rezagos, la brecha en `ll4` sobre el
panel es de −0,007 °C y los dos intervalos incluyen el cero; en `ll4b` es de −0,043 °C
y ninguno lo incluye. Dentro del Perú la brecha en `ll4` es de −0,032 °C
[−0,047; −0,018] con bloques mes-año, de modo que la brecha pequeña del panel en `ll4`
proviene de las celdas fuera del país. El año 2013 concentra esa diferencia: en el
panel TimesFM es el peor de los métodos de regresión ese año (1,205 contra 1,137 del
LLR con rezagos) y dentro del Perú es el mejor (0,858 contra 0,868). Con un solo bloque
por período no se puede separar si esto es propio de 2013 o de la región fuera del
Perú.

Quitar los rezagos de Td a `tuned` baja su RMSE en los dos bloques: de 1,228 a 1,174 °C
en `ll4` (brecha `tuned − tuned_sin_td` de +0,054 °C, IC mes-año [+0,019; +0,096]) y de
1,122 a 1,108 °C en `ll4b` (+0,014 °C, IC mes-año [−0,000; +0,027]). En el Perú las
mejoras son de +0,036 y +0,005 °C, y en `ll4b` el intervalo mes-año incluye el cero.
Sin rezagos de Td, `tuned` queda a la par del LLR simple (−0,001 °C en `ll4`, +0,010 °C
en `ll4b`, ambos con intervalos mes-año que incluyen el cero) y por detrás del LLR con
rezagos de Tmin en 33 y 32 de 33 zonas. Es consistente con que la mayor parte de la
desventaja de `tuned` frente al LLR simple (+0,053 °C en `ll4`, +0,024 °C en `ll4b`)
venga de la recursión sobre Td predicho dentro del bloque; el efecto es mayor en `ll4`,
el bloque con El Niño 2015-2016.

TimesFM sigue por delante de `tuned_sin_td`, que es el rival con entradas equiparables
(solo Tmin, sin Td observado en el bloque). La brecha `timesfm_anom − tuned_sin_td` es
de −0,021 °C en `ll4` sobre el panel, con IC espacial [−0,029; −0,013] y mes-año
[−0,056; +0,015], y de −0,062 °C en `ll4b` (mes-año [−0,084; −0,043]). En el Perú es de
−0,043 °C en `ll4` (mes-año [−0,060; −0,027]) y −0,052 °C en `ll4b` (mes-año
[−0,064; −0,040]). La lectura prudente es la misma que frente al LLR con rezagos:
ventaja clara en `ll4b` y en el Perú, no concluyente en el panel de `ll4`.

Acortar el contexto de TimesFM a los años con MODIS empeora el resultado:
`timesfm_anom_med − timesfm_anom` es de +0,047 °C en `ll4` (mes-año [+0,027; +0,068])
y +0,062 °C en `ll4b` ([+0,024; +0,100]), y el sesgo pasa a ser positivo en ambos bloques
(+0,201 y +0,089 °C en el panel). Con esa variante TimesFM no supera al LLR con
rezagos: la brecha es de +0,040 °C en `ll4` y +0,019 °C en `ll4b` sobre el panel, con
intervalos mes-año que incluyen el cero, y de +0,005 °C en el Perú en ambos bloques.
Esa pérdida no se debe al contexto corto. `tmin_anom_med` recorta también la
climatología con la que se forman y deshacen las anomalías (2002-2012 en `ll4`,
2002-2008 en `ll4b`). En la escalera de contexto sobre el panel de cribado
(`a1_escalera_contexto.md`, 1.092 celdas), con la climatología fija en 1981-train_end,
pasar el inicio del contexto de 1981 a 2002 costó +0,005 °C en `ll4` y +0,002 °C en
`ll4b`. Con el contexto desde 2002, recortar además la climatología costó +0,022 °C en
`ll4` (IC mes-año [+0,015; +0,029]) y +0,044 °C en `ll4b` ([+0,035; +0,053]). En esa
muestra la climatología explica unas cuatro quintas partes de la diferencia en `ll4` y
casi toda en `ll4b`. La ventaja de `timesfm_anom` depende, por tanto, de estimar la
climatología con los años desde 1981, y mucho menos de la longitud del contexto o de que
incluya años sin MODIS.

Con los LLR elegidos por validación interna la ventaja de TimesFM se reduce en todos los
casos, y en el panel de `ll4` deja de distinguirse de cero. La selección mejora a los dos LLR en los dos
bloques: `llr_rezagos_sel − llr_rezagos` es de −0,004 °C en `ll4` y −0,015 °C en `ll4b`
sobre el panel (IC espacial [−0,008; −0,002] y [−0,017; −0,012]), y de −0,007 y −0,014 °C
en el Perú; `llr_rezagos_sel` gana a `llr_rezagos` en 27 y 31 de 33 zonas. Frente a ese
rival, `timesfm_anom − llr_rezagos_sel` es de −0,003 °C en `ll4` sobre el panel, con IC
espacial [−0,011; +0,004] y mes-año [−0,029; +0,021]; en `ll4b` es de −0,028 °C
(espacial [−0,031; −0,026], mes-año [−0,044; −0,014]). En el Perú es de −0,026 °C en
`ll4` (espacial [−0,033; −0,018], mes-año [−0,038; −0,014]) y −0,025 °C en `ll4b`
(espacial [−0,028; −0,023], mes-año [−0,034; −0,016]). Frente al LLR simple seleccionado
las brechas son de −0,018 y −0,037 °C en el panel y −0,041 y −0,030 °C en el Perú; solo
la de `ll4` en el panel tiene un intervalo mes-año que incluye el cero
([−0,045; +0,007]). Por zonas, TimesFM gana a `llr_rezagos_sel` en 32 de 33 en `ll4` y
en todas en `ll4b`. La lectura queda como antes, con brechas más pequeñas: en el
panel de `ll4` TimesFM y el LLR con rezagos son indistinguibles en RMSE agregado (1,154
contra 1,157 °C), y en `ll4b` y en el Perú TimesFM queda por delante en 0,025 a
0,028 °C con intervalos que excluyen el cero. En 2013 el LLR seleccionado sigue por
delante de TimesFM en el panel (1,145 contra 1,205 °C) y apenas por detrás en el Perú
(0,869 contra 0,858 °C).

Las clasificaciones por zona son más estables que las agregadas: `timesfm_anom` gana al
LLR con rezagos en 32 de 33 zonas en `ll4` y en todas en `ll4b`, y la diferencia en RMSE
macro por zona es mayor que la agregada (0,802 contra 0,861 en `ll4`). Es consistente
con una ventaja de TimesFM mayor en las zonas con pocas celdas. El sesgo de TimesFM
cambia de signo entre bloques (+0,104 en `ll4`, −0,108 en `ll4b` sobre el panel); el del
LLR simple es negativo en ambos (−0,010 y −0,140).

Dos salvedades. La variante `tmin_anom_full` de TimesFM se eligió entre nueve sobre el
bloque `ll4` (bead `tdew-214.11.8`); `ll4b` no participó en esa elección, por lo que es
la medición menos expuesta a ese sesgo de selección y es la que da la ventaja más clara.
Y el LLR propio y `tuned_sin_td` son variantes construidas en este proyecto que no ha
revisado Palacios.
