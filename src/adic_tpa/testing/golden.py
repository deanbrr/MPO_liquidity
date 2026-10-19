"""Golden files: loader, frozen-fixture checksums and manifest reproduction (BUILD_SPEC v1.1 §4.5, §10.4, §10.5;
owner WP-03).

SYNTHETIC – NOT ADIC DATA.

- ``golden(name)`` loads ``tests/golden/<name>`` or the ported research fixture ``tests/regression/fixtures/<name>``
  (``.json`` parsed, ``.csv`` as a list of rows, ``.npz`` as a dict of arrays, other text as ``str``). A ported
  fixture is checked against ``port_manifest.json`` first, so an edited copy raises ``HashMismatch``.
- ``frozen_fixture_checksums()`` recomputes the checksums frozen in ``tests/golden/frozen_fixtures.json`` (mini book
  v1/v2, mini cube, mini FlowCube, fixture tree, fixture H's LP); ``check_frozen_fixtures()`` lists differences and
  ``write_frozen_fixtures()`` is the ``pytest --update-golden`` path (§10.4: needs a contract-change note).
- ``assert_manifest_reproduces(manifest_path)`` re-runs a golden ``RunManifest`` through the entry point named in
  its sibling ``rerun.json`` and compares ``canonical_artifact_hash`` of every artifact (§4.1, §9.4 #9).
"""

from __future__ import annotations

import csv
import importlib
import io
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Final

import numpy as np

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts import CONTRACTS_VERSION
from adic_tpa.contracts.config import load_json_payload
from adic_tpa.contracts.errors import HashMismatch, SchemaError
from adic_tpa.contracts.evidence import RunManifest
from adic_tpa.contracts.hashing import canonical_artifact_hash, file_hash, package_root

__all__ = [
    "tests_root", "golden_root", "regression_fixtures_root", "golden_path", "golden", "port_manifest",
    "FROZEN_FIXTURES_FILE", "frozen_fixture_checksums", "check_frozen_fixtures", "write_frozen_fixtures",
    "rerun_frozen_fixtures", "RERUN_FILE", "assert_manifest_reproduces",
]

FROZEN_FIXTURES_FILE: Final = "frozen_fixtures.json"
RERUN_FILE: Final = "rerun.json"
_PORT_MANIFEST: Final = "port_manifest.json"
_TEXT: Final = frozenset({".txt", ".md", ".py", ".yaml", ".yml", ".csv"})


def tests_root() -> Path:
    """``tests/`` of the running checkout (the testing kit is a development tool: it needs the repository)."""
    root = package_root().parents[1] / "tests"
    if not root.is_dir():
        raise SchemaError(f"tests_root: {root} is not a directory (the golden files live in the repository)")
    return root


def golden_root() -> Path:
    return tests_root() / "golden"


def regression_fixtures_root() -> Path:
    return tests_root() / "regression" / "fixtures"


def golden_path(name: str) -> Path:
    """Resolve ``name`` (``.json`` implied when no suffix) under ``tests/golden`` then the ported fixtures."""
    rel = Path(name)
    candidates = [rel] if rel.suffix else [rel.with_suffix(".json"), rel]
    for base in (golden_root(), regression_fixtures_root()):
        for cand in candidates:
            path = (base / cand).resolve()
            if base.resolve() in path.parents and path.is_file():
                return path
    raise SchemaError(f"golden: no golden file {name!r} under tests/golden or tests/regression/fixtures")


def port_manifest() -> dict[str, Any]:
    """``tests/regression/fixtures/port_manifest.json`` (written by ``tools/port_research.py``)."""
    path = regression_fixtures_root() / _PORT_MANIFEST
    if not path.is_file():
        raise SchemaError(f"{path} is missing; run tools/port_research.py")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _verify_port(path: Path) -> None:
    root = regression_fixtures_root().resolve()
    if root not in path.parents or path.name == _PORT_MANIFEST:
        return
    rel = path.relative_to(root).as_posix()
    entry = next((e for e in port_manifest()["entries"] if e["fixture"] == rel), None)
    if entry is None:
        return
    actual = file_hash(path)
    if actual != entry["sha256"]:
        raise HashMismatch(f"ported fixture {rel} was edited: {actual} != manifest {entry['sha256']}",
                           {"fixture": rel, "expected": entry["sha256"], "actual": actual})


def golden(name: str) -> Any:
    """Load a golden file (§4.5): JSON → parsed; CSV → list of row dicts (comment lines skipped); NPZ → dict of
    arrays; other text → str. Ported research fixtures are hash-checked against the port manifest first."""
    path = golden_path(name)
    _verify_port(path)
    suffix = path.suffix.lower()
    if suffix == ".json":
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    if suffix == ".npz":
        with np.load(path, allow_pickle=False) as store:
            return {k: store[k] for k in store.files}
    text = path.read_text(encoding="utf-8")
    if suffix == ".csv":
        lines = [ln for ln in text.splitlines() if ln and not ln.startswith("#")]
        return list(csv.DictReader(io.StringIO("\n".join(lines))))
    if suffix in _TEXT:
        return text
    return path.read_bytes()


# --------------------------------------------------------------------------------------------- frozen fixtures
def frozen_fixture_checksums() -> dict[str, dict[str, Any]]:
    """Checksums of the frozen fixtures (§4.5 DoD; §10.4), recomputed now."""
    from adic_tpa.testing.fixture_h import build_fixture_lp
    from adic_tpa.testing.fixtures import mini_book, mini_cube, mini_flowcube
    from adic_tpa.testing.trees import fixture_tree

    book_v1, book_v2 = mini_book("v1"), mini_book("v2")
    cube = mini_cube()
    flows = mini_flowcube(book_v2, cube)
    tree = fixture_tree()
    lp = build_fixture_lp("canonical")
    return {
        "mini_book_v1": {"call": "mini_book('v1', seed=7)", "content_hash": book_v1.content_hash,
                         "nav_total_reported_bn": book_v1.nav_total_reported_bn, "n_holdings": len(book_v1.holdings)},
        "mini_book_v2": {"call": "mini_book('v2', seed=7)", "content_hash": book_v2.content_hash,
                         "nav_total_reported_bn": book_v2.nav_total_reported_bn, "n_holdings": len(book_v2.holdings)},
        "mini_cube": {"call": "mini_cube(200, 'M1', seed=7)", "checksum": cube.checksum(),
                      "scenario_checksum": cube.meta.checksum, "shape": list(cube.factors.shape)},
        "mini_flowcube": {"call": "mini_flowcube(mini_book('v2'), mini_cube())", "checksum": flows.checksum(),
                          "shape": list(flows.values.shape)},
        "fixture_tree": {"call": "fixture_tree((2, 2, 2), unreduced=True)", "checksum": tree.checksum(),
                         "tree_hash": tree.tree_hash, "n_nodes": int(tree.p.size)},
        "fixture_h_lp": {"call": "build_fixture_lp('canonical')", "checksum": lp.checksum(),
                         "shape": [len(lp.row_keys), len(lp.col_keys)]},
    }


def _frozen_path() -> Path:
    return golden_root() / FROZEN_FIXTURES_FILE


def check_frozen_fixtures() -> list[str]:
    """Differences between the recomputed and the committed frozen checksums (empty list: all reproduce)."""
    path = _frozen_path()
    if not path.is_file():
        return [f"{path} is missing; run pytest --update-golden"]
    with open(path, encoding="utf-8") as fh:
        frozen = json.load(fh)["fixtures"]
    now = frozen_fixture_checksums()
    problems = []
    for name in sorted(set(frozen) | set(now)):
        if name not in now or name not in frozen:
            problems.append(f"{name}: present on one side only")
            continue
        for key in sorted(set(frozen[name]) | set(now[name])):
            if frozen[name].get(key) != now[name].get(key):
                problems.append(f"{name}.{key}: frozen {frozen[name].get(key)!r} != now {now[name].get(key)!r}")
    return problems


def write_frozen_fixtures() -> Path:
    """Rewrite ``tests/golden/frozen_fixtures.json`` (``pytest --update-golden``; §10.4 contract-change note)."""
    path = _frozen_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"note": f"{SYNTHETIC_FOOTER}. Frozen checksums of the WP-03 fixtures (BUILD_SPEC §4.5 DoD, §10.4). "
                    "Bit for bit on the same machine and pinned versions (§10.5); changing one needs "
                    "pytest --update-golden and a contract-change note.",
            "contracts_version": CONTRACTS_VERSION, "fixtures": frozen_fixture_checksums()}
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(body, indent=1, sort_keys=True) + "\n")
    return path


def rerun_frozen_fixtures(manifest: RunManifest) -> dict[str, Any]:
    """Re-run entry point of a frozen-fixture golden manifest: the fixtures themselves, by artifact name."""
    from adic_tpa.testing.fixtures import mini_book, mini_cube, mini_flowcube
    from adic_tpa.testing.trees import fixture_tree

    del manifest
    cube = mini_cube()
    return {"mini_book_v1": mini_book("v1"), "mini_book_v2": mini_book("v2"), "mini_cube": cube,
            "mini_flowcube": mini_flowcube(mini_book("v2"), cube), "fixture_tree": fixture_tree()}


# ------------------------------------------------------------------------------------------ manifest reproduce
def _resolve(entry: str) -> Callable[..., Mapping[str, Any]]:
    module, _, attr = entry.partition(":")
    if not module.startswith("adic_tpa.") or not attr:
        raise SchemaError(f"rerun entry {entry!r} must be 'adic_tpa.<module>:<function>'")
    fn = getattr(importlib.import_module(module), attr, None)
    if not callable(fn):
        raise SchemaError(f"rerun entry {entry!r} is not callable")
    return fn


def assert_manifest_reproduces(manifest_path: Path, *,
                               rerun: Callable[..., Mapping[str, Any]] | None = None) -> None:
    """Re-run a manifest and compare canonical artifact hashes (§4.1, §9.4 #9); raise ``HashMismatch`` on any
    difference, a missing artifact or an artifact the manifest does not list.

    The re-run comes from ``rerun`` or from ``rerun.json`` next to the manifest:
    ``{"entry": "adic_tpa.<module>:<function>", "kwargs": {...}}``; the function takes the ``RunManifest`` and the
    kwargs and returns the artifacts by name.
    """
    path = Path(manifest_path)
    manifest = load_json_payload(path.read_bytes(), RunManifest)
    kwargs: dict[str, Any] = {}
    if rerun is None:
        spec_path = path.parent / RERUN_FILE
        if not spec_path.is_file():
            raise SchemaError(f"{path}: no rerun callable given and no {RERUN_FILE} beside the manifest")
        with open(spec_path, encoding="utf-8") as fh:
            spec = json.load(fh)
        rerun = _resolve(spec["entry"])
        kwargs = dict(spec.get("kwargs", {}))
    artifacts = rerun(manifest, **kwargs)
    expected = dict(manifest.canonical_artifact_hashes)
    actual = {name: canonical_artifact_hash(obj) for name, obj in artifacts.items()}
    problems = [f"{name}: expected {expected[name]}, got {actual.get(name, '<missing>')}"
                for name in sorted(expected) if actual.get(name) != expected[name]]
    problems += [f"{name}: produced but not listed in the manifest" for name in sorted(set(actual) - set(expected))]
    if problems:
        raise HashMismatch(f"{path}: run {manifest.run_id} does not reproduce: " + "; ".join(problems),
                           {"manifest": str(path), "problems": problems})
