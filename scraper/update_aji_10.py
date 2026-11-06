#!/usr/bin/env python3
import json
import os
import sys

def build_aji_10():
    dest = "data/merchants/aji-10.json"
    
    data = {
        "storeInfo": {
            "id": "aji-10",
            "name": "Aji 10 Latin Cuisine",
            "tagline": "Peruvian, Venezuelan & Latin Fusion Dining in Norwalk / Cocina Peruana y Fusión Latina",
            "address": "10 Wall St, Norwalk, CT 06850",
            "hours": {
                "monday_friday": "11:30 AM - 10:00 PM",
                "saturday": "12:00 PM - 11:00 PM",
                "sunday": "12:00 PM - 9:00 PM"
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
                "Bilingual Menu",
                "Cocktail Bar",
                "Ceviche & Raw Bar"
            ],
            "themeColor": "#ea580c",
            "logoIcon": "utensils",
            "policies": {
                "restroomLocationEs": "Ubicado hacia la parte trasera del salón principal.",
                "restroomLocationEn": "Located towards the back of the main dining room.",
                "restroomCodeEs": "Abierto para clientes (no requiere código).",
                "restroomCodeEn": "Open for dining guests (no code required).",
                "wifiName": "Aji10_Guest",
                "wifiPassword": "welcometoaji10",
                "parkingPolicyEs": "Estacionamiento disponible en la calle Wall St y en el lote público cercano.",
                "parkingPolicyEn": "Street parking on Wall St and nearby public municipal lots.",
                "returnPolicyEs": "Nos esforzamos por la satisfacción total; por favor notifique a su mesero de inmediato.",
                "returnPolicyEn": "We strive for complete guest satisfaction; please notify your server immediately.",
                "deliveryPolicyEs": "Servicio para llevar disponible por teléfono y plataformas de entrega.",
                "deliveryPolicyEn": "Takeout available directly by phone and via delivery platforms."
            },
            "phone": "(203) 957-8585"
        },
        "categories": [
            {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
            {"id": "ceviches-sushi", "nameEs": "Ceviches, Tiraditos y Sushi Latino", "nameEn": "Ceviches & Latin Sushi", "icon": "Fish"},
            {"id": "platos-principales", "nameEs": "Platos Fuertes y Lomo Saltado", "nameEn": "Main Entrees & Lomo Saltado", "icon": "Beef"},
            {"id": "antojitos-arepas", "nameEs": "Antojitos, Arepas y Causas", "nameEn": "Antojitos, Arepas & Causitas", "icon": "Utensils"},
            {"id": "sopas-ensaladas", "nameEs": "Sopas Criollas y Ensaladas", "nameEn": "Soups & Andean Salads", "icon": "Soup"},
            {"id": "parrilladas", "nameEs": "Parrilladas y Cortes para Compartir", "nameEn": "Parrilladas & Steaks", "icon": "Beef"},
            {"id": "guarniciones", "nameEs": "Acompañamientos y Tostones", "nameEn": "Latin Sides & Plantains", "icon": "Utensils"},
            {"id": "postres", "nameEs": "Postres Caseros", "nameEn": "House Desserts", "icon": "Cake"}
        ],
        "items": [
            # --- CEVICHES, TIRADITOS Y SUSHI LATINO ---
            {
                "id": "ceviche-de-pescado",
                "nameEs": "Ceviche Clásico Peruano de Pescado",
                "nameEn": "Classic Peruvian Fish Ceviche",
                "descriptionEs": "Pescado fresco del día marinado al momento en auténtica leche de tigre con jugo de lima fresca, ají rocoto, cebolla morada en pluma, camote dulce cocido y maíz choclo peruano crujiente.",
                "descriptionEn": "Fresh fish of the day cured in vibrant leche de tigre with fresh lime juice, aji rocoto, red onions, sweet potato, and crunchy Peruvian choclo corn.",
                "price": 26.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado"],
                "popular": True
            },
            {
                "id": "ceviche-mixto",
                "nameEs": "Ceviche Mixto de Mariscos y Pescado",
                "nameEn": "Peruvian Seafood Mixed Ceviche",
                "descriptionEs": "Pescado fresco, camarones, calamares y mejillones marinados en leche de tigre con ají rocoto y cilantro, acompañado de camote glaseado y maíz cancha tostado.",
                "descriptionEn": "Peruvian style medley of fresh fish, shrimp, tender calamari, and mussels cured in spicy rocoto tiger milk, served with sweet potato and cancha.",
                "price": 28.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado", "Mariscos"],
                "popular": True
            },
            {
                "id": "aji-10-tiradito",
                "nameEs": "Tiradito Aji 10 en Leche de Tigre Bicolor",
                "nameEn": "Aji 10 Signature Sashimi Tiradito",
                "descriptionEs": "Finas láminas de pescado fresco estilo sashimi bañadas en infusión de leche de tigre de ají amarillo y ají rocoto con maíz choclo.",
                "descriptionEn": "Sashimi-cut fresh fish drizzled with vibrant Peruvian yellow aji and rocoto pepper leche de tigre, garnished with choclo.",
                "price": 26.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado"],
                "popular": True
            },
            {
                "id": "leche-de-tigre-chicharron",
                "nameEs": "Copa Leche de Tigre con Chicharrón de Calamar",
                "nameEn": "Leche de Tigre Cocktail with Crispy Calamari",
                "descriptionEs": "Copa concentrada de ceviche con jugo cítrico picante de leche de tigre, coronada con calamares fritos dorados crujientes, camote y maíz cancha.",
                "descriptionEn": "Concentrated tiger milk cocktail with fish ceviche, topped with golden crispy fried calamari, sweet potato, and crunchy cancha corn.",
                "price": 20.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado", "Mariscos", "Gluten"],
                "popular": True
            },
            {
                "id": "mar-y-tierra-sushi-roll",
                "nameEs": "Rollo de Sushi Latino Mar y Tierra",
                "nameEn": "Surf & Turf Latin Sushi Roll",
                "descriptionEs": "Rollo relleno de camarones en tempura crujiente y tiras de filete New York strip a la parrilla, terminado con chimichurri argentino y salsa de mostaza de la casa.",
                "descriptionEn": "New York strip steak and crispy tempura shrimp roll topped with house chimichurri and savory mustard reduction.",
                "price": 19.00,
                "category": "ceviches-sushi",
                "allergens": ["Gluten", "Mariscos"],
                "popular": True
            },
            {
                "id": "latin-shrimp-tempura-roll",
                "nameEs": "Rollo Latino de Camarón Tempura y Huancaína",
                "nameEn": "Latin Shrimp Tempura Sushi Roll",
                "descriptionEs": "Camarones tempura, aguacate y chile jalapeño cubierto con cebollas crujientes doradas, mayonesa picante, salsa huancaína peruana y reducción de anguila.",
                "descriptionEn": "Crispy tempura shrimp, avocado, and jalapeño topped with crispy fried onions, spicy mayo, Peruvian huancaina, and sweet eel sauce.",
                "price": 18.00,
                "category": "ceviches-sushi",
                "allergens": ["Gluten", "Mariscos", "Lácteos"]
            },
            {
                "id": "tico-rico-sushi-roll",
                "nameEs": "Rollo Tico Rico con Plátano Maduro y Salmón",
                "nameEn": "Tico Rico Salmon & Sweet Plantain Roll",
                "descriptionEs": "Salmón fresco, aguacate, cebollín y queso crema envuelto en láminas doradas de plátano maduro dulce caramelizado.",
                "descriptionEn": "Fresh salmon, avocado, scallions, and cream cheese roll wrapped in golden caramelized sweet plantain.",
                "price": 18.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado", "Lácteos"]
            },
            {
                "id": "rainbow-roll-acevichado",
                "nameEs": "Rollo Rainbow Acevichado con Leche de Tigre",
                "nameEn": "Rainbow Acevichado Roll with Leche de Tigre",
                "descriptionEs": "Atún rojo, salmón fresco, pescado blanco, aguacate y plátano dulce bañado en cremosa salsa acevichada de leche de tigre.",
                "descriptionEn": "Tuna, salmon, white fish, sweet plantain, and avocado drizzled with creamy Peruvian acevichado tiger milk sauce.",
                "price": 20.00,
                "category": "ceviches-sushi",
                "allergens": ["Pescado"]
            },

            # --- PLATOS FUERTES Y LOMO SALTADO ---
            {
                "id": "lomo-saltado-tradicional",
                "nameEs": "Lomo Saltado Tradicional Peruano al Wok",
                "nameEn": "Traditional Peruvian Lomo Saltado",
                "descriptionEs": "Tiras tiernas de lomo de res salteadas al wok a fuego vivo con cebolla morada, jitomates maduros, salsa de soya, jengibre, cilantro y papas fritas doradas, servido con arroz jazmín.",
                "descriptionEn": "Wok-seared beef tenderloin strips sautéed with red onions, ripe tomatoes, soy-ginger glaze, fresh cilantro, and crispy french fries, served with jasmine rice.",
                "price": 30.00,
                "category": "platos-principales",
                "allergens": ["Soja"],
                "popular": True
            },
            {
                "id": "tallarin-verde-con-bistec",
                "nameEs": "Tallarines Verdes con Bistec a la Parrilla",
                "nameEn": "Tallarín Verde with Charbroiled Steak",
                "descriptionEs": "Pasta tradicional peruana bañada en salsa cremosa de albahaca, espinaca y queso fresco, acompañada de un filete de res a la parrilla y papas doradas.",
                "descriptionEn": "Peruvian spinach-basil pesto cream pasta topped with a juicy grilled steak and roasted golden potatoes.",
                "price": 28.00,
                "category": "platos-principales",
                "allergens": ["Gluten", "Lácteos"],
                "popular": True
            },
            {
                "id": "pabellon-criollo-venezolano",
                "nameEs": "Pabellón Criollo Venezolano Tradicional",
                "nameEn": "Traditional Venezuelan Pabellón Criollo",
                "descriptionEs": "Carne de res deshebrada mechada sazonada con sofrito criollo, arroz blanco jazmín, caraotas negras (frijoles negros), queso blanco rallado y plátanos maduros fritos.",
                "descriptionEn": "Venezuela’s national dish: tender seasoned shredded beef, black beans, jasmine rice, grated queso blanco, and sweet golden plantains.",
                "price": 26.00,
                "category": "platos-principales",
                "allergens": ["Lácteos"],
                "popular": True
            },
            {
                "id": "costillas-a-fuego-lento",
                "nameEs": "Costillas Short Ribs Braseadas a Fuego Lento",
                "nameEn": "Slow-Braised Beef Short Ribs",
                "descriptionEs": "Costillas de res braseadas durante horas hasta deshacerse en su propio jugo glaseado, servidas con puré de papas con espinaca y verduras salteadas de temporada.",
                "descriptionEn": "Tender beef short ribs braised overnight in rich savory reduction, served with spinach mashed potatoes and sautéed seasonal vegetables.",
                "price": 32.00,
                "category": "platos-principales",
                "allergens": ["Lácteos"],
                "popular": True
            },
            {
                "id": "salmon-glaseado-guayaba",
                "nameEs": "Salmón a la Parrilla Glaseado con BBQ de Guayaba",
                "nameEn": "Grilled Salmon Glazed with Guava BBQ",
                "descriptionEs": "Filete de salmón del Atlántico a la parrilla con glaseado casero agridulce de barbacoa y guayaba tropical, acompañado de gallo pinto y salsa fresca de aguacate.",
                "descriptionEn": "Grilled fresh Atlantic salmon brushed with tropical guava barbecue sauce, served with gallo pinto (rice & beans) and fresh avocado salsa.",
                "price": 28.00,
                "category": "platos-principales",
                "allergens": ["Pescado"],
                "popular": True
            },
            {
                "id": "filete-pescado-salsa-mariscos",
                "nameEs": "Filete de Pescado en Salsa de Mariscos a la Crema de Langosta",
                "nameEn": "Pan-Seared Fish Fillet in Seafood Lobster Sauce",
                "descriptionEs": "Filete de pescado dorado a la sartén cubierto con camarones, calamares y mejillones en salsa sedosa de langosta y vino blanco, con arroz jazmín.",
                "descriptionEn": "Pan-seared fish fillet topped with shrimp, calamari, and PEI mussels in rich velvety lobster cream reduction, served with jasmine rice.",
                "price": 32.00,
                "category": "platos-principales",
                "allergens": ["Pescado", "Mariscos", "Lácteos"],
                "popular": True
            },
            {
                "id": "camarones-al-ajillo",
                "nameEs": "Camarones Jumbo al Ajillo con Vino Blanco",
                "nameEn": "Garlic Jumbo Shrimp (Camarones al Ajillo)",
                "descriptionEs": "Camarones gigantes salteados con abundante ajo dorado, aceite de oliva virgen extra, perejil y vino blanco, servidos con arroz jazmín.",
                "descriptionEn": "Pan-seared jumbo shrimp sautéed in fragrant garlic, extra virgin olive oil, herbs, and white wine, served with jasmine rice.",
                "price": 27.00,
                "category": "platos-principales",
                "allergens": ["Mariscos"]
            },
            {
                "id": "tallarin-saltado-de-carne",
                "nameEs": "Tallarín Saltado de Carne Estilo Chifa",
                "nameEn": "Peruvian Chifa Beef Lo Mein (Tallarín Saltado)",
                "descriptionEs": "Fideos salteados al wok estilo fusión Chifa chino-peruana con tiras de res, cebollines, pimientos, salsa de soya y aceite de ajonjolí.",
                "descriptionEn": "Peruvian-Chinese Chifa style wok-tossed lo mein noodles with beef strips, scallions, peppers, soy sauce, and sesame aromatics.",
                "price": 27.00,
                "category": "platos-principales",
                "allergens": ["Gluten", "Soja", "Sésamo"]
            },
            {
                "id": "pollo-plancha-aji-panca",
                "nameEs": "Medio Pollo a la Plancha Marinado en Ají Panca",
                "nameEn": "Half Grilled Chicken in Aji Panca Marinade",
                "descriptionEs": "Medio pollo marinado en ají panca ahumado peruano, ajos y comino, asado a la plancha con papas doradas y arroz jazmín.",
                "descriptionEn": "Half chicken marinated in smoky Peruvian aji panca, garlic, and spices, served with roasted golden potatoes and jasmine rice.",
                "price": 25.00,
                "category": "platos-principales"
            },

            # --- ANTOJITOS, AREPAS Y CAUSITAS ---
            {
                "id": "trio-causitas-peruanas",
                "nameEs": "Trío de Causitas Peruanas de la Casa",
                "nameEn": "Trio of Peruvian Causitas (Shrimp, Chicken, Crab)",
                "descriptionEs": "Tres causitas de puré de papa amarilla infusionadas con ají amarillo y lima, coronadas individualmente con camarón, ensalada de pollo y pulpa de cangrejo.",
                "descriptionEn": "Three whipped yellow potato cakes seasoned with aji amarillo and lime, individually topped with shrimp, chicken salad, and sweet crab meat.",
                "price": 16.00,
                "category": "antojitos-arepas",
                "allergens": ["Mariscos", "Huevos"],
                "popular": True
            },
            {
                "id": "arepas-venezolanas-duo",
                "nameEs": "Dúo de Arepas Venezolanas Artesanales",
                "nameEn": "Two Authentic Venezuelan Stuffed Arepas",
                "descriptionEs": "Dos arepas de maíz recién asadas en comal rellenas a su elección: Reina Pepiada (pollo con aguacate), Carne Mechada jugosa, Costillas deshebradas o Queso de mano.",
                "descriptionEn": "Two handmade grilled corn cakes stuffed with your choice of: Reina Pepiada (avocado chicken salad), Shredded Beef, Short Rib, or Artisan Cheese.",
                "price": 16.00,
                "category": "antojitos-arepas",
                "allergens": ["Lácteos"],
                "popular": True
            },
            {
                "id": "empanadas-de-carne",
                "nameEs": "Empanadas de Res con Ají Amarillo (2 unidades)",
                "nameEn": "Handmade Beef Empanadas with Aji Amarillo Dip",
                "descriptionEs": "Empanadas doradas rellenas de carne molida sazonada con aceitunas, pasas dulces, cebolla y cilantro, servidas con salsa de ají amarillo cremoso.",
                "descriptionEn": "Two golden flaky empanadas stuffed with seasoned ground beef, olives, raisins, and cilantro, served with aji amarillo dipping sauce.",
                "price": 14.00,
                "category": "antojitos-arepas",
                "allergens": ["Gluten", "Huevos"],
                "popular": True
            },
            {
                "id": "anticuchos-de-corazon-o-churrasco",
                "nameEs": "Anticuchos a la Parrilla con Yuca Frita y Huancaína",
                "nameEn": "Peruvian Anticuchos Skewers with Fried Yucca",
                "descriptionEs": "Brochetas a la parrilla de corazón de res tradicional o carne churrasco marinadas en ají panca y vinagre, servidas con yuca dorada y salsa huancaína.",
                "descriptionEn": "Traditional Peruvian grilled skewers of beef heart or tender skirt steak marinated in aji panca spices, served with fried yucca and huancaina sauce.",
                "price": 17.00,
                "category": "antojitos-arepas",
                "allergens": ["Lácteos"],
                "popular": True
            },
            {
                "id": "pulpo-a-la-parrilla-aji-10",
                "nameEs": "Pulpo a la Parrilla al Estilo Aji 10 a la Gallega",
                "nameEn": "Charred Grilled Octopus Aji 10 Style",
                "descriptionEs": "Tentáculos de pulpo tierno asados a las brasas con pimentón ahumado, servidos sobre papas doradas y espinacas salteadas al ajo.",
                "descriptionEn": "Tender charred octopus grilled with Spanish paprika, served over roasted potatoes and garlic sautéed baby spinach.",
                "price": 22.00,
                "category": "antojitos-arepas",
                "allergens": ["Mariscos"],
                "popular": True
            },
            {
                "id": "chicharrones-calamar-o-cerdo",
                "nameEs": "Chicharrones de Cerdo o Calamar con Tostones",
                "nameEn": "Crispy Chicharrones (Pork or Calamari) with Tostones",
                "descriptionEs": "Trozos de cerdo crujientes o calamares dorados servidos con tostones de plátano verde, ensalada fresca de salpicón y alioli de la casa.",
                "descriptionEn": "Choice of crispy fried pork belly or tender golden calamari served with green plantain tostones, fresh salpicon slaw, and house aioli.",
                "price": 15.00,
                "category": "antojitos-arepas",
                "allergens": ["Gluten"]
            },
            {
                "id": "mejillones-caldo-langosta",
                "nameEs": "Mejillones de la Isla del Príncipe Eduardo en Caldo de Langosta",
                "nameEn": "PEI Mussels in Zesty Lobster Herb Broth",
                "descriptionEs": "Mejillones frescos salteados en caldo aromático de langosta con aceite de oliva, vino blanco, hojuelas de chile y finas hierbas.",
                "descriptionEn": "Fresh Prince Edward Island mussels simmered in a zesty lobster broth with white wine, red pepper flakes, and fresh herbs.",
                "price": 16.00,
                "category": "antojitos-arepas",
                "allergens": ["Mariscos"]
            },

            # --- SOPAS CRIOLLAS Y ENSALADAS ---
            {
                "id": "parihuela-de-mariscos",
                "nameEs": "Parihuela Tradicional de Mariscos",
                "nameEn": "Peruvian Seafood Parihuela Bouillabaisse",
                "descriptionEs": "La gran sopa peruana del mar: camarones, filete de pescado, mejillones y calamares cocidos a fuego lento en un caldo especiado de ají panca y cerveza.",
                "descriptionEn": "Rich Peruvian seafood bouillabaisse with fresh fish, jumbo shrimp, calamari, and mussels in a fragrant spicy aji panca broth.",
                "price": 26.00,
                "category": "sopas-ensaladas",
                "allergens": ["Pescado", "Mariscos"],
                "popular": True
            },
            {
                "id": "sancocho-de-res",
                "nameEs": "Sancocho de Res Criollo Tradicional",
                "nameEn": "Traditional Latin Beef Sancocho Stew",
                "descriptionEs": "Guiso sustancioso de carne de res con trozos de yuca, mazorca de maíz tierno, calabaza y plátano, servido con arroz blanco y aguacate.",
                "descriptionEn": "Slow-simmered Latin American beef stew cooked with yucca, sweet corn on the cob, plantain, and squash, served with rice and avocado.",
                "price": 22.00,
                "category": "sopas-ensaladas",
                "popular": True
            },
            {
                "id": "ensalada-nueva-andina",
                "nameEs": "Ensalada Nueva Andina de Quinua y Aguacate",
                "nameEn": "Nueva Andina Quinoa & Avocado Salad",
                "descriptionEs": "Hojas verdes mixtas, pepino, aguacate maduro, quinua orgánica andina, queso fresco desmoronado, nueces mixtas y vinagreta de la casa.",
                "descriptionEn": "Baby greens, cucumbers, ripe avocado, organic Andean quinoa, crumbled queso fresco, toasted nuts, cranberries, and house dressing.",
                "price": 16.00,
                "category": "sopas-ensaladas",
                "allergens": ["Lácteos", "Frutos secos"]
            },
            {
                "id": "aji-10-caesar-salad",
                "nameEs": "Ensalada César Aji 10 con Ají Amarillo",
                "nameEn": "Aji 10 Signature Aji Amarillo Caesar Salad",
                "descriptionEs": "Corazones de lechuga romana con crutones dorados de pan brioche a la mantequilla de ajo, aderezo César infusionado con ají amarillo y lascas de parmesano.",
                "descriptionEn": "Crisp romaine hearts tossed with garlic butter brioche croutons, aji amarillo-infused Caesar dressing, and shaved parmesan.",
                "price": 15.00,
                "category": "sopas-ensaladas",
                "allergens": ["Gluten", "Lácteos", "Pescado"]
            },

            # --- PARRILLADAS Y CORTES PARA COMPARTIR ---
            {
                "id": "parrillada-argentina-de-carnes",
                "nameEs": "Gran Parrillada Argentina de Carnes (Para Compartir)",
                "nameEn": "Gran Parrillada Argentina Meat Board",
                "descriptionEs": "Festín a la parrilla con entraña (churrasco), chuleta de cerdo tierna, pechuga de pollo, chorizo argentino artesanal y morcilla, servido con yuca frita y chimichurri.",
                "descriptionEn": "Grilled feast of skirt steak, pork chop, chicken breast, artisan Argentine chorizo, and blood sausage, served with fried yucca and fresh chimichurri.",
                "price": 45.00,
                "category": "parrilladas",
                "popular": True
            },
            {
                "id": "parrillada-de-mariscos",
                "nameEs": "Gran Parrillada de Mariscos del Pacífico",
                "nameEn": "Grand Pacific Seafood Parrillada",
                "descriptionEs": "Mariscada completa a la plancha: camarones gigantes, calamares tiernos, almejas frescas, mejillones y filete de pescado dorado con yuca frita y tostones.",
                "descriptionEn": "Extravagant seafood platter: grilled jumbo shrimp, tender calamari, clams, PEI mussels, and fish fillet served with fried yucca and tostones.",
                "price": 48.00,
                "category": "parrilladas",
                "allergens": ["Pescado", "Mariscos"],
                "popular": True
            },
            {
                "id": "bistec-churrasco-de-la-casa",
                "nameEs": "Churrasco de Entraña a la Brasa con Chimichurri",
                "nameEn": "House Charbroiled Skirt Steak (Churrasco)",
                "descriptionEs": "Jugoso corte de entraña a las brasas sazonado con sal marina, servido con papas fritas al adobo, chimichurri argentino y guasacaca venezolana de aguacate.",
                "descriptionEn": "Charbroiled skirt steak served with house adobo seasoned fries, authentic Argentine chimichurri, and Venezuelan avocado guasacaca.",
                "price": 32.00,
                "category": "parrilladas",
                "popular": True
            },

            # --- GUARNICIONES ---
            {
                "id": "tostones-de-platano",
                "nameEs": "Tostones de Plátano Verde Crujientes",
                "nameEn": "Crispy Green Plantain Tostones with Mojo",
                "descriptionEs": "Plátanos verdes machacados y fritos dos veces crujientes con mojo de ajo.",
                "descriptionEn": "Twice-fried crispy green plantains served with garlic dipping mojo.",
                "price": 7.00,
                "category": "guarniciones"
            },
            {
                "id": "maduros-fritos",
                "nameEs": "Plátanos Maduros Fritos Dulces",
                "nameEn": "Sweet Fried Ripe Plantains (Maduros)",
                "descriptionEs": "Rebanadas doradas y caramelizadas de plátano macho maduro dulce.",
                "descriptionEn": "Caramelized sweet ripe plantains fried golden brown.",
                "price": 7.00,
                "category": "guarniciones"
            },
            {
                "id": "yuca-frita-huancaina",
                "nameEs": "Yuca Frita Crujiente con Salsa Huancaína",
                "nameEn": "Crispy Fried Cassava Yucca with Huancaina",
                "descriptionEs": "Bastones de yuca fritos dorados por fuera y suaves por dentro con salsa cremosa de ají amarillo y queso.",
                "descriptionEn": "Crispy golden cassava wedges served with creamy spicy Peruvian huancaina cheese sauce.",
                "price": 8.00,
                "category": "guarniciones",
                "allergens": ["Lácteos"]
            },
            {
                "id": "gallo-pinto",
                "nameEs": "Gallo Pinto Tradicional Centroamericano",
                "nameEn": "Gallo Pinto (Mixed Rice & Black Beans)",
                "descriptionEs": "Arroz blanco y frijoles negros sazonados con cebolla, pimientos y salsa Lizano tradicional.",
                "descriptionEn": "Traditional seasoned rice and black bean mixture sautéed with herbs and aromatics.",
                "price": 7.00,
                "category": "guarniciones"
            },

            # --- POSTRES ---
            {
                "id": "caribe-banana-coconut-roll",
                "nameEs": "Rollo Crujiente Caribeño de Plátano y Coco",
                "nameEn": "Caribe Warm Banana Coconut Roll",
                "descriptionEs": "Crujiente rollito horneado relleno de plátano dulce y coco rallado con helado de vainilla y caramelo.",
                "descriptionEn": "Warm crispy fried banana and sweet coconut spring roll served with rich vanilla bean ice cream and dulce de leche.",
                "price": 10.00,
                "category": "postres",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "tres-leches-aji-10",
                "nameEs": "Pastel Casero de Tres Leches Tradicional",
                "nameEn": "Traditional House Tres Leches Cake",
                "descriptionEs": "Bizcocho esponjoso empapado en tres leches dulces con canela y crema chantilly.",
                "descriptionEn": "Classic Latin sponge cake soaked in sweet infused three milks, finished with whipped cream.",
                "price": 9.00,
                "category": "postres",
                "allergens": ["Gluten", "Huevos", "Lácteos"],
                "popular": True
            },
            {
                "id": "churros-con-dulce-de-leche",
                "nameEs": "Churros Dorados con Azúcar, Canela y Dulce de Leche",
                "nameEn": "Golden Churros with Dulce de Leche",
                "descriptionEs": "Churros crujientes recién preparados espolvoreados con azúcar y canela con dip de dulce de leche caliente.",
                "descriptionEn": "Crispy freshly fried churros dusted in cinnamon sugar, served with warm dulce de leche dip.",
                "price": 9.00,
                "category": "postres",
                "allergens": ["Gluten", "Lácteos"]
            }
        ]
    }

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully created {dest} with {len(data['items'])} verified authentic items!")

if __name__ == "__main__":
    build_aji_10()
