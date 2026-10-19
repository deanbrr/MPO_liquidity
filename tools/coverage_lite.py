"""Line coverage with Python 3.12's ``sys.monitoring`` (BUILD_SPEC v1.1 §10.3; owner WP-03).

coverage.py is not installed, so this tool records LINE events for files under ``--source`` while pytest runs
in-process, and reports per module: executable lines (from the compiled code objects), lines hit, and the public
functions (names in the module's ``__all__`` that are functions or classes' methods defined in it) never entered.
Targets (§10.3): ≥ 85% of lines in every engine package, ≥ 90% in contracts, ledger, core.phase1/phase2/duals,
claims.validator, evaluator.gates and seal, and 100% of ``__all__`` functions called by a test.

Usage (PowerShell)::

    & "C:\\users\\dean\\ai_envs\\adic_tpa_lab\\.venv\\Scripts\\python.exe" tools\\coverage_lite.py `
        --source src\\adic_tpa\\testing --fail-under 85 -- tests\\unit -q -p no:cacheprovider

Everything after ``--`` goes to pytest. ``--json PATH`` writes the report as JSON. The exit code is pytest's, or 2
when a module falls below ``--fail-under`` (or a public function is never called with ``--require-public``).
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import types
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL_NAME = "coverage_lite"


@dataclass
class FileReport:
    path: str
    executable: int
    hit: int
    missing: list[int] = field(default_factory=list)
    public_never_called: list[str] = field(default_factory=list)

    @property
    def percent(self) -> float:
        return 100.0 if self.executable == 0 else 100.0 * self.hit / self.executable


def _code_objects(code: types.CodeType) -> Iterable[types.CodeType]:
    yield code
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            yield from _code_objects(const)


def executable_lines(path: Path) -> set[int]:
    """Line numbers that carry bytecode (docstring-only and blank lines excluded)."""
    source = path.read_text(encoding="utf-8")
    code = compile(source, str(path), "exec")
    lines: set[int] = set()
    for co in _code_objects(code):
        for _start, _end, line in co.co_lines():
            if line is not None and line > 0:
                lines.add(line)
    tree = ast.parse(source)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docstrings.update(range(body[0].lineno, (body[0].end_lineno or body[0].lineno) + 1))
    return lines - docstrings


def public_functions(path: Path) -> dict[str, int]:
    """``__all__`` names that are module-level functions, with their first line (classes count their methods)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    exported: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            try:
                exported = set(ast.literal_eval(node.value))
            except ValueError:
                exported = set()
    out: dict[str, int] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in exported:
            out[node.name] = node.lineno
        elif isinstance(node, ast.ClassDef) and node.name in exported:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                    out[f"{node.name}.{item.name}"] = item.lineno
    return out


class LineRecorder:
    """Registers a ``sys.monitoring`` tool that records (file, line) pairs under the given roots."""

    def __init__(self, roots: Sequence[Path]) -> None:
        self.roots = tuple(str(Path(r).resolve()).lower() for r in roots)
        self.hits: dict[str, set[int]] = {}
        self.started: set[tuple[str, int]] = set()
        self.tool_id: int | None = None

    def _wanted(self, filename: str) -> bool:
        return filename.lower().startswith(self.roots)

    def _line(self, code: types.CodeType, line: int) -> object:
        if self._wanted(code.co_filename):
            self.hits.setdefault(str(Path(code.co_filename).resolve()), set()).add(line)
        return sys.monitoring.DISABLE

    def _start(self, code: types.CodeType, offset: int) -> object:
        if self._wanted(code.co_filename):
            self.started.add((str(Path(code.co_filename).resolve()), code.co_firstlineno))
        return sys.monitoring.DISABLE

    def start(self) -> None:
        mon = sys.monitoring
        for candidate in (mon.COVERAGE_ID, 4, 3):
            if mon.get_tool(candidate) is None:
                self.tool_id = candidate
                break
        if self.tool_id is None:
            raise RuntimeError("coverage_lite: no free sys.monitoring tool id")
        mon.use_tool_id(self.tool_id, TOOL_NAME)
        mon.restart_events()          # re-arm locations an earlier recorder disabled (DISABLE persists per location)
        mon.register_callback(self.tool_id, mon.events.LINE, self._line)
        mon.register_callback(self.tool_id, mon.events.PY_START, self._start)
        mon.set_events(self.tool_id, mon.events.LINE | mon.events.PY_START)

    def stop(self) -> None:
        if self.tool_id is None:
            return
        mon = sys.monitoring
        mon.set_events(self.tool_id, 0)
        mon.register_callback(self.tool_id, mon.events.LINE, None)
        mon.register_callback(self.tool_id, mon.events.PY_START, None)
        mon.free_tool_id(self.tool_id)
        self.tool_id = None


def report(recorder: LineRecorder, sources: Sequence[Path]) -> list[FileReport]:
    out = []
    for root in sources:
        files = [root] if root.is_file() else sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)
        for path in files:
            resolved = str(path.resolve())
            lines = executable_lines(path)
            hit = recorder.hits.get(resolved, set()) & lines
            started_lines = {line for f, line in recorder.started if f == resolved}
            never = sorted(name for name, line in public_functions(path).items() if line not in started_lines
                           and not _decorated_start(path, line, started_lines))
            out.append(FileReport(path=_display(path), executable=len(lines), hit=len(hit),
                                  missing=sorted(lines - hit), public_never_called=never))
    return out


def _decorated_start(path: Path, def_line: int, started: set[int]) -> bool:
    """A decorated function's code object starts at its first decorator line, not at ``def``."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno == def_line and node.decorator_list:
            return min(d.lineno for d in node.decorator_list) in started
    return False


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def format_table(reports: Sequence[FileReport]) -> str:
    rows = [f"{'module':70s} {'lines':>6s} {'hit':>6s} {'cover':>7s}  public never called"]
    for r in reports:
        rows.append(f"{r.path:70s} {r.executable:6d} {r.hit:6d} {r.percent:6.1f}%  {', '.join(r.public_never_called)}")
    total_exec = sum(r.executable for r in reports)
    total_hit = sum(r.hit for r in reports)
    pct = 100.0 if total_exec == 0 else 100.0 * total_hit / total_exec
    rows.append(f"{'TOTAL':70s} {total_exec:6d} {total_hit:6d} {pct:6.1f}%")
    return "\n".join(rows)


def main(argv: Sequence[str] | None = None) -> int:
    args_in = list(sys.argv[1:] if argv is None else argv)
    pytest_args: list[str] = []
    if "--" in args_in:
        cut = args_in.index("--")
        args_in, pytest_args = args_in[:cut], args_in[cut + 1:]
    parser = argparse.ArgumentParser(description="Line coverage via sys.monitoring while pytest runs (§10.3).")
    parser.add_argument("--source", action="append", type=Path, required=True, help="file or directory to measure")
    parser.add_argument("--fail-under", type=float, default=0.0, help="minimum per-module line coverage, percent")
    parser.add_argument("--require-public", action="store_true", help="fail if an __all__ function is never called")
    parser.add_argument("--json", type=Path, default=None, help="write the report as JSON")
    args = parser.parse_args(args_in)
    import pytest  # imported here so the tool can be imported without pytest on the path

    recorder = LineRecorder(args.source)
    recorder.start()
    try:
        code = int(pytest.main(pytest_args))
    finally:
        recorder.stop()
    reports = report(recorder, args.source)
    print(format_table(reports))
    if args.json is not None:
        args.json.write_text(json.dumps([asdict(r) | {"percent": r.percent} for r in reports], indent=1), encoding="utf-8")
    below = [r for r in reports if r.percent < args.fail_under]
    unreached = [r for r in reports if r.public_never_called] if args.require_public else []
    if code == 0 and (below or unreached):
        return 2
    return code


if __name__ == "__main__":
    raise SystemExit(main())
