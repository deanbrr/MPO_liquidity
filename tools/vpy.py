"""Run Python with the project venv's packages, using the base interpreter.

Windows Smart App Control can block the venv launcher (`.venv\\Scripts\\python.exe`)
while still allowing the uv-managed base interpreter. This launcher adds the venv's
site-packages (processing its .pth files, so the editable `adic_tpa` install works),
exports PYTHONPATH so child processes see the same packages, then runs the target.

Usage (PowerShell):
    $py = 'C:\\Users\\dean\\AppData\\Roaming\\uv\\python\\cpython-3.12.15-windows-x86_64-none\\python.exe'
    & $py -X utf8 tools\\vpy.py path\\to\\script.py [args...]
    & $py -X utf8 tools\\vpy.py -m pytest -q tests
    & $py -X utf8 tools\\vpy.py -c "import numpy; print(numpy.__version__)"
"""
from __future__ import annotations

import os
import runpy
import site
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_SITE = ROOT / ".venv" / "Lib" / "site-packages"
SRC = ROOT / "src"


def _activate() -> None:
    site.addsitedir(str(VENV_SITE))
    extra = [str(VENV_SITE), str(SRC)]
    old = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = os.pathsep.join(extra + ([old] if old else []))
    os.environ.setdefault("PYTHONUTF8", "1")


def main() -> None:
    _activate()
    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: vpy.py (script.py | -m module | -c code) [args...]")
    if args[0] == "-m":
        sys.argv = [args[1], *args[2:]]
        sys.path[0] = os.getcwd()
        runpy.run_module(args[1], run_name="__main__", alter_sys=True)
    elif args[0] == "-c":
        sys.argv = ["-c", *args[2:]]
        sys.path[0] = os.getcwd()
        exec(compile(args[1], "<string>", "exec"), {"__name__": "__main__"})
    else:
        script = Path(args[0]).resolve()
        sys.argv = [str(script), *args[1:]]
        sys.path[0] = str(script.parent)
        runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
