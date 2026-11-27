# 17 — Roadmap and governance

Author: Emanuele De Bernardis · Module: Roadmap · Organises: [[16-experiments]], [[08-evaluation-soul-bench]], [[13-ideas-from-prior-work]]

## Principles

1. **Numbered stages, each closed by a check.** A stage is done when its check has produced a saved result,
   not when someone says it is done. The folder structure of this repository follows the same idea: numbered
   modules, each ending with a "Check" section, readable without prior context. (Inspired in part by the
   folder-as-architecture approach of [icm-architect](https://github.com/RinDig/icm-architect).)
2. **Claims ledger.** Every number in any report points to an evidence file, its SHA-256 and a provenance class:
   `MEASURED_REAL_USERS`, `MEASURED_PUBLIC_DATA`, `SIMULATED`, `PLANNED_NOT_MEASURED`. → [[13-ideas-from-prior-work]]
3. **Decision log.** Each choice of model, threshold or question budget is written down with the evidence that supported it.
4. **Same harness for everyone.** In-house and partner models go through SOUL-Bench unchanged.

## Stages

| Stage | Goal | Exit check |
| --- | --- | --- |
| 0 — Foundations | labels, consent levels, feature parity | parity test passes; consent levels approved; label form fixed |
| 1 — SOUL-Bench on public data | ladder B0–B6, conformal calibration, real voice (E31) | E1, E2, E4, E14, E31 results in the ledger |
| 2 — Team dogfooding | the loop runs on the team's phones, with enrollment, daily anchor and tagged readings, and the understanding layer's prompts ([[30-understanding-layer]]) | E3, E5, E6, E13, E17 results; question budget set; signatures for every team member |
| 3 — Private cohort pilot | consented group, micro-randomised; pulse, voice check-ins, signatures and the understanding layer (lens, body mirror, bridge to people) | E7, E8, E11, E12, E15, E16, E18, E19, E32–E40 results |
| 4 — Product | speak / ask / quiet in production | prompt precision, answer rate and coverage monitored weekly |

## Weekly review

- Answer rate (bridge node of the system), unnecessary-question rate, per-state coverage, drift triggers.
- Users "not on track" (readings repeatedly corrected). → [[12-clinical-practices]]
- New claims added to the ledger and their provenance.

## Check

A person who opens this repository without context can say which stage the project is in and what evidence
closed the previous one.
