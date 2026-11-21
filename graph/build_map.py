"""Build a self-contained interactive map of the project's knowledge graph.

    python graph/build_map.py graph/graph.json graph/map.html

The layout is computed here, once, so the page needs no physics engine and no
external library: it opens offline in any browser and always shows the whole graph.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

PALETTE = ["#c4622d", "#2f7d8c", "#7a5ea8", "#3f8f4f", "#b0476b", "#b8922a", "#4a6fb5", "#8a8478", "#6b8e23", "#a0522d", "#5f7f99", "#9a6b3f"]


def layout(G: nx.Graph, communities: dict[str, int]) -> dict[str, tuple[float, float]]:
    """Communities placed on a circle, each laid out internally, then refined globally."""
    groups: dict[int, list[str]] = {}
    for n in G.nodes:
        groups.setdefault(communities.get(n, -1), []).append(n)
    order = sorted(groups, key=lambda c: -len(groups[c]))
    init = {}
    R = 260.0 + 70.0 * len(order)
    for i, c in enumerate(order):
        ang = 2 * math.pi * i / max(1, len(order))
        cx, cy = R * math.cos(ang), R * math.sin(ang)
        sub = G.subgraph(groups[c])
        pos = nx.spring_layout(sub, seed=7, k=1.2 / math.sqrt(max(1, len(sub))), iterations=200)
        scale = 120 + 30 * math.sqrt(len(sub))
        for n, (x, y) in pos.items():
            init[n] = (cx + scale * x, cy + scale * y)
    return {n: (float(x), float(y)) for n, (x, y) in init.items()}


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    title = sys.argv[3] if len(sys.argv) > 3 else "SOUL-Calibrate — project map"
    g = json.loads(src.read_text(encoding="utf-8"))
    # External libraries (numpy, json, ...) have no source file in the project: leave them out of the map.
    g["nodes"] = [n for n in g["nodes"] if n.get("source_file")]
    G = nx.Graph()
    for n in g["nodes"]:
        G.add_node(n["id"])
    links = g.get("links") or g.get("edges") or []
    for e in links:
        if e["source"] in G and e["target"] in G and e["source"] != e["target"]:
            G.add_edge(e["source"], e["target"])
    comm = {n["id"]: n.get("community", -1) for n in g["nodes"]}
    pos = layout(G, comm)
    deg = Counter(dict(G.degree()))

    nodes = []
    for n in g["nodes"]:
        x, y = pos[n["id"]]
        nodes.append({
            "id": n["id"], "l": n.get("label") or n["id"], "c": n.get("community", -1),
            "cn": n.get("community_name") or "", "t": n.get("file_type") or "",
            "f": n.get("source_file") or "", "r": n.get("rationale") or "",
            "d": deg[n["id"]], "x": round(x, 1), "y": round(y, 1),
        })
    edges = [{"s": e["source"], "t": e["target"], "r": e.get("relation", ""), "k": e.get("confidence", "")}
             for e in links if e["source"] in pos and e["target"] in pos and e["source"] != e["target"]]
    hyper = [{"l": h.get("label", ""), "n": h.get("nodes", [])} for h in g.get("hyperedges", [])]
    comms = {}
    for n in nodes:
        comms.setdefault(n["c"], n["cn"] or f"Area {n['c']}")
    data = {"nodes": nodes, "edges": edges, "hyper": hyper, "comms": comms, "palette": PALETTE}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__TITLE__", title).replace("__DATA__", payload)
    dst.write_text(html, encoding="utf-8")
    print(f"written {dst} ({len(nodes)} nodes, {len(edges)} edges)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { --bg:#fbfaf8; --panel:#ffffff; --ink:#1f1e1c; --quiet:#6b6862; --line:#e4e1db; --edge:#cfcac1; --accent:#c4622d; }
  @media (prefers-color-scheme: dark) { :root { --bg:#1b1a18; --panel:#242320; --ink:#eceae6; --quiet:#a19d95; --line:#3a3833; --edge:#4a4741; --accent:#e08a5a; } }
  * { box-sizing:border-box; }
  html, body { height:100%; margin:0; }
  body { font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, sans-serif; background:var(--bg); color:var(--ink); display:flex; flex-direction:column; }
  header { padding:14px 20px 10px; border-bottom:1px solid var(--line); }
  h1 { font-size:18px; margin:0 0 4px; }
  .lead { color:var(--quiet); font-size:13px; margin:0; }
  main { flex:1; display:flex; min-height:0; }
  #stage { flex:1; position:relative; min-width:0; }
  svg { width:100%; height:100%; display:block; cursor:grab; touch-action:none; }
  svg.dragging { cursor:grabbing; }
  .edge { stroke:var(--edge); stroke-width:1; vector-effect:non-scaling-stroke; }
  .edge.inf { stroke-dasharray:4 3; }
  .edge.hl { stroke:var(--accent); stroke-width:2; vector-effect:non-scaling-stroke; }
  .node circle { stroke-width:1.5; vector-effect:non-scaling-stroke; cursor:pointer; }
  .node text { font-size:var(--fs, 11px); fill:var(--ink); pointer-events:none; paint-order:stroke; stroke:var(--bg); stroke-width:3px; }
  .node.minor text { display:none; }
  svg.zoomed .node.minor text { display:inline; }
  .node.sel circle { stroke:var(--ink); stroke-width:3; }
  .dim { opacity:.12; }
  .hidden { display:none; }
  .controls { position:absolute; left:12px; top:12px; display:flex; gap:6px; }
  .controls button { background:var(--panel); color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:5px 10px; font-size:13px; cursor:pointer; }
  aside { width:330px; flex:none; border-left:1px solid var(--line); background:var(--panel); padding:12px 14px; overflow:auto; font-size:13px; }
  input[type=search] { width:100%; padding:7px 9px; border:1px solid var(--line); border-radius:6px; background:var(--bg); color:var(--ink); font-size:13px; }
  .lg { display:flex; align-items:center; gap:8px; margin:4px 0; cursor:pointer; user-select:none; }
  .lg.off { opacity:.35; }
  .dot { width:11px; height:11px; border-radius:50%; flex:none; }
  h2 { font-size:15px; margin:14px 0 4px; }
  .meta, .hint { color:var(--quiet); font-size:12px; }
  ul { padding-left:16px; margin:6px 0; }
  li { margin:3px 0; cursor:pointer; }
  li:hover { color:var(--accent); }
  @media (max-width:800px) { main { flex-direction:column; } aside { width:auto; height:45vh; border-left:none; border-top:1px solid var(--line); } }
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <p class="lead">Drag to move, scroll or use the buttons to zoom, click a node to see its sources and links. Dashed lines are inferred links. Names of small nodes appear when you zoom in.</p>
</header>
<main>
  <div id="stage">
    <svg id="svg" xmlns="http://www.w3.org/2000/svg"><g id="edges"></g><g id="nodes"></g></svg>
    <div class="controls"><button id="zin" aria-label="Zoom in">+</button><button id="zout" aria-label="Zoom out">−</button><button id="fit">Fit</button><button id="clear">Clear</button></div>
  </div>
  <aside>
    <input type="search" id="q" placeholder="Search a concept">
    <div id="legend" style="margin:12px 0"></div>
    <div id="info"><p class="hint">Click a node.</p></div>
  </aside>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('svg'), gE = document.getElementById('edges'), gN = document.getElementById('nodes');
  var byId = {}, adj = {};
  D.nodes.forEach(function (n) { byId[n.id] = n; adj[n.id] = []; });
  D.edges.forEach(function (e) { adj[e.s].push(e.t); adj[e.t].push(e.s); });
  function color(c) { var p = D.palette; return p[((c % p.length) + p.length) % p.length]; }
  var maxD = Math.max.apply(null, D.nodes.map(function (n) { return n.d; }).concat([1]));
  var sorted = D.nodes.slice().sort(function (a, b) { return b.d - a.d; });
  var major = {}; sorted.filter(function (n) { return n.t !== 'document' && n.t !== 'code'; }).slice(0, Math.max(12, Math.round(D.nodes.length * 0.12))).forEach(function (n) { major[n.id] = true; });

  var edgeEls = D.edges.map(function (e) {
    var a = byId[e.s], b = byId[e.t], l = document.createElementNS(NS, 'line');
    l.setAttribute('x1', a.x); l.setAttribute('y1', a.y); l.setAttribute('x2', b.x); l.setAttribute('y2', b.y);
    l.setAttribute('class', 'edge' + (e.k === 'EXTRACTED' ? '' : ' inf'));
    gE.appendChild(l); return l;
  });
  var nodeEls = {};
  D.nodes.forEach(function (n) {
    var g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'node' + (major[n.id] ? '' : ' minor'));
    var r = 4 + 12 * Math.sqrt(n.d / maxD);
    var c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', n.x); c.setAttribute('cy', n.y); c.setAttribute('r', r);
    c.setAttribute('fill', n.t === 'document' ? 'var(--bg)' : color(n.c)); c.setAttribute('stroke', color(n.c));
    if (n.t === 'document') c.setAttribute('stroke-width', '2.5');
    var t = document.createElementNS(NS, 'text'); t.setAttribute('x', n.x + r + 3); t.setAttribute('y', n.y + 4);
    t.textContent = n.l.length > 48 ? n.l.slice(0, 46) + '…' : n.l;
    var tip = document.createElementNS(NS, 'title'); tip.textContent = n.l;
    g.appendChild(tip); g.appendChild(c); g.appendChild(t);
    g.addEventListener('click', function (ev) { ev.stopPropagation(); select(n.id); });
    gN.appendChild(g); nodeEls[n.id] = g;
  });

  // View box handling
  var xs = D.nodes.map(function (n) { return n.x; }), ys = D.nodes.map(function (n) { return n.y; });
  var full = { x: Math.min.apply(null, xs) - 80, y: Math.min.apply(null, ys) - 60 };
  full.w = Math.max.apply(null, xs) - full.x + 260; full.h = Math.max.apply(null, ys) - full.y + 60;
  var vb = { x: full.x, y: full.y, w: full.w, h: full.h };
  function apply() {
    svg.setAttribute('viewBox', vb.x + ' ' + vb.y + ' ' + vb.w + ' ' + vb.h);
    var r = svg.getBoundingClientRect(), s = Math.max(vb.w / Math.max(1, r.width), vb.h / Math.max(1, r.height));
    svg.style.setProperty('--fs', (12 * s).toFixed(2) + 'px');
    svg.classList.toggle('zoomed', vb.w < full.w * 0.45);
  }
  function zoom(f, cx, cy) {
    if (cx === undefined) { cx = vb.x + vb.w / 2; cy = vb.y + vb.h / 2; }
    vb.x = cx - (cx - vb.x) * f; vb.y = cy - (cy - vb.y) * f; vb.w *= f; vb.h *= f; apply();
  }
  function fit() { vb = { x: full.x, y: full.y, w: full.w, h: full.h }; apply(); }
  function toSvg(px, py) {
    var r = svg.getBoundingClientRect(), s = Math.max(vb.w / r.width, vb.h / r.height);
    var ox = (r.width * s - vb.w) / 2, oy = (r.height * s - vb.h) / 2;
    return { x: vb.x - ox + (px - r.left) * s, y: vb.y - oy + (py - r.top) * s, s: s };
  }
  svg.addEventListener('wheel', function (ev) { ev.preventDefault(); var p = toSvg(ev.clientX, ev.clientY); zoom(ev.deltaY > 0 ? 1.15 : 1 / 1.15, p.x, p.y); }, { passive: false });
  var drag = null;
  svg.addEventListener('pointerdown', function (ev) { drag = { x: ev.clientX, y: ev.clientY, vx: vb.x, vy: vb.y, s: toSvg(ev.clientX, ev.clientY).s, moved: false }; svg.classList.add('dragging'); });
  window.addEventListener('pointermove', function (ev) { if (!drag) return; var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true; vb.x = drag.vx - dx * drag.s; vb.y = drag.vy - dy * drag.s; apply(); });
  window.addEventListener('pointerup', function () { drag = null; svg.classList.remove('dragging'); });
  document.getElementById('zin').onclick = function () { zoom(1 / 1.4); };
  document.getElementById('zout').onclick = function () { zoom(1.4); };
  document.getElementById('fit').onclick = fit;
  document.getElementById('clear').onclick = function () { clearSel(); };
  svg.addEventListener('click', function () { if (drag === null) {} });

  // Legend
  var hidden = {};
  var legend = document.getElementById('legend');
  Object.keys(D.comms).sort(function (a, b) { return a - b; }).forEach(function (c) {
    var count = D.nodes.filter(function (n) { return String(n.c) === c; }).length;
    var row = document.createElement('div'); row.className = 'lg';
    var dot = document.createElement('span'); dot.className = 'dot'; dot.style.background = color(+c);
    var label = document.createElement('span'); label.textContent = D.comms[c] + ' (' + count + ')';
    row.appendChild(dot); row.appendChild(label);
    row.onclick = function () { hidden[c] = !hidden[c]; row.classList.toggle('off', hidden[c]); refreshHidden(); };
    legend.appendChild(row);
  });
  function refreshHidden() {
    D.nodes.forEach(function (n) { nodeEls[n.id].classList.toggle('hidden', !!hidden[String(n.c)]); });
    D.edges.forEach(function (e, i) { edgeEls[i].classList.toggle('hidden', !!hidden[String(byId[e.s].c)] || !!hidden[String(byId[e.t].c)]); });
  }

  // Selection
  var info = document.getElementById('info');
  function clearSel() {
    Object.keys(nodeEls).forEach(function (id) { nodeEls[id].classList.remove('dim', 'sel'); });
    edgeEls.forEach(function (l) { l.classList.remove('dim', 'hl'); });
    intro();
  }
  function select(id) {
    var n = byId[id], near = {}; near[id] = true; adj[id].forEach(function (x) { near[x] = true; });
    Object.keys(nodeEls).forEach(function (k) { nodeEls[k].classList.toggle('dim', !near[k]); nodeEls[k].classList.toggle('sel', k === id); });
    D.edges.forEach(function (e, i) { var on = e.s === id || e.t === id; edgeEls[i].classList.toggle('dim', !on); edgeEls[i].classList.toggle('hl', on); });
    info.innerHTML = '';
    var h = document.createElement('h2'); h.textContent = n.l; info.appendChild(h);
    var m = document.createElement('div'); m.className = 'meta'; m.textContent = (D.comms[n.c] || '') + ' · ' + n.f + ' · ' + n.d + ' links'; info.appendChild(m);
    if (n.r) { var p = document.createElement('p'); p.textContent = n.r; info.appendChild(p); }
    var hy = D.hyper.filter(function (x) { return x.n.indexOf(id) >= 0; });
    if (hy.length) { var q = document.createElement('p'); q.className = 'hint'; q.textContent = 'Part of: ' + hy.map(function (x) { return x.l; }).join('; '); info.appendChild(q); }
    if (n.d <= 1 && n.t !== 'document') { var w = document.createElement('p'); w.style.color = 'var(--accent)'; w.textContent = 'Weakly connected: a possible gap in the project.'; info.appendChild(w); }
    var t = document.createElement('div'); t.className = 'hint'; t.textContent = 'Linked to:'; info.appendChild(t);
    var ul = document.createElement('ul');
    adj[id].map(function (x) { return byId[x]; }).sort(function (a, b) { return b.d - a.d; }).forEach(function (x) {
      var li = document.createElement('li'); li.textContent = x.l; li.onclick = function () { select(x.id); center(x.id); }; ul.appendChild(li);
    });
    info.appendChild(ul);
  }
  function center(id) { var n = byId[id]; vb.x = n.x - vb.w / 2; vb.y = n.y - vb.h / 2; apply(); }
  document.getElementById('q').addEventListener('input', function (ev) {
    var s = ev.target.value.trim().toLowerCase(); if (s.length < 2) return;
    var hit = sorted.filter(function (n) { return n.l.toLowerCase().indexOf(s) >= 0; })[0];
    if (hit) { if (vb.w > full.w * 0.5) zoom(0.45); select(hit.id); center(hit.id); }
  });
  function intro() {
    info.innerHTML = '';
    var p = document.createElement('p'); p.className = 'hint'; p.textContent = 'Most connected concepts (click to explore):'; info.appendChild(p);
    var ul = document.createElement('ul');
    sorted.filter(function (n) { return n.t !== 'document' && n.t !== 'code'; }).slice(0, 12).forEach(function (x) {
      var li = document.createElement('li'); li.textContent = x.l + ' (' + x.d + ')'; li.onclick = function () { select(x.id); }; ul.appendChild(li);
    });
    info.appendChild(ul);
  }
  apply(); intro();
  window.addEventListener('resize', apply);
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
