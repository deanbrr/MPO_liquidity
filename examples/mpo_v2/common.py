"""Shared utilities for the MPO v2 prototype (SYNTHETIC - NOT ADIC DATA).

- Params: read-only access to params.json with usage tracking, so the run can list any parameter that the code
  never read (every number the program uses must live in params.json with a rationale and a source).
- Log: one run log (stdout + run_log.txt) used by every component; every LP/MIP solve writes status and size here.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LABEL = "SYNTHETIC - NOT ADIC DATA"

MACRO = ["expansion", "late_cycle", "crisis", "recovery"]
EXIT = ["open", "normal", "drought", "frozen"]
OIL = ["normal", "boom", "glut", "demand_bust", "supply_shock", "gulf_war"]
FACTORS = ["eq", "cr", "rt", "oil", "ex", "vol"]
CLASSES = ["BEN", "DRT", "STR"]
STAGES = ["Green", "Amber", "Red", "Black"]
GROUPS = ["PE", "SEC", "CO", "CS", "PC", "HF", "LO", "RA"]
GROUP_NAMES = {"PE": "PE funds", "SEC": "Secondaries", "CO": "Co-investment", "CS": "Capital Solutions",
               "PC": "Private Credit", "HF": "Public Markets (hedge funds)", "LO": "Public Markets (long-only)",
               "RA": "Real Assets", "OV": "Overlay", "CF": "Corporate Finance"}


class Params:
    """Nested params.json; leaves are {"value", "unit", "rationale", "source"}. get('a.b.c') returns the value."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.used: set[str] = set()
        self.overrides: dict[str, object] = {}

    def _leaf(self, key: str):
        node = self.raw
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                raise KeyError(f"params.json has no entry '{key}'")
            node = node[part]
        if not (isinstance(node, dict) and "value" in node):
            raise KeyError(f"params.json entry '{key}' is not a leaf with a 'value'")
        return node

    def get(self, key: str):
        self.used.add(key)
        if key in self.overrides:
            return self.overrides[key]
        return self._leaf(key)["value"]

    def arr(self, key: str) -> np.ndarray:
        return np.asarray(self.get(key), dtype=float)

    def leaves(self, node=None, prefix=""):
        node = self.raw if node is None else node
        out = []
        for k, v in node.items():
            if k.startswith("_"):
                continue
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and "value" in v:
                out.append(key)
            elif isinstance(v, dict):
                out.extend(self.leaves(v, key))
        return out

    def unused(self) -> list[str]:
        return [k for k in self.leaves() if k not in self.used]

    def missing_metadata(self) -> list[str]:
        bad = []
        for k in self.leaves():
            leaf = self._leaf(k)
            if not all(leaf.get(f) for f in ("unit", "rationale", "source")):
                bad.append(k)
        return bad

    def hash(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()[:16]


class Log:
    def __init__(self, path: Path | None = None, quiet: bool = False):
        self.path = path
        self.quiet = quiet
        self.lines: list[str] = []
        self.t0 = time.time()
        self.solves: list[dict] = []

    def __call__(self, msg: str = ""):
        line = f"[{time.time() - self.t0:7.1f}s] {msg}"
        self.lines.append(line)
        if not self.quiet:
            print(line, flush=True)

    def solve(self, rec: dict):
        self.solves.append(rec)
        self(f"  solve {rec['name']}: {rec['kind']} status={rec['status']} cols={rec['cols']} rows={rec['rows']} "
             f"nnz={rec['nnz']} ints={rec.get('ints', 0)} time={rec['time_s']:.2f}s"
             + (f" gap={rec['mip_gap']:.4f} nodes={rec['mip_nodes']}" if rec.get('ints') else "")
             + (f" obj={rec['obj']:.6g}" if rec.get('obj') is not None else ""))

    def save(self):
        if self.path is not None:
            self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def wilson(k: float, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (float(c - h), float(c + h))


def clopper_pearson_upper(k: int, n: int, conf: float = 0.95) -> float:
    from scipy.stats import beta
    if k >= n:
        return 1.0
    return float(beta.ppf(conf, k + 1, n - k))


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running = {}, 0.0
    for r, (k, p) in enumerate(items):
        adj = min(1.0, (m - r) * p)
        running = max(running, adj)
        out[k] = running
    return out


def sarle_bimodality(x: np.ndarray) -> float:
    from scipy.stats import kurtosis, skew
    n = len(x)
    g = skew(x)
    k = kurtosis(x)  # excess
    return float((g * g + 1) / (k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))))


def cvar_lower(x: np.ndarray, level: float, w: np.ndarray | None = None) -> float:
    """Mean of the worst `level` share of x (lower tail), exact for discrete weights."""
    x = np.asarray(x, float)
    w = np.full(len(x), 1.0 / len(x)) if w is None else np.asarray(w, float) / np.sum(w)
    o = np.argsort(x, kind="stable")
    xs, ws = x[o], w[o]
    cw = np.cumsum(ws)
    k = int(np.searchsorted(cw, level - 1e-15))
    take = ws[:k + 1].copy()
    take[-1] -= cw[k] - level
    take = np.clip(take, 0, None)
    return float(np.dot(take, xs[:k + 1]) / level)


def quantile_w(x: np.ndarray, q: float, w: np.ndarray | None = None) -> float:
    x = np.asarray(x, float)
    if w is None:
        return float(np.quantile(x, q))
    o = np.argsort(x, kind="stable")
    cw = np.cumsum(np.asarray(w, float)[o]) / np.sum(w)
    return float(x[o][min(int(np.searchsorted(cw, q)), len(x) - 1)])


def jdump(obj) -> str:
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(type(o))
    return json.dumps(obj, indent=1, default=conv, allow_nan=True)


def stable_hash(obj) -> str:
    return hashlib.sha256(jdump(obj).encode("utf-8")).hexdigest()[:16]


def r6(x):
    """Round floats recursively (6 significant decimals) for reporting and stable hashing."""
    if isinstance(x, dict):
        return {k: r6(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [r6(v) for v in x]
    if isinstance(x, (float, np.floating)):
        v = float(x)
        if not np.isfinite(v):
            return v
        return float(f"{v:.6g}")
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.ndarray):
        return r6(x.tolist())
    return x


def setup_stdout_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
