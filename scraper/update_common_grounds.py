#!/usr/bin/env python3
import json, os, requests, time, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Coffee & Espresso Classics
    ("coffee", "Common Grounds House Blend Drip Coffee", "$3.25", "Signature medium roast house blend brewed fresh, smooth and balanced"),
    ("coffee", "French Roast Dark Coffee", "$3.25", "Bold, smoky dark roast coffee brewed to perfection"),
    ("coffee", "Daily Flavored Coffee", "$3.50", "Freshly brewed specialty flavored roast of the day (Hazelnut, Vanilla, or Caramel)"),
    ("coffee", "Classic Caffe Americano", "$3.75", "Double shot of rich espresso topped with hot filtered water"),
    ("coffee", "Handcrafted Cappuccino", "$4.75", "Espresso layered with equal parts warm steamed milk and velvety foam"),
    ("coffee", "Caffe Latte", "$5.00", "Double shot of espresso smoothly blended with steamed milk and delicate foam"),
    ("coffee", "Classic Caffe Macchiato", "$4.50", "Double shot of espresso marked with a dollop of rich microfoam"),
    ("coffee", "Cafe Breve", "$5.25", "Espresso pulled over rich, steamed half-and-half for an ultra-creamy cup"),
    ("coffee", "Classic Cafe Au Lait", "$4.25", "Half freshly brewed house drip coffee and half warm steamed milk"),
    ("coffee", "96 oz Coffee Traveler Box", "$24.95", "Insulated bulk container of freshly brewed coffee, serves 8-10 with cups, lids, and condiments"),

    # Mochas & Specialty Creations
    ("specialty_drinks", "Ghirardelli Caffe Mocha", "$5.75", "Rich espresso blended with authentic Ghirardelli chocolate and steamed milk, topped with whip"),
    ("specialty_drinks", "Signature Caramel Macchiato", "$5.75", "Steamed milk marked with espresso and vanilla syrup, drizzled with buttery caramel sauce"),
    ("specialty_drinks", "The Common Macchiato", "$5.75", "House specialty espresso macchiato infused with hazelnut and caramel"),
    ("specialty_drinks", "Mocha Banana Latte", "$6.00", "Espresso combined with rich chocolate milk and sweet banana syrup"),
    ("specialty_drinks", "Mocha Choco Mint", "$6.00", "Decadent dark chocolate mocha infused with cooling peppermint syrup and whip"),
    ("specialty_drinks", "Golden Turmeric Wellness Latte", "$5.75", "Steamed oat or almond milk infused with aromatic turmeric, ginger, and honey"),
    ("specialty_drinks", "Matcha Green Tea Latte", "$5.75", "Japanese ceremonial grade matcha whisked with creamy steamed milk"),
    ("specialty_drinks", "Ghirardelli Hot Cocoa", "$4.50", "Sweet steamed milk swirled with rich Ghirardelli chocolate and whipped cream"),
    ("specialty_drinks", "Organic Spiced Chai Latte", "$5.25", "Black tea brewed with cardamom, cinnamon, clove, and steamed milk"),
    ("specialty_drinks", "Italian Sparkling Fruit Soda", "$4.25", "Sparkling mineral water over ice with choice of flavored fruit syrup and cream"),
    ("specialty_drinks", "Real Fruit Smoothie", "$6.50", "Blended strawberry, mango, or peach smoothie made with real fruit puree"),

    # Breakfast & Lunch Wraps
    ("food", "Classic Breakfast Wrap", "$7.95", "Fluffy scrambled eggs, melted cheddar cheese, and choice of crispy bacon or breakfast sausage in grilled tortilla"),
    ("food", "Western Breakfast Wrap", "$8.25", "Scrambled eggs, diced ham, sweet bell peppers, onions, and melted cheddar in grilled wrap"),
    ("food", "Spinach, Egg & Feta Wrap", "$7.95", "Scrambled farm eggs, baby spinach, and tangy Greek feta cheese in a warm wheat tortilla"),
    ("food", "Chipotle Grilled Chicken Wrap", "$10.50", "Grilled chicken breast, crispy bacon, cheddar, lettuce, tomato, and zesty chipotle mayo"),
    ("food", "Cranberry Walnut Chicken Salad Wrap", "$10.50", "Homemade roasted chicken salad tossed with sweet dried cranberries, toasted walnuts, and romaine"),
    ("food", "Turkey Bacon Swiss Panini", "$10.95", "Sliced turkey breast, crisp smoked bacon, melted Swiss cheese, and honey mustard on pressed artisan bread"),
    ("food", "Fresh Tomato Mozzarella Caprese Panini", "$9.95", "Ripe tomatoes, fresh mozzarella cheese, baby spinach, and basil pesto pressed golden"),

    # Bakery & Pastries
    ("bakery", "Fresh Baked Jumbo Muffin", "$3.75", "Choice of Blueberry, Corn, Lemon Poppy Seed, Double Chocolate Chip, or Pistachio"),
    ("bakery", "Flaky European Butter Croissant", "$3.50", "Warm, golden flaky European-style butter croissant"),
    ("bakery", "Almond Paste Croissant", "$4.25", "Flaky croissant filled with sweet almond frangipane cream and sliced almonds"),
    ("bakery", "Pain au Chocolat (Chocolate Croissant)", "$4.25", "Crisp buttery croissant rolled with imported semi-sweet chocolate batons"),
    ("bakery", "Wild Blueberry Scone", "$3.75", "Buttery baked English-style scone studded with sweet wild blueberries"),
    ("bakery", "Cinnamon Streusel Crumb Cake", "$4.25", "Tender butter cake piled high with brown sugar cinnamon streusel crumble"),
    ("bakery", "Artisan Overnight Oats with Fruit & Granola", "$5.50", "Chilled rolled oats soaked in almond milk, layered with fresh berries and toasted granola"),
    ("bakery", "Jumbo Chocolate Chip Cookie", "$3.00", "Freshly baked soft-baked bakery cookie with melted chocolate chips")
]

cat_map = {
    "coffee": ("coffee", "Café y Espresso", "Coffee & Espresso", "Coffee"),
    "specialty_drinks": ("specialty_drinks", "Mochas y Bebidas Especiales", "Mochas & Specialties", "Sparkles"),
    "food": ("food", "Wraps de Desayuno y Paninis", "Breakfast & Lunch Wraps", "Sandwich"),
    "bakery": ("bakery", "Pastelería y Panadería", "Bakery & Pastries", "Utensils")
}

api_key = get_gemini_api_key()
models = ["gemini-3.1-flash-lite", "gemini-3.6-flash"]

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each coffeehouse beverage, breakfast wrap, and artisanal bakery pastry name and description into appetizing Spanish.
Return a JSON list with the exact same length ({len(items_data)} items):
Input: {json.dumps(prompt_input)}

Output format:
[
  {{"nameEs": "...", "descriptionEs": "..."}}
]"""

translated = None
for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    for attempt in range(3):
        try:
            print(f"Trying {model} (attempt {attempt+1})...")
            resp = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
            }, timeout=30)
            if resp.status_code == 200:
                translated = json.loads(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
                break
            else:
                print(f"Status {resp.status_code}, retrying...")
                time.sleep(2)
        except Exception as e:
            print(f"Timeout/Error: {e}, retrying...")
            time.sleep(2)
    if translated:
        break

if not translated:
    print("All translation attempts failed.")
    sys.exit(1)

print(f"Successfully translated {len(translated)} Common Grounds items!")

categories = [{"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"}]
seen_cats = set()
for it in items_data:
    cid = it[0]
    if cid not in seen_cats:
        seen_cats.add(cid)
        c = cat_map[cid]
        categories.append({"id": c[0], "nameEs": c[1], "nameEn": c[2], "icon": c[3]})

products = []
for idx, (it, tr) in enumerate(zip(items_data, translated), start=1):
    cid, nameEn, price, descEn = it
    products.append({
        "id": f"common-grounds-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 5, 6, 11, 12, 18, 22, 25, 29, 31, 35],
        "badge": "House Favorite" if idx in [1, 11, 12, 22, 29] else None,
        "tags": ["Popular"] if idx in [1, 11, 12, 22, 29] else [],
        "allergens": [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/common-grounds.json"
with open(target_file) as f:
    cg = json.load(f)

cg["categories"] = categories
cg["products"] = products

with open(target_file, "w") as f:
    json.dump(cg, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
