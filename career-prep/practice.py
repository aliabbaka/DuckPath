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
