"""Component 2a: the scenario generator and the quarterly unit engine (SYNTHETIC - NOT ADIC DATA).

One quarterly engine is shared by the tree builder (component 2) and the simulator (component 4), so the tree and the
out-of-sample paths use the same ledger code (SLIM section 1.5; DSGO section 5.1).

Generator (DSGO section 5.1): three coupled regime chains - macro S {expansion, late-cycle, crisis, recovery}, exit
window e {open, normal, drought, frozen}, oil-shock type Z {normal, boom, glut, demand bust, supply shock, Gulf war} -
and six return factors driven by t5 shocks with regime-dependent volatility and correlation:
  eq   equity excess log return        cr  credit excess return (carry - duration x d(spread) - expected loss)
  rt   duration excess return          oil d log Brent
  ex   change in the private exit factor   vol  d(VIX)/100
Regimes move volatility, tails, cash flows, bids and availability but NOT next quarter's expected equity return: the
regime shift of the quarter entered is centred on its expectation given the quarter left (no timing signal; TD
verify_finance M2). Worlds M1, M2, M6 (DSGO RV-14) shift the equity, credit and term premia.
"""
from __future__ import annotations

import numpy as np

from common import Params


def _chol(R):
    R = np.asarray(R, float)
    w, V = np.linalg.eigh(R)
    w = np.clip(w, 1e-8, None)
    R2 = (V * w) @ V.T
    d = np.sqrt(np.diag(R2))
    R2 = R2 / np.outer(d, d)
    return np.linalg.cholesky(R2)


def _cat(u, cum_rows):
    """Sample categorical next states: u (n,), cum_rows (n, K) cumulative probabilities."""
    return np.minimum((u[:, None] > cum_rows).sum(1), cum_rows.shape[1] - 1)


class Generator:
    """Quarterly regime-switching factor generator."""

    def __init__(self, P: Params):
        g = P.get
        self.P = P
        self.rf = g("rates.sofr")
        self.Ps = P.arr("regimes.macro.P_q")
        self.Pe = P.arr("regimes.exit.P_q")
        self.Pz = P.arr("regimes.oil.P_q")
        self.s0p = P.arr("regimes.macro.start")
        self.e0p = P.arr("regimes.exit.start")
        self.z0p = P.arr("regimes.oil.start")
        self.push = g("regimes.exit.crisis_push_q")
        self.cr_db = g("regimes.oil.crisis_given_demand_bust_q")
        self.cr_glut = g("regimes.oil.crisis_given_glut_q")
        self.eq_shift = P.arr("factors.eq.regime_shift_q")
        self.eq_vol = P.arr("factors.eq.vol_annual")
        self.Ec = self.Ps @ self.eq_shift
        self.nu = g("factors.t_dof")
        self.cs_lev = P.arr("factors.cr.level")
        self.cs0 = g("factors.cr.start")
        self.cs_k = g("factors.cr.kappa_q")
        self.cs_vol = P.arr("factors.cr.vol_q")
        self.cs_D = g("factors.cr.duration")
        self.pd = P.arr("factors.cr.pd_annual")
        self.lgd = g("factors.cr.lgd")
        self.y0 = g("factors.rt.start")
        self.ybar = g("factors.rt.mean")
        self.y_k = g("factors.rt.kappa_q")
        self.y_vol = g("factors.rt.vol_q")
        self.y_crisis = g("factors.rt.crisis_shift_q")
        self.y_D = g("factors.rt.duration")
        self.lb0 = np.log(g("factors.oil.spot"))
        self.oil_lev = np.log(P.arr("factors.oil.level"))
        self.oil_k = g("factors.oil.kappa_q")
        self.oil_vol = P.arr("factors.oil.vol_q")
        self.x_lev = P.arr("factors.ex.level")
        self.x0 = g("factors.ex.start")
        self.x_phi = g("factors.ex.phi_q")
        self.x_sig = g("factors.ex.sigma_q")
        self.v_lev = P.arr("factors.vix.level")
        self.v0 = g("factors.vix.start")
        self.v_k = g("factors.vix.kappa_q")
        self.v_dn = g("factors.vix.spot_down")
        self.v_up = g("factors.vix.spot_up")
        self.v_sig = g("factors.vix.sigma_q")
        self.v_floor = g("factors.vix.floor")
        self.L_norm = _chol(P.arr("factors.corr_normal"))
        self.L_cris = _chol(P.arr("factors.corr_crisis"))
        self.w_names = g("worlds.names")
        self.w_prob = P.arr("worlds.weights")
        self.w_eq = P.arr("worlds.eq_log_excess")
        self.w_cr = P.arr("worlds.credit_drift")
        self.w_tp = P.arr("worlds.term_premium")
        # owner draw
        self.d_prior = g("owner_draw.prior_rate")
        self.d_floor = g("owner_draw.floor")
        self.d_cap = g("owner_draw.cap")
        self.k_hi = g("owner_draw.kink_high")
        self.k_lo = g("owner_draw.kink_low")
        self.d_s = g("owner_draw.smoothing")
        self.ov_p = P.arr("owner_draw.override_prob")
        self.ov_size = g("owner_draw.override_size")
        self.cum_s = np.cumsum(self.Ps, 1)
        self.cum_e = np.cumsum(self.Pe, 1)
        self.cum_z = np.cumsum(self.Pz, 1)
        self.c_oil = np.zeros(self.Pz.shape[0])          # crisis probability by oil state entered
        self.c_oil[3] = self.cr_db
        self.c_oil[2] = self.cr_glut

    # ------------------------------------------------------------------ state helpers
    def start_state(self, n, rng, world=None):
        """t0 state for n paths: regimes drawn from the start probabilities (drought 0.87, Gulf war 0.85)."""
        st = {
            "S": _cat(rng.random(n), np.tile(np.cumsum(self.s0p), (n, 1))),
            "E": _cat(rng.random(n), np.tile(np.cumsum(self.e0p), (n, 1))),
            "Z": _cat(rng.random(n), np.tile(np.cumsum(self.z0p), (n, 1))),
            "cs": np.full(n, self.cs0), "y": np.full(n, self.y0), "lb": np.full(n, self.lb0),
            "X": np.full(n, self.x0), "vix": np.full(n, self.v0),
            "d_prev": np.full(n, self.d_prior),
        }
        if world is None:
            u = rng.random(n)
            world = np.minimum((u[:, None] > np.cumsum(self.w_prob)).sum(1), len(self.w_prob) - 1)
        st["w"] = np.asarray(world, int)
        return st

    def draw_rate(self, brent, d_prev, Z, u):
        tgt = self.d_floor + (self.d_cap - self.d_floor) * (self.k_hi - brent) / (self.k_hi - self.k_lo)
        tgt = np.clip(tgt, self.d_floor, self.d_cap)
        tgt = np.clip(tgt + self.ov_size * (u < self.ov_p[Z]), self.d_floor, self.d_cap)
        return np.clip(self.d_s * d_prev + (1 - self.d_s) * tgt, self.d_floor, self.d_cap)

    def expected_next_draw(self, brent, d_prev, Z):
        """E[d_next | state] (the override enters at its probability)."""
        base = self.draw_rate(brent, d_prev, Z, np.ones_like(brent))
        bump = self.draw_rate(brent, d_prev, Z, np.zeros_like(brent))
        p = self.ov_p[Z]
        return (1 - p) * base + p * bump

    # ------------------------------------------------------------------ one quarter
    def step(self, st, rng):
        """One quarter. Price factors (credit, rates, oil, exit, vol) enter asset returns as SURPRISES against their
        conditional expectation, so expected mean reversion (Brent falling down the strip, exits recovering from the
        drought, VIX drifting to its regime level) is not a predictable asset return: it is already in today's
        economic NAV. Carry (spreads, term premium) and the equity premium are the expected returns."""
        n = len(st["S"])
        u = rng.random((n, 5))
        nrm = rng.standard_normal((n, 6))
        chi = rng.chisquare(self.nu, n)
        S, E, Z = st["S"], st["E"], st["Z"]
        Z1 = _cat(u[:, 0], self.cum_z[Z])
        c = np.where(Z1 == 3, self.cr_db, np.where(Z1 == 2, self.cr_glut, 0.0))   # oil-driven crisis probability
        S1 = _cat(u[:, 1], self.cum_s[S])
        S1 = np.where(u[:, 2] < c, 2, S1)
        E1 = _cat(u[:, 3], self.cum_e[E])
        E1 = np.where((S1 == 2) & (u[:, 4] < self.push), np.minimum(E1 + 1, 3), E1)
        crisis = S1 == 2
        z5 = np.where(crisis[:, None], nrm[:, :5] @ self.L_cris.T, nrm[:, :5] @ self.L_norm.T)
        t5 = z5 / np.sqrt(chi / self.nu)[:, None] * np.sqrt((self.nu - 2) / self.nu)
        w = st["w"]
        f = np.empty((n, 6))
        # Expectations use START-of-quarter information (S, Z) only: the oil shock Z1 drawn during the quarter is a
        # surprise, so a demand-bust crisis onset is an equity loss, not an expected return. c_bar integrates the
        # oil-driven crisis probability over Z1 given Z (P(S1 = s | S, Z) = c_bar 1{s = crisis} + (1 - c_bar) P_S[S, s]).
        c = self.Pz[Z] @ self.c_oil
        Eq = lambda q: c * q[2] + (1 - c) * (self.Ps[S] @ q)
        f[:, 0] = self.w_eq[w] / 4 + (self.eq_shift[S1] - Eq(self.eq_shift)) + self.eq_vol[S1] / 2 * t5[:, 0]
        cs_exp = st["cs"] + self.cs_k * (Eq(self.cs_lev) - st["cs"])
        cs1 = np.maximum(st["cs"] + self.cs_k * (self.cs_lev[S1] - st["cs"]) + self.cs_vol[S1] * t5[:, 1], 0.005)
        f[:, 1] = st["cs"] / 4 - self.cs_D * (cs1 - cs_exp) - self.pd[S1] * self.lgd / 4 + self.w_cr[w] / 4
        p_cris = c + (1 - c) * self.Ps[S, 2]
        y_exp = st["y"] + self.y_k * (self.ybar - st["y"]) + self.y_crisis * p_cris
        y1 = np.maximum(st["y"] + self.y_k * (self.ybar - st["y"]) + self.y_crisis * crisis + self.y_vol * t5[:, 2], 0.0)
        f[:, 2] = self.w_tp[w] / 4 - self.y_D * (y1 - y_exp)
        lb_exp = st["lb"] + self.oil_k * (self.Pz[Z] @ self.oil_lev - st["lb"])
        lb1 = st["lb"] + self.oil_k * (self.oil_lev[Z1] - st["lb"]) + self.oil_vol[Z1] * t5[:, 3]
        f[:, 3] = lb1 - lb_exp
        x_up = self.x_lev[np.minimum(np.arange(4) + 1, 3)]          # level one exit window worse
        pp = (p_cris * self.push)[:, None]
        x_exp = ((1 - pp) * self.Pe[E] * self.x_lev + pp * self.Pe[E] * x_up).sum(1) + self.x_phi * (st["X"] - self.x_lev[E])
        X1 = self.x_lev[E1] + self.x_phi * (st["X"] - self.x_lev[E]) + self.x_sig * t5[:, 4]
        f[:, 4] = X1 - x_exp
        req = 100 * f[:, 0]
        v1 = (st["vix"] + self.v_k * (self.v_lev[S1] - st["vix"]) + self.v_dn * np.minimum(req, 0)
              + self.v_up * np.maximum(req, 0) + self.v_sig * nrm[:, 5])
        v1 = np.maximum(v1, self.v_floor)
        mu_r = 100 * self.w_eq[w] / 4
        sd_r = np.maximum(100 * Eq(self.eq_vol) / 2, 1e-6)
        from scipy.stats import norm as _n
        e_min = mu_r * _n.cdf(-mu_r / sd_r) - sd_r * _n.pdf(mu_r / sd_r)
        spot_exp = self.v_dn * e_min + self.v_up * (mu_r - e_min)
        v_exp = st["vix"] + self.v_k * (Eq(self.v_lev) - st["vix"]) + spot_exp
        f[:, 5] = (v1 - v_exp) / 100
        new = dict(st)
        new.update(S=S1, E=E1, Z=Z1, cs=cs1, y=y1, lb=lb1, X=X1, vix=v1)
        return new, f

    def simulate(self, st0, n_q, rng):
        """Simulate n_q quarters from st0. Returns a path dict with states (n, n_q+1), factors (n, n_q, 6) and the
        owner-draw rate of each fiscal year that starts inside the window (one per 4 quarters, set at its start)."""
        n = len(st0["S"])
        keys = ["S", "E", "Z", "cs", "y", "lb", "X", "vix"]
        out = {k: np.empty((n, n_q + 1), dtype=(int if k in "SEZ" else float)) for k in keys}
        for k in keys:
            out[k][:, 0] = st0[k]
        F = np.empty((n, n_q, 6))
        n_y = (n_q + 3) // 4
        D = np.empty((n, n_y))
        st = dict(st0)
        d_prev = st0["d_prev"].copy()
        for q in range(n_q):
            if q % 4 == 0:
                u = rng.random(n)
                d = self.draw_rate(np.exp(st["lb"]), d_prev, st["Z"], u)
                D[:, q // 4] = d
                d_prev = d
            st, f = self.step(st, rng)
            F[:, q] = f
            for k in keys:
                out[k][:, q + 1] = st[k]
        out["f"] = F
        out["draw"] = D
        out["w"] = st0["w"].copy()
        out["d_last"] = d_prev
        return out


def node_class(S, E, Z, d_next, P: Params):
    """BEN / DRT / STR node classes (DSGO section 1.1): STR = macro crisis, frozen exits, or a demand-bust or glut
    shock with the next draw >= the stress draw threshold; DRT = exit drought; BEN otherwise."""
    thr = P.get("tree.str_draw_threshold")
    strs = (S == 2) | (E == 3) | (((Z == 3) | (Z == 2)) & (d_next >= thr))
    drt = (E == 2) & ~strs
    return np.where(strs, 2, np.where(drt, 1, 0))


class UnitEngine:
    """Full-position quarterly engine for a set of units (existing holdings or per-$ templates).

    Each unit carries economic NAV V, reported NAV N, unfunded U and its age. Decisions only scale the fraction held,
    so every flow of a position is linear in the fraction (DSGO section 1.3, positive homogeneity).
      economic log return  r = rf/4 + f.b + a/4 (+ idiosyncratic noise in the simulator)
      distributions        D = income yield x V + exit intensity(age) x m_D(exit window) x V
      calls                C = call intensity(age) x m_C(exit window) x stress(crisis) x U
      reported NAV         log return (1-phi) r_lag + phi r_rep_lag + kappa_theta ln(V/N), scaled down by exits
    """

    def __init__(self, spec: dict, P: Params):
        self.rf = P.get("rates.sofr")
        self.mD = P.arr("private_engine.exit_dist_mult")
        self.mC = P.arr("private_engine.exit_call_mult")
        self.stress = P.get("private_engine.crisis_call_stress")
        self.kth = P.get("private_engine.kappa_theta_q")
        self.B = np.asarray(spec["B"], float)                 # (I, 6)
        self.yld = np.asarray(spec["yield"], float)           # (I,)
        self.dist = np.asarray(spec["dist"], float)           # (I, 4) annual exit intensity by age bucket
        self.call = np.asarray(spec["call"], float)           # (I, 4) annual call intensity by age bucket
        self.edges = np.asarray(spec["edges"], float)         # (I, 3) age bucket edges
        self.phi = np.asarray(spec["phi"], float)             # (I,)
        self.liquid = np.asarray(spec["liquid"], bool)        # (I,)
        self.I = self.B.shape[0]

    def _bucket(self, age):
        """age (n, I) -> age-bucket index (n, I) in 0..3 using each unit's own three edges."""
        return (age[:, :, None] >= self.edges[None, :, :]).sum(-1)

    def init_state(self, n, V, N, U, age):
        sh = (n, self.I)
        return {"V": np.broadcast_to(np.asarray(V, float), sh).copy(),
                "N": np.broadcast_to(np.asarray(N, float), sh).copy(),
                "U": np.broadcast_to(np.asarray(U, float), sh).copy(),
                "age": np.broadcast_to(np.asarray(age, float), sh).copy(),
                "rl": np.zeros(sh), "rr": np.zeros(sh)}

    def step(self, st, f, E, S, alpha, idio=None, active=None):
        """Advance one quarter. f (n, 6); E, S (n,); alpha (I,) or (n, I) annual log alpha.
        active (n, I) bool: units that exist yet (templates start later); inactive units are left untouched."""
        r = self.rf / 4 + f @ self.B.T + np.asarray(alpha) / 4
        if idio is not None:
            r = r + idio
        g = np.exp(r)
        Vg = st["V"] * g
        b = self._bucket(st["age"])
        cols = np.arange(self.I)[None, :]
        ex_int = self.dist[cols, b]
        c_int = self.call[cols, b]
        inc = Vg * self.yld / 4
        exits = (Vg - inc) * (1 - np.exp(-ex_int * self.mD[E][:, None] / 4))
        D = inc + exits
        stress = np.where(S == 2, self.stress, 1.0)[:, None]
        C = st["U"] * (1 - np.exp(-c_int * self.mC[E][:, None] * stress / 4))
        V1 = Vg - D + C
        theta = np.where(st["N"] > 1e-12, st["V"] / np.maximum(st["N"], 1e-12), 1.0)
        rr = (1 - self.phi) * st["rl"] + self.phi * st["rr"] + self.kth * np.log(np.clip(theta, 1e-6, None))
        keep = np.where(Vg > 1e-12, 1 - D / np.maximum(Vg, 1e-12), 0.0)
        N1 = st["N"] * np.exp(rr) * keep + C
        N1 = np.where(self.liquid[None, :], V1, N1)
        rr = np.where(self.liquid[None, :], r, rr)
        new = {"V": V1, "N": N1, "U": st["U"] - C, "age": st["age"] + 0.25, "rl": r, "rr": rr}
        if active is not None:
            for k in new:
                new[k] = np.where(active, new[k], st[k])
            D = np.where(active, D, 0.0)
            C = np.where(active, C, 0.0)
        return new, D, C, r


def factor_means(gen: Generator, P: Params, rng, n=None, years=None):
    """Average expected factor log returns over the first `years` years from the t0 state (pooled worlds).
    Used to translate a unit's expected forward return into its alpha: a_i = mu_i - rf - b_i . E[f]."""
    n = n or P.get("tree.n_factor_mean_paths")
    years = years or P.get("goal.years")
    st = gen.start_state(n, rng)
    sim = gen.simulate(st, 4 * years, rng)
    fq = sim["f"].mean(axis=(0, 1))          # mean quarterly factor return
    by_world = {}
    for k, name in enumerate(gen.w_names):
        m = sim["w"] == k
        by_world[name] = (sim["f"][m].mean(axis=(0, 1)) * 4).tolist()
    return fq * 4, by_world
