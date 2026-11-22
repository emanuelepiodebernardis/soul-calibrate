# 16 — Experiment plan: where it works and where it does not

Author: Emanuele De Bernardis · Module: Experiments · Verifies: [[08-evaluation-soul-bench]] · Covers the risks of: [[10-risks]]

Each experiment states the result that would prove the idea wrong. E11–E18 close the gaps found by the knowledge graph and the clinical review.

| # | Experiment | Data | Hypothesis | Result that refutes it |
| --- | --- | --- | --- | --- |
| E1 | Person normalisation vs none | CREMA-D (by actor), WESAD | centring on the person raises within-person metrics | no gain with person-wise splits |
| E2 | Answers → accuracy curve | WESAD, then team data | 10–20 answers beat the generic model | hundreds of answers needed |
| E3 | Simulated active questions | WESAD / team data with known labels | uncertainty + context save questions vs random | no saving vs random (as in our simulation, [[18-simulation]]) |
| E4 | Conformal set as options | MSP-Podcast / CREMA-D | 90% coverage with sets of 2–3 states | sets too large to be questions |
| E5 | Session anchor | team data | deviation from the anchor correlates with self-report better than raw features | no difference |
| E6 | Voice vs words per person | team data | for some users voice adds information | voice adds nothing for anyone |
| E7 | Reactivity | consented cohort, 4 weeks | a question budget limits the drop in positive affect | same drop with and without budget |
| E8 | Calming effect of the question | cohort, A/B | choosing between two labels lowers reported activation afterwards | no effect |
| E9 | Drift | longitudinal data | the rolling baseline keeps performance over time | same decline as a fixed baseline |
| E10 | Face | opt-in cohort | the face adds over voice and words | no gain → drop the face |
| E11 | Leading questions | cohort, A/B | option order and number do not change answers beyond chance | answers follow the first option |
| E12 | Selection bias | cohort | anomaly-only questions miss "ordinary" states; adding 5–10% random questions fixes it | no difference |
| E13 | Physiological confounders | team data with accelerometer and context | excluding movement removes false "stress" readings | no change in false readings |
| E14 | Person leakage | all labelled data | random splits overstate accuracy vs person-and-time splits | no gap |
| E15 | Micro-randomised question trial | cohort | asking (vs not) improves self-rated calm 10 minutes later | no proximal effect |
| E16 | Micro-randomised haptic pulse | cohort with bracelet | a paced pulse raises HRV during the pulse | no HRV change |
| E17 | Reading audit | generated readings | readings pass the batteries of [[14-reading-audit]] | any battery fails |
| E18 | Martingale drift trigger | longitudinal data with known changes | the trigger fires after real changes and rarely otherwise | missed changes or frequent false triggers |
| E19 | Cohort transfer | private cohort + new users | cohort answers improve readings for users who are never asked | no gain for new users ([[19-private-cohort-pilot]]) |
| E20 | Recurring situations | cohort, calibration week | after one answer, later readings of the same situation improve vs a micro-randomised no-question control | no gain on the same situation ([[20-recurring-situations]]) |
| E21 | Words vs expression | public multimodal sets + cohort | incongruent moments are where generic models fail and where one question gains most | no gap between congruent and incongruent moments ([[21-text-face-incongruence]]) |
| E22 | Coverage after personalization | cohort | per-user coverage stays near 90% with adaptive conformal thresholds | coverage below 85% for many users ([[20-recurring-situations]]) |
| E23 | Life change | cohort, follow-up | one-tap corrections recover changed situations faster without hurting the others | no faster recovery ([[20-recurring-situations]]) |
| E24 | Personalization speed | cohort, randomised presets | Light, Standard and Fast reach the same accuracy, Fast sooner | no difference in speed, or a lower ceiling for Light ([[23-question-budget]]) |
| E25 | Burden by preset | cohort | answer rate and drop-out stay acceptable for Standard and Fast | drop-out rises sharply with the budget ([[23-question-budget]]) |
| E26 | Free notes | cohort | notes replace questions at the same accuracy | notes add nothing ([[23-question-budget]]) |
| E27 | Four vs eight states | cohort | agreement with self-report stays useful with eight states, and wrong readings are mostly neighbours | no gain from the finer vocabulary ([[24-what-precise-means]]) |
| E28 | Answers needed by granularity | cohort | eight states need about 50% more answers with wide questions | eight states never reach the four-state level ([[24-what-precise-means]]) |
| E29 | Level of detail per reading | cohort | showing the main state until the fine one is sure keeps readings right from the first days without slowing learning | no gain in early shown precision ([[25-coarse-to-fine-and-archetypes]]) |
| E30 | Archetypes | cohort, new users | matching a new person to an archetype beats one head pooled over the cohort in the first week (synthetic: the pooled head already gives +3 to +5 points, archetypes add nothing) | no gain over the pooled head, or worse for people who fit no archetype ([[25-coarse-to-fine-and-archetypes]]) |
| E31 | First check on real voice | public multi-speaker emotion speech, pretrained speech model (PyTorch) | a per-speaker baseline and a few answers per speaker beat the generic model, scored on held-out recordings of each speaker | no gain over the generic model on real audio ([[00-problem]], [[06-personal-model]]) |

## Before the interview (done)

A synthetic simulation of E1-like, E2-like, E3-like, E4-like, E9-like, E19-like and E20-like experiments. → [[18-simulation]]

## First 90 days

- Days 1–30: E1, E2, E4, E14 on public and team data; claims ledger in place.
- Days 31–60: E3, E5, E6, E13, E17; first partner model through the same harness.
- Days 61–90: private cohort pilot with E7, E8, E11, E12, E15, E16, E18, E19.
