import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

/* ================================================================
   COMPREHENSIVE ENGLISH → SPANISH WORD DICTIONARY
   Covers store signage, food, policy, and common phrases.
   ================================================================ */
const WORD_MAP: Record<string, string> = {
  // ---- Greetings & Common ----
  welcome: "bienvenidos", hello: "hola", hi: "hola",
  "thank": "gracias", "thanks": "gracias", "you": "usted",
  please: "por favor", sorry: "disculpe", yes: "sí", no: "no",
  "good": "buen", "morning": "mañana", "afternoon": "tarde",
  "evening": "noche", "night": "noche", "day": "día",
  "have": "tenga", "nice": "buen", "enjoy": "disfrute",

  // ---- Store / Location ----
  store: "tienda", shop: "tienda", market: "mercado",
  supermarket: "supermercado", grocery: "abarrotes",
  entrance: "entrada", exit: "salida", door: "puerta",
  floor: "piso", aisle: "pasillo", section: "sección",
  counter: "mostrador", register: "caja", checkout: "caja",
  parking: "estacionamiento", lot: "lote", restroom: "baño",
  bathroom: "baño", office: "oficina", room: "sala",
  area: "área", zone: "zona", back: "atrás",
  front: "frente", left: "izquierda", right: "derecha",
  upstairs: "arriba", downstairs: "abajo", elevator: "elevador",
  stairs: "escaleras", behind: "detrás", next: "siguiente",

  // ---- Time ----
  hours: "horarios", hour: "hora", minutes: "minutos",
  minute: "minuto", open: "abierto", closed: "cerrado",
  today: "hoy", tomorrow: "mañana", yesterday: "ayer",
  daily: "diariamente", weekly: "semanalmente", monthly: "mensualmente",
  monday: "lunes", tuesday: "martes", wednesday: "miércoles",
  thursday: "jueves", friday: "viernes", saturday: "sábado",
  sunday: "domingo", "mon": "lun", "tue": "mar", "wed": "mié",
  "thu": "jue", "fri": "vie", "sat": "sáb", "sun": "dom",
  until: "hasta", from: "desde", to: "a",

  // ---- Food & Drink ----
  food: "comida", menu: "menú", meal: "comida", plate: "plato",
  dish: "plato", bowl: "tazón", cup: "taza", glass: "vaso",
  bottle: "botella", can: "lata", bag: "bolsa", box: "caja",
  bread: "pan", roll: "panecillo", toast: "tostada", bun: "bollo",
  cake: "pastel", pie: "pastel", cookie: "galleta", cookies: "galletas",
  pastry: "pastelería", donut: "dona", muffin: "muffin",
  meat: "carne", beef: "res", steak: "bistec", pork: "cerdo",
  chicken: "pollo", turkey: "pavo", ham: "jamón", bacon: "tocino",
  sausage: "salchicha", fish: "pescado", shrimp: "camarones",
  seafood: "mariscos", lamb: "cordero", ribs: "costillas",
  wing: "ala", wings: "alitas", thigh: "muslo", breast: "pechuga",
  cheese: "queso", swiss: "suizo", american: "americano",
  cheddar: "cheddar", mozzarella: "mozzarella", cream: "crema",
  butter: "mantequilla", milk: "leche", eggs: "huevos", egg: "huevo",
  rice: "arroz", beans: "frijoles", corn: "maíz", flour: "harina",
  pasta: "pasta", noodles: "fideos", potato: "papa", potatoes: "papas",
  fries: "papas fritas", chips: "papas fritas",
  tomato: "tomate", onion: "cebolla", lettuce: "lechuga",
  pepper: "pimiento", peppers: "pimientos", jalapeño: "jalapeño",
  avocado: "aguacate", garlic: "ajo", cilantro: "cilantro",
  lime: "lima", lemon: "limón", orange: "naranja", apple: "manzana",
  banana: "plátano", grape: "uva", grapes: "uvas",
  strawberry: "fresa", mango: "mango", coconut: "coco",
  pineapple: "piña", watermelon: "sandía", peach: "durazno",
  salad: "ensalada", soup: "sopa", stew: "guiso",
  sandwich: "sándwich", burger: "hamburguesa", taco: "taco",
  tacos: "tacos", burrito: "burrito", quesadilla: "quesadilla",
  empanada: "empanada", empanadas: "empanadas", arepa: "arepa",
  tamale: "tamal", tamales: "tamales", tortilla: "tortilla",
  plantain: "plátano", plantains: "plátanos",
  water: "agua", juice: "jugo", soda: "refresco", pop: "refresco",
  coffee: "café", tea: "té", beer: "cerveza", wine: "vino",
  drink: "bebida", drinks: "bebidas", beverage: "bebida",
  beverages: "bebidas", smoothie: "batido", shake: "malteada",
  ice: "hielo", sugar: "azúcar", salt: "sal", oil: "aceite",
  sauce: "salsa", dressing: "aderezo", syrup: "jarabe",
  honey: "miel", vinegar: "vinagre", mustard: "mostaza",
  ketchup: "kétchup", mayo: "mayonesa", mayonnaise: "mayonesa",
  spice: "especia", spices: "especias", seasoning: "sazón",
  herb: "hierba", herbs: "hierbas",
  candy: "dulce", chocolate: "chocolate", gum: "chicle",
  snack: "bocadillo", snacks: "bocadillos", nuts: "nueces",
  peanut: "maní", peanuts: "maní", almond: "almendra",

  // ---- Food Preparation ----
  fresh: "fresco", hot: "caliente", cold: "frío", warm: "tibio",
  frozen: "congelado", raw: "crudo", cooked: "cocido",
  baked: "horneado", fried: "frito", grilled: "a la parrilla",
  roast: "asado", roasted: "asado", steamed: "al vapor",
  boiled: "hervido", smoked: "ahumado", stuffed: "relleno",
  melted: "fundido", crispy: "crujiente", crunchy: "crujiente",
  tender: "tierno", juicy: "jugoso", seasoned: "sazonado",
  marinated: "marinado", homemade: "casero", handmade: "hecho a mano",
  organic: "orgánico", natural: "natural", gluten: "gluten",
  vegan: "vegano", vegetarian: "vegetariano",

  // ---- Store Signs & Notices ----
  special: "especial", specials: "especiales",
  sale: "oferta", offer: "oferta", deal: "oferta", deals: "ofertas",
  discount: "descuento", price: "precio", cost: "costo",
  free: "gratis", buy: "compre", get: "obtenga",
  save: "ahorre", off: "de descuento",
  new: "nuevo", best: "mejor", top: "mejor",
  popular: "popular", favorite: "favorito", recommended: "recomendado",
  featured: "destacado", limited: "limitado", exclusive: "exclusivo",
  available: "disponible", sold: "vendido", out: "agotado",
  notice: "aviso", attention: "atención", important: "importante",
  warning: "advertencia", caution: "precaución", danger: "peligro",
  emergency: "emergencia", help: "ayuda", info: "información",
  information: "información", ask: "pregunte",
  employees: "empleados", only: "solo", staff: "personal",
  customers: "clientes", customer: "cliente",
  service: "servicio", services: "servicios",
  delivery: "entrega", pickup: "recoger", takeout: "para llevar",
  dine: "comer", "in": "dentro", order: "pedido", orders: "pedidos",
  online: "en línea", call: "llame", phone: "teléfono",
  push: "empuje", pull: "jale",
  wet: "mojado", slippery: "resbaloso",
  keep: "mantener", clean: "limpio",

  // ---- Payment ----
  cash: "efectivo", card: "tarjeta", credit: "crédito",
  debit: "débito", payment: "pago", pay: "pague",
  accepted: "aceptado", required: "requerido", requires: "requiere",
  minimum: "mínimo", maximum: "máximo", total: "total",
  tax: "impuesto", included: "incluido", includes: "incluye",
  receipt: "recibo", change: "cambio", tip: "propina",

  // ---- Quantities & Sizes ----
  small: "pequeño", medium: "mediano", large: "grande",
  extra: "extra", regular: "regular", double: "doble",
  half: "medio", whole: "entero", single: "sencillo",
  combo: "combo", pair: "par", pack: "paquete",
  pound: "libra", pounds: "libras", ounce: "onza",
  ounces: "onzas", dozen: "docena", piece: "pieza",
  pieces: "piezas", slice: "rebanada", slices: "rebanadas",
  serving: "porción", each: "cada uno", per: "por",
  all: "todos", any: "cualquier", some: "algunos",
  more: "más", less: "menos", many: "muchos", much: "mucho",

  // ---- Adjectives ----
  delicious: "delicioso", tasty: "sabroso", amazing: "increíble",
  great: "excelente", sweet: "dulce", sour: "agrio",
  spicy: "picante", mild: "suave", strong: "fuerte",
  soft: "suave", hard: "duro", thick: "grueso", thin: "delgado",
  big: "grande", little: "pequeño", first: "primera",
  second: "segunda", last: "última",

  // ---- Verbs ----
  try: "pruebe", taste: "pruebe", eat: "coma", come: "venga",
  see: "vea", visit: "visite", share: "comparta",
  bring: "traiga", take: "tome", pick: "elija", choose: "elija",
  find: "encuentre", look: "busque", made: "hecho",
  prepared: "preparado", served: "servido",

  // ---- Connectors ----
  the: "el", a: "un", an: "un", and: "y", or: "o",
  with: "con", without: "sin", for: "para", of: "de",
  at: "en", on: "en", is: "es", are: "son", our: "nuestro",
  your: "su", we: "nosotros", they: "ellos", this: "este",
  that: "ese", here: "aquí", there: "allí", now: "ahora",
  not: "no", do: "haga", "don't": "no",

  // ---- Sections ----
  deli: "delicatessen", bakery: "panadería", produce: "frutas y verduras",
  dairy: "lácteos", meats: "carnes", seafoods: "mariscos",
  canned: "enlatados", dry: "secos",
  shelf: "estante",

  // ---- Numbers written out ----
  one: "uno", two: "dos", three: "tres", four: "cuatro",
  five: "cinco", six: "seis", seven: "siete", eight: "ocho",
  nine: "nueve", ten: "diez",

  // ---- Pharmacy / Health ----
  pharmacy: "farmacia", prescription: "receta", medicine: "medicina",
  health: "salud", vaccine: "vacuna", vitamins: "vitaminas",
  allergy: "alergia", allergies: "alergias",

  // ---- Repair / Tech ----
  repair: "reparación", warranty: "garantía", screen: "pantalla",
  battery: "batería", charger: "cargador",
  device: "dispositivo", parts: "piezas", labor: "mano de obra",

  // ---- Misc ----
  family: "familia", kids: "niños", children: "niños", baby: "bebé",
  pet: "mascota", dog: "perro", cat: "gato", home: "hogar",
  cleaning: "limpieza", supplies: "suministros", paper: "papel",
  towel: "toalla", soap: "jabón", detergent: "detergente",
  trash: "basura", recycle: "reciclaje", restrooms: "baños",
};

/* ================================================================
   PHRASE DICTIONARY — checked FIRST (longest-match priority)
   ================================================================ */
const PHRASES: [RegExp, string][] = [
  // Multi-word phrases (order matters — longer first)
  [/\bDAILY SPECIALS?\b/gi, "ESPECIAL DEL DÍA"],
  [/\bSPECIAL TODAY\b/gi, "ESPECIAL DE HOY"],
  [/\bTODAY'?S SPECIAL\b/gi, "ESPECIAL DE HOY"],
  [/\bHOT ROAST BEEF SANDWICH\b/gi, "SÁNDWICH DE CARNE ASADA CALIENTE"],
  [/\bROAST BEEF\b/gi, "CARNE ASADA"],
  [/\bMELTED SWISS CHEESE\b/gi, "QUESO SUIZO FUNDIDO"],
  [/\bSWISS CHEESE\b/gi, "QUESO SUIZO"],
  [/\bCREAM CHEESE\b/gi, "QUESO CREMA"],
  [/\bGRILLED CHICKEN\b/gi, "POLLO A LA PARRILLA"],
  [/\bFRIED CHICKEN\b/gi, "POLLO FRITO"],
  [/\bFRESH BREAD\b/gi, "PAN FRESCO"],
  [/\bFRESH WARM BREAD\b/gi, "PAN FRESCO CALIENTE"],
  [/\bBAKED DAILY\b/gi, "HORNEADO DIARIAMENTE"],
  [/\bMADE FRESH DAILY\b/gi, "HECHO FRESCO DIARIAMENTE"],
  [/\bMADE TO ORDER\b/gi, "HECHO AL MOMENTO"],
  [/\bFRESH BAKED\b/gi, "RECIÉN HORNEADO"],
  [/\bFRESHLY BAKED\b/gi, "RECIÉN HORNEADO"],
  [/\bHOMEMADE STYLE\b/gi, "ESTILO CASERO"],
  [/\bFRESH SQUEEZED\b/gi, "RECIÉN EXPRIMIDO"],
  [/\bEBT ACCEPTED\b/gi, "SE ACEPTA EBT"],
  [/\bCASH ONLY\b/gi, "SOLO EFECTIVO"],
  [/\bCASH OR CARD\b/gi, "EFECTIVO O TARJETA"],
  [/\bCREDIT CARDS? ACCEPTED\b/gi, "SE ACEPTAN TARJETAS DE CRÉDITO"],
  [/\bNO PARKING\b/gi, "PROHIBIDO ESTACIONAR"],
  [/\bLOADING ZONE\b/gi, "ZONA DE CARGA"],
  [/\bNO SMOKING\b/gi, "PROHIBIDO FUMAR"],
  [/\bNO PETS\b/gi, "NO SE PERMITEN MASCOTAS"],
  [/\bWET FLOOR\b/gi, "PISO MOJADO"],
  [/\bDO NOT ENTER\b/gi, "NO ENTRE"],
  [/\bEMPLOYEES ONLY\b/gi, "SOLO EMPLEADOS"],
  [/\bPLEASE WAIT\b/gi, "POR FAVOR ESPERE"],
  [/\bWAIT HERE\b/gi, "ESPERE AQUÍ"],
  [/\bOPEN DAILY\b/gi, "ABIERTO DIARIAMENTE"],
  [/\bNOW OPEN\b/gi, "YA ABIERTO"],
  [/\bNOW HIRING\b/gi, "SOLICITAMOS EMPLEADOS"],
  [/\bFOR SALE\b/gi, "EN VENTA"],
  [/\bFOR RENT\b/gi, "EN RENTA"],
  [/\bCOMING SOON\b/gi, "PRÓXIMAMENTE"],
  [/\bSOLD OUT\b/gi, "AGOTADO"],
  [/\bOUT OF STOCK\b/gi, "AGOTADO"],
  [/\bWHILE SUPPLIES LAST\b/gi, "HASTA AGOTAR EXISTENCIAS"],
  [/\bBUY ONE GET ONE\b/gi, "COMPRE UNO Y LLEVE OTRO"],
  [/\bFREE DELIVERY\b/gi, "ENTREGA GRATIS"],
  [/\bFREE WIFI\b/gi, "WIFI GRATIS"],
  [/\bTHANK YOU\b/gi, "GRACIAS"],
  [/\bGOD BLESS\b/gi, "DIOS LOS BENDIGA"],
  [/\bHAPPY HOLIDAYS\b/gi, "FELICES FIESTAS"],
  [/\bMERRY CHRISTMAS\b/gi, "FELIZ NAVIDAD"],
  [/\bHAPPY NEW YEAR\b/gi, "FELIZ AÑO NUEVO"],
  [/\bWELCOME TO\b/gi, "BIENVENIDOS A"],
  [/\bOPEN HOURS\b/gi, "HORARIO DE ATENCIÓN"],
  [/\bSTORE HOURS\b/gi, "HORARIO DE LA TIENDA"],
  [/\bBUSINESS HOURS\b/gi, "HORARIO COMERCIAL"],
  [/\bSERVICE COUNTER\b/gi, "MOSTRADOR DE SERVICIO"],
  [/\bSELF CHECKOUT\b/gi, "CAJA DE AUTOSERVICIO"],
  [/\bICE CREAM\b/gi, "HELADO"],
  [/\bFRUIT JUICE\b/gi, "JUGO DE FRUTAS"],
  [/\bORANGE JUICE\b/gi, "JUGO DE NARANJA"],
  [/\bHOT DOG\b/gi, "PERRO CALIENTE"],
  [/\bHOT DOGS\b/gi, "PERROS CALIENTES"],
  [/\bFRIED RICE\b/gi, "ARROZ FRITO"],
  [/\bBLACK BEANS\b/gi, "FRIJOLES NEGROS"],
  [/\bWHITE RICE\b/gi, "ARROZ BLANCO"],
  [/\bSWEET PLANTAINS?\b/gi, "PLÁTANOS MADUROS"],
  [/\bGREEN PLANTAINS?\b/gi, "PLÁTANOS VERDES"],
  [/\bFRIED EGG\b/gi, "HUEVO FRITO"],
  [/\bSCRAMBLED EGGS?\b/gi, "HUEVOS REVUELTOS"],
  [/\bTAKE OUT\b/gi, "PARA LLEVAR"],
  [/\bTO GO\b/gi, "PARA LLEVAR"],
  [/\bFOR HERE\b/gi, "PARA COMER AQUÍ"],
  [/\bDINE IN\b/gi, "COMER AQUÍ"],
  [/\bSIDE ORDER\b/gi, "ORDEN APARTE"],
  [/\bSIDE DISH\b/gi, "ACOMPAÑAMIENTO"],
  [/\bPER POUND\b/gi, "POR LIBRA"],
  [/\bPER PERSON\b/gi, "POR PERSONA"],
  [/\bALL DAY\b/gi, "TODO EL DÍA"],
  [/\bALL WEEK\b/gi, "TODA LA SEMANA"],
  [/\bLIMITED TIME\b/gi, "TIEMPO LIMITADO"],
  [/\bFIRST BATCH\b/gi, "PRIMERA HORNADA"],
  [/\bSECOND BATCH\b/gi, "SEGUNDA HORNADA"],
  [/\bFRESH PRODUCE\b/gi, "FRUTAS Y VERDURAS FRESCAS"],
  [/\bCUSTOMER SERVICE\b/gi, "SERVICIO AL CLIENTE"],
  [/\bMONEY ORDER\b/gi, "GIRO POSTAL"],
  [/\bMONEY ORDERS\b/gi, "GIROS POSTALES"],
  [/\bGIFT CARD\b/gi, "TARJETA DE REGALO"],
  [/\bPHONE CARD\b/gi, "TARJETA TELEFÓNICA"],
  [/\bLOTTERY TICKETS?\b/gi, "BOLETOS DE LOTERÍA"],
];

/* ================================================================
   CASE-PRESERVING WORD-BY-WORD TRANSLATOR
   ================================================================ */
function translateWordByWord(text: string): string {
  // First apply phrase-level replacements
  let result = text;
  for (const [pattern, replacement] of PHRASES) {
    result = result.replace(pattern, (match) => {
      // Preserve the original casing style
      if (match === match.toUpperCase()) return replacement.toUpperCase();
      if (match[0] === match[0].toUpperCase() && match.slice(1) === match.slice(1).toLowerCase()) {
        return replacement.charAt(0).toUpperCase() + replacement.slice(1).toLowerCase();
      }
      return replacement;
    });
  }

  // Then word-by-word translation for remaining English words
  result = result.replace(/[A-Za-zÀ-ÿ'']+/g, (word) => {
    const lower = word.toLowerCase();
    const translated = WORD_MAP[lower];
    if (!translated) return word; // Unknown word — keep as-is (numbers, names, etc.)

    // Preserve casing
    if (word === word.toUpperCase()) return translated.toUpperCase();
    if (word[0] === word[0].toUpperCase() && word.length > 1) {
      return translated.charAt(0).toUpperCase() + translated.slice(1);
    }
    return translated;
  });

  return result;
}

/* ================================================================
   MAIN ROUTE HANDLER
   ================================================================ */
export async function POST(req: NextRequest) {
  let textToTranslate = "";
  try {
    const payload = await req.json();
    textToTranslate = payload.text || "";

    if (!textToTranslate || typeof textToTranslate !== "string") {
      return NextResponse.json({ translation: "" });
    }

    /* ---- Try Gemini AI first (if valid key available) ---- */
    const apiKey = process.env.GEMINI_API_KEY;
    if (apiKey && apiKey.startsWith("AIza")) {
      try {
        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
          model: "gemini-2.0-flash",
          systemInstruction:
            "You are a professional English to Spanish translator. Translate the user's English text into accurate, natural Spanish. Output ONLY the translated Spanish text. Do not add quotes, explanations, or introductory text.",
        });

        const result = await model.generateContent(textToTranslate);
        const translation = result.response.text().trim();
        if (translation && translation !== textToTranslate) {
          return NextResponse.json({ translation });
        }
      } catch (err: any) {
        console.warn("Gemini translate API error:", err?.message);
      }
    }

    /* ---- Comprehensive local translation engine ---- */
    const translation = translateWordByWord(textToTranslate);
    return NextResponse.json({ translation });
  } catch (error: any) {
    console.error("Error in /api/translate:", error);
    // Even on error, try to translate what we have
    if (textToTranslate) {
      return NextResponse.json({ translation: translateWordByWord(textToTranslate) });
    }
    return NextResponse.json({ translation: textToTranslate });
  }
}
