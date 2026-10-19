"""Overlay contracts (BUILD_SPEC v1.1 §3.4, §3.18; ARCH §4.6; GROUPS §3.7).

Three books (TAIL, OPP, BETA); CRIF rows use the ISDA Risk Data Standard keys. ``OverlayGreeks`` and
``OverlayStressCoeffs`` are array containers (B = 3 books, K factors, J vega buckets, S named stresses).

``CSA`` (listed under §3.3) is defined here because ``OverlayBook`` holds it and ``contracts.book`` imports this
module; ``contracts.book`` re-exports it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from pydantic import model_validator

from adic_tpa.contracts.arrays import F64, ArrayContainer
from adic_tpa.contracts.enums import Book, ContractModel, DataClass
from adic_tpa.contracts.ids import CsaId, GroupId, TradeId, check_synthetic_consistency

__all__ = ["OverlayTrade", "CRIFRow", "ServiceContract", "OverlayPolicy", "OverlayBook", "OverlayGreeks",
           "OverlayStressCoeffs", "CSA"]


class CSA(ContractModel):
    """Credit support annex terms (§3.3; S-ADR-15 VM delays)."""

    csa_id: CsaId
    dealer_id: str
    threshold_bn: float
    mta_bn: float
    ia_bn: float
    eligible_collateral: tuple[Literal["cash", "ust", "ig"], ...]
    reuse_right: bool
    im_regime: Literal["two_way_simm", "ia_only", "cleared"]
    phi_recognition: float                       # 1.0 cash VM, 0.7 OTC collateral with reuse, 0.0 pledged
    gcc_dealer: bool = False
    settlement_lag_bd: int = 1
    stress_delay_bd: int = 3                     # S-ADR-15


class OverlayTrade(ContractModel):
    trade_id: TradeId
    book: Book
    template: str
    client_group: GroupId | None = None
    service_id: str | None = None
    underlying: str
    strike_rel: float | None = None
    strike2_rel: float | None = None
    expiry: date | None = None
    notional_bn: float
    premium_bn: float
    venue: Literal["listed", "cleared", "bilateral"]
    csa_id: CsaId | None = None
    rung: Literal["3M", "6M", "12M"] | None = None
    s_lock_a: float | None = None
    trigger_state: str | None = None
    is_synthetic: bool
    data_class: DataClass

    @model_validator(mode="after")
    def _labels(self) -> OverlayTrade:
        check_synthetic_consistency(self.is_synthetic, self.data_class, self.trade_id)
        if self.venue == "bilateral" and self.csa_id is None:
            raise ValueError(f"{self.trade_id}: a bilateral trade needs a csa_id")
        return self


class CRIFRow(ContractModel):
    """ISDA Risk Data Standards keys (GROUPS §3.7)."""

    trade_id: TradeId
    portfolio_id: str
    product_class: Literal["RatesFX", "Credit", "Equity", "Commodity"]
    risk_type: str
    qualifier: str
    bucket: str
    label1: str | None
    label2: str | None
    amount_usd_bn: float
    im_model: Literal["SIMM", "Schedule"]
    end_date: date | None
    post_regulations: str | None
    collect_regulations: str | None


class ServiceContract(ContractModel):
    service_id: str
    client_group: GroupId
    kind: Literal["completion_beta", "p2s", "pe_beta_rebuild", "group_hedge", "portable_alpha_collateral"]
    notional_bn: float
    reference_index: str
    s_lock_a: float
    clc_basis_bn: float


class OverlayPolicy(ContractModel):
    tail_budget_a: float = 0.0015                # IC floor 0.15% of NAV a year; cap 0.50% (GROUPS §3.7)
    tail_budget_cap_a: float = 0.0050
    ladder_weights: tuple[float, float, float] = (0.25, 0.50, 0.25)   # 3M/6M/12M rungs, 90/72 put spreads
    opp_vol_target_a: float = 0.011
    opp_im_budget_bn: float = 1.5
    completion_beta_bn: float = 10.0
    ov1_ratio: float = 0.75                      # [I] IC-set
    ov2_max: float = 0.25
    ov3_share: float = 0.5
    dealer_max_share_nav: float = 0.005
    min_dealers: int = 5

    @model_validator(mode="after")
    def _ladder(self) -> OverlayPolicy:
        if abs(sum(self.ladder_weights) - 1.0) > 1e-9:
            raise ValueError("ladder_weights must sum to 1")
        if not self.tail_budget_a <= self.tail_budget_cap_a:
            raise ValueError("tail_budget_a must not exceed tail_budget_cap_a")
        return self


class OverlayBook(ContractModel):
    trades: tuple[OverlayTrade, ...]
    csas: tuple[CSA, ...]
    services: tuple[ServiceContract, ...]
    policy: OverlayPolicy
    fixture: bool = False                        # True for the ≈250-trade engine-test blotter

    @model_validator(mode="after")
    def _csa_refs(self) -> OverlayBook:
        known = {c.csa_id for c in self.csas}
        missing = sorted({str(t.csa_id) for t in self.trades if t.csa_id is not None and t.csa_id not in known})
        if missing:
            raise ValueError(f"trades reference unknown CSAs {missing}")
        return self


@dataclass(frozen=True, slots=True)
class OverlayGreeks(ArrayContainer):
    delta: F64                                   # [B, K]
    gamma_diag: F64                              # [B, K]
    vega: F64                                    # [B, J] by expiry bucket
    vanna: F64                                   # [B, J]
    volga: F64                                   # [B, J]
    theta: F64                                   # [B]
    nv_eq: F64                                   # [S] economic net VIX-equivalent vega per named stress
    pnl_stress: F64                              # [B, S]


@dataclass(frozen=True, slots=True)
class OverlayStressCoeffs(ArrayContainer):
    """Per-unit stress coefficients of overlay columns for the OV1/OV2 rows in H (§3.18)."""

    stresses: tuple[str, ...]
    col_ids: tuple[str, ...]
    nv_eq_tail: F64
    nv_eq_ovl: F64
    pnl_tail: F64
    pnl_opp: F64                                 # [S, n_cols] per unit of each overlay column
    base_nv_eq_tail: F64
    base_nv_eq_ovl: F64
    base_pnl_tail: F64
    base_pnl_opp: F64                            # [S] for the current book
