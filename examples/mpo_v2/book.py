"""Component 1a: the synthetic book SYN-ADIC-177 (SYNTHETIC - NOT ADIC DATA).

Holdings come from params.json (allocation v2: $177bn reported NAV across the eight groups plus Treasury). For each
book seed this module draws a SEALED truth (true forward alpha per holding, true group biases) and then generates
what ADIC would actually see from that truth:
  - the underwritten case (MOIC/IRR, down/base/up), set at inception with the group's underwriting optimism;
  - the actual since-inception net IRR and TVPI, partly persistent in true alpha;
  - the group's current forecast (since-inception net IRR and MOIC, P10/P50/P90), with forecast optimism that is
    stronger in a drought and stated ranges that are too narrow (they cover ~36-52% of outcomes);
  - an external secondary bid that is only partly informative about true alpha;
  - a quarterly forecast archive per group (scored past forecast errors) for the bias credibility of fusion.
The truth model deliberately differs from the belief model the fusion assumes (DSGO RV-02): dispersion multiplier,
bias shifted by +1 prior sd, a regime component, narrow ranges and attenuated bid information. The placebo book draws
true alpha independently of everything ADIC observes.
"""
from __future__ import annotations

import numpy as np

from common import GROUPS, Params


def _seg(P: Params, key: str) -> dict:
    return P.get(f"book.segments.{key}")


def build_units(P: Params, Ef: np.ndarray) -> list[dict]:
    """Expand the unit list with segment defaults. Ef = pooled mean annual factor returns (6,)."""
    units = []
    rf = P.get("rates.sofr")
    alpha_star = P.get("fusion.alpha_star_pp")
    for u in P.get("book.units"):
        s = dict(_seg(P, u["segment"]))
        s.update(u)
        s["B"] = list(map(float, s["B"]))
        b = np.asarray(s["B"])
        s["beta_return"] = float(rf + b @ Ef)
        s["alpha_star"] = alpha_star[s["group"]] / 100.0
        s["mu_prior"] = s["beta_return"] + s["alpha_star"]
        age_b = int(np.searchsorted(np.asarray(s["edges"], float), s["age"], side="right"))
        s["age_bucket"] = age_b
        s["theta0"] = float(s["theta_by_age"][age_b]) if "theta0" not in u else float(u["theta0"])
        s["nav_econ"] = s["nav"] * s["theta0"]
        s["H"] = float(max(s["min_remaining"], s["life"] - s["age"]))
        s["D"] = float(s["duration_share"] * s["H"])
        units.append(s)
    return units


def make_book(P: Params, units: list[dict], seed: int, variant: dict) -> dict:
    """Draw the sealed truth and the marks/bids for one synthetic book.
    variant: {"alpha_dispersion": x, "bid_info": y, "placebo": bool}."""
    rng = np.random.default_rng(seed)
    I = len(units)
    prior_sd = P.get("fusion.unit_prior_sd_pp")
    bu_prior = P.get("fusion.bias_prior_underwritten_pp")
    bf_prior = P.get("fusion.bias_prior_forecast_pp")
    b_sd = P.get("fusion.bias_prior_sd_pp")
    shift_sd = P.get("truth_model.bias_shift_sd")
    drought_extra = P.get("truth_model.drought_forecast_optimism_pp")
    kappa_true = P.get("truth_model.range_kappa_true")
    persist = P.get("truth_model.actual_persistence")
    fe_sd = P.get("truth_model.forecast_error_sd_pp")
    ue_sd = P.get("truth_model.underwriting_error_sd_pp")
    bid_sd = P.get("truth_model.bid_noise_sd")
    bid_pass = P.get("truth_model.bid_alpha_passthrough")
    arch_sd = P.get("truth_model.archive_error_sd_pp")
    n_eff = P.get("fusion.archive_n_eff")
    out_noise = P.get("fusion.outcome_noise")
    case_dn = P.get("truth_model.underwritten_case_down_pp")
    case_up = P.get("truth_model.underwritten_case_up_pp")
    bench_sd = P.get("truth_model.realized_benchmark_sd_pp")
    rho_bid = P.get("bids.rho")
    agemult = P.arr("bids.age_multiplier")
    disp = variant["alpha_dispersion"]
    info = variant["bid_info"]

    # true group biases: prior + shift_sd prior sds (+ drought component for forecasts)
    true_bu = {g: (bu_prior[g] + shift_sd * b_sd[g]) / 100 for g in GROUPS}
    true_bf = {g: (bf_prior[g] + shift_sd * b_sd[g] + drought_extra) / 100 for g in GROUPS}
    z = rng.standard_normal(I)
    alpha_true = np.array([u["alpha_star"] + disp * prior_sd[u["group"]] / 100 * z[i] for i, u in enumerate(units)])
    if variant.get("placebo"):
        z_obs = rng.standard_normal(I)     # what the marks and bids are generated from: independent of the truth
        alpha_obs = np.array([u["alpha_star"] + disp * prior_sd[u["group"]] / 100 * z_obs[i] for i, u in enumerate(units)])
    else:
        rng.standard_normal(I)             # keep the random stream aligned across variants
        alpha_obs = alpha_true
    eps = rng.standard_normal((I, 6))
    bench = rng.standard_normal(I)
    holdings = []
    for i, u in enumerate(units):
        g = u["group"]
        mu_obs = u["beta_return"] + alpha_obs[i]
        H, age = u["H"], u["age"]
        V = u["nav_econ"]
        N = u["nav"]
        liquid = u["tier"] == "liquid"
        nc = u["noise"]
        noise_f = fe_sd[nc] / 100
        # --- actual since-inception: benchmark realized + persistence x alpha + noise
        r_bench = u["beta_return"] + bench_sd / 100 * bench[i]
        r_act = r_bench + persist * alpha_obs[i] + out_noise[nc] / np.sqrt(max(age, 1.0)) * eps[i, 0] * 0.5
        hold = max(age * u["duration_share"], 0.5)
        tvpi = float(np.exp(r_act * hold))
        p_real = float(np.clip((age - u["realize_start"]) / u["realize_span"], 0.0, u["realize_max"]))
        paid_in = N / max((1 - p_real) * tvpi, 1e-6)
        dist_to_date = p_real * tvpi * paid_in
        # --- forecast: forward return with optimism, stated range too narrow
        rho_f = mu_obs + true_bf[g] + noise_f * eps[i, 1]
        sd_total = np.sqrt(noise_f ** 2 + (out_noise[nc] ** 2) / max(H, 1.0))
        sd_stated = sd_total / kappa_true
        R = lambda rho: V * np.exp(rho * H)  # remaining value on the economic nowcast basis
        if liquid:
            moic_f = {k: float(np.exp(v * H)) for k, v in
                      (("p10", rho_f - 1.2816 * sd_stated), ("p50", rho_f), ("p90", rho_f + 1.2816 * sd_stated))}
        else:
            moic_f = {k: float((dist_to_date + R(v)) / paid_in) for k, v in
                      (("p10", rho_f - 1.2816 * sd_stated), ("p50", rho_f), ("p90", rho_f + 1.2816 * sd_stated))}
        dur_tot = max((age + H) * u["duration_share"], 0.5)
        irr_f = {k: float(np.exp(np.log(max(m, 1e-6)) / dur_tot) - 1) for k, m in moic_f.items()}
        # --- underwritten at inception
        rho_u = u["beta_return"] + alpha_obs[i] + true_bu[g] + ue_sd / 100 * eps[i, 2]
        T_u = u["life"]
        dur_u = T_u * u["duration_share"]
        moic_u = {"down": float(np.exp((rho_u - case_dn / 100) * dur_u)), "base": float(np.exp(rho_u * dur_u)),
                  "up": float(np.exp((rho_u + case_up / 100) * dur_u))}
        irr_u = {k: float(np.exp(np.log(m) / dur_u) - 1) for k, m in moic_u.items()}
        # --- market bid (per $ of reported NAV) in today's class (DRT), partly informative; liquid units trade at NAV
        bid = None
        if u["bid_key"] is not None and not liquid:
            base = rho_bid[u["bid_key"]][1] * float(agemult[u["age_bucket"]] if u["age_mult"] else 1.0)
            bid = float(u["theta0"] * base * np.exp(info * bid_pass * (alpha_obs[i] - u["alpha_star"]) * min(u["D"], 4.0)
                                                    + bid_sd * eps[i, 3]))
        holdings.append({
            "unit_id": u["id"], "name": u["name"], "group": g, "segment": u["segment"], "vehicle": u["vehicle"],
            "control": u["control"], "tier": u["tier"], "kind": u["kind"],
            "nav_rep_bn": N, "nav_econ_bn": V, "theta": u["theta0"], "unfunded_bn": u["unfunded"], "age_y": age,
            "remaining_life_y": H, "duration_y": u["D"],
            "paid_in_bn": paid_in, "distributed_bn": dist_to_date,
            "marks": {
                "underwritten": {"moic": moic_u, "irr": irr_u, "life_y": T_u},
                "actual": {"irr": float(np.exp(r_act) - 1), "tvpi": tvpi if not liquid else None,
                           "irr_log": float(r_act), "bench_log": float(r_bench)},   # realized benchmark (PME basis)
                "forecast": {"moic": moic_f, "irr": irr_f, "as_of": "2026-09-30"},
            },
            "bid": ({"p_ce": bid, "source": "external" if u["bid_external"] else "segment", "node_class": "DRT"}
                    if bid is not None else None),
        })
    # --- quarterly forecast archive per group: scored past forecast errors (forecast minus realized, so a
    #     positive mean is optimism); the archive spans drought and normal quarters, so it carries half the
    #     drought optimism that today's forecasts carry (truth != belief, RV-02)
    archive = {}
    for g in GROUPS:
        n = int(n_eff[g])
        e_f = rng.normal(true_bf[g] - drought_extra / 100 * 0.5, arch_sd / 100, n)   # archive spans drought and normal
        e_u = rng.normal(true_bu[g], arch_sd / 100, n)
        cover = rng.random(n) < (2 * _phi(1.2816 / kappa_true) - 1)
        archive[g] = {"n_eff": n, "mean_forecast_error": float(e_f.mean()), "mean_underwriting_error": float(e_u.mean()),
                      "range_coverage": float(cover.mean())}
    opp_sr = rng.normal(P.get("truth_model.opp_sr_mean"), P.get("truth_model.opp_sr_sd"))
    truth = {"alpha_true": alpha_true.tolist(), "true_bias_underwritten": true_bu, "true_bias_forecast": true_bf,
             "opp_sharpe_true": float(opp_sr), "variant": variant, "seed": seed}
    return {"holdings": holdings, "archive": archive, "truth": truth}


def _phi(x):
    from scipy.stats import norm
    return float(norm.cdf(x))
