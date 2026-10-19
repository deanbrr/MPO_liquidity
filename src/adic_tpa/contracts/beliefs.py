"""Beliefs and the bridge (BUILD_SPEC v1.1 §3.10; ARCH §4.7, §4.11; S-ADR-10, -27, -28).

``BeliefSet.alpha_a`` is the fused forward log return in excess of the unit's benchmark; ``mu_total_a =
bench_ref_a + alpha_a`` is for display, cards and Tier-1 views only and never reaches an engine, which adds only
α to the world's beta return (S-ADR-28). ``BeliefDraws`` carries the per-path α draws for one world and block.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from typing import Final, Literal

import numpy as np

from adic_tpa.contracts.arrays import B, F32, F64, U32, ArrayContainer
from adic_tpa.contracts.enums import ContractModel, DataClass, MarkType, WorldId
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.ids import SponsorId, UnitId

__all__ = ["BeliefMeta", "BeliefSet", "BeliefDraws", "UnitBelief", "LeverLine", "BridgeCard", "BELIEF_FLAG_BITS",
           "FUSION_SIGNALS"]

# BeliefSet.flags bitmask: F1..F10 = bits 0-9, ZOMBIE = 10, CATALYST_MISSING = 11.
BELIEF_FLAG_BITS: Final[tuple[str, ...]] = (
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "ZOMBIE", "CATALYST_MISSING")
# Column order of BeliefSet.weights: forecast, underwritten, actual, market-implied (f, u, a, m).
FUSION_SIGNALS: Final[tuple[MarkType, ...]] = (
    MarkType.FORECAST, MarkType.UNDERWRITTEN, MarkType.ACTUAL, MarkType.MARKET_IMPLIED)


class BeliefMeta(ContractModel):
    asof: date
    fbe_version: str
    prior_hash: str
    inputs_hash: str
    frozen_optimizer_outputs_hash: str           # previous quarter's SELL flags and envelope status (acyclic)
    data_class: DataClass
    content_hash: str


@dataclass(frozen=True, slots=True)
class BeliefSet(ArrayContainer):
    meta: BeliefMeta
    unit_ids: tuple[UnitId, ...]
    alpha_a: F64                 # [U] fused forward log return in EXCESS of the benchmark, a year, net
    benchmark_id: tuple[str, ...]   # [U] CMA asset class of the unit's benchmark
    beta_hat: F64                # [U]
    bench_ref_a: F64             # [U] r_f + β̂·ERP_ref (mixture CMA, as-of)
    mu_total_a: F64              # [U] = bench_ref_a + alpha_a; display only
    sigma_hat: F64               # [U]
    band80: F64                  # [U, 2] on mu_total_a
    mu_p10: F64                  # [U] Tier-1 view: posterior P10 with group bias at +2 sd
    weights: F64                 # [U, 4] fusion weights on (f, u, a, m); 0 where absent
    market_anchor: F64
    has_market: B                # [U]
    nowcast_nav_bn: F64          # [U]
    flags: U32                   # [U] bitmask (BELIEF_FLAG_BITS)
    p_achieved: F64              # [U, 2] P(forecast achieved within 4, 8 quarters)
    group_bias_mean: F64
    group_bias_sd: F64
    kappa: F64                   # [G]
    info_value_usd_m: F64 | None = None   # [G] information value of each group's forecast (W2)

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if np.abs(self.mu_total_a - (self.bench_ref_a + self.alpha_a)).max(initial=0.0) > 1e-12:
            raise SchemaError("BeliefSet: mu_total_a must equal bench_ref_a + alpha_a (1e-12)")
        if not ((self.band80[:, 0] < self.mu_total_a) & (self.mu_total_a < self.band80[:, 1])).all():
            raise SchemaError("BeliefSet: band80[:, 0] < mu_total_a < band80[:, 1] must hold")

    def flag_names(self, i: int) -> tuple[str, ...]:
        """Names of the flags set on unit ``i``."""
        bits = int(self.flags[i])
        return tuple(name for b, name in enumerate(BELIEF_FLAG_BITS) if bits >> b & 1)


@dataclass(frozen=True, slots=True)
class BeliefDraws(ArrayContainer):
    """Per-path α draws for one world and block (``beliefs.draw_paths``); consumed via ``AssetEngine.init``.

    Invariant: draws frozen at α̂ (eta_sd = 0, bias = 0, GP effect = 0, no basis shift) reproduce the no-learning
    variant exactly (``alpha0_q == BeliefSet.alpha_a / 4``).
    """

    world_id: WorldId
    path_offset: int
    unit_ids: tuple[UnitId, ...]
    gp_ids: tuple[SponsorId, ...]
    alpha0_q: F32                # [P, U]
    group_bias_q: F32            # [P, G]
    gp_effect_q: F32             # [P, n_gp]
    m_q: F64
    phi: F64
    eta_sd_q: F64                # [U] learning: α_{t+1} = m + φ(α_t − m) + η_t


class UnitBelief(ContractModel):
    """Card view of one unit's beliefs."""

    unit_id: UnitId
    raw: dict[MarkType, float | None]
    fused_mu_a: float
    alpha_a: float
    benchmark_id: str
    sigma_a: float
    band80: tuple[float, float]
    market_anchor_a: float | None
    flags: tuple[str, ...]
    p_achieved_4q: float
    p_achieved_8q: float
    weights: dict[MarkType, float]


class LeverLine(ContractModel):
    name: str
    weight: float
    alpha_star_a: float
    sd_a: float
    benchmark: str


class BridgeCard(ContractModel):
    """What-you-need-to-believe bridge per world (ARCH §4.11)."""

    world_id: WorldId
    beta_return_a: float
    levers: tuple[LeverLine, ...]
    overlay_sr: float
    overlay_sigma_a: float
    leverage: float
    drags: dict[str, float]
    arith_mean_a: float
    geom_mean_a: float
    gap_to_target_pp: float
    p_mu_ge_target: tuple[float, float]          # (independent, comonotone levers)
    p_10y_ge_target: float
    break_evens: dict[str, float]
    verdict: Literal["Plan", "Stretch", "Aspiration"]
    data_class: DataClass
