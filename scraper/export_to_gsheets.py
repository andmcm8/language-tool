#!/usr/bin/env python3
"""
Smart Google Sheets API Sync Script with Strict Email Filtering & Deduplication.
Policy: ONLY uploads businesses with verified email addresses. Completely excludes any entries without an email.
Ensures zero duplicate business names or duplicate email addresses in the Google Sheet.
"""

import os
import csv
import re
import argparse
from typing import List, Dict, Set
import gspread

def normalize_name(name: str) -> str:
    """Normalize business name for duplicate checking."""
    if not name:
        return ""
    clean = name.lower()
    clean = re.sub(r"\(.*?\)", "", clean)
    clean = re.sub(r"[^\w\s]", "", clean)
    clean = re.sub(r"\b(norwalk|wilton|darien|ct|connecticut)\b", "", clean)
    return " ".join(clean.split())

def normalize_email(email: str) -> str:
    """Normalize email address for duplicate checking."""
    if not email or email.lower().strip() == "needs verification":
        return ""
    return email.lower().strip()

def deduplicate_and_filter_leads(rows: List[List[str]]) -> List[List[str]]:
    """
    1. STRICTLY FILTERS OUT entries with empty emails or 'Needs Verification'.
    2. Deduplicates lead rows based on business name and email address.
    """
    if not rows or len(rows) <= 1:
        return rows

    header = rows[0]
    data_rows = rows[1:]

    unique_map: Dict[str, List[str]] = {}
    seen_emails: Set[str] = set()

    for row in data_rows:
        if len(row) < 2:
            continue

        biz_name = row[0]
        email = row[1]

        norm_em = normalize_email(email)

        # STRICT FILTER: Exclude any business without a real email
        if not norm_em:
            continue

        norm_biz = normalize_name(biz_name)

        # Skip duplicate email if already seen for another business entry
        if norm_em in seen_emails and norm_biz not in unique_map:
            continue

        unique_map[norm_biz] = row
        seen_emails.add(norm_em)

    return [header] + list(unique_map.values())

def sync_to_google_sheet(sheet_url: str, credentials_json: str = "service_account.json", csv_path: str = "local_business_leads.csv"):
    if not os.path.exists(credentials_json):
        print(f"❌ Error: Google Service Account credentials file '{credentials_json}' not found.")
        return

    if not os.path.exists(csv_path):
        print(f"❌ Error: Lead file '{csv_path}' not found. Run the scraper first.")
        return

    print("🔑 Authenticating with Google Sheets API...")
    try:
        gc = gspread.service_account(filename=credentials_json)
        sheet = gc.open_by_url(sheet_url).sheet1

        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)

        if not data or len(data) <= 1:
            print("CSV has no lead entries to sync.")
            return

        header_mapping = {
            "business_name": "Business Name",
            "email": "Email",
            "location": "Location",
            "google_profile_url": "Google Profile",
            "verified": "Verified",
            "outreach_status": "Outreach Status",
            "notes": "Notes / Follow Up"
        }

        raw_headers = data[0]
        display_headers = [header_mapping.get(h, h.title().replace("_", " ")) for h in raw_headers]
        
        all_raw_rows = [display_headers] + data[1:]

        cleaned_rows = deduplicate_and_filter_leads(all_raw_rows)

        print(f"📤 Uploading {len(cleaned_rows) - 1} verified email leads to Google Sheet (Zero Email-less Rows)...")
        sheet.clear()
        sheet.update(range_name="A1", values=cleaned_rows)

        print("✅ Successfully updated live Google Sheet with ONLY verified email leads!")
        print(f"🔗 View Sheet: {sheet_url}")

    except Exception as e:
        print(f"❌ Error syncing to Google Sheets: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sync verified leads directly to Google Sheets")
    parser.add_argument("--url", type=str, required=True, help="Full URL of your target Google Sheet")
    parser.add_argument("--credentials", type=str, default="service_account.json", help="Path to Google service_account.json")
    parser.add_argument("--csv", type=str, default="local_business_leads.csv", help="Source CSV file")

    args = parser.parse_args()
    sync_to_google_sheet(args.url, args.credentials, args.csv)

if __name__ == "__main__":
    main()
