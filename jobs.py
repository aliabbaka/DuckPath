"""
Phase 2 — Pull real job postings.   OWNER: Person A

This module is the app's only connection to the outside job market. It calls the
JSearch API (via RapidAPI) and hands back the *text* of real postings so the rest
of the app never has to know the API exists.

Keep this file focused on ONE job: turn a role name into a list of posting
description strings. Skill extraction happens later, in analysis.py.
"""
import requests
from config import RAPIDAPI_KEY, JSEARCH_HOST, JSEARCH_URL, POSTINGS_TO_ANALYZE


def fetch_postings(role: str) -> list[str]:
    """
    Fetch current job postings for `role` and return their description text.

    TODO — Phase 2:

    1. Build the request:
         headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": JSEARCH_HOST}
         params  = {"query": role, "num_pages": "1"}
       Call requests.get(JSEARCH_URL, headers=headers, params=params).

    2. Parse the response. JSearch returns JSON shaped like:
         {"status": "OK", "data": [ {"job_description": "...", ...}, ... ]}
       Pull the "job_description" string out of each item in data.

    3. Return at most POSTINGS_TO_ANALYZE descriptions as a list of strings.

    4. Handle the unhappy paths gracefully — DON'T let the app crash:
         - request fails / non-200  -> return []
         - "data" missing or empty   -> return []
         - a posting has no description -> skip it
       (The UI in app.py decides what message to show when this is empty.)

    CONTRACT (the rest of the app depends on this exact shape):
        returns: list[str]   # each item is one job's description text
                             # empty list means "no postings found / lookup failed"
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 2: implement fetch_postings()")


# Standalone smoke test — run `python jobs.py` to test THIS file without the UI.
if __name__ == "__main__":
    postings = fetch_postings("Software Engineering Internship")
    print(f"Got {len(postings)} postings")
    if postings:
        print("First posting (first 300 chars):\n", postings[0][:300])
