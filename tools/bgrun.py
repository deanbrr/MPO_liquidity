"""Start a long-running command detached, then wait on it in bounded chunks.

A single tool call is limited to about 10 minutes, so a run that takes longer is
started once with `start` and then awaited with repeated `wait` calls, each of
which returns after at most --max seconds with the log tail and the state.

    $py = 'C:\\Users\\dean\\AppData\\Roaming\\uv\\python\\cpython-3.12.15-windows-x86_64-none\\python.exe'
    & $py -X utf8 tools\\bgrun.py start NAME -- <command> [args...]
    & $py -X utf8 tools\\bgrun.py wait NAME --max 540
    & $py -X utf8 tools\\bgrun.py status NAME
    & $py -X utf8 tools\\bgrun.py kill NAME

State lives in runs/bg/NAME/ (pid, command, stdout+stderr log, exit code).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG = ROOT / "runs" / "bg"

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_BREAKAWAY_FROM_JOB = 0x01000000


def _dir(name: str) -> Path:
    d = BG / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def _alive(pid: int) -> bool:
    if os.name == "nt":
        import ctypes

        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        ctypes.windll.kernel32.CloseHandle(handle)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _tail(path: Path, n: int) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-n:])


def start(name: str, cmd: list[str]) -> None:
    d = _dir(name)
    meta = d / "meta.json"
    if meta.exists():
        old = json.loads(meta.read_text(encoding="utf-8"))
        if _alive(old["pid"]):
            raise SystemExit(f"{name} is still running (pid {old['pid']}); wait for it or kill it first")
    for f in ("exit_code", "log.txt", "wrapper_log.txt"):
        (d / f).unlink(missing_ok=True)
    log = open(d / "wrapper_log.txt", "wb")
    # A small wrapper records the exit code even though this launcher has returned by then. It hands the log
    # file to the command explicitly: a console child of a detached parent would not inherit redirected handles.
    wrapper = (
        "import subprocess, pathlib; "
        f"f = open({str(d / 'log.txt')!r}, 'ab'); "
        f"r = subprocess.call({cmd!r}, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, "
        "creationflags=0x08000000); "
        f"pathlib.Path({str(d / 'exit_code')!r}).write_text(str(r))"
    )
    env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONUTF8="1")
    flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    try:
        p = subprocess.Popen([sys.executable, "-X", "utf8", "-c", wrapper], stdout=log, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, cwd=os.getcwd(), env=env,
                             creationflags=flags | (CREATE_BREAKAWAY_FROM_JOB if os.name == "nt" else 0))
    except OSError:
        p = subprocess.Popen([sys.executable, "-X", "utf8", "-c", wrapper], stdout=log, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, cwd=os.getcwd(), env=env, creationflags=flags)
    meta.write_text(json.dumps({"pid": p.pid, "cmd": cmd, "cwd": os.getcwd(), "started": time.time()}),
                    encoding="utf-8")
    print(f"started {name}: pid {p.pid}; log {d / 'log.txt'}")


def status(name: str, n: int = 30) -> bool:
    d = _dir(name)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    code = (d / "exit_code").read_text().strip() if (d / "exit_code").exists() else None
    running = _alive(meta["pid"]) and code is None
    mins = (time.time() - meta["started"]) / 60
    state = "RUNNING" if running else (f"EXITED code={code}" if code is not None else "GONE (no exit code: killed?)")
    print(f"[{name}] {state} after {mins:.1f} min")
    print(_tail(d / "log.txt", n))
    return running


def wait(name: str, max_s: float, n: int) -> None:
    d = _dir(name)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    t0 = time.time()
    while time.time() - t0 < max_s:
        if (d / "exit_code").exists() or not _alive(meta["pid"]):
            break
        time.sleep(10)
    status(name, n)


def kill(name: str) -> None:
    d = _dir(name)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    subprocess.call(["taskkill", "/PID", str(meta["pid"]), "/T", "/F"])


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="op", required=True)
    s = sub.add_parser("start")
    s.add_argument("name")
    s.add_argument("cmd", nargs=argparse.REMAINDER)
    w = sub.add_parser("wait")
    w.add_argument("name")
    w.add_argument("--max", type=float, default=540)
    w.add_argument("--tail", type=int, default=40)
    st = sub.add_parser("status")
    st.add_argument("name")
    st.add_argument("--tail", type=int, default=40)
    k = sub.add_parser("kill")
    k.add_argument("name")
    a = ap.parse_args()
    if a.op == "start":
        cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
        if not cmd:
            raise SystemExit("start needs a command after --")
        start(a.name, cmd)
    elif a.op == "wait":
        wait(a.name, a.max, a.tail)
    elif a.op == "status":
        status(a.name, a.tail)
    else:
        kill(a.name)


if __name__ == "__main__":
    main()
