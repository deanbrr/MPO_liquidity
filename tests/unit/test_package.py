"""Packaging (BUILD_SPEC v1.1 §1.1, §2, S-ADR-42): pyproject pins exactly the §1.1 stack, the version agrees, the
pytest markers exist, .gitattributes normalizes text, and tools/dev_install.py writes the .pth. Owner WP-01."""

from __future__ import annotations

import importlib.util
import sys
import tomllib
from pathlib import Path

import pytest

import adic_tpa
from adic_tpa import contracts

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

# BUILD_SPEC §1.1 "Pinned stack", verbatim as requirement specifiers.
SPEC_PINS = {
    "numpy==2.5.*", "scipy==1.18.*", "pandas==3.0.*", "pyarrow==26.*", "cvxpy==1.9.3", "highspy==1.15.1",
    "clarabel==0.11.1", "osqp==1.1.3", "scs==3.3.1", "statsmodels==0.15.*", "scikit-learn==1.9.1",
    "hmmlearn==0.3.3", "arch==8.0.*", "numba==0.68.*", "pydantic==2.14.*", "typer", "rich", "jinja2", "plotly",
    "matplotlib", "pytest", "hypothesis", "anthropic==1.15.*", "mcp==2.3.*", "opentelemetry-api", "pyyaml",
    "jsonschema", "pywin32; sys_platform == 'win32'", "cryptography==50.0.2",
}


def test_dependencies_pin_exactly_the_spec_stack() -> None:
    assert set(PYPROJECT["project"]["dependencies"]) == SPEC_PINS
    assert PYPROJECT["build-system"]["build-backend"] == "hatchling.build"
    assert PYPROJECT["project"]["scripts"]["tpa"] == "adic_tpa.cli:app"
    assert PYPROJECT["project"]["requires-python"] == ">=3.12,<3.13"


def test_installed_versions_satisfy_the_pins() -> None:
    from importlib.metadata import version

    from packaging.specifiers import SpecifierSet

    for req in SPEC_PINS:
        name, _, spec = req.split(";")[0].partition("==")
        if spec:
            assert version(name) in SpecifierSet("==" + spec), f"{name} {version(name)} violates =={spec}"


def test_version_and_footer() -> None:
    assert adic_tpa.__version__ == PYPROJECT["project"]["version"]
    assert adic_tpa.SYNTHETIC_FOOTER == contracts.SYNTHETIC_FOOTER == "SYNTHETIC – NOT ADIC DATA"


def test_pytest_configuration() -> None:
    cfg = PYPROJECT["tool"]["pytest"]["ini_options"]
    assert cfg["pythonpath"] == ["src"]
    markers = {m.split(":", 1)[0] for m in cfg["markers"]}
    assert {"slow", "perf", "requires_accounts"} <= markers


def test_gitattributes_normalizes_text_and_protects_binaries() -> None:
    lines = [ln.strip() for ln in (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()]
    assert "* text eol=lf" in lines
    assert {"*.npz binary", "*.png binary", "*.parquet binary", "*.pdf binary"} <= set(lines)


def _dev_install():
    spec = importlib.util.spec_from_file_location("dev_install", ROOT / "tools" / "dev_install.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_dev_install_writes_and_removes_the_pth(tmp_path: Path) -> None:
    dev = _dev_install()
    venv = tmp_path / "venv"
    (venv / "Lib" / "site-packages").mkdir(parents=True)
    target = dev.install(venv)
    assert target.name == "adic_tpa_dev.pth"
    assert Path(target.read_text(encoding="utf-8").strip()) == (ROOT / "src").resolve()
    assert dev.install(venv) == target                                       # idempotent
    assert dev.uninstall(venv) and not target.exists() and not dev.uninstall(venv)


@pytest.mark.skipif(sys.prefix == sys.base_prefix, reason="needs the project venv")
def test_isolated_mode_imports_this_checkout() -> None:
    assert _dev_install().check(None)
