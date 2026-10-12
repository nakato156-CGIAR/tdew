# Propuesta de pruebas: predicción multicanal de PISCO para Perú

Documento de trabajo para el practicante · revisión 1 · 22 de septiembre de 2026

> **Revisión 1.** Corrige el inventario de datos de la versión del 22/09/2026, que fue escrita declaradamente "sin haber
> inspeccionado los archivos del dataset". Todas las cifras de geometría, períodos, resoluciones y
> variables de este documento fueron verificadas leyendo los archivos en disco; el método de
> verificación se indica en cada caso para que sea reproducible. La metodología experimental del
> documento original (separación temporal, matriz de ablaciones, pruebas de corrección) se conserva
> casi íntegra: era su parte sólida.
>
> **Nota de transparencia (política CIP de uso de IA):** este documento fue elaborado con asistencia
> de Claude (Anthropic). Las cifras son medidas sobre los archivos, pero la interpretación
> climatológica — en particular la densidad de la red de estaciones y su relación con la resolución
> efectiva — debe ser validada por un especialista antes de usarse como argumento formal.

---

## 0. Qué cambió respecto de la versión anterior

| # | Versión anterior | Corrección |
|---|---|---|
| 1 | Alcance = un solo canal (`td`) | Alcance = **todos los canales diarios de PISCO como objetivos simultáneos**. La regla causal de la versión anterior (ninguna entrada posterior al corte) **se mantiene** |
| 2 | "aproximadamente dos millones de ubicaciones" | **2,818,404** celdas exactas (1982 × 1422 @ 0.01°) |
| 3 | "1981 a 2016" para todo | Cada canal tiene período distinto; la intersección es 1981–2016 |
| 4 | 6 canales diarios incl. viento y radiación | **5** canales diarios predecibles; viento es una normal estática; radiación = brillo solar (`sd`), sí existe |
| 5 | `eo` como canal más a predecir | `eo` es **función determinista** de los otros canales: se calcula, no se predice |
| 6 | Geometría por auditar (grilla regular vs nube irregular) | **Resuelto**: grilla regular completa, 100 % densa → la alternativa de grafo (§16.9 anterior) se descarta |
| 7 | "39 categorías" de zonas por confirmar | **Resuelto**: 38 climas oficiales SENAMHI (37 Thornthwaite + Glaciar); la capa del proyecto tiene 41 = esos + 2 lagos + lomas |
| 8 | Precipitación como un canal más a 0.01° | PISCOp es nativo **0.10°** — 100× más grueso |
| 9 | CNN local 15×15 como primer codificador espacial | El receptive field de 15×15 accede a ~8 % de la varianza diaria: hay que **medir antes de construir** |
| 10 | 631 GB estimados | 398 GB solo para `td` + `tmin_v12` ya en disco como parquet; el volumen fuente completo supera 600 GB en NetCDF |

---

## 1. Objetivo y alcance

**Objetivo:** determinar si un modelo neuronal que aprende una función de ponderación temporal — y
opcionalmente contexto espacial — predice mejor los canales diarios de PISCO que las referencias
clásicas, y cuánta de esa capacidad proviene del kernel aprendido, del condicionamiento geográfico y
de las observaciones vecinas.

**Qué se predice.** Todos los canales diarios predecibles de §2.2 son **objetivos simultáneos**:
`td`, `sd`, `tmin`, `tmax`, y `pc` con las salvedades de §2.2. No hay canal privilegiado; `td` es uno
más. Los canales derivados y estáticos (§2.3) no son objetivos.

**Regla causal — se mantiene íntegra de la versión anterior.** Ninguna observación posterior al corte
t entra al modelo, de ningún canal, ni como entrada, ni como imputación, ni en estadísticas
calculadas al vuelo. En particular **la temperatura del día objetivo es una salida, no una entrada**:
alimentarla sería circular, porque es parte de lo que el modelo debe predecir. En entrenamiento el
futuro se usa como etiqueta supervisada, nunca como entrada.

Predecir t+1 primero; después extender a t+3 y t+7 mediante salidas directas independientes, sin
introducir observaciones reales intermedias.

**Relación con el pipeline que el proyecto ya tiene.** El modelo en producción (`tdew_estimation/`)
resuelve un problema distinto con otro enfoque: estimar `td` condicionado a `tmin` observado **del
mismo día**, para rellenar `td` donde `tmin` ya existe. Dispone de información que este modelo no
tendrá. **No es la referencia a superar aquí** y no debe presentarse como tal: una comparación
directa no sería informativa en ninguna dirección. Lo que sí corresponde como referencia es la misma
regresión local por anomalías **reformulada con entradas causales** (sólo lags), que es B2 en §9.

**A definir antes de empezar:** los horizontes ℓ y el uso previsto del modelo. Un pronóstico a
t+1…t+7 evaluado sobre años retenidos es un objetivo de investigación coherente por sí mismo; si
además se espera usarlo para extender las series varios años más allá de 2016, conviene saberlo
desde ahora, porque una recursión larga converge a climatología en pocos días y eso cambia qué
métricas importan.

**Hipótesis separadas:**

1. Un kernel temporal aprendido mejora respecto de un kernel fijo.
2. Condicionar ese kernel por ubicación/calendario mejora respecto de una curva compartida.
3. Incorporar observaciones vecinas mejora respecto de usar sólo la serie del punto objetivo.
4. La clasificación ambiental aporta información adicional a coordenadas y elevación.
5. Modelar los canales conjuntamente mejora respecto de un modelo independiente por canal.

Cada hipótesis necesita su comparación controlada; un único modelo grande no permite distinguirlas.

---

## 2. Inventario de datos — VERIFICADO

Esta sección reemplaza la auditoría pendiente de la versión anterior. Ya está hecha.

### 2.1. Malla espacial

**Resuelto: es una grilla regular completa, no una nube irregular.**

| Propiedad | Valor |
|---|---|
| Dimensiones | 1982 filas (lat) × 1422 columnas (lon) = **2,818,404 celdas** |
| Paso | 0.01° exacto en ambos ejes (min = max = mediana de las diferencias) |
| Extensión | lon [−81.40, −67.19], lat [−18.59, 1.22] |
| Ocupación | **100.00 %** — sin huecos; el índice contiene exactamente 1982 × 1422 filas |
| Residual respecto al retículo perfecto | 7×10⁻¹⁰ (lon), 4×10⁻¹¹ (lat) |
| Orden del ID | `ID = fila·1422 + columna`, fila 0 = lat máxima → **scan raster** |
| Máscara de dominio | 2,178,827 celdas válidas (**77.31 %**); el 22.7 % restante es océano/fuera de dominio |

*Verificado en* `henry_simcast_peru_full/td/Outputs/grid_index.parquet` *y contra las coordenadas
nativas de los NetCDF.* El `grid_index.parquet` de `td` y el de `tmin_v12` son idénticos.

Consecuencia: `array = df.sort_values("ID").Value.to_numpy().reshape(1982, 1422)` reconstruye el
mapa sin interpolación. La alternativa de grafo para coordenadas irregulares **queda descartada**.

La máscara de dominio es idéntica para `td`, `sd`, `tmin` y `tmax` (2,178,827 celdas). `eo` difiere:
2,170,925 celdas, 7,902 menos. Construir una máscara de intersección explícita y documentarla.

**Grilla de papa (302,449 IDs):** subconjunto exacto de la malla de 2.8M — las 302,449 celdas caen
dentro del rectángulo y el 100 % tiene `td` válido. Su ID propio (0…302448) **no** es el ID de la
malla grande; el mapeo se obtiene de las columnas `longitude`/`latitude` del shapefile. Los parquet
de 302k no contienen coordenadas.

### 2.2. Canales diarios disponibles

| Canal | Variable | Producto | Período | Res. nativa | Unidad | Archivos | Tamaño |
|---|---|---|---|---|---|---|---|
| Punto de rocío | `td` | PISCOeo_pm (sobre PISCOt **v1.1**) | 1981–**2016** | 0.01° | °C | 433 nc | 101 GB |
| Brillo solar | `sd` | PISCOeo_pm | 1981–2016 | 0.01° | h/día | 433 nc | 109 GB |
| Temp. mínima | `tmin` | **PISCOt v1.2** | 1981–**2020** | 0.01° | °C | 41 nc | 57 GB |
| Temp. máxima | `tmax` | **PISCOt v1.2** | 1981–2020 | 0.01° | °C | 41 nc | 55 GB |
| Precipitación | `pc` | PISCOp | 1981–**2019** | **0.10°** | mm | 1 nc | — |
| *(Temp. v1.1)* | `tmin`,`tmax` | PISCOeo_pm (downscaling v1.1) | 1981–2016 | 0.01° | °C | 866 nc | 185 GB |

`td` y `sd` se construyeron sobre PISCOt **v1.1**, que fue descontinuado y reemplazado por v1.2. Los
`tmin`/`tmax` dentro de `v1_1/` son subproductos intermedios de ese pipeline, **no** la fuente
recomendada de temperatura: para temperatura usar siempre `v1_2/`. Un modelo que use `v1_2/tmin`
para predecir `v1_1/td` cruza dos generaciones de producto. Es exactamente lo que ya hace el modelo
en producción, y es defendible, pero debe declararse.

**Precipitación (PISCOp) es el canal problemático.** Es nativo 0.10°: 198 × 133 = 26,334 celdas,
100 veces más grueso que la malla de temperatura. En disco sólo está extraído a la grilla de papa
(302k), no regrillado a 2.8M. Como entrada a una CNN fina es casi constante dentro del parche; como
objetivo a 0.01° sería inventar resolución que el producto no tiene. Tratarlo aparte, en su propia
malla, o excluirlo de la primera fase.

### 2.3. Canales que NO son predecibles

| Canal | Qué es realmente | Implicación |
|---|---|---|
| Viento `ws` | `ws_mean.nc`: **normal climatológica mensual** (12 pasos de tiempo), sólo velocidad escalar, sin dirección, sin serie diaria | Es un campo estático. Entra como covariable, nunca como objetivo. El ejemplo de advección del documento anterior (vecinos al oeste + viento del oeste) **no es implementable** |
| Evapotranspiración `eo` | Función determinista FAO Penman-Monteith de `tmax`, `tmin`, `td`, `sd`, `ws` y elevación | Predecirla como canal independiente es contar dos veces. Se predicen sus insumos y se **calcula**. Su error se propaga desde ellos y debe reportarse así |
| Incertidumbre ΔETo | 2 agregados (anual, mensual) del paper de `eo` | Referencia de validación, no objetivo |

**Los canales diarios realmente predecibles son cinco:** `td`, `sd`, `tmin`, `tmax`, `pc`.

### 2.4. Covariables estáticas

De la propia colección PISCOt v1.2, todas en la misma malla 1982 × 1422 @ 0.01°:

`DEM` (elevación, 0–6478 m) · `TDI` (índice de disección topográfica, 0–5) ·
`LST_DAY` / `LST_NIGHT` (12 normales mensuales MODIS) · `X`, `Y` (coordenadas).

Advertencia: estas covariables **son las que PISCOt usó para construir el producto**. Usarlas como
predictores no es fuga temporal, pero sí significa que el modelo está reaprendiendo la relación que
el interpolador ya impuso. Reportarlo al interpretar ganancias.

### 2.5. Resolución efectiva — la cifra que decide la arquitectura

PISCOt v1.2 se construye interpolando una red de **302 estaciones** (241 marcadas `filter_qc` para
corrección de sesgo en el gap-filling; 48 marcadas `filter_qc70`, la bandera que el README del
producto asocia al modelo espacial diario y a la validación cruzada) sobre 2,818,404 celdas, usando
las covariables de §2.4. `td` viene además de un producto *downscaleado* desde PISCOt v1.1: es
doblemente derivado.

Dos millones ochocientas mil celdas no son dos millones ochocientas mil observaciones
independientes. Medida de cuánta varianza vive por debajo de cada escala (campo `td`, 1981-01-16, y
su tendencia diaria `Td(t+1)−Td(t)`, donde la climatología estática se cancela):

| Suavizado | Escala | Var. residual — campo `td` | Var. residual — tendencia diaria |
|---|---|---:|---:|
| 3×3 | ~3 km | 0.09 % | 2.0 % |
| **15×15** | **~17 km** | **0.60 %** | **7.8 %** |
| 31×31 | ~34 km | 1.15 % | 10.4 % |
| 61×61 | ~67 km | 2.01 % | 12.0 % |
| 101×101 | ~111 km | 3.20 % | 13.6 % |

Lectura: **el 92 % de la variabilidad día a día es de escala mayor a 17 km.** Un codificador
convolucional con campo receptivo de 15×15 celdas accedería, como techo absoluto, a ~8 % de la
señal — y parte de ese 8 % es la firma del interpolador y del DEM, no atmósfera.

Esto no prueba que el componente espacial sea inútil; prueba que **hay que medirlo antes de
construirlo**. Ver §5.

### 2.6. Capa de zonas ambientales

**Resuelto.** El shapefile de SENAMHI del proyecto es correcto: 38 climas oficiales = 37 tipos de
Thornthwaite + Glaciar. La capa del proyecto tiene **41 clases** = esas 38 + 2 lagos + lomas. No son
39. Usar categorías nominales (41 + una categoría "desconocido"), nunca el código como magnitud
ordinal.

Dos advertencias que siguen vigentes:

- **Fuga temporal.** La publicación oficial del mapa describe el período 1981–2010. Si esa es la
  capa disponible, usarla como predictor en una validación 2005–2010 introduce climatología del
  propio período de validación. En el benchmark principal usar coordenadas y topografía; la capa de
  zonas entra sólo en el experimento Z1, reportado aparte.
- **Dominio fuera de Perú.** El 51 % del campo publicado por el proyecto cae fuera de Perú y recibe
  su etiqueta de zona por un fallback de vecino más cercano. La desagregación de resultados debe
  separar dentro-de-Perú de la región de fallback; de lo contrario, la mitad de la evaluación se
  hace sobre etiquetas extrapoladas. El 100 % de la cola cálida por encima de 35 °C vive en esa
  región y 0 % dentro de Perú.

### 2.7. Lo que falta auditar

- Hora real de agregación de cada variable diaria, y a qué corresponde exactamente `td` diario
  (media, valor a hora fija, derivado de humedad relativa). Esto condiciona qué restricciones físicas
  entre `td`, `tmin` y `tmax` son legítimas.
- Cómo se rellenaron las series de estación (gap-filling con ERA5-Land corregido). Si ese
  procedimiento usó información posterior en el tiempo, el producto ya trae una forma de suavizado
  temporal que ningún diseño posterior puede deshacer. Documentarlo aunque no se pueda corregir.
- Hardware: GPU, VRAM, RAM, almacenamiento y tasa de lectura real de parches. Medirlos antes de
  asignar tiempos.

---

## 3. Separación temporal y construcción de anomalías

**El período común a todos los canales diarios es 1981–2016 (13,149 días).** Todo entrenamiento y
evaluación multicanal ocurre dentro de ese período, porque `td` y `sd` no existen después de 2016.
Si más adelante se quiere un modelo sólo de temperatura, `tmin`/`tmax` v1.2 permiten extender a 2020
— pero sería otro experimento, con otro período y otras fechas de corte.

| Uso | Años | Regla |
|---|---|---|
| Entrenamiento | 1981–2004 | Ajustar pesos, climatologías, escalas y cualquier transformación aprendida |
| Validación | 2005–2010 | Elegir modelos, ventanas, regularización y parada |
| Prueba final | 2011–2016 | Usar después de congelar decisiones |

Asignar cada muestra por sus fechas objetivo. Descartar los cortes cuyos objetivos crucen la
frontera entre bloques; el contexto observado anterior a la frontera sí puede usarse. No mezclar
ventanas aleatoriamente.

Para cada ubicación r, canal v y día del año d, estimar la climatología C(r,v,d) **exclusivamente
con entrenamiento**, suavizando el ciclo anual con una media circular sobre días del año (31 días
como punto de partida configurable). Resolver el 29 de febrero con una convención explícita y
constante. Si hay pocos datos, usar un respaldo regional calculado sólo con entrenamiento y
registrar dónde se empleó.

Definir A(r,v,t) = X(r,v,t) − C(r,v,d(t)) y Z = A/σ_v, con σ_v una escala positiva **por canal**
calculada en entrenamiento. Documentar un piso numérico para canales degenerados. Reconstruir como
X̂ = C + σ_v·Ẑ.

> Nota respecto del pipeline actual: el proyecto ya tiene ajuste por zona × día-del-año. Una única σ
> nacional por canal descarta esa estructura. Empezar con σ global por simplicidad y comparabilidad,
> pero incluir σ por zona como una variante explícita en la matriz de experimentos.

Agregar calendario cíclico (seno/coseno de la fase anual) para días históricos y fechas objetivo.
Quitar la climatología no elimina la estacionalidad de la variabilidad.

Para datos ausentes: máscaras explícitas, objetivos ausentes excluidos del error, imputación sólo
con información permitida. El cero de una anomalía imputada debe distinguirse de una anomalía
observada igual a cero.

---

## 4. Qué significa aprender el kernel temporal

*(Esta sección se conserva sin cambios sustantivos respecto de la versión anterior: su contenido
técnico es correcto e independiente de las correcciones de inventario.)*

No se fija una exponencial ni un tricúbico: se aprende una función positiva del desfase temporal.
Aquí «kernel» significa función de ponderación, no se requiere que sea un kernel de Mercer.

Sea j la antigüedad en días (j=0 es el último día disponible, j=L−1 el más antiguo). Para ubicación
r, corte t, horizonte ℓ y cabeza m:

    b̃(j) = f_θ( log(1+j), j/30, z_r, c_{t+ℓ}, e_ℓ, e_m )

donde z son metadatos estáticos, c es calendario y e son representaciones aprendidas del horizonte y
la cabeza. La división por 30 sólo fija una escala numérica de entrada: no es una ventana ni una
preferencia por treinta días. Mantenerla igual al cambiar L; no normalizar j por L.

Anclar la curva: b(j) = b̃(j) − b̃(0), K(j) = exp(b(j)). Esto fija K(0)=1 sin cambiar los pesos de
atención (restar una constante desaparece en softmax). No obliga a que K sea decreciente.

La atención temporal es a(j) = softmax_j[ qᵀk_j/√d_k + b(j) + M(j) ], con M = 0 en posiciones
permitidas y −∞ en excluidas. **Sumar b directamente a los puntajes**; no calcular exp(b) y después
log(K). Si no existe ninguna observación válida, activar un respaldo explícito (climatología) y no
ejecutar softmax sobre una fila totalmente enmascarada.

**Configuración inicial:** MLP de dos capas ocultas de 32 unidades, compartido entre ubicaciones;
representación de zona de 8 dimensiones cuando esté permitida; una salida escalar por combinación de
ubicación, desfase, horizonte y cabeza; cuatro cabezas temporales. Inicializar la última capa en
cero o muy cerca para comenzar con K≈1, sin imponer recencia. Registrar inicialización y semilla. No
crear un parámetro independiente por cada celda de la malla.

Primero usar z y calendario como contexto de f; no incluir todavía un resumen de la historia
meteorológica dentro del kernel (el puntaje q·k ya depende de ella).

Penalización de rugosidad opcional, sólo si validación la justifica:
R = mean_j [ b(j+1) − 2b(j) + b(j−1) ]², con L = L_pred + ηR. Probar η = 0, 10⁻⁴, 10⁻³. Favorece
suavidad, no monotonía.

**Control barato e imprescindible:** una tabla aprendida de un sesgo por desfase, compartida en todo
el país. Si la red condicionada por lugar no supera esa tabla, no hay caso.

Antecedentes: [representaciones de posición relativa](https://aclanthology.org/N18-2074/),
[ALiBi](https://arxiv.org/abs/2108.12409),
[atención de alcance adaptable](https://arxiv.org/abs/1905.07799). Respaldan mecanismos generales de
posición o alcance; no validan esta combinación para estos datos.

---

## 5. Decidir el componente espacial ANTES de construirlo

Esta sección reemplaza el orden de trabajo del documento anterior, que especificaba una CNN local de
campo receptivo 15×15 como primer codificador espacial.

### 5.1. La medición previa (dos días de trabajo, no dos semanas)

Antes de escribir código de modelo, el practicante debe entregar un **variograma** — o su
equivalente por descomposición de escala — de cada canal.

Un variograma mide cuánto se parecen dos celdas en función de la distancia que las separa: se toman
todos los pares separados por ~1 km y se calcula la varianza de su diferencia, luego los pares a
5 km, 20 km, 100 km. La curva dice a qué escala espacial vive la información. La versión barata,
equivalente para este fin, es suavizar el campo con una ventana k×k y medir qué fracción de la
varianza sobrevive: eso es lo que produjo la tabla de §2.5.

Protocolo mínimo:

- ~50 días elegidos al azar dentro de 1981–2016, estratificados por estación del año.
- Dos campos por canal: el valor crudo y la **anomalía** (o, como proxy barato, la tendencia diaria
  X(t+1) − X(t), donde la climatología estática se cancela).
- Escalas 3, 9, 15, 31, 61, 101, 201 celdas, expresadas también en km (a 0.01° ≈ 1.1 km).
- Reportar por región (costa/sierra/selva) y por estrato de elevación: la sierra puede tener
  estructura fina que el promedio nacional esconde.

### 5.2. Regla de decisión

| Resultado | Qué construir |
|---|---|
| >25 % de la varianza de anomalía por debajo de 17 km, en alguna región | CNN local de §5.3, restringida a esas regiones |
| 8–25 % | Ir directo a la rama regional: agregación 5×5 + CNN sobre la malla gruesa (§5.4) |
| <8 % (lo que sugiere la medición preliminar) | **Omitir el componente espacial en la primera fase.** Probar T0–T3 solamente y reportar que la geometría del producto no sostiene un codificador convolucional fino |

El tercer resultado no es un fracaso: es un hallazgo publicable sobre la resolución efectiva de
PISCO, y ahorra semanas de cómputo.

### 5.3. CNN local, si la medición la justifica

Todas las convoluciones con stride 1, sin pooling.

| Etapa | Operación | Canales | Campo receptivo |
|---|---|---:|---:|
| Proyección inicial | Conv 1×1 + GELU | 32 | 1×1 |
| Bloque 1 | Conv 3×3, dilatación 1, padding 1, residual | 32 | 3×3 |
| Bloque 2 | Conv 3×3, dilatación 2, padding 2, residual | 32 | 7×7 |
| Bloque 3 | Conv 3×3, dilatación 4, padding 4, residual | 32 | 15×15 |
| Proyección final | Conv 1×1 | 64 | 15×15 |

Bloque residual: `U_sig = U + GELU(Conv_d(LN_canales(U)))` — **una sola** convolución espacial por
bloque. `LN_canales` normaliza los 32 canales de cada píxel por separado: llevar canales a la última
dimensión y normalizar sólo esa. No normalizar conjuntamente canales, alto y ancho — introduciría
dependencia de todo el parche e invalidaría el campo receptivo local.

Parches: para un núcleo de 16×16, leer 30×30 (halo de 7 por lado), aplicar la CNN, conservar
`[7:23, 7:23]`, calcular la pérdida sólo en el núcleo. En la frontera real del dominio el halo puede
no tener datos: marcarlo y medir los errores de borde por separado. **No reflejar observaciones
territoriales para fabricar meteorología al otro lado de la costa.**

Campo receptivo físico: 15 celdas × 1.1 km ≈ **17 km**. En una malla lat-lon la distancia
este-oeste varía con la latitud; reportarlo en km, no sólo en píxeles.

Control obligatorio: reemplazar cada Conv 3×3 por Conv 1×1 con los mismos canales y metadatos. Eso
conserva una transformación neuronal por punto y elimina el acceso a vecinos. Si la ganancia es
marginal, agregar un control puntual con capacidad aproximadamente equiparada.

### 5.4. Rama regional

Agregación de 5×5 celdas (≈5.5 km) y una CNN de campo receptivo 15×15 sobre esa escala cubren
≈75 celdas originales por lado (≈83 km). Concatenar con la representación fina y proyectar a 64
componentes antes de la atención temporal. Calcular halo, alineación y resolución física de cada
rama por separado: el halo de 7 celdas finas no sirve para ambas.

Al agregar: promediar magnitudes intensivas; **no** sumar milímetros de precipitación entre celdas
como si fueran días acumulados; no promediar códigos de clase — usar fracciones por categoría.

### 5.5. Entradas del codificador espacial

| Grupo | Canales |
|---|---:|
| Anomalías estandarizadas de los canales diarios (`td`, `sd`, `tmin`, `tmax`) | 4 |
| Disponibilidad por canal | 4 |
| Latitud, longitud, elevación (DEM), TDI, escalados | 4 |
| Normales mensuales: `ws`, `LST_DAY`, `LST_NIGHT` — interpoladas al mes de la fecha | 3 |
| Máscara de celda dentro del dominio | 1 |
| Representación aprendida de la clase ambiental (41 + desconocido), si Z1 lo permite | 8 opcionales |

**16 canales** sin la capa de zonas, 24 con ella. Precipitación se excluye de este bloque: a 0.10°
no aporta estructura dentro del parche. Si se incorpora, hacerlo en la rama regional de §5.4, en su
propia malla.

Los metadatos se alinean espacialmente con cada celda incluyendo los vecinos; replicarlos
conceptualmente en el tiempo no exige guardarlos sesenta veces en disco. En datos dinámicos
ausentes, usar relleno estable (cero en espacio de anomalías) **junto con** la máscara.

---

## 6. Ventana temporal máxima

Se define un máximo L de observaciones diarias. Un kernel aprendido reparte pesos dentro de L; no
descubre datos que no recibió.

- L=60 significa días t−59,…,t: sesenta observaciones incluyendo el corte.
- No equivale a h=60 de una ventana simétrica, que tendría hasta 121 fechas.
- Usar resolución diaria completa dentro de L en el primer experimento.

**Prueba escalonada:** L=60 como configuración de trabajo; comparar L=30 y L=90 en los finalistas.
Si L=90 mejora consistentemente y recibe masa relevante cerca del límite, evaluar L=180. Usar las
mismas fechas objetivo elegibles para todas las ventanas comparadas.

> **Pre-test barato y muy informativo.** Antes de entrenar ninguna red, ajustar la regresión local
> causal de B2 con 7, 14, 30 y 60 lags y ver si el error baja al agregar historia. Si no baja, la
> hipótesis de que hacen falta sesenta días de contexto queda muy debilitada, y con ella buena parte
> de la motivación del kernel aprendido. Este experimento cuesta horas, no días, y da la primera
> lectura empírica sobre cuánta memoria temporal tienen realmente estas series.

No anunciar un «h óptimo» a partir de una curva libre. Reportar, por cabeza y contexto, la mínima
antigüedad que acumula el 90 % del peso de atención; llamarla **alcance efectivo del peso**, no
ventana causal ni memoria física. Mostrar también la curva completa.

Para comprobar que la historia antigua aporta, **reentrenar** con ventana menor y comparar errores.
Quitar días a un modelo ya entrenado es una sensibilidad adicional, no un sustituto.

---

## 7. Especificación de tensores

Para el codificador espacial, el lote de entrada tiene forma `[B, L, C, H, W]`; la salida
`[B, N_horizontes, C_objetivo, H_núcleo, W_núcleo]`. Para B=2, L=60, 16 canales, parche 30×30:

1. Leer `[2, 60, 16, 30, 30]`.
2. Reorganizar como `[120, 16, 30, 30]` para aplicar la misma CNN diaria (no mezcla días).
3. Obtener `[120, 64, 30, 30]`.
4. Recortar el núcleo → `[2, 60, 64, 16, 16]`.
5. Reordenar como `[512, 60, 64]`: 512 secuencias (2×16×16 ubicaciones), cada una con 60
   representaciones diarias de 64 componentes.
6. Construir consultas por ubicación/horizonte y aplicar la atención temporal con el kernel.
7. Salida por canal y horizonte; reconstruir `[2, N_horizontes, C_objetivo, 16, 16]`.

Representación D=64, cuatro cabezas de 16 dimensiones. La consulta se construye con el último H, la
media de los últimos siete H, su cambio reciente, metadatos y fecha objetivo. **La consulta nunca
incorpora ninguna observación del día objetivo**, de ningún canal — sólo su calendario. Todos los
días de entrada son anteriores o iguales al corte t. Enmascarar claves inválidas según una regla
explícita de disponibilidad y mantener idéntico tratamiento en todas las variantes.

La reorganización de tensores no declara independientes las ubicaciones. La pérdida se calcula sobre
los objetivos válidos del núcleo; el gradiente atraviesa salida, atención, kernel y CNN.

Esta factorización permite que un vecino de hace j días influya sobre el objetivo, pero **no** asigna
un peso explícito y auditable a cada par vecino-desfase. No describir la CNN como si ya fuera ese
mecanismo.

---

## 8. Canales objetivo y función de pérdida

**Fase 1 — depuración del flujo:** `tmin` y `tmax` como objetivos, manteniendo todos los canales
históricos disponibles como predictores. Son los canales más suaves y mejor muestreados: si el flujo
tiene un error, aquí se ve antes. No se reporta como resultado.

**Fase 2 — multicanal completo:** `td`, `sd`, `tmin`, `tmax` como objetivos simultáneos en la malla
de 0.01°. Ésta es la configuración que responde las hipótesis de §1.

**Fase 3 — precipitación:** `pc` en su propia malla de 0.10°, con su propia pérdida (§8, última
parte). Una mejora térmica no demuestra mejora en precipitación.

**`eo` nunca es objetivo.** Es una función determinista de los canales predichos (§2.3): se calcula
por FAO Penman-Monteith a partir de `tmax`, `tmin`, `td`, `sd` predichos más `ws` y elevación.
Reportar su error como propagación desde los insumos y comparar contra el `eo` publicado como prueba
de consistencia de extremo a extremo. Es la validación más exigente disponible, porque castiga
errores correlacionados entre canales que las métricas por canal no detectan.

**Pérdida inicial:** MSE de anomalías estandarizadas, promediada por canal, horizonte y objetivo
válido, de modo que ningún canal domine por unidades o por cantidad de datos. Si se balancea el
muestreo por regiones, documentar qué distribución de entrenamiento induce y usar la misma para
todas las comparaciones.

**Restricciones físicas.** `sd` (horas de sol) es no negativa y acotada por la duración del día
astronómico en esa latitud y fecha — es una cota dura y verificable, úsala. `pc` es no negativa.
Registrar cuántas reconstrucciones crudas violan cada condición y reportar métricas antes y después
de una proyección determinista, aplicada igual a todos los modelos comparados. Revisar inversiones
`tmin > tmax`. **No** imponer restricciones de `td` frente a `tmin`/`tmax` sin resolver antes §2.7
(cómo se agregó cada variable y a qué hora corresponde).

Si `pc` entra en alguna fase y presenta muchos ceros, añadir una salida separada de probabilidad de
lluvia y cantidad condicionada, con su propia comparación: cambia el objetivo y la distribución de
salida.

---

## 9. Matriz mínima de experimentos

Mantener idénticos datos, fechas objetivo, normalización, metadatos comunes, presupuesto y criterio
de selección. «Sin kernel» conserva la misma información de calendario y desfase como entrada.

| ID | Modelo | Pregunta |
|---|---|---|
| B0 | Climatología de entrenamiento | ¿Se supera la predicción de anomalía cero? |
| B1 | Persistencia de la anomalía + climatología de la fecha objetivo | ¿Se supera conservar el estado reciente? |
| **B2** | **Regresión local por anomalías en versión causal**: sólo lags, ninguna entrada del día objetivo | **La referencia clásica a superar, con la misma información que el modelo neuronal** |
| B2b | B2 con 7, 14, 30 y 60 lags causales | ¿Aporta más historia, sin red neuronal de por medio? |
| T0 | Atención del punto, sin sesgo temporal adicional | Referencia neuronal temporal |
| T1 | T0 + kernel exponencial con escala global elegida en validación | ¿Basta una preferencia simple por recencia? |
| T2 | T0 + kernel flexible aprendido, compartido | ¿Ayuda aprender la forma? |
| T3 | T2 + condicionamiento por geografía y calendario | ¿Ayuda adaptar la curva al contexto? |
| M1 | T3 con `td` y `sd` como objetivos conjuntos | ¿Ayuda modelar los canales juntos? |
| S0–S2 | Codificador espacial (§5.3/§5.4) + las tres variantes de kernel | **Sólo si §5.2 lo justifica** |
| Z1 | Mejor modelo + capa de zonas auditada | ¿La capa aporta información adicional? |
| E1 | `eo` recalculado desde los canales predichos, vs `eo` publicado | Consistencia física de extremo a extremo |

**Sobre B2.** El proyecto ya tiene implementada una regresión local por anomalías, pero resuelve
otro problema: usa `tmin` del día objetivo (§1). Para este benchmark hay que **reformularla con
entradas causales** — misma estructura, mismas climatologías, sólo lags — y documentar cómo se
obtiene esa versión unilateral. No comparar un suavizado retrospectivo, ni el modelo de producción
tal cual, contra el modelo causal: son tareas distintas con información distinta, y la comparación
no sería informativa en ninguna dirección. Si se reporta el modelo de producción como contexto,
declarar explícitamente esa asimetría de información.

En T0–T3 proporcionar los mismos metadatos permitidos a la salida/consulta; en T2 sólo se retiran
del generador del kernel, de modo que T3−T2 mida condicionar la curva y no simplemente agregar
ubicación. Aplicar el mismo principio a S1 y S2.

Orden: B0–B2b y la medición de §5.1 primero; después T0–T3; luego M1; S0–S2 sólo si la regla de §5.2
lo autoriza; Z1 y E1 al final. No ejecutar toda la matriz con todas las ventanas, pérdidas y
semillas a la vez.

---

## 10. Entrenamiento y presupuesto

AdamW, tasa 3×10⁻⁴, weight decay 10⁻⁴, dropout 0.1, recorte de norma de gradiente a 1. Precisión
mixta sólo si el hardware la admite de forma estable. Lote inicial de dos parches; aumentar tras
medir memoria. Registrar lote efectivo si hay acumulación de gradientes.

Ciclo piloto: hasta 20,000 pasos, validación cada 1,000, parada tras cinco validaciones sin mejora.
Son límites operativos; si las curvas muestran subentrenamiento, ampliar el presupuesto de manera
comparable para todos los finalistas. No interpretar una prueba corta como evidencia definitiva
contra una arquitectura.

Una semilla para depuración y cribado; tres semillas para finalistas y sus controles. Seleccionar el
checkpoint por el promedio de MSE estandarizado de los canales y horizontes definidos previamente;
conservar todos los resultados desagregados. El barrido de L se hace después del cribado
arquitectónico, con entrenamiento nuevo por configuración.

Entrenar con un subconjunto de parches geográficamente distribuido (100–300 si la memoria lo
permite), con diversidad de estaciones y años, muestreando también regiones raras y reportando su
cantidad efectiva. Mantener todos los años de entrenamiento como fuente del muestreo.

El benchmark principal evalúa fechas retenidas en ubicaciones conocidas. Si además interesa
generalizar a ubicaciones nunca supervisadas, crear un benchmark distinto con bloques geográficos
reservados y halos separados. No mezclar los dos objetivos en una cifra.

---

## 11. Escala y acceso a datos

Cifras reales medidas en disco:

| Concepto | Valor |
|---|---|
| Fuente NetCDF, canales diarios 1981–2016 (`td`,`sd`,`tmin`,`tmax`,`eo` v1.1) | ~493 GB |
| Fuente NetCDF, PISCOt v1.2 `tmin`+`tmax` 1981–2020 | 112 GB |
| Extracción a parquet ya hecha: `td` + `tmin_v12` en malla 2.8M | **398 GB** |
| Días del período común (1981–2016) | 13,149 |
| Celdas válidas por día | 2,178,827 de 2,818,404 |
| 4 canales × 13,149 días × 2.82 M celdas × float32 | ~593 GB sólo valores |

No materializar todas las ventanas ni cargar el dataset completo en RAM. Lectura por bloques de
tiempo y espacio, en un formato adecuado al patrón de acceso — Zarr o NetCDF con particiones — pero
**no convertir los datos completos antes de medir un piloto**. El proyecto ya tiene todo indexado por
`ID` en parquet; el costo de conversión es real y hay que medirlo contra el beneficio.

Compartir pesos entre ubicaciones y procesar parches. Evitar atención espacial global entre los
2.8 M de puntos: son ~8×10¹² pares por cabeza y fecha antes de la dimensión temporal.

Registrar tiempo por lote, porcentaje de tiempo en lectura, uso máximo de GPU/RAM, tamaño de
checkpoint y costo de inferencia por fecha. Extrapolar al dominio completo con esas medidas.

Para inferencia en malla, usar mosaicos con halo y conservar los núcleos. Comprobar que las
predicciones coinciden al cambiar el origen del mosaico.

---

## 12. Evaluación

Reportar MAE, RMSE y sesgo **en unidades originales por canal y horizonte** (°C para `td`,
`tmin`, `tmax`; h/día para `sd`; mm para `pc`). Agregar habilidad relativa frente a persistencia,
climatología y B2, indicando qué métrica se usa y tratando explícitamente los denominadores cero.
No presentar una sola cifra que mezcle grados, horas y milímetros.

Desagregar por:

- costa / sierra / selva y estratos de elevación;
- estación del año;
- las 41 clases de la cartografía auditada;
- **dentro de Perú vs región de fallback de zona** (§2.6) — obligatorio, son el 49 % y el 51 % del
  campo respectivamente;
- proximidad a estación: distancia a la estación PISCOt más cercana, en estratos. Si el error crece
  monótonamente con esa distancia, el modelo está aprendiendo el interpolador más que el clima, y
  eso debe decirse.

Presentar promedio por área y, por separado, promedio entre regiones. Informar el número de días y
puntos válidos detrás de cada resultado.

La incertidumbre se calcula con remuestreo por bloques temporales (30 días como inicio) y espaciales
(mayores que el campo receptivo), con sensibilidad al tamaño de bloque. No suponer independientes
miles de millones de celdas-día.

Guardar las curvas K(j) separadas de los pesos finales a(j). Su forma puede variar por lugar,
estación, horizonte y cabeza. La red puede compensar un sesgo temporal con los puntajes de
contenido: no hay identificación única garantizada. Los pesos de atención no son coeficientes de
correlación ni pruebas de causalidad.

Para evidencia sobre uso del espacio, la comparación primaria es contra el modelo **reentrenado** sin
vecinos. Una perturbación de vecinos sobre un modelo ya entrenado es sólo un diagnóstico.

---

## 13. Pruebas de corrección obligatorias

1. **Prueba de causalidad, sin excepciones.** Alterar cualquier observación posterior al corte t —
   de cualquier canal, incluida la del propio día objetivo — no modifica la predicción. Ejecutarla
   sobre todos los canales, no sólo sobre el que se está mirando. Esas observaciones no deben
   aparecer en entradas, imputaciones, máscaras ni estadísticas calculadas al vuelo.
2. Objetivos y ventanas alineados: distinguir t, t+ℓ y acumulados diarios.
3. Restar climatología y escalar, luego invertir ambas operaciones, reconstruye el dato observado
   dentro de tolerancia numérica.
4. En una fila de atención con datos válidos, los pesos suman uno; posiciones excluidas pesan cero;
   filas totalmente inválidas activan el respaldo sin NaN.
5. Los parámetros del generador de kernel reciben gradientes y cambian. K≈1 inicial reproduce la
   atención base si el resto de parámetros es idéntico.
6. Un lote pequeño puede sobreajustarse como prueba del flujo; no se reporta como desempeño.
7. Metadatos, máscaras y canales comparten coordenadas, orientación y unidades. **Verificar
   explícitamente que la fila 0 es lat = 1.22 (norte) en todos los arreglos**: los NetCDF tienen
   latitud descendente y el `grid_index.parquet` sigue esa convención. No rotar imágenes
   meteorológicas como aumento genérico.
8. Repetir inferencia de un mismo núcleo con halo válido no altera la salida.
9. `eo` recalculado desde los canales **observados** 1981–2016 reproduce el `eo` publicado dentro de
   tolerancia. Si no, la implementación de Penman-Monteith está mal y E1 no significa nada.
10. La máscara de intersección entre canales (§2.1) se aplica de forma idéntica en todos los modelos
    comparados.

---

## 14. Entregables y criterios de decisión

1. **Primero:** el variograma / descomposición de escala de §5.1, con la recomendación de §5.2. Éste
   es el primer entregable y condiciona todo lo demás.
2. **Segundo:** B0, B1, B2, B2b — las referencias causales, incluida la reformulación causal de la
   regresión local por anomalías.
3. Recién entonces, T0–T3, M1 y lo que §5.2 autorice.

Cada entrega incluye: configuración reproducible con semilla e índice de bloques; transformaciones y
climatologías ajustadas sólo con entrenamiento; comandos para reproducir cada corrida; tabla por
experimento, canal, horizonte y región con tiempo, memoria y cantidad de datos evaluados; curvas de
entrenamiento/validación; tres semillas en finalistas; controles de corrección de §13; mapas de
error; y las curvas de kernel claramente diferenciadas de los pesos finales.

**Recomendación final exigida:** conservar o retirar el kernel, conservar o retirar el componente
espacial, ampliar o mantener L, y si el modelo multicanal supera a modelos independientes por canal
— cada una con evidencia de validación y confirmación en test.

**No se exige que el modelo neuronal gane.** Encontrar que una regresión local causal ya es
competitiva, o que la geometría del producto no sostiene un codificador espacial, resuelve la
pregunta experimental igual de bien y a mucho menor costo.

Promover un componente sólo cuando mejore a su control comparable de manera consistente entre
semillas y a un costo aceptable. Acordar antes de abrir test la tolerancia a deterioros por canal y
región. Una diferencia menor que la variabilidad entre corridas no prueba una mejora.

**No se exige que el kernel gane.** Encontrar que la regresión local en producción ya es competitiva,
o que la geometría del producto no sostiene un codificador espacial, resuelve la pregunta
experimental igual de bien y a mucho menor costo.

**Primer resultado útil esperado:** una comparación reproducible entre las referencias causales, la
atención temporal estándar y la atención con kernel aprendido, sobre los canales de 0.01° en
1981–2016, con información estrictamente anterior al corte y evaluación separada por años y
regiones. El entrenamiento a escala nacional y la variante espacial se justifican después de esa
comparación.

---

## 15. Referencias

- [Shaw et al., Self-Attention with Relative Position Representations](https://aclanthology.org/N18-2074/) — mecanismo de representación relativa; antecedente conceptual.
- [Press et al., ALiBi](https://arxiv.org/abs/2108.12409) — penalizaciones de distancia en puntajes; el sesgo lineal original no es el kernel libre condicionado aquí propuesto.
- [Sukhbaatar et al., Adaptive Attention Span](https://arxiv.org/abs/1905.07799) — aprendizaje del alcance.
- [Lam et al., GraphCast](https://arxiv.org/abs/2212.12794) — antecedente espacial con grafos; otros datos, escala y recursos.
- [Shi et al., ConvLSTM](https://arxiv.org/abs/1506.04214) — estructura espacial y temporal en precipitación a corto plazo.
- [Hwang et al., Improving Subseasonal Forecasting in the Western U.S. with Machine Learning](https://arxiv.org/abs/1809.07394) — inspiración del modelo de regresión local que el proyecto ya tiene en producción.
- Huerta, A. et al. (2023). *High-resolution grids of daily air temperature for Peru – the new PISCOt v1.2 dataset.* Scientific Data 10, 847. https://doi.org/10.1038/s41597-023-02777-w
- PISCOeo_pm — *A reference evapotranspiration gridded database based on FAO Penman-Monteith in Peru during 1981-2016*, colección Figshare (fuente de `td`, `sd`, `ws`, `eo`).

Las elecciones de arquitectura, ventanas, particiones e hiperparámetros son propuestas
experimentales específicas para este proyecto. No se presentan como configuración publicada ni
validada sobre estos datos.

---

## Apéndice A — Cómo se verificó cada cifra

| Afirmación | Verificación |
|---|---|
| Malla 1982×1422, 100 % densa, `ID` = scan raster | `grid_index.parquet` de `td` y `tmin_v12`: unicidad de lat/lon, paso constante, residual al retículo, `ID == fila·1422 + col` |
| Máscara 77.31 %, idéntica entre canales | `np.isfinite` sobre un corte temporal de cada NetCDF |
| Grilla de papa ⊂ malla 2.8M | 302,449/302,449 celdas dentro del rectángulo, 100 % con `td` válido |
| Períodos por canal | conteo de archivos y años en `_raw/`, y coordenada temporal de cada NetCDF |
| `ws` es normal mensual | `ws_mean.nc`: dimensión `time` = 12, un solo archivo de 11 MB |
| `pc` nativo 0.10° | `PISCOp_daily.nc`: 198×133, paso 0.1000, `z` = 14,244 días = 1981-01-01 a 2019-12-31 |
| 302 estaciones | `_raw/v1_2/stations/xyz_qc_gf_hmg.csv`: 302 filas; 241 con `filter_qc`=1; 48 con `filter_qc70`=1 |
| Tabla de escalas de §2.5 | suavizado por ventana k×k con normalización por máscara, sobre `td` 1981-01-16 y su tendencia a 1981-01-17. **Un solo día — debe rehacerse con el protocolo de §5.1 antes de tomarlo como definitivo** |
| `eo` es función de los demás canales | README original de PISCOeo_pm: construido a partir de tmax, tmin, td, brillo solar y viento vía FAO Penman-Monteith |
| 41 clases de zona | auditoría previa del proyecto contra la cartografía oficial de SENAMHI |
