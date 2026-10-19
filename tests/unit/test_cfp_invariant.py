"""CFP invariant (BUILD_SPEC v1.1 §3.9, §4.14; ARCH §4.9): the playbook is RED or BLACK only if the event stage is
at least RED (readiness-Red alone never fires the Red playbook). Owner WP-01."""

from __future__ import annotations

import itertools

import numpy as np
import pytest
from pydantic import ValidationError

from adic_tpa.contracts.enums import CFPStage
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.ledger import CFPReading, LedgerState

INDICATORS = {"sh_tp_months": 17.0, "lcr30": 2.1, "treasury_share": 0.077, "liquid_share": 0.308,
              "lar99_over_cbc": 0.65}


def reading(readiness: CFPStage, event: CFPStage, playbook: CFPStage) -> CFPReading:
    return CFPReading(readiness=readiness, event=event, planning=max(readiness, event), playbook=playbook,
                      indicators=INDICATORS, triggers=())


@pytest.mark.parametrize(("event", "playbook"), list(itertools.product(CFPStage, CFPStage)))
def test_playbook_red_requires_event_red(event: CFPStage, playbook: CFPStage) -> None:
    if playbook >= CFPStage.RED and event < CFPStage.RED:
        with pytest.raises(ValidationError, match="event stage"):
            reading(CFPStage.BLACK, event, playbook)
    else:
        assert reading(CFPStage.GREEN, event, playbook).playbook is playbook


def test_readiness_red_with_event_amber_is_an_amber_playbook() -> None:
    """The t0 reading of ARCH §4.9: readiness Red, event Amber → Amber playbook (plus PHASE2_PLAN)."""
    r = reading(CFPStage.RED, CFPStage.AMBER, CFPStage.AMBER)
    assert r.planning is CFPStage.RED


def _ledger_state(event: int, playbook: int, n: int = 3) -> LedgerState:
    z, i8 = np.zeros(n), np.zeros(n, dtype=np.int8)
    return LedgerState(
        m=0, fy=2026, hqla_unenc_bn=z.copy(), treasury_bn=np.zeros((n, 3)), posted_im_bn=z.copy(),
        vm_balance_bn=z.copy(), vm_in_transit_bn=z.copy(), fac_drawn_bn=np.zeros((n, 1)), fac_limit_bn=np.ones((n, 1)),
        asset_debt_bn=z.copy(), unit_debt_bn=z.copy(), encumbrance_bn=z.copy(), nav_econ_bn=np.full(n, 177.0),
        nav_rep_bn=np.full(n, 177.0), liquid_bn=z.copy(), nav_group_econ=np.zeros((n, 2)),
        nav_group_rep=np.zeros((n, 2)), unfunded_group=np.zeros((n, 2)), draw_basis_bn=np.full(n, 177.0),
        draw_rate=np.full(n, 0.058), payout_ytd_bn=z.copy(), twr_index=np.ones(n), twr_peak=np.ones(n),
        cushion=z.copy(), readiness=i8.copy(), event=np.full(n, event, dtype=np.int8), planning=i8.copy(),
        playbook=np.full(n, playbook, dtype=np.int8), event_hist=np.zeros((n, 2), dtype=np.int8),
        red_event=np.zeros(n, dtype=bool), payout_short=np.zeros(n, dtype=bool), failed=np.zeros(n, dtype=bool),
        red_month=np.full(n, -1, dtype=np.int16))


def test_ledger_state_validate_enforces_the_invariant() -> None:
    _ledger_state(CFPStage.RED, CFPStage.RED).validate()
    _ledger_state(CFPStage.AMBER, CFPStage.AMBER).validate()
    with pytest.raises(SchemaError, match="playbook"):
        _ledger_state(CFPStage.AMBER, CFPStage.BLACK).validate()
