# Figuras del paper nuevo

Generadas por `experiments/paper_nuevo/figuras.py` (`uv run python -m experiments.paper_nuevo.figuras`) con el estilo de `experiments/paper_nuevo/estilo.py`. Cada figura sale en PNG (300 dpi), PDF y SVG. Los valores graficados se leen de los CSV; el código falla si faltan métodos, bloques o ámbitos esperados. Convención de signo: brecha = RMSE(TimesFM) − RMSE(rival); un valor negativo favorece a TimesFM. Ninguna figura lleva título dentro de la imagen. Anchos: 16 cm (figuras 1 a 5, suplementos), pensados para texto completo A4.

Nombres de método: TimesFM = `timesfm_anom`; `tuned` = `tuned` de Palacios; LLR con rezagos (sel.) = `llr_rezagos_sel`.

## Figura 1. `fig1_panel`

- Mensaje único: casi la mitad de las celdas del dominio queda fuera de Perú, y más de la mitad de ellas pertenece a una sola zona SENAMHI (la de más celdas, `A (r) A′`). Se rediseñó siguiendo `GUIAS_MIT_CHECKLIST.md`.
- Diseño: un mapa en gris (Perú gris oscuro, fuera gris claro), con la zona más numerosa en violeta como único color de foco; contorno nacional oscuro y límites departamentales finos en blanco; sin marco, ticks ni leyendas; proporción cartográfica (1/cos de la latitud media); barra de escala de 500 km. A la derecha, dos barras de longitud sobre base común (Perú y fuera de Perú), con la zona focal partiendo de cero y rótulos directos. El titular de la figura calcula en código los totales y el porcentaje.
- Fuentes: `panels/nacional_17027.csv`, `peru_mask`, GeoJSON departamental y `zone_table.parquet`. Control en código: 8.272 dentro y 8.755 fuera.
- Pie sugerido: «Casi la mitad de las celdas del dominio de evaluación ({{< var panel.celdas_fuera >}} de {{< var panel.celdas >}}) está fuera de Perú, y la zona SENAMHI `A (r) A′` concentra la mayor parte de ellas. Gris oscuro: celdas dentro de Perú; gris claro: fuera; violeta: zona `A (r) A′`. Cada punto es una celda de 0,01°; el panel es un subconjunto de la grilla nacional, y la caja envolvente no es el territorio peruano.»

## Figura 2. `fig2_brechas`

- Fuente: `reports/paper_nuevo/resultados/a1_brechas.csv`.
- Filtro: `metodo_a = timesfm_anom`, `metodo_b` en {`tuned`, `llr_rezagos_sel`}, `split` en {`ll4b`, `ll4`}, `ambito` en {`panel`, `peru`}, `esquema` en {`espacial_2g`, `mes_anio`}. 16 intervalos.
- Muestra: brecha pareada de RMSE con dos IC 95 % por celda del diseño: bloques espaciales de 2 grados (línea gruesa, punto lleno) y bloques mes-año (línea fina, punto vacío). Filas: bloque 2009–2012 (`ll4b`) arriba y 2013–2016 (`ll4`) abajo; columnas: dominio completo y Perú. Eje x compartido. El valor numérico es la brecha puntual.
- Pie sugerido: «Brecha pareada de RMSE, TimesFM − rival (°C), por bloque y ámbito. Negativo indica menor RMSE de TimesFM. Dos intervalos de confianza al 95 %: bloques espaciales de 2 grados (línea gruesa) y bloques mes-año (línea fina). Frente a `tuned` los ocho intervalos quedan por debajo de cero. Frente a LLR con rezagos (sel.), en 2013–2016 y dominio completo los dos intervalos incluyen el cero (espacial [−0,011; +0,004], mes-año [−0,029; +0,021]); en los otros tres casos excluyen el cero. Un intervalo que incluye el cero no establece empate ni equivalencia.»
- Cifras del pie verificadas contra `ic_lo` e `ic_hi` de `a1_brechas.csv`.

## Figura 3. `fig3_anual`

- Fuente: `a1_por_metodo.csv`.
- Filtro: `periodo` = año 2009 a 2016 (años de `ll4b` para 2009–2012 y de `ll4` para 2013–2016), `ambito` en {`panel`, `peru`}, métodos `timesfm_anom`, `tuned`, `llr_rezagos_sel`. Brecha = RMSE(TimesFM) − RMSE(rival) en cada año.
- Muestra: una línea por rival y panel por ámbito; línea discontinua entre 2012 y 2013 (cambio de bloque, es decir, otra selección y otro contexto); línea sólida en cero. Sin intervalos: `a1_por_metodo.csv` no los trae para cada año.
- Pie sugerido: «Brecha anual de RMSE, TimesFM − rival (°C), 2009–2016. Negativo favorece a TimesFM. La línea discontinua separa los bloques 2009–2012 y 2013–2016, evaluados con contextos y selecciones distintos. No se muestran intervalos de confianza por año. En el dominio completo la brecha fue positiva en 2013 frente a ambos rivales; en Perú todas las brechas anuales fueron negativas.»

## Figura 4. `fig4_zonas`

- Fuente: `a1_por_zona.csv`.
- Filtro: `ambito = panel`; 33 zonas por bloque; métodos `timesfm_anom`, `tuned`, `llr_rezagos_sel`. Brecha por zona = RMSE(TimesFM) − RMSE(rival). El número de celdas por zona (columna `celdas`) va entre paréntesis en la etiqueta y como tamaño del punto.
- Orden: por la brecha frente a `tuned` en 2013–2016 (arriba la menos negativa), igual en ambos paneles para poder comparar bloques.
- Pie sugerido: «Brecha de RMSE por zona SENAMHI, TimesFM − rival (°C), dominio completo. Negativo favorece a TimesFM. Entre paréntesis, número de celdas de la zona; el tamaño del punto es proporcional a la raíz de ese número. Las zonas se ordenan por la brecha frente a `tuned` en 2013–2016. Las zonas con pocas celdas (por ejemplo, una celda en `D (i) D′`) tienen estimaciones inestables.» Y, si se quiere, «Frente a LLR con rezagos (sel.) una zona (`A (r) A′`, 7.091 celdas) tuvo brecha positiva en 2013–2016.»
- Los datos no traen intervalos por zona; no se comparan zonas entre sí como si las diferencias fueran significativas.

## Figura 5. `fig5_horizonte`

- Fuente: `reports/paper_nuevo/resultados/r1_brecha_horizonte.csv` (`experiments/paper_nuevo/analisis_inferencia.py`).
- Filtro: `unidad = mes`, `metodo_a = timesfm_anom`, `metodo_b` en {`tuned`, `tuned_sin_td`, `llr_rezagos_sel`, `llr_simple_sel`}, `split` en {`ll4b`, `ll4`}, `ambito` en {`panel`, `peru`}. 16 series de 48 meses; el código falla si falta algún mes.
- Muestra: brecha de RMSE (TimesFM − rival) en cada mes desde el inicio del bloque (1 a 48). Filas: bloque 2009–2012 arriba y 2013–2016 abajo; columnas: dominio completo y Perú; ejes compartidos. Línea sólida en cero; líneas verticales tenues en los límites de año del bloque (meses 12/13, 24/25, 36/37). Banda translúcida: IC 95 % por bootstrap de bloques espaciales de 2° de cada mes (muy estrecha; se ve sobre todo en los picos). Trazo continuo para `tuned` y `llr_rezagos_sel`; discontinuo para `tuned_sin_td` y `llr_simple_sel`. Colores de método de `estilo.py`; `tuned_sin_td` (azul claro) y `llr_simple_sel` (terracota) se añadieron para esta figura.
- Pie sugerido: «Brecha pareada de RMSE, TimesFM − rival (°C), por mes desde el inicio del bloque. Negativo favorece a TimesFM. Las líneas verticales marcan los límites de año del bloque; la banda es el IC 95 % de cada mes (bloques espaciales de 2°). En 2013–2016 y dominio completo la brecha anual del primer año es positiva frente a los cuatro rivales; en los otros tres casos todas las brechas anuales son negativas. Cada mes es una estimación descriptiva y no se corrige por comparaciones múltiples.»
- Cifras del pie: `horizonte.<bloque>.<ámbito>.<rival>.anios_positivos` en `cifras.csv` (la brecha anual por año del bloque con su IC está en `horizonte.*.anio<k>.v` y `.ic`).

## Figura 6. `fig6_robustez` (id Quarto sugerido: `fig-robustez`)

- Fuentes: `reports/paper_nuevo/resultados/r1_bootstrap_espaciotemporal.csv` (brecha puntual y tres IC) con control cruzado de la brecha puntual contra `a1_brechas.csv` (`tuned` y `llr_rezagos_sel`); el código falla si falta una combinación o si la brecha puntual difiere entre esquemas o frente a `a1_brechas.csv`.
- Filtro: `metodo_a = timesfm_anom`; `metodo_b` en {`tuned`, `tuned_sin_td`, `llr_rezagos_sel`, `llr_simple_sel`}; `split` en {`ll4b`, `ll4`}; `ambito` en {`panel`, `peru`}; `esquema` en {`espacial_2g`, `espaciotemporal_2g_anio`, `temporal_trim_anio`}. 48 intervalos.
- Muestra: multiples pequenos 2 × 2 (filas: bloque 2009–2012 arriba y 2013–2016 abajo; columnas: dominio completo y Perú), eje x compartido, linea del cero. Cada rival lleva tres intervalos apilados (de arriba abajo: bloques espaciales de 2°, bloques 2° × año, bloques trimestre-año) con grosor decreciente y el color del metodo de `estilo.py`; el circulo blanco es la brecha puntual. Sustituye a la tabla larga de robustez en el cuerpo (la tabla `tab7_robustez` queda para el suplemento con los p de Diebold–Mariano).
- Pie sugerido: «Brecha pareada de RMSE, TimesFM − rival (°C), con tres IC 95 % por bootstrap de bloques: espaciales de 2° (trazo grueso), 2° × año (medio) y trimestre-año (fino). El círculo es la brecha puntual; negativo favorece a TimesFM. Los intervalos que cruzan la línea del cero no establecen empate ni equivalencia. En 2013–2016 y dominio completo, frente a `llr_rezagos_sel`, el IC espacial es {{< var robustez.ll4.panel.llr_rezagos_sel.esp_ic >}}, el de 2° × año {{< var robustez.ll4.panel.llr_rezagos_sel.esa_ic >}} y el de trimestre-año {{< var robustez.ll4.panel.llr_rezagos_sel.ta_ic >}}. Los IC espaciales dejan fijos los días y son los más estrechos; el dominio completo y Perú no son muestras independientes.»
- Claves de apoyo: `robustez.<bloque>.<ámbito>.<rival>.{v,esp_ic,esa_ic,ta_ic}` en `cifras.csv`; conteos `robustez_conteo.*`.

## Suplemento

### `sfig_escalera_contexto`

- Fuente: `a1_escalera_contexto.csv`, `periodo = total`, métodos `timesfm`, `llr_rezagos`, `llr_simple`, y `tuned` como referencia (RMSE del bloque).
- Muestra: RMSE total por año de inicio del historial (1981, 1986, 1991, 1996, 2002), por bloque, 1.092 celdas.
- Pie sugerido: «RMSE total (°C) según el año de inicio del historial, en las 1.092 celdas del panel de cribado. La climatología se mantuvo fija en 1981–fin del entrenamiento. La línea punteada es `tuned` con su configuración de producción. La figura no identifica la causa de las diferencias entre inicios.»

### `sfig_a3_tmin_barajada`

- Fuente: `a3_control_tmin_barajada.csv` (todas las filas).
- Muestra: RMSE total de climatología, `tuned`, TimesFM con Tmin real (Td y anomalía) y TimesFM con Tmin barajada (entre celdas, entre años; tres semillas en la variante anomalía entre años), con la climatología como línea de referencia.
- Pie sugerido: «RMSE total (°C) de TimesFM con la Tmin del bloque y con la Tmin barajada, frente a climatología y `tuned`, en 1.092 celdas. Con la Tmin barajada entre años el RMSE superó al de la climatología (1,284); con la barajada entre celdas fue 1,266. Una sola semilla en la variante entre celdas.»

## Notas de datos

- `a1_por_zona.csv` trae 33 zonas en el ámbito `panel` y 32 en `peru` (la zona 39, 256 celdas, está fuera de Perú). La Figura 4 usa `panel`.
- La zona 34 tiene una celda; su brecha (−0,30 °C en 2013–2016) es un valor extremo no robusto. Se conserva sin recortar y se señala por el tamaño del punto.
- Los años por bloque provienen de `split`: `ll4b` solo tiene 2009–2012 y `ll4` solo 2013–2016.
