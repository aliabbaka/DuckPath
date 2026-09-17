"""
agents.py — the three advisor personas.

Same three-agent design as before: each one only ever sees a short list of
REAL courses/resources pulled from db.py, and every reference it makes gets
double-checked against that exact list before it's shown to the student.
That double-check — not "the model being careful" — is what makes a
made-up link structurally impossible.
"""

import json
import os
import re

from groq import Groq

import db
from circuit_breaker import verify_agent_output, build_repair_prompt

# Groq retired its old Llama chat models (llama-3.3-70b-versatile and
# llama-3.1-8b-instant) — this is their current general-purpose replacement.
# If this stops working, run `python3 -c "from groq import Groq; print(Groq().models.list())"`
# to see what's live on your account right now.
MODEL = "openai/gpt-oss-120b"
MAX_REPAIR_PASSES = 2

_client = None


def get_client():
    """Created on first use, not at import time — so a missing
    GROQ_API_KEY doesn't crash the whole app before onboarding even
    renders. app.py wraps calls into this file in a try/except and shows a
    friendly message instead, the same fix you already made once in the
    AI201 project when a bad key returned a silent 401."""
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def call_groq(system, user):
    response = get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


def shared_rules(institution_name):
    return f"""
You are one of three advising personas inside AdvisorPath, a roadmap tool for
CS/STEM students at {institution_name}. You are given a student profile and a
CLOSED list of allowed course and resource candidates pulled live from
{institution_name}'s database.

Hard rules — breaking any of these causes your output to be discarded:
1. Cite ONLY items from the allowed candidate lists you are given. Never
   invent a course id or resource id that isn't in those lists.
2. Never print a raw http:// or https:// URL anywhere in your output.
   Reference a resource by wrapping its "id" field as a token:
   resourceToken = "[[RESOURCE:id]]". Reference a course by its "id" field
   directly in referenceId.
3. Output STRICTLY a JSON array, matching this shape per item:
   {{
     "title": string,
     "description": string,
     "referenceType": "course" or "resource",
     "referenceId": string,
     "resourceToken": string or null,
     "horizon": "now-open", "active-contribution", or "next-horizon"
   }}
   No prose, no markdown code fences, no commentary before or after the JSON.
4. If nothing in the candidate list genuinely fits, return an empty array
   rather than fabricating an item.
5. Recommend at most 4 items.
"""


def agent_a_system(institution_name):
    return shared_rules(institution_name) + """
PERSONA: Agent A — Academic Tracker ("Now Open").
Determine which core/major requirements are unlocked RIGHT NOW given the
student's completed courses and interests. Every item's "horizon" must be
"now-open" and "referenceType" must be "course".
"""


def agent_b_system(institution_name):
    return shared_rules(institution_name) + """
PERSONA: Agent B — Professional Matcher ("Active Contribution").
Match the student to real opportunities they can act on today from the
resource candidates. Every item's "horizon" must be "active-contribution"
and "referenceType" must be "resource".
"""


def agent_c_system(institution_name):
    return shared_rules(institution_name) + """
PERSONA: Agent C — Visionary Futurist ("Next Horizon").
Forecast what becomes available ONLY after the student finishes the roadmap
Agents A and B just proposed — advanced courses, niche job markets, stretch
projects. Every item's "horizon" must be "next-horizon".
"""


def fetch_candidates(profile):
    institutions = {i["id"]: i["name"] for i in db.get_institutions()}
    institution_name = institutions.get(profile["institution_id"], "the student's school")

    courses = db.get_courses(profile["institution_id"])
    courses = [c for c in courses if any(t in profile["interests"] for t in c["tags"])]

    resources = db.get_resources(tags=profile["interests"])

    return courses, resources, institution_name


def build_user_prompt(profile, courses, resources):
    resource_preview = [
        {"id": r["id"], "title": r["title"], "type": r["type"], "tags": r["tags"]} for r in resources
    ]
    return (
        f"STUDENT PROFILE:\n{json.dumps(profile, indent=2)}\n\n"
        f'ALLOWED COURSE CANDIDATES (cite "id" only, never invent one):\n'
        f"{json.dumps(courses, indent=2)}\n\n"
        f'ALLOWED RESOURCE CANDIDATES (cite "id" only, wrapped as [[RESOURCE:id]]):\n'
        f"{json.dumps(resource_preview, indent=2)}\n\n"
        "Return the JSON array now."
    )


def run_agent_with_repair(system_prompt, profile, courses, resources):
    base_prompt = build_user_prompt(profile, courses, resources)
    raw = call_groq(system_prompt, base_prompt)

    for attempt in range(MAX_REPAIR_PASSES + 1):
        is_valid, parsed, issues, parse_error = verify_agent_output(raw)
        if is_valid:
            return parsed
        if attempt == MAX_REPAIR_PASSES:
            return []  # circuit breaker: give up gracefully instead of showing bad data

        follow_up = (
            f"Your last response was not valid JSON ({parse_error}). Re-emit valid JSON only."
            if parse_error else build_repair_prompt(issues)
        )
        raw = call_groq(system_prompt, base_prompt + "\n\n---\n" + follow_up)

    return []


def resolve_against_candidates(item, courses, resources):
    """Defense-in-depth: look the cited id up in the EXACT list that was
    served to the model. If it's not there, drop the item — this is what
    makes a hallucinated link structurally impossible, independent of
    whether the model followed instructions."""
    if item.get("referenceType") == "course":
        match = next((c for c in courses if c["id"] == item.get("referenceId")), None)
        if not match:
            return None
        return {"canonical_id": match["id"], "title": match["title"], "resolved_url": None}

    token = item.get("resourceToken") or ""
    m = re.match(r"^\[\[RESOURCE:([a-z0-9_-]+)\]\]$", token, re.IGNORECASE)
    resource_id = m.group(1) if m else item.get("referenceId")
    match = next((r for r in resources if r["id"] == resource_id), None)
    if not match:
        return None
    return {"canonical_id": match["id"], "title": match["title"], "resolved_url": match["url"]}


def run_chat_agent(agent_id, messages, profile_context=None):
    """
    Generate dynamic conversation response for a specific agent persona (A, B, or C).
    agent_id: 'A' (Academic Tracker), 'B' (Professional Matcher), or 'C' (Visionary Futurist)
    messages: conversation transcript history list of {"role": "user"/"assistant", "speaker": "User"/"Agent A"/..., "content": str}
    """
    institution_id = profile_context.get("institution_id", "whitman") if profile_context else "whitman"
    institutions = {i["id"]: i["name"] for i in db.get_institutions()}
    inst_name = institutions.get(institution_id, "the university")

    agent_roles = {
        "A": (
            f"You are Agent A (Academic Tracker) at {inst_name}. "
            "Your job is to talk with the student, ask about their current academic standing, courses completed/enjoyed, "
            "and identify what foundational skills or core academic courses they need or have unlocked. Keep responses conversational, concise, friendly, and under 3-4 sentences."
        ),
        "B": (
            f"You are Agent B (Professional Matcher) at {inst_name}. "
            "Your job is to ask about practical interests, projects, hackathons, internships, or hands-on tools they want to test. "
            "Help match their aspirations with active real-world opportunities. Keep responses conversational, concise, energetic, and under 3-4 sentences."
        ),
        "C": (
            f"You are Agent C (Visionary Futurist) at {inst_name}. "
            "Your job is to ask about long-term vision, stretch goals, cutting-edge topics (AI, research, niche careers), "
            "and challenge the student to imagine what's next. Keep responses conversational, inspiring, concise, and under 3-4 sentences."
        ),
    }

    system_prompt = agent_roles.get(agent_id, agent_roles["A"])

    # Format transcript history into model messages
    formatted_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        speaker = m.get("speaker", "User")
        content = m.get("content", "")
        if speaker == "User":
            formatted_messages.append({"role": "user", "content": f"Student says: {content}"})
        else:
            formatted_messages.append({"role": "assistant", "content": f"{speaker}: {content}"})

    response = get_client().chat.completions.create(
        model=MODEL,
        messages=formatted_messages,
    )
    return response.choices[0].message.content.strip()


def generate_recommendations_proposal(profile, history=None):
    """
    Generates structured proposals from Agent A, B, and C categorized by:
    - What is suited & available now
    - Skill gap items (what requires learning a new skill first, with prerequisites/resources)
    - Next horizons
    All grounded strictly in SQLite catalog data.
    """
    courses, resources, institution_name = fetch_candidates(profile)

    agent_runs = [
        ("A", agent_a_system(institution_name)),
        ("B", agent_b_system(institution_name)),
        ("C", agent_c_system(institution_name)),
    ]

    proposals = {"A": [], "B": [], "C": []}
    for agent_id, system_prompt in agent_runs:
        items = run_agent_with_repair(system_prompt, profile, courses, resources)
        for item in items:
            resolved = resolve_against_candidates(item, courses, resources)
            if not resolved:
                continue

            # Check if there's a prerequisite / skill gap for courses
            skill_gap_info = None
            if item.get("referenceType") == "course":
                course_record = next((c for c in courses if c["id"] == resolved["canonical_id"]), None)
                if course_record and course_record.get("prerequisites"):
                    prereq_ids = course_record["prerequisites"]
                    completed = set(profile.get("completed_courses", []))
                    missing_prereqs = [p for p in prereq_ids if p not in completed]
                    if missing_prereqs:
                        # Find prerequisite titles
                        prereq_objs = [c for c in db.get_courses(profile["institution_id"]) if c["id"] in missing_prereqs]
                        prereq_names = ", ".join(c["code"] for c in prereq_objs) if prereq_objs else ", ".join(missing_prereqs)
                        skill_gap_info = f"Requires completing prerequisite skill/course first: {prereq_names}"

            proposals[agent_id].append({
                "lane": "professional" if agent_id == "B" else "academic",
                "horizon": item.get("horizon", "now-open"),
                "source_agent": agent_id,
                "title": item.get("title") or resolved["title"],
                "description": item.get("description", ""),
                "reference_type": item.get("referenceType"),
                "reference_id": resolved["canonical_id"],
                "resolved_url": resolved["resolved_url"],
                "skill_gap": skill_gap_info,
            })

    return proposals


def evaluate_roadmap_addition(student_id, newly_added_item, profile, current_roadmap):
    """
    Triggers dynamic agent reactions and suggestions when a student adds an item to their roadmap.
    Returns agent commentary dict mapping agent_id -> comment message.
    """
    courses, resources, institution_name = fetch_candidates(profile)

    item_title = newly_added_item.get("title", "this item")
    agent_source = newly_added_item.get("source_agent", "A")

    # Prompt Groq to produce dynamic follow-up commentary from all agents
    prompt = (
        f"The student at {institution_name} just added '{item_title}' (suggested by Agent {agent_source}) to their private roadmap!\n"
        f"Current roadmap items: {[i['title'] for i in current_roadmap]}\n\n"
        "Provide a short JSON object with reactions from Agent A, Agent B, and Agent C.\n"
        "Each agent should briefly comment (1-2 sentences) on how this choice builds their pathway or opens next steps.\n"
        'Format: {"Agent A": "...", "Agent B": "...", "Agent C": "..."}\n'
        "Return JSON strictly."
    )

    try:
        raw = call_groq("You are the multi-agent coordinator for AdvisorPath.", prompt)
        cleaned = re.sub(r"^```json\s*|```$", "", raw.strip()).strip()
        reactions = json.loads(cleaned)
        return reactions
    except Exception:
        return {
            "Agent A": f"Great pick! Adding '{item_title}' strengthens your academic foundation.",
            "Agent B": f"Adding '{item_title}' unlocks practical applications you can test in real projects.",
            "Agent C": f"With '{item_title}' on your roadmap, higher-level horizons and specializations start opening up!",
        }


def generate_roadmap(profile, student_id):
    courses, resources, institution_name = fetch_candidates(profile)

    agent_runs = [
        ("A", agent_a_system(institution_name)),
        ("B", agent_b_system(institution_name)),
        ("C", agent_c_system(institution_name)),
    ]

    all_rows = []
    for agent_id, system_prompt in agent_runs:
        items = run_agent_with_repair(system_prompt, profile, courses, resources)
        for item in items:
            resolved = resolve_against_candidates(item, courses, resources)
            if not resolved:
                continue  # hallucinated / unresolvable reference — drop it
            all_rows.append(
                {
                    "lane": "professional" if agent_id == "B" else "academic",
                    "horizon": item.get("horizon", "now-open"),
                    "source_agent": agent_id,
                    "title": item.get("title") or resolved["title"],
                    "description": item.get("description", ""),
                    "reference_type": item.get("referenceType"),
                    "reference_id": resolved["canonical_id"],
                    "resolved_url": resolved["resolved_url"],
                }
            )

    if all_rows:
        db.insert_roadmap_items(student_id, all_rows)
    return db.get_roadmap_items(student_id)
