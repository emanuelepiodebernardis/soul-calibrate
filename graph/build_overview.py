"""Static overview of the knowledge graph: one circle per area (community), sized by its concepts, linked by
how many connections run between two areas. For the README; the full map is map.html.

    python graph/build_overview.py graph/graph.json graph/overview.png
"""

from __future__ import annotations

import json
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

# areas grouped into a few themes, so the picture reads at a glance
THEMES = {
    "Problem and evidence": "why", "Clinical practice": "why", "Vibration products and rhythms": "why",
    "When the bracelet pulses: evidence": "why", "Architecture and regulation": "why", "Session anchor and voice quality": "why",
    "Active questions and decision rule": "loop", "Enrollment, risks and eight states": "loop", "Enrollment details": "loop",
    "Recurring situations and question budget": "loop", "What precise means, consent and archetype path": "loop",
    "Pulse tuned to the person": "loop", "Voice and body: body triggers, voice decides": "loop",
    "Incongruence and masking": "loop", "Fusion of sources": "loop", "README: the loop, real voice and the voice question": "loop",
    "Personal head and situation memory": "loop", "Cold start and measurement reactivity": "loop",
    "Evaluation: SOUL-Bench": "eval", "Authorship, inspiration and prior work": "eval",
    "Simulation scripts and question budget results": "code", "First simulation code": "code",
    "Engine I/O and synthetic checks": "code", "Engine fusion model": "code", "Engine personal baseline": "code",
    "Engine concept-to-code map": "code", "Engine overview, SOUL-Bench and pattern graph": "code", "Archetype prototype": "code",
    "Engine input and package": "code", "Haptic tuning check": "code", "Engine commands and tests": "code",
}
COLORS = {"why": "#2f7d8c", "loop": "#c4622d", "eval": "#6b5ca5", "code": "#8a8478"}
NAMES = {"why": "Evidence and context", "loop": "The loop: decide, ask, learn, pulse", "eval": "Evaluation and authorship",
         "code": "Code"}


def main(src: str, out: str) -> None:
    g = json.load(open(src, encoding="utf-8"))
    com = {n["id"]: n.get("community_name") or str(n.get("community")) for n in g["nodes"]}
    size = Counter(com.values())
    keep = {c for c, k in size.items() if k >= 3}
    w: Counter = Counter()
    for e in g.get("links", g.get("edges", [])):
        a, b = com.get(e["source"]), com.get(e["target"])
        if a in keep and b in keep and a != b:
            w[tuple(sorted((a, b)))] += 1
    G = nx.Graph()
    for c in keep:
        G.add_node(c, size=size[c])
    for (a, b), k in w.items():
        G.add_edge(a, b, weight=k)
    # columns from evidence to code, so the picture reads left to right: where an idea comes from, where it is built
    order = ["why", "loop", "eval", "code"]
    cols = {t: sorted([c for c in G.nodes if THEMES.get(c, "eval") == t], key=lambda c: -size[c]) for t in order}
    pos = {}
    for _ in range(4):                                   # barycentre ordering to reduce crossings
        for i, t in enumerate(order):
            for j, c in enumerate(cols[t]):
                pos[c] = (i * 1.0, -j / max(len(cols[t]) - 1, 1))
        for t in order:
            def bary(c):
                nb = [(pos[n][1], G[c][n]["weight"]) for n in G.neighbors(c) if THEMES.get(n, "eval") != t]
                return sum(y * k for y, k in nb) / sum(k for _, k in nb) if nb else pos[c][1]
            cols[t] = sorted(cols[t], key=bary, reverse=True)
    for i, t in enumerate(order):
        n = len(cols[t])
        for j, c in enumerate(cols[t]):
            pos[c] = (i * 1.0, 0.5 - j / max(n - 1, 1) if n > 1 else 0.0)
    fig, ax = plt.subplots(figsize=(17, 11))
    top = sorted(w.values(), reverse=True)
    cut = top[min(len(top) - 1, 55)] if top else 0
    for (a, b), k in w.items():
        if k >= cut:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            xs = [x1 + (x2 - x1) * u for u in (0, 0.5, 1)]
            bend = 0.08 if x1 == x2 else 0.0
            ys = [y1, (y1 + y2) / 2, y2]
            xs[1] += bend
            ax.plot(xs, ys, color="#b9b2a5", linewidth=0.4 + 0.1 * k, alpha=0.5, zorder=1)
    for c in G.nodes:
        t = THEMES.get(c, "eval")
        ax.scatter(*pos[c], s=28 * size[c], color=COLORS[t], alpha=0.9, edgecolor="white", linewidth=1.5, zorder=2)
        ax.text(pos[c][0] + 0.035, pos[c][1], f"{c} ({size[c]})", ha="left", va="center", fontsize=10,
                color="#2b2925", zorder=3, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
    for i, t in enumerate(order):
        ax.text(i * 1.0, 0.62, NAMES[t], ha="left", fontsize=13, color=COLORS[t], weight="bold")
    n_nodes, n_links = len(g["nodes"]), len(g.get("links", g.get("edges", [])))
    ax.set_title(f"How the project's ideas connect: {len(keep)} areas, {n_nodes} concepts, {n_links} links "
                 "(circle = area, number = concepts in it, line = links between areas; the strongest links shown)", loc="left",
                 fontsize=13, color="#2b2925", pad=12)
    ax.set_xlim(-0.1, 3.75)
    ax.set_ylim(-0.56, 0.68)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("graph/graph.json", "graph/overview.png")))
