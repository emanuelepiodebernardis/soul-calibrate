"""Data model: one reading from the device, the user's profile and the decision SOUL-Calibrate returns.

A reading can carry any subset of channels. Missing channels are simply left out of the fusion.

CSV columns accepted by :func:`read_csv` (all optional except ``user_id`` and ``timestamp``)::

    user_id, timestamp (ISO 8601),
    face_calm, face_energized, face_tense, face_low        probabilities from any facial expression model
    voice_calm, voice_energized, voice_tense, voice_low    probabilities from any speech emotion model
    text_calm, text_energized, text_tense, text_low        probabilities from any text model or LLM
    heart_rate (bpm), hrv_rmssd (ms), skin_temp (°C), motion (any activity index)
    self_report                                            the user's own label, when there is one

If a model outputs the seven basic emotions instead, use :func:`basic_emotions_to_states`.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

STATES = ("calm", "energized", "tense", "low")
N_STATES = len(STATES)
CHANNELS = ("face", "voice", "text")
PHYSIO = ("heart_rate", "hrv_rmssd", "skin_temp", "motion")

# How the seven basic emotions of common facial / speech models spread over the four states
# (valence x arousal quadrants). A starting point, to be replaced by a mapping learned per product.
_BASIC_TO_STATES = {
    "happy": {"energized": 0.6, "calm": 0.4},
    "neutral": {"calm": 0.7, "low": 0.3},
    "surprise": {"energized": 0.6, "tense": 0.4},
    "angry": {"tense": 1.0},
    "fear": {"tense": 1.0},
    "disgust": {"tense": 0.7, "low": 0.3},
    "sad": {"low": 1.0},
}


def basic_emotions_to_states(scores: dict[str, float]) -> dict[str, float]:
    """Map probabilities over the seven basic emotions onto the four states."""
    out = {s: 0.0 for s in STATES}
    for emotion, p in scores.items():
        for state, w in _BASIC_TO_STATES.get(emotion.lower(), {}).items():
            out[state] += p * w
    total = sum(out.values()) or 1.0
    return {s: v / total for s, v in out.items()}


@dataclass
class Reading:
    user_id: str
    timestamp: datetime
    face: dict[str, float] | None = None
    voice: dict[str, float] | None = None
    text: dict[str, float] | None = None
    heart_rate: float | None = None
    hrv_rmssd: float | None = None
    skin_temp: float | None = None
    motion: float | None = None
    self_report: str | None = None

    def channel(self, name: str) -> dict[str, float] | None:
        return getattr(self, name)

    def physio(self) -> dict[str, float]:
        return {k: getattr(self, k) for k in PHYSIO if getattr(self, k) is not None}


@dataclass
class Profile:
    user_id: str
    birth_date: date | None = None          # only used by the optional reflection (astrology) layer
    consent_level: int = 0                  # 0: everything stays on the device (see docs/15)


@dataclass
class Decision:
    action: str                             # "speak" | "ask" | "quiet"
    state: str | None                       # the state spoken, when action == "speak"
    options: list[str]                      # the states offered, when action == "ask"
    proba: dict[str, float]
    contributions: dict[str, dict[str, float]] = field(default_factory=dict)  # per channel, log-evidence per state
    incongruence: float | None = None       # personal z-score of words vs expression disagreement
    reason: str = ""
    reading_index: int = -1


def _probs(row: dict[str, str], prefix: str) -> dict[str, float] | None:
    vals = {s: row.get(f"{prefix}_{s}", "") for s in STATES}
    if not any(v.strip() for v in vals.values()):
        return None
    out = {s: float(v) if v.strip() else 0.0 for s, v in vals.items()}
    total = sum(out.values()) or 1.0
    return {s: v / total for s, v in out.items()}


def _num(row: dict[str, str], key: str) -> float | None:
    v = (row.get(key) or "").strip()
    return float(v) if v else None


def read_csv(path: str | Path) -> list[Reading]:
    """Load readings from a CSV file with the columns described in the module docstring."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            report = (row.get("self_report") or "").strip() or None
            if report is not None and report not in STATES:
                raise ValueError(f"unknown self_report {report!r}; expected one of {STATES}")
            out.append(Reading(
                user_id=row["user_id"], timestamp=datetime.fromisoformat(row["timestamp"]),
                face=_probs(row, "face"), voice=_probs(row, "voice"), text=_probs(row, "text"),
                heart_rate=_num(row, "heart_rate"), hrv_rmssd=_num(row, "hrv_rmssd"),
                skin_temp=_num(row, "skin_temp"), motion=_num(row, "motion"), self_report=report,
            ))
    out.sort(key=lambda r: (r.user_id, r.timestamp))
    return out


def write_csv(readings: list[Reading], path: str | Path) -> None:
    cols = ["user_id", "timestamp"] + [f"{c}_{s}" for c in CHANNELS for s in STATES] + list(PHYSIO) + ["self_report"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in readings:
            row = [r.user_id, r.timestamp.isoformat()]
            for c in CHANNELS:
                p = r.channel(c)
                row += [f"{p[s]:.4f}" if p else "" for s in STATES]
            row += ["" if getattr(r, k) is None else f"{getattr(r, k):.3f}" for k in PHYSIO]
            row.append(r.self_report or "")
            w.writerow(row)
