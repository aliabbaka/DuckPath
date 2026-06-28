# Career Prep Map — Build Plan

A two-person Streamlit app: type a target role, get a complete free prep plan
(skills → learn → prove → simulate → interview → network).

This file is the source of truth for **who builds what, in what order, and what's
still missing**. Read it before each work session.

---

## 1. File structure (one file ≈ one phase ≈ one owner)

The structure mirrors the DuckPath reference: a thin UI, a config file, shared LLM
client, AI-orchestration modules, and curated-data modules. Splitting by file is
deliberate — if Person A is in `projects.py` and Person B is in `simulations.py`,
Git never has to reconcile the same lines.

| File | Phase | Does | Owner |
|------|-------|------|-------|
| `config.py` | 0 | env vars + constants | done ✅ |
| `llm.py` | 0 | one shared Groq client | done ✅ |
| `jobs.py` | 2 | fetch real postings from JSearch | **A** |
| `analysis.py` | 3 | AI: postings → skills + interview signals | **A + B (pair)** |
| `resources.py` | 4 | curated: how to learn each skill free | **A** (fundamentals) + **B** (specialized) |
| `projects.py` | 5 | AI: project idea per skill | **A** |
| `practice.py` | 5 | curated: where to practice free | **B** |
| `alt_paths.py` | 6 | AI: 5 non-project proof paths | **B** |
| `simulations.py` | 7 | curated: job sims + mock interviews | **A** (tech) + **B** (corporate) |
| `outreach.py` | 8 | networking kit + cold email | **both** |
| `app.py` | 9–10 | wire it all together + polish | **both (Live Share)** |

Curated data lives as Python dicts inside the modules (roadmap style), not in
`data/*.json`. That's the one intentional difference from DuckPath — simpler for now.

---

## 2. Build order (dependencies — don't build out of order)

```
config.py ✅  llm.py ✅
        │
        ▼
   jobs.py (P2) ──► analysis.py (P3) ─────────────┐
                                                  │ app.py needs these
   resources.py (P4)   projects.py (P5)           │ wired LAST
   practice.py (P5)    alt_paths.py (P6)  ────────►  app.py (P9-10)
   simulations.py (P7) outreach.py (P8)            │
                                                  ┘
```

- **Phases 2 → 3 are the spine** and must come first — nothing else has data without them.
- Phases 4–8 are **independent of each other** → this is where the two of you split
  and work in parallel on separate files/branches.
- `app.py` is wired only once 4–8 exist. Until then, test each module standalone:
  every module has an `if __name__ == "__main__":` smoke test — run `python jobs.py`,
  `python resources.py`, etc. to test your file without touching the UI.

---

## 3. The contracts (agree on these — they're how parallel work stays compatible)

Each function's exact return shape is written in its docstring. The ones app.py
depends on, summarized:

- `fetch_postings(role) -> list[str]`  (empty list = none found)
- `analyze_postings(role, postings) -> {"core_skills":[...], "interview_focus":[...], "experience_signals":[...]}`  **(a dict, not a string!)**
- `get_resources(skill) -> dict | None`
- `generate_project_idea(skill, role) -> str`
- `suggest_alt_paths(skill, role) -> dict` (5 fixed keys)
- `get_simulations(role) -> list[dict]`  (each `{"name","link"}`; `[]` = no match)
- `build_outreach_kit(role) -> {"linkedin_terms":[...], "questions":[...], "email_template": str}`

If you need to change a contract, change it here + tell the other person *before* coding.

---

## 4. Git workflow (the rule, short version)

1. Never commit to `main` (branch protection is on).
2. One branch per phase, named after the file: `jobs-fetch-postings`, `simulations-data`.
3. Commit small, specific messages.
4. Push → open PR → **the other person reviews the diff** → merge → both pull `main`.
5. **`resources.py` exception:** you both edit it (Phase 4). Work on ONE shared branch
   for that phase, OR merge one person's entries before the other starts — don't both
   edit it on separate branches for days.
6. **`app.py` (Phase 9):** one shared branch + **Live Share**, build it together.

---

## 5. What's missing / gaps to build (this is the "homework")

Everything above is scaffolding with `NotImplementedError` stubs. Here's what still
needs real code or decisions — including a few places the original roadmap had gaps:

| # | Gap | Where | Why it matters |
|---|-----|-------|----------------|
| 1 | `fetch_postings` body — extract `job_description`, handle errors/empty | `jobs.py` | roadmap only showed a print-script, never a reusable function |
| 2 | **Parse the AI JSON.** `analyze_postings` must `json.loads()` and return a **dict** | `analysis.py` | roadmap's app.py did `analysis["core_skills"]` on a **string** — would crash |
| 3 | `rank_skills` de-dup/ranking helper | `analysis.py` | postings repeat skills; needs Counter |
| 4 | **`build_outreach_kit` didn't exist** — app.py imported it but Phase 8 never defined it | `outreach.py` | stubbed for you; implement it |
| 5 | **Skill-name matching.** AI returns "Data Analysis"/"pandas"; dict keys won't match raw | `resources.py` | without normalize + matching, almost every skill shows "not curated" |
| 6 | **Role matching.** User types "SWE Intern at Meta"; sim keys are canonical | `simulations.py` | needs a keyword/category mapping step |
| 7 | **Caching.** Streamlit reruns everything each click; AI calls re-fire & cost time | `app.py` | wrap slow calls in `@st.cache_data` |
| 8 | Error/empty states (blank role, bad API key, no postings) | `app.py` | Phase 10 |
| 9 | Cold email template — write it by hand, together | `outreach.py` | the one part AI shouldn't write |
| 10 | Deployment secrets (Streamlit Cloud "Secrets" panel replaces `.env`) | Phase 11 | `.env` is gitignored, won't deploy |
| 11 | Grow curated dicts to the ~15–20 skills / 5–6 roles your testing actually surfaces | resources/simulations | don't over-build; grow from real Phase 2 output |

Recommended order to close them: **1 → 2 → 3** (get the spine working end-to-end with
hardcoded data), then **5 → 4 → 6**, then **7 → 8**, then **9–11** polish/ship.

---

## 6. API keys you need (free)

- **Groq** (LLM): https://console.groq.com/keys
- **JSearch** (jobs): subscribe to the free tier on https://rapidapi.com (search "JSearch")

Put both in `.env` (copy `.env.example`). Never commit `.env`.
