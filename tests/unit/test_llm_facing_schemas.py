"""LLM-facing schemas (BUILD_SPEC v1.1 S-ADR-36, §7.4; CHAT_ANALYST §5.1, §14.1 WP-01 DoD). Owner WP-01.

Every role output model and every tool input a model fills must survive the SDK's strict-schema transform
(``anthropic.transform_schema``): an object root with no root-level ``anyOf``/``oneOf``/``allOf`` (Claude Code
flattens them), ``additionalProperties: false`` on every object, no fixed-length tuples (``prefixItems``), no
free-form dicts (they collapse to empty objects), and discriminators that stay enforceable (a single-value
``enum`` on each variant's tag after the transform). ``agents.check_llm_schema`` (WP-25) runs the same rules.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import pytest
from anthropic import transform_schema
from pydantic import BaseModel

from adic_tpa.contracts.analyst import ANALYST_TOOLS
from adic_tpa.contracts.ports import LLM_OUTPUT_MODELS, LLM_TOOL_INPUT_MODELS

MODELS = sorted(set(LLM_OUTPUT_MODELS) | set(LLM_TOOL_INPUT_MODELS), key=lambda m: m.__name__)


def _walk(node: Any, path: str = "#") -> Iterator[tuple[str, dict[str, Any]]]:
    if isinstance(node, dict):
        yield path, node
        for key, value in node.items():
            yield from _walk(value, f"{path}/{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _walk(value, f"{path}/{i}")


def llm_schema_issues(model: type[BaseModel]) -> list[str]:
    raw = model.model_json_schema()
    issues = []
    if raw.get("type") != "object":
        issues.append("root is not an object")
    issues += [f"root-level {k}" for k in ("anyOf", "oneOf", "allOf") if k in raw]
    for path, node in _walk(raw):
        if node.get("type") == "object" and node.get("additionalProperties") is not False:
            issues.append(f"{path}: object without additionalProperties false (free-form dict?)")
        if "prefixItems" in node:
            issues.append(f"{path}: fixed-length tuple (prefixItems)")
        if "propertyNames" in node:
            issues.append(f"{path}: dict keyed by propertyNames")
    transformed = transform_schema(model)
    for path, node in _walk(transformed):
        if path != "#" and node.get("type") == "object" and not node.get("properties"):
            issues.append(f"{path}: empty object after the strict transform")
    for path, node in _walk(raw):
        disc = node.get("discriminator")
        if not disc:
            continue
        tag = disc["propertyName"]
        for ref in disc["mapping"].values():
            name = ref.rsplit("/", 1)[1]
            prop = transformed.get("$defs", {}).get(name, {}).get("properties", {}).get(tag, {})
            if len(prop.get("enum", [])) != 1:
                issues.append(f"{path}: discriminator {tag!r} of {name} is not enforceable after the transform")
    return issues


def test_inventory() -> None:
    names = {m.__name__ for m in MODELS}
    for required in ("SeatArgumentDraft", "MemoDraft", "AnswerDraft", "ViewSpecDraft", "ScenarioSpecDraft",
                     "AuditDraft", "IdeaBundle", "DraftParamOverrideIn", "GetMetricIn", "EvalRequest",
                     "EscalationDraft", "AssumptionEntry"):
        assert required in names
    assert len({t.input_model for t in ANALYST_TOOLS}) == 34
    # every model name is unique, so tool schemas never share a title for different shapes (review R10)
    assert len(names) == len(MODELS)
    # human-owned confirmation fields never appear in an LLM-facing schema (S-ADR-36; review R12)
    for model in MODELS:
        text = json.dumps(model.model_json_schema())
        assert '"confirmed"' not in text and '"author_hash"' not in text and '"resolved_by"' not in text, model


@pytest.mark.parametrize("model", MODELS, ids=lambda m: m.__name__)
def test_llm_facing_schema_survives_the_strict_transform(model: type[BaseModel]) -> None:
    assert llm_schema_issues(model) == []


def test_checker_rejects_the_shapes_s_adr_36_forbids() -> None:
    from typing import Literal

    from adic_tpa.contracts.enums import ContractModel

    class WithDict(ContractModel):
        targets: dict[str, float]

    class WithTuple(ContractModel):
        band: tuple[float, float]

    class A(ContractModel):
        kind: Literal["a"]

    class Bv(ContractModel):
        kind: Literal["b"]

    from pydantic import RootModel

    class RootUnion(RootModel[A | Bv]):
        pass

    assert any("dict" in i or "empty object" in i for i in llm_schema_issues(WithDict))
    assert any("prefixItems" in i for i in llm_schema_issues(WithTuple))
    assert any("root" in i for i in llm_schema_issues(RootUnion))  # type: ignore[arg-type]


def test_discriminated_override_tags_are_enforceable() -> None:
    from adic_tpa.contracts.analyst import DraftParamOverrideIn

    transformed = transform_schema(DraftParamOverrideIn)
    tags = {name: d["properties"]["kind"]["enum"] for name, d in transformed["$defs"].items() if "kind" in d.get("properties", {})}
    assert tags["ConsentOverride"] == ["consent"] and tags["ParamShift"] == ["param_shift"] and len(tags) == 7
