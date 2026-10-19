"""Third-party import allowlist (BUILD_SPEC v1.1 §1.1; ARCH §11.8; owner WP-01).

Every import in ``src/adic_tpa`` is the standard library, ``adic_tpa`` itself, or a module of the §1.1 pinned
stack. A PyPI addition needs a written justification and an ADR before this list changes.
"""

from __future__ import annotations

from types import SimpleNamespace


def test_only_pinned_third_party_imports(import_records: list, stdlib_names: frozenset[str],
                                         layer_rules: SimpleNamespace) -> None:
    violations = sorted(f"{r.where()}: {r.target}" for r in import_records
                        if r.top != "adic_tpa" and r.top not in stdlib_names
                        and r.top not in layer_rules.ALLOWED_THIRD_PARTY)
    assert not violations, "imports outside the §1.1 allowlist:\n" + "\n".join(violations)


def test_allowlist_is_importable(layer_rules: SimpleNamespace) -> None:
    """Every allowlisted distribution the contracts layer relies on is installed in this venv."""
    import importlib.util

    needed = ("numpy", "scipy", "pydantic", "pydantic_core", "yaml", "cryptography", "jsonschema")
    missing = [name for name in needed if importlib.util.find_spec(name) is None]
    assert not missing, f"pinned stack incomplete: {missing}"


def test_contracts_use_no_heavy_optional_stack(import_records: list) -> None:
    """contracts stays light: no solver, dataframe, plotting, numba or LLM SDK at import time."""
    heavy = {"cvxpy", "highspy", "pandas", "pyarrow", "matplotlib", "plotly", "numba", "anthropic", "mcp", "scipy"}
    violations = [f"{r.where()}: {r.target}" for r in import_records
                  if r.module.startswith("adic_tpa.contracts") and r.top in heavy and not _lazy(r)]
    assert not violations, "\n".join(violations)


def _lazy(record) -> bool:
    """scipy.sparse is imported lazily inside ArrayContainer._unflatten for LPModel persistence only."""
    return record.target == "scipy" and record.module == "adic_tpa.contracts.arrays"
