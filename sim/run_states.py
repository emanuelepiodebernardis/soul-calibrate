"""Four states or eight? Finer emotions on the valence x arousal circle.

    python run_states.py --seeds 5 --out results

States sit on a circle (the circumplex): four quadrants (calm, energized, tense, low) or eight, with an
intermediate state between each pair (for example content between calm and energized, tired between calm
and low). The signal strength is the same in both worlds, so eight states are closer to each other and
harder to tell apart. Synthetic people only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from soul_calibrate import situations as S

RADIUS = 0.5
KEYS = ("test_accuracy", "test_within_one", "questions_per_person", "test_speak_share", "test_speak_accuracy", "test_coverage")


def week(k: int, seeds, **kw) -> dict:
    S.configure_states(k)
    cfg = replace(S.SituationConfig(), circumplex=True, radius=RADIUS, **kw)
    runs = [S.exp_situations(s, cfg, qtypes=("closed",)) for s in seeds]
    S.configure_states(4)
    return {n: {key: float(np.nanmean([r[n][key] for r in runs])) for key in KEYS} for n in ("never", "random/closed", "ambiguous/closed")}


def speed(k: int, budget: float, seeds, days: int = 28, **kw) -> dict:
    S.configure_states(k)
    cfg = replace(S.SituationConfig(), circumplex=True, radius=RADIUS, calib_days=days, test_days=0,
                  questions_per_day=budget, **kw)
    acc, near, q = [], [], []
    for sd in seeds:
        cap = {}
        orig = S.summarise
        S.summarise = lambda logs, c: (cap.update(logs), orig(logs, c))[1]
        try:
            S.exp_situations(sd, cfg, qtypes=("closed",))
        finally:
            S.summarise = orig
        e = cap[("closed", "ambiguous")]
        n_people = len({x["person"] for x in e})
        acc.append([np.mean([x["correct"] for x in e if x["day"] == d]) for d in range(days)])
        near.append([np.mean([x["near"] for x in e if x["day"] == d]) for d in range(days)])
        q.append(np.cumsum([sum(1 for x in e if x["day"] == d and x.get("asked")) / n_people for d in range(days)]))
    S.configure_states(4)
    a, n_ = np.mean(acc, 0), np.mean(near, 0)
    sm = np.convolve(a, np.ones(3) / 3, mode="same")
    sm[0], sm[-1] = a[0], a[-1]
    reach = {}
    for t in (0.70, 0.80, 0.90):
        hit = np.flatnonzero(sm >= t)
        reach[str(t)] = int(hit[0]) + 1 if len(hit) else None
    return {"accuracy": a.tolist(), "within_one": n_.tolist(), "questions": np.mean(q, 0).tolist(), "days_to": reach}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    seeds = list(range(a.seeds))
    res = {
        "week": {
            "4 states": week(4, seeds),
            "8 states, ask only when 2-3 are plausible": week(8, seeds),
            "8 states, also ask when more are plausible (3 most likely offered)": week(8, seeds, ask_wide=True),
            "8 states, same, up to 2 a day": week(8, seeds, ask_wide=True, questions_per_day=2),
            "8 states, same, up to 2 a day, less sure answers (10% / 25% errors)": week(
                8, seeds, ask_wide=True, questions_per_day=2, closed_error=0.10, open_error=0.25),
        },
        "speed": {f"{k} states, {b}/day": speed(k, b, seeds, ask_wide=True) for k in (4, 8) for b in (1, 2, 4)},
    }
    Path(a.out, "states.json").write_text(json.dumps(res, indent=1))

    L = ["# Four states or eight?", "",
         f"Synthetic people, {len(seeds)} seeds, 60 people each; states on the valence x arousal circle with the same "
         "signal strength; 6 recurring situations, 4 readings a day; closed questions. Chance: 0.25 with 4 states, "
         "0.125 with 8. 'Within one' = the reading is the true state or the state next to it on the circle "
         "(for example content instead of calm).", "",
         "## A. One calibration week, then 5 test days without questions", "",
         "| World and policy | Questions per person | Accuracy, test days | Within one | Speaks | Accuracy when speaking | Coverage |",
         "| --- | --- | --- | --- | --- | --- | --- |"]
    for name, r in res["week"].items():
        for pol, lab in (("never", "no questions"), ("random/closed", "random moments"), ("ambiguous/closed", "ambiguous moments")):
            if pol == "never" and not name.startswith(("4 states", "8 states, ask only")):
                continue
            v = r[pol]
            L.append(f"| {name}: {lab} | {v['questions_per_person']:.1f} | {v['test_accuracy']:.3f} | {v['test_within_one']:.3f} | "
                     f"{v['test_speak_share']:.0%} | {v['test_speak_accuracy']:.3f} | {v['test_coverage']:.3f} |")
    L += ["", "## B. Personalization speed (questions allowed for 28 days, ambiguous moments, wide questions allowed)", "",
          "| World, budget | Day 7 | Day 14 | Day 28 | Within one, day 28 | Days to 0.70 | Days to 0.80 | Days to 0.90 | Questions by day 28 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, r in res["speed"].items():
        acc, d = r["accuracy"], r["days_to"]
        def f(x):
            return "not reached" if x is None else str(x)
        L.append(f"| {name} | {acc[6]:.2f} | {acc[13]:.2f} | {acc[27]:.2f} | {r['within_one'][27]:.2f} | {f(d['0.7'])} | "
                 f"{f(d['0.8'])} | {f(d['0.9'])} | {r['questions'][27]:.1f} |")
    Path(a.out, "STATES.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
