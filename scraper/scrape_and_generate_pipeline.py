#!/usr/bin/env python3
"""
Integrated Lead Scraper & Custom Merchant Page Generator for DuoTaps
Discovers uncontacted restaurants across Connecticut (excluding New Canaan),
verifies active Instagram and Facebook profiles (balanced 50/50),
scrapes their official menus, generates authentic bilingual Spanish pages with Gemini,
updates Google Sheets with live demo links, and rebuilds the merchant registry.
"""

import os
import sys
import re
import json
import time
import random
import urllib.parse
from typing import List, Dict, Any, Set, Tuple

import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ensure scraper dir is in sys.path
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

ALL_TARGET_TOWNS = [
    "Norwalk",
    "Danbury",
    "Fairfield",
    "West Haven",
    "Orange",
    "Greenwich",
    "Stamford",
    "Bridgeport",
    "Hamden",
    "Milford",
    "Stratford",
    "Shelton",
    "Trumbull",
    "Bethel",
    "Newtown",
    "Monroe",
    "Derby",
    "Ansonia",
    "Wallingford",
    "Branford",
    "Cheshire",
    "East Haven",
    "Naugatuck",
    "Waterbury",
    "Meriden",
    "Southington",
    "Middletown",
    "New Haven",
    "North Haven",
    "Hartford",
    "West Hartford",
    "Manchester",
    "Glastonbury",
    "Newington",
    "Wethersfield",
    "Rocky Hill",
    "Cromwell",
    "Berlin",
    "Bristol",
    "Plainville",
    "Farmington",
    "Avon",
    "Simsbury",
    "Torrington",
    "Watertown",
    "Prospect",
    "Seymour",
    "Oxford",
    "Southbury",
    "Woodbury",
    "Brookfield",
    "New Fairfield",
    "Westport",
    "Darien",
    "Wilton",
    "Ridgefield",
    "Enfield",
    "Groton",
    "Norwich",
    "East Hartford",
    "Vernon",
    "Windsor",
    "Mansfield",
    "South Windsor",
    "Guilford",
    "Bloomfield",
    "Waterford"
]

def run_pipeline(target_count: int = 20):
    print("=" * 65)
    print(" 🚀 DuoTaps Integrated Scrape & Instant Custom Page Pipeline")
    print(f" Target to confirm & build: {target_count} new places")
    print(f" Excluded: {', '.join(sorted(EXCLUDED_TOWNS))}")
    print("=" * 65)

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

    print(f"📊 Google Sheet currently has {len(all_rows)-1} rows.")
    print(f"   Balance: {ig_count} Instagram / {fb_count} Facebook")

    # 2. Existing local merchant slugs
    existing_slugs = set()
    if os.path.exists(MERCHANTS_DIR):
        for f in os.listdir(MERCHANTS_DIR):
            if f.endswith(".json"):
                existing_slugs.add(f[:-5].lower())

    # 3. Initialize scraper
    scraper = SocialLeadScraper(delay_min=0.3, delay_max=0.6)
    scraper.seen_profiles = set(existing_links)
    scraper.seen_names = set(existing_names)
    scraper.ig_assigned_count = ig_count
    scraper.fb_assigned_count = fb_count

    categories = [
        "restaurant", "cafe", "pizzeria", "deli", "bakery",
        "tacos", "diner", "coffee", "bagels", "grill", "bistro",
        "mexican", "seafood", "bbq", "burgers", "sushi",
        "italian", "thai", "pub", "steakhouse",
        "ramen", "cantina", "brewery", "creperie"
    ]

    # Prioritize towns with lowest representations first
    town_priority = list(ALL_TARGET_TOWNS)
    # Shuffle slightly within groups to vary queries
    random.shuffle(town_priority)

    confirmed_and_created = 0
    newly_created_merchants: List[Dict[str, str]] = []

    for town in town_priority:
        if confirmed_and_created >= target_count:
            break

        if any(ex in town.lower() for ex in EXCLUDED_TOWNS):
            continue

        print(f"\n📍 Scanning Town: {town}, CT (Progress: {confirmed_and_created}/{target_count})")

        # Discover candidates via Nominatim OSM
        candidates = []
        for cat in categories:
            if confirmed_and_created >= target_count:
                break
            osm_results = scraper.query_nominatim_osm(town, cat, limit=12)
            for item in osm_results:
                norm = normalize_biz_name(item["business_name"])
                if norm and norm not in scraper.seen_names:
                    scraper.seen_names.add(norm)
                    candidates.append(item)

        print(f"   Found {len(candidates)} candidates in {town}.")

        for c in candidates:
            if confirmed_and_created >= target_count:
                break

            biz_name = c["business_name"]
            website = c.get("website", "")
            osm_ig = c.get("osm_ig", "")
            osm_fb = c.get("osm_fb", "")

            # Deduplicate against existing slugs
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
                if not re.search(r"\b(Cafe|Café|Bistro|Pizzeria|Kitchen|Grill|Bakery|Deli|Tavern|Bar|Diner|Restaurant|House|Shop|Bagel|Pizza|Coffee|Roasters|Brewing|Ale|Steakhouse|BBQ|Tapas|Seafood)\b", biz_name, re.I):
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

            # Selection based on 50/50 balance
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

            # --- CONFIRMED PLACE! NOW IMMEDIATELY CREATE THE CUSTOM PAGE ---
            print(f"\n✨ [CONFIRMED #{confirmed_and_created+1}] {biz_name} ({town}, CT)")
            print(f"   Platform: {chosen_platform} ({chosen_handle}) | Site: {target_site or 'N/A'}")

            slug = base_slug
            json_path = os.path.join(MERCHANTS_DIR, f"{slug}.json")
            live_url = f"https://language-tool-six.vercel.app/{slug}"

            # 1. Scrape real menu content
            scraped_content = ""
            if target_site and target_site.startswith("http"):
                print(f"   🌐 Scraping menu content from {target_site}...")
                scraped_content = scrape_website_content(target_site)
                if scraped_content:
                    print(f"   ✅ Extracted {len(scraped_content)} chars of menu content.")

            # 2. Call Gemini for bilingual custom page configuration
            print(f"   🤖 Generating bilingual Spanish menu & AI assistant via Gemini...")
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
                print(f"   💾 Saved: data/merchants/{slug}.json ({len(config.get('products', []))} items)")

                # 4. Rebuild registry file
                update_registry_file()

                # 5. Append immediately to Google Sheet
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
                sheet.append_row(new_row, value_input_option="USER_ENTERED")
                print(f"   📊 Appended to Google Sheet: {live_url}")

                confirmed_and_created += 1
                newly_created_merchants.append({
                    "business_name": biz_name,
                    "location": f"{town}, CT",
                    "platform": chosen_platform,
                    "handle": chosen_handle,
                    "profile_link": chosen_link,
                    "website": target_site or "N/A",
                    "live_url": live_url
                })

                time.sleep(1.0) # Polite pacing

            except Exception as e:
                print(f"   ❌ Error generating custom page for {biz_name}: {e}")

    print("\n" + "=" * 65)
    print(f"🎉 Pipeline Batch Complete! Successfully created {confirmed_and_created} new places.")
    print(f"   Updated Balance: {scraper.ig_assigned_count} Instagram / {scraper.fb_assigned_count} Facebook")
    print("=" * 65)

    return newly_created_merchants

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    run_pipeline(target_count=count)
