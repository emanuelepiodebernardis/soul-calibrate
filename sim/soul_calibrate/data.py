"""Synthetic users whose signals depend more on who they are than on how they feel.

Each user has a latent affect trajectory (valence, arousal) that follows an AR(1)
process around a personal mean. The observed features mix three things, in the
proportions that make the real problem hard:

* a large personal offset (voice timbre, resting heart rate): between-person variance;
* a personal expression gain (how strongly this person's signals move with affect);
* measurement noise.

The momentary state is one of four quadrants of the valence/arousal plane, and the
user's self-report is that state with some reporting error, which is the label
the product would collect.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

STATES = ("calm", "energized", "tense", "low")
N_STATES = len(STATES)


@dataclass(frozen=True)
class SimConfig:
    n_features: int = 16
    n_moments: int = 120          # about 40 days at 3 moments a day
    offset_sd: float = 3.0        # between-person offset: dominates the raw signal
    gain_sd: float = 1.0          # person-specific expression style
    noise_sd: float = 1.0
    ar_phi: float = 0.7
    affect_sd: float = 0.8
    mean_affect_sd: float = 0.5
    report_error: float = 0.15    # probability the self-report names a neighbouring state


@dataclass
class User:
    uid: int
    X: np.ndarray                 # (n_moments, n_features)
    state: np.ndarray             # true state per moment
    report: np.ndarray            # self-reported state per moment (noisy label)
    meta: dict = field(default_factory=dict)


def state_from_affect(valence: np.ndarray, arousal: np.ndarray) -> np.ndarray:
    """Quadrant of the valence/arousal plane: calm, energized, tense, low."""
    pos = valence >= 0
    high = arousal >= 0
    out = np.empty(valence.shape, dtype=int)
    out[pos & ~high] = 0
    out[pos & high] = 1
    out[~pos & high] = 2
    out[~pos & ~high] = 3
    return out


def _neighbour(state: int, rng: np.random.Generator) -> int:
    # Neighbours share one axis with the true quadrant (a plausible reporting slip).
    neighbours = {0: (1, 3), 1: (0, 2), 2: (1, 3), 3: (0, 2)}
    return int(rng.choice(neighbours[state]))


def make_population(n_users: int, cfg: SimConfig, seed: int,
                    world_seed: int | None = None, domain_shift: float = 0.0) -> list[User]:
    """Users of one population.

    world_seed fixes how affect maps onto signals in general (shared by every
    population of the same world); domain_shift perturbs that mapping, to imitate
    a public dataset (acted speech, other microphones, other people) that differs
    from the product's real users.
    """
    rng = np.random.default_rng(seed)
    world = np.random.default_rng(seed if world_seed is None else world_seed)
    pop_gain = world.normal(0.0, 1.0, size=(cfg.n_features, 2))
    if domain_shift > 0:
        pop_gain = pop_gain + rng.normal(0.0, domain_shift, size=pop_gain.shape)
    users = []
    for uid in range(n_users):
        mu = rng.normal(0.0, cfg.mean_affect_sd, size=2)
        z = np.zeros((cfg.n_moments, 2))
        z[0] = mu + rng.normal(0, cfg.affect_sd, size=2)
        for t in range(1, cfg.n_moments):
            z[t] = mu + cfg.ar_phi * (z[t - 1] - mu) + rng.normal(0, cfg.affect_sd, size=2)
        offset = rng.normal(0.0, cfg.offset_sd, size=cfg.n_features)
        gain = pop_gain + rng.normal(0.0, cfg.gain_sd, size=pop_gain.shape)
        X = offset + z @ gain.T + rng.normal(0.0, cfg.noise_sd, size=(cfg.n_moments, cfg.n_features))
        state = state_from_affect(z[:, 0], z[:, 1])
        report = state.copy()
        slips = rng.random(cfg.n_moments) < cfg.report_error
        for t in np.flatnonzero(slips):
            report[t] = _neighbour(int(state[t]), rng)
        users.append(User(uid=uid, X=X, state=state, report=report, meta={"mean_affect": mu}))
    return users
