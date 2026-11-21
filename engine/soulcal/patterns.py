"""Personal pattern graph: which contexts, body signals, expressions and reflection features go with
which states, for this person.

Every candidate link "factor -> state" is tested with a two-sided Fisher exact test. Because many links
are tested at once, p-values are corrected with Benjamini-Hochberg (false discovery rate). A link is then
re-tested on the later half of the person's history, which the discovery step did not see:

* supported   - significant after correction on the first half AND same direction with p < 0.05 later;
* exploratory - suggestive (uncorrected p < 0.05 on all data) but not supported: shown as an idea to
                reflect on, never as a finding;
* links that are neither are not drawn.

Factors come in layers: context (day, time), body (heart rate, HRV, movement vs the person's norm),
expression (what face, voice and words suggest, and whether they disagree) and reflection (moon phase,
moon sign: see astro.py). Only the measured layers can ever feed the reading; the reflection layer is
for the person's own curiosity and is labelled as such.

The graph is written in the same node-link format as the project map (graph/graph.json), so the
same viewer (graph/build_map.py) draws it.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

from .astro import reflection_factors
from .baseline import PersonalBaseline
from .schema import STATES, Reading

WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
LAYERS = ("context", "body", "expression", "reflection")


def _time_of_day(h: int) -> str:
    return "morning" if 5 <= h < 12 else "afternoon" if h < 18 else "evening" if h < 23 else "night"


def factors_for(readings: list[Reading], birth: date | None = None) -> list[dict[tuple[str, str], bool]]:
    """Binary factors per reading, keyed by (layer, name). Body factors use a personal baseline
    updated in time order, so each reading is judged against the norm known at that moment."""
    base = PersonalBaseline()
    out = []
    for r in readings:
        f: dict[tuple[str, str], bool] = {}
        f[("context", f"day: {WEEKDAYS[r.timestamp.weekday()]}")] = True
        f[("context", f"time: {_time_of_day(r.timestamp.hour)}")] = True
        f[("context", "weekend")] = r.timestamp.weekday() >= 5
        z = base.physio_z(r)
        if "heart_rate" in z:
            f[("body", "heart rate above usual")] = z["heart_rate"] > 1.0
        if "hrv_rmssd" in z:
            f[("body", "HRV below usual")] = z["hrv_rmssd"] < -1.0
        if "motion" in z:
            f[("body", "moving more than usual")] = z["motion"] > 1.0
        logits = base.channel_logits(r)
        for c, v in logits.items():
            f[("expression", f"{c} suggests {STATES[int(np.argmax(v))]}")] = True
        if "text" in logits and ("face" in logits or "voice" in logits):
            expr = np.mean([logits[c] for c in ("face", "voice") if c in logits], axis=0)
            f[("expression", "words and expression disagree")] = int(np.argmax(logits["text"])) != int(np.argmax(expr))
        for k, v in reflection_factors(r.timestamp, birth).items():
            f[("reflection", f"{k}: {v}")] = True
        base.update(r)
        out.append(f)
    return out


def _fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact test on [[a, b], [c, d]]."""
    n1, n2, k, n = a + b, c + d, a + c, a + b + c + d
    def p(x: int) -> float:
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n, k)
    lo, hi = max(0, k - n2), min(k, n1)
    p_obs = p(a)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= p_obs * (1 + 1e-9)))


def _bh(pvals: list[float]) -> list[float]:
    m = len(pvals)
    order = np.argsort(pvals)
    q = np.empty(m)
    prev = 1.0
    for rank, i in reversed(list(enumerate(order, start=1))):
        prev = min(prev, pvals[i] * m / rank)
        q[i] = prev
    return q.tolist()


@dataclass
class Link:
    layer: str
    factor: str
    state: str
    n_factor: int
    rate_with: float
    rate_without: float
    p_all: float
    q_discovery: float
    p_replication: float
    status: str               # "supported" | "exploratory" | "none"

    @property
    def lift(self) -> float:
        return self.rate_with / max(self.rate_without, 1e-9)


def _table(rows, labels, key, state):
    a = sum(1 for f, y in zip(rows, labels) if f.get(key) and y == state)
    b = sum(1 for f, y in zip(rows, labels) if f.get(key) and y != state)
    c = sum(1 for f, y in zip(rows, labels) if not f.get(key) and y == state)
    d = sum(1 for f, y in zip(rows, labels) if not f.get(key) and y != state)
    return a, b, c, d


def find_patterns(readings: list[Reading], labels: list[str | None], birth: date | None = None,
                  q_level: float = 0.10, min_support: int = 6) -> list[Link]:
    """Test every factor -> state link on the labelled readings (labels: self-reports or answers)."""
    rows_all = factors_for(readings, birth)
    pairs = [(f, y) for f, y in zip(rows_all, labels) if y is not None]
    if len(pairs) < 20:
        return []
    rows, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    half = len(rows) // 2
    keys = sorted({k for f in rows for k, v in f.items() if v})
    cand = []
    for key in keys:
        n_f = sum(1 for f in rows if f.get(key))
        if n_f < min_support or n_f > len(rows) - min_support:
            continue
        for s in STATES:
            a, b, c, d = _table(rows, ys, key, s)
            if a + c == 0:
                continue
            p_all = _fisher_two_sided(a, b, c, d)
            da, db, dc, dd = _table(rows[:half], ys[:half], key, s)
            p_disc = _fisher_two_sided(da, db, dc, dd) if (da + db) and (dc + dd) else 1.0
            ra, rb, rc, rd = _table(rows[half:], ys[half:], key, s)
            p_rep = _fisher_two_sided(ra, rb, rc, rd) if (ra + rb) and (rc + rd) else 1.0
            disc_dir = (da / max(da + db, 1)) - (dc / max(dc + dd, 1))
            rep_dir = (ra / max(ra + rb, 1)) - (rc / max(rc + rd, 1))
            cand.append([key, s, n_f, a / (a + b), c / max(c + d, 1), p_all, p_disc, p_rep,
                         disc_dir * rep_dir > 0 and disc_dir > 0])
    if not cand:
        return []
    qs = _bh([c[6] for c in cand])
    links = []
    for c, q in zip(cand, qs):
        key, s, n_f, rw, rwo, p_all, _, p_rep, same_dir_positive = c
        if q <= q_level and p_rep < 0.05 and same_dir_positive:
            status = "supported"
        elif p_all < 0.05 and rw > rwo:
            status = "exploratory"
        else:
            status = "none"
        links.append(Link(key[0], key[1], s, n_f, rw, rwo, p_all, q, p_rep, status))
    return links


def to_graph(links: list[Link], user_id: str) -> dict:
    """Node-link graph in the project-map format: states, factors and the links worth drawing."""
    comm = {layer: i for i, layer in enumerate(("states",) + LAYERS)}
    nodes = [{"id": f"state_{s}", "label": s, "community": comm["states"], "community_name": "States",
              "file_type": "concept", "source_file": f"personal data ({user_id})"} for s in STATES]
    seen, edges = set(), []
    for lk in links:
        if lk.status == "none":
            continue
        fid = "factor_" + "".join(ch if ch.isalnum() else "_" for ch in f"{lk.layer}_{lk.factor}".lower())
        if fid not in seen:
            seen.add(fid)
            nodes.append({"id": fid, "label": lk.factor, "community": comm[lk.layer],
                          "community_name": lk.layer.capitalize() + (" (reflection, not evidence)" if lk.layer == "reflection" else ""),
                          "file_type": "rationale" if lk.layer == "reflection" else "concept",
                          "source_file": f"personal data ({user_id})",
                          "rationale": f"seen in {lk.n_factor} labelled readings"})
        edges.append({"source": fid, "target": f"state_{lk.state}", "relation": "goes_with",
                      "confidence": "EXTRACTED" if lk.status == "supported" else "AMBIGUOUS",
                      "status": lk.status, "lift": round(lk.lift, 2), "p_all": round(lk.p_all, 4),
                      "q_discovery": round(lk.q_discovery, 4), "p_replication": round(lk.p_replication, 4)})
    return {"directed": False, "multigraph": False, "graph": {"user_id": user_id}, "nodes": nodes,
            "links": edges, "hyperedges": []}


def report(links: list[Link], user_id: str) -> str:
    lines = [f"# Personal patterns: {user_id}", "",
             "Supported = significant after false-discovery correction on the first half of the history and "
             "confirmed on the second half. Exploratory = suggestive only: an idea to reflect on, not a finding. "
             "Reflection-layer factors (moon, signs) never feed the reading.", ""]
    for status in ("supported", "exploratory"):
        rows = sorted([lk for lk in links if lk.status == status], key=lambda lk: lk.p_all)
        lines += [f"## {status.capitalize()} ({len(rows)})", ""]
        if not rows:
            lines += ["None.", ""]
            continue
        lines += ["| Layer | When | State | Share with | Share without | p (all) | q (discovery) | p (replication) |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for lk in rows:
            lines.append(f"| {lk.layer} | {lk.factor} | {lk.state} | {lk.rate_with:.2f} | {lk.rate_without:.2f} | "
                         f"{lk.p_all:.4f} | {lk.q_discovery:.3f} | {lk.p_replication:.4f} |")
        lines.append("")
    tested = defaultdict(int)
    for lk in links:
        tested[lk.layer] += 1
    lines.append("Links tested per layer: " + ", ".join(f"{k} {v}" for k, v in sorted(tested.items())) + ".")
    return "\n".join(lines) + "\n"


def write(links: list[Link], user_id: str, out_dir: str | Path) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "patterns.json").write_text(json.dumps(to_graph(links, user_id), indent=1), encoding="utf-8")
    (out / "PATTERNS.md").write_text(report(links, user_id), encoding="utf-8")
