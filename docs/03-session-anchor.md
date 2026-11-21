# 03 — Session anchor (5 seconds)

Author: Emanuele De Bernardis · Module: Session anchor · Part of: [[01-architecture]] · Feeds: [[04-rolling-baseline]]

## What it does

At the start of each evening session Nightlet asks for one thing: read one short neutral sentence. At the
same time it takes resting heart rate from the bracelet. About five seconds in total.

## Why

- With the same words every time, only the voice changes. This controls **lexical leakage**: a model that
  reads the transcript instead of listening to the tone (LISTEN, VoxParadox).
- It follows the protocol of Koch et al. (2026): validated sentences read aloud, openSMILE eGeMAPS features
  (88 features) computed on the phone, raw audio deleted immediately, only features transmitted. → [[09-privacy-and-regulation]]
- It is the daily comparison point for the rolling baseline, and the equivalent of the between-session
  calibration used in brain–computer interfaces. → [[11-analogous-systems]]

## Variant

Rotate sentences of positive, neutral and negative valence (as Koch et al. did) to measure how much this
person's voice moves with content.

## Limits

- The effect of sentence content on voice was small in Koch et al. (|β| ≈ 0.06–0.13 SD).
- Background noise and phone position change the features → quality check (harmonics-to-noise ratio, voice detected) before use. → [[15-labels-and-consent]]
- The same sentence for months is boring → rotate a set of equivalent sentences. → [[10-risks]]
- Training and on-device feature code must be identical. → train/serve parity in [[13-ideas-from-prior-work]]

## Check

Test–retest stability of anchor features on "ordinary" days, and correlation between anchor deviation and
self-report. → [[16-experiments]] (E5)
