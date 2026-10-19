"""contracts.ports (BUILD_SPEC v1.1 §3.17, §3.18): Protocols are runtime-checkable and complete; contexts and LLM
request types construct. Owner WP-01 (the walking skeleton, WP-03, exercises them end to end)."""

from __future__ import annotations

import dataclasses
import inspect
import json

import pytest

from adic_tpa.contracts import ports as P
from adic_tpa.contracts.enums import Clock, ModelFamily, RoleId
from adic_tpa.contracts.evidence import LLMCallRecord
from adic_tpa.contracts.world import OwnerConfig

EVALUATOR_TOOLS = (  # §7.4 tools served by the evaluator
    "state_snapshot", "phase1_restore", "compile_spec", "evaluate_policy", "price_actions", "optimize_h",
    "evaluate_scenario", "reverse_stress", "implied_actions", "ep_condition", "evsi_crossfit", "flip_thresholds",
    "robustness_card", "bridge_card", "group_envelopes", "overlay_offset_card", "attribute", "price_trade",
    "crif_sensitivities", "simm_like", "greek_offsets", "hybrid_quote_check", "get_metric", "list_metrics",
    "get_provenance", "validate_claims", "log_assumption", "escalate",
)


def _methods(proto: type) -> set[str]:
    return {n for n, v in vars(proto).items() if inspect.isfunction(v) and not n.startswith("_")}


def test_protocol_methods_match_the_spec() -> None:
    assert _methods(P.AssetEngine) == {"init", "noise_requests", "recourse_quotes", "step", "apply_recourse",
                                       "column_flows"}
    assert _methods(P.Ledger) == {"apply", "row_slacks", "stress_replica"}
    assert _methods(P.EngineFactory) == {"build"} and _methods(P.Policy) == {"act"}
    assert _methods(P.LLMBackend) == {"parse", "run_tools"}
    assert _methods(P.RoomPort) == {"compile_agenda", "build_briefs", "run_shadow_ic", "lock_prevotes",
                                    "record_decisions"}
    assert _methods(P.EvaluatorPort) == set(EVALUATOR_TOOLS)
    init = inspect.signature(P.AssetEngine.init)
    assert [p.name for p in init.parameters.values() if p.kind is p.KEYWORD_ONLY] == ["draws", "world"]


class FakeEngine:
    engine_id, groups, clock = "fake", ("PE",), Clock.QUARTERLY

    def init(self, book, beliefs, n_paths, *, draws, world): ...
    def noise_requests(self, t): return ()
    def recourse_quotes(self, t, st, world): ...
    def step(self, t, st, world, act, noise): ...
    def apply_recourse(self, st, outcome): ...
    def column_flows(self, unit_id, action, cube): ...


class FakeLedger:
    def apply(self, m, ls, flows, draw, quotes): ...
    def row_slacks(self, ls): return {}
    def stress_replica(self, ls0, stress): ...


class FakeBackend:
    family = ModelFamily.A

    def parse(self, req, output_model): ...
    def run_tools(self, req, tools, executor): ...


def test_runtime_conformance() -> None:
    assert isinstance(FakeEngine(), P.AssetEngine) and isinstance(FakeLedger(), P.Ledger)
    assert isinstance(FakeBackend(), P.LLMBackend)
    assert not isinstance(FakeLedger(), P.AssetEngine)


def owner_cfg() -> OwnerConfig:
    return OwnerConfig.model_validate_json(json.dumps({
        "override_p_a": {"0": 0.0025, "1": 0.0025, "2": 0.01, "3": 0.01, "4": 0.0025, "5": 0.02},
        "fiscal_noise_sd_pp": 1.0, "ref_price": 70.0,
        "p_accept_band": {"0": 1.0, "1": 1.0, "2": 1.0, "3": 0.3, "4": 1.0, "5": 1.0}}))


def test_engine_bundle_is_frozen() -> None:
    bundle = P.EngineBundle(engines=(FakeEngine(),), ledger=FakeLedger(), owner_cfg=owner_cfg(), policy_wrappers=(),
                            effective_config_hashes={"priv": "sha256:" + "0" * 64})
    with pytest.raises(dataclasses.FrozenInstanceError):
        bundle.ledger = FakeLedger()  # type: ignore[misc]
    assert owner_cfg().p_accept_band[3] == 0.3        # ShockType.DB


def test_llm_request_and_response() -> None:
    tool = P.ToolDef(name="answer_grounded", description="submit", input_schema={"type": "object"})
    req = P.LLMRequest(role=RoleId.ANALYST, model="claude-opus-5-5", system="frozen", messages=(), tools=(tool,),
                       effort="medium")
    assert req.max_tokens == 16000 and req.thinking == {"type": "adaptive"} and tool.strict
    record = LLMCallRecord.model_validate_json(json.dumps({
        "call_id": "c1", "role": "ANALYST", "requested_model": "claude-opus-5-5", "served_model": "claude-opus-5-5",
        "fallback_event": False, "prompt_hash": "p", "response_hash": "r", "input_tokens": 10, "output_tokens": 5,
        "cache_read_tokens": 0, "cost_usd": 0.0, "stop_reason": "end_turn", "latency_s": 0.1, "replay_key": "k"}))
    resp = P.LLMResponse(content=(), parsed=None, stop_reason="end_turn", served_model="claude-opus-5-5",
                         usage={"input_tokens": 10}, record=record)
    assert resp.record.role is RoleId.ANALYST


def test_contexts_are_frozen_dataclasses() -> None:
    for ctx in (P.PolicyContext, P.SimContext, P.EngineContext):
        assert dataclasses.is_dataclass(ctx) and ctx.__dataclass_params__.frozen  # type: ignore[attr-defined]
    assert [f.name for f in dataclasses.fields(P.SimContext)][:3] == ["factory", "book", "beliefs"]


def test_llm_facing_model_lists_cover_the_draft_models() -> None:
    names = {m.__name__ for m in P.LLM_OUTPUT_MODELS}
    assert {"SeatArgumentDraft", "MemoDraft", "AnswerDraft", "ViewSpecDraft", "ScenarioSpecDraft", "AuditDraft"} <= names
