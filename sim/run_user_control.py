"""The user in control: chosen question budget and times, free notes, and a memory robust to wrong answers.

    python run_user_control.py --seeds 5 --out results

Synthetic people only; same people and moments in every setting; ambiguous moments, closed questions.
Readings of the day are numbered 0-3 (for example morning, afternoon, evening, night).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from soul_calibrate.situations import SituationConfig, exp_situations

KEYS = ("test_accuracy", "questions_per_person", "test_speak_share", "test_speak_accuracy", "test_coverage")


def run(cfg: SituationConfig, seeds: list[int]) -> dict:
    runs = [exp_situations(s, cfg, qtypes=("closed",)) for s in seeds]
    return {name: {k: float(np.nanmean([r[name][k] for r in runs])) for k in KEYS} for name in ("never", "ambiguous/closed")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    seeds = list(range(a.seeds))
    base = SituationConfig()
    res: dict = {}
    res["preferences"] = {
        "1 a day, any time": run(base, seeds),
        "1 a day, evenings only (readings 2-3)": run(replace(base, allowed_slots=(2, 3)), seeds),
        "2 a day, any time": run(replace(base, questions_per_day=2), seeds),
        "2 a day, evenings only": run(replace(base, questions_per_day=2, allowed_slots=(2, 3)), seeds),
        "as many as needed (up to 4 a day)": run(replace(base, questions_per_day=4), seeds),
    }
    res["notes"] = {f"{p:.0%} of readings": run(replace(base, note_p=p), seeds) for p in (0.0, 0.1, 0.25)}
    res["notes_only"] = {f"no questions, notes on {p:.0%}": run(replace(base, questions_per_day=0.0001, note_p=p), seeds)
                         for p in (0.1, 0.25)}
    res["robust"] = {}
    for err in (0.05, 0.2, 0.35):
        for trust in (False, True):
            cfg = replace(base, questions_per_day=2, closed_error=err, open_error=max(err, 0.15), trust_memory=trust)
            res["robust"][f"{err}/{trust}"] = run(cfg, seeds)
    Path(a.out, "user_control.json").write_text(json.dumps(res, indent=1))

    head = ("| Setting | Questions per person (week) | Accuracy, test days | Speaks | Accuracy when speaking | Coverage |\n"
            "| --- | --- | --- | --- | --- | --- |")

    def row(label, v):
        return (f"| {label} | {v['questions_per_person']:.1f} | {v['test_accuracy']:.3f} | {v['test_speak_share']:.0%} | "
                f"{v['test_speak_accuracy']:.3f} | {v['test_coverage']:.3f} |")

    L = ["# The user in control", "",
         f"Synthetic people, {len(seeds)} seeds, 60 people each; 6 recurring situations; 4 readings a day; a 7-day "
         "calibration week, then 5 test days without questions; questions at ambiguous moments, closed options.", "",
         "## A. The user chooses how many questions and when", "", head,
         row("No questions", res["preferences"]["1 a day, any time"]["never"])]
    for k, r in res["preferences"].items():
        L.append(row(k, r["ambiguous/closed"]))
    L += ["", "## B. Free notes (\"I trained this morning\", \"I got angry about...\"), read on the phone into a state", "", head]
    for k, r in res["notes"].items():
        L.append(row(f"1 question a day + notes on {k}", r["ambiguous/closed"]))
    for k, r in res["notes_only"].items():
        L.append(row(k, r["ambiguous/closed"]))
    L += ["", "## C. Wrong answers: plain memory vs consensus memory (2 questions a day)", "",
          "Consensus memory: an answer that agrees with nearby answers gains weight; a lone contradiction loses "
          "weight instead of erasing what many answers agree on.", "", head]
    for k, r in res["robust"].items():
        err, trust = k.split("/")
        L.append(row(f"{float(err):.0%} wrong answers, {'consensus' if trust == 'True' else 'plain'} memory", r["ambiguous/closed"]))
    Path(a.out, "USER_CONTROL.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
