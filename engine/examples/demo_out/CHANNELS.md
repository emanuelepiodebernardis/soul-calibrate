# Voice, words, face and body (synthetic people)

Engine demo people, 5 seeds x 20 people, up to 1 question a day, 6 weeks; scored on weeks 5-6, before learning.

## A. One set of sources at a time, present at every moment

| Sources | Accuracy | Speaks | Right when it speaks |
| --- | --- | --- | --- |
| Body only (bracelet) | 0.52 | 0% | – |
| Voice only | 0.60 | 24% | 0.83 |
| Words only | 0.66 | 28% | 0.88 |
| Voice + words | 0.69 | 34% | 0.89 |
| Voice + words + body | 0.81 | 58% | 0.93 |
| All four (+ face) | 0.82 | 61% | 0.93 |

## B. The bracelet is always on; the app is used in a share of moments

| Moments with the app | Accuracy, all | With the app | Body-only moments | Tense moments reached (pulse or offer) | Pulses at tense moments |
| --- | --- | --- | --- | --- | --- |
| 100% | 0.77 | 0.78 | – | 76% | 90% |
| 50% | 0.69 | 0.74 | 0.67 | 45% | 86% |
| 25% | 0.62 | 0.71 | 0.61 | 27% | 80% |
| 10% | 0.51 | 0.64 | 0.52 | 13% | 83% |

## C. The body triggers, the voice decides (app used in 25% of moments)

At a body-only moment, body aroused and tension possible: a 5-second voice note is invited (at most 1 a day; half of the invitations answered).

| Policy | Accuracy, body-only moments | Tense moments reached | Pulses at tense moments | Invitations per week |
| --- | --- | --- | --- | --- |
| no invitation | 0.62 | 28% | 85% | 0.0 |
| voice check-in | 0.64 | 46% | 88% | 1.9 |

## D. Stronger speech front ends (open speech-recognition and speech-emotion models)

How clearly voice and words show the state is multiplied; each person's habits (flat voice, serious face, saying 'fine' when tense) stay the same.

| Front end | Generic reading | With personal calibration | Gain |
| --- | --- | --- | --- |
| Today's generic models | 0.62 | 0.77 | +0.16 |
| Stronger open models (x1.5) | 0.74 | 0.85 | +0.11 |
| Much stronger (x2) | 0.82 | 0.90 | +0.08 |
| Near-perfect on the words and the voice (x3) | 0.91 | 0.96 | +0.05 |
