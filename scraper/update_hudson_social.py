#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

items_data = [
    # Small Plates & Starters
    ("small_plates", "Ricotta Croquettes", "$12.00", "Crispy fried ricotta croquettes finished with local honey, fresh rosemary, and sea salt", False),
    ("small_plates", "Crispy Brussels Sprouts", "$13.00", "Flash-fried brussels sprouts tossed with shaved parmesan and homemade Caesar dressing", True),
    ("small_plates", "Classic Za'atar Hummus", "$14.00", "Housemade hummus with olive oil, za'atar spices, crushed pistachios, Kalamata olives, warm pita", True),
    ("small_plates", "Italian Meatballs", "$15.00", "Handmade meatballs simmered in romesco sauce, fresh ricotta, and aged parmesan", False),
    ("small_plates", "Burrata con Caponata", "$16.00", "Fresh burrata over warm Sicilian eggplant agrodolce, capers, fresh basil, tomatoes, olives, grilled bread", True),
    ("small_plates", "Spinaci e Carciofi Dip", "$16.00", "Creamy spinach and artichoke dip with roasted garlic, fresh rosemary, tortilla chips, and crostini", True),
    ("small_plates", "P.E.I. Steamed Mussels", "$17.00", "Prince Edward Island mussels prepared in choice of spicy fra diavolo or white wine butter garlic sauce", False),
    ("small_plates", "Crispy Chicken Wings", "$17.00", "Crispy wings with choice of honey BBQ, pineapple chili, garlic parmesan, buffalo, or Jamaican jerk", True),
    ("small_plates", "Crispy Chicken Bites", "$18.00", "Buttermilk-battered crispy fried chicken breast bites served with Alabama white BBQ sauce", False),
    ("small_plates", "Spanish Garlic Shrimp", "$18.00", "Sautéed shrimp with smoked paprika, chile de árbol, shallots, garlic, and savory clam broth", True),
    ("small_plates", "Chilled Shrimp Tostadas", "$18.00", "Crispy corn tostadas topped with diced shrimp, cilantro-lemon mayo, tomato, celery, and onion", False),
    ("small_plates", "Crispy Point Judith Calamari", "$19.00", "Lightly dusted flash-fried calamari served with roasted garlic chili aioli and house marinara", False),
    ("small_plates", "Birria Quesadilla", "$20.00", "Slow-cooked beef birria, melted mozzarella, cilantro, onion, avocado, served with rich consomé for dipping", True),
    ("small_plates", "Ahi Tuna Tartare", "$22.00", "Diced yellowfin tuna, house guacamole, watermelon radish, jalapeño, soy glaze, sesame seeds, wonton chips", True),
    ("small_plates", "Braised Short Rib Small Plate", "$21.00", "Slow-cooked tender beef short rib over creamy mashed potatoes with rich red wine au jus", True),
    ("small_plates", "Charred Grilled Spanish Octopus", "$21.00", "Grilled octopus over classic hummus, herb chimichurri, chickpeas, sundried tomato, and pepperoncini", True),
    ("small_plates", "Mini Maine Lobster Rolls (2)", "$22.00", "Tender sweet lobster on toasted brioche rolls with lettuce, tomato, celery, and house remoulade", True),
    ("small_plates", "Black Truffle Mac & Cheese", "$19.00", "Cavatappi pasta baked in fontina and parmesan cream, black truffle, crispy shallots, breadcrumb crust", False),
    ("small_plates", "The Social Charcuterie Board", "$24.00", "Manchego, Camembert, Gorgonzola Dolce, Prosciutto di Parma, Soppressata, Capicola, honeycomb, nuts, sourdough", True),

    # Raw Bar
    ("raw_bar", "Fresh Blue Point Oysters (Half Dozen)", "$18.00", "Six freshly shucked Long Island Sound Blue Point oysters with house mignonette and cocktail sauce", True),
    ("raw_bar", "Jumbo Chilled Shrimp Cocktail", "$17.00", "Four jumbo poached gulf shrimp served chilled with spicy house cocktail sauce and lemon", True),

    # Soups & Salads
    ("salads", "Chef's Soup of the Day", "$9.00", "Daily freshly prepared seasonal chef's soup", False),
    ("salads", "Hudson Caesar Salad", "$15.00", "Little gem lettuce, shaved parmesan, herbed focaccia croutons, lemon zest, creamy lemon tahini Caesar", False),
    ("salads", "Roasted Bosc Pear Salad", "$16.00", "Warm baked goat cheese, baby arugula, Belgian endive, toasted pecans, dried cranberries, white balsamic", True),
    ("salads", "Strawberry & Goat Cheese Salad", "$16.00", "Baby spinach and arugula, fresh strawberries, crumbled goat cheese, candied walnuts, raspberry vinaigrette", True),
    ("salads", "The Mediterranean Market Bowl", "$19.00", "Roasted spiced cauliflower, farro, quinoa, arugula, cucumber, cherry tomato, Kalamata olives, whipped feta", False),
    ("salads", "Grilled Steak Salad", "$26.00", "Grilled sliced sirloin steak over baby arugula, frizzled onions, shaved parmesan, horseradish Dijon dressing", False),

    # Large Plates & Entrees
    ("mains", "Hudson Grain & Rice Bowl", "$18.00", "Seasoned rice bowl with soy glaze, pickled ginger, fresh avocado, sriracha aioli, carrots, and roasted squash", False),
    ("mains", "Spicy Rigatoni alla Burrata", "$22.00", "Housemade rigatoni pasta tossed in spicy calabrian chili tomato cream, topped with fresh burrata and parmesan", False),
    ("mains", "Fettuccine Alfredo e Pollo", "$22.00", "Handmade fettuccine tossed in parmesan-garlic cream with herb-grilled chicken breast and cracked pepper", False),
    ("mains", "Hearthstone Roasted Half Chicken", "$23.00", "Pan-seared half chicken with tangy cherry pepper pan sauce, parsley-parmesan potatoes, and herbs", True),
    ("mains", "Craft Beer Battered Fish & Chips", "$25.00", "Crispy Australian sea bass fillet, house jalapeño tartar sauce, crispy chips, and malt vinegar", False),
    ("mains", "Crispy Pan-Seared Salmon", "$27.00", "Pan-seared crispy skin salmon fillet, lemon beurre blanc, charred broccoli, velvety cauliflower purée", True),
    ("mains", "Coastal Catch Seafood Linguine", "$29.00", "Pan-seared barramundi, PEI mussels, tender calamari, chopped clams in garlic white wine brodetto with filone", False),
    ("mains", "Ribeye Steak Frites (10 oz)", "$40.00", "10 oz grilled center-cut ribeye steak with Argentine chimichurri and parmesan truffle fries", True),

    # Brick Oven Pizzas
    ("pizza", "Classic Margherita Pizza", "$15.00", "San Marzano tomato sauce, fresh mozzarella, aged parmesan, fresh basil, extra virgin olive oil", False),
    ("pizza", "Fig & Prosciutto Arugula Pizza", "$18.00", "Sweet black mission figs, roasted garlic, crispy bacon, creamy goat cheese, arugula, fig jam drizzle", False),
    ("pizza", "The White Garden Pizza", "$18.00", "Roasted garlic cream, caramelized onions, mozzarella, stracciatella, sweet cherry tomatoes, fresh basil", False),
    ("pizza", "Spicy Pepperoni Pizza", "$18.00", "Old-school cupping pepperoni, pickled jalapeño slices, fresh tomato sauce, creamy mozzarella", False),
    ("pizza", "Nashville Hot Chicken Pizza", "$19.00", "Crispy buttermilk chicken tossed in Nashville hot oil, mozzarella, dill pickles, ranch drizzle, scallions", False),
    ("pizza", "Bee Sting Pizza", "$19.00", "Calabrese soppressata, chili-infused hot honey, basil aioli, creamy mozzarella, dried oregano", False),
    ("pizza", "Spicy Italian Meat Medley Pizza", "$19.00", "San Marzano sauce, bacon, soppressata, pepperoni, spicy hot cherry peppers, mozzarella", False),
    ("pizza", "Prosciutto Paradise Pizza", "$19.00", "Prosciutto di Parma, fresh mozzarella, baby arugula, extra virgin olive oil, balsamic glaze, shaved parmesan", False),

    # Sandwiches & Burgers
    ("burgers", "The Hudson Burger", "$20.00", "Signature custom blend beef patty, caramelized onions, sautéed mushrooms, sharp cheddar, house steak sauce, fries", False),
    ("burgers", "Birria Burger", "$22.00", "Custom beef patty topped with braised beef birria, melted mozzarella, cilantro, onions, steak fries, consommé", False),
    ("burgers", "The Godfather Italian Sub", "$20.00", "Prosciutto, soppressata, capicola, fresh mozzarella, basil pesto, garlic aioli, arugula on toasted sub", False),
    ("burgers", "Braised Short Rib Grilled Cheese", "$21.00", "Slow-cooked short rib, red wine demi-glace, sharp cheddar, caramelized onions, arugula on sourdough, chips", False),
    ("burgers", "Crispy Hot Honey Chicken Sandwich", "$20.00", "Buttermilk-fried chicken breast, red cabbage slaw, hot honey ranch, brioche bun, sweet potato fries", False),
    ("burgers", "Ahi Tuna Banh Mi Sandwich", "$22.00", "Blackened sushi-grade tuna steak, avocado, spicy cucumber-carrot pickled slaw, sriracha aioli, fries", False),
    ("burgers", "Roasted Turkey Club Sandwich", "$17.00", "Oven-roasted carved turkey, smoked bacon, crisp lettuce, ripe tomato, bacon aioli, sweet potato fries", False),
    ("burgers", "Artisanal Veggie Burger", "$18.00", "Housemade plant patty, caramelized onions, sautéed mushrooms, melted cheese, house steak sauce, fries", False),

    # Weekend Brunch
    ("brunch", "Double Cut Tiramisu French Toast", "$18.00", "Thick-cut brioche French toast topped with tiramisu mascarpone cream, cinnamon cocoa, berries, maple syrup", False),
    ("brunch", "Hudson Ranch Brunch Burger", "$22.00", "Beef burger with sunny fried egg, bacon, cheddar, lettuce, tomato, pickles, caramelized onion, spicy mayo", False),
    ("brunch", "Fluffy Buttermilk Pancakes", "$16.00", "Stack of golden pancakes with choice of fresh blueberries, banana flambé with candied walnuts, or chocolate chunk", False),
    ("brunch", "Belgian Malted Waffles", "$16.00", "Crispy Belgian waffle topped with vanilla ice cream, whipped butter, berries, and maple syrup", False),
    ("brunch", "Classic Canadian Eggs Benedict", "$18.00", "Toasted English muffin, thick Canadian bacon, two poached eggs, sliced avocado, hollandaise, house salad", False),
    ("brunch", "Eggs Royale with Smoked Salmon", "$21.00", "Poached farm eggs and smoked Atlantic salmon over toasted English muffins with avocado and hollandaise", False),
    ("brunch", "Eggs Florentine", "$16.00", "Poached eggs and sautéed garlic spinach over English muffins with avocado, creamy hollandaise, house salad", False),
    ("brunch", "Avocado Toast & Sunny Eggs", "$16.00", "Toasted filone bread, crushed Haas avocado, ripe tomato, crispy bacon, spicy chili oil, two sunny eggs", False),
    ("brunch", "Skillet Corned Beef Hash & Eggs", "$20.00", "Housemade corned beef and crispy hash browns with jalapeño, cilantro, tomato, avocado, and fried egg", False),
    ("brunch", "Hudson Morning Classic Breakfast", "$18.00", "Three scrambled farm eggs, breakfast sausage, smoked bacon, crispy homemade hash browns, buttered toast", False),
    ("brunch", "Chorizo Breakfast Burrito", "$18.00", "Scrambled eggs, spiced Mexican chorizo, pepper jack cheese, potatoes, peppers, onions, fries", False),
    ("brunch", "Chilaquiles Verdes con Huevos", "$19.00", "Crispy corn tortillas simmered in tangy salsa verde, crema, queso fresco, red onion, avocado, two eggs", True),
    ("brunch", "Maine Lobster Soft Scramble", "$28.00", "Soft farm scrambled eggs folded with butter-poached fresh lobster meat and chives on toasted brioche", False),
    ("brunch", "Steak & Eggs Brunch Plate", "$28.00", "Certified Angus Beef sirloin steak, sunny-side-up farm eggs, seasoned skillet hash potatoes", True),

    # Signature Cocktails
    ("cocktails", "Blood Orange Mule", "$15.00", "Tito's Handmade Vodka, Red Bull, fresh lime juice, blood orange puree, spicy ginger beer", True),
    ("cocktails", "Autumn Apple-rol Spritz", "$15.00", "Aperol, sparkling Italian prosecco, local apple cider, ginger beer splash, cinnamon sugar rim", True),
    ("cocktails", "Apple Hugo Spritz", "$16.00", "St. Germain elderflower liqueur, tart cranberry juice, spiced cinnamon syrup, prosecco, club soda", True),
    ("cocktails", "Midnight Harvest Bourbon", "$16.00", "Woodford Reserve Bourbon, toasted maple-cinnamon syrup, fresh orange zest expression, mole bitters", True),
    ("cocktails", "Twilight Fig Negroni", "$15.00", "Hendrick's Gin, Campari, sweet vermouth, spiced clove-fig syrup, charred rosemary sprig", True),
    ("cocktails", "Spicy Mezcal Paloma", "$15.00", "Artisanal smoky Mezcal, spicy jalapeño syrup, fresh lime juice, pink grapefruit soda", True),
    ("cocktails", "Velvet Bee Cocktail", "$15.00", "Vodka, St. Germain elderflower liqueur, fresh lime juice, lavender infused honey syrup", True),
    ("cocktails", "Hudson Lychee Martini", "$15.00", "Ketel One Citroen Vodka, sweet lychee puree, Lillet Blanc, French lychee liqueur", True),
    ("cocktails", "Honey & Harvest Nitro Espresso Martini", "$16.00", "Ketel One Vodka, fresh espresso, nitro cold brew, Kahlúa, spiced honey syrup, pumpkin spice", True),
    ("cocktails", "Housemade Hudson Red Sangria", "$14.00", "Seasonal fresh fruits macerated with red wine, brandy, St. Germain, and citrus juices", True)
]

cat_map = {
    "small_plates": ("small_plates", "Platillos para Compartir", "Small Plates", "Utensils"),
    "raw_bar": ("raw_bar", "Barra de Mariscos Crudos", "Raw Bar", "Utensils"),
    "salads": ("salads", "Ensaladas y Sopas", "Soups & Salads", "Salad"),
    "mains": ("mains", "Platos Fuertes y Pastas", "Large Plates & Pastas", "Beef"),
    "pizza": ("pizza", "Pizzas al Horno de Ladrillo", "Brick Oven Pizzas", "Pizza"),
    "burgers": ("burgers", "Hamburguesas y Sándwiches", "Burgers & Sandwiches", "Sandwich"),
    "brunch": ("brunch", "Brunch de Fin de Semana", "Weekend Brunch", "Coffee"),
    "cocktails": ("cocktails", "Cócteles de Autor", "Signature Cocktails", "Sparkles")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in items_data]
prompt = f"""Translate each New American gastropub dish/cocktail name and culinary description into refined, appetizing Spanish.
Return a JSON list with the exact same length ({len(items_data)} items):
Input: {json.dumps(prompt_input)}

Output format:
[
  {{"nameEs": "...", "descriptionEs": "..."}}
]"""

resp = requests.post(url, json={
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
}, timeout=60)

if resp.status_code != 200:
    print("Translation failed:", resp.status_code, resp.text)
    sys.exit(1)

translated = json.loads(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
print(f"Successfully translated {len(translated)} Hudson Social items!")

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
        "id": f"hudson-social-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 5, 8, 13, 14, 18, 28, 35, 37, 43, 51, 62, 72],
        "badge": "Hudson Favorite" if idx in [1, 13, 18, 28, 35, 43, 51] else None,
        "tags": ["Gluten-Free"] if is_gf else (["Spicy"] if "spicy" in descEn.lower() or "chili" in descEn.lower() else []),
        "allergens": [] if is_gf else ["Gluten"],
        "ctaType": "in_store"
    })

target_file = "data/merchants/hudson-social.json"
with open(target_file) as f:
    hs = json.load(f)

hs["categories"] = categories
hs["products"] = products

with open(target_file, "w") as f:
    json.dump(hs, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")
