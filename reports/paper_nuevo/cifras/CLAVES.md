# Claves de cifras del paper nuevo

Generado por `experiments/paper_nuevo/cifras.py`; no se edita a mano. En Quarto se usa `{{< var clave >}}`.
Brecha = RMSE(A) − RMSE(B) en °C; negativa favorece a A. `n. d.` indica que la cifra no existe en las fuentes.

Total de claves: 5872.

## filas

| clave | valor | significado |
|---|---|---|
| `filas.ll4b.panel` | 24.876.447 | Filas celda × día puntuadas en `ll4b`, dominio completo |
| `filas.ll4b.peru` | 12.085.392 | Filas celda × día puntuadas en `ll4b`, Perú |
| `filas.ll4.panel` | 24.876.447 | Filas celda × día puntuadas en `ll4`, dominio completo |
| `filas.ll4.peru` | 12.085.392 | Filas celda × día puntuadas en `ll4`, Perú |

## celdas

| clave | valor | significado |
|---|---|---|
| `celdas.ll4b.panel` | 17.027 | Celdas puntuadas en `ll4b`, dominio completo |
| `celdas.ll4b.peru` | 8.272 | Celdas puntuadas en `ll4b`, Perú |
| `celdas.ll4.panel` | 17.027 | Celdas puntuadas en `ll4`, dominio completo |
| `celdas.ll4.peru` | 8.272 | Celdas puntuadas en `ll4`, Perú |

## panel

| clave | valor | significado |
|---|---|---|
| `panel.celdas` | 17.027 | Celdas puntuadas del dominio completo (panel) |
| `panel.celdas_peru` | 8.272 | Celdas del panel dentro del contorno de Perú |
| `panel.celdas_fuera` | 8.755 | Celdas del panel fuera de Perú |
| `panel.pct_fuera` | 51,4 | Porcentaje del panel fuera de Perú (sin símbolo %) |
| `panel.dias_por_celda` | 1.461 | Días evaluados por celda en cada bloque |
| `panel.zonas_panel` | 33 | Unidades cartográficas con celdas en el panel |
| `panel.zonas_peru` | 32 | Unidades cartográficas con celdas dentro de Perú |
| `panel.zonas_sin_peru` | 1 | Zonas del panel sin celdas dentro de Perú (etiquetas: Lago Titicaca) |
| `panel.unidades_total` | 41 | Unidades cartográficas SENAMHI (zone_table) |
| `panel.unidades_extra` | 3 | Unidades adicionales (lagos y lomas costeras) (etiquetas: Lago Junín, Lago Titicaca y Loma) |
| `panel.tipos_climaticos` | 38 | Tipos climáticos (incluye 'Glaciar') |

## bloques

| clave | valor | significado |
|---|---|---|
| `bloques.ll4b.anio_ini` | 2009 | Primer año de prueba de `ll4b` |
| `bloques.ll4b.anio_fin` | 2012 | Último año de prueba de `ll4b` |
| `bloques.ll4b.n_anios` | 4 | Años de prueba de `ll4b` |
| `bloques.ll4b.contexto_ini` | 1981 | Primer año de contexto de `ll4b` |
| `bloques.ll4b.contexto_fin` | 2008 | Último año de contexto de `ll4b` |
| `bloques.ll4b.anios_contexto` | 28 | Años de contexto de la referencia de TimesFM en `ll4b` |
| `bloques.ll4.anio_ini` | 2013 | Primer año de prueba de `ll4` |
| `bloques.ll4.anio_fin` | 2016 | Último año de prueba de `ll4` |
| `bloques.ll4.n_anios` | 4 | Años de prueba de `ll4` |
| `bloques.ll4.contexto_ini` | 1981 | Primer año de contexto de `ll4` |
| `bloques.ll4.contexto_fin` | 2012 | Último año de contexto de `ll4` |
| `bloques.ll4.anios_contexto` | 32 | Años de contexto de la referencia de TimesFM en `ll4` |
| `bloques.n_anios_total` | 8 | Años evaluados en total |
| `bloques.anio_min` | 2009 | Primer año evaluado |
| `bloques.anio_max` | 2016 | Último año evaluado |

## bootstrap

| clave | valor | significado |
|---|---|---|
| `bootstrap.replicas` | 2.000 | Réplicas del bootstrap pareado |
| `bootstrap.semilla` | 0 | Semilla del bootstrap |
| `bootstrap.bloque_grados` | 2 | Lado (°) de los bloques espaciales |
| `bootstrap.bloques.espacial.panel` | 74 | Bloques del esquema espacial en dominio completo |
| `bootstrap.bloques.espacial.peru` | 45 | Bloques del esquema espacial en Perú |
| `bootstrap.bloques.mes_anio.panel` | 48 | Bloques del esquema mes_anio en dominio completo |
| `bootstrap.bloques.mes_anio.peru` | 48 | Bloques del esquema mes_anio en Perú |
| `bootstrap.nivel` | 95 | Nivel (%) de los IC bootstrap, sin símbolo % |
| `bootstrap.percentil_inf` | 2,5 | Percentil inferior (%) del IC bootstrap |
| `bootstrap.percentil_sup` | 97,5 | Percentil superior (%) del IC bootstrap |

## rmse

| clave | valor | significado |
|---|---|---|
| `rmse.ll4.panel.clim` | 1,535 | RMSE (°C), climatología, `ll4`, dominio completo |
| `rmse.ll4.panel.tuned` | 1,228 | RMSE (°C), tuned, `ll4`, dominio completo |
| `rmse.ll4.panel.tuned_sin_td` | 1,174 | RMSE (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse.ll4.panel.llr_simple` | 1,175 | RMSE (°C), LLR simple, `ll4`, dominio completo |
| `rmse.ll4.panel.llr_rezagos` | 1,161 | RMSE (°C), LLR con rezagos, `ll4`, dominio completo |
| `rmse.ll4.panel.llr_simple_sel` | 1,172 | RMSE (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `rmse.ll4.panel.llr_rezagos_sel` | 1,157 | RMSE (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse.ll4.panel.timesfm` | 1,154 | RMSE (°C), TimesFM, `ll4`, dominio completo |
| `rmse.ll4.panel.timesfm_med` | 1,201 | RMSE (°C), TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse.ll4.peru.clim` | 1,262 | RMSE (°C), climatología, `ll4`, Perú |
| `rmse.ll4.peru.tuned` | 0,944 | RMSE (°C), tuned, `ll4`, Perú |
| `rmse.ll4.peru.tuned_sin_td` | 0,908 | RMSE (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `rmse.ll4.peru.llr_simple` | 0,912 | RMSE (°C), LLR simple, `ll4`, Perú |
| `rmse.ll4.peru.llr_rezagos` | 0,897 | RMSE (°C), LLR con rezagos, `ll4`, Perú |
| `rmse.ll4.peru.llr_simple_sel` | 0,906 | RMSE (°C), LLR simple seleccionado, `ll4`, Perú |
| `rmse.ll4.peru.llr_rezagos_sel` | 0,891 | RMSE (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse.ll4.peru.timesfm` | 0,865 | RMSE (°C), TimesFM, `ll4`, Perú |
| `rmse.ll4.peru.timesfm_med` | 0,903 | RMSE (°C), TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse.ll4b.panel.clim` | 1,362 | RMSE (°C), climatología, `ll4b`, dominio completo |
| `rmse.ll4b.panel.tuned` | 1,122 | RMSE (°C), tuned, `ll4b`, dominio completo |
| `rmse.ll4b.panel.tuned_sin_td` | 1,108 | RMSE (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse.ll4b.panel.llr_simple` | 1,098 | RMSE (°C), LLR simple, `ll4b`, dominio completo |
| `rmse.ll4b.panel.llr_rezagos` | 1,089 | RMSE (°C), LLR con rezagos, `ll4b`, dominio completo |
| `rmse.ll4b.panel.llr_simple_sel` | 1,083 | RMSE (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse.ll4b.panel.llr_rezagos_sel` | 1,074 | RMSE (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse.ll4b.panel.timesfm_td` | 1,106 | RMSE (°C), TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse.ll4b.panel.timesfm` | 1,046 | RMSE (°C), TimesFM, `ll4b`, dominio completo |
| `rmse.ll4b.panel.timesfm_med` | 1,108 | RMSE (°C), TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse.ll4b.peru.clim` | 1,087 | RMSE (°C), climatología, `ll4b`, Perú |
| `rmse.ll4b.peru.tuned` | 0,861 | RMSE (°C), tuned, `ll4b`, Perú |
| `rmse.ll4b.peru.tuned_sin_td` | 0,856 | RMSE (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse.ll4b.peru.llr_simple` | 0,849 | RMSE (°C), LLR simple, `ll4b`, Perú |
| `rmse.ll4b.peru.llr_rezagos` | 0,844 | RMSE (°C), LLR con rezagos, `ll4b`, Perú |
| `rmse.ll4b.peru.llr_simple_sel` | 0,834 | RMSE (°C), LLR simple seleccionado, `ll4b`, Perú |
| `rmse.ll4b.peru.llr_rezagos_sel` | 0,830 | RMSE (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse.ll4b.peru.timesfm_td` | 0,840 | RMSE (°C), TimesFM en Td cruda, `ll4b`, Perú |
| `rmse.ll4b.peru.timesfm` | 0,804 | RMSE (°C), TimesFM, `ll4b`, Perú |
| `rmse.ll4b.peru.timesfm_med` | 0,849 | RMSE (°C), TimesFM con contexto desde 2002, `ll4b`, Perú |

## rmse4

| clave | valor | significado |
|---|---|---|
| `rmse4.ll4.panel.clim` | 1,5352 | RMSE (°C) con 4 decimales, climatología, `ll4`, dominio completo |
| `rmse4.ll4.panel.tuned` | 1,2279 | RMSE (°C) con 4 decimales, tuned, `ll4`, dominio completo |
| `rmse4.ll4.panel.tuned_sin_td` | 1,1742 | RMSE (°C) con 4 decimales, tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse4.ll4.panel.llr_simple` | 1,1748 | RMSE (°C) con 4 decimales, LLR simple, `ll4`, dominio completo |
| `rmse4.ll4.panel.llr_rezagos` | 1,1611 | RMSE (°C) con 4 decimales, LLR con rezagos, `ll4`, dominio completo |
| `rmse4.ll4.panel.llr_simple_sel` | 1,1718 | RMSE (°C) con 4 decimales, LLR simple seleccionado, `ll4`, dominio completo |
| `rmse4.ll4.panel.llr_rezagos_sel` | 1,1567 | RMSE (°C) con 4 decimales, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse4.ll4.panel.timesfm` | 1,1536 | RMSE (°C) con 4 decimales, TimesFM, `ll4`, dominio completo |
| `rmse4.ll4.panel.timesfm_med` | 1,2009 | RMSE (°C) con 4 decimales, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse4.ll4.peru.clim` | 1,2618 | RMSE (°C) con 4 decimales, climatología, `ll4`, Perú |
| `rmse4.ll4.peru.tuned` | 0,9443 | RMSE (°C) con 4 decimales, tuned, `ll4`, Perú |
| `rmse4.ll4.peru.tuned_sin_td` | 0,9078 | RMSE (°C) con 4 decimales, tuned sin rezagos de Td, `ll4`, Perú |
| `rmse4.ll4.peru.llr_simple` | 0,9121 | RMSE (°C) con 4 decimales, LLR simple, `ll4`, Perú |
| `rmse4.ll4.peru.llr_rezagos` | 0,8973 | RMSE (°C) con 4 decimales, LLR con rezagos, `ll4`, Perú |
| `rmse4.ll4.peru.llr_simple_sel` | 0,9061 | RMSE (°C) con 4 decimales, LLR simple seleccionado, `ll4`, Perú |
| `rmse4.ll4.peru.llr_rezagos_sel` | 0,8907 | RMSE (°C) con 4 decimales, LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse4.ll4.peru.timesfm` | 0,8651 | RMSE (°C) con 4 decimales, TimesFM, `ll4`, Perú |
| `rmse4.ll4.peru.timesfm_med` | 0,9026 | RMSE (°C) con 4 decimales, TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse4.ll4b.panel.clim` | 1,3618 | RMSE (°C) con 4 decimales, climatología, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.tuned` | 1,1220 | RMSE (°C) con 4 decimales, tuned, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.tuned_sin_td` | 1,1082 | RMSE (°C) con 4 decimales, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.llr_simple` | 1,0984 | RMSE (°C) con 4 decimales, LLR simple, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.llr_rezagos` | 1,0891 | RMSE (°C) con 4 decimales, LLR con rezagos, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.llr_simple_sel` | 1,0831 | RMSE (°C) con 4 decimales, LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.llr_rezagos_sel` | 1,0745 | RMSE (°C) con 4 decimales, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.timesfm_td` | 1,1058 | RMSE (°C) con 4 decimales, TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.timesfm` | 1,0463 | RMSE (°C) con 4 decimales, TimesFM, `ll4b`, dominio completo |
| `rmse4.ll4b.panel.timesfm_med` | 1,1083 | RMSE (°C) con 4 decimales, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse4.ll4b.peru.clim` | 1,0873 | RMSE (°C) con 4 decimales, climatología, `ll4b`, Perú |
| `rmse4.ll4b.peru.tuned` | 0,8607 | RMSE (°C) con 4 decimales, tuned, `ll4b`, Perú |
| `rmse4.ll4b.peru.tuned_sin_td` | 0,8559 | RMSE (°C) con 4 decimales, tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse4.ll4b.peru.llr_simple` | 0,8485 | RMSE (°C) con 4 decimales, LLR simple, `ll4b`, Perú |
| `rmse4.ll4b.peru.llr_rezagos` | 0,8437 | RMSE (°C) con 4 decimales, LLR con rezagos, `ll4b`, Perú |
| `rmse4.ll4b.peru.llr_simple_sel` | 0,8340 | RMSE (°C) con 4 decimales, LLR simple seleccionado, `ll4b`, Perú |
| `rmse4.ll4b.peru.llr_rezagos_sel` | 0,8297 | RMSE (°C) con 4 decimales, LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse4.ll4b.peru.timesfm_td` | 0,8398 | RMSE (°C) con 4 decimales, TimesFM en Td cruda, `ll4b`, Perú |
| `rmse4.ll4b.peru.timesfm` | 0,8043 | RMSE (°C) con 4 decimales, TimesFM, `ll4b`, Perú |
| `rmse4.ll4b.peru.timesfm_med` | 0,8488 | RMSE (°C) con 4 decimales, TimesFM con contexto desde 2002, `ll4b`, Perú |

## mae

| clave | valor | significado |
|---|---|---|
| `mae.ll4.panel.clim` | 1,136 | MAE (°C), climatología, `ll4`, dominio completo |
| `mae.ll4.panel.tuned` | 0,881 | MAE (°C), tuned, `ll4`, dominio completo |
| `mae.ll4.panel.tuned_sin_td` | 0,851 | MAE (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `mae.ll4.panel.llr_simple` | 0,856 | MAE (°C), LLR simple, `ll4`, dominio completo |
| `mae.ll4.panel.llr_rezagos` | 0,843 | MAE (°C), LLR con rezagos, `ll4`, dominio completo |
| `mae.ll4.panel.llr_simple_sel` | 0,852 | MAE (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `mae.ll4.panel.llr_rezagos_sel` | 0,840 | MAE (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `mae.ll4.panel.timesfm` | 0,830 | MAE (°C), TimesFM, `ll4`, dominio completo |
| `mae.ll4.panel.timesfm_med` | 0,867 | MAE (°C), TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `mae.ll4.peru.clim` | 0,954 | MAE (°C), climatología, `ll4`, Perú |
| `mae.ll4.peru.tuned` | 0,695 | MAE (°C), tuned, `ll4`, Perú |
| `mae.ll4.peru.tuned_sin_td` | 0,673 | MAE (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `mae.ll4.peru.llr_simple` | 0,679 | MAE (°C), LLR simple, `ll4`, Perú |
| `mae.ll4.peru.llr_rezagos` | 0,666 | MAE (°C), LLR con rezagos, `ll4`, Perú |
| `mae.ll4.peru.llr_simple_sel` | 0,675 | MAE (°C), LLR simple seleccionado, `ll4`, Perú |
| `mae.ll4.peru.llr_rezagos_sel` | 0,661 | MAE (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `mae.ll4.peru.timesfm` | 0,638 | MAE (°C), TimesFM, `ll4`, Perú |
| `mae.ll4.peru.timesfm_med` | 0,667 | MAE (°C), TimesFM con contexto desde 2002, `ll4`, Perú |
| `mae.ll4b.panel.clim` | 1,016 | MAE (°C), climatología, `ll4b`, dominio completo |
| `mae.ll4b.panel.tuned` | 0,820 | MAE (°C), tuned, `ll4b`, dominio completo |
| `mae.ll4b.panel.tuned_sin_td` | 0,809 | MAE (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `mae.ll4b.panel.llr_simple` | 0,802 | MAE (°C), LLR simple, `ll4b`, dominio completo |
| `mae.ll4b.panel.llr_rezagos` | 0,796 | MAE (°C), LLR con rezagos, `ll4b`, dominio completo |
| `mae.ll4b.panel.llr_simple_sel` | 0,793 | MAE (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `mae.ll4b.panel.llr_rezagos_sel` | 0,787 | MAE (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `mae.ll4b.panel.timesfm_td` | 0,815 | MAE (°C), TimesFM en Td cruda, `ll4b`, dominio completo |
| `mae.ll4b.panel.timesfm` | 0,768 | MAE (°C), TimesFM, `ll4b`, dominio completo |
| `mae.ll4b.panel.timesfm_med` | 0,818 | MAE (°C), TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `mae.ll4b.peru.clim` | 0,829 | MAE (°C), climatología, `ll4b`, Perú |
| `mae.ll4b.peru.tuned` | 0,644 | MAE (°C), tuned, `ll4b`, Perú |
| `mae.ll4b.peru.tuned_sin_td` | 0,638 | MAE (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `mae.ll4b.peru.llr_simple` | 0,634 | MAE (°C), LLR simple, `ll4b`, Perú |
| `mae.ll4b.peru.llr_rezagos` | 0,631 | MAE (°C), LLR con rezagos, `ll4b`, Perú |
| `mae.ll4b.peru.llr_simple_sel` | 0,626 | MAE (°C), LLR simple seleccionado, `ll4b`, Perú |
| `mae.ll4b.peru.llr_rezagos_sel` | 0,622 | MAE (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `mae.ll4b.peru.timesfm_td` | 0,634 | MAE (°C), TimesFM en Td cruda, `ll4b`, Perú |
| `mae.ll4b.peru.timesfm` | 0,602 | MAE (°C), TimesFM, `ll4b`, Perú |
| `mae.ll4b.peru.timesfm_med` | 0,639 | MAE (°C), TimesFM con contexto desde 2002, `ll4b`, Perú |

## sesgo

| clave | valor | significado |
|---|---|---|
| `sesgo.ll4.panel.clim` | −0,363 | Sesgo (°C), climatología, `ll4`, dominio completo |
| `sesgo.ll4.panel.tuned` | −0,033 | Sesgo (°C), tuned, `ll4`, dominio completo |
| `sesgo.ll4.panel.tuned_sin_td` | +0,014 | Sesgo (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `sesgo.ll4.panel.llr_simple` | −0,010 | Sesgo (°C), LLR simple, `ll4`, dominio completo |
| `sesgo.ll4.panel.llr_rezagos` | +0,025 | Sesgo (°C), LLR con rezagos, `ll4`, dominio completo |
| `sesgo.ll4.panel.llr_simple_sel` | −0,002 | Sesgo (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `sesgo.ll4.panel.llr_rezagos_sel` | +0,036 | Sesgo (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `sesgo.ll4.panel.timesfm` | +0,104 | Sesgo (°C), TimesFM, `ll4`, dominio completo |
| `sesgo.ll4.panel.timesfm_med` | +0,201 | Sesgo (°C), TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `sesgo.ll4.peru.clim` | −0,301 | Sesgo (°C), climatología, `ll4`, Perú |
| `sesgo.ll4.peru.tuned` | +0,010 | Sesgo (°C), tuned, `ll4`, Perú |
| `sesgo.ll4.peru.tuned_sin_td` | +0,047 | Sesgo (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `sesgo.ll4.peru.llr_simple` | +0,009 | Sesgo (°C), LLR simple, `ll4`, Perú |
| `sesgo.ll4.peru.llr_rezagos` | +0,059 | Sesgo (°C), LLR con rezagos, `ll4`, Perú |
| `sesgo.ll4.peru.llr_simple_sel` | −0,014 | Sesgo (°C), LLR simple seleccionado, `ll4`, Perú |
| `sesgo.ll4.peru.llr_rezagos_sel` | +0,034 | Sesgo (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `sesgo.ll4.peru.timesfm` | +0,050 | Sesgo (°C), TimesFM, `ll4`, Perú |
| `sesgo.ll4.peru.timesfm_med` | +0,098 | Sesgo (°C), TimesFM con contexto desde 2002, `ll4`, Perú |
| `sesgo.ll4b.panel.clim` | −0,300 | Sesgo (°C), climatología, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.tuned` | −0,156 | Sesgo (°C), tuned, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.tuned_sin_td` | −0,124 | Sesgo (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.llr_simple` | −0,140 | Sesgo (°C), LLR simple, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.llr_rezagos` | −0,117 | Sesgo (°C), LLR con rezagos, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.llr_simple_sel` | −0,138 | Sesgo (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.llr_rezagos_sel` | −0,117 | Sesgo (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.timesfm_td` | +0,035 | Sesgo (°C), TimesFM en Td cruda, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.timesfm` | −0,108 | Sesgo (°C), TimesFM, `ll4b`, dominio completo |
| `sesgo.ll4b.panel.timesfm_med` | +0,089 | Sesgo (°C), TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `sesgo.ll4b.peru.clim` | −0,203 | Sesgo (°C), climatología, `ll4b`, Perú |
| `sesgo.ll4b.peru.tuned` | −0,060 | Sesgo (°C), tuned, `ll4b`, Perú |
| `sesgo.ll4b.peru.tuned_sin_td` | −0,034 | Sesgo (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `sesgo.ll4b.peru.llr_simple` | −0,056 | Sesgo (°C), LLR simple, `ll4b`, Perú |
| `sesgo.ll4b.peru.llr_rezagos` | −0,028 | Sesgo (°C), LLR con rezagos, `ll4b`, Perú |
| `sesgo.ll4b.peru.llr_simple_sel` | −0,083 | Sesgo (°C), LLR simple seleccionado, `ll4b`, Perú |
| `sesgo.ll4b.peru.llr_rezagos_sel` | −0,062 | Sesgo (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `sesgo.ll4b.peru.timesfm_td` | −0,003 | Sesgo (°C), TimesFM en Td cruda, `ll4b`, Perú |
| `sesgo.ll4b.peru.timesfm` | −0,085 | Sesgo (°C), TimesFM, `ll4b`, Perú |
| `sesgo.ll4b.peru.timesfm_med` | −0,004 | Sesgo (°C), TimesFM con contexto desde 2002, `ll4b`, Perú |

## rmse_macro

| clave | valor | significado |
|---|---|---|
| `rmse_macro.ll4.panel.clim` | 1,249 | RMSE macro por zona (°C), climatología, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.tuned` | 0,901 | RMSE macro por zona (°C), tuned, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.tuned_sin_td` | 0,875 | RMSE macro por zona (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.llr_simple` | 0,874 | RMSE macro por zona (°C), LLR simple, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.llr_rezagos` | 0,861 | RMSE macro por zona (°C), LLR con rezagos, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.llr_simple_sel` | 0,856 | RMSE macro por zona (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.llr_rezagos_sel` | 0,840 | RMSE macro por zona (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.timesfm` | 0,802 | RMSE macro por zona (°C), TimesFM, `ll4`, dominio completo |
| `rmse_macro.ll4.panel.timesfm_med` | 0,828 | RMSE macro por zona (°C), TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse_macro.ll4.peru.clim` | 1,226 | RMSE macro por zona (°C), climatología, `ll4`, Perú |
| `rmse_macro.ll4.peru.tuned` | 0,884 | RMSE macro por zona (°C), tuned, `ll4`, Perú |
| `rmse_macro.ll4.peru.tuned_sin_td` | 0,861 | RMSE macro por zona (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `rmse_macro.ll4.peru.llr_simple` | 0,861 | RMSE macro por zona (°C), LLR simple, `ll4`, Perú |
| `rmse_macro.ll4.peru.llr_rezagos` | 0,847 | RMSE macro por zona (°C), LLR con rezagos, `ll4`, Perú |
| `rmse_macro.ll4.peru.llr_simple_sel` | 0,844 | RMSE macro por zona (°C), LLR simple seleccionado, `ll4`, Perú |
| `rmse_macro.ll4.peru.llr_rezagos_sel` | 0,828 | RMSE macro por zona (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse_macro.ll4.peru.timesfm` | 0,787 | RMSE macro por zona (°C), TimesFM, `ll4`, Perú |
| `rmse_macro.ll4.peru.timesfm_med` | 0,811 | RMSE macro por zona (°C), TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse_macro.ll4b.panel.clim` | 1,115 | RMSE macro por zona (°C), climatología, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.tuned` | 0,825 | RMSE macro por zona (°C), tuned, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.tuned_sin_td` | 0,808 | RMSE macro por zona (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.llr_simple` | 0,798 | RMSE macro por zona (°C), LLR simple, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.llr_rezagos` | 0,793 | RMSE macro por zona (°C), LLR con rezagos, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.llr_simple_sel` | 0,778 | RMSE macro por zona (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.llr_rezagos_sel` | 0,770 | RMSE macro por zona (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.timesfm_td` | 0,769 | RMSE macro por zona (°C), TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.timesfm` | 0,745 | RMSE macro por zona (°C), TimesFM, `ll4b`, dominio completo |
| `rmse_macro.ll4b.panel.timesfm_med` | 0,789 | RMSE macro por zona (°C), TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse_macro.ll4b.peru.clim` | 1,083 | RMSE macro por zona (°C), climatología, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.tuned` | 0,808 | RMSE macro por zona (°C), tuned, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.tuned_sin_td` | 0,792 | RMSE macro por zona (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.llr_simple` | 0,782 | RMSE macro por zona (°C), LLR simple, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.llr_rezagos` | 0,778 | RMSE macro por zona (°C), LLR con rezagos, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.llr_simple_sel` | 0,763 | RMSE macro por zona (°C), LLR simple seleccionado, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.llr_rezagos_sel` | 0,756 | RMSE macro por zona (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.timesfm_td` | 0,750 | RMSE macro por zona (°C), TimesFM en Td cruda, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.timesfm` | 0,729 | RMSE macro por zona (°C), TimesFM, `ll4b`, Perú |
| `rmse_macro.ll4b.peru.timesfm_med` | 0,774 | RMSE macro por zona (°C), TimesFM con contexto desde 2002, `ll4b`, Perú |

## rmse_anual

| clave | valor | significado |
|---|---|---|
| `rmse_anual.ll4.panel.clim.a2013` | 1,393 | RMSE (°C) del año 2013, climatología, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned.a2013` | 1,149 | RMSE (°C) del año 2013, tuned, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned_sin_td.a2013` | 1,154 | RMSE (°C) del año 2013, tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple.a2013` | 1,143 | RMSE (°C) del año 2013, LLR simple, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos.a2013` | 1,137 | RMSE (°C) del año 2013, LLR con rezagos, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple_sel.a2013` | 1,159 | RMSE (°C) del año 2013, LLR simple seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos_sel.a2013` | 1,145 | RMSE (°C) del año 2013, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm.a2013` | 1,205 | RMSE (°C) del año 2013, TimesFM, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm_med.a2013` | 1,281 | RMSE (°C) del año 2013, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.clim.a2014` | 1,391 | RMSE (°C) del año 2014, climatología, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned.a2014` | 1,186 | RMSE (°C) del año 2014, tuned, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned_sin_td.a2014` | 1,151 | RMSE (°C) del año 2014, tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple.a2014` | 1,152 | RMSE (°C) del año 2014, LLR simple, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos.a2014` | 1,148 | RMSE (°C) del año 2014, LLR con rezagos, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple_sel.a2014` | 1,147 | RMSE (°C) del año 2014, LLR simple seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos_sel.a2014` | 1,149 | RMSE (°C) del año 2014, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm.a2014` | 1,127 | RMSE (°C) del año 2014, TimesFM, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm_med.a2014` | 1,188 | RMSE (°C) del año 2014, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.clim.a2015` | 1,648 | RMSE (°C) del año 2015, climatología, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned.a2015` | 1,245 | RMSE (°C) del año 2015, tuned, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned_sin_td.a2015` | 1,166 | RMSE (°C) del año 2015, tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple.a2015` | 1,172 | RMSE (°C) del año 2015, LLR simple, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos.a2015` | 1,142 | RMSE (°C) del año 2015, LLR con rezagos, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple_sel.a2015` | 1,156 | RMSE (°C) del año 2015, LLR simple seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos_sel.a2015` | 1,130 | RMSE (°C) del año 2015, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm.a2015` | 1,080 | RMSE (°C) del año 2015, TimesFM, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm_med.a2015` | 1,115 | RMSE (°C) del año 2015, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.clim.a2016` | 1,684 | RMSE (°C) del año 2016, climatología, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned.a2016` | 1,324 | RMSE (°C) del año 2016, tuned, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.tuned_sin_td.a2016` | 1,224 | RMSE (°C) del año 2016, tuned sin rezagos de Td, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple.a2016` | 1,231 | RMSE (°C) del año 2016, LLR simple, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos.a2016` | 1,215 | RMSE (°C) del año 2016, LLR con rezagos, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_simple_sel.a2016` | 1,224 | RMSE (°C) del año 2016, LLR simple seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.llr_rezagos_sel.a2016` | 1,202 | RMSE (°C) del año 2016, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm.a2016` | 1,199 | RMSE (°C) del año 2016, TimesFM, `ll4`, dominio completo |
| `rmse_anual.ll4.panel.timesfm_med.a2016` | 1,214 | RMSE (°C) del año 2016, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `rmse_anual.ll4.peru.clim.a2013` | 1,123 | RMSE (°C) del año 2013, climatología, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned.a2013` | 0,883 | RMSE (°C) del año 2013, tuned, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned_sin_td.a2013` | 0,879 | RMSE (°C) del año 2013, tuned sin rezagos de Td, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple.a2013` | 0,870 | RMSE (°C) del año 2013, LLR simple, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos.a2013` | 0,868 | RMSE (°C) del año 2013, LLR con rezagos, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple_sel.a2013` | 0,876 | RMSE (°C) del año 2013, LLR simple seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos_sel.a2013` | 0,869 | RMSE (°C) del año 2013, LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm.a2013` | 0,858 | RMSE (°C) del año 2013, TimesFM, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm_med.a2013` | 0,929 | RMSE (°C) del año 2013, TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse_anual.ll4.peru.clim.a2014` | 1,147 | RMSE (°C) del año 2014, climatología, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned.a2014` | 0,932 | RMSE (°C) del año 2014, tuned, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned_sin_td.a2014` | 0,905 | RMSE (°C) del año 2014, tuned sin rezagos de Td, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple.a2014` | 0,905 | RMSE (°C) del año 2014, LLR simple, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos.a2014` | 0,901 | RMSE (°C) del año 2014, LLR con rezagos, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple_sel.a2014` | 0,896 | RMSE (°C) del año 2014, LLR simple seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos_sel.a2014` | 0,895 | RMSE (°C) del año 2014, LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm.a2014` | 0,861 | RMSE (°C) del año 2014, TimesFM, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm_med.a2014` | 0,897 | RMSE (°C) del año 2014, TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse_anual.ll4.peru.clim.a2015` | 1,372 | RMSE (°C) del año 2015, climatología, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned.a2015` | 0,973 | RMSE (°C) del año 2015, tuned, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned_sin_td.a2015` | 0,910 | RMSE (°C) del año 2015, tuned sin rezagos de Td, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple.a2015` | 0,921 | RMSE (°C) del año 2015, LLR simple, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos.a2015` | 0,890 | RMSE (°C) del año 2015, LLR con rezagos, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple_sel.a2015` | 0,910 | RMSE (°C) del año 2015, LLR simple seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos_sel.a2015` | 0,882 | RMSE (°C) del año 2015, LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm.a2015` | 0,836 | RMSE (°C) del año 2015, TimesFM, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm_med.a2015` | 0,865 | RMSE (°C) del año 2015, TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse_anual.ll4.peru.clim.a2016` | 1,381 | RMSE (°C) del año 2016, climatología, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned.a2016` | 0,985 | RMSE (°C) del año 2016, tuned, `ll4`, Perú |
| `rmse_anual.ll4.peru.tuned_sin_td.a2016` | 0,937 | RMSE (°C) del año 2016, tuned sin rezagos de Td, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple.a2016` | 0,950 | RMSE (°C) del año 2016, LLR simple, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos.a2016` | 0,929 | RMSE (°C) del año 2016, LLR con rezagos, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_simple_sel.a2016` | 0,940 | RMSE (°C) del año 2016, LLR simple seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.llr_rezagos_sel.a2016` | 0,915 | RMSE (°C) del año 2016, LLR con rezagos seleccionado, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm.a2016` | 0,903 | RMSE (°C) del año 2016, TimesFM, `ll4`, Perú |
| `rmse_anual.ll4.peru.timesfm_med.a2016` | 0,918 | RMSE (°C) del año 2016, TimesFM con contexto desde 2002, `ll4`, Perú |
| `rmse_anual.ll4b.panel.clim.a2009` | 1,241 | RMSE (°C) del año 2009, climatología, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned.a2009` | 1,035 | RMSE (°C) del año 2009, tuned, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned_sin_td.a2009` | 1,050 | RMSE (°C) del año 2009, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple.a2009` | 1,027 | RMSE (°C) del año 2009, LLR simple, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos.a2009` | 1,032 | RMSE (°C) del año 2009, LLR con rezagos, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple_sel.a2009` | 1,033 | RMSE (°C) del año 2009, LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos_sel.a2009` | 1,034 | RMSE (°C) del año 2009, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_td.a2009` | 1,185 | RMSE (°C) del año 2009, TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm.a2009` | 1,026 | RMSE (°C) del año 2009, TimesFM, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_med.a2009` | 1,195 | RMSE (°C) del año 2009, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.clim.a2010` | 1,426 | RMSE (°C) del año 2010, climatología, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned.a2010` | 1,127 | RMSE (°C) del año 2010, tuned, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned_sin_td.a2010` | 1,103 | RMSE (°C) del año 2010, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple.a2010` | 1,095 | RMSE (°C) del año 2010, LLR simple, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos.a2010` | 1,089 | RMSE (°C) del año 2010, LLR con rezagos, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple_sel.a2010` | 1,073 | RMSE (°C) del año 2010, LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos_sel.a2010` | 1,067 | RMSE (°C) del año 2010, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_td.a2010` | 1,081 | RMSE (°C) del año 2010, TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm.a2010` | 1,021 | RMSE (°C) del año 2010, TimesFM, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_med.a2010` | 1,075 | RMSE (°C) del año 2010, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.clim.a2011` | 1,409 | RMSE (°C) del año 2011, climatología, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned.a2011` | 1,117 | RMSE (°C) del año 2011, tuned, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned_sin_td.a2011` | 1,091 | RMSE (°C) del año 2011, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple.a2011` | 1,096 | RMSE (°C) del año 2011, LLR simple, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos.a2011` | 1,076 | RMSE (°C) del año 2011, LLR con rezagos, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple_sel.a2011` | 1,080 | RMSE (°C) del año 2011, LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos_sel.a2011` | 1,061 | RMSE (°C) del año 2011, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_td.a2011` | 1,062 | RMSE (°C) del año 2011, TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm.a2011` | 1,034 | RMSE (°C) del año 2011, TimesFM, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_med.a2011` | 1,050 | RMSE (°C) del año 2011, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.clim.a2012` | 1,363 | RMSE (°C) del año 2012, climatología, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned.a2012` | 1,202 | RMSE (°C) del año 2012, tuned, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.tuned_sin_td.a2012` | 1,184 | RMSE (°C) del año 2012, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple.a2012` | 1,171 | RMSE (°C) del año 2012, LLR simple, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos.a2012` | 1,156 | RMSE (°C) del año 2012, LLR con rezagos, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_simple_sel.a2012` | 1,143 | RMSE (°C) del año 2012, LLR simple seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.llr_rezagos_sel.a2012` | 1,133 | RMSE (°C) del año 2012, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_td.a2012` | 1,092 | RMSE (°C) del año 2012, TimesFM en Td cruda, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm.a2012` | 1,102 | RMSE (°C) del año 2012, TimesFM, `ll4b`, dominio completo |
| `rmse_anual.ll4b.panel.timesfm_med.a2012` | 1,108 | RMSE (°C) del año 2012, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `rmse_anual.ll4b.peru.clim.a2009` | 1,013 | RMSE (°C) del año 2009, climatología, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned.a2009` | 0,796 | RMSE (°C) del año 2009, tuned, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned_sin_td.a2009` | 0,813 | RMSE (°C) del año 2009, tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple.a2009` | 0,796 | RMSE (°C) del año 2009, LLR simple, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos.a2009` | 0,801 | RMSE (°C) del año 2009, LLR con rezagos, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple_sel.a2009` | 0,790 | RMSE (°C) del año 2009, LLR simple seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos_sel.a2009` | 0,792 | RMSE (°C) del año 2009, LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_td.a2009` | 0,867 | RMSE (°C) del año 2009, TimesFM en Td cruda, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm.a2009` | 0,774 | RMSE (°C) del año 2009, TimesFM, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_med.a2009` | 0,874 | RMSE (°C) del año 2009, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.clim.a2010` | 1,137 | RMSE (°C) del año 2010, climatología, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned.a2010` | 0,852 | RMSE (°C) del año 2010, tuned, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned_sin_td.a2010` | 0,847 | RMSE (°C) del año 2010, tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple.a2010` | 0,843 | RMSE (°C) del año 2010, LLR simple, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos.a2010` | 0,835 | RMSE (°C) del año 2010, LLR con rezagos, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple_sel.a2010` | 0,821 | RMSE (°C) del año 2010, LLR simple seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos_sel.a2010` | 0,811 | RMSE (°C) del año 2010, LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_td.a2010` | 0,819 | RMSE (°C) del año 2010, TimesFM en Td cruda, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm.a2010` | 0,776 | RMSE (°C) del año 2010, TimesFM, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_med.a2010` | 0,822 | RMSE (°C) del año 2010, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.clim.a2011` | 1,089 | RMSE (°C) del año 2011, climatología, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned.a2011` | 0,841 | RMSE (°C) del año 2011, tuned, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned_sin_td.a2011` | 0,830 | RMSE (°C) del año 2011, tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple.a2011` | 0,835 | RMSE (°C) del año 2011, LLR simple, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos.a2011` | 0,821 | RMSE (°C) del año 2011, LLR con rezagos, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple_sel.a2011` | 0,826 | RMSE (°C) del año 2011, LLR simple seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos_sel.a2011` | 0,815 | RMSE (°C) del año 2011, LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_td.a2011` | 0,813 | RMSE (°C) del año 2011, TimesFM en Td cruda, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm.a2011` | 0,789 | RMSE (°C) del año 2011, TimesFM, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_med.a2011` | 0,818 | RMSE (°C) del año 2011, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.clim.a2012` | 1,106 | RMSE (°C) del año 2012, climatología, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned.a2012` | 0,947 | RMSE (°C) del año 2012, tuned, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.tuned_sin_td.a2012` | 0,929 | RMSE (°C) del año 2012, tuned sin rezagos de Td, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple.a2012` | 0,916 | RMSE (°C) del año 2012, LLR simple, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos.a2012` | 0,912 | RMSE (°C) del año 2012, LLR con rezagos, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_simple_sel.a2012` | 0,895 | RMSE (°C) del año 2012, LLR simple seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.llr_rezagos_sel.a2012` | 0,897 | RMSE (°C) del año 2012, LLR con rezagos seleccionado, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_td.a2012` | 0,859 | RMSE (°C) del año 2012, TimesFM en Td cruda, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm.a2012` | 0,874 | RMSE (°C) del año 2012, TimesFM, `ll4b`, Perú |
| `rmse_anual.ll4b.peru.timesfm_med.a2012` | 0,879 | RMSE (°C) del año 2012, TimesFM con contexto desde 2002, `ll4b`, Perú |

## sesgo_anual

| clave | valor | significado |
|---|---|---|
| `sesgo_anual.ll4.panel.clim.a2013` | +0,022 | Sesgo (°C) del año 2013, climatología, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned.a2013` | +0,207 | Sesgo (°C) del año 2013, tuned, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned_sin_td.a2013` | +0,218 | Sesgo (°C) del año 2013, tuned sin rezagos de Td, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple.a2013` | +0,228 | Sesgo (°C) del año 2013, LLR simple, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos.a2013` | +0,231 | Sesgo (°C) del año 2013, LLR con rezagos, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple_sel.a2013` | +0,241 | Sesgo (°C) del año 2013, LLR simple seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos_sel.a2013` | +0,245 | Sesgo (°C) del año 2013, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm.a2013` | +0,350 | Sesgo (°C) del año 2013, TimesFM, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm_med.a2013` | +0,447 | Sesgo (°C) del año 2013, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.clim.a2014` | −0,211 | Sesgo (°C) del año 2014, climatología, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned.a2014` | +0,053 | Sesgo (°C) del año 2014, tuned, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned_sin_td.a2014` | +0,085 | Sesgo (°C) del año 2014, tuned sin rezagos de Td, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple.a2014` | +0,064 | Sesgo (°C) del año 2014, LLR simple, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos.a2014` | +0,087 | Sesgo (°C) del año 2014, LLR con rezagos, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple_sel.a2014` | +0,075 | Sesgo (°C) del año 2014, LLR simple seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos_sel.a2014` | +0,101 | Sesgo (°C) del año 2014, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm.a2014` | +0,159 | Sesgo (°C) del año 2014, TimesFM, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm_med.a2014` | +0,282 | Sesgo (°C) del año 2014, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.clim.a2015` | −0,740 | Sesgo (°C) del año 2015, climatología, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned.a2015` | −0,315 | Sesgo (°C) del año 2015, tuned, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned_sin_td.a2015` | −0,219 | Sesgo (°C) del año 2015, tuned sin rezagos de Td, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple.a2015` | −0,264 | Sesgo (°C) del año 2015, LLR simple, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos.a2015` | −0,197 | Sesgo (°C) del año 2015, LLR con rezagos, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple_sel.a2015` | −0,262 | Sesgo (°C) del año 2015, LLR simple seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos_sel.a2015` | −0,197 | Sesgo (°C) del año 2015, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm.a2015` | −0,128 | Sesgo (°C) del año 2015, TimesFM, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm_med.a2015` | −0,036 | Sesgo (°C) del año 2015, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.clim.a2016` | −0,522 | Sesgo (°C) del año 2016, climatología, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned.a2016` | −0,075 | Sesgo (°C) del año 2016, tuned, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.tuned_sin_td.a2016` | −0,027 | Sesgo (°C) del año 2016, tuned sin rezagos de Td, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple.a2016` | −0,067 | Sesgo (°C) del año 2016, LLR simple, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos.a2016` | −0,019 | Sesgo (°C) del año 2016, LLR con rezagos, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_simple_sel.a2016` | −0,063 | Sesgo (°C) del año 2016, LLR simple seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.llr_rezagos_sel.a2016` | −0,006 | Sesgo (°C) del año 2016, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm.a2016` | +0,038 | Sesgo (°C) del año 2016, TimesFM, `ll4`, dominio completo |
| `sesgo_anual.ll4.panel.timesfm_med.a2016` | +0,113 | Sesgo (°C) del año 2016, TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `sesgo_anual.ll4.peru.clim.a2013` | +0,056 | Sesgo (°C) del año 2013, climatología, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned.a2013` | +0,174 | Sesgo (°C) del año 2013, tuned, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned_sin_td.a2013` | +0,188 | Sesgo (°C) del año 2013, tuned sin rezagos de Td, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple.a2013` | +0,182 | Sesgo (°C) del año 2013, LLR simple, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos.a2013` | +0,199 | Sesgo (°C) del año 2013, LLR con rezagos, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple_sel.a2013` | +0,165 | Sesgo (°C) del año 2013, LLR simple seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos_sel.a2013` | +0,177 | Sesgo (°C) del año 2013, LLR con rezagos seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm.a2013` | +0,185 | Sesgo (°C) del año 2013, TimesFM, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm_med.a2013` | +0,262 | Sesgo (°C) del año 2013, TimesFM con contexto desde 2002, `ll4`, Perú |
| `sesgo_anual.ll4.peru.clim.a2014` | −0,145 | Sesgo (°C) del año 2014, climatología, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned.a2014` | +0,089 | Sesgo (°C) del año 2014, tuned, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned_sin_td.a2014` | +0,116 | Sesgo (°C) del año 2014, tuned sin rezagos de Td, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple.a2014` | +0,084 | Sesgo (°C) del año 2014, LLR simple, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos.a2014` | +0,120 | Sesgo (°C) del año 2014, LLR con rezagos, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple_sel.a2014` | +0,064 | Sesgo (°C) del año 2014, LLR simple seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos_sel.a2014` | +0,098 | Sesgo (°C) del año 2014, LLR con rezagos seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm.a2014` | +0,122 | Sesgo (°C) del año 2014, TimesFM, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm_med.a2014` | +0,184 | Sesgo (°C) del año 2014, TimesFM con contexto desde 2002, `ll4`, Perú |
| `sesgo_anual.ll4.peru.clim.a2015` | −0,655 | Sesgo (°C) del año 2015, climatología, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned.a2015` | −0,205 | Sesgo (°C) del año 2015, tuned, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned_sin_td.a2015` | −0,129 | Sesgo (°C) del año 2015, tuned sin rezagos de Td, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple.a2015` | −0,189 | Sesgo (°C) del año 2015, LLR simple, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos.a2015` | −0,110 | Sesgo (°C) del año 2015, LLR con rezagos, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple_sel.a2015` | −0,217 | Sesgo (°C) del año 2015, LLR simple seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos_sel.a2015` | −0,141 | Sesgo (°C) del año 2015, LLR con rezagos seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm.a2015` | −0,102 | Sesgo (°C) del año 2015, TimesFM, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm_med.a2015` | −0,070 | Sesgo (°C) del año 2015, TimesFM con contexto desde 2002, `ll4`, Perú |
| `sesgo_anual.ll4.peru.clim.a2016` | −0,458 | Sesgo (°C) del año 2016, climatología, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned.a2016` | −0,019 | Sesgo (°C) del año 2016, tuned, `ll4`, Perú |
| `sesgo_anual.ll4.peru.tuned_sin_td.a2016` | +0,015 | Sesgo (°C) del año 2016, tuned sin rezagos de Td, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple.a2016` | −0,040 | Sesgo (°C) del año 2016, LLR simple, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos.a2016` | +0,028 | Sesgo (°C) del año 2016, LLR con rezagos, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_simple_sel.a2016` | −0,069 | Sesgo (°C) del año 2016, LLR simple seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.llr_rezagos_sel.a2016` | +0,001 | Sesgo (°C) del año 2016, LLR con rezagos seleccionado, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm.a2016` | −0,005 | Sesgo (°C) del año 2016, TimesFM, `ll4`, Perú |
| `sesgo_anual.ll4.peru.timesfm_med.a2016` | +0,018 | Sesgo (°C) del año 2016, TimesFM con contexto desde 2002, `ll4`, Perú |
| `sesgo_anual.ll4b.panel.clim.a2009` | −0,080 | Sesgo (°C) del año 2009, climatología, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned.a2009` | +0,150 | Sesgo (°C) del año 2009, tuned, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned_sin_td.a2009` | +0,211 | Sesgo (°C) del año 2009, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple.a2009` | +0,176 | Sesgo (°C) del año 2009, LLR simple, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos.a2009` | +0,217 | Sesgo (°C) del año 2009, LLR con rezagos, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple_sel.a2009` | +0,174 | Sesgo (°C) del año 2009, LLR simple seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos_sel.a2009` | +0,214 | Sesgo (°C) del año 2009, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_td.a2009` | +0,359 | Sesgo (°C) del año 2009, TimesFM en Td cruda, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm.a2009` | +0,215 | Sesgo (°C) del año 2009, TimesFM, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_med.a2009` | +0,394 | Sesgo (°C) del año 2009, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.clim.a2010` | −0,412 | Sesgo (°C) del año 2010, climatología, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned.a2010` | −0,134 | Sesgo (°C) del año 2010, tuned, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned_sin_td.a2010` | −0,106 | Sesgo (°C) del año 2010, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple.a2010` | −0,127 | Sesgo (°C) del año 2010, LLR simple, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos.a2010` | −0,103 | Sesgo (°C) del año 2010, LLR con rezagos, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple_sel.a2010` | −0,123 | Sesgo (°C) del año 2010, LLR simple seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos_sel.a2010` | −0,095 | Sesgo (°C) del año 2010, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_td.a2010` | +0,098 | Sesgo (°C) del año 2010, TimesFM en Td cruda, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm.a2010` | −0,087 | Sesgo (°C) del año 2010, TimesFM, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_med.a2010` | +0,153 | Sesgo (°C) del año 2010, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.clim.a2011` | −0,339 | Sesgo (°C) del año 2011, climatología, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned.a2011` | −0,267 | Sesgo (°C) del año 2011, tuned, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned_sin_td.a2011` | −0,240 | Sesgo (°C) del año 2011, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple.a2011` | −0,237 | Sesgo (°C) del año 2011, LLR simple, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos.a2011` | −0,226 | Sesgo (°C) del año 2011, LLR con rezagos, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple_sel.a2011` | −0,231 | Sesgo (°C) del año 2011, LLR simple seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos_sel.a2011` | −0,228 | Sesgo (°C) del año 2011, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_td.a2011` | −0,085 | Sesgo (°C) del año 2011, TimesFM en Td cruda, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm.a2011` | −0,205 | Sesgo (°C) del año 2011, TimesFM, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_med.a2011` | −0,006 | Sesgo (°C) del año 2011, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.clim.a2012` | −0,369 | Sesgo (°C) del año 2012, climatología, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned.a2012` | −0,373 | Sesgo (°C) del año 2012, tuned, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.tuned_sin_td.a2012` | −0,360 | Sesgo (°C) del año 2012, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple.a2012` | −0,371 | Sesgo (°C) del año 2012, LLR simple, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos.a2012` | −0,354 | Sesgo (°C) del año 2012, LLR con rezagos, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_simple_sel.a2012` | −0,370 | Sesgo (°C) del año 2012, LLR simple seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.llr_rezagos_sel.a2012` | −0,360 | Sesgo (°C) del año 2012, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_td.a2012` | −0,232 | Sesgo (°C) del año 2012, TimesFM en Td cruda, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm.a2012` | −0,352 | Sesgo (°C) del año 2012, TimesFM, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.panel.timesfm_med.a2012` | −0,183 | Sesgo (°C) del año 2012, TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `sesgo_anual.ll4b.peru.clim.a2009` | −0,173 | Sesgo (°C) del año 2009, climatología, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned.a2009` | +0,089 | Sesgo (°C) del año 2009, tuned, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned_sin_td.a2009` | +0,150 | Sesgo (°C) del año 2009, tuned sin rezagos de Td, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple.a2009` | +0,108 | Sesgo (°C) del año 2009, LLR simple, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos.a2009` | +0,157 | Sesgo (°C) del año 2009, LLR con rezagos, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple_sel.a2009` | +0,077 | Sesgo (°C) del año 2009, LLR simple seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos_sel.a2009` | +0,123 | Sesgo (°C) del año 2009, LLR con rezagos seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_td.a2009` | +0,174 | Sesgo (°C) del año 2009, TimesFM en Td cruda, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm.a2009` | +0,095 | Sesgo (°C) del año 2009, TimesFM, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_med.a2009` | +0,165 | Sesgo (°C) del año 2009, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.clim.a2010` | −0,204 | Sesgo (°C) del año 2010, climatología, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned.a2010` | +0,035 | Sesgo (°C) del año 2010, tuned, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned_sin_td.a2010` | +0,042 | Sesgo (°C) del año 2010, tuned sin rezagos de Td, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple.a2010` | +0,010 | Sesgo (°C) del año 2010, LLR simple, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos.a2010` | +0,048 | Sesgo (°C) del año 2010, LLR con rezagos, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple_sel.a2010` | −0,019 | Sesgo (°C) del año 2010, LLR simple seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos_sel.a2010` | +0,016 | Sesgo (°C) del año 2010, LLR con rezagos seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_td.a2010` | +0,082 | Sesgo (°C) del año 2010, TimesFM en Td cruda, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm.a2010` | −0,030 | Sesgo (°C) del año 2010, TimesFM, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_med.a2010` | +0,081 | Sesgo (°C) del año 2010, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.clim.a2011` | −0,158 | Sesgo (°C) del año 2011, climatología, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned.a2011` | −0,128 | Sesgo (°C) del año 2011, tuned, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned_sin_td.a2011` | −0,108 | Sesgo (°C) del año 2011, tuned sin rezagos de Td, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple.a2011` | −0,111 | Sesgo (°C) del año 2011, LLR simple, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos.a2011` | −0,101 | Sesgo (°C) del año 2011, LLR con rezagos, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple_sel.a2011` | −0,135 | Sesgo (°C) del año 2011, LLR simple seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos_sel.a2011` | −0,136 | Sesgo (°C) del año 2011, LLR con rezagos seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_td.a2011` | −0,064 | Sesgo (°C) del año 2011, TimesFM en Td cruda, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm.a2011` | −0,137 | Sesgo (°C) del año 2011, TimesFM, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_med.a2011` | −0,059 | Sesgo (°C) del año 2011, TimesFM con contexto desde 2002, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.clim.a2012` | −0,277 | Sesgo (°C) del año 2012, climatología, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned.a2012` | −0,236 | Sesgo (°C) del año 2012, tuned, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.tuned_sin_td.a2012` | −0,220 | Sesgo (°C) del año 2012, tuned sin rezagos de Td, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple.a2012` | −0,230 | Sesgo (°C) del año 2012, LLR simple, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos.a2012` | −0,215 | Sesgo (°C) del año 2012, LLR con rezagos, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_simple_sel.a2012` | −0,256 | Sesgo (°C) del año 2012, LLR simple seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.llr_rezagos_sel.a2012` | −0,250 | Sesgo (°C) del año 2012, LLR con rezagos seleccionado, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_td.a2012` | −0,202 | Sesgo (°C) del año 2012, TimesFM en Td cruda, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm.a2012` | −0,267 | Sesgo (°C) del año 2012, TimesFM, `ll4b`, Perú |
| `sesgo_anual.ll4b.peru.timesfm_med.a2012` | −0,204 | Sesgo (°C) del año 2012, TimesFM con contexto desde 2002, `ll4b`, Perú |

## sesgo_conteo

| clave | valor | significado |
|---|---|---|
| `sesgo_conteo.ll4b.panel.timesfm_mayor_abs` | no | ¿El sesgo de TimesFM es mayor en magnitud que el de `tuned`? (ll4b, dominio completo) |
| `sesgo_conteo.ll4b.peru.timesfm_mayor_abs` | sí | ¿El sesgo de TimesFM es mayor en magnitud que el de `tuned`? (ll4b, Perú) |
| `sesgo_conteo.ll4.panel.timesfm_mayor_abs` | sí | ¿El sesgo de TimesFM es mayor en magnitud que el de `tuned`? (ll4, dominio completo) |
| `sesgo_conteo.ll4.peru.timesfm_mayor_abs` | sí | ¿El sesgo de TimesFM es mayor en magnitud que el de `tuned`? (ll4, Perú) |
| `sesgo_conteo.n_mayor` | 3 | Casos (de 4) en que /sesgo TimesFM/ > /sesgo tuned/ |
| `sesgo_conteo.n_casos` | 4 | Casos comparados (bloque × ámbito) |
| `sesgo_conteo.casos_mayor` | 2009–2012 en Perú, 2013–2016 en el dominio completo y 2013–2016 en Perú | Lista de casos con mayor sesgo absoluto de TimesFM |
| `sesgo_conteo.casos_menor` | 2009–2012 en el dominio completo | Casos con /sesgo TimesFM/ <= /sesgo tuned/ |

## rmse_min

| clave | valor | significado |
|---|---|---|
| `rmse_min.n_casos_timesfm_menor` | 4 | Casos (de 4) en que TimesFM `tmin_anom_full` tiene el menor RMSE entre todos los métodos |

## brecha_anual

| clave | valor | significado |
|---|---|---|
| `brecha_anual.ll4b.panel.timesfm_vs_tuned.a2009` | −0,009 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2009, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned.a2010` | −0,107 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2010, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned.a2011` | −0,083 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2011, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned.a2012` | −0,100 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2012, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_llr_rezagos_sel.a2009` | −0,008 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2009, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_llr_rezagos_sel.a2010` | −0,046 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2010, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_llr_rezagos_sel.a2011` | −0,028 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2011, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_llr_rezagos_sel.a2012` | −0,031 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2012, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned_sin_td.a2009` | −0,024 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2009, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned_sin_td.a2010` | −0,083 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2010, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned_sin_td.a2011` | −0,057 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2011, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_vs_tuned_sin_td.a2012` | −0,082 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2012, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_td_vs_tuned.a2009` | +0,150 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2009, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_td_vs_tuned.a2010` | −0,047 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2010, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_td_vs_tuned.a2011` | −0,055 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2011, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.panel.timesfm_td_vs_tuned.a2012` | −0,110 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2012, `ll4b`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned.a2009` | −0,022 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2009, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned.a2010` | −0,076 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2010, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned.a2011` | −0,052 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2011, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned.a2012` | −0,073 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2012, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_llr_rezagos_sel.a2009` | −0,018 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2009, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_llr_rezagos_sel.a2010` | −0,035 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2010, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_llr_rezagos_sel.a2011` | −0,026 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2011, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_llr_rezagos_sel.a2012` | −0,023 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2012, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned_sin_td.a2009` | −0,039 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2009, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned_sin_td.a2010` | −0,071 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2010, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned_sin_td.a2011` | −0,041 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2011, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_vs_tuned_sin_td.a2012` | −0,055 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2012, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_td_vs_tuned.a2009` | +0,071 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2009, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_td_vs_tuned.a2010` | −0,033 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2010, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_td_vs_tuned.a2011` | −0,028 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2011, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4b.peru.timesfm_td_vs_tuned.a2012` | −0,088 | Brecha anual RMSE(TimesFM en Td cruda) − RMSE(tuned), 2012, `ll4b`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned.a2013` | +0,055 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2013, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned.a2014` | −0,059 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2014, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned.a2015` | −0,165 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2015, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned.a2016` | −0,126 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2016, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_llr_rezagos_sel.a2013` | +0,060 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2013, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_llr_rezagos_sel.a2014` | −0,022 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2014, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_llr_rezagos_sel.a2015` | −0,050 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2015, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_llr_rezagos_sel.a2016` | −0,003 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2016, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned_sin_td.a2013` | +0,050 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2013, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned_sin_td.a2014` | −0,024 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2014, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned_sin_td.a2015` | −0,087 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2015, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.panel.timesfm_vs_tuned_sin_td.a2016` | −0,026 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2016, `ll4`, dominio completo (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned.a2013` | −0,025 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2013, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned.a2014` | −0,072 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2014, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned.a2015` | −0,137 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2015, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned.a2016` | −0,081 | Brecha anual RMSE(TimesFM) − RMSE(tuned), 2016, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_llr_rezagos_sel.a2013` | −0,011 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2013, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_llr_rezagos_sel.a2014` | −0,035 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2014, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_llr_rezagos_sel.a2015` | −0,046 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2015, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_llr_rezagos_sel.a2016` | −0,012 | Brecha anual RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), 2016, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned_sin_td.a2013` | −0,020 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2013, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned_sin_td.a2014` | −0,045 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2014, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned_sin_td.a2015` | −0,073 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2015, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ll4.peru.timesfm_vs_tuned_sin_td.a2016` | −0,033 | Brecha anual RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), 2016, `ll4`, Perú (descriptiva, sin IC) |
| `brecha_anual.ic` | n. d. | IC de las brechas anuales (las brechas anuales son descriptivas, sin IC) |

## anual_resumen

| clave | valor | significado |
|---|---|---|
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.anios_mayor_ventaja` | 2010, 2011 y 2012 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.anio_mejor` | 2010 | Año con la brecha más negativa |
| `anual_resumen.ll4b.panel.timesfm_vs_tuned.brecha_mejor` | −0,107 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.anios_mayor_ventaja` | 2010 y 2012 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.anio_mejor` | 2010 | Año con la brecha más negativa |
| `anual_resumen.ll4b.panel.timesfm_vs_llr_rezagos_sel.brecha_mejor` | −0,046 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.anios_mayor_ventaja` | 2010 y 2012 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.anio_mejor` | 2010 | Año con la brecha más negativa |
| `anual_resumen.ll4b.peru.timesfm_vs_tuned.brecha_mejor` | −0,076 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.anios_mayor_ventaja` | 2010 y 2011 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.anio_mejor` | 2010 | Año con la brecha más negativa |
| `anual_resumen.ll4b.peru.timesfm_vs_llr_rezagos_sel.brecha_mejor` | −0,035 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.n_negativas` | 3 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.todas_negativas` | no | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.anios_positivos` | 2013 | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.anios_mayor_ventaja` | 2015 y 2016 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.anio_mejor` | 2015 | Año con la brecha más negativa |
| `anual_resumen.ll4.panel.timesfm_vs_tuned.brecha_mejor` | −0,165 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.n_negativas` | 3 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.todas_negativas` | no | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.anios_positivos` | 2013 | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.anios_mayor_ventaja` | 2014, 2015 y 2016 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.anio_mejor` | 2015 | Año con la brecha más negativa |
| `anual_resumen.ll4.panel.timesfm_vs_llr_rezagos_sel.brecha_mejor` | −0,050 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.anios_mayor_ventaja` | 2015 y 2016 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.anio_mejor` | 2015 | Año con la brecha más negativa |
| `anual_resumen.ll4.peru.timesfm_vs_tuned.brecha_mejor` | −0,137 | Brecha del año con la brecha más negativa |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.n_negativas` | 4 | Años con brecha negativa (favorece a TimesFM) |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.n_anios` | 4 | Años comparados |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.todas_negativas` | sí | ¿Todas las brechas anuales son negativas? |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.anios_positivos` | ninguno | Años con brecha positiva (TimesFM peor) |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.anios_mayor_ventaja` | 2014 y 2015 | Años en que la ventaja de TimesFM supera la brecha agregada del bloque |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.anio_mejor` | 2015 | Año con la brecha más negativa |
| `anual_resumen.ll4.peru.timesfm_vs_llr_rezagos_sel.brecha_mejor` | −0,046 | Brecha del año con la brecha más negativa |

## inversion

| clave | valor | significado |
|---|---|---|
| `inversion.n_casos_vs_tuned` | 1 | Casos (bloque × ámbito × año) en que TimesFM tiene mayor RMSE que `tuned` |
| `inversion.anio` | 2013 | Año en que se invierte el orden frente a `tuned` (dominio completo) |
| `inversion.gap_tuned` | +0,055 | Brecha TimesFM − `tuned` en 2013, dominio completo |
| `inversion.gap_llr_rezagos_sel` | +0,060 | Brecha TimesFM − `llr_rezagos_sel` en 2013, dominio completo |
| `inversion.sesgo_timesfm` | +0,350 | Sesgo de TimesFM en 2013, dominio completo |
| `inversion.sesgo_tuned` | +0,207 | Sesgo de `tuned` en 2013, dominio completo |
| `inversion.solo_panel` | sí | ¿En Perú TimesFM sigue por debajo de `tuned` en 2013? |

## brecha

| clave | valor | significado |
|---|---|---|
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.v` | −0,007 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.abs` | 0,007 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.esp_lo` | −0,017 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.esp_hi` | +0,001 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.esp_ic` | [−0,017; +0,001] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.esp_bloques_a_gana` | 48 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ma_lo` | −0,038 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ma_hi` | +0,023 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ma_ic` | [−0,038; +0,023] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ma_bloques_a_gana` | 29 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.v` | −0,021 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.abs` | 0,021 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.esp_lo` | −0,031 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.esp_hi` | −0,012 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.esp_ic` | [−0,031; −0,012] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.esp_bloques_a_gana` | 57 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ma_lo` | −0,053 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ma_hi` | +0,010 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ma_ic` | [−0,053; +0,010] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ma_bloques_a_gana` | 29 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.v` | −0,074 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.abs` | 0,074 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.esp_lo` | −0,080 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.esp_hi` | −0,069 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.esp_ic` | [−0,080; −0,069] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ma_lo` | −0,140 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ma_hi` | −0,015 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ma_ic` | [−0,140; −0,015] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ma_bloques_a_gana` | 35 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.v` | +0,053 | Brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.abs` | 0,053 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.esp_lo` | +0,044 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.esp_hi` | +0,062 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.esp_ic` | [+0,044; +0,062] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.esp_bloques_a_gana` | 13 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ma_lo` | +0,017 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ma_hi` | +0,097 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ma_ic` | [+0,017; +0,097] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ma_bloques_a_gana` | 12 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.v` | +0,067 | Brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.abs` | 0,067 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.esp_lo` | +0,058 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.esp_hi` | +0,075 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.esp_ic` | [+0,058; +0,075] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.esp_bloques_a_gana` | 1 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ma_lo` | +0,029 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ma_hi` | +0,114 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ma_ic` | [+0,029; +0,114] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ma_bloques_a_gana` | 9 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.v` | +0,054 | Brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.abs` | 0,054 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.esp_lo` | +0,046 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.esp_hi` | +0,061 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.esp_ic` | [+0,046; +0,061] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.esp_bloques_a_gana` | 1 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ma_lo` | +0,019 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ma_hi` | +0,096 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ma_ic` | [+0,019; +0,096] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ma_bloques_a_gana` | 11 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_vs_tuned_sin_td.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.v` | −0,001 | Brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.abs` | 0,001 | Magnitud de la brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.esp_lo` | −0,003 | Límite inferior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.esp_hi` | +0,002 | Límite superior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.esp_ic` | [−0,003; +0,002] | IC 95 % espacial_2g como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.esp_bloques_a_gana` | 40 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ma_lo` | −0,012 | Límite inferior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ma_hi` | +0,011 | Límite superior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ma_ic` | [−0,012; +0,011] | IC 95 % mes_anio como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ma_bloques_a_gana` | 21 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.tuned_sin_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.v` | −0,021 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.abs` | 0,021 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.esp_lo` | −0,029 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.esp_hi` | −0,013 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.esp_ic` | [−0,029; −0,013] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.esp_bloques_a_gana` | 58 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ma_lo` | −0,056 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ma_hi` | +0,015 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ma_ic` | [−0,056; +0,015] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ma_bloques_a_gana` | 29 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_tuned_sin_td.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.v` | +0,047 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.abs` | 0,047 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.esp_lo` | +0,041 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.esp_hi` | +0,053 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.esp_ic` | [+0,041; +0,053] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.esp_bloques_a_gana` | 2 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ma_lo` | +0,027 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ma_hi` | +0,068 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ma_ic` | [+0,027; +0,068] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ma_bloques_a_gana` | 13 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_timesfm.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.v` | +0,040 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.abs` | 0,040 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.esp_lo` | +0,025 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.esp_hi` | +0,053 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.esp_ic` | [+0,025; +0,053] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.esp_bloques_a_gana` | 28 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ma_lo` | −0,005 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ma_hi` | +0,083 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ma_ic` | [−0,005; +0,083] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ma_bloques_a_gana` | 20 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_med_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.v` | −0,003 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.abs` | 0,003 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.esp_lo` | −0,011 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.esp_hi` | +0,004 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.esp_ic` | [−0,011; +0,004] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.esp_bloques_a_gana` | 49 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ma_lo` | −0,029 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ma_hi` | +0,021 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ma_ic` | [−0,029; +0,021] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ma_bloques_a_gana` | 28 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_rezagos_sel.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.v` | −0,018 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.abs` | 0,018 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.esp_lo` | −0,027 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.esp_hi` | −0,010 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.esp_ic` | [−0,027; −0,010] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.esp_bloques_a_gana` | 58 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ma_lo` | −0,045 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ma_hi` | +0,007 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ma_ic` | [−0,045; +0,007] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ma_bloques_a_gana` | 30 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.timesfm_vs_llr_simple_sel.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.v` | −0,004 | Brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.abs` | 0,004 | Magnitud de la brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.esp_lo` | −0,008 | Límite inferior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.esp_hi` | −0,002 | Límite superior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.esp_ic` | [−0,008; −0,002] | IC 95 % espacial_2g como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.esp_bloques_a_gana` | 49 | Bloques (de 74) en que A gana, espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ma_lo` | −0,013 | Límite inferior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ma_hi` | +0,004 | Límite superior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ma_ic` | [−0,013; +0,004] | IC 95 % mes_anio como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ma_bloques_a_gana` | 26 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_rezagos_sel_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.v` | −0,003 | Brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.abs` | 0,003 | Magnitud de la brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.esp_lo` | −0,006 | Límite inferior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.esp_hi` | −0,001 | Límite superior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.esp_ic` | [−0,006; −0,001] | IC 95 % espacial_2g como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.esp_bloques_a_gana` | 40 | Bloques (de 74) en que A gana, espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ma_lo` | −0,010 | Límite inferior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ma_hi` | +0,005 | Límite superior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ma_ic` | [−0,010; +0,005] | IC 95 % mes_anio como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ma_bloques_a_gana` | 27 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.panel.llr_simple_sel_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, dominio completo |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.v` | −0,032 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.abs` | 0,032 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.esp_lo` | −0,044 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.esp_hi` | −0,021 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.esp_ic` | [−0,044; −0,021] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.esp_bloques_a_gana` | 39 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ma_lo` | −0,047 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ma_hi` | −0,018 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ma_ic` | [−0,047; −0,018] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ma_bloques_a_gana` | 37 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.v` | −0,047 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.abs` | 0,047 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.esp_lo` | −0,058 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.esp_hi` | −0,036 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.esp_ic` | [−0,058; −0,036] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.esp_bloques_a_gana` | 43 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ma_lo` | −0,063 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ma_hi` | −0,031 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ma_ic` | [−0,063; −0,031] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ma_bloques_a_gana` | 40 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.v` | −0,079 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.abs` | 0,079 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.esp_lo` | −0,087 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.esp_hi` | −0,071 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.esp_ic` | [−0,087; −0,071] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ma_lo` | −0,109 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ma_hi` | −0,052 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ma_ic` | [−0,109; −0,052] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.v` | +0,032 | Brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.abs` | 0,032 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.esp_lo` | +0,021 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.esp_hi` | +0,043 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.esp_ic` | [+0,021; +0,043] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.esp_bloques_a_gana` | 7 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ma_lo` | +0,016 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ma_hi` | +0,050 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ma_ic` | [+0,016; +0,050] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ma_bloques_a_gana` | 12 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.v` | +0,047 | Brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.abs` | 0,047 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.esp_lo` | +0,036 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.esp_hi` | +0,058 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.esp_ic` | [+0,036; +0,058] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.esp_bloques_a_gana` | 0 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ma_lo` | +0,026 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ma_hi` | +0,071 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ma_ic` | [+0,026; +0,071] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ma_bloques_a_gana` | 9 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.v` | +0,036 | Brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.abs` | 0,036 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.esp_lo` | +0,027 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.esp_hi` | +0,046 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.esp_ic` | [+0,027; +0,046] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.esp_bloques_a_gana` | 1 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ma_lo` | +0,019 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ma_hi` | +0,057 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ma_ic` | [+0,019; +0,057] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ma_bloques_a_gana` | 12 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_vs_tuned_sin_td.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.v` | −0,004 | Brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.abs` | 0,004 | Magnitud de la brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.esp_lo` | −0,008 | Límite inferior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.esp_hi` | −0,001 | Límite superior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.esp_ic` | [−0,008; −0,001] | IC 95 % espacial_2g como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.esp_bloques_a_gana` | 31 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ma_lo` | −0,011 | Límite inferior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ma_hi` | +0,003 | Límite superior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ma_ic` | [−0,011; +0,003] | IC 95 % mes_anio como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ma_bloques_a_gana` | 28 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.tuned_sin_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.v` | −0,043 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.abs` | 0,043 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.esp_lo` | −0,054 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.esp_hi` | −0,033 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.esp_ic` | [−0,054; −0,033] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.esp_bloques_a_gana` | 43 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ma_lo` | −0,060 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ma_hi` | −0,027 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ma_ic` | [−0,060; −0,027] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_tuned_sin_td.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.v` | +0,037 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.abs` | 0,037 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.esp_lo` | +0,030 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.esp_hi` | +0,045 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.esp_ic` | [+0,030; +0,045] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.esp_bloques_a_gana` | 2 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ma_lo` | +0,025 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ma_hi` | +0,050 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ma_ic` | [+0,025; +0,050] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ma_bloques_a_gana` | 9 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_timesfm.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.v` | +0,005 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.abs` | 0,005 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.esp_lo` | −0,013 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.esp_hi` | +0,023 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.esp_ic` | [−0,013; +0,023] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.esp_bloques_a_gana` | 25 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ma_lo` | −0,016 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ma_hi` | +0,026 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ma_ic` | [−0,016; +0,026] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ma_bloques_a_gana` | 26 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_med_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.v` | −0,026 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.abs` | 0,026 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.esp_lo` | −0,033 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.esp_hi` | −0,018 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.esp_ic` | [−0,033; −0,018] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.esp_bloques_a_gana` | 41 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ma_lo` | −0,038 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ma_hi` | −0,014 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ma_ic` | [−0,038; −0,014] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_rezagos_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.v` | −0,041 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.abs` | 0,041 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.esp_lo` | −0,049 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.esp_hi` | −0,033 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.esp_ic` | [−0,049; −0,033] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.esp_bloques_a_gana` | 43 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ma_lo` | −0,054 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ma_hi` | −0,029 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ma_ic` | [−0,054; −0,029] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.timesfm_vs_llr_simple_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.v` | −0,007 | Brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.abs` | 0,007 | Magnitud de la brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.esp_lo` | −0,013 | Límite inferior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.esp_hi` | −0,001 | Límite superior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.esp_ic` | [−0,013; −0,001] | IC 95 % espacial_2g como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.esp_bloques_a_gana` | 25 | Bloques (de 45) en que A gana, espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ma_lo` | −0,011 | Límite inferior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ma_hi` | −0,002 | Límite superior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ma_ic` | [−0,011; −0,002] | IC 95 % mes_anio como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ma_bloques_a_gana` | 32 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_rezagos_sel_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.v` | −0,006 | Brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.abs` | 0,006 | Magnitud de la brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.esp_lo` | −0,011 | Límite inferior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.esp_hi` | −0,002 | Límite superior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.esp_ic` | [−0,011; −0,002] | IC 95 % espacial_2g como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.esp_bloques_a_gana` | 25 | Bloques (de 45) en que A gana, espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ma_lo` | −0,011 | Límite inferior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ma_hi` | −0,0002 | Límite superior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ma_ic` | [−0,011; −0,0002] | IC 95 % mes_anio como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ma_bloques_a_gana` | 33 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4.peru.llr_simple_sel_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4`, Perú |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.v` | −0,043 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.abs` | 0,043 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.esp_lo` | −0,047 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.esp_hi` | −0,039 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.esp_ic` | [−0,047; −0,039] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ma_lo` | −0,062 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ma_hi` | −0,026 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ma_ic` | [−0,062; −0,026] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ma_bloques_a_gana` | 36 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.v` | −0,052 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.abs` | 0,052 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.esp_lo` | −0,057 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.esp_hi` | −0,048 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.esp_ic` | [−0,057; −0,048] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ma_lo` | −0,073 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ma_hi` | −0,033 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ma_ic` | [−0,073; −0,033] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ma_bloques_a_gana` | 37 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.v` | −0,076 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.abs` | 0,076 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.esp_lo` | −0,084 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.esp_hi` | −0,068 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.esp_ic` | [−0,084; −0,068] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ma_lo` | −0,102 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ma_hi` | −0,050 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ma_ic` | [−0,102; −0,050] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ma_bloques_a_gana` | 37 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.v` | +0,024 | Brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.abs` | 0,024 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.esp_lo` | +0,020 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.esp_hi` | +0,027 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.esp_ic` | [+0,020; +0,027] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.esp_bloques_a_gana` | 11 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ma_lo` | +0,009 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ma_hi` | +0,039 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ma_ic` | [+0,009; +0,039] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ma_bloques_a_gana` | 19 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.v` | +0,033 | Brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.abs` | 0,033 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.esp_lo` | +0,028 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.esp_hi` | +0,037 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.esp_ic` | [+0,028; +0,037] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.esp_bloques_a_gana` | 2 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ma_lo` | +0,019 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ma_hi` | +0,046 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ma_ic` | [+0,019; +0,046] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ma_bloques_a_gana` | 10 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.v` | +0,007 | Brecha (°C) RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.abs` | 0,007 | Magnitud de la brecha (°C) RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.esp_lo` | −0,001 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.esp_hi` | +0,015 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.esp_ic` | [−0,001; +0,015] | IC 95 % espacial_2g como texto, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.esp_bloques_a_gana` | 38 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ma_lo` | −0,042 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ma_hi` | +0,059 | Límite superior IC 95 % mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ma_ic` | [−0,042; +0,059] | IC 95 % mes_anio como texto, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ma_bloques_a_gana` | 22 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.v` | +0,014 | Brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.abs` | 0,014 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.esp_lo` | +0,011 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.esp_hi` | +0,017 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.esp_ic` | [+0,011; +0,017] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.esp_bloques_a_gana` | 13 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ma_lo` | −0,0001 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ma_hi` | +0,027 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ma_ic` | [−0,0001; +0,027] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ma_bloques_a_gana` | 18 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_vs_tuned_sin_td.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.v` | +0,010 | Brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.abs` | 0,010 | Magnitud de la brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.esp_lo` | +0,007 | Límite inferior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.esp_hi` | +0,012 | Límite superior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.esp_ic` | [+0,007; +0,012] | IC 95 % espacial_2g como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.esp_bloques_a_gana` | 22 | Bloques (de 74) en que A gana, espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ma_lo` | −0,003 | Límite inferior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ma_hi` | +0,022 | Límite superior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ma_ic` | [−0,003; +0,022] | IC 95 % mes_anio como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ma_bloques_a_gana` | 14 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.tuned_sin_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.v` | −0,062 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.abs` | 0,062 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.esp_lo` | −0,068 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.esp_hi` | −0,056 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.esp_ic` | [−0,068; −0,056] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ma_lo` | −0,084 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ma_hi` | −0,043 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ma_ic` | [−0,084; −0,043] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ma_bloques_a_gana` | 41 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_tuned_sin_td.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.v` | +0,062 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.abs` | 0,062 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.esp_lo` | +0,053 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.esp_hi` | +0,071 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.esp_ic` | [+0,053; +0,071] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.esp_bloques_a_gana` | 3 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ma_lo` | +0,024 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ma_hi` | +0,100 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ma_ic` | [+0,024; +0,100] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ma_bloques_a_gana` | 16 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_timesfm.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.v` | +0,019 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.abs` | 0,019 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.esp_lo` | +0,011 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.esp_hi` | +0,026 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.esp_ic` | [+0,011; +0,026] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.esp_bloques_a_gana` | 24 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ma_lo` | −0,032 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ma_hi` | +0,067 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ma_ic` | [−0,032; +0,067] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ma_bloques_a_gana` | 19 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_med_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.v` | −0,028 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.abs` | 0,028 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.esp_lo` | −0,031 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.esp_hi` | −0,026 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.esp_ic` | [−0,031; −0,026] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ma_lo` | −0,044 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ma_hi` | −0,013 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ma_ic` | [−0,044; −0,013] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ma_bloques_a_gana` | 33 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_rezagos_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.v` | −0,037 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.abs` | 0,037 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.esp_lo` | −0,041 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.esp_hi` | −0,033 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.esp_ic` | [−0,041; −0,033] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.esp_bloques_a_gana` | 74 | Bloques (de 74) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ma_lo` | −0,052 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ma_hi` | −0,023 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ma_ic` | [−0,052; −0,023] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.timesfm_vs_llr_simple_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.v` | −0,015 | Brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.abs` | 0,015 | Magnitud de la brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.esp_lo` | −0,017 | Límite inferior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.esp_hi` | −0,012 | Límite superior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.esp_ic` | [−0,017; −0,012] | IC 95 % espacial_2g como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.esp_bloques_a_gana` | 73 | Bloques (de 74) en que A gana, espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ma_lo` | −0,026 | Límite inferior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ma_hi` | −0,004 | Límite superior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ma_ic` | [−0,026; −0,004] | IC 95 % mes_anio como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ma_bloques_a_gana` | 29 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.v` | −0,015 | Brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.abs` | 0,015 | Magnitud de la brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.esp_lo` | −0,017 | Límite inferior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.esp_hi` | −0,013 | Límite superior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.esp_ic` | [−0,017; −0,013] | IC 95 % espacial_2g como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.esp_bloques_a_gana` | 72 | Bloques (de 74) en que A gana, espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ma_lo` | −0,026 | Límite inferior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ma_hi` | −0,005 | Límite superior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ma_ic` | [−0,026; −0,005] | IC 95 % mes_anio como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ma_bloques_a_gana` | 31 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.panel.llr_simple_sel_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, dominio completo |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.v` | −0,039 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.abs` | 0,039 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.esp_lo` | −0,046 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.esp_hi` | −0,033 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.esp_ic` | [−0,046; −0,033] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ma_lo` | −0,050 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ma_hi` | −0,029 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ma_ic` | [−0,050; −0,029] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ma_bloques_a_gana` | 41 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.v` | −0,044 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.abs` | 0,044 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.esp_lo` | −0,050 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.esp_hi` | −0,039 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.esp_ic` | [−0,050; −0,039] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ma_lo` | −0,057 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ma_hi` | −0,033 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ma_ic` | [−0,057; −0,033] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ma_bloques_a_gana` | 43 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.v` | −0,056 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.abs` | 0,056 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.esp_lo` | −0,065 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.esp_hi` | −0,049 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.esp_ic` | [−0,065; −0,049] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ma_lo` | −0,073 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ma_hi` | −0,040 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ma_ic` | [−0,073; −0,040] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ma_bloques_a_gana` | 38 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.v` | +0,012 | Brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.abs` | 0,012 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.esp_lo` | +0,008 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.esp_hi` | +0,016 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.esp_ic` | [+0,008; +0,016] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.esp_bloques_a_gana` | 10 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ma_lo` | +0,002 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ma_hi` | +0,024 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ma_ic` | [+0,002; +0,024] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ma_bloques_a_gana` | 22 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.v` | +0,017 | Brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.abs` | 0,017 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.esp_lo` | +0,014 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.esp_hi` | +0,021 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.esp_ic` | [+0,014; +0,021] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.esp_bloques_a_gana` | 0 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ma_lo` | +0,007 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ma_hi` | +0,027 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ma_ic` | [+0,007; +0,027] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ma_bloques_a_gana` | 11 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.v` | −0,009 | Brecha (°C) RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.abs` | 0,009 | Magnitud de la brecha (°C) RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.esp_lo` | −0,020 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.esp_hi` | +0,002 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.esp_ic` | [−0,020; +0,002] | IC 95 % espacial_2g como texto, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.esp_bloques_a_gana` | 27 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ma_lo` | −0,037 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ma_hi` | +0,019 | Límite superior IC 95 % mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ma_ic` | [−0,037; +0,019] | IC 95 % mes_anio como texto, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ma_bloques_a_gana` | 25 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM en Td cruda) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.v` | +0,005 | Brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.abs` | 0,005 | Magnitud de la brecha (°C) RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.esp_lo` | +0,001 | Límite inferior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.esp_hi` | +0,008 | Límite superior IC 95 % espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.esp_ic` | [+0,001; +0,008] | IC 95 % espacial_2g como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.esp_bloques_a_gana` | 11 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ma_lo` | −0,005 | Límite inferior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ma_hi` | +0,014 | Límite superior IC 95 % mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ma_ic` | [−0,005; +0,014] | IC 95 % mes_anio como texto, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ma_bloques_a_gana` | 20 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_vs_tuned_sin_td.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.v` | +0,007 | Brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.abs` | 0,007 | Magnitud de la brecha (°C) RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.esp_lo` | +0,003 | Límite inferior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.esp_hi` | +0,011 | Límite superior IC 95 % espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.esp_ic` | [+0,003; +0,011] | IC 95 % espacial_2g como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.esp_bloques_a_gana` | 15 | Bloques (de 45) en que A gana, espacial_2g, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ma_lo` | −0,0002 | Límite inferior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ma_hi` | +0,015 | Límite superior IC 95 % mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ma_ic` | [−0,0002; +0,015] | IC 95 % mes_anio como texto, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ma_bloques_a_gana` | 19 | Bloques (de 48) en que A gana, mes_anio, RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.tuned_sin_td_vs_llr_simple.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(tuned sin rezagos de Td) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.v` | −0,052 | Brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.abs` | 0,052 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.esp_lo` | −0,058 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.esp_hi` | −0,045 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.esp_ic` | [−0,058; −0,045] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ma_lo` | −0,064 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ma_hi` | −0,040 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ma_ic` | [−0,064; −0,040] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ma_bloques_a_gana` | 43 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_tuned_sin_td.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(tuned sin rezagos de Td), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.v` | +0,044 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.abs` | 0,044 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.esp_lo` | +0,037 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.esp_hi` | +0,052 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.esp_ic` | [+0,037; +0,052] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.esp_bloques_a_gana` | 0 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ma_lo` | +0,024 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ma_hi` | +0,064 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ma_ic` | [+0,024; +0,064] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ma_bloques_a_gana` | 11 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_timesfm.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(TimesFM), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.v` | +0,005 | Brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.abs` | 0,005 | Magnitud de la brecha (°C) RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.esp_lo` | −0,004 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.esp_hi` | +0,013 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.esp_ic` | [−0,004; +0,013] | IC 95 % espacial_2g como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.esp_excluye_cero` | no | ¿El IC espacial_2g excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.esp_bloques_a_gana` | 17 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ma_lo` | −0,021 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ma_hi` | +0,029 | Límite superior IC 95 % mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ma_ic` | [−0,021; +0,029] | IC 95 % mes_anio como texto, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ma_excluye_cero` | no | ¿El IC mes_anio excluye cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ma_bloques_a_gana` | 17 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_med_vs_llr_rezagos.ambos_excluyen_cero` | no | ¿Los dos IC excluyen cero? RMSE(TimesFM con contexto desde 2002) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.v` | −0,025 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.abs` | 0,025 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.esp_lo` | −0,028 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.esp_hi` | −0,023 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.esp_ic` | [−0,028; −0,023] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ma_lo` | −0,034 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ma_hi` | −0,016 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ma_ic` | [−0,034; −0,016] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ma_bloques_a_gana` | 39 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_rezagos_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR con rezagos seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.v` | −0,030 | Brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.abs` | 0,030 | Magnitud de la brecha (°C) RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.esp_lo` | −0,033 | Límite inferior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.esp_hi` | −0,026 | Límite superior IC 95 % espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.esp_ic` | [−0,033; −0,026] | IC 95 % espacial_2g como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.esp_bloques_a_gana` | 45 | Bloques (de 45) en que A gana, espacial_2g, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ma_lo` | −0,039 | Límite inferior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ma_hi` | −0,021 | Límite superior IC 95 % mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ma_ic` | [−0,039; −0,021] | IC 95 % mes_anio como texto, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ma_bloques_a_gana` | 41 | Bloques (de 48) en que A gana, mes_anio, RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.timesfm_vs_llr_simple_sel.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(TimesFM) − RMSE(LLR simple seleccionado), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.v` | −0,014 | Brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.abs` | 0,014 | Magnitud de la brecha (°C) RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.esp_lo` | −0,019 | Límite inferior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.esp_hi` | −0,010 | Límite superior IC 95 % espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.esp_ic` | [−0,019; −0,010] | IC 95 % espacial_2g como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.esp_bloques_a_gana` | 42 | Bloques (de 45) en que A gana, espacial_2g, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ma_lo` | −0,022 | Límite inferior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ma_hi` | −0,006 | Límite superior IC 95 % mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ma_ic` | [−0,022; −0,006] | IC 95 % mes_anio como texto, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ma_bloques_a_gana` | 34 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR con rezagos seleccionado) − RMSE(LLR con rezagos), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.v` | −0,015 | Brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.abs` | 0,015 | Magnitud de la brecha (°C) RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.esp_lo` | −0,018 | Límite inferior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.esp_hi` | −0,011 | Límite superior IC 95 % espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.esp_ic` | [−0,018; −0,011] | IC 95 % espacial_2g como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.esp_excluye_cero` | sí | ¿El IC espacial_2g excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.esp_bloques_a_gana` | 43 | Bloques (de 45) en que A gana, espacial_2g, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ma_lo` | −0,022 | Límite inferior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ma_hi` | −0,008 | Límite superior IC 95 % mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ma_ic` | [−0,022; −0,008] | IC 95 % mes_anio como texto, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ma_excluye_cero` | sí | ¿El IC mes_anio excluye cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ma_bloques_a_gana` | 33 | Bloques (de 48) en que A gana, mes_anio, RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.peru.llr_simple_sel_vs_llr_simple.ambos_excluyen_cero` | sí | ¿Los dos IC excluyen cero? RMSE(LLR simple seleccionado) − RMSE(LLR simple), `ll4b`, Perú |
| `brecha.ll4b.panel.timesfm_td_vs_llr_rezagos_sel.ic` | n. d. | IC de TimesFM en Td cruda frente a `llr_rezagos_sel` (dominio completo) (no se calculó IC; solo diferencia puntual de RMSE) |
| `brecha.ll4b.panel.timesfm_td_vs_tuned.ic` | n. d. | IC de TimesFM en Td cruda frente a `tuned` (dominio completo) (no se calculó IC; solo diferencia puntual de RMSE) |
| `brecha.ll4.panel.timesfm_td_vs_tuned.ic` | n. d. | `timesfm_td` en `ll4` (timesfm_td solo se evaluó en ll4b) |
| `brecha.ll4b.peru.timesfm_td_vs_llr_rezagos_sel.ic` | n. d. | IC de TimesFM en Td cruda frente a `llr_rezagos_sel` (Perú) (no se calculó IC; solo diferencia puntual de RMSE) |
| `brecha.ll4b.peru.timesfm_td_vs_tuned.ic` | n. d. | IC de TimesFM en Td cruda frente a `tuned` (Perú) (no se calculó IC; solo diferencia puntual de RMSE) |
| `brecha.ll4.peru.timesfm_td_vs_tuned.ic` | n. d. | `timesfm_td` en `ll4` (timesfm_td solo se evaluó en ll4b) |

## brecha_conteo

| clave | valor | significado |
|---|---|---|
| `brecha_conteo.timesfm_vs_tuned.n_excluyen` | 4 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs tuned |
| `brecha_conteo.timesfm_vs_tuned.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú, 2013–2016 en el dominio completo y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_tuned.incluyen` | ninguno | Casos en que algún IC incluye cero |
| `brecha_conteo.timesfm_vs_llr_rezagos_sel.n_excluyen` | 3 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs LLR con rezagos seleccionado |
| `brecha_conteo.timesfm_vs_llr_rezagos_sel.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_llr_rezagos_sel.incluyen` | 2013–2016 en el dominio completo | Casos en que algún IC incluye cero |
| `brecha_conteo.timesfm_vs_tuned_sin_td.n_excluyen` | 3 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs tuned sin rezagos de Td |
| `brecha_conteo.timesfm_vs_tuned_sin_td.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_tuned_sin_td.incluyen` | 2013–2016 en el dominio completo | Casos en que algún IC incluye cero |
| `brecha_conteo.timesfm_vs_llr_simple.n_excluyen` | 3 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs LLR simple |
| `brecha_conteo.timesfm_vs_llr_simple.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_llr_simple.incluyen` | 2013–2016 en el dominio completo | Casos en que algún IC incluye cero |
| `brecha_conteo.timesfm_vs_llr_simple_sel.n_excluyen` | 3 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs LLR simple seleccionado |
| `brecha_conteo.timesfm_vs_llr_simple_sel.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_llr_simple_sel.incluyen` | 2013–2016 en el dominio completo | Casos en que algún IC incluye cero |
| `brecha_conteo.timesfm_vs_llr_rezagos.n_excluyen` | 3 | Casos (de 4) en que los dos IC excluyen cero, TimesFM vs LLR con rezagos |
| `brecha_conteo.timesfm_vs_llr_rezagos.excluyen` | 2009–2012 en el dominio completo, 2009–2012 en Perú y 2013–2016 en Perú | Casos con ambos IC sin cero |
| `brecha_conteo.timesfm_vs_llr_rezagos.incluyen` | 2013–2016 en el dominio completo | Casos en que algún IC incluye cero |
| `brecha_conteo.llr_ll4_panel.esp_excluyen` | LLR simple y LLR simple seleccionado | LLR sin zonas frente a los que el IC espacial excluye cero (`ll4`, dominio completo) |
| `brecha_conteo.llr_ll4_panel.n_ma_excluyen` | 0 | Número de LLR sin zonas (de 4) frente a los que el IC mes-año excluye cero (`ll4`, dominio completo) |
| `brecha_conteo.llr_ll4_panel.n_esp_excluyen` | 2 | Número de LLR sin zonas (de 4) frente a los que el IC espacial excluye cero (`ll4`, dominio completo) |

## puntual

| clave | valor | significado |
|---|---|---|
| `puntual.ll4b.panel.timesfm_td_vs_llr_rezagos_sel` | +0,031 | Diferencia puntual (sin IC) Td cruda − `llr_rezagos_sel` |
| `puntual.ll4b.panel.timesfm_td_vs_tuned` | −0,016 | Diferencia puntual (sin IC) Td cruda − `tuned` (a1_brechas.csv no tiene IC para esta pareja) |
| `puntual.ll4b.panel.timesfm_vs_timesfm_td` | −0,060 | Diferencia puntual (sin IC) TimesFM `tmin_anom_full` − Td cruda (signo opuesto al de `puntual.*.timesfm_td_vs_*`) (a1_brechas.csv no tiene IC para esta pareja) |
| `puntual.ll4b.peru.timesfm_td_vs_llr_rezagos_sel` | +0,010 | Diferencia puntual (sin IC) Td cruda − `llr_rezagos_sel` |
| `puntual.ll4b.peru.timesfm_td_vs_tuned` | −0,021 | Diferencia puntual (sin IC) Td cruda − `tuned` (a1_brechas.csv no tiene IC para esta pareja) |
| `puntual.ll4b.peru.timesfm_vs_timesfm_td` | −0,036 | Diferencia puntual (sin IC) TimesFM `tmin_anom_full` − Td cruda (signo opuesto al de `puntual.*.timesfm_td_vs_*`) (a1_brechas.csv no tiene IC para esta pareja) |

## brecha_zona

| clave | valor | significado |
|---|---|---|
| `brecha_zona.ic` | n. d. | IC de las brechas por zona (las brechas por zona son descriptivas, sin IC) |

## zonas

| clave | valor | significado |
|---|---|---|
| `zonas.ll4b.panel.n_zonas` | 33 | Zonas con celdas en `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.n_negativas` | 33 | Zonas con brecha por zona TimesFM − tuned, `ll4b`, dominio completo negativa |
| `zonas.ll4b.panel.vs_tuned.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned, `ll4b`, dominio completo positiva |
| `zonas.ll4b.panel.vs_tuned.mas_negativa` | −0,182 | Valor más negativo de la brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.menos_negativa` | −0,030 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.mas_negativa_2d` | −0,18 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.peor_zona` | C (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.peor_zona_id` | 26 | Identificador de esa zona |
| `zonas.ll4b.panel.vs_tuned.peor_zona_gap` | −0,030 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_tuned.peor_zona_celdas` | 39 | Celdas de esa zona |
| `zonas.ll4b.panel.vs_tuned.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned.mejor_zona_gap` | −0,182 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_tuned.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.n_negativas` | 33 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo negativa |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.n_positivas` | 0 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo positiva |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.mas_negativa` | −0,048 | Valor más negativo de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.menos_negativa` | −0,006 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.mas_negativa_2d` | −0,05 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.menos_negativa_2d` | −0,01 | Valor más alto (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.peor_zona` | D (i) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.peor_zona_id` | 31 | Identificador de esa zona |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.peor_zona_gap` | −0,006 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.peor_zona_celdas` | 20 | Celdas de esa zona |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.mejor_zona` | C (o , i) C' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.mejor_zona_gap` | −0,048 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_llr_rezagos_sel.mejor_zona_celdas` | 174 | Celdas de esa zona |
| `zonas.ll4b.panel.vs_tuned_sin_td.n_negativas` | 33 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo negativa |
| `zonas.ll4b.panel.vs_tuned_sin_td.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo positiva |
| `zonas.ll4b.panel.vs_tuned_sin_td.mas_negativa` | −0,143 | Valor más negativo de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.menos_negativa` | −0,026 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.mas_negativa_2d` | −0,14 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.peor_zona` | B (i) B' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.peor_zona_id` | 4 | Identificador de esa zona |
| `zonas.ll4b.panel.vs_tuned_sin_td.peor_zona_gap` | −0,026 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_tuned_sin_td.peor_zona_celdas` | 174 | Celdas de esa zona |
| `zonas.ll4b.panel.vs_tuned_sin_td.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zonas.ll4b.panel.vs_tuned_sin_td.mejor_zona_gap` | −0,143 | Brecha de esa zona |
| `zonas.ll4b.panel.vs_tuned_sin_td.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4b.peru.n_zonas` | 32 | Zonas con celdas en `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.n_negativas` | 32 | Zonas con brecha por zona TimesFM − tuned, `ll4b`, Perú negativa |
| `zonas.ll4b.peru.vs_tuned.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned, `ll4b`, Perú positiva |
| `zonas.ll4b.peru.vs_tuned.mas_negativa` | −0,182 | Valor más negativo de la brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.menos_negativa` | −0,030 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.mas_negativa_2d` | −0,18 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.peor_zona` | C (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.peor_zona_id` | 26 | Identificador de esa zona |
| `zonas.ll4b.peru.vs_tuned.peor_zona_gap` | −0,030 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_tuned.peor_zona_celdas` | 39 | Celdas de esa zona |
| `zonas.ll4b.peru.vs_tuned.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned.mejor_zona_gap` | −0,182 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_tuned.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.n_negativas` | 32 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú negativa |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.n_positivas` | 0 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú positiva |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.mas_negativa` | −0,051 | Valor más negativo de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.menos_negativa` | −0,014 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.mas_negativa_2d` | −0,05 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.menos_negativa_2d` | −0,01 | Valor más alto (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.peor_zona` | E (d) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.peor_zona_id` | 35 | Identificador de esa zona |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.peor_zona_gap` | −0,014 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.peor_zona_celdas` | 199 | Celdas de esa zona |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.mejor_zona` | C (o , i) C' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.mejor_zona_gap` | −0,051 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_llr_rezagos_sel.mejor_zona_celdas` | 145 | Celdas de esa zona |
| `zonas.ll4b.peru.vs_tuned_sin_td.n_negativas` | 32 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú negativa |
| `zonas.ll4b.peru.vs_tuned_sin_td.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú positiva |
| `zonas.ll4b.peru.vs_tuned_sin_td.mas_negativa` | −0,143 | Valor más negativo de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.menos_negativa` | −0,026 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.mas_negativa_2d` | −0,14 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.peor_zona` | B (i) B' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.peor_zona_id` | 4 | Identificador de esa zona |
| `zonas.ll4b.peru.vs_tuned_sin_td.peor_zona_gap` | −0,026 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_tuned_sin_td.peor_zona_celdas` | 174 | Celdas de esa zona |
| `zonas.ll4b.peru.vs_tuned_sin_td.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zonas.ll4b.peru.vs_tuned_sin_td.mejor_zona_gap` | −0,143 | Brecha de esa zona |
| `zonas.ll4b.peru.vs_tuned_sin_td.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.panel.n_zonas` | 33 | Zonas con celdas en `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.n_negativas` | 33 | Zonas con brecha por zona TimesFM − tuned, `ll4`, dominio completo negativa |
| `zonas.ll4.panel.vs_tuned.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned, `ll4`, dominio completo positiva |
| `zonas.ll4.panel.vs_tuned.mas_negativa` | −0,302 | Valor más negativo de la brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.menos_negativa` | −0,033 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.mas_negativa_2d` | −0,30 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.peor_zona` | B (i) B' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.peor_zona_id` | 4 | Identificador de esa zona |
| `zonas.ll4.panel.vs_tuned.peor_zona_gap` | −0,033 | Brecha de esa zona |
| `zonas.ll4.panel.vs_tuned.peor_zona_celdas` | 174 | Celdas de esa zona |
| `zonas.ll4.panel.vs_tuned.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned.mejor_zona_gap` | −0,302 | Brecha de esa zona |
| `zonas.ll4.panel.vs_tuned.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.panel.vs_llr_rezagos_sel.n_negativas` | 32 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo negativa |
| `zonas.ll4.panel.vs_llr_rezagos_sel.n_positivas` | 1 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo positiva |
| `zonas.ll4.panel.vs_llr_rezagos_sel.mas_negativa` | −0,074 | Valor más negativo de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.menos_negativa` | +0,014 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.mas_negativa_2d` | −0,07 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.menos_negativa_2d` | +0,01 | Valor más alto (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.peor_zona` | A (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.peor_zona_id` | 0 | Identificador de esa zona |
| `zonas.ll4.panel.vs_llr_rezagos_sel.peor_zona_gap` | +0,014 | Brecha de esa zona |
| `zonas.ll4.panel.vs_llr_rezagos_sel.peor_zona_celdas` | 7.091 | Celdas de esa zona |
| `zonas.ll4.panel.vs_llr_rezagos_sel.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_llr_rezagos_sel.mejor_zona_gap` | −0,074 | Brecha de esa zona |
| `zonas.ll4.panel.vs_llr_rezagos_sel.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.panel.vs_tuned_sin_td.n_negativas` | 33 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo negativa |
| `zonas.ll4.panel.vs_tuned_sin_td.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo positiva |
| `zonas.ll4.panel.vs_tuned_sin_td.mas_negativa` | −0,205 | Valor más negativo de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.menos_negativa` | −0,003 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.mas_negativa_2d` | −0,20 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.menos_negativa_2d` | −0,003 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.peor_zona` | A (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.peor_zona_id` | 0 | Identificador de esa zona |
| `zonas.ll4.panel.vs_tuned_sin_td.peor_zona_gap` | −0,003 | Brecha de esa zona |
| `zonas.ll4.panel.vs_tuned_sin_td.peor_zona_celdas` | 7.091 | Celdas de esa zona |
| `zonas.ll4.panel.vs_tuned_sin_td.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zonas.ll4.panel.vs_tuned_sin_td.mejor_zona_gap` | −0,205 | Brecha de esa zona |
| `zonas.ll4.panel.vs_tuned_sin_td.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.peru.n_zonas` | 32 | Zonas con celdas en `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.n_negativas` | 32 | Zonas con brecha por zona TimesFM − tuned, `ll4`, Perú negativa |
| `zonas.ll4.peru.vs_tuned.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned, `ll4`, Perú positiva |
| `zonas.ll4.peru.vs_tuned.mas_negativa` | −0,302 | Valor más negativo de la brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.menos_negativa` | −0,033 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.mas_negativa_2d` | −0,30 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.menos_negativa_2d` | −0,03 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.peor_zona` | B (i) B' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.peor_zona_id` | 4 | Identificador de esa zona |
| `zonas.ll4.peru.vs_tuned.peor_zona_gap` | −0,033 | Brecha de esa zona |
| `zonas.ll4.peru.vs_tuned.peor_zona_celdas` | 174 | Celdas de esa zona |
| `zonas.ll4.peru.vs_tuned.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned.mejor_zona_gap` | −0,302 | Brecha de esa zona |
| `zonas.ll4.peru.vs_tuned.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.peru.vs_llr_rezagos_sel.n_negativas` | 32 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú negativa |
| `zonas.ll4.peru.vs_llr_rezagos_sel.n_positivas` | 0 | Zonas con brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú positiva |
| `zonas.ll4.peru.vs_llr_rezagos_sel.mas_negativa` | −0,074 | Valor más negativo de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.menos_negativa` | −0,006 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.mas_negativa_2d` | −0,07 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.menos_negativa_2d` | −0,01 | Valor más alto (2 decimales) de la brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.peor_zona` | A (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.peor_zona_id` | 0 | Identificador de esa zona |
| `zonas.ll4.peru.vs_llr_rezagos_sel.peor_zona_gap` | −0,006 | Brecha de esa zona |
| `zonas.ll4.peru.vs_llr_rezagos_sel.peor_zona_celdas` | 2.147 | Celdas de esa zona |
| `zonas.ll4.peru.vs_llr_rezagos_sel.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zonas.ll4.peru.vs_llr_rezagos_sel.mejor_zona_gap` | −0,074 | Brecha de esa zona |
| `zonas.ll4.peru.vs_llr_rezagos_sel.mejor_zona_celdas` | 1 | Celdas de esa zona |
| `zonas.ll4.peru.vs_tuned_sin_td.n_negativas` | 32 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú negativa |
| `zonas.ll4.peru.vs_tuned_sin_td.n_positivas` | 0 | Zonas con brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú positiva |
| `zonas.ll4.peru.vs_tuned_sin_td.mas_negativa` | −0,205 | Valor más negativo de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.menos_negativa` | −0,019 | Valor más alto (más cercano a cero o positivo) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.mas_negativa_2d` | −0,20 | Valor más negativo (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.menos_negativa_2d` | −0,02 | Valor más alto (2 decimales) de la brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.peor_zona` | A (r) A' | Etiqueta de la zona con peor desempeño relativo de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.peor_zona_id` | 0 | Identificador de esa zona |
| `zonas.ll4.peru.vs_tuned_sin_td.peor_zona_gap` | −0,019 | Brecha de esa zona |
| `zonas.ll4.peru.vs_tuned_sin_td.peor_zona_celdas` | 2.147 | Celdas de esa zona |
| `zonas.ll4.peru.vs_tuned_sin_td.mejor_zona` | D (i) D' | Etiqueta de la zona con mayor ventaja de TimesFM, brecha por zona TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zonas.ll4.peru.vs_tuned_sin_td.mejor_zona_gap` | −0,205 | Brecha de esa zona |
| `zonas.ll4.peru.vs_tuned_sin_td.mejor_zona_celdas` | 1 | Celdas de esa zona |

## victorias

| clave | valor | significado |
|---|---|---|
| `victorias.ll4.panel.clim_vs_tuned` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_tuned_sin_td` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_llr_simple` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_llr_rezagos` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_llr_simple_sel` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_timesfm` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.clim_vs_timesfm_med` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_clim` | 33 | Zonas (de 33) en que tuned tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_tuned_sin_td` | 1 | Zonas (de 33) en que tuned tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_llr_simple` | 4 | Zonas (de 33) en que tuned tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_llr_rezagos` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_llr_simple_sel` | 2 | Zonas (de 33) en que tuned tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_timesfm` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_vs_timesfm_med` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_clim` | 33 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_tuned` | 32 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_llr_simple` | 17 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_llr_rezagos` | 0 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_llr_simple_sel` | 13 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_timesfm` | 0 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.tuned_sin_td_vs_timesfm_med` | 3 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_clim` | 33 | Zonas (de 33) en que LLR simple tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_tuned` | 29 | Zonas (de 33) en que LLR simple tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_tuned_sin_td` | 16 | Zonas (de 33) en que LLR simple tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_llr_rezagos` | 5 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_llr_simple_sel` | 4 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_timesfm` | 1 | Zonas (de 33) en que LLR simple tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_vs_timesfm_med` | 2 | Zonas (de 33) en que LLR simple tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_clim` | 33 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_tuned` | 33 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_tuned_sin_td` | 33 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_llr_simple` | 28 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_llr_simple_sel` | 17 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_llr_rezagos_sel` | 6 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_timesfm` | 1 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_vs_timesfm_med` | 7 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_clim` | 33 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_tuned` | 31 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_tuned_sin_td` | 20 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_llr_simple` | 29 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_llr_rezagos` | 16 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_llr_rezagos_sel` | 4 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_timesfm` | 0 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_simple_sel_vs_timesfm_med` | 3 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_clim` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_tuned` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_tuned_sin_td` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_llr_simple` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_llr_rezagos` | 27 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_llr_simple_sel` | 29 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_timesfm` | 1 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.panel.llr_rezagos_sel_vs_timesfm_med` | 10 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_clim` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_tuned` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_tuned_sin_td` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_llr_simple` | 32 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_llr_rezagos` | 32 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_llr_simple_sel` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_llr_rezagos_sel` | 32 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_vs_timesfm_med` | 32 | Zonas (de 33) en que TimesFM tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_clim` | 33 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que climatología, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_tuned` | 33 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_tuned_sin_td` | 30 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned sin rezagos de Td, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_llr_simple` | 31 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_llr_rezagos` | 26 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_llr_simple_sel` | 30 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_llr_rezagos_sel` | 23 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, dominio completo |
| `victorias.ll4.panel.timesfm_med_vs_timesfm` | 1 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM, `ll4`, dominio completo |
| `victorias.ll4.peru.clim_vs_tuned` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_tuned_sin_td` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_llr_simple` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_llr_rezagos` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_llr_simple_sel` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_timesfm` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.clim_vs_timesfm_med` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_clim` | 32 | Zonas (de 32) en que tuned tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_tuned_sin_td` | 2 | Zonas (de 32) en que tuned tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_llr_simple` | 6 | Zonas (de 32) en que tuned tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_llr_rezagos` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_llr_simple_sel` | 4 | Zonas (de 32) en que tuned tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_timesfm` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.tuned_vs_timesfm_med` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_clim` | 32 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_tuned` | 30 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_llr_simple` | 17 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_llr_rezagos` | 0 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_llr_simple_sel` | 14 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_timesfm` | 0 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.tuned_sin_td_vs_timesfm_med` | 3 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_clim` | 32 | Zonas (de 32) en que LLR simple tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_tuned` | 26 | Zonas (de 32) en que LLR simple tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_tuned_sin_td` | 15 | Zonas (de 32) en que LLR simple tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_llr_rezagos` | 4 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_llr_simple_sel` | 5 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_timesfm` | 0 | Zonas (de 32) en que LLR simple tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_vs_timesfm_med` | 1 | Zonas (de 32) en que LLR simple tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_clim` | 32 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_tuned` | 32 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_tuned_sin_td` | 32 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_llr_simple` | 28 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_llr_simple_sel` | 17 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_llr_rezagos_sel` | 6 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_timesfm` | 0 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_vs_timesfm_med` | 5 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_clim` | 32 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_tuned` | 28 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_tuned_sin_td` | 18 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_llr_simple` | 27 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_llr_rezagos` | 15 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_llr_rezagos_sel` | 4 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_timesfm` | 0 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.llr_simple_sel_vs_timesfm_med` | 2 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_clim` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_tuned` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_tuned_sin_td` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_llr_simple` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_llr_rezagos` | 26 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_llr_simple_sel` | 28 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_timesfm` | 0 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4.peru.llr_rezagos_sel_vs_timesfm_med` | 9 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_clim` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_tuned` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_tuned_sin_td` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_llr_simple` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_llr_rezagos` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_llr_simple_sel` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_llr_rezagos_sel` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_vs_timesfm_med` | 30 | Zonas (de 32) en que TimesFM tiene menor RMSE que TimesFM con contexto desde 2002, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_clim` | 32 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que climatología, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_tuned` | 32 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_tuned_sin_td` | 29 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned sin rezagos de Td, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_llr_simple` | 31 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_llr_rezagos` | 27 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_llr_simple_sel` | 30 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_llr_rezagos_sel` | 23 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos seleccionado, `ll4`, Perú |
| `victorias.ll4.peru.timesfm_med_vs_timesfm` | 2 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM, `ll4`, Perú |
| `victorias.ll4b.panel.clim_vs_tuned` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_tuned_sin_td` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_llr_simple` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_llr_rezagos` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_llr_simple_sel` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_timesfm_td` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_timesfm` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.clim_vs_timesfm_med` | 0 | Zonas (de 33) en que climatología tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_clim` | 33 | Zonas (de 33) en que tuned tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_tuned_sin_td` | 3 | Zonas (de 33) en que tuned tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_llr_simple` | 5 | Zonas (de 33) en que tuned tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_llr_rezagos` | 1 | Zonas (de 33) en que tuned tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_llr_simple_sel` | 1 | Zonas (de 33) en que tuned tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_timesfm_td` | 3 | Zonas (de 33) en que tuned tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_timesfm` | 0 | Zonas (de 33) en que tuned tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_vs_timesfm_med` | 7 | Zonas (de 33) en que tuned tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_clim` | 33 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_tuned` | 30 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_llr_simple` | 12 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_llr_rezagos` | 1 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_llr_simple_sel` | 3 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_timesfm_td` | 5 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_timesfm` | 0 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.tuned_sin_td_vs_timesfm_med` | 11 | Zonas (de 33) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_clim` | 33 | Zonas (de 33) en que LLR simple tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_tuned` | 28 | Zonas (de 33) en que LLR simple tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_tuned_sin_td` | 21 | Zonas (de 33) en que LLR simple tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_llr_rezagos` | 12 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_llr_simple_sel` | 2 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_llr_rezagos_sel` | 0 | Zonas (de 33) en que LLR simple tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_timesfm_td` | 4 | Zonas (de 33) en que LLR simple tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_timesfm` | 0 | Zonas (de 33) en que LLR simple tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_vs_timesfm_med` | 14 | Zonas (de 33) en que LLR simple tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_clim` | 33 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_tuned` | 32 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_tuned_sin_td` | 32 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_llr_simple` | 21 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_llr_simple_sel` | 14 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_llr_rezagos_sel` | 2 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_timesfm_td` | 6 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_timesfm` | 0 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_vs_timesfm_med` | 17 | Zonas (de 33) en que LLR con rezagos tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_clim` | 33 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_tuned` | 32 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_tuned_sin_td` | 30 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_llr_simple` | 31 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_llr_rezagos` | 19 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_llr_rezagos_sel` | 5 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_timesfm_td` | 12 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_timesfm` | 0 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_simple_sel_vs_timesfm_med` | 23 | Zonas (de 33) en que LLR simple seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_clim` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_tuned` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_tuned_sin_td` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_llr_simple` | 33 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_llr_rezagos` | 31 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_llr_simple_sel` | 28 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_timesfm_td` | 13 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_timesfm` | 0 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.llr_rezagos_sel_vs_timesfm_med` | 27 | Zonas (de 33) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_clim` | 33 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_tuned` | 30 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_tuned_sin_td` | 28 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_llr_simple` | 29 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_llr_rezagos` | 27 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_llr_simple_sel` | 21 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_llr_rezagos_sel` | 20 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_timesfm` | 3 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_td_vs_timesfm_med` | 27 | Zonas (de 33) en que TimesFM en Td cruda tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_clim` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_tuned` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_tuned_sin_td` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_llr_simple` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_llr_rezagos` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_llr_simple_sel` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_llr_rezagos_sel` | 33 | Zonas (de 33) en que TimesFM tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_timesfm_td` | 30 | Zonas (de 33) en que TimesFM tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_vs_timesfm_med` | 32 | Zonas (de 33) en que TimesFM tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_clim` | 33 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que climatología, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_tuned` | 26 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_tuned_sin_td` | 22 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_llr_simple` | 19 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_llr_rezagos` | 16 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_llr_simple_sel` | 10 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_llr_rezagos_sel` | 6 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_timesfm_td` | 6 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM en Td cruda, `ll4b`, dominio completo |
| `victorias.ll4b.panel.timesfm_med_vs_timesfm` | 1 | Zonas (de 33) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM, `ll4b`, dominio completo |
| `victorias.ll4b.peru.clim_vs_tuned` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_tuned_sin_td` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_llr_simple` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_llr_rezagos` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_llr_simple_sel` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_timesfm_td` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_timesfm` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.clim_vs_timesfm_med` | 0 | Zonas (de 32) en que climatología tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_clim` | 32 | Zonas (de 32) en que tuned tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_tuned_sin_td` | 5 | Zonas (de 32) en que tuned tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_llr_simple` | 6 | Zonas (de 32) en que tuned tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_llr_rezagos` | 1 | Zonas (de 32) en que tuned tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_llr_simple_sel` | 1 | Zonas (de 32) en que tuned tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_timesfm_td` | 3 | Zonas (de 32) en que tuned tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_timesfm` | 0 | Zonas (de 32) en que tuned tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_vs_timesfm_med` | 10 | Zonas (de 32) en que tuned tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_clim` | 32 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_tuned` | 27 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_llr_simple` | 12 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_llr_rezagos` | 1 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_llr_simple_sel` | 3 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_timesfm_td` | 3 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_timesfm` | 0 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.tuned_sin_td_vs_timesfm_med` | 12 | Zonas (de 32) en que tuned sin rezagos de Td tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_clim` | 32 | Zonas (de 32) en que LLR simple tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_tuned` | 26 | Zonas (de 32) en que LLR simple tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_tuned_sin_td` | 20 | Zonas (de 32) en que LLR simple tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_llr_rezagos` | 10 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_llr_simple_sel` | 1 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_llr_rezagos_sel` | 0 | Zonas (de 32) en que LLR simple tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_timesfm_td` | 4 | Zonas (de 32) en que LLR simple tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_timesfm` | 0 | Zonas (de 32) en que LLR simple tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_vs_timesfm_med` | 14 | Zonas (de 32) en que LLR simple tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_clim` | 32 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_tuned` | 31 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_tuned_sin_td` | 31 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_llr_simple` | 22 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_llr_simple_sel` | 13 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_llr_rezagos_sel` | 2 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_timesfm_td` | 6 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_timesfm` | 0 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_vs_timesfm_med` | 18 | Zonas (de 32) en que LLR con rezagos tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_clim` | 32 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_tuned` | 31 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_tuned_sin_td` | 29 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_llr_simple` | 31 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_llr_rezagos` | 19 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_llr_rezagos_sel` | 6 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_timesfm_td` | 9 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_timesfm` | 0 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_simple_sel_vs_timesfm_med` | 24 | Zonas (de 32) en que LLR simple seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_clim` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_tuned` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_tuned_sin_td` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_llr_simple` | 32 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_llr_rezagos` | 30 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_llr_simple_sel` | 26 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_timesfm_td` | 10 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_timesfm` | 0 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.llr_rezagos_sel_vs_timesfm_med` | 25 | Zonas (de 32) en que LLR con rezagos seleccionado tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_clim` | 32 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_tuned` | 29 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_tuned_sin_td` | 29 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_llr_simple` | 28 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_llr_rezagos` | 26 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_llr_simple_sel` | 23 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_llr_rezagos_sel` | 22 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_timesfm` | 3 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que TimesFM, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_td_vs_timesfm_med` | 26 | Zonas (de 32) en que TimesFM en Td cruda tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_clim` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_tuned` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_tuned_sin_td` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_llr_simple` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_llr_rezagos` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_llr_simple_sel` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_llr_rezagos_sel` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_timesfm_td` | 29 | Zonas (de 32) en que TimesFM tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_vs_timesfm_med` | 32 | Zonas (de 32) en que TimesFM tiene menor RMSE que TimesFM con contexto desde 2002, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_clim` | 32 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que climatología, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_tuned` | 22 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_tuned_sin_td` | 20 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que tuned sin rezagos de Td, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_llr_simple` | 18 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_llr_rezagos` | 14 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_llr_simple_sel` | 8 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR simple seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_llr_rezagos_sel` | 7 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que LLR con rezagos seleccionado, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_timesfm_td` | 6 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM en Td cruda, `ll4b`, Perú |
| `victorias.ll4b.peru.timesfm_med_vs_timesfm` | 0 | Zonas (de 32) en que TimesFM con contexto desde 2002 tiene menor RMSE que TimesFM, `ll4b`, Perú |

## cribado

| clave | valor | significado |
|---|---|---|
| `cribado.n_celdas` | 1.092 | Celdas puntuadas del cribado limpio (en común con `tuned`) |
| `cribado.n_filas` | 1.595.412 | Filas del cribado limpio |
| `cribado.n_variantes` | 9 | Variantes de TimesFM del cribado |
| `cribado.n_menor_tuned` | 6 | Variantes con RMSE menor que `tuned` |
| `cribado.n_mayor_tuned` | 3 | Variantes con RMSE mayor que `tuned` |
| `cribado.pierden` | tmin_td_short, uni_anom_full y uni_td_full | Variantes que pierden frente a `tuned` |
| `cribado.tuned.rmse` | 0,933 | RMSE (°C) de tuned en el cribado |
| `cribado.tuned.mae` | 0,684 | MAE (°C) de tuned en el cribado |
| `cribado.tuned.sesgo` | +0,089 | Sesgo (°C) de tuned en el cribado |
| `cribado.clim.rmse` | 1,284 | RMSE (°C) de clim en el cribado |
| `cribado.clim.mae` | 0,975 | MAE (°C) de clim en el cribado |
| `cribado.clim.sesgo` | −0,166 | Sesgo (°C) de clim en el cribado |
| `cribado.v.tmin_anom_full.rmse` | 0,839 | RMSE (°C) de la variante tmin_anom_full |
| `cribado.v.tmin_anom_full.mae` | 0,615 | MAE (°C) de la variante tmin_anom_full |
| `cribado.v.tmin_anom_full.sesgo` | +0,065 | Sesgo (°C) de la variante tmin_anom_full |
| `cribado.v.tmin_anom_full.delta_tuned` | −0,094 | RMSE de tmin_anom_full menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_anom_full.menor_tuned` | sí | ¿tmin_anom_full tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_anom_full.skill` | +0,347 | Habilidad frente a climatología de tmin_anom_full |
| `cribado.v.tmin_doy_td_full.rmse` | 0,862 | RMSE (°C) de la variante tmin_doy_td_full |
| `cribado.v.tmin_doy_td_full.mae` | 0,632 | MAE (°C) de la variante tmin_doy_td_full |
| `cribado.v.tmin_doy_td_full.sesgo` | +0,129 | Sesgo (°C) de la variante tmin_doy_td_full |
| `cribado.v.tmin_doy_td_full.delta_tuned` | −0,071 | RMSE de tmin_doy_td_full menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_doy_td_full.menor_tuned` | sí | ¿tmin_doy_td_full tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_doy_td_full.skill` | +0,329 | Habilidad frente a climatología de tmin_doy_td_full |
| `cribado.v.tmin_td_symavg.rmse` | 0,864 | RMSE (°C) de la variante tmin_td_symavg |
| `cribado.v.tmin_td_symavg.mae` | 0,634 | MAE (°C) de la variante tmin_td_symavg |
| `cribado.v.tmin_td_symavg.sesgo` | +0,119 | Sesgo (°C) de la variante tmin_td_symavg |
| `cribado.v.tmin_td_symavg.delta_tuned` | −0,069 | RMSE de tmin_td_symavg menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_td_symavg.menor_tuned` | sí | ¿tmin_td_symavg tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_td_symavg.skill` | +0,327 | Habilidad frente a climatología de tmin_td_symavg |
| `cribado.v.tmin_td_znorm.rmse` | 0,872 | RMSE (°C) de la variante tmin_td_znorm |
| `cribado.v.tmin_td_znorm.mae` | 0,640 | MAE (°C) de la variante tmin_td_znorm |
| `cribado.v.tmin_td_znorm.sesgo` | +0,124 | Sesgo (°C) de la variante tmin_td_znorm |
| `cribado.v.tmin_td_znorm.delta_tuned` | −0,061 | RMSE de tmin_td_znorm menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_td_znorm.menor_tuned` | sí | ¿tmin_td_znorm tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_td_znorm.skill` | +0,321 | Habilidad frente a climatología de tmin_td_znorm |
| `cribado.v.tmin_td_full.rmse` | 0,872 | RMSE (°C) de la variante tmin_td_full |
| `cribado.v.tmin_td_full.mae` | 0,640 | MAE (°C) de la variante tmin_td_full |
| `cribado.v.tmin_td_full.sesgo` | +0,124 | Sesgo (°C) de la variante tmin_td_full |
| `cribado.v.tmin_td_full.delta_tuned` | −0,061 | RMSE de tmin_td_full menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_td_full.menor_tuned` | sí | ¿tmin_td_full tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_td_full.skill` | +0,321 | Habilidad frente a climatología de tmin_td_full |
| `cribado.v.tmin_td_med.rmse` | 0,879 | RMSE (°C) de la variante tmin_td_med |
| `cribado.v.tmin_td_med.mae` | 0,648 | MAE (°C) de la variante tmin_td_med |
| `cribado.v.tmin_td_med.sesgo` | +0,100 | Sesgo (°C) de la variante tmin_td_med |
| `cribado.v.tmin_td_med.delta_tuned` | −0,053 | RMSE de tmin_td_med menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_td_med.menor_tuned` | sí | ¿tmin_td_med tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_td_med.skill` | +0,315 | Habilidad frente a climatología de tmin_td_med |
| `cribado.v.tmin_td_short.rmse` | 0,948 | RMSE (°C) de la variante tmin_td_short |
| `cribado.v.tmin_td_short.mae` | 0,703 | MAE (°C) de la variante tmin_td_short |
| `cribado.v.tmin_td_short.sesgo` | +0,129 | Sesgo (°C) de la variante tmin_td_short |
| `cribado.v.tmin_td_short.delta_tuned` | +0,015 | RMSE de tmin_td_short menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.tmin_td_short.menor_tuned` | no | ¿tmin_td_short tiene RMSE menor que `tuned`? |
| `cribado.v.tmin_td_short.skill` | +0,262 | Habilidad frente a climatología de tmin_td_short |
| `cribado.v.uni_anom_full.rmse` | 1,278 | RMSE (°C) de la variante uni_anom_full |
| `cribado.v.uni_anom_full.mae` | 0,965 | MAE (°C) de la variante uni_anom_full |
| `cribado.v.uni_anom_full.sesgo` | −0,025 | Sesgo (°C) de la variante uni_anom_full |
| `cribado.v.uni_anom_full.delta_tuned` | +0,345 | RMSE de uni_anom_full menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.uni_anom_full.menor_tuned` | no | ¿uni_anom_full tiene RMSE menor que `tuned`? |
| `cribado.v.uni_anom_full.skill` | +0,005 | Habilidad frente a climatología de uni_anom_full |
| `cribado.v.uni_td_full.rmse` | 1,312 | RMSE (°C) de la variante uni_td_full |
| `cribado.v.uni_td_full.mae` | 0,990 | MAE (°C) de la variante uni_td_full |
| `cribado.v.uni_td_full.sesgo` | −0,049 | Sesgo (°C) de la variante uni_td_full |
| `cribado.v.uni_td_full.delta_tuned` | +0,380 | RMSE de uni_td_full menos RMSE de `tuned` (puntual, sin IC) |
| `cribado.v.uni_td_full.menor_tuned` | no | ¿uni_td_full tiene RMSE menor que `tuned`? |
| `cribado.v.uni_td_full.skill` | −0,022 | Habilidad frente a climatología de uni_td_full |
| `cribado.dif_td_full_znorm` | 1,12 × 10^−8^ | Diferencia de RMSE (°C) entre `tmin_td_full` y `tmin_td_znorm` (la igualdad de predicciones no se comprobó) |
| `cribado.n_celdas_predichas` | 1.106 | Celdas predichas en el cribado (más que las puntuadas en común con `tuned`) |
| `cribado.mejor_variante` | tmin_anom_full | Variante de TimesFM con menor RMSE en el cribado |

## escalera

| clave | valor | significado |
|---|---|---|
| `escalera.ll4b.clim.i1981.rmse` | 1,143 | RMSE (°C) clim, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.clim.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, clim, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.clim.i1981.anios` | 28 | Años de historial, clim, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1981.rmse` | 0,771 | RMSE (°C) timesfm, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1981.anios` | 28 | Años de historial, timesfm, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1981.rmse` | 0,823 | RMSE (°C) llr_simple, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1981.anios` | 28 | Años de historial, llr_simple, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1981.rmse` | 0,817 | RMSE (°C) llr_rezagos, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1981.anios` | 28 | Años de historial, llr_rezagos, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1986.rmse` | 0,770 | RMSE (°C) timesfm, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1986.delta` | −0,0004 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1986.anios` | 23 | Años de historial, timesfm, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1986.rmse` | 0,814 | RMSE (°C) llr_simple, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1986.delta` | −0,009 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1986.anios` | 23 | Años de historial, llr_simple, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1986.rmse` | 0,806 | RMSE (°C) llr_rezagos, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1986.delta` | −0,011 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1986.anios` | 23 | Años de historial, llr_rezagos, inicio 1986, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1991.rmse` | 0,769 | RMSE (°C) timesfm, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1991.delta` | −0,002 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1991.anios` | 18 | Años de historial, timesfm, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1991.rmse` | 0,805 | RMSE (°C) llr_simple, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1991.delta` | −0,019 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1991.anios` | 18 | Años de historial, llr_simple, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1991.rmse` | 0,796 | RMSE (°C) llr_rezagos, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1991.delta` | −0,021 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1991.anios` | 18 | Años de historial, llr_rezagos, inicio 1991, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1996.rmse` | 0,767 | RMSE (°C) timesfm, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1996.delta` | −0,003 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i1996.anios` | 13 | Años de historial, timesfm, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1996.rmse` | 0,807 | RMSE (°C) llr_simple, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1996.delta` | −0,017 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i1996.anios` | 13 | Años de historial, llr_simple, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1996.rmse` | 0,798 | RMSE (°C) llr_rezagos, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1996.delta` | −0,019 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i1996.anios` | 13 | Años de historial, llr_rezagos, inicio 1996, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i2002.rmse` | 0,773 | RMSE (°C) timesfm, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i2002.delta` | +0,002 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm.i2002.anios` | 7 | Años de historial, timesfm, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i2002.rmse` | 0,815 | RMSE (°C) llr_simple, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i2002.delta` | −0,009 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_simple.i2002.anios` | 7 | Años de historial, llr_simple, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i2002.rmse` | 0,808 | RMSE (°C) llr_rezagos, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i2002.delta` | −0,009 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.llr_rezagos.i2002.anios` | 7 | Años de historial, llr_rezagos, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm_clim_propia.i2002.rmse` | 0,817 | RMSE (°C) timesfm_clim_propia, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm_clim_propia.i2002.delta` | +0,046 | Cambio de RMSE (°C) frente a inicio 1981, timesfm_clim_propia, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.timesfm_clim_propia.i2002.anios` | 7 | Años de historial, timesfm_clim_propia, inicio 2002, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.tuned.i1981.rmse` | 0,848 | RMSE (°C) tuned, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.tuned.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, tuned, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.tuned.i1981.anios` | 28 | Años de historial, tuned, inicio 1981, `ll4b` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.clim.i1981.rmse` | 1,284 | RMSE (°C) clim, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.clim.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, clim, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.clim.i1981.anios` | 32 | Años de historial, clim, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1981.rmse` | 0,839 | RMSE (°C) timesfm, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1981.anios` | 32 | Años de historial, timesfm, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1981.rmse` | 0,906 | RMSE (°C) llr_simple, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1981.anios` | 32 | Años de historial, llr_simple, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1981.rmse` | 0,894 | RMSE (°C) llr_rezagos, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1981.anios` | 32 | Años de historial, llr_rezagos, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1986.rmse` | 0,841 | RMSE (°C) timesfm, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1986.delta` | +0,002 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1986.anios` | 27 | Años de historial, timesfm, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1986.rmse` | 0,900 | RMSE (°C) llr_simple, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1986.delta` | −0,006 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1986.anios` | 27 | Años de historial, llr_simple, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1986.rmse` | 0,886 | RMSE (°C) llr_rezagos, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1986.delta` | −0,008 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1986.anios` | 27 | Años de historial, llr_rezagos, inicio 1986, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1991.rmse` | 0,840 | RMSE (°C) timesfm, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1991.delta` | +0,001 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1991.anios` | 22 | Años de historial, timesfm, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1991.rmse` | 0,887 | RMSE (°C) llr_simple, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1991.delta` | −0,019 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1991.anios` | 22 | Años de historial, llr_simple, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1991.rmse` | 0,873 | RMSE (°C) llr_rezagos, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1991.delta` | −0,021 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1991.anios` | 22 | Años de historial, llr_rezagos, inicio 1991, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1996.rmse` | 0,840 | RMSE (°C) timesfm, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1996.delta` | +0,001 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i1996.anios` | 17 | Años de historial, timesfm, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1996.rmse` | 0,886 | RMSE (°C) llr_simple, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1996.delta` | −0,020 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i1996.anios` | 17 | Años de historial, llr_simple, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1996.rmse` | 0,871 | RMSE (°C) llr_rezagos, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1996.delta` | −0,024 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i1996.anios` | 17 | Años de historial, llr_rezagos, inicio 1996, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i2002.rmse` | 0,844 | RMSE (°C) timesfm, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i2002.delta` | +0,005 | Cambio de RMSE (°C) frente a inicio 1981, timesfm, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm.i2002.anios` | 11 | Años de historial, timesfm, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i2002.rmse` | 0,893 | RMSE (°C) llr_simple, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i2002.delta` | −0,013 | Cambio de RMSE (°C) frente a inicio 1981, llr_simple, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_simple.i2002.anios` | 11 | Años de historial, llr_simple, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i2002.rmse` | 0,877 | RMSE (°C) llr_rezagos, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i2002.delta` | −0,017 | Cambio de RMSE (°C) frente a inicio 1981, llr_rezagos, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.llr_rezagos.i2002.anios` | 11 | Años de historial, llr_rezagos, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm_clim_propia.i2002.rmse` | 0,866 | RMSE (°C) timesfm_clim_propia, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm_clim_propia.i2002.delta` | +0,028 | Cambio de RMSE (°C) frente a inicio 1981, timesfm_clim_propia, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.timesfm_clim_propia.i2002.anios` | 11 | Años de historial, timesfm_clim_propia, inicio 2002, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.tuned.i1981.rmse` | 0,933 | RMSE (°C) tuned, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.tuned.i1981.delta` | 0,000 | Cambio de RMSE (°C) frente a inicio 1981, tuned, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4.tuned.i1981.anios` | 32 | Años de historial, tuned, inicio 1981, `ll4` (panel de cribado, 1.092 celdas) |
| `escalera.ll4b.costo_recortar_clim` | +0,044 | Costo (°C) de recortar además la climatología desde 2002, `ll4b` |
| `escalera.ll4.costo_recortar_clim` | +0,022 | Costo (°C) de recortar además la climatología desde 2002, `ll4` |

## escalera_brecha

| clave | valor | significado |
|---|---|---|
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_timesfm_1981.v` | −0,0004 | Brecha RMSE (°C) timesfm@1986 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_timesfm_1981.lo` | −0,002 | IC inferior timesfm@1986 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_timesfm_1981.hi` | +0,001 | IC superior timesfm@1986 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_timesfm_1981.ic` | [−0,002; +0,001] | IC 95 % timesfm@1986 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1981.v` | −0,002 | Brecha RMSE (°C) timesfm@1991 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1981.lo` | −0,004 | IC inferior timesfm@1991 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1981.hi` | +0,0003 | IC superior timesfm@1991 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1981.ic` | [−0,004; +0,0003] | IC 95 % timesfm@1991 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1981.v` | −0,003 | Brecha RMSE (°C) timesfm@1996 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1981.lo` | −0,009 | IC inferior timesfm@1996 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1981.hi` | +0,002 | IC superior timesfm@1996 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1981.ic` | [−0,009; +0,002] | IC 95 % timesfm@1996 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1981.v` | +0,002 | Brecha RMSE (°C) timesfm@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1981.lo` | −0,005 | IC inferior timesfm@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1981.hi` | +0,009 | IC superior timesfm@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1981.ic` | [−0,005; +0,009] | IC 95 % timesfm@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1986.v` | −0,002 | Brecha RMSE (°C) timesfm@1991 − timesfm@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1986.lo` | −0,004 | IC inferior timesfm@1991 − timesfm@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1986.hi` | +0,001 | IC superior timesfm@1991 − timesfm@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_timesfm_1986.ic` | [−0,004; +0,001] | IC 95 % timesfm@1991 − timesfm@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1991.v` | −0,001 | Brecha RMSE (°C) timesfm@1996 − timesfm@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1991.lo` | −0,005 | IC inferior timesfm@1996 − timesfm@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1991.hi` | +0,002 | IC superior timesfm@1996 − timesfm@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_timesfm_1991.ic` | [−0,005; +0,002] | IC 95 % timesfm@1996 − timesfm@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1996.v` | +0,005 | Brecha RMSE (°C) timesfm@2002 − timesfm@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1996.lo` | +0,002 | IC inferior timesfm@2002 − timesfm@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1996.hi` | +0,008 | IC superior timesfm@2002 − timesfm@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_timesfm_1996.ic` | [+0,002; +0,008] | IC 95 % timesfm@2002 − timesfm@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1986_vs_llr_simple_1981.v` | −0,009 | Brecha RMSE (°C) llr_simple@1986 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1986_vs_llr_simple_1981.lo` | −0,013 | IC inferior llr_simple@1986 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1986_vs_llr_simple_1981.hi` | −0,006 | IC superior llr_simple@1986 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1986_vs_llr_simple_1981.ic` | [−0,013; −0,006] | IC 95 % llr_simple@1986 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1981.v` | −0,019 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1981.lo` | −0,027 | IC inferior llr_simple@1991 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1981.hi` | −0,009 | IC superior llr_simple@1991 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1981.ic` | [−0,027; −0,009] | IC 95 % llr_simple@1991 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1981.v` | −0,017 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1981.lo` | −0,026 | IC inferior llr_simple@1996 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1981.hi` | −0,007 | IC superior llr_simple@1996 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1981.ic` | [−0,026; −0,007] | IC 95 % llr_simple@1996 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1981.v` | −0,009 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1981.lo` | −0,021 | IC inferior llr_simple@2002 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1981.hi` | +0,004 | IC superior llr_simple@2002 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1981.ic` | [−0,021; +0,004] | IC 95 % llr_simple@2002 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1986.v` | −0,009 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1986.lo` | −0,016 | IC inferior llr_simple@1991 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1986.hi` | −0,003 | IC superior llr_simple@1991 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1991_vs_llr_simple_1986.ic` | [−0,016; −0,003] | IC 95 % llr_simple@1991 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1991.v` | +0,002 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1991.lo` | −0,001 | IC inferior llr_simple@1996 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1991.hi` | +0,005 | IC superior llr_simple@1996 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_1996_vs_llr_simple_1991.ic` | [−0,001; +0,005] | IC 95 % llr_simple@1996 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1996.v` | +0,008 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1996.lo` | +0,002 | IC inferior llr_simple@2002 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1996.hi` | +0,014 | IC superior llr_simple@2002 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_simple_2002_vs_llr_simple_1996.ic` | [+0,002; +0,014] | IC 95 % llr_simple@2002 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.v` | −0,011 | Brecha RMSE (°C) llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.lo` | −0,015 | IC inferior llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.hi` | −0,008 | IC superior llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.ic` | [−0,015; −0,008] | IC 95 % llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.v` | −0,021 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.lo` | −0,030 | IC inferior llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.hi` | −0,012 | IC superior llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.ic` | [−0,030; −0,012] | IC 95 % llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.v` | −0,019 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.lo` | −0,028 | IC inferior llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.hi` | −0,009 | IC superior llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.ic` | [−0,028; −0,009] | IC 95 % llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.v` | −0,009 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.lo` | −0,021 | IC inferior llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.hi` | +0,003 | IC superior llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.ic` | [−0,021; +0,003] | IC 95 % llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.v` | −0,010 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.lo` | −0,017 | IC inferior llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.hi` | −0,004 | IC superior llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.ic` | [−0,017; −0,004] | IC 95 % llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.v` | +0,003 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.lo` | −0,0004 | IC inferior llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.hi` | +0,005 | IC superior llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.ic` | [−0,0004; +0,005] | IC 95 % llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.v` | +0,010 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.lo` | +0,004 | IC inferior llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.hi` | +0,015 | IC superior llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.ic` | [+0,004; +0,015] | IC 95 % llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_rezagos_1981.v` | −0,047 | Brecha RMSE (°C) timesfm@1981 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_rezagos_1981.lo` | −0,060 | IC inferior timesfm@1981 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_rezagos_1981.hi` | −0,034 | IC superior timesfm@1981 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_rezagos_1981.ic` | [−0,060; −0,034] | IC 95 % timesfm@1981 − llr_rezagos@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_simple_1981.v` | −0,053 | Brecha RMSE (°C) timesfm@1981 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_simple_1981.lo` | −0,066 | IC inferior timesfm@1981 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_simple_1981.hi` | −0,040 | IC superior timesfm@1981 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1981_vs_llr_simple_1981.ic` | [−0,066; −0,040] | IC 95 % timesfm@1981 − llr_simple@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_rezagos_1986.v` | −0,036 | Brecha RMSE (°C) timesfm@1986 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_rezagos_1986.lo` | −0,046 | IC inferior timesfm@1986 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_rezagos_1986.hi` | −0,027 | IC superior timesfm@1986 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_rezagos_1986.ic` | [−0,046; −0,027] | IC 95 % timesfm@1986 − llr_rezagos@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_simple_1986.v` | −0,044 | Brecha RMSE (°C) timesfm@1986 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_simple_1986.lo` | −0,054 | IC inferior timesfm@1986 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_simple_1986.hi` | −0,034 | IC superior timesfm@1986 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1986_vs_llr_simple_1986.ic` | [−0,054; −0,034] | IC 95 % timesfm@1986 − llr_simple@1986, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_rezagos_1991.v` | −0,027 | Brecha RMSE (°C) timesfm@1991 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_rezagos_1991.lo` | −0,034 | IC inferior timesfm@1991 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_rezagos_1991.hi` | −0,020 | IC superior timesfm@1991 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_rezagos_1991.ic` | [−0,034; −0,020] | IC 95 % timesfm@1991 − llr_rezagos@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_simple_1991.v` | −0,036 | Brecha RMSE (°C) timesfm@1991 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_simple_1991.lo` | −0,043 | IC inferior timesfm@1991 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_simple_1991.hi` | −0,029 | IC superior timesfm@1991 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1991_vs_llr_simple_1991.ic` | [−0,043; −0,029] | IC 95 % timesfm@1991 − llr_simple@1991, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_rezagos_1996.v` | −0,031 | Brecha RMSE (°C) timesfm@1996 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_rezagos_1996.lo` | −0,040 | IC inferior timesfm@1996 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_rezagos_1996.hi` | −0,022 | IC superior timesfm@1996 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_rezagos_1996.ic` | [−0,040; −0,022] | IC 95 % timesfm@1996 − llr_rezagos@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_simple_1996.v` | −0,039 | Brecha RMSE (°C) timesfm@1996 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_simple_1996.lo` | −0,048 | IC inferior timesfm@1996 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_simple_1996.hi` | −0,031 | IC superior timesfm@1996 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_1996_vs_llr_simple_1996.ic` | [−0,048; −0,031] | IC 95 % timesfm@1996 − llr_simple@1996, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_rezagos_2002.v` | −0,035 | Brecha RMSE (°C) timesfm@2002 − llr_rezagos@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_rezagos_2002.lo` | −0,044 | IC inferior timesfm@2002 − llr_rezagos@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_rezagos_2002.hi` | −0,026 | IC superior timesfm@2002 − llr_rezagos@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_rezagos_2002.ic` | [−0,044; −0,026] | IC 95 % timesfm@2002 − llr_rezagos@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_simple_2002.v` | −0,042 | Brecha RMSE (°C) timesfm@2002 − llr_simple@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_simple_2002.lo` | −0,051 | IC inferior timesfm@2002 − llr_simple@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_simple_2002.hi` | −0,033 | IC superior timesfm@2002 − llr_simple@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_2002_vs_llr_simple_2002.ic` | [−0,051; −0,033] | IC 95 % timesfm@2002 − llr_simple@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.v` | +0,044 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.lo` | +0,035 | IC inferior timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.hi` | +0,053 | IC superior timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.ic` | [+0,035; +0,053] | IC 95 % timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.v` | +0,046 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.lo` | +0,035 | IC inferior timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.hi` | +0,057 | IC superior timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.ic` | [+0,035; +0,057] | IC 95 % timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, mes_anio |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_timesfm_1981.v` | −0,0004 | Brecha RMSE (°C) timesfm@1986 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_timesfm_1981.lo` | −0,002 | IC inferior timesfm@1986 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_timesfm_1981.hi` | +0,001 | IC superior timesfm@1986 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_timesfm_1981.ic` | [−0,002; +0,001] | IC 95 % timesfm@1986 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1981.v` | −0,002 | Brecha RMSE (°C) timesfm@1991 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1981.lo` | −0,004 | IC inferior timesfm@1991 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1981.hi` | −0,001 | IC superior timesfm@1991 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1981.ic` | [−0,004; −0,001] | IC 95 % timesfm@1991 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1981.v` | −0,003 | Brecha RMSE (°C) timesfm@1996 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1981.lo` | −0,006 | IC inferior timesfm@1996 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1981.hi` | −0,001 | IC superior timesfm@1996 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1981.ic` | [−0,006; −0,001] | IC 95 % timesfm@1996 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1981.v` | +0,002 | Brecha RMSE (°C) timesfm@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1981.lo` | −0,002 | IC inferior timesfm@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1981.hi` | +0,007 | IC superior timesfm@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1981.ic` | [−0,002; +0,007] | IC 95 % timesfm@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1986.v` | −0,002 | Brecha RMSE (°C) timesfm@1991 − timesfm@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1986.lo` | −0,003 | IC inferior timesfm@1991 − timesfm@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1986.hi` | −0,0004 | IC superior timesfm@1991 − timesfm@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_timesfm_1986.ic` | [−0,003; −0,0004] | IC 95 % timesfm@1991 − timesfm@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1991.v` | −0,001 | Brecha RMSE (°C) timesfm@1996 − timesfm@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1991.lo` | −0,003 | IC inferior timesfm@1996 − timesfm@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1991.hi` | +0,001 | IC superior timesfm@1996 − timesfm@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_timesfm_1991.ic` | [−0,003; +0,001] | IC 95 % timesfm@1996 − timesfm@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1996.v` | +0,005 | Brecha RMSE (°C) timesfm@2002 − timesfm@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1996.lo` | +0,002 | IC inferior timesfm@2002 − timesfm@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1996.hi` | +0,009 | IC superior timesfm@2002 − timesfm@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_timesfm_1996.ic` | [+0,002; +0,009] | IC 95 % timesfm@2002 − timesfm@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1986_vs_llr_simple_1981.v` | −0,009 | Brecha RMSE (°C) llr_simple@1986 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1986_vs_llr_simple_1981.lo` | −0,013 | IC inferior llr_simple@1986 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1986_vs_llr_simple_1981.hi` | −0,006 | IC superior llr_simple@1986 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1986_vs_llr_simple_1981.ic` | [−0,013; −0,006] | IC 95 % llr_simple@1986 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1981.v` | −0,019 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1981.lo` | −0,026 | IC inferior llr_simple@1991 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1981.hi` | −0,011 | IC superior llr_simple@1991 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1981.ic` | [−0,026; −0,011] | IC 95 % llr_simple@1991 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1981.v` | −0,017 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1981.lo` | −0,025 | IC inferior llr_simple@1996 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1981.hi` | −0,008 | IC superior llr_simple@1996 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1981.ic` | [−0,025; −0,008] | IC 95 % llr_simple@1996 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1981.v` | −0,009 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1981.lo` | −0,018 | IC inferior llr_simple@2002 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1981.hi` | +0,001 | IC superior llr_simple@2002 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1981.ic` | [−0,018; +0,001] | IC 95 % llr_simple@2002 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1986.v` | −0,009 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1986.lo` | −0,013 | IC inferior llr_simple@1991 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1986.hi` | −0,006 | IC superior llr_simple@1991 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1991_vs_llr_simple_1986.ic` | [−0,013; −0,006] | IC 95 % llr_simple@1991 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1991.v` | +0,002 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1991.lo` | +0,0004 | IC inferior llr_simple@1996 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1991.hi` | +0,004 | IC superior llr_simple@1996 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_1996_vs_llr_simple_1991.ic` | [+0,0004; +0,004] | IC 95 % llr_simple@1996 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1996.v` | +0,008 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1996.lo` | +0,005 | IC inferior llr_simple@2002 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1996.hi` | +0,010 | IC superior llr_simple@2002 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_simple_2002_vs_llr_simple_1996.ic` | [+0,005; +0,010] | IC 95 % llr_simple@2002 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.v` | −0,011 | Brecha RMSE (°C) llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.lo` | −0,015 | IC inferior llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.hi` | −0,007 | IC superior llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.ic` | [−0,015; −0,007] | IC 95 % llr_rezagos@1986 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.v` | −0,021 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.lo` | −0,030 | IC inferior llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.hi` | −0,013 | IC superior llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.ic` | [−0,030; −0,013] | IC 95 % llr_rezagos@1991 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.v` | −0,019 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.lo` | −0,029 | IC inferior llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.hi` | −0,008 | IC superior llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.ic` | [−0,029; −0,008] | IC 95 % llr_rezagos@1996 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.v` | −0,009 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.lo` | −0,020 | IC inferior llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.hi` | +0,001 | IC superior llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.ic` | [−0,020; +0,001] | IC 95 % llr_rezagos@2002 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.v` | −0,010 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.lo` | −0,015 | IC inferior llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.hi` | −0,006 | IC superior llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.ic` | [−0,015; −0,006] | IC 95 % llr_rezagos@1991 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.v` | +0,003 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.lo` | +0,001 | IC inferior llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.hi` | +0,004 | IC superior llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.ic` | [+0,001; +0,004] | IC 95 % llr_rezagos@1996 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.v` | +0,010 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.lo` | +0,007 | IC inferior llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.hi` | +0,012 | IC superior llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.ic` | [+0,007; +0,012] | IC 95 % llr_rezagos@2002 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.v` | −0,047 | Brecha RMSE (°C) timesfm@1981 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.lo` | −0,057 | IC inferior timesfm@1981 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.hi` | −0,036 | IC superior timesfm@1981 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.ic` | [−0,057; −0,036] | IC 95 % timesfm@1981 − llr_rezagos@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_simple_1981.v` | −0,053 | Brecha RMSE (°C) timesfm@1981 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_simple_1981.lo` | −0,060 | IC inferior timesfm@1981 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_simple_1981.hi` | −0,045 | IC superior timesfm@1981 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1981_vs_llr_simple_1981.ic` | [−0,060; −0,045] | IC 95 % timesfm@1981 − llr_simple@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.v` | −0,036 | Brecha RMSE (°C) timesfm@1986 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.lo` | −0,042 | IC inferior timesfm@1986 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.hi` | −0,030 | IC superior timesfm@1986 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.ic` | [−0,042; −0,030] | IC 95 % timesfm@1986 − llr_rezagos@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_simple_1986.v` | −0,044 | Brecha RMSE (°C) timesfm@1986 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_simple_1986.lo` | −0,049 | IC inferior timesfm@1986 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_simple_1986.hi` | −0,039 | IC superior timesfm@1986 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1986_vs_llr_simple_1986.ic` | [−0,049; −0,039] | IC 95 % timesfm@1986 − llr_simple@1986, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.v` | −0,027 | Brecha RMSE (°C) timesfm@1991 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.lo` | −0,031 | IC inferior timesfm@1991 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.hi` | −0,024 | IC superior timesfm@1991 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.ic` | [−0,031; −0,024] | IC 95 % timesfm@1991 − llr_rezagos@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_simple_1991.v` | −0,036 | Brecha RMSE (°C) timesfm@1991 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_simple_1991.lo` | −0,041 | IC inferior timesfm@1991 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_simple_1991.hi` | −0,031 | IC superior timesfm@1991 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1991_vs_llr_simple_1991.ic` | [−0,041; −0,031] | IC 95 % timesfm@1991 − llr_simple@1991, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.v` | −0,031 | Brecha RMSE (°C) timesfm@1996 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.lo` | −0,035 | IC inferior timesfm@1996 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.hi` | −0,027 | IC superior timesfm@1996 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.ic` | [−0,035; −0,027] | IC 95 % timesfm@1996 − llr_rezagos@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_simple_1996.v` | −0,039 | Brecha RMSE (°C) timesfm@1996 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_simple_1996.lo` | −0,044 | IC inferior timesfm@1996 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_simple_1996.hi` | −0,035 | IC superior timesfm@1996 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_1996_vs_llr_simple_1996.ic` | [−0,044; −0,035] | IC 95 % timesfm@1996 − llr_simple@1996, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.v` | −0,035 | Brecha RMSE (°C) timesfm@2002 − llr_rezagos@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.lo` | −0,040 | IC inferior timesfm@2002 − llr_rezagos@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.hi` | −0,031 | IC superior timesfm@2002 − llr_rezagos@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.ic` | [−0,040; −0,031] | IC 95 % timesfm@2002 − llr_rezagos@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_simple_2002.v` | −0,042 | Brecha RMSE (°C) timesfm@2002 − llr_simple@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_simple_2002.lo` | −0,048 | IC inferior timesfm@2002 − llr_simple@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_simple_2002.hi` | −0,035 | IC superior timesfm@2002 − llr_simple@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_2002_vs_llr_simple_2002.ic` | [−0,048; −0,035] | IC 95 % timesfm@2002 − llr_simple@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.v` | +0,044 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.lo` | +0,041 | IC inferior timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.hi` | +0,048 | IC superior timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.ic` | [+0,041; +0,048] | IC 95 % timesfm_clim_propia@2002 − timesfm@2002, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.v` | +0,046 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.lo` | +0,040 | IC inferior timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.hi` | +0,053 | IC superior timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4b.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.ic` | [+0,040; +0,053] | IC 95 % timesfm_clim_propia@2002 − timesfm@1981, `ll4b`, espacial_2g |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_timesfm_1981.v` | +0,002 | Brecha RMSE (°C) timesfm@1986 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_timesfm_1981.lo` | +0,001 | IC inferior timesfm@1986 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_timesfm_1981.hi` | +0,004 | IC superior timesfm@1986 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_timesfm_1981.ic` | [+0,001; +0,004] | IC 95 % timesfm@1986 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1981.v` | +0,001 | Brecha RMSE (°C) timesfm@1991 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1981.lo` | −0,001 | IC inferior timesfm@1991 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1981.hi` | +0,003 | IC superior timesfm@1991 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1981.ic` | [−0,001; +0,003] | IC 95 % timesfm@1991 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1981.v` | +0,001 | Brecha RMSE (°C) timesfm@1996 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1981.lo` | −0,001 | IC inferior timesfm@1996 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1981.hi` | +0,004 | IC superior timesfm@1996 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1981.ic` | [−0,001; +0,004] | IC 95 % timesfm@1996 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1981.v` | +0,005 | Brecha RMSE (°C) timesfm@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1981.lo` | +0,002 | IC inferior timesfm@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1981.hi` | +0,008 | IC superior timesfm@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1981.ic` | [+0,002; +0,008] | IC 95 % timesfm@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1986.v` | −0,001 | Brecha RMSE (°C) timesfm@1991 − timesfm@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1986.lo` | −0,003 | IC inferior timesfm@1991 − timesfm@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1986.hi` | +0,001 | IC superior timesfm@1991 − timesfm@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_timesfm_1986.ic` | [−0,003; +0,001] | IC 95 % timesfm@1991 − timesfm@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1991.v` | +0,0002 | Brecha RMSE (°C) timesfm@1996 − timesfm@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1991.lo` | −0,002 | IC inferior timesfm@1996 − timesfm@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1991.hi` | +0,003 | IC superior timesfm@1996 − timesfm@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_timesfm_1991.ic` | [−0,002; +0,003] | IC 95 % timesfm@1996 − timesfm@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1996.v` | +0,004 | Brecha RMSE (°C) timesfm@2002 − timesfm@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1996.lo` | +0,001 | IC inferior timesfm@2002 − timesfm@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1996.hi` | +0,007 | IC superior timesfm@2002 − timesfm@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_timesfm_1996.ic` | [+0,001; +0,007] | IC 95 % timesfm@2002 − timesfm@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1986_vs_llr_simple_1981.v` | −0,006 | Brecha RMSE (°C) llr_simple@1986 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1986_vs_llr_simple_1981.lo` | −0,010 | IC inferior llr_simple@1986 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1986_vs_llr_simple_1981.hi` | −0,003 | IC superior llr_simple@1986 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1986_vs_llr_simple_1981.ic` | [−0,010; −0,003] | IC 95 % llr_simple@1986 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1981.v` | −0,019 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1981.lo` | −0,027 | IC inferior llr_simple@1991 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1981.hi` | −0,010 | IC superior llr_simple@1991 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1981.ic` | [−0,027; −0,010] | IC 95 % llr_simple@1991 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1981.v` | −0,020 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1981.lo` | −0,029 | IC inferior llr_simple@1996 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1981.hi` | −0,010 | IC superior llr_simple@1996 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1981.ic` | [−0,029; −0,010] | IC 95 % llr_simple@1996 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1981.v` | −0,013 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1981.lo` | −0,023 | IC inferior llr_simple@2002 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1981.hi` | −0,003 | IC superior llr_simple@2002 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1981.ic` | [−0,023; −0,003] | IC 95 % llr_simple@2002 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1986.v` | −0,012 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1986.lo` | −0,018 | IC inferior llr_simple@1991 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1986.hi` | −0,006 | IC superior llr_simple@1991 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1991_vs_llr_simple_1986.ic` | [−0,018; −0,006] | IC 95 % llr_simple@1991 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1991.v` | −0,001 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1991.lo` | −0,004 | IC inferior llr_simple@1996 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1991.hi` | +0,001 | IC superior llr_simple@1996 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_1996_vs_llr_simple_1991.ic` | [−0,004; +0,001] | IC 95 % llr_simple@1996 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1996.v` | +0,007 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1996.lo` | +0,003 | IC inferior llr_simple@2002 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1996.hi` | +0,011 | IC superior llr_simple@2002 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_simple_2002_vs_llr_simple_1996.ic` | [+0,003; +0,011] | IC 95 % llr_simple@2002 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.v` | −0,008 | Brecha RMSE (°C) llr_rezagos@1986 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.lo` | −0,012 | IC inferior llr_rezagos@1986 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.hi` | −0,005 | IC superior llr_rezagos@1986 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1986_vs_llr_rezagos_1981.ic` | [−0,012; −0,005] | IC 95 % llr_rezagos@1986 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.v` | −0,021 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.lo` | −0,029 | IC inferior llr_rezagos@1991 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.hi` | −0,013 | IC superior llr_rezagos@1991 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1981.ic` | [−0,029; −0,013] | IC 95 % llr_rezagos@1991 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.v` | −0,024 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.lo` | −0,032 | IC inferior llr_rezagos@1996 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.hi` | −0,014 | IC superior llr_rezagos@1996 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1981.ic` | [−0,032; −0,014] | IC 95 % llr_rezagos@1996 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.v` | −0,017 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.lo` | −0,026 | IC inferior llr_rezagos@2002 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.hi` | −0,008 | IC superior llr_rezagos@2002 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1981.ic` | [−0,026; −0,008] | IC 95 % llr_rezagos@2002 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.v` | −0,013 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.lo` | −0,018 | IC inferior llr_rezagos@1991 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.hi` | −0,007 | IC superior llr_rezagos@1991 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1991_vs_llr_rezagos_1986.ic` | [−0,018; −0,007] | IC 95 % llr_rezagos@1991 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.v` | −0,002 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.lo` | −0,005 | IC inferior llr_rezagos@1996 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.hi` | +0,0005 | IC superior llr_rezagos@1996 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_1996_vs_llr_rezagos_1991.ic` | [−0,005; +0,0005] | IC 95 % llr_rezagos@1996 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.v` | +0,007 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.lo` | +0,003 | IC inferior llr_rezagos@2002 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.hi` | +0,011 | IC superior llr_rezagos@2002 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.llr_rezagos_2002_vs_llr_rezagos_1996.ic` | [+0,003; +0,011] | IC 95 % llr_rezagos@2002 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_rezagos_1981.v` | −0,055 | Brecha RMSE (°C) timesfm@1981 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_rezagos_1981.lo` | −0,067 | IC inferior timesfm@1981 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_rezagos_1981.hi` | −0,043 | IC superior timesfm@1981 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_rezagos_1981.ic` | [−0,067; −0,043] | IC 95 % timesfm@1981 − llr_rezagos@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_simple_1981.v` | −0,067 | Brecha RMSE (°C) timesfm@1981 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_simple_1981.lo` | −0,080 | IC inferior timesfm@1981 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_simple_1981.hi` | −0,054 | IC superior timesfm@1981 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1981_vs_llr_simple_1981.ic` | [−0,080; −0,054] | IC 95 % timesfm@1981 − llr_simple@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_rezagos_1986.v` | −0,045 | Brecha RMSE (°C) timesfm@1986 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_rezagos_1986.lo` | −0,055 | IC inferior timesfm@1986 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_rezagos_1986.hi` | −0,034 | IC superior timesfm@1986 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_rezagos_1986.ic` | [−0,055; −0,034] | IC 95 % timesfm@1986 − llr_rezagos@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_simple_1986.v` | −0,058 | Brecha RMSE (°C) timesfm@1986 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_simple_1986.lo` | −0,070 | IC inferior timesfm@1986 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_simple_1986.hi` | −0,047 | IC superior timesfm@1986 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1986_vs_llr_simple_1986.ic` | [−0,070; −0,047] | IC 95 % timesfm@1986 − llr_simple@1986, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_rezagos_1991.v` | −0,033 | Brecha RMSE (°C) timesfm@1991 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_rezagos_1991.lo` | −0,041 | IC inferior timesfm@1991 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_rezagos_1991.hi` | −0,026 | IC superior timesfm@1991 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_rezagos_1991.ic` | [−0,041; −0,026] | IC 95 % timesfm@1991 − llr_rezagos@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_simple_1991.v` | −0,047 | Brecha RMSE (°C) timesfm@1991 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_simple_1991.lo` | −0,057 | IC inferior timesfm@1991 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_simple_1991.hi` | −0,039 | IC superior timesfm@1991 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1991_vs_llr_simple_1991.ic` | [−0,057; −0,039] | IC 95 % timesfm@1991 − llr_simple@1991, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_rezagos_1996.v` | −0,030 | Brecha RMSE (°C) timesfm@1996 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_rezagos_1996.lo` | −0,038 | IC inferior timesfm@1996 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_rezagos_1996.hi` | −0,024 | IC superior timesfm@1996 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_rezagos_1996.ic` | [−0,038; −0,024] | IC 95 % timesfm@1996 − llr_rezagos@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_simple_1996.v` | −0,046 | Brecha RMSE (°C) timesfm@1996 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_simple_1996.lo` | −0,054 | IC inferior timesfm@1996 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_simple_1996.hi` | −0,038 | IC superior timesfm@1996 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_1996_vs_llr_simple_1996.ic` | [−0,054; −0,038] | IC 95 % timesfm@1996 − llr_simple@1996, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_rezagos_2002.v` | −0,033 | Brecha RMSE (°C) timesfm@2002 − llr_rezagos@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_rezagos_2002.lo` | −0,043 | IC inferior timesfm@2002 − llr_rezagos@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_rezagos_2002.hi` | −0,023 | IC superior timesfm@2002 − llr_rezagos@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_rezagos_2002.ic` | [−0,043; −0,023] | IC 95 % timesfm@2002 − llr_rezagos@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_simple_2002.v` | −0,049 | Brecha RMSE (°C) timesfm@2002 − llr_simple@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_simple_2002.lo` | −0,061 | IC inferior timesfm@2002 − llr_simple@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_simple_2002.hi` | −0,037 | IC superior timesfm@2002 − llr_simple@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_2002_vs_llr_simple_2002.ic` | [−0,061; −0,037] | IC 95 % timesfm@2002 − llr_simple@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.v` | +0,022 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.lo` | +0,015 | IC inferior timesfm_clim_propia@2002 − timesfm@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.hi` | +0,029 | IC superior timesfm_clim_propia@2002 − timesfm@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_2002.ic` | [+0,015; +0,029] | IC 95 % timesfm_clim_propia@2002 − timesfm@2002, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.v` | +0,028 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.lo` | +0,018 | IC inferior timesfm_clim_propia@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.hi` | +0,036 | IC superior timesfm_clim_propia@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.mes_anio.timesfm_clim_propia_2002_vs_timesfm_1981.ic` | [+0,018; +0,036] | IC 95 % timesfm_clim_propia@2002 − timesfm@1981, `ll4`, mes_anio |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_timesfm_1981.v` | +0,002 | Brecha RMSE (°C) timesfm@1986 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_timesfm_1981.lo` | +0,001 | IC inferior timesfm@1986 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_timesfm_1981.hi` | +0,003 | IC superior timesfm@1986 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_timesfm_1981.ic` | [+0,001; +0,003] | IC 95 % timesfm@1986 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1981.v` | +0,001 | Brecha RMSE (°C) timesfm@1991 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1981.lo` | −0,0003 | IC inferior timesfm@1991 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1981.hi` | +0,003 | IC superior timesfm@1991 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1981.ic` | [−0,0003; +0,003] | IC 95 % timesfm@1991 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1981.v` | +0,001 | Brecha RMSE (°C) timesfm@1996 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1981.lo` | −0,001 | IC inferior timesfm@1996 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1981.hi` | +0,004 | IC superior timesfm@1996 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1981.ic` | [−0,001; +0,004] | IC 95 % timesfm@1996 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1981.v` | +0,005 | Brecha RMSE (°C) timesfm@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1981.lo` | +0,002 | IC inferior timesfm@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1981.hi` | +0,009 | IC superior timesfm@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1981.ic` | [+0,002; +0,009] | IC 95 % timesfm@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1986.v` | −0,001 | Brecha RMSE (°C) timesfm@1991 − timesfm@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1986.lo` | −0,002 | IC inferior timesfm@1991 − timesfm@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1986.hi` | −0,0003 | IC superior timesfm@1991 − timesfm@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_timesfm_1986.ic` | [−0,002; −0,0003] | IC 95 % timesfm@1991 − timesfm@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1991.v` | +0,0002 | Brecha RMSE (°C) timesfm@1996 − timesfm@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1991.lo` | −0,002 | IC inferior timesfm@1996 − timesfm@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1991.hi` | +0,003 | IC superior timesfm@1996 − timesfm@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_timesfm_1991.ic` | [−0,002; +0,003] | IC 95 % timesfm@1996 − timesfm@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1996.v` | +0,004 | Brecha RMSE (°C) timesfm@2002 − timesfm@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1996.lo` | +0,002 | IC inferior timesfm@2002 − timesfm@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1996.hi` | +0,006 | IC superior timesfm@2002 − timesfm@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_timesfm_1996.ic` | [+0,002; +0,006] | IC 95 % timesfm@2002 − timesfm@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1986_vs_llr_simple_1981.v` | −0,006 | Brecha RMSE (°C) llr_simple@1986 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1986_vs_llr_simple_1981.lo` | −0,010 | IC inferior llr_simple@1986 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1986_vs_llr_simple_1981.hi` | −0,002 | IC superior llr_simple@1986 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1986_vs_llr_simple_1981.ic` | [−0,010; −0,002] | IC 95 % llr_simple@1986 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1981.v` | −0,019 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1981.lo` | −0,026 | IC inferior llr_simple@1991 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1981.hi` | −0,010 | IC superior llr_simple@1991 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1981.ic` | [−0,026; −0,010] | IC 95 % llr_simple@1991 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1981.v` | −0,020 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1981.lo` | −0,028 | IC inferior llr_simple@1996 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1981.hi` | −0,010 | IC superior llr_simple@1996 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1981.ic` | [−0,028; −0,010] | IC 95 % llr_simple@1996 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1981.v` | −0,013 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1981.lo` | −0,022 | IC inferior llr_simple@2002 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1981.hi` | −0,003 | IC superior llr_simple@2002 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1981.ic` | [−0,022; −0,003] | IC 95 % llr_simple@2002 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1986.v` | −0,012 | Brecha RMSE (°C) llr_simple@1991 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1986.lo` | −0,016 | IC inferior llr_simple@1991 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1986.hi` | −0,008 | IC superior llr_simple@1991 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1991_vs_llr_simple_1986.ic` | [−0,016; −0,008] | IC 95 % llr_simple@1991 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1991.v` | −0,001 | Brecha RMSE (°C) llr_simple@1996 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1991.lo` | −0,003 | IC inferior llr_simple@1996 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1991.hi` | +0,0003 | IC superior llr_simple@1996 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_1996_vs_llr_simple_1991.ic` | [−0,003; +0,0003] | IC 95 % llr_simple@1996 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1996.v` | +0,007 | Brecha RMSE (°C) llr_simple@2002 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1996.lo` | +0,005 | IC inferior llr_simple@2002 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1996.hi` | +0,009 | IC superior llr_simple@2002 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_simple_2002_vs_llr_simple_1996.ic` | [+0,005; +0,009] | IC 95 % llr_simple@2002 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.v` | −0,008 | Brecha RMSE (°C) llr_rezagos@1986 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.lo` | −0,012 | IC inferior llr_rezagos@1986 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.hi` | −0,003 | IC superior llr_rezagos@1986 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1986_vs_llr_rezagos_1981.ic` | [−0,012; −0,003] | IC 95 % llr_rezagos@1986 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.v` | −0,021 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.lo` | −0,030 | IC inferior llr_rezagos@1991 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.hi` | −0,011 | IC superior llr_rezagos@1991 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1981.ic` | [−0,030; −0,011] | IC 95 % llr_rezagos@1991 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.v` | −0,024 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.lo` | −0,034 | IC inferior llr_rezagos@1996 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.hi` | −0,012 | IC superior llr_rezagos@1996 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1981.ic` | [−0,034; −0,012] | IC 95 % llr_rezagos@1996 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.v` | −0,017 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.lo` | −0,027 | IC inferior llr_rezagos@2002 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.hi` | −0,005 | IC superior llr_rezagos@2002 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1981.ic` | [−0,027; −0,005] | IC 95 % llr_rezagos@2002 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.v` | −0,013 | Brecha RMSE (°C) llr_rezagos@1991 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.lo` | −0,018 | IC inferior llr_rezagos@1991 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.hi` | −0,008 | IC superior llr_rezagos@1991 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1991_vs_llr_rezagos_1986.ic` | [−0,018; −0,008] | IC 95 % llr_rezagos@1991 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.v` | −0,002 | Brecha RMSE (°C) llr_rezagos@1996 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.lo` | −0,005 | IC inferior llr_rezagos@1996 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.hi` | −0,0002 | IC superior llr_rezagos@1996 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_1996_vs_llr_rezagos_1991.ic` | [−0,005; −0,0002] | IC 95 % llr_rezagos@1996 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.v` | +0,007 | Brecha RMSE (°C) llr_rezagos@2002 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.lo` | +0,004 | IC inferior llr_rezagos@2002 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.hi` | +0,009 | IC superior llr_rezagos@2002 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.llr_rezagos_2002_vs_llr_rezagos_1996.ic` | [+0,004; +0,009] | IC 95 % llr_rezagos@2002 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.v` | −0,055 | Brecha RMSE (°C) timesfm@1981 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.lo` | −0,068 | IC inferior timesfm@1981 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.hi` | −0,040 | IC superior timesfm@1981 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_rezagos_1981.ic` | [−0,068; −0,040] | IC 95 % timesfm@1981 − llr_rezagos@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_simple_1981.v` | −0,067 | Brecha RMSE (°C) timesfm@1981 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_simple_1981.lo` | −0,076 | IC inferior timesfm@1981 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_simple_1981.hi` | −0,055 | IC superior timesfm@1981 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1981_vs_llr_simple_1981.ic` | [−0,076; −0,055] | IC 95 % timesfm@1981 − llr_simple@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.v` | −0,045 | Brecha RMSE (°C) timesfm@1986 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.lo` | −0,053 | IC inferior timesfm@1986 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.hi` | −0,034 | IC superior timesfm@1986 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_rezagos_1986.ic` | [−0,053; −0,034] | IC 95 % timesfm@1986 − llr_rezagos@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_simple_1986.v` | −0,058 | Brecha RMSE (°C) timesfm@1986 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_simple_1986.lo` | −0,065 | IC inferior timesfm@1986 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_simple_1986.hi` | −0,050 | IC superior timesfm@1986 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1986_vs_llr_simple_1986.ic` | [−0,065; −0,050] | IC 95 % timesfm@1986 − llr_simple@1986, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.v` | −0,033 | Brecha RMSE (°C) timesfm@1991 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.lo` | −0,038 | IC inferior timesfm@1991 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.hi` | −0,026 | IC superior timesfm@1991 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_rezagos_1991.ic` | [−0,038; −0,026] | IC 95 % timesfm@1991 − llr_rezagos@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_simple_1991.v` | −0,047 | Brecha RMSE (°C) timesfm@1991 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_simple_1991.lo` | −0,053 | IC inferior timesfm@1991 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_simple_1991.hi` | −0,040 | IC superior timesfm@1991 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1991_vs_llr_simple_1991.ic` | [−0,053; −0,040] | IC 95 % timesfm@1991 − llr_simple@1991, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.v` | −0,030 | Brecha RMSE (°C) timesfm@1996 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.lo` | −0,036 | IC inferior timesfm@1996 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.hi` | −0,022 | IC superior timesfm@1996 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_rezagos_1996.ic` | [−0,036; −0,022] | IC 95 % timesfm@1996 − llr_rezagos@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_simple_1996.v` | −0,046 | Brecha RMSE (°C) timesfm@1996 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_simple_1996.lo` | −0,051 | IC inferior timesfm@1996 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_simple_1996.hi` | −0,039 | IC superior timesfm@1996 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_1996_vs_llr_simple_1996.ic` | [−0,051; −0,039] | IC 95 % timesfm@1996 − llr_simple@1996, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.v` | −0,033 | Brecha RMSE (°C) timesfm@2002 − llr_rezagos@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.lo` | −0,040 | IC inferior timesfm@2002 − llr_rezagos@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.hi` | −0,025 | IC superior timesfm@2002 − llr_rezagos@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_rezagos_2002.ic` | [−0,040; −0,025] | IC 95 % timesfm@2002 − llr_rezagos@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_simple_2002.v` | −0,049 | Brecha RMSE (°C) timesfm@2002 − llr_simple@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_simple_2002.lo` | −0,055 | IC inferior timesfm@2002 − llr_simple@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_simple_2002.hi` | −0,041 | IC superior timesfm@2002 − llr_simple@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_2002_vs_llr_simple_2002.ic` | [−0,055; −0,041] | IC 95 % timesfm@2002 − llr_simple@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.v` | +0,022 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.lo` | +0,020 | IC inferior timesfm_clim_propia@2002 − timesfm@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.hi` | +0,025 | IC superior timesfm_clim_propia@2002 − timesfm@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_2002.ic` | [+0,020; +0,025] | IC 95 % timesfm_clim_propia@2002 − timesfm@2002, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.v` | +0,028 | Brecha RMSE (°C) timesfm_clim_propia@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.lo` | +0,024 | IC inferior timesfm_clim_propia@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.hi` | +0,031 | IC superior timesfm_clim_propia@2002 − timesfm@1981, `ll4`, espacial_2g |
| `escalera_brecha.ll4.espacial_2g.timesfm_clim_propia_2002_vs_timesfm_1981.ic` | [+0,024; +0,031] | IC 95 % timesfm_clim_propia@2002 − timesfm@1981, `ll4`, espacial_2g |

## a3

| clave | valor | significado |
|---|---|---|
| `a3.pred_clim.rmse` | 1,284 | RMSE (°C), corrida A3 pred_clim (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.pred_clim.skill` | 0,000 | Habilidad frente a climatología, pred_clim |
| `a3.pred_clim.sesgo` | −0,166 | Sesgo (°C), pred_clim |
| `a3.pred_tuned.rmse` | 0,933 | RMSE (°C), corrida A3 pred_tuned (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.pred_tuned.skill` | +0,274 | Habilidad frente a climatología, pred_tuned |
| `a3.pred_tuned.sesgo` | +0,089 | Sesgo (°C), pred_tuned |
| `a3.real_td.rmse` | 0,872 | RMSE (°C), corrida A3 real_td (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.real_td.skill` | +0,321 | Habilidad frente a climatología, real_td |
| `a3.real_td.sesgo` | +0,124 | Sesgo (°C), real_td |
| `a3.real_anom.rmse` | 0,839 | RMSE (°C), corrida A3 real_anom (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.real_anom.skill` | +0,347 | Habilidad frente a climatología, real_anom |
| `a3.real_anom.sesgo` | +0,065 | Sesgo (°C), real_anom |
| `a3.shuf_anom_cell_s0.rmse` | 1,266 | RMSE (°C), corrida A3 shuf_anom_cell_s0 (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.shuf_anom_cell_s0.skill` | +0,014 | Habilidad frente a climatología, shuf_anom_cell_s0 |
| `a3.shuf_anom_cell_s0.sesgo` | +0,079 | Sesgo (°C), shuf_anom_cell_s0 |
| `a3.shuf_td_year_s0.rmse` | 1,508 | RMSE (°C), corrida A3 shuf_td_year_s0 (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.shuf_td_year_s0.skill` | −0,174 | Habilidad frente a climatología, shuf_td_year_s0 |
| `a3.shuf_td_year_s0.sesgo` | −0,176 | Sesgo (°C), shuf_td_year_s0 |
| `a3.shuf_anom_year_s0.rmse` | 1,509 | RMSE (°C), corrida A3 shuf_anom_year_s0 (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.shuf_anom_year_s0.skill` | −0,175 | Habilidad frente a climatología, shuf_anom_year_s0 |
| `a3.shuf_anom_year_s0.sesgo` | −0,224 | Sesgo (°C), shuf_anom_year_s0 |
| `a3.shuf_anom_year_s1.rmse` | 1,506 | RMSE (°C), corrida A3 shuf_anom_year_s1 (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.shuf_anom_year_s1.skill` | −0,173 | Habilidad frente a climatología, shuf_anom_year_s1 |
| `a3.shuf_anom_year_s1.sesgo` | −0,281 | Sesgo (°C), shuf_anom_year_s1 |
| `a3.shuf_anom_year_s2.rmse` | 1,551 | RMSE (°C), corrida A3 shuf_anom_year_s2 (`ll4`, panel de cribado; 3 decimales, como en el resto del paper) |
| `a3.shuf_anom_year_s2.skill` | −0,208 | Habilidad frente a climatología, shuf_anom_year_s2 |
| `a3.shuf_anom_year_s2.sesgo` | −0,156 | Sesgo (°C), shuf_anom_year_s2 |
| `a3.barajado_anio.rmse_min` | 1,506 | RMSE mínimo entre las corridas con Tmin barajada entre años |
| `a3.barajado_anio.rmse_max` | 1,551 | RMSE máximo entre las corridas con Tmin barajada entre años |
| `a3.barajado_anio.n_semillas` | 3 | Semillas del barajado entre años |
| `a3.barajado_anio.n_corridas` | 4 | Corridas con barajado entre años |
| `a3.barajado_anio.todas_peor_que_clim` | sí | ¿Todas las corridas con barajado entre años quedan peor que la climatología? |
| `a3.n_celdas` | 1.092 | Celdas del panel de A3 |
| `a3.n_filas` | 1.595.412 | Filas del panel de A3 |
| `a3.ll4b.rmse` | n. d. | A3 en `ll4b` (A3 solo se corrió en ll4) |

## a4

| clave | valor | significado |
|---|---|---|
| `a4.anom.palacios_2017_2020.n_dias` | 14.666 | Días-estación, anom palacios 2017-2020 |
| `a4.anom.palacios_2017_2020.n_estaciones` | 12 | Estaciones, anom palacios 2017-2020 |
| `a4.anom.palacios_2017_2020.rmse` | 1,68 | RMSE (°C), anom palacios 2017-2020 (2 decimales) |
| `a4.anom.palacios_2017_2020.sesgo` | +0,18 | Sesgo (°C), anom palacios 2017-2020 (2 decimales) |
| `a4.anom.palacios_2017_2020.mae` | 1,05 | MAE (°C), anom palacios 2017-2020 (2 decimales) |
| `a4.anom.pisco_2009_2016.n_dias` | 30.751 | Días-estación, anom pisco 2009-2016 |
| `a4.anom.pisco_2009_2016.n_estaciones` | 12 | Estaciones, anom pisco 2009-2016 |
| `a4.anom.pisco_2009_2016.rmse` | 1,33 | RMSE (°C), anom pisco 2009-2016 (2 decimales) |
| `a4.anom.pisco_2009_2016.sesgo` | +0,02 | Sesgo (°C), anom pisco 2009-2016 (2 decimales) |
| `a4.anom.pisco_2009_2016.mae` | 0,86 | MAE (°C), anom pisco 2009-2016 (2 decimales) |
| `a4.anom.timesfm_2017_2020.n_dias` | 14.666 | Días-estación, anom timesfm 2017-2020 |
| `a4.anom.timesfm_2017_2020.n_estaciones` | 12 | Estaciones, anom timesfm 2017-2020 |
| `a4.anom.timesfm_2017_2020.rmse` | 1,63 | RMSE (°C), anom timesfm 2017-2020 (2 decimales) |
| `a4.anom.timesfm_2017_2020.sesgo` | +0,29 | Sesgo (°C), anom timesfm 2017-2020 (2 decimales) |
| `a4.anom.timesfm_2017_2020.mae` | 1,02 | MAE (°C), anom timesfm 2017-2020 (2 decimales) |
| `a4.td.palacios_2017_2020.n_dias` | 14.666 | Días-estación, td palacios 2017-2020 |
| `a4.td.palacios_2017_2020.n_estaciones` | 12 | Estaciones, td palacios 2017-2020 |
| `a4.td.palacios_2017_2020.rmse` | 2,88 | RMSE (°C), td palacios 2017-2020 (2 decimales) |
| `a4.td.palacios_2017_2020.sesgo` | +1,38 | Sesgo (°C), td palacios 2017-2020 (2 decimales) |
| `a4.td.palacios_2017_2020.mae` | 1,98 | MAE (°C), td palacios 2017-2020 (2 decimales) |
| `a4.td.pisco_2009_2016.n_dias` | 31.326 | Días-estación, td pisco 2009-2016 |
| `a4.td.pisco_2009_2016.n_estaciones` | 13 | Estaciones, td pisco 2009-2016 |
| `a4.td.pisco_2009_2016.rmse` | 3,06 | RMSE (°C), td pisco 2009-2016 (2 decimales) |
| `a4.td.pisco_2009_2016.sesgo` | +1,42 | Sesgo (°C), td pisco 2009-2016 (2 decimales) |
| `a4.td.pisco_2009_2016.mae` | 2,11 | MAE (°C), td pisco 2009-2016 (2 decimales) |
| `a4.td.timesfm_2017_2020.n_dias` | 14.666 | Días-estación, td timesfm 2017-2020 |
| `a4.td.timesfm_2017_2020.n_estaciones` | 12 | Estaciones, td timesfm 2017-2020 |
| `a4.td.timesfm_2017_2020.rmse` | 2,89 | RMSE (°C), td timesfm 2017-2020 (2 decimales) |
| `a4.td.timesfm_2017_2020.sesgo` | +1,48 | Sesgo (°C), td timesfm 2017-2020 (2 decimales) |
| `a4.td.timesfm_2017_2020.mae` | 2,03 | MAE (°C), td timesfm 2017-2020 (2 decimales) |
| `a4.delta_rmse.td.timesfm_vs_palacios.v` | +0,010 | ΔRMSE (°C) timesfm − palacios, td, 2017-2020 |
| `a4.delta_rmse.td.timesfm_vs_palacios.ic` | [−0,025; +0,057] | IC 95 % del ΔRMSE |
| `a4.delta_rmse.td.timesfm_vs_palacios.excluye_cero` | no | ¿El IC excluye cero? |
| `a4.delta_rmse.td.timesfm_vs_palacios.n_estaciones` | 12 | Estaciones del bootstrap |
| `a4.delta_rmse.td.timesfm_vs_palacios.n_dias` | 14.666 | Días-estación del bootstrap |
| `a4.delta_rmse.anom.timesfm_vs_palacios.v` | −0,046 | ΔRMSE (°C) timesfm − palacios, anom, 2017-2020 |
| `a4.delta_rmse.anom.timesfm_vs_palacios.ic` | [−0,073; −0,019] | IC 95 % del ΔRMSE |
| `a4.delta_rmse.anom.timesfm_vs_palacios.excluye_cero` | sí | ¿El IC excluye cero? |
| `a4.delta_rmse.anom.timesfm_vs_palacios.n_estaciones` | 12 | Estaciones del bootstrap |
| `a4.delta_rmse.anom.timesfm_vs_palacios.n_dias` | 14.666 | Días-estación del bootstrap |
| `a4.td.pisco_2009_2016.estacion_sesgo1` | +5,91 | Sesgo de la estación con el 1.º mayor sesgo de PISCO Td (estación: RODRIGUEZ BALLON) |
| `a4.td.pisco_2009_2016.estacion_sesgo2` | +4,24 | Sesgo de la estación con el 2.º mayor sesgo de PISCO Td (estación: ANDAHUAYLAS) |
| `a4.td.pisco_2009_2016.estacion_sesgo3` | +3,97 | Sesgo de la estación con el 3.º mayor sesgo de PISCO Td (estación: TENIENTE ALEJANDRO VELASCO ASTETE INTL) |
| `a4.td.pisco_2009_2016.estacion_sesgo1_nombre` | Rodriguez Ballon | Nombre de la estación con el 1.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.estacion_sesgo1_elev` | 2.562 | Elevación (m) de la estación con el 1.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.estacion_sesgo2_nombre` | Andahuaylas | Nombre de la estación con el 2.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.estacion_sesgo2_elev` | 3.444 | Elevación (m) de la estación con el 2.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.estacion_sesgo3_nombre` | Alejandro Velasco Astete | Nombre de la estación con el 3.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.estacion_sesgo3_elev` | 3.310 | Elevación (m) de la estación con el 3.º mayor sesgo de PISCO Td |
| `a4.td.pisco_2009_2016.n_sesgo_gt2` | 4 | Estaciones con /sesgo/ > 2 °C, Td pisco 2009-2016 |
| `a4.td.pisco_2009_2016.n_estaciones_tabla` | 13 | Estaciones evaluadas, Td pisco 2009-2016 |
| `a4.td.palacios_2017_2020.n_sesgo_gt2` | 2 | Estaciones con /sesgo/ > 2 °C, Td palacios 2017-2020 |
| `a4.td.palacios_2017_2020.n_estaciones_tabla` | 12 | Estaciones evaluadas, Td palacios 2017-2020 |
| `a4.td.timesfm_2017_2020.n_sesgo_gt2` | 2 | Estaciones con /sesgo/ > 2 °C, Td timesfm 2017-2020 |
| `a4.td.timesfm_2017_2020.n_estaciones_tabla` | 12 | Estaciones evaluadas, Td timesfm 2017-2020 |
| `a4.independencia_estaciones` | n. d. | Independencia de las estaciones ISD frente a PISCO (no hay lista pública para comprobarlo (sintesis_amenazas.md §6)) |

## costo

| clave | valor | significado |
|---|---|---|
| `costo.timesfm_ll4b_inferencia.seg` | 4.389,8 | Segundos de pared, timesfm_anom ll4b prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_ll4b_inferencia.tiempo` | 73 min 10 s | Tiempo de pared legible, timesfm_anom ll4b prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_ll4b_inferencia.celdas` | 17.041 | Celdas procesadas |
| `costo.timesfm_ll4b_inferencia.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_ll4b_inferencia.celdas_por_s` | 3,88 | Celdas por segundo |
| `costo.timesfm_td_ll4b_inferencia.seg` | 4.380,6 | Segundos de pared, timesfm_td ll4b prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_td_ll4b_inferencia.tiempo` | 73 min 1 s | Tiempo de pared legible, timesfm_td ll4b prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_td_ll4b_inferencia.celdas` | 17.041 | Celdas procesadas |
| `costo.timesfm_td_ll4b_inferencia.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_td_ll4b_inferencia.celdas_por_s` | 3,89 | Celdas por segundo |
| `costo.timesfm_ll4_inferencia.seg` | 5.154,9 | Segundos de pared, timesfm_anom ll4 prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_ll4_inferencia.tiempo` | 85 min 55 s | Tiempo de pared legible, timesfm_anom ll4 prediccion (sin ajuste ni seleccion) |
| `costo.timesfm_ll4_inferencia.celdas` | 17.041 | Celdas procesadas |
| `costo.timesfm_ll4_inferencia.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_ll4_inferencia.celdas_por_s` | 3,31 | Celdas por segundo |
| `costo.timesfm_cribado.seg` | 2.948 | Segundos de pared, timesfm (9 variantes) ll4 seleccion de variante (cribado) |
| `costo.timesfm_cribado.tiempo` | 49 min 8 s | Tiempo de pared legible, timesfm (9 variantes) ll4 seleccion de variante (cribado) |
| `costo.timesfm_cribado.celdas` | 1.106 | Celdas procesadas |
| `costo.timesfm_cribado.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_ll4_escala.seg` | 85.686 | Segundos de pared, timesfm_anom ll4 prediccion pasada de escala |
| `costo.timesfm_ll4_escala.tiempo` | 23 h 48 min | Tiempo de pared legible, timesfm_anom ll4 prediccion pasada de escala |
| `costo.timesfm_ll4_escala.celdas` | 436.519 | Celdas procesadas |
| `costo.timesfm_ll4_escala.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_ll4_escala.celdas_por_s` | 5,09 | Celdas por segundo |
| `costo.timesfm_producto_inferencia.seg` | 438.074 | Segundos de pared, timesfm_anom real 2017-2020 prediccion producto completo |
| `costo.timesfm_producto_inferencia.tiempo` | ≈5,1 días | Tiempo de pared legible, timesfm_anom real 2017-2020 prediccion producto completo |
| `costo.timesfm_producto_inferencia.celdas` | 2.178.827 | Celdas procesadas |
| `costo.timesfm_producto_inferencia.hardware` | RTX A2000 12 GB | Hardware declarado |
| `costo.timesfm_producto_inferencia.celdas_por_s` | 4,97 | Celdas por segundo |
| `costo.tuned_ll4b_seleccion.seg` | 3.158 | Segundos de pared, tuned ll4b seleccion de recetas (solo anios de entrenamiento) |
| `costo.tuned_ll4b_seleccion.tiempo` | 52 min 38 s | Tiempo de pared legible, tuned ll4b seleccion de recetas (solo anios de entrenamiento) |
| `costo.tuned_ll4b_seleccion.celdas` | 5.506 | Celdas procesadas |
| `costo.tuned_ll4b_seleccion.hardware` | RTX A2000 12 GB + CPU | Hardware declarado |
| `costo.tuned_ll4b_ajuste.seg` | 350 | Segundos de pared, tuned ll4b ajuste + prediccion (backtest) |
| `costo.tuned_ll4b_ajuste.tiempo` | 5 min 50 s | Tiempo de pared legible, tuned ll4b ajuste + prediccion (backtest) |
| `costo.tuned_ll4b_ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.tuned_ll4b_ajuste.hardware` | RTX A2000 12 GB + CPU | Hardware declarado |
| `costo.tuned_ll4_seleccion.seg` | 3.194 | Segundos de pared, tuned ll4 seleccion de recetas (solo anios de entrenamiento) |
| `costo.tuned_ll4_seleccion.tiempo` | 53 min 14 s | Tiempo de pared legible, tuned ll4 seleccion de recetas (solo anios de entrenamiento) |
| `costo.tuned_ll4_seleccion.celdas` | 5.506 | Celdas procesadas |
| `costo.tuned_ll4_seleccion.hardware` | no registrado (GPU con CuPy) | Hardware declarado |
| `costo.tuned_ll4_ajuste.seg` | 402 | Segundos de pared, tuned ll4 ajuste + prediccion (backtest) |
| `costo.tuned_ll4_ajuste.tiempo` | 6 min 42 s | Tiempo de pared legible, tuned ll4 ajuste + prediccion (backtest) |
| `costo.tuned_ll4_ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.tuned_ll4_ajuste.hardware` | no registrado (GPU con CuPy) | Hardware declarado |
| `costo.tuned_prod_seleccion.seg` | 117.698 | Segundos de pared, tuned produccion 1981-2016 seleccion de recetas (grid completo) |
| `costo.tuned_prod_seleccion.tiempo` | 32 h 42 min | Tiempo de pared legible, tuned produccion 1981-2016 seleccion de recetas (grid completo) |
| `costo.tuned_prod_seleccion.celdas` | 2.818.404 | Celdas procesadas |
| `costo.tuned_prod_seleccion.hardware` | no registrado (b0_run.sh: local single-GPU) | Hardware declarado |
| `costo.tuned_prod_ajuste.seg` | 24.293 | Segundos de pared, tuned produccion 1981-2016 ajuste (grid completo) |
| `costo.tuned_prod_ajuste.tiempo` | 6 h 45 min | Tiempo de pared legible, tuned produccion 1981-2016 ajuste (grid completo) |
| `costo.tuned_prod_ajuste.celdas` | 2.818.404 | Celdas procesadas |
| `costo.tuned_prod_ajuste.hardware` | no registrado (b0_run.sh: local single-GPU) | Hardware declarado |
| `costo.tuned_producto_prediccion.seg` | 1.180 | Segundos de pared, tuned real 2017-2020 prediccion (grid completo) |
| `costo.tuned_producto_prediccion.tiempo` | 19 min 40 s | Tiempo de pared legible, tuned real 2017-2020 prediccion (grid completo) |
| `costo.tuned_producto_prediccion.celdas` | 2.178.827 | Celdas procesadas |
| `costo.tuned_producto_prediccion.hardware` | no registrado; 14 procesos | Hardware declarado |
| `costo.llr_simple_ll4b_carga.seg` | 17 | Segundos de pared, llr_simple ll4b carga de datos |
| `costo.llr_simple_ll4b_carga.tiempo` | 17 s | Tiempo de pared legible, llr_simple ll4b carga de datos |
| `costo.llr_simple_ll4b_carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_ll4b_carga.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_simple_ll4b_seleccion_h.seg` | 92 | Segundos de pared, llr_simple ll4b seleccion de h (7 valores; ultimos 4 anios de entrenamiento) |
| `costo.llr_simple_ll4b_seleccion_h.tiempo` | 1 min 32 s | Tiempo de pared legible, llr_simple ll4b seleccion de h (7 valores; ultimos 4 anios de entrenamiento) |
| `costo.llr_simple_ll4b_seleccion_h.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_ll4b_seleccion_h.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_simple_ll4b_ajuste.seg` | 19 | Segundos de pared, llr_simple ll4b ajuste final + prediccion |
| `costo.llr_simple_ll4b_ajuste.tiempo` | 19 s | Tiempo de pared legible, llr_simple ll4b ajuste final + prediccion |
| `costo.llr_simple_ll4b_ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_ll4b_ajuste.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_simple_ll4b_total.seg` | 128,1 | Segundos de pared, llr_simple ll4b total |
| `costo.llr_simple_ll4b_total.tiempo` | 2 min 8 s | Tiempo de pared legible, llr_simple ll4b total |
| `costo.llr_simple_ll4b_total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_ll4b_total.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_rezagos_ll4b_carga.seg` | 14 | Segundos de pared, llr_rezagos ll4b carga de datos |
| `costo.llr_rezagos_ll4b_carga.tiempo` | 14 s | Tiempo de pared legible, llr_rezagos ll4b carga de datos |
| `costo.llr_rezagos_ll4b_carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_ll4b_carga.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_rezagos_ll4b_seleccion_h.seg` | 403 | Segundos de pared, llr_rezagos ll4b seleccion de h (7 valores) |
| `costo.llr_rezagos_ll4b_seleccion_h.tiempo` | 6 min 43 s | Tiempo de pared legible, llr_rezagos ll4b seleccion de h (7 valores) |
| `costo.llr_rezagos_ll4b_seleccion_h.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_ll4b_seleccion_h.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_rezagos_ll4b_ajuste.seg` | 91 | Segundos de pared, llr_rezagos ll4b ajuste final + prediccion |
| `costo.llr_rezagos_ll4b_ajuste.tiempo` | 1 min 31 s | Tiempo de pared legible, llr_rezagos ll4b ajuste final + prediccion |
| `costo.llr_rezagos_ll4b_ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_ll4b_ajuste.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.llr_rezagos_ll4b_total.seg` | 508,4 | Segundos de pared, llr_rezagos ll4b total |
| `costo.llr_rezagos_ll4b_total.tiempo` | 8 min 28 s | Tiempo de pared legible, llr_rezagos ll4b total |
| `costo.llr_rezagos_ll4b_total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_ll4b_total.hardware` | 32 nucleos CPU | Hardware declarado |
| `costo.ll4b.tuned_total.seg` | 3.508 | Total `tuned` en `ll4b` (selección + ajuste y predicción) (s) |
| `costo.ll4b.tuned_total.tiempo` | 58 min 28 s | Total `tuned` en `ll4b` (selección + ajuste y predicción) (legible) |
| `costo.ll4b.timesfm_inferencia.seg` | 4.389,8 | Inferencia de TimesFM en `ll4b` (s) |
| `costo.ll4b.timesfm_inferencia.tiempo` | 73 min 10 s | Inferencia de TimesFM en `ll4b` (legible) |
| `costo.ll4b.timesfm_seleccion.seg` | 2.948 | Selección única de configuración de TimesFM (s) |
| `costo.ll4b.timesfm_seleccion.tiempo` | 49 min 8 s | Selección única de configuración de TimesFM (legible) |
| `costo.ll4b.timesfm_total.seg` | 7.337,8 | Total TimesFM en `ll4b` incluyendo la selección una vez (s) |
| `costo.ll4b.timesfm_total.tiempo` | 122 min 18 s | Total TimesFM en `ll4b` incluyendo la selección una vez (legible) |
| `costo.ll4b.ratio_total` | 2,09 | Cociente total TimesFM / total `tuned` en `ll4b` |
| `costo.ll4b.ratio_total_r` | 2 | Cociente total TimesFM / total `tuned` en `ll4b`, entero |
| `costo.ll4b.ratio_inferencia_tuned_total` | 1,25 | Cociente inferencia TimesFM / total `tuned` |
| `costo.ll4b.ratio_inferencia_ajuste` | 12,5 | Cociente inferencia TimesFM / ajuste y predicción de `tuned` |
| `costo.ll4b.ratio_inferencia_ajuste_r` | 13 | Cociente inferencia TimesFM / ajuste y predicción de `tuned`, entero |
| `costo.ll4b.celdas_timesfm_extra` | 14 | Celdas que TimesFM predice de más (panel 17.041) |
| `costo.ll4.tuned_total.seg` | 3.596 | Total `tuned` limpio de Palacios en `ll4` (s) |
| `costo.ll4.tuned_total.tiempo` | 59 min 56 s | Total `tuned` limpio de Palacios en `ll4` (legible) |
| `costo.producto.tuned_entrenamiento.seg` | 141.991 | Selección y ajuste de `tuned` (1981–2016) (s) |
| `costo.producto.tuned_entrenamiento.tiempo` | 39 h 27 min | Selección y ajuste de `tuned` (1981–2016) (legible) |
| `costo.producto.tuned_entrenamiento.horas` | 39,4 | Horas de selección y ajuste de `tuned` a escala de producto |
| `costo.producto.tuned_entrenamiento.horas_enteras` | 39 | Horas redondeadas ("unas N h") |
| `costo.producto.tuned_prediccion.seg` | 1.180 | Predicción 2017–2020 de `tuned` (s) |
| `costo.producto.tuned_prediccion.tiempo` | 19 min 40 s | Predicción 2017–2020 de `tuned` (legible) |
| `costo.producto.timesfm_inferencia.seg` | 438.074 | Inferencia 2017–2020 de TimesFM (s) |
| `costo.producto.timesfm_inferencia.tiempo` | ≈5,1 días | Inferencia 2017–2020 de TimesFM (legible) |
| `costo.producto.timesfm_inferencia.dias` | 5,1 | Días de inferencia de TimesFM a escala de producto |
| `costo.producto.timesfm_inferencia.dias_aprox` | ≈5,1 días | Días de inferencia, con símbolo ≈ |
| `costo.producto.ratio_inferencia` | 371 | Cociente de inferencia TimesFM / `tuned` a escala de producto (costo.md dice «unas 370 veces»; el cociente exacto es 371,2) |
| `costo.producto.ratio_inferencia_1d` | 371,2 | Cociente con un decimal |
| `costo.producto.tuned_total_con_prediccion.seg` | 143.171 | `tuned` a escala de producto, entrenamiento y predicción 2017–2020 (s) |
| `costo.producto.tuned_total_con_prediccion.tiempo` | 39 h 46 min | `tuned` a escala de producto, entrenamiento y predicción 2017–2020 (legible) |
| `costo.producto.celdas_por_s_timesfm` | 4,97 | Celdas por segundo de TimesFM a escala de producto |
| `costo.producto.celdas` | 2.178.827 | Celdas del producto 2017–2020 |
| `costo.tuned_sin_td.tiempo` | n. d. | Tiempo de `tuned` sin rezagos de Td (no figura en la tabla de costo) |
| `costo.horas_humanas` | n. d. | Horas-persona de diseño (no medidas) |
| `costo.preentrenamiento_timesfm` | n. d. | Costo de preentrenamiento de TimesFM (no cronometrado) |
| `costo.preprocesamiento_compartido` | n. d. | Preprocesamiento compartido (regrillado, climatologías) (sin cronometraje independiente completo) |
| `costo.host_palacios` | n. d. | Host de las corridas de Palacios (el log no registra el host) |
| `costo.hardware.estacion` | Intel Core i9-14900K (32 hilos), 125 GB de RAM, NVIDIA RTX A2000 12 GB limitada a 70 W | Estación de trabajo (CPU, RAM, GPU) |
| `costo.llr_simple_sel.ll4b.carga.seg` | 14,3 | Segundos de pared, llr_simple_sel ll4b carga |
| `costo.llr_simple_sel.ll4b.carga.tiempo` | 14 s | Tiempo de pared legible, llr_simple_sel ll4b carga |
| `costo.llr_simple_sel.ll4b.carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4b.carga.celdas_por_s` | 1.190,70 | Celdas por segundo |
| `costo.llr_simple_sel.ll4b.carga.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4b.seleccion.seg` | 77,9 | Segundos de pared, llr_simple_sel ll4b seleccion |
| `costo.llr_simple_sel.ll4b.seleccion.tiempo` | 1 min 18 s | Tiempo de pared legible, llr_simple_sel ll4b seleccion |
| `costo.llr_simple_sel.ll4b.seleccion.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4b.seleccion.celdas_por_s` | 218,58 | Celdas por segundo |
| `costo.llr_simple_sel.ll4b.seleccion.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4b.ajuste.seg` | 9,8 | Segundos de pared, llr_simple_sel ll4b ajuste |
| `costo.llr_simple_sel.ll4b.ajuste.tiempo` | 10 s | Tiempo de pared legible, llr_simple_sel ll4b ajuste |
| `costo.llr_simple_sel.ll4b.ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4b.ajuste.celdas_por_s` | 1.737,45 | Celdas por segundo |
| `costo.llr_simple_sel.ll4b.ajuste.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4b.total.seg` | 102 | Segundos de pared, llr_simple_sel ll4b total |
| `costo.llr_simple_sel.ll4b.total.tiempo` | 1 min 42 s | Tiempo de pared legible, llr_simple_sel ll4b total |
| `costo.llr_simple_sel.ll4b.total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4b.total.celdas_por_s` | 166,93 | Celdas por segundo |
| `costo.llr_simple_sel.ll4b.total.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4.carga.seg` | 14,4 | Segundos de pared, llr_simple_sel ll4 carga |
| `costo.llr_simple_sel.ll4.carga.tiempo` | 14 s | Tiempo de pared legible, llr_simple_sel ll4 carga |
| `costo.llr_simple_sel.ll4.carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4.carga.celdas_por_s` | 1.182,43 | Celdas por segundo |
| `costo.llr_simple_sel.ll4.carga.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4.seleccion.seg` | 81 | Segundos de pared, llr_simple_sel ll4 seleccion |
| `costo.llr_simple_sel.ll4.seleccion.tiempo` | 1 min 21 s | Tiempo de pared legible, llr_simple_sel ll4 seleccion |
| `costo.llr_simple_sel.ll4.seleccion.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4.seleccion.celdas_por_s` | 210,21 | Celdas por segundo |
| `costo.llr_simple_sel.ll4.seleccion.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4.ajuste.seg` | 11 | Segundos de pared, llr_simple_sel ll4 ajuste |
| `costo.llr_simple_sel.ll4.ajuste.tiempo` | 11 s | Tiempo de pared legible, llr_simple_sel ll4 ajuste |
| `costo.llr_simple_sel.ll4.ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4.ajuste.celdas_por_s` | 1.547,91 | Celdas por segundo |
| `costo.llr_simple_sel.ll4.ajuste.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.ll4.total.seg` | 106,4 | Segundos de pared, llr_simple_sel ll4 total |
| `costo.llr_simple_sel.ll4.total.tiempo` | 1 min 46 s | Tiempo de pared legible, llr_simple_sel ll4 total |
| `costo.llr_simple_sel.ll4.total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_simple_sel.ll4.total.celdas_por_s` | 160,03 | Celdas por segundo |
| `costo.llr_simple_sel.ll4.total.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_simple_sel.hardware` | Intel Core i9-14900K (32 hilos), 125 GB RAM | Hardware de la corrida |
| `costo.llr_simple_sel.gpu` | sin GPU | Uso de GPU en la corrida |
| `costo.llr_simple_sel.reproduce_max` | 0,0 | Diferencia absoluta máxima de reproducción (todas las filas) |
| `costo.llr_simple_sel.reproduce_texto` | reproduce la predicción con diferencia absoluta máxima de 0,0 | Texto de la verificación de reproducción |
| `costo.llr_simple_sel.tiempo` | 1 min 42 s | Tiempo total de `llr_simple_sel` en `ll4b` |
| `costo.llr_simple_sel.seg` | 102 | Segundos totales de `llr_simple_sel` en `ll4b` |
| `costo.llr_simple_sel.ratio_timesfm` | 71,94 | Cociente total TimesFM / `llr_simple_sel` en `ll4b` |
| `costo.llr_simple_sel.ratio_tuned` | 34,39 | Cociente total `tuned` / `llr_simple_sel` en `ll4b` |
| `costo.llr_simple_sel.ratio_timesfm_r` | 72 | Cociente total TimesFM / `llr_simple_sel` en `ll4b`, entero |
| `costo.llr_simple_sel.ratio_tuned_r` | 34 | Cociente total `tuned` / `llr_simple_sel` en `ll4b`, entero |
| `costo.llr_rezagos_sel.ll4b.carga.seg` | 14,4 | Segundos de pared, llr_rezagos_sel ll4b carga |
| `costo.llr_rezagos_sel.ll4b.carga.tiempo` | 14 s | Tiempo de pared legible, llr_rezagos_sel ll4b carga |
| `costo.llr_rezagos_sel.ll4b.carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4b.carga.celdas_por_s` | 1.182,43 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4b.carga.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4b.seleccion.seg` | 61,5 | Segundos de pared, llr_rezagos_sel ll4b seleccion |
| `costo.llr_rezagos_sel.ll4b.seleccion.tiempo` | 1 min 2 s | Tiempo de pared legible, llr_rezagos_sel ll4b seleccion |
| `costo.llr_rezagos_sel.ll4b.seleccion.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4b.seleccion.celdas_por_s` | 276,86 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4b.seleccion.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4b.ajuste.seg` | 9,7 | Segundos de pared, llr_rezagos_sel ll4b ajuste |
| `costo.llr_rezagos_sel.ll4b.ajuste.tiempo` | 10 s | Tiempo de pared legible, llr_rezagos_sel ll4b ajuste |
| `costo.llr_rezagos_sel.ll4b.ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4b.ajuste.celdas_por_s` | 1.755,36 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4b.ajuste.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4b.total.seg` | 85,6 | Segundos de pared, llr_rezagos_sel ll4b total |
| `costo.llr_rezagos_sel.ll4b.total.tiempo` | 1 min 26 s | Tiempo de pared legible, llr_rezagos_sel ll4b total |
| `costo.llr_rezagos_sel.ll4b.total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4b.total.celdas_por_s` | 198,91 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4b.total.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4.carga.seg` | 14,5 | Segundos de pared, llr_rezagos_sel ll4 carga |
| `costo.llr_rezagos_sel.ll4.carga.tiempo` | 15 s | Tiempo de pared legible, llr_rezagos_sel ll4 carga |
| `costo.llr_rezagos_sel.ll4.carga.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4.carga.celdas_por_s` | 1.174,28 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4.carga.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4.seleccion.seg` | 63,4 | Segundos de pared, llr_rezagos_sel ll4 seleccion |
| `costo.llr_rezagos_sel.ll4.seleccion.tiempo` | 1 min 3 s | Tiempo de pared legible, llr_rezagos_sel ll4 seleccion |
| `costo.llr_rezagos_sel.ll4.seleccion.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4.seleccion.celdas_por_s` | 268,56 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4.seleccion.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4.ajuste.seg` | 10,5 | Segundos de pared, llr_rezagos_sel ll4 ajuste |
| `costo.llr_rezagos_sel.ll4.ajuste.tiempo` | 11 s | Tiempo de pared legible, llr_rezagos_sel ll4 ajuste |
| `costo.llr_rezagos_sel.ll4.ajuste.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4.ajuste.celdas_por_s` | 1.621,62 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4.ajuste.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.ll4.total.seg` | 88,4 | Segundos de pared, llr_rezagos_sel ll4 total |
| `costo.llr_rezagos_sel.ll4.total.tiempo` | 1 min 28 s | Tiempo de pared legible, llr_rezagos_sel ll4 total |
| `costo.llr_rezagos_sel.ll4.total.celdas` | 17.027 | Celdas procesadas |
| `costo.llr_rezagos_sel.ll4.total.celdas_por_s` | 192,61 | Celdas por segundo |
| `costo.llr_rezagos_sel.ll4.total.reproduce` | 0,0 | Diferencia absoluta máxima al reproducir la predicción de la selección |
| `costo.llr_rezagos_sel.hardware` | Intel Core i9-14900K (32 hilos), 125 GB RAM | Hardware de la corrida |
| `costo.llr_rezagos_sel.gpu` | sin GPU | Uso de GPU en la corrida |
| `costo.llr_rezagos_sel.reproduce_max` | 0,0 | Diferencia absoluta máxima de reproducción (todas las filas) |
| `costo.llr_rezagos_sel.reproduce_texto` | reproduce la predicción con diferencia absoluta máxima de 0,0 | Texto de la verificación de reproducción |
| `costo.llr_rezagos_sel.tiempo` | 1 min 26 s | Tiempo total de `llr_rezagos_sel` en `ll4b` |
| `costo.llr_rezagos_sel.seg` | 85,6 | Segundos totales de `llr_rezagos_sel` en `ll4b` |
| `costo.llr_rezagos_sel.ratio_timesfm` | 85,72 | Cociente total TimesFM / `llr_rezagos_sel` en `ll4b` |
| `costo.llr_rezagos_sel.ratio_tuned` | 40,98 | Cociente total `tuned` / `llr_rezagos_sel` en `ll4b` |
| `costo.llr_rezagos_sel.ratio_timesfm_r` | 86 | Cociente total TimesFM / `llr_rezagos_sel` en `ll4b`, entero |
| `costo.llr_rezagos_sel.ratio_tuned_r` | 41 | Cociente total `tuned` / `llr_rezagos_sel` en `ll4b`, entero |

## a2

| clave | valor | significado |
|---|---|---|
| `a2.ll4b.panel.mejora_sin_td` | 0,014 | Reduccion de RMSE (°C) de `tuned` al quitar los rezagos de Td, `ll4b`, dominio completo |
| `a2.ll4b.panel.brecha_timesfm_tuned` | 0,076 | Magnitud de la brecha TimesFM − `tuned` (°C), `ll4b`, dominio completo |
| `a2.ll4b.panel.fraccion_cerrada_pct` | 18 | Porcentaje (sin %) de la brecha TimesFM − `tuned` que cubre quitar los rezagos de Td, `ll4b`, dominio completo |
| `a2.ll4b.panel.brecha_timesfm_sin_td` | 0,062 | Magnitud de la brecha restante de TimesFM frente a `tuned` sin rezagos de Td (°C), `ll4b`, dominio completo |
| `a2.ll4b.peru.mejora_sin_td` | 0,005 | Reduccion de RMSE (°C) de `tuned` al quitar los rezagos de Td, `ll4b`, Perú |
| `a2.ll4b.peru.brecha_timesfm_tuned` | 0,056 | Magnitud de la brecha TimesFM − `tuned` (°C), `ll4b`, Perú |
| `a2.ll4b.peru.fraccion_cerrada_pct` | 9 | Porcentaje (sin %) de la brecha TimesFM − `tuned` que cubre quitar los rezagos de Td, `ll4b`, Perú |
| `a2.ll4b.peru.brecha_timesfm_sin_td` | 0,052 | Magnitud de la brecha restante de TimesFM frente a `tuned` sin rezagos de Td (°C), `ll4b`, Perú |
| `a2.ll4.panel.mejora_sin_td` | 0,054 | Reduccion de RMSE (°C) de `tuned` al quitar los rezagos de Td, `ll4`, dominio completo |
| `a2.ll4.panel.brecha_timesfm_tuned` | 0,074 | Magnitud de la brecha TimesFM − `tuned` (°C), `ll4`, dominio completo |
| `a2.ll4.panel.fraccion_cerrada_pct` | 72 | Porcentaje (sin %) de la brecha TimesFM − `tuned` que cubre quitar los rezagos de Td, `ll4`, dominio completo |
| `a2.ll4.panel.brecha_timesfm_sin_td` | 0,021 | Magnitud de la brecha restante de TimesFM frente a `tuned` sin rezagos de Td (°C), `ll4`, dominio completo |
| `a2.ll4.peru.mejora_sin_td` | 0,036 | Reduccion de RMSE (°C) de `tuned` al quitar los rezagos de Td, `ll4`, Perú |
| `a2.ll4.peru.brecha_timesfm_tuned` | 0,079 | Magnitud de la brecha TimesFM − `tuned` (°C), `ll4`, Perú |
| `a2.ll4.peru.fraccion_cerrada_pct` | 46 | Porcentaje (sin %) de la brecha TimesFM − `tuned` que cubre quitar los rezagos de Td, `ll4`, Perú |
| `a2.ll4.peru.brecha_timesfm_sin_td` | 0,043 | Magnitud de la brecha restante de TimesFM frente a `tuned` sin rezagos de Td (°C), `ll4`, Perú |
| `a2.anios_sin_td_peor` | 2009 y 2013 | Años (dominio completo) en que `tuned` sin rezagos de Td tiene mayor RMSE que `tuned` |

## variantes

| clave | valor | significado |
|---|---|---|
| `variantes.uni_td_full.contexto_ini` | 1981 | Primer año de contexto de la variante uni_td_full |
| `variantes.uni_td_full.contexto_anios.ll4b` | 28 | Años de contexto de la variante uni_td_full en `ll4b` |
| `variantes.uni_td_full.contexto_anios.ll4` | 32 | Años de contexto de la variante uni_td_full en `ll4` |
| `variantes.uni_anom_full.contexto_ini` | 1981 | Primer año de contexto de la variante uni_anom_full |
| `variantes.uni_anom_full.contexto_anios.ll4b` | 28 | Años de contexto de la variante uni_anom_full en `ll4b` |
| `variantes.uni_anom_full.contexto_anios.ll4` | 32 | Años de contexto de la variante uni_anom_full en `ll4` |
| `variantes.tmin_td_full.contexto_ini` | 1981 | Primer año de contexto de la variante tmin_td_full |
| `variantes.tmin_td_full.contexto_anios.ll4b` | 28 | Años de contexto de la variante tmin_td_full en `ll4b` |
| `variantes.tmin_td_full.contexto_anios.ll4` | 32 | Años de contexto de la variante tmin_td_full en `ll4` |
| `variantes.tmin_anom_full.contexto_ini` | 1981 | Primer año de contexto de la variante tmin_anom_full |
| `variantes.tmin_anom_full.contexto_anios.ll4b` | 28 | Años de contexto de la variante tmin_anom_full en `ll4b` |
| `variantes.tmin_anom_full.contexto_anios.ll4` | 32 | Años de contexto de la variante tmin_anom_full en `ll4` |
| `variantes.tmin_doy_td_full.contexto_ini` | 1981 | Primer año de contexto de la variante tmin_doy_td_full |
| `variantes.tmin_doy_td_full.contexto_anios.ll4b` | 28 | Años de contexto de la variante tmin_doy_td_full en `ll4b` |
| `variantes.tmin_doy_td_full.contexto_anios.ll4` | 32 | Años de contexto de la variante tmin_doy_td_full en `ll4` |
| `variantes.tmin_td_med.contexto_ini` | 2002 | Primer año de contexto de la variante tmin_td_med |
| `variantes.tmin_td_med.contexto_anios.ll4b` | 7 | Años de contexto de la variante tmin_td_med en `ll4b` |
| `variantes.tmin_td_med.contexto_anios.ll4` | 11 | Años de contexto de la variante tmin_td_med en `ll4` |
| `variantes.tmin_anom_med.contexto_ini` | 2002 | Primer año de contexto de la variante tmin_anom_med |
| `variantes.tmin_anom_med.contexto_anios.ll4b` | 7 | Años de contexto de la variante tmin_anom_med en `ll4b` |
| `variantes.tmin_anom_med.contexto_anios.ll4` | 11 | Años de contexto de la variante tmin_anom_med en `ll4` |
| `variantes.tmin_td_short.contexto_ini` | 2011 | Primer año de contexto de la variante tmin_td_short |
| `variantes.tmin_td_short.contexto_anios.ll4b` | -2 | Años de contexto de la variante tmin_td_short en `ll4b` |
| `variantes.tmin_td_short.contexto_anios.ll4` | 2 | Años de contexto de la variante tmin_td_short en `ll4` |
| `variantes.tmin_td_symavg.contexto_ini` | 1981 | Primer año de contexto de la variante tmin_td_symavg |
| `variantes.tmin_td_symavg.contexto_anios.ll4b` | 28 | Años de contexto de la variante tmin_td_symavg en `ll4b` |
| `variantes.tmin_td_symavg.contexto_anios.ll4` | 32 | Años de contexto de la variante tmin_td_symavg en `ll4` |
| `variantes.tmin_td_znorm.contexto_ini` | 1981 | Primer año de contexto de la variante tmin_td_znorm |
| `variantes.tmin_td_znorm.contexto_anios.ll4b` | 28 | Años de contexto de la variante tmin_td_znorm en `ll4b` |
| `variantes.tmin_td_znorm.contexto_anios.ll4` | 32 | Años de contexto de la variante tmin_td_znorm en `ll4` |
| `variantes.n_total` | 10 | Variantes definidas en el código (incluye las que no entraron al cribado) |
| `variantes.inicios_cribado` | 1981, 2002 y 2011 | Años de inicio del contexto probados en el cribado |
| `variantes.n_univariadas` | 2 | Variantes del cribado sin Tmin (univariadas) |

## diseno

| clave | valor | significado |
|---|---|---|
| `diseno.llr.n_variantes` | 4 | Variantes de LLR sin zonas evaluadas (llr_rezagos, llr_rezagos_sel, llr_simple y llr_simple_sel) |
| `diseno.tuned.pool_terminos` | 11 | Términos candidatos del pool de `tuned` (incluye la constante) |
| `diseno.tuned.pool_rezagos_td` | 5 | Rezagos de Td en el pool de `tuned` |
| `diseno.tuned.pool_rezagos_tmin` | 4 | Rezagos de Tmin en el pool de `tuned` |
| `diseno.tuned.pool_sin_td` | 6 | Términos del pool de `tuned_sin_td` |
| `diseno.tuned.rezagos_td` | 1, 2, 3, 7 y 30 | Lista de rezagos de Td del pool |
| `diseno.tuned.rezagos_tmin` | 1, 2, 7 y 30 | Lista de rezagos de Tmin del pool |
| `diseno.tuned.h_min` | n. d. | Menor semiancho `h` de la grilla de `tuned` (usada en el artículo) (la grilla 7-45 solo está documentada en costo.md; el valor por defecto del código es otro (HPC_code_tunning, h_grid=7,11,15,21)) |
| `diseno.tuned.h_max` | n. d. | Mayor semiancho `h` de la grilla de `tuned` (usada en el artículo) (ver diseno.tuned.h_min) |
| `diseno.llr.h_n` | 7 | Valores de `h` de los LLR sin selección conjunta |
| `diseno.llr.h_min` | 7 | Menor `h` de los LLR sin selección conjunta |
| `diseno.llr.h_max` | 60 | Mayor `h` de los LLR sin selección conjunta |
| `diseno.llr_sel.h_n` | 10 | Valores de `h` de los LLR seleccionados |
| `diseno.llr_sel.h_min` | 7 | Menor `h` de los LLR seleccionados |
| `diseno.llr_sel.h_max` | 180 | Mayor `h` de los LLR seleccionados |
| `diseno.llr_sel.inicios_n` | 4 | Años de inicio candidatos de los LLR seleccionados |
| `diseno.llr_sel.inicio_min` | 1981 | Primer año de inicio candidato |
| `diseno.llr_sel.inicio_max` | 1996 | Último año de inicio candidato |
| `diseno.llr_sel.combinaciones` | 40 | Combinaciones (h, inicio) evaluadas por los LLR seleccionados |
| `diseno.llr.validacion_anios` | 4 | Últimos años de entrenamiento usados como validación interna de los LLR |
| `diseno.llr.rezagos_tmin` | 1, 2, 7 y 30 | Rezagos de Tmin del LLR con rezagos |

## timesfm

| clave | valor | significado |
|---|---|---|
| `timesfm.parametros_millones` | 330 | Parámetros de TimesFM 3.0 (millones) (constante documentada (API de Hugging Face), no derivada de código) |

## horizonte

| clave | valor | significado |
|---|---|---|
| `horizonte.ll4b.panel.tuned.anio1.v` | −0,009 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio1.ic` | [−0,019; +0,001] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio1.excluye_cero` | no | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.panel.tuned.anio2.v` | −0,107 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio2.ic` | [−0,122; −0,091] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.panel.tuned.anio3.v` | −0,083 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio3.ic` | [−0,095; −0,071] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.panel.tuned.anio4.v` | −0,100 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio4.ic` | [−0,110; −0,090] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.panel.tuned.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes1.v` | −0,026 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes1.ic` | [−0,035; −0,017] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes12.v` | −0,027 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes12.ic` | [−0,047; −0,006] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes24.v` | +0,008 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes24.ic` | [−0,003; +0,018] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes36.v` | −0,064 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes36.ic` | [−0,076; −0,051] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes48.v` | −0,031 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes48.ic` | [−0,043; −0,020] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.meses_neg` | 37 | Meses (de 48) con brecha negativa, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.meses_ic_neg` | 34 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.meses_ic_pos` | 8 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.meses_ic_incluye` | 6 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes_mayor_ventaja` | 19 | Mes con la brecha más negativa, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.brecha_mayor_ventaja` | −0,323 | Brecha del mes con la brecha más negativa, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.mes_menor_ventaja` | 4 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.brecha_menor_ventaja` | +0,096 | Brecha del mes con la brecha menos negativa, TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.media_mes1_12` | −0,009 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned.media_mes37_48` | −0,096 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio1.v` | −0,024 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio1.ic` | [−0,032; −0,017] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.panel.tuned_sin_td.anio2.v` | −0,083 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio2.ic` | [−0,093; −0,073] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.panel.tuned_sin_td.anio3.v` | −0,057 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio3.ic` | [−0,065; −0,049] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.panel.tuned_sin_td.anio4.v` | −0,082 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio4.ic` | [−0,092; −0,072] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.panel.tuned_sin_td.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes1.v` | −0,028 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes1.ic` | [−0,036; −0,021] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes12.v` | −0,038 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes12.ic` | [−0,058; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes24.v` | −0,046 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes24.ic` | [−0,056; −0,036] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes36.v` | −0,045 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes36.ic` | [−0,056; −0,035] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes48.v` | −0,035 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes48.ic` | [−0,043; −0,027] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.meses_neg` | 41 | Meses (de 48) con brecha negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.meses_ic_neg` | 39 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.meses_ic_pos` | 4 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.meses_ic_incluye` | 5 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes_mayor_ventaja` | 19 | Mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.brecha_mayor_ventaja` | −0,324 | Brecha del mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.mes_menor_ventaja` | 14 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.brecha_menor_ventaja` | +0,087 | Brecha del mes con la brecha menos negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.media_mes1_12` | −0,025 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.tuned_sin_td.media_mes37_48` | −0,078 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio1.v` | −0,008 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio1.ic` | [−0,014; −0,002] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio2.v` | −0,046 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio2.ic` | [−0,055; −0,037] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio3.v` | −0,028 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio3.ic` | [−0,031; −0,024] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio4.v` | −0,031 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio4.ic` | [−0,035; −0,027] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.panel.llr_rezagos_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes1.v` | −0,008 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes1.ic` | [−0,017; −0,001] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes12.v` | +0,009 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes12.ic` | [−0,005; +0,024] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes24.v` | −0,047 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes24.ic` | [−0,056; −0,039] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes36.v` | −0,012 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes36.ic` | [−0,018; −0,008] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes48.v` | −0,029 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes48.ic` | [−0,036; −0,021] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.meses_neg` | 33 | Meses (de 48) con brecha negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.meses_ic_neg` | 30 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.meses_ic_pos` | 9 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.meses_ic_incluye` | 9 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes_mayor_ventaja` | 19 | Mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.brecha_mayor_ventaja` | −0,179 | Brecha del mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.mes_menor_ventaja` | 15 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.brecha_menor_ventaja` | +0,095 | Brecha del mes con la brecha menos negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.media_mes1_12` | −0,006 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_rezagos_sel.media_mes37_48` | −0,032 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio1.v` | −0,007 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio1.ic` | [−0,013; −0,001] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.panel.llr_simple_sel.anio2.v` | −0,052 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio2.ic` | [−0,058; −0,047] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.panel.llr_simple_sel.anio3.v` | −0,046 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio3.ic` | [−0,051; −0,042] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.panel.llr_simple_sel.anio4.v` | −0,041 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio4.ic` | [−0,050; −0,033] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.panel.llr_simple_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes1.v` | −0,029 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes1.ic` | [−0,036; −0,022] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes12.v` | −0,001 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes12.ic` | [−0,012; +0,009] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes24.v` | −0,042 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes24.ic` | [−0,053; −0,033] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes36.v` | −0,017 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes36.ic` | [−0,022; −0,013] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes48.v` | −0,024 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes48.ic` | [−0,031; −0,016] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.meses_ic_neg` | 35 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.meses_ic_pos` | 7 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.meses_ic_incluye` | 6 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.brecha_mayor_ventaja` | −0,178 | Brecha del mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.mes_menor_ventaja` | 15 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.brecha_menor_ventaja` | +0,085 | Brecha del mes con la brecha menos negativa, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.media_mes1_12` | −0,005 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.panel.llr_simple_sel.media_mes37_48` | −0,042 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `horizonte.ll4b.peru.tuned.anio1.v` | −0,022 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio1.ic` | [−0,040; −0,007] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.peru.tuned.anio2.v` | −0,076 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio2.ic` | [−0,092; −0,060] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.peru.tuned.anio3.v` | −0,052 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio3.ic` | [−0,061; −0,044] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.peru.tuned.anio4.v` | −0,073 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio4.ic` | [−0,084; −0,061] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.peru.tuned.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes1.v` | −0,016 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes1.ic` | [−0,027; −0,005] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes12.v` | +0,002 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes12.ic` | [−0,028; +0,031] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes24.v` | −0,014 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes24.ic` | [−0,031; +0,002] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes36.v` | −0,044 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes36.ic` | [−0,057; −0,032] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes48.v` | −0,018 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes48.ic` | [−0,036; −0,002] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.meses_neg` | 38 | Meses (de 48) con brecha negativa, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.meses_ic_neg` | 31 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.meses_ic_pos` | 2 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.meses_ic_incluye` | 15 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes_mayor_ventaja` | 44 | Mes con la brecha más negativa, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.brecha_mayor_ventaja` | −0,215 | Brecha del mes con la brecha más negativa, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.mes_menor_ventaja` | 8 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.brecha_menor_ventaja` | +0,061 | Brecha del mes con la brecha menos negativa, TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.media_mes1_12` | −0,021 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned.media_mes37_48` | −0,069 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio1.v` | −0,039 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio1.ic` | [−0,051; −0,030] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.peru.tuned_sin_td.anio2.v` | −0,071 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio2.ic` | [−0,082; −0,061] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.peru.tuned_sin_td.anio3.v` | −0,041 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio3.ic` | [−0,047; −0,036] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.peru.tuned_sin_td.anio4.v` | −0,055 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio4.ic` | [−0,065; −0,046] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.peru.tuned_sin_td.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes1.v` | −0,045 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes1.ic` | [−0,054; −0,036] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes12.v` | −0,009 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes12.ic` | [−0,029; +0,012] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes24.v` | −0,043 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes24.ic` | [−0,051; −0,034] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes36.v` | −0,029 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes36.ic` | [−0,038; −0,021] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes48.v` | −0,031 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes48.ic` | [−0,040; −0,023] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.meses_neg` | 43 | Meses (de 48) con brecha negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.meses_ic_neg` | 37 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.meses_ic_pos` | 1 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.meses_ic_incluye` | 10 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes_mayor_ventaja` | 19 | Mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.brecha_mayor_ventaja` | −0,197 | Brecha del mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.mes_menor_ventaja` | 14 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.brecha_menor_ventaja` | +0,035 | Brecha del mes con la brecha menos negativa, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.media_mes1_12` | −0,039 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.tuned_sin_td.media_mes37_48` | −0,053 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio1.v` | −0,018 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio1.ic` | [−0,025; −0,013] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio2.v` | −0,035 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio2.ic` | [−0,040; −0,030] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio3.v` | −0,026 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio3.ic` | [−0,030; −0,023] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio4.v` | −0,023 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio4.ic` | [−0,027; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.peru.llr_rezagos_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes1.v` | −0,029 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes1.ic` | [−0,037; −0,021] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes12.v` | +0,022 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes12.ic` | [+0,003; +0,040] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes24.v` | −0,043 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes24.ic` | [−0,052; −0,036] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes36.v` | −0,025 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes36.ic` | [−0,034; −0,017] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes48.v` | −0,031 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes48.ic` | [−0,039; −0,023] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.meses_ic_neg` | 32 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.meses_ic_pos` | 4 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.meses_ic_incluye` | 12 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes_mayor_ventaja` | 19 | Mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.brecha_mayor_ventaja` | −0,090 | Brecha del mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.mes_menor_ventaja` | 15 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.brecha_menor_ventaja` | +0,058 | Brecha del mes con la brecha menos negativa, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.media_mes1_12` | −0,017 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_rezagos_sel.media_mes37_48` | −0,026 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio1.v` | −0,016 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio1.ic` | [−0,026; −0,008] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4b.peru.llr_simple_sel.anio2.v` | −0,045 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio2.ic` | [−0,049; −0,041] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4b.peru.llr_simple_sel.anio3.v` | −0,037 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio3.ic` | [−0,041; −0,033] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4b.peru.llr_simple_sel.anio4.v` | −0,021 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio4.ic` | [−0,026; −0,016] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4b.peru.llr_simple_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes1.v` | −0,036 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes1.ic` | [−0,046; −0,028] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes12.v` | −0,001 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes12.ic` | [−0,017; +0,015] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes24.v` | −0,050 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes24.ic` | [−0,060; −0,041] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes36.v` | −0,027 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes36.ic` | [−0,034; −0,020] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes48.v` | −0,024 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes48.ic` | [−0,036; −0,012] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.meses_neg` | 41 | Meses (de 48) con brecha negativa, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.meses_ic_neg` | 37 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.meses_ic_pos` | 2 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.meses_ic_incluye` | 9 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.brecha_mayor_ventaja` | −0,108 | Brecha del mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.mes_menor_ventaja` | 15 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.brecha_menor_ventaja` | +0,043 | Brecha del mes con la brecha menos negativa, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.media_mes1_12` | −0,017 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4b.peru.llr_simple_sel.media_mes37_48` | −0,023 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `horizonte.ll4.panel.tuned.anio1.v` | +0,055 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio1.ic` | [+0,026; +0,082] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.panel.tuned.anio2.v` | −0,059 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio2.ic` | [−0,069; −0,049] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.panel.tuned.anio3.v` | −0,165 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio3.ic` | [−0,179; −0,152] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.panel.tuned.anio4.v` | −0,126 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio4.ic` | [−0,148; −0,101] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.panel.tuned.anios_positivos` | 1 | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.anio1_positivo` | sí | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes1.v` | −0,103 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes1.ic` | [−0,124; −0,078] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes12.v` | −0,058 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes12.ic` | [−0,074; −0,042] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes24.v` | −0,032 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes24.ic` | [−0,043; −0,022] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes36.v` | −0,095 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes36.ic` | [−0,113; −0,078] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes48.v` | −0,012 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes48.ic` | [−0,024; +0,0001] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.meses_neg` | 35 | Meses (de 48) con brecha negativa, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.meses_ic_neg` | 32 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.meses_ic_pos` | 11 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.meses_ic_incluye` | 5 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes_mayor_ventaja` | 37 | Mes con la brecha más negativa, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.brecha_mayor_ventaja` | −0,595 | Brecha del mes con la brecha más negativa, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.mes_menor_ventaja` | 6 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.brecha_menor_ventaja` | +0,367 | Brecha del mes con la brecha menos negativa, TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.media_mes1_12` | +0,015 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned.media_mes37_48` | −0,085 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio1.v` | +0,050 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio1.ic` | [+0,026; +0,072] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.panel.tuned_sin_td.anio2.v` | −0,024 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio2.ic` | [−0,032; −0,015] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.panel.tuned_sin_td.anio3.v` | −0,087 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio3.ic` | [−0,093; −0,080] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.panel.tuned_sin_td.anio4.v` | −0,026 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio4.ic` | [−0,034; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.panel.tuned_sin_td.anios_positivos` | 1 | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.anio1_positivo` | sí | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes1.v` | −0,070 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes1.ic` | [−0,085; −0,054] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes12.v` | +0,018 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes12.ic` | [+0,005; +0,031] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes24.v` | −0,064 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes24.ic` | [−0,075; −0,054] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes36.v` | −0,008 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes36.ic` | [−0,032; +0,012] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes48.v` | −0,019 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes48.ic` | [−0,030; −0,008] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.meses_neg` | 29 | Meses (de 48) con brecha negativa, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.meses_ic_neg` | 26 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.meses_ic_pos` | 16 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.meses_ic_incluye` | 6 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.brecha_mayor_ventaja` | −0,295 | Brecha del mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.mes_menor_ventaja` | 8 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.brecha_menor_ventaja` | +0,240 | Brecha del mes con la brecha menos negativa, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.media_mes1_12` | +0,018 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.tuned_sin_td.media_mes37_48` | −0,020 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio1.v` | +0,060 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio1.ic` | [+0,035; +0,083] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.panel.llr_rezagos_sel.anio2.v` | −0,022 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio2.ic` | [−0,027; −0,017] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.panel.llr_rezagos_sel.anio3.v` | −0,050 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio3.ic` | [−0,054; −0,047] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.panel.llr_rezagos_sel.anio4.v` | −0,003 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio4.ic` | [−0,010; +0,002] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio4.excluye_cero` | no | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.panel.llr_rezagos_sel.anios_positivos` | 1 | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.anio1_positivo` | sí | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes1.v` | −0,055 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes1.ic` | [−0,065; −0,045] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes12.v` | +0,065 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes12.ic` | [+0,042; +0,088] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes24.v` | −0,069 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes24.ic` | [−0,080; −0,058] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes36.v` | +0,004 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes36.ic` | [−0,019; +0,023] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes48.v` | −0,024 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes48.ic` | [−0,030; −0,017] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.meses_neg` | 28 | Meses (de 48) con brecha negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.meses_ic_neg` | 27 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.meses_ic_pos` | 15 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.meses_ic_incluye` | 6 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.brecha_mayor_ventaja` | −0,179 | Brecha del mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.mes_menor_ventaja` | 8 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.brecha_menor_ventaja` | +0,200 | Brecha del mes con la brecha menos negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.media_mes1_12` | +0,041 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_rezagos_sel.media_mes37_48` | −0,004 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio1.v` | +0,046 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio1.ic` | [+0,023; +0,067] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio1.excluye_cero` | sí | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio1.n` | 6.214.855 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.panel.llr_simple_sel.anio2.v` | −0,020 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio2.ic` | [−0,025; −0,014] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio2.n` | 6.214.855 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.panel.llr_simple_sel.anio3.v` | −0,076 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio3.ic` | [−0,082; −0,070] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio3.n` | 6.214.855 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.panel.llr_simple_sel.anio4.v` | −0,026 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio4.ic` | [−0,032; −0,021] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio4.n` | 6.231.882 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.panel.llr_simple_sel.anios_positivos` | 1 | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.anio1_positivo` | sí | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes1.v` | −0,057 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes1.ic` | [−0,064; −0,049] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes12.v` | +0,049 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes12.ic` | [+0,025; +0,071] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes24.v` | −0,035 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes24.ic` | [−0,043; −0,027] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes36.v` | −0,063 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes36.ic` | [−0,095; −0,037] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes48.v` | −0,018 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes48.ic` | [−0,025; −0,013] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.meses_neg` | 30 | Meses (de 48) con brecha negativa, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.meses_ic_neg` | 29 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.meses_ic_pos` | 15 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.meses_ic_incluye` | 4 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.brecha_mayor_ventaja` | −0,231 | Brecha del mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.mes_menor_ventaja` | 6 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.brecha_menor_ventaja` | +0,143 | Brecha del mes con la brecha menos negativa, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.media_mes1_12` | +0,029 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.panel.llr_simple_sel.media_mes37_48` | −0,022 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `horizonte.ll4.peru.tuned.anio1.v` | −0,025 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio1.ic` | [−0,049; +0,0004] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio1.excluye_cero` | no | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.peru.tuned.anio2.v` | −0,072 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio2.ic` | [−0,080; −0,065] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.peru.tuned.anio3.v` | −0,137 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio3.ic` | [−0,159; −0,114] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.peru.tuned.anio4.v` | −0,081 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio4.ic` | [−0,100; −0,062] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.peru.tuned.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes1.v` | −0,061 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes1.ic` | [−0,078; −0,043] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes12.v` | −0,082 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes12.ic` | [−0,101; −0,064] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes24.v` | −0,039 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes24.ic` | [−0,060; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes36.v` | −0,107 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes36.ic` | [−0,135; −0,078] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes48.v` | −0,016 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes48.ic` | [−0,034; +0,002] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.meses_ic_neg` | 36 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.meses_ic_pos` | 3 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.meses_ic_incluye` | 9 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.brecha_mayor_ventaja` | −0,313 | Brecha del mes con la brecha más negativa, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.mes_menor_ventaja` | 6 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.brecha_menor_ventaja` | +0,126 | Brecha del mes con la brecha menos negativa, TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.media_mes1_12` | −0,037 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned.media_mes37_48` | −0,068 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio1.v` | −0,020 | Brecha (°C) en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio1.ic` | [−0,042; +0,002] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio1.excluye_cero` | no | ¿El IC del año 1 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.peru.tuned_sin_td.anio2.v` | −0,045 | Brecha (°C) en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio2.ic` | [−0,053; −0,038] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.peru.tuned_sin_td.anio3.v` | −0,073 | Brecha (°C) en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio3.ic` | [−0,084; −0,062] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.peru.tuned_sin_td.anio4.v` | −0,033 | Brecha (°C) en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio4.ic` | [−0,049; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.peru.tuned_sin_td.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes1.v` | −0,057 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes1.ic` | [−0,074; −0,042] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes12.v` | −0,025 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes12.ic` | [−0,035; −0,016] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes24.v` | −0,073 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes24.ic` | [−0,093; −0,056] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes36.v` | −0,041 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes36.ic` | [−0,080; −0,004] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes48.v` | −0,031 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes48.ic` | [−0,045; −0,018] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.meses_ic_neg` | 32 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.meses_ic_pos` | 2 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.meses_ic_incluye` | 14 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.brecha_mayor_ventaja` | −0,196 | Brecha del mes con la brecha más negativa, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.mes_menor_ventaja` | 8 | Mes con la brecha menos negativa (o más positiva), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.brecha_menor_ventaja` | +0,060 | Brecha del mes con la brecha menos negativa, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.media_mes1_12` | −0,029 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.tuned_sin_td.media_mes37_48` | −0,033 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio1.v` | −0,011 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio1.ic` | [−0,029; +0,010] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio1.excluye_cero` | no | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.peru.llr_rezagos_sel.anio2.v` | −0,035 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio2.ic` | [−0,039; −0,031] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.peru.llr_rezagos_sel.anio3.v` | −0,046 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio3.ic` | [−0,052; −0,039] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.peru.llr_rezagos_sel.anio4.v` | −0,012 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio4.ic` | [−0,023; −0,001] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.peru.llr_rezagos_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes1.v` | −0,046 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes1.ic` | [−0,059; −0,034] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes12.v` | −0,0004 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes12.ic` | [−0,016; +0,017] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes24.v` | −0,052 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes24.ic` | [−0,063; −0,041] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes36.v` | −0,013 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes36.ic` | [−0,047; +0,019] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes48.v` | −0,021 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes48.ic` | [−0,030; −0,012] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.meses_ic_neg` | 29 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.meses_ic_pos` | 3 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.meses_ic_incluye` | 16 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.brecha_mayor_ventaja` | −0,114 | Brecha del mes con la brecha más negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.mes_menor_ventaja` | 37 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.brecha_menor_ventaja` | +0,054 | Brecha del mes con la brecha menos negativa, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.media_mes1_12` | −0,014 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_rezagos_sel.media_mes37_48` | −0,012 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio1.v` | −0,018 | Brecha (°C) en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio1.ic` | [−0,037; +0,002] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 1 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio1.excluye_cero` | no | ¿El IC del año 1 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio1.n` | 3.019.280 | Filas celda × día del año 1 del bloque |
| `horizonte.ll4.peru.llr_simple_sel.anio2.v` | −0,036 | Brecha (°C) en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio2.ic` | [−0,041; −0,031] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 2 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio2.excluye_cero` | sí | ¿El IC del año 2 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio2.n` | 3.019.280 | Filas celda × día del año 2 del bloque |
| `horizonte.ll4.peru.llr_simple_sel.anio3.v` | −0,074 | Brecha (°C) en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio3.ic` | [−0,086; −0,062] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 3 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio3.excluye_cero` | sí | ¿El IC del año 3 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio3.n` | 3.019.280 | Filas celda × día del año 3 del bloque |
| `horizonte.ll4.peru.llr_simple_sel.anio4.v` | −0,037 | Brecha (°C) en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio4.ic` | [−0,046; −0,028] | IC 95 % (bloques espaciales de 2°) de la brecha en el año 4 del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio4.excluye_cero` | sí | ¿El IC del año 4 del bloque excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio4.n` | 3.027.552 | Filas celda × día del año 4 del bloque |
| `horizonte.ll4.peru.llr_simple_sel.anios_positivos` | ninguno | Años del bloque con brecha positiva (TimesFM peor), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.anio1_positivo` | no | ¿La brecha del primer año del bloque es positiva (TimesFM peor)? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes1.v` | −0,052 | Brecha (°C) en el mes 1 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes1.ic` | [−0,064; −0,041] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 1, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes12.v` | −0,014 | Brecha (°C) en el mes 12 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes12.ic` | [−0,031; +0,003] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 12, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes24.v` | −0,033 | Brecha (°C) en el mes 24 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes24.ic` | [−0,048; −0,019] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 24, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes36.v` | −0,072 | Brecha (°C) en el mes 36 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes36.ic` | [−0,109; −0,043] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 36, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes48.v` | −0,023 | Brecha (°C) en el mes 48 desde el inicio del bloque, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes48.ic` | [−0,033; −0,014] | IC 95 % (bloques espaciales de 2°) de la brecha del mes 48, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.meses_neg` | 39 | Meses (de 48) con brecha negativa, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.meses_ic_neg` | 32 | Meses (de 48) con IC 95 % enteramente por debajo de cero, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.meses_ic_pos` | 1 | Meses (de 48) con IC 95 % enteramente por encima de cero, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.meses_ic_incluye` | 15 | Meses (de 48) con IC 95 % que incluye cero, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes_mayor_ventaja` | 31 | Mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.brecha_mayor_ventaja` | −0,174 | Brecha del mes con la brecha más negativa, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.mes_menor_ventaja` | 15 | Mes con la brecha menos negativa (o más positiva), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.brecha_menor_ventaja` | +0,032 | Brecha del mes con la brecha menos negativa, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.media_mes1_12` | −0,022 | Media simple de las brechas mensuales de los meses 1–12 (descriptiva), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `horizonte.ll4.peru.llr_simple_sel.media_mes37_48` | −0,035 | Media simple de las brechas mensuales de los meses 37–48 (descriptiva), TimesFM − LLR simple seleccionado, `ll4`, Perú |

## robustez

| clave | valor | significado |
|---|---|---|
| `robustez.ll4b.panel.tuned.v` | −0,076 | Brecha puntual (°C), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_lo` | −0,084 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_hi` | −0,068 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_ic` | [−0,084; −0,068] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esp_bloques_a_gana` | 74 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_lo` | −0,084 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_hi` | −0,067 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_ic` | [−0,084; −0,067] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.esa_bloques_a_gana` | 266 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_lo` | −0,113 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_hi` | −0,039 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_ic` | [−0,113; −0,039] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned.ta_bloques_a_gana` | 12 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.v` | −0,062 | Brecha puntual (°C), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_lo` | −0,068 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_hi` | −0,056 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_ic` | [−0,068; −0,056] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esp_bloques_a_gana` | 74 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_lo` | −0,068 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_hi` | −0,056 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_ic` | [−0,068; −0,056] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.esa_bloques_a_gana` | 281 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_lo` | −0,092 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_hi` | −0,034 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_ic` | [−0,092; −0,034] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.tuned_sin_td.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.v` | −0,028 | Brecha puntual (°C), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_lo` | −0,031 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_hi` | −0,026 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_ic` | [−0,031; −0,026] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esp_bloques_a_gana` | 74 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_lo` | −0,032 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_hi` | −0,025 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_ic` | [−0,032; −0,025] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.esa_bloques_a_gana` | 266 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_lo` | −0,048 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_hi` | −0,011 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_ic` | [−0,048; −0,011] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_rezagos_sel.ta_bloques_a_gana` | 12 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.v` | −0,037 | Brecha puntual (°C), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_lo` | −0,041 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_hi` | −0,033 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_ic` | [−0,041; −0,033] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esp_bloques_a_gana` | 74 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_lo` | −0,041 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_hi` | −0,032 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_ic` | [−0,041; −0,032] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.esa_bloques_a_gana` | 265 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_lo` | −0,058 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_hi` | −0,019 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_ic` | [−0,058; −0,019] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.panel.llr_simple_sel.ta_bloques_a_gana` | 13 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `robustez.ll4b.peru.tuned.v` | −0,056 | Brecha puntual (°C), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_lo` | −0,065 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_hi` | −0,049 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_ic` | [−0,065; −0,049] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esp_bloques_a_gana` | 45 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_lo` | −0,064 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_hi` | −0,049 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_ic` | [−0,064; −0,049] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.esa_bloques_a_gana` | 166 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_lo` | −0,078 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_hi` | −0,035 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_ic` | [−0,078; −0,035] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.v` | −0,052 | Brecha puntual (°C), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_lo` | −0,058 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_hi` | −0,045 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_ic` | [−0,058; −0,045] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esp_bloques_a_gana` | 45 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_lo` | −0,057 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_hi` | −0,047 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_ic` | [−0,057; −0,047] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.esa_bloques_a_gana` | 178 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_lo` | −0,069 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_hi` | −0,036 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_ic` | [−0,069; −0,036] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.tuned_sin_td.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.v` | −0,025 | Brecha puntual (°C), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_lo` | −0,028 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_hi` | −0,023 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_ic` | [−0,028; −0,023] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esp_bloques_a_gana` | 45 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_lo` | −0,028 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_hi` | −0,023 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_ic` | [−0,028; −0,023] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.esa_bloques_a_gana` | 169 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_lo` | −0,036 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_hi` | −0,015 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_ic` | [−0,036; −0,015] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_rezagos_sel.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.v` | −0,030 | Brecha puntual (°C), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_lo` | −0,033 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_hi` | −0,026 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_ic` | [−0,033; −0,026] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esp_bloques_a_gana` | 45 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_lo` | −0,033 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_hi` | −0,026 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_ic` | [−0,033; −0,026] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.esa_bloques_a_gana` | 164 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_lo` | −0,041 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_hi` | −0,019 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_ic` | [−0,041; −0,019] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4b.peru.llr_simple_sel.ta_bloques_a_gana` | 14 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `robustez.ll4.panel.tuned.v` | −0,074 | Brecha puntual (°C), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_lo` | −0,080 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_hi` | −0,069 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_ic` | [−0,080; −0,069] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esp_bloques_a_gana` | 74 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_lo` | −0,091 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_hi` | −0,058 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_ic` | [−0,091; −0,058] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.esa_bloques_a_gana` | 251 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_lo` | −0,143 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_hi` | −0,005 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_ic` | [−0,143; −0,005] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned.ta_bloques_a_gana` | 12 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.v` | −0,021 | Brecha puntual (°C), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_lo` | −0,029 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_hi` | −0,013 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_ic` | [−0,029; −0,013] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esp_bloques_a_gana` | 58 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_lo` | −0,030 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_hi` | −0,011 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_ic` | [−0,030; −0,011] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.esa_bloques_a_gana` | 234 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_lo` | −0,062 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_hi` | +0,021 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_ic` | [−0,062; +0,021] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_excluye_cero` | no | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.tuned_sin_td.ta_bloques_a_gana` | 11 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.v` | −0,003 | Brecha puntual (°C), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_lo` | −0,011 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_hi` | +0,004 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_ic` | [−0,011; +0,004] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_excluye_cero` | no | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esp_bloques_a_gana` | 49 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_lo` | −0,011 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_hi` | +0,006 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_ic` | [−0,011; +0,006] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_excluye_cero` | no | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.esa_bloques_a_gana` | 219 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_lo` | −0,033 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_hi` | +0,028 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_ic` | [−0,033; +0,028] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_excluye_cero` | no | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_rezagos_sel.ta_bloques_a_gana` | 10 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.v` | −0,018 | Brecha puntual (°C), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_lo` | −0,027 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_hi` | −0,010 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_ic` | [−0,027; −0,010] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_bloques` | 74 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esp_bloques_a_gana` | 58 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_lo` | −0,027 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_hi` | −0,009 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_ic` | [−0,027; −0,009] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_bloques` | 296 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.esa_bloques_a_gana` | 248 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_lo` | −0,049 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_hi` | +0,012 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_ic` | [−0,049; +0,012] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_excluye_cero` | no | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.panel.llr_simple_sel.ta_bloques_a_gana` | 11 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `robustez.ll4.peru.tuned.v` | −0,079 | Brecha puntual (°C), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_lo` | −0,087 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_hi` | −0,071 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_ic` | [−0,087; −0,071] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esp_bloques_a_gana` | 45 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_lo` | −0,091 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_hi` | −0,067 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_ic` | [−0,091; −0,067] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.esa_bloques_a_gana` | 166 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_lo` | −0,113 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_hi` | −0,048 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_ic` | [−0,113; −0,048] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.v` | −0,043 | Brecha puntual (°C), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_lo` | −0,054 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_hi` | −0,033 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_ic` | [−0,054; −0,033] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esp_bloques_a_gana` | 43 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_lo` | −0,051 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_hi` | −0,034 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_ic` | [−0,051; −0,034] | IC 95 % (bloques de 2° × año) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.esa_bloques_a_gana` | 159 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_lo` | −0,064 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_hi` | −0,025 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_ic` | [−0,064; −0,025] | IC 95 % (bloques trimestre-año) como texto, TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.tuned_sin_td.ta_bloques_a_gana` | 13 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.v` | −0,026 | Brecha puntual (°C), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_lo` | −0,033 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_hi` | −0,018 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_ic` | [−0,033; −0,018] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esp_bloques_a_gana` | 41 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_lo` | −0,032 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_hi` | −0,018 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_ic` | [−0,032; −0,018] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.esa_bloques_a_gana` | 154 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_lo` | −0,039 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_hi` | −0,012 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_ic` | [−0,039; −0,012] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_rezagos_sel.ta_bloques_a_gana` | 13 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.v` | −0,041 | Brecha puntual (°C), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_lo` | −0,049 | Límite inferior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_hi` | −0,033 | Límite superior IC 95 % (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_ic` | [−0,049; −0,033] | IC 95 % (bloques espaciales de 2°) como texto, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_excluye_cero` | sí | ¿El IC (bloques espaciales de 2°) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_bloques` | 45 | Bloques del esquema (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esp_bloques_a_gana` | 43 | Bloques en que TimesFM gana (bloques espaciales de 2°), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_lo` | −0,048 | Límite inferior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_hi` | −0,033 | Límite superior IC 95 % (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_ic` | [−0,048; −0,033] | IC 95 % (bloques de 2° × año) como texto, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_excluye_cero` | sí | ¿El IC (bloques de 2° × año) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_bloques` | 180 | Bloques del esquema (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.esa_bloques_a_gana` | 167 | Bloques en que TimesFM gana (bloques de 2° × año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_lo` | −0,058 | Límite inferior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_hi` | −0,027 | Límite superior IC 95 % (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_ic` | [−0,058; −0,027] | IC 95 % (bloques trimestre-año) como texto, TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_excluye_cero` | sí | ¿El IC (bloques trimestre-año) excluye cero? TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_bloques` | 16 | Bloques del esquema (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `robustez.ll4.peru.llr_simple_sel.ta_bloques_a_gana` | 15 | Bloques en que TimesFM gana (bloques trimestre-año), TimesFM − LLR simple seleccionado, `ll4`, Perú |

## robustez_conteo

| clave | valor | significado |
|---|---|---|
| `robustez_conteo.esp.n_comparaciones` | 16 | Comparaciones (bloque × ámbito × rival) bajo bloques espaciales de 2° |
| `robustez_conteo.esp.n_excluyen` | 15 | Comparaciones cuyo IC excluye cero bajo bloques espaciales de 2° |
| `robustez_conteo.esp.texto` | 15 de 16 | «M de N» comparaciones con IC sin cero bajo bloques espaciales de 2° |
| `robustez_conteo.esp.ll4b.panel.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en el dominio completo |
| `robustez_conteo.esp.ll4b.panel.n_excluyen` | 4 | Rivales cuyo IC (bloques espaciales de 2°) excluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.esp.ll4b.panel.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques espaciales de 2°) en 2009–2012 en el dominio completo |
| `robustez_conteo.esp.ll4b.panel.incluyen` | ninguno | Rivales cuyo IC (bloques espaciales de 2°) incluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.esp.ll4b.peru.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en Perú |
| `robustez_conteo.esp.ll4b.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques espaciales de 2°) excluye cero en 2009–2012 en Perú |
| `robustez_conteo.esp.ll4b.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques espaciales de 2°) en 2009–2012 en Perú |
| `robustez_conteo.esp.ll4b.peru.incluyen` | ninguno | Rivales cuyo IC (bloques espaciales de 2°) incluye cero en 2009–2012 en Perú |
| `robustez_conteo.esp.ll4.panel.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en el dominio completo |
| `robustez_conteo.esp.ll4.panel.n_excluyen` | 3 | Rivales cuyo IC (bloques espaciales de 2°) excluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.esp.ll4.panel.texto` | 3 de 4 | «M de N» rivales con IC sin cero (bloques espaciales de 2°) en 2013–2016 en el dominio completo |
| `robustez_conteo.esp.ll4.panel.incluyen` | LLR con rezagos seleccionado | Rivales cuyo IC (bloques espaciales de 2°) incluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.esp.ll4.peru.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en Perú |
| `robustez_conteo.esp.ll4.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques espaciales de 2°) excluye cero en 2013–2016 en Perú |
| `robustez_conteo.esp.ll4.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques espaciales de 2°) en 2013–2016 en Perú |
| `robustez_conteo.esp.ll4.peru.incluyen` | ninguno | Rivales cuyo IC (bloques espaciales de 2°) incluye cero en 2013–2016 en Perú |
| `robustez_conteo.esa.n_comparaciones` | 16 | Comparaciones (bloque × ámbito × rival) bajo bloques de 2° × año |
| `robustez_conteo.esa.n_excluyen` | 15 | Comparaciones cuyo IC excluye cero bajo bloques de 2° × año |
| `robustez_conteo.esa.texto` | 15 de 16 | «M de N» comparaciones con IC sin cero bajo bloques de 2° × año |
| `robustez_conteo.esa.ll4b.panel.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en el dominio completo |
| `robustez_conteo.esa.ll4b.panel.n_excluyen` | 4 | Rivales cuyo IC (bloques de 2° × año) excluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.esa.ll4b.panel.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques de 2° × año) en 2009–2012 en el dominio completo |
| `robustez_conteo.esa.ll4b.panel.incluyen` | ninguno | Rivales cuyo IC (bloques de 2° × año) incluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.esa.ll4b.peru.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en Perú |
| `robustez_conteo.esa.ll4b.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques de 2° × año) excluye cero en 2009–2012 en Perú |
| `robustez_conteo.esa.ll4b.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques de 2° × año) en 2009–2012 en Perú |
| `robustez_conteo.esa.ll4b.peru.incluyen` | ninguno | Rivales cuyo IC (bloques de 2° × año) incluye cero en 2009–2012 en Perú |
| `robustez_conteo.esa.ll4.panel.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en el dominio completo |
| `robustez_conteo.esa.ll4.panel.n_excluyen` | 3 | Rivales cuyo IC (bloques de 2° × año) excluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.esa.ll4.panel.texto` | 3 de 4 | «M de N» rivales con IC sin cero (bloques de 2° × año) en 2013–2016 en el dominio completo |
| `robustez_conteo.esa.ll4.panel.incluyen` | LLR con rezagos seleccionado | Rivales cuyo IC (bloques de 2° × año) incluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.esa.ll4.peru.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en Perú |
| `robustez_conteo.esa.ll4.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques de 2° × año) excluye cero en 2013–2016 en Perú |
| `robustez_conteo.esa.ll4.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques de 2° × año) en 2013–2016 en Perú |
| `robustez_conteo.esa.ll4.peru.incluyen` | ninguno | Rivales cuyo IC (bloques de 2° × año) incluye cero en 2013–2016 en Perú |
| `robustez_conteo.ta.n_comparaciones` | 16 | Comparaciones (bloque × ámbito × rival) bajo bloques trimestre-año |
| `robustez_conteo.ta.n_excluyen` | 13 | Comparaciones cuyo IC excluye cero bajo bloques trimestre-año |
| `robustez_conteo.ta.texto` | 13 de 16 | «M de N» comparaciones con IC sin cero bajo bloques trimestre-año |
| `robustez_conteo.ta.ll4b.panel.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en el dominio completo |
| `robustez_conteo.ta.ll4b.panel.n_excluyen` | 4 | Rivales cuyo IC (bloques trimestre-año) excluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.ta.ll4b.panel.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques trimestre-año) en 2009–2012 en el dominio completo |
| `robustez_conteo.ta.ll4b.panel.incluyen` | ninguno | Rivales cuyo IC (bloques trimestre-año) incluye cero en 2009–2012 en el dominio completo |
| `robustez_conteo.ta.ll4b.peru.n_comparaciones` | 4 | Rivales comparados en 2009–2012 en Perú |
| `robustez_conteo.ta.ll4b.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques trimestre-año) excluye cero en 2009–2012 en Perú |
| `robustez_conteo.ta.ll4b.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques trimestre-año) en 2009–2012 en Perú |
| `robustez_conteo.ta.ll4b.peru.incluyen` | ninguno | Rivales cuyo IC (bloques trimestre-año) incluye cero en 2009–2012 en Perú |
| `robustez_conteo.ta.ll4.panel.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en el dominio completo |
| `robustez_conteo.ta.ll4.panel.n_excluyen` | 1 | Rivales cuyo IC (bloques trimestre-año) excluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.ta.ll4.panel.texto` | 1 de 4 | «M de N» rivales con IC sin cero (bloques trimestre-año) en 2013–2016 en el dominio completo |
| `robustez_conteo.ta.ll4.panel.incluyen` | tuned sin rezagos de Td, LLR con rezagos seleccionado y LLR simple seleccionado | Rivales cuyo IC (bloques trimestre-año) incluye cero en 2013–2016 en el dominio completo |
| `robustez_conteo.ta.ll4.peru.n_comparaciones` | 4 | Rivales comparados en 2013–2016 en Perú |
| `robustez_conteo.ta.ll4.peru.n_excluyen` | 4 | Rivales cuyo IC (bloques trimestre-año) excluye cero en 2013–2016 en Perú |
| `robustez_conteo.ta.ll4.peru.texto` | 4 de 4 | «M de N» rivales con IC sin cero (bloques trimestre-año) en 2013–2016 en Perú |
| `robustez_conteo.ta.ll4.peru.incluyen` | ninguno | Rivales cuyo IC (bloques trimestre-año) incluye cero en 2013–2016 en Perú |

## dm

| clave | valor | significado |
|---|---|---|
| `dm.familia` | 16 | Pruebas por regla de rezago en la familia de Holm (bloque × ámbito × rival) |
| `dm.rezago_corto` | 7 | Rezago Newey-West automático, floor(4 (T/100)^(2/9)) con T = 1.461 |
| `dm.rezago_largo` | 30 | Rezago Newey-West largo |
| `dm.ll4.panel.tuned.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.perdida_media` | −0,177 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.dm` | −3,23 | Estadístico DM, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.dm_hln` | −3,23 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.p_normal` | 0,001 | p bilateral con normal, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.p_hln` | 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.p_holm` | 0,005 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.p_holm_sci` | 5,00 × 10^−3^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.perdida_media` | −0,177 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.dm` | −2,25 | Estadístico DM, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.dm_hln` | −2,25 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.p_normal` | 0,025 | p bilateral con normal, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.p_hln` | 0,025 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.p_holm` | 0,099 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.p_holm_sci` | 9,90 × 10^−2^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned.lag30.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.perdida_media` | −0,048 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.dm` | −1,55 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.dm_hln` | −1,55 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.p_normal` | 0,121 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.p_hln` | 0,122 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.p_holm` | 0,243 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.p_holm_sci` | 2,43 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag7.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.tuned_sin_td.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.perdida_media` | −0,048 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.dm` | −1,10 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.dm_hln` | −1,10 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.p_normal` | 0,273 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.p_hln` | 0,274 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.p_holm` | 0,547 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.p_holm_sci` | 5,47 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.tuned_sin_td.lag30.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.perdida_media` | −0,007 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.dm` | −0,32 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.dm_hln` | −0,32 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.p_normal` | 0,751 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.p_hln` | 0,752 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.p_holm` | 0,752 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.p_holm_sci` | 7,52 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag7.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.perdida_media` | −0,007 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.dm` | −0,24 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.dm_hln` | −0,23 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.p_normal` | 0,814 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.p_hln` | 0,814 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.p_holm` | 0,814 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.p_holm_sci` | 8,14 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_rezagos_sel.lag30.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.perdida_media` | −0,042 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.dm` | −1,86 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.dm_hln` | −1,86 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.p_normal` | 0,063 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.p_hln` | 0,063 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.p_holm` | 0,190 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.p_holm_sci` | 1,90 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag7.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 7 |
| `dm.ll4.panel.llr_simple_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.perdida_media` | −0,042 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.dm` | −1,37 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.dm_hln` | −1,37 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.p_normal` | 0,172 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.p_hln` | 0,172 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.p_holm` | 0,516 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.p_holm_sci` | 5,16 × 10^−1^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.panel.llr_simple_sel.lag30.sig05` | no | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4`, dominio completo, rezago 30 |
| `dm.ll4.peru.tuned.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.perdida_media` | −0,143 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.dm` | −6,86 | Estadístico DM, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.dm_hln` | −6,86 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.p_holm_sci` | 1,21 × 10^−10^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.perdida_media` | −0,143 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.dm` | −4,95 | Estadístico DM, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.dm_hln` | −4,95 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.p_holm_sci` | 7,42 × 10^−6^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.perdida_media` | −0,076 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.dm` | −6,31 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.dm_hln` | −6,31 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.p_holm_sci` | 4,07 × 10^−9^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.tuned_sin_td.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.perdida_media` | −0,076 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.dm` | −4,72 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.dm_hln` | −4,72 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.p_holm_sci` | 2,11 × 10^−5^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.tuned_sin_td.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.perdida_media` | −0,045 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.dm` | −5,29 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.dm_hln` | −5,29 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.p_holm_sci` | 8,55 × 10^−7^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.perdida_media` | −0,045 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.dm` | −4,32 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.dm_hln` | −4,32 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.p_holm_sci` | 9,97 × 10^−5^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_rezagos_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.perdida_media` | −0,073 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.dm` | −7,70 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.dm_hln` | −7,70 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.p_holm_sci` | 3,61 × 10^−13^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 7 |
| `dm.ll4.peru.llr_simple_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.perdida_media` | −0,073 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.dm` | −5,74 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.dm_hln` | −5,73 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.p_holm_sci` | 1,55 × 10^−7^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4.peru.llr_simple_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4`, Perú, rezago 30 |
| `dm.ll4b.panel.tuned.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.perdida_media` | −0,164 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.dm` | −6,03 | Estadístico DM, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.dm_hln` | −6,03 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.p_holm_sci` | 1,68 × 10^−8^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.perdida_media` | −0,164 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.dm` | −5,17 | Estadístico DM, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.dm_hln` | −5,17 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.p_holm_sci` | 2,67 × 10^−6^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.perdida_media` | −0,134 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.dm` | −6,24 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.dm_hln` | −6,24 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.p_holm_sci` | 5,21 × 10^−9^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.tuned_sin_td.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.perdida_media` | −0,134 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.dm` | −5,46 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.dm_hln` | −5,46 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.p_holm_sci` | 6,80 × 10^−7^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.tuned_sin_td.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.perdida_media` | −0,060 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.dm` | −3,78 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.dm_hln` | −3,77 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.p_holm_sci` | 8,32 × 10^−4^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.perdida_media` | −0,060 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.dm` | −3,40 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.dm_hln` | −3,40 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.p_holm` | 0,004 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.p_holm_sci` | 3,50 × 10^−3^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_rezagos_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.perdida_media` | −0,078 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.dm` | −5,57 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.dm_hln` | −5,57 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.p_holm_sci` | 2,11 × 10^−7^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 7 |
| `dm.ll4b.panel.llr_simple_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.perdida_media` | −0,078 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.dm` | −4,54 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.dm_hln` | −4,54 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.p_holm_sci` | 4,28 × 10^−5^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.panel.llr_simple_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4b`, dominio completo, rezago 30 |
| `dm.ll4b.peru.tuned.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.perdida_media` | −0,094 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.dm` | −7,47 | Estadístico DM, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.dm_hln` | −7,46 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.p_holm_sci` | 1,86 × 10^−12^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.perdida_media` | −0,094 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.dm` | −5,89 | Estadístico DM, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.dm_hln` | −5,89 | Estadístico DM con corrección HLN, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.p_holm_sci` | 6,82 × 10^−8^ | p ajustado por Holm en notación científica, TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.perdida_media` | −0,086 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.dm` | −8,64 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.dm_hln` | −8,64 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.p_holm_sci` | 2,38 × 10^−16^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.tuned_sin_td.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.perdida_media` | −0,086 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.dm` | −7,12 | Estadístico DM, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.dm_hln` | −7,12 | Estadístico DM con corrección HLN, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.p_holm_sci` | 2,65 × 10^−11^ | p ajustado por Holm en notación científica, TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.tuned_sin_td.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − tuned sin rezagos de Td, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.perdida_media` | −0,041 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.dm` | −6,28 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.dm_hln` | −6,27 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.p_holm_sci` | 4,61 × 10^−9^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.perdida_media` | −0,041 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.dm` | −5,20 | Estadístico DM, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.dm_hln` | −5,20 | Estadístico DM con corrección HLN, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.p_holm_sci` | 2,54 × 10^−6^ | p ajustado por Holm en notación científica, TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_rezagos_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag7.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.perdida_media` | −0,049 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.dm` | −8,22 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.dm_hln` | −8,21 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.p_holm_sci` | 7,03 × 10^−15^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag7.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 7 |
| `dm.ll4b.peru.llr_simple_sel.lag30.T` | 1.461 | Días de la serie diaria de diferencial de pérdida, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.perdida_media` | −0,049 | Diferencial medio diario de error cuadrático medio por celda (°C²), TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.dm` | −6,31 | Estadístico DM, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.dm_hln` | −6,31 | Estadístico DM con corrección HLN, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.p_normal` | < 0,001 | p bilateral con normal, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.p_hln` | < 0,001 | p bilateral HLN (t de T−1 gl), sin ajuste, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.p_holm` | < 0,001 | p HLN ajustado por Holm sobre la familia de 16, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.p_holm_sci` | 5,59 × 10^−9^ | p ajustado por Holm en notación científica, TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |
| `dm.ll4b.peru.llr_simple_sel.lag30.sig05` | sí | ¿p de Holm menor que 0,05? TimesFM − LLR simple seleccionado, `ll4b`, Perú, rezago 30 |

## dm_conteo

| clave | valor | significado |
|---|---|---|
| `dm_conteo.lag7.n` | 16 | Pruebas DM con rezago 7 |
| `dm_conteo.lag7.n_holm05` | 13 | Pruebas DM con rezago 7 y p de Holm menor que 0,05 |
| `dm_conteo.lag7.texto` | 13 de 16 | «M de N» pruebas DM con p de Holm menor que 0,05 (rezago 7) |
| `dm_conteo.lag7.ll4b.panel.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2009–2012 en el dominio completo, rezago 7 |
| `dm_conteo.lag7.ll4b.panel.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2009–2012 en el dominio completo, rezago 7 |
| `dm_conteo.lag7.ll4b.peru.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2009–2012 en Perú, rezago 7 |
| `dm_conteo.lag7.ll4b.peru.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2009–2012 en Perú, rezago 7 |
| `dm_conteo.lag7.ll4.panel.n_holm05` | 1 | Rivales con p de Holm menor que 0,05 en 2013–2016 en el dominio completo, rezago 7 |
| `dm_conteo.lag7.ll4.panel.no_signif` | tuned sin rezagos de Td, LLR con rezagos seleccionado y LLR simple seleccionado | Rivales sin significancia (p de Holm ≥ 0,05) en 2013–2016 en el dominio completo, rezago 7 |
| `dm_conteo.lag7.ll4.peru.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2013–2016 en Perú, rezago 7 |
| `dm_conteo.lag7.ll4.peru.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2013–2016 en Perú, rezago 7 |
| `dm_conteo.lag30.n` | 16 | Pruebas DM con rezago 30 |
| `dm_conteo.lag30.n_holm05` | 12 | Pruebas DM con rezago 30 y p de Holm menor que 0,05 |
| `dm_conteo.lag30.texto` | 12 de 16 | «M de N» pruebas DM con p de Holm menor que 0,05 (rezago 30) |
| `dm_conteo.lag30.ll4b.panel.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2009–2012 en el dominio completo, rezago 30 |
| `dm_conteo.lag30.ll4b.panel.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2009–2012 en el dominio completo, rezago 30 |
| `dm_conteo.lag30.ll4b.peru.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2009–2012 en Perú, rezago 30 |
| `dm_conteo.lag30.ll4b.peru.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2009–2012 en Perú, rezago 30 |
| `dm_conteo.lag30.ll4.panel.n_holm05` | 0 | Rivales con p de Holm menor que 0,05 en 2013–2016 en el dominio completo, rezago 30 |
| `dm_conteo.lag30.ll4.panel.no_signif` | tuned, tuned sin rezagos de Td, LLR con rezagos seleccionado y LLR simple seleccionado | Rivales sin significancia (p de Holm ≥ 0,05) en 2013–2016 en el dominio completo, rezago 30 |
| `dm_conteo.lag30.ll4.peru.n_holm05` | 4 | Rivales con p de Holm menor que 0,05 en 2013–2016 en Perú, rezago 30 |
| `dm_conteo.lag30.ll4.peru.no_signif` | ninguno | Rivales sin significancia (p de Holm ≥ 0,05) en 2013–2016 en Perú, rezago 30 |

## skill

| clave | valor | significado |
|---|---|---|
| `skill.ll4.panel.timesfm.skill` | 0,435 | Habilidad 1 − MSE/MSE(climatología), TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.timesfm.razon_varianza` | 0,372 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.timesfm.razon_desv` | 0,610 | Razón de desviaciones estándar de las anomalías, TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.timesfm.skill_celda_media` | 0,486 | Media entre celdas de la habilidad por celda, TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.timesfm.skill_celda_mediana` | 0,464 | Mediana entre celdas de la habilidad por celda, TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.timesfm.corr` | 0,638 | Correlación de las anomalías predicha y observada, TimesFM, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.skill` | 0,360 | Habilidad 1 − MSE/MSE(climatología), tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.razon_varianza` | 0,221 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.razon_desv` | 0,470 | Razón de desviaciones estándar de las anomalías, tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.skill_celda_media` | 0,407 | Media entre celdas de la habilidad por celda, tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.skill_celda_mediana` | 0,380 | Mediana entre celdas de la habilidad por celda, tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned.corr` | 0,578 | Correlación de las anomalías predicha y observada, tuned, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.skill` | 0,415 | Habilidad 1 − MSE/MSE(climatología), tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.razon_varianza` | 0,335 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.razon_desv` | 0,579 | Razón de desviaciones estándar de las anomalías, tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.skill_celda_media` | 0,452 | Media entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.skill_celda_mediana` | 0,427 | Mediana entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.tuned_sin_td.corr` | 0,618 | Correlación de las anomalías predicha y observada, tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.skill` | 0,432 | Habilidad 1 − MSE/MSE(climatología), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.razon_varianza` | 0,337 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.razon_desv` | 0,581 | Razón de desviaciones estándar de las anomalías, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.skill_celda_media` | 0,469 | Media entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.skill_celda_mediana` | 0,443 | Mediana entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_rezagos_sel.corr` | 0,634 | Correlación de las anomalías predicha y observada, LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.skill` | 0,417 | Habilidad 1 − MSE/MSE(climatología), LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.razon_varianza` | 0,325 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.razon_desv` | 0,570 | Razón de desviaciones estándar de las anomalías, LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.skill_celda_media` | 0,451 | Media entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.skill_celda_mediana` | 0,425 | Mediana entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.llr_simple_sel.corr` | 0,621 | Correlación de las anomalías predicha y observada, LLR simple seleccionado, `ll4`, dominio completo |
| `skill.ll4.panel.clim.skill` | 0,000 | Habilidad 1 − MSE/MSE(climatología), climatología, `ll4`, dominio completo |
| `skill.ll4.panel.clim.razon_varianza` | 0,000 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), climatología, `ll4`, dominio completo |
| `skill.ll4.panel.clim.razon_desv` | 0,000 | Razón de desviaciones estándar de las anomalías, climatología, `ll4`, dominio completo |
| `skill.ll4.panel.clim.skill_celda_media` | 0,000 | Media entre celdas de la habilidad por celda, climatología, `ll4`, dominio completo |
| `skill.ll4.panel.clim.skill_celda_mediana` | 0,000 | Mediana entre celdas de la habilidad por celda, climatología, `ll4`, dominio completo |
| `skill.ll4.peru.timesfm.skill` | 0,530 | Habilidad 1 − MSE/MSE(climatología), TimesFM, `ll4`, Perú |
| `skill.ll4.peru.timesfm.razon_varianza` | 0,425 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), TimesFM, `ll4`, Perú |
| `skill.ll4.peru.timesfm.razon_desv` | 0,652 | Razón de desviaciones estándar de las anomalías, TimesFM, `ll4`, Perú |
| `skill.ll4.peru.timesfm.skill_celda_media` | 0,546 | Media entre celdas de la habilidad por celda, TimesFM, `ll4`, Perú |
| `skill.ll4.peru.timesfm.skill_celda_mediana` | 0,540 | Mediana entre celdas de la habilidad por celda, TimesFM, `ll4`, Perú |
| `skill.ll4.peru.timesfm.corr` | 0,712 | Correlación de las anomalías predicha y observada, TimesFM, `ll4`, Perú |
| `skill.ll4.peru.tuned.skill` | 0,440 | Habilidad 1 − MSE/MSE(climatología), tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned.razon_varianza` | 0,270 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned.razon_desv` | 0,520 | Razón de desviaciones estándar de las anomalías, tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned.skill_celda_media` | 0,457 | Media entre celdas de la habilidad por celda, tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned.skill_celda_mediana` | 0,447 | Mediana entre celdas de la habilidad por celda, tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned.corr` | 0,651 | Correlación de las anomalías predicha y observada, tuned, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.skill` | 0,482 | Habilidad 1 − MSE/MSE(climatología), tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.razon_varianza` | 0,409 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.razon_desv` | 0,640 | Razón de desviaciones estándar de las anomalías, tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.skill_celda_media` | 0,494 | Media entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.skill_celda_mediana` | 0,485 | Mediana entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.tuned_sin_td.corr` | 0,674 | Correlación de las anomalías predicha y observada, tuned sin rezagos de Td, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.skill` | 0,502 | Habilidad 1 − MSE/MSE(climatología), LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.razon_varianza` | 0,410 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.razon_desv` | 0,641 | Razón de desviaciones estándar de las anomalías, LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.skill_celda_media` | 0,511 | Media entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.skill_celda_mediana` | 0,501 | Mediana entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_rezagos_sel.corr` | 0,689 | Correlación de las anomalías predicha y observada, LLR con rezagos seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.skill` | 0,484 | Habilidad 1 − MSE/MSE(climatología), LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.razon_varianza` | 0,393 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.razon_desv` | 0,627 | Razón de desviaciones estándar de las anomalías, LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.skill_celda_media` | 0,489 | Media entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.skill_celda_mediana` | 0,479 | Mediana entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.llr_simple_sel.corr` | 0,675 | Correlación de las anomalías predicha y observada, LLR simple seleccionado, `ll4`, Perú |
| `skill.ll4.peru.clim.skill` | 0,000 | Habilidad 1 − MSE/MSE(climatología), climatología, `ll4`, Perú |
| `skill.ll4.peru.clim.razon_varianza` | 0,000 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), climatología, `ll4`, Perú |
| `skill.ll4.peru.clim.razon_desv` | 0,000 | Razón de desviaciones estándar de las anomalías, climatología, `ll4`, Perú |
| `skill.ll4.peru.clim.skill_celda_media` | 0,000 | Media entre celdas de la habilidad por celda, climatología, `ll4`, Perú |
| `skill.ll4.peru.clim.skill_celda_mediana` | 0,000 | Mediana entre celdas de la habilidad por celda, climatología, `ll4`, Perú |
| `skill.ll4b.panel.timesfm.skill` | 0,410 | Habilidad 1 − MSE/MSE(climatología), TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.timesfm.razon_varianza` | 0,456 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.timesfm.razon_desv` | 0,675 | Razón de desviaciones estándar de las anomalías, TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.timesfm.skill_celda_media` | 0,422 | Media entre celdas de la habilidad por celda, TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.timesfm.skill_celda_mediana` | 0,375 | Mediana entre celdas de la habilidad por celda, TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.timesfm.corr` | 0,624 | Correlación de las anomalías predicha y observada, TimesFM, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.skill` | 0,321 | Habilidad 1 − MSE/MSE(climatología), tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.razon_varianza` | 0,282 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.razon_desv` | 0,531 | Razón de desviaciones estándar de las anomalías, tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.skill_celda_media` | 0,341 | Media entre celdas de la habilidad por celda, tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.skill_celda_mediana` | 0,289 | Mediana entre celdas de la habilidad por celda, tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned.corr` | 0,548 | Correlación de las anomalías predicha y observada, tuned, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.skill` | 0,338 | Habilidad 1 − MSE/MSE(climatología), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.razon_varianza` | 0,421 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.razon_desv` | 0,649 | Razón de desviaciones estándar de las anomalías, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.skill_celda_media` | 0,352 | Media entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.skill_celda_mediana` | 0,301 | Mediana entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.tuned_sin_td.corr` | 0,565 | Correlación de las anomalías predicha y observada, tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.skill` | 0,377 | Habilidad 1 − MSE/MSE(climatología), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.razon_varianza` | 0,435 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.razon_desv` | 0,660 | Razón de desviaciones estándar de las anomalías, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.skill_celda_media` | 0,388 | Media entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.skill_celda_mediana` | 0,343 | Mediana entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_rezagos_sel.corr` | 0,598 | Correlación de las anomalías predicha y observada, LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.skill` | 0,367 | Habilidad 1 − MSE/MSE(climatología), LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.razon_varianza` | 0,422 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.razon_desv` | 0,650 | Razón de desviaciones estándar de las anomalías, LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.skill_celda_media` | 0,378 | Media entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.skill_celda_mediana` | 0,333 | Mediana entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.llr_simple_sel.corr` | 0,591 | Correlación de las anomalías predicha y observada, LLR simple seleccionado, `ll4b`, dominio completo |
| `skill.ll4b.panel.clim.skill` | 0,000 | Habilidad 1 − MSE/MSE(climatología), climatología, `ll4b`, dominio completo |
| `skill.ll4b.panel.clim.razon_varianza` | 0,000 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), climatología, `ll4b`, dominio completo |
| `skill.ll4b.panel.clim.razon_desv` | 0,000 | Razón de desviaciones estándar de las anomalías, climatología, `ll4b`, dominio completo |
| `skill.ll4b.panel.clim.skill_celda_media` | 0,000 | Media entre celdas de la habilidad por celda, climatología, `ll4b`, dominio completo |
| `skill.ll4b.panel.clim.skill_celda_mediana` | 0,000 | Mediana entre celdas de la habilidad por celda, climatología, `ll4b`, dominio completo |
| `skill.ll4b.peru.timesfm.skill` | 0,453 | Habilidad 1 − MSE/MSE(climatología), TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.timesfm.razon_varianza` | 0,534 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.timesfm.razon_desv` | 0,731 | Razón de desviaciones estándar de las anomalías, TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.timesfm.skill_celda_media` | 0,443 | Media entre celdas de la habilidad por celda, TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.timesfm.skill_celda_mediana` | 0,386 | Mediana entre celdas de la habilidad por celda, TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.timesfm.corr` | 0,666 | Correlación de las anomalías predicha y observada, TimesFM, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.skill` | 0,373 | Habilidad 1 − MSE/MSE(climatología), tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.razon_varianza` | 0,344 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.razon_desv` | 0,586 | Razón de desviaciones estándar de las anomalías, tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.skill_celda_media` | 0,369 | Media entre celdas de la habilidad por celda, tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.skill_celda_mediana` | 0,319 | Mediana entre celdas de la habilidad por celda, tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned.corr` | 0,595 | Correlación de las anomalías predicha y observada, tuned, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.skill` | 0,380 | Habilidad 1 − MSE/MSE(climatología), tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.razon_varianza` | 0,522 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.razon_desv` | 0,723 | Razón de desviaciones estándar de las anomalías, tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.skill_celda_media` | 0,371 | Media entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.skill_celda_mediana` | 0,311 | Mediana entre celdas de la habilidad por celda, tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.tuned_sin_td.corr` | 0,610 | Correlación de las anomalías predicha y observada, tuned sin rezagos de Td, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.skill` | 0,418 | Habilidad 1 − MSE/MSE(climatología), LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.razon_varianza` | 0,531 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.razon_desv` | 0,729 | Razón de desviaciones estándar de las anomalías, LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.skill_celda_media` | 0,405 | Media entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.skill_celda_mediana` | 0,348 | Mediana entre celdas de la habilidad por celda, LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_rezagos_sel.corr` | 0,639 | Correlación de las anomalías predicha y observada, LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.skill` | 0,412 | Habilidad 1 − MSE/MSE(climatología), LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.razon_varianza` | 0,516 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.razon_desv` | 0,718 | Razón de desviaciones estándar de las anomalías, LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.skill_celda_media` | 0,398 | Media entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.skill_celda_mediana` | 0,347 | Mediana entre celdas de la habilidad por celda, LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.llr_simple_sel.corr` | 0,635 | Correlación de las anomalías predicha y observada, LLR simple seleccionado, `ll4b`, Perú |
| `skill.ll4b.peru.clim.skill` | 0,000 | Habilidad 1 − MSE/MSE(climatología), climatología, `ll4b`, Perú |
| `skill.ll4b.peru.clim.razon_varianza` | 0,000 | Razón de varianzas (varianza de la anomalía predicha / varianza de la anomalía observada), climatología, `ll4b`, Perú |
| `skill.ll4b.peru.clim.razon_desv` | 0,000 | Razón de desviaciones estándar de las anomalías, climatología, `ll4b`, Perú |
| `skill.ll4b.peru.clim.skill_celda_media` | 0,000 | Media entre celdas de la habilidad por celda, climatología, `ll4b`, Perú |
| `skill.ll4b.peru.clim.skill_celda_mediana` | 0,000 | Mediana entre celdas de la habilidad por celda, climatología, `ll4b`, Perú |
| `skill.ll4b.panel.mse_clim` | 1,855 | MSE de la climatología (°C²), `ll4b`, dominio completo |
| `skill.ll4b.panel.mse_timesfm` | 1,095 | MSE de TimesFM (°C²), `ll4b`, dominio completo |
| `skill.ll4b.peru.mse_clim` | 1,182 | MSE de la climatología (°C²), `ll4b`, Perú |
| `skill.ll4b.peru.mse_timesfm` | 0,647 | MSE de TimesFM (°C²), `ll4b`, Perú |
| `skill.ll4.panel.mse_clim` | 2,357 | MSE de la climatología (°C²), `ll4`, dominio completo |
| `skill.ll4.panel.mse_timesfm` | 1,331 | MSE de TimesFM (°C²), `ll4`, dominio completo |
| `skill.ll4.peru.mse_clim` | 1,592 | MSE de la climatología (°C²), `ll4`, Perú |
| `skill.ll4.peru.mse_timesfm` | 0,748 | MSE de TimesFM (°C²), `ll4`, Perú |

## skill_dif

| clave | valor | significado |
|---|---|---|
| `skill_dif.ll4b.panel.timesfm_vs_tuned.skill` | +0,089 | Habilidad de TimesFM − habilidad de tuned, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_tuned.razon_varianza` | +0,174 | Razón de varianzas de TimesFM − la de tuned, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_tuned.corr` | +0,075 | Correlación de anomalías de TimesFM − la de tuned, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_tuned_sin_td.skill` | +0,072 | Habilidad de TimesFM − habilidad de tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_tuned_sin_td.razon_varianza` | +0,035 | Razón de varianzas de TimesFM − la de tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_tuned_sin_td.corr` | +0,058 | Correlación de anomalías de TimesFM − la de tuned sin rezagos de Td, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_rezagos_sel.skill` | +0,032 | Habilidad de TimesFM − habilidad de LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_rezagos_sel.razon_varianza` | +0,021 | Razón de varianzas de TimesFM − la de LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_rezagos_sel.corr` | +0,026 | Correlación de anomalías de TimesFM − la de LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_simple_sel.skill` | +0,042 | Habilidad de TimesFM − habilidad de LLR simple seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_simple_sel.razon_varianza` | +0,033 | Razón de varianzas de TimesFM − la de LLR simple seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.panel.timesfm_vs_llr_simple_sel.corr` | +0,033 | Correlación de anomalías de TimesFM − la de LLR simple seleccionado, `ll4b`, dominio completo |
| `skill_dif.ll4b.peru.timesfm_vs_tuned.skill` | +0,080 | Habilidad de TimesFM − habilidad de tuned, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_tuned.razon_varianza` | +0,190 | Razón de varianzas de TimesFM − la de tuned, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_tuned.corr` | +0,071 | Correlación de anomalías de TimesFM − la de tuned, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_tuned_sin_td.skill` | +0,072 | Habilidad de TimesFM − habilidad de tuned sin rezagos de Td, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_tuned_sin_td.razon_varianza` | +0,012 | Razón de varianzas de TimesFM − la de tuned sin rezagos de Td, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_tuned_sin_td.corr` | +0,056 | Correlación de anomalías de TimesFM − la de tuned sin rezagos de Td, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_rezagos_sel.skill` | +0,035 | Habilidad de TimesFM − habilidad de LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_rezagos_sel.razon_varianza` | +0,003 | Razón de varianzas de TimesFM − la de LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_rezagos_sel.corr` | +0,027 | Correlación de anomalías de TimesFM − la de LLR con rezagos seleccionado, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_simple_sel.skill` | +0,041 | Habilidad de TimesFM − habilidad de LLR simple seleccionado, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_simple_sel.razon_varianza` | +0,018 | Razón de varianzas de TimesFM − la de LLR simple seleccionado, `ll4b`, Perú |
| `skill_dif.ll4b.peru.timesfm_vs_llr_simple_sel.corr` | +0,031 | Correlación de anomalías de TimesFM − la de LLR simple seleccionado, `ll4b`, Perú |
| `skill_dif.ll4.panel.timesfm_vs_tuned.skill` | +0,075 | Habilidad de TimesFM − habilidad de tuned, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_tuned.razon_varianza` | +0,151 | Razón de varianzas de TimesFM − la de tuned, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_tuned.corr` | +0,060 | Correlación de anomalías de TimesFM − la de tuned, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_tuned_sin_td.skill` | +0,020 | Habilidad de TimesFM − habilidad de tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_tuned_sin_td.razon_varianza` | +0,036 | Razón de varianzas de TimesFM − la de tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_tuned_sin_td.corr` | +0,020 | Correlación de anomalías de TimesFM − la de tuned sin rezagos de Td, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_rezagos_sel.skill` | +0,003 | Habilidad de TimesFM − habilidad de LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_rezagos_sel.razon_varianza` | +0,034 | Razón de varianzas de TimesFM − la de LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_rezagos_sel.corr` | +0,004 | Correlación de anomalías de TimesFM − la de LLR con rezagos seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_simple_sel.skill` | +0,018 | Habilidad de TimesFM − habilidad de LLR simple seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_simple_sel.razon_varianza` | +0,047 | Razón de varianzas de TimesFM − la de LLR simple seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.panel.timesfm_vs_llr_simple_sel.corr` | +0,018 | Correlación de anomalías de TimesFM − la de LLR simple seleccionado, `ll4`, dominio completo |
| `skill_dif.ll4.peru.timesfm_vs_tuned.skill` | +0,090 | Habilidad de TimesFM − habilidad de tuned, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_tuned.razon_varianza` | +0,154 | Razón de varianzas de TimesFM − la de tuned, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_tuned.corr` | +0,061 | Correlación de anomalías de TimesFM − la de tuned, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_tuned_sin_td.skill` | +0,048 | Habilidad de TimesFM − habilidad de tuned sin rezagos de Td, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_tuned_sin_td.razon_varianza` | +0,015 | Razón de varianzas de TimesFM − la de tuned sin rezagos de Td, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_tuned_sin_td.corr` | +0,038 | Correlación de anomalías de TimesFM − la de tuned sin rezagos de Td, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_rezagos_sel.skill` | +0,028 | Habilidad de TimesFM − habilidad de LLR con rezagos seleccionado, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_rezagos_sel.razon_varianza` | +0,014 | Razón de varianzas de TimesFM − la de LLR con rezagos seleccionado, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_rezagos_sel.corr` | +0,023 | Correlación de anomalías de TimesFM − la de LLR con rezagos seleccionado, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_simple_sel.skill` | +0,046 | Habilidad de TimesFM − habilidad de LLR simple seleccionado, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_simple_sel.razon_varianza` | +0,031 | Razón de varianzas de TimesFM − la de LLR simple seleccionado, `ll4`, Perú |
| `skill_dif.ll4.peru.timesfm_vs_llr_simple_sel.corr` | +0,037 | Correlación de anomalías de TimesFM − la de LLR simple seleccionado, `ll4`, Perú |

## skill_max

| clave | valor | significado |
|---|---|---|
| `skill_max.ll4b.panel.razon_varianza` | TimesFM | Método con mayor razón de varianzas, `ll4b`, dominio completo |
| `skill_max.ll4b.panel.corr` | TimesFM | Método con mayor correlación de anomalías, `ll4b`, dominio completo |
| `skill_max.ll4b.peru.razon_varianza` | TimesFM | Método con mayor razón de varianzas, `ll4b`, Perú |
| `skill_max.ll4b.peru.corr` | TimesFM | Método con mayor correlación de anomalías, `ll4b`, Perú |
| `skill_max.ll4.panel.razon_varianza` | TimesFM | Método con mayor razón de varianzas, `ll4`, dominio completo |
| `skill_max.ll4.panel.corr` | TimesFM | Método con mayor correlación de anomalías, `ll4`, dominio completo |
| `skill_max.ll4.peru.razon_varianza` | TimesFM | Método con mayor razón de varianzas, `ll4`, Perú |
| `skill_max.ll4.peru.corr` | TimesFM | Método con mayor correlación de anomalías, `ll4`, Perú |

## extremos

| clave | valor | significado |
|---|---|---|
| `extremos.ll4.panel.inf5.timesfm.rmse` | 2,164 | RMSE (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.timesfm.sesgo` | +1,792 | Sesgo (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.n` | 1.260.027 | Filas celda × día, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.tuned.rmse` | 2,246 | RMSE (°C), tuned, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.tuned.sesgo` | +1,943 | Sesgo (°C), tuned, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.tuned_sin_td.rmse` | 2,117 | RMSE (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.tuned_sin_td.sesgo` | +1,721 | Sesgo (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.llr_rezagos_sel.rmse` | 2,131 | RMSE (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.llr_rezagos_sel.sesgo` | +1,747 | Sesgo (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.llr_simple_sel.rmse` | 2,140 | RMSE (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.llr_simple_sel.sesgo` | +1,743 | Sesgo (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.clim.rmse` | 2,707 | RMSE (°C), climatología, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.clim.sesgo` | +2,485 | Sesgo (°C), climatología, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.timesfm.rmse` | 2,218 | RMSE (°C), TimesFM, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.timesfm.sesgo` | −1,843 | Sesgo (°C), TimesFM, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.n` | 1.260.026 | Filas celda × día, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.tuned.rmse` | 2,791 | RMSE (°C), tuned, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.tuned.sesgo` | −2,326 | Sesgo (°C), tuned, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.tuned_sin_td.rmse` | 2,455 | RMSE (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.tuned_sin_td.sesgo` | −1,995 | Sesgo (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.llr_rezagos_sel.rmse` | 2,361 | RMSE (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.llr_rezagos_sel.sesgo` | −1,959 | Sesgo (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.llr_simple_sel.rmse` | 2,431 | RMSE (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.llr_simple_sel.sesgo` | −2,047 | Sesgo (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.clim.rmse` | 3,762 | RMSE (°C), climatología, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.clim.sesgo` | −3,440 | Sesgo (°C), climatología, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.timesfm.rmse` | 0,969 | RMSE (°C), TimesFM, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.timesfm.sesgo` | +0,119 | Sesgo (°C), TimesFM, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.n` | 22.356.394 | Filas celda × día, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.tuned.rmse` | 0,977 | RMSE (°C), tuned, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.tuned.sesgo` | −0,015 | Sesgo (°C), tuned, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.tuned_sin_td.rmse` | 0,971 | RMSE (°C), tuned sin rezagos de Td, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.tuned_sin_td.sesgo` | +0,031 | Sesgo (°C), tuned sin rezagos de Td, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.llr_rezagos_sel.rmse` | 0,958 | RMSE (°C), LLR con rezagos seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.llr_rezagos_sel.sesgo` | +0,052 | Sesgo (°C), LLR con rezagos seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.llr_simple_sel.rmse` | 0,968 | RMSE (°C), LLR simple seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.llr_simple_sel.sesgo` | +0,015 | Sesgo (°C), LLR simple seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.clim.rmse` | 1,188 | RMSE (°C), climatología, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.clim.sesgo` | −0,350 | Sesgo (°C), climatología, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.peru.inf5.timesfm.rmse` | 1,632 | RMSE (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.timesfm.sesgo` | +1,360 | Sesgo (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.n` | 612.143 | Filas celda × día, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.tuned.rmse` | 1,837 | RMSE (°C), tuned, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.tuned.sesgo` | +1,605 | Sesgo (°C), tuned, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.tuned_sin_td.rmse` | 1,712 | RMSE (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.tuned_sin_td.sesgo` | +1,405 | Sesgo (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.llr_rezagos_sel.rmse` | 1,686 | RMSE (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.llr_rezagos_sel.sesgo` | +1,391 | Sesgo (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.llr_simple_sel.rmse` | 1,668 | RMSE (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.llr_simple_sel.sesgo` | +1,365 | Sesgo (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.clim.rmse` | 2,330 | RMSE (°C), climatología, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.clim.sesgo` | +2,134 | Sesgo (°C), climatología, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.timesfm.rmse` | 1,615 | RMSE (°C), TimesFM, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.timesfm.sesgo` | −1,351 | Sesgo (°C), TimesFM, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.n` | 612.142 | Filas celda × día, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.tuned.rmse` | 1,941 | RMSE (°C), tuned, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.tuned.sesgo` | −1,634 | Sesgo (°C), tuned, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.tuned_sin_td.rmse` | 1,699 | RMSE (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.tuned_sin_td.sesgo` | −1,361 | Sesgo (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.llr_rezagos_sel.rmse` | 1,673 | RMSE (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.llr_rezagos_sel.sesgo` | −1,377 | Sesgo (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.llr_simple_sel.rmse` | 1,762 | RMSE (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.llr_simple_sel.sesgo` | −1,478 | Sesgo (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.clim.rmse` | 2,917 | RMSE (°C), climatología, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.clim.sesgo` | −2,723 | Sesgo (°C), climatología, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.resto.timesfm.rmse` | 0,732 | RMSE (°C), TimesFM, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.timesfm.sesgo` | +0,055 | Sesgo (°C), TimesFM, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.n` | 10.861.107 | Filas celda × día, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.tuned.rmse` | 0,768 | RMSE (°C), tuned, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.tuned.sesgo` | +0,012 | Sesgo (°C), tuned, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.tuned_sin_td.rmse` | 0,768 | RMSE (°C), tuned sin rezagos de Td, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.tuned_sin_td.sesgo` | +0,050 | Sesgo (°C), tuned sin rezagos de Td, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.llr_rezagos_sel.rmse` | 0,752 | RMSE (°C), LLR con rezagos seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.llr_rezagos_sel.sesgo` | +0,037 | Sesgo (°C), LLR con rezagos seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.llr_simple_sel.rmse` | 0,763 | RMSE (°C), LLR simple seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.llr_simple_sel.sesgo` | −0,009 | Sesgo (°C), LLR simple seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.clim.rmse` | 0,993 | RMSE (°C), climatología, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.clim.sesgo` | −0,301 | Sesgo (°C), climatología, 90 % central, `ll4`, Perú |
| `extremos.ll4b.panel.inf5.timesfm.rmse` | 1,693 | RMSE (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.timesfm.sesgo` | +1,369 | Sesgo (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.n` | 1.260.038 | Filas celda × día, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.tuned.rmse` | 1,902 | RMSE (°C), tuned, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.tuned.sesgo` | +1,612 | Sesgo (°C), tuned, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.tuned_sin_td.rmse` | 1,828 | RMSE (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.tuned_sin_td.sesgo` | +1,452 | Sesgo (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.llr_rezagos_sel.rmse` | 1,767 | RMSE (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.llr_rezagos_sel.sesgo` | +1,402 | Sesgo (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.llr_simple_sel.rmse` | 1,775 | RMSE (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.llr_simple_sel.sesgo` | +1,408 | Sesgo (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.clim.rmse` | 2,504 | RMSE (°C), climatología, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.clim.sesgo` | +2,301 | Sesgo (°C), climatología, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.timesfm.rmse` | 1,978 | RMSE (°C), TimesFM, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.timesfm.sesgo` | −1,642 | Sesgo (°C), TimesFM, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.n` | 1.260.029 | Filas celda × día, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.tuned.rmse` | 2,337 | RMSE (°C), tuned, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.tuned.sesgo` | −1,987 | Sesgo (°C), tuned, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.tuned_sin_td.rmse` | 2,158 | RMSE (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.tuned_sin_td.sesgo` | −1,753 | Sesgo (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.llr_rezagos_sel.rmse` | 2,088 | RMSE (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.llr_rezagos_sel.sesgo` | −1,715 | Sesgo (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.llr_simple_sel.rmse` | 2,113 | RMSE (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.llr_simple_sel.sesgo` | −1,748 | Sesgo (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.clim.rmse` | 3,104 | RMSE (°C), climatología, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.clim.sesgo` | −2,849 | Sesgo (°C), climatología, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.timesfm.rmse` | 0,914 | RMSE (°C), TimesFM, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.timesfm.sesgo` | −0,104 | Sesgo (°C), TimesFM, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.n` | 22.356.380 | Filas celda × día, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.tuned.rmse` | 0,943 | RMSE (°C), tuned, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.tuned.sesgo` | −0,153 | Sesgo (°C), tuned, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.tuned_sin_td.rmse` | 0,957 | RMSE (°C), tuned sin rezagos de Td, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.tuned_sin_td.sesgo` | −0,121 | Sesgo (°C), tuned sin rezagos de Td, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.llr_rezagos_sel.rmse` | 0,929 | RMSE (°C), LLR con rezagos seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.llr_rezagos_sel.sesgo` | −0,113 | Sesgo (°C), LLR con rezagos seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.llr_simple_sel.rmse` | 0,936 | RMSE (°C), LLR simple seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.llr_simple_sel.sesgo` | −0,134 | Sesgo (°C), LLR simple seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.clim.rmse` | 1,080 | RMSE (°C), climatología, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.clim.sesgo` | −0,303 | Sesgo (°C), climatología, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.peru.inf5.timesfm.rmse` | 1,285 | RMSE (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.timesfm.sesgo` | +1,030 | Sesgo (°C), TimesFM, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.n` | 612.151 | Filas celda × día, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.tuned.rmse` | 1,543 | RMSE (°C), tuned, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.tuned.sesgo` | +1,327 | Sesgo (°C), tuned, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.tuned_sin_td.rmse` | 1,453 | RMSE (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.tuned_sin_td.sesgo` | +1,162 | Sesgo (°C), tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.llr_rezagos_sel.rmse` | 1,374 | RMSE (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.llr_rezagos_sel.sesgo` | +1,096 | Sesgo (°C), LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.llr_simple_sel.rmse` | 1,368 | RMSE (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.llr_simple_sel.sesgo` | +1,090 | Sesgo (°C), LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.clim.rmse` | 2,128 | RMSE (°C), climatología, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.clim.sesgo` | +1,969 | Sesgo (°C), climatología, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.timesfm.rmse` | 1,477 | RMSE (°C), TimesFM, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.timesfm.sesgo` | −1,244 | Sesgo (°C), TimesFM, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.n` | 612.146 | Filas celda × día, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.tuned.rmse` | 1,668 | RMSE (°C), tuned, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.tuned.sesgo` | −1,434 | Sesgo (°C), tuned, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.tuned_sin_td.rmse` | 1,526 | RMSE (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.tuned_sin_td.sesgo` | −1,220 | Sesgo (°C), tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.llr_rezagos_sel.rmse` | 1,507 | RMSE (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.llr_rezagos_sel.sesgo` | −1,233 | Sesgo (°C), LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.llr_simple_sel.rmse` | 1,524 | RMSE (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.llr_simple_sel.sesgo` | −1,264 | Sesgo (°C), LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.clim.rmse` | 2,364 | RMSE (°C), climatología, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.clim.sesgo` | −2,233 | Sesgo (°C), climatología, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.timesfm.rmse` | 0,710 | RMSE (°C), TimesFM, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.timesfm.sesgo` | −0,082 | Sesgo (°C), TimesFM, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.n` | 10.861.095 | Filas celda × día, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.tuned.rmse` | 0,730 | RMSE (°C), tuned, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.tuned.sesgo` | −0,061 | Sesgo (°C), tuned, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.tuned_sin_td.rmse` | 0,752 | RMSE (°C), tuned sin rezagos de Td, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.tuned_sin_td.sesgo` | −0,035 | Sesgo (°C), tuned sin rezagos de Td, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.llr_rezagos_sel.rmse` | 0,729 | RMSE (°C), LLR con rezagos seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.llr_rezagos_sel.sesgo` | −0,061 | Sesgo (°C), LLR con rezagos seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.llr_simple_sel.rmse` | 0,733 | RMSE (°C), LLR simple seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.llr_simple_sel.sesgo` | −0,083 | Sesgo (°C), LLR simple seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.clim.rmse` | 0,863 | RMSE (°C), climatología, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.clim.sesgo` | −0,211 | Sesgo (°C), climatología, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.panel.inf5.brecha.tuned` | −0,209 | Brecha (°C) TimesFM − tuned, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.brecha.tuned_sin_td` | −0,134 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.brecha.llr_rezagos_sel` | −0,073 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.inf5.brecha.llr_simple_sel` | −0,081 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.brecha.tuned` | −0,358 | Brecha (°C) TimesFM − tuned, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.brecha.tuned_sin_td` | −0,180 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.brecha.llr_rezagos_sel` | −0,110 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.sup5.brecha.llr_simple_sel` | −0,134 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.brecha.tuned` | −0,029 | Brecha (°C) TimesFM − tuned, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.brecha.tuned_sin_td` | −0,043 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.brecha.llr_rezagos_sel` | −0,015 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.resto.brecha.llr_simple_sel` | −0,022 | Brecha (°C) TimesFM − LLR simple seleccionado, 90 % central, `ll4b`, dominio completo |
| `extremos.ll4b.panel.pct_extremos` | 10,1 | Porcentaje de filas en las dos colas (sin símbolo %), `ll4b`, dominio completo |
| `extremos.ll4b.panel.colas_favorecen.tuned` | sí | ¿TimesFM tiene menor RMSE que tuned en las dos colas? `ll4b`, dominio completo |
| `extremos.ll4b.panel.colas_favorecen.tuned_sin_td` | sí | ¿TimesFM tiene menor RMSE que tuned sin rezagos de Td en las dos colas? `ll4b`, dominio completo |
| `extremos.ll4b.panel.colas_favorecen.llr_rezagos_sel` | sí | ¿TimesFM tiene menor RMSE que LLR con rezagos seleccionado en las dos colas? `ll4b`, dominio completo |
| `extremos.ll4b.panel.colas_favorecen.llr_simple_sel` | sí | ¿TimesFM tiene menor RMSE que LLR simple seleccionado en las dos colas? `ll4b`, dominio completo |
| `extremos.ll4b.peru.inf5.brecha.tuned` | −0,258 | Brecha (°C) TimesFM − tuned, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.brecha.tuned_sin_td` | −0,168 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.brecha.llr_rezagos_sel` | −0,088 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.inf5.brecha.llr_simple_sel` | −0,082 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.brecha.tuned` | −0,191 | Brecha (°C) TimesFM − tuned, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.brecha.tuned_sin_td` | −0,048 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.brecha.llr_rezagos_sel` | −0,030 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.sup5.brecha.llr_simple_sel` | −0,047 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.brecha.tuned` | −0,021 | Brecha (°C) TimesFM − tuned, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.brecha.tuned_sin_td` | −0,042 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.brecha.llr_rezagos_sel` | −0,019 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.resto.brecha.llr_simple_sel` | −0,023 | Brecha (°C) TimesFM − LLR simple seleccionado, 90 % central, `ll4b`, Perú |
| `extremos.ll4b.peru.pct_extremos` | 10,1 | Porcentaje de filas en las dos colas (sin símbolo %), `ll4b`, Perú |
| `extremos.ll4b.peru.colas_favorecen.tuned` | sí | ¿TimesFM tiene menor RMSE que tuned en las dos colas? `ll4b`, Perú |
| `extremos.ll4b.peru.colas_favorecen.tuned_sin_td` | sí | ¿TimesFM tiene menor RMSE que tuned sin rezagos de Td en las dos colas? `ll4b`, Perú |
| `extremos.ll4b.peru.colas_favorecen.llr_rezagos_sel` | sí | ¿TimesFM tiene menor RMSE que LLR con rezagos seleccionado en las dos colas? `ll4b`, Perú |
| `extremos.ll4b.peru.colas_favorecen.llr_simple_sel` | sí | ¿TimesFM tiene menor RMSE que LLR simple seleccionado en las dos colas? `ll4b`, Perú |
| `extremos.ll4.panel.inf5.brecha.tuned` | −0,082 | Brecha (°C) TimesFM − tuned, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.brecha.tuned_sin_td` | +0,047 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.brecha.llr_rezagos_sel` | +0,032 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.inf5.brecha.llr_simple_sel` | +0,024 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.brecha.tuned` | −0,573 | Brecha (°C) TimesFM − tuned, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.brecha.tuned_sin_td` | −0,238 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.brecha.llr_rezagos_sel` | −0,143 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.sup5.brecha.llr_simple_sel` | −0,213 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.brecha.tuned` | −0,007 | Brecha (°C) TimesFM − tuned, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.brecha.tuned_sin_td` | −0,001 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.brecha.llr_rezagos_sel` | +0,011 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.resto.brecha.llr_simple_sel` | +0,002 | Brecha (°C) TimesFM − LLR simple seleccionado, 90 % central, `ll4`, dominio completo |
| `extremos.ll4.panel.pct_extremos` | 10,1 | Porcentaje de filas en las dos colas (sin símbolo %), `ll4`, dominio completo |
| `extremos.ll4.panel.colas_favorecen.tuned` | sí | ¿TimesFM tiene menor RMSE que tuned en las dos colas? `ll4`, dominio completo |
| `extremos.ll4.panel.colas_favorecen.tuned_sin_td` | no | ¿TimesFM tiene menor RMSE que tuned sin rezagos de Td en las dos colas? `ll4`, dominio completo |
| `extremos.ll4.panel.colas_favorecen.llr_rezagos_sel` | no | ¿TimesFM tiene menor RMSE que LLR con rezagos seleccionado en las dos colas? `ll4`, dominio completo |
| `extremos.ll4.panel.colas_favorecen.llr_simple_sel` | no | ¿TimesFM tiene menor RMSE que LLR simple seleccionado en las dos colas? `ll4`, dominio completo |
| `extremos.ll4.peru.inf5.brecha.tuned` | −0,204 | Brecha (°C) TimesFM − tuned, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.brecha.tuned_sin_td` | −0,080 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.brecha.llr_rezagos_sel` | −0,054 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.inf5.brecha.llr_simple_sel` | −0,035 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % inferior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.brecha.tuned` | −0,327 | Brecha (°C) TimesFM − tuned, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.brecha.tuned_sin_td` | −0,084 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.brecha.llr_rezagos_sel` | −0,058 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.sup5.brecha.llr_simple_sel` | −0,148 | Brecha (°C) TimesFM − LLR simple seleccionado, 5 % superior de la anomalía observada, `ll4`, Perú |
| `extremos.ll4.peru.resto.brecha.tuned` | −0,036 | Brecha (°C) TimesFM − tuned, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.brecha.tuned_sin_td` | −0,036 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.brecha.llr_rezagos_sel` | −0,020 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.resto.brecha.llr_simple_sel` | −0,031 | Brecha (°C) TimesFM − LLR simple seleccionado, 90 % central, `ll4`, Perú |
| `extremos.ll4.peru.pct_extremos` | 10,1 | Porcentaje de filas en las dos colas (sin símbolo %), `ll4`, Perú |
| `extremos.ll4.peru.colas_favorecen.tuned` | sí | ¿TimesFM tiene menor RMSE que tuned en las dos colas? `ll4`, Perú |
| `extremos.ll4.peru.colas_favorecen.tuned_sin_td` | sí | ¿TimesFM tiene menor RMSE que tuned sin rezagos de Td en las dos colas? `ll4`, Perú |
| `extremos.ll4.peru.colas_favorecen.llr_rezagos_sel` | sí | ¿TimesFM tiene menor RMSE que LLR con rezagos seleccionado en las dos colas? `ll4`, Perú |
| `extremos.ll4.peru.colas_favorecen.llr_simple_sel` | sí | ¿TimesFM tiene menor RMSE que LLR simple seleccionado en las dos colas? `ll4`, Perú |

## calib

| clave | valor | significado |
|---|---|---|
| `calib.nominal` | 80 | Cobertura nominal (%) del intervalo q10–q90 |
| `calib.cola_nominal` | 10 | Fracción nominal (%) de cada cola (bajo q10, sobre q90) |
| `calib.ll4.panel.total.n` | 24.876.447 | Filas celda × día, `ll4`, dominio completo, total |
| `calib.ll4.panel.total.cobertura` | 81,0 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.anchura` | 2,67 | Anchura media del intervalo 80 % (°C), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.crps` | 0,646 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pinball` | 0,323 | Pinball medio de los nueve cuantiles (°C), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.frac_bajo_q10` | 11,0 | Observaciones bajo q10 (%, sin símbolo), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.frac_sobre_q90` | 8,0 | Observaciones sobre q90 (%, sin símbolo), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit0` | 11,0 | Observaciones en el decil 1 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit1` | 10,8 | Observaciones en el decil 2 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit2` | 10,8 | Observaciones en el decil 3 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit3` | 10,6 | Observaciones en el decil 4 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit4` | 10,3 | Observaciones en el decil 5 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit5` | 10,3 | Observaciones en el decil 6 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit6` | 9,9 | Observaciones en el decil 7 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit7` | 9,5 | Observaciones en el decil 8 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit8` | 8,7 | Observaciones en el decil 9 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.total.pit9` | 8,0 | Observaciones en el decil 10 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, dominio completo, total |
| `calib.ll4.panel.a2013.n` | 6.214.855 | Filas celda × día, `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.cobertura` | 79,1 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.anchura` | 2,59 | Anchura media del intervalo 80 % (°C), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.crps` | 0,662 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.pinball` | 0,331 | Pinball medio de los nueve cuantiles (°C), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.frac_bajo_q10` | 15,4 | Observaciones bajo q10 (%, sin símbolo), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2013.frac_sobre_q90` | 5,6 | Observaciones sobre q90 (%, sin símbolo), `ll4`, dominio completo, año 2013 |
| `calib.ll4.panel.a2014.n` | 6.214.855 | Filas celda × día, `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.cobertura` | 80,4 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.anchura` | 2,64 | Anchura media del intervalo 80 % (°C), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.crps` | 0,639 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.pinball` | 0,320 | Pinball medio de los nueve cuantiles (°C), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.frac_bajo_q10` | 12,5 | Observaciones bajo q10 (%, sin símbolo), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2014.frac_sobre_q90` | 7,2 | Observaciones sobre q90 (%, sin símbolo), `ll4`, dominio completo, año 2014 |
| `calib.ll4.panel.a2015.n` | 6.214.855 | Filas celda × día, `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.cobertura` | 82,8 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.anchura` | 2,67 | Anchura media del intervalo 80 % (°C), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.crps` | 0,613 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.pinball` | 0,306 | Pinball medio de los nueve cuantiles (°C), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.frac_bajo_q10` | 6,8 | Observaciones bajo q10 (%, sin símbolo), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2015.frac_sobre_q90` | 10,4 | Observaciones sobre q90 (%, sin símbolo), `ll4`, dominio completo, año 2015 |
| `calib.ll4.panel.a2016.n` | 6.231.882 | Filas celda × día, `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.cobertura` | 81,8 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.anchura` | 2,80 | Anchura media del intervalo 80 % (°C), `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.crps` | 0,670 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.pinball` | 0,335 | Pinball medio de los nueve cuantiles (°C), `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.frac_bajo_q10` | 9,3 | Observaciones bajo q10 (%, sin símbolo), `ll4`, dominio completo, año 2016 |
| `calib.ll4.panel.a2016.frac_sobre_q90` | 8,8 | Observaciones sobre q90 (%, sin símbolo), `ll4`, dominio completo, año 2016 |
| `calib.ll4.peru.total.n` | 12.085.392 | Filas celda × día, `ll4`, Perú, total |
| `calib.ll4.peru.total.cobertura` | 81,6 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, Perú, total |
| `calib.ll4.peru.total.anchura` | 2,10 | Anchura media del intervalo 80 % (°C), `ll4`, Perú, total |
| `calib.ll4.peru.total.crps` | 0,497 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, Perú, total |
| `calib.ll4.peru.total.pinball` | 0,249 | Pinball medio de los nueve cuantiles (°C), `ll4`, Perú, total |
| `calib.ll4.peru.total.frac_bajo_q10` | 10,3 | Observaciones bajo q10 (%, sin símbolo), `ll4`, Perú, total |
| `calib.ll4.peru.total.frac_sobre_q90` | 8,1 | Observaciones sobre q90 (%, sin símbolo), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit0` | 10,3 | Observaciones en el decil 1 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit1` | 10,2 | Observaciones en el decil 2 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit2` | 10,5 | Observaciones en el decil 3 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit3` | 10,5 | Observaciones en el decil 4 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit4` | 10,4 | Observaciones en el decil 5 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit5` | 10,5 | Observaciones en el decil 6 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit6` | 10,2 | Observaciones en el decil 7 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit7` | 10,1 | Observaciones en el decil 8 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit8` | 9,2 | Observaciones en el decil 9 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.total.pit9` | 8,1 | Observaciones en el decil 10 de la predicción (%, sin símbolo; 10 % nominal), `ll4`, Perú, total |
| `calib.ll4.peru.a2013.n` | 3.019.280 | Filas celda × día, `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.cobertura` | 80,2 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.anchura` | 2,00 | Anchura media del intervalo 80 % (°C), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.crps` | 0,490 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.pinball` | 0,245 | Pinball medio de los nueve cuantiles (°C), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.frac_bajo_q10` | 13,5 | Observaciones bajo q10 (%, sin símbolo), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2013.frac_sobre_q90` | 6,3 | Observaciones sobre q90 (%, sin símbolo), `ll4`, Perú, año 2013 |
| `calib.ll4.peru.a2014.n` | 3.019.280 | Filas celda × día, `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.cobertura` | 80,8 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.anchura` | 2,07 | Anchura media del intervalo 80 % (°C), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.crps` | 0,498 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.pinball` | 0,249 | Pinball medio de los nueve cuantiles (°C), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.frac_bajo_q10` | 12,3 | Observaciones bajo q10 (%, sin símbolo), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2014.frac_sobre_q90` | 6,9 | Observaciones sobre q90 (%, sin símbolo), `ll4`, Perú, año 2014 |
| `calib.ll4.peru.a2015.n` | 3.019.280 | Filas celda × día, `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.cobertura` | 82,6 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.anchura` | 2,10 | Anchura media del intervalo 80 % (°C), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.crps` | 0,484 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.pinball` | 0,242 | Pinball medio de los nueve cuantiles (°C), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.frac_bajo_q10` | 7,0 | Observaciones bajo q10 (%, sin símbolo), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2015.frac_sobre_q90` | 10,4 | Observaciones sobre q90 (%, sin símbolo), `ll4`, Perú, año 2015 |
| `calib.ll4.peru.a2016.n` | 3.027.552 | Filas celda × día, `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.cobertura` | 82,7 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.anchura` | 2,22 | Anchura media del intervalo 80 % (°C), `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.crps` | 0,517 | CRPS aproximado por cuadratura de pinball (°C), `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.pinball` | 0,259 | Pinball medio de los nueve cuantiles (°C), `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.frac_bajo_q10` | 8,4 | Observaciones bajo q10 (%, sin símbolo), `ll4`, Perú, año 2016 |
| `calib.ll4.peru.a2016.frac_sobre_q90` | 8,9 | Observaciones sobre q90 (%, sin símbolo), `ll4`, Perú, año 2016 |
| `calib.ll4b.panel.total.n` | 24.876.447 | Filas celda × día, `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.cobertura` | 83,6 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.anchura` | 2,69 | Anchura media del intervalo 80 % (°C), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.crps` | 0,597 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pinball` | 0,299 | Pinball medio de los nueve cuantiles (°C), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.frac_bajo_q10` | 6,6 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.frac_sobre_q90` | 9,8 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit0` | 6,6 | Observaciones en el decil 1 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit1` | 8,6 | Observaciones en el decil 2 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit2` | 9,5 | Observaciones en el decil 3 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit3` | 10,2 | Observaciones en el decil 4 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit4` | 10,9 | Observaciones en el decil 5 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit5` | 11,2 | Observaciones en el decil 6 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit6` | 11,3 | Observaciones en el decil 7 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit7` | 11,2 | Observaciones en el decil 8 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit8` | 10,7 | Observaciones en el decil 9 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.total.pit9` | 9,8 | Observaciones en el decil 10 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, dominio completo, total |
| `calib.ll4b.panel.a2009.n` | 6.214.855 | Filas celda × día, `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.cobertura` | 82,4 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.anchura` | 2,56 | Anchura media del intervalo 80 % (°C), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.crps` | 0,586 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.pinball` | 0,293 | Pinball medio de los nueve cuantiles (°C), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.frac_bajo_q10` | 11,4 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2009.frac_sobre_q90` | 6,2 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, dominio completo, año 2009 |
| `calib.ll4b.panel.a2010.n` | 6.214.855 | Filas celda × día, `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.cobertura` | 85,8 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.anchura` | 2,76 | Anchura media del intervalo 80 % (°C), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.crps` | 0,582 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.pinball` | 0,291 | Pinball medio de los nueve cuantiles (°C), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.frac_bajo_q10` | 6,1 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2010.frac_sobre_q90` | 8,1 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, dominio completo, año 2010 |
| `calib.ll4b.panel.a2011.n` | 6.214.855 | Filas celda × día, `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.cobertura` | 85,0 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.anchura` | 2,72 | Anchura media del intervalo 80 % (°C), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.crps` | 0,588 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.pinball` | 0,294 | Pinball medio de los nueve cuantiles (°C), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.frac_bajo_q10` | 4,9 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2011.frac_sobre_q90` | 10,1 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, dominio completo, año 2011 |
| `calib.ll4b.panel.a2012.n` | 6.231.882 | Filas celda × día, `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.cobertura` | 81,2 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.anchura` | 2,73 | Anchura media del intervalo 80 % (°C), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.crps` | 0,633 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.pinball` | 0,317 | Pinball medio de los nueve cuantiles (°C), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.frac_bajo_q10` | 4,0 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.panel.a2012.frac_sobre_q90` | 14,8 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, dominio completo, año 2012 |
| `calib.ll4b.peru.total.n` | 12.085.392 | Filas celda × día, `ll4b`, Perú, total |
| `calib.ll4b.peru.total.cobertura` | 83,5 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.anchura` | 2,10 | Anchura media del intervalo 80 % (°C), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.crps` | 0,469 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pinball` | 0,234 | Pinball medio de los nueve cuantiles (°C), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.frac_bajo_q10` | 6,6 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.frac_sobre_q90` | 9,9 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit0` | 6,6 | Observaciones en el decil 1 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit1` | 8,6 | Observaciones en el decil 2 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit2` | 9,4 | Observaciones en el decil 3 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit3` | 10,2 | Observaciones en el decil 4 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit4` | 10,8 | Observaciones en el decil 5 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit5` | 11,1 | Observaciones en el decil 6 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit6` | 11,4 | Observaciones en el decil 7 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit7` | 11,3 | Observaciones en el decil 8 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit8` | 10,8 | Observaciones en el decil 9 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.total.pit9` | 9,9 | Observaciones en el decil 10 de la predicción (%, sin símbolo; 10 % nominal), `ll4b`, Perú, total |
| `calib.ll4b.peru.a2009.n` | 3.019.280 | Filas celda × día, `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.cobertura` | 83,1 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.anchura` | 2,01 | Anchura media del intervalo 80 % (°C), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.crps` | 0,452 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.pinball` | 0,226 | Pinball medio de los nueve cuantiles (°C), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.frac_bajo_q10` | 9,8 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2009.frac_sobre_q90` | 7,1 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, Perú, año 2009 |
| `calib.ll4b.peru.a2010.n` | 3.019.280 | Filas celda × día, `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.cobertura` | 85,6 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.anchura` | 2,14 | Anchura media del intervalo 80 % (°C), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.crps` | 0,454 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.pinball` | 0,227 | Pinball medio de los nueve cuantiles (°C), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.frac_bajo_q10` | 6,8 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2010.frac_sobre_q90` | 7,6 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, Perú, año 2010 |
| `calib.ll4b.peru.a2011.n` | 3.019.280 | Filas celda × día, `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.cobertura` | 85,0 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.anchura` | 2,11 | Anchura media del intervalo 80 % (°C), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.crps` | 0,459 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.pinball` | 0,230 | Pinball medio de los nueve cuantiles (°C), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.frac_bajo_q10` | 5,3 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2011.frac_sobre_q90` | 9,7 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, Perú, año 2011 |
| `calib.ll4b.peru.a2012.n` | 3.027.552 | Filas celda × día, `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.cobertura` | 80,3 | Cobertura empírica del intervalo 80 % (%, sin símbolo), `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.anchura` | 2,13 | Anchura media del intervalo 80 % (°C), `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.crps` | 0,510 | CRPS aproximado por cuadratura de pinball (°C), `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.pinball` | 0,255 | Pinball medio de los nueve cuantiles (°C), `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.frac_bajo_q10` | 4,5 | Observaciones bajo q10 (%, sin símbolo), `ll4b`, Perú, año 2012 |
| `calib.ll4b.peru.a2012.frac_sobre_q90` | 15,3 | Observaciones sobre q90 (%, sin símbolo), `ll4b`, Perú, año 2012 |

## altitud

| clave | valor | significado |
|---|---|---|
| `altitud.ll4.panel.b0_500.rmse.timesfm` | 1,293 | RMSE (°C), TimesFM, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.sesgo.timesfm` | +0,118 | Sesgo (°C), TimesFM, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.celdas` | 11.397 | Celdas, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.n` | 16.651.017 | Filas celda × día, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.rmse.tuned` | 1,365 | RMSE (°C), tuned, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.sesgo.tuned` | −0,096 | Sesgo (°C), tuned, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.brecha.tuned` | −0,072 | Brecha (°C) TimesFM − tuned, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.rmse.tuned_sin_td` | 1,301 | RMSE (°C), tuned sin rezagos de Td, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.sesgo.tuned_sin_td` | −0,041 | Sesgo (°C), tuned sin rezagos de Td, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.brecha.tuned_sin_td` | −0,008 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.rmse.llr_rezagos_sel` | 1,285 | RMSE (°C), LLR con rezagos seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.sesgo.llr_rezagos_sel` | +0,015 | Sesgo (°C), LLR con rezagos seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.brecha.llr_rezagos_sel` | +0,008 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.rmse.llr_simple_sel` | 1,301 | RMSE (°C), LLR simple seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.sesgo.llr_simple_sel` | −0,026 | Sesgo (°C), LLR simple seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b0_500.brecha.llr_simple_sel` | −0,009 | Brecha (°C) TimesFM − LLR simple seleccionado, 0–500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.rmse.timesfm` | 0,782 | RMSE (°C), TimesFM, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.sesgo.timesfm` | +0,017 | Sesgo (°C), TimesFM, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.celdas` | 918 | Celdas, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.n` | 1.341.198 | Filas celda × día, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.rmse.tuned` | 0,840 | RMSE (°C), tuned, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.sesgo.tuned` | +0,010 | Sesgo (°C), tuned, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.brecha.tuned` | −0,058 | Brecha (°C) TimesFM − tuned, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.rmse.tuned_sin_td` | 0,813 | RMSE (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.sesgo.tuned_sin_td` | +0,034 | Sesgo (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.brecha.tuned_sin_td` | −0,031 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.rmse.llr_rezagos_sel` | 0,806 | RMSE (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.sesgo.llr_rezagos_sel` | +0,012 | Sesgo (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.brecha.llr_rezagos_sel` | −0,024 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.rmse.llr_simple_sel` | 0,821 | RMSE (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.sesgo.llr_simple_sel` | −0,029 | Sesgo (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b1500_2500.brecha.llr_simple_sel` | −0,040 | Brecha (°C) TimesFM − LLR simple seleccionado, 1.500–2.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.rmse.timesfm` | 0,855 | RMSE (°C), TimesFM, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.sesgo.timesfm` | +0,077 | Sesgo (°C), TimesFM, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.celdas` | 902 | Celdas, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.n` | 1.317.822 | Filas celda × día, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.rmse.tuned` | 0,937 | RMSE (°C), tuned, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.sesgo.tuned` | +0,092 | Sesgo (°C), tuned, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.brecha.tuned` | −0,081 | Brecha (°C) TimesFM − tuned, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.rmse.tuned_sin_td` | 0,907 | RMSE (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.sesgo.tuned_sin_td` | +0,119 | Sesgo (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.brecha.tuned_sin_td` | −0,052 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.rmse.llr_rezagos_sel` | 0,891 | RMSE (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.sesgo.llr_rezagos_sel` | +0,084 | Sesgo (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.brecha.llr_rezagos_sel` | −0,036 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.rmse.llr_simple_sel` | 0,901 | RMSE (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.sesgo.llr_simple_sel` | +0,056 | Sesgo (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b2500_3500.brecha.llr_simple_sel` | −0,046 | Brecha (°C) TimesFM − LLR simple seleccionado, 2.500–3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.rmse.timesfm` | 0,699 | RMSE (°C), TimesFM, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.sesgo.timesfm` | −0,008 | Sesgo (°C), TimesFM, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.celdas` | 1.537 | Celdas, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.n` | 2.245.557 | Filas celda × día, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.rmse.tuned` | 0,760 | RMSE (°C), tuned, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.sesgo.tuned` | −0,058 | Sesgo (°C), tuned, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.brecha.tuned` | −0,061 | Brecha (°C) TimesFM − tuned, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.rmse.tuned_sin_td` | 0,732 | RMSE (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.sesgo.tuned_sin_td` | −0,027 | Sesgo (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.brecha.tuned_sin_td` | −0,033 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.rmse.llr_rezagos_sel` | 0,727 | RMSE (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.sesgo.llr_rezagos_sel` | −0,034 | Sesgo (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.brecha.llr_rezagos_sel` | −0,028 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.rmse.llr_simple_sel` | 0,751 | RMSE (°C), LLR simple seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.sesgo.llr_simple_sel` | −0,093 | Sesgo (°C), LLR simple seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b500_1500.brecha.llr_simple_sel` | −0,051 | Brecha (°C) TimesFM − LLR simple seleccionado, 500–1.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.rmse.timesfm` | 0,851 | RMSE (°C), TimesFM, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.sesgo.timesfm` | +0,157 | Sesgo (°C), TimesFM, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.celdas` | 2.273 | Celdas, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.n` | 3.320.853 | Filas celda × día, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.rmse.tuned` | 0,967 | RMSE (°C), tuned, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.sesgo.tuned` | +0,234 | Sesgo (°C), tuned, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.brecha.tuned` | −0,116 | Brecha (°C) TimesFM − tuned, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.rmse.tuned_sin_td` | 0,942 | RMSE (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.sesgo.tuned_sin_td` | +0,271 | Sesgo (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.brecha.tuned_sin_td` | −0,091 | Brecha (°C) TimesFM − tuned sin rezagos de Td, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.rmse.llr_rezagos_sel` | 0,900 | RMSE (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.sesgo.llr_rezagos_sel` | +0,179 | Sesgo (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.brecha.llr_rezagos_sel` | −0,049 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.rmse.llr_simple_sel` | 0,905 | RMSE (°C), LLR simple seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.sesgo.llr_simple_sel` | +0,164 | Sesgo (°C), LLR simple seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.b3500_mas.brecha.llr_simple_sel` | −0,053 | Brecha (°C) TimesFM − LLR simple seleccionado, más de 3.500 m, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.rmse.timesfm` | 1,372 | RMSE (°C), TimesFM, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.sesgo.timesfm` | +0,156 | Sesgo (°C), TimesFM, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.celdas` | 8.755 | Celdas, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.n` | 12.791.055 | Filas celda × día, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.rmse.tuned` | 1,446 | RMSE (°C), tuned, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.sesgo.tuned` | −0,073 | Sesgo (°C), tuned, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.brecha.tuned` | −0,074 | Brecha (°C) TimesFM − tuned, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.rmse.tuned_sin_td` | 1,379 | RMSE (°C), tuned sin rezagos de Td, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.sesgo.tuned_sin_td` | −0,017 | Sesgo (°C), tuned sin rezagos de Td, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.brecha.tuned_sin_td` | −0,008 | Brecha (°C) TimesFM − tuned sin rezagos de Td, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.rmse.llr_rezagos_sel` | 1,361 | RMSE (°C), LLR con rezagos seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.sesgo.llr_rezagos_sel` | +0,038 | Sesgo (°C), LLR con rezagos seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.brecha.llr_rezagos_sel` | +0,011 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.rmse.llr_simple_sel` | 1,376 | RMSE (°C), LLR simple seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.sesgo.llr_simple_sel` | +0,009 | Sesgo (°C), LLR simple seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.fuera_peru.brecha.llr_simple_sel` | −0,005 | Brecha (°C) TimesFM − LLR simple seleccionado, fuera de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.rmse.timesfm` | 0,865 | RMSE (°C), TimesFM, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.sesgo.timesfm` | +0,050 | Sesgo (°C), TimesFM, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.celdas` | 8.272 | Celdas, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.n` | 12.085.392 | Filas celda × día, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.rmse.tuned` | 0,944 | RMSE (°C), tuned, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.sesgo.tuned` | +0,010 | Sesgo (°C), tuned, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.brecha.tuned` | −0,079 | Brecha (°C) TimesFM − tuned, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.rmse.tuned_sin_td` | 0,908 | RMSE (°C), tuned sin rezagos de Td, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.sesgo.tuned_sin_td` | +0,047 | Sesgo (°C), tuned sin rezagos de Td, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.brecha.tuned_sin_td` | −0,043 | Brecha (°C) TimesFM − tuned sin rezagos de Td, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.rmse.llr_rezagos_sel` | 0,891 | RMSE (°C), LLR con rezagos seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.sesgo.llr_rezagos_sel` | +0,034 | Sesgo (°C), LLR con rezagos seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.brecha.llr_rezagos_sel` | −0,026 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.rmse.llr_simple_sel` | 0,906 | RMSE (°C), LLR simple seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.sesgo.llr_simple_sel` | −0,014 | Sesgo (°C), LLR simple seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.panel.peru.brecha.llr_simple_sel` | −0,041 | Brecha (°C) TimesFM − LLR simple seleccionado, dentro de Perú, `ll4`, dominio completo |
| `altitud.ll4.peru.b0_500.rmse.timesfm` | 0,956 | RMSE (°C), TimesFM, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.sesgo.timesfm` | +0,049 | Sesgo (°C), TimesFM, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.celdas` | 4.185 | Celdas, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.n` | 6.114.285 | Filas celda × día, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.rmse.tuned` | 1,035 | RMSE (°C), tuned, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.sesgo.tuned` | −0,079 | Sesgo (°C), tuned, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.brecha.tuned` | −0,079 | Brecha (°C) TimesFM − tuned, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.rmse.tuned_sin_td` | 0,984 | RMSE (°C), tuned sin rezagos de Td, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.sesgo.tuned_sin_td` | −0,032 | Sesgo (°C), tuned sin rezagos de Td, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.brecha.tuned_sin_td` | −0,027 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.rmse.llr_rezagos_sel` | 0,971 | RMSE (°C), LLR con rezagos seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.sesgo.llr_rezagos_sel` | −0,002 | Sesgo (°C), LLR con rezagos seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.brecha.llr_rezagos_sel` | −0,015 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.rmse.llr_simple_sel` | 0,990 | RMSE (°C), LLR simple seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.sesgo.llr_simple_sel` | −0,063 | Sesgo (°C), LLR simple seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b0_500.brecha.llr_simple_sel` | −0,033 | Brecha (°C) TimesFM − LLR simple seleccionado, 0–500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.rmse.timesfm` | 0,739 | RMSE (°C), TimesFM, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.sesgo.timesfm` | −0,012 | Sesgo (°C), TimesFM, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.celdas` | 636 | Celdas, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.n` | 929.196 | Filas celda × día, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.rmse.tuned` | 0,793 | RMSE (°C), tuned, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.sesgo.tuned` | +0,030 | Sesgo (°C), tuned, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.brecha.tuned` | −0,054 | Brecha (°C) TimesFM − tuned, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.rmse.tuned_sin_td` | 0,775 | RMSE (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.sesgo.tuned_sin_td` | +0,049 | Sesgo (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.brecha.tuned_sin_td` | −0,035 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.rmse.llr_rezagos_sel` | 0,767 | RMSE (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.sesgo.llr_rezagos_sel` | +0,007 | Sesgo (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.brecha.llr_rezagos_sel` | −0,028 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.rmse.llr_simple_sel` | 0,783 | RMSE (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.sesgo.llr_simple_sel` | −0,036 | Sesgo (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b1500_2500.brecha.llr_simple_sel` | −0,044 | Brecha (°C) TimesFM − LLR simple seleccionado, 1.500–2.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.rmse.timesfm` | 0,784 | RMSE (°C), TimesFM, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.sesgo.timesfm` | +0,047 | Sesgo (°C), TimesFM, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.celdas` | 630 | Celdas, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.n` | 920.430 | Filas celda × día, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.rmse.tuned` | 0,857 | RMSE (°C), tuned, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.sesgo.tuned` | +0,117 | Sesgo (°C), tuned, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.brecha.tuned` | −0,073 | Brecha (°C) TimesFM − tuned, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.rmse.tuned_sin_td` | 0,839 | RMSE (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.sesgo.tuned_sin_td` | +0,136 | Sesgo (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.brecha.tuned_sin_td` | −0,055 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.rmse.llr_rezagos_sel` | 0,819 | RMSE (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.sesgo.llr_rezagos_sel` | +0,080 | Sesgo (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.brecha.llr_rezagos_sel` | −0,036 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.rmse.llr_simple_sel` | 0,830 | RMSE (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.sesgo.llr_simple_sel` | +0,053 | Sesgo (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b2500_3500.brecha.llr_simple_sel` | −0,046 | Brecha (°C) TimesFM − LLR simple seleccionado, 2.500–3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.rmse.timesfm` | 0,630 | RMSE (°C), TimesFM, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.sesgo.timesfm` | −0,039 | Sesgo (°C), TimesFM, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.celdas` | 1.144 | Celdas, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.n` | 1.671.384 | Filas celda × día, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.rmse.tuned` | 0,689 | RMSE (°C), tuned, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.sesgo.tuned` | −0,055 | Sesgo (°C), tuned, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.brecha.tuned` | −0,059 | Brecha (°C) TimesFM − tuned, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.rmse.tuned_sin_td` | 0,668 | RMSE (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.sesgo.tuned_sin_td` | −0,022 | Sesgo (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.brecha.tuned_sin_td` | −0,039 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.rmse.llr_rezagos_sel` | 0,663 | RMSE (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.sesgo.llr_rezagos_sel` | −0,042 | Sesgo (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.brecha.llr_rezagos_sel` | −0,034 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.rmse.llr_simple_sel` | 0,687 | RMSE (°C), LLR simple seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.sesgo.llr_simple_sel` | −0,102 | Sesgo (°C), LLR simple seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b500_1500.brecha.llr_simple_sel` | −0,058 | Brecha (°C) TimesFM − LLR simple seleccionado, 500–1.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.rmse.timesfm` | 0,837 | RMSE (°C), TimesFM, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.sesgo.timesfm` | +0,138 | Sesgo (°C), TimesFM, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.celdas` | 1.677 | Celdas, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.n` | 2.450.097 | Filas celda × día, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.rmse.tuned` | 0,942 | RMSE (°C), tuned, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.sesgo.tuned` | +0,227 | Sesgo (°C), tuned, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.brecha.tuned` | −0,105 | Brecha (°C) TimesFM − tuned, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.rmse.tuned_sin_td` | 0,924 | RMSE (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.sesgo.tuned_sin_td` | +0,260 | Sesgo (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.brecha.tuned_sin_td` | −0,087 | Brecha (°C) TimesFM − tuned sin rezagos de Td, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.rmse.llr_rezagos_sel` | 0,885 | RMSE (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.sesgo.llr_rezagos_sel` | +0,167 | Sesgo (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.brecha.llr_rezagos_sel` | −0,048 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.rmse.llr_simple_sel` | 0,890 | RMSE (°C), LLR simple seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.sesgo.llr_simple_sel` | +0,151 | Sesgo (°C), LLR simple seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4.peru.b3500_mas.brecha.llr_simple_sel` | −0,053 | Brecha (°C) TimesFM − LLR simple seleccionado, más de 3.500 m, `ll4`, Perú |
| `altitud.ll4b.panel.b0_500.rmse.timesfm` | 1,171 | RMSE (°C), TimesFM, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.sesgo.timesfm` | −0,136 | Sesgo (°C), TimesFM, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.celdas` | 11.397 | Celdas, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.n` | 16.651.017 | Filas celda × día, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.rmse.tuned` | 1,249 | RMSE (°C), tuned, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.sesgo.tuned` | −0,245 | Sesgo (°C), tuned, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.brecha.tuned` | −0,078 | Brecha (°C) TimesFM − tuned, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.rmse.tuned_sin_td` | 1,236 | RMSE (°C), tuned sin rezagos de Td, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.sesgo.tuned_sin_td` | −0,204 | Sesgo (°C), tuned sin rezagos de Td, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.brecha.tuned_sin_td` | −0,065 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.rmse.llr_rezagos_sel` | 1,199 | RMSE (°C), LLR con rezagos seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.sesgo.llr_rezagos_sel` | −0,162 | Sesgo (°C), LLR con rezagos seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.brecha.llr_rezagos_sel` | −0,028 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.rmse.llr_simple_sel` | 1,209 | RMSE (°C), LLR simple seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.sesgo.llr_simple_sel` | −0,185 | Sesgo (°C), LLR simple seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b0_500.brecha.llr_simple_sel` | −0,038 | Brecha (°C) TimesFM − LLR simple seleccionado, 0–500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.rmse.timesfm` | 0,720 | RMSE (°C), TimesFM, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.sesgo.timesfm` | −0,094 | Sesgo (°C), TimesFM, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.celdas` | 918 | Celdas, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.n` | 1.341.198 | Filas celda × día, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.rmse.tuned` | 0,772 | RMSE (°C), tuned, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.sesgo.tuned` | −0,042 | Sesgo (°C), tuned, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.brecha.tuned` | −0,052 | Brecha (°C) TimesFM − tuned, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.rmse.tuned_sin_td` | 0,758 | RMSE (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.sesgo.tuned_sin_td` | −0,026 | Sesgo (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.brecha.tuned_sin_td` | −0,037 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.rmse.llr_rezagos_sel` | 0,745 | RMSE (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.sesgo.llr_rezagos_sel` | −0,062 | Sesgo (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.brecha.llr_rezagos_sel` | −0,025 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.rmse.llr_simple_sel` | 0,754 | RMSE (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.sesgo.llr_simple_sel` | −0,076 | Sesgo (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b1500_2500.brecha.llr_simple_sel` | −0,034 | Brecha (°C) TimesFM − LLR simple seleccionado, 1.500–2.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.rmse.timesfm` | 0,761 | RMSE (°C), TimesFM, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.sesgo.timesfm` | −0,075 | Sesgo (°C), TimesFM, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.celdas` | 902 | Celdas, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.n` | 1.317.822 | Filas celda × día, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.rmse.tuned` | 0,849 | RMSE (°C), tuned, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.sesgo.tuned` | −0,021 | Sesgo (°C), tuned, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.brecha.tuned` | −0,088 | Brecha (°C) TimesFM − tuned, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.rmse.tuned_sin_td` | 0,815 | RMSE (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.sesgo.tuned_sin_td` | −0,005 | Sesgo (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.brecha.tuned_sin_td` | −0,054 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.rmse.llr_rezagos_sel` | 0,796 | RMSE (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.sesgo.llr_rezagos_sel` | −0,060 | Sesgo (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.brecha.llr_rezagos_sel` | −0,035 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.rmse.llr_simple_sel` | 0,805 | RMSE (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.sesgo.llr_simple_sel` | −0,070 | Sesgo (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b2500_3500.brecha.llr_simple_sel` | −0,044 | Brecha (°C) TimesFM − LLR simple seleccionado, 2.500–3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.rmse.timesfm` | 0,663 | RMSE (°C), TimesFM, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.sesgo.timesfm` | −0,102 | Sesgo (°C), TimesFM, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.celdas` | 1.537 | Celdas, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.n` | 2.245.557 | Filas celda × día, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.rmse.tuned` | 0,700 | RMSE (°C), tuned, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.sesgo.tuned` | −0,066 | Sesgo (°C), tuned, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.brecha.tuned` | −0,037 | Brecha (°C) TimesFM − tuned, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.rmse.tuned_sin_td` | 0,698 | RMSE (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.sesgo.tuned_sin_td` | −0,048 | Sesgo (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.brecha.tuned_sin_td` | −0,035 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.rmse.llr_rezagos_sel` | 0,687 | RMSE (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.sesgo.llr_rezagos_sel` | −0,063 | Sesgo (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.brecha.llr_rezagos_sel` | −0,024 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.rmse.llr_simple_sel` | 0,695 | RMSE (°C), LLR simple seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.sesgo.llr_simple_sel` | −0,084 | Sesgo (°C), LLR simple seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b500_1500.brecha.llr_simple_sel` | −0,032 | Brecha (°C) TimesFM − LLR simple seleccionado, 500–1.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.rmse.timesfm` | 0,766 | RMSE (°C), TimesFM, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.sesgo.timesfm` | +0,014 | Sesgo (°C), TimesFM, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.celdas` | 2.273 | Celdas, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.n` | 3.320.853 | Filas celda × día, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.rmse.tuned` | 0,867 | RMSE (°C), tuned, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.sesgo.tuned` | +0,125 | Sesgo (°C), tuned, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.brecha.tuned` | −0,100 | Brecha (°C) TimesFM − tuned, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.rmse.tuned_sin_td` | 0,842 | RMSE (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.sesgo.tuned_sin_td` | +0,140 | Sesgo (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.brecha.tuned_sin_td` | −0,076 | Brecha (°C) TimesFM − tuned sin rezagos de Td, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.rmse.llr_rezagos_sel` | 0,802 | RMSE (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.sesgo.llr_rezagos_sel` | +0,023 | Sesgo (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.brecha.llr_rezagos_sel` | −0,035 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.rmse.llr_simple_sel` | 0,806 | RMSE (°C), LLR simple seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.sesgo.llr_simple_sel` | +0,013 | Sesgo (°C), LLR simple seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.b3500_mas.brecha.llr_simple_sel` | −0,039 | Brecha (°C) TimesFM − LLR simple seleccionado, más de 3.500 m, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.rmse.timesfm` | 1,232 | RMSE (°C), TimesFM, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.sesgo.timesfm` | −0,129 | Sesgo (°C), TimesFM, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.celdas` | 8.755 | Celdas, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.n` | 12.791.055 | Filas celda × día, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.rmse.tuned` | 1,322 | RMSE (°C), tuned, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.sesgo.tuned` | −0,247 | Sesgo (°C), tuned, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.brecha.tuned` | −0,090 | Brecha (°C) TimesFM − tuned, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.rmse.tuned_sin_td` | 1,302 | RMSE (°C), tuned sin rezagos de Td, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.sesgo.tuned_sin_td` | −0,208 | Sesgo (°C), tuned sin rezagos de Td, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.brecha.tuned_sin_td` | −0,071 | Brecha (°C) TimesFM − tuned sin rezagos de Td, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.rmse.llr_rezagos_sel` | 1,263 | RMSE (°C), LLR con rezagos seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.sesgo.llr_rezagos_sel` | −0,170 | Sesgo (°C), LLR con rezagos seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.brecha.llr_rezagos_sel` | −0,031 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.rmse.llr_simple_sel` | 1,274 | RMSE (°C), LLR simple seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.sesgo.llr_simple_sel` | −0,189 | Sesgo (°C), LLR simple seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.fuera_peru.brecha.llr_simple_sel` | −0,043 | Brecha (°C) TimesFM − LLR simple seleccionado, fuera de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.rmse.timesfm` | 0,804 | RMSE (°C), TimesFM, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.sesgo.timesfm` | −0,085 | Sesgo (°C), TimesFM, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.celdas` | 8.272 | Celdas, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.n` | 12.085.392 | Filas celda × día, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.rmse.tuned` | 0,861 | RMSE (°C), tuned, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.sesgo.tuned` | −0,060 | Sesgo (°C), tuned, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.brecha.tuned` | −0,056 | Brecha (°C) TimesFM − tuned, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.rmse.tuned_sin_td` | 0,856 | RMSE (°C), tuned sin rezagos de Td, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.sesgo.tuned_sin_td` | −0,034 | Sesgo (°C), tuned sin rezagos de Td, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.brecha.tuned_sin_td` | −0,052 | Brecha (°C) TimesFM − tuned sin rezagos de Td, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.rmse.llr_rezagos_sel` | 0,830 | RMSE (°C), LLR con rezagos seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.sesgo.llr_rezagos_sel` | −0,062 | Sesgo (°C), LLR con rezagos seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.brecha.llr_rezagos_sel` | −0,025 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.rmse.llr_simple_sel` | 0,834 | RMSE (°C), LLR simple seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.sesgo.llr_simple_sel` | −0,083 | Sesgo (°C), LLR simple seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.panel.peru.brecha.llr_simple_sel` | −0,030 | Brecha (°C) TimesFM − LLR simple seleccionado, dentro de Perú, `ll4b`, dominio completo |
| `altitud.ll4b.peru.b0_500.rmse.timesfm` | 0,894 | RMSE (°C), TimesFM, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.sesgo.timesfm` | −0,125 | Sesgo (°C), TimesFM, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.celdas` | 4.185 | Celdas, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.n` | 6.114.285 | Filas celda × día, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.rmse.tuned` | 0,945 | RMSE (°C), tuned, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.sesgo.tuned` | −0,171 | Sesgo (°C), tuned, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.brecha.tuned` | −0,050 | Brecha (°C) TimesFM − tuned, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.rmse.tuned_sin_td` | 0,946 | RMSE (°C), tuned sin rezagos de Td, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.sesgo.tuned_sin_td` | −0,135 | Sesgo (°C), tuned sin rezagos de Td, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.brecha.tuned_sin_td` | −0,051 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.rmse.llr_rezagos_sel` | 0,917 | RMSE (°C), LLR con rezagos seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.sesgo.llr_rezagos_sel` | −0,115 | Sesgo (°C), LLR con rezagos seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.brecha.llr_rezagos_sel` | −0,023 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.rmse.llr_simple_sel` | 0,920 | RMSE (°C), LLR simple seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.sesgo.llr_simple_sel` | −0,143 | Sesgo (°C), LLR simple seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b0_500.brecha.llr_simple_sel` | −0,026 | Brecha (°C) TimesFM − LLR simple seleccionado, 0–500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.rmse.timesfm` | 0,692 | RMSE (°C), TimesFM, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.sesgo.timesfm` | −0,076 | Sesgo (°C), TimesFM, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.celdas` | 636 | Celdas, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.n` | 929.196 | Filas celda × día, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.rmse.tuned` | 0,735 | RMSE (°C), tuned, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.sesgo.tuned` | +0,013 | Sesgo (°C), tuned, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.brecha.tuned` | −0,043 | Brecha (°C) TimesFM − tuned, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.rmse.tuned_sin_td` | 0,729 | RMSE (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.sesgo.tuned_sin_td` | +0,027 | Sesgo (°C), tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.brecha.tuned_sin_td` | −0,036 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.rmse.llr_rezagos_sel` | 0,715 | RMSE (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.sesgo.llr_rezagos_sel` | −0,029 | Sesgo (°C), LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.brecha.llr_rezagos_sel` | −0,023 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.rmse.llr_simple_sel` | 0,725 | RMSE (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.sesgo.llr_simple_sel` | −0,044 | Sesgo (°C), LLR simple seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b1500_2500.brecha.llr_simple_sel` | −0,033 | Brecha (°C) TimesFM − LLR simple seleccionado, 1.500–2.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.rmse.timesfm` | 0,716 | RMSE (°C), TimesFM, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.sesgo.timesfm` | −0,048 | Sesgo (°C), TimesFM, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.celdas` | 630 | Celdas, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.n` | 920.430 | Filas celda × día, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.rmse.tuned` | 0,781 | RMSE (°C), tuned, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.sesgo.tuned` | +0,053 | Sesgo (°C), tuned, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.brecha.tuned` | −0,065 | Brecha (°C) TimesFM − tuned, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.rmse.tuned_sin_td` | 0,762 | RMSE (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.sesgo.tuned_sin_td` | +0,065 | Sesgo (°C), tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.brecha.tuned_sin_td` | −0,047 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.rmse.llr_rezagos_sel` | 0,742 | RMSE (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.sesgo.llr_rezagos_sel` | −0,013 | Sesgo (°C), LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.brecha.llr_rezagos_sel` | −0,026 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.rmse.llr_simple_sel` | 0,750 | RMSE (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.sesgo.llr_simple_sel` | −0,024 | Sesgo (°C), LLR simple seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b2500_3500.brecha.llr_simple_sel` | −0,035 | Brecha (°C) TimesFM − LLR simple seleccionado, 2.500–3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.rmse.timesfm` | 0,611 | RMSE (°C), TimesFM, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.sesgo.timesfm` | −0,085 | Sesgo (°C), TimesFM, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.celdas` | 1.144 | Celdas, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.n` | 1.671.384 | Filas celda × día, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.rmse.tuned` | 0,643 | RMSE (°C), tuned, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.sesgo.tuned` | −0,030 | Sesgo (°C), tuned, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.brecha.tuned` | −0,032 | Brecha (°C) TimesFM − tuned, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.rmse.tuned_sin_td` | 0,644 | RMSE (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.sesgo.tuned_sin_td` | −0,012 | Sesgo (°C), tuned sin rezagos de Td, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.brecha.tuned_sin_td` | −0,033 | Brecha (°C) TimesFM − tuned sin rezagos de Td, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.rmse.llr_rezagos_sel` | 0,635 | RMSE (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.sesgo.llr_rezagos_sel` | −0,037 | Sesgo (°C), LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.brecha.llr_rezagos_sel` | −0,024 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.rmse.llr_simple_sel` | 0,643 | RMSE (°C), LLR simple seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.sesgo.llr_simple_sel` | −0,061 | Sesgo (°C), LLR simple seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b500_1500.brecha.llr_simple_sel` | −0,032 | Brecha (°C) TimesFM − LLR simple seleccionado, 500–1.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.rmse.timesfm` | 0,752 | RMSE (°C), TimesFM, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.sesgo.timesfm` | −0,001 | Sesgo (°C), TimesFM, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.celdas` | 1.677 | Celdas, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.n` | 2.450.097 | Filas celda × día, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.rmse.tuned` | 0,843 | RMSE (°C), tuned, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.sesgo.tuned` | +0,127 | Sesgo (°C), tuned, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.brecha.tuned` | −0,091 | Brecha (°C) TimesFM − tuned, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.rmse.tuned_sin_td` | 0,824 | RMSE (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.sesgo.tuned_sin_td` | +0,142 | Sesgo (°C), tuned sin rezagos de Td, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.brecha.tuned_sin_td` | −0,072 | Brecha (°C) TimesFM − tuned sin rezagos de Td, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.rmse.llr_rezagos_sel` | 0,787 | RMSE (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.sesgo.llr_rezagos_sel` | +0,023 | Sesgo (°C), LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.brecha.llr_rezagos_sel` | −0,035 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.rmse.llr_simple_sel` | 0,791 | RMSE (°C), LLR simple seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.sesgo.llr_simple_sel` | +0,012 | Sesgo (°C), LLR simple seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.peru.b3500_mas.brecha.llr_simple_sel` | −0,039 | Brecha (°C) TimesFM − LLR simple seleccionado, más de 3.500 m, `ll4b`, Perú |
| `altitud.ll4b.panel.vs_tuned.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned.brecha_max_ventaja` | −0,100 | Brecha en la banda de mayor ventaja frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned.brecha_min_ventaja` | −0,037 | Brecha en la banda de menor ventaja frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.brecha_max_ventaja` | −0,076 | Brecha en la banda de mayor ventaja frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.brecha_min_ventaja` | −0,035 | Brecha en la banda de menor ventaja frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_tuned_sin_td.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned sin rezagos de Td, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.brecha_max_ventaja` | −0,035 | Brecha en la banda de mayor ventaja frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.brecha_min_ventaja` | −0,024 | Brecha en la banda de menor ventaja frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_rezagos_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.banda_max_ventaja` | 2.500–3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.brecha_max_ventaja` | −0,044 | Brecha en la banda de mayor ventaja frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.brecha_min_ventaja` | −0,032 | Brecha en la banda de menor ventaja frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.panel.vs_llr_simple_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR simple seleccionado, `ll4b`, dominio completo |
| `altitud.ll4b.peru.vs_tuned.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned.brecha_max_ventaja` | −0,091 | Brecha en la banda de mayor ventaja frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned.brecha_min_ventaja` | −0,032 | Brecha en la banda de menor ventaja frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.brecha_max_ventaja` | −0,072 | Brecha en la banda de mayor ventaja frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.banda_min_ventaja` | 500–1.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.brecha_min_ventaja` | −0,033 | Brecha en la banda de menor ventaja frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_tuned_sin_td.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned sin rezagos de Td, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.brecha_max_ventaja` | −0,035 | Brecha en la banda de mayor ventaja frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.brecha_min_ventaja` | −0,023 | Brecha en la banda de menor ventaja frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_rezagos_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR con rezagos seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.brecha_max_ventaja` | −0,039 | Brecha en la banda de mayor ventaja frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.brecha_min_ventaja` | −0,026 | Brecha en la banda de menor ventaja frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4b.peru.vs_llr_simple_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR simple seleccionado, `ll4b`, Perú |
| `altitud.ll4.panel.vs_tuned.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned.brecha_max_ventaja` | −0,116 | Brecha en la banda de mayor ventaja frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned.banda_min_ventaja` | 1.500–2.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned.brecha_min_ventaja` | −0,058 | Brecha en la banda de menor ventaja frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.brecha_max_ventaja` | −0,091 | Brecha en la banda de mayor ventaja frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.brecha_min_ventaja` | −0,008 | Brecha en la banda de menor ventaja frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_tuned_sin_td.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned sin rezagos de Td, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.brecha_max_ventaja` | −0,049 | Brecha en la banda de mayor ventaja frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.brecha_min_ventaja` | +0,008 | Brecha en la banda de menor ventaja frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.n_bandas_positivas` | 1 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_rezagos_sel.n_bandas_negativas` | 4 | Bandas (de 5) con brecha no positiva frente a LLR con rezagos seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.brecha_max_ventaja` | −0,053 | Brecha en la banda de mayor ventaja frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.brecha_min_ventaja` | −0,009 | Brecha en la banda de menor ventaja frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.panel.vs_llr_simple_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR simple seleccionado, `ll4`, dominio completo |
| `altitud.ll4.peru.vs_tuned.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned.brecha_max_ventaja` | −0,105 | Brecha en la banda de mayor ventaja frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned.banda_min_ventaja` | 1.500–2.500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned.brecha_min_ventaja` | −0,054 | Brecha en la banda de menor ventaja frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.brecha_max_ventaja` | −0,087 | Brecha en la banda de mayor ventaja frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.brecha_min_ventaja` | −0,027 | Brecha en la banda de menor ventaja frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_tuned_sin_td.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a tuned sin rezagos de Td, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.banda_max_ventaja` | más de 3.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.brecha_max_ventaja` | −0,048 | Brecha en la banda de mayor ventaja frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.brecha_min_ventaja` | −0,015 | Brecha en la banda de menor ventaja frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_rezagos_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR con rezagos seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.banda_max_ventaja` | 500–1.500 m | Banda de altitud con la brecha más negativa (mayor ventaja de TimesFM) frente a LLR simple seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.brecha_max_ventaja` | −0,058 | Brecha en la banda de mayor ventaja frente a LLR simple seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.banda_min_ventaja` | 0–500 m | Banda con la brecha menos negativa (menor ventaja) frente a LLR simple seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.brecha_min_ventaja` | −0,033 | Brecha en la banda de menor ventaja frente a LLR simple seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.n_bandas_positivas` | 0 | Bandas (de 5) con brecha positiva (TimesFM peor) frente a LLR simple seleccionado, `ll4`, Perú |
| `altitud.ll4.peru.vs_llr_simple_sel.n_bandas_negativas` | 5 | Bandas (de 5) con brecha no positiva frente a LLR simple seleccionado, `ll4`, Perú |

## zdom

| clave | valor | significado |
|---|---|---|
| `zdom.ll4b.panel.etiqueta` | A (r) A' | Zona SENAMHI con más celdas, `ll4b`, dominio completo |
| `zdom.ll4b.panel.celdas_zona` | 7.091 | Celdas de la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.celdas_ambito` | 17.027 | Celdas del ámbito, `ll4b`, dominio completo |
| `zdom.ll4b.panel.pct_celdas` | 41,6 | Porcentaje de celdas en la zona dominante (sin símbolo %), `ll4b`, dominio completo |
| `zdom.ll4b.panel.pct_filas` | 41,6 | Porcentaje de filas celda × día en la zona dominante (sin símbolo %), `ll4b`, dominio completo |
| `zdom.ll4b.panel.timesfm.rmse_total` | 1,046 | RMSE total (°C), TimesFM, `ll4b`, dominio completo |
| `zdom.ll4b.panel.timesfm.rmse_zona` | 1,316 | RMSE dentro de la zona dominante (°C), TimesFM, `ll4b`, dominio completo |
| `zdom.ll4b.panel.timesfm.rmse_sin_zona` | 0,800 | RMSE sin la zona dominante (°C), TimesFM, `ll4b`, dominio completo |
| `zdom.ll4b.panel.timesfm.pct_sse_zona` | 65,9 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), TimesFM, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned.rmse_total` | 1,122 | RMSE total (°C), tuned, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned.rmse_zona` | 1,408 | RMSE dentro de la zona dominante (°C), tuned, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned.rmse_sin_zona` | 0,861 | RMSE sin la zona dominante (°C), tuned, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned.pct_sse_zona` | 65,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned_sin_td.rmse_total` | 1,108 | RMSE total (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned_sin_td.rmse_zona` | 1,393 | RMSE dentro de la zona dominante (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned_sin_td.rmse_sin_zona` | 0,849 | RMSE sin la zona dominante (°C), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zdom.ll4b.panel.tuned_sin_td.pct_sse_zona` | 65,8 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_rezagos_sel.rmse_total` | 1,074 | RMSE total (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_rezagos_sel.rmse_zona` | 1,349 | RMSE dentro de la zona dominante (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_rezagos_sel.rmse_sin_zona` | 0,824 | RMSE sin la zona dominante (°C), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_rezagos_sel.pct_sse_zona` | 65,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_simple_sel.rmse_total` | 1,083 | RMSE total (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_simple_sel.rmse_zona` | 1,359 | RMSE dentro de la zona dominante (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_simple_sel.rmse_sin_zona` | 0,832 | RMSE sin la zona dominante (°C), LLR simple seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.llr_simple_sel.pct_sse_zona` | 65,5 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR simple seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.clim.rmse_total` | 1,362 | RMSE total (°C), climatología, `ll4b`, dominio completo |
| `zdom.ll4b.panel.clim.rmse_zona` | 1,664 | RMSE dentro de la zona dominante (°C), climatología, `ll4b`, dominio completo |
| `zdom.ll4b.panel.clim.rmse_sin_zona` | 1,096 | RMSE sin la zona dominante (°C), climatología, `ll4b`, dominio completo |
| `zdom.ll4b.panel.clim.pct_sse_zona` | 62,2 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), climatología, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned.total` | −0,076 | Brecha total (°C) TimesFM − tuned, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned.zona` | −0,092 | Brecha (°C) TimesFM − tuned dentro de la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned.sin_zona` | −0,062 | Brecha (°C) TimesFM − tuned sin la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned? `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned_sin_td.total` | −0,062 | Brecha total (°C) TimesFM − tuned sin rezagos de Td, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned_sin_td.zona` | −0,076 | Brecha (°C) TimesFM − tuned sin rezagos de Td dentro de la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned_sin_td.sin_zona` | −0,049 | Brecha (°C) TimesFM − tuned sin rezagos de Td sin la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.tuned_sin_td.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned sin rezagos de Td? `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_rezagos_sel.total` | −0,028 | Brecha total (°C) TimesFM − LLR con rezagos seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_rezagos_sel.zona` | −0,033 | Brecha (°C) TimesFM − LLR con rezagos seleccionado dentro de la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_rezagos_sel.sin_zona` | −0,025 | Brecha (°C) TimesFM − LLR con rezagos seleccionado sin la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_rezagos_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR con rezagos seleccionado? `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_simple_sel.total` | −0,037 | Brecha total (°C) TimesFM − LLR simple seleccionado, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_simple_sel.zona` | −0,042 | Brecha (°C) TimesFM − LLR simple seleccionado dentro de la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_simple_sel.sin_zona` | −0,033 | Brecha (°C) TimesFM − LLR simple seleccionado sin la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.panel.brecha.llr_simple_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR simple seleccionado? `ll4b`, dominio completo |
| `zdom.ll4b.panel.n_rivales_sin_zona_favorece` | 4 | Rivales (de 4) frente a los que TimesFM sigue ganando sin la zona dominante, `ll4b`, dominio completo |
| `zdom.ll4b.peru.etiqueta` | A (r) A' | Zona SENAMHI con más celdas, `ll4b`, Perú |
| `zdom.ll4b.peru.celdas_zona` | 2.147 | Celdas de la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.celdas_ambito` | 8.272 | Celdas del ámbito, `ll4b`, Perú |
| `zdom.ll4b.peru.pct_celdas` | 26,0 | Porcentaje de celdas en la zona dominante (sin símbolo %), `ll4b`, Perú |
| `zdom.ll4b.peru.pct_filas` | 26,0 | Porcentaje de filas celda × día en la zona dominante (sin símbolo %), `ll4b`, Perú |
| `zdom.ll4b.peru.timesfm.rmse_total` | 0,804 | RMSE total (°C), TimesFM, `ll4b`, Perú |
| `zdom.ll4b.peru.timesfm.rmse_zona` | 1,030 | RMSE dentro de la zona dominante (°C), TimesFM, `ll4b`, Perú |
| `zdom.ll4b.peru.timesfm.rmse_sin_zona` | 0,708 | RMSE sin la zona dominante (°C), TimesFM, `ll4b`, Perú |
| `zdom.ll4b.peru.timesfm.pct_sse_zona` | 42,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), TimesFM, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned.rmse_total` | 0,861 | RMSE total (°C), tuned, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned.rmse_zona` | 1,085 | RMSE dentro de la zona dominante (°C), tuned, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned.rmse_sin_zona` | 0,767 | RMSE sin la zona dominante (°C), tuned, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned.pct_sse_zona` | 41,3 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned_sin_td.rmse_total` | 0,856 | RMSE total (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned_sin_td.rmse_zona` | 1,088 | RMSE dentro de la zona dominante (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned_sin_td.rmse_sin_zona` | 0,758 | RMSE sin la zona dominante (°C), tuned sin rezagos de Td, `ll4b`, Perú |
| `zdom.ll4b.peru.tuned_sin_td.pct_sse_zona` | 41,9 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned sin rezagos de Td, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_rezagos_sel.rmse_total` | 0,830 | RMSE total (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_rezagos_sel.rmse_zona` | 1,054 | RMSE dentro de la zona dominante (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_rezagos_sel.rmse_sin_zona` | 0,735 | RMSE sin la zona dominante (°C), LLR con rezagos seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_rezagos_sel.pct_sse_zona` | 41,9 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR con rezagos seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_simple_sel.rmse_total` | 0,834 | RMSE total (°C), LLR simple seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_simple_sel.rmse_zona` | 1,055 | RMSE dentro de la zona dominante (°C), LLR simple seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_simple_sel.rmse_sin_zona` | 0,741 | RMSE sin la zona dominante (°C), LLR simple seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.llr_simple_sel.pct_sse_zona` | 41,5 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR simple seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.clim.rmse_total` | 1,087 | RMSE total (°C), climatología, `ll4b`, Perú |
| `zdom.ll4b.peru.clim.rmse_zona` | 1,278 | RMSE dentro de la zona dominante (°C), climatología, `ll4b`, Perú |
| `zdom.ll4b.peru.clim.rmse_sin_zona` | 1,012 | RMSE sin la zona dominante (°C), climatología, `ll4b`, Perú |
| `zdom.ll4b.peru.clim.pct_sse_zona` | 35,9 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), climatología, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned.total` | −0,056 | Brecha total (°C) TimesFM − tuned, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned.zona` | −0,055 | Brecha (°C) TimesFM − tuned dentro de la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned.sin_zona` | −0,058 | Brecha (°C) TimesFM − tuned sin la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned? `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned_sin_td.total` | −0,052 | Brecha total (°C) TimesFM − tuned sin rezagos de Td, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned_sin_td.zona` | −0,058 | Brecha (°C) TimesFM − tuned sin rezagos de Td dentro de la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned_sin_td.sin_zona` | −0,050 | Brecha (°C) TimesFM − tuned sin rezagos de Td sin la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.tuned_sin_td.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned sin rezagos de Td? `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_rezagos_sel.total` | −0,025 | Brecha total (°C) TimesFM − LLR con rezagos seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_rezagos_sel.zona` | −0,023 | Brecha (°C) TimesFM − LLR con rezagos seleccionado dentro de la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_rezagos_sel.sin_zona` | −0,027 | Brecha (°C) TimesFM − LLR con rezagos seleccionado sin la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_rezagos_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR con rezagos seleccionado? `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_simple_sel.total` | −0,030 | Brecha total (°C) TimesFM − LLR simple seleccionado, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_simple_sel.zona` | −0,024 | Brecha (°C) TimesFM − LLR simple seleccionado dentro de la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_simple_sel.sin_zona` | −0,033 | Brecha (°C) TimesFM − LLR simple seleccionado sin la zona dominante, `ll4b`, Perú |
| `zdom.ll4b.peru.brecha.llr_simple_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR simple seleccionado? `ll4b`, Perú |
| `zdom.ll4b.peru.n_rivales_sin_zona_favorece` | 4 | Rivales (de 4) frente a los que TimesFM sigue ganando sin la zona dominante, `ll4b`, Perú |
| `zdom.ll4.panel.etiqueta` | A (r) A' | Zona SENAMHI con más celdas, `ll4`, dominio completo |
| `zdom.ll4.panel.celdas_zona` | 7.091 | Celdas de la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.celdas_ambito` | 17.027 | Celdas del ámbito, `ll4`, dominio completo |
| `zdom.ll4.panel.pct_celdas` | 41,6 | Porcentaje de celdas en la zona dominante (sin símbolo %), `ll4`, dominio completo |
| `zdom.ll4.panel.pct_filas` | 41,6 | Porcentaje de filas celda × día en la zona dominante (sin símbolo %), `ll4`, dominio completo |
| `zdom.ll4.panel.timesfm.rmse_total` | 1,154 | RMSE total (°C), TimesFM, `ll4`, dominio completo |
| `zdom.ll4.panel.timesfm.rmse_zona` | 1,480 | RMSE dentro de la zona dominante (°C), TimesFM, `ll4`, dominio completo |
| `zdom.ll4.panel.timesfm.rmse_sin_zona` | 0,846 | RMSE sin la zona dominante (°C), TimesFM, `ll4`, dominio completo |
| `zdom.ll4.panel.timesfm.pct_sse_zona` | 68,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), TimesFM, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned.rmse_total` | 1,228 | RMSE total (°C), tuned, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned.rmse_zona` | 1,562 | RMSE dentro de la zona dominante (°C), tuned, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned.rmse_sin_zona` | 0,918 | RMSE sin la zona dominante (°C), tuned, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned.pct_sse_zona` | 67,4 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned_sin_td.rmse_total` | 1,174 | RMSE total (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned_sin_td.rmse_zona` | 1,484 | RMSE dentro de la zona dominante (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned_sin_td.rmse_sin_zona` | 0,890 | RMSE sin la zona dominante (°C), tuned sin rezagos de Td, `ll4`, dominio completo |
| `zdom.ll4.panel.tuned_sin_td.pct_sse_zona` | 66,5 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned sin rezagos de Td, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_rezagos_sel.rmse_total` | 1,157 | RMSE total (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_rezagos_sel.rmse_zona` | 1,466 | RMSE dentro de la zona dominante (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_rezagos_sel.rmse_sin_zona` | 0,871 | RMSE sin la zona dominante (°C), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_rezagos_sel.pct_sse_zona` | 66,9 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_simple_sel.rmse_total` | 1,172 | RMSE total (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_simple_sel.rmse_zona` | 1,481 | RMSE dentro de la zona dominante (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_simple_sel.rmse_sin_zona` | 0,887 | RMSE sin la zona dominante (°C), LLR simple seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.llr_simple_sel.pct_sse_zona` | 66,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR simple seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.clim.rmse_total` | 1,535 | RMSE total (°C), climatología, `ll4`, dominio completo |
| `zdom.ll4.panel.clim.rmse_zona` | 1,872 | RMSE dentro de la zona dominante (°C), climatología, `ll4`, dominio completo |
| `zdom.ll4.panel.clim.rmse_sin_zona` | 1,240 | RMSE sin la zona dominante (°C), climatología, `ll4`, dominio completo |
| `zdom.ll4.panel.clim.pct_sse_zona` | 62,0 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), climatología, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned.total` | −0,074 | Brecha total (°C) TimesFM − tuned, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned.zona` | −0,082 | Brecha (°C) TimesFM − tuned dentro de la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned.sin_zona` | −0,071 | Brecha (°C) TimesFM − tuned sin la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned? `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned_sin_td.total` | −0,021 | Brecha total (°C) TimesFM − tuned sin rezagos de Td, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned_sin_td.zona` | −0,003 | Brecha (°C) TimesFM − tuned sin rezagos de Td dentro de la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned_sin_td.sin_zona` | −0,043 | Brecha (°C) TimesFM − tuned sin rezagos de Td sin la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.tuned_sin_td.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned sin rezagos de Td? `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_rezagos_sel.total` | −0,003 | Brecha total (°C) TimesFM − LLR con rezagos seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_rezagos_sel.zona` | +0,014 | Brecha (°C) TimesFM − LLR con rezagos seleccionado dentro de la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_rezagos_sel.sin_zona` | −0,024 | Brecha (°C) TimesFM − LLR con rezagos seleccionado sin la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_rezagos_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR con rezagos seleccionado? `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_simple_sel.total` | −0,018 | Brecha total (°C) TimesFM − LLR simple seleccionado, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_simple_sel.zona` | −0,001 | Brecha (°C) TimesFM − LLR simple seleccionado dentro de la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_simple_sel.sin_zona` | −0,041 | Brecha (°C) TimesFM − LLR simple seleccionado sin la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.panel.brecha.llr_simple_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR simple seleccionado? `ll4`, dominio completo |
| `zdom.ll4.panel.n_rivales_sin_zona_favorece` | 4 | Rivales (de 4) frente a los que TimesFM sigue ganando sin la zona dominante, `ll4`, dominio completo |
| `zdom.ll4.peru.etiqueta` | A (r) A' | Zona SENAMHI con más celdas, `ll4`, Perú |
| `zdom.ll4.peru.celdas_zona` | 2.147 | Celdas de la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.celdas_ambito` | 8.272 | Celdas del ámbito, `ll4`, Perú |
| `zdom.ll4.peru.pct_celdas` | 26,0 | Porcentaje de celdas en la zona dominante (sin símbolo %), `ll4`, Perú |
| `zdom.ll4.peru.pct_filas` | 26,0 | Porcentaje de filas celda × día en la zona dominante (sin símbolo %), `ll4`, Perú |
| `zdom.ll4.peru.timesfm.rmse_total` | 0,865 | RMSE total (°C), TimesFM, `ll4`, Perú |
| `zdom.ll4.peru.timesfm.rmse_zona` | 1,118 | RMSE dentro de la zona dominante (°C), TimesFM, `ll4`, Perú |
| `zdom.ll4.peru.timesfm.rmse_sin_zona` | 0,757 | RMSE sin la zona dominante (°C), TimesFM, `ll4`, Perú |
| `zdom.ll4.peru.timesfm.pct_sse_zona` | 43,4 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), TimesFM, `ll4`, Perú |
| `zdom.ll4.peru.tuned.rmse_total` | 0,944 | RMSE total (°C), tuned, `ll4`, Perú |
| `zdom.ll4.peru.tuned.rmse_zona` | 1,203 | RMSE dentro de la zona dominante (°C), tuned, `ll4`, Perú |
| `zdom.ll4.peru.tuned.rmse_sin_zona` | 0,835 | RMSE sin la zona dominante (°C), tuned, `ll4`, Perú |
| `zdom.ll4.peru.tuned.pct_sse_zona` | 42,1 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned, `ll4`, Perú |
| `zdom.ll4.peru.tuned_sin_td.rmse_total` | 0,908 | RMSE total (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `zdom.ll4.peru.tuned_sin_td.rmse_zona` | 1,137 | RMSE dentro de la zona dominante (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `zdom.ll4.peru.tuned_sin_td.rmse_sin_zona` | 0,812 | RMSE sin la zona dominante (°C), tuned sin rezagos de Td, `ll4`, Perú |
| `zdom.ll4.peru.tuned_sin_td.pct_sse_zona` | 40,7 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), tuned sin rezagos de Td, `ll4`, Perú |
| `zdom.ll4.peru.llr_rezagos_sel.rmse_total` | 0,891 | RMSE total (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_rezagos_sel.rmse_zona` | 1,124 | RMSE dentro de la zona dominante (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_rezagos_sel.rmse_sin_zona` | 0,793 | RMSE sin la zona dominante (°C), LLR con rezagos seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_rezagos_sel.pct_sse_zona` | 41,3 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR con rezagos seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_simple_sel.rmse_total` | 0,906 | RMSE total (°C), LLR simple seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_simple_sel.rmse_zona` | 1,139 | RMSE dentro de la zona dominante (°C), LLR simple seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_simple_sel.rmse_sin_zona` | 0,809 | RMSE sin la zona dominante (°C), LLR simple seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.llr_simple_sel.pct_sse_zona` | 41,0 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), LLR simple seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.clim.rmse_total` | 1,262 | RMSE total (°C), climatología, `ll4`, Perú |
| `zdom.ll4.peru.clim.rmse_zona` | 1,518 | RMSE dentro de la zona dominante (°C), climatología, `ll4`, Perú |
| `zdom.ll4.peru.clim.rmse_sin_zona` | 1,159 | RMSE sin la zona dominante (°C), climatología, `ll4`, Perú |
| `zdom.ll4.peru.clim.pct_sse_zona` | 37,6 | Porcentaje del error cuadrático total que aporta la zona dominante (sin símbolo %), climatología, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned.total` | −0,079 | Brecha total (°C) TimesFM − tuned, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned.zona` | −0,085 | Brecha (°C) TimesFM − tuned dentro de la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned.sin_zona` | −0,078 | Brecha (°C) TimesFM − tuned sin la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned? `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned_sin_td.total` | −0,043 | Brecha total (°C) TimesFM − tuned sin rezagos de Td, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned_sin_td.zona` | −0,019 | Brecha (°C) TimesFM − tuned sin rezagos de Td dentro de la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned_sin_td.sin_zona` | −0,056 | Brecha (°C) TimesFM − tuned sin rezagos de Td sin la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.tuned_sin_td.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a tuned sin rezagos de Td? `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_rezagos_sel.total` | −0,026 | Brecha total (°C) TimesFM − LLR con rezagos seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_rezagos_sel.zona` | −0,006 | Brecha (°C) TimesFM − LLR con rezagos seleccionado dentro de la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_rezagos_sel.sin_zona` | −0,036 | Brecha (°C) TimesFM − LLR con rezagos seleccionado sin la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_rezagos_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR con rezagos seleccionado? `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_simple_sel.total` | −0,041 | Brecha total (°C) TimesFM − LLR simple seleccionado, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_simple_sel.zona` | −0,021 | Brecha (°C) TimesFM − LLR simple seleccionado dentro de la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_simple_sel.sin_zona` | −0,052 | Brecha (°C) TimesFM − LLR simple seleccionado sin la zona dominante, `ll4`, Perú |
| `zdom.ll4.peru.brecha.llr_simple_sel.sin_zona_favorece` | sí | ¿La brecha sin la zona dominante sigue favoreciendo a TimesFM frente a LLR simple seleccionado? `ll4`, Perú |
| `zdom.ll4.peru.n_rivales_sin_zona_favorece` | 4 | Rivales (de 4) frente a los que TimesFM sigue ganando sin la zona dominante, `ll4`, Perú |

## enso

| clave | valor | significado |
|---|---|---|
| `enso.ll4b.panel.el_nino.meses` | 9 | Meses de la clase ONI, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.n` | 4.665.398 | Filas celda × día de la clase, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.celdas` | 17.027 | Celdas con filas en la clase, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.timesfm` | 0,995 | RMSE (°C), TimesFM, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.timesfm` | +0,074 | Sesgo (°C), TimesFM, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.tuned` | 1,005 | RMSE (°C), tuned, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.tuned` | +0,009 | Sesgo (°C), tuned, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.tuned_sin_td` | 1,012 | RMSE (°C), tuned sin rezagos de Td, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.tuned_sin_td` | +0,076 | Sesgo (°C), tuned sin rezagos de Td, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.llr_rezagos_sel` | 1,000 | RMSE (°C), LLR con rezagos seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.llr_rezagos_sel` | +0,086 | Sesgo (°C), LLR con rezagos seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.llr_simple_sel` | 0,998 | RMSE (°C), LLR simple seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.llr_simple_sel` | +0,025 | Sesgo (°C), LLR simple seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.rmse.clim` | 1,246 | RMSE (°C), climatología, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.sesgo.clim` | −0,441 | Sesgo (°C), climatología, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.brecha.tuned` | −0,009 | Brecha (°C) TimesFM − tuned, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.brecha.tuned_sin_td` | −0,016 | Brecha (°C) TimesFM − tuned sin rezagos de Td, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.brecha.llr_rezagos_sel` | −0,005 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.el_nino.brecha.llr_simple_sel` | −0,003 | Brecha (°C) TimesFM − LLR simple seleccionado, El Niño, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.meses` | 22 | Meses de la clase ONI, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.n` | 11.374.036 | Filas celda × día de la clase, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.celdas` | 17.027 | Celdas con filas en la clase, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.timesfm` | 1,016 | RMSE (°C), TimesFM, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.timesfm` | −0,163 | Sesgo (°C), TimesFM, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.tuned` | 1,109 | RMSE (°C), tuned, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.tuned` | −0,211 | Sesgo (°C), tuned, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.tuned_sin_td` | 1,088 | RMSE (°C), tuned sin rezagos de Td, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.tuned_sin_td` | −0,184 | Sesgo (°C), tuned sin rezagos de Td, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.llr_rezagos_sel` | 1,052 | RMSE (°C), LLR con rezagos seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.llr_rezagos_sel` | −0,189 | Sesgo (°C), LLR con rezagos seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.llr_simple_sel` | 1,065 | RMSE (°C), LLR simple seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.llr_simple_sel` | −0,191 | Sesgo (°C), LLR simple seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.rmse.clim` | 1,338 | RMSE (°C), climatología, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.sesgo.clim` | −0,229 | Sesgo (°C), climatología, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.brecha.tuned` | −0,093 | Brecha (°C) TimesFM − tuned, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.brecha.tuned_sin_td` | −0,072 | Brecha (°C) TimesFM − tuned sin rezagos de Td, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.brecha.llr_rezagos_sel` | −0,036 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.la_nina.brecha.llr_simple_sel` | −0,049 | Brecha (°C) TimesFM − LLR simple seleccionado, La Niña, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.meses` | 17 | Meses de la clase ONI, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.n` | 8.837.013 | Filas celda × día de la clase, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.celdas` | 17.027 | Celdas con filas en la clase, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.timesfm` | 1,110 | RMSE (°C), TimesFM, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.timesfm` | −0,132 | Sesgo (°C), TimesFM, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.tuned` | 1,195 | RMSE (°C), tuned, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.tuned` | −0,173 | Sesgo (°C), tuned, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.tuned_sin_td` | 1,181 | RMSE (°C), tuned sin rezagos de Td, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.tuned_sin_td` | −0,151 | Sesgo (°C), tuned sin rezagos de Td, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.llr_rezagos_sel` | 1,139 | RMSE (°C), LLR con rezagos seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.llr_rezagos_sel` | −0,131 | Sesgo (°C), LLR con rezagos seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.llr_simple_sel` | 1,148 | RMSE (°C), LLR simple seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.llr_simple_sel` | −0,154 | Sesgo (°C), LLR simple seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.rmse.clim` | 1,448 | RMSE (°C), climatología, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.sesgo.clim` | −0,317 | Sesgo (°C), climatología, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.brecha.tuned` | −0,085 | Brecha (°C) TimesFM − tuned, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.brecha.tuned_sin_td` | −0,071 | Brecha (°C) TimesFM − tuned sin rezagos de Td, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.brecha.llr_rezagos_sel` | −0,030 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.neutral.brecha.llr_simple_sel` | −0,038 | Brecha (°C) TimesFM − LLR simple seleccionado, neutral, `ll4b`, dominio completo |
| `enso.ll4b.panel.meses_total` | 48 | Meses del bloque clasificados por ONI, `ll4b`, dominio completo |
| `enso.ll4b.panel.n_clases_favorece.tuned` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned es negativa, `ll4b`, dominio completo |
| `enso.ll4b.panel.n_clases_favorece.tuned_sin_td` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned sin rezagos de Td es negativa, `ll4b`, dominio completo |
| `enso.ll4b.panel.n_clases_favorece.llr_rezagos_sel` | 3 | Clases ENSO (de 3) en que la brecha frente a LLR con rezagos seleccionado es negativa, `ll4b`, dominio completo |
| `enso.ll4b.panel.n_clases_favorece.llr_simple_sel` | 3 | Clases ENSO (de 3) en que la brecha frente a LLR simple seleccionado es negativa, `ll4b`, dominio completo |
| `enso.ll4b.peru.el_nino.meses` | 9 | Meses de la clase ONI, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.n` | 2.266.528 | Filas celda × día de la clase, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.celdas` | 8.272 | Celdas con filas en la clase, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.timesfm` | 0,767 | RMSE (°C), TimesFM, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.timesfm` | +0,034 | Sesgo (°C), TimesFM, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.tuned` | 0,780 | RMSE (°C), tuned, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.tuned` | +0,021 | Sesgo (°C), tuned, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.tuned_sin_td` | 0,787 | RMSE (°C), tuned sin rezagos de Td, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.tuned_sin_td` | +0,080 | Sesgo (°C), tuned sin rezagos de Td, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.llr_rezagos_sel` | 0,769 | RMSE (°C), LLR con rezagos seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.llr_rezagos_sel` | +0,061 | Sesgo (°C), LLR con rezagos seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.llr_simple_sel` | 0,773 | RMSE (°C), LLR simple seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.llr_simple_sel` | −0,010 | Sesgo (°C), LLR simple seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.rmse.clim` | 1,055 | RMSE (°C), climatología, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.sesgo.clim` | −0,431 | Sesgo (°C), climatología, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.brecha.tuned` | −0,013 | Brecha (°C) TimesFM − tuned, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.brecha.tuned_sin_td` | −0,020 | Brecha (°C) TimesFM − tuned sin rezagos de Td, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.brecha.llr_rezagos_sel` | −0,002 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.el_nino.brecha.llr_simple_sel` | −0,006 | Brecha (°C) TimesFM − LLR simple seleccionado, El Niño, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.meses` | 22 | Meses de la clase ONI, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.n` | 5.525.696 | Filas celda × día de la clase, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.celdas` | 8.272 | Celdas con filas en la clase, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.timesfm` | 0,769 | RMSE (°C), TimesFM, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.timesfm` | −0,081 | Sesgo (°C), TimesFM, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.tuned` | 0,832 | RMSE (°C), tuned, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.tuned` | −0,038 | Sesgo (°C), tuned, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.tuned_sin_td` | 0,827 | RMSE (°C), tuned sin rezagos de Td, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.tuned_sin_td` | −0,030 | Sesgo (°C), tuned sin rezagos de Td, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.llr_rezagos_sel` | 0,800 | RMSE (°C), LLR con rezagos seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.llr_rezagos_sel` | −0,063 | Sesgo (°C), LLR con rezagos seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.llr_simple_sel` | 0,810 | RMSE (°C), LLR simple seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.llr_simple_sel` | −0,059 | Sesgo (°C), LLR simple seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.rmse.clim` | 1,038 | RMSE (°C), climatología, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.sesgo.clim` | −0,025 | Sesgo (°C), climatología, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.brecha.tuned` | −0,063 | Brecha (°C) TimesFM − tuned, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.brecha.tuned_sin_td` | −0,058 | Brecha (°C) TimesFM − tuned sin rezagos de Td, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.brecha.llr_rezagos_sel` | −0,031 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.la_nina.brecha.llr_simple_sel` | −0,041 | Brecha (°C) TimesFM − LLR simple seleccionado, La Niña, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.meses` | 17 | Meses de la clase ONI, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.n` | 4.293.168 | Filas celda × día de la clase, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.celdas` | 8.272 | Celdas con filas en la clase, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.timesfm` | 0,866 | RMSE (°C), TimesFM, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.timesfm` | −0,153 | Sesgo (°C), TimesFM, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.tuned` | 0,935 | RMSE (°C), tuned, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.tuned` | −0,132 | Sesgo (°C), tuned, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.tuned_sin_td` | 0,924 | RMSE (°C), tuned sin rezagos de Td, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.tuned_sin_td` | −0,100 | Sesgo (°C), tuned sin rezagos de Td, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.llr_rezagos_sel` | 0,895 | RMSE (°C), LLR con rezagos seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.llr_rezagos_sel` | −0,126 | Sesgo (°C), LLR con rezagos seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.llr_simple_sel` | 0,894 | RMSE (°C), LLR simple seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.llr_simple_sel` | −0,153 | Sesgo (°C), LLR simple seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.rmse.clim` | 1,163 | RMSE (°C), climatología, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.sesgo.clim` | −0,312 | Sesgo (°C), climatología, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.brecha.tuned` | −0,069 | Brecha (°C) TimesFM − tuned, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.brecha.tuned_sin_td` | −0,058 | Brecha (°C) TimesFM − tuned sin rezagos de Td, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.brecha.llr_rezagos_sel` | −0,029 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.neutral.brecha.llr_simple_sel` | −0,028 | Brecha (°C) TimesFM − LLR simple seleccionado, neutral, `ll4b`, Perú |
| `enso.ll4b.peru.meses_total` | 48 | Meses del bloque clasificados por ONI, `ll4b`, Perú |
| `enso.ll4b.peru.n_clases_favorece.tuned` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned es negativa, `ll4b`, Perú |
| `enso.ll4b.peru.n_clases_favorece.tuned_sin_td` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned sin rezagos de Td es negativa, `ll4b`, Perú |
| `enso.ll4b.peru.n_clases_favorece.llr_rezagos_sel` | 3 | Clases ENSO (de 3) en que la brecha frente a LLR con rezagos seleccionado es negativa, `ll4b`, Perú |
| `enso.ll4b.peru.n_clases_favorece.llr_simple_sel` | 3 | Clases ENSO (de 3) en que la brecha frente a LLR simple seleccionado es negativa, `ll4b`, Perú |
| `enso.ll4.panel.el_nino.meses` | 20 | Meses de la clase ONI, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.n` | 10.369.443 | Filas celda × día de la clase, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.celdas` | 17.027 | Celdas con filas en la clase, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.timesfm` | 1,096 | RMSE (°C), TimesFM, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.timesfm` | −0,058 | Sesgo (°C), TimesFM, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.tuned` | 1,259 | RMSE (°C), tuned, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.tuned` | −0,209 | Sesgo (°C), tuned, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.tuned_sin_td` | 1,161 | RMSE (°C), tuned sin rezagos de Td, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.tuned_sin_td` | −0,131 | Sesgo (°C), tuned sin rezagos de Td, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.llr_rezagos_sel` | 1,128 | RMSE (°C), LLR con rezagos seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.llr_rezagos_sel` | −0,106 | Sesgo (°C), LLR con rezagos seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.llr_simple_sel` | 1,148 | RMSE (°C), LLR simple seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.llr_simple_sel` | −0,175 | Sesgo (°C), LLR simple seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.rmse.clim` | 1,641 | RMSE (°C), climatología, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.sesgo.clim` | −0,665 | Sesgo (°C), climatología, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.brecha.tuned` | −0,163 | Brecha (°C) TimesFM − tuned, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.brecha.tuned_sin_td` | −0,065 | Brecha (°C) TimesFM − tuned sin rezagos de Td, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.brecha.llr_rezagos_sel` | −0,032 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.el_nino.brecha.llr_simple_sel` | −0,052 | Brecha (°C) TimesFM − LLR simple seleccionado, El Niño, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.meses` | 1 | Meses de la clase ONI, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.n` | 527.837 | Filas celda × día de la clase, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.celdas` | 17.027 | Celdas con filas en la clase, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.timesfm` | 1,241 | RMSE (°C), TimesFM, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.timesfm` | −0,266 | Sesgo (°C), TimesFM, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.tuned` | 1,310 | RMSE (°C), tuned, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.tuned` | −0,295 | Sesgo (°C), tuned, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.tuned_sin_td` | 1,238 | RMSE (°C), tuned sin rezagos de Td, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.tuned_sin_td` | −0,275 | Sesgo (°C), tuned sin rezagos de Td, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.llr_rezagos_sel` | 1,230 | RMSE (°C), LLR con rezagos seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.llr_rezagos_sel` | −0,269 | Sesgo (°C), LLR con rezagos seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.llr_simple_sel` | 1,251 | RMSE (°C), LLR simple seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.llr_simple_sel` | −0,332 | Sesgo (°C), LLR simple seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.rmse.clim` | 1,781 | RMSE (°C), climatología, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.sesgo.clim` | −0,625 | Sesgo (°C), climatología, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.brecha.tuned` | −0,069 | Brecha (°C) TimesFM − tuned, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.brecha.tuned_sin_td` | +0,003 | Brecha (°C) TimesFM − tuned sin rezagos de Td, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.brecha.llr_rezagos_sel` | +0,012 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.la_nina.brecha.llr_simple_sel` | −0,009 | Brecha (°C) TimesFM − LLR simple seleccionado, La Niña, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.meses` | 27 | Meses de la clase ONI, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.n` | 13.979.167 | Filas celda × día de la clase, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.celdas` | 17.027 | Celdas con filas en la clase, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.timesfm` | 1,191 | RMSE (°C), TimesFM, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.timesfm` | +0,239 | Sesgo (°C), TimesFM, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.tuned` | 1,201 | RMSE (°C), tuned, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.tuned` | +0,108 | Sesgo (°C), tuned, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.tuned_sin_td` | 1,181 | RMSE (°C), tuned sin rezagos de Td, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.tuned_sin_td` | +0,133 | Sesgo (°C), tuned sin rezagos de Td, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.llr_rezagos_sel` | 1,175 | RMSE (°C), LLR con rezagos seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.llr_rezagos_sel` | +0,152 | Sesgo (°C), LLR con rezagos seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.llr_simple_sel` | 1,186 | RMSE (°C), LLR simple seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.llr_simple_sel` | +0,138 | Sesgo (°C), LLR simple seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.rmse.clim` | 1,441 | RMSE (°C), climatología, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.sesgo.clim` | −0,129 | Sesgo (°C), climatología, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.brecha.tuned` | −0,010 | Brecha (°C) TimesFM − tuned, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.brecha.tuned_sin_td` | +0,010 | Brecha (°C) TimesFM − tuned sin rezagos de Td, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.brecha.llr_rezagos_sel` | +0,017 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.neutral.brecha.llr_simple_sel` | +0,005 | Brecha (°C) TimesFM − LLR simple seleccionado, neutral, `ll4`, dominio completo |
| `enso.ll4.panel.meses_total` | 48 | Meses del bloque clasificados por ONI, `ll4`, dominio completo |
| `enso.ll4.panel.n_clases_favorece.tuned` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned es negativa, `ll4`, dominio completo |
| `enso.ll4.panel.n_clases_favorece.tuned_sin_td` | 1 | Clases ENSO (de 3) en que la brecha frente a tuned sin rezagos de Td es negativa, `ll4`, dominio completo |
| `enso.ll4.panel.n_clases_favorece.llr_rezagos_sel` | 1 | Clases ENSO (de 3) en que la brecha frente a LLR con rezagos seleccionado es negativa, `ll4`, dominio completo |
| `enso.ll4.panel.n_clases_favorece.llr_simple_sel` | 2 | Clases ENSO (de 3) en que la brecha frente a LLR simple seleccionado es negativa, `ll4`, dominio completo |
| `enso.ll4.peru.el_nino.meses` | 20 | Meses de la clase ONI, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.n` | 5.037.648 | Filas celda × día de la clase, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.celdas` | 8.272 | Celdas con filas en la clase, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.timesfm` | 0,837 | RMSE (°C), TimesFM, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.timesfm` | −0,053 | Sesgo (°C), TimesFM, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.tuned` | 0,950 | RMSE (°C), tuned, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.tuned` | −0,121 | Sesgo (°C), tuned, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.tuned_sin_td` | 0,889 | RMSE (°C), tuned sin rezagos de Td, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.tuned_sin_td` | −0,062 | Sesgo (°C), tuned sin rezagos de Td, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.llr_rezagos_sel` | 0,865 | RMSE (°C), LLR con rezagos seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.llr_rezagos_sel` | −0,072 | Sesgo (°C), LLR con rezagos seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.llr_simple_sel` | 0,891 | RMSE (°C), LLR simple seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.llr_simple_sel` | −0,155 | Sesgo (°C), LLR simple seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.rmse.clim` | 1,357 | RMSE (°C), climatología, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.sesgo.clim` | −0,613 | Sesgo (°C), climatología, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.brecha.tuned` | −0,113 | Brecha (°C) TimesFM − tuned, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.brecha.tuned_sin_td` | −0,052 | Brecha (°C) TimesFM − tuned sin rezagos de Td, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.brecha.llr_rezagos_sel` | −0,028 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.el_nino.brecha.llr_simple_sel` | −0,054 | Brecha (°C) TimesFM − LLR simple seleccionado, El Niño, `ll4`, Perú |
| `enso.ll4.peru.la_nina.meses` | 1 | Meses de la clase ONI, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.n` | 256.432 | Filas celda × día de la clase, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.celdas` | 8.272 | Celdas con filas en la clase, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.timesfm` | 0,970 | RMSE (°C), TimesFM, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.timesfm` | −0,163 | Sesgo (°C), TimesFM, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.tuned` | 1,022 | RMSE (°C), tuned, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.tuned` | −0,145 | Sesgo (°C), tuned, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.tuned_sin_td` | 0,983 | RMSE (°C), tuned sin rezagos de Td, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.tuned_sin_td` | −0,130 | Sesgo (°C), tuned sin rezagos de Td, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.llr_rezagos_sel` | 0,968 | RMSE (°C), LLR con rezagos seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.llr_rezagos_sel` | −0,158 | Sesgo (°C), LLR con rezagos seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.llr_simple_sel` | 0,990 | RMSE (°C), LLR simple seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.llr_simple_sel` | −0,217 | Sesgo (°C), LLR simple seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.rmse.clim` | 1,403 | RMSE (°C), climatología, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.sesgo.clim` | −0,382 | Sesgo (°C), climatología, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.brecha.tuned` | −0,053 | Brecha (°C) TimesFM − tuned, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.brecha.tuned_sin_td` | −0,013 | Brecha (°C) TimesFM − tuned sin rezagos de Td, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.brecha.llr_rezagos_sel` | +0,002 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.la_nina.brecha.llr_simple_sel` | −0,020 | Brecha (°C) TimesFM − LLR simple seleccionado, La Niña, `ll4`, Perú |
| `enso.ll4.peru.neutral.meses` | 27 | Meses de la clase ONI, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.n` | 6.791.312 | Filas celda × día de la clase, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.celdas` | 8.272 | Celdas con filas en la clase, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.timesfm` | 0,881 | RMSE (°C), TimesFM, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.timesfm` | +0,134 | Sesgo (°C), TimesFM, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.tuned` | 0,937 | RMSE (°C), tuned, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.tuned` | +0,112 | Sesgo (°C), tuned, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.tuned_sin_td` | 0,918 | RMSE (°C), tuned sin rezagos de Td, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.tuned_sin_td` | +0,136 | Sesgo (°C), tuned sin rezagos de Td, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.llr_rezagos_sel` | 0,906 | RMSE (°C), LLR con rezagos seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.llr_rezagos_sel` | +0,120 | Sesgo (°C), LLR con rezagos seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.llr_simple_sel` | 0,914 | RMSE (°C), LLR simple seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.llr_simple_sel` | +0,098 | Sesgo (°C), LLR simple seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.rmse.clim` | 1,180 | RMSE (°C), climatología, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.sesgo.clim` | −0,066 | Sesgo (°C), climatología, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.brecha.tuned` | −0,055 | Brecha (°C) TimesFM − tuned, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.brecha.tuned_sin_td` | −0,037 | Brecha (°C) TimesFM − tuned sin rezagos de Td, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.brecha.llr_rezagos_sel` | −0,025 | Brecha (°C) TimesFM − LLR con rezagos seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.neutral.brecha.llr_simple_sel` | −0,033 | Brecha (°C) TimesFM − LLR simple seleccionado, neutral, `ll4`, Perú |
| `enso.ll4.peru.meses_total` | 48 | Meses del bloque clasificados por ONI, `ll4`, Perú |
| `enso.ll4.peru.n_clases_favorece.tuned` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned es negativa, `ll4`, Perú |
| `enso.ll4.peru.n_clases_favorece.tuned_sin_td` | 3 | Clases ENSO (de 3) en que la brecha frente a tuned sin rezagos de Td es negativa, `ll4`, Perú |
| `enso.ll4.peru.n_clases_favorece.llr_rezagos_sel` | 2 | Clases ENSO (de 3) en que la brecha frente a LLR con rezagos seleccionado es negativa, `ll4`, Perú |
| `enso.ll4.peru.n_clases_favorece.llr_simple_sel` | 3 | Clases ENSO (de 3) en que la brecha frente a LLR simple seleccionado es negativa, `ll4`, Perú |
| `enso.umbral_oni` | 0,5 | Umbral del ONI (°C) para clasificar los meses |

## preentrenamiento

| clave | valor | significado |
|---|---|---|
| `preentrenamiento.reanalisis_anio_ini` | 1989 | Primer año de ERA5 en GiftEvalPretrain |
| `preentrenamiento.reanalisis_anio_fin` | 2018 | Último año de ERA5 en GiftEvalPretrain |
| `preentrenamiento.reanalisis_anios` | 30 | Años (directorios) de ERA5 en GiftEvalPretrain |
| `preentrenamiento.reanalisis_grilla_grados` | 2,8125 | Resolución de la grilla de ERA5 y CMIP6 en LOTSA (°) |
| `preentrenamiento.reanalisis_grilla` | 64 × 128 | Dimensiones de la grilla (latitud × longitud) |
| `preentrenamiento.reanalisis_celdas_por_anio` | 8.192 | Series por año en ERA5 (64 × 128 celdas) |
| `preentrenamiento.reanalisis_series` | 245.760 | Series de ERA5 en GIFT-Eval/LOTSA |
| `preentrenamiento.reanalisis_variables` | 45 | Variables (canales) de ERA5 |
| `preentrenamiento.reanalisis_puntos` | 2.146.959.000 | Puntos de tiempo de ERA5 |
| `preentrenamiento.reanalisis_frecuencia` | horaria | Frecuencia de ERA5 en GiftEvalPretrain |
| `preentrenamiento.cmip6_anio_ini` | 1850 | Primer año de CMIP6 en GiftEvalPretrain |
| `preentrenamiento.cmip6_anio_fin` | 2010 | Último año de CMIP6 en GiftEvalPretrain |
| `preentrenamiento.cmip6_paso_anios` | 5 | Paso (años) entre carpetas de CMIP6 |
| `preentrenamiento.cmip6_series` | 1.351.680 | Series de CMIP6 |
| `preentrenamiento.cmip6_variables` | 53 | Variables de CMIP6 |
| `preentrenamiento.gifteval_univariadas` | 71 | Conjuntos univariados de GiftEvalPretrain |
| `preentrenamiento.gifteval_multivariadas` | 17 | Conjuntos multivariados de GiftEvalPretrain |
| `preentrenamiento.gifteval_carpetas` | 152 | Carpetas de GiftEvalPretrain en el Hub |
| `preentrenamiento.gifteval_series_millones` | 4,5 | Series de GiftEvalPretrain (millones) |
| `preentrenamiento.gifteval_puntos_miles_de_millones` | 230 | Puntos de GiftEvalPretrain (miles de millones) |
| `preentrenamiento.gifteval_dominios` | 7 | Dominios de GiftEvalPretrain |
| `preentrenamiento.parche_entrada` | 32 | Largo del parche de entrada (días) |
| `preentrenamiento.parche_salida` | 64 | Largo del parche de salida (días) |
| `preentrenamiento.solapamiento` | 32 | Solapamiento entre parches de salida (días) |
| `preentrenamiento.horizonte_dias` | 1.461 | Horizonte decodificado (días) |
| `preentrenamiento.n_parches` | 45 | Parches de pronóstico que cubren el horizonte de 1.461 días |
| `preentrenamiento.horizonte_relleno` | 1.472 | Horizonte rellenado (días) |
| `preentrenamiento.n_parches_horizonte` | 46 | Parches de horizonte tras el relleno |
| `preentrenamiento.contexto_max` | 15.360 | Contexto máximo del código (días) |
| `preentrenamiento.max_variates` | 32 | Máximo de series (variates) por pasada |

## tuned

| clave | valor | significado |
|---|---|---|
| `tuned.ll4.referencia_limpia_palacios` | n. d. | Cifra limpia de referencia de Palacios para `tuned` en `ll4` (no está en las fuentes numéricas permitidas; solo se informa el RMSE de a1_por_metodo.csv (rmse4.ll4.panel.tuned)) |
