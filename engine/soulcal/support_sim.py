"""Synthetic check of when to pulse (python -m soulcal support).

The readings, states and engine decisions are the demo's synthetic people. The effect of a pulse is an
ASSUMPTION, written here so it can be changed: when a person is tense, the pattern that suits them adds about
1.0 to their recovery over the next minutes (HRV up, heart rate down, in units of 10), the other pattern about
0.2; when they are not tense a pulse adds nothing. Each false pulse (the person was not tense) makes the person
turn pulses off with probability 5%. These numbers are not measurements: the point is to compare when to
pulse, and to check that the effect and the right pattern can be learned from the person's own body.
"""

from __future__ import annotations

import numpy as np

from .engine import SPEAK, EngineConfig
from .run import run_stream
from .schema import Decision, Profile
from .support import NONE, OFFER, PATTERNS, PULSE, SupportConfig, SupportPolicy
from .synthetic import Person, generate

POLICIES = {
    "body": "Body alone: heart rate above the person's usual, not moving",
    "generic": "Generic reading says tense (today's reading, no questions)",
    "fixed": "SOUL-Calibrate decision, one fixed pattern (breathing)",
    "learned": "SOUL-Calibrate decision, pattern learned per person",
}


def _person(rng: np.random.Generator, i: int) -> tuple[Person, dict]:
    p = Person(user_id=f"p{i}", face_bias=tuple(np.array(Person().face_bias) + rng.normal(0, 0.2, 4)),
               voice_bias=tuple(np.array(Person().voice_bias) + rng.normal(0, 0.2, 4)),
               mask_prob=float(np.clip(rng.normal(0.4, 0.15), 0, 1)),
               hr_rest=float(rng.normal(64, 8)), hrv_rest=float(rng.normal(55, 12)))
    good = PATTERNS[int(rng.integers(2))]
    effect = {pt: (float(rng.normal(1.0, 0.2)) if pt == good else float(rng.normal(0.2, 0.2))) for pt in PATTERNS}
    return p, effect


def simulate(seed: int, policy: str, people: int = 20, weeks: int = 6, turn_off_p: float = 0.05) -> dict:
    rng = np.random.default_rng(seed)
    out = {"pulses": 0, "true_pulses": 0, "false_energized": 0, "tense_eligible": 0, "tense_helped": 0,
           "offers": 0, "extra_recovery": 0.0, "turned_off": 0, "right_pattern": [], "effect_error": []}
    for i in range(people):
        p, effect = _person(rng, i)
        readings, truth, _ = generate(days=7 * weeks, seed=int(rng.integers(1e9)), person=p)
        cfg = EngineConfig(personal=False, max_questions_per_day=0) if policy == "generic" else EngineConfig()
        decisions = run_stream(readings, truth, Profile(p.user_id), cfg, seed=i).decisions
        sp = SupportPolicy(SupportConfig(), seed=seed * 1000 + i)
        if policy == "fixed":
            sp._pattern = lambda: "breathing"
        hr_seen: list[float] = []
        off = False
        for r, y, d in zip(readings, truth, decisions):
            rest = float(np.mean(hr_seen)) if len(hr_seen) >= 5 else None
            if policy == "body":
                sd = float(np.std(hr_seen)) if len(hr_seen) >= 5 else None
                hot = rest is not None and r.heart_rate is not None and r.heart_rate > rest + sd
                dec = Decision(action=SPEAK if hot else "quiet", state="tense" if hot else None, options=[], proba={})
            else:
                dec = Decision(action=d["action"], state=d["state"], options=d["options"].split("|") if d["options"] else [],
                               proba={})
            if r.heart_rate is not None:
                hr_seen.append(r.heart_rate)
            eligible = r.heart_rate is not None and (r.motion is None or r.motion <= sp.cfg.motion_max)
            if y == "tense" and eligible:
                out["tense_eligible"] += 1
            if off:
                continue
            s = sp.decide(dec, r, resting_hr=rest)
            tense = y == "tense"
            natural = float(rng.normal(0.5 if tense else 0.0, 0.6))
            if s.action == OFFER:
                out["offers"] += 1
                if tense and rng.random() < 0.7:          # the person accepts the calm minute
                    out["tense_helped"] += 1
                    out["extra_recovery"] += max(effect.values()) * 0.8
            if s.action == PULSE:
                out["pulses"] += 1
                gain = effect[s.pattern] if tense else 0.0
                out["true_pulses"] += tense
                out["false_energized"] += y == "energized"
                if tense:
                    out["tense_helped"] += 1
                    out["extra_recovery"] += gain
                elif rng.random() < turn_off_p:
                    off = True
                    out["turned_off"] += 1
                sp.record_outcome(s.support_id, 0.0, 10 * (natural + gain))
            elif s.held_out:
                sp.record_outcome(s.support_id, 0.0, 10 * natural)
        if policy == "learned":
            rep = sp.effect_report()
            best = max(PATTERNS, key=lambda pt: rep[pt]["recovery"] if rep[pt]["n"] else -9)
            out["right_pattern"].append(best == max(effect, key=effect.get))
            pt = max(effect, key=effect.get)
            if rep[pt]["n"] >= 3 and rep["held_out"]["n"] >= 3:
                out["effect_error"].append(rep[pt]["effect"] - effect[pt])
    return out


def support_check(seeds: int = 5, people: int = 20, weeks: int = 6) -> dict:
    res = {}
    for pol in POLICIES:
        runs = [simulate(s, pol, people, weeks) for s in range(seeds)]
        tot = {k: sum(r[k] for r in runs) for k in ("pulses", "true_pulses", "false_energized", "tense_eligible",
                                                      "tense_helped", "offers", "extra_recovery", "turned_off")}
        n_people_weeks = seeds * people * weeks
        res[pol] = {
            "label": POLICIES[pol],
            "pulses_per_week": tot["pulses"] / n_people_weeks,
            "precision": tot["true_pulses"] / max(tot["pulses"], 1),
            "false_on_excitement": tot["false_energized"] / max(tot["pulses"], 1),
            "tense_moments_helped": tot["tense_helped"] / max(tot["tense_eligible"], 1),
            "extra_recovery_per_tense_moment": tot["extra_recovery"] / max(tot["tense_eligible"], 1),
            "turned_pulses_off": tot["turned_off"] / (seeds * people),
            "right_pattern": float(np.mean(sum((r["right_pattern"] for r in runs), []))) if pol == "learned" else None,
            "effect_error": float(np.mean(np.abs(sum((r["effect_error"] for r in runs), [])))) if pol == "learned" else None,
        }
    return res
