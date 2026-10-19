"""Each contracts validator rejects its violation (BUILD_SPEC v1.1 §3, §1.12, §3.17; review WP01-R04). Owner WP-01.

One row per validator that no other test pins: the baseline payload must validate and the single change must raise
the validator's own error. The labelling validators come first (§1.12; ``tpa audit labels`` counts on them), then
the tree, flow, recourse, configuration and analyst rules. SYNTHETIC values only.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pytest
import yaml
from pydantic import ValidationError

from adic_tpa.contracts.actions import DecisionCard
from adic_tpa.contracts.analyst import AnswerCard, Fact, NoPayload, OverrideConfirmation, ToolResult
from adic_tpa.contracts.engine_io import FlowCubeMeta, NoiseRequest, NoiseSlice
from adic_tpa.contracts.enums import ConsentScenario, PricedOn
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.evidence import (
    REQUIRED_TERMINAL_SERIES, EvalRequest, PathMetrics, PathMetricsMeta, RunManifest, SolverRecord,
)
from adic_tpa.contracts.ledger import CanonicalConventions, RecourseOutcome
from adic_tpa.contracts.marks import Mark, Quote
from adic_tpa.contracts.optimizer import DualSet, HSolution, LPMeta, NodeCoefficients
from adic_tpa.contracts.overlay import OverlayTrade
from adic_tpa.contracts.room import ViewSpec
from adic_tpa.contracts.taxonomy import GroupSpec, TaxonomyConfig, taxonomy_path
from adic_tpa.contracts.world import CubeMeta, Tree, TreeSpec

H64 = "sha256:" + "0" * 64
RUN = "run-20261018T091500Z-3f2a9c1d"
REF = f"{RUN}:cards:/0"
P = 3


@dataclass(frozen=True)
class Case:
    name: str
    build: Callable[[dict[str, Any] | None], object]   # None: the valid baseline; a dict: the change to apply
    change: dict[str, Any]
    error: type[Exception]
    match: str


def _json_case(model: Any, base: dict[str, Any]) -> Callable[[dict[str, Any] | None], object]:
    def build(change: dict[str, Any] | None) -> object:
        return model.model_validate_json(json.dumps({**copy.deepcopy(base), **(change or {})}))
    return build


# --------------------------------------------------------------------------------------- §1.12 labelling rows
CUBE_META = {"world_id": "M1", "plane": "SEARCH", "base_entropy_hex": "00ff", "generator_hash": "g",
             "asof": "2026-09-30", "n_paths": P, "path_offset": 0, "months": 6, "factor_names": ["us_eq"],
             "factor_kinds": ["logret"], "asset_names": ["us_eq"], "is_synthetic": True, "data_class": "SYNTHETIC",
             "checksum": H64}
MARK = {"holding_id": "SYN-PE-0042", "mark_type": "FORECAST", "as_of": "2026-09-30",
        "recorded_at": "2026-10-05T00:00:00Z", "basis": "IRR", "gross_net": "net", "value": 0.16, "author": "pe-desk",
        "revision_id": 3, "is_synthetic": True, "data_class": "SYNTHETIC"}
QUOTE = {"quote_id": "q1", "holding_id": "SYN-PE-0042", "as_of": "2026-09-30", "kind": "secondary_bid",
         "bid_pct_ref_nav": 0.88, "ref_nav_date": "2026-06-30", "source": "external", "counterparty_class": "dealer",
         "conflict_flag": False, "is_synthetic": True, "data_class": "SYNTHETIC"}
TRADE = {"trade_id": "SYN-TR-00001", "book": "TAIL", "template": "put", "underlying": "SPX", "notional_bn": 1.0,
         "premium_bn": 0.01, "venue": "listed", "is_synthetic": True, "data_class": "SYNTHETIC"}
REPORT = {"passed": True, "coverage": 1.0, "errors": []}
RENDERED = {"doc_id": "d1", "kind": "answer", "template_text": "t", "rendered_html": "<p>t</p>", "claims": [],
            "validation": REPORT, "provenance_root": REF, "data_class": "SYNTHETIC"}
ANSWER = {"context_id": "C1", "statements": [], "status": 1, "synthetic": True, "interim": False,
          "rendered": RENDERED, "answer_id": "a1", "labels": ["SYNTHETIC"], "run_ids": [], "validation": REPORT,
          "fallback": False, "served_by_fallback": False}
MANIFEST = {"run_id": RUN, "kind": "quarter", "created_at": "2026-10-18T09:15:00Z", "engine_git_sha": "abc",
            "engine_tree_hash": H64, "config_hash": H64, "contract_hash": None, "snapshot_hash": H64,
            "census_hash": None, "belief_hash": None, "scenario_hashes": {}, "seed_spawn": {}, "plane": "SEARCH",
            "cache_keys": [], "solver_records": [], "versions": {}, "env": {}, "llm_calls": [],
            "data_class": "SYNTHETIC", "run_mode": "DEV_SYNTHETIC", "status": "OK"}

LABELLING = [
    Case("CubeMeta is_synthetic vs data_class", _json_case(CubeMeta, CUBE_META), {"is_synthetic": False},
         ValidationError, "disagrees with data_class"),
    Case("Mark is_synthetic vs data_class", _json_case(Mark, MARK), {"data_class": "REAL"},
         ValidationError, "disagrees with data_class"),
    Case("Mark SYN id on a REAL row", _json_case(Mark, MARK), {"data_class": "REAL", "is_synthetic": False},
         ValidationError, "carries the SYN- prefix"),
    Case("Quote is_synthetic vs data_class", _json_case(Quote, QUOTE), {"is_synthetic": False},
         ValidationError, "disagrees with data_class"),
    Case("OverlayTrade is_synthetic vs data_class", _json_case(OverlayTrade, TRADE), {"data_class": "REAL"},
         ValidationError, "disagrees with data_class"),
    Case("OverlayTrade real id on a SYNTHETIC row", _json_case(OverlayTrade, TRADE), {"trade_id": "ADIC-TR-1"},
         ValidationError, "lacks the SYN- prefix"),
    Case("AnswerCard synthetic without the SYNTHETIC label", _json_case(AnswerCard, ANSWER), {"labels": []},
         ValidationError, "SYNTHETIC label"),
    Case("AnswerCard fallback without SERVED_BY_FALLBACK", _json_case(AnswerCard, ANSWER),
         {"served_by_fallback": True}, ValidationError, "SERVED_BY_FALLBACK"),
    Case("RunManifest REAL data in DEV_SYNTHETIC mode", _json_case(RunManifest, MANIFEST), {"data_class": "REAL"},
         RunModeRefused, "DEV_SYNTHETIC"),
]


# --------------------------------------------------------------------------------------- §3.17 trees
def _coef(n: int) -> NodeCoefficients:
    nc3, n1 = np.zeros((n, 2, 2)), np.zeros(n)
    kw: dict[str, Any] = {f: nc3 for f in ("delta", "qcall", "ret_simple", "bid", "income", "u_per_nav", "nav_share",
                                           "call_stress_12m")}
    kw.update({f: n1 for f in ("lo_ret", "hf_ret", "vm_per_beta", "cash_rate", "fac_rate", "draw_rate_q", "tau_lo",
                               "h_im", "ra_debt_rate", "ra_amort", "ra_direct_share", "tail_prem_rate", "tail_value",
                               "opp_pnl_rate", "delta_im_rate", "opex_rate")})
    return NodeCoefficients(**kw, hf_phi=np.zeros((n, 4)), fac_avail=np.ones((n, 1)), amber_depth=np.zeros((n, 2)))


TREE = {"p": [1.0, 0.4, 0.6], "p_world": [[1.0, 1.0], [0.5, 0.3], [0.5, 0.7]], "leaf_world": [-1, 0, 1]}


def _tree(change: dict[str, Any] | None) -> object:
    arrays = {**TREE, **(change or {})}
    tree = Tree(spec=TreeSpec(worlds=("M1", "M6")), tree_hash="t", pooled_worlds=("M1", "M6"),
                parent=np.array([-1, 0, 0], dtype=np.int32), t_end=np.array([0, 1, 1], dtype=np.int16),
                period_q=np.array([0, 1, 1], dtype=np.int8), stage=np.array([0, 1, 1], dtype=np.int8),
                p=np.array(arrays["p"]), p_world=np.array(arrays["p_world"]),
                is_leaf=np.array([False, True, True]), leaf_world=np.array(arrays["leaf_world"], dtype=np.int8),
                lr_weight=np.ones(3), member_ptr=np.array([0, 2, 3, 4], dtype=np.int32),
                member_idx=np.array([0, 1, 0, 1], dtype=np.int32), coef=_coef(3), obs_centroid=np.zeros((3, 2)),
                regime_class=np.zeros(3, dtype=np.int8))
    tree.validate()
    return tree


TREES = [
    # children sum to the parent's p (0.4 + 0.5 = 0.9 = root), yet the leaves hold only 0.9
    Case("Tree leaves sum to 1", _tree, {"p": [0.9, 0.4, 0.5]}, SchemaError, "leaf probabilities must sum to 1"),
    Case("Tree p_world leaves sum to 1 per world", _tree, {"p_world": [[1.0, 1.0], [0.6, 0.3], [0.5, 0.7]]},
         SchemaError, "per world"),
    Case("Tree leaf_world is -1 on interior nodes", _tree, {"leaf_world": [0, 0, 1]}, SchemaError, "leaf_world"),
    Case("Tree leaf_world indexes a world", _tree, {"leaf_world": [-1, 0, 2]}, SchemaError, "leaf_world"),
    Case("Tree leaves carry a world", _tree, {"leaf_world": [-1, -1, 1]}, SchemaError, "leaf_world"),
]


# --------------------------------------------------------------------------------------- flows and recourse
def _noise(change: dict[str, Any] | None) -> object:
    req = NoiseRequest.model_validate_json(json.dumps({"source": "priv.fund.idio", "slots": 2,
                                                       "entity_ids": ["SYN-PE-0001"], "months": [0, 1, 2]}))
    months = (change or {}).get("months", 3)
    noise = NoiseSlice(requests=(req,), u={"priv.fund.idio": np.full((P, months, 1, 2), 0.5)})
    noise.validate()
    return noise


def _outcome(change: dict[str, Any] | None) -> object:
    sold = np.zeros((P, 2), dtype=np.float32)
    sold[0, 0] = 0.1
    red = np.zeros((P, 2), dtype=bool)
    red[0, 0] = True
    if change:
        red[1, 1] = True                                             # a red flag on an unsold unit
    month = np.where(sold > 0, 2, -1).astype(np.int16)
    out = RecourseOutcome(unit_ids=("SYN-PE-0001", "SYN-PE-0002"), sold_frac=sold, month=month,
                          proceeds_bn=np.where(sold > 0, 0.5, 0.0), red=red, reason=np.zeros((P, 2), dtype=np.int8))
    out.validate()
    return out


SELL = {"unit_id": "SYN-PE-0001", "group": "PE", "lens": "SELL", "instrument": "lp_sale", "size_bn": 1.0,
        "exposure_delta_bn": -1.0, "financing_delta_bn": 0.0, "cash_out_bn": 0.9}
FLOW_CUBE_META = {"unit_ids": ["SYN-PE-0001"], "group_of": ["PE"], "cube_checksum": H64, "action": SELL}

FLOWS = [
    Case("NoiseSlice months axis matches its request", _noise, {"months": 2}, SchemaError, "disagrees with its request"),
    Case("RecourseOutcome red only on sold units", _outcome, {"red_unsold": True}, SchemaError, "only on sold units"),
    Case("FlowCube column cubes carry 1-3 units", _json_case(FlowCubeMeta, FLOW_CUBE_META),
         {"unit_ids": ["SYN-PE-0001", "SYN-PE-0002", "SYN-PE-0003", "SYN-PE-0004"],
          "group_of": ["PE", "PE", "PE", "PE"]}, ValidationError, "1-3"),
    Case("FlowCube group_of has one group per unit", _json_case(FlowCubeMeta, FLOW_CUBE_META),
         {"group_of": ["PE", "PE"]}, ValidationError, "one group per unit"),
]


# --------------------------------------------------------------------------------------- configuration rows
def _taxonomy_raw() -> dict[str, Any]:
    return yaml.safe_load(taxonomy_path("v2").read_text(encoding="utf-8"))


PUBLIC_SPEC = next(g for g in _taxonomy_raw()["groups"] if g["kind"] == "public")


def _taxonomy(change: dict[str, Any] | None) -> object:
    raw = _taxonomy_raw()
    if change:
        raw["couplings"][0]["target"] = change["target"]
    return TaxonomyConfig.model_validate_json(json.dumps(raw))


CONVENTIONS = {"credit_cash_a": {"PRIVCREDIT": 0.10}, "commitment_split": {"PE": 0.6, "COINVEST": 0.4},
               "real_assets": {"noi_yield_mult": 0.8, "refi_spread_stress_a": 0.02, "refi_ltv_cap": 0.5}}

CONFIG = [
    Case("GroupSpec fund_distribution_stress only on private groups", _json_case(GroupSpec, PUBLIC_SPEC),
         {"fund_distribution_stress": True}, ValidationError, "private groups only"),
    Case("GroupSpec amber tier enters at TPFA or ALL", _json_case(GroupSpec, PUBLIC_SPEC), {"amber_tier": True},
         ValidationError, "amber-tier"),
    Case("TaxonomyConfig couplings name known groups", _taxonomy, {"target": "NOT_A_GROUP"}, ValidationError,
         "unknown group"),
    Case("CanonicalConventions commitment split sums to 1", _json_case(CanonicalConventions, CONVENTIONS),
         {"commitment_split": {"PE": 0.6, "COINVEST": 0.3}}, ValidationError, "sum to 1"),
    Case("CanonicalConventions revolver credit in [0, 1]", _json_case(CanonicalConventions, CONVENTIONS),
         {"revolver_credit": 1.2}, ValidationError, "revolver_credit"),
]


# --------------------------------------------------------------------------------------- evidence and optimizer rows
def _path_metrics(change: dict[str, Any] | None) -> object:
    meta = PathMetricsMeta.model_validate_json(json.dumps({
        "world_id": "M1", "plane": "SEARCH", "policy_ref": {"kind": "native", "name": "HOLD", "params_hash": H64},
        "cube_checksum": H64, "quarterly_names": [], "terminal_names": list(REQUIRED_TERMINAL_SERIES),
        "data_class": "SYNTHETIC"}))
    terminal = np.zeros((P, len(REQUIRED_TERMINAL_SERIES)))
    if change:
        terminal[1, REQUIRED_TERMINAL_SERIES.index(change["flag"])] = 0.5
    pm = PathMetrics(meta=meta, quarterly=np.zeros((P, 41, 0), dtype=np.float32), terminal=terminal)
    pm.validate()
    return pm


SOLVER = {"solver": "highs", "version": "1.15.1", "algorithm": "simplex", "options": {}, "threads": 1,
          "status": "optimal", "iterations": 0, "time_s": 0.0, "objective": 0.0, "primal_infeas": 0.0,
          "dual_infeas": 0.0, "crossover": False}
LP_META = {"tree_hash": "t", "contract_hash": "c", "catalogue_hash": "k", "ledger_hash": "l", "builder_version": "1",
           "consent_scenario": "R0", "pricing_level": "tolerance", "replication": 0}


def _h_solution(change: dict[str, Any] | None) -> object:
    priced_on, recovery = (PricedOn.RESTORED, None) if change else (PricedOn.RESTORED, H64)
    sol = HSolution(meta=LPMeta.model_validate_json(json.dumps(LP_META)), status="optimal", objective=0.0,
                    x=np.zeros(2), duals=DualSet(pi_row=np.zeros(1), mu_cash=np.ones(1), M_cash=np.zeros(1),
                                                 ell=np.zeros(1), quality={}),
                    root_values={}, marginal_utility_wealth=1.0, priced_on=priced_on,
                    consent_scenario=ConsentScenario.R0, pricing_level="tolerance", recovery_hash=recovery,
                    replication=0, solver=SolverRecord.model_validate_json(json.dumps(SOLVER)))
    sol.validate()
    return sol


LEVER = {"unit_id": "SYN-PE-0001", "group": "PE", "lens": "LEVER", "instrument": "nav_loan_add", "size_bn": 1.0,
         "exposure_delta_bn": 1.0, "financing_delta_bn": 1.0, "cash_out_bn": 0.0}
BELIEF_CARD = {"raw_marks": {}, "fused_mu_a": 0.1, "sigma_a": 0.2, "band80": [0.0, 0.2], "market_anchor_a": None,
               "flags": [], "zombie": False, "catalyst_status": "n/a", "p_achieved_4q": 0.5, "p_achieved_8q": 0.5,
               "info_value_usd_m": None}
CARD = {"card_id": "c1", "unit_id": "SYN-PE-0001", "group": "PE", "asof": "2026-09-30", "action": LEVER,
        "reduced_cost_bp": 1.0, "dual_interval_bp": [0.5, 1.5], "at_kink": False, "value_usd_m": 10.0, "p_best": 0.6,
        "regret_bp": [0.0, 2.0], "lapv_waterfall": [],
        "flips": {"reservation_price": None, "breakeven_fwd_return_a": None, "breakeven_ell_a": None,
                  "one_off_premium": None},
        "belief": BELIEF_CARD, "consents": [], "rofr": False, "envelope_use_bn": 0.0, "alpha_star_a": 0.01,
        "drag_a": 0.0, "priced_on": "feasible", "consent_scenario": "R0", "recovery_hash": None,
        "gamma_status": "certified", "consent_sensitive": False, "second_order_material": False,
        "tree_sensitive": False, "hp_rank_flag": False, "t6_consuming": False,
        "lever_legs": [{"label": "ADD", "value_usd_m": 6.0}, {"label": "REFI", "value_usd_m": 4.0}],
        "binding_rows": [], "shadow_prices": {}, "plane": "search", "run_ref": REF, "data_class": "SYNTHETIC"}
EVAL = {"request_id": "r1", "campaign_id": "cmp-2026Q4-1", "attempt_id": "a1", "spec_hash": H64, "kind": "tune",
        "tuning_job": {"box": [{"name": "rho", "lo": -0.5, "hi": 0.5}]}}

EVIDENCE = [
    Case("PathMetrics red_event is 0/1", _path_metrics, {"flag": "red_event"}, SchemaError, "red_event"),
    Case("PathMetrics payout_short is 0/1", _path_metrics, {"flag": "payout_short"}, SchemaError, "payout_short"),
    Case("PathMetrics failed is 0/1", _path_metrics, {"flag": "failed"}, SchemaError, "failed"),
    Case("HSolution priced on the restored problem needs recovery_hash", _h_solution, {"recovery_hash": None},
         SchemaError, "recovery_hash"),
    Case("DecisionCard LEVER shows its legs", _json_case(DecisionCard, CARD), {"lever_legs": None},
         ValidationError, "LEVER card"),
    Case("DecisionCard restored pricing carries recovery_hash", _json_case(DecisionCard, CARD),
         {"priced_on": "restored_problem"}, ValidationError, "recovery_hash"),
    Case("EvalRequest tune needs a tuning_job", _json_case(EvalRequest, EVAL), {"tuning_job": None},
         ValidationError, "tuning_job"),
    Case("EvalRequest evaluate forbids a tuning_job", _json_case(EvalRequest, EVAL), {"kind": "evaluate"},
         ValidationError, "tuning_job"),
]


# --------------------------------------------------------------------------------------- analyst and room rows
FACT = {"handle": "F3.1", "ref": REF, "metric_id": "cards.lens@v1", "label": "lens", "about": [], "keys": [],
        "value_num": None, "value_cat": "SELL", "unit": "cat", "fmt": "cat", "plane": "search", "status": 1,
        "gate_label": None, "ci": None, "model_range": None, "mc_se": None, "paired_table": None,
        "scenario_hash": None, "as_of": "2026-09-30", "recorded_at": None, "data_class": "SYNTHETIC",
        "priced_on": None, "consent_scenario": None, "flags": []}
TOOL_ERROR = {"code": "NOT_IN_ARTIFACTS", "rule_id": None, "route": None}
RESULT = {"context_id": "C1", "turn": 1, "status": "OK", "payload": None, "facts": [], "entities": [], "quotes": [],
          "tables": [], "withheld": [], "error": None, "model_text": "RESULT get_metric OK"}
VIEW = {"view_id": "v1", "draft": {"channel": "FBE", "metric": "fwd_return_a", "operator": "eq", "value": 0.08},
        "author_hash": "a"}

ANALYST = [
    Case("Fact categorical values use fmt cat", _json_case(Fact, FACT), {"fmt": "pct"}, ValidationError,
         "fmt 'cat'"),
    Case("ToolResult OK carries no error", _json_case(ToolResult[NoPayload], RESULT), {"error": TOOL_ERROR},
         ValidationError, "carries no error"),
    Case("ToolResult PARTIAL carries no error", _json_case(ToolResult[NoPayload], RESULT),
         {"status": "PARTIAL", "error": TOOL_ERROR}, ValidationError, "carries no error"),
    Case("ToolResult ERROR needs an error", _json_case(ToolResult[NoPayload], RESULT), {"status": "ERROR"},
         ValidationError, "needs an error"),
    Case("ViewSpec unconfirmed carries no confirmer", _json_case(ViewSpec, VIEW), {"confirmed_by": "u"},
         ValidationError, "unconfirmed view"),
    Case("ViewSpec unconfirmed carries no surface", _json_case(ViewSpec, VIEW), {"confirmation_surface": "tpa_chat"},
         ValidationError, "unconfirmed view"),
]

CASES = LABELLING + TREES + FLOWS + CONFIG + EVIDENCE + ANALYST


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.name)
def test_baseline_is_valid_and_the_change_is_rejected(case: Case) -> None:
    case.build(None)
    with pytest.raises(case.error, match=case.match):
        case.build(case.change)


CONFIRMATION = {"confirmation_id": "cf-1", "bundle_id": "B1", "bundle_hash": "sha256:" + "6" * 64,
                "user_hash": "sha256:" + "5" * 64, "surface": "tpa_chat", "ticked_inferred": ["horizon_q"],
                "confirmed_at": "2026-10-18T09:00:00Z", "expires_at": "2026-10-18T09:10:00Z", "signer_key_id": "dev",
                "signature": "00"}
ALTERNATIVES = {"confirmation_id": "cf-2", "bundle_id": "B2", "bundle_hash": "sha256:" + "7" * 64,
                "user_hash": "sha256:" + "8" * 64, "surface": "ask_service", "ticked_inferred": [],
                "confirmed_at": "2026-10-18T08:59:00Z", "expires_at": "2026-10-18T09:20:00Z", "signer_key_id": "k2"}


@pytest.mark.parametrize("field", sorted(ALTERNATIVES))
def test_override_confirmation_signature_binds_every_field(field: str) -> None:
    """Who confirmed, where and what: the signed payload covers every field but the signature (S-ADR-40)."""
    base = OverrideConfirmation.model_validate_json(json.dumps(CONFIRMATION))
    changed = OverrideConfirmation.model_validate_json(json.dumps({**CONFIRMATION, field: ALTERNATIVES[field]}))
    assert changed.signed_payload() != base.signed_payload()
    assert set(ALTERNATIVES) == set(OverrideConfirmation.model_fields) - {"signature"}
    assert base.model_copy(update={"signature": "ff"}).signed_payload() == base.signed_payload()
