#!/usr/bin/env python3
import json
import os
import sys

def build_obriens():
    dest = "data/merchants/obriens-irish-pub.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["storeInfo"]["name"] = "O'Brien's Irish Pub"
    data["storeInfo"]["address"] = "83 Lake Ave, Danbury, CT 06810"
    data["storeInfo"]["tagline"] = "Authentic Irish Pub Fare, Craft Pints & Warm Hospitality / Auténtica Comida de Pub Irlandés y Cervezas"
    data["storeInfo"]["phone"] = "(203) 628-7108"

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
        {"id": "irish-favorites", "nameEs": "Especialidades Irlandesas", "nameEn": "Irish Favorites", "icon": "Utensils"},
        {"id": "burgers", "nameEs": "Hamburguesas Angus", "nameEn": "Angus Burgers", "icon": "Beef"},
        {"id": "sandwiches-wraps", "nameEs": "Sándwiches y Wraps", "nameEn": "Sandwiches & Wraps", "icon": "Sandwich"},
        {"id": "starters", "nameEs": "Entrantes y Alitas", "nameEn": "Starters & Wings", "icon": "Utensils"},
        {"id": "entrees", "nameEs": "Platos Fuertes y Pastas", "nameEn": "Main Dishes", "icon": "Beef"},
        {"id": "soups-salads", "nameEs": "Sopas y Ensaladas", "nameEn": "Soups & Salads", "icon": "Salad"},
        {"id": "sides", "nameEs": "Acompañamientos", "nameEn": "Sides", "icon": "Utensils"}
    ]

    items = [
        # --- IRISH FAVORITES ---
        {
            "id": "full-irish-breakfast",
            "nameEs": "Desayuno Tradicional Irlandés Completo (Full Irish Breakfast)",
            "nameEn": "Traditional Full Irish Breakfast",
            "descriptionEs": "El desayuno tradicional: tocino irlandés, salchichas irlandesas, morcilla negra y blanca (pudding), tomates asados a la plancha, 2 huevos al gusto y pan tostado.",
            "descriptionEn": "Traditional hearty Irish breakfast: imported Irish bacon, Irish sausages, black and white pudding, grilled tomatoes, 2 eggs, and toast.",
            "price": 16.99,
            "category": "irish-favorites",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "beer-battered-fish-chips",
            "nameEs": "Fish & Chips Rebozado a la Cerveza",
            "nameEn": "Beer-Battered Fish & Chips",
            "descriptionEs": "Filetes tiernos de bacalao rebozados en masa crujiente de cerveza artesanal dorados a la perfección, servidos con papas fritas y salsa tártara casera.",
            "descriptionEn": "Crispy beer-battered fresh cod fillets fried golden, served with piping hot hand-cut fries, lemon, and house tartar sauce.",
            "price": 16.99,
            "category": "irish-favorites",
            "allergens": ["Gluten", "Pescado", "Huevos"],
            "popular": True
        },
        {
            "id": "corned-beef-cabbage",
            "nameEs": "Carne Curada con Col Tradicional (Corned Beef and Cabbage)",
            "nameEn": "Traditional Corned Beef and Cabbage",
            "descriptionEs": "Falda de res curada cocida lentamente hasta quedar ultra tierna, servida con col verde al vapor, papas rojas y zanahorias tiernas.",
            "descriptionEn": "Slow-braised melt-in-your-mouth corned beef brisket served with tender steamed cabbage, boiled red potatoes, and baby carrots.",
            "price": 18.99,
            "category": "irish-favorites",
            "popular": True
        },
        {
            "id": "bangers-and-mash",
            "nameEs": "Salchichas Irlandesas con Puré de Papas (Bangers & Mash)",
            "nameEn": "Bangers and Mash",
            "descriptionEs": "Auténticas salchichas irlandesas de cerdo servidas sobre una cama de puré de papas cremoso, coronadas con cebollas caramelizadas y gravy oscuro casero.",
            "descriptionEn": "Traditional plump Irish pork sausages served over creamy mashed potatoes, smothered in sweet caramelized onions and rich brown gravy.",
            "price": 16.99,
            "category": "irish-favorites",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "homemade-shepherds-pie",
            "nameEs": "Pastel de Pastor Casero Irlandés (Shepherd’s Pie)",
            "nameEn": "Homemade Shepherd’s Pie",
            "descriptionEs": "Carne molida de res sazonada cocinada a fuego lento con cebollas, maíz tierno, chícharos y zanahorias en salsa sustanciosa, cubierta con puré de papa gratinado y queso fundido.",
            "descriptionEn": "Savory seasoned minced beef simmered with onions, sweet corn, garden peas, and carrots, topped with baked mashed potatoes and melted cheese.",
            "price": 18.99,
            "category": "irish-favorites",
            "allergens": ["Lácteos"],
            "popular": True
        },

        # --- BURGERS ---
        {
            "id": "obrien-burger",
            "nameEs": "Hamburguesa Insignia O’Brien",
            "nameEn": "O’Brien Signature Burger",
            "descriptionEs": "Carne 100% Angus a la parrilla en pan brioche tostado, cubierta con tocino irlandés crujiente, huevo frito tierno y queso cheddar derretido.",
            "descriptionEn": "100% Angus beef patty on a toasted brioche bun, topped with crispy Irish bacon, a fried egg, and melted cheddar cheese.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "dubliner-burger",
            "nameEs": "Hamburguesa Dubliner con Cebolla Salteada y Tocino",
            "nameEn": "Dubliner Burger",
            "descriptionEs": "Carne Angus jugosa con queso cheddar añejo fundido, cebollas caramelizadas salteadas y abundante tocino crujiente.",
            "descriptionEn": "100% Angus beef topped with melted cheddar cheese, sweet sautéed onions, and crispy smoked bacon on brioche.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "belfast-burger",
            "nameEs": "Hamburguesa Clásica Belfast",
            "nameEn": "Belfast Classic Burger",
            "descriptionEs": "Hamburguesa Angus con queso americano fundido, lechuga fresca, rebanadas de jitomate y cebolla en pan brioche.",
            "descriptionEn": "100% Angus beef patty with melted cheese, crisp lettuce, ripe tomato, and red onion on a brioche bun.",
            "price": 13.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "gorgonzola-bacon-burger",
            "nameEs": "Hamburguesa con Queso Gorgonzola y Tocino",
            "nameEn": "Gorgonzola Bacon Burger",
            "descriptionEs": "Carne Angus con queso azul gorgonzola desmoronado, tocino crujiente ahumado, lechuga y jitomate.",
            "descriptionEn": "100% Angus beef topped with tangy melted gorgonzola crumbles, smoky bacon, fresh lettuce, and tomato.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "cali-burger",
            "nameEs": "Hamburguesa California con Aguacate",
            "nameEn": "Cali Avocado & Bacon Burger",
            "descriptionEs": "Carne Angus con queso derretido, rebanadas de aguacate fresco, cebolla morada y tocino crujiente.",
            "descriptionEn": "100% Angus beef topped with melted cheese, fresh sliced avocado, red onion, and smoky bacon on brioche.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "chili-cheddar-burger",
            "nameEs": "Hamburguesa con Chili Casero y Cheddar",
            "nameEn": "Chili Cheddar Burger",
            "descriptionEs": "Hamburguesa Angus bañada en abundante chili casero de carne de res con especias y queso cheddar fundido.",
            "descriptionEn": "100% Angus beef smothered in hearty house-made beef chili and melted cheddar cheese.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "cowboy-bbq-burger",
            "nameEs": "Hamburguesa Vaquera Cowboy Bacon BBQ",
            "nameEn": "Cowboy Bacon BBQ Burger",
            "descriptionEs": "Carne Angus con queso cheddar, aros de cebolla crujientes dorados, tocino ahumado y salsa barbacoa dulce.",
            "descriptionEn": "100% Angus beef topped with melted cheddar, crisp smoky bacon, golden onion rings, and tangy BBQ sauce.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "swiss-mushroom-burger",
            "nameEs": "Hamburguesa con Champiñones y Queso Suizo",
            "nameEn": "Swiss & Sautéed Mushroom Burger",
            "descriptionEs": "Carne Angus cubierta de champiñones salteados a la mantequilla y queso suizo derretido.",
            "descriptionEn": "100% Angus beef topped with buttery sautéed button mushrooms and melted Swiss cheese.",
            "price": 14.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- SANDWICHES & WRAPS ---
        {
            "id": "corned-beef-reuben",
            "nameEs": "Sándwich Reuben Tradicional de Corned Beef en Pan de Centeno",
            "nameEn": "Classic Corned Beef Reuben on Rye",
            "descriptionEs": "Corned beef caliente en pan de centeno tostado, queso suizo fundido, chucrut agridulce y aderezo ruso de la casa.",
            "descriptionEn": "Tender corned beef on toasted rye with melted Swiss cheese, tangy sauerkraut, and Russian dressing (or plain with deli mustard).",
            "price": 14.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Huevos"],
            "popular": True
        },
        {
            "id": "sliced-steak-sandwich",
            "nameEs": "Sándwich de Filete de Res en Rebanadas con Queso Suizo",
            "nameEn": "Sliced Steak Sandwich with Sautéed Onions",
            "descriptionEs": "Tiernas tiras de bistec con cebollas y champiñones salteados cubiertas con queso suizo derretido en pan tostado.",
            "descriptionEn": "Tender sliced steak with sautéed onions and mushrooms topped with melted Swiss cheese on a toasted roll.",
            "price": 15.50,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "irish-blt",
            "nameEs": "Sándwich B.L.T. con Tocino Irlandés Crujiente",
            "nameEn": "Traditional Irish B.L.T. Sandwich",
            "descriptionEs": "Auténtico tocino irlandés importado dorado crujiente, lechuga fresca, jitomate y mayonesa en pan blanco tostado.",
            "descriptionEn": "Crispy imported Irish back bacon, fresh lettuce, sliced ripe tomato, and mayonnaise on toasted white bread.",
            "price": 12.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Huevos"]
        },
        {
            "id": "crispy-chicken-fillet-sandwich",
            "nameEs": "Sándwich de Filete de Pollo Crujiente con Chipotle",
            "nameEn": "Crispy Chicken Fillet Sandwich with Chipotle Mayo",
            "descriptionEs": "Pechuga de pollo frita crujiente con queso cheddar fundido, lechuga, jitomate y mayonesa de chipotle en pan brioche.",
            "descriptionEn": "Golden fried chicken breast, melted cheddar, lettuce, tomato, and zesty chipotle mayo on a toasted brioche bun.",
            "price": 14.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Huevos"]
        },
        {
            "id": "pesto-chicken-sandwich",
            "nameEs": "Sándwich de Pollo al Pesto y Mozzarella",
            "nameEn": "Pesto Grilled Chicken Sandwich",
            "descriptionEs": "Pollo a la parrilla, queso mozzarella derretido, jitomates maduros, verduras frescas y mayonesa al pesto en panecillo tostado.",
            "descriptionEn": "Grilled chicken breast, melted mozzarella, ripe tomatoes, fresh greens, and pesto mayo on a toasted roll.",
            "price": 14.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Huevos", "Frutos secos"]
        },
        {
            "id": "chicken-quesadilla",
            "nameEs": "Quesadilla de Pollo y Queso con Salsa y Crema",
            "nameEn": "Chicken & Melted Cheese Quesadilla",
            "descriptionEs": "Tortilla dorada a la plancha rellena de pollo sazonado y queso derretido, servida con salsa y crema agria.",
            "descriptionEn": "Grilled flour tortilla folded with seasoned chicken and melted cheddar-jack cheese, served with salsa and sour cream.",
            "price": 14.50,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "philly-steak-wrap",
            "nameEs": "Wrap Philly de Bistec, Pimientos y Champiñones",
            "nameEn": "Philly Steak Wrap with Peppers & Onions",
            "descriptionEs": "Bistec a la plancha con cebollas, pimientos y champiñones salteados con queso cheddar en tortilla suave de harina.",
            "descriptionEn": "Grilled sliced steak, sautéed onions, bell peppers, mushrooms, and melted cheddar wrapped in a warm flour tortilla.",
            "price": 15.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "california-chicken-wrap",
            "nameEs": "Wrap California de Pollo a la Parrilla y Aguacate",
            "nameEn": "California Grilled Chicken Wrap",
            "descriptionEs": "Pechuga de pollo a la parrilla, aguacate fresco, lechuga, jitomate, tocino crujiente y mayonesa.",
            "descriptionEn": "Grilled chicken breast, fresh avocado, lettuce, ripe tomato, smoky bacon, and mayonnaise in a flour wrap.",
            "price": 13.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Huevos"]
        },
        {
            "id": "crispy-buffalo-chicken-wrap",
            "nameEs": "Wrap de Pollo Crujiente Buffalo",
            "nameEn": "Crispy Buffalo Chicken Wrap",
            "descriptionEs": "Tiras de pollo crujiente bañadas en salsa picante Buffalo, lechuga fresca, jitomate y aderezo cremoso de queso azul.",
            "descriptionEn": "Crispy fried chicken tossed in spicy Buffalo sauce, fresh lettuce, tomato, and creamy blue cheese dressing.",
            "price": 13.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Huevos"]
        },

        # --- ENTRANTES Y ALITAS ---
        {
            "id": "crispy-wings-8",
            "nameEs": "Alitas Crujientes (8 piezas)",
            "nameEn": "8 Crispy Jumbo Chicken Wings",
            "descriptionEs": "Alitas de pollo doradas en su elección de salsa: Buffalo (Picante, Media, Suave), Ajo Parmesano, BBQ Dulce, Sweet Chili, Teriyaki, Dry Rub Cajún o Pimienta Limón. Servidas con apio y aderezo.",
            "descriptionEn": "Eight jumbo wings tossed in your choice of sauce: Hot, Medium, Mild, Garlic Parmesan, BBQ, Sweet Chili, Teriyaki, Cajun Dry Rub, or Lemon Pepper. Served with celery and blue cheese or ranch.",
            "price": 12.99,
            "category": "starters",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "boneless-wings-10",
            "nameEs": "Alitas Deshuesadas Boneless (10 piezas)",
            "nameEn": "10 Boneless Wings",
            "descriptionEs": "Diez trozos de pechuga de pollo empanizados y dorados crujientes bañados en su salsa favorita.",
            "descriptionEn": "Ten tender all-white meat boneless wings tossed in your choice of signature wing sauce.",
            "price": 11.99,
            "category": "starters",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "irish-nachos",
            "nameEs": "Nachos Irlandeses con Papas Caseras",
            "nameEn": "Irish Nachos on House Potato Chips",
            "descriptionEs": "Papas fritas caseras estilo chips cubiertas de abundante queso fundido, guacamole, crema agria y salsa fresca mexicana.",
            "descriptionEn": "Crispy house-made potato chips smothered in melted cheddar cheese, guacamole, cool sour cream, and fresh salsa.",
            "price": 12.99,
            "category": "starters",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "beef-sliders-3",
            "nameEs": "Mini Hamburguesas Sliders de Res Angus (3 piezas)",
            "nameEn": "3 Angus Beef Sliders with Caramelized Onions",
            "descriptionEs": "Tres mini hamburguesas de carne 100% Angus con queso cheddar y cebollas caramelizadas dulces en panecillos brioche.",
            "descriptionEn": "Three 100% Angus beef mini sliders topped with melted cheddar cheese and sweet caramelized onions.",
            "price": 10.99,
            "category": "starters",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "crispy-calamari",
            "nameEs": "Calamares Crujientes con Pimientos Picantes",
            "nameEn": "Crispy Calamari with Hot Cherry Peppers",
            "descriptionEs": "Calamares fritos doraditos acompañados de pimientos cherry picantes y salsa marinara casera.",
            "descriptionEn": "Golden fried tender calamari tossed with zesty hot cherry peppers, served with house marinara sauce.",
            "price": 12.99,
            "category": "starters",
            "allergens": ["Gluten", "Mariscos"]
        },
        {
            "id": "chili-cheddar-waffle-fries",
            "nameEs": "Papas Waffle con Chili Casero y Queso Cheddar",
            "nameEn": "Chili Cheddar Waffle Fries",
            "descriptionEs": "Papas estilo rejilla (waffle fries) crujientes cubiertas con chili casero y abundante queso derretido con crema.",
            "descriptionEn": "Crispy waffle fries loaded with house-made beef chili, melted cheddar cheese, and a side of sour cream.",
            "price": 11.99,
            "category": "starters",
            "allergens": ["Lácteos"]
        },
        {
            "id": "mozzarella-sticks",
            "nameEs": "Dedos de Queso Mozzarella Fritos",
            "nameEn": "Crispy Mozzarella Sticks with Marinara",
            "descriptionEs": "Bastones de mozzarella empanizados dorados y crujientes por fuera con queso derretido elástico, salsa marinara.",
            "descriptionEn": "Golden breaded mozzarella sticks with warm melted cheese, served with a side of house marinara.",
            "price": 9.99,
            "category": "starters",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- PLATOS FUERTES Y PASTAS ---
        {
            "id": "baked-honey-mustard-salmon",
            "nameEs": "Salmón Horneado a la Mostaza y Miel",
            "nameEn": "Baked Honey-Mustard Atlantic Salmon",
            "descriptionEs": "Filete de salmón del Atlántico horneado con glaseado de miel y mostaza, servido con puré de papas y verduras de temporada.",
            "descriptionEn": "Fresh Atlantic salmon baked with a honey-mustard glaze, served with sautéed vegetables and creamy mashed potatoes.",
            "price": 20.99,
            "category": "entrees",
            "allergens": ["Pescado", "Lácteos"],
            "popular": True
        },
        {
            "id": "ny-strip-steak",
            "nameEs": "Filete New York Strip con Gravy a la Pimienta",
            "nameEn": "New York Strip Steak with Peppercorn Gravy",
            "descriptionEs": "Corte New York Strip a la parrilla servido con puré de papas suave, vegetales salteados y gravy a la pimienta negra.",
            "descriptionEn": "Choice grilled NY strip steak served with creamy mashed potatoes, seasonal vegetables, and peppercorn gravy.",
            "price": 25.99,
            "category": "entrees",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "bacon-wrapped-meatloaf",
            "nameEs": "Pastel de Carne Envuelto en Tocino con Gravy Casero",
            "nameEn": "Bacon-Wrapped Homestyle Meatloaf",
            "descriptionEs": "Pastel de carne de res casero envuelto en tocino ahumado crujiente, servido con puré de papas, verduras y salsa gravy.",
            "descriptionEn": "Hearty homestyle meatloaf wrapped in crispy bacon, served with mashed potatoes, seasonal vegetables, and house brown gravy.",
            "price": 18.99,
            "category": "entrees",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "bens-chicken-parm",
            "nameEs": "Pollo a la Parmigiana de Ben sobre Penne",
            "nameEn": "Ben's Chicken Parmigiana over Penne",
            "descriptionEs": "Pechuga de pollo empanizada y dorada cubierta con salsa marinara casera y mozzarella derretida sobre pasta penne.",
            "descriptionEn": "Pan-fried breaded chicken cutlet smothered in house marinara and melted mozzarella over penne pasta.",
            "price": 17.99,
            "category": "entrees",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "chicken-francese",
            "nameEs": "Pollo a la Francesa al Limón y Vino Blanco",
            "nameEn": "Chicken Francese in Lemon Wine Sauce",
            "descriptionEs": "Medallones de pollo rebozados en huevo salteados en salsa sedosa de limón, mantequilla y vino blanco, servidos con arroz y verduras.",
            "descriptionEn": "Egg-battered chicken cutlets in a delicate lemon white wine butter sauce, served with rice and seasonal vegetables.",
            "price": 16.99,
            "category": "entrees",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "penne-a-la-vodka",
            "nameEs": "Penne a la Vodka Casero con Parmesano",
            "nameEn": "Penne a la Vodka with Fresh Parmesan",
            "descriptionEs": "Pasta penne salteada en salsa rosa cremosa de vodka hecha en casa con queso parmesano rallado fresco.",
            "descriptionEn": "Penne pasta tossed in a creamy pink house vodka sauce, finished with freshly grated parmesan cheese.",
            "price": 13.99,
            "category": "entrees",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "stuffed-chicken-prosciutto",
            "nameEs": "Pollo Relleno de Prosciutto y Queso Fontina",
            "nameEn": "Stuffed Chicken with Prosciutto & Fontina",
            "descriptionEs": "Pechuga de pollo rellena de prosciutto italiano y queso fontina fundente, bañada en salsa de vino blanco y champiñones, puré y verduras.",
            "descriptionEn": "Pan-seared chicken breast stuffed with prosciutto and fontina cheese in a white wine mushroom reduction, with mashed potatoes and vegetables.",
            "price": 20.99,
            "category": "entrees",
            "allergens": ["Lácteos"]
        },

        # --- SOPAS Y ENSALADAS ---
        {
            "id": "lobster-bisque",
            "nameEs": "Bisque Cremoso de Langosta",
            "nameEn": "Creamy Lobster Bisque",
            "descriptionEs": "Sopa cremosa tradicional de langosta con jerez, crema fresca y trocitos tiernos de carne de langosta.",
            "descriptionEn": "Rich and velvety lobster bisque simmered with sherry and cream with tender lobster morsels.",
            "price": 8.99,
            "category": "soups-salads",
            "allergens": ["Mariscos", "Lácteos"],
            "popular": True
        },
        {
            "id": "french-onion-soup",
            "nameEs": "Sopa Francesa de Cebolla Gratinada con Queso Suizo",
            "nameEn": "Classic French Onion Soup Gratinée",
            "descriptionEs": "Cebollas caramelizadas a fuego lento en caldo oscuro con crutones horneados y capa gruesa de queso suizo gratinado burbujeante.",
            "descriptionEn": "Slow-simmered rich onion broth topped with crusty croutons and a thick blanket of bubbly melted Swiss cheese.",
            "price": 6.99,
            "category": "soups-salads",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "tropical-salad",
            "nameEs": "Ensalada Tropical con Queso de Cabra y Nueces",
            "nameEn": "Tropical Salad with Goat Cheese & Walnuts",
            "descriptionEs": "Hojas verdes mixtas con queso de cabra, gajos de mandarina, manzana, arándanos secos, nueces y vinagreta de frambuesa.",
            "descriptionEn": "Mixed greens, creamy goat cheese, mandarin oranges, apple slices, dried cranberries, walnuts, and raspberry vinaigrette.",
            "price": 12.99,
            "category": "soups-salads",
            "allergens": ["Lácteos", "Frutos secos"]
        },
        {
            "id": "california-gorgonzola-salad",
            "nameEs": "Ensalada California con Aguacate, Tocino y Gorgonzola",
            "nameEn": "California Salad with Avocado & Gorgonzola",
            "descriptionEs": "Hojas verdes mixtas con cebolla morada, jitomate, tocino crujiente, aguacate fresco y queso gorgonzola desmoronado.",
            "descriptionEn": "Mixed greens topped with red onion, tomato, crisp bacon, fresh avocado, and tangy crumbled gorgonzola.",
            "price": 11.99,
            "category": "soups-salads",
            "allergens": ["Lácteos"]
        },
        {
            "id": "teriyaki-chicken-salad",
            "nameEs": "Ensalada de Pollo al Teriyaki con Manzana y Nueces",
            "nameEn": "Teriyaki Chicken Salad with Maple Mustard Dressing",
            "descriptionEs": "Mezcla de lechugas, rebanadas de manzana, arándanos y nueces con pollo marinado en teriyaki y aderezo de mostaza dulce con arce.",
            "descriptionEn": "Mixed greens, apple slices, cranberries, walnuts, and teriyaki chicken with sweet maple mustard dressing.",
            "price": 14.99,
            "category": "soups-salads",
            "allergens": ["Frutos secos", "Soja"]
        },
        {
            "id": "buffalo-chicken-salad",
            "nameEs": "Ensalada de Pollo Buffalo Crujiente con Queso Azul",
            "nameEn": "Crispy Buffalo Chicken Salad",
            "descriptionEs": "Lechuga romana, queso gorgonzola y jitomate cubiertos con pollo crujiente bañado en salsa picante Buffalo y aderezo de queso azul.",
            "descriptionEn": "Romaine lettuce, gorgonzola, and tomatoes topped with crispy Buffalo chicken and creamy blue cheese dressing.",
            "price": 14.99,
            "category": "soups-salads",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "grilled-steak-salad",
            "nameEs": "Ensalada de Filete de Res a la Parrilla con Gorgonzola",
            "nameEn": "Grilled Steak Salad with Gorgonzola",
            "descriptionEs": "Lechuga romana crujiente, jitomates maduros y cebolla morada con tiras de filete a la parrilla, queso gorgonzola y vinagreta balsámica.",
            "descriptionEn": "Crisp romaine, tomatoes, and red onions topped with tender grilled steak, crumbled gorgonzola, and balsamic vinaigrette.",
            "price": 15.99,
            "category": "soups-salads",
            "allergens": ["Lácteos"]
        },
        {
            "id": "chicken-caesar-salad",
            "nameEs": "Ensalada César con Pollo a la Parrilla",
            "nameEn": "Grilled Chicken Caesar Salad",
            "descriptionEs": "Corazones de lechuga romana, aderezo César cremoso, queso parmesano y crutones de hierbas con pechuga de pollo a la parrilla.",
            "descriptionEn": "Crisp romaine tossed in creamy Caesar dressing with parmesan, herb croutons, and grilled chicken breast.",
            "price": 12.99,
            "category": "soups-salads",
            "allergens": ["Gluten", "Lácteos", "Pescado"]
        },

        # --- ACOMPAÑAMIENTOS ---
        {
            "id": "hand-cut-fries",
            "nameEs": "Papas Fritas Caseras Cortadas a Mano",
            "nameEn": "Hand-Cut French Fries",
            "descriptionEs": "Papas naturales cortadas a mano en el pub y fritas dos veces para máxima textura crujiente dorada.",
            "descriptionEn": "Fresh natural potatoes cut by hand in-house, twice-fried for golden crunch.",
            "price": 6.50,
            "category": "sides"
        },
        {
            "id": "sweet-potato-fries",
            "nameEs": "Papas Fritas Dulces de Camote (Sweet Potato Fries)",
            "nameEn": "Crispy Sweet Potato Fries",
            "descriptionEs": "Bastones de camote dulce fritos crujientes, ligeramente salados.",
            "descriptionEn": "Crispy golden sweet potato fries served with sweet honey dip.",
            "price": 6.50,
            "category": "sides"
        },
        {
            "id": "crispy-onion-rings",
            "nameEs": "Aros de Cebolla Crujientes Dorados",
            "nameEn": "Golden Crispy Onion Rings",
            "descriptionEs": "Aros de cebolla dulce gruesos rebozados y fritos doraditos y crujientes.",
            "descriptionEn": "Thick-cut sweet onion rings battered and fried golden brown.",
            "price": 6.50,
            "category": "sides",
            "allergens": ["Gluten"]
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(items)} verified items to {dest}!")

if __name__ == "__main__":
    build_obriens()
