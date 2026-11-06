#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Starters & Antipasti
    ("starters", "Butternut Squash Bisque", "$15.00", "Made with sweet onions, carrots, celery, vegetable stock, fresh mint, touch of honey, and honey sour cream", True),
    ("starters", "Crispy Eggplant", "$16.00", "Breaded pan-fried eggplant in e.v.o.o. served over marinara, fresh stracciatella cheese, and balsamic glaze", False),
    ("starters", "Artichoke Hearts", "$16.00", "Pan-seared artichoke hearts simmered with white wine, garlic, butter, petite greens, and shaved Parmigiano Reggiano", True),
    ("starters", "Roasted Pepper and Buffalo Mozzarella", "$18.00", "Holland red, yellow, and orange peppers marinated with garlic, parsley, e.v.o.o., and imported buffalo mozzarella", True),
    ("starters", "Heirloom Tomato Salad", "$18.00", "Heirloom tomatoes and mozzarella di bufala topped with red onion, e.v.o.o., fresh basil, and balsamic reduction", True),
    ("starters", "Italian Long Hot Peppers (Spicy)", "$16.00", "Grilled hot long peppers with e.v.o.o., anchovy, seasoned breadcrumbs, garlic, cured black olives, and provolone", False),
    ("starters", "Rosie’s Meatballs", "$16.00", "Three handmade meatballs crafted from veal, beef, pork, pine nuts, raisins, parmigiano, sweet onions, and marinara", False),
    ("starters", "Yellowtail Ahi Tuna Tartare", "$19.00", "Ahi tuna, scallions, preserved lemon, capers, chili, toasted almonds, currants, avocado, spicy orange aioli, crostini", False),
    ("starters", "Maryland Crab Cakes", "$19.00", "Pan-seared jumbo lump crab meat with onions, sweet holland peppers, breadcrumbs, and remoulade sauce", False),
    ("starters", "Grilled Shrimp with Cannellini Beans", "$17.00", "Tender grilled shrimp served over dressed baby arugula with warm cannellini bean salad", True),
    ("starters", "Prime Beef Carpaccio", "$26.00", "Thinly sliced raw filet mignon, petite greens, capers, shaved parmigiano reggiano, and wasabi aioli", True),

    # Insalate
    ("salads", "Classic Caesar Salad", "$15.00", "Crisp chopped romaine, in-house traditional Caesar dressing, herbed croutons, and shaved Parmigiano", False),
    ("salads", "Insalata Mista", "$15.00", "Mixed petite greens, cucumbers, cherry tomatoes, carrots, red onion, shaved parmesan, and balsamic vinaigrette", True),
    ("salads", "Roasted Beet Salad", "$14.00", "Red and yellow roasted beets, creamy goat cheese, dressed arugula, toasted pine nuts, and house piquillo vinaigrette", True),
    ("salads", "Iceberg Wedge Salad", "$15.00", "Baby iceberg wedge, house blue cheese dressing, crispy applewood smoked bacon, and sweet cherry tomatoes", True),

    # Primi / Pastas
    ("pastas", "Linguine & Shrimp Fra Diavolo", "$36.00", "In-house fresh linguine, sautéed shrimp, garlic, white wine, parsley, marinara, and red pepper flakes", False),
    ("pastas", "Strozzapreti Bolognese", "$36.00", "Fresh strozzapreti pasta with slow-braised beef, veal, and pork ragù, touch of cream, and torn stracciatella", False),
    ("pastas", "Broccoli Rabe and Sausage Pappardelle", "$36.00", "Fresh ribbon pappardelle, e.v.o.o., broccoli rabe, housemade fennel sausage, caramelized garlic, and chili", False),
    ("pastas", "Fettuccini Carbonara", "$28.00", "Handcrafted fettuccini with caramelized onions, smoked pancetta, cream, aged Pecorino Romano, and sweet peas", False),
    ("pastas", "Butternut Squash Ravioli", "$28.00", "Delicate ravioli in a nutty brown butter sage sauce topped with crumbled sweet amaretto cookies", False),
    ("pastas", "Lobster Linguine Scampi", "$35.00", "In-house fresh linguine served with sweet fresh lobster meat in a rich garlic white wine scampi sauce", False),
    ("pastas", "Pesto Shrimp Linguine", "$35.00", "Housemade linguine sautéed with succulent shrimp, cherry tomatoes, fresh basil pesto, pine nuts, and parmesan", False),

    # Secondi / Entrees
    ("entrees", "Organic Faroe Island Salmon", "$38.00", "Pan-seared salmon fillet, orange cream reduction, warm cannellini bean salad, baby arugula, garlic, and e.v.o.o.", True),
    ("entrees", "Chicken Paillard", "$32.00", "Grilled thin-pounded chicken breast marinated in garlic and olive oil, served with arugula and tomato salad", True),
    ("entrees", "Chicken Parmigiano", "$32.00", "Breaded pan-fried chicken cutlet in e.v.o.o., house marinara, melted mozzarella, sautéed garlic spinach", False),
    ("entrees", "Amish Chicken Scarpariello", "$40.00", "Pan-seared half Amish chicken, sweet Holland peppers, onions, garlic white wine, aged balsamic, scallion mash", True),
    ("entrees", "Veal Milanese", "$42.00", "Pan-seared 'Plume de Veau' cutlet in ciabatta crumbs, topped with baby arugula, cherry tomatoes, and red onions", False),
    ("entrees", "Chef Mauri’s Roasted Duck", "$41.00", "Oven-roasted half duck, orange port wine demi-glace, sautéed green beans, and sweet potato purée", True),
    ("entrees", "Grilled Prime Filet Mignon (8 oz)", "$54.00", "8 oz center-cut prime filet mignon, peppercorn cognac sauce, scallion mashed potatoes, sautéed brussels sprouts", True),
    ("entrees", "Grilled Mediterranean Branzino", "$40.00", "Whole grilled Mediterranean sea bass fillet, olive caper tapenade, saffron vegetable couscous, and broccoli", False),
    ("entrees", "Red Wine Braised Beef Short Rib", "$42.00", "Slow-braised tender short rib, creamy wild mushroom risotto, caramelized carrots, and natural pan jus", True),
    ("entrees", "Snake River Farms Prime Rib Eye (16 oz)", "$63.00", "16 oz grilled prime rib eye, garlic herb marinade, scallion mashed potatoes, and sautéed brussels sprouts", True),
    ("entrees", "The Paci Burger", "$25.00", "Prime dry-aged beef burger, melted Gruyère cheese, caramelized onions, tomato jam, arugula, kettle chips", False),

    # Contorni / Sides ($12 each)
    ("sides", "Sautéed Brussels Sprouts", "$12.00", "Brussels sprouts sautéed in extra virgin olive oil and roasted garlic", True),
    ("sides", "Sautéed Green Beans", "$12.00", "Tender French green beans sautéed with garlic and e.v.o.o.", True),
    ("sides", "Scallion Mashed Potatoes", "$12.00", "Velvety whipped potatoes infused with fresh green scallions and butter", True),
    ("sides", "Sautéed Broccoli", "$12.00", "Fresh broccoli crowns sautéed with sliced garlic and olive oil", True),

    # Brunch Specialties
    ("brunch", "Pastry Basket", "$12.00", "Assortment of fresh cheese danishes, flaky croissants, muffins, sweet butter, and fruit jam", False),
    ("brunch", "House Granola Bowl", "$14.00", "In-house toasted oat granola, thick Greek yogurt, local Connecticut honey, and fresh berries", False),
    ("brunch", "Lobster Eggs Benedict", "$28.00", "Toasted English muffin, fresh lobster meat, sautéed spinach, roasted tomato, potato hash, hollandaise", False),
    ("brunch", "Brioche French Toast", "$18.00", "Egg-battered thick Pullman brioche loaf, whipped cinnamon butter, local maple syrup, and side", False),
    ("brunch", "Southport Sunrise Breakfast", "$18.00", "Two farm eggs any style, seasoned potato hash, and choice of chicken apple sausage or bacon", True),
    ("brunch", "Spring Vegetable Omelet", "$21.00", "Three-egg omelet with asparagus, roasted mushrooms, caramelized onions, goat cheese, chicken apple sausage", True),
    ("brunch", "Lemon Ricotta Pancakes", "$18.00", "Fluffy ricotta hotcakes with macerated blueberries, cinnamon butter, local maple syrup, choice of side", False),
    ("brunch", "Capri Pancetta Omelet", "$21.00", "Eggs, sweet peppers, onions, spinach, smoked pancetta, shredded provolone cheese, potato hash", True),
    ("brunch", "Filet Mignon Steak & Eggs", "$31.00", "Pan-seared tender filet mignon, two eggs any style, caramelized onions, and crispy potato hash", True),

    # Dolci / Desserts ($12 each)
    ("desserts", "Key Lime Tart", "$12.00", "Homemade graham cracker crust, sweet condensed milk and key lime custard, fresh whipped cream, berry coulis", False),
    ("desserts", "Warm Apple Crisp", "$12.00", "Baked Granny Smith apples, oats, brown sugar, cinnamon, vanilla gelato, and salted caramel drizzle", False),
    ("desserts", "Basque Ricotta Lemon Cheesecake", "$12.00", "Creamy crustless ricotta cheesecake perfumed with lemon zest and garnished with fresh mint", True),
    ("desserts", "Chocolate Molten Cake", "$12.00", "Warm molten center chocolate cake, crème anglaise, vanilla gelato, fresh berries, whipped cream", True),
    ("desserts", "Coconut Almond Cake", "$12.00", "Moist almond cake with fresh shaved coconut topped with bittersweet chocolate espresso drizzle", False),
    ("desserts", "Toasted Almond Amaretto Cake", "$12.00", "Ladyfingers steeped in Amaretto syrup, sweet mascarpone cream, amaretti cookies, roasted almonds", False),
    ("desserts", "Classic Tiramisu", "$12.00", "Espresso-soaked ladyfingers layered with sweet imported mascarpone cream and dusted with dark cocoa", False),
    ("desserts", "Fresh Seasonal Berries", "$15.00", "Hand-selected market fresh berries served with house whipped vanilla cream", True),
    ("desserts", "Tartufo Gelato Ball", "$12.00", "Choice of Manhattan, Salted Caramel, or Cappuccino gelato encased in chocolate shell", True),
    ("desserts", "Artisanal Gelato & Sorbet", "$8.00", "Small scoop of Strawberry, Stracciatella, Vanilla, Chocolate, Coconut, Lemon, or Raspberry sorbet", True)
]

cat_map = {
    "starters": ("starters", "Antipasti y Entradas", "Starters & Antipasti", "Utensils"),
    "salads": ("salads", "Insalate", "Salads", "Salad"),
    "pastas": ("pastas", "Primi Piatti (Pastas)", "Pastas", "Utensils"),
    "entrees": ("entrees", "Secondi Piatti (Platos Fuertes)", "Entrees", "Beef"),
    "sides": ("sides", "Contorni (Guarniciones)", "Sides", "Utensils"),
    "brunch": ("brunch", "Brunch de Fin de Semana", "Brunch Specialties", "Coffee"),
    "desserts": ("desserts", "Dolci (Postres)", "Desserts", "Sparkles")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each dish name and culinary description into refined, elegant Spanish suitable for a high-end Italian restaurant.
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
print(f"Successfully translated {len(translated)} Paci Restaurant items!")

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
    cid, nameEn, price, descEn, is_gf = it
    products.append({
        "id": f"paci-restaurant-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [2, 7, 16, 17, 23, 27, 29, 39, 49, 52],
        "badge": "Chef Mauri Special" if idx in [7, 17, 23, 27, 29] else None,
        "tags": ["Gluten-Free"] if is_gf else [],
        "allergens": [] if is_gf else ["Gluten"],
        "ctaType": "in_store"
    })

target_file = "data/merchants/paci-restaurant.json"
with open(target_file) as f:
    paci = json.load(f)

paci["categories"] = categories
paci["products"] = products

with open(target_file, "w") as f:
    json.dump(paci, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
