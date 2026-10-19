"""Ledger contracts and the recourse protocol (BUILD_SPEC v1.1 §3.9, §3.18; ARCH §4.9; S-ADR-29, -30, -32).

The recourse protocol has one owner per fact: every engine publishes ``RecourseAvailability`` at quarter start;
``Ledger.apply`` executes the waterfall, books proceeds once and returns ``RecourseOutcome``; engines apply it
before t + 1. Red status comes from ``ledger.red_test`` on economic substance, never from a ``SaleReason`` label.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, Literal

import numpy as np
from pydantic import model_validator

from adic_tpa.contracts.arrays import B, F32, F64, I8, I16, ArrayContainer
from adic_tpa.contracts.enums import CFPStage, ContractModel, RecourseTier
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.ids import GroupId, UnitId
from adic_tpa.contracts.optimizer import RowKey

__all__ = [
    "LedgerState", "LedgerPaths", "OverlayStressConvention", "RAStressConvention", "CanonicalConventions",
    "ConventionSets", "StressSpec", "StressReport", "CFPReading", "RecourseAvailability", "RecourseOutcome",
    "S_STAR_EQUITY_BASE", "S_STAR_EQUITY_SLOPE", "S_STAR_DIST_BASE", "S_STAR_CALL_SLOPE", "S_STAR_BASE_CALL_RATE_A",
]

# s*(θ) definition (gap_02 §1; ARCH §4.9): equity −(0.30 + 0.10θ); distributions 0.45(1 − θ) × drought rates on
# groups flagged fund_distribution_stress; calls (1 + 0.5θ) × 28% of unfunded a year; 24 months.
S_STAR_EQUITY_BASE: Final = 0.30
S_STAR_EQUITY_SLOPE: Final = 0.10
S_STAR_DIST_BASE: Final = 0.45
S_STAR_CALL_SLOPE: Final = 0.5
S_STAR_BASE_CALL_RATE_A: Final = 0.28


@dataclass(slots=True)
class LedgerState(ArrayContainer):
    """One path block at monthly instant ``m`` (mutable: the kernel advances it in place)."""

    m: int
    fy: int
    hqla_unenc_bn: F64           # [P] unencumbered, haircut HQLA under CF control
    treasury_bn: F64             # [P, 3] cash, UST, IG (market value)
    posted_im_bn: F64
    vm_balance_bn: F64
    vm_in_transit_bn: F64        # [P]
    fac_drawn_bn: F64
    fac_limit_bn: F64            # [P, NF]
    asset_debt_bn: F64           # [P] RA non-recourse (look-through only)
    unit_debt_bn: F64            # [P] Σ UnitFinancing balances (look-through leverage; BUILD-24)
    encumbrance_bn: F64
    nav_econ_bn: F64
    nav_rep_bn: F64
    liquid_bn: F64               # [P]
    nav_group_econ: F64
    nav_group_rep: F64
    unfunded_group: F64          # [P, G]
    draw_basis_bn: F64
    draw_rate: F64
    payout_ytd_bn: F64           # [P]
    twr_index: F64
    twr_peak: F64
    cushion: F64                 # [P]
    readiness: I8
    event: I8
    planning: I8
    playbook: I8                 # [P] CFPStage
    event_hist: I8               # [P, 2] last two event readings (hysteresis)
    red_event: B
    payout_short: B
    failed: B                    # [P]
    red_month: I16               # [P] first red month, −1 if none

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        bad = (self.playbook >= CFPStage.RED) & (self.event < CFPStage.RED)
        if bad.any():
            raise SchemaError("LedgerState: playbook RED/BLACK requires event stage >= RED (ARCH §4.9)")


@dataclass(frozen=True, slots=True)
class LedgerPaths(ArrayContainer):
    row_keys: tuple[RowKey, ...]
    rows: F32                    # [P, M + 1, R] row slacks at monthly instants ($bn; ≥ 0 means satisfied)
    stages: I8                   # [P, M + 1, 4] readiness, event, planning, playbook


class OverlayStressConvention(ContractModel):
    beta_notional_bn: float = 10.0
    im_from: float = 0.04
    im_to: float = 0.10
    tail_monetization: bool = True
    opp_loss: Literal["ov2_consistent", "pct_nav"] = "ov2_consistent"   # S-ADR-32
    opp_loss_pct_nav: float = 0.015              # used only by the research ("as ratified") sensitivity set


class RAStressConvention(ContractModel):
    """S-ADR-32; replaces the PE distribution multiplier for Real Assets. Values [I] live in
    ``config/ledger/t4prime_canonical_v1.yaml``."""

    noi_yield_mult: float
    development_calls: bool = True
    refinancing_wall: bool = True
    refi_spread_stress_a: float
    refi_ltv_cap: float


class CanonicalConventions(ContractModel):
    """Hashed contract fields (ARCH §4.9 table); defaults are the lab's internally consistent pricing set."""

    draw_basis: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"] = "opening_fy_reported_nav"
    draw_rate_in_stress: float = 0.10
    draw_years_capped: int = 2
    revolver_credit: float = 0.50                # s* is the joint oil–crisis state (S-ADR-12/32); 0.80 research
    revolver_from_month: int = 2
    nav_facility_ltv_stressed: float = 0.05
    pledge_pool_cap: float = 0.20
    ig_target: float = 0.08
    ig_hard: float = 0.04
    ig_restore_quarters: int = 4
    credit_cash_a: dict[GroupId, float]          # no code default: values live in config (group-id lint)
    hf_whole_book_noticed: bool = True
    hf_pass_through: float = 0.83
    new_commitments_bn_a: float = 12.0
    commitment_split: dict[GroupId, float]
    overlay: OverlayStressConvention = OverlayStressConvention()
    real_assets: RAStressConvention
    shock_timing: Literal["vertex_t0"] = "vertex_t0"
    pacing_credit_lag_q: int = 2                 # S-ADR-20/32; 0 only in the ported research fixtures

    @model_validator(mode="after")
    def _split(self) -> CanonicalConventions:
        total = sum(self.commitment_split.values())
        if self.commitment_split and abs(total - 1.0) > 1e-9:
            raise ValueError(f"commitment_split must sum to 1, got {total}")
        if not 0.0 <= self.revolver_credit <= 1.0:
            raise ValueError("revolver_credit must lie in [0, 1]")
        return self


class ConventionSets(ContractModel):
    """What prices and what prints as a sensitivity until A1 (S-ADR-32)."""

    pricing: CanonicalConventions                # the internally consistent set
    research: CanonicalConventions               # "as ratified": revolver 0.80, opp loss 1.5% NAV, lag 0, RA via dist_mult


class StressSpec(ContractModel):
    name: str
    theta: float
    months: int = 24
    equity_shock: float                          # −(0.30 + 0.10 θ)
    dist_mult: float                             # 0.45 (1 − θ), groups with fund_distribution_stress; never RA
    call_mult: float                             # 1 + 0.5 θ
    base_call_rate_a: float = 0.28
    conventions: CanonicalConventions
    role: Literal["pricing", "reverse"]          # reverse stresses never price (PricingRefused)

    @classmethod
    def s_star(cls, theta: float, conv: CanonicalConventions) -> StressSpec:
        """The canonical pricing stress s*(θ) (§3.9; ARCH §4.9)."""
        if not 0.0 <= theta <= 1.0:
            raise SchemaError(f"theta must lie in [0, 1], got {theta}")
        return cls(name=f"s*({theta:.4f})", theta=float(theta), months=24,
                   equity_shock=-(S_STAR_EQUITY_BASE + S_STAR_EQUITY_SLOPE * theta),
                   dist_mult=S_STAR_DIST_BASE * (1.0 - theta), call_mult=1.0 + S_STAR_CALL_SLOPE * theta,
                   base_call_rate_a=S_STAR_BASE_CALL_RATE_A, conventions=conv, role="pricing")


@dataclass(frozen=True, slots=True)
class StressReport(ArrayContainer):
    spec_hash: str
    headroom_bn: F64                             # [P, 24] hd_h on T + P + F (facility-inclusive)
    nco_bn: F64                                  # [P, 24]
    cbc_bn: dict[RecourseTier, F64]              # each [P, 24]
    survival_months: dict[RecourseTier, I16]     # each [P]; 25 means "> 24"; APPETITE reads survival_months[TP]
    gap_bn: F64                                  # [P] G* = max_h [NCO(h) + 0.04 W(h) − CBC_TP(h)]
    d0_bn: F64                                   # [P] max(0, −min_h hd_h)

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        expected = np.maximum(0.0, -self.headroom_bn.min(axis=1))
        if not np.allclose(self.d0_bn, expected, rtol=0.0, atol=1e-9):
            raise SchemaError("StressReport: d0_bn must equal max(0, −min_h headroom_bn)")


class CFPReading(ContractModel):
    readiness: CFPStage
    event: CFPStage
    planning: CFPStage
    playbook: CFPStage
    indicators: dict[Literal["sh_tp_months", "lcr30", "treasury_share", "liquid_share", "lar99_over_cbc"], float]
    triggers: tuple[str, ...]

    @model_validator(mode="after")
    def _invariant(self) -> CFPReading:
        if self.playbook >= CFPStage.RED and self.event < CFPStage.RED:
            raise ValueError("playbook RED/BLACK requires event stage >= RED (ARCH §4.9 invariant)")
        return self


@dataclass(frozen=True, slots=True)
class RecourseAvailability(ArrayContainer):
    """Published by every ``AssetEngine.recourse_quotes`` at quarter start (phase 1)."""

    engine_id: str
    unit_ids: tuple[UnitId, ...]
    group_of: tuple[GroupId, ...]
    bid_frac: F32                # [P, U_r] cash-equivalent bid ÷ economic NAV (incl. crowding haircut)
    normal_bid_frac: F32         # [U_r] normal-regime hedonic bid (red test (iii))
    depth_frac: F32              # [P, U_r] maximum fraction saleable this quarter
    lag_m: I8                    # [P, U_r] settlement lag in months
    tier: I8                     # [U_r] 1 = amber, 2 = red (from the taxonomy)


@dataclass(frozen=True, slots=True)
class RecourseOutcome(ArrayContainer):
    """Returned by ``Ledger.apply`` (phase 2); consumed by ``AssetEngine.apply_recourse`` (phase 3)."""

    unit_ids: tuple[UnitId, ...]
    sold_frac: F32               # [P, U_r] fraction sold by recourse_cover this quarter
    month: I16                   # [P, U_r] month of the sale, −1 if none
    proceeds_bn: F64             # [P, U_r] booked by the ledger after the lag
    red: B                       # [P, U_r] ledger.red_test result (S-ADR-30)
    reason: I8                   # [P, U_r] SaleReason label (reporting only)

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if ((self.month < 0) & (self.sold_frac > 0)).any():
            raise SchemaError("RecourseOutcome: a sold fraction needs a sale month")
        if (self.red & (self.sold_frac <= 0)).any():
            raise SchemaError("RecourseOutcome: red flags only on sold units")

    def check_against(self, quotes: RecourseAvailability) -> None:
        """Cross-check with the quarter's quotes: sold ≤ depth and red only where the tier is red (§3.17)."""
        if tuple(quotes.unit_ids) != tuple(self.unit_ids):
            raise SchemaError("RecourseOutcome.unit_ids must match the quotes' unit_ids")
        if (self.sold_frac > quotes.depth_frac + 1e-6).any():
            raise SchemaError("RecourseOutcome: sold_frac exceeds depth_frac")
        if (self.red & (quotes.tier[np.newaxis, :] != 2)).any():
            raise SchemaError("RecourseOutcome: red flags only where tier = red")
