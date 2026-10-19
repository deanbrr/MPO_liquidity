import sys, json
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
p = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json", encoding="utf-8"))
segs = p["book"]["segments"]
for k, v in segs.items():
    vv = v.get("value", v) if isinstance(v, dict) else v
    print(k, json.dumps(vv)[:900])
print("== units")
units = p["book"]["units"]["value"]
print("rationale:", p["book"]["units"].get("rationale"))
for u in units:
    print(json.dumps(u)[:400])
