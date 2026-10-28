"""Component 1a: the book (DATA + ASSUMPTION), at the grain the engine and the optimizer use.

Private holdings are grouped into units: per ER bucket, a TAIL of credible underperformers and a CORE.
  perf_i  = c_i (A_i - peer_i)          credibility-weighted actual IRR excess over same-bucket, same-vintage-band peers
  tail    = holdings with perf_i < -1pp, worst first, up to 60% of the bucket's exposure (NAV + unfunded)
So "sell underperformers" (the PE program, user 2026-10-25) is a linear decision on the tail units, and every unit
keeps the holding-level evidence: NAV-weighted forward returns per ER world (tpp.returns), age cohorts for the
cash-flow engine, unfunded commitments, and a secondary-bid factor
  bid_i(state, tau) = rho[bid key][state] x agemult(age_i + tau) x exp(q x clip(perf_i, -15%, 15%) x min(D_i, 4))
(underperformers trade at deeper discounts: buyers price q = 50% of their relative underperformance to persist).

The fund file does not hold every private asset: private NAV is fund.private_share of the whole fund (DATA, the user).
The difference is derived from the current private strategies (fund.private_outside_file = replicate): one OUTSIDE unit
per ER bucket that scales the bucket's book up (same age profile, same unfunded per $ of NAV), earns the ER strategy
returns and is never sold by a plan; status-quo pacing scales in proportion.
Liquid and reserve buckets hold the fund-file managers (hedge funds, long-only mandates) plus the internally managed
sleeves that the fund file does not contain, sized so the whole fund equals fund.total_nav_bn (ASSUMPTION; the Balance
Sheet group edits the split), with the reserve (cash + Treasury) at least at its target today
(internal_sleeves.reserve_at_target). Status-quo pacing per private bucket is the average original commitment of the
pacing.basis_vintages (DATA-derived).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .buckets import BY_ID, CATALOG, PRIVATE, SLEEVES
from .legacy import mpo_params, segment
from .returns import WORLDS

AGE_EDGES = [3.0, 6.0, 9.0]


@dataclass
class Unit:
    id: str
    bucket: str
    part: str                      # "tail" | "core" | "swap" (holdings singled out for a substitution test) | "ext"
                                   # (private NAV outside the fund file, derived from the current strategies)
    nav0: float
    unf0: float
    n: int
    codes: list
    cohorts: list                  # [{"nav", "unf", "age"}]
    r_world: list                  # forward return per ER world (Downside, Base, Upside)
    bidfac: list                   # bid factor (agemult x quality, NAV-weighted) at tau = 0, 1, 2
    perf: float                    # NAV-weighted perf score
    pe_program: bool

    @property
    def exposure0(self) -> float:
        return self.nav0 + self.unf0


@dataclass
class Book:
    units: list[Unit]
    liquid: dict                   # bucket -> $bn (liquid, semi and reserve buckets)
    liquid_src: dict               # bucket -> {"file": $bn, "sleeve": $bn}
    holdings: pd.DataFrame         # classified live holdings with returns, perf, bid, unit
    bucket_ret: pd.DataFrame       # tpp.returns bucket table (exist_* / new_*)
    er: pd.DataFrame
    pacing_sq: dict                # bucket -> $bn a year of new commitments (status quo)
    revolver_drawn0: float
    term0: float
    file_nav: float
    total_nav: float
    W0: float
    Wstar: float
    goal_rate: float
    years: int
    notes: list = field(default_factory=list)
    private_share: float = 0.0     # private NAV / whole-fund NAV asked for (fund.private_share)
    pace_scale: float = 1.0        # status-quo pacing multiplier (1 + outside NAV / fund-file private NAV)
    reserve_moved: float = 0.0     # $bn moved into the reserve today (internal_sleeves.reserve_at_target)

    @property
    def private_nav(self) -> float:
        return float(sum(u.nav0 for u in self.units))

    @property
    def unfunded(self) -> float:
        return float(sum(u.unf0 for u in self.units))

    @property
    def outside_nav(self) -> float:
        return float(sum(u.nav0 for u in self.units if u.part == "ext"))

    @property
    def outside_unfunded(self) -> float:
        return float(sum(u.unf0 for u in self.units if u.part == "ext"))

    def summary(self) -> dict:
        by_dept = {}
        for u in self.units:
            d = BY_ID[u.bucket].department
            by_dept[d] = by_dept.get(d, 0.0) + u.nav0
        for b, v in self.liquid.items():
            d = BY_ID[b].department
            by_dept[d] = by_dept.get(d, 0.0) + v
        reserve = float(self.liquid.get("CASH", 0.0) + self.liquid.get("TREASURY", 0.0))
        return {"total_nav_bn": self.total_nav, "file_nav_bn": self.file_nav, "private_nav_bn": self.private_nav,
                "file_private_nav_bn": self.private_nav - self.outside_nav, "outside_nav_bn": self.outside_nav,
                "outside_unfunded_bn": self.outside_unfunded, "private_share_target": self.private_share,
                "unfunded_bn": self.unfunded, "liquid_bn": float(sum(self.liquid.values())),
                "liquid_file_bn": float(sum(v["file"] for v in self.liquid_src.values())),
                "liquid_sleeves_bn": float(sum(v["sleeve"] for v in self.liquid_src.values())),
                "reserve_bn": reserve, "reserve_moved_bn": self.reserve_moved, "pace_scale": self.pace_scale,
                "pacing_sq_bn": float(sum(self.pacing_sq.values())),
                "overcommit0": (self.private_nav + self.unfunded) / max(self.W0, 1e-9),
                "W0_bn": self.W0, "Wstar_bn": self.Wstar, "by_department_bn": by_dept,
                "revolver_drawn0_bn": self.revolver_drawn0, "term0_bn": self.term0}


def _rho_table(MP, P) -> dict:
    rho = {k: list(v) for k, v in MP._leaf("bids.rho")["value"].items()}
    rho.update({k: list(v) for k, v in P.get("bids.rho_extra").items()})
    return rho


def _agemult(MP, age: np.ndarray, edges) -> np.ndarray:
    am = np.asarray(MP._leaf("bids.age_multiplier")["value"], float)
    b = (np.asarray(age, float)[:, None] >= np.asarray(edges, float)[None, :]).sum(1)
    return am[b]


def build_book(holdings: pd.DataFrame, bucket_ret: pd.DataFrame, er: pd.DataFrame, P, settings: dict | None = None
               ) -> Book:
    """holdings: classified live holdings with tpp.returns columns. settings: optional overrides (total NAV, sleeve
    split, liabilities) from the Balance Sheet group."""
    st = settings or {}
    MP = mpo_params()
    rho = _rho_table(MP, P)
    q = float(P.get("bids.quality_passthrough"))
    bclip = P.get("bids.clip")
    h = holdings.copy()
    h["perf"] = (h["act_excess"].fillna(0.0) * h["act_cred"].fillna(0.0)).clip(-0.5, 0.5)
    life = np.zeros(len(h))
    dur_share = np.zeros(len(h))
    edges = []
    for i, b in enumerate(h["bucket"]):
        bk = BY_ID[b]
        if bk.segment:
            sg = segment(MP, bk.segment)
            life[i], dur_share[i] = sg["life"], sg["duration_share"]
            edges.append(sg["edges"])
        else:
            life[i], dur_share[i] = 5.0, 1.0
            edges.append([3, 6, 9])
    rem = np.maximum(life - h["age"].to_numpy(), 1.5)
    h["duration"] = rem * dur_share
    qual = np.exp(q * np.clip(h["perf"].to_numpy(), -0.15, 0.15) * np.minimum(h["duration"].to_numpy(), 4.0))
    h["bid_quality"] = qual
    today = int(P.get("bids.today_state"))
    bid0 = []
    for i, r in enumerate(h.itertuples()):
        bk = BY_ID[r.bucket]
        if bk.private:
            am = _agemult(MP, np.array([r.age]), edges[i])[0]
            bid0.append(float(np.clip(rho[bk.bid_key][today] * am * qual[i], *bclip)))
        else:
            bid0.append(1.0)
    h["bid0"] = bid0
    # ---- tail / core split per private bucket. PE program buckets share one candidate pool ranked jointly across
    # the department (worst relative performance first), sized at 1.25x the program so the optimizer keeps a
    # choice; other buckets' tails are their credible underperformers (perf < -1pp).
    h["unit"] = ""
    h["expo"] = h["nav_bn"] + h["unfunded_bn"]
    # basis-independent ranking (the same units under every return view, so plans transfer exactly between views):
    # credible relative performance, then the shortfall against underwriting, then the code for determinism
    h["uw_short"] = (h["act_irr"] - h["uw_irr"]).fillna(0.0)
    pe_pool = set()
    prog_total = float(st.get("pe_program_total_bn", P.get("pe_program.total_bn")))
    pe_rows = h[h["bucket"].map(lambda x: BY_ID[x].pe_program)].sort_values(["perf", "uw_short", "FUND_CODE"])
    acc = 0.0
    for idx, r in pe_rows.iterrows():
        if acc >= 1.25 * prog_total:
            break
        pe_pool.add(idx)
        acc += r["expo"]
    units: list[Unit] = []
    swap_codes = set(st.get("swap_codes", []))
    for b in PRIVATE:
        g = h[h["bucket"] == b]
        if g.empty:
            continue
        swap_idx = [i for i in g.index if h.at[i, "FUND_CODE"] in swap_codes]
        g_rest = g.drop(index=swap_idx)
        if BY_ID[b].pe_program:
            tail_idx = [i for i in g_rest.index if i in pe_pool]
        else:
            cap = 0.60 * float(g_rest["expo"].sum())
            tail_idx, acc = [], 0.0
            for idx, r in g_rest.sort_values("perf").iterrows():
                if r["perf"] < -0.01 and acc + r["expo"] <= cap + 1e-12:
                    tail_idx.append(idx)
                    acc += r["expo"]
        parts = {"tail": g_rest.loc[tail_idx], "core": g_rest.drop(index=tail_idx), "swap": g.loc[swap_idx]}
        for part, gg in parts.items():
            if gg.empty or (gg["nav_bn"].sum() + gg["unfunded_bn"].sum()) < 1e-6:
                continue
            uid = f"{b}:{part}"
            h.loc[gg.index, "unit"] = uid
            nav, unf = float(gg["nav_bn"].sum()), float(gg["unfunded_bn"].sum())
            w = gg["nav_bn"].to_numpy()
            ex = gg["nav_bn"].to_numpy() + gg["unfunded_bn"].to_numpy()
            if w.sum() > 1e-9:
                r_w = (gg[["r_down", "r_base", "r_up"]].to_numpy().T @ w / w.sum()).tolist()
                perf = float(gg["perf"].to_numpy() @ w / w.sum())
            else:
                r_w = [bucket_ret.loc[b, f"new_{x}"] for x in WORLDS]
                perf = 0.0
            # cohorts by age band (exposure-weighted age)
            cohorts = []
            band = np.digitize(gg["age"].to_numpy(), AGE_EDGES)
            for k in range(len(AGE_EDGES) + 1):
                m = band == k
                if not m.any():
                    continue
                cn, cu = float(gg["nav_bn"].to_numpy()[m].sum()), float(gg["unfunded_bn"].to_numpy()[m].sum())
                if cn + cu < 1e-9:
                    continue
                age = float(np.average(gg["age"].to_numpy()[m], weights=np.maximum(ex[m], 1e-12)))
                cohorts.append({"nav": cn, "unf": cu, "age": age})
            bk = BY_ID[b]
            sg = segment(MP, bk.segment)
            bf = []
            for tau in range(3):
                am = _agemult(MP, gg["age"].to_numpy() + tau, sg["edges"])
                f = am * gg["bid_quality"].to_numpy()
                bf.append(float(f @ w / w.sum()) if w.sum() > 1e-9 else 1.0)
            units.append(Unit(uid, b, part, nav, unf, int(len(gg)), gg["FUND_CODE"].tolist(), cohorts, r_w, bf, perf,
                              bk.pe_program and part != "swap"))
    notes = []
    file_nav = float(h["nav_bn"].sum())
    total = float(st.get("total_nav_bn", P.get("fund.total_nav_bn")))
    # ---- private NAV outside the fund file (fund.private_share, DATA: the user): the current private strategies
    # scaled up to it, one unit per ER bucket with the bucket's age profile and unfunded per $ of NAV, earning the ER
    # strategy returns (no holding record: no tilt, no quality discount in the bid)
    file_priv = float(sum(u.nav0 for u in units))
    share = float(st.get("private_share", P.get("fund.private_share")) or 0.0)
    mode = st.get("private_outside_file", P.get("fund.private_outside_file"))
    outside = max(share * total - file_priv, 0.0) if (mode == "replicate" and file_priv > 1e-9) else 0.0
    k_out = outside / file_priv if file_priv > 1e-9 else 0.0
    if share * total < file_priv - 1e-6 and mode == "replicate":
        notes.append(f"The fund file's private NAV ({file_priv:.1f}) already exceeds {share:.0%} of the whole fund; "
                     f"no private assets are added outside the file.")
    if k_out > 1e-12:
        for b in PRIVATE:
            us = [u for u in units if u.bucket == b]
            if sum(u.nav0 for u in us) <= 1e-9:
                continue
            band = {}
            for u in us:
                for c in u.cohorts:
                    j = int(np.digitize(c["age"], AGE_EDGES))
                    a = band.setdefault(j, {"nav": 0.0, "unf": 0.0, "w": 0.0, "aw": 0.0})
                    a["nav"] += c["nav"]
                    a["unf"] += c["unf"]
                    a["w"] += c["nav"] + c["unf"]
                    a["aw"] += c["age"] * (c["nav"] + c["unf"])
            cohorts = [{"nav": k_out * a["nav"], "unf": k_out * a["unf"], "age": a["aw"] / max(a["w"], 1e-12)}
                       for j, a in sorted(band.items()) if a["w"] > 1e-12]
            nav = float(sum(c["nav"] for c in cohorts))
            unf = float(sum(c["unf"] for c in cohorts))
            sg = segment(MP, BY_ID[b].segment)
            ages = np.array([c["age"] for c in cohorts])
            wts = np.array([c["nav"] for c in cohorts])
            bf = [float(_agemult(MP, ages + tau, sg["edges"]) @ wts / max(wts.sum(), 1e-12)) for tau in range(3)]
            r_w = [float(bucket_ret.loc[b, f"new_{x}"]) for x in WORLDS]
            units.append(Unit(f"{b}:ext", b, "ext", nav, unf, 0, [], cohorts, r_w, bf, 0.0, False))
    # ---- liquid buckets: fund-file managers + internal sleeves filling the total NAV
    split = dict(P.get("internal_sleeves.gap_split"))
    split.update(st.get("sleeve_split", {}))
    ssum = sum(split.values())
    gap = max(total - file_nav - outside, 0.0)
    if total - file_nav - outside < 0:
        notes.append(f"Total NAV {total:.1f} is below the fund-file NAV plus the private assets outside it "
                     f"({file_nav + outside:.1f}); sleeves set to zero.")
    liquid, src = {}, {}
    for b in CATALOG:
        if b.private:
            continue
        f = float(h.loc[h["bucket"] == b.id, "nav_bn"].sum())
        s = gap * split.get(b.id, 0.0) / ssum if b.id in SLEEVES else 0.0
        liquid[b.id] = f + s
        src[b.id] = {"file": f, "sleeve": s}
    rev0 = float(st.get("revolver_drawn0_bn", P.get("corporate_finance.revolver_drawn0_bn")))
    term0 = float(st.get("term_debt0_bn", P.get("corporate_finance.term_debt0_bn")))
    assets = file_nav + outside + gap
    W0 = assets - rev0 - term0
    # the reserve (cash + Treasury) starts at least at its target: any shortfall moves in from the other internal
    # sleeves pro rata (ASSUMPTION internal_sleeves.reserve_at_target). Today's balances are a fact about the book, so
    # the assumption file's target sets them, not a variant's policy (a run without the Liquidity group's limits starts
    # from the same balance sheet)
    moved = 0.0
    if bool(P.get("internal_sleeves.reserve_at_target")):
        ft = float(P.get("liquidity.floor_target"))
        short = ft * W0 - (liquid.get("CASH", 0.0) + liquid.get("TREASURY", 0.0))
        donors = [b for b in SLEEVES if b not in ("CASH", "TREASURY") and src.get(b, {}).get("sleeve", 0.0) > 1e-12]
        pool = float(sum(src[b]["sleeve"] for b in donors))
        moved = float(min(max(short, 0.0), pool))
        if moved > 1e-9:
            for b in donors:
                take = moved * src[b]["sleeve"] / pool
                src[b]["sleeve"] -= take
                liquid[b] -= take
            rs = src["CASH"]["sleeve"] + src["TREASURY"]["sleeve"]
            for b in ("CASH", "TREASURY"):
                add = moved * (src[b]["sleeve"] / rs if rs > 1e-12 else 0.5)
                src[b]["sleeve"] += add
                liquid[b] += add
            notes.append(f"Today's reserve is held at its {ft:.0%} target: {moved:.1f} moved into cash and Treasury "
                         f"from the other internal sleeves (working split).")
    goal = float(st.get("goal_rate", P.get("goal.rate")))
    years = int(P.get("simulation.years"))
    # ---- status-quo pacing from recent vintages (DATA-derived), scaled with the private book outside the file
    vint = list(P.get("pacing.basis_vintages"))
    pacing = {}
    for b in PRIVATE:
        g = h[(h["bucket"] == b) & h["vintage"].isin(vint)]
        pacing[b] = float(g["commit_bn"].sum()) / len(vint) * (1.0 + k_out)
    return Book(units, liquid, src, h, bucket_ret, er, pacing, rev0, term0, file_nav, assets, W0,
                W0 * (1 + goal) ** years, goal, years, notes, private_share=share, pace_scale=1.0 + k_out,
                reserve_moved=moved)
