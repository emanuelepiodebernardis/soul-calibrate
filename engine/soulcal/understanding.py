"""Understanding layer: help the person understand their own states, only where it is needed (docs/30).

The reading says *what* state the person is probably in. The understanding layer helps the person put it into
words, notice it in their body and see their own patterns. It is dosed by need:

* ``monitor`` (default): the person who is doing well gets one short weekly reflection and nothing more;
* ``support``: the person who shows sustained distress, or who struggles to tell their negative states apart,
  gets one reflective prompt on the days that call for it: a finer word for the state, their own body mirror
  (the voice-and-body signature), a question built from their situations;
* ``bridge``: on top of support, when distress lasts, the prompt points towards a person (a friend, a
  professional), never towards more time in the app.

The level is decided by :class:`NeedGate` from what the system already sees: the share of readings in negative
states, and how often the person's answers swap two negative states that the reading separates confidently
(a proxy of low emotional granularity). A symbolic *lens* (seasons, weather, zodiac) can frame a prompt, but the
content always comes from the person's own data, never predicts, and never changes the reading.
"""
from __future__ import annotations

from dataclasses import dataclass, field

NEGATIVE = ("tense", "low")
POSITIVE = ("calm", "energized")

FINER = {  # a finer word to offer, from the coarse state (coarse to fine, docs/25)
    "tense": ["worried", "frustrated", "overwhelmed", "restless"],
    "low": ["sad", "tired", "lonely", "flat"],
    "calm": ["content", "relaxed", "settled"],
    "energized": ["excited", "motivated", "playful"],
}

LENSES = {
    None: "{q}",
    "weather": "If today were weather inside you, {q}",
    "seasons": "Some days feel like late autumn. {q}",
    "zodiac": "Your chart talks about how you take things to heart; not as a forecast, as a mirror: {q}",
}


@dataclass
class NeedGate:
    """Decides the level of the understanding layer from the readings and answers of the last window."""

    window_days: int = 14
    distress_share: float = 0.35      # share of readings in negative states that calls for support
    confusion_share: float = 0.30     # share of negative answers that swap tense and low against a confident reading
    min_negative_answers: int = 4
    bridge_days: int = 10             # consecutive days with a mostly negative reading that call for a person
    hysteresis: float = 0.8           # step down only below 80% of a threshold
    level: str = "monitor"
    _readings: list = field(default_factory=list)    # (day, state)
    _answers: list = field(default_factory=list)     # (day, read_state, answer, confident)
    _neg_days: int = 0

    def observe(self, day: int, state: str) -> None:
        self._readings.append((day, state))

    def answer(self, day: int, read_state: str, answer: str, confident: bool) -> None:
        self._answers.append((day, read_state, answer, confident))

    def end_of_day(self, day: int) -> None:
        today = [s for d, s in self._readings if d == day]
        if today and sum(s in NEGATIVE for s in today) / len(today) > 0.5:
            self._neg_days += 1
        else:
            self._neg_days = 0

    def scores(self, day: int) -> dict:
        lo = day - self.window_days
        rs = [s for d, s in self._readings if d > lo]
        dist = sum(s in NEGATIVE for s in rs) / len(rs) if rs else 0.0
        neg = [(r, a) for d, r, a, c in self._answers if d > lo and c and r in NEGATIVE and a in NEGATIVE]
        conf = sum(r != a for r, a in neg) / len(neg) if len(neg) >= self.min_negative_answers else None
        return {"distress": dist, "confusion": conf, "negative_days_in_a_row": self._neg_days}

    def decide(self, day: int) -> str:
        s = self.scores(day)
        k = self.hysteresis if self.level != "monitor" else 1.0
        need = s["distress"] >= self.distress_share * k or (s["confusion"] is not None and s["confusion"] >= self.confusion_share * k)
        self.level = "support" if need else "monitor"
        if need and s["negative_days_in_a_row"] >= self.bridge_days:
            self.level = "bridge"
        return self.level


def granularity_index(answers: list[tuple[str, str]]) -> float | None:
    """1 - share of negative answers that swap tense and low against a confident reading (higher = finer)."""
    neg = [(r, a) for r, a in answers if r in NEGATIVE and a in NEGATIVE]
    return None if not neg else 1 - sum(r != a for r, a in neg) / len(neg)


def prompt(level: str, state: str, *, situation: str | None = None, body: list[tuple[str, float]] | None = None,
           lens: str | None = None, weekly: bool = False) -> dict | None:
    """One reflective prompt, or None. Always a question, never a forecast; the lens only frames it."""
    if level == "monitor" and not weekly:
        return None
    if weekly:
        q = "what moment this week felt most like you, and which felt least?"
        kind = "weekly_story"
    elif level == "bridge":
        q = "the last days have been heavy. Is there someone you would like to tell how you feel?"
        kind = "bridge"
    elif body:
        name, change = body[0]
        q = f"when you feel {state}, your {name} changes ({change:+.1f}). Do you notice it in your body right now?"
        kind = "body_mirror"
    elif situation:
        q = f"this often happens {situation}. What is it about that moment?"
        kind = "reflect"
    else:
        q = f"which word is closest: {', '.join(FINER.get(state, [state]))}?"
        kind = "vocabulary"
    text = LENSES.get(lens, "{q}").format(q=q)
    return {"kind": kind, "text": text[0].upper() + text[1:], "lens": lens}


# --------------------------------------------------------------------------- helping a person who does not know
# what they feel (docs/30 section 6). Do not ask for a name they do not have: ask what it is like, show the body
# first, and let the system put the state together; learn from each answer as much as it can be trusted.

SCAFFOLD = [
    ("valence", "Right now, is it more pleasant or more unpleasant?", ["pleasant", "unpleasant", "not sure"]),
    ("energy", "Is there a lot of energy in you, or little?", ["a lot", "little", "not sure"]),
    ("body", "Where do you feel it most?", ["chest", "stomach", "throat", "head", "arms and legs", "nowhere"]),
]

BODY_HINT = {"chest": "tense", "throat": "tense", "stomach": "tense", "arms and legs": "energized",
             "head": None, "nowhere": None}


def body_first(signature_difference: list[tuple[str, float]], top: int = 2) -> str:
    """What the bracelet and the voice show, said before the question, so the answer starts from the body."""
    if not signature_difference:
        return "Take a breath and notice your body for a moment."
    parts = [f"your {n} is {'higher' if v > 0 else 'lower'} than usual" for n, v in signature_difference[:top]]
    return "Right now " + " and ".join(parts) + "."


def compose(valence: str | None, energy: str | None) -> list[str]:
    """The states compatible with the two easy answers ('not sure' keeps both options open)."""
    vs = {"pleasant": ["calm", "energized"], "unpleasant": ["tense", "low"]}.get(valence, ["calm", "energized", "tense", "low"])
    es = {"a lot": ["energized", "tense"], "little": ["calm", "low"]}.get(energy, ["calm", "energized", "tense", "low"])
    return [s for s in vs if s in es]


@dataclass
class AnswerReliability:
    """How much to trust this person's answers, learned from them (a one-person, Dawid-Skene-like estimate).

    Each time the reading was confident and the person answered, record whether they agreed. The weight of a
    new answer falls when the person often swaps states the reading separates well, and rises as they learn."""

    prior_agree: float = 8.0
    prior_disagree: float = 2.0
    agree: float = 0.0
    disagree: float = 0.0

    def record(self, read_state: str, answer: str, confident: bool) -> None:
        if not confident:
            return
        if answer == read_state:
            self.agree += 1
        else:
            self.disagree += 1

    @property
    def reliability(self) -> float:
        return (self.prior_agree + self.agree) / (self.prior_agree + self.prior_disagree + self.agree + self.disagree)

    def weight(self, read_state: str, answer: str, confident: bool) -> float:
        """Weight of one answer for learning: full when it agrees or the reading is unsure, lower otherwise."""
        if not confident or answer == read_state:
            return 1.0
        r = self.reliability
        return max(0.0, 2 * r - 1)
