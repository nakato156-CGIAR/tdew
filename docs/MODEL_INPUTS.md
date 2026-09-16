# TDEW — Qué predice el modelo y con qué inputs

> Nota introductoria para quien recién llega al proyecto: este documento resume, en
> lenguaje simple, cuál es el problema, qué datos existen y qué recibe exactamente
> el modelo como entrada.

## El problema

**PISCO** es un producto de datos climáticos grillados de Perú (SENAMHI): el país está
dividido en ~2.8 millones de celdas, y para cada celda existen series diarias de
variables climáticas.

Este proyecto trabaja con dos de esas variables:

- **TD** — temperatura de punto de rocío (dewpoint). Disponible **1981–2016**.
- **TMIN** — temperatura mínima diaria. Disponible **1981–2020** (versión v1.2).

No hay ninguna otra variable cruda en juego. El hueco a resolver: **TD no existe para
2017–2020**, pero sí se necesita (por ejemplo, para alimentar otros sistemas como
Simcast). El objetivo del proyecto es **predecir/estimar TD para 2017–2020, celda por
celda, día por día**, usando TMIN (el único dato real disponible en ese período) más
información derivada del historial 1981–2016.

## Qué produce el modelo (output)

Un valor diario de **TD** para cada celda (`ID`), para cada día de 2017–2020. El modelo
internamente predice una **anomalía** (`TD_anom`), que luego se suma al promedio
histórico (`TD_clim`) de ese día del año para obtener el valor final de TD.

## Tabla de inputs del modelo

La tabla lista **todo** lo que entra a la fórmula de regresión, qué representa cada
cosa y de dónde sale (dato real observado, cálculo derivado, o predicción previa del
propio modelo).

| Input | Qué representa | De dónde sale |
|---|---|---|
| `const` | Intercepto de la regresión (constante = 1) | No es un dato, es un término fijo de la fórmula |
| `TMIN` (dato crudo) | Temperatura mínima del día, en esa celda | **Dato real observado** (v1.2, disponible 1981–2020) |
| `TD` (dato crudo, solo 1981–2016) | Temperatura de punto de rocío del día, en esa celda | **Dato real observado** (v1.1, solo hasta 2016) |
| `TD_clim(ID, doy)` | Promedio histórico de TD para esa celda, en ese día del año (ej.: promedio de todos los 15-marzo entre 1981–2016) | **Calculado una sola vez** a partir de los 36 años de historia (climatología) |
| `TMIN_clim(ID, doy)` | Promedio histórico de TMIN para esa celda, en ese día del año | **Calculado una sola vez** a partir de los 36 años de historia (climatología) |
| `TMIN_anom` | Cuánto se desvía el TMIN de hoy respecto a su promedio histórico (`TMIN - TMIN_clim`) | **Derivado** del dato real de TMIN de hoy |
| `TD_anom_lag1` | Desviación de TD de **ayer** respecto a su promedio histórico | 1981–2016: derivado de un dato real. <br>2017–2020: derivado de la **predicción que el propio modelo hizo ayer** (no hay TD real en este rango) |
| `TD_anom_lag2` | Desviación de TD de **hace 2 días** respecto a su promedio histórico | Igual que arriba: dato real (hasta 2016) o predicción previa del modelo (2017–2020) |
| `TD_anom_lag3` *(solo versión tuneada)* | Desviación de TD de hace 3 días | Igual mecanismo que los lags anteriores |
| `TD_anom_lag7` *(solo versión tuneada)* | Desviación de TD de hace 7 días | Igual mecanismo |
| `TD_anom_lag30` *(solo versión tuneada)* | Desviación de TD de hace 30 días | Igual mecanismo |
| `TMIN_anom_lag1` | Desviación de TMIN de **ayer** respecto a su promedio histórico | **Derivado** de un dato real de TMIN (TMIN sí existe todos los días, incluido 2017–2020) |
| `TMIN_anom_lag2` *(solo versión tuneada)* | Desviación de TMIN de hace 2 días | Derivado de dato real de TMIN |
| `TMIN_anom_lag7` *(solo versión tuneada)* | Desviación de TMIN de hace 7 días | Derivado de dato real de TMIN |
| `TMIN_anom_lag30` *(solo versión tuneada)* | Desviación de TMIN de hace 30 días | Derivado de dato real de TMIN |
| Zona climática SENAMHI (41 zonas) | Región climática a la que pertenece la celda (costa, sierra, selva, etc.) | **Metadato geográfico fijo**, asignado por un shapefile de zonas climáticas (no cambia con el tiempo) |
| Día del año (`doy`, 1–366) | Qué día del calendario es (para elegir la climatología y la ventana de entrenamiento correspondiente) | Se deriva directamente de la fecha |

### Notas sobre las filas marcadas *(solo versión tuneada)*

El modelo de **producción** (fijo, más simple) usa solo 5 inputs:
`const`, `TMIN_anom`, `TD_anom_lag1`, `TD_anom_lag2`, `TMIN_anom_lag1`.

El modelo **tuneado** (en desarrollo) permite elegir automáticamente, para cada
combinación de zona climática × día del año, un subconjunto distinto de lags dentro de
un menú más amplio (ver tabla completa arriba). Ningún feature usa datos que no
provengan, en última instancia, de TMIN o TD.

## Punto clave a recordar

**El único dato real observado que existe para el período que se quiere predecir
(2017–2020) es TMIN.** Todo lo demás que ve el modelo —climatologías, anomalías, y los
lags de TD durante 2017–2020— son cantidades calculadas a partir de la historia
1981–2016 o predicciones que el propio modelo genera día tras día (por eso se dice que
la predicción es "autoregresiva": se retroalimenta con su propia salida anterior).
