"""Optimizer contracts (BUILD_SPEC v1.1 §3.12, §3.18, §5; S-ADR-29, S-ADR-33).

Row and column keys are typed (``RowKey``, ``ColKey``) with canonical string forms such as ``T4P:h=07``,
``LR4:g=PE:h=24`` and ``TRANSITION:s=C:n=113`` (integers print zero-padded to two digits); column coefficient
vectors are keyed by ``str(RowKey)`` so columns can be built before H is assembled (BUILD-22).

``ActionSet`` is exported as an alias of ``ActionProposal`` (ARCH §3.5's name).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Final, Literal

from pydantic import ValidationError, model_validator

from adic_tpa.contracts.arrays import F64, I8, I32, ArrayContainer
from adic_tpa.contracts.enums import (
    ConsentScenario, ContractMode, ContractModel, FinWindow, PricedOn, RowFamily, StressState,
)
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.evidence import SolverRecord
from adic_tpa.contracts.ids import ArtifactRef, GroupId, UnitId

# scipy.sparse.csc_array [m, n]; typed Any so contracts need not import scipy (validate() duck-types it).
SparseMatrix = Any

__all__ = [
    "RowKey", "ColKey", "LPMeta", "LPModel", "RowTier", "Lever", "LeverSet", "TierResult", "Phase1Result",
    "GlidePath", "RecoveryPlan", "DualQuality", "DualSet", "HSolution", "Kernel", "FTPPoint", "FTPCurves",
    "Envelope", "EnvelopeSet", "Column", "ColumnPool", "Selection", "WhatChanged", "SafeAction", "ActionProposal",
    "ActionSet", "NodeCoefficients", "T6Screen", "LinearizedTier1", "ExactCheck", "VarIndex", "RowBlock",
    "RowIndex", "format_key_parts", "parse_key_parts", "SparseMatrix",
]

_INT_RE: Final = re.compile(r"^-?\d+$")
_KEY_PART_RE: Final = re.compile(r"^[A-Za-z0-9_]+$")
_VALUE_RE: Final = re.compile(r"^[A-Za-z0-9_.\-]+$")


def format_key_parts(idx: tuple[tuple[str, str | int], ...]) -> str:
    """``:k=v`` segments; integers zero-padded to two digits (``h=07``, ``n=113``)."""
    out = []
    for k, v in idx:
        out.append(f":{k}={v:02d}" if isinstance(v, int) else f":{k}={v}")
    return "".join(out)


def parse_key_parts(parts: list[str]) -> tuple[tuple[str, str | int], ...]:
    idx: list[tuple[str, str | int]] = []
    for part in parts:
        if "=" not in part:
            raise SchemaError(f"key segment {part!r} lacks '='")
        k, v = part.split("=", 1)
        idx.append((k, int(v) if _INT_RE.match(v) else v))
    return tuple(idx)


def _check_idx(idx: tuple[tuple[str, str | int], ...]) -> None:
    for k, v in idx:
        if not _KEY_PART_RE.match(k):
            raise ValueError(f"key name {k!r} must match [A-Za-z0-9_]+")
        if isinstance(v, str) and (not _VALUE_RE.match(v) or _INT_RE.match(v)):
            raise ValueError(f"key value {v!r} must be a non-numeric token [A-Za-z0-9_.-]+ (use an int for numbers)")


class RowKey(ContractModel):
    """Typed row key; ``str(RowKey)`` is the canonical form shared by H, the ledger and the columns."""

    family: RowFamily
    idx: tuple[tuple[str, str | int], ...] = ()

    @model_validator(mode="after")
    def _idx(self) -> RowKey:
        _check_idx(self.idx)
        return self

    def __str__(self) -> str:
        return self.family.value + format_key_parts(self.idx)

    @classmethod
    def parse(cls, s: str) -> RowKey:
        """Inverse of ``str``; ``SchemaError`` on a malformed key."""
        family, *parts = s.split(":")
        try:
            fam = RowFamily(family)
        except ValueError:
            raise SchemaError(f"unknown row family in {s!r}") from None
        try:
            return cls(family=fam, idx=parse_key_parts(parts))
        except ValidationError as exc:
            raise SchemaError(f"malformed row key {s!r}: {exc.errors()[0]['msg']}") from None


class ColKey(ContractModel):
    """Typed column key; ``str(ColKey)`` keys ``HSolution.root_values``."""

    family: Literal["state", "decision", "lens", "aux", "elastic"]
    name: str
    node: int | None = None
    idx: tuple[tuple[str, str | int], ...] = ()

    @model_validator(mode="after")
    def _idx(self) -> ColKey:
        if not _KEY_PART_RE.match(self.name):
            raise ValueError(f"column name {self.name!r} must match [A-Za-z0-9_]+")
        _check_idx(self.idx)
        return self

    def __str__(self) -> str:
        node = "" if self.node is None else f"@{self.node}"
        return f"{self.family}:{self.name}{node}" + format_key_parts(self.idx)

    @classmethod
    def parse(cls, s: str) -> ColKey:
        """Inverse of ``str``; ``SchemaError`` on a malformed key."""
        family, *rest = s.split(":")
        if not rest:
            raise SchemaError(f"malformed column key {s!r}: expected <family>:<name>[@node][:k=v...]")
        head, *parts = rest
        name, _, node = head.partition("@")
        try:
            node_index = int(node) if node else None
            return cls(family=family, name=name, node=node_index, idx=parse_key_parts(parts))  # type: ignore[arg-type]
        except (ValidationError, ValueError) as exc:
            msg = exc.errors()[0]["msg"] if isinstance(exc, ValidationError) else str(exc)
            raise SchemaError(f"malformed column key {s!r}: {msg}") from None


class LPMeta(ContractModel):
    tree_hash: str
    contract_hash: str
    catalogue_hash: str
    ledger_hash: str
    builder_version: str
    consent_scenario: ConsentScenario
    pricing_level: Literal["tolerance", "appetite"]
    replication: int


@dataclass(frozen=True, slots=True)
class LPModel(ArrayContainer):
    """The assembled H in W₀ units; sense is always MAXIMIZE (§5.5)."""

    name: str
    meta: LPMeta
    c: F64                         # [n]
    A: SparseMatrix                # [m, n] scipy.sparse.csc_array
    row_lo: F64                    # [m]  (−inf allowed)
    row_hi: F64                    # [m]  (+inf allowed)
    col_lo: F64                    # [n]
    col_hi: F64                    # [n]
    integrality: I8 | None         # [n]  Level B only
    row_keys: tuple[RowKey, ...]
    col_keys: tuple[ColKey, ...]
    row_role: I8                   # [m]  RowRole
    row_tier: I8                   # [m]  Phase-I tier (0 = not tiered)
    node_of_row: I32               # [m]
    node_of_col: I32               # [n]
    scale_bn: float                # W₀ in $bn (177.0 at the SYNTHETIC as-of)

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if not (self.row_lo <= self.row_hi).all() or not (self.col_lo <= self.col_hi).all():
            raise SchemaError("LPModel: lower bounds must not exceed upper bounds")
        if not self.scale_bn > 0:
            raise SchemaError("LPModel.scale_bn must be positive")


class RowTier(ContractModel):
    tier: int
    name: str
    families: tuple[RowFamily, ...]
    weight: float = 1.0


class Lever(ContractModel):
    lever_id: str
    owner_group: GroupId
    reversible: bool
    consent_scenario: ConsentScenario
    cap_bn: float
    cost: float                                  # PV cost per $bn used
    slope: tuple[float, ...]                     # 24 values: month-h T4′ headroom relief per $bn
    ig_effect: float = 0.0
    lag_q: int = 0
    shares_sleeve_with: str | None = None

    @model_validator(mode="after")
    def _slope(self) -> Lever:
        if len(self.slope) != 24:
            raise ValueError(f"Lever.slope needs 24 monthly values, got {len(self.slope)}")
        return self


class LeverSet(ContractModel):
    levers: tuple[Lever, ...]

    def available(self, scenario: ConsentScenario) -> tuple[Lever, ...]:
        """Levers usable under ``scenario`` (nested: every lever whose consent scenario ≤ ``scenario``)."""
        return tuple(lv for lv in self.levers if lv.consent_scenario <= scenario)


class TierResult(ContractModel):
    tier: int
    u_star_bn: float
    violations_bn: dict[str, float]
    iis: tuple[str, ...]
    farkas_ray_ref: ArtifactRef | None
    levers_at_cap: tuple[str, ...]
    solver: SolverRecord


class Phase1Result(ContractModel):
    by_scenario: dict[ConsentScenario, tuple[TierResult, ...]]
    d0_bn: float
    mode: ContractMode
    pricing_scenario: ConsentScenario
    infeasibility_prices: dict[str, float]       # Treasurer panel only; never on cards, envelopes or FTP
    recovery_hash: str | None


class GlidePath(ContractModel):
    kind: Literal["none", "execution", "structural"]
    t_rec_q: int = 4
    d0_bn: float = 0.0
    u_star_by_row: dict[str, float] = {}
    g_bn: tuple[float, ...]                      # per quarter t = 0..T_rec: g_t = d0 (1 − t/T_rec)+
    phi_g: dict[GroupId, tuple[float, ...]] = {} # delivery shares per quarter (ARCH §6.4)
    recovery_hash: str


class RecoveryPlan(ContractModel):
    mode: ContractMode
    u_star_bn: float
    d0_bn: float
    iis: tuple[str, ...]
    glide: GlidePath
    board_signoff_required: bool
    owner_signoff_required: bool


class DualQuality(ContractModel):
    one_sided: tuple[float, float]
    at_kink: bool
    ranging: tuple[float, float]
    band: tuple[float, float, float]             # min, median, max across SAA replications
    sign_flip: bool
    pinned: bool
    method: Literal["ranging", "parametric_step", "finite_difference"]   # FD only on ≤ 10 rows (S-ADR-38)


@dataclass(frozen=True, slots=True)
class DualSet(ArrayContainer):
    pi_row: F64                                  # [m]  normalized shadow prices (§5.8)
    mu_cash: F64                                 # [N]  value of an exogenous W₀-unit of cash at node n
    M_cash: F64                                  # [N]  dual mass of PRICING liquidity rows containing C_n
    ell: F64                                     # [N]  ℓ_n = M_n / (μ_n − M_n), per period
    quality: dict[str, DualQuality]              # keyed by str(RowKey), PRICING rows shown on cards

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        # §3.17: ℓ ≥ 0 wherever μ − M > 0 (where μ − M ≤ 0 ℓ is undefined and pricing refuses; §5.8)
        if (self.ell[(self.mu_cash - self.M_cash) > 0] < -1e-12).any():
            raise SchemaError("DualSet.ell must be >= 0 where mu_cash - M_cash > 0")


@dataclass(frozen=True, slots=True)
class HSolution(ArrayContainer):
    meta: LPMeta
    status: str
    objective: float
    x: F64                                       # [n]
    duals: DualSet
    root_values: dict[str, float]                # str(ColKey) -> value, root decisions and lens columns
    marginal_utility_wealth: float               # ū′ (CE conversion, §5.11)
    priced_on: PricedOn
    consent_scenario: ConsentScenario
    pricing_level: Literal["tolerance", "appetite"]
    recovery_hash: str | None
    replication: int
    solver: SolverRecord
    resolve_counts: dict[Literal["selection", "finite_difference", "parametric", "forced"], int] = field(
        default_factory=dict)                    # logged in the manifest
    exact_objective: float | None = None         # exact CRRA/shortfall at the solution's leaf wealth (A8)

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if self.priced_on is PricedOn.RESTORED and self.recovery_hash is None:
            raise SchemaError("HSolution priced on the restored problem needs recovery_hash")


class Kernel(ContractModel):
    pi: tuple[float, ...]
    ell: tuple[float, ...]
    deflator: tuple[float, ...]
    esscher_gamma: float
    lambda_spot: dict[StressState, float]
    one_off_premium: float
    priced_on: PricedOn
    recovery_hash: str | None


class FTPPoint(ContractModel):
    tenor_q: int
    decision_q: float
    published_q: float
    band_q: tuple[float, float]
    components: dict[RowFamily, float]           # λ decomposition by binding row (S-ADR-16)
    fin_window: FinWindow | None = None
    priced_on: PricedOn
    recovery_hash: str | None


class FTPCurves(ContractModel):
    asof: date
    tolerance: tuple[FTPPoint, ...]
    appetite: tuple[FTPPoint, ...] | None
    ewma_halflife_q: int = 2
    collar: float = 0.5


class Envelope(ContractModel):
    group: GroupId
    row: str
    value_bn: float
    range_bn: tuple[float, float]
    dual: float
    ranging_bn: tuple[float, float]
    elasticity_bn_per_100bp: float
    delivery_share: float | None
    priced_on: PricedOn
    recovery_hash: str | None


class EnvelopeSet(ContractModel):
    envelopes: tuple[Envelope, ...]
    pool_bn: dict[str, float]
    slack_bn: dict[str, float]
    risk_haircut: float = 0.10                   # S-ADR-16


class Column(ContractModel):
    col_id: str
    unit_id: UnitId | None
    group: GroupId
    action: LensAction
    node_coeffs_ref: ArtifactRef                 # sparse vector keyed by str(RowKey), not row number
    cost: float
    consent_p: float
    lag_q: int
    min_ticket_bn: float
    irreversible: bool
    t6_consuming: bool = False                   # red-tier SELL meeting ledger.red_test (ii)/(iii): bound 0 in Phase II


class ColumnPool(ContractModel):
    columns: tuple[Column, ...]
    tree_hash: str


class Selection(ContractModel):
    chosen: tuple[str, ...]
    x: dict[str, float]
    split_assets: tuple[UnitId, ...]             # marginal-asset agenda
    gamma_bp: float
    gamma_bp_exact: float
    certified: bool
    iterations: int
    forced_resolve_flags: dict[str, bool]
    calibration_capped: bool = False             # S-ADR-44


class WhatChanged(ContractModel):
    field: str
    before: float
    after: float
    reason_row: str


class ActionProposal(ContractModel):
    """ARCH §3.5 calls this type ``ActionSet`` (exported as an alias)."""

    source: Literal["optimizer", "agent", "ic_amendment", "archetype", "standing_policy"]
    root_values: dict[str, float]
    lens_actions: tuple[LensAction, ...]


ActionSet = ActionProposal


class SafeAction(ContractModel):
    action: ActionProposal
    changed: tuple[WhatChanged, ...]
    binding_rows: tuple[str, ...]
    projected: bool
    tier1_override_needed: bool
    exact_recheck_passed: bool


@dataclass(frozen=True, slots=True)
class NodeCoefficients(ArrayContainer):
    """GroupRates aggregated per node (fan periods compounded); rates only, never amounts (§3.18)."""

    delta: F64
    qcall: F64
    ret_simple: F64
    bid: F64
    income: F64                                  # [N, Gp, 2]
    u_per_nav: F64
    nav_share: F64
    call_stress_12m: F64                         # [N, Gp, 2]  κ^U, ω, H3 outflow rate
    lo_ret: F64
    hf_ret: F64
    vm_per_beta: F64
    cash_rate: F64
    fac_rate: F64
    draw_rate_q: F64
    tau_lo: F64
    h_im: F64                                    # [N]
    ra_debt_rate: F64
    ra_amort: F64
    ra_direct_share: F64                         # [N]
    tail_prem_rate: F64
    tail_value: F64
    opp_pnl_rate: F64
    delta_im_rate: F64
    opex_rate: F64                               # [N]
    hf_phi: F64                                  # [N, 4]
    fac_avail: F64                               # [N, NF]  availability multipliers (≤ 0.5 in the joint oil–crisis state)
    amber_depth: F64                             # [N, Ga]  depth fraction per amber group


class T6Screen(ContractModel):
    scenario: ConsentScenario
    levers_at_cap: tuple[str, ...]
    t6_cvar_at_hold: dict[str, float]            # per class (W₀ units)
    floor_cvar_at_hold: dict[str, float]         # per world (Tier 1B)
    breach: dict[str, Literal["none", "tolerance", "capacity"]]   # only "capacity" triggers Phase I-b (S-ADR-31)


@dataclass(frozen=True, slots=True)
class LinearizedTier1(ArrayContainer):
    row_keys: tuple[RowKey, ...]
    action_names: tuple[str, ...]
    G: F64                                       # [m_F, n_a]
    g0: F64                                      # [m_F]
    delta: F64                                   # [m_F]
    fd_checked: bool


class ExactCheck(ContractModel):
    passed: bool
    violations: dict[str, float]
    simm_im_bn: float
    ov3_share: float
    recomputed_rows: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class VarIndex(ArrayContainer):
    state_names: tuple[str, ...]
    decision_names: tuple[str, ...]
    state_cols: I32                              # [N, n_state]
    decision_cols: I32                           # [N, n_dec]; −1 where a decision does not exist at a node
    root_cols: dict[str, int]
    leaf_cols: dict[str, I32]                    # u, psi, w_tilde, z_<class>, z_floor


@dataclass(frozen=True, slots=True)
class RowBlock(ArrayContainer):
    """COO triplets for a batch of rows."""

    row_keys: tuple[RowKey, ...]
    i: I32
    j: I32
    v: F64
    lo: F64
    hi: F64
    role: I8
    tier: I8

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if self.i.size and int(self.i.max()) >= len(self.row_keys):
            raise SchemaError("RowBlock.i indexes past row_keys")
        if not (self.lo <= self.hi).all():
            raise SchemaError("RowBlock: lo must not exceed hi")


@dataclass(frozen=True, slots=True)
class RowIndex(ArrayContainer):
    """``str(RowKey)`` → row number in the assembled LPModel (built after ``build_h``; BUILD-22)."""

    row_of: dict[str, int]


# Deferred import (see contracts.actions): actions imports ColumnPool from this module.
from adic_tpa.contracts.actions import LensAction  # noqa: E402

for _model in (Column, ColumnPool, ActionProposal, SafeAction):
    _model.model_rebuild()
del _model
