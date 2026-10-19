"""Lab contracts (BUILD_SPEC v1.1 §3.16; ARCH §7; S-ADR-36).

``KeyValue`` and ``Interval`` (defined in ``contracts.enums`` to sit below every other module) are the LLM-facing
replacements for dict fields and fixed-length tuples. ``IdeaBundle`` is LLM-authored; its ``predicted_effect`` is
a search diagnostic that is never rendered, pooled or compared with engine numbers.

``EscalationDraft`` (WP-01 addition) is what a role fills when it calls ``escalate`` (§7.4): S-ADR-36 forbids
system- and human-owned fields in LLM-facing schemas, so the lab firewall assembles the ``Escalation`` ledger row
(``Escalation.from_draft``: id, worker, campaign state, ``raised_at``) and humans set ``resolved_by`` and
``resolution``. ``EvaluatorPort.escalate`` keeps the §7.4 input type ``Escalation``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import model_validator

from adic_tpa.contracts.enums import CampaignState, ContractModel, Interval, KeyValue, RoleId
from adic_tpa.contracts.ids import ArtifactRef, MetricId
from adic_tpa.contracts.policy import PolicySpec

__all__ = ["KeyValue", "Interval", "Rubric", "EffectForecast", "IdeaBundle", "AmendmentDraft", "EscalationDraft",
           "Escalation", "AssumptionEntry", "MemoryEvent"]


class Rubric(ContractModel):
    kind: Literal["metric", "constraint", "implementation"]
    text: str
    metric_id: MetricId | None = None
    threshold: float | None = None


class EffectForecast(ContractModel):
    """A search diagnostic only: never rendered, pooled or compared with engine numbers (S-ADR-36)."""

    metric_id: MetricId
    direction: Literal["up", "down"]
    size_bp: float
    interval_bp: Interval


class IdeaBundle(ContractModel):
    """Paper App. F.2; PB §5.4. LLM-authored (the IDEATOR's output model)."""

    idea_id: str
    title: str
    worker: int
    cycle: int
    kind: Literal["policy_residual", "action_package", "overlay_structure"]
    hypothesis: str
    mechanism_refs: tuple[ArtifactRef, ...]
    implementation_plan: tuple[str, ...]
    spec: PolicySpec
    target_rubrics: tuple[Rubric, ...]           # >= 1 metric and >= 1 constraint/implementation
    predicted_effect: EffectForecast
    assumptions: tuple[str, ...]

    @model_validator(mode="after")
    def _rubrics(self) -> IdeaBundle:
        kinds = {r.kind for r in self.target_rubrics}
        if "metric" not in kinds or not kinds & {"constraint", "implementation"}:
            raise ValueError("target_rubrics need >= 1 metric and >= 1 constraint or implementation rubric")
        return self


class AmendmentDraft(ContractModel):
    draft_id: str
    target_field: str
    proposed_value: str
    rationale: str
    author_role: RoleId


class EscalationDraft(ContractModel):
    """The ``escalate`` tool input a role fills (LLM-facing; S-ADR-36)."""

    kind: str
    question: str
    blocking: bool
    proposed_assumption: str | None
    severity: Literal["low", "medium", "high"]


class Escalation(ContractModel):
    """The escalation ledger row (§7.8); assembled by the lab firewall, resolved by a human."""

    escalation_id: str
    kind: str
    question: str
    blocking: bool
    proposed_assumption: str | None
    severity: Literal["low", "medium", "high"]
    worker: int | None
    state: CampaignState
    raised_at: datetime
    resolved_by: str | None = None
    resolution: str | None = None

    @classmethod
    def from_draft(cls, draft: EscalationDraft, *, escalation_id: str, worker: int | None, state: CampaignState,
                   raised_at: datetime) -> Escalation:
        """The unresolved ledger row for a role's draft (the firewall supplies the system-owned fields)."""
        return cls(escalation_id=escalation_id, kind=draft.kind, question=draft.question, blocking=draft.blocking,
                   proposed_assumption=draft.proposed_assumption, severity=draft.severity, worker=worker,
                   state=state, raised_at=raised_at)


class AssumptionEntry(ContractModel):
    assumption_id: str
    text: str
    origin: str
    tagged_artifacts: tuple[ArtifactRef, ...]


class MemoryEvent(ContractModel):
    worker: int
    cycle: int
    kind: Literal["event", "conclusion_update"]
    text: str
    reason: str | None
