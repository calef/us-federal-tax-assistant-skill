#!/usr/bin/env python3
"""
Download IRS form PDFs organized into forms/<year>/ directories.

Usage:
  python3 scripts/download-forms.py          # download all forms
  python3 scripts/download-forms.py 2025     # download only 2025 forms
  python3 scripts/download-forms.py 2024 2025 2026  # multiple years

Forms are organized by their IRS revision year as listed in forms/metadata.json.
Run scripts/scrape-metadata.py first if metadata.json is missing or outdated.

Filters out non-English language variants automatically.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..")
FORMS_DIR = os.path.join(REPO_ROOT, "forms")
META_FILE = os.path.join(FORMS_DIR, "metadata.json")
BASE_URL = "https://www.irs.gov/pub/irs-pdf"

# Non-English language suffixes to skip
LANG_SUFFIXES = {
    "sp", "ru", "ko", "zhs", "zht", "ar", "bn", "cs", "de", "fa", "fr",
    "gj", "gu", "ht", "it", "ja", "km", "kr", "pa", "pl", "pt", "so",
    "tl", "ur", "vn", "vie", "cn",
}


def parse_year(description):
    """Extract revision year from an IRS description string."""
    desc = description.strip()
    m = re.match(r"^(20\d\d)\s", desc)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d{2})(\d{2})\s", desc)
    if m:
        yy = int(m.group(2))
        return (2000 + yy) if yy < 50 else (1900 + yy)
    return None


def is_lang_variant(fname):
    base = fname.replace(".pdf", "")
    for suffix in sorted(LANG_SUFFIXES, key=len, reverse=True):
        if base.endswith(suffix) and len(base) > len(suffix) + 2:
            return True
    return False


def load_metadata():
    if not os.path.exists(META_FILE):
        print(f"ERROR: {META_FILE} not found.")
        print("Run: python3 scripts/scrape-metadata.py")
        raise SystemExit(1)
    with open(META_FILE) as f:
        records = json.load(f)
    result = {}
    for r in records:
        fname = r["filename"]
        if not re.match(r"^f[0-9]", fname):
            continue
        if is_lang_variant(fname):
            continue
        year = parse_year(r["description"])
        result[fname] = year
    return result


def human_size(n):
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n // 1024}KB"
    return f"{n / (1024 * 1024):.1f}MB"


def download(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return len(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def main():
    target_years = set(int(y) for y in sys.argv[1:]) if sys.argv[1:] else None

    mapping = load_metadata()  # fname -> year (or None)

    # Filter to requested years
    if target_years:
        to_download = {f: y for f, y in mapping.items() if y in target_years}
        print(f"Downloading forms for year(s): {sorted(target_years)}")
    else:
        to_download = mapping
        print(f"Downloading all {len(to_download)} forms organized by year")

    print()

    passed = skipped = failed = 0

    for fname, year in sorted(to_download.items(), key=lambda x: (x[1] or 0, x[0])):
        year_str = str(year) if year else "unknown"
        dest_dir = os.path.join(FORMS_DIR, year_str)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, fname)

        if os.path.exists(dest_path):
            skipped += 1
            continue

        url = f"{BASE_URL}/{fname}"
        size = download(url, dest_path)
        if size is not None:
            print(f"  [{year_str}] {fname:<50} OK ({human_size(size)})")
            passed += 1
        else:
            print(f"  [{year_str}] {fname:<50} 404")
            failed += 1

    print()
    print(f"Done: {passed} downloaded, {skipped} already present, {failed} not found.")


if __name__ == "__main__":
    main()
