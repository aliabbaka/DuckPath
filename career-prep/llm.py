"""
Shared LLM client.

Every module that asks the AI a question (analysis.py, projects.py, alt_paths.py)
imports `client` from here, so there is exactly ONE Groq client for the whole app
instead of each file creating its own. This mirrors how agent.py holds the single
client in the DuckPath reference project.

You should not need to edit this file.
"""
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
