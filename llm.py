"""
Shared LLM client.

Every module that asks the AI a question (analysis.py, projects.py, alt_paths.py)
imports `client` from here, so there is exactly ONE client for the whole app
instead of each file creating its own.

The provider is chosen in config.py: OpenRouter if its key is set, otherwise Groq.
Both expose the same OpenAI-style `client.chat.completions.create(...)` interface,
so nothing downstream changes.
"""
import json
import re

from config import LLM_PROVIDER, OPENROUTER_API_KEY, GROQ_API_KEY

if LLM_PROVIDER == "openrouter":
    from openai import OpenAI
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
else:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)


def extract_json(text):
    """Parse a JSON object out of an LLM reply.

    Not every model honors response_format={"type": "json_object"} — some wrap the
    JSON in ```json fences or add prose like "Here is the JSON:". This tries the
    clean parse first, then strips fences, then falls back to the first {...} block.
    Raises ValueError if nothing parseable is found.
    """
    if not text:
        raise ValueError("Empty response from the model.")

    # 1. Clean parse.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Strip ```json ... ``` (or plain ```) fences, then retry.
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Grab the outermost {...} span and try that.
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from model reply: {text[:200]!r}")
