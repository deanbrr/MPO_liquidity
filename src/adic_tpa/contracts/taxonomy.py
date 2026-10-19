"""Group taxonomy as configuration (BUILD_SPEC v1.1 §3.2; S-ADR-01, S-ADR-05, S-ADR-22, S-ADR-32).

``GroupId`` is a validated string, never a closed enum; the group set, codes and capabilities come from
``config/taxonomy/groups_v{1,2}.yaml`` (v2 default: eight investment groups plus the non-investment owners
``CF`` and ``TPA``). Engine code reads capabilities (``GroupSpec`` flags), never group names;
``tests/layering/test_no_hardcoded_group_ids.py`` scans ``src/`` for literals equal to a configured id or code.
"""

from __future__ import annotations

import functools
from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from pydantic import model_validator

from adic_tpa.contracts.config import ConfigLoad, config_root, load_yaml, load_yaml_audited, note_config_load
from adic_tpa.contracts.enums import ContractModel, Lens, RecourseTier
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import RESERVED_SYN_CODES, GroupId

__all__ = ["GroupSpec", "CouplingSpec", "TaxonomyConfig", "GroupRegistry", "GroupKind", "EngineName",
           "INVESTMENT_KINDS", "SEATS_BEYOND_GROUPS", "taxonomy_path"]

GroupKind = Literal["private", "public", "overlay", "funding", "attribution"]
EngineName = Literal["fund", "company", "claims", "credit", "realassets", "hf", "longonly", "overlay", "treasury"]
INVESTMENT_KINDS: tuple[GroupKind, ...] = ("private", "public", "overlay")
# CIO, CRO, Treasurer, Outside-View Forecaster, Red Team: seats = n_groups + 5 (S-ADR-22).
SEATS_BEYOND_GROUPS = 5


class GroupSpec(ContractModel):
    """One group's capabilities (§3.2)."""

    group_id: GroupId
    code: str                                   # SYN id code: PE, SEC, CS, CO, PM, PC, OVL, RA, CF, TPA
    display_name: str
    kind: GroupKind
    engines: tuple[EngineName, ...]
    recourse_tier: RecourseTier | None          # tier where its SALES enter
    red_tier: bool                              # forced sale = T6 red event (S-ADR-05)
    amber_tier: bool
    has_unfunded: bool
    age_buckets: tuple[str, ...] = ("young", "mature")
    young_max_age_years: float = 4.0
    lenses: tuple[Lens, ...]
    forecast_basis: Literal["gp_projection", "deal_model", "contract_yield", "loss_adjusted_yield", "net_alpha",
                            "benchmark_ir", "strategy_pnl", "business_plan"]
    fbe_path: Literal["fund", "single_deal", "cohort", "hierarchical_factor", "benchmark", "scenario"]
    seat: bool
    commitment_split: float = 0.0               # canonical new-commitment split (sum = 1 over groups)
    pacing_eta_sign: Literal[-1, 0, 1] = 0
    contingent_budget: bool = False
    in_envelopes: bool = True
    fund_distribution_stress: bool = False      # s* applies 0.45(1 − θ) × drought rates to its fund distributions

    @model_validator(mode="after")
    def _consistent(self) -> GroupSpec:
        if not (2 <= len(self.code) <= 5 and self.code.isupper() and self.code.isalpha()):
            raise ValueError(f"group code {self.code!r} must be 2-5 upper-case letters")
        if self.code in RESERVED_SYN_CODES:
            raise ValueError(f"group code {self.code!r} is reserved for another id kind")
        if not 0.0 <= self.commitment_split <= 1.0:
            raise ValueError(f"commitment_split must lie in [0, 1], got {self.commitment_split}")
        if self.red_tier and self.recourse_tier is not RecourseTier.ALL:
            raise ValueError(f"{self.group_id}: red-tier sales enter at ALL, got {self.recourse_tier}")
        if self.amber_tier and self.recourse_tier not in (RecourseTier.TPFA, RecourseTier.ALL):
            raise ValueError(f"{self.group_id}: amber-tier sales enter at TPFA or ALL, got {self.recourse_tier}")
        if self.fund_distribution_stress and self.kind != "private":
            raise ValueError(f"{self.group_id}: fund_distribution_stress applies to private groups only")
        if not self.age_buckets or len(set(self.age_buckets)) != len(self.age_buckets):
            raise ValueError(f"{self.group_id}: age_buckets must be non-empty and unique")
        return self


class CouplingSpec(ContractModel):
    """A cross-group coupling (§3.2; G-gap_04 §1.2)."""

    kind: Literal["offered_flow", "shared_gp_effect", "recap_netting"]
    source: GroupId
    target: GroupId
    params: dict[str, float | list[float] | str]   # incl. time_unit ("quarter")


class TaxonomyConfig(ContractModel):
    """The YAML model of ``config/taxonomy/groups_v{1,2}.yaml``."""

    version: Literal["v1", "v2"]
    groups: tuple[GroupSpec, ...]
    strategies: dict[GroupId, tuple[str, ...]]
    couplings: tuple[CouplingSpec, ...]

    @model_validator(mode="after")
    def _consistent(self) -> TaxonomyConfig:
        ids = [g.group_id for g in self.groups]
        codes = [g.code for g in self.groups]
        if len(set(ids)) != len(ids):
            raise ValueError(f"duplicate group ids in taxonomy {self.version}")
        if len(set(codes)) != len(codes):
            raise ValueError(f"duplicate group codes in taxonomy {self.version}")
        split = sum(g.commitment_split for g in self.groups)
        if abs(split - 1.0) > 1e-9:
            raise ValueError(f"commitment_split must sum to 1 over groups, got {split}")
        unknown = set(self.strategies) - set(ids)
        if unknown:
            raise ValueError(f"strategies for unknown groups {sorted(unknown)}")
        for c in self.couplings:
            if c.source not in ids or c.target not in ids:
                raise ValueError(f"coupling {c.kind} {c.source}->{c.target} names an unknown group")
        return self


def taxonomy_path(version: Literal["v1", "v2"] = "v2") -> Path:
    """``config/taxonomy/groups_<version>.yaml``."""
    return config_root() / "taxonomy" / f"groups_{version}.yaml"


class GroupRegistry:
    """Immutable runtime view of a taxonomy (§3.2). Group order is the taxonomy order and is stable."""

    __slots__ = ("_config", "_index", "_hash")

    def __init__(self, config: TaxonomyConfig) -> None:
        object.__setattr__(self, "_config", config)
        object.__setattr__(self, "_index", {g.group_id: i for i, g in enumerate(config.groups)})
        object.__setattr__(self, "_hash", content_hash(config))

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("GroupRegistry is immutable")

    @classmethod
    def load(cls, path: Path | None = None) -> GroupRegistry:
        """Load a taxonomy file (default ``config/taxonomy/groups_v2.yaml``)."""
        return cls(load_yaml(path if path is not None else taxonomy_path("v2"), TaxonomyConfig))

    @classmethod
    def for_version(cls, version: Literal["v1", "v2"]) -> GroupRegistry:
        """The packaged taxonomy of ``version`` (cached per process; every call keeps the file in the config
        audit, also after ``clear_config_audit()``)."""
        registry, record = _packaged_registry(version)
        note_config_load(record)
        return registry

    @property
    def config(self) -> TaxonomyConfig:
        return self._config

    @property
    def version(self) -> Literal["v1", "v2"]:
        return self._config.version

    @property
    def hash(self) -> str:
        """``content_hash`` of the taxonomy model (independent of YAML comments and layout)."""
        return self._hash

    def ids(self, kind: str | None = None) -> tuple[GroupId, ...]:
        """Group ids in taxonomy order, optionally filtered by ``kind``."""
        return tuple(g.group_id for g in self._config.groups if kind is None or g.kind == kind)

    def spec(self, g: str) -> GroupSpec:
        """The spec of group ``g``; ``SchemaError`` on an unknown id."""
        try:
            return self._config.groups[self._index[g]]
        except KeyError:
            raise SchemaError(f"unknown group id {g!r} in taxonomy {self.version}", {"group": g}) from None

    def index(self, g: str) -> int:
        """Column index of ``g`` in [.., G, ..] arrays."""
        if g not in self._index:
            raise SchemaError(f"unknown group id {g!r} in taxonomy {self.version}", {"group": g})
        return self._index[g]

    def private(self) -> tuple[GroupId, ...]:
        return self.ids("private")

    def red_tier(self) -> tuple[GroupId, ...]:
        return tuple(g.group_id for g in self._config.groups if g.red_tier)

    def amber_tier(self) -> tuple[GroupId, ...]:
        return tuple(g.group_id for g in self._config.groups if g.amber_tier)

    def investment(self) -> tuple[GroupId, ...]:
        """Investment groups (kind private, public or overlay); ``n_groups`` counts these."""
        return tuple(g.group_id for g in self._config.groups if g.kind in INVESTMENT_KINDS)

    def seat_groups(self) -> tuple[GroupId, ...]:
        """Groups with their own shadow-IC seat."""
        return tuple(g.group_id for g in self._config.groups if g.seat)

    @property
    def n_groups(self) -> int:
        return len(self.investment())

    @property
    def n_seats(self) -> int:
        """Shadow-IC seats: n_groups + 5 (S-ADR-22)."""
        return self.n_groups + SEATS_BEYOND_GROUPS

    def codes(self) -> tuple[str, ...]:
        return tuple(g.code for g in self._config.groups)

    def by_code(self, code: str) -> GroupSpec:
        for g in self._config.groups:
            if g.code == code:
                return g
        raise SchemaError(f"unknown group code {code!r} in taxonomy {self.version}", {"code": code})

    def strategies(self, g: str) -> tuple[str, ...]:
        self.spec(g)
        return self._config.strategies.get(GroupId(g), ())

    @property
    def couplings(self) -> tuple[CouplingSpec, ...]:
        return self._config.couplings

    def __len__(self) -> int:
        return len(self._config.groups)

    def __iter__(self) -> Iterator[GroupId]:
        return iter(self.ids())

    def __contains__(self, g: object) -> bool:
        return g in self._index

    def __repr__(self) -> str:
        return f"GroupRegistry(version={self.version!r}, groups={list(self.ids())})"


@functools.lru_cache(maxsize=2)
def _packaged_registry(version: Literal["v1", "v2"]) -> tuple[GroupRegistry, ConfigLoad]:
    config, record = load_yaml_audited(taxonomy_path(version), TaxonomyConfig)
    return GroupRegistry(config), record
