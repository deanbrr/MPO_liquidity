"""``tools/coverage_lite.py``: line coverage through ``sys.monitoring`` (BUILD_SPEC v1.1 §10.3; owner WP-03)."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType

import pytest

REPO = Path(__file__).resolve().parents[2]
SOURCE = '''"""Module docstring."""
__all__ = ["used", "unused", "Klass"]


def used(x):
    """Function docstring."""
    if x > 0:
        return 1
    return 2


def unused():
    return 3


class Klass:
    def method(self):
        return 4
'''


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def tool() -> Iterator[ModuleType]:
    module = _load("coverage_lite_under_test", REPO / "tools" / "coverage_lite.py")
    yield module
    sys.modules.pop("coverage_lite_under_test", None)


def test_static_analysis(tool: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "sample_mod.py"
    path.write_text(SOURCE, encoding="utf-8")
    lines = tool.executable_lines(path)
    assert {2, 5, 7, 8, 9, 12, 13, 16, 17, 18} <= lines
    assert not lines & {1, 6}, "docstrings are not executable lines"
    assert tool.public_functions(path) == {"used": 5, "unused": 12, "Klass.method": 17}


def test_recorder_reports_hits_misses_and_unreached_public_functions(tool: ModuleType, tmp_path: Path) -> None:
    path = (tmp_path / "sample_cov.py").resolve()
    path.write_text(SOURCE, encoding="utf-8")
    recorder = tool.LineRecorder([tmp_path])
    recorder.start()
    try:
        module = _load("sample_cov_under_test", path)
        assert module.used(1) == 1
    finally:
        recorder.stop()
        sys.modules.pop("sample_cov_under_test", None)
    (rep,) = tool.report(recorder, [path])
    assert {9, 13, 18} <= set(rep.missing) and not {7, 8} & set(rep.missing)
    assert rep.public_never_called == ["Klass.method", "unused"]
    assert 0.0 < rep.percent < 100.0
    table = tool.format_table([rep])
    assert "TOTAL" in table and "unused" in table
    assert recorder.tool_id is None, "stop() frees the sys.monitoring tool id"
