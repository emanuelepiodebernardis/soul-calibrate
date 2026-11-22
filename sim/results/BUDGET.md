# How many questions a day?
Synthetic people, 5 seeds, 60 people each; 6 recurring situations; 4 readings a day unless stated; closed questions; a calibration period with questions, then 5 test days without questions.
## A. Budget per day during a 7-day calibration week
| Setting | Questions per person | Accuracy, test days | Same situation after an answer | Speaks | Accuracy when speaking | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 0.25/day, no questions | 0.0 | 0.504 | nan | 7% | 0.818 | 0.918 |
| 0.25/day, random moments | 1.0 | 0.587 | 0.904 | 29% | 0.862 | 0.887 |
| 0.25/day, ambiguous moments | 1.0 | 0.581 | 0.924 | 28% | 0.851 | 0.881 |
| 0.25/day, ambiguous and not yet known | 1.0 | 0.582 | 0.922 | 28% | 0.848 | 0.881 |
| 0.5/day, random moments | 3.0 | 0.696 | 0.874 | 55% | 0.846 | 0.859 |
| 0.5/day, ambiguous moments | 2.8 | 0.728 | 0.879 | 51% | 0.899 | 0.896 |
| 0.5/day, ambiguous and not yet known | 2.6 | 0.746 | 0.864 | 44% | 0.905 | 0.909 |
| 1/day, random moments | 7.0 | 0.751 | 0.840 | 73% | 0.845 | 0.855 |
| 1/day, ambiguous moments | 6.0 | 0.863 | 0.892 | 72% | 0.938 | 0.930 |
| 1/day, ambiguous and not yet known | 4.4 | 0.816 | 0.853 | 55% | 0.941 | 0.941 |
| 2/day, random moments | 14.0 | 0.793 | 0.825 | 86% | 0.845 | 0.848 |
| 2/day, ambiguous moments | 8.3 | 0.910 | 0.914 | 81% | 0.955 | 0.948 |
| 2/day, ambiguous and not yet known | 4.8 | 0.840 | 0.860 | 60% | 0.941 | 0.946 |
| 3/day, random moments | 21.0 | 0.797 | 0.819 | 91% | 0.833 | 0.835 |
| 3/day, ambiguous moments | 9.0 | 0.917 | 0.920 | 83% | 0.963 | 0.953 |
| 3/day, ambiguous and not yet known | 4.9 | 0.838 | 0.856 | 60% | 0.934 | 0.938 |
| 4/day, random moments | 28.0 | 0.810 | 0.822 | 93% | 0.842 | 0.841 |
| 4/day, ambiguous moments | 8.9 | 0.920 | 0.920 | 84% | 0.961 | 0.954 |
| 4/day, ambiguous and not yet known | 4.9 | 0.841 | 0.851 | 60% | 0.936 | 0.943 |

## B. Spreading questions over the day (ambiguous moments)

| Setting | Questions per person | Accuracy, test days | Same situation after an answer | Speaks | Accuracy when speaking | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 1/day, first ambiguous moments | 6.0 | 0.863 | 0.892 | 72% | 0.938 | 0.930 |
| 1/day, spread | 5.1 | 0.829 | 0.885 | 68% | 0.924 | 0.914 |
| 2/day, first ambiguous moments | 8.3 | 0.910 | 0.914 | 81% | 0.955 | 0.948 |
| 2/day, spread | 8.0 | 0.906 | 0.907 | 80% | 0.958 | 0.954 |

## C. The state changes more often: 8 readings a day

| Setting | Questions per person | Accuracy, test days | Same situation after an answer | Speaks | Accuracy when speaking | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 1/day, first ambiguous moments | 6.5 | 0.875 | 0.898 | 74% | 0.945 | 0.938 |
| 1/day, random moments | 7.0 | 0.744 | 0.833 | 72% | 0.841 | 0.847 |
| 1/day, spread | 5.8 | 0.850 | 0.890 | 71% | 0.934 | 0.927 |
| 2/day, first ambiguous moments | 10.2 | 0.935 | 0.932 | 86% | 0.971 | 0.963 |
| 2/day, random moments | 14.0 | 0.786 | 0.823 | 86% | 0.841 | 0.845 |
| 2/day, spread | 9.7 | 0.931 | 0.930 | 84% | 0.973 | 0.961 |
| no questions | 0.0 | 0.499 | nan | 7% | 0.802 | 0.911 |

## D. Fewer questions over a longer calibration (ambiguous moments)

| Setting | Questions per person | Accuracy, test days | Same situation after an answer | Speaks | Accuracy when speaking | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 7d, 1/day | 6.0 | 0.863 | 0.892 | 72% | 0.938 | 0.930 |
| 14d, 0.5/day | 5.9 | 0.866 | 0.895 | 73% | 0.943 | 0.930 |
| 28d, 0.25/day | 6.0 | 0.861 | 0.878 | 70% | 0.948 | 0.939 |
| 14d, 1/day | 9.9 | 0.924 | 0.916 | 85% | 0.964 | 0.956 |
