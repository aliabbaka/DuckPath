"""
circuit_breaker.py — the same two safety checks from the design, just in
plain Python this time.

1. screen_input()        — runs on every onboarding answer, catching
                            requests to do graded schoolwork, anything
                            unsafe, or attempts to override instructions.
2. verify_agent_output()  — runs on every agent's raw response. If it finds
                            a raw http(s):// link where a structured
                            [[RESOURCE:id]] token belongs, build_repair_prompt()
                            builds the follow-up message that gets sent back
                            to the model to fix it.
"""

import json
import re

ACADEMIC_DISHONESTY_PATTERNS = [
    r"write (my|this|the) (essay|paper|thesis|assignment|homework)\b",
    r"do (my|this) (homework|assignment|exam|test)\b",
    r"take my (exam|quiz|test|proctored)",
    r"solve (my|this) (problem set|pset|assignment)\b",
    r"(answers?|solutions?) to (the|my) (exam|midterm|final|quiz)",
    r"bypass (turnitin|plagiarism|the proctor)",
]

ILLEGAL_OR_UNSAFE_PATTERNS = [
    r"how (do|to) (i |you )?(hack|breach|exploit)\s+(the school|the registrar|canvas|the lms)",
    r"(steal|leak) (grades|transcripts|student records|ferpa)",
    r"\b(malware|ransomware|keylogger|ddos)\b",
    r"make (a )?(bomb|weapon|explosive)",
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all|any|the) (previous|prior|above) instructions",
    r"you are now (in )?(dan|developer) mode",
    r"reveal your (system prompt|instructions)",
]

SAFE_FALLBACK_TITLE = "Let's keep this about your roadmap"
SAFE_FALLBACK_BODY = "Try rephrasing your answer around what you've done, or what you're hoping to do next."


def _matches_any(text, patterns):
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def screen_input(text):
    """Returns (is_safe, reason). reason is None when is_safe is True."""
    if not text or not text.strip():
        return True, None
    if _matches_any(text, ACADEMIC_DISHONESTY_PATTERNS):
        return False, ("That reads like a request to complete graded academic work on your "
                        "behalf — AdvisorPath only helps you plan, not submit work for you.")
    if _matches_any(text, ILLEGAL_OR_UNSAFE_PATTERNS):
        return False, "That touches on unsafe or unauthorized activity, so AdvisorPath can't act on it."
    if _matches_any(text, PROMPT_INJECTION_PATTERNS):
        return False, "That looks like an attempt to override system instructions rather than an onboarding answer."
    return True, None


RAW_URL_PATTERN = re.compile(r"https?://\S+")
RESOURCE_TOKEN_PATTERN = re.compile(r"^\[\[RESOURCE:[a-z0-9_-]+\]\]$", re.IGNORECASE)


def verify_agent_output(raw_text):
    """Parses the model's raw text as JSON and checks every string field for
    a bare URL. Returns (is_valid, parsed_list_or_None, issues, parse_error).
    issues is a list of (item_index, field_name, bad_value) tuples."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json\s*|```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
        if not isinstance(parsed, list):
            parsed = [parsed]
    except json.JSONDecodeError as e:
        return False, None, [], str(e)

    issues = []
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            continue
        for field, value in item.items():
            if not isinstance(value, str):
                continue
            if RAW_URL_PATTERN.search(value):
                issues.append((i, field, value))
                continue
            if field == "resourceToken" and value and not RESOURCE_TOKEN_PATTERN.match(value):
                issues.append((i, field, value))

    return (len(issues) == 0), parsed, issues, None


def build_repair_prompt(issues):
    lines = "\n".join(
        f'- item[{i}].{field} = "{value}" is a raw string, not a token' for i, field, value in issues
    )
    return (
        "Your previous JSON output was rejected by output verification because it "
        "contained raw strings instead of structured reference tokens:\n"
        f"{lines}\n\n"
        "Re-emit the FULL corrected JSON array. Every resource reference must be a "
        "`[[RESOURCE:id]]` token using an id from the candidate list you were given. "
        "Never print a bare http(s):// URL. Return JSON only — no prose, no markdown fences."
    )
