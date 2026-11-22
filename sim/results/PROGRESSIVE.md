# Coarse to fine

Synthetic people living eight states (four main states and an intermediate one between each pair), 5 seeds, 60 people each; 6 recurring situations, 4 readings a day; questions allowed for 28 days at ambiguous moments with closed options; every reading scored before learning.

- **Shown precision:** the reading is right at the level of detail shown (a main state counts as right for an intermediate state next to it).
- **Fine precision:** the model's best guess among the eight states, shown or not.

| Budget | Approach | Shown, day 3 | Shown, day 7 | Shown, day 14 | Shown, day 28 | Fine, day 14 | Fine, day 28 | Fine readings shown, day 28 | Mean switch day | Questions by day 28 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1/day | Eight states from day one | 0.55 | 0.75 | 0.85 | 0.95 | 0.85 | 0.95 | 100% | – | 19.5 |
| 1/day | Four main states, switch to eight on day 7 | 0.75 | 0.82 | 0.78 | 0.91 | 0.78 | 0.91 | 100% after the switch | 7.0 | 21.4 |
| 1/day | Four main states, switch when readings are confident | 0.75 | 0.75 | 0.75 | 0.88 | 0.63 | 0.87 | 100% after the switch | 10.6 | 22.5 |
| 1/day | Level of detail chosen per reading | 0.75 | 0.85 | 0.91 | 0.96 | 0.85 | 0.95 | 86% | – | 19.5 |
| 2/day | Eight states from day one | 0.67 | 0.85 | 0.92 | 0.97 | 0.92 | 0.97 | 100% | – | 23.7 |
| 2/day | Four main states, switch to eight on day 7 | 0.80 | 0.89 | 0.85 | 0.94 | 0.85 | 0.94 | 100% after the switch | 7.0 | 28.5 |
| 2/day | Four main states, switch when readings are confident | 0.80 | 0.76 | 0.84 | 0.95 | 0.81 | 0.95 | 100% after the switch | 7.0 | 28.7 |
| 2/day | Level of detail chosen per reading | 0.81 | 0.91 | 0.94 | 0.98 | 0.92 | 0.97 | 91% | – | 23.7 |
