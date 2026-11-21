# Knowledge graph of the project

Built with [Graphify](https://pypi.org/project/graphifyy/) from `docs/`, `README.md`, `AUTHORS.md`, the
simulation code and results in `sim/`, and the engine in `engine/soulcal/` with its demo reports.

| File | What it is |
| --- | --- |
| `map.html` | interactive map: open it in any browser, works offline |
| `GRAPH_REPORT.md` | most connected concepts, surprising links, weakly connected nodes (possible gaps), suggested questions |
| `graph.json` | the graph data (nodes, links, communities) |
| `build_map.py` | rebuilds `map.html` from `graph.json` with a precomputed layout |

At the last build: 680 nodes, 1898 links, 27 communities (21 with three or more nodes), from 30 documents and
19 code files: the docs, the simulation and the `soulcal` engine.

## What the graph found

Built three times while the project grew; each round pointed at the next fix.

| Round | What the graph showed | What was done |
| --- | --- | --- |
| 1 (docs + simulation) | Active questions are the bridge between most areas; 23 isolated nodes (audio quality check, sliders, enrollment studies) | Answer rate became the first metric; E11–E14 added for the weak risks |
| 2 (+ recurring situations, incongruence) | "Situation stability" formed an island; the situation memory and the personal head were two separate clusters; incongruence was linked to the literature but not to fusion | Life-change and coverage experiments (docs/20), the population → head → memory order (docs/06), fusion linked to docs/21; new risks in docs/10 and E22–E23 |
| 3 (+ the engine) | The decision rule (speak / ask / quiet) and the engine are now the backbone, and SOUL-Bench is the bridge between evidence, risks, consent and regulation; 20+ concepts are linked to the code that implements them | SOUL-Bench ladder and quality gate implemented in `engine/soulcal` |

Still only on paper (no code yet): the session anchor and the enrollment flow, the reading audit batteries, the
private cohort pilot, HRV biofeedback and the micro-randomised trials. These are the next things to build or run,
and they need real users or Nightlet's app.

## Rebuild

```bash
pip install graphifyy networkx
graphify install            # registers the /graphify skill for your coding agent
# in the agent, from the repository root:
/graphify . --update
python graph/build_map.py graphify-out/graph.json graph/map.html
```
