"""The AnalysisContract and governance models (BUILD_SPEC v1.1 §3.14; ARCH §10.1; S-ADR-06, -25, -31, -32, -37).

The contract is human-owned: no agent tool returns a ``SignOff``. Validators enforce the ARCH §10.1 rules plus the
v1.1 additions (run mode, data class, consent-scenario signing, shortfall exponent > 1, model weights).

WP-01 addition: ``AnalysisContract.lever_signoffs`` records which consent-scenario levers carry sign-offs, because
the rule "pricing_scenario ≤ the highest scenario whose levers carry SignOffs (R1 needs a signed revolver, R2 an
owner band agreement)" cannot be checked from the other contract fields.

Run-mode rules (S-ADR-37) raise ``RunModeRefused`` (code ``RUN_MODE``) rather than a ``ValueError``, so Pydantic
propagates them for gates to classify: a REAL contract refuses any DEV test-signer sign-off, identified by its
signer (``signer_hash == DEV_TEST_SIGNER_HASH``) as well as by its ``method`` label, which the signature does not
cover; REAL data refuses ``run_mode = DEV_SYNTHETIC``.
"""

from __future__ import annotations

import hashlib
import math
import re
from datetime import date, datetime
from typing import Final, Literal

from pydantic import model_validator

from adic_tpa.contracts.enums import (
    AllocationId, CensusId, ConsentScenario, ContractMode, ContractModel, DataClass, LLMMode, Lens, MandateMode,
    ModelFamily, RoleId, RunMode, ShockType, T6SurrogateKind, TargetMode, WorldId,
)
from adic_tpa.contracts.errors import PricingRefused, RunModeRefused
from adic_tpa.contracts.ids import ContractId, GroupId, MetricId
from adic_tpa.contracts.ledger import ConventionSets
from adic_tpa.contracts.optimizer import RecoveryPlan
from adic_tpa.contracts.policy import PolicyRef

__all__ = [
    "SignOff", "ObjectiveSpec", "Tier1Spec", "FloorSpec", "ActionSpace", "PlaneSpec", "GateSpec", "BudgetSpec",
    "RoleLLMSpec", "LLMSpec", "RACI", "RiskBudget", "FrozenQuestion", "LeverSignOff", "AnalysisContract",
    "SignOffRole", "SignOffMethod", "DEV_TEST_KEY_METHOD", "DEV_TEST_SIGNER_HASH",
]

SignOffRole = Literal["CIO", "CRO", "TREASURER", "BOARD", "OWNER", "SECRETARY"]
SignOffMethod = Literal["ed25519_dpapi", "hardware_token", "dev_test_key"]
DEV_TEST_KEY_METHOD: Final = "dev_test_key"
# signer_hash of the DEV/SYNTHETIC test signer (= contracts.signing.signer_hash("SYNTHETIC dev test signer"));
# defined here because SignOff and the contract's REAL-mode rule need it and contracts.signing imports this module.
DEV_TEST_SIGNER_HASH: Final = "sha256:" + hashlib.sha256(b"SYNTHETIC dev test signer").hexdigest()
_QUARTER_RE: Final = re.compile(r"\d{4}Q[1-4]")


class SignOff(ContractModel):
    """A human sign-off (S-ADR-40): Ed25519 over canonical_json({object_hash, role, signer_hash, signed_at}).

    Created only by ``tpa room/seal sign`` under an authenticated Windows account; verified by
    ``contracts.signing.verify`` against ``config/room/signers_roster.yaml``; ``dev_test_key`` is refused in REAL.
    """

    role: SignOffRole
    signer_hash: str
    signed_at: datetime
    object_hash: str
    method: SignOffMethod
    signature: str

    @property
    def is_dev_test(self) -> bool:
        """True for a DEV test-signer sign-off, by signer identity or by method label (S-ADR-37)."""
        return self.signer_hash == DEV_TEST_SIGNER_HASH or self.method == DEV_TEST_KEY_METHOD


class ObjectiveSpec(ContractModel):
    gamma: float = 3.0
    lambda_T: float = 1.0
    shortfall_exponent: float = 2.0              # > 1 strictly (S-ADR-06)
    target_annual: float = 0.10
    horizon_years: int = 10
    accrual: Literal["own_return"] = "own_return"
    target_mode: TargetMode = TargetMode.PRECOMMITTED
    target_anchor_date: date
    target_anchor_wealth_bn: float
    psi_tau_pp: float = 0.5
    model_weights: dict[WorldId, float]          # no code default: set in the contract template; B1/B2 never enter Ψ_τ
    h_utility_tangents: int = 48
    h_utility_tangents_fallback: int = 32
    h_shortfall_breaks: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20, 0.35, 0.50)
    lambda_T_H: float = 1.0                      # tuned by core.mpc.calibrate_buffers (S-ADR-44)

    @model_validator(mode="after")
    def _rules(self) -> ObjectiveSpec:
        if not self.shortfall_exponent > 1.0:
            raise ValueError(f"shortfall_exponent must be > 1 strictly (S-ADR-06), got {self.shortfall_exponent}")
        if not self.model_weights:
            raise ValueError("model_weights must not be empty")
        if any(w in ("B1", "B2") for w in self.model_weights):
            raise ValueError("B1/B2 never enter Psi_tau (BUILD-38)")
        if any(v < 0 for v in self.model_weights.values()):
            raise ValueError("model weights must be non-negative")
        total = math.fsum(self.model_weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"model weights must sum to 1, got {total}")
        if not self.gamma > 0:
            raise ValueError("gamma must be positive")
        return self


class Tier1Spec(ContractModel):
    t6_bands: dict[str, tuple[float | None, float, float]]   # appetite, tolerance, capacity per class
    t6_window_years: int = 5
    t7_limit: float = 0.025
    t8_shock_types: tuple[ShockType, ...] = (ShockType.DB, ShockType.GW, ShockType.SG)
    t8_hard: float = 1.0
    t8_green: float = 1.25
    t9_trigger_12m: float = 0.02
    t9_default_life: float = 0.01
    red_discount_max: float = 0.10               # δ_max of the economic-substance red test (S-ADR-30) [I], A1 field
    theta_rule: Literal["class_banded", "prudence_overlay"] = "class_banded"   # S-ADR-32
    theta_star: float                            # no code default: set by ledger.calibrate_theta_star at G0 (B13)
    theta_star_overlay: float | None = None
    t3_vm_stat: Literal["P99", "CVaR99"] = "P99"
    conventions: ConventionSets
    t6_surrogate: T6SurrogateKind = T6SurrogateKind.CVAR_CLASS
    b_red: dict[str, float] = {}
    b_floor: dict[WorldId, float] = {}           # {} means last quarter's values; zero buffers in the first quarter
    t5: dict[str, float]

    @model_validator(mode="after")
    def _theta(self) -> Tier1Spec:
        if not (math.isfinite(self.theta_star) and 0.0 <= self.theta_star <= 1.0):
            raise ValueError(f"theta_star must be set at G0 to a value in [0, 1], got {self.theta_star}")
        if self.theta_star_overlay is not None and not 0.0 <= self.theta_star_overlay <= 1.0:
            raise ValueError("theta_star_overlay must lie in [0, 1]")
        for cls_name, (appetite, tolerance, capacity) in self.t6_bands.items():
            if not tolerance <= capacity or (appetite is not None and not appetite <= tolerance):
                raise ValueError(f"t6_bands[{cls_name}] must satisfy appetite <= tolerance <= capacity")
        return self


class FloorSpec(ContractModel):
    """Tier-1B floor (S-ADR-31): 10-year forward windows re-certified at every quarterly re-solve."""

    window_years: int = 10
    recertify_each_quarter: bool = True
    median_10y_min: float = 0.07
    median_10y_capacity: float = 0.06
    cvar10_bands: dict[Literal["M1_M5", "MIX", "M6"], tuple[float | None, float, float]] = {
        "M1_M5": (0.01, 0.0, -0.02), "MIX": (0.01, 0.0, -0.02), "M6": (None, -0.025, -0.05)}   # [I]
    misspec_report_only: bool = True


class ActionSpace(ContractModel):
    lenses_by_group: dict[GroupId, tuple[Lens, ...]]
    instrument_whitelist: tuple[str, ...]
    idea_kinds: tuple[Literal["policy_residual", "action_package", "overlay_structure"], ...]
    max_lens_per_asset_q: int = 1


class PlaneSpec(ContractModel):
    search_worlds: tuple[WorldId, ...]
    final_worlds: tuple[WorldId, ...]
    misspec: tuple[str, ...]
    book_variants: tuple[CensusId, ...] = ()     # misspecification members that are another book (S-ADR-43)
    b2_mode: Literal["family_holdout", "out_of_time"] = "family_holdout"
    seal_commitment: str                         # SHA256(salt ‖ contract_hash) written at signing
    windows: dict[str, tuple[date, date]]
    embargo_months_bootstrap: int = 12
    embargo_months_calibration: int = 3
    paths: dict[Literal["race", "confirm", "final", "tail"], int] = {
        "race": 2000, "confirm": 10000, "final": 50000, "tail": 250000}

    @model_validator(mode="after")
    def _b2_final_only(self) -> PlaneSpec:
        if "B2" in self.search_worlds:
            raise ValueError("B2 is final-plane only (§4.10)")
        return self


class GateSpec(ContractModel):
    eps_ni_bp: float = 5.0
    eps_mat_bp: dict[Literal["overlay", "pacing", "refi_lever", "sell", "other"], float]
    lcb_level: float = 0.95
    holm: bool = True
    pbo_max: float = 0.20
    cscv_blocks: int = 8
    mde_max_bp: float
    pbo_source: Literal["search_ledger"] = "search_ledger"
    ni_worlds_search: tuple[WorldId, ...]
    ni_worlds_final: tuple[WorldId, ...]
    ni_comparator: Literal["HOLD", "RESTORED_BASELINE"]
    miss_fd_cost_ratio: float
    search_t6_factor: float = 0.8


class BudgetSpec(ContractModel):
    cycles: int = 24
    cycles_per_worker: int = 12
    evals: int = 650
    evals_per_attempt: int = 2
    tuning_evals: int = 24
    usd_soft: float = 50.0
    usd_hard: float = 200.0
    core_hours: float = 20.0
    alpha_wealth0: float = 0.05
    wall_clock_hours: float = 48.0
    validation_retries: int = 3
    workers: int = 2                             # configurable to 4 (ADR-17)


class RoleLLMSpec(ContractModel):
    role: RoleId
    family: ModelFamily
    model: str
    effort: Literal["low", "medium", "high", "xhigh", "max"]
    max_tokens: int = 16000
    prompt_hash: str
    tools: tuple[str, ...]
    data_classes_allowed: tuple[DataClass, ...]
    materiality: Literal["high", "medium", "low"]
    blocking_escalation: bool


class LLMSpec(ContractModel):
    mode: LLMMode
    provider: Literal["anthropic", "bedrock", "vertex", "foundry"]
    roles: tuple[RoleLLMSpec, ...]
    fallback: Literal["server_default", "client_middleware", "none"] = "server_default"
    holding_level_content_allowed: bool = False  # operator flag (P13)


class RACI(ContractModel):
    owners: dict[str, str]


class RiskBudget(ContractModel):
    name: str
    t6_eps: float
    floor: float
    tail_budget_a: float
    leverage_max: float


class FrozenQuestion(ContractModel):
    qid: str
    item_id: str
    text: str
    resolves_by: date
    metric_id: MetricId | None = None


class LeverSignOff(ContractModel):
    """A signed consent-scenario lever (WP-01 addition): R1 = a signed facility, R2 = the owner band agreement."""

    lever_id: str
    consent_scenario: ConsentScenario
    signoff: SignOff

    @model_validator(mode="after")
    def _scenario(self) -> LeverSignOff:
        if self.consent_scenario not in (ConsentScenario.R1, ConsentScenario.R2):
            raise ValueError("only R1 (facility) and R2 (owner band) levers need sign-offs; R0x/R0 are own authority")
        if self.consent_scenario is ConsentScenario.R2 and self.signoff.role != "OWNER":
            raise ValueError("the R2 band agreement is signed by the OWNER")
        return self


class AnalysisContract(ContractModel):
    """ARCH §10.1 fields plus the v1.1 additions (allocation, census_side_by_side, root_seed, canary, run_mode)."""

    contract_id: ContractId
    version: int
    quarter: str
    data_class: DataClass
    census_id: CensusId | None
    purpose: Literal["DECISION", "OWNER_PROPOSAL"] = "DECISION"
    allocation: AllocationId = "v2"
    census_side_by_side: CensusId | None = None
    mandate_mode: MandateMode = MandateMode.B_OWNER_CALL
    owner_signoff: SignOff | None = None
    mode: ContractMode
    recovery: RecoveryPlan | None
    pricing_scenario: ConsentScenario
    pricing_level: Literal["tolerance", "appetite"] = "tolerance"
    signoffs: tuple[SignOff, ...]
    frozen_questions: tuple[FrozenQuestion, ...]
    objective: ObjectiveSpec
    tier1: Tier1Spec
    floor: FloorSpec
    actions: ActionSpace
    anchor: PolicyRef
    controls: tuple[PolicyRef, ...]
    planes: PlaneSpec
    gates: GateSpec
    budgets: BudgetSpec
    horizons_q: tuple[int, ...] = (12, 20, 40)
    operating_points: tuple[RiskBudget, ...]
    llm_policy: LLMSpec
    raci: RACI
    root_seed: int                               # S-ADR-25
    canary_commitment: str | None = None         # S-ADR-18
    run_mode: RunMode                            # S-ADR-37
    engine_hash: str
    config_hash: str
    snapshot_hash: str
    scenario_hashes: dict[str, str]
    taxonomy_hash: str
    lever_signoffs: tuple[LeverSignOff, ...] = ()   # WP-01 addition (module docstring)

    def all_signoffs(self) -> tuple[SignOff, ...]:
        """Every SignOff the contract carries (contract, owner and lever sign-offs)."""
        extra = (self.owner_signoff,) if self.owner_signoff is not None else ()
        return self.signoffs + extra + tuple(ls.signoff for ls in self.lever_signoffs)

    def highest_signed_scenario(self) -> ConsentScenario:
        """R0 always (own and CF authority); R1 with a signed facility; R2 also with the owner band agreement."""
        signed = {ls.consent_scenario for ls in self.lever_signoffs}
        if ConsentScenario.R1 not in signed:
            return ConsentScenario.R0
        if ConsentScenario.R2 in signed and self.mandate_mode is MandateMode.H_HYBRID:
            return ConsentScenario.R2
        return ConsentScenario.R1

    def cards_allowed(self) -> bool:
        """OWNER_PROPOSAL outputs never reach cards, envelopes or FTP (ARCH §10.1)."""
        return self.purpose == "DECISION"

    def require_pricing_allowed(self) -> None:
        """Raise ``PricingRefused`` when the contract may not feed cards, envelopes or FTP."""
        if not self.cards_allowed():
            raise PricingRefused(f"{self.contract_id}: OWNER_PROPOSAL outputs never reach cards, envelopes or FTP",
                                 {"contract_id": str(self.contract_id), "purpose": self.purpose})

    @model_validator(mode="after")
    def _arch_10_1(self) -> AnalysisContract:
        if not _QUARTER_RE.fullmatch(self.quarter):
            raise ValueError(f"quarter must look like 2026Q4, got {self.quarter!r}")
        b_mode = self.mandate_mode is MandateMode.B_OWNER_CALL
        if b_mode and self.owner_signoff is not None:
            raise ValueError("owner_signoff is set only when mandate_mode != B")
        if not b_mode and self.owner_signoff is None:
            raise ValueError("owner_signoff is required when mandate_mode != B")
        if self.owner_signoff is not None and self.owner_signoff.role != "OWNER":
            raise ValueError("owner_signoff must be signed by the OWNER")
        if self.purpose == "DECISION" and not b_mode:
            raise ValueError("B (owner call) is the only mandate mode in DECISION contracts (ARCH §4.3)")
        if self.mode is ContractMode.STRUCTURAL_RECOVERY and not any(s.role == "BOARD" for s in self.signoffs):
            raise ValueError("STRUCTURAL_RECOVERY requires a BOARD SignOff")
        if (self.mode is not ContractMode.NORMAL) != (self.gates.ni_comparator == "RESTORED_BASELINE"):
            raise ValueError("gates.ni_comparator must be RESTORED_BASELINE iff mode != NORMAL")
        if self.mode is not ContractMode.NORMAL and (self.recovery is None or self.recovery.mode is not self.mode):
            raise ValueError("a recovery-mode contract carries the RecoveryPlan of that mode")
        if self.pricing_scenario > self.highest_signed_scenario():
            raise ValueError(f"pricing_scenario {self.pricing_scenario.value} exceeds the highest signed scenario "
                             f"{self.highest_signed_scenario().value} (R1 needs a signed revolver, R2 an owner band)")
        ctx = {"contract_id": str(self.contract_id), "run_mode": self.run_mode.value}
        if self.run_mode is RunMode.REAL and any(s.is_dev_test for s in self.all_signoffs()):
            raise RunModeRefused(f"{self.contract_id}: run_mode REAL forbids DEV test-signer (dev_test_key) SignOffs "
                                 "(S-ADR-37)", {**ctx, "facility": "dev_test_key"})
        if self.data_class is DataClass.REAL and self.run_mode is RunMode.DEV_SYNTHETIC:
            raise RunModeRefused(f"{self.contract_id}: data_class REAL forbids run_mode DEV_SYNTHETIC (S-ADR-37)",
                                 {**ctx, "data_class": self.data_class.value})
        return self
