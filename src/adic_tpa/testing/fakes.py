"""Fakes that honour the frozen Protocols (BUILD_SPEC v1.1 §4.5, §3.17, §3.18; owner WP-03).

SYNTHETIC – NOT ADIC DATA. Every fake is deterministic and small; none is a model of anything real.

- ``fake_engines(book)``: one ``FakeEngine`` per engine id of the book (treasury sleeves stay with the ledger).
  Flows are linear in the unit stocks (rates × NAV or unfunded on the world's benchmark returns plus the unit's α),
  so a sold fraction scales out of later flows exactly (positive homogeneity, §4.14). ``simulate_hold`` runs the
  same per-period kernel over a whole cube; ``fixtures.mini_flowcube`` and ``FakeEngine.column_flows`` use it, so
  the three agree by construction.
- ``FakeLedger``: identity-exact stand-in for ``ledger.LedgerKernel`` (cash moves only by booked flows, the owner
  instalment and recourse proceeds, each once) with a fixed amber-then-red recourse waterfall.
- ``fake_beliefs``, ``fake_belief_draws`` (α frozen at α̂, the no-learning variant), ``fake_filter`` (a Gaussian-HMM
  forward filter standing in for ``state.simulate_filter``), ``fake_owner_draws`` (stand-in for
  ``owner.attach_draws``) and ``fake_draw_block`` (stand-in for ``rng.draw_block``).
- ``FakeEngineFactory``, ``FakePolicy``, ``FakeLLMBackend`` and ``FakeEvaluator`` implement ``EngineFactory``,
  ``Policy``, ``LLMBackend`` and ``EvaluatorPort``; ``testing.committee.FakeRoom`` implements ``RoomPort``.

Conventions the fakes fix (WP-03 decisions): an engine's unit axis ``U_e`` lists its units in
``BookSnapshot.unit_index()`` order, which is how the ledger maps ``FlowSlice`` stocks to groups (a ``FlowSlice``
carries no unit ids for that axis); monthly engines are stepped with ``t`` = the month index and apply the quarter's
``ActionSlice`` in the quarter's first month; the fake ledger books recourse proceeds in the sale month.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from types import MappingProxyType
from typing import Any, Final

import numpy as np
from pydantic import BaseModel

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts.actions import FlipThresholds, LensAction
from adic_tpa.contracts.arrays import F32, F64, MAX_BLOCK_PATHS
from adic_tpa.contracts.beliefs import BeliefDraws, BeliefMeta, BeliefSet, BridgeCard, LeverLine
from adic_tpa.contracts.book import (
    BookSnapshot, Facility, Holding, LoanCohortTerms, LongOnlyTerms, PrivateFundTerms, RealAssetTerms, TreasuryTerms,
)
from adic_tpa.contracts.calendar import Calendar
from adic_tpa.contracts.claims import ProvenanceNode, ValidationReport
from adic_tpa.contracts.engine_io import (
    ActionSlice, EngineState, FlowCube, FlowCubeMeta, FlowSlice, NoiseRequest, NoiseSlice, UnitFinancing, WorldSlice,
)
from adic_tpa.contracts.enums import (
    FLOW_IS_CASH, N_FLOW_TYPES, Book, CFPStage, Clock, ConsentScenario, ContractMode, ContractModel, DataClass,
    EvidencePlane, FlowType, Lens, ModelFamily, PricedOn, RecourseTier, RowFamily, SaleReason, StressState,
)
from adic_tpa.contracts.errors import ReplayMiss, SchemaError
from adic_tpa.contracts.evidence import EvalRequest, EvalResultAgentView, LLMCallRecord, MetricInstance
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import ArtifactRef, GroupId, MetricId, RunId, UnitId
from adic_tpa.contracts.lab import AssumptionEntry, Escalation
from adic_tpa.contracts.ledger import (
    CFPReading, LedgerState, RecourseAvailability, RecourseOutcome, StressReport, StressSpec,
)
from adic_tpa.contracts.optimizer import Envelope, FTPPoint, RowKey
from adic_tpa.contracts.overlay import CRIFRow
from adic_tpa.contracts.policy import ActionPackage, Observables, OverlayStructure, PolicyRef, PolicySpec
from adic_tpa.contracts.ports import (
    AssetEngine, EngineBundle, Ledger, LLMRequest, LLMResponse, PolicyContext, ToolDef, ToolExecutor,
)
from adic_tpa.contracts.room import EPResult, ScenarioSpecDraft
from adic_tpa.contracts.rules import instalment_bn, intra_quarter_profile
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.tools import (
    Ack, AttributeIn, AttributionCard, CardIdsIn, EnvelopeSummary, EPIn, EVSIIn, EVSIResult, FlipIn, HSummary,
    HybridCheck, ImpliedActionCard, ImpliedIn, MetricListIn, MetricQueryIn, OffsetCard, OffsetRow, OptimizeHIn,
    PackagePrice, Phase1Card, Phase1In, ProvenanceQueryIn, ReverseStressIn, ReverseStressResult, ScenarioResult,
    StateCard, StateSnapshotIn, TierSummary, TradePrice, TypeReport, ValidateClaimsIn,
)
from adic_tpa.contracts.units import q_rate
from adic_tpa.contracts.world import OwnerConfig, ScenarioCube, StressFilterParams, WorldSpec

__all__ = [
    "MINI_ASSET_CLASSES", "FILTER_OBSERVABLES", "FAKE_RUN_ID", "FakeUnitModel", "unit_models", "benchmark_of",
    "simulate_hold", "book_hold_flows", "world_slice", "FakeEngineState", "FakeEngine", "fake_engines", "FakeLedger",
    "merge_quotes", "merge_outcomes", "fake_beliefs", "fake_belief_draws", "fake_filter_params", "fake_filter", "fake_owner_draws",
    "fake_draw_block", "fake_observables", "FakePolicy", "FakeEngineFactory", "FakeLLMBackend", "FakeEvaluator",
    "FakeRobustnessCard", "FakeSimmResult", "FakeOVReport", "EVALUATOR_METHODS",
]

# CMA asset classes of the mini world and cube (contracts treat asset names as data; WP-06 owns the real list).
MINI_ASSET_CLASSES: Final[tuple[str, ...]] = (
    "us_equity", "global_equity", "em_equity", "us_treasury", "ig_credit", "hy_credit", "pe_buyout", "venture",
    "private_credit", "real_estate", "infrastructure", "hedge_funds", "cash")
# The stress filter's own observables, read from the cube (§4.9 simulate_filter; S-ADR-35).
FILTER_OBSERVABLES: Final[tuple[str, ...]] = ("us_eq_excess", "log_rv", "ebp_lag1", "d_ust10y")
FAKE_RUN_ID: Final = RunId("run-20261018T000000Z-0000fa4e")
_F: Final = N_FLOW_TYPES
_CASH: Final = np.array(FLOW_IS_CASH, dtype=bool)
_CRISIS_DIST_MULT: Final = 0.5
_CRISIS_CALL_MULT: Final = 1.25
_CRISIS_INCOME_MULT: Final = 0.9
_CRISIS_BID_MULT: Final = 0.75
_FIN_WINDOW_HAIRCUT: Final = (0.0, 0.03, 0.08)      # OPEN, TIGHT, CLOSED: stand-in for the crowding haircut
_REFI_RATE_A: Final = 0.06
_IM_RATE: Final = 0.04
_LO_HQLA_SHARE: Final = 0.85
_TREASURY_HQLA: Final = np.array([1.0, 0.98, 0.90])      # cash, UST, IG haircuts for unencumbered HQLA


def _ref(artifact: str, pointer: str = "") -> ArtifactRef:
    return ArtifactRef.make(FAKE_RUN_ID, artifact, pointer)


# --------------------------------------------------------------------------------------------------- unit model
@dataclass(frozen=True, slots=True)
class FakeUnitModel:
    """Per-unit constants of the fake flow model (rates per quarter; money in USD bn)."""

    unit_id: UnitId
    group: GroupId
    group_index: int
    engine_id: str
    unit_kind: str
    strategy: str
    benchmark: str
    alpha_q: float              # α̂ per quarter (fake_beliefs alpha_a / 4); used when no BeliefDraws are given
    nav0: float
    unfunded0: float
    encumbered0: float
    dist_q: float
    call_q: float
    income_q: float
    pik_q: float
    fee_q: float
    capex_q: float
    debt_service_q: float
    smoothing: float            # reported-NAV appraisal weight per period (1.0: marked to market)
    tier: int                   # 0 not a recourse unit, 1 amber, 2 red
    normal_bid: float           # normal-regime cash-equivalent bid ÷ economic NAV
    depth: float                # maximum fraction saleable per quarter
    lag_m: int
    hqla_share: float           # share of NAV counted in hqla_contrib_bn (public sleeves only)


_KIND_ALPHA_A: Final = MappingProxyType({
    "fund": 0.015, "company": 0.020, "claim": 0.010, "loan_cohort": 0.005, "ra_asset": 0.010, "ra_open_end": 0.008,
    "hf_lot": 0.010, "longonly": 0.0, "treasury": 0.0, "overlay_bucket": 0.0})
_KIND_BETA: Final = MappingProxyType({
    "fund": 1.1, "company": 1.3, "claim": 0.5, "loan_cohort": 0.3, "ra_asset": 0.6, "ra_open_end": 0.5, "hf_lot": 0.35,
    "longonly": 1.0, "treasury": 0.0, "overlay_bucket": 0.0})
_KIND_SIGMA: Final = MappingProxyType({
    "fund": 0.18, "company": 0.25, "claim": 0.08, "loan_cohort": 0.06, "ra_asset": 0.12, "ra_open_end": 0.10,
    "hf_lot": 0.07, "longonly": 0.15, "treasury": 0.01, "overlay_bucket": 0.05})
_NORMAL_BID: Final = MappingProxyType({"company": 0.80, "claim": 0.88, "loan_cohort": 0.95, "ra_asset": 0.85,
                                       "ra_open_end": 0.95})


def benchmark_of(h: Holding) -> str:
    """The mini world's CMA asset class benchmarking a holding (stand-in for ``scen.asset_class_map``)."""
    t = h.terms
    if isinstance(t, PrivateFundTerms):
        return {"vc": "venture", "growth": "venture", "credit_fund": "private_credit",
                "ra_closed": "real_estate"}.get(t.strategy_class, "pe_buyout")
    if isinstance(t, RealAssetTerms):
        return "real_estate" if t.sector == "REAL_ESTATE" else "infrastructure"
    if isinstance(t, LongOnlyTerms):
        return {"DM_EQ": "global_equity", "EM_EQ": "em_equity", "FI": "ig_credit"}[t.sleeve]
    if isinstance(t, TreasuryTerms):
        return {"CASH": "cash", "UST": "us_treasury", "IG": "ig_credit"}[t.sleeve]
    return {"company": "pe_buyout", "claim": "hy_credit", "loan_cohort": "private_credit", "hf_lot": "hedge_funds",
            "overlay_bucket": "us_equity"}.get(h.unit_kind, "us_equity")


def _unit_jitter(unit_id: str, scale: float) -> float:
    """A deterministic, unit-specific offset in [-scale, scale] (makes per-unit mappings testable)."""
    k = int.from_bytes(hashlib.sha256(unit_id.encode("utf-8")).digest()[:4], "little")
    return scale * ((k % 2001) / 1000.0 - 1.0)


def _rates(h: Holding, age_bucket: int) -> dict[str, float]:
    kind, t = h.unit_kind, h.terms
    r = dict(dist_q=0.0, call_q=0.0, income_q=0.0, pik_q=0.0, fee_q=0.0, capex_q=0.0, debt_service_q=0.0)
    if isinstance(t, PrivateFundTerms):
        r.update(dist_q=0.030 if age_bucket == 0 else 0.055, call_q=0.08 if age_bucket == 0 else 0.05,
                 fee_q=t.fee_rate_a / 4.0)
    elif kind == "company":
        r.update(dist_q=0.02)
    elif kind == "claim":
        r.update(income_q=0.11 * 0.7 / 4.0, pik_q=0.11 * 0.3 / 4.0, dist_q=0.03, call_q=0.10)
    elif isinstance(t, LoanCohortTerms):
        r.update(income_q=(0.0389 + t.spread_a) / 4.0, dist_q=1.0 / (4.0 * t.wam_years), call_q=0.10)
    elif isinstance(t, RealAssetTerms):
        nav = max(h.nav_reported_bn, 1e-12)
        debt = t.debt.balance_bn * (0.0389 + t.debt.spread_a) if t.debt is not None else 0.0
        r.update(income_q=t.noi_bn / nav / 4.0, capex_q=t.capex_reserve_rate_a / 4.0, debt_service_q=debt / nav / 4.0,
                 call_q=0.06)
    return r


def unit_models(book: BookSnapshot, *, tax: GroupRegistry | None = None,
                beliefs: BeliefSet | None = None) -> tuple[FakeUnitModel, ...]:
    """Fake-engine units of ``book`` in ``unit_index()`` order (treasury sleeves excluded: the ledger owns them)."""
    reg = tax if tax is not None else GroupRegistry.for_version(book.taxonomy_version)
    idx = book.unit_index(reg)
    by_id = {str(h.holding_id): h for h in book.holdings}
    alpha = ({str(u): float(a) for u, a in zip(beliefs.unit_ids, beliefs.alpha_a, strict=True)}
             if beliefs is not None else {})
    out = []
    for i, uid in enumerate(idx.unit_ids):
        engine = idx.engine_of[i]
        if engine == "treasury":
            continue
        h = by_id[str(uid)]
        spec = reg.spec(h.group)
        ab = max(int(idx.age_bucket[i]), 0)
        tier = 1 if h.unit_kind == "ra_open_end" else 2 if spec.red_tier else 1 if spec.amber_tier else 0
        normal_bid = (0.85 if ab == 0 else 0.90) if h.unit_kind == "fund" else _NORMAL_BID.get(h.unit_kind, 1.0)
        a_q = alpha.get(str(uid), _alpha_a(h)) / 4.0
        out.append(FakeUnitModel(
            unit_id=UnitId(str(uid)), group=h.group, group_index=reg.index(h.group), engine_id=engine,
            unit_kind=h.unit_kind, strategy=h.strategy, benchmark=benchmark_of(h), alpha_q=a_q,
            nav0=h.nav_reported_bn, unfunded0=h.unfunded_bn, encumbered0=h.encumbered_bn, **_rates(h, ab),
            smoothing=1.0 if spec.kind in ("public", "overlay") else 0.5, tier=tier, normal_bid=normal_bid,
            depth={2: 0.25, 1: 0.5}.get(tier, 0.0), lag_m={2: 2, 1: 1}.get(tier, 0),
            hqla_share=_LO_HQLA_SHARE if h.unit_kind == "longonly" else 0.0))
    return tuple(out)


def _alpha_a(h: Holding) -> float:
    return _KIND_ALPHA_A[h.unit_kind] + (_unit_jitter(str(h.holding_id), 0.001) if _KIND_ALPHA_A[h.unit_kind] else 0.0)


@dataclass(frozen=True, slots=True)
class _OverlayParams:
    """Overlay-engine constants from ``BookSnapshot.overlay`` (strategies tail / opportunistic / synthetic_beta)."""

    tail_premium_m: float       # USD bn a month
    tail_notional: float
    beta_notional: float
    service_fee_m: float        # completion-beta service fee, USD bn a month (intra-ADIC)
    service_client_index: int   # taxonomy column of the service client (-1: none)
    owner_index: int            # taxonomy column of the overlay group
    tail_unit: int              # unit column of the tail bucket (-1: none)
    beta_unit: int              # unit column of the synthetic-beta bucket (-1: none)


def _overlay_params(book: BookSnapshot, units: Sequence[FakeUnitModel], reg: GroupRegistry) -> _OverlayParams:
    ov = book.overlay
    strategy = [m.strategy for m in units]
    return _OverlayParams(
        tail_premium_m=ov.policy.tail_budget_a * book.nav_total_reported_bn / 12.0,
        tail_notional=sum(t.notional_bn for t in ov.trades if t.book is Book.TAIL),
        beta_notional=sum(t.notional_bn for t in ov.trades if t.book is Book.BETA),
        service_fee_m=sum(s.s_lock_a * s.notional_bn for s in ov.services) / 12.0,
        service_client_index=reg.index(ov.services[0].client_group) if ov.services else -1,
        owner_index=units[0].group_index,
        tail_unit=strategy.index("tail") if "tail" in strategy else -1,
        beta_unit=strategy.index("synthetic_beta") if "synthetic_beta" in strategy else -1)


# ---------------------------------------------------------------------------------------------- period kernel
def _crisis(stress_post: F32) -> np.ndarray:
    """Crisis indicator of a period [P]: stress-filter posterior of CRISIS above one half at the period's end."""
    return np.asarray(stress_post[:, -1, int(StressState.CRISIS)], dtype=np.float64) > 0.5


def _period(units: Sequence[FakeUnitModel], nav: F64, unf: F64, nav_rep: F64, log_ret: F64, crisis: np.ndarray,
            alpha_q: F64, n_months: int) -> tuple[F64, F64, F64, F64]:
    """One period of the linear kernel; returns (flows [P, U, 18], nav, unfunded, reported NAV) at period end."""
    p, u = nav.shape
    scale = n_months / 3.0
    rate = {k: np.array([getattr(m, k) for m in units], dtype=np.float64) * scale
            for k in ("dist_q", "call_q", "income_q", "pik_q", "fee_q", "capex_q", "debt_service_q")}
    growth = np.expm1(log_ret + alpha_q * scale)
    c = crisis[:, None]
    dist = rate["dist_q"] * np.where(c, _CRISIS_DIST_MULT, 1.0) * nav
    calls = np.minimum(unf, rate["call_q"] * np.where(c, _CRISIS_CALL_MULT, 1.0) * unf)
    pik = rate["pik_q"] * nav
    flows = np.zeros((p, u, _F))
    flows[:, :, FlowType.CALL] = -calls
    flows[:, :, FlowType.DISTRIBUTION] = dist
    flows[:, :, FlowType.INCOME_CASH] = rate["income_q"] * np.where(c, _CRISIS_INCOME_MULT, 1.0) * nav
    flows[:, :, FlowType.PIK_ACCRUAL] = pik
    flows[:, :, FlowType.FEES] = -rate["fee_q"] * nav
    flows[:, :, FlowType.CAPEX] = -rate["capex_q"] * nav
    flows[:, :, FlowType.DEBT_SERVICE] = -rate["debt_service_q"] * nav
    nav_new = np.maximum(nav * (1.0 + growth) + calls - dist + pik, 0.0)
    w = np.array([m.smoothing for m in units], dtype=np.float64)
    return flows, nav_new, unf - calls, nav_rep + w * (nav_new - nav_rep)


def _overlay_period(ov: _OverlayParams, flows: F64, intra: F64 | None, eq_log_ret: F64, eq_index: F64,
                    n_months: int) -> F64:
    """Overlay flows of one period (premium, monetization, VM and ΔIM); returns the new equity index level [P]."""
    gross = np.expm1(eq_log_ret)
    if ov.tail_unit >= 0:
        flows[:, ov.tail_unit, FlowType.PREMIUM] = -ov.tail_premium_m * n_months
        flows[:, ov.tail_unit, FlowType.MONETIZATION] = 0.5 * ov.tail_notional * np.maximum(0.0, -gross - 0.15)
    new_index = eq_index * (1.0 + gross)
    if ov.beta_unit >= 0:
        flows[:, ov.beta_unit, FlowType.VM] = ov.beta_notional * eq_index * gross
        flows[:, ov.beta_unit, FlowType.DELTA_IM] = -_IM_RATE * ov.beta_notional * (new_index - eq_index)
    if intra is not None and ov.service_client_index >= 0:
        fee = ov.service_fee_m * n_months
        intra[:, ov.service_client_index, FlowType.FEES] -= fee
        intra[:, ov.owner_index, FlowType.FEES] += fee
    return new_index


def _benchmark_index(units: Sequence[FakeUnitModel], asset_names: Sequence[str]) -> np.ndarray:
    pos = {a: i for i, a in enumerate(asset_names)}
    missing = sorted({m.benchmark for m in units} - set(pos))
    if missing:
        raise SchemaError(f"fake engine: benchmarks {missing} are not cube asset classes {tuple(asset_names)}")
    return np.array([pos[m.benchmark] for m in units], dtype=np.int64)


def _engine_clock(engine_id: str) -> Clock:
    """Private engines run quarterly; Public Markets and the overlay monthly (§4.11–§4.13)."""
    return Clock.QUARTERLY if engine_id.startswith("priv.") else Clock.MONTHLY


def _steps(clock: Clock, quarters: int) -> list[tuple[int, tuple[int, ...]]]:
    if clock is Clock.MONTHLY:
        return [(q, (3 * q + k,)) for q in range(quarters) for k in range(3)]
    return [(q, (3 * q, 3 * q + 1, 3 * q + 2)) for q in range(quarters)]


def simulate_hold(units: Sequence[FakeUnitModel], cube: ScenarioCube, *, quarters: int = 40,
                  overlay: _OverlayParams | None = None) -> F64:
    """HOLD flows of ``units`` on ``cube`` by quarter: [P, Q, U, 18] signed USD bn (§1.4), α frozen at α̂.

    Quarterly engines step once per quarter; monthly engines (``pub.*``, ``overlay``) step monthly and are summed
    into the quarter. No actions, no recourse. ``overlay`` adds the overlay engine's notional-driven flows.
    """
    p = cube.meta.n_paths
    if quarters * 3 > cube.meta.months:
        raise SchemaError(f"simulate_hold: {quarters} quarters exceed the cube's {cube.meta.months} months")
    bench = _benchmark_index(units, cube.meta.asset_names)
    eq = cube.meta.asset_names.index("us_equity") if "us_equity" in cube.meta.asset_names else 0
    out = np.zeros((p, quarters, len(units), _F))
    for engine in sorted({m.engine_id for m in units}):
        cols = [i for i, m in enumerate(units) if m.engine_id == engine]
        sub = [units[i] for i in cols]
        nav = np.tile([m.nav0 for m in sub], (p, 1)).astype(np.float64)
        unf = np.tile([m.unfunded0 for m in sub], (p, 1)).astype(np.float64)
        rep = nav.copy()
        alpha = np.tile([m.alpha_q for m in sub], (p, 1)).astype(np.float64)
        eq_index = np.ones(p)
        for q, months in _steps(_engine_clock(engine), quarters):
            sl = slice(months[0], months[-1] + 1)
            log_ret = cube.asset_returns[:, sl, :][:, :, bench[cols]].astype(np.float64).sum(axis=1)
            flows, nav, unf, rep = _period(sub, nav, unf, rep, log_ret, _crisis(cube.stress_post[:, sl, :]), alpha,
                                           len(months))
            if engine == "overlay" and overlay is not None:
                eq_ret = cube.asset_returns[:, sl, eq].astype(np.float64).sum(axis=1)
                eq_index = _overlay_period(overlay, flows, None, eq_ret, eq_index, len(months))
            out[:, q, cols, :] += flows
    return out


def book_hold_flows(book: BookSnapshot, cube: ScenarioCube, *,
                    beliefs: BeliefSet | None = None) -> tuple[tuple[FakeUnitModel, ...], F64]:
    """HOLD flows [P, 40, U, 18] of every engine unit of ``book`` on ``cube`` (``simulate_hold`` with the overlay
    engine's notional-driven flows), units in ``unit_index()`` order; α from ``beliefs`` (default: frozen α̂)."""
    reg = GroupRegistry.for_version(book.taxonomy_version)
    units = unit_models(book, tax=reg, beliefs=beliefs)
    overlay_units = [m for m in units if m.engine_id == "overlay"]
    overlay = _overlay_params(book, overlay_units, reg) if overlay_units else None
    return units, simulate_hold(units, cube, overlay=overlay)


def world_slice(cube: ScenarioCube, months: Sequence[int], *, clock: Clock, t: int) -> WorldSlice:
    """The ``WorldSlice`` of ``cube`` over ``months`` (``core.sim``'s job; a helper for tests and the skeleton)."""
    sl = [int(m) for m in months]
    return WorldSlice(clock=clock, t=t, months=tuple(sl),
                      factors=np.ascontiguousarray(cube.factors[:, sl, :]),
                      regimes=np.ascontiguousarray(cube.regimes[:, sl, :]),
                      stress_post=np.ascontiguousarray(cube.stress_post[:, sl, :]),
                      vol=np.ascontiguousarray(cube.vol[:, sl, :]),
                      fin_window=np.ascontiguousarray(cube.fin_window[:, sl]),
                      asset_returns=np.ascontiguousarray(cube.asset_returns[:, sl, :]),
                      brent=np.ascontiguousarray(cube.brent[:, sl]))


# ------------------------------------------------------------------------------------------------ fake engine
class FakeEngineState(EngineState):
    """Mutable state of one ``FakeEngine`` block (float64 internally; ``stocks()`` returns float32 copies)."""

    def __init__(self, unit_ids: tuple[UnitId, ...], nav: F64, unfunded: F64, encumbered: F64, alpha_q: F64,
                 action_cols: np.ndarray, financing: UnitFinancing) -> None:
        self.unit_ids = unit_ids
        self.nav = nav
        self.nav_rep = nav.copy()
        self.unfunded = unfunded
        self.encumbered = encumbered
        self.alpha_q = alpha_q
        self.action_cols = action_cols
        self.financing = financing
        self.eq_index = np.ones(nav.shape[0])

    @property
    def n_paths(self) -> int:
        return int(self.nav.shape[0])

    def stocks(self) -> tuple[F32, F32, F32]:
        return (self.nav.astype(np.float32), self.nav_rep.astype(np.float32), self.unfunded.astype(np.float32))


class FakeEngine:
    """Deterministic linear engine (§4.5): implements ``contracts.ports.AssetEngine``."""

    def __init__(self, engine_id: str, units: Sequence[FakeUnitModel], *, n_groups: int,
                 asset_names: Sequence[str] = MINI_ASSET_CLASSES, overlay: _OverlayParams | None = None) -> None:
        if not units:
            raise SchemaError(f"{engine_id}: a fake engine needs at least one unit")
        self.engine_id = engine_id
        self.clock = _engine_clock(engine_id)
        self.units = tuple(units)
        order: list[GroupId] = []
        for m in sorted(self.units, key=lambda m: m.group_index):
            if m.group not in order:
                order.append(m.group)
        self.groups: tuple[GroupId, ...] = tuple(order)
        self.n_groups = n_groups
        self.asset_names = tuple(asset_names)
        self.overlay = overlay
        self._bench = _benchmark_index(self.units, self.asset_names)
        self._unit_ids = tuple(m.unit_id for m in self.units)
        self._rec = np.array([i for i, m in enumerate(self.units) if m.tier > 0], dtype=np.int64)

    @property
    def unit_ids(self) -> tuple[UnitId, ...]:
        return self._unit_ids

    @property
    def recourse_unit_ids(self) -> tuple[UnitId, ...]:
        return tuple(self._unit_ids[i] for i in self._rec)

    # -- Protocol --------------------------------------------------------------------------------------
    def init(self, book: BookSnapshot, beliefs: BeliefSet, n_paths: int, *, draws: BeliefDraws,
             world: WorldSpec) -> FakeEngineState:
        if not 1 <= n_paths <= MAX_BLOCK_PATHS:
            raise SchemaError(f"{self.engine_id}: n_paths must lie in [1, {MAX_BLOCK_PATHS}] (one block)")
        if draws.alpha0_q.shape[0] != n_paths:
            raise SchemaError(f"{self.engine_id}: BeliefDraws hold {draws.alpha0_q.shape[0]} paths, expected {n_paths}")
        if draws.world_id != world.world_id:
            raise SchemaError(f"{self.engine_id}: draws are for world {draws.world_id}, not {world.world_id}")
        by_id = {str(h.holding_id): h for h in book.holdings}
        dcol = {str(u): j for j, u in enumerate(draws.unit_ids)}
        icol = {str(u): j for j, u in enumerate(book.unit_index().unit_ids)}
        missing = [str(u) for u in self._unit_ids if str(u) not in by_id or str(u) not in dcol]
        if missing:
            raise SchemaError(f"{self.engine_id}: units {missing[:3]} missing from the book or the draws")
        hs = [by_id[str(u)] for u in self._unit_ids]

        def tile(values: Sequence[float]) -> F64:
            return np.tile(np.asarray(values, dtype=np.float64), (n_paths, 1))

        n = len(self._unit_ids)
        financing = UnitFinancing(
            unit_ids=self._unit_ids, instrument_ids=tuple("navloan" for _ in range(n)),
            balance_bn=np.zeros((n_paths, n)), rate_q=np.full(n, q_rate(_REFI_RATE_A)), amort_q=np.zeros(n),
            ltv_covenant=np.full(n, 0.5), breached=np.zeros((n_paths, n), dtype=bool))
        alpha = draws.alpha0_q[:, [dcol[str(u)] for u in self._unit_ids]].astype(np.float64)
        return FakeEngineState(unit_ids=self._unit_ids, nav=tile([h.nav_reported_bn for h in hs]),
                               unfunded=tile([h.unfunded_bn for h in hs]), encumbered=tile([h.encumbered_bn for h in hs]),
                               alpha_q=np.ascontiguousarray(alpha),
                               action_cols=np.array([icol[str(u)] for u in self._unit_ids], dtype=np.int64),
                               financing=financing)

    def noise_requests(self, t: int) -> tuple[NoiseRequest, ...]:
        """One stream per quarter (the fake checks but never uses its uniforms: flows are deterministic)."""
        return (NoiseRequest(source=f"{self.engine_id}.fake", slots=1, entity_ids=tuple(str(u) for u in self._unit_ids),
                             months=(3 * t, 3 * t + 1, 3 * t + 2)),)

    def recourse_quotes(self, t: int, st: EngineState, world: WorldSlice) -> RecourseAvailability:
        if not isinstance(st, FakeEngineState):
            raise SchemaError(f"{self.engine_id}: expected a FakeEngineState")
        rec = [self.units[i] for i in self._rec]
        p = st.n_paths
        crisis = _crisis(world.stress_post)
        # TODO(contracts): WorldSlice carries no crowding_index, so a financing-window haircut stands in for
        # S-ADR-13's crowding haircut; liquid units (long-only, HF lots) are not quoted because
        # RecourseAvailability.tier admits only 1 (amber) and 2 (red).
        window = np.asarray(_FIN_WINDOW_HAIRCUT)[world.fin_window[:, 0].astype(np.int64)]
        normal = np.array([m.normal_bid for m in rec], dtype=np.float64)
        bid = normal[None, :] * np.where(crisis[:, None], _CRISIS_BID_MULT, 1.0) * (1.0 - window[:, None])
        return RecourseAvailability(
            engine_id=self.engine_id, unit_ids=tuple(m.unit_id for m in rec), group_of=tuple(m.group for m in rec),
            bid_frac=np.clip(bid, 1e-6, 1.2).astype(np.float32),
            normal_bid_frac=normal.astype(np.float32),
            depth_frac=np.tile(np.array([m.depth for m in rec], dtype=np.float32), (p, 1)),
            lag_m=np.tile(np.array([m.lag_m for m in rec], dtype=np.int8), (p, 1)),
            tier=np.array([m.tier for m in rec], dtype=np.int8))

    def step(self, t: int, st: EngineState, world: WorldSlice, act: ActionSlice, noise: NoiseSlice) -> FlowSlice:
        if not isinstance(st, FakeEngineState):
            raise SchemaError(f"{self.engine_id}: expected a FakeEngineState")
        months = tuple(world.months)
        expected = (t,) if self.clock is Clock.MONTHLY else (3 * t, 3 * t + 1, 3 * t + 2)
        if months != expected or world.clock is not self.clock:
            raise SchemaError(f"{self.engine_id}: step t={t} needs a {self.clock.value} WorldSlice over {expected}, "
                              f"got {world.clock.value} {months}")
        source = f"{self.engine_id}.fake"
        req = next((r for r in noise.requests if r.source == source), None)
        if req is None or source not in noise.u or not set(months) <= set(req.months):
            raise SchemaError(f"{self.engine_id}: the NoiseSlice does not cover source {source} months {months}")
        p, u = st.nav.shape
        flows = np.zeros((p, u, _F))
        if months[0] % 3 == 0 and act.t == months[0] // 3:
            self._apply_actions(st, act, flows)
        flows[:, :, FlowType.DEBT_SERVICE] -= np.asarray(st.financing.rate_q) * (len(months) / 3.0) * \
            st.financing.balance_bn
        log_ret = world.asset_returns[:, :, self._bench].astype(np.float64).sum(axis=1)
        body, st.nav, st.unfunded, st.nav_rep = _period(self.units, st.nav, st.unfunded, st.nav_rep, log_ret,
                                                        _crisis(world.stress_post), st.alpha_q, len(months))
        flows += body
        intra = np.zeros((p, self.n_groups, _F))
        if self.overlay is not None:
            eq = self.asset_names.index("us_equity") if "us_equity" in self.asset_names else 0
            eq_ret = world.asset_returns[:, :, eq].astype(np.float64).sum(axis=1)
            st.eq_index = _overlay_period(self.overlay, flows, intra, eq_ret, st.eq_index, len(months))
        by_group = np.zeros((p, self.n_groups, _F))
        for i, m in enumerate(self.units):
            by_group[:, m.group_index, :] += flows[:, i, :]
        f32 = np.float32
        return FlowSlice(
            engine_id=self.engine_id, clock=self.clock, t=t, by_group=by_group.astype(f32), intra=intra.astype(f32),
            by_unit=flows.astype(f32), recourse_unit_ids=self.recourse_unit_ids,
            by_recourse_unit=np.ascontiguousarray(flows[:, self._rec, :]).astype(f32),
            nav_econ=st.nav.astype(f32), nav_rep=st.nav_rep.astype(f32), unfunded=st.unfunded.astype(f32),
            encumbered=st.encumbered.astype(f32),
            hqla_contrib_bn=(st.nav * np.array([m.hqla_share for m in self.units])).sum(axis=1).astype(f32))

    def _apply_actions(self, st: FakeEngineState, act: ActionSlice, flows: F64) -> None:
        """Discretionary sells at the normal bid, REFINANCE draws and ADDs at the quarter's start."""
        cols = st.action_cols
        sell = np.asarray(act.sell_frac[:, cols], dtype=np.float64)
        bid = np.array([m.normal_bid for m in self.units])[None, :]
        flows[:, :, FlowType.SALE_PROCEEDS] += sell * st.nav * bid
        for arr in (st.nav, st.nav_rep, st.unfunded, st.encumbered):
            arr *= 1.0 - sell
        add = np.asarray(act.add_bn[:, cols], dtype=np.float64)
        flows[:, :, FlowType.CALL] -= add
        st.nav += add
        st.nav_rep += add
        draw = np.asarray(act.refi_draw_bn[:, cols], dtype=np.float64)
        flows[:, :, FlowType.DEBT_DRAW] += draw
        st.financing.balance_bn += draw

    def apply_recourse(self, st: EngineState, outcome: RecourseOutcome) -> None:
        if not isinstance(st, FakeEngineState):
            raise SchemaError(f"{self.engine_id}: expected a FakeEngineState")
        pos = {str(u): i for i, u in enumerate(st.unit_ids)}
        for j, uid in enumerate(outcome.unit_ids):
            i = pos.get(str(uid))
            if i is None:
                continue
            keep = 1.0 - outcome.sold_frac[:, j].astype(np.float64)
            for arr in (st.nav, st.nav_rep, st.unfunded, st.encumbered):
                arr[:, i] *= keep

    def column_flows(self, unit_id: UnitId, action: LensAction, cube: ScenarioCube) -> FlowCube:
        """Δ flows vs HOLD on CRN for one unit over 40 quarters (§3.8 column cube; LEVER ≡ ADD + REFI exactly)."""
        pos = {str(u): i for i, u in enumerate(self._unit_ids)}
        if str(unit_id) not in pos:
            raise SchemaError(f"{self.engine_id}: unknown unit {unit_id}")
        if action.lens is Lens.PACE or action.unit_id is None or str(action.unit_id) != str(unit_id):
            raise SchemaError(f"{self.engine_id}: column_flows needs a unit-level action on {unit_id}")
        m = self.units[pos[str(unit_id)]]
        hold = simulate_hold(self.units, cube, overlay=self.overlay)[:, :, pos[str(unit_id)], :]
        delta = np.zeros_like(hold)
        if action.lens in (Lens.SELL, Lens.ADD, Lens.LEVER):
            delta += (action.exposure_delta_bn / max(m.nav0, 1e-12)) * hold
            if action.lens is Lens.SELL:
                delta[:, 0, FlowType.SALE_PROCEEDS] += -action.exposure_delta_bn * m.normal_bid
            else:
                delta[:, 0, FlowType.CALL] -= action.exposure_delta_bn
        if action.lens in (Lens.REFINANCE, Lens.LEVER):
            draw = action.financing_delta_bn
            delta[:, 0, FlowType.DEBT_DRAW] += draw
            delta[:, :, FlowType.DEBT_SERVICE] -= q_rate(_REFI_RATE_A) * draw
            delta[:, -1, FlowType.DEBT_REPAY] -= draw
        meta = FlowCubeMeta(unit_ids=(m.unit_id,), group_of=(m.group,), quarters=hold.shape[1],
                            cube_checksum=cube.meta.checksum, action=action)
        return FlowCube(meta=meta, values=delta[:, :, None, :].astype(np.float32))


def fake_engines(book: BookSnapshot) -> list[AssetEngine]:
    """One deterministic linear engine per engine id of ``book`` (§4.5), in engine-id order; treasury sleeves
    belong to the ledger (``LedgerState.treasury_bn``) and get no engine. Each is a ``FakeEngine``."""
    reg = GroupRegistry.for_version(book.taxonomy_version)
    units = unit_models(book, tax=reg)
    engines: list[AssetEngine] = []
    for engine in sorted({m.engine_id for m in units}):
        sub = [m for m in units if m.engine_id == engine]
        overlay = _overlay_params(book, sub, reg) if engine == "overlay" else None
        engines.append(FakeEngine(engine, sub, n_groups=len(reg), overlay=overlay))
    return engines


# ------------------------------------------------------------------------------------------------ fake ledger
def merge_quotes(quotes: Sequence[RecourseAvailability]) -> RecourseAvailability:
    """Concatenate the engines' quarter-start quotes into the one ``RecourseAvailability`` ``Ledger.apply`` takes."""
    if not quotes:
        raise SchemaError("merge_quotes needs at least one RecourseAvailability")
    return RecourseAvailability(
        engine_id="merged", unit_ids=tuple(u for q in quotes for u in q.unit_ids),
        group_of=tuple(g for q in quotes for g in q.group_of),
        bid_frac=np.concatenate([q.bid_frac for q in quotes], axis=1),
        normal_bid_frac=np.concatenate([q.normal_bid_frac for q in quotes]),
        depth_frac=np.concatenate([q.depth_frac for q in quotes], axis=1),
        lag_m=np.concatenate([q.lag_m for q in quotes], axis=1),
        tier=np.concatenate([q.tier for q in quotes]))


def merge_outcomes(outcomes: Sequence[RecourseOutcome]) -> RecourseOutcome:
    """A quarter's monthly ``RecourseOutcome``s as one (fractions add: each is a share of the quarter-start
    position; the month is the first sale month), for ``AssetEngine.apply_recourse``."""
    if not outcomes:
        raise SchemaError("merge_outcomes needs at least one RecourseOutcome")
    first = outcomes[0]
    if any(tuple(o.unit_ids) != tuple(first.unit_ids) for o in outcomes):
        raise SchemaError("merge_outcomes: outcomes cover different units")
    big = np.iinfo(np.int16).max
    month = np.stack([np.where(o.month >= 0, o.month, big) for o in outcomes]).min(axis=0)
    return RecourseOutcome(
        unit_ids=first.unit_ids,
        sold_frac=np.minimum(np.sum([o.sold_frac.astype(np.float64) for o in outcomes], axis=0), 1.0).astype(np.float32),
        month=np.where(month == big, -1, month).astype(np.int16),
        proceeds_bn=np.sum([o.proceeds_bn for o in outcomes], axis=0),
        red=np.logical_or.reduce([o.red for o in outcomes]),
        reason=np.max([o.reason for o in outcomes], axis=0).astype(np.int8))


class FakeLedger(Ledger):
    """Identity-exact stand-in for ``ledger.LedgerKernel`` (§4.5, §4.14): implements ``contracts.ports.Ledger``.

    The treasury (cash, UST, IG at market value) changes only by the month's booked cash flows (quarterly
    ``FlowSlice``s spread by ``contracts.rules.intra_quarter_profile``; intra-ADIC and non-cash flows excluded), the
    owner instalment, facility draws and recourse proceeds, each booked once:
    Δ(cash + UST + IG) = booked − sold units' remaining flows + instalment + unpaid + facility draw + proceeds
    (+ shortfall). Waterfall rungs: reserve (UST, then IG into cash while cash < 0, value-neutral), facility (signed,
    committed lines from their availability month), amber then red sales at the quarter-start bids within their
    quarterly depth, then the instalment goes unpaid (``payout_short``); a path that still cannot pay is ``failed``.
    The trigger is HQLA below ``ig_hard`` × W (or negative cash). A sold fraction scales out of the unit's remaining
    intra-quarter flows (``FlowSlice.by_recourse_unit``, exact by positive homogeneity). Red flags follow S-ADR-30
    (i): a red-tier sale executed by the waterfall is red whatever its label. ``last`` holds the latest call's
    identity terms (booked, draw_requested, unpaid, facility_draw, proceeds, shortfall).
    """

    def __init__(self, tax: GroupRegistry, facilities: Sequence[Facility] = (), cal: Calendar | None = None, *,
                 ig_hard: float = 0.04, ig_target: float = 0.08) -> None:
        self.tax = tax
        self.facilities = tuple(facilities)
        self.cal = cal if cal is not None else Calendar()
        self.ig_hard = ig_hard
        self.ig_target = ig_target
        self._engine_units: dict[str, tuple[UnitId, ...]] = {}
        self._unit_group: dict[str, int] = {}
        self._unit_stocks: dict[str, tuple[F64, F64, F64, F64]] = {}   # nav, nav_rep, unfunded, encumbered
        self._quarter = -1
        self._sold: dict[str, F64] = {}
        self.last: dict[str, F64] = {}
        cf = [g for g in tax.ids() if "treasury" in tax.spec(g).engines]
        self._treasury_col = tax.index(cf[0]) if cf else -1

    # -- set-up (LedgerKernel.init_state) ---------------------------------------------------------------
    def init_state(self, book: BookSnapshot, n_paths: int) -> LedgerState:
        """The as-of ledger state of ``book`` for one block of ``n_paths`` paths."""
        idx = book.unit_index(self.tax)
        by_id = {str(h.holding_id): h for h in book.holdings}
        self._engine_units, self._unit_group, self._unit_stocks = {}, {}, {}
        self._quarter, self._sold = -1, {}
        for uid, eng in zip(idx.unit_ids, idx.engine_of, strict=True):
            h = by_id[str(uid)]
            self._unit_group[str(uid)] = self.tax.index(h.group)
            if eng != "treasury":
                self._engine_units[eng] = self._engine_units.get(eng, ()) + (uid,)
                self._unit_stocks[str(uid)] = tuple(np.full(n_paths, v) for v in (
                    h.nav_reported_bn, h.nav_reported_bn, h.unfunded_bn, h.encumbered_bn))
        treasury = np.zeros(3)
        asset_debt = 0.0
        for h in book.holdings:
            if isinstance(h.terms, TreasuryTerms):
                treasury[("CASH", "UST", "IG").index(h.terms.sleeve)] += h.nav_reported_bn
            if isinstance(h.terms, RealAssetTerms) and h.terms.debt is not None:
                asset_debt += h.terms.debt.balance_bn
        posted_im = _IM_RATE * sum(t.notional_bn for t in book.overlay.trades if t.book is Book.BETA)
        posted_im += 0.5 * book.overlay.policy.opp_im_budget_bn
        nav_total = book.nav_total_reported_bn
        fy0 = self.cal.fiscal_year(0)
        rate = dict(book.owner.history).get(fy0, book.owner.d_prev)
        tre = np.tile(treasury, (n_paths, 1))
        nav_g, rep_g, unf_g, enc = self._aggregate(tre)
        limit = np.array([f.size_bn if (f.status == "signed" and f.committed) else 0.0 for f in self.facilities])
        stage = np.zeros(n_paths, dtype=np.int8)

        def full(x: float) -> F64:
            return np.full(n_paths, float(x))

        return LedgerState(
            m=0, fy=fy0, hqla_unenc_bn=tre @ _TREASURY_HQLA - posted_im, treasury_bn=tre, posted_im_bn=full(posted_im),
            vm_balance_bn=full(0.0), vm_in_transit_bn=full(0.0),
            fac_drawn_bn=np.zeros((n_paths, len(self.facilities))), fac_limit_bn=np.tile(limit, (n_paths, 1)),
            asset_debt_bn=full(asset_debt), unit_debt_bn=full(0.0), encumbrance_bn=enc + posted_im,
            nav_econ_bn=full(nav_total), nav_rep_bn=full(nav_total), liquid_bn=self._liquid(tre, nav_g),
            nav_group_econ=nav_g, nav_group_rep=rep_g, unfunded_group=unf_g, draw_basis_bn=full(nav_total),
            draw_rate=full(rate), payout_ytd_bn=full(0.75 * rate * nav_total),   # three FY2026 instalments paid
            twr_index=full(1.0), twr_peak=full(1.0), cushion=full(0.0), readiness=stage.copy(), event=stage.copy(),
            planning=stage.copy(), playbook=stage.copy(), event_hist=np.zeros((n_paths, 2), dtype=np.int8),
            red_event=np.zeros(n_paths, dtype=bool), payout_short=np.zeros(n_paths, dtype=bool),
            failed=np.zeros(n_paths, dtype=bool), red_month=np.full(n_paths, -1, dtype=np.int16))

    def instalment(self, ls: LedgerState, draw_rate_y: F32, m: int) -> F32:
        """Owner instalment [P] (≤ 0) in month 3t + 2 via ``contracts.rules.instalment_bn``; zero otherwise."""
        q = m // 3
        if m != self.cal.instalment_month(q):
            return np.zeros(ls.cushion.shape[0], dtype=np.float32)
        return instalment_bn(np.asarray(draw_rate_y, dtype=np.float64), ls.draw_basis_bn,
                             self.cal.instalments_left(q), ls.payout_ytd_bn).astype(np.float32)

    def month_weights(self, fs: FlowSlice, m: int) -> F64:
        """Weights [18] by flow type with which ``fs`` books in month ``m`` (intra-quarter profile or 1)."""
        return self._weights(fs, m, m // 3)

    def booked_cash(self, m: int, flows: Sequence[FlowSlice]) -> F64:
        """Cash the month books from ``flows`` before any scale-out (the identity's flow term; for tests)."""
        out = 0.0
        for fs in flows:
            w = self.month_weights(fs, m)
            out = out + (fs.by_group.astype(np.float64)[:, :, _CASH] * w[_CASH]).sum(axis=(1, 2))
        return np.asarray(out, dtype=np.float64)

    # -- Protocol ----------------------------------------------------------------------------------------
    def apply(self, m: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: F32,
              quotes: RecourseAvailability) -> tuple[LedgerState, RecourseOutcome]:
        if m != ls.m:
            raise SchemaError(f"FakeLedger.apply: month {m} does not match the state's instant {ls.m}")
        q = m // 3
        p = ls.cushion.shape[0]
        rec_ids = tuple(str(u) for u in quotes.unit_ids)
        if q != self._quarter:
            self._quarter = q
            self._sold = {}
        sold_before = np.stack([self._sold.get(u, np.zeros(p)) for u in rec_ids], axis=1) if rec_ids \
            else np.zeros((p, 0))
        pos = {u: j for j, u in enumerate(rec_ids)}
        booked = np.zeros(p)
        debt = np.zeros(p)
        debt_types = [int(FlowType.DEBT_DRAW), int(FlowType.DEBT_REPAY)]
        for fs in flows:
            w = self._weights(fs, m, q)
            by_group = fs.by_group.astype(np.float64)
            booked += (by_group[:, :, _CASH] * w[_CASH]).sum(axis=(1, 2))
            debt += (by_group[:, :, debt_types] * w[debt_types]).sum(axis=(1, 2))
            for k, uid in enumerate(fs.recourse_unit_ids):
                j = pos.get(str(uid))
                if j is not None:
                    unit_cash = (fs.by_recourse_unit[:, k, :].astype(np.float64)[:, _CASH] * w[_CASH]).sum(axis=1)
                    booked -= sold_before[:, j] * unit_cash
            self._record_stocks(fs)
        draw64 = np.asarray(draw, dtype=np.float64)
        if draw64.shape != (p,) or (draw64 > 1e-12).any():
            raise SchemaError("FakeLedger.apply: draw is a [P] array of instalments <= 0 (§1.4)")
        treasury = ls.treasury_bn.copy()
        treasury[:, 0] += booked + draw64
        self._reserve_rung(treasury)
        nav_total = self._aggregate(treasury, sold_before, rec_ids)[0].sum(axis=1)
        hqla = treasury @ _TREASURY_HQLA - ls.posted_im_bn
        need = np.maximum(np.maximum(self.ig_hard * nav_total - hqla, -treasury[:, 0]), 0.0)
        fac_drawn = ls.fac_drawn_bn.copy()
        fac_draw = self._facility_rung(m, need, fac_drawn, ls.fac_limit_bn)
        treasury[:, 0] += fac_draw
        sold, proceeds = self._waterfall(need - fac_draw, quotes, sold_before)
        treasury[:, 0] += proceeds.sum(axis=1)
        unpaid = np.where(treasury[:, 0] < 0.0, np.minimum(-treasury[:, 0], -draw64), 0.0)   # instalment unpaid
        treasury[:, 0] += unpaid
        shortfall = np.maximum(-treasury[:, 0], 0.0)          # nothing left to sell, draw or withhold: path fails
        treasury[:, 0] += shortfall
        self.last = {"booked": booked, "draw_requested": draw64, "unpaid": unpaid, "facility_draw": fac_draw,
                     "proceeds": proceeds.sum(axis=1), "shortfall": shortfall}
        for j, u in enumerate(rec_ids):
            self._sold[u] = sold_before[:, j] + sold[:, j]
        nav_g, rep_g, unf_g, enc = self._aggregate(treasury, sold_before + sold, rec_ids)
        nav_total = nav_g.sum(axis=1)
        hqla = treasury @ _TREASURY_HQLA - ls.posted_im_bn
        tier = quotes.tier.astype(np.int64)[None, :]
        red = (sold > 0) & (tier == 2)
        outcome = RecourseOutcome(
            unit_ids=quotes.unit_ids, sold_frac=sold.astype(np.float32), month=np.where(sold > 0, m, -1).astype(np.int16),
            proceeds_bn=proceeds, red=red,
            reason=np.where(sold > 0, np.where(tier == 2, SaleReason.RECOURSE_RED, SaleReason.RECOURSE_AMBER),
                            SaleReason.NONE).astype(np.int8))
        paid = draw64 + unpaid
        payout_short = ls.payout_short | (unpaid > 1e-12)
        event = np.where(payout_short, CFPStage.RED,
                         np.where(hqla < self.ig_hard * nav_total, CFPStage.AMBER, CFPStage.GREEN)).astype(np.int8)
        readiness = np.where(hqla < self.ig_target * nav_total, CFPStage.AMBER, CFPStage.GREEN).astype(np.int8)
        new_red = red.any(axis=1)
        twr = ls.twr_index * (nav_total - paid) / np.maximum(ls.nav_econ_bn, 1e-12)
        fy = self.cal.fiscal_year(min((m + 1) // 3, self.cal.n_quarters - 1))
        rollover = fy != ls.fy
        state = LedgerState(
            m=m + 1, fy=fy, hqla_unenc_bn=hqla, treasury_bn=treasury, posted_im_bn=ls.posted_im_bn.copy(),
            vm_balance_bn=ls.vm_balance_bn.copy(), vm_in_transit_bn=ls.vm_in_transit_bn.copy(),
            fac_drawn_bn=fac_drawn, fac_limit_bn=ls.fac_limit_bn.copy(),
            asset_debt_bn=ls.asset_debt_bn.copy(), unit_debt_bn=np.maximum(ls.unit_debt_bn + debt, 0.0),
            encumbrance_bn=enc + ls.posted_im_bn, nav_econ_bn=nav_total, nav_rep_bn=rep_g.sum(axis=1),
            liquid_bn=self._liquid(treasury, nav_g), nav_group_econ=nav_g, nav_group_rep=rep_g, unfunded_group=unf_g,
            draw_basis_bn=np.where(rollover, nav_total, ls.draw_basis_bn), draw_rate=ls.draw_rate.copy(),
            payout_ytd_bn=np.where(rollover, 0.0, ls.payout_ytd_bn - paid), twr_index=twr,
            twr_peak=np.maximum(ls.twr_peak, twr),
            cushion=(nav_total - 0.9 * ls.draw_basis_bn) / np.maximum(nav_total, 1e-12), readiness=readiness,
            event=event, planning=np.maximum(readiness, event), playbook=event.copy(),
            event_hist=np.stack([ls.event_hist[:, 1], ls.event], axis=1).astype(np.int8),
            red_event=ls.red_event | new_red, payout_short=payout_short, failed=ls.failed | (shortfall > 1e-12),
            red_month=np.where((ls.red_month < 0) & new_red, m, ls.red_month).astype(np.int16))
        return state, outcome

    def row_slacks(self, ls: LedgerState) -> dict[RowKey, F32]:
        w = ls.nav_econ_bn
        return {
            RowKey(family=RowFamily.T2_IG_HARD): (ls.hqla_unenc_bn - self.ig_hard * w).astype(np.float32),
            RowKey(family=RowFamily.T2_IG_TARGET): (ls.hqla_unenc_bn - self.ig_target * w).astype(np.float32),
            RowKey(family=RowFamily.T5_DEBT): (0.15 * w - ls.fac_drawn_bn.sum(axis=1) - ls.unit_debt_bn
                                               ).astype(np.float32),
        }

    def stress_replica(self, ls0: LedgerState, stress: StressSpec) -> StressReport:
        """A linear 24-month T4′-style ladder on the group aggregates (illustrative only; WP-13 owns the replica)."""
        conv = stress.conventions
        h = np.arange(1, stress.months + 1, dtype=np.float64)
        zero = np.zeros_like(ls0.nav_econ_bn)
        dist, amber, red, public = zero.copy(), zero.copy(), zero.copy(), zero.copy()
        for g in self.tax.ids():
            spec, nav = self.tax.spec(g), ls0.nav_group_econ[:, self.tax.index(g)]
            if spec.kind == "private":
                dist += nav * (0.20 * stress.dist_mult if spec.fund_distribution_stress else 0.08)
            if spec.kind == "public":
                public += nav
            if spec.red_tier:
                red += nav
            elif spec.amber_tier:
                amber += nav
        outflow = (conv.draw_rate_in_stress * ls0.draw_basis_bn
                   + stress.base_call_rate_a * stress.call_mult * ls0.unfunded_group.sum(axis=1) - dist) / 12.0
        nco = outflow[:, None] * h[None, :]
        t_cap = np.repeat(ls0.hqla_unenc_bn[:, None], h.size, axis=1)
        tp = t_cap + public[:, None] * (1.0 + stress.equity_shock) * _LO_HQLA_SHARE * np.minimum(1.0, h / 3.0)
        tpf = tp + ls0.fac_limit_bn.sum(axis=1)[:, None] * conv.revolver_credit * (h >= conv.revolver_from_month)
        tpfa = tpf + 0.25 * amber[:, None] * np.minimum(1.0, h / 6.0)
        cbc = {RecourseTier.T: t_cap, RecourseTier.TP: tp, RecourseTier.TPF: tpf, RecourseTier.TPFA: tpfa,
               RecourseTier.ALL: tpfa + 0.10 * red[:, None] * np.minimum(1.0, h / 12.0)}
        floor = self.ig_hard * ls0.nav_econ_bn[:, None]
        survival = {}
        for tier, cap in cbc.items():
            breach = (nco + floor) > cap
            survival[tier] = np.where(breach.any(axis=1), breach.argmax(axis=1) + 1, 25).astype(np.int16)
        headroom = tpf - nco - floor
        return StressReport(spec_hash=content_hash(stress), headroom_bn=headroom, nco_bn=nco, cbc_bn=cbc,
                            survival_months=survival, gap_bn=(nco + floor - tp).max(axis=1),
                            d0_bn=np.maximum(0.0, -headroom.min(axis=1)))

    # -- internals -----------------------------------------------------------------------------------------
    def _weights(self, fs: FlowSlice, m: int, q: int) -> F64:
        if fs.clock is Clock.QUARTERLY:
            if fs.t != q:
                raise SchemaError(f"FakeLedger: quarterly FlowSlice of quarter {fs.t} applied in month {m}")
            return np.array([intra_quarter_profile(ft, Clock.QUARTERLY)[m - 3 * q] for ft in FlowType])
        if fs.t != m:
            raise SchemaError(f"FakeLedger: monthly FlowSlice of month {fs.t} applied in month {m}")
        return np.ones(_F)

    def _record_stocks(self, fs: FlowSlice) -> None:
        uids = self._engine_units.get(fs.engine_id)
        if uids is None or fs.nav_econ.shape[1] != len(uids):
            raise SchemaError(f"FakeLedger: {fs.engine_id} stocks do not match its units in unit_index() order")
        for k, uid in enumerate(uids):
            self._unit_stocks[str(uid)] = tuple(a[:, k].astype(np.float64)
                                                for a in (fs.nav_econ, fs.nav_rep, fs.unfunded, fs.encumbered))

    def _aggregate(self, treasury: F64, sold: F64 | None = None,
                   rec_ids: Sequence[str] = ()) -> tuple[F64, F64, F64, F64]:
        """Group stocks [P, G] (NAV, reported NAV, unfunded) and total encumbrance [P]; units sold by the waterfall
        this quarter count net of the sold fraction until their engines apply the outcome."""
        p, g = treasury.shape[0], len(self.tax)
        keep = {u: 1.0 - sold[:, j] for j, u in enumerate(rec_ids)} if sold is not None else {}
        nav_g, rep_g, unf_g, enc = np.zeros((p, g)), np.zeros((p, g)), np.zeros((p, g)), np.zeros(p)
        for uid, (nav, rep, unf, e) in self._unit_stocks.items():
            k = keep.get(uid, 1.0)
            col = self._unit_group[uid]
            nav_g[:, col] += k * nav
            rep_g[:, col] += k * rep
            unf_g[:, col] += k * unf
            enc += k * e
        if self._treasury_col >= 0:
            nav_g[:, self._treasury_col] += treasury.sum(axis=1)
            rep_g[:, self._treasury_col] += treasury.sum(axis=1)
        return nav_g, rep_g, unf_g, enc

    def _liquid(self, treasury: F64, nav_g: F64) -> F64:
        public = [self.tax.index(g) for g in self.tax.ids("public")]
        return treasury.sum(axis=1) + (nav_g[:, public].sum(axis=1) if public else 0.0)

    @staticmethod
    def _reserve_rung(treasury: F64) -> None:
        """Reserve rung: cover negative cash from the UST, then the IG sleeve, at market value (value-neutral)."""
        for sleeve in (1, 2):
            move = np.minimum(np.maximum(-treasury[:, 0], 0.0), treasury[:, sleeve])
            treasury[:, sleeve] -= move
            treasury[:, 0] += move

    def _facility_rung(self, m: int, need: F64, fac_drawn: F64, fac_limit: F64) -> F64:
        """Facility rung: draw signed, committed facilities from their availability month, in order (in place)."""
        total = np.zeros(need.shape[0])
        for k, f in enumerate(self.facilities):
            if m < f.available_from_month:
                continue
            draw = np.minimum(np.maximum(need - total, 0.0), np.maximum(fac_limit[:, k] - fac_drawn[:, k], 0.0))
            fac_drawn[:, k] += draw
            total += draw
        return total

    def _waterfall(self, need: F64, quotes: RecourseAvailability, sold_before: F64) -> tuple[F64, F64]:
        """Amber, then red sales at the quoted bids within the quarter's remaining depth. Fractions are rounded to
        float32 first, so the ledger books exactly what ``RecourseOutcome.sold_frac`` tells the engines."""
        p, n = sold_before.shape
        sold, proceeds = np.zeros((p, n)), np.zeros((p, n))
        need = np.maximum(need, 0.0)
        if n == 0 or not (need > 0).any():
            return sold, proceeds
        for j in sorted(range(n), key=lambda j: (int(quotes.tier[j]), j)):     # amber (1) before red (2)
            stocks = self._unit_stocks.get(str(quotes.unit_ids[j]))
            if stocks is None:
                continue
            value = stocks[0] * quotes.bid_frac[:, j].astype(np.float64)
            room = np.maximum(quotes.depth_frac[:, j].astype(np.float64) - sold_before[:, j], 0.0)
            frac = np.where((need > 0) & (value > 0), np.minimum(room, need / np.maximum(value, 1e-300)), 0.0)
            sold[:, j] = _f32_within(frac, room)
            proceeds[:, j] = sold[:, j] * value
            rem = need - proceeds[:, j]                                  # > 0 only when the depth capped the sale
            need = np.where(rem <= 1e-12 * np.maximum(need, 1.0), 0.0, rem)
        return sold, proceeds


def _f32_within(frac: F64, room: F64) -> F64:
    """``frac`` rounded up to float32 (a sale covers its whole need, leaving no rounding residue for the next
    unit), but never above ``room`` (then the largest float32 ≤ room); returned as float64."""
    up = frac.astype(np.float32)
    up = np.where(up.astype(np.float64) < frac, np.nextafter(up, np.float32(np.inf)), up)
    cap = room.astype(np.float32)
    cap = np.where(cap.astype(np.float64) > room, np.nextafter(cap, np.float32(0.0)), cap)
    return np.where(up.astype(np.float64) > room, cap, up).astype(np.float64)


# ------------------------------------------------------------------------------------- beliefs, draws, filter
_RF_A: Final = 0.0389          # SOFR at the SYNTHETIC as-of (§1.2 example sofr_a)
_ERP_REF_A: Final = 0.045      # reference equity risk premium of the fake decomposition [I]


def fake_beliefs(book: BookSnapshot) -> BeliefSet:
    """A deterministic ``BeliefSet`` for every unit of ``book`` (S-ADR-28 decomposition; SYNTHETIC)."""
    reg = GroupRegistry.for_version(book.taxonomy_version)
    idx = book.unit_index(reg)
    by_id = {str(h.holding_id): h for h in book.holdings}
    hs = [by_id[str(u)] for u in idx.unit_ids]
    alpha = np.array([_alpha_a(h) for h in hs])
    beta = np.array([_KIND_BETA[h.unit_kind] for h in hs])
    bench = np.log1p(_RF_A) + beta * _ERP_REF_A
    mu = bench + alpha
    sigma = np.array([_KIND_SIGMA[h.unit_kind] for h in hs])
    z80 = 1.2815515655446004
    g = len(reg)
    meta = BeliefMeta(asof=book.asof, fbe_version="testing.fake_beliefs/1", prior_hash=content_hash("fake-prior"),
                      inputs_hash=book.content_hash, frozen_optimizer_outputs_hash=content_hash("no-prior-quarter"),
                      data_class=book.data_class, content_hash=content_hash({"book": book.content_hash, "alpha": alpha}))
    return BeliefSet(
        meta=meta, unit_ids=idx.unit_ids, alpha_a=alpha, benchmark_id=tuple(benchmark_of(h) for h in hs),
        beta_hat=beta, bench_ref_a=bench, mu_total_a=mu, sigma_hat=sigma,
        band80=np.stack([mu - z80 * sigma, mu + z80 * sigma], axis=1), mu_p10=mu - z80 * sigma - 2 * 0.01,
        weights=np.tile([0.4, 0.2, 0.3, 0.1], (len(hs), 1)), market_anchor=mu.copy(),
        has_market=np.zeros(len(hs), dtype=bool), nowcast_nav_bn=np.array([h.nav_reported_bn for h in hs]),
        flags=np.zeros(len(hs), dtype=np.uint32), p_achieved=np.tile([0.5, 0.6], (len(hs), 1)),
        group_bias_mean=np.zeros(g), group_bias_sd=np.full(g, 0.01), kappa=np.full(g, 1.75))


def fake_belief_draws(bs: BeliefSet, world: WorldSpec, n_paths: int) -> BeliefDraws:
    """``BeliefDraws`` frozen at α̂: α₀ = α̂/4 on every path, zero bias, no GP effects, no learning noise (the
    no-learning variant whose engines reproduce α̂ exactly; S-ADR-28)."""
    if not 1 <= n_paths <= MAX_BLOCK_PATHS:
        raise SchemaError(f"fake_belief_draws: n_paths must lie in [1, {MAX_BLOCK_PATHS}]")
    a_q = bs.alpha_a / 4.0
    u, g = len(bs.unit_ids), bs.kappa.shape[0]
    return BeliefDraws(world_id=world.world_id, path_offset=0, unit_ids=bs.unit_ids, gp_ids=(),
                       alpha0_q=np.tile(a_q.astype(np.float32), (n_paths, 1)),
                       group_bias_q=np.zeros((n_paths, g), dtype=np.float32),
                       gp_effect_q=np.zeros((n_paths, 0), dtype=np.float32), m_q=a_q.copy(), phi=np.zeros(u),
                       eta_sd_q=np.zeros(u))


def fake_filter_params() -> StressFilterParams:
    """Gaussian-HMM parameters (CALM, ELEVATED, CRISIS) on ``FILTER_OBSERVABLES`` [I] for ``fake_filter``."""
    means = [[0.006, -1.95, 0.000, 0.0000], [-0.002, -1.55, 0.004, -0.0005], [-0.030, -0.95, 0.015, -0.0020]]
    sds = [[0.030, 0.25, 0.004, 0.0020], [0.045, 0.25, 0.005, 0.0025], [0.070, 0.30, 0.008, 0.0030]]
    covs = [[[s[i] ** 2 if i == j else 0.0 for j in range(4)] for i in range(4)] for s in sds]
    transmat = [[0.96, 0.03, 0.01], [0.10, 0.85, 0.05], [0.03, 0.12, 0.85]]
    startprob = [0.80, 0.15, 0.05]
    body = dict(means=means, covs=covs, transmat=transmat, startprob=startprob, version="testing.fake_filter/1")
    return StressFilterParams(means=means, covs=covs, transmat=transmat, startprob=startprob,
                              fitted_through=date(2026, 8, 31), ab=(-2.0, 1.2), base_rate=0.17,
                              version_hash=content_hash(body))


def _filter_observables(factors: F32, factor_names: Sequence[str], panel_tail: F64 | None) -> F64:
    names = list(factor_names)
    need = ("us_eq", "short_rate", "log_rv", "ebp", "ust10y")
    missing = [n for n in need if n not in names]
    if missing:
        raise SchemaError(f"fake_filter: the cube lacks the filter's factors {missing}")
    x = np.asarray(factors, dtype=np.float64)
    col = {n: names.index(n) for n in need}
    p, m, _ = x.shape
    prev = np.asarray(panel_tail, dtype=np.float64) if panel_tail is not None else None
    ebp, ust = x[:, :, col["ebp"]], x[:, :, col["ust10y"]]
    ebp_prev0 = np.full(p, prev[0]) if prev is not None and prev.size >= 1 else ebp[:, 0]
    ust_prev0 = np.full(p, prev[1]) if prev is not None and prev.size >= 2 else ust[:, 0]
    obs = np.empty((p, m, 4))
    obs[:, :, 0] = x[:, :, col["us_eq"]] - x[:, :, col["short_rate"]] / 12.0
    obs[:, :, 1] = x[:, :, col["log_rv"]]
    obs[:, :, 2] = np.concatenate([ebp_prev0[:, None], ebp[:, :-1]], axis=1)
    obs[:, :, 3] = np.diff(np.concatenate([ust_prev0[:, None], ust], axis=1), axis=1)
    return obs


def fake_filter(params: StressFilterParams | None = None) -> Callable[..., F32]:
    """Stand-in for ``state.simulate_filter`` (WP-06 before WP-07): returns
    ``simulate_filter(factors, factor_names, params=None, panel_tail=None) -> F32 [P, M, 3]``.

    A forward-only Gaussian-HMM filter on the cube's own observables (excess us_eq return, log_rv, ebp lagged one
    month, Δust10y; §4.9). ``panel_tail`` (optional) holds the as-of month's ``(ebp, ust10y)`` for the first lag.
    Appending months never changes earlier posteriors (no look-ahead).
    """
    default = params if params is not None else fake_filter_params()

    def simulate_filter(factors: F32, factor_names: Sequence[str], params: StressFilterParams | None = None,
                        panel_tail: F64 | None = None) -> F32:
        prm = params if params is not None else default
        obs = _filter_observables(factors, factor_names, panel_tail)
        means = np.asarray(prm.means, dtype=np.float64)
        covs = np.asarray(prm.covs, dtype=np.float64)
        trans = np.asarray(prm.transmat, dtype=np.float64)
        prec = np.linalg.inv(covs)
        logdet = np.linalg.slogdet(covs)[1]
        diff = obs[:, :, None, :] - means[None, None, :, :]
        loglik = -0.5 * (np.einsum("pmkd,kde,pmke->pmk", diff, prec, diff) + logdet[None, None, :])
        p, m, k = loglik.shape
        post = np.empty((p, m, k))
        alpha = np.tile(np.asarray(prm.startprob, dtype=np.float64), (p, 1))
        for t in range(m):
            prior = alpha if t == 0 else alpha @ trans
            lw = np.log(np.maximum(prior, 1e-300)) + loglik[:, t, :]
            lw -= lw.max(axis=1, keepdims=True)
            w = np.exp(lw)
            alpha = w / w.sum(axis=1, keepdims=True)
            post[:, t, :] = alpha
        out = post.astype(np.float32)
        return out / out.sum(axis=2, keepdims=True)

    return simulate_filter


def fake_owner_draws(cube: ScenarioCube, rate: float = 0.075) -> ScenarioCube:
    """Stand-in for ``owner.attach_draws``: the cube with a flat ``draw_rate`` of ``rate`` a year in every fiscal
    year (Y = 11) and no overrides. The scenario identity (``meta.checksum``) is unchanged."""
    if not 0.05 <= rate <= 0.10:
        raise SchemaError(f"fake_owner_draws: rate {rate} outside the owner's 5-10% band")
    p = cube.meta.n_paths
    return replace(cube, draw_rate=np.full((p, 11), rate, dtype=np.float32),
                   draw_override=np.zeros((p, 11), dtype=bool))


def fake_draw_block(base: bytes, requests: Sequence[NoiseRequest], paths: np.ndarray) -> NoiseSlice:
    """Stand-in for ``rng.draw_block`` (same signature): uniforms in [0, 1) from numpy's Philox keyed by
    SHA-256(base ‖ source). Deterministic, but not the §1.7 counter layout (WP-02 owns that)."""
    p = np.asarray(paths)
    u: dict[str, F64] = {}
    for req in requests:
        n_ent = 1 if req.entity_ids is None else len(req.entity_ids)
        digest = hashlib.sha256(bytes(base) + req.source.encode("utf-8")).digest()
        key = np.frombuffer(digest[:16], dtype=np.uint64).copy()
        raw = np.random.Philox(key=key).random_raw(int(p.size) * len(req.months) * n_ent * req.slots)
        u[req.source] = ((raw >> np.uint64(11)).astype(np.float64) * 2.0 ** -53).reshape(
            p.size, len(req.months), n_ent, req.slots)
    return NoiseSlice(requests=tuple(requests), u=u)


def fake_observables(t: int, ls: LedgerState, n_units: int) -> Observables:
    """Lagged-looking observables built from a ledger state (stand-in for ``core.sim.build_observables``)."""
    p, g = ls.nav_group_econ.shape
    w = np.maximum(ls.nav_econ_bn, 1e-12)
    return Observables(
        t=t, values={"liquid_share": (ls.liquid_bn / w).astype(np.float32), "cushion": ls.cushion.astype(np.float32),
                     "event_stage": ls.event.astype(np.float32)},
        unit_values={"bid_ce": np.full((p, n_units), 0.9, dtype=np.float32)},
        group_values={"unfunded_share": (ls.unfunded_group / w[:, None]).astype(np.float32)})


# --------------------------------------------------------------------------------------- policy and factory
class FakePolicy:
    """A HOLD policy (implements ``contracts.ports.Policy``) with optional scheduled discretionary sells."""

    def __init__(self, ctx: PolicyContext, n_paths: int, *, n_lots: int, n_facilities: int,
                 sells: Mapping[int, Mapping[str, float]] | None = None) -> None:
        self.ctx = ctx
        self.n_paths = n_paths
        self.n_lots = n_lots
        self.n_facilities = n_facilities
        self.sells = {int(q): dict(v) for q, v in (sells or {}).items()}
        self.policy_ref = PolicyRef(kind="native", name="HOLD", params_hash=content_hash(self.sells))
        self._col = {str(u): j for j, u in enumerate(ctx.idx.unit_ids)}

    def act(self, q: int, obs: Observables) -> ActionSlice:
        if not obs.world_hidden:
            raise SchemaError("FakePolicy: observables must hide the world (TR2)")
        act = ActionSlice.empty(q, self.n_paths, len(self.ctx.idx.unit_ids), len(self.ctx.tax), self.n_lots,
                                self.n_facilities, recourse_order=self.ctx.recourse.codes())
        for uid, frac in self.sells.get(q, {}).items():
            act.sell_frac[:, self._col[uid]] = np.float32(frac)
            act.sell_reason[:, self._col[uid]] = np.int8(SaleReason.DISCRETIONARY)
        return act


class FakeEngineFactory:
    """Implements ``contracts.ports.EngineFactory``: fake engines and ledger; the world's overrides are hashed into
    the effective config of the module they target (S-ADR-43)."""

    def __init__(self, owner_cfg: OwnerConfig) -> None:
        self.owner_cfg = owner_cfg

    def build(self, book: BookSnapshot, world: WorldSpec) -> EngineBundle:
        engines = tuple(fake_engines(book))
        ledger = FakeLedger(GroupRegistry.for_version(book.taxonomy_version), book.facilities)
        modules = sorted({e.engine_id.split(".")[0] for e in engines} | {"ledger", "owner", "policy", "scen"})
        hashes = {mod: content_hash({"module": mod, "base": "testing.fake/1",
                                     "overrides": [o for o in world.overrides if o.target_module == mod]})
                  for mod in modules}
        return EngineBundle(engines=engines, ledger=ledger, owner_cfg=self.owner_cfg, policy_wrappers=(),
                            effective_config_hashes=MappingProxyType(hashes))


# ---------------------------------------------------------------------------------------------- LLM backend
class FakeLLMBackend:
    """Implements ``contracts.ports.LLMBackend`` from canned outputs (no network; ``ReplayMiss`` when absent)."""

    def __init__(self, family: ModelFamily = ModelFamily.A, *, outputs: Mapping[type[BaseModel], BaseModel] | None = None,
                 tool_calls: Sequence[tuple[str, Mapping[str, Any]]] = ()) -> None:
        self.family = family
        self.outputs = dict(outputs or {})
        self.tool_calls = tuple(tool_calls)

    def _record(self, req: LLMRequest, response: Any) -> LLMCallRecord:
        prompt = content_hash({"role": req.role, "model": req.model, "system": req.system, "messages": req.messages,
                               "tools": [t.name for t in req.tools]})
        return LLMCallRecord(call_id=f"fake-{prompt[7:19]}", role=req.role, requested_model=req.model,
                             served_model="fake-backend", fallback_event=False, prompt_hash=prompt,
                             response_hash=content_hash(response), input_tokens=0, output_tokens=0,
                             cache_read_tokens=0, cost_usd=0.0, stop_reason="end_turn", latency_s=0.0,
                             replay_key=prompt)

    def parse(self, req: LLMRequest, output_model: type[BaseModel]) -> LLMResponse:
        if output_model not in self.outputs:
            raise ReplayMiss(f"FakeLLMBackend: no canned {output_model.__name__} output", {"role": str(req.role)})
        parsed = self.outputs[output_model]
        content = ({"type": "text", "text": parsed.model_dump_json()},)
        return LLMResponse(content=content, parsed=parsed, stop_reason="end_turn", served_model="fake-backend",
                           usage=MappingProxyType({"input_tokens": 0, "output_tokens": 0}),
                           record=self._record(req, content))

    def run_tools(self, req: LLMRequest, tools: Sequence[ToolDef], executor: ToolExecutor) -> LLMResponse:
        names = {t.name for t in tools}
        blocks: list[dict[str, Any]] = []
        for i, (name, tool_input) in enumerate(self.tool_calls):
            if name not in names:
                raise ReplayMiss(f"FakeLLMBackend: canned call to {name!r} is not in the tool list")
            blocks.append(dict(executor(f"toolu_fake_{i:02d}", name, tool_input)))
        content = tuple(blocks) + ({"type": "text", "text": SYNTHETIC_FOOTER},)
        return LLMResponse(content=content, parsed=None, stop_reason="end_turn", served_model="fake-backend",
                           usage=MappingProxyType({"input_tokens": 0, "output_tokens": 0}),
                           record=self._record(req, content))


# -------------------------------------------------------------------------------------------- fake evaluator
class FakeRobustnessCard(ContractModel):
    """Placeholder of ``robust.RobustnessCard`` (WP-22) returned by ``FakeEvaluator.robustness_card``."""

    ids: tuple[str, ...]
    data_class: DataClass = DataClass.SYNTHETIC


class FakeSimmResult(ContractModel):
    """Placeholder of ``overlay.SimmResult`` (WP-12)."""

    im_bn: float
    data_class: DataClass = DataClass.SYNTHETIC


class FakeOVReport(ContractModel):
    """Placeholder of ``overlay.OVReport`` (WP-12)."""

    ov1_ok: bool
    ov2_ok: bool
    ov3_ok: bool
    data_class: DataClass = DataClass.SYNTHETIC


# Every typed method of contracts.ports.EvaluatorPort (§7.4), in Protocol order.
EVALUATOR_METHODS: Final[tuple[str, ...]] = (
    "state_snapshot", "phase1_restore", "compile_spec", "evaluate_policy", "price_actions", "optimize_h",
    "evaluate_scenario", "reverse_stress", "implied_actions", "ep_condition", "evsi_crossfit", "flip_thresholds",
    "robustness_card", "bridge_card", "group_envelopes", "overlay_offset_card", "attribute", "price_trade",
    "crif_sensitivities", "simm_like", "greek_offsets", "hybrid_quote_check", "get_metric", "list_metrics",
    "get_provenance", "validate_claims", "log_assumption", "escalate")


class FakeEvaluator:
    """Implements ``contracts.ports.EvaluatorPort`` with fixed, schema-valid SYNTHETIC answers (§7.4).

    ``calls`` records every method called (in order); ``evaluate_policy`` counts against ``budget``.
    """

    def __init__(self, *, budget: int = 650, group: GroupId | None = None) -> None:
        self.budget = budget
        self.calls: list[str] = []
        self.group = group if group is not None else GroupId("PE")

    def _call(self, name: str) -> None:
        self.calls.append(name)

    def _envelope(self) -> Envelope:
        return Envelope(group=self.group, row="T4P:h=07", value_bn=2.0, range_bn=(1.5, 2.5), dual=0.011,
                        ranging_bn=(1.0, 3.0), elasticity_bn_per_100bp=0.2, delivery_share=None,
                        priced_on=PricedOn.FEASIBLE, recovery_hash=None)

    def _ftp(self) -> FTPPoint:
        return FTPPoint(tenor_q=4, decision_q=0.0028, published_q=0.0028, band_q=(0.0025, 0.0031),
                        components={RowFamily.T4P: 0.0028}, priced_on=PricedOn.FEASIBLE, recovery_hash=None)

    def _lambda(self) -> dict[StressState, float]:
        return {StressState.CALM: 0.001, StressState.ELEVATED: 0.004, StressState.CRISIS: 0.02}

    def state_snapshot(self, req: StateSnapshotIn) -> StateCard:
        self._call("state_snapshot")
        cfp = CFPReading(readiness=CFPStage.GREEN, event=CFPStage.GREEN, planning=CFPStage.GREEN,
                         playbook=CFPStage.GREEN, indicators={"sh_tp_months": 17.0, "lcr30": 1.4}, triggers=())
        return StateCard(cfp=cfp, F_t=0.10, e0=(0.03, 0.05, 0.87, 0.05), z0=(0.15, 0.0, 0.15, 0.0, 0.0, 0.70),
                         draw_12m_bn=(9.9, 10.8), t4p_survival_months={t: 17 for t in RecourseTier},
                         lambda_spot=self._lambda(), plane=EvidencePlane.EXPLORATORY, refs=(_ref("state_card"),))

    def phase1_restore(self, req: Phase1In) -> Phase1Card:
        self._call("phase1_restore")
        tiers = (TierSummary(tier=1, u_star_bn=0.0, iis=(), levers_at_cap=()),)
        return Phase1Card(by_scenario={s: tiers for s in ConsentScenario}, mode=ContractMode.NORMAL, d0_bn=0.0,
                          glide=None, pricing_scenario=req.scenario or ConsentScenario.R1)

    def compile_spec(self, spec: PolicySpec) -> TypeReport:
        self._call("compile_spec")
        return TypeReport(passed=True, errors=())

    def evaluate_policy(self, req: EvalRequest) -> EvalResultAgentView:
        self._call("evaluate_policy")
        self.budget -= 1
        return EvalResultAgentView(request_id=req.request_id, correct=True, delta_psi_bucket="0..3",
                                   gate_categories=(), promotable=False, budget_left=self.budget)

    def price_actions(self, package: ActionPackage) -> PackagePrice:
        self._call("price_actions")
        return PackagePrice(robust_rc_bucket="0..3", dominated=False)

    def optimize_h(self, req: OptimizeHIn) -> HSummary:
        self._call("optimize_h")
        hold = LensAction(unit_id=None, group=self.group, lens=Lens.PACE, instrument="pace", size_bn=0.0,
                          exposure_delta_bn=0.0, financing_delta_bn=0.0, cash_out_bn=0.0)
        return HSummary(root_actions=(hold,), lambda_spot=self._lambda(), ftp=(self._ftp(),),
                        envelopes=(self._envelope(),), gamma_status="certified", priced_on=PricedOn.FEASIBLE,
                        run_ref=_ref("h_summary"))

    def evaluate_scenario(self, spec: ScenarioSpecDraft) -> ScenarioResult:
        self._call("evaluate_scenario")
        return ScenarioResult(dp_red_bucket="0..1pp", binding_rows=("T4P:h=07",), kl=min(spec.kl_bound, 0.1))

    def reverse_stress(self, req: ReverseStressIn) -> ReverseStressResult:
        self._call("reverse_stress")
        return ReverseStressResult(kl=0.2, tilt_ref=_ref("reverse_stress"), ranking=(("hy_spread", 0.4),))

    def implied_actions(self, req: ImpliedIn) -> ImpliedActionCard:
        self._call("implied_actions")
        return ImpliedActionCard(seat_id=req.seat_id, item_id=req.item_id, action="HOLD",
                                 regret_bp_by_option={"STATUS_QUO": 0.0, "RECOMMENDED": 1.5},
                                 ref=_ref("implied_actions", f"/{req.seat_id}"))

    def ep_condition(self, req: EPIn) -> EPResult:
        self._call("ep_condition")
        return EPResult(weights_ref=_ref("ep_weights"), kl=0.05, ess=8500.0, max_ratio=2.1,
                        effective_views=req.views, flags=("inform",))

    def evsi_crossfit(self, req: EVSIIn) -> EVSIResult:
        self._call("evsi_crossfit")
        return EVSIResult(lb80_usd_m=0.0, mean_usd_m=3.0, folds=2, cost_of_delay_usd_m=5.0)

    def flip_thresholds(self, req: FlipIn) -> FlipThresholds:
        self._call("flip_thresholds")
        return FlipThresholds(reservation_price=0.877, breakeven_fwd_return_a=0.06, breakeven_ell_a=0.011,
                              one_off_premium=None)

    def robustness_card(self, req: CardIdsIn) -> BaseModel:
        self._call("robustness_card")
        return FakeRobustnessCard(ids=req.ids)

    def bridge_card(self, req: CardIdsIn) -> BridgeCard:
        self._call("bridge_card")
        return BridgeCard(world_id="M1", beta_return_a=0.07, levers=(LeverLine(name="pe_selection", weight=0.19,
                                                                               alpha_star_a=0.015, sd_a=0.01,
                                                                               benchmark="pe_buyout"),),
                          overlay_sr=0.15, overlay_sigma_a=0.011, leverage=1.0, drags={"fees": 0.004},
                          arith_mean_a=0.0917, geom_mean_a=0.0839, gap_to_target_pp=-1.6, p_mu_ge_target=(0.39, 0.40),
                          p_10y_ge_target=0.35, break_evens={"pe_selection": 0.04}, verdict="Stretch",
                          data_class=DataClass.SYNTHETIC)

    def group_envelopes(self, req: CardIdsIn) -> EnvelopeSummary:
        self._call("group_envelopes")
        return EnvelopeSummary(envelopes=(self._envelope(),), pool_bn={"T4P": 13.9})

    def overlay_offset_card(self, req: CardIdsIn) -> OffsetCard:
        self._call("overlay_offset_card")
        row = OffsetRow(stress="equity_minus_30", pnl_tail_bn=1.2, pnl_opp_bn=-0.4, offset_ratio=0.33,
                        nv_eq_economic=0.8, nv_simm=0.9, im_by_csa_bn={}, im_saving_priced_bn=0.19)
        return OffsetCard(rows=(row,), stress_coverage_ratio=1.0)

    def attribute(self, req: AttributeIn) -> AttributionCard:
        self._call("attribute")
        return AttributionCard(kind=req.kind, components={"overlay": (1.0, 0.5)}, residual=0.0,
                               established={"overlay": False}, ref=_ref("attribution"))

    def price_trade(self, structure: OverlayStructure) -> TradePrice:
        self._call("price_trade")
        return TradePrice(value_bn=sum(leg.notional_bn for leg in structure.legs) * 0.01, greeks_ref=_ref("greeks"))

    def crif_sensitivities(self, structure: OverlayStructure) -> tuple[CRIFRow, ...]:
        self._call("crif_sensitivities")
        return ()

    def simm_like(self, structure: OverlayStructure) -> BaseModel:
        self._call("simm_like")
        return FakeSimmResult(im_bn=0.05 * sum(abs(leg.notional_bn) for leg in structure.legs))

    def greek_offsets(self, structure: OverlayStructure) -> BaseModel:
        self._call("greek_offsets")
        return FakeOVReport(ov1_ok=True, ov2_ok=True, ov3_ok=True)

    def hybrid_quote_check(self, structure: OverlayStructure) -> HybridCheck:
        self._call("hybrid_quote_check")
        return HybridCheck(implied_corr_spread=0.05, q_vs_p_pass=True, accepted=True)

    def get_metric(self, req: MetricQueryIn) -> MetricInstance:
        self._call("get_metric")
        return MetricInstance(metric_id=req.metric_id, run_id=req.run_id or FAKE_RUN_ID, value=0.009, unit="prob",
                              plane=req.plane or EvidencePlane.EXPLORATORY, scenario_hash=content_hash("fake-cube"),
                              data_class=DataClass.SYNTHETIC)

    def list_metrics(self, req: MetricListIn) -> tuple[MetricId, ...]:
        self._call("list_metrics")
        return tuple(m for m in (MetricId("tier1.t6.cp_upper@v1"), MetricId("liquidity.t4p.survival_months@v1"))
                     if m.startswith(req.prefix))

    def get_provenance(self, req: ProvenanceQueryIn) -> ProvenanceNode:
        self._call("get_provenance")
        return ProvenanceNode(ref=req.ref, kind="fake", parents=(), hash=content_hash(str(req.ref)))

    def validate_claims(self, req: ValidateClaimsIn) -> ValidationReport:
        self._call("validate_claims")
        return ValidationReport(passed=True, coverage=1.0, errors=())

    def log_assumption(self, entry: AssumptionEntry) -> Ack:
        self._call("log_assumption")
        return Ack(accepted=True, row_hash=content_hash(entry))

    def escalate(self, e: Escalation) -> Ack:
        self._call("escalate")
        return Ack(accepted=True, row_hash=content_hash(e))
