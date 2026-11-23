# Graph Report - graph-src  (2026-11-23)

## Corpus Check
- 84 files · ~67,342 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1169 nodes · 3430 edges · 35 communities (32 shown, 3 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 580 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Voice, vibration and the pulse
- Risks, traps and cold start
- Simulation scripts and question budget results
- Speech front end and real-voice check
- Recurring situations and question budget
- Engine overview and commands
- First simulation code
- Voice-and-body signatures
- Cohort pilot and archetype path
- SOUL-Bench code
- Enrollment details
- Engine core code
- Signature checks (code)
- Archetype and channel checks (code)
- Problem and evidence
- Active questions and decision rule
- Architecture and the closed loop
- Engine fusion code
- Engine baseline and conformal code
- Archetype prototype
- Question budget experiments
- Clinical practice
- Engine personal baseline
- Privacy and regulation
- Analogous systems
- README: the project at a glance
- Ideas from prior work
- Authorship
- Incongruence and masking
- Evaluation: SOUL-Bench
- README: voice, vibration and the loop
- README: voice and body
- Misc
- Misc
- Misc

## God Nodes (most connected - your core abstractions)
1. `References` - 60 edges
2. `22 — The engine: code Nightlet can run on its own data` - 59 edges
3. `27 — Voice and vibration: what each is for, and how to integrate them` - 52 edges
4. `05 Active questions` - 51 edges
5. `README: SOUL-Calibrate` - 50 edges
6. `29 — Your voice, your body, your signature: one fixed sentence, three uses` - 49 edges
7. `SoulEngine` - 48 edges
8. `20 — Recurring situations: one answer, every later reading of the same situation` - 47 edges
9. `Reading` - 42 edges
10. `04 Rolling personal baseline` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Ladder of results on free voice notes (synthetic, 5 seeds x 40 people, 4 states): generic 0.44 -> baseline 0.68 -> daily anchor 0.74 -> 1/2/4 tagged readings 0.80/0.82/0.83` --semantically_similar_to--> `test_personal_baseline_and_answers_help_when_the_speaker_dominates()`  [INFERRED] [semantically similar]
  docs/29-voice-signatures.md → realvoice/tests/test_protocol.py
- `SupportPolicy` --implements--> `soulcal support command (when to pulse, synthetic)`  [INFERRED]
  engine/soulcal/support.py → docs/22-engine.md
- `First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/__main__.py
- `When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36` --implemented_by--> `support_demo()`  [INFERRED]
  docs/26-when-to-pulse.md → engine/soulcal/__main__.py
- `anchors_demo()` --implements--> `Engine check (4 seeds x 25 people, two voice notes and one question a day, days 22-42): public approach 0.41 (right when speaking 52%), engine without signature 0.57 (61%), + enrollment and anchor 0.67 (74%), + 3 tagged a week 0.75 (81%), default with answered notes 0.81 (88%); added instead of replacing 0.65 (70%); unsoftened 0.71 (75%, speaks 87%)`  [INFERRED]
  engine/soulcal/__main__.py → docs/29-voice-signatures.md

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
- **Masking detection: words-vs-expression questions and tense recall** — docs_22_engine_masking_questions, engine_examples_demo_words_vs_expression, docs_22_engine_tense_recall, engine_soulcal_engine_soulengine_incongruence, docs_22_engine_quality_gate [INFERRED 0.85]
- **One fixed sentence, three moments: enrollment, daily anchor, tagged reading -> personal signature** — docs_29_voice_signatures_one_fixed_sentence_three_moments, docs_29_voice_signatures_enrollment, docs_29_voice_signatures_daily_anchor, docs_29_voice_signatures_tagged_reading, docs_29_voice_signatures_personal_signature [EXTRACTED 1.00]
- **Signature wired as the engine's voice channel: replace generic voice, soften (temperature 4), body not counted twice, answered voice notes teach it** — docs_29_voice_signatures_feeds_voice_channel, docs_29_voice_signatures_replaces_generic_voice, docs_29_voice_signatures_softened_temperature4, docs_29_voice_signatures_avoid_double_counting_body, docs_29_voice_signatures_answers_teach_signature, engine_soulcal_engine_soulengine [EXTRACTED 1.00]
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]

## Communities (35 total, 3 thin omitted)

### Community 0 - "Voice, vibration and the pulse"
Cohesion: 0.05
Nodes (71): The body triggers, the voice decides, the vibration acts (original contribution 15): voice moments teach body-only moments, voice check-in, pulse tied to live heart rate and resonance breathing, soulcal haptics command (tuning the pulse), Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, 26 — When and how the bracelet should pulse, 20% of eligible moments held out at random: a micro-randomised trial inside the product, Pulse effect: heart-rate and HRV recovery with a pulse minus the person's recovery without one; optional one-tap 'did it help?', One line on screen with the pulse; calm voice off by default (people are often not alone) (+63 more)

### Community 1 - "Risks, traps and cold start"
Cohesion: 0.05
Nodes (67): Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation, What 'precise' means: agreement with the state the person would choose, per reading and per person (not intensity, mixed states or causes yet), Diagnostic drift of language, Face signal risk, Person leakage in evaluation, Non-diagnostic language battery, Persona invariance battery, Safety routing battery (+59 more)

### Community 2 - "Simulation scripts and question budget results"
Cohesion: 0.06
Nodes (31): main(), mean_runs(), main(), aggregate(), fmt(), main(), curves(), main() (+23 more)

### Community 3 - "Speech front end and real-voice check"
Cohesion: 0.06
Nodes (56): E31 First check on real voice: RAVDESS (24 speakers) or any labeled multi-speaker set, emotion2vec+ front end, ready-to-run realvoice/e31_real_voice.py; personal baseline and a few answers per speaker vs generic head and zero-shot scores on held-out recordings, Model-agnostic input: probabilities over four states (basic_emotions_to_states), Audio events (a laugh, a sigh, crying) as a natural next input, CosyVoice (FunAudioLLM): open text-to-speech, the open counterpart for generating speech; only matters for the optional calm voice, not for reading, 28 — Listening well from day one: open speech models as the front end, Check E31: on real voice with emotion2vec+ as front end, the personal baseline and a few answers per speaker beat the generic head and the zero-shot scores on held-out recordings of each speaker, E31 protocol: leave one speaker out; half of the held-out speaker's clips are the calibration pool, half the test; zero-shot, generic head, + personal baseline (unlabeled), + 2/4/8/16 answers, ElevenLabs Scribe (commercial): speech to text in 90+ languages with non-speech event tags; a cloud reference point (ElevenLabs is best known for generating speech, not reading people) (+48 more)

### Community 4 - "Recurring situations and question budget"
Cohesion: 0.07
Nodes (70): Recurring situations (original contribution 8), Ambiguous-moment timing helps when situations recur, Hard daily question budget, Situation memory next to the personal head, Broken guarantee (personal memory changes probabilities), Life change (situation memory), Too many questions, Users stop answering (bridge node) (+62 more)

### Community 5 - "Engine overview and commands"
Cohesion: 0.06
Nodes (56): The soulcal engine (original contribution 10), Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), soulcal archetypes command (future phase, synthetic cohort), soulcal channels command (voice, words, face, body), Concept-to-code map, Conformal set, speak / ask / quiet, daily question budget (SoulEngine.observe); adaptive per-person thresholds (SoulEngine._learn), One-tap "not quite" corrections (SoulEngine.correct), Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking (+48 more)

### Community 6 - "First simulation code"
Cohesion: 0.10
Nodes (30): main(), style(), summarise(), calibrate(), coverage(), decide(), prediction_sets(), _quantile() (+22 more)

### Community 7 - "Voice-and-body signatures"
Cohesion: 0.07
Nodes (31): Voice-and-body signatures (original contribution 17): one fixed sentence for enrollment, daily anchor and tagged readings; wired into the engine as its voice channel (softened, replacing the generic voice reading, body not counted twice) and into the real-voice check, Voice enrollment: three fixed sentences a day; later the same sentence read in a clear state becomes the person's signature, In code: engine/soulcal/anchors.py (SignatureModel.set_anchor), with enrollment and tagged readings, Lexical leakage, The 5-second evening anchor is the cheapest, most valuable feedback (3 evenings a week costs 7-12 points), Signature accuracy week 3 / week 6: light 0.72/0.74, standard 0.75/0.82, fast 0.82/0.86, Answered voice notes teach the signature: a voice note the person answers is also stored as a tagged reading (free speech, noisier, no extra effort), Blood pressure: one more body feature if the bracelet measures it; not assumed here (+23 more)

### Community 8 - "Cohort pilot and archetype path"
Cohesion: 0.07
Nodes (42): Coarse to fine, cohort learning and archetype prototype (original contribution 13), GDPR (voice as personal data), Consent level 2 — research cohort, GDPR, E19 Cohort transfer, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort, A private cohort helps everyone (0.550 -> 0.590 for users never asked) (+34 more)

### Community 9 - "SOUL-Bench code"
Cohesion: 0.10
Nodes (24): Input format: soulcal/schema.py (CSV columns or Reading objects), seconds_per_week(), bench_table(), _only(), _running_average(), _score(), soul_bench(), anchors_demo() (+16 more)

### Community 10 - "Enrollment details"
Cohesion: 0.10
Nodes (37): Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment, Trap: baseline absorbs anomalous days (normalising long stress), Baseline per device, Label-free drift trigger (conformal test martingale), 04 Rolling personal baseline (+29 more)

### Community 11 - "Engine core code"
Cohesion: 0.11
Nodes (17): moon_age_days(), moon_longitude(), moon_phase(), moon_sign(), reflection_factors(), sun_sign(), _utc(), _bh() (+9 more)

### Community 12 - "Signature checks (code)"
Cohesion: 0.11
Nodes (10): The signature inside the engine (4 seeds x 25 people): public approach 0.41/52%, engine without signature 0.57/61%, + enrollment and anchor 0.67/74%, + 3 tagged 0.75/81%, default 0.81/88%; added instead of replacing 0.65/70%; not softened 0.71/75%, anchors_check(), engine_check(), _person(), _reading(), simulate(), _to_reading(), checkin_check() (+2 more)

### Community 13 - "Archetype and channel checks (code)"
Cohesion: 0.15
Nodes (14): app_use_check(), frontend_check(), _score(), sources_check(), EngineConfig, run_stream(), Decision, Profile (+6 more)

### Community 14 - "Problem and evidence"
Cohesion: 0.12
Nodes (27): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Koch et al. 2026 in-the-wild smartphone voice study, Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), Physiological confounders (exercise, caffeine, alcohol, cycle, medication) (+19 more)

### Community 15 - "Active questions and decision rule"
Cohesion: 0.13
Nodes (28): Active questions, Affect labeling (Lieberman et al., 2007), Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+20 more)

### Community 16 - "Architecture and the closed loop"
Cohesion: 0.13
Nodes (21): Reading audit of the language layer, SOUL-Calibrate (original contribution 1): entry calibration, 5-second session anchor, rolling personal baseline, conformal questions, Cold start, 01 Architecture of SOUL-Calibrate, Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Measurement reactivity, 03 Session anchor (5 seconds) (+13 more)

### Community 17 - "Engine fusion code"
Cohesion: 0.13
Nodes (7): Fusion of face, voice, words and body with missing channels (model.FusionHead); personal head shrunk toward a transparent prior (FusionHead.update), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), context_vector(), feature_vector(), FusionHead, prior_weights(), SituationMemory

### Community 18 - "Engine baseline and conformal code"
Cohesion: 0.09
Nodes (5): Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), EMA, calibrate_thresholds(), _js_bits(), _softmax()

### Community 19 - "Archetype prototype"
Cohesion: 0.13
Nodes (10): Archetype, ArchetypeModel, fit(), _js(), _kmeans(), _person(), signature(), synthetic_check() (+2 more)

### Community 20 - "Question budget experiments"
Cohesion: 0.11
Nodes (26): E24 Personalization speed, E25 Burden by preset, E26 Free notes, Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed, Harder engine demo check (week 6: 0.63 none, 0.77 1/day, 0.81 2-3/day), Experiments E24-E26 (presets on real users, answer rate/drop-out, notes vs questions), Failed idea: consensus memory made accuracy worse at every error rate (0.910->0.835, 0.818->0.717, 0.675->0.581) (+18 more)

### Community 21 - "Clinical practice"
Cohesion: 0.19
Nodes (16): Prompt as clinical alarm (alarm fatigue), 12 — What clinical practice already knows, HeartSteps trial, Pulse gates: bracelet worn, no strong movement, at most 3 a day and 90 minutes apart, only in the user's hours (question budget applied to the wrist), Pulse as an intervention to calm, not a stress notification ('pulses when you need to come back to yourself'; no outcome guaranteed, so measure per person), Bos et al. (2022) early warning signals in bipolar disorder, Chromik et al. (2022) alarm fatigue in intensive care, Costache et al. (2025) DBT, alexithymia and emotion awareness (+8 more)

### Community 22 - "Engine personal baseline"
Cohesion: 0.21
Nodes (3): User-chosen question hours (evenings only costs accuracy unless one more question is allowed), PersonalBaseline, Reading

### Community 23 - "Privacy and regulation"
Cohesion: 0.17
Nodes (16): openSMILE eGeMAPS features (88) computed on phone, EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Federated learning with differential privacy (Gboard), Kintsugi case, The medical line: name states, never conditions, Kintsugi: short prompted free-form voice answer (~25 s) screened for depression in 14,898 adults, sensitivity 71% (a short prompted sample carries signal) (+8 more)

### Community 24 - "Analogous systems"
Cohesion: 0.18
Nodes (19): User error in labels, BCI cross-subject/cross-session transfer learning, CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy (+11 more)

### Community 25 - "README: the project at a glance"
Cohesion: 0.16
Nodes (17): anchors.SignatureModel module: voice-and-body signatures from one fixed sentence (enrollment, daily anchor, tagged readings); what changes in the person, Astrology reflection layer, Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue), Coarse to fine and archetypes (shown precision 0.75 day 3, 0.85 week 1 vs 0.55/0.75), README: SOUL-Calibrate, False-discovery correction and replication, Future phase: learn from consenting users as glucose monitors moved from finger-stick to factory calibration, Graphify knowledge graph of the project (1,111 concepts, 3,337 links) (+9 more)

### Community 26 - "Ideas from prior work"
Cohesion: 0.19
Nodes (9): Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Calibration vs representation diagnosis, Integer additive model on bracelet, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study) (+1 more)

### Community 27 - "Authorship"
Cohesion: 0.15
Nodes (13): Transfer of clinical methods (original contribution 4), Emanuele De Bernardis, MIT License, Nightlet SOUL layer proposal (first written 21 November 2026), Strong open speech models as the front end, calibration on top (original contribution 16), What 'precise' means, and eight states (original contribution 12), Private cohort pilot (original contribution 3), Question budget and personalization speed (original contribution 11): light / standard / fast, chosen hours, free notes (+5 more)

### Community 28 - "Incongruence and masking"
Cohesion: 0.20
Nodes (12): Incongruence as a reason to ask (original contribution 9), Masking (words vs face or voice), E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21) (+4 more)

### Community 29 - "Evaluation: SOUL-Bench"
Cohesion: 0.29
Nodes (12): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Split by person and in time, Prompt precision (alarm-fatigue metric) (+4 more)

### Community 30 - "README: voice, vibration and the loop"
Cohesion: 0.22
Nodes (8): SOUL (State Observation & Understanding Layer), How others use voice (Nightlet episodic voice, Amazon Halo Tone, Kintsugi), Closed personal loop, How it works: readings against the personal baseline, personal model + situation memory, conformal set -> speak / ask / quiet, pulse when sure of tension, offer when maybe tense, invite a 5-second voice note when the body is aroused without voice, Nightlet, Session anchor (5 seconds), SOUL-Calibrate: personal calibration, active questions and user-grounded evaluation for emotion-reading systems, Support step: the bracelet pulses only when the reading is sure the person is tense, tuned to their heart and breathing; when the person is not talking, the body can invite a 5-second voice note

### Community 31 - "README: voice and body"
Cohesion: 0.25
Nodes (8): Personal incongruence score (Jensen-Shannon divergence vs personal usual distance), Enrollment (3-7 days): fixed sentences, resting physiology, sliders and one word; later the same sentence read in a clear state becomes the voice-and-body signature, Listening well from day one: open speech models (words via Whisper, Parakeet, Handy, SenseVoice; voice via emotion2vec+, SenseVoice; on the phone, swappable); generic 0.62 -> 0.82+, calibration still adds +0.16 today, +0.08 with much stronger models; E31 ready to run, Tuning the pulse to each person: heartbeat at 80% of the live heart rate (never above 90%); learned resonance breathing (4.5-7/min); live heartbeat 0.72 vs fixed 0.53, learned breathing 0.81 vs 0.71, Voice and body, which matters? Body alone 0.52, voice and words 0.69, together 0.81; voice moments teach body-only moments (0.67 vs 0.52); voice check-in raises tense moments reached 28% -> 46%; never always-on listening, Voice, body and the bracelet: the body triggers, the voice decides, the vibration acts, Your voice, your body, your signature: one fixed sentence, three uses; 0.44 -> 0.68 -> 0.74 -> 0.82 with two tagged readings; voice + body beat either alone; signature shown back; voluntary modes light 0.74 / standard 0.82 / fast 0.86 by week 6, When the bracelet pulses: pulse when sure of tension, offer when unsure, nothing when calm, excited, low or moving; body alone 3% of tense moments vs calibrated 56% at 88% precision; 20% held out

## Knowledge Gaps
- **35 isolated node(s):** `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Rolling baseline recovers after step change (0.581 vs 0.584; fixed 0.541)`, `Baseline per device`, `AI Act Annex III high-risk emotion recognition`, `Persona invariance battery` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 177 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `29 — Your voice, your body, your signature: one fixed sentence, three uses` connect `Voice-and-body signatures` to `Voice, vibration and the pulse`, `Risks, traps and cold start`, `Speech front end and real-voice check`, `Engine overview and commands`, `SOUL-Bench code`, `Enrollment details`, `Signature checks (code)`, `Active questions and decision rule`, `Architecture and the closed loop`, `Question budget experiments`, `Clinical practice`, `Privacy and regulation`, `README: the project at a glance`, `README: voice and body`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `27 — Voice and vibration: what each is for, and how to integrate them` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`27 — Voice and vibration: what each is for, and how to integrate them` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Rolling baseline recovers after step change (0.581 vs 0.584; fixed 0.541)`, `Baseline per device` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Voice, vibration and the pulse` be split into smaller, more focused modules?**
  _Cohesion score 0.0502497796062298 - nodes in this community are weakly interconnected._
- **Why does `27 — Voice and vibration: what each is for, and how to integrate them` connect `Voice, vibration and the pulse` to `Risks, traps and cold start`, `Speech front end and real-voice check`, `Recurring situations and question budget`, `Engine overview and commands`, `Voice-and-body signatures`, `Archetype and channel checks (code)`, `Problem and evidence`, `Clinical practice`, `Privacy and regulation`, `README: voice, vibration and the loop`, `README: voice and body`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `05 Active questions` (e.g. with `A strong front end makes the engine sure more often, so it asks fewer questions (front end and calibration work together)` and `Answered voice notes teach the signature: a voice note the person answers is also stored as a tagged reading (free speech, noisier, no extra effort)`) actually correct?**
  _`05 Active questions` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Risks, traps and cold start` be split into smaller, more focused modules?**
  _Cohesion score 0.05365686944634313 - nodes in this community are weakly interconnected._