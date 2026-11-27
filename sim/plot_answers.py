"""Figure: right answers from people who find it hardest to tell their feelings apart, by how the system asks.

    cd engine && python -m soulcal understanding --out examples/demo_out
    cd ../sim && python plot_answers.py ../engine/examples/demo_out/understanding.json results/fig12_answers.png
"""

from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ORANGE, GREY, INK = "#D07A1E", "#9A948A", "#2b2925"
LABELS = ["Ask for\nthe name", "+ what is it like\n(pleasant? energy?)", "+ body first", "+ weigh by\nreliability",
          "+ layer over\n8 weeks"]


def main(src: str, out: str) -> None:
    ans = json.load(open(src, encoding="utf-8"))["answers"]
    fig, axes = plt.subplots(1, 2, figsize=(15, 4.6), sharey=True)
    x, w = np.arange(len(LABELS)), 0.38
    for ax, (rn, res) in zip(axes, ans["rounds"].items()):
        conds = list(res)
        for j, (g, col, lab) in enumerate((("hard", ORANGE, f"lowest {ans['hard_share']:.0%} in differentiation"),
                                            ("others", GREY, "everyone else"))):
            v = [res[c][g]["answers_right"] for c in conds]
            b = ax.bar(x + (j - 0.5) * w * 1.02, v, w, color=col, label=lab, zorder=2)
            for bb, val in zip(b, v):
                ax.text(bb.get_x() + bb.get_width() / 2, val + 0.004, f"{val:.2f}", ha="center", va="bottom",
                        fontsize=8.5, color=INK)
        ax.set_xticks(x, LABELS, fontsize=8.8)
        ax.set_ylim(0.6, 1.0)
        ax.set_title(rn, loc="left", fontsize=10.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    axes[0].set_ylabel("answers that match the true state")
    fig.suptitle(f"People who do not know what they feel: right answers by how the system asks "
                 f"({ans['people']} real profiles, simulated 8 weeks)", x=0.01, ha="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*sys.argv[1:3])
