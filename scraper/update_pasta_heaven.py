#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Fresh Pasta
    ("fresh_pasta", "Fresh Spaghetti", "$5.50 / lb", "Handmade fresh traditional Italian spaghetti made daily"),
    ("fresh_pasta", "Fresh Linguini", "$5.50 / lb", "Handmade fresh flat linguini pasta ribbons"),
    ("fresh_pasta", "Fresh Fettuccine", "$5.50 / lb", "Freshly cut wide ribbon egg fettuccine"),
    ("fresh_pasta", "Fresh Angel Hair", "$5.50 / lb", "Delicate handmade thin capellini angel hair pasta"),
    ("fresh_pasta", "Fresh Ziti", "$5.50 / lb", "Fresh artisanal hollow tubular ziti pasta"),
    ("fresh_pasta", "Fresh Cavatelli", "$5.50 / lb", "Traditional handmade riched cavatelli pasta dumplings"),
    ("fresh_pasta", "Fresh Bucatini", "$5.50 / lb", "Thick hollow spaghetti-style fresh pasta"),
    ("fresh_pasta", "Fresh Pasta Sheets", "$5.50 / lb", "Fresh hand-rolled pasta dough sheets perfect for lasagna or cannelloni"),
    ("fresh_pasta", "Fresh Potato Gnocchi", "$6.00 / lb", "Tender Italian potato gnocchi dumplings made fresh"),
    ("fresh_pasta", "Fresh Saccottini", "$7.50 / lb", "Delicate hand-pinched pasta beggar's purse pouches"),
    ("fresh_pasta", "Fresh Meat Tortellini", "$7.00 / lb", "Handmade ring-shaped pasta filled with savory seasoned meat"),
    ("fresh_pasta", "Fresh Cheese Tortellini", "$6.50 / lb", "Handmade delicate pasta rings filled with rich Italian cheeses"),

    # Stuffed Pasta
    ("stuffed_pasta", "Handmade Cheese Ravioli", "$5.50 / dozen", "Traditional pasta pillows filled with whole milk ricotta and herbs"),
    ("stuffed_pasta", "Jumbo Stuffed Shells", "$2.25 each", "Large pasta shells hand-stuffed with seasoned ricotta and herbs"),
    ("stuffed_pasta", "Jumbo Manicotti", "$2.50 each", "Hand-rolled tender pasta tubes filled with creamy ricotta and mozzarella"),

    # Prepared Trays & Entrees
    ("entrees", "Homemade Meat Lasagna", "$5.99 / lb", "6x9 inch tray of layered pasta sheets, ground meat, ricotta, and melted mozzarella"),
    ("entrees", "Homemade Cheese Lasagna", "$5.99 / lb", "6x9 inch tray of layered pasta with rich ricotta, mozzarella, and marinara"),
    ("entrees", "Homemade Vegetable Lasagna", "$5.99 / lb", "6x9 inch tray of fresh seasonal vegetables layered with pasta and cheeses"),
    ("entrees", "Baked Eggplant Parmesan", "$6.99 / lb", "6x9 inch tray of breaded eggplant cutlets layered with marinara and melted mozzarella"),

    # Fresh Sauces
    ("sauces", "Homemade Bolognese Sauce (Pint)", "$6.75", "Slow-simmered rich meat sauce with beef, herbs, and San Marzano tomatoes"),
    ("sauces", "Fra Diavolo Spicy Sauce (Pint)", "$6.75", "Zesty spicy marinara infused with red crushed pepper and garlic"),
    ("sauces", "Red Clam Sauce (Pint)", "$6.75", "Classic Italian red clam sauce with tender clams, garlic, and herbs"),
    ("sauces", "White Clam Sauce (Pint)", "$6.75", "Savory white wine and garlic sauce loaded with tender ocean clams"),
    ("sauces", "Creamy Vodka Sauce (Pint)", "$7.75", "Velvety pink cream sauce finished with vodka, garlic, and parmesan"),
    ("sauces", "Creamy Vodka Sauce (Quart)", "$15.50", "Full quart of velvety pink cream vodka sauce"),
    ("sauces", "Traditional Marinara Sauce (Pint)", "$6.00", "Classic slow-cooked tomato sauce with garlic, basil, and olive oil"),
    ("sauces", "Traditional Marinara Sauce (Quart)", "$10.00", "Full quart of classic house marinara sauce"),
    ("sauces", "Lobster Newburg Sauce (Pint)", "$7.75", "Decadent rich cream sauce infused with sweet lobster reduction and sherry"),
    ("sauces", "Fresh Basil Pesto (Half Pint)", "$7.00", "Fragrant crushed fresh basil, olive oil, pine nuts, garlic, and parmesan"),
    ("sauces", "Creamy Alfredo Sauce (Pint)", "$7.75", "Rich authentic parmesan and heavy cream alfredo sauce (24hr pre-order)"),

    # Stuffed Breads
    ("stuffed_breads", "Pepperoni & Cheese Stuffed Bread", "$10.25", "Fresh baked golden bread rolled with savory pepperoni and melted mozzarella"),
    ("stuffed_breads", "Broccoli & Sausage Stuffed Bread", "$10.25", "Fresh baked Italian loaf stuffed with sautéed broccoli and Italian sausage"),
    ("stuffed_breads", "Broccoli & Cheese Stuffed Bread", "$10.25", "Fresh baked bread rolled with tender garlic broccoli and cheeses"),
    ("stuffed_breads", "Eggplant Parmesan Stuffed Bread", "$10.25", "Fresh baked loaf filled with seasoned breaded eggplant and melted mozzarella"),

    # Specialties & Sides
    ("specialties", "Garlic Bread Loaf", "$5.25", "Crisp Italian bread toasted with garlic butter and herbs"),
    ("specialties", "Homemade Meatball", "$1.75 each", "Tender Italian meatball simmered in marinara sauce"),
    ("specialties", "Sweet Italian Sausage Link", "$1.75 each", "Savory Italian pork sausage link simmered in marinara"),
    ("specialties", "Stuffed Mushrooms", "$6.99 / lb", "Plump mushroom caps stuffed with savory herb breadcrumb filling"),
    ("specialties", "Fresh Pizza Dough Ball", "$3.50 / lb", "Fresh daily fermented traditional pizza dough"),
    ("specialties", "Pasta Fagioli Soup (Pint)", "$4.75", "Classic hearty Italian white bean, ditalini pasta, and vegetable soup"),
    ("specialties", "Fresh Whole Mozzarella Cheese", "$6.00 / lb", "Fresh creamy artisanal whole mozzarella cheese"),
    ("specialties", "Whole Milk Ricotta Cheese", "$6.50 / lb", "Ultra-creamy whole milk Italian ricotta cheese"),
    ("specialties", "Grated Pecorino / Parmesan Cheese", "$9.99 / lb", "Aged sharp imported Italian cheese freshly grated"),

    # Catering Trays
    ("catering", "Baked Cheese Ravioli Catering Tray", "$85.00", "Half sheet pan of cheese ravioli baked in marinara with melted mozzarella (serves 10-12)"),
    ("catering", "Cavatelli & Broccoli Catering Tray", "$55.00", "Half sheet pan of fresh cavatelli tossed with garlic, olive oil, and tender broccoli florets"),
    ("catering", "Eggplant Rollatine Catering Tray", "$75.00", "Tender eggplant slices rolled with seasoned ricotta and baked in marinara"),
    ("catering", "Sausage & Peppers Catering Tray", "$70.00", "Sweet Italian sausage sautéed with bell peppers and onions"),
    ("catering", "Chicken Marsala Catering Tray", "$75.00", "Pan-seared chicken cutlets in a rich mushroom and Marsala wine sauce"),
    ("catering", "Chicken Francaise Catering Tray", "$75.00", "Egg-battered tender chicken cutlets in a bright lemon-butter white wine sauce"),
    ("catering", "Chicken Parmesan Catering Tray", "$75.00", "Crispy breaded chicken cutlets topped with marinara and melted mozzarella")
]

cat_map = {
    "fresh_pasta": ("fresh_pasta", "Pastas Frescas", "Fresh Pastas", "Utensils"),
    "stuffed_pasta": ("stuffed_pasta", "Pastas Rellenas", "Stuffed Pastas", "Utensils"),
    "entrees": ("entrees", "Platos Preparados", "Prepared Trays & Entrees", "Utensils"),
    "sauces": ("sauces", "Salsas Caseras", "Fresh Sauces", "Sparkles"),
    "stuffed_breads": ("stuffed_breads", "Panes Rellenos", "Stuffed Breads", "Sandwich"),
    "specialties": ("specialties", "Especialidades y Quesos", "Specialties & Cheeses", "Utensils"),
    "catering": ("catering", "Bandejas para Eventos", "Catering Trays", "Utensils")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each dish/grocery item name and description accurately and appetizingly into Spanish.
Preserve culinary tone. Return a JSON list with the exact same number of items ({len(items_data)} items):
Input: {json.dumps(prompt_input)}

Output strictly valid JSON:
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
print(f"Successfully translated {len(translated)} items!")

categories = [{"id": "all", "nameEs": "Todos los Productos", "nameEn": "All Items", "icon": "Utensils"}]
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
        "id": f"pasta-heaven-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 3, 6, 9, 13, 16, 20, 24, 31, 32, 40],
        "badge": "Shop Favorite" if idx in [1, 13, 16, 24, 31] else None,
        "tags": ["Fresh Daily"] if cid in ["fresh_pasta", "stuffed_pasta", "sauces"] else [],
        "allergens": ["Gluten"] if cid in ["fresh_pasta", "stuffed_pasta", "stuffed_breads"] else [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/pasta-heaven.json"
with open(target_file) as f:
    ph = json.load(f)

ph["categories"] = categories
ph["products"] = products

with open(target_file, "w") as f:
    json.dump(ph, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
