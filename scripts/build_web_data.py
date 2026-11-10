import json, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
q = {x["_id"]: x for x in json.load(open(D / "data/questions.json"))}
res, fin = json.load(open(D / "results.json")), json.load(open(D / "findings.json"))
rp = {x["reportId"]: x for x in json.load(open(D / "data/reports.json"))}
Q = {}
for i in {r["questionId"] for r in res}:
    x = q[i]; b = x[x["questionType"]]
    Q[i] = dict(id=i, type=x["questionType"], subject=x["subject"], chapter=x["chapter"], question=b["question"], solution=b.get("solution") or "", answer=b["answer"], hist=x["errorHistory"])
open(D / "web/data.js", "w").write("const DATA=" + json.dumps(dict(q=Q, results=res, findings=fin, reports=rp), ensure_ascii=False) + ";")
