"""Component 1b: three-return fusion - the Forward Belief Engine (SYNTHETIC - NOT ADIC DATA).

DSGO section 3 / SYN section 4.3. Every mark is restated as the annualized forward log return on nowcast economic NAV,
net of fees, over the holding's remaining life H. Since-inception IRR is sunk and only displayed.
  forecast      rho_f = ln(R_f / V*) / H, with R_f = MOIC_f x paid-in - distributions to date   (error kappa_g x range)
  underwritten  rho_u = (ln M_u - ln M_t) / (T_u - age), expires after T_u + 1                  (deals only)
  actual        a~    = mu_k + phi_a (r_actual - r_benchmark), unused before year 3
  market        rho_m = (y_b - pi_b(age)) + ln(p / theta) / D                                    (leave-one-out)
  prior         mu_k  = r_f + b . E[f] + alpha*_group
Group bias is removed with Buhlmann credibility on the quarterly archive, Z = n_eff / (n_eff + 20). Fund interests
use Benktander credibility c* = p / (p + t) between the forecast and the outside-view prior frozen at inception
(no separate underwriting signal). Weights are shrunk halfway to equal until the archive reaches n_eff >= 20;
correlated errors enter only the predictive variance.

Leave-one-out: the belief that drives the unit's own SELL decision excludes the unit's own bid (DSGO section 3.1), so
the reservation price is never pulled toward the price it is compared with. The fused belief including the bid is
reported beside it.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm, t as student_t

from common import Params


def fuse(P: Params, units: list[dict], book: dict, use_beliefs: bool = True) -> list[dict]:
    rf = P.get("rates.sofr")
    prior_sd = P.get("fusion.unit_prior_sd_pp")
    bu_prior = P.get("fusion.bias_prior_underwritten_pp")
    bf_prior = P.get("fusion.bias_prior_forecast_pp")
    k_prior = P.get("fusion.kappa_prior_median")
    cred_c = P.get("fusion.credibility_constant")
    neff_full = P.get("fusion.precision_weights_after_n_eff")
    t_bk = P.get("fusion.benktander_t")
    phi_a = P.get("fusion.actual_weight_phi")
    phi_min_age = P.get("fusion.actual_min_age")
    out_noise = P.get("fusion.outcome_noise")
    yb = P.get("fusion.buyer_required_return")
    pib = P.get("fusion.buyer_seller_gap_by_age")
    pib_edges = P.get("fusion.buyer_seller_gap_age_edges")
    anchor_min_age = P.get("fusion.market_anchor_min_age")
    bid_disp = P.get("fusion.bid_dispersion")
    nu = P.get("fusion.student_t_dof")
    hz_q = P.get("fusion.precision_horizon_quarters")
    flags_p = P.get("fusion.flags")
    archive = book["archive"]
    beliefs = []
    for u, h in zip(units, book["holdings"]):
        g = u["group"]
        arc = archive[g]
        Z = arc["n_eff"] / (arc["n_eff"] + cred_c)
        b_f = Z * arc["mean_forecast_error"] + (1 - Z) * bf_prior[g] / 100
        b_u = Z * arc["mean_underwriting_error"] + (1 - Z) * bu_prior[g] / 100
        cov = min(max(arc["range_coverage"], 0.05), 0.95)
        k_arch = 1.2816 / norm.ppf((1 + cov) / 2)
        kappa = float(np.exp(Z * np.log(k_arch) + (1 - Z) * np.log(k_prior)))
        H, D, age = u["H"], u["D"], u["age"]
        V = h["nav_econ_bn"]
        theta = h["theta"]
        liquid = u["tier"] == "liquid"
        fund = u["kind"] == "fund"
        mu_k = u["mu_prior"]
        sd_k = prior_sd[g] / 100
        signals = {}
        # forecast
        mf = h["marks"]["forecast"]["moic"]

        def rho_from_moic(m):
            if liquid:
                return np.log(max(m, 1e-6)) / H
            R = m * h["paid_in_bn"] - h["distributed_bn"]
            return np.log(max(R, 1e-6) / V) / H

        rf50, rf10, rf90 = (rho_from_moic(mf[k]) for k in ("p50", "p10", "p90"))
        sd_f = kappa * max(rf90 - rf10, 1e-4) / 2.563
        prec_hz = min(1.0, hz_q / (4 * H))
        s_f = rf50 - b_f
        c_star = None
        if fund:
            p_real = h["distributed_bn"] / max(h["distributed_bn"] + h["nav_rep_bn"], 1e-9)
            c_star = p_real / (p_real + t_bk)
            s_f = c_star * s_f + (1 - c_star) * mu_k
            sd_f = np.sqrt((c_star * sd_f) ** 2 + ((1 - c_star) * sd_k) ** 2)
        signals["f"] = {"raw": rf50, "debiased": float(s_f), "sd": float(sd_f / np.sqrt(prec_hz)), "bias": b_f}
        # underwritten (deals and liquid mandates only; expires after T_u + 1)
        mu_ = h["marks"]["underwritten"]["moic"]
        T_u = h["marks"]["underwritten"]["life_y"]
        if liquid:   # mandate underwriting: the expected annual return at hiring, valid for the mandate's life
            ru = lambda m: np.log(m) / (T_u * u["duration_share"])
        else:        # (ln M_u - ln M_t) / (T_u - age): what the holding must return to reach the underwritten MOIC
            m_t = (h["distributed_bn"] + V) / h["paid_in_bn"]
            ru = lambda m: (np.log(m) - np.log(max(m_t, 1e-6))) / (T_u - age)
        if not fund and age <= T_u + 1 and (liquid or T_u - age >= 1.0):
            r_u = ru(mu_["base"])
            sd_u = kappa * max(ru(mu_["up"]) - ru(mu_["down"]), 1e-4) / 2.563
            signals["u"] = {"raw": float(r_u), "debiased": float(r_u - b_u), "sd": float(sd_u), "bias": b_u}
        # actual
        pa = phi_a[u["actual_class"]]
        if age >= phi_min_age and pa > 0:
            a_sig = mu_k + pa * (h["marks"]["actual"]["irr_log"] - h["marks"]["actual"]["bench_log"])
            sd_a = np.sqrt((pa * out_noise[u["noise"]]) ** 2 / max(age, 1.0) + ((1 - pa) * sd_k) ** 2)
            signals["a"] = {"raw": float(a_sig), "debiased": float(a_sig), "sd": float(sd_a), "bias": 0.0}
        # market anchor (own bid; leave-one-out for the decision belief)
        if h["bid"] is not None and age >= anchor_min_age.get(u["bid_key"], 0):
            p = h["bid"]["p_ce"]
            y = yb[u["bid_key"]]
            gap = pib[int(np.searchsorted(pib_edges, age, side="right"))] if u["bid_key"] == "fund" else 0.0
            r_m = (y - gap) + np.log(p / theta) / max(D, 0.5)
            signals["m"] = {"raw": float(r_m), "debiased": float(r_m), "sd": float(bid_disp / max(D, 0.5)), "bias": 0.0}

        def combine(keys):
            vals = [] if fund else [(mu_k, sd_k)]
            names = [] if fund else ["prior"]
            for k in keys:
                if k in signals:
                    vals.append((signals[k]["debiased"], signals[k]["sd"]))
                    names.append(k)
            if not vals:
                return mu_k, sd_k, {"prior": 1.0}
            prec = np.array([1 / s ** 2 for _, s in vals])
            J1 = len(vals)
            w = prec / prec.sum() if arc["n_eff"] >= neff_full else 0.5 * prec / prec.sum() + 0.5 / J1
            w = w / w.sum()
            mu = float(np.dot(w, [v for v, _ in vals]))
            sd = float(np.sqrt(np.sum((w * np.array([s for _, s in vals])) ** 2)))
            wd = dict(zip(names, map(float, w)))
            if fund:   # the prior's weight sits inside the Benktander forecast channel
                wf = wd.get("f", 0.0)
                wd["prior"] = wf * (1 - c_star)
                wd["f"] = wf * c_star
            return mu, sd, wd

        mu_loo, sd_post, w_loo = combine(["f", "u", "a"])
        mu_full, sd_full, w_full = combine(["f", "u", "a", "m"])
        if not use_beliefs:          # F10 switch-off: group prior only
            mu_loo, sd_post, w_loo = mu_k, sd_k, {"prior": 1.0}
        sd_hat = float(np.sqrt(sd_post ** 2 + out_noise[u["noise"]] ** 2 / max(H, 1.0)))
        tq = student_t.ppf([0.1, 0.5, 0.9], nu) * np.sqrt((nu - 2) / nu)
        fl = []
        irr_f50 = h["marks"]["forecast"]["irr"]["p50"]
        if age >= flags_p["hockey_min_age"] and irr_f50 - h["marks"]["actual"]["irr"] > flags_p["hockey_gap"]:
            fl.append("hockey_stick")
        if theta < flags_p["stale_theta"]:
            fl.append("stale_nav")
        if "m" in signals and abs(signals["m"]["raw"] - signals["f"]["raw"]) > flags_p["market_disagreement"]:
            fl.append("market_disagreement")
        if age < phi_min_age:
            fl.append("young_actual_unused")
        if not fund and "u" not in signals:
            fl.append("underwriting_expired")
        tv = h["marks"]["actual"]["tvpi"]
        if tv is not None and age >= flags_p["zombie_age"] and tv < flags_p["zombie_tvpi"]:
            fl.append("zombie_nav")
        beliefs.append({
            "unit_id": u["id"], "group": g, "mu_hat": mu_loo, "mu_hat_with_own_bid": mu_full,
            "alpha_hat": mu_loo - u["beta_return"], "sigma_post": sd_post, "sigma_hat": sd_hat, "nu": nu,
            "p10": mu_loo + tq[0] * sd_hat, "p50": mu_loo, "p90": mu_loo + tq[2] * sd_hat,
            "prior": mu_k, "prior_sd": sd_k, "weights": w_loo, "weights_with_own_bid": w_full,
            "signals": signals, "bias_forecast_applied": b_f, "bias_underwritten_applied": b_u, "kappa_g": kappa,
            "credibility_Z": Z, "benktander_c": c_star, "flags": fl,
            "p_forecast_optimistic": float(norm.cdf((signals["f"]["raw"] - mu_loo) / sd_hat)),
        })
    return beliefs
