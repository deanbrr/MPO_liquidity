"""Policy contracts (BUILD_SPEC v1.1 §3.11; ARCH §5.10–§5.11; S-ADR-13, S-ADR-30).

``PolicySpec`` is the DSL object agents propose and the evaluator compiles; its type rules TR1–TR8 are checked by
``core.dsl`` (WP-21), not here. ``ResidualSpec.box`` uses ``Interval`` sub-models instead of fixed (lo, hi)
tuples because ``IdeaBundle`` carries a ``PolicySpec`` in an LLM-facing schema (§3.16, S-ADR-36).

``PolicySpec.spec_hash`` is a derived read-only property, not the ``@computed_field`` §3.11 writes: a computed
field is serialized by ``model_dump_json`` and then rejected as ``extra_forbidden`` by ``model_validate_json``, so
``PolicySpec``, ``IdeaBundle`` and ``VariantSet`` could not round-trip through their own JSON (S-ADR-39 requires
MCP payloads and registry rows to be validated that way). A spec has one identity:
``spec.spec_hash == content_hash(spec)``, and the plane store keys compiled specs on it (§7.4 ``compile_spec``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final, Literal

from pydantic import model_validator

from adic_tpa.contracts.arrays import F32, ArrayContainer
from adic_tpa.contracts.enums import Book, ContractModel, Interval, Lens, MandateMode
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import GroupId, HoldingId

__all__ = [
    "PolicyRef", "FeatureExpr", "ResidualSpec", "PackageItem", "ActionPackage", "OverlayLeg", "OverlayStructure",
    "PolicySpec", "RecourseOrder", "Observables", "RECOURSE_RUNGS", "NATIVE_POLICIES", "Rung",
]

# Native policies named in §3.11 (controls, archetypes, the anchor P0 and the H-derived C_H).
NATIVE_POLICIES: Final[tuple[str, ...]] = (
    "HOLD", "STATIC_SAA", "DECK_RULES", "TARGET_CHASING", "PLACEBO", "PRO_RATA", "OVERLAY_ONLY", "LIQUID_FIRST",
    "CASH_LAST", "ARCH_A", "ARCH_B", "ARCH_C", "P0", "C_H")

Rung = Literal["reserve", "p2s", "liquid", "facility", "amber", "red"]
# Index order of ActionSlice.recourse_order codes (§3.8); there is no "preemptive" rung (S-ADR-30).
RECOURSE_RUNGS: Final[tuple[Rung, ...]] = ("reserve", "p2s", "liquid", "facility", "amber", "red")
_ANCHOR_RE: Final = re.compile(r"^[A-Za-z0-9_]+@sha256:[0-9a-f]{64}$")


class PolicyRef(ContractModel):
    """Reference to a native policy or a compiled ``PolicySpec``."""

    kind: Literal["native", "spec"]
    name: str
    params_hash: str
    spec_hash: str | None = None

    @model_validator(mode="after")
    def _consistent(self) -> PolicyRef:
        if self.kind == "native" and self.name not in NATIVE_POLICIES:
            raise ValueError(f"unknown native policy {self.name!r}; expected one of {NATIVE_POLICIES}")
        if self.kind == "spec" and self.spec_hash is None:
            raise ValueError("a spec PolicyRef needs spec_hash")
        return self


class FeatureExpr(ContractModel):
    var: str                                     # registry variable (config/core/dsl_variables.yaml)
    lag: int                                     # quarters; >= registry minimum (TR1)
    xforms: tuple[Literal["logit", "zscore_frozen", "diff", "min", "max", "hinge"], ...] = ()
    xform_args: tuple[float, ...] = ()

    @model_validator(mode="after")
    def _lag(self) -> FeatureExpr:
        if self.lag < 0:
            raise ValueError("lag must be >= 0 quarters")
        return self


class ResidualSpec(ContractModel):
    slot: str                                    # reserve_target | pacing_mult[g] | econ_leverage | tail_hedge_ratio
                                                 # | opp_budget | sell_screen[g] | refi_hurdle[g] | hf_notice_share
                                                 # | p2s_share | recourse_order | preemptive_raise | payout_topup (TR8)
    form: Literal["mult_tanh", "add_clip", "switch_hyst"]
    rho: float | None = None
    lo: float | None = None
    hi: float | None = None
    on: float | None = None
    off: float | None = None
    features: tuple[FeatureExpr, ...]            # 1..3
    box: tuple[Interval, ...]                    # one box per weight; must contain 0 (TR5)
    gate_id: str

    @model_validator(mode="after")
    def _counts(self) -> ResidualSpec:
        if not 1 <= len(self.features) <= 3:
            raise ValueError(f"a residual takes 1..3 features, got {len(self.features)}")
        return self


class PackageItem(ContractModel):
    target: HoldingId | GroupId
    lens: Lens
    instrument: str
    size_bn: float | None = None
    size_frac: float | None = None
    trigger: FeatureExpr | None = None
    window_q: int = 1


class ActionPackage(ContractModel):
    items: tuple[PackageItem, ...]               # <= 12, <= 1 lens per asset per quarter

    @model_validator(mode="after")
    def _limits(self) -> ActionPackage:
        if len(self.items) > 12:
            raise ValueError(f"a package holds at most 12 items, got {len(self.items)}")
        targets = [str(i.target) for i in self.items]
        if len(set(targets)) != len(targets):
            raise ValueError("at most one lens per asset per quarter")
        return self


class OverlayLeg(ContractModel):
    template: str
    strike_rel: float | None
    expiry_months: int
    notional_bn: float
    side: Literal["long", "short"]


class OverlayStructure(ContractModel):
    template: str
    legs: tuple[OverlayLeg, ...]
    sleeve: Book
    monetization_trigger: FeatureExpr | None = None


class PolicySpec(ContractModel):
    """A DSL policy: P0 anchor plus residuals, packages and overlay structures (ARCH §5.11)."""

    anchor: str                                  # "P0@sha256:..."
    residuals: tuple[ResidualSpec, ...] = ()     # 0..6
    packages: tuple[ActionPackage, ...] = ()     # 0..3
    overlays: tuple[OverlayStructure, ...] = ()  # 0..3
    mandate_mode: MandateMode = MandateMode.B_OWNER_CALL

    @model_validator(mode="after")
    def _limits(self) -> PolicySpec:
        if not _ANCHOR_RE.match(self.anchor):
            raise ValueError(f"anchor must look like 'P0@sha256:<64 hex>', got {self.anchor!r}")
        if len(self.residuals) > 6 or len(self.packages) > 3 or len(self.overlays) > 3:
            raise ValueError("PolicySpec allows at most 6 residuals, 3 packages and 3 overlay structures")
        return self

    @property
    def spec_hash(self) -> str:
        """The spec's identity, ``content_hash(self)``; derived, so never serialized or accepted as input."""
        return content_hash(self)


class RecourseOrder(ContractModel):
    """P0's state-dependent recourse waterfall (S-ADR-13)."""

    rungs: tuple[Rung, ...]                      # no "preemptive" rung (S-ADR-30)
    switch_on: Literal["planning_stage", "drought"] | None = None
    alt_rungs: tuple[str, ...] | None = None
    switch_threshold: float | None = None
    crowding_haircut_coef: float = 0.0           # discount per unit of ScenarioCube.crowding_index (S-ADR-13)

    @model_validator(mode="after")
    def _permutation(self) -> RecourseOrder:
        if sorted(self.rungs) != sorted(RECOURSE_RUNGS):
            raise ValueError(f"rungs must be a permutation of {RECOURSE_RUNGS}, got {self.rungs}")
        if self.alt_rungs is not None and sorted(self.alt_rungs) != sorted(RECOURSE_RUNGS):
            raise ValueError(f"alt_rungs must be a permutation of {RECOURSE_RUNGS}, got {self.alt_rungs}")
        if self.switch_on is not None and (self.alt_rungs is None or self.switch_threshold is None):
            raise ValueError("switch_on needs alt_rungs and switch_threshold")
        return self

    def codes(self, *, alternative: bool = False) -> tuple[int, ...]:
        """Rung order as indices into ``RECOURSE_RUNGS`` (the ``ActionSlice.recourse_order`` row)."""
        order = self.alt_rungs if alternative and self.alt_rungs is not None else self.rungs
        return tuple(RECOURSE_RUNGS.index(r) for r in order)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class Observables(ArrayContainer):
    """Lagged DSL variables at quarter ``t``; no world id, path id, horizon or budget is present (TR2)."""

    t: int
    values: dict[str, F32]                       # DSL variables already lagged, each [P]
    unit_values: dict[str, F32]                  # per-unit observables, each [P, U]
    group_values: dict[str, F32]                 # per-group observables, each [P, G]
    world_hidden: Literal[True] = True
