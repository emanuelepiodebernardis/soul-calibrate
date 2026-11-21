"""Personal fusion head and situation memory.

Fusion head
    A small multinomial logistic model on the device. Its input is every available channel's
    baseline-corrected log-probabilities (face, voice, text) plus the physiological z-scores.
    It starts from a transparent prior (each channel trusted by a fixed weight; heart rate up and
    HRV down mean higher arousal, unless movement explains it) and learns from the person's answers,
    with an L2 pull back toward that prior (shrinkage), so a few answers cannot wreck it.
    Its weights tell, per person, which channel to trust: some people's face says little, others'
    voice says a lot.

Situation memory
    Answers stored with the signal and the context they were given for. A new reading close to a
    stored one (same kind of situation) receives that answer's evidence, weighted by a Gaussian kernel.
    The head learns how the person shows each state; the memory learns what their recurring situations
    mean (docs/20-recurring-situations.md).
"""

from __future__ import annotations

import math

import numpy as np

from .schema import CHANNELS, N_STATES, PHYSIO

CHANNEL_PRIOR_WEIGHT = {"face": 0.5, "voice": 0.6, "text": 0.8}
N_FEATURES = len(CHANNELS) * N_STATES + len(PHYSIO)
CALM, ENERGIZED, TENSE, LOW = range(4)


def feature_vector(logits: dict[str, np.ndarray], z: dict[str, float]) -> np.ndarray:
    f = np.zeros(N_FEATURES)
    for i, c in enumerate(CHANNELS):
        if c in logits:
            f[i * N_STATES:(i + 1) * N_STATES] = logits[c]
    base = len(CHANNELS) * N_STATES
    for j, k in enumerate(PHYSIO):
        f[base + j] = float(np.clip(z.get(k, 0.0), -4, 4))
    return f


def prior_weights() -> np.ndarray:
    W = np.zeros((N_STATES, N_FEATURES))
    for i, c in enumerate(CHANNELS):
        for k in range(N_STATES):
            W[k, i * N_STATES + k] = CHANNEL_PRIOR_WEIGHT[c]
    base = len(CHANNELS) * N_STATES
    hr, hrv, temp, motion = (base + j for j in range(len(PHYSIO)))
    # arousal from the body: heart rate up, HRV down; movement explains part of it away
    for k, sign in ((ENERGIZED, 1), (TENSE, 1), (CALM, -1), (LOW, -1)):
        W[k, hr] = 0.25 * sign
        W[k, hrv] = -0.25 * sign
        W[k, motion] = -0.15 * sign
    return W


class FusionHead:
    def __init__(self, lr: float = 0.15, shrink: float = 0.05):
        self.W0 = prior_weights()
        self.W = self.W0.copy()
        self.b = np.zeros(N_STATES)
        self.lr = lr
        self.shrink = shrink
        self.n_labels = 0

    def logits(self, f: np.ndarray) -> np.ndarray:
        return self.W @ f + self.b

    def contributions(self, f: np.ndarray) -> dict[str, np.ndarray]:
        """Log-evidence per state contributed by each channel and by the body signals."""
        out = {}
        for i, c in enumerate(CHANNELS):
            sl = slice(i * N_STATES, (i + 1) * N_STATES)
            if np.any(f[sl]):
                out[c] = self.W[:, sl] @ f[sl]
        base = len(CHANNELS) * N_STATES
        if np.any(f[base:]):
            out["body"] = self.W[:, base:] @ f[base:]
        return out

    def update(self, f: np.ndarray, label: int, weight: float = 1.0) -> None:
        z = self.logits(f)
        p = np.exp(z - z.max())
        p /= p.sum()
        g = p.copy()
        g[label] -= 1.0
        self.W -= self.lr * weight * (np.outer(g, f) + self.shrink * (self.W - self.W0))
        self.b -= self.lr * weight * (g + self.shrink * self.b)
        self.n_labels += 1

    def channel_trust(self) -> dict[str, float]:
        """Average diagonal weight per channel: how much this person's channel is trusted now."""
        return {c: float(np.mean([self.W[k, i * N_STATES + k] for k in range(N_STATES)]))
                for i, c in enumerate(CHANNELS)}

    def to_dict(self) -> dict:
        return {"W": self.W.tolist(), "b": self.b.tolist(), "lr": self.lr, "shrink": self.shrink,
                "n_labels": self.n_labels}

    @classmethod
    def from_dict(cls, d: dict) -> "FusionHead":
        h = cls(d["lr"], d["shrink"])
        h.W, h.b, h.n_labels = np.array(d["W"]), np.array(d["b"]), d["n_labels"]
        return h


def context_vector(hour: float, weekday: int) -> np.ndarray:
    a, b = 2 * math.pi * hour / 24, 2 * math.pi * weekday / 7
    return np.array([math.cos(a), math.sin(a), math.cos(b), math.sin(b)])


class SituationMemory:
    """Key = when it happens (time of day, day of week) + what the fused channels say (a probability
    vector, so missing channels do not change the key's shape). Evidence saturates: many similar
    answers count like a confident one, not like a hundred."""

    def __init__(self, bandwidth: float = 0.6, reliability: float = 0.9, context_weight: float = 1.0):
        self.h = bandwidth
        self.cw = context_weight
        self.keys: list[np.ndarray] = []
        self.labels: list[int] = []
        self.llr = math.log(reliability / ((1 - reliability) / (N_STATES - 1)))

    def key(self, proba: np.ndarray, ctx: np.ndarray) -> np.ndarray:
        return np.concatenate([proba, self.cw * ctx])

    def weights(self, k: np.ndarray) -> np.ndarray:
        if not self.keys:
            return np.zeros(0)
        d2 = ((np.asarray(self.keys) - k) ** 2).sum(axis=1)
        return np.exp(-d2 / (2 * self.h ** 2))

    def evidence(self, k: np.ndarray) -> np.ndarray:
        mass = np.zeros(N_STATES)
        for w, a in zip(self.weights(k), self.labels):
            mass[a] += w
        return self.llr * (1.0 - np.exp(-mass))

    def coverage(self, k: np.ndarray) -> float:
        w = self.weights(k)
        return float(w.max()) if len(w) else 0.0

    def add(self, k: np.ndarray, label: int) -> None:
        self.keys.append(k)
        self.labels.append(label)

    def to_dict(self) -> dict:
        return {"h": self.h, "cw": self.cw, "llr": self.llr,
                "keys": [k.tolist() for k in self.keys], "labels": self.labels}

    @classmethod
    def from_dict(cls, d: dict) -> "SituationMemory":
        m = cls(d["h"], 0.9, d["cw"])
        m.llr = d["llr"]
        m.keys = [np.array(k) for k in d["keys"]]
        m.labels = list(d["labels"])
        return m
