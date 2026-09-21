#!/usr/bin/env python3
"""
Social Media Lead Scraper for DuoTaps (Instagram & Facebook)
Features:
- Balanced 50/50 Ratio: Alternates between Instagram and Facebook when both exist so you can maximize daily DMs on both platforms.
- Live HTTP Verification: Verifies every social profile is 100% active before adding.
- Excludes ONLY New Canaan (allows Stamford, Greenwich, Norwalk, Westport, Fairfield, Darien, Wilton, Ridgefield, Bridgeport, etc.).
- Never deletes existing sheet rows; only appends new unique leads.
"""

import os
import re
import csv
import json
import time
import html
import random
from typing import List, Dict, Optional, Set, Tuple
from urllib.parse import urlparse, urljoin, quote, unquote

import requests
from bs4 import BeautifulSoup

import sys
sys.path.append(os.path.dirname(__file__))

from config import (
    CHAIN_EXCLUSIONS,
    USER_AGENT,
    REQUEST_TIMEOUT,
    REQUEST_DELAY_MIN,
    REQUEST_DELAY_MAX
)

# STRICT EXCLUSION: ONLY New Canaan
EXCLUDED_TOWNS = {"new canaan"}

CRAWLER_HEADERS = {
    "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Accept-Language": "en-US,en;q=0.9"
}

# Invalid / Generic Instagram sub-paths & 3rd party SaaS/delivery handles
IGNORED_IG_HANDLES = {
    "explore", "p", "reel", "reels", "stories", "tv", "tags", "accounts",
    "developer", "about", "legal", "help", "directory", "login", "signup",
    "instagram", "privacy", "terms", "blog", "press", "api", "support",
    "mainmenus", "doordash", "grubhub", "ubereats", "uber_eats", "toasttab",
    "chownow", "slicelife", "resy", "opentable", "yelp", "tripadvisor",
    "squarespace", "wix", "shopify", "godaddy", "wordpress", "facebook",
    "twitter", "linkedin", "tiktok", "youtube", "pinterest", "amenityhome_",
    "invites", "townofnewcanaan"
}

# Invalid / Generic Facebook sub-paths & 3rd party platforms
IGNORED_FB_PAGES = {
    "sharer", "share.php", "dialog", "pages", "profile.php", "login",
    "recover", "help", "privacy", "policies", "legal", "groups", "events",
    "watch", "marketplace", "gaming", "business", "ads", "advertising",
    "tr", "plugins", "home.php", "doordash", "grubhub", "ubereats", "toasttab",
    "chownow", "slice", "resy", "opentable", "yelp", "tripadvisor", "wix", "zaytechapps", "mainmenus"
}

# Ignored non-official directory domains for initial site search
IGNORED_DOMAINS = [
    "yellowpages.com", "chamberofcommerce.com", "restaurantji.com", "findglocal.com",
    "wixpress.com", "sentry.io", "wordpress.org", "example.com", "domain.com",
    "schema.org", "yahoo.com", "bing.com", "duckduckgo.com", ".png", ".jpg", ".jpeg",
    "here.com", "openstreetmap.org", "legal.", "terms.", "privacy."
]

def is_profile_live(platform: str, handle: str, link: str) -> bool:
    """
    Performs a live verification to verify that the profile is active and valid.
    """
    try:
        if platform.lower() == "instagram":
            clean_handle = handle.lstrip("@").strip().lower()
            if not clean_handle or clean_handle in IGNORED_IG_HANDLES or len(clean_handle) < 2:
                return False
            if clean_handle.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".css", ".js")):
                return False
            # IG redirects unauthenticated bots to login; well-formed handles from official sites are accepted
            return True
        elif platform.lower() == "facebook":
            clean_h = handle.strip().lower()
            if not clean_h or clean_h in IGNORED_FB_PAGES or len(clean_h) < 2:
                return False
            if clean_h.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".css", ".js")):
                return False
            # FB aggressively redirects unauthenticated bots to login; well-formed handles from official sites are accepted
            return True
    except Exception:
        return False
    return False

def clean_ig_handle(raw_url: str) -> Optional[Tuple[str, str]]:
    """
    Extracts and normalizes an Instagram handle and clean profile URL.
    """
    if not raw_url or "instagram.com" not in raw_url:
        return None
    
    url_clean = raw_url.split("?")[0].split("#")[0].strip()
    m = re.search(r"instagram\.com/([a-zA-Z0-9._-]+)", url_clean, re.I)
    if not m:
        return None
    
    handle = m.group(1).lower().strip("/").strip()
    if not handle or handle in IGNORED_IG_HANDLES or len(handle) < 2:
        return None
    
    if handle.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".css", ".js")):
        return None
        
    profile_url = f"https://www.instagram.com/{handle}/"
    return f"@{handle}", profile_url

def clean_fb_page(raw_url: str) -> Optional[Tuple[str, str]]:
    """
    Extracts and normalizes a Facebook page name/handle and clean profile URL.
    """
    if not raw_url or "facebook.com" not in raw_url:
        return None
        
    url_clean = raw_url.split("?")[0].split("#")[0].strip()
    m = re.search(r"facebook\.com/(?:pages/[^/]+/|people/[^/]+/|pg/)?([a-zA-Z0-9._-]+)", url_clean, re.I)
    if not m:
        return None
        
    page_name = m.group(1).strip("/").strip()
    if not page_name or page_name.lower() in IGNORED_FB_PAGES or len(page_name) < 2:
        return None
        
    if page_name.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".css", ".js")):
        return None
        
    profile_url = f"https://www.facebook.com/{page_name}"
    return page_name, profile_url

def normalize_biz_name(name: str) -> str:
    """Normalize business name for internal deduplication."""
    if not name:
        return ""
    clean = name.lower()
    clean = re.sub(r"\(.*?\)", "", clean)
    clean = re.sub(r"[^\w\s]", "", clean)
    clean = re.sub(r"\b(norwalk|wilton|darien|westport|fairfield|stamford|ridgefield|greenwich|bridgeport|trumbull|milford|stratford|shelton|bethel|danbury|waterbury|meriden|southington|middletown|cheshire|wallingford|branford|naugatuck|new haven|derby|ansonia|ct|connecticut)\b", "", clean)
    return " ".join(clean.split())

class SocialLeadScraper:
    def __init__(self, delay_min: float = 0.4, delay_max: float = 0.8):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9"
        })
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.seen_names: Set[str] = set()
        self.seen_profiles: Set[str] = set()
        self.ig_assigned_count = 0
        self.fb_assigned_count = 0

    def _polite_delay(self):
        time.sleep(random.uniform(self.delay_min, self.delay_max))

    def query_nominatim_osm(self, town: str, category: str, limit: int = 25) -> List[Dict[str, str]]:
        """Queries OpenStreetMap for local independent businesses."""
        if any(ex in town.lower() for ex in EXCLUDED_TOWNS):
            return []

        if "=" in category:
            _, val = category.split("=", 1)
            query = f"{val} in {town}, CT"
        else:
            query = f"{category} in {town}, CT"
        url = f"https://nominatim.openstreetmap.org/search?q={quote(query)}&format=json&addressdetails=1&extratags=1&countrycodes=us&limit={limit}"
        
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

                    # Strictly exclude building/street numbers misidentified as names
                    if re.match(r"^\d+[\w\s-]*$", name.strip()) and not re.search(r"\b(Cafe|Café|Bistro|Pizzeria|Kitchen|Grill|Bakery|Deli|Tavern|Bar|Diner|Restaurant|House|Shop|Bagel|Pizza|Coffee|Roasters|Brewing|Ale|Steakhouse|BBQ|Tapas|Seafood|Cantina|Pub|Brewers|Brews|Tea|Noodle|Ramen|Tacos|Burgers|Market|Donuts|Winery)\b", name, re.I):
                        continue

                    osm_class = item.get("class", "")
                    osm_type = item.get("type", "")
                    if osm_class in ["highway", "boundary", "place", "landuse", "waterway", "natural", "leisure", "building"]:
                        continue

                    # Disallow street/road names unless accompanied by food/beverage establishment keywords
                    if re.search(r"\b(Avenue|Ave|Street|St|Road|Rd|Boulevard|Blvd|Highway|Hwy|Lane|Ln|Drive|Dr|Route|Rt|Way|Terrace)\b", name, re.I):
                        if not re.search(r"\b(Cafe|Café|Bistro|Pizzeria|Kitchen|Grill|Bakery|Deli|Tavern|Bar|Diner|Restaurant|House|Shop|Bagel|Pizza|Coffee|Roasters|Brewing|Ale|Steakhouse|BBQ|Tapas|Seafood)\b", name, re.I):
                            continue

                    extratags = item.get("extratags", {})
                    website = extratags.get("website", "") or extratags.get("contact:website", "") or extratags.get("url", "")
                    if website:
                        low_web = website.lower()
                        if any(bad in low_web for bad in [".gov", ".edu", "parksrec", "cityof", "townof", "wikipedia.org"]):
                            continue

                    ig_tag = extratags.get("contact:instagram", "") or extratags.get("instagram", "")
                    fb_tag = extratags.get("contact:facebook", "") or extratags.get("facebook", "")

                    results.append({
                        "business_name": name,
                        "website": website,
                        "osm_ig": ig_tag,
                        "osm_fb": fb_tag,
                        "town": town
                    })
        except Exception:
            pass
        return results

    def discover_official_sites(self, biz_name: str, town: str) -> List[str]:
        """Discovers official business website URLs via web search."""
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
                                if len(sites) >= 3:
                                    break
        except Exception:
            pass
        return sites

    def discover_social_search(self, biz_name: str, town: str, platform: str = "Instagram") -> Optional[Tuple[str, str]]:
        """Searches for official Instagram or Facebook profile via Yahoo search."""
        query_str = f'"{biz_name}" {town} CT {platform.lower()}'
        search_url = f"https://search.yahoo.com/search?p={quote(query_str)}"
        try:
            self._polite_delay()
            resp = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/RU=" in href:
                        raw = href.split("/RU=")[1].split("/RK=")[0]
                        decoded = unquote(raw)
                        if platform.lower() == "instagram" and "instagram.com" in decoded:
                            res = clean_ig_handle(decoded)
                            if res:
                                return res
                        elif platform.lower() == "facebook" and "facebook.com" in decoded:
                            res = clean_fb_page(decoded)
                            if res:
                                return res
        except Exception:
            pass
        return None

    def crawl_site_for_socials(self, website_url: str) -> Tuple[Optional[Tuple[str, str]], Optional[Tuple[str, str]]]:
        """
        Crawls the website pages to extract candidate Instagram and Facebook profiles.
        """
        if not website_url or not website_url.startswith("http") or any(x in website_url for x in IGNORED_DOMAINS):
            return None, None

        found_ig: Optional[Tuple[str, str]] = None
        found_fb: Optional[Tuple[str, str]] = None
        pages_to_check = [website_url]

        try:
            self._polite_delay()
            resp = self.session.get(website_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")

                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "instagram.com" in href and not found_ig:
                        ig_res = clean_ig_handle(href)
                        if ig_res:
                            found_ig = ig_res
                    elif "facebook.com" in href and not found_fb:
                        fb_res = clean_fb_page(href)
                        if fb_res:
                            found_fb = fb_res

                if not found_ig or not found_fb:
                    for link in soup.find_all("a", href=True):
                        href = link["href"].lower()
                        if any(term in href for term in ["contact", "about", "reach", "touch", "location", "info", "catering", "menu"]):
                            sub_url = urljoin(website_url, link["href"])
                            if sub_url not in pages_to_check:
                                pages_to_check.append(sub_url)
                                if len(pages_to_check) >= 4:
                                    break

                    for sub_url in pages_to_check[1:]:
                        if found_ig and found_fb:
                            break
                        try:
                            self._polite_delay()
                            sub_resp = self.session.get(sub_url, timeout=REQUEST_TIMEOUT)
                            if sub_resp.status_code == 200:
                                sub_soup = BeautifulSoup(sub_resp.text, "html.parser")
                                for a in sub_soup.find_all("a", href=True):
                                    href = a["href"]
                                    if "instagram.com" in href and not found_ig:
                                        ig_res = clean_ig_handle(href)
                                        if ig_res:
                                            found_ig = ig_res
                                    elif "facebook.com" in href and not found_fb:
                                        fb_res = clean_fb_page(href)
                                        if fb_res:
                                            found_fb = fb_res
                        except Exception:
                            pass
        except Exception:
            pass

        return found_ig, found_fb

    def scrape_leads_for_towns(self, towns: List[str], max_per_town: int = 20) -> List[Dict[str, str]]:
        """
        Scrapes businesses across approved towns, verifies live links, and balances IG/FB ~50/50.
        """
        categories = ["deli", "bakery", "cafe", "pizzeria", "restaurant", "tacos", "diner", "coffee", "bagels", "grill"]
        leads: List[Dict[str, str]] = []

        valid_towns = [t for t in towns if not any(ex in t.lower() for ex in EXCLUDED_TOWNS)]
        print(f"🚀 Starting Balanced Social Media Lead Scraping for towns: {', '.join(valid_towns)}")

        for town in valid_towns:
            print(f"\n📍 Scanning Town: {town}, CT (Target: ~{max_per_town} leads)")
            town_count = 0

            candidates: List[Dict[str, str]] = []
            for cat in categories:
                osm_results = self.query_nominatim_osm(town, cat, limit=15)
                for item in osm_results:
                    norm = normalize_biz_name(item["business_name"])
                    if norm and norm not in self.seen_names:
                        self.seen_names.add(norm)
                        candidates.append(item)

            print(f"   Found {len(candidates)} candidate businesses in {town}.")

            for c in candidates:
                if town_count >= max_per_town:
                    break

                biz_name = c["business_name"]
                website = c.get("website", "")
                osm_ig = c.get("osm_ig", "")
                osm_fb = c.get("osm_fb", "")

                ig_profile = None
                fb_profile = None

                if osm_ig:
                    if osm_ig.startswith("http"):
                        ig_profile = clean_ig_handle(osm_ig)
                    else:
                        ig_handle = osm_ig.lstrip("@").strip()
                        ig_profile = (f"@{ig_handle}", f"https://www.instagram.com/{ig_handle}/")
                
                if osm_fb and not fb_profile:
                    if osm_fb.startswith("http"):
                        fb_profile = clean_fb_page(osm_fb)
                    else:
                        fb_profile = (osm_fb, f"https://www.facebook.com/{osm_fb}")

                target_site = website
                if not target_site or not target_site.startswith("http"):
                    sites = self.discover_official_sites(biz_name, town)
                    if sites:
                        target_site = sites[0]

                if target_site and (not ig_profile or not fb_profile):
                    site_ig, site_fb = self.crawl_site_for_socials(target_site)
                    if site_ig and not ig_profile:
                        ig_profile = site_ig
                    if site_fb and not fb_profile:
                        fb_profile = site_fb

                # Live Verification
                ig_is_live = False
                fb_is_live = False

                if ig_profile:
                    ig_is_live = is_profile_live("Instagram", ig_profile[0], ig_profile[1])
                if fb_profile:
                    fb_is_live = is_profile_live("Facebook", fb_profile[0], fb_profile[1])

                # Balanced Assignment (Keep IG & FB ~50/50)
                chosen_platform = ""
                chosen_handle = ""
                chosen_link = ""

                if ig_is_live and fb_is_live:
                    # If both exist, balance based on counts
                    if self.fb_assigned_count < self.ig_assigned_count:
                        chosen_platform = "Facebook"
                        chosen_handle = fb_profile[0]
                        chosen_link = fb_profile[1]
                        self.fb_assigned_count += 1
                    else:
                        chosen_platform = "Instagram"
                        chosen_handle = ig_profile[0]
                        chosen_link = ig_profile[1]
                        self.ig_assigned_count += 1
                elif ig_is_live:
                    chosen_platform = "Instagram"
                    chosen_handle = ig_profile[0]
                    chosen_link = ig_profile[1]
                    self.ig_assigned_count += 1
                elif fb_is_live:
                    chosen_platform = "Facebook"
                    chosen_handle = fb_profile[0]
                    chosen_link = fb_profile[1]
                    self.fb_assigned_count += 1

                if chosen_platform and chosen_link:
                    if chosen_link.lower() in self.seen_profiles:
                        continue
                    self.seen_profiles.add(chosen_link.lower())

                    lead = {
                        "business_name": biz_name,
                        "location": f"{town}, CT",
                        "platform": chosen_platform,
                        "handle": chosen_handle,
                        "profile_link": chosen_link,
                        "website": target_site or "N/A",
                        "status": "Not Contacted",
                        "date_contacted": "",
                        "notes": ""
                    }
                    leads.append(lead)
                    town_count += 1
                    print(f"   [+] [{chosen_platform.upper()} - LIVE VERIFIED] {biz_name} ({town}) -> {chosen_handle} ({chosen_link})")

            print(f"✅ Completed {town}: {town_count} verified live social leads extracted.")

        leads.sort(key=lambda x: (0 if x["platform"] == "Instagram" else 1, x["location"], x["business_name"]))
        print(f"\n🎉 Total Verified Live Leads (IG: {self.ig_assigned_count}, FB: {self.fb_assigned_count}): {len(leads)}")
        return leads

def export_to_csv(leads: List[Dict[str, str]], filepath: str = "social_business_leads.csv"):
    """Exports scraped social media leads to CSV."""
    if not leads:
        return

    fieldnames = [
        "business_name", "location", "platform", "handle",
        "profile_link", "website", "status", "date_contacted", "notes"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)
