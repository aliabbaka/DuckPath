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

    Calls the LLM and returns plain text — no JSON needed here because a project
    idea is narrative, not structured data.

    CONTRACT:
        returns: str   # 2-3 sentence project idea
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You suggest ONE small portfolio project that demonstrates a specific skill, "
                    "relevant to the target role. Name the actual tools and technologies to use. "
                    "Keep it to 2-3 sentences. It must be buildable in under a week by a student "
                    "with basic coding knowledge. Be concrete — no vague advice like 'build an app "
                    "that uses X'. Say exactly what the app does, what data it uses, what the tech stack should be, and what the "
                    "output looks like."
                ),
            },
            {
                "role": "user",
                "content": f"Skill: {skill}\nTarget role: {role}",
            },
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(generate_project_idea("SQL", "Data Analyst Intern"))
