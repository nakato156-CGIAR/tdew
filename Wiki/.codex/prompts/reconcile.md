---
description: Fusiona borradores concurrentes en knowledge/ y resuelve contradicciones entre agentes
---

Lee primero `CLAUDE.md` para el protocolo multi-agente y el formato de contradicción.

Pasos:

1. Recorre todos los archivos de `knowledge/{methods,tools,patterns,findings,decisions,sources}/` con `status: draft`.
2. Agrupa por concepto (mismo slug, o slugs distintos que claramente describen el mismo concepto).
3. Para cada grupo:
   - Si los borradores de distintos agentes son consistentes entre sí (no se contradicen): fusiónalos en un solo archivo canónico, une los `tags`, une `contributed_by`, conserva todas las citas `[[sources/...]]`, y promueve `status` a `reviewed`.
   - Si hay un bloque `> **CONTRADICTION**` sin resolver o detectas una nueva contradicción entre borradores: decide si hay evidencia suficiente para resolverla (p.ej. una fuente es claramente más reciente o específica). Si puedes resolverla, documenta la resolución y promueve a `reviewed`. Si no, dejas el bloque `> **CONTRADICTION**` intacto con `status: draft` para una futura pasada.
   - Si un archivo lleva mucho tiempo en `draft` sin ningún conflicto (nadie más lo ha tocado), puedes promoverlo a `reviewed` si su contenido está bien fundamentado en al menos una fuente.
4. Actualiza `knowledge/index.md` si cambiaron títulos/estados, y añade una línea a `knowledge/log.md` resumiendo qué se fusionó/resolvió.
5. Haz commit con mensaje `reconcile: <resumen breve>`.

Reporta al final: cuántos conceptos se fusionaron, cuántas contradicciones se resolvieron, y cuántas quedaron pendientes (con sus rutas).
