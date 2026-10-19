"""SYNTHETIC checks for the DSGO spec review (not ADIC data).

C1  bPOE optimum in a complete market is all-or-nothing (linear-hinge family).
C2  Pure-beta frontier: P(goal) bought by spending the depth-guard budget delta on beta.
C3  Moment-matching rank: 5 children cannot match a full-rank 6x6 covariance.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.stats import norm

W0 = 1.0
T = 5
G = 1.10 ** T            # W*/W0
RF = 0.0389
SIG = 0.144              # log vol (bridge model)


# ---------------------------------------------------------------- C1
def complete_market(geo=0.083, n=400, seed=1):
    """Lognormal market; states = quantiles of Z; state prices from the lognormal kernel."""
    mu_log = np.log1p(geo)
    m_ar = np.exp(mu_log + SIG**2 / 2) - 1
    lam = (np.log1p(m_ar) - np.log1p(RF)) / SIG          # Sharpe (log)
    u = (np.arange(n) + 0.5) / n
    z = norm.ppf(u)
    p = np.full(n, 1.0 / n)
    # kernel: xi = exp(-r T - lam^2 T/2 - lam sqrt(T) z)
    r = np.log1p(RF)
    xi = np.exp(-r * T - 0.5 * lam**2 * T - lam * np.sqrt(T) * z)
    xi = xi / np.sum(p * xi) * np.exp(-r * T)            # normalise discreteness
    q = p * xi                                           # state prices
    s_T = np.exp(T * mu_log + SIG * np.sqrt(T) * z)      # index wealth multiple
    return p, q, z, s_T


def min_bpoe_complete(p, q, Wstar):
    """min_{a>=0,W>=0} E[(a(W*-W)/W0+1)^+] s.t. sum q W = W0 (perspective LP)."""
    n = len(p)
    # vars: y (n), tau (1), zz (n)
    c = np.concatenate([np.zeros(n), [0.0], p])
    # zz_s >= tau*W* - y_s + 1   ->  -y_s + tau*W* - zz_s <= -1
    A1 = np.hstack([-np.eye(n), np.full((n, 1), Wstar), -np.eye(n)])
    b1 = -np.ones(n)
    Aeq = np.concatenate([q, [-W0], np.zeros(n)])[None, :]
    beq = [0.0]
    bounds = [(0, None)] * n + [(0, None)] + [(0, None)] * n
    res = linprog(c, A_ub=A1, b_ub=b1, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")
    y = res.x[:n]; tau = res.x[n]
    W = y / tau
    return res.fun, W, tau


def min_sq_shortfall_complete(p, q, Wstar, k=200):
    """min E[((W*-W)^+)^2] s.t. budget (closed form via bisection on the multiplier)."""
    # pointwise: W = max(0, W* - nu*xi_ratio/2) with xi_ratio = q/p
    xr = q / p
    lo, hi = 0.0, 1e6
    for _ in range(k):
        nu = 0.5 * (lo + hi)
        W = np.clip(Wstar - nu * xr / 2.0, 0.0, Wstar)
        if np.sum(q * W) > W0:
            lo = nu
        else:
            hi = nu
    return W


def c1():
    out = {}
    for geo in (0.083, 0.1047):
        p, q, z, sT = complete_market(geo)
        val, W, tau = min_bpoe_complete(p, q, G)
        pgoal = np.sum(p[W >= G - 1e-9])
        p_zero = np.sum(p[W <= 1e-6])
        levels = np.unique(np.round(W, 4))
        # the plain index (W = sT scaled to budget)
        Widx = sT * W0 / np.sum(q * sT)
        out[geo] = dict(bpoe=val, p_goal=pgoal, p_zero=p_zero, levels=levels[:6].tolist(),
                        n_levels=len(levels), K_over_Wstar=float(W.max() / G),
                        idx_p_goal=float(np.sum(p[Widx >= G])),
                        idx_E=float(np.sum(p * Widx)))
        Wsq = min_sq_shortfall_complete(p, q, G)
        out[geo]["sq_p_zero"] = float(np.sum(p[Wsq <= 1e-6]))
        out[geo]["sq_n_levels"] = int(len(np.unique(np.round(Wsq, 4))))
    return out


# ---------------------------------------------------------------- C2
def lev_stats(geo, L, f=0.0030, n=400000, seed=7):
    """Bridge model: arithmetic m_L = m + (L-1)(m - rf - f); log vol L*sigma."""
    mu_log = np.log1p(geo)
    m = np.exp(mu_log + SIG**2 / 2) - 1
    mL = m + (L - 1) * (m - RF - f)
    sL = L * SIG
    muL = np.log1p(mL) - sL**2 / 2
    rng = np.random.default_rng(seed)
    zz = rng.standard_normal(n)
    W = np.exp(T * muL + sL * np.sqrt(T) * zz)
    pg = np.mean(W >= G)
    w10 = np.sort(W)[: n // 10].mean()              # worst-decile mean of W~/W0
    return pg, w10, np.mean(W)


def c2():
    rows = []
    for geo in (0.083, 0.0884):
        p0, w0, e0 = lev_stats(geo, 1.0)
        for L in (1.00, 1.02, 1.05, 1.10, 1.15, 1.30):
            pg, w10, e = lev_stats(geo, L)
            rows.append(dict(geo=geo, L=L, p_goal=pg, dP_pp=100 * (pg - p0),
                             cvar90_worsen_W0=w0 - w10, E_over_Wstar=e / G))
    return rows


# ---------------------------------------------------------------- C3
def c3():
    names = ["equity", "credit", "rates", "brent", "exit", "draw"]
    C = np.array([
        [1.00, -0.60, 0.10, 0.30, 0.60, -0.25],
        [-0.60, 1.00, -0.20, -0.20, -0.50, 0.20],
        [0.10, -0.20, 1.00, 0.20, 0.00, -0.10],
        [0.30, -0.20, 0.20, 1.00, 0.15, -0.80],
        [0.60, -0.50, 0.00, 0.15, 1.00, -0.15],
        [-0.25, 0.20, -0.10, -0.80, -0.15, 1.00]])
    ev, V = np.linalg.eigh(C)
    res = {"eigenvalues": np.round(ev[::-1], 3).tolist()}
    for k in (4, 3):   # 5 children -> rank <= 4 ; 4 fan paths -> rank <= 3
        idx = np.argsort(ev)[::-1][:k]
        Ck = (V[:, idx] * ev[idx]) @ V[:, idx].T
        d = np.sqrt(np.diag(Ck))
        vol_err = np.max(np.abs(d - 1.0))
        Cn = Ck / np.outer(d, d)
        corr_err = np.max(np.abs(Cn - C))
        res[f"rank{k}"] = dict(max_vol_err=float(vol_err), max_corr_err=float(corr_err))
    return res


if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    print("C1 complete-market bPOE optimum (SYNTHETIC)")
    for k, v in c1().items():
        print(" geo", k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
    print("C2 pure-beta frontier (SYNTHETIC, bridge model)")
    for r in c2():
        print("  geo {geo:.4f} L {L:.2f}  P(goal) {p_goal:.4f}  dP {dP_pp:+.2f}pp  "
              "CVaR90 worsening {cvar90_worsen_W0:.4f} W0  E/W* {E_over_Wstar:.3f}".format(**r))
    print("C3 moment-matching rank (SYNTHETIC correlation)")
    print(" ", c3())
