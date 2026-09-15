#!/usr/bin/env python3
"""
Continuous Social Media Lead Scraper for DuoTaps (Instagram & Facebook)
Features:
- Balanced 50/50 Output: Balances Instagram and Facebook so you can maximize outreach on both channels.
- Live Profile Verification: Every link is tested live so dead/broken pages are rejected.
- Strict Exclusions: ONLY New Canaan is excluded (Stamford, Greenwich, Norwalk, etc. are included).
- Append-Only: Preserves all current rows and notes in Google Sheet, only appends new leads.
"""

import os
import sys
import time
import random
from typing import List, Dict

import gspread
from google.oauth2.service_account import Credentials

import sys
sys.path.append(os.path.dirname(__file__))

from social_lead_scraper import SocialLeadScraper, is_profile_live, export_to_csv, EXCLUDED_TOWNS
from export_to_social_gsheet import sync_social_leads_to_gsheet

CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"

TARGET_TOWNS = [
    "Stamford",
    "Greenwich",
    "Norwalk",
    "Westport",
    "Fairfield",
    "Darien",
    "Wilton",
    "Ridgefield",
    "Bridgeport",
    "Trumbull",
    "Milford",
    "Stratford",
    "Shelton",
    "Bethel",
    "Danbury",
    "Newtown",
    "Monroe",
    "Orange",
    "West Haven",
    "Derby",
    "Ansonia"
]

def run_continuous_scraper():
    print("=" * 65)
    print(" 🚀 DuoTaps Balanced Social Media Lead Scraper (IG & FB)")
    print("=" * 65)
    print(f"Excluded Towns: {', '.join(sorted(EXCLUDED_TOWNS))}")
    print(f"Target Towns: {', '.join(TARGET_TOWNS)}")
    print(f"Destination: Google Sheet '{SPREADSHEET_TITLE}' (Append-Only)")
    print("=" * 65)

    cycle = 1
    while True:
        print(f"\n🔄 === Starting Discovery Cycle #{cycle} ===")
        scraper = SocialLeadScraper(delay_min=0.5, delay_max=1.0)
        
        # Read current sheet to seed seen links and populate existing IG vs FB balance
        if os.path.exists(CREDENTIALS_JSON):
            try:
                scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
                creds = Credentials.from_service_account_file(CREDENTIALS_JSON, scopes=scopes)
                gc = gspread.authorize(creds)
                sheet = gc.open(SPREADSHEET_TITLE).sheet1
                vals = sheet.get_all_values()
                for r in vals[1:]:
                    if len(r) >= 5 and r[4]:
                        scraper.seen_profiles.add(r[4].strip().lower())
                    if len(r) >= 3:
                        if r[2].lower() == "instagram":
                            scraper.ig_assigned_count += 1
                        elif r[2].lower() == "facebook":
                            scraper.fb_assigned_count += 1
                print(f"   Current Sheet Balance: {scraper.ig_assigned_count} Instagram / {scraper.fb_assigned_count} Facebook")
            except Exception as e:
                print(f"   Sheet read notice: {e}")

        # Shuffle towns for organic discovery
        town_batch = list(TARGET_TOWNS)
        random.shuffle(town_batch)

        leads = scraper.scrape_leads_for_towns(town_batch, max_per_town=15)
        if leads:
            csv_path = os.path.join(os.path.dirname(__file__), "..", "social_business_leads.csv")
            export_to_csv(leads, csv_path)
            added = sync_social_leads_to_gsheet(leads, SPREADSHEET_TITLE)
            print(f"📊 Cycle #{cycle} completed: Appended {added} new verified leads.")

        cycle += 1
        sleep_mins = random.randint(10, 20)
        print(f"⏳ Sleeping for {sleep_mins} minutes before next discovery cycle...")
        time.sleep(sleep_mins * 60)

if __name__ == "__main__":
    run_continuous_scraper()
