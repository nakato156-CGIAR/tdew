# Notas sobre el preentrenamiento de TimesFM y la posible exposición a PISCO o a series meteorológicas peruanas (bead tdew-ddx)

Fecha de consulta: 2026-10-23. Un revisor preguntó si TimesFM pudo ver PISCO o series meteorológicas peruanas durante el preentrenamiento. Este documento reúne lo que la documentación pública permite afirmar, lo que no documenta, el mecanismo con que el repositorio entrega las covariables y dos párrafos propuestos para el manuscrito. Las citas literales provienen de las fuentes primarias citadas; el texto fue elaborado con ayuda de IA generativa (Claude) y requiere revisión por una persona experta antes de pasar al manuscrito. Los resúmenes automáticos de páginas web se contrastaron con el texto crudo (README del Hub, README de GitHub, HTML del blog, PDF de los artículos, API del Hub).

## 1. Qué está documentado sobre el corpus de preentrenamiento

### 1.1 Artículo original (TimesFM de 200M, 2023–2024)

Fuente: Das et al., arXiv 2310.10688 (ICML 2024), sección «Pretraining Details», PDF leído en texto completo (https://arxiv.org/abs/2310.10688; `das2024` en `references.bib`).

- «sourcing the bulk of data used to train our models from three major sources: Google trends, Wiki Pageview statistics and synthetic time-series.»
- Google Trends: «around 22k head queries» de 2007 a 2022, en granularidades horaria, diaria, semanal y mensual, «roughly 0.5B time-points».
- Wiki Pageviews: «from Jan. 2012 to Nov. 2023 [...] The final corpus contains roughly 300B time-points.»
- Sintéticos: «3M synthetic time-series each of length 2048 time-points» (generadores ARMA, estacionales, tendencias, escalones).
- Otras fuentes reales: «We add all the granularities of the M4 dataset, the hourly and 15 minute Electricity and the hourly Traffic datasets (see [ZZP+ 21]). We also add the 10-minute granularity Weather dataset used for evaluations in [ZZP+ 21].» Además, series de tráfico de 15 minutos de otra fuente.
- Mezcla: «The training loader samples 80% real data and 20% synthetic».
- Evaluación fuera de muestra: «These datasets have been intentionally held out from our pretraining data» (Monash, Darts, ETT); en ETT el texto aclara que «A few of these datasets are used in pretraining, so we focus on the other datasets in this collection (ETTm1, ETTm2, ETTh1 and ETTh2)».

El conjunto «Weather» de este artículo es el de Zhou et al. (2021, Informer/Autoformer), 21 indicadores meteorológicos de una estación de Alemania cada 10 minutos. Esa procedencia no la afirma el artículo de TimesFM; es conocimiento externo y no se verificó aquí. El artículo no menciona ERA5, reanálisis, GHCN, ISD ni productos grillados. Los datos de series peruanas no aparecen.

### 1.2 TimesFM 2.0 y 2.5

- TimesFM 2.0 (500M): la ficha de https://huggingface.co/google/timesfm-2.0-500m-pytorch no tiene sección de datos; remite al artículo de 2023.
- TimesFM 2.5 (200M): la ficha https://huggingface.co/google/timesfm-2.5-200m-pytorch dice «`timesfm-2.5-200m` is pretrained using» GiftEvalPretrain, Wikimedia Pageviews (corte nov. 2023), Google Trends top queries (corte fin de 2022) y «Synthetic and augmented data.»

### 1.3 TimesFM 3.0 (checkpoint de este repositorio)

Checkpoint `google/timesfm-3.0-pytorch`, revisión `43046b85ec22d584a13f8098c2ed39c889e129c2` (`experiments/timesfm/variants.py:17-20`). Ficha: https://huggingface.co/google/timesfm-3.0-pytorch (README crudo):

> timesfm-3.0 is pretrained using
> - GiftEvalPretrain excluding the datasets that overlap with fev-bench
> - Wikipedia Pageviews, cutoff Nov 2023 (see paper for details).
> - Google Trends top queries, cutoff EoY 2022 (see paper for details).
> - Synthetic and augmented data.

El blog de lanzamiento (Jain y Sen, 2026-08-31; https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/; `jain2026timesfm3blog`) añade solo: «330 million parameters and is pre-trained on a real-world and synthetic time-series corpus comprising more than 1 trillion time points.» No enumera fuentes, no habla de contaminación, y no cita un artículo propio de la versión 3.0; la ficha remite todavía al artículo de 2023. El README de GitHub (https://github.com/google-research/timesfm) no contiene declaración sobre datos de preentrenamiento.

### 1.4 Contenido de GiftEvalPretrain: hay datos climáticos grillados

`GiftEvalPretrain` es el conjunto de Salesforce (https://huggingface.co/datasets/Salesforce/GiftEvalPretrain; `aksu2024`). Su ficha dice: «71 univariate and 17 multivariate datasets, spanning seven domains and 13 frequencies, totaling 4.5 million time series and 230 billion data points. Notably this collection of data has no leakage issue with the train/test split» (de GIFT-Eval). El listado de archivos del repositorio en el Hub (API, consultada 2026-10-23, `lastModified` 2025-01-21, sha `6830b624de7ed2b3d3e5b85bb6959d81dcc5d874`) incluye, entre 152 carpetas, estas de dominio climático:

- `era5_1989` a `era5_2018` (un directorio por año, 30 años);
- `cmip6_1850` a `cmip6_2010` (cada 5 años; simulaciones de modelos climáticos, no observaciones);
- `oikolab_weather`, `weather` y `subseasonal`, `subseasonal_precip`.

La descripción de esas series está en el artículo de Moirai (Woo et al., arXiv 2402.02592, apéndice sobre LOTSA, `woo2024`) y en la tabla 14 de GIFT-Eval: ERA5, dominio «Climate», frecuencia horaria, 245.760 series, 45 variables, 2.146.959.000 puntos; CMIP6, 6 h, 1.351.680 series, 53 variables. Cita literal del apéndice de Moirai: «The ERA5 and CMIP6 datasets provide time series of various climate related variables such as temperature, and humidity and various pressure levels, based on a grid structure. We use the 2.8125° resolution which contains time series in a 64 × 128 grid.» Los metadatos de `era5_2000` en el Hub muestran 8.192 ejemplos de 45 canales cada uno (64 × 128 = 8.192), de modo que cada año recorre la grilla global completa. Que esa grilla incluya celdas sobre Perú es una deducción geométrica (la grilla es global), no una afirmación de las fuentes.

Esto contradice la expectativa de que «no hay ningún dato climático en el corpus»: para el checkpoint 3.0, si la ficha se lee literalmente, el corpus contiene reanálisis ERA5 horario de 1989 a 2018 a 2,8125°, con variables que incluyen temperatura y humedad. Tres salvedades:

1. La ficha dice «excluding the datasets that overlap with fev-bench», y no lista cuáles se excluyeron. No se puede afirmar ni descartar que `era5_*` o `weather` hayan quedado fuera. En el texto de fev-bench (Shchur et al., arXiv 2509.26468, `shchur2025`) no aparece la cadena «ERA5»; esa ausencia no prueba que ninguna tarea use ERA5 con otro nombre.
2. Lo que la ficha nombra es el conjunto Salesforce, no la lista de tablas efectivamente muestreadas ni sus pesos en la mezcla.
3. ERA5 a 2,8125° y a 1 h no es PISCO. PISCO es un producto interpolado desde estaciones a 0,1° (referencia disponible en el repositorio: `huerta2022`, PISCOeo_pm; no existe ficha propia del producto Td v1.1, ver `bib_verificacion.md` §3). Si PISCO usa algún reanálisis como covariable de su interpolación de Td no se verificó. El solapamiento temporal de ERA5 (1989–2018) con los bloques evaluados (2009–2016, y 2017–2018 dentro del bloque 2017–2020) existe, de modo que una exposición indirecta a la misma atmósfera (a otra resolución, otras variables y otra frecuencia) no puede excluirse.

Contra la hipótesis de memorización específica: la entrada de TimesFM es una serie univariante de anomalías o Td de una celda, sin coordenadas ni identificador; no hay mecanismo documentado para que el modelo reconozca «la celda de Cusco». Esto es un argumento de plausibilidad, no una prueba.

## 2. Contaminación de evaluación y benchmarks reservados

- Artículo de 2023: los conjuntos de evaluación se declaran reservados («intentionally held out») para Monash e Informer-ETT, con la excepción de los ETT señalada arriba. No hay enunciado sobre datos peruanos ni de PISCO.
- GIFT-Eval (`aksu2024`, apéndice F.2): «there is a partial data leakage issue when these models are evaluated against our GIFT-Eval»; en el cuerpo del texto se nombra explícitamente a TimesFM: «pre-training datasets of TimesFM, Chronos, and Moirai exhibit partial data leakage issues for GIFT-Eval». Para Moirai miden el efecto («data leakage from training sets can boost performance on the corresponding test sets, with this effect becoming more pronounced as prediction length increases»). Esa advertencia se refiere a versiones previas de los modelos; la ficha de 3.0 declara usar la partición sin fuga de GiftEvalPretrain.
- fev-bench (`shchur2025`): la fuga se maneja por autoinforme: «contributors must report, for each model–task pair, whether any part of the dataset at the same frequency was used during training»; los autores reconocen que «more subtle forms of leakage may remain difficult to detect» y que se apoyan en el autoinforme «as a practical safeguard».
- Blog y ficha de 3.0: sin enunciado de contaminación más allá de la exclusión por solapamiento con fev-bench.

Qué no está documentado: la lista exacta de series de entrenamiento de 3.0; los pesos de mezcla; si ERA5 o CMIP6 entraron; cómo se filtró el solapamiento con fev-bench; cualquier verificación sobre Perú, PISCO o SENAMHI. Tampoco existe, según lo encontrado, una auditoría independiente de contaminación de TimesFM 3.0 con datos climáticos.

## 3. Mecanismo de covariables y decodificación del horizonte

Paquete instalado: `timesfm` 3.0.2 (módulo `timesfm3`, `.venv/lib/python3.13/site-packages/timesfm3/`; licencia Apache-2.0 del código, pesos bajo licencia no comercial).

### 3.1 Corrección de supuesto: no es XReg

La consulta planteaba «XReg: regresión lineal en contexto sobre las covariables combinada con la predicción del modelo». Eso corresponde a TimesFM 2.5. El README de GitHub dice: «Added back the covariate support through XReg for TimesFM 2.5» (actualización del 29-oct-2025). Para 3.0 el mismo README (actualización de agosto de 2026) dice: «native support for past-only and past-and-future dynamic covariates without per-task tuning». El blog describe el mecanismo: las covariables solo pasadas se tratan como series adicionales; para las covariables pasadas y futuras, «each token concatenates the current patch with future patches, allowing the model to peek at upcoming known signals», y hay atención entre series («Tokens attend vertically across series»). No hay mención de XReg para 3.0 en esas fuentes, ni en el código revisado (`grep` sin resultados en `experiments/timesfm/` ni en `timesfm3/`). Cualquier texto del repositorio que describa la covariable de 3.0 como «regresión lineal sobre residuales» es incorrecto; la revisión de `reports/paper_nuevo/` no encontró esa descripción (la búsqueda de «XReg» no dio resultados).

### 3.2 Entrega de la covariable en este repositorio

- `experiments/timesfm/variants.py:75-110`: `tmin_anom_full` usa objetivo `TD_anom`, covariable `TMIN_anom`, contexto desde 1981. La docstring (líneas 8-11) justifica que la covariable sea solo Tmin.
- `experiments/timesfm/run.py:121-167` (`build_inputs`): el contexto es la anomalía de Td del bloque de contexto (o Td cruda); cada covariable se construye como la concatenación del tramo de contexto y del tramo del horizonte (`np.concatenate([...tmin_ctx, ...tmin_hold])`, y para anomalías con la climatología). El ancho de la covariable debe ser contexto + horizonte (líneas 158-166); la docstring (líneas 123-125) advierte que ese ancho define el horizonte «sin validación alguna» (`timesfm3/torch/model.py:395-396`).
- `experiments/timesfm/run.py:222-246` (`_predict_chunk`): llama a `model.predict_batch(contexts=..., horizon=..., past_future_covariates=..., make_positive=False, padding_mode="none", ...)`. Se entrega como `past_future_covariates` (conocida en el horizonte), no como `past_only_covariates`. `make_positive=False` evita el recorte a cero que afectaría los valores negativos de Td en Cusco (comentario en la línea 236). `autoregressive` de `Variant` (`variants.py:31`) está fijado en `False` y solo se escribe en la procedencia (`run.py:92`); no controla ningún despliegue recursivo del modelo.
- `experiments/timesfm/run.py:215-217`: carga con `TimesFM3Forecaster.from_pretrained(spec.checkpoint, device=..., revision=CHECKPOINT_REVISION)`.

### 3.3 Qué ocurre dentro del modelo (código de `timesfm3/torch/model.py`)

- Las covariables pasadas-futuras entran como canales (variates) adicionales con las series objetivo: se concatenan al contexto (`model.py:454-467`) y sus valores futuros ocupan la región del horizonte (`model.py:547-570`); los canales objetivo ocupan el horizonte con ceros y máscara verdadera (`model.py:526-545`). Si `use_linear_detrending` está activo (config del checkpoint: `true`, umbral 0,5), se ajusta y resta una tendencia lineal por canal, y se extrapola la de las covariables futuras (`model.py:472-524`, `552-570`).
- Cada parche de entrada se concatena con los parches futuros por «roll» (`model.py:240-250`, preprocesamiento).
- El bloque transformador tiene atención secuencial y, con `use_variate_attention` activo (config del checkpoint: `true`), atención entre variates por parche (`timesfm3/torch/transformer.py:441-452`, `516-530`), con un máximo de 32 variates (`max_variates`, `config.json`). Así la covariable influye en la predicción de Td a través de esa atención, no por una regresión explícita.
- La salida son 9 cuantiles (0,1 a 0,9); la predicción puntual es la mediana (`timesfm3/torch/timesfm3_forecaster.py`, `predict_batch`, línea 465 y siguientes; `forecast=raw[:horizon, median_quantile_index]`).

### 3.4 Decodificación de un horizonte de 1.461 días

`TimesFM3Torch.decode` se documenta como «Non-autoregressive single-pass decoding for TimesFM3» (`model.py:364-376`, docstring en la línea 376). El horizonte se infiere del ancho de la covariable (`model.py:395-396`). Con `use_stitching=true` (config del checkpoint; `model.py:434-440`, `613-625`), parche de entrada 32 y de salida 64: `extract_len = min(2·32, 64) = 64` (`model.py:144`), solapamiento 32, y se extraen `ceil((1461 − 32)/32) = 45` parches de pronóstico, que se unen por interpolación lineal en las zonas de solapamiento (`timesfm3/torch/util.py`, `stitch_patches`, líneas 337-367). El horizonte se rellena a 1.472 (46 parches de horizonte, incluidos `rolls − 1`). Todo ocurre en una sola pasada hacia adelante. El horizonte, así, no se genera por realimentación de las propias predicciones. Cada parche de horizonte se predice condicionado al contexto y a las covariables futuras de la ventana; la dependencia de largo plazo en el horizonte pasa solo por la atención del contexto. No se encontró en la documentación un horizonte máximo declarado para 3.0 (el README de GitHub atribuye «up to 1k horizon» a la cabeza de cuantiles de 2.5). El contexto máximo del código es 15.360 puntos (`_MAX_CONTEXT_LENGTH`, `timesfm3_forecaster.py:32`; `global_context`, línea 363), con truncamiento a los puntos más recientes; los contextos del benchmark de 11.688 días (1981–2012) caben sin truncar. El horizonte de 1.461 días (4 años) supera el rango sobre el cual la documentación muestra resultados; no se encontró validación del modelo en horizontes de esa magnitud ni a escala diaria.

## 4. Qué se puede saber y qué no

Con los datos existentes no puede construirse una prueba libre de sospecha sobre exposición a PISCO o a ERA5. La pertenencia exacta de series al corpus no es observable: los pesos y la lista de tablas muestreadas no son públicos, y no se dispone de una versión del modelo entrenada sin esos datos para contrastar. Sí se sabe, por documentación, cuáles son las fuentes declaradas (sección 1) y que entre ellas hay reanálisis a otra resolución. Sí es observable el comportamiento del modelo ante manipulaciones de la entrada, y ese resultado no prueba ausencia de exposición: el control de Tmin barajada en el horizonte ya está en el repositorio (`experiments/timesfm/run.py:103`, `control_tmin_barajada_eval.py`) y mide dependencia de la covariable, no memorización. La única diligencia de bajo costo que no exige experimentos nuevos es declarar la limitación, citar la ficha y reconocer que la ausencia de PISCO en el corpus documentado no equivale a su ausencia en el corpus real. Un diseño que sí discriminaría (no ejecutado aquí) compararía el desempeño sobre años de PISCO anteriores y posteriores al corte de 2018 de ERA5, y en regiones sin cobertura de estaciones peruanas; su interpretación seguiría dependiendo de supuestos sobre el corpus.

## 5. Párrafo propuesto para Límites

La documentación pública del checkpoint usado (`google/timesfm-3.0-pytorch`) declara que se preentrenó con GiftEvalPretrain, excluidos los conjuntos que se solapan con fev-bench, más visitas de Wikipedia, consultas de Google Trends y datos sintéticos. GiftEvalPretrain contiene series climáticas grilladas, entre ellas ERA5 horario de 1989 a 2018 a 2,8125° y simulaciones CMIP6. La ficha no enumera las series efectivamente incluidas ni sus pesos, y no existe un artículo específico de la versión 3.0. Por eso no puede descartarse que el modelo haya visto atmósfera correspondiente a Perú en el periodo de los bloques evaluados, aunque no se documenta que haya visto PISCO, productos de SENAMHI ni series de estaciones peruanas. La exposición, de existir, sería a otra variable, otra resolución y otra frecuencia, y el modelo no recibe coordenadas ni identificadores de celda. Esa plausibilidad no equivale a una prueba, y la comparación con `tuned` y con las LLR debe leerse con esa limitación: el estudio no puede separar la habilidad del modelo en una serie nueva de una familiaridad con la dinámica atmosférica de los datos de preentrenamiento. Los resultados no se interpretan como evidencia de generalización a regiones o variables sin cobertura en el corpus.

## 6. Párrafo propuesto para Métodos

TimesFM 3.0 se usó sin ajuste de pesos, con el checkpoint `google/timesfm-3.0-pytorch` en la revisión `43046b85ec22d584a13f8098c2ed39c889e129c2` (330 710 976 parámetros) y el paquete `timesfm` 3.0.2. Cada celda se trató como una serie independiente. El contexto fue la anomalía diaria de Td respecto de la climatología de Palacios, desde 1981 hasta el inicio del bloque, y la Tmin (también en anomalía) se entregó como covariable conocida en el horizonte, mediante el argumento `past_future_covariates`. En la versión 3.0 las covariables entran como canales adicionales que el modelo procesa con atención entre series, sin la regresión lineal en contexto (XReg) de la versión 2.5. El horizonte, de 1 461 días (cuatro años), se decodifica en una sola pasada, no autoregresiva, con parches de salida de 64 días que se empalman por interpolación lineal; el ancho de la covariable (contexto más horizonte) fija el horizonte. La predicción puntual es la mediana de nueve cuantiles. Se desactivó el recorte a valores no negativos, porque Td es negativa en parte de Cusco. El contexto máximo del código es 15 360 días y ningún contexto lo superó.
