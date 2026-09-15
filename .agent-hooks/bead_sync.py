#!/usr/bin/env python3
"""
bead_sync.py — Propaga el cierre de un bead a la capa de ejecución (GitHub).

Flujo (ver .agent-hooks/README.md):

    bd close tdew-xxx
            |
            v
    [este hook]  ---> GitHub Issue: closed
                 ---> GitHub Project: Status = Done
                 ---> Notion: resumen  (DESACTIVADO por defecto; se encola)

Se invoca como hook PostToolUse desde Claude Code (.claude/settings.json)
y desde Codex (.codex/hooks.json). Ambos entregan el mismo JSON por stdin
con tool_input.command.

REGLA DE ORO: este hook nunca bloquea al agente. Cualquier fallo se registra
y se sale con código 0.

Variables de entorno:
    TDEW_REPO            default "nakato156-CGIAR/tdew"
    TDEW_PROJECT_OWNER   default "nakato156-CGIAR"
    TDEW_PROJECT_NUMBER  default "1"
    TDEW_NOTION_SYNC     "off" (default) | "on"
    TDEW_HOOK_DEBUG      "1" para trazas en el log
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = os.environ.get("TDEW_REPO", "nakato156-CGIAR/tdew")
OWNER = os.environ.get("TDEW_PROJECT_OWNER", "nakato156-CGIAR")
PROJECT = os.environ.get("TDEW_PROJECT_NUMBER", "1")
NOTION_SYNC = os.environ.get("TDEW_NOTION_SYNC", "off").lower()
DEBUG = os.environ.get("TDEW_HOOK_DEBUG") == "1"

HOOK_DIR = Path(__file__).resolve().parent
LOG = HOOK_DIR / "sync.log"
NOTION_QUEUE = HOOK_DIR / "pending-notion"

# `bd close tdew-abc`, `bd close tdew-abc tdew-def`,
# `bd update tdew-abc --status closed|done|completed`
BEAD_RE = re.compile(r"\btdew-[a-z0-9]{3,}\b", re.I)
CLOSE_RE = re.compile(
    r"\bbd\b[^\n|;&]*?(?:\bclose\b|--status[=\s]+(?:closed|done|completed))",
    re.I,
)


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}"
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass
    if DEBUG:
        print(line, file=sys.stderr)


def gh(args, parse_json=False):
    """Ejecuta gh. Devuelve None ante cualquier fallo (fail-open)."""
    try:
        out = subprocess.run(
            ["gh"] + args,
            capture_output=True, text=True, timeout=60, check=False,
        )
    except Exception as exc:
        log(f"  gh EXC {' '.join(args[:3])}: {exc}")
        return None
    if out.returncode != 0:
        log(f"  gh FAIL {' '.join(args[:3])}: {out.stderr.strip()[:200]}")
        return None
    if not parse_json:
        return out.stdout
    try:
        return json.loads(out.stdout)
    except Exception:
        return None


def extract_beads(command):
    """Devuelve los bead IDs de un comando de cierre, o [] si no lo es."""
    if not command or not CLOSE_RE.search(command):
        return []
    # Ignora flags tipo --status=closed al recoger ids
    return sorted({m.group(0).lower() for m in BEAD_RE.finditer(command)})


def find_issue(bead):
    """
    Localiza el issue cuyo cuerpo declara este Bead ID.
    Vía REST: la búsqueda de gh usa GraphQL y es la primera en toparse
    con rate limits secundarios.
    """
    data = gh([
        "api", "--paginate",
        f"repos/{REPO}/issues?state=all&per_page=100",
    ], parse_json=True)
    if not data:
        return None
    needle = f"bead id: `{bead}`"
    for issue in data:
        if "pull_request" in issue:
            continue
        if needle in (issue.get("body") or "").lower():
            return {
                "number": issue["number"],
                "title": issue.get("title", ""),
                "state": (issue.get("state") or "").upper(),
                "body": issue.get("body") or "",
            }
    return None


def set_project_done(issue_number):
    """Fija Status=Done en el Project. Independiente de los workflows de la UI."""
    items = gh([
        "project", "item-list", PROJECT, "--owner", OWNER,
        "--format", "json", "--limit", "100",
    ], parse_json=True)
    if not items:
        return False
    item_id = next(
        (it["id"] for it in items.get("items", [])
         if (it.get("content") or {}).get("number") == issue_number),
        None,
    )
    if not item_id:
        log(f"  #{issue_number} no está en el Project {PROJECT}")
        return False

    pid = gh(["project", "view", PROJECT, "--owner", OWNER,
              "--format", "json", "--jq", ".id"])
    fields = gh(["project", "field-list", PROJECT, "--owner", OWNER,
                 "--format", "json"], parse_json=True)
    if not pid or not fields:
        return False
    status = next((f for f in fields.get("fields", []) if f.get("name") == "Status"), None)
    if not status:
        return False
    done = next((o["id"] for o in status.get("options", []) if o["name"] == "Done"), None)
    if not done:
        return False

    return gh([
        "project", "item-edit", "--id", item_id, "--project-id", pid.strip(),
        "--field-id", status["id"], "--single-select-option-id", done,
    ]) is not None


def queue_notion(bead, issue):
    """
    Notion es la capa de conocimiento: aquí sólo se deja el resumen preparado.
    Mientras TDEW_NOTION_SYNC != "on" NO se escribe nada en Notion.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    NOTION_QUEUE.mkdir(parents=True, exist_ok=True)
    path = NOTION_QUEUE / f"{stamp}-{bead}.md"
    body = (issue.get("body") or "")
    notion_url = ""
    m = re.search(r"Notion source:\s*(\S+)", body)
    if m:
        notion_url = m.group(1)

    path.write_text(
        f"# Cierre de {bead}\n\n"
        f"- Bead ID: `{bead}`\n"
        f"- GitHub Issue: #{issue['number']} — {issue['title']}\n"
        f"- URL: https://github.com/{REPO}/issues/{issue['number']}\n"
        f"- Notion source: {notion_url or '(no declarada en el issue)'}\n"
        f"- Cerrado: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
        f"## Resumen pendiente de redactar\n\n"
        f"_Qué se hizo, qué evidencia quedó, qué decisión se tomó._\n",
        encoding="utf-8",
    )
    log(f"  Notion: encolado en {path.name} (sync={NOTION_SYNC})")

    if NOTION_SYNC == "on":
        # Punto de extensión deliberadamente vacío.
        # Cuando se migre esta pata, escribir aquí contra la API de Notion
        # APPEND-ONLY: añadir un bloque de resumen, nunca sobrescribir la página.
        log("  Notion: sync=on pero el writer aún no está implementado (no-op)")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    command = (payload.get("tool_input") or {}).get("command", "")
    beads = extract_beads(command)
    if not beads:
        sys.exit(0)

    log(f"cierre detectado: {beads} :: {command[:120]}")
    done = []

    for bead in beads:
        issue = find_issue(bead)
        if not issue:
            log(f"  {bead}: sin issue asociado en {REPO}")
            continue
        n = issue["number"]
        if issue.get("state", "").upper() == "OPEN":
            if gh(["issue", "close", str(n), "--repo", REPO,
                   "--reason", "completed"]) is not None:
                log(f"  {bead}: issue #{n} cerrado")
        else:
            log(f"  {bead}: issue #{n} ya estaba cerrado")
        if set_project_done(n):
            log(f"  {bead}: Project Status=Done para #{n}")
        queue_notion(bead, issue)
        done.append(f"{bead} -> #{n}")

    if done:
        # Contexto visible para el modelo, sin bloquear nada.
        print(json.dumps({
            "systemMessage": "Sincronizado con GitHub: " + ", ".join(done)
        }))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail-open pase lo que pase
        log(f"ERROR no controlado: {exc}")
        sys.exit(0)
