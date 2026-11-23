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
    data = json.load(open(src, encoding="utf-8"))
    r = data.get("ladder", data)
    v = [r[k] for k in LADDER]
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(17, 4.6), gridspec_kw={"width_ratios": [1.6, 1, 1.25]})
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
    en = data.get("engine", {})
    rows = [("Public approach\ntoday", "Public approach today"), ("Our engine,\nno signature", "Our engine without the signature"),
            ("One voice-and-body\nreading", "+ answered voice notes also teach the signature")]
    got = [(lab, next((v for k, v in en.items() if k.startswith(key)), None)) for lab, key in rows]
    got = [(lab, v) for lab, v in got if v is not None]
    if got:
        xs = range(len(got))
        acc = [v["accuracy"] for _, v in got]
        right = [v["spoken_correct"] for _, v in got]
        w = 0.38
        a3.axvspan(len(got) - 1.5, len(got) - 0.5, color="#f1ede6", zorder=0)   # our reading, set apart
        b1 = a3.bar([x - w / 2 - 0.01 for x in xs], acc, w, color="#2A78D6", label="reading right", zorder=2)
        b2 = a3.bar([x + w / 2 + 0.01 for x in xs], right, w, color="#D07A1E", label="right when it speaks", zorder=2)
        for b, x in list(zip(b1, acc)) + list(zip(b2, right)):
            a3.text(b.get_x() + b.get_width() / 2, x + 0.02, f"{x:.2f}", ha="center", fontsize=9, color="#2b2925")
        a3.set_xticks(list(xs), [lab for lab, _ in got], fontsize=9)
        a3.set_ylim(0, 1.05)
        a3.axhline(0.25, color="#cfc9bd", linestyle="--", linewidth=1, zorder=1)
        a3.set_xlim(-0.6, len(got) - 0.4)
        a3.legend(frameon=False, fontsize=8.5, loc="upper left")
        a3.set_title("C. Inside the engine: one reading of the state", loc="left", fontsize=10.5)
        a3.spines[["top", "right"]].set_visible(False)
    else:
        a3.axis("off")
    fig.suptitle("Personal voice-and-body signatures from one fixed sentence (synthetic people)", x=0.01, ha="left",
                 fontsize=11.5)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ("../engine/examples/demo_out/anchors.json",
                                                     "results/fig10_voice_signatures.png")))
