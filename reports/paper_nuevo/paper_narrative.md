# Maquetación narrativa del paper nuevo (TimesFM frente a `tuned`)

Documento de estructura, redactado el 21 de octubre de 2026. No es el paper ni un borrador de sus `.qmd`: fija la historia que el artículo cuenta, el orden de las secciones, las ideas y la evidencia de cada una, y comprueba que las afirmaciones finales se apoyen en algo mostrado antes.

## 1. Propósito y fuentes

La decisión editorial está en `ORIENTACION_PAPER.md` (tesis E acotada, reparto cuerpo/suplemento). La guía principal es `historia_paper.md`: supuestos de comparabilidad, mapa de evidencia, costo, interpretaciones retiradas y formulaciones permitidas o prohibidas. Se ordena ese material en secciones de artículo con las decisiones ya armonizadas: `ll4b` primero, resumen de A2 en el cuerpo y costo de selección de TimesFM contabilizado una sola vez.

Las cifras mandan desde los CSV de `resultados/` (`a1_por_metodo.csv`, `a1_brechas.csv`, `a1_por_zona.csv`, `costo.csv`) y desde `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv`. Aquí solo se citan cuando justifican una decisión de estructura. Convenciones: `ll4` es el bloque de prueba 2013–2016 (contexto hasta 2012) y `ll4b` el de 2009–2012 (contexto hasta 2008); «dominio completo» o «panel» son las 17.027 celdas puntuadas y «Perú» las 8.272 que caen dentro del país; brecha = RMSE(A) − RMSE(B) en °C, negativa a favor de A.

El paper vigente de Palacios (`reports/paper/`, `PAPER_PLAN.md`) no se toca. Si se reutiliza su descripción de datos o del método `tuned`, se copia a `reports/paper_nuevo/` con atribución.

## 2. La historia

El registro PISCO de temperatura de punto de rocío (Td) diaria termina en 2016 y el de Tmin continúa hasta 2020. Para reconstruir ese intervalo, el método `tuned` de Palacios agrupa las celdas en las 41 unidades cartográficas de SENAMHI (38 tipos climáticos y tres unidades adicionales: dos lagos y lomas costeras) (33 de ellas tienen celdas en el panel evaluado y 32 en Perú; `a1_por_zona.csv`), busca una receta de regresión local por zona y día del año, y ajusta coeficientes en cada celda. El artículo pregunta si un modelo fundacional de series de tiempo, TimesFM 3.0, usado sin ajustar sus pesos y con los mismos insumos locales, reconstruye Td con menor error, y qué cuesta hacerlo.

La respuesta que el artículo sostiene es acotada. En PISCO y en los dos bloques evaluados, TimesFM (`tmin_anom_full`) tuvo menor RMSE que `tuned` en Perú y en el dominio completo, sin zonificación, sin selección de recetas por zona y día del año y sin ajuste de pesos locales. Esa ventaja tiene condiciones: TimesFM necesita historial local de Td y Tmin, climatologías y la Tmin observada de todo el bloque, y su configuración se eligió en un cribado sobre 2013–2016. La ventaja no es uniforme: se concentra en 2015–2016 y 2010–2012, y en 2013 se invierte en el dominio completo. Un LLR local sin zonas queda cerca de TimesFM. Una variante de `tuned` sin rezagos autorregresivos de Td reduce buena parte de la distancia en 2013–2016 (0,054 de los 0,074 °C del dominio completo) y poco en 2009–2012 (0,014 de 0,076) (`a1_brechas.csv`). En cómputo, `tuned` paga en el entrenamiento y TimesFM en la inferencia; el total no favorece a TimesFM.

La historia avanza como la secuencia de preguntas que un lector se haría en orden: por qué importa el problema y qué se ha hecho; qué datos hay y qué se conoce en el bloque que se reconstruye; qué exige cada método antes de producir un valor; cómo se evalúa sin que la selección contamine la prueba; quién reconstruye mejor en agregado; si esa ventaja es estable o dónde cambia; si depende de una configuración afortunada o de una debilidad concreta del rival; cuánto cuesta; cuándo conviene cada uno; y qué queda sin probar. El LLR sin zonas atraviesa toda la secuencia como control: separa «ventaja frente a `tuned`» de «ventaja frente a cualquier regresión local».

El lector debería salir con tres ideas, en este orden de seguridad: TimesFM sin ajuste de pesos reconstruyó Td en PISCO con menor error que el método diseñado por zona, en los dos bloques; en 2013–2016 una variante de `tuned` sin rezagos de Td reduce buena parte de esa distancia y en 2009–2012 poco, y frente a un LLR local sin zonas la ventaja es pequeña; y TimesFM prescinde de zonificación, selección de recetas por zona y día del año y ajuste de pesos locales, conserva una selección de configuración hecha una vez y no reduce el cómputo total.

## 3. Secciones propuestas

### 3.1 Introducción

Pregunta: por qué importa reconstruir Td diaria y qué opciones existen.

Ideas. Vacío del registro de Td después de 2016 y continuidad de Tmin hasta 2020, como en la introducción del artículo previo. Las aplicaciones agrícolas o de salud se incluyen solo con referencias comprobadas. La escasez de estaciones que miden Td en Perú y la existencia de productos grillados (PISCO; Huerta et al. 2022, tabla 1; 2023, como los citan `historia_paper.md` y `sintesis_amenazas.md`; verificar en texto completo). En `reports/paper/references.bib` existe la clave `huerta2022` (PISCOeo_pm, *Scientific Data* 9, 328, doi 10.1038/s41597-022-01373-8), que se copiaría a la bibliografía de esta carpeta sin editar el original; no hay entrada para Huerta et al. 2023, y falta confirmar cuál es la referencia del producto Td. El método de regresión local adaptado por zona de Palacios como antecedente (citar el paper vigente como antecedente, sin modificarlo). Los modelos fundacionales de series de tiempo y TimesFM en particular (referencias por verificar; no se cita ningún autor ni año que no esté confirmado). La pregunta del artículo y el ámbito: PISCO, dos bloques retrospectivos.

Evidencia: ninguna cifra propia. Las referencias de Td, modelos fundacionales y TimesFM quedan marcadas «por verificar» hasta que alguien las confirme.

No debe afirmar que TimesFM «no necesita conocer el país», que «solo usa Tmin», ni anticipar un resultado más fuerte que el de la sección 3.5.

Entrega: plantea la pregunta, y la sección siguiente precisa qué datos la hacen comparable.

### 3.2 Datos y problema de reconstrucción

Pregunta: qué datos hay y qué se conoce en el bloque reconstruido.

Ideas. Productos PISCO de Td y Tmin, versiones y grilla de Palacios; regrillado de Tmin y climatologías de entrenamiento como preparación compartida. Comparabilidad: mismos productos, climatologías de referencia, celdas y fechas; las diferencias de selección, historial usado y rezagos forman parte de cada método. El problema es de reconstrucción con Tmin observada del bloque, no de pronóstico. Panel de 17.027 celdas, de las cuales 8.755 están fuera de Perú: se reportan Perú y dominio completo por separado, y el dominio completo es el mismo producto, no otra región. El artículo previo describe covariables espaciales compartidas entre Td y Tmin. El detalle de LST de MODIS y la referencia Huerta 2023 se mantienen como bibliografía por comprobar, sin atribuirles un mecanismo. La máscara política de Perú usada aquí difiere del ámbito clasificado del artículo previo.

Evidencia: Figura 1 (mapa del panel, Perú y fuera de Perú, zonas SENAMHI), desde `reports/timesfm_benchmark/panels/nacional_17027.csv` y la tabla de zonas.

No debe usar «pronóstico» para el bloque, ni presentar el dominio completo como prueba de transferencia.

Entrega: con los datos fijados, la pregunta pasa a ser qué hace cada método con ellos.

### 3.3 Métodos y lo que exige cada uno

Pregunta: qué preparación requiere cada método antes de producir un valor.

Ideas. `tuned`: zonas SENAMHI, pool de 11 términos, selección de receta y semiancho `h` por zona × día del año mediante validación dejando un año fuera y coseno sobre anomalías, ajuste por celda y despliegue autorregresivo con sus rezagos de Td. TimesFM `tmin_anom_full`: checkpoint preentrenado de 330M parámetros, anomalías de Td y Tmin respecto de la climatología de Palacios como contexto y Tmin del bloque como covariable, sin modificar pesos; configuración elegida una vez entre nueve. Controles: climatología (referencia sin Tmin del bloque) y los LLR sin zonas, en particular `llr_rezagos_sel` (ventana y año inicial elegidos por validación interna). La diferencia de preparación aparece aquí: es el argumento de la tesis y debe mostrarse antes de cualquier resultado. «Sin ajuste de pesos» no significa sin preparación local ni sin selección.

Evidencia: Tabla 1, inventario de diseño (información del país, búsqueda previa, ajuste, datos por celda, hardware, licencia de pesos: no comercial para el checkpoint de TimesFM, no aplica a `tuned` ni a los LLR), desde `costo.md` («Insumos de diseño») y la columna `insumos_de_diseno` de `costo.csv`.

No debe decir que «LLR requiere zonificación»: la zonificación es la adaptación específica de `tuned`. Tampoco atribuir a la licencia de TimesFM más que un límite al uso operativo.

Entrega: el inventario deja claro que la selección de configuración de TimesFM tocó un bloque, lo que obliga a explicar el protocolo de evaluación.

### 3.4 Protocolo de evaluación

Pregunta: cómo se evalúa sin que la selección contamine la prueba.

Ideas. Dos bloques retrospectivos. `ll4b` (2009–2012) es la evaluación principal (decisión cerrada) porque no participó en la elección de la configuración de TimesFM; `ll4` (2013–2016) se lee sabiendo que el cribado se hizo sobre ese bloque. Las recetas de `tuned` y la selección de los LLR usan solo años de entrenamiento. El `tuned` de `ll4b` se corrió con el código del repositorio, no con el entorno de Palacios; en `ll4` ese código reprodujo la cifra limpia de referencia (1,2279; `sintesis_amenazas.md` §6), y el protocolo lo declara. Métricas: RMSE, MAE y sesgo, sobre las mismas filas celda × día en cada ámbito para todos los métodos. Brechas pareadas con dos esquemas de IC por bootstrap (bloques espaciales de 2° y bloques mes-año): el espacial conserva las series completas y rompe la dependencia entre bloques vecinos; el mes-año conserva la dependencia espacial dentro del mes y rompe la que hay entre meses; ninguno cubre ambas. Un IC que incluye cero se lee como «no se distinguió una diferencia con este análisis». Las brechas por año y zona son descriptivas, sin IC.

Evidencia: Tabla 2 (bloques, años de contexto y de prueba, qué etapa de selección vio cada bloque, celdas y filas), compuesta desde `a1_desglose.md` y `costo.md`.

No debe presentar los IC como certificación de superioridad ni como prueba de equivalencia.

Entrega: con las reglas de lectura fijadas, se presentan los resultados agregados.

### 3.5 Resultados agregados

Pregunta: quién reconstruye mejor en agregado.

Ideas. Los métodos de la comparación principal que usan Tmin del bloque tienen menor RMSE que la climatología; esta comparación no aísla por sí sola el efecto de Tmin. TimesFM tiene el menor RMSE puntual en los dos bloques y ámbitos; frente a `tuned` las cuatro brechas excluyen cero con los dos esquemas. Frente a `llr_rezagos_sel` la diferencia es menor: en `ll4b` y en Perú excluye cero; en el dominio completo de `ll4` no se distinguió una diferencia. Para ordenar la lectura, `ll4b` va primero: panel 1,122 (`tuned`), 1,074 (`llr_rezagos_sel`), 1,046 (TimesFM); Perú 0,861, 0,830 y 0,804 (`a1_por_metodo.csv`). La elección no se reduce al RMSE: en `ll4` dominio completo TimesFM tiene MAE menor que `tuned` (0,830 frente a 0,881) pero sesgo mayor en magnitud (+0,104 frente a −0,033). Ese patrón se repite en Perú en los dos bloques; solo en `ll4b` dominio completo el sesgo de TimesFM es menor que el de `tuned` (−0,108 frente a −0,156) (`a1_por_metodo.csv`). El sesgo debe aparecer en la tabla principal, no en el suplemento.

Evidencia: Tabla 3, RMSE, MAE y sesgo de climatología, `tuned`, `llr_rezagos_sel` y TimesFM, por bloque y ámbito (`a1_por_metodo.csv`, `periodo = total`). Figura 2, brechas pareadas TimesFM − `tuned` y TimesFM − `llr_rezagos_sel` con los dos IC, por bloque y ámbito (`a1_brechas.csv`).

No debe decir «empatan» o «equivalentes» para la brecha con `llr_rezagos_sel` en `ll4` dominio completo, ni «TimesFM gana» sin mencionar el sesgo.

Entrega: un agregado de cuatro años puede esconder años o regiones donde el orden cambia; eso se revisa a continuación.

### 3.6 Dónde cambia la ventaja

Pregunta: si la ventaja es estable o dónde cambia.

Ideas. Por año, en el dominio completo, la brecha TimesFM − `tuned` fue +0,055 en 2013 (TimesFM peor que `tuned`, y peor que `llr_rezagos_sel` por +0,060), −0,059 en 2014, −0,165 en 2015 y −0,126 en 2016; en `ll4b`, −0,009 en 2009 y mayor en 2010–2012 (`a1_por_metodo.csv`, `periodo` por año). En Perú todas las brechas anuales TimesFM − `tuned` son negativas. La ventaja se concentra en 2015–2016 y 2010–2012. El año 2013 se muestra en el cuerpo: es el único caso en que el orden se invierte, solo ocurre en el dominio completo, y en ese año el sesgo fue +0,350 para TimesFM y +0,207 para `tuned` (`a1_por_metodo.csv`). No se le atribuye causa; con un bloque por período no se separa si es propio de 2013 o de las celdas fuera del país (`sintesis_amenazas.md` §6). Por zona, TimesFM tiene menor RMSE que `tuned` en todas las zonas, con brechas entre −0,03 y −0,30 °C en `ll4` y entre −0,03 y −0,18 °C en `ll4b` (`a1_por_zona.csv`); se reporta la magnitud, y el conteo de zonas ganadas queda en el suplemento. Frente a `llr_rezagos_sel`, en `ll4` dominio completo una zona tiene brecha positiva: +0,014 en la zona 0 (`A (r) A'`, 7.091 celdas; `a1_por_zona.csv`).

Evidencia: Figura 3, brecha anual TimesFM − `tuned` y TimesFM − `llr_rezagos_sel` por ámbito, 2009–2016 (`a1_por_metodo.csv`). Figura 4, brecha por zona frente a `tuned` y frente a `llr_rezagos_sel`, ordenada por magnitud y con número de celdas (`a1_por_zona.csv`).

No debe explicar 2015–2016 por El Niño ni 2013 por un mecanismo físico o de producto; no se probó ninguno.

Entrega: la variación por año plantea si el resultado depende de algo particular, de la configuración de TimesFM o del diseño de `tuned`.

### 3.7 Sensibilidad del resultado

Pregunta: si la ventaja depende de una configuración afortunada o de una debilidad concreta del rival.

Ideas, en este orden:

1. Configuración. En el cribado limpio (1.092 celdas, 2013–2016), 6 de las 9 variantes tienen menor RMSE que `tuned` (0,933); pierden las dos univariadas sin Tmin (1,278 y 1,312) y `tmin_td_short`, con 2 años de contexto (0,948) (`leaderboard.csv`). `tmin_td_full` y `tmin_td_znorm` tienen RMSE casi iguales (diferencia ≈1,12 × 10⁻⁸ °C), sin haberse comprobado la igualdad de sus predicciones. Se mantienen las nueve variantes y las seis con RMSE menor que `tuned`. El cribado se hizo en el bloque que luego se evalúa y no tiene IC. Esto describe el cribado observado. La referencia usa contexto desde 1981; la escalera con climatología fija muestra cambios pequeños al recortar hasta 2002 (+0,002 °C en `ll4b`, +0,005 °C en `ll4`). No se determinó el historial mínimo necesario.
2. Representación. `timesfm_td` (Td y Tmin sin anomalías) tiene menor RMSE que `tuned` en `ll4b` en los dos ámbitos (1,106 frente a 1,122 en el dominio completo; `a1_por_metodo.csv`), pero queda detrás de `llr_rezagos_sel` y es peor que `tuned` en 2009 (1,185 frente a 1,035). El control muestra una ventaja agregada pequeña sin anomalías en `ll4b`; no prueba independencia general de la representación.
3. Rezagos de Td en `tuned`. `tuned_sin_td`, el mismo protocolo sin rezagos de Td en el pool, tiene RMSE 1,174 en `ll4` dominio completo, mejor que `tuned` (1,228). Frente a él la brecha de TimesFM baja a −0,021, con IC mes-año que incluye cero (`a1_brechas.csv`). En `ll4b` el efecto es menor: `tuned_sin_td` mejora a `tuned` en 0,014 y la brecha de TimesFM frente a él (−0,062) sigue excluyendo cero. Esta sección va en el cuerpo porque un revisor preguntará si la ventaja viene de esa decisión de `tuned`. Se informa sin atribuir causalidad y matiza la tesis: TimesFM supera a `tuned` tal como fue diseñado; frente a variantes LLR sin esa dependencia la ventaja es menor, sobre todo en 2013–2016.

Evidencia: Tabla 4, las nueve variantes del cribado con RMSE, MAE, sesgo y su relación con `tuned` (`leaderboard.csv`). Tabla 5, `tuned`, `tuned_sin_td`, `llr_rezagos_sel`, `timesfm_td` y TimesFM por bloque y ámbito, con las brechas disponibles de TimesFM frente a `tuned`, `tuned_sin_td` y `llr_rezagos_sel` (`a1_por_metodo.csv`, `a1_brechas.csv`). `timesfm_td` solo tiene evaluación en `ll4b`; las parejas sin IC calculado se identifican como diferencias puntuales, sin inventar intervalos.

No debe afirmar que los rezagos de Td «causan» la desventaja de `tuned`, ni que el diseño experto «no aporta»: las variantes comparadas difieren en selección, ventana y tratamiento autorregresivo, y esa contribución no se aisló.

Entrega: establecido que la ventaja tiene condiciones y un tamaño que depende del rival, queda la pregunta de qué cuesta.

### 3.8 Costo

Pregunta: qué cuesta cada método, por etapa y en total.

Ideas. `tuned` concentra el costo en el entrenamiento: en `ll4b`, 52 min 38 s de selección de recetas y 5 min 50 s de ajuste y predicción, unos 58 min. TimesFM no ajusta pesos locales: 73 min 10 s de predicción en `ll4b`, más el cribado de 49 min 8 s, que se pagó una sola vez y se suma como costo único de selección, como pide `costo.md`; el total queda en 122 min 18 s, frente a 58 min 28 s de `tuned`. El cribado se reutiliza y no se vuelve a cargar por bloque. A escala de producto, `tuned` necesitó unas 39 h de selección y ajuste (1981–2016) y predijo 2017–2020 en 19 min 40 s; TimesFM predijo el mismo período en unos 5,1 días (`costo.csv`). El argumento de la tesis es que TimesFM prescinde de zonificación, selección de recetas por zona y día del año y ajuste de pesos locales, y conserva una selección de configuración hecha una vez; el cómputo total no lo favorece. Condiciones: corridas no controladas (host de Palacios sin registrar, GPU compartida en tramos de la corrida de producto), preprocesamiento compartido sin cronometrar, tiempos de los LLR seleccionados no medidos, horas humanas no medidas.

Evidencia: Tabla 6, costo por etapa y total en `ll4b` (misma máquina) y a escala de producto, con hardware y fuente de cada fila (`costo.csv`, `costo.md`). La Tabla 1 ya cubre la parte cualitativa.

No debe decir «más barato» ni «más rápido» para TimesFM, ni poner junto al RMSE de los LLR seleccionados los tiempos de versiones anteriores.

Entrega: con precisión, condiciones y costo a la vista, se puede responder cuándo conviene cada uno.

### 3.9 Discusión: cuándo conviene cada método

Pregunta: con lo mostrado, cuándo conviene cada método.

Ideas. TimesFM puede convenir cuando se dispone del historial local de la configuración evaluada (sin mínimo necesario determinado), Tmin observada del bloque, GPU y tiempo de inferencia, y no se quiere diseñar zonas ni recetas; la licencia no comercial de los pesos limita el uso operativo. `tuned` conviene cuando sus coeficientes ya existen y se reconstruyen períodos nuevos, porque su inferencia toma minutos. Un LLR local sin zonas es una alternativa cercana en precisión; su costo seleccionado no se midió. La diferencia entre `tuned` y los LLR sin zonas se informa sin atribuirla a un componente. El contraste externo con estaciones ISD y la comparación de productos 2017–2020 se mencionan como alcance limitado, con remisión al suplemento: acuerdo entre productos no equivale a exactitud.

Evidencia: ninguna nueva; cada recomendación remite a 3.3, 3.5–3.8 (ver sección 5).

No debe introducir resultados que no estén antes ni mecanismos físicos no probados.

Entrega: las condiciones de la recomendación llevan a lo que no se probó.

### 3.10 Límites

Pregunta: qué no se probó.

Ideas. Desempeño sin historial local de Td; Tmin del bloque ausente o con error sistemático; aporte marginal del historial de Td en TimesFM (el barajado de Tmin no lo aísla); IC que no cubren a la vez la dependencia espacial y la temporal; selección de la configuración sobre `ll4`; costo sin comparación homogénea; horas humanas; rivales LLR y `tuned_sin_td` construidos en este proyecto y aún sin revisión de Palacios; `tuned` de `ll4b` corrido con el código del repositorio y no con el entorno de Palacios; grillas de `h` distintas entre `tuned` (7–45) y los LLR seleccionados (hasta 180); posibles insumos espaciales compartidos entre Td y Tmin, con detalle bibliográfico de MODIS por comprobar. Transferencia a otros productos o regiones fuera de alcance.

Evidencia: remite a `historia_paper.md` («Límites y referencias») y a `sintesis_amenazas.md` §6.

Entrega: cierra el artículo antes de la conclusión.

### 3.11 Conclusión

Un párrafo. Repite el resultado con sus condiciones: en PISCO y en 2009–2012 y 2013–2016, TimesFM sin ajuste de pesos reconstruyó Td con menor RMSE que `tuned`, sin zonificación, selección de recetas por zona y día ni ajuste de pesos locales, con el historial local de la configuración evaluada y Tmin observada del bloque; el historial mínimo no se determinó; la configuración se eligió sobre 2013–2016; la ventaja varía por año, frente a un LLR local sin zonas es pequeña, el sesgo de TimesFM fue de mayor magnitud que el de `tuned` en tres de los cuatro casos, y el costo pasa del entrenamiento a la inferencia. Sin perspectivas genéricas.

### 3.12 Suplemento

| Parte | Contenido | Origen | Función |
|---|---|---|---|
| S1 | A2: `tuned_sin_td` completo, por año y zona, y frente al LLR simple | `a1_por_metodo.csv`, `a1_brechas.csv`, `a1_por_zona.csv` | Detalle de lo resumido en 3.7 |
| S2 | A3: Tmin barajada entre años (tres semillas) y entre celdas | `a3_control_tmin_barajada.csv` | Muestra sensibilidad a la covariable correcta; no aísla el aporte de Td histórica |
| S3 | Escalera de contexto y `timesfm_anom_med` | `a1_escalera_contexto.csv`, `a1_escalera_contexto_brechas.csv` | Sensibilidad al inicio del historial y de la climatología; no prueba un quiebre de producto en 2000 |
| S4 | A4: contraste con estaciones ISD y comparación de productos 2017–2020 | `a4_contraste_externo.md`, `a4_*` (sin ERA5) | Alcance externo limitado; independencia de estaciones sin verificar |
| S5 | LLR no seleccionados (`llr_simple`, `llr_rezagos`) y `llr_simple_sel`, con sus brechas | `a1_por_metodo.csv`, `a1_brechas.csv` | Muestra que la cercanía de los LLR no depende de una sola variante |
| S6 | Conteo de zonas ganadas | `a1_victorias_zona.csv` | Registro secundario; siempre junto a la magnitud de la Figura 4 |
| S7 | Lista completa de corridas de costo | `costo.csv` | Trazabilidad de la Tabla 6 |

## 4. Figuras y tablas propuestas

| Núm. | Contenido | Origen | Sección |
|---|---|---|---|
| Figura 1 | Mapa del panel: Perú y fuera de Perú, zonas SENAMHI | `reports/timesfm_benchmark/panels/nacional_17027.csv`, tabla de zonas | 3.2 |
| Tabla 1 | Inventario de diseño por método | `costo.md`, `costo.csv` (`insumos_de_diseno`) | 3.3 |
| Tabla 2 | Bloques, contexto, prueba y qué selección vio cada uno | `a1_desglose.md`, `costo.md` | 3.4 |
| Tabla 3 | RMSE, MAE y sesgo por método, bloque y ámbito | `a1_por_metodo.csv` | 3.5 |
| Figura 2 | Brechas pareadas con IC espacial y mes-año | `a1_brechas.csv` | 3.5 |
| Figura 3 | Brecha anual 2009–2016 frente a `tuned` y `llr_rezagos_sel` | `a1_por_metodo.csv` | 3.6 |
| Figura 4 | Brecha por zona, ordenada por magnitud | `a1_por_zona.csv` | 3.6 |
| Tabla 4 | Nueve variantes del cribado frente a `tuned` | `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv` | 3.7 |
| Tabla 5 | `tuned`, `tuned_sin_td`, `llr_rezagos_sel`, `timesfm_td` y TimesFM con brechas | `a1_por_metodo.csv`, `a1_brechas.csv` | 3.7 |
| Tabla 6 | Costo por etapa y total, bloque y producto | `costo.csv`, `costo.md` | 3.8 |

Las figuras se generan con scripts en `experiments/` o en esta carpeta, nunca en `reports/paper/scripts/`.

## 5. Verificación de coherencia

### 5.1 Afirmaciones finales y dónde se mostraron

| Afirmación de la discusión o la conclusión | Sección previa | Evidencia |
|---|---|---|
| TimesFM tuvo menor RMSE que `tuned` en los dos bloques y ámbitos | 3.5 | Tabla 3, Figura 2 |
| La ventaja se observó también en 2009–2012, bloque que no participó en la selección (en 2009 la brecha fue −0,009 en el dominio completo) | 3.4, 3.5, 3.6 | Tabla 2, Tabla 3, Figura 3 |
| Frente a un LLR local sin zonas la ventaja es pequeña y en un caso no se distinguió | 3.5 | Figura 2 |
| La elección no se reduce al RMSE (sesgo) | 3.5 | Tabla 3 |
| La ventaja varía por año y se invierte en 2013 en el dominio completo | 3.6 | Figura 3 |
| En todas las zonas TimesFM tuvo menor RMSE que `tuned` | 3.6 | Figura 4 |
| Configuración evaluada: Tmin del bloque y contexto local; mínimo no determinado | 3.7 | Tabla 4 |
| TimesFM supera a `tuned` tal como fue diseñado; frente a `tuned_sin_td` la ventaja es menor | 3.7 | Tabla 5 |
| Sin zonificación, selección de recetas por zona y día ni ajuste de pesos locales | 3.3 | Tabla 1 |
| El costo pasa del entrenamiento a la inferencia; el total no favorece a TimesFM | 3.8 | Tabla 6 |
| `tuned` conviene con coeficientes ya existentes | 3.8 | Tabla 6 (predicción de producto) |
| Licencia no comercial como límite operativo | 3.3 | Tabla 1 (columna de licencia) |
| Sesgo de mayor magnitud en tres de cuatro casos | 3.5 | Tabla 3 |
| Acuerdo entre productos 2017–2020 no es exactitud | Suplemento S4 | `a4_contraste_externo.md` |

La última fila es la única afirmación de la discusión que se apoya en el suplemento; se admite porque la discusión solo la menciona como límite de alcance.

### 5.2 Criterios armonizados

Se adoptó el mismo reparto en `ORIENTACION_PAPER.md` e `historia_paper.md`: resumen de A2 en el cuerpo y detalle en S1; `ll4b` primero; selección única de TimesFM separada de inferencia y sumada una vez al total. Se informan en el cuerpo la inversión del orden en 2013 y el mayor sesgo absoluto de TimesFM en tres combinaciones. La atribución a la recursión queda como hipótesis no aislada; la ventaja con Td cruda se acota a los agregados de `ll4b`.

Se distinguen las 1.106 celdas predichas en el cribado de las 1.092 puntuadas en común con `tuned`. Se conservan como dos variantes `tmin_td_full` y `tmin_td_znorm`, pues métricas próximas no establecen igualdad de predicciones.

## 6. Alcance de la actualización

Se alinearon los documentos de esta carpeta. El artículo previo, `HANDOFF.md`, el código de experimentos y el artefacto externo a `paper_nuevo` no se actualizaron; no se los usa para reemplazar la orientación editorial vigente. Las referencias por comprobar y las limitaciones de evidencia se mantienen explícitas, sin presentar su comprobación como realizada.
