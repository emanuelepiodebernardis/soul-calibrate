"""Coarse to fine: four main states first, or the level of detail chosen per reading.

    python run_progressive.py --seeds 5 --out results

Synthetic people living eight states; every reading scored before learning. Synthetic people only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from soul_calibrate.progressive import run  # noqa: E402

MODES = {
    "fine": ("Eight states from day one", {}),
    "switch": ("Four main states, switch to eight on day 7", {"switch_day": 7}),
    "adaptive": ("Four main states, switch when readings are confident", {"agree_level": 0.6}),
    "per_reading": ("Level of detail chosen per reading", {}),
}
DAYS = 28


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    seeds = list(range(a.seeds))
    res: dict = {}
    for budget in (1, 2):
        for mode, (label, kw) in MODES.items():
            runs = [run(sd, mode, budget=budget, days=DAYS, **kw) for sd in seeds]
            res[f"{budget}/{mode}"] = {
                "label": label, "budget": budget,
                "shown": np.mean([r["shown"] for r in runs], 0).tolist(),
                "fine": np.mean([r["fine"] for r in runs], 0).tolist(),
                "fine_shown_share": np.mean([r["fine_shown_share"] for r in runs], 0).tolist(),
                "questions": np.mean([r["questions"] for r in runs], 0).tolist(),
                "switch_day": float(np.mean([r["switch_day_mean"] for r in runs])),
            }
    Path(a.out, "progressive.json").write_text(json.dumps(res, indent=1))

    L = ["# Coarse to fine", "",
         f"Synthetic people living eight states (four main states and an intermediate one between each pair), "
         f"{len(seeds)} seeds, 60 people each; 6 recurring situations, 4 readings a day; questions allowed for {DAYS} days "
         "at ambiguous moments with closed options; every reading scored before learning.", "",
         "- **Shown precision:** the reading is right at the level of detail shown (a main state counts as right "
         "for an intermediate state next to it).",
         "- **Fine precision:** the model's best guess among the eight states, shown or not.", "",
         "| Budget | Approach | Shown, day 3 | Shown, day 7 | Shown, day 14 | Shown, day 28 | Fine, day 14 | Fine, day 28 | "
         "Fine readings shown, day 28 | Mean switch day | Questions by day 28 |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for k, r in res.items():
        s, f, fs = r["shown"], r["fine"], r["fine_shown_share"]
        fs28 = "all" if k.endswith("/fine") or (k.endswith(("switch", "adaptive")) and r["switch_day"] < DAYS and False) else f"{fs[27]:.0%}"
        if k.endswith("/fine"):
            fs28 = "100%"
        elif k.endswith(("/switch", "/adaptive")):
            fs28 = "100% after the switch"
        sw = "–" if k.endswith(("/fine", "/per_reading")) else f"{r['switch_day']:.1f}"
        L.append(f"| {r['budget']}/day | {r['label']} | {s[2]:.2f} | {s[6]:.2f} | {s[13]:.2f} | {s[27]:.2f} | {f[13]:.2f} | "
                 f"{f[27]:.2f} | {fs28} | {sw} | {r['questions'][27]:.1f} |")
    Path(a.out, "PROGRESSIVE.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    colors = {"fine": "#b9b2a5", "switch": "#2f7d8c", "adaptive": "#8a8478", "per_reading": "#c4622d"}
    days = np.arange(1, DAYS + 1)
    for ax, key, title in ((axes[0], "shown", "Shown precision (what the user sees)"),
                           (axes[1], "fine", "Fine precision (eight states)")):
        for mode in MODES:
            r = res[f"1/{mode}"]
            ax.plot(days, r[key], color=colors[mode], linewidth=2.2, label=r["label"])
        ax.set_title(title, loc="left", fontsize=11)
        ax.set_xlabel("Day (up to 1 question a day)", color="#8a8478")
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e4e1db", linewidth=0.8)
    axes[0].set_ylim(0.3, 1.0)
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(Path(a.out, "fig7_coarse_to_fine.png"), dpi=160)


if __name__ == "__main__":
    main()
