# Preparación del paper nuevo: LLR frente a TimesFM

Se reúnen las guías narrativas y los resultados para redactar el artículo nuevo. Las fuentes Quarto, la bibliografía y las figuras ya existen (ver el mapa de carpetas). La orientación vigente se fija en [ORIENTACION_PAPER.md](ORIENTACION_PAPER.md), se desarrolla en [historia_paper.md](historia_paper.md) y se organiza por secciones en [paper_narrative.md](paper_narrative.md). El registro de las correcciones está en [REVISION_COHERENCIA.md](REVISION_COHERENCIA.md).

Se compara la reconstrucción de Td con Tmin observada del bloque, sobre PISCO y con los mismos insumos locales. Se presenta primero `ll4b` (2009–2012), que no participó en la selección de la configuración de TimesFM; `ll4` (2013–2016) se informa como evaluación retrospectiva expuesta a esa selección. Se conserva la tesis E acotada; la regla E/C+A está retirada.

Las cifras se toman de los CSV de `resultados/` y del cribado limpio. Los informes de resultados describen su alcance; la cercanía de métricas no establece equivalencia ni igualdad de predicciones. El historial mínimo necesario no se determinó. En el costo se separan selección única de configuración, inferencia y total con selección incluida.

`reports/paper/` y `PAPER_PLAN.md` pertenecen al artículo previo de Palacios y no se modifican. Los materiales del artículo nuevo se escriben en esta carpeta; cualquier reutilización del artículo previo requiere atribución. Los scripts de cálculo existentes permanecen en `experiments/`; esta revisión solo modifica documentos dentro de `reports/paper_nuevo/`.

Antes de redactar se aplica `ESTILO_REDACCION.md`. Se declara el uso de IA generativa y se mantiene la revisión científica con Palacios y SENAMHI antes de trasladar el contenido al artículo. No se han publicado estos cambios ni se ha actualizado el artefacto situado fuera de esta carpeta.


## Regeneración

Todo el código vive en `experiments/paper_nuevo/` y se ejecuta con `uv run`:

```bash
uv run python -m experiments.paper_nuevo.analisis_inferencia    # IC, bootstrap, Diebold–Mariano (resultados r1)
uv run python -m experiments.paper_nuevo.analisis_descriptivo   # horizonte, calibración, ENSO, altitud, extremos (r2)
uv run python -m experiments.paper_nuevo.costo_llr_sel          # costo de las LLR seleccionadas (r3)
uv run python -m experiments.paper_nuevo.cli todo               # cifras (+ _variables.yml), tablas y figuras
```

El orden importa: primero los análisis, después `cli todo`. `cli` acepta también `cifras`, `tablas` o `figuras` por separado.

## Render

```bash
cd reports/paper_nuevo
quarto render paper.qmd --to typst && quarto render paper.qmd --to html
quarto render suplemento.qmd --to typst && quarto render suplemento.qmd --to html
```

## Mapa de carpetas

- `secciones/`: texto del cuerpo (`00_resumen.qmd` a `11_conclusion.qmd`); `paper.qmd` y `suplemento.qmd` los incluyen.
- `tablas/`: tablas generadas (`tab*.md`, `s*.md` y sus CSV con proveniencia). `tab6_resumen` es la tabla de costo del cuerpo; `tab6` (detalle completo) y `s7` (lista de corridas) están en el suplemento S7.
- `figuras/`: figuras en PNG, PDF y SVG; `FIGURAS.md` describe cada una.
- `cifras/`: `cifras.csv` (cada cifra con fuente y filtro) y `CLAVES.md`; de ahí sale `_variables.yml`. Ningún número de resultado se escribe a mano en los `.qmd`.
- `resultados/`: CSV de entrada. `a1_*`, `a3_*` y `a4_*` provienen de los análisis previos; `r1_*` (inferencia), `r2_*` (descriptivo) y `r3_*` (costo de LLR seleccionadas) los producen los scripts anteriores.
- `revisiones/` y `REVISION_COHERENCIA.md`: informes de los revisores y correcciones de coherencia.
- `references.bib`, `apa.csl`, `bib_verificacion.md`: bibliografía y su verificación.

## Marcadores pendientes en el texto

- `[[CITA: ficha o DOI de PISCO Td v1.1 ...]]` (introducción).
- `[[FALTA: número de estaciones de Td usadas por PISCO v1.1 y su fuente]]` (introducción).
- `[[PENDIENTE: depósito de predicciones]]` y `[[PENDIENTE: licencia y condiciones de acceso de PISCO]]` (disponibilidad de código y datos).
- Autores, instituciones y firmas de validación figuran como `[pendiente]`.

`tests/test_paper_nuevo_qmd.py::test_no_pending_markers_*` falla mientras existan estos marcadores.
