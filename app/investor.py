"""Investor side: an investor's own framework, applied by the same fixed rules.

The framework is treated like a programme's published requirements, plus
must-have evidence that gates the result. Gemma is not involved here.
"""
import json
from pathlib import Path

from app import anomalies
from app.matching import ELIGIBLE, NOT_ELIGIBLE, UNCLEAR, check
from app.readiness import CRITERIA, EVIDENCED, apply_conflicts, assess

DATA = Path(__file__).resolve().parent.parent / "data" / "demo_startups.json"


def load_startups(path=DATA):
    """Demo startups with their stored Gemma extraction; rules run fresh each time."""
    startups = []
    for s in json.loads(Path(path).read_text()):
        d = s["extraction"]
        conflicts = anomalies.contradictions(s["text"], d.get("contradictions", []))
        results = apply_conflicts(assess(d.get("evidence", {}), s["text"]), conflicts)
        flags = anomalies.detect(s["text"], d.get("anomalies", []))
        startups.append({"name": s["name"], "text": s["text"], "data": d, "results": results,
                         "warnings": len(flags) + len(conflicts)})
    return startups


def screen(startup, framework):
    """Apply an investor framework. Missing must-have evidence makes it not a fit."""
    m = check(startup["data"].get("profile", {}), framework, startup["results"])
    names = {c["id"]: c["question"] for c in CRITERIA}
    status = {r["id"]: r["status"] for r in startup["results"]}
    missing = [names[cid] for cid in framework.get("required_evidence", []) if status.get(cid) != EVIDENCED]
    if missing and m["verdict"] != NOT_ELIGIBLE:
        m["verdict"] = NOT_ELIGIBLE
        m["reasons"] = [f"Missing must-have: {q}" for q in missing]
        m["confirm"] = None
    if startup["warnings"] and m["verdict"] == ELIGIBLE:
        m["reasons"] = m["reasons"] + ["Has warnings (trick text or contradictions): review before contacting"]
    m["met"] = sum(r["status"] == EVIDENCED for r in startup["results"])
    return m


def screen_all(startups, framework):
    order = {ELIGIBLE: 0, UNCLEAR: 1, NOT_ELIGIBLE: 2}
    out = [(s, screen(s, framework)) for s in startups]
    return sorted(out, key=lambda x: (order[x[1]["verdict"]], -x[1]["met"]))
