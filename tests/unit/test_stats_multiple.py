"""Holm and α-investing mechanics (BUILD_SPEC v1.1 §4.4, §7.7). Owner WP-02.

Error-rate control on synthetic null campaigns is in tests/statistical/test_multiple_testing.py. SYNTHETIC p-values.
"""

from __future__ import annotations

import math

import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import AlphaInvesting, holm


def test_holm_step_down() -> None:
    # sorted: 0.005 <= .05/4, 0.01 <= .05/3, 0.03 > .05/2 -> stop
    assert holm([0.01, 0.04, 0.03, 0.005], 0.05) == (True, False, False, True)
    assert holm([0.01, 0.011, 0.012], 0.05) == (True, True, True)
    assert holm([0.02, 0.001], 0.05) == (True, True)
    assert holm([0.026, 0.001], 0.05) == (True, True)       # second step at α/1
    assert holm([0.06, 0.001], 0.05) == (False, True)
    assert holm([0.03, 0.026], 0.05) == (False, False)      # first step at α/2 = 0.025 fails
    assert holm([], 0.05) == ()


def test_holm_stops_at_the_first_acceptance() -> None:
    # 0.0125 = .05/4 rejected, then 0.0170 > .05/3 stops even though 0.024 <= .05/2
    assert holm([0.0125, 0.0170, 0.024, 0.9], 0.05) == (True, False, False, False)


def test_holm_validation() -> None:
    with pytest.raises(SchemaError):
        holm([0.1, 1.2], 0.05)
    with pytest.raises(SchemaError):
        holm([0.1, math.nan], 0.05)
    with pytest.raises(SchemaError):
        holm([0.1], 0.0)


def test_alpha_investing_levels_and_wealth() -> None:
    ai = AlphaInvesting()
    assert (ai.wealth, ai.alpha, ai.eta) == (0.05, 0.05, 1.0)
    assert ai.level == pytest.approx(0.005 / 1.005)
    assert AlphaInvesting(decay=0.0).level == pytest.approx(0.05 / 1.05)      # research all-in form, 0.0476
    for k in range(1, 6):
        assert not ai.test(0.5)
        assert ai.wealth == pytest.approx(0.05 * 0.9 ** k)
    before = ai.wealth
    assert ai.test(0.0)
    assert ai.wealth == pytest.approx(before + 0.05)
    assert (ai.n_tests, ai.n_rejections) == (6, 1)


def test_rejection_threshold_is_the_level() -> None:
    ai = AlphaInvesting()
    assert ai.test(ai.level)
    ai2 = AlphaInvesting()
    assert not ai2.test(ai2.level * (1 + 1e-12))


def test_escalation_threshold_is_crossed_after_22_null_tests() -> None:
    ai = AlphaInvesting()
    for _ in range(21):
        ai.test(1.0)
    assert ai.wealth >= 0.005
    ai.test(1.0)
    assert ai.wealth < 0.005                                   # the lab escalates below 0.005 (§7.7)


def test_all_in_rule_dies_after_one_acceptance() -> None:
    ai = AlphaInvesting(decay=0.0)
    assert not ai.test(0.9)
    assert ai.wealth == pytest.approx(0.0, abs=1e-18) and ai.level == pytest.approx(0.0, abs=1e-18)
    assert not ai.test(0.0)                                    # no wealth, no test


@pytest.mark.parametrize("kwargs", [{"w0": 0.0}, {"payout": 0.0}, {"payout": 1.0}, {"decay": 1.0},
                                    {"decay": -0.1}, {"w0": math.inf}])
def test_alpha_investing_validation(kwargs: dict) -> None:
    with pytest.raises(SchemaError):
        AlphaInvesting(**kwargs)
    with pytest.raises(SchemaError):
        AlphaInvesting().test(1.5)
