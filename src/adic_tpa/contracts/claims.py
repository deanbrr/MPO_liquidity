"""Claims: placeholders, validation reports, rendered documents and audits (BUILD_SPEC v1.1 §3.16, §4.28;
CHAT_ANALYST §4.3, §4.5, §5.5).

Writers never type numbers: they use placeholders that ``claims.render`` fills. ``PLACEHOLDER_RE`` is the memo
form of §3.16; ``ANALYST_PLACEHOLDER_RE`` adds the analyst's session-handle forms (§4.3: ``{{f:F3.7}}``,
``{{cmp:F3.7,F3.9}}``, ``{{e:E3.2}}``, ``{{c:<constant>}}``, ``{{q:Q3.1}}``, ``{{u:U3.1}}``, ``{{t:T3.1}}``,
``{{m:<metric>@<run>|fmt}}``, ``{{a:<ref>|fmt}}``). The analyst's ``AnswerDraft`` and ``StatementDraft`` live in
``contracts.analyst`` (the §3.16 pair is retired by CHAT_ANALYST §5.5); ``SeatArgumentDraft`` lives in
``contracts.room`` next to ``ViewSpecDraft``, which it embeds.
"""

from __future__ import annotations

import re
from typing import Final, Literal

from adic_tpa.contracts.contract import SignOff
from adic_tpa.contracts.enums import ContractModel, DataClass, ModelFamily
from adic_tpa.contracts.ids import ArtifactRef, MetricId

__all__ = [
    "PLACEHOLDER_RE", "PLACEHOLDER_FORMATS", "ANALYST_PLACEHOLDER_RE", "ValidationCode", "ValidationError_",
    "ValidationReport", "ClaimRecord", "RenderedDocument", "AuditFinding", "AuditCheck", "AuditReport", "MemoDraft",
    "AuditDraft", "ProvenanceNode",
]

PLACEHOLDER_FORMATS: Final[tuple[str, ...]] = ("pct", "pp", "bp", "usd_bn", "usd_m", "x", "months", "int", "prob", "ratio")
PLACEHOLDER_RE: Final = (
    r"\{\{m:(?P<metric>[a-z0-9_.@:-]+)\|(?P<fmt>pct|pp|bp|usd_bn|usd_m|x|months|int|prob|ratio)\}\}")

_FMT = "|".join(PLACEHOLDER_FORMATS)
_RUN = r"run-\d{8}T\d{6}Z-[0-9a-f]{8}"
ANALYST_PLACEHOLDER_RE: Final = re.compile(
    r"\{\{(?:"
    r"f:(?P<f>F\d+\.\d+)"
    r"|cmp:(?P<cmp_a>F\d+\.\d+),(?P<cmp_b>F\d+\.\d+)"
    r"|e:(?P<e>E\d+\.\d+)"
    r"|c:(?P<c>[a-z][a-z0-9_]*)"
    r"|q:(?P<q>Q\d+\.\d+)"
    r"|u:(?P<u>U\d+\.\d+)"
    r"|t:(?P<t>T\d+\.\d+)"
    rf"|m:(?P<m_metric>[a-z0-9_.@:-]+?)(?:@(?P<m_run>{_RUN}))?\|(?P<m_fmt>{_FMT})"
    rf"|a:(?P<a_ref>{_RUN}:[A-Za-z0-9_.-]+:(?:/[^/|{{}}]*)*)\|(?P<a_fmt>{_FMT})"
    r")\}\}")

ValidationCode = Literal[
    "LITERAL_DIGIT", "UNKNOWN_METRIC", "WRONG_PLANE", "IMPROVEMENT_VERB_UNQUALIFIED", "PROB_WITHOUT_RANGE",
    "CITES_MEMORY", "SYNTHETIC_AS_ADIC", "LOW_COVERAGE", "LEAGUE_TABLE", "NAMED_PERSON_REGRET", "BLUEPRINT_FIGURE",
    "MISSING_P14_FIELD",
    "LLM_NUMBER_RENDERED",        # an LLM-originated numeric field reached a rendered or aggregated output (S-ADR-36)
    "UNFETCHED_REF",              # analyst answer cites a reference not fetched in this turn under its context
    # CHAT_ANALYST §4.5 codes (added per §5.5):
    "CONTEXT_MISMATCH", "CLAIM_FACT_MISMATCH", "UNBOUND_COMPARATIVE", "UNBOUND_CATEGORICAL", "FREE_PROBABILITY_WORD",
    "AGENT_JUDGMENT_NUMERIC", "ADVISORY_LANGUAGE", "USER_INPUT_MISUSE", "P10_WITHOUT_PRED", "CARD_WITHOUT_PRICED_ON",
    "REVERSE_STRESS_AS_PRICE", "MULTI_GROUP_CREDIBILITY", "GRADE_LANGUAGE", "PREVOTE_NARRATIVE", "EXTERNAL_LINK",
    "MISSING_WHAT_WOULD_CHANGE",
]


class ValidationError_(ContractModel):  # noqa: N801 (spec name; avoids pydantic.ValidationError)
    code: ValidationCode
    span: tuple[int, int]
    detail: str


class ValidationReport(ContractModel):
    passed: bool
    coverage: float
    errors: tuple[ValidationError_, ...]


class ClaimRecord(ContractModel):
    claim_id: str
    doc_id: str
    sentence_index: int
    placeholders: tuple[MetricId, ...]
    verbs: tuple[str, ...]
    supports_verdict: Literal["supports", "partial", "not_supported", "unaudited"] = "unaudited"
    auditor_family: ModelFamily | None = None
    human_countersign: SignOff | None = None


class RenderedDocument(ContractModel):
    """Assembled by ``claims.render``; never an LLM output model."""

    doc_id: str
    kind: Literal["memo", "brief", "minutes", "answer", "seat_argument", "minority_report"]
    template_text: str
    rendered_html: str
    claims: tuple[ClaimRecord, ...]
    validation: ValidationReport
    provenance_root: ArtifactRef
    data_class: DataClass


class AuditFinding(ContractModel):
    claim_id: str
    severity: Literal["minor", "major"]
    text: str


class AuditCheck(ContractModel):
    check: Literal["recompute", "contract", "references", "bundle_alignment"]
    result: Literal["pass", "fail"]


class AuditReport(ContractModel):
    """Assembled by deterministic code from an ``AuditDraft``."""

    doc_id: str
    checks: tuple[AuditCheck, ...]
    findings: tuple[AuditFinding, ...]
    verdict: Literal["PASS", "FAIL"]
    family: ModelFamily
    correlated: bool


# LLM draft models (S-ADR-36): the only output models a role may submit; no engine-, validator- or human-owned field.
class MemoDraft(ContractModel):
    doc_kind: Literal["memo", "brief", "minutes", "answer", "minority_report"]
    template_text: str


class AuditDraft(ContractModel):
    doc_id: str
    checks: tuple[AuditCheck, ...]
    findings: tuple[AuditFinding, ...]
    verdict: Literal["PASS", "FAIL"]


class ProvenanceNode(ContractModel):
    ref: ArtifactRef
    kind: str
    parents: tuple[ArtifactRef, ...]
    hash: str
