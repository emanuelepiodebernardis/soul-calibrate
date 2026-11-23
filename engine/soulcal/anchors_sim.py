"""Synthetic check of personal voice-and-body signatures (python -m soulcal anchors; docs/29).

Each synthetic person has 6 prosodic features (pitch, pitch range, energy, speech rate, jitter, pause share) and
3 body signals (heart rate, HRV, skin temperature). A reading is:

    who the person is (large) + today's microphone, room and day (voice) or day (body)
    + how THIS person shows the state (population direction + a personal twist)
    + what is being said (free voice notes only) + noise

Read sentences carry less emotion than free speech (factor 0.6, after Koch et al.). The person's states follow a
day's mix. Enrollment: 7 days, 3 neutral readings of the fixed sentence a day. Tagged readings: in days 8-21, when
the person is in a clear state, they read the sentence and say how they feel, up to k times per state. Scored on
free voice notes in days 22-42. All of this is a model of the problem, not a measurement.
"""

from __future__ import annotations

import numpy as np

from .anchors import SignatureModel
from .schema import STATES

VOICE = ["pitch", "pitch range", "energy", "speech rate", "jitter", "pause share"]
BODY = ["heart rate", "HRV", "skin temperature"]
NAMES = VOICE + BODY
#                     pitch range energy rate jitter pause |  HR   HRV  temp
POP = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],          # calm
                [1.0, 1.0, 1.0, 0.8, 0.0, -0.5, 1.0, -0.5, 0.0],        # energized
                [1.0, 0.2, 0.8, 0.8, 1.0, -0.2, 1.0, -1.0, -0.6],       # tense
                [-0.8, -0.8, -0.8, -0.8, 0.2, 0.9, -0.5, 0.2, 0.0]])    # low
P_STATE = [0.4, 0.2, 0.25, 0.15]


def _person(rng):
    return {"base": rng.normal(0, 3.0, 9), "twist": POP + rng.normal(0, 0.6, POP.shape) * (POP != 0) + rng.normal(0, 0.3, POP.shape),
            "gain": float(rng.uniform(0.6, 1.4))}


def _reading(rng, p, k, session, read: bool) -> np.ndarray:
    eff = p["twist"][k] * p["gain"] * 1.5
    eff = np.concatenate([eff[:6] * (0.6 if read else 1.0), eff[6:]])
    content = np.concatenate([rng.normal(0, 0 if read else 1.0, 6), np.zeros(3)])
    return p["base"] + session + eff + content + rng.normal(0, 0.5, 9)


def simulate(seed: int, people: int = 40, ks=(0, 1, 2, 4), days: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    pop = POP * 1.5 / 1.0
    res: dict = {}
    for i in range(people):
        p = _person(rng)
        sessions = [np.concatenate([rng.normal(0, 1.0, 6), rng.normal(0, 0.5, 3)]) for _ in range(days)]
        day_states = [int(rng.choice(4, p=P_STATE)) for _ in range(days)]
        # data
        enroll = [_reading(rng, p, 0, sessions[d], True) for d in range(7) for _ in range(3)]
        anchors = [_reading(rng, p, day_states[d], sessions[d], True) for d in range(days)]
        tagged = {s: [(d, _reading(rng, p, day_states[d], sessions[d], True)) for d in range(7, 21) if day_states[d] == s]
                  for s in range(4)}
        tests = [(d, day_states[d], _reading(rng, p, day_states[d], sessions[d], False)) for d in range(21, days)
                 for _ in range(2)]
        # the anchor of the day is read in a neutral tone, whatever the mood: its emotional part is damped
        neutral_anchor = [_reading(rng, p, 0, sessions[d], True) for d in range(days)]

        def score(model, use_anchor, personal, cols=slice(None)):
            ok = []
            for d, y, x in tests:
                if use_anchor:
                    model.set_anchor(neutral_anchor[d][cols])
                pr = model.proba(x[cols], use_anchor=use_anchor, personal=personal)
                ok.append(max(pr, key=pr.get) == STATES[y])
            return float(np.mean(ok))

        def build(k, cols=slice(None), use_anchor=True):
            m = SignatureModel(n_features=len(NAMES[cols]), population=pop[:, cols])
            for x in enroll:
                m.add_enrollment(x[cols])
            for s in range(4):
                for d, x in tagged[s][:k]:
                    if use_anchor:
                        m.set_anchor(neutral_anchor[d][cols])
                    m.add_tagged(STATES[s], x[cols], use_anchor=use_anchor)
            return m

        # generic: population directions on features standardised over everyone (no personal reference)
        glob = SignatureModel(n_features=9, population=pop)
        rows = {
            "Generic (no personal reference)": score(glob, False, False),
            "+ voice-and-body baseline (enrollment)": score(build(0, use_anchor=False), False, True),
            "+ daily 5-second anchor": score(build(0), True, True),
        }
        for k in ks[1:]:
            rows[f"+ {k} tagged readings per state"] = score(build(k), True, True)
        rows["Voice only, + 2 tagged readings"] = score(build(2, slice(0, 6)), True, True, slice(0, 6))
        rows["Body only, + 2 tagged readings"] = score(build(2, slice(6, 9)), True, True, slice(6, 9))
        for k, v in rows.items():
            res.setdefault(k, []).append(v)
    return {k: float(np.mean(v)) for k, v in res.items()}


def anchors_check(seeds: int = 5) -> dict:
    runs = [simulate(s) for s in range(seeds)]
    return {k: float(np.mean([r[k] for r in runs])) for k in runs[0]}


MODES = {
    # name: (enrollment readings per day in week 1, evening anchors per week, tagged sentences per week)
    "Light": (1, 7, 1),
    "Standard": (1, 7, 3),
    "Fast": (2, 7, 7),
    "Anchor less than daily (3 a week, 2 tagged)": (1, 3, 2),
}


def modes_check(seeds: int = 5, people: int = 40, days: int = 42) -> dict:
    """How fast each voluntary mode learns the person. Week 1: enrollment (neutral sentence). From day 8 the
    person reads the sentence when they choose and says how they feel (the state they are in that day), up to the
    mode's number per week, and the evening anchor on the mode's days (the latest anchor is reused otherwise).
    Scored every day on free voice notes, with what was collected before that day."""
    out: dict = {}
    for name, (enroll_pd, anchors_pw, tagged_pw) in MODES.items():
        acc = np.zeros(days)
        cnt = np.zeros(days)
        reach2, tagged_total = [], []
        for s in range(seeds):
            rng = np.random.default_rng(s)
            for i in range(people):
                p = _person(rng)
                sessions = [np.concatenate([rng.normal(0, 1.0, 6), rng.normal(0, 0.5, 3)]) for _ in range(days)]
                st = [int(rng.choice(4, p=P_STATE)) for _ in range(days)]
                m = SignatureModel(n_features=9, population=POP * 1.5)
                last_anchor = None
                tag_days = set()
                for w in range(1, days // 7):
                    week = list(range(7 * w, 7 * w + 7))
                    tag_days |= set(rng.choice(week, size=min(tagged_pw, 7), replace=False).tolist())
                anchor_days = {d for w in range(days // 7) for d in
                               rng.choice(range(7 * w, 7 * w + 7), size=anchors_pw, replace=False).tolist()}
                n_tag = 0
                seen = [0, 0, 0, 0]
                got2 = None
                for d in range(days):
                    if d < 7:
                        for _ in range(enroll_pd):
                            m.add_enrollment(_reading(rng, p, 0, sessions[d], True))
                    if d in anchor_days:
                        last_anchor = _reading(rng, p, 0, sessions[d], True)
                        m.set_anchor(last_anchor)
                    if d >= 7:
                        for _ in range(2):
                            x = _reading(rng, p, st[d], sessions[d], False)
                            pr = m.proba(x, use_anchor=last_anchor is not None)
                            acc[d] += max(pr, key=pr.get) == STATES[st[d]]
                            cnt[d] += 1
                    if d in tag_days:
                        m.add_tagged(STATES[st[d]], _reading(rng, p, st[d], sessions[d], True),
                                     use_anchor=last_anchor is not None)
                        n_tag += 1
                        seen[st[d]] += 1
                        if got2 is None and min(seen) >= 2:
                            got2 = d
                reach2.append(got2 if got2 is not None else days)
                tagged_total.append(n_tag)
        daily = np.divide(acc, np.maximum(cnt, 1))
        weekly = [float(daily[7 * w:7 * w + 7].mean()) for w in range(1, days // 7)]
        out[name] = {"weekly": weekly, "days_to_two_per_state": float(np.median(reach2)),
                     "tagged_by_day_42": float(np.mean(tagged_total)),
                     "enroll_pd": enroll_pd, "anchors_pw": anchors_pw, "tagged_pw": tagged_pw}
    return out


# --------------------------------------------------------------------------- the signature inside the engine
def _to_reading(uid, ts, x, generic_voice: dict, with_features: bool):
    from .schema import Reading
    # body features in the simulation are z-like units: map them to plausible bracelet values
    return Reading(user_id=uid, timestamp=ts, voice=generic_voice,
                   heart_rate=72 + 6 * x[6], hrv_rmssd=max(5.0, 42 + 8 * x[7]), skin_temp=33.5 + 0.4 * x[8], motion=0.2,
                   voice_features=list(x) if with_features else None)


ENGINE_CONDITIONS = {
    # name: (config overrides, tagged sentences a week in days 8-21)
    "Public approach today: generic speech model + population body norms, nothing personal": ({"signature": False, "personal": False, "head_lr": 0.0}, 0),
    "Our engine without the signature: generic speech model + body, personal baseline, answers": ({"signature": False}, 0),
    "+ signature, enrollment and evening anchor only": ({"signature_learns_from_answers": False}, 0),
    "+ 3 tagged sentences a week (standard mode)": ({"signature_learns_from_answers": False}, 3),
    "+ answered voice notes also teach the signature (default)": ({}, 3),
    "Same, signature added to the generic voice reading instead of replacing it": ({"signature_replaces_voice": False}, 3),
    "Same, signature not softened (temperature 1)": ({"signature_temperature": 1.0}, 3),
}


def engine_check(seeds: int = 4, people: int = 25, days: int = 42) -> dict:
    """The full SoulEngine on free voice notes, with and without the person's signature in its voice channel.
    Week 1: enrollment (3 neutral sentences a day); every evening the 5-second anchor; two free voice notes a day,
    each read by a generic speech model (voice channel) and the bracelet (body); the engine speaks, asks (one
    question a day, answered truthfully) or stays quiet. Scored on days 22-42: accuracy of the most likely state,
    and of what the engine actually says."""
    from datetime import datetime, timedelta

    from .engine import EngineConfig, SoulEngine
    from .schema import Profile
    generic = SignatureModel(n_features=6, population=POP[:, :6] * 1.5)
    out: dict = {}
    for name, (over, tagged_pw) in ENGINE_CONDITIONS.items():
        acc, spoken_ok, spoken = [], 0, 0
        for s in range(seeds):
            rng = np.random.default_rng(200 + s)          # seeds 100-101 were used to choose the defaults
            for i in range(people):
                p = _person(rng)
                sessions = [np.concatenate([rng.normal(0, 1.0, 6), rng.normal(0, 0.5, 3)]) for _ in range(days)]
                st = [int(rng.choice(4, p=P_STATE)) for _ in range(days)]
                notes = [[st[d], st[d]] for d in range(days)]
                eng = SoulEngine(Profile(f"p{i}"), EngineConfig(**over))
                t0 = datetime(2026, 1, 5, 9)
                tagged_left = 0
                for d in range(days):
                    if d < 7:
                        for _ in range(3):
                            eng.enroll(_reading(rng, p, 0, sessions[d], True))
                    eng.anchor(_reading(rng, p, 0, sessions[d], True))
                    if d % 7 == 0:
                        tagged_left = tagged_pw if 7 <= d < 21 else 0
                    if tagged_left and rng.random() < tagged_pw / 7 + 0.15:
                        eng.tag(STATES[st[d]], _reading(rng, p, st[d], sessions[d], True))
                        tagged_left -= 1
                    for j, k in enumerate(notes[d]):
                        x = _reading(rng, p, k, sessions[d], False)
                        gv = generic.proba(x[:6], personal=False)
                        r = _to_reading(f"p{i}", t0 + timedelta(days=d, hours=10 * j), x, gv, True)
                        dec = eng.observe(r)
                        if d >= 21:
                            acc.append(max(dec.proba, key=dec.proba.get) == STATES[k])
                            if dec.action == "speak":
                                spoken += 1
                                spoken_ok += dec.state == STATES[k]
                        if dec.action == "ask" and STATES[k] in dec.options:
                            eng.answer(dec.reading_index, STATES[k])
                        elif dec.action == "ask":
                            eng.correct(dec.reading_index, STATES[k])
        out[name] = {"accuracy": float(np.mean(acc)), "spoken_share": spoken / max(len(acc), 1),
                     "spoken_correct": spoken_ok / max(spoken, 1)}
    return out
