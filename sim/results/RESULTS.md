# Simulation results

Synthetic users, 5 seeds, mean ± standard deviation across seeds. Four states (calm, energized, tense, low); chance is 0.25. These numbers describe the method on simulated data, not real users.

## A. Personalization ladder (accuracy on later moments)

| Model | Accuracy |
| --- | --- |
| Generic model, raw signals | 0.578 ± 0.019 |
| Personal baseline, no answers | 0.605 ± 0.023 |
| Personal head, 5 answers | 0.625 ± 0.034 |
| Personal head, 10 answers | 0.622 ± 0.024 |
| Personal head, 20 answers | 0.656 ± 0.025 |
| Personal head, 40 answers | 0.689 ± 0.016 |

## B. Active versus random questions

| Budget | Random moments | Ambiguous moments |
| --- | --- | --- |
| 5 | 0.618 ± 0.033 | 0.618 ± 0.016 |
| 10 | 0.626 ± 0.032 | 0.620 ± 0.010 |
| 20 | 0.651 ± 0.025 | 0.650 ± 0.015 |

## C. Conformal sets (target coverage 0.90)

| Variant | Coverage | Worst state | Mean set size | Speaks | Asks | Quiet | Accuracy when speaking |
| --- | --- | --- | --- | --- | --- | --- | --- |
| global | 0.902 ± 0.007 | 0.880 ± 0.010 | 2.541 ± 0.033 | 0.066 ± 0.004 | 0.763 ± 0.016 | 0.171 ± 0.013 | 0.762 ± 0.028 |
| per_state | 0.905 ± 0.011 | 0.876 ± 0.023 | 2.579 ± 0.037 | 0.062 ± 0.007 | 0.762 ± 0.011 | 0.176 ± 0.014 | 0.762 ± 0.029 |

## D. Drift: a step change in a user's signals

| Baseline | Accuracy after the change |
| --- | --- |
| Fixed at enrollment | 0.541 ± 0.028 |
| Rolling | 0.581 ± 0.020 |
| Rolling, no change (reference) | 0.584 ± 0.020 |

## E. From today's approach to SOUL-Calibrate (users who are never asked)

The shared model is trained on public data whose mapping from affect to signals differs from real users (domain shift). A private cohort answers 20 questions each; their answers retrain the shared model. Accuracy is measured on new users who answer nothing, except in the last row.

| Setting | Accuracy |
| --- | --- |
| Today: generic model on public data | 0.550 ± 0.036 |
| + personal baseline (no labels) | 0.545 ± 0.046 |
| + cohort of 10 users | 0.571 ± 0.039 |
| + cohort of 25 users | 0.576 ± 0.038 |
| + cohort of 50 users | 0.590 ± 0.039 |
| Full loop: the new user also answers 20 questions | 0.652 ± 0.023 |
