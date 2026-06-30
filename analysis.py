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
from llm import client, extract_json


# ================================================================================
# FUNCTION 1: COMMUNICATE WITH THE AI
# ================================================================================
# PRIMARY OWNER: Person A (The Driver) | REVIEWER: Person B (The Navigator)
def analyze_postings(role: str, job_descriptions: list[str]) -> dict:
    """Ask the AI to read the postings and return structured skills & signals."""
    # Guard Clause: If no job descriptions are provided, return an empty contract shape
    if not job_descriptions:
        return {"core_skills": [], "interview_focus": [], "experience_signals": []}

    # STEP 1.1: Bundle the listings cleanly using a markdown horizontal rule divider
    combined_postings = "\n\n---\n\n".join(job_descriptions)

    # STEP 1.2: Execute the structured inference call to the LLM Client API
    response = client.chat.completions.create(
        model=LLM_MODEL,
        response_format={"type": "json_object"},  # Enforce programmatic JSON formatting
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter. You must output a JSON "
                    "object with exactly these keys: "
                    "'core_skills' (a list of specific technical skill names as strings), "
                    "'interview_focus' (a list of 3-5 short phrases about what gets tested), "
                    "'experience_signals' (a list of tools or certifications requested). "
                    "Do not include any conversational intro or outro text. Respond "
                    "ONLY with valid JSON formatting."
                ),
            },
            {
                "role": "user",
                "content": f"Target Role: {role}\n\nJob Postings Data:\n{combined_postings}",
            },
        ],
    )

    # STEP 1.3: Extract the raw flat text string payload from the network message
    raw_json_string = response.choices[0].message.content

    # Deserialize the string text back into a functional Python dictionary
    analysis_data = extract_json(raw_json_string)

    return analysis_data


def analyze_role(role: str) -> dict:
    """Fallback analysis when no live job postings are found.

    Asks the AI to infer, from general knowledge, the skills a typical posting for
    this role/goal would require — so the app can still build a roadmap for any
    input (including free-form goals like "learn machine learning"). Returns the
    same contract shape as analyze_postings.
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter and career mentor. For the "
                    "given target role or learning goal, output a JSON object with "
                    "exactly these keys: "
                    "'core_skills' (a list of specific technical skill names as strings, "
                    "ordered from foundational to advanced), "
                    "'interview_focus' (a list of 3-5 short phrases about what gets tested), "
                    "'experience_signals' (a list of tools or certifications employers want). "
                    "Base it on what real job postings for this role typically require. "
                    "Respond ONLY with valid JSON, no extra text."
                ),
            },
            {"role": "user", "content": f"Target role or learning goal: {role}"},
        ],
    )
    return extract_json(response.choices[0].message.content)

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
    clean_skills = []
    for sublist in skill_lists:
        for skill in sublist:
            clean_skills.append(skill.strip().lower())
    # Step 2.2: COUNTER AND EXTRACT POPULARITY
    counts = Counter(clean_skills)
    return [skill for skill, _ in counts.most_common()]
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
