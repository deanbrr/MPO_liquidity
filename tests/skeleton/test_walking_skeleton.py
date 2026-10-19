"""The walking skeleton (BUILD_SPEC v1.1 §4.5, §0.1 item 3, BUILD-11; owner WP-03): the gate for tagging
``contracts-v1.0``.

SYNTHETIC – NOT ADIC DATA. One end-to-end pass on ``mini_book`` (allocation v2) with the testing fakes, through every
Protocol method of §3.17 and the cross-WP functions of the §4.5 chain:

    engine ``init`` with ``BeliefDraws`` → ``recourse_quotes`` → ``step`` → ``Ledger.apply`` → ``apply_recourse`` →
    P on 200 paths → tree → ``fixture_h`` → ``phase2`` → ``price`` → ``select`` → ``project`` → evaluator → ``RoomPort``

Cross-WP functions whose packages have not landed (``core.sim.simulate``, ``core.tree.build_tree``,
``core.phase2.phase2``, ``icm.price``, ``core.levelb.select``, ``core.safety.project``, ``rng.draw_block``,
``state.simulate_filter``, ``owner.attach_draws``, ``beliefs.draw_paths``, ...) run as stand-ins defined below with
the exact §4 signatures. ``SPEC`` transcribes those signatures and the §3.17 Protocols verbatim as stubs; the drift
tests fail if a Protocol, a fake, a stand-in or a landed implementation departs from them. Every array container met
on the way is validated against ``ARRAY_SPECS`` (types, dtypes, shapes, invariants) and its money fields are checked
to be declared and plausible in USD bn.
"""

from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timezone
from typing import Any

import numpy as np
import pytest
from pydantic import BaseModel

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts import ports
from adic_tpa.contracts.actions import LensAction
from adic_tpa.contracts.arrays import ARRAY_SPECS, F32, F64, ArrayContainer
from adic_tpa.contracts.beliefs import BeliefDraws, BeliefSet
from adic_tpa.contracts.book import BookSnapshot, OverlapGraph
from adic_tpa.contracts.claims import MemoDraft
from adic_tpa.contracts.config import load_json_payload
from adic_tpa.contracts.engine_io import FlowSlice, NoiseRequest, NoiseSlice
from adic_tpa.contracts.enums import (
    Book, CampaignState, Clock, ConsentScenario, ContractMode, DataClass, FlowType, Lens, MandateMode, Plane, PricedOn, RoleId,
    RowFamily, RunMode, StressState, WorldId,
)
from adic_tpa.contracts.errors import PricingRefused, SchemaError
from adic_tpa.contracts.evidence import REQUIRED_TERMINAL_SERIES, EvalRequest, PathMetrics, PathMetricsMeta, RunManifest
from adic_tpa.contracts.hashing import canonical_artifact_hash, content_hash
from adic_tpa.contracts.ids import ArtifactRef, CampaignId, HoldingId, MetricId, RunId, UnitId, make_run_id
from adic_tpa.contracts.lab import AssumptionEntry, Escalation, KeyValue
from adic_tpa.contracts.ledger import LedgerState, StressSpec
from adic_tpa.contracts.optimizer import (
    ActionProposal, Column, ColumnPool, Envelope, EnvelopeSet, ExactCheck, FTPCurves, FTPPoint, GlidePath, HSolution,
    Kernel, LinearizedTier1, LPModel, Phase1Result, SafeAction, Selection, WhatChanged,
)
from adic_tpa.contracts.policy import ActionPackage, OverlayLeg, OverlayStructure, PackageItem, PolicySpec, RecourseOrder
from adic_tpa.contracts.ports import EngineFactory, LLMRequest, Policy, PolicyContext, ToolDef
from adic_tpa.contracts.room import ScenarioSpecDraft, ViewSpec, ViewSpecDraft
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.tools import (
    AttributeIn, CardIdsIn, EPIn, EVSIIn, FlipIn, ImpliedIn, MetricListIn, MetricQueryIn, OptimizeHIn, Phase1In,
    ProvenanceQueryIn, ReverseStressIn, StateSnapshotIn, ValidateClaimsIn,
)
from adic_tpa.contracts.units import q_rate
from adic_tpa.contracts.world import (
    GroupRates, GroupRatesMeta, OwnerConfig, ScenarioCube, StateSnapshot, StressFilterParams, Tree, TreeSpec, WorldSpec,
)
from adic_tpa.testing import (
    EVALUATOR_METHODS, FakeEngineFactory, FakeEvaluator, FakeLedger, FakeLLMBackend, FakePolicy, FakeRoom,
    fake_belief_draws, fake_beliefs, fake_draw_block, fake_engines, fake_filter, fake_filter_params, fake_observables,
    fake_owner_draws, fixture_h, fixture_phase1, fixture_tree, merge_outcomes, merge_quotes, mini_book,
    mini_contract, mini_cube, mini_owner_config, mini_register, mini_state0, mini_world, solve_fixture_lp,
    synthetic_committee, world_slice,
)
from adic_tpa.testing.fixture_h import T4_ROW

N_PATHS = 200
QUARTERS = 40
TREE_QUARTERS = 12
ROOT_SEED = 20261018
_UTC = timezone.utc
_CASH = np.array([FlowType(i).is_cash() for i in range(18)])


# =============================================================================================== spec stubs
class SPEC:
    """§3.17 Protocol methods and §4 cross-WP signatures, transcribed verbatim (annotations stay strings)."""

    class AssetEngine:
        def init(self, book: BookSnapshot, beliefs: BeliefSet, n_paths: int, *, draws: BeliefDraws,
                 world: WorldSpec) -> EngineState: ...  # noqa: F821
        def noise_requests(self, t: int) -> Sequence[NoiseRequest]: ...
        def recourse_quotes(self, t: int, st: EngineState, world: WorldSlice) -> RecourseAvailability: ...  # noqa: F821
        def step(self, t: int, st: EngineState, world: WorldSlice, act: ActionSlice,  # noqa: F821
                 noise: NoiseSlice) -> FlowSlice: ...
        def apply_recourse(self, st: EngineState, outcome: RecourseOutcome) -> None: ...  # noqa: F821
        def column_flows(self, unit_id: UnitId, action: LensAction, cube: ScenarioCube) -> "FlowCube": ...  # noqa: F821

    class Ledger:
        def apply(self, m: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: F32,
                  quotes: RecourseAvailability) -> tuple[LedgerState, RecourseOutcome]: ...  # noqa: F821
        def row_slacks(self, ls: LedgerState) -> dict[RowKey, F32]: ...  # noqa: F821
        def stress_replica(self, ls0: LedgerState, stress: StressSpec) -> StressReport: ...  # noqa: F821

    class EngineFactory:
        def build(self, book: BookSnapshot, world: WorldSpec) -> "EngineBundle": ...  # noqa: F821

    class Policy:
        def act(self, q: int, obs: Observables) -> ActionSlice: ...  # noqa: F821

    class LLMBackend:
        def parse(self, req: "LLMRequest", output_model: type[BaseModel]) -> "LLMResponse": ...  # noqa: F821
        def run_tools(self, req: "LLMRequest", tools: Sequence["ToolDef"],
                      executor: "ToolExecutor") -> "LLMResponse": ...  # noqa: F821

    class RoomPort:
        def compile_agenda(self, quarter: str, snapshot_hash: str) -> EvidencePlan: ...  # noqa: F821
        def build_briefs(self, plan: EvidencePlan) -> tuple[RenderedDocument, ...]: ...  # noqa: F821
        def run_shadow_ic(self, items: Sequence[str]) -> tuple[SeatAssessment, ...]: ...  # noqa: F821
        def lock_prevotes(self, quarter: str) -> tuple[str, ...]: ...
        def record_decisions(self, quarter: str) -> tuple[DecisionRecord, ...]: ...  # noqa: F821

    # §4 cross-WP functions on the chain, and the upstream functions the fakes stand in for.
    @staticmethod
    def draw_block(base: bytes, requests: Sequence[NoiseRequest], paths: np.ndarray) -> NoiseSlice: ...

    @staticmethod
    def simulate_filter(factors: F32, factor_names: Sequence[str], params: StressFilterParams,
                        panel_tail: F64) -> F32: ...

    @staticmethod
    def attach_draws(cube: ScenarioCube, cfg: OwnerConfig, d_prev: float, base: bytes) -> ScenarioCube: ...

    @staticmethod
    def draw_paths(bs: BeliefSet, base: bytes, paths: np.ndarray, graph: OverlapGraph, tax: GroupRegistry,
                   world: WorldSpec) -> BeliefDraws: ...

    @staticmethod
    def simulate(book: BookSnapshot, beliefs: BeliefSet, policy: Policy, world: WorldSpec, state0: StateSnapshot,
                 cfg: SimConfig, *, root_seed: int, owner_cfg: OwnerConfig, filter_params: StressFilterParams,
                 salt: bytes | None = None, factory: EngineFactory | None = None) -> SimResult: ...

    @staticmethod
    def record_group_rates(book: BookSnapshot, beliefs: BeliefSet, world: WorldSpec, state0: StateSnapshot,
                           n_paths: int, plane: Plane, *, root_seed: int, owner_cfg: OwnerConfig,
                           filter_params: StressFilterParams, quarters: int = 12) -> GroupRates: ...

    @staticmethod
    def attach_group_rates(cubes: Mapping[WorldId, ScenarioCube],
                           rates: Mapping[WorldId, GroupRates]) -> dict[WorldId, ScenarioCube]: ...

    @staticmethod
    def build_tree(cubes: Mapping[WorldId, ScenarioCube], spec: TreeSpec) -> Tree: ...

    @staticmethod
    def phase2(lp: LPModel, p1: Phase1Result, glide: GlidePath, tree: Tree) -> HSolution: ...

    @staticmethod
    def price(sol: HSolution, lp: LPModel, tree: Tree, tax: GroupRegistry) -> tuple[Kernel, FTPCurves, EnvelopeSet]: ...

    @staticmethod
    def select(lp: LPModel, sol: HSolution, cols: ColumnPool, *, basis: "Basis") -> Selection: ...  # noqa: F821

    @staticmethod
    def project(prop: ActionProposal, state: StateSnapshot, *, ls0: LedgerState, rows: "LinearizedTier1",
                exact_check: Callable[[ActionProposal], "ExactCheck"], q_weights: Mapping[str, float]) -> SafeAction: ...


# Where each §4 function lives once its work package lands; the drift test checks the landed ones.
LANDING: dict[str, tuple[str, ...]] = {
    "draw_block": ("adic_tpa.rng", "adic_tpa.rng.streams"),
    "simulate_filter": ("adic_tpa.state", "adic_tpa.state.filter"),
    "attach_draws": ("adic_tpa.owner", "adic_tpa.owner.draw"),
    "draw_paths": ("adic_tpa.beliefs", "adic_tpa.beliefs.draws"),
    "simulate": ("adic_tpa.core.sim",),
    "record_group_rates": ("adic_tpa.core.sim",),
    "attach_group_rates": ("adic_tpa.core.tree",),
    "build_tree": ("adic_tpa.core.tree",),
    "phase2": ("adic_tpa.core.phase2",),
    "price": ("adic_tpa.icm", "adic_tpa.icm.pricing"),
    "select": ("adic_tpa.core.levelb", "adic_tpa.core.colgen"),
    "project": ("adic_tpa.core.safety",),
}
SPEC_FUNCTIONS: tuple[str, ...] = tuple(LANDING)
PROTOCOLS: dict[str, type] = {"AssetEngine": ports.AssetEngine, "Ledger": ports.Ledger,
                              "EngineFactory": ports.EngineFactory, "Policy": ports.Policy,
                              "LLMBackend": ports.LLMBackend, "RoomPort": ports.RoomPort,
                              "EvaluatorPort": ports.EvaluatorPort}


def protocol_methods(proto: type) -> tuple[str, ...]:
    return tuple(name for name, value in vars(proto).items() if callable(value) and not name.startswith("_"))


# ---------------------------------------------------------------------------------------- signature canon
_QUALIFIER = re.compile(r"\b(?:[A-Za-z_]\w*\.)+(?=[A-Za-z_])")


def _norm(annotation: Any) -> str:
    """Annotation text without quotes, spaces or module qualifiers; ``Optional[X]`` read as ``X | None``."""
    if annotation is inspect.Parameter.empty:
        return ""
    text = annotation if isinstance(annotation, str) else getattr(annotation, "__name__", repr(annotation))
    text = text.replace('"', "").replace("'", "").replace(" ", "")
    text = re.sub(r"Optional\[([^\[\]]+)\]", r"\1|None", text)
    return _QUALIFIER.sub("", text)


def canon(fn: Callable[..., Any], *, with_return: bool = True) -> tuple[Any, ...]:
    """(name, kind, default, annotation) per parameter (``self`` dropped) and the return annotation."""
    sig = inspect.signature(fn)
    params = tuple((p.name, p.kind.name, "<none>" if p.default is inspect.Parameter.empty else repr(p.default),
                    _norm(p.annotation)) for p in sig.parameters.values() if p.name != "self")
    return (params, _norm(sig.return_annotation) if with_return else None)


def refines(impl: Callable[..., Any], spec: Callable[..., Any]) -> bool:
    """§0.2: an implementation may add parameters with defaults to a frozen signature, nothing else. The spec's
    parameters must come first, unchanged, and the return annotation must agree."""
    got, want = canon(impl), canon(spec)
    n = len(want[0])
    extra = got[0][n:]
    return got[0][:n] == want[0] and got[1] == want[1] and all(p[2] != "<none>" for p in extra)


# ============================================================================================== stand-ins
@dataclass(frozen=True)
class SimConfig:
    """Stand-in for ``core.sim.SimConfig`` (§4.19)."""

    n_paths: int
    block: int = 2000
    plane: Plane = Plane.SEARCH
    quarters: int = 40
    record: tuple[str, ...] = ()
    keep_units: bool = False
    private_clock: Clock = Clock.QUARTERLY
    processes: int = 1
    numba_threads: int = 8


@dataclass(frozen=True)
class SimResult:
    """Stand-in for ``core.sim.SimResult`` (§4.19): a frozen dataclass because it holds arrays."""

    metrics: PathMetrics
    ledger_paths_ref: ArtifactRef | None
    group_rates: GroupRates | None
    manifest: RunManifest


@dataclass
class Trace:
    """What the skeleton records on its way (calls, containers, identity residuals, sales)."""

    calls: set[tuple[str, str]] = field(default_factory=set)
    containers: list[ArrayContainer] = field(default_factory=list)
    cash_residuals: list[float] = field(default_factory=list)
    min_cash_bn: float = float("inf")
    failed_paths: int = 0
    proceeds_bn: float = 0.0
    red_sales: int = 0
    sale_proceeds_bn: float = 0.0

    def call(self, proto: str, method: str) -> None:
        self.calls.add((proto, method))

    def keep(self, *objs: ArrayContainer | None) -> None:
        self.containers.extend(o for o in objs if o is not None)

    def reset(self) -> None:
        fresh = Trace()
        for name in ("calls", "containers", "cash_residuals", "min_cash_bn", "failed_paths", "proceeds_bn",
                     "red_sales", "sale_proceeds_bn"):
            setattr(self, name, getattr(fresh, name))


TRACE = Trace()


def _base(root_seed: int, plane: Plane, world: str) -> bytes:
    """Stand-in for ``rng.base_entropy`` (§1.7): 16 bytes per (plane, world)."""
    return hashlib.sha256(f"{root_seed}|{plane.value}|{world}".encode("utf-8")).digest()[:16]


def draw_block(base: bytes, requests: Sequence[NoiseRequest], paths: np.ndarray) -> NoiseSlice:
    """Stand-in for ``rng.draw_block`` (§4.2)."""
    return fake_draw_block(base, requests, paths)


def simulate_filter(factors: F32, factor_names: Sequence[str], params: StressFilterParams,
                    panel_tail: F64) -> F32:
    """Stand-in for ``state.simulate_filter`` (§4.9)."""
    return fake_filter(params)(factors, factor_names, params, panel_tail)


def attach_draws(cube: ScenarioCube, cfg: OwnerConfig, d_prev: float, base: bytes) -> ScenarioCube:
    """Stand-in for ``owner.attach_draws`` (§4.8): a flat draw at the owner's target constant c."""
    del d_prev, base
    return fake_owner_draws(cube, rate=min(max(cfg.c, 0.05), 0.10))


def draw_paths(bs: BeliefSet, base: bytes, paths: np.ndarray, graph: OverlapGraph, tax: GroupRegistry,
               world: WorldSpec) -> BeliefDraws:
    """Stand-in for ``beliefs.draw_paths`` (§4.15): α frozen at α̂."""
    del base, graph, tax
    return fake_belief_draws(bs, world, int(np.asarray(paths).size))


def _scale_out(ledger: FakeLedger, slices: Sequence[FlowSlice], m: int, unit_ids: Sequence[UnitId],
               sold: np.ndarray) -> np.ndarray:
    """Cash not booked in month m for units sold earlier in the quarter (recomputed independently of the ledger)."""
    out = np.zeros(sold.shape[0])
    pos = {str(u): j for j, u in enumerate(unit_ids)}
    for fs in slices:
        w = ledger.month_weights(fs, m)
        for k, uid in enumerate(fs.recourse_unit_ids):
            j = pos.get(str(uid))
            if j is not None:
                out += sold[:, j] * (fs.by_recourse_unit[:, k, :].astype(np.float64)[:, _CASH] * w[_CASH]).sum(axis=1)
    return out


@dataclass
class _Run:
    book: BookSnapshot
    cube: ScenarioCube
    bundle: Any
    ledger_states: list[LedgerState]
    unit_flows: dict[int, dict[str, np.ndarray]]       # quarter → engine → by_unit flows summed over the quarter
    navs: dict[int, dict[str, np.ndarray]]             # quarter → engine → economic NAV at quarter end
    unfs: dict[int, dict[str, np.ndarray]]             # quarter → engine → unfunded at quarter end
    navs0: dict[str, np.ndarray]
    unfs0: dict[str, np.ndarray]


def _run(book: BookSnapshot, beliefs: BeliefSet, policy: Policy, world: WorldSpec, state0: StateSnapshot,
         n_paths: int, quarters: int, plane: Plane, *, root_seed: int, owner_cfg: OwnerConfig,
         filter_params: StressFilterParams, factory: EngineFactory) -> _Run:
    """The §4.19 simulation loop on one block, with the testing fakes behind the frozen Protocols."""
    bundle = factory.build(book, world)
    TRACE.call("EngineFactory", "build")
    tax = GroupRegistry.for_version(book.taxonomy_version)
    base = _base(root_seed, plane, world.world_id)
    cube = mini_cube(n_paths, world.world_id)
    post = simulate_filter(cube.factors, cube.meta.factor_names, filter_params, np.array([0.002, 0.042]))
    assert np.array_equal(post, cube.stress_post), "the cube's stress posterior is the filter stand-in's"
    cube = attach_draws(cube, owner_cfg, state0.d_prev, base)
    draws = draw_paths(beliefs, base, np.arange(n_paths), book.overlap, tax, world)
    TRACE.keep(cube, draws)
    states = {}
    for e in bundle.engines:
        states[e.engine_id] = e.init(book, beliefs, n_paths, draws=draws, world=world)
        TRACE.call("AssetEngine", "init")
    ledger = bundle.ledger
    # TODO(contracts): the Ledger Protocol has no init_state; LedgerKernel (§4.14) and FakeLedger provide one.
    ls = ledger.init_state(book, n_paths)
    run = _Run(book=book, cube=cube, bundle=bundle, ledger_states=[ls], unit_flows={}, navs={}, unfs={},
               navs0={eid: st.stocks()[0].astype(np.float64) for eid, st in states.items()},
               unfs0={eid: st.stocks()[2].astype(np.float64) for eid, st in states.items()})
    n_units = len(book.unit_index().unit_ids)
    for t in range(quarters):
        act = policy.act(t, fake_observables(t, ls, n_units))
        TRACE.call("Policy", "act")
        quotes_e = []
        for e in bundle.engines:
            ws0 = world_slice(cube, [3 * t], clock=e.clock, t=3 * t if e.clock is Clock.MONTHLY else t)
            quotes_e.append(e.recourse_quotes(t, states[e.engine_id], ws0))
            TRACE.call("AssetEngine", "recourse_quotes")
        quotes = merge_quotes(quotes_e)
        noise = {}
        for e in bundle.engines:
            noise[e.engine_id] = draw_block(base, e.noise_requests(t), np.arange(n_paths))
            TRACE.call("AssetEngine", "noise_requests")
        q_slices: list[FlowSlice] = []
        m_slices: dict[int, list[FlowSlice]] = {}
        for e in bundle.engines:
            if e.clock is Clock.QUARTERLY:
                ws = world_slice(cube, [3 * t, 3 * t + 1, 3 * t + 2], clock=e.clock, t=t)
                q_slices.append(e.step(t, states[e.engine_id], ws, act, noise[e.engine_id]))
            else:
                for m in range(3 * t, 3 * t + 3):
                    ws = world_slice(cube, [m], clock=e.clock, t=m)
                    m_slices.setdefault(m, []).append(e.step(m, states[e.engine_id], ws, act, noise[e.engine_id]))
            TRACE.call("AssetEngine", "step")
        all_slices = q_slices + [s for ms in m_slices.values() for s in ms]
        if t in (0, 1, quarters - 1):
            TRACE.keep(act, quotes, *all_slices, *noise.values())
        run.unit_flows[t], run.navs[t], run.unfs[t] = {}, {}, {}
        for fs in all_slices:
            run.unit_flows[t][fs.engine_id] = run.unit_flows[t].get(fs.engine_id, 0.0) + fs.by_unit.astype(np.float64)
            run.navs[t][fs.engine_id] = fs.nav_econ.astype(np.float64)
            run.unfs[t][fs.engine_id] = fs.unfunded.astype(np.float64)
            TRACE.sale_proceeds_bn += float(fs.by_group[:, :, FlowType.SALE_PROCEEDS].astype(np.float64).sum())
        outcomes, sold = [], np.zeros((n_paths, len(quotes.unit_ids)))
        for m in range(3 * t, 3 * t + 3):
            flows = q_slices + m_slices.get(m, [])
            fy_col = ledger.cal.fy_index(ledger.cal.fiscal_year(t))
            draw = ledger.instalment(ls, cube.draw_rate[:, fy_col], m)
            booked = ledger.booked_cash(m, flows) - _scale_out(ledger, flows, m, quotes.unit_ids, sold)
            new_ls, outcome = ledger.apply(m, ls, flows, draw, quotes)
            TRACE.call("Ledger", "apply")
            outcome.check_against(quotes)
            fac_draw = new_ls.fac_drawn_bn.sum(axis=1) - ls.fac_drawn_bn.sum(axis=1)
            expected = (ls.treasury_bn.sum(axis=1) + booked + draw.astype(np.float64) + outcome.proceeds_bn.sum(axis=1)
                        + fac_draw + ledger.last["unpaid"] + ledger.last["shortfall"])
            TRACE.cash_residuals.append(float(np.abs(new_ls.treasury_bn.sum(axis=1) - expected).max()))
            TRACE.min_cash_bn = min(TRACE.min_cash_bn, float(new_ls.treasury_bn[:, 0].min()))
            TRACE.failed_paths = max(TRACE.failed_paths, int(new_ls.failed.sum()))
            TRACE.proceeds_bn += float(outcome.proceeds_bn.sum())
            TRACE.red_sales += int(outcome.red.sum())
            sold += outcome.sold_frac.astype(np.float64)
            outcomes.append(outcome)
            ls = new_ls
        merged = merge_outcomes(outcomes)
        for e in bundle.engines:
            e.apply_recourse(states[e.engine_id], merged)
            TRACE.call("AssetEngine", "apply_recourse")
        if t in (0, quarters - 1):
            TRACE.keep(merged, ls)
        run.ledger_states.append(ls)
    return run


def _path_metrics(run: _Run, world: WorldSpec, plane: Plane, policy: Policy) -> PathMetrics:
    states = run.ledger_states
    quarterly_names = ("nav_econ_bn", "hqla_unenc_bn", "cushion")
    w0 = states[0].nav_econ_bn
    q = np.zeros((w0.size, 41, len(quarterly_names)), dtype=np.float32)
    for i, ls in enumerate(states[::3][:41]):
        q[:, i, 0], q[:, i, 1], q[:, i, 2] = ls.nav_econ_bn, ls.hqla_unenc_bn, ls.cushion
    last = states[-1]
    twr = np.array([ls.twr_index for ls in states])
    peak = np.maximum.accumulate(twr, axis=0)
    years = (len(states) - 1) / 12.0
    terminal = {
        "w_tilde_40": last.nav_econ_bn / w0, "w_tilde_real_40": last.nav_econ_bn / w0 / 1.02 ** years,
        "twr_3y": twr[min(36, len(twr) - 1)] ** (1 / 3) - 1, "twr_5y": twr[min(60, len(twr) - 1)] ** (1 / 5) - 1,
        "twr_10y": twr[-1] ** (1 / years) - 1, "red_event": last.red_event.astype(np.float64),
        "red_quarter": np.where(last.red_month >= 0, last.red_month // 3, -1).astype(np.float64),
        "payout_short": last.payout_short.astype(np.float64), "t7_shortfall_12m": np.zeros_like(w0),
        "t9_trigger_12m": np.zeros_like(w0), "max_dd_10y": (1.0 - twr / peak).max(axis=0),
        "failed": last.failed.astype(np.float64)}
    meta = PathMetricsMeta(world_id=world.world_id, plane=plane, policy_ref=policy.policy_ref,
                           cube_checksum=run.cube.meta.checksum, quarterly_names=quarterly_names,
                           terminal_names=REQUIRED_TERMINAL_SERIES, data_class=DataClass.SYNTHETIC)
    return PathMetrics(meta=meta, quarterly=q, terminal=np.stack([np.asarray(terminal[k], dtype=np.float64)
                                                                  for k in REQUIRED_TERMINAL_SERIES], axis=1))


def _group_rates(run: _Run, world: WorldSpec, policy: Policy, quarters: int) -> GroupRates:
    """``GroupRates`` (§3.7) of the run's first ``quarters`` quarters, private groups × age buckets."""
    tax = GroupRegistry.for_version(run.book.taxonomy_version)
    idx = run.book.unit_index(tax)
    bucket = {str(u): int(b) for u, b in zip(idx.unit_ids, idx.age_bucket, strict=True)}
    private = tax.private()
    p = run.cube.meta.n_paths
    shape = (p, quarters, len(private), 2)
    out = {k: np.zeros(shape) for k in ("delta", "qcall", "ret_simple", "bid", "income", "u_per_nav", "nav_share")}
    for qtr in range(quarters):
        for gi, g in enumerate(private):
            nav_b = []
            for b in range(2):
                nav0, nav1, unf0, flows, bids = np.zeros(p), np.zeros(p), np.zeros(p), np.zeros((p, 18)), []
                for e in run.bundle.engines:
                    for k, m in enumerate(e.units):
                        if m.group != g or bucket[str(m.unit_id)] != b:
                            continue
                        eid = e.engine_id
                        nav0 += run.navs[qtr - 1][eid][:, k] if qtr else run.navs0[eid][:, k]
                        unf0 += run.unfs[qtr - 1][eid][:, k] if qtr else run.unfs0[eid][:, k]
                        nav1 += run.navs[qtr][eid][:, k]
                        flows += run.unit_flows[qtr][eid][:, k, :]
                        bids.append(m.normal_bid)
                safe = np.maximum(nav0, 1e-12)
                dist, calls = flows[:, FlowType.DISTRIBUTION], -flows[:, FlowType.CALL]
                out["delta"][:, qtr, gi, b] = np.clip(dist / safe, 0.0, 1.0)
                out["qcall"][:, qtr, gi, b] = np.where(unf0 > 1e-12, np.clip(calls / np.maximum(unf0, 1e-12), 0.0, 1.0),
                                                       0.0)
                out["ret_simple"][:, qtr, gi, b] = (nav1 - nav0 - calls + dist) / safe
                out["bid"][:, qtr, gi, b] = float(np.mean(bids)) if bids else 0.9
                out["income"][:, qtr, gi, b] = flows[:, FlowType.INCOME_CASH] / safe
                out["u_per_nav"][:, qtr, gi, b] = unf0 / safe
                nav_b.append(nav0)
            total = nav_b[0] + nav_b[1]
            for b in range(2):
                out["nav_share"][:, qtr, gi, b] = np.where(total > 0, nav_b[b] / np.maximum(total, 1e-12), 0.5)
    call_stress = 1.0 - (1.0 - np.minimum(out["qcall"] * 1.5, 1.0)) ** 4
    eq = run.cube.meta.asset_names.index("us_equity")
    eq_q = np.stack([np.expm1(run.cube.asset_returns[:, 3 * k:3 * k + 3, eq].astype(np.float64).sum(axis=1))
                     for k in range(quarters)], axis=1)
    stress = np.stack([run.cube.stress_post[:, 3 * k + 2, :].argmax(axis=1) for k in range(quarters)], axis=1)
    flat = np.ones((p, quarters))
    obs = np.stack([run.cube.stress_post[:, 3 * k + 2, int(StressState.CRISIS)] for k in range(quarters)], axis=1)
    f32 = np.float32
    meta = GroupRatesMeta(groups=private, age_buckets=("young", "mature"), policy_ref=policy.policy_ref,
                          world_id=world.world_id, cube_checksum=run.cube.meta.checksum, quarters=quarters)
    return GroupRates(
        meta=meta, **{k: v.astype(f32) for k, v in out.items()}, call_stress_12m=call_stress.astype(f32),
        lo_ret=(0.6 * eq_q).astype(f32), hf_ret=(0.35 * eq_q).astype(f32),
        hf_phi=np.tile(np.array([0.24, 0.45, 0.75, 0.95], dtype=f32), (p, quarters, 1)), vm_per_beta=eq_q.astype(f32),
        cash_rate=(q_rate(0.0389) * flat).astype(f32), fac_rate=(q_rate(0.0474) * flat).astype(f32),
        ra_debt_rate=(q_rate(0.06) * flat).astype(f32), ra_amort=(0.005 * flat).astype(f32),
        ra_direct_share=(0.5 * flat).astype(f32), tail_prem_rate=(0.0015 / 4 * flat).astype(f32),
        tail_value=np.zeros((p, quarters), f32), opp_pnl_rate=np.zeros((p, quarters), f32),
        delta_im_rate=np.zeros((p, quarters), f32),
        draw_rate_q=np.stack([run.cube.draw_rate[:, min(k // 4, 10)] / 4.0 for k in range(quarters)], axis=1).astype(f32),
        stress_class=stress.astype(np.int8), obs=obs[:, :, None].astype(f32))


def simulate(book: BookSnapshot, beliefs: BeliefSet, policy: Policy, world: WorldSpec, state0: StateSnapshot,
             cfg: SimConfig, *, root_seed: int, owner_cfg: OwnerConfig, filter_params: StressFilterParams,
             salt: bytes | None = None, factory: EngineFactory | None = None) -> SimResult:
    """Stand-in for ``core.sim.simulate`` (§4.19) on the fakes."""
    if salt is not None or cfg.plane is Plane.FINAL:
        raise SchemaError("the skeleton runs on the search plane without a salt")
    fac = factory if factory is not None else FakeEngineFactory(owner_cfg)
    run = _run(book, beliefs, policy, world, state0, cfg.n_paths, cfg.quarters, cfg.plane, root_seed=root_seed,
               owner_cfg=owner_cfg, filter_params=filter_params, factory=fac)
    metrics = _path_metrics(run, world, cfg.plane, policy)
    rates = _group_rates(run, world, policy, TREE_QUARTERS) if "group_rates" in cfg.record else None
    created = datetime(2026, 10, 18, 9, 0, tzinfo=_UTC)
    key = f"{cfg.plane.value}:{world.world_id}"
    manifest = RunManifest(
        run_id=make_run_id(created, content_hash({"book": book.content_hash, "world": world.content_hash,
                                                  "policy": policy.policy_ref, "seed": root_seed})),
        kind="skeleton.simulate", created_at=created, engine_git_sha="skeleton",
        engine_tree_hash=content_hash("skeleton-engines"), config_hash=content_hash("skeleton-config"),
        contract_hash=None, snapshot_hash=book.content_hash, census_hash=None, belief_hash=beliefs.meta.content_hash,
        scenario_hashes={key: run.cube.meta.checksum}, seed_spawn={key: _base(root_seed, cfg.plane, world.world_id).hex()},
        plane=cfg.plane, cache_keys=(), solver_records=(), versions={"numpy": np.__version__}, env={}, llm_calls=(),
        data_class=DataClass.SYNTHETIC, run_mode=RunMode.DEV_SYNTHETIC, status="OK",
        effective_config_hashes=dict(run.bundle.effective_config_hashes),
        canonical_artifact_hashes={"metrics": canonical_artifact_hash(metrics)})
    return SimResult(metrics=metrics, ledger_paths_ref=None, group_rates=rates, manifest=manifest)


def record_group_rates(book: BookSnapshot, beliefs: BeliefSet, world: WorldSpec, state0: StateSnapshot,
                       n_paths: int, plane: Plane, *, root_seed: int, owner_cfg: OwnerConfig,
                       filter_params: StressFilterParams, quarters: int = 12) -> GroupRates:
    """Stand-in for ``core.sim.record_group_rates`` (§4.19): HOLD over the tree's quarters."""
    tax = GroupRegistry.for_version(book.taxonomy_version)
    ctx = PolicyContext(idx=book.unit_index(tax), tax=tax, p0_theta={}, recourse=_ORDER,
                        mandate_mode=MandateMode.B_OWNER_CALL, archetype_params={},
                        contract_hash=content_hash("skeleton"))
    policy = FakePolicy(ctx, n_paths, n_lots=3, n_facilities=len(book.facilities))
    run = _run(book, beliefs, policy, world, state0, n_paths, quarters, plane, root_seed=root_seed,
               owner_cfg=owner_cfg, filter_params=filter_params, factory=FakeEngineFactory(owner_cfg))
    return _group_rates(run, world, policy, quarters)


def attach_group_rates(cubes: Mapping[WorldId, ScenarioCube],
                       rates: Mapping[WorldId, GroupRates]) -> dict[WorldId, ScenarioCube]:
    """Stand-in for ``core.tree.attach_group_rates`` (§4.20)."""
    return {w: replace(cube, group_rates=rates[w]) for w, cube in cubes.items()}


def build_tree(cubes: Mapping[WorldId, ScenarioCube], spec: TreeSpec) -> Tree:
    """Stand-in for ``core.tree.build_tree`` (§4.20): checks its inputs, returns the fixture tree on the worlds."""
    if tuple(spec.worlds) != tuple(cubes):
        raise SchemaError("build_tree: the cubes must be the spec's worlds, in order")
    for w, cube in cubes.items():
        if cube.group_rates is None or cube.group_rates.meta.world_id != w:
            raise SchemaError(f"build_tree: cube {w} carries no group rates of its own world")
        cube.validate()
    return fixture_tree(worlds=tuple(spec.worlds))


def phase2(lp: LPModel, p1: Phase1Result, glide: GlidePath, tree: Tree) -> HSolution:
    """Stand-in for ``core.phase2.phase2`` (§4.20, §5.10): the restored problem's solution; duals only from here."""
    restored = p1.mode is not ContractMode.NORMAL
    if restored and (p1.recovery_hash is None or p1.recovery_hash != glide.recovery_hash):
        raise SchemaError("phase2: a recovery-mode solve prices on the glide path's recovery hash")
    if lp.meta.tree_hash != tree.tree_hash:
        raise SchemaError("phase2: the LP was built on another tree")
    return solve_fixture_lp(lp, tree, priced_on=PricedOn.RESTORED if restored else PricedOn.FEASIBLE,
                            recovery_hash=p1.recovery_hash)


def price(sol: HSolution, lp: LPModel, tree: Tree, tax: GroupRegistry) -> tuple[Kernel, FTPCurves, EnvelopeSet]:
    """Stand-in for ``icm.price`` (§4.22, §5.8): kernel over strict ancestors, FTP by tenor, T4′ envelopes."""
    if any(q.pinned for q in sol.duals.quality.values()):
        raise PricingRefused("price: pinned duals never price")
    ell = sol.duals.ell
    deflator = np.ones(tree.p.size)
    for node in range(1, tree.p.size):
        deflator[node] = deflator[tree.parent[node]] / (1.0 + ell[tree.parent[node]])
    q1 = tree.stage == 1
    lam = {}
    for s in StressState:
        mask = q1 & (tree.regime_class == s)
        lam[s] = float(np.average(ell[mask], weights=tree.p[mask])) if mask.any() else 0.0
    kernel = Kernel(pi=tuple(map(float, tree.p * deflator)), ell=tuple(map(float, ell)),
                    deflator=tuple(map(float, deflator)), esscher_gamma=0.0, lambda_spot=lam,
                    one_off_premium=float(ell[0]), priced_on=sol.priced_on, recovery_hash=sol.recovery_hash)
    m0 = float(sol.duals.M_cash[0])
    components = {k.family: float(ell[0] * sol.duals.pi_row[i] / m0) if m0 > 0 else 0.0
                  for i, k in enumerate(lp.row_keys)}
    points = []
    for h in range(1, int(tree.stage.max()) + 1):
        rate = (1.0 + float(ell[0])) ** (1.0 / h) - 1.0
        points.append(FTPPoint(tenor_q=h, decision_q=rate, published_q=rate, band_q=(rate, rate),
                               components=components, priced_on=sol.priced_on, recovery_hash=sol.recovery_hash))
    a = lp.A.toarray()
    owner = {"rcf": tax.ids("funding")[0], "reserve": tax.ids("funding")[0], "amber": tax.amber_tier()[0],
             "pace": tax.red_tier()[0], "sell": tax.red_tier()[0]}
    use: dict[str, float] = {}
    for j, key in enumerate(lp.col_keys):
        g = owner.get(key.name)
        if g is not None:
            use[g] = use.get(g, 0.0) + float(a[0, j] * sol.x[j] * lp.scale_bn)
    rng = sol.duals.quality[str(lp.row_keys[0])].ranging
    envelopes = tuple(Envelope(group=g, row=str(lp.row_keys[0]), value_bn=v, range_bn=(v, v),
                               dual=float(sol.duals.pi_row[0]), ranging_bn=(rng[0] * lp.scale_bn, rng[1] * lp.scale_bn),
                               elasticity_bn_per_100bp=0.0, delivery_share=None, priced_on=sol.priced_on,
                               recovery_hash=sol.recovery_hash) for g, v in use.items())
    slack = (float(a[0] @ sol.x) - float(lp.row_lo[0])) * lp.scale_bn
    return kernel, FTPCurves(asof=date(2026, 9, 30), tolerance=tuple(points), appetite=None), EnvelopeSet(
        envelopes=envelopes, pool_bn={str(lp.row_keys[0]): sum(use.values())}, slack_bn={str(lp.row_keys[0]): slack})


def select(lp: LPModel, sol: HSolution, cols: ColumnPool, *, basis: "Basis") -> Selection:  # noqa: F821
    """Stand-in for ``core.levelb.select`` (§4.21): the LP's positive lens columns, Γ = 0 on a pure LP."""
    del basis
    col_of = {str(k.idx[0][1]): j for j, k in enumerate(lp.col_keys) if k.family == "lens"}
    chosen, x, split = [], {}, []
    for col in cols.columns:
        j = col_of[str(col.unit_id)]
        value = float(sol.x[j] * lp.scale_bn)
        if value > 1e-12:
            chosen.append(col.col_id)
            x[col.col_id] = value
            if value < float(lp.col_hi[j] * lp.scale_bn) - 1e-9:
                split.append(col.unit_id)
    return Selection(chosen=tuple(chosen), x=x, split_assets=tuple(split), gamma_bp=0.0, gamma_bp_exact=0.0,
                     certified=True, iterations=1, forced_resolve_flags={})


def project(prop: ActionProposal, state: StateSnapshot, *, ls0: LedgerState, rows: "LinearizedTier1",
            exact_check: Callable[[ActionProposal], "ExactCheck"], q_weights: Mapping[str, float]) -> SafeAction:
    """Stand-in for ``core.safety.project`` (§4.21 module F): the minimum Q-norm move onto ĝ ≤ −δ, row by row."""
    del state, ls0
    names = rows.action_names
    a = np.array([prop.root_values.get(n, 0.0) for n in names])
    q = np.array([q_weights.get(n, 1.0) for n in names])
    safe, binding = a.copy(), []
    for k, key in enumerate(rows.row_keys):
        excess = rows.g0[k] + rows.G[k] @ (safe - a) + rows.delta[k]
        if excess > 1e-12:
            grad = rows.G[k]
            safe = safe - excess * (grad / q) / float(grad @ (grad / q))
            binding.append(str(key))
    changed = tuple(WhatChanged(field=n, before=float(a[i]), after=float(safe[i]), reason_row=binding[0])
                    for i, n in enumerate(names) if binding and abs(safe[i] - a[i]) > 1e-15)
    new = ActionProposal(source=prop.source, root_values={**prop.root_values, **dict(zip(names, map(float, safe)))},
                         lens_actions=prop.lens_actions)
    return SafeAction(action=new, changed=changed, binding_rows=tuple(binding), projected=bool(binding),
                      tier1_override_needed=False, exact_recheck_passed=exact_check(new).passed)


_ORDER = RecourseOrder(rungs=("reserve", "p2s", "liquid", "facility", "amber", "red"))


# ============================================================================================== the run
@dataclass
class Skeleton:
    book: BookSnapshot
    sim: SimResult
    rates_m6: GroupRates
    cubes: dict[str, ScenarioCube]
    tree: Tree
    lp: LPModel
    sol: HSolution
    sol2: HSolution
    p1: Phase1Result
    glide: GlidePath
    kernel: Kernel
    ftp: FTPCurves
    envelopes: EnvelopeSet
    selection: Selection
    safe: SafeAction
    column_cubes: dict[str, Any]
    stress_report: Any
    row_slacks: dict
    evaluator: FakeEvaluator
    room_records: tuple
    llm_parsed: Any
    llm_tools: Any


def _evaluator_calls(ev: FakeEvaluator, run_id: RunId) -> None:
    """Every ``EvaluatorPort`` method once, with schema-valid inputs (the skeleton's 'evaluator client' step)."""
    ref = ArtifactRef.make(run_id, "metrics", "")
    leg = OverlayLeg(template="put_spread_90_72", strike_rel=0.90, expiry_months=6, notional_bn=5.0, side="long")
    structure = OverlayStructure(template="put_spread_90_72", legs=(leg,), sleeve=Book.TAIL)
    view = ViewSpec(view_id="v1", draft=ViewSpecDraft(channel="EP", metric="hy_spread", operator="ge", value=0.06),
                    author_hash=content_hash("analyst"), confirmed=True, confirmed_by=content_hash("cro"),
                    confirmation_surface="tpa_chat")
    spec = PolicySpec(anchor="P0@sha256:" + "a" * 64)
    metric = MetricId("tier1.t6.cp_upper@v1")
    calls = {
        "state_snapshot": (StateSnapshotIn(),), "phase1_restore": (Phase1In(scenario=ConsentScenario.R1),),
        "compile_spec": (spec,),
        "evaluate_policy": (EvalRequest(request_id="r1", campaign_id=CampaignId("cmp-2026Q4-1"), attempt_id="a1",
                                        spec_hash=spec.spec_hash, kind="evaluate"),),
        "price_actions": (ActionPackage(items=(PackageItem(target=HoldingId("SYN-PE-0001"), lens=Lens.SELL,
                                                           instrument="lp_secondary_sale", size_frac=0.1),)),),
        "optimize_h": (OptimizeHIn(views=(view,)),),
        "evaluate_scenario": (ScenarioSpecDraft(kind="tilt", targets=(KeyValue(key="hy_spread", value=0.08),),
                                                kl_bound=0.2),),
        "reverse_stress": (ReverseStressIn(metric=metric, threshold=0.01),),
        "implied_actions": (ImpliedIn(seat_id="CRO", item_id="Q1"),), "ep_condition": (EPIn(views=(view,)),),
        "evsi_crossfit": (EVSIIn(item_id="Q1"),), "flip_thresholds": (FlipIn(card_id="card-1"),),
        "robustness_card": (CardIdsIn(ids=("Q1",)),), "bridge_card": (CardIdsIn(ids=("M1",)),),
        "group_envelopes": (CardIdsIn(),), "overlay_offset_card": (CardIdsIn(),),
        "attribute": (AttributeIn(run_id=run_id, kind="null"),), "price_trade": (structure,),
        "crif_sensitivities": (structure,), "simm_like": (structure,), "greek_offsets": (structure,),
        "hybrid_quote_check": (structure,), "get_metric": (MetricQueryIn(metric_id=metric),),
        "list_metrics": (MetricListIn(prefix="tier1"),), "get_provenance": (ProvenanceQueryIn(ref=ref),),
        "validate_claims": (ValidateClaimsIn(doc_id="memo-1"),),
        "log_assumption": (AssumptionEntry(assumption_id="A1", text="SYNTHETIC assumption", origin="skeleton",
                                           tagged_artifacts=(ref,)),),
        "escalate": (Escalation(escalation_id="E1", kind="question", question="SYNTHETIC?", blocking=False,
                                proposed_assumption=None, severity="low", worker=None, state=CampaignState.IDEATION,
                                raised_at=datetime(2026, 10, 18, tzinfo=_UTC)),),
    }
    assert tuple(calls) == EVALUATOR_METHODS == protocol_methods(ports.EvaluatorPort)
    for name, args in calls.items():
        assert getattr(ev, name)(*args) is not None, name
        TRACE.call("EvaluatorPort", name)


def _llm(backend: FakeLLMBackend, evaluator: FakeEvaluator) -> tuple[Any, Any]:
    req = LLMRequest(role=RoleId.MEMO_WRITER, model="claude-opus-5-5", system=SYNTHETIC_FOOTER,
                     messages=({"role": "user", "content": "Draft the memo."},), tools=(), effort="high")
    parsed = backend.parse(req, MemoDraft)
    TRACE.call("LLMBackend", "parse")
    tool = ToolDef(name="get_metric", description="Read one metric instance.",
                   input_schema=MetricQueryIn.model_json_schema())

    def executor(tool_use_id: str, name: str, tool_input: Mapping[str, Any]) -> Mapping[str, Any]:
        out = evaluator.get_metric(load_json_payload(json.dumps(dict(tool_input)), MetricQueryIn))
        return {"type": "tool_result", "tool_use_id": tool_use_id, "content": out.model_dump_json(), "is_error": False}

    ran = backend.run_tools(req, (tool,), executor)
    TRACE.call("LLMBackend", "run_tools")
    return parsed, ran


def _lens_actions(unit: UnitId, group: Any) -> dict[str, LensAction]:
    def act(lens: Lens, instrument: str, exposure: float, financing: float, cash: float) -> LensAction:
        return LensAction(unit_id=unit, group=group, lens=lens, instrument=instrument, size_bn=1.0,
                          exposure_delta_bn=exposure, financing_delta_bn=financing, cash_out_bn=cash)
    return {"SELL": act(Lens.SELL, "lp_secondary_sale", -1.0, 0.0, 0.88),
            "ADD": act(Lens.ADD, "secondary_buy", 1.0, 0.0, 0.0),
            "REFINANCE": act(Lens.REFINANCE, "nav_loan", 0.0, 0.5, 0.5),
            "LEVER": act(Lens.LEVER, "levered_add", 1.0, 0.5, 0.0)}


@pytest.fixture(scope="module")
def skeleton() -> Skeleton:
    TRACE.reset()
    book = mini_book("v2")
    tax = GroupRegistry.for_version("v2")
    beliefs = fake_beliefs(book)
    world, world6 = mini_world("M1"), mini_world("M6")
    state0, owner_cfg, filter_params = mini_state0(), mini_owner_config(), fake_filter_params()
    contract = mini_contract()
    idx = book.unit_index(tax)
    ctx = PolicyContext(idx=idx, tax=tax, p0_theta={}, recourse=_ORDER, mandate_mode=contract.mandate_mode,
                        archetype_params={}, contract_hash=content_hash(contract))
    red_unit = next(u for u, red in zip(idx.unit_ids, idx.red_tier, strict=True) if red)
    policy = FakePolicy(ctx, N_PATHS, n_lots=3, n_facilities=len(book.facilities), sells={1: {str(red_unit): 0.10}})
    factory = FakeEngineFactory(owner_cfg)
    cfg = SimConfig(n_paths=N_PATHS, plane=Plane.SEARCH, quarters=QUARTERS, record=("group_rates",), keep_units=True)
    sim = simulate(book, beliefs, policy, world, state0, cfg, root_seed=ROOT_SEED, owner_cfg=owner_cfg,
                   filter_params=filter_params, factory=factory)
    rates_m6 = record_group_rates(book, beliefs, world6, state0, N_PATHS, Plane.SEARCH, root_seed=ROOT_SEED,
                                  owner_cfg=owner_cfg, filter_params=filter_params, quarters=TREE_QUARTERS)
    bundle = factory.build(book, world)
    TRACE.call("EngineFactory", "build")
    ls0 = bundle.ledger.init_state(book, N_PATHS)
    stress_report = bundle.ledger.stress_replica(ls0, StressSpec.s_star(0.58, contract.tier1.conventions.pricing))
    TRACE.call("Ledger", "stress_replica")
    slacks = bundle.ledger.row_slacks(ls0)
    TRACE.call("Ledger", "row_slacks")
    cube1 = fake_owner_draws(mini_cube(N_PATHS, "M1"))
    cubes = attach_group_rates({"M1": cube1, "M6": fake_owner_draws(mini_cube(N_PATHS, "M6"))},
                               {"M1": sim.group_rates, "M6": rates_m6})
    tree = build_tree(cubes, TreeSpec(worlds=("M1", "M6")))
    engine = next(e for e in bundle.engines if red_unit in e.unit_ids)
    group = next(h.group for h in book.holdings if str(h.holding_id) == str(red_unit))
    column_cubes = {}
    for name, action in _lens_actions(red_unit, group).items():
        column_cubes[name] = engine.column_flows(red_unit, action, cube1)
        TRACE.call("AssetEngine", "column_flows")
    lp, sol, duals, tree_h = fixture_h("canonical")
    p1, glide = fixture_phase1("canonical")
    sol2 = phase2(lp, p1, glide, tree_h)
    kernel, ftp, env = price(sol2, lp, tree_h, tax)
    red_group = tax.red_tier()[0]
    cols = ColumnPool(tree_hash=tree_h.tree_hash, columns=tuple(
        Column(col_id=f"sell:{key.idx[0][1]}", unit_id=UnitId(str(key.idx[0][1])), group=red_group,
               action=LensAction(unit_id=UnitId(str(key.idx[0][1])), group=red_group, lens=Lens.SELL,
                                 instrument="lp_secondary_sale", size_bn=0.5, exposure_delta_bn=-0.5,
                                 financing_delta_bn=0.0, cash_out_bn=0.44),
               node_coeffs_ref=ArtifactRef.make(sim.manifest.run_id, "columns", f"/{j}"), cost=0.0, consent_p=1.0,
               lag_q=0, min_ticket_bn=0.05, irreversible=True)
        for j, key in enumerate(lp.col_keys) if key.family == "lens"))
    selection = select(lp, sol2, cols, basis=None)
    decisions = [str(k) for k in lp.col_keys if k.family == "decision"]
    a_row = lp.A.toarray()[0]
    proposal = ActionProposal(source="optimizer", lens_actions=(), root_values={
        **sol2.root_values, decisions[0]: 0.9 * sol2.root_values[decisions[0]]})        # 10% less revolver
    x_prop = np.array([proposal.root_values[n] for n in decisions])
    g0 = float(lp.row_lo[0] - a_row[:len(decisions)] @ x_prop - a_row[len(decisions):] @ sol2.x[len(decisions):])
    rows = LinearizedTier1(row_keys=(T4_ROW,), action_names=tuple(decisions), G=-a_row[None, :len(decisions)].copy(),
                           g0=np.array([g0]), delta=np.zeros(1), fd_checked=True)
    safe = project(proposal, state0, ls0=ls0, rows=rows, q_weights={},
                   exact_check=lambda p: ExactCheck(passed=True, violations={}, simm_im_bn=0.0, ov3_share=0.0,
                                                    recomputed_rows=(str(T4_ROW),)))
    evaluator = FakeEvaluator()
    _evaluator_calls(evaluator, sim.manifest.run_id)
    register = mini_register()
    room = FakeRoom(register, synthetic_committee(register, seed=ROOT_SEED), evaluator)
    plan = room.compile_agenda(contract.quarter, book.content_hash)
    TRACE.call("RoomPort", "compile_agenda")
    assert room.build_briefs(plan)
    TRACE.call("RoomPort", "build_briefs")
    assert room.run_shadow_ic(tuple(plan.by_decision))
    TRACE.call("RoomPort", "run_shadow_ic")
    assert room.lock_prevotes(contract.quarter)
    TRACE.call("RoomPort", "lock_prevotes")
    records = room.record_decisions(contract.quarter)
    TRACE.call("RoomPort", "record_decisions")
    backend = FakeLLMBackend(outputs={MemoDraft: MemoDraft(doc_kind="memo", template_text=SYNTHETIC_FOOTER)},
                             tool_calls=(("get_metric", {"metric_id": "tier1.t6.cp_upper@v1"}),))
    parsed, ran = _llm(backend, evaluator)
    TRACE.keep(beliefs, sim.metrics, sim.group_rates, rates_m6, tree, tree_h, lp, sol, sol2, duals, ls0,
               stress_report, *cubes.values(), *column_cubes.values(), rows)
    return Skeleton(book=book, sim=sim, rates_m6=rates_m6, cubes=cubes, tree=tree, lp=lp, sol=sol, sol2=sol2, p1=p1,
                    glide=glide, kernel=kernel, ftp=ftp, envelopes=env, selection=selection, safe=safe,
                    column_cubes=column_cubes, stress_report=stress_report, row_slacks=slacks, evaluator=evaluator,
                    room_records=records, llm_parsed=parsed, llm_tools=ran)


# ================================================================================================= tests
def test_every_protocol_method_is_called_end_to_end(skeleton: Skeleton) -> None:
    expected = {(name, method) for name, proto in PROTOCOLS.items() for method in protocol_methods(proto)}
    missing = sorted(expected - TRACE.calls)
    assert not missing, f"Protocol methods the skeleton never called: {missing}"


def test_every_container_validates_against_array_specs(skeleton: Skeleton) -> None:
    names = {type(o).__name__ for o in TRACE.containers}
    assert {"ScenarioCube", "BeliefSet", "BeliefDraws", "NoiseSlice", "ActionSlice", "FlowSlice",
            "RecourseAvailability", "RecourseOutcome", "LedgerState", "StressReport", "PathMetrics", "GroupRates",
            "Tree", "LPModel", "HSolution", "DualSet", "FlowCube", "LinearizedTier1"} <= names
    for obj in TRACE.containers:
        assert type(obj).__name__ in ARRAY_SPECS, type(obj).__name__
        obj.validate()


def test_money_fields_are_usd_bn_and_plausible(skeleton: Skeleton) -> None:
    """Units (§1.2, S-ADR-04): every money field is declared in $bn and holds book-scale values (|x| ≪ 1e4)."""
    checked = 0
    for obj in TRACE.containers:
        for name, spec in ARRAY_SPECS[type(obj).__name__].items():
            assert spec.units, f"{type(obj).__name__}.{name} declares no unit"
            if "$bn" not in spec.units or spec.kind not in ("array", "mapping"):
                continue
            value = getattr(obj, name)
            arrays = list(value.values()) if isinstance(value, Mapping) else ([] if value is None else [value])
            for arr in arrays:
                assert np.isfinite(arr).all() and float(np.abs(arr).max(initial=0.0)) < 1e4, \
                    f"{type(obj).__name__}.{name}"
                checked += 1
    assert checked > 20
    assert np.allclose(skeleton.sim.metrics.quarterly[:, 0, 0], 177.0, atol=1e-4), "t0 NAV is the book's $177bn"


def test_ledger_identity_is_exact_every_month(skeleton: Skeleton) -> None:
    """Δtreasury = booked flows − flows of units sold earlier in the quarter + instalment + facility draws +
    recourse proceeds (+ the unpaid instalment), to 1e-10 $bn per path-month (§3.17, §4.14)."""
    assert len(TRACE.cash_residuals) == 3 * (QUARTERS + TREE_QUARTERS)
    assert max(TRACE.cash_residuals) <= 1e-10
    assert TRACE.min_cash_bn >= 0.0, "the waterfall keeps cash non-negative"
    # The fake cannot quote the liquid sleeves (RecourseAvailability.tier admits only amber and red), so a few
    # long-crisis paths exhaust it; they are flagged failed and kept in the metrics (never dropped; §1.5).
    terminal = skeleton.sim.metrics.terminal
    failed = terminal[:, list(skeleton.sim.metrics.meta.terminal_names).index("failed")]
    assert TRACE.failed_paths <= 0.05 * N_PATHS
    assert terminal.shape[0] == N_PATHS and int(failed.sum()) <= TRACE.failed_paths


def test_recourse_protocol_ran(skeleton: Skeleton) -> None:
    """Quotes → waterfall → outcome → apply_recourse: discretionary and recourse sales both happened, the
    recourse proceeds were booked once by the ledger and red-tier recourse sales were flagged red."""
    assert TRACE.sale_proceeds_bn > 0, "the policy's discretionary sale booked engine proceeds"
    assert TRACE.proceeds_bn > 0, "the recourse waterfall sold units on some paths"
    assert TRACE.red_sales > 0


def test_p_produces_path_metrics_group_rates_and_manifest(skeleton: Skeleton) -> None:
    sim = skeleton.sim
    assert sim.metrics.quarterly.shape == (N_PATHS, 41, 3)
    assert sim.metrics.terminal.shape == (N_PATHS, len(REQUIRED_TERMINAL_SERIES))
    assert sim.group_rates is not None and sim.group_rates.delta.shape[:2] == (N_PATHS, TREE_QUARTERS)
    assert sim.manifest.data_class is DataClass.SYNTHETIC and sim.manifest.run_mode is RunMode.DEV_SYNTHETIC
    assert sim.manifest.canonical_artifact_hashes["metrics"] == canonical_artifact_hash(sim.metrics)


def test_tree_pools_the_worlds_and_carries_group_rates(skeleton: Skeleton) -> None:
    assert skeleton.tree.pooled_worlds == ("M1", "M6")
    for w, cube in skeleton.cubes.items():
        assert cube.group_rates is not None and cube.group_rates.meta.world_id == w
        assert cube.group_rates.meta.cube_checksum == cube.meta.checksum


def test_h_chain_phase2_price_select_project(skeleton: Skeleton) -> None:
    sk = skeleton
    assert sk.p1.mode is ContractMode.EXECUTION_RECOVERY and sk.sol2.priced_on is PricedOn.RESTORED
    assert sk.sol2.recovery_hash == sk.p1.recovery_hash == sk.glide.recovery_hash
    assert sk.sol2.objective == pytest.approx(sk.sol.objective, abs=1e-15)
    assert np.allclose(sk.sol2.duals.pi_row, sk.sol.duals.pi_row, atol=1e-15)
    assert sk.kernel.priced_on is PricedOn.RESTORED and len(sk.kernel.pi) == sk.tree.p.size
    assert sk.ftp.tolerance and all(p.decision_q >= 0 for p in sk.ftp.tolerance)
    assert sum(e.value_bn for e in sk.envelopes.envelopes) == pytest.approx(sk.envelopes.pool_bn[str(T4_ROW)])
    assert sk.selection.chosen and all(c.startswith("sell:") for c in sk.selection.chosen)
    assert sk.safe.projected and sk.safe.changed and sk.safe.exact_recheck_passed
    assert sk.safe.binding_rows == (str(T4_ROW),)


def test_column_cubes_honour_lever_equals_add_plus_refi(skeleton: Skeleton) -> None:
    c = skeleton.column_cubes
    lever = c["LEVER"].values.astype(np.float64)
    parts = c["ADD"].values.astype(np.float64) + c["REFINANCE"].values.astype(np.float64)
    assert np.allclose(lever, parts, rtol=1e-6, atol=1e-7)
    assert c["SELL"].meta.action is not None and c["SELL"].values.shape[1:] == (40, 1, 18)


def test_evaluator_room_and_llm_ports(skeleton: Skeleton) -> None:
    calls = skeleton.evaluator.calls
    assert tuple(calls[:len(EVALUATOR_METHODS)]) == EVALUATOR_METHODS        # then the room's and the LLM's reads
    assert calls.count("implied_actions") == 3 and calls[-1] == "get_metric"
    records = skeleton.room_records
    assert [r.prev_hash for r in records[1:]] == [r.record_hash for r in records[:-1]]
    assert all(r.data_class is DataClass.SYNTHETIC for r in records)
    assert all(b.rationale.startswith(SYNTHETIC_FOOTER) for r in records for b in r.ballots)
    assert isinstance(skeleton.llm_parsed.parsed, MemoDraft)
    assert skeleton.llm_tools.content[0]["type"] == "tool_result"


def test_stress_replica_and_row_slacks(skeleton: Skeleton) -> None:
    rep = skeleton.stress_report
    assert rep.headroom_bn.shape == (N_PATHS, 24) and set(rep.survival_months) == set(rep.cbc_bn)
    assert {k.family for k in skeleton.row_slacks} <= set(RowFamily)


# ======================================================================================== signature drift
@pytest.mark.parametrize("proto_name", sorted(set(PROTOCOLS) - {"EvaluatorPort"}))
def test_protocols_match_the_spec(proto_name: str) -> None:
    """``contracts.ports`` Protocols equal §3.17 verbatim (names, kinds, defaults, annotations, returns)."""
    spec, proto = getattr(SPEC, proto_name), PROTOCOLS[proto_name]
    assert set(protocol_methods(proto)) == set(protocol_methods(spec)), proto_name
    for method in protocol_methods(spec):
        assert canon(getattr(proto, method)) == canon(getattr(spec, method)), f"{proto_name}.{method} drifted"


def _fake(proto_name: str) -> Any:
    tax = GroupRegistry.for_version("v2")
    ctx = PolicyContext(idx=mini_book().unit_index(), tax=tax, p0_theta={}, recourse=_ORDER,
                        mandate_mode=MandateMode.B_OWNER_CALL, archetype_params={}, contract_hash="x")
    return {"AssetEngine": lambda: fake_engines(mini_book())[0], "Ledger": lambda: FakeLedger(tax),
            "EngineFactory": lambda: FakeEngineFactory(mini_owner_config()),
            "Policy": lambda: FakePolicy(ctx, 2, n_lots=3, n_facilities=2), "LLMBackend": FakeLLMBackend,
            "RoomPort": lambda: FakeRoom(mini_register(), synthetic_committee(mini_register(), 1), FakeEvaluator()),
            "EvaluatorPort": FakeEvaluator}[proto_name]()


@pytest.mark.parametrize("proto_name", sorted(PROTOCOLS))
def test_fakes_conform_to_the_protocols(proto_name: str) -> None:
    """Every fake is an instance of its runtime-checkable Protocol and keeps each method's parameters exactly
    (a return type may narrow, e.g. tuple for Sequence)."""
    fake, proto = _fake(proto_name), PROTOCOLS[proto_name]
    assert isinstance(fake, proto)
    for method in protocol_methods(proto):
        assert canon(getattr(type(fake), method), with_return=False) == \
            canon(getattr(proto, method), with_return=False), f"{type(fake).__name__}.{method}"


@pytest.mark.parametrize("name", SPEC_FUNCTIONS)
def test_stand_ins_match_the_spec(name: str) -> None:
    assert canon(globals()[name]) == canon(getattr(SPEC, name)), f"stand-in {name} drifted from §4"


@pytest.mark.parametrize("name", SPEC_FUNCTIONS)
def test_landed_implementations_match_the_spec(name: str) -> None:
    """Once a work package lands its function, its signature must equal §4's; until then the stand-in runs."""
    found = None
    for module in LANDING[name]:
        try:
            mod = importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        if hasattr(mod, name):
            found = getattr(mod, name)
            break
    if found is None:
        pytest.skip(f"{name}: not landed yet; the stand-in runs in the skeleton")
    assert refines(found, getattr(SPEC, name)), \
        f"{name} drifted from BUILD_SPEC §4: {canon(found)} vs {canon(getattr(SPEC, name))}"


def test_canon_detects_drift() -> None:
    """The drift detector itself works: renamed, re-typed, re-kinded or re-defaulted parameters are caught."""
    def base(a: int, *, b: str | None = None) -> float: ...
    def renamed(x: int, *, b: str | None = None) -> float: ...
    def retyped(a: float, *, b: str | None = None) -> float: ...
    def positional(a: int, b: str | None = None) -> float: ...
    def defaulted(a: int, *, b: str | None = "x") -> float: ...
    def returns(a: int, *, b: str | None = None) -> int: ...
    def optional(a: int, *, b: Optional[str] = None) -> float: ...  # noqa: F821
    def refined(a: int, *, b: str | None = None, validate: bool = False) -> float: ...
    def required_extra(a: int, *, b: str | None = None, mode: str) -> float: ...
    for other in (renamed, retyped, positional, defaulted, returns):
        assert canon(other) != canon(base), other.__name__
        assert not refines(other, base), other.__name__
    assert canon(optional) == canon(base)
    assert refines(refined, base) and not refines(required_extra, base)     # §0.2: defaulted additions only
    assert _norm("np.ndarray") == "ndarray" and _norm('"Basis | None"') == "Basis|None"
