"""Level of detail per reading: say what you know, at the level you know it (docs/25).

Works on top of any model that outputs probabilities over fine states (for example Nightlet's own labels)
when each fine state belongs to a main state. The reading is shown at the finest level the model is sure of:

* one plausible fine state                 -> show the fine state ("you seem content")
* otherwise one plausible main state       -> show the main state ("you seem calm")
* otherwise two or three plausible states  -> ask, offering them
* otherwise                                -> stay quiet

Questions should always be asked about fine states: the simulation shows that coarse answers slow learning,
while choosing the level of detail per reading keeps readings right from the first days without slowing it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# An example hierarchy: the engine's four main states, each with two finer states.
EXAMPLE_PARENT = {
    "calm": "calm", "content": "calm",
    "energized": "energized", "excited": "energized",
    "tense": "tense", "anxious": "tense",
    "low": "low", "tired": "low",
}


@dataclass
class Detail:
    level: str                       # "fine" | "coarse" | "ask" | "quiet"
    state: str | None = None         # the state shown, at that level
    options: list[str] = field(default_factory=list)
    fine_set: list[str] = field(default_factory=list)
    coarse_set: list[str] = field(default_factory=list)


def coarse_proba(proba: dict[str, float], parent: dict[str, str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for s, p in proba.items():
        out[parent[s]] = out.get(parent[s], 0.0) + p
    return out


def _set(proba: dict[str, float], tau: float) -> list[str]:
    """States whose probability reaches tau (a split-conformal threshold), most likely first; never empty."""
    order = sorted(proba, key=proba.get, reverse=True)
    kept = [s for s in order if proba[s] >= tau]
    return kept or order[:1]


def calibrate_tau(proba: np.ndarray, labels: np.ndarray, alpha: float = 0.10) -> float:
    """Split-conformal threshold: sets {p >= tau} hold the true state about 1 - alpha of the time."""
    p_true = proba[np.arange(len(labels)), labels]
    n = len(p_true)
    q = np.floor(alpha * (n + 1)) / n
    return float(np.quantile(p_true, min(max(q, 0.0), 1.0), method="lower"))


def level_of_detail(proba: dict[str, float], parent: dict[str, str], tau_fine: float = 0.2,
                    tau_coarse: float = 0.2, max_options: int = 3, can_ask: bool = True) -> Detail:
    fine = _set(proba, tau_fine)
    coarse = _set(coarse_proba(proba, parent), tau_coarse)
    if len(fine) == 1:
        return Detail("fine", fine[0], fine_set=fine, coarse_set=coarse)
    if len(coarse) == 1:
        return Detail("coarse", coarse[0], fine_set=fine, coarse_set=coarse)
    if can_ask and len(fine) <= max_options:
        return Detail("ask", options=fine, fine_set=fine, coarse_set=coarse)
    if can_ask and len(coarse) <= max_options:
        # too many fine states: offer the most likely fine state of each plausible main state
        opts = [max((s for s in proba if parent[s] == c), key=proba.get) for c in coarse]
        return Detail("ask", options=opts, fine_set=fine, coarse_set=coarse)
    return Detail("quiet", fine_set=fine, coarse_set=coarse)


def is_right(detail: Detail, truth: str, parent: dict[str, str]) -> bool | None:
    """Shown precision: right at the level shown (a main state is right for any of its fine states)."""
    if detail.level == "fine":
        return detail.state == truth
    if detail.level == "coarse":
        return detail.state == parent[truth]
    return None
