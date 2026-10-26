"""A plan: every non-anticipative decision, dated (the change list today plus the multi-year schedule).

  sell[unit]       fractions of each private unit (tail / core per ER bucket) sold at the start of years 1-3
                   (tau = 0, 1, 2), at that year's realized secondary bid; the buyer takes the unfunded
  liquid[bucket]   $bn in each liquid-risk bucket after today's trades (Global Agg, Global Equities, HF, MAO)
  cash, treasury   the liquidity reserve after today's trades
  commit[bucket]   $bn of new commitments (fund buckets, called over time) or deployments (co-invest buckets,
                   paid at once) in each of years 1-5 (tau = 0..4)
  term_sched       new term debt drawn at the start of years 1-3 (term_bn is the total)
  navf_bn          NAV-facility draw today (REFINANCE raises cash against holdings; LEVER when the cash buys
                   exposure: R1 labels them from the balance-sheet change)
  rev_upsize_bn    extra committed revolver capacity
  beta_bn          synthetic equity beta notional (LEVER)
  contingent       optional: the later decisions by the market state observed when they are taken (benign / exit
                   drought / stress, the engine's year-end classes): commitments in years 2-5 by the state at that
                   year end; sales and term debt at the start of year 2 by the year-1 state and at the start of year 3
                   by the year-1 and year-2 states together (9 histories, year-1 state major); sell, commit and
                   term_sched then hold today's decisions and the probability-weighted average of the later ones;
                   beta: the synthetic beta for years 2-5 by the market class at the start of the year (beta_bn
                   is year 1's)
The status quo is today's book, status-quo pacing from the 2023-25 vintages, no new debt and, if enabled, the PE
program as decided: $20bn of exposure over three years, underperformers first.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np

from .buckets import BY_ID, LIQUID_RISK, PRIVATE

STATES = ["benign", "exit drought", "stress"]


@dataclass
class Plan:
    name: str
    sell: dict = field(default_factory=dict)
    liquid: dict = field(default_factory=dict)
    cash: float = 0.0
    treasury: float = 0.0
    commit: dict = field(default_factory=dict)
    term_bn: float = 0.0
    term_sched: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    navf_bn: float = 0.0
    rev_upsize_bn: float = 0.0
    beta_bn: float = 0.0
    meta: dict = field(default_factory=dict)
    contingent: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    def restrict_units(self, ids: set) -> "Plan":
        """Keep only sales of units in ids (a plan read on another view's book)."""
        self.sell = {k: v for k, v in self.sell.items() if k in ids}
        if self.contingent and self.contingent.get("sell"):
            self.contingent["sell"] = {k: v for k, v in self.contingent["sell"].items() if k in ids}
        return self

    @staticmethod
    def from_dict(d: dict) -> "Plan":
        return Plan(**{k: d[k] for k in Plan.__dataclass_fields__ if k in d})


def program_fractions(book, P, settings: dict | None = None) -> dict:
    """The PE program as decided: per unit, fractions of the original unit sold at tau = 0..years-1.
    Underperformers first: the PE tail units (the department-wide candidate pool) pro rata; if the pool is smaller
    than the program, the remainder comes from the PE core units pro rata."""
    st = settings or {}
    if not st.get("pe_program_enabled", P.get("pe_program.enabled")):
        return {}
    total = float(st.get("pe_program_total_bn", P.get("pe_program.total_bn")))
    years = int(min(st.get("pe_program_years", P.get("pe_program.years")), 3))
    basis = st.get("pe_program_basis", P.get("pe_program.basis"))
    selection = st.get("pe_program_selection", P.get("pe_program.selection"))
    size = (lambda u: u.exposure0) if basis == "exposure" else (lambda u: u.nav0)
    pe = [u for u in book.units if u.pe_program]
    if selection == "underperformers":
        tiers = [[u for u in pe if u.part == "tail"], [u for u in pe if u.part == "core"]]
    else:
        tiers = [pe]
    out, left = {}, total
    for tier in tiers:
        cap = sum(size(u) for u in tier)
        if cap <= 1e-12 or left <= 1e-12:
            continue
        take = min(left, cap)
        for u in tier:
            share = take * size(u) / cap / max(size(u), 1e-12)          # fraction of the original unit
            out[u.id] = [share / years if k < years else 0.0 for k in range(3)]
        left -= take
    return out


def status_quo(book, P, settings: dict | None = None, program: bool = True) -> Plan:
    st = settings or {}
    sell = program_fractions(book, P, st) if program else {}
    liquid = {b: float(book.liquid.get(b, 0.0)) for b in LIQUID_RISK}
    beta0 = float(st.get("beta0_bn", P.get("overlay.beta0_bn")))
    pace = {b: [float(book.pacing_sq.get(b, 0.0))] * 5 for b in PRIVATE}
    return Plan(name="Status quo" + (" + PE program" if sell else ""), sell=sell, liquid=liquid,
                cash=float(book.liquid.get("CASH", 0.0)), treasury=float(book.liquid.get("TREASURY", 0.0)),
                commit=pace, term_bn=0.0, term_sched=[0.0, 0.0, 0.0], navf_bn=0.0, rev_upsize_bn=0.0, beta_bn=beta0,
                meta={"kind": "status_quo", "program": bool(sell)})


# operating rules for doing nothing: no annual rebalancing and no reserve top-ups (obligations are still paid,
# from cash first and then the liquid sleeves in the waterfall's order)
DO_NOTHING_SIM = {"rebalance": False, "maintain_target": False}


def do_nothing(book, P, settings: dict | None = None) -> Plan:
    """No decisions at all: no sales (the PE program is not executed), no new commitments, no trades, no new debt.
    Distributions accumulate as cash; the owner's distribution and existing commitments' calls are paid."""
    st = settings or {}
    return Plan(name="Do nothing", sell={}, liquid={b: float(book.liquid.get(b, 0.0)) for b in LIQUID_RISK},
                cash=float(book.liquid.get("CASH", 0.0)), treasury=float(book.liquid.get("TREASURY", 0.0)),
                commit={b: [0.0] * 5 for b in PRIVATE}, term_bn=0.0, term_sched=[0.0, 0.0, 0.0], navf_bn=0.0,
                rev_upsize_bn=0.0, beta_bn=float(st.get("beta0_bn", P.get("overlay.beta0_bn"))),
                meta={"kind": "do_nothing", "program": False})


def schedule_paths(plan: Plan, unit_ids: list, tpl_buckets: list, cls_y) -> tuple:
    """Per-path schedules for the simulator: sales (3, m, K), commitments (5, m, T), term draws (3, m). A decision
    taken at the start of a later year tau follows the state observed then, cls_y[:, tau], when the plan is
    state-contingent; otherwise every path gets the same schedule."""
    cls_y = np.asarray(cls_y, int)
    m = cls_y.shape[0]
    sell = np.zeros((3, m, len(unit_ids)))
    amt = np.zeros((5, m, len(tpl_buckets)))
    c = plan.contingent or {}
    for k, u in enumerate(unit_ids):
        if u in plan.sell:
            sell[:, :, k] = np.asarray(plan.sell[u], float)[:3, None]
        cs = (c.get("sell") or {}).get(u)
        if cs is not None:
            for tau in (1, 2):
                sell[tau, :, k] = np.asarray(cs[tau - 1], float)[_ctx(cs[tau - 1], tau, cls_y)]
    for j, b in enumerate(tpl_buckets):
        if b in plan.commit:
            amt[:, :, j] = np.asarray(plan.commit[b], float)[:5, None]
        cc = (c.get("commit") or {}).get(b)
        if cc is not None:
            for tau in range(1, 5):
                amt[tau, :, j] = np.asarray(cc[tau - 1], float)[cls_y[:, tau]]
    ts = list(plan.term_sched or [plan.term_bn, 0.0, 0.0])
    sched = np.repeat(np.asarray(ts, float)[:3, None], m, 1)
    if c.get("term"):
        for tau in (1, 2):
            sched[tau] = np.asarray(c["term"][tau - 1], float)[_ctx(c["term"][tau - 1], tau, cls_y)]
    return sell, amt, sched


def beta_paths(plan: Plan, cls_y) -> np.ndarray:
    """(5, m) synthetic beta per year: year 1 today's; years 2-5 by the path's market class at the start of the year."""
    cls_y = np.asarray(cls_y, int)
    b = np.full((5, cls_y.shape[0]), float(plan.beta_bn))
    cb = (plan.contingent or {}).get("beta")
    if cb:
        for t in range(1, 5):
            b[t] = np.asarray(cb[t - 1], float)[cls_y[:, t]]
    return b


def _ctx(values, tau: int, cls_y):
    """The context a later sale or debt draw follows: the year-2 one the year-1 state; the year-3 one the year-1 and
    year-2 states together (9 histories), or the year-2 state alone for a plan stored by state (3 values)."""
    if tau == 2 and len(values) == len(STATES) ** 2:
        return cls_y[:, 1] * len(STATES) + cls_y[:, 2]
    return cls_y[:, tau]


def program_summary(book, plan: Plan) -> dict:
    """Exposure, NAV and unfunded sold by the plan per tranche, PE vs other departments."""
    rows = []
    units = {u.id: u for u in book.units}
    for uid, fr in plan.sell.items():
        u = units[uid]
        for tau, f in enumerate(fr):
            if f > 1e-9:
                rows.append({"unit": uid, "bucket": u.bucket, "department": BY_ID[u.bucket].department,
                             "tau": tau, "nav_bn": f * u.nav0, "unfunded_bn": f * u.unf0,
                             "exposure_bn": f * u.exposure0, "pe": u.pe_program})
    pe_expo = sum(r["exposure_bn"] for r in rows if r["pe"])
    return {"rows": rows, "pe_exposure_bn": pe_expo,
            "pe_nav_bn": sum(r["nav_bn"] for r in rows if r["pe"]),
            "other_exposure_bn": sum(r["exposure_bn"] for r in rows if not r["pe"]),
            "by_tranche_bn": [sum(r["exposure_bn"] for r in rows if r["tau"] == k) for k in range(3)]}
