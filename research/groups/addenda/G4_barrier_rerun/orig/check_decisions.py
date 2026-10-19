"""Independent re-check of G4 dossier section 6.5 decision examples (SELL bid, REFI breach).

Replicates the G4_coinvest_calcs.py section6 assumptions, then:
  (a) REFI: probability that the position breaches the 1.5x-LTV trigger (equity < 2/3 NAV)
      or the 2x-LTV default (equity < 1/2 NAV) at ANY quarterly test date, vs. only at exit.
  (b) SELL: bid implied by the dossier's own buyer-return model p = E_b[X]/(1+y_b)^tau
      for y_b in {0.20, 0.25}, using 'our' beliefs as E_b[X].
All inputs are the dossier's illustrative [I] values; nothing here is ADIC data.
"""
import math

import numpy as np

SEED = 20261018 + 6
NAV = 400.0
NOWCAST = 0.97 * NAV
L_NOW = 6.0 / 14.0
EV0 = NOWCAST / (1 - L_NOW)
DEBT = EV0 * L_NOW
H = 0.09


def run(tau, mu_a, s_a, n=400_000, dt=0.25, seed=SEED):
    rng = np.random.default_rng(seed)
    steps = int(round(tau / dt))
    ln_ev = np.full(n, math.log(EV0))
    min_eq = np.full(n, np.inf)
    for _ in range(steps):
        ln_ev += (mu_a - 0.5 * s_a ** 2) * dt + s_a * math.sqrt(dt) * rng.standard_normal(n)
        eq = np.maximum(np.exp(ln_ev) - DEBT, 0.0)
        min_eq = np.minimum(min_eq, eq)
    eq_T = np.maximum(np.exp(ln_ev) - DEBT, 0.0)
    out = dict(
        tau=tau,
        E_exit_equity=float(eq_T.mean()),
        p_trigger_terminal=float((eq_T < NAV * (2 / 3)).mean()),
        p_trigger_pathwise_quarterly=float((min_eq < NAV * (2 / 3)).mean()),
        p_default_terminal=float((eq_T < NAV * 0.5).mean()),
        p_default_pathwise_quarterly=float((min_eq < NAV * 0.5).mean()),
    )
    for yb in (0.20, 0.25):
        bid = out["E_exit_equity"] / (1 + yb) ** tau
        out[f"implied_bid_pct_nav_yb{int(yb*100)}"] = bid / NAV
    out["buyer_irr_at_95pct_bid"] = (out["E_exit_equity"] / (0.95 * NAV)) ** (1 / tau) - 1
    return out


if __name__ == "__main__":
    for name, (tau, mu, s) in {"normal": (2.5, 0.06, 0.28), "drought": (3.5, 0.04, 0.30)}.items():
        r = run(tau, mu, s)
        print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
