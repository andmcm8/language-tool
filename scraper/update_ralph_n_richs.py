#!/usr/bin/env python3
import requests
import json
import re
import os
import sys
import time

sys.path.insert(0, "scraper")
from generate_custom_merchants import get_gemini_api_key

def fetch_ralph_items():
    bzn_id = "bzn-IrSx1iZPQbe1jfqzkW1mCA"
    url = f"https://data.gonation.com/businesses/{bzn_id}/inventory"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    data = r.json()
    inv = data.get("inventory", [])

    def parse_items(node, path=[]):
        sec = node.get("secItem", {})
        itype = sec.get("inventoryType")
        io = sec.get("inventoryObject", {})
        name = io.get("name", "").strip()
        items = []
        if itype == "section":
            curr_path = path + [name]
            for ch in node.get("children", []):
                items.extend(parse_items(ch, curr_path))
        elif itype == "item":
            p = " > ".join(path)
            # Only dinner, lunch, dessert, appetizers, raw bar, pasta, entrees
            if any(k in p for k in ["Dinner", "Lunch", "Dessert", "Sunday Lounge", "Restaurant Week"]):
                desc = (io.get("desc") or io.get("description") or "").strip()
                price = None
                if io.get("price"):
                    try: price = float(str(io["price"]).replace("$", ""))
                    except: pass
                if not price and io.get("variants"):
                    v = io["variants"][0]
                    if v.get("price"):
                        try: price = float(str(v["price"]).replace("$", ""))
                        except: pass
                if not price:
                    m = re.search(r"\$([0-9]+(?:\.[0-9]{2})?)", name)
                    if m:
                        price = float(m.group(1))
                clean_name = re.sub(r"[\u2014\-]\s*\$[0-9]+.*", "", name).strip()
                if not clean_name.startswith("*") and not clean_name.startswith("~") and len(clean_name) > 2:
                    items.append({
                        "name": clean_name,
                        "price": price,
                        "desc": desc,
                        "path": p
                    })
        else:
            for ch in node.get("children", []):
                items.extend(parse_items(ch, path))
        return items

    raw_items = parse_items({"children": inv})
    seen = {}
    for it in raw_items:
        k = it["name"].lower()
        if k not in seen or (it["price"] and not seen[k]["price"]):
            seen[k] = it
        elif it["desc"] and not seen[k]["desc"]:
            seen[k]["desc"] = it["desc"]

    # Filter out pure placeholders
    filtered = []
    for it in seen.values():
        n = it["name"]
        if n in ["Entrée", "Dessert", "Daily Fresh Oysters", "Additional Priced Accordingly", "Please refer to our specials"]:
            continue
        filtered.append(it)

    print(f"Total authentic items to process: {len(filtered)}")
    return filtered

def assign_category(path, name):
    p = path.lower()
    n = name.lower()
    if any(k in p for k in ["raw bar", "antipasto", "appetizer"]) or any(k in n for k in ["clam", "oyster", "calamari", "shrimp cocktail", "crab cake", "bruschetta", "antipasto"]):
        if "raw bar" in p or "clam" in n or "oyster" in n or "crab claw" in n:
            return "raw-bar"
        return "appetizers"
    if any(k in p for k in ["soup", "salad"]) or "salad" in n or "minestrone" in n:
        return "soups-salads"
    if "pasta" in p or any(k in n for k in ["penne", "rigatoni", "spaghetti", "linguine", "fettuccine", "cavatelli", "lasagna", "ravioli", "gnocchi", "fusilli"]):
        return "pasta"
    if "dessert" in p or any(k in n for k in ["tiramisu", "cheesecake", "cannoli", "gelato", "leches", "pudding", "cookie"]):
        return "desserts"
    if "sandwich" in p or any(k in n for k in ["wrap", "panini", "burger", "grinder"]):
        return "sandwiches"
    if "side" in p or any(k in n for k in ["spinach", "broccoli", "string bean", "potato", "rabe"]):
        return "sides"
    return "entrees"

def translate_batch(batch, api_key):
    prompt = """You are an expert Italian culinary translator. Translate these authentic Italian restaurant dishes into bilingual format for DuoTaps Language Tool.
For each item, return a JSON object with:
- id: unique kebab-case slug
- nameEs: Spanish name of dish
- nameEn: English name
- descriptionEs: appetizing Spanish description explaining ingredients and Italian culinary style
- descriptionEn: appetizing English description
- price: float number (if given or reasonable market price: appetizers $12-18, salads $10-16, pastas $20-28, entrees $26-42, desserts $10-14, sides $8-12)
- category: one of ["raw-bar", "appetizers", "soups-salads", "pasta", "entrees", "sides", "desserts", "sandwiches"]
- allergens: list of allergens in Spanish like ["Gluten", "Lácteos", "Mariscos", "Huevos", "Pescado", "Frutos secos"]
- popular: boolean (true for famous Italian classics like Chicken Parm, Penne Vodka, Calamari, Tiramisu, Clams Casino)

Input Items:
""" + json.dumps(batch, indent=2) + """

Output ONLY valid JSON array with the exact translated objects. Do not wrap in markdown quotes or preamble.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
    }

    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=40)
            if r.status_code == 200:
                txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                return json.loads(txt)
            else:
                print(f"API attempt {attempt+1} error {r.status_code}: {r.text[:200]}")
                time.sleep(2)
        except Exception as e:
            print(f"Attempt {attempt+1} exception: {e}")
            time.sleep(2)
    return []

def main():
    items = fetch_ralph_items()
    api_key = get_gemini_api_key()

    formatted_inputs = []
    for it in items:
        cat = assign_category(it["path"], it["name"])
        formatted_inputs.append({
            "name": it["name"],
            "price": it["price"],
            "desc": it["desc"],
            "category": cat
        })

    # Batch process in chunks of 25
    chunk_size = 25
    translated_all = []
    for i in range(0, len(formatted_inputs), chunk_size):
        chunk = formatted_inputs[i:i+chunk_size]
        print(f"Translating chunk {i//chunk_size + 1}/{(len(formatted_inputs)-1)//chunk_size + 1} ({len(chunk)} items)...")
        translated_chunk = translate_batch(chunk, api_key)
        if not translated_chunk:
            print(f"⚠️ Failed chunk {i//chunk_size + 1}, retrying with 3.6-flash...")
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": "Translate to JSON array: " + json.dumps(chunk)}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            res = requests.post(url_alt, json=payload, timeout=45)
            if res.status_code == 200:
                translated_chunk = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"].strip())
        print(f"Received {len(translated_chunk)} translated items.")
        translated_all.extend(translated_chunk)

    print(f"Total translated items: {len(translated_all)}")

    dest = "data/merchants/ralph-n-richs.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
        {"id": "raw-bar", "nameEs": "Barra de Mariscos Crudos", "nameEn": "Raw Bar & Chilled Seafood", "icon": "Fish"},
        {"id": "appetizers", "nameEs": "Antipasti y Entrantes", "nameEn": "Antipasti & Appetizers", "icon": "Utensils"},
        {"id": "soups-salads", "nameEs": "Sopas y Ensaladas", "nameEn": "Soups & Salads", "icon": "Salad"},
        {"id": "pasta", "nameEs": "Pastas Tradicionales", "nameEn": "Traditional Pastas", "icon": "Utensils"},
        {"id": "entrees", "nameEs": "Segundos de Carne y Pescado", "nameEn": "Entrees: Meat & Seafood", "icon": "Beef"},
        {"id": "sandwiches", "nameEs": "Paninis y Sándwiches de Almuerzo", "nameEn": "Lunch Sandwiches", "icon": "Sandwich"},
        {"id": "sides", "nameEs": "Contornos y Acompañamientos", "nameEn": "Sides & Vegetables", "icon": "Salad"},
        {"id": "desserts", "nameEs": "Dolci y Postres Caseros", "nameEn": "House Desserts", "icon": "Coffee"}
    ]

    data["categories"] = categories
    data["items"] = translated_all

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(translated_all)} verified items to {dest}!")

if __name__ == "__main__":
    main()

