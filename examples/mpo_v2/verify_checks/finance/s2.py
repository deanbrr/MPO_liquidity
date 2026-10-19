import sys, json
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
p = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json", encoding="utf-8"))
def show(d, pre="", depth=0, maxdepth=2):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                print(pre + str(k) + ":")
                if depth < maxdepth:
                    show(v, pre + "  ", depth + 1, maxdepth)
                else:
                    print(pre + "  ...", list(v.keys())[:20])
            elif isinstance(v, list):
                s = json.dumps(v)
                print(pre + str(k) + " = " + (s if len(s) < 300 else s[:300] + "..."))
            else:
                print(pre + str(k) + " = " + repr(v)[:300])
print("TOP KEYS:", list(p.keys()))
show(p, maxdepth=1)
