"""The four experiments of the simulation.

A. Personalization ladder: generic model, personal baseline, personal head with n answers.
B. Active questions versus random questions at the same budget.
C. Conformal sets: coverage, set size and the speak / ask / quiet split.
D. Drift: a step change in a user's signals (new phone, new job) with a fixed or rolling baseline.

Accuracy is measured against the true state on a held-out final window of each test
user's timeline; questions can only be asked earlier in the timeline.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import conformal as cf
from .data import N_STATES, SimConfig, User, make_population
from .models import PersonalHead, fit_population, population_logp, rolling_transform


@dataclass(frozen=True)
class Protocol:
    n_train: int = 50
    n_calib: int = 15
    n_test: int = 40
    n_enroll: int = 15
    stream_end: int = 80          # questions may be asked in [n_enroll, stream_end)
    eval_start: int = 80          # accuracy measured on [eval_start, n_moments)
    alpha: float = 0.1            # target miscoverage of the conformal sets
    explore: float = 0.1          # share of active questions asked at random moments
    min_gap: int = 2              # minimum moments between two questions


def split(users: list[User], p: Protocol):
    a, b = p.n_train, p.n_train + p.n_calib
    return users[:a], users[a:b], users[b:b + p.n_test]


def _acc(proba: np.ndarray, y: np.ndarray) -> float:
    return float((proba.argmax(axis=1) == y).mean())


def _head_eval(logp: np.ndarray, user: User, idx: list[int], p: Protocol) -> float:
    head = PersonalHead()
    if idx:
        head.fit(logp[idx], user.report[idx])
    ev = slice(p.eval_start, None)
    return _acc(head.predict_proba(logp[ev]), user.state[ev])


def exp_ladder(seed: int, cfg: SimConfig, p: Protocol, budgets=(0, 5, 10, 20, 40)) -> dict:
    rng = np.random.default_rng(seed + 1000)
    users = make_population(p.n_train + p.n_calib + p.n_test, cfg, seed)
    train, _, test = split(users, p)
    generic = fit_population(train, p.n_enroll, centered=False)
    centered = fit_population(train, p.n_enroll, centered=True)
    ev = slice(p.eval_start, None)
    out = {"generic": [], "baseline": []}
    out.update({f"personal_{n}": [] for n in budgets})
    for u in test:
        out["generic"].append(_acc(np.exp(population_logp(generic, u.X[ev])), u.state[ev]))
        Xc = rolling_transform(u.X, p.n_enroll)
        logp = population_logp(centered, Xc)
        H = np.hstack([logp, Xc])
        out["baseline"].append(_acc(np.exp(logp[ev]), u.state[ev]))
        stream = np.arange(p.n_enroll, p.stream_end)
        for n in budgets:
            idx = sorted(rng.choice(stream, size=min(n, len(stream)), replace=False).tolist()) if n else []
            out[f"personal_{n}"].append(_head_eval(H, u, idx, p))
    return {k: float(np.mean(v)) for k, v in out.items()}


def _thresholds(centered, calib: list[User], p: Protocol, per_class: bool) -> np.ndarray:
    P, Y = [], []
    for u in calib:
        Xc = rolling_transform(u.X, p.n_enroll)
        P.append(np.exp(population_logp(centered, Xc[p.n_enroll:])))
        Y.append(u.report[p.n_enroll:])
    return cf.calibrate(np.vstack(P), np.concatenate(Y), p.alpha, per_class)


def exp_active(seed: int, cfg: SimConfig, p: Protocol, budgets=(5, 10, 20)) -> dict:
    rng = np.random.default_rng(seed + 2000)
    users = make_population(p.n_train + p.n_calib + p.n_test, cfg, seed)
    train, calib, test = split(users, p)
    centered = fit_population(train, p.n_enroll, centered=True)
    thr = _thresholds(centered, calib, p, per_class=True)
    out = {}
    for n in budgets:
        acc_r, acc_a, used_a = [], [], []
        for u in test:
            Xc = rolling_transform(u.X, p.n_enroll)
            H = np.hstack([population_logp(centered, Xc), Xc])
            stream = np.arange(p.n_enroll, p.stream_end)
            idx_r = sorted(rng.choice(stream, size=n, replace=False).tolist())
            acc_r.append(_head_eval(H, u, idx_r, p))
            # Active: ask when the conformal set is ambiguous (2-3 states), plus a little exploration.
            head, idx_a, last = PersonalHead(), [], -10
            for t in stream:
                if len(idx_a) >= n:
                    break
                if t - last < p.min_gap:
                    continue
                proba = head.predict_proba(H[t:t + 1])
                sets = cf.prediction_sets(proba, thr)
                ambiguous = cf.decide(sets[0]) != cf.SPEAK
                if ambiguous or rng.random() < p.explore:
                    idx_a.append(int(t))
                    last = t
                    head.fit(H[idx_a], u.report[idx_a])
            acc_a.append(_head_eval(H, u, idx_a, p))
            used_a.append(len(idx_a))
        out[f"random_{n}"] = float(np.mean(acc_r))
        out[f"active_{n}"] = float(np.mean(acc_a))
        out[f"active_{n}_labels_used"] = float(np.mean(used_a))
    return out


def exp_conformal(seed: int, cfg: SimConfig, p: Protocol) -> dict:
    users = make_population(p.n_train + p.n_calib + p.n_test, cfg, seed)
    train, calib, test = split(users, p)
    centered = fit_population(train, p.n_enroll, centered=True)
    out = {}
    for name, per_class in (("global", False), ("per_state", True)):
        thr = _thresholds(centered, calib, p, per_class)
        P, Y = [], []
        for u in test:
            Xc = rolling_transform(u.X, p.n_enroll)
            P.append(np.exp(population_logp(centered, Xc[p.n_enroll:])))
            Y.append(u.report[p.n_enroll:])
        P, Y = np.vstack(P), np.concatenate(Y)
        sets = cf.prediction_sets(P, thr)
        decisions = [cf.decide(s) for s in sets]
        out[f"{name}_coverage"] = cf.coverage(sets, Y)
        out[f"{name}_worst_state_coverage"] = float(min(cf.coverage(sets[Y == k], Y[Y == k]) for k in range(N_STATES)))
        out[f"{name}_mean_set_size"] = float(sets.sum(axis=1).mean())
        for d in (cf.SPEAK, cf.ASK, cf.QUIET):
            out[f"{name}_share_{d}"] = float(np.mean([x == d for x in decisions]))
        speak = np.array([x == cf.SPEAK for x in decisions])
        out[f"{name}_accuracy_when_speaking"] = float((P[speak].argmax(axis=1) == Y[speak]).mean()) if speak.any() else float("nan")
    return out


def exp_drift(seed: int, cfg: SimConfig, p: Protocol, shift_at: int = 60, shift_sd: float = 1.5) -> dict:
    rng = np.random.default_rng(seed + 3000)
    users = make_population(p.n_train + p.n_calib + p.n_test, cfg, seed)
    train, _, test = split(users, p)
    centered = fit_population(train, p.n_enroll, centered=True)
    ev = slice(p.eval_start, None)
    out = {"fixed_baseline": [], "rolling_baseline": [], "no_shift_rolling": []}
    for u in test:
        X = u.X.copy()
        X[shift_at:] += rng.normal(0, shift_sd, size=X.shape[1])
        for name, alpha, data in (("fixed_baseline", 0.0, X), ("rolling_baseline", 0.05, X), ("no_shift_rolling", 0.05, u.X)):
            logp = population_logp(centered, rolling_transform(data, p.n_enroll, alpha))
            out[name].append(_acc(np.exp(logp[ev]), u.state[ev]))
    return {k: float(np.mean(v)) for k, v in out.items()}


def exp_cohort(seed: int, cfg: SimConfig, p: Protocol, cohort_sizes=(10, 25, 50),
               questions: int = 20, public_shift: float = 0.8, cohort_weight: float = 3.0) -> dict:
    """E. From today's approach to SOUL-Calibrate, measured on users who are never asked anything.

    * today: a generic model trained on public data that differs from real users (domain shift);
    * + personal baseline: the same model on person-normalised signals (no labels needed);
    * + cohort: a private group answers `questions` questions each; their answers retrain the shared model;
    * full loop (reference): a new user who also answers questions gets a personal head on top.
    """
    rng = np.random.default_rng(seed + 4000)
    public = make_population(p.n_train, cfg, seed=seed + 11, world_seed=seed, domain_shift=public_shift)
    real = make_population(max(cohort_sizes) + p.n_test, cfg, seed=seed + 22, world_seed=seed)
    cohort_pool, test = real[:max(cohort_sizes)], real[max(cohort_sizes):]
    ev = slice(p.eval_start, None)
    stream = np.arange(p.n_enroll, p.stream_end)

    def evaluate(model, centered: bool) -> float:
        accs = []
        for u in test:
            X = rolling_transform(u.X, p.n_enroll) if centered else u.X
            accs.append(_acc(np.exp(population_logp(model, X[ev])), u.state[ev]))
        return float(np.mean(accs))

    out = {
        "today_generic": evaluate(fit_population(public, p.n_enroll, centered=False), False),
    }
    base = fit_population(public, p.n_enroll, centered=True)
    out["plus_baseline"] = evaluate(base, True)
    # Answers collected from the private cohort (noisy self-reports at question moments).
    answers = []
    for u in cohort_pool:
        idx = rng.choice(stream, size=questions, replace=False)
        answers.append((rolling_transform(u.X, p.n_enroll)[idx], u.report[idx]))
    best = base
    for m in cohort_sizes:
        Xa = np.vstack([a[0] for a in answers[:m]])
        ya = np.concatenate([a[1] for a in answers[:m]])
        model = fit_population(public, p.n_enroll, centered=True, extra=(Xa, ya, cohort_weight))
        out[f"plus_cohort_{m}"] = evaluate(model, True)
        best = model
    # Reference: the full loop for a user who answers 20 questions, on top of the largest cohort model.
    accs = []
    for u in test:
        Xc = rolling_transform(u.X, p.n_enroll)
        H = np.hstack([population_logp(best, Xc), Xc])
        idx = sorted(rng.choice(stream, size=20, replace=False).tolist())
        accs.append(_head_eval(H, u, idx, p))
    out["full_loop_20_answers"] = float(np.mean(accs))
    return out
