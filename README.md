# DuckPath 

**An AI career-roadmap tool: type a target role ("AI Engineer", "SWE Intern at Meta")
and get a complete, free prep plan — the skills the role demands, how to learn each
one, projects to prove them, and how to network your way to a referral.**

Powered by a fine-tuned **DistilBERT** multi-label classifier, with **Streamlit** +
**Groq** (LLM) + **JSearch** (live job postings). In development for launch with
Whitman College's Career and Community Engagement Center (CCEC).
## The Model: Multi-Label Opportunity Classifier

DuckPath's core is a fine-tuned `distilbert-base-uncased` classifier that labels
CS career-opportunity descriptions across three dimensions simultaneously:
**[dimension 1]**, **[dimension 2]**, and **seniority level**.

### Dataset
- **4,636** opportunity descriptions collected via [your actual source, e.g., the JSearch API]
- Cleaned, deduplicated, and annotated for multi-label classification
- Train/validation/test split: [e.g., 70/15/15]
- A small sample is included at `model/data_sample.csv`; full dataset available on request

### Results (held-out test set)
| Metric | Value |
|---|---|
| Relevant-label capture across all dimensions | **83.45%** |
| False-positive rate | **2%** |
| F1 — seniority prediction | **91.71%** |

Full metrics: [`model/evaluation_results.json`](model/evaluation_results.json) ·
Confusion matrices: [`model/figures/`](model/figures/)

### Training setup
- Base model: `distilbert-base-uncased` (HuggingFace Transformers, Trainer API)
- Hardware: Google Colab [T4] GPU
- Key hyperparameters: learning rate [2e-5], batch size [16], epochs [N]
- Full training + evaluation code: [`model/duckpath_classifier.ipynb`](model/duckpath_classifier.ipynb)

### The lesson behind it
In an earlier project ([TakeMeter](https://github.com/aliabbaka/ai201-project3-takemeter)),
I watched fine-tuning collapse to the majority class on 50 imbalanced examples.
DuckPath applies that lesson at scale: [one honest sentence about what you did
differently — e.g., 4,636 examples and class weighting].
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
