"""Recurring-situations experiment: questions and the next reading of the same situation.

    python run_situations.py --seeds 5 --out results

Synthetic people only: the numbers show how the method behaves, not how it will
perform on real users.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from soul_calibrate.situations import SituationConfig, exp_situations  # noqa: E402

INK, QUIET, ACCENT, SECOND, THIRD = "#1f1e1c", "#8a8478", "#c4622d", "#2f7d8c", "#b9b2a5"
SCALARS = ("test_accuracy", "questions_per_person", "same_situation_after", "same_situation_without_questions",
           "other_situations", "other_situations_without_questions", "share_moments_after_asked")
CURVES = ("accuracy_by_day", "set_size_by_day", "speak_by_day")
LABELS = {
    "never": "No questions (today)",
    "random/closed": "Random moment, closed question",
    "ambiguous/closed": "Ambiguous moment, closed question",
    "ambiguous_new/closed": "Ambiguous and not yet known, closed",
    "random/open": "Random moment, open question",
    "ambiguous/open": "Ambiguous moment, open question",
    "ambiguous_new/open": "Ambiguous and not yet known, open",
}


def aggregate(runs: list[dict]) -> dict:
    out = {}
    for name in runs[0]:
        out[name] = {}
        for k in SCALARS:
            vals = [r[name][k] for r in runs if not np.isnan(r[name][k])]
            out[name][k] = {"mean": float(np.mean(vals)) if vals else None,
                            "sd": float(np.std(vals)) if vals else None}
        for k in CURVES:
            arr = np.array([r[name][k] for r in runs])
            out[name][k] = {"mean": arr.mean(axis=0).tolist(), "sd": arr.std(axis=0).tolist()}
    return out


def fmt(x: dict | None) -> str:
    if x is None or x["mean"] is None:
        return "–"
    return f"{x['mean']:.3f} ± {x['sd']:.3f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    seeds = list(range(args.seeds))
    base = SituationConfig()

    main_res = aggregate([exp_situations(s, base) for s in seeds])
    sweep = {}
    for stab in (1.0, 0.8, 0.6):
        cfg = replace(base, stability=stab)
        sweep[str(stab)] = aggregate([exp_situations(s, cfg, qtypes=("closed",)) for s in seeds])

    (out / "situations.json").write_text(json.dumps({"main": main_res, "stability_sweep": sweep,
                                                     "config": base.__dict__, "seeds": seeds}, indent=2))

    lines = [
        "# Recurring situations: does a question improve the next reading of the same situation?",
        "",
        f"Synthetic people, {len(seeds)} seeds, 60 people per seed, mean ± standard deviation across seeds. "
        f"Each person has {base.n_situations} recurring situations; {base.moments_per_day} readings a day; "
        f"a calibration week of {base.calib_days} days with at most one question a day, then "
        f"{base.test_days} test days without questions. Four states, chance 0.25. "
        "Policies share the same people and the same moments: only the questions differ.",
        "",
        "## A. Policies and question types (situations always bring their usual state)",
        "",
        "| Policy | Questions per person | Accuracy in the test days | Same situation, after the answer | Same moments, no questions | Other situations | Same moments, no questions |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, r in main_res.items():
        lines.append(f"| {LABELS[name]} | {r['questions_per_person']['mean']:.1f} | {fmt(r['test_accuracy'])} | "
                     f"{fmt(r['same_situation_after'])} | {fmt(r['same_situation_without_questions'])} | "
                     f"{fmt(r['other_situations'])} | {fmt(r['other_situations_without_questions'])} |")
    lines += ["", "## B. The field narrows: mean size of the set of plausible states, by day", "",
              "| Day | " + " | ".join(str(d + 1) for d in range(base.calib_days + base.test_days)) + " |",
              "| --- | " + " | ".join("---" for _ in range(base.calib_days + base.test_days)) + " |"]
    for name in ("never", "random/closed", "ambiguous/closed"):
        vals = main_res[name]["set_size_by_day"]["mean"]
        lines.append(f"| {LABELS[name]} | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
    lines += ["", "## C. How stable the situations are (closed questions)", "",
              "Stability = probability that a situation brings its usual state; otherwise it brings a neighbouring one.",
              "",
              "| Stability | No questions | Random moment | Ambiguous moment | Ambiguous and not yet known |",
              "| --- | --- | --- | --- | --- |"]
    for stab, r in sweep.items():
        lines.append(f"| {stab} | {fmt(r['never']['test_accuracy'])} | {fmt(r['random/closed']['test_accuracy'])} | "
                     f"{fmt(r['ambiguous/closed']['test_accuracy'])} | {fmt(r['ambiguous_new/closed']['test_accuracy'])} |")
    (out / "SITUATIONS.md").write_text("\n".join(lines) + "\n")

    # Figure 5: accuracy by day
    days = np.arange(1, base.calib_days + base.test_days + 1)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axes[0]
    for name, color in (("never", THIRD), ("random/closed", SECOND), ("ambiguous/closed", ACCENT)):
        m = np.array(main_res[name]["accuracy_by_day"]["mean"])
        sd = np.array(main_res[name]["accuracy_by_day"]["sd"])
        ax.plot(days, m, color=color, linewidth=2.2, label=LABELS[name])
        ax.fill_between(days, m - sd, m + sd, color=color, alpha=0.15, linewidth=0)
    ax.axvspan(base.calib_days + 0.5, days[-1] + 0.5, color="#f1eee8", zorder=0)
    ax.text(base.calib_days + 0.8, 0.96, "test days, no questions", color=QUIET, fontsize=9)
    ax.set_ylim(0.25, 1.0)
    ax.set_xlabel("Day", color=QUIET)
    ax.set_title("Accuracy by day", loc="left", fontsize=12, color=INK)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax = axes[1]
    for name, color in (("never", THIRD), ("random/closed", SECOND), ("ambiguous/closed", ACCENT)):
        ax.plot(days, main_res[name]["set_size_by_day"]["mean"], color=color, linewidth=2.2, label=LABELS[name])
    ax.axvspan(base.calib_days + 0.5, days[-1] + 0.5, color="#f1eee8", zorder=0)
    ax.set_xlabel("Day", color=QUIET)
    ax.set_title("Plausible states per reading (the field narrows)", loc="left", fontsize=12, color=INK)
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.grid(axis="y", color="#e4e1db", linewidth=0.8)
        a.tick_params(colors=QUIET)
    fig.tight_layout()
    fig.savefig(out / "fig5_recurring_situations.png", dpi=160)
    print((out / "SITUATIONS.md").read_text())


if __name__ == "__main__":
    main()
