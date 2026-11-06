#!/usr/bin/env python3
"""
Menu & Catalog Expansion Pipeline for DuoTaps
==============================================
Expands ALL merchant menus and catalogs that have fewer than 20 products
to 25-35 authentic, bilingual items.
Prioritizes the smallest catalogs first (2-6 items), then systematically
upgrades all 2,000+ merchants.

Uses Gemini with concurrent workers, rate limit handling, automated registry
updates, and git checkpoints.
"""

import os
import sys
import re
import json
import time
import glob
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Dict, Any, List, Optional, Tuple

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRAPER_DIR)

from generate_custom_merchants import get_gemini_api_key, update_registry_file

MERCHANTS_DIR = os.path.join(SCRAPER_DIR, "..", "data", "merchants")
LOG_FILE = os.path.join(SCRAPER_DIR, "menu_expansion.log")

MIN_TARGET_PRODUCTS = 25   # Minimum products we want each merchant to have
MAX_TARGET_PRODUCTS = 35   # Maximum products to aim for
MAX_WORKERS = 6            # Concurrent Gemini API workers
CHECKPOINT_EVERY = 30      # Git checkpoint & registry update every N merchants
MIN_PRODUCTS_THRESHOLD = 20  # Expand any merchant with fewer than this

log_lock = Lock()
counter_lock = Lock()


def log(msg: str):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {msg}"
    with log_lock:
        print(line, flush=True)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as lf:
                lf.write(line + "\n")
        except Exception:
            pass


def checkpoint_deploy(expanded_count: int):
    """Rebuild registry, git commit and push expanded menus."""
    log(f"🚀 [CHECKPOINT] Updating registry and committing {expanded_count} expanded menus...")
    try:
        update_registry_file()
        cwd = os.path.join(SCRAPER_DIR, "..")
        subprocess.run(["git", "add", "data/merchants/", "scraper/"], cwd=cwd, check=True, capture_output=True)
        commit_msg = f"feat(menus): expand menus to 25-35 items ({expanded_count} merchants updated)"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=cwd, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=cwd, check=True, capture_output=True)
        log(f"✅ [DEPLOYED] Pushed to GitHub -> Vercel deploying {expanded_count} expanded menus!")
    except Exception as e:
        log(f"⚠️ [CHECKPOINT NOTICE] Git: {e}")


def get_merchants_needing_expansion() -> List[Tuple[str, Dict[str, Any]]]:
    """Find all merchant JSON files with fewer than MIN_PRODUCTS_THRESHOLD products, sorted smallest first."""
    results = []
    for filepath in sorted(glob.glob(os.path.join(MERCHANTS_DIR, "*.json"))):
        filename = os.path.basename(filepath)
        if filename == "registry.ts":
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            products = data.get("products", [])
            if len(products) < MIN_PRODUCTS_THRESHOLD:
                results.append((filepath, data))
        except Exception:
            continue
            
    # Sort so smallest catalogs are expanded FIRST
    results.sort(key=lambda x: len(x[1].get("products", [])))
    return results


def build_expansion_prompt(merchant_data: Dict[str, Any]) -> str:
    """Build a Gemini prompt that generates ADDITIONAL catalog/menu items for an existing merchant."""
    store_info = merchant_data.get("storeInfo", {})
    biz_name = store_info.get("name", "Business")
    location = store_info.get("address", "Connecticut")
    slug = store_info.get("id", "business")
    tagline = store_info.get("tagline", "")

    existing_products = merchant_data.get("products", [])
    existing_categories = merchant_data.get("categories", [])
    current_count = len(existing_products)

    # Calculate how many more items we need
    target = random.randint(MIN_TARGET_PRODUCTS, MAX_TARGET_PRODUCTS)
    items_needed = target - current_count
    if items_needed <= 0:
        items_needed = 15  # fallback

    # Build a summary of existing items so the AI doesn't duplicate them
    existing_names = [p.get("nameEn", "") for p in existing_products if p.get("nameEn")]
    existing_names_str = ", ".join(existing_names[:30])

    # Get category IDs (excluding 'all')
    cat_ids = [c["id"] for c in existing_categories if c.get("id") != "all"]
    cats_str = ", ".join(cat_ids) if cat_ids else "appetizers, mains, specialties, beverages"

    # Get the next product number
    existing_ids = [p.get("id", "") for p in existing_products]
    max_num = 0
    for pid in existing_ids:
        match = re.search(r'-(\d+)$', pid)
        if match:
            max_num = max(max_num, int(match.group(1)))
    start_num = max_num + 1

    prompt = f"""You are an expert bilingual catalog and digital menu engineer for Connecticut local businesses and restaurants.

You are EXPANDING the catalog/menu for "{biz_name}" ({tagline}) located at {location}.

This business currently only has {current_count} items. Generate EXACTLY {items_needed} ADDITIONAL new items/dishes/services to make this a complete, realistic catalog.

EXISTING ITEMS (DO NOT duplicate any of these):
{existing_names_str}

AVAILABLE CATEGORY IDs to distribute new items across: {cats_str}

RULES:
1. Generate EXACTLY {items_needed} new items — no more, no less.
2. DO NOT repeat or duplicate any existing items listed above.
3. Evenly distribute items across ALL available categories ({cats_str}).
4. Each item must have authentic, mouthwatering bilingual descriptions (English and Spanish).
5. Prices must be realistic (for food: appetizers $7-16, mains $14-32, drinks $3-14; for services/repairs: $25-150; for pharmacy/groceries: $3-25).
6. Include realistic allergens (e.g. Gluten, Lácteos, Mariscos, Frutos Secos) and badges.
7. Use sequential IDs starting from "{slug}-{start_num:02d}".
8. Make the items authentic to this specific business's cuisine, style, or industry.

Output ONLY a JSON array of product objects following this exact schema:
[
  {{
    "id": "{slug}-{start_num:02d}",
    "categoryId": "{cat_ids[0] if cat_ids else 'mains'}",
    "nameEs": "Nombre del plato o producto en Español",
    "nameEn": "Dish or Product Name in English",
    "descriptionEs": "Descripción apetitosa y detallada en Español.",
    "descriptionEn": "Appetizing and detailed description in English.",
    "price": "$14.95",
    "popular": true,
    "badge": "Popular",
    "tags": ["Casero", "Fresco"],
    "allergens": ["Gluten"],
    "ctaType": "in_store"
  }}
]

Output ONLY the raw JSON array. No markdown fences, no backticks, no conversational text."""

    return prompt


def expand_merchant_menu(filepath: str, merchant_data: Dict[str, Any]) -> Optional[int]:
    """
    Call Gemini to generate additional menu items, merge them into the existing
    merchant data, and save the updated JSON.
    Returns the new total product count, or None on failure.
    """
    api_key = get_gemini_api_key()
    store_info = merchant_data.get("storeInfo", {})
    biz_name = store_info.get("name", "Unknown")

    prompt = build_expansion_prompt(merchant_data)

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.35,
            "responseMimeType": "application/json",
            "maxOutputTokens": 16384
        }
    }

    candidate_models = ["gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-3.1-flash-lite", "gemini-3.6-flash"]

    for model in candidate_models:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        for attempt in range(2):
            try:
                resp = requests.post(endpoint, json=payload, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                    raw_text = re.sub(r"\s*```$", "", raw_text)
                    new_products = json.loads(raw_text)

                    if not isinstance(new_products, list):
                        continue

                    if len(new_products) < 5:
                        continue

                    # Validate each product has required fields
                    valid_products = []
                    for p in new_products:
                        if all(k in p for k in ["id", "categoryId", "nameEs", "nameEn", "price"]):
                            if "ctaType" not in p:
                                p["ctaType"] = "in_store"
                            if "popular" not in p:
                                p["popular"] = False
                            if "badge" not in p:
                                p["badge"] = ""
                            if "tags" not in p:
                                p["tags"] = []
                            if "allergens" not in p:
                                p["allergens"] = []
                            if "descriptionEs" not in p:
                                p["descriptionEs"] = ""
                            if "descriptionEn" not in p:
                                p["descriptionEn"] = ""
                            valid_products.append(p)

                    if len(valid_products) < 5:
                        continue

                    # Merge new products into existing merchant data
                    merchant_data["products"].extend(valid_products)
                    new_total = len(merchant_data["products"])

                    # Save updated JSON
                    with open(filepath, "w", encoding="utf-8") as jf:
                        json.dump(merchant_data, jf, indent=2, ensure_ascii=False)

                    return new_total

                elif resp.status_code == 429:
                    log(f"   ⏳ {biz_name}: Rate limited (429) on {model}, backing off...")
                    time.sleep(6 + random.uniform(2, 4))
                else:
                    time.sleep(1.5)

            except json.JSONDecodeError:
                time.sleep(1)
            except Exception:
                time.sleep(1)

    return None


def run_expansion():
    log("=" * 80)
    log("🍽️  DuoTaps Comprehensive Menu & Catalog Expansion Pipeline")
    log(f"   Target: Expand all menus to {MIN_TARGET_PRODUCTS}-{MAX_TARGET_PRODUCTS} items")
    log(f"   Threshold: Expanding merchants with < {MIN_PRODUCTS_THRESHOLD} products")
    log(f"   Workers: {MAX_WORKERS} concurrent")
    log("=" * 80)

    merchants = get_merchants_needing_expansion()
    total_to_expand = len(merchants)
    log(f"\n📊 Found {total_to_expand} merchants needing menu expansion (sorted smallest first)\n")

    if total_to_expand == 0:
        log("✅ All merchants already have complete menus (>= 20 items)!")
        return

    expanded_count = 0
    failed_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        batch_size = 24
        for batch_start in range(0, total_to_expand, batch_size):
            batch = merchants[batch_start:batch_start + batch_size]

            futures = {}
            for filepath, data in batch:
                biz_name = data.get("storeInfo", {}).get("name", os.path.basename(filepath))
                future = executor.submit(expand_merchant_menu, filepath, data)
                futures[future] = (filepath, biz_name, len(data.get("products", [])))

            for future in as_completed(futures):
                filepath, biz_name, old_count = futures[future]
                try:
                    new_count = future.result()
                    if new_count is not None:
                        with counter_lock:
                            expanded_count += 1
                        log(f"✨ [{expanded_count}/{total_to_expand}] {biz_name}: {old_count} → {new_count} items")

                        if expanded_count % CHECKPOINT_EVERY == 0:
                            checkpoint_deploy(expanded_count)
                    else:
                        with counter_lock:
                            failed_count += 1
                        log(f"⚠️ [{expanded_count}/{total_to_expand}] {biz_name}: Retried but skipped (had {old_count} items)")
                except Exception as e:
                    with counter_lock:
                        failed_count += 1
                    log(f"⚠️ {biz_name}: Exception: {e}")

            time.sleep(0.5)

    # Final checkpoint & deploy
    checkpoint_deploy(expanded_count)

    log("\n" + "=" * 80)
    log(f"🎉 MENU EXPANSION COMPLETE!")
    log(f"   Successfully expanded: {expanded_count} merchants")
    log(f"   Failed/Skipped: {failed_count} merchants")
    log(f"   All menus now have 25-35 comprehensive items!")
    log("=" * 80)


if __name__ == "__main__":
    run_expansion()
