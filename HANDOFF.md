# Handoff: reorientación del paper (LLR frente a TimesFM)

Fecha: 2026-10-20. Rama: `tdew-214-real-2017-2020`. Este documento reúne el contexto para planificar y ejecutar, en una sesión nueva, el cierre de las amenazas a la validez y la prueba de transferencia que decidirán la narrativa del paper nuevo. No se abrieron beads, no se editó código ni se hizo commit.

Contenido generado con asistencia de IA (Claude). Debe validarse con especialistas (Palacios, SENAMHI) antes de citarse, y el paper nuevo debe declarar el uso de IA generativa. Las cifras con marca «(derivado)» o «(subagente)» no figuran en ningún reporte del repositorio y deben recalcularse antes de citarlas.

> **Decisión del 2026-10-20:** el paper vigente (`reports/paper/`) y `PAPER_PLAN.md` no se modifican. El paper nuevo se escribe en `reports/paper_nuevo/` (carpeta propia con todos los `.qmd`). Beads: A1 `tdew-03g`, A2 `tdew-f6a`, A3 `tdew-077`, A4 `tdew-ra6`, T1 `tdew-kpp` (T1 al final). Respuesta de Palacios sobre Tmin y Td: Tmin no es insumo directo de Td, pero ambos usan LST de MODIS; ver nota en `tdew-ra6`.

## 1. Tareas que cubre este handoff

Se usan las etiquetas A1–A4 y T1 para no chocar con los E1–E12 ya usados en los PLAN_n.

| Etiqueta | Qué cierra | Costo estimado |
|---|---|---|
| A1 | Segundo bloque de evaluación sin El Niño dominante (2009-2012) con TimesFM, LLR simple, climatología y `tuned` | ≈56 min de GPU para TimesFM; segundos para LLR simple y climatología; una corrida GPU de selección y backtest de Palacios para `tuned` |
| A2 | `tuned` sin rezagos de Td (pool de candidatas sin autorregresión) | una corrida GPU de `select_backtest` y `backtest` solo en `ll4` |
| A3 | Control negativo con Tmin barajada | ≈5,5 min en el panel de cribado |
| A4 | Contraste con ERA5-Land o estaciones SENAMHI en 2017-2020 | por definir según acceso a los datos |
| T1 | Prueba de transferencia a otra región o producto con los mismos ajustes | depende de encontrar datos con Td y Tmin; es la tarea de mayor riesgo |

## 2. Punto de partida

### Paper actual (método de Palacios)

- Versión vigente: `reports/paper/paper.qmd` (954 líneas). `paper_taac.qmd` es su derivación para revista y `paper_taac_esm.qmd` su suplemento. `PAPER_PLAN.md` está desfasado (última actualización de contenido el 2026-09-14) y es de Palacios: no se edita ni se añaden entradas.
- Tesis: el mapeo Tmin→Td aprendido en 1981-2016 reconstruye Td 2017-2020 mejor que climatología, Td=Tmin y OLS por zona. Aporte central: regresión local lineal sobre anomalías con selección de receta por zona SENAMHI × día del año.
- Cifras de referencia (validación 1981-2012 → 2013-2016, selección solo con años de entrenamiento): RMSE agrupado 1,228 °C, skill 0,200, 17.027 celdas, 33 de 41 zonas.
- No compara contra ningún modelo de aprendizaje automático ni de fundación. No aísla fuera de muestra cuánto aporta la selección por zona×doy (solo +0,015 de coseno en muestra).
- Partes independientes del método ganador y reutilizables: datos y alcance, protocolo de validación temporal, baselines, corrección FAO-56, validación por soporte observacional, seam test, cola cálida, no estacionariedad, sensibilidad a la versión de Tmin.
- Partes dependientes del método: sección de selección, explicación de la cola de noviembre por el ancho de banda, estabilidad autorregresiva, tablas de escalamiento.

### Benchmark TimesFM

Fuente: `reports/timesfm_benchmark/README.md`, `TRACEABILITY.md`, CSV con sufijo `_limpio`. Código en `experiments/timesfm/`. Modelo: TimesFM 3.0 (330M), zero-shot, checkpoint `google/timesfm-3.0-pytorch`, licencia `timesfm-non-commercial-license-v1.0`.

| Resultado (`ll4`, 17.027 celdas) | Valor | Fuente |
|---|---|---|
| RMSE TimesFM `tmin_anom_full` | 1,1536 | `nacional_limpio/leaderboard.csv` |
| RMSE `tuned` | 1,2279 | ídem |
| RMSE climatología | 1,5352 | ídem |
| ΔRMSE pareado TimesFM − `tuned` | +0,0743 [0,074; 0,075], gana en 99,24 % de celdas | `nacional_limpio/effect_sizes_all.csv` |
| Gana en zonas | 33 de 33 en `ll4` y `ll2`; 32 de 33 en `ll1` | `nacional_limpio/metrics_by_zone.csv` (derivado) |
| Sesgo global | TimesFM +0,104; `tuned` −0,033 | leaderboard |
| Cribado (1.092 celdas): variante ingenua `tmin_td_full` | 0,8718 frente a 0,9326 de `tuned` | `cribado_limpio/leaderboard.csv` |
| Cribado: sin Tmin (`uni_td_full`, `uni_anom_full`) | 1,3124 y 1,2780, sin mejorar la climatología (1,2840) | ídem |
| Cribado: contexto de 2 años (`tmin_td_short`) | 0,9476, peor que `tuned` | ídem |
| Departamental (2.048 celdas) vs TCN | 0,7996 frente a 0,8484 / 0,8429 / 0,8325 (tres semillas) | `departamental/metrics.csv` |
| Producto 2017-2020, acuerdo TimesFM–Palacios | RMSE entre productos 0,465, r 0,9986 | `real_limpio/agreement_overall_limpio.csv` |
| Cola cálida >35 °C | TimesFM 0,171 %; Palacios 0,133 %; ambos solo en la clase A(r)A', 82,8 % en noviembre en TimesFM | `real_limpio/tail_summary_limpio.csv` |
| Cobertura del intervalo q10–q90 | 0,8102 en el backtest nacional | leaderboard |
| Costo | 5,09 celdas/s con TF32; ≈6,4 días para 2,8 M celdas; producto 2017-2020 en ≈5,1 días y 158 GB | `coste_throughput.csv`, `TRACEABILITY.md` §7 |

Salvedades ya documentadas: el agregado no es un promedio del Perú (el 51,4 % de las celdas, 8.755 de 17.027, cae fuera del país; bead `tdew-214.8`); los paneles departamental y de escala usan un `tuned` con selección con fuga y no son comparables con las cifras limpias; la variante ganadora se eligió sobre el mismo bloque de evaluación, sin fold de desarrollo (bead `tdew-214.11.8`).

## 3. Hallazgos de la revisión escéptica (subagente)

Los análisis se hicieron con scripts en el scratchpad de la sesión anterior (`/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad/a1.py` a `a6.py`). Pueden no persistir; si se necesitan, copiarlos al repositorio. Leen `/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet`.

**LLR simple (reimplementación del subagente, no es el pipeline de Palacios).** Regresión local de la anomalía de Td sobre la anomalía de Tmin del mismo día, núcleo tricúbico circular en día del año, ajustada con 1981-2012, `h` elegido con validación 2009-2012. Sin zonas ni autorregresión.

| método | RMSE total | 2013-14 | 2015-16 | sesgo |
|---|---|---|---|---|
| TimesFM | 1,1536 | 1,1665 | 1,1407 | +0,104 |
| `tuned` | 1,2279 | 1,1676 | 1,2853 | −0,033 |
| LLR simple (h = 60) | 1,1748 | 1,1471 | 1,2019 | −0,010 |
| climatología | 1,5352 | 1,3921 | 1,6658 | −0,363 |

- El LLR simple apenas depende de `h`: 1,175 a 1,181 entre h = 7 y h = 60. Un OLS por celda sin ventana da 1,190.
- Brecha `tuned` − TimesFM por año: 2013 = −0,055, 2014 = +0,059, 2015 = +0,165, 2016 = +0,126. En 2013-14 hay empate.
- Bootstrap por bloques mes-año (48 bloques): brecha +0,074, IC [0,011; 0,140]; TimesFM mejor en 35 de 48 meses.
- Frente al LLR simple, TimesFM gana +0,021: IC por bloques espaciales de 2° [0,012; 0,031], IC por bloques mes-año [−0,011; 0,053], que incluye el cero. Gana en 77 % de las celdas y en 32 de 33 zonas.
- El sesgo no explica la ventaja: quitar el sesgo agranda la brecha (1,149 frente a 1,227). El 86 % de la diferencia de error cuadrático viene de |z| > 2 (6 % de los casos); en |z| < 1 gana `tuned`. Enero concentra más de un tercio del ΔMSE (aproximado).
- Los errores de TimesFM y `tuned` tienen correlación 0,929.
- Hipótesis, no verificada: que 2015-2016 (El Niño; anomalía media observada +0,74 y +0,52 °C) explique la ventaja de ese tramo.

Por verificar: el subagente reimplementó el LLR simple y recalculó todo; Palacios y el equipo deben revisar esa reimplementación antes de usarla como rival oficial.

## 4. Enfoques considerados y camino elegido

| Narrativa | Idea | Estado |
|---|---|---|
| A | «La covariable hace el trabajo»: escalera climatología, LLR simple, `tuned`, TimesFM; casi todo el beneficio viene de Tmin y un regresor | adoptada como forma de la evidencia |
| B | Dos productos 2017-2020 (LLR y TimesFM) con su desacuerdo como incertidumbre; descriptor de datos | segundo artículo, tras A4 |
| C | Protocolo de validación de extensiones temporales de productos grillados (fuga de selección, marco de muestreo, soporte, año frente a horizonte) | adoptada como columna vertebral |
| D | Híbrido LLR + TimesFM | descartado por ahora, sin evidencia de que aporte |
| E | Un modelo de fundación como reemplazo sin diseño local: se compara costo de diseño y conocimiento del país, no solo cómputo | adoptada como tesis |

**Camino elegido: E como tesis, C como columna vertebral, A como estructura de la evidencia.** Frase objetivo, sujeta a lo que cierren A1–A3 y T1: un modelo de fundación zero-shot sin diseño local iguala o supera a una regresión diseñada por zona climática para reconstruir Td desde Tmin; un regresor simple queda muy cerca; el protocolo de validación cambia la conclusión más que el estimador.

Argumento de E (aportado por el usuario): LLR es más rápido, pero exige diseñar y conocer el contexto del país (shapefile SENAMHI de 41 zonas, búsqueda de recetas por zona×doy, grilla de `h`, regrid de la Tmin 2017-2020, recursión autorregresiva, ≈39,5 h de GPU para seleccionar y entrenar). TimesFM solo necesita el checkpoint público, el historial de Td de cada celda y la Tmin futura. El eje relevante es el esfuerzo de diseño más el cómputo, no el cómputo solo.

Matices que el paper debe sostener:
- Frente al LLR simple la ventaja es ≈0,02 °C. «No hace falta diseñar» es cierto frente a `tuned`, pero un regresor simple también casi no necesita diseño. La comparación honesta tiene tres puntos: LLR experto, LLR simple, TimesFM.
- «Sin conocer el país» no está probado: todo el benchmark es Perú y PISCO. Las celdas fuera de Perú (51,4 %) son el mismo producto y no cuentan como transferencia.
- TimesFM no es independiente de los datos: necesita Tmin y entre 11 y 32 años de historial local de Td.
- La licencia de los pesos es no comercial; limita cualquier recomendación de uso operativo.
- El costo de cómputo comparado en la documentación mezcla hardware y etapas distintas (TimesFM en RTX A2000 sin selección; `tuned` con coeficientes ya entrenados). Hay que medir en la misma máquina y las mismas celdas, con y sin selección de recetas.

## 5. Plan de resolución

Orden recomendado: A1 y A2 en paralelo, A3, decisión 1, T1, A4, redacción.

### A1. Bloque 2009-2012

Objetivo: separar efecto del estimador de efecto del año calendario (El Niño 2015-2016).

- Definir un split nuevo en `experiments/timesfm/panel.py` (`SPLITS`, `SplitSpec`; hoy `ll1`, `ll2`, `ll4`): entrenar 1981-2008, predecir 2009-2012. Mantener la regla de que Td del bloque oculto no entra al contexto y Tmin sí.
- Correr `experiments/timesfm/run.py` con `tmin_td_full` (variante primaria preregistrada, descrita en `variants.py` como «la comparación justa») y con `tmin_anom_full` (exploratoria), sobre las mismas 17.027 celdas del run limpio.
- `tuned` del mismo bloque: `HPC_code_tunning/select_backtest.py` con `--train-years` 1981-2008 y luego `HPC_code_tunning/backtest.py` (ver `reports/paper/scripts/backtest_clean_run.sh` para el recetario). Climatología con años de entrenamiento solamente. Verificar que la reproducción de ll4 siga dando 1,2279 antes de confiar en el nuevo bloque.
- LLR simple: reimplementar a partir de `a1.py`–`a6.py` y registrarlo como rival oficial.
- Evaluar con `experiments/timesfm/evaluate.py` y `HPC_code_tunning/effect_sizes.py`, `merge_predictions.py` para añadir la columna `pred_timesfm`.
- Reportar siempre la brecha por año, además de la agregada. Reportar el RMSE restringido a las 8.272 celdas dentro de Perú y el RMSE macro por zona.
- Nota: antes de 2000 no hay LST de MODIS en la construcción de PISCO; el bloque 2009-2012 con contexto desde 1981 mezcla regímenes del producto. `tmin_td_med` (contexto 2002-2012) ya existe como control.

Criterio de lectura: si TimesFM mantiene la ventaja sobre `tuned` y sobre el LLR simple en 2009-2012, E se sostiene; si la brecha con el LLR simple desaparece, el paper pasa a C+A.

### A2. `tuned` sin rezagos de Td

Objetivo: medir cuánto cuestan la autorregresión y el criterio de selección. Evidencia: `HPC_code_tunning/loyocv.py:6-16` selecciona con coseno sin centrar y puntuación de un paso (teacher-forced), pero el despliegue es autorregresivo y se puntúa con RMSE (`backtest.py:274-276`); el rezago se siembra con `hist_df`.

- Correr `select_backtest` y `backtest` solo en `ll4` con un pool sin rezagos de Td (`const`, `TMIN_anom`, rezagos de Tmin).
- Alternativa más barata: incluir el LLR simple como cuarto rival oficial, y documentar que no equivale a Palacios sin autorregresión.
- Requiere coordinación con Palacios: el pipeline y su configuración son suyos.

### A3. Control con Tmin barajada

Objetivo: comprobar que la habilidad de TimesFM proviene de la covariable.

- Sobre el panel de cribado (1.092 celdas, ≈5,5 min a 3,3 celdas/s), entregar a TimesFM la Tmin de otro año con el mismo día del año, o de otra celda de la misma zona.
- Resultado esperado: el skill colapsa hacia la climatología. Si no colapsa, hay estructura de Td en el contexto que se está usando y hay que investigarla.
- Reutilizar `run.py` con un parámetro de barajado; registrar proveniencia como el resto (`reports/metric_provenance.jsonl`).

### A4. Contraste externo 2017-2020

Objetivo: dar alguna referencia de exactitud donde no hay Td observado en PISCO.

- Contrastar ambos productos con ERA5-Land Td o con estaciones SENAMHI en 2017-2020, en anomalías y por año. Reportar el desacuerdo por año junto con el índice ONI.
- Verificar la distribución de la Tmin regridada 2017-2020 (`future_tmin_by_bucket`) frente a 2013-2016 en las mismas celdas: media, desviación y correlación en el solapamiento, si existe.
- Pendiente de decidir: acceso a ERA5-Land y a estaciones SENAMHI con Td.

### T1. Prueba de transferencia

Objetivo: sostener «sin conocer el país».

- Requisitos del conjunto: Td y Tmin diarias con al menos 15 años de historial común y un bloque de 4 años reservado; idealmente otro país o región climática distinta.
- Candidatos a evaluar (no verificados): Tmin y Td de ERA5-Land en otro dominio (por ejemplo Colombia, Bolivia o Chile) con los mismos ajustes de TimesFM y una escalera idéntica; otra variable PISCO si existe con par comparable.
- Mismos ajustes de TimesFM (variante, contexto, covariable), sin tocar nada por región. LLR simple y climatología como baselines; `tuned` solo si se dispone de zonas climáticas locales, lo cual es en sí mismo un dato sobre el costo de diseño.
- Si no se encuentran datos, la tesis E se redacta como hipótesis con evidencia dentro de Perú y se declara la limitación.

### Decisión 1 (después de A1–A3)

- Si TimesFM sigue ganando en 2009-2012 y su brecha con el LLR simple se mantiene con intervalos que excluyan el cero por bloques mes-año: seguir con E como tesis.
- Si la brecha desaparece: paper C + A, con el mensaje de que la covariable hace el trabajo y el diseño experto no mejora un regresor simple.

## 6. Preguntas abiertas

1. ¿Tmin entra como predictor en la construcción de Td PISCO v1.1? Si entra, parte de la habilidad compartida es circular. Preguntar a Palacios.
2. ¿Hay dominio fuera de Perú con Td y Tmin disponibles para T1?
3. ¿Qué evidencia de esfuerzo de diseño se puede cuantificar (horas-persona, componentes del pipeline) para la columna de costo?
4. Acuerdo con Palacios sobre el cambio de historia: el paper y `PAPER_PLAN.md` son suyos.

## 7. Referencias consultadas (existencia verificada solo por fichas; abrir texto completo antes de citar)

- Das et al. (2024), TimesFM, ICML, PMLR 235, arXiv:2310.10688.
- Ansari et al. (2024), Chronos, TMLR, arXiv:2403.07815. Woo et al. (2024), Moirai, ICML. Rasul et al. (2023), Lag-Llama, arXiv:2310.08278. Garza y Mergenthaler-Canseco (2023), TimeGPT-1, arXiv:2310.03589 (autores a confirmar).
- Toner et al. (2025), modelos zero-shot en datos de nube, arXiv:2502.12944: quedan por debajo de un modelo lineal y de un naive estacional.
- Kimball, Running y Nemani (1997), Td desde Tmin, *Agric. For. Meteorol.* 85. Allen et al. (1998), FAO-56. Lobit et al. (2018), *Theor. Appl. Climatol.* 133.
- Huerta et al. (2023), PISCOt v1.2, *Scientific Data*. Aybar et al. (2020), PISCOp, *Hydrol. Sci. J.* Muñoz-Sabater et al. (2021), ERA5-Land, *ESSD*. Verdin et al. (2020), CHIRTS-daily, *Scientific Data*.
- Chronos-2 (arXiv:2510.15821, preprint; admite covariables nativas). Faw et al. (2025), In-Context Fine-Tuning, ICML.
- Gneiting y Raftery (2007), reglas de puntuación propias, *JASA*. MultiLLR: arXiv:1809.07394 (autores a verificar en la ficha).
- No se encontró estudio directo de modelos de fundación en gap-filling de variables meteorológicas grilladas; la búsqueda fue acotada y debe repetirse con «ERA5», «station temperature» y «CAMELS» antes de afirmar un vacío.
- XReg de TimesFM: solo respaldado por el README del repositorio de google-research/timesfm.

Revistas candidatas: Environmental Data Science o GMD (comparación y protocolo), Scientific Data o ESSD (producto, para el segundo artículo), Journal of Hydrometeorology o IJC (validación).

## 8. Documentos desactualizados (corregir antes de usarlos como fuente)

- `reports/timesfm_benchmark/limitaciones.md` §8: conserva 90 min, 38,5 h y ≈10,3 días extrapolados; el README y `TRACEABILITY.md` traen 56 min, 23 h 48 min y ≈6,4 días con TF32.
- `experiments/timesfm/README.md`, sección del producto 2017-2020: cita ≈5,9 días y 4,3 celdas/s extrapolados; la corrida real fue de 4,99 celdas/s y ≈5,1 días.
- `docs/protocol/timesfm_manifest.yaml`: conserva `coste.resumen: PENDIENTE`, panel departamental de 8.192 celdas, 38 zonas y «block-bootstrap».
- `reports/timesfm_benchmark/README.md` no recoge el cambio de signo del sesgo entre bloques (+0,180, −0,126, +0,104 en `ll1`, `ll2`, `ll4`; derivado), la cobertura del 80 % del backtest nacional ni los resultados de anomalías; esos viven en el artefacto y en los CSV.
- Las tablas departamental y de escala usan `tuned` con fuga; no mezclarlas con cifras limpias sin advertencia.

## 9. Restricciones del proyecto relevantes

- Todo texto en español, voz impersonal, según `ESTILO_REDACCION.md`; antes de redactar el paper se debe releer ese archivo.
- Ejecutar todo con `uv run`.
- Un cierre de bead dispara la actualización del Gantt en Notion (`Bead ID`); si se abren beads para A1–A4 y T1, crear también la fila en Notion con su `Bead ID`.
- `git push` va al remoto `fork`. Hacer commit de los fuentes de un artefacto antes de publicarlo.
- Los datos son celdas de rejilla agregadas y no contienen PII. Si se comparte material inédito con Claude, no dar retroalimentación (pulgar arriba o abajo) sobre esa conversación.
- Org (CIP): validar el contenido generado con IA con expertos, ser consciente de sesgos y declarar el uso de IA generativa en el trabajo.
