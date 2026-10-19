import sys, json, io
out = open(sys.argv[1], "w", encoding="utf-8")
r = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\results.json", encoding="utf-8"))
print(list(r.keys()), file=out)
s = r["solutions"]
print(json.dumps(s["GBO"], indent=1)[:3000], file=out)
print(json.dumps(s["MILP"], indent=1)[:4000], file=out)
print(json.dumps(s["B0"], indent=1)[:2000], file=out)
print(json.dumps(r["config"], indent=1), file=out)
print(json.dumps(r["phase1"], indent=1), file=out)
print(json.dumps(r["in_tree"], indent=1)[:6000], file=out)
import numpy, scipy, cvxpy, highspy
print(numpy.__version__, scipy.__version__, cvxpy.__version__, cvxpy.installed_solvers(), file=out)
out.close()
