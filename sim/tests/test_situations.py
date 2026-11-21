"""Tests for the recurring-situations experiment."""

from __future__ import annotations

import numpy as np

from soul_calibrate.situations import Memory, SituationConfig, answer, exp_life_change, exp_situations


def test_memory_moves_the_reading_toward_the_answer():
    mem = Memory(bandwidth=1.0, reliability=0.9)
    x = np.zeros(4)
    logp = np.log(np.array([0.4, 0.4, 0.1, 0.1]))
    mem.add(x, 1)
    p_same = mem.adjust(logp, x)
    p_far = mem.adjust(logp, x + 10.0)
    assert p_same.argmax() == 1
    assert np.isclose(p_far, np.exp(logp) / np.exp(logp).sum()).all()


def test_closed_answer_stays_inside_the_offered_options():
    cfg = SituationConfig(closed_error=0.5)
    rng = np.random.default_rng(0)
    offered = np.array([True, True, False, False])
    answers = {answer(0, offered, cfg, rng) for _ in range(200)}
    assert answers <= {0, 1}


def test_questions_improve_the_same_situation():
    res = exp_situations(seed=0, n_people=20, qtypes=("closed",))
    amb = res["ambiguous/closed"]
    assert amb["same_situation_after"] > amb["same_situation_without_questions"] + 0.2
    assert amb["test_accuracy"] > res["never"]["test_accuracy"] + 0.2


def test_no_questions_means_no_change():
    res = exp_situations(seed=1, n_people=10, qtypes=("closed",))
    assert res["never"]["questions_per_person"] == 0.0
    assert res["never"]["other_situations"] == res["never"]["other_situations_without_questions"]


def test_life_change_reports_every_variant():
    res = exp_life_change(seed=0, n_people=8, visibility=0.5)
    assert "answers never fade" in res and "+ user corrections (30% of wrong readings)" in res
    for v in res.values():
        assert 0.0 <= v["changed_first_week"] <= 1.0 and v["interactions_per_person"] > 0
