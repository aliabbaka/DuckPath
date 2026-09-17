"""
app.py — AdvisorPath, dynamic multi-agent conversational advising platform.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

import agents
import db
import questions
from circuit_breaker import SAFE_FALLBACK_BODY, SAFE_FALLBACK_TITLE, screen_input

load_dotenv()
db.init_db()
db.seed_if_empty()

st.set_page_config(page_title="AdvisorPath — Dynamic AI Advising", page_icon="🧭", layout="wide")

# Custom styling for agent themes and timeline
APP_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #181926 0%, #201e38 50%, #1a162b 100%);
    color: #f0f0f5;
}

.agent-badge-A {
    background-color: #1e3a8a;
    color: #93c5fd;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 4px;
}

.agent-badge-B {
    background-color: #064e3b;
    color: #6ee7b7;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 4px;
}

.agent-badge-C {
    background-color: #581c87;
    color: #d8b4fe;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 4px;
}

.user-badge {
    background-color: #374151;
    color: #f3f4f6;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.8rem;
    display: inline-block;
    margin-bottom: 4px;
}

.chat-bubble {
    background: rgba(255, 255, 255, 0.05);
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
}

.chat-bubble-A { border-left-color: #3b82f6; }
.chat-bubble-B { border-left-color: #10b981; }
.chat-bubble-C { border-left-color: #a855f7; }
.chat-bubble-User { border-left-color: #9ca3af; }

.roadmap-eyebrow {
    color: rgba(255,255,255,0.8); letter-spacing: 3px; font-size: 0.75rem;
    text-transform: uppercase; text-align: center; font-weight: 700; margin-bottom: 0;
}
.roadmap-title {
    color: white; text-align: center; font-weight: 800; font-size: 1.8rem;
    margin-top: 0; margin-bottom: 1.5rem;
}
.timeline-card {
    background: rgba(30, 20, 70, 0.65); border-radius: 12px; padding: 12px 16px;
    color: white; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1);
}
.timeline-card .horizon-label {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8;
    margin-bottom: 4px; color: #a7f3d0;
}
.skill-gap-box {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid #ef4444;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.82rem;
    color: #fca5a5;
    margin-top: 6px;
}
</style>
"""

st.markdown(APP_CSS, unsafe_allow_html=True)

# ── session state initialization ──────────────────────────────────────────
defaults = {
    "student_id": None,
    "institution_id": "whitman",
    "year": "sophomore",
    "interests": ["ai-ml", "cybersecurity"],
    "completed_courses": [],
    "chat_messages": [],
    "recommendations": None,
    "show_split_screen": False,
    "blocked_reason": None,
    "roadmap_items": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Initialize student ID in db if not present
if not st.session_state.student_id:
    student_id = db.insert_student_profile(
        st.session_state.institution_id,
        st.session_state.year,
        st.session_state.interests,
        st.session_state.completed_courses,
        "beginner",
    )
    st.session_state.student_id = student_id
    st.session_state.roadmap_items = db.get_roadmap_items(student_id)

    # Initial welcoming greeting from Agent A
    welcome_msg = (
        "Hello! We're your AI advising team. I'm Agent A (Academic Tracker), and alongside "
        "Agent B (Professional Matcher) and Agent C (Visionary Futurist), we're here to help shape your personalized path. "
        "Tell us: what CS or STEM topics excite you right now, and what projects or courses have you taken?"
    )
    st.session_state.chat_messages.append({"speaker": "Agent A", "agent_id": "A", "content": welcome_msg})
    db.save_chat_message(student_id, "Agent A", welcome_msg)

st.title("🧭 AdvisorPath — Interactive Multi-Agent Advising")


# ── Header & Setup Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Student Setup")
    institutions = db.get_institutions()
    inst_options = {i["id"]: i["name"] for i in institutions}
    chosen_inst = st.selectbox(
        "University / Institution",
        options=list(inst_options.keys()),
        format_func=lambda k: inst_options[k],
        index=0 if st.session_state.institution_id == "whitman" else 1,
    )
    st.session_state.institution_id = chosen_inst

    chosen_year = st.selectbox(
        "Current Year",
        options=["first-year", "sophomore", "junior", "senior"],
        index=["first-year", "sophomore", "junior", "senior"].index(st.session_state.year),
    )
    st.session_state.year = chosen_year

    st.markdown("---")
    st.markdown("### 🤖 Your Advisory Team")
    st.markdown('<span class="agent-badge-A">🎓 Agent A</span> Academic Tracker (Unlocked Courses & Skills)', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge-B">💼 Agent B</span> Professional Matcher (Real Opportunities & Projects)', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge-C">🚀 Agent C</span> Visionary Futurist (Next Horizons & Advanced Roles)', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Reset Conversation & Roadmap"):
        st.session_state.chat_messages = []
        st.session_state.recommendations = None
        st.session_state.show_split_screen = False
        st.session_state.student_id = None
        st.rerun()


# ── Profile Dict Helper ──────────────────────────────────────────────────
def get_current_profile():
    return {
        "institution_id": st.session_state.institution_id,
        "year": st.session_state.year,
        "interests": st.session_state.interests,
        "completed_courses": st.session_state.completed_courses,
        "experience_level": "beginner",
    }


# ── Chat Handler ──────────────────────────────────────────────────────────
def handle_user_message(user_input):
    is_safe, reason = screen_input(user_input)
    if not is_safe:
        st.session_state.blocked_reason = reason
        st.rerun()
        return

    # 1. Append user message
    student_id = st.session_state.student_id
    st.session_state.chat_messages.append({"speaker": "User", "agent_id": "User", "content": user_input})
    db.save_chat_message(student_id, "User", user_input)

    # Detect interests from user text simple heuristic update
    text_lower = user_input.lower()
    for tag in questions.INTEREST_LABELS:
        if tag.replace("-", " ") in text_lower or questions.INTEREST_LABELS[tag].lower() in text_lower:
            if tag not in st.session_state.interests:
                st.session_state.interests.append(tag)

    # 2. Pick next responding agent based on sequence or user prompt
    last_agent = next((m["agent_id"] for m in reversed(st.session_state.chat_messages) if m["agent_id"] in ("A", "B", "C")), "C")
    next_agent = {"A": "B", "B": "C", "C": "A"}.get(last_agent, "A")

    # Format transcript history for the agent
    history = [
        {"speaker": m["speaker"], "content": m["content"]}
        for m in st.session_state.chat_messages
    ]

    try:
        reply = agents.run_chat_agent(next_agent, history, profile_context=get_current_profile())
    except Exception as e:
        reply = f"Thank you for sharing that! (Note: Could not reach Groq: {e})"

    speaker_name = f"Agent {next_agent}"
    st.session_state.chat_messages.append({"speaker": speaker_name, "agent_id": next_agent, "content": reply})
    db.save_chat_message(student_id, speaker_name, reply)

    st.rerun()


# ── Render Chat Interface ─────────────────────────────────────────────────
def render_chat_panel():
    st.subheader("💬 Live Multi-Agent Advising Chat")
    st.caption("Chat dynamically with your advisors to narrow down your interests and explore opportunities.")

    chat_container = st.container()
    with chat_container:
        for m in st.session_state.chat_messages:
            agent_id = m.get("agent_id", "User")
            speaker = m.get("speaker", "User")
            content = m.get("content", "")

            badge_class = f"agent-badge-{agent_id}" if agent_id in ("A", "B", "C") else "user-badge"
            bubble_class = f"chat-bubble-{agent_id}"

            st.markdown(
                f'''<div class="chat-bubble {bubble_class}">
                    <span class="{badge_class}">{speaker}</span><br>
                    <span>{content}</span>
                </div>''',
                unsafe_allow_html=True,
            )

    # User input chat box
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input = st.text_input("Type a message or answer advisor questions:", placeholder="e.g. I enjoyed Data Structures and want to explore Cybersecurity...")
        cols = st.columns([4, 3])
        with cols[0]:
            submit_msg = st.form_submit_button("Send Message 🚀")
        with cols[1]:
            ready_advice = st.form_submit_button("✨ Ready for Advice / Recommendations")

        if submit_msg and user_input.strip():
            handle_user_message(user_input.strip())
        elif ready_advice:
            trigger_advice_generation()


def trigger_advice_generation():
    profile = get_current_profile()
    student_id = st.session_state.student_id

    with st.spinner("Advisors are reviewing candidates, checking prerequisites, and organizing advice proposals..."):
        try:
            proposals = agents.generate_recommendations_proposal(profile, st.session_state.chat_messages)
        except Exception as e:
            st.error(f"Error generating advice proposals: {e}")
            return

    st.session_state.recommendations = proposals
    st.session_state.show_split_screen = True

    # Add advisor announcement to chat
    announcement = (
        "We've analyzed your profile and candidate opportunities! Review our tailored proposals below. "
        "Select whichever items fit your goal to build your private roadmap on the right."
    )
    st.session_state.chat_messages.append({"speaker": "Team Advisor", "agent_id": "A", "content": announcement})
    db.save_chat_message(student_id, "Team Advisor", announcement)
    st.rerun()


# ── Render Advice Proposals Section ────────────────────────────────────────
def render_advice_proposals():
    st.markdown("---")
    st.markdown("### 🎯 Agent Recommendations & Proposals")
    st.caption("Select items proposed by each agent to add to your private roadmap on the right.")

    proposals = st.session_state.recommendations
    if not proposals:
        st.info("No recommendations generated yet. Click 'Ready for Advice' above!")
        return

    agent_titles = {
        "A": "🎓 Agent A (Academic Tracker — Open & Required Courses)",
        "B": "💼 Agent B (Professional Matcher — Active Opportunities & Projects)",
        "C": "🚀 Agent C (Visionary Futurist — Next Horizon & Advanced Goals)",
    }

    for agent_id in ["A", "B", "C"]:
        items = proposals.get(agent_id, [])
        with st.expander(agent_titles[agent_id], expanded=True):
            if not items:
                st.write("No specific items proposed for this category.")
                continue

            for idx, item in enumerate(items):
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.markdown(f"**{item['title']}**")
                    st.markdown(f"<span style='font-size:0.85rem;'>{item['description']}</span>", unsafe_allow_html=True)

                    if item.get("skill_gap"):
                        st.markdown(f'<div class="skill-gap-box">⚠️ <b>Skill Gap / Prerequisite:</b> {item["skill_gap"]}</div>', unsafe_allow_html=True)

                    if item.get("resolved_url"):
                        st.markdown(f'<a href="{item["resolved_url"]}" target="_blank" style="font-size:0.8rem; color:#a7f3d0;">Verified Resource Link ↗</a>', unsafe_allow_html=True)

                with col_btn:
                    btn_key = f"add_proposal_{agent_id}_{idx}_{item['reference_id']}"
                    # Check if already added
                    already_added = any(r["reference_id"] == item["reference_id"] for r in st.session_state.roadmap_items)
                    if already_added:
                        st.caption("✅ On Roadmap")
                    else:
                        if st.button("➕ Add", key=btn_key):
                            add_item_to_roadmap(item)


def add_item_to_roadmap(item):
    student_id = st.session_state.student_id
    db.insert_roadmap_items(student_id, [item])
    st.session_state.roadmap_items = db.get_roadmap_items(student_id)

    # Dynamic Agent Reaction in chat transcript
    reactions = agents.evaluate_roadmap_addition(student_id, item, get_current_profile(), st.session_state.roadmap_items)
    for agent_name, reaction in reactions.items():
        agent_code = "A" if "A" in agent_name else ("B" if "B" in agent_name else "C")
        st.session_state.chat_messages.append({"speaker": agent_name, "agent_id": agent_code, "content": reaction})
        db.save_chat_message(student_id, agent_name, reaction)

    st.toast(f"Added '{item['title']}' to your private roadmap!")
    st.rerun()


# ── Render Private Roadmap Panel ─────────────────────────────────────────
def render_roadmap_panel():
    st.markdown('<p class="roadmap-eyebrow">Personal Timeline</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-title">Your Private Roadmap</p>', unsafe_allow_html=True)

    items = st.session_state.roadmap_items
    if not items:
        st.info("Your roadmap is currently empty. Pick items from the Advisor Proposals or explore below to populate it!")
    else:
        horizon_order = {"now-open": 0, "active-contribution": 1, "next-horizon": 2}
        horizon_labels = {
            "now-open": "Now Open", "active-contribution": "Active Contribution", "next-horizon": "Next Horizon",
        }
        lane_badges = {"academic": "🎓 Academic", "professional": "💼 Professional"}

        ordered = sorted(items, key=lambda i: horizon_order.get(i["horizon"], 99))

        for idx, item in enumerate(ordered):
            st.markdown(
                f'''<div class="timeline-card">
                    <div class="horizon-label">{horizon_labels.get(item["horizon"], item["horizon"])}
                        · {lane_badges.get(item["lane"], item["lane"])}</div>
                    <b>{item["title"]}</b><br>
                    <span style="font-size:0.85rem;opacity:0.9;">{item["description"]}</span>
                </div>''',
                unsafe_allow_html=True,
            )
            if item.get("resolved_url"):
                st.markdown(
                    f'<a href="{item["resolved_url"]}" target="_blank" style="color:#e3d9ff; font-size:0.8rem;">Open verified link ↗</a>',
                    unsafe_allow_html=True,
                )

            col1, col2 = st.columns([1, 1])
            with col1:
                if item["claimed"]:
                    st.caption("✅ Completed")
                elif st.button("Mark Completed", key=f"claim_{item['id']}"):
                    db.claim_roadmap_item(item["id"])
                    st.session_state.roadmap_items = db.get_roadmap_items(st.session_state.student_id)
                    st.rerun()

    render_add_interest_section()


def render_add_interest_section():
    st.markdown("---")
    st.markdown("#### Explore More Catalog Topics")

    current = set(st.session_state.interests)
    available = [tag for tag in questions.INTEREST_LABELS if tag not in current]

    if available:
        col1, col2 = st.columns([2, 1])
        with col1:
            chosen_tag = st.selectbox(
                "Explore new domain",
                options=available,
                format_func=lambda t: questions.INTEREST_LABELS[t],
                label_visibility="collapsed",
            )
        with col2:
            if st.button("Add Topic"):
                institution_id = st.session_state.institution_id
                added = db.add_interest(st.session_state.student_id, institution_id, chosen_tag)
                db.add_interest_to_profile(st.session_state.student_id, chosen_tag)
                st.session_state.interests.append(chosen_tag)
                st.session_state.roadmap_items = db.get_roadmap_items(st.session_state.student_id)
                st.toast(f"Added {len(added)} items for {questions.INTEREST_LABELS[chosen_tag]}.")
                st.rerun()


# ── Main Render Layout ────────────────────────────────────────────────────
if st.session_state.blocked_reason:
    st.warning(f"**{SAFE_FALLBACK_TITLE}**\n\n{st.session_state.blocked_reason}")
    if st.button("Try again"):
        st.session_state.blocked_reason = None
        st.rerun()

elif not st.session_state.show_split_screen:
    # Full screen conversation before recommendations start
    render_chat_panel()

else:
    # Split screen layout: Chat + Proposals on Left, Private Roadmap on Right
    left_col, right_col = st.columns([3, 2])
    with left_col:
        render_chat_panel()
        render_advice_proposals()
    with right_col:
        render_roadmap_panel()
