---
description: Chequeo de salud de knowledge/ (huérfanos, links rotos, drafts viejos, staleness)
---

Recorre todo `knowledge/` y reporta (sin modificar nada todavía):

1. **`type` faltante** — cualquier archivo sin el campo `type` en su frontmatter (única regla dura heredada de OKF).
2. **Enlaces rotos** — cualquier `[[slug]]` que no corresponda a un archivo existente en `knowledge/`.
3. **Páginas huérfanas** — archivos en `knowledge/` que ningún `index.md` ni otro archivo referencia.
4. **Drafts estancados** — archivos con `status: draft` cuyo `timestamp` es más antiguo que ~2-4 semanas y que no tienen una contradicción activa (candidatos a correr `/reconcile`).
5. **Fuentes no aprovechadas** — archivos en `knowledge/sources/` que ningún Method/Tool/Pattern/Finding/Decision cita.
6. **Staleness** — archivos cuyo `resource` (si es una URL) probablemente cambió desde `timestamp` (heurística: mucho tiempo transcurrido + tipo de recurso volátil como un repo activo).
7. **Contradicciones sin resolver** — bloques `> **CONTRADICTION**` que llevan mucho tiempo sin pasar por `/reconcile`.

Presenta los hallazgos agrupados por categoría, con la ruta de archivo de cada uno. Al final, pregunta al usuario si quiere que apliques automáticamente las correcciones seguras (arreglar un link roto obvio, actualizar `index.md` con páginas huérfanas) — no apliques nada sin confirmación, ya que `/lint` es de solo diagnóstico por defecto. Si el usuario aprueba correcciones, aplícalas y haz commit `lint: <resumen>`.
