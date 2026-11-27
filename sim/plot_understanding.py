"""Figure for the understanding layer: real data and the two simulation rounds.

    cd engine && python -m soulcal understanding --out examples/demo_out
    cd ../sim && python plot_understanding.py ../engine/soulcal/data/esm_profiles.json \
        ../engine/examples/demo_out/understanding.json results/fig11_understanding_layer.png
"""

from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

BLUE, ORANGE, GREY, INK = "#2A78D6", "#D07A1E", "#9A948A", "#2b2925"
CONDS = [("No understanding layer", "No layer"), ("Layer at hard moments, for everyone", "At hard moments\n(everyone)"),
         ("Layer by need (person-level gate)", "Person-level\ngate")]


def main(prof_src: str, res_src: str, out: str) -> None:
    people = [p for p in json.load(open(prof_src, encoding="utf-8"))["people"] if p["neg_diff"] is not None]
    res = json.load(open(res_src, encoding="utf-8"))
    na = np.array([p["na_mean"] for p in people])
    dif = np.array([p["neg_diff"] for p in people])
    rho = res["real_data"]["spearman_negative_affect_vs_differentiation"]
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(17, 4.8), gridspec_kw={"width_ratios": [1.1, 1, 1]})
    need = (na >= np.percentile(na, 75)) | (dif <= np.percentile(dif, 25))
    a1.scatter(na[~need], dif[~need], s=12, color=GREY, alpha=0.55, label="doing well", linewidths=0)
    a1.scatter(na[need], dif[need], s=12, color=ORANGE, alpha=0.75, label="needs it", linewidths=0)
    a1.set_xlabel("mean negative affect (0-1)")
    a1.set_ylabel("telling negative emotions apart\n(differentiation)")
    a1.set_title(f"A. {len(people)} real people, 5 open studies: rho = {rho:.2f}", loc="left", fontsize=10.5)
    a1.legend(frameon=False, fontsize=8.5, loc="lower left")
    rounds = list(res["rounds"])
    x = np.arange(len(CONDS))
    w = 0.38
    for ax, key, title, fmt in ((a2, "confusion_end", "B. Tense/low swapped by people who need it", "{:.2f}"),
                                (a3, "negative_affect_change", "C. Negative affect after 8 weeks, people who need it", "{:+.0%}")):
        for j, (rn, col) in enumerate(zip(rounds, (BLUE, "#6DA7EC"))):
            v = [res["rounds"][rn][c]["need"][key] for c, _ in CONDS]
            b = ax.bar(x + (j - 0.5) * w * 1.02, v, w, color=col, label=rn.split(" (")[0] + (" (as reported)" if j == 0 else " (conservative)"), zorder=2)
            for bb, val in zip(b, v):
                ax.text(bb.get_x() + bb.get_width() / 2, val + (0.006 if val >= 0 else -0.006), fmt.format(val),
                        ha="center", va="bottom" if val >= 0 else "top", fontsize=8.5, color=INK)
        ax.set_xticks(x, [s for _, s in CONDS], fontsize=9)
        ax.set_title(title, loc="left", fontsize=10.5)
        ax.axhline(0, color="#cfc9bd", linewidth=1)
        ax.legend(frameon=False, fontsize=8.5, loc="lower left" if key == "negative_affect_change" else "upper right")
    a3.set_ylim(min(-0.13, a3.get_ylim()[0]), 0.02)
    for ax in (a1, a2, a3):
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("The understanding layer: who needs it (real data) and what it may do (simulated, effects from published studies)",
                 x=0.01, ha="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*sys.argv[1:4])
