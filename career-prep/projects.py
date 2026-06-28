"""
Phase 5 — "Prove it" layer: AI-generated project ideas.   OWNER: Person A

AI is allowed to improvise HERE because a project idea can't be "fake" the way a
URL can. Keep the prompt tight so ideas stay concrete and buildable.
"""
from llm import client
from config import LLM_MODEL


def generate_project_idea(skill: str, role: str) -> str:
    """
    Suggest one small, buildable portfolio project that proves `skill` for `role`.

    TODO — Phase 5:
      - client.chat.completions.create(model=LLM_MODEL, messages=[...])
      - SYSTEM: "Suggest ONE small portfolio project that demonstrates this skill,
        relevant to the target role. Name the actual tools. 2-3 sentences, buildable
        in under a week. Be concrete."
      - USER: f"Skill: {skill}\\nTarget role: {role}"
      - Return response.choices[0].message.content (plain text is fine here).

    CONTRACT:
        returns: str   # 2-3 sentence project idea
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 5: implement generate_project_idea()")


if __name__ == "__main__":
    print(generate_project_idea("SQL", "Data Analyst Intern"))
