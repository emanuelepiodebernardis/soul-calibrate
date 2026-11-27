# soulcal — the SOUL-Calibrate engine

Author: Emanuele De Bernardis · MIT License · numpy only

The decision and personalization layer that sits on top of any face, voice and text emotion model and the
bracelet's signals: personal baseline, fusion with missing channels, speak / ask / quiet with conformal sets
and a question budget, situation memory, one-tap corrections, words-vs-expression disagreement, and a
personal pattern graph with statistical guardrails (including the astrology reflection layer).

```bash
pip install -e .                       # or just run from this folder
python -m pytest tests -q              # 28 tests
python -m soulcal bench --readings my_readings.csv
python -m soulcal demo --out examples/demo_out
python -m soulcal run --readings my_readings.csv --out results [--birth-date 1990-05-17]
python -m soulcal archetypes --out examples/demo_out    # future phase: archetypes, synthetic cohort
python -m soulcal support --out examples/demo_out       # when and how the bracelet pulses
python -m soulcal channels --out examples/demo_out      # voice, words, face and body
python -m soulcal haptics --out examples/demo_out       # tuning the pulse to the person
python -m soulcal anchors --out examples/demo_out       # voice-and-body signatures, alone and inside the engine
python -m soulcal understanding --out examples/demo_out # the understanding layer, people from open ESM data
```

Voice-and-body signatures (docs/29): `engine.enroll(x)`, `engine.anchor(x)`, `engine.tag("tense", x)`, then
`Reading(..., voice_features=x)`; the signature becomes the engine's voice channel.

- Input format: `soulcal/schema.py` (CSV columns or `Reading` objects).
- Python API and design: [docs/22-engine.md](../docs/22-engine.md).
- Demo outputs: `examples/demo_out/` (`DEMO.md`, `PATTERNS.md`, `patterns_map.html`, example readings,
  decisions and the engine's on-device state).
