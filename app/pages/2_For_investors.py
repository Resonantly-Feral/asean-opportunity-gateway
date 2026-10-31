"""Investor side: build your own evaluation framework and screen ASEAN startups."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
for _m in [m for m in sys.modules if m == "app" or m.startswith("app.")]:
    del sys.modules[_m]

import streamlit as st

from app.investor import load_startups, screen_all
from app.matching import ASEAN, ELIGIBLE, NOT_ELIGIBLE, SECTORS, STAGES, UNCLEAR
from app.readiness import CRITERIA

st.set_page_config(page_title="For investors · ASEAN Opportunity Gateway", page_icon="💼", layout="wide")
ss = st.session_state
ss.setdefault("shortlist", [])

st.title("💼 For investors and programme managers")
st.markdown("#### Set your own evaluation framework. See which ASEAN startups fit, and why.")
st.caption("Your framework is applied by the same fixed rules as the founder side. "
           "No AI judgment, no success percentages. Startups below are demo examples.")

VERDICT = {ELIGIBLE: ":green-background[✅ Fits your framework]",
           UNCLEAR: ":orange-background[❔ Need one answer first]",
           NOT_ELIGIBLE: ":red-background[⛔ Not a fit]"}

with st.container(border=True):
    st.subheader("1. Your framework")
    c1, c2, c3 = st.columns(3)
    countries = c1.multiselect("Countries", ASEAN, help="Leave empty for all of ASEAN")
    stages = c2.multiselect("Stages", STAGES, default=STAGES)
    sectors = c3.multiselect("Sectors", SECTORS, help="Leave empty for any sector")
    c4, c5 = st.columns([3, 1])
    must = c4.multiselect("Must-have evidence", [c["question"] for c in CRITERIA],
                          default=["Is there evidence customers want it?"])
    registered = c5.checkbox("Registered company only")
    min_team = c5.number_input("Minimum team size", 0, 20, 0)

framework = {
    "countries": countries or ["ANY_ASEAN"],
    "stages": stages or STAGES,
    "sectors": sectors or ["ANY"],
    "incorporated_required": registered,
    "min_team_size": min_team,
    "required_evidence": [c["id"] for c in CRITERIA if c["question"] in must],
}

results = screen_all(load_startups(), framework)
fits = sum(m["verdict"] == ELIGIBLE for _, m in results)
st.subheader(f"2. Startups that fit: {fits} of {len(results)}")

cols = st.columns(3)
for i, (s, m) in enumerate(results):
    p = s["data"].get("profile", {})
    summary = s["data"].get("summary", {})
    with cols[i % 3].container(border=True):
        st.markdown(f"**{s['name']}**  \n{VERDICT[m['verdict']]}")
        st.caption(f"{p.get('country') or '?'} · {p.get('stage') or '?'} · {p.get('sector') or '?'}  \n"
                   f"{m['met']} of 9 questions backed")
        if summary.get("problem"):
            st.markdown(f"<small>{summary['problem']}</small>", unsafe_allow_html=True)
        reasons = [r for r in m["reasons"] if r != "Meets the requirements this app checks"]
        for r in reasons:
            st.markdown(f"<small>• {r}</small>", unsafe_allow_html=True)
        if m["confirm"]:
            st.markdown(f"<small>**Ask:** {m['confirm']}</small>", unsafe_allow_html=True)
        if m["verdict"] != NOT_ELIGIBLE:
            if s["name"] in ss.shortlist:
                st.button("✓ Shortlisted", key=f"sl_{s['name']}", disabled=True, use_container_width=True)
            elif st.button("Shortlist", key=f"sl_{s['name']}", use_container_width=True):
                ss.shortlist.append(s["name"])
                st.rerun()
        with st.expander("Evidence"):
            for r in s["results"]:
                mark = "✅" if r["status"] == "Evidence stated" else "⚠️"
                st.markdown(f"<small>{mark} {r['question']}</small>", unsafe_allow_html=True)

st.subheader("3. Your shortlist")
if not ss.shortlist:
    st.info("Shortlist startups above to arrange a meeting.")
else:
    for name in ss.shortlist:
        st.markdown(f"- **{name}**: next step, request an intro meeting")
st.caption("Everything shown is what founders have stated. Nothing is verified, and this is not investment advice.")
