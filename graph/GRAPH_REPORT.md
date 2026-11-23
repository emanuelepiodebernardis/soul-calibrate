# Graph Report - soul-calibrate  (2026-11-23)

## Corpus Check
- 76 files · ~57,352 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 980 nodes · 2910 edges · 34 communities (31 shown, 3 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 539 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Simulation scripts and question budget results
- Recurring situations and question budget
- Enrollment, risks and eight states
- Authorship, inspiration and prior work
- Engine overview, SOUL-Bench and pattern graph
- What precise means, consent and archetype path
- Engine I/O and synthetic checks
- First simulation code
- Engine concept-to-code map
- README: the loop, real voice and the voice question
- Active questions and decision rule
- Enrollment details
- Vibration products and rhythms
- When the bracelet pulses: evidence
- Pulse tuned to the person
- Clinical practice
- Session anchor and voice quality
- Engine personal baseline
- Architecture and regulation
- Archetype prototype
- Engine fusion model
- Engine input and package
- Problem and evidence
- Evaluation: SOUL-Bench
- Fusion of sources
- Incongruence and masking
- Haptic tuning check
- Personal head and situation memory
- Voice and body: body triggers, voice decides
- Cold start and measurement reactivity
- Engine commands and tests
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of speaking

## God Nodes (most connected - your core abstractions)
1. `References` - 61 edges
2. `22 — The engine: code Nightlet can run on its own data` - 53 edges
3. `27 — Voice and vibration: what each is for, and how to integrate them` - 51 edges
4. `README: SOUL-Calibrate` - 49 edges
5. `05 Active questions` - 48 edges
6. `20 — Recurring situations: one answer, every later reading of the same situation` - 45 edges
7. `04 Rolling personal baseline` - 41 edges
8. `12 — What clinical practice already knows` - 40 edges
9. `26 — When and how the bracelet should pulse` - 37 edges
10. `Reading` - 36 edges

## Surprising Connections (you probably didn't know these)
- `soulcal archetypes command (future phase, synthetic cohort)` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/__main__.py
- `Label-free archetype signature from the first 4 days (usual look of each channel, rate of words-expression disagreement), grouped by k-means` --implemented_by--> `signature()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py
- `Archetypes built from cohort answers (channel weights and priors per group)` --implemented_by--> `fit()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py
- `First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start` --implemented_by--> `synthetic_check()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py

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
- **The body triggers, the voice decides, the vibration acts: sources ablation, voice teaching body-only moments, voice check-in and per-person pulse tuning** — docs_27_voice_and_vibration_body_triggers_voice_decides_vibration_acts, docs_27_voice_and_vibration_sources_ablation, docs_27_voice_and_vibration_voice_teaches_body_only, docs_27_voice_and_vibration_voice_checkin, docs_27_voice_and_vibration_pulse_tuning_in_code [EXTRACTED 1.00]
- **Calming vibration products surveyed: on-demand vs automatic personal-threshold triggers** — docs_27_voice_and_vibration_doppel, docs_27_voice_and_vibration_emotioncheck, docs_27_voice_and_vibration_nightware, docs_27_voice_and_vibration_lief, docs_27_voice_and_vibration_apollo_neuro, docs_27_voice_and_vibration_touchpoints, docs_27_voice_and_vibration_garmin [EXTRACTED 1.00]
- **Pulse calibrated to the person: live heart rate, interoception and resonance breathing rate, implemented in SupportConfig/SupportPolicy and checked in haptics_sim** — docs_27_voice_and_vibration_calibration_to_live_heart_rate, docs_27_voice_and_vibration_interoception, docs_27_voice_and_vibration_resonance_breathing_rate, engine_soulcal_support_supportconfig, engine_soulcal_support_supportpolicy_breathing_rate, engine_soulcal_haptics_sim_haptics_check [INFERRED 0.85]

## Communities (34 total, 3 thin omitted)

### Community 0 - "Simulation scripts and question budget results"
Cohesion: 0.06
Nodes (35): main(), mean_runs(), main(), aggregate(), fmt(), main(), curves(), main() (+27 more)

### Community 1 - "Recurring situations and question budget"
Cohesion: 0.05
Nodes (76): Ambiguous-moment timing helps when situations recur, Hard daily question budget, 5-10% of questions at random ordinary moments (selection bias), Cold start: 10-20 labels for the head; head adds 2-8 points between 5 and 40 answers, Federated learning with differential privacy (Gboard), Broken guarantee (personal memory changes probabilities), Life change (situation memory), Selection bias (questions only at anomalous moments) (+68 more)

### Community 2 - "Enrollment, risks and eight states"
Cohesion: 0.06
Nodes (68): Prompt as clinical alarm (alarm fatigue), Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, Cold start, Face signal risk, Novelty during enrollment, Before the interview: synthetic simulation of E1/E2/E3/E4/E9/E19/E20-like experiments, Claims ledger (days 1-30), CREMA-D dataset (+60 more)

### Community 3 - "Authorship, inspiration and prior work"
Cohesion: 0.06
Nodes (46): Transfer of clinical methods, Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot, Reading audit of the language layer (+38 more)

### Community 4 - "Engine overview, SOUL-Bench and pattern graph"
Cohesion: 0.06
Nodes (45): Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, 22 — The engine: code Nightlet can run on its own data, Four factor layers: context, body, expression, reflection, Guardrail: Fisher exact test + Benjamini-Hochberg FDR 10%, SOUL-Bench ladder demo results: B4 generic 0.57 -> B5 0.64 -> B6 full loop 0.76, Words-vs-expression disagreement: 29 questions, 48% at real masking (9% base rate), Moon links significant on all data but failed correction and replication (no planted effect), Personal pattern graph (factor -> state links per person) (+37 more)

### Community 5 - "What precise means, consent and archetype path"
Cohesion: 0.06
Nodes (50): What 'precise' means: agreement with the state the person would choose, per reading and per person (not intensity, mixed states or causes yet), GDPR (voice as personal data), Consent level 2 — research cohort, GDPR, E27 Four vs eight states, E28 Answers needed by granularity, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort (+42 more)

### Community 6 - "Engine I/O and synthetic checks"
Cohesion: 0.12
Nodes (30): _person(), synthetic_check(), bench_table(), _only(), _running_average(), _score(), soul_bench(), app_use_check() (+22 more)

### Community 7 - "First simulation code"
Cohesion: 0.11
Nodes (26): main(), style(), summarise(), decide(), make_population(), _neighbour(), SimConfig, state_from_affect() (+18 more)

### Community 8 - "Engine concept-to-code map"
Cohesion: 0.06
Nodes (11): Concept-to-code map, All engine state in a small JSON file on the phone, Explanation: evidence per channel for each reading (Decision.contributions), Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds() (+3 more)

### Community 9 - "README: the loop, real voice and the voice question"
Cohesion: 0.10
Nodes (28): SOUL (State Observation & Understanding Layer), E31 First check on real voice: per-speaker baseline and a few answers per speaker vs generic pretrained speech model, scored on held-out recordings per speaker, Amazon Halo Tone: always-on band microphones analysing tone of voice; criticised for privacy, microphones removed, line discontinued 2023 (always-on listening costs trust), How others use voice (Nightlet episodic voice, Amazon Halo Tone, Kintsugi), Amazon Halo Tone: always-on voice tone analysis, microphones removed, line discontinued 2023 (MacRumors, Mozilla Privacy Not Included), Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Closed personal loop, Decision with a guarantee (speak / ask / stay quiet) (+20 more)

### Community 10 - "Active questions and decision rule"
Cohesion: 0.13
Nodes (27): Missing labels, Active questions, Affect labeling (Lieberman et al., 2007), Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions (+19 more)

### Community 11 - "Enrollment details"
Cohesion: 0.17
Nodes (29): Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment, Trap: baseline absorbs anomalous days (normalising long stress), Baseline per device (+21 more)

### Community 12 - "Vibration products and rhythms"
Cohesion: 0.13
Nodes (24): When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, Slow heartbeat rhythm: heartbeat-like vibration at 80% of the person's heart rate at that moment, never faster, Apollo Neuro: on-demand or scheduled patterned waves by mode (calm, sleep, focus); small double-blind placebo-controlled crossover HRV trials, doppel: on-demand heartbeat-like vibration slower than resting heart rate; smaller arousal rise and less anxiety before a speech (Azevedo et al., 2017), EmotionCheck (research): false slow heart-rate feedback on the wrist during a stress task; 67 participants, anxiety regulated (Costa et al., 2017), Garmin: stress from HRV while still, relax reminder on high spikes, guided breathing (6 s in, 6 s out), How others use vibration: triggers, patterns and evidence across calming wearables, Lief Smart Patch: automatic vibration when HRV reaches a preset level, then 3-minute HRV biofeedback breathing guidance; pilot of 14 adults (+16 more)

### Community 13 - "When the bracelet pulses: evidence"
Cohesion: 0.13
Nodes (20): When the bracelet pulses (original contribution 14): pulse follows the reading decision, held-out moments, rhythm learned per person, soulcal support command (when to pulse, synthetic), Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), 26 — When and how the bracelet should pulse, 20% of eligible moments held out at random: a micro-randomised trial inside the product, Pulse effect: heart-rate and HRV recovery with a pulse minus the person's recovery without one; optional one-tap 'did it help?', One line on screen with the pulse; calm voice off by default (people are often not alone), When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36 (+12 more)

### Community 14 - "Pulse tuned to the person"
Cohesion: 0.13
Nodes (9): Pulse tuned to the person in code: heartbeat at 80% of the live heart rate (never above 90%), breathing at the learned resonance rate (SupportConfig.heartbeat_ratio, learn_resonance), engine/soulcal Python package (numpy only), When and how the bracelet pulses in code (support.SupportPolicy): pulse when sure, offer when unsure, gates, rhythm learned per person with held-out moments, Rhythm chosen per person by Thompson sampling on the measured effect (SupportPolicy), Pulse tuning in support.py: slow heartbeat at 80% of the current heart rate, never above 90%; breathing pacer starts at 6/min and learns resonance rate by Thompson sampling over 4.5-7 on a separate random stream, soulcal: decision and personalization layer on any face, voice and text emotion model plus bracelet signals (baseline, fusion, conformal speak/ask/quiet, memory, corrections, disagreement, pattern graph), _Arm, Support (+1 more)

### Community 15 - "Clinical practice"
Cohesion: 0.22
Nodes (15): 12 — What clinical practice already knows, HeartSteps trial, Pulse as an intervention to calm, not a stress notification ('pulses when you need to come back to yourself'; no outcome guaranteed, so measure per person), Bos et al. (2022) early warning signals in bipolar disorder, Chromik et al. (2022) alarm fatigue in intensive care, Costache et al. (2025) DBT, alexithymia and emotion awareness, References, Goessl, Curtiss, Hofmann (2017) HRV biofeedback meta-analysis (+7 more)

### Community 16 - "Session anchor and voice quality"
Cohesion: 0.16
Nodes (18): 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, Lexical leakage, Signal quality check (HNR, voice detected), Fitbit Body Response, BCI cross-subject/cross-session transfer learning, 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection (+10 more)

### Community 17 - "Engine personal baseline"
Cohesion: 0.23
Nodes (4): PersonalBaseline, _softmax(), factors_for(), Reading

### Community 18 - "Architecture and regulation"
Cohesion: 0.20
Nodes (15): 01 Architecture of SOUL-Calibrate, EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, 15 — Label quality and consent, Kintsugi case, Periodic audit: no level-0 data in any training set, The medical line: name states, never conditions (+7 more)

### Community 19 - "Archetype prototype"
Cohesion: 0.20
Nodes (7): Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), Archetype, ArchetypeModel, fit(), _js(), _kmeans(), signature()

### Community 20 - "Engine fusion model"
Cohesion: 0.19
Nodes (5): Physiological prior (HR up, HRV down = arousal), learned away per person, context_vector(), feature_vector(), prior_weights(), SituationMemory

### Community 21 - "Engine input and package"
Cohesion: 0.20
Nodes (7): Model-agnostic input: probabilities over four states (basic_emotions_to_states), basic_emotions_to_states(), Decision, _num(), _probs(), read_csv(), write_csv()

### Community 22 - "Problem and evidence"
Cohesion: 0.23
Nodes (14): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Moving reference (people change over weeks), Word-voice conflict ('I'm fine' in a flat voice), Barrett et al. (2019) Emotional Expressions Reconsidered (+6 more)

### Community 23 - "Evaluation: SOUL-Bench"
Cohesion: 0.23
Nodes (14): Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time, Prompt precision (alarm-fatigue metric) (+6 more)

### Community 24 - "Fusion of sources"
Cohesion: 0.19
Nodes (13): Physiological confounders (exercise, caffeine, alcohol, cycle, medication), Hypotheses from words and voice; body sets intensity, 07 Fusion of sources, HRV biofeedback (Goessl et al., 2017), Late fusion with missing-modality handling, Rule out movement (accelerometer) before interpreting heart rate, Source reliability table (words, voice, body, face, context), Words/voice decide state, body sets intensity (+5 more)

### Community 25 - "Incongruence and masking"
Cohesion: 0.18
Nodes (13): Masking (words vs face or voice), Speaker recognition enrollment, E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Personal incongruence score (Jensen-Shannon divergence vs personal usual distance), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight (+5 more)

### Community 26 - "Haptic tuning check"
Cohesion: 0.25
Nodes (12): soulcal haptics command (tuning the pulse), Synthetic checks of sources (voice, words, face, body), app use, voice check-ins and pulse tuning in code (channels_sim, haptics_sim), Haptics synthetic check (assumed effects): heartbeat at 80% of live HR 0.72 vs fixed 60/min 0.53 vs 80% of resting HR 0.35; learned resonance breathing 0.81 in last 8 moments vs fixed 6/min 0.71, Tuning the pulse to each person (synthetic; the effects are assumptions from the literature), Rhythm results: fixed 60/min 0.53 (3.3% faster than the heart), 80% of resting HR 0.35, 80% of live HR 0.72, fixed 6/min breathing 0.71, learned resonance 0.73 (0.81 last 8), rhythm and rate learned 0.73 (0.81), Haptics setup: 5 seeds x 200 people, 24 tense moments each; effect = calming effect of one pulse (1.0 = full), _add(), breathing_effect() (+4 more)

### Community 27 - "Personal head and situation memory"
Cohesion: 0.19
Nodes (13): Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population, Situation memory next to the personal head, User error in labels, CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), Nightlet's disclaimer (user is best source) (+5 more)

### Community 28 - "Voice and body: body triggers, voice decides"
Cohesion: 0.27
Nodes (11): Bracelet always on, app used in a share of moments: accuracy 0.77/0.69/0.62/0.51 at 100/50/25/10% app use, 27 — Voice and vibration: what each is for, and how to integrate them, E33: voice check-ins at body-only moments with an aroused body (response rate, tense moments reached, felt intrusiveness), The less the person talks, the fewer tense moments the pulse can reach (76% -> 13%), while pulse precision stays high: the rule waits rather than guessing, Voice check-in: at a body-only moment with an aroused body and possible tension, invite a 5-second voice note, at most once a day (tense moments reached 28% -> 46% with ~1.9 invitations a week), B. Bracelet always on, app in a share of moments: body-only moments 0.67/0.61/0.52 at 50/25/10%; tense moments reached 76/45/27/13%, Voice, words, face and body (synthetic people), Channels setup: engine demo people, 5 seeds x 20 people, up to 1 question a day, 6 weeks, scored on weeks 5-6 before learning (+3 more)

### Community 29 - "Cold start and measurement reactivity"
Cohesion: 0.40
Nodes (4): Cold start, Measurement reactivity, Measurement reactivity, Eisele et al. (2023) Measurement Reactivity to the Experience Sampling Method

### Community 30 - "Engine commands and tests"
Cohesion: 0.50
Nodes (4): soulcal archetypes command (future phase, synthetic cohort), soulcal channels command (voice, words, face, body), Engine tests (20), incl. loop beats today and no supported moon pattern when none planted, soulcal — the SOUL-Calibrate engine (engine README)

## Knowledge Gaps
- **38 isolated node(s):** `Claims ledger (days 1-30)`, `MSP-Podcast dataset`, `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)`, `Graphify knowledge graph of the project (894 concepts, 2,570 links)`, `MIT License (README)` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 153 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `README: SOUL-Calibrate` connect `README: the loop, real voice and the voice question` to `Simulation scripts and question budget results`, `Recurring situations and question budget`, `Enrollment, risks and eight states`, `Authorship, inspiration and prior work`, `Engine overview, SOUL-Bench and pattern graph`, `What precise means, consent and archetype path`, `Engine I/O and synthetic checks`, `When the bracelet pulses: evidence`, `Clinical practice`, `Architecture and regulation`, `Problem and evidence`, `Evaluation: SOUL-Bench`, `Incongruence and masking`, `Haptic tuning check`, `Voice and body: body triggers, voice decides`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `27 — Voice and vibration: what each is for, and how to integrate them` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`27 — Voice and vibration: what each is for, and how to integrate them` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Claims ledger (days 1-30)`, `MSP-Podcast dataset`, `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Simulation scripts and question budget results` be split into smaller, more focused modules?**
  _Cohesion score 0.05854341736694678 - nodes in this community are weakly interconnected._
- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Engine overview, SOUL-Bench and pattern graph` to `Recurring situations and question budget`, `Enrollment, risks and eight states`, `Authorship, inspiration and prior work`, `What precise means, consent and archetype path`, `Engine concept-to-code map`, `README: the loop, real voice and the voice question`, `Active questions and decision rule`, `Enrollment details`, `When the bracelet pulses: evidence`, `Pulse tuned to the person`, `Architecture and regulation`, `Archetype prototype`, `Engine fusion model`, `Engine input and package`, `Evaluation: SOUL-Bench`, `Fusion of sources`, `Haptic tuning check`, `Voice and body: body triggers, voice decides`, `Engine commands and tests`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `README: SOUL-Calibrate` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`README: SOUL-Calibrate` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Recurring situations and question budget` be split into smaller, more focused modules?**
  _Cohesion score 0.053297199638663056 - nodes in this community are weakly interconnected._