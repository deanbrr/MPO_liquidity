"""Fixture H: the gap_02 coefficient export as ``LPModel``, ``HSolution``, ``DualSet`` and ``Tree`` (BUILD_SPEC
v1.1 §4.5, §5.8–§5.10, §5.13; BUILD-21; owner WP-03).

SYNTHETIC – NOT ADIC DATA (allocation v1, census v1.0, research conventions; lever costs and capacities [I]).

The LP is gap_02's linearised t0 liquidity block (``tests/regression/fixtures/gap02/coefs.json``, exported by
``tools/port_research.py`` from ``phase1_demo_results.json``): one T4′ row (the minimum 24-month TPF headroom, key
``T4P:h=min``) and one T2 row (IG + cash 8% target, ``T2_IG_TARGET``), both PRICING rows; five reversible levers
(revolver, reserve top-up, amber sale, pacing cut, owner band) and three SELL columns on test PE funds. It is
written in W₀ units (``scale_bn`` = 177: $bn amounts ÷ W₀; the band is a share), MAXIMIZE, so its duals equal the
research's $bn duals and its objective × W₀ equals the research objective. Every row and column sits at the root of
``fixture_tree()``.

Phase I is gap_02's lexicographic minimum violation (T4′ at tier 1, T2 at tier 2) with every SELL fixed at 0
(no fire sales in Phase I), per consent scenario: R0x (amber sale, pacing cut), R0 (+ reserve top-up), R1 (+ the
signed revolver; gap_02 Mode B) and R2 (+ the owner band; Mode H). The mode follows §5.9: u* > 0 under the pricing
scenario → STRUCTURAL_RECOVERY; else d₀ > 0 → EXECUTION_RECOVERY; else NORMAL. Phase II solves the restored
problem the research solves (T4′ RHS relaxed by u* + 1e-6 when u* > 0): the t0 block has no later quarters on which
the glide path g_t could bind, so the glide path is reported, not imposed (WP-18 imposes it on the full H). When the
mode is not NORMAL the solution is ``RESTORED`` with ``recovery_hash`` = content hash of the ``GlidePath`` (§5.10).

DualSet (§5.8): ``pi_row`` = −HiGHS row dual (≥ 0 on binding ≥ rows of a MAXIMIZE problem); at the root exogenous
cash enters both PRICING rows with coefficient 1, so M₀ = π_T4 + π_T2; the objective values wealth at par (ū′ = 1),
so μ₀ = 1 + M₀ and ℓ₀ = M₀/(μ₀ − M₀) = M₀ (the gap_02 card's y_cash); other nodes carry no rows (μ_n = p_n,
M_n = 0, ℓ_n = 0). Dual quality: one-sided derivatives by warm finite differences (δ = 1e-4 W₀), the kink rule
|V′₊ − V′₋| > 1e-6 + 1e-3|V′| and the validity interval from ``Highs.getRanging``.
"""

from __future__ import annotations

import time
from collections.abc import Mapping
from typing import Any, Final, Literal

import numpy as np

from adic_tpa.contracts.enums import ConsentScenario, ContractMode, PricedOn, RowFamily, RowRole
from adic_tpa.contracts.errors import SchemaError, SolverError
from adic_tpa.contracts.evidence import SolverRecord
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import UnitId
from adic_tpa.contracts.optimizer import (
    ColKey, DualQuality, DualSet, GlidePath, HSolution, LPMeta, LPModel, Phase1Result, RowKey, TierResult,
)
from adic_tpa.contracts.world import Tree
from adic_tpa.testing.golden import golden
from adic_tpa.testing.trees import fixture_tree

__all__ = [
    "Reading", "READINGS", "LEVERS", "TEST_FUND_UNITS", "T4_ROW", "IG_ROW", "SCENARIO_LEVERS", "gap02_coefs",
    "build_fixture_lp", "fixture_phase1", "solve_fixture_lp", "fixture_h",
]

Reading = Literal["canonical", "as_written", "critic"]
READINGS: Final[tuple[Reading, ...]] = ("canonical", "as_written", "critic")
LEVERS: Final[tuple[str, ...]] = ("rcf", "reserve", "amber", "pace", "band")
TEST_FUND_UNITS: Final[tuple[UnitId, ...]] = (UnitId("SYN-PE-0901"), UnitId("SYN-PE-0902"), UnitId("SYN-PE-0903"))
T4_ROW: Final = RowKey(family=RowFamily.T4P, idx=(("h", "min"),))
IG_ROW: Final = RowKey(family=RowFamily.T2_IG_TARGET)
# Levers available per consent scenario (nested; gap_02 Mode B = R1, Mode H = R2; G-gap_01 STATES; §5.9).
SCENARIO_LEVERS: Final[Mapping[ConsentScenario, frozenset[str]]] = {
    ConsentScenario.R0X: frozenset({"amber", "pace"}),
    ConsentScenario.R0: frozenset({"amber", "pace", "reserve"}),
    ConsentScenario.R1: frozenset({"amber", "pace", "reserve", "rcf"}),
    ConsentScenario.R2: frozenset({"amber", "pace", "reserve", "rcf", "band"}),
}
_RELAX_PAD_BN: Final = 1e-6      # gap_02: the restored RHS is u* + 1e-6 when u* > 0
_FD_STEP: Final = 1e-4           # W₀ units (§5.8 dual quality)
_PHASE1_DELTA: Final = 1e-6      # W₀ units (§5.9 tier chaining)
_T_REC_Q: Final = 4
_OPTIONS: Final[Mapping[str, str | int | float | bool]] = {
    "threads": 1, "solver": "simplex", "simplex_strategy": 1, "random_seed": 0, "presolve": "on"}


def gap02_coefs() -> dict[str, Any]:
    """The ported gap_02 coefficient export (hash-checked against the port manifest)."""
    return golden("gap02/coefs")


def _scenario(mode_h: bool) -> ConsentScenario:
    return ConsentScenario.R2 if mode_h else ConsentScenario.R1


def build_fixture_lp(reading: Reading = "canonical", *, mode_h: bool = False, relax_bn: float = 0.0,
                     scenario: ConsentScenario | None = None, tree: Tree | None = None) -> LPModel:
    """The gap_02 block of ``reading`` as an ``LPModel`` in W₀ units (T4′ RHS relaxed by ``relax_bn``, USD bn)."""
    data = gap02_coefs()
    if reading not in data["readings"]:
        raise SchemaError(f"fixture_h: unknown reading {reading!r}; expected one of {READINGS}")
    r = data["readings"][reading]
    w0 = float(data["nav0_bn"])
    scen = scenario if scenario is not None else _scenario(mode_h)
    allowed = SCENARIO_LEVERS[scen]
    t = tree if tree is not None else fixture_tree()
    funds = data["test_funds"]
    n_lev, n = len(LEVERS), len(LEVERS) + len(funds)
    a = np.zeros((2, n))
    c = np.zeros(n)
    hi = np.zeros(n)
    for j, k in enumerate(LEVERS):
        scale = 1.0 if data["lever_units"][k] == "share" else w0     # x_bn = scale · x_lp
        slope = float(r["slope"][k])
        a[0, j] = slope * scale / w0
        a[1, j] = float(data["ig_coefficients"].get(k, 0.0)) * scale / w0
        unit_cost = float(data["costs"][k]) * (max(slope, 1e-9) if k == "band" else 1.0)   # band: per $ withheld
        c[j] = -unit_cost * scale / w0
        hi[j] = float(data["caps"][k]) / scale if k in allowed else 0.0
    for i, f in enumerate(funds):
        j = n_lev + i
        a[0, j] = a[1, j] = float(f["bid"])
        c[j] = float(f["bid"]) - float(f["hold"])
        hi[j] = float(f["nav"]) / w0
    from scipy import sparse  # lazy: keeps importing adic_tpa.testing light

    meta = LPMeta(tree_hash=t.tree_hash,
                  contract_hash=content_hash({"fixture": "gap02", "reading": reading, "scenario": scen.value}),
                  catalogue_hash=content_hash({"test_funds": funds, "units": TEST_FUND_UNITS}),
                  ledger_hash=content_hash({"h0": r["h0"], "slope": r["slope"],
                                            "ig_short_t0_bn": data["ig_short_t0_bn"]}),
                  builder_version="testing.fixture_h/1", consent_scenario=scen, pricing_level="tolerance",
                  replication=0)
    col_keys = tuple(ColKey(family="decision", name=k, node=0) for k in LEVERS) + tuple(
        ColKey(family="lens", name="sell", node=0, idx=(("unit", str(u)),)) for u in TEST_FUND_UNITS[:len(funds)])
    return LPModel(
        name=f"fixture_h_{reading}_{scen.value}", meta=meta, c=c, A=sparse.csc_array(a),
        row_lo=np.array([(-float(relax_bn) - float(r["h0"])) / w0, float(data["ig_short_t0_bn"]) / w0]),
        row_hi=np.full(2, np.inf), col_lo=np.zeros(n), col_hi=hi, integrality=None, row_keys=(T4_ROW, IG_ROW),
        col_keys=col_keys, row_role=np.full(2, RowRole.PRICING, dtype=np.int8), row_tier=np.array([1, 2], dtype=np.int8),
        node_of_row=np.zeros(2, dtype=np.int32), node_of_col=np.zeros(n, dtype=np.int32), scale_bn=w0)


# ------------------------------------------------------------------------------------------------ HiGHS wrapper
def _highs_solve(c: np.ndarray, a: Any, row_lo: np.ndarray, row_hi: np.ndarray, col_lo: np.ndarray,
                 col_hi: np.ndarray, *, maximize: bool, ranging: bool = False) -> dict[str, Any]:
    """Single-threaded HiGHS simplex (§1.13); ``SolverError`` unless optimal."""
    import highspy  # lazy: only fixture H solves

    h = highspy.Highs()
    h.silent()
    for key, value in _OPTIONS.items():
        h.setOptionValue(key, value)
    inf = highspy.kHighsInf
    csc = a.tocsc()
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = int(c.size), int(row_lo.size)
    lp.col_cost_ = np.asarray(c, dtype=np.float64)
    lp.col_lower_ = np.where(np.isinf(col_lo), -inf, col_lo)
    lp.col_upper_ = np.where(np.isinf(col_hi), inf, col_hi)
    lp.row_lower_ = np.where(np.isinf(row_lo), -inf, row_lo)
    lp.row_upper_ = np.where(np.isinf(row_hi), inf, row_hi)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = csc.indptr
    lp.a_matrix_.index_ = csc.indices
    lp.a_matrix_.value_ = csc.data
    lp.sense_ = highspy.ObjSense.kMaximize if maximize else highspy.ObjSense.kMinimize
    h.passModel(lp)
    started = time.perf_counter()
    h.run()
    elapsed = time.perf_counter() - started
    status = h.getModelStatus()
    if status != highspy.HighsModelStatus.kOptimal:
        raise SolverError(f"fixture_h: HiGHS status {h.modelStatusToString(status)}", {"status": str(status)})
    sol, info = h.getSolution(), h.getInfo()
    record = SolverRecord(
        solver="highs", version=f"{h.versionMajor()}.{h.versionMinor()}.{h.versionPatch()}", algorithm="simplex",
        options=dict(_OPTIONS), threads=1, status="optimal", iterations=int(info.simplex_iteration_count),
        time_s=float(elapsed), objective=float(info.objective_function_value),
        primal_infeas=float(max(info.max_primal_infeasibility, 0.0)),
        dual_infeas=float(max(info.max_dual_infeasibility, 0.0)), crossover=False)
    out: dict[str, Any] = {"x": np.array(sol.col_value, dtype=np.float64),
                           "row_dual": np.array(sol.row_dual, dtype=np.float64),
                           "objective": float(info.objective_function_value), "record": record}
    if ranging:
        st, rg = h.getRanging()
        if st == highspy.HighsStatus.kOk:
            out["row_range"] = (np.array(rg.row_bound_dn.value_, dtype=np.float64),
                                np.array(rg.row_bound_up.value_, dtype=np.float64))
    return out


# --------------------------------------------------------------------------------------------------- Phase I
def _phase1_tiers(lp: LPModel) -> tuple[float, float, tuple[str, ...], SolverRecord]:
    """Lexicographic minimum violation (§5.9) on ``lp`` with every SELL fixed at 0. Returns u*_T4 and u*_T2 (W₀
    units), the levers at cap with T4′ relief, and the last solver record."""
    from scipy import sparse

    n, m = lp.c.size, lp.row_lo.size
    sells = np.array([k.family == "lens" for k in lp.col_keys])
    hi = np.where(sells, 0.0, lp.col_hi)
    aug = sparse.hstack([lp.A, sparse.identity(m, format="csc")], format="csc")      # elastic u_r on each tiered row
    lo2, hi2 = np.concatenate([lp.col_lo, np.zeros(m)]), np.concatenate([hi, np.full(m, np.inf)])
    cost = np.zeros(n + m)
    cost[n] = 1.0
    first = _highs_solve(cost, aug, lp.row_lo, lp.row_hi, lo2, hi2, maximize=False)
    u_t4 = max(0.0, float(first["x"][n]))
    hi2[n] = u_t4 + _PHASE1_DELTA
    cost = np.zeros(n + m)
    cost[n + 1] = 1.0
    second = _highs_solve(cost, aug, lp.row_lo, lp.row_hi, lo2, hi2, maximize=False)
    u_t2 = max(0.0, float(second["x"][n + 1]))
    x = first["x"][:n]
    slopes = lp.A.toarray()[0]
    at_cap = tuple(lp.col_keys[j].name for j in range(n)
                   if not sells[j] and hi[j] > 0 and slopes[j] > 0 and abs(x[j] - hi[j]) <= 1e-9)
    return u_t4, u_t2, at_cap, second["record"]


def fixture_phase1(reading: Reading = "canonical", *, mode_h: bool = False) -> tuple[Phase1Result, GlidePath]:
    """Phase I of the fixture per consent scenario (R0x, R0, R1, R2), the contract mode it implies (computed, never
    asserted; §5.9) and the glide path (g_t = d₀(1 − t/4)⁺, or u*(1 − t/4)⁺ in structural recovery)."""
    data = gap02_coefs()
    w0 = float(data["nav0_bn"])
    d0 = max(0.0, -float(data["readings"][reading]["h0"]))
    by_scenario: dict[ConsentScenario, tuple[TierResult, ...]] = {}
    u_star: dict[ConsentScenario, float] = {}
    for scen in ConsentScenario:
        lp = build_fixture_lp(reading, scenario=scen)
        u_t4, u_t2, at_cap, record = _phase1_tiers(lp)
        u_star[scen] = u_t4 * w0
        by_scenario[scen] = (
            TierResult(tier=1, u_star_bn=u_t4 * w0, violations_bn={str(T4_ROW): u_t4 * w0},
                       iis=((str(T4_ROW),) + tuple(f"cap:{k}" for k in at_cap)) if u_t4 > 1e-12 else (),
                       farkas_ray_ref=None, levers_at_cap=at_cap, solver=record),
            TierResult(tier=2, u_star_bn=u_t2 * w0, violations_bn={str(IG_ROW): u_t2 * w0},
                       iis=(str(IG_ROW),) if u_t2 > 1e-12 else (), farkas_ray_ref=None, levers_at_cap=(),
                       solver=record))
    scen = _scenario(mode_h)
    u = u_star[scen]
    if u > 1e-9:
        mode, kind, target = ContractMode.STRUCTURAL_RECOVERY, "structural", u
    elif d0 > 1e-12:
        mode, kind, target = ContractMode.EXECUTION_RECOVERY, "execution", d0
    else:
        mode, kind, target = ContractMode.NORMAL, "none", 0.0
    body = dict(kind=kind, t_rec_q=_T_REC_Q, d0_bn=d0, u_star_by_row={str(T4_ROW): u},
                g_bn=tuple(target * max(0.0, 1.0 - t / _T_REC_Q) for t in range(_T_REC_Q + 1)))
    # §5.10 recovery_hash = content_hash(GlidePath): every field of the glide path but the hash itself
    draft = GlidePath(**body, recovery_hash="")                                      # type: ignore[arg-type]
    glide_hash = content_hash(draft.model_dump(exclude={"recovery_hash"}))
    glide = GlidePath(**body, recovery_hash=glide_hash)                              # type: ignore[arg-type]
    recovery_hash = None if mode is ContractMode.NORMAL else glide_hash
    p1 = Phase1Result(by_scenario=by_scenario, d0_bn=d0, mode=mode, pricing_scenario=scen, infeasibility_prices={},
                      recovery_hash=recovery_hash)
    return p1, glide


# -------------------------------------------------------------------------------------------------- Phase II
def solve_fixture_lp(lp: LPModel, tree: Tree, *, priced_on: PricedOn = PricedOn.FEASIBLE,
                     recovery_hash: str | None = None) -> HSolution:
    """Solve ``lp`` (MAXIMIZE) with HiGHS and assemble the ``HSolution`` and ``DualSet`` of the module docstring."""
    res = _highs_solve(lp.c, lp.A, lp.row_lo, lp.row_hi, lp.col_lo, lp.col_hi, maximize=True, ranging=True)
    pi = -res["row_dual"]
    pi = np.where(np.abs(pi) <= 1e-15, 0.0, pi)
    dn, up = res.get("row_range", (lp.row_lo, lp.row_lo))
    quality: dict[str, DualQuality] = {}
    for i, key in enumerate(lp.row_keys):
        if lp.row_role[i] != RowRole.PRICING:
            continue
        side = []
        for step in (-_FD_STEP, _FD_STEP):
            lo = lp.row_lo.copy()
            lo[i] += step
            side.append(_highs_solve(lp.c, lp.A, lo, lp.row_hi, lp.col_lo, lp.col_hi, maximize=True)["objective"])
        loosen = (side[0] - res["objective"]) / _FD_STEP          # V′ from relaxing the ≥ row
        tighten = (res["objective"] - side[1]) / _FD_STEP         # V′ from tightening it
        quality[str(key)] = DualQuality(
            one_sided=(loosen, tighten), at_kink=bool(abs(tighten - loosen) > 1e-6 + 1e-3 * abs(float(pi[i]))),
            ranging=(float(dn[i]), float(up[i])), band=(float(pi[i]),) * 3, sign_flip=False, pinned=False,
            method="ranging")
    mu = tree.p.astype(np.float64).copy()
    big_m = np.zeros(mu.size)
    big_m[0] = float(pi[lp.node_of_row == 0].sum())               # cash enters each root row with coefficient 1
    mu[0] = 1.0 + big_m[0]
    ell = np.where(mu - big_m > 0, big_m / np.maximum(mu - big_m, 1e-300), 0.0)
    x = res["x"]
    return HSolution(
        meta=lp.meta, status="optimal", objective=res["objective"], x=x,
        duals=DualSet(pi_row=pi, mu_cash=mu, M_cash=big_m, ell=ell, quality=quality),
        root_values={str(k): float(x[j]) for j, k in enumerate(lp.col_keys) if lp.node_of_col[j] == 0},
        marginal_utility_wealth=1.0, priced_on=priced_on, consent_scenario=lp.meta.consent_scenario,
        pricing_level=lp.meta.pricing_level, recovery_hash=recovery_hash, replication=lp.meta.replication,
        solver=res["record"], resolve_counts={"finite_difference": 2 * len(quality)},
        exact_objective=res["objective"])


def fixture_h(reading: Reading = "canonical", *, mode_h: bool = False) -> tuple[LPModel, HSolution, DualSet, Tree]:
    """Fixture H (§4.5): the restored Phase-II problem of the gap_02 block for ``reading`` (Mode B: R1 with the
    signed revolver; ``mode_h``: R2 with the owner band), its solution and duals, and ``fixture_tree()``."""
    tree = fixture_tree()
    p1, _glide = fixture_phase1(reading, mode_h=mode_h)
    u = p1.by_scenario[p1.pricing_scenario][0].u_star_bn
    lp = build_fixture_lp(reading, mode_h=mode_h, relax_bn=u + _RELAX_PAD_BN if u > 0 else 0.0, tree=tree)
    restored = p1.mode is not ContractMode.NORMAL
    sol = solve_fixture_lp(lp, tree, priced_on=PricedOn.RESTORED if restored else PricedOn.FEASIBLE,
                           recovery_hash=p1.recovery_hash)
    return lp, sol, sol.duals, tree
