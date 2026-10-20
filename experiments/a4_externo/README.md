# A4: contraste externo de Td 2017-2020 (bead `tdew-ra6`)

Referencia de exactitud externa para los dos productos de Td 2017-2020 (Palacios `tuned` y
TimesFM `tmin_anom_full`), que no tienen Td observado de PISCO en ese periodo. La referencia
son estaciones sinópticas/METAR del Perú en NOAA NCEI ISD (global-hourly), y como segunda
referencia ERA5 y ERA5-Land en la coordenada de cada estación (API pública de Open-Meteo, sin
credenciales). Resultados y lectura: `reports/paper_nuevo/resultados/a4_contraste_externo.md`.

| Módulo | Qué hace |
|---|---|
| `download.py` | Descarga `isd-history.csv`, el ONI y los CSV anuales 2009-2020 de las estaciones con `CTRY=PE` (espejo de NOAA en AWS) |
| `isd.py` | Parseo de `DEW`/`TMP`, control de calidad y Td media diaria (día local UTC-5, cuatro bloques de 6 h) |
| `grid.py` | Mapeo lon/lat ↔ ID de la grilla PISCO 0,01° y lectura de celdas por bucket (solo lectura de `$RES`) |
| `openmeteo.py` | Td diaria de ERA5 y ERA5-Land en puntos y elevación DEM de la celda |
| `compare.py` | Pares estación–fuente, anomalías armónicas, métricas por estación, año y periodo, bootstrap por estaciones, desacuerdo entre productos con ONI y Niño 1+2 |
| `tmin_check.py` | Distribución de la Tmin regridada 2017-2020 frente a 2013-2016 en el panel nacional, costura dic/ene y textura espacial |

Orden de ejecución (los datos descargados van a `/home/cvelasquez/tdew_timesfm/a4/`, fuera del
repositorio; son datos no confiables y solo se leen con pandas/json):

```bash
uv run python -m experiments.a4_externo.download --out /home/cvelasquez/tdew_timesfm/a4
uv run python -m experiments.a4_externo.tmin_check
uv run python -m experiments.a4_externo.compare --work /home/cvelasquez/tdew_timesfm/a4
uv run python -m experiments.a4_externo.compare --work /home/cvelasquez/tdew_timesfm/a4 --min-blocks 2  # sensibilidad
uv run pytest tests/test_a4_isd.py
```

Criterio diario principal: al menos 4 horas válidas y al menos una en cada bloque local de 6 h
(00-06, 06-12, 12-18, 18-24); Td diaria = media de las cuatro medias de bloque. La variante
`--min-blocks 2` admite aeropuertos sin observación nocturna y se usa solo como sensibilidad.
