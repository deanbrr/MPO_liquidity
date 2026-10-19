"""Pure rules shared by owner, ledger, priv and H (BUILD_SPEC v1.1 §3.18; BUILD-25).

One copy of the owner instalment rule and of the intra-quarter cash-flow profiles, so P, H and the T4′ replica
cannot drift apart (ADR-02).

The profile table is a timing convention, not a calibrated number, and §2 and §4.0 place it here ("the
intra-quarter profiles exist once, in contracts.rules"), so it is code rather than config (§1.11). ARCH §4.0 says
only that the fixed profile "spreads calls and distributions over months" and is admissible only while error-ledger
row A1 passes. The other choices are WP-01's, recorded as a deviation for WP-13 and WP-17 to confirm:

- every flow spreads evenly over months 3t, 3t+1 and 3t+2, except
- ``DEBT_DRAW`` lands in the first month: a draw is decided at the quarter-start policy instant (§1.3 step 1);
- ``SALE_PROCEEDS`` lands in the last month: discretionary and planned sales settle with a lag (recourse proceeds
  are booked by the ledger itself after the quoted lag, S-ADR-29), and late cash is the prudent liquidity reading;
- ``DEBT_REPAY`` lands in the last month: scheduled repayments fall at the quarter end;
- ``OWNER_DRAW`` lands in the last month: the instalment falls at month 3t + 2 (§1.3).
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.enums import Clock, FlowType
from adic_tpa.contracts.errors import SchemaError, UnitError

__all__ = ["instalment_bn", "intra_quarter_profile", "DRAW_FLOOR_A", "DRAW_CAP_A"]

# The owner's mandate band (5-10% of the opening-FY reported NAV a year; context §1, ARCH §4.3). Mandate terms,
# not calibrated numbers; the defaults of instalment_bn's keyword arguments.
DRAW_FLOOR_A: Final = 0.05
DRAW_CAP_A: Final = 0.10

_EVEN: Final = (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
_FIRST: Final = (1.0, 0.0, 0.0)
_LAST: Final = (0.0, 0.0, 1.0)
# Quarterly-clock flows (module docstring): even spread, except draws first and proceeds, repayments and the owner
# instalment last.
_QUARTERLY_PROFILE: Final[Mapping[FlowType, tuple[float, float, float]]] = MappingProxyType({
    ft: (_FIRST if ft is FlowType.DEBT_DRAW
         else _LAST if ft in (FlowType.SALE_PROCEEDS, FlowType.DEBT_REPAY, FlowType.OWNER_DRAW)
         else _EVEN)
    for ft in FlowType
})


def instalment_bn(draw_rate: F64, basis_bn: F64, instalments_left: int, paid_ytd_bn: F64,
                  *, floor_rate: float = DRAW_FLOOR_A, cap_rate: float = DRAW_CAP_A) -> F64:
    """Owner instalment for the current quarter (§1.3, §4.8; QUANT-25). Returns ≤ 0 (an outflow, §1.4).

    The annual payout is the owner call ``draw_rate × B_y`` clipped to [floor, cap] × B_y (the floor is an
    annual floor, never applied per instalment); each instalment is the remaining annual amount ÷ instalments
    left, so a mid-year override that lifts the rate to the cap re-spreads only what remains.

    Units: ``draw_rate`` decimal a year [P]; ``basis_bn`` B_y, USD bn [P]; ``paid_ytd_bn`` USD bn already paid this
    fiscal year, a non-negative magnitude [P]; result USD bn [P].
    """
    if instalments_left < 1:
        raise SchemaError(f"instalments_left must be >= 1, got {instalments_left}")
    rate = np.asarray(draw_rate, dtype=np.float64)
    basis = np.asarray(basis_bn, dtype=np.float64)
    paid = np.asarray(paid_ytd_bn, dtype=np.float64)
    if (basis < 0).any() or (paid < 0).any():
        raise UnitError("basis_bn and paid_ytd_bn are non-negative magnitudes (§1.4)")
    if not (np.isfinite(rate).all() and np.isfinite(basis).all() and np.isfinite(paid).all()):
        raise UnitError("instalment_bn: non-finite input")
    annual = np.clip(rate, floor_rate, cap_rate) * basis
    remaining = np.maximum(annual - paid, 0.0)
    return -(remaining / float(instalments_left))


def intra_quarter_profile(flow_type: FlowType, clock: Clock) -> F64:
    """Month weights [3] (summing to 1) that spread one quarterly flow over months 3t, 3t+1, 3t+2.

    Only quarterly-clock flows are spread; monthly engines emit monthly flows, so ``Clock.MONTHLY`` raises
    ``SchemaError``. A1 governs whether the fixed profile is admissible (ARCH §4.0).
    """
    if clock is not Clock.QUARTERLY:
        raise SchemaError(f"intra_quarter_profile applies to quarterly flows only, got clock {clock.value}")
    return np.array(_QUARTERLY_PROFILE[FlowType(flow_type)], dtype=np.float64)
