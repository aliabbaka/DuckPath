"""
Phase 4 — "How to learn this, for free" layer.   OWNERS: Person A (fundamentals) + Person B (specialized)

This is a CURATED dictionary, not AI output. The AI invents fake course names and
URLs; this file is the trustworthy source. The AI's job (later) is only to produce
skills — THIS file decides what's real.

IMPORTANT (see PLAN.md gap #5): skills come back from the AI with messy names
("Data Analysis", "data analysis", "Pandas"). Match through normalize_skill() +
get_resources(), NOT a raw dict[skill] lookup, or almost everything will "miss".

⚠️ Both people edit this same file. Either work on ONE shared branch for this phase,
or merge one person's entries in before the other starts. See PLAN.md git notes.

The `free_certificate` flag must be honest:
    True  = course AND certificate are free
    False = course is free to take ("audit"), certificate costs money
    None  = no formal certificate exists
"""

LEARNING_RESOURCES = {
    # ── Person A: fundamentals (Python, Git, DSA, SQL) ──
    "python": {
        "docs": "https://docs.python.org/3/tutorial/ — sections 3 to 5 only",
        "video": "Corey Schafer's Python OOP series on YouTube",
        "course": "freeCodeCamp's Scientific Computing with Python certification",
        "free_certificate": True,
    },
    # TODO Person A: add git, data structures & algorithms, sql

    # ── Person B: specialized (System Design, ML/AI, Cloud, Frontend) ──
    "data analysis": {
        "docs": "https://pandas.pydata.org/docs/user_guide/10min.html",
        "video": "freeCodeCamp's Pandas tutorial on YouTube",
        "course": "Coursera's IBM Data Analyst course (audit free, certificate paid)",
        "free_certificate": False,
    },
    # TODO Person B: add system design, ml/ai tooling, cloud (aws basics), react/frontend
}


def normalize_skill(skill: str) -> str:
    """Lowercase + strip so AI skill names match dictionary keys. OWNER: whoever pairs first."""
    return skill.strip().lower()


def get_resources(skill: str) -> dict | None:
    """
    Look up curated resources for a skill.

    TODO — Phase 4:
      - Normalize the incoming skill with normalize_skill().
      - Return LEARNING_RESOURCES[key] if present, else None.
      - (Stretch: handle simple aliases, e.g. "py" -> "python".)

    CONTRACT:
        returns: dict (the resource entry) OR None if not curated yet.
                 app.py shows a friendly "not curated yet" message on None.
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 4: implement get_resources()")


if __name__ == "__main__":
    print(get_resources("Python"))        # should find it
    print(get_resources("Quantum Magic"))  # should be None
