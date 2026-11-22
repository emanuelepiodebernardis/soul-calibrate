"""Personalization speed: how fast each question budget reaches a given accuracy.

    python run_speed.py --seeds 5 --out results

Questions stay allowed for 28 days (ambiguous moments, closed options); every reading is scored before
the model learns from it. Synthetic people only.
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

from soul_calibrate import situations as S  # noqa: E402

DAYS = 28
BUDGETS = (0.5, 1, 2, 4)
TARGETS = (0.80, 0.85, 0.90)
COLORS = {0.5: "#b9b2a5", 1: "#2f7d8c", 2: "#c4622d", 4: "#1f1e1c"}


def curves(budget: float, seeds: list[int]) -> dict:
    cfg = replace(S.SituationConfig(), calib_days=DAYS, test_days=0, questions_per_day=budget)
    acc, qcum = [], []
    for sd in seeds:
        captured = {}
        orig = S.summarise
        S.summarise = lambda logs, c: (captured.update(logs), orig(logs, c))[1]
        try:
            S.exp_situations(sd, cfg, qtypes=("closed",))
        finally:
            S.summarise = orig
        entries = captured[("closed", "ambiguous")]
        n_people = len({e["person"] for e in entries})
        a = [np.mean([e["correct"] for e in entries if e["day"] == d]) for d in range(DAYS)]
        q = np.cumsum([sum(1 for e in entries if e["day"] == d and e.get("asked")) / n_people for d in range(DAYS)])
        acc.append(a)
        qcum.append(q)
    acc_m = np.mean(acc, axis=0)
    # smooth over 3 days so the day a target is reached is not decided by one noisy day
    smooth = np.convolve(acc_m, np.ones(3) / 3, mode="same")
    smooth[0], smooth[-1] = acc_m[0], acc_m[-1]
    reach = {}
    for t in TARGETS:
        hit = np.flatnonzero(smooth >= t)
        reach[str(t)] = int(hit[0]) + 1 if len(hit) else None
    return {"accuracy_by_day": acc_m.tolist(), "questions_cumulative": np.mean(qcum, axis=0).tolist(), "days_to": reach,
            "plateau_last_week": float(np.mean(acc_m[-7:]))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    seeds = list(range(a.seeds))
    res = {str(b): curves(b, seeds) for b in BUDGETS}
    Path(a.out, "speed.json").write_text(json.dumps(res, indent=1))

    L = ["# Personalization speed: how fast each question budget gets there", "",
         f"Synthetic people, {len(seeds)} seeds, 60 people each; 6 recurring situations; 4 readings a day; questions "
         f"allowed for {DAYS} days at ambiguous moments with closed options; each reading scored before learning. "
         "Accuracy smoothed over 3 days to find the first day a level is reached. No questions: about 0.50.", "",
         "| Questions allowed per day | Day 3 | Day 7 | Day 14 | Day 28 | Days to 0.80 | Days to 0.85 | Days to 0.90 | "
         "Questions asked by day 7 | by day 14 | by day 28 |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for b, r in res.items():
        acc, q, d = r["accuracy_by_day"], r["questions_cumulative"], r["days_to"]
        def f(x):
            return "not reached" if x is None else str(x)
        L.append(f"| {b} | {acc[2]:.2f} | {acc[6]:.2f} | {acc[13]:.2f} | {acc[27]:.2f} | {f(d['0.8'])} | {f(d['0.85'])} | "
                 f"{f(d['0.9'])} | {q[6]:.1f} | {q[13]:.1f} | {q[27]:.1f} |")
    Path(a.out, "SPEED.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

    fig, ax = plt.subplots(figsize=(8, 4.4))
    days = np.arange(1, DAYS + 1)
    for b, r in res.items():
        ax.plot(days, r["accuracy_by_day"], color=COLORS[float(b) if "." in b else int(b)], linewidth=2.2,
                label=f"up to {b} question{'s' if b != '1' else ''} a day")
    for t in TARGETS:
        ax.axhline(t, color="#e4e1db", linewidth=0.8, zorder=0)
    ax.axhline(0.5, color="#b9b2a5", linewidth=1, linestyle="--")
    ax.text(1.5, 0.51, "no questions", ha="left", fontsize=8, color="#8a8478")
    ax.set_ylim(0.45, 1.0)
    ax.set_xlabel("Day", color="#8a8478")
    ax.set_title("Personalization speed by question budget (synthetic people)", loc="left", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    fig.savefig(Path(a.out, "fig6_personalization_speed.png"), dpi=160)


if __name__ == "__main__":
    main()
