"""
load_resources_csv.py

Loads a CLEANED resources CSV (same columns extract_cs_resources.py
produces: year_tab, title, url, description, tags, type,
duplicate_of_row, verified) directly into advisorpath.db's `resources`
table.

This replaces resources_csv_to_sql.py from the old Supabase version, which
doesn't work here — it generates Postgres array syntax like
'{"tag1","tag2"}' for the tags column, but this database is SQLite, where
tags are just a plain comma-separated string (see db.py). Python's sqlite3
module takes plain values directly, so there's no SQL text to generate at
all this time — just straight inserts.

This does NOT decide what's relevant or dedupe — that's the review pass you
already know from before. Run this only on a CSV you've already cleaned in
a spreadsheet.

It DOES refuse to load rows whose `verified` column is empty. A row only
gets into the database once someone (or check_links.py) has confirmed the
URL actually resolves, because nothing downstream re-checks it: agents.py
verifies that a cited resource *exists in the database*, so a dead link
sitting in the database is a dead link shown to a student. Pass
--allow-unverified to bypass this while testing.

Usage:
    python3 load_resources_csv.py resources_cleaned.csv
    python3 load_resources_csv.py resources_cleaned.csv --allow-unverified
"""

import csv
import re
import sys

import db
from questions import INTEREST_LABELS

ALLOWED_TYPES = {
    "codepath_track", "open_source_repo", "internship", "club",
    "article", "sandbox_project", "competition", "fellowship", "course",
}

# Anything outside this set is invisible to the app: get_resources() filters
# by tag, and the only tags ever queried are the six onboarding interests.
ALLOWED_TAGS = set(INTEREST_LABELS)

TRUTHY = {"true", "yes", "y", "1", "x", "✓"}
# An explicit "no" is different from a blank: blank means nobody has checked
# this URL yet, "no" means someone checked and it was dead. --allow-unverified
# forgives the first and never the second.
FALSY = {"false", "no", "n", "0", "dead", "broken"}


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "resource"


def normalize_url(url):
    """Two rows pointing at the same page are the same resource even when
    their titles differ, so the URL is what identifies a resource — the
    title slug only decides what its id looks like."""
    return url.strip().rstrip("/").lower()


def is_verified(row):
    return row.get("verified", "").strip().lower() in TRUTHY


def is_known_dead(row):
    return row.get("verified", "").strip().lower() in FALSY


def clean_tags(raw):
    """Normalizes the extractor's ';' separator to ',' and drops any tag the
    app can't query. Returns (kept_string, dropped_list)."""
    tags = [t.strip() for t in (raw or "").replace(";", ",").split(",") if t.strip()]
    kept = [t for t in tags if t in ALLOWED_TAGS]
    dropped = [t for t in tags if t not in ALLOWED_TAGS]
    return ",".join(kept), dropped


def load(csv_path, allow_unverified=False):
    db.init_db()
    # Must run before the inserts below, not after. seed_if_empty() decides
    # whether to seed by counting institutions, so if this loader populates
    # `resources` into a fresh database first, the app's next startup still
    # thinks it needs to seed and collides on ids like 'picoctf'. Seeding
    # first means slug de-collision below turns that into 'picoctf-2'.
    db.seed_if_empty()

    conn = db.get_connection()
    existing = conn.execute("SELECT id, url FROM resources").fetchall()
    existing_ids = {row["id"] for row in existing}
    existing_urls = {normalize_url(row["url"]) for row in existing if row["url"]}

    inserted = 0
    skipped_dupes = 0
    skipped_bad = 0
    skipped_unverified = 0
    skipped_dead = 0
    skipped_untagged = 0
    skipped_existing = 0
    bad_tags = set()

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("duplicate_of_row", "").strip():
                skipped_dupes += 1
                continue

            title = row.get("title", "").strip()
            url = row.get("url", "").strip()
            if not title or not url:
                skipped_bad += 1
                continue

            if normalize_url(url) in existing_urls:
                # Already in the database — either seeded in db.py or loaded by
                # an earlier run. Inserting it again under a de-collided id
                # would put the same resource on a student's roadmap twice.
                skipped_existing += 1
                continue

            if is_known_dead(row):
                skipped_dead += 1
                continue

            if not allow_unverified and not is_verified(row):
                skipped_unverified += 1
                continue

            tags, dropped = clean_tags(row.get("tags"))
            bad_tags.update(dropped)
            if not tags:
                # No queryable tag means no student would ever see this row.
                skipped_untagged += 1
                continue

            base_id = slugify(title)
            resource_id = base_id
            suffix = 2
            while resource_id in existing_ids:
                resource_id = f"{base_id}-{suffix}"
                suffix += 1
            existing_ids.add(resource_id)
            existing_urls.add(normalize_url(url))

            type_value = row.get("type", "").strip()
            if type_value not in ALLOWED_TYPES:
                type_value = "article"

            conn.execute(
                "INSERT INTO resources (id, title, type, url, description, tags) VALUES (?, ?, ?, ?, ?, ?)",
                (resource_id, title, type_value, url, row.get("description", "").strip(), tags),
            )
            inserted += 1

    conn.commit()
    conn.close()

    print(f"Inserted {inserted} resources into {db.DB_PATH}.")
    print(f"Skipped: {skipped_dupes} flagged duplicate, {skipped_bad} missing a title or url, "
          f"{skipped_untagged} with no usable tag, {skipped_dead} marked dead, "
          f"{skipped_existing} already in the database.")
    if allow_unverified:
        print("WARNING: --allow-unverified was set, so unchecked URLs may have been loaded.")
    else:
        print(f"Skipped: {skipped_unverified} not marked verified.")
        if skipped_unverified and not inserted:
            print("\nNothing loaded — no row has its `verified` column filled in.\n"
                  "Run `python3 check_links.py <csv>` to fill it, or mark rows by hand "
                  "with true/yes/1/x.")
    if bad_tags:
        print(f"\nDropped {len(bad_tags)} unrecognized tag(s): {', '.join(sorted(bad_tags))}")
        print(f"Valid tags are: {', '.join(sorted(ALLOWED_TAGS))}")
    return inserted


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    unknown = flags - {"--allow-unverified"}
    if len(args) != 1 or unknown:
        if unknown:
            print(f"Unknown option(s): {', '.join(sorted(unknown))}")
        print("Usage: python3 load_resources_csv.py <cleaned.csv> [--allow-unverified]")
        sys.exit(1)
    load(args[0], allow_unverified="--allow-unverified" in flags)
