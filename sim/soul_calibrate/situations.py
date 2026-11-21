"""Recurring situations: does a question improve the next reading of the same situation?

The earlier active-question experiment measured accuracy on later moments in general.
This module asks a narrower question, closer to how a person lives: the same
situations come back (the evening after a long work call, the gym, dinner with a
partner). Each situation has a fixed true state for that person and a personal signal
signature. A generic model narrows the field to two or three states; the user's answer
should then make every later reading of *that* situation more precise.

World
-----
* Four states. Each state has a population prototype in feature space.
* Each user distorts the prototypes in a personal way (expression style), so the
  population model is often torn between two or three states for that user.
* Each user has a few recurring situations: a fixed true state, a personal signature
  (prototype + personal distortion + a situation-specific component) and a frequency.
* An occurrence is the signature plus measurement noise. Features are already centred
  on the person's baseline (enrollment done).

Personal memory
---------------
Every answer is stored with the signal it was given for. A new reading adds, to the
population log-probabilities, the evidence of the stored answers weighted by a Gaussian
kernel on signal distance. The model never sees the situation's identity: it can only
recognise a situation by its signal.

Questions
---------
* closed: the options are the states of the conformal set (plus "neither": then the
  user answers openly);
* open: the user names the state freely, with a higher error.

Policies, at the same budget of one question a day at most:
* never: no questions (today's approach);
* random: a random moment each day;
* ambiguous: the first moment of the day whose set has two or three states;
* ambiguous + new: as ambiguous, but skip moments the memory already covers
  (a simple value-of-information rule: do not ask what you already know).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LogisticRegression

from .conformal import calibrate, prediction_sets

N_STATES = 4
NEIGHBOURS = {0: (1, 3), 1: (0, 2), 2: (1, 3), 3: (0, 2)}


@dataclass(frozen=True)
class SituationConfig:
    n_features: int = 16
    n_situations: int = 6          # recurring situations per person
    moments_per_day: int = 4
    calib_days: int = 7            # the calibration week, with questions
    test_days: int = 5             # afterwards: no questions, readings only
    separation: float = 0.15       # distance between population prototypes (per feature)
    personal_sd: float = 0.45      # personal distortion of the prototypes
    situation_sd: float = 0.2      # what makes one situation different from another of the same state
    noise_sd: float = 0.35         # moment-to-moment measurement noise
    stability: float = 1.0         # probability that a situation brings its usual state
    closed_error: float = 0.05     # wrong pick among offered options
    open_error: float = 0.15       # wrong state named in an open answer
    alpha: float = 0.1             # conformal miscoverage
    bandwidth: float | None = None # kernel bandwidth; None = estimated from the noise
    covered_weight: float = 0.5    # "ambiguous + new" skips moments already this covered
    public_shift: float = 0.0      # how much public training data differ from the product's users
    aci_gamma: float = 0.0         # adaptive conformal step on the person's own answers (0 = off)


@dataclass
class Person:
    protos: np.ndarray       # (4, d) the person's own version of each state
    component: np.ndarray    # (S, d) what is specific to each situation
    truth: np.ndarray        # (S,) usual state of each situation
    freq: np.ndarray         # (S,)

    @property
    def signatures(self) -> np.ndarray:
        return self.protos[self.truth] + self.component


def _world(cfg: SituationConfig, world_seed: int) -> np.ndarray:
    rng = np.random.default_rng(world_seed)
    return rng.normal(0.0, cfg.separation, size=(N_STATES, cfg.n_features))


def make_person(cfg: SituationConfig, protos: np.ndarray, rng: np.random.Generator) -> Person:
    personal = protos + rng.normal(0.0, cfg.personal_sd, size=protos.shape)
    truth = rng.integers(0, N_STATES, size=cfg.n_situations)
    component = rng.normal(0.0, cfg.situation_sd, size=(cfg.n_situations, cfg.n_features))
    freq = rng.dirichlet(np.full(cfg.n_situations, 2.0))
    return Person(protos=personal, component=component, truth=truth, freq=freq)


def occurrences(cfg: SituationConfig, person: Person, n: int, rng: np.random.Generator):
    """Situation, signal and true state of n moments.

    With probability 1 - stability the situation brings a neighbouring state instead
    of its usual one, and the signal follows that state.
    """
    s = rng.choice(len(person.truth), size=n, p=person.freq)
    y = person.truth[s].copy()
    for t in np.flatnonzero(rng.random(n) >= cfg.stability):
        y[t] = rng.choice(NEIGHBOURS[int(y[t])])
    X = person.protos[y] + person.component[s] + rng.normal(0.0, cfg.noise_sd, size=(n, cfg.n_features))
    return s, X, y


def population_model(cfg: SituationConfig, protos: np.ndarray, n_people: int, rng: np.random.Generator):
    Xs, ys = [], []
    for _ in range(n_people):
        p = make_person(cfg, protos, rng)
        _, X, y = occurrences(cfg, p, 20, rng)
        Xs.append(X)
        ys.append(y)
    model = LogisticRegression(max_iter=2000, C=1.0)
    model.fit(np.vstack(Xs), np.concatenate(ys))
    return model


def answer(true_state: int, offered: np.ndarray | None, cfg: SituationConfig, rng: np.random.Generator) -> int:
    """The user's answer. offered = boolean mask of the options (closed question) or None (open)."""
    if offered is not None and offered[true_state]:
        if rng.random() < cfg.closed_error:
            others = np.flatnonzero(offered & (np.arange(N_STATES) != true_state))
            if len(others):
                return int(rng.choice(others))
        return true_state
    # open question, or "neither" followed by an open answer
    if rng.random() < cfg.open_error:
        return int(rng.choice(NEIGHBOURS[true_state]))
    return true_state


class Memory:
    """Answers stored with their signals; evidence spreads to similar signals."""

    def __init__(self, bandwidth: float, reliability: float = 0.9, half_life_days: float | None = None,
                 contradiction_reset: bool = False):
        self.h = bandwidth
        self.X: list[np.ndarray] = []
        self.a: list[int] = []
        self.t: list[float] = []
        self.now = 0.0
        self.half_life = half_life_days
        self.reset = contradiction_reset
        self.strength: list[float] = []
        self.llr = float(np.log(reliability / ((1 - reliability) / (N_STATES - 1))))

    def weights(self, x: np.ndarray) -> np.ndarray:
        if not self.X:
            return np.zeros(0)
        d2 = ((np.asarray(self.X) - x) ** 2).sum(axis=1)
        w = np.exp(-d2 / (2 * self.h ** 2))
        if self.half_life:
            # older answers count less: a situation can change its usual state
            w = w * 0.5 ** ((self.now - np.asarray(self.t)) / self.half_life)
        return w * np.asarray(self.strength)

    def coverage_weight(self, x: np.ndarray) -> float:
        w = self.weights(x)
        return float(w.max()) if len(w) else 0.0

    def adjust(self, logp: np.ndarray, x: np.ndarray) -> np.ndarray:
        w = self.weights(x)
        out = logp.copy()
        for wi, ai in zip(w, self.a):
            out[ai] += wi * self.llr
        out -= out.max()
        p = np.exp(out)
        return p / p.sum()

    def add(self, x: np.ndarray, a: int) -> None:
        if self.reset and self.X:
            # a new answer that contradicts nearby old ones weakens them, locally:
            # the situation may have changed its meaning, the rest of memory is untouched
            w = self.weights(x)
            for i, (wi, ai) in enumerate(zip(w, self.a)):
                if ai != a:
                    self.strength[i] *= (1.0 - min(1.0, wi))
        self.strength.append(1.0)
        self.X.append(x)
        self.a.append(a)
        self.t.append(self.now)


POLICIES = ("never", "random", "ambiguous", "ambiguous_new")


def run_person(cfg: SituationConfig, model, thresholds, person: Person, stream, policy: str,
               qtype: str, bandwidth: float, rng: np.random.Generator,
               half_life_days: float | None = None, explore_p: float = 0.0, correct_p: float = 0.0,
               contradiction_reset: bool = False) -> dict:
    """One person through the calibration week and the test days under one policy.

    half_life_days: older answers fade (None = they never fade).
    explore_p: chance per day of one check-in question at a random moment, even when the model is sure.
    correct_p: chance that the user taps "not quite" on a wrong confident reading and names the state.
    """
    s_all, X_all, y_all = stream
    days = cfg.calib_days + cfg.test_days
    mem = Memory(bandwidth, reliability=1 - (cfg.closed_error if qtype == "closed" else cfg.open_error),
                 half_life_days=half_life_days, contradiction_reset=contradiction_reset)
    asked_situations: set[int] = set()
    delta = 0.0   # personal shift of the conformal thresholds, learned from the person's own answers
    log = []
    for day in range(days):
        idx = range(day * cfg.moments_per_day, (day + 1) * cfg.moments_per_day)
        asked_today = False
        random_pick = int(rng.integers(0, cfg.moments_per_day))
        explore_today = explore_p > 0 and rng.random() < explore_p
        for j, t in enumerate(idx):
            mem.now = day + j / cfg.moments_per_day
            x, s = X_all[t], int(s_all[t])
            y = int(y_all[t])
            logp = model.predict_log_proba(x[None, :])[0]
            proba = mem.adjust(logp, x)
            st = prediction_sets(proba[None, :], np.clip(thresholds + delta, 0.0, 1.0))[0]
            size = int(st.sum())
            pred = int(proba.argmax())
            # who had been asked about this situation *before* this reading
            seen_before = s in asked_situations
            log.append({"day": day, "s": s, "correct": pred == y, "size": size,
                        "in_set": bool(st[y]), "after_asked": seen_before, "test": day >= cfg.calib_days})
            if correct_p and size == 1 and pred != y and rng.random() < correct_p:
                # a user-initiated correction of a confident reading: an open answer
                mem.add(x, answer(y, None, cfg, rng))
                log[-1]["corrected"] = True
            if day >= cfg.calib_days or asked_today or policy == "never":
                continue
            ask = False
            if explore_today and j == random_pick:
                ask = True
            elif policy == "random":
                ask = j == random_pick
            elif policy == "ambiguous":
                ask = 2 <= size <= 3
            elif policy == "ambiguous_new":
                ask = 2 <= size <= 3 and mem.coverage_weight(x) < cfg.covered_weight
            if ask:
                offered = st if (qtype == "closed" and size <= 3) else None
                a = answer(y, offered, cfg, rng)
                if cfg.aci_gamma:
                    # adaptive conformal inference: a miss widens this person's sets, a hit narrows them
                    delta += cfg.aci_gamma * ((0.0 if st[a] else 1.0) - cfg.alpha)
                mem.add(x, a)
                asked_situations.add(s)
                asked_today = True
                log[-1]["asked"] = True
    return {"log": log, "n_asked": len(mem.a)}


def exp_situations(seed: int, cfg: SituationConfig = SituationConfig(), n_people: int = 60,
                   qtypes=("closed", "open")) -> dict:
    """Same world, same people, same moments: only the questions differ between policies."""
    protos = _world(cfg, world_seed=1000 + seed)
    rng = np.random.default_rng(seed)
    # The shared model only sees public data (voice and face of users are never used for
    # training); with public_shift > 0 those data map states onto signals differently.
    public = protos + rng.normal(0.0, cfg.public_shift, size=protos.shape) if cfg.public_shift > 0 else protos
    model = population_model(cfg, public, n_people=150, rng=rng)

    # conformal calibration on other people
    Xc, yc = [], []
    for _ in range(60):
        p = make_person(cfg, public, rng)
        _, X, y = occurrences(cfg, p, 10, rng)
        Xc.append(X)
        yc.append(y)
    thresholds = calibrate(model.predict_proba(np.vstack(Xc)), np.concatenate(yc), cfg.alpha, per_class=True)

    h = cfg.bandwidth or float(cfg.noise_sd * np.sqrt(2 * cfg.n_features))
    n_moments = (cfg.calib_days + cfg.test_days) * cfg.moments_per_day
    people = [make_person(cfg, protos, rng) for _ in range(n_people)]
    streams = [occurrences(cfg, p, n_moments, rng) for p in people]

    logs: dict[tuple[str, str], list] = {}
    for qtype in qtypes:
        for policy in POLICIES:
            if policy == "never" and qtype != qtypes[0]:
                continue
            key = ("none" if policy == "never" else qtype, policy)
            entries = []
            for i, (p, st) in enumerate(zip(people, streams)):
                prng = np.random.default_rng([seed, i, POLICIES.index(policy), qtypes.index(qtype)])
                out = run_person(cfg, model, thresholds, p, st, policy, qtype, h, prng)
                for e in out["log"]:
                    e["person"] = i
                entries.extend(out["log"])
            logs[key] = entries
    return summarise(logs, cfg)


def summarise(logs: dict, cfg: SituationConfig) -> dict:
    never = logs[("none", "never")]
    base_correct = np.array([e["correct"] for e in never])
    days = cfg.calib_days + cfg.test_days
    res: dict = {}
    for (qtype, policy), entries in logs.items():
        name = policy if policy == "never" else f"{policy}/{qtype}"
        correct = np.array([e["correct"] for e in entries])
        test = np.array([e["test"] for e in entries])
        after = np.array([e["after_asked"] for e in entries])
        size = np.array([e["size"] for e in entries])
        day = np.array([e["day"] for e in entries])
        asked = np.array([e.get("asked", False) for e in entries])
        in_set = np.array([e["in_set"] for e in entries])
        speak = size == 1
        r = {
            "test_accuracy": float(correct[test].mean()),
            "test_coverage": float(in_set[test].mean()),
            "test_speak_share": float(speak[test].mean()),
            "test_speak_accuracy": float(correct[test & speak].mean()) if (test & speak).any() else float("nan"),
            "questions_per_person": float(asked.sum() / (len(entries) / (days * cfg.moments_per_day))),
            # the same situation, read again after the user answered about it,
            # compared with the very same moments when nobody asked
            "same_situation_after": float(correct[after].mean()) if after.any() else float("nan"),
            "same_situation_without_questions": float(base_correct[after].mean()) if after.any() else float("nan"),
            # situations the policy never asked about (spill-over)
            "other_situations": float(correct[~after & (day > 0)].mean()),
            "other_situations_without_questions": float(base_correct[~after & (day > 0)].mean()),
            "share_moments_after_asked": float(after.mean()),
            "accuracy_by_day": [float(correct[day == d].mean()) for d in range(days)],
            "set_size_by_day": [float(size[day == d].mean()) for d in range(days)],
            "speak_by_day": [float((size[day == d] == 1).mean()) for d in range(days)],
        }
        res[name] = r
    return res


def exp_life_change(seed: int, cfg: SituationConfig = SituationConfig(), n_people: int = 60,
                    n_changed: int = 2, before_days: int = 7, after_days: int = 14,
                    visibility: float = 1.0) -> dict:
    """A life change: after the calibration week, some situations change their usual state for good.

    Questions stay allowed (closed, at ambiguous moments, at most one a day) all along. Variants add
    fading answers, a small share of check-in questions, and user corrections of confident readings.
    visibility = how much the signal moves with the new state (1 = fully, 0.5 = halfway: the situation
    still looks partly like before, so old answers mislead).
    """
    protos = _world(cfg, world_seed=1000 + seed)
    rng = np.random.default_rng(seed)
    model = population_model(cfg, protos, n_people=150, rng=rng)
    Xc, yc = [], []
    for _ in range(60):
        p = make_person(cfg, protos, rng)
        _, X, y = occurrences(cfg, p, 10, rng)
        Xc.append(X)
        yc.append(y)
    thresholds = calibrate(model.predict_proba(np.vstack(Xc)), np.concatenate(yc), cfg.alpha, per_class=True)
    h = cfg.bandwidth or float(cfg.noise_sd * np.sqrt(2 * cfg.n_features))
    run_cfg = SituationConfig(**{**cfg.__dict__, "calib_days": before_days + after_days, "test_days": 0})
    m = cfg.moments_per_day
    people, streams, changed_sets = [], [], []
    for _ in range(n_people):
        p = make_person(cfg, protos, rng)
        changed = rng.choice(cfg.n_situations, size=n_changed, replace=False)
        p2 = Person(protos=p.protos, component=p.component, truth=p.truth.copy(), freq=p.freq)
        for c in changed:
            p2.truth[c] = int(rng.choice([k for k in range(N_STATES) if k != p.truth[c]]))
        s1, X1, y1 = occurrences(cfg, p, before_days * m, rng)
        s2, X2, y2 = occurrences(cfg, p2, after_days * m, rng)
        if visibility < 1.0:
            old = p.truth[s2]
            moved = np.isin(s2, changed)
            X2[moved] += (1 - visibility) * (p.protos[old[moved]] - p.protos[y2[moved]])
        people.append(p)
        streams.append((np.concatenate([s1, s2]), np.vstack([X1, X2]), np.concatenate([y1, y2])))
        changed_sets.append(set(int(c) for c in changed))
    variants = {
        "answers never fade": {},
        "+ check-in questions (15% of days)": {"explore_p": 0.15},
        "+ user corrections (30% of wrong readings)": {"correct_p": 0.3},
        "+ answers fade (half-life 7 days)": {"half_life_days": 7.0},
        "+ contradicted answers weaken": {"contradiction_reset": True},
    }
    res = {}
    for vi, (name, kw) in enumerate(variants.items()):
        changed_by_day = np.zeros(after_days)
        changed_n = np.zeros(after_days)
        unchanged = []
        questions = 0
        for i, (p, st) in enumerate(zip(people, streams)):
            prng = np.random.default_rng([seed, i, vi, 7])
            out = run_person(run_cfg, model, thresholds, p, st, "ambiguous", "closed", h, prng, **kw)
            questions += sum(1 for e in out["log"] if e.get("asked")) + sum(1 for e in out["log"] if e.get("corrected"))
            for e in out["log"]:
                if e["day"] < before_days:
                    continue
                d = e["day"] - before_days
                if e["s"] in changed_sets[i]:
                    changed_by_day[d] += e["correct"]
                    changed_n[d] += 1
                else:
                    unchanged.append(e["correct"])
        by_day = (changed_by_day / np.maximum(changed_n, 1)).tolist()
        res[name] = {
            "changed_first_week": float(np.mean(by_day[:7])),
            "changed_second_week": float(np.mean(by_day[7:])),
            "unchanged": float(np.mean(unchanged)),
            "interactions_per_person": questions / n_people,
            "changed_by_day": by_day,
        }
    return res
