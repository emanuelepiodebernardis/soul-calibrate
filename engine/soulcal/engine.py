"""SoulEngine: one person's SOUL-Calibrate loop, meant to run on the phone.

    engine = SoulEngine(Profile("u1"))
    decision = engine.observe(reading)              # speak / ask / quiet, with the options to offer
    engine.answer(decision.reading_index, "tense")  # the user's answer to a question
    engine.correct(decision.reading_index, "low")   # a one-tap "not quite" on a spoken reading
    engine.save("u1.json")                          # all state is a small JSON file kept on the device

Steps for every reading
    1. read every signal against the person's baseline (baseline.py);
    2. fuse the channels with the personal head, then add the situation memory's evidence (model.py);
    3. turn the probabilities into a conformal set of plausible states, with this person's adaptive
       threshold shift (adaptive conformal inference: a miss widens the sets, a hit narrows them);
    4. measure how much the words disagree with the expression (face, voice), against the person's own
       usual disagreement: a high personal z-score never yields a confident reading;
    5. decide: one plausible state -> speak; two or three (or a disagreement) -> ask with those states,
       within a daily question budget; otherwise stay quiet.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .anchors import DEFAULT_POPULATION, SignatureModel
from .baseline import EMA, PersonalBaseline
from .model import FusionHead, SituationMemory, context_vector, feature_vector
from .schema import N_STATES, STATES, Decision, Profile, Reading

SPEAK, ASK, QUIET = "speak", "ask", "quiet"


@dataclass
class EngineConfig:
    alpha: float = 0.10                       # conformal miscoverage: sets hold the true state ~90% of the time
    thresholds: list[float] = field(default_factory=lambda: [0.80] * N_STATES)  # population calibration (see calibrate_thresholds)
    aci_step: float = 0.05                    # adaptive conformal step on the person's own answers
    max_questions_per_day: float = 1          # below 1 = one question every few days (0.5 = every other day)
    question_hours: tuple | None = None       # the user's chosen window, e.g. (18, 23); None = any time
    max_options: int = 3
    ask_wide: bool = False                    # also ask when more states are plausible, offering the most likely ones (docs/24)
    incongruence_z: float = 2.0               # personal z-score above which words and expression disagree
    incongruence_min: float = 0.15            # and the raw disagreement (Jensen-Shannon, bits) above this
    memory_bandwidth: float = 0.3
    closed_answer_weight: float = 1.0
    correction_weight: float = 0.8
    head_lr: float = 0.05
    head_shrink: float = 0.05
    ask_needs_expression: bool = True         # quality gate: never ask from body signals alone
    note_weight: float = 0.7                  # weight of a free note read on the phone into a state
    personal: bool = True                     # False = today's generic reading: population norms, no personal correction
    signature: bool = True                    # use the person's voice-and-body signature in the voice channel (docs/29)
    signature_weight: float = 1.0             # weight of the signature's evidence in the voice channel
    signature_temperature: float = 4.0        # >1 softens the signature's evidence to the scale of the other channels
    signature_replaces_voice: bool = True     # the signature replaces the generic voice reading (both read the same voice)
    signature_min_enrollment: int = 3         # neutral readings of the fixed sentence before the signature is used
    signature_has_body: bool = True           # the signature already holds the body: drop the body's z-scores then
    signature_learns_from_answers: bool = True   # answered voice notes also become tagged readings (docs/29)


# Personalization speed presets the user can pick (docs/23-question-budget.md)
PRESETS = {"light": 0.5, "standard": 1, "fast": 2}


# Population norms used only when personal=False (a generic, non-personal reading)
POPULATION_NORMS = {"heart_rate": (72.0, 11.0), "hrv_rmssd": (42.0, 16.0), "skin_temp": (33.5, 0.9), "motion": (0.3, 0.4)}


def calibrate_thresholds(proba: np.ndarray, labels: np.ndarray, alpha: float = 0.10) -> list[float]:
    """Class-conditional split-conformal thresholds on 1 - p(true state), from labelled population data."""
    out = []
    for k in range(N_STATES):
        s = np.sort(1.0 - proba[labels == k, k])
        if len(s) == 0:
            out.append(0.8)
            continue
        level = min(1.0, np.ceil((len(s) + 1) * (1 - alpha)) / len(s))
        out.append(float(np.quantile(s, level, method="higher")))
    return out


def _js_bits(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p + q)
    def kl(a, b):
        return float(np.sum(a * (np.log2(np.maximum(a, 1e-9)) - np.log2(np.maximum(b, 1e-9)))))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def _softmax(z: np.ndarray) -> np.ndarray:
    e = np.exp(z - z.max())
    return e / e.sum()


class SoulEngine:
    def __init__(self, profile: Profile, config: EngineConfig | None = None):
        self.profile = profile
        self.cfg = config or EngineConfig()
        self.baseline = PersonalBaseline()
        self.head = FusionHead(self.cfg.head_lr, self.cfg.head_shrink)
        self.memory = SituationMemory(bandwidth=self.cfg.memory_bandwidth)
        self.incongruence = EMA(0.05)
        self.delta = 0.0                       # personal shift of the conformal thresholds
        self.questions_by_day: dict[str, int] = {}
        self.first_day: str | None = None
        self._pending: dict[int, dict] = {}    # recent readings that can still be answered or corrected
        self.n_readings = 0
        self.drift_events = 0
        self.signature: SignatureModel | None = None

    # ------------------------------------------------------------------ voice-and-body signature (docs/29)
    def _sig(self, x) -> SignatureModel:
        if self.signature is None:
            n = len(x)
            pop = DEFAULT_POPULATION if n == DEFAULT_POPULATION.shape[1] else np.zeros((N_STATES, n))
            self.signature = SignatureModel(n_features=n, population=pop)
        return self.signature

    def enroll(self, features) -> None:
        """The fixed sentence read in a normal tone (first week): the person's usual voice and body."""
        self._sig(features).add_enrollment(np.asarray(features, float))

    def anchor(self, features) -> None:
        """Today's 5-second reading of the fixed sentence: today's microphone, room and day."""
        self._sig(features).set_anchor(np.asarray(features, float))

    def tag(self, state: str, features) -> None:
        """The fixed sentence read while the person says how they feel: their own signature of that state."""
        if state not in STATES:
            raise ValueError(f"unknown state {state!r}; expected one of {STATES}")
        self._sig(features).add_tagged(state, np.asarray(features, float))

    def signature_difference(self, state: str, names: list[str] | None = None) -> list[tuple[str, float]]:
        """What changes in this person in ``state``, largest first: what the app can show them."""
        if self.signature is None:
            return []
        from .anchors import DEFAULT_FEATURES
        names = names or (DEFAULT_FEATURES if self.signature.n_features == len(DEFAULT_FEATURES)
                          else [f"feature {i}" for i in range(self.signature.n_features)])
        return self.signature.difference(state, names)

    def _use_signature(self, r: Reading) -> bool:
        return (self.cfg.signature and self.cfg.personal and r.voice_features is not None
                and self.signature is not None and self.signature.ready(self.cfg.signature_min_enrollment)
                and len(r.voice_features) == self.signature.n_features)

    # ------------------------------------------------------------------------------------------
    def _features(self, r: Reading):
        if self.cfg.personal:
            logits = self.baseline.channel_logits(r)
            z = self.baseline.physio_z(r)
        else:
            logits = {c: np.log(np.maximum([r.channel(c)[s] for s in STATES], 1e-4)) - np.log(1 / N_STATES)
                      for c in ("face", "voice", "text") if r.channel(c) is not None}
            z = {k: (v - POPULATION_NORMS[k][0]) / POPULATION_NORMS[k][1] for k, v in r.physio().items()}
        if self._use_signature(r):
            sig = self.signature.proba(np.asarray(r.voice_features, float))
            lp = np.log(np.maximum([sig[s] for s in STATES], 1e-9)) / self.cfg.signature_temperature
            sig_logits = self.cfg.signature_weight * (lp - lp.mean())
            logits = dict(logits)
            if "voice" in logits and not self.cfg.signature_replaces_voice:
                logits["voice"] = logits["voice"] + sig_logits
            else:
                logits["voice"] = sig_logits
            if self.cfg.signature_has_body:
                z = {k: v for k, v in z.items() if k == "motion"}   # the body is already in the signature
        f = feature_vector(logits, z)
        ctx = context_vector(r.timestamp.hour + r.timestamp.minute / 60, r.timestamp.weekday())
        return f, self.memory.key(_softmax(self.head.logits(f)), ctx), logits

    def _incongruence(self, f: np.ndarray) -> tuple[float | None, list[str]]:
        """Words vs everything else the person shows (face, voice, body), each as weighted by the head."""
        contrib = self.head.contributions(f)
        expressive = [c for c in ("face", "voice", "body") if c in contrib]
        if "text" not in contrib or not expressive:
            return None, []
        words = _softmax(contrib["text"])
        expr = _softmax(np.sum([contrib[c] for c in expressive], axis=0))
        js = _js_bits(words, expr)
        z = self.incongruence.z(js) if self.incongruence.n >= 10 else 0.0
        self.incongruence.update(js)
        pair = [STATES[int(words.argmax())], STATES[int(expr.argmax())]]
        if z >= self.cfg.incongruence_z and js >= self.cfg.incongruence_min and pair[0] != pair[1]:
            return z, pair
        return z, []

    def observe(self, r: Reading) -> Decision:
        f, key, logits = self._features(r)
        scores = self.head.logits(f) + self.memory.evidence(key)
        proba = _softmax(scores)
        thr = np.clip(np.array(self.cfg.thresholds) + self.delta, 0.0, 1.0)
        in_set = (1.0 - proba) <= thr
        if not in_set.any():
            in_set[int(proba.argmax())] = True
        order = [int(k) for k in np.argsort(-proba) if in_set[k]]
        inc_z, inc_pair = self._incongruence(f)

        day = r.timestamp.date().isoformat()
        budget_left = self.questions_by_day.get(day, 0) < self._allowance(r)
        if self.cfg.question_hours is not None:
            start, end = self.cfg.question_hours
            if not start <= r.timestamp.hour < end:
                budget_left = False   # outside the times the user chose for questions
        if self.cfg.ask_needs_expression and not (any(r.channel(c) is not None for c in ("face", "voice", "text"))
                                                  or self._use_signature(r)):
            budget_left = False   # nothing the person said or showed: a question would be a guess
        if inc_pair and budget_left:
            action, options = ASK, inc_pair
            reason = "your words and your expression disagree more than usual for you"
        elif len(order) == 1 and not inc_pair:
            action, options, reason = SPEAK, [], "one plausible state"
        elif 2 <= len(order) <= self.cfg.max_options and budget_left:
            action, options = ASK, [STATES[k] for k in order]
            reason = f"{len(order)} plausible states"
        elif self.cfg.ask_wide and len(order) > self.cfg.max_options and budget_left:
            action, options = ASK, [STATES[k] for k in order[:self.cfg.max_options]]
            reason = f"{len(order)} plausible states: the {self.cfg.max_options} most likely offered"
        else:
            action, options = QUIET, []
            reason = "too uncertain" if len(order) > self.cfg.max_options else "question budget used today"
        if action == ASK:
            self.questions_by_day[day] = self.questions_by_day.get(day, 0) + 1

        idx = self.n_readings
        self.n_readings += 1
        self._pending[idx] = {"f": f, "key": key, "set": in_set.copy(),
                              "vf": list(r.voice_features) if r.voice_features is not None else None}
        if len(self._pending) > 50:
            self._pending.pop(min(self._pending))
        if self.baseline.update(r):
            self.drift_events += 1

        contrib = {c: {s: float(v[k]) for k, s in enumerate(STATES)} for c, v in self.head.contributions(f).items()}
        if self.memory.keys:
            ev = self.memory.evidence(key)
            if np.any(ev):
                contrib["memory"] = {s: float(ev[k]) for k, s in enumerate(STATES)}
        return Decision(action=action, state=STATES[order[0]] if action == SPEAK else None, options=options,
                        proba={s: float(proba[k]) for k, s in enumerate(STATES)}, contributions=contrib,
                        incongruence=inc_z, reason=reason, reading_index=idx)

    def _allowance(self, r: Reading) -> int:
        """Questions allowed today; a budget below 1 a day becomes one question every few days."""
        b = self.cfg.max_questions_per_day
        if b >= 1:
            return int(b)
        from datetime import date
        if self.first_day is None:
            self.first_day = r.timestamp.date().isoformat()
        d = (r.timestamp.date() - date.fromisoformat(self.first_day)).days
        return int(np.floor((d + 1) * b)) - int(np.floor(d * b))

    def _learn(self, index: int, state: str, weight: float) -> None:
        item = self._pending.get(index)
        if item is None:
            raise KeyError(f"reading {index} is too old to be answered")
        k = STATES.index(state)
        self.head.update(item["f"], k, weight)
        self.memory.add(item["key"], k)
        if (self.cfg.signature_learns_from_answers and item.get("vf") is not None and self.signature is not None
                and self.signature.ready(self.cfg.signature_min_enrollment)):
            self.signature.add_tagged(state, np.asarray(item["vf"], float))
        miss = 0.0 if item["set"][k] else 1.0
        self.delta += self.cfg.aci_step * (miss - self.cfg.alpha)

    def answer(self, index: int, state: str) -> None:
        """The user's answer to a question about reading ``index``."""
        self._learn(index, state, self.cfg.closed_answer_weight)

    def correct(self, index: int, state: str) -> None:
        """A one-tap "not quite" on a spoken reading, with the state the user names."""
        self._learn(index, state, self.cfg.correction_weight)

    def note(self, index: int, state: str) -> None:
        """A free note the user left about a reading ("I trained this morning", "I got angry about...").
        The text is read on the phone by any text model into a state; only that state is learned here,
        and nothing leaves the device. Notes do not use the question budget."""
        self._learn(index, state, self.cfg.note_weight)

    def channel_trust(self) -> dict[str, float]:
        return self.head.channel_trust()

    # ------------------------------------------------------------------------------------------
    def save(self, path: str | Path) -> None:
        state = {"profile": {"user_id": self.profile.user_id,
                             "birth_date": self.profile.birth_date.isoformat() if self.profile.birth_date else None,
                             "consent_level": self.profile.consent_level},
                 "config": self.cfg.__dict__, "baseline": self.baseline.to_dict(), "head": self.head.to_dict(),
                 "memory": self.memory.to_dict(), "incongruence": self.incongruence.to_dict(),
                 "delta": self.delta, "questions_by_day": self.questions_by_day, "first_day": self.first_day,
                 "n_readings": self.n_readings, "drift_events": self.drift_events,
                 "signature": self.signature.to_dict() if self.signature is not None else None}
        Path(path).write_text(json.dumps(state), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "SoulEngine":
        from datetime import date
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        p = d["profile"]
        prof = Profile(p["user_id"], date.fromisoformat(p["birth_date"]) if p["birth_date"] else None, p["consent_level"])
        e = cls(prof, EngineConfig(**d["config"]))
        e.baseline = PersonalBaseline.from_dict(d["baseline"])
        e.head = FusionHead.from_dict(d["head"])
        e.memory = SituationMemory.from_dict(d["memory"])
        e.incongruence = EMA.from_dict(d["incongruence"])
        e.delta, e.questions_by_day = d["delta"], d["questions_by_day"]
        e.first_day = d.get("first_day")
        if isinstance(e.cfg.question_hours, list):
            e.cfg.question_hours = tuple(e.cfg.question_hours)
        e.n_readings, e.drift_events = d["n_readings"], d["drift_events"]
        if d.get("signature"):
            e.signature = SignatureModel.from_dict(d["signature"])
        return e
