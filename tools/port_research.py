"""Port the research fixtures into ``tests/regression/fixtures`` (BUILD_SPEC v1.1 §10.4, §5.13, §9.2 WP-03; owner WP-03).

SYNTHETIC – NOT ADIC DATA. Every ported number comes from the research prototypes (SYN-ADIC-177 working book,
allocation v1, census v1.0, research conventions) and is a calibration target or regression fixture, never an
acceptance value unless a test names it (§0.2).

Two kinds of fixture land under ``tests/regression/fixtures/<source>/``:

- **copies**: research outputs (and the scripts and inputs that define them) copied byte for byte, then marked
  read-only;
- **exports**: the extracts the specification names explicitly — the gap_02 coefficient export
  (``gap02/coefs.json``, §5.13), the G-gap_01 coefficient export (``groups_gap01/coefs.json``), the gap_02
  G*(θ) grid and per-model gap quantiles (``gap02/gstar_grid.json``, BUILD-36), the ``t1_engine.ladder``
  readings (``t1_engine/ladder_readings.json``) and the ``perf_module.py`` golden cases
  (``perf/golden_cases.json``). Exports that need research code run it in a child ``python -I`` process
  (numpy/scipy/cvxpy only, deterministic) and are cross-checked against the research's own stored results before
  they are written.

``port_manifest.json`` lists every fixture with its source file(s) and SHA-256 (``contracts.hashing.file_hash``:
CRLF→LF normalized for text files, so checkouts with any ``core.autocrlf`` agree; S-ADR-42). ``--check`` re-hashes
the sources and the fixtures and fails on any difference.

Usage (PowerShell; the bare ``python`` command is never used)::

    & "C:\\users\\dean\\ai_envs\\adic_tpa_lab\\.venv\\Scripts\\python.exe" tools\\port_research.py
    & "C:\\users\\dean\\ai_envs\\adic_tpa_lab\\.venv\\Scripts\\python.exe" tools\\port_research.py --check
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH = REPO_ROOT / "research"
FIXTURES = REPO_ROOT / "tests" / "regression" / "fixtures"
MANIFEST = FIXTURES / "port_manifest.json"

if str(REPO_ROOT / "src") not in sys.path:      # works with or without tools/dev_install.py
    sys.path.insert(0, str(REPO_ROOT / "src"))

from adic_tpa import SYNTHETIC_FOOTER  # noqa: E402
from adic_tpa.contracts.hashing import file_hash  # noqa: E402

MANIFEST_SCHEMA = "adic_tpa.port_manifest/1"
# BUILD_SPEC §6.3: the seal of the sealed census v1.1 history.
SEALED_PE_HISTORY_SHA256 = "sha256:4346dc249e83bff8d952588715a69ec038b9725ab436e0b24b8bb4227f2f54a9"
GAP02 = "addenda/gap_02_calcs"
GROUPS_GAP01 = "groups/addenda/gap_01_calcs"


@dataclass(frozen=True)
class Copy:
    """A research file copied unedited into ``fixtures/<dest>/``."""

    dest: str
    source: str            # path relative to research/


# Research outputs, plus the scripts and inputs that define them (§10.4 "Research ports").
COPIES: tuple[Copy, ...] = (
    Copy("hf_ladder", "addenda/gap_01_calcs/hf_ladder.py"),
    Copy("hf_ladder", "addenda/gap_01_calcs/hf_ladder_results.json"),
    Copy("t1_engine", f"{GAP02}/t1_engine.py"),
    Copy("t1_engine", f"{GAP02}/gap02_study.py"),
    Copy("gap02", f"{GAP02}/gap02_results.json"),
    Copy("gap02", f"{GAP02}/phase1_demo.py"),
    Copy("gap02", f"{GAP02}/phase1_demo_results.json"),
    Copy("gap02", f"{GAP02}/test_no_pinned_duals.py"),
    Copy("groups_gap01", f"{GROUPS_GAP01}/g01_core.py"),
    Copy("groups_gap01", f"{GROUPS_GAP01}/g01_results.json"),
    Copy("groups_gap01", f"{GROUPS_GAP01}/test_no_pinned_duals_groups.py"),
    Copy("perf", "groups/addenda/gap_02_calcs/perf_module.py"),
    Copy("bridge", "addenda/gap_05_calcs/bridge.py"),
    Copy("bridge", "addenda/gap_05_calcs/bridge_results.json"),
    Copy("bridge", "addenda/gap_05_calcs/jpm2026_matrix.npz"),
    Copy("v8_rerun", "addenda/gap_05_calcs/v8_rerun.py"),
    Copy("v8_rerun", "addenda/gap_05_calcs/v8_rerun_results.json"),
    Copy("simm", "addenda/gap_03_calcs/simm_offset_example.py"),
    Copy("simm", "addenda/gap_03_calcs/simm_offset_example_results.json"),
    Copy("simm", "addenda/gap_03_calcs/gap03_greek_layer_results.json"),
    Copy("sealed_pe_history", "groups/addenda/gap_02_calcs/sealed_pe_history_v1_1.csv"),
    Copy("sealed_pe_history", "groups/addenda/gap_02_calcs/seal_history.py"),
    Copy("sealed_pe_history", "groups/addenda/gap_02_calcs/seal_history_results.json"),
)


class PortError(RuntimeError):
    """A source is missing, a cross-check failed, or a fixture differs from the manifest."""


# --------------------------------------------------------------------------------------------- file helpers
def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _make_writable(path: Path) -> None:
    if path.exists():
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)


def _make_read_only(path: Path) -> None:
    os.chmod(path, stat.S_IREAD)


def _write_json(path: Path, obj: Any) -> None:
    """Exports are written as sorted, indented, ASCII JSON with LF line ends (floats by repr: exact round trip)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    _make_writable(path)
    text = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    _make_read_only(path)


def _load_json(rel: str) -> Any:
    with open(RESEARCH / rel, encoding="utf-8") as fh:
        return json.load(fh)


def _source(rel: str) -> Path:
    path = RESEARCH / rel
    if not path.is_file():
        raise PortError(f"research source missing: research/{rel}")
    return path


def _close(a: float | None, b: float | None, tol: float = 1e-12) -> bool:
    if a is None or b is None:
        return a is b
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------------------------- safe literal extraction
def _safe_eval(node: ast.AST) -> Any:
    """Literal evaluator that also accepts ``dict(k=<literal>, ...)`` calls (research constants use them)."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict" and not node.args:
        return {kw.arg: _safe_eval(kw.value) for kw in node.keywords if kw.arg is not None}
    if isinstance(node, ast.List):
        return [_safe_eval(e) for e in node.elts]
    if isinstance(node, ast.Tuple):
        return [_safe_eval(e) for e in node.elts]
    if isinstance(node, ast.Dict):
        return {_safe_eval(k): _safe_eval(v) for k, v in zip(node.keys, node.values, strict=True) if k is not None}
    return ast.literal_eval(node)


def literal_constants(path: Path, names: Sequence[str]) -> dict[str, Any]:
    """Top-level ``NAME = <literal>`` assignments of a research module, read from its AST (never executed)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in names:
                found[name] = _safe_eval(node.value)
    missing = sorted(set(names) - set(found))
    if missing:
        raise PortError(f"{_rel(path)}: literal constants not found: {missing}")
    return found


# ------------------------------------------------------------------------------------- research subprocesses
def run_research(code: str, *args: str) -> Any:
    """Run ``code`` in a child ``python -I`` (isolated: no cwd or PYTHONPATH on sys.path) and parse its stdout JSON."""
    env = dict(os.environ)       # -I already ignores PYTHON* variables; threads pinned for bit-stable BLAS sums
    env.update({"OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"})
    out = subprocess.run([sys.executable, "-I", "-B", "-c", code, *args], capture_output=True, text=True,
                         check=False, env=env, timeout=600)
    if out.returncode != 0:
        raise PortError(f"research runner failed ({out.returncode}):\n{out.stderr.strip()[-4000:]}")
    return json.loads(out.stdout)


_LADDER_RUNNER = r'''
import dataclasses, json, sys
sys.path.insert(0, sys.argv[1])
import t1_engine as E
from gap02_study import s_star, t4_literal

READINGS = {
    "s_star_0.76": s_star(0.76),
    "t4_literal": t4_literal(),
    "t4_as_written": t4_literal(floor=0.08),
    "t4_critic": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)),
}
POLICIES = {
    "do_nothing": E.Policy("A"),
    "stage_pacing_cut": E.Policy("A", pace_cut=True),
    "owner_band": E.Policy("A", band=True),
    "cut_and_band": E.Policy("A", pace_cut=True, band=True),
}
NAMED = {
    "T4_literal": t4_literal(), "T4_literal_floor8": t4_literal(floor=0.08),
    "T4_literal_fixedusd": t4_literal(draw_basis="fixed_usd"), "T4_literal_current": t4_literal(draw_basis="current"),
    "T4_literal_hf_gated": t4_literal(hf_pass=0.0), "T4_literal_hf50": t4_literal(hf_pass=0.5),
    "T4_literal_noPCCS": t4_literal(pc_cs_rates=(0.0, 0.0)),
    "T4_literal_worst_conventions": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)),
    "C3_like": s_star(0.0),
}
THETAS = [0.0, 0.35, 0.42, 0.58, 0.76, 0.79, 1.0]
A = E.Policy("A")
out = {
    "readings": {r: {"stress": dataclasses.asdict(s), "policies": {p: E.ladder(s, pol) for p, pol in POLICIES.items()}}
                 for r, s in READINGS.items()},
    "s_star_do_nothing": {f"{th:.2f}": E.ladder(s_star(th), A) for th in THETAS},
    "named_do_nothing": {k: E.ladder(s, A) for k, s in NAMED.items()},
    "gstar_grid": [E.ladder(s_star(0.02 * i), A)["gstar"] for i in range(61)],
    "policy_defaults": dataclasses.asdict(A),
}
print(json.dumps(out))
'''

_G01_RUNNER = r'''
import dataclasses, json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
import g01_core as G
from g01_core import s_star, t4_literal

READ = {"canonical": (s_star(0.76), "pricing"), "t4_literal": (t4_literal(), "reverse"),
        "critic": (t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)), "reverse")}
BASE_KEYS = ("SH_TP", "SH_TPF", "min_head_tpf_24", "argmin_24", "fac_need_24", "gstar", "nco24", "tre_t0", "enc0",
             "usable_t0")

def tolist(x):
    return x.tolist() if isinstance(x, np.ndarray) else x

readings = {}
for key, (s, role) in READ.items():
    c = G.coefficients_for(s, role)
    readings[key] = {
        "role": role, "stress": dataclasses.asdict(s), "h0": tolist(c["h0"]), "cash": tolist(c["cash"]),
        "lever": {k: {kk: tolist(vv) for kk, vv in v.items()} for k, v in c["lever"].items()},
        "card": {k: {kk: tolist(vv) for kk, vv in v.items()} for k, v in c["card"].items()},
        "commit": {g: tolist(v) for g, v in c["commit"].items()},
        "base": {k: tolist(c["base"][k]) for k in BASE_KEYS},
    }
states = {k: {"label": v["label"], "allow": v["allow"], "cards": v.get("cards", True)} for k, v in G.STATES.items()}
out = {"readings": readings, "states": states, "ig_short_t0": G.IG_SHORT_T0, "sma_sleeve": G.SMA_SLEEVE,
       "m_tiers": G.M_TIERS, "h_rows": G.H_ROWS, "group_name": G.GROUP_NAME, "w_new": G.W_NEW,
       "alpha_d": {k: list(v) for k, v in G.ALPHA_D.items()}, "prices_t0": {"sma": G.P_SMA, "cs": G.P_CS, "hf": G.P_HF},
       "nav0": G.E.NAV0}
print(json.dumps(out))
'''

_PERF_RUNNER = r'''
import datetime as dt, json, math, sys
sys.path.insert(0, sys.argv[1])
import perf_module as P

cases = json.loads(sys.stdin.read())
D = dt.date.fromisoformat

def flows(pairs):
    return [(D(d), x) for d, x in pairs]

got = []
for c in cases:
    fn, inp = c["fn"], c["inputs"]
    try:
        if fn == "xirr":
            val = P.xirr(flows(inp["flows"]))
        elif fn == "multiples":
            val = P.multiples(flows(inp["flows"]), inp["nav"])[c["output"]]
        elif fn == "ks_pme":
            val = P.ks_pme(flows(inp["flows"]), inp["nav"], D(inp["asof"]), {D(k): v for k, v in inp["index"].items()})
        elif fn == "direct_alpha":
            val = P.direct_alpha(flows(inp["flows"]), inp["nav"], D(inp["asof"]), {D(k): v for k, v in inp["index"].items()})
        elif fn == "twr":
            val = P.twr(flows(inp["vals"]), flows(inp["flows"]))
        elif fn == "credit_realized":
            val = P.credit_realized(inp["periods"])[c["output"]]
        elif fn == "overlay_pnl":
            val = P.overlay_pnl(inp["trades"], inp["ftp_rate"])[c["output"]]["pnl"]
        else:
            raise KeyError(fn)
        got.append({"name": c["name"], "value": val, "raised": None})
    except ValueError as exc:
        got.append({"name": c["name"], "value": None, "raised": type(exc).__name__})
research = [{"name": n, "passed": bool(ok), "got": g if isinstance(g, (int, float)) or g is None else None,
             "expected": e} for n, ok, g, e in P._tests()]
print(json.dumps({"version": P.VERSION, "got": got, "research_tests": research}))
'''


# ------------------------------------------------------------------------------------------------- exporters
def export_gap02_coefs() -> tuple[dict[str, Any], list[str]]:
    """gap_02's linearised t0 liquidity block (§5.13): coefficients per reading plus the research's outcomes."""
    results_rel = f"{GAP02}/phase1_demo_results.json"
    demo_rel = f"{GAP02}/phase1_demo.py"
    engine_rel = f"{GAP02}/t1_engine.py"
    res = _load_json(results_rel)
    consts = literal_constants(_source(demo_rel), ("M_TIERS", "TEST_FUNDS"))
    nav0 = literal_constants(_source(engine_rel), ("NAV0",))["NAV0"]
    keys = {"canonical": "s_star_canonical", "as_written": "T4_as_written", "critic": "T4_critic_reading"}

    def outcome(block: Mapping[str, Any]) -> dict[str, Any]:
        restored = block["restored"]
        return {
            "phase1": block["phase1"],
            "restored": {k: restored[k] for k in ("obj", "x", "sell", "duals", "relax", "status")},
            "restored_cards": [{k: c[k] for k in ("bid", "hold", "y_cash", "reservation_price", "action")}
                               for c in restored["cards"]],
            "elastic_x1_duals": block["restored_elastic_x1"]["duals"],
            "elastic_x10_duals": block["restored_elastic_x10"]["duals"],
            "cushion_on_glide_path": block["cushion_on_glide_path"],
        }

    readings = {}
    for name, key in keys.items():
        blk = res[key]
        case1 = blk["case1_elastic_modeB"]
        readings[name] = {
            "research_key": key, "stress": blk["stress"], "h0": blk["coef"]["h0"], "slope": blk["coef"]["slope"],
            "expected": {
                "case1_elastic_modeB": {"duals": case1["duals"], "u_S": case1["u_S"], "u_IG": case1["u_IG"],
                                        "x": case1["x"], "sell": case1["sell"],
                                        "cards": [{k: c[k] for k in ("reservation_price", "action")}
                                                  for c in case1["cards"]]},
                "case1_pinned_rows": blk["case1_pinned_rows"],
                "case1_dual_T4_penalty_x10": blk["case1_dual_T4_penalty_x10"],
                "modeB": outcome(blk["modeB"]),
                "modeH": outcome(blk["modeH"]),
            },
        }
    out = {
        "note": f"{SYNTHETIC_FOOTER}. gap_02 linearised H liquidity block (phase1_demo.py): T4 row = minimum 24-month "
                "TPF headroom ($bn) with finite-difference lever slopes from t1_engine.ladder; IG row = t0 T2 8% "
                "target shortfall. Lever costs and capacities are research design assumptions [I]. Units: USD bn; "
                "slopes $bn of headroom per $bn of lever (band: per unit share).",
        "source": "research/" + results_rel,
        "nav0_bn": nav0,
        "ig_short_t0_bn": res["ig_short_t0"],
        "caps": res["caps"],
        "costs": res["costs"],
        "lever_units": {k: ("share" if k == "band" else "bn") for k in res["caps"]},
        "ig_coefficients": {"reserve": 1.0, "amber": 0.89},
        "m_tiers": consts["M_TIERS"],
        "test_funds": consts["TEST_FUNDS"],
        "readings": readings,
    }
    return out, [results_rel, demo_rel, engine_rel]


def export_gstar_grid() -> tuple[dict[str, Any], list[str]]:
    """The 61-point G*(θ) grid and per-model gap quantiles of gap02_results.json (BUILD-36)."""
    rel = f"{GAP02}/gap02_results.json"
    engine_rel = f"{GAP02}/t1_engine.py"
    cal = _load_json(rel)["calibration"]
    text = _source(engine_rel).read_text(encoding="utf-8")
    levels = {}
    for name in ("gstar", "netneed8"):
        m = re.search(rf"np\.quantile\({name}, (\[[^\]]+\])\)", text)
        if m is None:
            raise PortError(f"quantile levels of {name} not found in {engine_rel}")
        levels[name] = ast.literal_eval(m.group(1))
    out = {
        "note": f"{SYNTHETIC_FOOTER}. gap_02 G*(θ) grid (do-nothing book, s*(θ), research conventions) and per-model "
                "Monte Carlo quantiles of the facility-free 24-month gap G* ($bn); allocation v1, census v1.0. "
                "ledger.theta_from_grid must reproduce theta_for to ±0.005 (BUILD-36).",
        "source": "research/" + rel,
        "theta_grid": cal["theta_grid"],
        "gstar_theta_bn": cal["gstar_theta"],
        "eps24": cal["eps24"],
        "targets_bn": cal["targets"],
        "theta_for": cal["theta_for"],
        "models": {k: v["label"] for k, v in cal["models"].items()},
        "gstar_q_levels": levels["gstar"],
        "netneed8_q_levels": levels["netneed8"],
        "per_model": cal["mc"],
    }
    if len(out["theta_grid"]) != 61 or len(out["gstar_theta_bn"]) != 61:
        raise PortError("gap02 G*(θ) grid must have 61 points")
    if any(len(v["gstar_q"]) != len(levels["gstar"]) for v in cal["mc"].values()):
        raise PortError("gstar_q length disagrees with its quantile levels")
    return out, [rel, engine_rel]


def export_ladder_readings() -> tuple[dict[str, Any], list[str]]:
    """``t1_engine.ladder`` readings (research convention set), regenerated and cross-checked against
    gap02_results.json (named readings and the G*(θ) grid must match exactly)."""
    gap02_dir = RESEARCH / GAP02
    data = run_research(_LADDER_RUNNER, str(gap02_dir))
    cal = _load_json(f"{GAP02}/gap02_results.json")["calibration"]
    for key, reading in data["named_do_nothing"].items():
        stored = cal["named"][key]
        for field, value in reading.items():
            same = _close(value, stored[field]) if isinstance(value, float) else value == stored[field]
            if not same:
                raise PortError(f"ladder {key}.{field}: regenerated {value!r} != stored {stored[field]!r}")
    if not all(_close(a, b) for a, b in zip(data["gstar_grid"], cal["gstar_theta"], strict=True)):
        raise PortError("regenerated G*(θ) grid differs from gap02_results.json")
    canonical = data["readings"]["s_star_0.76"]["policies"]["do_nothing"]
    if not (canonical["SH_TP"] == 17 and abs(canonical["min_head_tpf_24"] + 11.1) < 0.05
            and abs(canonical["fac_need_24"] - 13.9) < 0.05):
        raise PortError(f"s*(0.76) do-nothing reading disagrees with gap_02 §1.3: {canonical}")
    out = {
        "note": f"{SYNTHETIC_FOOTER}. t1_engine.ladder readings on the research book (allocation v1, census v1.0, "
                "research conventions, 80% revolver credit for s*); USD bn and months. readings: gap_02 §1.3 "
                "table (4 stresses x 4 policies); s_star_do_nothing: s*(θ) do-nothing; named_do_nothing: the "
                "named stresses of gap02_results.json (cross-checked exactly).",
        "source": "research/" + f"{GAP02}/t1_engine.py",
        "readings": data["readings"],
        "s_star_do_nothing": data["s_star_do_nothing"],
        "named_do_nothing": data["named_do_nothing"],
        "policy_defaults": data["policy_defaults"],
        "book": literal_constants(_source(f"{GAP02}/t1_engine.py"),
                                  ("NAV0", "SOFR", "TRE0", "LO0", "HF0", "PRIV0", "UNF0", "SEC_DEF0", "PC_REV0",
                                   "N_SYN0", "N_TAIL", "TAIL_PREM", "OPP_IM0", "DIST_NORMAL", "BETA", "CALL_BASE",
                                   "PRICE_N", "PRICE_C", "DROUGHT_DIST")),
    }
    return out, [f"{GAP02}/t1_engine.py", f"{GAP02}/gap02_study.py", f"{GAP02}/gap02_results.json"]


def export_groups_gap01_coefs() -> tuple[dict[str, Any], list[str]]:
    """G-gap_01's group-resolved linearisation (24 monthly T4' rows, the t0 T2 row, 13 group levers, 4 cards)."""
    data = run_research(_G01_RUNNER, str(RESEARCH / GROUPS_GAP01))
    stored = _load_json(f"{GROUPS_GAP01}/g01_results.json")
    h0_min = min(data["readings"]["canonical"]["h0"])
    if not _close(h0_min, stored["recovery_T4prime"]["h0_min"], 1e-9):
        raise PortError(f"G-gap_01 canonical h0 min {h0_min} != stored {stored['recovery_T4prime']['h0_min']}")
    if len(data["readings"]["canonical"]["h0"]) != data["h_rows"] or len(data["readings"]["canonical"]["lever"]) != 13:
        raise PortError("G-gap_01 export must hold 24 monthly rows and 13 group levers")
    out = {
        "note": f"{SYNTHETIC_FOOTER}. G-gap_01 group-resolved linearisation of H's liquidity block under s*(0.76) "
                "(pricing) and two reverse readings: monthly T4' headroom rows h = 1..24 (T + P + F, $bn) with "
                "finite-difference slopes per group lever and card, the t0 T2 row (IG + cash 8% target). Lever "
                "costs and caps are research design assumptions [I]. Units: USD bn.",
        "source": "research/" + f"{GROUPS_GAP01}/g01_core.py",
        **data,
    }
    return out, [f"{GROUPS_GAP01}/g01_core.py", f"{GROUPS_GAP01}/g01_results.json", f"{GAP02}/t1_engine.py",
                 f"{GAP02}/gap02_study.py"]


def _perf_cases() -> list[dict[str, Any]]:
    """The 17 golden cases of perf_module._tests(), transcribed as data (verified against the research code)."""
    fl = [["2015-01-01", -50.0], ["2016-01-01", -50.0], ["2020-01-01", 60.0]]
    flat = {"2015-01-01": 100.0, "2016-01-01": 100.0, "2020-01-01": 100.0, "2024-01-01": 100.0}
    tracker_index = {"2018-01-01": 100.0, "2023-01-01": 161.051}
    period = [{"avg_par": 100.0, "len": 1.0, "cash_interest": 8.0, "pik_interest": 2.0, "fees": 0.0,
               "charge_offs": 1.5, "recoveries": 0.5}]
    trades = [{"book": "tail", "mtm0": 0.0, "mtm1": 10.0, "cash": -4.0, "im_posted": 0.0, "len": 1.0},
              {"book": "opportunistic", "mtm0": 5.0, "mtm1": 3.0, "cash": 1.0, "im_posted": 20.0, "len": 1.0}]
    cases: list[dict[str, Any]] = [
        dict(name="xirr_2y_10pct", fn="xirr", inputs={"flows": [["2020-01-01", -100.0], ["2021-12-31", 121.0]]},
             expected=0.10, tol=1e-9),
        dict(name="xirr_no_root_is_None", fn="xirr", inputs={"flows": [["2020-01-01", 100.0], ["2021-01-01", 5.0]]},
             expected=None, tol=None),
        dict(name="tvpi", fn="multiples", output="tvpi", inputs={"flows": fl, "nav": 80.0}, expected=1.4, tol=1e-9),
        dict(name="dpi", fn="multiples", output="dpi", inputs={"flows": fl, "nav": 80.0}, expected=0.6, tol=1e-9),
        dict(name="kspme_flat_index_equals_tvpi", fn="ks_pme",
             inputs={"flows": fl, "nav": 80.0, "asof": "2024-01-01", "index": flat}, expected=1.4, tol=1e-9),
        dict(name="direct_alpha_flat_index", fn="direct_alpha",
             inputs={"flows": fl, "nav": 80.0, "asof": "2024-01-01", "index": flat}, expected="ln1p_xirr", tol=1e-9),
        dict(name="direct_alpha_index_tracker_zero", fn="direct_alpha",
             inputs={"flows": [["2018-01-01", -100.0]], "nav": 161.051, "asof": "2023-01-01", "index": tracker_index},
             expected=0.0, tol=1e-9),
        dict(name="kspme_index_tracker_one", fn="ks_pme",
             inputs={"flows": [["2018-01-01", -100.0]], "nav": 161.051, "asof": "2023-01-01", "index": tracker_index},
             expected=1.0, tol=1e-12),
        dict(name="twr_flow_on_valuation_date", fn="twr",
             inputs={"vals": [["2025-01-01", 100.0], ["2025-07-01", 160.0], ["2026-01-01", 176.0]],
                     "flows": [["2025-07-01", 50.0]]}, expected=1.10 * 1.10 - 1, tol=1e-12),
        dict(name="twr_large_flow_requires_revaluation", fn="twr",
             inputs={"vals": [["2025-01-01", 100.0], ["2025-12-31", 130.0]], "flows": [["2025-06-30", 20.0]]},
             expected="raises:ValueError", tol=None),
        dict(name="credit_cash_yield", fn="credit_realized", output="cash_yield", inputs={"periods": period},
             expected=0.08, tol=1e-9),
        dict(name="credit_pik_share", fn="credit_realized", output="pik_share", inputs={"periods": period},
             expected=0.2, tol=1e-9),
        dict(name="credit_loss_rate", fn="credit_realized", output="loss_rate", inputs={"periods": period},
             expected=0.01, tol=1e-9),
        dict(name="credit_loss_adj_cash_yield", fn="credit_realized", output="loss_adj_cash_yield",
             inputs={"periods": period}, expected=0.07, tol=1e-9),
        dict(name="overlay_tail_pnl", fn="overlay_pnl", output="tail", inputs={"trades": trades, "ftp_rate": 0.045},
             expected=6.0, tol=1e-9),
        dict(name="overlay_opp_pnl", fn="overlay_pnl", output="opportunistic",
             inputs={"trades": trades, "ftp_rate": 0.045}, expected=-1.9, tol=1e-9),
        dict(name="overlay_total_pnl", fn="overlay_pnl", output="total", inputs={"trades": trades, "ftp_rate": 0.045},
             expected=4.1, tol=1e-9),
    ]
    return cases


def export_perf_golden() -> tuple[dict[str, Any], list[str]]:
    """perf_module.py golden cases (17), each re-run through the research functions before export."""
    rel = "groups/addenda/gap_02_calcs/perf_module.py"
    cases = _perf_cases()
    proc = subprocess.run([sys.executable, "-I", "-B", "-c", _PERF_RUNNER, str(_source(rel).parent)],
                          input=json.dumps(cases), capture_output=True, text=True, check=False, timeout=120)
    if proc.returncode != 0:
        raise PortError(f"perf runner failed:\n{proc.stderr.strip()[-4000:]}")
    data = json.loads(proc.stdout)
    research = {r["name"]: r for r in data["research_tests"]}
    if len(research) != 17 or not all(r["passed"] for r in research.values()):
        raise PortError(f"perf_module._tests() is not 17/17: {research}")
    for case, got in zip(cases, data["got"], strict=True):
        if set(research) != {c["name"] for c in cases} or got["name"] != case["name"]:
            raise PortError(f"perf case names disagree with perf_module._tests(): {case['name']}")
        exp = case["expected"]
        if exp == "ln1p_xirr":                       # T5: the research test computes ln(1 + IRR) inline
            exp = research[case["name"]]["expected"]
            case["expected"] = exp
        if exp == "raises:ValueError":
            ok = got["raised"] == "ValueError"
        elif exp is None:
            ok = got["value"] is None and got["raised"] is None
        else:
            ok = got["value"] is not None and abs(got["value"] - exp) <= case["tol"]
        if not ok:
            raise PortError(f"perf case {case['name']}: research returned {got}, expected {exp}")
    out = {
        "note": f"{SYNTHETIC_FOOTER}. Golden cases of the deterministic performance module O3 ({data['version']}): "
                "beliefs.perf must pass 17/17 (§4.15). Dates ISO-8601 (ACT/365F); amounts in one currency; "
                "contributions negative. expected = null means 'returns None'; 'raises:ValueError' means the call "
                "must raise.",
        "source": "research/" + rel,
        "version": data["version"],
        "n_cases": len(cases),
        "cases": cases,
    }
    return out, [rel]


@dataclass(frozen=True)
class Export:
    dest: str                                       # path under fixtures/
    build: Callable[[], tuple[dict[str, Any], list[str]]]


EXPORTS: tuple[Export, ...] = (
    Export("gap02/coefs.json", export_gap02_coefs),
    Export("gap02/gstar_grid.json", export_gstar_grid),
    Export("t1_engine/ladder_readings.json", export_ladder_readings),
    Export("groups_gap01/coefs.json", export_groups_gap01_coefs),
    Export("perf/golden_cases.json", export_perf_golden),
)


# ------------------------------------------------------------------------------------------------ port / check
def _entry_for_copy(c: Copy) -> dict[str, Any]:
    src = _source(c.source)
    dst = FIXTURES / c.dest / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    _make_writable(dst)
    shutil.copyfile(src, dst)
    _make_read_only(dst)
    src_hash, dst_hash = file_hash(src), file_hash(dst)
    if src_hash != dst_hash:
        raise PortError(f"copy of {c.source} does not hash equal to its source")
    if src.name == "sealed_pe_history_v1_1.csv" and dst_hash != SEALED_PE_HISTORY_SHA256:
        raise PortError(f"sealed PE history hash {dst_hash} != BUILD_SPEC §6.3 {SEALED_PE_HISTORY_SHA256}")
    return {"fixture": f"{c.dest}/{src.name}", "kind": "copy", "sources": {"research/" + c.source: src_hash},
            "sha256": dst_hash, "bytes": dst.stat().st_size}


def _entry_for_export(e: Export) -> dict[str, Any]:
    obj, sources = e.build()
    dst = FIXTURES / e.dest
    _write_json(dst, obj)
    return {"fixture": e.dest, "kind": "export", "exporter": e.build.__name__,
            "sources": {"research/" + s: file_hash(_source(s)) for s in sources},
            "sha256": file_hash(dst), "bytes": dst.stat().st_size}


def port() -> dict[str, Any]:
    """Copy and export every fixture, then write ``port_manifest.json`` (read-only)."""
    FIXTURES.mkdir(parents=True, exist_ok=True)
    entries = [_entry_for_copy(c) for c in COPIES] + [_entry_for_export(e) for e in EXPORTS]
    entries.sort(key=lambda d: d["fixture"])
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "note": f"{SYNTHETIC_FOOTER}. Read-only research ports (BUILD_SPEC §10.4): copies are byte-identical to "
                "their research sources; exports are regenerated or extracted by tools/port_research.py and "
                "cross-checked against the research's stored results. Updating a fixture needs a re-port and a "
                "contract-change note (§10.4).",
        "generated_by": "tools/port_research.py",
        "hash_rule": "sha256 of the file bytes, CRLF normalized to LF for text suffixes (contracts.hashing.file_hash; "
                     "S-ADR-42)",
        "data_class": "SYNTHETIC",
        "entries": entries,
    }
    _write_json(MANIFEST, manifest)
    return manifest


def check() -> list[str]:
    """Problems found when re-hashing every manifest entry's sources and fixture (empty list: all good)."""
    if not MANIFEST.is_file():
        return [f"{_rel(MANIFEST)} is missing; run tools/port_research.py"]
    with open(MANIFEST, encoding="utf-8") as fh:
        manifest = json.load(fh)
    problems: list[str] = []
    if manifest.get("schema") != MANIFEST_SCHEMA:
        problems.append(f"unknown manifest schema {manifest.get('schema')!r}")
    listed = set()
    for entry in manifest.get("entries", ()):
        fixture = FIXTURES / entry["fixture"]
        listed.add(fixture.resolve())
        if not fixture.is_file():
            problems.append(f"missing fixture {entry['fixture']}")
        elif file_hash(fixture) != entry["sha256"]:
            problems.append(f"fixture {entry['fixture']} was edited (hash differs from the manifest)")
        for src_rel, src_hash in entry["sources"].items():
            src = REPO_ROOT / src_rel
            if not src.is_file():
                problems.append(f"research source {src_rel} is missing")
            elif file_hash(src) != src_hash:
                problems.append(f"research source {src_rel} changed since the port (re-port and review)")
    expected = {(FIXTURES / c.dest / Path(c.source).name).resolve() for c in COPIES}
    expected |= {(FIXTURES / e.dest).resolve() for e in EXPORTS}
    for path in sorted(expected - listed):
        problems.append(f"{_rel(path)} is declared by the port but not listed in the manifest")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Port research fixtures (read-only copies + SHA-256 manifest).")
    parser.add_argument("--check", action="store_true", help="verify sources and fixtures against the manifest")
    args = parser.parse_args(argv)
    if args.check:
        problems = check()
        for p in problems:
            print(f"FAIL {p}")
        print("ok" if not problems else f"{len(problems)} problem(s)")
        return 0 if not problems else 1
    manifest = port()
    print(f"ported {len(manifest['entries'])} fixtures into {_rel(FIXTURES)}; manifest {_rel(MANIFEST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
