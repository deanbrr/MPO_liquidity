"""Marks, forecasts, quotes and milestones (BUILD_SPEC v1.1 §3.5; brief §9; S-ADR-27).

ADIC's marks are since-inception net IRR or MOIC per holding with down/base/up cases, read as nominal quantiles
(P10/P50/P90 by default; per-group overrides in ``config/beliefs/translation.yaml``).
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from types import MappingProxyType
from typing import Final, Literal

from pydantic import model_validator

from adic_tpa.contracts.enums import ContractModel, DataClass, ExitWindow, MacroRegime, MarkType
from adic_tpa.contracts.ids import ArtifactRef, DecisionId, GroupId, HoldingId, check_synthetic_consistency

__all__ = ["CaseMap", "Mark", "ForecastSnapshot", "ForecastRecord", "Quote", "Milestone", "QUANTILE_LEVELS",
           "QuantileLabel"]

QuantileLabel = Literal["p05", "p10", "p25", "p50", "p75", "p90", "p95"]
QUANTILE_LEVELS: Final[Mapping[str, float]] = MappingProxyType({
    "p05": 0.05, "p10": 0.10, "p25": 0.25, "p50": 0.50, "p75": 0.75, "p90": 0.90, "p95": 0.95})


class CaseMap(ContractModel):
    """Cases read as nominal quantiles unless the group states otherwise (brief §9)."""

    down: Literal["p05", "p10", "p25"] = "p10"
    base: Literal["p50"] = "p50"
    up: Literal["p75", "p90", "p95"] = "p90"


class Mark(ContractModel):
    holding_id: HoldingId
    mark_type: MarkType
    as_of: date
    recorded_at: datetime
    basis: Literal["IRR", "MOIC", "TVPI", "YIELD", "YIELD_ON_COST", "EXIT_CAP_RATE", "NAV", "PRICE"]
    gross_net: Literal["gross", "net"]
    since_inception: bool = True                 # ADIC's IRR/MOIC marks are since inception (shown as sunk)
    value: float
    horizon_years: float | None = None
    exit_date: date | None = None
    author: str
    revision_id: int
    case_down: float | None = None
    case_base: float | None = None
    case_up: float | None = None
    case_map: CaseMap = CaseMap()                # per-group override from config/beliefs/translation.yaml
    is_synthetic: bool
    data_class: DataClass

    @model_validator(mode="after")
    def _rules(self) -> Mark:
        check_synthetic_consistency(self.is_synthetic, self.data_class, self.holding_id)
        cases = [c for c in (self.case_down, self.case_base, self.case_up) if c is not None]
        # a higher exit cap rate is the worse case, so its cases run the other way
        expected = sorted(cases, reverse=self.basis == "EXIT_CAP_RATE")
        if cases != expected:
            raise ValueError(f"{self.holding_id}: cases must be ordered from the down to the up case")
        return self


class ForecastSnapshot(ContractModel):
    u: float | None
    a: float | None
    nav_bn: float
    regime: MacroRegime
    exit: ExitWindow


class ForecastRecord(ContractModel):
    record_id: str
    group: GroupId
    holding_id: HoldingId | None
    author: str
    as_of: date
    recorded_at: datetime
    horizon_q: int
    exit_horizon_q: int | None = None            # forecast exit timing (IRR/MOIC targets)
    target: Literal["irr_si", "moic_si", "fwd_return_a", "distributions_bn", "calls_bn", "exit_quarter",
                    "net_alpha_a", "tvpi", "lay_a", "pnl_bn"]   # irr_si / moic_si: since-inception net (S-ADR-27)
    case_map: CaseMap = CaseMap()
    quantiles: dict[QuantileLabel, float]        # from the cases via case_map; p10 < p50 < p90
    cashflow_ref: ArtifactRef | None = None      # the unit's cash-flow history used by the translation
    cashflows_4q: tuple[float, ...] | None = None
    cashflows_8q: tuple[float, ...] | None = None
    snapshot: ForecastSnapshot
    decision_link: DecisionId | None = None
    shadow_id: str | None = None                 # declined deals
    resolved_value: float | None = None
    resolved_at: date | None = None
    is_synthetic: bool
    data_class: DataClass

    @model_validator(mode="after")
    def _rules(self) -> ForecastRecord:
        check_synthetic_consistency(self.is_synthetic, self.data_class, self.holding_id)
        ordered = [self.quantiles[k] for k in sorted(self.quantiles, key=QUANTILE_LEVELS.__getitem__)]
        if any(b <= a for a, b in zip(ordered, ordered[1:], strict=False)):
            raise ValueError(f"{self.record_id}: quantiles must increase strictly with the level (p10 < p50 < p90)")
        if (self.resolved_value is None) != (self.resolved_at is None):
            raise ValueError(f"{self.record_id}: resolved_value and resolved_at are set together")
        return self


class Quote(ContractModel):
    quote_id: str
    holding_id: HoldingId
    as_of: date
    kind: Literal["secondary_bid", "financing_reserve", "dealer_hybrid"]
    bid_pct_ref_nav: float
    ref_nav_date: date
    deferral_share: float = 0.0
    deferral_months: int = 0
    source: Literal["external", "in_house"]
    desk: GroupId | None = None
    counterparty_class: str
    conflict_flag: bool
    second_source_id: str | None = None
    is_synthetic: bool
    data_class: DataClass

    @model_validator(mode="after")
    def _rules(self) -> Quote:
        check_synthetic_consistency(self.is_synthetic, self.data_class, self.holding_id)
        if self.source == "in_house" and not self.conflict_flag:
            raise ValueError(f"{self.quote_id}: an in-house quote carries conflict_flag")
        return self


class Milestone(ContractModel):
    holding_id: HoldingId
    milestone_id: str
    description: str
    due: date
    verification_source: str
    status: Literal["pending", "met", "missed"]
