"""Identifier types (BUILD_SPEC v1.1 §1.8, §3.1).

Each id is a ``str`` subclass whose constructor validates the §1.8 format ("NewType(str) aliases validated on
construction"): ``HoldingId("SYN-PE-0042")`` succeeds, ``HoldingId("PE-42")`` raises ``SchemaError`` (also a
``ValueError``). Pydantic fields typed with these classes validate the same way and serialize as plain strings.

Synthetic ids carry ``SYN-``; real ids are adapter-assigned and never start with ``SYN-`` (§1.12). Which group
codes exist is configuration (S-ADR-01), so ``HoldingId`` checks only the shape ``SYN-<CODE>-<4 digits>`` and
reserves the entity-kind codes of other id types (CMP, GP, TR, CSA, FAC).
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, ClassVar, Final

from pydantic_core import core_schema

from adic_tpa.contracts.enums import DataClass
from adic_tpa.contracts.errors import SchemaError

__all__ = [
    "GroupId", "HoldingId", "UnitId", "CompanyId", "SponsorId", "TradeId", "CsaId", "FacilityId", "RunId",
    "MetricId", "DecisionId", "ContractId", "CampaignId", "ArtifactRef", "CONTENT_HASH_RE", "SYN_PREFIX",
    "RESERVED_SYN_CODES", "is_content_hash", "check_synthetic_consistency", "synthetic_holding_id", "make_run_id",
]

SYN_PREFIX: Final = "SYN-"
RESERVED_SYN_CODES: Final = frozenset({"CMP", "GP", "TR", "CSA", "FAC"})
CONTENT_HASH_RE: Final = re.compile(r"^sha256:[0-9a-f]{64}$")
_REAL_TOKEN: Final = r"(?!SYN-)\S{1,128}"
_RUN: Final = r"run-\d{8}T\d{6}Z-[0-9a-f]{8}"
_QUARTER: Final = r"\d{4}Q[1-4]"


class _ValidatedId(str):
    """A ``str`` validated against ``PATTERN`` on construction."""

    __slots__ = ()
    PATTERN: ClassVar[re.Pattern[str]]
    DESCRIPTION: ClassVar[str] = ""

    def __new__(cls, value: str) -> _ValidatedId:
        if not isinstance(value, str):
            raise SchemaError(f"{cls.__name__} must be a str, got {type(value).__name__}")
        cls._check(value)
        return super().__new__(cls, value)

    @classmethod
    def _check(cls, value: str) -> None:
        if not cls.PATTERN.fullmatch(value):
            raise SchemaError(f"invalid {cls.__name__} {value!r}: expected {cls.DESCRIPTION}")

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: Any) -> core_schema.CoreSchema:
        # The constructor validates (Python ``re``; some patterns use look-ahead, which pydantic-core's Rust
        # regex engine rejects), so the inner schema is a plain strict str.
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str, when_used="always"),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: Any) -> dict[str, Any]:
        json_schema: dict[str, Any] = handler(schema)
        json_schema["pattern"] = cls.PATTERN.pattern.replace("(?P<", "(?<")  # ECMA-262 named groups
        return json_schema

    @classmethod
    def is_valid(cls, value: object) -> bool:
        """True if ``value`` would construct without error."""
        if not isinstance(value, str):
            return False
        try:
            cls._check(value)
        except SchemaError:
            return False
        return True


class GroupId(_ValidatedId):
    """Validated group id, never a closed enum (S-ADR-01); membership is checked by ``GroupRegistry.spec``."""

    __slots__ = ()
    PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{0,31}$")
    DESCRIPTION = "an upper-case identifier such as a taxonomy group id"


class HoldingId(_ValidatedId):
    """``SYN-<GROUPCODE>-<4 digits>`` for synthetic holdings; adapter-assigned (never ``SYN-``) for real ones.

    Real ids must contain a hyphen (as every SYN id does), so holding ids and group ids are disjoint and the
    ``HoldingId | GroupId`` union of ``PackageItem.target`` is unambiguous.
    """

    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-(?P<code>[A-Z]{{2,5}})-\d{{4}}|(?=\S*-){_REAL_TOKEN})$")
    DESCRIPTION = "SYN-<GROUPCODE>-<4 digits> or a real adapter id containing '-' and not starting with SYN-"

    @classmethod
    def _check(cls, value: str) -> None:
        super()._check(value)
        m = cls.PATTERN.fullmatch(value)
        if m is not None and m.group("code") in RESERVED_SYN_CODES:
            raise SchemaError(f"invalid HoldingId {value!r}: SYN-{m.group('code')}- is reserved for another id kind")

    @property
    def is_synthetic(self) -> bool:
        return self.startswith(SYN_PREFIX)

    @property
    def group_code(self) -> str | None:
        """The SYN group code (e.g. ``PE``), None for real ids."""
        m = self.PATTERN.fullmatch(self)
        return m.group("code") if m is not None else None


class UnitId(_ValidatedId):
    """Unit id: a holding id or a cohort id (cohort formats are engine-assigned tokens without whitespace)."""

    __slots__ = ()
    PATTERN = re.compile(r"^\S{1,128}$")
    DESCRIPTION = "a holding or cohort id (no whitespace, at most 128 characters)"


class CompanyId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-CMP-\d{{6}}|{_REAL_TOKEN})$")
    DESCRIPTION = "SYN-CMP-<6 digits> or a real id"


class SponsorId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-GP-\d{{4}}|{_REAL_TOKEN})$")
    DESCRIPTION = "SYN-GP-<4 digits> or a real id"


class TradeId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-TR-\d{{5}}|{_REAL_TOKEN})$")
    DESCRIPTION = "SYN-TR-<5 digits> or a real id"


class CsaId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-CSA-\d{{2}}|{_REAL_TOKEN})$")
    DESCRIPTION = "SYN-CSA-<2 digits> or a real id"


class FacilityId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^(?:SYN-FAC-\d{{2}}|{_REAL_TOKEN})$")
    DESCRIPTION = "SYN-FAC-<2 digits> or a real id"


class RunId(_ValidatedId):
    """``run-<UTC yyyymmddThhmmssZ>-<first 8 hex of manifest hash>``."""

    __slots__ = ()
    PATTERN = re.compile(rf"^{_RUN}$")
    DESCRIPTION = "run-<yyyymmddThhmmssZ>-<8 hex>"


class MetricId(_ValidatedId):
    """Dotted lower-case, versioned: ``<family>.<name>[.<qualifier>]@v<k>``."""

    __slots__ = ()
    PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z0-9_-]+)+@v\d+$")
    DESCRIPTION = "<family>.<name>[.<qualifier>]@v<k>, e.g. tier1.t6.cp_upper@v1"


class DecisionId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^dec-[A-Za-z0-9]+-{_QUARTER}-\d+$")
    DESCRIPTION = "dec-<register_id>-<quarter>-<n>"


class ContractId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^ctr-{_QUARTER}-v\d+$")
    DESCRIPTION = "ctr-<quarter>-v<n>"


class CampaignId(_ValidatedId):
    __slots__ = ()
    PATTERN = re.compile(rf"^cmp-{_QUARTER}-\d+$")
    DESCRIPTION = "cmp-<quarter>-<n>"


class ArtifactRef(_ValidatedId):
    """``<run_id>:<artifact>:<json-pointer>`` (RFC 6901 pointer, possibly empty)."""

    __slots__ = ()
    PATTERN = re.compile(rf"^(?P<run_id>{_RUN}):(?P<artifact>[A-Za-z0-9_.-]+):(?P<pointer>(?:/[^/]*)*)$")
    DESCRIPTION = "<run_id>:<artifact>:<json-pointer>"

    @classmethod
    def make(cls, run_id: str, artifact: str, pointer: str = "") -> ArtifactRef:
        return cls(f"{run_id}:{artifact}:{pointer}")

    def _parts(self) -> re.Match[str]:
        m = self.PATTERN.fullmatch(self)
        assert m is not None  # validated on construction
        return m

    @property
    def run_id(self) -> RunId:
        return RunId(self._parts().group("run_id"))

    @property
    def artifact(self) -> str:
        return self._parts().group("artifact")

    @property
    def pointer(self) -> str:
        return self._parts().group("pointer")


def is_content_hash(value: object) -> bool:
    """True for ``sha256:<64 hex>`` (§1.8 content hash)."""
    return isinstance(value, str) and CONTENT_HASH_RE.fullmatch(value) is not None


def check_synthetic_consistency(is_synthetic: bool, data_class: DataClass, *ids: str | None) -> None:
    """Enforce §1.12 rule 1: ``is_synthetic == (data_class == SYNTHETIC)`` and synthetic ids carry ``SYN-``.

    Raises ``SchemaError`` (a ``ValueError``, so model validators surface it as a ``ValidationError``).
    """
    if is_synthetic != (data_class == DataClass.SYNTHETIC):
        raise SchemaError(f"is_synthetic={is_synthetic} disagrees with data_class={data_class.value}")
    for ident in ids:
        if ident is None:
            continue
        if ident.startswith(SYN_PREFIX) != is_synthetic:
            raise SchemaError(f"id {ident!r} {'lacks' if is_synthetic else 'carries'} the SYN- prefix "
                              f"for a {'SYNTHETIC' if is_synthetic else 'REAL'} row")


def synthetic_holding_id(code: str, n: int) -> HoldingId:
    """``SYN-<code>-<n:04d>``; the code comes from the taxonomy (``GroupSpec.code``)."""
    return HoldingId(f"{SYN_PREFIX}{code}-{n:04d}")


def make_run_id(created_at: datetime, manifest_hash: str) -> RunId:
    """Run id from a creation time (converted to UTC; naive means UTC) and a ``sha256:`` manifest hash."""
    if not is_content_hash(manifest_hash):
        raise SchemaError(f"manifest hash must be sha256:<64 hex>, got {manifest_hash!r}")
    utc = created_at.replace(tzinfo=timezone.utc) if created_at.tzinfo is None else created_at.astimezone(timezone.utc)
    return RunId(f"run-{utc.strftime('%Y%m%dT%H%M%SZ')}-{manifest_hash[7:15]}")
