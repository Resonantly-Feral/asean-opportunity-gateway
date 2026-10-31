"""ASEAN Opportunity Gateway: submit, assess, match, track, improve."""
import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# Streamlit reruns this file on every update but keeps imported modules cached.
# Drop our own modules so a new deploy never mixes old and new code.
for _m in [m for m in sys.modules if m == "app" or m.startswith("app.")]:
    del sys.modules[_m]

import streamlit as st
from dotenv import load_dotenv

from app import anomalies, gemma
from app.matching import ELIGIBLE, NOT_ELIGIBLE, UNCLEAR, load_programmes, match_all
from app.readiness import (AREAS, CRITERIA, EVIDENCED, NOT_ACHIEVED, PLAIN, apply_conflicts,
                           area_summary, assess, changes, gaps)

load_dotenv()
try:
    for k in ("GEMINI_API_KEY", "GEMMA_MODEL"):
        if k in st.secrets:
            os.environ.setdefault(k, st.secrets[k])
except Exception:
    pass

st.set_page_config(page_title="ASEAN Opportunity Gateway", page_icon="🌏", layout="wide")
ss = st.session_state
ss.setdefault("history", [])   # past assessments, newest last
ss.setdefault("tracker", [])   # applications the founder is tracking

TRACK_STATES = ["Interested", "Preparing", "Submitted", "Interview", "Accepted", "Rejected"]
SAMPLES = json.loads((Path(__file__).resolve().parent.parent / "data" / "samples.json").read_text())
LEVEL_ICON = {"All addressed": "🟢", "Partly addressed": "🟡", "None addressed": "🔴"}
VERDICT_ICON = {ELIGIBLE: "✅", UNCLEAR: "❔", NOT_ELIGIBLE: "⛔"}
VERDICT_PLAIN = {ELIGIBLE: "Potential match", UNCLEAR: "Need one answer first", NOT_ELIGIBLE: "Not a fit right now"}

st.title("🌏 ASEAN Opportunity Gateway")
st.markdown("#### Discover ASEAN startup opportunities, understand eligibility gaps, and track your next steps.")
h1, h2, h3 = st.columns(3)
h1.info("**1. Describe your startup**\n\nIn plain words, like a short pitch.")
h2.info("**2. See what's backed up**\n\n9 simple questions. AI finds the sentences; fixed rules decide.")
h3.info("**3. Find programmes that may fit**\n\nReal ASEAN grants and accelerators, with reasons and what to confirm.")
st.caption("We check evidence. We never predict success or give made-up percentages.")
st.page_link("pages/2_For_investors.py", label="Investor or programme manager? Screen startups with your own framework →",
             icon="💼")

DISCLAIMER = ("This is a checklist of what the founder has stated. Nothing here is verified, "
              "and it is not an approval or endorsement by any programme.")

submit_tab, match_tab, track_tab, rubric_tab = st.tabs(
    ["1. Check my startup", "2. Programmes for me", "3. My applications", "How it works"])

with submit_tab:
    ss.setdefault("idea_text", "")
    c1, c2 = st.columns([4, 1])
    pick = c1.selectbox("Try a demo case", [x["name"] for x in SAMPLES])
    case = next(x for x in SAMPLES if x["name"] == pick)
    c1.caption(f"What to look for: {case['expect']}")
    c2.write("")
    if c2.button("Load sample submission", use_container_width=True):
        ss.idea_text = case["text"]
    text = st.text_area("Describe your startup idea", height=260, key="idea_text",
                        placeholder="Problem, customers, solution, traction, team, business model, next milestone…")
    slides = st.file_uploader("Pitch deck pages (optional, images)", type=["png", "jpg", "jpeg"],
                              accept_multiple_files=True)

    if st.button("Check my startup", type="primary", disabled=not text.strip()):
        with st.spinner(f"Gemma ({gemma.model_name()}) is reading your submission…"):
            try:
                data = gemma.extract(text, [(f.getvalue(), f.type) for f in slides or []])
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                st.stop()
        results = assess(data.get("evidence", {}), text)
        flags = anomalies.detect(text, data.get("anomalies", []))
        conflicts = anomalies.contradictions(text, data.get("contradictions", []))
        results = apply_conflicts(results, conflicts)
        ss.history.append({"text": text, "data": data, "results": results, "anomalies": flags,
                           "conflicts": conflicts,
                           "when": date.today().isoformat()})

    if ss.history:
        run = ss.history[-1]
        data, results = run["data"], run["results"]
        flags, conflicts = run.get("anomalies", []), run.get("conflicts", [])
        summary = area_summary(results)
        met = sum(v["met"] for v in summary.values())
        total = sum(v["total"] for v in summary.values())
        matches = match_all(data.get("profile", {}), load_programmes(), results)
        fits = [m for m in matches if m["verdict"] == ELIGIBLE]

        st.divider()
        st.subheader("At a glance")
        with st.container(border=True):
            k1, k2, k3 = st.columns(3)
            k1.metric("Questions backed by evidence", f"{met} of {total}")
            k2.metric("Potential programme matches", f"{len(fits)} of {len(matches)}",
                      help="Meets every requirement this app can check. Some requirements must still be "
                           "confirmed on the official page.")
            k3.metric("Warnings", len(flags) + len(conflicts),
                      help="Counts attempts to trick the AI and claims that contradict each other.")
            for area, v in summary.items():
                words = {"All addressed": "all answered", "Partly addressed": "partly answered",
                         "None addressed": "not answered yet"}[v["level"]]
                st.markdown(f"{LEVEL_ICON[v['level']]} **{area}:** {words} ({v['met']} of {v['total']})")
            if fits:
                st.markdown("🎯 **Potential match:** " + ", ".join(m["programme"]["name"] for m in fits)
                            + " (see Programmes for what to confirm)")

        if len(ss.history) > 1:
            gained, lost = changes(ss.history[-2]["results"], results)
            if gained or lost:
                st.success("**Since your last version:** "
                           + "; ".join([f"now backed: {g['question']}" for g in gained]
                                       + [f"no longer backed: {l['question']}" for l in lost]))

        if flags:
            st.warning("**⚠️ Someone tried to trick the AI.** This text tried to change the result. "
                       "It was ignored.\n\n"
                       + "\n".join(f"- “{f['text']}”" for f in flags))
        if conflicts:
            st.warning("**⚠️ The submission contradicts itself.** Neither claim counts until it's cleared up.\n\n"
                       + "\n".join(f"- “{c['first']}” vs “{c['second']}”" for c in conflicts))

        g = gaps(results)
        if g:
            st.subheader("Top things to do next")
            for i, r in enumerate(g[:3], 1):
                st.markdown(f"**{i}.** {r['action']}")
            if len(g) > 3:
                st.caption(f"+ {len(g) - 3} more in the details below.")

        with st.expander("See the evidence behind every answer"):
            s = data.get("summary", {})
            st.markdown(f"**Problem:** {s.get('problem') or '_not stated_'}  \n"
                        f"**Solution:** {s.get('solution') or '_not stated_'}  \n"
                        f"**Target market:** {s.get('target_market') or '_not stated_'}")
            for area in AREAS:
                st.markdown(f"#### {area}")
                for r in [r for r in results if r["area"] == area]:
                    icon = {EVIDENCED: "✅", NOT_ACHIEVED: "⭕"}.get(r["status"], "⚠️")
                    line = f"{icon} **{r['question']}** {PLAIN[r['status']]}"
                    if r["reason"] and r["status"] != NOT_ACHIEVED:
                        line += f" ({r['reason']})"
                    if r["quote"]:
                        line += f"\n\n> “{r['quote']}” _({r['source_label']})_"
                    elif r["status"] != EVIDENCED:
                        line += f"\n\n_To fix: {r['action']}_"
                    st.markdown(line)

        with st.expander("AI notes (for discussion only, never scored)"):
            c1, c2 = st.columns(2)
            c1.markdown("**Strengths**\n\n" + "\n".join(f"- {x}" for x in data.get("strengths", [])))
            c2.markdown("**Claims without proof**\n\n" + "\n".join(f"- {x}" for x in data.get("assumptions", [])))

        st.caption(DISCLAIMER + " To improve, edit the description and check again.")

with match_tab:
    if not ss.history:
        st.info("Assess an idea first.")
    else:
        run = ss.history[-1]
        profile = dict(run["data"].get("profile", {}))
        headline = st.empty()
        exp = st.expander("Details we used to match (edit if anything is wrong)")
        c = exp.columns(5)
        profile["country"] = c[0].text_input("Country", profile.get("country") or "") or None
        profile["stage"] = c[1].selectbox("Stage", [None, "idea", "prototype", "early revenue", "growth"],
                                          index=[None, "idea", "prototype", "early revenue", "growth"]
                                          .index(profile.get("stage")) if profile.get("stage") in
                                          ["idea", "prototype", "early revenue", "growth"] else 0)
        profile["sector"] = c[2].text_input("Sector", profile.get("sector") or "").lower() or None
        inc_opts = {"Unknown": None, "Yes": True, "No": False}
        inc_label = {None: "Unknown", True: "Yes", False: "No"}[profile.get("incorporated")]
        profile["incorporated"] = inc_opts[c[3].selectbox("Registered company", list(inc_opts),
                                                          index=list(inc_opts).index(inc_label))]
        size = c[4].number_input("Team size (0 = unknown)", 0, 100, profile.get("team_size") or 0)
        profile["team_size"] = size or None

        st.caption("Programme facts come from official pages, checked 31/10/2026. "
                   "Requirements change: always confirm on the official page before applying.")
        matched = match_all(profile, load_programmes(), run["results"])
        n_fit = sum(m["verdict"] == ELIGIBLE for m in matched)
        headline.subheader(f"Potential matches: {n_fit} of {len(matched)} programmes")
        st.caption("A potential match meets every requirement this app can check. It is not confirmed "
                   "eligibility: each card lists what you still need to confirm.")
        for m in matched:
            p = m["programme"]
            with st.container(border=True):
                st.markdown(f"### {VERDICT_ICON[m['verdict']]} {p['name']}: {VERDICT_PLAIN[m['verdict']]}")
                st.caption(f"{p.get('type', '')} · {', '.join(p.get('countries', []))} · "
                           f"Source: {p.get('source', 'not stated')}")
                st.markdown(p.get("offer", ""))
                for r in m["reasons"]:
                    st.markdown(f"- {r}")
                if p.get("not_checked") and m["verdict"] != NOT_ELIGIBLE:
                    st.markdown("**Still to confirm on the official page:**\n"
                                + "\n".join(f"- {x}" for x in p["not_checked"]))
                if m["confirm"]:
                    st.markdown(f"**One question to answer:** {m['confirm']}")
                if m["outstanding"] and m["verdict"] != NOT_ELIGIBLE:
                    st.markdown("**What this programme will want to see, that's missing:**")
                    for o in m["outstanding"]:
                        st.markdown(f"- {o}")
                if p.get("status"):
                    st.markdown(f"**Application window:** {p['status']}")
                if p.get("url"):
                    st.markdown(f"[Official page]({p['url']})")
                tracked = any(t["id"] == p["id"] for t in ss.tracker)
                if m["verdict"] != NOT_ELIGIBLE and not tracked:
                    if st.button("Track this programme", key=f"track_{p['id']}"):
                        ss.tracker.append({"id": p["id"], "name": p["name"], "status": "Interested",
                                           "note": "", "updated": date.today().isoformat()})
                        st.rerun()

with track_tab:
    if not ss.tracker:
        st.info("Track programmes from the Programmes tab.")
    for i, t in enumerate(ss.tracker):
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 4])
            c1.markdown(f"**{t['name']}**\n\nUpdated {t['updated']}")
            new = c2.selectbox("Status", TRACK_STATES, TRACK_STATES.index(t["status"]), key=f"st_{i}")
            note = c3.text_input("Next step / note", t["note"], key=f"note_{i}")
            if new != t["status"] or note != t["note"]:
                t.update(status=new, note=note, updated=date.today().isoformat())
    if ss.tracker:
        st.download_button("Export tracker (JSON)", json.dumps(ss.tracker, indent=2),
                           "tracker.json", "application/json")

with rubric_tab:
    st.markdown("### How ideas are checked")
    st.markdown("Gemma only **highlights** a quote for each question. Fixed rules give the mark:\n"
                "1. Nothing relevant → **Missing** (the founder didn't address it)\n"
                "2. Founder says it isn't done (\"we have not built a prototype\") → "
                "**Explicitly not achieved**\n"
                "3. Quote not word-for-word in the founder's text → **Quote not found in text**\n"
                "4. Quote fails the hard rule → **Fails rule**, with the reason\n"
                "5. Otherwise → **Evidence stated** (what the founder says, not verified)\n\n"
                "Asking again never changes a mark. Only new evidence in the text does. "
                "Instruction-like text in a submission is flagged as an anomaly and never obeyed. "
                "Self-contradicting claims are flagged as conflicting claims.")
    st.table([{"Area": c["area"], "Question": c["question"], "Counts": c["counts"],
               "Doesn't count": c["not_counts"], "Hard rule": c.get("rule", "—")} for c in CRITERIA])
    st.caption(DISCLAIMER)
