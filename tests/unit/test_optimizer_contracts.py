"""Optimizer contracts (BUILD_SPEC v1.1 §3.12, §3.17, §5.8): nested lever sets, typed row and column keys, the
DualSet ℓ invariant. Owner WP-01."""

from __future__ import annotations

import json

import numpy as np
import pytest

from adic_tpa.contracts.enums import ConsentScenario, RowFamily
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.optimizer import ColKey, DualSet, LeverSet, RowKey

SCENARIOS = [ConsentScenario.R0X, ConsentScenario.R0, ConsentScenario.R1, ConsentScenario.R2]


def _lever(lever_id: str, scenario: ConsentScenario) -> dict:
    return {"lever_id": lever_id, "owner_group": "CF", "reversible": True, "consent_scenario": scenario.value,
            "cap_bn": 1.0, "cost": 0.0, "slope": [0.0] * 24}


LEVERS = LeverSet.model_validate_json(json.dumps({"levers": [_lever(f"l_{s.value}", s) for s in reversed(SCENARIOS)]}))


@pytest.mark.parametrize(("scenario", "expected"), [
    (ConsentScenario.R0X, {"l_R0x"}),
    (ConsentScenario.R0, {"l_R0x", "l_R0"}),
    (ConsentScenario.R1, {"l_R0x", "l_R0", "l_R1"}),
    (ConsentScenario.R2, {"l_R0x", "l_R0", "l_R1", "l_R2"}),
])
def test_lever_sets_nest(scenario: ConsentScenario, expected: set[str]) -> None:
    """R0x ⊂ R0 ⊂ R1 ⊂ R2: a lever is usable in its own scenario and every larger one."""
    assert {lv.lever_id for lv in LEVERS.available(scenario)} == expected


def test_available_keeps_lever_order() -> None:
    assert [lv.lever_id for lv in LEVERS.available(ConsentScenario.R2)] == ["l_R2", "l_R1", "l_R0", "l_R0x"]


@pytest.mark.parametrize("key", [
    ColKey(family="decision", name="sell", node=3, idx=(("g", "PE"), ("h", 7))),
    ColKey(family="state", name="cash"),
    ColKey(family="lens", name="lever", node=0),
    ColKey(family="elastic", name="t4p_up", idx=(("h", 24),)),
])
def test_col_key_string_round_trip(key: ColKey) -> None:
    text = str(key)
    assert ColKey.parse(text) == key and str(ColKey.parse(text)) == text


def test_col_key_canonical_form() -> None:
    assert str(ColKey(family="decision", name="sell", node=3, idx=(("h", 7),))) == "decision:sell@3:h=07"


@pytest.mark.parametrize("bad", ["decision", "bogus:sell", "decision:sell@x", "decision:sell:noeq", "decision:bad name",
                                 "decision:sell:h=a b", ""])
def test_malformed_col_keys_raise_schema_error(bad: str) -> None:
    with pytest.raises(SchemaError):
        ColKey.parse(bad)


@pytest.mark.parametrize("bad", ["NOPE:h=1", "T4P:h", "T4P:h=a b", "T4P:bad key=1", "T4P:h=07:h2=1.5x!"])
def test_malformed_row_keys_raise_schema_error(bad: str) -> None:
    with pytest.raises(SchemaError):
        RowKey.parse(bad)


def test_row_key_parse_still_round_trips() -> None:
    key = RowKey(family=RowFamily.LR4, idx=(("g", "PE"), ("h", 24)))
    assert RowKey.parse(str(key)) == key


def _duals(ell: list[float], mu: list[float], m: list[float]) -> DualSet:
    return DualSet(pi_row=np.zeros(2), mu_cash=np.array(mu), M_cash=np.array(m), ell=np.array(ell), quality={})


def test_dual_set_ell_is_non_negative_where_mu_exceeds_m() -> None:
    """§3.17: ℓ ≥ 0 wherever μ − M > 0 (review R13)."""
    _duals([0.25, 0.0], [1.0, 1.0], [0.2, 0.0]).validate()
    _duals([0.25, -3.0], [1.0, 0.5], [0.2, 0.5]).validate()          # μ − M = 0 at node 1: ℓ undefined
    with pytest.raises(SchemaError, match="ell"):
        _duals([0.25, -0.1], [1.0, 1.0], [0.2, 0.0]).validate()
