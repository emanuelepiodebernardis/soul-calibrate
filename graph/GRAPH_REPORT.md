# Graph Report - soul-calibrate  (2026-11-23)

## Corpus Check
- 84 files · ~63,258 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1111 nodes · 3337 edges · 45 communities (42 shown, 3 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 638 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Simulation scripts and question budget results
- Recurring situations and question budget
- Voice-and-body signatures
- Risks, traps and cold start
- Speech front end and real-voice check
- Cohort, archetype path and analogies
- First simulation code
- Engine concept-to-code map
- Archetype and channel checks (code)
- Engine core code
- When the bracelet pulses: evidence
- SOUL-Bench code
- Question budget experiments
- Active questions and decision rule
- Enrollment details
- Claims ledger and inspiration
- Engine personal baseline
- Problem and evidence
- Clinical practice
- Architecture
- Personal pattern graph
- Authorship
- Ideas from prior work
- Archetype prototype
- Analogous systems
- What precise means, eight states
- Vibration products and rhythms
- Fusion of sources
- Privacy and regulation
- Engine overview
- Haptic tuning check
- Voice check-ins: body triggers, voice decides
- Astrology utilities
- Evaluation: SOUL-Bench
- Engine commands
- Pulse tuning code
- Incongruence and masking
- Engine fusion code
- Biofeedback and vibration evidence
- README: voice, vibration and the loop
- Reading audit
- Model-agnostic input
- Demo: accuracy by week
- Demo: accuracy when speaking
- Demo: share of speaking

## God Nodes (most connected - your core abstractions)
1. `References` - 62 edges
2. `README: SOUL-Calibrate` - 59 edges
3. `22 — The engine: code Nightlet can run on its own data` - 56 edges
4. `27 — Voice and vibration: what each is for, and how to integrate them` - 53 edges
5. `05 Active questions` - 50 edges
6. `20 — Recurring situations: one answer, every later reading of the same situation` - 45 edges
7. `04 Rolling personal baseline` - 42 edges
8. `12 — What clinical practice already knows` - 41 edges
9. `Experiment plan E1-E36 (falsifiable)` - 38 edges
10. `26 — When and how the bracelet should pulse` - 38 edges

## Surprising Connections (you probably didn't know these)
- `Ladder of results on free voice notes (synthetic, 5 seeds x 40 people, 4 states): generic 0.44 -> baseline 0.68 -> daily anchor 0.74 -> 1/2/4 tagged readings 0.80/0.82/0.83` --semantically_similar_to--> `test_personal_baseline_and_answers_help_when_the_speaker_dominates()`  [INFERRED] [semantically similar]
  docs/29-voice-signatures.md → realvoice/tests/test_protocol.py
- `soulcal archetypes command (future phase, synthetic cohort)` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `First synthetic archetype check: 24 consenting synthetic people of three types (serious face, flat voice, masks with words), 6 weeks, 10 seeds; generic vs pooled vs archetype start` --implemented_by--> `archetypes_demo()`  [INFERRED]
  docs/25-coarse-to-fine-and-archetypes.md → engine/soulcal/__main__.py
- `soulcal support command (when to pulse, synthetic)` --implemented_by--> `support_demo()`  [INFERRED]
  docs/22-engine.md → engine/soulcal/__main__.py
- `When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36` --implemented_by--> `support_demo()`  [INFERRED]
  docs/26-when-to-pulse.md → engine/soulcal/__main__.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three sub-problems and their modules** — docs_00_problem_cold_start, docs_00_problem_moving_reference, docs_00_problem_missing_labels, docs_02_enrollment_entry_calibration, docs_04_rolling_baseline_rolling_personal_baseline, docs_05_active_questions_active_questions [EXTRACTED 1.00]
- **SOUL-Calibrate closed personal loop** — docs_02_enrollment_entry_calibration, docs_03_session_anchor_session_anchor, docs_04_rolling_baseline_rolling_personal_baseline, docs_06_personal_model_personal_head, docs_01_architecture_conformal_decision, docs_05_active_questions_active_questions, docs_01_architecture_closed_loop_update [EXTRACTED 1.00]
- **What precise means and eight states across README, SOUL-Bench, E27-E28 and wide questions** — readme_what_precise_means_eight_states, docs_08_evaluation_soul_bench_what_precise_means, docs_16_experiments_e27, docs_16_experiments_e28, docs_22_engine_wide_questions, docs_24_what_precise_means_eight_states [INFERRED 0.85]
- **New problems of personalization: broken guarantee and life change, with experiments E22/E23 and simulation H** — docs_10_risks_broken_guarantee, docs_10_risks_life_change, docs_16_experiments_e22, docs_16_experiments_e23, docs_18_simulation_new_problems [INFERRED 0.85]
- **Reading audit test batteries** — docs_14_reading_audit_reading_audit, docs_14_reading_audit_persona_invariance, docs_14_reading_audit_uncertainty_honesty, docs_14_reading_audit_non_diagnostic_language, docs_14_reading_audit_sycophancy, docs_14_reading_audit_separation_of_layers, docs_14_reading_audit_safety_routing [EXTRACTED 1.00]
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
- **Pattern graph statistical guardrails against chance moon links** — docs_22_engine_fdr_correction, docs_22_engine_replication_split, docs_22_engine_supported_vs_exploratory, docs_22_engine_moon_links_exploratory [EXTRACTED 1.00]
- **Evidence-based governance (claims ledger, provenance, evidence-before-done)** — docs_17_roadmap_and_governance_claims_ledger, docs_17_roadmap_and_governance_provenance_classes, docs_13_ideas_from_prior_work_claim_evidence_map, docs_13_ideas_from_prior_work_evidence_before_done, docs_17_roadmap_and_governance_numbered_stages, docs_17_roadmap_and_governance_decision_log [INFERRED 0.85]
- **One fixed sentence, three moments: enrollment, daily anchor, tagged reading -> personal signature** — docs_29_voice_signatures_one_fixed_sentence_three_moments, docs_29_voice_signatures_enrollment, docs_29_voice_signatures_daily_anchor, docs_29_voice_signatures_tagged_reading, docs_29_voice_signatures_personal_signature [EXTRACTED 1.00]
- **SignatureModel pipeline: enrollment, anchor, tagged readings, probabilities for the voice channel, difference shown back** — engine_soulcal_anchors_signaturemodel_add_enrollment, engine_soulcal_anchors_signaturemodel_set_anchor, engine_soulcal_anchors_signaturemodel_add_tagged, engine_soulcal_anchors_signaturemodel_proba, engine_soulcal_anchors_signaturemodel_difference [INFERRED 0.85]

## Communities (45 total, 3 thin omitted)

### Community 0 - "Simulation scripts and question budget results"
Cohesion: 0.06
Nodes (35): main(), mean_runs(), main(), aggregate(), fmt(), main(), curves(), main() (+27 more)

### Community 1 - "Recurring situations and question budget"
Cohesion: 0.05
Nodes (77): Label-free drift trigger (conformal test martingale), Behavioural situation-level drift trigger (repeated corrections), Ambiguous-moment timing helps when situations recur, Hard daily question budget, Forgetting: incremental updates without losing the past, Situation memory next to the personal head, Federated learning with differential privacy (Gboard), Broken guarantee (personal memory changes probabilities) (+69 more)

### Community 2 - "Voice-and-body signatures"
Cohesion: 0.07
Nodes (35): Voice-and-body signatures (original contribution 17): one fixed sentence for enrollment, daily anchor and tagged readings; each person's way of showing a state learned and shown back, Koch et al. 2026 in-the-wild smartphone voice study, Voice enrollment: three fixed sentences a day; later the same sentence read in a clear state becomes the person's signature, 03 Session anchor (5 seconds), openSMILE eGeMAPS features (88) computed on phone, In code: engine/soulcal/anchors.py (SignatureModel.set_anchor), with enrollment and tagged readings, Lexical leakage, Voice-and-body signatures in code (anchors.SignatureModel, .difference()): enrollment, daily anchor, tagged readings; what changes in the person (+27 more)

### Community 3 - "Risks, traps and cold start"
Cohesion: 0.07
Nodes (60): Cold start, Measurement reactivity, Trap: baseline absorbs anomalous days (normalising long stress), Physiological confounders (exercise, caffeine, alcohol, cycle, medication), No strong emotion without neutral alternative; randomised option order, 5-10% of questions at random ordinary moments (selection bias), Cold start: 10-20 labels for the head; head adds 2-8 points between 5 and 40 answers, Checks: gain of voice over words (B4 vs B1), conflict accuracy, per-source ablation (+52 more)

### Community 4 - "Speech front end and real-voice check"
Cohesion: 0.07
Nodes (49): Stronger speech front ends: how much calibration still adds (channels_sim.frontend_check), Real-voice check with an open speech-emotion model (E31), outside the engine (realvoice/e31_real_voice.py), Audio events (a laugh, a sigh, crying) as a natural next input, CosyVoice (FunAudioLLM): open text-to-speech, the open counterpart for generating speech; only matters for the optional calm voice, not for reading, 28 — Listening well from day one: open speech models as the front end, Check E31: on real voice with emotion2vec+ as front end, the personal baseline and a few answers per speaker beat the generic head and the zero-shot scores on held-out recordings of each speaker, E31 protocol: leave one speaker out; half of the held-out speaker's clips are the calibration pool, half the test; zero-shot, generic head, + personal baseline (unlabeled), + 2/4/8/16 answers, ElevenLabs Scribe (commercial): speech to text in 90+ languages with non-speech event tags; a cloud reference point (ElevenLabs is best known for generating speech, not reading people) (+41 more)

### Community 5 - "Cohort, archetype path and analogies"
Cohesion: 0.07
Nodes (47): CGM: from user calibration to factory calibration, Dexcom G6 (first factory-calibrated real-time CGM), Speaker recognition enrollment, E29 Level of detail per reading, E30 Archetypes vs one head pooled over the cohort, Personal incongruence score (Jensen-Shannon divergence vs personal usual distance), Level of detail per reading in code (detail.level_of_detail): main state until the fine one is sure, for any model with finer labels, Label-free archetype signature from the first 4 days (usual look of each channel, rate of words-expression disagreement), grouped by k-means (+39 more)

### Community 6 - "First simulation code"
Cohesion: 0.11
Nodes (26): main(), style(), summarise(), decide(), make_population(), _neighbour(), SimConfig, state_from_affect() (+18 more)

### Community 7 - "Engine concept-to-code map"
Cohesion: 0.07
Nodes (12): Concept-to-code map, All engine state in a small JSON file on the phone, Physiological prior (HR up, HRV down = arousal), learned away per person, Personalization speed presets, chosen question hours, free notes (PRESETS, EngineConfig.question_hours, SoulEngine.note), Learned channel weights (face 0.51, voice 0.59, words 0.73; start 0.50/0.60/0.80), EMA, SoulEngine, context_vector() (+4 more)

### Community 8 - "Archetype and channel checks (code)"
Cohesion: 0.18
Nodes (18): _person(), synthetic_check(), app_use_check(), checkin_check(), frontend_check(), _mask(), _score(), sources_check() (+10 more)

### Community 9 - "Engine core code"
Cohesion: 0.10
Nodes (9): _bh(), find_patterns(), Link, report(), _table(), _time_of_day(), to_graph(), write() (+1 more)

### Community 10 - "When the bracelet pulses: evidence"
Cohesion: 0.09
Nodes (18): When the bracelet pulses (original contribution 14): pulse follows the reading decision, held-out moments, rhythm learned per person, Breathing pacer: vibration rising and fading at about 6 breaths a minute (HRV biofeedback pace), 26 — When and how the bracelet should pulse, 20% of eligible moments held out at random: a micro-randomised trial inside the product, Pulse effect: heart-rate and HRV recovery with a pulse minus the person's recovery without one; optional one-tap 'did it help?', One line on screen with the pulse; calm voice off by default (people are often not alone), When-to-pulse synthetic check: body alone helps 3% of tense moments (51% of pulses at excitement), generic reading 16%, calibrated decision 56-57% at 86-88% precision; learned rhythm 0.41 vs 0.36, Interoception: the calming effect of an artificial heartbeat depends on how well people perceive their own body, so it is measured per person (+10 more)

### Community 11 - "SOUL-Bench code"
Cohesion: 0.14
Nodes (19): bench_table(), _running_average(), _score(), soul_bench(), archetypes_demo(), bench(), channels_demo(), demo() (+11 more)

### Community 12 - "Question budget experiments"
Cohesion: 0.10
Nodes (29): Prompt as clinical alarm (alarm fatigue), E24 Personalization speed, E25 Burden by preset, E26 Free notes, Ambiguous moments beat random moments at every budget (0.92 vs ~0.80 plateau), 23 — How many questions: budget, timing and personalization speed, Harder engine demo check (week 6: 0.63 none, 0.77 1/day, 0.81 2-3/day), Experiments E24-E26 (presets on real users, answer rate/drop-out, notes vs questions) (+21 more)

### Community 13 - "Active questions and decision rule"
Cohesion: 0.17
Nodes (23): Active questions, Affect labeling (Lieberman et al., 2007), Class-conditional (per-state) conformal calibration, Conformal prediction set as question options, Clinical skills training: naming emotions (DBT), 05 Active questions, Emotional granularity (Hoemann, Barrett & Quigley, 2021), Just-in-time adaptive intervention (JITAI) framework (+15 more)

### Community 14 - "Enrollment details"
Cohesion: 0.22
Nodes (24): Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin), 02 Enrollment (entry calibration), Ihori et al. 2025 in-context personalization (NTT), Islam & Washington self-supervised personal pre-training, Meta-PerSER (Interspeech 2025), Triantafyllopoulos et al. 2022 speaker enrolment, Baseline per device, 04 Rolling personal baseline (+16 more)

### Community 15 - "Claims ledger and inspiration"
Cohesion: 0.16
Nodes (16): RinDig (open-source inspiration), RinDig open-source projects (inspiration for docs/14 and docs/17), Affect Grid, AuditEngine (RinDig), 14 — Reading audit: testing the words, not only the model, Self-Assessment Manikin, 17 — Roadmap and governance, icm-architect (RinDig) (+8 more)

### Community 16 - "Engine personal baseline"
Cohesion: 0.21
Nodes (5): PersonalBaseline, _only(), _softmax(), factors_for(), Reading

### Community 17 - "Problem and evidence"
Cohesion: 0.18
Nodes (18): Barrett et al. 2019 (faces not reliable emotion read-outs), 00 The problem, Fisher, Medaglia & Jeronimus 2018 (group-to-individual generalisability), Audio-language models follow words not voice (LISTEN, VoxParadox), Missing labels, Moving reference (people change over weeks), 07 Fusion of sources, Late fusion with missing-modality handling (+10 more)

### Community 18 - "Clinical practice"
Cohesion: 0.19
Nodes (13): Alarm fatigue (prompts), 12 — What clinical practice already knows, HeartSteps trial, Pulse as an intervention to calm, not a stress notification ('pulses when you need to come back to yourself'; no outcome guaranteed, so measure per person), Bos et al. (2022) early warning signals in bipolar disorder, Chromik et al. (2022) alarm fatigue in intensive care, Costache et al. (2025) DBT, alexithymia and emotion awareness, Klasnja et al. (2019) HeartSteps micro-randomized trial (+5 more)

### Community 19 - "Architecture"
Cohesion: 0.14
Nodes (15): 01 Architecture of SOUL-Calibrate, Signal quality check (HNR, voice detected), Personal head (per-user, on-device), Labels weighted by answer reliability, Shrinkage toward population, GDPR (voice as personal data), User error in labels, Audio quality check gates questions (+7 more)

### Community 20 - "Personal pattern graph"
Cohesion: 0.18
Nodes (15): Four factor layers: context, body, expression, reflection, Guardrail: Fisher exact test + Benjamini-Hochberg FDR 10%, Moon links significant on all data but failed correction and replication (no planted effect), Personal pattern graph (factor -> state links per person), Pattern graph written in project-map format (graph/build_map.py), Guardrail: discovery on first half, replication on second half (same direction), Supported vs exploratory links (exploratory never shown as finding), Personal patterns: demo-user (+7 more)

### Community 21 - "Authorship"
Cohesion: 0.31
Nodes (15): Transfer of clinical methods, Emanuele De Bernardis, Incongruence as a reason to ask (original contribution), MIT License, Nightlet SOUL layer proposal, Strong open speech models as the front end, calibration on top (original contribution 16): words and voice from open models on the phone, personal layer measured on real voice by a ready-to-run experiment, Reuse of author's prior research (drift, conformal martingales, integer on-device inference, evidence maps), Private cohort pilot (+7 more)

### Community 22 - "Ideas from prior work"
Cohesion: 0.20
Nodes (8): Calibration vs representation diagnosis, Integer additive model on bracelet, Assist_CLI-V2 repository, 13 — Ideas reused from the author's prior work, efficient-on-device-ai repository, IDS-KAN repository, kan-ids-v2 repository (KAN-IDS drift-adaptation study), sentineledge-core repository

### Community 23 - "Archetype prototype"
Cohesion: 0.19
Nodes (7): Archetype demo setup: 24 synthetic people (3 types x 8), 4-day label-free signature, 3 archetypes, pooled-head control, up to 1 question a day, 10 seeds, Archetype, ArchetypeModel, fit(), _js(), _kmeans(), signature()

### Community 24 - "Analogous systems"
Cohesion: 0.29
Nodes (15): Fitbit Body Response, BCI cross-subject/cross-session transfer learning, 11 — Analogous systems in other fields, Empatica Embrace wearable seizure detection, Fitbit Body Response (Google), Gboard federated learning with differential privacy, Tazarv et al. (2023) stress detector with ask-when agent, Abdel-Ghaffar et al. (2025) Fitbit Body Response (+7 more)

### Community 25 - "What precise means, eight states"
Cohesion: 0.23
Nodes (13): E27 Four vs eight states, E28 Answers needed by granularity, Wide questions when more than three states are plausible (EngineConfig.ask_wide), 24 — What "precise" means, and what happens with eight states, Eight states on the valence x arousal circumplex (intermediate states; chance 0.125), Experiments E27-E28 (four vs eight agreement and within-one; answers needed per user), Old question rule (ask only when 2-3 plausible) almost never fires with eight states (1.2 questions, 0.324), Eight states need ~50% more answers and ~twice the time (0.90 in 12 days instead of 8 at 2/day) (+5 more)

### Community 26 - "Vibration products and rhythms"
Cohesion: 0.30
Nodes (15): Slow heartbeat rhythm: heartbeat-like vibration at 80% of the person's heart rate at that moment, never faster, Apollo Neuro: on-demand or scheduled patterned waves by mode (calm, sleep, focus); small double-blind placebo-controlled crossover HRV trials, 27 — Voice and vibration: what each is for, and how to integrate them, doppel: on-demand heartbeat-like vibration slower than resting heart rate; smaller arousal rise and less anxiety before a speech (Azevedo et al., 2017), EmotionCheck (research): false slow heart-rate feedback on the wrist during a stress task; 67 participants, anxiety regulated (Costa et al., 2017), Garmin: stress from HRV while still, relax reminder on high spikes, guided breathing (6 s in, 6 s out), How others use vibration: triggers, patterns and evidence across calming wearables, Lief Smart Patch: automatic vibration when HRV reaches a preset level, then 3-minute HRV biofeedback breathing guidance; pilot of 14 adults (+7 more)

### Community 27 - "Fusion of sources"
Cohesion: 0.19
Nodes (11): Hypotheses from words and voice; body sets intensity, Words/voice decide state, body sets intensity, Quality gate: no question from body signals alone (EngineConfig.ask_needs_expression), Amazon Halo Tone: always-on band microphones analysing tone of voice; criticised for privacy, microphones removed, line discontinued 2023 (always-on listening costs trust), How it fits together: bracelet reads body vs baseline; voice and words give direction and teach body-only moments; voice-note invitation on aroused body; pulse tied to heart or breathing when sure of tension; recovery on held-out moments tunes rhythm and rate, Sources alone and together: body 0.52 (never speaks), voice 0.60, words 0.66, voice+words 0.69, voice+words+body 0.81 (speaks 58%, right 0.93), all four 0.82, Voice moments teach the body-only moments (0.67 with half the moments voiced vs 0.52 for a bracelet that never hears the person), via situation memory and personal head, Amazon Halo Tone: always-on voice tone analysis, microphones removed, line discontinued 2023 (MacRumors, Mozilla Privacy Not Included) (+3 more)

### Community 28 - "Privacy and regulation"
Cohesion: 0.24
Nodes (12): EU AI Act Article 5(1)(f), AI Act Annex III high-risk emotion recognition, 09 Privacy and regulation, Kintsugi case, The medical line: name states, never conditions, Kintsugi: short prompted free-form voice answer (~25 s) screened for depression in 14,898 adults, sensitivity 71% (a short prompted sample carries signal), Behavioral Health Business (2026) Kintsugi closes, Covington (2026) AEPD guidance on AI voice transcription (+4 more)

### Community 29 - "Engine overview"
Cohesion: 0.15
Nodes (13): Demo: today 0.57 vs baseline 0.63 vs engine 0.77 accuracy in week 6; 0.94 when speaking, Words-vs-expression disagreement: 29 questions, 48% at real masking (9% base rate), engine/soulcal Python package (numpy only), SOUL-Bench ladder B0-B6 (mean over people): B6 full loop 0.76 last 2 weeks, 0.90 when speaking, tense recall 0.72, soulcal: decision and personalization layer on any face, voice and text emotion model plus bracelet signals (baseline, fusion, conformal speak/ask/quiet, memory, corrections, disagreement, pattern graph), anchors.SignatureModel module: voice-and-body signatures from one fixed sentence (enrollment, daily anchor, tagged readings), Astrology reflection layer, Engine demo, 20 synthetic people: week-6 accuracy 0.57 -> 0.77; when speaking 0.68 -> 0.94 (+5 more)

### Community 30 - "Haptic tuning check"
Cohesion: 0.27
Nodes (11): Synthetic checks of sources (voice, words, face, body), app use, voice check-ins and pulse tuning in code (channels_sim, haptics_sim), Haptics synthetic check (assumed effects): heartbeat at 80% of live HR 0.72 vs fixed 60/min 0.53 vs 80% of resting HR 0.35; learned resonance breathing 0.81 in last 8 moments vs fixed 6/min 0.71, Tuning the pulse to each person (synthetic; the effects are assumptions from the literature), Rhythm results: fixed 60/min 0.53 (3.3% faster than the heart), 80% of resting HR 0.35, 80% of live HR 0.72, fixed 6/min breathing 0.71, learned resonance 0.73 (0.81 last 8), rhythm and rate learned 0.73 (0.81), Haptics setup: 5 seeds x 200 people, 24 tense moments each; effect = calming effect of one pulse (1.0 = full), _add(), breathing_effect(), haptics_check() (+3 more)

### Community 31 - "Voice check-ins: body triggers, voice decides"
Cohesion: 0.18
Nodes (14): Bracelet always on, app used in a share of moments: accuracy 0.77/0.69/0.62/0.51 at 100/50/25/10% app use, E33: voice check-ins at body-only moments with an aroused body (response rate, tense moments reached, felt intrusiveness), The less the person talks, the fewer tense moments the pulse can reach (76% -> 13%), while pulse precision stays high: the rule waits rather than guessing, Voice check-in: at a body-only moment with an aroused body and possible tension, invite a 5-second voice note, at most once a day (tense moments reached 28% -> 46% with ~1.9 invitations a week), B. Bracelet always on, app in a share of moments: body-only moments 0.67/0.61/0.52 at 50/25/10%; tense moments reached 76/45/27/13%, Voice, words, face and body (synthetic people), D. Stronger speech front ends: generic 0.62/0.74/0.82/0.91 vs with personal calibration 0.77/0.85/0.90/0.96 (gain +0.16/+0.11/+0.08/+0.05) as clarity is multiplied x1.5/x2/x3, personal habits unchanged, Channels setup: engine demo people, 5 seeds x 20 people, up to 1 question a day, 6 weeks, scored on weeks 5-6 before learning (+6 more)

### Community 32 - "Astrology utilities"
Cohesion: 0.32
Nodes (7): moon_age_days(), moon_longitude(), moon_phase(), moon_sign(), reflection_factors(), sun_sign(), _utc()

### Community 33 - "Evaluation: SOUL-Bench"
Cohesion: 0.28
Nodes (13): Check: questions/day, answer rate, 'none of these' share, per-state coverage, gain per question, Claims ledger, 08 Evaluation: SOUL-Bench, Seven evaluation questions (answers needed, baseline gain, questions saved, voice vs words, coverage, drift, proximal calm), Where it may fail: flat voices, same-answer users, rare states, Label efficiency: area under the answers -> accuracy curve, Model ladder B0-B6, Split by person and in time (+5 more)

### Community 34 - "Engine commands"
Cohesion: 0.26
Nodes (13): Archetypes from a consenting cohort, new people matched after a few days (archetypes.fit, ArchetypeModel.start_engine; future phase, prototype), soulcal archetypes command (future phase, synthetic cohort), soulcal channels command (voice, words, face, body), 22 — The engine: code Nightlet can run on its own data, Engine tests (22), incl. loop beats today and no supported moon pattern when none planted, soulcal haptics command (tuning the pulse), SOUL-Bench ladder demo results: B4 generic 0.57 -> B5 0.64 -> B6 full loop 0.76, Reflection layer (moon phase, moon sign, sun sign; astro.py) (+5 more)

### Community 35 - "Pulse tuning code"
Cohesion: 0.27
Nodes (8): Pulse tuned to the person in code: heartbeat at 80% of the live heart rate (never above 90%), breathing at the learned resonance rate (SupportConfig.heartbeat_ratio, learn_resonance), When and how the bracelet pulses in code (support.SupportPolicy): pulse when sure, offer when unsure, gates, rhythm learned per person with held-out moments, When to pulse: pulse on a sure 'tense', offer when 'tense' is among the options, nothing for calm, energized, low or quiet, Rhythm chosen per person by Thompson sampling on the measured effect (SupportPolicy), Pulse tuning in support.py: slow heartbeat at 80% of the current heart rate, never above 90%; breathing pacer starts at 6/min and learns resonance rate by Thompson sampling over 4.5-7 on a separate random stream, Resonance breathing rate: personal optimum between about 4.5 and 7 breaths a minute (standard protocol tests 6.5 down to 4.5 in 0.5 steps), Support, SupportPolicy

### Community 36 - "Incongruence and masking"
Cohesion: 0.24
Nodes (10): Masking (words vs face or voice), E21 Words vs expression, Empathic prompting (prompt-level incongruence handling), Learning whether the person masks or has a serious face, Dragut et al. (2026) Evaluating multimodal emotion recognition in proactive conversational agents, Hoque & Picard, Acted vs. natural frustration and delight, Section: Recurring situations and incongruence (20, 21), Stacchio et al. Empathic Prompting: Non-Verbal Context Integration for Multimodal LLM Conversations (+2 more)

### Community 37 - "Engine fusion code"
Cohesion: 0.18
Nodes (4): Explanation: evidence per channel for each reading (Decision.contributions), Words vs expression: 29 questions, 48% at real masking (masking 9% of readings), calibrate_thresholds(), _js_bits()

### Community 38 - "Biofeedback and vibration evidence"
Cohesion: 0.22
Nodes (10): HRV biofeedback (Goessl et al., 2017), Apollo Neuroscience double-blind placebo-controlled crossover trials on HRV (University of Pittsburgh), Chung et al. (2021) Pilot study on HRV biofeedback wearable (Lief Smart Patch) for anxiety (Applied Psychophysiology and Biofeedback), FDA De Novo DEN200033: NightWare vibrotactile feedback from heart rate and motion during sleep, personalised threshold, Garmin manual: stress level from HRV and relax reminders, Goessl, Curtiss, Hofmann (2017) HRV biofeedback meta-analysis, Section: Voice and vibration (27-voice-and-vibration), Shaffer, Meehan (2020) Practical guide to resonance frequency assessment for HRV biofeedback (Frontiers in Neuroscience) (+2 more)

### Community 39 - "README: voice, vibration and the loop"
Cohesion: 0.25
Nodes (7): SOUL (State Observation & Understanding Layer), How others use voice (Nightlet episodic voice, Amazon Halo Tone, Kintsugi), MacDonald, Brewster, Pollick et al. (2023) Fast heartbeats via vibration and sound raise anxiety and heart rate (ICMI 23), Decision with a guarantee (speak / ask / stay quiet), Nightlet, SOUL-Calibrate, When the bracelet pulses: pulse when sure of tension (slow heartbeat at 80% of the live heart rate, or breathing pacer at the person's learned resonance rate), offer when unsure, nothing when calm, excited, low or moving; body alone 3% of tense moments vs calibrated 56% at 88% precision; 20% held out

### Community 40 - "Reading audit"
Cohesion: 0.25
Nodes (7): Diagnostic drift of language, Non-diagnostic language battery, Persona invariance battery, Safety routing battery, Separation of layers battery (astrology vs measured), Sycophancy battery, Uncertainty honesty battery

### Community 41 - "Model-agnostic input"
Cohesion: 0.40
Nodes (3): Model-agnostic input: probabilities over four states (basic_emotions_to_states), Model-agnostic engine: any front-end model (in-house or partner) can be swapped in and compared by SOUL-Bench on the users' own answers, basic_emotions_to_states()

## Knowledge Gaps
- **37 isolated node(s):** `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Claims ledger (days 1-30)`, `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)`, `Graphify knowledge graph of the project (1,049 concepts, 3,135 links)`, `MIT License (README)` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 169 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `README: SOUL-Calibrate` connect `Cohort, archetype path and analogies` to `Simulation scripts and question budget results`, `Recurring situations and question budget`, `Voice-and-body signatures`, `Risks, traps and cold start`, `Speech front end and real-voice check`, `Archetype and channel checks (code)`, `When the bracelet pulses: evidence`, `Question budget experiments`, `Claims ledger and inspiration`, `Problem and evidence`, `Clinical practice`, `Architecture`, `Authorship`, `Analogous systems`, `What precise means, eight states`, `Vibration products and rhythms`, `Fusion of sources`, `Engine overview`, `Haptic tuning check`, `Voice check-ins: body triggers, voice decides`, `Evaluation: SOUL-Bench`, `Engine commands`, `Incongruence and masking`, `README: voice, vibration and the loop`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `README: SOUL-Calibrate` (e.g. with `Personal voice-and-body signatures from a fixed sentence (synthetic people)` and `Voice, words, face and body (synthetic people)`) actually correct?**
  _`README: SOUL-Calibrate` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Valence/arousal sliders (Russell's Affect Grid, Self-Assessment Manikin)`, `Claims ledger (days 1-30)`, `Clinical methods for timing and testing (JITAI, MRT, outcome monitoring, HRV biofeedback, alarm fatigue)` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Simulation scripts and question budget results` be split into smaller, more focused modules?**
  _Cohesion score 0.057946069994262765 - nodes in this community are weakly interconnected._
- **Why does `22 — The engine: code Nightlet can run on its own data` connect `Engine commands` to `Recurring situations and question budget`, `Voice-and-body signatures`, `Speech front end and real-voice check`, `Cohort, archetype path and analogies`, `Engine concept-to-code map`, `When the bracelet pulses: evidence`, `Question budget experiments`, `Active questions and decision rule`, `Enrollment details`, `Claims ledger and inspiration`, `Problem and evidence`, `Architecture`, `Personal pattern graph`, `Authorship`, `Ideas from prior work`, `What precise means, eight states`, `Vibration products and rhythms`, `Fusion of sources`, `Engine overview`, `Haptic tuning check`, `Evaluation: SOUL-Bench`, `Pulse tuning code`, `Engine fusion code`, `Model-agnostic input`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `27 — Voice and vibration: what each is for, and how to integrate them` (e.g. with `Voice, words, face and body (synthetic people)` and `Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)`) actually correct?**
  _`27 — Voice and vibration: what each is for, and how to integrate them` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Recurring situations and question budget` be split into smaller, more focused modules?**
  _Cohesion score 0.05462962962962963 - nodes in this community are weakly interconnected._