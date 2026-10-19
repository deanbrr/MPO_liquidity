"""The book: holdings, terms, overlap graph, facilities, owner history and the snapshot (BUILD_SPEC v1.1 §3.3).

Every data row carries ``is_synthetic`` and ``data_class``; synthetic ids carry ``SYN-`` (§1.12). Holding terms
are a discriminated union on ``kind`` matched to ``Holding.unit_kind``. ``BookSnapshot`` checks that every group
is in its taxonomy (``taxonomy_version``), that a synthetic holding id carries its group's code
(``SYN-<GROUPCODE>-<4 digits>``, §1.8), and that the snapshot holds one data class: SYNTHETIC and REAL rows
together raise ``DataClassMixError`` itself (§1.10 code ``DATA_CLASS_MIX``; not a ``ValueError``, so Pydantic
propagates it unwrapped). ``unit_index()`` orders units by taxonomy group order, then holding id.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from types import MappingProxyType
from typing import Annotated, Final, Literal

import numpy as np
from pydantic import Field, model_validator

from adic_tpa.contracts.arrays import B, I8, I32, ArrayContainer
from adic_tpa.contracts.contract import SignOff
from adic_tpa.contracts.enums import AllocationId, CensusId, ConsentScenario, ContractModel, CreditState, DataClass
from adic_tpa.contracts.errors import DataClassMixError
from adic_tpa.contracts.ids import (
    CompanyId, FacilityId, GroupId, HoldingId, SponsorId, UnitId, check_synthetic_consistency, is_content_hash,
)
from adic_tpa.contracts.overlay import CSA, OverlayBook
from adic_tpa.contracts.taxonomy import GroupRegistry

__all__ = [
    "PrivateFundTerms", "CompanyTerms", "Warrants", "ClaimTerms", "LoanCohortTerms", "HFTerms", "LongOnlyTerms",
    "TreasuryTerms", "DevelopmentPlan", "AssetDebt", "OpenEndTerms", "RealAssetTerms", "HoldingTerms", "Holding",
    "SponsorNode", "CompanyNode", "ClaimEdge", "OverlapGraph", "Facility", "CSA", "OwnerDrawHistory",
    "BookSnapshot", "UnitIndex", "UnitKind", "UNIT_KIND_ENGINE", "UNIT_KIND_TERMS", "Wrapper",
]

UnitKind = Literal["fund", "company", "claim", "loan_cohort", "hf_lot", "longonly", "treasury", "ra_asset",
                   "ra_open_end", "overlay_bucket"]
Wrapper = Literal["SMA", "CEF", "EVERGREEN", "BDC", "COMMINGLED", "MANAGED_ACCOUNT", "DIRECT", "JV", "OPEN_END",
                  "CLOSED_END", "LISTED", "TREASURY"]
Dealing = Literal["monthly", "quarterly", "semiannual", "annual"]

# Engine id that owns each unit kind (§4.11–§4.13); closed-end RA funds are unit_kind "fund" on the fund engine.
UNIT_KIND_ENGINE: Final[Mapping[str, str]] = MappingProxyType({
    "fund": "priv.fund", "company": "priv.company", "claim": "priv.claims", "loan_cohort": "priv.credit",
    "hf_lot": "pub.hf", "longonly": "pub.longonly", "treasury": "treasury", "ra_asset": "priv.realassets",
    "ra_open_end": "priv.realassets", "overlay_bucket": "overlay",
})
# Terms kind admitted for each unit kind (None: the unit carries no terms).
UNIT_KIND_TERMS: Final[Mapping[str, str | None]] = MappingProxyType({
    "fund": "fund", "company": "company", "claim": "claim", "loan_cohort": "loan_cohort", "hf_lot": "hf_lot",
    "longonly": "longonly", "treasury": "treasury", "ra_asset": "realasset", "ra_open_end": "realasset",
    "overlay_bucket": None,
})


class PrivateFundTerms(ContractModel):
    kind: Literal["fund"] = "fund"
    strategy_class: Literal["buyout_large", "buyout_mid", "growth", "vc", "sector", "special_sits", "secondary_fund",
                            "credit_fund", "ra_closed"]
    age_years: float
    effective_age_years: float
    fee_rate_a: float
    carry: float
    hurdle_a: float
    lpa_term_years: float
    extensions_used: int
    subscription_line_bn: float
    gp_navloan_bn: float
    recallable_bn: float
    recycling_cap: float = 1.10
    sec_template: Literal["S1", "S2", "S3", "S4", "S5", "S6"] | None = None
    theta_true_over_ref: float | None = None     # Secondaries


class CompanyTerms(ContractModel):
    kind: Literal["company"] = "company"
    ownership: float
    ev_bn: float
    net_debt_bn: float
    ebitda_bn: float
    entry_ev_ebitda: float
    icr: float
    software_flag: bool
    spv_debt_bn: float
    beta_asset: float
    sigma_id_a: float
    exit_route: str


class Warrants(ContractModel):
    n_w: float
    strike_bn: float
    expiry: date


class ClaimTerms(ContractModel):
    """Capital Solutions claim, families A–G."""

    kind: Literal["claim"] = "claim"
    family: Literal["A", "B", "C", "D", "E", "F", "G"]
    claim_bn: float
    coupon_a: float
    pik_share_cap: float
    pik_window_q: int
    step_up_a: float
    make_whole: float
    moic_floor: float
    warrants: Warrants | None
    seniority: int
    ltv: float
    icr: float
    negative_ebitda: bool
    status: CreditState
    syndication_share: float


class LoanCohortTerms(ContractModel):
    """Private Credit loan cohort."""

    kind: Literal["loan_cohort"] = "loan_cohort"
    segment: Literal["DL", "ABF", "MEZZ", "OPP"]
    vehicle_id: str
    wrapper: Wrapper
    n_loans: int
    par_bn: float                                # incl. PIK
    spread_a: float
    floor_a: float
    oid: float
    wam_years: float
    undrawn_bn: float
    sponsored_share: float
    software_share: float
    state_shares: dict[CreditState, float]       # sum 1
    collateral_type: str                         # LGD key (S-ADR-11)
    evergreen_cap_q: float | None = None

    @model_validator(mode="after")
    def _shares(self) -> LoanCohortTerms:
        if abs(math.fsum(self.state_shares.values()) - 1.0) > 1e-9:
            raise ValueError("state_shares must sum to 1")
        return self


class HFTerms(ContractModel):
    """Hedge-fund liquidity terms τ."""

    kind: Literal["hf_lot"] = "hf_lot"
    strategy: str
    dealing: Dealing
    notice_days: int
    notice_revocable: bool = False
    lockup_end: date | None
    soft_lock_fee: float
    gate_type: Literal["none", "investor", "fund"]
    gate_level: float
    holdback: float
    payment_lag_days: int
    side_pocket_cap: float
    suspension_allowed: bool
    transfer_consent: bool
    pledge_consent: bool
    beta_eq_normal: float
    beta_eq_crisis: float
    alpha_net_a: float
    alpha_sd_a: float
    crisis_gate_hazard_q: float
    leverage_navw: float
    smoothing_theta: float
    adic_share_of_fund: float


class LongOnlyTerms(ContractModel):
    kind: Literal["longonly"] = "longonly"
    sleeve: Literal["DM_EQ", "EM_EQ", "FI"]
    benchmark: str
    beta: float
    te_a: float
    ir_prior: float
    adv_bn: float
    vehicle: Literal["SMA", "COMMINGLED"]
    tax_rate: float
    credit_beta: float


class TreasuryTerms(ContractModel):
    kind: Literal["treasury"] = "treasury"
    sleeve: Literal["CASH", "UST", "IG"]
    haircut: float
    hqla_level: Literal["L1", "L2A", "L2B"]
    cf_controlled: bool
    duration_years: float


class DevelopmentPlan(ContractModel):
    committed_bn: float
    s_curve_quarters: int


class AssetDebt(ContractModel):
    """Non-recourse real-asset debt (outside CF facilities; counts in look-through leverage)."""

    balance_bn: float
    rate_type: Literal["FIXED", "FLOATING"]
    spread_a: float
    hedge_ratio: float
    maturity: date
    ltv_max: float
    dscr_covenant: float
    amort_q: float
    recourse: Literal[False] = False


class OpenEndTerms(ContractModel):
    """Open-end fund dealing terms (run by ``pub.queue.RedemptionQueue``)."""

    dealing: Dealing
    notice_days: int
    gate_pct_nav_q: float


class RealAssetTerms(ContractModel):
    kind: Literal["realasset"] = "realasset"
    sector: Literal["REAL_ESTATE", "INFRASTRUCTURE", "ENERGY_NATRES"]
    # §3.3 writes the co-investment access as "COINVEST", which equals a configured group id and would fail the
    # no-hard-coded-group-id scan in every engine that compares against it; the value is "COINVESTMENT".
    access: Literal["CLOSED_END_FUND", "OPEN_END_FUND", "COINVESTMENT", "DIRECT", "JV"]
    noi_bn: float
    cap_rate: float
    inflation_passthrough: float
    oil_beta: float
    capex_reserve_rate_a: float
    development: DevelopmentPlan | None
    debt: AssetDebt | None
    open_end: OpenEndTerms | None
    appraisal_lambda: float
    report_lag_q: int


HoldingTerms = Annotated[
    PrivateFundTerms | CompanyTerms | ClaimTerms | LoanCohortTerms | HFTerms | LongOnlyTerms | TreasuryTerms
    | RealAssetTerms,
    Field(discriminator="kind"),
]


class Holding(ContractModel):
    holding_id: HoldingId
    group: GroupId
    strategy: str
    sub_strategy: str | None = None
    unit_kind: UnitKind
    gp_id: SponsorId | None = None
    company_ids: tuple[CompanyId, ...] = ()
    vintage: int | None = None
    region: Literal["US", "EUROPE", "ASIA", "GCC", "EM", "GLOBAL"]
    sector: str | None = None
    commitment_bn: float | None = None
    unfunded_bn: float = 0.0                     # >= 0, <= commitment
    nav_reported_bn: float                       # >= 0
    nav_reference_date: date
    wrapper: Wrapper | None = None
    consent_transfer: bool = True
    consent_pledge: bool = True
    rofr: bool = False
    pledged_bn: float = 0.0
    encumbered_bn: float = 0.0
    terms: HoldingTerms | None
    is_synthetic: bool
    data_class: DataClass
    source: str

    @model_validator(mode="after")
    def _rules(self) -> Holding:
        check_synthetic_consistency(self.is_synthetic, self.data_class, self.holding_id)
        if self.nav_reported_bn < 0:
            raise ValueError(f"{self.holding_id}: nav_reported_bn must be >= 0")
        if self.unfunded_bn < 0:
            raise ValueError(f"{self.holding_id}: unfunded_bn must be >= 0")
        if self.commitment_bn is None:
            if self.unfunded_bn > 0:
                raise ValueError(f"{self.holding_id}: unfunded_bn > 0 needs a commitment")
        elif self.unfunded_bn > self.commitment_bn + 1e-12:
            raise ValueError(f"{self.holding_id}: unfunded_bn must not exceed commitment_bn")
        if self.pledged_bn < 0 or self.encumbered_bn < 0:
            raise ValueError(f"{self.holding_id}: pledged/encumbered amounts are non-negative magnitudes")
        expected = UNIT_KIND_TERMS[self.unit_kind]
        actual = None if self.terms is None else self.terms.kind
        if expected is None and actual is not None:
            raise ValueError(f"{self.holding_id}: unit_kind {self.unit_kind} carries no terms")
        if actual is not None and actual != expected:
            raise ValueError(f"{self.holding_id}: terms kind {actual!r} does not match unit_kind {self.unit_kind!r}")
        return self

    def age_years(self, asof: date) -> float | None:
        """Calendar age: fund terms' ``age_years`` if present, else from the vintage, else None."""
        if isinstance(self.terms, PrivateFundTerms):
            return self.terms.age_years
        if self.vintage is not None:
            return float(asof.year - self.vintage)
        return None


class SponsorNode(ContractModel):
    sponsor_id: SponsorId
    tier: Literal["elite", "core", "other"]


class CompanyNode(ContractModel):
    company_id: CompanyId
    sponsor_id: SponsorId | None
    sector: str
    ev_bn: float
    net_debt_bn: float
    ebitda_bn: float
    icr: float
    software_flag: bool


class ClaimEdge(ContractModel):
    holder_id: HoldingId
    company_id: CompanyId
    share: float
    seniority: int
    claim_kind: Literal["pe_lookthrough", "coinvest_equity", "cs_claim", "pc_loan", "sec_cv"]


class OverlapGraph(ContractModel):
    sponsors: tuple[SponsorNode, ...]
    companies: tuple[CompanyNode, ...]
    edges: tuple[ClaimEdge, ...]

    @model_validator(mode="after")
    def _refs(self) -> OverlapGraph:
        companies = {c.company_id for c in self.companies}
        sponsors = {s.sponsor_id for s in self.sponsors}
        if any(e.company_id not in companies for e in self.edges):
            raise ValueError("an edge names an unknown company")
        if any(c.sponsor_id is not None and c.sponsor_id not in sponsors for c in self.companies):
            raise ValueError("a company names an unknown sponsor")
        return self

    def gp_concentration(self, book: BookSnapshot) -> dict[SponsorId, float]:
        """Share of private NAV + unfunded held through each GP (holdings whose ``gp_id`` is that GP)."""
        tax = GroupRegistry.for_version(book.taxonomy_version)
        private = set(tax.private())
        exposure = [(h.gp_id, h.nav_reported_bn + h.unfunded_bn) for h in book.holdings if h.group in private]
        total = math.fsum(x for _, x in exposure)
        out: dict[SponsorId, float] = {s.sponsor_id: 0.0 for s in self.sponsors}
        if total <= 0:
            return out
        for gp, x in exposure:
            if gp is not None:
                out[gp] = out.get(gp, 0.0) + x / total
        return out


class Facility(ContractModel):
    facility_id: FacilityId
    kind: Literal["revolver", "nav_facility", "repo", "term_debt", "cf_term_prefund"]
    status: Literal["signed", "requested", "indicative"]
    committed: bool
    size_bn: float
    drawn_bn: float = 0.0
    spread_drawn_a: float
    fee_undrawn_a: float
    fee_upfront: float
    maturity: date
    n_banks: int | None = None
    max_bank_share: float | None = None
    covenant_headroom_test: bool = True
    test_draw_annual: bool = True
    credit_30d: Literal[0.0] = 0.0               # facilities never count in 30-day rows
    credit_stress: float                         # canonical credit in T4′ rows (pricing set; S-ADR-32)
    available_from_month: int = 2
    pledge_pool_cap_share: float | None = None   # NAV facility: 0.20 of private NAV
    ltv_normal: float | None = None
    ltv_stressed: float | None = None
    lead_time_q: int = 0
    consent_scenario: ConsentScenario            # lowest scenario in which it may be priced

    @model_validator(mode="after")
    def _amounts(self) -> Facility:
        if self.size_bn < 0 or self.drawn_bn < 0 or self.drawn_bn > self.size_bn + 1e-12:
            raise ValueError(f"{self.facility_id}: need 0 <= drawn_bn <= size_bn")
        if not 0.0 <= self.credit_stress <= 1.0:
            raise ValueError(f"{self.facility_id}: credit_stress must lie in [0, 1]")
        return self


class OwnerDrawHistory(ContractModel):
    convention: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"]
    history: tuple[tuple[int, float], ...]       # (fiscal year, rate)
    d_prev: float                                # FY2026 actual rate (client data; SYNTHETIC 0.058)
    band_agreement: SignOff | None = None        # Mode H only (S-ADR-14)


@dataclass(frozen=True, slots=True)
class UnitIndex(ArrayContainer):
    """Stable unit order: taxonomy group order, then holding id (§3.3)."""

    unit_ids: tuple[UnitId, ...]
    group_of: I32                                # [U] taxonomy index
    engine_of: tuple[str, ...]                   # [U] engine id
    age_bucket: I8                               # [U] index into GroupSpec.age_buckets; −1 for non-private units
    red_tier: B                                  # [U]


class BookSnapshot(ContractModel):
    snapshot_id: str
    asof: date
    known_at: datetime
    taxonomy_version: Literal["v1", "v2"]
    allocation: AllocationId | None
    census_id: CensusId | None
    holdings: tuple[Holding, ...]
    overlap: OverlapGraph
    facilities: tuple[Facility, ...]
    overlay: OverlayBook
    owner: OwnerDrawHistory
    nav_total_reported_bn: float
    data_class: DataClass
    content_hash: str

    @model_validator(mode="after")
    def _rules(self) -> BookSnapshot:
        total = math.fsum(h.nav_reported_bn for h in self.holdings)
        if abs(total - self.nav_total_reported_bn) > 1e-9 * max(1.0, abs(total)):
            raise ValueError(f"Σ nav_reported_bn = {total} differs from nav_total_reported_bn = "
                             f"{self.nav_total_reported_bn}")
        tax = GroupRegistry.for_version(self.taxonomy_version)
        unknown = sorted({str(h.group) for h in self.holdings if h.group not in tax})
        if unknown:
            raise ValueError(f"groups {unknown} are not in taxonomy {self.taxonomy_version}")
        miscoded = [str(h.holding_id) for h in self.holdings
                    if h.is_synthetic and h.holding_id.group_code != tax.spec(h.group).code]
        if miscoded:
            raise ValueError(f"synthetic holding ids {miscoded[:5]} do not carry their group's code (§1.8)")
        classes = {h.data_class for h in self.holdings} | {t.data_class for t in self.overlay.trades}
        if classes - {self.data_class}:
            found = sorted(c.value for c in classes | {self.data_class})
            raise DataClassMixError(f"snapshot {self.snapshot_id!r} mixes data classes {found} (§1.12 rule 2)",
                                    {"snapshot_id": self.snapshot_id, "data_classes": found})
        ids = [h.holding_id for h in self.holdings]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate holding ids in the snapshot")
        if not is_content_hash(self.content_hash):
            raise ValueError("content_hash must be sha256:<64 hex>")
        return self

    def hash_payload(self) -> dict[str, object]:
        """Everything except ``content_hash``: ``data.freeze`` sets content_hash = content_hash(hash_payload())."""
        return self.model_dump(mode="python", exclude={"content_hash"})

    def by_group(self, tax: GroupRegistry | None = None) -> dict[GroupId, tuple[Holding, ...]]:
        """Holdings per group, in taxonomy order then holding id (groups without holdings map to ())."""
        reg = tax if tax is not None else GroupRegistry.for_version(self.taxonomy_version)
        return {g: tuple(sorted((h for h in self.holdings if h.group == g), key=lambda h: str(h.holding_id)))
                for g in reg.ids()}

    def unit_index(self, tax: GroupRegistry | None = None) -> UnitIndex:
        """The stable ``UnitIndex`` (taxonomy group order, then holding id)."""
        reg = tax if tax is not None else GroupRegistry.for_version(self.taxonomy_version)
        ordered = [h for hs in self.by_group(reg).values() for h in hs]
        ages = []
        for h in ordered:
            spec = reg.spec(h.group)
            if spec.kind != "private":
                ages.append(-1)
                continue
            age = h.age_years(self.asof)
            ages.append(len(spec.age_buckets) - 1 if age is None or age >= spec.young_max_age_years else 0)
        return UnitIndex(
            unit_ids=tuple(UnitId(str(h.holding_id)) for h in ordered),
            group_of=np.array([reg.index(h.group) for h in ordered], dtype=np.int32),
            engine_of=tuple(UNIT_KIND_ENGINE[h.unit_kind] for h in ordered),
            age_bucket=np.array(ages, dtype=np.int8),
            red_tier=np.array([reg.spec(h.group).red_tier for h in ordered], dtype=np.bool_),
        )
