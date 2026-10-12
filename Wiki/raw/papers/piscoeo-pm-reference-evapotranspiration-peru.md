# PISCOeo_pm, a reference evapotranspiration gridded database based on FAO Penman-Monteith in Peru

- **Venue/año**: Scientific Data, Volume 9, Article 328. Publicado 2022-06-17.
- **DOI**: 10.1038/s41597-022-01373-8
- **Autores**: Adrian Huerta (correspondencia, adrhuerta@gmail.com, SENAMHI), Vivien Bonnesoeur
  (CONDESAN/iMHEA), José Cuadros-Adriazola (CONDESAN/iMHEA/Imperial College London), Leonardo
  Gutierrez (SENAMHI), Boris F. Ochoa-Tocachi (Imperial College London/ATUK/Forest Trends),
  Francisco Román-Dañobeytia (CONDESAN/iMHEA), Waldo Lavado-Casimiro (SENAMHI).
- **Fuente del PDF**: archivo local proporcionado por el usuario
  (`s41597-022-01373-8.pdf`), leído directamente (Open Access, CC BY 4.0).
- **Fecha de captura**: 2026-09-14

## Abstract

Se presenta un nuevo dataset grillado de evapotranspiración de referencia (ETo) basado en
FAO Penman-Monteith (FPM), llamado PISCOeo_pm. Desarrollado para el período 1981–2016 a
~1 km (0.01°) de resolución espacial para todo el territorio continental peruano. El marco
de desarrollo se basa en datos grillados previamente generados de subvariables
meteorológicas: temperatura del aire (máxima y mínima), duración de horas de sol, punto de
rocío, y velocidad del viento. Se aplicaron distintos pasos (control de calidad,
relleno de vacíos, homogenización, e interpolación espacial) a las subvariables. Basado en
una validación independiente, PISCOeo_pm exhibe en promedio mejor precisión que tres
productos grillados existentes (CRU_TS, TerraClimate, y ERA5-Land) porque presenta una
capacidad predictiva por encima del promedio observado usando datos diarios y mensuales, y
tiene mayor resolución espacial.

## Contexto y motivación

- ETo (evapotranspiración de referencia) es clave para estimar evapotranspiración real en
  agronomía (vía coeficientes de cultivo) y para entender balances hídricos y energéticos
  terrestres.
- La fórmula más aceptada para calcular ETo es FAO Penman-Monteith (FPM), pero requiere
  temperatura máx/mín, radiación solar (vía horas de sol), presión de vapor real (vía punto
  de rocío) y velocidad del viento — datos que suelen faltar en estaciones meteorológicas.
- En Perú, la temperatura del aire está fácilmente disponible, pero las demás subvariables
  son escasas. Estudios previos (Lavado et al. 2015, Laqui et al. 2019) estimaron ETo con
  datos limitados, usando aproximaciones para radiación solar.
- No existía previamente un producto grillado de ETo (FPM) de buena resolución para Perú; el
  único producto experimental (PISCO PET) usa la fórmula de Oudin y estima evapotranspiración
  potencial, no ETo.
- Productos globales existentes (CRU_TS, TerraClimate) o reanálisis (ERA5, ERA5-Land, NCEP/NCAR)
  proveen ETo o sus subvariables, pero con limitaciones de resolución espacial o
  representatividad en terreno complejo como Perú.

## Metodología

### Estrategia general: "interpolating first, calculating later" (IC)

Dos enfoques posibles quando faltan subvariables para FPM: (i) "less demanding methods"
(p.ej. Hargreaves-Samani, solo con temperatura) o (ii) estimar los datos faltantes antes de
calcular ETo. Dentro de (ii), la estrategia IC (interpolar primero, calcular después) usa
estaciones vecinas y métodos de interpolación espacio-temporal sobre la misma variable, en
vez de relaciones empíricas estacionarias entre variables (que pueden fallar bajo cambio
climático). Hay evidencia de que IC da mejores resultados que las alternativas. Esta es la
estrategia usada para PISCOeo_pm.

### Flujo de trabajo (Fig. 1)

Subvariables: Tmax, Tmin (tomadas de PISCOt, con downscaling espacial), duración de sol (Sd),
temperatura de punto de rocío (Td), velocidad del viento (Ws).

1. **Control de calidad, relleno de vacíos y homogenización** de Sd, Td, Ws (Tmax/Tmin ya
   procesadas en PISCOt).
2. **Interpolación climatológicamente asistida** (climatologically aided interpolation) de
   las subvariables, con apoyo de covariables espaciales: LST (temperatura de superficie),
   CC (frecuencia de nubosidad), DEM (elevación), X/Y (longitud/latitud), TDI (índice de
   disección topográfica).
3. **Aplicación de la fórmula FAO Penman-Monteith** a nivel de grilla → ETo (PISCOeo_pm).

### Datos observacionales

Más de 300 estaciones meteorológicas de SENAMHI iniciales; tras QC/gap-filling/homogenización
quedaron 93 estaciones para Sd, 182 para Td, 99 para Ws (Tabla 1). Buena cobertura en Andes y
costa, escasa en la Amazonía baja. La disponibilidad de datos aumentó fuertemente desde 1995
(antes de eso, ~70% menos datos, por inestabilidad social/política del país).

### Control de calidad (5 etapas)

1. Control de errores de codificación (secuencias repetidas de valores).
2. Control de rango físico (límites físicos por variable: Sd∈[0, máx horas sol por latitud];
   Td∈[−25°C, 30°C]; Ws∈[0, 40 m/s]).
3. Control de rango climático (outliers vía IQR: m=3.5 para Sd/Td, m=4.5 para Ws).
4. Comparación con estaciones vecinas (percentile rank, estaciones dentro de 70 km y <1000 m
   de diferencia de elevación; umbrales 0.8 para Sd/Td, 1 para Ws).
5. Control visual (inspección de series de tiempo diarias y frecuencias anuales de decimales).

### Relleno de vacíos (gap-filling)

Algoritmo basado en estaciones vecinas usando datos estandarizados (climatología diaria).
Condiciones: ≥5 años de datos en común y correlación mínima de 0.6; búsqueda iterativa (3
ciclos) con umbrales de distancia horizontal-vertical crecientes (70 km-1000 m, 100 km-1000 m,
150 km-sin límite vertical). Para completar series, se usaron "estaciones virtuales" de
ERA5-Land corregidas por quantile mapping (basado en anomalías, preservando climatología
diaria), usadas solo si tenían ≥7 años de datos y correlación mínima de 0.55 tras corrección.

### Homogenización

Test estándar de homogeneidad normal (SNHT), en su versión relativa (pairwise homogenization
algorithm, PHA) cuando había ≥8 estaciones vecinas con correlación ≥0.6 (radio 1000 km,
diferencia de elevación 1000 m), o absoluta si no. Aplicada a escala mensual; corrección
llevada a escala diaria vía interpolación de factores mensuales.

### Predictores espaciales

- **LST** (temperatura de superficie terrestre): MODIS MOD11A2, 1 km, promedios diurno/nocturno/
  medio 2000–2019.
- **CC** (frecuencia de nubosidad): EarthEnv, climatología 2000–2014, 1 km.
- **DEM** (elevación): GMTED2010, 1 km; de ahí también X, Y, y TDI (índice de disección
  topográfica, calculado a 5 escalas espaciales: 3, 6, 9, 12, 15 km).
- **WS_worldclim** (viento): WorldClim 2.1, climatología 1970–2000, 1 km.

### Interpolación espacial: climatologically aided interpolation

Enfoque en 3 pasos: (1) interpolación espacial de valores normales (climatología) vía
regression-kriging; (2) interpolación espacial de anomalías respecto a los normales (mismos
covariables + TDI); (3) agregación de 1+2 para obtener el valor real. Reduce costo
computacional vs. interpolar cada paso temporal independientemente, y preserva la
variabilidad promedio de ETo a escala nacional. Sd y Td se interpolaron en normales
(1981–2010) y anomalías (1981–2016); Ws solo en normales (por escasez/calidad de datos).

### Downscaling espacial de Tmax/Tmin

PISCOt (temperatura, resolución ~10 km/0.1°) se redujo a 0.01° usando geographically weighted
regression (GWR) con LST y DEM como covariables, en un proceso análogo (normales +
anomalías + agregación).

### Fórmula FAO Penman-Monteith aplicada

ETo = [0.408Δ(Rn−G) + γ(900/(T+273))u2(es−ea)] / [Δ+γ(1+0.34u2)]

- T: promedio de Tmax y Tmin.
- Rn = Rns − Rnl (radiación neta de onda corta menos onda larga saliente, vía Stefan-Boltzmann
  corregido por humedad/nubosidad).
- Rs (radiación solar) calculada con la fórmula de Angstrom a partir de Sd, usando as=0.25,
  bs=0.50 (sin calibración local, por falta de datos de radiación solar real).
- ea estimada a partir de Td, con corrección iterativa para mantener humedad relativa ≤100%.
- u2: normales grilladas de Ws como valor cuasi-constante (climatología mensual).
- G (flujo de calor del suelo) se ignora (G=0) a escala diaria.

## Datos generados

Archivos grillados en NetCDF (una variable por archivo, dimensiones tiempo/lat/lon) para
valores normales y diarios de Tmax, Tmin, Sd, Td, Ws, y ETo. Repositorio: figshare
(https://doi.org/10.6084/m9.figshare.c.5633182.v3 y
https://doi.org/10.6084/m9.figshare.19686738.v1).

## Validación técnica

Métricas: bias (error simple), MAE (error absoluto medio), y dr (índice de acuerdo refinado,
rango −1 a 1; dr>0.5 indica poder predictivo mayor al promedio observado).

### Validación del gap-filling (Sd, Td)

dr mediano de 0.76 (Sd) y 0.78 (Td); ningún dr<0.5 en ninguna estación. Buen desempeño
general, atribuido al uso de estaciones virtuales de ERA5-Land y preservación de la
climatología diaria.

### Validación independiente de ETo (train/test split)

39 estaciones con todas las subvariables disponibles ("ETo_conventional") separadas como test;
el resto usado para reconstruir PISCOeo_pm_for_cv (peor escenario, con menos estaciones que el
producto final). Comparado contra ETo_conventional, CRU_TS, TerraClimate y ERA5-Land a escala
diaria, mensual, anual y normal mensual (Tabla 4):

| Producto | Escala | bias (mm) | MAE (mm) | dr |
|---|---|---|---|---|
| PISCOeo_pm_for_cv | diaria | 0.08 | 0.52 | 0.67 |
| ERA5-Land | diaria | −0.22 | 0.69 | 0.55 |
| PISCOeo_pm_for_cv | mensual | 2.39 | 11.7 | 0.66 |
| CRU_TS | mensual | −14.3 | 16.18 | 0.37 |
| TerraClimate | mensual | −16.51 | 16.75 | 0.35 |
| ERA5-Land | mensual | −6.7 | 16.18 | 0.54 |
| PISCOeo_pm_for_cv | anual | 28.67 | 80.46 | −0.06 |
| CRU_TS | anual | −171.55 | 182.75 | −0.53 |
| TerraClimate | anual | −198.18 | 198.18 | −0.51 |
| ERA5-Land | anual | −80.42 | 162.13 | −0.45 |

PISCOeo_pm_for_cv tiene el mejor desempeño (dr>0.5) en todas las escalas salvo la anual, donde
todos los productos tienen baja eficiencia (dr<0.5) por acumulación de sesgos diarios. Orden
jerárquico de mejor a peor: PISCOeo_pm_for_cv, ERA5-Land, TerraClimate, CRU_TS. Peor desempeño
espacial en la costa (Pacific Coast).

### Comparación con productos globales (PISCOeo_pm completo, no cv)

Por regiones climáticas (Pacific Coast/PC, High Amazon/HA, Low Amazon/LA, Western Andes/WA,
Eastern Andes/EA):

- Los tres productos globales subestiman sistemáticamente ETo respecto a PISCOeo_pm, sobre
  todo en PC y WA.
- ERA5-Land tiene la mayor similitud espacial y de magnitud con PISCOeo_pm en general
  (especialmente en PC, EA, WA, HA); CRU_TS sigue mejor la señal mensual en HA y EA.
- Diferencias mayores en zonas áridas (costa) que húmedas (Amazonía) — patrón consistente con
  literatura previa (Singer et al. 2021), aunque con matices porque este estudio compara solo
  productos basados en FPM.
- Análisis de tendencias (1981–2016, pendiente de Sen): PISCOeo_pm muestra tendencias
  positivas significativas en todas las regiones salvo PC; ERA5-Land es el producto que más
  se acerca a esas tendencias en magnitud y dirección (salvo en LA, donde CRU_TS se acerca
  más). TerraClimate difiere en dirección de tendencia en casi todas las regiones.
- Posibles causas de discrepancia: baja resolución espacial de CRU_TS en terreno complejo;
  sesgos en radiación solar estimada (el término más influyente en errores de ETo según
  literatura) tanto en TerraClimate como en ERA5-Land.

### Estimación de incertidumbre de ETo

Se estimó la incertidumbre (ΔETo) vía propagación de errores (diferencias finitas de cada
variable de la fórmula FPM), a escala de grilla, para cada día 1981–2016. Mayor incertidumbre
en la costa (hasta 2.75 mm/día) y, en menor medida, en la Amazonía (1.5–2.25 mm/día); menor
en el norte y centro de los Andes (0–1 mm/día). Nota: esta incertidumbre solo cubre la
fórmula FPM en sí, no las etapas previas de preparación de datos (QC, gap-filling,
homogenización, interpolación, downscaling).

## Notas de uso (Usage Notes)

- La validación técnica priorizó ETo; el uso de las subvariables (Sd, Td, Ws) por separado no
  fue validado explícitamente.
- Los grids sobre cuerpos de agua (lagos, ríos) deben considerarse vacíos/enmascarados — el
  dataset solo debe usarse en áreas continentales.
- PISCOeo_pm es útil para caracterizar tendencias históricas de ETo, pero se recomienda
  complementar cualquier análisis de tendencias con datos de estaciones cuando sea posible.
- La fórmula FPM asume resistencia superficial mínima fija (sin respuesta a CO2 creciente),
  una limitación conocida bajo condiciones de cambio climático; no se aplicó ninguna
  corrección por esto, lo cual podría introducir sesgo en los años más recientes.
- Actualización esperada cada ~2 años, incorporando más observaciones (especialmente de la
  Amazonía y países vecinos).

## Código y datos disponibles

- Código (R 3.6.3, Python 3.8.5) para QC, gap-filling, homogenización, interpolación espacial
  y downscaling: figshare y GitHub
  (https://github.com/adrHuerta/PISCOeo_pm), bajo licencia GNU GPL v3.
- Datos grillados: figshare (ver DOIs arriba).

## Relación con otras fuentes de la wiki

Este paper es parte de la misma familia de productos PISCO/SENAMHI que
`[[sources/piscop-h-hourly-precipitation-peru]]` (PISCOp_h, precipitación horaria, mismo
grupo de autores: Huerta, Lavado-Casimiro). PISCOeo_pm usa PISCOt (temperatura) como insumo
directo (vía downscaling) y comparte la filosofía de "climatologically aided
interpolation"/normales+anomalías. No hay contradicción con PISCOp_h (variables distintas:
evapotranspiración de referencia vs. precipitación), pero ambos son insumos potenciales para
el dominio de tdew (variables meteorológicas derivadas para Perú).
