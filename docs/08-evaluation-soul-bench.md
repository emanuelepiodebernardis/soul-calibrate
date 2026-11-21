# 08 — Evaluation: SOUL-Bench

Author: Emanuele De Bernardis · Module: Evaluation · Evaluates: [[01-architecture]] and every module

**Original contribution (E. De Bernardis):** SOUL-Bench, a reproducible evaluation protocol whose ground
truth comes from the user, that measures for each person what every signal adds over the others and is the
same harness for in-house and partner models.

## Questions

1. After how many answers does the personal model beat the generic one?
2. How much does baseline normalisation alone give, with no labels?
3. How many questions does active selection save compared with random timing?
4. Does voice add anything to words, for this person?
5. Does the conformal set keep its promised coverage for every user and every state?
6. How fast does the model degrade without recalibration (drift)?
7. Does asking help the user (proximal calm), not only the model? → micro-randomised trial in [[12-clinical-practices]]

## The model ladder

| Step | Model | Question it answers |
| --- | --- | --- |
| B0 | User's own average | How much is won just by knowing who it is? |
| B1 | Text only (transcript + classifier or LLM) | How much do the words say? |
| B2 | eGeMAPS prosodic features | Does classic prosody add anything? |
| B3 | emotion2vec / WavLM + small head | Do modern encoders add anything? |
| B4 | Late fusion text + voice (+ body) | Do sources together beat the best alone? |
| B5 | B4 personalised (baseline + per-user head) | How much does adapting to the person add? |
| B6 | Open audio-language model as judge | Does a generalist do better or worse? |

Each step enters the product only if it beats the one below.

## Metrics

- **Within person:** CCC and Spearman on per-user centred values, alongside global ones.
- **Label efficiency:** area under the curve "answers → accuracy".
- **Question efficiency:** accuracy per question asked; answer rate; share of "none of these".
- **Calibration:** ECE; empirical conformal coverage per user and per state; mean set size.
- **Prompt precision:** share of questions that the answer shows were unnecessary (alarm-fatigue metric, as the
  false-alarm rate per 24 h is for wearable seizure detectors). → [[12-clinical-practices]]
- **Burden:** questions per day, enrollment drop-out.
- **Stability:** accuracy week by week.
- **Fairness:** by sex, language, device, noise.
- **Cost:** latency, memory, energy on phone and bracelet.

## Protocol

- Always split by person and in time (train on the past, evaluate on the future of the same person).
- Simulate active learning offline on labelled data (as Tazarv et al. did) before touching real users. A first
  simulation is in this repository. → [[18-simulation]]
- Data: public (MSP-Podcast, WESAD, CREMA-D), team dogfooding, consented cohort. → [[09-privacy-and-regulation]]
- Every claim recorded in a claims ledger with its evidence file, provenance class and hash. → [[17-roadmap-and-governance]]

## Where it may fail (to look for actively)

- People whose voice barely moves: voice adds nothing → the system must notice and rely on words and body.
- Users who always answer the same (habit or reactivity). → [[10-risks]]
- Rare states (strong anger): worse conformal coverage. → [[16-experiments]]
