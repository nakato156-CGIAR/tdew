# Revisor 2 (climatología / datos), segunda ronda

Leí completos paper.pdf (27 págs.) y suplemento.pdf (19 págs.). Verifiqué contra `resultados/a1_por_zona.csv`, `r1_*`, `r2_*`, `r3_*`, el recuento de palabras de `secciones/*.qmd` y las marcas pendientes en el texto. No leí documentos editoriales ni informes de otros revisores.

## 1. Estado de cada comentario del primer informe

### Mayores

**M1 (circularidad: el "observado" es un producto interpolado). Parcialmente atendido.**
- Atendido: el alcance se reformuló. El resumen (p. 1) dice "se mide reproducción del producto, no exactitud atmosférica" y da el RMSE de 3,06 °C frente a ISD. La introducción (p. 2) y la Sección 2.1 (p. 3) repiten la salvedad, y la Sección 9 (p. 23) compara el tamaño de las brechas con el error del producto. El título cambió a "comparación con regresiones locales".
- No atendido: sigue sin cifra de cuántas estaciones de Td alimentan PISCO v1.1. El marcador [[FALTA: número de estaciones...]] sigue en p. 2. No hay estratificación por distancia a la estación PISCO más cercana. Esta se declara como análisis pendiente en la lista de la Sección 10 (p. 25).
- Falta además aclarar si PISCO v1.1 usó Tmin o covariables comunes con v1.2. Sin eso la circularidad se nombra pero no se acota.
- Residuo de redacción: el título de sección, la conclusión (p. 25) y varios párrafos siguen usando "reconstruyó Td" sin calificar.

**M2 (desajuste de versiones Tmin v1.1/v1.2 y degradación 2017–2020). No atendido.**
- La Sección 2.1 sigue sin comparar las versiones de Tmin ni analizar por qué la anomalía frente a estaciones empeora de 1,33 °C (2009–2016) a 1,63–1,68 °C (2017–2020). Esa cifra sigue solo en Tabla S7 (supl. p. 6).
- El chequeo favorable de continuidad de Tmin (`a4_tmin_celda_mes.csv`, r = 0,978 del ciclo anual por celda) sigue sin citarse.

**M3 (validación ISD débil y ubicada en el suplemento). Parcialmente atendido.**
- Atendido: hay una subsección 5.5 en el cuerpo (p. 12), con RMSE de 3,06 °C y sesgo +1,42 °C. La Discusión (p. 23) usa esa cifra como cota de lectura. El texto admite que la independencia de ISD respecto de PISCO no se pudo comprobar.
- No atendido: sigue sin tabla por estación, sin estratificación por régimen (costa, sierra, selva) y sin discusión del mecanismo. Los sesgos de +4 a +6 °C en Arequipa, Cusco y Andahuaylas y de signo contrario en Cajamarca y Ayacucho no aparecen. Tampoco la rotura de la relación Td–Tmin en zonas áridas o de altura, ni las limitaciones del sensor de aeropuerto a baja humedad relativa. No se incorporaron estaciones SENAMHI.

**M4 (representatividad y dominancia de una zona). Atendido en lo analítico, parcialmente en lo conceptual.**
- Atendido: la Sección 6.3.a y la Tabla S18 descomponen la brecha dentro y fuera de la zona A(r)A' (41,6 % de las celdas). Verifiqué con `a1_por_zona.csv` que aporta ~66 % del error cuadrático de TimesFM en 2009–2012 (0,659) y ~69 % en 2013–2016. Cuadra con el 65,9 % del texto. La Sección 6.4 y la Tabla S16 estratifican por altitud y por ámbito. El resumen reconoce que la diferencia "se concentra en Perú, en las bandas de mayor altitud y en la cola cálida".
- No atendido: el resumen y la conclusión siguen encabezando con la cifra del dominio completo (−0,076 y −0,074 °C). Perú no pasó a ser el análisis primario. No se explica qué territorio ocupan las 8.755 celdas fuera de Perú, y el texto mantiene que "no constituyen una región distinta" (p. 3). No hay mapa de brecha por celda. La banda 0–500 m (11.397 celdas) sigue mezclando Amazonía, costa y celdas extranjeras sin separar.

**M5 (años anómalos y ENSO). Parcialmente atendido.**
- Atendido: hay estratificación por fase ONI (Sección 6.6, Tabla S17) y por cola de anomalía (6.5, Tabla S14). El texto no atribuye causa y marca que La Niña 2013–2016 tiene un solo mes.
- No atendido: 2013 sigue sin causa ("No se identificó una causa", p. 14). No hay discusión física de 2015–2016 (El Niño extraordinario, anomalías costeras). Tampoco hay evaluación con más bloques ni rolling origin: la lista de "Quedan sin hacer" (p. 25) lo reconoce. El estrato ENSO está confundido con el bloque y el año, por lo que no aporta evidencia, como el propio texto admite.
- Hallazgo nuevo útil: todos los métodos subestiman la cola cálida (sesgo de −1,6 a −2,3 °C), y la ventaja de TimesFM es mayor allí (Tabla S14). Es relevante para humedad extrema, pero se deja sin interpretación climática.

**M6 (utilidad operativa: ET0, calibración). Parcialmente atendido.**
- Atendido: hay calibración de cuantiles (7.5, Tabla S15: 83,6 % y 81,0 % de cobertura para un 80 % nominal), habilidad frente a climatología y razón de varianzas (7.4, Tabla S13). La conclusión es más matizada: frente a las LLR sin zonas la diferencia es pequeña, y se nombra a `llr_rezagos_sel` como candidato (p. 23). Se midió el costo de las LLR seleccionadas (Tabla 7; 1 min 26 s frente a 122 min).
- No atendido: no se propaga el error de Td a ET0, que sigue como "sin hacer" (p. 25). No hay RMSE por percentil de Td ni por estación del año. Tampoco análisis del sesgo cambiante de TimesFM sobre series acumuladas.

**M7 (datos, licencia, reproducibilidad). Parcialmente atendido.**
- Atendido: hay sección "Disponibilidad de código y datos" (p. 26) y la licencia no comercial de TimesFM figura en el resumen. Se añadió la posible exposición de TimesFM a ERA5 en el preentrenamiento (Sección 3.3, p. 6, y 10).
- No atendido: siguen [[PENDIENTE: depósito de predicciones]] y [[PENDIENTE: licencia y condiciones de acceso de PISCO]], además de [[CITA]] y [[FALTA]] en la introducción y en 3.2. Hay 6 marcadores abiertos en el texto fuente. `tuned` sigue sin cita publicada y sin cifra de referencia de Palacios para 2009–2012. Las tablas de costo siguen con rutas `$WORK`/`$RES` no accesibles.

### Menores (numeración del primer informe)

| N.º | Tema | Estado | Evidencia |
|---|---|---|---|
| 1 | Distinguir "reproducción retrospectiva" de "relleno" | Parcial | El resumen y la 2.1 lo hacen, pero el cuerpo y la conclusión siguen diciendo "reconstruyó". La frase "carece de una serie observada" se mantiene (p. 2). |
| 2 | Mecanismo físico Td–Tmin y panel de la relación por zona | No atendido | Sigue la mención a Kimball y Eccel (p. 2) sin panel ni análisis. |
| 3 | Qué productos cubren las celdas fuera de Perú | No atendido | Figura 1 y Sección 2.2 sin cambios. |
| 4 | Lago Titicaca (agua) tratado aparte | No atendido | Sigue en la Figura 5 y en los agregados (256 celdas). |
| 5 | Figura 3 anual sin IC; no llevar a la Discusión | Atendido | Se aclara que es descriptiva y que no se corrige por comparaciones múltiples (pp. 9 y 14). La Figura 3 nueva (mensual, con banda de IC) la reemplaza parcialmente. |
| 6 | Figura 4 por zona: ordenar mejor / mapa | Parcial | Ahora es Figura 5 y se precisa que la brecha de una zona pequeña es la de sus celdas. No hay mapa por celda. |
| 7 | Zonas mixtas en vertientes | No atendido | |
| 8 | Habilidad y RMSE de anomalía | Atendido | Sección 7.4 y Tabla S13. |
| 9 | Centrar el titular en 2009–2012 | Atendido | El bloque 2009–2012 pasa a "confirmatorio" y el 2013–2016 a "exploratorio" (Sección 4.1). |
| 10 | Sesgo de muestra de ISD (criterio nocturno) | Parcial | Declarado en la Sección 10 (p. 25), pero no en 5.5 ni discutido. |
| 11 | IC subestiman incertidumbre espacio-temporal | Atendido | Cuatro esquemas de bootstrap (incluye espacio-tiempo y trimestre-año) y prueba de Diebold–Mariano con Holm (4.4, Tabla 4). |
| 12 | Rivales no validados por Palacios | No atendido | Sigue en el encabezado, en la Sección 3.4 y en los límites. |
| 13 | Frase de conclusión neta | Parcial | La conclusión (p. 25) sí distingue el rival y el bloque, pero es larga y no da una frase única. |

## 2. Problemas nuevos introducidos por la revisión

1. **Extensión y legibilidad.** El cuerpo suma unas 12.600 palabras en `secciones/*.qmd` (la coordinación estima 11.000 sin metadatos) y 27 páginas. El resumen pasó de 3 párrafos cortos a un bloque denso con siete afirmaciones cuantitativas. Para Environmental Data Science, GMD o IJC es excesivo para un efecto de 0,003 a 0,08 °C. Las Secciones 6 (≈2.000 palabras) y 4 (≈1.300) son las más largas. Se recomienda recortar el cuerpo a ~6.000–7.000 palabras.
2. **Dilución del mensaje.** Hay cuatro esquemas de bootstrap, dos reglas de rezago de Diebold–Mariano, Holm sobre 16 pruebas, cuatro rivales, dos bloques y dos ámbitos, y cuatro estratificaciones descriptivas (zona, altitud, cola, ENSO). El lector no distingue el resultado principal de la sensibilidad. La Tabla 4 de 16 filas con siete columnas es ilegible como cuerpo principal. Conviene pasarla al suplemento y dejar una figura de forest con los resultados clave.
3. **Doble lectura de las pruebas.** Varias condiciones aparecen con tres criterios distintos de "excluir cero" (espacial, espacio-tiempo, trimestre-año) más DM. Eso invita a elegir la lectura favorable. Debería fijarse una regla (por ejemplo, la prueba más conservadora) antes de reportar.
4. **Jerarquía confirmatorio/exploratorio sin registro previo.** El texto lo admite ("No hay registro previo del diseño", p. 7). Etiquetar un bloque como "confirmatorio" a posteriori es retórico. En la práctica solo la brecha frente a `tuned` en 2009–2012 es limpia, y eso debería decirse sin el adjetivo.
5. **Más estratificaciones descriptivas no sustituyen el análisis climático faltante.** Altitud, ENSO y cola cálida se calculan, pero sin interpretación física y con estratos desbalanceados (La Niña = 1 mes; 11.397 celdas en 0–500 m). Cada una abre preguntas que el texto rehúsa responder. Se agrega volumen sin cerrar M2, M3 ni M5.
6. **Nueva inconsistencia en el cuerpo.** El resumen dice que la ventaja frente a rivales sin recursión "se sostiene en 2009–2012" y a la vez que "TimesFM no mejora a `llr_rezagos_sel`" en la zona A(r)A'. Esa zona aporta ~66 % del error. La lectura global "se sostiene" depende de que se pondere por celdas y de que se acepte que en la zona dominante el efecto es nulo. Debe decirse explícitamente.
7. **Exposición a ERA5.** Se añade bien la advertencia (pp. 6 y 25). Pero es un argumento meramente especulativo (pesos de mezcla no listados) que ocupa un párrafo largo en límites. Se pide acortarlo y proponer un control concreto (p. ej., una serie sintética o una variable sin ERA5) o dejarlo en una frase.
8. **Marcas pendientes en un documento que va a revisores.** Las 6 marcas [[...]] abiertas y la portada "Borrador para revisión de Palacios y SENAMHI" son aceptables en el borrador, no en un envío. El `tuned` de 2009–2012 sigue sin reproducirse en el entorno de Palacios.
9. **Costo de LLR.** La nueva medición (Tabla 7) es una corrida única, en otra máquina y sin GPU. Los cocientes de 72 a 86 veces son llamativos pero se presentan con precisión de centésimas (71,94; 85,72). Redondear y advertir que no son controlados evitaría sobreinterpretación.

## 3. Recomendación actualizada

**Revisión mayor, ahora dirigida a una revista especializada (Environmental Data Science, GMD o IJC) y con recorte fuerte de longitud.** La revisión mejora la honestidad del encuadre (reproducción de PISCO, no Td real), la inferencia estadística (cuatro esquemas de bootstrap, DM, Holm) y la transparencia sobre la zona dominante y el costo de las LLR. El resultado central se sostiene: TimesFM mejora a `tuned` en 0,07–0,08 °C y es indistinguible de las LLR sin zonas en el caso más exigente.

Pero no se cerró lo que era propio de la dimensión climática. Faltan:
- el mecanismo físico de la relación Td–Tmin y su rotura en zonas áridas y de altura;
- la validación ISD por estación y régimen;
- la comparación de versiones de Tmin y la degradación 2017–2020;
- el análisis climático de 2013 y 2015–2016;
- una cifra de las estaciones que sustentan PISCO Td;
- los marcadores de datos, licencia y citas.

Con un cuerpo de ~6.500 palabras, la validación ISD por estación en el cuerpo y el Perú como análisis primario, sería publicable. Sin eso, la publicación sigue siendo prematura.

Nota de cumplimiento: este informe fue generado con apoyo de IA y debe validarse con expertos en la materia antes de usarse.
