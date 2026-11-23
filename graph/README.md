# Knowledge graph of the project

Built with [Graphify](https://pypi.org/project/graphifyy/) from `docs/`, `README.md`, `AUTHORS.md`, the
simulation code and results in `sim/`, and the engine in `engine/soulcal/` with its demo reports.

| File | What it is |
| --- | --- |
| `overview.png` | one picture of the areas and how they connect (in the main README): every area with its two strongest links, plus the strongest overall; rebuilt by `build_overview.py` |
| `map.html` | interactive map: open it in any browser, works offline |
| `GRAPH_REPORT.md` | most connected concepts, surprising links, weakly connected nodes (possible gaps), suggested questions |
| `graph.json` | the graph data (nodes, links, communities) |
| `build_map.py` | rebuilds `map.html` from `graph.json` with a precomputed layout |

At the last build (round 10): 1169 nodes, 3430 links, 35 communities (32 with three or more nodes), from 49 documents
and 35 code files: the docs, the simulation and the `soulcal` engine.

## What the graph found

Built nine times while the project grew; each round pointed at the next fix.

| Round | What the graph showed | What was done |
| --- | --- | --- |
| 1 (docs + simulation) | Active questions are the bridge between most areas; 23 isolated nodes (audio quality check, sliders, enrollment studies) | Answer rate became the first metric; E11–E14 added for the weak risks |
| 2 (+ recurring situations, incongruence) | "Situation stability" formed an island; the situation memory and the personal head were two separate clusters; incongruence was linked to the literature but not to fusion | Life-change and coverage experiments (docs/20), the population → head → memory order (docs/06), fusion linked to docs/21; new risks in docs/10 and E22–E23 |
| 3 (+ the engine) | The decision rule (speak / ask / quiet) and the engine are now the backbone, and SOUL-Bench is the bridge between evidence, risks, consent and regulation; 20+ concepts are linked to the code that implements them | SOUL-Bench ladder and quality gate implemented in `engine/soulcal` |
| 4 (+ question budget, eight states, coarse to fine) | The open question of docs/24 (start with the main states?) is answered by docs/25; the glucose-monitor analogy (docs/11) stops being an island and joins cohort transfer (E19) and the private pilot through archetypes; but the level of detail per reading and archetypes existed only in the simulation, linked to the engine by nothing but numpy | `engine/soulcal/detail.py` and a prototype `engine/soulcal/archetypes.py` with its own check |
| 5 (+ detail and archetype code) | Archetypes now connect to the engine, the personal baseline and the incongruence score; the check found that one head pooled over the cohort gives the gain and archetypes add nothing on top, so the pilot plan changed (pooled cohort first). New gaps: everything is still synthetic (E31, a first check on real voice, has no code yet); "when the bracelet should pulse" is in the README but not in code; the fits-no-archetype check is weak (it matched 88% of a type it never saw) | E31 added; the next code is the real-voice experiment |
| 6 (+ when and how the bracelet pulses) | docs/26 becomes one of the most connected documents (37 links), touching 12 areas: the decision rule, the question budget, clinical practice (HRV biofeedback, alarm fatigue, micro-randomised trials), the problem (the body says how much, not which way), fusion and the cohort pilot; HRV biofeedback, on paper since round 1, is now linked to code; 41 communities merge into 27, because the pulse is where the reading, the budget and the evaluation meet. New gaps: the support policy sits next to the engine (they share only the reading); the effect of a pulse is assumed until the cohort measures it (E32); no support is defined for "low" | `engine/soulcal/support.py`, E32 |
| 7 (+ voice and vibration) | docs/27 becomes the fourth most connected document (51 links, 15 areas), joining fusion, situation memory, clinical practice, the pulse and the products that calm with vibration; it answers two open questions: what the voice is for when the bracelet is always on (voice moments teach body-only moments) and how the pulse should be tuned (live heart rate, resonance breathing). The voice check-in existed only in the simulation, so it moved into the support policy (`invite`). New gaps: every effect of the pulse is assumed until E32–E34; whether invitations feel intrusive (E33); real voice (E31) | `SupportPolicy.decide` → `invite`, E33–E34 |
| 8 (+ speech front end) | docs/28 links 11 areas (32 links); E31, open since round 5, now has code (`realvoice/`) linked to the evidence that the speaker dominates the voice, to SOUL-Bench and to the voice channel of the engine. New gaps: the real-voice check runs beside the engine (embeddings and a linear head), not through it; the next step is to feed emotion2vec+ scores into the engine's voice channel on real recordings | `realvoice/e31_real_voice.py`, `channels_sim.frontend_check` |
| 9 (+ voice-and-body signatures) | docs/29 links 12 areas (37 links) and turns the enrollment sentences and the 5-second session anchor, on paper since round 1, into code, joined with tagged readings in one area; voluntary modes connect it to the question budget. New gaps: the signature model sits beside the engine (its probabilities still have to be passed into the voice channel), and the real-voice check (E31) does not yet use signatures: emotion2vec+ features are the natural input | `anchors.SignatureModel`, `anchors.MODES`, E35–E36 |
| 10 (+ one reading: the signature in the engine) | Both round-9 gaps closed: `SoulEngine.enroll`, `anchor` and `tag` and the engine check sit with the signature code, `_use_signature` joins the engine's personal baseline, and docs/29 now has 100 links into 20 areas (from 37 into 12), so the signature is no longer beside the engine but one of its bridges. E31's signature arms tie the real-voice check to the fixed-sentence protocol. Still open: everything is synthetic; with a strong speech model, whether the signature should replace or add to the generic voice reading has to be measured again | `SoulEngine.enroll/anchor/tag`, `Reading.voice_features`, `anchors_sim.engine_check`, E31 signature arms |

Still only on paper (no code yet): the enrollment and anchor screens in the app (their logic is in `anchors.py`), the reading audit batteries, the
private cohort pilot, the measured effect and tuning of the pulse (E32, E34), voice check-ins on real people
(E33), signatures on real people (E35, E36), the micro-randomised trials, and running the real-voice check (E31,
ready in `realvoice/`). Most need real users or Nightlet's app; E31 only needs public speech data and a GPU.

## Rebuild

```bash
pip install graphifyy networkx
graphify install            # registers the /graphify skill for your coding agent
# in the agent, from the repository root:
/graphify . --update
python graph/build_map.py graphify-out/graph.json graph/map.html
```
