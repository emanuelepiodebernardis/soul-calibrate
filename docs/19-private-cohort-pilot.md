# 19 — Private cohort pilot: from today's approach to SOUL-Calibrate

Author: Emanuele De Bernardis · Module: Pilot · Uses: [[16-experiments]] (E19), [[15-labels-and-consent]], [[18-simulation]]

**Original contribution (E. De Bernardis):** test the loop on a private, consented group first. The group's
answers improve the shared reading model, so the improvement reaches also the users who will never be asked
anything.

## Why a private cohort

- Nightlet promises "never used for training": a separate, explicitly consented group (consent level 2) is the
  clean way to obtain in-domain labels. → [[15-labels-and-consent]]
- Public emotion datasets differ from Nightlet's users (acted speech, other microphones, other people).
  In-domain answers correct that gap.

## Design

| Item | Proposal |
| --- | --- |
| Group | 30–60 adults, consent level 2, team members first |
| Duration | 4–6 weeks |
| Each participant | enrollment (3–7 days), session anchor, up to 3 questions a day |
| Randomisation | micro-randomised: ask vs not ask, two options vs open question, pulse vs no pulse |
| Control arm | the current SOUL readings, computed in parallel and never shown, on the same moments |
| Held-out users | a second group that never answers questions, to measure transfer |

## What is compared

1. **Today:** current SOUL model.
2. **+ personal baseline:** the same model on person-normalised signals.
3. **+ cohort answers:** the shared model retrained with the cohort's answers.
4. **Full loop:** personal head for users who answer.

Measured on the held-out users (rows 1–3) and on the cohort itself (row 4): within-person accuracy and CCC,
per-state coverage, answer rate, unnecessary-question rate, and proximal calm after a question.

## What the simulation suggests (synthetic, not a promise)

| Setting | Accuracy on users never asked |
| --- | --- |
| Today: generic model on public data | 0.550 |
| + cohort of 10 users | 0.571 |
| + cohort of 25 users | 0.576 |
| + cohort of 50 users | 0.590 |
| Full loop (user also answers 20 questions) | 0.652 |

See [[18-simulation]] for the setting and the caveats.

## Decision at the end of the pilot

- Ship the baseline + cohort-trained model to everyone if it beats today's model on held-out users.
- Ship questions only if the answer rate stays high and the unnecessary-question rate stays low.
- Drop any signal (e.g. face) that adds nothing.
