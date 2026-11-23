"""Figure for personal voice-and-body signatures, from the engine's synthetic check.

    cd engine && python -m soulcal anchors --out examples/demo_out
    cd ../sim && python plot_anchors.py ../engine/examples/demo_out/anchors.json results/fig10_voice_signatures.png
"""

from __future__ import annotations

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LADDER = ["Generic (no personal reference)", "+ voice-and-body baseline (enrollment)", "+ daily 5-second anchor",
          "+ 1 tagged readings per state", "+ 2 tagged readings per state", "+ 4 tagged readings per state"]
SHORT = ["Generic", "+ baseline\n(first week)", "+ daily\n5-s anchor", "+ 1 tagged\nper state", "+ 2 tagged\nper state",
         "+ 4 tagged\nper state"]


def main(src: str, out: str) -> None:
    r = json.load(open(src, encoding="utf-8"))
    v = [r[k] for k in LADDER]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.4), gridspec_kw={"width_ratios": [1.6, 1]})
    a1.plot(range(len(v)), v, "-o", color="#c4622d", linewidth=2.4)
    for i, x in enumerate(v):
        a1.text(i, x + 0.025, f"{x:.2f}", ha="center", fontsize=9.5)
    a1.set_xticks(range(len(v)), SHORT, fontsize=9)
    a1.set_ylim(0.2, 1.0)
    a1.axhline(0.25, color="#e4e1db", linestyle="--", linewidth=1)
    a1.set_title("A. Accuracy on free voice notes, step by step", loc="left", fontsize=10.5)
    a1.grid(axis="y", color="#e4e1db", linewidth=0.8)
    a1.spines[["top", "right"]].set_visible(False)
    names = ["Voice only", "Body only", "Voice + body"]
    vals = [r["Voice only, + 2 tagged readings"], r["Body only, + 2 tagged readings"], r["+ 2 tagged readings per state"]]
    bars = a2.bar(names, vals, color=["#8a8478", "#b9b2a5", "#c4622d"])
    for b, x in zip(bars, vals):
        a2.text(b.get_x() + b.get_width() / 2, x + 0.02, f"{x:.2f}", ha="center", fontsize=9.5)
    a2.set_ylim(0, 1.0)
    a2.set_title("B. Signatures from voice, body, or both", loc="left", fontsize=10.5)
    a2.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Personal voice-and-body signatures from one fixed sentence (synthetic people)", x=0.01, ha="left",
                 fontsize=11.5)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("../engine/examples/demo_out/anchors.json",
                                                     "results/fig10_voice_signatures.png")))
