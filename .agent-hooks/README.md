# Hooks de sincronización beads → GitHub

Propagan el cierre de un bead a la capa de ejecución, respetando la separación
de responsabilidades del proyecto:

```
NOTION            conocimiento / investigación   (append-only, aún NO tocado)
  |
  v
GITHUB PROJECT    ejecución / planificación      <- este hook escribe aquí
  |
  v
ISSUE -> CODEX -> branch -> PR -> tests/CI -> merge -> issue Done
```

## Qué hace

Al detectar `bd close <bead>` (o `bd update <bead> --status closed`) en un
comando Bash ejecutado por el agente:

1. resuelve el Bead ID contra el cuerpo de los issues (`Bead ID: \`tdew-xxx\``);
2. cierra el GitHub Issue correspondiente;
3. fija `Status = Done` en el Project, sin depender de los workflows de la UI;
4. deja un resumen **encolado** en `pending-notion/` para Notion.

## Notion está desactivado a propósito

`TDEW_NOTION_SYNC=off` es el valor por defecto: **no se escribe nada en Notion**.
Los resúmenes se acumulan como ficheros locales. Cuando se migre esa pata, el
writer debe ser *append-only*: añadir un bloque de resumen a la página, nunca
sobrescribirla ni cambiar sus propiedades.

## Instalación

Ambos agentes leen la config del repo. No hace falta nada más que tener `gh`
autenticado con scopes `repo` y `project`.

- Claude Code: `.claude/settings.json`
- Codex: `.codex/hooks.json` — requiere confiar el hook la primera vez
  con `/hooks` en la CLI (Codex no ejecuta hooks no gestionados sin revisión).

## Variables

| Variable | Default | Uso |
|---|---|---|
| `TDEW_REPO` | `nakato156-CGIAR/tdew` | repo destino |
| `TDEW_PROJECT_OWNER` | `nakato156-CGIAR` | owner del Project |
| `TDEW_PROJECT_NUMBER` | `1` | número del Project |
| `TDEW_NOTION_SYNC` | `off` | `on` activa la pata de Notion |
| `TDEW_HOOK_DEBUG` | — | `1` para trazas por stderr |

## Garantías

- Nunca bloquea al agente: cualquier fallo se registra y sale con código 0.
- Idempotente: reejecutarlo sobre un bead ya cerrado no cambia nada.
- No toca código del proyecto ni crea ramas ni PRs.
