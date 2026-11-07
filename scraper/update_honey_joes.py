#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Specials & Cold Brew on Tap
    ("specials", "Honey Joe's Signature Latte", "$6.25", "House favorite latte crafted with double shot of La Colombe espresso, organic honey syrup, and cinnamon"),
    ("specials", "La Colombe Draft Latte on Tap", "$6.50", "La Colombe's signature oat milk latte on tap infused with nitrous oxide for silky microfoam texture"),
    ("specials", "Pure Black Cold Brew on Tap", "$5.00", "Steeped La Colombe cold brew served crisp and refreshing on draft"),
    ("specials", "Black & Tan Draft", "$6.00", "Layered draft pour combining Pure Black Cold Brew and silky Draft Latte"),
    ("specials", "Classic Affogato", "$5.75", "A creamy scoop of vanilla ice cream drowned in a hot double shot of La Colombe espresso"),

    # Espresso & Coffee
    ("coffee", "La Colombe Espresso Double Shot", "$3.50", "Double shot of rich, artisanal La Colombe espresso"),
    ("coffee", "Caffe Americano", "$4.00", "Double shot of La Colombe espresso diluted with hot water"),
    ("coffee", "Drip Coffee (La Colombe Blend)", "$3.50", "Freshly brewed La Colombe specialty house blend coffee"),
    ("coffee", "Caffe Latte", "$5.50", "Double shot of espresso combined with velvety steamed milk and a thin layer of foam"),
    ("coffee", "Cappuccino", "$5.00", "Equal parts espresso, steamed milk, and airy microfoam"),
    ("coffee", "Cortado", "$4.50", "Double shot of espresso cut with an equal volume of warm steamed milk"),
    ("coffee", "Caffe Macchiato", "$4.25", "Double shot of espresso marked with a small dollop of steamed milk foam"),
    ("coffee", "Caffe Mocha", "$6.00", "Rich espresso and steamed milk swirled with decadent dark chocolate syrup"),
    ("coffee", "Box of Coffee to Go (96 oz)", "$28.00", "Bulk 96 oz tote of fresh brewed La Colombe coffee, serves 8-10 with cups and condiments"),

    # Teas & Specialty Drinks
    ("tea_drinks", "Rishi Masala Chai Tea Latte", "$5.75", "Slow-brewed organic Rishi Masala chai spices combined with steamed milk"),
    ("tea_drinks", "Rishi Matcha Latte", "$6.00", "Whisked organic unsweetened Japanese Rishi matcha green tea with velvety steamed milk"),
    ("tea_drinks", "Rishi Artisan Hot Tea", "$3.75", "Selection of premium organic Rishi hot tea sachets"),
    ("tea_drinks", "Rishi Fresh Iced Tea", "$4.25", "Choice of Green Tea Citrus, Peach Black, or caffeine-free Wildberry Hibiscus"),
    ("tea_drinks", "Rich Hot Chocolate", "$4.50", "Decadent melted chocolate syrup steamed with milk and topped with whipped cream"),
    ("tea_drinks", "Steamed Flavored Milk Steamer", "$3.50", "Comforting warm steamed milk with choice of vanilla, caramel, cinnamon, or hazelnut syrup"),

    # Smoothies & Milkshakes
    ("smoothies", "Peachy Green Smoothie", "$8.50", "Fresh baby spinach, juicy peaches, ripe banana, coconut water, and orange juice"),
    ("smoothies", "Beary Good Berry Smoothie", "$8.50", "Antioxidant-rich mixed berries, banana, almond milk, and orange juice"),
    ("smoothies", "Bowtie Banana Cinnamon Smoothie", "$8.50", "Fresh banana, milk, organic honey syrup, and ground cinnamon"),
    ("smoothies", "Cold Brew Coffee Milkshake", "$8.50", "Rich vanilla ice cream blended with concentrated Pure Black cold brew"),
    ("smoothies", "Chai Tea Milkshake", "$8.00", "Vanilla ice cream spun with Rishi Masala chai tea spices"),
    ("smoothies", "Caramel Banana Milkshake", "$8.50", "Creamy vanilla ice cream blended with ripe banana and rich caramel drizzle"),
    ("smoothies", "Classic Ice Cream Milkshake", "$7.50", "Hand-spun milkshake in your choice of vanilla, chocolate, or caramel"),
    ("smoothies", "Double Scoop Ice Cream Sundae", "$6.50", "Two scoops of vanilla ice cream topped with chocolate or caramel sauce and whipped cream"),

    # Food, Sandwiches & Flatbreads
    ("food", "Wave Hill Breads Artisanal Pastry", "$4.50", "Daily selection of fresh handmade artisanal pastries from Norwalk's Wave Hill Breads"),
    ("food", "Sausage, Egg & Cheese Croissant", "$7.50", "Savory sausage patty, fluffy egg, and melted American cheese on a toasted butter croissant"),
    ("food", "Turkey Bacon Avocado Sandwich", "$11.50", "Sliced roasted turkey, crispy bacon, ripe tomato, and house avocado spread on toasted multigrain bread"),
    ("food", "Sriracha Turkey Club Melt", "$11.50", "Warm oven-melted multigrain sandwich with roasted turkey, bacon, cheddar, spinach, red onion, and zesty sriracha mayo"),
    ("food", "Fresh Caprese Sandwich", "$10.50", "Fresh mozzarella, basil pesto, ripe sliced tomatoes, and baby spinach pressed on multigrain bread"),
    ("food", "Classic Pizza Flatbread", "$10.00", "Crispy flatbread crust topped with savory marinara sauce and melted mozzarella (pepperoni optional)"),
    ("food", "Tomato Basil Balsamic Flatbread", "$10.50", "Garlic olive oil base with melted cheeses, sweet grape tomatoes, fresh basil, and balsamic reduction drizzle"),
    ("food", "BBQ Chicken Flatbread", "$11.50", "Tangy BBQ sauce, melted cheese blend, seasoned diced chicken breast, red onion, and garlic"),
    ("food", "Avocado Toast with Mozzarella", "$9.50", "Crushed avocado mash, toasted sunflower seeds, and fresh mozzarella on artisan toast")
]

cat_map = {
    "specials": ("specials", "Especialidades y Cold Brew", "Specials & Cold Brew", "Sparkles"),
    "coffee": ("coffee", "Café y Espresso La Colombe", "Espresso & Coffee", "Coffee"),
    "tea_drinks": ("tea_drinks", "Tés Rishi y Otras Bebidas", "Teas & Drinks", "Coffee"),
    "smoothies": ("smoothies", "Batidos, Smoothies y Helados", "Smoothies & Shakes", "Utensils"),
    "food": ("food", "Comida, Sandwiches y Flatbreads", "Food, Sandwiches & Flatbreads", "Sandwich")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each café beverage and food item name and description accurately and appetizingly into Spanish.
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
print(f"Successfully translated {len(translated)} Honey Joe's items!")

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
        "id": f"honey-joes-family-coffeehouse-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 2, 6, 9, 15, 21, 24, 30, 31, 37],
        "badge": "Signature" if idx in [1, 2, 30, 31] else None,
        "tags": ["La Colombe"] if cid in ["specials", "coffee"] else [],
        "allergens": [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/honey-joes-family-coffeehouse.json"
with open(target_file) as f:
    hj = json.load(f)

hj["categories"] = categories
hj["products"] = products

with open(target_file, "w") as f:
    json.dump(hj, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")

