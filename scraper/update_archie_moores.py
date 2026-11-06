#!/usr/bin/env python3
import json
import os
import sys

def build_archie():
    dest = "data/merchants/archie-moores-bar-restaurant.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["storeInfo"]["name"] = "Archie Moore's Bar & Restaurant"
    data["storeInfo"]["address"] = "15 Factory Lane, Milford, CT 06460"
    data["storeInfo"]["tagline"] = "Connecticut’s Neighborhood Bar & Famous Buffalo Wings / Las Famosas Alitas Buffalo de Connecticut"
    data["storeInfo"]["phone"] = "(203) 876-5088"

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
        {"id": "famous-wings", "nameEs": "Nuestras Famosas Alitas Buffalo", "nameEn": "Famous Buffalo Wings", "icon": "Utensils"},
        {"id": "burgers", "nameEs": "Hamburguesas Gourmet (1/2 Libra)", "nameEn": "Gourmet Half-Pound Burgers", "icon": "Beef"},
        {"id": "sandwiches-wraps", "nameEs": "Sándwiches, Wraps y Grilled Cheese", "nameEn": "Sandwiches, Wraps & Melts", "icon": "Sandwich"},
        {"id": "starters-nachos", "nameEs": "Entrantes, Nachos y Piqueos", "nameEn": "Starters & Nachos", "icon": "Utensils"},
        {"id": "flatbreads", "nameEs": "Pizzas Rústicas Flatbread", "nameEn": "Stone Hearth Flatbreads", "icon": "Pizza"},
        {"id": "entrees", "nameEs": "Platos Fuertes y Costillas", "nameEn": "Entrées & Ribs", "icon": "Beef"},
        {"id": "salads", "nameEs": "Ensaladas Frescas", "nameEn": "Gourmet Salads", "icon": "Salad"},
        {"id": "sides", "nameEs": "Papas y Acompañamientos", "nameEn": "Signature Sides", "icon": "Utensils"}
    ]

    items = [
        # --- FAMOUS BUFFALO WINGS ---
        {
            "id": "famous-buffalo-wings-7",
            "nameEs": "Famosas Alitas Buffalo de Archie Moore's (7 piezas)",
            "nameEn": "Our Famous Buffalo Style Wings (7 pcs)",
            "descriptionEs": "Las legendarias alitas de Connecticut galardonadas nacionalmente, bañadas en la salsa Buffalo original de Archie Moore's, servidas con apio crujiente y abundante aderezo de queso azul casero.",
            "descriptionEn": "Connecticut's award-winning original Buffalo chicken wings tossed in Archie Moore's signature sauce, served with crisp celery and hearty house Bleu cheese dressing.",
            "price": 13.99,
            "category": "famous-wings",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "famous-buffalo-wings-14",
            "nameEs": "Famosas Alitas Buffalo de Archie Moore's (14 piezas)",
            "nameEn": "Our Famous Buffalo Style Wings (14 pcs)",
            "descriptionEs": "Catorce alitas jumbo jugosas bañadas en su salsa favorita: Buffalo Clásica, Buff-a-que, BBQ, Ajo Parmesano, Peach Chipotle, Raspberry Bourbon, Thai Chili o Honey Hot.",
            "descriptionEn": "Fourteen jumbo wings tossed in choice of sauce: Classic Buffalo, Buff-a-que, BBQ, Garlic Parmesan, Peach Chipotle, Raspberry Bourbon, Thai Chili, or Honey Hot.",
            "price": 25.99,
            "category": "famous-wings",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "famous-buffalo-wings-21",
            "nameEs": "Famosas Alitas Buffalo de Archie Moore's (21 piezas)",
            "nameEn": "Our Famous Buffalo Style Wings (21 pcs)",
            "descriptionEs": "Veintiuna alitas ideales para compartir con amigos, acompañadas de apio fresco y generoso aderezo Bleu cheese.",
            "descriptionEn": "Twenty-one famous jumbo wings served with crisp celery sticks and hearty house Bleu cheese.",
            "price": 37.99,
            "category": "famous-wings",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "boneless-wings-10",
            "nameEs": "Alitas Deshuesadas Boneless (10 piezas)",
            "nameEn": "Our Famous Boneless Wings (10 pcs)",
            "descriptionEs": "Diez tiernas piezas de pechuga de pollo 100% natural empanizadas doraditas y bañadas en su salsa de alitas favorita con aderezo Bleu cheese.",
            "descriptionEn": "Ten tender all-white meat boneless wings tossed in your choice of Archie's famous sauces, with celery and Bleu cheese.",
            "price": 14.99,
            "category": "famous-wings",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "boneless-wings-21",
            "nameEs": "Alitas Deshuesadas Boneless (21 piezas)",
            "nameEn": "Our Famous Boneless Wings (21 pcs)",
            "descriptionEs": "Veintiún bocados crujientes de pollo deshuesado bañados en salsa con apio y queso azul.",
            "descriptionEn": "Twenty-one crispy tender boneless wings tossed in signature wing sauce with celery and blue cheese dressing.",
            "price": 29.99,
            "category": "famous-wings",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "buffalo-chicken-dip",
            "nameEs": "Dip Cremoso Caliente de Pollo Buffalo",
            "nameEn": "Warm Buffalo Chicken Dip with Tortilla Chips",
            "descriptionEs": "Pollo deshebrado horneado y mezclado con queso azul cremoso y la famosa salsa de alitas Buffalo de Archie Moore's, servido caliente con totopos y apio.",
            "descriptionEn": "Shredded chicken baked with Bleu cheese and Archie's famous Buffalo wing sauce, served warm with tortilla chips and celery.",
            "price": 16.99,
            "category": "famous-wings",
            "allergens": ["Lácteos"],
            "popular": True
        },

        # --- BURGERS (Más de 1/2 libra de carne Angus con papas fritas y pepinillo) ---
        {
            "id": "traditional-cheeseburger",
            "nameEs": "Hamburguesa Tradicional con Queso (1/2 Libra)",
            "nameEn": "Traditional Half-Pound Cheeseburger",
            "descriptionEs": "Más de media libra de carne de res premium recién molida a la parrilla, con lechuga, jitomate y queso americano, suizo o cheddar en pan brioche tostado. Servida con papas y pepinillo.",
            "descriptionEn": "Over a half-pound of fresh ground 100% premium beef grilled to order, with lettuce, tomato, and choice of cheese. Served with French fries and a pickle.",
            "price": 16.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "mac-and-cheese-burger",
            "nameEs": "Hamburguesa con Macaroni & Cheese Casero",
            "nameEn": "House Mac & Cheese Burger",
            "descriptionEs": "Hamburguesa tradicional de media libra coronada con macarrones con queso cremosos hechos en casa, queso americano, cheddar fundido, lechuga y jitomate.",
            "descriptionEn": "Half-pound Angus burger topped with creamy house-made macaroni & cheese, sliced American and Cheddar cheeses, lettuce, and tomato.",
            "price": 18.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "jalapeno-burger",
            "nameEs": "Hamburguesa Jalapeño con Queso de Wisconsin",
            "nameEn": "Crispy Jalapeño Burger with Secret Sauce",
            "descriptionEs": "Carne de media libra cubierta con queso jalapeño derretido de Wisconsin, chiles jalapeños rebozados crujientes, salsa secreta de la casa, lechuga y jitomate.",
            "descriptionEn": "Topped with melted Wisconsin jalapeño cheese, beer-battered crunchy jalapeños, Archie's signature secret sauce, lettuce, and tomato.",
            "price": 18.50,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "bar-burger",
            "nameEs": "Hamburguesa Bar Burger con Tocino y Barbacoa",
            "nameEn": "Archie's Bar Burger with Bacon & BBQ",
            "descriptionEs": "Media libra de res con cebollas dulces a la plancha, tocino ahumado crujiente, salsa BBQ ahumada y queso cheddar derretido.",
            "descriptionEn": "Half-pound beef burger topped with grilled onions, crispy bacon, smoky barbecue sauce, and melted Cheddar cheese.",
            "price": 18.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "northfork-bison-burger",
            "nameEs": "Hamburguesa de Bisonte Northfork 100% Magro",
            "nameEn": "Northfork 100% Bison Burger",
            "descriptionEs": "Carne de bisonte americano 100% pura, tierna, magra y baja en grasa, cocinada a la parrilla con su elección de queso fundido, lechuga y jitomate.",
            "descriptionEn": "100% pure all-natural lean bison burger, grilled juicy and served with choice of cheese, lettuce, and tomato.",
            "price": 18.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "gyro-burger",
            "nameEs": "Hamburguesa Gyro Griega en Pan Plano con Tzatziki",
            "nameEn": "Greek Gyro Burger on Flatbread",
            "descriptionEs": "Hamburguesa sazonada con especias griegas servida en pan plano tostado con salsa de pepino tzatziki, queso feta, jitomate, cebolla, aceitunas kalamata y pepperoncini.",
            "descriptionEn": "Greek-seasoned beef patty folded in flatbread with cool cucumber tzatziki, feta cheese, lettuce, tomato, onion, Kalamata olives, and pepperoncini.",
            "price": 18.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "bruschetta-burger",
            "nameEs": "Hamburguesa Bruschetta en Pan Focaccia",
            "nameEn": "Bruschetta Burger on Artisan Focaccia",
            "descriptionEs": "Carne de media libra coronada con jitomates maduros, cebolla, albahaca fresca, aceite de oliva virgen extra y mozzarella fresca en pan focaccia.",
            "descriptionEn": "Half-pound burger topped with ripe diced tomatoes, onion, fresh basil, extra virgin olive oil, and fresh Mozzarella on toasted focaccia.",
            "price": 18.50,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "all-natural-veggie-burger",
            "nameEs": "Hamburguesa Vegetariana Artesanal",
            "nameEn": "All-Natural Vegetarian Burger",
            "descriptionEs": "Medallón vegetariano elaborado con granos y verduras naturales, servido con queso al gusto, lechuga fresca y jitomate.",
            "descriptionEn": "All-natural garden veggie patty served on a toasted bun with choice of cheese, crisp lettuce, and ripe tomato.",
            "price": 16.99,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "grilled-turkey-burger",
            "nameEs": "Hamburguesa de Pavo a la Parrilla",
            "nameEn": "Grilled Gourmet Turkey Burger",
            "descriptionEs": "Pechuga de pavo molida sazonada a las finas hierbas a la parrilla, con queso derretido, lechuga y jitomate.",
            "descriptionEn": "Lean seasoned ground turkey breast patty grilled to juicy perfection with choice of melted cheese, lettuce, and tomato.",
            "price": 17.50,
            "category": "burgers",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- SANDWICHES, WRAPS & SUPER GRILLED CHEESE ---
        {
            "id": "buffalo-chicken-wrap",
            "nameEs": "Wrap de Pollo Buffalo con Aderezo Bleu Cheese",
            "nameEn": "Buffalo Chicken Wrap",
            "descriptionEs": "Pollo crujiente marinado en la famosa salsa de alitas Buffalo de Archie, con lechuga fresca, jitomate y aderezo cremoso de queso azul. Con papas fritas.",
            "descriptionEn": "Crispy chicken tossed in Archie's Buffalo wing sauce, rolled with fresh lettuce, tomato, and creamy Bleu cheese dressing. With fries.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "chicken-caesar-wrap",
            "nameEs": "Wrap de Pollo César a la Parrilla",
            "nameEn": "Grilled Chicken Caesar Wrap",
            "descriptionEs": "Pechuga de pollo a la parrilla, lechuga romana crujiente, queso parmesano rallado, crutones y aderezo César cremoso.",
            "descriptionEn": "Grilled chicken breast tossed with crisp romaine, creamy Caesar dressing, chopped tomatoes, and garlic croutons.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Pescado"]
        },
        {
            "id": "grilled-chicken-pesto-wrap",
            "nameEs": "Wrap de Pollo al Pesto y Mozzarella Fresca",
            "nameEn": "Grilled Chicken Pesto Wrap",
            "descriptionEs": "Pechuga de pollo a la plancha, jitomates en cubos, salsa pesto aromática y queso mozzarella fresco.",
            "descriptionEn": "Tender grilled chicken breast, fresh Mozzarella cheese, diced ripe tomatoes, and fragrant basil pesto.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos", "Frutos secos"]
        },
        {
            "id": "sausalito-chicken-wrap",
            "nameEs": "Wrap Sausalito con Jalapeños y Monterey Jack",
            "nameEn": "Sausalito Grilled Chicken Wrap",
            "descriptionEs": "Pollo a la parrilla, queso Monterey Jack fundido, rodajas de jalapeños, salsa mexicana y crema agria.",
            "descriptionEn": "Grilled chicken, melted Monterey Jack cheese, spicy jalapeños, fresh salsa, and cool sour cream in a warm wrap.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "abc-grilled-cheese",
            "nameEs": "Super Grilled Cheese 'ABC' (Manzana, Tocino y Cheddar)",
            "nameEn": "The 'ABC' Gourmet Grilled Cheese Melt",
            "descriptionEs": "Pan de corte doblemente grueso tostado con mantequilla, relleno de rebanadas de manzana verde crujiente, tocino ahumado, queso cheddar añejo y queso gouda derretido.",
            "descriptionEn": "Double-thick artisan bread filled with crisp green apple slices, smoked bacon, melted Cheddar, and Gouda cheeses.",
            "price": 15.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "apizza-grilled-cheese",
            "nameEs": "Super Grilled Cheese 'Apizza' con Pepperoni y Ajo",
            "nameEn": "The 'Apizza' Pepperoni Garlic Melt",
            "descriptionEs": "Pan grueso dorado a la mantequilla de ajo, relleno de pepperoni de res, queso mozzarella derretido, cheddar y rebanadas de jitomate fresco.",
            "descriptionEn": "Grilled with garlic butter, stuffed with beef pepperoni, melted Mozzarella, Cheddar, and fresh tomato slices.",
            "price": 15.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "grilled-herb-chicken-sandwich",
            "nameEs": "Sándwich de Pollo a las Hierbas y Pimientos Asados",
            "nameEn": "Grilled Herb Chicken Sandwich",
            "descriptionEs": "Pechuga de pollo marinada en hierbas frescas con pimientos rojos asados y queso mozzarella derretido en panecillo tostado.",
            "descriptionEn": "Herb-marinated boneless chicken breast topped with roasted red peppers and melted Mozzarella cheese.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "charleston-bbq-chicken-sandwich",
            "nameEs": "Sándwich de Pollo Charleston con BBQ y Tocino",
            "nameEn": "Charleston Barbecue Chicken Sandwich",
            "descriptionEs": "Pechuga de pollo a la barbacoa con queso cheddar derretido, tocino crujiente, lechuga y jitomate.",
            "descriptionEn": "Barbecued chicken breast topped with melted Cheddar cheese, smoky bacon, fresh lettuce, and ripe tomato.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "pauls-chicken-sandwich",
            "nameEs": "Sándwich de Pollo de Paul con Pimientos y Cebolla",
            "nameEn": "Paul’s Chicken Sandwich with Sweet & Hot Peppers",
            "descriptionEs": "Pollo a la plancha con queso americano, pimientos dulces y picantes salteados y cebollas caramelizadas.",
            "descriptionEn": "Grilled chicken breast topped with melted American cheese, sautéed hot and sweet peppers, and grilled onions.",
            "price": 17.99,
            "category": "sandwiches-wraps",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- ENTRANTES Y NACHOS ---
        {
            "id": "nachos-grande",
            "nameEs": "Nachos Grande con Carne Especiada",
            "nameEn": "Archie Moore’s Nachos Grande",
            "descriptionEs": "Capas de totopos crujientes cubiertos con carne molida sazonada picante, cebollas, jitomate, jalapeños, aceitunas y queso Monterey Jack derretido con salsa y crema.",
            "descriptionEn": "Layered with seasoned spicy ground beef, onions, tomatoes, jalapeños, black olives, and melted Monterey Jack, served with salsa and sour cream.",
            "price": 17.99,
            "category": "starters-nachos",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "buffalo-nachos",
            "nameEs": "Nachos Buffalo de la Casa",
            "nameEn": "Archie Moore's Signature Buffalo Nachos",
            "descriptionEs": "Totopos de maíz cubiertos con pollo a la parrilla marinado en salsa Buffalo, jalapeños, jitomate, salsa, crema agria y aderezo Bleu cheese.",
            "descriptionEn": "Crispy nachos loaded with grilled chicken marinated in Buffalo wing sauce, jalapeños, diced tomatoes, salsa, sour cream, and Bleu cheese.",
            "price": 17.99,
            "category": "starters-nachos",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "fried-calamari",
            "nameEs": "Calamares Fritos con Salsa Marinara",
            "nameEn": "Golden Fried Calamari with Marinara",
            "descriptionEs": "Porción generosa de calamares ligeramente empanizados y fritos crujientes dorados, servidos con salsa marinara casera (estilo Buffalo disponible por $18.50).",
            "descriptionEn": "Generous portion of lightly breaded tender calamari fried golden brown, served with house marinara sauce.",
            "price": 17.99,
            "category": "starters-nachos",
            "allergens": ["Gluten", "Mariscos"]
        },
        {
            "id": "kung-pao-calamari",
            "nameEs": "Calamares Estilo Kung Pao con Chile Dulce y Cacahuates",
            "nameEn": "Kung Pao Sweet Chili Calamari",
            "descriptionEs": "Calamares fritos bañados en salsa agridulce sweet chili con rodajas de jalapeños rebozados, cacahuates tostados y cilantro fresco.",
            "descriptionEn": "Fried calamari tossed in sweet chili sauce with beer-battered jalapeños, crushed peanuts, and fresh cilantro.",
            "price": 18.50,
            "category": "starters-nachos",
            "allergens": ["Gluten", "Mariscos", "Frutos secos"],
            "popular": True
        },
        {
            "id": "burger-bites-6",
            "nameEs": "Mini Hamburguesas Burger Bites (6 piezas)",
            "nameEn": "Archie’s Burger Bites (6 mini burgers)",
            "descriptionEs": "Seis mini hamburguesas de res jugosas con queso americano derretido, lechuga y pepinillos.",
            "descriptionEn": "Six mini hamburgers topped with melted American cheese, shredded lettuce, and pickle chips.",
            "price": 19.99,
            "category": "starters-nachos",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "hot-garlic-pretzels",
            "nameEs": "Pretzels Horneados al Ajo con Queso y Mostaza Dulce (3 piezas)",
            "nameEn": "Hot Garlic Baked Jumbo Pretzels (3 pcs)",
            "descriptionEs": "Tres pretzels gigantes recién horneados con mantequilla de ajo, acompañados de salsa de queso caliente y mostaza con miel.",
            "descriptionEn": "Three baked jumbo garlic pretzels served warm with house cheese dipping sauce and honey mustard.",
            "price": 13.99,
            "category": "starters-nachos",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "golden-potato-skins",
            "nameEs": "Cáscaras de Papa Rellenas (Potato Skins)",
            "nameEn": "Golden Stuffed Potato Skins",
            "descriptionEs": "Papas doradas rellenas de tocino crujiente y queso cheddar derretido con crema agria (opción vegetariana de brócoli o estilo Buffalo disponibles).",
            "descriptionEn": "Crispy potato skins stuffed with smoky bacon and melted Cheddar cheese, served with sour cream.",
            "price": 15.99,
            "category": "starters-nachos",
            "allergens": ["Lácteos"]
        },

        # --- PIZZAS RÚSTICAS FLATBREAD ---
        {
            "id": "buffalo-chicken-flatbread",
            "nameEs": "Pizza Flatbread de Pollo Buffalo",
            "nameEn": "Buffalo Chicken Stone Hearth Flatbread",
            "descriptionEs": "Inspirada en las famosas alitas de la casa: masa horneada a la piedra cubierta con pollo Buffalo, ajo, queso mozzarella fundido y aderezo Bleu cheese.",
            "descriptionEn": "Stone hearth flatbread baked with Buffalo style chicken, garlic, bubbly Mozzarella, and served with house Bleu cheese dressing.",
            "price": 13.99,
            "category": "flatbreads",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "margherita-flatbread",
            "nameEs": "Pizza Flatbread Margherita Clásica",
            "nameEn": "Classic Margherita Flatbread",
            "descriptionEs": "Jitomates asados al horno, albahaca fresca picada y queso mozzarella fundido sobre masa rústica a la piedra.",
            "descriptionEn": "Stone hearth flatbread with sweet roasted tomatoes, fresh basil, and melted Mozzarella cheese.",
            "price": 12.99,
            "category": "flatbreads",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "tuscan-pepperoni-flatbread",
            "nameEs": "Pizza Flatbread de Pepperoni Toscano",
            "nameEn": "Tuscan Pepperoni Flatbread",
            "descriptionEs": "Pepperoni de res, aceite de oliva al ajo, quesos mozzarella, parmesano y cheddar sobre base crujiente.",
            "descriptionEn": "Beef pepperoni, garlic infused olive oil, melted Mozzarella, Parmesan, and Cheddar cheeses.",
            "price": 13.99,
            "category": "flatbreads",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "bruschetta-flatbread",
            "nameEs": "Pizza Flatbread Bruschetta con Glaseado Balsámico",
            "nameEn": "Bruschetta Flatbread with Balsamic Glaze",
            "descriptionEs": "Jitomates maduros picados, cebolla, albahaca fresca, quesos mozzarella y parmesano terminada con reducción balsámica dulce.",
            "descriptionEn": "Fresh diced tomatoes, onion, basil, Mozzarella, Parmesan, olive oil, and sweet balsamic reduction glaze.",
            "price": 12.99,
            "category": "flatbreads",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- PLATOS FUERTES Y COSTILLAS ---
        {
            "id": "baby-back-ribs-full-rack",
            "nameEs": "Costillar Completo de Costillitas Baby Back (Full Rack)",
            "nameEn": "Full Rack of Danish Baby Back Ribs",
            "descriptionEs": "Costillar entero de costillitas danesas ahumadas a fuego lento, barnizadas con salsa barbacoa de la casa, servidas con papas fritas y ensalada de col.",
            "descriptionEn": "Full rack of tender Danish pork ribs smoked slow and basted with Archie's house barbecue sauce, served with French fries and coleslaw.",
            "price": 25.99,
            "category": "entrees",
            "popular": True
        },
        {
            "id": "beer-battered-fish-and-chips",
            "nameEs": "Fish & Chips de Bacalao al Rebozado de Cerveza",
            "nameEn": "House Favorite Fish & Chips",
            "descriptionEs": "Filetes frescos de bacalao rebozados en masa de cerveza artesanal fritos crujientes, servidos con papas fritas, ensalada coleslaw y salsa tártara.",
            "descriptionEn": "A house favorite: beer-battered fresh cod fillets fried crispy and golden, served with French fries, coleslaw, and tartar sauce.",
            "price": 18.99,
            "category": "entrees",
            "allergens": ["Gluten", "Pescado", "Huevos"],
            "popular": True
        },
        {
            "id": "clam-strip-platter",
            "nameEs": "Platón de Tiras de Almeja de Nueva Inglaterra (Clam Strips)",
            "nameEn": "New England Clam Strip Platter",
            "descriptionEs": "Tiras tiernas de almeja dulce de Nueva Inglaterra ligeramente empanizadas y doradas crujientes, con papas fritas, ensalada coleslaw y salsa tártara.",
            "descriptionEn": "Tender sweet New England clam strips lightly breaded and fried golden, served with French fries, coleslaw, and tartar sauce.",
            "price": 23.99,
            "category": "entrees",
            "allergens": ["Gluten", "Mariscos"]
        },
        {
            "id": "fajita-bowl",
            "nameEs": "Tazón Fajita Bowl (Pollo, Bistec, Camarón o Portobello)",
            "nameEn": "Sizzling Fajita Bowl",
            "descriptionEs": "Pimientos dulces y cebollas salteadas sobre arroz sazonado, cubierto con jalapeños, jitomates, aceitunas y queso rallado, servido con salsa y crema agria.",
            "descriptionEn": "Sautéed bell peppers and onions over seasoned rice, topped with jalapeños, tomatoes, black olives, and melted shredded cheese, with salsa and sour cream.",
            "price": 19.99,
            "category": "entrees",
            "allergens": ["Lácteos"]
        },

        # --- ENSALADAS ---
        {
            "id": "apple-salad-chicken",
            "nameEs": "Ensalada de Manzana, Pollo Asado y Nueces con Miel de Arce",
            "nameEn": "Signature Apple & Maple Walnut Salad with Chicken",
            "descriptionEs": "Pechuga de pollo a la plancha sobre lechugas tiernas, manzanas verdes crujientes, queso cheddar, nueces caramelizadas con arce, arándanos secos y semillas de calabaza con vinagreta de manzana.",
            "descriptionEn": "Grilled chicken, baby greens, crisp green apples, Cheddar, maple-glazed walnuts, dried cranberries, pumpkin seeds, and sunflower seeds with apple vinaigrette.",
            "price": 19.99,
            "category": "salads",
            "allergens": ["Lácteos", "Frutos secos"],
            "popular": True
        },
        {
            "id": "cobb-salad",
            "nameEs": "Ensalada Cobb Completa con Pollo y Gorgonzola",
            "nameEn": "Archie’s Classic Cobb Salad",
            "descriptionEs": "Pollo a la plancha en cubos, tocino crocante, jitomate, cebolla, aguacate fresco, huevo cocido y queso gorgonzola sobre lechuga romana fresca.",
            "descriptionEn": "Diced grilled chicken, crisp bacon, tomato, red onion, fresh avocado, hard-boiled egg, and crumbled Gorgonzola over Romaine lettuce.",
            "price": 19.99,
            "category": "salads",
            "allergens": ["Huevos", "Lácteos"],
            "popular": True
        },
        {
            "id": "spinach-salad",
            "nameEs": "Ensalada de Espinacas Frescas con Tocino y Huevo",
            "nameEn": "Fresh Baby Spinach Salad with Warm Bacon Dressing",
            "descriptionEs": "Espinacas tiernas con huevo en rebanadas, tocino desmoronado, champiñones frescos en láminas, crutones de ajo, cebolla morada y aderezo cremoso de tocino.",
            "descriptionEn": "Baby spinach with sliced egg, crumbled bacon, fresh mushrooms, garlic croutons, Bermuda onion, and creamy bacon dressing.",
            "price": 17.50,
            "category": "salads",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "sesame-chicken-salad",
            "nameEs": "Ensalada de Pollo al Ajonjolí y Mandarinas",
            "nameEn": "Sesame Ginger Chicken Salad",
            "descriptionEs": "Pollo marinado a la plancha sobre mezcla de hojas verdes con almendras tostadas, gajos de mandarina dulce y aderezo de sésamo y jengibre.",
            "descriptionEn": "Grilled marinated chicken over tender field greens with toasted sliced almonds, sweet Mandarin oranges, and sesame ginger dressing.",
            "price": 19.99,
            "category": "salads",
            "allergens": ["Frutos secos", "Sésamo"]
        },

        # --- SIGNATURE SIDES ---
        {
            "id": "eggplant-fries",
            "nameEs": "Papas Fritas de Berenjena con Queso Parmesano",
            "nameEn": "Parmesan Dusted Eggplant Fries",
            "descriptionEs": "Bastones de berenjena fresca empanizados y fritos crujientes, espolvoreados con queso parmesano y servidos con salsa marinara.",
            "descriptionEn": "Crispy eggplant fries dusted with grated Parmesan cheese, served with warm house marinara sauce.",
            "price": 9.99,
            "category": "sides",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "french-fried-onion-rings",
            "nameEs": "Aros de Cebolla Fritos con Salsa Secreta",
            "nameEn": "Crispy French Fried Onion Rings with Secret Sauce",
            "descriptionEs": "Aros de cebolla gruesos rebozados y fritos doraditos servidos con la famosa salsa secreta de Archie Moore's.",
            "descriptionEn": "Thick-cut battered onion rings fried golden brown, served with Archie's legendary house secret sauce.",
            "price": 10.99,
            "category": "sides",
            "allergens": ["Gluten"]
        },
        {
            "id": "waffle-fries",
            "nameEs": "Papas Rejilla Waffle Fries",
            "nameEn": "Seasoned Crispy Waffle Fries",
            "descriptionEs": "Papas doradas enrejadas crocantes con sazón especial.",
            "descriptionEn": "Golden crisp seasoned waffle-cut french fries.",
            "price": 9.99,
            "category": "sides"
        },
        {
            "id": "bacon-cheese-fries",
            "nameEs": "Papas Fritas Cargadas con Queso y Tocino",
            "nameEn": "Loaded Bacon & Melted Cheese Fries",
            "descriptionEs": "Papas fritas crujientes bañadas en queso derretido y trocitos abundantes de tocino ahumado crocante.",
            "descriptionEn": "Hot french fries smothered in melted Monterey Jack and Cheddar cheeses and crispy bacon crumbles.",
            "price": 12.99,
            "category": "sides",
            "allergens": ["Lácteos"]
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(items)} verified items to {dest}!")

if __name__ == "__main__":
    build_archie()
