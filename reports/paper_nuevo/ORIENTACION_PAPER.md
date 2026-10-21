# TimesFM sin entrenamiento frente al método diseñado de Palacios

Orientación editorial del 21 de octubre de 2026, actualizada el mismo día para adoptar la tesis E acotada (ver `historia_paper.md`). Se retiró la regla que elegía entre E y C+A según un IC; la tesis E se mantiene. El paper vigente en `reports/paper/` y `PAPER_PLAN.md` quedan fuera de este encargo.

Tesis: sin ajustar pesos y con los mismos datos que Palacios, TimesFM reconstruye Td con menor error que la regresión diseñada por zona climática, sin zonificación, búsqueda de recetas ni entrenamiento. Un LLR local sin zonas queda cerca y entra como control. La tesis vale para PISCO y los dos bloques evaluados; no se decide con un umbral estadístico y la discusión indica cuándo sigue conviniendo `tuned`.

Se conservarán los datos y versiones de Palacios, su grilla, las celdas y fechas comunes y sus transformaciones. Los rezagos pueden diferir entre métodos. La referencia TimesFM es `tmin_anom_full`: requiere historial local de Td y Tmin y sus climatologías de entrenamiento. Se conoce Tmin durante todo el bloque por reconstruir; no se trata de pronosticar sin covariables futuras. «Sin ajuste de pesos» no significa ausencia de preparación local ni ausencia de selección de configuración. Las zonas y recetas por zona × día del año son requisitos de `tuned`, no de toda la familia LLR.

| Evidencia | Destino | Uso editorial |
|---|---|---|
| Climatología, Palacios, LLR simple, LLR con rezagos seleccionado y TimesFM de referencia | Cuerpo | Comparación de RMSE, MAE y sesgo en 2009–2012 y 2013–2016, separando Perú y dominio completo |
| Brechas pareadas, ambos esquemas de IC, magnitudes anuales y por zona | Cuerpo | Precisar cuánto cambia el error y con qué incertidumbre |
| Requisitos de diseño y costo de entrenamiento, inferencia y total | Cuerpo | Palacios paga en el entrenamiento y TimesFM en la inferencia; el argumento es eliminar diseño y entrenamiento, no el cómputo |
| Robustez: 6 de 9 configuraciones del cribado superan a `tuned`; `tmin_td_full` también lo supera en 2009–2012 | Cuerpo | La ventaja no depende de una configuración; condiciones de uso: Tmin del período e historial largo |
| A2, A3, escalera de contexto y otras variantes | Suplemento | Sensibilidades del mecanismo y la configuración, sin convertirlas en prueba causal completa |
| Contraste ISD y comparación entre productos 2017–2020 | Suplemento | Alcance externo limitado: independencia de estaciones sin verificar; acuerdo entre productos no equivale a exactitud |
| Regla E/C+A; supuesto quiebre MODIS en 2000; IC con cero como empate; barajado como prueba de inutilidad de Td histórica | Retirado | Ninguna de estas interpretaciones queda respaldada por los controles disponibles |

Las cifras se consultan en la sección «Paper» del artefacto local, generada desde `a1_por_metodo.csv`, `a1_brechas.csv`, `a1_por_zona.csv` y `costo.csv` de `resultados/`. Se evitan copias numéricas en este documento. El generador `experiments/amenazas/artifact_amenazas.py` conserva las filas de origen en `datos_amenazas.js`; las brechas descriptivas por año y zona se calculan restando RMSE sobre la misma clave. No se calculan intervalos nuevos.

Los IC existentes son del RMSE pareado, por bootstrap espacial de 2° o por mes-año, con el número de réplicas declarado en el generador. Son dos remuestreos separados; ninguno representa conjuntamente la dependencia espacial y temporal. Un intervalo que contiene cero admite diferencias de ambos signos; no demuestra equivalencia. Las brechas anuales y zonales son descriptivas, sin IC. Las victorias por zona quedan como registro secundario frente a las magnitudes.

TimesFM presenta menor RMSE puntual que Palacios en ambos períodos y ámbitos. Frente al LLR con rezagos seleccionado, la diferencia es pequeña y en el dominio completo de 2013–2016 los intervalos incluyen cero. La elección práctica exige valorar también MAE, sesgo y costo. La configuración de TimesFM se eligió en el cribado de 2013–2016; 2009–2012 no participó en esa elección, pero sigue siendo una evaluación retrospectiva en el mismo producto.

TimesFM puede convenir cuando se dispone de contexto local largo y Tmin del bloque, se acepta el costo de inferencia y se prioriza la reducción observada del error sin diseñar recetas por zona. Palacios puede convenir cuando ya están disponibles sus recetas y coeficientes y se requiere reconstruir grandes volúmenes con la rapidez de su inferencia medida. Los LLR simples constituyen controles competitivos sin zonificación; sus costos seleccionados no se han medido. No se atribuyen a esos modelos los tiempos de las versiones anteriores con una grilla menor.

El preprocesamiento de PISCO, regrillado y climatologías se reconoce como preparación compartida y no dispone de un cronometraje independiente completo. Algunas filas de costo reúnen ajuste e inferencia; no se separan artificialmente. Los tiempos de producto completo usan corridas y hardware con documentación desigual y no constituyen una comparación controlada de velocidad.

No se ha probado el desempeño sin historial local de Td, ausencia o error sistemático de Tmin futura, ni una comparación de costos completamente homogénea. El barajado de Tmin muestra sensibilidad a la covariable correcta, pero no aísla el aporte marginal de Td histórica. La escalera cambia inicios de contexto y no prueba un quiebre de producto en 2000. No se incorporan ERA5 ni experimentos nuevos. Se conservan los resultados exploratorios como registro.

La actualización corresponde al artefacto local. No se realizó publicación remota, commit ni push.
