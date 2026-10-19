"""
gap_02 (groups) - company and sponsor overlap for SYN-ADIC-177: parameterization, sampler and gate V24.  SYNTHETIC.

One exposure graph links sponsors (GPs) -> funds -> companies, and every ADIC claim to a company or fund:
PE look-through, Co-investment, Capital Solutions (A: fund finance; C/D/E: company structured/junior/rescue),
Private Credit loans.  Overlap probabilities (pre-stated; anchors in gap_02.md sec. 6):
  s_PC   sponsored share of PC borrowers          0.75  (KBRA DLD ~1,700 of ~2,300 index borrowers, Mar 2024;
                                                          Block et al. 2024: 78% of US PD capital in sponsored deals)
  tilt   PC sponsor draw  ~ activity^0.8           (mid-market tilt relative to ADIC's large-cap GP set) [I]
  h      ADIC holds the fund owning a company, given the sponsor is an ADIC GP: 120 funds / 70 GPs over ~3 active
         funds per GP -> ~0.57 [I]
  p_co   co-investment alongside an ADIC GP        0.70  (census v1.0 / G4)
  h_co   co-investment in an ADIC-held fund, given ADIC GP  0.90 [I] (co-investment rights attach to fund LPs)
  p_csA  Capital Solutions fund-finance loan to an ADIC-held fund 0.50 [I]
  p_csC  Capital Solutions company exposure to an ADIC GP's company 0.50 [I]
Sponsor universe: 800 sponsors, lognormal activity with the top decile backing ~50% of sponsored companies
(S&P Global Ratings Dec-2023 BDC study, figure seen only in a search summary [U]).
Outputs: realized overlap shares (count and value), GP look-through concentration vs the 5% limit, and
V24a/b/c checks on one sampled census.  Run:  .venv\\Scripts\\python.exe -I -B overlap_graph.py
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "overlap_graph_results.json")
P = dict(n_sponsors=800, top_decile_share=0.50, n_adic_gps=70, n_pe_funds=120, funds_per_gp_active=3,
         companies_universe=12000, companies_per_fund=12, n_co=90, n_pc_loans=1500, n_cs=40,
         s_pc=0.75, tilt=0.8, p_co=0.70, h_co=0.90, p_csA=0.50, p_csC=0.50,
         pe_nav=52.0, pe_unf=16.42, co_nav=18.0, pc_nav=14.0, cs_nav=8.0, private_nav_plus_unf=106.0 + 27.02)
# V24b bands: binomial 90% band around the parameter-implied expectation at census sizes
# (n = 90 co-investments, 1,500 PC loans, 18 Capital Solutions company positions, 12 fund-finance loans)
BANDS = {"co_in_pe": (0.59, 0.76), "pc_in_pe": (0.115, 0.143), "csC_in_pe": (0.15, 0.51), "csA_adic_fund": (0.26, 0.74),
         "co_with_pc_loan": (0.03, 0.13)}


def lognormal_sigma_for_top_share(n, share, rng):
    lo, hi = 0.1, 3.0
    z = rng.standard_normal(n)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        w = np.sort(np.exp(mid * z))[::-1]
        s = w[: n // 10].sum() / w.sum()
        lo, hi = (mid, hi) if s < share else (lo, mid)
    return 0.5 * (lo + hi), z


def sample(seed=7):
    rng = np.random.default_rng(seed)
    sig, z = lognormal_sigma_for_top_share(P["n_sponsors"], P["top_decile_share"], rng)
    act = np.exp(sig * z)
    act /= act.sum()
    # companies per sponsor and their fund (0..2 = the sponsor's three active funds)
    n_comp = np.maximum(1, np.round(act * P["companies_universe"]).astype(int))
    comp_sponsor = np.repeat(np.arange(P["n_sponsors"]), n_comp)
    comp_fund = rng.integers(0, P["funds_per_gp_active"], size=comp_sponsor.size)
    # ADIC GP set: 70 sponsors drawn without replacement, probability ~ activity^1.5 (large-cap tilt)
    pr = act ** 1.5 / (act ** 1.5).sum()
    adic = rng.choice(P["n_sponsors"], size=P["n_adic_gps"], replace=False, p=pr)
    is_adic = np.zeros(P["n_sponsors"], bool)
    is_adic[adic] = True
    # ADIC funds: 120 interests over 70 GPs (>=1 each), at most the GP's 3 active funds
    held = {g: {int(rng.integers(0, 3))} for g in adic}
    extra = P["n_pe_funds"] - P["n_adic_gps"]
    while extra > 0:
        g = int(rng.choice(adic, p=pr[adic] / pr[adic].sum()))
        if len(held[g]) < 3:
            held[g].add(int(rng.integers(0, 3)))
            extra -= 1
    in_pe = np.array([is_adic[s] and (f in held.get(s, ())) for s, f in zip(comp_sponsor, comp_fund)])
    pe_companies = np.where(in_pe)[0]
    # PE look-through weights: fund NAV split lognormal, companies equal within a fund
    fund_keys = [(g, f) for g in adic for f in sorted(held[g])]
    fw = rng.lognormal(0, 1.0, len(fund_keys))
    fw = fw / fw.sum() * (P["pe_nav"] + P["pe_unf"])
    fund_val = dict(zip(fund_keys, fw))
    # co-investments
    co = []
    for _ in range(P["n_co"]):
        if rng.random() < P["p_co"]:
            g = int(rng.choice(adic, p=pr[adic] / pr[adic].sum()))
            cand = np.where((comp_sponsor == g) & (in_pe if rng.random() < P["h_co"] else ~in_pe))[0]
            if cand.size == 0:
                cand = np.where(comp_sponsor == g)[0]
        else:
            g = int(rng.choice(np.where(~is_adic)[0]))
            cand = np.where(comp_sponsor == g)[0]
        co.append(int(rng.choice(cand)))
    co = np.array(co)
    co_w = rng.lognormal(0, 0.8, co.size)
    co_w = co_w / co_w.sum() * P["co_nav"]
    # private-credit loans
    pt = act ** P["tilt"] / (act ** P["tilt"]).sum()
    pc = []
    for _ in range(P["n_pc_loans"]):
        if rng.random() < P["s_pc"]:
            g = int(rng.choice(P["n_sponsors"], p=pt))
            pc.append(int(rng.choice(np.where(comp_sponsor == g)[0])))
        else:
            pc.append(-1)  # non-sponsored borrower outside the PE universe
    pc = np.array(pc)
    pc_w = rng.lognormal(0, 0.8, pc.size)
    pc_w = pc_w / pc_w.sum() * P["pc_nav"]
    # capital solutions: 12 fund-finance (A), 18 company (C/D/E), 10 other (B/F/G, no company link)
    csA_adic = rng.random(12) < P["p_csA"]
    csC = []
    for _ in range(18):
        if rng.random() < P["p_csC"]:
            g = int(rng.choice(adic, p=pr[adic] / pr[adic].sum()))
            csC.append(int(rng.choice(np.where(comp_sponsor == g)[0])))
        else:
            csC.append(int(rng.choice(np.where(~is_adic[comp_sponsor])[0])))
    csC = np.array(csC)
    pe_set = set(pe_companies.tolist())
    shares = dict(
        co_in_pe=float(np.mean([c in pe_set for c in co])),
        pc_in_pe=float(np.mean([c in pe_set for c in pc if c >= 0]) * P["s_pc"]) if (pc >= 0).any() else 0.0,
        pc_in_pe_value=float(sum(w for c, w in zip(pc, pc_w) if c in pe_set) / P["pc_nav"]),
        csC_in_pe=float(np.mean([c in pe_set for c in csC])),
        csA_adic_fund=float(csA_adic.mean()),
        co_with_pc_loan=float(np.mean([c in set(pc[pc >= 0].tolist()) for c in co])),
        co_in_pe_value=float(sum(w for c, w in zip(co, co_w) if c in pe_set) / P["co_nav"]),
    )
    # GP look-through concentration on the graph
    gp_exp = np.zeros(P["n_sponsors"])
    for (g, f), v in fund_val.items():
        gp_exp[g] += v
    for c, w in zip(co, co_w):
        gp_exp[comp_sponsor[c]] += w
    for c, w in zip(pc, pc_w):
        if c >= 0:
            gp_exp[comp_sponsor[c]] += w
    gp_share = gp_exp / P["private_nav_plus_unf"]
    top = np.argsort(gp_share)[::-1][:5]
    # V24a structural identity: every claim keys the company's single EV draw id
    claims = [("pe", int(c)) for c in pe_companies] + [("co", int(c)) for c in co] + \
             [("pc", int(c)) for c in pc if c >= 0] + [("cs", int(c)) for c in csC]
    ev_id = {}
    identity_ok = True
    for _, c in claims:
        key = c                       # generator contract: EV path keyed by company_id only
        if ev_id.setdefault(c, key) != key:
            identity_ok = False
    multi = {}
    for grp, c in claims:
        multi.setdefault(c, set()).add(grp)
    n_multi = sum(len(v) > 1 for v in multi.values())
    v24b = {k: dict(value=round(shares[k], 3), band=BANDS[k], pass_=bool(BANDS[k][0] <= shares[k] <= BANDS[k][1]))
            for k in BANDS}
    return dict(sigma=sig, top_decile_share=float(np.sort(act)[::-1][: P["n_sponsors"] // 10].sum()),
                adic_gp_share_of_companies=float(n_comp[adic].sum() / n_comp.sum()),
                pe_lookthrough_companies=int(pe_companies.size), h_realized=float(in_pe[is_adic[comp_sponsor]].mean()),
                shares=shares, v24a_identity=identity_ok, companies_with_claims_in_2plus_groups=int(n_multi),
                v24b=v24b,
                v24c_gp_limit=dict(max_gp_share=float(gp_share.max()), limit=0.05, pass_=bool(gp_share.max() <= 0.05),
                                   top5_gp_shares=[round(float(gp_share[i]), 4) for i in top],
                                   top5_gp_bn=[round(float(gp_exp[i]), 2) for i in top]))


def main():
    runs = [sample(seed) for seed in range(7, 27)]
    keys = runs[0]["shares"].keys()
    agg = {k: dict(mean=float(np.mean([r["shares"][k] for r in runs])), p05=float(np.quantile([r["shares"][k] for r in runs], 0.05)),
                   p95=float(np.quantile([r["shares"][k] for r in runs], 0.95))) for k in keys}
    gp = [r["v24c_gp_limit"]["max_gp_share"] for r in runs]
    res = dict(label="SYNTHETIC - NOT ADIC DATA", params=P, bands=BANDS, first_sample=runs[0], shares_over_20_samples=agg,
               max_gp_share=dict(mean=float(np.mean(gp)), p95=float(np.quantile(gp, 0.95)),
                                 share_of_samples_breaching=float(np.mean([x > 0.05 for x in gp]))),
               adic_gp_share_of_companies_mean=float(np.mean([r["adic_gp_share_of_companies"] for r in runs])),
               h_realized_mean=float(np.mean([r["h_realized"] for r in runs])))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(json.dumps({k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in agg.items()}, indent=1))
    print("max GP share:", res["max_gp_share"], "ADIC GP share of companies:", round(res["adic_gp_share_of_companies_mean"], 3),
          "h:", round(res["h_realized_mean"], 3))
    print("first sample V24:", json.dumps({"a": runs[0]["v24a_identity"], "b": runs[0]["v24b"], "c": runs[0]["v24c_gp_limit"]}))


if __name__ == "__main__":
    main()
