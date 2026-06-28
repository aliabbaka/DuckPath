# Career Prep Map

Type a target role ("Google Internship", "AI Engineer", "SWE Intern at Meta") and
get back a complete, free prep plan: the skills the role demands, how to learn each
one free, project ideas to prove them, real job simulations, what interviewers test
for, and how to network your way to a referral.

Built with **Streamlit** + **Groq** (LLM) + **JSearch** (live job postings).

## Setup

```bash
# 1. virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. dependencies
pip install -r requirements.txt

# 3. API keys
cp .env.example .env            # then edit .env with your real keys
#   GROQ_API_KEY   -> https://console.groq.com/keys (free)
#   RAPIDAPI_KEY   -> subscribe to JSearch on https://rapidapi.com (free tier)

# 4. run
streamlit run app.py
```

## Project map

See [PLAN.md](PLAN.md) for the full build plan, task assignments, and the list of
what still needs to be built.

Each module can be tested on its own before wiring into the app:

```bash
python jobs.py          # test the job-postings fetch
python analysis.py      # test the AI skill extraction
python resources.py     # test the curated-resource lookup
# ...etc
```

> **Status:** scaffold. Functions raise `NotImplementedError` until you implement
> them (see the `TODO` blocks in each file and the gap table in PLAN.md).
