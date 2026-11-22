"""Tests for the soulcal engine."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np

from soulcal import EngineConfig, Profile, Reading, SoulEngine, basic_emotions_to_states, read_csv, write_csv
from soulcal.astro import moon_phase, sun_sign
from soulcal.baseline import PersonalBaseline
from soulcal.patterns import _bh, _fisher_two_sided, find_patterns
from soulcal.run import run_stream
from soulcal.synthetic import generate

T0 = datetime(2026, 9, 7, 19, 0)


def test_basic_emotions_map_to_four_states():
    p = basic_emotions_to_states({"angry": 0.7, "sad": 0.3})
    assert abs(sum(p.values()) - 1) < 1e-9 and p["tense"] > p["low"] > 0


def test_baseline_removes_a_personal_expression_bias():
    b = PersonalBaseline()
    serious = {"calm": 0.1, "energized": 0.1, "tense": 0.7, "low": 0.1}
    for i in range(30):
        b.update(Reading("u", T0 + timedelta(hours=i), face=serious))
    logits = b.channel_logits(Reading("u", T0, face=serious))
    assert np.allclose(logits["face"], 0.0, atol=0.15)   # a usual face says nothing new


def test_missing_channels_are_skipped():
    eng = SoulEngine(Profile("u"))
    d = eng.observe(Reading("u", T0, heart_rate=70))
    assert d.action in ("speak", "ask", "quiet") and abs(sum(d.proba.values()) - 1) < 1e-9


def test_question_budget_is_respected():
    eng = SoulEngine(Profile("u"), EngineConfig(max_questions_per_day=1, thresholds=[0.99] * 4))
    flat = {"calm": 0.3, "energized": 0.3, "tense": 0.2, "low": 0.2}
    actions = [eng.observe(Reading("u", T0 + timedelta(minutes=10 * i), voice=flat)).action for i in range(5)]
    assert actions.count("ask") <= 1


def test_answers_change_the_next_reading_of_the_same_situation():
    eng = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.95] * 4))
    flat = {"calm": 0.3, "energized": 0.2, "tense": 0.3, "low": 0.2}
    before = eng.observe(Reading("u", T0, voice=flat))
    for k in range(4):
        d = eng.observe(Reading("u", T0 + timedelta(days=7 * (k + 1)), voice=flat))
        eng.answer(d.reading_index, "tense")
    after = eng.observe(Reading("u", T0 + timedelta(days=35), voice=flat))
    assert after.proba["tense"] > before.proba["tense"]


def test_save_and_load_keep_the_state(tmp_path):
    readings, truth, _ = generate(days=7, seed=1)
    res = run_stream(readings, truth, Profile("u"), EngineConfig())
    res.engine.save(tmp_path / "s.json")
    eng = SoulEngine.load(tmp_path / "s.json")
    r = readings[-1]
    assert np.isclose(eng.observe(r).proba["calm"], res.engine.observe(r).proba["calm"])


def test_csv_round_trip(tmp_path):
    readings, _, _ = generate(days=2, seed=2)
    write_csv(readings, tmp_path / "r.csv")
    back = read_csv(tmp_path / "r.csv")
    assert len(back) == len(readings) and back[0].timestamp == readings[0].timestamp


def test_full_loop_beats_todays_generic_reading():
    acc = {}
    for name, cfg, learn in (("generic", EngineConfig(personal=False, max_questions_per_day=0), False),
                             ("loop", EngineConfig(), True)):
        last = []
        for sd in range(6):
            readings, truth, _ = generate(days=42, seed=sd)
            res = run_stream(readings, truth, Profile("u"), cfg, learn=learn, seed=sd)
            last.append(np.mean([w["accuracy"] for w in res.weekly[-2:]]))
        acc[name] = np.mean(last)
    assert acc["loop"] > acc["generic"] + 0.1


def test_astro_reference_dates():
    assert sun_sign(date(1990, 5, 17)) == "Taurus" and sun_sign(date(1990, 1, 5)) == "Capricorn"
    assert moon_phase(datetime(2024, 1, 25, 18))[0] == "full moon"      # full moon of 25 January 2024
    assert moon_phase(datetime(2024, 1, 11, 12))[0] == "new moon"       # new moon of 11 January 2024


def test_statistics_helpers():
    assert _fisher_two_sided(10, 0, 0, 10) < 0.001 and _fisher_two_sided(5, 5, 5, 5) > 0.99
    q = _bh([0.01, 0.04, 0.03, 0.5])
    assert all(a >= b for a, b in zip(q, [0.01, 0.04, 0.03, 0.5]))


def test_pattern_finder_supports_planted_patterns_and_not_the_moon():
    readings, truth, _ = generate(days=56, seed=3)
    links = find_patterns(readings, truth)
    supported = [lk for lk in links if lk.status == "supported"]
    assert supported, "the planted routine should produce supported links"
    assert not [lk for lk in supported if lk.layer == "reflection"], "no moon effect is planted"


def test_soul_bench_ladder_runs_and_full_loop_beats_generic():
    from soulcal.bench import soul_bench
    readings, truth, _ = generate(days=42, seed=4)
    res = soul_bench(readings, truth)
    assert set(res) >= {"B0 user's own average", "B4 all channels, generic", "B6 full loop"}
    assert res["B6 full loop"]["accuracy_last_weeks"] > res["B4 all channels, generic"]["accuracy_last_weeks"]


def test_no_question_from_body_signals_alone():
    eng = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.99] * 4))
    d = eng.observe(Reading("u", T0, heart_rate=90, hrv_rmssd=20))
    assert d.action != "ask"


def test_user_chosen_hours_and_light_budget():
    flat = {"calm": 0.45, "energized": 0.45, "tense": 0.05, "low": 0.05}   # two plausible states
    eng = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.7] * 4, question_hours=(18, 23)))
    morning = eng.observe(Reading("u", T0.replace(hour=9), voice=flat))
    evening = eng.observe(Reading("u", T0.replace(hour=20), voice=flat))
    assert morning.action != "ask" and evening.action == "ask"
    light = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.7] * 4, max_questions_per_day=0.5))
    asks = [light.observe(Reading("u", T0 + timedelta(days=d), voice=flat)).action == "ask" for d in range(4)]
    assert asks == [False, True, False, True]   # one question every other day


def test_free_note_teaches_like_an_answer():
    eng = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.95] * 4, max_questions_per_day=0))
    flat = {"calm": 0.3, "energized": 0.2, "tense": 0.3, "low": 0.2}
    before = eng.observe(Reading("u", T0, voice=flat))
    for k in range(4):
        d = eng.observe(Reading("u", T0 + timedelta(days=7 * (k + 1)), voice=flat))
        eng.note(d.reading_index, "energized")
    after = eng.observe(Reading("u", T0 + timedelta(days=35), voice=flat))
    assert after.proba["energized"] > before.proba["energized"]


def test_wide_question_offers_the_most_likely_states():
    flat = {"calm": 0.3, "energized": 0.28, "tense": 0.22, "low": 0.2}
    narrow = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.95] * 4))
    wide = SoulEngine(Profile("u"), EngineConfig(thresholds=[0.95] * 4, ask_wide=True))
    assert narrow.observe(Reading("u", T0, voice=flat)).action == "quiet"
    d = wide.observe(Reading("u", T0, voice=flat))
    assert d.action == "ask" and len(d.options) == 3


def test_level_of_detail_shows_main_state_until_fine_is_sure():
    from soulcal.detail import EXAMPLE_PARENT, is_right, level_of_detail
    unsure = {s: 0.0 for s in EXAMPLE_PARENT} | {"calm": 0.45, "content": 0.45, "tired": 0.10}
    d = level_of_detail(unsure, EXAMPLE_PARENT, tau_fine=0.2, tau_coarse=0.2)
    assert (d.level, d.state) == ("coarse", "calm") and is_right(d, "content", EXAMPLE_PARENT)
    sure = {s: 0.0 for s in EXAMPLE_PARENT} | {"content": 0.9, "calm": 0.1}
    assert level_of_detail(sure, EXAMPLE_PARENT).state == "content"
    torn = {s: 0.0 for s in EXAMPLE_PARENT} | {"calm": 0.4, "anxious": 0.35, "tired": 0.25}
    d = level_of_detail(torn, EXAMPLE_PARENT)
    assert d.level == "ask" and set(d.options) == {"calm", "anxious", "tired"}
    assert level_of_detail(torn, EXAMPLE_PARENT, can_ask=False).level == "quiet"


def test_archetype_start_and_no_match_far_away():
    import numpy as np
    from soulcal import archetypes as A
    from soulcal.run import run_stream
    from soulcal.schema import Profile
    from soulcal.synthetic import generate
    rng = np.random.default_rng(0)
    cohort = []
    for name, kind in A.TYPES.items():
        for i in range(3):
            p = A._person(kind, f"{name}-{i}", rng)
            r, y, _ = generate(days=14, seed=i, person=p)
            cohort.append((r[:12], run_stream(r, y, Profile(p.user_id), seed=i).engine))
    model = A.fit(cohort, k=3, radius_margin=5.0)   # small cohort: wider radius
    assert sum(a.members for a in model.archetypes) == 9
    r, _, _ = generate(days=4, seed=99, person=A._person(A.TYPES["masks with words"], "new", rng))
    eng, k = model.start_engine(Profile("new"), r)
    assert k is not None and np.allclose(eng.head.W, model.archetypes[k].W)
    far = A.signature(r) + 100 * model.scale
    assert model.match(far)[0] is None


def test_pulse_only_when_sure_of_tension_and_never_while_moving():
    from datetime import datetime
    from soulcal.schema import Decision, Reading
    from soulcal.support import NONE, OFFER, PULSE, SupportConfig, SupportPolicy
    sp = SupportPolicy(SupportConfig(hold_out=0.0))
    ts = datetime(2026, 9, 7, 19, 0)
    still = Reading("u", ts, heart_rate=80.0, motion=0.2)
    tense = Decision(action="speak", state="tense", options=[], proba={})
    s = sp.decide(tense, still, resting_hr=60.0)
    assert s.action == PULSE and s.screen_text and s.voice_text is None
    if s.pattern == "slow_heartbeat":
        assert s.rate_per_minute == 48.0            # 80% of the resting heart rate
    assert sp.decide(tense, Reading("u", ts.replace(hour=20), heart_rate=80.0, motion=0.2)).reason == "cooldown"
    sp2 = SupportPolicy(SupportConfig(hold_out=0.0))
    assert sp2.decide(tense, Reading("u", ts, heart_rate=120.0, motion=1.6)).action == NONE      # gym
    assert sp2.decide(Decision("speak", "energized", [], {}), still).action == NONE             # excitement
    assert sp2.decide(Decision("ask", None, ["tense", "energized"], {}), still).action == OFFER
    sp2.record_outcome(0, 40.0, 50.0)                                                            # unknown id: ignored
