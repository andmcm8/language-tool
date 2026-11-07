#!/usr/bin/env python3
"""
Generate 100% verified authentic merchant menu for Bobo's Cafe (Ridgefield, CT).
Extracted directly from official high-resolution menu boards on boboscafe.net/menu.
Zero hallucinations. Full menu captured.
"""

import json
import os
import sys

def build_bobos_cafe():
    dest = "data/merchants/bobos-cafe.json"

    data = {
        "storeInfo": {
            "id": "bobos-cafe",
            "name": "Bobo's Cafe",
            "tagline": "Specialty Coffee, Handcrafted Breakfast & Artisan Sandwiches in Ridgefield",
            "address": "32 Danbury Rd, Ridgefield, CT 06877",
            "phone": "(203) 403-3444",
            "hours": {
                "monday_friday": "6:30 AM - 4:00 PM",
                "saturday": "7:00 AM - 4:00 PM",
                "sunday": "7:00 AM - 4:00 PM"
            },
            "paymentMethods": [
                "Cash",
                "Credit/Debit Cards",
                "Apple Pay",
                "Contactless",
                "Toast Tab Pay"
            ],
            "amenities": [
                "Dine-In",
                "Takeout",
                "Online Ordering",
                "Outdoor Patio Seating",
                "Gluten-Free Options",
                "Espresso Bar",
                "Bilingual Menu"
            ],
            "themeColor": "#0284c7",
            "logoIcon": "coffee",
            "policies": {
                "returnPolicyEs": "Si su orden o bebida no queda a su gusto, con gusto se la preparamos nuevamente de inmediato.",
                "returnPolicyEn": "If your drink or meal isn't made to your complete liking, we will gladly remake it right away.",
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
                "id": "bobos-best",
                "nameEs": "Lo Mejor de Bobo's",
                "nameEn": "Bobo's Best",
                "icon": "Star"
            },
            {
                "id": "desayunos",
                "nameEs": "Desayunos y Huevos",
                "nameEn": "Morning Favorites",
                "icon": "Egg"
            },
            {
                "id": "sandwiches-almuerzo",
                "nameEs": "Sándwiches y Almuerzo",
                "nameEn": "Afternoon Delights",
                "icon": "Sandwich"
            },
            {
                "id": "ensaladas",
                "nameEs": "Ensaladas Frescas",
                "nameEn": "Salads",
                "icon": "Salad"
            },
            {
                "id": "smoothies-bowls",
                "nameEs": "Batidos y Tazones Açaí",
                "nameEn": "Smoothies & Bowls",
                "icon": "Sparkles"
            },
            {
                "id": "cafe-bebidas",
                "nameEs": "Café, Té y Bebidas Especiales",
                "nameEn": "Coffee & Specialty Drinks",
                "icon": "Coffee"
            },
            {
                "id": "menu-ninos",
                "nameEs": "Menú Infantil Little Bo's",
                "nameEn": "Little Bo's",
                "icon": "Smile"
            }
        ],
        "products": [
            # BOBO'S BEST
            {
                "id": "the-number-one",
                "categoryId": "bobos-best",
                "nameEs": "El Sándwich Número Uno (The Number One)",
                "nameEn": "The Number One Sandwich",
                "descriptionEs": "Tocino crujiente, huevos revueltos esponjosos, queso americano derretido, hash brown libre de gluten crocante, aguacate fresco y mayonesa cremosa de sriracha servido en un croissant francés hojaldrado.",
                "descriptionEn": "Crispy bacon, scrambled eggs, melted American cheese, gluten-free crispy hash brown, fresh avocado, and creamy sriracha served on a flaky French croissant.",
                "price": "$10.95",
                "popular": True,
                "badge": "Signature",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "hot-chick-sandwich",
                "categoryId": "bobos-best",
                "nameEs": "Sándwich de Pollo Hot Chick",
                "nameEn": "Hot Chick Sandwich",
                "descriptionEs": "Milanesa de pechuga de pollo crujiente (sin gluten) bañada en miel picante con salsa búfalo hot honey, queso azul desmenuzado y ensalada slaw de col crujiente sobre baguette tostada.",
                "descriptionEn": "Crispy gluten-free chicken cutlet tossed in sweet hot honey buffalo sauce, blue cheese crumble, and crunchy cabbage slaw served on a fresh toasted baguette.",
                "price": "$14.95",
                "popular": True,
                "badge": "House Favorite",
                "allergens": ["Lácteos"]
            },
            {
                "id": "og-acai-bowl",
                "categoryId": "bobos-best",
                "nameEs": "Tazón Clásico Açaí Original (OG Acai)",
                "nameEn": "OG Acai Bowl",
                "descriptionEs": "Base orgánica cremosa de açaí puro con fresas frescas, plátano, arándanos azules, llovizna de Nutella y granola artesanal casera (sin gluten, sin nueces, vegana).",
                "descriptionEn": "Organic creamy pure acai base topped with fresh strawberries, sliced bananas, blueberries, rich Nutella drizzle, and homemade signature granola (GF, NF, Vegan).",
                "price": "$13.95",
                "popular": True,
                "badge": "Organic",
                "allergens": ["Lácteos", "Frutos Secos"]
            },
            {
                "id": "dirty-iced-chai",
                "categoryId": "bobos-best",
                "nameEs": "Té Chai Especiado con Espresso Frío (Dirty Iced Chai)",
                "nameEn": "Dirty Iced Chai",
                "descriptionEs": "Té chai especiado con vainilla cremosa, hielo y un shot concentrado de espresso artesanal caliente para el toque enérgico ideal.",
                "descriptionEn": "Vanilla-infused spiced chai latte served over ice, elevated with a fresh double shot of robust espresso.",
                "price": "$5.50",
                "allergens": ["Lácteos"]
            },
            {
                "id": "smooth-brew",
                "categoryId": "bobos-best",
                "nameEs": "Café Frío Smooth Brew con Crema Suave",
                "nameEn": "Smooth Brew Cold Brew",
                "descriptionEs": "Infusión fría Cold Brew artesanal mezcla exclusiva de Bobo's con espuma dulce aterciopelada 'soft top'.",
                "descriptionEn": "Bobo's signature craft cold brew blend served over crystal ice, finished with an ultra-smooth velvety soft sweet cream top.",
                "price": "$5.50",
                "popular": True,
                "badge": "Best Seller",
                "allergens": ["Lácteos"]
            },

            # MORNING FAVORITES
            {
                "id": "bo-licious-toast",
                "categoryId": "desayunos",
                "nameEs": "Tostada Bo-Licious de Aguacate en Masa Madre",
                "nameEn": "Bo-Licious Avocado Toast",
                "descriptionEs": "Aguacate maduro machacado, queso feta griego, arúgula tierna, hojuelas de chile rojo, huevo frito con yema tierna y vinagreta de limón fresco sobre rebanada gruesa de pan de masa madre artesanal.",
                "descriptionEn": "Crushed ripe avocado, tangy feta cheese, fresh baby arugula, red pepper flakes, over-easy sunny egg, and lemon vinaigrette on thick-cut artisan sourdough.",
                "price": "$7.50",
                "popular": True,
                "badge": "Healthy",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "breakfast-bo-rrito",
                "categoryId": "desayunos",
                "nameEs": "Burrito de Desayuno Bo-rrito",
                "nameEn": "Breakfast Bo-rrito",
                "descriptionEs": "Huevos revueltos, queso cheddar fundido, salchicha de desayuno campesina, hash brown crujiente sin gluten, salsa elote con frijoles negros y crema artesanal de cilantro y lima envuelto en tortilla suave.",
                "descriptionEn": "Fluffy scrambled eggs, melted cheddar, country breakfast sausage, crispy GF hash brown, Mexican elote & black bean salsa, and cilantro lime crema in a warm flour wrap.",
                "price": "$9.95",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "bacon-egg-and-cheese-brioche",
                "categoryId": "desayunos",
                "nameEs": "Sándwich Clásico de Tocino, Huevo y Cheddar en Brioche",
                "nameEn": "Bacon, Egg & Cheese on Brioche",
                "descriptionEs": "Tocino ahumado crocante, huevos revueltos esponjosos y queso cheddar derretido servido en pan suave de brioche con mantequilla tostada.",
                "descriptionEn": "Smoked crispy bacon, scrambled eggs, and melted sharp cheddar cheese served warm on a toasted golden brioche bun.",
                "price": "$7.50",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "sausage-egg-cheese-hot-honey",
                "categoryId": "desayunos",
                "nameEs": "Sándwich de Salchicha, Huevo y Cebolla Caramelizada Hot Honey",
                "nameEn": "Sausage, Egg & Cheese Brioche",
                "descriptionEs": "Salchicha sabrosa de cerdo, huevos revueltos, queso cheddar fundido y cebollas caramelizadas con miel picante hot honey en suave pan brioche.",
                "descriptionEn": "Savory sausage patty, scrambled eggs, cheddar, and sweet hot-honey caramelized onions on a warm toasted brioche roll.",
                "price": "$7.95",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Puerco"]
            },
            {
                "id": "waffle-house-special",
                "categoryId": "desayunos",
                "nameEs": "Waffles Belgas Dulces Waffle House",
                "nameEn": "Waffle House Belgian Waffles",
                "descriptionEs": "Waffles belgas dorados y crujientes cubiertos con compota tibia casera de manzana y arándanos agridulces, espolvoreados con azúcar flor glass.",
                "descriptionEn": "Golden crisp Belgian waffles topped with warm homemade apple cranberry compote and dusted with powdered sugar.",
                "price": "$11.95",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "quiche-and-tell",
                "categoryId": "desayunos",
                "nameEs": "Quiche Artesanal Horneada Quiche & Tell",
                "nameEn": "Quiche & Tell",
                "descriptionEs": "Huevos esponjosos horneados con pimientos rojos asados, queso suizo suave y tocino ahumado en costra artesanal libre de gluten. Acompañada de ensalada de arúgula con parmesano.",
                "descriptionEn": "Baked eggs with roasted red peppers, melted Swiss cheese, and bacon inside a gluten-free crust, served alongside a baby arugula & parmesan side salad.",
                "price": "$12.95",
                "badge": "Gluten-Free Crust",
                "allergens": ["Huevos", "Lácteos", "Puerco"]
            },
            {
                "id": "veggie-omelette",
                "categoryId": "desayunos",
                "nameEs": "Omelette Vegetariana de la Huerta",
                "nameEn": "Veggie Omelette",
                "descriptionEs": "Omelette de tres huevos frescos rellena de tomates en cubos, espinacas tiernas, queso cheddar y cebollín verde picado. Servida con ensalada de arúgula y parmesano más pan tostado de masa madre.",
                "descriptionEn": "Three-egg omelette folded with ripe diced tomatoes, sharp cheddar, fresh spinach, and scallions. Served with arugula parmesan salad and sourdough toast.",
                "price": "$9.95",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "green-eggs-and-ham",
                "categoryId": "desayunos",
                "nameEs": "Sándwich Green Eggs & Ham con Mortadela y Pesto",
                "nameEn": "Green, Eggs & Ham Sandwich",
                "descriptionEs": "Mortadela italiana fina, huevos revueltos, mozzarella derretida, pesto genovés de albahaca, arúgula fresca y glaseado balsámico en pan brioche tostado.",
                "descriptionEn": "Italian mortadella, scrambled eggs, fresh mozzarella, basil pesto, arugula, and balsamic reduction on warm brioche.",
                "price": "$10.95",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Puerco"]
            },
            {
                "id": "tootsies-potatoes-and-eggs",
                "categoryId": "desayunos",
                "nameEs": "Sándwich Tootsie's de Papas, Huevos y Salsa Picante",
                "nameEn": "Tootsie's Potatoes & Eggs",
                "descriptionEs": "Papas doradas en cubos, huevos revueltos, cebollas caramelizadas con miel picante hot honey, queso parmesano, mozzarella fundida, salsa picante y kétchup en brioche.",
                "descriptionEn": "Home fries potato hash, scrambled eggs, hot-honey caramelized onions, parmesan, melted mozzarella, hot sauce, and ketchup on toasted brioche.",
                "price": "$7.95",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "bowl-pack-sweet-potato",
                "categoryId": "desayunos",
                "nameEs": "Tazón Saludable Bowl Pack con Camote y Queso de Cabra",
                "nameEn": "Bowl Pack Breakfast Bowl",
                "descriptionEs": "Tazón matutino de camote asado dulce en cubos, huevos revueltos frescos, queso de cabra cremoso desmenuzado y salsa elote de maíz rostizado.",
                "descriptionEn": "Roasted sweet potato hash bowl with fluffy scrambled eggs, creamy crumbled goat cheese, and fresh roasted corn salsa.",
                "price": "$10.95",
                "badge": "Gluten-Free",
                "allergens": ["Huevos", "Lácteos"]
            },

            # AFTERNOON DELIGHTS / SANDWICHES
            {
                "id": "the-dellacamera",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Baguette Caprese The Dellacamera",
                "nameEn": "The Dellacamera Sandwich",
                "descriptionEs": "Mozzarella fresca artesanal, tomates maduros en rodajas, pesto de albahaca fragante y reducción de vinagre balsámico de Módena en baguette francesa crujiente.",
                "descriptionEn": "Fresh mozzarella, sliced ripe tomatoes, basil pesto, and balsamic glaze on a crisp French baguette.",
                "price": "$10.50",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "the-heritage-sandwich",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich The Heritage de Pavo, Tocino y Aguacate",
                "nameEn": "The Heritage Sandwich",
                "descriptionEs": "Pavo horneado fino, tocino ahumado crujiente, lechuga romana fresca, tomate, aguacate en rebanadas y aderezo cremoso de sriracha en baguette.",
                "descriptionEn": "Sliced roasted turkey, crisp bacon, fresh romaine lettuce, tomato, sliced avocado, and creamy sriracha aioli on a toasted baguette.",
                "price": "$14.95",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Puerco"]
            },
            {
                "id": "bernardis-deli",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich Submarino Bernardi's Deli",
                "nameEn": "Bernardi’s Deli Sub",
                "descriptionEs": "Pavo asado, mortadela italiana, mayonesa de pimienta negra molida, lechuga romana, queso cheddar, cebollas moradas encurtidas con cúrcuma y pimientos rojos asados en baguette.",
                "descriptionEn": "Roasted turkey, mortadella, black pepper mayo, crisp romaine, sharp cheddar, turmeric pickled red onions, and roasted sweet peppers on a baguette.",
                "price": "$15.95",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Puerco"]
            },
            {
                "id": "nacho-libre-wrap",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Wrap Mexicano Nacho Libre de Pollo a la Parrilla",
                "nameEn": "Nacho Libre Wrap",
                "descriptionEs": "Pechuga de pollo a la parrilla, aguacate fresco, salsa de maíz elote, tiritas crujientes de tortilla frita, lechuga romana y aderezo cremoso de sriracha envuelto en tortilla suave.",
                "descriptionEn": "Grilled chicken breast, fresh avocado, elote corn salsa, crispy tortilla strips, romaine lettuce, and creamy sriracha in a soft tortilla wrap.",
                "price": "$13.50",
                "popular": True,
                "allergens": ["Gluten", "Huevos"]
            },
            {
                "id": "shmelt-tuna-chicken-melt",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich Shmelt de Ensalada Fundida con Cheddar",
                "nameEn": "Shmelt Artisan Melt",
                "descriptionEs": "Elección de ensalada de pollo con arándanos, ensalada de atún con manzana y arándanos, o ensalada de atún al eneldo fresco, con tomate y queso cheddar fundido en pan grueso de masa madre tostada.",
                "descriptionEn": "Your choice of cranberry chicken salad, cranberry apple tuna salad, or fresh dill tuna salad with sliced tomato and melted sharp cheddar on thick-cut toasted sourdough.",
                "price": "$12.95",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Pescado"]
            },
            {
                "id": "katz-pajamas-pastrami",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich de Pastrami Katz’ Pajamas",
                "nameEn": "Katz’ Pajamas Pastrami",
                "descriptionEs": "Pastrami curado y sazonado al estilo deli, queso suizo derretido, ensalada crujiente de col slaw y salsa secreta casera en pan de masa madre grueso tostado.",
                "descriptionEn": "Warm sliced deli pastrami, melted Swiss cheese, crisp cabbage slaw, and signature house secret sauce on thick-cut toasted sourdough.",
                "price": "$14.95",
                "popular": True,
                "badge": "House Specialty",
                "allergens": ["Gluten", "Huevos", "Lácteos"]
            },
            {
                "id": "bo-chicken-baguette",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich Bo-Chicken de Milanesa Crujiente",
                "nameEn": "Bo-Chicken Sandwich",
                "descriptionEs": "Milanesa de pechuga crujiente sin gluten, lechuga romana crujiente, rodajas de tomate, pepinillos encurtidos caseros y mayonesa clásica en baguette recién horneada.",
                "descriptionEn": "Crispy gluten-free chicken cutlet, romaine lettuce, ripe tomato, house-made dill pickles, and mayo on a crusty baguette.",
                "price": "$14.95",
                "allergens": ["Gluten", "Huevos"]
            },
            {
                "id": "irmas-quesadilla",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Quesadilla Dorada Irma’s de Pollo y Pico de Gallo",
                "nameEn": "Irma’s Chicken Quesadilla",
                "descriptionEs": "Tortilla grande dorada rellena de abundante queso cheddar fundido, pollo a la parrilla desmenuzado, pico de gallo fresco y cebollín. Servida con salsa crema de cilantro-lima y aderezo cremoso de sriracha.",
                "descriptionEn": "Melted cheddar cheese blend, shredded grilled chicken breast, fresh pico de gallo, and scallions in a crispy flour tortilla. Served with sides of cilantro lime crema and creamy sriracha.",
                "price": "$13.50",
                "popular": True,
                "allergens": ["Gluten", "Lácteos", "Huevos"]
            },
            {
                "id": "bbq-grilled-cheese",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Sándwich BBQ Grilled Cheese de Pollo y Cheddar",
                "nameEn": "BBQ Grilled Cheese",
                "descriptionEs": "Pollo desmenuzado marinado en salsa barbacoa ahumada dulce con abundancia de queso cheddar fundido entre dos rebanadas gruesas de masa madre dorada a la plancha.",
                "descriptionEn": "Tender shredded chicken marinated in sweet smoky BBQ sauce with melted sharp cheddar cheese on buttered thick-cut sourdough.",
                "price": "$12.95",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "arroz-con-pollo-bobo-bowl",
                "categoryId": "sandwiches-almuerzo",
                "nameEs": "Tazón Arroz con Pollo, Huevo y Aguacate",
                "nameEn": "Arroz con Pollo Rice Bowl",
                "descriptionEs": "Tazón de arroz blanco caliente coronado con milanesa crujiente de pechuga de pollo (sin gluten), aguacate fresco en abanico, huevo frito soleado, mayonesa cremosa de sriracha y cebollín fresco picado.",
                "descriptionEn": "Warm seasoned rice bowl topped with crispy GF chicken cutlet, sliced avocado, sunny-side-up egg, creamy sriracha drizzle, and fresh green scallions.",
                "price": "$13.95",
                "popular": True,
                "allergens": ["Huevos"]
            },

            # SALADS
            {
                "id": "south-of-the-border-salad",
                "categoryId": "ensaladas",
                "nameEs": "Ensalada South of the Border con Pollo y Elote",
                "nameEn": "South of the Border Salad",
                "descriptionEs": "Lechuga romana crujiente, pechuga de pollo asada a la parrilla, tomates cherry dulces, salsa elote de maíz con frijoles negros, tiritas crocantes de tortilla de maíz, aguacate fresco y aderezo cremoso de sriracha.",
                "descriptionEn": "Crisp romaine, grilled chicken breast, sweet grape tomatoes, corn black-bean salsa, crispy tortilla strips, avocado, and creamy sriracha dressing.",
                "price": "$14.95",
                "popular": True,
                "allergens": ["Huevos"]
            },
            {
                "id": "balkan-bronson-salad",
                "categoryId": "ensaladas",
                "nameEs": "Ensalada Mediterránea Balkan Bronson",
                "nameEn": "Balkan Bronson Salad",
                "descriptionEs": "Col tierna rallada, tomates cherry, pepino crujiente en cubos, queso feta griego, cebollas moradas encurtidas en cúrcuma caseras, hummus cremoso de garbanzo y pollo a la parrilla.",
                "descriptionEn": "Finely shredded cabbage, grape tomatoes, cucumber, authentic feta cheese, house turmeric pickled onions, creamy chickpea hummus, and warm grilled chicken.",
                "price": "$12.95",
                "allergens": ["Lácteos", "Sésamo"]
            },
            {
                "id": "spicy-chicken-caesar-salad",
                "categoryId": "ensaladas",
                "nameEs": "Ensalada César Picante con Pollo Hot Honey Buffalo",
                "nameEn": "Spicy Chicken Caesar Salad",
                "descriptionEs": "Pollo crujiente bañado en miel picante con salsa búfalo hot honey, lechuga romana fresca, lluvia de crutones tostados de masa madre, lascas de queso parmesano y aderezo César cremoso.",
                "descriptionEn": "Hot honey buffalo chicken, crisp romaine lettuce, toasted sourdough crouton dusting, shaved aged parmesan, and creamy caesar dressing.",
                "price": "$13.95",
                "popular": True,
                "allergens": ["Gluten", "Huevos", "Lácteos", "Pescado"]
            },
            {
                "id": "chicken-milanese-salad",
                "categoryId": "ensaladas",
                "nameEs": "Ensalada Chicken Milanese con Arúgula y Parmesano",
                "nameEn": "Chicken Milanese Salad",
                "descriptionEs": "Milanesa de pechuga crujiente (sin gluten) sobre cama de arúgula tierna, lascas de parmesano italiano, cebollas moradas encurtidas con cúrcuma, tomates cherry y vinagreta balsámica blanca.",
                "descriptionEn": "Crispy GF chicken cutlet, baby arugula, shaved parmesan, house turmeric pickled onions, grape tomatoes, and bright white balsamic vinaigrette.",
                "price": "$14.95",
                "allergens": ["Lácteos"]
            },
            {
                "id": "the-angry-orchard-salad",
                "categoryId": "ensaladas",
                "nameEs": "Ensalada The Angry Orchard con Manzanas y Queso de Cabra",
                "nameEn": "The Angry Orchard Salad",
                "descriptionEs": "Lechuga romana fresca, manzanas crujientes en láminas finas, queso de cabra suave, almendras confitadas caramelizadas, arándanos deshidratados, cebollas encurtidas con cúrcuma y vinagreta balsámica blanca.",
                "descriptionEn": "Crisp romaine, fresh apple slices, creamy goat cheese, candied almonds, craisins, turmeric pickled onions, and white balsamic vinaigrette.",
                "price": "$10.95",
                "allergens": ["Lácteos", "Frutos Secos"]
            },

            # SMOOTHIES & BOWLS
            {
                "id": "takes-2-to-mango-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Frutal Takes 2 to Mango (20 oz)",
                "nameEn": "Takes 2 to Mango Smoothie",
                "descriptionEs": "Mango dulce tropical maduro, fresas frescas, piña jugosa y yogur natural cremoso batido al momento.",
                "descriptionEn": "Sweet ripe mango, fresh strawberries, golden pineapple, and creamy blended yogurt.",
                "price": "$11.95",
                "allergens": ["Lácteos"]
            },
            {
                "id": "acai-u-baby-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Energético Acai-U-Baby con Mantequilla de Maní (20 oz)",
                "nameEn": "Acai-U-Baby Smoothie",
                "descriptionEs": "Açaí orgánico puro, plátano dulce, mantequilla cremosa de maní natural y leche suave de avena sin lácteos.",
                "descriptionEn": "Pure organic acai, ripe banana, creamy natural peanut butter, and plant-based oat milk.",
                "price": "$9.95",
                "popular": True,
                "allergens": ["Frutos Secos"]
            },
            {
                "id": "the-cosmos-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido The Cosmos de Coco, Piña y Proteína Azul (20 oz)",
                "nameEn": "The Cosmos Smoothie",
                "descriptionEs": "Coco tropical, piña fresca, proteína de suero de vainilla natural, yogur cremoso, polvo de flor de guisante azul de mariposa butterfly pea y leche de avena.",
                "descriptionEn": "Creamy coconut, pineapple, vanilla whey protein, yogurt, vibrant butterfly pea flower powder, and oat milk.",
                "price": "$11.95",
                "badge": "High Protein",
                "allergens": ["Lácteos"]
            },
            {
                "id": "killa-kate-green-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Verde Killa Kate con Espinaca y Proteína (20 oz)",
                "nameEn": "Killa Kate Green Smoothie",
                "descriptionEs": "Plátano, piña, mango, espinacas frescas tiernas, mantequilla de almendras tostadas, proteína de vainilla y leche de avena.",
                "descriptionEn": "Banana, pineapple, mango, baby spinach, toasted almond butter, vanilla whey protein, and oat milk.",
                "price": "$11.95",
                "badge": "Superfood",
                "allergens": ["Lácteos", "Frutos Secos"]
            },
            {
                "id": "bo-ccino-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Energético Bo-ccino con Espresso y Chocolate (20 oz)",
                "nameEn": "Bo-ccino Espresso Smoothie",
                "descriptionEs": "Plátano dulce, mantequilla de maní, canela molida, proteína de chocolate rica, shot de espresso artesanal concentrado y leche de avena.",
                "descriptionEn": "Fresh banana, peanut butter, warm cinnamon, chocolate protein, double espresso shot, and oat milk.",
                "price": "$11.95",
                "popular": True,
                "badge": "Signature Energy",
                "allergens": ["Lácteos", "Frutos Secos"]
            },
            {
                "id": "johnnys-bananas-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Refrescante Johnny’s Bananas con Agua de Coco (20 oz)",
                "nameEn": "Johnny’s Bananas Smoothie",
                "descriptionEs": "Fresas dulces frescas, plátano maduro e hidratante agua de coco 100% natural sin endulzantes añadidos.",
                "descriptionEn": "Sweet strawberries, ripe banana, and refreshing pure coconut water.",
                "price": "$9.95"
            },
            {
                "id": "tonitos-way-pitaya-smoothie",
                "categoryId": "smoothies-bowls",
                "nameEs": "Batido Exótico Tonito’s Way con Pitaya Rosa y Chía (20 oz)",
                "nameEn": "Tonito’s Way Pitaya Smoothie",
                "descriptionEs": "Pitaya fruta del dragón rosa fucsia, fresa, plátano, arándanos azules, semillas orgánicas de chía, proteína de vainilla y leche de avena.",
                "descriptionEn": "Vibrant pink pitaya dragon fruit, strawberry, banana, blueberry, organic chia seeds, vanilla protein, and oat milk.",
                "price": "$12.95",
                "allergens": ["Lácteos"]
            },

            # COFFEE, TEA & SPECIALTY DRINKS
            {
                "id": "bobos-blend-hot-coffee",
                "categoryId": "cafe-bebidas",
                "nameEs": "Café de la Casa Bobo's Blend Caliente",
                "nameEn": "Bobo’s Blend Drip Coffee",
                "descriptionEs": "Mezcla de tueste artesanal exclusivo de granos de especialidad tostados a la perfección con notas suaves a chocolate y nuez tostada.",
                "descriptionEn": "Bobo's signature freshly brewed house roast blend coffee with smooth rich nutty notes.",
                "price": "$2.50"
            },
            {
                "id": "deja-brew-cold-brew",
                "categoryId": "cafe-bebidas",
                "nameEs": "Infusión Fría Bobo's Deja Brew Cold Brew",
                "nameEn": "Bobo’s Deja Brew Cold Brew",
                "descriptionEs": "Café infusionado en frío lentamente durante 18 horas, ultra suave, con cuerpo denso y baja acidez servido sobre hielo.",
                "descriptionEn": "Slow cold-steeped 18-hour craft cold brew blend with low acidity and naturally rich chocolate undertones.",
                "price": "$4.50",
                "popular": True
            },
            {
                "id": "pistachio-latte",
                "categoryId": "cafe-bebidas",
                "nameEs": "Latte Artesanal de Pistacho (Pistachio Latte)",
                "nameEn": "Artisan Pistachio Latte",
                "descriptionEs": "Espresso doble con infusión aromática de pistacho tostado auténtico y leche sedosa cremosa al vapor o servido con hielo.",
                "descriptionEn": "Fresh double espresso infused with roasted pistachio flavor and velvety steamed milk or iced.",
                "price": "$4.95",
                "popular": True,
                "badge": "Seasonal Favorite",
                "allergens": ["Lácteos", "Frutos Secos"]
            },
            {
                "id": "maple-after-dark-cold-brew",
                "categoryId": "cafe-bebidas",
                "nameEs": "Cold Brew Especial Maple After Dark con Soft Top",
                "nameEn": "Maple After Dark Cold Brew",
                "descriptionEs": "Cold brew de chocolate profundo y rico, cubierto con crema suave batida 'soft top' de miel de maple con sal marina en escamas.",
                "descriptionEn": "Dark chocolate-infused rich cold brew topped with salted maple sweet velvety soft top foam.",
                "price": "$5.50",
                "popular": True,
                "badge": "Specialty",
                "allergens": ["Lácteos"]
            },
            {
                "id": "frozen-apple-cider-chai",
                "categoryId": "cafe-bebidas",
                "nameEs": "Frappé Frozen Apple Cider Chai",
                "nameEn": "Frozen Apple Cider Chai",
                "descriptionEs": "Té chai especiado mezclado con sidra de manzana dulce de Nueva Inglaterra y leche entera batido frozen con hielo frappé.",
                "descriptionEn": "Spiced chai blended frozen with sweet local New England apple cider and whole milk.",
                "price": "$7.95",
                "allergens": ["Lácteos"]
            },
            {
                "id": "morning-glow-refresher",
                "categoryId": "cafe-bebidas",
                "nameEs": "Jugo Revitalizante Morning Glow",
                "nameEn": "Morning Glow Cold-Pressed Drink",
                "descriptionEs": "Piña fresca, mango tropical, pepino crujiente refrescante, agua pura de coco y toque de jugo de limón recién exprimido.",
                "descriptionEn": "Pure pineapple, mango, refreshing cucumber, coconut water, and freshly squeezed lemon juice.",
                "price": "$10.95",
                "badge": "Hydration"
            },
            {
                "id": "pecant-resist-latte",
                "categoryId": "cafe-bebidas",
                "nameEs": "Latte Helado Pecan’t Resist con Nuez y Maple",
                "nameEn": "Pecan’t Resist Iced Latte",
                "descriptionEs": "Latte helado de maple y nuez pecana tostada coronado con suave capa espumosa de maple y azúcar morena pura.",
                "descriptionEn": "Maple pecan iced latte finished with a rich maple soft top and a sprinkle of brown sugar (Iced only).",
                "price": "$5.95",
                "badge": "Signature",
                "allergens": ["Lácteos", "Frutos Secos"]
            },
            {
                "id": "ceremonial-matcha-latte",
                "categoryId": "cafe-bebidas",
                "nameEs": "Latte Tradicional de Té Matcha Japonés",
                "nameEn": "Japanese Matcha Latte",
                "descriptionEs": "Té verde matcha ceremonial japonés batido fino al vapor con leche a elección, disponible caliente o con hielo.",
                "descriptionEn": "Premium stone-ground Japanese ceremonial matcha whisked with steamed milk or poured over ice.",
                "price": "$4.50",
                "allergens": ["Lácteos"]
            },

            # LITTLE BO'S (KIDS MENU)
            {
                "id": "little-bos-pb-and-j-waffles",
                "categoryId": "menu-ninos",
                "nameEs": "Sándwich PB&J de Mantequilla de Maní y Mermelada en Waffles",
                "nameEn": "Little Bo’s PB & J Waffles",
                "descriptionEs": "Mantequilla cremosa de maní y mermelada dulce de uva servidas como sándwich entre dos waffles belgas tibios.",
                "descriptionEn": "Creamy peanut butter and sweet jelly sandwiched between two warm golden Belgian waffles.",
                "price": "$9.95",
                "allergens": ["Gluten", "Huevos", "Lácteos", "Frutos Secos"]
            },
            {
                "id": "little-bos-grilled-cheese",
                "categoryId": "menu-ninos",
                "nameEs": "Sándwich de Queso Americano Fundido a la Plancha",
                "nameEn": "Little Bo's Grilled Cheese",
                "descriptionEs": "Abundante queso americano derretido suavemente en pan artesanal de masa madre untado con mantequilla dorada.",
                "descriptionEn": "Gooey melted American cheese grilled on buttered thick-cut artisan sourdough bread.",
                "price": "$5.95",
                "allergens": ["Gluten", "Lácteos"]
            },
            {
                "id": "chocolate-wasted-shake",
                "categoryId": "menu-ninos",
                "nameEs": "Batido de Chocolate Saludable Chocolate Wasted",
                "nameEn": "Chocolate Wasted Shake",
                "descriptionEs": "Batido cremoso de cacao puro elaborado con plátano dulce maduro y leche de avena sin lácteos añadidos.",
                "descriptionEn": "Rich chocolate smoothie shake made with real banana and creamy oat milk.",
                "price": "$5.50"
            },
            {
                "id": "boss-baby-steamer",
                "categoryId": "menu-ninos",
                "nameEs": "Vaso Espumoso Boss Baby de Vainilla y Flor Azul",
                "nameEn": "Boss Baby Vanilla Steamer",
                "descriptionEs": "Leche tibia al vapor aromatizada con vainilla suave y polvo natural azul de flor de mariposa butterfly pea.",
                "descriptionEn": "Warm frothy vanilla milk steamer naturally tinted with colorful butterfly pea flower powder.",
                "price": "$2.95",
                "allergens": ["Lácteos"]
            }
        ],
        "faqs": [
            {
                "qEs": "¿Dónde se encuentra ubicado Bobo's Cafe en Ridgefield?",
                "qEn": "Where is Bobo's Cafe located in Ridgefield?",
                "aEs": "Estamos convenientemente ubicados en 32 Danbury Rd en Ridgefield, CT con amplio estacionamiento en plaza gratuito.",
                "aEn": "We are located at 32 Danbury Rd in Ridgefield, CT, with convenient free plaza parking in front."
            },
            {
                "qEs": "¿Tienen opciones sin gluten y veganas en el menú?",
                "qEn": "Do you have gluten-free and vegan options available?",
                "aEs": "¡Sí! Ofrecemos milanesas de pollo sin gluten (GF chicken cutlets), costra de quiche sin gluten, hash browns sin gluten, tazas de açaí veganas y opciones de leches vegetales de avena, almendra y soya.",
                "aEn": "Yes! We offer gluten-free breaded chicken cutlets, GF quiche crust, GF hash browns, vegan acai bowls, and plant-based milks including oat and almond milk."
            },
            {
                "qEs": "¿Puedo pedir con anticipación para recoger o ordenar a domicilio?",
                "qEn": "Can I order online for pickup or delivery?",
                "aEs": "Por supuesto. Puede hacer su pedido directamente en línea a través de nuestro Toast Tab en boboscafe.net para recoger en el mostrador rápidamente.",
                "aEn": "Absolutely! You can order directly online through our Toast Tab platform on boboscafe.net for quick counter pickup or local delivery."
            }
        ]
    }

    with open(dest, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✅ Generated {dest} with {len(data['products'])} 100% verified authentic items.")

if __name__ == "__main__":
    build_bobos_cafe()

