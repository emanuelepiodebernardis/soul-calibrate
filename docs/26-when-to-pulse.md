# 26 — When and how the bracelet should pulse

Author: Emanuele De Bernardis · Module: Support · Extends: [[05-active-questions]], [[12-clinical-practices]], [[23-question-budget]], [[25-coarse-to-fine-and-archetypes]] · Code: `engine/soulcal/support.py` · Experiment: E32 in [[16-experiments]]

**Original contribution (E. De Bernardis):** the pulse is where the reading becomes help, so it follows the same
rule as the reading. It pulses only when the engine is sure the person is tense against their own baseline, offers
a calm minute when it is unsure, and stays still otherwise. Each person's body then shows which rhythm calms them.

## What the pulse is for, in Nightlet's words

Nightlet's site says the bracelet "pulses when you need to come back to yourself": it does not count steps, it
helps you find your calm and regulate your nervous system when things get loud. The pulse is therefore an
**intervention to calm**, not a notification that you are stressed. Its
disclaimer adds that no outcome is guaranteed, which is a reason to measure the effect for each person.

## When: agitated, not calm, never excited

| The engine's decision | The pulse | Why |
| --- | --- | --- |
| Speaks "tense" (sure, against the person's baseline) | **Pulse**: a slow rhythm for 1–3 minutes, a line on screen, a calm voice only if the user turned it on | This is the moment it is for |
| Asks, and "tense" is among the options | **Offer**: one soft tap and "Want a calm minute?"; the answer is also a label ([[05-active-questions]]) | A pulse imposed on a wrong reading costs trust; an offer does not |
| Speaks "calm" | Nothing | There is nothing to regulate; the user can always start a calm minute themselves |
| Speaks "energized" | Nothing | Heart rate and skin conductance rise with excitement as with anxiety ([[00-problem]]): calming someone who is excited is a false alarm |
| Speaks "low" | Nothing (a calming rhythm does not lift low arousal) | Other support (a page, a kindred match) belongs to the reading, not to the pulse |
| Quiet | Nothing | |

**Gates, the same for every pulse:** the bracelet is worn; no strong movement (exercise raises heart rate without
stress); at most 3 a day and 90 minutes apart; only in the hours the user chose. This is the question budget of
[[23-question-budget]] applied to the wrist, for the same reason: alarm fatigue ([[12-clinical-practices]]).

**Why this needs the calibrated reading.** A pulse triggered by the body alone fires on excitement as often as on
anxiety. The engine combines words, voice, face and body against the person's own norm, so it can tell them apart,
and it knows when it is unsure.

## How: two rhythms from the literature, chosen per person

- **Slow heartbeat:** a heartbeat-like vibration below the person's own resting heart rate (80% by default). In a
  single-blind study (Azevedo et al., 2017, *Scientific Reports*), people anticipating a public speech with the
  device on showed smaller rises in skin conductance and reported less anxiety than those with it off.
- **Breathing pacer:** a vibration that rises and fades at about 6 breaths a minute, the slow pace used in HRV
  biofeedback. Haptic and voice guidance both slowed breathing in a driving study (Paredes et al., 2018), and
  vibrotactile pacers have been studied for anxiety regulation (Miri et al., 2020).
- **Limits:** a 2025 study of two tactile breathing devices in stressed people found effects during use but no
  lasting effects afterwards. So the pulse is short, it is offered when it is needed, and its effect is measured
  for each person instead of assumed.

**Screen and voice:** the pulse comes with one line on screen ("Breathe with the pulse: in as it rises, out as it
fades"). A calm voice ("Take a moment. Breathe slowly with me.") is off by default, because people are often not alone.

## Learning what works for this person

- After each pulse, the heart rate and HRV of the next minutes are compared with the moment before; a one-tap
  "did it help?" can be added.
- **20% of eligible moments are held out at random:** a micro-randomised trial inside the product
  ([[12-clinical-practices]]). The effect is the recovery with a pulse minus the person's recovery without one.
- The rhythm is chosen by Thompson sampling on that effect (`SupportPolicy`).

## Synthetic check (`python -m soulcal support`)

The readings and decisions are the engine demo's synthetic people. **The effect of a pulse is an assumption:**
when tense, the rhythm that suits the person adds about 1.0 to recovery and the other about 0.2; when not tense, a
pulse adds nothing. Each false pulse makes the person turn pulses off with probability 5%. The same gates apply
to every policy; 5 seeds, 20 people each, 6 weeks.

| When to pulse | Pulses per week | Pulses at tense moments | Pulses at excitement | Tense moments helped | Extra recovery per tense moment |
| --- | --- | --- | --- | --- | --- |
| Body alone: heart rate above the person's usual, not moving | 0.15 | 47% | 51% | 3% | 0.02 |
| Generic reading says tense (today, no questions) | 0.49 | 86% | 6% | 16% | 0.10 |
| SOUL-Calibrate decision, one fixed rhythm | 1.00 | 88% | 6% | 56% | 0.36 |
| SOUL-Calibrate decision, rhythm learned per person | 1.00 | 86% | 5% | 57% | **0.41** |

- **Body alone gets it wrong half the time:** half of its pulses land on excitement, and it rarely reaches the
  tense moments, because tension at rest moves the heart rate only a little.
- **The generic reading is precise but rarely sure**, so it helps only 16% of tense moments. The calibrated
  decision helps 56–57% (pulse, or an accepted offer) at the same precision. **That is the whole project in one
  number:** the better the reading, the more often the pulse can help without false alarms.
- **Learning the rhythm adds a little** (0.36 → 0.41), and after 6 weeks it picks the right rhythm for 72% of
  people (50% by chance). The effect measured on one person is still noisy (error 0.51 on a true effect of about
  1.0, from about 6 pulses), so **the size of the effect should be measured on the consenting cohort first**
  ([[19-private-cohort-pilot]]), and per person only the choice of rhythm.

## Check

- E32: on the cohort, micro-randomised pulses at moments the engine is sure are tense: HRV and heart-rate
  recovery and "did it help?" with vs without a pulse, slow heartbeat vs breathing pacer, and pulses turned off
  over 8 weeks, compared with pulses triggered by the body alone.
