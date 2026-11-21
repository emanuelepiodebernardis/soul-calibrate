# 22 — The engine: code Nightlet can run on its own data

Author: Emanuele De Bernardis · Module: Engine · Implements: [[01-architecture]], [[04-rolling-baseline]], [[05-active-questions]], [[06-personal-model]], [[07-fusion]], [[20-recurring-situations]], [[21-text-face-incongruence]]

**Original contribution (E. De Bernardis):** `engine/soulcal`, a small Python package (numpy only) that takes
the readings Nightlet's device and app already produce (facial expression model outputs, speech emotion model
outputs, text model outputs, heart rate, HRV, skin temperature, movement) and returns, for every reading,
speak / ask / quiet with the options to offer. It learns from the person's answers and corrections, and keeps
all its state in a small JSON file on the phone.

## How the concepts map to code

| Concept | Code | Docs |
| --- | --- | --- |
| Personal baseline (z-scores, usual expression removed) | `baseline.PersonalBaseline` | [[04-rolling-baseline]] |
| Drift trigger (conformal test martingale) | `PersonalBaseline._martingale_step` | [[04-rolling-baseline]], [[13-ideas-from-prior-work]] |
| Fusion of face, voice, words and body, missing channels allowed | `model.FusionHead` | [[07-fusion]] |
| Personal head shrunk toward a transparent prior | `FusionHead.update` (L2 pull to the prior) | [[06-personal-model]] |
| Situation memory (time, day and what the channels say) | `model.SituationMemory` | [[20-recurring-situations]] |
| Conformal set, speak / ask / quiet, daily question budget | `engine.SoulEngine.observe` | [[05-active-questions]] |
| Adaptive conformal thresholds per person | `SoulEngine._learn` (`delta`) | [[20-recurring-situations]] |
| One-tap "not quite" corrections | `SoulEngine.correct` | [[20-recurring-situations]] |
| Words vs expression disagreement, read against the person | `SoulEngine._incongruence` | [[21-text-face-incongruence]] |
| Explanation: evidence per channel for each reading | `Decision.contributions` | [[14-reading-audit]] |
| SOUL-Bench ladder B0–B6, within-person metrics | `bench.soul_bench` | [[08-evaluation-soul-bench]] |
| Quality gate: no question from body signals alone | `EngineConfig.ask_needs_expression` | [[15-labels-and-consent]] |
| Personal pattern graph with statistical guardrails | `patterns.find_patterns`, `patterns.to_graph` | below |
| Reflection layer (moon phase, moon sign, sun sign) | `astro` | below |

## Using it

```python
from soulcal import SoulEngine, Profile, Reading, basic_emotions_to_states
eng = SoulEngine(Profile("user-42"))
d = eng.observe(Reading("user-42", ts, face=basic_emotions_to_states(fer_output),
                        voice=ser_probs, text=llm_probs, heart_rate=71, hrv_rmssd=38))
if d.action == "ask":
    show_question(d.options)                 # e.g. ["tense", "tired"]
eng.answer(d.reading_index, "tense")         # or eng.correct(...) after a spoken reading
eng.save("user-42.json")                     # stays on the device
```

```bash
cd engine
python -m pytest tests -q                    # 13 tests
python -m soulcal bench --readings my_readings.csv   # SOUL-Bench ladder
python -m soulcal demo --out examples/demo_out
python -m soulcal run --readings my_readings.csv --out results   # CSV format in soulcal/schema.py
```

Any facial, speech or text model can feed it: only its probabilities over the four states are needed
(`basic_emotions_to_states` converts the usual seven basic emotions). The engine is the decision and
personalization layer on top of Nightlet's models or its partners' models.

## Demo: today's reading vs the engine (synthetic people)

20 synthetic people, 6 weeks, 3 evening readings a day, every channel with realistic gaps; each person has a
weekly routine, a serious-looking face, a flat voice, writes "fine" when tense half of the time, and a resting
heart rate far from the population average. At most one question a day. Full output: `engine/examples/demo_out/DEMO.md`.

| Setting | Accuracy, week 1 | Accuracy, week 6 | Accuracy when speaking, week 6 | Questions per week |
| --- | --- | --- | --- | --- |
| Today: generic reading (population norms) | 0.60 | 0.57 | 0.68 | 0 |
| Personal baseline only | 0.68 | 0.63 | 0.87 | 0 |
| **Engine: baseline + questions + corrections + memory** | 0.68 | **0.77** | **0.94** | about 6 |

- Wrong readings fall from 43% to 23% by week 6, and when Nightlet speaks it is right 94% of the time.
- The personal baseline alone already removes the "serious face" and resting-heart-rate biases (+8 points in
  week 1); questions and corrections add the rest over the weeks.
- Disagreement between words and face, voice and body triggered 29 questions; 48% came at moments of real
  masking, which happens at 9% of readings: five times the base rate.
- A quality gate never asks from body signals alone: with nothing said or shown, a question would be a guess.

## SOUL-Bench in code

`bench.soul_bench` runs the ladder of [[08-evaluation-soul-bench]] on any person's readings, with their own
labels as ground truth, every rung scored before it learns. Mean over the 20 demo people:

| Rung | Accuracy, first 2 weeks | Accuracy, last 2 weeks | Accuracy when speaking | Recall: tense |
| --- | --- | --- | --- | --- |
| B0 the user's own average | 0.22 | 0.29 | 0.26 | 0.00 |
| B1 words only | 0.48 | 0.46 | 0.68 | 0.21 |
| B2 voice only | 0.47 | 0.43 | 0.67 | 0.30 |
| B3 face only | 0.33 | 0.34 | 0.40 | 0.42 |
| B4 all channels, generic | 0.59 | 0.57 | 0.73 | 0.37 |
| B5 personal baseline | 0.69 | 0.64 | 0.85 | 0.55 |
| B6 full loop | 0.69 | **0.76** | **0.90** | **0.72** |

Tension is what masking hides: the full loop finds it 72% of the time, the generic fusion 37%.
`python -m soulcal bench --readings my.csv` runs the same ladder on real readings with a `self_report` column.

## The personal pattern graph

For each person, `patterns.find_patterns` tests every link "factor → state" between the labelled readings
and four layers of factors:

- **context:** day of the week, time of day, weekend;
- **body:** heart rate above usual, HRV below usual, moving more than usual (against the person's own norm);
- **expression:** what face, voice and words suggest, and whether words and expression disagree;
- **reflection:** moon phase, moon sign, moon in the person's sun sign (`astro.py`).

Guardrails, because many links are tested at once and a few will always look significant by chance:

1. Fisher exact test for each link, Benjamini–Hochberg correction across all links (false discovery rate 10%).
2. Discovery on the first half of the person's history, **replication on the second half**, same direction.
3. **Supported** = passes both; **exploratory** = suggestive only, shown as an idea to reflect on, never as a
   finding; everything else is not drawn.
4. The reflection layer never feeds the reading. It is there because Nightlet offers it to users, so that
   each person can see whether a pattern holds in their own data.

In the demo person (6 weeks, labels as in a consented diary study), the supported links are real parts of the
routine ("night → low", "heart rate above usual → energized", "moving → energized"). Two moon links looked
significant on all data (first quarter → calm, p = 0.016; moon in Capricorn → calm, p = 0.021) but failed the
correction and the replication: no moon effect was planted. This is exactly the trap the guardrails exist for.

The graph is written in the project-map format, so the same viewer draws it:
`python graph/build_map.py engine/examples/demo_out/patterns.json engine/examples/demo_out/patterns_map.html`.

## Limits

- Tuned and tested on synthetic people; real data will need new defaults (thresholds, budget, bandwidth).
- The physiological prior (heart rate up, HRV down = arousal) is a starting point, learned away per person.
- The moon-sign computation is approximate (about 1–2 degrees); see `astro.py`.
- No model of the face, voice or text is included: the engine consumes their outputs.

## Check

- `python -m pytest engine/tests -q` passes (13 tests, including "the loop beats today's generic reading" and
  "no supported moon pattern when none is planted").
- On real data: `python -m soulcal run` on a pilot export, then SOUL-Bench metrics per user ([[08-evaluation-soul-bench]]).
