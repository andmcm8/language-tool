#!/usr/bin/env python3
"""
CT Local Business Lead & Email Scraper (WEBSITE-NATIVE VERIFIED EMAILS ONLY)
Strict User Policy:
1. Emails MUST be physically extracted directly from the business's official live website pages
   (Homepage, /contact, /contact-us, /about, /catering, /locations, /menu).
2. Excludes third-party directories or non-website fallback sources.
3. Live DNS validation on every extracted email domain.
4. Built-in Strict Deduplication by Business Name & Email Address.
"""

import os
import re
import csv
import json
import time
import html
import socket
import random
import argparse
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse, urljoin, quote, unquote
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from config import (
    PRIORITY_TOWNS,
    SECONDARY_TOWNS,
    EXCLUDED_TOWNS,
    TARGET_SEARCH_TERMS,
    CHAIN_EXCLUSIONS,
    USER_AGENT,
    REQUEST_TIMEOUT,
    REQUEST_DELAY_MIN,
    REQUEST_DELAY_MAX
)

# Email Regex Patterns
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE
)

OBFUSCATED_EMAIL_REGEX = re.compile(
    r"([a-zA-Z0-9._%+-]+)\s*(?:\[at\]|\(at\)|@)\s*([a-zA-Z0-9.-]+)\s*(?:\[dot\]|\(dot\)|\.)\s*([a-zA-Z]{2,})",
    re.IGNORECASE
)

IGNORED_DOMAINS = [
    "yellowpages.com", "chamberofcommerce.com", "restaurantji.com", "findglocal.com",
    "wixpress.com", "wix.com", "sentry.io", "wordpress.org", "example.com", "domain.com",
    "mysite.com", "schema.org", "yahoo.com", "bing.com", "duckduckgo.com", "facebook.com", ".png", ".jpg", ".jpeg"
]

def has_active_dns(email: str) -> bool:
    """Verify recipient email domain has active DNS records."""
    if not email or "@" not in email:
        return False
    domain = email.split("@")[-1].strip()
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def sanitize_email(raw_email: str) -> str:
    """Clean and sanitize extracted email address string."""
    if not raw_email:
        return ""
    cleaned = html.unescape(raw_email).replace("\\u003e", ">").replace("\\u003c", "<")
    cleaned = re.sub(r"^(?:u003e|3e|gt|lt|>|<|&gt;|&lt;)+", "", cleaned, flags=re.I)
    m = EMAIL_REGEX.search(cleaned)
    if not m:
        return ""
    e = m.group(0).lower().strip()
    e = re.sub(r"^(?:u003e|3e|gt|lt|>|<)+", "", e)
    e = re.sub(r"^[0-9+() -]+(?=[a-zA-Z])", "", e)
    e = re.sub(r"(privacy|terms|cookies|disclaimer)$", "", e)
    
    domain = e.split("@")[-1] if "@" in e else ""
    if any(ign in domain for ign in ["yellowpages", "chamberofcommerce", "restaurantji", "findglocal", "wixpress", "sentry.io", "wordpress.org", "example.com", "domain.com", "mysite.com", "schema.org", "png", "jpg", "jpeg"]):
        return ""
    if len(e) < 6:
        return ""
    
    if not has_active_dns(e):
        return ""

    return e

def normalize_biz_name(name: str) -> str:
    """Normalize business name for internal deduplication."""
    if not name:
        return ""
    clean = name.lower()
    clean = re.sub(r"\(.*?\)", "", clean)
    clean = re.sub(r"[^\w\s]", "", clean)
    clean = re.sub(r"\b(norwalk|wilton|darien|ct|connecticut)\b", "", clean)
    return " ".join(clean.split())

class StrictVerifiedLeadScraper:
    def __init__(self, delay_min: float = REQUEST_DELAY_MIN, delay_max: float = REQUEST_DELAY_MAX):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        })
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.robots_cache: Dict[str, RobotFileParser] = {}

    def _polite_delay(self):
        time.sleep(random.uniform(self.delay_min, self.delay_max))

    def _can_fetch(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            robots_url = f"{base_url}/robots.txt"

            if base_url not in self.robots_cache:
                rp = RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                except Exception:
                    pass
                self.robots_cache[base_url] = rp
            return self.robots_cache[base_url].can_fetch(USER_AGENT, url)
        except Exception:
            return True

    def query_nominatim_osm(self, town: str, category: str, limit: int = 15) -> List[Dict[str, str]]:
        """Queries OpenStreetMap Nominatim for local independent businesses."""
        query = f"{category} in {town}, CT"
        url = f"https://nominatim.openstreetmap.org/search?q={quote(query)}&format=json&addressdetails=1&extratags=1&limit={limit}"
        
        results = []
        try:
            self._polite_delay()
            resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                for item in data:
                    name = item.get("display_name", "").split(",")[0].strip()
                    if not name or any(chain.lower() in name.lower() for chain in CHAIN_EXCLUSIONS):
                        continue

                    extratags = item.get("extratags", {})
                    website = extratags.get("website", "") or extratags.get("contact:website", "") or extratags.get("url", "")
                    email = extratags.get("email", "") or extratags.get("contact:email", "")

                    results.append({
                        "business_name": name,
                        "website": website,
                        "osm_email": email,
                        "town": town
                    })
        except Exception:
            pass
        return results

    def discover_official_sites(self, biz_name: str, town: str) -> List[str]:
        """Discovers candidate official website URLs via web search."""
        query_str = f"{biz_name} {town} CT official website"
        search_url = f"https://search.yahoo.com/search?p={quote(query_str)}"
        sites = []
        try:
            self._polite_delay()
            resp = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/RU=" in href:
                        decoded = unquote(href.split("/RU=")[1].split("/RK=")[0])
                        if decoded.startswith("http") and not any(x in decoded for x in IGNORED_DOMAINS):
                            if decoded not in sites:
                                sites.append(decoded)
                                if len(sites) >= 4:
                                    break
        except Exception:
            pass
        return sites

    def crawl_site_for_real_email(self, website_url: str) -> str:
        """
        WEBSITE-NATIVE EMAIL CRAWLER:
        Crawls the business's official live website pages (Homepage + /contact + /about + /catering + /menu)
        and extracts verified active emails directly from HTML DOM, mailto links, and JSON-LD microdata.
        """
        if not website_url or not website_url.startswith("http") or any(x in website_url for x in IGNORED_DOMAINS):
            return ""

        if not self._can_fetch(website_url):
            return ""

        found_emails: Set[str] = set()
        pages_to_check = [website_url]

        try:
            self._polite_delay()
            resp = self.session.get(website_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                page_text = unquote(html.unescape(resp.text))
                soup = BeautifulSoup(resp.text, "html.parser")

                self._extract_json_ld_emails(soup, found_emails)
                self._extract_emails_from_text_and_dom(page_text, soup, found_emails)

                # Collect subpages (/contact, /about, /locations, /catering, /menu)
                for link in soup.find_all("a", href=True):
                    href = link["href"].lower()
                    if any(term in href for term in ["contact", "about", "reach", "touch", "location", "team", "info", "catering", "menu"]):
                        sub_url = urljoin(website_url, link["href"])
                        if sub_url not in pages_to_check:
                            pages_to_check.append(sub_url)
                            if len(pages_to_check) >= 6:
                                break

                # Crawl subpages directly off their website
                for page_url in pages_to_check[1:]:
                    if self._can_fetch(page_url):
                        self._polite_delay()
                        sub_resp = self.session.get(page_url, timeout=REQUEST_TIMEOUT)
                        if sub_resp.status_code == 200:
                            sub_text = unquote(html.unescape(sub_resp.text))
                            sub_soup = BeautifulSoup(sub_resp.text, "html.parser")
                            self._extract_json_ld_emails(sub_soup, found_emails)
                            self._extract_emails_from_text_and_dom(sub_text, sub_soup, found_emails)
                            if found_emails:
                                break

        except Exception:
            pass

        for email in found_emails:
            clean = sanitize_email(email)
            if clean:
                return clean

        return ""

    def _extract_json_ld_emails(self, soup: BeautifulSoup, email_set: Set[str]):
        """Parses Schema.org JSON-LD blocks for real contact emails."""
        for s in soup.find_all("script", type="application/ld+json"):
            if not s.string:
                continue
            try:
                data = json.loads(s.string)
                if isinstance(data, dict):
                    if data.get("email"):
                        clean = sanitize_email(str(data["email"]))
                        if clean:
                            email_set.add(clean)
                    if isinstance(data.get("contactPoint"), dict) and data["contactPoint"].get("email"):
                        clean = sanitize_email(str(data["contactPoint"]["email"]))
                        if clean:
                            email_set.add(clean)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("email"):
                            clean = sanitize_email(str(item["email"]))
                            if clean:
                                email_set.add(clean)
            except Exception:
                pass

    def _extract_emails_from_text_and_dom(self, text: str, soup: BeautifulSoup, email_set: Set[str]):
        """Extract standard regex, obfuscated emails, and mailto attributes."""
        for m in EMAIL_REGEX.findall(text):
            clean = sanitize_email(m)
            if clean:
                email_set.add(clean)

        for m in OBFUSCATED_EMAIL_REGEX.findall(text):
            clean = sanitize_email(f"{m[0]}@{m[1]}.{m[2]}")
            if clean:
                email_set.add(clean)

        for elem in soup.find_all(["a", "button", "div", "span"]):
            for attr in ["href", "data-email", "data-mailto", "aria-label"]:
                val = elem.get(attr)
                if val and "mailto:" in str(val):
                    clean_m = sanitize_email(str(val).replace("mailto:", "").split("?")[0])
                    if clean_m:
                        email_set.add(clean_m)

    def extract_real_email_strictly(self, website_url: str, biz_name: str, town: str, osm_email: str = "") -> str:
        """
        STRICT WEBSITE-NATIVE REAL EMAIL PIPELINE:
        Emails MUST be physically extracted directly from the business's official live website pages.
        Returns empty string if no active email found directly on their website.
        """
        # 1. Primary: Crawl candidate website URL & contact subpages
        if website_url:
            crawled = self.crawl_site_for_real_email(website_url)
            if crawled:
                return crawled

        # 2. Secondary: Discover official business website via web search & crawl its subpages
        official_sites = self.discover_official_sites(biz_name, town)
        for site in official_sites[:4]:
            crawled = self.crawl_site_for_real_email(site)
            if crawled:
                return crawled

        return ""

    def scrape_leads_for_towns(self, towns: List[str], max_per_town: int = 20) -> List[Dict[str, str]]:
        """Main pipeline: Scrapes independent local business leads with website-verified emails ONLY."""
        all_leads = []
        seen_biz_names = set()
        seen_emails = set()

        for town in towns:
            if town in EXCLUDED_TOWNS:
                continue

            print(f"\n📍 Processing Town: {town.upper()} (Priority Target)")
            town_count = 0

            for cat in TARGET_SEARCH_TERMS:
                if town_count >= max_per_town:
                    break

                print(f"  🔍 Searching '{cat}' in {town}...")

                osm_biz_list = self.query_nominatim_osm(town, cat, limit=10)
                for biz in osm_biz_list:
                    if town_count >= max_per_town:
                        break

                    name = biz["business_name"]
                    norm_name = normalize_biz_name(name)

                    if norm_name in seen_biz_names:
                        continue

                    website = biz["website"]
                    osm_email = biz["osm_email"]

                    real_email = self.extract_real_email_strictly(website, name, town, osm_email)
                    norm_email = real_email.lower().strip()

                    # STRICT EMAIL-ONLY FILTER: Skip any business without a real email on their website
                    if not norm_email:
                        continue

                    if norm_email in seen_emails:
                        continue

                    seen_biz_names.add(norm_name)
                    seen_emails.add(norm_email)

                    google_profile_url = f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + town + ' CT')}"

                    all_leads.append({
                        "business_name": name,
                        "email": real_email,
                        "location": f"{town}, CT",
                        "google_profile_url": google_profile_url,
                        "verified": "[ ]",
                        "outreach_status": "Not Contacted",
                        "notes": ""
                    })
                    town_count += 1

        return all_leads

def export_to_csv(leads: List[Dict[str, str]], filename: str = "local_business_leads.csv"):
    """Export lead data to CSV."""
    if not leads:
        print("⚠️ No leads to export.")
        return

    fieldnames = ["business_name", "email", "location", "google_profile_url", "verified", "outreach_status", "notes"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    print(f"✅ Saved {len(leads)} website-verified email lead entries to '{filename}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CT Local Lead Scraper (Website-Native Verified Emails ONLY)")
    parser.add_argument("--towns", type=str, default="Norwalk,Wilton,Darien", help="Comma-separated list of CT towns")
    parser.add_argument("--max", type=int, default=20, help="Max leads per town")
    parser.add_argument("--out", type=str, default="local_business_leads.csv", help="Output CSV filepath")
    parser.add_argument("--gsheet", type=str, default="", help="Optional Google Sheet URL to sync")

    args = parser.parse_args()

    town_list = [t.strip() for t in args.towns.split(",") if t.strip()]

    scraper = StrictVerifiedLeadScraper()
    leads = scraper.scrape_leads_for_towns(town_list, max_per_town=args.max)
    export_to_csv(leads, args.out)

    if args.gsheet:
        try:
            from export_to_gsheets import sync_to_google_sheet
            sync_to_google_sheet(args.gsheet, csv_path=args.out)
        except ImportError:
            print("⚠️ Could not import export_to_gsheets module.")
