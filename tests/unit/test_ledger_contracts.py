"""Ledger contracts (BUILD_SPEC v1.1 §3.9, §3.17; ARCH §4.9; S-ADR-32): the canonical stress s*(θ) and the ledger
array shapes. Owner WP-01. SYNTHETIC values only."""

from __future__ import annotations

import json

import numpy as np
import pytest

from adic_tpa.contracts.enums import RecourseTier, RowFamily
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.ledger import CanonicalConventions, LedgerPaths, StressReport, StressSpec
from adic_tpa.contracts.optimizer import RowKey

CONVENTIONS = CanonicalConventions.model_validate_json(json.dumps({
    "credit_cash_a": {"PRIVCREDIT": 0.10}, "commitment_split": {"PE": 1.0},
    "real_assets": {"noi_yield_mult": 0.8, "refi_spread_stress_a": 0.02, "refi_ltv_cap": 0.5}}))


@pytest.mark.parametrize(("theta", "equity", "dist", "call"), [
    (0.0, -0.30, 0.45, 1.0),
    (0.58, -0.358, 0.189, 1.29),        # θ* ≈ 0.58 on the research fixture (S-ADR-32)
    (1.0, -0.40, 0.0, 1.5),
])
def test_s_star_goldens(theta: float, equity: float, dist: float, call: float) -> None:
    """s*(θ): equity −(0.30 + 0.10θ); distributions 0.45(1 − θ); calls (1 + 0.5θ) × 28% a year; 24 months."""
    s = StressSpec.s_star(theta, CONVENTIONS)
    assert s.equity_shock == pytest.approx(equity, abs=1e-15)
    assert s.dist_mult == pytest.approx(dist, abs=1e-15)
    assert s.call_mult == pytest.approx(call, abs=1e-15)
    assert (s.base_call_rate_a, s.months, s.role, s.theta) == (0.28, 24, "pricing", theta)
    assert s.conventions == CONVENTIONS and s.name.startswith("s*(")


@pytest.mark.parametrize("theta", [-0.01, 1.01])
def test_s_star_needs_theta_in_unit_interval(theta: float) -> None:
    with pytest.raises(SchemaError, match="theta"):
        StressSpec.s_star(theta, CONVENTIONS)


def _report(survival: int) -> StressReport:
    headroom = np.ones((2, 24))
    return StressReport(spec_hash="sha256:" + "1" * 64, headroom_bn=headroom, nco_bn=np.zeros((2, 24)),
                        cbc_bn={RecourseTier.TP: np.ones((2, 24))},
                        survival_months={RecourseTier.TP: np.full(2, survival, dtype=np.int16)},
                        gap_bn=np.zeros(2), d0_bn=np.zeros(2))


def test_survival_months_lie_in_0_to_25() -> None:
    """25 encodes "> 24 months" (§3.9); nothing larger exists (review R13)."""
    _report(25).validate()
    _report(0).validate()
    with pytest.raises(SchemaError, match=r"\[0.0, 25.0\]"):
        _report(26).validate()


def _paths(months: int) -> LedgerPaths:
    keys = (RowKey(family=RowFamily.T4P, idx=(("h", 7),)), RowKey(family=RowFamily.LR4))
    return LedgerPaths(row_keys=keys, rows=np.zeros((2, months, 2), dtype=np.float32),
                       stages=np.zeros((2, months, 4), dtype=np.int8))


def test_ledger_paths_cover_121_monthly_instants() -> None:
    _paths(121).validate()
    with pytest.raises(SchemaError, match="size 121"):
        _paths(120).validate()
