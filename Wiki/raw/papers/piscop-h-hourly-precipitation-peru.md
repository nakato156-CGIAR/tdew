# PISCOp_h: High-Resolution Gridded Hourly Precipitation Dataset for Peru

- **Venue/año**: Data in Brief, Volume 45, Article 108570. Publicado 2022-09-02 (impreso
  diciembre 2022).
- **DOI**: 10.1016/j.dib.2022.108570
- **PII**: S2352340922007776
- **PMCID**: PMC9486058
- **URL original**: enlace firmado de ScienceDirect (S3, expira en minutos) provisto por el
  usuario; no reutilizable. URL estable de referencia:
  https://www.sciencedirect.com/science/article/pii/S2352340922007776 (acceso bloqueado por
  paywall/anti-scraping, HTTP 403 en WebFetch directo).
- **Autores**: Adrian Huerta (autor de correspondencia, adrhuerta@gmail.com), Waldo
  Lavado-Casimiro, Oscar Felipe-Obando — Servicio Nacional de Meteorología e Hidrología
  (SENAMHI), Calle Cahuide 785, Jesús María, Lima, Perú.
- **Fecha de captura**: 2026-09-11

## Nota de captura

El enlace firmado de ScienceDirect (S3, `X-Amz-Expires=300`) no fue accesible vía WebFetch
(error "Invalid URL"), y la página estable de ScienceDirect devolvió HTTP 403 (bloqueo
anti-scraping). El contenido de este artículo se reconstruyó vía WebSearch (identificación
del PII/DOI/título) y WebFetch sobre el espejo de acceso abierto en PMC
(https://pmc.ncbi.nlm.nih.gov/articles/PMC9486058/), ya que *Data in Brief* es una revista
open-access. Contenido generado con asistencia de IA (Claude) — validar cifras exactas
contra el PDF original o el HTML de ScienceDirect/PMC antes de citarlas en trabajo downstream.

## Abstract

Este artículo presenta un dataset grillado de alta resolución (0.1°) de precipitación
horaria para Perú, para el período 2015–2020, llamado PISCOp_h. El producto se desarrolló
usando una técnica de desagregación temporal basada en el dataset diario grillado PISCOp y
datos adicionales de 309 estaciones meteorológicas automáticas y tres productos satelitales
de precipitación (IMERG-Early, PERSIANN-CCS, GSMaP_NRT). Basado en validación técnica,
PISCOp_h provee eficiencia de moderada a alta al caracterizar la frecuencia, intensidad y
coherencia temporal de la precipitación horaria, particularmente en el centro y sur de Perú.

## Descripción de los datos

### Resolución espacial y temporal

- **Espacial**: grilla de 0.1° × 0.1°.
- **Temporal**: resolución horaria, período 2015–2020.
- **Extensión geográfica**: 0.95°N–18.75°S, 81.25°W–68.05°W (todo el territorio peruano).

### Datos fuente

1. **Estaciones meteorológicas automáticas (AWS)**: 309 estaciones de la red SENAMHI.
2. **Productos satelitales**: IMERG-Early, PERSIANN-CCS, GSMaP_NRT.
3. **Dataset diario de referencia**: PISCOp v2.1 (producto combinado de estaciones +
   satélite).

### Metodología: desagregación temporal (temporal disaggregation)

Flujo de trabajo en cuatro etapas:

1. Crear SAT (satelital promedio) vía promedio lineal de los tres productos satelitales.
2. Interpolar espacialmente los datos de AWS usando Inverse Distance Weighting (IDW).
3. Aplicar corrección de sesgo del ciclo diurno a SAT usando algoritmos de quantile mapping
   con las observaciones de AWS, generando SATc (satelital corregido).
4. Desagregar los totales diarios de PISCOp usando los patrones horarios del satélite
   corregido — la fórmula de desagregación distribuye el total diario en fracciones
   horarias, preservando el total diario de precipitación.

Productos generados en el proceso: SAT (satelital sin corregir), SATc (satelital corregido
por sesgo), PISCOp_h_non-DBC (desagregado sin corrección de sesgo diurno), PISCOp_h
(producto final, con corrección de sesgo).

## Validación técnica

### Métricas

1. **Frequency ratio (Fr)**: compara la ocurrencia de horas húmedas (≥0.1 mm) entre el
   producto grillado y las observaciones.
2. **Intensity ratio (Ir)**: compara las tasas medias de precipitación durante períodos
   húmedos.
3. **Standardized Mean Absolute Difference (MAD)**: evalúa la coherencia/alineación
   temporal del ciclo horario.

### Resultados

- **Andes central y sur**: buen desempeño, con ratios (Fr, Ir) dentro de ±25% durante el
  verano austral.
- **Regiones del norte**: subestimación de la frecuencia y sobreestimación de la
  intensidad, particularmente en invierno.
- **Coherencia temporal**: valores de MAD tienden a ser menores a 0.25 en la mayor parte
  de Perú.
- **Efecto de la corrección de sesgo**: PISCOp_h (con corrección de sesgo diurno) muestra
  mejora sobre la versión no corregida (PISCOp_h_non-DBC).

## Tabla de especificaciones

| Atributo | Detalle |
|---|---|
| Subject area | Earth and Planetary Sciences |
| Área específica | Hidrología, meteorología, climatología |
| Tipo de dato | Archivos grillados georreferenciados |
| Formato | NetCDF (.nc), convenciones CF |
| Resolución espacial | 0.1° × 0.1° |
| Resolución temporal | Horaria |
| Período | 2015–2020 |
| Repositorio de datos | Figshare, https://doi.org/10.6084/m9.figshare.c.5743166 |

## Valor de los datos

- Primer producto grillado horario de precipitación construido vía desagregación temporal
  para Perú.
- Soporta calibración/validación de modelos hidrológicos a distintas escalas espaciales.
- Habilita el análisis de peligros por precipitación extrema a escala sub-diaria.
- Formato NetCDF con convenciones CF facilita su procesamiento e integración con otras
  variables (evapotranspiración, temperatura) — relevante para el dominio de tdew
  (estimación de evapotranspiración/variables meteorológicas derivadas).

## Repositorio de código asociado

- GitHub: https://github.com/adrHuerta/PISCOp_tdisaggregation (PISCOp_h: desagregación
  temporal, código del flujo de trabajo). No explorado en detalle en esta captura.
