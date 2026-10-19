"""Frozen mini fixtures: book, world, state, contract, register, cube and FlowCube (BUILD_SPEC v1.1 §4.5; WP-03).

SYNTHETIC – NOT ADIC DATA. Sizes follow the working allocations of context §1A (v1: PE $52bn, seven groups;
v2: PE $34bn and Real Assets $18bn, eight groups; $177bn in total) but every number is illustrative [I].

- ``mini_book(allocation, seed=...)``: one unit per private group × age bucket, 3 HF lots, 2 long-only sleeves,
  3 treasury sleeves and a small overlay policy book (5 trades, 2 CSAs, 1 service) with its three buckets.
- ``mini_cube(n_paths, world, seed=...)``: 120 months of a two-regime (calm/crisis) Gaussian factor model on the
  increment-1 factor names and kinds (§4.10, S-ADR-35), with the stress posterior from ``fakes.fake_filter``.
  Not ``scen``: no CMA anchoring. Uniforms come from numpy's Philox (raw outputs, a stable stream) through the
  normal inverse CDF, laid out path-major, so the first n paths of a larger cube equal a smaller cube.
- ``mini_flowcube(book, cube)``: HOLD flows of every engine unit by quarter (``fakes.simulate_hold``).

Their checksums are frozen in ``tests/golden/frozen_fixtures.json`` (§4.5 DoD, §10.4).
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping
from datetime import date, datetime, timezone
from typing import Any, Final

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.book import (
    AssetDebt, BookSnapshot, ClaimEdge, ClaimTerms, CompanyNode, CompanyTerms, DevelopmentPlan, Facility, Holding,
    HFTerms, LoanCohortTerms, LongOnlyTerms, OverlapGraph, OwnerDrawHistory, PrivateFundTerms, RealAssetTerms,
    SponsorNode, TreasuryTerms,
)
from adic_tpa.contracts.contract import (
    RACI, ActionSpace, AnalysisContract, BudgetSpec, FloorSpec, FrozenQuestion, GateSpec, LLMSpec, ObjectiveSpec,
    PlaneSpec, RiskBudget, RoleLLMSpec, SignOff, Tier1Spec,
)
from adic_tpa.contracts.engine_io import FlowCube, FlowCubeMeta
from adic_tpa.contracts.enums import (
    AllocationId, Book, ConsentScenario, ContractMode, CreditState, DataClass, ExitWindow, FactorKind, LLMMode, MacroRegime,
    ModelFamily, Plane, ReturnBasis, RoleId, RunMode, ShockType, Tier, WorldId,
)
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import (
    CompanyId, ContractId, CsaId, FacilityId, GroupId, HoldingId, MetricId, SponsorId, TradeId,
)
from adic_tpa.contracts.ledger import CanonicalConventions, ConventionSets, RAStressConvention
from adic_tpa.contracts.overlay import CSA, OverlayBook, OverlayPolicy, OverlayTrade, ServiceContract
from adic_tpa.contracts.policy import PolicyRef
from adic_tpa.contracts.room import DecisionType, DecisionVariable, EvidenceSpec, Register, SignpostRule
from adic_tpa.contracts.signing import DEV_TEST_KEY_REF, DEV_TEST_SIGNER_HASH, sign, signoff_payload
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.world import (
    BootstrapParams, CMALine, CubeMeta, OilParams, OilState, OwnerConfig, ScenarioCube, StateSnapshot, VolParams,
    WorldSpec, validate_world_id,
)
from adic_tpa.testing.fakes import MINI_ASSET_CLASSES, book_hold_flows, fake_beliefs, fake_filter, fake_filter_params

__all__ = [
    "MINI_ASOF", "MINI_KNOWN_AT", "MINI_FACTORS", "MINI_FACTOR_KINDS", "MINI_W0_BN", "mini_book", "mini_world",
    "mini_state0", "mini_owner_config", "mini_signoff", "mini_register", "mini_contract", "mini_cube",
    "mini_flowcube", "ALLOCATIONS",
]

MINI_ASOF: Final = date(2026, 9, 30)                                   # §1.3 census instant (S-ADR-26)
MINI_KNOWN_AT: Final = datetime(2026, 10, 18, tzinfo=timezone.utc)      # R0 snapshot date
MINI_W0_BN: Final = 177.0
# Increment-1 factor subset and kinds (§4.10, S-ADR-35, S-ADR-37).
MINI_FACTORS: Final[tuple[str, ...]] = (
    "us_eq", "short_rate", "ust10y", "hy_spread", "ebp", "log_rv", "brent_log", "exit_X")
MINI_FACTOR_KINDS: Final[tuple[FactorKind, ...]] = (
    FactorKind.LOGRET, FactorKind.LEVEL, FactorKind.LEVEL, FactorKind.LEVEL, FactorKind.LEVEL, FactorKind.LEVEL,
    FactorKind.LOGRET, FactorKind.LEVEL)

# Working allocations (context §1A), USD bn; the testing package may name groups (the group-id lint exempts it).
ALLOCATIONS: Final[Mapping[str, Mapping[str, float]]] = {
    "v1": {"PE": 52.0, "SECONDARIES": 14.0, "CAPSOL": 8.0, "COINVEST": 18.0, "PRIVCREDIT": 14.0},
    "v2": {"PE": 34.0, "SECONDARIES": 14.0, "CAPSOL": 8.0, "COINVEST": 18.0, "PRIVCREDIT": 14.0, "REALASSETS": 18.0},
}
_CENSUS: Final = {"v1": "v1.0", "v2": "v1.1"}           # research fixtures run v1 + census v1.0; v1.1 is the user's choice
_UNFUNDED: Final = {"v1": {"PE": (20.0, 7.4), "SECONDARIES": (1.8, 0.6), "CAPSOL": (0.9, 0.3), "PRIVCREDIT": (1.9, 0.6)},
                    "v2": {"PE": (12.0, 4.4), "SECONDARIES": (1.8, 0.6), "CAPSOL": (0.9, 0.3), "PRIVCREDIT": (1.9, 0.6),
                           "REALASSETS": (3.0, 1.0)}}
_AGES: Final = (2.0, 7.0)                                 # young (< 4 years) and mature buckets
_HF_LOTS: Final = (8.0, 7.0, 5.0)
_LONG_ONLY: Final = (("DM_EQ", 28.0), ("FI", 8.0))
_TREASURY: Final = (("CASH", 5.70), ("UST", 4.0), ("IG", 5.0))   # $15bn less the overlay buckets' $0.30bn
_OVERLAY: Final = (("tail", 0.25), ("opportunistic", 0.05), ("synthetic_beta", 0.0))
_SPONSORS: Final = (SponsorId("SYN-GP-0001"), SponsorId("SYN-GP-0002"))
_COMPANIES: Final = (CompanyId("SYN-CMP-000001"), CompanyId("SYN-CMP-000002"), CompanyId("SYN-CMP-000003"))


def _rng(*parts: object) -> np.random.Generator:
    """A Philox generator keyed by SHA-256 of ``parts`` (stable raw stream; used for small fixture jitter)."""
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).digest()
    return np.random.Generator(np.random.Philox(key=np.frombuffer(digest[:16], dtype=np.uint64).copy()))


def _private_terms(secondary: bool, kind: str, nav: float, unfunded: float, age: float, young: bool) -> Any:
    """Terms of one private unit; ``secondary`` marks a fund+company group (Secondaries' capability signature)."""
    if kind == "fund":
        sec = secondary
        return PrivateFundTerms(strategy_class="secondary_fund" if sec else ("buyout_mid" if young else "buyout_large"),
                                age_years=age, effective_age_years=age, fee_rate_a=0.015, carry=0.20, hurdle_a=0.08,
                                lpa_term_years=10.0, extensions_used=0 if young else 1, subscription_line_bn=0.0,
                                gp_navloan_bn=0.0, recallable_bn=0.0, sec_template="S1" if sec else None,
                                theta_true_over_ref=1.0 if sec else None)
    if kind == "company":
        return CompanyTerms(ownership=0.08, ev_bn=nav / 0.08 * 1.6, net_debt_bn=nav / 0.08 * 0.6,
                            ebitda_bn=nav / 0.08 * 1.6 / 12.0, entry_ev_ebitda=12.0, icr=3.0, software_flag=young,
                            spv_debt_bn=0.0, beta_asset=1.2, sigma_id_a=0.25, exit_route="sponsor_sale")
    if kind == "claim":
        return ClaimTerms(family="A" if young else "C", claim_bn=nav, coupon_a=0.11, pik_share_cap=0.5, pik_window_q=8,
                          step_up_a=0.01, make_whole=0.0, moic_floor=1.3, warrants=None, seniority=1, ltv=0.45,
                          icr=2.2, negative_ebitda=False, status=CreditState.PERFORMING, syndication_share=0.0)
    if kind == "loan_cohort":
        return LoanCohortTerms(segment="DL" if young else "ABF", vehicle_id=f"SYN-PC-VEH-{1 if young else 2:02d}",
                               wrapper="SMA" if young else "EVERGREEN", n_loans=40, par_bn=nav, spread_a=0.055,
                               floor_a=0.01, oid=0.02, wam_years=3.5, undrawn_bn=unfunded, sponsored_share=0.8,
                               software_share=0.15,
                               state_shares={CreditState.PERFORMING: 0.95, CreditState.PIK: 0.05},
                               collateral_type="senior_secured", evergreen_cap_q=None if young else 0.05)
    if kind == "ra_asset":
        return RealAssetTerms(
            sector="REAL_ESTATE" if young else "INFRASTRUCTURE", access="DIRECT", noi_bn=0.05 * nav, cap_rate=0.05,
            inflation_passthrough=0.6, oil_beta=0.1, capex_reserve_rate_a=0.02,
            development=DevelopmentPlan(committed_bn=unfunded, s_curve_quarters=8) if unfunded > 0 else None,
            debt=AssetDebt(balance_bn=0.3 * nav, rate_type="FLOATING", spread_a=0.02, hedge_ratio=0.5,
                           maturity=date(2030, 6, 30), ltv_max=0.65, dscr_covenant=1.3, amort_q=0.005),
            open_end=None, appraisal_lambda=0.5, report_lag_q=1)
    raise SchemaError(f"mini_book: no terms for private unit kind {kind!r}")


_ENGINE_KIND: Final = {"fund": "fund", "company": "company", "claims": "claim", "credit": "loan_cohort",
                       "realassets": "ra_asset"}


def mini_book(allocation: AllocationId = "v2", *, seed: int = 7) -> BookSnapshot:
    """The mini book (§4.5): one unit per private group × age bucket, 3 HF lots, 2 long-only, 3 treasury sleeves
    and a small overlay policy book; $177bn, SYNTHETIC. ``seed`` jitters the young/mature NAV split only."""
    if allocation not in ALLOCATIONS:
        raise SchemaError(f"mini_book: unknown allocation {allocation!r}")
    tax = GroupRegistry.for_version("v2" if allocation == "v2" else "v1")
    rng = _rng("mini_book", allocation, seed)
    holdings: list[Holding] = []

    def add(group: str, n: int, **kw: object) -> Holding:
        code = tax.spec(group).code
        h = Holding(holding_id=HoldingId(f"SYN-{code}-{n:04d}"), group=GroupId(group), is_synthetic=True,
                    data_class=DataClass.SYNTHETIC, source=f"testing.mini_book/{allocation}/s{seed}", **kw)
        holdings.append(h)
        return h

    sizes = ALLOCATIONS[allocation]
    for g in tax.private():
        spec = tax.spec(g)
        kind = _ENGINE_KIND[spec.engines[0]]
        total = sizes[str(g)]
        share = round(0.35 + 0.10 * float(rng.random()), 4)
        navs = (round(total * share, 4), total - round(total * share, 4))
        unf = _UNFUNDED[allocation].get(str(g), (0.0, 0.0)) if spec.has_unfunded else (0.0, 0.0)
        strategies = tax.strategies(g) or ("default",)
        secondary = spec.engines == ("fund", "company")
        for b, (age, nav, u) in enumerate(zip(_AGES, navs, unf, strict=True)):
            young = b == 0
            companies = ((_COMPANIES[b],) if kind in ("company", "claim") else ())
            add(str(g), b + 1, strategy=strategies[min(b, len(strategies) - 1)], unit_kind=kind,
                gp_id=_SPONSORS[b] if kind == "fund" else None, company_ids=companies,
                vintage=MINI_ASOF.year - int(age), region="US" if young else "GLOBAL",
                commitment_bn=(nav + u) if u > 0 else None, unfunded_bn=u, nav_reported_bn=nav,
                nav_reference_date=date(2026, 6, 30), wrapper={"fund": "CLOSED_END", "company": "DIRECT",
                                                               "claim": "DIRECT", "loan_cohort": "SMA",
                                                               "ra_asset": "DIRECT"}[kind],
                encumbered_bn=0.0, terms=_private_terms(secondary, kind, nav, u, age, young))
    public = tax.ids("public")[0]
    for n, nav in enumerate(_HF_LOTS, start=1):
        add(str(public), n, strategy="hedge_funds", unit_kind="hf_lot", region="GLOBAL", nav_reported_bn=nav,
            nav_reference_date=date(2026, 8, 31), wrapper="COMMINGLED",
            terms=HFTerms(strategy=("macro", "equity_ls", "credit")[n - 1], dealing="quarterly", notice_days=65,
                          lockup_end=None, soft_lock_fee=0.0, gate_type="investor", gate_level=0.25, holdback=0.05,
                          payment_lag_days=30, side_pocket_cap=0.10, suspension_allowed=True, transfer_consent=True,
                          pledge_consent=True, beta_eq_normal=0.35, beta_eq_crisis=0.55, alpha_net_a=0.02,
                          alpha_sd_a=0.03, crisis_gate_hazard_q=0.05, leverage_navw=1.5, smoothing_theta=0.1,
                          adic_share_of_fund=0.05))
    for n, (sleeve, nav) in enumerate(_LONG_ONLY, start=len(_HF_LOTS) + 1):
        add(str(public), n, strategy="long_only_dm_equity" if sleeve == "DM_EQ" else "long_only_fixed_income",
            unit_kind="longonly", region="GLOBAL", nav_reported_bn=nav, nav_reference_date=MINI_ASOF, wrapper="SMA",
            terms=LongOnlyTerms(sleeve=sleeve, benchmark="MSCI World" if sleeve == "DM_EQ" else "Bloomberg US Agg",
                                beta=1.0, te_a=0.02, ir_prior=0.2, adv_bn=50.0, vehicle="SMA", tax_rate=0.0,
                                credit_beta=0.0 if sleeve == "DM_EQ" else 0.3))
    funding = tax.ids("funding")[0]
    for n, (sleeve, nav) in enumerate(_TREASURY, start=1):
        add(str(funding), n, strategy=sleeve.lower(), unit_kind="treasury", region="US", nav_reported_bn=nav,
            nav_reference_date=MINI_ASOF, wrapper="TREASURY",
            terms=TreasuryTerms(sleeve=sleeve, haircut={"CASH": 0.0, "UST": 0.02, "IG": 0.10}[sleeve],
                                hqla_level="L2A" if sleeve == "IG" else "L1", cf_controlled=True,
                                duration_years={"CASH": 0.1, "UST": 4.0, "IG": 5.0}[sleeve]))
    overlay_group = tax.ids("overlay")[0]
    for n, (strategy, nav) in enumerate(_OVERLAY, start=1):
        add(str(overlay_group), n, strategy=strategy, unit_kind="overlay_bucket", region="GLOBAL", nav_reported_bn=nav,
            nav_reference_date=MINI_ASOF, terms=None)
    return _snapshot(tax, allocation, seed, tuple(holdings))


def _overlay_book(public: str) -> OverlayBook:
    csa = (CSA(csa_id=CsaId("SYN-CSA-01"), dealer_id="SYN-DEALER-A", threshold_bn=0.0, mta_bn=0.005, ia_bn=0.0,
               eligible_collateral=("cash", "ust"), reuse_right=True, im_regime="two_way_simm", phi_recognition=1.0),
           CSA(csa_id=CsaId("SYN-CSA-02"), dealer_id="SYN-DEALER-B", threshold_bn=0.0, mta_bn=0.005, ia_bn=0.0,
               eligible_collateral=("cash",), reuse_right=False, im_regime="two_way_simm", phi_recognition=0.7))
    trades = tuple(
        OverlayTrade(trade_id=TradeId(f"SYN-TR-{i:05d}"), book=Book(book), template=template, underlying=underlying,
                     strike_rel=k1, strike2_rel=k2, expiry=expiry, notional_bn=notional, premium_bn=premium,
                     venue=venue, csa_id=None if venue == "listed" else CsaId(csa_id), rung=rung,
                     is_synthetic=True, data_class=DataClass.SYNTHETIC)
        for i, (book, template, underlying, k1, k2, expiry, notional, premium, venue, csa_id, rung) in enumerate((
            ("TAIL", "put_spread_90_72", "SPX", 0.90, 0.72, date(2026, 12, 31), 7.5, 0.020, "bilateral", "SYN-CSA-01", "3M"),
            ("TAIL", "put_spread_90_72", "SPX", 0.90, 0.72, date(2027, 3, 31), 15.0, 0.060, "bilateral", "SYN-CSA-01", "6M"),
            ("TAIL", "put_spread_90_72", "SPX", 0.90, 0.72, date(2027, 9, 30), 7.5, 0.045, "bilateral", "SYN-CSA-02", "12M"),
            ("OPP", "short_strangle_1m", "SPX", 0.95, 1.05, date(2026, 10, 30), 2.0, 0.010, "bilateral", "SYN-CSA-02", None),
            ("BETA", "equity_index_future", "ES", None, None, date(2026, 12, 18), 10.0, 0.0, "listed", "", None),
        ), start=1))
    service = ServiceContract(service_id="SYN-SVC-01", client_group=GroupId(public), kind="completion_beta",
                              notional_bn=10.0, reference_index="MSCI World", s_lock_a=0.002, clc_basis_bn=0.0)
    return OverlayBook(trades=trades, csas=csa, services=(service,), policy=OverlayPolicy())


def _snapshot(tax: GroupRegistry, allocation: str, seed: int, holdings: tuple[Holding, ...]) -> BookSnapshot:
    overlap = OverlapGraph(
        sponsors=(SponsorNode(sponsor_id=_SPONSORS[0], tier="elite"), SponsorNode(sponsor_id=_SPONSORS[1], tier="core")),
        companies=(CompanyNode(company_id=_COMPANIES[0], sponsor_id=_SPONSORS[0], sector="software", ev_bn=5.0,
                               net_debt_bn=2.5, ebitda_bn=0.40, icr=2.5, software_flag=True),
                   CompanyNode(company_id=_COMPANIES[1], sponsor_id=_SPONSORS[1], sector="healthcare", ev_bn=3.0,
                               net_debt_bn=1.2, ebitda_bn=0.25, icr=3.2, software_flag=False),
                   CompanyNode(company_id=_COMPANIES[2], sponsor_id=None, sector="industrials", ev_bn=2.0,
                               net_debt_bn=0.8, ebitda_bn=0.20, icr=3.8, software_flag=False)),
        edges=tuple(
            ClaimEdge(holder_id=h.holding_id, company_id=h.company_ids[0], share=0.08 if h.unit_kind == "company" else 0.05,
                      seniority=0 if h.unit_kind == "company" else 1,
                      claim_kind="coinvest_equity" if h.unit_kind == "company" else "cs_claim")
            for h in holdings if h.company_ids) + tuple(
            ClaimEdge(holder_id=h.holding_id, company_id=_COMPANIES[0], share=0.02, seniority=0,
                      claim_kind="pe_lookthrough")
            for h in holdings if h.unit_kind == "fund" and h.gp_id == _SPONSORS[0]))
    facilities = (
        Facility(facility_id=FacilityId("SYN-FAC-01"), kind="revolver", status="signed", committed=True, size_bn=15.0,
                 spread_drawn_a=0.0085, fee_undrawn_a=0.0015, fee_upfront=0.0015, maturity=date(2029, 9, 30),
                 n_banks=8, max_bank_share=0.2, credit_stress=0.5, consent_scenario=ConsentScenario.R1),
        Facility(facility_id=FacilityId("SYN-FAC-02"), kind="nav_facility", status="requested", committed=False,
                 size_bn=5.0, spread_drawn_a=0.03, fee_undrawn_a=0.005, fee_upfront=0.01, maturity=date(2029, 12, 31),
                 credit_stress=0.05, pledge_pool_cap_share=0.20, ltv_normal=0.10, ltv_stressed=0.05, lead_time_q=2,
                 consent_scenario=ConsentScenario.R1))
    owner = OwnerDrawHistory(convention="opening_fy_reported_nav", history=((2024, 0.060), (2025, 0.055), (2026, 0.058)),
                             d_prev=0.058)
    public = tax.ids("public")[0]
    book = BookSnapshot(
        snapshot_id=f"SYN-MINI-{allocation}-s{seed}", asof=MINI_ASOF, known_at=MINI_KNOWN_AT,
        taxonomy_version="v2" if allocation == "v2" else "v1", allocation=allocation,  # type: ignore[arg-type]
        census_id=_CENSUS[allocation], holdings=holdings, overlap=overlap,  # type: ignore[arg-type]
        facilities=facilities, overlay=_overlay_book(str(public)), owner=owner,
        nav_total_reported_bn=math.fsum(h.nav_reported_bn for h in holdings), data_class=DataClass.SYNTHETIC,
        content_hash="sha256:" + "0" * 64)
    return book.model_copy(update={"content_hash": content_hash(book.hash_payload())})


# ------------------------------------------------------------------------------------------------ mini world
# (arith_mean_a, vol_a, correlation with us_equity) per asset class; M6 lowers risky means and raises vols [I].
_CMA: Final[Mapping[str, tuple[float, float, float]]] = {
    "us_equity": (0.075, 0.16, 1.0), "global_equity": (0.078, 0.16, 0.9), "em_equity": (0.085, 0.21, 0.75),
    "us_treasury": (0.042, 0.06, -0.2), "ig_credit": (0.050, 0.07, 0.3), "hy_credit": (0.065, 0.10, 0.6),
    "pe_buyout": (0.095, 0.22, 0.7), "venture": (0.110, 0.30, 0.6), "private_credit": (0.080, 0.10, 0.4),
    "real_estate": (0.070, 0.15, 0.5), "infrastructure": (0.075, 0.13, 0.4), "hedge_funds": (0.060, 0.08, 0.5),
    "cash": (0.039, 0.01, 0.0)}


def _cma(world_id: str) -> dict[str, tuple[float, float, float]]:
    stressed = world_id == "M6" or world_id.startswith("MS:")
    out = {}
    for name, (mu, vol, rho) in _CMA.items():
        risky = rho > 0.25
        out[name] = (mu - (0.02 if stressed and risky else 0.0), vol * (1.2 if stressed and risky else 1.0), rho)
    return out


def mini_world(world_id: WorldId = "M1") -> WorldSpec:
    """A ``WorldSpec`` for the mini cube: CMA lines on ``MINI_ASSET_CLASSES`` (M6 and misspecification worlds are
    stressed), oil and vol parameters [I]; B1/B2 carry bootstrap parameters. ``regime`` and ``factors`` stay None
    (the mini cube is not engine E)."""
    wid = validate_world_id(world_id)
    family = "B1" if wid == "B1" else "B2" if wid == "B2" else "E"
    t6 = "M1_M5" if wid in ("M1", "M2", "M3", "M4", "M5", "B1", "B2") else "M6"
    cma = {name: CMALine(asset_class=name, arith_mean_a=mu, vol_a=vol, basis=ReturnBasis(kind="arith", fees="net"),
                         benchmark=name, fee_adjusted=True, selection_included=False)
           for name, (mu, vol, _rho) in _cma(wid).items()}
    bootstrap = (BootstrapParams(panel_start=date(1990, 1, 31), panel_end=date(2015, 12, 31),
                                 method="stationary_block" if family == "B1" else "fhs",
                                 observed_factors=("us_eq", "short_rate", "log_rv", "ust10y", "ebp"))
                 if family != "E" else None)
    body = dict(world_id=wid, family=family, provider="testing.mini_world", cma_asof=MINI_ASOF, cma=cma, regime=None,
                factors=None, oil=OilParams(kappa={"short": 0.9, "long": 0.2}, vol={"short": 0.35, "long": 0.20},
                                            rho_eq={"calm": 0.2, "crisis": 0.5}, gw_jump={"mean": -0.2, "sd": 0.1}),
                vol=VolParams(move={"base": 100.0, "slope": 0.5}, ovx={"base": 35.0, "slope": 0.6}),
                bootstrap=bootstrap, t6_class=t6)
    return WorldSpec(**body, content_hash=content_hash(body))  # type: ignore[arg-type]


def mini_state0() -> StateSnapshot:
    """The frozen as-of state of the mini fixtures (gap_04 shapes; values [I], e0[D] = 0.87 as in §4.9)."""
    levels = {"short_rate": 0.0389, "ust10y": 0.042, "hy_spread": 0.032, "ebp": 0.002, "log_rv": math.log(0.15),
              "exit_X": 0.0}
    body = dict(asof=MINI_ASOF, data_timestamps={"panel": datetime(2026, 8, 31, tzinfo=timezone.utc)},
                pi0_macro=(0.55, 0.25, 0.10, 0.10), pi0_range=((0.45, 0.65), (0.15, 0.35), (0.05, 0.15), (0.05, 0.15)),
                stress_post=(0.70, 0.20, 0.10), F_t=0.10, F_base_rate=0.17, F_ab=(-2.0, 1.2),
                e0=(0.03, 0.05, 0.87, 0.05), z0=(0.15, 0.0, 0.15, 0.0, 0.0, 0.70), z_disagreement=False,
                oil=OilState(spot=66.0, front=67.0, chi0=math.log(66.0 / 67.0), xi0=0.0), gw_elapsed_months=14,
                draw_12m_bn=(9.9, 10.8), draw_p90_bn=11.2, d_prev=0.058, factor_levels0=levels,
                filter_version_hash=fake_filter_params().version_hash)
    return StateSnapshot(**body, content_hash=content_hash(body))  # type: ignore[arg-type]


def mini_owner_config() -> OwnerConfig:
    """``OwnerConfig`` with the §4.8 tables (override and band-acceptance probabilities by shock type)."""
    override = {ShockType.N: 0.0025, ShockType.B: 0.0025, ShockType.SG: 0.01, ShockType.DB: 0.01,
                ShockType.SS: 0.0025, ShockType.GW: 0.02}
    accept = {z: (0.30 if z is ShockType.DB else 1.0) for z in ShockType}
    return OwnerConfig(override_p_a=override, fiscal_noise_sd_pp=2.0, ref_price=70.0, p_accept_band=accept)


def mini_signoff(object_hash: str, role: str = "CIO", signed_at: datetime | None = None) -> SignOff:
    """A DEV/SYNTHETIC sign-off by the fixed test signer (refused in REAL mode; S-ADR-37, S-ADR-40)."""
    at = signed_at if signed_at is not None else MINI_KNOWN_AT
    payload = signoff_payload(object_hash, role, DEV_TEST_SIGNER_HASH, at)
    return SignOff(role=role, signer_hash=DEV_TEST_SIGNER_HASH, signed_at=at, object_hash=object_hash,  # type: ignore[arg-type]
                   method="dev_test_key", signature=sign(payload, DEV_TEST_KEY_REF, run_mode=RunMode.DEV_SYNTHETIC))


def mini_register() -> Register:
    """A two-entry Register (Q1 Phase-I status, Q2 survival) signed by the DEV test signer (SYNTHETIC)."""
    entries = (
        DecisionType(id="Q1", title="Phase-I status and recovery mode", proposer="TREASURER", decider="IC", tier=Tier.A,
                     cadence="quarterly", deadline_rule="G0", variables=(DecisionVariable(name="mode", unit="enum"),),
                     evidence=(EvidenceSpec(metric=MetricId("phase1.u_star_bn@v1")),), signposts=SignpostRule(),
                     increment="1"),
        DecisionType(id="Q2", title="Liquidity survival under T4' and reverse stresses", proposer="CRO",
                     decider="IC", tier=Tier.A, cadence="quarterly", deadline_rule="G1",
                     variables=(DecisionVariable(name="facility_bn", unit="usd_bn", bounds=(0.0, 30.0)),),
                     evidence=(EvidenceSpec(metric=MetricId("liquidity.t4p.survival_months@v1")),
                               EvidenceSpec(metric=MetricId("tier1.t6.cp_upper@v1"))),
                     signposts=SignpostRule(), increment="1"))
    body = {"version": "mini-1", "entries": entries}
    h = content_hash(body)
    return Register(version="mini-1", entries=entries, signoffs=(mini_signoff(h, "SECRETARY"),), hash=h)


def mini_contract(*, run_mode: RunMode = RunMode.DEV_SYNTHETIC, quarter: str = "2026Q4") -> AnalysisContract:
    """A NORMAL-mode DECISION contract on allocation v2 in DEV_SYNTHETIC mode (signed by the DEV test signer)."""
    tax = GroupRegistry.for_version("v2")
    split = {g: tax.spec(g).commitment_split for g in tax.ids() if tax.spec(g).commitment_split > 0}
    credit = {g: (0.10 if tax.spec(g).engines[0] == "credit" else 0.07)
              for g in tax.ids() if tax.spec(g).engines and tax.spec(g).engines[0] in ("credit", "claims")}
    ra = RAStressConvention(noi_yield_mult=0.85, refi_spread_stress_a=0.03, refi_ltv_cap=0.55)
    pricing = CanonicalConventions(credit_cash_a=credit, commitment_split=split, real_assets=ra)
    research = pricing.model_copy(update={"revolver_credit": 0.80, "pacing_credit_lag_q": 0})
    bands = {"M1_M5": (0.005, 0.01, 0.02), "MIX": (0.005, 0.01, 0.02), "M6": (None, 0.025, 0.05)}
    tier1 = Tier1Spec(t6_bands=bands, theta_star=0.58, theta_star_overlay=0.76,
                      conventions=ConventionSets(pricing=pricing, research=research),
                      t5={"recourse_debt_target": 0.10, "recourse_debt_hard": 0.15, "exposure": 1.30,
                          "encumbrance_target": 0.15, "encumbrance_hard": 0.20, "pledge": 0.20, "maturity_12m": 0.20,
                          "lr8": 0.80, "gross_overlay": 0.30})
    roles = (RoleLLMSpec(role=RoleId.MEMO_WRITER, family=ModelFamily.A, model="claude-opus-5-5", effort="high",
                         prompt_hash=content_hash("memo_writer.md"), tools=("get_metric",),
                         data_classes_allowed=(DataClass.SYNTHETIC,), materiality="high", blocking_escalation=False),)
    body: dict[str, Any] = dict(
        contract_id=ContractId(f"ctr-{quarter}-v1"), version=1, quarter=quarter, data_class=DataClass.SYNTHETIC,
        census_id="v1.1", census_side_by_side="v1.1r", mode=ContractMode.NORMAL, recovery=None,
        pricing_scenario=ConsentScenario.R0, frozen_questions=(
            FrozenQuestion(qid="FQ1", item_id="Q2", text="Does T4' survival on T+P reach 24 months?",
                           resolves_by=date(2027, 9, 30), metric_id=MetricId("liquidity.t4p.survival_months@v1")),),
        objective=ObjectiveSpec(target_anchor_date=MINI_ASOF, target_anchor_wealth_bn=MINI_W0_BN,
                                model_weights={"M1": 0.5, "M6": 0.5}),
        tier1=tier1, floor=FloorSpec(),
        actions=ActionSpace(lenses_by_group={g: tax.spec(g).lenses for g in tax.investment()},
                            instrument_whitelist=("lp_secondary_sale", "nav_loan", "pace_cut"),
                            idea_kinds=("policy_residual", "action_package", "overlay_structure")),
        anchor=PolicyRef(kind="native", name="P0", params_hash=content_hash("p0-theta")),
        controls=(PolicyRef(kind="native", name="HOLD", params_hash=content_hash({})),),
        planes=PlaneSpec(search_worlds=("M1", "M6", "B1"), final_worlds=("M1", "M6"), misspec=(),
                         seal_commitment=content_hash("seal"),
                         windows={"calibration": (date(1990, 1, 31), date(2026, 8, 31))}),
        gates=GateSpec(eps_mat_bp={"overlay": 3.0, "pacing": 5.0, "refi_lever": 10.0, "sell": 15.0, "other": 10.0},
                       mde_max_bp=10.0, ni_worlds_search=("M1", "M6", "B1"), ni_worlds_final=("M1", "M6"),
                       ni_comparator="HOLD", miss_fd_cost_ratio=1.0),
        budgets=BudgetSpec(), operating_points=(RiskBudget(name="tolerance", t6_eps=0.01, floor=0.07,
                                                           tail_budget_a=0.0015, leverage_max=1.3),),
        llm_policy=LLMSpec(mode=LLMMode.OFFLINE, provider="anthropic", roles=roles),
        raci=RACI(owners={"contract": "CRO"}), root_seed=20261018, run_mode=run_mode,
        engine_hash=content_hash("engine"), config_hash=content_hash("config"),
        snapshot_hash=mini_book("v2").content_hash, scenario_hashes={}, taxonomy_hash=tax.hash)
    cid = content_hash(body)              # the sign-offs bind every other contract field
    return AnalysisContract(**body, signoffs=(mini_signoff(cid, "CIO"), mini_signoff(cid, "CRO")))


# ------------------------------------------------------------------------------------------------- mini cube
_N_STREAM: Final = 1 + len(MINI_FACTORS) + (len(MINI_ASSET_CLASSES) - 1)     # regime, factor shocks, asset shocks
# Two regimes (calm, crisis): monthly transition matrices [I]; M6 and misspecification worlds are crisis-prone.
_P_REGIME: Final = {False: np.array([[0.98, 0.02], [0.08, 0.92]]), True: np.array([[0.96, 0.04], [0.05, 0.95]])}
_P_CRISIS0: Final = 0.10
# Per factor: (calm mean, crisis mean, calm sd, crisis sd, mean reversion κ (level kinds), start level).
_FACTOR_PARAMS: Final[Mapping[str, tuple[float, float, float, float, float, float]]] = {
    "us_eq": (0.0075, -0.025, 0.040, 0.075, 0.0, 0.0),
    "short_rate": (0.035, 0.015, 0.0010, 0.0015, 0.05, 0.0389),
    "ust10y": (0.042, 0.030, 0.0015, 0.0025, 0.03, 0.042),
    "hy_spread": (0.035, 0.080, 0.0020, 0.0060, 0.15, 0.032),
    "ebp": (0.000, 0.018, 0.0010, 0.0030, 0.20, 0.002),
    "log_rv": (-1.95, -1.00, 0.10, 0.15, 0.30, math.log(0.15)),
    "brent_log": (0.0, -0.02, 0.08, 0.12, 0.0, 0.0),
    "exit_X": (0.3, -1.0, 0.10, 0.15, 0.15, 0.0),
}


def _uniform_stream(world: str, seed: int, n_paths: int, months: int) -> F64:
    digest = hashlib.sha256(f"testing.mini_cube|{world}|{seed}".encode("utf-8")).digest()
    key = np.frombuffer(digest[:16], dtype=np.uint64).copy()
    raw = np.random.Philox(key=key).random_raw(n_paths * months * _N_STREAM)
    # (x >> 11 + 0.5) · 2^-53 lies in the open interval (0, 1), so the normal inverse CDF stays finite
    return (((raw >> np.uint64(11)).astype(np.float64) + 0.5) * 2.0 ** -53).reshape(n_paths, months, _N_STREAM)


def mini_cube(n_paths: int = 200, world: WorldId = "M1", *, seed: int = 7) -> ScenarioCube:
    """A 120-month SYNTHETIC ``ScenarioCube`` (§4.5): two-regime Gaussian factors with real factor names and kinds,
    asset returns on ``MINI_ASSET_CLASSES`` from ``mini_world(world)``'s CMA lines, the stress posterior of
    ``fakes.fake_filter`` and derived vol, financing-window and crowding series. Not ``scen``."""
    from scipy.special import ndtri  # lazy: keeps importing adic_tpa.testing light

    wid = validate_world_id(world)
    if not 1 <= n_paths <= 2000:
        raise SchemaError("mini_cube: n_paths must lie in [1, 2000] (one block, §1.5)")
    months = 120
    stressed = wid == "M6" or wid.startswith("MS:")
    u = _uniform_stream(wid, seed, n_paths, months)
    z = ndtri(u[:, :, 1:])
    trans = _P_REGIME[stressed]
    crisis = np.zeros((n_paths, months), dtype=bool)
    state = u[:, 0, 0] < _P_CRISIS0
    for m in range(months):
        if m > 0:
            p_crisis = np.where(state, trans[1, 1], trans[0, 1])
            state = u[:, m, 0] < p_crisis
        crisis[:, m] = state
    k = len(MINI_FACTORS)
    factors = np.empty((n_paths, months, k))
    for j, name in enumerate(MINI_FACTORS):
        mu_c, mu_x, sd_c, sd_x, kappa, start = _FACTOR_PARAMS[name]
        mean = np.where(crisis, mu_x, mu_c)
        sd = np.where(crisis, sd_x, sd_c)
        if MINI_FACTOR_KINDS[j] is FactorKind.LOGRET:
            factors[:, :, j] = mean + sd * z[:, :, j]
            continue
        level = np.full(n_paths, start)
        for m in range(months):
            level = level + kappa * (mean[:, m] - level) + sd[:, m] * z[:, m, j]
            factors[:, m, j] = level
    factors[:, :, MINI_FACTORS.index("hy_spread")] = np.maximum(factors[:, :, MINI_FACTORS.index("hy_spread")], 0.005)
    cma = _cma(wid)
    eq_z = z[:, :, MINI_FACTORS.index("us_eq")]
    assets = np.empty((n_paths, months, len(MINI_ASSET_CLASSES)))
    idio = 0
    for a, name in enumerate(MINI_ASSET_CLASSES):
        if name == "us_equity":
            assets[:, :, a] = factors[:, :, 0]
            continue
        mu_a, vol_a, rho = cma[name]
        sd_m = vol_a / math.sqrt(12.0)
        mu_m = (math.log1p(mu_a) - 0.5 * vol_a ** 2) / 12.0
        shock = rho * eq_z + math.sqrt(max(1.0 - rho * rho, 0.0)) * z[:, :, k + idio]
        risky = rho > 0.25
        assets[:, :, a] = np.where(crisis & risky, mu_m - 0.015, mu_m) + np.where(crisis & risky, 1.6, 1.0) * sd_m * shock
        idio += 1
    f32 = factors.astype(np.float32)
    simulate_filter = fake_filter()
    stress_post = simulate_filter(f32, MINI_FACTORS, fake_filter_params(), np.array([0.002, 0.042]))
    log_rv = factors[:, :, MINI_FACTORS.index("log_rv")]
    vol = np.stack([log_rv + 0.15, math.log(100.0) + 0.6 * (log_rv + 1.9), math.log(35.0) + 0.5 * (log_rv + 1.9)],
                   axis=2)
    hy = factors[:, :, MINI_FACTORS.index("hy_spread")]
    ebp = factors[:, :, MINI_FACTORS.index("ebp")]
    fin_window = np.where((hy > 0.09) | (ebp > 0.025), 2, np.where((hy > 0.055) | (ebp > 0.01), 1, 0)).astype(np.int8)
    regimes = np.empty((n_paths, months, 3), dtype=np.int8)
    regimes[:, :, 0] = np.where(crisis, MacroRegime.CRIS, MacroRegime.EXP)
    regimes[:, :, 1] = np.where(crisis, ExitWindow.D, ExitWindow.N)
    regimes[:, :, 2] = np.where(crisis, ShockType.DB, ShockType.N)
    brent = 66.0 * np.exp(np.cumsum(factors[:, :, MINI_FACTORS.index("brent_log")], axis=1))
    meta = CubeMeta(
        world_id=wid, plane=Plane.SEARCH,
        base_entropy_hex=hashlib.sha256(f"testing.mini_cube|{wid}|{seed}".encode("utf-8")).digest()[:16].hex(),
        generator_hash=content_hash({"generator": "testing.mini_cube", "version": 1, "factors": _FACTOR_PARAMS,
                                     "regime": {str(k): v.tolist() for k, v in _P_REGIME.items()}, "cma": cma}),
        asof=MINI_ASOF, n_paths=n_paths, path_offset=0, months=months, factor_names=MINI_FACTORS,
        factor_kinds=MINI_FACTOR_KINDS, asset_names=MINI_ASSET_CLASSES, is_synthetic=True,
        data_class=DataClass.SYNTHETIC, checksum="sha256:" + "0" * 64)
    return ScenarioCube.build(
        meta, factors=f32, regimes=regimes, stress_post=stress_post, vol=vol.astype(np.float32), fin_window=fin_window,
        crowding_index=np.maximum(0.0, (hy - 0.04) / 0.04).astype(np.float32),
        asset_returns=assets.astype(np.float32), brent=brent.astype(np.float32))


def mini_flowcube(book: BookSnapshot, cube: ScenarioCube) -> FlowCube:
    """HOLD flows of every engine unit of ``book`` on ``cube`` by quarter (§4.5): [P, 40, U, 18] signed USD bn,
    units in ``unit_index()`` order without the treasury sleeves (the ledger's), α frozen at ``fake_beliefs``."""
    units, values = book_hold_flows(book, cube, beliefs=fake_beliefs(book))
    meta = FlowCubeMeta(unit_ids=tuple(m.unit_id for m in units), group_of=tuple(m.group for m in units), quarters=40,
                        cube_checksum=cube.meta.checksum)
    return FlowCube(meta=meta, values=values.astype(np.float32))
