"""Every contracts model round-trips through its own JSON (BUILD_SPEC v1.1 S-ADR-39; review WP01-R01). Owner WP-01.

S-ADR-39 validates registry rows, MCP payloads and config files in Pydantic JSON mode, so for every model
``model_validate_json(obj.model_dump_json()) == obj`` must hold. Instances come from a minimal-payload generator
driven by each model's JSON schema (required properties only; ``null`` for nullable fields; the first enum value;
empty containers; the example below for each id pattern), with per-model patches where a validator needs specific
values. A model that serializes a field its own validation rejects (R01: a computed field under
``extra="forbid"``) fails here. SYNTHETIC values only.
"""

from __future__ import annotations

import importlib
import json
import pkgutil
import sys
from collections.abc import Callable
from typing import Any

import pytest
from pydantic import BaseModel

import adic_tpa.contracts as contracts_pkg
from adic_tpa.contracts import ids as I
from adic_tpa.contracts.analyst import ANALYST_TOOLS, DraftScenarioViewIn, ToolResult, WhatIfBundle
from adic_tpa.contracts.enums import ContractModel
from adic_tpa.contracts.evidence import REQUIRED_TERMINAL_SERIES
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.policy import RECOURSE_RUNGS
from adic_tpa.contracts.taxonomy import GroupSpec
from adic_tpa.contracts.world import PanelRow

for _info in pkgutil.iter_modules(contracts_pkg.__path__):
    importlib.import_module(f"adic_tpa.contracts.{_info.name}")


def _subclasses(cls: type) -> list[type]:
    out, todo = [], list(cls.__subclasses__())
    while todo:
        c = todo.pop()
        out.append(c)
        todo.extend(c.__subclasses__())
    return out


def _exported(c: type) -> bool:
    return c.__module__.startswith("adic_tpa.") and getattr(sys.modules[c.__module__], c.__name__, None) is c


MODELS = sorted({c for c in _subclasses(ContractModel) if "[" not in c.__name__ and _exported(c)},
                key=lambda c: (c.__module__, c.__name__))
TOOL_RESULTS = sorted({ToolResult[t.payload_model] for t in ANALYST_TOOLS}, key=lambda m: m.__name__)

ID_EXAMPLES: dict[type[I._ValidatedId], str] = {
    I.GroupId: "PE", I.HoldingId: "SYN-PE-0001", I.UnitId: "SYN-PE-0001", I.CompanyId: "SYN-CMP-000001",
    I.SponsorId: "SYN-GP-0001", I.TradeId: "SYN-TR-00001", I.CsaId: "SYN-CSA-01", I.FacilityId: "SYN-FAC-01",
    I.RunId: "run-20261018T091500Z-3f2a9c1d", I.MetricId: "tier1.t6.cp_upper@v1",
    I.DecisionId: "dec-Q1-2026Q4-1", I.ContractId: "ctr-2026Q4-v1", I.CampaignId: "cmp-2026Q4-1",
    I.ArtifactRef: "run-20261018T091500Z-3f2a9c1d:cards:/0",
}
BY_PATTERN = {cls.PATTERN.pattern.replace("(?P<", "(?<"): ex for cls, ex in ID_EXAMPLES.items()}


def _override_draft(p: dict[str, Any]) -> dict[str, Any]:
    spec = DraftScenarioViewIn.model_validate_json(json.dumps(p["spec"]))
    return {**p, "spec_hash": content_hash(spec), "expires_at": "2026-10-18T09:30:00Z"}


def _whatif_bundle(p: dict[str, Any]) -> dict[str, Any]:
    # the raw JSON forms (lists, "Z" timestamps, plain strings) hash like the validated values; validation checks it
    assert set(p) | {"bundle_hash"} == set(WhatIfBundle.model_fields)
    return {**p, "bundle_hash": content_hash({k: v for k, v in p.items() if k != "bundle_hash"})}


Patch = dict[str, Any] | Callable[[dict[str, Any]], dict[str, Any]]
# Values a model's own validators require (keyed by class name, applied wherever the model is generated).
PATCHES: dict[str, Patch] = {
    "LensAction": {"lens": "HOLD"},
    "DraftBundleIn": {"override_ids": ["o1"], "outputs": ["PATH_METRICS"]},
    "DraftGoalSeekIn": {"target_value_dec": 0.1, "tolerance": 0.01},
    "ScenarioViewItem": {"value_dec": 0.01},
    "DraftScenarioViewIn": {"views": [{"view_library_id": "v", "operator": "eq", "value_dec": 0.01}]},
    "EntityRef": {"handle": "E1.1"},
    "ExplainCardIn": {"card_id": "c1"},
    "Fact": {"handle": "F1.1", "value_num": 0.1},
    "FieldSpan": {"span": "U1.1"},
    "ModelWeights": {"weights": [{"world": "M1", "weight_dec": 1.0}]},
    "OverrideConfirmation": {"expires_at": "2026-10-18T09:10:00Z"},
    "OverrideDraft": _override_draft,
    "QuoteView": {"handle": "Q1.1"},
    "RunHandleView": {"handle": "R1.1"},
    "TableSpec": {"handle": "T1.1"},
    "WhatIfBundle": _whatif_bundle,
    "Holding": {"is_synthetic": True},
    "LoanCohortTerms": {"state_shares": {"0": 1.0}},
    "AnalysisContract": {"quarter": "2026Q4"},
    "LeverSignOff": {"consent_scenario": "R1"},
    "ObjectiveSpec": {"model_weights": {"M1": 1.0}},
    "NoiseRequest": {"slots": 1},
    "PathMetricsMeta": {"terminal_names": list(REQUIRED_TERMINAL_SERIES)},
    "IdeaBundle": {"target_rubrics": [{"kind": "metric", "text": "m"}, {"kind": "constraint", "text": "c"}]},
    "ForecastRecord": {"is_synthetic": True},
    "Mark": {"is_synthetic": True},
    "Quote": {"is_synthetic": True},
    "Lever": {"slope": [0.0] * 24},
    "OverlayTrade": {"is_synthetic": True},
    "PolicyRef": {"name": "HOLD"},
    "PolicySpec": {"anchor": "P0@sha256:" + "a" * 64},
    "RecourseOrder": {"rungs": list(RECOURSE_RUNGS)},
    "ResidualSpec": {"features": [{"var": "F_t", "lag": 1}]},
    "Theta": {"gamma": 3.0, "shortfall_exponent": 2.0},
    "GroupSpec": {"code": "XX"},
    "TaxonomyConfig": lambda p: {**p, "groups": [{**example_payload(GroupSpec), "commitment_split": 1.0}]},
    "CubeMeta": {"base_entropy_hex": "00", "n_paths": 1, "is_synthetic": True},
    "StatePanel": lambda p: {**p, "rows": [example_payload(PanelRow)] * 12},
    "StateSnapshot": {"pi0_macro": [1.0], "stress_post": [1.0, 0.0, 0.0], "e0": [1.0, 0.0, 0.0, 0.0]},
}


def _patch(name: str, value: Any) -> Any:
    patch = PATCHES.get(name)
    if patch is None or not isinstance(value, dict):
        return value
    return patch(value) if callable(patch) else {**value, **patch}


def _gen(node: dict[str, Any], defs: dict[str, Any], name: str) -> Any:
    if "$ref" in node:
        def_name = node["$ref"].rsplit("/", 1)[1]
        return _patch(def_name, _gen(defs[def_name], defs, name))
    if "const" in node:
        return node["const"]
    if "enum" in node:
        return node["enum"][0]
    for key in ("anyOf", "oneOf"):
        if key in node:
            options = node[key]
            if any(o.get("type") == "null" for o in options):
                return None
            return _gen(options[0], defs, name)
    if "allOf" in node:
        return _gen(node["allOf"][0], defs, name)
    kind = node.get("type")
    if kind == "object":
        required = node.get("required", [])
        return {k: _gen(v, defs, k) for k, v in node.get("properties", {}).items() if k in required}
    if kind == "array":
        return [_gen(x, defs, name) for x in node.get("prefixItems", [])]
    if kind == "string":
        if node.get("pattern") in BY_PATTERN:
            return BY_PATTERN[node["pattern"]]
        if node.get("format") == "date":
            return "2026-09-30"
        if node.get("format") == "date-time":
            return "2026-10-18T09:00:00Z"
        if "world" in name:
            return "M1"
        if name.endswith("hash"):
            return "sha256:" + "0" * 64
        return "x"
    return {"number": 0.0, "integer": 0, "boolean": False}.get(kind)


def example_payload(model: type[BaseModel]) -> dict[str, Any]:
    schema = model.model_json_schema()
    return _patch(model.__name__, _gen(schema, schema.get("$defs", {}), ""))


def _round_trip(model: type[BaseModel]) -> None:
    obj = model.model_validate_json(json.dumps(example_payload(model)))
    text = obj.model_dump_json()
    again = model.model_validate_json(text)
    assert again == obj and again.model_dump_json() == text


def test_inventory_covers_the_exchange_models() -> None:
    names = {m.__name__ for m in MODELS}
    assert len(MODELS) > 300
    assert {"PolicySpec", "IdeaBundle", "AnalysisContract", "RunManifest", "EvalRecord", "DecisionRecord",
            "ChatTurnRecord", "OverrideConfirmation", "WhatIfBundle", "BookSnapshot", "EscalationDraft"} <= names


@pytest.mark.parametrize("model", MODELS, ids=lambda c: f"{c.__module__.rsplit('.', 1)[1]}.{c.__name__}")
def test_every_contract_model_round_trips_through_json(model: type[ContractModel]) -> None:
    _round_trip(model)


@pytest.mark.parametrize("model", TOOL_RESULTS, ids=lambda m: m.__name__)
def test_every_analyst_tool_result_round_trips_through_json(model: type[BaseModel]) -> None:
    _round_trip(model)


@pytest.mark.parametrize("model", MODELS, ids=lambda c: f"{c.__module__.rsplit('.', 1)[1]}.{c.__name__}")
def test_no_model_serializes_a_field_its_validation_rejects(model: type[ContractModel]) -> None:
    """Under ``extra="forbid"`` a computed field is dumped but refused on input (R01); derived values are
    plain properties or methods (e.g. ``PolicySpec.spec_hash``)."""
    assert not model.model_computed_fields, f"{model.__name__} has computed fields {list(model.model_computed_fields)}"
