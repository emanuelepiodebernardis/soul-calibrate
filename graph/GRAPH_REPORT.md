# Graph Report - soul-calibrate  (2026-11-22)

## Corpus Check
- 71 files · ~50,748 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 894 nodes · 2570 edges · 27 communities (23 shown, 4 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 418 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Enrollment, risks and experiments
- Simulation scripts and question budget results
- Coarse to fine, cohort and archetypes
- Evaluation, SOUL-Bench and pattern graph
- Recurring situations and question budget risks
- First simulation code
- Authorship, inspiration and prior work
- Engine I/O and the when-to-pulse check
- Architecture, privacy and analogous systems
- Question budget, speed and eight states
- Active questions and decision rule
- Words vs expression and engine state
- Clinical practice
- README, closed loop and real-voice step
- Pulse evidence: alarms, biofeedback, haptic rhythms
- Engine fusion model
- Pattern graph code
- Engine concept-to-code map
- Engine personal baseline
- Problem and evidence
- When and how the bracelet pulses
- Fusion of sources
- Incongruence and masking
- Synthetic device stream
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of speaking

## God Nodes (most connected - your core abstractions)
1. `References` - 59 edges
2. `22 — The engine: code Nightlet can run on its own data` - 48 edges
3. `05 Active questions` - 48 edges
4. `20 — Recurring situations: one answer, every later reading of the same situation` - 44 edges
5. `04 Rolling personal baseline` - 40 edges
6. `README: SOUL-Calibrate` - 39 edges
7. `12 — What clinical practice already knows` - 39 edges
8. `26 — When and how the bracelet should pulse` - 37 edges
9. `Reading` - 36 edges
10. `06 Personal model` - 36 edges

## Surprising Connections (you probably didn't know these)
- `Engine tests (19), incl. loop beats today and no supported moon pattern when none planted` --conceptually_related_to--> `run_stream()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/run.py
- `soulcal archetypes command (future phase, synthetic cohort)` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `soulcal support command (when to pulse, synthetic)` --implemented_by--> `support_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `soul_bench()` --implements--> `Model ladder B0-B6`  [INFERRED]
  engine/soulcal/bench.py → docs/08-evaluation-soul-bench.md
- `soul_bench()` --implements--> `SOUL-Bench ladder B0-B6 in code (bench.soul_bench, within-person metrics)`  [INFERRED]
  engine/soulcal/bench.py → docs/22-engine.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three sub-problems and their modules** — docs_00_problem_cold_start, docs_00_problem_moving_reference, docs_00_problem_missing_labels, docs_02_enrollment_entry_calibration, docs_04_rolling_baseline_rolling_personal_baseline, docs_05_active_questions_active_questions [EXTRACTED 1.00]
- **SOUL-Calibrate closed personal loop** — docs_02_enrollment_entry_calibration, docs_03_session_anchor_session_anchor, docs_04_rolling_baseline_rolling_personal_baseline, docs_06_personal_model_personal_head, docs_01_architecture_conformal_decision, docs_05_active_questions_active_questions, docs_01_architecture_closed_loop_update [EXTRACTED 1.00]
- **What precise means and eight states across README, SOUL-Bench, E27-E28 and wide questions** — readme_what_precise_means_eight_states, docs_08_evaluation_soul_bench_what_precise_means, docs_16_experiments_e27, docs_16_experiments_e28, docs_22_engine_wide_questions, docs_24_what_precise_means_eight_states [INFERRED 0.85]
- **New problems of personalization: broken guarantee and life change, with experiments E22/E23 and simulation H** — docs_10_risks_broken_guarantee, docs_10_risks_life_change, docs_16_experiments_e22, docs_16_experiments_e23, docs_18_simulation_new_problems [INFERRED 0.85]
- **Reading audit test batteries** — docs_14_reading_audit_reading_audit, docs_14_reading_audit_persona_invariance, docs_14_reading_audit_uncertainty_honesty, docs_14_reading_audit_non_diagnostic_language, docs_14_reading_audit_sycophancy, docs_14_reading_audit_separation_of_layers, docs_14_reading_audit_safety_routing [EXTRACTED 1.00]
- **Evidence-based governance (claims ledger, provenance, evidence-before-done)** — docs_17_roadmap_and_governance_claims_ledger, docs_17_roadmap_and_governance_provenance_classes, docs_13_ideas_from_prior_work_claim_evidence_map, docs_13_ideas_from_prior_work_evidence_before_done, docs_17_roadmap_and_governance_numbered_stages, docs_17_roadmap_and_governance_decision_log [INFERRED 0.85]
- **Private cohort: consent level 2 -> pilot -> E19 -> cohort transfer evidence** — docs_15_labels_and_consent_consent_level_2_research_cohort, docs_19_private_cohort_pilot_private_cohort_pilot, docs_16_experiments_e19, docs_18_simulation_cohort_transfer, sim_results_results_table_e_cohort_transfer, docs_19_private_cohort_pilot_held_out_users [INFERRED 0.85]
- **Life change repair: corrections as situation-level drift, targeted forgetting, same logic as martingale trigger** — docs_20_recurring_situations_life_change_problem, docs_20_recurring_situations_one_tap_corrections, docs_20_recurring_situations_situation_level_drift, docs_20_recurring_situations_targeted_forgetting, docs_04_rolling_baseline_conformal_test_martingale [EXTRACTED 1.00]
- **Population -> personal head -> situation memory stack** — docs_06_personal_model_shared_encoders, docs_06_personal_model_personal_head, docs_20_recurring_situations_personal_memory, docs_20_recurring_situations_two_personal_models, engine_soulcal_model_fusionhead, engine_soulcal_model_situationmemory [INFERRED 0.85]
- **Words vs face/voice incongruence related work** — docs_references_stacchio_empathic_prompting, docs_references_dragut_2026, docs_references_hoque_picard, docs_21_text_face_incongruence_incongruence_as_reason_to_ask [EXTRACTED 1.00]
- **User-controlled question settings: budget preset, chosen hours, free notes** — docs_23_question_budget_presets, docs_23_question_budget_user_chosen_hours, docs_23_question_budget_free_notes, engine_soulcal_engine_engineconfig, engine_soulcal_engine_soulengine_note [EXTRACTED 1.00]
- **Eight-state granularity: problem, fix and cost** — docs_24_what_precise_means_eight_states, docs_24_what_precise_means_failed_old_question_rule, docs_24_what_precise_means_wide_questions, docs_24_what_precise_means_fifty_percent_more_answers, docs_24_what_precise_means_within_one [EXTRACTED 1.00]
- **Coarse-to-fine design, its simulation, its code and its experiment** — docs_25_coarse_to_fine_and_archetypes_level_of_detail_per_reading, docs_25_coarse_to_fine_and_archetypes_coarse_to_fine_comparison, sim_results_progressive_one_per_day, sim_results_progressive_two_per_day, docs_16_experiments_e29, readme_coarse_to_fine_and_archetypes, engine_soulcal_detail_level_of_detail [INFERRED 0.85]
- **From personal calibration to needing less of it (CGM path, cohort transfer, pooled head, archetypes)** — docs_11_analogous_systems_cgm_factory_calibration, docs_11_analogous_systems_dexcom_g6, docs_25_coarse_to_fine_and_archetypes_archetypes, docs_25_coarse_to_fine_and_archetypes_reading_on_its_own, docs_16_experiments_e30, docs_25_coarse_to_fine_and_archetypes_pooled_cohort_head, docs_16_experiments_e19, engine_soulcal_archetypes [INFERRED 0.85]
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **When to pulse: calibrated decision, gates, held-out moments and per-person rhythm learning in SupportPolicy** — docs_26_when_to_pulse_pulse_follows_reading_rule, docs_26_when_to_pulse_gates, docs_26_when_to_pulse_held_out_moments, docs_26_when_to_pulse_thompson_sampling, engine_soulcal_support_supportpolicy [EXTRACTED 1.00]

## Communities (27 total, 4 thin omitted)

### Community 0 - "Enrollment, risks and experiments"
Cohesion: 0.05
Nodes (83): Cold start, Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Measurement reactivity, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment (+75 more)

### Community 1 - "Simulation scripts and question budget results"
Cohesion: 0.06
Nodes (32): Coarse-to-fine simulation setup (8 states, 5 seeds x 60 people, 6 situations, 4 readings/day, 28 days), main(), mean_runs(), main(), aggregate(), fmt(), main(), curves() (+24 more)

### Community 2 - "Coarse to fine, cohort and archetypes"
Cohesion: 0.05
Nodes (53): CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), E19 Cohort transfer, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort, A private cohort helps everyone (0.550 -> 0.590 for users never asked), E. Cohort transfer (0.550 -> 0.590 with 50 users; full loop 0.652), Comparison: today -> personal baseline -> cohort answers -> full loop (+45 more)

### Community 3 - "Evaluation, SOUL-Bench and pattern graph"
Cohesion: 0.06
Nodes (58): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time (+50 more)

### Community 4 - "Recurring situations and question budget risks"
Cohesion: 0.07
Nodes (63): Ambiguous-moment timing helps when situations recur, Alarm fatigue (prompts), Broken guarantee (personal memory changes probabilities), Life change (situation memory), Too many questions, Per-state (class-conditional) conformal calibration, E20 Recurring situations, E22 Coverage after personalization (+55 more)

### Community 5 - "First simulation code"
Cohesion: 0.10
Nodes (30): main(), style(), summarise(), calibrate(), coverage(), decide(), prediction_sets(), _quantile() (+22 more)

### Community 6 - "Authorship, inspiration and prior work"
Cohesion: 0.06
Nodes (43): Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot, Reading audit of the language layer, Recurring situations (original contribution) (+35 more)

### Community 7 - "Engine I/O and the when-to-pulse check"
Cohesion: 0.11
Nodes (29): When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36, Policy comparison: body alone 3% tense helped, generic 16%, calibrated fixed 56%, learned 57% (extra recovery 0.41); turned off 0% / 0% / 2% / 6%, _person(), bench_table(), _only(), _running_average(), _score(), soul_bench() (+21 more)

### Community 8 - "Architecture, privacy and analogous systems"
Cohesion: 0.08
Nodes (39): 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, Lexical leakage, Signal quality check (HNR, voice detected), Fitbit Body Response, EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation (+31 more)

### Community 9 - "Question budget, speed and eight states"
Cohesion: 0.07
Nodes (40): E24 Personalization speed, E25 Burden by preset, E26 Free notes, E27 Four vs eight states, E28 Answers needed by granularity, Wide questions when more than three states are plausible (EngineConfig.ask_wide), Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed (+32 more)

### Community 10 - "Active questions and decision rule"
Cohesion: 0.17
Nodes (25): Active questions, Affect labeling (Lieberman et al., 2007), Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+17 more)

### Community 11 - "Words vs expression and engine state"
Cohesion: 0.09
Nodes (5): All engine state in a small JSON file on the phone, Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits()

### Community 12 - "Clinical practice"
Cohesion: 0.19
Nodes (14): Transfer of clinical methods, 12 — What clinical practice already knows, HeartSteps trial, Pulse as an intervention to calm, not a stress notification ('pulses when you need to come back to yourself'; no outcome guaranteed, so measure per person), Bos et al. (2022) early warning signals in bipolar disorder, Chromik et al. (2022) alarm fatigue in intensive care, Costache et al. (2025) DBT, alexithymia and emotion awareness, Goessl, Curtiss, Hofmann (2017) HRV biofeedback meta-analysis (+6 more)

### Community 13 - "README, closed loop and real-voice step"
Cohesion: 0.13
Nodes (21): SOUL (State Observation & Understanding Layer), Speaker recognition enrollment, E31 First check on real voice: per-speaker baseline and a few answers per speaker vs generic pretrained speech model, scored on held-out recordings per speaker, Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Closed personal loop, Decision with a guarantee (speak / ask / stay quiet), README: SOUL-Calibrate, Enrollment (3-7 days) (+13 more)

### Community 14 - "Pulse evidence: alarms, biofeedback, haptic rhythms"
Cohesion: 0.15
Nodes (17): Prompt as clinical alarm (alarm fatigue), Hard daily question budget, Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), 26 — When and how the bracelet should pulse, Pulse gates: bracelet worn, no strong movement, at most 3 a day and 90 minutes apart, only in the user's hours (question budget applied to the wrist), 20% of eligible moments held out at random: a micro-randomised trial inside the product, Pulse effect: heart-rate and HRV recovery with a pulse minus the person's recovery without one; optional one-tap 'did it help?', One line on screen with the pulse; calm voice off by default (people are often not alone) (+9 more)

### Community 15 - "Engine fusion model"
Cohesion: 0.16
Nodes (5): Physiological prior (HR up, HRV down = arousal), learned away per person, context_vector(), feature_vector(), prior_weights(), SituationMemory

### Community 16 - "Pattern graph code"
Cohesion: 0.14
Nodes (9): Pattern graph written in project-map format (graph/build_map.py), find_patterns(), _fisher_two_sided(), Link, report(), _table(), _time_of_day(), to_graph() (+1 more)

### Community 17 - "Engine concept-to-code map"
Cohesion: 0.16
Nodes (6): Concept-to-code map, Explanation: evidence per channel for each reading (Decision.contributions), Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), SoulEngine, FusionHead

### Community 18 - "Engine personal baseline"
Cohesion: 0.23
Nodes (4): PersonalBaseline, _softmax(), factors_for(), Reading

### Community 19 - "Problem and evidence"
Cohesion: 0.19
Nodes (16): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), Source reliability table (words, voice, body, face, context) (+8 more)

### Community 20 - "When and how the bracelet pulses"
Cohesion: 0.17
Nodes (6): When and how the bracelet pulses in code (support.SupportPolicy): pulse when sure, offer when unsure, gates, rhythm learned per person with held-out moments, When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, Rhythm chosen per person by Thompson sampling on the measured effect (SupportPolicy), _Arm, Support, SupportPolicy

### Community 21 - "Fusion of sources"
Cohesion: 0.23
Nodes (10): Physiological confounders (exercise, caffeine, alcohol, cycle, medication), Hypotheses from words and voice; body sets intensity, 07 Fusion of sources, HRV biofeedback (Goessl et al., 2017), Late fusion with missing-modality handling, Rule out movement (accelerometer) before interpreting heart rate, Words/voice decide state, body sets intensity, Wu et al. (2024) survey on missing modalities (+2 more)

### Community 22 - "Incongruence and masking"
Cohesion: 0.24
Nodes (10): Masking (words vs face or voice), E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21), Stacchio et al. Empathic Prompting: Non-Verbal Context Integration for Multimodal LLM Conversations (+2 more)

## Knowledge Gaps
- **38 isolated node(s):** `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)`, `Graphify knowledge graph of the project`, `MIT License (README)`, `Simulation results on synthetic users (0.550 -> 0.590 -> 0.652; rolling baseline 0.581 vs 0.541; ask at 76% of moments)`, `Words vs face/voice disagreement as a reason to ask` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 147 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Evaluation, SOUL-Bench and pattern graph` to `Enrollment, risks and experiments`, `Coarse to fine, cohort and archetypes`, `Recurring situations and question budget risks`, `Authorship, inspiration and prior work`, `Architecture, privacy and analogous systems`, `Question budget, speed and eight states`, `Active questions and decision rule`, `Words vs expression and engine state`, `README, closed loop and real-voice step`, `Pulse evidence: alarms, biofeedback, haptic rhythms`, `Engine fusion model`, `Pattern graph code`, `Engine concept-to-code map`, `When and how the bracelet pulses`, `Fusion of sources`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **What connects `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)`, `Graphify knowledge graph of the project`, `MIT License (README)` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Enrollment, risks and experiments` be split into smaller, more focused modules?**
  _Cohesion score 0.054858934169279 - nodes in this community are weakly interconnected._
- **Why does `README: SOUL-Calibrate` connect `README, closed loop and real-voice step` to `Enrollment, risks and experiments`, `Simulation scripts and question budget results`, `Coarse to fine, cohort and archetypes`, `Evaluation, SOUL-Bench and pattern graph`, `Recurring situations and question budget risks`, `Authorship, inspiration and prior work`, `Question budget, speed and eight states`, `Active questions and decision rule`, `Clinical practice`, `Pulse evidence: alarms, biofeedback, haptic rhythms`, `Problem and evidence`, `Incongruence and masking`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Should `Simulation scripts and question budget results` be split into smaller, more focused modules?**
  _Cohesion score 0.06426906426906427 - nodes in this community are weakly interconnected._
- **Why does `26 — When and how the bracelet should pulse` connect `Pulse evidence: alarms, biofeedback, haptic rhythms` to `Enrollment, risks and experiments`, `Coarse to fine, cohort and archetypes`, `Evaluation, SOUL-Bench and pattern graph`, `Engine I/O and the when-to-pulse check`, `Question budget, speed and eight states`, `Active questions and decision rule`, `Clinical practice`, `README, closed loop and real-voice step`, `Problem and evidence`, `When and how the bracelet pulses`, `Fusion of sources`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Should `Coarse to fine, cohort and archetypes` be split into smaller, more focused modules?**
  _Cohesion score 0.054414414414414414 - nodes in this community are weakly interconnected._