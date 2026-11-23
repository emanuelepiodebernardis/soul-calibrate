# 28 — Listening well from day one: open speech models as the front end

Author: Emanuele De Bernardis · Module: Speech front end · Extends: [[27-voice-and-vibration]], [[07-fusion]], [[22-engine]], [[16-experiments]] · Code: `realvoice/e31_real_voice.py`, `engine/soulcal/channels_sim.py` (part D) · Experiment: E31

**Original contribution (E. De Bernardis):** start from the strongest open models for *what is said* and *how it
is said*, run them on the phone, and let SOUL-Calibrate do what no general model can: learn this person. And
measure, on real voice, how much the personal layer still adds.

## 1. What "voice" means here

- **Voice is an input:** the person talks to the app (Nightlet: "just talk or type"; voice and face are read from
  those moments). The bracelet does not speak; on Nightlet's site it is a haptic core and a sensor. The "calm voice"
  of [[26-when-to-pulse]] is an optional line of audio from the phone, off by default.
- **From one voice note, two signals:** the **words** (speech recognition, then a text model) and the **way they
  are said** (a speech-emotion model on pitch, energy, rhythm, pauses). They enter the engine as two separate
  channels, `text` and `voice`, because they disagree exactly when it matters ([[21-text-face-incongruence]]).

## 2. Open models that understand speech well

| Model or tool | What it does | Why it matters here |
| --- | --- | --- |
| Whisper (OpenAI), Parakeet (NVIDIA) | speech to text, many languages, automatic language detection | the words, offline |
| Handy (MIT, open source) | an offline speech-to-text app built on Whisper and Parakeet (and others, including SenseVoice) | a working example of on-device transcription to fork; it does not generate speech |
| SenseVoice (FunAudioLLM) | speech recognition, language identification, speech emotion recognition and audio events (laughter, crying) in one model; the open Small model covers 5 languages, the Large over 50 | words, emotion and events from one pass |
| emotion2vec / emotion2vec+ | open speech-emotion foundation model; universal representation tested across 10 languages; emotion2vec+ gives emotion scores directly | the "how it is said" channel, plus embeddings for a personal head |
| ElevenLabs Scribe (commercial) | speech to text in 90+ languages, with tags for non-speech events such as laughter | a cloud reference point; ElevenLabs is best known for generating speech, which is not what SOUL needs to read people |

ElevenLabs' open-source counterpart for **generating** speech would be a text-to-speech model (for example
CosyVoice from the same FunAudioLLM family); it only matters for the optional calm voice, not for reading.

## 3. How it plugs in

```
voice note (phone, on device)
 ├─ speech to text (Whisper / Parakeet / SenseVoice) ─> text emotion model ─> text  probabilities ┐
 └─ speech emotion (emotion2vec+ / SenseVoice SER) ─────────────────────────> voice probabilities ├─> SoulEngine
bracelet: heart rate, HRV, skin temperature, movement ────────────────────────────────────────────┘
```

The engine is model-agnostic ([[22-engine]]): any of these models can be swapped in, in-house or from a partner,
and SOUL-Bench compares them on the users' own answers ([[08-evaluation-soul-bench]]). Audio events (a laugh, a
sigh, crying) are a natural next input.

## 4. Does a stronger front end make calibration unnecessary? No, but it changes how much it adds

**D. Synthetic check** (`python -m soulcal channels`, part D): how clearly voice and words show the state is
multiplied, as with better models, while each person's habits (a flat voice, a serious face, saying "fine" when
tense) stay the same, because they belong to the person, not to the model. 5 seeds × 20 people, weeks 5–6:

| Front end | Generic reading | With personal calibration | Gain |
| --- | --- | --- | --- |
| Today's generic models | 0.62 | 0.77 | +0.16 |
| Stronger open models (×1.5) | 0.74 | 0.85 | +0.11 |
| Much stronger (×2) | 0.82 | 0.90 | +0.08 |
| Near-perfect on words and voice (×3) | 0.91 | 0.96 | +0.05 |

- **Better models raise the floor for everyone**, from the first day: this is the "start from a high level" part.
- **Calibration still adds on top**, because masking and personal habits are not a model problem; the gain is
  smaller as models improve, which is why it should be measured, not assumed.
- **The two work together:** a strong front end makes the engine sure more often, so it asks fewer questions.

## 5. The real-voice check, ready to run (E31)

`realvoice/e31_real_voice.py` runs the experiment on real recordings on any machine with internet access:

- **Data:** RAVDESS (24 speakers, 8 emotions, mapped to the four states), or any CSV of `path, speaker, label`.
- **Encoders:** emotion2vec+ (FunASR; embeddings and its own zero-shot emotion scores) or MFCCs (no download).
- **Protocol:** leave one speaker out; half of the held-out speaker's clips are the calibration pool, half the
  test. Settings: zero-shot, generic head, + personal baseline (unlabeled), + 2, 4, 8, 16 answers.
- **Tested here** on synthetic features and generated audio (`realvoice/tests`); the real numbers come from
  running it. RAVDESS is acted speech: a fair first check of speaker effects, not of everyday emotion.

```
pip install -r realvoice/requirements.txt
python realvoice/e31_real_voice.py --data path/to/RAVDESS --encoder emotion2vec --out realvoice/results
```

## Check

- E31: on real voice, with emotion2vec+ as the front end, the personal baseline and a few answers per speaker
  beat the generic head and the zero-shot scores, on held-out recordings of each speaker.
