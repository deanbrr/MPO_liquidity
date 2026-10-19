"""SYNTHETIC - NOT ADIC DATA. Reduced verification instance: 20 holdings (every group and sleeve represented, group
NAV totals rescaled to the full book's so every $-denominated parameter keeps its meaning), tree 5 x 4 x 3 = 60
leaves. Everything else is params.json unchanged, except the MILP gap (1e-6, so the author's MILP runs to optimality)."""
import json
import os

SRC = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reduced")
os.makedirs(OUT, exist_ok=True)
P = json.load(open(SRC, encoding="utf-8"))
keep = ["PE-01", "PE-05", "PE-08", "PE-12", "SEC-02", "SEC-04", "SEC-05", "CO-01", "CO-02", "CS-01", "PC-01", "PC-03",
        "HF-01", "HF-03", "LO-01", "LO-03", "LO-04", "RA-01", "RA-02", "RA-08"]
units = P["book"]["units"]["value"]
full_tot = {}
for u in units:
    full_tot[u["group"]] = full_tot.get(u["group"], 0.0) + u["nav"]
sel = [dict(u) for u in units if u["id"] in keep]
sel_tot = {}
for u in sel:
    sel_tot[u["group"]] = sel_tot.get(u["group"], 0.0) + u["nav"]
for u in sel:
    f = full_tot[u["group"]] / sel_tot[u["group"]]
    u["nav"] = round(u["nav"] * f, 6)
    u["unfunded"] = round(u["unfunded"] * f, 6)
P["book"]["units"]["value"] = sel
P["book"]["units"]["rationale"] = "VERIFICATION REDUCED INSTANCE (SYNTHETIC): 20 of the 55 holdings, group totals rescaled to the full book."
P["tree"]["branches"]["value"] = [5, 4]
P["tree"]["stage1_strata"]["value"] = {"STR_DB": 1, "STR_other": 1, "DRT_GW": 1, "DRT": 1, "BEN": 1}
P["objective"]["milp_gap"]["value"] = 1e-6
json.dump(P, open(os.path.join(OUT, "params.json"), "w", encoding="utf-8"), indent=1)
print(len(sel), {g: round(sum(u["nav"] for u in sel if u["group"] == g), 3) for g in full_tot})
