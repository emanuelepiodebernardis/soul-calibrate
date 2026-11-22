"""Coarse to fine: start with the four main states, open the intermediate ones once readings are reliable.

The person really lives eight states on the valence x arousal circle (four main states, the quadrants, and
an intermediate state between each pair). The question is how to show and ask about them:

* fine from day one: readings and questions use all eight states from the start;
* coarse to fine: readings and questions use the four main states first (an intermediate state is answered
  with one of its two neighbouring main states), then switch to eight states on a fixed day or as soon as the
  person's recent answers agree with the readings;
* coarse only: four main states forever (the reference for how precise a coarse reading is);
* per reading: questions use all eight states from day one, but each reading is shown at the level of detail
  the model is sure of: the fine state when only one fine state is plausible, otherwise the main state when
  only one main state is plausible ("say what you know at the level you know it").

Coarse answers are not wasted after the switch: each one is stored as evidence for its main state and,
half as strongly, for the two intermediate states next to it.

"Displayed precision" is what the user experiences: the reading is right at the level of detail shown that
day (four states before the switch, eight after). Every reading is scored before the model learns from it.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from . import situations as S

K = 8
MAIN = (0, 2, 4, 6)                   # with 8 states, the even states are the quadrant (main) states
# intermediate state i (odd) sits between main states i-1 and i+1


def coarse_of(fine: int, rng: np.random.Generator) -> int:
    """Index 0-3 of the main state a person names for a fine state (an intermediate one: either neighbour)."""
    if fine % 2 == 0:
        return fine // 2
    return int(rng.choice([(fine - 1) % K // 2, (fine + 1) % K // 2]))


def coarse_proba(p: np.ndarray) -> np.ndarray:
    q = np.array([p[m] + 0.5 * (p[(m - 1) % K] + p[(m + 1) % K]) for m in MAIN])
    return q / q.sum()


def evidence_vector(label: int, coarse: bool) -> np.ndarray:
    e = np.zeros(K)
    if coarse:
        m = MAIN[label]
        e[m], e[(m - 1) % K], e[(m + 1) % K] = 1.0, 0.5, 0.5
    else:
        e[label] = 1.0
    return e


def _threshold(scores: np.ndarray, alpha: float) -> float:
    n = len(scores)
    level = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(scores, level, method="higher"))


def run(seed: int, mode: str, switch_day: int = 7, budget: float = 1.0, days: int = 28, n_people: int = 60,
        cfg: S.SituationConfig | None = None, agree_window: int = 6, agree_level: float = 0.8) -> dict:
    """mode: 'fine', 'coarse', 'switch' (fixed day), 'adaptive' (switch when most coarse readings of the last
    3 days are confident) or 'per_reading' (fine questions, level of detail chosen per reading)."""
    S.configure_states(K)
    cfg = cfg or replace(S.SituationConfig(), circumplex=True, radius=0.5)
    protos = S._world(cfg, world_seed=1000 + seed)
    rng = np.random.default_rng(seed)
    model = S.population_model(cfg, protos, n_people=150, rng=rng)
    # calibration at both levels of detail
    Xc, yc = [], []
    for _ in range(60):
        p = S.make_person(cfg, protos, rng)
        _, X, y = S.occurrences(cfg, p, 10, rng)
        Xc.append(X)
        yc.append(y)
    Pc = model.predict_proba(np.vstack(Xc))
    Yc = np.concatenate(yc)
    thr_f = np.array([_threshold(1 - Pc[Yc == k, k], cfg.alpha) for k in range(K)])
    Qc = np.array([coarse_proba(p) for p in Pc])
    Yq = np.array([coarse_of(int(y), rng) for y in Yc])
    thr_c = np.array([_threshold(1 - Qc[Yq == q, q], cfg.alpha) for q in range(4)])
    h = float(cfg.noise_sd * np.sqrt(2 * cfg.n_features))
    llr = float(np.log(0.95 / (0.05 / (K - 1))))

    shown = np.zeros(days)
    fine_acc = np.zeros(days)
    count = np.zeros(days)
    questions = np.zeros(days)
    switch_days = []
    fine_shown = np.zeros(days)
    for i in range(n_people):
        prng = np.random.default_rng([seed, i, 11])
        person = S.make_person(cfg, protos, rng)
        s_all, X_all, y_all = S.occurrences(cfg, person, days * cfg.moments_per_day, rng)
        keys, evid = [], []
        fine_mode = mode in ("fine", "per_reading")
        recent: list[bool] = []
        confident_by_day: list[float] = []
        switched_at = 0 if fine_mode else None
        for day in range(days):
            if mode == "switch" and day == switch_day:
                fine_mode, switched_at = True, day
            if mode == "adaptive" and not fine_mode and len(confident_by_day) >= 3 and np.mean(confident_by_day[-3:]) >= agree_level:
                fine_mode, switched_at = True, day
            conf_today = []
            allowance = (int(np.floor((day + 1) * budget)) - int(np.floor(day * budget))) if budget < 1 else int(budget)
            asked = 0
            for j in range(cfg.moments_per_day):
                t = day * cfg.moments_per_day + j
                x, y = X_all[t], int(y_all[t])
                logp = model.predict_log_proba(x[None, :])[0].copy()
                if keys:
                    d2 = ((np.asarray(keys) - x) ** 2).sum(axis=1)
                    w = np.exp(-d2 / (2 * h * h))
                    logp += llr * (w[:, None] * np.asarray(evid)).sum(axis=0)
                p = np.exp(logp - logp.max())
                p /= p.sum()
                pred_f = int(p.argmax())
                fine_acc[day] += pred_f == y
                count[day] += 1
                if mode == "per_reading":
                    sset = (1 - p) <= thr_f
                    q = coarse_proba(p)
                    cset = (1 - q) <= thr_c
                    if int(sset.sum()) == 1:
                        shown[day] += pred_f == y
                        fine_shown[day] += 1
                    else:
                        pred_c = int(q.argmax())
                        shown[day] += (pred_c == y // 2) if y % 2 == 0 else pred_c in ((y - 1) % K // 2, (y + 1) % K // 2)
                    size = int(sset.sum())
                    options = [k for k in np.argsort(-p) if sset[k]][:3] if size >= 2 else []
                elif fine_mode:
                    shown[day] += pred_f == y
                    sset = (1 - p) <= thr_f
                    order = [k for k in np.argsort(-p)]
                    size = int(sset.sum())
                    options = [k for k in order if sset[k]][:3] if size >= 2 else []
                else:
                    q = coarse_proba(p)
                    pred_c = int(q.argmax())
                    truth_c = coarse_of(y, prng) if y % 2 == 1 else y // 2
                    shown[day] += pred_c == truth_c if y % 2 == 0 else pred_c in ((y - 1) % K // 2, (y + 1) % K // 2)
                    cset = (1 - q) <= thr_c
                    size = int(cset.sum())
                    conf_today.append(size == 1)
                    options = [k for k in np.argsort(-q) if cset[k]][:3] if size >= 2 else []
                if options and asked < allowance:
                    asked += 1
                    questions[day] += 1
                    if fine_mode:
                        offered = np.zeros(K, dtype=bool)
                        offered[options] = True
                        a = S.answer(y, offered, cfg, prng)
                        keys.append(x)
                        evid.append(evidence_vector(a, coarse=False))
                    else:
                        truth_c = coarse_of(y, prng)
                        if truth_c in options and prng.random() > cfg.closed_error:
                            a = truth_c
                        elif truth_c in options:
                            a = int(prng.choice([o for o in options if o != truth_c] or [truth_c]))
                        else:
                            a = truth_c if prng.random() > cfg.open_error else int(prng.choice([(truth_c + 1) % 4, (truth_c - 1) % 4]))
                        keys.append(x)
                        evid.append(evidence_vector(a, coarse=True))
            if conf_today:
                confident_by_day.append(float(np.mean(conf_today)))
        switch_days.append(switched_at if switched_at is not None else days)
    S.configure_states(4)
    return {"shown": (shown / count).tolist(), "fine": (fine_acc / count).tolist(),
            "questions": (np.cumsum(questions) / n_people).tolist(), "switch_day_mean": float(np.mean(switch_days)),
            "switch_day_share_switched": float(np.mean([d < days for d in switch_days])),
            "fine_shown_share": (fine_shown / count).tolist()}
