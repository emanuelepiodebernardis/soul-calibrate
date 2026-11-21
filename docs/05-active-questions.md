# 05 — Active questions ("tense or angry?")

Author: Emanuele De Bernardis · Module: Active questions · Part of: [[01-architecture]] · Produces labels for: [[06-personal-model]]

**Original contribution (E. De Bernardis):** when the signals move away from the person's baseline and the
model is unsure, Nightlet does not guess. It offers the most plausible states and lets the user choose, and
the first answers come from the user so that every state is learned per person.

## What it does

The options are 2–3 plausible states, always with "none of these" and "something else".

## When to ask

- **Just-in-time adaptive intervention (JITAI) framework** (Nahum-Shani et al., 2018): define decision points,
  options, tailoring variables, decision rules, proximal and distal outcomes. The question is one option at
  each decision point. → [[12-clinical-practices]]
- **Tazarv et al. (2023):** an agent that chooses when to ask using model uncertainty, time since the last
  question, the user's response rate at that hour and time of day needed up to 88% fewer questions than random
  timing and 32% fewer than uncertainty alone, on the participant with most labels.
- **Receptivity and affect are linked** (King et al., 2024): asking at the wrong moment biases the data.
- **Our simulation is more modest:** choosing ambiguous moments did not beat random moments clearly. The
  claim must be tested on real people. → [[18-simulation]]

## What to ask (the options)

- **Conformal prediction** returns the set of plausible emotions with a coverage guarantee; set size is a reliable
  indicator of uncertainty (Roohi et al., 2025). The conformal set becomes the options of the question.
- Plain conformal favours "neutral" and under-covers rare states → class-conditional (per-state) calibration.
- **Selective conformal risk control** (2025): first decide whether to answer, then guarantee the error on accepted cases.

## Why the question itself helps

- **Affect labeling** (Lieberman et al., 2007): naming the emotion reduces amygdala activity; participants chose
  between two words, exactly the two-option format.
- **Emotional granularity** grows with experience sampling, more with more answers per day (Hoemann, Barrett & Quigley, 2021).
- **Clinical skills training** teaches identifying and naming emotions as a first step of regulation (DBT). → [[12-clinical-practices]]
- Collecting labels is therefore also a wellbeing function, consistent with "understood, not optimized".

## Rules

- A hard **question budget** per day and a minimum gap between questions. In the simulation, with a generic model the
  conformal set is ambiguous at 76% of moments: without a budget and without personalization Nightlet would ask almost always. → [[18-simulation]]
- 5–10% of questions at random ordinary moments, or the model only learns unusual moments (selection bias).
- Hypotheses come from words and voice; the body sets intensity. → [[07-fusion]]
- Never suggest a strong emotion without a neutral alternative; randomise option order (leading questions). → [[10-risks]]
- Treat the prompt like a clinical alarm: track the share of unnecessary prompts (alarm fatigue). → [[12-clinical-practices]]

## Check

Questions per day, answer rate, share of "none of these", per-user and per-state conformal coverage, accuracy
gain per question. → [[08-evaluation-soul-bench]], [[16-experiments]] (E3, E4, E11, E12, E15)
