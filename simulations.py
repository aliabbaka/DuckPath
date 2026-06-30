"""
Phase 7 — Job simulations layer.   OWNERS: Person A (tech tracks) + Person B (corporate/interview)

CURATED, not AI — the AI would invent simulations that don't exist. Point at each
platform's catalog/search page (with a "search '[Role]' here" note) rather than a
specific module title that may get retired.

Two SEPARATE things, kept apart on purpose:
  JOB_SIMULATIONS    = do a watered-down version of the actual job
  INTERVIEW_SIMULATORS = rehearse the hiring conversation
Don't merge them in the UI — they test different things.
"""

JOB_SIMULATIONS = {
    "ai engineer": [
        {"name": "Kaggle Learn (data/ML hands-on tracks)", "link": "https://www.kaggle.com/learn"},
        {"name": "Omdena (real collaborative ML challenges)", "link": "https://omdena.com/"},
        {"name": "Forage: AI/ML simulations (catalog rotates — search your role)", "link": "https://www.theforage.com"},
    ],
    "software engineering internship": [
        {"name": "Frontend Mentor (real design handoff + build)", "link": "https://www.frontendmentor.io/"},
        {"name": "GreatFrontEnd (frontend engineering challenges)", "link": "https://www.greatfrontend.com/"},
        {"name": "Forage: Software Engineering Job Simulation", "link": "https://www.theforage.com"},
    ],
    "data analyst": [
        {"name": "Kaggle Learn (data analysis tracks)", "link": "https://www.kaggle.com/learn"},
        {"name": "Mode Analytics SQL Tutorial (hands-on SQL practice)", "link": "https://mode.com/sql-tutorial/"},
        {"name": "Forage: Data Analytics Job Simulation", "link": "https://www.theforage.com"},
    ],
    "product manager": [
        {"name": "Product School Free Resources (product management exercises)", "link": "https://www.productschool.com/resources"},
        {"name": "MindSumo (real-world product challenges)", "link": "https://www.mindsumo.com/"},
        {"name": "Forage: Product Management Job Simulation", "link": "https://www.theforage.com"},
    ],
    "consulting analyst": [
        {"name": "InterSECT Consulting Challenges (real consulting case studies)", "link": "https://www.intersectconsulting.com/challenges"},
        {"name": "EntryLevel Consulting Simulations (case prep exercises)", "link": "https://www.entrylevelconsulting.com/simulations"},
        {"name": "Forage: Consulting Job Simulation", "link": "https://www.theforage.com"},
    ],
    "business analyst": [
        {"name": "Kaggle Learn (data analysis tracks)", "link": "https://www.kaggle.com/learn"},
        {"name": "MindSumo (real-world business challenges)", "link": "https://www.mindsumo.com/"},
        {"name": "Forage: Business Analyst Job Simulation", "link": "https://www.theforage.com"},
    ],
    "product designer": [
        {"name": "UX Collective (design challenges and case studies)", "link": "https://uxdesign.cc/"},
        {"name": "Daily UI (daily design prompts)", "link": "https://www.dailyui.co/"},
        {"name": "Forage: Product Design Job Simulation", "link": "https://www.theforage.com"},
    ],  
    "marketing analyst": [
        {"name": "HubSpot Academy (marketing analytics courses)", "link": "https://academy.hubspot.com/courses/marketing-analytics"},
        {"name": "Google Analytics Academy (free courses)", "link": "https://analytics.google.com/analytics/academy/"},
        {"name": "Forage: Marketing Analyst Job Simulation", "link": "https://www.theforage.com"},
    ],
    # TODO Person A: data/analytics roles, more tech roles
    # TODO Person B: consulting/corporate roles (InterSECT, EntryLevel, MindSumo)
}

INTERVIEW_SIMULATORS = [
    {"name": "Interviews by AI", "link": "https://www.interviewsby.ai/"},
    {"name": "RightJoin AI Mock Interviews", "link": "https://rightjoin.co/"},
    {"name": "Pramp (peer mock interviews)", "link": "https://www.pramp.com/"},
    {"name": "LeetCode Mock Interviews", "link": "https://leetcode.com/mock-interview/"},
    {"name": "Interviewing.io", "link": "https://interviewing.io/"},
    {"name": "TechCareers (AI-powered interview prep)", "link": "https://www.techcareers.com/"},
    {"name": "HackerRank (coding interview prep)", "link": "https://www.hackerrank.com/interview-preparation-kit"},
    {"name": "CodeSignal (general coding interview prep)", "link": "https://codesignal.com/"},
    # TODO Person B: verify these links are live before the demo
]


# Ordered keyword → canonical-key rules. First matching rule wins, so more
# specific phrases must come before broader ones (e.g. "business analyst" before
# the bare "analyst" fallback). Each tuple: (keywords-all-present, canonical key).
_ROLE_RULES = [
    (("ai",), "ai engineer"),
    (("ml",), "ai engineer"),
    (("machine", "learning"), "ai engineer"),
    (("data", "engineer"), "ai engineer"),
    (("data", "analyst"), "data analyst"),
    (("data", "scientist"), "data analyst"),
    (("business", "analyst"), "business analyst"),
    (("marketing",), "marketing analyst"),
    (("product", "manager"), "product manager"),
    (("product", "management"), "product manager"),
    (("pm",), "product manager"),
    (("product", "design"), "product designer"),
    (("ux",), "product designer"),
    (("ui",), "product designer"),
    (("designer",), "product designer"),
    (("consult",), "consulting analyst"),
    (("software",), "software engineering internship"),
    (("swe",), "software engineering internship"),
    (("frontend",), "software engineering internship"),
    (("front", "end"), "software engineering internship"),
    (("backend",), "software engineering internship"),
    (("full", "stack"), "software engineering internship"),
    (("developer",), "software engineering internship"),
    (("engineer",), "software engineering internship"),
]


def _canonical_role(role: str) -> str | None:
    """Map a free-typed role to a JOB_SIMULATIONS key, or None if nothing fits."""
    text = role.strip().lower()
    if not text:
        return None
    if text in JOB_SIMULATIONS:        # already canonical
        return text
    for keywords, key in _ROLE_RULES:
        if all(word in text for word in keywords):
            return key
    return None


def get_simulations(role: str) -> list[dict]:
    """
    Match a free-typed role to curated simulations.

    The user types free text ("SWE Intern at Meta") but keys are canonical
    ("software engineering internship"), so we run a keyword mapping step first.
    Returns the matching list, or [] if no good match (UI shows a "search Forage
    / Kaggle directly" fallback — don't force a bad match).

    CONTRACT:
        returns: list[dict]   # each: {"name": str, "link": str}; [] = no match
    """
    key = _canonical_role(role)
    if key is None:
        return []
    return JOB_SIMULATIONS.get(key, [])



if __name__ == "__main__":
    print(get_simulations("AI Engineer"))
