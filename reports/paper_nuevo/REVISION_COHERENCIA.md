# Revisión de coherencia: correcciones aplicadas

Se consolidaron los diez Markdown de `reports/paper_nuevo/` el 21 de octubre de 2026, a partir de la revisión de los nueve documentos originales. Este archivo registra las correcciones realizadas y sustituye el informe inicial de recomendaciones. El alcance se limita a esta carpeta: no se modificaron el artículo de Palacios, los scripts, el artefacto externo ni los CSV de resultados.

Se mantuvo la tesis E acotada y se armonizaron `ORIENTACION_PAPER.md`, `historia_paper.md` y `paper_narrative.md`. Las referencias externas no comprobadas se identifican como tales; no se las convirtió en evidencia confirmada.

## Resolución de los hallazgos

| Hallazgo de la revisión | Corrección aplicada | Documentos |
|---|---|---|
| Historial largo presentado como mínimo demostrado | Se distingue el contexto desde 1981 de la referencia, el efecto pequeño del recorte hasta 2002 con climatología fija y el mínimo no determinado | Orientación, historia, narrativa, escalera, desglose y síntesis |
| Explicación MODIS incompatible con la interpretación retirada | Se describe el inicio de contexto y de climatología; no se identifica un quiebre en 2000 ni se confirma bibliografía sin comprobar | Historia, narrativa, escalera, desglose, síntesis y A4 |
| IC con cero interpretado como equivalencia | Se informa la brecha y la incertidumbre sin establecer empate, equivalencia o igualdad de predicciones | Guías y resultados |
| Descripción incorrecta del bootstrap | Se precisa qué conserva cada bloque y qué dependencia se rompe; se informan los dos esquemas como sensibilidades | Orientación, historia, narrativa, desglose y síntesis |
| Atribución causal a la recursión de Td | Se informa la reducción observada de A2, aclarando la nueva selección de recetas y ventanas y la causa no aislada | Historia, narrativa, desglose y síntesis |
| RMSE próximos convertidos en predicciones iguales | Se mantienen nueve variantes, seis por debajo de `tuned`; la igualdad de predicciones no fue comprobada | Historia y narrativa |
| Orden de Td cruda frente al LLR simple sin ámbito | Se distingue mayor RMSE en dominio completo de menor RMSE en Perú, con ambos IC incluyendo cero | Síntesis |
| Costo total sin cribado | Se separa inferencia (73 min 10 s), selección única (49 min 8 s) y total con selección (122 min 18 s), frente a 58 min 28 s de `tuned` | Orientación, historia, narrativa, costo y síntesis |
| Reparto cuerpo/suplemento y prioridad de bloques distintos | Se presenta `ll4b` primero; A2 se resume en el cuerpo y se detalla en el suplemento | Orientación, historia, narrativa y síntesis |
| Referencias activas a la regla retirada | Se conserva su retiro como antecedente y se elimina como regla de decisión vigente | README, orientación, historia, narrativa y síntesis |
| 41 tipos climáticos implícitos | Se distinguen 38 tipos climáticos y tres unidades adicionales, 41 unidades cartográficas en total | Orientación, historia, narrativa, desglose y costo |
| Máscaras de Perú intercambiadas | Se distingue contorno político del nuevo panel de ámbito clasificado del artículo previo | Orientación, historia, narrativa, desglose y síntesis |
| “Sin entrenamiento” y eliminación de todo diseño | Se usa “sin ajuste de pesos locales”, con checkpoint preentrenado y selección única de configuración | Guías y costo |
| A4 con comparaciones excluidas y afirmación excesiva de independencia | Se retiran tablas y lecturas de ERA5, conservando CSV históricos; se distingue ausencia de solapamiento temporal de independencia espacial sin verificar | A4, historia y síntesis |
| Conteos de A4 compartidos entre métricas con muestras distintas | Se separan días-estación y estaciones de Td y anomalías; se ajustan conteos anuales y sensibilidad diaria desde los CSV | A4 |
| Redondeo del IC de `ll4b` | Se corrige −0,014 a −0,013 para el límite superior mes-año de TimesFM frente a `llr_rezagos_sel` en dominio completo | Desglose |
| README describía materiales todavía inexistentes | Se describe la carpeta actual de preparación y se enlazan sus guías vigentes | README |

## Evidencia conservada

En `resultados/a1_por_metodo.csv`, TimesFM tiene menor RMSE agregado que `tuned` en los cuatro casos. El sesgo absoluto de TimesFM es mayor en tres: ambos ámbitos de `ll4` y Perú en `ll4b`. En 2013 se invierte el orden del RMSE en el dominio completo. Frente a `llr_rezagos_sel` los márgenes son menores y los dos IC contienen cero en dominio completo de `ll4` (`resultados/a1_brechas.csv`). No se interpretó ese caso como equivalencia.

El costo se deriva de `resultados/costo.csv`: TimesFM suma 4.389,8 + 2.948 = 7.337,8 s, redondeados a 122 min 18 s; `tuned` suma 3.158 + 350 = 3.508 s, o 58 min 28 s. El cribado se hizo en `ll4` y se reutilizó; no se vuelve a cobrar por bloque. Los tiempos de producto no constituyen una comparación controlada de velocidad.

En A4 se usan las filas `muestra = productos`. PISCO tiene 31.326 días-estación y 13 estaciones para Td absoluta en 2009–2016, frente a 30.751 y 12 para anomalías. Los dos productos 2017–2020 tienen 14.666 días-estación y 12 estaciones para ambas métricas. La sensibilidad `_h4b2` también distingue los conteos por métrica. Las diferencias entre muestras quedan explícitas en lugar de usar un único conteo para todas las columnas.

Como guía de narración se tomó `reports/paper/paper_taac.qmd`: vacío de Td después de 2016, continuidad de Tmin, datos y dominio, selección y ajuste por celda, reconstrucción, evaluación y límites. Las 41 unidades se describen según su sección de datos; el protocolo de `tuned` se describe según su sección de selección. No se modificó ese artículo.

## Alcance de la comprobación

Se contrastaron los agregados, las brechas y los costos citados con sus CSV; se revisaron los conteos por métrica en A4, las tablas Markdown y las interpretaciones de los diez documentos. Se comprobó que las tablas generadas de A1 y de la escalera permanecen idénticas y que no hay cambios en los CSV existentes. Se verificaron las columnas de 496 filas de tablas de los diez Markdown, los enlaces locales y la ausencia de las formulaciones retiradas. La comparación de hashes de archivos existentes fuera de esta carpeta no registró cambios respecto al inicio; `git diff --check` no indicó errores de formato. No se recalcularon predicciones ni se ejecutaron experimentos nuevos.

La corrección documental no resuelve por sí sola las limitaciones científicas: contexto mínimo, independencia de estaciones, referencia bibliográfica específica de MODIS, Huerta 2023, costos seleccionados de los LLR y comparación homogénea de cómputo no se dan por demostrados. Se expresan como límites de la evidencia, de forma consistente entre documentos.

Se usó asistencia de IA generativa (Codex) para esta revisión y corrección. La revisión científica con Palacios y SENAMHI corresponde a la preparación del artículo; no se realizó publicación, commit ni push.
