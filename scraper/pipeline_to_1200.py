#!/usr/bin/env python3
"""
High-Velocity Expansion Pipeline to 1,200+ Connecticut Merchants for DuoTaps
Features:
- Exhaustive coverage across Connecticut dining hubs (strictly excluding New Canaan).
- Deduplicates against all existing 878+ merchants and sheet rows.
- 50/50 Channel Balance between Instagram and Facebook.
- Real CT phone numbers only; falls back strictly to empty string "" (ZERO fake numbers).
- Real bilingual menus translated with Gemini.
- Protects all Contacted leads in the Google Sheet (kept strictly at the bottom).
- Rebuilds registry and auto-deploys to Vercel in checkpoints.
"""

import os
import sys
import re
import json
import time
import random
import subprocess
from typing import List, Dict, Any, Set, Tuple

import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRAPER_DIR)

from social_lead_scraper import (
    SocialLeadScraper,
    clean_ig_handle,
    clean_fb_page,
    is_profile_live,
    normalize_biz_name,
    EXCLUDED_TOWNS,
    CHAIN_EXCLUSIONS
)
from generate_custom_merchants import (
    get_gemini_api_key,
    slugify,
    scrape_website_content,
    generate_merchant_config_with_gemini,
    update_registry_file
)

CREDENTIALS_JSON = os.path.join(SCRAPER_DIR, "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"
MERCHANTS_DIR = os.path.join(SCRAPER_DIR, "..", "data", "merchants")
LOG_FILE = os.path.join(SCRAPER_DIR, "pipeline_to_1200.log")

# Primary CT dining hubs ordered by density (strictly excluding New Canaan)
PRIORITY_TOWNS = [
    "New Haven", "Hartford", "Stamford", "Norwalk", "Bridgeport",
    "Danbury", "Waterbury", "West Hartford", "Greenwich", "Fairfield",
    "Milford", "Middletown", "Manchester", "Bristol", "Meriden",
    "Hamden", "Stratford", "Enfield", "Southington", "Norwich",
    "Groton", "Shelton", "Torrington", "Trumbull", "Glastonbury",
    "Wallingford", "Naugatuck", "Vernon", "Newington", "Cheshire",
    "East Hartford", "Branford", "Westport", "New London", "Farmington",
    "Simsbury", "Bethel", "Southbury", "Newtown", "Ridgefield",
    "Watertown", "Wilton", "Clinton", "Madison", "Guilford",
    "Old Saybrook", "Mystic", "Colchester", "Plainville", "Windsor",
    "Rocky Hill", "Cromwell", "Berlin", "Seymour", "Oxford",
    "Derby", "Ansonia", "Monroe", "Easton", "Redding",
    "Weston", "Woodbridge", "Bethany", "North Haven", "North Branford",
    "Middlefield", "Durham", "Killingworth", "Darien", "Wolcott",
    "Avon", "Canton", "Granby", "Suffield", "East Lyme",
    "Old Lyme", "Stonington", "Waterford", "Ledyard", "Montville",
    "Coventry", "Mansfield", "Windham", "Tolland", "Ellington",
    "South Windsor", "Bloomfield", "Winchester", "Litchfield", "Woodbury",
    "New Milford", "Brookfield", "Middlebury", "Prospect", "Beacon Falls"
]

HIGH_YIELD_CATEGORIES = [
    "restaurant",
    "cafe",
    "pizzeria",
    "bakery",
    "deli",
    "bar and grill",
    "diner",
    "seafood",
    "brewery",
    "tacos",
    "sushi",
    "burgers",
    "ice cream"
]

def log(msg: str):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as lf:
            lf.write(line + "\n")
    except Exception:
        pass

def checkpoint_deploy(total_merchants: int, newly_created: int):
    """Rebuilds registry, runs build, and pushes to git/Vercel."""
    log(f"🚀 [CHECKPOINT] Total places: {total_merchants} (+{newly_created} new). Auto-deploying to Vercel...")
    try:
        update_registry_file()
        cwd = os.path.join(SCRAPER_DIR, "..")
        subprocess.run(
            ["git", "add", "data/merchants/"],
            cwd=cwd, check=True, capture_output=True
        )
        commit_msg = f"feat(merchants): expansion checkpoint ({total_merchants} places on website)"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=cwd, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=cwd, check=True, capture_output=True
        )
        log(f"✅ [CHECKPOINT] Pushed to GitHub & triggered Vercel deployment! Total: {total_merchants}")
    except Exception as e:
        log(f"⚠️ [CHECKPOINT WARNING] Notice: {e}")

def flush_sheet(sheet, pending_sheet_rows: List[List[str]]):
    if not pending_sheet_rows:
        return
    log(f"📊 Flushing {len(pending_sheet_rows)} new leads to Google Sheet...")
    try:
        current_all_rows = sheet.get_all_values()
        headers = current_all_rows[0]
        uncontacted_rows = []
        contacted_rows = []
        for r in current_all_rows[1:]:
            if len(r) >= 8 and r[7].strip().lower() == "contacted":
                contacted_rows.append(r)
            else:
                uncontacted_rows.append(r)

        new_fb = [r for r in pending_sheet_rows if len(r) > 2 and r[2].lower() == "facebook"]
        new_ig = [r for r in pending_sheet_rows if len(r) > 2 and r[2].lower() == "instagram"]

        all_fb = [r for r in uncontacted_rows if len(r) > 2 and "facebook" in r[2].lower()] + new_fb
        all_ig = [r for r in uncontacted_rows if len(r) > 2 and "instagram" in r[2].lower()] + new_ig

        interleaved = []
        fb_idx = 0
        ig_idx = 0
        while fb_idx < len(all_fb) or ig_idx < len(all_ig):
            if fb_idx < len(all_fb):
                interleaved.extend(all_fb[fb_idx:fb_idx+10])
                fb_idx += 10
            if ig_idx < len(all_ig):
                interleaved.extend(all_ig[ig_idx:ig_idx+10])
                ig_idx += 10

        final_sheet_matrix = [headers] + interleaved + contacted_rows
        sheet.update(range_name=f"A1:K{len(final_sheet_matrix)}", values=final_sheet_matrix)
        log(f"✅ Google Sheet updated successfully: {len(interleaved)} uncontacted leads + {len(contacted_rows)} protected contacted leads.")
        pending_sheet_rows.clear()
    except Exception as se:
        log(f"⚠️ Google Sheet update notice: {se}")

def run_expansion(target_total: int = 1215):
    log("=" * 75)
    log(f" 🚀 DuoTaps Expansion Pipeline to {target_total}+ Connecticut Merchants")
    log(f" Excluded: New Canaan strictly omitted.")
    log("=" * 75)

    # 1. Inspect existing local merchants
    existing_slugs: Set[str] = set()
    if os.path.exists(MERCHANTS_DIR):
        for f in os.listdir(MERCHANTS_DIR):
            if f.endswith(".json"):
                existing_slugs.add(f[:-5].lower())

    initial_total = len(existing_slugs)
    log(f"📂 Current local merchants: {initial_total}")
    if initial_total >= target_total:
        log(f"🎉 Target already reached! ({initial_total} >= {target_total})")
        return

    needed = target_total - initial_total
    log(f"🎯 Need to create {needed} new merchants to reach {target_total}.")

    # 2. Connect to Google Sheet
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_JSON, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open(SPREADSHEET_TITLE)
    sheet = sh.sheet1

    all_rows = sheet.get_all_values()
    existing_links: Set[str] = set()
    existing_names: Set[str] = set()
    ig_count = 0
    fb_count = 0

    contacted_count = 0
    for r in all_rows[1:]:
        if len(r) >= 1 and r[0].strip():
            existing_names.add(normalize_biz_name(r[0].strip()))
        if len(r) >= 5 and r[4].strip():
            existing_links.add(r[4].strip().lower())
        if len(r) >= 3:
            plat = r[2].strip().lower()
            if plat == "instagram":
                ig_count += 1
            elif plat == "facebook":
                fb_count += 1
        if len(r) >= 8 and r[7].strip().lower() == "contacted":
            contacted_count += 1

    log(f"📊 Google Sheet currently has {len(all_rows)-1} rows.")
    log(f"   Balance: {ig_count} Instagram / {fb_count} Facebook | {contacted_count} Contacted (Protected)")

    # 3. Initialize scraper
    scraper = SocialLeadScraper(delay_min=0.15, delay_max=0.3)
    scraper.seen_profiles = set(existing_links)
    scraper.seen_names = set(existing_names)
    scraper.ig_assigned_count = ig_count
    scraper.fb_assigned_count = fb_count

    confirmed_and_created = 0
    pending_sheet_rows: List[List[str]] = []

    # Iterate through priority towns
    town_list = list(PRIORITY_TOWNS)
    random.shuffle(town_list)

    while confirmed_and_created < needed:
        for town in town_list:
            if confirmed_and_created >= needed:
                break

            if any(ex in town.lower() for ex in EXCLUDED_TOWNS):
                continue

            current_total = initial_total + confirmed_and_created
            log(f"\n📍 Scanning: {town}, CT (Progress: {current_total}/{target_total}, +{confirmed_and_created} new)")

            candidates = []
            for cat in HIGH_YIELD_CATEGORIES:
                if confirmed_and_created >= needed:
                    break
                osm_results = scraper.query_nominatim_osm(town, cat, limit=30)
                for item in osm_results:
                    name = item.get("business_name", "")
                    norm = normalize_biz_name(name)
                    if not norm or norm in scraper.seen_names:
                        continue
                    if any(chain.lower() in name.lower() for chain in CHAIN_EXCLUSIONS):
                        continue
                    base_slug = slugify(name)
                    if not base_slug or base_slug in existing_slugs:
                        continue
                    scraper.seen_names.add(norm)
                    candidates.append(item)

            log(f"   Found {len(candidates)} new candidates in {town}.")

            for c in candidates:
                if confirmed_and_created >= needed:
                    break

                biz_name = c["business_name"]
                website = c.get("website", "")
                osm_ig = c.get("osm_ig", "")
                osm_fb = c.get("osm_fb", "")

                base_slug = slugify(biz_name)
                if not base_slug or base_slug in existing_slugs:
                    continue

                ig_profile = None
                fb_profile = None

                if osm_ig:
                    if osm_ig.startswith("http"):
                        ig_profile = clean_ig_handle(osm_ig)
                    else:
                        ig_h = osm_ig.lstrip("@").strip()
                        ig_profile = (f"@{ig_h}", f"https://www.instagram.com/{ig_h}/")

                if osm_fb:
                    if osm_fb.startswith("http"):
                        fb_profile = clean_fb_page(osm_fb)
                    else:
                        fb_profile = (osm_fb, f"https://www.facebook.com/{osm_fb}")

                target_site = website
                if not target_site or not target_site.startswith("http"):
                    sites = scraper.discover_official_sites(biz_name, town)
                    if sites:
                        target_site = sites[0]

                if target_site:
                    low_ts = target_site.lower()
                    if any(bad in low_ts for bad in [".gov", ".edu", "parksrec", "cityof", "townof", "wikipedia.org"]):
                        continue

                if target_site and (not ig_profile or not fb_profile):
                    site_ig, site_fb = scraper.crawl_site_for_socials(target_site)
                    if site_ig and not ig_profile:
                        ig_profile = site_ig
                    if site_fb and not fb_profile:
                        fb_profile = site_fb

                # Search fallback if social not found
                if not ig_profile and not fb_profile:
                    if scraper.fb_assigned_count < scraper.ig_assigned_count:
                        fb_profile = scraper.discover_social_search(biz_name, town, "Facebook")
                        if not fb_profile:
                            ig_profile = scraper.discover_social_search(biz_name, town, "Instagram")
                    else:
                        ig_profile = scraper.discover_social_search(biz_name, town, "Instagram")
                        if not ig_profile:
                            fb_profile = scraper.discover_social_search(biz_name, town, "Facebook")

                # Verification
                ig_is_live = False
                fb_is_live = False

                if ig_profile:
                    ig_is_live = is_profile_live("Instagram", ig_profile[0], ig_profile[1])
                if fb_profile:
                    fb_is_live = is_profile_live("Facebook", fb_profile[0], fb_profile[1])

                # 50/50 Channel Balancing
                chosen_platform = ""
                chosen_handle = ""
                chosen_link = ""

                if ig_is_live and fb_is_live:
                    if scraper.fb_assigned_count < scraper.ig_assigned_count:
                        chosen_platform = "Facebook"
                        chosen_handle = fb_profile[0]
                        chosen_link = fb_profile[1]
                        scraper.fb_assigned_count += 1
                    else:
                        chosen_platform = "Instagram"
                        chosen_handle = ig_profile[0]
                        chosen_link = ig_profile[1]
                        scraper.ig_assigned_count += 1
                elif ig_is_live:
                    chosen_platform = "Instagram"
                    chosen_handle = ig_profile[0]
                    chosen_link = ig_profile[1]
                    scraper.ig_assigned_count += 1
                elif fb_is_live:
                    chosen_platform = "Facebook"
                    chosen_handle = fb_profile[0]
                    chosen_link = fb_profile[1]
                    scraper.fb_assigned_count += 1

                if not chosen_platform or not chosen_link:
                    continue

                if chosen_link.lower() in scraper.seen_profiles:
                    continue
                scraper.seen_profiles.add(chosen_link.lower())

                # --- CONFIRMED PLACE: GENERATE BILINGUAL DEMO PAGE ---
                slug = base_slug
                json_path = os.path.join(MERCHANTS_DIR, f"{slug}.json")
                live_url = f"https://duotaps.com/{slug}"

                log(f"✨ [CONFIRMED #{initial_total + confirmed_and_created + 1}/{target_total}] {biz_name} ({town}, CT)")
                log(f"   Platform: {chosen_platform} ({chosen_handle}) | Site: {target_site or 'N/A'}")

                scraped_content = ""
                if target_site and target_site.startswith("http"):
                    scraped_content = scrape_website_content(target_site)

                try:
                    config = generate_merchant_config_with_gemini(
                        biz_name=biz_name,
                        location=f"{town}, CT",
                        website=target_site or "",
                        scraped_content=scraped_content,
                        slug=slug
                    )

                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(config, jf, indent=2, ensure_ascii=False)
                    existing_slugs.add(slug.lower())

                    # Queue for Google Sheet
                    new_row = [
                        biz_name,
                        f"{town}, CT",
                        chosen_platform,
                        chosen_handle,
                        chosen_link,
                        "",
                        target_site or "N/A",
                        "Not Contacted",
                        "",
                        "",
                        live_url
                    ]
                    pending_sheet_rows.append(new_row)
                    confirmed_and_created += 1

                    # Checkpoint commit & push every 25 places
                    if confirmed_and_created % 25 == 0:
                        cur_tot = initial_total + confirmed_and_created
                        flush_sheet(sheet, pending_sheet_rows)
                        checkpoint_deploy(cur_tot, confirmed_and_created)

                    time.sleep(0.3)

                except Exception as e:
                    log(f"   ❌ Error generating config for {biz_name}: {e}")
                    time.sleep(1.0)

        random.shuffle(town_list)

    # Final flush and deploy
    update_registry_file()
    final_total = len([f for f in os.listdir(MERCHANTS_DIR) if f.endswith(".json")])

    if pending_sheet_rows:
        flush_sheet(sheet, pending_sheet_rows)

    checkpoint_deploy(final_total, confirmed_and_created)

    log("\n" + "=" * 75)
    log(f"🎉 Pipeline Complete! Total merchants on website: {final_total} (+{confirmed_and_created} created).")
    log(f"   Final Channel Balance: {scraper.ig_assigned_count} Instagram / {scraper.fb_assigned_count} Facebook")
    log("=" * 75)

if __name__ == "__main__":
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 1215
    run_expansion(target_total=target)
