"""Personal voice-and-body signatures from a fixed sentence (docs/29).

The same short sentence, read in three moments, gives three things:

1. **Enrollment** (first days, neutral): the person's usual voice and body, so every later reading is measured
   against them, not against other people (up to two thirds of voice variance is who is speaking).
2. **Daily anchor** (5 seconds, any mood): today's microphone, room and day, removed from the evening's readings.
3. **Tagged readings:** when the person feels a clear state ("I'm tense right now"), they read the same sentence and
   say how they feel. Same words, so only the voice and the body differ: the system stores that difference as the
   person's own signature for that state, voice and body together.

Readings are then compared with the person's signatures, shrunk towards the population's directions while the
person has few tagged readings. The output is a probability for each state, which feeds the engine's voice
channel. Raw audio never leaves the phone: only prosodic features (pitch, energy, rate, pauses, voice quality)
and body signals (heart rate, HRV, skin temperature) are used.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .schema import STATES


@dataclass
class SignatureModel:
    n_features: int
    population: np.ndarray                       # (states, features): typical direction of each state, in z units
    shrink: float = 2.0                          # tagged readings needed before a signature outweighs the population
    temperature: float = 1.0
    neutral: list = field(default_factory=list)
    session: np.ndarray | None = None
    tagged: dict = field(default_factory=dict)  # state -> list of z vectors

    # ------------------------------------------------------------------ baseline and anchor
    def add_enrollment(self, x: np.ndarray) -> None:
        """A neutral reading of the fixed sentence during the first days."""
        self.neutral.append(np.asarray(x, float))

    def _mu_sd(self) -> tuple[np.ndarray, np.ndarray]:
        n = np.array(self.neutral)
        return n.mean(0), n.std(0) + 1e-3 if len(n) > 1 else np.ones(self.n_features)

    def set_anchor(self, x: np.ndarray) -> None:
        """Today's 5-second anchor (the fixed sentence, any mood): today's offset from the person's usual."""
        mu, _ = self._mu_sd()
        self.session = np.asarray(x, float) - mu

    def z(self, x: np.ndarray, use_anchor: bool = True) -> np.ndarray:
        if not self.neutral:
            return np.asarray(x, float)
        mu, sd = self._mu_sd()
        off = self.session if (use_anchor and self.session is not None) else 0.0
        return (np.asarray(x, float) - mu - off) / sd

    # ------------------------------------------------------------------ signatures
    def add_tagged(self, state: str, x: np.ndarray, use_anchor: bool = True) -> None:
        """The fixed sentence read while the person says how they feel."""
        self.tagged.setdefault(state, []).append(self.z(x, use_anchor))

    def prototypes(self) -> np.ndarray:
        out = []
        for k, s in enumerate(STATES):
            pts = self.tagged.get(s, [])
            if pts:
                n = len(pts)
                out.append((n * np.mean(pts, 0) + self.shrink * self.population[k]) / (n + self.shrink))
            else:
                out.append(self.population[k])
        return np.array(out)

    def proba(self, x: np.ndarray, use_anchor: bool = True, personal: bool = True) -> dict:
        zx = self.z(x, use_anchor) if personal else np.asarray(x, float)
        protos = self.prototypes() if personal else self.population
        d2 = ((zx[None, :] - protos) ** 2).sum(1)
        logits = -d2 / (2 * self.temperature)
        e = np.exp(logits - logits.max())
        return {s: float(v) for s, v in zip(STATES, e / e.sum())}

    def ready(self, min_enrollment: int = 3) -> bool:
        """Enough neutral readings to measure the person against themselves."""
        return len(self.neutral) >= min_enrollment

    def to_dict(self) -> dict:
        return {"n_features": self.n_features, "population": self.population.tolist(), "shrink": self.shrink,
                "temperature": self.temperature, "neutral": [v.tolist() for v in self.neutral],
                "session": None if self.session is None else self.session.tolist(),
                "tagged": {s: [v.tolist() for v in pts] for s, pts in self.tagged.items()}}

    @classmethod
    def from_dict(cls, d: dict) -> "SignatureModel":
        m = cls(d["n_features"], np.array(d["population"]), d["shrink"], d["temperature"])
        m.neutral = [np.array(v) for v in d["neutral"]]
        m.session = None if d["session"] is None else np.array(d["session"])
        m.tagged = {s: [np.array(v) for v in pts] for s, pts in d["tagged"].items()}
        return m

    def difference(self, state: str, names: list[str]) -> list[tuple[str, float]]:
        """What changes in this person when they are in `state`, largest first: what the app can show them."""
        if state not in self.tagged:
            return []
        delta = np.mean(self.tagged[state], 0) - (np.mean(self.tagged["calm"], 0) if "calm" in self.tagged else 0)
        order = np.argsort(-np.abs(delta))
        return [(names[i], float(delta[i])) for i in order]


# Default features of the fixed sentence: prosody from the voice note, body from the bracelet at that moment.
# The population directions are a starting point in z units, replaced by the person's own as they tag readings.
DEFAULT_FEATURES = ["pitch", "pitch range", "energy", "speech rate", "jitter", "pause share",
                    "heart rate", "HRV", "skin temperature"]
#                               pitch range energy rate jitter pause |  HR   HRV  temp
DEFAULT_POPULATION = 1.5 * np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],          # calm
                                     [1.0, 1.0, 1.0, 0.8, 0.0, -0.5, 1.0, -0.5, 0.0],        # energized
                                     [1.0, 0.2, 0.8, 0.8, 1.0, -0.2, 1.0, -1.0, -0.6],       # tense
                                     [-0.8, -0.8, -0.8, -0.8, 0.2, 0.9, -0.5, 0.2, 0.0]])    # low


# Voluntary adaptation modes: the user chooses how fast the system learns them; each mode asks for the minimum
# that reached its level in the synthetic checks (docs/23 for questions, docs/29 for sentences). Seconds are
# estimates: anchor 5 s, tagged sentence 10 s, question 3 s.
MODES = {
    "light": {"questions_per_day": 0.5, "enrollment_per_day": 1, "anchor_every_evening": True, "tagged_per_week": 1},
    "standard": {"questions_per_day": 1.0, "enrollment_per_day": 1, "anchor_every_evening": True, "tagged_per_week": 3},
    "fast": {"questions_per_day": 2.0, "enrollment_per_day": 2, "anchor_every_evening": True, "tagged_per_week": 7},
}


def seconds_per_week(mode: str) -> float:
    """Estimated time the mode asks of the person in a normal week (after enrollment)."""
    m = MODES[mode]
    return 7 * 5 * m["anchor_every_evening"] + 10 * m["tagged_per_week"] + 3 * 7 * m["questions_per_day"]


def offer_tagged_today(mode: str, tagged_this_week: int, days_left_in_week: int) -> bool:
    """Offer the optional 'read the sentence and tell me how you feel' today? Spread the week's readings out."""
    left = MODES[mode]["tagged_per_week"] - tagged_this_week
    return left > 0 and left >= days_left_in_week / 7 * MODES[mode]["tagged_per_week"] - 1e-9
