"""
Phase 9 + 10 — Wire everything into one Streamlit app.   OWNER: both (Live Share)

This file is the only place that imports from every other module. By the time you
get here, every imported function should already work on its own (you tested each
with `python <file>.py`). This phase is just connecting wires + polish.

Run:  streamlit run app.py
"""
import streamlit as st
from dotenv import load_dotenv

from jobs import fetch_postings                         # Phase 2
from analysis import analyze_postings                   # Phase 3
from resources import get_resources                     # Phase 4
from projects import generate_project_idea              # Phase 5
from practice import PRACTICE_RESOURCES                  # Phase 5
from alt_paths import suggest_alt_paths                 # Phase 6
from simulations import get_simulations, INTERVIEW_SIMULATORS  # Phase 7
from outreach import build_outreach_kit                 # Phase 8

load_dotenv()

st.title("🎯 Career Prep Map")
st.caption("Type a target role and get a complete, free prep plan.")

role = st.text_input(
    "Target role",
    placeholder="e.g. Google Internship, AI Engineer, SWE Intern at Meta",
)
go = st.button("Build my prep plan")


# TODO — Phase 10, gap #7 (COST/SPEED):
# Streamlit reruns this whole file on every click. Each skill triggers AI calls,
# so without caching the app re-pays for everything every interaction. Wrap the
# slow functions with @st.cache_data, e.g.:
#
#   @st.cache_data(show_spinner=False)
#   def cached_idea(skill, role):
#       return generate_project_idea(skill, role)
#
# and call the cached versions below.


if go and role:
    # TODO — Phase 10: handle empty/whitespace role, API errors, no postings found.
    with st.spinner("Pulling current postings and analyzing..."):
        postings = fetch_postings(role)          # Phase 2
        if not postings:
            st.warning("No postings found for that role. Try a broader title.")
            st.stop()
        analysis = analyze_postings(role, postings)   # Phase 3  -> dict

    st.header(f"Prep Map: {role}")

    # ── Per-skill nodes (the "map") ──
    for skill in analysis["core_skills"]:
        with st.expander(f"📍 {skill}"):
            st.subheader("Learn it free")
            res = get_resources(skill)
            st.write(res if res else "Not curated yet — add this one to resources.py!")

            st.subheader("Prove it (project)")
            st.write(generate_project_idea(skill, role))

            st.subheader("Other ways to prove it")
            st.write(suggest_alt_paths(skill, role))

    # ── Whole-role sections ──
    st.subheader("Try a real job simulation")
    sims = get_simulations(role)
    st.write(sims if sims else "No exact match yet — search this role on Forage or Kaggle.")

    st.subheader("Practice the interview itself")
    st.write(INTERVIEW_SIMULATORS)

    st.subheader("What interviewers test for")
    st.write(analysis["interview_focus"])

    st.subheader("Practice for free")
    st.write(PRACTICE_RESOURCES)

    st.subheader("Network your way in")
    st.write(build_outreach_kit(role))
