"""The mFDR table (BUILD_SPEC v1.1 S-ADR-18, §7.7): fixed parameters, one wealth sequence across contracts, the
rejection rule, and exact replay of the online p-values. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.registry import Registry


def test_configure_once(reg: Registry) -> None:
    ledger = reg.mfdr()
    assert ledger.config() is None and ledger.state().wealth is None
    with pytest.raises(SchemaError, match="not configured"):
        ledger.wealth()
    cfg = ledger.configure(w0=0.05, payout=0.05, decay=0.9)
    assert ledger.configure(w0=0.05, payout=0.05, decay=0.9) == cfg == ledger.config()
    with pytest.raises(SchemaError, match="fixed across contracts"):
        ledger.configure(w0=0.10, payout=0.05, decay=0.9)
    with pytest.raises(SchemaError, match="invalid mFDR parameters"):
        reg.mfdr().configure(w0=0.0, payout=0.05, decay=0.9)
    assert ledger.wealth() == 0.05


def test_tests_form_one_wealth_sequence_across_contracts(reg: Registry) -> None:
    ledger = reg.mfdr()
    with pytest.raises(SchemaError, match="configure"):
        ledger.record(contract_id="ctr-2026Q4-v1", hypothesis_id="h1", p_value=0.2, alpha_level=0.01,
                      rejected=False, wealth_after=0.04)
    ledger.configure(w0=0.05, payout=0.05, decay=0.9)
    ledger.record(contract_id="ctr-2026Q4-v1", hypothesis_id="h1", p_value=0.20, alpha_level=0.010,
                  rejected=False, wealth_after=0.0400, campaign_id="cmp-2026Q4-1", family_size=3)
    ledger.record(contract_id="ctr-2026Q4-v1", hypothesis_id="h2", p_value=0.001, alpha_level=0.008,
                  rejected=True, wealth_after=0.0850)
    ledger.record(contract_id="ctr-2027Q1-v1", hypothesis_id="h1", p_value=0.5, alpha_level=0.02,
                  rejected=False, wealth_after=0.0630)
    rows = ledger.rows()
    assert [r.wealth_before for r in rows] == [0.05, 0.04, 0.085]
    assert [r.seq for r in rows] == sorted(r.seq for r in rows)
    assert rows[0].family_size == 3 and rows[0].campaign_id == "cmp-2026Q4-1"
    assert ledger.p_values() == (0.20, 0.001, 0.5)
    assert ledger.wealth() == 0.063
    state = ledger.state()
    assert (state.n_tests, state.n_rejections, state.wealth) == (3, 1, 0.063)
    assert state.contracts == ("ctr-2026Q4-v1", "ctr-2027Q1-v1")
    assert [r.hypothesis_id for r in ledger.rows(contract_id="ctr-2027Q1-v1")] == ["h1"]
    assert reg.verify_chain().ok


@pytest.mark.parametrize("kwargs, match", [
    (dict(p_value=0.001, alpha_level=0.01, rejected=False, wealth_after=0.04), "rejects exactly"),
    (dict(p_value=0.5, alpha_level=0.01, rejected=True, wealth_after=0.04), "rejects exactly"),
    (dict(p_value=1.5, alpha_level=0.01, rejected=False, wealth_after=0.04), "probabilities"),
    (dict(p_value=0.5, alpha_level=0.01, rejected=False, wealth_after=-0.01), "never negative"),
    (dict(p_value=float("nan"), alpha_level=0.01, rejected=False, wealth_after=0.04), "finite"),
])
def test_invalid_tests_are_refused(reg: Registry, kwargs: dict, match: str) -> None:
    ledger = reg.mfdr()
    ledger.configure(w0=0.05, payout=0.05, decay=0.9)
    with pytest.raises(SchemaError, match=match):
        ledger.record(contract_id="ctr-2026Q4-v1", hypothesis_id="h1", **kwargs)
    assert ledger.rows() == []
