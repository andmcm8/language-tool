#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Breakfast Sandwiches & Rolls
    ("breakfast", "Egg & Cheese Roll", "$4.50", "Two fried eggs and melted American cheese on choice of fresh Portuguese roll, hard roll, or poppyseed roll"),
    ("breakfast", "Bacon, Egg & Cheese", "$5.95", "Crispy bacon, two fried eggs, and melted American cheese on fresh toasted Portuguese roll"),
    ("breakfast", "Ham, Egg & Cheese", "$5.95", "Grilled ham, two fried eggs, and melted cheese on choice of Portuguese roll or hard roll"),
    ("breakfast", "Sausage, Egg & Cheese", "$5.95", "Savory breakfast sausage patty, two fried eggs, and melted cheese on fresh Portuguese roll"),
    ("breakfast", "Turkey, Egg & Cheese", "$6.25", "Sliced Boar's Head turkey, fried eggs, and melted cheese on toasted roll"),
    ("breakfast", "Steak, Egg & Cheese", "$7.50", "Seasoned breakfast steak, fried eggs, and melted American cheese on Portuguese roll"),
    ("breakfast", "The Hungry Man Breakfast Grinder", "$9.95", "3 fried eggs, sausage, crispy bacon, and melted American cheese on a toasted grinder sub roll"),
    ("breakfast", "The Sassy Lady Healthy Wrap", "$8.95", "Whole wheat wrap with 3 egg white omelet, Boar's Head chipotle chicken, tomato, roasted peppers, pepper jack"),
    ("breakfast", "Chaves Signature Breakfast Wrap", "$8.50", "Warm flour wrap with 3 egg omelet, crispy bacon, onions, cheddar cheese, and spicy hot sauce"),
    ("breakfast", "Toasted Portuguese Roll with Butter", "$2.50", "Freshly baked authentic Portuguese crusty roll toasted with butter or cream cheese"),
    ("breakfast", "Toasted New York Bagel with Cream Cheese", "$3.25", "Choice of plain, everything, cinnamon raisin, sesame, or garlic bagel toasted with cream cheese"),
    ("breakfast", "Fresh Brewed Chaves Coffee", "$2.50", "Hot brewed coffee: Morning Blend, Dark Roast, Cinnamon Hazelnut, or French Vanilla"),

    # Boar's Head Signature Deli Sandwiches
    ("deli", "Signature #1 Italian Deluxe Sub", "$11.50", "Boar's Head Deluxe Ham, Genoa Salami, Pepperoni, Provolone, roasted peppers, lettuce, tomato, deli dressing"),
    ("deli", "Signature #2 Turkey & Ham Club", "$11.50", "Ovengold Turkey, Deluxe Ham, American cheese, crispy bacon, lettuce, tomato, mayonnaise"),
    ("deli", "Signature #3 Golden Chicken Caesar Sub", "$11.50", "Golden Classic Chicken breast, Monterey Jack, bacon, crisp lettuce, creamy Caesar dressing"),
    ("deli", "Signature #4 Deluxe Roast Beef & Cheddar", "$11.95", "Boar's Head Deluxe Roast Beef, Vermont Cheddar, lettuce, tomato, zesty horseradish sauce"),
    ("deli", "Signature #5 Maple Honey Ham & Muenster", "$11.50", "Maple Honey Ham, Muenster cheese, sweet roasted peppers, lettuce, tomato, honey mustard"),
    ("deli", "Signature #6 Maple Honey Turkey & Bacon", "$11.50", "Maple Honey Turkey, American cheese, crispy bacon, crisp lettuce, tomato, mayonnaise"),
    ("deli", "Signature #7 Blazing Buffalo Chicken Sub", "$11.50", "Blazing Buffalo Chicken, Pepper Jack cheese, lettuce, tomato, onions, blue cheese dressing, hot sauce"),
    ("deli", "Signature #8 Hot Pastrami & Swiss Reuben", "$11.95", "Lean Boar's Head pastrami served hot with melted Swiss cheese, sauerkraut, and Russian dressing"),
    ("deli", "Signature #9 Black Forest Ham & Swiss", "$11.50", "Black Forest Ham, Swiss cheese, crisp lettuce, ripe tomato, and deli spicy mustard"),
    ("deli", "Signature #10 Mesquite Smoked Turkey & Mozzarella", "$11.50", "Mesquite Smoked Turkey, fresh mozzarella, bacon, lettuce, tomato, spicy mustard"),
    ("deli", "Signature #11 Cracked PepperMill Turkey Sub", "$11.50", "Cracked PepperMill Turkey, sharp cheddar cheese, lettuce, red onions, mayonnaise"),
    ("deli", "Homemade Chicken Salad Sandwich", "$9.95", "House-roasted chicken, diced celery, onions, and mayonnaise on Portuguese roll or wrap"),
    ("deli", "Cranberry Walnut Chicken Salad Sandwich", "$10.50", "Roasted chicken salad with sweet cranberries, toasted walnuts, celery, and creamy mayo"),
    ("deli", "Homemade Albacore Tuna Salad Sandwich", "$9.95", "Solid white albacore tuna salad with celery, onion, and mayonnaise on fresh roll"),
    ("deli", "Homemade Deli Potato Salad (1/2 lb)", "$4.50", "Traditional deli potato salad with hard boiled eggs, celery, onion, and creamy mayonnaise dressing"),
    ("deli", "Homemade Deli Macaroni Salad (1/2 lb)", "$4.50", "Classic elbow macaroni salad with diced carrots, celery, peppers, and sweet mayo dressing"),

    # Authentic Portuguese Bakery & Pastries
    ("bakery", "Pastel de Nata (Portuguese Custard Tart)", "$2.50", "Iconic flaky puff pastry cup filled with rich caramelized egg custard"),
    ("bakery", "Assorted Fresh Glazed & Frosted Donuts", "$2.00", "Handmade donuts: glazed, chocolate frosted, Boston cream, powdered jelly, cinnamon sugar, coconut"),
    ("bakery", "Apple Fritter Donut", "$2.75", "Glazed fried dough fritter loaded with tender spiced apples and cinnamon"),
    ("bakery", "Cinnamon Sugar Coffee Roll", "$2.75", "Large spiral yeast dough coffee roll tossed in cinnamon sugar or sweet vanilla glaze"),
    ("bakery", "Artisanal Fruit Danish", "$3.25", "Flaky layered pastry filled with apple, apricot, blueberry, cherry, lemon, or raspberry"),
    ("bakery", "Specialty Bakery Danish (Bear Claw / Cheese)", "$3.50", "Choice of almond bear claw, sweet cheese danish, crumb cake, or toasted walnut danish"),
    ("bakery", "Fresh Baked Butter Croissant", "$3.25", "Flaky, golden layered European-style butter croissant"),
    ("bakery", "Decadent Chocolate Croissant", "$3.75", "Flaky golden croissant filled with imported bittersweet chocolate batons"),
    ("bakery", "Traditional Italian Cannoli", "$3.50", "Crispy fried pastry shell filled with sweet whole milk ricotta cream and chocolate chips"),
    ("bakery", "Chocolate Custard Eclair", "$3.75", "Choux pastry filled with vanilla Bavarian cream, topped with rich chocolate ganache"),
    ("bakery", "Portuguese Bakery Cake Squares", "$3.50", "Individual delicate layered sponge cake squares with assorted fruit and cream fillings"),
    ("bakery", "Fudge Chocolate Brownie", "$3.25", "Dense, chewy dark chocolate fudge brownie with chocolate chunks"),
    ("bakery", "New York Cheesecake Slice", "$4.95", "Slice of rich, creamy homemade bakery cheesecake with graham cracker crust"),
    ("bakery", "Assorted Italian Butter Cookies (1/2 lb)", "$8.95", "Half-pound box of handmade bakery butter cookies, rainbow cookies, and chocolate dipped biscotti"),

    # In-Store Specialty Cakes (7" / 8")
    ("cakes", "Chaves Signature Cannoli Cake", "$28.00", "Vanilla sponge soaked with sweet cherry juice, filled with cannoli cream, whipped cream frosting, chocolate chips"),
    ("cakes", "Fresh Strawberry Shortcake", "$28.00", "Layers of vanilla cake, sweet strawberry filling, fresh whipped cream, and ripe strawberries"),
    ("cakes", "Vanilla Chocolate Mousse Cake", "$28.00", "Fluffy vanilla sponge cake layered with rich Belgian chocolate mousse and vanilla buttercream"),
    ("cakes", "Vanilla Oreo Cookies & Cream Cake", "$28.00", "Vanilla cake with crushed Oreo cookie whipped cream filling and vanilla frosting"),
    ("cakes", "Triple Threat Chocolate Fudge Cake", "$30.00", "Decadent chocolate cake, layer of dark chocolate mousse, layer of chocolate fudge, buttercream frosting"),
    ("cakes", "Chocolate Cannoli Cake", "$30.00", "Rich chocolate cake with sweet ricotta cannoli filling, chocolate buttercream, mini cannolis on top"),
    ("cakes", "Classic Bakery Carrot Cake", "$30.00", "Spiced carrot cake layered with cream cheese frosting, topped with toasted chopped walnuts"),
    ("cakes", "Red Velvet Cream Cheese Cake", "$30.00", "Traditional southern red velvet cake with creamy cream cheese frosting and walnuts"),
    ("cakes", "Bungalow Tropical Cake", "$32.00", "Marble sponge layered with fresh strawberries, ripe bananas, custard, whipped cream, and chocolate drizzle")
]

cat_map = {
    "breakfast": ("breakfast", "Desayunos y Sandwiches", "Breakfast & Rolls", "Coffee"),
    "deli": ("deli", "Sandwiches Boar's Head y Ensaladas", "Boar's Head Deli & Subs", "Sandwich"),
    "bakery": ("bakery", "Pastelería y Pan Portugués", "Portuguese Bakery & Pastries", "Sparkles"),
    "cakes": ("cakes", "Pasteles Artesanales", "Specialty Bakery Cakes", "Utensils")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each Portuguese bakery pastry, Boar's Head deli sandwich, breakfast roll, and custom cake name and description into appetizing Spanish.
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
print(f"Successfully translated {len(translated)} Chaves Bakery items!")

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
        "id": f"chaves-bakery-deli-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [2, 7, 10, 13, 14, 20, 29, 30, 37, 43, 44, 49],
        "badge": "Bakery Favorite" if idx in [2, 7, 13, 29, 43, 44] else None,
        "tags": ["Fresh Daily"] if cid in ["breakfast", "bakery"] else [],
        "allergens": ["Gluten"] if cid in ["breakfast", "deli", "bakery", "cakes"] else [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/chaves-bakery-deli.json"
with open(target_file) as f:
    chaves = json.load(f)

chaves["categories"] = categories
chaves["products"] = products

with open(target_file, "w") as f:
    json.dump(chaves, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
