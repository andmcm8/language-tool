#!/usr/bin/env python3
import json
import os
import sys

def build_bodega():
    dest = "data/merchants/bodega-taco-bar.json"
    
    data = {
        "storeInfo": {
            "id": "bodega-taco-bar",
            "name": "Bodega Taco Bar",
            "tagline": "Modern Mexican Street Food, Handcrafted Tacos & Tequila Bar in Fairfield",
            "address": "1700 Post Rd, Fairfield, CT 06824",
            "hours": {
                "monday_thursday": "11:30 AM - 9:30 PM",
                "friday_saturday": "11:30 AM - 10:30 PM",
                "sunday": "11:30 AM - 9:00 PM"
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
                "Outdoor Patio",
                "Full Tequila & Cocktail Bar",
                "Bilingual Menu",
                "Taco Tuesday Specials"
            ],
            "themeColor": "#ea580c",
            "logoIcon": "utensils",
            "policies": {
                "restroomLocationEs": "Los baños se encuentran en el pasillo lateral derecho del restaurante.",
                "restroomLocationEn": "Restrooms are located down the right hallway of the restaurant.",
                "restroomCodeEs": "Abierto para clientes (no requiere código).",
                "restroomCodeEn": "Open for dining guests (no code required).",
                "wifiName": "Bodega_Guest",
                "wifiPassword": "tacosandtequila",
                "parkingPolicyEs": "Estacionamiento disponible en la plaza comercial y en la calle Post Rd.",
                "parkingPolicyEn": "Parking available in the shopping center lot and along Post Rd.",
                "returnPolicyEs": "Nos enorgullecemos de la calidad de nuestra comida; notifique al gerente si algo no está a su gusto.",
                "returnPolicyEn": "We pride ourselves on fresh quality; please inform a manager immediately if not fully satisfied.",
                "deliveryPolicyEs": "Pedidos para llevar y entrega disponibles a través de Toast Online y plataformas asociadas.",
                "deliveryPolicyEn": "Takeout and delivery available directly via Toast Online ordering."
            },
            "phone": "(203) 292-9590"
        },
        "categories": [
            {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
            {"id": "guacamole-antojitos", "nameEs": "Guacamoles y Antojitos", "nameEn": "Guacamole & Antojitos", "icon": "Sparkles"},
            {"id": "tacos", "nameEs": "Tacos Hechos a Mano", "nameEn": "Handcrafted Tacos", "icon": "Utensils"},
            {"id": "birria-oaxaca", "nameEs": "Birria y Tacos Callejeros Oaxaca", "nameEn": "Birria & Oaxaca Street Tacos", "icon": "Flame"},
            {"id": "platos", "nameEs": "Platos Principales y Fajitas", "nameEn": "Principal Plates & Fajitas", "icon": "Beef"},
            {"id": "burritos-bowls", "nameEs": "Burritos, Bowls y Quesadillas", "nameEn": "Burritos, Bowls & Quesadillas", "icon": "Utensils"},
            {"id": "ensaladas-sopas", "nameEs": "Ensaladas y Sopas", "nameEn": "Salads & Soups", "icon": "Soup"},
            {"id": "sides-postres", "nameEs": "Acompañamientos y Postres", "nameEn": "Sides & Desserts", "icon": "Cake"},
            {"id": "bebidas-margaritas", "nameEs": "Margaritas y Bebidas", "nameEn": "Margaritas & Refreshers", "icon": "Coffee"}
        ],
        "items": [
            # --- GUACAMOLE & ANTOJITOS ---
            {
                "id": "bodega-original-guacamole",
                "nameEs": "Guacamole Original Bodega",
                "nameEn": "Bodega Original Guacamole",
                "descriptionEs": "Aguacates frescos machacados al momento a mano con tomate, jalapeño, cebolla, cilantro, Tabasco verde, sal de mar y jugo de lima recién exprimido. Servido con totopos de maíz crujientes.",
                "descriptionEn": "Slapped to order fresh avocado, diced tomato, jalapeño, onion, cilantro, green tabasco, sea salt, and fresh lime juice. Served with warm house tortilla chips.",
                "price": 12.50,
                "category": "guacamole-antojitos",
                "badge": "Popular",
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan"]
            },
            {
                "id": "double-original-guac",
                "nameEs": "Guacamole Original Doble",
                "nameEn": "DOUBLE Original Guac",
                "descriptionEs": "Porción doble grande de nuestro guacamole fresco preparado a mano con totopos adicionales.",
                "descriptionEn": "Extra-large double portion of our freshly slapped-to-order house guacamole with plenty of warm tortilla chips.",
                "price": 18.00,
                "category": "guacamole-antojitos",
                "badge": "Para Compartir",
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan"]
            },
            {
                "id": "orange-habanero-guac",
                "nameEs": "Guacamole Habanero y Naranja",
                "nameEn": "Orange Habanero Guacamole",
                "descriptionEs": "Nuestro guacamole insignia enriquecido con un toque cítrico de naranja fresca y chile habanero asado para los amantes del picante.",
                "descriptionEn": "House guacamole spiked with fresh orange zest and fire-roasted habanero chiles for an exhilarating citrus kick.",
                "price": 13.50,
                "category": "guacamole-antojitos",
                "badge": "Picante",
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan", "Spicy"]
            },
            {
                "id": "bodega-chips-pico",
                "nameEs": "Totopos con Pico de Gallo Casero",
                "nameEn": "Bodega Chips & House Pico",
                "descriptionEs": "Totopos de maíz crujientes acompañados de nuestro pico de gallo tradicional con tomate roma, cebolla picada, cilantro y chile serrano.",
                "descriptionEn": "Crispy corn tortilla chips paired with freshly made pico de gallo with diced Roma tomatoes, onion, cilantro, and serrano pepper.",
                "price": 8.00,
                "category": "guacamole-antojitos",
                "badge": None,
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan"]
            },
            {
                "id": "guac-pico-combo",
                "nameEs": "Combo Guacamole y Pico de Gallo",
                "nameEn": "Guac & Pico Combo",
                "descriptionEs": "La combinación perfecta de guacamole original Bodega y pico de gallo fresco servido con canasta de totopos.",
                "descriptionEn": "The ultimate starter pairing: freshly mashed original guacamole and zesty house pico de gallo served with warm tortilla chips.",
                "price": 14.50,
                "category": "guacamole-antojitos",
                "badge": "Favorito",
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan"]
            },
            {
                "id": "ceviche-tiradito",
                "nameEs": "Ceviche Tiradito de Hamachi",
                "nameEn": "Hamachi Ceviche Tiradito",
                "descriptionEs": "Hamachi fresco en corte fino, marinado en jugo cítrico de mango y habanero con aguacate, láminas de serrano, cebolla morada y chips de plátano macho.",
                "descriptionEn": "Fresh hamachi yellowtail, mango habanero citrus marinade, sliced avocado, serrano chiles, red onion, and crispy plantain chips.",
                "price": 16.00,
                "category": "guacamole-antojitos",
                "badge": "Chef Pick",
                "allergens": ["Fish", "Gluten-Free"]
            },
            {
                "id": "queso-fundido",
                "nameEs": "Queso Fundido Tradicional",
                "nameEn": "Queso Fundido",
                "descriptionEs": "Mezcla de quesos mexicanos derretidos y burbujeantes servido con tortillas de harina recién calientes.",
                "descriptionEn": "Gooey molten Mexican cheese fusion served bubbling hot with warm flour tortillas.",
                "price": 12.00,
                "category": "guacamole-antojitos",
                "badge": None,
                "allergens": ["Dairy", "Gluten"]
            },
            {
                "id": "sweet-chili-duck-nachos",
                "nameEs": "Nachos de Carnitas de Pato Sweet Chili",
                "nameEn": "Sweet Chili Duck Nachos",
                "descriptionEs": "Totopos de maíz coronados con carnitas de pato deshebradas, queso cotija y salsa dulce y picante de arándanos con jalapeño.",
                "descriptionEn": "Tender shredded duck carnitas, melted cheese, crumbled cotija, and sweet-tart cranberry-jalapeño salsa over crispy chips.",
                "price": 16.00,
                "category": "guacamole-antojitos",
                "badge": "Signature",
                "allergens": ["Dairy", "Gluten-Free"]
            },
            {
                "id": "pork-belly-arepa",
                "nameEs": "Arepa de Panceta Glaseada",
                "nameEn": "Pork Belly Arepa",
                "descriptionEs": "Arepa tierna de maíz hecha en casa rellena de panceta de cerdo glaseada con salsa hoisin y cebollín verde fresco.",
                "descriptionEn": "Fresh griddled corn cake topped with hoisin glazed pork belly and sliced green scallions.",
                "price": 10.00,
                "category": "guacamole-antojitos",
                "badge": None,
                "allergens": ["Pork", "Gluten-Free"]
            },
            {
                "id": "tuna-tostada",
                "nameEs": "Tostada Crujiente de Atún Fresco",
                "nameEn": "Tuna Tostada",
                "descriptionEs": "Tártaro de atún de grado sushi sobre tostada de maíz crujiente con puré de aguacate, alioli de chipotle y hojas de cilantro crujiente.",
                "descriptionEn": "Fresh sushi-grade tuna tartare, mashed avocado, smoky chipotle aioli, and crispy flash-fried cilantro on a crunchy corn tostada.",
                "price": 15.00,
                "category": "guacamole-antojitos",
                "badge": "Mariscos",
                "allergens": ["Fish", "Eggs", "Gluten-Free"]
            },
            {
                "id": "street-corn-elote",
                "nameEs": "Elote Callejero Desgranado",
                "nameEn": "Street Corn Elote",
                "descriptionEs": "Maíz dulce asado a la parrilla desgranado, mezclado con queso cotija, chile piquín en polvo y alioli cítrico de la casa.",
                "descriptionEn": "Grilled corn off the cob tossed with creamy cotija cheese, chili powder blend, and zesty citrus aioli.",
                "price": 8.00,
                "category": "guacamole-antojitos",
                "badge": "Favorito",
                "allergens": ["Dairy", "Eggs", "Vegetarian", "Gluten-Free"]
            },
            {
                "id": "blistered-brussels-sprouts",
                "nameEs": "Coles de Bruselas Glaseadas al Habanero",
                "nameEn": "Bodega Blistered Brussels Sprouts",
                "descriptionEs": "Coles de Bruselas tostadas al fuego con glaseado agridulce de agave y chile habanero.",
                "descriptionEn": "Fire-blistered Brussels sprouts glazed in sweet agave nectar and fiery habanero reduction.",
                "price": 10.00,
                "category": "guacamole-antojitos",
                "badge": None,
                "allergens": ["Vegetarian", "Vegan", "Gluten-Free"]
            },
            {
                "id": "mozzarella-fry-cheese",
                "nameEs": "Queso Frito en Costra de Panko",
                "nameEn": "Mozzarella Fry Cheese",
                "descriptionEs": "Cuadros de queso mozzarella empanizados en panko crujiente servidos con salsa tibia de tomate al chipotle y epazote.",
                "descriptionEn": "Crispy panko-crusted fried mozzarella served with rich chipotle tomato dipping sauce and Mexican epazote.",
                "price": 11.00,
                "category": "guacamole-antojitos",
                "badge": None,
                "allergens": ["Dairy", "Gluten", "Vegetarian"]
            },

            # --- TACOS HECHOS A MANO ---
            {
                "id": "taco-baja",
                "nameEs": "Taco Baja de Mahi Mahi Crujiente",
                "nameEn": "Baja Mahi Mahi Taco",
                "descriptionEs": "Filete de pescado mahi mahi empanizado en panko crujiente, pico de gallo fresco y alioli de limón en tortilla de maíz nixtamalizado.",
                "descriptionEn": "Crispy panko-crusted mahi mahi, house pico de gallo, and bright lemon aioli in a soft nixtamal corn tortilla.",
                "price": 5.25,
                "category": "tacos",
                "badge": "Top Seller",
                "allergens": ["Fish", "Gluten", "Eggs"]
            },
            {
                "id": "taco-cochinita-pibil",
                "nameEs": "Taco de Cochinita Pibil",
                "nameEn": "Cochinita Pibil Taco",
                "descriptionEs": "Cerdo tierno marinado en achiote yucateco cocinado a fuego lento, frijoles refritos, cebollas moradas encurtidas y cilantro.",
                "descriptionEn": "Yucatan-style slow-cooked citrus-achiote pork, creamy refried black beans, tangy pickled red onions, and cilantro.",
                "price": 4.95,
                "category": "tacos",
                "badge": "Auténtico",
                "allergens": ["Pork", "Gluten-Free"]
            },
            {
                "id": "taco-gambas",
                "nameEs": "Taco de Gambas al Chile Ancho",
                "nameEn": "Gambas Ancho Shrimp Taco",
                "descriptionEs": "Camarones sellados a la plancha con chile ancho, salsa fresca de pepino y mango dulce y mayonesa al chipotle ahumado.",
                "descriptionEn": "Seared ancho chili shrimp, refreshing cucumber-mango salsa, and smoky chipotle mayo.",
                "price": 5.50,
                "category": "tacos",
                "badge": "Mariscos",
                "allergens": ["Shellfish", "Eggs", "Gluten-Free"]
            },
            {
                "id": "taco-ya-mon",
                "nameEs": "Taco Ya Mon de Pollo Jerk",
                "nameEn": "Ya Mon Jerk Chicken Taco",
                "descriptionEs": "Pechuga de pollo marinada en especias jerk caribeñas, col rizada crujiente y plátanos maduros fritos.",
                "descriptionEn": "Spiced jerk marinated chicken, crispy shredded kale, and sweet fried plantains.",
                "price": 4.95,
                "category": "tacos",
                "badge": "Fusión",
                "allergens": ["Gluten-Free"]
            },
            {
                "id": "taco-pork-carnitas",
                "nameEs": "Taco de Carnitas Michoacanas",
                "nameEn": "Pork Carnitas Taco",
                "descriptionEs": "Carnitas crujientes de cerdo, papas doradas, cebolla picada, crema de aguacate con chile serrano y cilantro fresco.",
                "descriptionEn": "Crispy golden slow-cooked pork carnitas, roasted potato cubes, onion, serrano-avocado crema, and cilantro.",
                "price": 4.95,
                "category": "tacos",
                "badge": "Clásico",
                "allergens": ["Pork", "Dairy", "Gluten-Free"]
            },
            {
                "id": "taco-argentino",
                "nameEs": "Taco Argentino de Hanger Steak",
                "nameEn": "Argentino Hanger Steak Taco",
                "descriptionEs": "Corte jugoso de hanger steak asado a la parrilla, cebolla asada dulce, salsa picante de chile de árbol y cilantro.",
                "descriptionEn": "Grilled hanger steak asada, charred sweet onions, spicy chile de arbol salsa, and cilantro.",
                "price": 5.50,
                "category": "tacos",
                "badge": "Carne",
                "allergens": ["Beef", "Gluten-Free"]
            },
            {
                "id": "taco-americano",
                "nameEs": "Taco Americano Crujiente",
                "nameEn": "Americano Crispy Taco",
                "descriptionEs": "Carne molida de res sazonada con especias de la casa, queso manchego rallado y salsa de russa en tortilla crujiente dorada.",
                "descriptionEn": "Seasoned ground beef, shredded manchego cheese, and house salsa de russa in a crunchy hard-shell taco.",
                "price": 4.75,
                "category": "tacos",
                "badge": "Crujiente",
                "allergens": ["Beef", "Dairy", "Gluten-Free"]
            },
            {
                "id": "taco-chicken-tinga",
                "nameEs": "Taco de Tinga de Pollo",
                "nameEn": "Chicken Tinga Taco",
                "descriptionEs": "Pollo deshebrado estofado en salsa tradicional de jitomate y chipotle, queso cotija y crema mexicana.",
                "descriptionEn": "Slow-braised chicken in rich smoky chipotle-tomato sauce, crumbled cotija cheese, and Mexican crema.",
                "price": 4.95,
                "category": "tacos",
                "badge": None,
                "allergens": ["Dairy", "Gluten-Free"]
            },
            {
                "id": "taco-duck-mechado",
                "nameEs": "Taco de Pato Mechado",
                "nameEn": "Duck Mechado Taco",
                "descriptionEs": "Pato mechado suavemente desmenuzado con ensalada crujiente de col morada y aderezo cremoso de jalapeño y aguacate.",
                "descriptionEn": "Tender shredded braised duck, crunchy cabbage slaw, and creamy jalapeño-avocado dressing.",
                "price": 5.50,
                "category": "tacos",
                "badge": "Especialidad",
                "allergens": ["Dairy", "Gluten-Free"]
            },
            {
                "id": "taco-seared-tuna",
                "nameEs": "Taco de Atún Sellado",
                "nameEn": "Seared Tuna Taco",
                "descriptionEs": "Atún fresco sellado al sésamo con puré de aguacate, tiras de zanahoria al jengibre y alioli cremoso de sriracha.",
                "descriptionEn": "Seared rare ahi tuna, crushed avocado, ginger carrots, and spicy sriracha aioli.",
                "price": 5.75,
                "category": "tacos",
                "badge": "Premium",
                "allergens": ["Fish", "Eggs", "Gluten-Free"]
            },
            {
                "id": "taco-rajas-veggie",
                "nameEs": "Taco Vegetariano de Rajas Poblanas",
                "nameEn": "Rajas Veggie Taco",
                "descriptionEs": "Salteado de chile poblano asado, col rizada, elote tierno, pimientos, cebolla dulce y queso fresco.",
                "descriptionEn": "Sautéed roasted poblano peppers, kale, sweet corn, bell peppers, onions, and crumbled queso fresco.",
                "price": 4.75,
                "category": "tacos",
                "badge": "Vegetariano",
                "allergens": ["Dairy", "Vegetarian", "Gluten-Free"]
            },

            # --- BIRRIA Y CALLEJEROS OAXACA ---
            {
                "id": "oaxaca-brisket-tacos",
                "nameEs": "Tacos Callejeros Oaxaca de Brisket (2)",
                "nameEn": "Oaxaca Street Style Brisket Tacos (2)",
                "descriptionEs": "Dos tortillas de maíz doradas al comal rellenas de brisket de res ahumado jugoso y queso Oaxaca derretido. Acompañado de consomé de birria caliente para sopear.",
                "descriptionEn": "Two griddled corn tortillas stuffed with juicy smoked beef brisket and melty Oaxaca cheese. Served with a warm cup of rich birria consomé for dipping.",
                "price": 12.00,
                "category": "birria-oaxaca",
                "badge": "Favorito de la Casa",
                "allergens": ["Beef", "Dairy", "Gluten-Free"]
            },
            {
                "id": "oaxaca-mushroom-tacos",
                "nameEs": "Tacos Callejeros Oaxaca de Portobello (2)",
                "nameEn": "Oaxaca Street Mushroom Tacos (2)",
                "descriptionEs": "Dos tortillas de harina hechas a mano a la plancha rellenas de champiñones portobello salteados, cebolla caramelizada, rajas de poblano y queso Oaxaca fundido.",
                "descriptionEn": "Two griddled flour tortillas stuffed with hearty portobello mushrooms, caramelized onion, roasted poblano peppers, and melted Oaxaca cheese.",
                "price": 11.00,
                "category": "birria-oaxaca",
                "badge": "Vegetariano",
                "allergens": ["Dairy", "Gluten", "Vegetarian"]
            },
            {
                "id": "birria-dilla",
                "nameEs": "Birria-Dilla con Consomé",
                "nameEn": "Birria Dilla",
                "descriptionEs": "Quesadilla crujiente en tortilla de maíz rellena de carne de res estofada al chile pasilla, quesos cotija y Oaxaca derretidos, servida con consomé pasilla caliente.",
                "descriptionEn": "Crispy griddled corn tortilla quesadilla packed with pasilla-braised beef, cotija, and Oaxaca cheeses. Served with warm pasilla dipping broth.",
                "price": 16.00,
                "category": "birria-oaxaca",
                "badge": "Must Order",
                "allergens": ["Beef", "Dairy", "Gluten-Free"]
            },
            {
                "id": "birria-nachos",
                "nameEs": "Nachos Supremos de Birria",
                "nameEn": "Birria Nachos",
                "descriptionEs": "Totopos de maíz crujientes bañados con birria deshebrada, salsa de chile cascabel, quesos mexicanos fundidos, mousse de aguacate, jalapeños encurtidos y crema.",
                "descriptionEn": "Crispy corn chips piled high with shredded beef birria, savory cascabel sauce, melted Mexican cheese, avocado mousse, pickled jalapeño, and crema.",
                "price": 16.00,
                "category": "birria-oaxaca",
                "badge": "Generoso",
                "allergens": ["Beef", "Dairy", "Gluten-Free"]
            },
            {
                "id": "korean-short-rib-placero",
                "nameEs": "Placero de Costilla Corta al Estilo Coreano",
                "nameEn": "Korean Short Rib Placero",
                "descriptionEs": "Costilla de res glaseada tierna, caldo aromático de birria, tortilla de harina con queso derretido, ensalada crujiente de pepino y jalapeño, cacahuates con chile y ajonjolí.",
                "descriptionEn": "Tender glazed beef short rib, rich birria broth, cheesy griddled flour tortilla, crisp cucumber-jalapeño salad, chili peanuts, and toasted sesame seeds.",
                "price": 18.00,
                "category": "birria-oaxaca",
                "badge": "Chef Creation",
                "allergens": ["Beef", "Dairy", "Gluten", "Peanuts", "Sesame"]
            },

            # --- PLATOS PRINCIPALES Y FAJITAS ---
            {
                "id": "duck-carnitas-enchiladas",
                "nameEs": "Enchiladas de Carnitas de Pato",
                "nameEn": "Duck Carnitas Enchiladas",
                "descriptionEs": "Tortillas de maíz enrolladas rellenas de tiernas carnitas de pato, salsa verde de poblano y tomatillo, queso jalapeño-jack gratinado, crema, queso fresco y coles de Bruselas crujientes.",
                "descriptionEn": "Tender braised duck carnitas rolled in corn tortillas, covered with roasted poblano-tomatillo sauce, melted jalapeño-jack cheese, crema, queso fresco, and crispy brussels sprouts.",
                "price": 24.00,
                "category": "platos",
                "badge": "Plato Insignia",
                "allergens": ["Dairy", "Gluten-Free"]
            },
            {
                "id": "camarones-enchilados",
                "nameEs": "Camarones Enchilados Costeños",
                "nameEn": "Camarones Enchilados",
                "descriptionEs": "Camarones gigantes salteados en salsa picante enchilada, servidos con ensalada fresca de mango con jícama y arroz blanco bañado en crema mexicana.",
                "descriptionEn": "Sautéed jumbo shrimp in spicy house chili sauce, paired with refreshing mango-jicama salad and arroz con crema mexicana.",
                "price": 19.00,
                "category": "platos",
                "badge": "Mariscos",
                "allergens": ["Shellfish", "Dairy", "Gluten-Free"]
            },
            {
                "id": "carne-asada-bodega",
                "nameEs": "Carne Asada de Hanger Steak",
                "nameEn": "Carne Asada",
                "descriptionEs": "Hanger steak marinado y asado al término preferido, acompañado de papas doradas al horno, cebollitas asadas y salsa macha de chiles secos y semillas.",
                "descriptionEn": "Char-grilled marinated hanger steak, roasted golden potatoes, sweet grilled onions, and nutty salsa macha reduction.",
                "price": 28.00,
                "category": "platos",
                "badge": "Carne Premium",
                "allergens": ["Beef", "Nuts", "Gluten-Free"]
            },
            {
                "id": "salmon-al-pastor",
                "nameEs": "Salmón del Atlántico al Pastor",
                "nameEn": "Salmon al Pastor",
                "descriptionEs": "Filete de salmón fresco marinado en adobo al pastor, piña asada al carbón, ensalada fresca de col, rábano y jícama, pepitas tostadas y vinagreta de guajillo.",
                "descriptionEn": "Pan-seared Atlantic salmon glazed with al pastor adobo, char-grilled pineapple, cabbage-radish-jicama slaw, toasted pumpkin seeds, and guajillo vinaigrette.",
                "price": 26.00,
                "category": "platos",
                "badge": "Especialidad",
                "allergens": ["Fish", "Gluten-Free"]
            },
            {
                "id": "double-smash-burger",
                "nameEs": "Hamburguesa Double Smash Bodega",
                "nameEn": "Double Smash Burger",
                "descriptionEs": "Dos hamburguesas smash de res Angus, cebolla caramelizada, queso muenster fundido, tomate, jalapeño asado al agave y salsa russa en pan brioche tostado con papas.",
                "descriptionEn": "Two smashed beef patties, caramelized sweet onions, melted muenster cheese, tomato, agave roasted jalapeño, and house russa sauce on a toasted brioche bun.",
                "price": 16.00,
                "category": "platos",
                "badge": "Popular",
                "allergens": ["Beef", "Dairy", "Gluten", "Eggs"]
            },
            {
                "id": "fajitas-hanger-steak",
                "nameEs": "Fajitas Chispeantes de Hanger Steak",
                "nameEn": "Hanger Steak Sizzling Fajitas",
                "descriptionEs": "Corte de carne servido en sartén de hierro hirviendo con mezcla de pimientos, cebollas, champiñones, tomatillos, queso Oaxaca fundido, cebollitas toreadas, crema y tortillas de harina.",
                "descriptionEn": "Sizzling platter with sliced hanger steak, peppers, onions, mushrooms, tomatillos, melted Oaxaca cheese fundido, spring onion toreados, crema, and warm flour tortillas.",
                "price": 27.00,
                "category": "platos",
                "badge": "Sizzling Platter",
                "allergens": ["Beef", "Dairy", "Gluten"]
            },
            {
                "id": "fajitas-ancho-shrimp",
                "nameEs": "Fajitas Chispeantes de Camarón al Ancho",
                "nameEn": "Ancho Shrimp Sizzling Fajitas",
                "descriptionEs": "Camarones salteados con adobo de chile ancho sobre cama de verduras chispeantes, queso fundido, crema agria y tortillas de harina.",
                "descriptionEn": "Jumbo shrimp rubbed in ancho chili, served over sizzling peppers, onions, mushrooms, Oaxaca cheese fundido, crema, and flour tortillas.",
                "price": 25.00,
                "category": "platos",
                "badge": "Sizzling Platter",
                "allergens": ["Shellfish", "Dairy", "Gluten"]
            },

            # --- BURRITOS, BOWLS Y QUESADILLAS ---
            {
                "id": "bodega-burrito-clasico",
                "nameEs": "Burrito Monumental Bodega",
                "nameEn": "Bodega Burrito",
                "descriptionEs": "Arroz mexicano, frijoles negros, pico de gallo, queso fresco, aguacate, crema y elección de salsa roja o regular envueltos en tortilla gigante de harina. Elija pollo tinga, carnitas, res o verduras.",
                "descriptionEn": "Giant flour tortilla rolled with Mexican rice, black beans, fresh pico, queso fresco, sliced avocado, crema, and choice of protein (Chicken Tinga, Carnitas, Beef, or Rajas).",
                "price": 15.00,
                "category": "burritos-bowls",
                "badge": "Relleno",
                "allergens": ["Dairy", "Gluten"]
            },
            {
                "id": "bodega-burrito-bowl",
                "nameEs": "Burrito Bowl Bodega",
                "nameEn": "Bodega Burrito Bowl",
                "descriptionEs": "Todos los ingredientes frescos de nuestro burrito servidos en un tazón sin tortilla: arroz, frijoles negros, pico de gallo, queso fresco, aguacate, crema y proteína al gusto.",
                "descriptionEn": "All burrito fixings served in a hearty bowl over rice: black beans, fresh pico, queso fresco, avocado, crema, and choice of meat or roasted veggies.",
                "price": 15.00,
                "category": "burritos-bowls",
                "badge": "Sin Gluten",
                "allergens": ["Dairy", "Gluten-Free"]
            },
            {
                "id": "bodega-cheese-quesadillas",
                "nameEs": "Quesadillas de Queso Bodega",
                "nameEn": "Bodega Cheese Quesadillas",
                "descriptionEs": "Tortilla de harina doblada y tostada a la perfección con abundante queso derretido, acompañada de crema agria y pico de gallo fresco.",
                "descriptionEn": "Golden griddled flour tortilla filled with melted Mexican cheeses, served with fresh pico and cool crema.",
                "price": 12.00,
                "category": "burritos-bowls",
                "badge": None,
                "allergens": ["Dairy", "Gluten", "Vegetarian"]
            },
            {
                "id": "bodega-grain-bowl",
                "nameEs": "Tazón Saludable de Granos Farro Mexicana",
                "nameEn": "Bodega Grain Bowl",
                "descriptionEs": "Base de granos farro al estilo mexicano con coles de Bruselas tostadas, elote tierno desgranado, verduras salteadas rajas y aguacate fresco.",
                "descriptionEn": "Mexican seasoned farro grains topped with blistered Brussels sprouts, sweet street corn elote, rajas veggies, and avocado.",
                "price": 14.00,
                "category": "burritos-bowls",
                "badge": "Saludable",
                "allergens": ["Gluten", "Vegetarian"]
            },

            # --- ENSALADAS Y SOPAS ---
            {
                "id": "mexico-caesar-salad",
                "nameEs": "Ensalada César al Estilo México",
                "nameEn": "Mexico Caesar Salad",
                "descriptionEs": "Lechuga baby gem crujiente con aguacate fresco, jitomates cherry tatemados, aderezo César con queso parmesano y migas de pan crujientes al ajo.",
                "descriptionEn": "Crisp baby gem lettuce, sliced avocado, charred cherry tomatoes, rich parmesan caesar dressing, and crunchy toasted garlic breadcrumbs.",
                "price": 13.00,
                "category": "ensaladas-sopas",
                "badge": "Clásico",
                "allergens": ["Dairy", "Gluten", "Eggs", "Vegetarian"]
            },
            {
                "id": "massaged-kale-salad",
                "nameEs": "Ensalada de Col Rizada y Calabaza Kabocha",
                "nameEn": "Massaged Kale Salad",
                "descriptionEs": "Col rizada tierna masajeada con aderezo de limón y chile poblano, trozos de calabaza kabocha asada, queso cotija y cacahuates tostados con chile piquín.",
                "descriptionEn": "Tender massaged kale, roasted kabocha squash, crumbled cotija cheese, spicy chilified peanuts, and a light lemon-poblano vinaigrette.",
                "price": 14.00,
                "category": "ensaladas-sopas",
                "badge": "Nutritivo",
                "allergens": ["Dairy", "Peanuts", "Gluten-Free", "Vegetarian"]
            },
            {
                "id": "roasted-chicken-soup-pozole",
                "nameEs": "Sopa Pozole de Pollo Rostizado",
                "nameEn": "Roasted Chicken Pozole Soup",
                "descriptionEs": "Sopa tradicional de pollo con granos tiernos de maíz pozolero en caldo de chiles rojos aromáticos con guarniciones crujientes de rábano y col.",
                "descriptionEn": "Hearty roasted chicken soup with hominy corn in a savory red chili broth, finished with crunchy radish and fresh lime garnish.",
                "price": 9.00,
                "category": "ensaladas-sopas",
                "badge": "Reconfortante",
                "allergens": ["Gluten-Free"]
            },

            # --- SIDES Y POSTRES ---
            {
                "id": "arroz-blanco-frijoles-negro",
                "nameEs": "Arroz Blanco y Frijoles Negros",
                "nameEn": "Arroz Blanco y Frijoles Negro",
                "descriptionEs": "Arroz blanco sazonado acompañado de frijoles negros cocidos a fuego lento con epazote.",
                "descriptionEn": "Seasoned white rice and slow-simmered black beans with epazote herbs.",
                "price": 5.00,
                "category": "sides-postres",
                "badge": None,
                "allergens": ["Gluten-Free", "Vegetarian", "Vegan"]
            },
            {
                "id": "platanos-con-crema",
                "nameEs": "Plátanos Maduros Fritos con Crema",
                "nameEn": "Platanos con Crema",
                "descriptionEs": "Plátanos maduros fritos caramelizados por fuera y suaves por dentro, rociados con crema mexicana y queso cotija.",
                "descriptionEn": "Sweet caramelized fried plantains drizzled with rich Mexican crema and crumbled cotija cheese.",
                "price": 6.00,
                "category": "sides-postres",
                "badge": "Dulce y Salado",
                "allergens": ["Dairy", "Gluten-Free", "Vegetarian"]
            },
            {
                "id": "mexican-chocolate-pot-de-creme",
                "nameEs": "Pot de Crème de Chocolate Mexicano",
                "nameEn": "Mexican Chocolate Pot de Creme",
                "descriptionEs": "Crema untuosa de chocolate mexicano con canela, espolvoreada con polvo de chile piquín y crema batida fresca.",
                "descriptionEn": "Silky chilled Mexican chocolate custard with cinnamon, light piquin chili dust, and freshly whipped cream.",
                "price": 9.00,
                "category": "sides-postres",
                "badge": "Postre Estrella",
                "allergens": ["Dairy", "Eggs", "Gluten-Free", "Vegetarian"]
            },
            {
                "id": "smores-fundido",
                "nameEs": "S'mores Fundido con Tortillas de Canela",
                "nameEn": "S'mores Fundido",
                "descriptionEs": "Malvaviscos tostados derretidos sobre chocolate caliente líquido, acompañados de tortillas de maíz fritas espolvoreadas con azúcar y canela.",
                "descriptionEn": "Gooey roasted marshmallows melted over rich chocolate sauce, served with crispy cinnamon-sugar dusted tortillas.",
                "price": 9.00,
                "category": "sides-postres",
                "badge": "Para Compartir",
                "allergens": ["Dairy", "Gluten", "Vegetarian"]
            },
            {
                "id": "chocolate-tres-leches",
                "nameEs": "Pastel de Tres Leches de Chocolate y Fresa",
                "nameEn": "Chocolate Tres Leches Cake",
                "descriptionEs": "Bizcocho esponjoso de chocolate mexicano bañado en infusión de tres leches con fresas frescas maceradas.",
                "descriptionEn": "Rich Mexican chocolate sponge cake soaked in traditional three-milk infusion with fresh macerated strawberries.",
                "price": 9.00,
                "category": "sides-postres",
                "badge": "Favorito",
                "allergens": ["Dairy", "Eggs", "Gluten", "Vegetarian"]
            },

            # --- BEBIDAS Y MARGARITAS ---
            {
                "id": "bodegarita-signature",
                "nameEs": "Margarita Insignia 'Bodegarita'",
                "nameEn": "The Bodegarita",
                "descriptionEs": "Nuestra margarita estrella preparada con tequila Cazadores blanco, licor Luxardo Triplum, jugo de lima fresca y néctar de agave orgánico.",
                "descriptionEn": "Our house signature margarita shaken with Cazadores blanco tequila, Luxardo Triplum orange liqueur, fresh lime juice, and organic agave.",
                "price": 13.00,
                "category": "bebidas-margaritas",
                "badge": "#1 Cocktail",
                "allergens": ["Alcohol"]
            },
            {
                "id": "spicy-rita",
                "nameEs": "Spicy Rita de Jalapeño",
                "nameEn": "Spicy Rita",
                "descriptionEs": "Tequila infundido en la casa con jalapeños frescos, Triplum, jugo de lima y néctar de agave con escarchado picante.",
                "descriptionEn": "House jalapeño-infused tequila, Triplum, fresh lime juice, agave nectar, and spicy chile-salted rim.",
                "price": 14.00,
                "category": "bebidas-margaritas",
                "badge": "Picante",
                "allergens": ["Alcohol", "Spicy"]
            },
            {
                "id": "blood-orange-margarita",
                "nameEs": "Margarita de Naranja Roja",
                "nameEn": "Blood Orange Margarita",
                "descriptionEs": "Tequila Espolón blanco, licor Triplum, puré natural de naranja roja siciliana y agave orgánico.",
                "descriptionEn": "Espolón blanco tequila, Triplum, vibrant Sicilian blood orange, and sweet organic agave.",
                "price": 14.00,
                "category": "bebidas-margaritas",
                "badge": "Cítrico",
                "allergens": ["Alcohol"]
            },
            {
                "id": "agua-fresca-cuatro-citrus",
                "nameEs": "Agua Fresca Cuatro Cítricos",
                "nameEn": "Cuatro Citrus Agua Fresca",
                "descriptionEs": "Bebida refrescante sin alcohol preparada diariamente con jugo fresco de naranja, lima, limón amarillo y toronja rosada.",
                "descriptionEn": "Daily house-made fresh fruit refresher made with pure pressed orange, lime, lemon, and ruby grapefruit juices.",
                "price": 5.00,
                "category": "bebidas-margaritas",
                "badge": "Sin Alcohol",
                "allergens": ["Vegetarian", "Vegan", "Gluten-Free"]
            },
            {
                "id": "mexican-coca-cola",
                "nameEs": "Coca-Cola Mexicana de Botella de Vidrio",
                "nameEn": "Mexican Coke",
                "descriptionEs": "Auténtica Coca-Cola importada de México endulzada con azúcar de caña pura en botella de vidrio de 355 ml.",
                "descriptionEn": "Authentic imported glass bottle Mexican Coke sweetened exclusively with 100% pure cane sugar.",
                "price": 4.00,
                "category": "bebidas-margaritas",
                "badge": "Importado",
                "allergens": ["Vegetarian", "Vegan", "Gluten-Free"]
            }
        ],
        "faqs": [
            {
                "qEs": "¿Tienen opciones sin gluten o para vegetarianos?",
                "qEn": "Do you have gluten-free or vegetarian options?",
                "aEs": "¡Sí! Nuestros tacos se preparan en tortillas de maíz nixtamalizado libres de gluten y ofrecemos lechuga como envoltura ('lettuce cups'). También contamos con opciones vegetarianas y veganas claramente marcadas en nuestro menú.",
                "aEn": "Yes! All our tacos are prepared on gluten-free nixtamal corn tortillas or crisp lettuce cups upon request. We also offer clearly marked vegetarian and vegan dishes."
            },
            {
                "qEs": "¿Tienen especiales de Taco Tuesday?",
                "qEn": "Do you have Taco Tuesday specials?",
                "aEs": "¡Por supuesto! Todos los martes ofrecemos $1.00 de descuento en todos los tacos individuales y Bodegaritas a $9.00 todo el día para clientes en el salón.",
                "aEn": "Absolutely! Every Tuesday we feature $1.00 off all individual tacos and $9.00 Bodegaritas all day for dine-in guests."
            },
            {
                "qEs": "¿Se pueden ordenar paquetes familiares para llevar?",
                "qEn": "Can we order family taco packs for takeout?",
                "aEs": "Sí, ofrecemos paquetes 'Bodega Family Pack' y 'Taco 6-Pack' con totopos, guacamole, salsas y guarniciones ideales para compartir en familia o eventos.",
                "aEn": "Yes, we offer Bodega Family Packs and Taco 6-Packs complete with chips, guacamole, salsas, and sides perfect for family sharing."
            }
        ]
    }

    # Transform items to format expected by schema
    products = []
    for item in data["items"]:
        products.append({
            "id": item["id"],
            "nameEs": item["nameEs"],
            "nameEn": item["nameEn"],
            "descriptionEs": item["descriptionEs"],
            "descriptionEn": item["descriptionEn"],
            "price": item["price"],
            "category": item["category"],
            "badge": item["badge"],
            "allergens": item["allergens"]
        })

    full_record = {
        "storeInfo": data["storeInfo"],
        "categories": data["categories"],
        "products": products,
        "faqs": data["faqs"]
    }

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(full_record, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully wrote {dest} with {len(products)} 100% verified authentic items!")

if __name__ == "__main__":
    build_bodega()
