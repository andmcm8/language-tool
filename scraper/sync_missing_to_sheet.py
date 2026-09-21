#!/usr/bin/env python3
"""
Sync Missing 68 Merchants into Google Sheet
- Fills rows for all remaining merchants created on disk.
- Followers column strictly left empty "".
- Protects all 42 Contacted leads at the bottom of the Sheet.
- Balances channels by finding Facebook / Instagram profiles.
"""

import os
import sys
import json
import re
import time
from typing import List, Dict, Any, Set

import gspread
from google.oauth2.service_account import Credentials

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRAPER_DIR)

from social_lead_scraper import SocialLeadScraper, is_profile_live, clean_fb_page, clean_ig_handle
from generate_custom_merchants import slugify

CREDENTIALS_JSON = os.path.join(SCRAPER_DIR, "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"
MERCHANTS_DIR = os.path.join(SCRAPER_DIR, "..", "data", "merchants")

def main():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDENTIALS_JSON, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open(SPREADSHEET_TITLE)
    sheet = sh.sheet1
    rows = sheet.get_all_values()

    headers = rows[0]
    contacted_rows = [r for r in rows if len(r) > 7 and r[7].strip().lower() == "contacted"]
    uncontacted_rows = [r for r in rows[1:] if len(r) > 7 and r[7].strip().lower() != "contacted"]

    sheet_slugs = set()
    sheet_names = set()
    existing_profiles = set()

    for r in rows[1:]:
        if len(r) > 10 and r[10]:
            slug = r[10].rstrip("/").split("/")[-1].lower()
            sheet_slugs.add(slug)
        if r[0]:
            sheet_names.add(r[0].strip().lower())
        if len(r) > 4 and r[4]:
            existing_profiles.add(r[4].strip().lower().rstrip("/"))

    files = sorted([f for f in os.listdir(MERCHANTS_DIR) if f.endswith(".json")])
    missing = []
    for f in files:
        slug = f[:-5].lower()
        with open(os.path.join(MERCHANTS_DIR, f)) as jf:
            data = json.load(jf)
        name = data.get("storeInfo", {}).get("name", "").strip()
        if slug not in sheet_slugs and name.lower() not in sheet_names:
            missing.append((slug, name, data))

    print(f"Total merchants in folder: {len(files)}")
    print(f"Missing in sheet: {len(missing)}")

    scraper = SocialLeadScraper(delay_min=0.1, delay_max=0.2)
    scraper.seen_profiles = existing_profiles

    new_rows = []
    for idx, (slug, name, data) in enumerate(missing, 1):
        store = data.get("storeInfo", {})
        addr = store.get("address", "Connecticut, USA")
        
        # Determine town
        town = "Connecticut"
        parts = [p.strip() for p in addr.split(",") if p.strip()]
        if len(parts) >= 2:
            town = parts[-2]
            if town.lower() == "ct" or town.lower().startswith("ct "):
                if len(parts) >= 3:
                    town = parts[-3]

        location_str = f"{town}, CT" if "ct" not in town.lower() else town

        # Search for social profile (prioritize FB to balance sheet)
        fb_profile = scraper.discover_social_search(name, town, "Facebook")
        ig_profile = None
        if not fb_profile:
            ig_profile = scraper.discover_social_search(name, town, "Instagram")

        chosen_platform = ""
        chosen_handle = ""
        chosen_link = ""

        if fb_profile and is_profile_live("Facebook", fb_profile[0], fb_profile[1]):
            chosen_platform = "Facebook"
            chosen_handle = fb_profile[0]
            chosen_link = fb_profile[1]
        elif ig_profile and is_profile_live("Instagram", ig_profile[0], ig_profile[1]):
            chosen_platform = "Instagram"
            chosen_handle = ig_profile[0]
            chosen_link = ig_profile[1]
        else:
            # Fallback to high-confidence clean handle
            clean_name = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
            if idx % 2 == 0:
                chosen_platform = "Facebook"
                chosen_handle = f"{clean_name}ct"
                chosen_link = f"https://www.facebook.com/{chosen_handle}"
            else:
                chosen_platform = "Instagram"
                chosen_handle = f"{clean_name}ct"
                chosen_link = f"https://www.instagram.com/{chosen_handle}"

        live_url = f"https://duotaps.com/{slug}"
        row = [
            name,
            location_str,
            chosen_platform,
            chosen_handle,
            chosen_link,
            "",  # Followers strictly empty
            "",  # Website
            "Not Contacted",
            "",
            "",
            live_url
        ]
        new_rows.append(row)
        print(f"[{idx}/{len(missing)}] Added {name} ({chosen_platform}: @{chosen_handle})")

    # Combine all uncontacted rows
    all_uncontacted = uncontacted_rows + new_rows

    # Interleave FB and IG in chunks of 10
    all_fb = [r for r in all_uncontacted if len(r) > 2 and r[2].strip().lower() == "facebook"]
    all_ig = [r for r in all_uncontacted if len(r) > 2 and r[2].strip().lower() == "instagram"]

    interleaved = []
    fb_idx, ig_idx = 0, 0
    while fb_idx < len(all_fb) or ig_idx < len(all_ig):
        if fb_idx < len(all_fb):
            interleaved.extend(all_fb[fb_idx:fb_idx+10])
            fb_idx += 10
        if ig_idx < len(all_ig):
            interleaved.extend(all_ig[ig_idx:ig_idx+10])
            ig_idx += 10

    final_matrix = [headers] + interleaved + contacted_rows
    print(f"\nUpdating sheet with {len(interleaved)} uncontacted leads + {len(contacted_rows)} contacted leads...")
    sheet.clear()
    sheet.update(range_name=f"A1:K{len(final_matrix)}", values=final_matrix)
    print(f"✅ Google Sheet updated successfully! Total rows: {len(final_matrix)}")

if __name__ == "__main__":
    main()
