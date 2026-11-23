# Graph Report - soul-calibrate  (2026-11-23)

## Corpus Check
- 80 files · ~60,447 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1049 nodes · 3135 edges · 40 communities (36 shown, 4 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 599 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Simulation scripts and question budget results
- Recurring situations and question budget
- Speech front end and real-voice check
- First simulation code
- Engine overview and commands
- Cohort, archetype path and analogies
- Engine concept-to-code map and baseline
- Clinical practice and authorship
- Engine I/O and SOUL-Bench code
- Problem, evidence and masking
- Voice and body checks (code)
- Enrollment
- Engine fusion and words vs expression
- Active questions and decision rule
- Risks of questions
- Question budget experiments
- Vibration products and rhythms
- Archetype prototype
- Analogous systems
- README: the loop and voice check-ins
- Architecture and session anchor
- When the bracelet pulses: evidence
- Ideas from prior work
- Traps and confounders
- Pulse tuning code
- Inspiration and affect grid
- Privacy and regulation
- Voice and body: body triggers, voice decides
- Pattern graph code
- Evaluation: SOUL-Bench
- Claims ledger and working method
- What precise means, eight states
- Astrology utilities
- Fusion of sources
- Haptic tuning check
- Engine state persistence
- Cold start and evaluation pitfalls
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of speaking

## God Nodes (most connected - your core abstractions)
1. `References` - 62 edges
2. `22 — The engine: code Nightlet can run on its own data` - 54 edges
3. `README: SOUL-Calibrate` - 53 edges
4. `27 — Voice and vibration: what each is for, and how to integrate them` - 52 edges
5. `05 Active questions` - 49 edges
6. `20 — Recurring situations: one answer, every later reading of the same situation` - 45 edges
7. `04 Rolling personal baseline` - 41 edges
8. `12 — What clinical practice already knows` - 40 edges
9. `26 — When and how the bracelet should pulse` - 38 edges
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
- **Coarse-to-fine design, its simulation, its code and its experiment** — docs_25_coarse_to_fine_and_archetypes_level_of_detail_per_reading, docs_25_coarse_to_fine_and_archetypes_coarse_to_fine_comparison, sim_results_progressive_one_per_day, sim_results_progressive_two_per_day, docs_16_experiments_e29, readme_coarse_to_fine_and_archetypes, engine_soulcal_detail_level_of_detail [INFERRED 0.85]
- **From personal calibration to needing less of it (CGM path, cohort transfer, pooled head, archetypes)** — docs_11_analogous_systems_cgm_factory_calibration, docs_11_analogous_systems_dexcom_g6, docs_25_coarse_to_fine_and_archetypes_archetypes, docs_25_coarse_to_fine_and_archetypes_reading_on_its_own, docs_16_experiments_e30, docs_25_coarse_to_fine_and_archetypes_pooled_cohort_head, docs_16_experiments_e19, engine_soulcal_archetypes [INFERRED 0.85]
- **When to pulse: calibrated decision, gates, held-out moments and per-person rhythm learning in SupportPolicy** — docs_26_when_to_pulse_pulse_follows_reading_rule, docs_26_when_to_pulse_gates, docs_26_when_to_pulse_held_out_moments, docs_26_when_to_pulse_thompson_sampling, engine_soulcal_support_supportpolicy [EXTRACTED 1.00]
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]
- **The body triggers, the voice decides, the vibration acts: sources ablation, voice teaching body-only moments, voice check-in and per-person pulse tuning** — docs_27_voice_and_vibration_body_triggers_voice_decides_vibration_acts, docs_27_voice_and_vibration_sources_ablation, docs_27_voice_and_vibration_voice_teaches_body_only, docs_27_voice_and_vibration_voice_checkin, docs_27_voice_and_vibration_pulse_tuning_in_code [EXTRACTED 1.00]
- **Calming vibration products surveyed: on-demand vs automatic personal-threshold triggers** — docs_27_voice_and_vibration_doppel, docs_27_voice_and_vibration_emotioncheck, docs_27_voice_and_vibration_nightware, docs_27_voice_and_vibration_lief, docs_27_voice_and_vibration_apollo_neuro, docs_27_voice_and_vibration_touchpoints, docs_27_voice_and_vibration_garmin [EXTRACTED 1.00]
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **Pulse calibrated to the person: live heart rate, interoception and resonance breathing rate, implemented in SupportConfig/SupportPolicy and checked in haptics_sim** — docs_27_voice_and_vibration_calibration_to_live_heart_rate, docs_27_voice_and_vibration_interoception, docs_27_voice_and_vibration_resonance_breathing_rate, engine_soulcal_support_supportconfig, engine_soulcal_support_supportpolicy_breathing_rate, engine_soulcal_haptics_sim_haptics_check [INFERRED 0.85]
- **E31 real-voice check: leave-one-speaker-out protocol on RAVDESS with emotion2vec+ or MFCC encoders, run by realvoice/e31_real_voice.py** — docs_16_experiments_e31, docs_28_speech_front_end_e31_protocol, docs_28_speech_front_end_ravdess, docs_28_speech_front_end_emotion2vec_plus, docs_28_speech_front_end_mfcc_encoder, realvoice_e31_real_voice, realvoice_readme_results_output [EXTRACTED 1.00]
- **Open speech front end feeding the model-agnostic engine: speech to text and speech emotion models produce text and voice probabilities for SoulEngine** — docs_28_speech_front_end_plug_in_pipeline, docs_28_speech_front_end_whisper, docs_28_speech_front_end_parakeet, docs_28_speech_front_end_sensevoice, docs_28_speech_front_end_emotion2vec_plus, docs_22_engine_four_state_adapter, docs_28_speech_front_end_two_signals_one_voice_note [INFERRED 0.85]

## Communities (40 total, 4 thin omitted)

### Community 0 - "Simulation scripts and question budget results"
Cohesion: 0.06
Nodes (32): Coarse-to-fine simulation setup (8 states, 5 seeds x 60 people, 6 situations, 4 readings/day, 28 days), main(), mean_runs(), main(), aggregate(), fmt(), main(), curves() (+24 more)

### Community 1 - "Recurring situations and question budget"
Cohesion: 0.06
Nodes (71): Label-free drift trigger (conformal test martingale), Behavioural situation-level drift trigger (repeated corrections), Ambiguous-moment timing helps when situations recur, Hard daily question budget, Cold start: 10-20 labels for the head; head adds 2-8 points between 5 and 40 answers, Forgetting: incremental updates without losing the past, Situation memory next to the personal head, Broken guarantee (personal memory changes probabilities) (+63 more)

### Community 2 - "Speech front end and real-voice check"
Cohesion: 0.07
Nodes (49): E31 First check on real voice: RAVDESS (24 speakers) or any labeled multi-speaker set, emotion2vec+ front end, ready-to-run realvoice/e31_real_voice.py; personal baseline and a few answers per speaker vs generic head and zero-shot scores on held-out recordings, Stronger speech front ends: how much calibration still adds (channels_sim.frontend_check), Real-voice check with an open speech-emotion model (E31), outside the engine (realvoice/e31_real_voice.py), Synthetic checks of sources (voice, words, face, body), app use, voice check-ins and pulse tuning in code (channels_sim, haptics_sim), Audio events (a laugh, a sigh, crying) as a natural next input, CosyVoice (FunAudioLLM): open text-to-speech, the open counterpart for generating speech; only matters for the optional calm voice, not for reading, 28 — Listening well from day one: open speech models as the front end, Check E31: on real voice with emotion2vec+ as front end, the personal baseline and a few answers per speaker beat the generic head and the zero-shot scores on held-out recordings of each speaker (+41 more)

### Community 3 - "First simulation code"
Cohesion: 0.10
Nodes (30): main(), style(), summarise(), calibrate(), coverage(), decide(), prediction_sets(), _quantile() (+22 more)

### Community 4 - "Engine overview and commands"
Cohesion: 0.06
Nodes (48): soulcal archetypes command (future phase, synthetic cohort), soulcal channels command (voice, words, face, body), Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, 22 — The engine: code Nightlet can run on its own data, Engine tests (21), incl. loop beats today and no supported moon pattern when none planted, Four factor layers: context, body, expression, reflection, Guardrail: Fisher exact test + Benjamini-Hochberg FDR 10%, Model-agnostic input: probabilities over four states (basic_emotions_to_states) (+40 more)

### Community 5 - "Cohort, archetype path and analogies"
Cohesion: 0.07
Nodes (42): CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), E19 Cohort transfer, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort, A private cohort helps everyone (0.550 -> 0.590 for users never asked), E. Cohort transfer (0.550 -> 0.590 with 50 users; full loop 0.652), Comparison: today -> personal baseline -> cohort answers -> full loop (+34 more)

### Community 6 - "Engine concept-to-code map and baseline"
Cohesion: 0.08
Nodes (14): Concept-to-code map, Explanation: evidence per channel for each reading (Decision.contributions), Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Pulse tuned to the person in code: heartbeat at 80% of the live heart rate (never above 90%), breathing at the learned resonance rate (SupportConfig.heartbeat_ratio, learn_resonance), When and how the bracelet pulses in code (support.SupportPolicy): pulse when sure, offer when unsure, gates, rhythm learned per person with held-out moments, Wide questions when more than three states are plausible (EngineConfig.ask_wide), User-chosen question hours (evenings only costs accuracy unless one more question is allowed), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80) (+6 more)

### Community 7 - "Clinical practice and authorship"
Cohesion: 0.11
Nodes (31): Transfer of clinical methods, Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Strong open speech models as the front end, calibration on top (original contribution 16): words and voice from open models on the phone, personal layer measured on real voice by a ready-to-run experiment, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot (+23 more)

### Community 8 - "Engine I/O and SOUL-Bench code"
Cohesion: 0.13
Nodes (18): bench_table(), _only(), _running_average(), _score(), soul_bench(), archetypes_demo(), bench(), demo() (+10 more)

### Community 9 - "Problem, evidence and masking"
Cohesion: 0.12
Nodes (26): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), 07 Fusion of sources (+18 more)

### Community 10 - "Voice and body checks (code)"
Cohesion: 0.20
Nodes (15): app_use_check(), checkin_check(), frontend_check(), _mask(), _score(), sources_check(), EngineConfig, channels_demo() (+7 more)

### Community 11 - "Enrollment"
Cohesion: 0.19
Nodes (26): Cold start, Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Measurement reactivity, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment (+18 more)

### Community 12 - "Engine fusion and words vs expression"
Cohesion: 0.12
Nodes (9): Physiological prior (HR up, HRV down = arousal), learned away per person, Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits(), _softmax(), context_vector(), feature_vector() (+1 more)

### Community 13 - "Active questions and decision rule"
Cohesion: 0.16
Nodes (24): Active questions, Affect labeling (Lieberman et al., 2007), Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+16 more)

### Community 14 - "Risks of questions"
Cohesion: 0.18
Nodes (23): 5-10% of questions at random ordinary moments (selection bias), Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, Selection bias (questions only at anomalous moments), Claims ledger (days 1-30), 16 — Experiment plan: where it works and where it does not, E11 Leading questions, E12 Selection bias, E13 Physiological confounders (+15 more)

### Community 15 - "Question budget experiments"
Cohesion: 0.11
Nodes (26): E24 Personalization speed, E25 Burden by preset, E26 Free notes, Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed, Harder engine demo check (week 6: 0.63 none, 0.77 1/day, 0.81 2-3/day), Experiments E24-E26 (presets on real users, answer rate/drop-out, notes vs questions), Failed idea: consensus memory made accuracy worse at every error rate (0.910->0.835, 0.818->0.717, 0.675->0.581) (+18 more)

### Community 16 - "Vibration products and rhythms"
Cohesion: 0.13
Nodes (23): HRV biofeedback (Goessl et al., 2017), Slow heartbeat rhythm: heartbeat-like vibration at 80% of the person's heart rate at that moment, never faster, Apollo Neuro: on-demand or scheduled patterned waves by mode (calm, sleep, focus); small double-blind placebo-controlled crossover HRV trials, doppel: on-demand heartbeat-like vibration slower than resting heart rate; smaller arousal rise and less anxiety before a speech (Azevedo et al., 2017), EmotionCheck (research): false slow heart-rate feedback on the wrist during a stress task; 67 participants, anxiety regulated (Costa et al., 2017), Garmin: stress from HRV while still, relax reminder on high spikes, guided breathing (6 s in, 6 s out), How others use vibration: triggers, patterns and evidence across calming wearables, Lief Smart Patch: automatic vibration when HRV reaches a preset level, then 3-minute HRV biofeedback breathing guidance; pilot of 14 adults (+15 more)

### Community 17 - "Archetype prototype"
Cohesion: 0.16
Nodes (12): Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start, Archetype demo setup: 24 synthetic people (3 types x 8), 4-day label-free signature, 3 archetypes, pooled-head control, up to 1 question a day, 10 seeds, Archetype, ArchetypeModel, fit(), _js(), _kmeans() (+4 more)

### Community 18 - "Analogous systems"
Cohesion: 0.16
Nodes (23): Fitbit Body Response, BCI cross-subject/cross-session transfer learning, 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy, Speaker recognition enrollment, Tazarv et al. (2023) stress detector with ask-when agent (+15 more)

### Community 19 - "README: the loop and voice check-ins"
Cohesion: 0.13
Nodes (21): SOUL (State Observation & Understanding Layer), E33: voice check-ins at body-only moments with an aroused body (response rate, tense moments reached, felt intrusiveness), Voice check-in: at a body-only moment with an aroused body and possible tension, invite a 5-second voice note, at most once a day (tense moments reached 28% -> 46% with ~1.9 invitations a week), Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Closed personal loop, Decision with a guarantee (speak / ask / stay quiet), README: SOUL-Calibrate, Graphify knowledge graph of the project (980 concepts, 2,910 links) (+13 more)

### Community 20 - "Architecture and session anchor"
Cohesion: 0.13
Nodes (18): 01 Architecture of SOUL-Calibrate, 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, Lexical leakage, Signal quality check (HNR, voice detected), Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population (+10 more)

### Community 21 - "When the bracelet pulses: evidence"
Cohesion: 0.15
Nodes (13): When the bracelet pulses (original contribution 14): pulse follows the reading decision, held-out moments, rhythm learned per person, Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), 26 — When and how the bracelet should pulse, 20% of eligible moments held out at random: a micro-randomised trial inside the product, Pulse effect: heart-rate and HRV recovery with a pulse minus the person's recovery without one; optional one-tap 'did it help?', One line on screen with the pulse; calm voice off by default (people are often not alone), Interoception: the calming effect of an artificial heartbeat depends on how well people perceive their own body, so it is measured per person, Voice is an input: the person talks to the app; the bracelet does not speak (haptic core and sensor); the calm voice is an optional line of audio from the phone, off by default (+5 more)

### Community 22 - "Ideas from prior work"
Cohesion: 0.17
Nodes (8): Calibration vs representation diagnosis, Integer additive model on bracelet, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study), sentineledge-core repository

### Community 23 - "Traps and confounders"
Cohesion: 0.15
Nodes (16): Trap: baseline absorbs anomalous days (normalising long stress), Physiological confounders (exercise, caffeine, alcohol, cycle, medication), No strong emotion without neutral alternative; randomised option order, Rule out movement (accelerometer) before interpreting heart rate, 10 — Risks and failure modes, Face signal risk, Leading questions, Measurement reactivity (+8 more)

### Community 24 - "Pulse tuning code"
Cohesion: 0.18
Nodes (5): Rhythm chosen per person by Thompson sampling on the measured effect (SupportPolicy), Pulse tuning in support.py: slow heartbeat at 80% of the current heart rate, never above 90%; breathing pacer starts at 6/min and learns resonance rate by Thompson sampling over 4.5-7 on a separate random stream, _Arm, Support, SupportPolicy

### Community 25 - "Inspiration and affect grid"
Cohesion: 0.17
Nodes (15): RinDig (open-source inspiration), RinDig open-source projects (inspiration for docs/14 and docs/17), Diagnostic drift of language, Affect Grid, AuditEngine (RinDig), 14 — Reading audit: testing the words, not only the model, Non-diagnostic language battery, Persona invariance battery (+7 more)

### Community 26 - "Privacy and regulation"
Cohesion: 0.21
Nodes (13): EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Federated learning with differential privacy (Gboard), Kintsugi case, The medical line: name states, never conditions, Kintsugi: short prompted free-form voice answer (~25 s) screened for depression in 14,898 adults, sensitivity 71% (a short prompted sample carries signal), Behavioral Health Business (2026) Kintsugi closes (+5 more)

### Community 27 - "Voice and body: body triggers, voice decides"
Cohesion: 0.23
Nodes (14): When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, Amazon Halo Tone: always-on band microphones analysing tone of voice; criticised for privacy, microphones removed, line discontinued 2023 (always-on listening costs trust), Bracelet always on, app used in a share of moments: accuracy 0.77/0.69/0.62/0.51 at 100/50/25/10% app use, 27 — Voice and vibration: what each is for, and how to integrate them, How it fits together: bracelet reads body vs baseline; voice and words give direction and teach body-only moments; voice-note invitation on aroused body; pulse tied to heart or breathing when sure of tension; recovery on held-out moments tunes rhythm and rate, How others use voice (Nightlet episodic voice, Amazon Halo Tone, Kintsugi), The less the person talks, the fewer tense moments the pulse can reach (76% -> 13%), while pulse precision stays high: the rule waits rather than guessing, NightWare (FDA De Novo, Breakthrough Device): automatic vibration from heart rate and movement during sleep against a per-person threshold, interrupting PTSD nightmares (+6 more)

### Community 28 - "Pattern graph code"
Cohesion: 0.20
Nodes (6): find_patterns(), Link, report(), _table(), _time_of_day(), write()

### Community 29 - "Evaluation: SOUL-Bench"
Cohesion: 0.24
Nodes (13): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time (+5 more)

### Community 30 - "Claims ledger and working method"
Cohesion: 0.22
Nodes (9): 17 — Roadmap and governance, icm-architect (RinDig), Provenance classes (MEASURED_REAL_USERS, MEASURED_PUBLIC_DATA, SIMULATED, PLANNED_NOT_MEASURED), Stage 0 — Foundations, Stage 4 — Product, Provenance: SIMULATED, RinDig icm-architect, Section: Inspiration from other open-source projects (14-reading-audit, 17-roadmap-and-governance) (+1 more)

### Community 31 - "What precise means, eight states"
Cohesion: 0.24
Nodes (12): E27 Four vs eight states, E28 Answers needed by granularity, 24 — What "precise" means, and what happens with eight states, Eight states on the valence x arousal circumplex (intermediate states; chance 0.125), Experiments E27-E28 (four vs eight agreement and within-one; answers needed per user), Old question rule (ask only when 2-3 plausible) almost never fires with eight states (1.2 questions, 0.324), Eight states need ~50% more answers and ~twice the time (0.90 in 12 days instead of 8 at 2/day), Wide-question fix: offer the 3 most likely when more are plausible (ask_wide; 0.737 at 1/day, 0.841 at 2/day) (+4 more)

### Community 32 - "Astrology utilities"
Cohesion: 0.32
Nodes (7): moon_age_days(), moon_longitude(), moon_phase(), moon_sign(), reflection_factors(), sun_sign(), _utc()

### Community 33 - "Fusion of sources"
Cohesion: 0.19
Nodes (11): Hypotheses from words and voice; body sets intensity, Words/voice decide state, body sets intensity, Quality gate: no question from body signals alone (EngineConfig.ask_needs_expression), Sources alone and together: body 0.52 (never speaks), voice 0.60, words 0.66, voice+words 0.69, voice+words+body 0.81 (speaks 58%, right 0.93), all four 0.82, B. Bracelet always on, app in a share of moments: body-only moments 0.67/0.61/0.52 at 50/25/10%; tense moments reached 76/45/27/13%, Voice, words, face and body (synthetic people), D. Stronger speech front ends: generic 0.62/0.74/0.82/0.91 vs with personal calibration 0.77/0.85/0.90/0.96 (gain +0.16/+0.11/+0.08/+0.05) as clarity is multiplied x1.5/x2/x3, personal habits unchanged, Channels setup: engine demo people, 5 seeds x 20 people, up to 1 question a day, 6 weeks, scored on weeks 5-6 before learning (+3 more)

### Community 34 - "Haptic tuning check"
Cohesion: 0.31
Nodes (10): Haptics synthetic check (assumed effects): heartbeat at 80% of live HR 0.72 vs fixed 60/min 0.53 vs 80% of resting HR 0.35; learned resonance breathing 0.81 in last 8 moments vs fixed 6/min 0.71, Tuning the pulse to each person (synthetic; the effects are assumptions from the literature), Rhythm results: fixed 60/min 0.53 (3.3% faster than the heart), 80% of resting HR 0.35, 80% of live HR 0.72, fixed 6/min breathing 0.71, learned resonance 0.73 (0.81 last 8), rhythm and rate learned 0.73 (0.81), Haptics setup: 5 seeds x 200 people, 24 tense moments each; effect = calming effect of one pulse (1.0 = full), _add(), breathing_effect(), haptics_check(), heartbeat_effect() (+2 more)

### Community 36 - "Cold start and evaluation pitfalls"
Cohesion: 0.27
Nodes (11): Cold start, Person leakage in evaluation, Before the interview: synthetic simulation of E1/E2/E3/E4/E9/E19/E20-like experiments, CREMA-D dataset, E1 Person normalisation vs none, E14 Person leakage, E2 Answers to accuracy curve, E4 Conformal set as options (+3 more)

## Knowledge Gaps
- **37 isolated node(s):** `Claims ledger (days 1-30)`, `MSP-Podcast dataset`, `MIT License`, `Defaults tuned on synthetic people (thresholds, budget, bandwidth) need re-tuning on real data`, `Astrology reflection layer` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 158 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Engine overview and commands` to `Recurring situations and question budget`, `Speech front end and real-voice check`, `Cohort, archetype path and analogies`, `Engine concept-to-code map and baseline`, `Clinical practice and authorship`, `Problem, evidence and masking`, `Enrollment`, `Engine fusion and words vs expression`, `Active questions and decision rule`, `Question budget experiments`, `Archetype prototype`, `README: the loop and voice check-ins`, `Architecture and session anchor`, `When the bracelet pulses: evidence`, `Ideas from prior work`, `Inspiration and affect grid`, `Voice and body: body triggers, voice decides`, `Evaluation: SOUL-Bench`, `What precise means, eight states`, `Fusion of sources`, `Engine state persistence`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `README: SOUL-Calibrate` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`README: SOUL-Calibrate` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Claims ledger (days 1-30)`, `MSP-Podcast dataset`, `MIT License` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Simulation scripts and question budget results` be split into smaller, more focused modules?**
  _Cohesion score 0.06426906426906427 - nodes in this community are weakly interconnected._
- **Why does `README: SOUL-Calibrate` connect `README: the loop and voice check-ins` to `Simulation scripts and question budget results`, `Recurring situations and question budget`, `Speech front end and real-voice check`, `Engine overview and commands`, `Cohort, archetype path and analogies`, `Clinical practice and authorship`, `Problem, evidence and masking`, `Voice and body checks (code)`, `Risks of questions`, `Question budget experiments`, `Analogous systems`, `Architecture and session anchor`, `When the bracelet pulses: evidence`, `Inspiration and affect grid`, `Voice and body: body triggers, voice decides`, `Evaluation: SOUL-Bench`, `What precise means, eight states`, `Fusion of sources`, `Haptic tuning check`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `27 — Voice and vibration: what each is for, and how to integrate them` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`27 — Voice and vibration: what each is for, and how to integrate them` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Recurring situations and question budget` be split into smaller, more focused modules?**
  _Cohesion score 0.06317907444668008 - nodes in this community are weakly interconnected._