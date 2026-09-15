#!/usr/bin/env python3
"""
Overnight Continuous CT Local Business Lead Scraper
Runs continuously in an endless loop across all target CT towns.
1. Strictly extracts 100% verified real emails (Web, Contact Pages, JSON-LD, Facebook Page Intro).
2. Deduplicates leads by business name & email.
3. Excludes email-less businesses (Google Sheet receives ONLY verified emails).
4. Auto-syncs live to Google Sheet after each town pass.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from local_lead_scraper import StrictVerifiedLeadScraper, export_to_csv
from export_to_gsheets import sync_to_google_sheet

ALL_CT_TARGET_TOWNS = [
    "Norwalk", "Wilton", "Darien", "Westport", "Fairfield",
    "Ridgefield", "Weston", "Trumbull", "Stratford", "Bridgeport",
    "Milford", "Orange", "Shelton", "Bethel", "Danbury", "Newtown", "Monroe"
]

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1twWEsJ6jpAUEDd0zpF8lWOgkNoFWPjpRrlZV34gqkn4/edit?gid=0#gid=0"

def run_overnight_loop():
    print("==================================================")
    print(" 🌙 OVERNIGHT CONTINUOUS CT LOCAL LEAD SCRAPER")
    print("==================================================")
    print(f"Target Towns: {', '.join(ALL_CT_TARGET_TOWNS)}")
    print("Strict Policy: NO Stamford, NO New Canaan, NO Greenwich.")
    print("Filter: VERIFIED REAL EMAILS ONLY + STRICT DEDUPLICATION.")
    print("==================================================\n")

    scraper = StrictVerifiedLeadScraper(delay_min=1.0, delay_max=2.5)

    iteration = 1
    while True:
        print(f"\n🚀 --- Starting Overnight Pass #{iteration} ---")
        try:
            leads = scraper.scrape_leads_for_towns(ALL_CT_TARGET_TOWNS, max_per_town=30)
            if leads:
                export_to_csv(leads, "local_business_leads.csv")
                sync_to_google_sheet(GSHEET_URL, csv_path="local_business_leads.csv")
                print(f"✅ Pass #{iteration} complete! Synced {len(leads)} verified email leads live.")
        except Exception as e:
            print(f"⚠️ Pass #{iteration} encountered an error: {e}")

        print(f"💤 Resting 60 seconds before Pass #{iteration + 1}...\n")
        time.sleep(60)
        iteration += 1

if __name__ == "__main__":
    run_overnight_loop()
