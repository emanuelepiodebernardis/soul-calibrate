"""Command line.

    python -m soulcal demo --out demo_out            synthetic people, today's reading vs SOUL-Calibrate
    python -m soulcal run --readings my.csv --out o  your own readings (CSV format in soulcal/schema.py)
    python -m soulcal bench --readings my.csv        SOUL-Bench ladder B0-B6 against the self_report column
                          [--birth-date 1990-05-17]  only for the optional reflection layer
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import numpy as np

from . import patterns
from .bench import bench_table, soul_bench
from .engine import EngineConfig
from .run import run_stream, write_decisions
from .schema import Profile, read_csv, write_csv
from .synthetic import generate


def _fmt(values) -> str:
    v = np.array(values, dtype=float)
    v = v[~np.isnan(v)]
    return f"{v.mean():.2f} ± {v.std():.2f}" if len(v) else "–"


def demo(out: Path, people: int, weeks: int) -> None:
    out.mkdir(parents=True, exist_ok=True)
    variants = {
        "Today: generic reading (population norms, no questions)": (EngineConfig(personal=False, max_questions_per_day=0), False),
        "Personal baseline only (no questions)": (EngineConfig(max_questions_per_day=0), False),
        "SOUL-Calibrate: baseline + questions + corrections + memory": (EngineConfig(), True),
    }
    table: dict[str, list] = {}
    extra = {"inc_asks": 0, "inc_masking": 0, "masking": 0, "trust": []}
    first = None
    for name, (cfg, learn) in variants.items():
        rows = []
        for sd in range(people):
            readings, truth, masking = generate(days=7 * weeks, seed=sd)
            res = run_stream(readings, truth, Profile(readings[0].user_id), cfg, learn=learn, seed=sd, masking=masking)
            rows.append(res.weekly)
            if learn:
                inc = [d for d in res.decisions if d["reason"].startswith("your words")]
                extra["inc_asks"] += len(inc)
                extra["inc_masking"] += sum(d["masking"] for d in inc)
                extra["masking"] += sum(masking)
                extra["trust"].append(res.trust)
                if sd == 0:
                    first = (readings, truth, res)
        table[name] = rows

    lines = ["# soulcal demo: today's reading vs SOUL-Calibrate", "",
             f"{people} synthetic people, {weeks} weeks, 3 evening readings a day, every channel Nightlet reads "
             "(face, voice, words, heart rate, HRV, skin temperature, movement), with channels missing at "
             "realistic rates. Each person has a weekly routine, a serious-looking face, a flat voice, masks "
             "tension in words half of the time, and a resting heart rate far from the population average. "
             "At most one question a day. Synthetic data: the numbers show how the code behaves, not real users.", ""]
    for metric, label in (("accuracy", "Accuracy (4 states, chance 0.25)"), ("speak_share", "Share of readings where Nightlet speaks"),
                          ("accuracy_when_speaking", "Accuracy when Nightlet speaks"), ("questions", "Questions per week")):
        lines += [f"## {label}", "", "| Setting | " + " | ".join(f"Week {w + 1}" for w in range(weeks)) + " |",
                  "| --- | " + " | ".join("---" for _ in range(weeks)) + " |"]
        for name, rows in table.items():
            cells = [_fmt([r[w][metric] for r in rows if len(r) > w]) for w in range(weeks)]
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines.append("")
    prec = extra["inc_masking"] / max(extra["inc_asks"], 1)
    base_rate = extra["masking"] / (people * weeks * 21)
    trust = {c: np.mean([t[c] for t in extra["trust"]]) for c in extra["trust"][0]}
    lines += ["## Words vs expression",
              "",
              f"Questions triggered by an unusual disagreement between words and face, voice and body: {extra['inc_asks']}. "
              f"{prec:.0%} of them came at moments when the person was really masking tension "
              f"(masking happens at {base_rate:.0%} of readings).", "",
              "## What the head learned to trust (mean weight per channel; start: face 0.50, voice 0.60, words 0.80)", "",
              "| Face | Voice | Words |", "| --- | --- | --- |",
              f"| {trust['face']:.2f} | {trust['voice']:.2f} | {trust['text']:.2f} |", ""]
    ladder: dict[str, list] = {}
    for sd in range(people):
        readings, truth, _ = generate(days=7 * weeks, seed=sd)
        for name, m in soul_bench(readings, truth, seed=sd).items():
            ladder.setdefault(name, []).append(m)
    mean = {name: {k: float(np.nanmean([m[k] for m in ms])) for k in ms[0]} for name, ms in ladder.items()}
    lines += ["## SOUL-Bench ladder (mean over people)", "",
              "Every rung reads the same readings and is scored before it learns from them. "
              "Generic = population norms, no personal correction.", "", bench_table(mean), ""]
    (out / "DEMO.md").write_text("\n".join(lines), encoding="utf-8")

    readings, truth, res = first
    write_csv(readings, out / "example_readings.csv")
    write_decisions(res, out / "example_decisions.csv")
    res.engine.save(out / "example_engine_state.json")
    # Pattern graph as in a consented diary study (every reading labelled), see docs/22
    links = patterns.find_patterns(readings, truth)
    patterns.write(links, readings[0].user_id, out)
    print((out / "DEMO.md").read_text(encoding="utf-8"))
    print((out / "PATTERNS.md").read_text(encoding="utf-8"))


def run(readings_path: Path, out: Path, birth: date | None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    readings = read_csv(readings_path)
    users = sorted({r.user_id for r in readings})
    summary = {}
    for u in users:
        rs = [r for r in readings if r.user_id == u]
        labels = [r.self_report for r in rs]
        res = run_stream(rs, labels, Profile(u, birth), EngineConfig(), learn=True)
        write_decisions(res, out / f"{u}_decisions.csv")
        res.engine.save(out / f"{u}_engine_state.json")
        links = patterns.find_patterns(rs, labels, birth)
        patterns.write(links, u, out / u)
        summary[u] = {"readings": len(rs), "weekly": res.weekly, "channel_trust": res.trust}
    (out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


def bench(readings_path: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    readings = read_csv(readings_path)
    text = ["# SOUL-Bench on your readings", "", "Ground truth: the self_report column. Scored before learning.", ""]
    for u in sorted({r.user_id for r in readings}):
        rs = [r for r in readings if r.user_id == u]
        text += [f"## {u}", "", bench_table(soul_bench(rs, [r.self_report for r in rs], u)), ""]
    (out / "BENCH.md").write_text("\n".join(text), encoding="utf-8")
    print("\n".join(text))


def main() -> None:
    ap = argparse.ArgumentParser(prog="soulcal")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo")
    d.add_argument("--out", default="demo_out")
    d.add_argument("--people", type=int, default=20)
    d.add_argument("--weeks", type=int, default=6)
    r = sub.add_parser("run")
    r.add_argument("--readings", required=True)
    r.add_argument("--out", default="soulcal_out")
    r.add_argument("--birth-date", default=None)
    b = sub.add_parser("bench")
    b.add_argument("--readings", required=True)
    b.add_argument("--out", default="soulcal_bench")
    a = ap.parse_args()
    if a.cmd == "demo":
        demo(Path(a.out), a.people, a.weeks)
    elif a.cmd == "bench":
        bench(Path(a.readings), Path(a.out))
    else:
        run(Path(a.readings), Path(a.out), date.fromisoformat(a.birth_date) if a.birth_date else None)


if __name__ == "__main__":
    main()
