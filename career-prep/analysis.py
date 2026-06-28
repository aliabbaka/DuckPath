"""
Phase 3 — Extract skills and interview signals from postings.   OWNER: Person A + B (pair)

This is the "AI engineering" core, but it's really just: send the AI the postings,
tell it EXACTLY what shape of JSON to return, and parse it. No magic.

Person A: write + stress-test the prompt (Phase 3).
Person B: write the de-dup / ranking helper (Phase 3).
"""
import json
from collections import Counter
from llm import client
from config import LLM_MODEL


def analyze_postings(role: str, job_descriptions: list[str]) -> dict:
    """
    Ask the AI to read the postings and return skills + interview signals.

    TODO — Phase 3:

    1. Join the postings into one string (separate them with a divider like
       "\\n\\n---\\n\\n") so the model can tell them apart.

    2. Call client.chat.completions.create(...) with:
         - model=LLM_MODEL
         - a SYSTEM message that says: return a JSON object with exactly these keys:
             'core_skills'        -> list of specific technical skill names
             'interview_focus'    -> list of 3-5 short phrases about what gets tested
             'experience_signals' -> list of tools/certs postings keep asking for
           and "respond with ONLY valid JSON, no other text".
         - a USER message containing the role name and the combined postings.
         - response_format={"type": "json_object"}   # forces clean JSON

    3. The API gives you a STRING. Parse it with json.loads() and RETURN THE DICT.
       (Common bug: returning response.choices[0].message.content directly — that's
        a string, and app.py expects a dict it can do analysis["core_skills"] on.)

    CONTRACT:
        returns: {
            "core_skills":        list[str],
            "interview_focus":    list[str],
            "experience_signals": list[str],
        }
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 3: implement analyze_postings()")


def rank_skills(skill_lists: list[list[str]]) -> list[str]:
    """
    De-dup and rank skills by how often they appear across postings.   OWNER: Person B

    TODO — Phase 3:
      - Flatten all the skill lists into one list.
      - Normalize (e.g. .strip().lower()) so "Python " and "python" count as one.
      - Use collections.Counter to count, then return skill names ordered most-common
        first, with duplicates removed.

    CONTRACT:
        returns: list[str]   # unique skills, most-frequent first
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 3: implement rank_skills()")


if __name__ == "__main__":
    fake = [
        "We want Python, SQL, and strong communication. Pandas a plus.",
        "Looking for Python and SQL skills, plus experience with Git.",
    ]
    print(analyze_postings("Data Analyst", fake))
