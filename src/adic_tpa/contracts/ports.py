"""Ports: the cross-WP Protocols and contexts (BUILD_SPEC v1.1 §3.17, §3.18; S-ADR-24, -28, -29, -43).

The walking skeleton (WP-03) calls every Protocol method here once, end to end on ``mini_book`` with fakes.

``LLMRequest``, ``LLMResponse``, ``ToolDef`` and ``ToolExecutor`` are defined here rather than in ``agents``:
``contracts`` may import no other ``adic_tpa`` package (§4.0), the ``LLMBackend`` Protocol needs them, and the
wave-0 skeleton must call ``LLMBackend`` before ``agents`` (wave 4) exists. ``agents`` re-exports them and builds
``ToolRegistry`` on top. Result types defined outside ``contracts`` (``RobustnessCard``, ``SimmResult``,
``OVReport``) are typed ``BaseModel`` in ``EvaluatorPort``.

``LLM_OUTPUT_MODELS`` and ``LLM_TOOL_INPUT_MODELS`` list every LLM-facing schema; ``check_llm_schema`` (agents)
and ``tests/unit/test_llm_facing_schemas.py`` run on all of them (S-ADR-36). Deliberately absent:

- ``Escalation`` (the ``escalate`` input of ``EvaluatorPort``): roles fill ``EscalationDraft`` and the lab firewall
  assembles the ledger row, because ``raised_at``, ``resolved_by`` and ``resolution`` are system- or human-owned.
- ``OptimizeHIn`` and ``EPIn``: §7.4 lists the TRANSLATOR among their callers, but they carry ``ViewSpec``s whose
  ``confirmed``, ``confirmed_by`` and ``author_hash`` are human-owned. The TRANSLATOR emits ``ViewSpecDraft``s
  (``draft_viewspec``); after a human confirms the effective view, the room or the firewall builds the request
  from the confirmed ``ViewSpec``s. No LLM fills these two models (a contract note for WP-25/WP-27).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Final, Protocol, runtime_checkable

from pydantic import BaseModel

from adic_tpa.contracts.actions import FlipThresholds, LensAction
from adic_tpa.contracts.analyst import ANALYST_TOOLS, AnswerDraft
from adic_tpa.contracts.arrays import F32
from adic_tpa.contracts.beliefs import BeliefDraws, BeliefSet, BridgeCard
from adic_tpa.contracts.book import BookSnapshot, UnitIndex
from adic_tpa.contracts.claims import AuditDraft, MemoDraft, ProvenanceNode, RenderedDocument, ValidationReport
from adic_tpa.contracts.engine_io import ActionSlice, EngineState, FlowCube, FlowSlice, NoiseRequest, NoiseSlice, WorldSlice
from adic_tpa.contracts.enums import Clock, MandateMode, ModelFamily, Plane, RoleId, WorldId
from adic_tpa.contracts.evidence import EvalRequest, EvalResultAgentView, LLMCallRecord, MetricInstance
from adic_tpa.contracts.ids import GroupId, MetricId, UnitId
from adic_tpa.contracts.lab import AmendmentDraft, AssumptionEntry, Escalation, EscalationDraft, IdeaBundle
from adic_tpa.contracts.ledger import LedgerState, RecourseAvailability, RecourseOutcome, StressReport, StressSpec
from adic_tpa.contracts.optimizer import RowKey
from adic_tpa.contracts.overlay import CRIFRow
from adic_tpa.contracts.policy import ActionPackage, Observables, OverlayStructure, PolicyRef, PolicySpec, RecourseOrder
from adic_tpa.contracts.room import DecisionRecord, EPResult, EvidencePlan, ScenarioSpecDraft, SeatArgumentDraft, SeatAssessment, ViewSpecDraft
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.tools import (
    Ack, AttributeIn, AttributionCard, CardIdsIn, EnvelopeSummary, EPIn, EVSIIn, EVSIResult, ExtractionRecord, FlipIn,
    HSummary, HybridCheck, ImpliedActionCard, ImpliedIn, MetricListIn, MetricQueryIn, OffsetCard, OptimizeHIn,
    PackagePrice, Phase1Card, Phase1In, ProvenanceQueryIn, ReverseStressIn, ReverseStressResult, ReviewFindings,
    ScenarioResult, StateCard, StateSnapshotIn, TradePrice, TypeReport, ValidateClaimsIn, VariantSet,
)
from adic_tpa.contracts.world import OwnerConfig, ScenarioCube, StateSnapshot, StressFilterParams, TreeSpec, WorldSpec

__all__ = [
    "AssetEngine", "Ledger", "EngineFactory", "EngineBundle", "Policy", "LLMBackend", "EvaluatorPort", "RoomPort",
    "PolicyContext", "SimContext", "EngineContext", "LLMRequest", "LLMResponse", "ToolDef", "ToolExecutor",
    "LLM_OUTPUT_MODELS", "LLM_TOOL_INPUT_MODELS",
]


@runtime_checkable
class AssetEngine(Protocol):
    """priv.*, pub.*, overlay (ARCH §3.5 v1.1; S-ADR-28/29). Engines add only α to the world's beta return."""

    engine_id: str
    groups: tuple[GroupId, ...]
    clock: Clock

    def init(self, book: BookSnapshot, beliefs: BeliefSet, n_paths: int, *, draws: BeliefDraws,
             world: WorldSpec) -> EngineState: ...

    def noise_requests(self, t: int) -> Sequence[NoiseRequest]: ...

    def recourse_quotes(self, t: int, st: EngineState, world: WorldSlice) -> RecourseAvailability:
        """Phase 1 of the recourse protocol, at quarter start."""
        ...

    def step(self, t: int, st: EngineState, world: WorldSlice, act: ActionSlice, noise: NoiseSlice) -> FlowSlice: ...

    def apply_recourse(self, st: EngineState, outcome: RecourseOutcome) -> None:
        """Phase 3: scale sold units before t + 1."""
        ...

    def column_flows(self, unit_id: UnitId, action: LensAction, cube: ScenarioCube) -> FlowCube: ...


@runtime_checkable
class Ledger(Protocol):
    def apply(self, m: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: F32,
              quotes: RecourseAvailability) -> tuple[LedgerState, RecourseOutcome]:
        """Phase 2 of the recourse protocol; books proceeds once."""
        ...

    def row_slacks(self, ls: LedgerState) -> dict[RowKey, F32]: ...

    def stress_replica(self, ls0: LedgerState, stress: StressSpec) -> StressReport: ...


@runtime_checkable
class Policy(Protocol):
    policy_ref: PolicyRef

    def act(self, q: int, obs: Observables) -> ActionSlice:
        """``obs`` is lagged; no horizon, path id or world id."""
        ...


@dataclass(frozen=True)
class EngineBundle:
    engines: tuple[AssetEngine, ...]
    ledger: Ledger
    owner_cfg: OwnerConfig
    policy_wrappers: tuple[Callable[[Policy], Policy], ...]   # e.g. playbook slippage (one-quarter delay, 50% fills)
    effective_config_hashes: Mapping[str, str]


@runtime_checkable
class EngineFactory(Protocol):
    """Implemented by ``core.sim.factory.DefaultEngineFactory`` (S-ADR-43)."""

    def build(self, book: BookSnapshot, world: WorldSpec) -> EngineBundle:
        """Applies ``world.overrides``; hashes effective configs."""
        ...


@dataclass(frozen=True)
class ToolDef:
    """A strict tool definition as sent to the model: ``{"name", "description", "input_schema", "strict"}``."""

    name: str
    description: str
    input_schema: Mapping[str, Any]
    strict: bool = True


@runtime_checkable
class ToolExecutor(Protocol):
    def __call__(self, tool_use_id: str, name: str, tool_input: Mapping[str, Any]) -> Mapping[str, Any]:
        """Run one tool call; return one ``tool_result`` content block
        (``{"type": "tool_result", "tool_use_id", "content", "is_error"}``)."""
        ...


@dataclass(frozen=True)
class LLMRequest:
    """§4.29 (BUILD-34)."""

    role: RoleId
    model: str
    system: str
    messages: tuple[dict[str, Any], ...]
    tools: tuple[ToolDef, ...]
    effort: str
    max_tokens: int = 16000
    thinking: Mapping[str, str] = field(default_factory=lambda: {"type": "adaptive"})


@dataclass(frozen=True)
class LLMResponse:
    """§4.29."""

    content: tuple[dict[str, Any], ...]
    parsed: BaseModel | None
    stop_reason: str
    served_model: str
    usage: Mapping[str, int]
    record: LLMCallRecord


@runtime_checkable
class LLMBackend(Protocol):
    family: ModelFamily

    def parse(self, req: LLMRequest, output_model: type[BaseModel]) -> LLMResponse: ...

    def run_tools(self, req: LLMRequest, tools: Sequence[ToolDef], executor: ToolExecutor) -> LLMResponse: ...


@runtime_checkable
class EvaluatorPort(Protocol):
    """One typed method per evaluator tool (§7.4); in-process or MCP client."""

    def state_snapshot(self, req: StateSnapshotIn) -> StateCard: ...
    def phase1_restore(self, req: Phase1In) -> Phase1Card: ...
    def compile_spec(self, spec: PolicySpec) -> TypeReport: ...
    def evaluate_policy(self, req: EvalRequest) -> EvalResultAgentView: ...
    def price_actions(self, package: ActionPackage) -> PackagePrice: ...
    def optimize_h(self, req: OptimizeHIn) -> HSummary: ...
    def evaluate_scenario(self, spec: ScenarioSpecDraft) -> ScenarioResult: ...
    def reverse_stress(self, req: ReverseStressIn) -> ReverseStressResult: ...
    def implied_actions(self, req: ImpliedIn) -> ImpliedActionCard: ...
    def ep_condition(self, req: EPIn) -> EPResult: ...
    def evsi_crossfit(self, req: EVSIIn) -> EVSIResult: ...
    def flip_thresholds(self, req: FlipIn) -> FlipThresholds: ...
    def robustness_card(self, req: CardIdsIn) -> BaseModel: ...          # robust.RobustnessCard
    def bridge_card(self, req: CardIdsIn) -> BridgeCard: ...
    def group_envelopes(self, req: CardIdsIn) -> EnvelopeSummary: ...
    def overlay_offset_card(self, req: CardIdsIn) -> OffsetCard: ...
    def attribute(self, req: AttributeIn) -> AttributionCard: ...
    def price_trade(self, structure: OverlayStructure) -> TradePrice: ...
    def crif_sensitivities(self, structure: OverlayStructure) -> tuple[CRIFRow, ...]: ...
    def simm_like(self, structure: OverlayStructure) -> BaseModel: ...   # overlay.SimmResult
    def greek_offsets(self, structure: OverlayStructure) -> BaseModel: ...   # overlay.OVReport
    def hybrid_quote_check(self, structure: OverlayStructure) -> HybridCheck: ...
    def get_metric(self, req: MetricQueryIn) -> MetricInstance: ...
    def list_metrics(self, req: MetricListIn) -> tuple[MetricId, ...]: ...
    def get_provenance(self, req: ProvenanceQueryIn) -> ProvenanceNode: ...
    def validate_claims(self, req: ValidateClaimsIn) -> ValidationReport: ...
    def log_assumption(self, entry: AssumptionEntry) -> Ack: ...
    def escalate(self, e: Escalation) -> Ack: ...


@runtime_checkable
class RoomPort(Protocol):
    """Implemented by ``idm.room_service.RoomService``; injected by ``pipeline`` (S-ADR-24)."""

    def compile_agenda(self, quarter: str, snapshot_hash: str) -> EvidencePlan: ...
    def build_briefs(self, plan: EvidencePlan) -> tuple[RenderedDocument, ...]: ...
    def run_shadow_ic(self, items: Sequence[str]) -> tuple[SeatAssessment, ...]: ...
    def lock_prevotes(self, quarter: str) -> tuple[str, ...]: ...
    def record_decisions(self, quarter: str) -> tuple[DecisionRecord, ...]: ...


@dataclass(frozen=True)
class PolicyContext:
    """What native policies need beyond observables (BUILD-11)."""

    idx: UnitIndex
    tax: GroupRegistry
    p0_theta: Mapping[str, float]
    recourse: RecourseOrder
    mandate_mode: MandateMode
    archetype_params: Mapping[str, Mapping[str, float]]
    contract_hash: str


@dataclass(frozen=True)
class SimContext:
    factory: EngineFactory
    book: BookSnapshot
    beliefs: BeliefSet
    state0: StateSnapshot
    worlds: Mapping[WorldId, WorldSpec]
    owner_cfg: OwnerConfig
    filter_params: StressFilterParams
    root_seed: int
    plane: Plane
    salt: bytes | None
    policy_ctx: PolicyContext
    contract_hash: str


@dataclass(frozen=True)
class EngineContext:
    """What ``core.mpc`` needs beyond the contract and snapshot."""

    sim: SimContext
    tree_spec: TreeSpec
    catalogue_cfg: Mapping[str, Any]
    solver_policy: Mapping[str, str]
    processes: int = 5


# Every LLM-facing schema (S-ADR-36): role output models (§7.5) and the tool inputs roles fill (§7.4, CHAT §5.2).
LLM_OUTPUT_MODELS: Final[tuple[type[BaseModel], ...]] = (
    AmendmentDraft, ReviewFindings, IdeaBundle, VariantSet, MemoDraft, AuditDraft, ViewSpecDraft, ScenarioSpecDraft,
    AnswerDraft, SeatArgumentDraft, ExtractionRecord,
)
LLM_TOOL_INPUT_MODELS: Final[tuple[type[BaseModel], ...]] = (
    StateSnapshotIn, Phase1In, PolicySpec, EvalRequest, ActionPackage, ScenarioSpecDraft, ReverseStressIn, ImpliedIn,
    EVSIIn, FlipIn, AttributeIn, CardIdsIn, MetricQueryIn, MetricListIn, ProvenanceQueryIn, ValidateClaimsIn,
    AssumptionEntry, EscalationDraft, OverlayStructure,
    *(t.input_model for t in ANALYST_TOOLS),
)
