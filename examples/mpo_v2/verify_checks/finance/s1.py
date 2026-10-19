import sys, json
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
r = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\results.json", encoding="utf-8"))
def show(d, pre="", depth=0):
    if depth > 3: return
    if isinstance(d, dict):
        for k, v in d.items():
            t = type(v).__name__
            ln = len(v) if hasattr(v, "__len__") and not isinstance(v, str) else ""
            s = ""
            if isinstance(v, (int, float, str)) and not isinstance(v, bool):
                s = repr(v)[:80]
            elif isinstance(v, bool):
                s = repr(v)
            print(pre + str(k), t, ln, s)
            show(v, pre + "  ", depth + 1)
    elif isinstance(d, list) and d and isinstance(d[0], dict):
        print(pre + "[0] keys:", list(d[0].keys())[:40])
show(r)
