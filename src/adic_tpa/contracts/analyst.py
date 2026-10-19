"""Conversational-analyst contracts (CHAT_ANALYST v1.1 §5.1, §5.3, §5.5, §6.3, §11; BUILD_SPEC v1.1 §3.18,
S-ADR-34; frozen by WP-01 with contracts-v1.0, i.e. WP-CHAT-01).

Every tool result is a ``ToolResult[P]``; engine numbers and categoricals travel only as ``Fact`` objects under
session-unique handles (``F3.7`` = turn 3's seventh fact; ``E`` entities, ``Q`` quotes, ``T`` tables, ``U`` user
numbers, ``R`` run handles). Payload fields that point at numbers hold fact handles, never values.

LLM-facing input models (``ANALYST_TOOLS[*].input_model``) avoid root-level unions, free-form dicts (``KeyValue``
lists instead) and fixed-length tuples (``Interval``, ``CasePoint`` and other named sub-models); units are in field
names. Discriminator fields also emit a single-value ``enum`` so they stay enforceable after the SDK's
strict-schema transform. Strict schemas drop numeric bounds, so validators check bounds here and the service
re-checks override values against the MRM-signed allowlist.

Reconciliation with BUILD_SPEC v1.1 §3.18 (CHAT_ANALYST §5.5): ``Principal`` and ``ContextHandle`` gain fields;
``AnswerDraft``/``StatementDraft`` are the analyst's (the claims.py pair is retired); ``WhatIfDraft`` becomes
``OverrideDraft`` (service record) plus ``OverrideDraftView`` (model-facing); ``WhatIfConfirmation`` becomes the
Ed25519-signed ``OverrideConfirmation`` over a bundle hash, with no token (so there is no ``ConfirmToken``); BS's
``QuoteRef`` is ``QuoteView``. The BS names are exported as aliases. The catalogue has 34 tools (21 in increment 1).

The aliases below (``Fmt``, ``FactFlag``, ``RouteCode``, ...) are the closed enums of CHAT_ANALYST §5.3, with
members taken from the addendum's §4, §5.2, §6, §7.1, §9 and CQ §3; ``LeverId`` and ``ActionOptionKind`` name the
levers and options the addendum's examples use. Override parameter ids stay strings checked against the signed
allowlist, so a config change never reopens frozen contracts.

Provisional v1 shapes. CHAT_ANALYST v1.1 §5.3 says rows 16–23 and 34 "keep v1.0's shapes", but v1.0 is not on
disk, so their input and payload models (``GovernanceIn``, ``ImpliedActionsIn``, ``BindingIn``, ``AttributionIn``,
``CompareRunsIn``, ``GroupRollupIn``, ``TreasuryIn``, ``OverlayIn``, ``ChatAuditIn``; ``GovernanceView``,
``BindingView``, ``AttributionView``) are WP-01 reconstructions from §5.2's row descriptions. They are listed in
``PROVISIONAL_V1_TOOLS``, outside the contracts-v1.0 freeze guarantee: WP-40 confirms or replaces them before any
increment-1 code relies on them (none does; they are v1 tools). The analyst's row-17 and row-19 inputs are named
``ImpliedActionsIn`` and ``AttributionIn`` so they do not collide with the evaluator's ``tools.ImpliedIn`` and
``tools.AttributeIn`` (JSON-schema titles and ``$defs`` stay distinct); the addendum's names ``ImpliedIn`` and
``AttributeIn`` are aliases in this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Any, Final, Generic, Literal, TypeVar

from pydantic import BaseModel, Field, model_validator

from adic_tpa.contracts.claims import ProvenanceNode, RenderedDocument, ValidationReport
from adic_tpa.contracts.enums import (
    AllocationId, AnswerStatus, CensusId, CFPStage, ConsentScenario, ContractMode, ContractModel, DataClass,
    EvidencePlane, GateLabel, Interval, KeyValue, Lens, MarkType, PricedOn, StressState, WorldId,
)
from adic_tpa.contracts.evidence import LLMCallRecord
from adic_tpa.contracts.hashing import canonical_json, content_hash
from adic_tpa.contracts.ids import (
    ArtifactRef, CsaId, FacilityId, GroupId, HoldingId, MetricId, RunId, is_content_hash,
)
from adic_tpa.contracts.tools import WorldClass

__all__ = [
    # aliases
    "Fmt", "FactFlag", "QuoteSource", "RouteCode", "RuleId", "WithheldKind", "EntityKind", "PackSection",
    "HoldingSection", "HoldingFilterField", "HoldingSortKey", "CardFlag", "CardBlock", "PolicyCode", "OverrideKind",
    "ActionOptionKind", "LeverId", "GoalSeekTarget", "GoalSeekLever", "TradeTemplate", "WorldClass", "Output",
    "Composition", "GateFlag", "TierReason", "PolicyNote", "RunStatus", "Category", "Outcome", "AnswerStatus",
    "AttributionKind", "RunDiffScope", "GroupSection", "TreasurySection", "OverlaySection", "ToolErrorCode",
    "ToolStatus", "WTier", "Surface", "ConfirmSurface", "WallSide",
    # §5.1
    "Fact", "EntityRef", "QuoteView", "QuoteRef", "TableSpec", "Withheld", "ToolError", "ToolResult", "NoPayload",
    # §5.3 inputs
    "SessionContextIn", "ContextView", "ResolveIn", "HoldingFilter", "ListHoldingsIn", "ListMetricsIn",
    "GetMetricIn", "ProvenanceIn", "MethodologyIn", "QueryPackIn", "ListCardsIn", "ExplainCardIn", "HoldingFactsIn",
    "HoldingMarksIn", "TrackRecordIn", "ComparePoliciesIn", "ProbabilityIn", "GovernanceIn", "ImpliedActionsIn",
    "ImpliedIn", "BindingIn", "AttributionIn", "AttributeIn", "CompareRunsIn", "GroupRollupIn", "TreasuryIn",
    "OverlayIn", "ChatAuditIn",
    "FieldSpan", "QuarterValue", "ScenarioViewItem", "DraftScenarioViewIn", "WorldWeight", "ConsentOverride",
    "ModelWeights", "PacingOverride", "ActionOption", "Availability", "LeverSetting", "ParamShift",
    "DraftParamOverrideIn", "DraftBeliefViewIn", "DraftTradeIn", "DraftGoalSeekIn", "DraftReverseStressIn",
    "DraftBundleIn", "RunWhatifIn", "RunStatusIn", "StatementDraft", "NotAnswered", "AnswerDraft",
    # §5.3 payloads
    "EntityCandidates", "HoldingListView", "MetricListRow", "MetricListView", "ManifestSummary", "ProvenanceView",
    "MethodologyView", "PackSectionView", "CardRow", "CardListView", "Atom", "CardExplanation", "TablesView",
    "CasePoint", "MarkRow", "MarksView", "TrackRecordView", "ProbabilityView", "TriggerCheck", "GovernanceView",
    "BindingRow", "BindingView", "AttributionView", "FieldTag", "OverrideDraftView", "WhatIfBundleView",
    "RunHandleView", "Statement", "AnswerCard",
    # §5.5, §6.3, §11
    "Principal", "ContextHandle", "OverrideDraft", "WhatIfBundle", "OverrideConfirmation", "ToolCallRecord",
    "ChatTurnRecord", "WhatIfDraft", "WhatIfConfirmation",
    # catalogue
    "AnalystToolSpec", "ANALYST_TOOLS", "INCREMENT_1_TOOLS", "PROVISIONAL_V1_TOOLS", "ANSWER_LABELS",
    "ANALYST_LEDGER_KINDS", "HANDLE_RE",
]

# --------------------------------------------------------------------------------------------------- aliases
Fmt = Literal["pct", "pp", "bp", "usd_bn", "usd_m", "x", "months", "int", "prob", "ratio", "dec", "cat"]
FactFlag = Literal[
    "SUNK_IRR", "CASES_AS_QUANTILES", "GREY_2SE", "REVERSE_STRESS", "INFEASIBILITY_PRICE", "INTERIM_MODEL",
    "CONSENT_SENSITIVE", "TREE_SENSITIVE", "AT_A_KINK", "SELECTION_NOT_CERTIFIED", "TIER1_INFEASIBLE_AS_SPECIFIED",
    "EVIDENCE_MISSING", "OWNER_PROPOSAL", "ASSIGNED_DISSENT", "NOT_ESTABLISHED", "CONFIRMATORY_RUN_REQUIRED",
    "PROXY", "CALIBRATION_CAPPED", "T6_CONSUMING", "SECOND_ORDER_MATERIAL", "NO_ERROR_ESTIMATE",
    "CONTRACT_UNCHANGED", "USER_INPUT"]
QuoteSource = Literal["minority_report", "seat_argument", "methodology_note", "memo", "brief", "minutes",
                      "decision_rationale", "gp_notice", "adviser_note", "human_rationale", "red_team"]
RouteCode = Literal["IC_SECRETARIAT", "MRM", "CRO_OFFICE", "CF_PRICING_COMMITTEE", "TREASURER", "CIO",
                    "BOARD_SECRETARY", "FORECAST_INTAKE", "SEAL_SERVICE", "AI_GOVERNANCE", "COMPLIANCE",
                    "REGISTER_A1", "REGISTER_A2", "PACK_SECTION", "WHATIF_W3", "CONTRACT_AMENDMENT"]
RuleId = Literal["AR-1", "AR-2", "AR-3", "AR-3i", "AR-4F", "AR-4M", "AR-5", "AR-5i", "AR-6", "AR-7", "AR-8", "AR-8b",
                 "AR-9", "AR-10", "AR-11", "WALL", "RESTRICTED_LIST", "NEFF_BELOW_20", "NO_LEAGUE_TABLE",
                 "PREVOTE_GATE", "SMALL_CELL", "DATA_CLASS", "RUN_MODE"]
WithheldKind = Literal["HOLDING_DETAIL", "GROUP_CREDIBILITY", "INDIVIDUAL_SCORES", "SELLER_SIDE_ECONOMICS", "MNPI",
                       "TREASURY_DETAIL", "INFEASIBILITY_PRICES", "OVERLAY_DETAIL", "OWNER_ITEMS", "DELIBERATION",
                       "PREVOTES_BALLOTS", "SEALED_CONTENT", "TRANSCRIPTS", "LAB_LEDGER", "SMALL_CELL",
                       "WALLED_DATA"]
EntityKind = Literal["holding", "group", "gp", "policy", "register_item", "metric", "world", "seat", "run",
                     "company", "facility", "csa", "trade"]
PackSection = Literal["L0", "L1_BRIEF", "GROUP_BLOCK", "TREASURER_VIEW", "CRO_VIEW", "OVERLAY_VIEW", "REGISTER_ITEM",
                      "STATE_PANEL", "TIER1_BOARD", "RECOVERY_PANEL", "CONSENT_PANEL", "BRIDGE", "ROBUSTNESS",
                      "CONTROLS", "ARCHETYPES", "DECISIONS", "LAB_BLOCK", "LAB_LEDGER", "ERROR_LEDGER",
                      "REVERSE_STRESS", "OWNER_PROPOSAL", "SEAT_MAP", "MINORITY_REPORTS", "APPENDIX"]
HoldingSection = Literal["profile", "cashflows", "hf_terms", "loan_tape", "performance", "consents", "asset_debt",
                         "quotes"]
HoldingFilterField = Literal["gp", "strategy", "vintage", "flag", "maturity_within_q", "facility_type", "lens"]
HoldingSortKey = Literal["reported_nav", "commitment", "unfunded", "loan_balance", "vintage"]
CardFlag = Literal["TREE_SENSITIVE", "AT_A_KINK", "CONSENT_SENSITIVE", "SELECTION_NOT_CERTIFIED", "T6_CONSUMING",
                   "SECOND_ORDER_MATERIAL", "HP_RANK_FLAG", "CALIBRATION_CAPPED", "ZOMBIE", "CATALYST_MISSING"]
CardBlock = Literal["READING_RULE", "BINDING_CONSTRAINTS", "CONSENT_BASIS", "FLIP_THRESHOLDS", "BELIEF_CARD",
                    "ROBUSTNESS", "DISAGREEMENT"]
PolicyCode = Literal["RECOMMENDED", "STATUS_QUO", "DEFER", "ALTERNATIVE", "ARCH_A", "ARCH_B", "ARCH_C", "HOLD",
                     "STATIC_SAA", "DECK_RULES", "TARGET_CHASING", "PLACEBO", "PRO_RATA", "OVERLAY_ONLY",
                     "LIQUID_FIRST", "CASH_LAST", "P0", "C_H"]
OverrideKind = Literal["scenario_view", "forced_path", "belief_view", "model_weights", "consent", "pacing",
                       "action_option", "availability", "lever", "param_shift", "trade", "goal_seek",
                       "reverse_stress"]
ActionOptionKind = Literal["CV_ROLL", "CV_SELL", "LP_SALE", "STRIP_SALE", "NAV_LOAN", "PREFERRED_EQUITY", "RECAP",
                           "SYNDICATION", "REDEMPTION"]
LeverId = Literal["econ_leverage", "reserve_target", "treasury_topup", "revolver_size", "nav_facility_size",
                  "cf_term_prefund", "commitment_pacing", "p2s_notional", "tail_budget", "opp_budget",
                  "hf_notice_share"]
GoalSeekTarget = Literal["event_stage", "readiness_stage", "t4p_survival_tp", "p_red_class", "ig_cash_share",
                         "lcr30"]
GoalSeekLever = LeverId
TradeTemplate = Literal["put", "put_spread", "put_spread_ladder", "call", "call_spread", "collar", "vix_call",
                        "cdx_payer", "brent_put", "brent_put_spread", "hybrid", "future", "trs", "variance_swap"]
Output = Literal["PATH_METRICS", "MODEL_MIX", "CARDS", "LAMBDA_FTP", "ENVELOPES", "ROOT_ACTIONS", "BINDING_ROWS",
                 "STATE_READING", "CERTIFIED_PROBABILITIES", "TRADE_PRICE", "REVERSE_STRESS"]
Composition = Literal["CANONICAL", "SINGLE_MEMBER"]   # §6.3: canonical 4-step composition, or a single member
GateFlag = Literal["KL_INFORM", "KL_WARN", "KL_AMBER", "KL_RED", "ESS_WARN", "ESS_BLOCK", "RATIO_WARN"]
TierReason = Literal["KIND_MINIMUM", "OUTPUT_MINIMUM", "GATE_ESCALATION", "PROBABILITY_AFTER_CHANGE",
                     "FORCED_PATH", "DYNAMICS_CHANGE", "ALLOWLIST_TIER"]
PolicyNote = Literal["CONTRACT_UNCHANGED", "MODEL_WEIGHTS_A2_VOTE", "CONVENTION_A1_ROUTE", "MRM_ROUTE",
                     "EXPLORATORY_ONLY", "CONFIRMATORY_RUN_REQUIRED", "STORED_EVIDENCE_AVAILABLE",
                     "OWNER_DRAW_EXOGENOUS"]
RunStatus = Literal["QUEUED", "RUNNING", "COMPLETE", "FAILED", "CANCELLED"]
Category = Literal["explain", "drill-down", "probability", "comparison", "what-if", "data-lookup",
                   "process-governance", "out-of-scope"]
Outcome = Literal["ANSWER", "ANSWER_REDACTED", "DISAMBIGUATE", "DRAFT_OVERRIDE", "RUN_HANDLE", "NOT_IN_ARTIFACTS",
                  "DENY", "DECLINE"]
# v1.0 shapes kept for rows 16-23 and 34 (CHAT_ANALYST §5.3)
AttributionKind = Literal["shapley6", "group_dva", "null_control", "what_moved", "capability", "price_of_safety"]
RunDiffScope = Literal["portfolio", "group", "holding", "metrics"]
GroupSection = Literal["envelopes", "requests", "charges", "delivery_share", "pacing", "dva", "concentration",
                       "information_value"]
TreasurySection = Literal["ladder", "survival", "cfp", "draw_fan", "facilities", "maturities", "ftp_mismatch",
                          "infeasibility_prices"]
OverlaySection = Literal["positions", "greeks", "offset_card", "ov_rows", "im_by_csa", "vm", "services_ledger"]

ToolErrorCode = Literal[
    "AMBIGUOUS_ENTITY", "NO_MATCH_IN_SCOPE", "ENTITLEMENT_DENIED", "PREVOTE_GATED", "NOT_IN_ARTIFACTS",
    "EVIDENCE_MISSING", "PRICING_REFUSED", "PARAM_NOT_OVERRIDABLE", "BUNDLE_INCOMPATIBLE", "BUNDLE_NOT_CONFIRMED",
    "CONFIRMATION_INVALID", "CONFIRMATION_USED", "CONFIRMATION_EXPIRED", "BUNDLE_CHANGED", "GATE_ESCALATE_W3",
    "USER_INPUT_AMBIGUOUS", "QUOTA_EXHAUSTED", "BUDGET_EXHAUSTED", "RATE_LIMITED", "TOOL_BUDGET", "ANSWER_NOT_ALONE",
    "CONTEXT_EXPIRED", "VALIDATION_FAILED", "PERSONA_REFUSED", "REPLAY_MISS", "REPLAY_DRIFT"]
ToolStatus = Literal["OK", "PARTIAL", "AMBIGUOUS", "NOT_IN_ARTIFACTS", "DENIED", "ERROR"]
WTier = Literal["W1", "W2", "W3"]
Surface = Literal["tpa_chat", "ask_service", "mcp"]
ConfirmSurface = Literal["tpa_chat", "ask_service", "tpa_analyst_confirm"]
WallSide = Literal["above", "private", "public"]

# Label vocabulary rendered on answers (CQ §3.5 plus CHAT_ANALYST §4.4 and §3.2).
ANSWER_LABELS: Final[tuple[str, ...]] = (
    "SYNTHETIC", "STATEMENT_TYPE", "SEALED", "SEARCH", "EXPLORATORY", "GATE3_LABEL", "ICD203_RANGE", "PRICED_ON",
    "CONSENT_SCENARIO", "CONSENT_SENSITIVE", "TREE_SENSITIVE", "AT_A_KINK", "SELECTION_NOT_CERTIFIED",
    "TIER1_INFEASIBLE_AS_SPECIFIED", "EVIDENCE_MISSING", "OWNER_PROPOSAL", "ASSIGNED_DISSENT", "INFEASIBILITY_PRICE",
    "PRICING_LEVEL", "CENSUS", "NOT_ESTABLISHED", "CONFIRMATORY_RUN_REQUIRED", "INTERIM_MODEL", "USER_INPUT",
    "SIMULATED_PERSONA", "SERVED_BY_FALLBACK", "DRAFT_METHODOLOGY", "CONTRACT_UNCHANGED",
    "EXPLORATION_NOT_FOR_RECORD")
# Registry ledger kinds the analyst appends (§11).
ANALYST_LEDGER_KINDS: Final[tuple[str, ...]] = (
    "chat_session", "chat_turn", "override_draft", "whatif_bundle", "override_confirmation", "whatif_run",
    "chat_spend", "access_denial", "turn_validation", "decision_link")

HANDLE_RE: Final = re.compile(r"^(?P<kind>[FEQTUR])(?P<turn>\d+)\.(?P<n>\d+)$")


def _check_handle(handle: str, kinds: str, what: str) -> None:
    m = HANDLE_RE.match(handle)
    if m is None or m.group("kind") not in kinds:
        raise ValueError(f"{what} handle {handle!r} must look like {kinds[0]}<turn>.<n>")


def _tag(value: str) -> Any:
    """A required discriminator field that also emits ``enum: [value]`` (kept by the strict-schema transform)."""
    return Field(json_schema_extra={"enum": [value]})


# --------------------------------------------------------------------------------------------------- §5.1
class Fact(ContractModel):
    """The only carrier of engine numbers and categoricals; exactly one value field is set."""

    handle: str
    ref: ArtifactRef
    metric_id: MetricId
    label: str                                   # the metric registry's short label
    about: tuple[str, ...]                       # entity handles
    keys: tuple[KeyValue, ...]                   # other dimensions (policy, class, horizon)
    value_num: float | None
    value_cat: str | None
    unit: str
    fmt: Fmt
    plane: EvidencePlane
    status: AnswerStatus
    gate_label: GateLabel | None
    ci: Interval | None
    model_range: Interval | None
    mc_se: float | None
    paired_table: str | None
    scenario_hash: str | None
    as_of: date
    recorded_at: datetime | None
    data_class: DataClass
    priced_on: PricedOn | None
    consent_scenario: ConsentScenario | None
    flags: tuple[FactFlag, ...]

    @model_validator(mode="after")
    def _one_value(self) -> Fact:
        _check_handle(self.handle, "F", "fact")
        if (self.value_num is None) == (self.value_cat is None):
            raise ValueError("a Fact sets exactly one of value_num and value_cat")
        if self.value_cat is not None and self.fmt != "cat":
            raise ValueError("categorical facts use fmt 'cat'")
        for h in self.about:
            _check_handle(h, "E", "entity")
        return self


class EntityRef(ContractModel):
    handle: str
    kind: EntityKind
    canonical_id: str
    attrs: tuple[KeyValue, ...]                  # group, strategy, vintage, size bucket; never a free-text name
    score: float | None

    @model_validator(mode="after")
    def _handle(self) -> EntityRef:
        _check_handle(self.handle, "E", "entity")
        return self


class QuoteView(ContractModel):
    handle: str
    ref: ArtifactRef
    source: QuoteSource
    authentic: bool | None
    trust: Literal["mrm_note", "internal_validated", "untrusted"]
    text: str | None                             # mrm_note and internal_validated only; None when untrusted
    words: int
    linked_facts: tuple[str, ...]

    @model_validator(mode="after")
    def _untrusted(self) -> QuoteView:
        _check_handle(self.handle, "Q", "quote")
        if self.trust == "untrusted" and self.text is not None:
            raise ValueError("untrusted quote text never enters a model context (§10)")
        return self


QuoteRef = QuoteView   # BUILD_SPEC v1.1 §3.18 name


class TableSpec(ContractModel):
    handle: str
    title: str
    columns: tuple[str, ...]
    cells: tuple[tuple[str, ...], ...]           # cells: handles
    page: int
    total_rows: int

    @model_validator(mode="after")
    def _rect(self) -> TableSpec:
        _check_handle(self.handle, "T", "table")
        if any(len(row) != len(self.columns) for row in self.cells):
            raise ValueError("every table row has one cell per column")
        return self


class Withheld(ContractModel):
    """Names a scope removal without counts."""

    rule_id: RuleId
    what: WithheldKind


class ToolError(ContractModel):
    code: ToolErrorCode
    rule_id: RuleId | None
    route: RouteCode | None
    candidates: tuple[str, ...] = ()


class NoPayload(ContractModel):
    """Payload type of tools whose result is only facts (e.g. ``get_metric``)."""


P = TypeVar("P", bound=BaseModel)


class ToolResult(ContractModel, Generic[P]):
    """Every analyst tool result; ``model_text`` is what any model reads, the JSON is MCP ``structured_content``."""

    context_id: str
    turn: int
    status: ToolStatus
    payload: P | None
    facts: tuple[Fact, ...]
    entities: tuple[EntityRef, ...]
    quotes: tuple[QuoteView, ...]
    tables: tuple[TableSpec, ...]
    withheld: tuple[Withheld, ...]
    error: ToolError | None
    model_text: str

    @model_validator(mode="after")
    def _status(self) -> ToolResult[P]:
        if self.status in ("OK", "PARTIAL") and self.error is not None:
            raise ValueError(f"status {self.status} carries no error")
        if self.status in ("DENIED", "ERROR") and self.error is None:
            raise ValueError(f"status {self.status} needs an error")
        handles = [f.handle for f in self.facts] + [e.handle for e in self.entities] + \
            [q.handle for q in self.quotes] + [t.handle for t in self.tables]
        if len(set(handles)) != len(handles):
            raise ValueError("handles are unique within a result")
        return self


# --------------------------------------------------------------------------------------------------- §5.3 reads
class SessionContextIn(ContractModel):
    """Row 1 takes no input."""


class ContextView(ContractModel):                                             # 1
    context_id: str
    quarter: str
    baseline_run: RunId
    sealed_runs: tuple[RunId, ...]
    asof: date
    contract_mode: ContractMode
    pricing_scenario: ConsentScenario
    pricing_level: Literal["tolerance", "appetite"]
    census_id: CensusId
    allocation: AllocationId
    data_class: DataClass
    persona: str
    simulated_persona: bool
    groups_in_full_scope: tuple[GroupId, ...]
    prevote_open_items: tuple[str, ...]
    referents: tuple[EntityRef, ...]
    newer_run: RunId | None
    budget_left: str
    increment: Literal["1", "v1"]
    mcp_stage: Literal["A", "B"] | None


class ResolveIn(ContractModel):                                               # 2 -> EntityRef candidates
    text: str
    kinds: tuple[EntityKind, ...]
    limit: int = 5

    @model_validator(mode="after")
    def _bounds(self) -> ResolveIn:
        if not 1 <= self.limit <= 25:
            raise ValueError("limit must lie in 1..25")
        return self


class HoldingFilter(ContractModel):
    field: HoldingFilterField
    value: str                                   # closed vocabulary per field, checked by the service


class ListHoldingsIn(ContractModel):                                          # 3 -> TableSpec of handles
    group: GroupId
    filters: tuple[HoldingFilter, ...] = ()
    sort_by: HoldingSortKey = "reported_nav"
    order: Literal["desc", "asc"] = "desc"
    limit: int = 10
    page: int = 1

    @model_validator(mode="after")
    def _bounds(self) -> ListHoldingsIn:
        if not 1 <= self.limit <= 25 or self.page < 1:
            raise ValueError("limit must lie in 1..25 (at most 25 rows a page) and page >= 1")
        return self


class ListMetricsIn(ContractModel):                                           # 4
    prefix: str = ""
    run_id: RunId | None = None
    page: int = 1


class GetMetricIn(ContractModel):                                             # 5
    metric_id: MetricId
    run_id: RunId | None = None
    by: tuple[KeyValue, ...] = ()                # keys = registered dimensions


class ProvenanceIn(ContractModel):                                            # 6
    target: str
    detail: Literal["summary", "manifest", "logs"] = "summary"


class MethodologyIn(ContractModel):                                           # 7
    topic: str
    note_id: str | None = None


class QueryPackIn(ContractModel):                                             # 8
    section: PackSection
    item_id: str | None = None
    group: GroupId | None = None
    page: int = 1


class ListCardsIn(ContractModel):                                             # 9
    group: GroupId | None = None
    lens: Lens | None = None
    flags: tuple[CardFlag, ...] = ()
    page: int = 1


class ExplainCardIn(ContractModel):                                           # 10
    holding_id: HoldingId | None = None
    card_id: str | None = None
    blocks: tuple[CardBlock, ...] = ()

    @model_validator(mode="after")
    def _target(self) -> ExplainCardIn:
        if (self.holding_id is None) == (self.card_id is None):
            raise ValueError("name exactly one of holding_id and card_id")
        return self


class HoldingFactsIn(ContractModel):                                          # 11
    holding_id: HoldingId
    sections: tuple[HoldingSection, ...]


class HoldingMarksIn(ContractModel):                                          # 12 (bitemporal, no look-ahead)
    holding_id: HoldingId
    as_of: date | None = None
    recorded_at: datetime | None = None
    history_quarters: int = 0

    @model_validator(mode="after")
    def _bounds(self) -> HoldingMarksIn:
        if not 0 <= self.history_quarters <= 20:
            raise ValueError("history_quarters must lie in 0..20")
        return self


class TrackRecordIn(ContractModel):                                           # 13
    group: GroupId
    horizon_q: Literal[4, 8] = 4
    as_of: date | None = None


class ComparePoliciesIn(ContractModel):                                       # 14
    policies: tuple[PolicyCode, ...]
    horizons_y: tuple[Literal[3, 5, 10], ...] = (3, 5, 10)


class ProbabilityIn(ContractModel):                                           # 15
    event_id: str
    policy: PolicyCode = "RECOMMENDED"
    horizon_y: Literal[3, 5, 10] | None = None
    model_class: str | None = None
    holding_id: HoldingId | None = None
    run_handle: str | None = None


# rows 16-23 and 34: "v1.0's shapes", reconstructed and provisional (module docstring; PROVISIONAL_V1_TOOLS)
class GovernanceIn(ContractModel):                                            # 16
    kind: Literal["register_entry", "decision_log"]
    register_id: str | None = None
    item_id: str | None = None


class ImpliedActionsIn(ContractModel):                                        # 17 (addendum name ImpliedIn)
    item_id: str


ImpliedIn = ImpliedActionsIn   # CHAT_ANALYST §5.3 name; distinct from the evaluator's tools.ImpliedIn


class BindingIn(ContractModel):                                               # 18
    scope: Literal["portfolio", "group", "card"]
    scope_id: str | None = None
    pricing_level: Literal["contract", "tolerance", "appetite"] = "contract"
    include_infeasibility: bool = False          # honoured for TRS only


class AttributionIn(ContractModel):                                           # 19 (addendum name AttributeIn)
    kind: AttributionKind
    run_id: RunId | None = None
    group: GroupId | None = None


AttributeIn = AttributionIn   # CHAT_ANALYST §5.3 name; distinct from the evaluator's tools.AttributeIn


class CompareRunsIn(ContractModel):                                           # 20
    run_a: RunId
    run_b: RunId
    scope: RunDiffScope


class GroupRollupIn(ContractModel):                                           # 21
    group: GroupId
    sections: tuple[GroupSection, ...]


class TreasuryIn(ContractModel):                                              # 22
    sections: tuple[TreasurySection, ...]


class OverlayIn(ContractModel):                                               # 23
    sections: tuple[OverlaySection, ...]
    named_stress: str | None = None


class ChatAuditIn(ContractModel):                                             # 34
    kind: Literal["my_sessions", "my_runs", "kpis"]
    period: Literal["day", "week", "month"] = "week"


# --------------------------------------------------------------------------------------------------- §5.3 what-ifs
class FieldSpan(ContractModel):
    """Draft field -> user-number handle ``U<turn>.<n>`` (the service parsed the value; the model only cites)."""

    field: str
    span: str

    @model_validator(mode="after")
    def _span(self) -> FieldSpan:
        _check_handle(self.span, "U", "user-number")
        return self


class QuarterValue(ContractModel):
    quarter_offset: int
    value_dec: float


class ScenarioViewItem(ContractModel):
    view_library_id: str
    operator: Literal["eq", "le", "ge"]
    value_dec: float | None = None
    value_bp: float | None = None
    horizon_q: int | None = None

    @model_validator(mode="after")
    def _one_unit(self) -> ScenarioViewItem:
        if (self.value_dec is None) == (self.value_bp is None):
            raise ValueError("set exactly the library entry's unit field: value_dec or value_bp")
        return self


class DraftScenarioViewIn(ContractModel):                                     # 24
    mode: Literal["reweight", "forced_path"]
    views: tuple[ScenarioViewItem, ...] = ()
    path: tuple[QuarterValue, ...] = ()
    path_metric: str | None = None
    field_spans: tuple[FieldSpan, ...] = ()

    @model_validator(mode="after")
    def _mode(self) -> DraftScenarioViewIn:
        if self.mode == "reweight" and (not self.views or self.path):
            raise ValueError("reweight mode takes views and no path")
        if self.mode == "forced_path" and (not self.path or self.path_metric is None or self.views):
            raise ValueError("forced_path mode takes a path and its path_metric, and no views")
        return self


class WorldWeight(ContractModel):
    world: WorldId
    weight_dec: float


class ConsentOverride(ContractModel):
    kind: Literal["consent"] = _tag("consent")
    scenario: ConsentScenario


class ModelWeights(ContractModel):
    kind: Literal["model_weights"] = _tag("model_weights")
    weights: tuple[WorldWeight, ...]

    @model_validator(mode="after")
    def _simplex(self) -> ModelWeights:
        if not self.weights or any(w.weight_dec < 0 for w in self.weights):
            raise ValueError("model weights are non-negative and non-empty")
        if abs(sum(w.weight_dec for w in self.weights) - 1.0) > 1e-9:
            raise ValueError("model weights must sum to 1")
        if len({w.world for w in self.weights}) != len(self.weights):
            raise ValueError("one weight per world")
        return self


class PacingOverride(ContractModel):
    kind: Literal["pacing"] = _tag("pacing")
    group: GroupId
    multiplier_x: float
    quarters: int


class ActionOption(ContractModel):
    kind: Literal["action_option"] = _tag("action_option")
    holding_id: HoldingId
    option: ActionOptionKind
    price_frac_nav: float | None = None


class Availability(ContractModel):
    kind: Literal["availability"] = _tag("availability")
    facility_id: FacilityId
    state: StressState
    availability_frac: float

    @model_validator(mode="after")
    def _frac(self) -> Availability:
        if not 0.0 <= self.availability_frac <= 1.0:
            raise ValueError("availability_frac must lie in [0, 1]")
        return self


class LeverSetting(ContractModel):
    kind: Literal["lever"] = _tag("lever")
    lever: LeverId
    value: float                                 # unit from the lever registry, shown in the back-translation


class ParamShift(ContractModel):
    kind: Literal["param_shift"] = _tag("param_shift")
    param: str                                   # an id from overridable_params.yaml, checked by the service
    op: Literal["set", "mult", "add"]
    value: float


class DraftParamOverrideIn(ContractModel):                                    # 25
    override: Annotated[
        ConsentOverride | ModelWeights | PacingOverride | ActionOption | Availability | LeverSetting | ParamShift,
        Field(discriminator="kind"),
    ]
    field_spans: tuple[FieldSpan, ...] = ()


class DraftBeliefViewIn(ContractModel):                                       # 26
    target_kind: Literal["holding", "strategy", "group"]
    target_id: str
    quantity: Literal["fwd_return_a", "forecast_realization", "lever_alpha"]
    operator: Literal["eq", "le", "ge"]
    value_dec: float
    horizon_q: int | None = None
    confidence_c: float | None = None            # None = contract default
    field_spans: tuple[FieldSpan, ...] = ()


class DraftTradeIn(ContractModel):                                            # 27
    book: Literal["tail", "opp", "beta"]
    template: TradeTemplate
    notional_usd_bn: float
    strikes_frac: tuple[float, ...]
    expiry_months: int | None = None
    csa_id: CsaId | None = None
    field_spans: tuple[FieldSpan, ...] = ()


class DraftGoalSeekIn(ContractModel):                                         # 28
    target: GoalSeekTarget
    target_stage: CFPStage | None = None
    target_value_dec: float | None = None
    lever: GoalSeekLever
    bounds: Interval                             # lever units from the registry
    tolerance: float
    field_spans: tuple[FieldSpan, ...] = ()

    @model_validator(mode="after")
    def _target(self) -> DraftGoalSeekIn:
        if (self.target_stage is None) == (self.target_value_dec is None):
            raise ValueError("set exactly one of target_stage and target_value_dec")
        if not self.tolerance > 0:
            raise ValueError("tolerance must be positive")
        return self


class DraftReverseStressIn(ContractModel):                                    # 29 (BS ReverseStressIn + class)
    metric_id: MetricId
    threshold_dec: float
    world_class: WorldClass
    field_spans: tuple[FieldSpan, ...] = ()


class FieldTag(ContractModel):
    override_id: str
    field: str
    tag: Literal["USER", "DEFAULT", "INFERRED"]
    shown: str                                   # rendered by code


class OverrideDraftView(ContractModel):
    """Rows 24–29 output: diagnostics only, no outcome number (O2)."""

    override_id: str
    spec_hash: str
    kind: OverrideKind
    effective: tuple[str, ...]
    kl: str | None
    ess: str | None
    gate_flags: tuple[GateFlag, ...]
    min_tier: WTier
    field_tags: tuple[FieldTag, ...]
    unresolved_fields: tuple[str, ...]
    policy_notes: tuple[PolicyNote, ...]
    stored_alternative: str | None
    expires_at: datetime


class DraftBundleIn(ContractModel):                                           # 30
    override_ids: tuple[str, ...]
    outputs: tuple[Output, ...]

    @model_validator(mode="after")
    def _non_empty(self) -> DraftBundleIn:
        if not self.override_ids or not self.outputs:
            raise ValueError("a bundle names at least one override and one output")
        if len(set(self.override_ids)) != len(self.override_ids):
            raise ValueError("override_ids must be unique")
        return self


class WhatIfBundleView(ContractModel):                                        # 30 output
    bundle_id: str
    bundle_hash: str
    override_ids: tuple[str, ...]
    composition: Composition
    outputs: tuple[Output, ...]
    tier: WTier
    tier_reasons: tuple[TierReason, ...]
    back_translation: str
    joint_kl: str | None
    joint_ess: str | None
    gate_flags: tuple[GateFlag, ...]
    field_tags: tuple[FieldTag, ...]
    expires_at: datetime


class RunWhatifIn(ContractModel):                                             # 31
    bundle_id: str
    bundle_hash: str


class RunHandleView(ContractModel):                                           # 31, 32
    handle: str
    run_id: RunId | None
    tier: str
    status: RunStatus
    progress_note: str | None

    @model_validator(mode="after")
    def _handle(self) -> RunHandleView:
        _check_handle(self.handle, "R", "run")
        return self


class RunStatusIn(ContractModel):                                             # 32
    handle: str


class StatementDraft(ContractModel):
    """Placeholders only; declared subject entities and metrics (§4.5)."""

    kind: Literal["model_output", "agent_judgment", "assumption"]
    text: str
    about: tuple[str, ...] = ()
    measures: tuple[MetricId, ...] = ()


class NotAnswered(ContractModel):
    part: str                                    # validated like statement text
    reason: Literal["not_in_artifacts", "out_of_scope", "denied", "not_in_increment", "needs_whatif"]
    route: RouteCode | None = None


class AnswerDraft(ContractModel):                                             # 33 in
    context_id: str
    category: Category
    outcome: Outcome
    lead: StatementDraft
    body: tuple[StatementDraft, ...] = ()
    table_handles: tuple[str, ...] = ()
    what_would_change: StatementDraft | None = None
    not_answered: tuple[NotAnswered, ...] = ()
    route: RouteCode | None = None
    candidate_handles: tuple[str, ...] = ()
    bundle_id: str | None = None

    @model_validator(mode="after")
    def _shape(self) -> AnswerDraft:
        limit = 6 if self.category == "explain" else 3
        if 1 + len(self.body) > limit:
            raise ValueError(f"at most {limit} statements for category {self.category} (§4.6)")
        if self.outcome == "DISAMBIGUATE" and not self.candidate_handles:
            raise ValueError("DISAMBIGUATE lists the candidate handles")
        if self.outcome == "DRAFT_OVERRIDE" and self.bundle_id is None:
            raise ValueError("DRAFT_OVERRIDE shows a drafted bundle (bundle_id)")
        for h in self.table_handles:
            _check_handle(h, "T", "table")
        return self


class Statement(ContractModel):
    text: str
    kind: Literal["model_output", "agent_judgment", "assumption"]
    refs: tuple[ArtifactRef, ...]


class AnswerCard(ContractModel):                                              # 33 out; BS v1.1 fields first
    """Assembled by code from an ``AnswerDraft``; rendered by ``claims.render``."""

    context_id: str
    statements: tuple[Statement, ...]
    status: AnswerStatus
    synthetic: bool
    interim: bool
    rendered: RenderedDocument
    not_answered: tuple[NotAnswered, ...] = ()
    answer_id: str
    labels: tuple[str, ...]
    supports: Literal["unaudited", "audited_supports", "audited_partial", "audited_not_supported"] = "unaudited"
    run_ids: tuple[RunId, ...]
    validation: ValidationReport
    fallback: bool
    served_by_fallback: bool

    @model_validator(mode="after")
    def _labels(self) -> AnswerCard:
        if self.synthetic and "SYNTHETIC" not in self.labels:
            raise ValueError("an answer touching synthetic data carries the SYNTHETIC label (U4)")
        if self.served_by_fallback and "SERVED_BY_FALLBACK" not in self.labels:
            raise ValueError("a fallback-served answer carries SERVED_BY_FALLBACK")
        return self


# --------------------------------------------------------------------------------------------------- payloads
class EntityCandidates(ContractModel):                                        # 2
    candidates: tuple[str, ...]                  # entity handles, best first
    ambiguous: bool


class HoldingListView(ContractModel):                                         # 3
    table: str                                   # table handle; rank and size cells are facts
    page: int
    total_rows: int


class MetricListRow(ContractModel):
    metric_id: MetricId
    label: str
    unit: str
    scope: str
    available: bool


class MetricListView(ContractModel):                                          # 4
    rows: tuple[MetricListRow, ...]
    page: int
    total: int


class ManifestSummary(ContractModel):
    run_id: RunId
    engine_git_sha: str
    config_hash: str
    snapshot_hash: str
    scenario_hashes: tuple[KeyValue, ...]
    plane: str
    created_at: datetime


class ProvenanceView(ContractModel):                                          # 6 (filtered, redacted)
    nodes: tuple[ProvenanceNode, ...]
    manifest: ManifestSummary | None


class MethodologyView(ContractModel):                                         # 7
    note_id: str
    version: str
    approval: Literal["approved", "draft"]      # unapproved notes render DRAFT_METHODOLOGY
    quotes: tuple[str, ...]                      # quote handles


class PackSectionView(ContractModel):                                         # 8
    section: PackSection
    section_id: str
    pack_hash: str


class CardRow(ContractModel):
    card_id: str
    holding: str | None                          # entity handle
    group: GroupId
    lens_fact: str                               # fact handle of the card's lens action
    flags: tuple[CardFlag, ...]


class CardListView(ContractModel):                                            # 9
    rows: tuple[CardRow, ...]
    page: int
    total: int


class Atom(ContractModel):
    """A versioned template sentence with handles (§7.1)."""

    block: CardBlock
    template_id: str
    text: str
    facts: tuple[str, ...]


class CardExplanation(ContractModel):                                         # 10
    card_id: str
    holding: str                                 # entity handle
    atoms: tuple[Atom, ...]
    alt_reading: Atom | None


class TablesView(ContractModel):
    """One table handle per requested section (holding_facts, group_rollup, treasury_panel, overlay_book,
    compare_policies, compare_runs, implied_actions, chat_audit)."""

    tables: tuple[str, ...]


class CasePoint(ContractModel):
    """A three-case set or any percentile set (brief §9)."""

    label: str
    quantile: float | None
    fact: str


class MarkRow(ContractModel):
    mark_type: MarkType
    basis: Literal["irr_si_net", "moic_si_net"]
    stored: str
    cases: tuple[CasePoint, ...]
    as_of: date
    recorded_at: datetime
    translated_fwd: str | None
    weight: str | None


class MarksView(ContractModel):                                               # 12
    marks: tuple[MarkRow, ...]
    fused_mu: str
    sigma: str
    band80: str                                  # an interval fact
    p_achieved_4q: str
    p_achieved_8q: str
    flags: tuple[FactFlag, ...]
    credibility: Literal["kappa_and_info_value", "info_value_only", "hidden_neff_below_20", "not_in_scope"]


class TrackRecordView(ContractModel):                                         # 13 (fact handles; no ranking fields)
    n_eff: str
    gated: bool
    wis: str | None
    coverage: str | None
    bias_terms: tuple[str, ...]
    kappa: str | None
    ge_status: str | None
    info_value: str | None


class ProbabilityView(ContractModel):                                         # 15
    central: str                                 # fact handle
    companion_p_red: str | None                  # paired worst-class P(red) for P(10%)-family events


class TriggerCheck(ContractModel):
    rule: str
    fact: str
    passed: bool


class GovernanceView(ContractModel):                                          # 16
    """v1.0's ``GovernanceView(register, log)``; fields renamed because ``register`` shadows ``BaseModel``."""

    register_checks: tuple[TriggerCheck, ...]    # Register trigger checks evaluated in code
    log_rows: tuple[str, ...]                    # table handles of decision-log rows; never ballots


class BindingRow(ContractModel):
    row_key: str
    dual: str
    lo: str
    hi: str
    validity: str
    at_kink: bool


class BindingView(ContractModel):                                             # 18
    rows: tuple[BindingRow, ...]


class AttributionView(ContractModel):                                         # 19
    components: tuple[str, ...]
    residual: str
    not_established: tuple[str, ...]


# --------------------------------------------------------------------------------------------------- §5.5, §6.3, §11
class Principal(ContractModel):
    """The authenticated person (§9.1); built from ``config/analyst/role_map.yaml``."""

    user_hash: str                               # sha256(Windows SID)
    roles: tuple[str, ...]
    groups: tuple[GroupId, ...]
    recusals: tuple[GroupId, ...]
    barriers: tuple[str, ...]
    prevote_locked_items: tuple[str, ...]
    wall_side: WallSide
    voting_member: bool
    simulated: bool
    entitlement_version: str


class ContextHandle(ContractModel):
    """Minted and MAC-signed by the service (§8); every fact must belong to it."""

    context_id: str
    asof: date
    contract_hash: str
    census_id: CensusId | None
    allocation: AllocationId
    plane: EvidencePlane                         # the context's default plane
    data_class: DataClass
    run_ids: tuple[RunId, ...]
    user_hash: str
    entitlement_version: str
    surface: Surface
    quarter: str
    baseline_run: RunId
    sealed_runs: tuple[RunId, ...]
    snapshot_hash: str
    wall_side: WallSide
    expires_at: datetime
    mac: str

    def mac_payload(self) -> bytes:
        """Canonical JSON of every field except ``mac`` (what the service's MAC covers)."""
        return canonical_json(self.model_dump(mode="python", exclude={"mac"}))


DraftSpec = (DraftScenarioViewIn | DraftParamOverrideIn | DraftBeliefViewIn | DraftTradeIn | DraftGoalSeekIn
             | DraftReverseStressIn)


class OverrideDraft(ContractModel):
    """Service record of one drafted override (engine-computed floats allowed); 30-minute TTL (§6.1)."""

    override_id: str
    spec_hash: str
    kind: OverrideKind
    spec: DraftSpec
    principal_hash: str
    session_id: str
    context_id: str
    effective: tuple[KeyValue, ...]              # effective form (after shrinkage or module-F projection)
    kl: float | None
    ess: float | None
    weight_ratio: float | None
    gate_flags: tuple[GateFlag, ...]
    min_tier: WTier
    field_tags: tuple[FieldTag, ...]
    unresolved_fields: tuple[str, ...]
    created_at: datetime
    expires_at: datetime

    @model_validator(mode="after")
    def _hash(self) -> OverrideDraft:
        if self.spec_hash != content_hash(self.spec):
            raise ValueError("spec_hash must be content_hash(spec)")
        if not self.expires_at > self.created_at:
            raise ValueError("expires_at must follow created_at")
        return self


class WhatIfBundle(ContractModel):
    """Service record; ``bundle_hash`` = sha256 of the canonical JSON of the other fields (§6.3)."""

    bundle_id: str
    override_ids: tuple[str, ...]                # canonical order: (kind rank, override_id)
    composition: Composition
    outputs: tuple[Output, ...]
    tier: WTier
    parent_run: RunId
    context_id: str
    user_hash: str
    field_tags: tuple[FieldTag, ...]
    back_translation_id: str
    expires_at: datetime
    bundle_hash: str

    def compute_hash(self) -> str:
        return content_hash(self.model_dump(mode="python", exclude={"bundle_hash"}))

    @classmethod
    def build(cls, **fields: Any) -> WhatIfBundle:
        """Create a bundle from every field but ``bundle_hash``, which is computed (strict Python-mode types)."""
        draft = cls.model_construct(**fields, bundle_hash="")
        return cls.model_validate({**fields, "bundle_hash": draft.compute_hash()})

    @model_validator(mode="after")
    def _hash(self) -> WhatIfBundle:
        if self.bundle_hash != self.compute_hash():
            raise ValueError("bundle_hash must equal the hash of the other fields")
        return self


class OverrideConfirmation(ContractModel):
    """Appended to the registry; Ed25519 over the canonical JSON of the other fields (S-ADR-40); single use."""

    confirmation_id: str
    bundle_id: str
    bundle_hash: str
    user_hash: str
    surface: ConfirmSurface
    ticked_inferred: tuple[str, ...]
    confirmed_at: datetime
    expires_at: datetime
    signer_key_id: str
    signature: str

    def signed_payload(self) -> bytes:
        """The bytes the signature covers (every field except ``signature``)."""
        return canonical_json(self.model_dump(mode="python", exclude={"signature"}))

    @model_validator(mode="after")
    def _times(self) -> OverrideConfirmation:
        if not self.expires_at > self.confirmed_at:
            raise ValueError("expires_at must follow confirmed_at")
        if not is_content_hash(self.bundle_hash):
            raise ValueError("bundle_hash must be sha256:<64 hex>")
        return self


class ToolCallRecord(ContractModel):
    name: str
    args_hash: str
    result_hash: str
    facts_served: tuple[str, ...]
    denials: tuple[RuleId, ...]
    latency_s: float


class ChatTurnRecord(ContractModel):
    """Hash-chained ``chat_turn`` row written by the service (§11); BS v1.1 fields first."""

    session_id: str
    turn: int
    principal_hash: str
    surface: str
    question_hash: str
    tool_calls: tuple[str, ...]
    answer_ref: ArtifactRef
    validator_passed: bool
    status: AnswerStatus
    served_model: str
    tokens: int
    cost_usd: float
    prev_hash: str
    record_hash: str
    # §11 additions
    persona: str
    simulated: bool
    entitlement_version: str
    mcp_stage: Literal["A", "B"] | None = None
    backend: Literal["stub", "replay", "live"]
    context_id: str
    tool_call_records: tuple[ToolCallRecord, ...] = ()
    llm_calls: tuple[LLMCallRecord, ...] = ()
    prompt_hash: str
    tool_list_hash: str
    answer_hash: str
    labels: tuple[str, ...] = ()
    supports: Literal["unaudited", "audited_supports", "audited_partial", "audited_not_supported"] = "unaudited"
    validation: ValidationReport | None = None
    fallback: bool = False
    bundles: tuple[str, ...] = ()
    confirmations: tuple[str, ...] = ()
    run_ids: tuple[RunId, ...] = ()
    stop_hook_verdict: Literal["validated", "blocked", "unvalidated"] | None = None
    transcript_chain_head: str | None = None


# BUILD_SPEC v1.1 §3.18 names; the addendum's models and fields win (§5.5).
WhatIfDraft = OverrideDraftView
WhatIfConfirmation = OverrideConfirmation


# --------------------------------------------------------------------------------------------------- catalogue
@dataclass(frozen=True, slots=True)
class AnalystToolSpec:
    """One row of the CHAT_ANALYST §5.2 catalogue."""

    number: int
    name: str
    input_model: type[ContractModel]
    payload_model: type[ContractModel]
    tier: Literal["T0", "T1", "T1-T3"]
    increment: Literal["1", "v1"]
    mcp_stage: Literal["A", "B"]
    kind: Literal["read", "draft", "run", "answer"]


def _tool(number: int, name: str, input_model: type[ContractModel], payload_model: type[ContractModel],
          tier: Literal["T0", "T1", "T1-T3"], increment: Literal["1", "v1"], mcp_stage: Literal["A", "B"],
          kind: Literal["read", "draft", "run", "answer"]) -> AnalystToolSpec:
    return AnalystToolSpec(number, name, input_model, payload_model, tier, increment, mcp_stage, kind)


ANALYST_TOOLS: Final[tuple[AnalystToolSpec, ...]] = (
    _tool(1, "get_session_context", SessionContextIn, ContextView, "T0", "1", "A", "read"),
    _tool(2, "resolve_entity", ResolveIn, EntityCandidates, "T0", "1", "A", "read"),
    _tool(3, "list_holdings", ListHoldingsIn, HoldingListView, "T0", "1", "A", "read"),
    _tool(4, "list_metrics", ListMetricsIn, MetricListView, "T0", "1", "A", "read"),
    _tool(5, "get_metric", GetMetricIn, NoPayload, "T0", "1", "A", "read"),
    _tool(6, "get_provenance", ProvenanceIn, ProvenanceView, "T0", "1", "A", "read"),
    _tool(7, "get_methodology", MethodologyIn, MethodologyView, "T0", "1", "A", "read"),
    _tool(8, "query_pack", QueryPackIn, PackSectionView, "T0", "1", "A", "read"),
    _tool(9, "list_cards", ListCardsIn, CardListView, "T0", "1", "A", "read"),
    _tool(10, "explain_card", ExplainCardIn, CardExplanation, "T0", "1", "A", "read"),
    _tool(11, "holding_facts", HoldingFactsIn, TablesView, "T0", "1", "A", "read"),
    _tool(12, "holding_marks", HoldingMarksIn, MarksView, "T0", "1", "A", "read"),
    _tool(13, "forecast_track_record", TrackRecordIn, TrackRecordView, "T0", "1", "A", "read"),
    _tool(14, "compare_policies", ComparePoliciesIn, TablesView, "T0", "1", "A", "read"),
    _tool(15, "probability_query", ProbabilityIn, ProbabilityView, "T0", "1", "A", "read"),
    _tool(16, "governance_lookup", GovernanceIn, GovernanceView, "T0", "v1", "A", "read"),
    _tool(17, "implied_actions", ImpliedActionsIn, TablesView, "T0", "v1", "B", "read"),
    _tool(18, "binding_constraints", BindingIn, BindingView, "T0", "v1", "A", "read"),
    _tool(19, "attribute", AttributionIn, AttributionView, "T0", "v1", "A", "read"),
    _tool(20, "compare_runs", CompareRunsIn, TablesView, "T0", "v1", "A", "read"),
    _tool(21, "group_rollup", GroupRollupIn, TablesView, "T0", "v1", "A", "read"),
    _tool(22, "treasury_panel", TreasuryIn, TablesView, "T0", "v1", "A", "read"),
    _tool(23, "overlay_book", OverlayIn, TablesView, "T0", "v1", "A", "read"),
    _tool(24, "draft_scenario_view", DraftScenarioViewIn, OverrideDraftView, "T1", "1", "B", "draft"),
    _tool(25, "draft_param_override", DraftParamOverrideIn, OverrideDraftView, "T1", "1", "B", "draft"),
    _tool(26, "draft_belief_view", DraftBeliefViewIn, OverrideDraftView, "T1", "v1", "B", "draft"),
    _tool(27, "draft_trade", DraftTradeIn, OverrideDraftView, "T1", "v1", "B", "draft"),
    _tool(28, "draft_goal_seek", DraftGoalSeekIn, OverrideDraftView, "T1", "v1", "B", "draft"),
    _tool(29, "draft_reverse_stress", DraftReverseStressIn, OverrideDraftView, "T1", "v1", "B", "draft"),
    _tool(30, "draft_whatif_bundle", DraftBundleIn, WhatIfBundleView, "T1", "1", "B", "draft"),
    _tool(31, "run_whatif", RunWhatifIn, RunHandleView, "T1-T3", "1", "B", "run"),
    _tool(32, "get_run_status", RunStatusIn, RunHandleView, "T0", "1", "B", "read"),
    _tool(33, "answer_grounded", AnswerDraft, AnswerCard, "T0", "1", "A", "answer"),
    _tool(34, "chat_audit", ChatAuditIn, TablesView, "T0", "v1", "B", "read"),
)
INCREMENT_1_TOOLS: Final[tuple[str, ...]] = tuple(t.name for t in ANALYST_TOOLS if t.increment == "1")
# Rows 16-23 and 34: shapes reconstructed from §5.2 (v1.0 is not on disk); WP-40 confirms or replaces them.
PROVISIONAL_V1_TOOLS: Final[tuple[str, ...]] = tuple(
    t.name for t in ANALYST_TOOLS if 16 <= t.number <= 23 or t.number == 34)
