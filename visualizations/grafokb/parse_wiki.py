"""
visualizations.grafokb.parse_wiki

Parses ``Wiki/knowledge/**/*.md`` (the OKF-style knowledge base described in
``Wiki/CLAUDE.md``) into a plain list of concept dicts, for
``build_graph.py`` to turn into a node/edge graph.

Frontmatter is simple enough (scalars, quoted strings, ``[a, b, c]`` lists)
that a small hand-rolled parser covers it without adding a PyYAML
dependency to the project.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KNOWLEDGE_DIR = REPO_ROOT / "Wiki" / "knowledge"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+?)(?:\|[^\[\]]*)?\]\]")


def _parse_scalar(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def _parse_value(raw: str) -> str | list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(item) for item in inner.split(",")]
    return _parse_scalar(raw)


def parse_frontmatter(text: str) -> dict[str, str | list[str]]:
    """Best-effort parse of the ``---\\n...\\n---`` frontmatter block used
    throughout ``Wiki/knowledge/`` (see ``Wiki/CLAUDE.md``). Unknown/extra
    keys pass through untouched."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str | list[str]] = {}
    key = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, raw_value = line.partition(":")
            fields[key.strip()] = _parse_value(raw_value)
        elif key is not None:
            # continuation line of a multi-line value; not used by this
            # wiki's frontmatter today, but don't silently drop it.
            prev = fields.get(key, "")
            fields[key] = f"{prev} {line.strip()}".strip()
    return fields


def extract_wikilinks(text: str) -> list[str]:
    """Every ``[[slug]]`` (or ``[[slug|label]]``) occurrence in ``text``,
    in order, deduplicated."""
    seen: list[str] = []
    for m in WIKILINK_RE.finditer(text):
        slug = m.group(1).strip()
        if slug not in seen:
            seen.append(slug)
    return seen


@dataclass
class Concept:
    slug: str  # e.g. "methods/stgcn-graph-conv-forecasting"
    type: str = "Unknown"
    title: str = ""
    description: str = ""
    resource: str = ""
    tags: list[str] = field(default_factory=list)
    status: str = "draft"
    contributed_by: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)  # outgoing [[wikilinks]], frontmatter + body


def _as_list(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value] if value else []


def load_concepts(knowledge_dir: Path = DEFAULT_KNOWLEDGE_DIR) -> list[Concept]:
    """One :class:`Concept` per ``knowledge/<category>/<slug>.md`` file
    (``index.md`` files are the wiki's own table of contents, not concepts,
    so they're skipped)."""
    concepts = []
    for path in sorted(knowledge_dir.glob("*/*.md")):
        if path.name == "index.md":
            continue
        slug = f"{path.parent.name}/{path.stem}"
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        body = text[len(FRONTMATTER_RE.match(text).group(0)):] if FRONTMATTER_RE.match(text) else text

        links = list(_as_list(fm.get("sources")))
        for link in extract_wikilinks(body):
            if link not in links:
                links.append(link)
        # a wikilink written as e.g. "[[sources/foo]]" inside a quoted
        # frontmatter string still has the brackets; strip them here too.
        links = [WIKILINK_RE.sub(r"\1", link) if link.startswith("[[") else link for link in links]

        concepts.append(
            Concept(
                slug=slug,
                type=str(fm.get("type", "Unknown")),
                title=str(fm.get("title", slug)),
                description=str(fm.get("description", "")),
                resource=str(fm.get("resource", "")),
                tags=_as_list(fm.get("tags")),
                status=str(fm.get("status", "draft")),
                contributed_by=_as_list(fm.get("contributed_by")),
                links=links,
            )
        )
    return concepts
