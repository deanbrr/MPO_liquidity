"""Fixture H reproduces the gap_02 research outcomes (BUILD_SPEC v1.1 §4.5, §5.8–§5.10; BUILD-21; owner WP-03).

The expected values come from the ported ``phase1_demo_results.json`` (via ``tests/regression/fixtures/gap02/
coefs.json``): Phase-I u*, contract mode, restored x, sells, objective, duals and the reservation price
hold/(1 + y_cash) in research Mode B and Mode H for the three readings. SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.enums import ConsentScenario, ContractMode, PricedOn, RowRole
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.testing import fixture_h, fixture_tree
from adic_tpa.testing.fixture_h import (
    IG_ROW, LEVERS, READINGS, T4_ROW, build_fixture_lp, fixture_phase1, gap02_coefs,
)

CASES = [(r, mode_h) for r in READINGS for mode_h in (False, True)]
# The research's STRUCT/EXEC verdicts: canonical restorable in both modes; as written structural without the band;
# the critic reading structural in both (gap_02 §3).
MODES = {("canonical", False): ContractMode.EXECUTION_RECOVERY, ("canonical", True): ContractMode.EXECUTION_RECOVERY,
         ("as_written", False): ContractMode.STRUCTURAL_RECOVERY, ("as_written", True): ContractMode.EXECUTION_RECOVERY,
         ("critic", False): ContractMode.STRUCTURAL_RECOVERY, ("critic", True): ContractMode.STRUCTURAL_RECOVERY}


def _expected(reading: str, mode_h: bool) -> dict:
    return gap02_coefs()["readings"][reading]["expected"]["modeH" if mode_h else "modeB"]


@pytest.fixture(scope="module")
def solved() -> dict:
    return {case: fixture_h(*case[:1], mode_h=case[1]) for case in CASES}


@pytest.mark.parametrize("case", CASES, ids=[f"{r}-{'H' if h else 'B'}" for r, h in CASES])
def test_phase1_reproduces_research_u_star_and_mode(case: tuple[str, bool]) -> None:
    reading, mode_h = case
    p1, glide = fixture_phase1(reading, mode_h=mode_h)
    exp = _expected(reading, mode_h)["phase1"]
    scen = ConsentScenario.R2 if mode_h else ConsentScenario.R1
    t4 = p1.by_scenario[scen][0]
    assert p1.pricing_scenario is scen and p1.mode is MODES[case]
    assert t4.u_star_bn == pytest.approx(exp["u_S_star"], abs=1e-9)
    assert p1.by_scenario[scen][1].u_star_bn == pytest.approx(exp["u_IG_star"], abs=1e-9)
    if t4.u_star_bn > 0:                                       # IIS names the T4' row and every lever at cap
        research = {s.removeprefix("cap:") for s in exp["iis"] if s.startswith("cap:")}
        assert t4.iis[0] == str(T4_ROW) and set(t4.levers_at_cap) == research
    assert p1.recovery_hash == glide.recovery_hash == content_hash(glide.model_dump(exclude={"recovery_hash"}))
    assert glide.g_bn[0] == pytest.approx(t4.u_star_bn if t4.u_star_bn > 0 else p1.d0_bn) and glide.g_bn[-1] == 0.0


def test_phase1_scenarios_are_nested() -> None:
    p1, _ = fixture_phase1("critic")
    u = [p1.by_scenario[s][0].u_star_bn for s in (ConsentScenario.R0X, ConsentScenario.R0, ConsentScenario.R1,
                                                   ConsentScenario.R2)]
    assert all(a >= b - 1e-9 for a, b in zip(u, u[1:]))           # more consent never worsens the violation


@pytest.mark.parametrize("case", CASES, ids=[f"{r}-{'H' if h else 'B'}" for r, h in CASES])
def test_restored_solution_reproduces_research(case: tuple[str, bool], solved: dict) -> None:
    reading, mode_h = case
    lp, sol, duals, tree = solved[case]
    exp = _expected(reading, mode_h)["restored"]
    w0 = lp.scale_bn
    x_bn = {k: sol.x[j] * (1.0 if k == "band" else w0) for j, k in enumerate(LEVERS)}
    for k in LEVERS:
        assert x_bn[k] == pytest.approx(exp["x"][k], abs=1e-9), k
    assert np.allclose(sol.x[len(LEVERS):] * w0, exp["sell"], atol=1e-9)
    assert sol.objective * w0 == pytest.approx(exp["obj"], abs=1e-9)
    assert duals.pi_row[0] == pytest.approx(exp["duals"]["T4"], abs=1e-9)
    assert duals.pi_row[1] == pytest.approx(exp["duals"]["IG"], abs=1e-9)
    assert sol.priced_on is PricedOn.RESTORED and sol.recovery_hash is not None
    assert tree.tree_hash == lp.meta.tree_hash == fixture_tree().tree_hash


@pytest.mark.parametrize("case", CASES, ids=[f"{r}-{'H' if h else 'B'}" for r, h in CASES])
def test_reservation_price_from_the_cash_shadow(case: tuple[str, bool], solved: dict) -> None:
    """ℓ₀ = M₀/(μ₀ − M₀) is the research card's y_cash; reservation price = hold/(1 + ℓ₀) (§5.8, §5.12)."""
    reading, mode_h = case
    _, _, duals, tree = solved[case]
    card = _expected(reading, mode_h)["restored_cards"][0]
    assert duals.ell[0] == pytest.approx(card["y_cash"], abs=1e-9)
    assert card["hold"] / (1.0 + duals.ell[0]) == pytest.approx(card["reservation_price"], abs=1e-9)
    assert np.array_equal(duals.mu_cash[1:], tree.p[1:]) and not duals.ell[1:].any() and not duals.M_cash[1:].any()


def test_canonical_card_numbers(solved: dict) -> None:
    _, _, duals, _ = solved[("canonical", False)]
    assert duals.ell[0] == pytest.approx(0.082906, abs=1e-6)
    assert 0.95 / (1.0 + duals.ell[0]) == pytest.approx(0.8773, abs=1e-4)


def test_dual_quality_fields(solved: dict) -> None:
    lp, sol, duals, _ = solved[("canonical", False)]
    assert set(duals.quality) == {str(T4_ROW), str(IG_ROW)}
    for i, key in enumerate(lp.row_keys):
        q = duals.quality[str(key)]
        assert q.method == "ranging" and isinstance(q.at_kink, bool) and not q.pinned
        lo, hi = q.one_sided
        assert min(lo, hi) - 1e-6 <= duals.pi_row[i] <= max(lo, hi) + 1e-6   # π lies between the one-sided slopes
    assert sol.resolve_counts == {"finite_difference": 4} and sol.solver.threads == 1


def test_lp_layout_and_validation() -> None:
    lp = build_fixture_lp("canonical")
    lp.validate()
    assert lp.row_keys == (T4_ROW, IG_ROW) and (lp.row_role == RowRole.PRICING).all()
    assert [k.name for k in lp.col_keys] == [*LEVERS, "sell", "sell", "sell"]
    assert lp.scale_bn == 177.0 and not lp.node_of_row.any() and not lp.node_of_col.any()
    assert lp.meta.consent_scenario is ConsentScenario.R1
    assert lp.col_hi[LEVERS.index("band")] == 0.0, "Mode B has no owner band"
    assert build_fixture_lp("canonical", mode_h=True).col_hi[LEVERS.index("band")] == 1.0
    relaxed = build_fixture_lp("canonical", relax_bn=1.77)
    assert relaxed.row_lo[0] == pytest.approx(lp.row_lo[0] - 0.01)
    with pytest.raises(SchemaError):
        build_fixture_lp("unknown")  # type: ignore[arg-type]
