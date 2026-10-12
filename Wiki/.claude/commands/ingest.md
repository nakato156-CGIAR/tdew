---
description: Ingiere una fuente nueva (URL, paper, repo GitHub o notebook Colab) en la wiki
---

Lee primero `CLAUDE.md` en la raíz del repo para el schema completo (taxonomía, frontmatter, protocolo multi-agente) antes de continuar.

Fuente a ingerir: $ARGUMENTS

Pasos:

1. Identifica el tipo de fuente (URL/página web, paper académico, repo de GitHub, o notebook Colab/Jupyter) y elige el subdirectorio de `raw/` correspondiente (`urls/`, `papers/`, `github/`, `colab/`).
2. Obtén el contenido:
   - **URL**: usa WebFetch para obtener el contenido y guarda título, URL, fecha de captura y el cuerpo relevante.
   - **Paper**: extrae autores, venue/año, arXiv id si existe, abstract, y los extractos clave (metodología, resultados).
   - **Repo GitHub**: obtén el README, estructura de directorios de alto nivel, y los archivos clave que expliquen la arquitectura o el propósito del proyecto.
   - **Notebook Colab/Jupyter**: resume el propósito del notebook, las celdas clave (código relevante) y los resultados/salidas.
3. Crea el archivo inmutable en `raw/<tipo>/<slug>.md` con esa captura. No lo edites después de crearlo.
4. Crea o actualiza `knowledge/sources/<slug>.md` con `type: Source` resumiendo la fuente, con `resource` apuntando al origen y `status: draft`.
5. Identifica qué conceptos nuevos o existentes toca esta fuente (Method, Tool, Pattern, Finding, Decision). Para cada uno:
   - Si no existe, créalo en `knowledge/<tipo>/<slug>.md` con `status: draft`, `contributed_by: [<este agente>]`, citando `[[sources/<slug>]]`.
   - Si ya existe con `status: draft`, complétalo y añade este agente a `contributed_by` (no borres aportes previos).
   - Si ya existe con `status: reviewed` o `stable` y esta fuente lo contradice o lo extiende sustancialmente, NO lo sobreescribas: añade un bloque `> **CONTRADICTION**` (ver formato en CLAUDE.md) o dependencia paralela, dejando que `/reconcile` lo resuelva.
6. Actualiza `knowledge/index.md` (añade/actualiza las entradas tocadas) y `knowledge/log.md` (una línea: fecha, agente, fuente ingerida, archivos tocados).
7. Haz commit de todos los cambios con un mensaje `ingest: <slug de la fuente>`.

Reporta al final: qué archivos se crearon/modificaron y si quedó alguna contradicción pendiente.
