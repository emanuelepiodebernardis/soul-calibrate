# soulcal demo: today's reading vs SOUL-Calibrate

20 synthetic people, 6 weeks, 3 evening readings a day, every channel Nightlet reads (face, voice, words, heart rate, HRV, skin temperature, movement), with channels missing at realistic rates. Each person has a weekly routine, a serious-looking face, a flat voice, masks tension in words half of the time, and a resting heart rate far from the population average. At most one question a day. Synthetic data: the numbers show how the code behaves, not real users.

## Accuracy (4 states, chance 0.25)

| Setting | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Today: generic reading (population norms, no questions) | 0.60 ± 0.07 | 0.59 ± 0.12 | 0.56 ± 0.11 | 0.54 ± 0.10 | 0.57 ± 0.12 | 0.57 ± 0.09 |
| Personal baseline only (no questions) | 0.68 ± 0.11 | 0.70 ± 0.09 | 0.64 ± 0.11 | 0.63 ± 0.12 | 0.65 ± 0.10 | 0.63 ± 0.12 |
| SOUL-Calibrate: baseline + questions + corrections + memory | 0.68 ± 0.10 | 0.70 ± 0.10 | 0.71 ± 0.09 | 0.72 ± 0.10 | 0.75 ± 0.08 | 0.77 ± 0.10 |

## Share of readings where Nightlet speaks

| Setting | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Today: generic reading (population norms, no questions) | 0.41 ± 0.08 | 0.39 ± 0.11 | 0.31 ± 0.11 | 0.30 ± 0.10 | 0.31 ± 0.11 | 0.36 ± 0.10 |
| Personal baseline only (no questions) | 0.39 ± 0.10 | 0.32 ± 0.11 | 0.31 ± 0.10 | 0.33 ± 0.13 | 0.32 ± 0.12 | 0.32 ± 0.08 |
| SOUL-Calibrate: baseline + questions + corrections + memory | 0.38 ± 0.10 | 0.35 ± 0.13 | 0.37 ± 0.18 | 0.38 ± 0.16 | 0.43 ± 0.14 | 0.42 ± 0.16 |

## Accuracy when Nightlet speaks

| Setting | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Today: generic reading (population norms, no questions) | 0.77 ± 0.10 | 0.76 ± 0.13 | 0.72 ± 0.20 | 0.74 ± 0.18 | 0.72 ± 0.18 | 0.68 ± 0.20 |
| Personal baseline only (no questions) | 0.89 ± 0.08 | 0.84 ± 0.16 | 0.84 ± 0.14 | 0.84 ± 0.15 | 0.85 ± 0.16 | 0.87 ± 0.15 |
| SOUL-Calibrate: baseline + questions + corrections + memory | 0.89 ± 0.12 | 0.90 ± 0.10 | 0.85 ± 0.11 | 0.93 ± 0.08 | 0.90 ± 0.09 | 0.94 ± 0.09 |

## Questions per week

| Setting | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Today: generic reading (population norms, no questions) | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| Personal baseline only (no questions) | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| SOUL-Calibrate: baseline + questions + corrections + memory | 7.00 ± 0.63 | 6.20 ± 0.81 | 6.35 ± 1.01 | 6.40 ± 1.07 | 5.90 ± 1.26 | 6.05 ± 0.74 |

## Words vs expression

Questions triggered by an unusual disagreement between words and face, voice and body: 29. 48% of them came at moments when the person was really masking tension (masking happens at 9% of readings).

## What the head learned to trust (mean weight per channel; start: face 0.50, voice 0.60, words 0.80)

| Face | Voice | Words |
| --- | --- | --- |
| 0.51 | 0.59 | 0.73 |

## SOUL-Bench ladder (mean over people)

Every rung reads the same readings and is scored before it learns from them. Generic = population norms, no personal correction.

| Rung | Accuracy, first 2 weeks | Accuracy, last 2 weeks | Speaks | Accuracy when speaking | Recall: tense | Recall: low |
| --- | --- | --- | --- | --- | --- | --- |
| B0 user's own average | 0.22 | 0.29 | 1.00 | 0.26 | 0.00 | 0.27 |
| B1 words only | 0.48 | 0.46 | 0.15 | 0.68 | 0.21 | 0.37 |
| B2 voice only | 0.47 | 0.43 | 0.10 | 0.67 | 0.30 | 0.67 |
| B3 face only | 0.33 | 0.34 | 0.07 | 0.40 | 0.42 | 0.23 |
| B4 all channels, generic | 0.59 | 0.57 | 0.35 | 0.73 | 0.37 | 0.86 |
| B5 personal baseline | 0.69 | 0.64 | 0.33 | 0.85 | 0.55 | 0.69 |
| B6 full loop | 0.69 | 0.76 | 0.39 | 0.90 | 0.72 | 0.71 |
