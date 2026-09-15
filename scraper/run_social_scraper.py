#!/usr/bin/env python3
"""
Master Runner for Social Media Lead Scraper (Instagram & Facebook)
Scrapes verified Instagram and Facebook business profiles across Fairfield County, CT
and automatically synchronizes results to Google Sheet 'FaceBook/Instagram Scraper'.
"""

import os
import sys
import time

from social_lead_scraper import SocialLeadScraper, export_to_csv
from export_to_social_gsheet import sync_social_leads_to_gsheet

TARGET_TOWNS = [
    "Norwalk",
    "Westport",
    "Fairfield",
    "Stamford",
    "Darien",
    "Wilton",
    "Ridgefield",
    "Greenwich",
    "New Canaan",
    "Bridgeport"
]

def main():
    print("=" * 60)
    print(" 🚀 DuoTaps Social Media Lead Scraper (Instagram & Facebook)")
    print("=" * 60)
    print("Priority Rule: Exactly 1 primary profile per business (Instagram first, Facebook fallback)")
    print(f"Target Towns: {', '.join(TARGET_TOWNS)}")
    print("Destination: Google Sheet 'FaceBook/Instagram Scraper'")
    print("=" * 60)

    scraper = SocialLeadScraper(delay_min=0.4, delay_max=0.8)
    leads = scraper.scrape_leads_for_towns(TARGET_TOWNS, max_per_town=15)

    csv_file = os.path.join(os.path.dirname(__file__), "..", "social_business_leads.csv")
    export_to_csv(leads, csv_file)

    print("\n" + "=" * 60)
    print(" 📊 Synchronizing Verified Social Leads to Google Sheet...")
    print("=" * 60)
    added_count = sync_social_leads_to_gsheet(leads, "FaceBook/Instagram Scraper")

    print("\n" + "=" * 60)
    print(f" 🎉 DONE! Extracted {len(leads)} leads. Added {added_count} new leads to Google Sheet.")
    print("=" * 60)

if __name__ == "__main__":
    main()
