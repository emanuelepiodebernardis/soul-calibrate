# 06 — Personal model

Author: Emanuele De Bernardis · Module: Personal model · Part of: [[01-architecture]] · Trained with labels from: [[05-active-questions]], [[02-enrollment]]

## Structure

- **Shared encoders (population):** emotion2vec or WavLM for voice, a text encoder for words, PaPaGei or similar for the bracelet's PPG. Frozen or nearly frozen.
- **Inputs normalised on the personal baseline** (person-mean centering). → [[04-rolling-baseline]]
- **A small personal head** per user, updated on the phone. It sees the population model's log-probabilities and
  the user's normalised features, and is shrunk toward the population until answers accumulate.
- **On the bracelet:** the head can be an integer additive model with exact per-signal contributions,
  so every reading can say which signal moved and by how much. → [[13-ideas-from-prior-work]]

## Personalisation strategies compared (scale B0–B6 of SOUL-Bench)

1. Person normalisation only (zero labels): a strong baseline (*Behavior Therapy*, 2026).
2. Personal linear head with a few labels.
3. Meta-learning (Meta-PerSER).
4. In-context learning with a speech-language model (Ihori et al., 2025).
5. Self-supervised pre-training on the person's unlabelled signals (Islam & Washington).

→ compared in [[08-evaluation-soul-bench]].

## Cold start

No labels: population model + normalisation. With 10–20 labels: personal head. The number of labels needed is
the quantity to measure. In the simulation the head adds 2–8 accuracy points over the baseline between 5 and
40 answers. → [[18-simulation]]

## Diagnose before adapting

Decide per user whether the error is a **calibration** problem (the ranking is right, the threshold is wrong:
fix with a bias or temperature, no labels needed beyond a few) or a **representation** problem (the ranking is
wrong: needs a richer head and more answers). This diagnosis comes from the author's drift research. → [[13-ideas-from-prior-work]]

## Risks

- Over-fitting with few labels → regularisation toward the population (shrinkage).
- Noisy or reactive labels → weights by answer reliability. → [[15-labels-and-consent]]
- Forgetting: incremental updates without losing the past (same family of problems as drift).
