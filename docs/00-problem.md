# 00 — The problem: a generic model cannot tell one person how they feel

Author: Emanuele De Bernardis · Module: Problem · Links: [[01-architecture]], [[references]]

## The gap in one sentence

SOUL (State Observation & Understanding Layer) has to tell one person how they are, but emotion signals
in voice, face and body are weak and highly personal in everyday life, and today there is no way to know
when a reading is right for that person.

## Evidence

- **Voice in daily life is a weak signal.** In the largest in-the-wild smartphone study (Koch et al., 2026;
  560 people, 9,877 recordings), prosody predicted momentary arousal at Spearman ρ = 0.12 and valence at ρ = 0.02.
- **Who is speaking dominates.** In the same data, 32.5% to 69.3% of the variance of voice features is between people.
- **Within-person fluctuations of happiness are hard to hear** (Weidman et al., 2020, *Emotion*).
- **Large audio-language models follow the words, not the voice** when the two disagree (LISTEN, 2025; VoxParadox, ICML 2026).
- **The body says "how much", not "which way":** skin conductance and heart rate rise with anxiety and with excitement alike (Fitbit / Google).
- **Faces are not reliable read-outs of specific emotions** (Barrett et al., 2019, *Psychological Science in the Public Interest*).
- **Group findings often do not hold for the individual** (Fisher, Medaglia & Jeronimus, 2018, *PNAS*): see [[12-clinical-practices]].

## What the product already says

- Nightlet's own disclaimer: voice and face readings are estimates; the user is the best source on their own experience.
- Privacy promise: "never used for training" → training data needs explicit, separate consent. See [[09-privacy-and-regulation]].
- The bracelet is optional and the face is not always available → modalities are often missing. See [[07-fusion]].

## Three sub-problems

1. **Cold start:** on day one the model does not know the person. → [[02-enrollment]]
2. **A moving reference:** people change over weeks (seasons, work, sleep, a new phone). → [[04-rolling-baseline]]
3. **Missing labels:** without the user's answer nobody knows whether a reading was right. → [[05-active-questions]]

## Why it matters

A confident wrong reading costs trust ("it doesn't know me"). The largest product risk is saying something
wrong about a person, with confidence.

## Check

This module is correct if every claim above links to a source in [[references]].
