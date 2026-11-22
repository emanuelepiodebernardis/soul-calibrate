"""How many questions a day? Budget, timing and spreading in the recurring-situations world.

    python run_budget.py --seeds 5 --out results

Synthetic people only. Every setting sees the same people and the same moments; only the questions differ.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from soul_calibrate.situations import SituationConfig, exp_situations

KEYS = ("test_accuracy", "questions_per_person", "test_speak_share", "test_speak_accuracy", "test_coverage",
        "same_situation_after")


def mean_runs(cfg: SituationConfig, seeds: list[int]) -> dict:
    runs = [exp_situations(s, cfg, qtypes=("closed",)) for s in seeds]
    return {name: {k: float(np.nanmean([r[name][k] for r in runs])) for k in KEYS} for name in runs[0]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    seeds = list(range(a.seeds))
    base = SituationConfig()
    out: dict = {}

    out["budget"] = {str(q): mean_runs(replace(base, questions_per_day=q), seeds) for q in (0.25, 0.5, 1, 2, 3, 4)}
    out["spread"] = {f"{q}/{sp}": mean_runs(replace(base, questions_per_day=q, spread=sp), seeds)
                     for q in (1, 2) for sp in (False, True)}
    out["fast_changes"] = {f"{q}/{sp}": mean_runs(replace(base, moments_per_day=8, questions_per_day=q, spread=sp), seeds)
                           for q in (1, 2) for sp in (False, True)}
    out["longer_calibration"] = {f"{d}d/{q}": mean_runs(replace(base, calib_days=d, questions_per_day=q), seeds)
                                 for d, q in ((7, 1), (14, 0.5), (28, 0.25), (14, 1))}
    Path(a.out, "budget.json").write_text(json.dumps(out, indent=1))

    def row(label, r, name):
        v = r[name]
        return (f"| {label} | {v['questions_per_person']:.1f} | {v['test_accuracy']:.3f} | {v['same_situation_after']:.3f} | "
                f"{v['test_speak_share']:.0%} | {v['test_speak_accuracy']:.3f} | {v['test_coverage']:.3f} |")

    head = ("| Setting | Questions per person | Accuracy, test days | Same situation after an answer | Speaks | "
            "Accuracy when speaking | Coverage |\n| --- | --- | --- | --- | --- | --- | --- |")
    L = ["# How many questions a day?", "",
         f"Synthetic people, {len(seeds)} seeds, 60 people each; 6 recurring situations; 4 readings a day unless stated; "
         "closed questions; a calibration period with questions, then 5 test days without questions.", "",
         "## A. Budget per day during a 7-day calibration week", "", head]
    for q, r in out["budget"].items():
        L.append(row(f"{q}/day, no questions", r, "never") if q == "0.25" else "")
        for name, lab in (("random/closed", "random moments"), ("ambiguous/closed", "ambiguous moments"),
                          ("ambiguous_new/closed", "ambiguous and not yet known")):
            L.append(row(f"{q}/day, {lab}", r, name))
    L = [x for x in L if x != ""]
    L += ["", "## B. Spreading questions over the day (ambiguous moments)", "", head]
    for k, r in out["spread"].items():
        q, sp = k.split("/")
        L.append(row(f"{q}/day, {'spread' if sp == 'True' else 'first ambiguous moments'}", r, "ambiguous/closed"))
    L += ["", "## C. The state changes more often: 8 readings a day", "", head]
    for k, r in out["fast_changes"].items():
        q, sp = k.split("/")
        L.append(row(f"{q}/day, {'spread' if sp == 'True' else 'first ambiguous moments'}", r, "ambiguous/closed"))
        if sp == "False":
            L.append(row(f"{q}/day, random moments", r, "random/closed"))
    L.append(row("no questions", out["fast_changes"]["1/False"], "never"))
    L += ["", "## D. Fewer questions over a longer calibration (ambiguous moments)", "", head]
    for k, r in out["longer_calibration"].items():
        d, q = k.split("/")
        L.append(row(f"{d}, {q}/day", r, "ambiguous/closed"))
    Path(a.out, "BUDGET.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
