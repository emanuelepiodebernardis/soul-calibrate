"""How the pulse should be tuned to each person (docs/27).

    python -m soulcal haptics --out examples/demo_out

ASSUMED effects, drawn from the literature and written here so they can be changed:
* slow heartbeat: calming when slower than the heart rate the person has at that moment, best around 80% of it
  (Azevedo et al. 2017; Costa et al. 2017), and arousing when faster (MacDonald et al. 2023); its size depends on
  how well the person perceives their own body (Keio University, 2021), drawn per person;
* breathing pacer: slow breathing helps in general, most at the person's own resonance rate, which lies between
  4.5 and 7 breaths a minute and differs between people (Lehrer et al.; Shaffer and Meehan 2020).
The recovery measured after a pulse is the effect plus noise (sd 0.5). Each person gets 24 tense moments.
"""

from __future__ import annotations

import numpy as np

RATES = np.arange(4.5, 7.01, 0.5)


def _people(rng: np.random.Generator, n: int) -> list[dict]:
    out = []
    for _ in range(n):
        rest = float(rng.normal(64, 8))
        out.append({"rest": rest, "resonance": float(rng.uniform(4.5, 7.0)), "intero": float(rng.uniform(0.2, 1.2))})
    return out


def heartbeat_effect(rate: float, current_hr: float, intero: float) -> float:
    q = rate / current_hr
    if q >= 1.0:
        return -0.8 * intero * (q - 1.0) / 0.2          # faster than the heart: arousing
    return intero * float(np.exp(-((q - 0.8) / 0.15) ** 2))


def breathing_effect(rate: float, resonance: float) -> float:
    return 0.4 + 0.6 * float(np.exp(-((rate - resonance) / 0.75) ** 2))


POLICIES = {
    "hb_fixed": "Slow heartbeat, fixed at 60 a minute",
    "hb_rest": "Slow heartbeat, 80% of the resting heart rate",
    "hb_live": "Slow heartbeat, 80% of the heart rate right now",
    "br_fixed": "Breathing pacer, fixed at 6 a minute",
    "br_learned": "Breathing pacer, the person's resonance rate learned",
    "both_learned": "Rhythm and rate learned per person (live heartbeat or resonance breathing)",
}


def _thompson(stats: dict, keys, rng) -> object:
    def draw(k):
        n, m, ss = stats.get(k, (0, 0.0, 0.0))
        if n < 2:
            return rng.normal(0.8, 1.0)
        sd = np.sqrt(max(ss / (n - 1), 1e-4) / n)
        return rng.normal(m, sd)
    return max(keys, key=draw)


def _add(stats: dict, k, x: float) -> None:
    n, m, ss = stats.get(k, (0, 0.0, 0.0))
    n += 1
    d = x - m
    m += d / n
    ss += d * (x - m)
    stats[k] = (n, m, ss)


def haptics_check(seeds: int = 5, people: int = 200, episodes: int = 24) -> dict:
    res = {k: {"effect": [], "effect_last8": [], "faster_than_heart": 0, "pulses": 0} for k in POLICIES}
    for s in range(seeds):
        rng = np.random.default_rng(s)
        for p in _people(rng, people):
            for pol in POLICIES:
                stats: dict = {}
                prng = np.random.default_rng(int(rng.integers(1e9)))
                effects = []
                for e in range(episodes):
                    hr = p["rest"] + float(prng.uniform(5, 20))          # tense: above rest
                    if pol == "hb_fixed":
                        arm, rate = "hb", 60.0
                    elif pol == "hb_rest":
                        arm, rate = "hb", 0.8 * p["rest"]
                    elif pol == "hb_live":
                        arm, rate = "hb", 0.8 * hr
                    elif pol == "br_fixed":
                        arm, rate = "br", 6.0
                    elif pol == "br_learned":
                        arm, rate = "br", float(_thompson(stats, list(RATES), prng))
                    else:
                        choice = _thompson(stats, ["hb"] + [f"br{r}" for r in RATES], prng)
                        arm, rate = ("hb", 0.8 * hr) if choice == "hb" else ("br", float(choice[2:]))
                    eff = heartbeat_effect(rate, hr, p["intero"]) if arm == "hb" else breathing_effect(rate, p["resonance"])
                    obs = eff + float(prng.normal(0, 0.5))
                    if pol == "br_learned":
                        _add(stats, rate, obs)
                    elif pol == "both_learned":
                        _add(stats, "hb" if arm == "hb" else f"br{rate}", obs)
                    effects.append(eff)
                    res[pol]["pulses"] += arm == "hb"
                    res[pol]["faster_than_heart"] += arm == "hb" and rate >= hr
                res[pol]["effect"].append(np.mean(effects))
                res[pol]["effect_last8"].append(np.mean(effects[-8:]))
    return {k: {"label": POLICIES[k], "effect": float(np.mean(v["effect"])), "effect_last8": float(np.mean(v["effect_last8"])),
                "faster_than_heart": v["faster_than_heart"] / v["pulses"] if v["pulses"] else 0.0} for k, v in res.items()}
