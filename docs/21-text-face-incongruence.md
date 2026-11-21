# 21 — When the words and the face disagree

Author: Emanuele De Bernardis · Module: Incongruence · Extends: [[07-fusion]], [[05-active-questions]], [[14-reading-audit]], [[08-evaluation-soul-bench]]

**Original contribution (E. De Bernardis):** treat disagreement between what a person writes or says and what
their face or voice shows as a *reason to ask*, decided by the calibrated speak / ask / quiet rule and read
against the person's own baseline, instead of letting a language model resolve it inside a prompt.

## Related work

- **Empathic prompting** (Stacchio, Ubaldi, Mauri, Gaggioli, Galdelli, Frontoni; University of Macerata,
  Università Cattolica, Università Politecnica delle Marche). A webcam feeds a commercial facial expression
  recognition service (emotion, intensity, valence, arousal); a middleware aggregates it over a few seconds and
  adds it to the prompt of a local language model. The system prompt tells the model to check whether the text
  matches the facial data and, when they diverge, to raise it as a gentle question. A within-subjects study with
  20 people compared this with a text-only chatbot: no significant differences at the level of the main
  constructs, with item-level advantages for the facial condition (for example perceived mood contagion and
  likability). [arXiv:2510.20743](https://arxiv.org/abs/2510.20743)
- **Proactive conversational agents** (Dragut et al., 2026): a facial module plus a linguistic analysis engine,
  20 users. Users often kept a "poker face" while expressing positive things in words, and the linguistic
  analysis proved more reliable than the face. [arXiv:2605.20200](https://arxiv.org/abs/2605.20200)
- **Natural frustration** (Hoque & Picard, MIT): many people smile when genuinely frustrated, so a smile is not
  a reliable sign of delight. [MIT Media Lab](https://www.media.mit.edu/publications/acted-vs-natural-frustration-and-delight-many-people-smile-in-natural-frustration/)
- Large audio-language models follow the words when the voice disagrees ([[00-problem]]).

## What SOUL-Calibrate adds

| Question | Empathic prompting | SOUL-Calibrate |
| --- | --- | --- |
| Who decides that words and face disagree? | The language model, from instructions in its prompt | A measured incongruence score between the text model and the face or voice model, each read against the person's baseline |
| Reference point | Population facial categories; a neutral face while typing is assumed to mean concentration | The person's own neutral face and voice from enrollment ([[02-enrollment]]); some people always look serious |
| What happens next | The model rephrases its reply | Speak / ask / stay quiet: incongruence widens the conformal set, so the reading becomes a two-option question ([[05-active-questions]]) |
| What the answer does | Nothing persists | It is a label: it teaches the personal model how this person masks or shows emotion ([[06-personal-model]], [[20-recurring-situations]]) |
| How it is evaluated | Questionnaires on perceived empathy | SOUL-Bench reports congruent and incongruent moments separately; the reading audit tests that the wording never overrides the measured decision ([[08-evaluation-soul-bench]], [[14-reading-audit]]) |

## Design

1. **Two readings, one per channel:** the words (transcript or text) and the expression channel (voice, face if
   consented). Each gives a probability over the same four states.
2. **Incongruence score:** the distance between the two distributions (for example the Jensen–Shannon
   divergence), compared with *this person's* usual distance. Some people always say "fine" in a flat voice:
   for them a gap is normal.
3. **Decision:** a high personal incongruence never produces a confident reading. It produces a closed question
   with the two candidate states: "Your words sound fine, but your voice sounds tighter than usual. Which is closer?"
4. **Learning:** the answer says which channel was right for this person in this kind of situation. Over time
   the personal model learns whether the person masks (trust the voice) or simply has a serious face (trust the words).
5. **Privacy:** the face stays optional and out of the default consent level until it proves useful for the
   person ([[15-labels-and-consent]]). The text never leaves the phone.

## Experiment E21

- **Data:** public multimodal sets with text, audio and video, plus self-reports from the pilot.
- **Measure:** accuracy and coverage on congruent vs incongruent moments; share of incongruent moments where the
  question was answered with the "expression" option vs the "words" option, per person.
- **Hypothesis:** incongruent moments are where generic models fail most and where one question gains most.
- **Would refute it:** no accuracy gap between congruent and incongruent moments, or answers that split evenly
  between the channels for most people (then incongruence is noise, not masking).

## Check

The incongruence trigger is accepted only if, in SOUL-Bench, questions it triggers change the reading more
often than questions at ambiguous moments without incongruence.
