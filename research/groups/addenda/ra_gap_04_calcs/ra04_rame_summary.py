"""
ra_gap_04 - aggregate the RAME ensemble (rame_ens_{ss,g13}_<SEG>.json) and apply the canonical gates.
ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.
Gates on the production filter (ALT = appraisal + listed + transaction index), per segment:
  G-A (M0): SBC (KS p >= 0.05 and SBC 80% coverage 0.75-0.85); coverage 0.75-0.85; excess CRPS <= 15%;
            plus the G-B SELL-bias and regret limits.
  G-B (each of M1..M6, M5s, and the pre-registered tau axes): excess CRPS <= 15%; coverage 0.72-0.88;
            |SELL bias| <= 1.5pp of reported NAV; excess regret <= 35%.
  G-C (MALL, MALL_T): <= 25%; >= 0.70; <= 2.0pp; <= 50%.
  G-D: detection power >= 0.70 (lag test on TL1/TL2, tau-innovation AR test on TA3/TA5, regime test on TBC);
       false positives under M0 <= 0.05.
  R2 : nowcast RMSE <= 50% of the appraisal RMSE (both layers).
Run:  .venv\\Scripts\\python.exe -I -B ra04_rame_summary.py -> ra04_rame_summary.json
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_rame_summary.json"
SEGS = ["CORE_RE", "VA_RE", "CORE_INFRA", "VA_INFRA", "ENERGY"]
GB = ("M1", "M2", "M3", "M4", "M5", "M5s", "M6", "TL1", "TL2", "TA3", "TA5", "TB", "TBC", "TW")
GC = ("MALL", "MALL_T")


def gate(v, x):
    if v in GC:
        ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.25, cov=x["cov80"] >= 0.70,
                  sell_bias=abs(x["sell_bias_pp"]) <= 2.0, regret=x["regret_excess_vs_oracle"] <= 0.50)
    elif v == "M0":
        ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.15, cov=0.75 <= x["cov80"] <= 0.85,
                  sell_bias=abs(x["sell_bias_pp"]) <= 1.5, regret=x["regret_excess_vs_oracle"] <= 0.35)
    else:
        ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.15, cov=0.72 <= x["cov80"] <= 0.88,
                  sell_bias=abs(x["sell_bias_pp"]) <= 1.5, regret=x["regret_excess_vs_oracle"] <= 0.35)
    ok = {k: bool(val) for k, val in ok.items()}
    ok["all"] = all(ok.values())
    return ok


def main():
    out = dict(label="SYNTHETIC - NOT ADIC DATA", ss={}, g13={})
    for layer in ("ss", "g13"):
        for seg in SEGS:
            files = sorted(glob.glob(str(HERE / f"rame_ens_{layer}_{seg}.json"))) + \
                sorted(glob.glob(str(HERE / f"rame_ens_{layer}_{seg}_p*.json")))
            if not files:
                continue
            r = None
            for fpath in files:                          # merge the main file and the variant-subset part files
                x = json.loads(Path(fpath).read_text(encoding="utf-8"))
                if r is None:
                    r = x
                    r["variants"] = dict(x.get("variants", {}))
                else:
                    r["variants"].update(x.get("variants", {}))
                    if "sbc" in x:
                        r["sbc"] = x["sbc"]
            segout = dict(W=r["W"], variants={})
            for v, x in r["variants"].items():
                row = {k: x[k] for k in ("ALT", "AL", "ALT4") if k in x}
                keep = {}
                for k, m in row.items():
                    keep[k] = {kk: m[kk] for kk in ("r2_ratio", "cov80", "sell_bias_pp", "regret_pp", "rmse_pp",
                                                    "rmse_appr_pp", "e4_slope", "e4_rmse_pp", "down_level_bias_pp")
                               if kk in m}
                    for kk in ("crps_excess_vs_oracle", "regret_excess_vs_oracle"):
                        if kk in m:
                            keep[k][kk] = m[kk]
                if layer == "ss":
                    keep["gate_ALT"] = gate(v, row["ALT"])
                    keep["gate_AL"] = gate(v, row["AL"])
                keep["R2_pass_ALT"] = bool(row["ALT"]["r2_ratio"] <= 0.50)
                keep["R2_pass_ALT4"] = bool(row["ALT4"]["r2_ratio"] <= 0.50)
                keep["lam_hat_mean"] = x.get("lam_hat_mean")
                if "detection" in x:
                    keep["detection"] = x["detection"]
                if "G0" in x:
                    keep["G0"] = x["G0"]
                if "bids" in x:
                    keep["bids"] = x["bids"]
                segout["variants"][v] = keep
            if "sbc" in r:
                s = r["sbc"]
                segout["sbc"] = s
                segout["sbc_pass"] = bool(s["ks_p"] >= 0.05 and 0.75 <= s["cov80"] <= 0.85)
            out[layer][seg] = segout
    # cross-segment tallies
    tall = {}
    for v in ["M0", *GB, *GC]:
        res = [out["ss"][s]["variants"][v]["gate_ALT"]["all"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        r2s = [out["ss"][s]["variants"][v]["ALT"]["r2_ratio"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        r2g = [out["g13"][s]["variants"][v]["ALT"]["r2_ratio"] for s in out["g13"] if v in out["g13"][s]["variants"]]
        xs = [out["ss"][s]["variants"][v]["ALT"]["crps_excess_vs_oracle"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        cv = [out["ss"][s]["variants"][v]["ALT"]["cov80"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        sb = [out["ss"][s]["variants"][v]["ALT"]["sell_bias_pp"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        rg = [out["ss"][s]["variants"][v]["ALT"]["regret_excess_vs_oracle"] for s in out["ss"] if v in out["ss"][s]["variants"]]
        tall[v] = dict(n_seg=len(res), n_pass=int(sum(res)), crps_xs_range=[min(xs), max(xs)] if xs else None,
                       cov_range=[min(cv), max(cv)] if cv else None, sell_bias_range=[min(sb), max(sb)] if sb else None,
                       regret_xs_range=[min(rg), max(rg)] if rg else None,
                       r2_ss_range=[min(r2s), max(r2s)] if r2s else None, r2_g13_range=[min(r2g), max(r2g)] if r2g else None)
    out["tally_ALT"] = tall
    OUT.write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    def rng_fmt(r, fmt):
        return "n/a" if r is None else f"{r[0]:{fmt}}..{r[1]:{fmt}}"

    for v, t in tall.items():
        print(f"{v:7s} pass {t['n_pass']}/{t['n_seg']} | xsCRPS {rng_fmt(t['crps_xs_range'], '+.1%')} | cov "
              f"{rng_fmt(t['cov_range'], '.2f')} | sellbias {rng_fmt(t['sell_bias_range'], '+.2f')} | xsReg "
              f"{rng_fmt(t['regret_xs_range'], '+.0%')} | R2 ss {rng_fmt(t['r2_ss_range'], '.2f')} "
              f"g13 {rng_fmt(t['r2_g13_range'], '.2f')}")
    for seg in out["ss"]:
        if "sbc" in out["ss"][seg]:
            s = out["ss"][seg]["sbc"]
            print(seg, "SBC cov80 %.3f KS p %.3f chi2 p %.3f pass %s" % (s["cov80"], s["ks_p"], s["chi2_p"], out["ss"][seg]["sbc_pass"]))
        for v in ("M0", "TL1", "TL2", "TA3", "TA5", "TBC", "TW"):
            if v in out["ss"][seg]["variants"] and "detection" in out["ss"][seg]["variants"][v]:
                print("  det", seg, v, out["ss"][seg]["variants"][v]["detection"])


if __name__ == "__main__":
    main()
