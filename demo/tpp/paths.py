"""Component 2: scenario paths (the prototype's generator and private-market engine, driven by ER worlds).

Factor and regime paths come from examples/mpo_v2 scenarios.Generator unchanged: quarterly macro regime (expansion,
late cycle, crisis, recovery), exit window (open, normal, drought, frozen), oil shock state, six factors with t5
shocks, and the oil-linked owner draw. Its own CMA worlds are neutralized; the ER file's three columns are the worlds
instead. Every factor path is evaluated in all three worlds (common random numbers), and a scenario's probability is
pi_w / n with pi set by the stakeholder's preference, so changing pi only reweights paths.

Each bucket's quarterly log return in world w:
    r = rf / 4 + f . B + alpha_w / 4 + idio,     alpha_w = ln(1 + R_w) - rf - B . E[f]
where R_w is the ER return (new money) or the unit's preference return (existing holdings), and E[f] is the base
case's mean annual factor return. So the base case reproduces R_w exactly in expectation, and a stress (crisis in
year 1, prolonged drought, oil crash) changes paths, flows and bids but keeps the alphas: stresses lower returns.

Private units run through scenarios.UnitEngine at their full original size (calls from unfunded by age and exit
window, distributions by age and exit window, crisis call stress), so a decision that keeps a fraction x of a unit
scales every flow by x exactly (the prototype's positive homogeneity). New commitments (fund buckets) and new
deployments (co-invest buckets) are per-$ templates started in each of years 0-4.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import numpy as np

from .buckets import BY_ID, CATALOG, PRIVATE
from .legacy import Generator, UnitEngine, mpo_params, node_class, segment
from .returns import WORLDS

NQ = 20
STRESSES = {
    "base": {"label": "Base case (exit drought today, DPI falling)", "desc": "Exit window starts in a drought; regimes then evolve as calibrated."},
    "prolonged_drought": {"label": "Prolonged DPI decline", "desc": "The exit drought persists (0.95 a quarter) and distributions stay near half of normal."},
    "crisis_y1": {"label": "Macro crisis in year 1", "desc": "Equities fall 30% and credit 5% over the next two quarters; the regime starts in crisis and exits are drought or frozen (calls up, distributions down, bids down)."},
    "oil_crash": {"label": "Oil crash, higher owner draw", "desc": "Brent falls from about $127 to $40 now (equities -10%); the oil-linked owner draw rises toward 10%."},
    "exit_window_opens": {"label": "Exit window reopens", "desc": "Exits start open or normal: distributions recover."},
    "rate_shock": {"label": "Rate shock +200bp", "desc": "Yields jump 200bp now: every rate-sensitive bucket marks down by its duration loading (Treasury about -7%, Global Agg -12%, real estate and infrastructure partly); SOFR, cash and all floating financing +200bp."},
    "stagflation": {"label": "2022-style stagflation", "desc": "The rate shock plus equities -20% over two quarters, a crisis regime, and stocks and bonds falling together (crisis correlation back to the prototype's -0.30)."},
    "hf_gates": {"label": "Hedge-fund gates", "desc": "Hedge funds redeem at most 10% / 5% / 0% a quarter by state."},
    "private_markdown": {"label": "Private markdown -20% today", "desc": "Every private holding marks down 20% at t0 (the goal stays on today's NAV)."},
    "calls_spike": {"label": "Capital-call spike", "desc": "Call intensities x1.5 on all unfunded commitments."},
    "draw_10": {"label": "Owner draw at 10%", "desc": "The owner takes 10% of opening NAV every year."},
}


def stress_overrides(stress: str, P) -> tuple[dict, dict]:
    """Generator overrides and deterministic shocks for a named stress (combinable with '+')."""
    start_drought = float(P.get("exits.start_in_drought"))
    gen = {"regimes.exit.start": [0.0, 1.0 - start_drought, start_drought, 0.0]}
    shock = {"rate_bp": 0.0, "private_markdown": 0.0, "hf_liq": None, "draw_fixed": None, "call_mult": 1.0,
             "fshock": np.zeros((NQ, 6))}
    fs = shock["fshock"]                     # additive factor shocks by quarter: [eq, cr, rt, oil, ex, vol]
    for s in [x for x in stress.split("+") if x and x != "base"]:
        if s == "prolonged_drought":
            p = float(P.get("exits.prolonged_drought_persistence"))
            gen["regimes.exit.P_q"] = [[0.85, 0.15, 0.0, 0.0], [0.06, 0.88, 0.06, 0.0], [0.0, 1.0 - p - 0.01, p, 0.01],
                                       [0.0, 0.1, 0.15, 0.75]]
            gen["regimes.exit.start"] = [0.0, 0.0, 1.0, 0.0]
        elif s == "crisis_y1":
            # the prototype centres regime shifts (regimes move risk, not means), so the crash itself is a shock
            gen["regimes.macro.start"] = [0.0, 0.0, 1.0, 0.0]
            gen["regimes.exit.start"] = [0.0, 0.0, 0.5, 0.5]
            fs[0:2, 0] += np.log(0.70) / 2
            fs[0:2, 1] += -0.05 / 2
            fs[0:2, 5] += 0.15 / 2
        elif s == "oil_crash":
            gen["regimes.oil.start"] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
            gen["factors.oil.spot"] = 40.0
            fs[0, 3] += np.log(40.0 / 126.55)
            fs[0, 0] += np.log(0.90)
        elif s == "exit_window_opens":
            gen["regimes.exit.start"] = [0.5, 0.5, 0.0, 0.0]
        elif s == "rate_shock":
            shock["rate_bp"] += 200.0
            fs[0, 2] += -6.0 * 0.02           # the rates factor is a 6-year-duration excess return
        elif s == "stagflation":
            shock["rate_bp"] += 200.0
            fs[0, 2] += -6.0 * 0.02
            fs[0:2, 0] += np.log(0.80) / 2
            fs[0:2, 1] += -0.03 / 2
            gen["regimes.macro.start"] = [0.0, 0.0, 1.0, 0.0]
            gen["_crisis_corr_sign"] = -1
        elif s == "hf_gates":
            shock["hf_liq"] = [0.10, 0.05, 0.0]
        elif s == "private_markdown":
            shock["private_markdown"] = 0.20
        elif s == "calls_spike":
            shock["call_mult"] = 1.5
        elif s == "draw_10":
            shock["draw_fixed"] = 0.10
        else:
            raise KeyError(f"unknown stress {s}")
    return gen, shock


def _gen_params(gen_over: dict):
    over = {k: v for k, v in gen_over.items() if not k.startswith("_")}
    MP = mpo_params(over)
    if gen_over.get("_crisis_corr_sign") == -1:
        corr = [list(r) for r in MP.get("factors.corr_crisis")]
        corr[0][2] = corr[2][0] = -0.30
        MP.overrides["factors.corr_crisis"] = corr
    return MP


_FACTOR_MEAN_CACHE: dict = {}


def pop_factor_mean(P, stress: str = "base", n: int = 8000) -> np.ndarray:
    """Population mean annual factor return for a scenario (large fixed-seed sample, cached)."""
    gen_over, _ = stress_overrides(stress, P)
    key = json.dumps(gen_over, sort_keys=True) + str(n)
    if key not in _FACTOR_MEAN_CACHE:
        MP = _gen_params(gen_over)
        gen = Generator(MP)
        rng = np.random.default_rng(int(P.get("simulation.seed_factor_means")))
        st = gen.start_state(n, rng)
        sim = gen.simulate(st, NQ, rng)
        _FACTOR_MEAN_CACHE[key] = sim["f"].mean(axis=(0, 1)) * 4
    return _FACTOR_MEAN_CACHE[key]


def factor_means(P) -> np.ndarray:
    """E[f] in the BASE case (today's state): calibrates every alpha, so a stress moves returns."""
    return pop_factor_mean(P, "base")


def _risk_override(P, b) -> dict:
    """risk.bucket_overrides in config/assumptions.json: per-bucket loadings and idiosyncratic vol (ASSUMPTION)."""
    try:
        return dict((P.get("risk.bucket_overrides") or {}).get(b.id, {}))
    except KeyError:
        return {}


def _loadings(MP, b, P=None) -> np.ndarray:
    ov = _risk_override(P, b) if P is not None else {}
    if ov.get("B") is not None:
        return np.asarray(ov["B"], float)
    if b.B:
        return np.asarray(b.B, float)
    return np.asarray(segment(MP, b.segment)["B"], float)


def _idio(b, P=None) -> float:
    ov = _risk_override(P, b) if P is not None else {}
    return float(ov["idio"]) if ov.get("idio") is not None else float(b.idio or 0.0)


@dataclass
class Factors:
    """Factor / regime paths for n paths (shared by the three worlds)."""
    n: int
    f: np.ndarray            # (n, 20, 6)
    S: np.ndarray            # (n, 21)
    E: np.ndarray
    Z: np.ndarray
    draw: np.ndarray         # (n, 5) owner draw rate per year
    cls_q: np.ndarray        # (n, 20) market state at each quarter end
    cls_y: np.ndarray        # (n, 6) state at year ends (t = 0 today)
    brent: np.ndarray        # (n, 21)
    vix: np.ndarray          # (n, 21)
    MP: object


_FACTOR_CACHE: dict = {}


def factors(P, stress: str, n: int, seed: int) -> Factors:
    gen_over, shock = stress_overrides(stress, P)
    key = hashlib.sha256((json.dumps(gen_over, sort_keys=True) + f"|{n}|{seed}").encode()).hexdigest()
    if key in _FACTOR_CACHE:
        return _FACTOR_CACHE[key]
    MP = _gen_params(gen_over)
    gen = Generator(MP)
    rng = np.random.default_rng(seed)
    st = gen.start_state(n, rng)
    sim = gen.simulate(st, NQ, rng)
    # variance reduction: match the sample's mean factor return to this scenario's population mean (first moment
    # only; paths, regimes and co-movement are untouched), so plan comparisons are not driven by sampling noise
    sim["f"] = sim["f"] - sim["f"].mean(axis=(0, 1)) + pop_factor_mean(P, stress) / 4
    cls_q = np.zeros((n, NQ), int)
    for q in range(NQ):
        dprev = sim["draw"][:, q // 4]
        dn = gen.expected_next_draw(np.exp(sim["lb"][:, q + 1]), dprev, sim["Z"][:, q + 1])
        cls_q[:, q] = node_class(sim["S"][:, q + 1], sim["E"][:, q + 1], sim["Z"][:, q + 1], dn, MP)
    cls_y = np.zeros((n, 6), int)
    cls_y[:, 0] = int(P.get("bids.today_state"))
    cls_y[:, 1:] = cls_q[:, 3::4]
    F = Factors(n, sim["f"], sim["S"], sim["E"], sim["Z"], sim["draw"], cls_q, cls_y, np.exp(sim["lb"]), sim["vix"], MP)
    _FACTOR_CACHE[key] = F
    if len(_FACTOR_CACHE) > 24:
        _FACTOR_CACHE.pop(next(iter(_FACTOR_CACHE)))
    return F


class PathSet:
    """Everything the LP and the simulator need on one set of scenarios (n factor paths x 3 worlds).

    Index m = w * n + j. Quarterly arrays have 21 points (levels, t = 0..20 quarters) or 20 (flows in quarter q).
    """

    def __init__(self, book, P, n: int, seed: int, stress: str = "base", pi=None, settings: dict | None = None):
        st = settings or {}
        self.book, self.P, self.n, self.stress = book, P, n, stress
        self.W = 3
        self.m = 3 * n
        pi = np.asarray(pi if pi is not None else [0.25, 0.5, 0.25], float)
        self.pi = pi / pi.sum()
        self.world = np.repeat(np.arange(3), n)
        self.prob = self.pi[self.world] / n
        F = factors(P, stress, n, seed)
        self.F = F
        # regimes at each year end on every path (macro: expansion / late cycle / crisis / recovery; exit window:
        # open / normal / drought / frozen), for the year-by-year view
        self.macro_y = np.tile(np.asarray(F.S)[:, 4::4][:, :5], (3, 1))
        self.exit_y = np.tile(np.asarray(F.E)[:, 4::4][:, :5], (3, 1))
        MP = F.MP
        gen_over, shock = stress_overrides(stress, P)
        self.shock = shock
        Ef = factor_means(P)
        self.Ef = Ef
        rf = float(P.get("rates.sofr"))
        self.rf = rf
        self.rf_fin = rf + shock["rate_bp"] / 1e4
        geo = P.get("returns.er_return_type") == "geometric"
        tile = lambda a: np.tile(a, (3,) + (1,) * (a.ndim - 1))
        f = tile(F.f) + shock["fshock"][None, :, :]      # (m, 20, 6), stress shocks added after mean matching
        self.cls_q, self.cls_y = tile(F.cls_q), tile(F.cls_y)
        if shock["draw_fixed"] is not None:
            self.draw = np.full((self.m, 5), float(shock["draw_fixed"]))
        elif st.get("draw_mode", P.get("owner_distribution.mode")) == "fixed_rate":
            self.draw = np.full((self.m, 5), float(st.get("draw_rate", P.get("owner_distribution.fixed_rate"))))
        else:
            self.draw = tile(F.draw)
        Eq, Sq = tile(F.E[:, 1:]), tile(F.S[:, 1:])
        rng = np.random.default_rng(seed + 7)

        def alpha(R_w, B, sig2=0.0):
            R_w = np.asarray(R_w, float)
            lm = np.log1p(R_w) if geo else np.log1p(R_w) - 0.5 * sig2
            return lm - rf - float(B @ Ef)

        # ---------------- liquid and reserve buckets: cumulative gross factors (m, 21)
        self.G = {}
        self.rq = {}
        br = book.bucket_ret
        for b in CATALOG:
            if b.private:
                continue
            B = _loadings(MP, b, P)
            Rw = [br.loc[b.id, f"exist_{w}"] for w in WORLDS]
            a = np.array([alpha(Rw[w], B) for w in range(3)])[self.world]          # (m,)
            z = np.tile(rng.standard_normal((self.n, NQ)), (3, 1))
            r = rf / 4 + f @ B + a[:, None] / 4 + _idio(b, P) / 2 * z
            if b.id in ("CASH", "TREASURY"):          # a rate shock raises cash and Treasury carry
                r = r + shock["rate_bp"] / 1e4 / 4
            self.rq[b.id] = r
            g = np.ones((self.m, NQ + 1))
            g[:, 1:] = np.exp(np.cumsum(r, axis=1))
            self.G[b.id] = g
        # synthetic beta: excess return per $ notional per quarter on developed-market equity
        self.eq_excess_q = np.exp(self.rq["GE_DM"]) - np.exp(rf / 4)
        # ---------------- private units: full original size, all cohorts in one engine run
        self.units = book.units
        mark = 1.0 - shock["private_markdown"]
        coh, owner = [], []
        for k, u in enumerate(book.units):
            for c in u.cohorts:
                coh.append((u, c))
                owner.append(k)
        owner = np.array(owner)
        self.unit_owner = owner
        segs = [segment(MP, BY_ID[u.bucket].segment) for u, _ in coh]
        spec = {"B": np.array([_loadings(MP, BY_ID[u.bucket], P) for u, _ in coh]),
                "yield": np.array([s["yield"] for s in segs]), "dist": np.array([s["dist"] for s in segs]),
                "call": np.array([s["call"] for s in segs]) * shock["call_mult"],
                "edges": np.array([s["edges"] for s in segs], float), "phi": np.array([s["phi"] for s in segs]),
                "liquid": np.zeros(len(coh), bool)}
        eng = UnitEngine(spec, MP)
        A = np.array([[alpha(u.r_world[w], spec["B"][i]) for w in range(3)] for i, (u, _) in enumerate(coh)])
        a_m = A[:, self.world].T                                                   # (m, I)
        sig = np.array([_idio(BY_ID[u.bucket], P) for u, _ in coh])
        V0 = np.array([c["nav"] for _, c in coh]) * mark
        U0 = np.array([c["unf"] for _, c in coh])
        age0 = np.array([c["age"] for _, c in coh])
        s = eng.init_state(self.m, V0, V0, U0, age0)
        I = len(coh)
        K = len(book.units)
        M = np.zeros((I, K))
        M[np.arange(I), owner] = 1.0                                                # cohort -> unit aggregation
        self.uV, self.uU = np.zeros((self.m, NQ + 1, K)), np.zeros((self.m, NQ + 1, K))
        self.uD, self.uC = np.zeros((self.m, NQ, K)), np.zeros((self.m, NQ, K))
        self.uV[:, 0], self.uU[:, 0] = s["V"] @ M, s["U"] @ M
        for q in range(NQ):
            z = np.tile(rng.standard_normal((self.n, I)), (3, 1))
            s, D, C, _ = eng.step(s, f[:, q], Eq[:, q], Sq[:, q], a_m, sig[None, :] / 2 * z)
            self.uV[:, q + 1], self.uU[:, q + 1] = s["V"] @ M, s["U"] @ M
            self.uD[:, q], self.uC[:, q] = D @ M, C @ M
        # bids per unit at year ends t = 0..5: rho[key][state] x bid factor at the sale year (tau capped at 2)
        rho = {k: list(v) for k, v in MP._leaf("bids.rho")["value"].items()}
        rho.update({k: list(v) for k, v in P.get("bids.rho_extra").items()})
        lo, hi = P.get("bids.clip")
        bid = np.zeros((self.m, 6, K))
        self.unit_bid_state = np.zeros((K, 3, 3))                                   # [unit, tau, state]
        for k, u in enumerate(book.units):
            r = np.array(rho[BY_ID[u.bucket].bid_key])
            for t in range(6):
                bid[:, t, k] = np.clip(r[self.cls_y[:, t]] * u.bidfac[min(t, 2)], lo, hi)
            for tau in range(3):
                self.unit_bid_state[k, tau] = np.clip(r * u.bidfac[tau], lo, hi)
        self.ubid = bid
        # ---------------- templates: $1 committed (fund buckets) or deployed (co-invest buckets) at year tau
        self.tpl_buckets = [b for b in PRIVATE]
        T = len(self.tpl_buckets)
        tsegs = [segment(MP, BY_ID[b].segment) for b in self.tpl_buckets]
        tspec = {"B": np.array([_loadings(MP, BY_ID[b], P) for b in self.tpl_buckets]),
                 "yield": np.array([s["yield"] for s in tsegs]), "dist": np.array([s["dist"] for s in tsegs]),
                 "call": np.array([s["call"] for s in tsegs]) * shock["call_mult"],
                 "edges": np.array([s["edges"] for s in tsegs], float), "phi": np.array([s["phi"] for s in tsegs]),
                 "liquid": np.zeros(T, bool)}
        teng = UnitEngine(tspec, MP)
        TA = np.array([[alpha(br.loc[b, f"new_{w}"], tspec["B"][i]) for w in WORLDS]
                       for i, b in enumerate(self.tpl_buckets)])
        ta_m = TA[:, self.world].T
        tsig = np.array([_idio(BY_ID[b], P) for b in self.tpl_buckets])
        is_fund = np.array([BY_ID[b].is_fund for b in self.tpl_buckets])
        tage = np.array([6.0 if b.startswith("SEC_LP") else 0.0 for b in self.tpl_buckets])
        # levels at year ends only (t = 0..5); flows quarterly (float32: the certification set is large)
        self.tV = np.zeros((5, self.m, 6, T), np.float32)
        self.tU = np.zeros((5, self.m, 6, T), np.float32)
        self.tD = np.zeros((5, self.m, NQ, T), np.float32)
        self.tC = np.zeros((5, self.m, NQ, T), np.float32)
        for tau in range(5):
            q0 = 4 * tau
            V0t = np.where(is_fund, 0.0, 1.0)
            U0t = np.where(is_fund, 1.0, 0.0)
            s = teng.init_state(self.m, V0t, V0t, U0t, tage)
            self.tV[tau, :, tau], self.tU[tau, :, tau] = s["V"], s["U"]
            for q in range(q0, NQ):
                z = np.tile(rng.standard_normal((self.n, T)), (3, 1))
                s, D, C, _ = teng.step(s, f[:, q], Eq[:, q], Sq[:, q], ta_m, tsig[None, :] / 2 * z)
                if (q + 1) % 4 == 0:
                    self.tV[tau, :, (q + 1) // 4], self.tU[tau, :, (q + 1) // 4] = s["V"], s["U"]
                self.tD[tau, :, q], self.tC[tau, :, q] = D, C
        self.tpl_is_fund = is_fund
        self.tpl_bid_state = np.array([np.clip(np.array(rho[BY_ID[b].bid_key]), lo, hi) for b in self.tpl_buckets])
        # status-quo portfolio's annual return per scenario (accrues draws in the LP's goal wealth)
        self._sq_return()

    # ------------------------------------------------------------------ helpers
    def year_flows(self, X: np.ndarray) -> np.ndarray:
        """Quarterly flows (..., 20, k) -> annual sums (..., 5, k)."""
        sh = X.shape
        return X.reshape(sh[:-2] + (5, 4) + sh[-1:]).sum(-2)

    def year_levels(self, X: np.ndarray) -> np.ndarray:
        """Quarterly levels (..., 21, k) -> year ends t = 0..5 (..., 6, k)."""
        return X[..., ::4, :]

    def _sq_return(self):
        """Approximate annual return of the status-quo book per scenario (value-weighted buckets, flows excluded)."""
        bk = self.book
        num = np.zeros((self.m, 6))
        for bid, v in bk.liquid.items():
            num += v * self.G[bid][:, ::4]
        Vy = self.uV[:, ::4, :].sum(-1)
        Dy = np.zeros((self.m, 6))
        Cy = np.zeros((self.m, 6))
        Dy[:, 1:] = self.year_flows(self.uD).sum(-1)
        Cy[:, 1:] = self.year_flows(self.uC).sum(-1)
        tot = num + Vy
        r = np.zeros((self.m, 6))
        r[:, 1:] = (tot[:, 1:] + Dy[:, 1:] - Cy[:, 1:]) / np.maximum(tot[:, :-1], 1e-9) - 1.0
        self.r_sq = r

    def accrual(self) -> np.ndarray:
        """A[m, t]: growth factor from the end of year t to year 5 at the status-quo return (t = 1..5; A[:, 5] = 1)."""
        A = np.ones((self.m, 6))
        for t in range(4, 0, -1):
            A[:, t] = A[:, t + 1] * (1.0 + self.r_sq[:, t + 1])
        return A
