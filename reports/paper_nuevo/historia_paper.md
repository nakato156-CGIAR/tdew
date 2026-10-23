# Historia y evidencia del paper nuevo

Guía consolidada el 21 de octubre de 2026. Se desarrolla la orientación de `ORIENTACION_PAPER.md`; `paper_narrative.md` organiza las mismas decisiones en secciones del artículo. Se conserva la tesis E acotada y se retira la regla E/C+A. El registro de la revisión documental está en `REVISION_COHERENCIA.md`. No se modifican `reports/paper/` ni `PAPER_PLAN.md`.

## Pregunta y tesis

Se compara cuánto cambia el error y qué preparación y cómputo requiere reconstruir Td diaria con TimesFM sin ajuste de pesos locales frente al método `tuned` de Palacios, con los mismos productos y transformaciones de PISCO.

La tesis queda acotada a los dos bloques y ámbitos evaluados: TimesFM obtuvo menor RMSE agregado que `tuned`, sin seleccionar recetas por unidad cartográfica y día del año ni ajustar coeficientes locales. Se usó un checkpoint preentrenado y se eligió una configuración entre nueve. La comparación con LLR locales sin zonas reduce la ventaja; no se atribuye la diferencia al valor del conocimiento experto ni a un componente aislado.

El problema se presenta siguiendo el antecedente de Palacios: el registro de Td termina en 2016 y el de Tmin continúa hasta 2020. Primero se describe ese vacío y los datos disponibles; después, métodos, evaluación, resultados y límites. Las etiquetas E/C+A y los identificadores de sesiones son contexto editorial, no contenido del artículo.

## Comparabilidad y dominio

Se comparten Td PISCO v1.1, Tmin PISCO v1.2, grilla de 0,01°, celdas y fechas puntuadas, climatologías de entrenamiento y vuelta a °C. Las diferencias de historial usado, rezagos, selección y ajuste forman parte de cada método; las variantes de sensibilidad que cambian climatología se identifican por separado.

TimesFM de referencia es `tmin_anom_full`: recibe anomalías locales de Td y Tmin, contexto desde 1981 y Tmin observada de todo el bloque reconstruido, sin modificar sus pesos. Se distingue la selección de configuración del ajuste de pesos. Se reconstruye con una covariable observada; no se evalúa un pronóstico meteorológico sin Tmin del bloque.

Se presenta primero `ll4b` (contexto hasta 2008; prueba 2009–2012), que no participó en la elección de configuración. `ll4` (contexto hasta 2012; prueba 2013–2016) coincide con el bloque del cribado y se informa con esa salvedad. Ambos son retrospectivos y del mismo producto; `ll4b` no constituye una prueba de transferencia.

El panel contiene 17.027 celdas puntuadas, de las cuales 8.272 centros están dentro del contorno político de Perú y 8.755 fuera. Se informan Perú y dominio completo por separado. El artículo previo usa un ámbito clasificado por el mapa; esa máscara no se intercambia con el contorno político usado aquí. Las 17.041 celdas predichas en TimesFM incluyen 14 no puntuadas; en el cribado se predijeron 1.106 y se puntuaron 1.092 comunes con la referencia limpia.

Según la descripción del artículo previo (`reports/paper/paper_taac.qmd`, sección «Data»), SENAMHI distingue 38 tipos climáticos y tres unidades adicionales, dos lagos y lomas costeras: 41 unidades cartográficas. Se usa «zona» como nombre operativo de esas unidades, no como sinónimo de 41 tipos climáticos. En el panel hay 33 unidades y en Perú 32.

## Orden del argumento y mapa de evidencia

Se presentan datos y preparación, métodos, protocolo, resultados agregados, variación anual y zonal, sensibilidades, costo y discusión de uso. El resumen de A2 entra en el cuerpo y su detalle en el suplemento. Las recomendaciones se apoyan en resultados ya presentados.

| Afirmación | Fuente | Destino |
|---|---|---|
| Menor RMSE agregado de TimesFM frente a `tuned` en los dos bloques y ámbitos | `resultados/a1_por_metodo.csv`, `resultados/a1_brechas.csv` | Cuerpo |
| Menor diferencia frente al LLR con rezagos seleccionado; IC con cero en dominio completo de `ll4` | `resultados/a1_brechas.csv` | Cuerpo |
| MAE y sesgo también condicionan la lectura | `resultados/a1_por_metodo.csv` | Cuerpo |
| El orden frente a `tuned` se invierte en 2013 en dominio completo; cambia la magnitud por zona | `resultados/a1_por_metodo.csv`, `resultados/a1_por_zona.csv` | Cuerpo |
| Preparación y cómputo distintos por método | `resultados/costo.md`, `resultados/costo.csv` | Cuerpo |
| Seis de nueve variantes tienen menor RMSE que `tuned` en el cribado observado | `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv` | Cuerpo |
| Td cruda también obtiene menor RMSE agregado que `tuned` en `ll4b`, con margen menor | `resultados/a1_por_metodo.csv` | Cuerpo; detalle frente a los LLR en suplemento |
| La variante `tuned_sin_td` reduce más el RMSE en `ll4` que en `ll4b`; no se aisló una causa | `resultados/a1_por_metodo.csv`, `resultados/a1_brechas.csv` | Resumen en cuerpo; detalle A2 en suplemento |
| Sensibilidad al inicio del historial y de la climatología; sin mínimo de contexto determinado | `resultados/a1_escalera_contexto.md` y sus CSV | Suplemento |
| Sensibilidad a Tmin alineada; aporte marginal de Td histórica sin aislar | `resultados/a3_control_tmin_barajada.csv` | Suplemento |
| Contraste ISD limitado y acuerdo entre productos 2017–2020 | `resultados/a4_contraste_externo.md` y CSV de productos y estaciones | Suplemento |
| Otras variantes LLR, conteos zonales y detalle de corridas | `resultados/a1_por_metodo.csv`, `resultados/a1_victorias_zona.csv`, `resultados/costo.csv` | Suplemento |

Las cifras proceden de los CSV; los documentos narrativos no sustituyen esas fuentes. La sección «Paper» del artefacto fuera de esta carpeta no se actualizó en esta corrección y no fija las decisiones editoriales vigentes.

## Resultados y lectura estadística

TimesFM tiene menor RMSE agregado que `tuned` en ambos bloques y ámbitos; los dos esquemas de IC de esas brechas excluyen cero. Frente a `llr_rezagos_sel`, los márgenes son menores y ambos intervalos contienen cero en el dominio completo de `ll4`. Se informa la brecha, sin concluir empate o equivalencia.

El sesgo absoluto de TimesFM es mayor que el de `tuned` en tres casos: Perú en ambos bloques y dominio completo en `ll4`. En dominio completo de `ll4b` es menor. En 2013 el RMSE de TimesFM es mayor que el de `tuned` en dominio completo; dentro de Perú la brecha anual permanece favorable a TimesFM. No se atribuye esta variación a ENSO ni a un mecanismo de producto.

Los IC usan 2.000 réplicas de bootstrap pareado por bloques espaciales de 2° o por mes-año. El espacial conserva las series completas dentro de cada bloque y rompe dependencia entre bloques; el mensual conserva todas las celdas y días del mes y rompe dependencia entre meses. Se presentan ambos como sensibilidades. Ninguno representa toda la dependencia espacial y temporal conjuntamente. Las brechas anuales y zonales son descriptivas, sin IC propios.

## Costo por etapa

| Escala y etapa | `tuned` | TimesFM `tmin_anom_full` |
|---|---|---|
| Selección de recetas en `ll4b` | 52 min 38 s, 5.506 celdas | no aplica |
| Ajuste + predicción / inferencia en `ll4b` | 5 min 50 s, 17.027 celdas | 73 min 10 s, 17.041 predichas; 17.027 puntuadas |
| Cribado único de configuración, realizado en `ll4` | no aplica | 49 min 8 s, 1.106 celdas × 9 variantes |
| Total de selección y reconstrucción, cargando una vez el cribado | 58 min 28 s | 122 min 18 s |
| Selección y ajuste para producto, 1981–2016 | 32 h 41 min + 6 h 45 min | sin ajuste local de pesos |
| Inferencia de producto 2017–2020, 2.178.827 celdas | 19 min 40 s | ≈5,1 días |

Fuentes: `resultados/costo.csv` y `resultados/costo.md`. El total que incluye cribado es ≈2,09 veces el de `tuned` en las corridas documentadas de evaluación; el cribado se reutiliza y no se cobra otra vez por bloque. La inferencia sola de TimesFM es ≈73 min, no su total con selección. No se midió el preentrenamiento del checkpoint.

La misma estación se usó para las corridas de `ll4b`, aunque hubo carga de CPU concurrente durante parte de la selección. Las corridas de producto no constituyen una comparación controlada: no consta el host de Palacios y TimesFM compartió GPU en algunos tramos. El preprocesamiento compartido no tiene cronometraje completo; los tiempos de los LLR seleccionados no se midieron y no se sustituyen por los de versiones anteriores. No se midieron horas humanas de diseño.

El inventario de preparación distingue `tuned` —mapa, selección de predictores y ventana por zona y día, ajuste por celda— de TimesFM —checkpoint, historial local, climatologías, Tmin del bloque y elección única de configuración—. No se afirma que desaparezca todo diseño ni que TimesFM reduzca el cómputo total.

## Sensibilidades y condiciones de uso

En el cribado limpio de 1.092 celdas y 2013–2016, seis de nueve variantes tienen menor RMSE que `tuned`. Las dos variantes univariadas y la variante cruda de dos años no lo superan. Esto describe el cribado observado; no garantiza independencia de configuración ni determina el mínimo de contexto de `tmin_anom_full`. `tmin_td_full` y `tmin_td_znorm` tienen métricas casi iguales, pero no se comprobó la igualdad de sus predicciones; se mantienen como dos variantes.

Con climatología fija desde 1981, recortar el contexto hasta 2002 cambia el RMSE +0,002 °C en `ll4b` y +0,005 °C en `ll4` en el panel de cribado. Cambiar además la climatología tiene un efecto mayor. La escalera no identifica un quiebre en 2000 ni una necesidad general de historial largo.

La reducción del RMSE de `tuned_sin_td` es 0,054 °C en dominio completo de `ll4` y 0,014 °C en `ll4b`. Se cambian el pool y la selección resultante de recetas y ventanas; no se aisló la recursión como causa. La ventaja frente a `tuned` con Td cruda en `ll4b` es pequeña, se invierte en 2009 y no se extiende a una superioridad frente a los LLR seleccionados.

TimesFM puede convenir cuando están disponibles los insumos de la configuración evaluada y se acepta su tiempo de inferencia; `tuned`, cuando ya existen coeficientes y se prioriza la inferencia rápida observada. Los LLR sin zonas son controles competitivos de costo seleccionado no medido. La licencia no comercial registrada para los pesos requiere comprobación antes de recomendar un uso operativo.

## Interpretaciones retiradas

| Interpretación | Lectura vigente |
|---|---|
| Elegir E o C+A según un IC | Se conserva E acotada y se valoran magnitudes, preparación y costo |
| Todo LLR requiere zonificación | La zonificación es una adaptación específica de `tuned` |
| El diseño experto no aporta o la recursión explica la diferencia | No se aisló la contribución de esos componentes |
| TimesFM recibe solo Tmin o no necesita preparación | Usa historial de Td y Tmin, climatologías y configuración seleccionada |
| Sin entrenamiento de ningún tipo | Sin ajuste de pesos locales; se usa un checkpoint preentrenado |
| Contexto desde 2002 controla un cambio MODIS en 2000 | Es sensibilidad al inicio del historial y de la climatología |
| El barajado demuestra inutilidad de Td histórica | Solo muestra sensibilidad a la covariable alineada |
| IC con cero demuestra empate | No se distinguió el signo de la diferencia con ese análisis |
| RMSE próximos demuestran predicciones idénticas | La igualdad requiere comparar las salidas pareadas |
| El cribado demuestra un historial largo mínimo | El mínimo no se determinó; la escalera distingue contexto y climatología |
| Dominio completo equivale a Perú o prueba transferencia | Se separan ámbitos dentro del mismo producto |
| A4 es validación independiente plena | Es contraste limitado con independencia espacial sin verificar |
| Comparar productos con ERA5 como escala | Fuera del artículo; se conservan únicamente los CSV históricos |

## Límites y referencias

No se probaron desempeño sin Td histórica, Tmin ausente o con error sistemático, aporte marginal de Td en TimesFM, ni transferencia a otro producto. Tampoco se determinó el contexto mínimo o un costo homogéneo con horas humanas. Los rivales LLR y A2 requieren revisión científica; `tuned` de `ll4b` se corrió con el código del repositorio. Las grillas de ventana difieren: 7–45 para `tuned`, hasta 180 para los LLR seleccionados.

En A4 hay 12–13 estaciones de aeropuerto y no se verificó su posible participación en PISCO. La ausencia de solapamiento temporal del objetivo en 2017–2020 no demuestra independencia espacial. Se distingue reproducir Td grillada de aproximar Td atmosférica y acuerdo entre productos de exactitud.

Las referencias bibliográficas de los insumos espaciales compartidos, incluido el detalle de MODIS y la referencia Huerta 2023, no se verificaron en texto completo en esta revisión. Se mantienen como asuntos bibliográficos por comprobar, sin usarlas para explicar un mecanismo. La clave `huerta2022` existe en la bibliografía del artículo previo; eso no verifica por sí solo cada afirmación nueva.

Se usó asistencia de IA generativa (Claude en la preparación inicial y Codex en la revisión). El contenido científico debe revisarse con Palacios y SENAMHI antes de trasladarlo a los `.qmd`; el artículo debe declarar esa asistencia.
