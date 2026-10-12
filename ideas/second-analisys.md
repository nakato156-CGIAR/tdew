# Segundo análisis de las dos propuestas de arquitectura para PISCO

Fecha: 25 de septiembre de 2026.

Documentos evaluados:

- **Propuesta A**: `ideas/pisco-prediction-model-architecture-en.md` ("PISCO Variable Prediction Model Architecture", revisión del 23 de septiembre de 2026).
- **Propuesta B**: `ideas/propuesta-pruebas-atencion-climatica-peru-REV1.md` ("Propuesta de pruebas: predicción multicanal de PISCO para Perú", revisión 1 del 22 de septiembre de 2026).

Este análisis se hizo de forma independiente de cualquier evaluación previa de las mismas propuestas. La evidencia del proyecto se tomó de `PAPER_PLAN.md`, `HANDOFF.md`, `reports/`, `docs/protocol/`, el código de `experiments/` y los issues de `bd`. Las cifras que se citan se contrastaron con los CSV o con el código. Cuando un informe en markdown y un CSV no coinciden, se indica.

Escala de fuerza de evidencia usada en todo el documento:

- **fuerte**: medición sobre el mismo problema, con controles, varias semillas o folds, y sin confusores conocidos;
- **moderada**: medición sobre un problema cercano, o sobre el mismo problema con un confusor identificado;
- **débil**: indicio indirecto (un solo día, una sola semilla, otro objetivo u otro horizonte);
- **nula**: no se midió.

---

## 1. Qué propone cada documento

### 1.1. Propuesta A

Problema. Pronosticar de forma directa `td`, `sd`, `tmin` y `tmax` en cada celda válida de la malla de 0,01° para t+1, t+3 y t+7, usando solo información disponible hasta el día t (A:7-15). El documento aclara que no es un modelo de reconstrucción histórica (A:15).

Hipótesis implícitas, formuladas como comparaciones pareadas en A:507-553: que una atención temporal con sesgo aprendido por antigüedad mejora a la atención sin sesgo (T0→T1→T2), que condicionar ese sesgo por geografía y calendario mejora a una curva compartida (T3 vs T2), que una rama regional a 0,10° aporta (S0–S2 vs T0–T3), que el contexto entre celdas regionales aporta respecto de usar solo la celda contenedora (S2 vs S2-1×1), y que la salida conjunta de las cuatro variables mejora a cuatro modelos separados (A:549).

Arquitectura (A:173-438). Una CNN residual con dilataciones 1, 2, 4 y 8 sobre mapas diarios de 12 canales a 0,10° (anomalías agregadas, fracciones de disponibilidad, fracción de dominio, DEM, latitud y longitud), con campo receptivo de 31 celdas regionales (unos 340 km de ancho, 167 km del centro al borde, A:253-259). Un codificador diario por punto de 64 componentes que concatena anomalías, máscaras, calendario, contexto geográfico y el vector regional (A:273-298). Tres consultas por punto, una por horizonte, con cuatro cabezas de 16 componentes; las claves incluyen la antigüedad `log(1+j)` y `j/30` (A:300-325). Un sesgo aditivo `b(j)` generado por un MLP de 1.889 parámetros, anclado en `b(0)=0` e inicializado en cero para que el modelo arranque igual que la atención base (A:342-386). Una cabeza de salida que combina la atención con el estado del día t (A:421-438). El orden de magnitud declarado es de 10⁵ parámetros.

Plan de evaluación. Partición 1981–2004 / 2005–2010 / 2011–2016 por fecha objetivo (A:63-69); climatología diaria con suavizado circular de 31 días, solo con entrenamiento (A:75-98); referencias B0 climatología, B1 persistencia de anomalía, B2 regresión regularizada con rezagos y B3 la regresión local del proyecto reformulada en modo causal (A:511-520); métricas en unidades originales por variable y horizonte, desagregación por región, elevación y estación, bootstrap por bloques temporales y espaciales, y tres semillas para finalistas (A:553-567). Diez pruebas de corrección antes de cualquier corrida costosa (A:569-580).

### 1.2. Propuesta B

Problema. Determinar si un modelo neuronal con función de ponderación temporal aprendida, y opcionalmente con contexto espacial, predice mejor que referencias clásicas los canales diarios de PISCO, con los mismos horizontes y la misma regla causal que A (B:36-53). Declara cinco hipótesis separadas (B:69-75) que coinciden en contenido con las de A, más una cuarta sobre la capa de zonas ambientales.

Lo que B agrega respecto de A:

- Un inventario de datos verificado sobre los archivos (B:81-212): malla de 1982 × 1422 = 2.818.404 celdas, 100 % densa, con 2.178.827 celdas de dominio; `td` y `sd` solo existen hasta 2016; `tmin` y `tmax` de PISCOt v1.2 llegan a 2020; `pc` es nativo a 0,10°; el viento `ws` es una normal mensual sin serie diaria; `eo` es una función determinista de los demás canales.
- Una regla de "medir antes de construir" para el componente espacial (B:304-338): un variograma o descomposición por escala sobre unos 50 días, con una tabla de decisión que omite el componente espacial si menos del 8 % de la varianza de anomalía vive por debajo de 17 km.
- Una prueba previa sin red neuronal: ajustar la regresión con 7, 14, 30 y 60 rezagos y ver si el error baja al agregar historia (B:413-417).
- Un control barato para el kernel: una tabla aprendida de un sesgo por desfase, compartida en todo el país (B:294-295).
- La exclusión de `eo` como objetivo y su uso como prueba de consistencia de extremo a extremo (E1, B:469-473).
- Desagregaciones que A no pide: dentro de Perú frente a la región de relleno por vecino más cercano de la capa de zonas, y distancia a la estación PISCOt más cercana (B:593-602).
- Una regla de cierre explícita: no se exige que el modelo neuronal gane (B:665-667).

### 1.3. Coherencia interna

**Propuesta A.** Es internamente consistente en lo que se pudo comprobar con aritmética. Las dimensiones cuadran: la CNN regional tiene 416 + 4 × 9.312 + 1.056 = 38.720 parámetros, como declara A:249; el MLP del kernel tiene 800 + 1.056 + 33 = 1.889 (A:380); la entrada de la consulta es 64 × 3 + 2 + 8 + D_c = 202 + D_c (A:315); la cabeza es 64 + 64 + 2 + 8 + D_c = 138 + D_c (A:430); una activación de 32 canales sobre 60 mapas de 199 × 143 tiene 54.637.440 valores (A:474). Los mapas de 199 × 143 corresponden a agregar por 10 la malla de 1982 × 1422 que B verificó. A también corrige su propia figura de motivación: señala que la curva rotulada "daily anomaly" es una diferencia entre días y no la anomalía climatológica del modelo, que 12 % de semivarianza normalizada equivale a correlación 0,88 y no 0,12, y que un variograma no mide el valor predictivo de los vecinos condicionado a la historia local (A:185-214). Esas correcciones son correctas.

Puntos débiles de A:

- El inventario está marcado como no verificado (A:17-36). Algunas de sus dudas ya las resolvió B.
- La maquinaria de máscaras, validez de tokens por soporte regional y respaldo climatológico (A:100-112, A:327-340) está pensada para datos con huecos. El producto es denso: B lo verificó (B:94-97) y el benchmark de TimesFM comprobó celda a celda que la ausencia en `bucketed_training_data` es por celda entera y nunca por huecos internos (`reports/timesfm_benchmark/limitaciones.md`, punto 4). Buena parte de esa maquinaria no se ejercitaría.
- El lote de un solo corte t con B celdas (A:442-448) es válido para reutilizar mapas regionales, pero en este producto 256 celdas del mismo día son muy redundantes entre sí (sección 4).
- No dice cómo se relaciona con el objetivo del proyecto.

**Propuesta B.** Es coherente en lo esencial y su inventario coincide con lo que el proyecto midió por otras vías: 2.818.404 celdas (`PAPER_PLAN.md`:43), la grilla de 302.449 ID como subconjunto (`PAPER_PLAN.md`:134-137), y el 51 % del campo fuera de Perú, que el benchmark de TimesFM reencontró de forma independiente como 51,4 % de la muestra del backtest (`reports/timesfm_benchmark/README.md`:158-167). Tiene cinco inconsistencias:

1. El argumento de §2.5 afirma que una CNN de 15 × 15 accedería "como techo absoluto" a cerca del 8 % de la señal (B:177-179). Es incorrecto: la varianza por debajo de 17 km no es un techo sobre la información que ve un codificador local. El parche contiene el valor local del campo de gran escala, y la pregunta relevante es cuánto mejoran los vecinos la predicción del futuro dado el historial del propio punto. A lo dice explícitamente (A:214). La medición es útil como descripción; como regla de decisión no alcanza.
2. La tabla de decisión de §5.2 usa umbrales de 8 % y 25 % calibrados sobre un solo día (1981-01-16), y el propio apéndice pide rehacerla (B:713). La medición preliminar da 7,8 %, justo en el borde del umbral.
3. El proxy de anomalía `X(t+1) − X(t)` (B:323-324) incluye el día siguiente. Es válido como diagnóstico descriptivo sobre entrenamiento, pero no mide lo mismo que la anomalía climatológica que usa el modelo (A:189-201).
4. M1 se define como "T3 con `td` y `sd` como objetivos conjuntos" (B:508), mientras la Fase 2 ya entrena los cuatro canales juntos (B:463-464). No queda claro cuál es el control de un solo canal para la hipótesis 5.
5. El §14 repite el párrafo "No se exige que ... gane" dos veces (B:665-667 y B:673-675). La segunda versión nombra a "la regresión local en producción" como referencia competitiva, lo que contradice B:56-61 y B:513-519, donde se afirma que el modelo de producción resuelve otro problema y no debe compararse.

Además, B lista `pc` como objetivo en §1 (B:44) y después lo saca de la primera fase (B:130-134, B:466-467). No es una contradicción de fondo, pero conviene ordenarlo.

### 1.4. Disponibilidad de insumos por período

Esta tabla decide qué se puede usar para 2017–2020, que es el período que el proyecto necesita rellenar. Las filas marcadas "según B" no se verificaron en este análisis.

| insumo | 1981–2016 | 2017–2020 | en el pipeline del proyecto |
|---|---|---|---|
| `td` (PISCOeo_pm, sobre PISCOt v1.1) | sí | **no** | sí: `Data/silver/td/` 2002–2016 y el histórico bucketed 1981–2016 (`HANDOFF.md`) |
| `sd` brillo solar (PISCOeo_pm) | sí, según B:118 | **no** | no: no aparece en `Data/silver` ni en el código de `experiments/` |
| `tmin` PISCOt v1.2 | sí | sí | sí; para 2017–2020 solo en los cuatro departamentos (`Data/silver/tmin/`, 436.519 celdas). La malla nacional de 2017–2020 requiere un regrillado pendiente (`PAPER_PLAN.md`:125-134, tarea B2) |
| `tmax` PISCOt v1.2 | sí | sí | igual que `tmin`, solo cuatro departamentos |
| `pc` PISCOp, 0,10° | sí | hasta 2019, según B:121 | no |
| `ws` normal mensual | 12 mapas | 12 mapas | no |
| LST día/noche, normales mensuales MODIS | 12 mapas | 12 mapas | sí (`STATIC_FEATURES`, `experiments/reconstruction/data.py`:19) |
| DEM, TDI, lat/lon | estático | estático | sí |
| capa de 41 zonas SENAMHI | estática, describe 1981–2010 según B:193-196 | estática | sí, usada por el método `tuned` |

La consecuencia es directa. Las dos propuestas usan `td` y `sd` históricos como entradas. En 2017–2020 no hay ni `td` ni `sd` observados, así que un pronóstico emitido el 2016-12-31 produce valores para el 1, el 3 y el 7 de enero de 2017 y nada más. Encadenarlo durante cuatro años sin entradas exógenas converge a la climatología en pocos días, como B mismo advierte (B:63-67).

---

## 2. Relación con el objetivo del proyecto

El objetivo del proyecto está en `PAPER_PLAN.md`:12-27: extender hacia adelante el Td grillado de PISCO para 2017–2020 aprendiendo la relación con la Tmin v1.2, que sí continúa hasta 2020, y evaluar con un backtest temporal que imita el hueco real de cuatro años (`ll4`, entrenar 1981–2012 y predecir 2013–2016). El protocolo de reconstrucción continua lo formaliza en `docs/protocol/reconstruction_manifest.yaml`: Tmin y Tmax contemporáneas permitidas (línea 32), ningún Td observado dentro del bloque oculto, climatología y normalización solo con entrenamiento.

Las propuestas formulan otro problema: pronóstico a corto plazo con información estrictamente anterior al corte. Las dos diferencias que importan son estas:

- En la reconstrucción, la Tmin y la Tmax del mismo día, y también las de días posteriores, son información legítima porque existen para todo 2017–2020. La regla causal de las propuestas prohíbe justamente eso. Esa regla es la correcta para un pronóstico y demasiado restrictiva para rellenar un hueco.
- El horizonte relevante de la reconstrucción es de 1 a 1.461 días desde el último Td observado, no de 1 a 7.

Lo que sigue siendo útil, y cómo se reorienta:

- **Atención temporal con sesgo por antigüedad.** Se puede aplicar sobre el historial de variables exógenas (Tmin, Tmax y derivadas) en lugar del historial de Td. En la reconstrucción la ventana puede además ser bilateral, t−k … t+k, porque la Tmin futura es conocida. El proyecto no ha probado una ventana bilateral: las features de `build_exogenous_features` solo miran hacia atrás (`experiments/reconstruction/data.py`:219-228).
- **Rama regional a 0,10°.** Se puede alimentar con anomalías de Tmin y Tmax agregadas, que sí existen en 2017–2020, en lugar de las de Td.
- **Salida multivariable.** Pierde sentido para `tmin` y `tmax`, que pasan a ser entradas. Conserva sentido para `td` junto con `sd`, que también falta después de 2016, si el proyecto quiere reconstruir `sd` y con ella calcular `eo` para 2017–2020. Esto último es una ampliación del alcance y debe decidirla el equipo.
- **Prueba E1 de B.** Calcular `eo` por Penman-Monteith a partir de los canales reconstruidos y compararlo con el `eo` publicado sobre bloques 1981–2016 sería una validación de extremo a extremo aplicable a la reconstrucción, siempre que se reconstruya también `sd`.
- **Disciplina experimental.** Las pruebas previas baratas, los controles pareados, las tres semillas y la regla de no exigir que el modelo gane sirven para cualquiera de los dos problemas.

Si el equipo tiene interés en el pronóstico de corto plazo como línea de investigación propia, las dos propuestas son una buena base para ella. En ese caso conviene tratarla como un segundo estudio, con su propio manifiesto, y no mezclar sus cifras con las de la reconstrucción.

---

## 3. Evidencia del proyecto y cuán justa es como prueba de cada idea

| experimento del proyecto | qué midió | en qué difiere de lo que proponen A y B | fuerza para las propuestas |
|---|---|---|---|
| Baselines semana 1 (`reports/week1_baselines/leaderboard.csv`) | Td(t+1) desde X≤t en Lima, Cusco, Loreto y San Martín; train 2002–2012. Validación ALL: climatología 1,3093, persistencia 0,9305, `dept_mlr` 0,8628, `generalist_mlr` 0,8632 | Solo Td, solo t+1, 4 departamentos, 11 años de entrenamiento en vez de 24 | Moderada como equivalente de B0, B1 y B2 para Td t+1 |
| TCN + atención por consulta, semana 1, y su auditoría (`reports/week1_tcn_audit/README.md`) | La atención pone 0,815 de su masa en t y como mucho 0,016 en cada rezago restante (`06_sensitivity.txt`:45-46). Truncar a los últimos 3 días un modelo ya entrenado mejora el RMSE en 0,055 °C. Un OLS sobre 3 días queda a 0,0025 °C del mismo OLS sobre 31 (0,8504 frente a 0,8479). El OLS con las mismas entradas (0,8479) supera al TCN `best.pt` (0,9498) (`compare_predictors.csv`) | El modelo no tiene codificación posicional de la antigüedad (bead `tdew-z94`); se evaluaba una vez cada 1,7 millones de pasos y el óptimo estaba cerca del paso 2.000; la ponderación por sitio no hacía lo que declaraba. Es el T0 de A sin la antigüedad en las claves y sin kernel | Moderada en contra de la ventana larga para Td t+1. Nula para T1–T3, porque nunca se implementó un sesgo por antigüedad |
| Ablación correctiva `tdew-x46.1` (`reports/week1_tcn_ablation/`) | Cabeza residual y FiLM en identidad mueven el mínimo en menos de 0,005 °C; todas las variantes se degradan tras el paso 1.000 | Una semilla, evaluación cada 1.000 pasos | Débil sobre la cabeza residual de A (A:436) |
| Rango efectivo entre celdas (`reports/week1_tcn_audit/README.md`:44-58) | Loreto 1,23, Tarapoto 1,62, Lima 2,14, Cusco 2,87; el orden coincide con el del sobreajuste en muestra | Entre 4 y 300 celdas; mide redundancia, no valor predictivo de los vecinos | Moderada sobre la redundancia espacial, que afecta al diseño del lote de A y es consistente con §2.5 de B. Débil sobre si una rama regional ayuda |
| Reconstrucción continua, TCN directa (`HANDOFF.md`:237-265) | En `dev_a` y `dev_b`, L=3, 7 y 14 quedan dentro de 0,002–0,013 °C; L=14 es la peor en ambos folds y la compuerta a L=31/60 se cerró | La ventana solo cubre features exógenas, y `exogenous_full` ya incluye medias, desviaciones y pendientes móviles de hasta 30 días (`data.py`:16, 220-228). El propio `HANDOFF.md`:262-265 reconoce que el efecto de la ventana no se aisló | Débil sobre la ventana larga, por ese confusor |
| Reconstrucción `ll4`, panel de 2.048 celdas (`reports/timesfm_benchmark/departamental/metrics.csv`) | RMSE: TimesFM 0,7996; TCN semillas 0/1/2: 0,8484, 0,8429, 0,8325; `tuned` 0,8669; climatología 1,1440. Sesgo de la TCN +0,047, +0,140 y +0,037 según la semilla | La TCN directa no ve Td en absoluto, solo Tmin/Tmax; `tuned` usa rezagos de Td autorregresivos y Tmin; TimesFM usa 32 años de Td y la Tmin de todo el bloque | Fuerte como referencia de nivel para la reconstrucción en los cuatro departamentos |
| TimesFM, cribado de variantes (`reports/timesfm_benchmark/cribado/leaderboard.csv`) | Con Tmin: contexto de 2 años 0,9509, de 11 años 0,8834, de 32 años 0,8760; anomalía de Td con anomalía de Tmin 0,8432; sin covariable 1,2825–1,3171 (climatología 1,2884) | Contexto de años, no de días; el modelo recibe la covariable para todo el bloque oculto; diez variantes se eligieron sobre el mismo `ll4` | Moderada a favor de modelar en anomalías y de un modelo de atención con historial largo y covariable exógena. Nula sobre el kernel de A y B |

Dos observaciones sobre esta tabla.

La evidencia contra la ventana larga es consistente entre tres experimentos distintos, pero los tres miden Td a un día o la reconstrucción con features ya resumidas. Nada del proyecto mide `sd`, `tmin` o `tmax` como objetivos, ni horizontes de 3 o 7 días, donde la memoria de más largo plazo podría pesar más. Tampoco se probó nunca un sesgo explícito por antigüedad: el TCN aprendió la recencia por su causalidad convolucional, sin que nada se la diera como cantidad (bead `tdew-z94`).

El resultado de TimesFM se lee a veces como evidencia a favor de "más contexto". Es contexto de otra escala. Lo que muestra el cribado es que ver 11 años o más de la relación Td–Tmin de una celda mejora frente a ver 2. Es un efecto de estimación de la relación y del ciclo estacional, cercano a lo que hace `tuned` al agrupar años por día del año. No dice nada sobre si pesar el día t−40 frente al t−3 aporta, que es lo que ponderan los kernels de A y B con L=60.

---

## 4. Evaluación componente por componente

Veredictos: **integrar** (adoptar tal cual o ya está en el proyecto), **adaptar** (adoptar con cambios), **posponer** (no ahora; condicionado a un resultado previo), **eliminar**.

| # | componente | origen | veredicto | razón | evidencia y fuerza | experimento más barato que lo resolvería |
|---|---|---|---|---|---|---|
| 1 | Formulación como pronóstico t+1/t+3/t+7 con corte causal | A:9, B:53 | adaptar | No sirve para 2017–2020 porque `td` y `sd` no existen después de 2016 (tabla 1.4). Se conserva solo si el equipo abre una línea propia de pronóstico | Disponibilidad de datos: fuerte | Ninguno: es una decisión de alcance |
| 2 | Regla causal y prueba de causalidad (alterar datos posteriores no cambia la predicción) | A:571, B:623-626 | integrar, reescrita | En la reconstrucción la regla correcta es "ningún Td del bloque oculto"; los exógenos pueden usarse en cualquier fecha del bloque. El proyecto ya tiene esta prueba: se reemplaza el Td oculto por 9999 y se exige igualdad bit a bit (`HANDOFF.md`:44-48) | Fuerte (prueba automatizada existente) | Extender la prueba a toda variante nueva |
| 3 | Objetivos `tmin` y `tmax` | A:9, B:463 | eliminar como objetivos en la reconstrucción | Existen en 2017–2020; son entradas | Fuerte | — |
| 4 | Objetivo `sd`, conjunto con `td` | A:9, B:463 | posponer | Solo tiene sentido si se decide reconstruir `eo` 2017–2020. `sd` no está en el pipeline y su archivo no se ha auditado en el proyecto | Nula | Auditoría de `sd` (período, máscara, unidades) y un OLS `sd ~ Tmax, DTR, calendario` en `dev_a`. La relación entre amplitud térmica y horas de sol debe validarla un especialista |
| 5 | Precipitación `pc` | B:121, B:466 | eliminar para esta fase | Resolución nativa 0,10°, fuera del objetivo, las dos propuestas ya la difieren | Fuerte sobre la resolución (según B, no verificado aquí) | — |
| 6 | `eo` como objetivo | B:141 | eliminar | Es función determinista de los demás canales | Fuerte (B:714, `Wiki/knowledge/tools/piscoeo-pm-dataset.md`) | — |
| 7 | Prueba E1: `eo` recalculado frente a `eo` publicado | B:469-473, B:640-641 | posponer | Útil si se reconstruye `sd`; requiere `ws` y una implementación verificada de Penman-Monteith | Nula | Recalcular `eo` con los canales observados de 1981–2016 en una celda por departamento |
| 8 | Anomalías estandarizadas, climatología solo con entrenamiento | A:75-98, B:233-241 | integrar | Ya está en el proyecto. TimesFM confirma el valor de trabajar en anomalías: 0,8432 frente a 0,8760 en Td crudo | Moderada | — |
| 9 | Suavizado circular de 31 días de la climatología y convención de 29 de febrero | A:77-79, B:234-236 | adaptar e integrar | `fit_daily_climatology` promedia por `(ID, doy)` sin suavizar (`experiments/reconstruction/data.py`:182-191), y el día 366 solo se estima con los años bisiestos (9 en 1981–2016). Afecta a todos los modelos por igual, pero añade ruido en la anomalía | Nula (no medido) | Recalcular la climatología suavizada en `dev_a` y medir el RMSE de la climatología y de la TCN L=7. Cuesta una corrida de unos 46 minutos |
| 10 | σ global por canal frente a σ por zona | B:243-245 | posponer | Segundo orden frente a las preguntas de arquitectura | Nula | — |
| 11 | Máscaras de disponibilidad, validez de tokens por soporte regional y respaldo climatológico | A:100-112, A:327-340 | adaptar (simplificar) | El producto es denso; basta con afirmar la ausencia de huecos al preparar los datos y fallar si aparecen | Fuerte sobre la densidad (B:94-97; `limitaciones.md` punto 4) | — |
| 12 | Partición 1981–2004 / 2005–2010 / 2011–2016 | A:63-69, B:223-227 | adaptar | Alinear con `dev_a` (1981–2004 → 2005–2008), `dev_b` (1981–2008 → 2009–2012) y `ll4` (`experiments/reconstruction/protocol.py`:41-58), que ya tienen cachés y resultados comparables | Fuerte (existe la infraestructura) | — |
| 13 | Ventana L=60 con barrido 30/60/90/180 | A:548, B:400-424 | adaptar | La evidencia actual va en contra para Td t+1, pero ningún experimento aisló la ventana en la reconstrucción | Moderada contra, para Td t+1; débil en la reconstrucción por el confusor de las features móviles | La prueba previa de B (B2b): OLS con anomalías de Tmin/Tmax con rezagos 0–7, 0–30 y 0–60, **sin** las features móviles, en `dev_a` y `dev_b`. Horas de CPU |
| 14 | Ventana bilateral de exógenos (t−k … t+k) | no está en A ni en B; surge al reorientar | adaptar (nuevo) | En la reconstrucción la Tmin futura es conocida. TimesFM la recibe para todo el bloque (`experiments/timesfm/run.py`:206-214); la TCN y `tuned` no. Podría explicar parte de la ventaja de TimesFM, aunque no se verificó si su arquitectura la aprovecha | Nula | Añadir al OLS del punto 13 las anomalías de Tmin/Tmax de t+1 … t+7 |
| 15 | Atención con una consulta por horizonte y antigüedad en las claves (T0) | A:300-325, B:504 | integrar como referencia | Es la versión corregida de lo que ya tiene el TCN: agrega la antigüedad que falta según `tdew-z94` | Moderada: el mismo tipo de atención sin antigüedad alcanzó la paridad con MLR en su mejor paso | Parte del paso 3 del plan |
| 16 | Sesgo exponencial global (T1) y tabla de un sesgo por desfase (control de B) | A:527, B:294-295 | integrar | Son los controles baratos; si una tabla por desfase no supera a T0, no hay caso para T2/T3 | Nula (nunca se probó) | Implementarlos en la atención existente sobre el banco de la auditoría (`experiments/tcn/audit_x46/10_ablation.py`) |
| 17 | Kernel flexible compartido (T2) y condicionado por geografía y calendario (T3) | A:342-386, A:528-529 | posponer | Solo si T1 o la tabla por desfase ganan. La atención ya concentra el 81 % de la masa en t sin ayuda, así que el margen esperado es pequeño | Débil (inferencia desde el perfil de atención) | — |
| 18 | Penalización de suavidad η y diagnóstico d₉₀ | A:388-409 | posponer | Depende de 17 | Nula | — |
| 19 | Inicialización en cero del generador del kernel (b=0 al inicio) | A:382, B:283-284 | integrar | Garantiza que la variante arranca igual que su control, lo que hace la comparación limpia | Fuerte por construcción | Prueba unitaria de equivalencia de logits (A:578) |
| 20 | Rama regional CNN a 0,10° con dilataciones 1–8 | A:226-271 | adaptar | En la reconstrucción debe leer anomalías de Tmin/Tmax, no de Td. Requiere Tmin/Tmax nacionales 2017–2020 regrilladas, que hoy no existen (`PAPER_PLAN.md`:125-134); dentro de los cuatro departamentos el campo de 340 km se sale del área disponible | Nula sobre su valor predictivo; moderada sobre la redundancia espacial | Añadir al OLS la anomalía media de Tmin/Tmax de la celda de 0,10° que contiene al punto y de su vecindad de 3 × 3. Si no mejora al OLS, la CNN tiene poco margen |
| 21 | Control S2-1×1 con capacidad equiparada | A:542-544, B:365-367 | integrar si se llega a 20 | Es el único control que separa "contexto entre celdas" de "más capacidad" | — | — |
| 22 | CNN local de 15 × 15 a 0,01° | B:340-367 | eliminar para esta fase | A no la incluye; B la condiciona a una medición que ya apunta a omitirla; el rango efectivo de 1,2–2,9 entre cientos de celdas sugiere poca estructura fina independiente | Débil a moderada | — |
| 23 | Variograma o descomposición por escala sobre anomalías | B:309-327, A:218 | adaptar | Útil como descripción de la resolución efectiva, con varias fechas y regiones como piden ambas. No sirve como regla de decisión: la decisión debe salir de la prueba predictiva del punto 20 | Débil (un solo día, B:713) | Descomposición por escala sobre 50 días de anomalías de Td y Tmin, estratificada por estación y región. Un día de trabajo sin GPU |
| 24 | DEM, TDI, latitud, longitud | A:118-122, B:148-151 | integrar | Ya se usan | — | — |
| 25 | Normales LST | A:124-136, B:150 | integrar con la advertencia de B | Ya se usan. La auditoría las encontró casi inertes en la condición del día objetivo: anularlas cuesta 0,003 °C | Moderada | — |
| 26 | Normal de viento `ws` | A:124, B:140 | posponer | Solo se necesitaría para `eo` | — | — |
| 27 | Capa de zonas como embedding (Z1) | A:550, B:186-201 | posponer | La capa describe 1981–2010 según B, y eso se superpone con los bloques ocultos de `dev_a` y `dev_b`. La advertencia también afecta a `tuned`, que selecciona recetas por zona; en `ll4` (2013–2016) no hay superposición | Nula | — |
| 28 | Lote de un corte t con B celdas | A:442-448 | adaptar | Con rango efectivo de 1,23 en Loreto, 256 celdas del mismo día aportan información equivalente a muy pocas series independientes. La auditoría ya encontró batches de solo 8–28 celdas y memorización en el período de entrenamiento | Moderada | Mezclar varios cortes por lote (A:448 lo permite) y registrar el número de fechas y celdas distintas por lote |
| 29 | Presupuesto: 20.000 pasos, validación cada 1.000 | A:503, B:537 | adaptar | En la reconstrucción el óptimo cayó en el paso 250 en los dos folds (`HANDOFF.md`:175-235); en semana 1, alrededor del paso 1.000–2.000 o antes. Con validación cada 1.000 pasos se perdería el mínimo | Fuerte para la TCN de reconstrucción | Evaluar cada 50 pasos hasta el 2.000, como ya se hace |
| 30 | Una semilla para cribado, tres para finalistas | A:553, B:542 | integrar | Ya está en el manifiesto (`seeds: [0, 1, 2]`). La TCN varía 0,016 °C de RMSE y 0,10 °C de sesgo entre semillas (bead `tdew-x46.3.7`) | Fuerte | — |
| 31 | Referencias B0, B1, B2 y B3 | A:511-520, B:500-503 | integrar, con la escalera del proyecto | En la reconstrucción las referencias son climatología, `tuned`, TCN directa y TimesFM sobre las mismas celdas | Fuerte | — |
| 32 | Prueba previa de B2 con 7, 14, 30 y 60 rezagos | B:413-417 | integrar | Es la prueba más barata del plan y la que decide si el kernel tiene caso | — | Ver punto 13 |
| 33 | Métricas en unidades originales, sesgo, skill; desagregación por región, elevación y estación | A:557-559, B:588-605 | integrar | Ya se hace por departamento y año de horizonte; falta por elevación y estación | Fuerte | Reutilizar las predicciones existentes |
| 34 | Desagregación dentro de Perú / región de relleno | B:197-201, B:598-599 | integrar | El 51,4 % de la muestra del backtest nacional está fuera de Perú (bead `tdew-214.8`) | Fuerte | Reetiquetar las predicciones existentes con `shapely.contains_xy`, como ya se hizo |
| 35 | Desagregación por distancia a la estación PISCOt más cercana | B:600-602 | integrar | Es barata y responde si el modelo aprende el interpolador más que el clima | Nula | Requiere el archivo de estaciones que cita B:712; no se verificó su presencia en este análisis |
| 36 | Bootstrap por bloques temporales y espaciales | A:563, B:607-609 | integrar | Los intervalos del proyecto remuestrean solo celdas. Con celdas muy correlacionadas y días autocorrelacionados, intervalos como [0,065; 0,066] °C (`reports/timesfm_benchmark/README.md`:187) probablemente son demasiado estrechos | Moderada (la dependencia está medida; el efecto sobre el intervalo no) | Recalcular los intervalos existentes con bloques de 30 días y bloques espaciales mayores que el rango de correlación |
| 37 | Restricciones físicas registradas antes y después de proyectar | A:438, B:480-485 | integrar para `sd` si se llega al punto 4; para Td basta el rango QC | Ya existe la fracción fuera de rango QC | — | — |
| 38 | Evaluación en celdas nunca supervisadas | A:561, B:551-553 | integrar como prueba secundaria | Coincide con el bead `tdew-x46.4` | Nula | Reservar una banda de latitud por departamento en `dev_a` |
| 39 | Pruebas de corrección antes de corridas costosas | A:569-580, B:621-643 | integrar | La mayoría ya existe como pruebas del repositorio (69 pruebas según `HANDOFF.md`:36) | Fuerte | Añadir las que falten para cada componente nuevo |
| 40 | Inferencia por fecha con caché regional y mosaicos con halo | A:582-605, B:581-582 | posponer | Solo si la rama regional supera su control | — | — |

---

## 5. Comparación entre las dos propuestas

Las dos comparten la mayor parte de la metodología: partición temporal por fecha objetivo, anomalías con climatología de entrenamiento, atención con sesgo aditivo anclado, controles T0–T3, tres semillas, y la advertencia de que las curvas de atención no son causalidad. A parece ser la revisión más tardía de un borrador común; B es la que verificó los datos.

Fortalezas de A:

- Especificación completa y comprobable: dimensiones, número de parámetros, formas de tensor por paso (A:452-465) y reglas de caché que evitan el error de reutilizar activaciones de una CNN que se sigue entrenando (A:467-472).
- Lectura correcta de la figura del variograma y la distinción entre separación de pares, ancho del campo receptivo y alcance desde el centro (A:214-216, A:259).
- Una rama regional a 0,10° que reparte el costo de forma razonable y trae su control 1×1 con la limitación declarada (A:544).
- Separación entre el T2 compartido y un control exponencial por cabeza y horizonte, para no atribuir a la forma lo que viene de más grados de libertad (A:533).

Fortalezas de B:

- Inventario verificado, con el método de verificación de cada cifra (B:702-716).
- Orden de trabajo que empieza por lo barato: la medición espacial y la prueba de rezagos antes de escribir el modelo (B:525-527, B:647-653).
- Exclusión razonada de `eo` y `pc`, y la prueba E1.
- Desagregaciones dentro/fuera de Perú y por distancia a estación, que el proyecto no tiene.
- La advertencia de que las covariables estáticas son las mismas que usó el interpolador de PISCOt, así que el modelo reaprende parte de esa relación (B:153-155).
- La regla de cierre: un resultado negativo resuelve la pregunta.

Qué tomar de cada una, en resumen: de B, el inventario, el orden de trabajo, las pruebas previas y las desagregaciones; de A, la especificación de la atención, del kernel y de la rama regional, sus pruebas de corrección y sus reglas de caché. De ninguna de las dos conviene tomar el problema tal como está formulado si el objetivo sigue siendo 2017–2020.

---

## 6. Debilidades de los experimentos propios que limitan estas conclusiones

1. **El sesgo por antigüedad nunca se probó.** La atención del TCN no recibe la posición en la ventana (`tdew-z94`). Las conclusiones sobre ventanas largas vienen de un modelo que no podía pesar los días por su antigüedad salvo por la causalidad convolucional, y de regresiones lineales. Eso es un argumento contra la ventana larga en general, no contra un kernel en particular.
2. **La ventana de la reconstrucción está confundida con las features móviles.** L=3, 7 y 14 se compararon con medias, desviaciones y pendientes de hasta 30 días ya incluidas (`HANDOFF.md`:262-265). La compuerta de L=31/60 se cerró bajo esa condición.
3. **Solo se estudió Td.** No hay nada medido sobre `sd`, ni sobre `tmin` o `tmax` como objetivos, ni sobre t+3 o t+7.
4. **El valor predictivo del espacio no se midió.** El rango efectivo mide redundancia, y el variograma de B mide estructura; ninguno responde si los vecinos mejoran la predicción dado el historial local.
5. **El bloque `ll4` ya no está intacto.** El `HANDOFF.md` lo describe como sellado, pero el benchmark `tdew-214` ya lo usó: diez variantes de TimesFM se eligieron sobre él (declarado en `reports/timesfm_benchmark/README.md`:78-96) y la TCN tiene resultados con tres semillas (`departamental/metrics.csv`). Cualquier variante nueva que se seleccione mirando `ll4` hereda ese sesgo. La selección debe hacerse en `dev_a` y `dev_b`.
6. **Los intervalos de confianza son estrechos por construcción.** Remuestrean celdas como si fueran independientes, lo que no son según la auditoría.
7. **Los informes en markdown van por detrás de los CSV.** `reports/timesfm_benchmark/README.md`:305-309 dice que faltan `tuned` y las semillas 1 y 2 de la TCN en el panel departamental, pero `departamental/metrics.csv` ya los contiene (`tuned` 0,8669; TCN 0,8429 y 0,8325). Las comparaciones de este documento usan los CSV.
8. **Las comparaciones de reconstrucción no igualan la información.** La TCN directa usa Tmin y Tmax hacia atrás y ningún Td; `tuned` usa Td autorregresivo y Tmin; TimesFM usa 32 años de Td y la Tmin de todo el bloque. Las diferencias entre ellos mezclan arquitectura con acceso a datos, y eso limita lo que se puede atribuir a la atención.
9. **La cobertura espacial de las pruebas neuronales es parcial.** Todo lo neuronal se hizo en cuatro departamentos y en paneles de 2.048 celdas o submuestras de hasta 8 de 64 buckets. La generalización a la malla nacional no está medida.

---

## 7. Plan integrado

El plan está ordenado por costo creciente. Cada paso tiene un criterio de continuación. El umbral de 0,01 °C que aparece varias veces se eligió porque la desviación estándar del RMSE de la TCN entre semillas es 0,008 °C (`tdew-x46.3.7`); una ganancia menor no se distinguiría de cambiar la semilla. Para modelos lineales deterministas el umbral podría ser menor, pero se mantiene por comparabilidad.

**Paso 0. Decidir el alcance.** El equipo decide si el trabajo se limita a la reconstrucción de Td 2017–2020 o si se abre también una línea de pronóstico de corto plazo, y si interesa reconstruir `sd` y `eo`. Sin costo de cómputo. Continuación: decisión escrita en un manifiesto. Si se abre la línea de pronóstico, se sigue el paso 7 en paralelo.

**Paso 1. Higiene sobre predicciones existentes.** Sin entrenar nada: recalcular los intervalos con bootstrap por bloques temporales y espaciales (componente 36), desagregar las predicciones de `tuned`, TCN y TimesFM por dentro/fuera de Perú, elevación y estación (33, 34) y, si el archivo de estaciones existe, por distancia a estación (35). Costo: horas de CPU. Continuación: no hay compuerta; el resultado cambia cómo se reportan las cifras. Si el error crece de forma monótona con la distancia a la estación, eso se reporta y condiciona la interpretación de todo lo demás.

**Paso 2. Pruebas lineales previas en `dev_a` y `dev_b`.** Un OLS o ridge sobre anomalías de Tmin y Tmax, sin features móviles, con cinco variantes: (a) rezagos 0–7; (b) rezagos 0–60; (c) (a) más t+1 … t+7; (d) (a) más la anomalía media regional a 0,10° en la celda contenedora y su vecindad de 3 × 3; (e) (a) con climatología suavizada a 31 días. Hay que resolver antes el problema de memoria de `run_baseline` (bead `tdew-x46.3.6`), por ejemplo ajustando por ecuaciones normales acumuladas por bucket. Costo: horas. Continuación:
- (b) mejora a (a) en ≥ 0,01 °C en ambos folds → el paso 3 tiene caso con ventana larga; si no, el paso 3 se hace solo con ventana corta o bilateral.
- (c) mejora a (a) en ≥ 0,01 °C → la ventana bilateral entra en el paso 3.
- (d) mejora a (a) en ≥ 0,01 °C en ambos folds y en al menos 3 de 4 departamentos → el paso 4 tiene caso. Si no, la rama regional se pospone.
- (e) se adopta si no empeora a ningún departamento.

**Paso 3. Atención con sesgo por antigüedad en la TCN de reconstrucción.** Solo si el paso 2 autorizó alguna ventana. Variantes: T0 con antigüedad en las claves, T1 exponencial global y la tabla de un sesgo por desfase, todas con inicialización en cero, sobre la ventana que el paso 2 haya habilitado (larga, bilateral o ambas), con evaluación cada 50 pasos y lotes con varios cortes. Control: la TCN directa congelada (`exogenous_full`, L=7, 250 pasos). Costo: unos 46 minutos por corrida con caché (`HANDOFF.md`:212-216); unas 18 corridas para tres variantes, dos folds y tres semillas. Continuación: alguna variante mejora al control en ≥ 0,01 °C de RMSE medio entre semillas, en ambos folds, sin aumentar el valor absoluto del sesgo por encima de 0,10 °C. Solo entonces se prueban T2 y T3.

**Paso 4. Rama regional a 0,10° sobre Tmin y Tmax.** Solo si el paso 2(d) lo autorizó. Requisito previo: regrillar Tmin/Tmax v1.2 nacionales de 2017–2020 (tarea B2 del `PAPER_PLAN.md`), porque la rama no se puede aplicar al período objetivo sin esos mapas. Variantes: S con CNN 3×3 dilatada y S-1×1 con capacidad equiparada. Continuación: S mejora a S-1×1 en ≥ 0,01 °C en ambos folds y tres semillas.

**Paso 5. `sd` y `eo`.** Solo si el paso 0 lo pidió. Primero una auditoría de `sd` y la prueba de Penman-Monteith con canales observados (componente 7); después un OLS de `sd` desde variables térmicas; al final, si las anteriores pasan, salida conjunta `td`+`sd` frente a dos modelos separados. Continuación: el `eo` recalculado con canales observados reproduce el publicado dentro de una tolerancia acordada con un especialista, y el `sd` reconstruido tiene skill positivo frente a su climatología en los cuatro departamentos.

**Paso 6. Confirmación.** Congelar la configuración ganadora de los pasos 3–5 y evaluarla una sola vez en `ll4`, declarando que ese bloque ya se usó para seleccionar variantes de TimesFM. Como confirmación adicional, evaluar en celdas reservadas por bloque espacial (componente 38). Aprobación: los criterios del manifiesto (`docs/protocol/reconstruction_manifest.yaml`:40-47), aplicados sobre el promedio de semillas por la razón que registra `tdew-x46.3.7`.

**Paso 7, opcional. Línea de pronóstico.** Si el paso 0 la abre: B0, B1, B2 y B2b para Td a t+1, t+3 y t+7 sobre los datos de semana 1, seguidos de T0 y T1 con evaluación cada 50 pasos. Continuación: T0 o T1 superan a `generalist_mlr` en ≥ 0,01 °C en validación a t+1 y en al menos uno de t+3 o t+7. Si no, la línea se cierra como negativa, que B acepta como resultado válido. Con `sd`, `tmin` y `tmax` como objetivos, el primer paso es auditar `sd`.

---

## 8. Veredicto

Las dos propuestas son coherentes como diseño experimental. A es la más completa como especificación técnica y sus cifras internas cuadran; B es la más sólida en datos y en orden de trabajo, con cinco inconsistencias puntuales y un argumento incorrecto sobre el "techo" del 8 % para la CNN local. Las dos son técnicamente factibles como piloto en la estación de trabajo actual (RTX A2000 de 12 GB) para la malla de pilotaje que proponen, aunque el costo no se midió y los datos de `sd` y de Tmax nacional no están en el pipeline del proyecto.

Resuelven un problema distinto al del proyecto. Aplicadas tal como están, no producen nada para 2017–2020 más allá de la primera semana de enero de 2017, porque sus entradas principales, `td` y `sd`, no existen después de 2016. Pueden funcionar como estudio de pronóstico de corto plazo. Para Td a un día, la evidencia del proyecto sugiere que la ganancia sobre una regresión con rezagos será pequeña, del orden de la dispersión entre semillas. Esa evidencia es moderada y tiene los huecos listados en la sección 6.

Para la reconstrucción, varios componentes se pueden reorientar: la atención con sesgo por antigüedad sobre variables exógenas, posiblemente con ventana bilateral; la rama regional sobre anomalías de Tmin y Tmax; y la salida conjunta con `sd` si se quiere `eo`. Lo que falta es probar cada uno contra su control en los folds de desarrollo, empezando por las pruebas lineales del paso 2, que cuestan horas y deciden cuáles de los pasos siguientes tienen caso. Las piezas metodológicas de ambas (controles pareados, inicialización en cero, bootstrap por bloques, desagregaciones, tres semillas, regla de no exigir que el modelo gane) se pueden integrar ya.

---

## Nota sobre uso de IA

Este análisis se elaboró con asistencia de Claude (Anthropic) mediante Claude Code, a partir de los archivos del repositorio. No se ejecutaron experimentos nuevos; las cifras citadas provienen de CSV, código e informes existentes y se indicó cuándo un informe no coincide con sus datos. Las interpretaciones climatológicas, en particular la resolución efectiva de PISCO, la relación entre amplitud térmica y brillo solar, la memoria física de las series y la pertinencia de reconstruir `sd` y `eo`, deben validarse con un especialista antes de usarse como argumento formal, conforme a la política de uso de IA del CIP.
