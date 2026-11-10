import json, sys, pathlib
from . import triage
d = pathlib.Path(__file__).resolve().parent.parent / "data"
res = triage.run(json.load(open(d / "questions.json")), json.load(open(d / "reports.json")))
json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "results.live.json", "w"), indent=1, ensure_ascii=False)
print(len(res), "reports triaged")
