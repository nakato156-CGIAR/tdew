---
description: Responde una pregunta usando el conocimiento sintetizado en knowledge/
---

Pregunta: $ARGUMENTS

Pasos:

1. Lee `knowledge/index.md` para identificar qué páginas son relevantes para la pregunta.
2. Lee esas páginas de `knowledge/` (prioriza `status: reviewed` o `stable` sobre `draft`; si solo hay `draft` relevante, úsalo pero adviértelo en la respuesta).
3. Sigue los `[[wiki-links]]` necesarios para completar el contexto (multi-hop si hace falta).
4. Redacta la respuesta citando cada afirmación con su `[[wiki-link]]` y, cuando aporte valor, el `resource` original.
5. Si detectas que la pregunta no está bien cubierta por el conocimiento actual, dilo explícitamente en vez de inventar contenido, y sugiere qué fuente convendría ingerir.
6. Pregunta al usuario (o decide por defecto que sí, si se está corriendo en modo no interactivo) si se debe archivar la respuesta en `queries/<slug-de-la-pregunta>.md`. Si se archiva, añade una línea a `knowledge/log.md` y haz commit `synthesize: <slug>`.

Devuelve la respuesta directamente al usuario, no solo un resumen de lo que harías.
