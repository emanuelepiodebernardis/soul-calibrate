# 15 — Label quality and consent

Author: Emanuele De Bernardis · Module: Labels and consent · Connects: [[02-enrollment]], [[03-session-anchor]], [[05-active-questions]], [[06-personal-model]], [[08-evaluation-soul-bench]], [[09-privacy-and-regulation]]

## Why this module exists

The first knowledge graph of this project left isolated nodes: the user's self-report, the audio quality check,
per-state conformal calibration, Nightlet's disclaimer, GDPR and the Kintsugi case. They are exactly the pieces
that decide whether the loop is reliable and lawful. This module connects them.

## 1. The user's answer is the ground truth, and it is noisy

- Source: self-report (sliders + free word) and answers to active questions.
- Nightlet's disclaimer says the user is the best source on their own experience: so the user's label is
  SOUL-Bench's ground truth, not an external annotator.
- As with glucose meters, the user's calibration is itself an error source. → [[11-analogous-systems]]
- **Reliability weight** per answer: response time, consistency with nearby answers, identical answers every
  time, delay from the measured moment (late answers are memories, not states).
- Weighted labels feed the personal head (with shrinkage) and the SOUL-Bench metrics.

## 2. Signal quality before asking

- The audio quality check (harmonics-to-noise ratio, voice detected, noise) decides whether a measurement may
  trigger a question. Low-quality signal never produces a question.

## 3. Fairness of the decision

- Per-state (class-conditional) conformal calibration so that rare states (strong anger, sadness) are not under-covered.
- Coverage checked per user and per state in SOUL-Bench.

## 4. Consent levels

| Level | Stays on the phone | May leave the phone | Basis |
| --- | --- | --- | --- |
| 0 — Normal use | features, baseline, personal head, answers | nothing ("never used for training") | the product's promise |
| 1 — Federated improvement | as level 0 | aggregated updates with differential privacy | explicit, revocable consent |
| 2 — Research cohort | as level 0 | pseudonymised features and answers | separate explicit consent, GDPR |

- The private pilot cohort of [[19-private-cohort-pilot]] is level 2.
- The face stays out of levels 0–1 until it proves useful.

## 5. The medical line

- Questions name states ("tense", "low"), never conditions ("depressed", "anxious" in a clinical sense).
- Kintsugi shows the cost of entering diagnostic territory.
- If a user repeatedly reports very negative states, the product shows support resources, not a diagnosis. → [[12-clinical-practices]]

## Check

- Correlation between reliability weight and agreement with later answers.
- Share of questions blocked by the quality check.
- Per-state conformal coverage.
- Periodic audit: no level-0 data in any training set.
