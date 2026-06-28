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
    # TODO Person A: data/analytics roles, more tech roles
    # TODO Person B: consulting/corporate roles (InterSECT, EntryLevel, MindSumo)
}

INTERVIEW_SIMULATORS = [
    {"name": "Interviews by AI", "link": "https://www.interviewsby.ai/"},
    {"name": "RightJoin AI Mock Interviews", "link": "https://rightjoin.co/"},
    # TODO Person B: verify these links are live before the demo
]


def get_simulations(role: str) -> list[dict]:
    """
    Match a free-typed role to curated simulations.

    TODO — Phase 7:
      - The user types free text ("SWE Intern at Meta") but keys are canonical
        ("software engineering internship"). See PLAN.md gap #6 — you need a small
        mapping step (keyword check, or reuse a role-category from analysis).
      - Return the matching list, or [] if no good match (UI shows a "search Forage
        / Kaggle directly" fallback — don't force a bad match).

    CONTRACT:
        returns: list[dict]   # each: {"name": str, "link": str}; [] = no match
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 7: implement get_simulations()")


if __name__ == "__main__":
    print(get_simulations("AI Engineer"))
