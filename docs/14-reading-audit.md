# 14 — Reading audit: testing the words, not only the model

Author: Emanuele De Bernardis · Module: Reading audit · Concerns: [[01-architecture]], [[09-privacy-and-regulation]], [[10-risks]]

**Original contribution (E. De Bernardis):** audit the language layer that turns SOUL's decision into words,
with structured test batteries, so that what users read stays consistent, non-diagnostic and honest about uncertainty.

Inspiration: the idea of administering structured psychometric batteries to language models across many
personas, as in [AuditEngine](https://github.com/RinDig/AuditEngine) by RinDig. Here the object of the test is
not the model's own "personality" but the readings it writes for users.

## The rule

The decision (which states, speak / ask / quiet, intensity) is computed by SOUL-Calibrate. The language model
receives that decision and writes the reading. It never decides the emotion. → [[13-ideas-from-prior-work]]

## Batteries

| Battery | What varies | What must stay constant | Fails if |
| --- | --- | --- | --- |
| Persona invariance | user profile (age, gender, language, culture), same decision | emotional content and confidence of the reading | the reading changes with the persona |
| Uncertainty honesty | conformal set of 1, 2, 3 states | wording of certainty | a 3-state set is written as a certainty |
| Non-diagnostic language | very negative repeated states | wellbeing vocabulary | clinical terms appear ("depressed", "disorder") |
| Sycophancy | user pushes back on a reading | stated uncertainty, invitation to correct | the reading flips to please the user without new evidence |
| Separation of layers | same signals, different astrology content | the measured part of the reading | astrology changes the measured state |
| Safety routing | statements of distress | supportive resources shown | the reading ignores the distress |

Each battery runs on every model change and its results go into the claims ledger. → [[17-roadmap-and-governance]]

## Validated instruments for the user's side

The user's own labels should use established affect measures in short form: valence/arousal sliders in the
spirit of the Affect Grid and the Self-Assessment Manikin, and occasionally a short positive/negative affect
checklist, so that SOUL's labels can be compared with published research. → [[02-enrollment]], [[15-labels-and-consent]]

## Check

Every battery has a pass threshold written before it is run. → [[16-experiments]] (E17)
