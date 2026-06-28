import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM (Groq — genuinely free tier) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# --- Job postings API (JSearch via RapidAPI) ---
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
JSEARCH_HOST = "jsearch.p.rapidapi.com"
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

# How many postings to pull and feed to the AI. Keep this small while building —
# more postings = more tokens = slower + closer to rate limits.
POSTINGS_TO_ANALYZE = 5
