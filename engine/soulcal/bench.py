"""SOUL-Bench in code: one harness, the user's own labels as ground truth, a ladder of baselines.

Every rung reads the same readings, in time order, and is scored on readings with a known state
before it learns from them (no peeking). Rungs:

    B0  the user's own running average state (needs no signal at all)
    B1  words only, generic          B2  voice only, generic          B3  face only, generic
    B4  all channels fused, generic (population norms, no personal correction)
    B5  B4 read against the personal baseline (no questions)
    B6  the full loop: B5 + questions, corrections and situation memory

If a fancy rung cannot beat B0 for a person, that is worth knowing. Metrics are within-person:
accuracy over the first and last weeks, per-state recall, accuracy when the system speaks, share of
readings where it speaks. Run any model of Nightlet or of a partner as a channel and it goes through the same
ladder unchanged.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import replace

import numpy as np

from .engine import EngineConfig
from .run import run_stream
from .schema import STATES, Profile, Reading


def _only(r: Reading, channel: str) -> Reading:
    keep = {c: (r.channel(c) if c == channel else None) for c in ("face", "voice", "text")}
    return replace(r, heart_rate=None, hrv_rmssd=None, skin_temp=None, motion=None, **keep)


def _score(decisions: list[dict], weeks_tail: int = 2) -> dict:
    rows = [d for d in decisions if d["truth"] is not None]
    if not rows:
        return {}
    last_week = max(d["week"] for d in rows)
    tail = [d for d in rows if d["week"] > last_week - weeks_tail]
    head = [d for d in rows if d["week"] < weeks_tail]
    speak = [d for d in rows if d["action"] == "speak"]
    out = {
        "accuracy_first_weeks": float(np.mean([d["predicted"] == d["truth"] for d in head])) if head else float("nan"),
        "accuracy_last_weeks": float(np.mean([d["predicted"] == d["truth"] for d in tail])),
        "speak_share": len(speak) / len(rows),
        "accuracy_when_speaking": float(np.mean([d["state"] == d["truth"] for d in speak])) if speak else float("nan"),
    }
    for s in STATES:
        rs = [d for d in tail if d["truth"] == s]
        out[f"recall_{s}"] = float(np.mean([d["predicted"] == s for d in rs])) if rs else float("nan")
    return out


def _running_average(truth: list[str | None], readings: list[Reading]) -> dict:
    seen: Counter = Counter()
    decisions = []
    start = readings[0].timestamp
    for r, y in zip(readings, truth):
        pred = seen.most_common(1)[0][0] if seen else STATES[0]
        decisions.append({"truth": y, "predicted": pred, "state": pred, "action": "speak", "options": "",
                          "week": (r.timestamp - start).days // 7, **{f"p_{s}": float(s == pred) for s in STATES}})
        if y is not None:
            seen[y] += 1
    return _score(decisions)


def soul_bench(readings: list[Reading], truth: list[str | None], user_id: str = "user",
               config: EngineConfig | None = None, seed: int = 0) -> dict[str, dict]:
    cfg = config or EngineConfig()
    quiet = replace(cfg, max_questions_per_day=0)
    generic = replace(quiet, personal=False)
    prof = Profile(user_id)
    out = {"B0 user's own average": _running_average(truth, readings)}
    for name, ch in (("B1 words only", "text"), ("B2 voice only", "voice"), ("B3 face only", "face")):
        rs = [_only(r, ch) for r in readings]
        out[name] = _score(run_stream(rs, truth, prof, generic, learn=False, seed=seed).decisions)
    out["B4 all channels, generic"] = _score(run_stream(readings, truth, prof, generic, learn=False, seed=seed).decisions)
    out["B5 personal baseline"] = _score(run_stream(readings, truth, prof, quiet, learn=False, seed=seed).decisions)
    out["B6 full loop"] = _score(run_stream(readings, truth, prof, cfg, learn=True, seed=seed).decisions)
    return out


def bench_table(results: dict[str, dict]) -> str:
    cols = [("accuracy_first_weeks", "Accuracy, first 2 weeks"), ("accuracy_last_weeks", "Accuracy, last 2 weeks"),
            ("speak_share", "Speaks"), ("accuracy_when_speaking", "Accuracy when speaking"),
            ("recall_tense", "Recall: tense"), ("recall_low", "Recall: low")]
    lines = ["| Rung | " + " | ".join(c[1] for c in cols) + " |", "| --- | " + " | ".join("---" for _ in cols) + " |"]
    for name, m in results.items():
        cells = []
        for k, _ in cols:
            v = m.get(k, float("nan"))
            cells.append("–" if v != v else f"{v:.2f}")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)
