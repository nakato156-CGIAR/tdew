# Verificación bibliográfica de `references.bib` (bead tdew-tpu)

Fecha de consulta: 2026-10-22. Se contrastaron los metadatos (autores, título, revista o actas, volumen, páginas, año, DOI) contra fuente primaria. No se leyó el texto completo de las obras nuevas: «verificada» significa que la ficha bibliográfica existe y coincide, no que la afirmación del paper esté respaldada. Antes de citar un resultado concreto hay que abrir el artículo. Las entradas copiadas de `reports/paper/references.bib` (Palacios) se reverificaron y llevan la marca `% origen:` en el `.bib`. Parte de la búsqueda se apoyó en IA generativa y debe validarse con expertos de la materia.

## 1. Entradas añadidas

Referencia a las secciones de `paper_narrative.md`: §3.1 (Td, PISCO, SENAMHI), §3.2 (trabajo previo, modelos de fundación, TimesFM, LLR), §3.3 (relación Td–Tmin, remuestreo, puntuación, ISD, ONI). La asignación de sección es propuesta, ya que el texto no trae marcas de cita.

| clave | referencia | fuente primaria consultada | estado | afirmación a la que sirve | nota |
|---|---|---|---|---|---|
| das2024 | Das, Kong, Sen, Zhou (2024). *A decoder-only foundation model for time-series forecasting.* ICML, PMLR 235:10148–10167 | https://proceedings.mlr.press/v235/das24c.html ; https://arxiv.org/abs/2310.10688 | verificada | §3.2: TimesFM como modelo de fundación | El artículo describe el modelo de 2023–2024 (200M); no el checkpoint 3.0 usado aquí. Ver sección 4 |
| timesfm3_checkpoint | Checkpoint `google/timesfm-3.0-pytorch`, revisión 43046b8… | https://huggingface.co/google/timesfm-3.0-pytorch (API del Hub, `config.json`, `LICENSE`) | verificada | §3.2 y reproducibilidad: versión exacta usada | 330.710.976 parámetros; licencia no comercial (sección 4) |
| ansari2024 | Ansari et al. (2024). *Chronos.* TMLR | https://jmlr.org/tmlr/papers/bib/gerNCVqqtR.bib ; https://arxiv.org/abs/2403.07815 | verificada | §3.2: otros modelos de fundación | TMLR sin volumen ni páginas; noviembre de 2024 según el listado de TMLR. La lista de autores es la de arXiv/TMLR (18) |
| woo2024 | Woo et al. (2024). *Unified Training of Universal Time Series Forecasting Transformers* (Moirai). ICML, PMLR 235:53140–53164 | https://proceedings.mlr.press/v235/woo24a.html ; https://arxiv.org/abs/2402.02592 | verificada | §3.2 | El nombre «Moirai» no figura en el título; se cita por su título oficial |
| rasul2023 | Rasul et al. (2023). *Lag-Llama* | https://arxiv.org/abs/2310.08278 | verificada (solo preprint) | §3.2 | No se confirmó versión en revista o congreso; se deja como `@misc` |
| garza2023 | Garza, Challu, Mergenthaler-Canseco (2023). *TimeGPT-1* | https://arxiv.org/abs/2310.03589 | verificada (solo preprint) | §3.2 | La ficha de arXiv lista tres autores con ese orden; se resuelve la duda de HANDOFF §7 sobre autores. Sin versión arbitrada confirmada |
| ansari2025 | Ansari et al. (2025). *Chronos-2* | https://arxiv.org/abs/2510.15821 | verificada (solo preprint) | §3.2: modelo con covariables nativas | La afirmación sobre covariables nativas no se comprobó en el texto |
| faw2025 | Faw, Sen, Zhou, Das (2025). *In-Context Fine-Tuning for Time-Series Foundation Models.* ICML, PMLR 267:16355–16374 | https://proceedings.mlr.press/v267/faw25b.html | verificada | §3.2: variante de TimesFM con contexto de series relacionadas | HANDOFF lo cita como «Faw et al. (2025)»: coincide |
| toner2025 | Toner et al. (2025). *Performance of Zero-Shot Time Series Foundation Models on Cloud Data* | https://arxiv.org/abs/2502.12944 | verificada (solo preprint) | §3.2: modelos zero-shot pueden quedar por debajo de líneas base simples | La afirmación de HANDOFF («quedan por debajo de un modelo lineal y de un naive estacional») no se comprobó en el texto; aplica a datos de nube, no a clima |
| hwang2019 | Hwang et al. (2019). *Improving Subseasonal Forecasting in the Western U.S. with Machine Learning.* KDD, pp. 2325–2335 | https://doi.org/10.1145/3292500.3330674 (Crossref); https://arxiv.org/abs/1809.07394 | verificada | §3.2: MultiLLR (arXiv:1809.07394 resuelta: Hwang, Orenstein, Cohen, Pfeiffer, Mackey) | Copiada de Palacios; se añadieron páginas |
| cleveland1979 | Cleveland (1979), *JASA* 74(368):829–836 | Crossref 10.1080/01621459.1979.10481038 | verificada | §3.2: regresión local ponderada | Opcional |
| cleveland1988 | Cleveland y Devlin (1988), *JASA* 83(403):596–610 | Crossref 10.1080/01621459.1988.10478639 | verificada | §3.2: regresión local | Opcional |
| huerta2022 | Huerta et al. (2022), PISCOeo_pm, *Sci. Data* 9:328 | Crossref 10.1038/s41597-022-01373-8; texto en https://www.nature.com/articles/s41597-022-01373-8 | verificada | §3.1: origen del producto Td PISCO | El resumen y la metodología del artículo mencionan Td entre las subvariables interpoladas. Es la referencia más cercana al producto Td, pero cita un producto de ETo; no se encontró ficha propia del Td v1.1 (sección 3). Se completaron los 7 autores (Palacios: «and others») |
| huerta2023 | Huerta et al. (2023), PISCOt v1.2, *Sci. Data* 10:847 | Crossref 10.1038/s41597-023-02777-w; https://www.nature.com/articles/s41597-023-02777-w | verificada | §3.1: producto Tmin (0,01°) | El artículo menciona LST MODIS (MOD11A2) y DEM como predictores, relevante para la discusión de insumos compartidos. No se verificó en texto completo el vínculo con el Td |
| aybar2020 | Aybar et al. (2020), PISCOp, *Hydrol. Sci. J.* 65(5):770–785 | Crossref 10.1080/02626667.2019.1649411 | verificada | §3.1: familia PISCO (precipitación) | Solo contexto; no es insumo del trabajo |
| tdew_estimation_repo | Centro Internacional de la Papa (2025). *tdew_estimation* (repositorio) | https://github.com/CENTRO-INTERNACIONAL-DE-LA-PAPA/tdew_estimation ; `gh api repos/CENTRO-INTERNACIONAL-DE-LA-PAPA/tdew_estimation` el 2026-10-23 | verificada | Disponibilidad de código: método de Palacios y producción | Propietario: organización CENTRO-INTERNACIONAL-DE-LA-PAPA; creado el 2025-12-17; último push 2026-10-12; sin licencia declarada; visibilidad privada en la fecha de consulta. Descripción de GitHub: estimación de Td con modelo de anomalías y regresión local para puntos de siembra de papa en Perú |
| tdew_paper_repo | nakato156-CGIAR (2026). *tdew* (repositorio) | https://github.com/nakato156-CGIAR/tdew ; `gh api repos/nakato156-CGIAR/tdew` el 2026-10-23 | verificada | Disponibilidad de código: figuras, tablas y cifras del artículo | Cuenta de usuario nakato156-CGIAR; creado el 2026-09-15; último push 2026-10-13; sin licencia declarada; público. En la API figura como repositorio no bifurcado (fork: false). El autor de la entrada es el nombre de cuenta, no el nombre de una persona. El código de este artículo puede estar aún sin subir al repositorio: confirmar antes de enviar |
| senamhi2021 | SENAMHI (2021). *Climas del Perú: Mapa de Clasificación Climática Nacional*, 1.ª ed. ISBN 978-612-48315-3-9 | PDF oficial https://www.senamhi.gob.pe/load/file/01404SENA-4.pdf (créditos: primera edición agosto de 2021, ISBN) | verificada | §3.1: clasificación climática (38 tipos) | Copiada de Palacios. La cifra «41 unidades» del paper nuevo no se contrastó aquí; los 38 tipos vienen del texto de Palacios y de la prensa |
| kimball1997 | Kimball, Running, Nemani (1997), *Agric. For. Meteorol.* 85(1–2):87–98 | Crossref 10.1016/S0168-1923(96)02366-0 | verificada | §3.3: Td aproximada desde Tmin y su sesgo en zonas áridas | Copiada de Palacios |
| allen1998 | Allen, Pereira, Raes, Smith (1998), FAO-56 | https://www.fao.org/4/x0490e/x0490e00.htm (autores, Roma 1998, ISBN 92-5-104219-5) | verificada | §3.3: Td ≈ Tmin como aproximación estándar | Copiada de Palacios; se añadió ISBN y URL |
| lobit2018 | Lobit, López Pérez, Lhomme, Gómez Tagle (2018), *Theor. Appl. Climatol.* 133(3–4):751–762 | Crossref 10.1007/s00704-017-2211-9 | verificada | §3.3: sesgo del método Td = Tmin | HANDOFF cita «133» sin título: coincide el volumen. Publicado en línea en 2017, volumen de 2018. Estudio en México; no extrapolar a Perú sin matiz |
| eccel2012 | Eccel (2012), *Meteorol. Appl.* 19:118–128 | Crossref 10.1002/met.258 | verificada | §3.3: Td desde Tmin requiere calibración local | Copiada de Palacios |
| verdin2020 | Verdin et al. (2020), CHIRTS-daily, *Sci. Data* 7:303 | Crossref 10.1038/s41597-020-00643-7 | verificada | §3.1/§3.3: producto de temperatura grillado de referencia | Solo si el paper lo usa |
| smith2011 | Smith, Lott, Vose (2011), ISD, *BAMS* 92(6):704–708 | Crossref 10.1175/2011BAMS3015.1; cita sugerida por NCEI https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database | verificada | §3.3: estaciones de aeropuerto de A4 | Los datos se acceden desde NCEI; añadir fecha de descarga |
| noaa_oni | NOAA CPC, Oceanic Niño Index | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php | verificada (producto de datos, sin artículo) | §3.3: ONI como covariable o estratificación | La página informa que el ONI sobre ERSST v5 pasó a v6 y que RONI es el índice de monitoreo oficial: declarar la versión empleada |
| gneiting2007 | Gneiting y Raftery (2007), *JASA* 102(477):359–378 | Crossref 10.1198/016214506000001437 | verificada | §3.3: reglas de puntuación propias (pinball/CRPS) | |
| kunsch1989 | Künsch (1989), *Ann. Statist.* 17(3):1217–1241 | Crossref 10.1214/aos/1176347265 | verificada | §3.3: bootstrap por bloques | Se eligió Künsch; Lahiri como texto de referencia |
| lahiri2003 | Lahiri (2003), *Resampling Methods for Dependent Data*, Springer | Crossref 10.1007/978-1-4757-3803-2 | verificada | §3.3 | |
| aksu2024 | Aksu et al. (2024). *GIFT-Eval.* arXiv 2410.10393 | https://arxiv.org/abs/2410.10393 (API de arXiv: 8 autores, publicado 2024-10-14) | verificada (solo preprint) | Límites: contaminación entre preentrenamiento y evaluación; contenido de `GiftEvalPretrain` | Texto completo leído en las secciones de fuga (apéndice F.2, tabla 14). Notas de preentrenamiento en `notas_preentrenamiento.md` |
| shchur2025 | Shchur et al. (2025). *fev-bench.* arXiv 2509.26468 | https://arxiv.org/abs/2509.26468 (API de arXiv: 8 autores, publicado 2025-09-30, actualizado 2026-06-30) | verificada (solo preprint) | Límites: política de fuga autoinformada | Se leyó la sección «Data leakage». No se confirmó versión arbitrada |
| jain2026timesfm3blog | Jain y Sen (2026). *TimesFM-3.* Google Research Blog, 2026-08-31 | https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/ (HTML crudo) | verificada | Métodos: mecanismo de covariables y tamaño del corpus | Entrada de blog, no arbitrada; no cita un artículo propio de la versión 3.0 |
| palacios_enprep | Palacios y Juarez (en preparación). *Extending the PISCO gridded dew-point record for Peru (2017–2020) from the continued minimum-temperature record, using per-climate-zone seasonal model selection.* Manuscrito en preparación | Encabezado YAML de `reports/paper/paper_taac.qmd` (título) y `reports/paper/paper.qmd` (autores: Piero Palacios, Henry Juarez); solo lectura | manuscrito no publicado; datos tomados del borrador | §3.2 y §3.3: método `tuned` (antecedente directo) | El año 2026 es el del borrador y es provisional (el encabezado trae `date: last-modified`). Sin DOI, revista ni versión estable; actualizar al publicarse. Decisión del usuario: citar como «manuscrito en preparación» |

## 2. Candidatos no añadidos

| candidato | motivo |
|---|---|
| Muñoz-Sabater et al. (2021), ERA5-Land, *ESSD* | No se consultó la ficha en esta pasada. Además, la regla del proyecto desaconseja comparar con ERA5 salvo en T1 |
| `forster2016` (MELODIST), `althoff2023`, `chabotcouture2014`, `he2021`, `wang2021`, `serranonotivoli2019`, `kilibarda2014`, `mu2025`, `hierro2025`, `huang2024`, `zhang2016`, `gallusser2025`, `jansen2026`, `asta2025` (Palacios) | Pertenecen al paper vigente y no se necesitan para las afirmaciones listadas en §3.1–3.3. `forster2016` sí se reverificó en Crossref (Förster et al., GMD 9:2315–2333, 2016) y puede añadirse si se discute la desagregación de humedad. Las demás no se reverificaron |
| Ficha propia del producto «Td PISCO v1.1» | No se encontró (sección 3) |
| Nota de TimesFM 2.5 / 200M | El checkpoint usado es 3.0 de 330M; no se cita 2.5 |
| Artículo de revista de TimesFM más allá de ICML 2024 | No se encontró; se usa PMLR |
| Referencia de Lag-Llama y TimeGPT-1 en revista | Solo preprint verificado |

## 3. Producto Td PISCO

La búsqueda de una publicación dedicada al producto de temperatura de rocío PISCO v1.1 (SENAMHI, Huerta, Lavado-Casimiro) no devolvió ninguna ficha. Solo aparece PISCOt (Tmax y Tmin) y PISCOeo_pm. Dentro de PISCOeo_pm (huerta2022) la metodología interpola Tmax, Tmin, horas de sol, Td y viento, de modo que es la cita defendible mientras Palacios no indique otra. Pendiente: preguntar a Palacios por la referencia o la ficha de distribución (DOI o repositorio SENAMHI) de la versión 1.1.

## 4. Checkpoint de TimesFM y licencia

- Uso en el repositorio: `experiments/timesfm/variants.py` fija `TIMESFM_30 = "google/timesfm-3.0-pytorch"` y `CHECKPOINT_REVISION = "43046b85ec22d584a13f8098c2ed39c889e129c2"`. El Hub devuelve esa misma revisión como actual.
- Tamaño verificado con la API del Hub: 330.710.976 parámetros (F32), 20 capas, dimensión del modelo 1280, 9 cuantiles, parche de entrada 32 y de salida 64. El número «330M» queda confirmado.
- Licencia (ficha del Hub y README de GitHub): TimesFM Non-Commercial License v1.0 para los pesos 3.0; el código es Apache-2.0 y los pesos hasta la 2.5 son Apache-2.0. Solo uso no comercial y no productivo; las salidas (predicciones) no se consideran derivados. Un producto operativo de SENAMHI con estos pesos exigiría revisar la licencia o usar los servicios autorizados que menciona el README (BigQuery ML). Es un hecho relevante para la sección de costo y de límites.
- La ficha del Hub cita aún el artículo de arXiv (2023) y no un artículo específico de la versión 3.0; por eso `das2024` no describe la versión 3.0. Redactar el texto con esa salvedad.

## 5. Búsqueda de trabajo previo directo

Una sola búsqueda extendida sobre modelos de fundación para rellenar o reconstruir variables meteorológicas grilladas. No devolvió ningún estudio directo. Resultados cercanos, sin verificar en texto completo:

- UHI-Bench (arXiv:2608.23857, Ling et al.; ficha confirmada en la API de arXiv): referido en la búsqueda como benchmark de imputación de LST con Chronos-2 en primer lugar. Es temperatura superficial y por ciudades, no Td grillada.
- MDPI, *Future Internet* 18(10):550 (https://www.mdpi.com/1999-5903/18/10/550): robustez de modelos zero-shot frente a datos faltantes en sensores industriales. La página devolvió 403; solo se conoce por el resumen del buscador.
- arXiv:2501.07276: imputación en medidores inteligentes con modelos de fundación.
- BiLSTM-I (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8507855/): relleno de huecos largos en estaciones, método no basado en modelos de fundación.
- Registro de Zenodo https://zenodo.org/records/23299384: posprocesamiento de pronósticos con TimesFM-3 y Chronos-2.

Conclusión prudente: no se halló trabajo previo directo con esta búsqueda acotada; no se puede afirmar un vacío en la literatura. HANDOFF §7 pide repetirla con «ERA5», «station temperature» y «CAMELS». Ninguno de estos hallazgos se añadió al `.bib` por no estar verificado.

## 6. Avisos de uso de datos y de IA

La verificación usó solo fuentes públicas. Esta tabla fue elaborada con ayuda de IA generativa (Claude) y requiere revisión por una persona experta antes de citarse.
