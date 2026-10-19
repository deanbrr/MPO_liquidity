"""The registry's hash chain (BUILD_SPEC v1.1 §4.6; owner WP-04).

Every registry record is one row of the append-only ``chain`` table. The row stores the canonical-JSON
*envelope* of the record,

    {"body": <record>, "class": "<module>:<Class>" | null, "kind": "<kind>", "recorded_at": "<UTC ISO-8601>"}

(sorted keys, ``contracts.hashing.canonical_json`` rules), plus ``prev_hash`` (the previous row's hash,
``GENESIS_HASH`` for the first row) and

    row_hash = sha256(prev_hash ‖ canonical_json(envelope))

which is §4.6's rule with the payload taken to be the envelope, so the record's kind and append time are bound
into the chain as well as its content. ``‖`` concatenates the ASCII ``prev_hash`` text and the UTF-8 envelope;
hashes are ``sha256:<hex>`` (§1.8). A chain detects any edit, insertion or deletion inside it; deleting the last
rows is visible only against an external anchor, so the head (``ChainReport.head``) belongs in manifests and
audit output.

Records that carry their own chain fields (``DecisionRecord``; also ``ChatTurnRecord``, CHAT_ANALYST §11) use
the same rule over the record without ``prev_hash`` and ``record_hash``: ``record_hash`` computes it,
``chain_record`` fills both fields and ``verify_record_chain`` checks a sequence (a decision log, a transcript).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Any, Final, TypeVar

from pydantic import BaseModel, ConfigDict

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import canonical_json

__all__ = [
    "GENESIS_HASH", "RegistryModel", "ChainIssue", "ChainReport", "row_hash", "envelope", "split_envelope",
    "record_hash", "chain_record", "verify_record_chain", "verify_links", "MAX_ISSUES",
]

GENESIS_HASH: Final = "sha256:" + "0" * 64
MAX_ISSUES: Final = 1000          # verify_chain stops listing issues here (a mass corruption needs no full inventory)
_RECORD_CHAIN_FIELDS: Final = frozenset({"prev_hash", "record_hash"})
_BODY_PREFIX: Final = '{"body":'
_CLASS_MARK: Final = ',"class":'

R = TypeVar("R", bound=BaseModel)


class RegistryModel(BaseModel):
    """Base of the registry's own models: frozen, extra fields forbidden, strict (as §3 contracts models).

    Registry rows are read back with ``model_validate_json`` (S-ADR-39).
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class ChainIssue(RegistryModel):
    """One integrity finding of ``verify_chain``."""

    seq: int | None                 # chain row the finding is attributed to; None for schema-level findings
    table: str                      # "chain", an index table, "artifacts" (files), "decisions", "mfdr_tests", "schema"
    reason: str


class ChainReport(RegistryModel):
    """Result of ``Registry.verify_chain`` (§4.6): ``first_bad_seq`` names the first bad row."""

    ok: bool
    rows: int
    head: str                       # last row hash (GENESIS_HASH when empty): anchor it outside the registry
    first_bad_seq: int | None
    issues: tuple[ChainIssue, ...]
    artifacts_checked: int
    checked_at: datetime

    @property
    def first_bad(self) -> ChainIssue | None:
        """The issue at ``first_bad_seq`` (else the first schema-level issue), or None when the chain is intact."""
        if not self.issues:
            return None
        if self.first_bad_seq is not None:
            return next(i for i in self.issues if i.seq == self.first_bad_seq)
        return self.issues[0]


def row_hash(prev_hash: str, payload: str | bytes) -> str:
    """``sha256(prev_hash ‖ payload)`` as ``sha256:<hex>``."""
    data = payload.encode("utf-8") if isinstance(payload, str) else payload
    return "sha256:" + hashlib.sha256(prev_hash.encode("ascii") + data).hexdigest()


def _text(value: str | None) -> str:
    return json.dumps(value, ensure_ascii=False)


def envelope(kind: str, body_text: str, *, cls: str | None, recorded_at: str) -> str:
    """The canonical envelope text of a record whose canonical JSON is ``body_text``.

    Built by concatenation in sorted-key order, so it equals ``canonical_json`` of the parsed envelope (tested);
    this keeps ``put_metrics`` from serializing each body twice.
    """
    return f'{_BODY_PREFIX}{body_text}{_CLASS_MARK}{_text(cls)},"kind":{_text(kind)},"recorded_at":{_text(recorded_at)}}}'


def split_envelope(payload: str) -> tuple[str, dict[str, Any]]:
    """(body text, header) of an envelope; the header holds ``class``, ``kind`` and ``recorded_at``.

    The envelope's own ``,"class":`` follows the whole body, so the last occurrence marks the body's end.
    """
    cut = payload.rfind(_CLASS_MARK)
    if not payload.startswith(_BODY_PREFIX) or cut < 0 or not payload.endswith("}"):
        raise SchemaError("registry row is not a registry envelope", {"payload_head": payload[:80]})
    header = json.loads("{" + payload[cut + 1:])
    return payload[len(_BODY_PREFIX):cut], header


def record_hash(record: BaseModel) -> str:
    """``sha256(record.prev_hash ‖ canonical_json(record without prev_hash and record_hash))``."""
    prev = getattr(record, "prev_hash", None)
    if not isinstance(prev, str):
        raise SchemaError(f"{type(record).__name__} has no prev_hash field to chain on")
    return row_hash(prev, canonical_json(record.model_dump(mode="python", exclude=set(_RECORD_CHAIN_FIELDS))))


def chain_record(record: R, prev_hash: str) -> R:
    """A copy of ``record`` with ``prev_hash`` set and ``record_hash`` computed (validated again)."""
    data = record.model_dump(mode="python")
    if not _RECORD_CHAIN_FIELDS <= data.keys():
        raise SchemaError(f"{type(record).__name__} lacks prev_hash/record_hash fields")
    linked = record.model_copy(update={"prev_hash": prev_hash, "record_hash": GENESIS_HASH})
    return type(record).model_validate_json(
        linked.model_copy(update={"record_hash": record_hash(linked)}).model_dump_json())


def verify_record_chain(records: Sequence[BaseModel], *, start: str = GENESIS_HASH) -> int | None:
    """Index of the first record that breaks the chain (wrong ``prev_hash`` link or ``record_hash``), else None."""
    prev = start
    for i, rec in enumerate(records):
        if getattr(rec, "prev_hash", None) != prev or record_hash(rec) != getattr(rec, "record_hash", None):
            return i
        prev = rec.record_hash  # type: ignore[attr-defined]
    return None


def verify_links(rows: Iterable[tuple[int, str, str, str]]) -> tuple[int, str, list[ChainIssue]]:
    """Check (seq, payload, prev_hash, row_hash) rows in seq order: contiguous seqs from 1, every link and hash.

    Returns (row count, head hash, issues). A row edited in place fails its own hash. A row whose hash was
    recomputed after an edit passes its own check but no longer links to its successor, so the break is
    attributed to the rewritten row. Missing seqs are reported at the first missing seq.
    """
    issues: list[ChainIssue] = []
    expected, last_stored, count = 1, GENESIS_HASH, 0
    for seq, payload, prev_hash, stored in rows:
        count += 1
        self_ok = row_hash(prev_hash, payload) == stored
        if seq != expected:
            issues.append(ChainIssue(seq=expected, table="chain", reason=f"rows {expected}..{seq - 1} are missing"))
        elif prev_hash != last_stored:
            if self_ok and seq > 1:
                issues.append(ChainIssue(seq=seq - 1, table="chain",
                                         reason=f"row hash rewritten: it no longer matches row {seq}'s prev_hash"))
            else:
                issues.append(ChainIssue(seq=seq, table="chain", reason="prev_hash does not link to the previous row"))
        if not self_ok:
            issues.append(ChainIssue(seq=seq, table="chain",
                                     reason="row_hash differs from sha256(prev_hash ‖ payload): row edited"))
        last_stored, expected = stored, seq + 1
        if len(issues) >= MAX_ISSUES:
            break
    return count, last_stored, issues
