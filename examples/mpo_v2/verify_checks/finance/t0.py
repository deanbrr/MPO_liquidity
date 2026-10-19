import sys
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
import numpy, scipy, cvxpy, highspy
print("ok", numpy.__version__, scipy.__version__, highspy.__file__)
