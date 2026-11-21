# 11 — Analogous systems in other fields

Author: Emanuele De Bernardis · Module: Analogues · Inspires: [[02-enrollment]], [[04-rolling-baseline]], [[05-active-questions]], [[09-privacy-and-regulation]]

**Lesson common to all of them:** start with personal calibration, then work to need less of it.

## Continuous glucose monitors (CGM): from user calibration to factory calibration

- Early CGMs required several finger-stick calibrations a day. Simulating one calibration factor for all
  sensors gave a mean absolute relative difference of 13.4% versus 12.7% with multiple user calibrations.
- Dexcom G6 (2018) was the first real-time factory-calibrated CGM; removing user calibration also removed an error source.
- In critically ill patients factory calibration may not suffice and per-patient calibration is recommended (Ramesh et al., 2025).
- **Lesson:** the user's label is useful but noisy; reduce the need for it over time, keep it for people who deviate.

## Brain–computer interfaces (BCI)

- Each user goes through a long, tedious calibration session to build a personal classifier.
- The field reduces it with cross-subject and cross-session transfer learning and semi-supervised learning.
- **Lesson:** population transfer + a little personal data; the session anchor is cross-session calibration. → [[03-session-anchor]]

## Fitbit Body Response (Google)

- Continuous on-wrist EDA; learns the wearer in the first month; on sudden changes invites the user to reflect on what is happening.
- Acknowledges that the same signals appear with positive excitement.
- **Lesson:** "deviation → question" already exists in a shipped product, without voice or words.

## Wearable seizure detection (Empatica Embrace)

- FDA-cleared wrist device using EDA and motion; the clearance reports a false alarm rate of 0.94 per 24 hours.
- **Lesson:** a prompting wearable states its false-alarm rate as a headline metric. Nightlet should state its
  unnecessary-question rate the same way. → [[08-evaluation-soul-bench]]

## Speaker recognition enrollment

A few phrases recorded at setup create a voice profile, then it updates implicitly. → [[02-enrollment]]

## Gboard: federated learning with differential privacy

Models trained on phones without moving raw data, with formal privacy guarantees and user controls. → [[09-privacy-and-regulation]]

## Tazarv et al. (2023)

The closest system to the proposed loop: a stress detector plus an agent that decides when to ask. → [[05-active-questions]]
