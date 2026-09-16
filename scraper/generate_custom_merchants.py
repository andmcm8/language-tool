#!/usr/bin/env python3
"""
Automated Custom Merchant Page Generator for DuoTaps
Scrapes real restaurant menus from Google Sheet leads, translates them into authentic
Spanish with Gemini 2.5 Flash, generates dedicated merchant JSON configurations,
updates the local registry, and populates the live link back into Google Sheets.
"""

import os
import re
import json
import time
import urllib.parse
from typing import Dict, Any, Optional, List

import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), "..", "service_account.json")
SPREADSHEET_TITLE = "FaceBook/Instagram Scraper"
REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "merchants", "registry.ts")
MERCHANTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "merchants")

# Load Gemini API Key from .env.local or environment
def get_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_local = os.path.join(os.path.dirname(__file__), "..", ".env.local")
    if os.path.exists(env_local):
        with open(env_local, "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip("\"' ")
    raise ValueError("GEMINI_API_KEY not found in environment or .env.local")

def slugify(text: str) -> str:
    """Converts business name to a clean URL-friendly ASCII slug."""
    import unicodedata
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")

def scrape_website_content(url: str) -> str:
    """Extracts text content and looks for menu subpages."""
    if not url or not url.startswith("http"):
        return ""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    extracted_text = []

    try:
        r = requests.get(url, headers=headers, timeout=(4, 6), verify=False)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            # Remove scripts & styles
            for elem in soup(["script", "style", "nav", "footer"]):
                elem.extract()
            text = soup.get_text(separator=" ", strip=True)
            extracted_text.append(f"HOMEPAGE CONTENT:\n{text[:3000]}")

            # Check for menu links
            menu_links = []
            for a in soup.find_all("a", href=True):
                href = a["href"].lower()
                link_text = a.get_text().lower()
                if any(k in href or k in link_text for k in ["menu", "food", "dinner", "lunch"]):
                    full_link = urllib.parse.urljoin(url, a["href"])
                    if full_link not in menu_links and full_link != url:
                        # Skip binary / non-html assets
                        if any(ext in full_link.lower() for ext in [".pdf", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".zip", ".doc"]):
                            continue
                        menu_links.append(full_link)

            # Scrape first 2 menu subpages if found
            for m_link in menu_links[:2]:
                try:
                    mr = requests.get(m_link, headers=headers, timeout=(4, 6), verify=False)
                    if mr.status_code == 200:
                        msoup = BeautifulSoup(mr.text, "html.parser")
                        for elem in msoup(["script", "style"]):
                            elem.extract()
                        mtext = msoup.get_text(separator=" ", strip=True)
                        extracted_text.append(f"MENU PAGE CONTENT ({m_link}):\n{mtext[:4000]}")
                except Exception:
                    pass
    except Exception as e:
        print(f"⚠️ Website scrape warning for {url}: {e}", flush=True)

    return "\n\n".join(extracted_text)

def generate_merchant_config_with_gemini(
    biz_name: str,
    location: str,
    website: str,
    scraped_content: str,
    slug: str
) -> Dict[str, Any]:
    """Uses Gemini 3.8 Flash to generate a production-ready MerchantConfig JSON."""
    api_key = get_gemini_api_key()
    candidate_models = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.7-flash", "gemini-3.8-flash"]

    prompt = f"""
You are an expert culinary bilingual translator and digital menu engineer for local Connecticut restaurants.
Create a complete, authentic bilingual MerchantConfig JSON for the following business:

Business Name: {biz_name}
Location: {location}
Website: {website}
Slug / ID: {slug}

SCRAPED WEBSITE / MENU DATA:
{scraped_content[:6000] if scraped_content else "No scraped content available. Research and generate accurate, typical signature items for this specific style of restaurant."}

Extract 12 to 25 representative menu items across all relevant categories (appetizers, mains, specialties, beverages, etc.).
Ensure descriptions are mouthwatering and accurately translated into Spanish. Include realistic prices, popular tags, and common allergen flags.
Note: If the scraped website content is empty or appears completely unrelated to food/dining (e.g. a national sports team or corporate portal), ignore it and generate an authentic, appetizing menu fitting a local restaurant/cafe/grill of this name in this CT town.

Strict JSON Schema Output Requirements:
{{
  "storeInfo": {{
    "id": "{slug}",
    "name": "{biz_name}",
    "tagline": "Authentic bilingual tagline (English & Spanish friendly)",
    "address": "Accurate street address or realistic CT address in {location}",
    "phone": "Phone number if found or realistic 203 area code",
    "hours": {{
      "monday_friday": "Realistic hours e.g. 11:00 AM - 9:30 PM",
      "saturday": "Realistic hours e.g. 11:30 AM - 10:00 PM",
      "sunday": "Realistic hours e.g. 12:00 PM - 9:00 PM"
    }},
    "paymentMethods": ["Cash", "Credit/Debit Cards", "Apple Pay", "Contactless"],
    "amenities": ["Dine-In", "Takeout", "Bilingual Menu", "Outdoor Seating"],
    "themeColor": "A refined brand color hex e.g. #003ec7, #b45309, #047857, #be123c",
    "logoIcon": "utensils",
    "policies": {{
      "restroomLocationEs": "Ubicado hacia la parte trasera del salón principal.",
      "restroomLocationEn": "Located towards the back of the main dining room.",
      "restroomCodeEs": "Abierto para clientes (no requiere código).",
      "restroomCodeEn": "Open for dining guests (no code required).",
      "wifiName": "{biz_name.replace(' ', '')}_Guest",
      "wifiPassword": "welcometo{slug[:6]}",
      "parkingPolicyEs": "Estacionamiento disponible en el lote contiguo o en la calle.",
      "parkingPolicyEn": "Parking available in adjacent lot or street parking.",
      "returnPolicyEs": "Nos esforzamos por la satisfacción total; por favor notifique a su mesero de inmediato.",
      "returnPolicyEn": "We strive for complete guest satisfaction; please notify your server immediately.",
      "deliveryPolicyEs": "Servicio para llevar disponible por teléfono y plataformas de entrega locales.",
      "deliveryPolicyEn": "Takeout service available by phone and local delivery platforms."
    }}
  }},
  "categories": [
    {{ "id": "all", "nameEs": "Todos los Platos", "nameEn": "All Items", "icon": "Utensils" }},
    {{ "id": "appetizers", "nameEs": "Entradas", "nameEn": "Appetizers & Starters", "icon": "Utensils" }},
    {{ "id": "mains", "nameEs": "Platos Principales", "nameEn": "Main Entrees", "icon": "Utensils" }},
    {{ "id": "specialties", "nameEs": "Especialidades de la Casa", "nameEn": "Chef Specialties", "icon": "Utensils" }},
    {{ "id": "beverages", "nameEs": "Bebidas", "nameEn": "Drinks & Beverages", "icon": "Coffee" }}
  ],
  "products": [
    {{
      "id": "{slug}-01",
      "categoryId": "appetizers",
      "nameEs": "Nombre culinario apetitoso en Español",
      "nameEn": "Item Name in English",
      "descriptionEs": "Descripción apetitosa y precisa en Español.",
      "descriptionEn": "Appetizing description in English.",
      "price": "$12.95",
      "popular": true,
      "badge": "Popular",
      "tags": ["Casero", "Fresco"],
      "allergens": ["Gluten"],
      "ctaType": "in_store"
    }}
  ],
  "faqs": [
    {{
      "qEs": "¿Tienen opciones vegetarianas o sin gluten?",
      "qEn": "Do you offer vegetarian or gluten-free options?",
      "aEs": "Sí, pregunte a nuestro personal por las opciones marcadas en el menú.",
      "aEn": "Yes, please ask our staff for items marked on the menu."
    }},
    {{
      "qEs": "¿Aceptan reservaciones?",
      "qEn": "Do you accept reservations?",
      "aEs": "Aceptamos clientes sin reservación y reservaciones por teléfono.",
      "aEn": "We welcome walk-ins and phone reservations."
    }}
  ]
}}

Output ONLY the raw JSON object. Do not include markdown code blocks, backticks, or any conversational preamble.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    last_err = None
    for model in candidate_models:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        for attempt in range(2):
            try:
                resp = requests.post(endpoint, json=payload, timeout=45)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                    raw_text = re.sub(r"\s*```$", "", raw_text)
                    parsed = json.loads(raw_text)
                    if "storeInfo" not in parsed:
                        parsed["storeInfo"] = {}
                    si = parsed["storeInfo"]
                    si["id"] = slug
                    si["name"] = biz_name
                    if not si.get("tagline"):
                        si["tagline"] = f"Authentic dining in {location} | Sabores auténticos en {location}"
                    if not si.get("address"):
                        si["address"] = f"{location}"
                    return parsed
                else:
                    last_err = f"Model {model} returned {resp.status_code}: {resp.text[:150]}"
                    time.sleep(2)
            except Exception as e:
                last_err = str(e)
                time.sleep(2)

    raise RuntimeError(f"All Gemini models failed. Last error: {last_err}")

def update_registry_file():
    """Scans data/merchants/ and rebuilds data/merchants/registry.ts."""
    json_files = [f for f in os.listdir(MERCHANTS_DIR) if f.endswith(".json")]
    
    imports = ["import { MerchantConfig } from '@/types/merchant';"]
    entries = []

    for f in sorted(json_files):
        slug = f[:-5] # remove .json
        var_name = re.sub(r"[^a-zA-Z0-9]", "_", slug)
        if var_name and (var_name[0].isdigit() or var_name[0] == "_"):
            var_name = f"m_{var_name}"
        imports.append(f"import {var_name} from './{f}';")
        entries.append(f"  '{slug}': {var_name} as unknown as MerchantConfig,")

    content = f"""{chr(10).join(imports)}

export const MERCHANTS_REGISTRY: Record<string, MerchantConfig> = {{
{chr(10).join(entries)}
}};
"""
    with open(REGISTRY_PATH, "w") as rf:
        rf.write(content)
    print(f"✅ Rebuilt registry with {len(json_files)} merchants.")

def process_uncontacted_leads(batch_size: int = 5):
    print("==================================================")
    print(" 🚀 DuoTaps Custom Merchant Page Generator")
    print(f" Target Batch Size: {batch_size} uncontacted leads")
    print("==================================================\n")

    gc = gspread.service_account(filename=CREDENTIALS_JSON)
    sh = gc.open(SPREADSHEET_TITLE)
    sheet = sh.sheet1
    rows = sheet.get_all_values()

    headers = rows[0]
    
    # Ensure 'Custom Demo Link' column exists (Column 10 / index 9)
    custom_link_col_idx = 9
    if len(headers) <= custom_link_col_idx:
        sheet.update_cell(1, custom_link_col_idx + 1, "Custom Demo Link")
        print("📝 Added 'Custom Demo Link' column header to Google Sheet.")

    processed = 0
    for row_idx, row in enumerate(rows[1:], start=2):
        if processed >= batch_size:
            break

        biz_name = row[0].strip() if len(row) > 0 else ""
        location = row[1].strip() if len(row) > 1 else "CT"
        website = row[5].strip() if len(row) > 5 else ""
        status = row[6].strip().lower() if len(row) > 6 else ""
        existing_custom_link = row[9].strip() if len(row) > 9 else ""

        # Skip if already contacted or empty name
        if not biz_name or status in ["contacted", "sent", "yes"]:
            continue

        # Exclude New Canaan leads per user preference
        if "new canaan" in location.lower():
            continue

        slug = slugify(biz_name)
        json_path = os.path.join(MERCHANTS_DIR, f"{slug}.json")
        live_url = f"https://language-tool-six.vercel.app/{slug}"

        # If already generated and sheet has link, skip
        if os.path.exists(json_path) and existing_custom_link:
            print(f"⏩ Skipping {biz_name} (already has page at {live_url})")
            continue

        print(f"\n[{processed+1}/{batch_size}] 🎯 Processing: '{biz_name}' ({location})")
        print(f"   Website: {website or 'None'}")
        print(f"   Slug: {slug}")

        # 1. Scrape real menu content
        scraped_content = ""
        if website:
            print(f"   🌐 Scraping website menu...")
            scraped_content = scrape_website_content(website)
            if scraped_content:
                print(f"   ✅ Extracted {len(scraped_content)} chars of menu content.")

        # 2. Call Gemini 2.5 Flash to generate MerchantConfig
        print(f"   🤖 Generating bilingual Spanish menu & AI assistant via Gemini...")
        try:
            config = generate_merchant_config_with_gemini(
                biz_name=biz_name,
                location=location,
                website=website,
                scraped_content=scraped_content,
                slug=slug
            )

            # 3. Save JSON file
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(config, jf, indent=2, ensure_ascii=False)
            print(f"   💾 Saved: data/merchants/{slug}.json ({len(config.get('products', []))} items)")

            # 4. Update Google Sheet with Live Custom Link
            sheet.update_cell(row_idx, custom_link_col_idx + 1, live_url)
            print(f"   📊 Google Sheet Row {row_idx} updated: {live_url}")

            processed += 1
            time.sleep(1.5) # Gentle rate limit pacing

        except Exception as e:
            print(f"   ❌ Error generating for {biz_name}: {e}")

    # 5. Rebuild registry so Next.js registers all new pages
    update_registry_file()
    print(f"\n🎉 Finished batch! Successfully generated {processed} new custom merchant pages.")

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    process_uncontacted_leads(batch_size=count)
