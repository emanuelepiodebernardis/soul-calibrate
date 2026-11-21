# Graph Report - soul-calibrate  (2026-11-21)

## Corpus Check
- Corpus is ~32,697 words - fits in a single context window. You may not need a graph.

## Summary
- 680 nodes · 1898 edges · 27 communities (21 shown, 6 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 275 edges (avg confidence: 0.88)
- Token cost: 590,432 input · 0 output

## Community Hubs (Navigation)
- Simulation code
- Recurring situations and cohort evidence
- Pattern graph and reflection layer
- Experiments and risks
- Prior work, architecture and governance
- Authorship and clinical practice
- Engine internals: decision and state
- Active questions
- Baseline, enrollment and personal model
- Data schema and synthetic stream
- Engine command line, runs and bench
- Problem and fusion evidence
- Incongruence and masking
- Baseline code
- Fusion head and situation memory
- Analogous systems
- Engine core and concept-to-code map
- Labels and consent
- Privacy and regulation
- SOUL-Bench
- Session anchor and signal quality
- Tuning note
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of readings that speak
- Project knowledge graph
- License

## God Nodes (most connected - your core abstractions)
1. `References` - 56 edges
2. `05 Active questions` - 43 edges
3. `16 — Experiment plan: where it works and where it does not` - 42 edges
4. `04 Rolling personal baseline` - 39 edges
5. `20 — Recurring situations: one answer, every later reading of the same situation` - 38 edges
6. `06 Personal model` - 33 edges
7. `12 — What clinical practice already knows` - 33 edges
8. `02 Enrollment (entry calibration)` - 31 edges
9. `10 — Risks and failure modes` - 30 edges
10. `18 — Simulation: what the method does on synthetic users` - 28 edges

## Surprising Connections (you probably didn't know these)
- `soul_bench()` --implements--> `SOUL-Bench ladder B0-B6 in code (bench.soul_bench, within-person metrics, every rung scored before it learns)`  [INFERRED]
  engine/soulcal/bench.py → docs/22-engine.md
- `EngineConfig` --implements--> `Quality gate: no question from body signals alone (EngineConfig.ask_needs_expression)`  [INFERRED]
  engine/soulcal/engine.py → docs/22-engine.md
- `soulcal engine (engine/soulcal, numpy-only Python package)` --references--> `SoulEngine`  [INFERRED]
  README.md → engine/soulcal/engine.py
- `Physiological prior (HR up, HRV down = arousal), learned away per person` --references--> `prior_weights()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/model.py
- `SOUL-Bench` --semantically_similar_to--> `SOUL-Bench (original contribution)`  [INFERRED] [semantically similar]
  docs/08-evaluation-soul-bench.md → AUTHORS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three sub-problems and their modules** — docs_00_problem_cold_start, docs_00_problem_moving_reference, docs_00_problem_missing_labels, docs_02_enrollment_entry_calibration, docs_04_rolling_baseline_rolling_personal_baseline, docs_05_active_questions_active_questions [EXTRACTED 1.00]
- **SOUL-Calibrate closed personal loop** — docs_02_enrollment_entry_calibration, docs_03_session_anchor_session_anchor, docs_04_rolling_baseline_rolling_personal_baseline, docs_06_personal_model_personal_head, docs_01_architecture_conformal_decision, docs_05_active_questions_active_questions, docs_01_architecture_closed_loop_update [EXTRACTED 1.00]
- **New problems of personalization: broken guarantee and life change, with experiments E22/E23 and simulation H** — docs_10_risks_broken_guarantee, docs_10_risks_life_change, docs_16_experiments_e22, docs_16_experiments_e23, docs_18_simulation_new_problems [INFERRED 0.85]
- **Reading audit test batteries** — docs_14_reading_audit_reading_audit, docs_14_reading_audit_persona_invariance, docs_14_reading_audit_uncertainty_honesty, docs_14_reading_audit_non_diagnostic_language, docs_14_reading_audit_sycophancy, docs_14_reading_audit_separation_of_layers, docs_14_reading_audit_safety_routing [EXTRACTED 1.00]
- **Evidence-based governance (claims ledger, provenance, evidence-before-done)** — docs_17_roadmap_and_governance_claims_ledger, docs_17_roadmap_and_governance_provenance_classes, docs_13_ideas_from_prior_work_claim_evidence_map, docs_13_ideas_from_prior_work_evidence_before_done, docs_17_roadmap_and_governance_numbered_stages, docs_17_roadmap_and_governance_decision_log [INFERRED 0.85]
- **Private cohort: consent level 2 -> pilot -> E19 -> cohort transfer evidence** — docs_15_labels_and_consent_consent_level_2_research_cohort, docs_19_private_cohort_pilot_private_cohort_pilot, docs_16_experiments_e19, docs_18_simulation_cohort_transfer, sim_results_results_table_e_cohort_transfer, docs_19_private_cohort_pilot_held_out_users [INFERRED 0.85]
- **Life change repair: corrections as situation-level drift, targeted forgetting, same logic as martingale trigger** — docs_20_recurring_situations_life_change_problem, docs_20_recurring_situations_one_tap_corrections, docs_20_recurring_situations_situation_level_drift, docs_20_recurring_situations_targeted_forgetting, docs_04_rolling_baseline_conformal_test_martingale [EXTRACTED 1.00]
- **Population -> personal head -> situation memory stack** — docs_06_personal_model_shared_encoders, docs_06_personal_model_personal_head, docs_20_recurring_situations_personal_memory, docs_20_recurring_situations_two_personal_models, engine_soulcal_model_fusionhead, engine_soulcal_model_situationmemory [INFERRED 0.85]
- **Words vs face/voice incongruence related work** — docs_references_stacchio_empathic_prompting, docs_references_dragut_2026, docs_references_hoque_picard, docs_21_text_face_incongruence_incongruence_as_reason_to_ask [EXTRACTED 1.00]
- **SOUL-Bench ladder: spec (docs/08), code (bench.soul_bench), code and results (docs/22, DEMO)** — docs_08_evaluation_soul_bench_model_ladder, docs_22_engine_soul_bench_ladder, docs_22_engine_ladder_results, engine_examples_demo_soul_bench_ladder, readme_soulcal_bench_command [INFERRED 0.95]
- **Pattern-graph statistical guardrails** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_reflection_never_feeds_reading, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]

## Communities (27 total, 6 thin omitted)

### Community 0 - "Simulation code"
Cohesion: 0.06
Nodes (45): main(), style(), summarise(), aggregate(), fmt(), main(), calibrate(), coverage() (+37 more)

### Community 1 - "Recurring situations and cohort evidence"
Cohesion: 0.06
Nodes (75): Rolling baseline recovers after step change (0.581 vs 0.584; fixed 0.541), Ambiguous-moment timing helps when situations recur, Cold start: 10-20 labels for the head; head adds 2-8 points between 5 and 40 answers, Broken guarantee (personal memory changes probabilities), Life change (situation memory), Too many questions, Per-state (class-conditional) conformal calibration, E22 Coverage after personalization (+67 more)

### Community 2 - "Pattern graph and reflection layer"
Cohesion: 0.07
Nodes (35): Four factor layers: context, body, expression, reflection, Guardrail: Fisher exact test + Benjamini-Hochberg FDR 10%, Moon links significant on all data but failed correction and replication (no moon effect planted), Personal pattern graph (factor -> state links per person), Pattern graph written in project-map format (graph/build_map.py), Reflection layer (moon phase, moon sign, sun sign; astro.py), Guardrail: the reflection layer never feeds the reading, Guardrail: discovery on first half, replication on second half (same direction) (+27 more)

### Community 3 - "Experiments and risks"
Cohesion: 0.10
Nodes (49): Measurement reactivity, Physiological confounders (exercise, caffeine, alcohol, cycle, medication), Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, Prompt precision (alarm-fatigue metric), Alarm fatigue (prompts), Cold start, 10 — Risks and failure modes, Face signal risk (+41 more)

### Community 4 - "Prior work, architecture and governance"
Cohesion: 0.07
Nodes (32): RinDig (open-source inspiration), RinDig open-source projects (inspiration for docs/14 and docs/17), 01 Architecture of SOUL-Calibrate, Calibration vs representation diagnosis, Integer additive model on bracelet, Diagnostic drift of language, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work (+24 more)

### Community 5 - "Authorship and clinical practice"
Cohesion: 0.13
Nodes (26): Transfer of clinical methods, Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot, Reading audit of the language layer (+18 more)

### Community 6 - "Engine internals: decision and state"
Cohesion: 0.07
Nodes (10): Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, Words-vs-expression disagreement: 29 questions, 48% at real masking (9% base rate, five times the base rate), All engine state in a small JSON file on the phone, engine/soulcal Python package (numpy only), Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits() (+2 more)

### Community 7 - "Active questions"
Cohesion: 0.13
Nodes (30): Active questions, Affect labeling (Lieberman et al., 2007), Prompt as clinical alarm (alarm fatigue), Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions (+22 more)

### Community 8 - "Baseline, enrollment and personal model"
Cohesion: 0.19
Nodes (27): Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment, Trap: baseline absorbs anomalous days (normalising long stress), Baseline per device (+19 more)

### Community 9 - "Data schema and synthetic stream"
Cohesion: 0.12
Nodes (11): Model-agnostic input: probabilities over four states (basic_emotions_to_states), Demo setup: 20 synthetic people, 6 weeks, 3 evening readings/day, channels missing at realistic rates, max one question/day, basic_emotions_to_states(), Decision, _num(), _probs(), read_csv(), write_csv() (+3 more)

### Community 10 - "Engine command line, runs and bench"
Cohesion: 0.22
Nodes (14): bench_table(), _running_average(), _score(), soul_bench(), EngineConfig, bench(), demo(), _fmt() (+6 more)

### Community 11 - "Problem and fusion evidence"
Cohesion: 0.15
Nodes (21): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), 07 Fusion of sources (+13 more)

### Community 12 - "Incongruence and masking"
Cohesion: 0.12
Nodes (20): SOUL (State Observation & Understanding Layer), Masking (words vs face or voice), Empathic prompting (prompt-level incongruence handling), Personal incongruence score (Jensen-Shannon divergence vs personal usual distance), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21) (+12 more)

### Community 13 - "Baseline code"
Cohesion: 0.22
Nodes (5): PersonalBaseline, _only(), _softmax(), factors_for(), Reading

### Community 14 - "Fusion head and situation memory"
Cohesion: 0.19
Nodes (5): Physiological prior (HR up, HRV down = arousal), learned away per person, context_vector(), feature_vector(), prior_weights(), SituationMemory

### Community 15 - "Analogous systems"
Cohesion: 0.26
Nodes (15): Fitbit Body Response, Dexcom G6 (first factory-calibrated real-time CGM), 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy, Speaker recognition enrollment, Abdel-Ghaffar et al. (2025) Fitbit Body Response (+7 more)

### Community 16 - "Engine core and concept-to-code map"
Cohesion: 0.18
Nodes (5): Concept-to-code map, Explanation: evidence per channel for each reading (Decision.contributions), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), SoulEngine, FusionHead

### Community 17 - "Labels and consent"
Cohesion: 0.19
Nodes (14): Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population, Situation memory next to the personal head, GDPR (voice as personal data), User error in labels, Consent level 2 — research cohort, Consent levels 0-2 (normal use, federated, research cohort) (+6 more)

### Community 18 - "Privacy and regulation"
Cohesion: 0.21
Nodes (11): EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Federated learning with differential privacy (Gboard), Kintsugi case, The medical line: name states, never conditions, Behavioral Health Business (2026) Kintsugi closes, Covington (2026) AEPD guidance on AI voice transcription (+3 more)

### Community 19 - "SOUL-Bench"
Cohesion: 0.27
Nodes (10): Claims ledger, 08 Evaluation: SOUL-Bench, Within-person metrics (CCC, Spearman on centred values), Engine tests (13), incl. loop beats today and no supported moon pattern when none planted, SOUL-Bench ladder demo results: B4 generic 0.57 -> B5 0.64 -> B6 full loop 0.76 (last 2 weeks); 0.90 when speaking, SOUL-Bench ladder B0-B6 in code (bench.soul_bench, within-person metrics, every rung scored before it learns), Tension recall: full loop 0.72 vs generic fusion 0.37 (tension is what masking hides), SOUL-Bench ladder B0-B6 (mean over people): B6 full loop 0.76 last 2 weeks, 0.90 when speaking, tense recall 0.72 (+2 more)

### Community 20 - "Session anchor and signal quality"
Cohesion: 0.25
Nodes (6): Cold start, 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, Lexical leakage, Signal quality check (HNR, voice detected), Audio quality check gates questions

## Knowledge Gaps
- **37 isolated node(s):** `MIT License`, `Session anchor (5 seconds)`, `Rolling personal baseline with drift trigger`, `Private cohort pilot`, `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 111 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `08 Evaluation: SOUL-Bench` connect `SOUL-Bench` to `Recurring situations and cohort evidence`, `Experiments and risks`, `Prior work, architecture and governance`, `Authorship and clinical practice`, `Baseline, enrollment and personal model`, `Problem and fusion evidence`, `Analogous systems`, `Labels and consent`, `Privacy and regulation`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **What connects `MIT License`, `Session anchor (5 seconds)`, `Rolling personal baseline with drift trigger` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Simulation code` be split into smaller, more focused modules?**
  _Cohesion score 0.062376237623762376 - nodes in this community are weakly interconnected._
- **Why does `Decision with a guarantee (speak / ask / stay quiet)` connect `Simulation code` to `Prior work, architecture and governance`, `Active questions`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Should `Recurring situations and cohort evidence` be split into smaller, more focused modules?**
  _Cohesion score 0.05707450444292549 - nodes in this community are weakly interconnected._
- **Should `Pattern graph and reflection layer` be split into smaller, more focused modules?**
  _Cohesion score 0.06894049346879536 - nodes in this community are weakly interconnected._
- **Should `Experiments and risks` be split into smaller, more focused modules?**
  _Cohesion score 0.10256410256410256 - nodes in this community are weakly interconnected._