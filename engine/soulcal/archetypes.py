"""Archetypes: learn from consenting users how people differ, so new people need fewer questions (docs/25).

A FUTURE-PHASE PROTOTYPE, tested only on synthetic people.

1. Each consenting user of the cohort has an engine trained on their own answers, and a few days of
   readings. From those readings we compute a label-free signature: how each channel usually looks for
   them (a serious face, a flat voice) and how often their words disagree with their expression (masking).
2. Signatures are grouped with k-means into archetypes. Each archetype keeps the average fusion head of its
   members: how much to trust each channel, and how, for people like them.
3. A new person gives a few days of readings with no questions needed; they are matched to the nearest
   archetype and their engine starts from that archetype's head instead of the generic one. Questions keep
   correcting it, and a person far from every archetype keeps the generic start.

Only the signature and the averaged heads are needed: nobody's readings leave their phone, and the cohort
requires the separate research consent (docs/15).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .engine import EngineConfig, SoulEngine
from .schema import STATES, Profile, Reading

CHANNEL_NAMES = ("face", "voice", "text")


def _js(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p + q)

    def kl(a, b):
        a, b = np.maximum(a, 1e-9), np.maximum(b, 1e-9)
        return float(np.sum(a * np.log2(a / b)))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def signature(readings: list[Reading]) -> np.ndarray:
    """Label-free signature from a few days of readings: the usual probabilities of each channel, and how
    much the words disagree with face and voice (mean and upper quartile of Jensen-Shannon)."""
    parts = []
    for c in CHANNEL_NAMES:
        rows = [np.array([r.channel(c)[s] for s in STATES]) for r in readings if r.channel(c) is not None]
        parts.append(np.mean(rows, axis=0) if rows else np.full(len(STATES), 1 / len(STATES)))
    js = []
    for r in readings:
        if r.text is None:
            continue
        expr = [np.array([r.channel(c)[s] for s in STATES]) for c in ("face", "voice") if r.channel(c) is not None]
        if expr:
            js.append(_js(np.array([r.text[s] for s in STATES]), np.mean(expr, axis=0)))
    js = np.array(js) if js else np.zeros(1)
    return np.concatenate(parts + [[js.mean(), np.quantile(js, 0.75)]])


@dataclass
class Archetype:
    centroid: np.ndarray
    W: np.ndarray
    b: np.ndarray
    members: int
    radius: float                     # distance within which a new person counts as a fit


@dataclass
class ArchetypeModel:
    archetypes: list[Archetype]
    mean: np.ndarray
    scale: np.ndarray

    def _z(self, sig: np.ndarray) -> np.ndarray:
        return (sig - self.mean) / self.scale

    def match(self, sig: np.ndarray) -> tuple[int | None, float]:
        """Nearest archetype and its distance; None when the person fits no archetype."""
        z = self._z(sig)
        d = [float(np.linalg.norm(z - a.centroid)) for a in self.archetypes]
        k = int(np.argmin(d))
        return (k if d[k] <= self.archetypes[k].radius else None), d[k]

    def start_engine(self, profile: Profile, first_days: list[Reading],
                     config: EngineConfig | None = None) -> tuple[SoulEngine, int | None]:
        """An engine for a new person that starts from their archetype's head (generic if none fits).
        The archetype's head also becomes the prior the head shrinks towards."""
        eng = SoulEngine(profile, config)
        k, _ = self.match(signature(first_days))
        if k is not None:
            a = self.archetypes[k]
            eng.head.W, eng.head.W0, eng.head.b = a.W.copy(), a.W.copy(), a.b.copy()
        return eng, k


def _kmeans(X: np.ndarray, k: int, seed: int = 0, iters: int = 100) -> np.ndarray:
    rng = np.random.default_rng(seed)
    C = X[[int(rng.integers(len(X)))]]
    while len(C) < k:                                    # k-means++ initialisation
        d = np.min(((X[:, None] - C[None]) ** 2).sum(-1), axis=1)
        C = np.vstack([C, X[rng.choice(len(X), p=d / d.sum())]])
    for _ in range(iters):
        lab = np.argmin(((X[:, None] - C[None]) ** 2).sum(-1), axis=1)
        new = np.array([X[lab == j].mean(0) if np.any(lab == j) else C[j] for j in range(k)])
        if np.allclose(new, C):
            break
        C = new
    return np.argmin(((X[:, None] - C[None]) ** 2).sum(-1), axis=1)


def fit(cohort: list[tuple[list[Reading], SoulEngine]], k: int = 3, seed: int = 0,
        radius_quantile: float = 0.95, radius_margin: float = 1.5) -> ArchetypeModel:
    """Build archetypes from consenting users: (their first days of readings, their trained engine)."""
    sigs = np.array([signature(r) for r, _ in cohort])
    mean, scale = sigs.mean(0), sigs.std(0) + 1e-6
    Z = (sigs - mean) / scale
    lab = _kmeans(Z, k, seed)
    out = []
    for j in range(k):
        idx = np.where(lab == j)[0]
        if len(idx) == 0:
            continue
        c = Z[idx].mean(0)
        dist = np.linalg.norm(Z[idx] - c, axis=1)
        out.append(Archetype(centroid=c,
                             W=np.mean([cohort[i][1].head.W for i in idx], axis=0),
                             b=np.mean([cohort[i][1].head.b for i in idx], axis=0),
                             members=len(idx),
                             radius=float(np.quantile(dist, radius_quantile) * radius_margin + 1e-6)))
    return ArchetypeModel(out, mean, scale)


# ----------------------------------------------------------------------------------------------
# Synthetic check (python -m soulcal archetypes)

TYPES = {
    "serious face": dict(face_bias=(-0.3, -0.5, 1.2, 0.2), voice_bias=(0, 0, 0, 0), mask_prob=0.1),
    "flat voice": dict(face_bias=(0, 0, 0, 0), voice_bias=(0.0, -0.6, 0.0, 0.9), mask_prob=0.1),
    "masks with words": dict(face_bias=(0, 0, 0, 0), voice_bias=(0, 0, 0, 0), mask_prob=0.7),
}
NEW_TYPE = {"smiling face (not in the cohort)": dict(face_bias=(0.8, 0.6, -0.8, -0.3), voice_bias=(0, 0, 0, 0), mask_prob=0.0)}


def _person(kind: dict, uid: str, rng: np.random.Generator):
    from .synthetic import Person
    return Person(user_id=uid,
                  face_bias=tuple(np.array(kind["face_bias"]) + rng.normal(0, 0.15, 4)),
                  voice_bias=tuple(np.array(kind["voice_bias"]) + rng.normal(0, 0.15, 4)),
                  mask_prob=float(np.clip(kind["mask_prob"] + rng.normal(0, 0.05), 0, 1)),
                  hr_rest=float(rng.normal(66, 8)), hrv_rest=float(rng.normal(50, 12)))


def synthetic_check(seeds: int = 10, cohort_per_type: int = 8, new_per_type: int = 8, cohort_weeks: int = 6,
                    new_weeks: int = 4, first_days: int = 4) -> dict:
    """Weekly accuracy of new people with three starts: generic, one pooled cohort head, nearest archetype.
    All three keep asking up to 1 question a day. The pooled start is the control: archetypes are only worth
    it if they beat it."""
    from .run import run_stream
    from .synthetic import SLOTS, generate
    cfg = EngineConfig()
    n_first = first_days * len(SLOTS)
    out: dict = {}
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        cohort = []
        for name, kind in TYPES.items():
            for i in range(cohort_per_type):
                p = _person(kind, f"cohort-{name}-{i}", rng)
                r, y, _ = generate(days=7 * cohort_weeks, seed=int(rng.integers(1e9)), person=p)
                cohort.append((r[:n_first], run_stream(r, y, Profile(p.user_id), cfg, seed=i).engine))
        model = fit(cohort, k=len(TYPES), seed=seed)
        pooled = fit(cohort, k=1, seed=seed, radius_margin=1e6)
        for name, kind in {**TYPES, **NEW_TYPE}.items():
            o = out.setdefault(name, {"generic": [], "pooled": [], "archetype": [], "matched": []})
            for i in range(new_per_type):
                p = _person(kind, f"new-{name}-{i}", rng)
                r, y, _ = generate(days=7 * new_weeks, seed=int(rng.integers(1e9)), person=p)
                gen = run_stream(r, y, Profile(p.user_id), cfg, seed=i)
                eng, k = model.start_engine(Profile(p.user_id), r[:n_first], cfg)
                arc = run_stream(r, y, Profile(p.user_id), cfg, seed=i, engine=eng)
                eng_p, _ = pooled.start_engine(Profile(p.user_id), r[:n_first], cfg)
                pool = run_stream(r, y, Profile(p.user_id), cfg, seed=i, engine=eng_p)
                o["generic"].append([w["accuracy"] for w in gen.weekly])
                o["pooled"].append([w["accuracy"] for w in pool.weekly])
                o["archetype"].append([w["accuracy"] for w in arc.weekly])
                o["matched"].append(k is not None)
    return {name: {"generic": np.mean(v["generic"], 0).tolist(), "pooled": np.mean(v["pooled"], 0).tolist(),
                   "archetype": np.mean(v["archetype"], 0).tolist(),
                   "matched": float(np.mean(v["matched"]))} for name, v in out.items()}
