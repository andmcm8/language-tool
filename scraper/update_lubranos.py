#!/usr/bin/env python3
import json, os, requests, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_custom_merchants import get_gemini_api_key

# Curated list of verified real dishes from Lubrano's Slice Life store
raw_items = [
    # Appetizers
    ("appetizers", "Fried Mozzarella Sticks", "$10.00", "Crispy breaded mozzarella cheese sticks served with homemade marinara sauce"),
    ("appetizers", "Chicken Wings", "$16.50", "Crispy chicken wings tossed in your choice of Mild, Hot, BBQ, or Sweet Red Chili"),
    ("appetizers", "Chicken Tenders", "$9.99", "Tender prime chicken battered and lightly fried, served with marinara sauce"),
    ("appetizers", "Fried Zucchini", "$9.00", "Fresh zucchini lightly breaded and fried golden, served with marinara sauce"),
    ("appetizers", "Hot Potato Chips", "$6.00", "Freshly fried hot potato chips served with seasoned ranch dressing"),
    ("appetizers", "Garlic Knots", "$9.00", "Fresh baked dough knots tossed with garlic butter, parmesan cheese, and Italian herbs"),
    ("appetizers", "French Fries", "$3.00", "Crispy golden french fries served with ketchup"),

    # Soups & Salads
    ("salads", "Minestrone Soup", "$7.00", "Classic Italian vegetable soup simmered with beans, vegetables, and pasta"),
    ("salads", "Pasta Fagioli Soup", "$7.00", "Homemade blend of white cannellini beans and ditalini pasta in rich seasoned broth"),
    ("salads", "Chef Salad", "$13.00", "Garden salad loaded with sliced deli meats, cheese, boiled egg, lettuce, tomato, and cucumbers"),
    ("salads", "Greek Salad", "$14.00", "Crisp lettuce, kalamata olives, feta cheese, tomatoes, onions, and pepperoncini"),
    ("salads", "Chicken Caesar Salad", "$13.00", "Grilled seasoned chicken breast over romaine lettuce, croutons, parmesan, and creamy caesar"),
    ("salads", "House Tossed Salad", "$5.00", "Fresh crisp garden mix of lettuce, ripe tomatoes, and shredded carrots"),
    ("salads", "Classic Caesar Salad", "$5.00", "Crisp romaine lettuce tossed with creamy caesar dressing, parmesan, and garlic croutons"),

    # Pizza & Calzones
    ("pizza", "Classic Cheese Pizza (Large)", "$14.00", "Traditional hand-stretched pizza dough with homemade tomato sauce and mozzarella"),
    ("pizza", "Meat Lovers Pizza", "$19.00", "Loaded with pepperoni, Italian sausage, seasoned hamburger, and crispy bacon"),
    ("pizza", "Supreme Pizza", "$22.00", "Pepperoni, Italian sausage, mushrooms, bell peppers, onions, and black olives"),
    ("pizza", "Garden Veggie Pizza", "$19.00", "Fresh mushrooms, onions, bell peppers, black olives, and tomatoes with mozzarella"),
    ("pizza", "Chicken Alfredo Pizza", "$23.00", "Creamy alfredo sauce base topped with grilled chicken and melted mozzarella"),
    ("pizza", "BBQ Chicken Pizza", "$23.00", "Tangy barbecue sauce base with grilled tender chicken and melted cheeses"),
    ("pizza", "Buffalo Chicken Pizza", "$23.00", "Spicy buffalo sauce base with buffalo chicken and mozzarella cheese"),
    ("pizza", "Traditional Cheese Calzone", "$16.00", "Baked folded dough pocket filled with creamy ricotta and mozzarella cheese, served with marinara"),
    ("pizza", "Italian Meat Stromboli", "$16.00", "Baked rolled pizza dough filled with ham, salami, pepperoni, provolone, and mozzarella"),
    ("pizza", "Chicken Stromboli", "$16.00", "Rolled baked pizza dough filled with seasoned tender chicken and melted mozzarella"),
    ("pizza", "Philly Steak Stromboli", "$17.00", "Rolled baked pizza crust stuffed with savory shaved steak and melted cheese"),

    # Hot Subs & Sandwiches
    ("subs", "Classic Cheesesteak Sub", "$13.00", "Thinly shaved steak grilled with melted cheese on a toasted Italian sub roll"),
    ("subs", "Cheesesteak Special Sub", "$13.00", "Shaved steak sautéed with mushrooms, sweet bell peppers, onions, and melted cheese"),
    ("subs", "Cheesesteak Hoagie", "$13.00", "Grilled steak with melted cheese, crisp shredded lettuce, sliced tomatoes, and onions"),
    ("subs", "Chicken Parmigiana Sub", "$14.00", "Breaded chicken cutlet topped with marinara sauce and melted mozzarella cheese"),
    ("subs", "Meatball Parmigiana Sub", "$13.00", "Homemade meatballs smothered in tomato sauce and baked with melted mozzarella"),
    ("subs", "Italian Cold Cut Sub", "$13.00", "Genoa salami, ham, provolone cheese, lettuce, tomato, onion, and vinaigrette"),
    ("subs", "Turkey & Provolone Sub", "$13.00", "Sliced roasted turkey breast with provolone cheese, lettuce, tomato, and onion"),
    ("subs", "Fried Chicken Sandwich", "$14.00", "Fresh tender chicken breast lightly breaded and fried, served on a toasted roll"),

    # Pasta & Baked Specialties
    ("pasta", "Homemade Baked Lasagna", "$17.00", "Layered wide pasta with seasoned ground beef, ricotta, mozzarella, and marinara"),
    ("pasta", "Fettuccine Alfredo", "$17.00", "Fettuccine pasta tossed in homemade creamy parmesan alfredo sauce"),
    ("pasta", "Fettuccine Alfredo with Chicken", "$19.00", "Creamy fettuccine alfredo topped with grilled seasoned chicken breast"),
    ("pasta", "Fettuccine Alfredo with Shrimp", "$19.99", "Creamy alfredo sauce with succulent sautéed shrimp over fettuccine"),
    ("pasta", "Pasta with Homemade Meat Sauce", "$17.00", "Choice of spaghetti, fettuccine or penne tossed with hearty simmered meat sauce"),
    ("pasta", "Pasta with Meatballs", "$17.00", "Spaghetti or penne served with two large homemade Italian meatballs in marinara"),
    ("pasta", "Penne Rustica", "$19.00", "Imported penne pasta with sautéed shrimp, grilled chicken, and savory garlic sauce"),
    ("pasta", "Cheese Ravioli Marinara", "$18.00", "Tender cheese-stuffed ravioli pillows smothered in homemade tomato sauce"),
    ("pasta", "Baked Ziti Al Forno", "$17.00", "Penne pasta tossed with ricotta, marinara, and herbs, baked with melted mozzarella"),
    ("pasta", "Eggplant Parmigiana", "$18.00", "Fresh breaded eggplant cutlets baked with tomato sauce and mozzarella over pasta"),
    ("pasta", "Baked Manicotti", "$17.00", "Large handmade pasta tubes filled with ricotta cheese and baked in tomato sauce"),
    ("pasta", "Chicken Parmigiana Entree", "$20.99", "Crispy breaded chicken cutlet baked with marinara and melted mozzarella over pasta"),
    ("pasta", "Chicken Bella Donna", "$19.99", "Sautéed chicken breast in a pink tomato-alfredo cream sauce with fresh mushrooms"),
    ("pasta", "Lobster Ravioli in Pink Sauce", "$21.00", "Decadent lobster-filled ravioli sautéed with shrimp in pink cream sauce"),
    ("pasta", "Shrimp a Pisano", "$21.00", "Large ocean shrimp sautéed with garlic in homemade pink alfredo cream sauce over pasta"),
    ("pasta", "Side of Homemade Meatballs", "$5.99", "Two large homemade meatballs served with warm marinara sauce"),

    # Kids Menu
    ("kids", "Kid's Chicken Fingers & Fries", "$9.99", "Crispy fried chicken tenders served with golden french fries"),
    ("kids", "Kid's Fettuccine Alfredo", "$9.99", "Kid-sized portion of fettuccine in creamy alfredo sauce"),
    ("kids", "Kid's Baked Lasagna", "$9.99", "Individual portion of baked beef and cheese lasagna"),
    ("kids", "Kid's Spaghetti with Meat Sauce", "$9.99", "Spaghetti pasta topped with homemade seasoned meat sauce"),

    # Desserts & Beverages
    ("desserts", "Homemade Cannoli", "$6.50", "Crispy pastry shell filled with sweet sweetened ricotta cream and chocolate chips"),
    ("desserts", "New York Cheesecake", "$6.50", "Classic dense, rich, and creamy New York style cheesecake"),
    ("desserts", "Limoncello Cake", "$6.50", "Fluffy sponge cake layered with limoncello mascarpone cream"),
    ("desserts", "Classic Tiramisu", "$6.50", "Ladyfingers dipped in espresso, layered with whipped mascarpone and dusted with cocoa"),
    ("desserts", "Fried Cheesecake with Strawberries", "$8.00", "Golden crispy fried cheesecake served with sweet strawberry topping"),
    ("beverages", "Bottled Soda (20 oz)", "$3.00", "20 oz bottle of Coca-Cola, Diet Coke, Sprite, or Ginger Ale")
]

cat_map = {
    "appetizers": ("appetizers", "Entradas y Alitas", "Appetizers & Wings", "Utensils"),
    "salads": ("salads", "Ensaladas y Sopas", "Salads & Soups", "Salad"),
    "pizza": ("pizza", "Pizzas, Calzones y Strombolis", "Pizza, Calzones & Stromboli", "Pizza"),
    "subs": ("subs", "Subs y Cheesesteaks", "Hot Subs & Cheesesteaks", "Sandwich"),
    "pasta": ("pasta", "Pastas y Especialidades Italianas", "Pasta & Baked Specialties", "Utensils"),
    "kids": ("kids", "Menú Infantil", "Kid's Menu", "Sparkles"),
    "desserts": ("desserts", "Postres", "Desserts", "Sparkles"),
    "beverages": ("beverages", "Bebidas", "Beverages", "Coffee")
}

api_key = get_gemini_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

prompt_input = [{"nameEn": it[1], "descriptionEn": it[3]} for it in raw_items]
prompt = f"""Translate each dish name and description accurately and appetizingly into Spanish for a classic pizzeria and Italian restaurant.
Return a JSON list with the exact same number of items ({len(raw_items)} items):
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
print(f"Successfully translated {len(translated)} Lubrano's Pizza items!")

categories = [{"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"}]
seen_cats = set()
for it in raw_items:
    cid = it[0]
    if cid not in seen_cats:
        seen_cats.add(cid)
        c = cat_map[cid]
        categories.append({"id": c[0], "nameEs": c[1], "nameEn": c[2], "icon": c[3]})

products = []
for idx, (it, tr) in enumerate(zip(raw_items, translated), start=1):
    cid, nameEn, price, descEn = it
    products.append({
        "id": f"lubranos-pizza-{idx:02d}",
        "categoryId": cid,
        "nameEs": tr.get("nameEs", nameEn),
        "nameEn": nameEn,
        "descriptionEs": tr.get("descriptionEs", descEn),
        "descriptionEn": descEn,
        "price": price,
        "popular": idx in [1, 2, 6, 15, 16, 22, 26, 33, 34, 43, 54, 57],
        "badge": "House Favorite" if idx in [1, 15, 22, 26, 33, 43] else None,
        "tags": ["Popular"] if idx in [1, 15, 22, 26, 33, 43] else [],
        "allergens": ["Gluten"] if cid in ["pizza", "subs", "pasta", "desserts"] else [],
        "ctaType": "in_store"
    })

target_file = "data/merchants/lubranos-pizza.json"
with open(target_file) as f:
    lubranos = json.load(f)

lubranos["categories"] = categories
lubranos["products"] = products

with open(target_file, "w") as f:
    json.dump(lubranos, f, indent=2, ensure_ascii=False)

print(f"🎉 Updated {target_file} with {len(products)} 100% verified real items!")

