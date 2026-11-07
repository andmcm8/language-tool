#!/usr/bin/env python3
import json
import os
import sys

def build_brewport():
    dest = "data/merchants/brewport.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Categories
    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
        {"id": "pizzas", "nameEs": "Pizzas a la Leña", "nameEn": "Wood-Fired Pizzas", "icon": "Pizza"},
        {"id": "salads", "nameEs": "Ensaladas Frescas", "nameEn": "Gourmet Salads", "icon": "Salad"},
        {"id": "house-brews", "nameEs": "Cervezas Artesanales", "nameEn": "House Brews", "icon": "Beer"},
        {"id": "cocktails", "nameEs": "Cócteles y Licores", "nameEn": "Cocktails & Spirits", "icon": "Wine"},
        {"id": "beverages-desserts", "nameEs": "Bebidas y Postres", "nameEn": "Beverages & Desserts", "icon": "Coffee"}
    ]

    items = [
        # --- PIZZAS ---
        {
            "id": "red-pie-sm",
            "nameEs": "Pizza Roja Tradicional (Pequeña 12\")",
            "nameEn": "Traditional Red Pie (Small 12\")",
            "descriptionEs": "Masa delgada y crujiente con salsa de tomate casera de la casa y mozzarella rallada fundida.",
            "descriptionEn": "Signature thin crust with house-made tomato sauce and melted shredded mozzarella cheese.",
            "price": 13.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "red-pie-lg",
            "nameEs": "Pizza Roja Tradicional (Grande 16\")",
            "nameEn": "Traditional Red Pie (Large 16\")",
            "descriptionEs": "Pizza grande de masa delgada estilo Connecticut con salsa de tomate hecha en casa y queso mozzarella.",
            "descriptionEn": "Large thin-crust Connecticut style pizza with house-made tomato sauce and bubbly mozzarella.",
            "price": 18.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "white-pie-sm",
            "nameEs": "Pizza Blanca de Ajo y Queso (Pequeña 12\")",
            "nameEn": "Garlic White Pie (Small 12\")",
            "descriptionEs": "Base blanca con aceite de oliva extra virgen, ajo fresco picado, parmesano rallado y mozzarella.",
            "descriptionEn": "White base brushed with extra virgin olive oil, fresh minced garlic, grated parmesan, and shredded mozzarella.",
            "price": 15.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "white-pie-lg",
            "nameEs": "Pizza Blanca de Ajo y Queso (Grande 16\")",
            "nameEn": "Garlic White Pie (Large 16\")",
            "descriptionEs": "Pizza blanca grande con aceite de oliva extra virgen, abundante ajo fresco, queso parmesano y mozzarella.",
            "descriptionEn": "Large white pie with extra virgin olive oil, fresh garlic, grated parmesan, and melted mozzarella.",
            "price": 20.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "new-haven-plain-sm",
            "nameEs": "Pizza Roja Estilo New Haven 'Plain' (Pequeña 12\")",
            "nameEn": "New Haven Style Plain Red Pie (Small 12\")",
            "descriptionEs": "Estilo auténtico New Haven: salsa de tomate casera sazonada, orégano y queso pecorino romano rallado (sin mozzarella).",
            "descriptionEn": "Authentic New Haven style plain pie: seasoned tomato sauce, oregano, and grated pecorino romano (no mozzarella).",
            "price": 11.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "new-haven-plain-lg",
            "nameEs": "Pizza Roja Estilo New Haven 'Plain' (Grande 16\")",
            "nameEn": "New Haven Style Plain Red Pie (Large 16\")",
            "descriptionEs": "Auténtica tarta grande tradicional con salsa de tomate rica, orégano aromático y toque de pecorino romano.",
            "descriptionEn": "Large authentic traditional New Haven plain pie with rich tomato sauce, oregano, and grated pecorino romano.",
            "price": 15.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "meat-master-sm",
            "nameEs": "Pizza The Meat Master (Pequeña 12\")",
            "nameEn": "The Meat Master Pizza (Small 12\")",
            "descriptionEs": "Salsa roja casera y mozzarella cargada de pepperoni cortado grueso, salchicha italiana artesanal, tocino ahumado y jamón.",
            "descriptionEn": "House red sauce and mozzarella loaded with thick-cut pepperoni, locally made sausage, smoky bacon, and ham.",
            "price": 25.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "meat-master-lg",
            "nameEs": "Pizza The Meat Master (Grande 16\")",
            "nameEn": "The Meat Master Pizza (Large 16\")",
            "descriptionEs": "El festín supremo para carnívoros: salsa roja, queso mozzarella, pepperoni grueso, salchicha local, tocino crocante y jamón.",
            "descriptionEn": "The ultimate carnivore feast: house red sauce, mozzarella, thick-cut pepperoni, local Italian sausage, crisp bacon, and ham.",
            "price": 31.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "white-clam-sm",
            "nameEs": "Pizza Blanca de Almejas Frescas (Pequeña 12\")",
            "nameEn": "The White Clam Pizza (Small 12\")",
            "descriptionEs": "La legendaria especialidad de la costa de CT: almejas frescas recién abiertas, mozzarella, ajo picado y aceite de oliva virgen extra.",
            "descriptionEn": "Connecticut coastline specialty: fresh shucked clams, shredded mozzarella, minced garlic, and extra virgin olive oil.",
            "price": 30.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos", "Mariscos"],
            "popular": True
        },
        {
            "id": "white-clam-lg",
            "nameEs": "Pizza Blanca de Almejas Frescas (Grande 16\")",
            "nameEn": "The White Clam Pizza (Large 16\")",
            "descriptionEs": "Pizza grande cargada con abundantes almejas frescas del Atlántico, ajo fresco, mozzarella y aceite de oliva virgen extra.",
            "descriptionEn": "Large coastal favorite loaded with fresh shucked Atlantic clams, fresh garlic, mozzarella, and extra virgin olive oil.",
            "price": 50.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos", "Mariscos"],
            "popular": True
        },
        {
            "id": "the-barrett-sm",
            "nameEs": "Pizza The Barrett con Pulled Pork y Kimchi (Pequeña 12\")",
            "nameEn": "The Barrett Pulled Pork Pizza (Small 12\")",
            "descriptionEs": "Base blanca con carne de cerdo deshebrada (pulled pork) cocida a fuego lento durante la noche, salsa BBQ coreana casera agridulce y guarnición de kimchi picante.",
            "descriptionEn": "White pie topped with overnight slow-cooked pulled pork, zesty secret-recipe Korean BBQ sauce, served with a side of spicy kimchi.",
            "price": 25.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos", "Nueces/Sésamo"]
        },
        {
            "id": "the-barrett-lg",
            "nameEs": "Pizza The Barrett con Pulled Pork y Kimchi (Grande 16\")",
            "nameEn": "The Barrett Pulled Pork Pizza (Large 16\")",
            "descriptionEs": "Pizza grande blanca con cerdo pulled pork cocido a fuego lento, salsa BBQ coreana artesanal y porción de kimchi fermentado picante.",
            "descriptionEn": "Large white pie loaded with overnight slow-cooked pulled pork, house Korean BBQ sauce, served with a side of spicy house kimchi.",
            "price": 30.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos", "Nueces/Sésamo"]
        },
        {
            "id": "the-brewmaster-sm",
            "nameEs": "Pizza The Brewmaster (Pequeña 12\")",
            "nameEn": "The Brewmaster Pizza (Small 12\")",
            "descriptionEs": "La combinación favorita del cervecero: salsa roja, mozzarella, pechuga de pollo desmenuzada, pepperoni cortado grueso y pimientos picantes cherry.",
            "descriptionEn": "The brewmaster's favorite: house red sauce, mozzarella, all-white meat chicken, thick-cut pepperoni, and tangy cherry hot peppers.",
            "price": 25.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "the-brewmaster-lg",
            "nameEs": "Pizza The Brewmaster (Grande 16\")",
            "nameEn": "The Brewmaster Pizza (Large 16\")",
            "descriptionEs": "Pizza grande con salsa roja de la casa, mozzarella, pollo tierno, pepperoni grueso y el toque especiado de pimientos cherry.",
            "descriptionEn": "Large signature pie with house red sauce, mozzarella, tender chicken, thick pepperoni, and zesty cherry peppers.",
            "price": 30.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "tree-hugger-sm",
            "nameEs": "Pizza Vegetariana The Tree Hugger (Pequeña 12\")",
            "nameEn": "The Tree Hugger Veggie Pizza (Small 12\")",
            "descriptionEs": "Paseo por el huerto: cebollas moradas, pimientos dulces, champiñones frescos en rodajas, brócoli tierno, aceitunas y ajo.",
            "descriptionEn": "Garden-fresh vegetarian delight: onions, sweet peppers, fresh sliced mushrooms, tender broccoli florets, olives, and garlic.",
            "price": 25.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "tree-hugger-lg",
            "nameEs": "Pizza Vegetariana The Tree Hugger (Grande 16\")",
            "nameEn": "The Tree Hugger Veggie Pizza (Large 16\")",
            "descriptionEs": "Pizza grande vegetariana repleta de pimientos, cebollas, champiñones, brócoli, aceitunas y mozzarella derretida.",
            "descriptionEn": "Large vegetable feast loaded with peppers, onions, mushrooms, broccoli, olives, garlic, and bubbly mozzarella.",
            "price": 30.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "potato-bacon-sm",
            "nameEs": "Pizza de Puré de Papa y Tocino (Pequeña 12\")",
            "nameEn": "Mashed Potato & Bacon Pizza (Small 12\")",
            "descriptionEs": "Clásico de culto de Connecticut: base blanca con puré de papas cremoso sazonado, tocino crocante, ajo y queso mozzarella fundido.",
            "descriptionEn": "Connecticut cult classic: white pie base with savory seasoned mashed potatoes, crispy bacon, garlic, and melted mozzarella.",
            "price": 21.50,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "potato-bacon-lg",
            "nameEs": "Pizza de Puré de Papa y Tocino (Grande 16\")",
            "nameEn": "Mashed Potato & Bacon Pizza (Large 16\")",
            "descriptionEs": "Pizza grande con suave puré de papa, trozos generosos de tocino ahumado crujiente, ajo asado y abundante queso mozzarella.",
            "descriptionEn": "Large white pie layered with creamy mashed potatoes, generous smoky bacon crumbles, roasted garlic, and mozzarella.",
            "price": 29.00,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "pepperoni-pie-sm",
            "nameEs": "Pizza de Pepperoni Artesanal (Pequeña 12\")",
            "nameEn": "Artisan Pepperoni Pizza (Small 12\")",
            "descriptionEs": "Salsa roja casera, queso mozzarella fundido y abundantes rodajas gruesas de pepperoni tostado crujiente.",
            "descriptionEn": "House red sauce, melted mozzarella, and generous slices of thick-cut cupping pepperoni.",
            "price": 16.25,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "pepperoni-pie-lg",
            "nameEs": "Pizza de Pepperoni Artesanal (Grande 16\")",
            "nameEn": "Artisan Pepperoni Pizza (Large 16\")",
            "descriptionEs": "Pizza grande con mozzarella burbujeante, salsa roja y doble porción de pepperoni cortado grueso.",
            "descriptionEn": "Large thin crust pie with bubbly mozzarella, red sauce, and double layer of thick artisan pepperoni.",
            "price": 22.50,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "sausage-pie-sm",
            "nameEs": "Pizza de Salchicha Italiana (Pequeña 12\")",
            "nameEn": "Italian Sausage Pizza (Small 12\")",
            "descriptionEs": "Salsa de tomate casera, queso mozzarella y trozos de salchicha italiana localmente elaborada con hierbas aromáticas.",
            "descriptionEn": "House tomato sauce, mozzarella, and locally crafted crumbled Italian sausage with aromatic spices.",
            "price": 16.25,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },
        {
            "id": "sausage-pie-lg",
            "nameEs": "Pizza de Salchicha Italiana (Grande 16\")",
            "nameEn": "Italian Sausage Pizza (Large 16\")",
            "descriptionEs": "Pizza grande con salsa roja tradicional, queso mozzarella y sabrosa salchicha italiana local desmenuzada.",
            "descriptionEn": "Large pie with traditional red sauce, mozzarella, and flavorful locally made crumbled Italian fennel sausage.",
            "price": 22.50,
            "category": "pizzas",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- SALADS ---
        {
            "id": "antipasto-salad-sm",
            "nameEs": "Ensalada Antipasto Tradicional (Pequeña)",
            "nameEn": "Antipasto Salad (Small)",
            "descriptionEs": "Lechugas mixtas frescas con pimientos rojos asados, tomates, aceitunas, jamón dulce, provolone, salami Génova, pepperoni y giardiniera en escabeche.",
            "descriptionEn": "Crisp house greens topped with roasted red peppers, tomatoes, olives, ham, provolone, Genoa salami, pepperoni, and pickled giardiniera.",
            "price": 15.00,
            "category": "salads",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "antipasto-salad-lg",
            "nameEs": "Ensalada Antipasto Tradicional (Grande Para Compartir)",
            "nameEn": "Antipasto Salad (Large Sharing Size)",
            "descriptionEs": "Platón grande con pimientos asados, aceitunas kalamata, jamón selecto, salami, provolone, pepperoni y vegetales encurtidos sobre hojas verdes de la casa.",
            "descriptionEn": "Large sharing platter loaded with roasted peppers, olives, premium ham, salami, provolone, pepperoni, and pickled vegetables over house greens.",
            "price": 27.00,
            "category": "salads",
            "allergens": ["Lácteos"],
            "popular": True
        },
        {
            "id": "caesar-salad-sm",
            "nameEs": "Ensalada César Clásica (Pequeña)",
            "nameEn": "Classic Caesar Salad (Small)",
            "descriptionEs": "Corazones de lechuga romana crujiente, lajas de queso parmesano importado, crutones dorados y aderezo César cremoso de la casa (anchoas opcionales).",
            "descriptionEn": "Crisp romaine hearts, shaved imported parmesan flakes, toasted croutons, and house creamy Caesar dressing (anchovies on request).",
            "price": 13.00,
            "category": "salads",
            "allergens": ["Gluten", "Lácteos", "Pescado"]
        },
        {
            "id": "caesar-salad-lg",
            "nameEs": "Ensalada César Clásica (Grande)",
            "nameEn": "Classic Caesar Salad (Large)",
            "descriptionEs": "Tazón grande de fresca lechuga romana con abundantes lajas de parmesano, crutones horneados y auténtico aderezo César.",
            "descriptionEn": "Large bowl of crisp romaine lettuce, generous shaved parmesan cheese, garlic croutons, and authentic house Caesar dressing.",
            "price": 20.00,
            "category": "salads",
            "allergens": ["Gluten", "Lácteos", "Pescado"]
        },
        {
            "id": "garden-gorgonzola-sm",
            "nameEs": "Ensalada del Huerto con Manzana y Gorgonzola (Pequeña)",
            "nameEn": "Garden Greens with Apple & Gorgonzola (Small)",
            "descriptionEs": "Mezcla de hojas tiernas de huerta, rodajas finas de manzana verde crujiente, nueces caramelizadas, queso gorgonzola cremoso y vinagreta balsámica de la casa.",
            "descriptionEn": "Tender mixed greens, crisp sliced green apples, candied walnuts, creamy gorgonzola crumbles, and house vinaigrette.",
            "price": 14.00,
            "category": "salads",
            "allergens": ["Lácteos", "Nueces"]
        },
        {
            "id": "garden-gorgonzola-lg",
            "nameEs": "Ensalada del Huerto con Manzana y Gorgonzola (Grande)",
            "nameEn": "Garden Greens with Apple & Gorgonzola (Large)",
            "descriptionEs": "Tazón grande de verduras del huerto, manzana fresca verde, nueces dulces glaseadas, queso azul gorgonzola y vinagreta casera.",
            "descriptionEn": "Large salad bowl of mixed greens, fresh crisp apples, sweet candied walnuts, tangy gorgonzola crumbles, and house vinaigrette.",
            "price": 24.00,
            "category": "salads",
            "allergens": ["Lácteos", "Nueces"]
        },
        {
            "id": "baby-spinach-salad-sm",
            "nameEs": "Ensalada de Espinacas Baby con Tocino y Huevo (Pequeña)",
            "nameEn": "Baby Spinach Salad with Bacon & Egg (Small)",
            "descriptionEs": "Hojas frescas de espinaca tierna, cebolla morada en julianas, gajos de huevo duro, queso gorgonzola desmoronado y tocino crocante picado.",
            "descriptionEn": "Tender baby spinach, thinly sliced red onion, hard-boiled egg wedges, gorgonzola crumbles, and crispy chopped bacon.",
            "price": 15.00,
            "category": "salads",
            "allergens": ["Huevos", "Lácteos"]
        },
        {
            "id": "baby-spinach-salad-lg",
            "nameEs": "Ensalada de Espinacas Baby con Tocino y Huevo (Grande)",
            "nameEn": "Baby Spinach Salad with Bacon & Egg (Large)",
            "descriptionEs": "Porción grande de espinaca tierna, huevo cocido, queso azul gorgonzola, cebollas moradas y abundante tocino ahumado crujiente.",
            "descriptionEn": "Large entree salad of baby spinach, hard-boiled egg wedges, crumbled gorgonzola, sliced red onion, and generous crispy bacon.",
            "price": 25.00,
            "category": "salads",
            "allergens": ["Huevos", "Lácteos"]
        },

        # --- HOUSE BREWS ---
        {
            "id": "blood-orange-blonde-pint",
            "nameEs": "Cerveza Blood Orange Blonde (Vaso 16oz)",
            "nameEn": "Blood Orange Blonde Ale (16oz Pint)",
            "descriptionEs": "Cerveza rubia insignia de la casa (5.0% ABV) elaborada con jugo natural de naranja roja. Aroma cítrico vibrante y cuerpo refrescante y sedoso.",
            "descriptionEn": "Flagship house blonde ale (5.0% ABV) brewed with real blood orange juice for crisp citrus aroma and refreshing thirst-quenching finish.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"],
            "popular": True
        },
        {
            "id": "blood-orange-blonde-6pk",
            "nameEs": "Blood Orange Blonde Ale (Pack de 6 Latas Para Llevar)",
            "nameEn": "Blood Orange Blonde (6-Pack To-Go)",
            "descriptionEs": "Six-pack de latas de 12oz de la cerveza más vendida y aclamada de Brewport para disfrutar en casa.",
            "descriptionEn": "Six-pack of 12oz cans of Brewport's #1 best-selling craft ale to take home.",
            "price": 12.00,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "naked-blonde-pint",
            "nameEs": "Cerveza Naked Blonde Ale (Vaso 16oz)",
            "nameEn": "Naked Blonde Ale (16oz Pint)",
            "descriptionEs": "Cerveza rubia pura y cristalina (5.0% ABV) elaborada únicamente con lúpulo fino, agua pura, levadura y cebada malteada. Ligera y muy bebible.",
            "descriptionEn": "Pure, unencumbered traditional blonde ale (5.0% ABV) crafted with hops, water, yeast, and barley. Light, easy drinking, and clean.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "midnight-lager-pint",
            "nameEs": "Cerveza Midnight Black Lager (Vaso 16oz)",
            "nameEn": "Midnight Black Lager (16oz Pint)",
            "descriptionEs": "Lager negra estilo checo (5.0% ABV) suave y misteriosa, con delicadas notas a malta tostada y final fresco como una noche junto al mar.",
            "descriptionEn": "Czech-inspired black lager (5.0% ABV). Dark and mysterious yet smooth and drinkable with delicate roasted malt hints.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "south-end-pale-ale-pint",
            "nameEs": "Cerveza South End Pale Ale (Vaso 16oz)",
            "nameEn": "South End Pale Ale (16oz Pint)",
            "descriptionEs": "Pale ale artesanal (5.2% ABV) fermentada con maltas canadienses de calidad y lúpulos Chinook cultivados localmente en Connecticut con toques sutiles de melón.",
            "descriptionEn": "American pale ale (5.2% ABV) brewed with locally grown Connecticut Chinook hops and Canadian malts with light melon aromatics.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "kings-tide-dipa-pint",
            "nameEs": "Cerveza King’s Tide Doble IPA (Vaso 16oz)",
            "nameEn": "King’s Tide DIPA (16oz Pint)",
            "descriptionEs": "Doble IPA potente (9.0% ABV) elaborada con lúpulos Sabro y Citra. Intensos toques frutales tropicales y cuerpo de malta balanceado.",
            "descriptionEn": "Powerhouse Double IPA (9.0% ABV) brewed with Sabro and Citra hops. Intense tropical hop punch and balanced malt profile.",
            "price": 8.50,
            "category": "house-brews",
            "allergens": ["Gluten"],
            "popular": True
        },
        {
            "id": "barrett-brothers-brown-pint",
            "nameEs": "Cerveza Barrett Brothers Brown Ale (Vaso 16oz)",
            "nameEn": "Barrett Brothers Brown Ale (16oz Pint)",
            "descriptionEs": "Cerveza tostada estilo británico (5.6% ABV) elaborada con generosa malta marrón inglesa y sutil lúpulo tradicional Fuggle.",
            "descriptionEn": "Sophisticated English-style brown ale (5.6% ABV) brewed with English brown malt and traditional English hops for a smooth, nutty finish.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "old-news-dipa-pint",
            "nameEs": "Cerveza Old News DIPA (Vaso 16oz)",
            "nameEn": "Old News Double IPA (16oz Pint)",
            "descriptionEs": "Doble IPA de la vieja escuela (8.0% ABV) cargada de lúpulos clásicos resinosos americanos y malta acaramelada con un final robusto.",
            "descriptionEn": "Old-school Double IPA (8.0% ABV) brewed with intense classic American hops and robust malt character for a bold, in-your-face bite.",
            "price": 8.50,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "high-tide-ipa-pint",
            "nameEs": "Cerveza High Tide IPA (Vaso 16oz)",
            "nameEn": "High Tide IPA (16oz Pint)",
            "descriptionEs": "IPA vibrante (6.2% ABV) con una mezcla exclusiva de lúpulos Sativa y Zamba que desprenden aromas a mango jugoso, maracuyá y cítricos frescos.",
            "descriptionEn": "Bright IPA (6.2% ABV) featuring a glorious blend of Sativa and Zamba hops bursting with mango, passion fruit, and crisp citrus notes.",
            "price": 8.00,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "the-roadie-sipa-pint",
            "nameEs": "Cerveza The Roadie Session IPA (Vaso 16oz)",
            "nameEn": "The Roadie Session IPA (16oz Pint)",
            "descriptionEs": "Session IPA ligera (4.6% ABV) pero con enorme sabor cítrico a lúpulo Citra fresco, diseñada para disfrutar trago tras trago.",
            "descriptionEn": "Light session IPA (4.6% ABV) brewed with Citra hops for tremendous citrus character without the high alcohol punch.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },
        {
            "id": "wehles-pale-lager-pint",
            "nameEs": "Cerveza Wehle’s Pale Lager Resucitada (Vaso 16oz)",
            "nameEn": "Wehle’s Historic Pale Lager (16oz Pint)",
            "descriptionEs": "Receta histórica resucitada de agosto de 1941 de la Wehle Brewing Co. de West Haven (5.4% ABV). 80% malta estándar, 20% maíz en hojuelas y lúpulo Hallertau alemán.",
            "descriptionEn": "Historic resurrected August 1941 West Haven recipe (5.4% ABV). 80% standard malt, 20% flaked corn, and German Hallertau hops. Crisp and nostalgic.",
            "price": 7.75,
            "category": "house-brews",
            "allergens": ["Gluten"]
        },

        # --- COCKTAILS & CRAFT DRINKS ---
        {
            "id": "espresso-martini",
            "nameEs": "Espresso Martini de la Casa",
            "nameEn": "House Espresso Martini",
            "descriptionEs": "Café espresso recién preparado batido en coctelera con licor de café y su elección de vodka o tequila artesanal.",
            "descriptionEn": "Freshly pulled rich espresso shaken with coffee liqueur and your choice of premium vodka or tequila.",
            "price": 14.00,
            "category": "cocktails"
        },
        {
            "id": "the-law-cocktail",
            "nameEs": "Cóctel The Law",
            "nameEn": "The Law Bourbon Cocktail",
            "descriptionEs": "Bourbon añejo, triple sec, jugo de arándano agrio, jugo de limón recién exprimido y amargos aromáticos, terminado con refresco lima-limón.",
            "descriptionEn": "Fine bourbon, triple sec, tart cranberry juice, fresh lemon juice, and aromatic bitters, topped with lemon-lime soda.",
            "price": 14.00,
            "category": "cocktails"
        },
        {
            "id": "repiccis-sangria",
            "nameEs": "Sangría Artesanal con Nieve Repicci's",
            "nameEn": "Repicci’s Italian Ice Sangria",
            "descriptionEs": "Fresas frescas, rodaja de naranja, brandy de manzana selecto, vino tinto robusto y una bola de nieve artesanal Repicci's Italian Ice.",
            "descriptionEn": "Fresh strawberries, orange wheel, apple brandy, red wine, topped with a refreshing scoop of Repicci’s Italian ice.",
            "price": 14.00,
            "category": "cocktails",
            "popular": True
        },
        {
            "id": "and-so-it-gose",
            "nameEs": "Cóctel And So It Gose",
            "nameEn": "And So It Gose Cocktail",
            "descriptionEs": "Tequila Mi Campo blanco, jugo de lima recién exprimido, néctar de agave orgánico, fresa machacada, albahaca fresca y toque de cerveza Gose ácida.",
            "descriptionEn": "Mi Campo blanco tequila, fresh lime juice, agave nectar, muddled strawberry, fresh basil, and house tart gose ale.",
            "price": 14.00,
            "category": "cocktails"
        },
        {
            "id": "elderflower-fizz",
            "nameEs": "Cóctel Elderflower Fizz",
            "nameEn": "Elderflower Fizz",
            "descriptionEs": "Vodka Elevate, licor de saúco St. Germain, Aperol italiano, jugo de limón fresco y rematado con cerveza de jengibre picante.",
            "descriptionEn": "Elevate craft vodka, St. Germain elderflower liqueur, Aperol, fresh lemon juice, topped with spicy ginger beer.",
            "price": 14.00,
            "category": "cocktails"
        },
        {
            "id": "mezcal-margarita",
            "nameEs": "Margarita Ahumada de Mezcal",
            "nameEn": "Smoky Mezcal Margarita",
            "descriptionEs": "Para quienes disfrutan una margarita de notas ahumadas profundas: mezcal artesanal, jugo de lima fresco, licor de naranja y agave.",
            "descriptionEn": "Artisanal smoky mezcal, fresh squeezed lime juice, triple sec, and agave nectar with a salted rim.",
            "price": 13.00,
            "category": "cocktails"
        },
        {
            "id": "jabrils-pineapple-smash",
            "nameEs": "Cóctel Jabril’s Pineapple Smash",
            "nameEn": "Jabril’s Pineapple Smash",
            "descriptionEs": "Whiskey irlandés suave, jugo de piña tropical, mezcla agridulce cítrica y néctar de agave rematado con cerveza de jengibre refrescante.",
            "descriptionEn": "Smooth Irish whiskey, sweet pineapple juice, citrus sour mix, and agave nectar topped with ginger beer.",
            "price": 14.00,
            "category": "cocktails"
        },
        {
            "id": "peach-tea-cocktail",
            "nameEs": "Cóctel de Té Helado y Durazno (Peach Tea)",
            "nameEn": "Brewport Peach Iced Tea Cocktail",
            "descriptionEs": "Vodka de calidad, licor de durazno Peachtree, toque de jarabe ligero, jugo de limón y té helado negro sin endulzar.",
            "descriptionEn": "Vodka, Peachtree schnapps, light simple syrup, fresh lemon juice, and unsweetened freshly brewed iced tea.",
            "price": 14.00,
            "category": "cocktails"
        },

        # --- BEVERAGES & DESSERTS ---
        {
            "id": "wellingtons-root-beer-pint",
            "nameEs": "Refresco Casero Wellington’s Old Style Root Beer (19oz)",
            "nameEn": "Wellington’s Old Style Root Beer (19oz Pint)",
            "descriptionEs": "El famoso refresco malteado tradicional de la casa preparado artesanalmente en la propia cervecería.",
            "descriptionEn": "Brewport's legendary house-brewed old-style malted soft soda made from scratch. Note: contains malt/gluten.",
            "price": 3.79,
            "category": "beverages-desserts",
            "allergens": ["Gluten"],
            "popular": True
        },
        {
            "id": "root-beer-float",
            "nameEs": "Vaca Negra (Root Beer Float de Wellington)",
            "nameEn": "Wellington’s Root Beer Float",
            "descriptionEs": "Refresco de malta Wellington's servido sobre dos bolas gigantes de helado cremoso de vainilla, coronado con crema batida y cereza al marrasquino.",
            "descriptionEn": "House Wellington’s malt root beer poured over two generous scoops of rich vanilla ice cream, finished with whipped cream and a cherry.",
            "price": 8.00,
            "category": "beverages-desserts",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "repicci-italian-ice",
            "nameEs": "Nieve Artesanal Repicci’s Italian Ice",
            "nameEn": "Repicci’s Artisanal Italian Ice",
            "descriptionEs": "Nieve italiana tradicional en refrescantes sabores frutales de temporada (pregunte a su mesero por las variedades del día).",
            "descriptionEn": "Authentic smooth Italian ice in rotating seasonal fruit flavors. Ask your server for today's selection.",
            "price": 4.00,
            "category": "beverages-desserts"
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully updated {dest} with {len(items)} verified items!")

if __name__ == "__main__":
    build_brewport()

