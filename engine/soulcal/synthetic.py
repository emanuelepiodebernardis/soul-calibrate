"""A synthetic device stream for demos and tests: one person, several weeks, every channel Nightlet reads.

The person has a weekly routine of recurring situations (the evening after work on Monday, the gym on
Tuesday and Thursday, a quiet Sunday night...), each with a usual state. They also have traits that
make a generic model fail:

* a "serious face": the facial model sees tension even when they are calm;
* masking: when tense they often write "fine";
* a personal resting heart rate and HRV far from population averages;
* the gym raises heart rate because of movement, not emotion.

Channels go missing at realistic rates (the camera is not always on, the bracelet is optional).
No effect of the moon is planted, so any moon pattern the pattern finder reports is noise.
These are synthetic data: they show how the code behaves, not how real people are.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np

from .schema import STATES, Reading

SLOTS = (19, 21, 23)   # three evening readings
# usual state for (weekday, slot)
ROUTINE = {
    (0, 19): "tense", (0, 21): "tense", (0, 23): "low",
    (1, 19): "energized", (1, 21): "calm", (1, 23): "low",
    (2, 19): "tense", (2, 21): "calm", (2, 23): "low",
    (3, 19): "energized", (3, 21): "calm", (3, 23): "low",
    (4, 19): "energized", (4, 21): "energized", (4, 23): "calm",
    (5, 19): "calm", (5, 21): "energized", (5, 23): "calm",
    (6, 19): "calm", (6, 21): "low", (6, 23): "low",
}
GYM = {(1, 19), (3, 19)}


@dataclass
class Person:
    user_id: str = "demo-user"
    face_bias: tuple = (-0.3, -0.5, 1.2, 0.2)    # serious face: looks tense
    voice_bias: tuple = (0.0, -0.4, 0.0, 0.6)    # flat voice: sounds low
    mask_prob: float = 0.5                         # when tense, writes "fine" (calm)
    hr_rest: float = 58.0                          # far from the population's 72
    hrv_rest: float = 70.0                         # far from the population's 42
    stability: float = 0.85                        # situation brings its usual state
    face_strength: float = 0.6                     # how clearly each channel shows the state
    voice_strength: float = 0.7
    text_strength: float = 1.0
    channel_noise: float = 0.9


def generate(days: int = 42, seed: int = 0, person: Person | None = None,
             start: datetime = datetime(2026, 9, 7)) -> tuple[list[Reading], list[str], list[bool]]:
    """Return readings (with no self-report), the true states, and whether the person was masking."""
    p = person or Person()
    rng = np.random.default_rng(seed)
    readings, truth, masking = [], [], []
    neighbours = {"calm": ("energized", "low"), "energized": ("calm", "tense"),
                  "tense": ("energized", "low"), "low": ("calm", "tense")}
    for d in range(days):
        day = start + timedelta(days=d)
        for h in SLOTS:
            ts = day.replace(hour=h, minute=int(rng.integers(0, 50)))
            key = (day.weekday(), h)
            y = ROUTINE[key] if rng.random() < p.stability else str(rng.choice(neighbours[ROUTINE[key]]))
            k = STATES.index(y)
            onehot = np.eye(4)[k]

            def probs(strength, bias, noise):
                z = strength * onehot + np.array(bias) + rng.normal(0, noise, 4)
                e = np.exp(z - z.max())
                return {s: float(v) for s, v in zip(STATES, e / e.sum())}

            masked = y == "tense" and rng.random() < p.mask_prob
            face = probs(p.face_strength, p.face_bias, p.channel_noise) if rng.random() < 0.6 else None
            voice = probs(p.voice_strength, p.voice_bias, p.channel_noise) if rng.random() < 0.9 else None
            text = None
            if rng.random() < 0.7:
                text = probs(p.text_strength, (0, 0, 0, 0), p.channel_noise)
                if masked:
                    text = probs(p.text_strength, (1.6, 0, -1.6, 0), p.channel_noise)   # "I'm fine"
            gym = key in GYM
            arousal = {"calm": -0.5, "energized": 1.0, "tense": 1.0, "low": -0.8}[y]
            neg = {"calm": 0.0, "energized": 0.0, "tense": 1.0, "low": 0.5}[y]
            bracelet = rng.random() < 0.8
            readings.append(Reading(
                user_id=p.user_id, timestamp=ts, face=face, voice=voice, text=text,
                heart_rate=float(p.hr_rest + 6 * arousal + (22 if gym else 0) + rng.normal(0, 3)) if bracelet else None,
                hrv_rmssd=float(p.hrv_rest - 6 * arousal - 10 * neg - (15 if gym else 0) + rng.normal(0, 5)) if bracelet else None,
                skin_temp=float(33.8 - 0.3 * neg + rng.normal(0, 0.25)) if bracelet else None,
                motion=float((1.5 if gym else 0.2) + abs(rng.normal(0, 0.15))) if bracelet else None,
            ))
            truth.append(y)
            masking.append(masked)
    return readings, truth, masking
