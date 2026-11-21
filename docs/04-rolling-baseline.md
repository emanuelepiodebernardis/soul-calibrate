# 04 — Rolling personal baseline

Author: Emanuele De Bernardis · Module: Rolling baseline · Part of: [[01-architecture]] · Fed by: [[02-enrollment]], [[03-session-anchor]]

## What it does

Keeps, for each person, the mean and spread of every signal (voice features, heart rate, HRV, sleep,
temperature) and turns each new measurement into a deviation from that person's norm (a personal z-score).

## Why it works

- **Person-mean centering** let a pooled machine-learning model match personalised models in a 2026 study of
  308 adults with passive smartphone sensing (*Behavior Therapy*); within-person R² was 0.16–0.26.
- **Fitbit Body Response** learns each wearer during the first month on the wrist. → [[11-analogous-systems]]
- **Group-to-individual generalisability often fails** (Fisher et al., 2018): the person is the right reference. → [[12-clinical-practices]]

## Updating and drift

- Exponential moving average with a long window (weeks), so one bad week does not become the norm.
- **Label-free drift trigger:** a conformal test martingale flags when a person's signals stop looking like
  their baseline (new phone, new job, illness) and triggers a light re-enrollment or extra questions.
  This reuses the author's drift-adaptation work. → [[13-ideas-from-prior-work]]
- In the simulation, after a step change in the signals, a rolling baseline recovers the accuracy of a user
  with no change (0.581 vs 0.584), while a fixed baseline drops to 0.541. → [[18-simulation]]

## Traps

- If the baseline also absorbs anomalous days, it "normalises" a long stressful period: separate drift from real change. → [[10-risks]]
- Physiological confounders: exercise, caffeine, alcohol, cycle, medication. Exclude movement before interpreting. → [[07-fusion]]
- A new device or microphone shifts features → baseline per device.

## Check

Within-person metrics (centred values), stability week by week. → [[08-evaluation-soul-bench]], [[16-experiments]] (E9, E18)
