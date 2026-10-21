# Síntesis de las amenazas A1-A4 para la Decisión 1

Fecha: 2026-10-20. Rama `tdew-214-real-2017-2020`, commit `010fd8a`. Este documento reúne los resultados de A1-A4 para aplicar la regla de la «Decisión 1» de `HANDOFF.md` §5, que elige entre dos narrativas para el paper nuevo:

- **E:** un modelo de fundación zero-shot sin diseño local iguala o supera a la regresión diseñada por zona.
- **C+A:** la covariable hace el trabajo, el diseño experto no mejora a un regresor simple y el protocolo de validación cambia la conclusión más que el estimador.

No se corrió ningún experimento nuevo. Las cifras se copiaron de `a1_desglose.md`, `a1_brechas.csv`, `a1_escalera_contexto.md`, `a4_contraste_externo.md`, `costo.md`, `experiments/llr_simple/resultados_ll4_ll4b.txt` y las notas de los beads. Las del control A3 salen de volver a ejecutar el script de evaluación sobre predicciones ya existentes (`uv run python -m experiments.timesfm.control_tmin_barajada_eval`). Los intervalos de `resultados_ll4_ll4b.txt` provienen de otro sorteo de bloques mes-año y difieren de los de `a1_brechas.csv` en la tercera cifra decimal; aquí se usan los de `a1_brechas.csv`.

Convenciones. Brecha = RMSE(A) − RMSE(B) en °C, pareada sobre las mismas 24.876.447 filas celda × día; negativo favorece a A. «Panel» son las 17.027 celdas del panel nacional; «Perú» son las 8.272 que caen dentro del país. `ll4` evalúa 2013-2016 con contexto hasta 2012; `ll4b` evalúa 2009-2012 con contexto hasta 2008. IC 95 % por bootstrap de 2.000 réplicas sobre bloques espaciales de 2° (74 en el panel, 45 en el Perú) o bloques mes-año (48).

## 1. Qué se hizo

| Etiqueta (bead) | Pregunta | Experimento | Resultado | Estado |
|---|---|---|---|---|
| A1 (`tdew-03g`) | ¿La ventaja de TimesFM se debe al El Niño 2015-2016 o al estimador? | Bloque `ll4b` (prueba 2009-2012) con climatología, `tuned`, dos LLR propios (con y sin selección interna de `h` y año de inicio) y TimesFM (`tmin_anom_full`, `tmin_td_full`, `tmin_anom_med`); desglose por Perú y zona; escalera de inicio del contexto en el panel de cribado; costo en la misma máquina | TimesFM `tmin_anom_full` tiene el RMSE más bajo en los dos bloques y ámbitos. Frente al LLR con rezagos seleccionado, empate en el panel de `ll4` (−0,003) y ventaja de 0,025-0,028 °C con IC sin cero en `ll4b` y en el Perú. `tmin_td_full` no supera al LLR simple en `ll4b` | resultados completos en `ll4` y `ll4b`; bead abierto (`IN_PROGRESS`) |
| A2 (`tdew-f6a`) | ¿Cuánto cuestan la autorregresión y el criterio de selección de `tuned`? | `tuned` con el pool sin rezagos de Td (`const`, `TMIN_anom` y sus rezagos), en `ll4` y `ll4b` | RMSE de 1,2279 a 1,1742 en `ll4` y de 1,1220 a 1,1082 en `ll4b`; sin rezagos de Td empata con el LLR simple | cerrado |
| A3 (`tdew-077`) | ¿La habilidad de TimesFM viene de la covariable? | TimesFM con la Tmin del bloque oculto barajada entre años (tres semillas) o entre celdas, panel de cribado de 1.092 celdas, `ll4` | Con barajado entre años el RMSE sube de 0,8389 a 1,506-1,551, peor que la climatología (1,2840); con barajado entre celdas queda en 1,2656 | cerrado |
| A4 (`tdew-ra6`) | ¿Qué exactitud tienen los productos 2017-2020 frente a Td atmosférico? | Contraste con 12-13 estaciones de aeropuerto ISD y con ERA5/ERA5-Land en puntos; chequeo de la Tmin regridada 2017-2020 | Los dos productos heredan el sesgo húmedo de PISCO (+1,4 °C); en anomalías TimesFM queda 0,046 °C por debajo de `tuned` (IC [−0,073; −0,019]); en Td no se distinguen | cerrado en puntos; el contraste grillado con ERA5 requiere credenciales |
| T1 (`tdew-kpp`) | ¿Se sostiene «sin conocer el país»? | — | — | abierto; se hace al final por decisión del usuario |

## 2. Escalera de métodos

RMSE en °C (`a1_desglose.md`). `tmin_td_full` solo se corrió en `ll4b`.

| método | `ll4` panel | `ll4` Perú | `ll4b` panel | `ll4b` Perú |
|---|---|---|---|---|
| climatología | 1,535 | 1,262 | 1,362 | 1,087 |
| `tuned` | 1,228 | 0,944 | 1,122 | 0,861 |
| `tuned` sin rezagos de Td | 1,174 | 0,908 | 1,108 | 0,856 |
| LLR simple | 1,175 | 0,912 | 1,098 | 0,849 |
| LLR simple seleccionado | 1,172 | 0,906 | 1,083 | 0,834 |
| LLR con rezagos | 1,161 | 0,897 | 1,089 | 0,844 |
| LLR con rezagos seleccionado | 1,157 | 0,891 | 1,074 | 0,830 |
| TimesFM en anomalías (`tmin_anom_full`) | 1,154 | 0,865 | 1,046 | 0,804 |
| TimesFM en Td cruda (`tmin_td_full`) | — | — | 1,106 | 0,840 |
| TimesFM en anomalías, contexto y climatología desde 2002 (`tmin_anom_med`) | 1,201 | 0,903 | 1,108 | 0,849 |

«Seleccionado» indica que el semiancho `h` (7 a 180) y el año de inicio del ajuste (1981 a 1996) se eligieron juntos por validación interna en los cuatro últimos años de entrenamiento, sin ver el bloque de prueba. Los cuatro LLR seleccionados eligieron el inicio 1991; `h` salió 60 y 45 en `ll4b` y 90 en `ll4`, sin tocar el borde de la grilla.

El sesgo de TimesFM `tmin_anom_full` cambia de signo entre bloques (+0,104 en `ll4`, −0,108 en `ll4b`, panel); el del LLR simple es negativo en ambos (−0,010 y −0,140). En el RMSE macro por zona del panel de `ll4`, TimesFM queda en 0,802 y el LLR con rezagos seleccionado en 0,840.

## 3. Brechas clave

Brecha y sus dos IC 95 % (`a1_brechas.csv`). Negativo favorece al primer método.

| A − B | ámbito | `ll4` brecha | `ll4` IC espacial 2° | `ll4` IC mes-año | `ll4b` brecha | `ll4b` IC espacial 2° | `ll4b` IC mes-año |
|---|---|---|---|---|---|---|---|
| TimesFM anom − `tuned` | panel | −0,074 | [−0,080; −0,069] | [−0,140; −0,015] | −0,076 | [−0,084; −0,068] | [−0,102; −0,050] |
| TimesFM anom − `tuned` | Perú | −0,079 | [−0,087; −0,071] | [−0,109; −0,052] | −0,056 | [−0,065; −0,049] | [−0,073; −0,040] |
| TimesFM anom − LLR simple | panel | −0,021 | [−0,031; −0,012] | [−0,053; +0,010] | −0,052 | [−0,057; −0,048] | [−0,073; −0,033] |
| TimesFM anom − LLR simple | Perú | −0,047 | [−0,058; −0,036] | [−0,063; −0,031] | −0,044 | [−0,050; −0,039] | [−0,057; −0,033] |
| TimesFM anom − LLR simple sel. | panel | −0,018 | [−0,027; −0,010] | [−0,045; +0,007] | −0,037 | [−0,041; −0,033] | [−0,052; −0,023] |
| TimesFM anom − LLR simple sel. | Perú | −0,041 | [−0,049; −0,033] | [−0,054; −0,029] | −0,030 | [−0,033; −0,026] | [−0,039; −0,021] |
| TimesFM anom − LLR rezagos sel. | panel | −0,003 | [−0,011; +0,004] | [−0,029; +0,021] | −0,028 | [−0,031; −0,026] | [−0,044; −0,013] |
| TimesFM anom − LLR rezagos sel. | Perú | −0,026 | [−0,033; −0,018] | [−0,038; −0,014] | −0,025 | [−0,028; −0,023] | [−0,034; −0,016] |
| TimesFM anom − `tuned` sin rezagos de Td | panel | −0,021 | [−0,029; −0,013] | [−0,056; +0,015] | −0,062 | [−0,068; −0,056] | [−0,084; −0,043] |
| TimesFM anom − `tuned` sin rezagos de Td | Perú | −0,043 | [−0,054; −0,033] | [−0,060; −0,027] | −0,052 | [−0,058; −0,045] | [−0,064; −0,040] |
| TimesFM td − LLR simple | panel | — | — | — | +0,007 | [−0,001; +0,015] | [−0,042; +0,059] |
| TimesFM td − LLR simple | Perú | — | — | — | −0,009 | [−0,020; +0,002] | [−0,037; +0,019] |
| `tuned` − LLR simple | panel | +0,053 | [+0,044; +0,062] | [+0,017; +0,097] | +0,024 | [+0,020; +0,027] | [+0,009; +0,039] |
| `tuned` − LLR simple | Perú | +0,032 | [+0,021; +0,043] | [+0,016; +0,050] | +0,012 | [+0,008; +0,016] | [+0,002; +0,024] |
| LLR rezagos sel. − LLR rezagos | panel | −0,004 | [−0,008; −0,002] | [−0,013; +0,004] | −0,015 | [−0,017; −0,012] | [−0,026; −0,004] |
| LLR rezagos sel. − LLR rezagos | Perú | −0,007 | [−0,013; −0,001] | [−0,011; −0,002] | −0,014 | [−0,019; −0,010] | [−0,022; −0,006] |

En todas las filas el IC mes-año es más ancho que el espacial. En tres casos el esquema decide si la brecha se distingue de cero: TimesFM anom frente al LLR simple, al LLR simple seleccionado y a `tuned` sin rezagos de Td en el panel de `ll4`. La brecha TimesFM td − LLR con rezagos seleccionado no se calculó con IC; en RMSE puntual TimesFM td queda por detrás (1,106 frente a 1,074 en el panel y 0,840 frente a 0,830 en el Perú).

Por zonas, TimesFM anom gana al LLR con rezagos seleccionado en 32 de 33 zonas del panel en `ll4` y en las 33 en `ll4b`; en el Perú gana en las 32 zonas en los dos bloques. TimesFM td gana al LLR con rezagos seleccionado en 20 de 33 zonas del panel en `ll4b` (`a1_victorias_zona.csv`).

## 4. Regla de la Decisión 1 aplicada de forma literal

La regla de `HANDOFF.md` §5 dice: «Si TimesFM sigue ganando en 2009-2012 y su brecha con el LLR simple se mantiene con intervalos que excluyan el cero por bloques mes-año: seguir con E como tesis. Si la brecha desaparece: paper C + A». Son dos condiciones:

- (1) TimesFM gana en 2009-2012 (`ll4b`).
- (2) Su brecha con el rival tiene IC por bloques mes-año que excluye el cero.

Se aplican frente al LLR simple, que es el rival que nombra la regla, y frente al LLR con rezagos seleccionado, que es el rival con entradas equiparables más fuerte.

La variante de referencia es `tmin_anom_full`, por decisión del usuario del 2026-10-20 (anotada en el bead `tdew-03g`). Es la equiparable en información con el LLR: recibe la Tmin en anomalía con la climatología de entrenamiento y tiene como objetivo la anomalía de Td. `tmin_td_full` recibe la Tmin cruda y queda como sensibilidad. `tmin_anom_full` se eligió entre nueve variantes en el cribado de `ll4` (bead `tdew-214.11.8`), así que `ll4b` es la evidencia fuera de muestra y `ll4` está expuesto a ese sesgo de selección. La regla no dice si (2) se evalúa solo en `ll4b` o en los dos bloques («se mantiene»); por eso la tabla muestra los dos.

| rival | ámbito | (1) gana en `ll4b` | (2) IC mes-año sin cero en `ll4b` | (2) IC mes-año sin cero en `ll4` |
|---|---|---|---|---|
| LLR simple | panel | sí (−0,052) | sí [−0,073; −0,033] | no [−0,053; +0,010] |
| LLR simple | Perú | sí (−0,044) | sí [−0,057; −0,033] | sí [−0,063; −0,031] |
| LLR con rezagos sel. | panel | sí (−0,028) | sí [−0,044; −0,013] | no [−0,029; +0,021] |
| LLR con rezagos sel. | Perú | sí (−0,025) | sí [−0,034; −0,016] | sí [−0,038; −0,014] |

`tmin_anom_full` también gana a `tuned` en `ll4b` en los dos ámbitos, con IC mes-año sin cero (sección 3).

Resultado de la regla:

- **Lectura sobre `ll4b`:** las dos condiciones se cumplen en el panel y en el Perú, frente a los dos rivales. La regla indica E.
- **Lectura que exige los dos bloques:** se cumple en el Perú frente a los dos rivales y falla en el panel frente a los dos, porque en `ll4` el IC mes-año incluye el cero (frente al LLR con rezagos seleccionado la brecha puntual es −0,003). La regla da E en el Perú y C+A en el panel.

**Sensibilidad con `tmin_td_full` (solo `ll4b`).** Frente al LLR simple, la brecha es +0,007 °C en el panel (IC mes-año [−0,042; +0,059]) y −0,009 °C en el Perú ([−0,037; +0,019]); ninguno excluye el cero. Frente al LLR con rezagos seleccionado pierde en RMSE puntual (1,106 frente a 1,074 en el panel y 0,840 frente a 0,830 en el Perú), sin IC calculado. A `tuned` le gana en RMSE puntual (1,106 frente a 1,122 y 0,840 frente a 0,861). Si se aplicara la regla a esta variante, indicaría C+A. La ventaja de TimesFM sobre los LLR depende, por tanto, de que la covariable y el objetivo entren en anomalía.

### Dos lecturas posibles

**E: TimesFM zero-shot iguala o supera a la regresión diseñada.**

A favor:
- `tmin_anom_full` tiene el RMSE más bajo de la escalera en los dos bloques y ámbitos, y gana a `tuned` por 0,056 a 0,079 °C con IC sin cero en todos los casos.
- `ll4b` no participó en la elección de la variante, y es donde la ventaja es más clara.
- La ventaja frente al rival más fuerte se mantiene con IC sin cero en tres de las cuatro combinaciones bloque × ámbito, y por zonas TimesFM gana en 32 o 33 de 33.
- En la escalera de contexto, TimesFM queda por delante de los dos LLR en todos los inicios y en los dos bloques, con IC que excluyen el cero.
- Frente a las estaciones, en anomalías TimesFM tiene 0,046 °C menos de RMSE que `tuned` (IC [−0,073; −0,019]).

En contra:
- Frente al LLR con rezagos seleccionado la ventaja es de 0,025 a 0,028 °C, y en el panel de `ll4` es −0,003 con los dos IC incluyendo el cero.
- En la sensibilidad con Tmin y objetivo crudos (`tmin_td_full`), TimesFM no supera al LLR simple en `ll4b`.
- La variante ganadora necesita una climatología desde 1981 para formar las anomalías (sección 5) y se eligió entre nueve configuraciones, lo que también es una decisión de diseño.
- Sin T1, «sin diseño local» y «sin conocer el país» solo se han probado dentro de PISCO y del Perú.

**C+A: la covariable hace el trabajo y el protocolo pesa más que el estimador.**

A favor:
- Con la Tmin barajada entre años TimesFM queda peor que la climatología.
- La distancia climatología − LLR simple (+0,263 °C en `ll4b` y +0,360 °C en `ll4`, panel, `resultados_ll4_ll4b.txt`) es mucho mayor que la que separa al LLR simple de TimesFM anom (0,052 y 0,021 °C).
- El diseño experto no mejora a un regresor simple: `tuned` queda por detrás del LLR simple en los dos bloques y ámbitos con IC sin cero, y sin rezagos de Td empata con él.
- Varias decisiones de protocolo cambian la conclusión o mueven más que la diferencia entre estimadores:
  - el esquema de IC decide la significación en el panel de `ll4`;
  - el ámbito (panel frente a Perú) cambia el resultado de `ll4`;
  - la ventana de la climatología explica la brecha de 0,044-0,062 °C entre `tmin_anom_med` y `tmin_anom_full`;
  - sintonizar al rival reduce la brecha en 0,003-0,015 °C;
  - la validación contra el Td grillado mide la reproducción de PISCO, no el Td atmosférico (A4).

En contra:
- `tmin_anom_full` conserva una brecha con IC mes-año sin cero frente al rival más fuerte en `ll4b` y en el Perú.
- La regla, en su lectura sobre `ll4b`, no indica «la brecha desaparece» para esa variante.
- «El protocolo cambia la conclusión más que el estimador» no se ha cuantificado como contraste formal; las magnitudes anteriores son comparaciones de órdenes de tamaño.

## 5. Hallazgos colaterales que el paper debería reportar

**Quitar los rezagos de Td mejora a `tuned`.** La brecha `tuned` − `tuned` sin rezagos de Td es:

- `ll4`, panel: +0,054 °C (IC espacial [+0,046; +0,061], mes-año [+0,019; +0,096]);
- `ll4b`, panel: +0,014 °C (espacial [+0,011; +0,017], mes-año [−0,000; +0,027]);
- Perú: +0,036 °C en `ll4` (mes-año [+0,019; +0,057]) y +0,005 °C en `ll4b` (mes-año [−0,005; +0,014]).

La versión sin rezagos gana a `tuned` en 32 de 33 zonas en `ll4` y en 30 de 33 en `ll4b` (panel). El efecto es mayor en el bloque con El Niño 2015-2016. Esto es consistente con que la recursión sobre Td predicho dentro del bloque cause la mayor parte de la desventaja de `tuned`. `HANDOFF.md` §5 (A2) ya señalaba un posible mecanismo: la selección puntúa con coseno sin centrar y a un paso, y el despliegue es autorregresivo y se puntúa con RMSE.

**El LLR simple empata con `tuned` sin rezagos de Td o lo supera.** La brecha `tuned` sin rezagos − LLR simple es:

- `ll4`: −0,001 °C en el panel (espacial [−0,003; +0,002], mes-año [−0,012; +0,011]) y −0,004 °C en el Perú (mes-año [−0,011; +0,003]);
- `ll4b`: +0,010 °C en el panel (espacial [+0,007; +0,012], mes-año [−0,003; +0,022]) y +0,007 °C en el Perú (mes-año [−0,000; +0,015]).

Con el IC espacial, el LLR simple gana en `ll4b`; con el mes-año, empatan. El LLR con rezagos de Tmin queda por delante de `tuned` sin rezagos en 33 y 32 de 33 zonas. Las recetas por zona × día del año, el shapefile de 41 zonas y la búsqueda de `h` por zona no producen una mejora medible sobre un LLR con un solo `h` global.

**La brecha entre contexto completo y contexto corto se debía a la climatología.** La escalera se corrió sobre 1.092 celdas del panel de cribado con la climatología fija en 1981-train_end. Pasar el inicio del contexto de TimesFM de 1981 a 2002 costó +0,002 °C en `ll4b` (IC mes-año [−0,005; +0,009]) y +0,005 °C en `ll4` ([+0,002; +0,008]). Con el contexto desde 2002, recortar además la climatología costó:

- `ll4b`: +0,044 °C (IC [+0,035; +0,053]), casi toda la diferencia;
- `ll4`: +0,022 °C (IC [+0,015; +0,029]), unas cuatro quintas partes.

Los LLR mejoraron al descartar 1981-1990: entre 0,017 y 0,024 °C con inicio en 1991 o 1996. Con esa mejora la ventaja de TimesFM sobre el LLR con rezagos baja de 0,047 a 0,027 °C en `ll4b` y de 0,055 a 0,030 °C en `ll4`, y sigue con IC que excluyen el cero en todos los inicios.

**La Tmin barajada colapsa.** Panel de cribado, `ll4`, 1.092 celdas y 1.595.412 filas:

| corrida | RMSE | skill frente a climatología | sesgo |
|---|---|---|---|
| climatología | 1,2840 | +0,000 | −0,166 |
| `tuned` | 0,9326 | +0,274 | +0,089 |
| TimesFM td, Tmin real | 0,8718 | +0,321 | +0,124 |
| TimesFM anom, Tmin real | 0,8389 | +0,347 | +0,065 |
| TimesFM td, barajado entre años, semilla 0 | 1,5079 | −0,174 | −0,176 |
| TimesFM anom, barajado entre años, semilla 0 | 1,5091 | −0,175 | −0,224 |
| TimesFM anom, barajado entre años, semilla 1 | 1,5062 | −0,173 | −0,281 |
| TimesFM anom, barajado entre años, semilla 2 | 1,5509 | −0,208 | −0,156 |
| TimesFM anom, barajado entre celdas | 1,2656 | +0,014 | +0,079 |

Con la Tmin de otro año TimesFM queda peor que la climatología en las tres semillas. Con la Tmin de otra celda, que conserva la señal temporal común entre celdas, queda a la altura de la climatología. Los resultados son consistentes con que la habilidad provenga de la covariable y no de estructura de Td en el contexto.

**Frente a las estaciones, los dos productos heredan el sesgo húmedo de PISCO.**

- En 2009-2016 PISCO tiene sesgo de Td +1,42 °C y RMSE 3,06 °C frente a 13 aeropuertos ISD (Arequipa +5,91, Cusco +3,97, Andahuaylas +4,24).
- En 2017-2020, `tuned` y TimesFM tienen sesgo +1,38 y +1,48 °C y repiten el patrón por estación (Arequipa +4,95 y +5,03).
- ERA5-Land, en los mismos días, tiene sesgo +0,06 °C en 2009-2016 y +0,14 °C en 2017-2020.
- En anomalías, el cociente de RMSE frente a ERA5-Land es 1,10 para PISCO en 2009-2016 y 1,11 (`tuned`) y 1,08 (TimesFM) en 2017-2020.

El RMSE de ≈1,15-1,23 °C del backtest mide cuánto reproducen los productos el Td grillado, no cuánto se acercan al Td atmosférico. El chequeo de la Tmin regridada 2017-2020 no encontró cambios de nivel ni de distribución frente a 2013-2016 (r = 0,9991 en medias celda-mes). Queda abierta la mayor dispersión del salto de enero de 2017 (desviación 1,33 frente a 0,66-0,90).

## 6. Limitaciones y salvedades

- **Intervalos.** Un subagente hizo una revisión independiente del código en la sesión del 2026-10-20. No encontró fugas ni errores de alineación. Sus hallazgos fueron la climatología recortada en `tmin_anom_med` (ya corregida con la escalera), el docstring de `shuffle_tmin` (corregido), la rejilla de `h` asimétrica y los IC posiblemente optimistas. Esa revisión señaló que los IC pueden ser optimistas y que los bloques espaciales de 2° no capturan forzantes comunes a todo el dominio, como ENSO. El bloque espacial no recoge la dependencia temporal y el mes-año no recoge la espacial; ninguno cubre ambas (`a1_desglose.md`). El esquema mes-año tiene solo 48 bloques. Se tomó el IC mes-año como lectura prudente, como pide la regla, pero ni siquiera ese está libre de esta salvedad.
- **Grillas de `h` distintas.** `tuned` busca `h` en 7-45 por zona × día del año (`costo.md`); los LLR sin selección usan 7 valores entre 7 y 60, y los seleccionados llegan hasta 180 y eligieron 45, 60 y 90. La comparación entre `tuned` y los LLR seleccionados no se hizo con el mismo espacio de búsqueda de `h`.
- **Entorno de `tuned`.** El `tuned` de `ll4b` y el `tuned` sin rezagos de Td (A2) se corrieron con el código del repositorio, no con el entorno de Palacios (nota del bead `tdew-03g`). En `ll4` la reproducción dio 1,2279, igual a la cifra limpia de referencia.
- **Barajado por celda.** El modo `cell` es determinista: desplaza la anomalía de Tmin la mitad de las celdas del lote (`np.roll` en `experiments/timesfm/panel.py`), sin usar la semilla, y depende de la composición del lote. Hay una sola realización, en `ll4` y solo para `tmin_anom_full`. El modo `year` tiene tres semillas, solo en `ll4`.
- **Insumos compartidos.** Td y Tmin de PISCO comparten insumos de LST de MODIS (Huerta et al. 2022, tabla 1; 2023; nota en el bead `tdew-ra6`). Palacios indicó que Tmin no es insumo directo de Td, pero ambos usan LST de MODIS. Un corte temporal no elimina ese error correlado, y parte de la habilidad compartida de todos los métodos frente al Td grillado puede deberse a él.
- **Estaciones ISD.** No se sabe si los 13 aeropuertos ISD son independientes de las 182 estaciones SENAMHI de PISCO Td v1.1; no hay una lista pública para comprobarlo. Si alguno entró en PISCO, el error de PISCO en 2009-2016 está subestimado en esa estación. La muestra es pequeña y sesgada: solo aeropuertos, ninguno en el altiplano con el criterio principal, y un salto aparente en Ayacucho en 2019.
- **Ámbito.** El 51,4 % del panel (8.755 de 17.027 celdas) cae fuera del Perú (bead `tdew-214.8`), y el panel agregado no es un promedio del país. Esas celdas son el mismo producto PISCO y no cuentan como transferencia. El resultado de `ll4` cambia entre panel y Perú, y con un solo bloque por período no se puede separar si eso es propio de 2013 o de la región fuera del país.
- **Variante de TimesFM.** `tmin_anom_full` es la variante de referencia por decisión del usuario, pero se eligió entre nueve en el cribado de `ll4` (bead `tdew-214.11.8`). Las cifras de `ll4` para esa variante están expuestas a ese sesgo de selección; `ll4b` no.
- **Rivales propios.** Los LLR y `tuned` sin rezagos de Td son variantes construidas en este proyecto que Palacios no ha revisado.
- **Costo.** `costo.md` tiene varias salvedades:
  - Los tiempos de los LLR se midieron con la grilla anterior de 7 valores de `h` e inicio fijo, no con la selección conjunta de 10 valores de `h` × 4 inicios de los LLR seleccionados.
  - En paralelo corría otro agente con carga de unos 3 núcleos.
  - El comando de TimesFM en `ll4b` no quedó registrado, y su ritmo (3,9 celdas/s) es menor que el de la pasada de escala (5,09) sin causa identificada.
  - Los 49 min de selección entre nueve variantes de TimesFM se hicieron sobre el bloque de evaluación.
  - No queda probado que las corridas de Palacios usaran la misma tarjeta.
  - El `tuned` sin rezagos de Td no figura en la tabla de costo.
  - El esfuerzo de diseño se describe de forma cualitativa, sin horas-persona.

## 7. Preguntas abiertas y lo que falta

Para Palacios:

1. Si «se mantiene» exige los dos bloques o solo `ll4b`. Con `tmin_anom_full`, el resultado de la regla en el panel depende de esta respuesta (sección 4).
2. Revisión de los LLR propios (`experiments/llr_simple/llr.py`, `llr_lags.py`) y de `tuned` sin rezagos de Td antes de tratarlos como rivales oficiales.
3. Si el `tuned` de `ll4b` y el de A2, corridos con el código del repositorio, se reproducen en su entorno.
4. Si la grilla de `h` de 7-45 en `tuned` es una decisión de diseño o una restricción de cómputo, y si se justifica ampliarla para igualar la de los LLR.
5. Si hay forma de saber qué estaciones SENAMHI entraron en PISCO Td v1.1, para confirmar la independencia de los aeropuertos ISD.
6. Qué componentes del pipeline y qué horas-persona de diseño se pueden documentar para la comparación de costo (`HANDOFF.md` §6, pregunta 3).
7. Acuerdo sobre el cambio de historia del paper (`HANDOFF.md` §6, pregunta 4).

Lo que falta:

- Calcular la brecha `tmin_td_full` − LLR con rezagos seleccionado con sus dos IC. Hoy solo hay RMSE puntual.
- Un esquema de IC que recoja a la vez la dependencia espacial y la temporal, o al menos una comprobación de cobertura de los dos esquemas actuales.
- El barajado por celda con otras asignaciones de donante, y el control A3 en `ll4b`.
- El contraste grillado con ERA5-Land en todo el Perú, que requiere una clave de Copernicus CDS, una cuenta de Google Earth Engine o lectura del bucket `s3://nsf-ncar-era5`.
- Medir el costo de los LLR seleccionados y de `tuned` sin rezagos de Td en la misma máquina.
- Cerrar el bead `tdew-03g` y actualizar su fila del Gantt en Notion.
- T1 (`tdew-kpp`) queda fuera de alcance de esta síntesis. Se hace al final, según la decisión del usuario. El candidato anotado en el bead es ERA5-Land en India, con un control dentro del Perú con ERA5-Land y estaciones HadISD.

---

Este documento se preparó con asistencia de IA generativa (Claude), que reunió y copió cifras de los reportes y CSV del repositorio. Antes de usarlo en el paper, debe validarse con Palacios y SENAMHI, en especial la lectura de la regla y los rivales construidos en este proyecto. El paper debe declarar el uso de IA generativa.
