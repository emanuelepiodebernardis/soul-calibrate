# Graph Report - soul-calibrate  (2026-11-22)

## Corpus Check
- Corpus is ~46,579 words - fits in a single context window. You may not need a graph.

## Summary
- 840 nodes · 2387 edges · 41 communities (37 shown, 4 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 364 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Simulation scripts and question budget results
- First simulation code
- Coarse to fine and calibration path
- Authorship, inspiration and pilot
- Engine SOUL-Bench and I/O code
- Experiments and risks
- Active questions and decision rule
- Archetype prototype and synthetic stream
- Recurring situations
- Clinical practice and alarm fatigue
- Question budget and personalization speed
- Engine concept-to-code map
- Enrollment and cold start
- README, closed loop and real-voice step
- Ideas from the author's prior work
- Problem and evidence
- Question budget risks and conformal sets
- Architecture and session anchor
- Engine fusion model
- Engine personal baseline
- Pattern graph design
- Pattern graph code
- What precise means, eight states
- Words vs expression and EMA
- Analogous systems
- Engine overview and archetype command
- Astrology utilities
- Privacy and regulation
- Rolling baseline and drift
- Incongruence and masking
- Engine state persistence
- Evaluation: SOUL-Bench
- Cohort transfer and pilot evidence
- Model-agnostic engine input
- Fusion of sources
- Recurring situations results
- Personal head and consent
- New problems: coverage and life change
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of speaking

## God Nodes (most connected - your core abstractions)
1. `References` - 57 edges
2. `05 Active questions` - 46 edges
3. `22 — The engine: code Nightlet can run on its own data` - 45 edges
4. `20 — Recurring situations: one answer, every later reading of the same situation` - 44 edges
5. `04 Rolling personal baseline` - 40 edges
6. `12 — What clinical practice already knows` - 38 edges
7. `README: SOUL-Calibrate` - 37 edges
8. `06 Personal model` - 36 edges
9. `18 — Simulation: what the method does on synthetic users` - 34 edges
10. `Experiment plan E1-E31 (falsifiable)` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Engine tests (18), incl. loop beats today and no supported moon pattern when none planted` --conceptually_related_to--> `run_stream()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/run.py
- `soulcal archetypes command (future phase, synthetic cohort)` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `Label-free archetype signature from the first 4 days (usual look of each channel, rate of words-expression disagreement), grouped by k-means` --implemented_by--> `signature()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py
- `Archetypes built from cohort answers (channel weights and priors per group)` --implemented_by--> `fit()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py
- `reflection_factors()` --implements--> `Reflection layer (moon phase, moon sign, sun sign; astro.py)`  [INFERRED]
  engine/soulcal/astro.py → docs/22-engine.md

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
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **Coarse-to-fine design, its simulation, its code and its experiment** — docs_25_coarse_to_fine_and_archetypes_level_of_detail_per_reading, docs_25_coarse_to_fine_and_archetypes_coarse_to_fine_comparison, sim_results_progressive_one_per_day, sim_results_progressive_two_per_day, docs_16_experiments_e29, readme_coarse_to_fine_and_archetypes, engine_soulcal_detail_level_of_detail [INFERRED 0.85]
- **From personal calibration to needing less of it (CGM path, cohort transfer, pooled head, archetypes)** — docs_11_analogous_systems_cgm_factory_calibration, docs_11_analogous_systems_dexcom_g6, docs_25_coarse_to_fine_and_archetypes_archetypes, docs_25_coarse_to_fine_and_archetypes_reading_on_its_own, docs_16_experiments_e30, docs_25_coarse_to_fine_and_archetypes_pooled_cohort_head, docs_16_experiments_e19, engine_soulcal_archetypes [INFERRED 0.85]

## Communities (41 total, 4 thin omitted)

### Community 0 - "Simulation scripts and question budget results"
Cohesion: 0.07
Nodes (34): main(), mean_runs(), main(), aggregate(), fmt(), main(), curves(), main() (+26 more)

### Community 1 - "First simulation code"
Cohesion: 0.11
Nodes (27): main(), style(), summarise(), decide(), prediction_sets(), make_population(), _neighbour(), SimConfig (+19 more)

### Community 2 - "Coarse to fine and calibration path"
Cohesion: 0.09
Nodes (35): CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), Speaker recognition enrollment, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort, Personal incongruence score (Jensen-Shannon divergence vs personal usual distance), Level of detail per reading in code (detail.level_of_detail): main state until the fine one is sure, for any model with finer labels, Label-free archetype signature from the first 4 days (usual look of each channel, rate of words-expression disagreement), grouped by k-means (+27 more)

### Community 3 - "Authorship, inspiration and pilot"
Cohesion: 0.09
Nodes (32): Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot, Reading audit of the language layer, Recurring situations (original contribution) (+24 more)

### Community 4 - "Engine SOUL-Bench and I/O code"
Cohesion: 0.14
Nodes (18): bench_table(), _running_average(), _score(), soul_bench(), EngineConfig, bench(), demo(), _fmt() (+10 more)

### Community 5 - "Experiments and risks"
Cohesion: 0.12
Nodes (35): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, Face signal risk, Novelty during enrollment, Before the interview: synthetic simulation of E1/E2/E3/E4/E9/E19/E20-like experiments, Claims ledger (days 1-30), CREMA-D dataset, 16 — Experiment plan: where it works and where it does not (+27 more)

### Community 6 - "Active questions and decision rule"
Cohesion: 0.12
Nodes (30): Active questions, Affect labeling (Lieberman et al., 2007), Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+22 more)

### Community 7 - "Archetype prototype and synthetic stream"
Cohesion: 0.11
Nodes (15): First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start, Archetypes (future phase, synthetic people only), Archetype demo setup: 24 synthetic people (3 types x 8), 4-day label-free signature, 3 archetypes, pooled-head control, up to 1 question a day, 10 seeds, Demo setup: 20 synthetic people, 6 weeks, 3 evening readings/day, channels missing at realistic rates, max one question/day, Archetype, ArchetypeModel, fit(), _js() (+7 more)

### Community 8 - "Recurring situations"
Cohesion: 0.15
Nodes (29): Ambiguous-moment timing helps when situations recur, Closed questions beat open ones; plausible set narrows 2.4 -> 1.4 states in a week, Adaptive conformal inference on the person's own answers (partial fix), Calibration week (7 days, max 1 question/day), Closed questions beat open questions (0.863 vs 0.794), Problem 1: 90% conformal guarantee can break after personalization, 20 — Recurring situations: one answer, every later reading of the same situation, E22 coverage per user after personalization (with/without adaptive conformal) (+21 more)

### Community 9 - "Clinical practice and alarm fatigue"
Cohesion: 0.15
Nodes (17): Transfer of clinical methods, Prompt as clinical alarm (alarm fatigue), HRV biofeedback (Goessl et al., 2017), Prompt precision (alarm-fatigue metric), Alarm fatigue (prompts), 12 — What clinical practice already knows, HeartSteps trial, Bos et al. (2022) early warning signals in bipolar disorder (+9 more)

### Community 10 - "Question budget and personalization speed"
Cohesion: 0.11
Nodes (26): E24 Personalization speed, E25 Burden by preset, E26 Free notes, Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed, Harder engine demo check (week 6: 0.63 none, 0.77 1/day, 0.81 2-3/day), Experiments E24-E26 (presets on real users, answer rate/drop-out, notes vs questions), Failed idea: consensus memory made accuracy worse at every error rate (0.910->0.835, 0.818->0.717, 0.675->0.581) (+18 more)

### Community 11 - "Engine concept-to-code map"
Cohesion: 0.13
Nodes (9): Concept-to-code map, Explanation: evidence per channel for each reading (Decision.contributions), Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Quality gate: no question from body signals alone (EngineConfig.ask_needs_expression), User-chosen question hours (evenings only costs accuracy unless one more question is allowed), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), SoulEngine, FusionHead (+1 more)

### Community 12 - "Enrollment and cold start"
Cohesion: 0.20
Nodes (22): Cold start, Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Measurement reactivity, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment (+14 more)

### Community 13 - "README, closed loop and real-voice step"
Cohesion: 0.13
Nodes (20): SOUL (State Observation & Understanding Layer), E31 First check on real voice: per-speaker baseline and a few answers per speaker vs generic pretrained speech model, scored on held-out recordings per speaker, Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Closed personal loop, README: SOUL-Calibrate, Graphify knowledge graph of the project, MIT License (README), Two new problems: coverage after personalization and life changes (+12 more)

### Community 14 - "Ideas from the author's prior work"
Cohesion: 0.16
Nodes (11): Calibration vs representation diagnosis, Integer additive model on bracelet, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study), sentineledge-core repository (+3 more)

### Community 15 - "Problem and evidence"
Cohesion: 0.18
Nodes (17): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), Lexical leakage (+9 more)

### Community 16 - "Question budget risks and conformal sets"
Cohesion: 0.19
Nodes (19): Hard daily question budget, Too many questions, Per-state (class-conditional) conformal calibration, A budget is not optional (ask at 3 moments in 4 with a generic model), C. Conformal sets (coverage 0.905; ambiguous at 76% of moments), 18 — Simulation: what the method does on synthetic users, Person normalisation alone did not help with out-of-domain public data (0.550 vs 0.545), A. Personalization ladder (0.578 -> 0.605 -> 0.689) (+11 more)

### Community 17 - "Architecture and session anchor"
Cohesion: 0.15
Nodes (15): 01 Architecture of SOUL-Calibrate, 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, Signal quality check (HNR, voice detected), GDPR (voice as personal data), User error in labels, Audio quality check gates questions, Consent level 2 — research cohort (+7 more)

### Community 18 - "Engine fusion model"
Cohesion: 0.19
Nodes (5): Physiological prior (HR up, HRV down = arousal), learned away per person, context_vector(), feature_vector(), prior_weights(), SituationMemory

### Community 19 - "Engine personal baseline"
Cohesion: 0.24
Nodes (4): PersonalBaseline, _only(), _softmax(), Reading

### Community 20 - "Pattern graph design"
Cohesion: 0.18
Nodes (15): Four factor layers: context, body, expression, reflection, Guardrail: Fisher exact test + Benjamini-Hochberg FDR 10%, Moon links significant on all data but failed correction and replication (no planted effect), Personal pattern graph (factor -> state links per person), Pattern graph written in project-map format (graph/build_map.py), Guardrail: discovery on first half, replication on second half (same direction), Supported vs exploratory links (exploratory never shown as finding), Personal patterns: demo-user (+7 more)

### Community 21 - "Pattern graph code"
Cohesion: 0.20
Nodes (9): _bh(), factors_for(), find_patterns(), Link, report(), _table(), _time_of_day(), to_graph() (+1 more)

### Community 22 - "What precise means, eight states"
Cohesion: 0.23
Nodes (15): What 'precise' means: agreement with the state the person would choose, per reading and per person (not intensity, mixed states or causes yet), E27 Four vs eight states, E28 Answers needed by granularity, Wide questions when more than three states are plausible (EngineConfig.ask_wide), 24 — What "precise" means, and what happens with eight states, Eight states on the valence x arousal circumplex (intermediate states; chance 0.125), Experiments E27-E28 (four vs eight agreement and within-one; answers needed per user), Old question rule (ask only when 2-3 plausible) almost never fires with eight states (1.2 questions, 0.324) (+7 more)

### Community 23 - "Words vs expression and EMA"
Cohesion: 0.15
Nodes (4): Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits()

### Community 24 - "Analogous systems"
Cohesion: 0.32
Nodes (14): Fitbit Body Response, BCI cross-subject/cross-session transfer learning, 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy, Abdel-Ghaffar et al. (2025) Fitbit Body Response, Denham (2020) factory-calibrated CGM first-day performance (+6 more)

### Community 25 - "Engine overview and archetype command"
Cohesion: 0.20
Nodes (14): Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), soulcal archetypes command (future phase, synthetic cohort), Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, 22 — The engine: code Nightlet can run on its own data, Engine tests (18), incl. loop beats today and no supported moon pattern when none planted, SOUL-Bench ladder demo results: B4 generic 0.57 -> B5 0.64 -> B6 full loop 0.76, Words-vs-expression disagreement: 29 questions, 48% at real masking (9% base rate), Reflection layer (moon phase, moon sign, sun sign; astro.py) (+6 more)

### Community 26 - "Astrology utilities"
Cohesion: 0.32
Nodes (7): moon_age_days(), moon_longitude(), moon_phase(), moon_sign(), reflection_factors(), sun_sign(), _utc()

### Community 27 - "Privacy and regulation"
Cohesion: 0.24
Nodes (9): EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Federated learning with differential privacy (Gboard), Behavioral Health Business (2026) Kintsugi closes, Covington (2026) AEPD guidance on AI voice transcription, FPF: Red Lines under the EU AI Act (emotion recognition), Orrick (2026) EU Digital Omnibus on AI (+1 more)

### Community 28 - "Rolling baseline and drift"
Cohesion: 0.24
Nodes (12): Trap: baseline absorbs anomalous days (normalising long stress), Baseline per device, Label-free drift trigger (conformal test martingale), 04 Rolling personal baseline, Long-window exponential moving average, Group-to-individual generalisability often fails (Fisher et al., 2018), Person-mean centering, Rolling personal baseline (personal z-score) (+4 more)

### Community 29 - "Incongruence and masking"
Cohesion: 0.24
Nodes (10): Masking (words vs face or voice), E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21), Stacchio et al. Empathic Prompting: Non-Verbal Context Integration for Multimodal LLM Conversations (+2 more)

### Community 31 - "Evaluation: SOUL-Bench"
Cohesion: 0.38
Nodes (10): Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time, SOUL-Bench (+2 more)

### Community 32 - "Cohort transfer and pilot evidence"
Cohesion: 0.36
Nodes (8): E19 Cohort transfer, A private cohort helps everyone (0.550 -> 0.590 for users never asked), E. Cohort transfer (0.550 -> 0.590 with 50 users; full loop 0.652), Comparison: today -> personal baseline -> cohort answers -> full loop, Control arm: current SOUL readings computed in parallel, never shown, 19 — Private cohort pilot: from today's approach to SOUL-Calibrate, Held-out users never asked (transfer measurement), Limits: synthetic people, signal-only situation recognition, assumed answer error rates

### Community 33 - "Model-agnostic engine input"
Cohesion: 0.25
Nodes (8): Model-agnostic input: probabilities over four states (basic_emotions_to_states), engine/soulcal Python package (numpy only), soulcal: decision and personalization layer on any face, voice and text emotion model plus bracelet signals (baseline, fusion, conformal speak/ask/quiet, memory, corrections, disagreement, pattern graph), basic_emotions_to_states(), Astrology reflection layer, False-discovery correction and replication, Personal pattern graph (context, body, expression, astrology reflection layer), soulcal engine (engine/soulcal, numpy-only Python package)

### Community 34 - "Fusion of sources"
Cohesion: 0.36
Nodes (8): Physiological confounders (exercise, caffeine, alcohol, cycle, medication), Hypotheses from words and voice; body sets intensity, 07 Fusion of sources, Late fusion with missing-modality handling, Rule out movement (accelerometer) before interpreting heart rate, Words/voice decide state, body sets intensity, Wu et al. (2024) survey on missing modalities, Physiological confounders

### Community 35 - "Recurring situations results"
Cohesion: 0.36
Nodes (8): E20 Recurring situations, B. Ambiguous vs random question moments (no clear difference), Choosing when to ask helps when situations recur (tie with drifting mood, ambiguous wins with recurring situations), F. Recurring situations (0.504 -> 0.751 -> 0.863; 0.892 after one answer), Recurring situations calibration, Same situation read correctly ~9 in 10 after one answer (0.892 vs 0.497), Why a second experiment (drifting mood vs recurring situations), Table B: active versus random questions

### Community 36 - "Personal head and consent"
Cohesion: 0.38
Nodes (7): Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population, Situation memory next to the personal head, Consent levels 0-2 (normal use, federated, research cohort), Reliability weight per answer, Problem 3: two personal models must not compete (head then memory)

### Community 37 - "New problems: coverage and life change"
Cohesion: 0.48
Nodes (7): Broken guarantee (personal memory changes probabilities), Life change (situation memory), E22 Coverage after personalization, E23 Life change, H. New problems: coverage 0.855 random / 0.881 adaptive conformal / 0.930 ambiguous; one-tap corrections recover life change 0.649 -> 0.711, Personal memory (Gaussian kernel over stored answers), Gibbs & Candès (2021) Adaptive Conformal Inference Under Distribution Shift (NeurIPS)

## Knowledge Gaps
- **37 isolated node(s):** `MIT License`, `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `openSMILE eGeMAPS features (88) computed on phone`, `Rolling baseline recovers after step change (0.581 vs 0.584; fixed 0.541)`, `Baseline per device` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 140 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Engine overview and archetype command` to `Model-agnostic engine input`, `Fusion of sources`, `Authorship, inspiration and pilot`, `Coarse to fine and calibration path`, `Active questions and decision rule`, `Recurring situations`, `Question budget and personalization speed`, `Engine concept-to-code map`, `Enrollment and cold start`, `README, closed loop and real-voice step`, `Ideas from the author's prior work`, `Architecture and session anchor`, `Engine fusion model`, `Pattern graph design`, `What precise means, eight states`, `Rolling baseline and drift`, `Engine state persistence`, `Evaluation: SOUL-Bench`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **What connects `MIT License`, `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `openSMILE eGeMAPS features (88) computed on phone` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Simulation scripts and question budget results` be split into smaller, more focused modules?**
  _Cohesion score 0.06569133677567413 - nodes in this community are weakly interconnected._
- **Why does `README: SOUL-Calibrate` connect `README, closed loop and real-voice step` to `Cohort transfer and pilot evidence`, `Model-agnostic engine input`, `Coarse to fine and calibration path`, `Authorship, inspiration and pilot`, `Simulation scripts and question budget results`, `Experiments and risks`, `Recurring situations`, `Clinical practice and alarm fatigue`, `Question budget and personalization speed`, `Ideas from the author's prior work`, `Problem and evidence`, `Question budget risks and conformal sets`, `Architecture and session anchor`, `What precise means, eight states`, `Analogous systems`, `Engine overview and archetype command`, `Incongruence and masking`, `Evaluation: SOUL-Bench`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Should `First simulation code` be split into smaller, more focused modules?**
  _Cohesion score 0.10841750841750841 - nodes in this community are weakly interconnected._
- **Why does `20 — Recurring situations: one answer, every later reading of the same situation` connect `Recurring situations` to `Cohort transfer and pilot evidence`, `Recurring situations results`, `Personal head and consent`, `New problems: coverage and life change`, `Experiments and risks`, `Active questions and decision rule`, `Clinical practice and alarm fatigue`, `Question budget and personalization speed`, `Enrollment and cold start`, `README, closed loop and real-voice step`, `Question budget risks and conformal sets`, `Architecture and session anchor`, `Engine overview and archetype command`, `Privacy and regulation`, `Rolling baseline and drift`, `Evaluation: SOUL-Bench`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Should `Coarse to fine and calibration path` be split into smaller, more focused modules?**
  _Cohesion score 0.0859465737514518 - nodes in this community are weakly interconnected._