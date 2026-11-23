"""Figure for voice, words and body, from the engine's synthetic check.

    cd engine && python -m soulcal channels --out examples/demo_out
    cd ../sim && python plot_channels.py ../engine/examples/demo_out/channels.json results/fig9_voice_and_body.png
"""

from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def main(src: str, out: str) -> None:
    r = json.load(open(src, encoding="utf-8"))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.1, 1]})
    names = list(r["sources"])
    vals = [r["sources"][k]["accuracy"] for k in names]
    cols = ["#b9b2a5", "#8a8478", "#8a8478", "#2f7d8c", "#c4622d", "#c4622d"]
    bars = a1.barh(range(len(names)), vals, color=cols)
    a1.set_yticks(range(len(names)), names, fontsize=9.5)
    a1.invert_yaxis()
    for b, v in zip(bars, vals):
        a1.text(v + 0.01, b.get_y() + b.get_height() / 2, f"{v:.2f}", va="center", fontsize=9)
    a1.axvline(0.25, color="#e4e1db", linestyle="--", linewidth=1)
    a1.set_xlim(0, 1)
    a1.set_title("A. Each source alone and together (accuracy, weeks 5-6)", loc="left", fontsize=10.5)
    a1.spines[["top", "right"]].set_visible(False)
    xs = [float(k) for k in r["app_use"]]
    a2.plot(xs, [r["app_use"][k]["accuracy_all"] for k in r["app_use"]], "-o", color="#2f7d8c", label="Accuracy, all moments")
    a2.plot(xs, [r["app_use"][k]["tense_reached"] for k in r["app_use"]], "-o", color="#c4622d", label="Tense moments reached by the pulse")
    c = r["checkin"]["voice check-in"]
    a2.scatter([0.25], [c["tense_reached"]], marker="*", s=220, color="#c4622d", zorder=3,
               label="+ voice check-in when the body is aroused")
    a2.set_xscale("log")
    a2.set_xticks(xs, [f"{x:.0%}" for x in xs])
    a2.minorticks_off()
    a2.invert_xaxis()
    a2.set_ylim(0, 1)
    a2.set_xlabel("Share of moments in which the person uses the app (the bracelet is always on)", fontsize=9)
    a2.set_title("B. When the person is not talking", loc="left", fontsize=10.5)
    a2.legend(frameon=False, fontsize=8.5, loc="lower left")
    a2.grid(axis="y", color="#e4e1db", linewidth=0.8)
    a2.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Voice and words say which way; the body says how much and when (synthetic people)", x=0.01, ha="left", fontsize=11.5)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("../engine/examples/demo_out/channels.json",
                                                     "results/fig9_voice_and_body.png")))
