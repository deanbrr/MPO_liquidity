"""Exception hierarchy (BUILD_SPEC v1.1 §1.10).

Every exception derives from :class:`TPAError` and carries a stable ``code`` used by gates, the failure taxonomy
and the CLI exit path. Errors pickle with their code, message and context, because Windows workers run under
``spawn`` and ship exceptions back to the parent (§1.13).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Any, ClassVar

__all__ = [
    "TPAError", "SchemaError", "UnitError", "DataClassMixError", "HashMismatch", "CacheMiss", "SolverError",
    "InfeasibleError", "PinnedDualError", "PricingRefused", "EvidenceMissing", "BudgetExhausted",
    "ExecutionFailed", "SealBreach", "ReplayMiss", "ReplayDrift", "EntitlementDenied", "RunModeRefused",
    "LLMRefusal", "DSLCompileError", "CensusInfeasible", "GateFailure", "LayeringViolation", "ERROR_CODES",
    "DSL_RULES",
]

DSL_RULES: tuple[str, ...] = ("TR1", "TR2", "TR3", "TR4", "TR5", "TR6", "TR7", "TR8")


def _rebuild(cls: type[TPAError], code: str, message: str, context: dict[str, Any]) -> TPAError:
    err = cls.__new__(cls)
    TPAError.__init__(err, code, message, context)
    return err


class TPAError(Exception):
    """Base of every lab exception: ``TPAError(code, message, context)``."""

    code: str
    message: str
    context: dict[str, Any]

    def __init__(self, code: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.context = dict(context or {})

    def __reduce__(self) -> tuple[Any, ...]:
        return (_rebuild, (type(self), self.code, self.message, self.context))

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class _FixedCodeError(TPAError):
    """Errors whose code is fixed by the class (§1.10 table)."""

    CODE: ClassVar[str] = ""

    def __init__(self, message: str, context: Mapping[str, Any] | None = None) -> None:
        super().__init__(self.CODE, message, context)


class SchemaError(_FixedCodeError, ValueError):
    """Pydantic or array-spec validation fails.

    Also a ``ValueError``, so a validator that raises it inside Pydantic surfaces as a ``ValidationError``.
    """

    CODE = "SCHEMA"


class UnitError(_FixedCodeError, ValueError):
    """A unit or sign tag is wrong (also a ``ValueError``)."""

    CODE = "UNIT"


class DataClassMixError(_FixedCodeError):
    """SYNTHETIC and REAL data meet (TB7; §1.12 rule 2)."""

    CODE = "DATA_CLASS_MIX"


class HashMismatch(_FixedCodeError):
    """An engine, config, scenario, belief or snapshot hash differs from the contract."""

    CODE = "HASH_MISMATCH"


class CacheMiss(_FixedCodeError):
    """A required cache entry is missing or stale; never recompute silently."""

    CODE = "CACHE_MISS"


class SolverError(_FixedCodeError):
    """Any LP/MILP/QP status other than optimal."""

    CODE = "SOLVER_NONOPTIMAL"


class InfeasibleError(_FixedCodeError):
    """A hard problem is infeasible where feasibility is required; carries the IIS row names."""

    CODE = "INFEASIBLE"

    def __init__(self, message: str, context: Mapping[str, Any] | None = None,
                 *, iis: Sequence[str] = ()) -> None:
        ctx = dict(context or {})
        ctx.setdefault("iis", list(iis))
        super().__init__(message, ctx)

    @property
    def iis(self) -> tuple[str, ...]:
        return tuple(self.context.get("iis", ()))


class PinnedDualError(_FixedCodeError):
    """A pricing dual equals a penalty tier, fails ×10 invariance, or μ − M ≤ 0."""

    CODE = "PINNED_DUAL"


class PricingRefused(_FixedCodeError):
    """Prices or envelopes requested from a reverse stress, a pinned solve or an unsigned consent scenario."""

    CODE = "PRICING_REFUSED"


class EvidenceMissing(_FixedCodeError):
    """An EvidenceSpec does not resolve."""

    CODE = "EVIDENCE_MISSING"


class BudgetExhausted(_FixedCodeError):
    """A counted budget is spent (distinct from EXECUTION_FAILED)."""

    CODE = "BUDGET_EXHAUSTED"


class ExecutionFailed(_FixedCodeError):
    """An engine fault (paper l.6685)."""

    CODE = "EXECUTION_FAILED"


class SealBreach(_FixedCodeError):
    """Final-plane access outside the seal runner, or a canary seen."""

    CODE = "SEAL_BREACH"


class ReplayMiss(_FixedCodeError):
    """The Replay backend has no cassette for the request's structural key."""

    CODE = "REPLAY_MISS"


class ReplayDrift(_FixedCodeError):
    """A cassette matches the structural key but not the full request digest (S-ADR-41)."""

    CODE = "REPLAY_DRIFT"


class EntitlementDenied(_FixedCodeError):
    """An analyst tool call exceeds the principal's entitlements; the refusal names the rule (S-ADR-34)."""

    CODE = "ENTITLEMENT"


class RunModeRefused(_FixedCodeError):
    """A DEV/SYNTHETIC-only facility is requested in REAL mode (S-ADR-37)."""

    CODE = "RUN_MODE"


class LLMRefusal(_FixedCodeError):
    """The whole fallback chain refused."""

    CODE = "LLM_REFUSAL"


class CensusInfeasible(_FixedCodeError):
    """No plan-consistent PE history meets the census targets."""

    CODE = "CENSUS_INFEASIBLE"


class LayeringViolation(_FixedCodeError):
    """Raised by the layering test harness."""

    CODE = "LAYERING"


class DSLCompileError(TPAError):
    """A PolicySpec breaks a type rule; code ``INVALID_SPEC/TR1`` … ``INVALID_SPEC/TR8``."""

    def __init__(self, rule: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        if rule not in DSL_RULES:
            raise ValueError(f"unknown DSL type rule {rule!r}; expected one of {DSL_RULES}")
        super().__init__(f"INVALID_SPEC/{rule}", message, context)

    @property
    def rule(self) -> str:
        return self.code.split("/", 1)[1]


class GateFailure(TPAError):
    """A validation gate (V1–V24, G-A–G-E) fails; code ``GATE/<id>``."""

    def __init__(self, gate: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        if not gate or "/" in gate:
            raise ValueError(f"invalid gate id {gate!r}")
        super().__init__(f"GATE/{gate}", message, context)

    @property
    def gate(self) -> str:
        return self.code.split("/", 1)[1]


# Stable code -> class map for the fixed-code errors (the failure taxonomy reads it).
ERROR_CODES: Mapping[str, type[TPAError]] = MappingProxyType({
    cls.CODE: cls
    for cls in (SchemaError, UnitError, DataClassMixError, HashMismatch, CacheMiss, SolverError, InfeasibleError,
                PinnedDualError, PricingRefused, EvidenceMissing, BudgetExhausted, ExecutionFailed, SealBreach,
                ReplayMiss, ReplayDrift, EntitlementDenied, RunModeRefused, LLMRefusal, CensusInfeasible,
                LayeringViolation)
})
