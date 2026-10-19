"""Fakes behind the frozen Protocols (BUILD_SPEC v1.1 §4.5, §3.17; owner WP-03). SYNTHETIC – NOT ADIC DATA."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from adic_tpa.contracts import ports
from adic_tpa.contracts.actions import LensAction
from adic_tpa.contracts.claims import MemoDraft
from adic_tpa.contracts.engine_io import ActionSlice
from adic_tpa.contracts.enums import (
    Clock, ConsentScenario, DataClass, FlowType, Lens, MandateMode, ModelFamily, RecourseTier, RoleId, RowFamily,
    SaleReason,
)
from adic_tpa.contracts.errors import ReplayMiss, SchemaError
from adic_tpa.contracts.ledger import StressSpec
from adic_tpa.contracts.policy import RecourseOrder
from adic_tpa.contracts.ports import LLMRequest, PolicyContext, ToolDef
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.tools import Phase1In
from adic_tpa.contracts.world import MisspecOverride
from adic_tpa.testing import (
    EVALUATOR_METHODS, MINI_ASSET_CLASSES, FakeEngineFactory, FakeEvaluator, FakeLedger, FakeLLMBackend, FakePolicy,
    fake_belief_draws, fake_beliefs, fake_draw_block, fake_engines, fake_filter, fake_filter_params, fake_observables,
    fake_owner_draws, merge_outcomes, merge_quotes, mini_book, mini_contract, mini_cube, mini_flowcube,
    mini_owner_config, mini_world, world_slice,
)

P = 40


@pytest.fixture(scope="module")
def setup():
    book = mini_book("v2")
    cube = fake_owner_draws(mini_cube(P))
    beliefs = fake_beliefs(book)
    world = mini_world("M1")
    draws = fake_belief_draws(beliefs, world, P)
    return book, cube, beliefs, world, draws


def _hold(book, t: int) -> ActionSlice:
    tax = GroupRegistry.for_version(book.taxonomy_version)
    return ActionSlice.empty(t, P, len(book.unit_index().unit_ids), len(tax), 3, len(book.facilities))


def _step_quarter(engines, states, cube, book, t, act=None):
    act = act if act is not None else _hold(book, t)
    q_slices, m_slices = [], {}
    for e in engines:
        noise = fake_draw_block(b"\x01" * 16, e.noise_requests(t), np.arange(P))
        if e.clock is Clock.QUARTERLY:
            q_slices.append(e.step(t, states[e.engine_id], world_slice(cube, [3 * t, 3 * t + 1, 3 * t + 2],
                                                                     clock=e.clock, t=t), act, noise))
        else:
            for m in range(3 * t, 3 * t + 3):
                m_slices.setdefault(m, []).append(e.step(m, states[e.engine_id], world_slice(cube, [m], clock=e.clock,
                                                                                            t=m), act, noise))
    return q_slices, m_slices


def _init(setup):
    book, cube, beliefs, world, draws = setup
    engines = fake_engines(book)
    states = {e.engine_id: e.init(book, beliefs, P, draws=draws, world=world) for e in engines}
    return engines, states


# ------------------------------------------------------------------------------------------------ engines
def test_fakes_are_protocol_instances(setup) -> None:
    book = setup[0]
    for e in fake_engines(book):
        assert isinstance(e, ports.AssetEngine)
    assert isinstance(FakeLedger(GroupRegistry.for_version("v2")), ports.Ledger)
    assert isinstance(FakeEngineFactory(mini_owner_config()), ports.EngineFactory)
    assert isinstance(FakeLLMBackend(), ports.LLMBackend)
    assert isinstance(FakeEvaluator(), ports.EvaluatorPort)


def test_engines_cover_every_engine_unit_once(setup) -> None:
    book = setup[0]
    engines = fake_engines(book)
    ids = [u for e in engines for u in e.unit_ids]
    idx = book.unit_index()
    assert sorted(ids) == sorted(u for u, eng in zip(idx.unit_ids, idx.engine_of, strict=True) if eng != "treasury")
    assert {e.engine_id: e.clock for e in engines}["priv.fund"] is Clock.QUARTERLY
    assert {e.engine_id: e.clock for e in engines}["pub.hf"] is Clock.MONTHLY


def test_flow_slices_validate_and_net_intra_flows(setup) -> None:
    engines, states = _init(setup)
    q, m = _step_quarter(engines, states, setup[1], setup[0], 0)
    for fs in q + [s for ms in m.values() for s in ms]:
        fs.validate()
        assert np.abs(fs.intra.astype(np.float64).sum(axis=1)).max() <= 1e-6
    overlay = next(s for s in m[0] if s.engine_id == "overlay")
    assert np.abs(overlay.intra).sum() > 0, "the completion-beta service books an intra-ADIC fee"


def test_hold_steps_reproduce_the_mini_flowcube(setup) -> None:
    book, cube, *_ = setup
    engines, states = _init(setup)
    fc = mini_flowcube(book, cube)
    pos = {str(u): i for i, u in enumerate(fc.meta.unit_ids)}
    for t in range(3):
        q, m = _step_quarter(engines, states, cube, book, t)
        totals: dict[str, np.ndarray] = {}
        for fs in q + [s for ms in m.values() for s in ms]:
            totals[fs.engine_id] = totals.get(fs.engine_id, 0.0) + fs.by_unit.astype(np.float64)
        for e in engines:
            cols = [pos[str(u)] for u in e.unit_ids]
            assert np.allclose(totals[e.engine_id], fc.values[:, t, cols, :].astype(np.float64), rtol=1e-6,
                               atol=1e-6), (e.engine_id, t)


def test_step_rejects_a_wrong_slice(setup) -> None:
    book, cube, *_ = setup
    engines, states = _init(setup)
    fund = next(e for e in engines if e.engine_id == "priv.fund")
    noise = fake_draw_block(b"\x00" * 16, fund.noise_requests(0), np.arange(P))
    with pytest.raises(SchemaError):
        fund.step(0, states[fund.engine_id], world_slice(cube, [0], clock=Clock.QUARTERLY, t=0), _hold(book, 0), noise)
    with pytest.raises(SchemaError):
        fund.step(1, states[fund.engine_id], world_slice(cube, [3, 4, 5], clock=Clock.QUARTERLY, t=1),
                  _hold(book, 1), noise)                                      # noise drawn for quarter 0


def test_init_checks_its_inputs(setup) -> None:
    book, cube, beliefs, world, draws = setup
    e = fake_engines(book)[0]
    with pytest.raises(SchemaError):
        e.init(book, beliefs, P + 1, draws=draws, world=world)
    with pytest.raises(SchemaError):
        e.init(book, beliefs, P, draws=draws, world=mini_world("M6"))


def test_discretionary_sale_books_proceeds_and_shrinks_the_unit(setup) -> None:
    book, cube, *_ = setup
    engines, states = _init(setup)
    fund = next(e for e in engines if e.engine_id == "priv.fund")
    unit = fund.unit_ids[0]
    col = list(book.unit_index().unit_ids).index(unit)
    act = _hold(book, 0)
    act.sell_frac[:, col] = 0.25
    act.sell_reason[:, col] = SaleReason.DISCRETIONARY
    nav0 = states[fund.engine_id].nav[:, 0].copy()
    q, _ = _step_quarter([fund], states, cube, book, 0, act)
    proceeds = q[0].by_unit[:, 0, FlowType.SALE_PROCEEDS].astype(np.float64)
    assert np.allclose(proceeds, 0.25 * nav0 * fund.units[0].normal_bid, rtol=1e-6)


def test_recourse_quotes_cover_red_and_amber_units_only(setup) -> None:
    book, cube, *_ = setup
    engines, states = _init(setup)
    tax = GroupRegistry.for_version("v2")
    quotes = merge_quotes([e.recourse_quotes(0, states[e.engine_id],
                                             world_slice(cube, [0], clock=e.clock, t=0)) for e in engines])
    quotes.validate()
    groups = {str(g) for g in quotes.group_of}
    assert groups <= {str(g) for g in tax.red_tier() + tax.amber_tier()}
    for g, tier in zip(quotes.group_of, quotes.tier, strict=True):
        assert tier == (2 if tax.spec(g).red_tier else 1)


def test_apply_recourse_scales_only_the_sold_units(setup) -> None:
    from adic_tpa.contracts.ledger import RecourseOutcome

    engines, states = _init(setup)
    fund = next(e for e in engines if e.engine_id == "priv.fund")
    st = states[fund.engine_id]
    before = st.nav.copy()
    sold = np.zeros((P, 1), dtype=np.float32)
    sold[:, 0] = 0.2
    outcome = RecourseOutcome(unit_ids=(fund.unit_ids[1],), sold_frac=sold, month=np.full((P, 1), 1, np.int16),
                              proceeds_bn=np.ones((P, 1)), red=np.ones((P, 1), bool),
                              reason=np.full((P, 1), SaleReason.RECOURSE_RED, np.int8))
    fund.apply_recourse(st, outcome)
    assert np.allclose(st.nav[:, 1], 0.8 * before[:, 1]) and np.array_equal(st.nav[:, 0], before[:, 0])


def test_column_flows_lens_rules(setup) -> None:
    book, cube, *_ = setup
    fund = next(e for e in fake_engines(book) if e.engine_id == "priv.fund")
    unit = fund.unit_ids[0]
    group = fund.units[0].group

    def act(lens: Lens, exposure: float, financing: float, cash: float) -> LensAction:
        return LensAction(unit_id=unit, group=group, lens=lens, instrument="x", size_bn=1.0,
                          exposure_delta_bn=exposure, financing_delta_bn=financing, cash_out_bn=cash)

    cubes = {name: fund.column_flows(unit, a, cube) for name, a in {
        "HOLD": act(Lens.HOLD, 0.0, 0.0, 0.0), "SELL": act(Lens.SELL, -1.0, 0.0, 0.85),
        "ADD": act(Lens.ADD, 1.0, 0.0, 0.0), "REFINANCE": act(Lens.REFINANCE, 0.0, 0.5, 0.5),
        "LEVER": act(Lens.LEVER, 1.0, 0.5, 0.0)}.items()}
    for c in cubes.values():
        c.validate()
    assert not cubes["HOLD"].values.any()
    assert cubes["SELL"].values[:, 0, 0, FlowType.SALE_PROCEEDS].min() > 0
    assert cubes["REFINANCE"].values[:, 0, 0, FlowType.DEBT_DRAW].min() == pytest.approx(0.5)
    lever = cubes["LEVER"].values.astype(np.float64)
    assert np.allclose(lever, cubes["ADD"].values.astype(np.float64) + cubes["REFINANCE"].values.astype(np.float64),
                       rtol=1e-6, atol=1e-7)
    with pytest.raises(SchemaError):
        fund.column_flows(unit, LensAction(unit_id=None, group=group, lens=Lens.PACE, instrument="pace", size_bn=1.0,
                                           exposure_delta_bn=0.0, financing_delta_bn=0.0, cash_out_bn=0.0), cube)


# ------------------------------------------------------------------------------------------------- ledger
def _ledger_quarter(setup, ledger, ls, engines, states, t, *, quotes_scale: float = 1.0):
    book, cube, *_ = setup
    q, m = _step_quarter(engines, states, cube, book, t)
    quotes = merge_quotes([e.recourse_quotes(t, states[e.engine_id], world_slice(cube, [3 * t], clock=e.clock,
                                                                               t=3 * t if e.clock is Clock.MONTHLY else t))
                           for e in engines])
    residuals, outcomes = [], []
    for month in range(3 * t, 3 * t + 3):
        flows = q + m.get(month, [])
        draw = ledger.instalment(ls, cube.draw_rate[:, ledger.cal.fy_index(ledger.cal.fiscal_year(t))], month)
        sold = sum((o.sold_frac.astype(np.float64) for o in outcomes), np.zeros((P, len(quotes.unit_ids))))
        scale_out = np.zeros(P)
        pos = {str(u): j for j, u in enumerate(quotes.unit_ids)}
        cash = np.array([FlowType(i).is_cash() for i in range(18)])
        for fs in flows:
            w = ledger.month_weights(fs, month)
            for k, uid in enumerate(fs.recourse_unit_ids):
                scale_out += sold[:, pos[str(uid)]] * (fs.by_recourse_unit[:, k, :].astype(np.float64)[:, cash]
                                                      * w[cash]).sum(axis=1)
        new, outcome = ledger.apply(month, ls, flows, draw, quotes)
        new.validate()
        outcome.validate()
        outcome.check_against(quotes)
        expected = (ls.treasury_bn.sum(axis=1) + ledger.booked_cash(month, flows) - scale_out + draw
                    + outcome.proceeds_bn.sum(axis=1) + new.fac_drawn_bn.sum(axis=1) - ls.fac_drawn_bn.sum(axis=1)
                    + ledger.last["unpaid"] + ledger.last["shortfall"])
        residuals.append(float(np.abs(new.treasury_bn.sum(axis=1) - expected).max()))
        outcomes.append(outcome)
        ls = new
    merged = merge_outcomes(outcomes)
    for e in engines:
        e.apply_recourse(states[e.engine_id], merged)
    return ls, merged, residuals


def test_ledger_identity_is_exact_and_recourse_respects_depth(setup) -> None:
    book = setup[0]
    engines, states = _init(setup)
    ledger = FakeLedger(GroupRegistry.for_version("v2"), book.facilities)
    ls = ledger.init_state(book, P)
    ls.validate()
    assert ls.nav_econ_bn[0] == pytest.approx(177.0) and ls.treasury_bn[0].sum() == pytest.approx(14.7)
    ls = replace(ls, treasury_bn=ls.treasury_bn * np.array([0.05, 0.05, 0.05]))     # force the waterfall
    residuals, any_sale = [], False
    for t in range(4):
        ls, merged, res = _ledger_quarter(setup, ledger, ls, engines, states, t)
        residuals += res
        any_sale |= bool(merged.sold_frac.any())
        assert (merged.sold_frac <= 0.5 + 1e-6).all()
    assert max(residuals) <= 1e-10 and any_sale
    assert ls.fac_drawn_bn.sum(axis=1).max() > 0, "the signed revolver was drawn from month 2"


def test_ledger_waterfall_order_and_red_flags(setup) -> None:
    book = setup[0]
    engines, states = _init(setup)
    ledger = FakeLedger(GroupRegistry.for_version("v2"))                       # no facilities
    ls = ledger.init_state(book, P)
    ls = replace(ls, treasury_bn=np.zeros_like(ls.treasury_bn))
    _, merged, _ = _ledger_quarter(setup, ledger, ls, engines, states, 0)
    tiers = merge_quotes([e.recourse_quotes(0, states[e.engine_id], world_slice(setup[1], [0], clock=e.clock, t=0))
                          for e in engines]).tier
    sold_any = merged.sold_frac.any(axis=0)
    assert sold_any[tiers == 1].all(), "amber units go first"
    assert np.array_equal(merged.red, (merged.sold_frac > 0) & (tiers[None, :] == 2))
    assert set(np.unique(merged.reason[merged.sold_frac > 0])) <= {SaleReason.RECOURSE_AMBER, SaleReason.RECOURSE_RED}


def test_sold_fractions_are_float32_cover_the_need_and_respect_depth() -> None:
    from adic_tpa.testing.fakes import _f32_within

    frac = np.array([1.0 / 3.0, 0.5, 0.7, 0.0, 0.25])
    room = np.array([0.5, 0.5, 0.7000000001, 0.2, 0.0])
    out = _f32_within(frac, room)
    assert np.array_equal(out.astype(np.float32).astype(np.float64), out)       # what RecourseOutcome carries
    assert (out <= room).all()
    assert out[0] >= frac[0] and out[1] == 0.5 and out[3] == 0.0 and out[4] == 0.0
    assert out[2] < frac[2] and out[2] == np.float32(0.7000000001)               # capped: largest float32 ≤ room


def test_ledger_instalment_uses_the_shared_rule(setup) -> None:
    book, cube, *_ = setup
    ledger = FakeLedger(GroupRegistry.for_version("v2"))
    ls = ledger.init_state(book, P)
    assert not ledger.instalment(ls, cube.draw_rate[:, 0], 0).any()
    draw = ledger.instalment(ls, cube.draw_rate[:, 0], 2)                      # FY2026's last instalment
    expected = -(0.075 * 177.0 - 0.75 * 0.058 * 177.0)
    assert np.allclose(draw, expected, rtol=1e-6)


def test_ledger_rejects_wrong_months_and_positive_draws(setup) -> None:
    book = setup[0]
    engines, states = _init(setup)
    ledger = FakeLedger(GroupRegistry.for_version("v2"))
    ls = ledger.init_state(book, P)
    quotes = merge_quotes([e.recourse_quotes(0, states[e.engine_id], world_slice(setup[1], [0], clock=e.clock, t=0))
                           for e in engines])
    with pytest.raises(SchemaError):
        ledger.apply(1, ls, [], np.zeros(P, np.float32), quotes)
    with pytest.raises(SchemaError):
        ledger.apply(0, ls, [], np.ones(P, np.float32), quotes)


def test_ledger_unpaid_instalment_when_everything_is_exhausted(setup) -> None:
    book = setup[0]
    ledger = FakeLedger(GroupRegistry.for_version("v2"))
    ls = ledger.init_state(book, P)
    ls = replace(ls, treasury_bn=np.zeros_like(ls.treasury_bn))
    empty = merge_quotes([fake_engines(book)[0].recourse_quotes(
        0, fake_engines(book)[0].init(book, setup[2], P, draws=setup[4], world=setup[3]),
        world_slice(setup[1], [0], clock=Clock.MONTHLY, t=0))])
    new, _ = ledger.apply(0, ls, [], np.full(P, -1.0, np.float32), empty)   # overlay quotes nothing
    assert new.payout_short.all() and np.allclose(ledger.last["unpaid"], 1.0)
    assert (new.treasury_bn >= 0).all() and not new.failed.any()


def test_ledger_row_slacks_and_stress_replica(setup) -> None:
    book = setup[0]
    ledger = FakeLedger(GroupRegistry.for_version("v2"), book.facilities)
    ls = ledger.init_state(book, P)
    slacks = ledger.row_slacks(ls)
    assert {k.family for k in slacks} == {RowFamily.T2_IG_HARD, RowFamily.T2_IG_TARGET, RowFamily.T5_DEBT}
    assert all(v.dtype == np.float32 and v.shape == (P,) for v in slacks.values())
    rep = ledger.stress_replica(ls, StressSpec.s_star(0.58, mini_contract().tier1.conventions.pricing))
    rep.validate()
    assert set(rep.cbc_bn) == set(RecourseTier)
    tp, tpf = rep.cbc_bn[RecourseTier.TP], rep.cbc_bn[RecourseTier.TPF]
    assert (tpf >= tp - 1e-12).all(), "facility credit only adds capacity"


def test_merge_outcomes_rejects_mismatched_units(setup) -> None:
    from adic_tpa.contracts.ledger import RecourseOutcome

    def outcome(uid: str) -> RecourseOutcome:
        return RecourseOutcome(unit_ids=(uid,), sold_frac=np.zeros((P, 1), np.float32), month=np.full((P, 1), -1, np.int16),
                               proceeds_bn=np.zeros((P, 1)), red=np.zeros((P, 1), bool), reason=np.zeros((P, 1), np.int8))
    with pytest.raises(SchemaError):
        merge_outcomes([outcome("SYN-PE-0001"), outcome("SYN-PE-0002")])
    with pytest.raises(SchemaError):
        merge_outcomes([])
    with pytest.raises(SchemaError):
        merge_quotes([])


# --------------------------------------------------------------------------------- beliefs, draws, filter
def test_fake_beliefs_decomposition(setup) -> None:
    book, _, beliefs, *_ = setup
    beliefs.validate()
    assert beliefs.unit_ids == book.unit_index().unit_ids
    assert set(beliefs.benchmark_id) <= set(MINI_ASSET_CLASSES)
    assert np.array_equal(beliefs.mu_total_a, beliefs.bench_ref_a + beliefs.alpha_a)
    assert beliefs.meta.data_class is DataClass.SYNTHETIC


def test_fake_belief_draws_are_frozen_at_alpha_hat(setup) -> None:
    _, _, beliefs, world, draws = setup
    draws.validate()
    assert np.array_equal(draws.alpha0_q, np.tile((beliefs.alpha_a / 4).astype(np.float32), (P, 1)))
    assert not draws.group_bias_q.any() and draws.gp_effect_q.shape == (P, 0) and not draws.eta_sd_q.any()
    assert draws.world_id == world.world_id
    with pytest.raises(SchemaError):
        fake_belief_draws(beliefs, world, 0)


def test_fake_filter_is_a_forward_filter() -> None:
    cube = mini_cube(30)
    f = fake_filter()
    post = f(cube.factors, cube.meta.factor_names, None, np.array([0.002, 0.042]))
    assert post.shape == (30, 120, 3) and np.allclose(post.sum(axis=2), 1.0, atol=1e-6)
    short = f(cube.factors[:, :60], cube.meta.factor_names, None, np.array([0.002, 0.042]))
    assert np.array_equal(short, post[:, :60]), "appending months never changes earlier posteriors"
    assert np.array_equal(post, f(cube.factors, cube.meta.factor_names, fake_filter_params(), np.array([0.002, 0.042])))
    with pytest.raises(SchemaError):
        f(cube.factors[:, :, :3], cube.meta.factor_names[:3], None, None)


def test_fake_filter_honours_its_params() -> None:
    cube = mini_cube(10)
    params = fake_filter_params()
    sticky = params.model_copy(update={"transmat": [[0.999, 0.0005, 0.0005], [0.0005, 0.999, 0.0005],
                                                    [0.0005, 0.0005, 0.999]]})
    a = fake_filter(params)(cube.factors, cube.meta.factor_names)
    b = fake_filter(sticky)(cube.factors, cube.meta.factor_names)
    assert not np.array_equal(a, b)


def test_fake_owner_draws_keep_the_scenario_identity() -> None:
    cube = mini_cube(10)
    drawn = fake_owner_draws(cube, 0.06)
    drawn.validate()
    assert drawn.meta.checksum == cube.meta.checksum and drawn.checksum() != cube.checksum()
    assert drawn.draw_rate.shape == (10, 11) and np.allclose(drawn.draw_rate, 0.06)
    with pytest.raises(SchemaError):
        fake_owner_draws(cube, 0.12)


def test_fake_draw_block() -> None:
    from adic_tpa.contracts.engine_io import NoiseRequest

    reqs = (NoiseRequest(source="a", slots=2, entity_ids=("x", "y"), months=(0, 1, 2)),
            NoiseRequest(source="b", slots=1, entity_ids=None, months=(0,)))
    ns = fake_draw_block(b"\x07" * 16, reqs, np.arange(5))
    ns.validate()
    assert ns.u["a"].shape == (5, 3, 2, 2) and ns.u["b"].shape == (5, 1, 1, 1)
    assert np.array_equal(ns.u["a"], fake_draw_block(b"\x07" * 16, reqs, np.arange(5)).u["a"])
    assert not np.array_equal(ns.u["a"], fake_draw_block(b"\x08" * 16, reqs, np.arange(5)).u["a"])


# ---------------------------------------------------------------------------------- policy, factory, ports
def _ctx(book) -> PolicyContext:
    tax = GroupRegistry.for_version("v2")
    return PolicyContext(idx=book.unit_index(tax), tax=tax, p0_theta={},
                         recourse=RecourseOrder(rungs=("reserve", "p2s", "liquid", "facility", "amber", "red")),
                         mandate_mode=MandateMode.B_OWNER_CALL, archetype_params={}, contract_hash="x")


def test_fake_policy_holds_and_schedules_sells(setup) -> None:
    book = setup[0]
    unit = str(book.unit_index().unit_ids[0])
    policy = FakePolicy(_ctx(book), P, n_lots=3, n_facilities=2, sells={1: {unit: 0.1}})
    assert isinstance(policy, ports.Policy) and policy.policy_ref.name == "HOLD"
    ledger = FakeLedger(GroupRegistry.for_version("v2"))
    obs = fake_observables(0, ledger.init_state(book, P), len(book.unit_index().unit_ids))
    obs.validate()
    a0, a1 = policy.act(0, obs), policy.act(1, obs)
    a0.validate()
    assert not a0.sell_frac.any() and np.allclose(a1.sell_frac[:, 0], 0.1)
    assert (a1.sell_reason[:, 0] == SaleReason.DISCRETIONARY).all()


def test_fake_factory_hashes_overrides_per_module(setup) -> None:
    book, _, _, world, _ = setup
    factory = FakeEngineFactory(mini_owner_config())
    base = factory.build(book, world)
    over = factory.build(book, world.model_copy(update={"overrides": (
        MisspecOverride(target_module="priv", param_path="fund.dist_q", op="mult", value=0.8),)}))
    changed = {k for k in base.effective_config_hashes if base.effective_config_hashes[k] != over.effective_config_hashes[k]}
    assert changed == {"priv"}
    assert isinstance(base.ledger, ports.Ledger) and all(isinstance(e, ports.AssetEngine) for e in base.engines)


def test_fake_llm_backend() -> None:
    req = LLMRequest(role=RoleId.MEMO_WRITER, model="claude-opus-5-5", system="s", messages=(), tools=(), effort="high")
    memo = MemoDraft(doc_kind="memo", template_text="SYNTHETIC")
    backend = FakeLLMBackend(ModelFamily.B, outputs={MemoDraft: memo}, tool_calls=(("t", {"x": 1}),))
    assert backend.parse(req, MemoDraft).parsed == memo
    with pytest.raises(ReplayMiss):
        backend.parse(req, LensAction)
    calls = []
    out = backend.run_tools(req, (ToolDef(name="t", description="d", input_schema={}),),
                            lambda tid, name, inp: calls.append((name, dict(inp))) or {"type": "tool_result",
                                                                                     "tool_use_id": tid})
    assert calls == [("t", {"x": 1})] and out.content[0]["type"] == "tool_result"
    with pytest.raises(ReplayMiss):
        backend.run_tools(req, (), lambda *a: {})


def test_fake_evaluator_counts_budget_and_records_calls() -> None:
    from adic_tpa.contracts.evidence import EvalRequest
    from adic_tpa.contracts.ids import CampaignId

    ev = FakeEvaluator(budget=2)
    view = ev.evaluate_policy(EvalRequest(request_id="r", campaign_id=CampaignId("cmp-2026Q4-1"), attempt_id="a",
                                          spec_hash="sha256:" + "0" * 64, kind="evaluate"))
    assert view.budget_left == 1 and ev.calls == ["evaluate_policy"]
    assert set(EVALUATOR_METHODS) == {n for n, v in vars(ports.EvaluatorPort).items()
                                      if callable(v) and not n.startswith("_")}
    card = ev.phase1_restore(Phase1In())
    assert set(card.by_scenario) == set(ConsentScenario)
