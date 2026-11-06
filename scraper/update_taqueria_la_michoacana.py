#!/usr/bin/env python3
import json
import os
import sys

def build_michoacana():
    dest = "data/merchants/taqueria-la-michoacana.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update store info with exact street address
    data["storeInfo"]["address"] = "1914 Main St, Bridgeport, CT 06604"
    data["storeInfo"]["tagline"] = "Auténtica Cocina Tradicional Mexicana en Bridgeport / Authentic Traditional Mexican Cuisine"

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
        {"id": "breakfast", "nameEs": "Desayunos Mexicanos", "nameEn": "Mexican Breakfast", "icon": "Egg"},
        {"id": "sopas-caldos", "nameEs": "Sopas y Caldos Tradicionales", "nameEn": "Traditional Soups & Caldos", "icon": "Soup"},
        {"id": "tacos", "nameEs": "Tacos Auténticos", "nameEn": "Authentic Street Tacos", "icon": "Utensils"},
        {"id": "tortas", "nameEs": "Tortas Mexicanas", "nameEn": "Mexican Tortas", "icon": "Sandwich"},
        {"id": "burritos-quesadillas", "nameEs": "Burritos y Quesadillas", "nameEn": "Burritos & Quesadillas", "icon": "Utensils"},
        {"id": "antojitos-sopes", "nameEs": "Sopes, Huaraches y Flautas", "nameEn": "Sopes, Huaraches & Antojitos", "icon": "Utensils"},
        {"id": "postres-bebidas", "nameEs": "Aguas Frescas y Postres", "nameEn": "Aguas Frescas & Desserts", "icon": "Coffee"}
    ]

    items = [
        # --- DESAYUNOS ---
        {
            "id": "huevos-estrellados",
            "nameEs": "Huevos Estrellados Tradicionales",
            "nameEn": "Traditional Huevos Estrellados",
            "descriptionEs": "Dos huevos fritos tiernos servidos con crema, queso fresco, frijoles refritos y 3 tortillas de maíz hechas a mano.",
            "descriptionEn": "Two eggs over easy topped with crema and queso fresco, served with refried beans and 3 handmade corn tortillas.",
            "price": 9.50,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "huevos-con-chorizo",
            "nameEs": "Huevos Revueltos con Chorizo",
            "nameEn": "Scrambled Eggs with Mexican Chorizo",
            "descriptionEs": "Huevos revueltos con chorizo mexicano artesanal sazonado, frijoles refritos y 3 tortillas de maíz calientitas hechas a mano.",
            "descriptionEn": "Scrambled eggs mixed with seasoned Mexican pork sausage, served with savory refried beans and 3 handmade corn tortillas.",
            "price": 12.00,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "huevos-a-la-mexicana",
            "nameEs": "Huevos a la Mexicana",
            "nameEn": "Huevos a la Mexicana",
            "descriptionEs": "Huevos revueltos con jitomate picado, cebolla y chile jalapeño fresco. Acompañados de frijoles refritos y 3 tortillas de maíz hechas a mano.",
            "descriptionEn": "Scrambled eggs with diced ripe tomato, onions, and fresh jalapeño peppers. Served with refried beans and 3 handmade corn tortillas.",
            "price": 11.00,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos"]
        },
        {
            "id": "huevos-con-jamon",
            "nameEs": "Huevos con Jamón",
            "nameEn": "Scrambled Eggs with Ham",
            "descriptionEs": "Huevos revueltos preparados con jamón picado, frijoles refritos tradicionales y 3 tortillas de maíz hechas a mano.",
            "descriptionEn": "Fluffy scrambled eggs cooked with diced ham, served with traditional refried beans and 3 handmade corn tortillas.",
            "price": 11.00,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos"]
        },
        {
            "id": "quesadilla-de-huevo",
            "nameEs": "Quesadilla de Huevo",
            "nameEn": "Scrambled Egg Breakfast Quesadilla",
            "descriptionEs": "Tortilla doblada rellena de huevo revuelto y queso derretido fundido, servida doradita en comal.",
            "descriptionEn": "Griddled tortilla folded with fluffy scrambled eggs and melted Mexican cheese.",
            "price": 8.00,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos", "Gluten"]
        },
        {
            "id": "chilaquiles-con-huevos",
            "nameEs": "Chilaquiles con Huevos (Salsa Verde o Roja)",
            "nameEn": "Chilaquiles with Eggs (Red or Green Salsa)",
            "descriptionEs": "Totopos de maíz crujientes bañados en salsa verde o roja casera, queso cotija desmoronado, crema fresca, huevos al gusto y frijoles refritos.",
            "descriptionEn": "Crispy corn tortilla chips simmered in house-made red or green salsa, topped with crumbled cotija cheese, crema, eggs, and refried beans.",
            "price": 15.00,
            "category": "breakfast",
            "allergens": ["Huevos", "Lácteos"],
            "popular": True
        },

        # --- SOPAS Y CALDOS ---
        {
            "id": "pozole-con-tostadas",
            "nameEs": "Pozole Rojo Tradicional con 3 Tostadas",
            "nameEn": "Traditional Red Pozole with 3 Tostadas",
            "descriptionEs": "Caldo tradicional mexicano de maíz cacahuazintle con trozos tiernos de carne de cerdo en caldo especiado de chiles secos. Servido con lechuga, rábanos, orégano, limón y 3 tostadas de maíz.",
            "descriptionEn": "Authentic Mexican hominy stew simmered with tender pork in an aromatic red chili broth. Served with shredded cabbage, radishes, lime, oregano, and 3 crispy corn tostadas.",
            "price": 19.00,
            "category": "sopas-caldos",
            "popular": True
        },
        {
            "id": "menudo-de-pancita",
            "nameEs": "Menudo de Pancita con Tortillas Hechas a Mano",
            "nameEn": "Traditional Beef Tripe Menudo with Handmade Tortillas",
            "descriptionEs": "Reconfortante caldo de pancita de res cocida lentamente en caldo de chile guajillo aromático con hierbabuena. Servido con cebolla picada, orégano, chile piquín, limón y tortillas hechas a mano.",
            "descriptionEn": "Comforting slow-simmered beef tripe soup in a rich guajillo chili broth. Served with diced onions, oregano, lime wedges, and warm handmade corn tortillas.",
            "price": 19.00,
            "category": "sopas-caldos",
            "popular": True
        },

        # --- TACOS ---
        {
            "id": "tacos-quesabirria",
            "nameEs": "Quesabirrias con Consomé (Orden de 3)",
            "nameEn": "Quesabirria Tacos with Consomé (Order of 3)",
            "descriptionEs": "Tres tortillas de maíz doraditas en comal con grasa de birria, rellenas de birria de res deshebrada ultra tierna y queso Oaxaca derretido. Acompañadas de cilantro, cebolla y taza de consomé caliente para chopear.",
            "descriptionEn": "Three crispy griddled corn tortillas stuffed with melt-in-your-mouth slow-braised beef birria and melted Oaxaca cheese. Served with cilantro, onions, lime, and rich hot consommé for dipping.",
            "price": 19.99,
            "category": "tacos",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "tacos-carne-asada",
            "nameEs": "Tacos de Carne Asada (Orden de 3)",
            "nameEn": "Carne Asada Tacos (Order of 3)",
            "descriptionEs": "Tres tortillas de maíz hechas a mano con bistec de res picado a la plancha, cebolla picada, cilantro fresco y gajos de limón.",
            "descriptionEn": "Three handmade corn tortillas filled with chopped grilled marinated steak, diced onions, fresh cilantro, and lime wedges.",
            "price": 16.00,
            "category": "tacos",
            "popular": True
        },
        {
            "id": "tacos-al-pastor",
            "nameEs": "Tacos al Pastor (Orden de 3)",
            "nameEn": "Al Pastor Tacos (Order of 3)",
            "descriptionEs": "Tres tortillas de maíz con carne de cerdo marinada en achiote y especias tradicionales, trocitos de piña asada, cebolla y cilantro.",
            "descriptionEn": "Three handmade corn tortillas filled with citrus-adobo marinated roasted pork, grilled pineapple chunks, onions, and cilantro.",
            "price": 16.00,
            "category": "tacos",
            "popular": True
        },
        {
            "id": "tacos-carnitas",
            "nameEs": "Tacos de Carnitas Estilo Michoacán (Orden de 3)",
            "nameEn": "Michoacán Style Carnitas Tacos (Order of 3)",
            "descriptionEs": "La especialidad de la casa: carnitas de cerdo cocidas a fuego lento doraditas por fuera y jugosas por dentro, cilantro, cebolla y limón.",
            "descriptionEn": "House specialty: authentic Michoacán-style slow-braised pork, golden crisp outside and juicy tender inside, topped with onions and cilantro.",
            "price": 16.00,
            "category": "tacos",
            "popular": True
        },
        {
            "id": "tacos-de-pollo",
            "nameEs": "Tacos de Pollo Asado (Orden de 3)",
            "nameEn": "Grilled Chicken Tacos (Order of 3)",
            "descriptionEs": "Tres tacos de pechuga de pollo deshebrada sazonada con hierbas mexicanas, cebolla fresca, cilantro y limón.",
            "descriptionEn": "Three handmade corn tortillas loaded with seasoned shredded chicken breast, fresh cilantro, onions, and lime.",
            "price": 16.00,
            "category": "tacos"
        },
        {
            "id": "tacos-de-lengua",
            "nameEs": "Tacos de Lengua de Res (Orden de 3)",
            "nameEn": "Braised Beef Tongue Tacos (Order of 3)",
            "descriptionEs": "Tres tacos de lengua de res cocida a fuego lento hasta quedar suave y tierna, servida con cilantro fresco, cebolla y salsas artesanales.",
            "descriptionEn": "Three handmade corn tortillas loaded with tender braised beef tongue, cilantro, onions, and fresh salsas.",
            "price": 25.00,
            "category": "tacos",
            "popular": True
        },
        {
            "id": "tacos-de-cabeza",
            "nameEs": "Tacos de Cabeza de Res (Orden de 3)",
            "nameEn": "Steamed Beef Cabeza Tacos (Order of 3)",
            "descriptionEs": "Carne de cabeza de res al vapor extraordinariamente jugosa y suave, servida sobre tortillas calientes con cilantro y cebolla.",
            "descriptionEn": "Three corn tortillas with succulent, ultra-tender steamed beef head meat, onions, and fresh cilantro.",
            "price": 16.00,
            "category": "tacos"
        },
        {
            "id": "tacos-de-chorizo",
            "nameEs": "Tacos de Chorizo Mexicano (Orden de 3)",
            "nameEn": "Mexican Chorizo Tacos (Order of 3)",
            "descriptionEs": "Chorizo de cerdo mexicano especiado dorado a la plancha, cebolla picada y cilantro en tortillas de maíz recién hechas.",
            "descriptionEn": "Three corn tortillas filled with flavorful spiced Mexican pork sausage, onions, cilantro, and fresh lime.",
            "price": 16.00,
            "category": "tacos"
        },

        # --- TORTAS ---
        {
            "id": "torta-cubana",
            "nameEs": "Torta Cubana Gigante",
            "nameEn": "Giant Mexican Torta Cubana",
            "descriptionEs": "Pan telera doradito untado con frijoles y mayonesa, milanesa de carne empanizada, jamón, salchicha, huevo, queso derretido, aguacate, jitomate y jalapeños.",
            "descriptionEn": "Colossal Mexican sandwich on toasted telera bread layered with breaded cutlet steak, sliced ham, hot dog sausage, egg, melted cheese, avocado, beans, tomato, and jalapeños.",
            "price": 16.00,
            "category": "tortas",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "torta-carne-asada",
            "nameEs": "Torta de Carne Asada",
            "nameEn": "Carne Asada Torta",
            "descriptionEs": "Pan telera tostado con bistec de res a la parrilla, frijoles refritos, rebanadas de aguacate fresco, jitomate, lechuga, cebolla y mayonesa.",
            "descriptionEn": "Toasted Mexican telera roll loaded with grilled steak, refried beans, fresh avocado slices, tomato, lettuce, onions, and mayo.",
            "price": 15.00,
            "category": "tortas",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "torta-al-pastor",
            "nameEs": "Torta al Pastor con Piña",
            "nameEn": "Al Pastor Torta with Pineapple",
            "descriptionEs": "Pan telera relleno de carne de cerdo al pastor marinada, trozos de piña dulce asada, frijoles, aguacate, queso y crema.",
            "descriptionEn": "Toasted telera filled with marinated al pastor pork, grilled pineapple, beans, avocado, melted cheese, and crema.",
            "price": 15.00,
            "category": "tortas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "torta-carnitas",
            "nameEs": "Torta de Carnitas Michoacanas",
            "nameEn": "Michoacán Carnitas Torta",
            "descriptionEs": "Deliciosas carnitas de cerdo tiernas sobre pan telera con frijoles refritos, aguacate, cebolla morada curtida, jitomate y mayonesa.",
            "descriptionEn": "Juicy slow-cooked carnitas on toasted telera roll with refried beans, avocado, pickled onions, tomato, and mayo.",
            "price": 15.00,
            "category": "tortas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "torta-milanesa-pollo",
            "nameEs": "Torta de Milanesa de Pollo",
            "nameEn": "Breaded Chicken Milanesa Torta",
            "descriptionEs": "Pechuga de pollo empanizada y dorada crujiente en pan telera con aguacate, jitomate, frijoles refritos, queso fresco y rajas de jalapeño.",
            "descriptionEn": "Crispy golden breaded chicken breast on toasted telera with sliced avocado, tomato, refried beans, queso fresco, and pickled jalapeños.",
            "price": 15.00,
            "category": "tortas",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "torta-milanesa-res",
            "nameEs": "Torta de Milanesa de Res",
            "nameEn": "Breaded Beef Milanesa Torta",
            "descriptionEs": "Fina milanesa de res empanizada artesanalmente, servida con frijoles, aguacate cremoso, lechuga, jitomate y queso fundido.",
            "descriptionEn": "Thinly pounded breaded beef cutlet fried crispy on telera bread with refried beans, creamy avocado, lettuce, tomato, and melted cheese.",
            "price": 16.00,
            "category": "tortas",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },

        # --- BURRITOS Y QUESADILLAS ---
        {
            "id": "quesadilla-la-michoacana",
            "nameEs": "Quesadilla Gigante a la Michoacana",
            "nameEn": "Quesadilla a la Michoacana",
            "descriptionEs": "Enorme quesadilla hecha a mano rellena con queso derretido y su elección de carne (Asada, Pastor o Pollo), acompañada de lechuga, queso cotija, crema y salsas.",
            "descriptionEn": "Large signature quesadilla loaded with melted cheese and your choice of grilled meat (Asada, Pastor, or Chicken), served with lettuce, cotija cheese, crema, and salsa.",
            "price": 19.00,
            "category": "burritos-quesadillas",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "burrito-carne-asada",
            "nameEs": "Burrito de Carne Asada",
            "nameEn": "Carne Asada Burrito",
            "descriptionEs": "Gran tortilla de harina rellena de bistec de res a la plancha, arroz mexicano sazonado, frijoles refritos, queso fundido, crema agria y pico de gallo.",
            "descriptionEn": "Large flour tortilla packed with grilled steak, seasoned Mexican rice, refried beans, melted cheese, sour cream, and fresh pico de gallo.",
            "price": 15.00,
            "category": "burritos-quesadillas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "burrito-al-pastor",
            "nameEs": "Burrito al Pastor",
            "nameEn": "Al Pastor Pork Burrito",
            "descriptionEs": "Tortilla de harina con carne de cerdo al pastor, piña dulce, arroz mexicano, frijoles, queso derretido y crema.",
            "descriptionEn": "Flour tortilla rolled with marinated al pastor pork, grilled pineapple, Mexican rice, refried beans, melted cheese, and crema.",
            "price": 15.00,
            "category": "burritos-quesadillas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "burrito-de-pollo",
            "nameEs": "Burrito de Pollo",
            "nameEn": "Seasoned Chicken Burrito",
            "descriptionEs": "Pechuga de pollo deshebrada con arroz mexicano, frijoles, queso monterrey fundido, lechuga y crema.",
            "descriptionEn": "Tender seasoned chicken breast rolled with Mexican rice, beans, melted cheese, lettuce, and sour cream.",
            "price": 14.50,
            "category": "burritos-quesadillas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "burrito-de-carnitas",
            "nameEs": "Burrito de Carnitas",
            "nameEn": "Michoacán Carnitas Burrito",
            "descriptionEs": "Carnitas tiernas de cerdo Michoacán enrolladas con arroz, frijoles, queso derretido, pico de gallo y crema agria.",
            "descriptionEn": "Slow-cooked carnitas rolled with rice, beans, melted cheese, fresh pico de gallo, and cool sour cream.",
            "price": 15.00,
            "category": "burritos-quesadillas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "burrito-vegetariano",
            "nameEs": "Burrito Vegetariano con Aguacate",
            "nameEn": "Vegetarian Avocado Burrito",
            "descriptionEs": "Pimientos salteados, cebollas caramelizadas, arroz, frijoles, abundante aguacate fresco, queso y crema.",
            "descriptionEn": "Sauteed peppers and onions, Mexican rice, beans, fresh avocado slices, melted cheese, and crema.",
            "price": 13.50,
            "category": "burritos-quesadillas",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- ANTOJITOS, SOPES Y FLAUTAS ---
        {
            "id": "sopes-orden-3",
            "nameEs": "Sopes Tradicionales (Orden de 3)",
            "nameEn": "Traditional Sopes (Order of 3)",
            "descriptionEs": "Tres bases gruesas de masa de maíz con bordes pellizcados fritas al momento, untadas con frijoles refritos y carne al gusto (Asada, Carnitas o Pastor), lechuga, queso cotija y crema.",
            "descriptionEn": "Three handmade thick pinched corn masa cakes fried golden, topped with refried beans, choice of meat (Asada, Carnitas, Pastor), crisp lettuce, cotija cheese, and crema.",
            "price": 15.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "huarache-con-carne",
            "nameEs": "Huarache Tradicional con Carne",
            "nameEn": "Traditional Huarache with Meat",
            "descriptionEs": "Gran base ovalada de masa de maíz rellena de frijoles molidos, dorada en comal con su carne favorita (Asada, Carnitas o Pastor), salsa verde o roja, cebolla picada, queso fresco y crema.",
            "descriptionEn": "Large oblong corn masa cake stuffed with refried beans, griddled with your choice of meat, green or red salsa, chopped onions, queso fresco, and sour cream.",
            "price": 16.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "flautas-doradas-pollo",
            "nameEs": "Flautas Doradas de Pollo (5 piezas)",
            "nameEn": "Crispy Chicken Flautas (5 pcs)",
            "descriptionEs": "Cinco taquitos de maíz enrollados rellenos de pechuga de pollo deshebrada, fritos doraditos y cubiertos con lechuga fresca, jitomate, aguacate, queso cotija y crema agria.",
            "descriptionEn": "Five crispy rolled corn taquitos stuffed with seasoned shredded chicken, topped with shredded lettuce, tomato, avocado slices, crumbled cotija cheese, and sour cream.",
            "price": 16.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "tostadas-de-tinga",
            "nameEs": "Tostadas de Tinga de Pollo (Orden de 3)",
            "nameEn": "Chicken Tinga Tostadas (Order of 3)",
            "descriptionEs": "Tres tostadas planas crujientes untadas con frijoles refritos, pechuga de pollo deshebrada en salsa de jitomate y chipotle, lechuga, crema agria y queso cotija.",
            "descriptionEn": "Three crispy fried flat corn tortillas topped with refried beans, shredded chicken tinga in chipotle-tomato sauce, lettuce, crema, and cotija cheese.",
            "price": 15.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"]
        },
        {
            "id": "guacamole-casero-totopos",
            "nameEs": "Guacamole Casero con Totopos",
            "nameEn": "Fresh Homemade Guacamole & Chips",
            "descriptionEs": "Aguacate maduro machacado al momento con jugo de lima, cilantro fresco picado, jitomate, cebolla y totopos de maíz dorados.",
            "descriptionEn": "Freshly mashed ripe avocados with lime juice, chopped cilantro, diced tomatoes, onions, and crispy tortilla chips.",
            "price": 9.00,
            "category": "antojitos-sopes",
            "popular": True
        },
        {
            "id": "ensalada-verde",
            "nameEs": "Ensalada Verde de la Casa",
            "nameEn": "House Fresh Green Salad",
            "descriptionEs": "Lechuga romana crujiente, cebolla morada, jitomate, rábanos rebanados, aguacate fresco y queso blanco desmoronado.",
            "descriptionEn": "Crisp romaine lettuce, red onion, ripe tomatoes, sliced radishes, fresh avocado, and crumbled queso blanco.",
            "price": 8.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"]
        },
        {
            "id": "ensalada-pollo-asado",
            "nameEs": "Ensalada con Pechuga de Pollo Asado",
            "nameEn": "Grilled Chicken Salad",
            "descriptionEs": "Ensalada verde abundante con tiras de pechuga de pollo marinada a la parrilla, aguacate, queso y vinagreta cítrica de la casa.",
            "descriptionEn": "Large green salad topped with seasoned grilled chicken breast strips, avocado, cheese, and citrus vinaigrette.",
            "price": 13.00,
            "category": "antojitos-sopes",
            "allergens": ["Lácteos"]
        },

        # --- POSTRES Y BEBIDAS ---
        {
            "id": "pastel-tres-leches",
            "nameEs": "Pastel Tradicional de Tres Leches",
            "nameEn": "Traditional Tres Leches Cake",
            "descriptionEs": "Bizcocho suave y esponjoso empapado en infusión de tres leches dulces, coronado con crema chantilly y cereza.",
            "descriptionEn": "Traditional authentic Mexican sponge cake soaked in three sweet milks, finished with whipped cream and a cherry.",
            "price": 5.00,
            "category": "postres-bebidas",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "flan-casero",
            "nameEs": "Flan Casero Napolitano",
            "nameEn": "Homemade Caramel Flan",
            "descriptionEs": "Flan tradicional cremoso de vainilla horneado a baño maría con caramelo líquido dorado.",
            "descriptionEn": "Traditional Mexican rich vanilla custard baked with golden amber caramel sauce.",
            "price": 5.00,
            "category": "postres-bebidas",
            "allergens": ["Huevos", "Lácteos"]
        },
        {
            "id": "churros-con-canela",
            "nameEs": "Churros con Azúcar y Canela (4 piezas)",
            "nameEn": "Cinnamon Sugar Churros (4 pcs)",
            "descriptionEs": "Churros crujientes recién fritos espolvoreados con azúcar y canela, acompañados de salsa dulce de cajeta o chocolate.",
            "descriptionEn": "Four freshly fried crispy Mexican churros dusted with cinnamon sugar, served with dulce de leche or chocolate dip.",
            "price": 6.00,
            "category": "postres-bebidas",
            "allergens": ["Gluten"]
        },
        {
            "id": "agua-fresca-horchata",
            "nameEs": "Agua Fresca de Horchata Casera (24oz)",
            "nameEn": "Homemade Horchata Agua Fresca (24oz)",
            "descriptionEs": "Bebida tradicional artesanal de arroz, canela molida, vainilla y leche servida bien fría con hielo.",
            "descriptionEn": "Traditional refreshing house-made Mexican rice milk drink infused with sweet cinnamon and vanilla over ice.",
            "price": 5.00,
            "category": "postres-bebidas",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "agua-fresca-jamaica",
            "nameEs": "Agua Fresca de Jamaica (24oz)",
            "nameEn": "Hibiscus Agua Fresca (24oz)",
            "descriptionEs": "Infusión natural de flor de jamaica mexicana, ligeramente endulzada, refrescante y digestiva con hielo.",
            "descriptionEn": "Refreshing all-natural steeped hibiscus flower iced tea, crisp and lightly sweetened over ice.",
            "price": 5.00,
            "category": "postres-bebidas",
            "popular": True
        },
        {
            "id": "agua-fresca-tamarindo",
            "nameEs": "Agua Fresca de Tamarindo Natural (24oz)",
            "nameEn": "Natural Tamarind Agua Fresca (24oz)",
            "descriptionEs": "Bebida tradicional mexicana elaborada con pulpa de tamarindo natural con un toque agridulce perfecto.",
            "descriptionEn": "Traditional sweet-and-sour agua fresca made with real strained tamarind pulp over ice.",
            "price": 5.00,
            "category": "postres-bebidas"
        },
        {
            "id": "coca-cola-mexicana",
            "nameEs": "Coca-Cola Mexicana de Vidrio (500ml)",
            "nameEn": "Mexican Coke in Glass Bottle (500ml)",
            "descriptionEs": "Auténtica Coca-Cola mexicana elaborada con azúcar de caña pura en botella de vidrio de medio litro.",
            "descriptionEn": "Authentic Mexican Coca-Cola sweetened with pure cane sugar in a 500ml glass bottle.",
            "price": 3.75,
            "category": "postres-bebidas",
            "popular": True
        },
        {
            "id": "jarritos-mexicanos",
            "nameEs": "Refresco Jarritos Surtido (Botella)",
            "nameEn": "Assorted Jarritos Mexican Soda",
            "descriptionEs": "Refrescos mexicanos en botella de vidrio: Mandarina, Tamarindo, Toronja, Piña o Ponche de Frutas.",
            "descriptionEn": "Classic fruit-flavored Mexican soda in glass bottle: Mandarin, Tamarind, Grapefruit, Pineapple, or Fruit Punch.",
            "price": 3.50,
            "category": "postres-bebidas"
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(items)} verified items to {dest}!")

if __name__ == "__main__":
    build_michoacana()
