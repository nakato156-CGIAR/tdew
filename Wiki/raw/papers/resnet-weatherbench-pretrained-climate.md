# Data-driven medium-range weather prediction with a Resnet pretrained on climate simulations: A new model for WeatherBench

- **Venue/año**: Journal of Advances in Modeling Earth Systems (JAMES), 2020
  (2020MS002405). Preprint: arXiv:2008.08626 (v1 19-08-2020, v2 18-11-2020).
- **URL**: https://arxiv.org/abs/2008.08626 — PDF capturado: https://arxiv.org/pdf/2008.08626v2
- **DOI (preprint)**: https://doi.org/10.48550/arXiv.2008.08626
- **Autores**: Stephan Rasp, Nils Thuerey.
- **Fecha de captura**: 2026-09-21

## Abstract (verbatim, v2)

"Numerical weather prediction has traditionally been based on physical models of the
atmosphere. Recently, however, the rise of deep learning has created increased interest in
purely data-driven medium-range weather forecasting with first studies exploring the
feasibility of such an approach. To accelerate progress in this area, the WeatherBench
benchmark challenge was defined. Here, we train a deep residual convolutional neural
network (Resnet) to predict geopotential, temperature and precipitation at 5.625 degree
resolution up to 5 days ahead. To avoid overfitting and improve forecast skill, we pretrain
the model using historical climate model output before fine-tuning on reanalysis data. The
resulting forecasts outperform previous submissions to WeatherBench and are comparable in
skill to a physical baseline at similar resolution. We also analyze how the neural network
creates its predictions and find that, with some exceptions, it is compatible with physical
reasoning. Finally, we perform scaling experiments to estimate the potential skill of
data-driven approaches at higher resolutions."

## Arquitectura (extracto, sección 2.2)

- Resnet totalmente convolucional (He et al., 2015) con **19 bloques residuales**. Cada
  bloque residual son dos bloques convolucionales
  `[conv 2D -> LeakyReLU -> Batch normalization -> Dropout]`, y al final la entrada del
  bloque se **suma** a la señal actual.
- Convoluciones internas: 128 canales, kernel 3. Primera capa: bloque convolucional simple
  de 128 canales con kernel 7 "para aumentar el campo de visión".
- Convoluciones periódicas en longitud, zero padding en latitud. LeakyReLU con α = 0.3,
  weight decay 1e-5, dropout 0.1 (sin dropout en el modelo preentrenado, que dio mejores
  scores de validación).
- Tres formas de construir pronósticos data-driven, explicitadas por los autores: **direct**
  (un modelo por horizonte), **continuous** (el horizonte entra como canal adicional, un
  solo modelo para todos los horizontes) e **iterative** (modelo de paso corto aplicado
  repetidamente sobre su propia salida). Este trabajo entrena direct y continuous.
- Entradas: geopotencial, temperatura, viento zonal y meridional y humedad específica en 7
  niveles (50, 250, 500, 600, 700, 850, 925 hPa), temperatura a 2 m, precipitación
  acumulada 6-horaria y radiación solar incidente en el tope de la atmósfera, todas en
  t, t−6h y t−12h; más tres campos constantes (máscara tierra-mar, orografía, latitud).
  Total: 114 canales.
- Normalización: se resta la media y se divide por la desviación estándar, salvo
  precipitación, a la que no se le resta la media (para mantener la cota inferior en cero) y
  a la que se aplica log-transform `ln(ε + PR) − ln(ε)` con ε = 0.001. Los autores califican
  esa transformación de decisiva para evitar que la red prediga simplemente ceros.
- Z500/T850/T2M se predicen con una red y TP con otra: predecir las cuatro variables con una
  sola red "llevó a malas predicciones para todas".
- Pérdida: MSE ponderado por latitud (peso ∝ cos φ). Adam, batch 32, learning rate inicial
  5e-5 (5e-7 para el fine-tuning desde CMIP), reducción por factor 5 al estancarse la
  validación, early stopping con paciencia 5.
- Datos: preentrenamiento con 150 años de salida de modelo climático (CMIP), fine-tuning con
  ERA (entrenamiento 1979-2015, validación solo 2016). Entrenar un modelo toma ~1 día en una
  GPU GTX 2080.

## Resultados (Table 1, RMSE ponderado por latitud, 3 días / 5 días, resolución 5.625°)

| Modelo | Z500 [m²s⁻²] | T850 [K] | T2M [K] | PR [mm] |
|---|---|---|---|---|
| Persistence | 936 / 1033 | 4.23 / 4.56 | 3.00 / 3.27 | 3.23 / 3.24 |
| Climatology | 1075 | 5.51 | 6.07 | 2.36 |
| Weekly climatology | 816 | 3.50 | 3.19 | 2.32 |
| IFS T42 | 489 / 743 | 3.09 / 3.83 | 3.21 / 3.69 | |
| IFS T63 | 268 / 463 | 1.85 / 2.52 | 2.04 / 2.44 | |
| Operational IFS | 154 / 334 | 1.36 / 2.03 | 1.35 / 1.77 | 2.36 / 2.59 |
| Weyn et al. (2020) | 373 / 611 | 1.98 / 2.87 | | |
| Direct (ERA only) | 314 / 561 | 1.79 / 2.82 | 1.53 / 2.32 | 2.03 / 2.35 |
| Direct (CMIP only) | 323 / 561 | 2.09 / 2.82 | 1.90 / 2.32 | 2.30 / 2.39 |
| **Direct (pretrained)** | **268 / 523** | **1.65 / 2.52** | **1.42 / 2.03** | 2.16 / 2.30 |
| Continuous (ERA only) | 331 / 545 | 1.87 / 2.57 | 1.60 / 2.06 | 2.22 / 2.32 |
| Continuous (CMIP only) | 330 / 548 | 2.12 / 2.75 | 2.24 / 2.59 | 2.29 / 2.38 |
| Continuous (pretrained) | 284 / 499 | 1.72 / 2.41 | 1.48 / 1.92 | 2.23 / 2.33 |

Persistencia, climatología y climatología semanal encabezan la tabla como referencias
triviales, junto a los modelos físicos IFS a distintas truncaciones. La tabla A1 del
apéndice repite la comparación en ACC, donde climatología queda en 0 por construcción y
persistencia en 0.62/0.53 (Z500) y 0.69/0.65 (T850).

## Observaciones de los autores

- El preentrenamiento con CMIP mejora el skill de Z500, T850 y T2M de forma creciente con el
  horizonte, y lo atribuyen a que el sobreajuste empeora con el horizonte: para horizontes
  largos la atmósfera es más caótica, condiciones iniciales similares llevan a resultados más
  dispersos, y un modelo entrenado con MSE tiende a predecir la media de esa distribución,
  que requiere más datos para estimarse.
- Los modelos entrenados **solo con CMIP**, sin fine-tuning sobre reanálisis, obtienen
  scores de test sobre ERA5 no mucho peores (o iguales) que los entrenados solo con ERA.
- Para precipitación el preentrenamiento no mejora, y los autores advierten que RMSE y ACC
  son métricas subóptimas para esa variable.
- Experimentos con cambios de dimensionalidad "no funcionaron tan bien como un Resnet simple
  sin ningún cambio".
