| Método | Selección de configuración | Ajuste o inferencia | Total | Hardware |
|:-------------------------|--------------------------:|-----------------------:|------------------------:|:-------------------------|
| tuned | 52 min 38 s | 5 min 50 s | 58 min 28 s | RTX A2000 12 GB + CPU |
| TimesFM | 49 min 8 s | 73 min 10 s | 122 min 18 s | RTX A2000 12 GB |
| LLR simple seleccionado | 1 min 18 s | 10 s | 1 min 42 s | Intel Core i9-14900K, sin GPU |
| LLR con rezagos seleccionado | 1 min 2 s | 10 s | 1 min 26 s | Intel Core i9-14900K, sin GPU |
| TimesFM / tuned (cociente de totales) | — | — | 2 | — |
| TimesFM / LLR simple seleccionado (cociente de totales) | — | — | 72 | — |
| TimesFM / LLR con rezagos seleccionado (cociente de totales) | — | — | 86 | — |
