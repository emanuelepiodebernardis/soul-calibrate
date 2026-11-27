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
from matplotlib.patches import PathPatch  # noqa: E402
from matplotlib.path import Path  # noqa: E402

# areas grouped into a few themes, so the picture reads at a glance
THEMES = {
    "Problem and evidence": "why", "Clinical practice": "why", "Vibration products and rhythms": "why",
    "When the bracelet pulses: evidence": "why", "Privacy and regulation": "why", "Analogous systems": "why",
    "Cohort, archetype path and analogies": "why", "Biofeedback and vibration evidence": "why",
    "Active questions and decision rule": "loop", "Enrollment details": "loop", "Recurring situations and question budget": "loop",
    "Risks, traps and cold start": "loop", "Question budget experiments": "loop", "What precise means, eight states": "loop",
    "Voice check-ins: body triggers, voice decides": "loop", "Speech front end and real-voice check": "loop",
    "Voice-and-body signatures": "loop", "Architecture": "loop",
    "Fusion of sources": "loop", "Incongruence and masking": "loop", "README: voice, vibration and the loop": "loop",
    "Evaluation: SOUL-Bench": "eval", "Claims ledger and inspiration": "eval", "Ideas from prior work": "eval",
    "Authorship": "eval", "Reading audit": "eval", "Model-agnostic input": "eval",
    "Simulation scripts and question budget results": "code", "First simulation code": "code", "Engine overview": "code",
    "Engine concept-to-code map": "code", "Archetype and channel checks (code)": "code", "Engine core code": "code",
    "SOUL-Bench code": "code", "Engine personal baseline": "code", "Personal pattern graph": "code",
    "Archetype prototype": "code", "Haptic tuning check": "code", "Astrology utilities": "code", "Engine commands": "code",
    "Pulse tuning code": "code", "Engine fusion code": "code",
    "Voice, vibration and the pulse": "loop", "Architecture and the closed loop": "loop", "README: voice and body": "loop",
    "README: the project at a glance": "loop", "Cohort pilot and archetype path": "why",
    "Understanding layer concept": "why", "Emotional granularity evidence": "why", "Public approach comparison": "why",
    "People who don't know what they feel": "loop", "Understanding results": "eval", "User control and situations": "code",
    "Understanding layer code": "code", "Answer reliability": "code", "Personal head and baseline": "code",
    "Engine input and run": "code", "Astrology reflection code": "code", "Conformal speak, ask, quiet": "code",
    "Coarse-to-fine simulation": "code", "Engine entry and commands": "code",
    "Engine overview and commands": "code", "Signature checks (code)": "code", "Engine baseline and conformal code": "code",
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
    # which links to draw: every area's two strongest links, so none is left without a line, plus the strongest overall
    shown = set(sorted(w, key=lambda p: -w[p])[:40])
    for c in G.nodes:
        mine = sorted((p for p in w if c in p), key=lambda p: -w[p])
        shown.update(mine[:2])
    kmax = max(w.values()) if w else 1
    for (a, b) in sorted(shown, key=lambda p: w[p]):      # strongest drawn last, on top
        k = w[(a, b)]
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if x1 == x2:                                       # same column: an arc to the left of the circles
            bulge = 0.06 + 0.22 * abs(y1 - y2)
            verts = [(x1, y1), (x1 - bulge, y1), (x1 - bulge, y2), (x2, y2)]
        else:                                              # across columns: a smooth S curve
            if x1 > x2:
                (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
            dx = (x2 - x1) * 0.45
            verts = [(x1, y1), (x1 + dx, y1), (x2 - dx, y2), (x2, y2)]
        path = Path(verts, [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
        lw = 0.6 + 3.2 * (k / kmax) ** 0.7
        ax.add_patch(PathPatch(path, fc="none", ec="#8f8879", lw=lw, alpha=0.28 + 0.4 * (k / kmax) ** 0.5, zorder=1,
                               capstyle="round"))
    for c in G.nodes:
        t = THEMES.get(c, "eval")
        ax.scatter(*pos[c], s=28 * size[c], color=COLORS[t], alpha=0.9, edgecolor="white", linewidth=1.5, zorder=2)
        ax.text(pos[c][0] + 0.035, pos[c][1], f"{c} ({size[c]})", ha="left", va="center", fontsize=10,
                color="#2b2925", zorder=3, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    for i, t in enumerate(order):
        ax.text(i * 1.0, 0.62, NAMES[t], ha="left", fontsize=13, color=COLORS[t], weight="bold")
    n_nodes, n_links = len(g["nodes"]), len(g.get("links", g.get("edges", [])))
    ax.set_title(f"How the project's ideas connect: {len(keep)} areas, {n_nodes} concepts, {n_links} links "
                 "\n(circle = area, number = concepts in it; line = links between two areas, thicker = more links; "
                 f"each area's two strongest links shown, {len(shown)} of {len(w)})", loc="left",
                 fontsize=13, color="#2b2925", pad=12)
    ax.set_xlim(-0.32, 3.75)
    ax.set_ylim(-0.56, 0.68)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=130)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("graph/graph.json", "graph/overview.png")))
