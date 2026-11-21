# 07 — Fusion of sources

Author: Emanuele De Bernardis · Module: Fusion · Part of: [[01-architecture]] · Uses: [[06-personal-model]]

| Source | What it says | Reliability |
| --- | --- | --- |
| Words (text, transcript) | content, topic, explicit valence | high, but it is what the user already knows |
| Voice (prosody, embeddings) | arousal, sometimes valence; weak in daily life | medium-low, very personal |
| Body (HR, HRV, EDA, temperature) | intensity of activation, not its sign | good for "how much", silent on "which way" |
| Face (optional) | facial configurations, not emotions (Barrett et al., 2019) | low, high regulatory risk |
| Context (time, sleep, weather, activity) | explains deviations | useful to rule out confounders |

## Key rule

Hypotheses about the state (which emotion) come from words and voice; the body sets intensity and confidence.
Example: high heart rate + raised voice → high activation; words and voice decide between anger, stress and
excitement. First rule out movement (accelerometer): after climbing stairs the heart rate rises for other reasons.

## Missing modalities

The bracelet is optional, the face often absent: late fusion with learned weights and explicit handling of
missing modalities (a survey: Wu et al., 2024). The model must work with a single source.

## The case that matters

"I'm fine" said in a flat voice: words and voice conflict. General audio-language models follow the words
(VoxParadox: no model above 31% across 12 models). A conflict relative to the person's baseline is exactly the
moment to ask. → [[05-active-questions]]

## The bracelet as an intervention, not only a sensor

Heart-rate-variability biofeedback (paced slow breathing guided by feedback) reduced self-reported stress and
anxiety with a large effect in a meta-analysis (Goessl et al., 2017; 24 studies, 484 participants, g = 0.83).
The haptic pulse can pace breathing, and HRV becomes the proximal outcome to measure. → [[12-clinical-practices]]

## Check

Gain of voice over words (B4 vs B1), accuracy on conflict cases, ablation per source. → [[08-evaluation-soul-bench]], [[16-experiments]] (E6, E13)
