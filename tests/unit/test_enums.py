"""contracts.enums (BUILD_SPEC v1.1 §3.1). Owner WP-01."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from adic_tpa.contracts import enums as E


def test_flow_types() -> None:
    assert len(E.FlowType) == E.N_FLOW_TYPES == 18
    assert [ft.value for ft in E.FlowType] == list(range(18))
    assert E.FlowType.sign(E.FlowType.CALL) == -1 and E.FlowType.DISTRIBUTION.sign() == 1
    assert E.FlowType.VM.sign() == 0 and E.FlowType.INTEREST_ON_CASH.sign() == 0
    assert not E.FlowType.is_cash(E.FlowType.PIK_ACCRUAL)
    assert all(ft.is_cash() for ft in E.FlowType if ft is not E.FlowType.PIK_ACCRUAL)
    negatives = {ft.name for ft in E.FlowType if ft.sign() < 0}
    assert negatives == {"CALL", "FEES", "PREMIUM", "DEBT_REPAY", "DEBT_SERVICE", "CAPEX", "OWNER_DRAW", "OPEX"}
    positives = {ft.name for ft in E.FlowType if ft.sign() > 0}
    assert positives == {"DISTRIBUTION", "INCOME_CASH", "PIK_ACCRUAL", "SALE_PROCEEDS", "MONETIZATION",
                         "REDEMPTION_PAY", "DEBT_DRAW"}


def test_flow_type_lookups_accept_plain_int_codes() -> None:
    """§3.1 calls them table lookups ``FlowType.sign(ft)``: a code from an int8 array works like the member."""
    assert E.FlowType.sign(0) == -1 and E.FlowType.sign(1) == 1 and E.FlowType.sign(6) == 0
    assert E.FlowType.is_cash(3) is False and E.FlowType.is_cash(17) is True
    assert [E.FlowType.sign(int(ft)) for ft in E.FlowType] == list(E.FLOW_SIGNS)
    for bad in (18, -1):
        with pytest.raises(ValueError):
            E.FlowType.sign(bad)


def test_consent_scenarios_order_by_rank() -> None:
    order = [E.ConsentScenario.R0X, E.ConsentScenario.R0, E.ConsentScenario.R1, E.ConsentScenario.R2]
    assert sorted(reversed(order)) == order
    assert E.ConsentScenario.R0X < E.ConsentScenario.R0 < E.ConsentScenario.R1 < E.ConsentScenario.R2
    assert E.ConsentScenario.R2 >= E.ConsentScenario.R1 and E.ConsentScenario.R0 <= "R1"
    assert max(order) is E.ConsentScenario.R2 and E.ConsentScenario.R0X.value == "R0x"


def test_explicit_values() -> None:
    assert E.MandateMode.B_OWNER_CALL.value == "B" and E.ContractMode.EXECUTION_RECOVERY.value == "EXEC_RECOVERY"
    assert E.PricedOn.RESTORED.value == "restored_problem" and E.EvidencePlane.SEALED.value == "sealed"
    assert int(E.CFPStage.BLACK) == 3 and int(E.ShockType.GW) == 5 and int(E.FinWindow.CLOSED) == 2
    assert int(E.HFLotState.TRS_TERM) == 10 and int(E.CreditState.REPAID) == 8
    assert E.AnswerStatus.EXPLORATORY < E.AnswerStatus.BASELINE < E.AnswerStatus.SEARCH < E.AnswerStatus.QUALIFIED
    assert min(E.AnswerStatus.SEARCH, E.AnswerStatus.EXPLORATORY) is E.AnswerStatus.EXPLORATORY


def test_shorthand_str_enums_use_their_names() -> None:
    for enum in (E.Lens, E.Plane, E.RecourseTier, E.Clock, E.RunMode, E.DataClass, E.MarkType, E.Book,
                 E.RowFamily, E.GateLabel, E.FailureLabel, E.OptionKind, E.RoleId, E.CampaignState):
        assert all(m.value == m.name for m in enum), enum.__name__
    assert len(E.RowFamily) == 32 and "ANALYST" in E.RoleId.__members__


def test_enums_the_spec_spells_in_lower_case() -> None:
    """S-ADR-35 / §1.2 factor kinds, S-ADR-06 ``target_mode = "precommitted"``, §7.1 ``TPA_LLM_MODE``."""
    assert [k.value for k in E.FactorKind] == ["logret", "level", "change"]
    assert E.FactorKind("logret") is E.FactorKind.LOGRET and E.FactorKind("level") is E.FactorKind.LEVEL
    assert [m.value for m in E.TargetMode] == ["precommitted", "rolling"]
    assert E.TargetMode("precommitted") is E.TargetMode.PRECOMMITTED
    assert [m.value for m in E.LLMMode] == ["offline", "replay", "live"]
    with pytest.raises(ValueError):
        E.FactorKind("LOGRET")                                               # one spelling in config files


@pytest.mark.parametrize(("raw", "member"), [("offline", "OFFLINE"), ("OFFLINE", "OFFLINE"), ("Replay", "REPLAY"),
                                             (" live ", "LIVE")])
def test_llm_mode_maps_tpa_llm_mode_case_insensitively(raw: str, member: str) -> None:
    assert E.LLMMode(raw) is E.LLMMode[member]


def test_llm_mode_rejects_unknown_values_and_validates_in_models() -> None:
    from adic_tpa.contracts.contract import LLMSpec

    for bad in ("stub", "", 1):
        with pytest.raises(ValueError):
            E.LLMMode(bad)
    spec = LLMSpec.model_validate_json('{"mode": "LIVE", "provider": "anthropic", "roles": []}')
    assert spec.mode is E.LLMMode.LIVE and spec.model_dump(mode="json")["mode"] == "live"


def test_recourse_tiers_nest() -> None:
    assert [t.value for t in E.RECOURSE_TIER_ORDER] == ["T", "TP", "TPF", "TPFA", "ALL"]


def test_world_ids() -> None:
    for wid in ("M1", "M6", "B1", "B2", "MS:fat_tails_v2"):
        assert E.check_world_id(wid) == wid
    for bad in ("M7", "B3", "MS:", "m1", "MS:bad name"):
        with pytest.raises(ValueError):
            E.check_world_id(bad)


def test_small_value_models() -> None:
    assert E.Interval.model_validate_json('{"lo": -1, "hi": 2}').hi == 2.0
    with pytest.raises(ValidationError):
        E.Interval(lo=1.0, hi=0.0)
    kv = E.KeyValue.model_validate_json(json.dumps({"key": "M1", "value": 0.5}))
    assert kv.value == 0.5
    assert E.ReturnBasis.model_validate_json('{"kind": "geom", "fees": "gross"}').kind == "geom"
