"""Run every experiment over several seeds and write results, a report and figures.

    python run_simulation.py --seeds 5 --out results

Synthetic users only: the numbers show how the method behaves and how it is
evaluated, not how it will perform on real people.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from soul_calibrate.data import SimConfig  # noqa: E402
from soul_calibrate.experiments import Protocol, exp_active, exp_cohort, exp_conformal, exp_drift, exp_ladder  # noqa: E402

INK, QUIET, ACCENT, SECOND = "#1f1e1c", "#8a8478", "#c4622d", "#2f7d8c"


def summarise(runs: list[dict]) -> dict:
    keys = runs[0].keys()
    return {k: {"mean": float(np.mean([r[k] for r in runs])), "sd": float(np.std([r[k] for r in runs]))} for k in keys}


def style(ax, title: str, ylabel: str) -> None:
    ax.set_title(title, loc="left", fontsize=12, color=INK)
    ax.set_ylabel(ylabel, color=QUIET)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e4e1db", linewidth=0.8)
    ax.tick_params(colors=QUIET)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cfg, p = SimConfig(), Protocol()
    seeds = list(range(args.seeds))

    res = {
        "ladder": summarise([exp_ladder(s, cfg, p) for s in seeds]),
        "active": summarise([exp_active(s, cfg, p) for s in seeds]),
        "conformal": summarise([exp_conformal(s, cfg, p) for s in seeds]),
        "drift": summarise([exp_drift(s, cfg, p) for s in seeds]),
        "cohort": summarise([exp_cohort(s, cfg, p) for s in seeds]),
        "config": {"sim": cfg.__dict__, "protocol": p.__dict__, "seeds": seeds},
    }
    (out / "results.json").write_text(json.dumps(res, indent=2))

    # Figure 1: personalization ladder
    L = res["ladder"]
    budgets = [0, 5, 10, 20, 40]
    fig, ax = plt.subplots(figsize=(7, 4))
    m = [L[f"personal_{n}"]["mean"] for n in budgets]
    sd = [L[f"personal_{n}"]["sd"] for n in budgets]
    ax.errorbar(budgets, m, yerr=sd, color=ACCENT, marker="o", capsize=3, label="personal head (baseline + answers)")
    ax.axhline(L["generic"]["mean"], color=QUIET, linestyle="--", label="generic model")
    ax.axhline(L["baseline"]["mean"], color=SECOND, linestyle=":", label="personal baseline, no answers")
    ax.axhline(0.25, color="#cccccc", linewidth=0.8)
    ax.text(0, 0.26, "chance", color=QUIET, ha="left", fontsize=9)
    ax.set_xlabel("answers given by the user", color=QUIET)
    style(ax, "Each layer of personalization adds accuracy", "accuracy on later moments")
    ax.set_ylim(0.2, 0.8)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(out / "fig1_personalization.png", dpi=160)
    plt.close(fig)

    # Figure 2: active vs random questions
    A = res["active"]
    b2 = [5, 10, 20]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(b2))
    ax.bar(x - 0.18, [A[f"random_{n}"]["mean"] for n in b2], 0.36, yerr=[A[f"random_{n}"]["sd"] for n in b2], color="#cfcac1", label="random moments", capsize=3)
    ax.bar(x + 0.18, [A[f"active_{n}"]["mean"] for n in b2], 0.36, yerr=[A[f"active_{n}"]["sd"] for n in b2], color=ACCENT, label="ambiguous moments (conformal set of 2-3)", capsize=3)
    ax.set_xticks(x, [f"{n} questions" for n in b2])
    style(ax, "Choosing when to ask helps only a little here", "accuracy on later moments")
    ax.set_ylim(0.4, 0.75)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(out / "fig2_active_vs_random.png", dpi=160)
    plt.close(fig)

    # Figure 3: decisions and drift
    C, D = res["conformal"], res["drift"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    shares = [C[f"per_state_share_{d}"]["mean"] for d in ("speak", "ask", "quiet")]
    axes[0].bar(["speaks", "asks", "stays quiet"], shares, color=[SECOND, ACCENT, "#cfcac1"])
    for i, v in enumerate(shares):
        axes[0].text(i, v + 0.01, f"{v:.0%}", ha="center", color=INK, fontsize=10)
    style(axes[0], "With a generic model, Nightlet would mostly have to ask", "share of moments")
    names = ["fixed_baseline", "rolling_baseline", "no_shift_rolling"]
    labels = ["fixed baseline", "rolling baseline", "no change (reference)"]
    vals = [D[n]["mean"] for n in names]
    axes[1].bar(labels, vals, yerr=[D[n]["sd"] for n in names], color=["#cfcac1", ACCENT, SECOND], capsize=3)
    style(axes[1], "After a step change in the signals", "accuracy on later moments")
    axes[1].set_ylim(0.4, 0.75)
    fig.tight_layout()
    fig.savefig(out / "fig3_decisions_and_drift.png", dpi=160)
    plt.close(fig)


    # Figure 4: from today's approach to the full loop, for users who are never asked
    E = res["cohort"]
    steps = ["today_generic", "plus_baseline", "plus_cohort_10", "plus_cohort_25", "plus_cohort_50", "full_loop_20_answers"]
    names = ["today:\ngeneric model\non public data", "+ personal\nbaseline", "+ cohort\n10 users", "+ cohort\n25 users", "+ cohort\n50 users", "full loop:\nuser also\nanswers 20"]
    fig, ax = plt.subplots(figsize=(9, 4.4))
    vals = [E[k]["mean"] for k in steps]
    cols = ["#cfcac1", "#cfcac1", SECOND, SECOND, SECOND, ACCENT]
    ax.bar(range(len(steps)), vals, yerr=[E[k]["sd"] for k in steps], color=cols, capsize=3)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.02, f"{v:.0%}", ha="center", color=INK, fontsize=10)
    ax.set_xticks(range(len(steps)), names, fontsize=8.5)
    style(ax, "A private cohort's answers improve readings even for users who are never asked", "accuracy on later moments")
    ax.set_ylim(0.3, 0.75)
    fig.tight_layout()
    fig.savefig(out / "fig4_cohort_transfer.png", dpi=160)
    plt.close(fig)

    def f(block, key):
        v = res[block][key]
        return f"{v['mean']:.3f} ± {v['sd']:.3f}"

    lines = [
        "# Simulation results",
        "",
        f"Synthetic users, {len(seeds)} seeds, mean ± standard deviation across seeds. "
        "Four states (calm, energized, tense, low); chance is 0.25. "
        "These numbers describe the method on simulated data, not real users.",
        "",
        "## A. Personalization ladder (accuracy on later moments)",
        "",
        "| Model | Accuracy |",
        "| --- | --- |",
        f"| Generic model, raw signals | {f('ladder', 'generic')} |",
        f"| Personal baseline, no answers | {f('ladder', 'baseline')} |",
    ] + [f"| Personal head, {n} answers | {f('ladder', f'personal_{n}')} |" for n in (5, 10, 20, 40)] + [
        "",
        "## B. Active versus random questions",
        "",
        "| Budget | Random moments | Ambiguous moments |",
        "| --- | --- | --- |",
    ] + [f"| {n} | {f('active', f'random_{n}')} | {f('active', f'active_{n}')} |" for n in (5, 10, 20)] + [
        "",
        "## C. Conformal sets (target coverage 0.90)",
        "",
        "| Variant | Coverage | Worst state | Mean set size | Speaks | Asks | Quiet | Accuracy when speaking |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ] + [
        f"| {v} | {f('conformal', f'{v}_coverage')} | {f('conformal', f'{v}_worst_state_coverage')} | {f('conformal', f'{v}_mean_set_size')} | "
        f"{f('conformal', f'{v}_share_speak')} | {f('conformal', f'{v}_share_ask')} | {f('conformal', f'{v}_share_quiet')} | {f('conformal', f'{v}_accuracy_when_speaking')} |"
        for v in ("global", "per_state")
    ] + [
        "",
        "## D. Drift: a step change in a user's signals",
        "",
        "| Baseline | Accuracy after the change |",
        "| --- | --- |",
        f"| Fixed at enrollment | {f('drift', 'fixed_baseline')} |",
        f"| Rolling | {f('drift', 'rolling_baseline')} |",
        f"| Rolling, no change (reference) | {f('drift', 'no_shift_rolling')} |",
        "",
        "## E. From today's approach to SOUL-Calibrate (users who are never asked)",
        "",
        "The shared model is trained on public data whose mapping from affect to signals differs from real users "
        "(domain shift). A private cohort answers 20 questions each; their answers retrain the shared model. "
        "Accuracy is measured on new users who answer nothing, except in the last row.",
        "",
        "| Setting | Accuracy |",
        "| --- | --- |",
        f"| Today: generic model on public data | {f('cohort', 'today_generic')} |",
        f"| + personal baseline (no labels) | {f('cohort', 'plus_baseline')} |",
        f"| + cohort of 10 users | {f('cohort', 'plus_cohort_10')} |",
        f"| + cohort of 25 users | {f('cohort', 'plus_cohort_25')} |",
        f"| + cohort of 50 users | {f('cohort', 'plus_cohort_50')} |",
        f"| Full loop: the new user also answers 20 questions | {f('cohort', 'full_loop_20_answers')} |",
        "",
    ]
    (out / "RESULTS.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
