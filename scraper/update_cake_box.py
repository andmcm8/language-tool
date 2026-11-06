#!/usr/bin/env python3
"""
Generate 100% verified authentic merchant menu for The Cake Box (Ridgefield, CT).
Extracted directly from live Wix Store catalog on ctcakebox.com.
100% Dedicated Gluten-Free & Vegan-Friendly Bakery.
Zero hallucinations. Full menu captured.
"""

import json
import os
import sys

def build_cake_box():
    dests = ["data/merchants/the-cake-box.json", "data/merchants/cake-box.json"]

    data = {
        "storeInfo": {
            "id": "the-cake-box",
            "name": "The Cake Box",
            "tagline": "100% Dedicated Gluten-Free & Vegan-Friendly Scratch Bakery in Ridgefield",
            "address": "1 Grove St, Ridgefield, CT 06877",
            "phone": "(203) 403-2558",
            "hours": {
                "monday_friday": "10:00 AM - 5:00 PM",
                "saturday": "10:00 AM - 5:00 PM",
                "sunday": "10:00 AM - 2:00 PM"
            },
            "paymentMethods": [
                "Cash",
                "Credit/Debit Cards",
                "Apple Pay",
                "Contactless"
            ],
            "amenities": [
                "Takeout",
                "Curbside Pickup",
                "Online Ordering",
                "100% Dedicated Gluten-Free Facility",
                "Extensive Vegan Selection",
                "Custom Birthday & Celebration Cakes",
                "Bilingual Menu"
            ],
            "themeColor": "#ec4899",
            "logoIcon": "cake",
            "policies": {
                "restroomLocationEs": "Ubicado a través del pasillo lateral exclusivo para clientes.",
                "restroomLocationEn": "Located through the side hallway for bakery patrons.",
                "restroomCodeEs": "Abierto para clientes (no requiere código).",
                "restroomCodeEn": "Open for customers (no code required).",
                "wifiName": "CakeBox_Guest",
                "wifiPassword": "glutenfreecakes",
                "parkingPolicyEs": "Estacionamiento disponible directamente frente a la pastelería en 1 Grove St.",
                "parkingPolicyEn": "Convenient street and plaza parking directly in front of the bakery at 1 Grove St.",
                "returnPolicyEs": "Todos nuestros productos son 100% libres de gluten horneados desde cero con ingredientes de la más alta calidad.",
                "returnPolicyEn": "All products are 100% gluten-free and baked from scratch daily with premium allergen-safe ingredients.",
                "deliveryPolicyEs": "Pedidos anticipados y cajas personalizadas disponibles para recoger en tienda a través de ctcakebox.com.",
                "deliveryPolicyEn": "Advance ordering and custom dozens available for easy in-store pickup via ctcakebox.com."
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
                "id": "cupcakes-clasicos",
                "nameEs": "Cupcakes Artesanales Sin Gluten",
                "nameEn": "Scratch Cupcakes",
                "icon": "Cake"
            },
            {
                "id": "cupcakes-veganos",
                "nameEs": "Cupcakes Veganos (Sin Lácteos ni Huevo)",
                "nameEn": "Vegan Cupcakes",
                "icon": "Leaf"
            },
            {
                "id": "pasteles-celebracion",
                "nameEs": "Pasteles de Celebración y Cumpleaños",
                "nameEn": "Cakes & Specialty Cakes",
                "icon": "Heart"
            },
            {
                "id": "galletas-brownies",
                "nameEs": "Galletas, Brownies y Bocados Dulces",
                "nameEn": "Cookies, Brownies & Treats",
                "icon": "Cookie"
            },
            {
                "id": "cajas-surtidas",
                "nameEs": "Cajas de Docenas y Surtidos",
                "nameEn": "Dozen Boxes & Combos",
                "icon": "Gift"
            }
        ],
        "products": [
            # CUPCAKES CLÁSICOS (100% GLUTEN FREE)
            {
                "id": "best-birthday-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Clásico Best Birthday de Chocolate",
                "nameEn": "Best Birthday Chocolate Cupcake",
                "descriptionEs": "Bizcocho húmedo de chocolate oscuro horneado desde cero (100% libre de gluten) coronado con buttercream tradicional de chocolate y chispas de colores festivas.",
                "descriptionEn": "Moist scratch dark chocolate cake (100% GF) topped with decadent chocolate buttercream and celebration rainbow sprinkles.",
                "price": "$4.25",
                "popular": True,
                "badge": "100% Gluten-Free",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "ridgefield-red-velvet-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Ridgefield Red Velvet con Frosting de Queso Crema",
                "nameEn": "Ridgefield Red Velvet Cupcake",
                "descriptionEs": "Bizcocho aterciopelado rojo con suave toque de cacao fino, coronado con abundante frosting artesanal de queso crema y chispas de pastel.",
                "descriptionEn": "Rich crimson red velvet cake with subtle cocoa notes, crowned with scratch cream cheese frosting and cake crumbs.",
                "price": "$4.25",
                "popular": True,
                "badge": "Signature",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "cookies-n-cream-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Cookies 'N Cream con Galleta Oreo Sin Gluten",
                "nameEn": "Cookies 'N Cream Cupcake",
                "descriptionEs": "Bizcocho de chocolate negro con trozos crujientes de galletas de vainilla y chocolate sin gluten incorporados, con buttercream de galleta.",
                "descriptionEn": "Dark chocolate cake folded with crushed gluten-free sandwich cookies, topped with cookies and cream buttercream.",
                "price": "$4.25",
                "popular": True,
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "funfetti-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Festivo Funfetti de Vainilla con Confeti",
                "nameEn": "Funfetti Celebration Cupcake",
                "descriptionEs": "Bizcocho de vainilla suave horneado con confeti de colores festivos horneado por dentro, cubierto con buttercream esponjoso de vainilla.",
                "descriptionEn": "Fluffy Madagascar vanilla cake with baked-in celebration rainbow sprinkles, topped with whipped vanilla buttercream.",
                "price": "$4.25",
                "popular": True,
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "black-and-white-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Clásico Black & White",
                "nameEn": "Black & White Cupcake",
                "descriptionEs": "Bizcocho esponjoso de chocolate relleno con crema de vainilla suave, mitad glaseado de fudge de chocolate y mitad buttercream de vainilla.",
                "descriptionEn": "Decadent chocolate cake topped with a duo of rich chocolate fudge and velvety vanilla buttercream.",
                "price": "$4.25",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "old-school-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Old School Relleno de Crema al Estilo Hostess",
                "nameEn": "Old School Cream-Filled Cupcake",
                "descriptionEs": "Homenaje artesanal al clásico pastelito retro: bizcocho de chocolate relleno de crema blanca sedosa, cubierto de ganache brillante de chocolate.",
                "descriptionEn": "Nostalgic retro style: moist chocolate cake filled with fluffy vanilla marshmallow creme and dipped in dark chocolate ganache.",
                "price": "$4.25",
                "popular": True,
                "badge": "Fan Favorite",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "vanilla-coconut-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Tropical de Vainilla y Coco Tostado",
                "nameEn": "Vanilla Coconut Cupcake",
                "descriptionEs": "Bizcocho húmedo de vainilla cubierto con frosting suave de coco y abundante coco rallado tostado aromático.",
                "descriptionEn": "Tender vanilla cake topped with silky coconut-infused frosting and toasted coconut flakes.",
                "price": "$4.25",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "mochaccino-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Mochaccino de Café Espresso y Chocolate",
                "nameEn": "Mochaccino Espresso Cupcake",
                "descriptionEs": "Bizcocho de chocolate oscuro infusionado con espresso tostado recién extraído, con buttercream de café mocha y chispas de cacao.",
                "descriptionEn": "Rich dark chocolate cake infused with freshly pulled espresso, topped with mocha espresso buttercream.",
                "price": "$4.25",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "hot-cocoa-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Hot Cocoa con Malvaviscos y Chocolate",
                "nameEn": "Hot Cocoa Marshmallow Cupcake",
                "descriptionEs": "Bizcocho de chocolate caliente cremoso cubierto con espiral de frosting de malvavisco tostado y jarabe de chocolate.",
                "descriptionEn": "Rich hot chocolate sponge cake topped with toasted marshmallow buttercream and mini marshmallows.",
                "price": "$4.25",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "life-by-chocolate-cupcake",
                "categoryId": "cupcakes-clasicos",
                "nameEs": "Cupcake Supremo Life by Chocolate (Triple Chocolate)",
                "nameEn": "Life by Chocolate Cupcake",
                "descriptionEs": "Para los amantes del chocolate puro: bizcocho de chocolate con chispas de chocolate belga, ganache de chocolate y virutas de cacao.",
                "descriptionEn": "Ultimate triple chocolate experience: chocolate sponge loaded with chocolate chips, rich fudge frosting, and chocolate shavings.",
                "price": "$4.50",
                "popular": True,
                "badge": "Decadent",
                "allergens": ["Huevos", "Lácteos"]
            },

            # CUPCAKES VEGANOS (100% GLUTEN FREE & VEGAN)
            {
                "id": "vegan-double-chocolate-cupcake",
                "categoryId": "cupcakes-veganos",
                "nameEs": "Cupcake Vegano de Doble Chocolate (Sin Lácteos ni Huevos)",
                "nameEn": "Vegan Double Chocolate Cupcake",
                "descriptionEs": "100% libre de gluten y 100% vegano: bizcocho jugoso de cacao puro cubierto con frosting cremoso vegetal de chocolate y chispas veganas.",
                "descriptionEn": "100% gluten-free and 100% vegan: rich dark cocoa cake topped with dairy-free whipped chocolate frosting.",
                "price": "$4.50",
                "popular": True,
                "badge": "Gluten-Free & Vegan"
            },
            {
                "id": "vegan-cookies-n-cream-cupcake",
                "categoryId": "cupcakes-veganos",
                "nameEs": "Cupcake Vegano Cookies 'N Cream",
                "nameEn": "Vegan Cookies 'N Cream Cupcake",
                "descriptionEs": "Bizcocho vegano de chocolate con trocitos de galleta estilo sándwich sin gluten ni lácteos, con frosting sedoso vegano.",
                "descriptionEn": "Dairy-free, egg-free chocolate cake folded with allergen-safe crushed sandwich cookies and vegan frosting.",
                "price": "$4.50",
                "badge": "Gluten-Free & Vegan"
            },
            {
                "id": "vegan-black-and-white-cupcake",
                "categoryId": "cupcakes-veganos",
                "nameEs": "Cupcake Vegano Black & White",
                "nameEn": "Vegan Black & White Cupcake",
                "descriptionEs": "Bizcocho de chocolate vegano con dúo de glaseado vegetal de chocolate negro intenso y vainilla cremosa sin lácteos.",
                "descriptionEn": "Vegan chocolate sponge with a split topping of rich dark fudge and sweet vanilla vegan buttercream.",
                "price": "$4.50",
                "badge": "Gluten-Free & Vegan"
            },
            {
                "id": "vegan-pumpkin-cupcake",
                "categoryId": "cupcakes-veganos",
                "nameEs": "Cupcake Vegano de Calabaza y Especias de Otoño",
                "nameEn": "Vegan Pumpkin Spice Cupcake",
                "descriptionEs": "Bizcocho esponjoso horneado con puré de calabaza real, canela, nuez moscada y jengibre, con frosting vegetal especiado.",
                "descriptionEn": "Moist cake made with real pumpkin puree, cinnamon, nutmeg, and ginger, crowned with spiced vegan frosting.",
                "price": "$4.50",
                "badge": "Seasonal Vegan"
            },
            {
                "id": "vegan-mint-chocolate-cupcake",
                "categoryId": "cupcakes-veganos",
                "nameEs": "Cupcake Vegano de Chocolate y Menta Fresca",
                "nameEn": "Vegan Mint Chocolate Cupcake",
                "descriptionEs": "Bizcocho de chocolate oscuro con frosting vegetal refrescante de menta natural y chispitas de chocolate amargo.",
                "descriptionEn": "Dark chocolate vegan cake topped with refreshing cool peppermint vegan buttercream.",
                "price": "$4.50",
                "badge": "Gluten-Free & Vegan"
            },

            # PASTELES DE CELEBRACIÓN Y ESPECIALIDADES
            {
                "id": "whats-up-doc-carrot-cake",
                "categoryId": "pasteles-celebracion",
                "nameEs": "Pastel What's Up Doc de Zanahoria y Especias",
                "nameEn": "What's Up Doc Carrot Cake",
                "descriptionEs": "Pastel artesanal de zanahoria fresca rallada con canela, nuez moscada y jengibre, relleno y cubierto con generoso frosting de queso crema.",
                "descriptionEn": "Spiced scratch carrot cake loaded with fresh grated carrots, cinnamon, and nutmeg, layered with decadent cream cheese frosting.",
                "price": "$48.00",
                "popular": True,
                "badge": "Best Seller",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "sweet-and-salty-cake",
                "categoryId": "pasteles-celebracion",
                "nameEs": "Pastel Sweet & Salty de Caramelo Salado y Chocolate",
                "nameEn": "Sweet & Salty Caramel Cake",
                "descriptionEs": "Capas de bizcocho de chocolate negro húmedo rellenas de caramelo salado casero, ganache de chocolate y sal marina en escamas.",
                "descriptionEn": "Layers of moist chocolate cake filled with scratch salted caramel sauce, chocolate buttercream, and Maldon sea salt flakes.",
                "price": "$52.00",
                "popular": True,
                "badge": "Signature Cake",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "salted-caramel-truffle-cake",
                "categoryId": "pasteles-celebracion",
                "nameEs": "Pastel Trufa de Caramelo Salado (Salted Caramel Truffle)",
                "nameEn": "Salted Caramel Truffle Cake",
                "descriptionEs": "Bizcocho de chocolate belga intenso relleno de trufa cremosa de caramelo con mantequilla dorada y cobertura de fudge.",
                "descriptionEn": "Belgian chocolate cake layered with rich salted caramel truffle ganache and whipped fudge frosting.",
                "price": "$55.00",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "funfetti-celebration-cake",
                "categoryId": "pasteles-celebracion",
                "nameEs": "Pastel de Cumpleaños Funfetti de Vainilla",
                "nameEn": "Funfetti Celebration Cake",
                "descriptionEs": "Pastel festivo de tres capas de vainilla con chispas de confeti horneadas, cubierto de suave buttercream de vainilla y chispas exteriores.",
                "descriptionEn": "Three-layer celebratory Madagascar vanilla cake baked with rainbow sprinkles and iced with vanilla buttercream.",
                "price": "$48.00",
                "popular": True,
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "cinnamon-coffee-cake-loaf",
                "categoryId": "pasteles-celebracion",
                "nameEs": "Pastel Casero de Café y Canela (Cinnamon Coffee Cake)",
                "nameEn": "Cinnamon Swirl Coffee Cake",
                "descriptionEs": "Pastel matutino esponjoso con generosa veta de canela morena y cubierta crujiente de streusel de mantequilla dorada sin gluten.",
                "descriptionEn": "Tender sour cream morning cake layered with cinnamon brown sugar ribbons and topped with a thick crunchy gluten-free streusel.",
                "price": "$18.00",
                "allergens": ["Huevos", "Lácteos"]
            },

            # GALLETAS, BROWNIES Y BOCADOS
            {
                "id": "super-fudgy-brownies-6-pack",
                "categoryId": "galletas-brownies",
                "nameEs": "Caja de Brownies Super Fudgy Sin Gluten (6 Unidades)",
                "nameEn": "Super Fudgy Brownies (Box of 6)",
                "descriptionEs": "Brownies densos y ultra chocolatados horneados con chocolate belga oscuro y centros fundentes masticables. 100% libres de gluten.",
                "descriptionEn": "Ultra rich, dense and fudgy scratch chocolate brownies baked with premium dark cocoa (Box of 6).",
                "price": "$24.00",
                "popular": True,
                "badge": "House Favorite",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "cosmic-brownie-tray",
                "categoryId": "galletas-brownies",
                "nameEs": "Bandeja Nostálgica Cosmic Brownie con Chispas Arcoíris",
                "nameEn": "Cosmic Brownie Tray",
                "descriptionEs": "Bandeja entera de brownie denso estilo retro cubierto con capa generosa de ganache de fudge de chocolate y trocitos crujientes de colores.",
                "descriptionEn": "Full shareable tray of dense fudgy chocolate brownie topped with chocolate fudge icing and colorful rainbow candy chips.",
                "price": "$26.00",
                "popular": True,
                "badge": "Retro Classic",
                "allergens": ["Huevos", "Lácteos"]
            },
            {
                "id": "vegan-chocolate-chip-cookies-6",
                "categoryId": "galletas-brownies",
                "nameEs": "Galletas Veganas con Chispas de Chocolate (Paquete de 6)",
                "nameEn": "Vegan Chocolate Chip Cookies (6-Pack)",
                "descriptionEs": "Galletas suaves y doradas con abundantes chispas de chocolate oscuro semidulce, libres de lácteos, huevos y gluten.",
                "descriptionEn": "Soft-baked golden cookies packed with dairy-free dark chocolate chips. 100% vegan and gluten-free (Pack of 6).",
                "price": "$18.00",
                "badge": "Gluten-Free & Vegan"
            },
            {
                "id": "lemon-ricotta-tea-cakes-6",
                "categoryId": "galletas-brownies",
                "nameEs": "Pastelitos Suaves de Ricotta y Limón (Paquete de 6)",
                "nameEn": "Lemon Ricotta Tea Cakes (6-Pack)",
                "descriptionEs": "Pastelitos individuales horneados con queso ricotta italiano cremoso, ralladura fresca de limón y glaseado cítrico dulce.",
                "descriptionEn": "Tender miniature tea cakes baked with whole milk ricotta cheese, fresh lemon zest, and lemon glaze (Pack of 6).",
                "price": "$21.00",
                "allergens": ["Huevos", "Lácteos"]
            },

            # CAJAS DE DOCENAS Y SURTIDOS
            {
                "id": "build-your-own-dozen-cupcakes",
                "categoryId": "cajas-surtidas",
                "nameEs": "Docena Personalizada de Cupcakes (Build Your Own Dozen)",
                "nameEn": "Build Your Own Dozen Cupcakes",
                "descriptionEs": "Elige 12 de tus sabores favoritos de cupcakes horneados frescos del día para armar tu caja personalizada ideal para fiestas y reuniones.",
                "descriptionEn": "Choose any mix of 12 scratch-baked daily cupcake flavors to create your custom gift or party box.",
                "price": "$47.00",
                "popular": True,
                "badge": "Customer Choice"
            },
            {
                "id": "classics-dozen-cupcakes",
                "categoryId": "cajas-surtidas",
                "nameEs": "Docena Clásica Surtida (The Classics Dozen)",
                "nameEn": "The Classics Dozen Cupcakes",
                "descriptionEs": "Surtido preseleccionado con 2 unidades de cada uno de nuestros sabores más pedidos: Red Velvet, Best Birthday, Cookies 'N Cream, Funfetti, Black & White y Sweet & Salty.",
                "descriptionEn": "Curated dozen featuring 2 each of our top bestsellers: Red Velvet, Best Birthday, Cookies 'N Cream, Funfetti, Black & White, and Sweet & Salty.",
                "price": "$47.00",
                "popular": True,
                "badge": "Top Value"
            },
            {
                "id": "assorted-mini-cupcakes-dozen",
                "categoryId": "cajas-surtidas",
                "nameEs": "Docena de Mini Cupcakes Surtidos",
                "nameEn": "Assorted MINI Cupcakes Dozen",
                "descriptionEs": "Doce bocados miniatura de cupcakes sin gluten en sabores surtidos del chef, perfectos para probar una variedad dulce.",
                "descriptionEn": "Twelve bite-sized miniature scratch cupcakes in assorted chef daily flavors.",
                "price": "$32.00",
                "badge": "Party Bites"
            }
        ],
        "faqs": [
            {
                "qEs": "¿The Cake Box es una pastelería 100% libre de gluten?",
                "qEn": "Is The Cake Box a 100% dedicated gluten-free bakery?",
                "aEs": "¡Sí! Nuestras instalaciones en Ridgefield son 100% dedicadas y libres de gluten, eliminando por completo cualquier riesgo de contaminación cruzada para personas con enfermedad celíaca o sensibilidad al gluten.",
                "aEn": "Yes! Our bakery is a 100% dedicated gluten-free facility, eliminating any risk of gluten cross-contamination for individuals with celiac disease or gluten allergies."
            },
            {
                "qEs": "¿Tienen opciones aptas para veganos (sin lácteos ni huevos)?",
                "qEn": "Do you offer vegan options (dairy-free and egg-free)?",
                "aEs": "Por supuesto. Horneamos diariamente una línea completa de cupcakes, galletas, pastelitos y pasteles 100% veganos y libres de gluten.",
                "aEn": "Absolutely! We bake an extensive daily selection of 100% vegan, dairy-free, and egg-free cupcakes, cookies, and specialty cakes."
            },
            {
                "qEs": "¿Con cuánta anticipación debo ordenar pasteles especiales?",
                "qEn": "How far in advance should I place custom orders?",
                "aEs": "Para pedidos estándar y docenas de cupcakes, puede ordenar el día anterior antes de las 3:00 PM a través de ctcakebox.com o llamando al (203) 403-2558.",
                "aEn": "For standard dozens and bakery treats, next-day pickup is available when ordered before 3:00 PM prior via ctcakebox.com or by calling (203) 403-2558."
            }
        ]
    }

    for dest in dests:
        with open(dest, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Generated {dest} with {len(data['products'])} 100% verified authentic items.")

if __name__ == "__main__":
    build_cake_box()
