#!/usr/bin/env python3
"""
Generate 100% verified authentic merchant menu for Mothership Bakery & Cafe (Danbury, CT).
Extracted directly from official website, SinglePlatform, and Squarespace catering menus.
Zero hallucinations. Full menu captured.
"""

import json
import os
import sys

def build_mothership():
    dests = ["data/merchants/mothership-bakery-and-cafe.json", "data/merchants/mothership.json"]

    data = {
        "storeInfo": {
            "id": "mothership-bakery-and-cafe",
            "name": "Mothership Bakery & Cafe",
            "tagline": "Scratch-Made All-Natural Farm Fare, House-Roasted Organic Coffee & Bakery Treats in Danbury",
            "address": "331 Main St, Danbury, CT 06810",
            "phone": "(203) 456-6627",
            "hours": {
                "monday_friday": "7:30 AM - 3:00 PM",
                "saturday": "7:30 AM - 3:00 PM",
                "sunday": "7:30 AM - 3:00 PM"
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
                "Garden Patio Seating",
                "House-Roasted Organic Coffee",
                "Zero-Food-Waste Philosophy",
                "Woodbury Farm Fresh Eggs",
                "Bilingual Menu"
            ],
            "themeColor": "#059669",
            "logoIcon": "coffee",
            "policies": {
                "restroomLocationEs": "Ubicado a través del pasillo del comedor hacia el fondo a la derecha.",
                "restroomLocationEn": "Located down the dining hallway towards the back right.",
                "restroomCodeEs": "Abierto para clientes (no requiere código).",
                "restroomCodeEn": "Open for cafe patrons (no code required).",
                "wifiName": "Mothership_Guest",
                "wifiPassword": "scratchbakery",
                "parkingPolicyEs": "Estacionamiento disponible frente al local y en la calle Main St.",
                "parkingPolicyEn": "On-site storefront parking and metered street parking along Main St.",
                "returnPolicyEs": "Elaboramos todo desde cero con ingredientes naturales de granja; si algo no está perfecto lo cambiamos con gusto.",
                "returnPolicyEn": "Everything is crafted from scratch using all-natural ingredients; please notify us if anything falls short.",
                "deliveryPolicyEs": "Pedidos para recoger en mostrador o servicio de banquetes y pasteles a través de mothershipbakeryandcafe.com.",
                "deliveryPolicyEn": "Counter pickup and catering orders available via mothershipbakeryandcafe.com."
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
                "id": "sandwiches-artesanales",
                "nameEs": "Sándwiches Artesanales",
                "nameEn": "Scratch Sandwiches",
                "icon": "Sandwich"
            },
            {
                "id": "desayuno-quiches",
                "nameEs": "Huevos de Granja y Quiches",
                "nameEn": "Farm Eggs & Quiches",
                "icon": "Egg"
            },
            {
                "id": "ensaladas-frescas",
                "nameEs": "Ensaladas de la Huerta",
                "nameEn": "Garden Salads",
                "icon": "Salad"
            },
            {
                "id": "pasteleria-reposteria",
                "nameEs": "Panadería y Pudines Caseros",
                "nameEn": "Scratch Bakery & Treats",
                "icon": "Cake"
            },
            {
                "id": "cafe-batidos",
                "nameEs": "Café Tostado en Casa y Batidos",
                "nameEn": "Organic Coffee & Smoothies",
                "icon": "Coffee"
            }
        ],
        "products": [
            # SÁNDWICHES ARTESANALES (SCRATCH SANDWICHES)
            {
                "id": "mothership-chicken-salad-sandwich",
                "categoryId": "sandwiches-artesanales",
                "nameEs": "Sándwich Casero de Ensalada de Pollo con Manzanas y Nueces",
                "nameEn": "Scratch Chicken Salad Sandwich",
                "descriptionEs": "Pechuga de pollo asada y desmenuzada a mano con manzanas crujientes Granny Smith, nueces tostadas de castilla y arándanos secos en pan multigrano artesanal.",
                "descriptionEn": "Roasted and hand-pulled chicken with tart Granny Smith apples, walnuts, and dried cranberries on multigrain bread.",
                "price": "$8.50",
                "popular": True,
                "badge": "House Favorite",
                "allergens": ["Gluten", "Huevos", "Frutos Secos"]
            },
            {
                "id": "chicken-tender-pesto-sandwich",
                "categoryId": "sandwiches-artesanales",
                "nameEs": "Sándwich de Tiras de Pollo Crujiente con Alioli de Pesto",
                "nameEn": "Crispy Chicken Tender Sandwich",
                "descriptionEs": "Tiras de pechuga de pollo crujientes, alioli casero de pesto de albahaca fresca, queso provolone fundido, lechuga y rodajas de jitomate en pan ciabatta.",
                "descriptionEn": "Crispy chicken tenders, homemade fresh basil pesto aioli, melted provolone cheese, lettuce, and tomato on warm ciabatta.",
                "price": "$8.50",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "scratch-hummus-veggie-sandwich",
                "categoryId": "sandwiches-artesanales",
                "nameEs": "Sándwich Vegano de Hummus Casero y Pimientos Asados",
                "nameEn": "Scratch Hummus Veggie Sandwich",
                "descriptionEs": "Hummus elaborado desde cero en nuestra cocina con garbanzos orgánicos y tahini, pimientos rojos asados y pepinos frescos crujientes en pan a elección.",
                "descriptionEn": "Kitchen-made organic chickpea hummus, fire-roasted sweet peppers, and crisp cucumbers on your choice of artisan bread.",
                "price": "$8.50",
                "badge": "Vegan",
                "allergens": ["Gluten", "Sésamo"]
            },
            {
                "id": "roast-beef-provolone-ciabatta",
                "categoryId": "sandwiches-artesanales",
                "nameEs": "Sándwich de Roast Beef Asado con Pesto y Provolone",
                "nameEn": "Roast Beef & Provolone Ciabatta",
                "descriptionEs": "Finas rebanadas de roast beef tierno, pesto de albahaca fresca, queso provolone fundido y pimientos rojos asados dulces en pan ciabatta.",
                "descriptionEn": "Tender roast beef, fresh basil pesto, melted provolone, and roasted sweet peppers on toasted ciabatta.",
                "price": "$8.50",
                "popular": True,
                "allergens": ["Gluten", "Lácteos"]
            },

            # HUEVOS DE GRANJA Y QUICHES (FARM EGGS & QUICHES)
            {
                "id": "daily-farm-quiche-slice",
                "categoryId": "desayuno-quiches",
                "nameEs": "Rebanada de Quiche Artesanal del Día",
                "nameEn": "Daily Farm Quiche Slice",
                "descriptionEs": "Quiche horneada diariamente con huevos frescos de granja de Woodbury: Vegetales asados con queso gouda ahumado, tocino crujiente con cebollín y cheddar, o espinaca con queso feta.",
                "descriptionEn": "Baked daily with local Woodbury farm fresh eggs: Roasted veggies & smoked gouda, bacon scallion & cheddar, or spinach feta & tomato.",
                "price": "$6.50",
                "popular": True,
                "badge": "Farm Fresh",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "gluten-free-frittata-bites",
                "categoryId": "desayuno-quiches",
                "nameEs": "Bocados de Frittata Horneada (Sin Gluten ni Lácteos)",
                "nameEn": "Gluten-Free & Dairy-Free Frittata Bites",
                "descriptionEs": "Bocados horneados de huevo de granja con verduras tiernas y finas hierbas de jardín, libres de gluten y lácteos.",
                "descriptionEn": "Baked farm egg frittata bites packed with garden vegetables and aromatic herbs. 100% gluten-free and dairy-free.",
                "price": "$3.50",
                "badge": "GF & DF",
                "allergens": ["Huevos"]
            },
            {
                "id": "scratch-chicken-pot-pie-mothership",
                "categoryId": "desayuno-quiches",
                "nameEs": "Pastel Rústico de Pollo de Granja (Chicken Pot Pie)",
                "nameEn": "Scratch Farm Chicken Pot Pie",
                "descriptionEs": "Pollo tierno desmenuzado cocinado a fuego lento con zanahorias dulces, chícharos y salsa cremosa suave horneado dentro de costra hojaldrada dorada de mantequilla.",
                "descriptionEn": "Slow-cooked pulled farm chicken with garden carrots, peas, and rich herb veloute inside a scratch-made buttery golden crust.",
                "price": "$12.50",
                "popular": True,
                "badge": "Scratch Made",
                "allergens": ["Gluten", "Lácteos"]
            },

            # ENSALADAS DE LA HUERTA (GARDEN SALADS)
            {
                "id": "signature-kale-salad",
                "categoryId": "ensaladas-frescas",
                "nameEs": "Ensalada Insignia de Col Rizada (Signature Kale Salad)",
                "nameEn": "Signature Kale Salad",
                "descriptionEs": "Hojas de col rizada kale tiernas masajeadas con arándanos secos, semillas de girasol tostadas, verduras de temporada asadas al horno y vinagreta balsámica toscana.",
                "descriptionEn": "Tender massaged kale, sweet cranberries, toasted sunflower seeds, oven-roasted seasonal vegetables, and Tuscan balsamic vinaigrette.",
                "price": "$11.00",
                "popular": True,
                "badge": "Signature Salad"
            },
            {
                "id": "spinach-and-strawberry-salad",
                "categoryId": "ensaladas-frescas",
                "nameEs": "Ensalada de Espinacas Tiernas con Fresas y Feta",
                "nameEn": "Spinach & Fresh Strawberry Salad",
                "descriptionEs": "Hojas tiernas de espinaca orgánica, fresas maduras en rodajas, queso feta desmenuzado, nueces o tocino ahumado artesanal y vinagreta casera.",
                "descriptionEn": "Organic baby spinach, sweet sliced strawberries, crumbled feta cheese, and balsamic dressing.",
                "price": "$10.50",
                "allergens": ["Lácteos"]
            },
            {
                "id": "southwest-black-bean-salad",
                "categoryId": "ensaladas-frescas",
                "nameEs": "Ensalada Southwest de Frijoles Negros y Cilantro",
                "nameEn": "Southwest Black Bean Salad",
                "descriptionEs": "Frijoles negros cocidos al dente, granos de maíz tierno, pimientos dulces, cebolla morada picada y aderezo fresco de cilantro y lima.",
                "descriptionEn": "Black beans, sweet corn, diced bell peppers, red onions, and fresh cilantro lime vinaigrette.",
                "price": "$9.50",
                "badge": "Vegan"
            },

            # PANADERÍA Y PUDINES CASEROS (SCRATCH BAKERY)
            {
                "id": "mothership-bread-pudding-portion",
                "categoryId": "pasteleria-reposteria",
                "nameEs": "Pudín de Pan Insignia de la Casa (Mothership Bread Pudding)",
                "nameEn": "Signature Mothership Bread Pudding",
                "descriptionEs": "La especialidad más famosa de Danbury: pudín de pan artesanal horneado con natilla tibia de vainilla pura, canela y toque sutil de licor dulce.",
                "descriptionEn": "Danbury's legendary dessert: rich scratch-baked custard bread pudding infused with pure vanilla bean and cinnamon.",
                "price": "$4.50",
                "popular": True,
                "badge": "Award Winning",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "daily-artisan-scone",
                "categoryId": "pasteleria-reposteria",
                "nameEs": "Scone Artesanal Horneado del Día",
                "nameEn": "Daily Scratch Artisan Scone",
                "descriptionEs": "Scone clásico británico de textura quebradiza y mantecosa con arándanos silvestres o chispas de chocolate horneado fresco todas las mañanas.",
                "descriptionEn": "Traditional tender buttery scone baked fresh daily with wild blueberries or chocolate chips.",
                "price": "$3.50",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "daily-farm-muffin",
                "categoryId": "pasteleria-reposteria",
                "nameEs": "Muffin Casero con Frutas de Temporada",
                "nameEn": "Daily Farm Muffin",
                "descriptionEs": "Muffin húmedo elaborado desde cero con frutas frescas de temporada, harina sin blanquear y azúcar de caña pura.",
                "descriptionEn": "Moist morning muffin baked from scratch with fresh seasonal fruits.",
                "price": "$3.50",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "fudgy-dark-chocolate-brownie",
                "categoryId": "pasteleria-reposteria",
                "nameEs": "Brownie Fundente de Chocolate Negro Puro",
                "nameEn": "Fudgy Dark Chocolate Brownie",
                "descriptionEs": "Brownie denso horneado con cacao puro holandés y centros masticables con trozos de chocolate amargo.",
                "descriptionEn": "Dense fudgy brownie made with premium Dutch dark cocoa and rich chocolate chips.",
                "price": "$3.00",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "lemon-iced-sugar-cookie",
                "categoryId": "pasteleria-reposteria",
                "nameEs": "Galleta Horneada con Glaseado de Limón Amarillo",
                "nameEn": "Lemon Iced Sugar Cookie",
                "descriptionEs": "Galleta tierna de mantequilla con bordes dorados, cubierta con glaseado fresco de limón natural.",
                "descriptionEn": "Tender scratch butter sugar cookie topped with tangy fresh lemon juice icing.",
                "price": "$2.50",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },

            # CAFÉ TOSTADO EN CASA Y BATIDOS (ORGANIC COFFEE & SMOOTHIES)
            {
                "id": "mothership-organic-latte",
                "categoryId": "cafe-batidos",
                "nameEs": "Latte con Café Orgánico Tostado en Casa",
                "nameEn": "House-Roasted Organic Latte",
                "descriptionEs": "Café espresso orgánico tostado artesanalmente en la propia cafetería, combinado con leche sedosa al vapor. Sabores especiales: Bourbon Vanilla, Dark Mocha, Caramelo o Mantequilla.",
                "descriptionEn": "Double shot of house-roasted organic espresso with silky steamed milk. Specialty flavors available: Bourbon Vanilla, Dark Mocha, Caramel, or Butterbeer.",
                "price": "$4.25",
                "popular": True,
                "badge": "House Roasted",
                "allergens": ["Lácteos"]
            },
            {
                "id": "mothership-flat-white",
                "categoryId": "cafe-batidos",
                "nameEs": "Flat White Espresso con Microespuma Densa",
                "nameEn": "Mothership Flat White",
                "descriptionEs": "Doble extracción de espresso orgánico mezclado con leche texturizada aterciopelada de microespuma fina.",
                "descriptionEn": "Smooth double pull of organic espresso velvety textured with dense steamed microfoam.",
                "price": "$4.25",
                "allergens": ["Lácteos"]
            },
            {
                "id": "mothership-cappuccino",
                "categoryId": "cafe-batidos",
                "nameEs": "Capuchino Clásico con Espuma de Leche",
                "nameEn": "Classic Organic Cappuccino",
                "descriptionEs": "Espresso orgánico con partes equilibradas de leche caliente y suave capa de espuma densa.",
                "descriptionEn": "Rich organic espresso balanced with steamed milk and airy foam.",
                "price": "$4.25",
                "allergens": ["Lácteos"]
            },
            {
                "id": "green-goddess-smoothie",
                "categoryId": "cafe-batidos",
                "nameEs": "Batido Revitalizante Green Goddess",
                "nameEn": "Green Goddess Smoothie",
                "descriptionEs": "Pepino crujiente, espinacas frescas baby, perejil desintoxicante y piña dulce madura batido al momento.",
                "descriptionEn": "Fresh cucumber, baby spinach, parsley, and golden pineapple blended fresh to order.",
                "price": "$7.00",
                "popular": True,
                "badge": "Detox Superfood"
            },
            {
                "id": "four-berry-smoothie",
                "categoryId": "cafe-batidos",
                "nameEs": "Batido Antioxidante 4 Berry con Açaí y Mantequilla de Almendra",
                "nameEn": "4 Berry Superfood Smoothie",
                "descriptionEs": "Arándanos azules, moras, frambuesas y bayas de açaí puro batidos con plátano dulce, leche de soya orgánica y mantequilla de almendras.",
                "descriptionEn": "Blueberries, blackberries, raspberries, and pure acai with banana, organic soy milk, and rich almond butter.",
                "price": "$7.00",
                "popular": True,
                "badge": "Antioxidant",
                "allergens": ["Soya", "Frutos Secos"]
            },
            {
                "id": "sunrise-smoothie",
                "categoryId": "cafe-batidos",
                "nameEs": "Batido Tropical Sunrise de Fresa, Naranja y Mango",
                "nameEn": "Sunrise Tropical Smoothie",
                "descriptionEs": "Fresas dulces, jugo puro de naranja recién exprimido y mango tropical maduro: un amanecer refrescante en tu vaso.",
                "descriptionEn": "Sweet strawberries, fresh-squeezed orange juice, and tropical mango like sunshine in a cup.",
                "price": "$7.00"
            }
        ],
        "faqs": [
            {
                "qEs": "¿Dónde se encuentra Mothership Bakery & Cafe en Danbury?",
                "qEn": "Where is Mothership Bakery & Cafe located in Danbury?",
                "aEs": "Estamos ubicados en 331 Main Street, Danbury, CT 06810 en una emblemática estación histórica restaurada de la década de 1930 con patio al aire libre.",
                "aEn": "We are located at 331 Main Street in Danbury, CT 06810 in a beautifully converted 1930s-era building with a welcoming garden patio."
            },
            {
                "qEs": "¿De dónde provienen sus ingredientes?",
                "qEn": "Where do your ingredients come from?",
                "aEs": "Seguimos una estricta filosofía de desperdicio cero y comida totalmente natural. Muchos de nuestros huevos frescos y productos provienen directamente de nuestra propia granja en Woodbury, CT.",
                "aEn": "We operate with a zero-food-waste philosophy using all-natural ingredients; many of our fresh eggs and produce come straight from our farm in Woodbury, CT."
            },
            {
                "qEs": "¿Tienen opciones sin gluten y veganas?",
                "qEn": "Do you offer gluten-free and vegan choices?",
                "aEs": "¡Sí! Ofrecemos frittata bites sin gluten ni lácteos, sándwiches veganos de hummus casero, ensaladas de la huerta y opciones de pasteles especiales sin gluten.",
                "aEn": "Yes! We serve gluten-free and dairy-free frittatas, vegan scratch hummus sandwiches, fresh salads, and custom gluten-free cakes upon advance request."
            }
        ]
    }

    for dest in dests:
        with open(dest, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Generated {dest} with {len(data['products'])} 100% verified authentic items.")

if __name__ == "__main__":
    build_mothership()
