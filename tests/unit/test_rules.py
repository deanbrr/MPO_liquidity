"""contracts.rules (BUILD_SPEC v1.1 §3.18, §4.8; BUILD-25, QUANT-25): each instalment is the remaining annual
amount ÷ instalments left; the 5% floor is annual (never 20%); the 10% cap holds; intra-quarter profiles sum to 1.
Owner WP-01."""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.calendar import Calendar
from adic_tpa.contracts.enums import Clock, FlowType
from adic_tpa.contracts.errors import SchemaError, UnitError
from adic_tpa.contracts.rules import instalment_bn, intra_quarter_profile

B_Y = np.array([177.0])


def pay_year(rate: float, quarters: int = 4) -> list[float]:
    paid, out = 0.0, []
    for left in range(quarters, 0, -1):
        inst = float(instalment_bn(np.array([rate]), B_Y, left, np.array([paid]))[0])
        out.append(inst)
        paid -= inst
    return out


def test_instalment_is_remaining_over_instalments_left() -> None:
    inst = pay_year(0.06)
    assert all(x <= 0 for x in inst)                                  # outflows are negative (§1.4)
    assert np.allclose(inst, [-0.06 * 177.0 / 4] * 4)
    assert abs(sum(inst) + 0.06 * 177.0) < 1e-12


def test_annual_floor_is_five_percent_never_twenty() -> None:
    inst = pay_year(0.02)                                             # owner call below the floor
    assert abs(sum(inst) + 0.05 * 177.0) < 1e-12                      # 5% of B_y a year
    assert abs(sum(inst) + 0.20 * 177.0) > 1.0                        # not 5% per instalment


def test_cap_is_ten_percent() -> None:
    assert abs(sum(pay_year(0.15)) + 0.10 * 177.0) < 1e-12


def test_mid_year_override_respreads_only_the_remainder() -> None:
    paid = 2 * 0.06 * 177.0 / 4                                       # two instalments at 6% already paid
    inst = instalment_bn(np.array([0.10]), B_Y, 2, np.array([paid]))  # override resets the year to 10%
    assert np.allclose(inst, -(0.10 * 177.0 - paid) / 2)
    over = instalment_bn(np.array([0.05]), B_Y, 1, np.array([0.08 * 177.0]))
    assert over[0] == 0.0                                             # never a refund


def test_vectorized_over_paths() -> None:
    rates = np.array([0.02, 0.07, 0.12])
    out = instalment_bn(rates, np.full(3, 100.0), 4, np.zeros(3))
    assert out.shape == (3,) and np.allclose(out, [-1.25, -1.75, -2.5])


def test_fiscal_year_remainder_uses_calendar_instalments() -> None:
    cal = Calendar()
    assert cal.instalments_left(0) == 1                               # FY2026 has one instalment left in horizon
    assert [cal.instalments_left(t) for t in range(1, 5)] == [4, 3, 2, 1]


def test_invalid_inputs() -> None:
    with pytest.raises(SchemaError):
        instalment_bn(np.array([0.06]), B_Y, 0, np.array([0.0]))
    with pytest.raises(UnitError):
        instalment_bn(np.array([0.06]), np.array([-1.0]), 1, np.array([0.0]))
    with pytest.raises(UnitError):
        instalment_bn(np.array([np.nan]), B_Y, 1, np.array([0.0]))


@pytest.mark.parametrize("ft", list(FlowType))
def test_intra_quarter_profiles_sum_to_one(ft: FlowType) -> None:
    w = intra_quarter_profile(ft, Clock.QUARTERLY)
    assert w.shape == (3,) and w.dtype == np.float64 and abs(w.sum() - 1.0) < 1e-15 and (w >= 0).all()


FIRST, LAST, EVEN = (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1 / 3, 1 / 3, 1 / 3)
# The full table (module docstring of contracts.rules; review R09): a change to any row is a contract change.
PROFILES = {ft: EVEN for ft in FlowType} | {
    FlowType.DEBT_DRAW: FIRST, FlowType.SALE_PROCEEDS: LAST, FlowType.DEBT_REPAY: LAST, FlowType.OWNER_DRAW: LAST}


@pytest.mark.parametrize("ft", list(FlowType), ids=lambda ft: ft.name)
def test_every_flow_type_profile_is_pinned(ft: FlowType) -> None:
    assert np.array_equal(intra_quarter_profile(ft, Clock.QUARTERLY), np.array(PROFILES[ft]))


def test_profile_timing() -> None:
    assert np.array_equal(intra_quarter_profile(FlowType.OWNER_DRAW, Clock.QUARTERLY), [0.0, 0.0, 1.0])  # month 3t+2
    assert np.array_equal(intra_quarter_profile(FlowType.DEBT_DRAW, Clock.QUARTERLY), [1.0, 0.0, 0.0])
    assert np.allclose(intra_quarter_profile(FlowType.CALL, Clock.QUARTERLY), 1 / 3)
    assert np.array_equal(intra_quarter_profile(4, Clock.QUARTERLY), [0.0, 0.0, 1.0])   # int code = SALE_PROCEEDS
    with pytest.raises(SchemaError):
        intra_quarter_profile(FlowType.CALL, Clock.MONTHLY)
