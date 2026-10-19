import sys, json
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
p = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json", encoding="utf-8"))
for sec in sys.argv[2].split(","):
    print("=" * 30, sec)
    d = p[sec]
    for k, v in d.items():
        if isinstance(v, dict) and "value" in v:
            val = json.dumps(v["value"])
            print(f"- {k} = {val[:1500]}  [{v.get('unit','')}]")
            print(f"    rationale: {str(v.get('rationale',''))[:900]}")
            print(f"    source: {str(v.get('source',''))[:400]}")
        else:
            print(f"- {k} = {json.dumps(v)[:2500]}")
