"""
visualizations.grafokb.build_graph

Renders ``Wiki/knowledge/`` as a single self-contained HTML file: an
interactive node/edge graph (vis-network, loaded from a CDN — open the file
with an internet connection) with three toggleable views over the facets
the wiki's frontmatter actually supports today (see the conversation that
asked for this: type/status/tags are real fields, "limitations" is not):

- **Tipo**: color nodes by ``type`` (Method/Tool/Pattern/Finding/Decision/Source).
- **Estado**: color nodes by ``status`` (draft/reviewed/stable).
- **Tags**: pick one or more tags to dim every node that has none of them.
- **Fuente**: pick a Source node to highlight everything reachable from it
  (the concepts it gave rise to), dimming the rest.

An edge is drawn for every ``[[wiki-link]]`` found (frontmatter ``sources:``
field, or a ``[[...]]`` in the body) that resolves to another concept that
exists; dangling links (a source not yet ingested, e.g.) are dropped from
the graph and printed to stderr instead of silently disappearing.

Usage
-----
python -m visualizations.grafokb.build_graph
    [--knowledge-dir Wiki/knowledge] [--out visualizations/grafokb/output/wiki_graph.html]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from visualizations.grafokb.parse_wiki import DEFAULT_KNOWLEDGE_DIR, Concept, load_concepts

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path(__file__).resolve().parent / "output" / "wiki_graph.html"

TYPE_COLORS = {
    "Method": "#4f8dfd",
    "Tool": "#3fb984",
    "Pattern": "#c77dff",
    "Finding": "#f2a03d",
    "Decision": "#e85d75",
    "Source": "#9aa5b1",
    "Unknown": "#666666",
}

STATUS_COLORS = {
    "draft": "#e85d75",
    "reviewed": "#4f8dfd",
    "stable": "#3fb984",
}


def build_graph_data(concepts: list[Concept]) -> tuple[list[dict], list[dict]]:
    by_slug = {c.slug: c for c in concepts}

    nodes = [
        {
            "id": c.slug,
            "label": c.title,
            "type": c.type,
            "status": c.status,
            "tags": c.tags,
            "description": c.description,
            "resource": c.resource,
        }
        for c in concepts
    ]

    edges = []
    for c in concepts:
        for target in c.links:
            if target == c.slug:
                continue
            if target not in by_slug:
                # links into raw/ (immutable source captures) are a
                # different layer, not modeled as graph nodes — expected,
                # not worth a warning. Anything else is an actually broken
                # [[wiki-link]].
                if "raw/" not in target:
                    print(f"[grafokb] link roto, omitido: {c.slug} -> {target}", file=sys.stderr)
                continue
            edges.append({"from": c.slug, "to": target})

    return nodes, edges


HTML_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>tdew — grafo de la wiki de investigación</title>
<script src="https://cdn.jsdelivr.net/npm/vis-network@9/standalone/umd/vis-network.min.js"></script>
<style>
  :root { color-scheme: light dark; }
  html, body { margin: 0; height: 100%; font-family: system-ui, sans-serif; background: #0f1115; color: #e6e6e6; }
  #layout { display: flex; height: 100%; }
  #sidebar { width: 300px; flex: none; padding: 16px; box-sizing: border-box; overflow-y: auto; background: #161922; border-right: 1px solid #2a2e3a; }
  #graph { flex: 1; }
  h1 { font-size: 15px; margin: 0 0 4px; }
  h2 { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #9aa5b1; margin: 20px 0 8px; }
  .sub { font-size: 12px; color: #9aa5b1; margin-bottom: 16px; }
  .view-btn { display: block; width: 100%; text-align: left; padding: 8px 10px; margin-bottom: 6px; border: 1px solid #2a2e3a; border-radius: 6px; background: #1d2130; color: #e6e6e6; cursor: pointer; font-size: 13px; }
  .view-btn.active { border-color: #4f8dfd; background: #23283a; }
  #tagList { display: flex; flex-wrap: wrap; gap: 6px; }
  .tag-chip { font-size: 11px; padding: 3px 8px; border-radius: 999px; border: 1px solid #2a2e3a; cursor: pointer; background: #1d2130; }
  .tag-chip.active { background: #4f8dfd; border-color: #4f8dfd; color: #fff; }
  select { width: 100%; padding: 6px; background: #1d2130; color: #e6e6e6; border: 1px solid #2a2e3a; border-radius: 6px; }
  #legend div { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 4px; }
  .swatch { width: 10px; height: 10px; border-radius: 50%; flex: none; }
  #detail { font-size: 12px; line-height: 1.5; white-space: pre-wrap; }
  #detail a { color: #4f8dfd; }
</style>
</head>
<body>
<div id="layout">
  <div id="sidebar">
    <h1>Wiki de investigación — grafo</h1>
    <div class="sub">__NODE_COUNT__ conceptos, __EDGE_COUNT__ enlaces</div>

    <h2>Vista</h2>
    <button class="view-btn active" data-view="type">Colorear por tipo</button>
    <button class="view-btn" data-view="status">Colorear por estado</button>
    <button class="view-btn" data-view="tags">Filtrar por tags</button>
    <button class="view-btn" data-view="source">Enfocar una fuente</button>

    <div id="tagPanel" style="display:none">
      <h2>Tags (clic para activar/desactivar, ninguno = todos)</h2>
      <div id="tagList"></div>
    </div>

    <div id="sourcePanel" style="display:none">
      <h2>Fuente</h2>
      <select id="sourceSelect"><option value="">— ninguna —</option></select>
    </div>

    <h2 id="legendTitle">Tipo</h2>
    <div id="legend"></div>

    <h2>Detalle</h2>
    <div id="detail">Clic en un nodo para ver su ficha.</div>
  </div>
  <div id="graph"></div>
</div>

<script>
const NODES = __NODES_JSON__;
const EDGES = __EDGES_JSON__;
const TYPE_COLORS = __TYPE_COLORS_JSON__;
const STATUS_COLORS = __STATUS_COLORS_JSON__;

const nodesById = Object.fromEntries(NODES.map(n => [n.id, n]));
const adjacency = {};
for (const n of NODES) adjacency[n.id] = new Set();
for (const e of EDGES) { adjacency[e.from].add(e.to); adjacency[e.to].add(e.from); }

function reachableFrom(startId) {
  const seen = new Set([startId]);
  const queue = [startId];
  while (queue.length) {
    const cur = queue.pop();
    for (const nxt of adjacency[cur] || []) {
      if (!seen.has(nxt)) { seen.add(nxt); queue.push(nxt); }
    }
  }
  return seen;
}

const nodesDataSet = new vis.DataSet(NODES.map(n => ({
  id: n.id,
  label: n.label,
  title: n.description || n.label,
  color: TYPE_COLORS[n.type] || TYPE_COLORS.Unknown,
  font: { color: "#e6e6e6" },
})));
const edgesDataSet = new vis.DataSet(EDGES.map((e, i) => ({ id: i, from: e.from, to: e.to, arrows: "to", color: { color: "#3a4050", opacity: 0.8 } })));

const network = new vis.Network(
  document.getElementById("graph"),
  { nodes: nodesDataSet, edges: edgesDataSet },
  {
    nodes: { shape: "dot", size: 14, borderWidth: 1 },
    edges: { width: 1, smooth: { type: "dynamic" } },
    physics: { solver: "forceAtlas2Based", forceAtlas2Based: { gravitationalConstant: -60, springLength: 120 }, stabilization: { iterations: 200 } },
    interaction: { hover: true, tooltipDelay: 150 },
  }
);

const legend = document.getElementById("legend");
const legendTitle = document.getElementById("legendTitle");

function renderLegend(colorMap, titleText) {
  legendTitle.textContent = titleText;
  legend.innerHTML = "";
  for (const [key, color] of Object.entries(colorMap)) {
    const row = document.createElement("div");
    row.innerHTML = `<span class="swatch" style="background:${color}"></span>${key}`;
    legend.appendChild(row);
  }
}

function colorByType() {
  nodesDataSet.update(NODES.map(n => ({ id: n.id, color: TYPE_COLORS[n.type] || TYPE_COLORS.Unknown, opacity: 1 })));
  renderLegend(TYPE_COLORS, "Tipo");
}

function colorByStatus() {
  nodesDataSet.update(NODES.map(n => ({ id: n.id, color: STATUS_COLORS[n.status] || "#666666", opacity: 1 })));
  renderLegend(STATUS_COLORS, "Estado");
}

let activeTags = new Set();
function applyTagFilter() {
  colorByType();
  if (activeTags.size === 0) return;
  nodesDataSet.update(NODES.map(n => ({
    id: n.id,
    opacity: n.tags.some(t => activeTags.has(t)) ? 1 : 0.12,
  })));
}

function applySourceFocus(sourceId) {
  colorByType();
  if (!sourceId) return;
  const reachable = reachableFrom(sourceId);
  nodesDataSet.update(NODES.map(n => ({ id: n.id, opacity: reachable.has(n.id) ? 1 : 0.12 })));
}

const allTags = [...new Set(NODES.flatMap(n => n.tags))].sort();
const tagList = document.getElementById("tagList");
for (const tag of allTags) {
  const chip = document.createElement("span");
  chip.className = "tag-chip";
  chip.textContent = tag;
  chip.onclick = () => {
    chip.classList.toggle("active");
    if (activeTags.has(tag)) activeTags.delete(tag); else activeTags.add(tag);
    applyTagFilter();
  };
  tagList.appendChild(chip);
}

const sourceSelect = document.getElementById("sourceSelect");
for (const n of NODES.filter(n => n.type === "Source").sort((a, b) => a.label.localeCompare(b.label))) {
  const opt = document.createElement("option");
  opt.value = n.id;
  opt.textContent = n.label;
  sourceSelect.appendChild(opt);
}
sourceSelect.onchange = () => applySourceFocus(sourceSelect.value);

const panels = { tags: document.getElementById("tagPanel"), source: document.getElementById("sourcePanel") };
document.querySelectorAll(".view-btn").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".view-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    Object.values(panels).forEach(p => p.style.display = "none");
    const view = btn.dataset.view;
    if (view === "type") colorByType();
    else if (view === "status") colorByStatus();
    else if (view === "tags") { panels.tags.style.display = "block"; applyTagFilter(); }
    else if (view === "source") { panels.source.style.display = "block"; applySourceFocus(sourceSelect.value); }
  };
});

const detail = document.getElementById("detail");
network.on("click", (params) => {
  if (!params.nodes.length) return;
  const n = nodesById[params.nodes[0]];
  const link = n.resource ? `<a href="${n.resource}" target="_blank" rel="noopener">fuente ↗</a>` : "";
  detail.innerHTML = `<b>${n.label}</b>\\n${n.type} · ${n.status}\\ntags: ${n.tags.join(", ") || "—"}\\n\\n${n.description}\\n\\n${link}`;
});

colorByType();
</script>
</body>
</html>
"""


def render_html(nodes: list[dict], edges: list[dict]) -> str:
    html = HTML_TEMPLATE
    html = html.replace("__NODE_COUNT__", str(len(nodes)))
    html = html.replace("__EDGE_COUNT__", str(len(edges)))
    html = html.replace("__NODES_JSON__", json.dumps(nodes, ensure_ascii=False))
    html = html.replace("__EDGES_JSON__", json.dumps(edges, ensure_ascii=False))
    html = html.replace("__TYPE_COLORS_JSON__", json.dumps(TYPE_COLORS, ensure_ascii=False))
    html = html.replace("__STATUS_COLORS_JSON__", json.dumps(STATUS_COLORS, ensure_ascii=False))
    return html


def build(knowledge_dir: Path = DEFAULT_KNOWLEDGE_DIR, out_path: Path = DEFAULT_OUT) -> Path:
    concepts = load_concepts(knowledge_dir)
    nodes, edges = build_graph_data(concepts)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(nodes, edges), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-dir", type=Path, default=DEFAULT_KNOWLEDGE_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    out_path = build(args.knowledge_dir, args.out)
    print(f"[grafokb] escrito: {out_path}")


if __name__ == "__main__":
    main()
