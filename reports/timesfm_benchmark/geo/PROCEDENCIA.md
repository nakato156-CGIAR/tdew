# Procedencia de la geometría

`peru_departamental_simple.geojson` — límites de los 25 departamentos del Perú.

- **Fuente**: repositorio comunitario `juaneladio/peru-geojson` en GitHub, declarado en
  [`docs/protocol/week1_manifest.yaml`](../../../docs/protocol/week1_manifest.yaml) como la
  fuente de límites usada para seleccionar las celdas de los cuatro departamentos del
  estudio, mediante un join espacial con predicado `within` sobre el centro de cada celda.
- **Limitación que el propio manifiesto advierte**: no proviene de una fuente oficial
  INEI, IGN ni SENAMHI, y es de resolución "simple", de modo que celdas cercanas al borde
  departamental podrían quedar mal clasificadas por unos pocos kilómetros.
- **Por qué está aquí**: el archivo vivía solo en un directorio temporal fuera del
  repositorio. Se copió para que el artefacto que lo usa sea reproducible.
- 25 features, geometrías `Polygon` y `MultiPolygon`, CRS84, 136 KB compactado.
