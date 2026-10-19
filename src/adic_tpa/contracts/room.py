"""Decision-room contracts (BUILD_SPEC v1.1 §3.16; ARCH §8; S-ADR-22, -36; CHAT_ANALYST §5.5).

Seat numbers come only from engine outputs (``implied_actions``); LLM roles emit draft models
(``SeatArgumentDraft``, ``ViewSpecDraft``, ``ScenarioSpecDraft``) and deterministic code assembles the records.
``ViewSpec.confirmed`` and ``author_hash`` are set only by a human confirmation step; client-attested
confirmations no longer exist (``confirmation_surface`` per CHAT_ANALYST §5.5).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import model_validator

from adic_tpa.contracts.claims import RenderedDocument
from adic_tpa.contracts.contract import SignOff
from adic_tpa.contracts.enums import (
    ConsentScenario, ContractModel, DataClass, EvidencePlane, KeyValue, ModelFamily, OptionKind, Plane, PricedOn,
    RoleId, Tier,
)
from adic_tpa.contracts.ids import ArtifactRef, DecisionId, GroupId, MetricId, RunId
from adic_tpa.contracts.policy import PolicyRef

__all__ = [
    "EvidenceSpec", "DecisionVariable", "SignpostRule", "DecisionType", "Register", "RunSpec", "EvidencePlan",
    "Theta", "SeatSpec", "SeatAssessment", "MinorityReport", "PreVote", "Ballot", "OptionSummary", "Signpost",
    "ContingentAction", "OutcomeScore", "DecisionRecord", "ViewSpecDraft", "SeatArgumentDraft", "ViewSpec",
    "ScenarioSpecDraft", "ScenarioSpec", "EPResult",
]


class EvidenceSpec(ContractModel):
    metric: MetricId
    by: tuple[str, ...] = ()
    plane: EvidencePlane = EvidencePlane.SEALED
    max_age_days: int = 31


class DecisionVariable(ContractModel):
    name: str
    unit: str
    bounds: tuple[float, float] | None = None


class SignpostRule(ContractModel):
    count_min: int = 3
    count_max: int = 6
    alarm_sigma: float = 0.5
    rearm_sigma: float = 0.25


class DecisionType(ContractModel):
    id: str
    title: str
    proposer: str
    decider: str
    tier: Tier | None
    cadence: Literal["quarterly", "annual", "event", "monthly", "dealing_dates", "budget_cycle"]
    deadline_rule: str
    variables: tuple[DecisionVariable, ...]
    always_show: tuple[OptionKind, ...] = (OptionKind.STATUS_QUO, OptionKind.DEFER, OptionKind.RECOMMENDED)
    evidence: tuple[EvidenceSpec, ...]
    signposts: SignpostRule
    increment: Literal["1", "v1"]


class Register(ContractModel):
    version: str
    entries: tuple[DecisionType, ...]
    signoffs: tuple[SignOff, ...]
    hash: str


class RunSpec(ContractModel):
    tool: str
    args: dict[str, Any]
    plane: Plane
    spec_hash: str


class EvidencePlan(ContractModel):
    specs: tuple[RunSpec, ...]
    edges: tuple[tuple[str, str], ...]
    by_decision: dict[str, tuple[str, ...]]
    hash: str


class Theta(ContractModel):
    """Admissible value set Θ (ARCH §8.5; S-ADR-06)."""

    gamma: float                                 # [2, 6]
    lambda_T: float                              # [0, 2]
    shortfall_exponent: float                    # (1, 3]
    t6_limit: float                              # <= the IC tolerance band
    extra_costs: dict[MetricId, float] = {}      # engine metrics only; no indicator or probability terms

    @model_validator(mode="after")
    def _admissible(self) -> Theta:
        if not 2.0 <= self.gamma <= 6.0:
            raise ValueError("Theta.gamma must lie in [2, 6]")
        if not 0.0 <= self.lambda_T <= 2.0:
            raise ValueError("Theta.lambda_T must lie in [0, 2]")
        if not 1.0 < self.shortfall_exponent <= 3.0:
            raise ValueError("Theta.shortfall_exponent must lie in (1, 3] (S-ADR-06)")
        if not 0.0 <= self.t6_limit <= 1.0:
            raise ValueError("Theta.t6_limit is a probability")
        return self


class SeatSpec(ContractModel):
    seat_id: str
    mandate: str                                 # "PE mandate (AI seat)" — never a person's name
    belief_channel: Literal["base_mixture", "worst_class", "base_plus_owner_stress", "group_forecasts",
                            "reference_class", "min_kl_failure"]
    group: GroupId | None
    theta: Theta | None
    family: ModelFamily
    recuse_on: tuple[GroupId, ...] = ()


class SeatAssessment(ContractModel):
    """Assembled by ``idm.seats`` from engine outputs and a ``SeatArgumentDraft``; never an LLM output."""

    seat_id: str
    item_id: str
    implied_action_ref: ArtifactRef
    regret_bp: dict[str, float]                  # engine numbers (implied_actions)
    belief_value_split: tuple[float, float]
    event_probs_ref: ArtifactRef                 # engine probabilities of the frozen-question events
    cruxes: tuple[str, ...]
    argument: RenderedDocument
    hash: str


class MinorityReport(ContractModel):
    author: str
    item_id: str
    document: RenderedDocument
    authentic: bool                              # Red Team: authentic=False ("assigned dissent")
    trigger: Literal["dp15", "regret10", "member"]
    hash: str


class PreVote(ContractModel):
    member_hash: str
    item_id: str
    choice: Literal["approve", "resize", "defer", "reject"]
    probabilities: dict[str, float]
    rationale: str
    locked_at: datetime
    hash: str


class Ballot(ContractModel):
    member_hash: str
    item_id: str
    choice: Literal["approve", "resize", "defer", "reject"]
    probabilities: dict[str, float]
    rationale: str
    what_would_change: str
    recused: bool
    second_chance_ack: bool
    how_could_be_wrong: str | None
    cast_at: datetime
    hash: str


class OptionSummary(ContractModel):
    kind: OptionKind
    label: str
    policy_ref: PolicyRef | None
    delta_ce_bp: MetricId
    p_red_by_class: dict[str, MetricId]
    p10_target: MetricId
    delta_survival_months: MetricId


class Signpost(ContractModel):
    indicator: MetricId
    flip_value: float
    alarm_value: float
    rearm_band: float
    sigma: float
    owner: str
    state: Literal["armed", "alarm", "flipped", "rearmed"] = "armed"


class ContingentAction(ContractModel):
    condition: str
    action: str
    tier: Tier


class OutcomeScore(ContractModel):
    horizon: Literal["q1", "q4", "q8"]
    brier: float
    resolved_at: date
    detail: dict[str, float]


class DecisionRecord(ContractModel):
    """ARCH §8.9 verbatim, plus data_class and the hash chain."""

    decision_id: DecisionId
    register_id: str
    as_of: date
    tier: Literal["A", "B", "C", "Board"]
    options: tuple[OptionSummary, ...]
    engine_recommendation: str
    evidence_plane: Literal["sealed", "search", "exploratory"]
    run_manifests: tuple[RunId, ...]
    priced_on: PricedOn
    consent_scenario: ConsentScenario
    recovery_hash: str | None
    prevote_hashes: tuple[str, ...]
    ballots: tuple[Ballot, ...]
    decision: str
    override: Literal["belief", "value", "info_outside_model", "implementation", "legal_consent", "relationship",
                      "other"] | None
    rationale: str
    minority_reports: tuple[str, ...]
    signposts: tuple[Signpost, ...]
    commitment_plan: tuple[ContingentAction, ...]
    review_date: date
    outcomes: dict[Literal["q1", "q4", "q8"], OutcomeScore] = {}
    data_class: DataClass
    prev_hash: str
    record_hash: str


class ViewSpecDraft(ContractModel):
    """What the Translator, a seat narrator or the analyst may emit (LLM-facing)."""

    channel: Literal["FBE", "EP"]
    metric: str
    operator: Literal["eq", "le", "ge"]
    value: float
    confidence_c: float = 0.6
    horizon_q: int | None = None


class SeatArgumentDraft(ContractModel):
    """LLM draft model of a seat narrator (S-ADR-36); beliefs change only through typed views."""

    seat_id: str
    item_id: str
    cruxes: tuple[str, ...]
    template_text: str
    view_proposals: tuple[ViewSpecDraft, ...] = ()


class ViewSpec(ContractModel):
    """Assembled by code; ``confirmed`` and ``author_hash`` are set only by a human confirmation step."""

    view_id: str
    draft: ViewSpecDraft
    author_hash: str
    confirmed: bool = False
    confirmed_by: str | None = None
    confirmation_surface: Literal["tpa_chat", "ask_service", "tpa_analyst_confirm", "room_console"] | None = None

    @model_validator(mode="after")
    def _confirmation(self) -> ViewSpec:
        if self.confirmed and (self.confirmed_by is None or self.confirmation_surface is None):
            raise ValueError("a confirmed view names who confirmed it and on which surface")
        if not self.confirmed and (self.confirmed_by is not None or self.confirmation_surface is not None):
            raise ValueError("an unconfirmed view carries no confirmation fields")
        return self


class ScenarioSpecDraft(ContractModel):
    """LLM-facing (red team): targets as a ``KeyValue`` list, not a dict."""

    kind: Literal["tilt", "param_shift", "named"]
    targets: tuple[KeyValue, ...]
    kl_bound: float


class ScenarioSpec(ContractModel):
    spec_id: str
    kind: Literal["tilt", "param_shift", "named"]
    targets: dict[str, float]
    kl_bound: float
    author_role: RoleId


class EPResult(ContractModel):
    weights_ref: ArtifactRef
    kl: float
    ess: float
    max_ratio: float
    effective_views: tuple[ViewSpec, ...]
    flags: tuple[Literal["inform", "warn", "amber", "red", "ess_block"], ...]
