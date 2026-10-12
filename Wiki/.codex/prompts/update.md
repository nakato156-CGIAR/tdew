---
description: Revisa un concepto puntual existente en knowledge/ sin pasar por un ingest completo
---

Slug o concepto a actualizar: $ARGUMENTS

Pasos:

1. Localiza el archivo en `knowledge/<tipo>/<slug>.md`. Si no existe, informa al usuario en vez de crearlo (para eso está `/ingest`).
2. Determina el motivo de la actualización (nueva fuente que lo supera, `[[link]]` roto detectado, una `Decision` reconsiderada, etc.) y aplica el cambio mínimo necesario.
3. Actualiza `timestamp` y añade el agente actual a `contributed_by` si no estaba.
4. Si el cambio es sustancial (no solo una corrección menor), baja `status` a `draft` para que pase por `/reconcile` antes de considerarse estable de nuevo.
5. Revisa qué otras páginas de `knowledge/` referencian este slug vía `[[...]]` y actualízalas en cascada si el cambio las afecta (p.ej. una `Decision` que ya no aplica).
6. Actualiza `knowledge/index.md` si el título o resumen cambiaron, y añade una línea a `knowledge/log.md`.
7. Haz commit con mensaje `update: <slug>`.

Reporta al final qué cambió y qué páginas se actualizaron en cascada.
