"""Split conformal prediction sets and the speak / ask / stay-quiet decision.

The prediction set holds every state whose score is within the calibrated
threshold, so that the true state is in the set with probability about 1 - alpha.
The class-conditional (Mondrian) variant calibrates one threshold per state, so
rare states are not under-covered.
"""

from __future__ import annotations

import numpy as np

from .data import N_STATES

SPEAK, ASK, QUIET = "speak", "ask", "quiet"


def _quantile(scores: np.ndarray, alpha: float) -> float:
    n = len(scores)
    if n == 0:
        return 1.0
    level = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(scores, level, method="higher"))


def calibrate(proba: np.ndarray, y: np.ndarray, alpha: float, per_class: bool) -> np.ndarray:
    """Return one threshold per state on the nonconformity score 1 - p(true state)."""
    scores = 1.0 - proba[np.arange(len(y)), y]
    if not per_class:
        return np.full(N_STATES, _quantile(scores, alpha))
    return np.array([_quantile(scores[y == k], alpha) for k in range(N_STATES)])


def prediction_sets(proba: np.ndarray, thresholds: np.ndarray) -> np.ndarray:
    """Boolean matrix: state k is in the set when 1 - p_k <= threshold_k."""
    sets = (1.0 - proba) <= thresholds[None, :]
    empty = ~sets.any(axis=1)
    sets[empty, proba[empty].argmax(axis=1)] = True
    return sets


def decide(set_row: np.ndarray, max_options: int = 3) -> str:
    size = int(set_row.sum())
    if size == 1:
        return SPEAK
    if size <= max_options:
        return ASK
    return QUIET


def coverage(sets: np.ndarray, y: np.ndarray) -> float:
    return float(sets[np.arange(len(y)), y].mean())
