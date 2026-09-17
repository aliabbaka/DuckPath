"""
check_links.py — fills in the `verified` column of a resources CSV by
actually requesting every URL.

This exists because load_resources_csv.py refuses unverified rows, and
checking 443 links by hand isn't realistic. It writes `true` for anything
that answers, `false` for anything that doesn't, and leaves a short note in
a `check_note` column so you can see *why* something failed before deciding
to delete the row or fix the URL.

It only judges whether a URL resolves. Whether a resource is any GOOD, or
belongs in the roadmap at all, is still your review pass — a live link to
something irrelevant is still a row you should cut.

Stdlib only (urllib), so there's no extra package to install.

Usage:
    python3 check_links.py resources_draft_PREVIEW.csv
    python3 check_links.py in.csv -o out.csv --workers 16 --recheck
"""

import argparse
import csv
import os
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def _build_ssl_context():
    """Python installed from python.org ships without a CA bundle, so every
    https:// request raises CERTIFICATE_VERIFY_FAILED and every real link
    looks dead. Fall back to certifi, then to the CA bundle macOS keeps at
    /etc/ssl/cert.pem, before giving up."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass

    if ssl.get_default_verify_paths().cafile is None:
        for candidate in ("/etc/ssl/cert.pem", "/usr/local/etc/openssl/cert.pem"):
            if os.path.exists(candidate):
                return ssl.create_default_context(cafile=candidate)

    return ssl.create_default_context()


SSL_CONTEXT = _build_ssl_context()

# Some sites reject the default urllib agent with a 403 that has nothing to
# do with whether the page exists.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
}

TIMEOUT = 15

# 403/405 mean "the server is there and answered" — plenty of sites block
# automated agents or HEAD specifically. That's a live URL, not a dead one.
OK_ERROR_CODES = {401, 403, 405, 406, 429}


def check_one(url):
    """Returns (verdict, note) where verdict is "true", "false", or "" for
    couldn't-tell. Tries HEAD first since it skips the body, then falls back
    to GET for servers that don't implement HEAD.

    A local TLS failure returns "" rather than "false" — that says something
    is wrong with this machine's certificate store, not with the link, and
    marking a live site dead is the one mistake worth guarding against here.
    """
    if not url.startswith(("http://", "https://")):
        return "false", "not an http(s) url"

    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT) as resp:
                return "true", f"{resp.status}"
        except urllib.error.HTTPError as e:
            if e.code in OK_ERROR_CODES:
                return "true", f"{e.code} (blocked automated request, but live)"
            if method == "GET":
                return "false", f"HTTP {e.code}"
        except urllib.error.URLError as e:
            if isinstance(e.reason, ssl.SSLCertVerificationError):
                return "", f"cert verify failed locally: {e.reason.verify_message or e.reason}"
            if method == "GET":
                return "false", f"unreachable: {e.reason}"
        except ssl.SSLError as e:
            return "", f"TLS error: {e}"
        except Exception as e:  # socket timeouts, bad redirects, odd encodings
            if method == "GET":
                return "false", f"{type(e).__name__}: {e}"
    return "false", "no response"


def run(in_path, out_path, workers, recheck):
    with open(in_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    if not rows:
        print("That CSV has no rows.")
        return

    if "check_note" not in fieldnames:
        fieldnames.append("check_note")
    if "verified" not in fieldnames:
        fieldnames.append("verified")

    # Skip rows already flagged duplicate, and (unless --recheck) rows that
    # already carry a verdict — so re-running only picks up what's new.
    def needs_check(row):
        if row.get("duplicate_of_row", "").strip():
            return False
        if not row.get("url", "").strip():
            return False
        return recheck or not row.get("verified", "").strip()

    todo = [r for r in rows if needs_check(r)]
    print(f"{len(rows)} rows, checking {len(todo)} "
          f"({len(rows) - len(todo)} skipped as duplicate/blank/already checked)\n")

    done = 0
    inconclusive = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for row, (verdict, note) in zip(todo, pool.map(lambda r: check_one(r["url"].strip()), todo)):
            row["verified"] = verdict
            row["check_note"] = note
            done += 1
            if verdict == "false":
                print(f"  DEAD  {note:<40} {row['url'][:70]}")
            elif verdict == "":
                inconclusive += 1
            if done % 25 == 0:
                print(f"  ... {done}/{len(todo)}")

    for row in rows:
        row.setdefault("check_note", "")
        row.setdefault("verified", "")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    live = sum(1 for r in rows if r.get("verified") == "true")
    dead = sum(1 for r in rows if r.get("verified") == "false")
    print(f"\nWrote {out_path}")
    print(f"  {live} live, {dead} dead, {len(rows) - live - dead} unchecked")

    if inconclusive:
        print(f"\n{inconclusive} link(s) couldn't be checked because this machine can't "
              "verify TLS certificates.\nThey were left blank rather than marked dead. Fix with:\n"
              "    pip install certifi --break-system-packages\n"
              "or, on macOS, run 'Install Certificates.command' in your "
              "/Applications/Python 3.x/ folder,\nthen re-run this script.")
    if dead:
        print("\nDead rows are marked verified=false and will NOT load. Fix the URL "
              "or delete the row, then re-run with --recheck.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fill the verified column of a resources CSV.")
    p.add_argument("csv_path")
    p.add_argument("-o", "--out", help="output path (default: overwrite input)")
    p.add_argument("--workers", type=int, default=12, help="parallel requests (default 12)")
    p.add_argument("--recheck", action="store_true", help="re-check rows that already have a verdict")
    a = p.parse_args()
    try:
        run(a.csv_path, a.out or a.csv_path, a.workers, a.recheck)
    except FileNotFoundError:
        print(f"No such file: {a.csv_path}")
        sys.exit(1)
