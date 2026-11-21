# Knowledge graph of the project

Built with [Graphify](https://pypi.org/project/graphifyy/) from `docs/`, `README.md`, `AUTHORS.md`, the
simulation code in `sim/soul_calibrate/` and `sim/results/RESULTS.md`.

| File | What it is |
| --- | --- |
| `map.html` | interactive map: open it in any browser, works offline |
| `GRAPH_REPORT.md` | most connected concepts, surprising links, weakly connected nodes (possible gaps), suggested questions |
| `graph.json` | the graph data (nodes, links, communities) |
| `build_map.py` | rebuilds `map.html` from `graph.json` with a precomputed layout |

At the last build: 326 nodes, 830 links, 8 communities (problem and evidence; simulation code; authorship,
prior work and governance; risks; labels, question budget and consent; decision and active questions;
clinical practices; analogous systems).

## What the graph found

- The active-question module is the bridge between most areas: if users stop answering, the loop stops.
- Each simulation function is linked to the result it produces in `docs/18-simulation.md`.
- Weakly connected nodes point to design items not yet in the code (for example the audio quality check) and
  to risks that need their own experiment (added as E11–E14 in `docs/16-experiments.md`).

## Rebuild

```bash
pip install graphifyy networkx
graphify install            # registers the /graphify skill for your coding agent
# in the agent, from the repository root:
/graphify . --update
python graph/build_map.py graphify-out/graph.json graph/map.html
```
