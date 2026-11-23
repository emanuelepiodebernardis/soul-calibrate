"""Voice, words, face and body: which matters, and what happens when the person is not talking (docs/27).

    python -m soulcal channels --out examples/demo_out

Synthetic people of the engine demo; up to 1 question a day; 6 weeks; scored on weeks 5-6, before learning.

A. Sources, one set at a time, each present at every moment.
B. How often the person uses the app (talks or types). In the other moments only the bracelet is there, which is
   the realistic case for a bracelet worn all day and an app opened a few times a day. Accuracy is split between
   moments with the app and body-only moments, and the pulse is scored as in docs/26.
"""

from __future__ import annotations

import numpy as np

from .engine import EngineConfig
from .run import run_stream
from .schema import Decision, Profile
from .support import OFFER, PULSE, SupportConfig, SupportPolicy
from .support_sim import _person
from .synthetic import generate

SETS = {
    "Body only (bracelet)": dict(face_p=0, voice_p=0, text_p=0, bracelet_p=1),
    "Voice only": dict(face_p=0, voice_p=1, text_p=0, bracelet_p=0),
    "Words only": dict(face_p=0, voice_p=0, text_p=1, bracelet_p=0),
    "Voice + words": dict(face_p=0, voice_p=1, text_p=1, bracelet_p=0),
    "Voice + words + body": dict(face_p=0, voice_p=1, text_p=1, bracelet_p=1),
    "All four (+ face)": dict(face_p=1, voice_p=1, text_p=1, bracelet_p=1),
}
APP_USE = (1.0, 0.5, 0.25, 0.1)


def _score(decisions: list[dict], mask=None) -> dict:
    late = [(i, d) for i, d in enumerate(decisions) if d["week"] >= 4 and (mask is None or mask[i])]
    acc = np.mean([d["predicted"] == d["truth"] for _, d in late]) if late else float("nan")
    spoke = [d for _, d in late if d["action"] == "speak"]
    return {"accuracy": float(acc), "speak_share": len(spoke) / max(len(late), 1),
            "speak_accuracy": float(np.mean([d["state"] == d["truth"] for d in spoke])) if spoke else float("nan"),
            "n": len(late)}


def sources_check(seeds: int = 3, people: int = 20, weeks: int = 6) -> dict:
    out = {}
    for name, kw in SETS.items():
        rows = []
        for s in range(seeds):
            rng = np.random.default_rng(s)
            for i in range(people):
                p, _ = _person(rng, i)
                r, y, m = generate(days=7 * weeks, seed=int(rng.integers(1e9)), person=p, **kw)
                rows.append(_score(run_stream(r, y, Profile(p.user_id), EngineConfig(), seed=i).decisions))
        out[name] = {k: float(np.nanmean([r[k] for r in rows])) for k in ("accuracy", "speak_share", "speak_accuracy")}
    return out


def app_use_check(seeds: int = 3, people: int = 20, weeks: int = 6) -> dict:
    out = {}
    for a in APP_USE:
        agg = {"app": [], "body": [], "all": [], "pulses": 0, "true": 0, "excite": 0, "tense_elig": 0, "helped": 0,
               "helped_body_only": 0, "tense_body_only": 0}
        for s in range(seeds):
            rng = np.random.default_rng(s)
            for i in range(people):
                p, _ = _person(rng, i)
                r, y, m = generate(days=7 * weeks, seed=int(rng.integers(1e9)), person=p, app_p=a)
                dec = run_stream(r, y, Profile(p.user_id), EngineConfig(), seed=i).decisions
                in_app = [x.voice is not None or x.text is not None or x.face is not None for x in r]
                agg["app"].append(_score(dec, in_app)["accuracy"])
                agg["body"].append(_score(dec, [not v and x.heart_rate is not None for v, x in zip(in_app, r)])["accuracy"])
                agg["all"].append(_score(dec)["accuracy"])
                sp = SupportPolicy(SupportConfig(hold_out=0.0), seed=s * 1000 + i)
                for x, t, d, app in zip(r, y, dec, in_app):
                    eligible = x.heart_rate is not None and (x.motion is None or x.motion <= sp.cfg.motion_max)
                    if t == "tense" and eligible:
                        agg["tense_elig"] += 1
                        agg["tense_body_only"] += not app
                    dd = Decision(action=d["action"], state=d["state"],
                                  options=d["options"].split("|") if d["options"] else [], proba={})
                    su = sp.decide(dd, x, resting_hr=None)
                    if su.action == PULSE:
                        agg["pulses"] += 1
                        agg["true"] += t == "tense"
                        agg["excite"] += t == "energized"
                    if su.action in (PULSE, OFFER) and t == "tense":
                        agg["helped"] += 1
                        agg["helped_body_only"] += not app
        out[str(a)] = {
            "accuracy_all": float(np.nanmean(agg["all"])), "accuracy_app": float(np.nanmean(agg["app"])),
            "accuracy_body_only": float(np.nanmean(agg["body"])) if a < 1 else float("nan"),
            "pulse_precision": agg["true"] / max(agg["pulses"], 1), "pulse_on_excitement": agg["excite"] / max(agg["pulses"], 1),
            "tense_reached": agg["helped"] / max(agg["tense_elig"], 1),
            "tense_reached_body_only": agg["helped_body_only"] / max(agg["tense_body_only"], 1) if a < 1 else float("nan"),
        }
    return out


def _mask(readings, rng, app_p):
    """Same moments, with the app used only in a share of them (the body keeps being read)."""
    from dataclasses import replace
    masked, in_app = [], []
    for r in readings:
        use = rng.random() < app_p
        in_app.append(use)
        masked.append(r if use else replace(r, face=None, voice=None, text=None))
    return masked, in_app


def checkin_check(seeds: int = 3, people: int = 20, weeks: int = 6, app_p: float = 0.25,
                  respond_p: float = 0.5, per_day: int = 1) -> dict:
    """C. The body triggers, the voice decides: at a body-only moment where the body is aroused and tension is
    possible, the app invites a 5-second voice note ("How are you right now?"). If the person answers, the
    reading has voice and words again. Compared with the same people and moments without the invitation."""
    from .engine import ASK, SPEAK, SoulEngine
    from .schema import STATES
    res = {}
    for mode in ("no invitation", "voice check-in"):
        acc_body, tense_elig, helped, pulses, true, excite, invites = [], 0, 0, 0, 0, 0, 0
        for s in range(seeds):
            rng = np.random.default_rng(s)
            for i in range(people):
                p, _ = _person(rng, i)
                full, y, _ = generate(days=7 * weeks, seed=int(rng.integers(1e9)), person=p)
                r, in_app = _mask(full, np.random.default_rng(1000 + s * 100 + i), app_p)
                eng = SoulEngine(Profile(p.user_id), EngineConfig())
                sp = SupportPolicy(SupportConfig(hold_out=0.0), seed=s * 1000 + i)
                lr = np.random.default_rng(i)
                hr_seen: list[float] = []
                day_inv: dict = {}
                start = r[0].timestamp
                for k, (x, xf, t, app) in enumerate(zip(r, full, y, in_app)):
                    d = eng.observe(x)
                    used = x
                    rest = float(np.mean(hr_seen)) if len(hr_seen) >= 5 else None
                    aroused = rest is not None and x.heart_rate is not None and x.heart_rate > rest
                    still = x.heart_rate is not None and (x.motion is None or x.motion <= 0.8)
                    day = x.timestamp.date()
                    if (mode == "voice check-in" and not app and still and aroused and d.action != SPEAK
                            and d.proba.get("tense", 0) >= 0.2 and day_inv.get(day, 0) < per_day):
                        day_inv[day] = day_inv.get(day, 0) + 1
                        invites += 1
                        if lr.random() < respond_p:
                            d = eng.observe(xf)          # the voice note: same moment, with voice and words
                            used, app = xf, True
                    if x.heart_rate is not None:
                        hr_seen.append(x.heart_rate)
                    week = (x.timestamp - start).days // 7
                    pred = max(d.proba, key=d.proba.get)
                    if week >= 4 and not in_app[k] and x.heart_rate is not None:
                        acc_body.append(pred == t)
                    if t == "tense" and still:
                        tense_elig += 1
                    su = sp.decide(d, used, resting_hr=rest)
                    if su.action == PULSE:
                        pulses += 1
                        true += t == "tense"
                        excite += t == "energized"
                    if su.action in (PULSE, OFFER) and t == "tense":
                        helped += 1
                    if d.action == ASK and lr.random() > 0.05:     # answers, as in run_stream
                        eng.answer(d.reading_index, t if t in d.options else t)
                    elif d.action == SPEAK and d.state != t and lr.random() < 0.3:
                        eng.correct(d.reading_index, t)
        n_pw = seeds * people * weeks
        res[mode] = {"accuracy_body_only_moments": float(np.mean(acc_body)), "tense_reached": helped / max(tense_elig, 1),
                     "pulse_precision": true / max(pulses, 1), "pulse_on_excitement": excite / max(pulses, 1),
                     "invitations_per_week": invites / n_pw}
    return res
