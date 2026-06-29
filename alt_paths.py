"""
Phase 6 — "Other ways to prove yourself" layer.   OWNER: Person B

Five categories beyond projects. AI fills in specifics, but the prompt must force
CONCRETE answers ("fix a good-first-issue on the requests repo", not "contribute to
open source"). Person A tests on technical roles; Person B stress-tests on a role
where some categories don't fit (and makes the prompt degrade gracefully).
"""
import json
from llm import client
from config import LLM_MODEL


def suggest_alt_paths(skill: str, role: str) -> dict:
    """
    Suggest one concrete idea in each of five proof categories.

    TODO — Phase 6:
      - SYSTEM prompt: one concrete idea in EACH of these five, role-specific, as a
        JSON object with EXACTLY these keys:
            "open_source", "technical_writing", "community_leadership",
            "competitions", "devops_architecture"
        Tell it: for open source, point to GitHub's good-first-issue / help-wanted
        labels rather than naming one repo that may be dead. If a category doesn't
        fit the role, say so honestly instead of forcing a bad answer.
      - response_format={"type": "json_object"}
      - json.loads() the result and RETURN THE DICT (see analysis.py for the gotcha).

    CONTRACT:
        returns: {
            "open_source": str, "technical_writing": str,
            "community_leadership": str, "competitions": str,
            "devops_architecture": str,
        }
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert career coach. Suggest one concrete idea in EACH of "
                    "these five proof categories: 'open_source', 'technical_writing', "
                    "'community_leadership', 'competitions', 'devops_architecture'. "
                    "For open source, point to GitHub's good-first-issue / help-wanted "
                    "labels rather than naming one repo that may be dead. If a category "
                    "doesn't fit the role, say so honestly instead of forcing a bad answer. "
                    "Respond ONLY with valid JSON formatting."
                ),
            },
            {
                "role": "user",
                "content": f"Skill: {skill}\n\nRole: {role}",
            },
        ],
    )

    # Extract the raw JSON string from the response and deserialize it into a dict
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)


if __name__ == "__main__":
    print(suggest_alt_paths("Python", "AI Engineer"))
