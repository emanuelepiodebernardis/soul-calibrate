# 10 — Risks and failure modes

Author: Emanuele De Bernardis · Module: Risks · Concerns: [[02-enrollment]], [[03-session-anchor]], [[04-rolling-baseline]], [[05-active-questions]], [[06-personal-model]]

| Risk | Where | Effect | Mitigation | Experiment |
| --- | --- | --- | --- | --- |
| Users stop answering | active questions (bridge node) | the whole loop stops | budget, good timing, visible benefit of answering | E3, E15 |
| Measurement reactivity | repeated questions | with frequent sampling positive affect drops and answers habituate (Eisele et al., 2023) | budget, rotation, measure reactivity | E7 |
| Leading questions | proposed options | user picks what is suggested | always "none" and "other"; random order | E11 |
| Selection bias | questions only at anomalous moments | the model never learns "ordinary" | 5–10% random questions | E12 |
| Receptivity | King et al., 2024 | people who feel low answer less | model response probability; weight the data | E3 |
| Cold start | first days | wrong readings while trust forms | population model + normalisation; speak little at first | E1, E2 |
| Novelty during enrollment | first days | unrepresentative baseline | self-updating baseline; discard early days | E9 |
| Normalising chronic stress | rolling baseline | a long state becomes "normal" | long windows; separate drift from change; martingale trigger | E9, E18 |
| Physiological confounders | body signals | exercise, caffeine, sleep read as emotion | exclude movement; context in the model | E13 |
| Person leakage in evaluation | data splits | inflated results | split by person and time | E14 |
| User error in labels | self-report | noisy labels | as with glucose meters, user calibration is itself an error source → reliability weights | E2 |
| Alarm fatigue | prompts | people ignore prompts they find useless (72–99% of clinical alarms are false or non-actionable) | prompt precision as a metric; budget | E3 |
| Face | camera | weak signal + regulatory risk | optional, drop if no gain | E10 |
| Diagnostic drift of language | generated readings | wellbeing app sounding clinical | reading audit; banned vocabulary | E17 |
| Too many questions | generic model | in simulation the set is ambiguous at 76% of moments | personalise first; cap questions | [[18-simulation]] |
| Broken guarantee | personal memory changes probabilities | coverage 0.855 with random questions | ask at ambiguous moments; adaptive conformal thresholds per user | E22, [[20-recurring-situations]] |
| Life change | situation memory | old answers mislead when a situation changes meaning | one-tap corrections; situation-level drift from repeated corrections | E23, [[20-recurring-situations]] |
| Masking | words vs face or voice | the person says "fine" while the expression disagrees, or always looks serious | incongruence read against the person's baseline; ask, never assume | E21, [[21-text-face-incongruence]] |

Every risk has an experiment in [[16-experiments]].
