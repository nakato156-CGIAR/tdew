# experiments/paper_nuevo

Código que produce cada cifra, tabla y figura del paper nuevo (`reports/paper_nuevo/`). Regla del proyecto: ningún número del texto se escribe a mano; el `.qmd` lo toma de `_variables.yml` con `{{< var clave >}}` o incluye una tabla generada.

## Uso

```bash
uv run python -m experiments.paper_nuevo.cli cifras   # _variables.yml, cifras/cifras.csv, cifras/CLAVES.md
uv run python -m experiments.paper_nuevo.cli tablas   # tablas/<id>.md y tablas/<id>.csv
uv run python -m experiments.paper_nuevo.cli figuras  # delega en experiments/paper_nuevo/figuras.py
uv run python -m experiments.paper_nuevo.cli todo
```

Las salidas son deterministas (mismos bytes en dos corridas). La proveniencia de `cifras.csv` y de los CSV de tablas se registra en `reports/metric_provenance.jsonl` solo cuando cambia su contenido.

## Módulos

| Módulo | Función |
|---|---|
| `fuentes.py` | Rutas de todas las entradas y salidas, relativas al repositorio. |
| `formato.py` | Formato en español: coma decimal, punto de miles desde 1.000 (como el texto narrativo), menos tipográfico U+2212, redondeo mitad hacia arriba, duraciones (`73 min 10 s`, `39 h 27 min`, `≈5,1 días`). |
| `datos.py` | Lectura de las fuentes en un objeto; no transforma cifras. |
| `cifras.py` | Calcula todas las cifras que cita `paper_narrative.md`. Cada clave lleva archivo y filtro de origen. Lo que no existe en las fuentes sale como `n. d.` con una nota. |
| `tablas.py` | Tab1–Tab6 y S1–S7 desde las claves de `cifras.py`. |
| `cli.py` | Punto de entrada. |
| `figuras.py`, `estilo.py` | Figuras (otro autor); `cli figuras` los importa solo al pedirlos. |

## Fuentes numéricas

`reports/paper_nuevo/resultados/`: `a1_por_metodo.csv`, `a1_brechas.csv`, `a1_por_zona.csv`, `a1_victorias_zona.csv`, `a1_escalera_contexto*.csv`, `a3_control_tmin_barajada.csv`, `a4_*` (solo la versión base, sin `_h4b2` y sin filas de ERA5), `costo.csv` y la tabla «Insumos de diseño» de `costo.md`; además `reports/timesfm_benchmark/cribado_limpio/leaderboard.csv` y `reports/timesfm_benchmark/panels/nacional_17027.csv`. `zone_table.parquet` (en `$RES`, ver `experiments/timesfm/paths.py`) solo aporta el conteo de 41 unidades cartográficas; sin él, esas tres claves salen `n. d.`. `HANDOFF.md` no es fuente numérica.

## Convenciones

- Brecha = RMSE(A) − RMSE(B) en °C; negativa favorece a A (TimesFM). Las brechas anuales y por zona son descriptivas, sin IC.
- Claves anidadas con puntos: `rmse.ll4b.panel.timesfm`, `brecha.ll4.panel.timesfm_vs_tuned.v`, `costo.ll4b.timesfm_total.tiempo`. Los años van como `a2013`, los inicios de contexto como `i2002`. `timesfm` es `timesfm_anom` (`tmin_anom_full`); `timesfm_td` y `timesfm_med` (contexto desde 2002) conservan sufijo.
- La lista completa de claves, con su significado, está en `reports/paper_nuevo/cifras/CLAVES.md`.
- Los textos cualitativos de la Tabla 1 (zonas, búsqueda previa, ajuste, datos por celda, licencia «No aplica») están en `tablas.py` con su origen citado; no contienen cifras.

## Pruebas

`tests/test_paper_nuevo_cifras.py` recalcula claves representativas desde los CSV fuente, comprueba el determinismo y que los archivos en disco coincidan con la salida actual. `tests/test_metric_provenance.py` registra los CSV de `cifras/` y `tablas/`.

Se usó IA generativa (Claude) para escribir este código; las cifras y su formato deben validarse con las fuentes antes de publicarse.
