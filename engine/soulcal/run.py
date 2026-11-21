"""Run the engine over a stream of readings and measure it against today's generic reading.

When a reading has a known state (a self-report in real data, the truth in the demo), it plays the
user: questions are answered (closed options; 5% slips), and a wrong spoken reading is corrected with a
one-tap "not quite" with some probability. Readings are scored before the engine learns from them.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .engine import ASK, SPEAK, EngineConfig, SoulEngine
from .schema import STATES, Profile, Reading


@dataclass
class RunResult:
    decisions: list = field(default_factory=list)
    weekly: list = field(default_factory=list)      # per week: dict of metrics
    labels_used: list = field(default_factory=list)  # label per reading that the engine learned (or None)


def run_stream(readings: list[Reading], truth: list[str | None], profile: Profile,
               config: EngineConfig | None = None, learn: bool = True, correct_p: float = 0.3,
               slip: float = 0.05, seed: int = 0, masking: list[bool] | None = None) -> RunResult:
    rng = np.random.default_rng(seed)
    eng = SoulEngine(profile, config)
    res = RunResult()
    start = readings[0].timestamp
    for i, (r, y) in enumerate(zip(readings, truth)):
        d = eng.observe(r)
        pred = max(d.proba, key=d.proba.get)
        week = (r.timestamp - start).days // 7
        res.decisions.append({"timestamp": r.timestamp.isoformat(), "action": d.action, "state": d.state,
                              "options": "|".join(d.options), "predicted": pred, "truth": y,
                              "incongruence": None if d.incongruence is None else round(d.incongruence, 2),
                              "reason": d.reason, "week": week,
                              "masking": bool(masking[i]) if masking else None,
                              **{f"p_{s}": round(d.proba[s], 3) for s in STATES}})
        label = None
        if learn and y is not None:
            if d.action == ASK:
                if y in d.options and rng.random() > slip:
                    label = y
                elif y in d.options:
                    label = str(rng.choice([o for o in d.options if o != y] or [y]))
                else:
                    label = y     # "none of these", then the user names the state
                eng.answer(d.reading_index, label)
            elif d.action == SPEAK and d.state != y and rng.random() < correct_p:
                label = y
                eng.correct(d.reading_index, y)
        res.labels_used.append(label)
    weeks = sorted({x["week"] for x in res.decisions})
    for w in weeks:
        rows = [x for x in res.decisions if x["week"] == w and x["truth"] is not None]
        if not rows:
            continue
        speak = [x for x in rows if x["action"] == SPEAK]
        asks = [x for x in rows if x["action"] == ASK]
        res.weekly.append({
            "week": w + 1, "readings": len(rows),
            "accuracy": float(np.mean([x["predicted"] == x["truth"] for x in rows])),
            "speak_share": len(speak) / len(rows),
            "accuracy_when_speaking": float(np.mean([x["state"] == x["truth"] for x in speak])) if speak else float("nan"),
            "questions": len(asks),
            "truth_in_options": float(np.mean([x["truth"] in x["options"].split("|") for x in asks])) if asks else float("nan"),
        })
    res.trust = eng.channel_trust()
    res.engine = eng
    return res


def write_decisions(res: RunResult, path: str | Path) -> None:
    if not res.decisions:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(res.decisions[0].keys()))
        w.writeheader()
        w.writerows(res.decisions)
