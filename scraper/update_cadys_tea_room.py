#!/usr/bin/env python3
import json
import os
import sys

def build_cadys():
    dest = "data/merchants/cadys-tea-room.json"
    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["storeInfo"]["name"] = "Cady's Tea Room"
    data["storeInfo"]["address"] = "76 Maple Ave, Greenwich, CT 06830 (Inside Stanton House Inn)"
    data["storeInfo"]["tagline"] = "Historic Victorian Afternoon Tea & Pastries / Servicio Tradicional de Té de la Tarde Victoriano"
    data["storeInfo"]["phone"] = "(203) 869-2110"

    categories = [
        {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Coffee"},
        {"id": "tea-service", "nameEs": "Servicio de Té Completo", "nameEn": "Afternoon Tea Experience", "icon": "Coffee"},
        {"id": "sandwiches", "nameEs": "Sándwiches de Té (Savories)", "nameEn": "Finger Sandwiches", "icon": "Sandwich"},
        {"id": "scones", "nameEs": "Scones Tradicionales Calientes", "nameEn": "Fresh Warm Scones", "icon": "Cake"},
        {"id": "sweets", "nameEs": "Pastelería y Bocados Dulces", "nameEn": "Pastries & Sweets", "icon": "Cake"},
        {"id": "loose-teas", "nameEs": "Selección de Tés de Hoja Suelta", "nameEn": "Loose-Leaf Tea Selection", "icon": "Coffee"},
        {"id": "bubbles", "nameEs": "Espumosos y Mimosas", "nameEn": "Prosecco & Bubbles", "icon": "Wine"}
    ]

    items = [
        # --- SERVICIO COMPLETO DE TÉ ---
        {
            "id": "traditional-afternoon-tea-service",
            "nameEs": "Servicio Tradicional de Té de la Tarde Victoriano (Por Persona)",
            "nameEn": "Traditional Victorian Afternoon Tea Service (Per Person)",
            "descriptionEs": "La experiencia completa de tres niveles: tetera de té de hoja suelta de especialidad a elección, copa de Prosecco italiano, 3 sándwiches de té salados, scones recién horneados calientes con crema cuajada inglesa 'clotted cream' y mermelada casera, y surtido de postres y pasteles pequeños.",
            "descriptionEn": "The quintessential three-tiered afternoon tea: pot of fine loose-leaf tea, glass of chilled Prosecco, 3 savory finger sandwiches, warm freshly baked scones with clotted cream and strawberry preserves, and an assortment of petite pastries and sweets.",
            "price": 45.00,
            "category": "tea-service",
            "allergens": ["Gluten", "Huevos", "Lácteos", "Pescado"],
            "popular": True
        },

        # --- SÁNDWICHES DE TÉ ---
        {
            "id": "cucumber-herb-finger-sandwich",
            "nameEs": "Sándwiches de Pepino Inglés y Queso Crema a las Hierbas",
            "nameEn": "English Cucumber & Herb Cream Cheese Sandwiches",
            "descriptionEs": "Finas rodajas de pepino inglés crujiente, queso crema batido con eneldo fresco y cebollín en pan blanco artesanal sin corteza.",
            "descriptionEn": "Thinly sliced English cucumbers, whipped herb and chive cream cheese, and fresh dill on delicate crustless artisan white bread.",
            "price": 10.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos"],
            "popular": True
        },
        {
            "id": "smoked-salmon-finger-sandwich",
            "nameEs": "Sándwiches de Salmón Ahumado y Crema de Rábano Picante",
            "nameEn": "Smoked Salmon & Horseradish Cream Sandwiches",
            "descriptionEs": "Salmón ahumado del Atlántico de primera calidad, queso crema con rábano picante suave y alcaparras sobre pan de centeno pumpernickel.",
            "descriptionEn": "Premium cold-smoked Atlantic salmon, gentle horseradish cream cheese, and baby capers on dark pumpernickel rye.",
            "price": 12.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Lácteos", "Pescado"],
            "popular": True
        },
        {
            "id": "curried-chicken-finger-sandwich",
            "nameEs": "Sándwiches de Ensalada de Pollo al Curry y Arándanos",
            "nameEn": "Curried Chicken Salad & Cranberry Finger Sandwiches",
            "descriptionEs": "Pechuga de pollo pochada con curry dorado suave, arándanos secos dulces, apio crujiente y almendras tostadas en pan integral.",
            "descriptionEn": "Poached chicken breast with mild golden curry, sweet dried cranberries, crisp celery, and toasted almonds on whole wheat bread.",
            "price": 11.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Frutos secos", "Huevos"]
        },
        {
            "id": "egg-salad-tarragon-sandwich",
            "nameEs": "Sándwiches de Ensalada de Huevo Orgánico al Estragón",
            "nameEn": "Organic Egg Salad with Fresh Tarragon Sandwiches",
            "descriptionEs": "Huevos orgánicos de granja cocidos con mayonesa de Dijon, estragón fresco y brotes verdes en suave pan brioche.",
            "descriptionEn": "Farm-fresh organic egg salad with a touch of Dijon, fresh tarragon, and microgreens on delicate brioche bread.",
            "price": 10.00,
            "category": "sandwiches",
            "allergens": ["Gluten", "Huevos"]
        },

        # --- SCONES ---
        {
            "id": "traditional-english-cream-scone",
            "nameEs": "Scone Tradicional Inglés con Clotted Cream y Mermelada",
            "nameEn": "Traditional English Cream Scone with Clotted Cream & Jam",
            "descriptionEs": "Scone clásico horneado al momento dorado y esponjoso, servido caliente con auténtica crema cuajada inglesa importada (clotted cream) y mermelada de fresa.",
            "descriptionEn": "Classic golden buttermilk scone baked fresh daily, served warm with authentic imported British clotted cream and strawberry preserves.",
            "price": 6.00,
            "category": "scones",
            "allergens": ["Gluten", "Lácteos", "Huevos"],
            "popular": True
        },
        {
            "id": "wild-blueberry-scone",
            "nameEs": "Scone Casero de Arándanos Azules Silvestres",
            "nameEn": "Fresh Wild Blueberry Scone",
            "descriptionEs": "Scone tierno horneado con arándanos azules frescos de Nueva Inglaterra, servido tibio con mantequilla dulce o crema cuajada.",
            "descriptionEn": "Tender scone loaded with sweet wild blueberries, served warm with clotted cream and berry preserves.",
            "price": 6.00,
            "category": "scones",
            "allergens": ["Gluten", "Lácteos", "Huevos"]
        },
        {
            "id": "strawberry-cream-scone",
            "nameEs": "Scone de Fresas de Temporada",
            "nameEn": "Fresh Summer Strawberry Scone",
            "descriptionEs": "Scone artesanal aromatizado con vainilla y trocitos de fresas dulces frescas, horneado diariamente.",
            "descriptionEn": "Artisan vanilla-infused scone baked with sweet seasonal strawberries, served warm with clotted cream.",
            "price": 6.00,
            "category": "scones",
            "allergens": ["Gluten", "Lácteos", "Huevos"]
        },
        {
            "id": "zucchini-cheddar-scone",
            "nameEs": "Scone Salado de Calabacín y Queso Cheddar de Vermont",
            "nameEn": "Savory Zucchini & Vermont Cheddar Scone",
            "descriptionEs": "Scone salado recién horneado con calabacín rallado de huerto, queso cheddar blanco añejo de Vermont y hierbas finas.",
            "descriptionEn": "Warm savory scone baked with garden-fresh grated zucchini, sharp aged Vermont white cheddar, and fresh herbs.",
            "price": 6.50,
            "category": "scones",
            "allergens": ["Gluten", "Lácteos", "Huevos"]
        },

        # --- DULCES Y PASTELERÍA ---
        {
            "id": "french-macarons-trio",
            "nameEs": "Trío de Macarons Franceses de Almendra",
            "nameEn": "French Macarons Trio",
            "descriptionEs": "Tres macarons franceses artesanales con concha crujiente de harina de almendras y rellenos cremosos de temporada (frambuesa, pistacho, vainilla).",
            "descriptionEn": "Trio of delicate French almond meringue macarons with seasonal ganache fillings (raspberry, pistachio, vanilla).",
            "price": 7.50,
            "category": "sweets",
            "allergens": ["Huevos", "Lácteos", "Frutos secos"],
            "popular": True
        },
        {
            "id": "french-madeleines",
            "nameEs": "Madeleines Francesas Calientes al Limón",
            "nameEn": "Freshly Baked Lemon Madeleines",
            "descriptionEs": "Bizcochitos tradicionales franceses horneados en molde de concha marina, con suave mantequilla y ralladura de limón fresco.",
            "descriptionEn": "Traditional petite French sponge cakes baked in shell molds with rich butter and fresh lemon zest.",
            "price": 5.50,
            "category": "sweets",
            "allergens": ["Gluten", "Huevos", "Lácteos"]
        },
        {
            "id": "petit-fours-mini-cheesecakes",
            "nameEs": "Surtido de Petit Fours y Minicheesecakes",
            "nameEn": "Assorted Petit Fours & Mini Cheesecakes",
            "descriptionEs": "Bocaditos de pastel glaseado con mermelada de frambuesa y mini tartas de queso estilo Nueva York con base de galleta graham.",
            "descriptionEn": "Delicate glazed layered almond petit fours and miniature New York style cheesecakes with graham cracker crust.",
            "price": 8.00,
            "category": "sweets",
            "allergens": ["Gluten", "Huevos", "Lácteos", "Frutos secos"]
        },
        {
            "id": "scottish-shortbread-fingers",
            "nameEs": "Galletas Escocesas de Mantequilla (Shortbread)",
            "nameEn": "Scottish Butter Shortbread Fingers",
            "descriptionEs": "Galletas tradicionales escocesas ricas en mantequilla pura con textura quebradiza que se deshace en la boca.",
            "descriptionEn": "Traditional crumbly melt-in-your-mouth Scottish shortbread fingers baked with pure sweet cream butter.",
            "price": 4.50,
            "category": "sweets",
            "allergens": ["Gluten", "Lácteos"]
        },

        # --- SELECCIÓN DE TÉS DE HOJA SUELTA ---
        {
            "id": "brooklyn-breakfast-tea",
            "nameEs": "Té Negro Brooklyn Breakfast (Tetera)",
            "nameEn": "Brooklyn Breakfast Loose-Leaf Tea (Pot)",
            "descriptionEs": "Mezcla robusta y con cuerpo de tés negros de Assam, Ceilán y Keemun, con notas maltosas perfectas para acompañar con una nube de leche.",
            "descriptionEn": "Bold and malty full-bodied blend of Assam, Ceylon, and Keemun black tea leaves, exceptional with a splash of milk.",
            "price": 7.00,
            "category": "loose-teas",
            "popular": True
        },
        {
            "id": "carroll-gardens-black-tea",
            "nameEs": "Té Negro Carroll Gardens con Bayas y Rosas (Tetera)",
            "nameEn": "Carroll Gardens Aromatic Black Tea (Pot)",
            "descriptionEs": "Té negro aromático infusionado con bayas de saúco secas, pétalos de rosa dulce y notas cítricas frescas.",
            "descriptionEn": "Fragrant black tea layered with dried elderberries, sweet rose petals, and bright citrus notes.",
            "price": 7.00,
            "category": "loose-teas"
        },
        {
            "id": "jasmine-green-tea",
            "nameEs": "Té Verde al Jazmín Imperial (Tetera)",
            "nameEn": "Imperial Jasmine Green Tea (Pot)",
            "descriptionEs": "Hojas de té verde finas aromatizadas naturalmente con flores de jazmín que abren de noche, aroma floral dulce y delicado.",
            "descriptionEn": "Delicate green tea scented with fresh nocturnal jasmine blossoms for a floral, soothing infusion.",
            "price": 7.00,
            "category": "loose-teas",
            "popular": True
        },
        {
            "id": "moroccan-mint-green-tea",
            "nameEs": "Té Verde a la Menta Marroquí (Tetera)",
            "nameEn": "Moroccan Mint Green Tea (Pot)",
            "descriptionEs": "Té verde Gunpowder enrollado infusionado con hojas aromáticas de hierbabuena y menta piperita refrescante.",
            "descriptionEn": "Rolled Gunpowder green tea blended with vibrant spearmint and peppermint leaves for a revitalizing sip.",
            "price": 7.00,
            "category": "loose-teas"
        },
        {
            "id": "earl-grey-supreme",
            "nameEs": "Té Earl Grey Supremo con Bergamota (Tetera)",
            "nameEn": "Earl Grey Supreme Black Tea (Pot)",
            "descriptionEs": "Té negro selecto infusionado con aceite esencial de bergamota de Calabria y toques de flor de aciano azul.",
            "descriptionEn": "Select black teas masterfully scented with pure Calabrian bergamot oil and blue cornflower petals.",
            "price": 7.00,
            "category": "loose-teas",
            "popular": True
        },
        {
            "id": "chamomile-citrus-herbal",
            "nameEs": "Infusión Herbal de Manzanilla Egipcia y Cítricos (Tetera)",
            "nameEn": "Egyptian Chamomile & Citrus Herbal Tea (Pot)",
            "descriptionEs": "Flores enteras de manzanilla egipcia orgánica combinadas con zacate limón y cáscara de naranja dulce. Naturalmente sin cafeína.",
            "descriptionEn": "Whole organic Egyptian chamomile flowers blended with lemongrass and sweet orange peel. Naturally caffeine-free.",
            "price": 7.00,
            "category": "loose-teas"
        },

        # --- BURBUJAS Y MIMOSAS ---
        {
            "id": "prosecco-glass",
            "nameEs": "Copa de Prosecco Italiano DOC",
            "nameEn": "Glass of Italian Prosecco DOC",
            "descriptionEs": "Vino espumoso italiano fresco y seco, con burbuja fina persistente y notas a manzana verde y flores blancas.",
            "descriptionEn": "Crisp, dry sparkling Italian Prosecco with fine persistent bubbles and notes of green apple and white flowers.",
            "price": 12.00,
            "category": "bubbles"
        },
        {
            "id": "fresh-orange-mimosa",
            "nameEs": "Mimosa Clásica con Jugo de Naranja Fresco",
            "nameEn": "Classic Mimosa with Fresh Orange Juice",
            "descriptionEs": "Prosecco italiano servido en copa flauta con jugo de naranja dulce recién exprimido al momento.",
            "descriptionEn": "Chilled Italian Prosecco mixed with freshly squeezed sweet orange juice in a champagne flute.",
            "price": 14.00,
            "category": "bubbles",
            "popular": True
        }
    ]

    data["categories"] = categories
    data["items"] = items

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully written {len(items)} verified items to {dest}!")

if __name__ == "__main__":
    build_cadys()
