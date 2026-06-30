"""
DuckPath — type a role, get a free step-by-step roadmap to reach it.
Run:  streamlit run app.py
"""
import streamlit as st
from dotenv import load_dotenv

from jobs import fetch_postings
from analysis import analyze_postings
from resources import get_resources
from projects import generate_project_idea
from practice import get_practice
from alt_paths import suggest_alt_paths
from simulations import get_simulations, get_interview_simulators
from outreach import build_outreach_kit

load_dotenv()
st.set_page_config(page_title="DuckPath", page_icon="🦆", layout="wide")


# ── Design system ─────────────────────────────────────────────────────────────
CSS = """
<style>
:root {
  --navy:   #1B3A57;
  --gold:   #E0A800;
  --light:  #FFF9EC;
  --muted:  #5b7891;
  --radius: 12px;
  --shadow: 0 4px 24px rgba(0,0,0,0.08);
}

/* Global */
.block-container { padding-top: 2.5rem !important; max-width: 1060px; padding-bottom: 4rem !important; }

/* Hero */
.hero {
  background: linear-gradient(135deg, #1B3A57 0%, #243f5c 100%);
  border-radius: 20px;
  padding: 2rem 2.4rem 1.8rem;
  margin: 0 0 1.8rem;
  display: flex;
  align-items: center;
  gap: 1.6rem;
}
.hero-text h1 {
  color: white;
  font-size: 2.6rem;
  font-weight: 800;
  margin: 0 0 4px;
  letter-spacing: -1px;
  line-height: 1;
}
.hero-text h1 b { color: #E0A800; }
.hero-text p { color: #aac4da; margin: 0 0 10px; font-size: 1rem; }
.stat-bar { display: flex; gap: 1.6rem; flex-wrap: wrap; }
.stat { color: #7fa8c4; font-size: 0.82rem; font-weight: 500; }
.stat b { color: #E0A800; }

/* Chip row */
.chip-label {
  font-size: 0.8rem;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* CTA button */
.stButton > button[kind="primary"] {
  background: linear-gradient(90deg, #E0A800, #f0bc00) !important;
  color: #1B3A57 !important;
  font-weight: 800 !important;
  border-radius: var(--radius) !important;
  border: none !important;
  font-size: 1.05rem !important;
  letter-spacing: 0.02em !important;
  transition: transform 0.12s, box-shadow 0.12s !important;
  box-shadow: 0 4px 14px rgba(224,168,0,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(224,168,0,0.45) !important;
}

/* Secondary (chip) buttons */
.stButton > button[kind="secondary"] {
  border-radius: 999px !important;
  border: 1.5px solid var(--gold) !important;
  color: var(--navy) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  background: var(--light) !important;
  padding: 3px 12px !important;
  transition: all 0.15s !important;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--gold) !important;
  color: white !important;
}

/* Cards */
.card {
  background: white;
  border-radius: var(--radius);
  padding: 1.1rem 1.3rem;
  margin-bottom: 0.75rem;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--gold);
  line-height: 1.55;
}
.card-muted {
  background: white;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  line-height: 1.5;
}
.card-idea {
  background: #fffbf0;
  border: 1.5px solid #f0d080;
  border-radius: var(--radius);
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
  font-size: 0.97rem;
  line-height: 1.6;
}

/* Badges */
.badge {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  margin-left: 6px;
  vertical-align: middle;
}
.badge-green { background: #d4f5e2; color: #1a7a45; }
.badge-gold  { background: #fff3cc; color: #7a5500; }
.badge-blue  { background: #ddeeff; color: #1a4a7a; }

/* Dividers */
.divider { border: none; border-top: 2px solid #eef0f3; margin: 1.4rem 0; }
.gold-divider { border: none; border-top: 2px solid rgba(224,168,0,0.35); margin: 0.3rem 0 1.4rem; }

/* Progress */
.progress-label {
  font-size: 0.82rem;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 3px;
}

/* Section heading */
.section-heading {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--navy);
  margin: 0 0 2px;
}
.section-sub {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 1rem;
}

/* Info panel */
.info-panel {
  background: #f0f6ff;
  border-radius: var(--radius);
  padding: 1.4rem;
  text-align: center;
  color: var(--muted);
  font-size: 0.95rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: #f0f2f5;
  border-radius: 10px;
  padding: 4px;
  border: none;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 7px;
  padding: 5px 14px;
  font-weight: 600;
  font-size: 0.87rem;
  color: var(--muted);
  border: none;
}
.stTabs [aria-selected="true"] {
  background: white !important;
  color: var(--navy) !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }

/* Input focus glow */
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px rgba(224,168,0,0.2) !important;
}
.stTextInput > div > div > input {
  border-radius: var(--radius) !important;
  font-size: 1rem !important;
  padding: 0.6rem 0.9rem !important;
}

/* Duck animation */
.duck-bob { animation: bob 2.8s ease-in-out infinite; display: block; }
@keyframes bob {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-7px); }
}

/* Graph container */
[data-testid="stCustomComponentV1"] {
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow) !important;
  background: white !important;
  width: 100% !important;
}
[data-testid="stCustomComponentV1"] iframe {
  border: none !important;
  display: block !important;
}

/* Footer — fixed to viewport bottom */
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(8px);
  border-top: 1px solid #eef0f3;
  z-index: 9999;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0.45rem 1.4rem;
  gap: 1rem;
  font-size: 0.78rem;
  color: var(--muted);
}
.footer-author {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  white-space: nowrap;
}
.footer-author:last-child { justify-content: flex-end; }
.footer-copy { text-align: center; font-size: 0.75rem; color: var(--muted); }
.footer a { color: var(--muted); text-decoration: none; line-height: 0; }
.footer a:hover svg { opacity: 0.75; }

/* Dark-mode toggle — lives inside the Streamlit header bar, to the left of the ⋮ menu.
   The header is 2.875rem tall; we match it so the button sits flush in that row. */
div.block-container > div:has(#dp-toggle-anchor) + div {
  position: fixed !important;
  top: 0 !important;
  right: 3.5rem !important;   /* ⋮ button is ~2.25rem wide; 3.5rem clears it + running-man */
  height: 2.875rem !important;
  display: flex !important;
  align-items: center !important;
  z-index: 10002 !important;
  width: fit-content !important;
  padding: 0 !important;
  margin: 0 !important;
}
div.block-container > div:has(#dp-toggle-anchor) + div > div,
div.block-container > div:has(#dp-toggle-anchor) + div [data-testid="stButtonGroup"] {
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
}
div.block-container > div:has(#dp-toggle-anchor) + div .stButton button {
  height: 2rem !important;
  padding: 0 0.5rem !important;
  font-size: 1.05rem !important;
  line-height: 1 !important;
  border: none !important;
  border-radius: 4px !important;
  background: transparent !important;
  color: rgb(49,51,63) !important;
  box-shadow: none !important;
}
div.block-container > div:has(#dp-toggle-anchor) + div .stButton button:hover {
  background: rgba(151,166,195,0.15) !important;
}

</style>
"""

DARK_CSS = """
<style>
/* ── Backgrounds ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
.block-container,
[data-testid="stVerticalBlock"] > div { background: #0f1923 !important; }
[data-testid="stHeader"] { background: rgba(15,25,35,0.9) !important; }

/* ── All text defaults to light ── */
.stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
.stApp label, .stApp span:not(svg span),
.stApp li, .stApp td, .stApp th,
.stApp [data-testid="stMarkdown"],
.stApp [data-testid="stMarkdown"] *,
.stApp [data-testid="stText"],
.stApp [data-testid="stCaptionContainer"],
.stApp .stMarkdown p { color: #e2e8f0 !important; }

/* ── Custom classes ── */
.section-heading, .section-sub, .progress-label, .chip-label { color: #e2e8f0 !important; }
.card, .card-muted, .card-idea { background: #1a2535 !important; color: #e2e8f0 !important; }
.card { border-left-color: var(--gold) !important; }
.info-panel { background: #1a2535 !important; color: #a0b9cc !important; }
.divider { border-top-color: #2d4a66 !important; }

/* ── Hero ── */
.hero { background: linear-gradient(135deg,#0d2236 0%,#1a3a55 100%) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #1a2535 !important; }
.stTabs [data-baseweb="tab"] { color: #a0b9cc !important; }
.stTabs [aria-selected="true"] { background: #243f5c !important; color: #e2e8f0 !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
  background: #1a2535 !important;
  color: #e2e8f0 !important;
  border-color: #2d4a66 !important;
}
.stTextInput label, .stTextArea label { color: #e2e8f0 !important; }

/* ── Buttons ── */
.stButton > button { background: #1a2535 !important; color: #e2e8f0 !important; border-color: #2d4a66 !important; }
.stButton > button[data-testid="baseButton-primary"] {
  background: var(--gold) !important; color: #1B3A57 !important; border: none !important;
}
/* Dark-mode toggle sits in the header bar — keep it transparent, not the dark card color */
div.block-container > div:has(#dp-toggle-anchor) + div .stButton button {
  background: transparent !important;
  border: none !important;
  color: #e2e8f0 !important;
  box-shadow: none !important;
}

/* ── Checkbox / radio ── */
.stCheckbox label, .stRadio label { color: #e2e8f0 !important; }

/* ── Footer ── */
.footer { background: rgba(15,25,35,0.97) !important; border-top-color: #2d4a66 !important; color: #a0b9cc !important; }
.footer .footer-copy, .footer .footer-author { color: #a0b9cc !important; }
.footer svg { fill: #a0b9cc !important; }

/* ── Links ── */
a { color: var(--gold) !important; }
</style>
"""

DUCK_SVG = """
<svg class="duck-bob" width="74" height="74" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="48" cy="64" rx="33" ry="28" fill="#FFD23F"/>
  <path d="M22 66 q26 20 52 0 q-26 26 -52 0" fill="#F4BE1E"/>
  <circle cx="62" cy="38" r="23" fill="#FFDD55"/>
  <circle cx="70" cy="33" r="4.6" fill="#27384a"/>
  <circle cx="71.6" cy="31.4" r="1.5" fill="#fff"/>
  <path d="M83 38 q19 5 0 12 q-7 -6 0 -12" fill="#FF924C"/>
</svg>
"""

EXAMPLE_ROLES = [
    "Machine Learning Engineer",
    "Data Analyst",
    "Software Engineer",
    "UX Designer",
    "Product Manager",
    "Data Scientist",
]

ALT_ICONS = {
    "open_source":          "🔓",
    "technical_writing":    "✍️",
    "community_leadership": "👥",
    "competitions":         "🏆",
    "devops_architecture":  "⚙️",
}


# ── Caching ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_postings(role):
    return fetch_postings(role)

@st.cache_data(show_spinner=False)
def cached_analysis(role, postings_tuple):
    return analyze_postings(role, list(postings_tuple))

@st.cache_data(show_spinner=False)
def cached_idea(skill, role, seed=0):
    # seed is a cache-busting int — increment it to force a new LLM call
    return generate_project_idea(skill, role)

@st.cache_data(show_spinner=False)
def cached_alt(skill, role):
    return suggest_alt_paths(skill, role)


# ── Roadmap ───────────────────────────────────────────────────────────────────
_ARROW = (
    '<div style="text-align:center;color:#E0A800;font-size:1.5rem;'
    'line-height:1;margin:2px 0;">↓</div>'
)
_NODE_BASE = (
    "text-align:center;padding:10px 28px;border-radius:10px;"
    "font-weight:700;font-size:0.9rem;"
)


def render_roadmap(skills, role):
    _, center, _ = st.columns([1, 2, 1])
    with center:
        completed = st.session_state.get("completed", set())

        st.markdown(
            f'<div style="{_NODE_BASE}background:#1B3A57;color:white;">'
            "▶&nbsp; Start here</div>",
            unsafe_allow_html=True,
        )

        for i, skill in enumerate(skills):
            done  = skill in completed
            label = f"{'✅  ' if done else str(i + 1) + '.  '}{skill}"
            st.markdown(_ARROW, unsafe_allow_html=True)
            if st.button(label, key=f"rmnode_{i}", use_container_width=True):
                st.session_state.active_skill = f"skill_{i}"
                st.rerun()

        st.markdown(_ARROW, unsafe_allow_html=True)
        st.markdown(
            f'<div style="{_NODE_BASE}background:#1B3A57;color:#E0A800;'
            f'border:2px solid #E0A800;">🎯&nbsp; {role}</div>',
            unsafe_allow_html=True,
        )


# ── Resource rendering ────────────────────────────────────────────────────────
def render_learn_tab(res):
    if not res:
        st.markdown('<div class="info-panel">No curated resources for this skill yet — check back soon.</div>', unsafe_allow_html=True)
        return
    for _section, fields in res.items():
        if not isinstance(fields, dict):
            continue
        for key, val in fields.items():
            label = key.replace("_", " ").title()
            if isinstance(val, bool):
                if val:
                    st.markdown(
                        f'<div class="card-muted">✅ <b>{label}</b>'
                        f'&nbsp;<span class="badge badge-green">Free cert</span></div>',
                        unsafe_allow_html=True,
                    )
            elif isinstance(val, list):
                items = "".join(f"<li style='margin:3px 0'>{v}</li>" for v in val)
                st.markdown(
                    f'<div class="card-muted"><b>{label}</b>'
                    f'<ul style="margin:6px 0 0 18px;padding:0">{items}</ul></div>',
                    unsafe_allow_html=True,
                )
            elif isinstance(val, str) and val.strip():
                is_url = val.startswith("http")
                content = f'<a href="{val}" target="_blank">{val}</a>' if is_url else val
                st.markdown(
                    f'<div class="card-muted">{"🔗 " if is_url else ""}<b>{label}:</b> {content}</div>',
                    unsafe_allow_html=True,
                )


def render_prove_tab(skill, role):
    seed_key = f"seed_{skill}"
    st.session_state.setdefault(seed_key, 0)

    with st.spinner("Generating project idea..."):
        idea = cached_idea(skill, role, st.session_state[seed_key])

    st.markdown(f'<div class="card-idea">{idea}</div>', unsafe_allow_html=True)

    if st.button("↺  Generate another idea", key=f"regen_{skill}"):
        st.session_state[seed_key] += 1
        st.rerun()


def render_alt_tab(skill, role):
    with st.spinner("Generating alternative paths..."):
        alt = cached_alt(skill, role)
    if not isinstance(alt, dict):
        st.write(alt)
        return
    for key, val in alt.items():
        icon  = ALT_ICONS.get(key, "•")
        label = key.replace("_", " ").title()
        st.markdown(
            f'<div class="card-muted">{icon} <b>{label}:</b> {val}</div>',
            unsafe_allow_html=True,
        )


# ── Prep tools ────────────────────────────────────────────────────────────────
def render_prep_tools(analysis, role):
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown("### ➕ Extra prep tools")

    t1, t2, t3, t4 = st.tabs([
        "🎯  Interview focus",
        "🏢  Simulations",
        "📝  Practice",
        "🤝  Network",
    ])

    with t1:
        focus   = analysis.get("interview_focus") or []
        signals = analysis.get("experience_signals") or []
        if focus:
            st.markdown("**What interviewers test for**")
            for item in focus:
                st.markdown(f'<div class="card-muted">• {item}</div>', unsafe_allow_html=True)
        if signals:
            st.markdown("**What they want on your resume**")
            for item in signals:
                st.markdown(f'<div class="card-muted">• {item}</div>', unsafe_allow_html=True)
        if not focus and not signals:
            st.markdown('<div class="info-panel">No interview focus data for this role.</div>', unsafe_allow_html=True)

    with t2:
        sims = get_simulations(role)
        if sims:
            st.markdown("**Practice doing the actual job**")
            for s in sims:
                st.markdown(f"- [{s['name']}]({s['link']})")
        else:
            st.info("No exact match — search your role on [Forage](https://www.theforage.com) or [Kaggle](https://www.kaggle.com).")
        st.markdown("---")
        st.markdown("**Mock interview platforms**")
        for s in get_interview_simulators():
            st.markdown(f"- [{s['name']}]({s['link']})")

    with t3:
        for category in ("coding_interviews", "system_design", "behavioral"):
            items = get_practice(category)
            if items:
                st.markdown(f"**{category.replace('_', ' ').title()}**")
                for item in items:
                    st.markdown(f'<div class="card-muted">• {item}</div>', unsafe_allow_html=True)

    with t4:
        kit = build_outreach_kit(role)
        st.markdown("**LinkedIn search terms**")
        for term in kit["linkedin_terms"]:
            st.markdown(f'<div class="card-muted">🔍 {term}</div>', unsafe_allow_html=True)
        if kit["questions"]:
            st.markdown("**Questions to ask on the call**")
            for q in kit["questions"]:
                st.markdown(f'<div class="card-muted">• {q}</div>', unsafe_allow_html=True)
        st.markdown("**Cold email — edit and copy**")
        st.text_area(
            label="cold-email",
            value=kit["email_template"],
            height=210,
            label_visibility="collapsed",
            key="email_draft",
        )


# ── App ───────────────────────────────────────────────────────────────────────
# Dark mode state must be set before CSS injection
st.session_state.setdefault("dark_mode", False)

st.markdown(CSS, unsafe_allow_html=True)
if st.session_state.dark_mode:
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# Hidden anchor div — CSS uses :has(#dp-toggle-anchor) to pin the next element
# (the dark toggle button) to position:fixed at the top-right corner.
st.markdown('<div id="dp-toggle-anchor"></div>', unsafe_allow_html=True)
_dm_label = "☀️" if st.session_state.dark_mode else "🌙"
if st.button(_dm_label, key="dark_toggle", help="Toggle dark / light mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# Hero
st.markdown(f"""
<div class="hero">
  {DUCK_SVG}
  <div class="hero-text">
    <h1>Duck<b>Path</b></h1>
    <p>Type a target role — get a complete, free prep plan to reach it.</p>
    <div class="stat-bar">
      <span class="stat"><b>20+</b> roles mapped</span>
      <span class="stat"><b>100%</b> free resources</span>
      <span class="stat"><b>No</b> sign-up needed</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Session state defaults
for key, default in [
    ("analysis",      None),
    ("role",          ""),
    ("active_skill",  None),
    ("completed",     set()),
    ("chip_selected", ""),
]:
    st.session_state.setdefault(key, default)

# Chips come FIRST — they set chip_selected (a plain state key, not a widget key)
# so Streamlit never complains about modifying a widget's key from outside.
st.markdown('<div class="chip-label">Try an example →</div>', unsafe_allow_html=True)
chip_cols = st.columns(len(EXAMPLE_ROLES), gap="small")
for col, chip in zip(chip_cols, EXAMPLE_ROLES):
    if col.button(chip, key=f"chip_{chip}", use_container_width=True):
        st.session_state["chip_selected"] = chip
        st.rerun()

# Input reads chip_selected as its initial value; plain value= (no key=) avoids conflict
role_input = st.text_input(
    "Target role",
    value=st.session_state["chip_selected"],
    placeholder='e.g. "Machine Learning Engineer" or "Data Analyst at Google"',
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)
go = st.button("🦆  Build my roadmap", type="primary", use_container_width=True)

if go:
    role = role_input.strip()
    if not role:
        st.warning('Type a role first — or click one of the examples above.')
        st.stop()

    try:
        with st.status("Building your roadmap...", expanded=True) as status:
            st.write("📡  Reading live job postings...")
            postings = cached_postings(role)
            if not postings:
                status.update(label="Couldn't find postings.", state="error")
                st.warning('No postings found. Try a job-title phrase like "Data Analyst" or "Software Engineer".')
                st.stop()
            st.write(f"✅  Found {len(postings)} postings. Analysing with AI...")
            analysis = cached_analysis(role, tuple(postings))
            st.write("🗺️  Mapping your skill path...")
            status.update(label="Your roadmap is ready.", state="complete")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.stop()

    if not analysis.get("core_skills"):
        st.warning("Couldn't pin down clear skills. Try a slightly different title.")
        st.stop()

    st.session_state.analysis      = analysis
    st.session_state.role          = role
    st.session_state.active_skill  = None
    st.session_state.chip_selected = ""
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
analysis = st.session_state.analysis
role     = st.session_state.role

if analysis:
    skills    = analysis["core_skills"]
    completed = st.session_state.completed
    n_done    = len([s for s in skills if s in completed])

    # Progress bar
    st.markdown(
        f'<div class="progress-label">{n_done} of {len(skills)} skills completed</div>',
        unsafe_allow_html=True,
    )
    st.progress(n_done / len(skills) if skills else 0)

    # Roadmap header
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-heading">Your roadmap to {role}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-sub">{len(skills)} skills · click any node to explore it</div>',
        unsafe_allow_html=True,
    )

    # Interactive roadmap (pure Streamlit — always centered)
    render_roadmap(skills, role)

    # Skill detail panel
    active = st.session_state.active_skill
    if active and active.startswith("skill_"):
        idx = int(active.split("_")[1])
        if idx < len(skills):
            skill = skills[idx]

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            title_col, check_col = st.columns([6, 1])
            with title_col:
                st.markdown(f"### {idx + 1}. {skill}")
            with check_col:
                ck = f"done_{skill}"
                # Only set initial value — never overwrite after widget is rendered,
                # otherwise Streamlit discards the user's click every rerun.
                st.session_state.setdefault(ck, skill in st.session_state.completed)
                if st.checkbox("Done ✅", key=ck):
                    st.session_state.completed.add(skill)
                else:
                    st.session_state.completed.discard(skill)

            learn_tab, prove_tab, alt_tab = st.tabs(["📚 Learn", "🛠️ Prove", "🌱 Alt paths"])

            with learn_tab:
                render_learn_tab(get_resources(skill))
            with prove_tab:
                render_prove_tab(skill, role)
            with alt_tab:
                render_alt_tab(skill, role)

    else:
        st.markdown(
            '<div class="info-panel" style="margin-top:1rem">'
            '👆 Click any skill node on the roadmap above to explore its resources, projects, and proof paths.'
            '</div>',
            unsafe_allow_html=True,
        )

    render_prep_tools(analysis, role)

    _LI = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#0A66C2">'
        '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 '
        '1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 '
        '0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 '
        '0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 '
        '1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 '
        '.774 23.2 0 22.222 0h.003z"/></svg>'
    )
    _GH = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#333">'
        '<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258'
        '.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 '
        '17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 '
        '1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93'
        ' 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-'
        '.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 '
        '1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42'
        '.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 '
        '24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
    )
    st.markdown(
        '<div class="footer">'

        # Left — Patrick MM
        '<div class="footer-author">'
        'Patrick MM'
        f'<a href="https://github.com/Patrick948-stack" target="_blank" title="GitHub">{_GH}</a>'
        f'<a href="https://www.linkedin.com/in/mulikuzap/" target="_blank" title="LinkedIn">{_LI}</a>'
        '</div>'

        # Centre — copyright
        '<div class="footer-copy">© 2026 DuckPath</div>'

        # Right — Ali Abbaka
        '<div class="footer-author">'
        'Ali Abbaka'
        f'<a href="https://github.com/aliabbaka" target="_blank" title="GitHub">{_GH}</a>'
        f'<a href="https://www.linkedin.com/in/aliabbaka" target="_blank" title="LinkedIn">{_LI}</a>'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )
