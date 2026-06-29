"""
Phase 5 — "Practice for free" layer.   OWNER: Person B

A small, stable, CURATED dictionary (not AI). "Where do I practice for free" has a
handful of good real answers that rarely change, so hardcoding them is correct.
"""

PRACTICE_RESOURCES = {
    "coding_interviews": [
        "NeetCode 150 (free)",
        "LeetCode free tier",
        "AlgoExpert free questions",
    ],
    "system_design": [
        "ByteByteGo free YouTube content",
        "System Design Primer (GitHub)",
    ],
    "behavioral": [
        "Pramp (free peer mock interviews)",
        "Big Interview's free trial questions",
    ],
    "resume_review": [
        "TopResume free resume review",
        "LinkedIn Resume Builder (free)",
    ],
    "mock_interviews": [
        "Pramp (free peer mock interviews)",
        "Interviewing.io (free anonymous mock interviews)",
    ],
    "product_design": [
        "Product Design Exercises (free resources)",
        "The Product Book (free chapters)",
    ],
    "data_structures": [
        "GeeksforGeeks free tutorials",
        "Khan Academy Data Structures (free)",
    ],
    "algorithms": [
        "MIT OpenCourseWare Algorithms (free)",
        "Coursera Algorithms Specialization (audit for free)",
    ],
    "databases": [
        "SQLZoo (free SQL tutorials)",
        "Mode Analytics SQL Tutorial (free)",
    ],
    "cloud_computing": [
        "AWS Free Tier (hands-on practice)",
        "Google Cloud Free Tier (hands-on practice)",
    ],
    "devops": [
        "Katacoda (free DevOps scenarios)",
        "Play with Docker (free practice environment)",
    ],
    "security": [
        "OWASP WebGoat (free security training)",
        "Hack The Box (free tier for practice)",
    ],
    "networking": [
        "Cisco Packet Tracer (free simulation tool)",
        "GNS3 (free network simulation software)",
    ],
    "machine_learning": [
        "Google Colab (free ML notebooks)",
        "Kaggle (free datasets and competitions)",
    ],
    "data_analysis": [
        "Pandas documentation (free tutorials)",
        "DataCamp free courses (limited access)",
    ],
    "web_development": [
        "freeCodeCamp (free web development curriculum)",
        "The Odin Project (free full-stack curriculum)",
    ],
    "mobile_development": [
        "Flutter documentation (free tutorials)",
        "React Native documentation (free tutorials)",
    ],
    "game_development": [
        "Unity Learn (free tutorials)",
        "Unreal Engine Online Learning (free courses)",
    ],
    "ai_and_ml": [
        "Fast.ai (free deep learning courses)",
        "DeepLearning.AI (free resources and courses)",
    ],
    "blockchain": [
        "CryptoZombies (free blockchain coding lessons)",
        "Ethereum.org Developer Resources (free)",
    ],
    "career_coaching": [
        "LinkedIn Career Advice (free mentorship)",
        "The Muse (free career resources)",
    ],
    "freelancing": [
        "Upwork Community (free resources for freelancers)",
        "Fiverr Learn (free courses for freelancers)",
    ],
    "entrepreneurship": [
        "Y Combinator Startup School (free online program)",
        "SBA Learning Center (free business courses)",
    ],
    "leadership": [
        "Harvard Business Review free articles on leadership",
        "MindTools Leadership Skills (free resources)",
    ],
    "competitive_programming": [
        "Codeforces (free competitive programming contests)",
        "AtCoder (free competitive programming contests)",
    ],
    "open_source_contribution": [
        "First Timers Only (free guide to contributing to open source)",
        "Up For Grabs (list of open source projects for beginners)",
    ],

    # TODO Person B: add more categories if your test roles need them
}


def get_practice(category: str) -> list[str]:
    """
    Return practice resources for a category (e.g. "coding_interviews").

    TODO — Phase 5:
      - Return PRACTICE_RESOURCES.get(category, []) — empty list if unknown.

    CONTRACT:
        returns: list[str]
    """
    # TODO: replace this stub
    raise NotImplementedError("Phase 5: implement get_practice()")


if __name__ == "__main__":
    print(get_practice("coding_interviews"))
