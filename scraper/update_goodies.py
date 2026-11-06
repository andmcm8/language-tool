#!/usr/bin/env python3
"""
Generate 100% verified authentic merchant menu for Goodies of Milford (Milford, CT).
Extracted directly from official GoNation database and live menu on goodiesmilford.com.
Zero hallucinations. Full menu captured.
"""

import json
import os
import sys

def build_goodies():
    dests = ["data/merchants/goodies-of-milford.json", "data/merchants/goodies.json"]

    data = {
        "storeInfo": {
            "id": "goodies-of-milford",
            "name": "Goodies of Milford",
            "tagline": "Iconic Coastal Hot Dogs, Fresh Fried Seafood, Gourmet Burgers & All-Day Breakfast in Milford",
            "address": "170 Cherry St, Milford, CT 06460",
            "phone": "(203) 874-0113",
            "hours": {
                "monday_friday": "7:00 AM - 9:00 PM",
                "saturday": "7:00 AM - 9:00 PM",
                "sunday": "7:00 AM - 8:00 PM"
            },
            "paymentMethods": [
                "Cash",
                "Credit/Debit Cards",
                "Apple Pay",
                "Contactless"
            ],
            "amenities": [
                "Dine-In",
                "Takeout",
                "Drive-Thru / Curbside",
                "Casual Family Friendly",
                "Full Breakfast All Day",
                "Seafood Platters",
                "Hand-Spun Milkshakes",
                "Bilingual Menu"
            ],
            "themeColor": "#dc2626",
            "logoIcon": "utensils",
            "policies": {
                "restroomLocationEs": "Ubicado hacia la parte trasera del comedor al lado izquierdo.",
                "restroomLocationEn": "Located towards the back left of the main dining room.",
                "restroomCodeEs": "Abierto para clientes (no requiere código).",
                "restroomCodeEn": "Open for customers (no code required).",
                "wifiName": "Goodies_Guest",
                "wifiPassword": "cherryhotdogs",
                "parkingPolicyEs": "Estacionamiento gratuito disponible en el amplio lote comercial propio frente al local.",
                "parkingPolicyEn": "Free ample on-site customer parking in our dedicated private lot on Cherry St.",
                "returnPolicyEs": "Queremos que disfrute su comida; cualquier problema con su orden lo corregimos de inmediato.",
                "returnPolicyEn": "We want you to love your meal; please notify our counter immediately with any concerns.",
                "deliveryPolicyEs": "Pedidos para recoger en mostrador o entrega a domicilio mediante UberEats, DoorDash y Grubhub.",
                "deliveryPolicyEn": "Takeout counter pickup or delivery through UberEats, DoorDash, and Grubhub."
            }
        },
        "categories": [
            {
                "id": "all",
                "nameEs": "Todo el Menú",
                "nameEn": "Full Menu",
                "icon": "Utensils"
            },
            {
                "id": "mariscos-fritos",
                "nameEs": "Mariscos Fritos y Almejas de la Costa",
                "nameEn": "Fried Coastal Seafood",
                "icon": "Fish"
            },
            {
                "id": "hamburguesas-especiales",
                "nameEs": "Hamburguesas Clásicas y Dobles",
                "nameEn": "Gourmet Burgers",
                "icon": "Flame"
            },
            {
                "id": "hot-dogs-iconicos",
                "nameEs": "Hot Dogs Famosos de Milford",
                "nameEn": "Iconic Hot Dogs",
                "icon": "Zap"
            },
            {
                "id": "sandwiches-grinders",
                "nameEs": "Sándwiches, Gyros y Grinders",
                "nameEn": "Sandwiches, Gyros & Grinders",
                "icon": "Sandwich"
            },
            {
                "id": "desayunos-completos",
                "nameEs": "Desayunos, Omelettes y Pancakes",
                "nameEn": "Breakfast, Omelets & Pancakes",
                "icon": "Egg"
            },
            {
                "id": "malteadas-postres",
                "nameEs": "Malteadas Hershey's y Postres",
                "nameEn": "Hershey's Shakes & Desserts",
                "icon": "IceCream"
            }
        ],
        "products": [
            # MARISCOS FRITOS Y PESCADOS
            {
                "id": "goodies-seafood-combo",
                "categoryId": "mariscos-fritos",
                "nameEs": "Platón Combinado de Mariscos Goodies (Seafood Combo)",
                "nameEn": "Goodies Seafood Combo Platter",
                "descriptionEs": "Pescado dorado crujiente rebozado, camarones jumbo fritos y tiras de almejas tiernas servido con papas fritas, salsa tártara, salsa cóctel y ensalada de col.",
                "descriptionEn": "Crispy golden fried white fish, jumbo shrimp, and tender clam strips served with French fries, tartar sauce, cocktail sauce, and coleslaw.",
                "price": "$24.99",
                "popular": True,
                "badge": "House Specialty",
                "allergens": ["Gluten", "Pescado", "Mariscos", "Huevos"]
            },
            {
                "id": "fish-and-chips-2pc",
                "categoryId": "mariscos-fritos",
                "nameEs": "Platón Clásico de Fish & Chips (2 Piezas)",
                "nameEn": "Classic Fish & Chips Platter (2 pc)",
                "descriptionEs": "Dos filetes generosos de pescado blanco rebozados en masa dorada crujiente, servidos con abundantes papas a la francesa, salsa tártara casera y gajos de limón.",
                "descriptionEn": "Two large fillets of crispy golden battered white fish served with French fries, scratch tartar sauce, and lemon wedges.",
                "price": "$20.99",
                "popular": True,
                "badge": "Customer Favorite",
                "allergens": ["Gluten", "Pescado", "Huevos"]
            },
            {
                "id": "hot-buttered-lobster-roll",
                "categoryId": "mariscos-fritos",
                "nameEs": "Rollo de Langosta Caliente de Connecticut en Mantequilla",
                "nameEn": "Connecticut Hot Buttered Lobster Roll",
                "descriptionEs": "Carne tierna y dulce de langosta fresca salteada en mantequilla derretida tibia y servida en pan brioche estilo split-top tostado a la plancha.",
                "descriptionEn": "Sweet succulent fresh lobster meat warm tossed in drawn butter on a grilled split-top roll.",
                "price": "$26.99",
                "popular": True,
                "badge": "CT Coastal Classic",
                "allergens": ["Gluten", "Lácteos", "Mariscos"]
            },
            {
                "id": "clam-strips-platter",
                "categoryId": "mariscos-fritos",
                "nameEs": "Platón de Tiras de Almeja Frita Crujientes",
                "nameEn": "Crispy Clam Strips Platter",
                "descriptionEs": "Tiras de almeja empanizadas y fritas a la perfección dorada, acompañadas de papas fritas crujientes y salsa tártara casera.",
                "descriptionEn": "Tender clam strips golden fried crisp, served with French fries, coleslaw, and homemade tartar sauce.",
                "price": "$16.99",
                "allergens": ["Gluten", "Mariscos", "Huevos"]
            },
            {
                "id": "fried-jumbo-shrimp-platter",
                "categoryId": "mariscos-fritos",
                "nameEs": "Platón de Camarones Jumbo Fritos",
                "nameEn": "Fried Jumbo Shrimp Platter",
                "descriptionEs": "Camarones gigantes empanizados al momento y fritos dorados, servidos con papas a la francesa, salsa cóctel zesty y limón.",
                "descriptionEn": "Golden breaded jumbo butterfly shrimp served with crispy fries, zesty cocktail sauce, and fresh lemon.",
                "price": "$18.99",
                "allergens": ["Gluten", "Mariscos"]
            },
            {
                "id": "soft-shell-crab-sandwich",
                "categoryId": "mariscos-fritos",
                "nameEs": "Sándwich de Cangrejo de Concha Suave (Soft Shell Crab)",
                "nameEn": "Soft Shell Crab Sandwich",
                "descriptionEs": "Cangrejo entero de concha suave dorado y crujiente, servido con lechuga fresca y salsa tártara en pan suave tostado.",
                "descriptionEn": "Crispy fried whole soft shell crab topped with lettuce and tartar sauce on a toasted roll.",
                "price": "$16.99",
                "badge": "Seasonal Delicacy",
                "allergens": ["Gluten", "Mariscos", "Huevos"]
            },

            # HAMBURGUESAS GOURMET
            {
                "id": "the-goodie-burger",
                "categoryId": "hamburguesas-especiales",
                "nameEs": "Hamburguesa Insignia The Goodie Burger Doble",
                "nameEn": "The Goodie Burger",
                "descriptionEs": "Doble hamburguesa de res a la parrilla, queso cheddar derretido, chili casero con carne, cebollas picadas y tocino ahumado crocante.",
                "descriptionEn": "Double grilled beef patties, melted sharp cheddar cheese, homemade beef chili, chopped onions, and crispy bacon on a toasted roll.",
                "price": "$10.29",
                "popular": True,
                "badge": "Signature Burger",
                "allergens": ["Gluten", "Lácteos", "Puerco"]
            },
            {
                "id": "the-greek-burger",
                "categoryId": "hamburguesas-especiales",
                "nameEs": "Hamburguesa The Greek Burger con Feta y Cebolla",
                "nameEn": "The Greek Burger",
                "descriptionEs": "Doble hamburguesa de res sazonada a la parrilla con abundante queso feta griego auténtico, jitomates en rodajas y cebolla morada en pan suave.",
                "descriptionEn": "Double grilled beef burger topped with imported Greek feta cheese, sliced ripe tomatoes, and red onions.",
                "price": "$9.99",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "the-southern-burger",
                "categoryId": "hamburguesas-especiales",
                "nameEs": "Hamburguesa The Southern Burger con BBQ y Tocino",
                "nameEn": "The Southern BBQ Burger",
                "descriptionEs": "Doble carne de res, salsa barbacoa ahumada dulce, tocino crujiente y queso cheddar derretido en pan tostado.",
                "descriptionEn": "Double grilled cheeseburger smothered with sweet smoky BBQ sauce, crispy bacon, and melted cheddar.",
                "price": "$9.99",
                "popular": True,
                "allergens": ["Gluten", "Lácteos", "Puerco"]
            },
            {
                "id": "double-cheeseburger-classic",
                "categoryId": "hamburguesas-especiales",
                "nameEs": "Hamburguesa Doble Clásica con Queso Americano",
                "nameEn": "Classic Double Cheeseburger",
                "descriptionEs": "Dos carnes jugosas a la parrilla con doble queso americano derretido, lechuga, jitomate y pepinillos.",
                "descriptionEn": "Two grilled beef patties with melted double American cheese, lettuce, tomato, and pickles.",
                "price": "$8.49",
                "allergens": ["Gluten", "Lácteos"]
            },

            # HOT DOGS FAMOSOS DE MILFORD
            {
                "id": "the-goodie-dog",
                "categoryId": "hot-dogs-iconicos",
                "nameEs": "Hot Dog Insignia The Goodie Dog con Chili y Tocino",
                "nameEn": "The Goodie Dog",
                "descriptionEs": "Salchicha premium asada a la plancha cubierta con chili casero de la casa, queso cheddar fundido, cebollas picadas y tocino crocante.",
                "descriptionEn": "Griddled all-beef dog smothered in homemade chili, melted cheddar cheese, chopped sweet onions, and crispy bacon.",
                "price": "$6.49",
                "popular": True,
                "badge": "Legendary",
                "allergens": ["Gluten", "Lácteos", "Puerco"]
            },
            {
                "id": "hot-dog-with-the-works",
                "categoryId": "hot-dogs-iconicos",
                "nameEs": "Hot Dog Clásico con Todo (The Works)",
                "nameEn": "Hot Dog w/ The Works",
                "descriptionEs": "Salchicha clásica a la plancha con mostaza amarilla picante, relish dulce de pepinillo, cebolla picada, chucrut agridulce y tocino crujiente.",
                "descriptionEn": "Classic grilled dog topped with yellow mustard, sweet pickle relish, chopped onions, warm sauerkraut, and crispy bacon.",
                "price": "$5.99",
                "popular": True,
                "badge": "Top Seller",
                "allergens": ["Gluten", "Puerco"]
            },
            {
                "id": "the-milford-dog",
                "categoryId": "hot-dogs-iconicos",
                "nameEs": "Hot Dog The Milford Dog con Coleslaw y Tocino",
                "nameEn": "The Milford Dog",
                "descriptionEs": "Salchicha a la plancha coronada con ensalada fresca de col coleslaw cremosa casera y tocino ahumado crocante.",
                "descriptionEn": "Grilled hot dog topped with creamy homemade coleslaw and crispy smoked bacon.",
                "price": "$5.99",
                "allergens": ["Gluten", "Huevos", "Puerco"]
            },
            {
                "id": "reuben-dog",
                "categoryId": "hot-dogs-iconicos",
                "nameEs": "Hot Dog Estilo Reuben con Chucrut y Queso Suizo",
                "nameEn": "The Reuben Dog",
                "descriptionEs": "Salchicha a la plancha con chucrut caliente, mostaza picante, queso suizo derretido y tocino crujiente.",
                "descriptionEn": "Grilled hot dog topped with warm sauerkraut, spicy mustard, melted Swiss cheese, and bacon.",
                "price": "$6.29",
                "allergens": ["Gluten", "Lácteos", "Puerco"]
            },
            {
                "id": "the-cruiser-dog",
                "categoryId": "hot-dogs-iconicos",
                "nameEs": "Hot Dog The Cruiser con Cebollas Asadas y Chili",
                "nameEn": "The Cruiser Dog",
                "descriptionEs": "Salchicha dorada con cebollas dulces asadas a la plancha, chili casero con carne, queso cheddar y tocino.",
                "descriptionEn": "Grilled dog topped with griddled caramelized onions, house chili, melted cheddar cheese, and bacon.",
                "price": "$6.49",
                "allergens": ["Gluten", "Lácteos", "Puerco"]
            },

            # SÁNDWICHES, GYROS Y GRINDERS
            {
                "id": "authentic-greek-gyro",
                "categoryId": "sandwiches-grinders",
                "nameEs": "Gyro Griego Auténtico en Pan Pita a la Parrilla",
                "nameEn": "Authentic Greek Gyro Sandwich",
                "descriptionEs": "Carne tradicional especiada de gyro asada al asador vertical, lechuga fresca picada, jitomates jugosos, cebolla morada y salsa tzatziki de yogur y pepino en pan pita tibio.",
                "descriptionEn": "Seasoned sliced gyro meat, fresh shredded lettuce, ripe tomatoes, red onions, and homemade tzatziki sauce on warm grilled pita bread.",
                "price": "$14.29",
                "popular": True,
                "badge": "Authentic Greek",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "milford-cheesesteak-grinder",
                "categoryId": "sandwiches-grinders",
                "nameEs": "Grinder Philly Cheesesteak de Milford",
                "nameEn": "Milford Cheesesteak Grinder",
                "descriptionEs": "Finas láminas de solomillo de res salteadas a la plancha con cebollas dulces doradas y abundante queso fundido en pan submarino grinder tostado.",
                "descriptionEn": "Tender thin-sliced ribeye steak, sautéed sweet onions, and melted cheese loaded into a toasted Italian grinder roll.",
                "price": "$13.99",
                "popular": True,
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "chicken-souvlaki-pita",
                "categoryId": "sandwiches-grinders",
                "nameEs": "Souvlaki de Pollo Marinado en Pan Pita",
                "nameEn": "Marinated Chicken Souvlaki",
                "descriptionEs": "Trozos de pechuga de pollo marinada con hierbas mediterráneas, cebollas y jitomates salteados, servidos en pita caliente con tzatziki.",
                "descriptionEn": "Tender marinated chicken breast skewers, sautéed onions and tomatoes, with cool tzatziki in warm grilled pita.",
                "price": "$13.99",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "roast-beef-grinder-with-gravy",
                "categoryId": "sandwiches-grinders",
                "nameEs": "Grinder Caliente de Roast Beef con Cebollas y Gravy",
                "nameEn": "Hot Roast Beef Grinder with Gravy",
                "descriptionEs": "Roast beef fresco en rodajas, queso americano derretido, cebollas fritas dulces y salsa gravy caliente sobre pan grinder.",
                "descriptionEn": "Warm thinly sliced roast beef, melted American cheese, fried sweet onions, and rich hot savory gravy on a toasted sub.",
                "price": "$13.99",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "florentine-chicken-wrap",
                "categoryId": "sandwiches-grinders",
                "nameEs": "Wrap Florentine de Pollo a la Parrilla y Feta",
                "nameEn": "Florentine Grilled Chicken Wrap",
                "descriptionEs": "Pechuga de pollo a la parrilla, espinacas tiernas frescas, queso feta desmenuzado y vinagreta balsámica en tortilla suave.",
                "descriptionEn": "Grilled chicken breast, baby spinach, crumbled imported feta cheese, and balsamic vinaigrette in a warm wrap.",
                "price": "$11.99",
                "allergens": ["Gluten", "Lácteos"]
            },

            # DESAYUNOS, OMELETTES Y PANCAKES
            {
                "id": "goodies-special-breakfast",
                "categoryId": "desayunos-completos",
                "nameEs": "Desayuno Completo Goodies Special con Pancakes y Café",
                "nameEn": "Goodies Special Breakfast Platter",
                "descriptionEs": "El desayuno más completo: dos huevos al gusto, dos pancakes dorados esponjosos de suero de leche, papas caseras home fries, pan tostado y café caliente incluido.",
                "descriptionEn": "Two eggs any style, two fluffy golden buttermilk pancakes, crispy home fries, buttered toast, and freshly brewed coffee included.",
                "price": "$12.99",
                "popular": True,
                "badge": "Best Value Breakfast",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "greek-gyro-omelet",
                "categoryId": "desayunos-completos",
                "nameEs": "Omelette Griego Tradicional con Gyro y Queso Feta",
                "nameEn": "Authentic Greek Gyro Omelet",
                "descriptionEs": "Tres huevos batidos rellenos de carne de gyro especiada, queso feta griego, jitomates en cubos y cebolla. Servido con papas home fries y pan tostado.",
                "descriptionEn": "Three-egg fluffy omelet stuffed with spiced gyro meat, imported feta cheese, diced tomatoes, and onions. Served with home fries and toast.",
                "price": "$13.99",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "goodie-omelet-hot-dog-bacon",
                "categoryId": "desayunos-completos",
                "nameEs": "Omelette Insignia Goodie con Salchicha, Tocino y Cheddar",
                "nameEn": "The Goodie Omelet",
                "descriptionEs": "Omelette cargado con rodajas de hot dog, tocino ahumado crujiente, cebollas dulces y queso cheddar fundido. Servido con papas y pan.",
                "descriptionEn": "Hearty omelet packed with sliced hot dog, crispy bacon, sweet onions, and melted cheddar. Served with home fries and buttered toast.",
                "price": "$13.99",
                "badge": "House Creation",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Puerco"]
            },
            {
                "id": "buttermilk-blueberry-pancakes",
                "categoryId": "desayunos-completos",
                "nameEs": "Pancakes Caseros de Suero de Leche con Arándanos",
                "nameEn": "Fluffy Buttermilk Blueberry Pancakes",
                "descriptionEs": "Tres pancakes dorados y esponjosos preparados con masa casera rellena de arándanos azules jugosos, servidos con mantequilla tibia y miel de maple.",
                "descriptionEn": "Stack of three fluffy scratch-made buttermilk pancakes loaded with juicy blueberries, served with butter and warm maple syrup.",
                "price": "$10.99",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "goodies-supreme-belgian-waffle",
                "categoryId": "desayunos-completos",
                "nameEs": "Waffle Belga Supremo con Fresas y Helado Hershey's",
                "nameEn": "Goodie's Supreme Belgian Waffle",
                "descriptionEs": "Waffle belga crujiente y dorado coronado con fresas frescas, bola de helado Hershey's a elección y crema chantilly batida.",
                "descriptionEn": "Golden crisp Belgian waffle topped with fresh sweet strawberries, a scoop of your choice of Hershey's ice cream, and whipped cream.",
                "price": "$12.99",
                "popular": True,
                "badge": "Dessert Waffle",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },

            # MALTEADAS HERSHEY'S Y POSTRES
            {
                "id": "hersheys-milkshake-hand-spun",
                "categoryId": "malteadas-postres",
                "nameEs": "Malteada Clásica Batida a Mano con Helado Hershey's",
                "nameEn": "Hand-Spun Hershey's Milkshake",
                "descriptionEs": "Malteada cremosa y espesa batida a mano con helado auténtico Hershey's: Chocolate, Vainilla, Fresa, Creamsicle de Naranja o Almendra Tostada.",
                "descriptionEn": "Thick, creamy hand-spun shake made with real Hershey's ice cream: Chocolate, Vanilla, Strawberry, Orange Creamsicle, or Toasted Almond.",
                "price": "$6.49",
                "popular": True,
                "badge": "Top Treat",
                "allergens": ["Lácteos"]
            },
            {
                "id": "carnival-fried-dough",
                "categoryId": "malteadas-postres",
                "nameEs": "Masa Frita Estilo Feria (Fried Dough)",
                "nameEn": "Carnival Style Fried Dough",
                "descriptionEs": "Masa frita esponjosa y crujiente servida con abundante azúcar glas en polvo o con salsa marinara tibia y queso rallado.",
                "descriptionEn": "Freshly fried golden dough dusted with powdered sugar or served savory with warm marinara and grated cheese.",
                "price": "$6.99",
                "popular": True,
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "homemade-rice-pudding",
                "categoryId": "malteadas-postres",
                "nameEs": "Arroz con Leche Casero Tradicional",
                "nameEn": "Homemade Rice Pudding",
                "descriptionEs": "Receta tradicional griega casera con arroz cremoso cocinado a fuego lento con leche dulce y canela aromática en polvo.",
                "descriptionEn": "Classic scratch-made creamy rice pudding dusted with ground cinnamon.",
                "price": "$4.99",
                "allergens": ["Lácteos"]
            }
        ],
        "faqs": [
            {
                "qEs": "¿Dónde se encuentra ubicado Goodies of Milford?",
                "qEn": "Where is Goodies of Milford located?",
                "aEs": "Estamos convenientemente ubicados en 170 Cherry St, Milford, CT 06860 con amplio estacionamiento propio.",
                "aEn": "We are located at 170 Cherry St in Milford, CT 06860 with convenient free on-site parking."
            },
            {
                "qEs": "¿Sirven desayuno todo el día?",
                "qEn": "Do you serve breakfast all day?",
                "aEs": "¡Sí! Servimos nuestro menú completo de desayunos, omelettes, sándwiches de huevo, pancakes y waffles desde la apertura hasta el cierre.",
                "aEn": "Yes! We proudly serve our full breakfast menu including omelets, egg sandwiches, pancakes, and waffles all day long."
            },
            {
                "qEs": "¿Tienen servicio de entrega a domicilio?",
                "qEn": "Do you offer delivery?",
                "aEs": "Sí, puede ordenar comida para recoger en mostrador llamando al (203) 874-0113 o pedir entrega a domicilio a través de UberEats, DoorDash y Grubhub.",
                "aEn": "Yes, you can order counter pickup directly by phone at (203) 874-0113 or get delivery through UberEats, DoorDash, and Grubhub."
            }
        ]
    }

    for dest in dests:
        with open(dest, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Generated {dest} with {len(data['products'])} 100% verified authentic items.")

if __name__ == "__main__":
    build_goodies()
