# Wiki de investigación — mantenida por agentes LLM (Claude y Codex)

Este directorio es una wiki mantenida por agentes LLM (Claude, Codex, otros) que combina
el flujo de trabajo de la "LLM Wiki" de Andrej Karpathy con la estructura del
Open Knowledge Format (OKF) de Google Cloud. Su dominio es investigación en general:
IA/LLMs, ML clásico, matemática, estadística, y cualquier otra área relevante para el
proyecto tdew — papers, repos de GitHub, notebooks de Colab, artículos y páginas web
sobre modelos, técnicas, benchmarks, datasets y herramientas. No está limitado a un
subcampo específico; cualquier fuente de investigación seria es candidata a `/ingest`.

Este mismo archivo existe también como `AGENTS.md` (contenido equivalente) para que
Codex lo lea automáticamente; cualquier agente debe seguir las reglas de ambos por igual.

## Capas

- `raw/` — capturas **inmutables** de fuentes originales (`urls/`, `papers/`, `github/`, `colab/`).
  Ningún agente edita un archivo de `raw/` después de crearlo; si una fuente cambia, se
  captura de nuevo con un slug distinto.
- `knowledge/` — bundle estilo OKF, la única capa que los agentes reescriben, y solo a
  través de las operaciones definidas más abajo (nunca a mano, nunca fuera de una operación).
- `queries/` — respuestas de `/synthesize` archivadas para no repetir síntesis ya hechas.
- `.claude/commands/` — definición de las operaciones como comandos slash para Claude Code.
- `.codex/prompts/` — las mismas definiciones de operaciones, en el formato de prompts
  personalizados que usa Codex CLI.

## Taxonomía de `knowledge/`

Cada concepto pertenece a exactamente uno de estos 6 tipos (campo `type`, obligatorio):

- **Method** — un procedimiento o técnica reproducible (p.ej. una técnica de fine-tuning, un algoritmo de sampling).
- **Tool** — software, librería, API o servicio concreto que alguien puede usar.
- **Pattern** — una solución recurrente observada en ≥1 fuente, no atada a una sola implementación.
- **Finding** — un resultado empírico u observación reportada en una fuente (un benchmark, una medición, un experimento).
- **Decision** — una elección de diseño/arquitectura tomada (por un paper, un proyecto, o por esta propia wiki) junto con su justificación.
- **Source** — el resumen de una fuente cruda ingerida (una por cada archivo en `raw/`).

Si un agente duda entre dos tipos, elige el más específico (`Finding` sobre `Pattern` si es un solo resultado puntual; `Method` sobre `Tool` si describe un procedimiento en vez de un producto).

## Frontmatter de cada archivo en `knowledge/`

```yaml
---
type: Method            # Method | Tool | Pattern | Finding | Decision | Source — obligatorio
title: Título humano
description: Resumen de una línea
resource: https://...   # link a la fuente autoritativa (paper, repo, url, colab)
tags: [tag1, tag2]
timestamp: 2026-09-11T00:00:00Z
status: draft            # draft | reviewed | stable
contributed_by: [claude] # agentes que han tocado este archivo
sources: ["[[sources/slug]]"]  # wiki-links a knowledge/sources/
---
```

Solo `type` es obligatorio (regla dura, heredada de OKF). El resto es convención que todo agente debe respetar para que `/lint` y `/synthesize` funcionen.

## Enlaces

Usa sintaxis `[[wiki-link]]` (compatible con Obsidian) para referenciar otro archivo de
`knowledge/` por su slug, p.ej. `[[methods/lora-finetuning]]`. Toda afirmación no trivial
en un archivo de `knowledge/` debe poder rastrearse a un `[[sources/slug]]` y/o su `resource`.

## Protocolo multi-agente

Varios agentes (Claude, Codex, otros) pueden ingerir sobre el mismo repositorio, en
secuencia o en paralelo:

- Un archivo nuevo o modificado se escribe siempre con `status: draft`, y el agente que
  lo tocó se añade a `contributed_by` (sin eliminar agentes previos).
- Ningún agente sobreescribe directamente un archivo con `status: reviewed` o `stable`.
  Si tiene información nueva para ese concepto, añade un bloque `> **CONTRADICTION**` (ver
  abajo) o dependencia paralela, y deja que `/reconcile` decida.
- `/reconcile` es quien fusiona borradores concurrentes, promueve `status` y resuelve
  contradicciones — nunca se hace a mano ni dentro de `/ingest`.

Formato de contradicción:

```markdown
> **CONTRADICTION** (detectada 2026-09-11, agentes: claude vs codex)
> Fuente A ([[sources/paper-x]]) afirma que Y; Fuente B ([[sources/paper-z]]) afirma lo contrario.
> Sin resolver — pendiente de `/reconcile`.
```

## Las 5 operaciones

1. **`/ingest <fuente>`** — captura una fuente nueva (URL, paper, repo GitHub, notebook
   Colab) en `raw/`, redacta su resumen en `knowledge/sources/`, y propone (`status: draft`)
   entradas nuevas/actualizadas en `methods/`, `tools/`, `patterns/`, `findings/`, `decisions/`.
   Actualiza `knowledge/index.md` y añade una línea a `knowledge/log.md`. Termina en un commit.
2. **`/reconcile`** — recorre los `status: draft` de `knowledge/`, fusiona los que no
   contradicen (promueve a `reviewed`, une `contributed_by`), y marca con
   `> **CONTRADICTION**` los que sí. Registra en `log.md`. Termina en un commit.
3. **`/synthesize <pregunta>`** — responde una pregunta leyendo `knowledge/index.md` y las
   páginas relevantes (prioriza `status: reviewed`/`stable` sobre `draft`), citando
   `[[wiki-links]]` y `resource`. Opcionalmente archiva la respuesta en `queries/`.
4. **`/update <slug>`** — revisa un concepto puntual existente sin pasar por un ingest
   completo (fuente que lo supera, link roto, decisión reconsiderada). Actualiza
   `timestamp` y `contributed_by`, y cascada a las páginas que lo referencian.
5. **`/lint`** — chequeo de salud: páginas huérfanas, `[[links]]` rotos, `type` faltante,
   `status: draft` sin reconciliar por mucho tiempo, fuentes en `sources/` sin ningún
   concepto que las cite, `timestamp` obsoleto frente a `resource`.

Codex no siempre soporta comandos slash de proyecto: si `/ingest` etc. no aparecen como
comandos, sigue el mismo procedimiento leyendo directamente el archivo correspondiente en
`.codex/prompts/<operación>.md` (contenido idéntico a `.claude/commands/`) como instrucciones
a ejecutar paso a paso.

## Provenance

Cada operación termina en un commit git — el historial de commits es la capa de
provenance (principio de OKF: confiar en el control de versiones, no en un schema de
confianza separado). No se usan ramas por agente; `contributed_by` + `status` en el
frontmatter bastan para rastrear autoría y madurez.
