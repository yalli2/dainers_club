# Loads one dated issue from tools/issues/<YYYY-MM-DD>.py (default: newest; override with ISSUE=YYYY-MM-DD)
import os, glob
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issues")
_f = os.path.join(_d, os.environ["ISSUE"] + ".py") if os.environ.get("ISSUE") else sorted(glob.glob(f"{_d}/*.py"))[-1]
exec(open(_f, encoding="utf-8").read())
for C in (EN, ES):
    C["ko"] = KO[C["lang"]]
