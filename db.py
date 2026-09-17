"""
db.py — local database for AdvisorPath.

Uses SQLite (built straight into Python — no server, no account, no
dashboard). The whole database is one file, advisorpath.db, created
automatically the first time you run the app, sitting right next to this
code — the same idea as the local ChromaDB folder in your AI201 project,
just for structured records instead of embeddings.

Five tables:
  institutions      one row per school
  courses           scoped to one institution (institution_id column)
  resources         global — CodePath, open-source, YouTube, etc. apply to
                     any student at any school, so these aren't scoped
  student_profiles  one row per completed onboarding
  roadmap_items     the agents' recommendations, one row each

SQLite has no array type, so `tags` and `prerequisites` are stored as plain
comma-separated text (e.g. "cybersecurity,devops-systems") and split back
into a Python list wherever they're read.
"""

import sqlite3
import uuid
from datetime import datetime, timezone

DB_PATH = "advisorpath.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read each row like a dict
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS institutions (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            institution_id TEXT NOT NULL,
            code TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            prerequisites TEXT DEFAULT '',
            tags TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS resources (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            tags TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS student_profiles (
            id TEXT PRIMARY KEY,
            institution_id TEXT NOT NULL,
            year TEXT NOT NULL,
            interests TEXT NOT NULL,
            completed_courses TEXT DEFAULT '',
            experience_level TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS roadmap_items (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            lane TEXT NOT NULL,
            horizon TEXT NOT NULL,
            source_agent TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            reference_type TEXT NOT NULL,
            reference_id TEXT NOT NULL,
            resolved_url TEXT,
            claimed INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chat_transcripts (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            speaker TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def seed_if_empty():
    """Fills in two schools plus starter courses/resources — but only the
    very first time. Safe to call on every app startup."""
    conn = get_connection()
    already_seeded = conn.execute("SELECT COUNT(*) FROM institutions").fetchone()[0] > 0
    if already_seeded:
        conn.close()
        return

    conn.executemany(
        "INSERT INTO institutions (id, name) VALUES (?, ?)",
        [
            ("whitman", "Whitman College"),
            ("cascade", "Cascade State University"),
        ],
    )

    conn.executemany(
        "INSERT INTO courses (id, institution_id, code, title, description, prerequisites, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("whitman-cs167", "whitman", "CS 167", "Introduction to Computer Science",
             "Intro programming and problem solving.", "", "web-mobile,ai-ml,devops-systems"),
            ("whitman-cs210", "whitman", "CS 210", "Data Structures",
             "Core data structures and algorithmic analysis.", "whitman-cs167",
             "ai-ml,theory-research,data-science"),
            ("whitman-cs270", "whitman", "CS 270", "Systems Programming",
             "Memory, processes, and low-level systems programming.", "whitman-cs210",
             "cybersecurity,devops-systems"),
            ("whitman-cs301", "whitman", "CS 301", "Computer Networks",
             "Network protocols and security fundamentals.", "whitman-cs270",
             "cybersecurity,devops-systems"),
            ("whitman-cs320", "whitman", "CS 320", "Machine Learning",
             "Applied ML models and evaluation.", "whitman-cs210", "ai-ml,data-science"),
            ("cascade-cs101", "cascade", "CS 101", "Foundations of Programming",
             "Intro programming in a general CS curriculum.", "", "web-mobile,ai-ml,devops-systems"),
            ("cascade-cs220", "cascade", "CS 220", "Operating Systems & Security",
             "Systems fundamentals with a security module.", "cascade-cs101",
             "cybersecurity,devops-systems"),
            ("cascade-cs315", "cascade", "CS 315", "Applied Machine Learning",
             "Applied ML models and evaluation.", "cascade-cs101", "ai-ml,data-science"),
        ],
    )

    conn.executemany(
        "INSERT INTO resources (id, title, type, url, description, tags) VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("codepath-cyb101", "CodePath CYB101 — Intro to Cybersecurity", "codepath_track",
             "https://www.codepath.org/courses/cybersecurity",
             "No-cost, open to all majors, offensive/defensive security foundations.", "cybersecurity"),
            ("codepath-web101", "CodePath WEB101 — Intro to Web Development", "codepath_track",
             "https://www.codepath.org/courses/web-development",
             "No-cost, open to all majors, HTML/CSS/JS foundations.", "web-mobile"),
            ("codepath-ai110", "CodePath AI110 — Applied AI Engineering: Foundations", "codepath_track",
             "https://www.codepath.org/courses/applied-ai-engineering",
             "Reinforces CS fundamentals while building with AI tools.", "ai-ml,devops-systems"),
            ("codepath-tip102", "CodePath TIP102 — Technical Interview Prep", "codepath_track",
             "https://www.codepath.org/courses/technical-interview-prep",
             "Algorithmic interview prep and communication practice.",
             "ai-ml,cybersecurity,devops-systems,web-mobile,data-science,theory-research"),
            ("picoctf", "picoCTF", "competition",
             "https://picoctf.org",
             "Free, beginner-friendly capture-the-flag challenges run by Carnegie Mellon — "
             "the standard place to actually test cybersecurity skills, not just read about them.",
             "cybersecurity"),
            ("leetcode", "LeetCode", "competition",
             "https://leetcode.com",
             "Timed, graded coding problems — the standard way to test yourself on data "
             "structures and algorithms before an internship or technical interview.",
             "ai-ml,devops-systems,web-mobile,data-science,theory-research"),
        ],
    )

    conn.commit()
    conn.close()


def _split(csv_text):
    return [t.strip() for t in (csv_text or "").split(",") if t.strip()]


def get_institutions():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM institutions ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_courses(institution_id, tag=None):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM courses WHERE institution_id = ?", (institution_id,)
    ).fetchall()
    conn.close()
    courses = [dict(r) for r in rows]
    for c in courses:
        c["tags"] = _split(c["tags"])
        c["prerequisites"] = _split(c["prerequisites"])
    if tag:
        courses = [c for c in courses if tag in c["tags"]]
    return courses


def get_resources(tags=None):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM resources").fetchall()
    conn.close()
    resources = [dict(r) for r in rows]
    for r in resources:
        r["tags"] = _split(r["tags"])
    if tags:
        resources = [r for r in resources if any(t in r["tags"] for t in tags)]
    return resources


def insert_student_profile(institution_id, year, interests, completed_courses, experience_level):
    student_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO student_profiles "
        "(id, institution_id, year, interests, completed_courses, experience_level, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            student_id, institution_id, year, ",".join(interests), ",".join(completed_courses),
            experience_level, datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
    return student_id


def insert_roadmap_items(student_id, items):
    """items: list of dicts with lane, horizon, source_agent, title,
    description, reference_type, reference_id, resolved_url."""
    conn = get_connection()
    for item in items:
        conn.execute(
            "INSERT INTO roadmap_items "
            "(id, student_id, lane, horizon, source_agent, title, description, "
            "reference_type, reference_id, resolved_url, claimed) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)",
            (
                str(uuid.uuid4()), student_id, item["lane"], item["horizon"], item["source_agent"],
                item["title"], item["description"], item["reference_type"], item["reference_id"],
                item["resolved_url"],
            ),
        )
    conn.commit()
    conn.close()


def get_roadmap_items(student_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM roadmap_items WHERE student_id = ?", (student_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def claim_roadmap_item(item_id):
    conn = get_connection()
    conn.execute("UPDATE roadmap_items SET claimed = 1 WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


def add_interest_to_profile(student_id, tag):
    """Appends a new tag to a student's stored interests, if it isn't
    already there. Doesn't touch roadmap_items — see add_interest() below
    for that."""
    conn = get_connection()
    row = conn.execute(
        "SELECT interests FROM student_profiles WHERE id = ?", (student_id,)
    ).fetchone()
    interests = _split(row["interests"]) if row else []
    if tag not in interests:
        interests.append(tag)
        conn.execute(
            "UPDATE student_profiles SET interests = ? WHERE id = ?",
            (",".join(interests), student_id),
        )
        conn.commit()
    conn.close()


def add_interest(student_id, institution_id, tag):
    """When a student adds a new interest on the dashboard, this is what
    runs — and notice it never calls Groq. Adding an interest isn't
    generating new advice, it's looking up rows that already exist in the
    database, so a plain query does the job; no AI call needed.

    First batch only: courses tagged with this interest ("what to learn")
    and any 'competition'-type resources tagged with it ("what you can
    test yourself on"). Other resource types are held back for
    reveal_more_resources() below, so this doesn't dump everything at once.
    Anything already on the student's roadmap is skipped.
    """
    existing_ids = {item["reference_id"] for item in get_roadmap_items(student_id)}
    new_rows = []

    for course in get_courses(institution_id, tag=tag):
        if course["id"] in existing_ids:
            continue
        new_rows.append(
            {
                "lane": "academic",
                "horizon": "now-open",
                "source_agent": "catalog",  # not AI-generated — a direct database match
                "title": f"Learn: {course['code']} — {course['title']}",
                "description": course["description"] or "",
                "reference_type": "course",
                "reference_id": course["id"],
                "resolved_url": None,
            }
        )

    for resource in get_resources(tags=[tag]):
        if resource["id"] in existing_ids or resource["type"] != "competition":
            continue
        new_rows.append(
            {
                "lane": "professional",
                "horizon": "active-contribution",
                "source_agent": "catalog",
                "title": f"Test yourself: {resource['title']}",
                "description": resource["description"] or "",
                "reference_type": "resource",
                "reference_id": resource["id"],
                "resolved_url": resource["url"],
            }
        )

    if new_rows:
        insert_roadmap_items(student_id, new_rows)
    return new_rows


def save_chat_message(student_id, speaker, content):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_transcripts (id, student_id, speaker, content, created_at) VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), student_id, speaker, content, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def get_chat_transcripts(student_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT speaker, content, created_at FROM chat_transcripts WHERE student_id = ? ORDER BY created_at ASC",
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def reveal_more_resources(student_id, tag):
    """The explicit 'show me more' action — pulls in whatever add_interest()
    held back for this tag (CodePath tracks, open-source repos, articles,
    etc.), skipping anything already on the roadmap. Safe to click more than
    once: once everything is added, it just returns an empty list."""
    existing_ids = {item["reference_id"] for item in get_roadmap_items(student_id)}
    new_rows = []

    for resource in get_resources(tags=[tag]):
        if resource["id"] in existing_ids or resource["type"] == "competition":
            continue
        new_rows.append(
            {
                "lane": "professional",
                "horizon": "active-contribution",
                "source_agent": "catalog",
                "title": f"Explore: {resource['title']}",
                "description": resource["description"] or "",
                "reference_type": "resource",
                "reference_id": resource["id"],
                "resolved_url": resource["url"],
            }
        )

    if new_rows:
        insert_roadmap_items(student_id, new_rows)
    return new_rows
