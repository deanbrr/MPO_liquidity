"""Evaluator and lab tool I/O (BUILD_SPEC v1.1 §3.18, §7.4; CHAT_ANALYST §5.5, §14.3).

Each tool is a pair of strict models (JSON schema ``additionalProperties: false``; every field required or
defaulted). Adopted from CHAT_ANALYST §14.3 ahead of the freeze (additive, with defaults):
``TypedOverride.op`` and ``value: float | str``; ``ReverseStressIn.world_class``; ``OptimizeHIn.pricing_scenario``,
``forced_actions`` and ``availability``. WP-01 additions so that ``EvaluatorPort`` has one typed method per §7.4
tool: ``CardIdsIn`` (the ``{ids}`` input of the card tools), ``MetricQueryIn``, ``MetricListIn``,
``ProvenanceQueryIn``, ``ValidateClaimsIn``, ``FacilityAvailability`` and ``Ack``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from adic_tpa.contracts.actions import LensAction
from adic_tpa.contracts.enums import (
    ConsentScenario, ContractMode, ContractModel, EvidencePlane, KeyValue, ModelFamily, PricedOn, RecourseTier,
    StressState,
)
from adic_tpa.contracts.ids import ArtifactRef, CsaId, FacilityId, MetricId, RunId
from adic_tpa.contracts.ledger import CFPReading
from adic_tpa.contracts.optimizer import Envelope, FTPPoint, GlidePath
from adic_tpa.contracts.policy import PolicySpec
from adic_tpa.contracts.room import ViewSpec

__all__ = [
    "StateSnapshotIn", "StateCard", "Phase1In", "TierSummary", "Phase1Card", "TypedOverride", "FacilityAvailability",
    "OptimizeHIn", "HSummary", "PackagePrice", "ScenarioResult", "ReverseStressIn", "ReverseStressResult", "ImpliedIn",
    "ImpliedActionCard", "EPIn", "EVSIIn", "EVSIResult", "FlipIn", "AttributeIn", "AttributionCard",
    "EnvelopeSummary", "OffsetRow", "OffsetCard", "TradePrice", "HybridCheck", "TypeReport", "ReviewFindings",
    "VariantSet", "ExtractionRecord", "CardIdsIn", "MetricQueryIn", "MetricListIn", "ProvenanceQueryIn",
    "ValidateClaimsIn", "Ack", "WorldClass",
]

WorldClass = Literal["M1_M5", "M6", "MIX"]


class StateSnapshotIn(ContractModel):
    """No input."""


class StateCard(ContractModel):
    cfp: CFPReading
    F_t: float
    e0: tuple[float, ...]
    z0: tuple[float, ...]
    draw_12m_bn: tuple[float, float]
    t4p_survival_months: dict[RecourseTier, int]
    lambda_spot: dict[StressState, float]
    plane: EvidencePlane
    refs: tuple[ArtifactRef, ...]


class Phase1In(ContractModel):
    scenario: ConsentScenario | None = None


class TierSummary(ContractModel):
    tier: int
    u_star_bn: float
    iis: tuple[str, ...]
    levers_at_cap: tuple[str, ...]


class Phase1Card(ContractModel):
    by_scenario: dict[ConsentScenario, tuple[TierSummary, ...]]
    mode: ContractMode
    d0_bn: float
    glide: GlidePath | None
    pricing_scenario: ConsentScenario


class TypedOverride(ContractModel):
    target: str
    field: str
    value: float | str
    unit: str
    source_view_id: str
    op: Literal["set", "mult", "add"] = "set"    # CHAT_ANALYST §5.5 / §14.3


class FacilityAvailability(ContractModel):
    """A facility availability multiplier in a named stress state (the W2 ``Availability`` kind)."""

    facility_id: FacilityId
    state: StressState
    availability_frac: float


class OptimizeHIn(ContractModel):
    """Views must carry ``confirmed = True``; the tool returns ``HSummary`` (EXPLORATORY)."""

    preset: Literal["whatif"] = "whatif"
    views: tuple[ViewSpec, ...] = ()
    overrides: tuple[TypedOverride, ...] = ()
    pricing_scenario: ConsentScenario | None = None   # CHAT_ANALYST §14.3 (W2 consent kind)
    forced_actions: tuple[LensAction, ...] = ()       # CHAT_ANALYST §14.3 (W2 action-option kind)
    availability: tuple[FacilityAvailability, ...] = ()   # CHAT_ANALYST §14.3 (W2 availability kind)

    @model_validator(mode="after")
    def _confirmed(self) -> OptimizeHIn:
        if any(not v.confirmed for v in self.views):
            raise ValueError("optimize_h takes confirmed views only")
        return self


class HSummary(ContractModel):
    root_actions: tuple[LensAction, ...]
    lambda_spot: dict[StressState, float]
    ftp: tuple[FTPPoint, ...]
    envelopes: tuple[Envelope, ...]
    gamma_status: Literal["certified", "selection_not_certified"]
    priced_on: PricedOn
    plane: Literal["exploratory"] = "exploratory"
    run_ref: ArtifactRef


class PackagePrice(ContractModel):
    robust_rc_bucket: str
    dominated: bool


class ScenarioResult(ContractModel):
    dp_red_bucket: str
    binding_rows: tuple[str, ...]
    kl: float


class ReverseStressIn(ContractModel):
    metric: MetricId
    threshold: float
    world_class: WorldClass = "MIX"              # CHAT_ANALYST §5.5 / §14.3


class ReverseStressResult(ContractModel):
    kl: float
    tilt_ref: ArtifactRef
    ranking: tuple[tuple[str, float], ...]


class ImpliedIn(ContractModel):
    seat_id: str
    item_id: str


class ImpliedActionCard(ContractModel):
    seat_id: str
    item_id: str
    action: str
    regret_bp_by_option: dict[str, float]
    ref: ArtifactRef


class EPIn(ContractModel):
    views: tuple[ViewSpec, ...]


class EVSIIn(ContractModel):
    item_id: str


class EVSIResult(ContractModel):
    lb80_usd_m: float
    mean_usd_m: float
    folds: int
    cost_of_delay_usd_m: float


class FlipIn(ContractModel):
    card_id: str


class AttributeIn(ContractModel):
    run_id: RunId
    kind: Literal["shapley6", "group", "null", "what_moved"]


class AttributionCard(ContractModel):
    kind: str
    components: dict[str, tuple[float, float]]
    residual: float
    established: dict[str, bool]
    ref: ArtifactRef


class EnvelopeSummary(ContractModel):
    envelopes: tuple[Envelope, ...]
    pool_bn: dict[str, float]


class OffsetRow(ContractModel):
    stress: str
    pnl_tail_bn: float
    pnl_opp_bn: float
    offset_ratio: float
    nv_eq_economic: float
    nv_simm: float
    im_by_csa_bn: dict[CsaId, float]
    im_saving_priced_bn: float


class OffsetCard(ContractModel):
    rows: tuple[OffsetRow, ...]
    stress_coverage_ratio: float


class TradePrice(ContractModel):
    value_bn: float
    greeks_ref: ArtifactRef


class HybridCheck(ContractModel):
    implied_corr_spread: float
    q_vs_p_pass: bool
    accepted: bool


class TypeReport(ContractModel):
    passed: bool
    errors: tuple[tuple[str, str], ...]          # (code, detail), codes INVALID_SPEC/TR1..TR8


class ReviewFindings(ContractModel):
    findings: tuple[str, ...]
    severity: tuple[Literal["minor", "major"], ...]

    @model_validator(mode="after")
    def _aligned(self) -> ReviewFindings:
        if len(self.findings) != len(self.severity):
            raise ValueError("one severity per finding")
        return self


class VariantSet(ContractModel):
    variants: tuple[PolicySpec, ...]
    rationale: tuple[str, ...]


class ExtractionRecord(ContractModel):
    """``confidence`` is a QA diagnostic only; fields reach engines only after verification (S-ADR-36)."""

    doc_hash: str
    fields: tuple[KeyValue, ...]
    confidence: float
    extractor_family: ModelFamily


class CardIdsIn(ContractModel):
    """The ``{ids}`` input of ``robustness_card``, ``bridge_card``, ``group_envelopes``, ``overlay_offset_card``."""

    ids: tuple[str, ...] = ()


class MetricQueryIn(ContractModel):
    """Input of the evaluator's ``get_metric`` registry read."""

    metric_id: MetricId
    run_id: RunId | None = None
    plane: EvidencePlane | None = None
    by: tuple[KeyValue, ...] = ()


class MetricListIn(ContractModel):
    """Input of the evaluator's ``list_metrics`` registry read."""

    run_id: RunId | None = None
    prefix: str = ""


class ProvenanceQueryIn(ContractModel):
    """Input of the evaluator's ``get_provenance`` registry read."""

    ref: ArtifactRef


class ValidateClaimsIn(ContractModel):
    doc_id: str


class Ack(ContractModel):
    """Acknowledgement of a ledger write (``log_assumption``, ``escalate``)."""

    accepted: bool
    row_hash: str
