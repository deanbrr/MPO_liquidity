"""Shared machinery of the layering harness (BUILD_SPEC v1.1 §4.0, §1.1, §10.6; owner WP-01).

The import table below transcribes §4.0 (authoritative). Later WPs extend the harness by adding their own
layering tests here; changing the table itself needs a contract-change note (§0.1). Fixtures expose the parsed
import graph of ``src/adic_tpa`` so each test stays small:

- ``import_records``: every import statement of every module (AST, including function-level and
  ``TYPE_CHECKING`` imports), resolved to absolute module names.
- ``layer_rules``: the §4.0 table as data.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
PKG_ROOT = SRC_ROOT / "adic_tpa"

ANY = "*"

# §4.0 import table: layer -> layers it may import (adic_tpa). Fine-grained entries name a submodule
# ("evaluator.client"); "core.*" means every core group.
IMPORT_TABLE: dict[str, frozenset[str]] = {
    "contracts": frozenset(),
    "numerics": frozenset({"contracts"}),
    "rng": frozenset({"contracts", "numerics"}),
    "stats": frozenset({"contracts", "numerics"}),
    "testing": frozenset({"contracts", "rng", "numerics"}),
    "registry": frozenset({"contracts"}),
    "data": frozenset({"contracts"}),
    "owner": frozenset({"contracts", "rng", "numerics"}),
    "state": frozenset({"contracts", "rng", "numerics", "stats", "data", "owner"}),
    "scen": frozenset({"contracts", "rng", "numerics", "data", "state"}),
    "pub": frozenset({"contracts", "rng", "numerics"}),
    "priv": frozenset({"contracts", "rng", "numerics", "pub"}),
    "overlay": frozenset({"contracts", "rng", "numerics"}),
    "ledger": frozenset({"contracts", "numerics"}),
    "beliefs": frozenset({"contracts", "rng", "numerics", "stats", "data"}),
    "bridge": frozenset({"contracts", "numerics", "stats", "data"}),
    "synth": frozenset({"contracts", "rng", "numerics", "data", "owner", "state", "scen", "pub", "priv", "overlay"}),
    "actions": frozenset({"contracts", "rng", "numerics", "pub", "priv", "overlay", "ledger", "beliefs"}),
    "core.sim": frozenset({"contracts", "rng", "numerics", "stats", "owner", "state", "scen", "pub", "priv",
                           "overlay", "ledger", "beliefs"}),
    "core.h": frozenset({"contracts", "rng", "numerics", "ledger", "overlay", "actions", "core.sim"}),
    "core.select": frozenset({"contracts", "numerics", "stats", "ledger", "overlay", "actions", "core.sim", "core.h"}),
    "icm": frozenset({"contracts", "numerics", "ledger", "core.h"}),
    "core.mpc": frozenset({"contracts", "numerics", "stats", "state", "beliefs", "actions", "core.sim", "core.h",
                           "core.select", "icm"}),
    "core.dsl": frozenset({"contracts", "rng", "numerics", "core.sim"}),
    "robust": frozenset({"contracts", "numerics", "stats"}),
    "attrib": frozenset({"contracts", "numerics", "stats", "owner", "core.sim", "core.h", "core.select", "core.dsl",
                         "icm", "robust"}),
    "evaluator": frozenset({"contracts", "registry", "rng", "numerics", "stats", "data", "owner", "state", "scen",
                            "pub", "priv", "overlay", "ledger", "beliefs", "bridge", "actions", "core.*", "icm",
                            "robust", "attrib"}),
    "seal": frozenset({"contracts", "registry", "evaluator.client"}),
    "claims": frozenset({"contracts", "registry"}),
    "agents": frozenset({"contracts", "registry", "claims"}),
    "lab": frozenset({"contracts", "registry", "claims", "agents", "evaluator.client", "seal"}),
    "idm": frozenset({"contracts", "registry", "claims", "agents", "evaluator.client"}),
    "pack": frozenset({"contracts", "registry", "claims", "idm"}),
    "analyst": frozenset({"contracts", "registry", "claims", "agents", "evaluator.client"}),
    "mcp_server": frozenset({"contracts", "registry", "evaluator.server", "analyst.server"}),
    "cli": frozenset({ANY}),
    "pipeline": frozenset({ANY}),
    "__main__": frozenset({ANY}),   # WP-29: python -m adic_tpa -> cli.app (same rule as cli)
}
# "evaluator (client and runner only)": seal's runner spawns the final-plane evaluator.
MODULE_OVERRIDES: dict[str, frozenset[str]] = {"adic_tpa.seal.runner": frozenset({"evaluator"})}

CORE_GROUPS: dict[str, str] = {
    **{m: "core.sim" for m in ("observables", "sim", "factory", "policy", "terminal", "certify")},
    **{m: "core.h" for m in ("tree", "h", "solver", "phase1", "phase2", "duals", "kernel")},
    **{m: "core.select" for m in ("colgen", "levelb", "safety")},
    "mpc": "core.mpc",
    **{m: "core.dsl" for m in ("dsl", "search")},
    "irb": "attrib",               # "attrib (+ core.irb)"
}
# Engine modules: everything above `evaluator` in the table (§4.0).
ENGINE_LAYERS: frozenset[str] = frozenset({
    "contracts", "numerics", "rng", "stats", "testing", "registry", "data", "owner", "state", "scen", "pub", "priv",
    "overlay", "ledger", "beliefs", "bridge", "synth", "actions", "core.sim", "core.h", "core.select", "icm",
    "core.mpc", "core.dsl", "robust", "attrib"})
NETWORK_MODULES: frozenset[str] = frozenset({"socket", "http", "urllib", "requests", "httpx", "anthropic", "mcp"})
FORBIDDEN_FOR_ENGINES: frozenset[str] = frozenset({"lab", "agents", "claims", "idm", "pack", "analyst", "pipeline"})

# §1.1 pinned stack as import names (pywin32 ships several top-level modules); anything else fails test_allowlist.
ALLOWED_THIRD_PARTY: frozenset[str] = frozenset({
    "numpy", "scipy", "pandas", "pyarrow", "cvxpy", "highspy", "clarabel", "osqp", "scs", "statsmodels", "sklearn",
    "hmmlearn", "arch", "numba", "pydantic", "pydantic_core", "typer", "rich", "jinja2", "plotly", "matplotlib",
    "pytest", "hypothesis", "anthropic", "mcp", "opentelemetry", "yaml", "jsonschema", "cryptography",
    "win32api", "win32con", "win32crypt", "win32event", "win32file", "win32pipe", "win32process", "win32security",
    "win32service", "win32profile", "win32ts", "pywintypes", "winerror", "ntsecuritycon",
})


@dataclass(frozen=True)
class ImportRecord:
    module: str          # importing module, e.g. adic_tpa.contracts.book
    path: Path
    lineno: int
    target: str          # absolute imported module, e.g. adic_tpa.contracts.taxonomy or numpy.typing

    @property
    def top(self) -> str:
        return self.target.split(".", 1)[0]

    def where(self) -> str:
        try:
            shown = self.path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            shown = str(self.path)
        return f"{shown}:{self.lineno}"


def module_name(path: Path) -> str:
    rel = path.relative_to(SRC_ROOT).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _is_module(dotted: str) -> bool:
    rel = Path(*dotted.split("."))
    return (SRC_ROOT / rel).with_suffix(".py").is_file() or (SRC_ROOT / rel / "__init__.py").is_file()


def _resolve_relative(module: str, is_pkg: bool, level: int, name: str | None) -> str:
    base = module.split(".") if is_pkg else module.split(".")[:-1]
    if level > 1:
        base = base[: len(base) - (level - 1)]
    return ".".join(base + ([name] if name else []))


def parse_imports(path: Path, module: str | None = None) -> list[ImportRecord]:
    """Import records of one file; ``module`` overrides the name derived from the path (for planted files)."""
    module = module if module is not None else module_name(path)
    is_pkg = path.name == "__init__.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    records: list[ImportRecord] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            records.extend(ImportRecord(module, path, node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = _resolve_relative(module, is_pkg, node.level, node.module) if node.level else (node.module or "")
            if base == "__future__":
                continue
            for alias in node.names:
                candidate = f"{base}.{alias.name}"
                target = candidate if base.startswith("adic_tpa") and _is_module(candidate) else base
                records.append(ImportRecord(module, path, node.lineno, target))
    return records


def layer_of(module: str) -> str:
    """Layer of an adic_tpa module for the import table ("__root__" for the package root)."""
    parts = module.split(".")
    if len(parts) == 1:
        return "__root__"
    if parts[1] == "core":
        return "core.sim" if len(parts) == 2 else CORE_GROUPS.get(parts[2], f"core.{parts[2]}")
    return parts[1]


def target_keys(target: str) -> set[str]:
    """Every table key an internal import target matches (layer and fine-grained submodule)."""
    parts = target.split(".")
    keys = {layer_of(target)}
    if len(parts) >= 3 and parts[1] != "core":
        keys.add(f"{parts[1]}.{parts[2]}")
    return keys


def allowed_for(module: str) -> frozenset[str]:
    layer = layer_of(module)
    base = IMPORT_TABLE.get(layer)
    if base is None:
        return frozenset({"<unknown layer>"})
    return base | MODULE_OVERRIDES.get(module, frozenset())


def is_allowed(module: str, target: str) -> bool:
    if target == "adic_tpa":
        return True                          # the root holds only constants (__version__, SYNTHETIC_FOOTER)
    src_layer = layer_of(module)
    keys = target_keys(target)
    if src_layer in keys:
        return True                          # modules of one layer may import each other
    allowed = allowed_for(module)
    if ANY in allowed or keys & allowed:
        return True
    return "core.*" in allowed and any(k.startswith("core.") for k in keys)


def package_files() -> list[Path]:
    return sorted(p for p in PKG_ROOT.rglob("*.py") if "__pycache__" not in p.parts)


@pytest.fixture(scope="session")
def import_records() -> list[ImportRecord]:
    return [rec for path in package_files() for rec in parse_imports(path)]


@pytest.fixture(scope="session")
def stdlib_names() -> frozenset[str]:
    return frozenset(sys.stdlib_module_names)


@pytest.fixture(scope="session")
def layer_rules() -> SimpleNamespace:
    """The §4.0 rules and helpers as one namespace (test modules cannot import conftest in importlib mode)."""
    return SimpleNamespace(
        IMPORT_TABLE=IMPORT_TABLE, ENGINE_LAYERS=ENGINE_LAYERS, NETWORK_MODULES=NETWORK_MODULES,
        FORBIDDEN_FOR_ENGINES=FORBIDDEN_FOR_ENGINES, ALLOWED_THIRD_PARTY=ALLOWED_THIRD_PARTY, PKG_ROOT=PKG_ROOT,
        SRC_ROOT=SRC_ROOT, REPO_ROOT=REPO_ROOT, layer_of=layer_of, target_keys=target_keys, is_allowed=is_allowed,
        allowed_for=allowed_for, module_name=module_name, parse_imports=parse_imports, package_files=package_files,
    )
