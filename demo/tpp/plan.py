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
The status quo is today's book, status-quo pacing from the 2023-25 vintages, no new debt and, if enabled, the PE
program as decided: $20bn of exposure over three years, underperformers first.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .buckets import BY_ID, LIQUID_RISK, PRIVATE


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

    def to_dict(self) -> dict:
        return asdict(self)

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
