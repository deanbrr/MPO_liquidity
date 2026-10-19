"""Enumerations and the small shared value models (BUILD_SPEC v1.1 §3.1, §3.16).

Besides the §3.1 enums this module hosts the pieces every other contracts module needs and that must sit at the
bottom of the import graph: the Pydantic base configuration (``ContractModel``: frozen, ``extra="forbid"``,
strict; §3), ``ReturnBasis`` (§3.1), and the LLM-facing replacements for dicts and fixed tuples ``KeyValue`` and
``Interval`` (§3.16, S-ADR-36; ``contracts.lab`` re-exports them).

Conventions. A §3.1 line written ``class X(StrEnum): A, B`` has values equal to the member names (row keys print
``RowFamily`` values, e.g. ``T4P:h=07``, and the prose spells ``DEV_SYNTHETIC``, ``SYNTHETIC``, ``SELL`` in upper
case), except where the specification spells the values elsewhere: ``FactorKind`` uses ``logret``/``level``/
``change`` (§1.2, S-ADR-35: the kinds declared in ``scen/factors.yaml``), ``TargetMode`` uses ``precommitted``/
``rolling`` (S-ADR-06) and ``LLMMode`` uses ``offline``/``replay``/``live`` (§7.1 ``TPA_LLM_MODE``; it also accepts
any letter case, because the value comes from an environment variable). IntEnums written without values number
their members 0, 1, ... in order. ``ConsentScenario`` orders R0x < R0 < R1 < R2 by rank, not by string comparison.
"""

from __future__ import annotations

import re
from enum import IntEnum, StrEnum
from typing import Annotated, Any, Final, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator

__all__ = [
    "ContractModel", "ReturnBasis", "KeyValue", "Interval", "CensusId", "AllocationId", "WorldId",
    "check_world_id", "WORLD_ID_RE",
    "Lens", "Plane", "MandateMode", "ContractMode", "ConsentScenario", "CFPStage", "RecourseTier", "MacroRegime",
    "ExitWindow", "ShockType", "StressState", "FinWindow", "Clock", "FlowType", "FLOW_SIGNS", "FLOW_IS_CASH",
    "N_FLOW_TYPES", "Counterparty", "SaleReason", "RunMode", "FactorKind", "AnswerStatus", "DataClass", "PricedOn",
    "EvidencePlane", "MarkType", "Book", "HFLotState", "CreditState", "RowFamily", "RowRole", "GateLabel",
    "FailureLabel", "OptionKind", "Tier", "RoleId", "ModelFamily", "LLMMode", "CampaignState", "T6SurrogateKind",
    "TargetMode", "RECOURSE_TIER_ORDER",
]


class ContractModel(BaseModel):
    """Base of every contracts Pydantic model: frozen, ``extra="forbid"``, strict (§3).

    External data (YAML, JSON, MCP payloads, registry rows) is validated in JSON mode (``model_validate_json``),
    because strict Python-mode validation rejects enum strings and lists for tuple fields (S-ADR-39). Models are
    never set members or dict keys unless they hold only hashable fields (e.g. ``RowKey``).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class ReturnBasis(ContractModel):
    """Return tag carried by every return field (§1.2; ARCH §0.5)."""

    kind: Literal["arith", "geom", "log"]
    fees: Literal["gross", "net"]


class KeyValue(ContractModel):
    """LLM-facing replacement for a dict entry (S-ADR-36)."""

    key: str
    value: float | str


class Interval(ContractModel):
    """LLM-facing replacement for a fixed-length (lo, hi) tuple (S-ADR-36)."""

    lo: float
    hi: float

    @model_validator(mode="after")
    def _ordered(self) -> Interval:
        if not self.lo <= self.hi:
            raise ValueError(f"Interval needs lo <= hi, got lo={self.lo}, hi={self.hi}")
        return self


CensusId = Literal["v1.0", "v1.1", "v1.1r"]
AllocationId = Literal["v1", "v2"]

# "M1".."M6", "B1", "B2", "MS:<name>" (§3.1); contracts.world.validate_world_id is the public validator.
WORLD_ID_RE: Final = re.compile(r"^(?:M[1-6]|B[12]|MS:[A-Za-z0-9_.-]{1,64})$")


def check_world_id(world_id: str) -> str:
    """Return ``world_id`` if it is a valid world id, else raise ``ValueError``."""
    if not isinstance(world_id, str) or not WORLD_ID_RE.match(world_id):
        raise ValueError(f"invalid world id {world_id!r}: expected M1..M6, B1, B2 or MS:<name>")
    return world_id


WorldId = Annotated[str, AfterValidator(check_world_id)]


class Lens(StrEnum):
    """Action lens. REFINANCE = cash-out; LEVER = exposure-up ≡ ADD + REFI (ARCH §4.8)."""

    SELL = "SELL"
    HOLD = "HOLD"
    REFINANCE = "REFINANCE"
    LEVER = "LEVER"
    ADD = "ADD"
    PACE = "PACE"


class Plane(StrEnum):
    """Evaluation plane (ARCH §7.5); RNG plane codes live in ``rng.PLANE_CODE`` (§1.7)."""

    CALIBRATION = "CALIBRATION"
    SEARCH = "SEARCH"
    FINAL = "FINAL"
    HISTORICAL = "HISTORICAL"
    EXPLORATION = "EXPLORATION"


class MandateMode(StrEnum):
    B_OWNER_CALL = "B"
    H_HYBRID = "H"
    A_ADIC_RULE = "A"


class ContractMode(StrEnum):
    NORMAL = "NORMAL"
    EXECUTION_RECOVERY = "EXEC_RECOVERY"
    STRUCTURAL_RECOVERY = "STRUCT_RECOVERY"


_CONSENT_ORDER: Final = ("R0x", "R0", "R1", "R2")


def _consent_rank(value: Any) -> int | None:
    if isinstance(value, str) and value in _CONSENT_ORDER:
        return _CONSENT_ORDER.index(value)
    return None


class ConsentScenario(StrEnum):
    """Nested consent lever sets, ordered R0x < R0 < R1 < R2 (ARCH §5.5)."""

    R0X = "R0x"
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"

    @property
    def rank(self) -> int:
        return _CONSENT_ORDER.index(self.value)

    def __lt__(self, other: object) -> bool:
        r = _consent_rank(other)
        return NotImplemented if r is None else self.rank < r

    def __le__(self, other: object) -> bool:
        r = _consent_rank(other)
        return NotImplemented if r is None else self.rank <= r

    def __gt__(self, other: object) -> bool:
        r = _consent_rank(other)
        return NotImplemented if r is None else self.rank > r

    def __ge__(self, other: object) -> bool:
        r = _consent_rank(other)
        return NotImplemented if r is None else self.rank >= r


class CFPStage(IntEnum):
    GREEN = 0
    AMBER = 1
    RED = 2
    BLACK = 3


class RecourseTier(StrEnum):
    """Nested recourse tiers T ⊂ TP ⊂ TPF ⊂ TPFA ⊂ ALL (GROUPS §2.4)."""

    T = "T"
    TP = "TP"
    TPF = "TPF"
    TPFA = "TPFA"
    ALL = "ALL"


RECOURSE_TIER_ORDER: Final[tuple[RecourseTier, ...]] = (
    RecourseTier.T, RecourseTier.TP, RecourseTier.TPF, RecourseTier.TPFA, RecourseTier.ALL)


class MacroRegime(IntEnum):
    EXP = 0
    LATE = 1
    CRIS = 2
    RECV = 3


class ExitWindow(IntEnum):
    O = 0  # noqa: E741  (spec name)
    N = 1
    D = 2
    F = 3


class ShockType(IntEnum):
    N = 0
    B = 1
    SG = 2
    DB = 3
    SS = 4
    GW = 5


class StressState(IntEnum):
    CALM = 0
    ELEVATED = 1
    CRISIS = 2


class FinWindow(IntEnum):
    """Financing window (S-ADR-12)."""

    OPEN = 0
    TIGHT = 1
    CLOSED = 2


class Clock(StrEnum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class FlowType(IntEnum):
    """Cash-flow types, F = 18, with an expected sign and a cash flag (§1.4, §3.1).

    ``FlowType.sign(ft)`` is +1, −1 or 0 (either sign); ``FlowType.is_cash(ft)`` is False only for PIK_ACCRUAL.
    Both are table lookups that accept a member or a plain int code (``FlowType.sign(0) == -1``); an unknown code
    raises ``ValueError``.
    """

    CALL = 0
    DISTRIBUTION = 1
    INCOME_CASH = 2
    PIK_ACCRUAL = 3
    SALE_PROCEEDS = 4
    FEES = 5
    VM = 6
    DELTA_IM = 7
    PREMIUM = 8
    MONETIZATION = 9
    REDEMPTION_PAY = 10
    DEBT_DRAW = 11
    DEBT_REPAY = 12
    DEBT_SERVICE = 13
    CAPEX = 14
    OWNER_DRAW = 15
    OPEX = 16
    INTEREST_ON_CASH = 17

    def sign(self) -> int:
        return FLOW_SIGNS[FlowType(self)]

    def is_cash(self) -> bool:
        return FLOW_IS_CASH[FlowType(self)]


#                     CALL DIST INC  PIK  SALE FEES VM   DIM  PREM MON  RED  DDRW DREP DSRV CAPX OWN  OPEX INT
FLOW_SIGNS: Final[tuple[int, ...]] = (
    -1, +1, +1, +1, +1, -1, 0, 0, -1, +1, +1, +1, -1, -1, -1, -1, -1, 0)
FLOW_IS_CASH: Final[tuple[bool, ...]] = tuple(i != FlowType.PIK_ACCRUAL.value for i in range(18))
N_FLOW_TYPES: Final = 18


class Counterparty(StrEnum):
    EXTERNAL = "EXTERNAL"
    INTRA_ADIC = "INTRA_ADIC"


class SaleReason(IntEnum):
    """Reporting labels only; whether a sale is a T6 red event is decided by ``ledger.red_test`` (S-ADR-30)."""

    NONE = 0
    DISCRETIONARY = 1
    PLANNED = 2
    RECOURSE_LIQUID = 3
    RECOURSE_AMBER = 4
    RECOURSE_RED = 5


class RunMode(StrEnum):
    """S-ADR-37."""

    DEV_SYNTHETIC = "DEV_SYNTHETIC"
    REAL = "REAL"


class FactorKind(StrEnum):
    """How a ``ScenarioCube`` factor is stored (S-ADR-35; §1.2 spells the values in lower case)."""

    LOGRET = "logret"
    LEVEL = "level"
    CHANGE = "change"


class AnswerStatus(IntEnum):
    """Analyst answer status (S-ADR-34); an answer takes the minimum over the facts it cites."""

    EXPLORATORY = 0
    BASELINE = 1
    SEARCH = 2
    SEALED_NOT_QUALIFIED = 3
    QUALIFIED = 4


class DataClass(StrEnum):
    SYNTHETIC = "SYNTHETIC"
    REAL = "REAL"


class PricedOn(StrEnum):
    FEASIBLE = "feasible"
    RESTORED = "restored_problem"


class EvidencePlane(StrEnum):
    SEALED = "sealed"
    SEARCH = "search"
    EXPLORATORY = "exploratory"


class MarkType(StrEnum):
    UNDERWRITTEN = "UNDERWRITTEN"
    ACTUAL = "ACTUAL"
    FORECAST = "FORECAST"
    MARKET_IMPLIED = "MARKET_IMPLIED"


class Book(StrEnum):
    TAIL = "TAIL"
    OPP = "OPP"
    BETA = "BETA"


class HFLotState(IntEnum):
    LOCK = 0
    SOFT = 1
    OPEN = 2
    NOTICE = 3
    QUEUE = 4
    SUSP = 5
    PAY = 6
    SP = 7
    LIQ = 8
    DONE = 9
    TRS_TERM = 10


class CreditState(IntEnum):
    PERFORMING = 0
    PIK = 1
    AMENDED = 2
    EXTENDED = 3
    NONACCRUAL = 4
    DEFAULT = 5
    WORKOUT = 6
    RESOLVED = 7
    REPAID = 8


class RowFamily(StrEnum):
    TRANSITION = "TRANSITION"
    T1_PAYOUT = "T1_PAYOUT"
    T2_IG_HARD = "T2_IG_HARD"
    T2_IG_TARGET = "T2_IG_TARGET"
    T3_COV30 = "T3_COV30"
    T4P = "T4P"
    T4P_APPETITE = "T4P_APPETITE"
    T5_DEBT = "T5_DEBT"
    T5_EXPOSURE = "T5_EXPOSURE"
    T5_ENCUMBRANCE = "T5_ENCUMBRANCE"
    T5_PLEDGE = "T5_PLEDGE"
    T5_MATURITY = "T5_MATURITY"
    T8_DCR = "T8_DCR"
    LR4 = "LR4"
    LR8 = "LR8"
    NAVF_LTV = "NAVF_LTV"
    RA_LTV = "RA_LTV"
    SALE_DEPTH = "SALE_DEPTH"
    HF_NOTICE = "HF_NOTICE"
    P2S_CAP = "P2S_CAP"
    FAC_AVAIL = "FAC_AVAIL"
    RED_MARGIN = "RED_MARGIN"
    T6_CVAR = "T6_CVAR"
    FLOOR_CVAR = "FLOOR_CVAR"
    UTILITY = "UTILITY"
    SHORTFALL = "SHORTFALL"
    OV1 = "OV1"
    OV2 = "OV2"
    OV3 = "OV3"
    DEALER = "DEALER"
    TAIL_BUDGET = "TAIL_BUDGET"
    LEVEL_B = "LEVEL_B"


class RowRole(IntEnum):
    """Only PRICING rows feed λ, cards and envelopes."""

    DEFINITION = 0
    PRICING = 1
    APPETITE = 2
    STRUCTURAL = 3


class GateLabel(StrEnum):
    CORRECT = "CORRECT"
    PROMOTED = "PROMOTED"
    NOT_PROMOTED = "NOT_PROMOTED"
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    NOT_CORRECT = "NOT_CORRECT"
    NOT_ASSESSED = "NOT_ASSESSED"


class FailureLabel(StrEnum):
    INVALID_SPEC = "INVALID_SPEC"
    TIER1_FAIL = "TIER1_FAIL"
    FLOOR_FAIL = "FLOOR_FAIL"
    NI_FAIL = "NI_FAIL"
    OV_FAIL = "OV_FAIL"
    PINNED_DUAL = "PINNED_DUAL"
    GAMBLING = "GAMBLING"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


class OptionKind(StrEnum):
    STATUS_QUO = "STATUS_QUO"
    DEFER = "DEFER"
    RECOMMENDED = "RECOMMENDED"
    ALTERNATIVE = "ALTERNATIVE"
    ARCH_A = "ARCH_A"
    ARCH_B = "ARCH_B"
    ARCH_C = "ARCH_C"


class Tier(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    BOARD = "BOARD"


class RoleId(StrEnum):
    """LLM roles (§7.5). ANALYST is CHAT_ANALYST S-ADR-49's role, which supersedes QA_ANSWERER (kept for §7.5)."""

    CONTRACT_DRAFTER = "CONTRACT_DRAFTER"
    DESIGN_REVIEWER = "DESIGN_REVIEWER"
    IDEATOR = "IDEATOR"
    EXECUTOR = "EXECUTOR"
    ABLATION_PROPOSER = "ABLATION_PROPOSER"
    ABLATION_FILTER = "ABLATION_FILTER"
    RED_TEAM = "RED_TEAM"
    MEMO_WRITER = "MEMO_WRITER"
    AUDITOR = "AUDITOR"
    TRANSLATOR = "TRANSLATOR"
    QA_ANSWERER = "QA_ANSWERER"
    SEAT_NARRATOR = "SEAT_NARRATOR"
    FACILITATOR = "FACILITATOR"
    AI_VALIDATOR = "AI_VALIDATOR"
    MINUTES_DRAFTER = "MINUTES_DRAFTER"
    EXTRACTOR = "EXTRACTOR"
    ANALYST = "ANALYST"


class ModelFamily(StrEnum):
    A = "A"
    B = "B"
    C = "C"


class LLMMode(StrEnum):
    """Backend selection, spelled like ``TPA_LLM_MODE ∈ {offline, replay, live}`` (§7.1); any letter case maps."""

    OFFLINE = "offline"
    REPLAY = "replay"
    LIVE = "live"

    @classmethod
    def _missing_(cls, value: object) -> LLMMode | None:
        if isinstance(value, str):
            folded = value.strip().lower()
            for member in cls:
                if member.value == folded:
                    return member
        return None


class CampaignState(StrEnum):
    DRAFT = "DRAFT"
    FROZEN = "FROZEN"
    SIGNED = "SIGNED"
    SIGNED_IN_RECOVERY = "SIGNED_IN_RECOVERY"
    DESIGN_REVIEWED = "DESIGN_REVIEWED"
    BASELINE_PRICED = "BASELINE_PRICED"
    IDEATION = "IDEATION"
    SCREENING = "SCREENING"
    SELECTION = "SELECTION"
    SEALED = "SEALED"
    RETROSPECTIVE = "RETROSPECTIVE"
    MEMO = "MEMO"
    REVIEW = "REVIEW"
    SHADOW_IC = "SHADOW_IC"
    PREVOTE_LOCK = "PREVOTE_LOCK"
    IC = "IC"
    CLOSED = "CLOSED"
    ABORTED = "ABORTED"


class T6SurrogateKind(StrEnum):
    """S-ADR-07."""

    CVAR_CLASS = "CVAR_CLASS"
    WORST_CASE_CVAR = "WORST_CASE_CVAR"
    ALSO_X = "ALSO_X"


class TargetMode(StrEnum):
    """S-ADR-06 (``ObjectiveSpec.target_mode = "precommitted"``)."""

    PRECOMMITTED = "precommitted"
    ROLLING = "rolling"
