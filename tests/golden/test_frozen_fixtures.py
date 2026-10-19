"""Frozen fixture checksums (BUILD_SPEC v1.1 §4.5 DoD, §10.4, §10.5; owner WP-03).

The checksums of ``mini_book`` v1/v2, ``mini_cube()``, ``mini_flowcube(mini_book(), mini_cube())``,
``fixture_tree()`` and fixture H's LP are committed in ``tests/golden/frozen_fixtures.json``; any change needs
``pytest --update-golden`` and a contract-change note (§0.1, §10.4). Bit for bit on the same machine and pinned
versions (§10.5). SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import json

import pytest

from adic_tpa.contracts import CONTRACTS_VERSION
from adic_tpa.testing import check_frozen_fixtures, frozen_fixture_checksums, golden, write_frozen_fixtures
from adic_tpa.testing.golden import golden_root


def test_frozen_fixtures_reproduce(update_golden: bool) -> None:
    if update_golden:
        path = write_frozen_fixtures()
        pytest.skip(f"golden rewritten: {path}")
    problems = check_frozen_fixtures()
    assert not problems, "frozen fixtures changed (needs --update-golden and a contract-change note):\n" + \
        "\n".join(problems)


def test_frozen_file_names_every_fixture_and_the_contracts_version() -> None:
    body = golden("frozen_fixtures")
    assert body["contracts_version"] == CONTRACTS_VERSION
    assert set(body["fixtures"]) == {"mini_book_v1", "mini_book_v2", "mini_cube", "mini_flowcube", "fixture_tree",
                                     "fixture_h_lp"}
    assert "SYNTHETIC" in body["note"]
    for entry in body["fixtures"].values():
        digests = [v for k, v in entry.items() if k in ("content_hash", "checksum", "tree_hash", "scenario_checksum")]
        assert digests and all(isinstance(d, str) and d.startswith("sha256:") for d in digests)


def test_checksums_are_deterministic_within_a_process() -> None:
    assert frozen_fixture_checksums() == frozen_fixture_checksums()


def test_frozen_file_is_lf_sorted_json() -> None:
    raw = (golden_root() / "frozen_fixtures.json").read_bytes()
    assert b"\r\n" not in raw
    body = json.loads(raw)
    assert raw.decode("utf-8") == json.dumps(body, indent=1, sort_keys=True) + "\n"
