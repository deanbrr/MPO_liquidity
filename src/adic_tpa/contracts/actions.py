"""Actions and decision cards (BUILD_SPEC v1.1 §3.13; ARCH §4.8; JE-MF9, ADR-49).

``LensAction`` enforces the exposure/financing semantics of the six lenses as schema rules: REFINANCE is
cash-out with exposure unchanged; LEVER is exposure-up funded by new financing (≡ ADD + REFI).

Import note: ``contracts.optimizer`` needs ``LensAction`` and ``ActionCatalogue`` needs ``optimizer.ColumnPool``.
The cycle is broken by importing ``ColumnPool`` below the models that optimizer needs (and optimizer importing
``LensAction`` at its end), which works whichever module is imported first.
"""

from __future__ import annotations

from datetime import date
from typing import Final, Literal

from pydantic import model_validator

from adic_tpa.contracts.enums import (
    ConsentScenario, ContractModel, DataClass, EvidencePlane, FinWindow, Lens, MacroRegime, MarkType, PricedOn,
)
from adic_tpa.contracts.ids import ArtifactRef, GroupId, UnitId

__all__ = [
    "LensAction", "InstrumentSpec", "ActionCatalogue", "FlipThresholds", "WaterfallItem", "BeliefCard",
    "DecisionCard", "ZERO_TOL",
]

ZERO_TOL: Final = 1e-12   # "== 0" in the lens rules means |x| ≤ 1e-12


class LensAction(ContractModel):
    """One lens action on a unit (or a group-level PACE action)."""

    unit_id: UnitId | None
    group: GroupId
    lens: Lens
    instrument: str
    size_bn: float
    exposure_delta_bn: float
    financing_delta_bn: float
    cash_out_bn: float

    @model_validator(mode="after")
    def _lens_rules(self) -> LensAction:
        exp, fin, cash = self.exposure_delta_bn, self.financing_delta_bn, self.cash_out_bn
        zero_exp, zero_fin = abs(exp) <= ZERO_TOL, abs(fin) <= ZERO_TOL
        lens = self.lens
        if lens is Lens.SELL and not exp < -ZERO_TOL:
            raise ValueError("SELL requires exposure_delta_bn < 0")
        if lens is Lens.HOLD and not (zero_exp and zero_fin):
            raise ValueError("HOLD requires exposure_delta_bn == 0 and financing_delta_bn == 0")
        if lens is Lens.REFINANCE and not (zero_exp and fin > ZERO_TOL and cash > ZERO_TOL):
            raise ValueError("REFINANCE requires exposure_delta_bn == 0, financing_delta_bn > 0 and cash_out_bn > 0")
        if lens is Lens.ADD and not (exp > ZERO_TOL and zero_fin):
            raise ValueError("ADD requires exposure_delta_bn > 0 and financing_delta_bn == 0")
        if lens is Lens.LEVER and not (exp > ZERO_TOL and fin > ZERO_TOL):
            raise ValueError("LEVER requires exposure_delta_bn > 0 and financing_delta_bn > 0")
        if lens is Lens.PACE and self.unit_id is not None:
            raise ValueError("PACE is a group-level action: unit_id must be None")
        return self


class InstrumentSpec(ContractModel):
    instrument_id: str
    group: GroupId
    lens: Lens
    description: str
    price_model: str
    availability: dict[MacroRegime, float]
    fin_window_mult: dict[FinWindow, float]
    lag_q: int
    consent_required: bool
    external_only: Literal[True] = True          # only external counterparties raise liquidity
    params: dict[str, float]


class FlipThresholds(ContractModel):
    reservation_price: float | None
    breakeven_fwd_return_a: float | None
    breakeven_ell_a: float | None
    one_off_premium: float | None
    lever_breakeven_financing_a: float | None = None   # LEVER flips where α* − risk charge = financing cost (ADR-49)


class WaterfallItem(ContractModel):
    label: str
    value_usd_m: float


class BeliefCard(ContractModel):
    raw_marks: dict[MarkType, float | None]
    fused_mu_a: float
    sigma_a: float
    band80: tuple[float, float]
    market_anchor_a: float | None
    flags: tuple[str, ...]
    zombie: bool
    catalyst_status: Literal["ok", "missing", "overdue", "n/a"]
    p_achieved_4q: float
    p_achieved_8q: float
    info_value_usd_m: float | None


class DecisionCard(ContractModel):
    """Generated per holding, never hand-edited (ARCH §4.8)."""

    card_id: str
    unit_id: UnitId | None
    group: GroupId
    asof: date
    action: LensAction
    reduced_cost_bp: float
    dual_interval_bp: tuple[float, float]
    at_kink: bool
    value_usd_m: float
    p_best: float
    regret_bp: tuple[float, float]
    lapv_waterfall: tuple[WaterfallItem, ...]
    flips: FlipThresholds
    belief: BeliefCard
    consents: tuple[str, ...]
    rofr: bool
    envelope_use_bn: float
    alpha_star_a: float
    drag_a: float
    priced_on: PricedOn
    consent_scenario: ConsentScenario
    recovery_hash: str | None
    gamma_status: Literal["certified", "selection_not_certified"]
    consent_sensitive: bool
    second_order_material: bool
    tree_sensitive: bool
    hp_rank_flag: bool
    t6_consuming: bool                           # "counts as a T6 red event in the current state" (S-ADR-30)
    lever_legs: tuple[WaterfallItem, ...] | None = None   # ADD and REFI legs of a LEVER (ADR-49)
    binding_rows: tuple[str, ...]
    shadow_prices: dict[str, tuple[float, float, float]]   # value, one-sided lo, hi
    plane: EvidencePlane
    run_ref: ArtifactRef
    data_class: DataClass

    @model_validator(mode="after")
    def _consistency(self) -> DecisionCard:
        if self.priced_on is PricedOn.RESTORED and self.recovery_hash is None:
            raise ValueError("a card priced on the restored problem must carry its recovery_hash")
        if self.action.lens is Lens.LEVER and self.lever_legs is None:
            raise ValueError("a LEVER card shows its ADD and REFI legs (ADR-49)")
        return self


# Deferred import (see module docstring): optimizer imports LensAction from this module.
from adic_tpa.contracts.optimizer import ColumnPool  # noqa: E402


class ActionCatalogue(ContractModel):
    instruments: tuple[InstrumentSpec, ...]
    columns: ColumnPool
    overlay_stress_ref: ArtifactRef              # NV^eq and P&L per named stress per overlay column (OV1/OV2 rows)
    hash: str
