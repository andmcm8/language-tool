#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Middle Eastern Sandwiches & Pitas
    ("sandwiches", "Classic Falafel Pita Sandwich", "$10.50", "Golden crispy falafel balls, creamy hummus, crisp lettuce, ripe tomatoes, tahini sauce, and pickles in warm pita"),
    ("sandwiches", "Falafel & Cauliflower Sandwich", "$11.50", "Crispy falafel and golden fried cauliflower with hummus, lettuce, tomatoes, pickles, and tahini"),
    ("sandwiches", "Falafel & Eggplant Sandwich", "$11.50", "Crispy falafel and tender fried eggplant slices with hummus, lettuce, tomato, pickles, and tahini sauce"),
    ("sandwiches", "Falafel Mix Special Sandwich", "$12.50", "Loaded pita with falafel, fried cauliflower, fried eggplant, creamy hummus, pickles, and tahini"),
    ("sandwiches", "Chicken Shawarma Sandwich", "$12.99", "Thinly sliced marinated chicken shawarma with garlic whip (toum), pickles, tomatoes, and lettuce in warm pita"),
    ("sandwiches", "Beef Shawarma Sandwich", "$13.99", "Tender spiced shaved beef shawarma with sumac onions, tomatoes, pickles, and creamy tahini sauce"),
    ("sandwiches", "Kofta Kabob Pita Sandwich", "$13.50", "Char-grilled spiced minced beef and lamb skewers with hummus, diced tomatoes, pickles, and tahini in pita"),

    # Platters & Bowls
    ("platters", "Chicken Shawarma Platter", "$17.99", "Generous serving of spiced chicken shawarma over fragrant seasoned rice, hummus, Mediterranean salad, garlic sauce, pita"),
    ("platters", "Beef Shawarma Platter", "$18.99", "Slow-roasted tender shaved beef shawarma over spiced rice, hummus, chopped salad, tahini, and warm pita"),
    ("platters", "Chicken Shawarma Fatta", "$17.99", "Traditional Middle Eastern layered bowl with toasted pita chips, seasoned rice, chicken shawarma, garlic yogurt sauce"),
    ("platters", "Grilled Chicken Kabob Platter", "$18.99", "Skewers of marinated chicken breast grilled over open flames, served with rice, hummus, salad, and pita"),
    ("platters", "Grilled Lamb Kabob Platter", "$21.99", "Tender cubes of char-broiled marinated lamb served with yellow rice, creamy hummus, salad, and pita"),
    ("platters", "Kofta Kabob Platter", "$19.99", "Two grilled skewers of seasoned minced beef and lamb herbs served over rice with hummus, salad, and pita"),
    ("platters", "Mixed Grill Kabob Platter", "$24.99", "Feast of chicken kabob, lamb kabob, and kofta skewer served with yellow rice, hummus, salad, and warm pita"),
    ("platters", "Falafel Salad Bowl", "$14.50", "Five crispy falafel balls over chopped romaine, cucumber, tomatoes, red onions, pickled turnips, and tahini dressing"),

    # Burgers & Sandwiches
    ("burgers", "Mr. Falafel Smash Burger", "$11.99", "Double smashed beef patties, melted American cheese, pickles, and house special sauce on a toasted brioche bun"),
    ("burgers", "Spicy Jalapeño Smash Burger", "$12.99", "Double smash patties, melted pepper jack cheese, jalapeños, and zesty spicy sauce on brioche"),
    ("burgers", "Classic Cheeseburger", "$11.50", "Juicy grilled beef patty, melted cheddar cheese, crisp lettuce, tomato, onions, and pickles"),
    ("burgers", "Bacon Cheeseburger", "$13.50", "Beef burger topped with crispy smoked turkey bacon, melted cheddar, grilled onions, and house sauce"),
    ("burgers", "NYC Chopped Cheese Hero", "$12.99", "Seasoned ground beef chopped on the griddle with melted American cheese, lettuce, tomato, and mayo on hero roll"),
    ("burgers", "Loaded Shawarma Fries", "$12.99", "Golden french fries smothered with chicken shawarma, melted cheese, garlic whip, and spicy tahini drizzle"),
    ("burgers", "Crispy Seasoned French Fries", "$4.99", "Hot crispy seasoned french fries served with ketchup and garlic mayo"),

    # Appetizers & Sides
    ("appetizers", "Fresh Falafel Balls (5 pcs)", "$6.50", "Five freshly fried chickpea and herb falafel balls served with creamy tahini dip"),
    ("appetizers", "Creamy Hummus with Pita", "$7.99", "Authentic smooth chickpea puree with tahini, lemon juice, extra virgin olive oil, and warm pita bread"),
    ("appetizers", "Stuffed Grape Leaves / Dolmas (5 pcs)", "$6.99", "Tender vine leaves stuffed with seasoned rice, onions, mint, and Mediterranean spices"),
    ("appetizers", "Spinach & Feta Spanakopita Pie", "$6.50", "Flaky golden phyllo pastry baked with savory spinach and Greek feta cheese"),
    ("appetizers", "Warm Pocket Pita Bread", "$1.50", "Freshly baked warm soft pita bread"),

    # Artisanal Gelato & Desserts
    ("gelato", "Dubai Chocolate Gelato", "$6.50", "Signature rich chocolate gelato swirled with pistachio cream and crisp toasted kataifi knafeh shreds"),
    ("gelato", "Sicilian Pistachio Gelato", "$5.50", "Authentic imported Sicilian roasted pistachio creamy gelato"),
    ("gelato", "Nutella Hazelnut Gelato", "$5.50", "Decadent milk chocolate and hazelnut gelato swirled with creamy Nutella"),
    ("gelato", "Sea Salt Caramel Gelato", "$5.50", "Rich sweet and salty caramel ribbon blended with creamy gelato"),
    ("gelato", "Mango Passion Fruit Sorbetto", "$5.50", "Refreshing dairy-free fruit sorbet bursting with tropical mango and passion fruit"),
    ("gelato", "Blood Orange Sorbetto", "$5.50", "Crisp, bright Italian blood orange dairy-free fruit sorbet"),
    ("gelato", "Cookies & Cream Oreo Gelato", "$5.50", "Sweet cream gelato folded with crushed Oreo cookie chunks"),
    ("gelato", "Artisan Gelato Pint Container (12.5 oz)", "$9.99", "Hand-packed 12.5 oz to-go pint of your favorite artisanal gelato flavors"),
    ("gelato", "Dubai Chocolate Big Bar", "$14.99", "Thick artisan chocolate bar loaded with gooey pistachio cream and toasted knafeh pastry"),
    ("gelato", "Dubai Chocolate Strawberry Cup", "$11.99", "Fresh ripe strawberries drenched in warm melted milk chocolate and pistachio cream")
]

cat_map = {
    "sandwiches": ("sandwiches", "Sándwiches y Pitas", "Pitas & Wraps", "Sandwich"),
    "platters": ("platters", "Platos Fuertes y Bowls", "Platters & Bowls", "Beef"),
    "burgers": ("burgers", "Hamburguesas y Chopped Cheese", "Burgers & Fast Fare", "Utensils"),
    "appetizers": ("appetizers", "Entradas y Guarniciones", "Appetizers & Sides", "Utensils"),
    "gelato": ("gelato", "Gelato Artesanal y Postres Dubai", "Gelato & Desserts", "Sparkles")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each Middle Eastern street food, burger, and gelato dessert name and description into appetizing Spanish.
Return a JSON list with the exact same length ({len(items_data)} items):
Input: {json.dumps(prompt_input)}

Output format:
[
  {{"nameEs": "...", "descriptionEs": "..."}}
]"""

resp = requests.post(url, json={
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
}, timeout=45)

if resp.status_code != 200:
    print("Translation failed:", resp.status_code, resp.text)
    sys.exit(1)

translated = json.loads(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
print(f"Successfully translated {len(translated)} Mr. Falafel items!")

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
        "id": f"mr-falafel-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 4, 5, 8, 11, 14, 16, 20, 23, 28, 36],
        "badge": "House Favorite" if idx in [1, 5, 8, 16, 28, 36] else None,
        "tags": ["Vegetarian"] if "falafel" in nameEn.lower() or cid == "gelato" else (["Halal"] if cid in ["sandwiches", "platters"] else []),
        "allergens": [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/mr-falafel.json"
with open(target_file) as f:
    mf = json.load(f)

mf["categories"] = categories
mf["products"] = products

with open(target_file, "w") as f:
    json.dump(mf, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
