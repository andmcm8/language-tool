#!/usr/bin/env python3
"""
Reorder Google Sheet 'FaceBook/Instagram Scraper' by Follower Count:
- Adds/populates 'Followers' column.
- Sorts uncontacted leads by lowest follower count to highest.
- Interleaves in chunks: 10 Facebook -> 10 Instagram -> 10 Facebook -> 10 Instagram...
- Places all Contacted rows at the bottom no matter what.
- Preserves all notes, links, and data.
"""

import os
import sys
import re
import json
import time
import random
import hashlib
from typing import List, Dict, Tuple, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

from google.oauth2.service_account import Credentials
import gspread

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_JSON = os.path.join(SCRAPER_DIR, "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"
CACHE_FILE = os.path.join(SCRAPER_DIR, "followers_cache.json")

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

def load_cache() -> Dict[str, int]:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache: Dict[str, int]):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save cache: {e}")

def parse_follower_count(raw: str) -> Optional[int]:
    if not raw:
        return None
    raw = raw.replace(",", "").strip()
    m = re.search(r"([\d.]+)\s*([KkMm]?)", raw)
    if not m:
        return None
    try:
        val = float(m.group(1))
        unit = m.group(2).upper()
        if unit == "K":
            return int(val * 1000)
        elif unit == "M":
            return int(val * 1000000)
        return int(val)
    except Exception:
        return None

def fetch_followers_yahoo(platform: str, name: str, handle: str) -> Optional[int]:
    clean_handle = handle.lstrip("@").strip()
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    if platform.lower() == "instagram":
        queries = [
            f"site:instagram.com/{clean_handle}",
            f"\"{clean_handle}\" site:instagram.com followers",
            f"\"{name}\" instagram followers"
        ]
        for q in queries:
            try:
                url = f"https://search.yahoo.com/search?p={quote(q)}"
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    for m in re.finditer(r"([\d.,]+[KkMm]?)\s*followers", resp.text, re.I):
                        cnt = parse_follower_count(m.group(1))
                        if cnt and cnt > 0 and cnt != 500: # avoid 500 status code false positives
                            return cnt
            except Exception:
                pass
            time.sleep(0.3)
    else:
        # Facebook
        queries = [
            f"site:facebook.com/{clean_handle}",
            f"\"{name}\" site:facebook.com followers OR likes",
            f"\"{clean_handle}\" facebook likes"
        ]
        for q in queries:
            try:
                url = f"https://search.yahoo.com/search?p={quote(q)}"
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    for m in re.finditer(r"([\d.,]+[KkMm]?)\s*(?:likes|followers)", resp.text, re.I):
                        cnt = parse_follower_count(m.group(1))
                        if cnt and cnt > 0 and cnt != 500:
                            return cnt
            except Exception:
                pass
            time.sleep(0.3)

    return None

    return None

def main():
    print("=" * 70)
    print(" 📊 Reordering Google Sheet by Follower Count (Low to High)")
    print("=" * 70)

    if not os.path.exists(CREDENTIALS_JSON):
        print(f"❌ Credentials not found at {CREDENTIALS_JSON}")
        sys.exit(1)

    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDENTIALS_JSON, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_TITLE).sheet1

    all_rows = sheet.get_all_values()
    if not all_rows:
        print("❌ Sheet is empty.")
        sys.exit(1)

    headers = all_rows[0]
    print(f"Current headers ({len(headers)} cols): {headers}")

    cache = load_cache()
    print(f"Loaded {len(cache)} cached follower counts.")

    # Determine column mapping
    has_followers_col = "followers" in [h.lower().strip() for h in headers]
    if has_followers_col:
        followers_col_idx = [h.lower().strip() for h in headers].index("followers")
    else:
        # Insert Followers at index 5 (Column F, right after Profile Link)
        followers_col_idx = 5

    contacted_rows = []
    uncontacted_fb = []
    uncontacted_ig = []

    for row_idx, r in enumerate(all_rows[1:], start=2):
        name = r[0].strip() if len(r) > 0 else ""
        loc = r[1].strip() if len(r) > 1 else ""
        plat = r[2].strip() if len(r) > 2 else ""
        handle = r[3].strip() if len(r) > 3 else ""
        link = r[4].strip() if len(r) > 4 else ""
        
        # Read other cols depending on whether followers col already exists
        if has_followers_col:
            f_val = r[followers_col_idx].strip() if len(r) > followers_col_idx else ""
            website = r[6].strip() if len(r) > 6 else ""
            status = r[7].strip() if len(r) > 7 else ""
            date_c = r[8].strip() if len(r) > 8 else ""
            notes = r[9].strip() if len(r) > 9 else ""
            demo = r[10].strip() if len(r) > 10 else ""
        else:
            f_val = ""
            website = r[5].strip() if len(r) > 5 else ""
            status = r[6].strip() if len(r) > 6 else ""
            date_c = r[7].strip() if len(r) > 7 else ""
            notes = r[8].strip() if len(r) > 8 else ""
            demo = r[9].strip() if len(r) > 9 else ""

        entry = {
            "row_idx": row_idx,
            "name": name,
            "location": loc,
            "platform": plat,
            "handle": handle,
            "link": link,
            "website": website,
            "status": status,
            "date_contacted": date_c,
            "notes": notes,
            "demo_link": demo,
            "followers": 0,
            "raw_row": r
        }

        if status.lower() == "contacted":
            contacted_rows.append(entry)
        elif "facebook" in plat.lower():
            uncontacted_fb.append(entry)
        elif "instagram" in plat.lower():
            uncontacted_ig.append(entry)
        else:
            uncontacted_ig.append(entry)

    print(f"📊 Summary of rows found:")
    print(f"   Uncontacted Facebook: {len(uncontacted_fb)}")
    print(f"   Uncontacted Instagram: {len(uncontacted_ig)}")
    print(f"   Contacted (Protected): {len(contacted_rows)}")

    # Resolve followers for all uncontacted leads
    all_uncontacted = uncontacted_fb + uncontacted_ig
    to_fetch = []

    for item in all_uncontacted:
        cache_key = f"{item['platform'].lower()}_{item['handle'].lower().strip()}"
        if cache_key in cache:
            item["followers"] = cache[cache_key]
        else:
            to_fetch.append((cache_key, item))

    print(f"🔍 Need to scrape followers for {len(to_fetch)} handles ({len(all_uncontacted) - len(to_fetch)} already cached)...")

    if to_fetch:
        # Multi-threaded batch resolution
        def worker(entry_tuple):
            key, it = entry_tuple
            cnt = fetch_followers_yahoo(it["platform"], it["name"], it["handle"])
            return key, it, cnt

        completed = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_item = {executor.submit(worker, t): t for t in to_fetch}
            for future in as_completed(future_to_item):
                try:
                    key, it, count = future.result()
                    if count:
                        cache[key] = count
                        it["followers"] = count
                    else:
                        it["followers"] = None
                    completed += 1
                    if completed % 50 == 0 or completed == len(to_fetch):
                        print(f"   Progress: {completed}/{len(to_fetch)} processed")
                        save_cache(cache)
                except Exception as e:
                    key, it = future_to_item[future]
                    it["followers"] = None
        save_cache(cache)

    # Sort Facebook ascending by followers
    uncontacted_fb.sort(key=lambda x: (x["followers"], x["name"].lower()))
    # Sort Instagram ascending by followers
    uncontacted_ig.sort(key=lambda x: (x["followers"], x["name"].lower()))

    print(f"\n✅ Sorting complete:")
    print(f"   FB Lowest: {uncontacted_fb[0]['name']} ({uncontacted_fb[0]['followers']:,} followers)")
    print(f"   FB Highest: {uncontacted_fb[-1]['name']} ({uncontacted_fb[-1]['followers']:,} followers)")
    print(f"   IG Lowest: {uncontacted_ig[0]['name']} ({uncontacted_ig[0]['followers']:,} followers)")
    print(f"   IG Highest: {uncontacted_ig[-1]['name']} ({uncontacted_ig[-1]['followers']:,} followers)")

    # Interleave in chunks of 10: 10 FB, 10 IG, 10 FB, 10 IG...
    interleaved_leads = []
    fb_i = 0
    ig_i = 0

    chunk_num = 1
    while fb_i < len(uncontacted_fb) or ig_i < len(uncontacted_ig):
        # 10 FB
        if fb_i < len(uncontacted_fb):
            chunk = uncontacted_fb[fb_i : fb_i + 10]
            interleaved_leads.extend(chunk)
            fb_i += 10
        # 10 IG
        if ig_i < len(uncontacted_ig):
            chunk = uncontacted_ig[ig_i : ig_i + 10]
            interleaved_leads.extend(chunk)
            ig_i += 10
        chunk_num += 1

    # Contacted rows at the bottom
    for c in contacted_rows:
        cache_key = f"{c['platform'].lower()}_{c['handle'].lower().strip()}"
        c["followers"] = cache.get(cache_key, None)

    final_records = interleaved_leads + contacted_rows

    print(f"\n📦 Final sheet structure:")
    print(f"   Interleaved Uncontacted: {len(interleaved_leads)} rows")
    print(f"   Bottom Contacted: {len(contacted_rows)} rows")
    print(f"   Total Lead Rows: {len(final_records)}")

    # Format new headers
    new_headers = [
        "Business Name",
        "Location",
        "Platform",
        "Handle",
        "Profile Link",
        "Followers",
        "Website",
        "Outreach Status",
        "Date Contacted",
        "Notes",
        "Custom Demo Link"
    ]

    # Convert records into 2D table
    new_table = [new_headers]
    for r in final_records:
        new_table.append([
            r["name"],
            r["location"],
            r["platform"],
            r["handle"],
            r["link"],
            f"{r['followers']:,}" if r.get("followers") is not None else "",
            r["website"],
            r["status"],
            r["date_contacted"],
            r["notes"],
            r["demo_link"]
        ])

    print("\n🚀 Writing reordered dataset to Google Sheet...")
    # Clear and update
    sheet.clear()
    sheet.update(values=new_table, range_name='A1')
    print(f"🎉 Successfully updated Google Sheet '{SPREADSHEET_TITLE}' with {len(new_table)} rows (including header)!")

if __name__ == "__main__":
    main()
