"""
DuckPath — type a target role and let the duck map your free path to it.

This file is the only place that imports from every other module. Each imported
function already works on its own; this layer is the UI + wiring.

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

# set_page_config MUST be the first Streamlit call.
st.set_page_config(page_title="DuckPath", page_icon="🦆", layout="wide")
load_dotenv()


# ── Caching (cost/speed) ────────────────────────────────────────────────────
# Streamlit reruns this whole file on every interaction. The slow functions all
# hit the network/AI, so without caching the app re-pays for everything every
# time. Wrap them once here and call the cached versions below.
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


# ── The duck ────────────────────────────────────────────────────────────────
DUCK_SVG = """
<svg class="duck-bob" width="86" height="86" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="48" cy="64" rx="33" ry="28" fill="#FFD23F"/>
  <path d="M22 66 q26 20 52 0 q-26 26 -52 0" fill="#F4BE1E"/>
  <circle cx="62" cy="38" r="23" fill="#FFDD55"/>
  <circle cx="70" cy="33" r="4.6" fill="#27384a"/>
  <circle cx="71.6" cy="31.4" r="1.5" fill="#fff"/>
  <path d="M83 38 q19 5 0 12 q-7 -6 0 -12" fill="#FF924C"/>
</svg>
"""


def inject_css():
    st.markdown(
        """
        <style>
          .stApp { background: linear-gradient(180deg,#eaf6ff 0%,#f6fbff 38%,#ffffff 100%); }
          #MainMenu, footer { visibility: hidden; }

          .brand { text-align:center; font-size:2.9rem; font-weight:800;
                   color:#1b3a57; letter-spacing:-1.5px; margin-bottom:0; }
          .brand b { color:#FFB400; }
          .tagline { text-align:center; color:#5b7891; font-size:1.06rem; margin-top:2px; }

          .duck-bob { animation: bob 2.6s ease-in-out infinite; }
          @keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

          .duck-row { display:flex; align-items:flex-start; gap:14px; margin:16px 0; }
          .bubble { position:relative; background:#fff; border:2px solid #FFE08A;
                    border-radius:18px; padding:13px 18px; color:#26415e; font-size:1.02rem;
                    box-shadow:0 6px 18px rgba(27,58,87,.09); max-width:760px; line-height:1.5; }
          .bubble:before { content:""; position:absolute; left:-13px; top:20px;
                    border:7px solid transparent; border-right-color:#FFE08A; }

          .road { margin:6px 0 6px 8px; }
          .node { display:flex; align-items:center; gap:14px; position:relative; padding:9px 0; }
          .node:not(:last-child):before { content:""; position:absolute; left:16px; top:36px;
                    bottom:-9px; width:3px; background:#FFD23F; }
          .dot { min-width:34px; height:34px; border-radius:50%; background:#FFB400; color:#1b3a57;
                 display:flex; align-items:center; justify-content:center; font-weight:800;
                 box-shadow:0 2px 7px rgba(0,0,0,.14); z-index:1; }
          .goal .dot { background:#1b3a57; color:#FFD23F; }
          .node-label { background:#fff; border-radius:11px; padding:9px 16px; font-weight:600;
                 color:#1b3a57; box-shadow:0 2px 9px rgba(27,58,87,.08); }
          .goal .node-label { background:#1b3a57; color:#fff; }

          .stButton>button { background:#FFB400; color:#1b3a57; font-weight:800; border:none;
                 border-radius:12px; padding:.55rem 1.5rem; transition:.15s; }
          .stButton>button:hover { background:#ffc62e; transform:translateY(-1px); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def duck_says(message):
    """Render the duck mascot with a speech bubble."""
    st.markdown(
        f'<div class="duck-row">{DUCK_SVG}<div class="bubble">{message}</div></div>',
        unsafe_allow_html=True,
    )


def render_roadmap(selected, role):
    """Draw the chosen routes as a connected path from Start to the Goal role."""
    nodes = ['<div class="node"><div class="dot">▶</div>'
             '<div class="node-label">Start — where you are today</div></div>']
    for i, skill in enumerate(selected, 1):
        nodes.append(f'<div class="node"><div class="dot">{i}</div>'
                     f'<div class="node-label">{skill}</div></div>')
    nodes.append(f'<div class="node goal"><div class="dot">🎯</div>'
                 f'<div class="node-label">Goal — {role}</div></div>')
    st.markdown(f'<div class="road">{"".join(nodes)}</div>', unsafe_allow_html=True)


def render_resources(res):
    """Render the curated-resource dict as friendly bullets instead of raw JSON."""
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
    """Render the alt-paths dict (open_source, technical_writing, ...) as bullets."""
    if not isinstance(alt, dict):
        st.write(alt)
        return
    for key, val in alt.items():
        st.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")


def render_links(items, empty_msg):
    """Render a list of {name, link} dicts as bullet links."""
    if not items:
        st.info(empty_msg)
        return
    for it in items:
        name, link = it.get("name", "Resource"), it.get("link", "")
        st.markdown(f"- [{name}]({link})" if link else f"- {name}")


# ── Page ────────────────────────────────────────────────────────────────────
inject_css()

st.markdown(f'<div style="text-align:center">{DUCK_SVG}</div>', unsafe_allow_html=True)
st.markdown('<div class="brand">Duck<b>Path</b></div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Tell the duck your dream role — get a free, '
            'choose-your-own-route map to reach it.</div>', unsafe_allow_html=True)
st.write("")

# Persist results so the page stays interactive (route picking reruns the script).
st.session_state.setdefault("analysis", None)
st.session_state.setdefault("role", "")

role_input = st.text_input(
    "Target role",
    placeholder="e.g. Google Internship, AI Engineer, SWE Intern at Meta",
    label_visibility="collapsed",
)
go = st.button("🦆  Map my DuckPath")

if go:
    role = role_input.strip()
    if not role:
        duck_says("Quack! You'll need to type a role first so I know where we're headed.")
        st.stop()
    try:
        with st.spinner("Paddling through current job postings..."):
            postings = cached_postings(role)
            if not postings:
                duck_says("I couldn't find live postings for that one. Try a broader "
                          "title and we'll waddle on.")
                st.stop()
            analysis = cached_analysis(role, postings)
    except Exception as e:
        st.error(f"Something went wrong while building your map: {e}")
        st.info("This is usually a temporary API hiccup — give it another try in a moment.")
        st.stop()

    if not analysis.get("core_skills"):
        duck_says("I read the postings but couldn't pin down clear skills. "
                  "A slightly different role title usually helps!")
        st.stop()

    st.session_state.analysis = analysis
    st.session_state.role = role

# ── Results (driven by session_state, so the UI survives reruns) ─────────────
analysis = st.session_state.analysis
role = st.session_state.role

if analysis:
    skills = analysis["core_skills"]

    duck_says(f"Here's the thing about <b>{role}</b>: there's no single road. "
              f"I pulled the <b>{len(skills)} skills</b> recruiters keep asking for — "
              "tick the routes you want to travel and I'll chart the path.")

    tab_map, tab_sims, tab_interview, tab_network = st.tabs(
        ["🗺️ Learning routes", "🧪 Job simulations", "🎤 Interview prep", "🤝 Networking"]
    )

    with tab_map:
        st.markdown("#### Pick your routes")
        selected = []
        cols = st.columns(3)
        for i, skill in enumerate(skills):
            with cols[i % 3]:
                if st.checkbox(skill, key=f"route_{skill}"):
                    selected.append(skill)

        st.divider()

        if not selected:
            duck_says("Pick at least one route above and watch your path appear. "
                      "Start with one — you can always add more lily pads later.")
        else:
            duck_says(f"Nice choice! Here's how your <b>{len(selected)} route"
                      f"{'s' if len(selected) > 1 else ''}</b> connect you to <b>{role}</b>. "
                      "Every step is a skill recruiters scan for — learn it, then prove it.")
            render_roadmap(selected, role)
            st.divider()

            for skill in selected:
                with st.expander(f"📍 {skill}", expanded=len(selected) == 1):
                    st.caption(f"Why it matters: **{skill}** is one of the signals "
                               f"hiring teams look for in {role}. Learn it, then ship "
                               "the project below as proof.")

                    st.markdown("##### 📚 Learn it free")
                    res = get_resources(skill)
                    if res:
                        render_resources(res)
                    else:
                        st.info("Not curated yet — a great one to add to resources.py!")

                    st.markdown("##### 🛠️ Prove it with a project")
                    st.write(cached_idea(skill, role))

                    st.markdown("##### 🌱 Other ways to prove it")
                    render_alt_paths(cached_alt_paths(skill, role))

    with tab_sims:
        st.markdown("#### Try the job before you get it")
        duck_says("Simulations let you do the actual work of the role — free, and "
                  "great to talk about in interviews.")
        render_links(get_simulations(role),
                     "No exact match yet — search this role on Forage or Kaggle.")

    with tab_interview:
        st.markdown("#### What interviewers actually test for")
        focus = analysis.get("interview_focus") or []
        if focus:
            for item in focus:
                st.markdown(f"- {item}")
        else:
            st.info("No specific focus extracted for this role.")

        st.markdown("#### Practice the interview itself")
        render_links(INTERVIEW_SIMULATORS, "No interview simulators listed.")

        st.markdown("#### Free practice resources")
        for category, items in PRACTICE_RESOURCES.items():
            with st.expander(category.replace("_", " ").title()):
                for item in items:
                    st.markdown(f"- {item}")

    with tab_network:
        st.markdown("#### Network your way in")
        duck_says("A warm intro beats a cold application every time. Here's your kit.")
        kit = build_outreach_kit(role)

        st.markdown("**🔍 LinkedIn search terms**")
        for term in kit["linkedin_terms"]:
            st.markdown(f"- {term}")

        st.markdown("**💬 Questions worth asking**")
        for q in kit["questions"]:
            st.markdown(f"- {q}")

        st.markdown("**✉️ Cold-email template** (fill in the placeholders):")
        st.code(kit["email_template"], language="text")
