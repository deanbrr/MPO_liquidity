"""Property tests of the registry chain (BUILD_SPEC v1.1 §4.6, §10.6): any sequence of appends verifies, and any
in-place edit of one row's payload is reported at exactly that row. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from adic_tpa.contracts.enums import KeyValue
from adic_tpa.registry import Registry
from adic_tpa.registry.store import LAB_LEDGER_KINDS

values = st.one_of(st.floats(allow_nan=False, allow_infinity=False, width=64), st.text(max_size=12))
entries = st.lists(st.tuples(st.sampled_from(LAB_LEDGER_KINDS), st.text(min_size=1, max_size=6), values),
                   min_size=1, max_size=12)


@settings(max_examples=20, deadline=None)
@given(entries, st.data())
def test_appends_verify_and_any_edit_is_named(rows: list, data: st.DataObject) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "registry.sqlite"
        with Registry(db, Path(tmp) / "runs") as reg:
            hashes = [reg.append_ledger(kind, KeyValue(key=key, value=value)) for kind, key, value in rows]
            report = reg.verify_chain()
            assert report.ok and report.rows == len(rows) and report.head == hashes[-1]
            assert [e.row_hash for e in reg.read_ledger()] == hashes
        target = data.draw(st.integers(1, len(rows)), label="edited row")
        con = sqlite3.connect(db)
        try:
            con.execute("DROP TRIGGER chain_no_update")
            con.execute("UPDATE chain SET payload = replace(payload, '\"kind\":', '\"kind\": ') WHERE seq = ?",
                        (target,))
            con.commit()
        finally:
            con.close()
        with Registry(db, Path(tmp) / "runs", readonly=True) as ro:
            tampered = ro.verify_chain()
        assert not tampered.ok and tampered.first_bad_seq == target
