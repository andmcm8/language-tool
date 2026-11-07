#!/usr/bin/env python3
"""List contacted businesses (outreach/sent_emails_db.json) whose menu page is not verified yet.
Matches on exact normalized business name only (prefix matching produced wrong pairs)."""
import glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and").replace("’", "'"))

db = json.load(open(os.path.join(ROOT, "outreach", "sent_emails_db.json")))
verified = set(json.load(open(os.path.join(ROOT, "data", "verified-menus.json"))))
verified |= set(json.load(open(os.path.join(ROOT, "scraper", "research_log.json"))))  # already researched
by_name = {}
for f in glob.glob(os.path.join(ROOT, "data", "merchants", "*.json")):
    d = json.load(open(f))
    by_name.setdefault(norm(d["storeInfo"]["name"]), []).append((os.path.basename(f)[:-5], d["storeInfo"].get("address", "")))

seen = set()
for r in sorted(db.values(), key=lambda r: r["sent_at"]):
    for slug, addr in by_name.get(norm(r["business_name"]), []):
        if slug in verified or slug in seen:
            continue
        seen.add(slug)
        print(f"{r['sent_at'][:10]}\t{slug}\t{addr}")
