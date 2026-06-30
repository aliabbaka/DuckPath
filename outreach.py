"""
Phase 8 — Networking and outreach layer.   OWNER: both (write the template together)

Mostly hand-written, not AI. The cold-email template should sound like a real human
wrote it, because one of you did. The LinkedIn search terms are simple string
templates you fill with the role/company.
"""

# Write this together in one sitting. Placeholders get filled by the user, not the AI.
COLD_EMAIL_TEMPLATE = """Hi {name},

I'm a student preparing to apply for {role} at {company}, and I came across {specific_detail}.

I'd love to hear about your experience on the team, specifically around {topic}.

Would you have 15 minutes sometime in the next couple weeks for a quick call?

Thanks for considering it,
{your_name}
"""

OUTREACH_QUESTIONS = [
    "What's one thing you wish you'd known before starting this role?",
    "What does a strong candidate's project portfolio usually look like for this team?",
    # TODO: add 2-3 more good ones (avoid "can you refer me" — it falls flat)
]


def build_outreach_kit(role: str, company: str = "the company") -> dict:
    """
    Assemble everything the networking section needs for one role.

    NOTE: app.py imports and calls this, but the roadmap never defined it
    (PLAN.md gap #4). This function IS the missing piece — build it here.

    TODO — Phase 8:
      - Build linkedin_terms: a list like
          f"{company} {role} alumni [your university]",
          f"{company} recruiter {role}",
          f"{company} {role} referral"
      - Return a dict bundling the search terms, the question list, and the template.

    CONTRACT:
        returns: {
            "linkedin_terms": list[str],
            "questions":      list[str],
            "email_template": str,   # COLD_EMAIL_TEMPLATE, shown in st.code() so it
                                     # gets a copy button for free
        }
    """
    return {
        "linkedin_terms": [
            f"{company} {role} alumni",
            f"{company} recruiter {role}",
            f"{company} {role} referral",
        ],
        "questions": OUTREACH_QUESTIONS,
        "email_template": COLD_EMAIL_TEMPLATE,
    }


if __name__ == "__main__":
    print(build_outreach_kit("AI Engineer", "Google"))
