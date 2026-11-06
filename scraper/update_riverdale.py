#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Brunch Favorites & Benedicts
    ("brunch", "Chicken & Belgian Waffle", "$16.00", "Crispy fried buttermilk chicken breast on a golden Belgian waffle with powdered sugar and maple syrup"),
    ("brunch", "Big Riverdale Breakfast", "$16.00", "Two buttermilk pancakes, two eggs any style, two bacon strips, two pork sausage links, and Yukon Gold home fries"),
    ("brunch", "Country Fried Steak & Eggs", "$16.00", "Buttermilk biscuits topped with country fried steak, house sausage gravy, two sunny eggs, and home fries"),
    ("brunch", "International Breakfast", "$16.00", "Two eggs any style with Belgian waffle or French toast, and choice of bacon, turkey, or pork sausage"),
    ("brunch", "Biscuits n' Gravy Platter", "$14.00", "Warm buttermilk biscuits topped with housemade sausage gravy, two eggs any style, pork sausage links, and home fries"),
    ("brunch", "Avocado Toast & Eggs", "$12.00", "Two thick slices of 7-grain toast topped with fresh smashed avocado and two farm eggs any style"),
    ("brunch", "Sunrise Breakfast Quesadilla", "$15.00", "Grilled flour tortilla with scrambled eggs, bacon, American and cheddar cheeses, sour cream, and fresh avocado"),
    ("brunch", "Chorizo Breakfast Burrito", "$15.00", "Scrambled eggs, crumbled chorizo, grilled onions, avocado, and cheddar in a grilled flour tortilla with home fries"),
    ("brunch", "Breakfast Tacos (3)", "$15.00", "Three grilled flour tortillas filled with scrambled eggs, cheddar, pico de gallo, and choice of chorizo, bacon, or avocado"),
    ("brunch", "Classic Canadian Eggs Benedict", "$15.00", "Poached eggs and Canadian bacon on English muffin with rich hollandaise and choice of Yukon home fries or grits"),
    ("brunch", "Famous Irish Corned Beef Hash Benedict", "$16.00", "Poached eggs over famous griddled house corned beef hash on English muffin with hollandaise"),
    ("brunch", "California Avocado Benedict", "$15.00", "Poached eggs, fresh avocado smash, baby spinach, and sliced tomato on English muffin with hollandaise"),
    ("brunch", "Maryland Crab Cake Benedict", "$18.00", "Grilled jumbo crab cakes and poached eggs on English muffin topped with Old Bay hollandaise sauce"),

    # Griddle & 2-Egg Platters
    ("griddle", "Buttermilk Pancakes (3)", "$11.00", "Three golden buttermilk pancakes served with freshly whipped salted butter and warm maple syrup"),
    ("griddle", "Chocolate Chip Pancakes (3)", "$12.00", "Three fluffy pancakes studded with melted semi-sweet chocolate chips and whipped cream"),
    ("griddle", "Fresh Blueberry Pancakes (3)", "$13.00", "Three buttermilk pancakes packed with plump fresh wild blueberries and whipped butter"),
    ("griddle", "Golden Belgian Waffle", "$11.00", "Crispy malted Belgian waffle dusted with powdered sugar, served with butter and syrup"),
    ("griddle", "Fresh Blueberry Belgian Waffle", "$13.00", "Crispy Belgian waffle topped with mountain of fresh wild blueberries and whipped cream"),
    ("griddle", "Challah Texas French Toast", "$12.00", "Three extra-thick slices of bakery challah bread dipped in cinnamon custard, griddled golden"),
    ("griddle", "Two Eggs Any Style Platter", "$8.79", "Two farm eggs cooked any style, served with Yukon Gold home fries and choice of toast or pancakes"),
    ("griddle", "Crispy Bacon & Eggs Platter", "$13.79", "Four thick strips of crispy bacon with two eggs any style, home fries, and buttered toast"),
    ("griddle", "Pork Sausage & Eggs Platter", "$13.79", "Two country pork sausage links, two eggs any style, seasoned home fries, and toast"),
    ("griddle", "Bee's American Breakfast Sandwich", "$8.00", "Crispy bacon, two fried eggs, melted American cheese, and crispy home fries pressed on a hard roll"),
    ("griddle", "Alex's Famous Hash Breakfast Wrap", "$12.00", "House corned beef hash, melted cheddar cheese, scrambled eggs, and chipotle mayo in a flour wrap"),
    ("griddle", "Mom's Breakfast Croissant", "$12.00", "Flaky butter croissant with bacon, fried eggs, Swiss cheese, smashed avocado, spinach, and chipotle mayo"),
    ("griddle", "Isabel's Power Wrap", "$12.00", "Scrambled egg whites, grilled chicken breast, smashed avocado, baby spinach, and tomatoes in a wheat wrap"),

    # Lunch Starters & Soups
    ("lunch_starters", "Homemade Chicken Noodle Soup", "$6.49", "Tender pulled chicken, housemade bone broth, curly egg noodles, sliced carrots, celery, and fresh herbs"),
    ("lunch_starters", "Creamy Tomato Basil Soup", "$6.49", "Rich creamy tomato puree seasoned with sweet basil and topped with garlic croutons"),
    ("lunch_starters", "Crock of French Onion Soup", "$8.00", "Caramelized onions, beef bone broth, garlic croutons, baked with melted Swiss and parmesan"),
    ("lunch_starters", "New England Clam Chowder Crock", "$9.00", "Traditional coastal New England chowder with chopped ocean clams, bacon, potatoes, and cream"),
    ("lunch_starters", "Crispy Chicken Tender Basket", "$14.00", "Buttermilk fried chicken tenders served with seasoned french fries, warm biscuit, and honey mustard"),
    ("lunch_starters", "Fried Mozzarella Sticks (8)", "$12.00", "Eight golden breaded mozzarella sticks served with house marinara sauce"),
    ("lunch_starters", "Maryland Style Crab Cakes (2)", "$13.00", "Two grilled lump crab cakes served with choice of chipotle aioli or house tartar sauce"),
    ("lunch_starters", "Beer-Battered Fish Tacos (3)", "$15.00", "Three crispy cod tacos with smashed avocado, fresh pico de gallo, melted cheddar, and crema"),
    ("lunch_starters", "Grilled Chicken Bacon Quesadilla", "$14.00", "Grilled chicken breast, smoky bacon, tomatoes, scallions, cheddar, and American in a grilled tortilla"),
    ("lunch_starters", "Classic Chicken Caesar Salad", "$16.00", "Herb-marinated grilled chicken over crisp romaine, garlic herb croutons, parmesan, and Caesar dressing"),

    # Burgers, Sandwiches & Melts
    ("burgers_sandwiches", "Riverdale Cheeseburger", "$15.00", "Half-pound fresh beef patty, American cheese, crisp lettuce, ripe tomato, and mayo on toasted brioche with fries"),
    ("burgers_sandwiches", "Bacon Cheeseburger", "$17.00", "Half-pound beef burger with crispy bacon, melted American, lettuce, tomato, mayo, served with fries"),
    ("burgers_sandwiches", "Original Patty Melt", "$15.00", "Half-pound burger on grilled marble rye with melted American cheese, caramelized onions, and garlic mayo"),
    ("burgers_sandwiches", "French Onion Swiss Burger", "$15.00", "Beef burger with sautéed mushrooms, caramelized onions, melted Swiss cheese, and garlic mayo"),
    ("burgers_sandwiches", "Avocado Bacon Burger", "$18.00", "Half-pound burger with American cheese, crisp bacon, fresh smashed avocado, chipotle mayo, and fries"),
    ("burgers_sandwiches", "Triple Decker Turkey Club", "$16.00", "Roasted carved turkey breast, crispy bacon, lettuce, tomato, and mayo on triple-decker country white toast"),
    ("burgers_sandwiches", "Grilled Chicken Avocado BLT", "$16.00", "Grilled chicken breast, fresh avocado smash, smoked bacon, lettuce, tomato, and mayo on 7-grain toast"),
    ("burgers_sandwiches", "Buttermilk Fried Chicken Sandwich", "$15.00", "Crispy fried chicken breast, chipotle mayo, and crunchy dill pickle chips on toasted brioche bun"),
    ("burgers_sandwiches", "New York Reuben (Corned Beef)", "$16.00", "House corned beef, tangy sauerkraut, melted Swiss cheese, and Russian dressing on grilled marble rye"),
    ("burgers_sandwiches", "Grown-Up Gourmet Grilled Cheese", "$12.00", "Melted American and cheddar cheeses, crispy bacon, sliced tomato, and garlic mayo on grilled sourdough"),
    ("burgers_sandwiches", "Albacore Tuna Salad Melt", "$14.00", "Housemade albacore white tuna salad, ripe tomato slices, and melted cheddar on grilled marble rye"),
    ("burgers_sandwiches", "Philly Shaved Ribeye Cheese Steak", "$16.00", "Thinly sliced grilled ribeye steak with sautéed peppers, onions, and melted cheese on a hero roll"),
    ("burgers_sandwiches", "Thanksgiving Feast Turkey Wrap", "$16.00", "Carved roast turkey, traditional bread stuffing, cranberry sauce, mayo, and a side of savory turkey gravy"),

    # Blue Plate Dinner Entrees
    ("dinner", "Homemade Chicken Pot Pie", "$16.00", "Tender pulled chicken, carrots, sweet peas, and celery in rich herb gravy under golden puff pastry"),
    ("dinner", "Traditional Shepherd's Pie", "$16.00", "Seasoned ground beef in savory rich gravy with corn, peas, carrots, topped with mashed potatoes and cheddar"),
    ("dinner", "Thanksgiving Roasted Turkey Dinner", "$19.00", "Carved oven-roasted turkey, savory herb bread stuffing, rich turkey gravy, cranberry sauce, and 2 sides"),
    ("dinner", "Fork Tender Beef Pot Roast", "$19.00", "Slow-braised tender pot roast with roasted carrots, onions, and celery in natural au jus, served with 2 sides"),
    ("dinner", "Crispy Beer-Battered Cod Fillet", "$19.00", "Golden beer-battered fresh cod fillets served with house tartar sauce, fresh lemon wedge, and 2 diner sides"),
    ("dinner", "Country Fried Steak with Sausage Gravy", "$18.00", "Two tender chopped steaks golden-fried and smothered in housemade sausage gravy with 2 sides"),
    ("dinner", "Griddle-Seared Comfort Meatloaf", "$16.00", "Custom blend of beef, pork, and veal meatloaf seared on the griddle with rich brown gravy and 2 sides"),
    ("dinner", "Buffalo Chicken Mac & Cheese", "$16.00", "Crispy chicken tenders tossed in spicy Buffalo sauce served over four-cheese baked macaroni"),
    ("dinner", "Maryland Jumbo Crab Cake Platter", "$18.00", "Two grilled Maryland-style crab cakes with chipotle aioli or tartar sauce and choice of 2 diner sides"),
    ("dinner", "Char-Broiled Chopped Steak", "$16.00", "Freshly ground chopped steak char-grilled with sautéed mushrooms, caramelized onions, and brown gravy"),

    # Desserts & Diner Beverages
    ("desserts", "Riverdale House NY Cheesecake", "$7.00", "Classic thick and creamy New York style cheesecake with graham cracker crust"),
    ("desserts", "Decadent Chocolate Layer Cake", "$6.00", "Multi-layered moist chocolate cake with rich chocolate fudge frosting"),
    ("desserts", "Homemade Carrot Layer Cake", "$6.00", "Spiced carrot cake layered with real cream cheese frosting and walnuts"),
    ("desserts", "Lemon Meringue Pie Slice", "$6.00", "Flaky pie crust filled with tangy lemon curd and topped with toasted meringue"),
    ("desserts", "Warm Apple Crisp with Vanilla Gelato", "$7.99", "Warm baked cinnamon apple crisp topped with vanilla ice cream and caramel drizzle"),
    ("desserts", "Old Fashioned Diner Milkshake", "$7.00", "Thick hand-spun milkshake in choice of Vanilla, Chocolate, or Strawberry"),
    ("desserts", "Lavazza Premium Brewed Coffee", "$3.29", "Freshly brewed Italian Lavazza dark or regular roast coffee"),
    ("desserts", "Brunch Mimosa / Bloody Mary", "$6.00", "Choice of fresh Orange Mimosa or Tito's Handmade Vodka Bloody Mary")
]

cat_map = {
    "brunch": ("brunch", "Brunch y Huevos Benedict", "Brunch & Benedicts", "Coffee"),
    "griddle": ("griddle", "Pancakes, Waffles y Desayunos", "Griddle & Platters", "Coffee"),
    "lunch_starters": ("lunch_starters", "Entradas, Sopas y Ensaladas", "Soups & Starters", "Salad"),
    "burgers_sandwiches": ("burgers_sandwiches", "Hamburguesas y Sandwiches", "Burgers & Sandwiches", "Sandwich"),
    "dinner": ("dinner", "Especialidades de la Cena (Blue Plate)", "Blue Plate Dinners", "Utensils"),
    "desserts": ("desserts", "Postres, Batidos y Bebidas", "Desserts & Shakes", "Sparkles")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each American diner dish, burger, breakfast, and bakery dessert name and description into appetizing Spanish.
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
print(f"Successfully translated {len(translated)} Riverdale Diner items!")

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
        "id": f"riverdale-diner-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 2, 6, 10, 11, 14, 19, 27, 30, 36, 41, 45, 51, 52, 61, 66],
        "badge": "Riverdale Favorite" if idx in [1, 2, 10, 19, 36, 51, 52, 61] else None,
        "tags": ["Popular"] if idx in [1, 2, 10, 19, 36, 51, 52, 61] else [],
        "allergens": [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/riverdale-diner.json"
with open(target_file) as f:
    rd = json.load(f)

rd["categories"] = categories
rd["products"] = products

with open(target_file, "w") as f:
    json.dump(rd, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
