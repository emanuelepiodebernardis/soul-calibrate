import numpy as np

from soul_calibrate import conformal as cf
from soul_calibrate.data import SimConfig, make_population, state_from_affect
from soul_calibrate.experiments import Protocol, exp_cohort, exp_conformal, exp_drift, exp_ladder
from soul_calibrate.models import PersonalHead, RollingBaseline, rolling_transform

SMALL = Protocol(n_train=20, n_calib=8, n_test=10)


def test_states_cover_the_four_quadrants():
    v = np.array([1.0, 1.0, -1.0, -1.0])
    a = np.array([-1.0, 1.0, 1.0, -1.0])
    assert state_from_affect(v, a).tolist() == [0, 1, 2, 3]


def test_population_is_reproducible():
    a = make_population(3, SimConfig(), seed=7)
    b = make_population(3, SimConfig(), seed=7)
    assert np.allclose(a[0].X, b[0].X)


def test_fixed_baseline_does_not_move():
    X = np.random.default_rng(0).normal(size=(30, 4))
    Z = rolling_transform(X, n_enroll=10, alpha=0.0)
    b = RollingBaseline(X[:10])
    assert np.allclose(Z[20], b.transform(X[20]))


def test_personal_head_falls_back_to_population_without_answers():
    logp = np.log(np.full((5, 4), 0.25))
    head = PersonalHead()
    head.fit(logp[:2], np.array([0, 1]))
    assert np.allclose(head.predict_proba(logp), 0.25)


def test_prediction_sets_are_never_empty():
    proba = np.array([[0.97, 0.01, 0.01, 0.01], [0.25, 0.25, 0.25, 0.25]])
    sets = cf.prediction_sets(proba, np.zeros(4))
    assert sets.any(axis=1).all()


def test_decision_rule():
    assert cf.decide(np.array([1, 0, 0, 0], bool)) == cf.SPEAK
    assert cf.decide(np.array([1, 1, 0, 0], bool)) == cf.ASK
    assert cf.decide(np.array([1, 1, 1, 1], bool)) == cf.QUIET


def test_conformal_coverage_is_near_target():
    r = exp_conformal(0, SimConfig(), SMALL)
    assert r["per_state_coverage"] > 0.8


def test_personal_baseline_beats_generic_model():
    r = exp_ladder(0, SimConfig(), Protocol(), budgets=(0, 40))
    assert r["baseline"] > r["generic"]
    assert r["personal_40"] > r["baseline"]


def test_rolling_baseline_recovers_from_a_step_change():
    r = exp_drift(0, SimConfig(), Protocol())
    assert r["rolling_baseline"] > r["fixed_baseline"]


def test_cohort_answers_help_users_who_are_never_asked():
    r = exp_cohort(0, SimConfig(), Protocol(), cohort_sizes=(50,))
    assert r["plus_cohort_50"] > r["today_generic"]
    assert r["full_loop_20_answers"] > r["plus_cohort_50"]
