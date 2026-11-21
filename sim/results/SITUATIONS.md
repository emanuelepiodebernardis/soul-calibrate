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
