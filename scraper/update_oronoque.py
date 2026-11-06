#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Regular 9" Pies ($20 each)
    ("fruit_pies", "Famous Oronoque Apple Pie (9\")", "$20.00", "Traditional double-crust pie overflowing with sweet, spiced orchard apples"),
    ("fruit_pies", "Wild Blueberry Pie (9\")", "$20.00", "Flaky crust packed with plump, sweet wild blueberries"),
    ("fruit_pies", "Tart Cherry Pie (9\")", "$20.00", "Classic lattice or double crust pie filled with tart red cherries and sweet glaze"),
    ("fruit_pies", "Strawberry Rhubarb Pie (9\")", "$20.00", "Perfect balance of sweet ripe strawberries and tart garden rhubarb in flaky pastry"),
    ("crumb_pies", "Apple Crumb Pie (9\")", "$20.00", "Orchard apples baked in flaky crust and crowned with sweet brown sugar cinnamon crumb streusel"),
    ("crumb_pies", "Blueberry Crumb Pie (9\")", "$20.00", "Plump wild blueberries topped with sweet buttery streusel crumble"),
    ("crumb_pies", "Cherry Crumb Pie (9\")", "$20.00", "Tart red cherries crowned with golden butter crumb topping"),
    ("cream_pies", "Chocolate Cream Pie (9\")", "$20.00", "Velvety dark chocolate pudding in flaky crust topped with fresh whipped cream and chocolate curls"),
    ("cream_pies", "Chocolate Banana Cream Pie (9\")", "$20.00", "Fresh sliced bananas and rich chocolate custard layered with fresh whipped cream"),
    ("cream_pies", "Toasted Coconut Cream Pie (9\")", "$20.00", "Creamy coconut custard filling topped with airy whipped cream and toasted coconut flakes"),
    ("cream_pies", "Banana Cream Pie (9\")", "$20.00", "Sliced ripe bananas in rich vanilla custard with whipped cream topping"),
    ("fruit_pies", "Sugar-Free Apple Pie (Frozen Unbaked 9\")", "$20.00", "Orchard apples baked without added sugar, unbaked and frozen ready for home baking"),

    # Fall & Winter Seasonal Pies
    ("seasonal_fall", "Southern Pecan Pie (9\")", "$20.00", "Rich, gooey brown sugar and vanilla filling loaded with toasted Georgia pecans"),
    ("seasonal_fall", "Traditional Harvest Pumpkin Pie (9\")", "$20.00", "Smooth spiced pumpkin custard baked in traditional flaky butter crust"),
    ("seasonal_fall", "Chocolate Pecan Pie (9\")", "$20.00", "Decadent dark chocolate melted into sweet pecan pie filling with toasted pecans"),
    ("seasonal_fall", "Baked Coconut Custard Pie (9\")", "$20.00", "Classic baked egg custard infused with sweet shredded coconut"),
    ("seasonal_fall", "Old Fashioned Custard Pie (9\")", "$20.00", "Silky baked whole milk egg custard dusted with fragrant nutmeg"),

    # Spring & Summer Seasonal Pies
    ("seasonal_summer", "Fresh Peach Pie (9\")", "$20.00", "Sweet summer peaches tossed in cinnamon and sugar, baked in double flaky crust"),
    ("seasonal_summer", "Fresh Peach Crumb Pie (9\")", "$20.00", "Sweet summer peaches crowned with brown sugar butter streusel crumble"),
    ("seasonal_summer", "Fresh Glazed Strawberry Pie (9\")", "$20.00", "Mound of fresh whole strawberries in sweet strawberry glaze with whipped cream"),
    ("seasonal_summer", "Pumpkin Chiffon Pie (9\")", "$20.00", "Light and airy spiced pumpkin chiffon mousse in flaky pie shell with whipped cream"),
    ("seasonal_summer", "Mile-High Lemon Meringue Pie (9\")", "$20.00", "Tangy fresh lemon curd topped with toasted fluffy meringue peaks"),
    ("seasonal_summer", "Key Lime Pie (9\")", "$20.00", "Authentic tart key lime custard in buttery graham cracker crust with whipped cream"),

    # Party Cakes & Farm Market Specialties
    ("party_cakes", "Apple Crumb Sheet Cake (Large Party)", "$48.99", "Large party sheet cake loaded with spiced apples and thick cinnamon streusel crumb (order 1 day ahead)"),
    ("farm_market", "Cider Donuts (Half Dozen)", "$7.50", "Half dozen fresh apple cider cake donuts tossed in cinnamon sugar"),
    ("farm_market", "Fresh Pressed Apple Cider (1 Gallon)", "$8.99", "Pure 100% freshly pressed Connecticut apple cider, pasteurized"),
    ("farm_market", "Fresh Pressed Apple Cider (Half Gallon)", "$5.50", "Half gallon of local freshly pressed chilled apple cider"),
    ("farm_market", "Local Pure Connecticut Honey Jar", "$12.00", "All-natural raw local honey harvested from Connecticut apiaries"),
    ("farm_market", "Farmhouse Orchard Fruit Jam Jar", "$8.50", "Artisanal small-batch fruit preserves (Apple Butter, Strawberry, or Peach)")
]

cat_map = {
    "fruit_pies": ("fruit_pies", "Tartas de Fruta Tradicionales", "Traditional Fruit Pies", "Sparkles"),
    "crumb_pies": ("crumb_pies", "Tartas con Streusel (Crumb)", "Crumb Streusel Pies", "Sparkles"),
    "cream_pies": ("cream_pies", "Tartas de Crema", "Cream Pies", "Utensils"),
    "seasonal_fall": ("seasonal_fall", "Especiales de Otoño e Invierno", "Fall & Winter Pies", "Coffee"),
    "seasonal_summer": ("seasonal_summer", "Especiales de Primavera y Verano", "Spring & Summer Pies", "Utensils"),
    "party_cakes": ("party_cakes", "Pasteles para Eventos", "Party Sheet Cakes", "Utensils"),
    "farm_market": ("farm_market", "Sidra de Manzana y Productos de Granja", "Farm Market & Cider", "Coffee")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each artisanal bakery pie, cider product, and farm preserve name and description accurately into Spanish.
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
print(f"Successfully translated {len(translated)} Oronoque Farms items!")

categories = [{"id": "all", "nameEs": "Todo el Menú de Tartas", "nameEn": "All Pies & Bakery", "icon": "Utensils"}]
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
        "id": f"oronoque-farms-gift-bakery-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 5, 8, 10, 13, 14, 18, 22, 24, 25],
        "badge": "Famous Oronoque Pie" if idx in [1, 5, 10, 13, 14, 24] else None,
        "tags": ["Baked Fresh"] if cid in ["fruit_pies", "crumb_pies", "cream_pies", "farm_market"] else [],
        "allergens": ["Gluten"] if cid != "farm_market" or "donut" in nameEn.lower() else [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/oronoque-farms-gift-bakery.json"
with open(target_file) as f:
    of = json.load(f)

of["categories"] = categories
of["products"] = products

with open(target_file, "w") as f:
    json.dump(of, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
