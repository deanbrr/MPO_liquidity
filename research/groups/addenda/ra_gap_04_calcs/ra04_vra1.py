"""
ra_gap_04 - V-RA1 on Cannon & Cole's capital-gain-adjusted basis, and the VA_RE recalibration.
ALL SIMULATED OUTPUTS SYNTHETIC - NOT ADIC DATA. Targets are PUBLISHED statistics (Cannon & Cole 2011, MPRA 32589).

Statistic (Cannon & Cole eq. 4): (P_t - A_{t-2}) / A_{t-2}, where A is the appraisal two quarters before sale.
  unadjusted: P_t = sale price;
  adjusted  : P_t rolled back by the APPRAISAL-BASED index appreciation between appraisal and sale (their eq. 1-3
              use the property-type value-weighted NPI capital appreciation, i.e. appraisal-based market values).
Sales process (as G13): discretionary sales with prob h0 exp(alpha (v - a)), plus forced sales in the down regime;
price = exp(v + bid noise).
Published targets, equal-weighted, NPI 1984-2010 (Cannon & Cole Tables 2A, 4A, 4B, 8):
  adjusted mean absolute 12.5% (median 8.1%), signed mean +3.9%; 2008 -11.0%; boom years 2004/05/06 +10.0/+10.6/
  +11.6% (maximum); unadjusted MAE 13.2%, signed +4.9%, 2008 -12.0%, maximum +14.7% (2005).
  Property-level absolute-error increments (Table 8, panel B): levered +1.0pp (t 2.97), office +1.5pp (t 3.98),
  closed-end fund 0.0pp (t 0.04), external or internal appraisal -2.2pp / -2.0pp vs none.
Gates (pre-registered here):
  CORE_RE, adjusted: MAE 10-14%; crash-quarter signed <= -8%; boom-quarter signed in [+5%, +11.6%].
  VA_RE, adjusted : MAE 12.5-16.5% (NPI mean; NPI mean + levered + office + no-appraisal increments 4.7pp, capped at
                    the worst NPI year, 2006: 16.5%); crash <= -8%; boom in [+5%, +14.1%] (CORE ceiling + 2.5pp).
VA_RE recalibration rule: keep the economic parameters (sig_i, sig_x, lam_agg) that drive true risk and RAME; search
the observation-noise parameters sig_e in {0.03..0.07} and lam_idio in {0.25, 0.35, 0.45}; choose the passing pair
closest to the MAE band midpoint (14.5%), tie-break by the smallest change from the G13 defaults.
Run:  .venv\\Scripts\\python.exe -I -B ra04_vra1.py  -> ra04_vra1_results.json
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import numpy as np
from numpy.random import SeedSequence, default_rng

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "G13_calcs"))
import g13_ra_marks_sim as g  # noqa: E402

SYN = "SYNTHETIC - NOT ADIC DATA"
OUT = HERE / "ra04_vra1_results.json"
W, T, NA = 100, 80, 60
SEED = 20261018 + 23            # G13's V-RA1 seed


def run(seg, params=None, h0=0.02, alpha_sel=1.0, sig_bid=0.04, forced_down=0.02, seed=SEED, variant="M0"):
    saved = copy.deepcopy(g.SEGMENTS[seg])
    if params:
        g.SEGMENTS[seg].update(params)
    try:
        ss = SeedSequence(seed)
        acc = {k: [] for k in ("u", "a", "u_abs", "a_abs", "crash_u", "crash_a", "boom_u", "boom_a",
                               "crash_obs", "boom_obs")}
        for cs in ss.spawn(W):
            rng = default_rng(cs)
            Fz = g.sim_factors(rng, T)
            d = g.sim_segment(rng, T, seg, Fz, NA, variant=variant)
            v, a, ai = d["v_asset"], d["a_asset"], d["a_index"]
            for t in range(10, T + 1):
                pr = np.minimum(0.5, h0 * np.exp(alpha_sel * (v[:, t] - a[:, t])) + (forced_down if d["z"][t] == 1 else 0.0))
                sold = rng.random(NA) < pr
                if not sold.any():
                    continue
                P = np.exp(v[sold, t] + sig_bid * rng.standard_normal(sold.sum()))
                A2 = np.exp(a[sold, t - 2])
                du = P / A2 - 1
                Padj = P / np.exp(ai[t] - ai[t - 2])                      # roll back by appraisal-index appreciation
                da = Padj / A2 - 1
                acc["u"].extend(du); acc["a"].extend(da)
                chg = d["vbar"][t] - d["vbar"][t - 4]
                if chg < -0.08:
                    acc["crash_u"].extend(du); acc["crash_a"].extend(da)
                if chg > 0.08:
                    acc["boom_u"].extend(du); acc["boom_a"].extend(da)
                # Cannon-Cole-consistent classification on the OBSERVABLE appraisal index (NPI-type):
                # boom years 2004-06 had NPI appreciation of +6.5% to +12.1% a year; 2008 had -11.3%.
                chg_obs = ai[t] - ai[t - 4]
                if chg_obs < -0.113:
                    acc["crash_obs"].extend(da)
                if chg_obs > 0.065:
                    acc["boom_obs"].extend(da)
        f = lambda x: float(np.mean(x)) if len(x) else None
        out = dict(n_sales=len(acc["u"]),
                   unadjusted=dict(mae=f(np.abs(acc["u"])), median_abs=float(np.median(np.abs(acc["u"]))),
                                   signed=f(acc["u"]), crash=f(acc["crash_u"]), boom=f(acc["boom_u"])),
                   adjusted=dict(mae=f(np.abs(acc["a"])), median_abs=float(np.median(np.abs(acc["a"]))),
                                 signed=f(acc["a"]), crash=f(acc["crash_a"]), boom=f(acc["boom_a"]),
                                 crash_obs=f(acc["crash_obs"]), boom_obs=f(acc["boom_obs"])),
                   n_crash=len(acc["crash_a"]), n_boom=len(acc["boom_a"]),
                   n_crash_obs=len(acc["crash_obs"]), n_boom_obs=len(acc["boom_obs"]))
    finally:
        g.SEGMENTS[seg] = saved
    return out


N_SEEDS = 5


def multi(seg, params=None, **kw):
    """Average the adjusted statistics over N_SEEDS independent seeds; report seed sd."""
    runs = [run(seg, params, seed=SEED + 1000 * k, **kw) for k in range(N_SEEDS)]
    keys = runs[0]["adjusted"].keys()
    mean = {k: float(np.mean([r["adjusted"][k] for r in runs])) for k in keys}
    sd = {k: float(np.std([r["adjusted"][k] for r in runs], ddof=1)) for k in keys}
    un = {k: float(np.mean([r["unadjusted"][k] for r in runs])) for k in runs[0]["unadjusted"]}
    return dict(adjusted=mean, adjusted_seed_sd=sd, unadjusted=un, first_seed=runs[0],
                n_crash_obs=int(np.mean([r["n_crash_obs"] for r in runs])),
                n_boom_obs=int(np.mean([r["n_boom_obs"] for r in runs])))


def gate_core(x):
    return dict(mae=0.10 <= x["mae"] <= 0.14, crash_obs=x["crash_obs"] <= -0.08,
                boom_obs=0.05 <= x["boom_obs"] <= 0.116)


def gate_va(x):
    return dict(mae=0.125 <= x["mae"] <= 0.165, crash_obs=x["crash_obs"] <= -0.08,
                boom_obs=0.05 <= x["boom_obs"] <= 0.141)


def main():
    res = dict(label=SYN, worlds=W, T=T, n_assets=NA, n_seeds=N_SEEDS,
               targets="Cannon & Cole (2011) Tables 2A/4A/4B/8, adjusted basis; boom/crash classified on the "
                       "appraisal index (NPI-type) as in the paper; true-index classification kept for continuity")
    base = {}
    for seg in ("CORE_RE", "VA_RE", "CORE_INFRA"):
        base[seg] = multi(seg)
        print(seg, "unadj", {k: round(v, 4) for k, v in base[seg]["unadjusted"].items()},
              "adj", {k: round(v, 4) for k, v in base[seg]["adjusted"].items()},
              "sd", {k: round(v, 4) for k, v in base[seg]["adjusted_seed_sd"].items()}, flush=True)
    res["g13_defaults"] = base
    res["gate_core_re"] = {k: bool(v) for k, v in gate_core(base["CORE_RE"]["adjusted"]).items()}
    res["gate_va_re_at_g13_defaults"] = {k: bool(v) for k, v in gate_va(base["VA_RE"]["adjusted"]).items()}
    grid = []
    for se in (0.03, 0.04, 0.05, 0.06, 0.07):
        for li in (0.25, 0.35, 0.45):
            r = multi("VA_RE", dict(sig_e=se, lam_idio=li))
            gv = gate_va(r["adjusted"])
            grid.append(dict(sig_e=se, lam_idio=li, adjusted=r["adjusted"], passes=bool(all(gv.values())),
                             gates={k: bool(v) for k, v in gv.items()}))
            x = r["adjusted"]
            print(f"  VA_RE sig_e {se:.2f} lam_idio {li:.2f}: MAE {x['mae']:.3f} crash_obs {x['crash_obs']:+.3f} "
                  f"boom_obs {x['boom_obs']:+.3f} (true-index crash {x['crash']:+.3f} boom {x['boom']:+.3f}) "
                  f"pass {all(gv.values())}", flush=True)
    res["va_re_grid"] = grid
    ok = [x for x in grid if x["passes"]]
    res["va_re_recalibrated"] = (min(ok, key=lambda x: (round(abs(x["adjusted"]["mae"] - 0.145), 3),
                                                        abs(x["sig_e"] - 0.07) + abs(x["lam_idio"] - 0.35)))
                                 if ok else None)
    res["core_re_alpha_sensitivity"] = {str(al): multi("CORE_RE", alpha_sel=al)["adjusted"] for al in (0.0, 0.5, 1.0)}
    # Recalibration candidate for the cycle statistics: downturn-dependent smoothing (G13 M_regime: lambda + 0.10
    # in the down regime), tested against the published values with their standard errors (Table 2A: 2006 boom
    # +11.6% s.e. 0.8%; 2008 crash -11.0% s.e. 1.1%); consistency = within 2 s.e.
    cc = dict(boom=(0.116, 0.008), crash=(-0.110, 0.011))
    res["cycle_consistency"] = {}
    for seg in ("CORE_RE", "VA_RE"):
        for var in ("M0", "M_regime"):
            r = multi(seg, variant=var)
            x = r["adjusted"]
            res["cycle_consistency"][f"{seg}|{var}"] = dict(
                mae=x["mae"], crash=x["crash"], boom=x["boom"], crash_obs=x["crash_obs"], boom_obs=x["boom_obs"],
                crash_z=(x["crash"] - cc["crash"][0]) / cc["crash"][1], boom_z=(x["boom"] - cc["boom"][0]) / cc["boom"][1],
                consistent=bool(abs((x["crash"] - cc["crash"][0]) / cc["crash"][1]) <= 2
                                and abs((x["boom"] - cc["boom"][0]) / cc["boom"][1]) <= 2))
            print(f"  cycle {seg} {var}: MAE {x['mae']:.3f} crash {x['crash']:+.3f} (z {res['cycle_consistency'][f'{seg}|{var}']['crash_z']:+.1f}) "
                  f"boom {x['boom']:+.3f} (z {res['cycle_consistency'][f'{seg}|{var}']['boom_z']:+.1f})", flush=True)
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("CORE gates", res["gate_core_re"], "| VA gates at defaults", res["gate_va_re_at_g13_defaults"])
    print("pick:", res["va_re_recalibrated"] and {k: res["va_re_recalibrated"][k] for k in ("sig_e", "lam_idio")})
    print("wrote", OUT, SYN)


if __name__ == "__main__":
    main()
