"""Figure for when the bracelet pulses, from the engine's synthetic check.

    cd engine && python -m soulcal support --out examples/demo_out
    cd ../sim && python plot_support.py ../engine/examples/demo_out/support.json results/fig8_when_to_pulse.png
"""

from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

SHORT = {"body": "Body alone\n(heart rate up, still)", "generic": "Generic reading\n(today)",
         "fixed": "Calibrated decision,\none rhythm", "learned": "Calibrated decision,\nrhythm learned per person"}


def main(src: str, out: str) -> None:
    res = json.load(open(src, encoding="utf-8"))
    keys = list(SHORT)
    helped = [res[k]["tense_moments_helped"] for k in keys]
    precise = [res[k]["precision"] for k in keys]
    excite = [res[k]["false_on_excitement"] for k in keys]
    x = np.arange(len(keys))
    fig, ax = plt.subplots(figsize=(10.5, 4.6))
    w = 0.26
    for off, vals, col, lab in ((-w, helped, "#c4622d", "Tense moments helped (pulse or accepted offer)"),
                                (0, precise, "#2f7d8c", "Pulses that came at tense moments"),
                                (w, excite, "#b9b2a5", "Pulses that came during excitement")):
        bars = ax.bar(x + off, vals, w * 0.95, color=col, label=lab)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.0%}", ha="center", fontsize=9, color="#2b2925")
    ax.set_xticks(x, [SHORT[k] for k in keys], fontsize=9.5)
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0%", "25%", "50%", "75%", "100%"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e4e1db", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(0, 1.16), ncol=3)
    ax.set_title("When the bracelet pulses (synthetic people; the effect of a pulse is an assumption)", loc="left",
                 fontsize=11, pad=34)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("../engine/examples/demo_out/support.json",
                                                     "results/fig8_when_to_pulse.png")))
