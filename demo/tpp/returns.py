"""Component 1b (replaces examples/mpo_v2/fusion.py): the Return Preference Engine.

The prototype fused three synthetic marks per holding (underwritten, actual, group forecast) by precision weights,
with group biases from a forecast archive and Benktander credibility. The user's files carry different evidence:
  1. strategy forward returns (ER file): Downside / Base / Upside per Department x Vertical x vehicle;
  2. the underwritten base IRR and MOIC per holding (fund file);
  3. the since-inception actual IRR, TVPI and DPI per holding (fund file).
So the forward return a stakeholder plans on is set by that stakeholder's PREFERENCE (which evidence to trust, and
how likely each ER world is) and UTILITY (how much the downside world weighs), not by a fixed statistical fusion:

  level_i     = S_b(i),Base + w_U * tilt_U,i + w_A * tilt_A,i                           (basis "blend")
  tilt_U,i    = y_i * clip(U_i - S_b,Base)        U_i = uw IRR_i - beta_b     y_i = max(0, 1 - age_i / 8)
  tilt_A,i    = phi * c_i * clip(A_i - peer_i)    c_i = clip((age_i - age_min + 1) / 5, 0, 1)
  r_i,s       = clip(level_i + (S_b,s - S_b,Base))                                       s in {Downside, Base, Upside}
  E_i         = sum_s pi_s r_i,s
  CE_i(gamma) = [sum_s pi_s (1 + r_i,s)^(H (1 - gamma))]^(1 / (H (1 - gamma))) - 1        (CRRA over the horizon H)

beta_b is the underwriting optimism MEASURED IN THE FILE: the median of (underwritten - actual IRR) over the bucket's
mature holdings (age >= 6 or DPI >= 0.75), credibility-weighted Z = n / (n + 20) toward the department's median (or a
4pp prior), as the prototype weighted archive biases. peer_i is the median actual IRR of the same bucket and vintage
band (so a 2021 vintage is compared with 2021 vintages, not with 2012 ones). Bases: "strategy" (w = 0: the ER return
itself), "blend" (weights chosen by the stakeholder), "underwritten" (level = U_i where available), "actual"
(phi = 1: relative performance persists in full). New money in a bucket always earns the ER strategy return: it has
no track record yet.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .buckets import BY_ID, CATALOG

WORLDS = ["Downside", "Base", "Upside"]
DEFAULT_PREFS = {
    "scenario_probs": {"Downside": 0.25, "Base": 0.50, "Upside": 0.25},
    "basis": "strategy",
    "weights": {"underwritten": 0.15, "actual": 0.25},
    "persistence": 0.30,
    "risk_aversion": 3.0,
    "uw_debias": True,
}
VINTAGE_BANDS = [(-1e9, 2012), (2013, 2016), (2017, 2019), (2020, 2022), (2023, 1e9)]


def norm_prefs(prefs: dict | None) -> dict:
    p = {k: (dict(v) if isinstance(v, dict) else v) for k, v in DEFAULT_PREFS.items()}
    for k, v in (prefs or {}).items():
        if isinstance(v, dict) and isinstance(p.get(k), dict):
            p[k].update(v)
        else:
            p[k] = v
    pr = np.array([float(p["scenario_probs"][w]) for w in WORLDS])
    pr = np.clip(pr, 0.0, None)
    pr = pr / pr.sum() if pr.sum() > 0 else np.array([0.25, 0.5, 0.25])
    p["scenario_probs"] = dict(zip(WORLDS, map(float, pr)))
    return p


def er_table(er: pd.DataFrame, P) -> pd.DataFrame:
    """ER returns per bucket and world (decimal, annual). MAO rows are converted to total returns when the ER
    figures are read as excess over cash."""
    rows = []
    cash = er[er["key"] == BY_ID["CASH"].er_key].iloc[0]
    excess = bool(P.get("overlay.mao_returns_are_excess"))
    for b in CATALOG:
        m = er[er["key"] == b.er_key]
        if m.empty:
            raise KeyError(f"ER file has no row for {b.er_key}")
        r = m.iloc[0]
        vals = {w: float(r[w]) for w in WORLDS}
        if b.department == "Multi-Asset Overlay" and excess:
            vals = {w: vals[w] + float(cash[w]) for w in WORLDS}
        rows.append({"bucket": b.id, **vals, "flags": r["flags"]})
    return pd.DataFrame(rows).set_index("bucket")


def _band(v):
    if pd.isna(v):
        return -1
    for k, (lo, hi) in enumerate(VINTAGE_BANDS):
        if lo <= v <= hi:
            return k
    return -1


def underwriting_bias(book: pd.DataFrame, P) -> pd.DataFrame:
    """Measured underwriting optimism (underwritten minus actual IRR) per bucket, credibility-weighted."""
    k = float(P.get("returns.credibility_constant"))
    prior = float(P.get("returns.uw_bias_prior_pp")) / 100
    mature = ((book["age"] >= float(P.get("returns.mature_age")))
              | (book["ACTUAL_DPI"].fillna(0) >= float(P.get("returns.mature_dpi"))))
    ok = mature & book["uw_irr"].notna() & book["act_irr"].notna() & (book["act_irr"].abs() < 1.0)
    d = book[ok].assign(err=lambda x: x["uw_irr"] - x["act_irr"])
    dept_med = d.groupby("department")["err"].agg(["median", "size"])
    out = []
    for b in CATALOG:
        g = d[d["bucket"] == b.id]["err"]
        n = int(len(g))
        dm = dept_med.loc[b.department] if b.department in dept_med.index else None
        pri = float(dm["median"]) if dm is not None and dm["size"] >= 10 else prior
        z = n / (n + k)
        beta = z * (float(g.median()) if n else 0.0) + (1 - z) * pri
        out.append({"bucket": b.id, "n_mature": n, "median_gap": float(g.median()) if n else np.nan,
                    "prior": pri, "Z": z, "beta": float(np.clip(beta, -0.05, 0.15))})
    return pd.DataFrame(out).set_index("bucket")


def holding_returns(book: pd.DataFrame, er: pd.DataFrame, P, prefs: dict | None = None) -> dict:
    """Per-holding scenario returns and their decomposition, plus bucket-level returns for the engine."""
    pf = norm_prefs(prefs)
    ert = er_table(er, P)
    bias = underwriting_bias(book, P)
    pi = np.array([pf["scenario_probs"][w] for w in WORLDS])
    cap = float(P.get("returns.tilt_cap_pp")) / 100
    lo, hi = P.get("returns.clip")
    age_min = float(P.get("returns.actual_min_age"))
    H = float(P.get("returns.horizon_years"))
    gam = float(pf["risk_aversion"])
    basis = pf["basis"]
    wU = float(pf["weights"].get("underwritten", 0.0)) if basis == "blend" else 0.0
    wA = float(pf["weights"].get("actual", 0.0)) if basis == "blend" else 0.0
    phi = float(pf["persistence"]) if basis != "actual" else 1.0
    if basis == "actual":
        wA = 1.0

    h = book.copy()
    S = ert.loc[h["bucket"], WORLDS].to_numpy()
    sb = S[:, 1]
    h["S_down"], h["S_base"], h["S_up"] = S[:, 0], S[:, 1], S[:, 2]
    # underwritten signal, debiased by the bucket's measured optimism, weighted toward young holdings
    beta = bias.loc[h["bucket"], "beta"].to_numpy() if pf["uw_debias"] else np.zeros(len(h))
    U = h["uw_irr"].to_numpy(dtype=float) - beta
    youth = np.clip(1.0 - h["age"].to_numpy(dtype=float) / 8.0, 0.0, 1.0)
    has_u = ~np.isnan(U)
    tiltU = np.where(has_u, youth * np.clip(np.nan_to_num(U) - sb, -cap, cap), 0.0)
    # actual signal: excess over the same bucket and vintage band, credibility by age
    h["band"] = h["vintage"].map(_band)
    act = h["act_irr"].clip(-0.9, 2.0)
    peer = np.full(len(h), np.nan)
    med_bb = act.groupby([h["bucket"], h["band"]]).agg(["median", "size"])
    med_b = act.groupby(h["bucket"]).median()
    med_dept_band = act.groupby([h["department"], h["band"]]).agg(["median", "size"])
    for i, r in enumerate(h.itertuples()):
        key = (r.bucket, r.band)
        if key in med_bb.index and med_bb.loc[key, "size"] >= 5:
            peer[i] = med_bb.loc[key, "median"]
        elif (r.department, r.band) in med_dept_band.index and med_dept_band.loc[(r.department, r.band), "size"] >= 5:
            peer[i] = med_dept_band.loc[(r.department, r.band), "median"]
        else:
            peer[i] = med_b.get(r.bucket, np.nan)
    A = act.to_numpy(dtype=float)
    cred = np.clip((h["age"].to_numpy(dtype=float) - age_min + 1.0) / 5.0, 0.0, 1.0)
    excess = np.where(np.isnan(A) | np.isnan(peer), 0.0, A - peer)
    tiltA = np.clip(phi * cred * np.clip(excess, -2 * cap, 2 * cap), -cap, cap)
    if basis == "underwritten":
        level = np.where(has_u, np.clip(np.nan_to_num(U), lo, hi), sb)
        tiltU_used = level - sb
        tiltA_used = np.zeros(len(h))
    else:
        tiltU_used = wU * tiltU
        tiltA_used = wA * tiltA
        level = sb + tiltU_used + tiltA_used
    R = np.clip(level[:, None] + (S - sb[:, None]), lo, hi)
    h["r_down"], h["r_base"], h["r_up"] = R[:, 0], R[:, 1], R[:, 2]
    h["r_exp"] = R @ pi
    h["r_ce"] = ce(R, pi, gam, H)
    h["uw_beta"], h["uw_debiased"], h["uw_youth"], h["tilt_uw"] = beta, U, youth, tiltU_used
    h["act_peer"], h["act_excess"], h["act_cred"], h["tilt_act"] = peer, excess, cred, tiltA_used
    h["shortfall_vs_uw"] = np.where(has_u, h["act_irr"] - h["uw_irr"], np.nan)
    # bucket level: existing holdings (NAV-weighted) and new money (ER)
    exist = {}
    for b in CATALOG:
        g = h[h["bucket"] == b.id]
        w = g["nav_bn"].to_numpy()
        if len(g) and w.sum() > 1e-9:
            exist[b.id] = (g[["r_down", "r_base", "r_up"]].to_numpy().T @ w / w.sum()).tolist()
        else:
            exist[b.id] = ert.loc[b.id, WORLDS].tolist()
    new = {b.id: ert.loc[b.id, WORLDS].tolist() for b in CATALOG}
    bk = pd.DataFrame({"bucket": [b.id for b in CATALOG]}).set_index("bucket")
    for j, w in enumerate(WORLDS):
        bk[f"exist_{w}"] = [exist[b][j] for b in bk.index]
        bk[f"new_{w}"] = [new[b][j] for b in bk.index]
    Ex = bk[[f"exist_{w}" for w in WORLDS]].to_numpy()
    Nw = bk[[f"new_{w}" for w in WORLDS]].to_numpy()
    bk["exist_exp"], bk["new_exp"] = Ex @ pi, Nw @ pi
    bk["exist_ce"], bk["new_ce"] = ce(Ex, pi, gam, H), ce(Nw, pi, gam, H)
    return {"holdings": h, "buckets": bk, "er": ert, "bias": bias, "prefs": pf, "pi": pi}


def ce(R: np.ndarray, pi: np.ndarray, gamma: float, H: float) -> np.ndarray:
    """CRRA certainty-equivalent annual return over H years of scenario returns R (n, 3) with probabilities pi."""
    G = np.maximum(1.0 + np.asarray(R, float), 1e-6)
    if abs(gamma - 1.0) < 1e-9:
        return np.exp(np.log(G) @ pi) - 1.0
    e = H * (1.0 - gamma)
    return (np.power(G, e) @ pi) ** (1.0 / e) - 1.0
