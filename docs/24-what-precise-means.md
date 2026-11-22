# 24 — What "precise" means, and what happens with eight states

Author: Emanuele De Bernardis · Module: Granularity · Extends: [[08-evaluation-soul-bench]], [[23-question-budget]], [[05-active-questions]] · Experiments: E27–E28 in [[16-experiments]]

## 1. Precise on what

Every accuracy in this repository answers one question: **for this person, at this moment, does the reading name
the state the person would choose themselves?**

- **The target** is the user's own label, among the states offered (calm, energized, tense, low: the four
  quadrants of valence, pleasant to unpleasant, and arousal, activated to deactivated). In the simulations the
  true state is known; with real people it is their self-report, which is noisy.
- **This matches SOUL's own definition:** Nightlet's disclaimer says the user is the best source on their own
  experience, so "precise" means agreeing with the person, not with an external annotator or a clinician.
- **What it covers:** which state, per reading, per person; when the system speaks, how often it is right
  (accuracy when speaking); how often the true state is among the plausible ones (coverage).
- **What it does not cover yet:** intensity (how tense), mixed states (tense and energized together), the
  cause (why), long-term mood, and anything clinical. Those are separate targets with their own labels
  ([[17-roadmap-and-governance]]).
- **What a number like 0.90 means:** in the synthetic world, 9 readings out of 10 name the state the person
  would pick. Real people will be lower, because real self-reports are noisier and real situations less regular.

## 2. Eight states: intermediate emotions on the same circle

States are placed on the valence × arousal circle. Four states are the quadrants; eight add an intermediate
state between each pair (for example *content* between calm and energized, *tired* between calm and low). The
signal strength is the same, so the eight states are closer to each other and harder to tell apart. Chance:
0.25 with four states, 0.125 with eight. "Within one" counts a reading as close when it names the true state or
its neighbour on the circle. Full tables: `sim/results/STATES.md`; script `sim/run_states.py`.

### A new problem: the question rule stops asking

With eight states the generic model is torn between more than three states most of the time, so the rule
"ask when 2 or 3 states are plausible" almost never fires: 1.2 questions in a week, accuracy 0.324. **Fix:**
also ask when more states are plausible, offering the three most likely ("none of these" leads to an open
answer). One calibration week, then 5 test days without questions:

| World and policy | Questions | Accuracy | Within one | Accuracy when speaking |
| --- | --- | --- | --- | --- |
| 4 states, no questions | 0 | 0.439 | 0.894 | 0.664 |
| 4 states, ambiguous moments, 1 a day | 5.9 | 0.839 | 0.959 | 0.933 |
| 8 states, no questions | 0 | 0.234 | 0.560 | – |
| 8 states, old rule (2-3 plausible only) | 1.2 | 0.324 | 0.590 | 0.920 |
| 8 states, wide questions, 1 a day | 6.7 | 0.737 | 0.852 | 0.907 |
| 8 states, wide questions, 2 a day | 10.9 | 0.841 | 0.901 | 0.946 |
| 8 states, 2 a day, less sure answers (10% / 25% errors) | 11.6 | 0.791 | 0.887 | 0.913 |

### Eight states reach the same level, more slowly

Questions allowed for 28 days (wide questions allowed):

| World, budget | Day 7 | Day 14 | Day 28 | Days to 0.80 | Days to 0.90 | Answers by day 28 |
| --- | --- | --- | --- | --- | --- | --- |
| 4 states, 1 a day | 0.83 | 0.92 | 0.96 | 6 | 11 | 14.5 |
| 4 states, 2 a day | 0.90 | 0.94 | 0.98 | 4 | 8 | 16.1 |
| 8 states, 1 a day | 0.74 | 0.87 | 0.95 | 10 | 20 | 19.9 |
| 8 states, 2 a day | 0.84 | 0.93 | 0.96 | 6 | 12 | 23.9 |
| 8 states, 4 a day | 0.86 | 0.93 | 0.96 | 5 | 11 | 24.9 |

- Eight states need **about 50% more answers and about twice the time** at 1 a day; at 2 a day they reach 0.90
  in 12 days instead of 8.
- When the reading is wrong with eight states, it is usually a neighbour (within one: 0.90 at 2 a day after one
  week, 0.97 after four), which a user experiences as "close", not "wrong".

## 3. What to do in the product

1. **Start with four states** for everyone; personalization is fastest there.
2. **Refine to eight** for people who engage (a vocabulary that grows, [[17-roadmap-and-governance]]), once the
   four-state reading is stable for them, ideally with the Fast preset.
3. **Ask wide when needed:** when more than three states are plausible, offer the three most likely
   (`ask_wide` in `sim/` and in the engine).
4. **Tested since:** showing the main state until the fine one is sure, with fine questions from day one, keeps
   readings right from the first days without slowing learning. → [[25-coarse-to-fine-and-archetypes]]
5. **Next to test:** intensity as a second, separate target.

## Check

- E27: on real users, agreement with self-report at four vs eight states, and "within one" with eight.
- E28: answers needed per user to reach a target at four vs eight states, with wide questions.
