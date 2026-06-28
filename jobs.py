"""
================================================================================
PHASE 2: FETCH REAL JOB POSTINGS
================================================================================
OWNER: Person A (The Driver - writing code / Person B - The Navigator - checking docs)

WHAT ARE WE BUILDING?
This module connects our app to the live job market using an external API 
called 'JSearch' via RapidAPI. Its only job is to take a job title (like 
"Data Analyst") and return a clean list of job description text strings.

PAIR PROGRAMMING TIPS FOR BEGINNERS:
1. One person shares their screen and types (The Driver). 
2. The other person looks up the links provided and guides the logic (The Navigator).
3. Switch roles halfway through (e.g., after step 2)!
4. Talk out loud constantly. Say what you are typing and why.
"""

import requests
# These variables are imported from your local config.py file.
# They store secret keys and API endpoints safely so they aren't hardcoded here.
from config import JSEARCH_HOST, JSEARCH_URL, POSTINGS_TO_ANALYZE, RAPIDAPI_KEY


def fetch_postings(role: str) -> list[str]:
    """Fetch current job postings for a role and return their description text.

    LEARNING OBJECTIVES FOR THIS STEP:
    - How to use the Python 'requests' library to talk to the internet.
    - How to handle external server failures without crashing your own app.
    - How to dig through nested JSON data (dicts and lists).

    ----------------------------------------------------------------------------
    STEP 1: PREPARE AND SEND THE NETWORK REQUEST
    ----------------------------------------------------------------------------
    What to learn: API Headers and Parameters.
    - Headers act like your ID card or passport for the API server.
    - Parameters are the search filters (like what role to search for).
    
    Where to learn it:
    - Real Python guide: https://realpython.com

    How to code it:
    1. Create a dictionary called 'headers' containing:
       - "X-RapidAPI-Key": RAPIDAPI_KEY
       - "X-RapidAPI-Host": JSEARCH_HOST
    2. Create a dictionary called 'params' containing:
       - "query": role
       - "num_pages": "1"
    3. Wrap your network call in a 'try/except' block! The internet fails often.
       Catch 'requests.RequestException' so your app doesn't crash if offline.
    4. Make the call: response = requests.get(JSEARCH_URL, headers=headers, params=params)
    5. Check if it worked: if response.status_code != 200, return [] safely.

    ----------------------------------------------------------------------------
    STEP 2: PARSE THE JSON DATA (DATA MINING)
    ----------------------------------------------------------------------------
    What to learn: Navigating nested JSON responses.
    - External servers send back text that looks like a Python dictionary.
    - JSearch gives you a structure that looks exactly like this:
      {
         "status": "OK",
         "data": [
             {"job_description": "We are looking for a Python dev...", "title": "Dev"},
             {"job_description": "Must love data...", "title": "Data Analyst"}
         ]
      }

    Where to learn it:
    - Working with JSON in Python: https://realpython.com

    How to code it:
    1. Convert the raw response into a Python dictionary: data_dict = response.json()
    2. Safely check if the key "data" exists in that dictionary.
    3. If "data" is missing, or if it is an empty list, return [] immediately.
    
    *** SWAP ROLES HERE! Driver becomes Navigator, Navigator becomes Driver ***

    ----------------------------------------------------------------------------
    STEP 3: EXTRACT AND FILTER THE DESCRIPTIONS
    ----------------------------------------------------------------------------
    What to learn: List filtering, loops, and slicing boundaries.

    How to code it:
    1. Create an empty list to hold your clean results: descriptions = []
    2. Loop through every job item inside the "data" list.
    3. For each job, look up the key "job_description".
    4. If the description is missing, blank, or None, 'continue' to skip it.
    5. Otherwise, append the description text to your list.
    6. Stop or slice your list so it only returns up to the POSTINGS_TO_ANALYZE limit.

    ----------------------------------------------------------------------------
    THE OUTCOME CONTRACT:
    - MUST return a list of strings: ["desc 1", "desc 2"]
    - If anything fails (timeout, bad API key, no results), return an empty list: []
    ----------------------------------------------------------------------------
    """
    # TODO: Delete the two lines below and write your pair-programming solution here!
    raise NotImplementedError("Phase 2: implement fetch_postings()")


# ================================================================================
# LOCAL SMOKE TEST
# ================================================================================
# This block only runs when you execute THIS file directly (python jobs.py).
# It allows you to test your API code instantly without running the entire app UI.
if __name__ == "__main__":
    print("Testing your fetch_postings function...")

    # Test with a common role name
    test_role = "Software Engineering Internship"
    postings = fetch_postings(test_role)

    print("\n--- TEST RESULTS ---")
    print(f"Total postings fetched: {len(postings)}")

    if postings:
        print("\nSUCCESS! Successfully read data from the API.")
        print(f"First posting preview (First 300 characters):\n")
        print(postings[0][:300] + "...")
    else:
        print("\nFAILURE OR NO RESULTS.")
        print(
            "Returned an empty list. Check your internet, API keys, or logic."
        )
