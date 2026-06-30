"""
conftest.py — pytest loads this file automatically before any tests run.

WHY THIS FILE EXISTS:
    llm.py creates a Groq client the moment it's imported. The Groq client
    crashes if GROQ_API_KEY is not set — even in tests where we never actually
    call the API (because we mock it). Setting a fake key here satisfies the
    client's startup check so tests can import everything cleanly.

    The fake key is never sent to Groq — our mocks intercept all API calls
    before they leave the machine.
"""
import os

os.environ.setdefault("GROQ_API_KEY", "test-fake-key-not-real")
os.environ.setdefault("RAPIDAPI_KEY", "test-fake-key-not-real")
