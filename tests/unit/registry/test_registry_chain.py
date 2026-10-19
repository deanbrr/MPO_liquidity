"""Hash-chain rules (BUILD_SPEC v1.1 §4.6): row_hash = sha256(prev_hash ‖ canonical_json(envelope)); the envelope
equals canonical JSON; record-level chains (DecisionRecord, ChatTurnRecord); link verification attributes every
edit, rewrite and deletion to its row. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import hashlib
import json

import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import canonical_json
from adic_tpa.registry.chain import (
    GENESIS_HASH, ChainIssue, ChainReport, chain_record, envelope, record_hash, row_hash, split_envelope,
    verify_links, verify_record_chain,
)


def test_row_hash_is_sha256_of_prev_and_payload() -> None:
    payload = '{"body":{},"class":null,"kind":"drill","recorded_at":"2026-10-18T09:15:00.000000Z"}'
    expected = "sha256:" + hashlib.sha256(GENESIS_HASH.encode("ascii") + payload.encode("utf-8")).hexdigest()
    assert row_hash(GENESIS_HASH, payload) == row_hash(GENESIS_HASH, payload.encode("utf-8")) == expected
    assert GENESIS_HASH == "sha256:" + "0" * 64


@pytest.mark.parametrize("body", [{}, {"a": 1, "b": [1.5, None, "x"]}, {"z": {"y": "SYNTHETIC – NOT ADIC DATA"}}])
@pytest.mark.parametrize("cls", [None, "adic_tpa.contracts.evidence:MetricDef"])
def test_envelope_is_canonical_json(body: dict, cls: str | None) -> None:
    text = envelope("metric", canonical_json(body).decode("utf-8"), cls=cls, recorded_at="2026-10-18T09:15:00.5Z")
    parsed = json.loads(text)
    assert canonical_json(parsed).decode("utf-8") == text
    assert parsed == {"body": body, "class": cls, "kind": "metric", "recorded_at": "2026-10-18T09:15:00.5Z"}
    body_text, header = split_envelope(text)
    assert json.loads(body_text) == body and header == {"class": cls, "kind": "metric",
                                                         "recorded_at": "2026-10-18T09:15:00.5Z"}


def test_split_envelope_survives_class_markers_inside_the_body() -> None:
    body = canonical_json({"note": ',"class":"x"', "class": "inner"}).decode("utf-8")
    text = envelope("claim", body, cls="m:C", recorded_at="t")
    assert split_envelope(text) == (body, {"class": "m:C", "kind": "claim", "recorded_at": "t"})
    with pytest.raises(SchemaError):
        split_envelope('{"not":"an envelope"}')


def _rows(n: int) -> list[tuple[int, str, str, str]]:
    rows, prev = [], GENESIS_HASH
    for seq in range(1, n + 1):
        payload = envelope("drill", canonical_json({"i": seq}).decode(), cls=None, recorded_at="t")
        digest = row_hash(prev, payload)
        rows.append((seq, payload, prev, digest))
        prev = digest
    return rows


def test_intact_rows_verify() -> None:
    rows = _rows(5)
    count, head, issues = verify_links(rows)
    assert (count, head, issues) == (5, rows[-1][3], [])
    assert verify_links([]) == (0, GENESIS_HASH, [])


def test_an_edited_row_is_named() -> None:
    rows = _rows(5)
    seq, payload, prev, digest = rows[2]
    rows[2] = (seq, payload.replace('"i":3', '"i":4'), prev, digest)
    _, _, issues = verify_links(rows)
    assert [i.seq for i in issues] == [3] and "edited" in issues[0].reason


def test_a_rewritten_row_is_named_by_the_broken_link() -> None:
    rows = _rows(5)
    seq, payload, prev, _ = rows[2]
    forged = payload.replace('"i":3', '"i":4')
    rows[2] = (seq, forged, prev, row_hash(prev, forged))           # hash recomputed to hide the edit
    _, _, issues = verify_links(rows)
    assert [i.seq for i in issues] == [3] and "rewritten" in issues[0].reason


def test_deleted_rows_and_a_bad_genesis_are_named() -> None:
    rows = _rows(5)
    _, _, issues = verify_links(rows[:2] + rows[3:])
    assert [i.seq for i in issues] == [3] and "missing" in issues[0].reason
    seq, payload, _, _ = rows[0]
    bad_start = [(seq, payload, "sha256:" + "1" * 64, row_hash("sha256:" + "1" * 64, payload))]
    assert [i.seq for i in verify_links(bad_start)[2]] == [1]


def test_record_chain_helpers(factory) -> None:
    d1 = factory.decision()
    assert d1.prev_hash == GENESIS_HASH and d1.record_hash == record_hash(d1)
    d2 = factory.decision(d1.record_hash, decision_id="dec-Q2-2026Q4-1")
    assert verify_record_chain([d1, d2]) is None
    assert verify_record_chain([d2]) == 0
    assert verify_record_chain([d1, d2.model_copy(update={"rationale": "edited"})]) == 1
    assert verify_record_chain([d2], start=d1.record_hash) is None
    # the hash covers every field except the two chain fields
    assert record_hash(d1.model_copy(update={"record_hash": "sha256:" + "9" * 64})) == d1.record_hash
    assert record_hash(d1.model_copy(update={"decision": "reject"})) != d1.record_hash
    with pytest.raises(SchemaError):
        record_hash(factory.claim())
    with pytest.raises(SchemaError):
        chain_record(factory.claim(), GENESIS_HASH)


def test_chain_report_first_bad() -> None:
    from datetime import datetime, timezone

    issues = (ChainIssue(seq=None, table="schema", reason="trigger missing"),
              ChainIssue(seq=7, table="metrics", reason="x"), ChainIssue(seq=4, table="chain", reason="y"))
    report = ChainReport(ok=False, rows=9, head=GENESIS_HASH, first_bad_seq=4, issues=issues, artifacts_checked=0,
                         checked_at=datetime.now(timezone.utc))
    assert report.first_bad == issues[2]
    schema_only = report.model_copy(update={"first_bad_seq": None, "issues": issues[:1]})
    assert schema_only.first_bad == issues[0]
    assert report.model_copy(update={"issues": (), "first_bad_seq": None}).first_bad is None
