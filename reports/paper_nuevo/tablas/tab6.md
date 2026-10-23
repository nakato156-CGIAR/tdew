| Escala | Método | Etapa | Tiempo de pared | Segundos | Hardware |
|:-------------------------|:-------------------------|:-------------------------|------------------------:|------------------:|:-------------------------|
| 2009–2012, estación con GPU | tuned | Selección de recetas (solo años de entrenamiento) | 52 min 38 s | 3.158 | RTX A2000 12 GB + CPU |
| 2009–2012, estación con GPU | tuned | Ajuste y predicción | 5 min 50 s | 350 | RTX A2000 12 GB + CPU |
| 2009–2012, estación con GPU | tuned | Total | 58 min 28 s | 3.508 | — |
| 2009–2012, estación con GPU | TimesFM | Inferencia (sin ajuste de pesos) | 73 min 10 s | 4.389,8 | RTX A2000 12 GB |
| 2009–2012, estación con GPU | TimesFM | Selección única de configuración (hecha en 2013–2016, suma de las variantes) | 49 min 8 s | 2.948 | RTX A2000 12 GB |
| 2009–2012, estación con GPU | TimesFM | Total incluyendo la selección una vez | 122 min 18 s | 7.337,8 | — |
| 2009–2012, estación con GPU | TimesFM / tuned | Cociente de totales | 2 | — | — |
| 2009–2012, otra máquina, sin GPU | LLR simple seleccionado | Carga de datos | 14 s | 14,3 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR simple seleccionado | Selección conjunta de h y año de inicio (40 combinaciones) | 1 min 18 s | 77,9 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR simple seleccionado | Ajuste final, predicción y escritura | 10 s | 9,8 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR simple seleccionado | Total | 1 min 42 s | 102 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | TimesFM / LLR simple seleccionado | Cociente de totales | 72 | — | — |
| 2009–2012, otra máquina, sin GPU | tuned / LLR simple seleccionado | Cociente de totales | 34 | — | — |
| 2009–2012, otra máquina, sin GPU | LLR con rezagos seleccionado | Carga de datos | 14 s | 14,4 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR con rezagos seleccionado | Selección conjunta de h y año de inicio (40 combinaciones) | 1 min 2 s | 61,5 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR con rezagos seleccionado | Ajuste final, predicción y escritura | 10 s | 9,7 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | LLR con rezagos seleccionado | Total | 1 min 26 s | 85,6 | Intel Core i9-14900K (32 hilos), 125 GB RAM |
| 2009–2012, otra máquina, sin GPU | TimesFM / LLR con rezagos seleccionado | Cociente de totales | 86 | — | — |
| 2009–2012, otra máquina, sin GPU | tuned / LLR con rezagos seleccionado | Cociente de totales | 41 | — | — |
| Producto 2017–2020 (corridas no controladas) | tuned | Selección de recetas, producción 1981–2016 | 32 h 42 min | 117.698 | no registrado (una GPU local) |
| Producto 2017–2020 (corridas no controladas) | tuned | Ajuste, producción 1981–2016 | 6 h 45 min | 24.293 | no registrado (una GPU local) |
| Producto 2017–2020 (corridas no controladas) | tuned | Selección y ajuste | 39 h 27 min | 141.991 | — |
| Producto 2017–2020 (corridas no controladas) | tuned | Predicción 2017–2020 | 19 min 40 s | 1.180 | no registrado; 14 procesos |
| Producto 2017–2020 (corridas no controladas) | TimesFM | Inferencia 2017–2020 | ≈5,1 días | 438.074 | RTX A2000 12 GB |
| Producto 2017–2020 (corridas no controladas) | TimesFM / tuned | Cociente de inferencia | 371 | — | — |
