# Limitaciones de TimesFM medidas o verificadas en el código

Cada punto de este documento remite a una línea del paquete instalado
(`timesfm` 3.0.2, importable como `timesfm3`, en `.venv/lib/python3.13/site-packages/`)
o a una medición hecha en esta estación de trabajo. Ninguno proviene de la
documentación del modelo ni de una impresión de uso. Las rutas se dan relativas a
`site-packages/`.

Varias de estas limitaciones no producen error: cambian el resultado en silencio.
Esa es la razón de escribirlas.

## 1. No existe indicador de frecuencia ni conciencia de calendario

`grep -rni "freq" timesfm3/` no devuelve un solo acierto. No hay argumento de
frecuencia, de estacionalidad ni de fecha en `predict`, `predict_batch`, `decode`,
`ModelConfig` ni en el `config.json` del checkpoint. El README del paquete lo
registra como decisión deliberada: TimesFM 2.5 "gets rid of the frequency
indicator" y 3.0 no lo reintrodujo.

Para una serie diaria con ciclo anual, la única forma de que el modelo perciba la
estacionalidad es que el período quepa en el contexto, porque la información
posicional entra por RoPE sobre índices de parche
(`use_rope_seq=True`, `timesfm3/torch/transformer.py:105-148`). Si se quiere un
efecto de día del año explícito, hay que construirlo a mano y entregarlo como
covariable. La variante `tmin_doy_td_full` de este benchmark existe para medir
cuánto vale hacerlo.

## 2. Los cuantiles llegan solo hasta el decil: el intervalo más ancho es del 80 %

`ForecastOutput.quantiles` trae nueve niveles, 0,1 a 0,9
(`timesfm3/torch/timesfm3_forecaster.py:54-56`, confirmado en el `config.json` del
checkpoint descargado). Alcanza para la pérdida pinball en esos nueve niveles y
para una aproximación del CRPS por cuadratura, pero no hay q05 ni q95, de modo que
no se puede reportar cobertura al 90 % ni al 95 %. Tampoco existe una cabeza
continua ni muestreo: el CRPS que se reporta aquí como `crps_aprox` ignora las
colas por debajo de q10 y por encima de q90, y queda sesgado a la baja.

## 3. El ancho de la covariable futura redefine el horizonte, sin validación

Cuando se pasan `past_future_covariates`, `decode` reescribe el horizonte a partir
del ancho del arreglo: `horizon = past_future_covariates.shape[-1] - context`
(`timesfm3/torch/model.py:395-396`). Nada comprueba que ese valor coincida con el
horizonte pedido; la prueba del propio paquete
(`timesfm3/torch/timesfm3_forecaster_test.py:262-281`) documenta el caso. Un
arreglo mal dimensionado cambia cuántos días predice el modelo y el recorte final
devuelve menos filas, sin aviso.

En este benchmark la covariable se construye con longitud exactamente
`contexto + horizonte` y se verifica antes de cada llamada
(`experiments/timesfm/run.py`, función `build_inputs`). El control de la corrida
confirmó 1.461 días por celda, de 2013-01-01 a 2016-12-31.

## 4. Los huecos se rellenan por interpolación lineal, sin señal de dato faltante

Los pasos iniciales todo-NaN se recortan del objetivo y de las covariables a la vez
(`timesfm3_forecaster.py:512-523`); una serie enteramente NaN se convierte en ceros
(`:524-528`); el resto de los NaN, tanto del objetivo como de ambos tipos de
covariable, se rellena por interpolación lineal con respaldo en la media
(`:136-162`, invocado en `:530`, `:534`, `:540`). Después `forward` aplica
`torch.nan_to_num` y recorta a `value_clip=1e20` (`model.py:288-291`).

El modelo no recibe ninguna máscara de ausencia: un tramo interpolado le llega como
observación real. En el panel de este benchmark el riesgo no se materializa porque
la ausencia en `bucketed_training_data` es por celda entera —mar y borde— y nunca
por huecos parciales, lo que se comprobó celda a celda antes de armar el panel. En
otro conjunto de datos con huecos internos, la limitación sí importa.

## 5. El recorte de negativos está activado por defecto en el evaluador

`TimesFM3Evaluator` fija `make_positive=True` (`timesfm3/torch/evaluator.py:53-59`).
Con esa bandera, si el histórico de una serie no tiene valores negativos, la
predicción y **todos** los cuantiles se recortan en cero
(`timesfm3_forecaster.py:739-749`). El punto de rocío en Cusco es negativo buena
parte del año, así que el recorte destruiría tanto el valor central como la
calibración de los cuantiles bajos.

Todas las corridas de este benchmark usan `TimesFM3Forecaster` con
`make_positive=False`. El control correspondiente encontró 11.524 predicciones
negativas sobre 99.348 en las celdas de Cusco del panel de cribado (11,6 %), con un
mínimo de −6,83 °C: con el valor por defecto, esas 11.524 predicciones habrían sido
cero.

## 6. Un contexto demasiado largo se recorta en silencio

El límite es `_MAX_CONTEXT_LENGTH = 15360` (`timesfm3_forecaster.py:32`). Es una
constante de módulo, no un campo de configuración, de modo que solo se cambia
parcheando el paquete. Un contexto más largo no produce error ni advertencia: se
recorta por la izquierda, `targets = targets[:, -context_len:]`
(`timesfm3_forecaster.py:225-239`).

Para este proyecto el límite no aprieta —1981-2012 son 11.688 días— pero deja fuera
cualquier uso que quisiera entregar el registro diario completo 1981-2016 más un
horizonte largo sin darse cuenta del recorte.

## 7. Con más de 32 variates las covariables se descartan al azar

El modelo se entrenó con `max_variates = 32` (`timesfm3/torch/configs.py:55`) y el
código de `TimesFM3Forecaster` no lo hace cumplir: acepta más y opera fuera de
distribución. `TimesFM3Evaluator` sí lo aplica, pero submuestreando las covariables
al azar con semilla fija 42 (`evaluator.py:142-151`) y repartiendo los objetivos en
bloques (`:162-166`). Con `univariate=True`, además, las covariables se descartan
por completo, sin aviso (`evaluator.py:90-91`).

Este benchmark usa como mucho tres canales, así que el caso no se toca, pero es la
clase de comportamiento que hace que dos corridas aparentemente iguales devuelvan
resultados distintos.

## 8. El costo lo gobierna la longitud del contexto, no el tamaño del lote

Medido en la RTX A2000 de 12 GB, 45 combinaciones de contexto × horizonte × lote,
con covariable y cuantiles activados
(`reports/timesfm_benchmark/coste_throughput.csv`):

| contexto (días) | horizonte 366 d | horizonte 731 d | horizonte 1.461 d |
|---|---|---|---|
| 731 | 40,8 celdas/s | 32,4 | 21,1 |
| 4.018 | 10,5 | 9,9 | 9,2 |
| 11.688 | 3,9 | 3,4 | 3,2 |

El rendimiento satura entre lote 8 y 16: pasar de 8 a 16 mejora menos del 5 % en
todas las combinaciones. No hubo un solo desbordamiento de memoria y el pico fue de
2,39 GB sobre 12 disponibles, lo que indica que el cuello es de cómputo y no de
memoria; un lote mayor no compra nada en esta tarjeta.

El paquete no estima memoria antes de correr ni reduce el lote ante un
desbordamiento: `try_gc` (`timesfm3_forecaster.py:119-134`) solo limpia la caché
cuando la ocupación supera el 90 %, y un lote excesivo termina en un error de CUDA.
El retroceso automático se implementó aquí (`experiments/timesfm/run.py`,
`predict_panel`).

### Lo que sí acelera y lo que no, medido en esta tarjeta

Se probaron tres formas de ir más rápido y solo una funcionó.

**TF32 funciona: 1,44×.** PyTorch trae `float32_matmul_precision='highest'`, que
desactiva los núcleos TF32 de Ampere; la convolución sí los usaba por defecto
(`cudnn.allow_tf32` viene en `True`), pero la multiplicación de matrices no, que es
donde este modelo pasa casi todo su tiempo. Activarlo sobre 48 celdas con contexto
11.688 y horizonte 1.461 llevó la corrida de 28,4 s a 19,7 s. El precio es
numérico y está acotado: diferencia máxima de 0,0034 °C entre ambas precisiones y
RMSE de 0,00043 °C, que sobre el agregado mueve el RMSE del orden de 10⁻⁷ °C,
siete órdenes por debajo del efecto que este benchmark mide. Queda activado por
defecto, con `--no-tf32` para recuperar la numérica exacta anterior.

**Un lote mayor no funciona.** Con TF32 activo y un panel de 128 celdas, el lote 32
gana 2,5 % sobre el 16 y el lote 64 desborda la memoria. El barrido de costo ya lo
insinuaba: el rendimiento satura entre 8 y 16.

**Repartir el trabajo entre procesos concurrentes no solo no funciona: empeora.**
Tres procesos simultáneos rindieron 4,59 celdas/s agregadas, contra 5,39 celdas/s
de un proceso con la tarjeta para sí — un 15 % menos. El intento de levantar un
cuarto proceso terminó además en un desbordamiento al cargar el modelo. La causa está en los contadores del
propio dispositivo: `SW Power Cap` figura activo con 2,26 horas acumuladas de
recorte, el límite de potencia está en 70 W que es a la vez el valor por defecto y
el **máximo que admite el firmware** —el rango declarado es 10 a 70 W, de modo que
no hay margen que subir— y el reloj se sostiene en 1.627 de 2.100 MHz. Con la
tarjeta limitada por vatios y no por ocupación, repartir el trabajo entre procesos
no crea vatios nuevos. La opción `--shard i/n` quedó implementada y probada, porque
en una tarjeta que no esté limitada por potencia sí tendría sentido.

Consecuencia para el proyecto: el camino para acortar una pasada nacional no está
en la configuración del software, que ya está en su punto, sino en más hardware o
en el clúster. La temperatura sostenida de 83 °C sugiere además que mejorar la
refrigeración permitiría sostener relojes más altos dentro del mismo presupuesto de
70 W.

Extrapolando a contexto completo y horizonte de cuatro años: 90 minutos para las
17.041 celdas del backtest nacional, 38,5 horas para las 436.519 celdas de los
cuatro departamentos y unos 10,3 días para las 2,8 millones del grid nacional. Con
contexto de 4.018 días esa última cifra baja a unos 3,5 días. El método de Palacios
cubre el grid completo en 20 minutos (`$RES/tuning/b3_fill.log`).

## 9. Los pesos de la versión 3.0 no permiten uso comercial ni productivo

El código es Apache-2.0 (`timesfm-3.0.2.dist-info/licenses/LICENSE`, y cada archivo
fuente lleva la cabecera). Los pesos no. El README del paquete lo dice sin
ambigüedad: los pesos de TimesFM 3.0 se distribuyen bajo
`timesfm-non-commercial-license-v1.0` y quedan restringidos a uso no comercial y no
productivo, mientras que los de versiones hasta la 2.5 siguen siendo Apache-2.0.

El alcance de este benchmark es investigación, sin despliegue en producción ni
entrega a usuarios finales, condición bajo la cual la licencia permite el uso de
los pesos. Para entregar un producto Td 2017-2020 que alimente Simcast u otro
sistema en producción, habría que revisar de nuevo esta licencia con quien
corresponda en CIP; es una decisión de política de datos, no técnica.

El texto de la licencia de los pesos no queda en disco: la caché de Hugging Face
solo guarda `config.json` y `model.safetensors`, porque `from_pretrained` descarga
únicamente esos dos archivos.

## 10. El paquete instalado no permite ajustar el modelo

No hay bucle de entrenamiento, ni ejemplos, ni dependencia de `peft` o
`transformers`: `grep -rniE "finetun|lora|peft|adapter"` sobre `timesfm3/` y
`timesfm/` no devuelve nada, y el modelo de torch está marcado como solo inferencia
(`timesfm3/torch/model.py:15-21`, con `@torch.no_grad()` sobre `decode` en `:363`).
El ejemplo de LoRA que menciona el README vive en el repositorio de GitHub, no en
la rueda instalada, y está escrito contra TimesFM 2.5.

## 11. No es autorregresivo: no acumula deriva, pero tampoco se recondiciona

`decode` produce el horizonte completo en una sola pasada
(`timesfm3/torch/model.py:376`). Los pasos futuros entran como parches marcados y
en cero (`model.py:526-545`) y las predicciones por parche se cosen con un fundido
lineal de 32 pasos de solape (`model.py:612-625`, `util.py:337-380`). El modelo
nunca consume su propia salida como entrada.

La consecuencia tiene dos caras y conviene decirlas juntas: no hay realimentación
de error, que es el mecanismo por el cual un pronóstico autorregresivo se degrada
con el horizonte, pero tampoco hay recondicionamiento, de modo que el día 1.461 se
predice con la misma información que el día 1. El método de Palacios, en cambio, sí
es autorregresivo dentro del bloque oculto.

Un efecto práctico: el sondeo previo asumió un tope de horizonte de 1.000 días,
tomado de la ficha del modelo. En el código no existe tal tope. El horizonte se
redondea al múltiplo de 64 superior
(`timesfm3_forecaster.py:480-483`) y se recorta al final (`:757-764`); la única
excepción es `horizon <= 0`, que sí lanza error (`model.py:397-398`). Los 1.461 días
del bloque 2013-2016 salen en una sola pasada, sin partir ni realimentar.

## 12. El panel de comparación cubre 33 de las 41 zonas SENAMHI

La referencia vigente de Palacios (`$RES/tuning/backtest_clean`) tiene 17.027 celdas
y cubre 33 de las 41 zonas SENAMHI; el panel con fuga tocaba 38. Las cifras por zona
(`nacional_limpio/metrics_by_zone.csv`, el mapa de la página interactiva) no dicen
nada sobre las ocho zonas ausentes. Además, el 51,4 % de las celdas (8.755 de
17.027) cae fuera del Perú, porque el marco de muestreo del backtest usa la caja
envolvente del producto PISCO. El agregado nacional describe esa muestra y no un
promedio del territorio peruano (bead `tdew-214.8`).

Las tablas departamental y de escala usan un `tuned` con selección de recetas con
fuga y no son comparables con las cifras del nivel backtest limpio.
