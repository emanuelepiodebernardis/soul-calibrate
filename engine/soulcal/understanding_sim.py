"""Synthetic check of the understanding layer, with people drawn from open experience-sampling data (docs/30).

Each simulated person is one of 463 real people from five open studies (data/esm_profiles.json): their mean,
spread and inertia of negative affect, their positive affect, and their negative-emotion differentiation (how well
they tell their negative emotions apart). From these:

* their moment-to-moment negative and positive affect follow an AR(1) process with their own parameters;
* the true state is tense or low when negative affect is above 0.25 (anxious vs sad flavour, persistent), else
  energized or calm by positive affect;
* when asked, they swap tense and low with probability 0.6 x (1 - differentiation): people who tell negative
  emotions apart badly also label them badly (calm and energized are swapped 12% of the time);
* the reading is a personal nearest-centroid model on 4 signal features, learning from their answers.

"Needs the layer" = top quarter of mean negative affect or bottom quarter of differentiation in the real data.

Effects of the understanding layer are assumptions taken from published studies, in two rounds:
round 1 uses the reported effects, round 2 a conservative version (smaller effects, none for people doing well).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .understanding import NeedGate

STATES = ["calm", "energized", "tense", "low"]
NEG = {2, 3}
CENTROIDS = np.array([[0, 0, 0, 0], [1.4, 1.0, 0, 0], [1.2, -0.4, 1.4, 0], [-1.0, -0.6, 0.4, 1.2]], float)

ROUNDS = {
    "Round 1 (effects as reported)": {
        # each reflective prompt answered narrows tense/low confusion by 2% (granularity grows with labelling:
        # Hoemann et al. 2021); negative affect falls ~11% over 8 weeks with support (MindScape 2024: -11%);
        # a lens raises the answer rate from 0.70 to 0.80 (assumed)
        "granularity_gain": 0.02, "relief_need": 0.11, "relief_well": 0.05, "answer_boost": 0.10,
    },
    "Round 2 (conservative)": {
        # gains at 40%, half the relief for people in need and none for people doing well (ECoWeB 2024:
        # no wellbeing gain in healthy young people), no boost from the lens
        "granularity_gain": 0.008, "relief_need": 0.05, "relief_well": 0.0, "answer_boost": 0.0,
    },
}
CONDITIONS = ["No understanding layer", "Layer at hard moments, for everyone", "Layer by need (person-level gate)"]


def load_profiles(path: str | Path | None = None) -> list[dict]:
    p = Path(path) if path else Path(__file__).parent / "data" / "esm_profiles.json"
    d = json.load(open(p, encoding="utf-8"))
    return [x for x in d["people"] if x["neg_diff"] is not None]


def _ar(rng, n, mean, sd, phi):
    phi = float(np.clip(phi if phi == phi else 0.3, 0.0, 0.9))
    e = rng.normal(0, sd * np.sqrt(1 - phi ** 2), n)
    x = np.empty(n)
    x[0] = mean + rng.normal(0, sd)
    for t in range(1, n):
        x[t] = mean + phi * (x[t - 1] - mean) + e[t]
    return x


def _person_run(rng, prof, need, cond, eff, days=56, per_day=4):
    n = days * per_day
    m0 = prof["na_mean"]
    p_neg = 0.6 * (1 - prof["neg_diff"])
    offset = rng.normal(0, 0.7, CENTROIDS.shape)                 # the person's own way of showing each state
    pa = _ar(rng, n, prof["pa_mean"], 0.15, 0.3)
    anx = np.empty(n, bool)
    anx[0] = rng.random() < 0.55
    for t in range(1, n):
        anx[t] = anx[t - 1] if rng.random() < 0.7 else rng.random() < 0.55
    # personal reading model: centroids start at the population, learn from answers
    mu = CENTROIDS.copy()
    cnt = np.full(4, 3.0)
    gate = NeedGate()
    active = cond == "Layer at hard moments, for everyone"
    prompts, answers_rate, correct, scored = 0, 0.70, 0, 0
    na_mean = m0
    na_sd, na_phi = prof["na_sd"], prof["na_ar1"]
    asked_today = 0
    longest = 0
    x_na = m0
    for t in range(n):
        day = t // per_day
        if t % per_day == 0:
            asked_today = 0
            if day and day % 7 == 0 and cond != "No understanding layer":
                if cond == "Layer by need (person-level gate)" and day >= 14 and day % 14 == 0:
                    active = gate.decide(day) != "monitor"
                if active:                                       # weekly relief while supported
                    rate = eff["relief_need"] if need else eff["relief_well"]
                    na_mean *= (1 - rate) ** (1 / 8)
        phi = float(np.clip(na_phi if na_phi == na_phi else 0.3, 0, 0.9))
        x_na = na_mean + phi * (x_na - na_mean) + rng.normal(0, na_sd * np.sqrt(1 - phi ** 2))
        if x_na > 0.25:
            s = 2 if anx[t] else 3
        else:
            s = 1 if pa[t] > 0.55 else 0
        x = CENTROIDS[s] + offset[s] + rng.normal(0, 1.0, 4)
        d2 = ((mu - x) ** 2).sum(1)
        order = np.argsort(d2)
        read = int(order[0])
        margin = d2[order[1]] - d2[order[0]]
        confident = margin > 1.5
        gate.observe(day, STATES[read])
        if day >= 42:
            scored += 1
            correct += read == s
        ambiguous = margin < 1.5
        rate = answers_rate + (eff["answer_boost"] if active else 0.0)
        if (ambiguous or read in NEG) and asked_today < 1 and rng.random() < rate:
            asked_today += 1
            if s in NEG:
                a = (5 - s) if rng.random() < p_neg else s
            else:
                a = (1 - s) if rng.random() < 0.12 else s
            mu[a] += (x - mu[a]) / (cnt[a] + 1)
            cnt[a] += 1
            gate.answer(day, STATES[read], STATES[a], bool(margin > 0.5))
            if active and s in NEG:                               # a reflective prompt on a negative moment
                prompts += 1
                p_neg *= (1 - eff["granularity_gain"])
        if t % per_day == per_day - 1:
            gate.end_of_day(day)
            longest = max(longest, gate.scores(day)["negative_days_in_a_row"])
            if cond != "No understanding layer" and not active:
                if day % 7 == 6:
                    prompts += 1                                  # the weekly reflection everyone gets
    return {"acc": correct / max(scored, 1), "conf_start": 0.6 * (1 - prof["neg_diff"]), "conf_end": p_neg,
            "na_change": (na_mean - m0) / m0 if m0 > 0 else 0.0, "prompts_per_week": prompts / (days / 7),
            "active_end": bool(active), "bridge": longest >= gate.bridge_days}


def understanding_check(seeds: int = 3, people: int | None = None, profiles: list[dict] | None = None) -> dict:
    prof = profiles or load_profiles()
    na = np.array([p["na_mean"] for p in prof])
    dif = np.array([p["neg_diff"] for p in prof])
    need = (na >= np.percentile(na, 75)) | (dif <= np.percentile(dif, 25))
    out = {"people": len(prof), "need_share": float(need.mean()), "rounds": {}}
    for rname, eff in ROUNDS.items():
        res = {}
        for cond in CONDITIONS:
            rows = {True: [], False: []}
            for s in range(seeds):
                rng = np.random.default_rng(1000 + s)
                idx = range(len(prof)) if people is None else rng.choice(len(prof), people, replace=False)
                for i in idx:
                    r = _person_run(rng, prof[i], bool(need[i]), cond, eff)
                    rows[bool(need[i])].append(r)
            res[cond] = {}
            for g, key in ((True, "need"), (False, "well")):
                R = rows[g]
                res[cond][key] = {
                    "reading_right": float(np.mean([r["acc"] for r in R])),
                    "confusion_start": float(np.mean([r["conf_start"] for r in R])),
                    "confusion_end": float(np.mean([r["conf_end"] for r in R])),
                    "negative_affect_change": float(np.mean([r["na_change"] for r in R])),
                    "prompts_per_week": float(np.mean([r["prompts_per_week"] for r in R])),
                    "layer_on_at_week_8": float(np.mean([r["active_end"] for r in R])),
                    "bridge_offered": float(np.mean([r["bridge"] for r in R])),
                }
        out["rounds"][rname] = res
    return out


# --------------------------------------------------------------------------- a person who does not know what they feel
ANSWER_CONDITIONS = [
    "Ask for the name (today)",
    "+ ask what it is like (pleasant? energy?)",
    "+ body first (signals shown before asking)",
    "+ weigh answers by reliability",
    "+ understanding layer over 8 weeks",
]
ANSWER_ROUNDS = {
    # valence is easy even for people who cannot name feelings; energy is harder, and harder the lower their
    # differentiation; seeing their own signals first helps (interoception); the layer makes feelings finer
    "Round 1 (effects as reported)": {"valence_error": 0.04, "energy_factor": 0.5, "body_help": 0.4, "granularity_gain": 0.02},
    "Round 2 (conservative)": {"valence_error": 0.08, "energy_factor": 0.75, "body_help": 0.2, "granularity_gain": 0.008},
}


def _person_answers(rng, prof, level: int, eff, days=56, per_day=4):
    from .understanding import AnswerReliability
    n = days * per_day
    p_neg = 0.6 * (1 - prof["neg_diff"])
    offset = rng.normal(0, 0.7, CENTROIDS.shape)
    pa = _ar(rng, n, prof["pa_mean"], 0.15, 0.3)
    na_sd, phi = prof["na_sd"], float(np.clip(prof["na_ar1"] if prof["na_ar1"] == prof["na_ar1"] else 0.3, 0, 0.9))
    x_na, m = prof["na_mean"], prof["na_mean"]
    anx = rng.random() < 0.55
    mu, cnt = CENTROIDS.copy(), np.full(4, 3.0)
    rel = AnswerReliability()
    answered = right = skipped = 0
    correct = scored = 0
    asked_today = 0
    for t in range(n):
        day = t // per_day
        if t % per_day == 0:
            asked_today = 0
        x_na = m + phi * (x_na - m) + rng.normal(0, na_sd * np.sqrt(1 - phi ** 2))
        anx = anx if rng.random() < 0.7 else rng.random() < 0.55
        s = (2 if anx else 3) if x_na > 0.25 else (1 if pa[t] > 0.55 else 0)
        x = CENTROIDS[s] + offset[s] + rng.normal(0, 1.0, 4)
        d2 = ((mu - x) ** 2).sum(1)
        order = np.argsort(d2)
        read, margin = int(order[0]), d2[order[1]] - d2[order[0]]
        if day >= 42:
            scored += 1
            correct += read == s
        if not ((margin < 1.5 or read in NEG) and asked_today < 1 and rng.random() < 0.7):
            continue
        asked_today += 1
        confusion = p_neg if s in NEG else 0.12
        if level == 0:                                            # name it: swap within the same valence
            a = ((5 - s) if s in NEG else (1 - s)) if rng.random() < confusion else s
        else:                                                     # what is it like: valence, then energy
            neg = s in NEG
            if rng.random() < eff["valence_error"]:
                neg = not neg
            high = s in (1, 2)
            e_err = eff["energy_factor"] * confusion * ((1 - eff["body_help"]) if level >= 2 else 1.0)
            if rng.random() < e_err:
                if rng.random() < 0.5:                            # "not sure": nothing wrong is learned
                    skipped += 1
                    continue
                high = not high
            a = (2 if high else 3) if neg else (1 if high else 0)
        answered += 1
        right += a == s
        confident = margin > 0.5
        w = rel.weight(STATES[read], STATES[a], confident) if level >= 3 else 1.0
        rel.record(STATES[read], STATES[a], confident)
        if w > 0:
            mu[a] += w * (x - mu[a]) / (cnt[a] + 1)
            cnt[a] += w
        if level >= 4 and s in NEG:
            p_neg *= (1 - eff["granularity_gain"])
    return {"answers_right": right / max(answered, 1), "not_sure": skipped / max(answered + skipped, 1),
            "reading_right": correct / max(scored, 1), "confusion_end": p_neg}


def answers_check(seeds: int = 3, profiles: list[dict] | None = None) -> dict:
    """Do people who cannot tell their feelings apart give right answers, and does the reading learn from them?"""
    prof = profiles or load_profiles()
    dif = np.array([p["neg_diff"] for p in prof])
    hard = dif <= np.percentile(dif, 25)
    out = {"people": len(prof), "hard_share": float(hard.mean()), "rounds": {}}
    for rname, eff in ANSWER_ROUNDS.items():
        res = {}
        for lvl, cond in enumerate(ANSWER_CONDITIONS):
            rows = {True: [], False: []}
            for s in range(seeds):
                rng = np.random.default_rng(2000 + s)
                for i, p in enumerate(prof):
                    rows[bool(hard[i])].append(_person_answers(rng, p, lvl, eff))
            res[cond] = {key: {k: float(np.mean([r[k] for r in rows[g]])) for k in rows[g][0]}
                         for g, key in ((True, "hard"), (False, "others"))}
        out["rounds"][rname] = res
    return out
