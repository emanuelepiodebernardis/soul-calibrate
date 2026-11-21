# Authors and contributions

**Emanuele De Bernardis** — author of this repository: concept, design, documentation, simulation code and
evaluation protocol. Contact: emanuelepio.debernardis@gmail.com · GitHub: [emanuelepiodebernardis](https://github.com/emanuelepiodebernardis)

First written on 21 November 2026, as a proposal for the SOUL layer of Nightlet. The git history of this
repository records the date of each part.

## Original contributions

1. **SOUL-Calibrate:** a personal calibration loop for emotion-reading systems: entry calibration, a 5-second
   session anchor, a rolling personal baseline, and questions to the user when the model is unsure, with the
   options taken from a conformal prediction set. → `docs/01`–`docs/06`
2. **SOUL-Bench:** an evaluation protocol whose ground truth is the user, with a ladder of baselines (B0–B6),
   within-person metrics and one harness for in-house and partner models. → `docs/08`
3. **Private cohort pilot:** using a consented group's answers to improve readings for users who are never asked. → `docs/19`
4. **Transfer of clinical methods** (JITAI, micro-randomised trials, idiographic baselines, early-warning signals
   as soft signals, outcome monitoring, HRV biofeedback, emotion naming, alarm fatigue) to a wellbeing product. → `docs/12`
5. **Reuse of the author's prior research** on drift, conformal martingales, integer on-device inference and
   evidence maps. → `docs/13`
6. **Reading audit** of the language layer. → `docs/14`
7. **Simulation** of the loop with synthetic users. → `sim/`

## Credits

Ideas and findings of other researchers are cited in `docs/references.md`. Two open-source projects by RinDig
inspired parts of `docs/14` and `docs/17`; no code or text from them is included.

## License

MIT (see `LICENSE`). Anyone may use, modify and build on this work, including commercially, provided the
copyright notice with the author's name is kept.
