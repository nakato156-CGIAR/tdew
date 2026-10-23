# Orientación del paper nuevo: TimesFM frente al método de Palacios

Orientación editorial consolidada el 21 de octubre de 2026. Se conserva la tesis E acotada: con los insumos locales de PISCO, TimesFM sin ajuste de pesos locales obtuvo menor RMSE agregado que `tuned` en ambos bloques y ámbitos. No necesita selección de recetas por unidad cartográfica y día del año; sí requiere preparación local y selección de configuración. Un LLR local sin zonas queda cerca. La regla E/C+A queda retirada y no se elige la narrativa mediante un umbral estadístico.

## Datos, evaluación y alcance

Se usan Td PISCO v1.1 (1981–2016), Tmin PISCO v1.2 (1981–2020), la grilla de 0,01° y las climatologías de entrenamiento del protocolo de Palacios. La comparación principal usa TimesFM `tmin_anom_full`, con contexto desde 1981 y Tmin observada durante todo el bloque reconstruido. Se trata de reconstrucción con covariable observada. Los métodos comparten productos, celdas y fechas puntuadas; difieren en cómo usan el historial, los rezagos y la selección.

Se presenta primero `ll4b`, prueba 2009–2012 con contexto hasta 2008, porque no participó en la elección de la configuración de TimesFM. `ll4`, prueba 2013–2016 con contexto hasta 2012, se informa con la salvedad de que el cribado de nueve variantes se hizo sobre ese bloque. Ambos son retrospectivos y pertenecen al mismo producto.

El dominio completo tiene 17.027 celdas puntuadas; Perú, 8.272 centros de celda dentro del contorno político; 8.755 quedan fuera. Esta máscara de Perú difiere del ámbito clasificado del artículo previo. Las 41 unidades cartográficas SENAMHI comprenden 38 tipos climáticos y tres unidades adicionales (dos lagos y lomas costeras); 33 unidades están representadas en el panel y 32 en Perú. La zonificación es propia de `tuned`, no de toda regresión local.

Los resultados incluyen RMSE, MAE y sesgo. TimesFM tiene mayor sesgo absoluto que `tuned` en tres de las cuatro combinaciones agregadas. En 2013 el orden del RMSE se invierte en el dominio completo. La ventaja frente al LLR con rezagos seleccionado es menor; en el dominio completo de `ll4` sus dos IC incluyen cero. Esto no establece equivalencia.

## Reparto de la evidencia

| Evidencia | Destino | Uso |
|---|---|---|
| Climatología, `tuned`, LLR con rezagos seleccionado y TimesFM | Cuerpo | RMSE, MAE y sesgo, primero `ll4b`; Perú y dominio completo separados |
| Inventario de preparación y selección | Cuerpo | Describir qué requiere cada método, sin atribuir horas humanas no medidas |
| Brechas pareadas con ambos IC; magnitudes anuales y por zona | Cuerpo | Tamaño y variación de las diferencias, incluido 2013 |
| Cribado de nueve variantes; control de representación cruda | Cuerpo | Sensibilidad observada, sin garantizar independencia de configuración |
| A2, `tuned_sin_td` | Resumen en cuerpo; detalle en suplemento | La reducción del RMSE es mayor en `ll4`; no se aisló una causa |
| Costo por etapa, selección única e inferencia | Cuerpo | Comparar las corridas documentadas con sus condiciones |
| A3, escalera de contexto y variantes adicionales LLR | Suplemento | Sensibilidades; no se determinó el historial mínimo |
| A4, estaciones ISD y acuerdo entre productos 2017–2020 | Suplemento | Contraste externo limitado; acuerdo no equivale a exactitud |
| Conteos de victorias por zona y lista completa de costos | Suplemento | Detalle junto a las magnitudes del cuerpo |

Los IC pareados existentes usan 2.000 réplicas por bloques espaciales de 2° o mes-año. El espacial conserva las series completas dentro del bloque y rompe dependencia entre bloques; el mensual conserva todas las celdas y días del mes y rompe dependencia entre meses. Ninguno representa toda la dependencia espacial y temporal conjuntamente. Las brechas anuales y zonales son descriptivas, sin IC propios.

## Costo y condiciones de uso

En `ll4b`, `tuned` suma 58 min 28 s de selección de recetas, ajuste y predicción. TimesFM emplea 73 min 10 s de inferencia y 49 min 8 s de cribado único: 122 min 18 s incluyendo selección. El cribado se realizó en `ll4` y se reutilizó; no se vuelve a sumar a cada bloque ni se atribuye a datos de `ll4b`. Los tiempos seleccionados de los LLR no se midieron. El preprocesamiento compartido carece de cronometraje independiente completo.

A escala de producto, `tuned` necesitó unas 39 h de selección y ajuste y 19 min 40 s de inferencia; TimesFM empleó unos 5,1 días de inferencia. El hardware y la carga no están controlados entre todas las corridas. No se afirma una ventaja general de velocidad o costo para TimesFM.

La referencia de TimesFM usa historial local de Td y Tmin, climatologías y Tmin del bloque. La escalera muestra cambios pequeños al recortar el contexto hasta 2002 con climatología fija; no demuestra que el historial largo sea un requisito mínimo. El barajado muestra sensibilidad a Tmin alineada, sin aislar el aporte marginal de Td histórica. No se probaron ausencia o error sistemático de Tmin ni transferencia a otro producto. Las condiciones de licencia de los pesos deben comprobarse antes de recomendar un uso operativo.

No se incorporan comparaciones con ERA5 ni mecanismos MODIS o ENSO no probados. Las referencias bibliográficas sin comprobar se identifican como tales. Se conservan los CSV existentes; el artículo previo y el artefacto externo a esta carpeta quedan fuera de esta actualización.
