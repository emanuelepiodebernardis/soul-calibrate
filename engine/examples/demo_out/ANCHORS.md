# Personal voice-and-body signatures from a fixed sentence (synthetic people)

5 seeds x 40 people; 6 prosodic features and 3 body signals; enrollment 7 days x 3 neutral readings; tagged readings in days 8-21 when the person is in that state; scored on free voice notes in days 22-42 (4 states, chance 25%).

| Reference | Accuracy on free voice notes |
| --- | --- |
| Generic (no personal reference) | 0.44 |
| + voice-and-body baseline (enrollment) | 0.68 |
| + daily 5-second anchor | 0.74 |
| + 1 tagged readings per state | 0.80 |
| + 2 tagged readings per state | 0.82 |
| + 4 tagged readings per state | 0.83 |
| Voice only, + 2 tagged readings | 0.69 |
| Body only, + 2 tagged readings | 0.65 |

## Voluntary modes: how fast each learns the person

Week 1 enrollment, then the evening anchor and the optional tagged sentences of each mode. Accuracy on free voice notes, by week.

| Mode | Enrollment / day (week 1) | Anchors / week | Tagged sentences / week | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Light | 1 | 7 | 1 | 0.73 | 0.72 | 0.73 | 0.72 | 0.74 |
| Standard | 1 | 7 | 3 | 0.74 | 0.75 | 0.77 | 0.78 | 0.82 |
| Fast | 2 | 7 | 7 | 0.78 | 0.82 | 0.84 | 0.87 | 0.86 |
| Anchor less than daily (3 a week, 2 tagged) | 1 | 3 | 2 | 0.65 | 0.64 | 0.65 | 0.68 | 0.70 |

Estimated time a week (anchor 5 s, tagged sentence 10 s, question 3 s): light 0.9 min, standard 1.4 min, fast 2.5 min.

## The signature inside the engine

The full SoulEngine on two free voice notes a day: a generic speech model reads the voice channel, the bracelet the body; one question a day, answered truthfully. With the signature, the person's voice-and-body signature reads the voice channel instead (softened to the scale of the other channels) and the body is not counted twice: voice and body become one reading of the person's state. Scored on days 22-42, 4 seeds x 25 people not used to choose the settings.

| Engine | Most likely state right | Speaks | Right when it speaks |
| --- | --- | --- | --- |
| Public approach today: generic speech model + population body norms, nothing personal | 0.41 | 38% | 52% |
| Our engine without the signature: generic speech model + body, personal baseline, answers | 0.57 | 69% | 61% |
| + signature, enrollment and evening anchor only | 0.67 | 64% | 74% |
| + 3 tagged sentences a week (standard mode) | 0.75 | 72% | 81% |
| + answered voice notes also teach the signature (default) | 0.81 | 74% | 88% |
| Same, signature added to the generic voice reading instead of replacing it | 0.65 | 78% | 70% |
| Same, signature not softened (temperature 1) | 0.71 | 87% | 75% |
