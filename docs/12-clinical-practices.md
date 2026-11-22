# 12 — What clinical practice already knows

Author: Emanuele De Bernardis · Module: Clinical practices · Strengthens: [[04-rolling-baseline]], [[05-active-questions]], [[07-fusion]], [[08-evaluation-soul-bench]], [[10-risks]]

**Original contribution (E. De Bernardis):** importing into a wellbeing product the methods clinicians and
digital-health researchers already use to follow individual people over time, while staying on the wellbeing
side of the line (no diagnosis).

## 1. Just-in-time adaptive interventions (JITAI)

- **What it is:** a design for giving the right support at the right time by adapting to a person's changing
  state and context (Nahum-Shani et al., 2018, *Annals of Behavioral Medicine*). Its elements: distal outcome,
  proximal outcome, decision points, intervention options, tailoring variables, decision rules.
- **For Nightlet:**

| JITAI element | In SOUL-Calibrate |
| --- | --- |
| Decision points | a voice note, the evening session, a deviation from baseline |
| Intervention options | speak, ask (2–3 options), stay quiet, haptic breathing pulse |
| Tailoring variables | conformal set, deviation size, likely receptivity, questions left today |
| Decision rules | the speak / ask / quiet rule of [[01-architecture]] |
| Proximal outcome | answer given; self-rated calm 10 minutes later; HRV during the pulse |
| Distal outcome | four-week wellbeing and retention |

## 2. Micro-randomised trials (MRT)

- **What it is:** at each decision point the option is randomised, so the short-term causal effect of each
  option can be estimated. HeartSteps (44 adults, 6 weeks, 5 decision points a day) found that a walking
  suggestion increased the next 30-minute step count by 14% (p = .06).
- **For Nightlet:** randomise "ask vs don't ask", "two options vs open question", "pulse vs no pulse", and
  measure the proximal outcomes above. This is how to test, causally, the claim that naming the feeling calms. → [[16-experiments]] (E15, E16)

## 3. Idiographic science: the person is the unit

- Fisher, Medaglia & Jeronimus (2018, *PNAS*) showed that group-level statistics often fail to describe the
  individuals in the group; only for ergodic processes do group inferences transfer to individuals.
- **For Nightlet:** the scientific case for personal baselines and per-user evaluation. → [[04-rolling-baseline]], [[08-evaluation-soul-bench]]

## 4. Early warning signals: useful as soft signals, not as alarms

- In bipolar disorder, rises in autocorrelation and variability of momentary states raised the probability
  of an upcoming transition from 32–36% to 46–48%, but their absence did not mean safety, and the signal varied
  a lot between people (Bos et al., 2022; 20 patients, 5 assessments a day for 4 months).
- A 2025 smartphone study of 29 patients over a year found several predictors, none meeting predefined clinical utility thresholds (Ludwig et al., *Journal of Affective Disorders*).
- **For Nightlet:** rising variability in a person's own series can raise the priority of a check-in, never
  trigger a warning about an episode. No episode prediction.

## 5. Routine outcome monitoring and "not on track"

- In psychotherapy, measuring progress and feeding it back to clinicians reduced deterioration and nearly
  doubled reliable improvement for clients predicted to do poorly (Lambert, Whipple & Kleinstäuber, 2018).
- **For Nightlet:** flag users for whom the model is "not on track" (its readings keep being corrected) → lower
  confidence, more questions, re-enrollment. Separately, a persistently low self-reported trend shows support resources, not a diagnosis. → [[15-labels-and-consent]]

## 6. Heart-rate-variability biofeedback

- Meta-analysis (Goessl, Curtiss & Hofmann, 2017; 24 studies, 484 participants): large reduction in self-reported stress and anxiety (between-group g = 0.83).
- **For Nightlet:** the bracelet's pulse can pace slow breathing; HRV during the pulse is the proximal outcome. → [[07-fusion]], designed in [[26-when-to-pulse]]

## 7. Naming emotions as a skill

- Emotion identification is an early skill in dialectical behaviour therapy (DBT); after DBT, alexithymia
  measures decreased and identified emotions increased in experience-sampling data (Costache et al., 2025).
- Emotional granularity grows with repeated experience sampling (Hoemann, Barrett & Quigley, 2021).
- **For Nightlet:** a vocabulary that grows: start with four broad states, then offer finer words to people
  who answer consistently (from "tense" to "worried", "frustrated", "pressured"). → [[25-coarse-to-fine-and-archetypes]]

## 8. Alarm fatigue

- Between 72% and 99% of clinical monitor alarms are false or not actionable, and staff respond to alarms in
  proportion to how reliable they find them.
- **For Nightlet:** every question is a small alarm. Track the share of unnecessary questions and cap them; a
  user who learns that questions are pointless will stop answering, and the loop stops. A pulse is an alarm on the
  wrist: same cap, and only when the reading is sure. → [[10-risks]], [[26-when-to-pulse]]

## Check

Every practice above maps to at least one experiment in [[16-experiments]] and one metric in [[08-evaluation-soul-bench]].
