#!/usr/bin/env python3
"""
Overnight 1,000 Lead Scraper & Custom Merchant Page Generator for DuoTaps
Designed for autonomous overnight execution:
- Discovers independent restaurants across Connecticut (strictly excluding New Canaan).
- Verifies live official websites and active Instagram & Facebook profiles (balanced 50/50).
- Scrapes menus (ignoring binary/PDF assets).
- Generates authentic culinary Spanish translations and AI assistants via Gemini with rate-limit retries.
- Flushes leads to Google Sheet in batches of 10 to respect Google API quotas.
- Automatically commits, rebuilds registry, and pushes to GitHub/Vercel every 50 places.
- Protects contacted leads (rows 74–103) and deduplicates against all existing records.
"""

import os
import sys
import re
import json
import time
import random
import subprocess
import urllib.parse
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
    IGNORED_DOMAINS
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
LOG_FILE = os.path.join(SCRAPER_DIR, "overnight_1000.log")

# All major dining towns in Connecticut (excluding New Canaan)
ALL_TARGET_TOWNS = [
    "Stamford", "Norwalk", "Bridgeport", "New Haven", "Hartford", "Waterbury",
    "Danbury", "West Hartford", "Greenwich", "Fairfield", "Milford", "Stratford",
    "Manchester", "Bristol", "Meriden", "West Haven", "Hamden", "Middletown",
    "Enfield", "Southington", "Shelton", "Groton", "Norwich", "Torrington",
    "Trumbull", "Glastonbury", "Naugatuck", "Newington", "Cheshire", "East Hartford",
    "Vernon", "Windsor", "Wethersfield", "Mansfield", "Westport", "South Windsor",
    "Farmington", "Ridgefield", "Simsbury", "North Haven", "Watertown", "Guilford",
    "Bloomfield", "Darien", "Rocky Hill", "Bethel", "Wilton", "Berlin",
    "Waterford", "Branford", "Orange", "Plainville", "Cromwell", "Seymour",
    "Derby", "Ansonia", "Southbury", "Oxford", "Brookfield", "New Fairfield",
    "Avon", "Woodbury", "Prospect", "Newtown", "Monroe"
]

CATEGORIES = [
    "restaurant", "cafe", "pizzeria", "deli", "bakery",
    "tacos", "diner", "coffee", "bagels", "grill", "bistro",
    "mexican", "seafood", "bbq", "burgers", "sushi",
    "italian", "thai", "pub", "steakhouse",
    "ramen", "cantina", "brewery", "creperie", "sandwich", "noodles"
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

def checkpoint_deploy(current_count: int, total_target: int):
    """Rebuilds registry, runs build, and pushes to git/Vercel."""
    log(f"🚀 [CHECKPOINT #{current_count}/{total_target}] Deploying batch to Vercel...")
    try:
        update_registry_file()
        cwd = os.path.join(SCRAPER_DIR, "..")
        # Git commit and push
        subprocess.run(
            ["git", "add", "data/merchants/", "app/page.tsx", "scraper/"],
            cwd=cwd, check=True, capture_output=True
        )
        commit_msg = f"feat(merchants): overnight checkpoint ({current_count}/{total_target} places)"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=cwd, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=cwd, check=True, capture_output=True
        )
        log(f"✅ [CHECKPOINT #{current_count}] Successfully pushed to GitHub & triggered Vercel deployment!")
    except Exception as e:
        log(f"⚠️ [CHECKPOINT WARNING] Auto-deploy notice: {e}")

def run_overnight_1000(target_count: int = 1000):
    log("=" * 68)
    log(" 🌙 DuoTaps Overnight 1,000 Lead Scraper & Custom Page Generator")
    log(f" Target to confirm & build: {target_count} places")
    log(f" Excluded: {', '.join(sorted(EXCLUDED_TOWNS))}")
    log("=" * 68)

    # 1. Connect to Google Sheet
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

    log(f"📊 Google Sheet currently has {len(all_rows)-1} rows.")
    log(f"   Current Balance: {ig_count} Instagram / {fb_count} Facebook")

    # 2. Existing local merchant slugs
    existing_slugs = set()
    if os.path.exists(MERCHANTS_DIR):
        for f in os.listdir(MERCHANTS_DIR):
            if f.endswith(".json"):
                existing_slugs.add(f[:-5].lower())

    # 3. Initialize scraper
    scraper = SocialLeadScraper(delay_min=0.2, delay_max=0.5)
    scraper.seen_profiles = set(existing_links)
    scraper.seen_names = set(existing_names)
    scraper.ig_assigned_count = ig_count
    scraper.fb_assigned_count = fb_count

    confirmed_and_created = 0
    pending_sheet_rows: List[List[str]] = []

    # Loop through randomized town batches until 1,000 target is reached
    while confirmed_and_created < target_count:
        town_priority = list(ALL_TARGET_TOWNS)
        random.shuffle(town_priority)

        for town in town_priority:
            if confirmed_and_created >= target_count:
                break

            if any(ex in town.lower() for ex in EXCLUDED_TOWNS):
                continue

            log(f"\n📍 Scanning Town: {town}, CT (Progress: {confirmed_and_created}/{target_count})")

            # Discover candidates via Nominatim OSM
            candidates = []
            for cat in CATEGORIES:
                if confirmed_and_created >= target_count:
                    break
                osm_results = scraper.query_nominatim_osm(town, cat, limit=10)
                for item in osm_results:
                    norm = normalize_biz_name(item["business_name"])
                    if norm and norm not in scraper.seen_names:
                        scraper.seen_names.add(norm)
                        candidates.append(item)

            log(f"   Found {len(candidates)} new candidates in {town}.")

            for c in candidates:
                if confirmed_and_created >= target_count:
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

                if re.search(r"\b(Avenue|Ave|Street|St|Road|Rd|Boulevard|Blvd|Highway|Hwy|Lane|Ln|Drive|Dr|Route|Rt|Way|Terrace)\b", biz_name, re.I):
                    if not re.search(r"\b(Cafe|Café|Bistro|Pizzeria|Kitchen|Grill|Bakery|Deli|Tavern|Bar|Diner|Restaurant|House|Shop|Bagel|Pizza|Coffee|Roasters|Brewing|Ale|Steakhouse|BBQ|Tapas|Seafood|Cantina|Pub)\b", biz_name, re.I):
                        continue

                if target_site and (not ig_profile or not fb_profile):
                    site_ig, site_fb = scraper.crawl_site_for_socials(target_site)
                    if site_ig and not ig_profile:
                        ig_profile = site_ig
                    if site_fb and not fb_profile:
                        fb_profile = site_fb

                # Verification
                ig_is_live = False
                fb_is_live = False

                if ig_profile:
                    ig_is_live = is_profile_live("Instagram", ig_profile[0], ig_profile[1])
                if fb_profile:
                    fb_is_live = is_profile_live("Facebook", fb_profile[0], fb_profile[1])

                # 50/50 Channel Balance
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

                # --- CONFIRMED PLACE: GENERATE CUSTOM DEMO PAGE ---
                log(f"✨ [CONFIRMED #{confirmed_and_created+1}/{target_count}] {biz_name} ({town}, CT)")
                log(f"   Platform: {chosen_platform} ({chosen_handle}) | Site: {target_site or 'N/A'}")

                slug = base_slug
                json_path = os.path.join(MERCHANTS_DIR, f"{slug}.json")
                live_url = f"https://language-tool-six.vercel.app/{slug}"

                # 1. Scrape real menu content
                scraped_content = ""
                if target_site and target_site.startswith("http"):
                    scraped_content = scrape_website_content(target_site)

                # 2. Call Gemini for bilingual custom page configuration
                try:
                    config = generate_merchant_config_with_gemini(
                        biz_name=biz_name,
                        location=f"{town}, CT",
                        website=target_site or "",
                        scraped_content=scraped_content,
                        slug=slug
                    )

                    # 3. Save JSON
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(config, jf, indent=2, ensure_ascii=False)
                    existing_slugs.add(slug.lower())

                    # 4. Queue for batched Google Sheet append
                    new_row = [
                        biz_name,
                        f"{town}, CT",
                        chosen_platform,
                        chosen_handle,
                        chosen_link,
                        target_site or "N/A",
                        "Not Contacted",
                        "",
                        "",
                        live_url
                    ]
                    pending_sheet_rows.append(new_row)
                    confirmed_and_created += 1

                    # Flush to Google Sheet every 10 places
                    if len(pending_sheet_rows) >= 10:
                        try:
                            sheet.append_rows(pending_sheet_rows, value_input_option="USER_ENTERED")
                            log(f"   📊 Flushed {len(pending_sheet_rows)} leads to Google Sheet.")
                            pending_sheet_rows = []
                        except Exception as se:
                            log(f"   ⚠️ Sheet flush warning: {se}")

                    # Checkpoint deploy every 50 places
                    if confirmed_and_created % 50 == 0:
                        # Flush any pending sheet rows first
                        if pending_sheet_rows:
                            try:
                                sheet.append_rows(pending_sheet_rows, value_input_option="USER_ENTERED")
                                pending_sheet_rows = []
                            except Exception:
                                pass
                        checkpoint_deploy(confirmed_and_created, target_count)

                    time.sleep(1.0) # Polite pacing

                except Exception as e:
                    log(f"   ❌ Error generating custom page for {biz_name}: {e}")
                    time.sleep(2.0)

    # Final cleanup: flush remaining sheet rows and rebuild registry
    if pending_sheet_rows:
        try:
            sheet.append_rows(pending_sheet_rows, value_input_option="USER_ENTERED")
            log(f"📊 Final flush of {len(pending_sheet_rows)} leads to Google Sheet.")
            pending_sheet_rows = []
        except Exception:
            pass

    checkpoint_deploy(confirmed_and_created, target_count)

    log("\n" + "=" * 68)
    log(f"🎉 Overnight Run Complete! Successfully created {confirmed_and_created} new places.")
    log(f"   Final Balance: {scraper.ig_assigned_count} Instagram / {scraper.fb_assigned_count} Facebook")
    log("=" * 68)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    run_overnight_1000(target_count=count)
