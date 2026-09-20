#!/usr/bin/env python3
"""
Sync Social Media Leads (Instagram & Facebook) to Google Sheet 'FaceBook/Instagram Scraper'
Safety:
- NEVER clears or modifies existing rows.
- Deduplicates against existing leads in the sheet by Profile Link and Business Name.
- Only appends brand-new unique records.
"""

import os
import sys
import csv
from typing import List, Dict

import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"

HEADERS = [
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

def sync_social_leads_to_gsheet(leads: List[Dict[str, str]], spreadsheet_title: str = SPREADSHEET_TITLE) -> int:
    """
    Appends new unique verified social leads into Google Sheet without modifying existing data.
    """
    if not os.path.exists(CREDENTIALS_JSON):
        print(f"❌ Error: Credentials not found at {CREDENTIALS_JSON}")
        return 0

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(CREDENTIALS_JSON, scopes=scopes)
    gc = gspread.authorize(creds)

    print(f"📊 Connecting to Google Sheet: '{spreadsheet_title}'...")
    try:
        sh = gc.open(spreadsheet_title)
    except Exception as e:
        print(f"❌ Error opening spreadsheet '{spreadsheet_title}': {e}")
        return 0

    sheet = sh.sheet1

    # 1. Read existing rows to guarantee 0 duplicates and preserve all user edits
    all_values = sheet.get_all_values()
    existing_links = set()
    existing_names = set()

    if not all_values:
        sheet.append_row(HEADERS)
        all_values = [HEADERS]
    else:
        for row in all_values[1:]:
            if len(row) >= 5 and row[4].strip():
                existing_links.add(row[4].strip().lower())
            if len(row) >= 1 and row[0].strip():
                existing_names.add(row[0].strip().lower())

    # 2. Filter new unique leads
    new_rows = []
    for lead in leads:
        link = lead.get("profile_link", "").strip()
        name = lead.get("business_name", "").strip()

        if not link or link.lower() in existing_links:
            continue
        if name and name.lower() in existing_names:
            continue

        existing_links.add(link.lower())
        if name:
            existing_names.add(name.lower())

        row = [
            lead.get("business_name", ""),
            lead.get("location", ""),
            lead.get("platform", ""),
            lead.get("handle", ""),
            lead.get("profile_link", ""),
            str(lead.get("followers", "")),
            lead.get("website", ""),
            lead.get("status", "Not Contacted"),
            lead.get("date_contacted", ""),
            lead.get("notes", ""),
            lead.get("custom_demo_link", "")
        ]
        new_rows.append(row)

    if not new_rows:
        print("ℹ️ No new unique leads to append. All leads already in Google Sheet!")
        return 0

    print(f"📥 Appending {len(new_rows)} brand-new verified social leads to Google Sheet...")
    sheet.append_rows(new_rows, value_input_option="USER_ENTERED")
    print(f"✅ Successfully appended! Total rows in sheet now: {len(all_values) + len(new_rows)}")

    return len(new_rows)

def sync_from_csv(csv_path: str, spreadsheet_title: str = SPREADSHEET_TITLE) -> int:
    """Reads a CSV file and appends it directly to the Google Sheet."""
    if not os.path.exists(csv_path):
        return 0

    leads = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    return sync_social_leads_to_gsheet(leads, spreadsheet_title)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith(".csv"):
        sync_from_csv(sys.argv[1])
