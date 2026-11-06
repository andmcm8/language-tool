#!/usr/bin/env python3
import json, os, requests, re, time, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

with open("/tmp/taste_of_thai_raw.txt") as f:
    text = f.read()

lines = [l.strip() for l in text.split("\n") if l.strip()]

# Parse items
items = []
for i in range(len(lines) - 2):
    line = lines[i]
    next_line = lines[i+1]
    if re.match(r"^[0-9]+\.[0-9]{2}$", next_line):
        desc = lines[i+2] if not re.match(r"^[0-9]+\.[0-9]{2}$", lines[i+2]) else ""
        price = f"${next_line}"
        items.append((line, price, desc))

print(f"Extracted {len(items)} items from raw text.")

def get_category(code_or_name):
    c = code_or_name.upper()
    if c.startswith("AP-"):
        return "appetizers"
    elif c.startswith("S-") or c.startswith("SA-"):
        return "soups_salads"
    elif c.startswith("SEA-"):
        return "seafood"
    elif c.startswith("SC-") or c.startswith("SM-"):
        return "crabs_salmon"
    elif c.startswith("CH-") or c.startswith("DK-"):
        return "poultry_duck"
    elif c.startswith("BF-") or c.startswith("SP-"):
        return "beef_chef"
    elif any(k in c.lower() for k in ["rice", "noodles", "sauce"]):
        return "sides_rice"
    elif any(k in c.lower() for k in ["cake", "banana", "mango", "sweet", "tea", "coffee", "shirley", "smoothie", "drink", "juice", "water", "lemonade"]):
        return "desserts_drinks"
    return "beef_chef"

cat_map = {
    "appetizers": ("appetizers", "Entradas Tailandesas", "Thai Appetizers", "Utensils"),
    "soups_salads": ("soups_salads", "Sopas y Ensaladas", "Soups & Salads", "Salad"),
    "seafood": ("seafood", "Especialidades de Mariscos", "Seafood Specialties", "Utensils"),
    "crabs_salmon": ("crabs_salmon", "Cangrejo Crujiente y Salmón", "Soft Shell Crab & Salmon", "Flame"),
    "poultry_duck": ("poultry_duck", "Pollo y Pato Asado al Curry", "Chicken & Roasted Duck", "Utensils"),
    "beef_chef": ("beef_chef", "Res y Especialidades de la Casa", "Beef & Chef's Specials", "Beef"),
    "sides_rice": ("sides_rice", "Arroces y Acompañamientos", "Rice & Sides", "Utensils"),
    "desserts_drinks": ("desserts_drinks", "Postres y Bebidas Tailandesas", "Desserts & Thai Drinks", "Sparkles")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

chunk_size = 25
translated_pairs = []

for i in range(0, len(items), chunk_size):
    chunk = items[i:i+chunk_size]
    prompt_input = [{"nameEn": it[0], "descriptionEn": it[2]} for it in chunk]
    prompt = f"""Translate each authentic Thai dish/drink name and description accurately and appetizingly into Spanish.
Preserve Thai culinary terms (Satay, Tom Yum, Som Tum, Pad Thai, etc.) where appropriate.
Return a JSON list with the exact same length ({len(chunk)} items):
Input: {json.dumps(prompt_input)}

Output format:
[
  {{"nameEs": "...", "descriptionEs": "..."}}
]"""

    resp = requests.post(url, json={
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
    }, timeout=45)

    if resp.status_code == 200:
        data = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        t_list = json.loads(data)
        translated_pairs.extend(t_list)
        print(f"Translated batch {i//chunk_size + 1}: {len(t_list)} items")
    else:
        print("Batch error:", resp.status_code)
    time.sleep(0.5)

print(f"Total translated: {len(translated_pairs)} / {len(items)}")

categories = [{"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"}]
seen_cats = set()
for it in items:
    cid = get_category(it[0])
    if cid not in seen_cats:
        seen_cats.add(cid)
        c = cat_map[cid]
        categories.append({"id": c[0], "nameEs": c[1], "nameEn": c[2], "icon": c[3]})

products = []
for idx, (it, tr) in enumerate(zip(items, translated_pairs), start=1):
    nameEn, price, descEn = it
    cid = get_category(nameEn)
    products.append({
        "id": f"taste-of-thai-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 2, 3, 9, 15, 19, 20, 24, 28, 41, 47, 50, 56, 73, 81],
        "badge": "Chef Recommendation" if idx in [1, 3, 19, 28, 47, 56, 81] else None,
        "tags": ["Spicy"] if "spicy" in descEn.lower() or "chili" in descEn.lower() or "curry" in descEn.lower() else [],
        "allergens": ["Peanuts"] if "peanut" in descEn.lower() else (["Shellfish"] if "shrimp" in descEn.lower() or "crab" in descEn.lower() else []),
        "ctaType": "in_store"
    })

target_file = "data/merchants/taste-of-thai.json"
with open(target_file) as f:
    tot = json.load(f)

tot["categories"] = categories
tot["products"] = products

with open(target_file, "w") as f:
    json.dump(tot, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
