"""
questions.py — the onboarding question flow.

Given everything answered so far, get_next_step() returns the next question
to show, or None once onboarding is done. Nothing in here touches the
database or Streamlit — app.py handles fetching data and drawing widgets.
Keeping this file "pure" (same answers in -> same question out, every time)
makes it easy to test on its own, which is exactly what the block at the
bottom of this file does.
"""

INTEREST_LABELS = {
    "ai-ml": "AI / Machine Learning",
    "cybersecurity": "Cybersecurity",
    "devops-systems": "DevOps / Systems",
    "web-mobile": "Web / Mobile Dev",
    "data-science": "Data Science",
    "theory-research": "Theory / Research",
}

# If a student picks multiple interests, Q2 branches on whichever of these
# comes first — cybersecurity and systems questions are the most
# discriminating signal, so they're checked first.
INTEREST_PRIORITY = [
    "cybersecurity", "ai-ml", "devops-systems", "data-science", "web-mobile", "theory-research",
]


def get_top_interest(interests):
    for interest in INTEREST_PRIORITY:
        if interest in interests:
            return interest
    return "web-mobile"


def background_step_id(interest):
    return f"background_{interest}"


def build_background_step(interest, course_options):
    """Phrases Q2 using the student's OWN school's real course codes,
    instead of naming one hardcoded course. Degrades to generic wording if
    the school hasn't tagged anything for this interest yet."""
    label = INTEREST_LABELS[interest]
    codes = course_options[:3]

    if not codes:
        return {
            "id": background_step_id(interest),
            "prompt": f"Have you taken any systems-level or {label} coursework yet?",
            "type": "single",
            "options": [("yes", "Yes, at least one course"), ("none", "Not yet")],
        }

    joined = " or ".join(c["code"] for c in codes)
    return {
        "id": background_step_id(interest),
        "prompt": f"Have you taken {joined}, or another {label.lower()} course?",
        "type": "single",
        "options": (
            [(c["id"], f"Yes — {c['code']}") for c in codes]
            + [("other", "Yes — a different course"), ("none", "Not yet")]
        ),
    }


def build_institution_step(institutions):
    return {
        "id": "institution",
        "prompt": "Which school are you at?",
        "type": "single",
        "options": [(i["id"], i["name"]) for i in institutions],
    }


STEP_YEAR = {
    "id": "year",
    "prompt": "What year are you?",
    "type": "single",
    "options": [
        ("first-year", "First-year"), ("sophomore", "Sophomore"),
        ("junior", "Junior"), ("senior", "Senior"),
    ],
}

STEP_INTERESTS = {
    "id": "interests",
    "prompt": "What's pulling your attention right now? Pick everything that fits.",
    "type": "multi",
    "options": list(INTEREST_LABELS.items()),
}

STEP_EXPERIENCE = {
    "id": "experience",
    "prompt": "Have you worked on a personal project, a class project you're proud of, or an internship?",
    "type": "single",
    "options": [
        ("internship", "Yes — an internship or co-op"),
        ("project", "Yes — a personal or class project"),
        ("none", "Not yet, and that's fine"),
    ],
}

STEP_INTERNSHIP_DETAIL = {
    "id": "experience_detail_internship",
    "prompt": "What did you work on there, in a sentence or two?",
    "type": "free-text",
    "options": [],
}


def get_next_step(answered, institutions, background_course_options):
    """answered: dict of question_id -> answer already given.
    Returns the next step dict to render, or None when onboarding is done."""
    if "institution" not in answered:
        return build_institution_step(institutions)
    if "year" not in answered:
        return STEP_YEAR
    if "interests" not in answered:
        return STEP_INTERESTS

    top_interest = get_top_interest(answered["interests"])
    bg_id = background_step_id(top_interest)
    if bg_id not in answered:
        return build_background_step(top_interest, background_course_options)

    if "experience" not in answered:
        return STEP_EXPERIENCE

    if answered["experience"] == "internship" and "experience_detail_internship" not in answered:
        return STEP_INTERNSHIP_DETAIL

    return None


def needs_course_context(answered):
    """True exactly when the NEXT unanswered step needs real course codes
    from the student's own school — lets app.py know when to query the
    database before rendering, instead of after."""
    if "institution" not in answered or "year" not in answered or "interests" not in answered:
        return False
    top_interest = get_top_interest(answered["interests"])
    return background_step_id(top_interest) not in answered


if __name__ == "__main__":
    # Quick manual trace through the whole flow — run with:
    #   python3 questions.py
    fake_institutions = [{"id": "whitman", "name": "Whitman College"}]
    fake_courses = [{"id": "whitman-cs270", "code": "CS 270"}, {"id": "whitman-cs301", "code": "CS 301"}]

    answered = {}
    print("Q:", get_next_step(answered, fake_institutions, [])["prompt"])
    answered["institution"] = "whitman"
    print("Q:", get_next_step(answered, fake_institutions, [])["prompt"])
    answered["year"] = "sophomore"
    print("Q:", get_next_step(answered, fake_institutions, [])["prompt"])
    answered["interests"] = ["cybersecurity"]

    assert needs_course_context(answered) is True
    step = get_next_step(answered, fake_institutions, fake_courses)
    print("Q:", step["prompt"])
    assert "CS 270" in step["prompt"]

    answered["background_cybersecurity"] = "whitman-cs270"
    print("Q:", get_next_step(answered, fake_institutions, [])["prompt"])
    answered["experience"] = "internship"
    print("Q:", get_next_step(answered, fake_institutions, [])["prompt"])
    answered["experience_detail_internship"] = "Built a small script."

    assert get_next_step(answered, fake_institutions, []) is None
    print("Onboarding complete — ALL CHECKS PASSED")
