"""Offline development install (BUILD_SPEC v1.1 §1.1; owner WP-01).

Writes ``adic_tpa_dev.pth`` into the target virtual environment's ``Lib\\site-packages``. The file holds one
line, the absolute path of the repository's ``src`` directory, so ``import adic_tpa`` works in that venv with
no build backend and no network. Site-packages ``.pth`` files are processed in isolated mode too
(``python -I``), which the evaluator and seal processes require.

Usage (PowerShell; the bare ``python`` command is never used)::

    & "C:\\users\\dean\\ai_envs\\adic_tpa_lab\\.venv\\Scripts\\python.exe" tools\\dev_install.py
    & "...\\python.exe" tools\\dev_install.py --check
    & "...\\python.exe" tools\\dev_install.py --uninstall
    & "...\\python.exe" tools\\dev_install.py --venv C:\\path\\to\\other\\.venv

Only the standard library is imported.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import sysconfig
from pathlib import Path

PTH_NAME = "adic_tpa_dev.pth"
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"


def site_packages(venv: Path | None) -> Path:
    """Return the purelib directory of ``venv``, or of the running interpreter when ``venv`` is None."""
    if venv is None:
        if sys.prefix == sys.base_prefix:
            raise SystemExit("dev_install: run with a virtual environment's python.exe or pass --venv")
        return Path(sysconfig.get_paths()["purelib"])
    candidate = venv / "Lib" / "site-packages"  # Windows venv layout
    if candidate.is_dir():
        return candidate
    posix = sorted((venv / "lib").glob("python3*/site-packages"))
    if posix:
        return posix[0]
    raise SystemExit(f"dev_install: no site-packages under {venv}")


def venv_python(venv: Path | None) -> Path:
    """Return the interpreter of ``venv`` (or the running one)."""
    if venv is None:
        return Path(sys.executable)
    for rel in ("Scripts/python.exe", "bin/python"):
        exe = venv / rel
        if exe.exists():
            return exe
    raise SystemExit(f"dev_install: no interpreter under {venv}")


def install(venv: Path | None) -> Path:
    """Write the .pth file; idempotent. Returns its path."""
    if not (SRC_DIR / "adic_tpa" / "__init__.py").is_file():
        raise SystemExit(f"dev_install: {SRC_DIR / 'adic_tpa'} is not a package")
    target = site_packages(venv) / PTH_NAME
    line = str(SRC_DIR) + "\n"
    if not target.exists() or target.read_text(encoding="utf-8") != line:
        target.write_text(line, encoding="utf-8", newline="\n")
    return target


def uninstall(venv: Path | None) -> bool:
    """Remove the .pth file; returns True if it existed."""
    target = site_packages(venv) / PTH_NAME
    if target.exists():
        target.unlink()
        return True
    return False


def check(venv: Path | None) -> bool:
    """Import adic_tpa in an isolated-mode child interpreter and confirm it resolves to this checkout."""
    exe = venv_python(venv)
    probe = "import adic_tpa, pathlib; print(pathlib.Path(adic_tpa.__file__).resolve().parent)"
    out = subprocess.run([str(exe), "-I", "-c", probe], capture_output=True, text=True, check=False)
    if out.returncode != 0:
        print(out.stderr.strip(), file=sys.stderr)
        return False
    resolved = Path(out.stdout.strip())
    expected = (SRC_DIR / "adic_tpa").resolve()
    if resolved != expected:
        print(f"dev_install: adic_tpa resolves to {resolved}, expected {expected}", file=sys.stderr)
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write adic_tpa_dev.pth into a venv (offline dev install).")
    parser.add_argument("--venv", type=Path, default=None, help="target venv (default: the running interpreter's)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify that python -I imports this checkout")
    group.add_argument("--uninstall", action="store_true", help="remove the .pth file")
    args = parser.parse_args(argv)
    venv = args.venv.resolve() if args.venv is not None else None
    if args.uninstall:
        print("removed" if uninstall(venv) else "not installed")
        return 0
    if args.check:
        ok = check(venv)
        print("ok" if ok else "FAILED")
        return 0 if ok else 1
    target = install(venv)
    print(f"wrote {target}")
    return 0 if check(venv) else 1


if __name__ == "__main__":
    raise SystemExit(main())
