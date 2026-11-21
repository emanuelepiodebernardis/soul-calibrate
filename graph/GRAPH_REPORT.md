# Graph Report - graph-src  (2026-11-21)

## Corpus Check
- Corpus is ~13,710 words - fits in a single context window. You may not need a graph.

## Summary
- 326 nodes · 830 edges · 8 communities
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 68 edges (avg confidence: 0.89)
- Token cost: 225,771 input · 0 output

## Community Hubs (Navigation)
- Problem and evidence
- Simulation code
- Authorship, prior work and governance
- Risks and failure modes
- Labels, question budget and consent
- Decision and active questions
- Clinical practices
- Analogous systems

## God Nodes (most connected - your core abstractions)
1. `References` - 52 edges
2. `05 Active questions` - 35 edges
3. `12 — What clinical practice already knows` - 33 edges
4. `16 — Experiment plan: where it works and where it does not` - 32 edges
5. `06 Personal model` - 28 edges
6. `10 — Risks and failure modes` - 28 edges
7. `13 — Ideas reused from the author's prior work` - 28 edges
8. `02 Enrollment (entry calibration)` - 25 edges
9. `04 Rolling personal baseline` - 25 edges
10. `08 Evaluation: SOUL-Bench` - 25 edges

## Surprising Connections (you probably didn't know these)
- `exp_ladder()` --implements--> `A. Personalization ladder (0.578 -> 0.605 -> 0.689)`  [INFERRED]
  sim/soul_calibrate/experiments.py → docs/18-simulation.md
- `exp_active()` --implements--> `B. Ambiguous vs random question moments (no clear difference)`  [INFERRED]
  sim/soul_calibrate/experiments.py → docs/18-simulation.md
- `exp_conformal()` --implements--> `C. Conformal sets (coverage 0.905; ambiguous at 76% of moments)`  [INFERRED]
  sim/soul_calibrate/experiments.py → docs/18-simulation.md
- `exp_drift()` --implements--> `D. Step change in signals (fixed 0.541, rolling 0.581)`  [INFERRED]
  sim/soul_calibrate/experiments.py → docs/18-simulation.md
- `exp_cohort()` --implements--> `E. Cohort transfer (0.550 -> 0.590 with 50 users; full loop 0.652)`  [INFERRED]
  sim/soul_calibrate/experiments.py → docs/18-simulation.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **SOUL-Calibrate closed personal loop** — docs_02_enrollment_entry_calibration, docs_03_session_anchor_session_anchor, docs_04_rolling_baseline_rolling_personal_baseline, docs_06_personal_model_personal_head, docs_01_architecture_conformal_decision, docs_05_active_questions_active_questions, docs_01_architecture_closed_loop_update [EXTRACTED 1.00]
- **Conformal uncertainty handling for questions** — docs_01_architecture_conformal_decision, docs_05_active_questions_conformal_prediction_options, docs_05_active_questions_class_conditional_calibration, docs_05_active_questions_selective_conformal_risk_control [INFERRED 0.85]
- **Three sub-problems and their modules** — docs_00_problem_cold_start, docs_00_problem_moving_reference, docs_00_problem_missing_labels, docs_02_enrollment_entry_calibration, docs_04_rolling_baseline_rolling_personal_baseline, docs_05_active_questions_active_questions [EXTRACTED 1.00]
- **Reading audit test batteries** — docs_14_reading_audit_reading_audit, docs_14_reading_audit_persona_invariance, docs_14_reading_audit_uncertainty_honesty, docs_14_reading_audit_non_diagnostic_language, docs_14_reading_audit_sycophancy, docs_14_reading_audit_separation_of_layers, docs_14_reading_audit_safety_routing [EXTRACTED 1.00]
- **Private cohort: consent level 2 -> pilot -> E19 -> cohort transfer evidence** — docs_15_labels_and_consent_consent_level_2_research_cohort, docs_19_private_cohort_pilot_private_cohort_pilot, docs_16_experiments_e19, docs_18_simulation_cohort_transfer, sim_results_results_table_e_cohort_transfer, docs_19_private_cohort_pilot_held_out_users [INFERRED 0.85]
- **Evidence-based governance (claims ledger, provenance, evidence-before-done)** — docs_17_roadmap_and_governance_claims_ledger, docs_17_roadmap_and_governance_provenance_classes, docs_13_ideas_from_prior_work_claim_evidence_map, docs_13_ideas_from_prior_work_evidence_before_done, docs_17_roadmap_and_governance_numbered_stages, docs_17_roadmap_and_governance_decision_log [INFERRED 0.85]

## Communities (8 total, 0 thin omitted)

### Community 0 - "Problem and evidence"
Cohesion: 0.05
Nodes (56): SOUL-Calibrate (original contribution), Barrett et al. 2019 (faces not reliable emotion read-outs), Cold start, 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Moving reference (people change over weeks) (+48 more)

### Community 1 - "Simulation code"
Cohesion: 0.09
Nodes (29): main(), style(), summarise(), calibrate(), coverage(), decide(), _quantile(), make_population() (+21 more)

### Community 2 - "Authorship, prior work and governance"
Cohesion: 0.07
Nodes (26): Transfer of clinical methods, MIT License, Private cohort pilot, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study) (+18 more)

### Community 3 - "Risks and failure modes"
Cohesion: 0.10
Nodes (28): 10 — Risks and failure modes, 16 — Experiment plan: where it works and where it does not, E1 Person normalisation vs none, E10 Face, E11 Leading questions, E12 Selection bias, E13 Physiological confounders, E14 Person leakage (+20 more)

### Community 4 - "Labels, question budget and consent"
Cohesion: 0.09
Nodes (24): Tazarv et al. (2023) stress detector with ask-when agent, Consent level 2 — research cohort, 15 — Label quality and consent, GDPR, Nightlet's disclaimer (user is best source), B. Ambiguous vs random question moments (no clear difference), E. Cohort transfer (0.550 -> 0.590 with 50 users; full loop 0.652), C. Conformal sets (coverage 0.905; ambiguous at 76% of moments) (+16 more)

### Community 5 - "Decision and active questions"
Cohesion: 0.10
Nodes (18): Emanuele De Bernardis, SOUL-Bench (original contribution), Missing labels, Affect labeling (Lieberman et al., 2007), Prompt as clinical alarm (alarm fatigue), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+10 more)

### Community 6 - "Clinical practices"
Cohesion: 0.18
Nodes (10): 12 — What clinical practice already knows, HeartSteps trial, Bos et al. (2022) early warning signals in bipolar disorder, Costache et al. (2025) DBT, alexithymia and emotion awareness, Goessl, Curtiss, Hofmann (2017) HRV biofeedback meta-analysis, Hoemann, Barrett, Quigley (2021) Emotional Granularity Increases With Ambulatory Assessment, Klasnja et al. (2019) HeartSteps micro-randomized trial, Lambert, Whipple, Kleinstäuber (2018) Routine Outcome Monitoring meta-analysis (+2 more)

### Community 7 - "Analogous systems"
Cohesion: 0.22
Nodes (12): Dexcom G6 (first factory-calibrated real-time CGM), 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy, Speaker recognition enrollment, Abdel-Ghaffar et al. (2025) Fitbit Body Response, Denham (2020) factory-calibrated CGM first-day performance (+4 more)

## Knowledge Gaps
- **23 isolated node(s):** `MIT License`, `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Triantafyllopoulos et al. 2022 speaker enrolment`, `openSMILE eGeMAPS features (88) computed on phone`, `Signal quality check (HNR, voice detected)` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 56 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `18 — Simulation: what the method does on synthetic users` connect `Labels, question budget and consent` to `Problem and evidence`, `Authorship, prior work and governance`, `Risks and failure modes`, `Decision and active questions`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `References` (e.g. with `AuditEngine (RinDig)` and `icm-architect (RinDig)`) actually correct?**
  _`References` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MIT License`, `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Triantafyllopoulos et al. 2022 speaker enrolment` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Problem and evidence` be split into smaller, more focused modules?**
  _Cohesion score 0.05052631578947368 - nodes in this community are weakly interconnected._
- **Why does `References` connect `Problem and evidence` to `Authorship, prior work and governance`, `Risks and failure modes`, `Labels, question budget and consent`, `Decision and active questions`, `Clinical practices`, `Analogous systems`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Should `Simulation code` be split into smaller, more focused modules?**
  _Cohesion score 0.08780903665814152 - nodes in this community are weakly interconnected._
- **Why does `16 — Experiment plan: where it works and where it does not` connect `Risks and failure modes` to `Problem and evidence`, `Authorship, prior work and governance`, `Labels, question budget and consent`, `Decision and active questions`, `Clinical practices`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._