"""When and how the bracelet should pulse (docs/26).

The pulse is an intervention, not a notification: its purpose is to help the person come back to calm. So it
follows the same rule as the reading. It acts only when the engine is sure the person is tense, offers when it is
unsure, and does nothing otherwise. Each person's response is measured on their own body, so the engine learns
which rhythm calms them.

* speak "tense"       -> pulse: a slow rhythm, with a line on screen (and a voice, if the user turned it on)
* ask, tense possible -> offer: one soft tap and "Want a calm minute?"; the answer is also a label
* anything else       -> nothing. Never for "energized": the body looks the same in excitement and anxiety.
* the user can always start a calm minute themselves (on demand)

Gates: the bracelet is worn, no strong movement (exercise raises heart rate without stress), a daily cap and a
cooldown, and the hours the user chose.

Patterns (from the literature, docs/26):
* slow_heartbeat: a heartbeat-like vibration below the person's own resting heart rate (Azevedo et al., 2017)
* breathing: a vibrotactile pacer at about 6 breaths a minute (Paredes et al., 2018; Miri et al., 2020)

Learning which pattern works for this person: after each pulse the heart rate and HRV of the next minutes are
compared with the moment before. A share of eligible moments is held out at random (a micro-randomised trial
inside the product), so the effect is measured against the person's own recovery without a pulse. Patterns are
chosen by Thompson sampling on that effect.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .engine import ASK, SPEAK, Decision
from .schema import Reading

PULSE, OFFER, NONE = "pulse", "offer", "none"
PATTERNS = ("slow_heartbeat", "breathing")


@dataclass
class SupportConfig:
    enabled: bool = True
    target_states: tuple = ("tense",)
    max_per_day: int = 3
    cooldown_minutes: int = 90
    motion_max: float = 0.8              # above this, the heart rate is likely movement, not stress
    hours: tuple | None = None           # the user's chosen window, e.g. (8, 23); None = any time
    offer_when_unsure: bool = True
    hold_out: float = 0.2                # share of eligible moments held out at random, to measure the effect
    heartbeat_ratio: float = 0.8         # slow heartbeat at 80% of the person's resting heart rate
    breaths_per_minute: float = 6.0
    minutes: float = 2.0
    voice: bool = False                  # the user's choice: a calm voice as well as the pulse
    screen: bool = True


@dataclass
class Support:
    action: str                          # "pulse" | "offer" | "none"
    pattern: str | None = None
    rate_per_minute: float | None = None
    minutes: float | None = None
    screen_text: str | None = None
    voice_text: str | None = None
    reason: str = ""
    held_out: bool = False               # eligible, but held out at random to measure the effect
    support_id: int = -1


@dataclass
class _Arm:
    n: int = 0
    mean: float = 0.0
    m2: float = 0.0

    def add(self, x: float) -> None:
        self.n += 1
        d = x - self.mean
        self.mean += d / self.n
        self.m2 += d * (x - self.mean)

    def sample(self, rng: np.random.Generator, prior_sd: float = 1.0) -> float:
        if self.n < 2:
            return float(rng.normal(0.0, prior_sd))
        sd = np.sqrt(self.m2 / (self.n - 1) / self.n)
        return float(rng.normal(self.mean, max(sd, 1e-3)))


class SupportPolicy:
    def __init__(self, config: SupportConfig | None = None, seed: int = 0):
        self.cfg = config or SupportConfig()
        self.rng = np.random.default_rng(seed)
        self.arms = {p: _Arm() for p in PATTERNS}
        self.held = _Arm()                       # recovery without a pulse, on eligible moments
        self.by_day: dict[str, int] = {}
        self.last: float | None = None           # timestamp (seconds) of the last pulse
        self._open: dict[int, dict] = {}
        self._n = 0

    def _gates(self, r: Reading) -> str | None:
        if r.heart_rate is None:
            return "bracelet not worn"
        if r.motion is not None and r.motion > self.cfg.motion_max:
            return "moving: heart rate is likely exercise"
        if self.cfg.hours is not None and not self.cfg.hours[0] <= r.timestamp.hour < self.cfg.hours[1]:
            return "outside the chosen hours"
        if self.by_day.get(r.timestamp.date().isoformat(), 0) >= self.cfg.max_per_day:
            return "daily cap reached"
        if self.last is not None and r.timestamp.timestamp() - self.last < 60 * self.cfg.cooldown_minutes:
            return "cooldown"
        return None

    def _pattern(self) -> str:
        return max(PATTERNS, key=lambda p: self.arms[p].sample(self.rng))

    def decide(self, d: Decision, r: Reading, resting_hr: float | None = None) -> Support:
        if not self.cfg.enabled:
            return Support(NONE, reason="pulses turned off")
        target = d.action == SPEAK and d.state in self.cfg.target_states
        unsure = d.action == ASK and any(s in self.cfg.target_states for s in d.options)
        if not (target or (unsure and self.cfg.offer_when_unsure)):
            return Support(NONE, reason="not tense, or not sure enough")
        gate = self._gates(r)
        if gate:
            return Support(NONE, reason=gate)
        if unsure:
            return Support(OFFER, pattern="tap", screen_text="Want a calm minute?",
                           reason="tense is possible but not certain: offer, don't impose")
        sid = self._n
        self._n += 1
        if self.rng.random() < self.cfg.hold_out:
            self._open[sid] = {"pattern": None}
            return Support(NONE, reason="eligible, held out at random to measure the effect", held_out=True,
                           support_id=sid)
        p = self._pattern()
        rest = resting_hr or 65.0
        rate = rest * self.cfg.heartbeat_ratio if p == "slow_heartbeat" else self.cfg.breaths_per_minute
        self.by_day[r.timestamp.date().isoformat()] = self.by_day.get(r.timestamp.date().isoformat(), 0) + 1
        self.last = r.timestamp.timestamp()
        self._open[sid] = {"pattern": p}
        text = ("Breathe with the pulse: in as it rises, out as it fades." if p == "breathing"
                else "Feel the slow beat on your wrist. Let your breath follow it.")
        return Support(PULSE, pattern=p, rate_per_minute=round(rate, 1), minutes=self.cfg.minutes,
                       screen_text=text if self.cfg.screen else None,
                       voice_text="Take a moment. Breathe slowly with me." if self.cfg.voice else None,
                       reason="sure the person is tense, against their own baseline", support_id=sid)

    def record_outcome(self, support_id: int, hrv_before: float, hrv_after: float,
                       hr_before: float | None = None, hr_after: float | None = None,
                       felt_better: bool | None = None) -> None:
        """Recovery after the moment: HRV up and heart rate down are both counted; an optional one-tap
        "did it help?" adds to it."""
        item = self._open.pop(support_id, None)
        if item is None:
            return
        rec = (hrv_after - hrv_before) / 10.0
        if hr_before is not None and hr_after is not None:
            rec += (hr_before - hr_after) / 10.0
        if felt_better is not None:
            rec += 0.5 if felt_better else -0.5
        (self.held if item["pattern"] is None else self.arms[item["pattern"]]).add(rec)

    def effect_report(self) -> dict:
        """Effect of each pattern = its mean recovery minus the recovery of held-out moments."""
        base = self.held.mean if self.held.n else float("nan")
        return {"held_out": {"n": self.held.n, "recovery": base},
                **{p: {"n": a.n, "recovery": a.mean, "effect": a.mean - base if self.held.n else float("nan")}
                   for p, a in self.arms.items()}}
