# Graph Report - graph-src  (2026-11-27)

## Corpus Check
- 105 files · ~90,430 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .cff 1)

## Summary
- 1364 nodes · 4152 edges · 46 communities (42 shown, 4 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 695 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Speech front end and real-voice check
- Voice-and-body signatures
- Recurring situations and question budget
- Voice, vibration and the pulse
- Cohort pilot and archetype path
- Simulation scripts and question budget results
- Signature checks (code)
- Risks, traps and cold start
- Engine fusion code
- Engine overview and commands
- Ideas from prior work
- Archetype and channel checks (code)
- User control and situations
- First simulation code
- Engine core code
- Clinical practice
- SOUL-Bench code
- Active questions and decision rule
- Problem and evidence
- Enrollment details
- Understanding layer concept
- Analogous systems
- Question budget experiments
- README: voice, vibration and the loop
- Architecture and the closed loop
- Archetype prototype
- People who don't know what they feel
- Understanding layer code
- Personal head and baseline
- Understanding results
- Engine input and run
- Authorship
- Astrology reflection code
- Incongruence and masking
- Evaluation: SOUL-Bench
- Conformal speak, ask, quiet
- Coarse-to-fine simulation
- Emotional granularity evidence
- Answer reliability
- Engine entry and commands
- README: the project at a glance
- Public approach comparison
- Weekly accuracy
- Accuracy when speaking
- Share of speaking
- soulcal package

## God Nodes (most connected - your core abstractions)
1. `30 · The understanding layer` - 70 edges
2. `References` - 61 edges
3. `22 — The engine: code Nightlet can run on its own data` - 59 edges
4. `SoulEngine` - 58 edges
5. `README: SOUL-Calibrate` - 56 edges
6. `Reading` - 55 edges
7. `05 Active questions` - 52 edges
8. `27 — Voice and vibration: what each is for, and how to integrate them` - 52 edges
9. `29 — Your voice, your body, your signature: one fixed sentence, three uses` - 51 edges
10. `20 — Recurring situations: one answer, every later reading of the same situation` - 47 edges

## Surprising Connections (you probably didn't know these)
- `Ladder of results on free voice notes (synthetic, 5 seeds x 40 people, 4 states): generic 0.44 -> baseline 0.68 -> daily anchor 0.74 -> 1/2/4 tagged readings 0.80/0.82/0.83` --semantically_similar_to--> `test_personal_baseline_and_answers_help_when_the_speaker_dominates()`  [INFERRED] [semantically similar]
  docs/29-voice-signatures.md → realvoice/tests/test_protocol.py
- `SupportPolicy` --implements--> `soulcal support command (when to pulse, synthetic)`  [INFERRED]
  engine/soulcal/support.py → docs/22-engine.md
- `First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/__main__.py
- `Label-free archetype signature from the first 4 days (usual look of each channel, rate of words-expression disagreement), grouped by k-means` --implemented_by--> `signature()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/archetypes.py
- `Archetypes built from cohort answers (channel weights and priors per group)` --implemented_by--> `fit()`  [INFERRED]
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
- **When to pulse: calibrated decision, gates, held-out moments and per-person rhythm learning in SupportPolicy** — docs_26_when_to_pulse_pulse_follows_reading_rule, docs_26_when_to_pulse_gates, docs_26_when_to_pulse_held_out_moments, docs_26_when_to_pulse_thompson_sampling, engine_soulcal_support_supportpolicy [EXTRACTED 1.00]
- **The body triggers, the voice decides, the vibration acts: sources ablation, voice teaching body-only moments, voice check-in and per-person pulse tuning** — docs_27_voice_and_vibration_body_triggers_voice_decides_vibration_acts, docs_27_voice_and_vibration_sources_ablation, docs_27_voice_and_vibration_voice_teaches_body_only, docs_27_voice_and_vibration_voice_checkin, docs_27_voice_and_vibration_pulse_tuning_in_code [EXTRACTED 1.00]
- **Calming vibration products surveyed: on-demand vs automatic personal-threshold triggers** — docs_27_voice_and_vibration_doppel, docs_27_voice_and_vibration_emotioncheck, docs_27_voice_and_vibration_nightware, docs_27_voice_and_vibration_lief, docs_27_voice_and_vibration_apollo_neuro, docs_27_voice_and_vibration_touchpoints, docs_27_voice_and_vibration_garmin [EXTRACTED 1.00]
- **Pulse calibrated to the person: live heart rate, interoception and resonance breathing rate, implemented in SupportConfig/SupportPolicy and checked in haptics_sim** — docs_27_voice_and_vibration_calibration_to_live_heart_rate, docs_27_voice_and_vibration_interoception, docs_27_voice_and_vibration_resonance_breathing_rate, engine_soulcal_support_supportconfig, engine_soulcal_support_supportpolicy_breathing_rate, engine_soulcal_haptics_sim_haptics_check [INFERRED 0.85]
- **E31 real-voice check: leave-one-speaker-out protocol on RAVDESS with emotion2vec+ or MFCC encoders, run by realvoice/e31_real_voice.py** — docs_16_experiments_e31, docs_28_speech_front_end_e31_protocol, docs_28_speech_front_end_ravdess, docs_28_speech_front_end_emotion2vec_plus, docs_28_speech_front_end_mfcc_encoder, realvoice_e31_real_voice, realvoice_readme_results_output [EXTRACTED 1.00]
- **Open speech front end feeding the model-agnostic engine: speech to text and speech emotion models produce text and voice probabilities for SoulEngine** — docs_28_speech_front_end_plug_in_pipeline, docs_28_speech_front_end_whisper, docs_28_speech_front_end_parakeet, docs_28_speech_front_end_sensevoice, docs_28_speech_front_end_emotion2vec_plus, docs_22_engine_four_state_adapter, docs_28_speech_front_end_two_signals_one_voice_note [INFERRED 0.85]
- **One fixed sentence, three moments: enrollment, daily anchor, tagged reading -> personal signature** — docs_29_voice_signatures_one_fixed_sentence_three_moments, docs_29_voice_signatures_enrollment, docs_29_voice_signatures_daily_anchor, docs_29_voice_signatures_tagged_reading, docs_29_voice_signatures_personal_signature [EXTRACTED 1.00]
- **Signature wired as the engine's voice channel: replace generic voice, soften (temperature 4), body not counted twice, answered voice notes teach it** — docs_29_voice_signatures_feeds_voice_channel, docs_29_voice_signatures_replaces_generic_voice, docs_29_voice_signatures_softened_temperature4, docs_29_voice_signatures_avoid_double_counting_body, docs_29_voice_signatures_answers_teach_signature, engine_soulcal_engine_soulengine [EXTRACTED 1.00]
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **Scaffolded answers for people who do not know what they feel: ask what it is like, not sure, body first, reliability weighting, simulated by answers_check** — docs_30_understanding_layer_ask_what_it_is_like, docs_30_understanding_layer_not_sure_option, docs_30_understanding_layer_compose, docs_30_understanding_layer_body_first, docs_30_understanding_layer_answer_reliability, docs_30_understanding_layer_answers_check [EXTRACTED 1.00]
- **Four evidence-based ingredients of the understanding layer** — docs_30_understanding_layer_affect_labeling, docs_30_understanding_layer_emotional_granularity, docs_30_understanding_layer_body_mirror, docs_30_understanding_layer_reflection_prompts [EXTRACTED 1.00]

## Communities (46 total, 4 thin omitted)

### Community 0 - "Speech front end and real-voice check"
Cohesion: 0.05
Nodes (57): Strong open speech models as the front end, calibration on top (original contribution 16), Model-agnostic input: probabilities over four states (basic_emotions_to_states), Stronger speech front ends: how much calibration still adds (channels_sim.frontend_check), Real-voice check with an open speech-emotion model (E31), outside the engine (realvoice/e31_real_voice.py), One line on screen with the pulse; calm voice off by default (people are often not alone), Audio events (a laugh, a sigh, crying) as a natural next input, CosyVoice (FunAudioLLM): open text-to-speech, the open counterpart for generating speech; only matters for the optional calm voice, not for reading, 28 — Listening well from day one: open speech models as the front end (+49 more)

### Community 1 - "Voice-and-body signatures"
Cohesion: 0.06
Nodes (40): Voice-and-body signatures (original contribution 17): one fixed sentence for enrollment, daily anchor and tagged readings; wired into the engine as its voice channel (softened, replacing the generic voice reading, body not counted twice) and into the real-voice check, Voice enrollment: three fixed sentences a day; later the same sentence read in a clear state becomes the person's signature, In code: engine/soulcal/anchors.py (SignatureModel.set_anchor), with enrollment and tagged readings, Lexical leakage, The signature as the voice channel in code: softened, replacing the generic voice reading, body not counted twice; answered voice notes become tagged readings (SoulEngine.enroll/anchor/tag, Reading.voice_features, EngineConfig.signature*, signature_difference()), Voice-and-body signatures in code (anchors.SignatureModel, .difference()): enrollment, daily anchor, tagged readings; what changes in the person, The 5-second evening anchor is the cheapest, most valuable feedback (3 evenings a week costs 7-12 points), Signature accuracy week 3 / week 6: light 0.72/0.74, standard 0.75/0.82, fast 0.82/0.86 (+32 more)

### Community 2 - "Recurring situations and question budget"
Cohesion: 0.07
Nodes (66): Recurring situations (original contribution 8), Ambiguous-moment timing helps when situations recur, Class-conditional (per-state) conformal calibration, Hard daily question budget, Alarm fatigue (prompts), Broken guarantee (personal memory changes probabilities), Life change (situation memory), Too many questions (+58 more)

### Community 3 - "Voice, vibration and the pulse"
Cohesion: 0.06
Nodes (60): The body triggers, the voice decides, the vibration acts (original contribution 15): voice moments teach body-only moments, voice check-in, pulse tied to live heart rate and resonance breathing, Kintsugi case, The medical line: name states, never conditions, soulcal haptics command (tuning the pulse), Synthetic checks of sources (voice, words, face, body), app use, voice check-ins and pulse tuning in code (channels_sim, haptics_sim), Offer: one soft tap and 'Want a calm minute?'; the answer is also a label, Slow heartbeat rhythm: heartbeat-like vibration at 80% of the person's heart rate at that moment, never faster, Amazon Halo Tone: always-on band microphones analysing tone of voice; criticised for privacy, microphones removed, line discontinued 2023 (always-on listening costs trust) (+52 more)

### Community 4 - "Cohort pilot and archetype path"
Cohesion: 0.06
Nodes (54): Coarse to fine, cohort learning and archetype prototype (original contribution 13), What 'precise' means: agreement with the state the person would choose, per reading and per person (not intensity, mixed states or causes yet), CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), E19 Cohort transfer, E27 Four vs eight states, E28 Answers needed by granularity, E29 Level of detail per reading (+46 more)

### Community 5 - "Simulation scripts and question budget results"
Cohesion: 0.09
Nodes (19): main(), main(), main(), main(), main(), A. One calibration week then 5 test days: 4 vs 8 states, old rule vs wide questions, STATES.md — Four states or eight? (results), B. Personalization speed with 4 vs 8 states (wide questions allowed) (+11 more)

### Community 6 - "Signature checks (code)"
Cohesion: 0.10
Nodes (22): Conformal set, speak / ask / quiet, daily question budget (SoulEngine.observe); adaptive per-person thresholds (SoulEngine._learn), User-chosen question hours (evenings only costs accuracy unless one more question is allowed), The signature inside the engine (4 seeds x 25 people): public approach 0.41/52%, engine without signature 0.57/61%, + enrollment and anchor 0.67/74%, + 3 tagged 0.75/81%, default 0.81/88%; added instead of replacing 0.65/70%; not softened 0.71/75%, engine_check(), _reading(), _to_reading(), EngineConfig, _softmax() (+14 more)

### Community 7 - "Risks, traps and cold start"
Cohesion: 0.11
Nodes (48): Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, Face signal risk, Novelty during enrollment, Before the interview: synthetic simulation of E1/E2/E3/E4/E9/E19/E20-like experiments, Claims ledger (days 1-30), CREMA-D dataset, 16 — Experiment plan: where it works and where it does not, E1 Person normalisation vs none (+40 more)

### Community 8 - "Engine fusion code"
Cohesion: 0.06
Nodes (12): Fusion of face, voice, words and body with missing channels (model.FusionHead); personal head shrunk toward a transparent prior (FusionHead.update), Explanation: evidence per channel for each reading (Decision.contributions), Situation memory in code (model.SituationMemory): time, day and what the channels say, Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits() (+4 more)

### Community 9 - "Engine overview and commands"
Cohesion: 0.07
Nodes (42): soulcal archetypes command (future phase, synthetic cohort), soulcal channels command (voice, words, face, body), Concept-to-code map, One-tap "not quite" corrections (SoulEngine.correct), Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, 22 — The engine: code Nightlet can run on its own data, Drift trigger: conformal test martingale (PersonalBaseline._martingale_step), Engine tests (28), incl. loop beats today and no supported moon pattern when none planted (+34 more)

### Community 10 - "Ideas from prior work"
Cohesion: 0.07
Nodes (29): Calibration vs representation diagnosis, Integer additive model on bracelet, Diagnostic drift of language, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study) (+21 more)

### Community 11 - "Archetype and channel checks (code)"
Cohesion: 0.10
Nodes (20): Rhythm chosen per person by Thompson sampling on the measured effect (SupportPolicy), Pulse tuning in support.py: slow heartbeat at 80% of the current heart rate, never above 90%; breathing pacer starts at 6/min and learns resonance rate by Thompson sampling over 4.5-7 on a separate random stream, app_use_check(), checkin_check(), _mask(), _score(), sources_check(), Decision (+12 more)

### Community 12 - "User control and situations"
Cohesion: 0.12
Nodes (22): main(), run(), answer(), configure_states(), exp_life_change(), exp_situations(), make_person(), Memory (+14 more)

### Community 13 - "First simulation code"
Cohesion: 0.16
Nodes (27): main(), style(), summarise(), make_population(), _neighbour(), SimConfig, state_from_affect(), User (+19 more)

### Community 14 - "Engine core code"
Cohesion: 0.09
Nodes (17): PersonalBaseline, _bh(), factors_for(), find_patterns(), _fisher_two_sided(), Link, report(), _table() (+9 more)

### Community 15 - "Clinical practice"
Cohesion: 0.12
Nodes (28): Prompt as clinical alarm (alarm fatigue), 12 — What clinical practice already knows, HeartSteps trial, Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, 26 — When and how the bracelet should pulse, Pulse gates: bracelet worn, no strong movement, at most 3 a day and 90 minutes apart, only in the user's hours (question budget applied to the wrist), 20% of eligible moments held out at random: a micro-randomised trial inside the product (+20 more)

### Community 16 - "SOUL-Bench code"
Cohesion: 0.12
Nodes (24): When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36, Policy comparison: body alone 3% tense helped, generic 16%, calibrated fixed 56%, learned 57% (extra recovery 0.41); turned off 0% / 0% / 2% / 6%, synthetic_check(), bench_table(), _only(), _running_average(), _score(), soul_bench() (+16 more)

### Community 17 - "Active questions and decision rule"
Cohesion: 0.11
Nodes (31): Cold start, Measurement reactivity, Active questions, Affect labeling (Lieberman et al., 2007), Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Just-in-time adaptive intervention (JITAI) framework (+23 more)

### Community 18 - "Problem and evidence"
Cohesion: 0.10
Nodes (28): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Physiological confounders (exercise, caffeine, alcohol, cycle, medication), Hypotheses from words and voice; body sets intensity (+20 more)

### Community 19 - "Enrollment details"
Cohesion: 0.15
Nodes (32): Moving reference (people change over weeks), Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment, Trap: baseline absorbs anomalous days (normalising long stress) (+24 more)

### Community 20 - "Understanding layer concept"
Cohesion: 0.15
Nodes (29): The understanding layer (original contribution 18): the reflective part of SOUL as a way in rather than a signal (from the conversation with Nightlet's founder); prompts at hard moments to name, feel and see one's states, dosed by moment, bridge to people; checked on 462 real people from five open ESM studies, Naming the feeling (affect labeling) lowers amygdala response and distress, Interoception, the body as a mirror: heartbeat-synchronised wrist vibration; signature shown back and the heartbeat pulse, 30 · The understanding layer, Reflection prompted by context: LLM prompts from phone sensing (MindScape), expressive writing; questions from situation memory and a weekly story, Two rounds of simulation on the 462 real profiles (understanding_sim.py, 8 weeks, 3 seeds): round 1 effects as reported, round 2 conservative, Understanding layer: helps the person understand the reading (put it into words, notice it in the body, see their own patterns, talk to someone when it lasts), APA (2025) AI and adolescent well-being; health advisory on generative AI chatbots and wellness apps (+21 more)

### Community 21 - "Analogous systems"
Cohesion: 0.12
Nodes (26): openSMILE eGeMAPS features (88) computed on phone, EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Federated learning with differential privacy (Gboard), BCI cross-subject/cross-session transfer learning, 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection (+18 more)

### Community 22 - "Question budget experiments"
Cohesion: 0.10
Nodes (27): E24 Personalization speed, E25 Burden by preset, E26 Free notes, Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed, Harder engine demo check (week 6: 0.63 none, 0.77 1/day, 0.81 2-3/day), Experiments E24-E26 (presets on real users, answer rate/drop-out, notes vs questions) (+19 more)

### Community 23 - "README: voice, vibration and the loop"
Cohesion: 0.13
Nodes (24): SOUL (State Observation & Understanding Layer), Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Closed personal loop, Decision with a guarantee (speak / ask / stay quiet), README: SOUL-Calibrate, Enrollment (3-7 days): fixed sentences, resting physiology, sliders and one word; later the same sentence read in a clear state becomes the voice-and-body signature, Future phase: learn from consenting users as glucose monitors moved from finger-stick to factory calibration, Graphify knowledge graph of the project (1,169 concepts, 3,430 links) (+16 more)

### Community 24 - "Architecture and the closed loop"
Cohesion: 0.13
Nodes (20): SOUL-Calibrate (original contribution 1): entry calibration, 5-second session anchor, rolling personal baseline, conformal questions, 01 Architecture of SOUL-Calibrate, 03 Session anchor (5 seconds), Signal quality check (HNR, voice detected), Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population, Situation memory next to the personal head (+12 more)

### Community 25 - "Archetype prototype"
Cohesion: 0.17
Nodes (10): Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), Archetype demo setup: 24 synthetic people (3 types x 8), 4-day label-free signature, 3 archetypes, pooled-head control, up to 1 question a day, 10 seeds, Archetype, ArchetypeModel, fit(), _js(), _kmeans(), _person() (+2 more)

### Community 26 - "People who don't know what they feel"
Cohesion: 0.19
Nodes (17): A person who does not know what they feel in code: ask what it is like (pleasant? energy?), body first, weigh answers by reliability (understanding.compose, body_first, AnswerReliability; understanding_sim.answers_check), Alexithymia (low emotional awareness; TAS-20), understanding.AnswerReliability: weighs each answer by how often this person agrees with confident readings (one-person Dawid & Skene), answers_check simulation on the 462 real profiles: hard quarter vs others, 3 seeds (python -m soulcal understanding), Ask what it is like, not its name: pleasant or unpleasant first (valence), then a lot of energy or little, with 'not sure' always allowed, Emotional awareness improves with training (interventions reduce alexithymia, g = -0.52; mindfulness lowers TAS-20 by ~5 points), The body comes first: shared bodily maps of emotions; interoceptive awareness predicts alexithymia; skills-based body-awareness training works best, understanding.body_first(): says what the bracelet and voice show before the question, then "where do you feel it?" (+9 more)

### Community 27 - "Understanding layer code"
Cohesion: 0.19
Nodes (8): Understanding layer in code: a finer word, the body mirror, a reflective question, a weekly story, a bridge to people; dosed at hard moments; need gate for the bridge (understanding.NeedGate, granularity_index, prompt; understanding_sim.understanding_check on open ESM data), understanding.NeedGate: watches share of negative readings and swaps of confidently separated negative states; decides only the bridge to a person, granularity_index(), NeedGate, prompt(), _person_run(), test_need_gate_and_prompts(), understanding module: need gate, granularity index, reflective prompts with an optional lens; checked on 462 people from open ESM data

### Community 28 - "Personal head and baseline"
Cohesion: 0.19
Nodes (6): centered_matrix(), PersonalHead, rolling_transform(), RollingBaseline, test_fixed_baseline_does_not_move(), test_personal_head_falls_back_to_population_without_answers()

### Community 29 - "Understanding results"
Cohesion: 0.15
Nodes (14): Answers results: hard quarter right answers 0.75 -> 0.89 (0.82 conservative) with what-it-is-like questions, 0.92 with body first; gap to others 10 points -> 1-3; reading +4-5 points, level with others, Bridge to people: when distress lasts (10 days in a row of mostly negative readings) the prompt points to a person, never to more time in the app, Understanding layer results: tense/low confusion 0.30 -> 0.17 (0.24 conservative), negative affect -10% (-4%) for people who need it; ~4 prompts a week vs ~1 for people doing well, The reading barely changes (0.68 -> 0.69): better labels help the person more than the model, The step towards a person is precise: 12-16% of people who need it, about 0.1% of people doing well, Answers round 1: ask for the name 0.75/0.85 -> what it is like 0.89/0.92 -> body first 0.92/0.94 -> reliability 0.92/0.94 -> layer 0.93/0.94; reading weeks 7-8 0.66 -> 0.71, Answers round 2 (conservative): 0.75/0.85 -> 0.82/0.86 -> 0.84/0.88 -> 0.84/0.88 -> 0.85/0.88; reading 0.66 -> 0.70, Understanding layer (docs/30) demo output: 462 people from open ESM data (+6 more)

### Community 30 - "Engine input and run"
Cohesion: 0.21
Nodes (8): Input format: soulcal/schema.py (CSV columns or Reading objects), RunResult, write_decisions(), _num(), _probs(), read_csv(), write_csv(), test_csv_round_trip()

### Community 31 - "Authorship"
Cohesion: 0.14
Nodes (14): Transfer of clinical methods (original contribution 4), Emanuele De Bernardis, MIT License, Nightlet SOUL layer proposal (first written 21 November 2026), What 'precise' means, and eight states (original contribution 12), Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot (original contribution 3), Question budget and personalization speed (original contribution 11): light / standard / fast, chosen hours, free notes (+6 more)

### Community 32 - "Astrology reflection code"
Cohesion: 0.30
Nodes (8): moon_age_days(), moon_longitude(), moon_phase(), moon_sign(), reflection_factors(), sun_sign(), _utc(), test_astro_reference_dates()

### Community 33 - "Incongruence and masking"
Cohesion: 0.20
Nodes (12): Incongruence as a reason to ask (original contribution 9), Masking (words vs face or voice), E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21) (+4 more)

### Community 34 - "Evaluation: SOUL-Bench"
Cohesion: 0.27
Nodes (13): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time (+5 more)

### Community 35 - "Conformal speak, ask, quiet"
Cohesion: 0.24
Nodes (7): calibrate(), coverage(), decide(), prediction_sets(), _quantile(), test_decision_rule(), test_prediction_sets_are_never_empty()

### Community 36 - "Coarse-to-fine simulation"
Cohesion: 0.29
Nodes (6): Coarse-to-fine simulation setup (8 states, 5 seeds x 60 people, 6 situations, 4 readings/day, 28 days), coarse_of(), coarse_proba(), evidence_vector(), run(), _threshold()

### Community 37 - "Emotional granularity evidence"
Cohesion: 0.31
Nodes (10): Emotional granularity (Hoemann, Barrett & Quigley, 2021), Emotional granularity grows with repeated momentary reporting; measured by granularity_index, Lowest quarter of differentiation: answers right 75% vs 85% for the others, Emotion knowledge raises differentiation (short emotion-knowledge intervention; online emotion-word training partial effects, 2024), Finding: people with more negative affect tell their negative emotions apart less well (Spearman rho = -0.27, p < 1e-8), 'Needs it': top quarter of negative affect or bottom quarter of differentiation (42% of people; overlap 8%, two different needs), Negative-emotion differentiation (1 minus the mean correlation between negative emotions), Open experience-sampling data: 462 people with 30+ prompts from five studies (archive jmbh/EmotionTimeSeries); person-level summaries only (esm_profiles.json, sim/esm/extract_profiles.py) (+2 more)

### Community 38 - "Answer reliability"
Cohesion: 0.31
Nodes (4): AnswerReliability, _ar(), _person_answers(), test_helping_a_person_who_does_not_know_what_they_feel()

### Community 39 - "Engine entry and commands"
Cohesion: 0.29
Nodes (8): The soulcal engine (original contribution 10), soulcal command line: pytest (28 tests), bench, demo, run, archetypes, support, channels, haptics, anchors, understanding, soulcal — the SOUL-Calibrate engine (engine README), soulcal: decision and personalization layer on any face, voice and text emotion model plus bracelet signals (baseline, fusion, conformal speak/ask/quiet, memory, corrections, disagreement, pattern graph), soulcal understanding command: the understanding layer, people from open ESM data, Astrology reflection layer, Figure 11: understanding layer (fig11_understanding_layer.png), Understanding yourself: the understanding layer (a way in, not a signal; 462 real people; confusion 0.30 -> 0.17, negative affect -10% for people who need it; ~1 prompt a week for people doing well; bridge to a person 12-16%)

### Community 40 - "README: the project at a glance"
Cohesion: 0.33
Nodes (6): anchors.SignatureModel module: voice-and-body signatures from one fixed sentence (enrollment, daily anchor, tagged readings); what changes in the person, Engine demo, 20 synthetic people: week-6 accuracy 0.57 -> 0.77; when speaking 0.68 -> 0.94, False-discovery correction and replication, Personal pattern graph (context, body, expression, astrology reflection layer), soulcal bench: SOUL-Bench ladder B0-B6 on any readings with self-reports, soulcal engine (engine/soulcal, numpy-only Python package)

### Community 41 - "Public approach comparison"
Cohesion: 0.67
Nodes (3): Public approach today: generic speech model + population body norms, nothing personal (0.41, right 52% when speaking), The single voice-and-body reading is right about twice as often as the public approach (0.81 vs 0.41) and 88% vs 52% when it speaks, Problem: weak, highly personal emotion signals (prosody rho=0.02; 32.5-69.3% speaker variance)

## Knowledge Gaps
- **37 isolated node(s):** `soulcal`, `MIT License`, `RinDig (open-source inspiration)`, `Simulation of the loop with synthetic users`, `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 201 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `30 · The understanding layer` connect `Understanding layer concept` to `Voice-and-body signatures`, `Cohort pilot and archetype path`, `Emotional granularity evidence`, `Risks, traps and cold start`, `Engine entry and commands`, `Engine overview and commands`, `Clinical practice`, `Analogous systems`, `Architecture and the closed loop`, `People who don't know what they feel`, `Understanding layer code`, `Understanding results`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `SoulEngine` (e.g. with `soulcal: decision and personalization layer on any face, voice and text emotion model plus bracelet signals (baseline, fusion, conformal speak/ask/quiet, memory, corrections, disagreement, pattern graph)` and `ArchetypeModel`) actually correct?**
  _`SoulEngine` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `soulcal`, `MIT License`, `RinDig (open-source inspiration)` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Speech front end and real-voice check` be split into smaller, more focused modules?**
  _Cohesion score 0.05368421052631579 - nodes in this community are weakly interconnected._
- **Why does `29 — Your voice, your body, your signature: one fixed sentence, three uses` connect `Voice-and-body signatures` to `Speech front end and real-voice check`, `Voice, vibration and the pulse`, `Signature checks (code)`, `Risks, traps and cold start`, `README: the project at a glance`, `Engine overview and commands`, `Clinical practice`, `Active questions and decision rule`, `Enrollment details`, `Understanding layer concept`, `Analogous systems`, `Question budget experiments`, `README: voice, vibration and the loop`, `Architecture and the closed loop`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Should `Voice-and-body signatures` be split into smaller, more focused modules?**
  _Cohesion score 0.058596491228070174 - nodes in this community are weakly interconnected._
- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Engine overview and commands` to `Speech front end and real-voice check`, `Voice-and-body signatures`, `Evaluation: SOUL-Bench`, `Voice, vibration and the pulse`, `Cohort pilot and archetype path`, `Signature checks (code)`, `Engine entry and commands`, `Engine fusion code`, `README: the project at a glance`, `Problem and evidence`, `Enrollment details`, `Question budget experiments`, `Architecture and the closed loop`, `Archetype prototype`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._