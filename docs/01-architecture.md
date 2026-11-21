# 01 — Architecture of SOUL-Calibrate

Author: Emanuele De Bernardis · Module: Architecture · Solves: [[00-problem]] · Measured by: [[08-evaluation-soul-bench]]

**Original contribution (E. De Bernardis):** a personal calibration layer for SOUL that combines an entry
calibration, a personal baseline, and questions to the user when the model is unsure, so that every answer
improves the next reading.

## The loop

1. **Enrollment** (once, 3–7 days) → [[02-enrollment]]
2. **Session anchor** (5 seconds per session: one fixed sentence + resting heart rate) → [[03-session-anchor]]
3. **Rolling personal baseline** (updates slowly, resists drift) → [[04-rolling-baseline]]
4. **Deviation detector:** each new signal is expressed against the person's own norm
5. **Personal model:** shared population encoders + a small per-user head → [[06-personal-model]]
6. **Fusion** of words, voice, body and optional face → [[07-fusion]]
7. **Decision with a guarantee:** a conformal set of plausible states
   - one state → Nightlet **speaks**
   - two or three states → Nightlet **asks**, offering exactly those states → [[05-active-questions]]
   - too many states, or poor signal quality → Nightlet **stays quiet** or asks openly
8. **Answer → label → update** of the personal head and the baseline (closed loop) → [[15-labels-and-consent]]

The decision is computed from calibrated statistics; a language model only writes the words of a reading
and never decides what the reading is. → [[13-ideas-from-prior-work]], [[14-reading-audit]]

## Where things run

- **On the phone / bracelet:** feature extraction, baseline, personal head, decision.
- **On the server, only with consent:** improvement of the shared population model, optionally federated.

## Data flow

raw signals → on-device features → deviation from baseline → personal model → conformal set
→ speak / ask / quiet → user answer → update.

## Critical dependencies (found with the knowledge graph)

- **Active questions are the bridge node of the whole system:** if users stop answering, the loop stops.
  Answer rate is the first metric to watch. → [[10-risks]]
- **Conformal guarantees need calibration data** that a new user does not yet have. → [[02-enrollment]]

## Check

The architecture is sound if a new team member can follow one moment of data from the microphone to the
user's answer using only this page and the linked modules.
