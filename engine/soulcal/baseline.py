"""Personal baseline: every signal is read against the person's own norm.

* Physiological signals become personal z-scores (exponential moving mean and variance).
* Channel probabilities are corrected by the person's usual distribution: someone whose face always
  looks "tense" to a facial model gets that bias removed (log p - log of their usual p).
* A conformal test martingale on the z-scores flags when the person's norm has moved (new phone,
  new job, illness), so the product can re-anchor instead of reading the change as emotion.
"""

from __future__ import annotations

import math

import numpy as np

from .schema import CHANNELS, N_STATES, PHYSIO, STATES, Reading


class EMA:
    """Exponential moving mean and variance with a warm-up that behaves like a plain average."""

    def __init__(self, alpha: float):
        self.alpha = alpha
        self.n = 0
        self.mean = 0.0
        self.var = 1.0

    def update(self, x: float) -> None:
        self.n += 1
        a = max(self.alpha, 1.0 / self.n)
        d = x - self.mean
        self.mean += a * d
        self.var = (1 - a) * (self.var + a * d * d) if self.n > 1 else 1.0

    def z(self, x: float) -> float:
        if self.n < 2:
            return 0.0
        return (x - self.mean) / math.sqrt(max(self.var, 1e-6))

    def to_dict(self) -> dict:
        return {"alpha": self.alpha, "n": self.n, "mean": self.mean, "var": self.var}

    @classmethod
    def from_dict(cls, d: dict) -> "EMA":
        e = cls(d["alpha"])
        e.n, e.mean, e.var = d["n"], d["mean"], d["var"]
        return e


class PersonalBaseline:
    def __init__(self, alpha: float = 0.02, drift_threshold: float = 20.0):
        self.alpha = alpha
        self.physio = {k: EMA(alpha) for k in PHYSIO}
        self.channel_mean = {c: np.full(N_STATES, 1.0 / N_STATES) for c in CHANNELS}
        self.channel_n = {c: 0 for c in CHANNELS}
        self.martingale = 1.0
        self.drift_threshold = drift_threshold
        self._recent: list[float] = []

    # -- reading against the norm -------------------------------------------------------------
    def physio_z(self, r: Reading) -> dict[str, float]:
        return {k: self.physio[k].z(v) for k, v in r.physio().items()}

    def channel_logits(self, r: Reading) -> dict[str, np.ndarray]:
        """log p - log(usual p) per available channel, so personal expression biases cancel out."""
        out = {}
        for c in CHANNELS:
            p = r.channel(c)
            if p is None:
                continue
            v = np.array([max(p[s], 1e-4) for s in STATES])
            usual = self.channel_mean[c] if self.channel_n[c] >= 5 else np.full(N_STATES, 1.0 / N_STATES)
            out[c] = np.log(v) - np.log(np.maximum(usual, 1e-4))
        return out

    # -- updating ---------------------------------------------------------------------------------
    def update(self, r: Reading) -> bool:
        """Update the norm with a reading. Returns True when the drift trigger fires."""
        z = self.physio_z(r)
        drift = self._martingale_step(z)
        for k, v in r.physio().items():
            self.physio[k].update(v)
        for c in CHANNELS:
            p = r.channel(c)
            if p is None:
                continue
            self.channel_n[c] += 1
            a = max(self.alpha, 1.0 / self.channel_n[c])
            self.channel_mean[c] = (1 - a) * self.channel_mean[c] + a * np.array([p[s] for s in STATES])
        return drift

    def _martingale_step(self, z: dict[str, float]) -> bool:
        """Power martingale on the conformal p-value of the reading's distance from the norm."""
        if not z:
            return False
        score = float(np.sqrt(np.mean([v * v for v in z.values()])))
        hist = self._recent
        p = (sum(1 for s in hist if s >= score) + 1) / (len(hist) + 1) if hist else 1.0
        hist.append(score)
        if len(hist) > 200:
            hist.pop(0)
        if len(hist) < 20:
            return False
        eps = 0.7
        self.martingale *= eps * p ** (eps - 1)
        self.martingale = min(self.martingale, 1e6)
        if self.martingale > self.drift_threshold:
            self.martingale = 1.0
            return True
        return False

    def to_dict(self) -> dict:
        return {"alpha": self.alpha, "physio": {k: e.to_dict() for k, e in self.physio.items()},
                "channel_mean": {c: v.tolist() for c, v in self.channel_mean.items()},
                "channel_n": self.channel_n, "martingale": self.martingale,
                "drift_threshold": self.drift_threshold, "recent": self._recent}

    @classmethod
    def from_dict(cls, d: dict) -> "PersonalBaseline":
        b = cls(d["alpha"], d["drift_threshold"])
        b.physio = {k: EMA.from_dict(v) for k, v in d["physio"].items()}
        b.channel_mean = {c: np.array(v) for c, v in d["channel_mean"].items()}
        b.channel_n = d["channel_n"]
        b.martingale = d["martingale"]
        b._recent = list(d["recent"])
        return b
