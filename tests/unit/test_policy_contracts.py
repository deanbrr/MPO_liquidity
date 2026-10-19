"""Policy contracts (BUILD_SPEC v1.1 §3.11; S-ADR-13, -30). Owner WP-01."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.lab import IdeaBundle
from adic_tpa.contracts.policy import ActionPackage, PolicyRef, PolicySpec, RECOURSE_RUNGS, RecourseOrder
from adic_tpa.contracts.tools import VariantSet

ANCHOR = "P0@sha256:" + "a" * 64
RESIDUAL = {"slot": "reserve_target", "form": "add_clip", "lo": 0.0, "hi": 0.2,
            "features": [{"var": "F_t", "lag": 1, "xforms": ["logit"]}],
            "box": [{"lo": -0.5, "hi": 0.5}], "gate_id": "g1"}
OVERLAY = {"template": "put_spread_ladder", "sleeve": "TAIL",
           "legs": [{"template": "put", "strike_rel": 0.9, "expiry_months": 6, "notional_bn": 1.0, "side": "long"}]}


def test_policy_spec_hash_is_content_addressed() -> None:
    spec = PolicySpec.model_validate_json(json.dumps({"anchor": ANCHOR, "residuals": [RESIDUAL]}))
    same = PolicySpec.model_validate_json(json.dumps({"residuals": [RESIDUAL], "anchor": ANCHOR}))
    other = PolicySpec.model_validate_json(json.dumps({"anchor": ANCHOR}))
    assert spec.spec_hash == same.spec_hash != other.spec_hash and spec.spec_hash.startswith("sha256:")
    assert spec.spec_hash == content_hash(spec)                               # one identity per spec
    assert "spec_hash" not in spec.model_dump() and "spec_hash" not in json.loads(spec.model_dump_json())
    with pytest.raises(ValidationError):                                      # derived, so never input
        PolicySpec.model_validate_json(json.dumps({"anchor": ANCHOR, "spec_hash": spec.spec_hash}))


def test_policy_spec_and_its_carriers_round_trip_through_json() -> None:
    """Review R01: S-ADR-39 validates MCP payloads and registry rows with model_validate_json."""
    spec = PolicySpec.model_validate_json(json.dumps(
        {"anchor": ANCHOR, "residuals": [RESIDUAL], "overlays": [OVERLAY], "mandate_mode": "B"}))
    assert PolicySpec.model_validate_json(spec.model_dump_json()) == spec
    bundle = IdeaBundle.model_validate_json(json.dumps({
        "idea_id": "i1", "title": "t", "worker": 1, "cycle": 1, "kind": "policy_residual", "hypothesis": "h",
        "mechanism_refs": [], "implementation_plan": ["p"], "spec": json.loads(spec.model_dump_json()),
        "target_rubrics": [{"kind": "metric", "text": "m"}, {"kind": "implementation", "text": "i"}],
        "predicted_effect": {"metric_id": "j.delta_ce_bp@v1", "direction": "up", "size_bp": 1.0,
                             "interval_bp": {"lo": 0.0, "hi": 2.0}},
        "assumptions": []}))
    assert IdeaBundle.model_validate_json(bundle.model_dump_json()) == bundle
    variants = VariantSet(variants=(spec, bundle.spec), rationale=("a", "b"))
    back = VariantSet.model_validate_json(variants.model_dump_json())
    assert back == variants and back.variants[0].spec_hash == spec.spec_hash


def test_policy_spec_limits() -> None:
    with pytest.raises(ValidationError, match="anchor"):
        PolicySpec.model_validate_json(json.dumps({"anchor": "P0"}))
    with pytest.raises(ValidationError, match="at most 6"):
        PolicySpec.model_validate_json(json.dumps({"anchor": ANCHOR, "residuals": [RESIDUAL] * 7}))
    with pytest.raises(ValidationError, match="1..3 features"):
        PolicySpec.model_validate_json(json.dumps({"anchor": ANCHOR, "residuals": [dict(RESIDUAL, features=[])]}))


def test_action_package_one_lens_per_asset() -> None:
    item = {"target": "SYN-PE-0042", "lens": "SELL", "instrument": "lp_sale", "size_frac": 0.5}
    pkg = ActionPackage.model_validate_json(json.dumps({"items": [item, dict(item, target="PE", lens="PACE")]}))
    assert type(pkg.items[1].target).__name__ == "GroupId" and type(pkg.items[0].target).__name__ == "HoldingId"
    with pytest.raises(ValidationError, match="one lens per asset"):
        ActionPackage.model_validate_json(json.dumps({"items": [item, dict(item, lens="REFINANCE")]}))
    with pytest.raises(ValidationError, match="12"):
        ActionPackage.model_validate_json(json.dumps(
            {"items": [dict(item, target=f"SYN-PE-{i:04d}") for i in range(13)]}))


def test_recourse_order_is_a_permutation_without_preemptive_rung() -> None:
    order = RecourseOrder.model_validate_json(json.dumps({"rungs": ["liquid", "reserve", "p2s", "facility", "amber", "red"]}))
    assert order.codes() == (2, 0, 1, 3, 4, 5) and RECOURSE_RUNGS[2] == "liquid"
    with pytest.raises(ValidationError):
        RecourseOrder.model_validate_json(json.dumps({"rungs": ["reserve", "p2s", "liquid", "facility", "amber",
                                                                "preemptive"]}))
    with pytest.raises(ValidationError, match="permutation"):
        RecourseOrder.model_validate_json(json.dumps({"rungs": ["reserve", "reserve", "liquid", "facility", "amber", "red"]}))
    with pytest.raises(ValidationError, match="switch_on"):
        RecourseOrder.model_validate_json(json.dumps({"rungs": list(RECOURSE_RUNGS), "switch_on": "drought"}))
    switch = RecourseOrder.model_validate_json(json.dumps(
        {"rungs": list(RECOURSE_RUNGS), "switch_on": "drought", "alt_rungs": list(reversed(RECOURSE_RUNGS)),
         "switch_threshold": 0.5}))
    assert switch.codes(alternative=True) == (5, 4, 3, 2, 1, 0)


def test_policy_refs() -> None:
    assert PolicyRef.model_validate_json('{"kind": "native", "name": "LIQUID_FIRST", "params_hash": "h"}').name
    with pytest.raises(ValidationError, match="unknown native policy"):
        PolicyRef.model_validate_json('{"kind": "native", "name": "YOLO", "params_hash": "h"}')
    with pytest.raises(ValidationError, match="spec_hash"):
        PolicyRef.model_validate_json('{"kind": "spec", "name": "idea-7", "params_hash": "h"}')
