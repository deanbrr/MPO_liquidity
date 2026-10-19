"""Evidence and evaluator contracts (BUILD_SPEC v1.1 §3.15, §3.17 PathMetrics, §3.18; ARCH §10.2–§10.4).

``EvalRequest`` has no fields for metrics, seeds, worlds or path counts (ARCH §10.4); the agent view of a result
is the minimal ``EvalResultAgentView``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Final, Literal

import numpy as np
from pydantic import model_validator

from adic_tpa.contracts.arrays import F32, F64, ArrayContainer
from adic_tpa.contracts.enums import (
    ContractModel, DataClass, EvidencePlane, FailureLabel, GateLabel, Plane, RoleId, RunMode, WorldId,
)
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.ids import ArtifactRef, CampaignId, MetricId, RunId
from adic_tpa.contracts.policy import PolicyRef

__all__ = [
    "SolverRecord", "LLMCallRecord", "RunManifest", "MetricDef", "MetricInstance", "TuningBox", "TuningJob",
    "EvalRequest",
    "EvalResultAgentView", "GateOutcome", "EvalRecord", "Certificate", "PathMetricsMeta", "PathMetrics",
    "FBEValidationSet", "GateReport", "REQUIRED_TERMINAL_SERIES",
]

REQUIRED_TERMINAL_SERIES: Final[tuple[str, ...]] = (
    "w_tilde_40", "w_tilde_real_40", "twr_3y", "twr_5y", "twr_10y", "red_event", "red_quarter", "payout_short",
    "t7_shortfall_12m", "t9_trigger_12m", "max_dd_10y", "failed")


class SolverRecord(ContractModel):
    solver: Literal["highs", "highs_mip", "clarabel", "osqp"]
    version: str
    algorithm: str
    options: dict[str, str | int | float | bool]
    threads: int
    status: str
    iterations: int
    time_s: float
    objective: float
    primal_infeas: float
    dual_infeas: float
    crossover: bool


class LLMCallRecord(ContractModel):
    call_id: str
    role: RoleId
    requested_model: str
    served_model: str
    fallback_event: bool
    prompt_hash: str
    response_hash: str
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cost_usd: float
    stop_reason: str
    latency_s: float
    replay_key: str


class RunManifest(ContractModel):
    run_id: RunId
    kind: str
    created_at: datetime
    engine_git_sha: str
    engine_tree_hash: str
    config_hash: str
    contract_hash: str | None
    snapshot_hash: str
    census_hash: str | None
    belief_hash: str | None
    scenario_hashes: dict[str, str]              # "plane:world" -> cube checksum
    seed_spawn: dict[str, str]                   # "plane:world" -> base entropy hex, or "HMAC" on the final plane
    plane: Plane
    cache_keys: tuple[str, ...]
    solver_records: tuple[SolverRecord, ...]
    versions: dict[str, str]
    env: dict[str, str]
    llm_calls: tuple[str, ...]
    data_class: DataClass
    run_mode: RunMode
    parent_runs: tuple[RunId, ...] = ()
    status: Literal["STARTED", "OK", "FAILED", "ABORTED"]
    effective_config_hashes: dict[str, str] = {}   # per module after misspecification overrides (S-ADR-43)
    canonical_artifact_hashes: dict[str, str] = {} # contracts.hashing.canonical_artifact_hash (§9.4 #9)

    @model_validator(mode="after")
    def _modes(self) -> RunManifest:
        # RunModeRefused (code RUN_MODE) is not a ValueError, so Pydantic propagates it for gates to classify
        if self.data_class == DataClass.REAL and self.run_mode == RunMode.DEV_SYNTHETIC:
            raise RunModeRefused(f"{self.run_id}: a REAL-data run cannot run in DEV_SYNTHETIC mode (S-ADR-37)",
                                 {"run_id": str(self.run_id), "data_class": self.data_class.value})
        return self


class MetricDef(ContractModel):
    metric_id: MetricId
    description: str
    unit: str
    aggregation: str
    ci_method: Literal["clopper_pearson", "paired_bootstrap", "mc_se", "none"]
    range_method: Literal["model_min_max", "none"]
    icd203: bool
    owner_role: str
    code_ref: str
    code_hash: str


class MetricInstance(ContractModel):
    metric_id: MetricId
    run_id: RunId
    value: float
    unit: str
    plane: EvidencePlane
    ci: tuple[float, float] | None = None
    model_range: tuple[float, float] | None = None
    mc_se: float | None = None
    scenario_hash: str
    by: dict[str, str] = {}
    data_class: DataClass


class TuningBox(ContractModel):
    """One tuned parameter's box (LLM-facing replacement of a ``dict[str, tuple[float, float]]`` entry; S-ADR-36)."""

    name: str
    lo: float
    hi: float

    @model_validator(mode="after")
    def _ordered(self) -> TuningBox:
        if not self.lo <= self.hi:
            raise ValueError(f"box {self.name}: lo must not exceed hi")
        return self


class TuningJob(ContractModel):
    box: tuple[TuningBox, ...]                   # §3.15's dict[str, (lo, hi)] as named sub-models (S-ADR-36)
    max_evals: int = 24
    method: Literal["cmaes"] = "cmaes"

    @model_validator(mode="after")
    def _unique(self) -> TuningJob:
        names = [b.name for b in self.box]
        if len(set(names)) != len(names):
            raise ValueError("one box per parameter")
        if self.max_evals < 1:
            raise ValueError("max_evals must be >= 1 (the contract's BudgetSpec.tuning_evals caps it)")
        return self

    def as_dict(self) -> dict[str, tuple[float, float]]:
        """The §3.15 view: parameter → (lo, hi)."""
        return {b.name: (b.lo, b.hi) for b in self.box}


class EvalRequest(ContractModel):
    """No fields for metrics, seeds, worlds or path counts (ARCH §10.4)."""

    request_id: str
    campaign_id: CampaignId
    attempt_id: str
    spec_hash: str
    kind: Literal["evaluate", "tune", "ablation", "price_package", "scenario"]
    tuning_job: TuningJob | None = None

    @model_validator(mode="after")
    def _tuning(self) -> EvalRequest:
        if (self.kind == "tune") != (self.tuning_job is not None):
            raise ValueError("a tuning_job is required for kind 'tune' and forbidden otherwise")
        return self


class EvalResultAgentView(ContractModel):
    request_id: str
    correct: bool
    delta_psi_bucket: Literal["<-10", "-10..-3", "-3..0", "0..3", "3..10", ">10"]   # CE bp a year
    gate_categories: tuple[FailureLabel, ...]
    promotable: bool
    budget_left: int


class GateOutcome(ContractModel):
    gate: Literal["G1_correct", "G2_selection", "G3_qualification"]
    passed: bool
    label: GateLabel | None
    failures: tuple[FailureLabel, ...]
    details: dict[str, float]


class EvalRecord(ContractModel):
    """Full record: humans and the auditor only."""

    request: EvalRequest
    agent_view: EvalResultAgentView
    gates: tuple[GateOutcome, ...]
    metrics: dict[MetricId, MetricInstance]
    run_id: RunId
    counted: bool
    cpu_s: float


class Certificate(ContractModel):
    gate: str
    world: WorldId
    k: int
    n: int
    p_hat: float
    cp_upper: float
    band: tuple[float | None, float, float]
    passed: bool
    importance_sampled: bool
    bpoe: float | None = None


class PathMetricsMeta(ContractModel):
    """``PathMetrics.meta`` (§3.17): world, plane, policy, cube checksum and series names."""

    world_id: WorldId
    plane: Plane
    policy_ref: PolicyRef
    cube_checksum: str
    quarterly_names: tuple[str, ...]             # Kq ≤ 48
    terminal_names: tuple[str, ...]              # ⊇ REQUIRED_TERMINAL_SERIES
    data_class: DataClass

    @model_validator(mode="after")
    def _series(self) -> PathMetricsMeta:
        if len(self.quarterly_names) > 48:
            raise ValueError(f"at most 48 quarterly series, got {len(self.quarterly_names)}")
        missing = [s for s in REQUIRED_TERMINAL_SERIES if s not in self.terminal_names]
        if missing:
            raise ValueError(f"terminal series missing {missing}")
        if len(set(self.terminal_names)) != len(self.terminal_names) or \
                len(set(self.quarterly_names)) != len(self.quarterly_names):
            raise ValueError("series names must be unique")
        return self


@dataclass(frozen=True, slots=True)
class PathMetrics(ArrayContainer):
    """Per-path metrics of one simulation block (§3.17); failed paths carry worst-case values, never NaN."""

    meta: PathMetricsMeta
    quarterly: F32                               # [P, 41, Kq]
    terminal: F64                                # [P, Kt]

    def _bindings(self) -> dict[str, int]:
        return {"KQ": len(self.meta.quarterly_names), "KT": len(self.meta.terminal_names)}

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        for name in ("red_event", "payout_short", "failed"):
            col = self.terminal[:, self.meta.terminal_names.index(name)]
            if not np.isin(col, (0.0, 1.0)).all():
                raise SchemaError(f"PathMetrics.terminal[{name}] must be 0 or 1")

    def terminal_series(self, name: str) -> F64:
        return self.terminal[:, self.meta.terminal_names.index(name)]


class FBEValidationSet(ContractModel):
    """Produced by ``beliefs.validation.fbe_variant`` (pure functions of seeds and variant parameters; BUILD-21)."""

    variant: str
    n_worlds: int
    root_seed: int
    config_hash: str
    forecasts_ref: ArtifactRef
    truth_ref: ArtifactRef
    oracle_ref: ArtifactRef


class GateReport(ContractModel):
    """Produced by ``priv.check_v24``, ``synth.run_gates``, ``beliefs.validate_fbe``."""

    subject: str
    gates: dict[str, Literal["pass", "fail", "n/a"]]
    details: dict[str, dict[str, float]]
    blocking: bool
