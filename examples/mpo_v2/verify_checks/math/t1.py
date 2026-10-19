import sys, time
out = open(sys.argv[1], "w", encoding="utf-8")
try:
    import clarabel, highspy, scipy, numpy as np
    print("clarabel", clarabel.__version__ if hasattr(clarabel, "__version__") else "?", file=out)
    h = highspy.Highs()
    print("highs", h.version() if hasattr(h, "version") else "?", file=out)
    print([n for n in dir(clarabel) if not n.startswith("_")], file=out)
except Exception as e:
    import traceback
    traceback.print_exc(file=out)
out.close()
