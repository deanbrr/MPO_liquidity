"""contracts import graph (BUILD_SPEC v1.1 §4.1; owner WP-01).

``contracts.actions`` and ``contracts.optimizer`` reference each other (``LensAction`` / ``ColumnPool``); the cycle
is broken by deferred imports. These tests import a contracts module first, in a clean interpreter state, then
validate a model that crosses the cycle, so no import order can leave a model half-built. (Modules that do not
reach the cycle cannot change how it resolves.)

- PR suite: every module that imports a cycle member directly. Whichever module is imported first, the cycle is
  entered through one of these, and the cycle members import nothing above them.
- Nightly (``slow``): every module that reaches the cycle at all (about 25 interpreter resets; review R22).
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

PKG = Path(__file__).resolve().parents[2] / "src" / "adic_tpa"
CYCLE = {"actions", "optimizer"}

SCRIPT = r'''
import importlib, json, sys
la = {"unit_id": "SYN-PE-0001", "group": "PE", "lens": "SELL", "instrument": "lp_sale", "size_bn": 1.0,
      "exposure_delta_bn": -1.0, "financing_delta_bn": 0.0, "cash_out_bn": 0.9}
col = {"col_id": "c1", "unit_id": "SYN-PE-0001", "group": "PE", "action": la,
       "node_coeffs_ref": "run-20261018T091500Z-3f2a9c1d:cols:/c1", "cost": 0.0, "consent_p": 1.0, "lag_q": 0,
       "min_ticket_bn": 0.0, "irreversible": True}
cat = {"instruments": [], "columns": {"columns": [col], "tree_hash": "h"},
       "overlay_stress_ref": "run-20261018T091500Z-3f2a9c1d:ov:", "hash": "h"}
for first in sys.argv[1:]:
    for name in [n for n in sys.modules if n.startswith("adic_tpa")]:
        del sys.modules[name]
    importlib.import_module("adic_tpa.contracts." + first)
    actions = importlib.import_module("adic_tpa.contracts.actions")
    obj = actions.ActionCatalogue.model_validate_json(json.dumps(cat))
    assert obj.columns.columns[0].action.lens.value == "SELL", first
print(len(sys.argv) - 1)
'''


def _contracts_edges() -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {}
    for path in (PKG / "contracts").glob("*.py"):
        deps: set[str] = set()
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("adic_tpa.contracts."):
                deps.add(node.module.rsplit(".", 1)[1])
        edges[path.stem] = deps
    return edges


def _reaching_cycle(edges: dict[str, set[str]]) -> list[str]:
    def reaches(mod: str, seen: set[str]) -> bool:
        if mod in CYCLE:
            return True
        seen.add(mod)
        return any(dep not in seen and reaches(dep, seen) for dep in edges.get(mod, ()))
    return sorted(m for m in edges if m != "__init__" and reaches(m, set()))


def _direct_importers(edges: dict[str, set[str]]) -> list[str]:
    return sorted(m for m, deps in edges.items() if m in CYCLE or deps & CYCLE)


def _import_each_first(first: list[str]) -> None:
    env = {"PYTHONPATH": str(PKG.parent), "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows")}
    out = subprocess.run([sys.executable, "-c", SCRIPT, *first], capture_output=True, text=True, timeout=120,
                         env=env, check=False)
    assert out.returncode == 0, out.stderr[-3000:]
    assert int(out.stdout.strip()) == len(first)


def test_cycle_members_reference_each_other() -> None:
    edges = _contracts_edges()
    assert "optimizer" in edges["actions"] and "actions" in edges["optimizer"]


def test_every_direct_importer_of_the_cycle_imports_first() -> None:
    first = _direct_importers(_contracts_edges())
    assert {"actions", "optimizer", "ports", "tools", "contract", "engine_io"} <= set(first)
    _import_each_first(first)


@pytest.mark.slow
def test_every_cycle_reaching_module_imports_first() -> None:
    first = _reaching_cycle(_contracts_edges())
    assert set(_direct_importers(_contracts_edges())) < set(first)
    _import_each_first(first)
