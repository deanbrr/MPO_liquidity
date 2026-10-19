"""RA gap 03, step 4: the ENR SELL decision card (fund-held levered upstream, $0.6-0.8bn).

SYNTHETIC - NOT ADIC DATA. The card prices SELL against HOLD on the canonical generator with the oil-aware Tier-1
engine (ra03_t1oil.simulate_oil, SLEEVE block), common random numbers, models M1-M6, do nothing and Mix B:
  * p* = the bid (per $ of reported NAV, at staleness theta = V^A / V*) at which the CRRA(3) certainty equivalent of
    distribution-inclusive wealth is equal under SELL and HOLD (equal-weight M1-M5 mixture; M6 shown separately);
  * HOLD carries the sleeve on V* with beta_eq 0.6, the canonical oil elasticity, oil-elastic distributions, calls
    on its unfunded, a forecast alpha (FBE prior 0; -2% / +2% shown), the transition charge tau and the P-measure
    drift g_PQ (the generator's median curve against the strip);
  * regret both ways is pathwise: E[(W_HOLD - W_SELL)+] and E[(W_SELL - W_HOLD)+] at the base bid;
  * flip thresholds: bid, alpha, theta, war persistence (Weibull k 0.8 / 2.2), funding mix.

Usage: python -I ra03_card_run.py <ledger_json> <out_json> [n_paths]
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402
from ra03_tier1_run import POLICIES  # noqa: E402

E = T.E
N = int(sys.argv[3]) if len(sys.argv) > 3 else 30000
SEED = 20261018
V0 = 0.70                      # $bn sold: mid of $0.6-0.8bn of the $0.80bn fund-held levered upstream
UNF = V0 * 0.6 / 1.6           # unfunded attached (ENR closed-end U/NAV, G15 census)
TAU = 0.0025                   # transition charge, a year [I, G12: 0.25-0.5%]
BETA_EQ = 0.6                  # G12 sec 6.9 (40%-LTV upstream)
COST = 0.01                    # transaction cost [I]
BIDS = np.round(np.arange(0.60, 1.101, 0.05), 3)
REBUILD = True                 # SELL leg rebuilds the sleeve's equity beta with index futures (groups s3.7 TPA service)
BASE_BID, BASE_THETA = 0.86, 1.0


def lev_value(curve: np.ndarray, debt: float | None = None) -> tuple[float, float]:
    Fk = L.annual_avg(curve)
    v = L.pdp_value(Fk)
    d = 0.4 * v if debt is None else debt
    return v - d, v


def pdp_duration(curve: np.ndarray) -> float:
    Fk = L.annual_avg(curve)
    K = np.arange(1, len(Fk) + 1)
    q = np.exp(-L.PDP["decline"] * (K - 0.5))
    nb = np.maximum(Fk * L.PDP["nri"] * (1 - L.PDP["tax"]) - L.PDP["loe"] - L.PDP["ga"] - L.PDP["diff"], 0.0)
    pv = q * nb * (1 + L.PDP["disc"]) ** -(K - 0.5)
    return float((pv * (K - 0.5)).sum() / pv.sum())


def p_median_curve(k_gw: float) -> np.ndarray:
    PZm = L.monthly_lsq(L.PZ_A)[0]
    PS = L.s_chain_for_share(0.1433)
    K, _ = L.calibrate_kappa(PS, PZm)
    g = L.Gen(PS, PZm, K, gw_mode="weibull", gw_k=k_gw)
    sim = g.simulate(n=20000, T=180, seed=7, S0=L.sLATE, Z0=T.Z0, x0=math.log(L.F1), chi0=math.log(L.SPOT / L.F1))
    med = np.median(sim["P"], axis=1)
    return np.concatenate([med, np.full(360 - 180, med[-1])])


def mix_ce(w_inv2: dict, keys) -> float:
    m2 = np.mean([w_inv2[k] for k in keys])
    return m2 ** (-0.5) ** 1


def ce_growth(w_inv2s: list[float]) -> float:
    m2 = float(np.mean(w_inv2s))
    return (m2 ** -0.5) ** 0.2 - 1.0


def main():
    led = json.load(open(sys.argv[1], encoding="utf-8"))
    t0 = time.time()
    out = {"label": L.LABEL, "n_paths": N, "sleeve": {"V0_bn": V0, "unfunded_bn": round(UNF, 3), "tau": TAU,
                                                     "beta_eq": BETA_EQ, "cost": COST}}
    # ---------------- P-measure drift against the strip (glut thesis) and barrels
    Fq = L.observed_curve_monthly(360)
    vq, pdq = lev_value(Fq)
    dur = pdp_duration(Fq)
    gpq = {}
    for k in (1.3, 0.8, 2.2):
        Fp = p_median_curve(k)
        vp, _ = lev_value(Fp, debt=0.4 * pdq)
        gpq[str(k)] = {"V_P_over_V_Q": round(vp / vq, 4), "g_pq_a_year": round((vp / vq - 1) / dur, 4)}
    out["g_pq"] = gpq
    out["pdp_cash_flow_duration_years"] = round(dur, 2)
    lev = led["ledger"]["RA ENR levered upstream (funds 0.80 + direct 0.27)"]
    bbl_per_bn = {st: lev[f"delta_{st}"] / 1.07 for st in ("now", "SG", "DB", "SG24", "DB24")}
    out["delta_bbl_removed"] = {st: [round(-0.6 * v, 2), round(-V0 * v, 2), round(-0.8 * v, 2)]
                                for st, v in bbl_per_bn.items()}
    eps = lev["eps_now"]

    # ---------------- engine runs
    res = {}
    for k_gw in (1.3, 0.8, 2.2):
        g_pq = gpq[str(k_gw)]["g_pq_a_year"]
        for pk in ("do_nothing", "mix_B"):
            pol = POLICIES[pk]
            for mk, m in E.MODELS.items():
                if k_gw != 1.3 and mk not in ("M1", "M4", "M5", "M6"):
                    continue
                gp = T.gen_paths(m, N, SEED + 1000, k_gw=k_gw)
                row = {"hold": {}, "sell": {}}
                for alpha in ((-0.02, 0.0, 0.02) if k_gw == 1.3 else (0.0,)):
                    spec = {"SLEEVE": {"V0": V0, "unf": UNF, "eps": eps, "beta_eq": BETA_EQ,
                                       "alpha": alpha - TAU, "g_pq": g_pq, "sell": False}}
                    r = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=gp)
                    row["hold"][str(alpha)] = {"w_inv2": r["w_inv2"], "p_red": r["p_red"],
                                               "g99.6": r["gstar_q"][0.996], "wt": r["w_tilde"], "red": r["red"]}
                for bid in BIDS:
                    spec = {"SLEEVE": {"V0": V0, "unf": UNF, "eps": eps, "beta_eq": BETA_EQ, "alpha": 0.0,
                                       "g_pq": 0.0, "sell": True, "bid": float(bid), "theta": 1.0, "cost": COST,
                                       "rebuild_beta": REBUILD, "after_topup": True}}
                    r = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=gp)
                    row["sell"][str(bid)] = {"w_inv2": r["w_inv2"], "p_red": r["p_red"],
                                             "g99.6": r["gstar_q"][0.996], "wt": r["w_tilde"], "red": r["red"]}
                row["Z_month"] = gp["Z_month"]
                res[(k_gw, pk, mk)] = row
            print(f"[{time.time() - t0:5.0f}s] k={k_gw} {pk} done", flush=True)

    # ---------------- reservation prices p* (bid x theta at which CE(SELL) = CE(HOLD))
    def pstar(k_gw, pk, alpha, keys):
        ce_h = ce_growth([res[(k_gw, pk, mk)]["hold"][str(alpha)]["w_inv2"] for mk in keys])
        ce_s = np.array([ce_growth([res[(k_gw, pk, mk)]["sell"][str(b)]["w_inv2"] for mk in keys]) for b in BIDS])
        diff = ce_s - ce_h
        if diff[0] > 0:
            return float(BIDS[0]), diff
        if diff[-1] < 0:
            return float("nan"), diff
        i = int(np.argmax(diff >= 0))
        b0, b1, d0, d1 = BIDS[i - 1], BIDS[i], diff[i - 1], diff[i]
        return float(b0 + (b1 - b0) * (-d0) / (d1 - d0)), diff

    M15 = ("M1", "M2", "M3", "M4", "M5")
    card = {}
    for pk in ("do_nothing", "mix_B"):
        for alpha in (-0.02, 0.0, 0.02):
            p_mix, d_mix = pstar(1.3, pk, alpha, M15)
            p_m6, _ = pstar(1.3, pk, alpha, ("M6",))
            card[f"{pk}|alpha{alpha:+.2f}"] = {"p_star_bid_x_theta_M1-M5": round(p_mix, 4),
                                               "p_star_M6": round(p_m6, 4),
                                               "dCE_bp_at_base_bid_M1-M5": round(1e4 * float(
                                                   np.interp(BASE_BID, BIDS, d_mix)), 3)}
        for k in (0.8, 2.2):
            p_k, _ = pstar(k, pk, 0.0, ("M1", "M4", "M5"))
            p_k13, _ = pstar(1.3, pk, 0.0, ("M1", "M4", "M5"))
            card[f"{pk}|war_k{k}"] = {"p_star_M1M4M5": round(p_k, 4), "p_star_M1M4M5_base_k1.3": round(p_k13, 4)}
    out["reservation_prices"] = card

    # ---------------- Tier-1 deltas, regret both ways at the base bid (k = 1.3, alpha = 0)
    t1 = {}
    for pk in ("do_nothing", "mix_B"):
        for mk in E.MODELS:
            row = res[(1.3, pk, mk)]
            h = row["hold"]["0.0"]
            s = row["sell"][f"{BASE_BID:.2f}".rstrip("0") if False else str(round(BASE_BID, 2))] \
                if str(round(BASE_BID, 2)) in row["sell"] else None
            if s is None:   # nearest grid bid
                kk = min(row["sell"], key=lambda b: abs(float(b) - BASE_BID))
                s = row["sell"][kk]
            dW = s["wt"] - h["wt"]
            Z = row["Z_month"]
            war_persists = Z[9] == L.iGW                  # still at war in Jul-2027
            glut_2028 = (Z[15:27] == L.iSG).any(axis=0)
            t1[f"{pk}|{mk}"] = {
                "dP_red_pp_sell_minus_hold": round(100 * (s["p_red"] - h["p_red"]), 4),
                "dG*_q99.6_bn_sell_minus_hold": round(s["g99.6"] - h["g99.6"], 4),
                "E_dW_sell_minus_hold_bn": round(float(dW.mean()), 4),
                "regret_SELL_bn": round(float(np.maximum(-dW, 0).mean()), 4),
                "regret_HOLD_bn": round(float(np.maximum(dW, 0).mean()), 4),
                "P(SELL better)": round(float((dW > 0).mean()), 3),
                "E[dW] war persists to Jul-27 (bn)": round(float(dW[war_persists].mean()), 4),
                "E[dW] glut in 2028 (bn)": round(float(dW[glut_2028].mean()), 4),
                "share_war_persists": round(float(war_persists.mean()), 3),
                "share_glut_2028": round(float(glut_2028.mean()), 3)}
    out["tier1_and_regret_at_bid_0.85"] = t1
    out["notes"] = {"base_bid": "0.85 grid point nearest the 0.86 Gulf-war bid [I]; G15 ladder 0.82 base, 0.80 "
                                "drought, 0.60 SG; Jefferies H1-26: upstream/NR pricing up, no level [S]",
                    "theta": "p* is per $ of reported NAV at theta = 1; at other theta divide by theta",
                    "H_j": "not an input: the CE comparison prices oil risk on J directly; the per-barrel price "
                           "from step 3 is reported alongside"}
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("g_pq", "pdp_cash_flow_duration_years", "delta_bbl_removed",
                                          "reservation_prices")}, indent=1))
    for k, v in t1.items():
        print(k, v)


if __name__ == "__main__":
    main()
