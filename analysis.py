"""
================================================================================
PHASE 3: AI SKILL EXTRACTION & DATA RANKING
================================================================================
OWNER: Person A & Person B (Collaborative Pair Programming)

WHAT ARE WE BUILDING?
This is the core "AI Engineering" module of the app. It does two jobs:
1. It bundles our job descriptions, sends them to an AI model, and forces the 
   AI to return clean, structured data instead of random conversational text.
2. It takes raw lists of skills, cleans them up (normalizes them), and ranks
   them by popularity so users know what skills matter most.

DIVISION OF LABOR FOR THIS PAIR SESSION:
- Person A (Driver for Function 1): Focuses on Prompt Engineering and AI communication.
- Person B (Driver for Function 2): Focuses on Python Data Wrangling and Aggregation.
- Both: Talk constantly out loud and review each other's code live!
"""

import json
from collections import Counter
from config import LLM_MODEL
from llm import client


# ================================================================================
# FUNCTION 1: COMMUNICATE WITH THE AI
# ================================================================================
# PRIMARY OWNER: Person A (The Driver) | REVIEWER: Person B (The Navigator)
def analyze_postings(role: str, job_descriptions: list[str]) -> dict:
    """Ask the AI to read the postings and return structured skills & signals.

    LEARNING OBJECTIVES FOR THIS STEP:
    - How to bundle unstructured text data cleanly for an AI prompt.
    - How to use Structured Outputs (`json_object`) to stop an AI from talking.
    - How to safely unpack stringified text back into an operational Python Dict.

    Where to learn it:
    - OpenAI Structured JSON Guide: https://openai.com

    ----------------------------------------------------------------------------
    STEP 1.1: BUNDLE THE POSTINGS
    ----------------------------------------------------------------------------
    What to do: Combine the separate job descriptions into one massive string.
    Why: The AI model processes text sequentially. Separating them with explicit
         visual markers prevents the AI from blending separate jobs together.
    How: Use `"\n\n---\n\n".join(job_descriptions)` to merge the list items.

    ----------------------------------------------------------------------------
    STEP 1.2: BUILD THE COMPLETION CALL
    ----------------------------------------------------------------------------
    What to do: Call `client.chat.completions.create(...)` using your configurations.
    Why: Passing `response_format={"type": "json_object"}` acts as an absolute 
         constraint on the model, forcing it to output clean JSON markup.
    
    How to configure the call:
    - model=LLM_MODEL
    - response_format={"type": "json_object"}
    - messages=[
         {
             "role": "system", 
             "content": (
                 "You are an expert technical recruiter. You must output a JSON "
                 "object with exactly these keys: "
                 "'core_skills' (a list of technical strings), "
                 "'interview_focus' (a list of 3-5 short phrases of what is tested), "
                 "'experience_signals' (a list of tools or certs explicitly requested). "
                 "Do not include any conversational intro or outro text. Respond "
                 "ONLY with valid JSON formatting."
             )
         },
         {
             "role": "user", 
             "content": f"Role: {role}\n\nJob Postings:\n{YOUR_COMBINED_STRING_HERE}"
         }
      ]

    ----------------------------------------------------------------------------
    STEP 1.3: EXTRACT AND UNPACK THE DATA
    ----------------------------------------------------------------------------
    What to do: Capture the text string from the response and run `json.loads()`.
    
    CRITICAL BEGINNER TRAP: 
    The AI data arrives inside `response.choices[0].message.content`. This looks 
    like a dictionary, but it is actually a standard, flat String! If you try 
    to read it using keys right away, your app will instantly crash.
    
    How to fix it: Pass that raw string into `json.loads(raw_string)`. This converts 
    it into an operational Python Dictionary that the rest of your app can read.

    CONTRACT OUTCOME:
    returns: {
        "core_skills": list[str],
        "interview_focus": list[str],
        "experience_signals": list[str]
    }
    """
    # TODO — Person A: Delete the stub below and implement the AI logic!
    raise NotImplementedError("Phase 3: implement analyze_postings()")


# ================================================================================
# FUNCTION 2: DE-DUPLICATE AND RANK THE TRACKED DATA
# ================================================================================
# PRIMARY OWNER: Person B (The Driver) | REVIEWER: Person A (The Navigator)
def rank_skills(skill_lists: list[list[str]]) -> list[str]:
    """De-duplicate and rank skills by frequency across all extractions.

    LEARNING OBJECTIVES FOR THIS STEP:
    - How to flatten nested lists (`[[a, b], [b, c]]` -> `[a, b, b, c]`).
    - Data normalization (removing whitespace and fixing casing discrepancies).
    - Utilizing high-utility standard library tools like `collections.Counter`.

    Where to learn it:
    - Python Counter Documentation: https://python.org

    ----------------------------------------------------------------------------
    STEP 2.1: FLATTEN AND CLEANSE THE DATA
    ----------------------------------------------------------------------------
    What to do: Take a list of lists (e.g., `[['Python', 'SQL'], ['python ', 'Git']]`) 
         and convert it into a single flat list where everything is standardized.
    Why: AI models can be unpredictable with styling. If one posting returns 
         "Python " (with a space) and another returns "python" (lowercase), Python 
         sees them as two completely unrelated things.
    How: 
    1. Create an empty list called `clean_skills = []`.
    2. Write a nested `for` loop: loop through each sublist, then loop through 
       each individual skill inside that sublist.
    3. For each skill, apply `.strip().lower()` to wipe out trailing spaces 
       and make the capitalization consistent. Append the result to `clean_skills`.

    ----------------------------------------------------------------------------
    STEP 2.2: COUNTER AND EXTRACT POPULARITY
    ----------------------------------------------------------------------------
    What to do: Track how many times each skill appears and sort them.
    Why: Manual tallying is error-prone. Python's built-in `Counter` objects
         handle calculations instantly and sort items automatically.
    How:
    1. Initialize your Counter: `counts = Counter(clean_skills)`
    2. Use `counts.most_common()` to extract the elements sorted by frequency.
    3. Use a list comprehension or loop to extract just the skill name from the 
       resulting tuples, leaving behind the numbers, and return that final list.

    CONTRACT OUTCOME:
    returns: list[str] -> A flat list of unique, lowercase strings ordered 
                          from the most common down to the least common.
    """
    # TODO — Person B: Delete the stub below and implement the ranking logic!
    raise NotImplementedError("Phase 3: implement rank_skills()")


# ================================================================================
# LOCAL SMOKE TEST
# ================================================================================
# Run `python analysis.py` directly in your terminal to test both functions.
if __name__ == "__main__":
    print("--- Running Phase 3 Tests ---\n")

    # 1. Test Mock Data for Person B's Sorting Function
    mock_extracted_skills = [
        ["Python", "SQL", "Communication"],
        ["python ", "AWS", "SQL"],
        ["Docker", "Python", "Kubernetes"],
    ]

    print("Testing rank_skills (Person B's section)...")
    try:
        ranked = rank_skills(mock_extracted_skills)
        print(f"Ranked Output: {ranked}")
        print("Expected Order: ['python', 'sql', 'communication', 'aws', 'docker', 'kubernetes']")
    except NotImplementedError:
        print("rank_skills() is still a placeholder stub.")

    print("\n------------------------------------------------")

    # 2. Test Live Prompt Execution for Person A's Section
    fake_descriptions = [
        "We want Python, SQL, and strong communication. Pandas experience is a big plus.",
        "Looking for an intern with Python and SQL skills, plus version control with Git.",
    ]

    print("Testing analyze_postings (Person A's section)...")
    try:
        analysis_result = analyze_postings("Data Analyst", fake_descriptions)
        print("\nSUCCESS! AI returned operational data structure:")
        print(json.dumps(analysis_result, indent=4))
    except NotImplementedError:
        print("analyze_postings() is still a placeholder stub.")
