# AdvisorPath

A dynamic, profile-matching forecasting platform for college students with focus on CS/STEM
It is a three-agent, database-backed roadmap generator with a real circuit breaker instead of a static form.

## 1. Set up (5 minutes)

```bash
# 1. Install the three packages this needs
pip install -r requirements.txt --break-system-packages

# 2. Copy the env template and add your real Groq key
cp .env.example .env
# open .env and replace your_key_here with your real key from console.groq.com

# 3. Run it
streamlit run app.py
```

That's it — no account to make, no dashboard to configure. The first time
it runs, it creates `advisorpath.db` right next to the code and fills it
with two example schools (Whitman + a generic "Cascade State University")
so you can see the multi-school behavior immediately.

## 2. What's in each file

| File | What it does | Compare to your AI201 project |
|---|---|---|
| `app.py` | The whole UI — onboarding questions, then the dashboard. Run this one. | Your `app.py` |
| `db.py` | Creates and queries the local database (SQLite — built into Python). | Your `embed.py`/local ChromaDB folder, but for structured records instead of embeddings |
| `questions.py` | Decides which onboarding question comes next, based on what's been answered so far. Pure logic, no UI. | — new, but plain functions like the ones you already write |
| `circuit_breaker.py` | Blocks unsafe/off-topic answers; checks the AI's output for made-up links and asks it to fix them. | — new |
| `agents.py` | The three advisor personas, calling Groq. | Your `query.py` (grounded generation — same idea: never let the model answer from outside the data it was actually given) |
| `check_links.py` | Requests every URL in a resources CSV and fills in its `verified` column. | — new |
| `load_resources_csv.py` | Loads a cleaned, verified CSV into the database. | Replaces the old Supabase `resources_csv_to_sql.py` |
| `test_advisorpath.py` | The test suite — 55 tests over the four modules that don't need a network or a browser. | — new |

Run the tests any time with:

```bash
python3 -m unittest test_advisorpath -v
```

They cover the onboarding state machine, both circuit breaker layers, the
database helpers, and the CSV loader. Each database test builds its own
throwaway `.db` in a temp folder, so running them never touches your real
`advisorpath.db`. `agents.py` isn't covered (every path calls Groq) and
neither is `app.py` (it needs a live Streamlit session).

## 3. What's the same as before, just in different tools

- **Three advisors, not one chatbot.** Agent A checks what's unlocked now,
  Agent B finds things to do about it today, Agent C forecasts what opens up
  after. Same as the original design.
- **The AI can't send you a fake link.** Every course or resource it
  mentions has to match something real in `advisorpath.db` — if it makes up
  an id, `agents.py` silently drops that item instead of showing it to you.
  This got its own test (`Test 3` when this was built) proving a made-up
  course id gets thrown away, not displayed.
- **Bad input gets caught before it reaches the AI**, and **bad AI output
  gets a chance to fix itself** before you ever see it — same two-layer
  safety idea as before (`circuit_breaker.py`), just in plain Python.
- **Works for more than one school.** Pick "Cascade State University"
  during onboarding instead of Whitman and Q2 asks about *its* courses, not
  Whitman's — because it's reading from the database, not a hardcoded
  question.

## 4. Loading the real resource catalog

`db.py`'s `seed_if_empty()` only holds a handful of starter rows. The full
catalog lives in a CSV and gets loaded in two steps:

```bash
# 1. Check every link and fill in the `verified` column
python3 check_links.py resources_draft_PREVIEW.csv -o resources_cleaned.csv

# 2. Load the rows that passed
python3 load_resources_csv.py resources_cleaned.csv
```

Between those two steps is the part no script can do for you: reading the
rows and deciding which ones are actually worth a student's time, cutting
the ones flagged `duplicate_of_row`, and fixing titles the PDF extractor
mangled. `check_links.py` only tells you a URL *resolves* — a live link to
something irrelevant is still a row to delete.

A few things the loader deliberately refuses:

- **Rows with a blank `verified` column.** Nothing downstream re-checks a
  URL: `agents.py` verifies that a cited resource *exists in the database*,
  so a dead link in the database is a dead link shown to a student. Pass
  `--allow-unverified` to bypass this while testing. Rows explicitly marked
  `false` are never loaded, flag or not.
- **Rows whose URL is already in the database**, so re-running the loader
  is safe and nothing lands on a roadmap twice.
- **Rows with no recognized tag.** The only tags the app ever queries are
  the six onboarding interests (`ai-ml`, `cybersecurity`, `devops-systems`,
  `web-mobile`, `data-science`, `theory-research`). A row tagged anything
  else is invisible to every student, so it's skipped and reported.

To change the *courses* instead, edit the `courses` list in
`seed_if_empty()` (same shape: id, institution_id, code, title,
description, prerequisites, tags), delete `advisorpath.db`, and re-run.

## 5. Putting this on GitHub

Commit everything except what `.gitignore` already excludes.

- **Commit:** every `.py` file, `requirements.txt`, `.env.example`,
  `AdvisorPath-README.md`, `.gitignore`, and your cleaned resources CSV.
- **Never commit:** `.env` (your real key) or `advisorpath.db`.

Committing the cleaned CSV matters more than it looks. `advisorpath.db` is
gitignored and regenerates from `seed_if_empty()` alone, so the CSV is the
only copy of your resource catalog that actually travels with the repo.
Anyone cloning it runs the two commands in section 4 to rebuild the same
database you have.
