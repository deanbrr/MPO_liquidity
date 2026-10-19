"""AnalysisContract validators (BUILD_SPEC v1.1 §3.14; ARCH §10.1): one test per rule. Owner WP-01."""

from __future__ import annotations

import copy
import json
from typing import Any

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.contract import DEV_TEST_SIGNER_HASH, AnalysisContract, ObjectiveSpec
from adic_tpa.contracts.enums import ConsentScenario
from adic_tpa.contracts.errors import PricingRefused, RunModeRefused

H64 = "sha256:" + "0" * 64


def signoff(role: str, method: str = "dev_test_key") -> dict[str, Any]:
    return {"role": role, "signer_hash": H64, "signed_at": "2026-10-18T09:00:00Z", "object_hash": H64,
            "method": method, "signature": "00"}


def conventions(revolver: float) -> dict[str, Any]:
    return {"revolver_credit": revolver, "credit_cash_a": {"PRIVCREDIT": 0.10, "CAPSOL": 0.07},
            "commitment_split": {"PE": 0.5, "SECONDARIES": 0.1, "CAPSOL": 0.1, "COINVEST": 0.1, "PRIVCREDIT": 0.1,
                                 "REALASSETS": 0.1},
            "real_assets": {"noi_yield_mult": 0.8, "refi_spread_stress_a": 0.02, "refi_ltv_cap": 0.5}}


def recovery(mode: str) -> dict[str, Any]:
    return {"mode": mode, "u_star_bn": 1.0 if mode == "STRUCT_RECOVERY" else 0.0, "d0_bn": 2.0, "iis": ["T4P:h=24"],
            "glide": {"kind": "structural" if mode == "STRUCT_RECOVERY" else "execution",
                      "g_bn": [2.0, 1.5, 1.0, 0.5, 0.0], "recovery_hash": H64},
            "board_signoff_required": mode == "STRUCT_RECOVERY", "owner_signoff_required": False}


BASE: dict[str, Any] = {
    "contract_id": "ctr-2026Q4-v1", "version": 1, "quarter": "2026Q4", "data_class": "SYNTHETIC", "census_id": "v1.1",
    "mode": "NORMAL", "recovery": None, "pricing_scenario": "R0",
    "signoffs": [signoff("CIO"), signoff("CRO")], "frozen_questions": [],
    "objective": {"target_anchor_date": "2026-09-30", "target_anchor_wealth_bn": 177.0,
                  "model_weights": {"M1": 0.5, "M6": 0.5}},
    "tier1": {"t6_bands": {"M1_M5": [0.005, 0.01, 0.02], "MIX": [0.005, 0.01, 0.02], "M6": [None, 0.025, 0.05]},
              "theta_star": 0.58, "conventions": {"pricing": conventions(0.5), "research": conventions(0.8)},
              "t5": {"recourse_debt_target": 0.10, "recourse_debt_hard": 0.15}},
    "floor": {},
    "actions": {"lenses_by_group": {"PE": ["SELL", "HOLD", "PACE"]}, "instrument_whitelist": ["lp_sale"],
                "idea_kinds": ["policy_residual", "action_package"]},
    "anchor": {"kind": "native", "name": "P0", "params_hash": H64},
    "controls": [{"kind": "native", "name": "HOLD", "params_hash": H64}],
    "planes": {"search_worlds": ["M1", "M6", "B1"], "final_worlds": ["M1", "M6", "B2"], "misspec": [],
               "seal_commitment": H64, "windows": {"calibration": ["1990-01-01", "2015-12-31"]}},
    "gates": {"eps_mat_bp": {"overlay": 5.0, "pacing": 5.0, "refi_lever": 5.0, "sell": 5.0, "other": 5.0},
              "mde_max_bp": 10.0, "ni_worlds_search": ["M1", "M6", "B1"], "ni_worlds_final": ["M1", "M6", "B2"],
              "ni_comparator": "HOLD", "miss_fd_cost_ratio": 1.0},
    "budgets": {},
    "operating_points": [{"name": "base", "t6_eps": 0.01, "floor": 0.07, "tail_budget_a": 0.0015, "leverage_max": 1.3}],
    "llm_policy": {"mode": "offline", "provider": "anthropic", "roles": []},
    "raci": {"owners": {"liquidity": "TREASURER"}},
    "root_seed": 20261018, "run_mode": "DEV_SYNTHETIC",
    "engine_hash": H64, "config_hash": H64, "snapshot_hash": H64, "scenario_hashes": {"search:M1": H64},
    "taxonomy_hash": H64,
}


def build(**changes: Any) -> AnalysisContract:
    data = copy.deepcopy(BASE)
    for dotted, value in changes.items():
        node = data
        *path, last = dotted.split("__")
        for key in path:
            node = node[key]
        node[last] = value
    return AnalysisContract.model_validate_json(json.dumps(data))


def test_baseline_contract_is_valid() -> None:
    c = build()
    assert c.cards_allowed() and c.highest_signed_scenario() is ConsentScenario.R0
    assert c.tier1.conventions.pricing.revolver_credit == 0.5
    c.require_pricing_allowed()


def test_owner_signoff_required_iff_mandate_not_b() -> None:
    with pytest.raises(ValidationError, match="owner_signoff is required"):
        build(purpose="OWNER_PROPOSAL", mandate_mode="H")
    ok = build(purpose="OWNER_PROPOSAL", mandate_mode="H", owner_signoff=signoff("OWNER"))
    assert ok.owner_signoff is not None
    with pytest.raises(ValidationError, match="only when mandate_mode != B"):
        build(owner_signoff=signoff("OWNER"))
    with pytest.raises(ValidationError, match="signed by the OWNER"):
        build(purpose="OWNER_PROPOSAL", mandate_mode="H", owner_signoff=signoff("CIO"))


def test_decision_contracts_use_mandate_b_only() -> None:
    with pytest.raises(ValidationError, match="only mandate mode in DECISION"):
        build(mandate_mode="H", owner_signoff=signoff("OWNER"))


def test_owner_proposal_cannot_feed_cards() -> None:
    c = build(purpose="OWNER_PROPOSAL", mandate_mode="A", owner_signoff=signoff("OWNER"))
    assert not c.cards_allowed()
    with pytest.raises(PricingRefused):
        c.require_pricing_allowed()


def test_structural_recovery_requires_board_signoff() -> None:
    kw = {"mode": "STRUCT_RECOVERY", "recovery": recovery("STRUCT_RECOVERY"), "gates__ni_comparator": "RESTORED_BASELINE"}
    with pytest.raises(ValidationError, match="BOARD"):
        build(**kw)
    ok = build(**kw, signoffs=[signoff("CIO"), signoff("CRO"), signoff("BOARD")])
    assert ok.mode.value == "STRUCT_RECOVERY"


def test_ni_comparator_restored_iff_recovery() -> None:
    with pytest.raises(ValidationError, match="ni_comparator"):
        build(gates__ni_comparator="RESTORED_BASELINE")
    with pytest.raises(ValidationError, match="ni_comparator"):
        build(mode="EXEC_RECOVERY", recovery=recovery("EXEC_RECOVERY"))
    ok = build(mode="EXEC_RECOVERY", recovery=recovery("EXEC_RECOVERY"), gates__ni_comparator="RESTORED_BASELINE")
    assert ok.gates.ni_comparator == "RESTORED_BASELINE"


def test_recovery_mode_carries_its_plan() -> None:
    with pytest.raises(ValidationError, match="RecoveryPlan"):
        build(mode="EXEC_RECOVERY", gates__ni_comparator="RESTORED_BASELINE")


def test_r1_pricing_needs_a_signed_revolver() -> None:
    with pytest.raises(ValidationError, match="highest signed scenario"):
        build(pricing_scenario="R1")
    revolver = {"lever_id": "SYN-FAC-01", "consent_scenario": "R1", "signoff": signoff("TREASURER")}
    ok = build(pricing_scenario="R1", lever_signoffs=[revolver])
    assert ok.highest_signed_scenario() is ConsentScenario.R1


def test_r2_pricing_needs_the_owner_band_in_mode_h() -> None:
    revolver = {"lever_id": "SYN-FAC-01", "consent_scenario": "R1", "signoff": signoff("TREASURER")}
    band = {"lever_id": "owner_band", "consent_scenario": "R2", "signoff": signoff("OWNER")}
    with pytest.raises(ValidationError, match="highest signed scenario"):
        build(pricing_scenario="R2", lever_signoffs=[revolver, band])            # mandate B
    ok = build(pricing_scenario="R2", lever_signoffs=[revolver, band], purpose="OWNER_PROPOSAL", mandate_mode="H",
               owner_signoff=signoff("OWNER"))
    assert ok.highest_signed_scenario() is ConsentScenario.R2
    with pytest.raises(ValidationError, match="OWNER"):
        build(lever_signoffs=[{"lever_id": "owner_band", "consent_scenario": "R2", "signoff": signoff("CIO")}])


def test_shortfall_exponent_must_exceed_one() -> None:
    with pytest.raises(ValidationError, match="shortfall_exponent"):
        build(objective__shortfall_exponent=1.0)
    assert build(objective__shortfall_exponent=1.5).objective.shortfall_exponent == 1.5


def test_model_weights_sum_to_one_and_exclude_b_worlds() -> None:
    with pytest.raises(ValidationError, match="sum to 1"):
        build(objective__model_weights={"M1": 0.5, "M6": 0.4})
    with pytest.raises(ValidationError, match="B1/B2"):
        build(objective__model_weights={"M1": 0.5, "B1": 0.5})
    with pytest.raises(ValidationError):
        build(objective__model_weights={"X9": 1.0})                              # not a world id


def test_theta_star_is_set() -> None:
    data = copy.deepcopy(BASE)
    del data["tier1"]["theta_star"]
    with pytest.raises(ValidationError, match="theta_star"):
        AnalysisContract.model_validate_json(json.dumps(data))
    with pytest.raises(ValidationError, match="theta_star"):
        build(tier1__theta_star=1.5)


def test_real_mode_refuses_dev_signer_and_dev_mode_refuses_real_data() -> None:
    with pytest.raises(RunModeRefused, match="dev_test_key") as exc:
        build(run_mode="REAL")
    assert exc.value.code == "RUN_MODE"
    ok = build(run_mode="REAL", signoffs=[signoff("CIO", "ed25519_dpapi"), signoff("CRO", "ed25519_dpapi")])
    assert ok.run_mode.value == "REAL"
    with pytest.raises(RunModeRefused, match="DEV_SYNTHETIC") as exc:
        build(data_class="REAL")
    assert exc.value.code == "RUN_MODE"


def test_real_mode_refuses_a_relabelled_dev_signoff() -> None:
    """Review R07: the method label is not signed, so the rule keys on the DEV signer's identity too."""
    relabelled = dict(signoff("CIO", "ed25519_dpapi"), signer_hash=DEV_TEST_SIGNER_HASH)
    with pytest.raises(RunModeRefused, match="dev_test_key"):
        build(run_mode="REAL", signoffs=[relabelled, signoff("CRO", "ed25519_dpapi")])
    band = {"lever_id": "SYN-FAC-01", "consent_scenario": "R1", "signoff": relabelled}
    with pytest.raises(RunModeRefused):                                         # lever sign-offs are covered too
        build(run_mode="REAL", signoffs=[signoff("CIO", "ed25519_dpapi")], lever_signoffs=[band])
    assert build(signoffs=[relabelled]).run_mode.value == "DEV_SYNTHETIC"       # DEV mode accepts it


def test_recovery_plan_mode_must_equal_the_contract_mode() -> None:
    with pytest.raises(ValidationError, match="RecoveryPlan of that mode"):
        build(mode="EXEC_RECOVERY", recovery=recovery("STRUCT_RECOVERY"), gates__ni_comparator="RESTORED_BASELINE",
              signoffs=[signoff("CIO"), signoff("CRO"), signoff("BOARD")])


def test_model_weights_must_be_non_negative() -> None:
    with pytest.raises(ValidationError, match="non-negative"):
        build(objective__model_weights={"M1": 1.5, "M6": -0.5})                 # sums to 1, one weight negative


def test_quarter_format() -> None:
    with pytest.raises(ValidationError, match="2026Q4"):
        build(quarter="2026-Q4")


def test_b2_is_final_plane_only() -> None:
    with pytest.raises(ValidationError, match="B2"):
        build(planes__search_worlds=["M1", "B2"])


def test_objective_spec_defaults() -> None:
    spec = ObjectiveSpec.model_validate_json(json.dumps(BASE["objective"]))
    assert (spec.gamma, spec.lambda_T, spec.shortfall_exponent, spec.target_annual) == (3.0, 1.0, 2.0, 0.10)
