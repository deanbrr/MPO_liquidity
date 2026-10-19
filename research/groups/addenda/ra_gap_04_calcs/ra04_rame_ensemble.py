"""
ra_gap_04 - RAME misspecification ensemble for one segment.   ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.

For each variant (ra04_rame_lib.VARIANTS) and W worlds (T = 80 quarters, common seeds across variants):
  * production RAME fits by MLE (G13 model): ALT (appraisal + listed + tau), AL (no tau), ALT4 (yearly tau);
  * the variant-aware oracle filter on the same observation set;
  * canonical metrics: excess CRPS vs oracle, 80% band coverage, SELL bias and regret for the rule
    SELL iff bid >= 0.861 x theta_hat (theta = exp(v - a)), R2 ratio (nowcast RMSE / appraisal RMSE), and the
    annual-return error of the nowcast index (feeds the forecast-engine ensemble's common-shock control);
  * G-D detection tests on the production fit: lagged-tau likelihood test, tau-innovation AR(1) test and a
    regime test on tau innovations (false positives under M0);
  * on M0 worlds: G0 experiment (imposed starting gap 0 / 2 / 5 / 8%) and the bid channel;
  * on TW worlds: bid channel again (does the bid rescue a bad tau?);
  * SBC for G-A: data drawn from the filter's own state-space model with parameters from a prior.
Run:  .venv\\Scripts\\python.exe -I -B ra04_rame_ensemble.py <SEGMENT> [W] [N_SBC]  -> rame_ens_<SEGMENT>.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from numpy.random import SeedSequence, default_rng

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ra04_rame_lib as L  # noqa: E402

SEG = sys.argv[1]
LAYER = sys.argv[2]                       # "ss" (canonical, RAME's own model + oracle) or "g13" (G13 world)
W = int(sys.argv[3]) if len(sys.argv) > 3 else 100
N_SBC = int(sys.argv[4]) if len(sys.argv) > 4 else 300
SUBSET = sys.argv[5].split(",") if len(sys.argv) > 5 else None      # optional variant subset (+ "SBC")
PART = sys.argv[6] if len(sys.argv) > 6 else ""
T = 80
SEED = 20261019
SEG_IDX = {"CORE_RE": 0, "VA_RE": 1, "CORE_INFRA": 2, "VA_INFRA": 3, "ENERGY": 4}[SEG]
S = L.g.SEGMENTS[SEG]
LAG = S["lag"]
MAIN_OUT = HERE / f"rame_ens_{LAYER}_{SEG}.json"
OUT = HERE / f"rame_ens_{LAYER}_{SEG}{('_' + PART) if PART else ''}.json"
DET_VARIANTS = ("M0", "TL1", "TL2", "TA3", "TA5", "TBC", "TW")
G0S = (0.0, 0.02, 0.05, 0.08)
G13_VARIANTS = ("M0", "TL1", "TL2", "TA3", "TA5", "TB", "TBC", "TW", "MALL", "MALL_T")


def filt(system):
    ll, vpre, Ppre, vpost, Ppost, inn, innv = L.run_filter(system)
    return dict(ll=ll, vpre=vpre, Ppre=Ppre, vpost=vpost, Ppost=Ppost, inn=inn, innv=innv)


def ar1_t(u):
    u = u[~np.isnan(u)]
    if u.size < 10:
        return 0.0
    x, y = u[:-1], u[1:]
    x = x - x.mean()
    y = y - y.mean()
    b = (x * y).sum() / (x * x).sum()
    r = y - b * x
    se = math.sqrt((r * r).sum() / (len(y) - 2) / (x * x).sum())
    return b / se


def regime_t(u, z):
    ok = ~np.isnan(u)
    u, z = u[ok], z[ok]
    a, b = u[z == 1], u[z == 0]
    if a.size < 3 or b.size < 3:
        return 0.0
    return (a.mean() - b.mean()) / math.sqrt(a.var(ddof=1) / a.size + b.var(ddof=1) / b.size)


def bid_metrics(d, v_hat, burn=12):
    sl = np.arange(burn, len(d["vbar"]))
    sl = sl[d["bid_seen"][sl]]
    v, a = d["vbar"][sl], d["a"][sl]
    th, thh = np.exp(v - a), np.exp(v_hat[sl] - a)
    q = np.exp(d["lnq"][sl])
    st, sh = q >= L.H_SELL * th, q >= L.H_SELL * thh
    reg = np.abs(q - L.H_SELL * th) * (st != sh)
    dn = d["z"][sl] == 1
    return dict(n=int(sl.size), sse_th=float(((thh - th) ** 2).sum()), n_sell=int(st.sum()),
                sell_bias=float((thh - th)[st].sum()), regret=float(reg.sum()), dec_err=int((st != sh).sum()),
                n_dn=int(dn.sum()), regret_dn=float(reg[dn].sum()), sell_hat_dn=int(sh[dn].sum()),
                sell_true_dn=int(st[dn].sum()), th_bias=float((thh - th).sum()), th_bias_dn=float((thh - th)[dn].sum()))


def bid_summary(rows):
    t = {}
    for r in rows:
        for k, v in r.items():
            t[k] = t.get(k, 0) + v
    n = max(t["n"], 1)
    nd = max(t["n_dn"], 1)
    return dict(theta_rmse_pp=100 * math.sqrt(t["sse_th"] / n), theta_bias_pp=100 * t["th_bias"] / n,
                theta_bias_down_pp=100 * t["th_bias_dn"] / nd, sell_bias_pp=100 * t["sell_bias"] / max(t["n_sell"], 1),
                regret_pp=100 * t["regret"] / n, regret_down_pp=100 * t["regret_dn"] / nd,
                dec_err_rate=t["dec_err"] / n, sell_rate_down_hat=t["sell_hat_dn"] / nd,
                sell_rate_down_true=t["sell_true_dn"] / nd, n=n, n_down=t["n_dn"])


def sbc(n_rep, P):
    """Simulation-based calibration of the production filter: parameters drawn from a prior centred on the
    segment's true index-level values P, truth and data drawn from the filter's own state-space model."""
    ss = SeedSequence([SEED, SEG_IDX, 777]).spawn(n_rep)
    pits, cov = [], []
    lam_c, mu_c, sv_c, sxi_c, _, phip_c, sp_c, sL_c, st_c, _ = P
    for cs in ss:
        rng = default_rng(cs)
        lam = float(np.clip(lam_c + rng.uniform(-0.05, 0.05), 0.3, 0.95))
        mu = rng.normal(mu_c, 0.002)
        sv = math.exp(rng.normal(math.log(sv_c), 0.2))
        sxi = math.exp(rng.normal(math.log(sxi_c), 0.3))
        beta = rng.normal(1.0, 0.1)
        phip = float(np.clip(rng.uniform(phip_c - 0.05, phip_c + 0.05), 0.5, 0.97))
        sp = math.exp(rng.normal(math.log(sp_c), 0.2))
        sL = math.exp(rng.normal(math.log(sL_c), 0.2))
        st = math.exp(rng.normal(math.log(st_c), 0.2))
        cL = rng.normal(0.0, 0.05)
        n = T + 1
        v = np.empty(n); p = np.empty(n); s = np.empty(n); e = np.empty(n)
        v[0] = 0.0
        p[0] = sp / math.sqrt(1 - phip ** 2) * rng.standard_normal()
        e[0] = sxi / math.sqrt(1 - L.g.PHI_E ** 2) * rng.standard_normal()
        s[0] = 0.0
        for t in range(1, n):
            v[t] = mu + v[t - 1] + sv * rng.standard_normal()
            p[t] = phip * p[t - 1] + sp * rng.standard_normal()
            s[t] = lam * s[t - 1] + (1 - lam) * v[max(t - LAG, 0)]
            e[t] = L.g.PHI_E * e[t - 1] + sxi * rng.standard_normal()
        a = s + e
        Lr = cL + beta * v + p + sL * rng.standard_normal(n)
        tau = v + st * rng.standard_normal(n)
        f = L.fit_prod(a, Lr, tau, LAG)
        dd = dict(vbar=v, a=a, L=Lr, tau=tau, lnq=np.zeros(n), bid_seen=np.zeros(n, dtype=bool))
        o = filt(L.prod_system(dd, f, LAG))
        for t in (40, T):
            zt = (v[t] - o["vpost"][t]) / math.sqrt(o["Ppost"][t])
            pits.append(0.5 * (1 + math.erf(zt / math.sqrt(2))))
            cov.append(abs(zt) <= L.Z80)
    pits = np.array(pits)
    from scipy import stats
    hist = np.histogram(pits, bins=10, range=(0, 1))[0]
    chi2 = float(((hist - len(pits) / 10) ** 2 / (len(pits) / 10)).sum())
    return dict(n_rep=n_rep, n_pit=int(pits.size), cov80=float(np.mean(cov)),
                ks_p=float(stats.kstest(pits, "uniform").pvalue), chi2_10bins=chi2,
                chi2_p=float(1 - stats.chi2.cdf(chi2, 9)), pit_hist=hist.tolist(),
                pit_tail_share=float(np.mean((pits < 0.05) | (pits > 0.95))))


def main():
    t0 = time.time()
    res = dict(label=L.SYN, segment=SEG, layer=LAYER, W=W, T=T, seed=SEED, segment_defaults=S)
    ss = LAYER == "ss"
    # true index-level parameters of RAME's own model implied by the G13 calibration (canonical layer)
    P = L.ss_params(SEG)
    res["ss_true_params"] = dict(zip(["lam", "mu", "sv", "sxi", "beta", "phip", "sp", "sL", "st", "cL"],
                                     [float(x) for x in P]))
    print(SEG, LAYER, "true SS params", res["ss_true_params"], flush=True)
    children = SeedSequence([SEED, SEG_IDX, 1 if ss else 2]).spawn(W)
    res["variants"] = {}
    done_elsewhere = set()
    for src in {MAIN_OUT, OUT}:            # resume: keep finished variants (same seeds, same worlds)
        if src.exists():
            prev = json.loads(src.read_text(encoding="utf-8"))
            if prev.get("W") == W and prev.get("layer") == LAYER:
                if src == OUT:
                    res["variants"] = prev.get("variants", {})
                done_elsewhere |= set(prev.get("variants", {}))
    print("resuming; done:", sorted(done_elsewhere), flush=True)
    vlist = list(L.VARIANTS) if ss else list(G13_VARIANTS)
    if SUBSET:
        vlist = [v for v in vlist if v in SUBSET]
    for vname in vlist:
        if vname in res["variants"] or vname in done_elsewhere:
            continue
        var = L.VARIANTS[vname]
        tv = time.time()
        rows = {k: [] for k in ("ALT", "AL", "ALT4", "OR_ALT", "OR_AL", "OR_ALT4")}
        lam_hat, det = [], dict(lag=[], ar=[], reg=[])
        g0rows = {gv: dict(ALT=[], AL=[]) for gv in G0S}
        bids = {k: [] for k in ("B0_noBid", "B1_IN_assumedPrem", "B2_LOO_assumedPrem", "B3_LOO_truePrem")}
        for wi in range(W):
            rng = default_rng(children[wi])
            d = L.sim_ss_world(rng, T, SEG, var, P) if ss else L.sim_world(rng, T, SEG, var)
            fits = {"ALT": L.fit_prod(d["a"], d["L"], d["tau"], LAG),
                    "AL": L.fit_prod(d["a"], d["L"], d["tau"], LAG, use_tau=False),
                    "ALT4": L.fit_prod(d["a"], d["L"], d["tau"], LAG, tau_every=4)}
            lam_hat.append(fits["ALT"]["params"][0])
            outs = {}
            for k, f in fits.items():
                o = filt(L.prod_system(d, f, LAG, tau_every=f["tau_every"]))
                outs[k] = o
                rows[k].append(L.nowcast_metrics(d, o["vpost"], o["Ppost"]))
                if ss:
                    oo = filt(L.oracle_system(d, SEG, var, P, use_tau=f["use_tau"], use_L=f["use_L"],
                                              tau_every=f["tau_every"]))
                    rows["OR_" + k].append(L.nowcast_metrics(d, oo["vpost"], oo["Ppost"]))
            if ss and vname in DET_VARIANTS:
                f1 = L.fit_prod(d["a"], d["L"], d["tau"], LAG, tau_lag=1)
                det["lag"].append(fits["ALT"]["nll"] - f1["nll"] > 1.92)
                u = outs["ALT"]["inn"] / np.sqrt(outs["ALT"]["innv"])
                det["ar"].append(ar1_t(u[12:]) > 1.645)
                det["reg"].append(abs(regime_t(u[12:], d["z"][12:])) > 1.96)
            if (not ss) and vname == "M0":
                for gv in G0S:
                    Ssh = 2 * gv / (1 + S["lam_agg"])
                    d2 = L.shock_last(d, SEG, Ssh) if gv > 0 else d
                    Tn = len(d2["a"]) - 1
                    Gtrue = d2["a"][Tn] - d2["vbar"][Tn]
                    for k in ("ALT", "AL"):
                        o = filt(L.prod_system(d2, fits[k], LAG))
                        Ghat = d2["a"][Tn] - o["vpost"][Tn]
                        sd = math.sqrt(o["Ppost"][Tn])
                        g0rows[gv][k].append((Gtrue, Ghat, abs(Ghat - Gtrue) <= L.Z80 * sd))
            if (not ss) and vname in ("M0", "TW"):
                f = fits["ALT"]
                o0 = outs["ALT"]
                o1 = filt(L.prod_system(d, f, LAG, use_bid=True, bid_prem=L.PREM_N))
                sys3 = L.prod_system(d, f, LAG, use_bid=True, bid_prem=L.PREM_N)
                sys3["dt"][:, 3] = -L.D_BID * d["prem"]
                o3 = filt(sys3)
                bids["B0_noBid"].append(bid_metrics(d, o0["vpost"]))
                bids["B1_IN_assumedPrem"].append(bid_metrics(d, o1["vpost"]))
                bids["B2_LOO_assumedPrem"].append(bid_metrics(d, o1["vpre"]))
                bids["B3_LOO_truePrem"].append(bid_metrics(d, o3["vpre"]))
        vr = {k: L.summarize(v) for k, v in rows.items() if v}
        if ss:
            for k in ("ALT", "AL", "ALT4"):
                p, o = vr[k], vr["OR_" + k]
                p["crps_excess_vs_oracle"] = p["crps_pp"] / o["crps_pp"] - 1
                p["regret_excess_vs_oracle"] = (p["regret_pp"] / o["regret_pp"] - 1 if o["regret_pp"] > 0
                                                else float("nan"))
        vr["lam_hat_mean"] = float(np.mean(lam_hat))
        vr["lam_hat_sd"] = float(np.std(lam_hat))
        if det["lag"]:
            vr["detection"] = {k: float(np.mean(v)) for k, v in det.items()}
        if (not ss) and vname == "M0":
            g0 = {}
            for gv, dd in g0rows.items():
                g0[str(gv)] = {}
                for k, lst in dd.items():
                    arr = np.array([(a, b) for a, b, _ in lst])
                    g0[str(gv)][k] = dict(G_true_mean_pp=100 * float(arr[:, 0].mean()),
                                          G_hat_mean_pp=100 * float(arr[:, 1].mean()),
                                          err_mean_pp=100 * float((arr[:, 1] - arr[:, 0]).mean()),
                                          err_rmse_pp=100 * float(np.sqrt(((arr[:, 1] - arr[:, 0]) ** 2).mean())),
                                          cov80_at_T=float(np.mean([c for _, _, c in lst])))
            vr["G0"] = g0
        if bids["B0_noBid"]:
            vr["bids"] = {k: bid_summary(v) for k, v in bids.items() if v}
            ob = vr["bids"]["B3_LOO_truePrem"]["regret_pp"]
            for k, v in vr["bids"].items():
                v["regret_vs_B3_truePrem"] = v["regret_pp"] / ob - 1 if ob > 0 else float("nan")
        res["variants"][vname] = vr
        a = vr["ALT"]
        xs = (f"xsCRPS {a['crps_excess_vs_oracle']:+.1%} xsReg {a['regret_excess_vs_oracle']:+.1%} "
              if ss else "")
        print(f"{SEG} {LAYER} {vname:6s} ALT: R2 {a['r2_ratio']:.2f} {xs}cov {a['cov80']:.3f} "
              f"sellbias {a['sell_bias_pp']:+.2f} reg {a['regret_pp']:.3f} | AL R2 {vr['AL']['r2_ratio']:.2f} "
              f"cov {vr['AL']['cov80']:.2f} | ALT4 R2 {vr['ALT4']['r2_ratio']:.2f} | lam {vr['lam_hat_mean']:.3f} "
              f"| {time.time() - tv:.0f}s", flush=True)
        OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    if ss and (SUBSET is None or "SBC" in SUBSET):
        res["sbc"] = sbc(N_SBC, P)
        print(SEG, "SBC", res["sbc"], flush=True)
    res["seconds"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    print("wrote", OUT, res["seconds"], "s", L.SYN)


if __name__ == "__main__":
    main()
