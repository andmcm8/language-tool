#!/usr/bin/env python3
import json
import os
import sys

def build_cfcf():
    dest = "data/merchants/cfcf-coffee.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Store info
    data["storeInfo"]["name"] = "CFCF Coffee"
    data["storeInfo"]["address"] = "118 Greenwich Ave, Greenwich, CT 06830"
    data["storeInfo"]["tagline"] = "Gourmet Café, House-Roasted Coffee & Artisan Bites / Café Gourmet, Tostadores Artesanales y Pastelería"
    data["storeInfo"]["phone"] = "(203) 661-8300"

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Coffee"},
        {"id": "breakfast", "nameEs": "Desayunos Gourmet", "nameEn": "Artisan Breakfast", "icon": "Egg"},
        {"id": "sandwiches", "nameEs": "Sándwiches y Tostadas", "nameEn": "Sandwiches & Toasts", "icon": "Sandwich"},
        {"id": "salads", "nameEs": "Ensaladas Frescas", "nameEn": "Gourmet Salads", "icon": "Salad"},
        {"id": "espresso-coffee", "nameEs": "Café y Espresso Caliente", "nameEn": "Espresso & Hot Coffee", "icon": "Coffee"},
        {"id": "cold-brew-tea", "nameEs": "Cold Brew, Matcha y Tés", "nameEn": "Cold Brew, Teas & Specialty", "icon": "Wine"},
        {"id": "pastries", "nameEs": "Croissants y Panadería", "nameEn": "Pastries & Croissants", "icon": "Cake"}
    ]

    items = [
        # --- DESAYUNOS (Servidos hasta las 4pm) ---
        {
            "id": "bacon-egg-cheese-brioche",
            "nameEs": "Sándwich de Tocino, Huevo y Queso en Pan Brioche",
            "nameEn": "Bacon, Egg, & Cheese on Brioche Roll",
            "descriptionEs": "Huevo orgánico esponjoso, queso suizo derretido y tocino crujiente en panecillo brioche dorado con mantequilla.",
            "descriptionEn": "Organic egg, melted Swiss cheese, and crispy bacon on a toasted golden brioche roll.",
            "price": 9.50,
            "category": "breakfast",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "egg-cheddar-avocado-brioche",
            "nameEs": "Sándwich de Huevo, Cheddar y Aguacate en Brioche",
            "nameEn": "Egg, Cheddar, & Avocado on Brioche Roll",
            "descriptionEs": "Huevo orgánico tierno, queso cheddar añejo fundido y aguacate fresco rebanado en suave pan brioche.",
            "descriptionEn": "Fluffy organic egg, melted sharp cheddar cheese, and sliced ripe avocado on a warm brioche roll.",
            "price": 9.50,
            "category": "breakfast",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "smoked-salmon-brioche",
            "nameEs": "Salmón Ahumado en Pan Brioche con Queso Crema",
            "nameEn": "Smoked Salmon on Brioche",
            "descriptionEs": "Salmón ahumado del Atlántico, queso crema batido con cebollín fresco, hojas de rúcula silvestre y aguacate en brioche artesanal.",
            "descriptionEn": "Smoked Atlantic salmon, chive cream cheese, fresh baby arugula, and sliced avocado on a buttery brioche roll.",
            "price": 14.50,
            "category": "breakfast",
            "allergens": ["Gluten", "Lácteos", "Pescado"],
            "popular": True
        },
        {
            "id": "ricotta-pancakes",
            "nameEs": "Panqueques Caseros de Ricotta con Frutos Rojos",
            "nameEn": "House Ricotta Pancakes",
            "descriptionEs": "Esponjosos panqueques artesanales elaborados con queso ricotta fresco, servidos con bayas frescas de temporada y jarabe de arce puro.",
            "descriptionEn": "Light and fluffy pancakes made with fresh ricotta cheese, served with fresh seasonal berries and pure maple syrup.",
            "price": 13.00,
            "category": "breakfast",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "organic-overnight-oats",
            "nameEs": "Avena Orgánica Nocturna 'Overnight Oats' (Fría)",
            "nameEn": "Organic Cold Overnight Oats",
            "descriptionEs": "Avena orgánica hidratada durante la noche con leche de almendras sin endulzar, semillas de chía, fruta fresca y un toque de canela.",
            "descriptionEn": "Chilled organic rolled oats soaked overnight in unsweetened almond milk with chia seeds and seasonal fruit.",
            "price": 7.50,
            "category": "breakfast",
            "allergens": ["Frutos secos"]
        },
        {
            "id": "organic-hot-oatmeal",
            "nameEs": "Tazón de Avena Orgánica Caliente al Gusto",
            "nameEn": "Organic Hot Oatmeal Bowl",
            "descriptionEs": "Avena orgánica cocida al momento con leche al vapor o agua, con su elección de frutos secos: arándanos, pasas, nueces de castilla o almendras.",
            "descriptionEn": "Steamed organic rolled oats prepared with choice of steamed milk or water, topped with cranberries, raisins, walnuts, or almonds.",
            "price": 6.50,
            "category": "breakfast",
            "allergens": ["Frutos secos"]
        },

        # --- SANDWICHES & TOASTS ---
        {
            "id": "avocado-toast",
            "nameEs": "Tostada de Aguacate y Hummus con Semillas de Girasol",
            "nameEn": "Signature Avocado Toast",
            "descriptionEs": "Aguacate fresco machacado, hummus artesanal, semillas de girasol tostadas y hojuelas de chile rojo sobre pan multigrano horneado.",
            "descriptionEn": "Mashed fresh avocado, smooth hummus, toasted sunflower seeds, and crushed red pepper flakes on thick multigrain bread.",
            "price": 12.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Sésamo"],
            "popular": True
        },
        {
            "id": "prosciutto-deluxe-sandwich",
            "nameEs": "Sándwich Prosciutto Deluxe en Ciabatta",
            "nameEn": "Prosciutto Deluxe Sandwich",
            "descriptionEs": "Prosciutto di Parma importado curado, mozzarella fresca, jitomate maduro, rúcula tierna y pesto casero de albahaca en baguette ciabatta.",
            "descriptionEn": "Imported Prosciutto di Parma, fresh mozzarella, ripe tomato, baby arugula, and basil pesto on a crusty ciabatta baguette.",
            "price": 13.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos", "Frutos secos"],
            "popular": True
        },
        {
            "id": "tuna-special-sandwich",
            "nameEs": "Sándwich Especial de Atún Albacora y Frijoles",
            "nameEn": "Tuna Special Sandwich",
            "descriptionEs": "Atún blanco albacora selecto, frijoles blancos y negros sazonados con hierbas y lechuga Little Gem fresca en pan multigrano.",
            "descriptionEn": "Line-caught white albacore tuna, seasoned white and black beans, and crisp little gem lettuce on choice of artisan bread.",
            "price": 12.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Pescado"]
        },
        {
            "id": "the-mediterranean-sandwich",
            "nameEs": "Sándwich El Mediterráneo Vegetariano",
            "nameEn": "The Mediterranean Sandwich",
            "descriptionEs": "Hummus cremoso, queso de cabra desmoronado, aguacate, jitomate, pepino persa crujiente, col morada y rúcula en pan multigrano.",
            "descriptionEn": "Creamy hummus, goat cheese crumbles, sliced avocado, tomato, cucumber, red cabbage, and baby arugula on multigrain bread.",
            "price": 12.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos", "Sésamo"]
        },
        {
            "id": "turkey-classic-sandwich",
            "nameEs": "Sándwich Clásico de Pavo Asado y Aguacate",
            "nameEn": "Turkey Classic Sandwich",
            "descriptionEs": "Pechuga de pavo asada al horno, aguacate fresco, lechuga tierna y alioli casero de albahaca fresca en pan ciabatta.",
            "descriptionEn": "Oven-roasted turkey breast, fresh avocado, crisp lettuce, and fragrant basil aioli on ciabatta bread.",
            "price": 12.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Huevos"]
        },
        {
            "id": "chicken-salad-sandwich",
            "nameEs": "Sándwich de Ensalada de Pollo al Cebollín",
            "nameEn": "CFCF Chicken Salad Sandwich",
            "descriptionEs": "Pechuga de pollo tierna desmenuzada, mayonesa artesanal, crema ácida, cebollín picado y hojas de lechuga Little Gem.",
            "descriptionEn": "Tender chicken breast, house mayonnaise, sour cream, fresh chives, and crisp little gem lettuce on artisan bread.",
            "price": 12.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "ham-swiss-sandwich",
            "nameEs": "Sándwich de Jamón Selva Negra y Queso Suizo",
            "nameEn": "Black Forest Ham & Swiss Sandwich",
            "descriptionEs": "Jamón artesanal curado, queso suizo fundente y alioli de mostaza Dijon en pan baguette ciabatta crujiente.",
            "descriptionEn": "Fine cured ham, imported Swiss cheese, and zesty mustard aioli on a toasted ciabatta baguette.",
            "price": 11.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "caprese-sandwich",
            "nameEs": "Sándwich Caprese Clásico con Pesto",
            "nameEn": "Classic Caprese Sandwich",
            "descriptionEs": "Mozzarella fresca artesanal, rebanadas de jitomate maduro, hojas de rúcula y pesto fresco de albahaca en ciabatta.",
            "descriptionEn": "Fresh mozzarella, ripe vine tomatoes, baby arugula, and aromatic basil pesto on ciabatta bread.",
            "price": 11.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos", "Frutos secos"]
        },
        {
            "id": "italian-herb-chicken-sandwich",
            "nameEs": "Sándwich de Pollo a las Hierbas Italianas",
            "nameEn": "Italian Herb Chicken Sandwich",
            "descriptionEs": "Pollo asado con hierbas italianas, pesto de jitomate deshidratado, mezcla de hojas verdes, cebolla morada y mozzarella fresca.",
            "descriptionEn": "Herb-roasted chicken breast, sun-dried tomato pesto, mixed greens, red onion, and fresh mozzarella on ciabatta.",
            "price": 13.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos", "Frutos secos"],
            "popular": True
        },
        {
            "id": "organic-egg-salad-sandwich",
            "nameEs": "Sándwich de Ensalada de Huevos Orgánicos",
            "nameEn": "Organic Egg Salad Sandwich",
            "descriptionEs": "Huevos orgánicos cocidos mezclados con mayonesa casera, lechuga y jitomate maduro en pan multigrano.",
            "descriptionEn": "Organic hard-boiled eggs mashed with mayonnaise, fresh lettuce, and ripe tomatoes on multigrain bread.",
            "price": 10.50,
            "category": "sandwiches",
            "allergens": ["Gluten", "Huevos"]
        },

        # --- ENSALADAS ---
        {
            "id": "golden-beet-salad",
            "nameEs": "Ensalada de Remolacha Amarilla y Queso de Cabra",
            "nameEn": "Golden Beet & Goat Cheese Salad",
            "descriptionEs": "Remolachas amarillas asadas, queso de cabra batido cremoso, semillas de calabaza tostadas, rúcula tierna y vinagreta de jerez.",
            "descriptionEn": "Roasted golden beets, whipped creamy goat cheese, toasted pumpkin seeds, baby arugula, and sherry vinaigrette.",
            "price": 14.00,
            "category": "salads",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "kale-lemon-salad",
            "nameEs": "Ensalada de Col Rizada (Kale) al Limón y Menta",
            "nameEn": "Kale & Lemon Salad with Mint",
            "descriptionEs": "Hojas tiernas de col rizada kale, jugo de limón fresco, chiles serranos en rodajas finas, menta fresca y crutones dorados a las hierbas.",
            "descriptionEn": "Tender chopped kale, fresh lemon, thinly sliced serrano chillies, fresh mint, and toasted herb croutons.",
            "price": 13.00,
            "category": "salads",
            "allergens": ["Gluten"]
        },
        {
            "id": "mediterraneo-salad",
            "nameEs": "Ensalada Mediterráneo con Garbanzos y Tahini",
            "nameEn": "Mediterraneo Salad with Tahini",
            "descriptionEs": "Pepino persa crujiente, garbanzos cocidos sazonados, lechuga Little Gem y aderezo cremoso de tahini y limón.",
            "descriptionEn": "Crisp cucumbers, seasoned chickpeas, tender little gem lettuce, and creamy house tahini lemon dressing.",
            "price": 13.00,
            "category": "salads",
            "allergens": ["Sésamo"]
        },
        {
            "id": "quinoa-apple-walnut-salad",
            "nameEs": "Ensalada de Quinua, Manzana y Nueces",
            "nameEn": "Quinoa, Apple, & Walnut Salad",
            "descriptionEs": "Quinua orgánica cocida, hojas de rúcula silvestre, manzana verde picada, nueces de castilla tostadas y vinagreta de sidra de manzana.",
            "descriptionEn": "Organic quinoa, wild baby arugula, diced crisp apples, toasted walnuts, and house apple cider vinaigrette.",
            "price": 13.50,
            "category": "salads",
            "allergens": ["Frutos secos"]
        },
        {
            "id": "mixed-greens-pecorino-salad",
            "nameEs": "Ensalada Verde Mixta con Queso Pecorino",
            "nameEn": "Mixed Green Salad with Shaved Pecorino",
            "descriptionEs": "Hojas verdes mixtas de huerto, col morada, tomates cherry dulces, aguacate fresco, lajas de queso pecorino italiano y vinagreta de sidra.",
            "descriptionEn": "Organic mixed greens, red cabbage, cherry tomatoes, avocado, shaved pecorino cheese, and apple cider vinaigrette.",
            "price": 12.50,
            "category": "salads",
            "allergens": ["Lácteos"]
        },

        # --- ESPRESSO Y CAFÉ CALIENTE ---
        {
            "id": "espresso-double",
            "nameEs": "Espresso Doble de Especialidad",
            "nameEn": "Double Espresso",
            "descriptionEs": "Doble extracción de café en grano tostado artesanalmente por CFCF, notas a caramelo y chocolate con crema densa.",
            "descriptionEn": "Double shot of CFCF house-roasted specialty espresso with a rich crema and notes of caramel and cocoa.",
            "price": 3.55,
            "category": "espresso-coffee",
            "popular": True
        },
        {
            "id": "cappuccino",
            "nameEs": "Cappuccino Tradicional Italiano",
            "nameEn": "Traditional Cappuccino",
            "descriptionEs": "Doble carga de espresso combinada con partes iguales de leche vaporizada y microespuma densa aterciopelada.",
            "descriptionEn": "Double shot of espresso layered with equal parts velvety steamed milk and thick microfoam.",
            "price": 5.35,
            "category": "espresso-coffee",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "cafe-latte",
            "nameEs": "Café Latte",
            "nameEn": "Café Latte",
            "descriptionEs": "Espresso suave combinado con abundante leche cremosa texturizada al vapor y una fina capa de espuma.",
            "descriptionEn": "Smooth double espresso combined with velvety steamed whole milk and a delicate layer of foam.",
            "price": 5.35,
            "category": "espresso-coffee",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "cortado",
            "nameEs": "Cortado",
            "nameEn": "Cortado",
            "descriptionEs": "Partes iguales de intenso espresso doble y leche sedosa al vapor en vaso de cristal tradicional.",
            "descriptionEn": "Equal parts rich double espresso and silky warm steamed milk served in a traditional glass tumbler.",
            "price": 4.55,
            "category": "espresso-coffee",
            "allergens": ["Lácteos"]
        },
        {
            "id": "flat-white",
            "nameEs": "Flat White Estilo Australiano",
            "nameEn": "Flat White",
            "descriptionEs": "Doble espresso ristretto infusionado con leche vaporizada finamente texturizada con microburbujas sin espuma gruesa.",
            "descriptionEn": "Double ristretto espresso shots blended seamlessly with micro-textured velvety steamed milk.",
            "price": 5.15,
            "category": "espresso-coffee",
            "allergens": ["Lácteos"]
        },
        {
            "id": "americano",
            "nameEs": "Café Americano",
            "nameEn": "Caffè Americano",
            "descriptionEs": "Doble carga de espresso vertida sobre agua caliente filtrada, conservando los aromas profundos del grano.",
            "descriptionEn": "Double shot of house espresso poured over hot filtered water for a clean, rich coffee profile.",
            "price": 4.45,
            "category": "espresso-coffee"
        },
        {
            "id": "cafe-mocha",
            "nameEs": "Café Mocha con Cacao Holandés",
            "nameEn": "Caffè Mocha with Dutch Chocolate",
            "descriptionEs": "Espresso intenso, salsa de chocolate oscuro holandés de primera calidad y leche caliente al vapor.",
            "descriptionEn": "Rich espresso, premium Dutch dark chocolate cocoa, and steamed milk finished with a touch of foam.",
            "price": 6.25,
            "category": "espresso-coffee",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "pour-over-single-origin",
            "nameEs": "Café Filtrado Manual 'Pour Over' de Origen Único",
            "nameEn": "House Roasted Single Origin Pour Over",
            "descriptionEs": "Café filtrado por goteo manual preparado taza por taza con los mejores granos tostados en casa por los maestros baristas de CFCF.",
            "descriptionEn": "Handcrafted pour-over coffee brewed cup-by-cup using CFCF's house-roasted single origin micro-lots.",
            "price": 5.00,
            "category": "espresso-coffee"
        },

        # --- COLD BREW, MATCHA Y TÉS ---
        {
            "id": "kyoto-cold-brew",
            "nameEs": "Cold Brew Estilo Kyoto de Goteo Lento (12 Horas)",
            "nameEn": "Kyoto-Style Single Origin Cold Brew",
            "descriptionEs": "El orgullo de CFCF: extracción gota a gota durante 12 horas en torres de cristal japonesas. Complejo, sedoso, aromático y sin amargor.",
            "descriptionEn": "Slow-drip 12-hour cold extraction brewed through Japanese Kyoto glass towers. Incredibly smooth, floral, and naturally sweet.",
            "price": 6.50,
            "category": "cold-brew-tea",
            "popular": True
        },
        {
            "id": "cold-brew-super-bar",
            "nameEs": "Cold Brew Artesanal Super Bar en Barril",
            "nameEn": "Super Bar Draft Cold Brew",
            "descriptionEs": "Café frío infusionado durante 24 horas servido de grifo sobre hielo, limpio y profundamente energizante.",
            "descriptionEn": "CFCF's signature 24-hour steeped craft cold brew served cold on tap over ice.",
            "price": 5.25,
            "category": "cold-brew-tea",
            "popular": True
        },
        {
            "id": "nitro-cold-brew",
            "nameEs": "Nitro Cold Brew Infusionado con Nitrógeno",
            "nameEn": "Nitro Super Bar Cold Brew",
            "descriptionEs": "Cold brew servido con microburbujas de nitrógeno que producen una textura ultra cremosa similar a una cerveza Guinness sin lácteos.",
            "descriptionEn": "Nitrogen-infused cold brew cascading with a velvety Guinness-like crema head and naturally sweet mouthfeel.",
            "price": 6.00,
            "category": "cold-brew-tea",
            "popular": True
        },
        {
            "id": "iced-latte",
            "nameEs": "Café Latte Helado",
            "nameEn": "Iced Caffè Latte",
            "descriptionEs": "Doble carga de espresso vertida sobre leche fría fresca y hielo cristalino.",
            "descriptionEn": "Double shot of espresso poured over chilled fresh milk and ice.",
            "price": 5.35,
            "category": "cold-brew-tea",
            "allergens": ["Lácteos"]
        },
        {
            "id": "matcha-latte",
            "nameEs": "Matcha Latte Ceremonial Japonés",
            "nameEn": "Ceremonial Japanese Matcha Latte",
            "descriptionEs": "Té verde matcha japonés de grado ceremonial batido artesanalmente con leche de avena o entera, servido frío o caliente.",
            "descriptionEn": "Authentic ceremonial grade Japanese green matcha whisked with your choice of steamed or iced milk.",
            "price": 6.25,
            "category": "cold-brew-tea",
            "popular": True
        },
        {
            "id": "turmeric-latte",
            "nameEs": "Leche Dorada con Cúrcuma (Turmeric Latte)",
            "nameEn": "Golden Milk Turmeric Latte",
            "descriptionEs": "Cúrcuma orgánica molida, canela, jengibre y leche al vapor de avena o almendra (sin cafeína).",
            "descriptionEn": "Organic ground turmeric, cinnamon, ginger, and steamed milk (hot or iced). Naturally caffeine-free.",
            "price": 6.25,
            "category": "cold-brew-tea"
        },
        {
            "id": "espresso-tonic",
            "nameEs": "Espresso Tónico con Cítricos",
            "nameEn": "Craft Espresso Tonic",
            "descriptionEs": "Doble espresso aromático vertido sobre agua tónica artesanal burbujeante y rodaja de cítrico con hielo.",
            "descriptionEn": "Double shot of espresso poured over chilled sparkling tonic water with a fresh citrus twist.",
            "price": 6.00,
            "category": "cold-brew-tea"
        },
        {
            "id": "chai-tea-latte",
            "nameEs": "Chai Latte Especiado",
            "nameEn": "Spiced Chai Tea Latte",
            "descriptionEs": "Té negro infusionado con cardamomo, canela, jengibre y clavos de olor, vaporizado con leche sedosa.",
            "descriptionEn": "Spiced black tea infused with cardamom, cinnamon, cloves, and ginger, blended with steamed milk.",
            "price": 5.50,
            "category": "cold-brew-tea",
            "allergens": ["Lácteos"]
        },
        {
            "id": "ginger-tonic-tea",
            "nameEs": "Té Tónico de Jengibre Natural (Frío o Caliente)",
            "nameEn": "Fiery Ginger Tonic Tea",
            "descriptionEs": "Infusión pura de raíz de jengibre fresca, miel y limón, revitalizante y antiinflamatoria.",
            "descriptionEn": "Fresh steeped spicy ginger root tea served steaming hot or iced with a touch of honey and lemon.",
            "price": 4.75,
            "category": "cold-brew-tea"
        },
        {
            "id": "fresh-lemonade",
            "nameEs": "Limonada Fresca Artesanal",
            "nameEn": "Fresh Squeezed House Lemonade",
            "descriptionEs": "Jugo de limón recién exprimido, azúcar de caña pura y agua filtrada sobre hielo.",
            "descriptionEn": "Freshly squeezed lemon juice, pure cane sugar, and filtered water served over ice.",
            "price": 4.50,
            "category": "cold-brew-tea"
        },

        # --- CROISSANTS Y PASTELERÍA ---
        {
            "id": "butter-croissant",
            "nameEs": "Croissant Francés de Mantequilla",
            "nameEn": "Classic French Butter Croissant",
            "descriptionEs": "Croissant tradicional hojaldrado con mantequilla francesa de alta calidad, horneado fresco todas las mañanas.",
            "descriptionEn": "Flaky, buttery French croissant baked fresh daily with crisp golden layers.",
            "price": 4.25,
            "category": "pastries",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "chocolate-croissant",
            "nameEs": "Pain au Chocolat (Croissant de Chocolate)",
            "nameEn": "Pain au Chocolat (Chocolate Croissant)",
            "descriptionEs": "Hojaldre crujiente relleno con barras de chocolate semiamargo belga fundente.",
            "descriptionEn": "Classic all-butter flaky pastry filled with two batons of semi-sweet Belgian dark chocolate.",
            "price": 4.75,
            "category": "pastries",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "nutella-croissant",
            "nameEs": "Croissant Hojaldrado Relleno de Nutella",
            "nameEn": "Nutella Filled Croissant",
            "descriptionEs": "Croissant artesanal dorado relleno generosamente con crema suave de avellanas y chocolate Nutella.",
            "descriptionEn": "Golden flaky croissant generously filled with rich creamy hazelnut Nutella spread.",
            "price": 5.25,
            "category": "pastries",
            "allergens": ["Gluten", "Lácteos", "Frutos secos"],
            "popular": True
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(items)} verified items to {dest}!")

if __name__ == "__main__":
    build_cfcf()

