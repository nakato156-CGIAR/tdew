# Historia del paper nuevo: narrativa, evidencia y errores corregidos

Guía para redactar los `.qmd` del paper nuevo (TimesFM frente al método LLR de Palacios). Redactada el 21 de octubre de 2026. Beads `tdew-214.16` y `tdew-214.17`.

`ORIENTACION_PAPER.md` registra la decisión editorial en forma breve. Este documento la desarrolla: propone el orden del argumento, asigna a cada afirmación su evidencia y deja constancia de las interpretaciones que se retiraron, con el motivo, para que no vuelvan al texto. Además adopta la tesis E en forma acotada (sección siguiente); `ORIENTACION_PAPER.md` y `HANDOFF.md` (línea 82) todavía describen E como retirada y deben alinearse con esta guía.

Las cifras de precisión se leen en la sección «Paper» del artefacto local (`reports/timesfm_benchmark/artifact/index.html`, `id="paper"`) y en los CSV de `resultados/`. Las pocas que se citan aquí, de costo y robustez, llevan su archivo de origen; ante cualquier discrepancia manda ese archivo.

Origen. Las sesiones del 20 y 21 de octubre (`RESUMEN_SESION_2026-10-20_21.md`) produjeron los experimentos A1–A4. Una auditoría posterior con Codex (sesión `01a15f09-6387-76b3-bc33-d027d7470501`) recalculó desde los parquet los RMSE de los cuatro métodos principales en ambos bloques y ámbitos, con diferencias menores a 0,000005 °C frente a los CSV, sin filas duplicadas ni faltantes. Las cifras se sostuvieron; las fallas estaban en las conclusiones extraídas de ellas y en la forma de organizar la historia. Las correcciones se aplicaron en la sesión Codex `01a15f28-72c8-7523-8acd-5c41429f70c1` (bead `tdew-214.15`).

El paper vigente (`reports/paper/`, `PAPER_PLAN.md`) es de Palacios y no se modifica. Puede citarse como antecedente; la descripción de datos y del método `tuned` se copia a esta carpeta con atribución si se reutiliza.

## Pregunta del artículo

Se compara cuánto cambia la precisión, y qué preparación y cómputo requiere, reconstruir Td diaria con TimesFM sin ajuste de pesos frente al método local de Palacios, con los mismos datos y transformaciones.

Tesis (enfoque E, acotado): sin ajustar pesos y con los mismos datos que Palacios, TimesFM reconstruye Td con menor error que el método diseñado por zona climática, sin zonificación, sin búsqueda de recetas y sin entrenamiento. Un LLR local sin zonas queda cerca.

E se planteó el 20 de octubre a partir de un argumento del equipo: LLR es más rápido, pero exige diseñar el método y conocer el país; TimesFM se usa tal como viene (`HANDOFF.md` §4 en el commit `6a2df6b`). La auditoría posterior retiró la regla que elegía entre E y C+A según un intervalo de confianza, no la tesis. Esta versión deja fuera tres partes de la formulación original que la evidencia no sostiene: «solo se le pasa Tmin», «sin conocer el país» y «el diseño experto no aporta».

La tesis vale para PISCO y para los dos bloques evaluados. No se plantea como ganador universal ni se decide con un umbral estadístico. La discusión final indica también cuándo sigue conviniendo `tuned`.

## Supuestos de comparabilidad

Regla fijada por el equipo: todo lo que usa Palacios lo usa también TimesFM. Mismos productos y versiones de Td y Tmin (PISCO), misma grilla, mismas celdas y fechas puntuadas, mismas climatologías de entrenamiento y misma vuelta a °C. Solo los rezagos difieren, porque forman parte de cada método.

La referencia de TimesFM es la variante `tmin_anom_full`: recibe anomalías de Td y Tmin respecto de la climatología de entrenamiento de Palacios y devuelve la reconstrucción en °C. Para escribir sobre ella conviene separar dos cosas. Los datos disponibles son los mismos para ambos métodos: historial local de Td y Tmin, climatologías, y Tmin del bloque que se reconstruye. La forma de usarlos es distinta: LLR ajusta coeficientes por celda y construye rezagos; TimesFM recibe las secuencias como contexto y covariable (`build_inputs`, `experiments/timesfm/run.py:120`) sin modificar sus pesos.

De ahí salen tres precisiones que el texto debe mantener:

- La Tmin de todo el bloque reconstruido es conocida. El problema es de reconstrucción con covariable observada, no de pronóstico meteorológico, y el supuesto vale para los dos métodos.
- «Sin ajuste de pesos» no equivale a «sin preparación». TimesFM necesita historial local de Td y Tmin, climatologías, y una configuración elegida en un cribado de nueve variantes sobre 2013–2016.
- La selección de recetas por zona climática × día del año es un requisito de `tuned`, no de la familia LLR. El LLR simple y el LLR con rezagos seleccionado ajustan coeficientes locales sin mapa de zonas.

El panel llamado «nacional» tiene 17.027 celdas puntuadas, de las cuales 8.272 están en Perú y 8.755 fuera. Perú y dominio completo se reportan por separado. Las celdas fuera del país pertenecen al mismo producto PISCO y al entrenamiento de ambos métodos; se reportan como dominio completo, no como otra región.

## Arco narrativo propuesto

1. **Problema y datos compartidos.** Reconstrucción de Td diaria en PISCO; insumos, grilla, climatologías y bloques de prueba (2009–2012 y 2013–2016). Qué se conoce en el bloque reconstruido.
2. **Métodos.** `tuned` de Palacios como método principal; TimesFM `tmin_anom_full` como alternativa sin ajuste de pesos. Controles: climatología (cuánto aporta usar Tmin), LLR simple y LLR con rezagos seleccionado (separan la ventaja frente a `tuned` de la ventaja frente a un LLR local sin zonificación). Inventario de diseño de cada método (tabla de la sección de costo).
3. **Resultados agregados.** RMSE, MAE y sesgo en Perú y dominio completo, en los dos bloques. Brechas pareadas con los dos esquemas de IC existentes, explicando qué dependencia conserva cada uno.
4. **Robustez y dónde cambia la ventaja.** Que el resultado frente a `tuned` no depende de una configuración ni del bloque; magnitudes por año y por zona. El conteo de zonas ganadas queda como registro secundario.
5. **Costo: entrenamiento, inferencia y total.** `tuned` concentra el costo en el entrenamiento y predice rápido; TimesFM no entrena y concentra el costo en la inferencia. Se compara el total con el hardware y las condiciones de cada corrida.
6. **Lectura para la tesis.** TimesFM sustituye la etapa de diseño y entrenamiento y obtiene menor error que `tuned`. `tuned` sigue conviniendo cuando sus coeficientes ya existen y se reconstruyen períodos nuevos, porque su inferencia toma minutos.
7. **Límites.** Lo que no se probó (sección final de este documento).

El orden importa por una razón: la sección 6 solo puede apoyarse en lo mostrado en 3–5. Si una recomendación necesita un resultado que no aparece antes, falta evidencia o sobra la recomendación.

## Mapa de evidencia

`ll4` es el bloque con prueba 2013–2016; `ll4b`, el de prueba 2009–2012. Los nombres de método son los de `a1_por_metodo.csv`.

| Afirmación que el paper puede hacer | Evidencia | Fuente | Destino |
|---|---|---|---|
| TimesFM tiene menor RMSE puntual que `tuned` en ambos bloques y ámbitos | `timesfm_anom` frente a `tuned` | `a1_por_metodo.csv`, `a1_brechas.csv` | Cuerpo |
| La ventaja se reduce frente a un LLR local sin zonificación; en dominio completo 2013–2016 los IC de esa brecha incluyen cero | `timesfm_anom` frente a `llr_rezagos_sel` | `a1_brechas.csv` | Cuerpo |
| Usar Tmin del bloque mejora sobre la climatología en todos los métodos | `clim` frente al resto | `a1_por_metodo.csv` | Cuerpo |
| La elección no se reduce al RMSE | MAE y sesgo de cada método | `a1_por_metodo.csv` | Cuerpo |
| La ventaja varía por año y zona | brechas descriptivas por año y zona, sin IC propios | `a1_por_metodo.csv` (periodo), `a1_por_zona.csv` | Cuerpo |
| El costo de `tuned` está en el entrenamiento y su inferencia es rápida; TimesFM no entrena y su costo está en la inferencia; en `ll4b` el total es del mismo orden | tiempos por etapa en la misma máquina | `costo.csv`, `costo.md` | Cuerpo, con sus condiciones |
| `tuned` requiere zonas, recetas y ajuste; TimesFM, datos de la celda y una configuración elegida una vez | inventario de diseño | `costo.md` (insumos de diseño), `costo.csv` (`insumos_de_diseno`) | Cuerpo (métodos y costo) |
| La configuración de TimesFM se eligió sin mirar 2009–2012 | cribado sobre 2013–2016 | `costo.md` (cribado), `experiments/timesfm/variants.py` | Cuerpo (métodos) |
| La ventaja frente a `tuned` no depende de acertar la configuración | 6 de las 9 variantes superan a `tuned` en el cribado limpio | `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv` | Cuerpo (robustez) |
| Frente a `tuned`, la ventaja no depende de trabajar en anomalías | `timesfm_td` (Td y Tmin crudas) frente a `tuned` en `ll4b` | `a1_por_metodo.csv` | Cuerpo (robustez); frente a los LLR, suplemento |
| Condiciones de uso: Tmin del bloque e historial largo | variantes sin Tmin y con 2 años de contexto no superan a `tuned` | `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv` | Cuerpo (condiciones) |
| Parte del comportamiento de `tuned` depende de los rezagos de Td | `tuned_sin_td` | `a1_por_metodo.csv` | Suplemento |
| La comparación incluye un rival local competitivo | `llr_simple_sel`, `llr_rezagos_sel` (búsqueda ampliada de ventana y año inicial) | `a1_por_metodo.csv` | Suplemento (el seleccionado con rezagos también figura en el cuerpo como control) |
| Sensibilidad al inicio del historial y de la climatología | escalera de contexto, `timesfm_anom_med` | `a1_escalera_contexto.csv`, `a1_escalera_contexto_brechas.csv` | Suplemento |
| TimesFM depende de que Tmin corresponda al período reconstruido | Tmin barajada | `a3_control_tmin_barajada.csv` | Suplemento |
| Contraste externo limitado frente a estaciones ISD | A4 (muestra pequeña; independencia respecto de PISCO sin verificar) | `a4_contraste_externo.md`, `a4_*` sin ERA5 | Suplemento |
| Acuerdo entre productos 2017–2020 | comparación TimesFM–Palacios fuera del período de prueba | `a4_*` | Suplemento; acuerdo no es exactitud |

`ORIENTACION_PAPER.md` y la sección «Paper» del artefacto tienen una tabla de este tipo. Esta guía sube al cuerpo el inventario de diseño, la robustez frente a la configuración y las condiciones de uso; los otros dos lugares deben actualizarse para que el reparto coincida.

Sobre los IC. Los existentes son del RMSE pareado, por bootstrap espacial en bloques de 2° o por bloques mes-año. El espacial conserva las series completas dentro de cada bloque y rompe la dependencia entre bloques vecinos; el mensual conserva la dependencia espacial dentro del mes y rompe la que hay entre meses. Ninguno cubre las dos a la vez. Se presentan como sensibilidades, no como certificación de superioridad.

## Costo: entrenamiento, inferencia y total

En el método de Palacios el costo está en el entrenamiento. Antes de predecir hay que seleccionar una receta por zona × día del año y ajustar los coeficientes de cada celda; hecho eso, la inferencia es rápida. TimesFM no tiene esa etapa: los pesos vienen preentrenados, no se ajustan y no hay recetas que buscar. Su costo está en la inferencia.

| Escala | Etapa | `tuned` | TimesFM `tmin_anom_full` |
|---|---|---|---|
| Bloque `ll4b`, 17.027 celdas, misma máquina | Selección de recetas | 52 min 38 s (sobre 5.506 celdas de muestra) | no aplica |
| | Ajuste + predicción / predicción | 5 min 50 s | 73 min 10 s |
| | Total | ≈58 min | ≈73 min |
| Producto de Palacios | Selección de recetas y ajuste (1981–2016) | 32 h 41 min + 6 h 45 min | no aplica |
| | Predicción 2017–2020 (2.178.827 celdas) | 19 min 40 s | ≈5,1 días |

Fuentes: `resultados/costo.csv` y `resultados/costo.md`.

Lectura. En el bloque de prueba, contando las etapas que cada método necesita para reconstruir sin ver el bloque oculto, el total es del mismo orden. A escala de producto, TimesFM se ahorra unas 39 h de entrenamiento, pero su inferencia supera ese total. Además, una vez entrenado, `tuned` reconstruye un período nuevo en minutos, mientras que TimesFM paga la inferencia completa cada vez. Por eso el argumento de E no es el cómputo. Es que TimesFM elimina la etapa de diseño y entrenamiento, con un cómputo total del mismo orden en el bloque de prueba y mayor a escala de producto.

La configuración de TimesFM se eligió una sola vez, en un cribado de nueve variantes sobre 2013–2016 (49 min sobre 1.106 celdas), y se reutilizó sin cambios en 2009–2012. No se repite por bloque ni por zona.

| | `tuned` | TimesFM |
|---|---|---|
| Información del país | shapefile SENAMHI de 41 zonas climáticas | ninguna fuera de los datos de cada celda |
| Búsqueda previa | receta y `h` por zona × día del año, con un pool de 11 términos (12.444 recetas en `ll4b`) | una configuración entre 9, elegida una vez |
| Ajuste | coeficientes por celda; pronóstico autorregresivo con sus rezagos de Td | ninguno; checkpoint preentrenado de 330M parámetros |
| Datos de cada celda | historial de Td y Tmin, climatología, Tmin del bloque | los mismos |
| Hardware | GPU (CuPy) para selección y ajuste | GPU para inferencia |

Fuente: `costo.md`, sección «Insumos de diseño».

Condiciones de la comparación:

- Las corridas de producto no forman una comparación controlada: los logs de Palacios no registran el host, y la corrida de TimesFM compartió la GPU con otros procesos en algunos tramos.
- El regrillado de Tmin, la preparación de PISCO y las climatologías son trabajo compartido por los dos métodos y no se cargan a ninguno.
- Los tiempos de `llr_simple_sel` y `llr_rezagos_sel` no se midieron; las filas de LLR de `costo.csv` son de versiones anteriores y no se emparejan con su RMSE.
- Las horas de trabajo humano no se midieron. El inventario de diseño las sustituye de forma cualitativa.

## Robustez del resultado frente a `tuned`

- TimesFM tiene menor RMSE que `tuned` en los dos bloques y los dos ámbitos, y los dos esquemas de IC excluyen el cero en los cuatro casos (`a1_brechas.csv`). El bloque 2009–2012 no participó en la elección de la configuración.
- La ventaja no depende de acertar la configuración. En el cribado limpio (1.092 celdas, 2013–2016), 6 de las 9 variantes tienen menor RMSE que `tuned` (`reports/timesfm_benchmark/cribado_limpio/leaderboard.csv`). El cribado no tiene IC y se hizo sobre el mismo bloque en que se eligió la variante.
- Frente a `tuned`, tampoco depende de trabajar en anomalías: `tmin_td_full`, con Td y Tmin crudas, tiene menor RMSE que `tuned` en 2009–2012 en los dos ámbitos (`a1_por_metodo.csv`, método `timesfm_td`).

Las tres variantes que no superan a `tuned` son las dos que no reciben Tmin y la que tiene solo 2 años de contexto. Eso define las condiciones de uso: Tmin del bloque reconstruido e historial local largo (con 11 años, `tmin_td_med`, ya supera a `tuned`). A esto se suma la licencia no comercial de los pesos, que limita cualquier recomendación de uso operativo.

El LLR con rezagos seleccionado tampoco usa zonas y queda cerca de TimesFM. Para la tesis se presenta así: también requiere una búsqueda por bloque (ventana y año inicial) y un ajuste por celda. TimesFM lo supera en tres de las cuatro combinaciones con IC sin cero; en la cuarta (dominio completo, 2013–2016) no se distinguió una diferencia. La tesis se formula frente al método diseñado de Palacios, y el LLR local entra como control, sin afirmar que exija conocer el país.

## Interpretaciones retiradas

| Afirmación anterior | Por qué no se sostiene | Formulación correcta | Estado |
|---|---|---|---|
| La historia se elige entre las narrativas E y C+A según si una brecha deja de excluir cero | Un umbral estadístico no responde cuándo conviene cada método; una diferencia pequeña o incierta también informa la elección | Se retira la regla; E se conserva como tesis acotada frente a `tuned`, apoyada en precisión, robustez y costo | Retirada en `HANDOFF.md`, `sintesis_amenazas.md` y `ORIENTACION_PAPER.md` |
| LLR exige conocer y zonificar el país | Un LLR con ventana global y sin zonas queda cerca de TimesFM; sigue ajustando coeficientes por celda, sin mapa climático | La zonificación por zona × día del año es la adaptación específica de `tuned` | Corregida en síntesis y orientación |
| El diseño experto de Palacios no mejora | Se compararon implementaciones con distintos criterios de selección, ventanas y tratamiento autorregresivo; esa contribución no se aisló | Se informa la diferencia entre `tuned` y los LLR sin zonas, sin atribuirla a un componente | Corregida en síntesis |
| A TimesFM solo se le pasa Tmin | Recibe historial local de Td y Tmin; `tmin_anom_full` usa climatologías locales | Durante el bloque reconstruido se aporta Tmin, sin ajustar los pesos de TimesFM; antes requiere historial y climatologías | Corregida en orientación y artefacto |
| La reconstrucción es un pronóstico | Tmin de todo el bloque es conocida | Reconstrucción con covariable observada, para ambos métodos | Corregida en orientación |
| PISCO cambia de régimen MODIS en 2000 y el contexto desde 2002 lo controla | Huerta et al. (2022, 2023) describen promedios mensuales de LST como predictores espaciales también para fechas anteriores a MODIS | La escalera es una sensibilidad al inicio del historial | Retirada en HANDOFF y síntesis. La nota de `tmin_anom_med` en `experiments/timesfm/variants.py:124` todavía conserva la explicación anterior |
| El barajado de Tmin demuestra que el historial de Td no aporta | Muestra dependencia de que Tmin esté alineada con el período; para aislar el aporte de Td habría que alterar el historial con Tmin correcta | TimesFM es sensible a la covariable correcta; el aporte marginal de Td histórica no se aisló | Corregida en síntesis y orientación |
| Un IC que incluye cero es un empate | Sin margen de equivalencia justificado de antemano, solo indica que el análisis no distinguió el signo | «No se distinguió una diferencia con este análisis» | Corregida en HANDOFF, síntesis y artefacto |
| El regrillado de Tmin es costo de LLR | TimesFM consume la misma Tmin regrillada | Preprocesamiento compartido | Corregida en artefacto y orientación |
| Tiempos de LLR anteriores junto al RMSE del LLR seleccionado | Son versiones distintas, con grilla y búsqueda diferentes | Tiempos de los LLR seleccionados: no medidos | Corregida en artefacto |
| El panel nacional representa a Perú | 8.755 de 17.027 celdas están fuera del país | Perú y dominio completo por separado; el dominio completo es el mismo producto, no otra región | Corregida en artefacto |
| A4 valida el producto frente a estaciones | Muestra pequeña; independencia de las estaciones ISD respecto de PISCO no verificada | Contraste externo limitado, en suplemento | Corregida en síntesis |
| ERA5 y ONI como ejes de comparación | Cambian de dataset y desplazan el artículo hacia validación de productos o mecanismos climáticos | Fuera de la comparación | ERA5 retirado del artefacto y la síntesis |
| «Se reprodujo `ll4`» | Se reutilizaron predicciones existentes | «Se reutilizaron las predicciones de `ll4`» | Señalado en la auditoría |

## Formulaciones

Usar:

- «TimesFM sin ajuste de pesos», con la lista de lo que sí requiere.
- «La adaptación específica del método de Palacios» al referirse a zonas y recetas.
- «No se distinguió una diferencia con este análisis» cuando el IC incluye cero.
- «En las corridas disponibles», «en esta muestra», al hablar de costos y de A4.
- «Reconstrucción con Tmin observada del bloque».
- «Sin entrenamiento, sin zonificación y sin búsqueda de recetas» para TimesFM.
- «El costo de `tuned` está en el entrenamiento; el de TimesFM, en la inferencia».

Evitar:

- «TimesFM es más barato» o «más rápido» en cómputo total.

- «Solo Tmin», «sin conocer el país», «plug-and-play».
- «Empatan», «equivalentes», «indistinguibles» como conclusión.
- «LLR requiere zonificación» sin precisar que se trata de `tuned`.
- «Pronóstico» para el bloque reconstruido.
- Cualquier explicación de mecanismo físico o de producto (MODIS, ENSO) que no se haya probado.
- Resumir una comparación por zona con el número de victorias sin la magnitud.

## Qué no se ha probado

- Desempeño sin historial local de Td.
- Tmin del bloque ausente o con error sistemático.
- Aporte marginal del historial de Td en TimesFM.
- Una comparación de costos homogénea: hardware, documentación de corridas y separación de etapas son desiguales, y los tiempos de los LLR seleccionados faltan.
- Horas de trabajo humano para preparar cada método.

Estos puntos van al apartado de límites del paper. Ninguno es necesario para la comparación dentro de PISCO tal como está planteada.

## Uso de IA generativa

Este documento se redactó con asistencia de IA generativa (Claude), a partir de la auditoría y las correcciones hechas con Codex. Su contenido debe validarse con Palacios y SENAMHI antes de trasladarlo al paper.
