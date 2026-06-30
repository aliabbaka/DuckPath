"""
DuckPath — type a role or field and get a clean, LeetCode-style learning roadmap
to reach it, with free resources for every step.

Run:  streamlit run app.py
"""
import streamlit as st
from dotenv import load_dotenv

from jobs import fetch_postings                         # Phase 2
from analysis import analyze_postings                   # Phase 3
from resources import get_resources                     # Phase 4
from projects import generate_project_idea              # Phase 5
from practice import get_practice                        # Phase 5
from alt_paths import suggest_alt_paths                 # Phase 6
from simulations import get_simulations, INTERVIEW_SIMULATORS  # Phase 7
from outreach import build_outreach_kit                 # Phase 8

st.set_page_config(page_title="DuckPath", page_icon="🦆", layout="centered")
load_dotenv()


# ── Caching (slow network/AI calls reused across reruns) ────────────────────
@st.cache_data(show_spinner=False)
def cached_postings(role):
    return fetch_postings(role)


@st.cache_data(show_spinner=False)
def cached_analysis(role, postings):
    return analyze_postings(role, postings)


@st.cache_data(show_spinner=False)
def cached_idea(skill, role):
    return generate_project_idea(skill, role)


@st.cache_data(show_spinner=False)
def cached_alt_paths(skill, role):
    return suggest_alt_paths(skill, role)


# ── Styling ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
          .block-container { padding-top: 2rem; max-width: 820px; }
          .brand { text-align:center; font-size:2.6rem; font-weight:800;
                   color:#1B3A57; letter-spacing:-1px; margin:0; }
          .brand b { color:#E0A800; }
          .tagline { text-align:center; color:#5b7891; font-size:1.02rem; margin:4px 0 8px; }
          .duck-bob { animation: bob 2.8s ease-in-out infinite; display:block; margin:0 auto; }
          @keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
          .stButton>button { font-weight:700; border-radius:10px; }
          h3 { color:#1B3A57; }
        </style>
        """,
        unsafe_allow_html=True,
    )


DUCK_SVG = """
<svg class="duck-bob" width="66" height="66" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="48" cy="64" rx="33" ry="28" fill="#FFD23F"/>
  <path d="M22 66 q26 20 52 0 q-26 26 -52 0" fill="#F4BE1E"/>
  <circle cx="62" cy="38" r="23" fill="#FFDD55"/>
  <circle cx="70" cy="33" r="4.6" fill="#27384a"/>
  <circle cx="71.6" cy="31.4" r="1.5" fill="#fff"/>
  <path d="M83 38 q19 5 0 12 q-7 -6 0 -12" fill="#FF924C"/>
</svg>
"""


# ── Roadmap graph (LeetCode/NeetCode style: connected nodes, top → goal) ─────
def build_roadmap_dot(skills, role):
    def esc(s):
        return str(s).replace('"', "'")

    lines = [
        "digraph roadmap {",
        '  rankdir=TB; bgcolor="transparent"; pad=0.3; nodesep=0.45; ranksep=0.55;',
        '  node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=13 '
        'penwidth=1.4 color="#E0A800" fillcolor="#FFF6DC" fontcolor="#1B3A57" '
        'margin="0.28,0.16"];',
        '  edge [color="#E0A800" penwidth=2 arrowsize=0.7];',
        '  start [label="Start here" fillcolor="#1B3A57" fontcolor="white" color="#1B3A57"];',
    ]
    prev = "start"
    for i, skill in enumerate(skills):
        nid = f"s{i}"
        lines.append(f'  {nid} [label="{i + 1}. {esc(skill)}"];')
        lines.append(f"  {prev} -> {nid};")
        prev = nid
    lines.append(f'  goal [label="GOAL: {esc(role)}" fillcolor="#1B3A57" '
                 'fontcolor="white" color="#1B3A57"];')
    lines.append(f"  {prev} -> goal;")
    lines.append("}")
    return "\n".join(lines)


def render_resources(res):
    """Render the curated-resource dict as friendly bullets."""
    for _section, fields in res.items():
        if not isinstance(fields, dict):
            st.write(fields)
            continue
        for key, val in fields.items():
            label = key.replace("_", " ").title()
            if isinstance(val, bool):
                if val:
                    st.markdown(f"- ✅ {label}")
            elif isinstance(val, list):
                st.markdown(f"**{label}:**")
                for item in val:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;• {item}", unsafe_allow_html=True)
            else:
                st.markdown(f"- **{label}:** {val}")


def render_alt_paths(alt):
    if not isinstance(alt, dict):
        st.write(alt)
        return
    for key, val in alt.items():
        st.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")


def render_links(items, empty_msg):
    if not items:
        st.info(empty_msg)
        return
    for it in items:
        name, link = it.get("name", "Resource"), it.get("link", "")
        st.markdown(f"- [{name}]({link})" if link else f"- {name}")


# ── Page ────────────────────────────────────────────────────────────────────
inject_css()
st.markdown(DUCK_SVG, unsafe_allow_html=True)
st.markdown('<div class="brand">Duck<b>Path</b></div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Type a role or field — get a free, step-by-step '
            'roadmap to reach it.</div>', unsafe_allow_html=True)

st.session_state.setdefault("analysis", None)
st.session_state.setdefault("role", "")

role_input = st.text_input(
    "Target role or field",
    placeholder="e.g. Machine Learning Engineer, Data Analyst, Frontend Developer",
    label_visibility="collapsed",
)
go = st.button("🦆  Build my roadmap", use_container_width=True)

if go:
    role = role_input.strip()
    if not role:
        st.warning("Type a role or field first — e.g. \"Machine Learning Engineer\".")
        st.stop()
    try:
        with st.spinner("Reading current job postings and mapping your path..."):
            postings = cached_postings(role)
            if not postings:
                st.warning("Couldn't find live postings for that. Try a job-title style "
                           "phrase like \"Machine Learning Engineer\" or \"Data Analyst\".")
                st.stop()
            analysis = cached_analysis(role, postings)
    except Exception as e:
        st.error(f"Something went wrong while building your roadmap: {e}")
        st.stop()

    if not analysis.get("core_skills"):
        st.warning("I read the postings but couldn't pin down clear skills. "
                   "Try a slightly different title.")
        st.stop()

    st.session_state.analysis = analysis
    st.session_state.role = role

# ── Results ─────────────────────────────────────────────────────────────────
analysis = st.session_state.analysis
role = st.session_state.role

if analysis:
    skills = analysis["core_skills"]

    st.markdown(f"### Your roadmap to {role}")
    st.caption("Follow it top to bottom. Each step below has free resources and a "
               "project to prove it.")
    st.graphviz_chart(build_roadmap_dot(skills, role), use_container_width=True)

    st.markdown("### Learn each step")
    for i, skill in enumerate(skills, 1):
        with st.expander(f"Step {i} — {skill}"):
            st.markdown("**📚 Learn it (free)**")
            res = get_resources(skill)
            if res:
                render_resources(res)
            else:
                st.info("No curated resources for this one yet.")

            st.markdown("**🛠️ Prove it with a project**")
            st.write(cached_idea(skill, role))

            st.markdown("**🌱 Other ways to prove it**")
            render_alt_paths(cached_alt_paths(skill, role))

    # Extra prep tools — collapsed and optional, so they stay out of the way.
    with st.expander("➕ Extra prep tools (interviews, simulations, networking)"):
        focus = analysis.get("interview_focus") or []
        if focus:
            st.markdown("**What interviewers test for**")
            for item in focus:
                st.markdown(f"- {item}")

        signals = analysis.get("experience_signals") or []
        if signals:
            st.markdown("**What they want to see on your resume**")
            for item in signals:
                st.markdown(f"- {item}")

        st.markdown("**Try a real job simulation**")
        render_links(get_simulations(role),
                     "No exact match — search this role on Forage or Kaggle.")

        st.markdown("**Practice the interview itself**")
        render_links(INTERVIEW_SIMULATORS, "No interview simulators listed.")

        st.markdown("**Free practice resources**")
        for category in ("coding_interviews", "system_design", "behavioral"):
            items = get_practice(category)
            if items:
                st.markdown(f"*{category.replace('_', ' ').title()}*")
                for item in items:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;• {item}", unsafe_allow_html=True)

        st.markdown("**Network your way in**")
        kit = build_outreach_kit(role)
        for term in kit["linkedin_terms"]:
            st.markdown(f"- {term}")
        if kit["questions"]:
            st.markdown("*Questions to ask during the call:*")
            for q in kit["questions"]:
                st.markdown(f"&nbsp;&nbsp;&nbsp;• {q}", unsafe_allow_html=True)
        st.code(kit["email_template"], language="text")
