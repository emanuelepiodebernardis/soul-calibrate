"""Command line.

    python -m soulcal demo --out demo_out            synthetic people, today's reading vs SOUL-Calibrate
    python -m soulcal run --readings my.csv --out o  your own readings (CSV format in soulcal/schema.py)
    python -m soulcal bench --readings my.csv        SOUL-Bench ladder B0-B6 against the self_report column
    python -m soulcal archetypes --out demo_out      future phase: archetypes from a synthetic cohort
    python -m soulcal support --out demo_out         when and how the bracelet should pulse (synthetic)
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


def archetypes_demo(out: Path, seeds: int) -> None:
    from .archetypes import synthetic_check
    out.mkdir(parents=True, exist_ok=True)
    res = synthetic_check(seeds=seeds)
    weeks = len(next(iter(res.values()))["generic"])
    head = " | ".join(f"Week {w + 1}" for w in range(weeks))
    text = ["# Archetypes (future phase, synthetic people only)", "",
            f"A cohort of 24 consenting synthetic people (three types, 8 each) answers questions for 6 weeks; their "
            f"first 4 days of readings give a label-free signature, grouped into 3 archetypes. New people are matched "
            f"after 4 days and start from their archetype's fusion head. Control: one fusion head pooled over the whole "
            f"cohort. All starts keep asking up to 1 question a day. Accuracy per week, {seeds} seeds, 8 new people per type and seed.", "",
            f"| New person | Start | {head} | Matched to an archetype |",
            "| --- | --- | " + " | ".join("---" for _ in range(weeks)) + " | --- |"]
    for name, r in res.items():
        text.append(f"| {name} | generic | " + " | ".join(f"{v:.3f}" for v in r["generic"]) + " | |")
        text.append(f"| {name} | cohort, pooled | " + " | ".join(f"{v:.3f}" for v in r["pooled"]) + " | |")
        text.append(f"| {name} | archetype | " + " | ".join(f"{v:.3f}" for v in r["archetype"]) + f" | {r['matched']:.0%} |")
    (out / "ARCHETYPES.md").write_text("\n".join(text) + "\n", encoding="utf-8")
    (out / "archetypes.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("\n".join(text))


def support_demo(out: Path, seeds: int) -> None:
    from .support_sim import support_check
    out.mkdir(parents=True, exist_ok=True)
    res = support_check(seeds=seeds)
    text = ["# When to pulse (synthetic people; the effect of a pulse is an assumption)", "",
            f"20 synthetic people per seed, {seeds} seeds, 6 weeks, 3 evening readings a day. A pulse helps only when "
            "the person is tense: the pattern that suits them adds about 1.0 to recovery, the other about 0.2. Each "
            "false pulse makes the person turn pulses off with probability 5%. Same gates for every policy: bracelet "
            "worn, not moving, at most 3 a day, 90 minutes apart; 20% of eligible moments held out to measure the effect.",
            "", "| When to pulse | Pulses per week | Pulses at tense moments | Pulses at excitement | "
            "Tense moments helped (pulse or accepted offer) | Extra recovery per tense moment | People who turned pulses off |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in res.values():
        text.append(f"| {r['label']} | {r['pulses_per_week']:.2f} | {r['precision']:.0%} | {r['false_on_excitement']:.0%} | "
                    f"{r['tense_moments_helped']:.0%} | {r['extra_recovery_per_tense_moment']:.2f} | {r['turned_pulses_off']:.0%} |")
    lr = res["learned"]
    text += ["", f"Pattern learned per person after 6 weeks: the one that suits them in {lr['right_pattern']:.0%} of people "
             f"(50% by chance); error of the measured effect against the true one {lr['effect_error']:.2f} (true effect about 1.0)."]
    (out / "SUPPORT.md").write_text("\n".join(text) + "\n", encoding="utf-8")
    (out / "support.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("\n".join(text))


def channels_demo(out: Path, seeds: int) -> None:
    from .channels_sim import app_use_check, checkin_check, frontend_check, sources_check
    out.mkdir(parents=True, exist_ok=True)
    a, b, c = sources_check(seeds=seeds), app_use_check(seeds=seeds), checkin_check(seeds=seeds)
    d = frontend_check(seeds=seeds)
    f = lambda v: "–" if v != v else f"{v:.2f}"  # noqa: E731
    t = ["# Voice, words, face and body (synthetic people)", "",
         f"Engine demo people, {seeds} seeds x 20 people, up to 1 question a day, 6 weeks; scored on weeks 5-6, before learning.", "",
         "## A. One set of sources at a time, present at every moment", "",
         "| Sources | Accuracy | Speaks | Right when it speaks |", "| --- | --- | --- | --- |"]
    for k, v in a.items():
        t.append(f"| {k} | {f(v['accuracy'])} | {v['speak_share']:.0%} | {f(v['speak_accuracy'])} |")
    t += ["", "## B. The bracelet is always on; the app is used in a share of moments", "",
          "| Moments with the app | Accuracy, all | With the app | Body-only moments | Tense moments reached (pulse or offer) | Pulses at tense moments |",
          "| --- | --- | --- | --- | --- | --- |"]
    for k, v in b.items():
        t.append(f"| {float(k):.0%} | {f(v['accuracy_all'])} | {f(v['accuracy_app'])} | {f(v['accuracy_body_only'])} | "
                 f"{v['tense_reached']:.0%} | {v['pulse_precision']:.0%} |")
    t += ["", "## C. The body triggers, the voice decides (app used in 25% of moments)", "",
          "At a body-only moment, body aroused and tension possible: a 5-second voice note is invited (at most 1 a day; "
          "half of the invitations answered).", "",
          "| Policy | Accuracy, body-only moments | Tense moments reached | Pulses at tense moments | Invitations per week |",
          "| --- | --- | --- | --- | --- |"]
    for k, v in c.items():
        t.append(f"| {k} | {f(v['accuracy_body_only_moments'])} | {v['tense_reached']:.0%} | {v['pulse_precision']:.0%} | "
                 f"{v['invitations_per_week']:.1f} |")
    t += ["", "## D. Stronger speech front ends (open speech-recognition and speech-emotion models)", "",
          "How clearly voice and words show the state is multiplied; each person's habits (flat voice, serious face, "
          "saying 'fine' when tense) stay the same.", "",
          "| Front end | Generic reading | With personal calibration | Gain |", "| --- | --- | --- | --- |"]
    for k, v in d.items():
        t.append(f"| {k} | {f(v['generic'])} | {f(v['calibrated'])} | {v['calibrated'] - v['generic']:+.2f} |")
    (out / "CHANNELS.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    (out / "channels.json").write_text(json.dumps({"sources": a, "app_use": b, "checkin": c, "frontend": d}, indent=1),
                                       encoding="utf-8")
    print("\n".join(t))


def haptics_demo(out: Path, seeds: int) -> None:
    from .haptics_sim import haptics_check
    out.mkdir(parents=True, exist_ok=True)
    r = haptics_check(seeds=seeds)
    t = ["# Tuning the pulse to each person (synthetic; the effects are assumptions from the literature)", "",
         f"{seeds} seeds x 200 people, 24 tense moments each. Effect = calming effect of one pulse (1.0 = full).", "",
         "| Rhythm | Mean effect | Effect, last 8 moments | Heartbeat pulses faster than the heart |", "| --- | --- | --- | --- |"]
    for v in r.values():
        t.append(f"| {v['label']} | {v['effect']:.2f} | {v['effect_last8']:.2f} | {v['faster_than_heart']:.1%} |")
    (out / "HAPTICS.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    (out / "haptics.json").write_text(json.dumps(r, indent=1), encoding="utf-8")
    print("\n".join(t))


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
    c = sub.add_parser("archetypes")
    c.add_argument("--out", default="demo_out")
    c.add_argument("--seeds", type=int, default=10)
    su = sub.add_parser("support")
    su.add_argument("--out", default="demo_out")
    su.add_argument("--seeds", type=int, default=5)
    ch = sub.add_parser("channels")
    ch.add_argument("--out", default="demo_out")
    ch.add_argument("--seeds", type=int, default=5)
    hp = sub.add_parser("haptics")
    hp.add_argument("--out", default="demo_out")
    hp.add_argument("--seeds", type=int, default=5)
    a = ap.parse_args()
    if a.cmd == "demo":
        demo(Path(a.out), a.people, a.weeks)
    elif a.cmd == "channels":
        channels_demo(Path(a.out), a.seeds)
    elif a.cmd == "haptics":
        haptics_demo(Path(a.out), a.seeds)
    elif a.cmd == "support":
        support_demo(Path(a.out), a.seeds)
    elif a.cmd == "archetypes":
        archetypes_demo(Path(a.out), a.seeds)
    elif a.cmd == "bench":
        bench(Path(a.readings), Path(a.out))
    else:
        run(Path(a.readings), Path(a.out), date.fromisoformat(a.birth_date) if a.birth_date else None)


if __name__ == "__main__":
    main()
