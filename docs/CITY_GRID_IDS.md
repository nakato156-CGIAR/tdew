# IDs de celda PISCO — Lima, Cusco, Iquitos y Tarapoto

> Generado con asistencia de IA (Claude Code). Validar con el equipo / experto de dominio
> antes de usar en el pipeline o en reportes.

## Fuentes usadas

- `Data/silver/grid_index.parquet` — índice espacial real del proyecto (2,818,404 celdas
  de la grilla PISCO, columnas `ID`, `latitude`, `longitude`, resolución ~0.01°).
- Límites departamentales de Perú (fuente pública externa: [juaneladio/peru-geojson](
  https://github.com/juaneladio/peru-geojson), `peru_departamental_simple.geojson`).
  **No viene del paper PISCO ni de una fuente oficial interna** — es un shapefile de
  terceros con nivel de detalle "simple"; conviene confirmar contra un shapefile oficial
  (INEI/IGN) si esto va a producción.

Se hizo un *spatial join* (`geopandas.sjoin`, predicado `within`) entre los puntos de la
grilla y los polígonos departamentales de Lima, Cusco, Loreto (Iquitos) y San Martín
(Tarapoto).

## Resultado: todas las celdas por departamento

| Ciudad de referencia | Departamento | # celdas | Rango de `ID` | Rango lat | Rango lon | Archivo |
|---|---|---:|---|---|---|---|
| Lima | LIMA | 29,079 | 1,635,749 – 2,068,104 | -13.32 a -10.28 | -77.88 a -75.51 | `Data/silver/department_grid_ids/lima.csv` |
| Cusco | CUSCO | 60,041 | 1,766,965 – 2,370,085 | -15.44 a -11.20 | -73.97 a -70.40 | `Data/silver/department_grid_ids/cusco.csv` |
| Iquitos | LORETO | 305,564 | 181,215 – 1,412,592 | -8.71 a -0.05 | -77.82 a -69.95 | `Data/silver/department_grid_ids/iquitos_loreto.csv` |
| Tarapoto | SAN MARTIN | 41,835 | 943,152 – 1,423,939 | -8.79 a -5.41 | -77.77 a -75.49 | `Data/silver/department_grid_ids/tarapoto_san_martin.csv` |

**Total: 436,519 celdas** (~15.5% de las 2.82M celdas de la grilla PISCO).

Cada CSV tiene columnas `ID, latitude, longitude` y contiene **todas** las celdas cuyo
centro cae dentro del polígono departamental correspondiente — no es un bounding box,
sino la forma real del departamento (por eso Loreto, muy irregular y grande, tiene
~305K celdas).

## Celda puntual más cercana a cada ciudad (referencia rápida)

Si en vez del departamento completo se necesita solo el punto de la ciudad:

| Ciudad | Lat/Lon de referencia | `ID` de celda más cercana |
|---|---|---|
| Lima | -12.0464, -77.0428 | 1887430 |
| Cusco | -13.5320, -71.9675 | 2098393 |
| Iquitos | -3.7437, -73.2516 | 706127 |
| Tarapoto | -6.4772, -76.3714 | 1095443 |

## Cómo se generó (reproducible)

```python
import geopandas as gpd
import pandas as pd

# Límites departamentales (fuente externa, ver nota arriba)
depts = gpd.read_file("peru_departamental_simple.geojson")
target = {"LIMA": "lima", "CUSCO": "cusco", "LORETO": "iquitos_loreto",
          "SAN MARTIN": "tarapoto_san_martin"}
depts = depts[depts["NOMBDEP"].isin(target.keys())]

# Grilla PISCO real del proyecto
df = pd.read_parquet("Data/silver/grid_index.parquet")
pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude),
                        crs="EPSG:4326")

joined = gpd.sjoin(pts, depts[["NOMBDEP", "geometry"]], how="inner", predicate="within")

for dept, fname in target.items():
    sub = joined[joined["NOMBDEP"] == dept].sort_values("ID")[["ID", "latitude", "longitude"]]
    sub.to_csv(f"Data/silver/department_grid_ids/{fname}.csv", index=False)
```

## Advertencias / pendientes de validar

- El shapefile de departamentos es de un repositorio comunitario de GitHub, no de una
  fuente oficial (INEI/IGN/SENAMHI). Es "simple" (poca resolución de borde), por lo que
  celdas muy cerca del límite departamental podrían quedar mal clasificadas por unos
  pocos km.
- "Iquitos" y "Tarapoto" son ciudades específicas, no departamentos enteros — se usó
  Loreto y San Martín porque el usuario pidió el departamento/región completo. Si el
  Día 1 solo necesita la ciudad y su área metropolitana inmediata, usar la celda puntual
  de la tabla de arriba o pedir un bounding box más chico.
- Nadie del equipo ha validado todavía que estos límites departamentales sean los que
  Simcast/SENAMHI usan internamente para sus zonas climáticas (el proyecto ya maneja
  "41 zonas climáticas SENAMHI" en `docs/MODEL_INPUTS.md`, que es un esquema distinto a los
  24 departamentos).
