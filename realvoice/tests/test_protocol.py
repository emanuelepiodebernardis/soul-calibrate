"""The E31 protocol on synthetic features: no audio, no model download."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from e31_real_voice import evaluate  # noqa: E402


def _data(seed=0, speakers=10, per_class=12, dim=16, offset=3.0, signal=1.0):
    """Each speaker has a large personal offset (who is speaking) and a small emotion signal."""
    rng = np.random.default_rng(seed)
    proto = rng.normal(0, signal, (4, dim))
    X, y, spk = [], [], []
    for s in range(speakers):
        off = rng.normal(0, offset, dim)
        for c in range(4):
            for _ in range(per_class):
                X.append(off + proto[c] + rng.normal(0, 1.0, dim))
                y.append(c)
                spk.append(f"s{s}")
    return np.array(X), np.array(y), np.array(spk)


def test_personal_baseline_and_answers_help_when_the_speaker_dominates():
    X, y, spk = _data()
    m = evaluate(X, y, spk, seed=0)["mean"]
    assert m["+ personal baseline"]["accuracy"] > m["generic"]["accuracy"] + 0.05
    assert m["+ 16 answers"]["accuracy"] >= m["+ personal baseline"]["accuracy"] - 0.02


def test_zero_shot_scores_are_used_when_given():
    X, y, spk = _data(speakers=4)
    Z = np.eye(4)[y] * 0.6 + 0.1
    m = evaluate(X, y, spk, Z=Z, seed=0, ks=(2,))["mean"]
    assert m["zero-shot"]["accuracy"] == 1.0


def test_signature_from_neutral_and_tagged_clips():
    """The fixed-sentence signature: neutral clips as enrollment, a few tagged clips per state."""
    X, y, spk = _data()
    m = evaluate(X, y, spk, seed=0, ks=(2,), neutral=(y == 0))["mean"]
    assert m["+ signature (neutral sentences)"]["accuracy"] > m["generic"]["accuracy"]
    assert m["+ signature, 4 tagged per state"]["accuracy"] >= m["+ signature (neutral sentences)"]["accuracy"] - 0.02
