# 02 — Enrollment (entry calibration)

Author: Emanuele De Bernardis · Module: Enrollment · Part of: [[01-architecture]] · Solves: cold start in [[00-problem]]

**Original contribution (E. De Bernardis):** a short calibration at the start, in which the user's own
answers anchor the model's first readings, instead of trusting a generic model from day one.

## What it does

During the first 3–7 days Nightlet builds the person's reference profile:

- **Voice:** three fixed sentences read each day (same words every time) → personal prosody reference; later, the
  same sentence read in a clear state becomes the person's signature. → [[29-voice-signatures]]
- **Body:** resting heart rate, overnight heart-rate variability, skin temperature (bracelet, Apple Health or Health Connect).
- **Face (optional, explicit consent only):** a short neutral capture with the phone camera.
- **Self-report:** two sliders (valence: negative–positive; arousal: calm–activated) plus one free word.
  Sliders follow well-known affect instruments (Russell's Affect Grid, the Self-Assessment Manikin). → [[14-reading-audit]]

## Why it works

- Speaker enrolment improves few-shot emotion prediction (Triantafyllopoulos et al., 2022; CCC 0.650 vs 0.634).
- In-context personalization from a few labelled utterances (Ihori et al., NTT, 2025) and meta-learning (Meta-PerSER, Interspeech 2025).
- Self-supervised pre-training on a person's own unlabelled signals reaches the same performance with far fewer labels
  (Islam & Washington: under 5% of annotations on WESAD).
- In brain–computer interfaces a per-user calibration session is standard; the field reduces it with transfer learning. → [[11-analogous-systems]]

## Design choice

No full test at every use: it costs time, tires people and changes the answer itself (measurement reactivity,
see [[10-risks]]). One complete calibration at the start, then only the 5-second anchor ([[03-session-anchor]])
and a baseline that updates itself ([[04-rolling-baseline]]).

## Risks

- Read-aloud sentences carry little emotion (a limit stated by Koch et al.): free voice notes are also needed.
- The first days are not representative (novelty). → [[10-risks]]
- If the user skips enrollment: start from the population model with per-person normalisation and personalise later. → [[06-personal-model]]

## Check

The curve "number of answers → accuracy" shows after how many answers the personal model beats the generic one.
In the simulation ([[18-simulation]]) the personal baseline alone already beats the generic model, and 40 answers
raise accuracy from 0.58 to 0.69 on synthetic users. → [[08-evaluation-soul-bench]]
