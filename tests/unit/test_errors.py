"""contracts.errors (BUILD_SPEC v1.1 §1.10): stable codes, structured context, pickling across spawn. Owner WP-01."""

from __future__ import annotations

import pickle

import pytest

from adic_tpa.contracts import errors as E

EXPECTED = {
    E.SchemaError: "SCHEMA", E.UnitError: "UNIT", E.DataClassMixError: "DATA_CLASS_MIX",
    E.HashMismatch: "HASH_MISMATCH", E.CacheMiss: "CACHE_MISS", E.SolverError: "SOLVER_NONOPTIMAL",
    E.InfeasibleError: "INFEASIBLE", E.PinnedDualError: "PINNED_DUAL", E.PricingRefused: "PRICING_REFUSED",
    E.EvidenceMissing: "EVIDENCE_MISSING", E.BudgetExhausted: "BUDGET_EXHAUSTED",
    E.ExecutionFailed: "EXECUTION_FAILED", E.SealBreach: "SEAL_BREACH", E.ReplayMiss: "REPLAY_MISS",
    E.ReplayDrift: "REPLAY_DRIFT", E.EntitlementDenied: "ENTITLEMENT", E.RunModeRefused: "RUN_MODE",
    E.LLMRefusal: "LLM_REFUSAL", E.CensusInfeasible: "CENSUS_INFEASIBLE", E.LayeringViolation: "LAYERING",
}


@pytest.mark.parametrize(("cls", "code"), EXPECTED.items(), ids=lambda x: getattr(x, "__name__", x))
def test_fixed_codes(cls: type[E.TPAError], code: str) -> None:
    err = cls("message", {"k": 1})
    assert isinstance(err, E.TPAError) and err.code == code and err.context.items() >= {"k": 1}.items()
    assert str(err) == f"{code}: message" and E.ERROR_CODES[code] is cls


def test_parametrized_codes() -> None:
    assert E.DSLCompileError("TR2", "horizon variable").code == "INVALID_SPEC/TR2"
    assert E.DSLCompileError("TR8", "payout lever in mode B").rule == "TR8"
    with pytest.raises(ValueError):
        E.DSLCompileError("TR9", "x")
    gate = E.GateFailure("V24a", "company draw identity")
    assert gate.code == "GATE/V24a" and gate.gate == "V24a"


def test_infeasible_carries_the_iis() -> None:
    err = E.InfeasibleError("T4P infeasible", iis=("T4P:h=24", "LR8"))
    assert err.iis == ("T4P:h=24", "LR8")


def test_schema_and_unit_errors_are_value_errors() -> None:
    assert issubclass(E.SchemaError, ValueError) and issubclass(E.UnitError, ValueError)


@pytest.mark.parametrize("err", [E.HashMismatch("cube", {"expected": "a"}), E.DSLCompileError("TR1", "leak"),
                                 E.GateFailure("V6", "census"), E.InfeasibleError("x", iis=("r",)),
                                 E.TPAError("CUSTOM", "m", {"a": [1]})])
def test_errors_pickle(err: E.TPAError) -> None:
    back = pickle.loads(pickle.dumps(err))
    assert type(back) is type(err) and back.code == err.code and back.message == err.message
    assert back.context == err.context
