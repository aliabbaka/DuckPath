import os
from dotenv import load_dotenv

load_dotenv()

# Read keys from the local .env (via os.getenv) when running locally, or from
# Streamlit's secrets manager when deployed to Streamlit Cloud (where no .env
# exists). This makes the same code work in both places.
try:
    import streamlit as st
    _secrets = st.secrets
except Exception:
    _secrets = {}


def get_key(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        return _secrets.get(name)
    except Exception:
        return None


# --- LLM provider ---
# Prefer OpenRouter when its key is set; otherwise fall back to Groq. Both expose
# the same OpenAI-style chat.completions interface, so the calling code is unchanged.
OPENROUTER_API_KEY = get_key("OPENROUTER_API_KEY")
GROQ_API_KEY = get_key("GROQ_API_KEY")

if OPENROUTER_API_KEY:
    LLM_PROVIDER = "openrouter"
    LLM_MODEL = "meta-llama/llama-3.3-70b-instruct"   # add ':free' for the free tier
else:
    LLM_PROVIDER = "groq"
    LLM_MODEL = "llama-3.3-70b-versatile"

# --- Job postings API (JSearch via RapidAPI) ---
RAPIDAPI_KEY = get_key("RAPIDAPI_KEY")
JSEARCH_HOST = "jsearch.p.rapidapi.com"
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search-v2"

# How many postings to pull and feed to the AI. Keep this small while building —
# more postings = more tokens = slower + closer to rate limits.
POSTINGS_TO_ANALYZE = 5
