"""Worlds, state, path cubes and trees (BUILD_SPEC v1.1 §3.6, §3.7, §3.18, §4.8; S-ADR-35, -43).

``ScenarioCube`` holds one block of simulated months in the axis order [path, month, ...]. Its scenario identity
``meta.checksum`` = ``scenario_identity(meta, arrays)``: the content hash of the generating meta (every
``CubeMeta`` field except ``checksum``: world, plane, entropy, generator, as-of, paths and offset, factor names and
kinds, assets, data class) and of the arrays ``scen`` builds (``SCENARIO_ARRAYS``), so a relabelled cube no longer
matches the identity recorded in manifests, ``GroupRatesMeta.cube_checksum`` or ``FlowCubeMeta.cube_checksum``.
``ScenarioCube.build`` sets it. The draw rates attached later by ``owner.attach_draws`` and the group rates
attached by ``core.sim`` are covered by the container's ``checksum()`` (which also covers all of ``meta`` except the
derived ``meta.checksum``) but not by the identity, so attaching them never invalidates it.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, ClassVar, Final, Literal

import numpy as np
from pydantic import model_validator

from adic_tpa.contracts.arrays import B, F32, F64, I8, I16, I32, ArrayContainer
from adic_tpa.contracts.enums import (
    CFPStage, ContractModel, DataClass, FactorKind, MandateMode, Plane, ReturnBasis, ShockType, WorldId,
    check_world_id,
)
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import array_checksum, content_hash
from adic_tpa.contracts.ids import GroupId, MetricId
from adic_tpa.contracts.optimizer import NodeCoefficients
from adic_tpa.contracts.policy import PolicyRef

__all__ = [
    "validate_world_id", "CMALine", "RegimeParams", "FactorModelParams", "OilParams", "VolParams",
    "BootstrapParams", "MisspecOverride", "WorldSpec", "OilState", "StateSnapshot", "PanelRow", "StatePanel",
    "CubeMeta", "ScenarioCube", "GroupRatesMeta", "GroupRates", "TreeSpec", "Tree", "StressFilterParams",
    "OwnerConfig", "SCENARIO_ARRAYS", "scenario_identity",
]

# The arrays scen builds; their checksum is CubeMeta.checksum.
SCENARIO_ARRAYS: Final[tuple[str, ...]] = (
    "factors", "regimes", "stress_post", "vol", "fin_window", "crowding_index", "asset_returns", "brent")


def validate_world_id(world_id: str) -> str:
    """Return ``world_id`` if it is "M1".."M6", "B1", "B2" or "MS:<name>"; raise ``SchemaError`` otherwise."""
    try:
        return check_world_id(world_id)
    except ValueError as exc:
        raise SchemaError(str(exc), {"world_id": world_id}) from None


def _sums_to_one(values: tuple[float, ...], name: str, tol: float = 1e-6) -> None:
    if values and abs(math.fsum(values) - 1.0) > tol:
        raise ValueError(f"{name} must sum to 1 (got {math.fsum(values)})")


class CMALine(ContractModel):
    asset_class: str
    arith_mean_a: float
    vol_a: float
    basis: ReturnBasis
    benchmark: str
    fee_adjusted: bool
    selection_included: bool
    levered: bool = False


class RegimeParams(ContractModel):
    n_macro: Literal[3, 4, 5] = 4
    dwell_substates: int = 3                     # state-expanded HMM for NB dwell (PD §4.3)
    P_macro: list[list[float]]
    P_exit: list[list[float]]
    P_shock_annual: list[list[float]]
    kappa_shock_macro: list[list[float]]
    gw_dwell_by_elapsed: list[float]


class FactorModelParams(ContractModel):
    factor_names: tuple[str, ...]
    factor_kinds: tuple[FactorKind, ...]         # S-ADR-35
    c: dict[str, list[float]]
    A: list[list[float]]
    D: dict[str, list[float]]
    R0: list[list[float]]
    R_crisis: list[list[float]]
    omega: dict[str, float]
    df: int = 5                                  # ε = sqrt((df − 2)/df) · t_df (unit variance)
    provenance: dict[str, Literal["fitted", "set_and_verified"]]   # per factor; set_and_verified until data exist
    asset_loadings: dict[str, list[float]]
    asset_alpha: dict[str, dict[str, float]]
    asset_sigma: dict[str, dict[str, float]]

    @model_validator(mode="after")
    def _kinds(self) -> FactorModelParams:
        if len(self.factor_kinds) != len(self.factor_names):
            raise ValueError("factor_kinds must have one entry per factor name")
        if self.df <= 2:
            raise ValueError("df must exceed 2 for unit-variance t innovations")
        return self


class OilParams(ContractModel):
    mean_level: float = 70.0
    kappa: dict[str, float]
    vol: dict[str, float]
    rho_eq: dict[str, float]
    gw_jump: dict[str, float]


class VolParams(ContractModel):
    beta_T_coef: float = 0.94
    beta_T_exp: float = -0.43
    spot_vol_slope: tuple[float, float] = (-1.35, -0.94)
    move: dict[str, float]
    ovx: dict[str, float]


class BootstrapParams(ContractModel):
    panel_start: date
    panel_end: date
    block_months: tuple[int, int] = (12, 24)
    embargo_months: int = 12
    method: Literal["stationary_block", "fhs"]
    observed_factors: tuple[str, ...]            # resampled from data_public panels
    fill: Literal["conditional_e"] = "conditional_e"   # other factors from E given the block; labelled PROXY


class MisspecOverride(ContractModel):
    """Typed misspecification override (S-ADR-43), applied by ``EngineFactory.build``."""

    target_module: Literal["priv", "pub", "overlay", "owner", "ledger", "policy", "scen"]
    param_path: str                              # dotted path into the target's config model
    op: Literal["set", "mult"]
    value: float | str | bool


class WorldSpec(ContractModel):
    world_id: WorldId
    family: Literal["E", "B1", "B2"]
    provider: str
    cma_asof: date
    cma: dict[str, CMALine]
    regime: RegimeParams | None
    factors: FactorModelParams | None
    oil: OilParams
    vol: VolParams
    bootstrap: BootstrapParams | None = None
    misspec_tags: tuple[str, ...] = ()
    overrides: tuple[MisspecOverride, ...] = ()
    t6_class: Literal["M1_M5", "M6", "REPORT_ONLY"]
    content_hash: str

    @model_validator(mode="after")
    def _classes(self) -> WorldSpec:
        wid = self.world_id
        family = "B1" if wid == "B1" else "B2" if wid == "B2" else "E"
        if self.family != family:
            raise ValueError(f"{wid}: family must be {family}")
        if wid in ("M1", "M2", "M3", "M4", "M5", "B1", "B2") and self.t6_class != "M1_M5":
            raise ValueError(f"{wid}: t6_class must be M1_M5")
        if wid == "M6" and self.t6_class != "M6":
            raise ValueError("M6: t6_class must be M6")
        if wid.startswith("MS:") and self.t6_class == "M1_M5":
            raise ValueError(f"{wid}: misspecification worlds are M6 for T6 (or REPORT_ONLY)")
        if self.family in ("B1", "B2") and self.bootstrap is None:
            raise ValueError(f"{wid}: bootstrap families need BootstrapParams")
        return self


class OilState(ContractModel):
    spot: float
    front: float
    chi0: float                                  # χ0 = ln spot − ln front (gap_04 §6.1 step 6)
    xi0: float


class StateSnapshot(ContractModel):
    asof: date
    data_timestamps: dict[str, datetime]
    pi0_macro: tuple[float, ...]
    pi0_range: tuple[tuple[float, float], ...]
    stress_post: tuple[float, float, float]
    F_t: float
    F_base_rate: float
    F_ab: tuple[float, float]
    e0: tuple[float, float, float, float]
    z0: tuple[float, ...]
    z_disagreement: bool
    oil: OilState
    gw_elapsed_months: int
    draw_12m_bn: tuple[float, float]
    draw_p90_bn: float
    d_prev: float
    factor_levels0: dict[str, float]             # t0 levels of every level-kind factor (FactorKind.LEVEL)
    filter_version_hash: str
    content_hash: str

    @model_validator(mode="after")
    def _posteriors(self) -> StateSnapshot:
        _sums_to_one(self.pi0_macro, "pi0_macro")
        _sums_to_one(self.stress_post, "stress_post")
        _sums_to_one(self.e0, "e0")
        _sums_to_one(self.z0, "z0")
        if not 0.0 <= self.F_t <= 1.0:
            raise ValueError("F_t is a probability")
        return self


class PanelRow(ContractModel):
    index: int
    light: str
    metric_id: MetricId
    status: CFPStage | Literal["INFO"]
    policy_link: str


class StatePanel(ContractModel):
    rows: tuple[PanelRow, ...]                   # exactly 12 (gap_04 §8)

    @model_validator(mode="after")
    def _twelve(self) -> StatePanel:
        if len(self.rows) != 12:
            raise ValueError(f"the state panel has exactly 12 rows, got {len(self.rows)}")
        return self


class CubeMeta(ContractModel):
    world_id: WorldId
    plane: Plane
    base_entropy_hex: str
    generator_hash: str
    asof: date
    n_paths: int
    path_offset: int
    months: int = 120
    factor_names: tuple[str, ...]
    factor_kinds: tuple[FactorKind, ...]
    proxy_factors: tuple[str, ...] = ()          # B1/B2 factors filled from E's conditional model (PROXY)
    asset_names: tuple[str, ...]
    vol_names: tuple[str, ...] = ("log_vix30", "log_move", "ovx")
    is_synthetic: bool
    data_class: DataClass
    checksum: str

    @model_validator(mode="after")
    def _consistent(self) -> CubeMeta:
        if len(self.factor_kinds) != len(self.factor_names):
            raise ValueError("factor_kinds must have one entry per factor name")
        if not set(self.proxy_factors) <= set(self.factor_names):
            raise ValueError("proxy_factors must be factor names")
        if self.is_synthetic != (self.data_class == DataClass.SYNTHETIC):
            raise ValueError("is_synthetic disagrees with data_class")
        if self.n_paths < 1 or self.months < 1 or self.path_offset < 0:
            raise ValueError("n_paths and months must be positive and path_offset non-negative")
        try:
            bytes.fromhex(self.base_entropy_hex)
        except ValueError:
            raise ValueError("base_entropy_hex must be hex") from None
        return self


def scenario_identity(meta: CubeMeta, arrays: Mapping[str, Any]) -> str:
    """The value ``meta.checksum`` must hold: ``content_hash`` of every ``CubeMeta`` field except ``checksum`` and of
    ``array_checksum`` over the ``SCENARIO_ARRAYS`` (in that order) taken from ``arrays``."""
    missing = [name for name in SCENARIO_ARRAYS if name not in arrays]
    if missing:
        raise SchemaError(f"scenario_identity: missing scenario arrays {missing}")
    return content_hash({"meta": meta.model_dump(mode="python", exclude={"checksum"}),
                         "arrays": array_checksum(*(arrays[name] for name in SCENARIO_ARRAYS))})


class GroupRatesMeta(ContractModel):
    groups: tuple[GroupId, ...]
    age_buckets: tuple[str, ...]
    policy_ref: PolicyRef
    world_id: WorldId
    cube_checksum: str
    quarters: int = 12
    rate_kind: Literal["simple"] = "simple"


@dataclass(frozen=True, slots=True)
class GroupRates(ArrayContainer):
    """Recorded under HOLD + plan pacing over the tree's quarters; private groups × age buckets (§3.7)."""

    meta: GroupRatesMeta
    delta: F32                   # [P, Q, Gp, 2] distributions ÷ opening economic NAV, per quarter
    qcall: F32                   # [P, Q, Gp, 2] calls ÷ opening unfunded, per quarter
    ret_simple: F32              # [P, Q, Gp, 2] economic NAV simple return per quarter
    bid: F32                     # [P, Q, Gp, 2] cash-equivalent secondary bid ÷ economic NAV
    income: F32                  # [P, Q, Gp, 2] contractual cash income ÷ NAV
    u_per_nav: F32               # [P, Q, Gp, 2] unfunded per $ of economic NAV (κ^U)
    nav_share: F32               # [P, Q, Gp, 2] bucket share of the group's economic NAV (ω)
    call_stress_12m: F32         # [P, Q, Gp, 2] stressed 12-month call rate on unfunded
    lo_ret: F32
    hf_ret: F32                  # [P, Q]
    hf_phi: F32                  # [P, Q, 4]
    vm_per_beta: F32             # [P, Q]
    cash_rate: F32
    fac_rate: F32                # [P, Q] per quarter
    ra_debt_rate: F32
    ra_amort: F32
    ra_direct_share: F32         # [P, Q]
    tail_prem_rate: F32
    tail_value: F32
    opp_pnl_rate: F32
    delta_im_rate: F32           # [P, Q]
    draw_rate_q: F32             # [P, Q] instalment ÷ B_y
    stress_class: I8             # [P, Q] StressState at quarter end
    obs: F32                     # [P, Q, n_obs] observable features for tree clustering

    def _bindings(self) -> dict[str, int]:
        return {"Q": self.meta.quarters, "Gp": len(self.meta.groups), "Ab": len(self.meta.age_buckets)}


@dataclass(frozen=True, slots=True)
class ScenarioCube(ArrayContainer):
    meta: CubeMeta
    factors: F32                 # [P, M, K]  per factor kind (log return, level or change)
    regimes: I8                  # [P, M, 3]  (MacroRegime, ExitWindow, ShockType) in month period m
    stress_post: F32             # [P, M, 3]  stress-filter posterior after month m
    vol: F32                     # [P, M, V]
    fin_window: I8               # [P, M]     FinWindow (S-ADR-12)
    crowding_index: F32          # [P, M]     exogenous forced-selling index (S-ADR-13)
    asset_returns: F32           # [P, M, A]  monthly log returns per asset class
    brent: F32                   # [P, M]     USD/bbl at month end
    draw_rate: F32 | None = None          # [P, Y]  attached by owner.attach_draws (Y = 11)
    draw_override: B | None = None        # [P, Y]
    group_rates: GroupRates | None = None # attached by core.sim.record_group_rates (tree building only)

    _CHECKSUM_EXCLUDE: ClassVar[frozenset[str]] = frozenset({"meta.checksum"})

    @classmethod
    def build(cls, meta: CubeMeta, **arrays: Any) -> ScenarioCube:
        """A cube whose ``meta.checksum`` is set to ``scenario_identity(meta, arrays)`` (any value it held is replaced).

        ``arrays`` are the scenario arrays plus, optionally, ``draw_rate``, ``draw_override`` and ``group_rates``.
        """
        identity = scenario_identity(meta, arrays)
        return cls(meta=meta.model_copy(update={"checksum": identity}), **arrays)

    def scenario_checksum(self) -> str:
        """``scenario_identity`` of this cube's meta and scenario arrays; ``validate()`` requires it to equal
        ``meta.checksum``."""
        return scenario_identity(self.meta, {name: getattr(self, name) for name in SCENARIO_ARRAYS})

    def _bindings(self) -> dict[str, int]:
        return {"P": self.meta.n_paths, "M": self.meta.months, "K": len(self.meta.factor_names),
                "A": len(self.meta.asset_names), "V": len(self.meta.vol_names)}

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        if self.scenario_checksum() != self.meta.checksum:
            raise SchemaError("ScenarioCube: meta and scenario arrays do not match meta.checksum")
        if (self.draw_rate is None) != (self.draw_override is None):
            raise SchemaError("ScenarioCube: draw_rate and draw_override are attached together")
        if self.draw_rate is not None and self.draw_override is not None:
            normal = self.draw_rate[~self.draw_override].astype(np.float64)
            # float32 storage: compare the [5%, 10%] band at float32 resolution
            if normal.size and ((normal < 0.05 - 1e-7).any() or (normal > 0.10 + 1e-7).any()):
                raise SchemaError("ScenarioCube.draw_rate outside [0.05, 0.10] where not flagged as an override")
        if self.group_rates is not None and self.group_rates.meta.cube_checksum != self.meta.checksum:
            raise SchemaError("ScenarioCube.group_rates were recorded on another cube")


class TreeSpec(ContractModel):
    k1: int = 24
    k4: int = 4
    fan_leaves: int = 6
    fan_ends_q: tuple[int, ...] = (6, 8, 10, 12)
    paths_per_world: int = 2000
    worlds: tuple[WorldId, ...]                  # no code default: from the contract template (BUILD-38)
    tail_quantile: float = 0.02
    min_tail_leaves_per_world: int = 30
    reducer: Literal["kmeans_observable", "forward_filtration"] = "kmeans_observable"
    features: tuple[str, ...] = ("F_t", "stress_post_crisis", "p_exit_DF", "p_shock_DB_GW_SG", "cum_eq_ret",
                                 "hy_spread", "draw_rate_realized", "override_flag", "pe_dist_rate")
    seed: int = 0


@dataclass(frozen=True, slots=True)
class Tree(ArrayContainer):
    spec: TreeSpec
    tree_hash: str
    pooled_worlds: tuple[WorldId, ...]
    parent: I32                  # [N]  (−1 for root)
    t_end: I16                   # [N]  quarter instant at node end (0 for root)
    period_q: I8                 # [N]  1 (Q1–Q4) or 2 (fan periods)
    stage: I8                    # [N]  0 root; 1–4 quarterly; 5–8 fan
    p: F64                       # [N]  Σ_m w_m p_{n|m}
    p_world: F64                 # [N, W], W = len(spec.worlds)
    is_leaf: B                   # [N]
    leaf_world: I8               # [N]  world index for leaves, −1 otherwise
    lr_weight: F64               # [N]  likelihood-ratio weights for tail-stratum leaves (1.0 otherwise)
    member_ptr: I32              # [N + 1]  CSR pointers into member_idx
    member_idx: I32              # [nnz]    pooled path indices
    coef: NodeCoefficients       # GroupRates fields aggregated per node: [N, ...]
    obs_centroid: F64            # [N, n_obs]
    regime_class: I8             # [N]  StressState of the node centroid

    def _bindings(self) -> dict[str, int]:
        return {"W": len(self.spec.worlds)}

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        n = self.p.shape[0]
        if n == 0 or int(self.parent[0]) != -1 or (self.parent[1:] < 0).any() or (self.parent[1:] >= n).any():
            raise SchemaError("Tree: node 0 is the only root and parents index existing nodes")
        if int(self.member_ptr[-1]) != self.member_idx.shape[0]:
            raise SchemaError("Tree: member_ptr must end at len(member_idx)")
        if self.coef.delta.shape[0] != n:
            raise SchemaError("Tree.coef must have one row per node")
        child_mass = np.bincount(self.parent[1:], weights=self.p[1:], minlength=n)
        inner = ~self.is_leaf
        if not np.allclose(child_mass[inner], self.p[inner], rtol=0.0, atol=1e-12):
            raise SchemaError("Tree: children's p must sum to the parent's p (1e-12)")
        if abs(float(self.p[self.is_leaf].sum()) - 1.0) > 1e-12:
            raise SchemaError("Tree: leaf probabilities must sum to 1 (1e-12)")
        world_mass = self.p_world[self.is_leaf].sum(axis=0)
        if not np.allclose(world_mass, 1.0, rtol=0.0, atol=1e-12):
            raise SchemaError("Tree: per world, leaf probabilities must sum to 1 (1e-12)")
        lw = self.leaf_world
        if (lw[inner] != -1).any() or (lw[self.is_leaf] < 0).any() or (lw[self.is_leaf] >= len(self.spec.worlds)).any():
            raise SchemaError("Tree.leaf_world: world index on leaves, −1 elsewhere")


class StressFilterParams(ContractModel):
    """Produced by ``state`` (WP-07); consumed by ``scen`` and ``core.sim``."""

    means: list[list[float]]
    covs: list[list[list[float]]]
    transmat: list[list[float]]
    startprob: list[float]
    fitted_through: date
    ab: tuple[float, float]
    base_rate: float
    version_hash: str


class OwnerConfig(ContractModel):
    """Owner draw configuration (fields normative in §4.8); produced from ``config/owner.yaml``."""

    c: float = 0.075
    b: float = 0.625
    rho_d: float = 0.5
    override_p_a: dict[ShockType, float]         # 0.0025 (N, B, SS), 0.01 (SG, DB), 0.02 (GW)
    hydro_share: tuple[float, float] = (0.113, 0.091)
    breakeven_median: float = 55.0
    breakeven_p05_p95: tuple[float, float] = (45.0, 70.0)
    gw_wedge_pp: tuple[float, float] = (-5.0, 2.0)
    fiscal_noise_sd_pp: float
    ref_price: float
    basis: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"] = "opening_fy_reported_nav"
    mode: MandateMode = MandateMode.B_OWNER_CALL
    band_floor: float = 0.05
    p_accept_band: dict[ShockType, float]        # DB: 0.30 [I], others 1.0 (Mode H only)
    domestic_obligation_bn_a: tuple[float, float] | None = None   # Mode H only

    @model_validator(mode="after")
    def _probabilities(self) -> OwnerConfig:
        for name, table in (("override_p_a", self.override_p_a), ("p_accept_band", self.p_accept_band)):
            if any(not 0.0 <= v <= 1.0 for v in table.values()):
                raise ValueError(f"{name} holds probabilities in [0, 1]")
        return self
