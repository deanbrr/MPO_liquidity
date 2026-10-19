"""Claims, room and lab contracts (BUILD_SPEC v1.1 §3.16; CHAT_ANALYST §4.3, §4.5, §5.5). Owner WP-01."""

from __future__ import annotations

import json
import re
from typing import get_args

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.claims import ANALYST_PLACEHOLDER_RE, PLACEHOLDER_RE, ValidationCode
from adic_tpa.contracts.lab import IdeaBundle
from adic_tpa.contracts.room import Theta, ViewSpec

RUN = "run-20261018T091500Z-3f2a9c1d"


def test_memo_placeholder_grammar() -> None:
    m = re.search(PLACEHOLDER_RE, "P(red) is {{m:tier1.t6.cp_upper@v1|prob}} in M6.")
    assert m and m.group("metric") == "tier1.t6.cp_upper@v1" and m.group("fmt") == "prob"
    assert re.search(PLACEHOLDER_RE, "{{m:tier1.t6.cp_upper@v1|dollars}}") is None


@pytest.mark.parametrize(("text", "group", "value"), [
    ("{{f:F3.7}}", "f", "F3.7"), ("{{cmp:F3.7,F3.9}}", "cmp_b", "F3.9"), ("{{e:E3.2}}", "e", "E3.2"),
    ("{{c:target_return}}", "c", "target_return"), ("{{q:Q3.1}}", "q", "Q3.1"), ("{{u:U3.1}}", "u", "U3.1"),
    ("{{t:T3.1}}", "t", "T3.1"), (f"{{{{m:tier1.t6.cp_upper@v1@{RUN}|prob}}}}", "m_run", RUN),
    ("{{m:tier1.t6.cp_upper@v1|prob}}", "m_metric", "tier1.t6.cp_upper@v1"),
    (f"{{{{a:{RUN}:tier1_board:/rows/T6/M6/cp_upper|prob}}}}", "a_ref", f"{RUN}:tier1_board:/rows/T6/M6/cp_upper"),
])
def test_analyst_placeholder_forms(text: str, group: str, value: str) -> None:
    m = ANALYST_PLACEHOLDER_RE.fullmatch(text)
    assert m is not None and m.group(group) == value


@pytest.mark.parametrize("text", ["{{f:E3.7}}", "{{f:F3}}", "{{cmp:F1.1}}", "{{u:3.1}}", "{{x:F3.1}}", "16%"])
def test_analyst_placeholder_rejects(text: str) -> None:
    assert ANALYST_PLACEHOLDER_RE.fullmatch(text) is None


def test_validation_codes_include_the_analyst_codes() -> None:
    codes = set(get_args(ValidationCode))
    assert {"LITERAL_DIGIT", "UNFETCHED_REF", "LLM_NUMBER_RENDERED", "CLAIM_FACT_MISMATCH", "UNBOUND_COMPARATIVE",
            "P10_WITHOUT_PRED", "MISSING_WHAT_WOULD_CHANGE"} <= codes
    assert "REF_NOT_FETCHED" not in codes                                     # retired by CHAT_ANALYST §5.5


def test_view_spec_confirmation_fields() -> None:
    draft = {"channel": "FBE", "metric": "fwd_return_a", "operator": "eq", "value": 0.08}
    base = {"view_id": "v1", "draft": draft, "author_hash": "a"}
    assert not ViewSpec.model_validate_json(json.dumps(base)).confirmed
    ok = ViewSpec.model_validate_json(json.dumps({**base, "confirmed": True, "confirmed_by": "u",
                                                  "confirmation_surface": "tpa_chat"}))
    assert ok.confirmation_surface == "tpa_chat"
    with pytest.raises(ValidationError, match="confirmed"):
        ViewSpec.model_validate_json(json.dumps({**base, "confirmed": True}))
    with pytest.raises(ValidationError):                                      # client attestation is gone
        ViewSpec.model_validate_json(json.dumps({**base, "confirmed": True, "confirmed_by": "u",
                                                 "confirmation_surface": "mcp_client_attested"}))


def test_theta_admissible_set() -> None:
    ok = Theta.model_validate_json('{"gamma": 3, "lambda_T": 1, "shortfall_exponent": 2, "t6_limit": 0.01}')
    assert ok.extra_costs == {}
    for field, bad in (("gamma", 7), ("lambda_T", -0.1), ("shortfall_exponent", 1.0), ("t6_limit", 1.5)):
        data = {"gamma": 3, "lambda_T": 1, "shortfall_exponent": 2, "t6_limit": 0.01, field: bad}
        with pytest.raises(ValidationError):
            Theta.model_validate_json(json.dumps(data))


def test_escalation_draft_is_llm_facing_and_the_firewall_assembles_the_row() -> None:
    """Review R12: roles fill EscalationDraft (no system- or human-owned field); the ledger row adds them."""
    from datetime import datetime, timezone

    from adic_tpa.contracts.enums import CampaignState
    from adic_tpa.contracts.lab import Escalation, EscalationDraft
    from adic_tpa.contracts.ports import LLM_TOOL_INPUT_MODELS

    assert EscalationDraft in LLM_TOOL_INPUT_MODELS and Escalation not in LLM_TOOL_INPUT_MODELS
    assert not {"raised_at", "resolved_by", "resolution", "escalation_id", "state"} & set(EscalationDraft.model_fields)
    draft = EscalationDraft.model_validate_json(json.dumps({
        "kind": "data_gap", "question": "Which census applies?", "blocking": True, "proposed_assumption": None,
        "severity": "high"}))
    when = datetime(2026, 10, 18, 9, tzinfo=timezone.utc)
    row = Escalation.from_draft(draft, escalation_id="esc-1", worker=2, state=CampaignState.IDEATION, raised_at=when)
    assert (row.question, row.blocking, row.severity, row.worker, row.raised_at) == (
        "Which census applies?", True, "high", 2, when)
    assert row.resolved_by is None and row.resolution is None
    with pytest.raises(ValidationError):
        EscalationDraft.model_validate_json(json.dumps({**draft.model_dump(), "raised_at": "2026-10-18T09:00:00Z"}))


def test_idea_bundle_needs_metric_and_constraint_rubrics() -> None:
    bundle = {
        "idea_id": "i1", "title": "t", "worker": 1, "cycle": 2, "kind": "policy_residual", "hypothesis": "h",
        "mechanism_refs": [f"{RUN}:cards:/0"], "implementation_plan": ["p"],
        "spec": {"anchor": "P0@sha256:" + "a" * 64},
        "target_rubrics": [{"kind": "metric", "text": "CE up", "metric_id": "j.delta_ce_bp@v1"},
                           {"kind": "constraint", "text": "T6 holds"}],
        "predicted_effect": {"metric_id": "j.delta_ce_bp@v1", "direction": "up", "size_bp": 3.0,
                             "interval_bp": {"lo": 0.0, "hi": 6.0}},
        "assumptions": []}
    assert IdeaBundle.model_validate_json(json.dumps(bundle)).spec.spec_hash.startswith("sha256:")
    with pytest.raises(ValidationError, match="rubric"):
        IdeaBundle.model_validate_json(json.dumps({**bundle, "target_rubrics": bundle["target_rubrics"][:1]}))
