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
    # TODO: replace this stub
    raise NotImplementedError("Phase 6: implement suggest_alt_paths()")


if __name__ == "__main__":
    print(suggest_alt_paths("Python", "AI Engineer"))
