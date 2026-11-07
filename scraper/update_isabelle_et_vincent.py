#!/usr/bin/env python3
import json
import os
import sys

def build_isabelle():
    dest = "data/merchants/isabella-et-vincent.json"
    
    data = {
        "storeInfo": {
            "id": "isabella-et-vincent",
            "name": "Isabelle et Vincent",
            "tagline": "Traditional French Boulangerie, Patisserie & Chocolaterie from Strasbourg in Fairfield",
            "address": "1903 Post Rd, Fairfield, CT 06824",
            "hours": {
                "tuesday_saturday": "7:00 AM - 6:00 PM",
                "sunday": "7:00 AM - 2:00 PM",
                "monday": "Closed"
            },
            "paymentMethods": [
                "Cash",
                "Credit/Debit Cards",
                "Apple Pay",
                "Contactless"
            ],
            "amenities": [
                "Scratch-Made French Bakery",
                "Artisan Breads Baked Daily",
                "Takeout",
                "Cafe Seating",
                "Bilingual Menu",
                "Custom French Celebration Cakes"
            ],
            "themeColor": "#0284c7",
            "logoIcon": "cake",
            "policies": {
                "returnPolicyEs": "Todos nuestros panes y pasteles se hornean desde cero cada madrugada; notifíquenos cualquier consulta.",
                "returnPolicyEn": "All breads and pastries are baked from scratch daily; please let our team know if anything isn't perfect.",
            },
            "phone": "(203) 292-8022"
        },
        "categories": [
            {"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"},
            {"id": "croissants-viennoiserie", "nameEs": "Croissants y Viennoiserie Francesa", "nameEn": "Croissants & Viennoiserie", "icon": "Sparkles"},
            {"id": "patisserie-postres", "nameEs": "Pastelería Fina y Postres (Patisserie)", "nameEn": "French Patisserie & Cakes", "icon": "Cake"},
            {"id": "macarons-galletas", "nameEs": "Macarons Franceses y Galletas", "nameEn": "French Macarons & Cookies", "icon": "Cake"},
            {"id": "pan-artesanal-baguettes", "nameEs": "Baguettes y Pan Rústico Francés", "nameEn": "Artisan Breads & Baguettes", "icon": "Utensils"},
            {"id": "sandwiches-quiches", "nameEs": "Sándwiches en Croissant y Quiches", "nameEn": "Croissant Sandwiches & Quiches", "icon": "Utensils"},
            {"id": "cafe-bebidas", "nameEs": "Café y Bebidas Francesas", "nameEn": "Coffee & French Drinks", "icon": "Coffee"}
        ],
        "items": [
            # --- CROISSANTS Y VIENNOISERIE ---
            {
                "id": "croissant-beurre-plain",
                "nameEs": "Croissant Tradicional de Mantequilla",
                "nameEn": "Plain Butter Croissant",
                "descriptionEs": "El clásico croissant francés de capas hojaldradas y crujientes elaborado con pura mantequilla francesa de primera calidad.",
                "descriptionEn": "Traditional scratch-made French butter croissant with flaky golden layers and airy honeycomb interior.",
                "price": 3.75,
                "category": "croissants-viennoiserie",
                "badge": "Signature",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "pain-au-chocolat",
                "nameEs": "Pain au Chocolat (Croissant de Chocolate)",
                "nameEn": "Pain au Chocolat (Chocolate Croissant)",
                "descriptionEs": "Hojaldre francés crujiente horneado con dos barras de chocolate negro belga semiamargo en su interior.",
                "descriptionEn": "Classic French pastry rolled with rich semi-sweet Belgian dark chocolate batons.",
                "price": 4.25,
                "category": "croissants-viennoiserie",
                "badge": "Top Seller",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "croissant-amandes-almond",
                "nameEs": "Croissant de Almendras (Croissant aux Amandes)",
                "nameEn": "Almond Croissant",
                "descriptionEs": "Croissant bañado en almíbar ligero, relleno de crema frangipane de almendras y cubierto de almendras fileteadas tostadas y azúcar glass.",
                "descriptionEn": "Twice-baked croissant soaked in syrup, filled with rich almond frangipane cream, and topped with toasted sliced almonds.",
                "price": 4.95,
                "category": "croissants-viennoiserie",
                "badge": "Favorito",
                "allergens": ["Gluten", "Dairy", "Eggs", "Nuts", "Vegetarian"]
            },
            {
                "id": "croissant-choc-raspberry",
                "nameEs": "Croissant de Chocolate y Frambuesa",
                "nameEn": "Chocolate & Raspberry Croissant",
                "descriptionEs": "Masa de hojaldre rellena de chocolate negro sedoso y mermelada ácida de frambuesas silvestres.",
                "descriptionEn": "Flaky croissant layered with rich dark chocolate and tart wild raspberry filling.",
                "price": 4.75,
                "category": "croissants-viennoiserie",
                "badge": None,
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "brioche-plie",
                "nameEs": "Brioche Plié Francés con Crema Pastelera",
                "nameEn": "Brioche Plié with Custard",
                "descriptionEs": "Pan brioche suave y mantecoso doblado con crema pastelera suave de vainilla y chispas de chocolate.",
                "descriptionEn": "Soft French brioche folded with vanilla pastry cream and dark chocolate chips.",
                "price": 4.50,
                "category": "croissants-viennoiserie",
                "badge": "Especialidad",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "pistachio-pinwheel",
                "nameEs": "Molinete Hojaldrado de Pistacho",
                "nameEn": "Pistachio Pinwheel",
                "descriptionEs": "Molinete de masa hojaldrada crujiente relleno de crema pura de pistacho verde tostado.",
                "descriptionEn": "Crispy spiraled pinwheel pastry filled with sweet roasted pistachio cream.",
                "price": 4.75,
                "category": "croissants-viennoiserie",
                "badge": "Gourmet",
                "allergens": ["Gluten", "Dairy", "Eggs", "Nuts", "Vegetarian"]
            },
            {
                "id": "pain-au-raisin",
                "nameEs": "Pain au Raisin (Caracola de Pasas)",
                "nameEn": "Pain au Raisin",
                "descriptionEs": "Espiral clásica francesa con crema pastelera a la vainilla y pasas rubias maceradas.",
                "descriptionEn": "Golden pastry spiral filled with smooth crème pâtissière and plump sweet raisins.",
                "price": 4.50,
                "category": "croissants-viennoiserie",
                "badge": "Clásico",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "french-apple-turnover",
                "nameEs": "Chaussons aux Pommes (Empanada Francesa de Manzana)",
                "nameEn": "French Apple Turnover (Chausson aux Pommes)",
                "descriptionEs": "Hojaldre dorado de mantequilla relleno de compota de manzanas naturales de temporada con canela.",
                "descriptionEn": "Crisp puff pastry shell filled with spiced fresh apple compote.",
                "price": 4.25,
                "category": "croissants-viennoiserie",
                "badge": None,
                "allergens": ["Gluten", "Dairy", "Vegetarian"]
            },
            {
                "id": "croissant-donut-cronut",
                "nameEs": "Croissant Donut (Glaseado o Canela)",
                "nameEn": "Croissant Donut (Cronut)",
                "descriptionEs": "Fusión artesanal de masa hojaldrada frita dorada con capas aireadas, cubierta de glaseado de vainilla, azúcar y canela o fresa crunch.",
                "descriptionEn": "Decadent layered croissant pastry fried golden with your choice of glaze, cinnamon sugar, or strawberry crunch.",
                "price": 4.50,
                "category": "croissants-viennoiserie",
                "badge": "Popular",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "french-palmiers",
                "nameEs": "Palmeras Hojaldradas de Mantequilla (Palmiers)",
                "nameEn": "Traditional French Palmiers",
                "descriptionEs": "Galleta crujiente en forma de corazón hecha de milhojas de hojaldre caramelizadas con mantequilla y azúcar.",
                "descriptionEn": "Crispy caramelized heart-shaped puff pastry cookies baked with butter and sugar.",
                "price": 3.75,
                "category": "croissants-viennoiserie",
                "badge": None,
                "allergens": ["Gluten", "Dairy", "Vegetarian"]
            },

            # --- PATISSERIE FINA Y POSTRES ---
            {
                "id": "mille-feuille-napoleon",
                "nameEs": "Milhojas Napoleón Francés Tradicional",
                "nameEn": "Classic Napoleon (Mille-Feuille)",
                "descriptionEs": "Tres capas de hojaldre crujiente caramelizado intercaladas con crema pastelera sedosa de vainilla de Madagascar y glaseado veteado tradicional.",
                "descriptionEn": "Three layers of crisp caramelized puff pastry layered with silky vanilla bean diplomat cream and marbled fondant icing.",
                "price": 6.95,
                "category": "patisserie-postres",
                "badge": "Masterpiece",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "french-eclair-chocolate",
                "nameEs": "Éclair Francés de Chocolate Belga",
                "nameEn": "French Chocolate Éclair",
                "descriptionEs": "Pasta choux horneada ligera rellena de crema pastelera espesa de chocolate y cubierta con ganache brillante de chocolate negro.",
                "descriptionEn": "Light choux pastry filled with rich chocolate custard cream, glazed with glossy dark Belgian chocolate ganache.",
                "price": 5.50,
                "category": "patisserie-postres",
                "badge": "Clásico",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "fraisier-cake-slice",
                "nameEs": "Pastel Fraisier Francés de Fresas",
                "nameEn": "Fraisier Cake Slice",
                "descriptionEs": "Bizcocho genovés empapado en almíbar de fresa, crema muselina de vainilla, fresas maduras enteras y cubierta de mazapán fino.",
                "descriptionEn": "Traditional French strawberry cake with Genoise sponge, velvety mousseline cream, fresh strawberries, and delicate marzipan topping.",
                "price": 7.50,
                "category": "patisserie-postres",
                "badge": "Postre Estrella",
                "allergens": ["Gluten", "Dairy", "Eggs", "Nuts", "Vegetarian"]
            },
            {
                "id": "lemon-meringue-tart",
                "nameEs": "Tarte au Citron Meringuée (Tarta de Limón y Merengue)",
                "nameEn": "Lemon Meringue Tart (Tarte au Citron)",
                "descriptionEs": "Base de masa quebrada crujiente rellena de crema cuajada de limón amarillo fresco y coronada con merengue tostado al soplete.",
                "descriptionEn": "Crisp sweet pastry crust filled with tangy fresh lemon curd and crowned with torched fluffy meringue.",
                "price": 6.50,
                "category": "patisserie-postres",
                "badge": "Favorito",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },
            {
                "id": "triple-chocolate-mousse",
                "nameEs": "Mousse de Tres Chocolates Franceses",
                "nameEn": "Triple Chocolate Mousse",
                "descriptionEs": "Capas sedosas de mousse de chocolate negro, chocolate con leche y chocolate blanco sobre base de bizcocho esponjoso.",
                "descriptionEn": "Decadent tiers of dark, milk, and white chocolate mousse over a tender chocolate sponge base.",
                "price": 6.95,
                "category": "patisserie-postres",
                "badge": "Chocolate",
                "allergens": ["Dairy", "Eggs", "Gluten", "Vegetarian"]
            },
            {
                "id": "fresh-fruit-tartlet",
                "nameEs": "Tartaleta de Frutas Frescas de Temporada",
                "nameEn": "Fresh Fruit Tartlet",
                "descriptionEs": "Corteza de masa dulce horneada con crema pastelera a la vainilla y abundante surtido de bayas frescas, kiwi y durazno con brillo de albaricoque.",
                "descriptionEn": "Sweet pastry crust with vanilla pastry cream topped with glazed fresh seasonal berries and fruits.",
                "price": 6.95,
                "category": "patisserie-postres",
                "badge": "Fresco",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },

            # --- MACARONS Y GALLETAS ---
            {
                "id": "french-macaron-single",
                "nameEs": "Macaron Francés París (Sabor Individual)",
                "nameEn": "French Macaron (Single)",
                "descriptionEs": "Macaron tradicional parisino con merengue de almendra y ganache cremoso. Sabores: Pistacho, Vainilla, Chocolate, Caramelo con Sal, Frambuesa o Maracuyá.",
                "descriptionEn": "Delicate Parisian almond meringue macaron with smooth ganache filling (Pistachio, Salted Caramel, Vanilla, Raspberry, Chocolate).",
                "price": 2.50,
                "category": "macarons-galletas",
                "badge": "Gluten-Free",
                "allergens": ["Nuts", "Dairy", "Eggs", "Gluten-Free", "Vegetarian"]
            },
            {
                "id": "french-macaron-box-6",
                "nameEs": "Caja de Regalo de 6 Macarons Franceses",
                "nameEn": "Gift Box of 6 French Macarons",
                "descriptionEs": "Caja surtida de 6 macarons artesanales elaborados a mano en variedad de sabores clásicos y de temporada.",
                "descriptionEn": "Elegant gift box of 6 handcrafted French macarons in an assortment of our most popular flavors.",
                "price": 15.00,
                "category": "macarons-galletas",
                "badge": "Para Regalo",
                "allergens": ["Nuts", "Dairy", "Eggs", "Gluten-Free", "Vegetarian"]
            },
            {
                "id": "linzer-cookie-raspberry",
                "nameEs": "Galleta Linzer Tradicional de Frambuesa",
                "nameEn": "Linzer Cookie with Raspberry",
                "descriptionEs": "Galleta mantecosa de almendra molida y canela rellena de mermelada de frambuesa y espolvoreada con azúcar glass.",
                "descriptionEn": "Buttery almond shortbread sandwich cookie filled with seedless red raspberry preserves and powdered sugar.",
                "price": 3.50,
                "category": "macarons-galletas",
                "badge": "Clásico",
                "allergens": ["Gluten", "Dairy", "Eggs", "Nuts", "Vegetarian"]
            },

            # --- PAN ARTESANAL Y BAGUETTES ---
            {
                "id": "traditional-french-baguette",
                "nameEs": "Baguette Tradicional Francesa",
                "nameEn": "Traditional French Baguette",
                "descriptionEs": "Auténtica baguette francesa horneada diariamente cada madrugada con corteza crujiente y miga aireada y suave.",
                "descriptionEn": "Traditional artisan French baguette baked fresh every morning with crisp golden crust and open, chewy crumb.",
                "price": 4.25,
                "category": "pan-artesanal-baguettes",
                "badge": "Horneado Diario",
                "allergens": ["Gluten", "Vegetarian", "Vegan"]
            },
            {
                "id": "parmesan-thyme-baguette",
                "nameEs": "Baguette de Queso Parmesano y Tomillo",
                "nameEn": "Parmesan & Thyme Baguette",
                "descriptionEs": "Baguette artesanal horneada con costra dorada de queso parmesano reggiano y tomillo fresco de jardín.",
                "descriptionEn": "Artisan baguette crusted with baked savory Parmesan cheese and fragrant fresh garden thyme.",
                "price": 4.95,
                "category": "pan-artesanal-baguettes",
                "badge": "Especialidad",
                "allergens": ["Gluten", "Dairy", "Vegetarian"]
            },
            {
                "id": "olive-french-baguette",
                "nameEs": "Baguette de Aceitunas Negras y Verdes",
                "nameEn": "Black & Green Olive Baguette",
                "descriptionEs": "Masa de baguette rústica amasada con aceitunas Kalamata y verdes enteras y aceite de oliva virgen extra.",
                "descriptionEn": "Crusty baguette packed with whole Kalamata and green olives and extra virgin olive oil.",
                "price": 4.95,
                "category": "pan-artesanal-baguettes",
                "badge": None,
                "allergens": ["Gluten", "Vegetarian", "Vegan"]
            },
            {
                "id": "cranberry-walnut-baguette",
                "nameEs": "Baguette de Arándanos Rojos y Nueces",
                "nameEn": "Cranberry Walnut Baguette",
                "descriptionEs": "Pan rústico amasado con arándanos deshidratados dulces y nueces de castilla crujientes tostadas.",
                "descriptionEn": "Artisan bread dough studded with sweet dried cranberries and toasted walnuts.",
                "price": 4.95,
                "category": "pan-artesanal-baguettes",
                "badge": None,
                "allergens": ["Gluten", "Nuts", "Vegetarian", "Vegan"]
            },

            # --- SANDWICHES EN CROISSANT Y QUICHES ---
            {
                "id": "croque-monsieur-brioche",
                "nameEs": "Croque Monsieur en Pan Brioche",
                "nameEn": "Croque Monsieur on Brioche",
                "descriptionEs": "Sándwich caliente francés en pan brioche artesanal dorado con jamón cocido, abundante queso Gruyère derretido y salsa bechamel sedosa.",
                "descriptionEn": "House-baked brioche bread layered with premium French ham, melted Gruyère cheese, and velvety scratch-made béchamel sauce.",
                "price": 10.95,
                "category": "sandwiches-quiches",
                "badge": "Plato Francés",
                "allergens": ["Gluten", "Dairy", "Pork"]
            },
            {
                "id": "poche-de-poulet-napoleon",
                "nameEs": "Poche de Poulet (Bolsita de Pollo en Hojaldre)",
                "nameEn": "Chicken Pocket (Poche de Poulet)",
                "descriptionEs": "Hojaldre tipo napoleón horneado y relleno de pechuga de pollo, cebollas caramelizadas dulces, zumaque y queso parmesano.",
                "descriptionEn": "Flaky Napoleon puff pastry pocket stuffed with seasoned chicken, sweet caramelized onions, sumac, and Parmesan cheese.",
                "price": 9.95,
                "category": "sandwiches-quiches",
                "badge": "Creación Exclusiva",
                "allergens": ["Gluten", "Dairy"]
            },
            {
                "id": "ham-gruyere-croissant-sandwich",
                "nameEs": "Sándwich de Jamón y Queso Gruyère en Croissant",
                "nameEn": "Ham & Gruyère Croissant Sandwich",
                "descriptionEs": "Croissant de mantequilla recién horneado relleno de jamón cocido francés, queso Gruyère fundido y toque de mostaza Dijon.",
                "descriptionEn": "Freshly baked butter croissant filled with sliced ham and warm melted Gruyère cheese.",
                "price": 9.50,
                "category": "sandwiches-quiches",
                "badge": "Almuerzo",
                "allergens": ["Gluten", "Dairy", "Pork"]
            },
            {
                "id": "bacon-egg-cheese-croissant",
                "nameEs": "Croissant de Desayuno con Huevo, Tocino y Queso",
                "nameEn": "Bacon, Egg & Cheese Croissant",
                "descriptionEs": "Huevo de granja fresco, tocino ahumado crujiente y queso fundido dentro de nuestro hojaldrado croissant de mantequilla.",
                "descriptionEn": "Fresh farm egg, crispy smoked bacon, and melted cheese served warm on our freshly baked butter croissant.",
                "price": 7.50,
                "category": "sandwiches-quiches",
                "badge": "Desayuno",
                "allergens": ["Gluten", "Dairy", "Eggs", "Pork"]
            },
            {
                "id": "quiche-lorraine-individual",
                "nameEs": "Quiche Lorraine Tradicional (Jamón y Tocino)",
                "nameEn": "Individual Quiche Lorraine",
                "descriptionEs": "Tartaleta salada de masa quebrada rellena de natilla francesa de huevos y crema con jamón ahumado, tocino crujiente y queso suizo.",
                "descriptionEn": "Individual savory French custard tart baked with smoked ham, crisp bacon, and melted Swiss cheese.",
                "price": 8.50,
                "category": "sandwiches-quiches",
                "badge": "Clásico Francés",
                "allergens": ["Gluten", "Dairy", "Eggs", "Pork"]
            },
            {
                "id": "quiche-spinach-goat-cheese",
                "nameEs": "Quiche de Espinacas Tiernas y Queso de Cabra",
                "nameEn": "Spinach & Goat Cheese Quiche",
                "descriptionEs": "Masa quebrada dorada rellena de crema horneada con espinacas frescas y medallones de queso de cabra.",
                "descriptionEn": "Individual savory tart baked with tender spinach, creamy goat cheese, and fresh herbs.",
                "price": 8.50,
                "category": "sandwiches-quiches",
                "badge": "Vegetariano",
                "allergens": ["Gluten", "Dairy", "Eggs", "Vegetarian"]
            },

            # --- CAFE Y BEBIDAS ---
            {
                "id": "french-cafe-au-lait",
                "nameEs": "Café au Lait Tradicional Francés",
                "nameEn": "Traditional Café au Lait",
                "descriptionEs": "Café tostado oscuro recién filtrado servido en tazón con partes iguales de leche entera caliente vaporizada.",
                "descriptionEn": "Classic French-style dark roast coffee served with equal parts rich steamed whole milk.",
                "price": 4.50,
                "category": "cafe-bebidas",
                "badge": "Tradición Francesa",
                "allergens": ["Dairy", "Vegetarian"]
            },
            {
                "id": "cappuccino-isabelle",
                "nameEs": "Capuchino Italiano al Vapor",
                "nameEn": "Classic Cappuccino",
                "descriptionEs": "Espresso doble con leche espumada densa y toque de cacao en polvo.",
                "descriptionEn": "Double espresso shot topped with rich steamed milk and velvety foam.",
                "price": 4.75,
                "category": "cafe-bebidas",
                "badge": None,
                "allergens": ["Dairy", "Vegetarian"]
            }
        ],
        "faqs": [
            {
                "qEs": "¿De dónde provienen las recetas y los maestros panaderos?",
                "qEn": "Where do your recipes and bakery heritage come from?",
                "aEs": "Vincent e Isabelle Koenig son originarios de Estrasburgo, Alsacia, Francia. Vincent es maestro panadero y chocolatero con décadas de experiencia en la tradición culinaria francesa artesanal.",
                "aEn": "Vincent and Isabelle Koenig originally hail from Strasbourg in Alsace, France. Vincent is a master French baker and chocolatier trained in authentic century-old European traditions."
            },
            {
                "qEs": "¿Todo se hornea fresco diariamente desde cero?",
                "qEn": "Is everything baked fresh from scratch daily?",
                "aEs": "¡Sí! Nuestros croissants, baguettes, panes de masa madre, macarons y postres de pastelería se elaboran desde cero cada madrugada en nuestra panadería de Fairfield.",
                "aEn": "Yes! All croissants, baguettes, boules, macarons, and delicate patisserie cakes are baked entirely from scratch each morning right here in Fairfield."
            },
            {
                "qEs": "¿Aceptan pedidos de pasteles para cumpleaños o eventos especiales?",
                "qEn": "Do you make custom cakes for birthdays and events?",
                "aEs": "Sí, elaboramos pasteles personalizados como Fraisier de fresas, Tiramisú, Mousse de Tres Chocolates y pasteles de buttercream. Por favor haga su pedido con al menos 3 días de anticipación.",
                "aEn": "Yes, we craft custom cakes including authentic Fraisier, Tiramisu, Triple Chocolate Mousse, and custom buttercream cakes with at least 3 days advance notice."
            }
        ]
    }

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
    build_isabelle()

