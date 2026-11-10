"""Deterministic safety guards. The LLM proposes; these decide what may auto-apply."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
TAX = json.load(open(ROOT / "data" / "taxonomy.json"))
INJECTION = re.compile(r"ignore (all )?(previous|prior)|you are (now )?(the )?admin|system prompt|mark this report|as an ai", re.I)
MIN_AUTO_CONF = 0.85
TEXT_ONLY = {"spelling", "noise", "exam_reference"}  # words only: no number / math may move

def body(q): return q[q["questionType"]]
def strip(s): return re.sub(r"<[^>]+>", " ", s or "")
def numbers(s): return sorted(re.findall(r"\d+(?:\.\d+)?", strip(s)))

def apply_edit(q, edit):
    """Return the new field value, or raise ValueError if the edit is not a clean surgical change."""
    f, find, rep = edit["field"], edit["find"], edit["replace"]
    cur = body(q).get(f)
    if f == "answer":
        if cur != find: raise ValueError(f"answer is {cur!r}, edit expects {find!r}")
        return rep
    if not isinstance(cur, str) or cur.count(find) != 1:
        raise ValueError(f"find string must occur exactly once in {f} (found {cur.count(find) if isinstance(cur, str) else 0})")
    return cur.replace(find, rep)

def detect_injection(comment): return bool(INJECTION.search(comment or ""))

def validate(res, q, comment=""):
    """Enforce taxonomy + scope; downgrade (never upgrade) the route. Returns (res, notes)."""
    notes = []
    if res["verdict"] not in TAX["verdicts"]: raise ValueError("verdict outside closed list")
    rep = res.get("repair")
    if res["verdict"] != "defect":
        if rep or res.get("edit"): notes.append("non-defect: edit/repair stripped")
        res["repair"], res["edit"], res["route"] = None, None, "no_change"
        return res, notes
    if rep not in TAX["repairs"]: raise ValueError("repair outside closed list")
    spec, edit = TAX["repairs"][rep], res.get("edit")
    if edit:
        if edit["field"] not in spec["fields"]:
            notes.append(f"scope: {rep} may not touch {edit['field']}"); res["edit"] = edit = None
        else:
            try:
                new = apply_edit(q, edit)
                if rep in TEXT_ONLY:
                    old = body(q)[edit["field"]]
                    if rep == "exam_reference": pass
                    elif numbers(old) != numbers(new) or old.count("<math") != new.count("<math"):
                        raise ValueError("text-only repair changed a number or formula")
            except ValueError as e:
                notes.append(f"edit rejected: {e}"); res["edit"] = edit = None
    auto_ok = spec["auto"] and edit and res["confidence"] >= MIN_AUTO_CONF
    c = res.get("checks", {})
    if rep == "answer_key" and edit and not c.get("format_only"):
        # highest stakes: needs an independent solve AND the stored solution to agree with the new key
        auto_ok = auto_ok and c.get("solver") == edit["replace"] and c.get("solution_agrees")
    if res["route"] == "auto_apply" and not auto_ok:
        notes.append("auto_apply downgraded to faculty_review"); res["route"] = "faculty_review"
    if not spec["auto"]: res["route"] = "faculty_review"
    if res["route"] == "no_change" : res["route"] = "faculty_review"  # a defect never closes silently
    return res, notes
