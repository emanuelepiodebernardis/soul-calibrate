"""Reflection layer: sun sign, moon phase and approximate moon sign.

Nightlet's product includes astrology as a reflection layer. These features are offered to the
pattern finder (patterns.py) exactly like any other context, so that a person can see whether a
pattern holds *in their own data*. They never enter the measured reading (engine.py), and a pattern
is only shown as supported if it survives multiple-testing correction and replicates on later data.

Accuracy: the moon phase is computed from the mean synodic month (error well under a day); the moon's
longitude uses a short series (error about 1-2 degrees), so a moon sign within ~2 degrees of a sign
boundary may be wrong. Good enough for a reflection feature, not for an ephemeris.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timezone

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

# (month, day) on which each sign starts, tropical zodiac
_SUN_STARTS = [((3, 21), "Aries"), ((4, 20), "Taurus"), ((5, 21), "Gemini"), ((6, 21), "Cancer"),
               ((7, 23), "Leo"), ((8, 23), "Virgo"), ((9, 23), "Libra"), ((10, 23), "Scorpio"),
               ((11, 22), "Sagittarius"), ((12, 22), "Capricorn"), ((1, 20), "Aquarius"), ((2, 19), "Pisces")]

SYNODIC_MONTH = 29.530588853
_NEW_MOON_EPOCH = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
_J2000 = datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc)
PHASES = ("new moon", "waxing crescent", "first quarter", "waxing gibbous",
          "full moon", "waning gibbous", "last quarter", "waning crescent")


def sun_sign(d: date) -> str:
    md = (d.month, d.day)
    sign = "Capricorn"
    for start, name in sorted(_SUN_STARTS):
        if md >= start:
            sign = name
    return sign


def _utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def moon_age_days(dt: datetime) -> float:
    days = (_utc(dt) - _NEW_MOON_EPOCH).total_seconds() / 86400
    return days % SYNODIC_MONTH


def moon_phase(dt: datetime) -> tuple[str, float]:
    """Phase name and illuminated fraction (0 new, 1 full)."""
    age = moon_age_days(dt)
    frac = age / SYNODIC_MONTH
    illum = (1 - math.cos(2 * math.pi * frac)) / 2
    return PHASES[int((frac * 8 + 0.5) % 8)], illum


def moon_longitude(dt: datetime) -> float:
    d = (_utc(dt) - _J2000).total_seconds() / 86400
    L = 218.316 + 13.176396 * d
    M = math.radians(134.963 + 13.064993 * d)
    return (L + 6.289 * math.sin(M)) % 360


def moon_sign(dt: datetime) -> str:
    return SIGNS[int(moon_longitude(dt) // 30)]


def reflection_factors(dt: datetime, birth: date | None = None) -> dict[str, str]:
    """Categorical reflection features for one moment."""
    phase, _ = moon_phase(dt)
    out = {"moon phase": phase, "moon sign": moon_sign(dt)}
    if birth is not None:
        out["moon in own sun sign"] = "yes" if moon_sign(dt) == sun_sign(birth) else "no"
    return out
