"""No hard-coded group ids (BUILD_SPEC v1.1 §4.1, S-ADR-01; owner WP-01).

Scans every string literal in ``src/adic_tpa`` except ``config/``, ``testing/`` and ``contracts/taxonomy.py``:
none may equal a configured group id or code (both taxonomies). Engine code reads group capabilities from
``GroupSpec`` flags, never names; that is also why ``CanonicalConventions.credit_cash_a`` has no code default.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from adic_tpa.contracts.taxonomy import GroupRegistry


@pytest.fixture(scope="module")
def configured_names() -> frozenset[str]:
    names: set[str] = set()
    for version in ("v1", "v2"):
        reg = GroupRegistry.for_version(version)
        names.update(str(g) for g in reg.ids())
        names.update(reg.codes())
    return frozenset(names)


def _scanned(pkg_root: Path) -> list[Path]:
    out = []
    for path in sorted(pkg_root.rglob("*.py")):
        rel = path.relative_to(pkg_root).as_posix()
        if rel.startswith(("config/", "testing/")) or rel == "contracts/taxonomy.py" or "__pycache__" in rel:
            continue
        out.append(path)
    return out


def _literals(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [(n.lineno, n.value) for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def test_configured_names_cover_both_taxonomies(configured_names: frozenset[str]) -> None:
    assert {"PE", "REALASSETS", "CF", "TPA", "SEC", "RA", "OVL"} <= configured_names


def test_no_string_literal_equals_a_group_id_or_code(configured_names: frozenset[str],
                                                     layer_rules: SimpleNamespace) -> None:
    hits = [f"{p.relative_to(layer_rules.REPO_ROOT).as_posix()}:{line}: {value!r}"
            for p in _scanned(layer_rules.PKG_ROOT) for line, value in _literals(p) if value in configured_names]
    assert not hits, "hard-coded group ids or codes (read GroupSpec flags instead):\n" + "\n".join(hits)


def test_scanner_catches_a_planted_literal(tmp_path: Path, configured_names: frozenset[str]) -> None:
    planted = tmp_path / "planted.py"
    planted.write_text('RED = ("PE", "SECONDARIES")\nok = "PE_FUND"\n', encoding="utf-8")
    found = [v for _, v in _literals(planted) if v in configured_names]
    assert found == ["PE", "SECONDARIES"]
