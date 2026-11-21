# Recurring situations: does a question improve the next reading of the same situation?

Synthetic people, 5 seeds, 60 people per seed, mean ± standard deviation across seeds. Each person has 6 recurring situations; 4 readings a day; a calibration week of 7 days with at most one question a day, then 5 test days without questions. Four states, chance 0.25. Policies share the same people and the same moments: only the questions differ.

## A. Policies and question types (situations always bring their usual state)

| Policy | Questions per person | Accuracy in the test days | Same situation, after the answer | Same moments, no questions | Other situations | Same moments, no questions |
| --- | --- | --- | --- | --- | --- | --- |
| No questions (today) | 0.0 | 0.504 ± 0.006 | – | – | 0.504 ± 0.011 | 0.504 ± 0.011 |
| Random moment, closed question | 7.0 | 0.751 ± 0.020 | 0.840 ± 0.016 | 0.510 ± 0.014 | 0.494 ± 0.027 | 0.493 ± 0.016 |
| Ambiguous moment, closed question | 6.0 | 0.863 ± 0.012 | 0.892 ± 0.012 | 0.497 ± 0.016 | 0.620 ± 0.034 | 0.519 ± 0.011 |
| Ambiguous and not yet known, closed | 4.4 | 0.816 ± 0.025 | 0.853 ± 0.019 | 0.499 ± 0.012 | 0.648 ± 0.047 | 0.514 ± 0.014 |
| Random moment, open question | 7.0 | 0.751 ± 0.019 | 0.810 ± 0.016 | 0.504 ± 0.021 | 0.519 ± 0.030 | 0.504 ± 0.011 |
| Ambiguous moment, open question | 6.4 | 0.794 ± 0.027 | 0.838 ± 0.016 | 0.499 ± 0.015 | 0.578 ± 0.037 | 0.516 ± 0.017 |
| Ambiguous and not yet known, open | 4.4 | 0.756 ± 0.016 | 0.784 ± 0.018 | 0.500 ± 0.013 | 0.621 ± 0.033 | 0.513 ± 0.014 |

## B. The field narrows: mean size of the set of plausible states, by day

| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| No questions (today) | 2.77 | 2.76 | 2.71 | 2.78 | 2.79 | 2.80 | 2.77 | 2.73 | 2.80 | 2.77 | 2.76 | 2.76 |
| Random moment, closed question | 2.55 | 2.11 | 1.80 | 1.63 | 1.51 | 1.42 | 1.36 | 1.32 | 1.35 | 1.37 | 1.31 | 1.32 |
| Ambiguous moment, closed question | 2.38 | 2.03 | 1.78 | 1.65 | 1.54 | 1.44 | 1.36 | 1.31 | 1.36 | 1.35 | 1.35 | 1.36 |

## C. How stable the situations are (closed questions)

Stability = probability that a situation brings its usual state; otherwise it brings a neighbouring one.

| Stability | No questions | Random moment | Ambiguous moment | Ambiguous and not yet known |
| --- | --- | --- | --- | --- |
| 1.0 | 0.504 ± 0.006 | 0.751 ± 0.020 | 0.863 ± 0.012 | 0.816 ± 0.025 |
| 0.8 | 0.512 ± 0.009 | 0.681 ± 0.031 | 0.784 ± 0.013 | 0.770 ± 0.026 |
| 0.6 | 0.509 ± 0.019 | 0.656 ± 0.047 | 0.742 ± 0.019 | 0.728 ± 0.026 |

## D. Nightlet's data constraint: a shared model trained on public data only (closed questions)

User voice and face data are never used for training, so the shared model learns from public data. Public shift = how differently public data map states onto signals (0 = same as the product's users).

| Public shift | No questions (today) | Random moment | Ambiguous moment | Gain of ambiguous over today |
| --- | --- | --- | --- | --- |
| 0.0 | 0.504 ± 0.006 | 0.751 ± 0.020 | 0.863 ± 0.012 | +0.359 |
| 0.1 | 0.442 ± 0.031 | 0.728 ± 0.016 | 0.822 ± 0.032 | +0.381 |
| 0.2 | 0.369 ± 0.038 | 0.706 ± 0.023 | 0.764 ± 0.015 | +0.395 |

## F. Is the 90% guarantee kept after personalization? (closed questions, test days)

The conformal thresholds are calibrated on the population; the personal memory changes the probabilities, so coverage must be checked again. Adaptive conformal inference (ACI) shifts each person's thresholds with their own answers: a miss widens the sets, a hit narrows them.

| Policy | ACI step | Coverage (target 0.90) | Share of readings that speak | Accuracy when speaking | Accuracy |
| --- | --- | --- | --- | --- | --- |
| No questions (today) | 0.0 | 0.918 ± 0.018 | 0.075 ± 0.010 | 0.818 ± 0.052 | 0.504 ± 0.006 |
| Random moment, closed question | 0.0 | 0.855 ± 0.021 | 0.734 ± 0.021 | 0.845 ± 0.023 | 0.751 ± 0.020 |
| Ambiguous moment, closed question | 0.0 | 0.930 ± 0.011 | 0.718 ± 0.015 | 0.938 ± 0.009 | 0.863 ± 0.012 |
| Random moment, closed question | 0.1 | 0.881 ± 0.020 | 0.627 ± 0.029 | 0.852 ± 0.038 | 0.746 ± 0.021 |
| Ambiguous moment, closed question | 0.1 | 0.939 ± 0.013 | 0.629 ± 0.030 | 0.938 ± 0.023 | 0.824 ± 0.024 |

## E. A life change: two of six situations change their usual state after the calibration week

Questions stay allowed (closed, ambiguous moments, at most one a day) for 14 more days. Visibility = how much the signal moves with the new state (1 = fully; 0.5 = halfway, so old answers mislead). Interactions = questions plus user corrections over the 21 days.

Visibility 1.0:

| Memory variant | Changed situations, week 1 | Changed situations, week 2 | Unchanged situations | Interactions per person |
| --- | --- | --- | --- | --- |
| answers never fade | 0.738 ± 0.032 | 0.883 ± 0.024 | 0.914 ± 0.022 | 13.3 |
| + check-in questions (15% of days) | 0.740 ± 0.029 | 0.879 ± 0.024 | 0.914 ± 0.016 | 14.5 |
| + user corrections (30% of wrong readings) | 0.773 ± 0.038 | 0.926 ± 0.021 | 0.936 ± 0.011 | 14.3 |
| + answers fade (half-life 7 days) | 0.737 ± 0.027 | 0.885 ± 0.012 | 0.887 ± 0.019 | 17.2 |
| + contradicted answers weaken | 0.706 ± 0.017 | 0.840 ± 0.007 | 0.849 ± 0.025 | 16.2 |

Visibility 0.5:

| Memory variant | Changed situations, week 1 | Changed situations, week 2 | Unchanged situations | Interactions per person |
| --- | --- | --- | --- | --- |
| answers never fade | 0.451 ± 0.030 | 0.649 ± 0.042 | 0.880 ± 0.026 | 15.0 |
| + check-in questions (15% of days) | 0.460 ± 0.033 | 0.632 ± 0.039 | 0.886 ± 0.019 | 15.6 |
| + user corrections (30% of wrong readings) | 0.487 ± 0.034 | 0.711 ± 0.019 | 0.902 ± 0.016 | 17.2 |
| + answers fade (half-life 7 days) | 0.485 ± 0.032 | 0.663 ± 0.017 | 0.853 ± 0.025 | 18.1 |
| + contradicted answers weaken | 0.474 ± 0.045 | 0.600 ± 0.036 | 0.798 ± 0.026 | 16.8 |

